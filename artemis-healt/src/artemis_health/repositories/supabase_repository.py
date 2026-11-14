"""Supabase PostgreSQL and REST repository with parameterized queries and strict error handling."""
from __future__ import annotations

import json
import math
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, List, Optional, Tuple

import httpx

from artemis_health.core.config import Settings, get_settings
from artemis_health.core.constants import INDICATOR_CATALOG
from artemis_health.core.exceptions import ObservationConflictError, SupabaseUnavailableError
from artemis_health.database.connection import postgres_connection
from artemis_health.database.seed import DEFAULT_EDUCATIONAL_CARDS, DEFAULT_RESEARCH_DATASETS
from artemis_health.models.entities import (
    CheckinRecord,
    EducationalContentRecord,
    IndicatorRecord,
    ObservationRecord,
    ProfileRecord,
    ResearchDatasetRecord,
)
from artemis_health.repositories.base import WellnessRepository


def _values_equal(a: Optional[float], b: Optional[float]) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-9)


class SupabasePostgresRepository(WellnessRepository):
    """Repository backed by Supabase PostgreSQL (via DATABASE_URL or Supabase REST API)."""

    def __init__(
        self,
        settings: Optional[Settings] = None,
        connection_factory: Optional[Callable[[], Any]] = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._connection_factory = connection_factory or (lambda: postgres_connection(admin=False))

    def _get_conn(self):
        try:
            return self._connection_factory()
        except SupabaseUnavailableError:
            raise
        except Exception as exc:
            raise SupabaseUnavailableError(
                "No se pudo conectar con Supabase PostgreSQL. El registro NO FUE GUARDADO."
            ) from exc

    def check_health(self) -> Tuple[bool, str]:
        if self._settings.active_backend_type == "supabase_rest":
            return self._check_rest_health(), "supabase_rest"
        try:
            with self._get_conn() as conn:
                row = conn.execute("SELECT 1 AS ok").fetchone()
                return bool(row and row.get("ok") == 1), "postgres"
        except Exception as exc:
            raise SupabaseUnavailableError(
                "Fallo en la verificación de estado de Supabase PostgreSQL."
            ) from exc

    def _check_rest_health(self) -> bool:
        if not self._settings.supabase_url:
            raise SupabaseUnavailableError("SUPABASE_URL no está configurada.")
        key = self._settings.supabase_service_role_key or self._settings.supabase_anon_key
        if not key:
            raise SupabaseUnavailableError("Clave de Supabase no configurada.")
        try:
            resp = httpx.get(
                f"{self._settings.supabase_url.rstrip('/')}/rest/v1/",
                headers={"apikey": key, "Authorization": f"Bearer {key}"},
                timeout=5.0,
            )
            if resp.status_code >= 500:
                raise SupabaseUnavailableError("Supabase REST devolvió error de servidor.")
            return resp.status_code < 400
        except SupabaseUnavailableError:
            raise
        except Exception as exc:
            raise SupabaseUnavailableError(
                "No fue posible contactar con el endpoint REST de Supabase."
            ) from exc

    def list_profiles(self, namespace: str = "demo") -> List[ProfileRecord]:
        try:
            with self._get_conn() as conn:
                rows = conn.execute(
                    "SELECT id, display_name, namespace, created_at FROM artemis.profiles WHERE namespace = %s ORDER BY id ASC",
                    (namespace,),
                ).fetchall()
                return [self._dict_to_profile(r) for r in rows]
        except SupabaseUnavailableError:
            raise
        except Exception as exc:
            raise SupabaseUnavailableError("Error al consultar perfiles en Supabase.") from exc

    def get_profile(self, profile_id: str, namespace: str = "demo") -> Optional[ProfileRecord]:
        try:
            with self._get_conn() as conn:
                row = conn.execute(
                    "SELECT id, display_name, namespace, created_at FROM artemis.profiles WHERE id = %s AND namespace = %s",
                    (profile_id, namespace),
                ).fetchone()
                return self._dict_to_profile(row) if row else None
        except SupabaseUnavailableError:
            raise
        except Exception as exc:
            raise SupabaseUnavailableError("Error al consultar el perfil en Supabase.") from exc

    def ensure_demo_profile(self, profile_id: str) -> ProfileRecord:
        existing = self.get_profile(profile_id, namespace="demo")
        if existing:
            return existing
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return ProfileRecord(
            id=profile_id,
            profile_uuid=str(uuid.uuid5(uuid.NAMESPACE_URL, f"artemis:profile:{profile_id}")),
            display_name=f"{profile_id} (DEMO)",
            alias=f"Astronauta Ficticio {profile_id} (SIMULADO)",
            profile_type="fictional_astronaut",
            role="Crew Member",
            mission="SIM-ISS-180",
            namespace="demo",
            created_at=now_iso,
            updated_at=now_iso,
        )

    def list_indicators(self) -> List[IndicatorRecord]:
        return [
            IndicatorRecord(
                key=spec.key,
                label=spec.label,
                description=spec.description,
                unit=spec.canonical_unit,
                allowed_units=list(spec.allowed_units),
                context=spec.default_context,
                minimum=spec.minimum,
                maximum=spec.maximum,
                integer_only=spec.integer_only,
            )
            for spec in INDICATOR_CATALOG.values()
        ]

    def get_observation_by_id(self, observation_id: str) -> Optional[ObservationRecord]:
        try:
            with self._get_conn() as conn:
                row = conn.execute(
                    "SELECT * FROM artemis.observations WHERE id = %s",
                    (observation_id,),
                ).fetchone()
                return self._dict_to_observation(row) if row else None
        except SupabaseUnavailableError:
            raise
        except Exception as exc:
            raise SupabaseUnavailableError("Error al recuperar la observación desde Supabase.") from exc

    def save_observation(self, observation: ObservationRecord) -> Tuple[ObservationRecord, bool]:
        try:
            with self._get_conn() as conn:
                existing_row = conn.execute(
                    "SELECT * FROM artemis.observations WHERE id = %s",
                    (observation.id,),
                ).fetchone()
                if existing_row is not None:
                    existing = self._dict_to_observation(existing_row)
                    same_payload = (
                        existing.profile_id == observation.profile_id
                        and existing.indicator == observation.indicator
                        and _values_equal(existing.value, observation.value)
                        and existing.unit == observation.unit
                        and existing.context == observation.context
                        and existing.measured_at == observation.measured_at
                        and existing.origin_type == observation.origin_type
                        and existing.capture_method == observation.capture_method
                    )
                    if same_payload:
                        return existing, True
                    raise ObservationConflictError(
                        f"El UUID '{observation.id}' ya existe en Supabase con contenido diferente.",
                        fields={"id": [observation.id]},
                    )

                conn.execute(
                    """
                    INSERT INTO artemis.observations
                    (id, profile_id, namespace, indicator, value, source_value, unit, context,
                     measured_at, mission_day, origin_type, capture_method, quality_flags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
                    """,
                    (
                        observation.id,
                        observation.profile_id,
                        observation.namespace,
                        observation.indicator,
                        observation.value,
                        observation.source_value if observation.source_value is not None else observation.value,
                        observation.unit,
                        observation.context,
                        observation.measured_at,
                        observation.mission_day,
                        observation.origin_type,
                        observation.capture_method,
                        json.dumps(observation.quality_flags or ["ok"]),
                    ),
                )
                inserted = conn.execute(
                    "SELECT * FROM artemis.observations WHERE id = %s",
                    (observation.id,),
                ).fetchone()
                return self._dict_to_observation(inserted), False
        except (ObservationConflictError, SupabaseUnavailableError):
            raise
        except Exception as exc:
            raise SupabaseUnavailableError(
                "Error en Supabase al guardar la observación. El registro NO FUE GUARDADO."
            ) from exc

    def list_observations(
        self,
        profile_id: str,
        *,
        indicator: Optional[str] = None,
        compatible_indicators: Optional[Tuple[str, ...]] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        origin_type: Optional[str] = None,
        namespace: str = "demo",
        limit: Optional[int] = None,
    ) -> List[ObservationRecord]:
        profile_ids = ["demo", "CM-01"] if profile_id == "demo" else [profile_id]
        clauses = ["profile_id = ANY(%s)", "namespace = %s"]
        params: List[Any] = [profile_ids, namespace]

        if compatible_indicators:
            clauses.append("indicator = ANY(%s)")
            params.append(list(compatible_indicators))
        elif indicator:
            clauses.append("indicator = %s")
            params.append(indicator)

        if origin_type:
            clauses.append("origin_type = %s")
            params.append(origin_type)
        if from_timestamp:
            clauses.append("measured_at >= %s")
            params.append(from_timestamp)
        if to_timestamp:
            clauses.append("measured_at <= %s")
            params.append(to_timestamp)

        sql = f"SELECT * FROM artemis.observations WHERE {' AND '.join(clauses)} ORDER BY measured_at ASC, id ASC"
        if limit is not None and limit > 0:
            sql += " LIMIT %s"
            params.append(int(limit))

        try:
            with self._get_conn() as conn:
                rows = conn.execute(sql, tuple(params)).fetchall()
                return [self._dict_to_observation(r) for r in rows]
        except SupabaseUnavailableError:
            raise
        except Exception as exc:
            raise SupabaseUnavailableError("Error al consultar historial de observaciones en Supabase.") from exc

    def save_checkin(self, checkin: CheckinRecord) -> Tuple[CheckinRecord, bool]:
        try:
            with self._get_conn() as conn:
                existing_row = conn.execute(
                    "SELECT * FROM artemis.checkins WHERE id = %s",
                    (checkin.id,),
                ).fetchone()
                if existing_row is not None:
                    existing = self._dict_to_checkin(existing_row)
                    same_payload = (
                        existing.profile_id == checkin.profile_id
                        and existing.checkin_date == checkin.checkin_date
                        and existing.fatigue == checkin.fatigue
                        and existing.perceived_stress == checkin.perceived_stress
                        and (existing.notes or None) == (checkin.notes or None)
                    )
                    if same_payload:
                        return existing, True
                    raise ObservationConflictError(
                        f"El check-in con UUID '{checkin.id}' ya existe con valores diferentes.",
                        fields={"id": [checkin.id]},
                    )

                conn.execute(
                    """
                    INSERT INTO artemis.checkins
                    (id, profile_id, namespace, checkin_date, fatigue, perceived_stress, notes, origin_type, capture_method, quality_flag)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        checkin.id,
                        checkin.profile_id,
                        checkin.namespace,
                        checkin.checkin_date,
                        checkin.fatigue,
                        checkin.perceived_stress,
                        checkin.notes,
                        checkin.origin_type,
                        checkin.capture_method,
                        checkin.quality_flag,
                    ),
                )
                inserted = conn.execute(
                    "SELECT * FROM artemis.checkins WHERE id = %s",
                    (checkin.id,),
                ).fetchone()
                return self._dict_to_checkin(inserted), False
        except (ObservationConflictError, SupabaseUnavailableError):
            raise
        except Exception as exc:
            raise SupabaseUnavailableError(
                "Error en Supabase al guardar el check-in. El registro NO FUE GUARDADO."
            ) from exc

    def list_checkins(self, profile_id: str) -> List[CheckinRecord]:
        profile_ids = ["demo", "CM-01"] if profile_id == "demo" else [profile_id]
        try:
            with self._get_conn() as conn:
                rows = conn.execute(
                    "SELECT * FROM artemis.checkins WHERE profile_id = ANY(%s) AND namespace = 'demo' ORDER BY checkin_date DESC, created_at DESC",
                    (profile_ids,),
                ).fetchall()
                return [self._dict_to_checkin(r) for r in rows]
        except SupabaseUnavailableError:
            raise
        except Exception as exc:
            raise SupabaseUnavailableError("Error al consultar check-ins en Supabase.") from exc

    def list_educational_content(self, indicator: Optional[str] = None) -> List[EducationalContentRecord]:
        cards = [
            EducationalContentRecord(
                id=c["id"],
                indicator=c["indicator"],
                title=c["title"],
                description=c["description"],
                unit=c["unit"],
                limitations=c["limitations"],
                bibliographic_reference=c["bibliographic_reference"],
                created_at=c["created_at"],
            )
            for c in DEFAULT_EDUCATIONAL_CARDS
        ]
        if indicator:
            return [c for c in cards if c.indicator == indicator]
        return cards

    def list_research_datasets(self) -> List[ResearchDatasetRecord]:
        return [
            ResearchDatasetRecord(
                id=d["id"],
                dataset_key=d["dataset_key"],
                file_name=d["file_name"],
                title=d["title"],
                namespace=d["namespace"],
                origin_type=d["origin_type"],
                capture_method=d["capture_method"],
                study_context=d["study_context"],
                is_inflight_measurement=bool(d["is_inflight_measurement"]),
                is_personal_radiation_dose=bool(d["is_personal_radiation_dose"]),
                included_in_personal_calculations=False,
                row_count=int(d["row_count"]),
                sha256=d["sha256"],
                limitations=d["limitations"],
                source_reference=d["source_reference"],
                quality_flag=d["quality_flag"],
                created_at=d["created_at"],
            )
            for d in DEFAULT_RESEARCH_DATASETS
        ]

    @staticmethod
    def _dict_to_profile(row: dict) -> ProfileRecord:
        pid = str(row["id"])
        created = str(row.get("created_at", "2026-03-01T00:00:00Z"))
        return ProfileRecord(
            id=pid,
            profile_uuid=str(row.get("profile_uuid") or uuid.uuid5(uuid.NAMESPACE_URL, f"artemis:profile:{pid}")),
            display_name=str(row.get("display_name", pid)),
            alias=str(row.get("alias") or f"{row.get('display_name', pid)} (SIMULADO)"),
            profile_type=str(row.get("profile_type", "fictional_astronaut")),
            role=str(row.get("role", "Crew Member")),
            mission=str(row.get("mission", "SIM-ISS-180")),
            namespace=str(row.get("namespace", "demo")),
            created_at=created,
            updated_at=str(row.get("updated_at", created)),
        )

    @staticmethod
    def _dict_to_observation(row: dict) -> ObservationRecord:
        raw_flags = row.get("quality_flags", ["ok"])
        if isinstance(raw_flags, str):
            flags = json.loads(raw_flags)
        elif isinstance(raw_flags, list):
            flags = raw_flags
        else:
            flags = ["ok"]
        measured = row.get("measured_at")
        if hasattr(measured, "astimezone"):
            measured_str = measured.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            measured_str = str(measured)
        created = row.get("created_at", measured_str)
        if hasattr(created, "astimezone"):
            created_str = created.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            created_str = str(created)
        return ObservationRecord(
            id=str(row["id"]),
            profile_id=str(row["profile_id"]),
            namespace=str(row.get("namespace", "demo")),
            indicator=str(row["indicator"]),
            value=float(row["value"]) if row.get("value") is not None else None,
            source_value=float(row["source_value"]) if row.get("source_value") is not None else None,
            unit=str(row["unit"]),
            context=str(row["context"]),
            measured_at=measured_str,
            mission_day=int(row["mission_day"]) if row.get("mission_day") is not None else None,
            origin_type=str(row["origin_type"]),
            capture_method=str(row["capture_method"]),
            source_reference=row.get("source_reference") or row.get("source_file"),
            quality_flag=str(row.get("quality_flag") or (flags[0] if flags else "ok")),
            quality_flags=flags,
            source_file=row.get("source_file"),
            source_row=row.get("source_row"),
            import_batch_id=row.get("import_batch_id"),
            created_at=created_str,
        )

    @staticmethod
    def _dict_to_checkin(row: dict) -> CheckinRecord:
        return CheckinRecord(
            id=str(row["id"]),
            profile_id=str(row["profile_id"]),
            namespace=str(row.get("namespace", "demo")),
            checkin_date=str(row["checkin_date"]),
            fatigue=int(row["fatigue"]),
            perceived_stress=int(row["perceived_stress"]),
            notes=row.get("notes"),
            origin_type=str(row.get("origin_type", "user_report")),
            capture_method=str(row.get("capture_method", "manual")),
            quality_flag=str(row.get("quality_flag", "ok")),
            created_at=str(row.get("created_at", "")),
        )
