"""Schemas and strict validators for observations, personal baseline comparisons, dashboard, and trends."""
from __future__ import annotations

import math
import uuid
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

from artemis_health.core.constants import (
    ALLOWED_CAPTURE_METHODS,
    ALLOWED_NAMESPACES,
    ALLOWED_ORIGIN_TYPES,
    ALLOWED_QUALITY_FLAGS,
    EXCLUDED_FLAG_SUFFIXES,
    resolve_indicator_spec,
)
from artemis_health.core.exceptions import DomainValidationError, NamespaceIsolationError


def _parse_iso_datetime(raw: Any) -> datetime:
    if isinstance(raw, datetime):
        dt = raw
    elif isinstance(raw, date):
        dt = datetime(raw.year, raw.month, raw.day, 7, 0, 0, tzinfo=timezone.utc)
    elif isinstance(raw, str):
        text = raw.strip()
        if not text:
            raise DomainValidationError("La fecha/hora 'measured_at' no puede estar vacía.", fields={"measured_at": ["Requerido"]})
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            if "T" not in text and " " not in text and len(text) == 10:
                d = date.fromisoformat(text)
                dt = datetime(d.year, d.month, d.day, 7, 0, 0, tzinfo=timezone.utc)
            else:
                dt = datetime.fromisoformat(text)
        except ValueError as exc:
            raise DomainValidationError(
                f"Fecha u hora inválida: '{raw}'. Use formato ISO 8601 (ej. 2026-03-15T07:00:00Z).",
                fields={"measured_at": ["Formato ISO 8601 inválido"]},
            ) from exc
    else:
        raise DomainValidationError(
            "Tipo de fecha inválido para 'measured_at'.",
            fields={"measured_at": ["Se esperaba cadena ISO 8601"]},
        )
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt


class ObservationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique UUID for idempotency.")
    profile_id: str = Field(default="demo", description="Fictional profile ID (e.g. 'demo' or 'CM-01').")
    indicator: str = Field(..., description="Indicator key (e.g. resting_hr_bpm, sleep_duration_h, fatigue, perceived_stress).")
    value: Optional[float] = Field(..., description="Numeric observation value.")
    unit: str = Field(..., description="Measurement unit compatible with the indicator.")
    measured_at: str = Field(..., description="ISO 8601 UTC timestamp of measurement.")
    context: Optional[str] = Field(default=None, description="Measurement context (e.g. rest, sleep_report).")
    origin_type: str = Field(default="user_report", description="Origin type: synthetic, user_report, or public_dataset.")
    capture_method: str = Field(default="manual", description="Capture method: manual, sensor, or import.")
    source_reference: Optional[str] = Field(default=None, description="Optional source or instrument reference.")
    quality_flag: str = Field(default="ok", description="Primary quality flag.")
    quality_flags: Optional[List[str]] = Field(default=None, description="Detailed quality flags list.")
    namespace: str = Field(default="demo", description="Data space ('demo' or 'research').")
    mission_day: Optional[int] = Field(default=None, description="Optional mission day (>= 1).")

    @model_validator(mode="before")
    @classmethod
    def normalize_and_validate_raw(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise DomainValidationError("El cuerpo de la solicitud debe ser un objeto JSON válido.")
        payload = dict(data)

        # Support 'uuid' or 'observation_id' as alias for 'id'
        if "id" not in payload:
            if "uuid" in payload:
                payload["id"] = payload.pop("uuid")
            elif "observation_id" in payload:
                payload["id"] = payload.pop("observation_id")
        else:
            payload.pop("uuid", None)
            payload.pop("observation_id", None)

        # Support 'timestamp' or 'date' as alias for 'measured_at'
        if "measured_at" not in payload:
            if "timestamp" in payload:
                payload["measured_at"] = payload.pop("timestamp")
            elif "date" in payload:
                payload["measured_at"] = payload.pop("date")
        else:
            payload.pop("timestamp", None)
            payload.pop("date", None)

        # Validate UUID
        raw_id = payload.get("id")
        if raw_id is not None:
            try:
                parsed_uuid = uuid.UUID(str(raw_id))
                payload["id"] = str(parsed_uuid)
            except (ValueError, TypeError) as exc:
                raise DomainValidationError(
                    f"El identificador '{raw_id}' no es un UUID válido.",
                    fields={"id": ["Debe ser un UUID válido"]},
                ) from exc

        # Validate profile_id
        profile_id = str(payload.get("profile_id", "demo")).strip()
        if not profile_id:
            raise DomainValidationError("El campo 'profile_id' no puede estar vacío.", fields={"profile_id": ["Requerido"]})
        payload["profile_id"] = profile_id

        # Validate indicator
        raw_indicator = payload.get("indicator")
        if not isinstance(raw_indicator, str) or not raw_indicator.strip():
            raise DomainValidationError(
                "El campo 'indicator' es obligatorio.",
                fields={"indicator": ["Indicador requerido"]},
            )
        spec = resolve_indicator_spec(raw_indicator)
        if spec is None:
            raise DomainValidationError(
                f"Indicador no permitido: '{raw_indicator}'. Indicadores válidos: resting_hr_bpm, sleep_duration_h, fatigue, samn_perelli, perceived_stress, stress_vas.",
                fields={"indicator": [f"Indicador '{raw_indicator}' no reconocido"]},
            )
        payload["indicator"] = spec.key

        # Validate unit compatibility
        raw_unit = payload.get("unit")
        if not isinstance(raw_unit, str) or not raw_unit.strip():
            raise DomainValidationError(
                "El campo 'unit' es obligatorio.",
                fields={"unit": ["Unidad requerida"]},
            )
        cleaned_unit = raw_unit.strip().lower()
        allowed_lower = {u.lower(): u for u in spec.allowed_units}
        if cleaned_unit not in allowed_lower:
            raise DomainValidationError(
                f"Unidad '{raw_unit}' incompatible con el indicador '{spec.key}'. Unidades permitidas: {', '.join(spec.allowed_units)}.",
                fields={"unit": [f"Unidad incompatible para {spec.key}; se esperaba {spec.canonical_unit}"]},
            )
        payload["unit"] = spec.canonical_unit

        # Validate context
        raw_context = payload.get("context")
        if raw_context is None or (isinstance(raw_context, str) and not raw_context.strip()):
            payload["context"] = spec.default_context
        else:
            cleaned_ctx = str(raw_context).strip().lower()
            if cleaned_ctx not in spec.allowed_contexts:
                raise DomainValidationError(
                    f"Contexto '{raw_context}' inválido para '{spec.key}'. Contextos permitidos: {', '.join(spec.allowed_contexts)}.",
                    fields={"context": [f"Contexto no válido para {spec.key}"]},
                )
            payload["context"] = cleaned_ctx

        # Validate namespace & origin_type isolation
        namespace = str(payload.get("namespace", "demo")).strip().lower()
        if namespace not in ALLOWED_NAMESPACES:
            raise DomainValidationError(
                f"Espacio '{namespace}' inválido. Valores permitidos: demo, research.",
                fields={"namespace": ["Espacio inválido"]},
            )
        origin_type = str(payload.get("origin_type", "user_report")).strip().lower()
        if origin_type not in ALLOWED_ORIGIN_TYPES:
            raise DomainValidationError(
                f"Tipo de origen '{origin_type}' inválido. Valores permitidos: synthetic, user_report, public_dataset.",
                fields={"origin_type": ["Origen inválido"]},
            )
        if origin_type == "public_dataset" or namespace == "research":
            raise NamespaceIsolationError(
                "No se permite registrar ni mezclar datasets públicos o del espacio 'research' en las observaciones personales del espacio 'demo'.",
                fields={"origin_type": ["Aislamiento demo/research activo"]},
            )
        payload["namespace"] = "demo"
        payload["origin_type"] = origin_type

        # Validate capture_method
        capture_method = str(payload.get("capture_method", "manual")).strip().lower()
        if capture_method not in ALLOWED_CAPTURE_METHODS:
            raise DomainValidationError(
                f"Método de captura '{capture_method}' inválido. Valores permitidos: manual, sensor, import.",
                fields={"capture_method": ["Método de captura inválido"]},
            )
        payload["capture_method"] = capture_method

        # Validate quality_flag and quality_flags
        q_flag = str(payload.get("quality_flag", "ok")).strip().lower()
        q_flags_raw = payload.get("quality_flags")
        if q_flags_raw is not None:
            if not isinstance(q_flags_raw, list) or not all(isinstance(x, str) for x in q_flags_raw):
                raise DomainValidationError("El campo 'quality_flags' debe ser una lista de cadenas.", fields={"quality_flags": ["Formato inválido"]})
            q_flags = [x.strip().lower() for x in q_flags_raw if x.strip()] or [q_flag]
        else:
            q_flags = [q_flag]

        for f in [q_flag, *q_flags]:
            if f not in ALLOWED_QUALITY_FLAGS and not f.endswith(("_imputed", "_out_of_range")):
                raise DomainValidationError(
                    f"Flag de calidad '{f}' no permitido.",
                    fields={"quality_flag": [f"Flag '{f}' desconocido"]},
                )
        payload["quality_flag"] = q_flag
        payload["quality_flags"] = q_flags

        # Validate numeric value
        raw_val = payload.get("value")
        is_excluded_flag = any(f.endswith(EXCLUDED_FLAG_SUFFIXES) for f in q_flags) or q_flag in (
            "imputed",
            "missing",
            "incompatible",
            "out_of_range",
        )
        if raw_val is None:
            if origin_type == "user_report" and not is_excluded_flag:
                raise DomainValidationError(
                    "El valor numérico ('value') es obligatorio para observaciones manuales.",
                    fields={"value": ["Valor requerido"]},
                )
            payload["value"] = None
        else:
            if isinstance(raw_val, bool):
                raise DomainValidationError(
                    "El campo 'value' debe ser un número finito, no booleano.",
                    fields={"value": ["Tipo booleano no permitido"]},
                )
            try:
                num_val = float(raw_val)
            except (ValueError, TypeError) as exc:
                raise DomainValidationError(
                    f"El valor '{raw_val}' no es numérico.",
                    fields={"value": ["Debe ser un número válido"]},
                ) from exc
            if not math.isfinite(num_val):
                raise DomainValidationError(
                    "El valor numérico debe ser finito (no se admite NaN ni Infinity).",
                    fields={"value": ["Valor no finito"]},
                )
            if spec.integer_only and num_val != math.trunc(num_val):
                raise DomainValidationError(
                    f"El indicador '{spec.key}' requiere un valor entero entre {int(spec.minimum)} y {int(spec.maximum)}.",
                    fields={"value": ["Se requiere un número entero"]},
                )
            if num_val < spec.minimum or num_val > spec.maximum:
                raise DomainValidationError(
                    f"Valor {num_val} fuera del dominio técnico permitido para '{spec.key}' [{spec.minimum}, {spec.maximum}] {spec.canonical_unit}.",
                    fields={"value": [f"Debe estar entre {spec.minimum} y {spec.maximum} {spec.canonical_unit}"]},
                )
            if any(f.endswith(("_imputed", "_out_of_range")) or f in ("imputed", "out_of_range") for f in q_flags):
                raise DomainValidationError(
                    "Los registros marcados como imputados o fuera de rango deben tener value=null.",
                    fields={"value": ["Flag excluido requiere value=null"]},
                )
            payload["value"] = num_val

        # Validate measured_at
        if "measured_at" not in payload or payload["measured_at"] is None:
            raise DomainValidationError(
                "El campo 'measured_at' es obligatorio.",
                fields={"measured_at": ["Fecha/hora requerida"]},
            )
        dt = _parse_iso_datetime(payload["measured_at"])
        payload["measured_at"] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        if payload.get("mission_day") is None:
            launch_date = date(2026, 3, 1)
            delta_days = (dt.date() - launch_date).days + 1
            payload["mission_day"] = max(1, delta_days)
        else:
            try:
                md = int(payload["mission_day"])
                if md < 1:
                    raise ValueError
                payload["mission_day"] = md
            except (ValueError, TypeError) as exc:
                raise DomainValidationError(
                    "El campo 'mission_day' debe ser un entero positivo.",
                    fields={"mission_day": ["Debe ser >= 1"]},
                ) from exc

        return payload


class BaselineComparisonOut(BaseModel):
    indicator: str
    unit: str
    context: str
    origin_type: str
    rule_version: str = "baseline_v1"
    reference_timestamp: str
    current_value: Optional[float] = None
    baseline_median: Optional[float] = None
    difference: Optional[float] = None
    sufficient_history: bool
    status: str = Field(..., description="'comparison_available' or 'insufficient_history' or 'no_current_value'")
    days_used: int
    minimum_days_required: int = 7
    window_days: int = 30
    max_days: int = 14
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    descriptive_notice: str = Field(..., description="Neutral, non-clinical description of comparison against personal median.")
    reference_observation_ids: List[str] = Field(default_factory=list)


class ObservationOut(BaseModel):
    id: str
    profile_id: str
    namespace: str = "demo"
    indicator: str
    value: Optional[float] = None
    source_value: Optional[float] = None
    unit: str
    context: str
    measured_at: str
    timestamp: str
    mission_day: Optional[int] = None
    origin_type: str
    capture_method: str
    source_reference: Optional[str] = None
    quality_flag: str
    quality_flags: List[str]
    is_Simulated: bool = Field(default=False, alias="is_simulated")
    created_at: str

    model_config = ConfigDict(populate_by_name=True)


class ObservationCreateResponse(BaseModel):
    status: str = Field(..., description="'created' (201) or 'idempotent_replay' (200).")
    save_status: str = Field(default="GUARDADO")
    idempotent: bool = Field(default=False)
    observation: ObservationOut
    comparison: BaselineComparisonOut


class ObservationListResponse(BaseModel):
    profile_id: str
    namespace: str = "demo"
    data_label: str = "SIMULADO"
    indicator_filter: Optional[str] = None
    from_filter: Optional[str] = None
    to_filter: Optional[str] = None
    count: int
    observations: List[ObservationOut]


class TrendPointOut(BaseModel):
    id: Optional[str] = None
    date: str
    measured_at: Optional[str] = None
    mission_day: Optional[int] = None
    value: Optional[float] = Field(None, description="Numeric value or null for missing/imputed gaps (never interpolated).")
    source_value: Optional[float] = None
    unit: str
    origin_type: str
    capture_method: str
    quality_flag: str
    quality_flags: List[str]
    is_gap: bool = Field(default=False, description="True when value is null (missing or excluded imputed value).")


class IndicatorTrendSeriesOut(BaseModel):
    indicator: str
    label: str
    unit: str
    context: str
    points_count: int
    valid_points_count: int
    null_gaps_count: int
    interpolation_applied: bool = False
    baseline_median: Optional[float] = None
    sufficient_history: bool = False
    series: List[TrendPointOut]


class TrendsResponse(BaseModel):
    profile_id: str
    alias: str
    namespace: str = "demo"
    data_label: str = "SIMULADO"
    interpolation_applied: bool = False
    disclaimer: str
    series_by_indicator: Dict[str, IndicatorTrendSeriesOut]
    trends: List[IndicatorTrendSeriesOut]


class IndicatorSummaryCardOut(BaseModel):
    slot: str
    indicator: str
    label: str
    unit: str
    context: str
    latest_observation: Optional[ObservationOut] = None
    comparison: BaselineComparisonOut


class DashboardResponse(BaseModel):
    profile: Dict[str, Any]
    namespace: str = "demo"
    data_label: str = "SIMULADO"
    is_simulated: bool = True
    cursor_timestamp: Optional[str] = None
    latest_recorded_at: Optional[str] = None
    disclaimer: str
    indicators_summary: List[IndicatorSummaryCardOut]
    cards: Dict[str, IndicatorSummaryCardOut]
