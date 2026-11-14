"""Application service orchestrating wellness observations, check-ins, dashboard, trends, education, and research."""
from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Dict, List, Optional, Tuple

from artemis_health.core.config import get_settings
from artemis_health.core.constants import (
    COMPATIBLE_QUERY_GROUPS,
    INDICATOR_CATALOG,
    NON_CLINICAL_DISCLAIMER,
    resolve_indicator_spec,
)
from artemis_health.core.exceptions import DomainValidationError, ResourceNotFoundError
from artemis_health.models.entities import (
    BaselineComparison,
    CheckinRecord,
    ObservationRecord,
    ProfileRecord,
)
from artemis_health.repositories.base import WellnessRepository
from artemis_health.schemas.checkins import CheckinCreate, CheckinCreateResponse, CheckinOut
from artemis_health.schemas.common import HealthResponse
from artemis_health.schemas.education import EducationalContentListResponse, EducationalContentOut
from artemis_health.schemas.indicators import IndicatorListResponse, IndicatorOut
from artemis_health.schemas.observations import (
    BaselineComparisonOut,
    DashboardResponse,
    IndicatorSummaryCardOut,
    IndicatorTrendSeriesOut,
    ObservationCreate,
    ObservationCreateResponse,
    ObservationListResponse,
    ObservationOut,
    TrendPointOut,
    TrendsResponse,
)
from artemis_health.schemas.profiles import ProfileListResponse, ProfileOut
from artemis_health.schemas.research import ResearchDatasetOut, ResearchDatasetsResponse
from artemis_health.services.baseline_service import compute_personal_baseline, parse_utc_timestamp

DASHBOARD_SLOTS: Tuple[Tuple[str, str, Tuple[str, ...]], ...] = (
    ("resting_hr_bpm", "Frecuencia cardíaca en reposo", ("resting_hr_bpm",)),
    ("sleep_duration_h", "Duración del sueño", ("sleep_duration_h",)),
    ("fatigue", "Fatiga percibida", ("fatigue", "samn_perelli")),
    ("perceived_stress", "Estrés percibido", ("perceived_stress", "stress_vas")),
)


def _normalize_date_filter(raw: Optional[str], *, is_end: bool = False) -> Optional[str]:
    if raw is None or not raw.strip():
        return None
    text = raw.strip()
    try:
        if len(text) == 10 and "T" not in text:
            d = date.fromisoformat(text)
            if is_end:
                return f"{d.isoformat()}T23:59:59Z"
            return f"{d.isoformat()}T00:00:00Z"
        dt = parse_utc_timestamp(text)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise DomainValidationError(
            f"Filtro de fecha inválido: '{raw}'. Use formato ISO 8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SSZ).",
            fields={"date_filter": [f"Valor inválido: {raw}"]},
        ) from exc


class WellnessService:
    """Business logic layer for ARTEMIS HEALTH."""

    def __init__(self, repository: WellnessRepository) -> None:
        self._repo = repository

    def get_health(self) -> HealthResponse:
        settings = get_settings()
        is_connected, backend_name = self._repo.check_health()
        return HealthResponse(
            status="ok" if is_connected else "degraded",
            service=settings.app_name,
            version=settings.app_version,
            mode=settings.artemis_mode,
            storage_backend=backend_name,
            database_connected=is_connected,
            database_checked=True,
            supabase_configured=bool(settings.has_postgres_config or settings.has_supabase_rest_config),
            disclaimer=NON_CLINICAL_DISCLAIMER,
        )

    def list_profiles(self) -> ProfileListResponse:
        records = self._repo.list_profiles(namespace="demo")
        items = [self._to_profile_out(r) for r in records]
        return ProfileListResponse(
            namespace="demo",
            data_label="SIMULADO",
            count=len(items),
            profiles=items,
        )

    def list_indicators(self) -> IndicatorListResponse:
        records = self._repo.list_indicators()
        items = [
            IndicatorOut(
                key=r.key,
                label=r.label,
                description=r.description,
                unit=r.unit,
                allowed_units=r.allowed_units,
                context=r.context,
                minimum=r.minimum,
                maximum=r.maximum,
                integer_only=r.integer_only,
            )
            for r in records
        ]
        return IndicatorListResponse(
            count=len(items),
            disclaimer=NON_CLINICAL_DISCLAIMER,
            indicators=items,
        )

    def create_observation(self, payload: ObservationCreate) -> Tuple[ObservationCreateResponse, int]:
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = ObservationRecord(
            id=payload.id,
            profile_id=payload.profile_id,
            namespace="demo",
            indicator=payload.indicator,
            value=payload.value,
            source_value=payload.value,
            unit=payload.unit,
            context=payload.context or INDICATOR_CATALOG[payload.indicator].default_context,
            measured_at=payload.measured_at,
            mission_day=payload.mission_day,
            origin_type=payload.origin_type,
            capture_method=payload.capture_method,
            source_reference=payload.source_reference,
            quality_flag=payload.quality_flag,
            quality_flags=payload.quality_flags or [payload.quality_flag],
            created_at=now_iso,
        )

        stored, is_idempotent = self._repo.save_observation(record)

        history = self._repo.list_observations(
            stored.profile_id,
            indicator=stored.indicator,
            origin_type=stored.origin_type,
            namespace="demo",
        )
        comparison = compute_personal_baseline(
            candidates=history,
            profile_id=stored.profile_id,
            indicator=stored.indicator,
            unit=stored.unit,
            context=stored.context,
            origin_type=stored.origin_type,
            reference_timestamp=stored.measured_at,
            current_value=stored.value,
            current_observation_id=stored.id,
        )

        http_status = 200 if is_idempotent else 201
        response = ObservationCreateResponse(
            status="idempotent_replay" if is_idempotent else "created",
            save_status="GUARDADO",
            idempotent=is_idempotent,
            observation=self._to_observation_out(stored),
            comparison=self._to_comparison_out(comparison),
        )
        return response, http_status

    def list_observations(
        self,
        profile_id: str,
        *,
        indicator: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        origin_type: Optional[str] = None,
        strict_indicator: bool = False,
        limit: Optional[int] = None,
    ) -> ObservationListResponse:
        profile = self._resolve_profile(profile_id)
        canonical_indicator: Optional[str] = None
        compatible_group: Optional[Tuple[str, ...]] = None

        if indicator is not None and indicator.strip():
            spec = resolve_indicator_spec(indicator)
            if spec is None:
                raise DomainValidationError(
                    f"Indicador de filtro no válido: '{indicator}'.",
                    fields={"indicator": [f"Indicador '{indicator}' no existe"]},
                )
            canonical_indicator = spec.key
            if not strict_indicator:
                exact_matches = self._repo.list_observations(
                    profile.id,
                    indicator=canonical_indicator,
                    namespace="demo",
                    limit=1,
                )
                if not exact_matches:
                    compatible_group = COMPATIBLE_QUERY_GROUPS.get(canonical_indicator, (canonical_indicator,))

        from_ts = _normalize_date_filter(from_date, is_end=False)
        to_ts = _normalize_date_filter(to_date, is_end=True)
        if from_ts and to_ts and from_ts > to_ts:
            raise DomainValidationError(
                "El rango de fechas es inválido: 'from' no puede ser posterior a 'to'.",
                fields={"from": ["Fecha inicial posterior a la final"]},
            )

        records = self._repo.list_observations(
            profile.id,
            indicator=canonical_indicator if not compatible_group else None,
            compatible_indicators=compatible_group,
            from_timestamp=from_ts,
            to_timestamp=to_ts,
            origin_type=origin_type,
            namespace="demo",
            limit=limit,
        )
        items = [self._to_observation_out(r) for r in records]
        return ObservationListResponse(
            profile_id=profile.id,
            namespace="demo",
            data_label="SIMULADO",
            indicator_filter=canonical_indicator,
            from_filter=from_ts,
            to_filter=to_ts,
            count=len(items),
            observations=items,
        )

    def get_dashboard(
        self,
        profile_id: str,
        *,
        at_timestamp: Optional[str] = None,
    ) -> DashboardResponse:
        profile = self._resolve_profile(profile_id)
        cursor_ts = _normalize_date_filter(at_timestamp, is_end=True) if at_timestamp else None
        all_obs = self._repo.list_observations(
            profile.id,
            to_timestamp=cursor_ts,
            namespace="demo",
        )

        cards_list: List[IndicatorSummaryCardOut] = []
        cards_dict: Dict[str, IndicatorSummaryCardOut] = {}
        latest_overall: Optional[str] = None

        for slot_key, slot_label, candidate_keys in DASHBOARD_SLOTS:
            slot_obs = [o for o in all_obs if o.indicator in candidate_keys]
            if slot_obs:
                latest = slot_obs[-1]
                if latest_overall is None or latest.measured_at > latest_overall:
                    latest_overall = latest.measured_at
                same_series = [
                    o
                    for o in slot_obs
                    if o.indicator == latest.indicator
                    and o.unit == latest.unit
                    and o.context == latest.context
                    and o.origin_type == latest.origin_type
                ]
                comp = compute_personal_baseline(
                    candidates=same_series,
                    profile_id=profile.id,
                    indicator=latest.indicator,
                    unit=latest.unit,
                    context=latest.context,
                    origin_type=latest.origin_type,
                    reference_timestamp=latest.measured_at,
                    current_value=latest.value,
                    current_observation_id=latest.id,
                )
                card = IndicatorSummaryCardOut(
                    slot=slot_key,
                    indicator=latest.indicator,
                    label=slot_label,
                    unit=latest.unit,
                    context=latest.context,
                    latest_observation=self._to_observation_out(latest),
                    comparison=self._to_comparison_out(comp),
                )
            else:
                spec = INDICATOR_CATALOG[slot_key]
                ref_now = cursor_ts or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                comp = compute_personal_baseline(
                    candidates=[],
                    profile_id=profile.id,
                    indicator=spec.key,
                    unit=spec.canonical_unit,
                    context=spec.default_context,
                    origin_type="synthetic",
                    reference_timestamp=ref_now,
                    current_value=None,
                )
                card = IndicatorSummaryCardOut(
                    slot=slot_key,
                    indicator=spec.key,
                    label=slot_label,
                    unit=spec.canonical_unit,
                    context=spec.default_context,
                    latest_observation=None,
                    comparison=self._to_comparison_out(comp),
                )
            cards_list.append(card)
            cards_dict[slot_key] = card

        return DashboardResponse(
            profile=self._to_profile_out(profile).model_dump(),
            namespace="demo",
            data_label="SIMULADO",
            is_simulated=True,
            cursor_timestamp=cursor_ts,
            latest_recorded_at=latest_overall,
            disclaimer=NON_CLINICAL_DISCLAIMER,
            indicators_summary=cards_list,
            cards=cards_dict,
        )

    def get_comparison(
        self,
        profile_id: str,
        *,
        indicator: str,
        at_timestamp: Optional[str] = None,
        origin_type: Optional[str] = None,
    ) -> BaselineComparisonOut:
        profile = self._resolve_profile(profile_id)
        spec = resolve_indicator_spec(indicator)
        if spec is None:
            raise DomainValidationError(
                f"Indicador inválido: '{indicator}'.",
                fields={"indicator": ["Indicador no reconocido"]},
            )
        cursor_ts = _normalize_date_filter(at_timestamp, is_end=True) if at_timestamp else None
        obs_list = self._repo.list_observations(
            profile.id,
            compatible_indicators=COMPATIBLE_QUERY_GROUPS.get(spec.key, (spec.key,)),
            to_timestamp=cursor_ts,
            origin_type=origin_type,
            namespace="demo",
        )
        if not obs_list:
            ref_ts = cursor_ts or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            comp = compute_personal_baseline(
                candidates=[],
                profile_id=profile.id,
                indicator=spec.key,
                unit=spec.canonical_unit,
                context=spec.default_context,
                origin_type=origin_type or "user_report",
                reference_timestamp=ref_ts,
                current_value=None,
            )
            return self._to_comparison_out(comp)

        latest = obs_list[-1]
        comp = compute_personal_baseline(
            candidates=obs_list,
            profile_id=profile.id,
            indicator=latest.indicator,
            unit=latest.unit,
            context=latest.context,
            origin_type=latest.origin_type,
            reference_timestamp=latest.measured_at,
            current_value=latest.value,
            current_observation_id=latest.id,
        )
        return self._to_comparison_out(comp)

    def get_trends(
        self,
        profile_id: str,
        *,
        indicator: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        origin_type: Optional[str] = None,
    ) -> TrendsResponse:
        profile = self._resolve_profile(profile_id)
        from_ts = _normalize_date_filter(from_date, is_end=False)
        to_ts = _normalize_date_filter(to_date, is_end=True)
        if from_ts and to_ts and from_ts > to_ts:
            raise DomainValidationError(
                "El rango de fechas es inválido: 'from' no puede ser posterior a 'to'.",
                fields={"from": ["Fecha inicial posterior a la final"]},
            )

        selected_slots = DASHBOARD_SLOTS
        if indicator:
            spec = resolve_indicator_spec(indicator)
            if spec is None:
                raise DomainValidationError(
                    f"Indicador inválido: '{indicator}'.",
                    fields={"indicator": ["Indicador no reconocido"]},
                )
            selected_slots = tuple(
                s for s in DASHBOARD_SLOTS if spec.key in s[2] or s[0] == spec.key
            )

        all_obs = self._repo.list_observations(
            profile.id,
            from_timestamp=from_ts,
            to_timestamp=to_ts,
            origin_type=origin_type,
            namespace="demo",
        )

        series_by_indicator: Dict[str, IndicatorTrendSeriesOut] = {}
        trends_list: List[IndicatorTrendSeriesOut] = []

        for slot_key, slot_label, candidate_keys in selected_slots:
            slot_obs = [o for o in all_obs if o.indicator in candidate_keys]
            active_key = slot_obs[-1].indicator if slot_obs else slot_key
            spec = INDICATOR_CATALOG[active_key]

            points: List[TrendPointOut] = []
            valid_count = 0
            null_count = 0
            for o in slot_obs:
                is_gap = o.value is None
                if is_gap:
                    null_count += 1
                else:
                    valid_count += 1
                points.append(
                    TrendPointOut(
                        id=o.id,
                        date=o.measured_at[:10],
                        measured_at=o.measured_at,
                        mission_day=o.mission_day,
                        value=o.value,
                        source_value=o.source_value,
                        unit=o.unit,
                        origin_type=o.origin_type,
                        capture_method=o.capture_method,
                        quality_flag=o.quality_flag,
                        quality_flags=o.quality_flags,
                        is_gap=is_gap,
                    )
                )

            baseline_med: Optional[float] = None
            suff = False
            if slot_obs:
                latest = slot_obs[-1]
                comp = compute_personal_baseline(
                    candidates=slot_obs,
                    profile_id=profile.id,
                    indicator=latest.indicator,
                    unit=latest.unit,
                    context=latest.context,
                    origin_type=latest.origin_type,
                    reference_timestamp=latest.measured_at,
                    current_value=latest.value,
                    current_observation_id=latest.id,
                )
                baseline_med = comp.baseline_median
                suff = comp.sufficient_history

            series_obj = IndicatorTrendSeriesOut(
                indicator=active_key,
                label=slot_label,
                unit=spec.canonical_unit,
                context=spec.default_context,
                points_count=len(points),
                valid_points_count=valid_count,
                null_gaps_count=null_count,
                interpolation_applied=False,
                baseline_median=baseline_med,
                sufficient_history=suff,
                series=points,
            )
            series_by_indicator[slot_key] = series_obj
            if active_key != slot_key:
                series_by_indicator[active_key] = series_obj
            trends_list.append(series_obj)

        return TrendsResponse(
            profile_id=profile.id,
            alias=profile.alias,
            namespace="demo",
            data_label="SIMULADO",
            interpolation_applied=False,
            disclaimer=NON_CLINICAL_DISCLAIMER,
            series_by_indicator=series_by_indicator,
            trends=trends_list,
        )

    def create_checkin(self, payload: CheckinCreate) -> Tuple[CheckinCreateResponse, int]:
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = CheckinRecord(
            id=payload.id,
            profile_id=payload.profile_id,
            namespace="demo",
            checkin_date=payload.date,
            fatigue=payload.fatigue,
            perceived_stress=payload.perceived_stress,
            notes=payload.notes,
            origin_type=payload.origin_type,
            capture_method=payload.capture_method,
            quality_flag="ok",
            created_at=now_iso,
        )
        stored_checkin, is_idempotent = self._repo.save_checkin(record)

        # Also create/ensure deterministic paired observations for fatigue (1-5) and perceived_stress (1-5)
        measured_at = f"{stored_checkin.checkin_date}T07:00:00Z"
        launch_date = date(2026, 3, 1)
        mission_day = max(1, (date.fromisoformat(stored_checkin.checkin_date) - launch_date).days + 1)

        fatigue_obs_id = str(uuid.uuid5(uuid.UUID(stored_checkin.id), "artemis:checkin:fatigue"))
        stress_obs_id = str(uuid.uuid5(uuid.UUID(stored_checkin.id), "artemis:checkin:perceived_stress"))

        if not is_idempotent:
            for obs_id, ind_key, val, ctx in (
                (fatigue_obs_id, "fatigue", float(stored_checkin.fatigue), "fatigue_report"),
                (stress_obs_id, "perceived_stress", float(stored_checkin.perceived_stress), "stress_report"),
            ):
                obs = ObservationRecord(
                    id=obs_id,
                    profile_id=stored_checkin.profile_id,
                    namespace="demo",
                    indicator=ind_key,
                    value=val,
                    source_value=val,
                    unit="scale_1_5",
                    context=ctx,
                    measured_at=measured_at,
                    mission_day=mission_day,
                    origin_type=stored_checkin.origin_type,
                    capture_method=stored_checkin.capture_method,
                    source_reference=f"checkin:{stored_checkin.id}",
                    quality_flag="ok",
                    quality_flags=["ok"],
                    created_at=now_iso,
                )
                self._repo.save_observation(obs)

        http_status = 200 if is_idempotent else 201
        return (
            CheckinCreateResponse(
                status="idempotent_replay" if is_idempotent else "created",
                save_status="GUARDADO",
                idempotent=is_idempotent,
                checkin=CheckinOut(
                    id=stored_checkin.id,
                    profile_id=stored_checkin.profile_id,
                    namespace=stored_checkin.namespace,
                    date=stored_checkin.checkin_date,
                    fatigue=stored_checkin.fatigue,
                    perceived_stress=stored_checkin.perceived_stress,
                    notes=stored_checkin.notes,
                    origin_type=stored_checkin.origin_type,
                    capture_method=stored_checkin.capture_method,
                    quality_flag=stored_checkin.quality_flag,
                    created_at=stored_checkin.created_at,
                ),
                generated_observation_ids=[fatigue_obs_id, stress_obs_id],
                disclaimer=NON_CLINICAL_DISCLAIMER,
            ),
            http_status,
        )

    def get_educational_content(self, indicator: Optional[str] = None) -> EducationalContentListResponse:
        filter_key: Optional[str] = None
        if indicator:
            spec = resolve_indicator_spec(indicator)
            if spec is None:
                raise ResourceNotFoundError(
                    f"No existe ficha educativa para el indicador '{indicator}'.",
                    fields={"indicator": [indicator]},
                )
            filter_key = spec.dashboard_slot
        records = self._repo.list_educational_content(indicator=filter_key)
        items = [
            EducationalContentOut(
                id=r.id,
                indicator=r.indicator,
                title=r.title,
                description=r.description,
                unit=r.unit,
                limitations=r.limitations,
                bibliographic_reference=r.bibliographic_reference,
                created_at=r.created_at,
            )
            for r in records
        ]
        return EducationalContentListResponse(
            count=len(items),
            disclaimer=NON_CLINICAL_DISCLAIMER,
            items=items,
        )

    def get_research_datasets(self) -> ResearchDatasetsResponse:
        records = self._repo.list_research_datasets()
        items = [
            ResearchDatasetOut(
                id=r.id,
                dataset_key=r.dataset_key,
                file_name=r.file_name,
                title=r.title,
                namespace=r.namespace,
                origin_type=r.origin_type,
                capture_method=r.capture_method,
                study_context=r.study_context,
                is_inflight_measurement=r.is_inflight_measurement,
                is_personal_radiation_dose=r.is_personal_radiation_dose,
                included_in_personal_calculations=False,
                row_count=r.row_count,
                sha256=r.sha256,
                limitations=r.limitations,
                source_reference=r.source_reference,
                quality_flag=r.quality_flag,
                created_at=r.created_at,
            )
            for r in records
        ]
        return ResearchDatasetsResponse(
            namespace="research",
            isolation_guaranteed=True,
            count=len(items),
            datasets=items,
        )

    def _resolve_profile(self, profile_id: str) -> ProfileRecord:
        pid = profile_id.strip()
        profile = self._repo.get_profile(pid, namespace="demo")
        if profile is None:
            raise ResourceNotFoundError(
                f"El perfil ficticio '{pid}' no fue encontrado en el espacio 'demo'.",
                fields={"profile_id": [pid]},
            )
        return profile

    @staticmethod
    def _to_profile_out(record: ProfileRecord) -> ProfileOut:
        return ProfileOut(
            id=record.id,
            uuid=record.profile_uuid,
            alias=record.alias,
            display_name=record.display_name,
            profile_type=record.profile_type,
            role=record.role,
            mission=record.mission,
            namespace=record.namespace,
            is_simulated=True,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    @staticmethod
    def _to_observation_out(record: ObservationRecord) -> ObservationOut:
        return ObservationOut(
            id=record.id,
            profile_id=record.profile_id,
            namespace=record.namespace,
            indicator=record.indicator,
            value=record.value,
            source_value=record.source_value,
            unit=record.unit,
            context=record.context,
            measured_at=record.measured_at,
            timestamp=record.measured_at,
            mission_day=record.mission_day,
            origin_type=record.origin_type,
            capture_method=record.capture_method,
            source_reference=record.source_reference,
            quality_flag=record.quality_flag,
            quality_flags=record.quality_flags,
            is_simulated=(record.origin_type == "synthetic"),
            created_at=record.created_at,
        )

    @staticmethod
    def _to_comparison_out(comp: BaselineComparison) -> BaselineComparisonOut:
        return BaselineComparisonOut(
            indicator=comp.indicator,
            unit=comp.unit,
            context=comp.context,
            origin_type=comp.origin_type,
            rule_version=comp.rule_version,
            reference_timestamp=comp.reference_timestamp,
            current_value=comp.current_value,
            baseline_median=comp.baseline_median,
            difference=comp.difference,
            sufficient_history=comp.sufficient_history,
            status=comp.status,
            days_used=comp.days_used,
            minimum_days_required=comp.minimum_days_required,
            window_days=comp.window_days,
            max_days=comp.max_days,
            period_start=comp.period_start,
            period_end=comp.period_end,
            descriptive_notice=comp.descriptive_notice,
            reference_observation_ids=comp.reference_observation_ids,
        )
