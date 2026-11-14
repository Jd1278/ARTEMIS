"""Personal baseline calculation service (rule version: baseline_v1).

Implements causal, non-clinical personal baseline comparisons:
- Uses median of up to 14 compatible daily observations within the prior 30 days.
- Requires at least 7 distinct valid days.
- Strictly excludes current day, current observation, future observations, and imputed/invalid records.
- Strictly matches profile, indicator, canonical unit, context, and origin_type (never mixes synthetic, user_report, or public_dataset).
"""
from __future__ import annotations

import statistics
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional, Set

from artemis_health.core.constants import (
    BASELINE_MAX_OBSERVATIONS,
    BASELINE_MIN_DAYS,
    BASELINE_RULE_VERSION,
    BASELINE_WINDOW_DAYS,
    EXCLUDED_FLAG_SUFFIXES,
)
from artemis_health.models.entities import BaselineComparison, ObservationRecord


def parse_utc_timestamp(ts: str) -> datetime:
    text = ts.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def is_observation_valid_for_baseline(obs: ObservationRecord) -> bool:
    """Return True only if the observation has a finite non-null value and no exclusion flags."""
    if obs.value is None:
        return False
    if obs.namespace != "demo" or obs.origin_type == "public_dataset":
        return False
    if obs.quality_flag in ("imputed", "missing", "incompatible", "out_of_range", "pending_review"):
        return False
    for flag in obs.quality_flags or []:
        cleaned = flag.strip().lower()
        if cleaned.endswith(EXCLUDED_FLAG_SUFFIXES) or cleaned == "pending_review":
            return False
    return True


def _compatible_profile_ids(profile_id: str) -> Set[str]:
    if profile_id in ("demo", "CM-01"):
        return {"demo", "CM-01"}
    return {profile_id}


def compute_personal_baseline(
    *,
    candidates: Iterable[ObservationRecord],
    profile_id: str,
    indicator: str,
    unit: str,
    context: str,
    origin_type: str,
    reference_timestamp: str,
    current_value: Optional[float] = None,
    current_observation_id: Optional[str] = None,
) -> BaselineComparison:
    """Calculate the personal baseline median and descriptive comparison."""
    ref_dt = parse_utc_timestamp(reference_timestamp)
    ref_day = ref_dt.date()
    window_start_day = ref_day - timedelta(days=BASELINE_WINDOW_DAYS)
    window_end_day = ref_day - timedelta(days=1)
    allowed_profiles = _compatible_profile_ids(profile_id)

    # Group compatible observations by calendar day, keeping the latest valid observation per day
    by_day: Dict[str, tuple[datetime, ObservationRecord]] = {}

    for obs in candidates:
        if current_observation_id and obs.id == current_observation_id:
            continue
        if obs.profile_id not in allowed_profiles:
            continue
        if obs.indicator != indicator or obs.unit != unit or obs.context != context:
            continue
        if obs.origin_type != origin_type:
            continue
        if not is_observation_valid_for_baseline(obs):
            continue

        obs_dt = parse_utc_timestamp(obs.measured_at)
        obs_day = obs_dt.date()

        # Strictly exclude future observations and the current calendar day
        if obs_dt >= ref_dt or obs_day >= ref_day:
            continue
        # Strictly enforce 30-day lookback window
        if obs_day < window_start_day or obs_day > window_end_day:
            continue

        day_key = obs_day.isoformat()
        prior = by_day.get(day_key)
        if prior is None or (obs_dt, obs.id) > (prior[0], prior[1].id):
            by_day[day_key] = (obs_dt, obs)

    # Take up to 14 most recent distinct valid days within the 30-day window
    most_recent_days = sorted(by_day.keys(), reverse=True)[:BASELINE_MAX_OBSERVATIONS]
    selected_chronological: List[ObservationRecord] = [
        by_day[d][1] for d in sorted(most_recent_days)
    ]
    days_used = len(selected_chronological)
    ref_ids = [obs.id for obs in selected_chronological]
    period_start = selected_chronological[0].measured_at[:10] if selected_chronological else None
    period_end = selected_chronological[-1].measured_at[:10] if selected_chronological else None

    if days_used < BASELINE_MIN_DAYS:
        notice = (
            f"Historial insuficiente para línea base personal ({days_used} de {BASELINE_MIN_DAYS} días "
            f"distintos compatibles requeridos en los {BASELINE_WINDOW_DAYS} días previos para origen '{origin_type}'). "
            f"No se genera aviso de variación."
        )
        return BaselineComparison(
            indicator=indicator,
            unit=unit,
            context=context,
            origin_type=origin_type,
            rule_version=BASELINE_RULE_VERSION,
            reference_timestamp=ref_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            current_value=current_value,
            baseline_median=None,
            difference=None,
            sufficient_history=False,
            status="insufficient_history",
            days_used=days_used,
            minimum_days_required=BASELINE_MIN_DAYS,
            window_days=BASELINE_WINDOW_DAYS,
            max_days=BASELINE_MAX_OBSERVATIONS,
            period_start=period_start,
            period_end=period_end,
            descriptive_notice=notice,
            reference_observation_ids=ref_ids,
        )

    values = [float(obs.value) for obs in selected_chronological if obs.value is not None]
    median_val = round(float(statistics.median(values)), 2)

    if current_value is None:
        notice = (
            f"Regla {BASELINE_RULE_VERSION}: registro actual sin valor numérico válido (excluido por calidad/imputación). "
            f"Mediana personal de referencia: {median_val} {unit} calculada sobre {days_used} días válidos "
            f"({period_start} a {period_end}). Información descriptiva no clínica."
        )
        return BaselineComparison(
            indicator=indicator,
            unit=unit,
            context=context,
            origin_type=origin_type,
            rule_version=BASELINE_RULE_VERSION,
            reference_timestamp=ref_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            current_value=None,
            baseline_median=median_val,
            difference=None,
            sufficient_history=True,
            status="no_current_value",
            days_used=days_used,
            minimum_days_required=BASELINE_MIN_DAYS,
            window_days=BASELINE_WINDOW_DAYS,
            max_days=BASELINE_MAX_OBSERVATIONS,
            period_start=period_start,
            period_end=period_end,
            descriptive_notice=notice,
            reference_observation_ids=ref_ids,
        )

    diff = round(float(current_value) - median_val, 2)
    sign = "+" if diff > 0 else ""
    notice = (
        f"Regla {BASELINE_RULE_VERSION}: valor actual {current_value} {unit} frente a mediana personal de "
        f"{median_val} {unit} (variación descriptiva de {sign}{diff} {unit}), calculada con {days_used} días "
        f"compatibles entre {period_start} y {period_end}. Aviso descriptivo no clínico."
    )
    return BaselineComparison(
        indicator=indicator,
        unit=unit,
        context=context,
        origin_type=origin_type,
        rule_version=BASELINE_RULE_VERSION,
        reference_timestamp=ref_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        current_value=current_value,
        baseline_median=median_val,
        difference=diff,
        sufficient_history=True,
        status="comparison_available",
        days_used=days_used,
        minimum_days_required=BASELINE_MIN_DAYS,
        window_days=BASELINE_WINDOW_DAYS,
        max_days=BASELINE_MAX_OBSERVATIONS,
        period_start=period_start,
        period_end=period_end,
        descriptive_notice=notice,
        reference_observation_ids=ref_ids,
    )
