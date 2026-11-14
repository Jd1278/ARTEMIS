"""Domain constants, canonical indicator definitions, scales, and baseline parameters."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet, Optional, Tuple


ALLOWED_NAMESPACES: FrozenSet[str] = frozenset({"demo", "research"})
ALLOWED_ORIGIN_TYPES: FrozenSet[str] = frozenset({"synthetic", "user_report", "public_dataset"})
ALLOWED_CAPTURE_METHODS: FrozenSet[str] = frozenset({"manual", "sensor", "import"})
ALLOWED_QUALITY_FLAGS: FrozenSet[str] = frozenset(
    {
        "ok",
        "missing",
        "imputed",
        "stale",
        "incompatible",
        "pending_review",
        "out_of_range",
        "resting_hr_bpm_imputed",
        "resting_hr_bpm_out_of_range",
        "sleep_duration_h_imputed",
        "sleep_duration_h_out_of_range",
        "samn_perelli_imputed",
        "samn_perelli_out_of_range",
        "stress_vas_imputed",
        "stress_vas_out_of_range",
    }
)

EXCLUDED_FLAG_SUFFIXES: Tuple[str, ...] = (
    "_imputed",
    "_out_of_range",
    "imputed",
    "missing",
    "incompatible",
    "out_of_range",
)

NON_CLINICAL_DISCLAIMER = (
    "ARTEMIS HEALTH es una plataforma informativa y educativa de seguimiento de bienestar para perfiles "
    "ficticios. No es un dispositivo médico: no diagnostica, no predice enfermedades, no prescribe "
    "tratamientos ni emite recomendaciones clínicas."
)

BASELINE_RULE_VERSION = "baseline_v1"
BASELINE_WINDOW_DAYS = 30
BASELINE_MAX_OBSERVATIONS = 14
BASELINE_MIN_DAYS = 7


@dataclass(frozen=True)
class IndicatorSpec:
    key: str
    display_key: str
    label: str
    description: str
    canonical_unit: str
    allowed_units: Tuple[str, ...]
    default_context: str
    allowed_contexts: Tuple[str, ...]
    minimum: float
    maximum: float
    integer_only: bool
    dashboard_slot: str


INDICATOR_CATALOG: Dict[str, IndicatorSpec] = {
    "resting_hr_bpm": IndicatorSpec(
        key="resting_hr_bpm",
        display_key="resting_hr_bpm",
        label="Frecuencia cardíaca en reposo",
        description="Frecuencia cardíaca matutina medida en condición de reposo (latidos por minuto).",
        canonical_unit="bpm",
        allowed_units=("bpm", "lpm", "beats/min"),
        default_context="rest",
        allowed_contexts=("rest", "morning_rest", "daily", "baseline"),
        minimum=20.0,
        maximum=250.0,
        integer_only=False,
        dashboard_slot="resting_hr_bpm",
    ),
    "sleep_duration_h": IndicatorSpec(
        key="sleep_duration_h",
        display_key="sleep_duration_h",
        label="Duración del sueño",
        description="Duración total del episodio principal de sueño en el ciclo diario de misión (horas).",
        canonical_unit="h",
        allowed_units=("h", "hours", "horas", "hr", "hrs"),
        default_context="sleep_report",
        allowed_contexts=("sleep_report", "rest", "daily", "actigraphy"),
        minimum=0.0,
        maximum=24.0,
        integer_only=False,
        dashboard_slot="sleep_duration_h",
    ),
    "fatigue": IndicatorSpec(
        key="fatigue",
        display_key="fatigue",
        label="Fatiga percibida (escala 1-5)",
        description="Nivel de fatiga percibida autoinformada en escala discreta de 1 (alerta) a 5 (fatiga elevada).",
        canonical_unit="scale_1_5",
        allowed_units=("scale_1_5", "1-5", "points_1_5", "points", "escala_1_5", "score"),
        default_context="fatigue_report",
        allowed_contexts=("fatigue_report", "daily", "checkin", "morning_report"),
        minimum=1.0,
        maximum=5.0,
        integer_only=False,
        dashboard_slot="fatigue",
    ),
    "samn_perelli": IndicatorSpec(
        key="samn_perelli",
        display_key="samn_perelli",
        label="Fatiga percibida (Samn-Perelli 1-7)",
        description="Escala operativa subjetiva de fatiga Samn-Perelli de 1 (totalmente alerta) a 7 (agotado).",
        canonical_unit="points_1_7",
        allowed_units=("points_1_7", "1-7", "scale_1_7", "points"),
        default_context="fatigue_report",
        allowed_contexts=("fatigue_report", "daily", "checkin", "morning_report"),
        minimum=1.0,
        maximum=7.0,
        integer_only=True,
        dashboard_slot="fatigue",
    ),
    "perceived_stress": IndicatorSpec(
        key="perceived_stress",
        display_key="perceived_stress",
        label="Estrés percibido (escala 1-5)",
        description="Nivel de estrés percibido autoinformado en escala discreta de 1 (bajo) a 5 (alto).",
        canonical_unit="scale_1_5",
        allowed_units=("scale_1_5", "1-5", "points_1_5", "points", "escala_1_5", "score"),
        default_context="stress_report",
        allowed_contexts=("stress_report", "daily", "checkin", "morning_report"),
        minimum=1.0,
        maximum=5.0,
        integer_only=False,
        dashboard_slot="perceived_stress",
    ),
    "stress_vas": IndicatorSpec(
        key="stress_vas",
        display_key="stress_vas",
        label="Estrés percibido (VAS 0-100)",
        description="Escala visual analógica (0 a 100 puntos) de tensión o estrés percibido autoinformado.",
        canonical_unit="points_0_100",
        allowed_units=("points_0_100", "0-100", "vas", "points"),
        default_context="stress_report",
        allowed_contexts=("stress_report", "daily", "checkin", "morning_report"),
        minimum=0.0,
        maximum=100.0,
        integer_only=False,
        dashboard_slot="perceived_stress",
    ),
}

INDICATOR_ALIASES: Dict[str, str] = {
    "resting_hr_bpm": "resting_hr_bpm",
    "resting_heart_rate": "resting_hr_bpm",
    "heart_rate": "resting_hr_bpm",
    "hr": "resting_hr_bpm",
    "frecuencia_cardiaca": "resting_hr_bpm",
    "sleep_duration_h": "sleep_duration_h",
    "sleep_duration": "sleep_duration_h",
    "sleep": "sleep_duration_h",
    "duracion_sueno": "sleep_duration_h",
    "fatigue": "fatigue",
    "fatiga": "fatigue",
    "samn_perelli": "samn_perelli",
    "perceived_stress": "perceived_stress",
    "stress": "perceived_stress",
    "estres": "perceived_stress",
    "estres_percibido": "perceived_stress",
    "stress_vas": "stress_vas",
}

# Equivalences when querying history/trends across the demo synthetic log and user check-ins
COMPATIBLE_QUERY_GROUPS: Dict[str, Tuple[str, ...]] = {
    "resting_hr_bpm": ("resting_hr_bpm",),
    "sleep_duration_h": ("sleep_duration_h",),
    "fatigue": ("fatigue", "samn_perelli"),
    "samn_perelli": ("samn_perelli", "fatigue"),
    "perceived_stress": ("perceived_stress", "stress_vas"),
    "stress_vas": ("stress_vas", "perceived_stress"),
}

DEFAULT_DEMO_PROFILES: Tuple[Dict[str, str], ...] = (
    {
        "id": "demo",
        "profile_uuid": "00000000-0000-5000-8000-000000000000",
        "display_name": "Cmdr. Alex Vega (DEMO)",
        "alias": "Cmdr. Alex Vega (DEMO SIMULADO)",
        "profile_type": "fictional_astronaut",
        "role": "Commander",
        "mission": "SIM-ISS-180",
        "namespace": "demo",
    },
    {
        "id": "CM-01",
        "profile_uuid": "00000000-0000-5000-8000-000000000001",
        "display_name": "CM-01 Commander",
        "alias": "Cmdr. Alex Vega (CM-01)",
        "profile_type": "fictional_astronaut",
        "role": "Commander",
        "mission": "SIM-ISS-180",
        "namespace": "demo",
    },
    {
        "id": "CM-02",
        "profile_uuid": "00000000-0000-5000-8000-000000000002",
        "display_name": "CM-02 Flight Engineer 1",
        "alias": "Ing. Elena Rostova (CM-02)",
        "profile_type": "fictional_astronaut",
        "role": "Flight Engineer 1",
        "mission": "SIM-ISS-180",
        "namespace": "demo",
    },
    {
        "id": "CM-03",
        "profile_uuid": "00000000-0000-5000-8000-000000000003",
        "display_name": "CM-03 Flight Engineer 2",
        "alias": "Ing. Mateo Silva (CM-03)",
        "profile_type": "fictional_astronaut",
        "role": "Flight Engineer 2",
        "mission": "SIM-ISS-180",
        "namespace": "demo",
    },
    {
        "id": "CM-04",
        "profile_uuid": "00000000-0000-5000-8000-000000000004",
        "display_name": "CM-04 Flight Engineer 3",
        "alias": "Ing. Sora Takahashi (CM-04)",
        "profile_type": "fictional_astronaut",
        "role": "Flight Engineer 3",
        "mission": "SIM-ISS-180",
        "namespace": "demo",
    },
    {
        "id": "CM-05",
        "profile_uuid": "00000000-0000-5000-8000-000000000005",
        "display_name": "CM-05 Science Officer",
        "alias": "Of. Científico Liam O'Connor (CM-05)",
        "profile_type": "fictional_astronaut",
        "role": "Science Officer",
        "mission": "SIM-ISS-180",
        "namespace": "demo",
    },
    {
        "id": "CM-06",
        "profile_uuid": "00000000-0000-5000-8000-000000000006",
        "display_name": "CM-06 Medical Officer",
        "alias": "Of. Médico Amara Okafor (CM-06)",
        "profile_type": "fictional_astronaut",
        "role": "Medical Officer",
        "mission": "SIM-ISS-180",
        "namespace": "demo",
    },
)


def resolve_indicator_spec(raw_indicator: str) -> Optional[IndicatorSpec]:
    """Resolve an indicator name or alias to its canonical IndicatorSpec."""
    if not raw_indicator:
        return None
    cleaned = raw_indicator.strip().lower()
    canonical = INDICATOR_ALIASES.get(cleaned)
    if not canonical:
        return None
    return INDICATOR_CATALOG.get(canonical)
