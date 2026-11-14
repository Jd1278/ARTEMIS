"""Seed data definitions and packaged demo loader for ARTEMIS HEALTH.

Respects all dataset provenance and isolation rules:
- crew_daily_log_clean.csv is always labeled SIMULADO (synthetic).
- bedrest_actigraphy_clean.csv and bedrest_winscat_clean.csv are labeled as ground analogs (not in-flight).
- inspiration4_blood_long.csv retains its 3-day short-flight cohort context.
- iss_radiation_daily_clean.csv is labeled as historical environmental ISS TEPC data (not personal dose).
- astronaut_health_observations.csv is flagged as excluded from primary use pending documentary reconciliation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from artemis_health.core.config import PROJECT_ROOT

DEFAULT_EDUCATIONAL_CARDS: Tuple[Dict[str, str], ...] = (
    {
        "id": "10000000-0000-4000-8000-000000000001",
        "indicator": "resting_hr_bpm",
        "title": "Frecuencia cardíaca en reposo",
        "description": (
            "Mide los latidos por minuto en condición de reposo matutino antes de iniciar las actividades "
            "operativas. Permite observar variaciones individuales frente a la mediana histórica personal "
            "durante las distintas fases de misión."
        ),
        "unit": "bpm",
        "limitations": (
            "Indicador descriptivo de bienestar general. No constituye un diagnóstico cardiológico ni "
            "sustituye un electrocardiograma clínico. La hidratación, el reacondicionamiento cardiovascular "
            "en microgravedad y el ciclo circadiano modifican el pulso sin implicar enfermedad."
        ),
        "bibliographic_reference": (
            "American Heart Association (AHA) — All About Heart Rate (Pulse); "
            "NASA Human Research Program (HRP) Standard Measures."
        ),
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "10000000-0000-4000-8000-000000000002",
        "indicator": "sleep_duration_h",
        "title": "Duración del sueño",
        "description": (
            "Registra el total de horas de sueño obtenidas en el ciclo diario de 24 horas. En misiones "
            "espaciales, el monitoreo longitudinal del descanso ayuda a identificar desajustes de horario "
            "y episodios de restricción de sueño."
        ),
        "unit": "h",
        "limitations": (
            "El autoinforme o actigrafía de muñeca no sustituye la polisomnografía clínica ni diagnostica "
            "trastornos del sueño. No evalúa la arquitectura detallada de fases REM/NREM."
        ),
        "bibliographic_reference": (
            "Barger LK et al. (2014). Prevalence of sleep deficiency and use of hypnotic drugs in astronauts "
            "before, during, and after spaceflight. The Lancet Neurology, 13(9):904-912. "
            "doi:10.1016/S1474-4422(14)70122-X."
        ),
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "10000000-0000-4000-8000-000000000003",
        "indicator": "fatigue",
        "title": "Fatiga percibida",
        "description": (
            "Registra la percepción subjetiva de cansancio al despertar o durante el seguimiento diario "
            "(escala 1-5 en check-in de bienestar y escala operativa Samn-Perelli 1-7 en bitácora de misión)."
        ),
        "unit": "scale_1_5",
        "limitations": (
            "Es un autoinforme subjetivo expuesto a sesgo de percepción personal. No mide tiempos de reacción "
            "objetivos (como la prueba PVT-B) ni determina aptitud médica o clínica."
        ),
        "bibliographic_reference": (
            "Samn SW, Perelli LP (1982). Estimating Aircrew Fatigue: A Technique with Application to Airlift "
            "Operations. USAF School of Aerospace Medicine, Technical Report SAM-TR-82-21."
        ),
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "10000000-0000-4000-8000-000000000004",
        "indicator": "perceived_stress",
        "title": "Estrés percibido",
        "description": (
            "Evalúa la tensión subjetiva percibida ante la carga de trabajo, el confinamiento y los cambios "
            "operativos de la misión (escala discreta 1-5 en check-in y escala visual analógica VAS 0-100 puntos)."
        ),
        "unit": "scale_1_5",
        "limitations": (
            "Representa una apreciación subjetiva expresada en puntos de escala, nunca un porcentaje clínico "
            "ni una evaluación psicológica o psiquiátrica."
        ),
        "bibliographic_reference": (
            "Jones CW et al. (2022). Sleep deficiency in spaceflight is associated with degraded "
            "neurobehavioral functions and elevated stress in astronauts on six-month missions aboard the ISS. "
            "SLEEP, 45(3). https://pmc.ncbi.nlm.nih.gov/articles/PMC8919197."
        ),
        "created_at": "2026-03-01T00:00:00Z",
    },
)

DEFAULT_RESEARCH_DATASETS: Tuple[Dict[str, Any], ...] = (
    {
        "id": "20000000-0000-4000-8000-000000000001",
        "dataset_key": "bedrest_actigraphy_clean",
        "file_name": "bedrest_actigraphy_clean.csv",
        "title": "NASA NLSP UTMB Bed Rest Campaign 1 — Actigrafía de sueño (Análogo Terrestre)",
        "namespace": "research",
        "origin_type": "public_dataset",
        "capture_method": "sensor",
        "study_context": (
            "ANÁLOGO TERRESTRE EN CAMA (head-down tilt 6°, 60 días, 3 sujetos C1G0001-C1G0003). "
            "NO son mediciones en vuelo espacial."
        ),
        "is_inflight_measurement": False,
        "is_personal_radiation_dose": False,
        "included_in_personal_calculations": False,
        "row_count": 207,
        "sha256": "09de1e728040c74b2e6633ea0dea6eefa2fdd065f9da8296550d3da4d41f92a6",
        "limitations": (
            "Estudio análogo terrestre con N=3 sujetos en reposo en cama con inclinación cefálica de -6°. "
            "Contiene 17 noches sin datos ('No Data' conservadas como missing). Prohibido afirmar que son "
            "mediciones obtenidas en vuelo espacial o usarlas en la línea base personal."
        ),
        "source_reference": "NASA Life Sciences Portal (NLSP) — Experiment BRSMAct (BRSMACT_Campagin_1_Actigraphy).",
        "quality_flag": "ok",
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "20000000-0000-4000-8000-000000000002",
        "dataset_key": "bedrest_winscat_clean",
        "file_name": "bedrest_winscat_clean.csv",
        "title": "NASA NLSP UTMB Bed Rest Campaign 1 — Batería neurocognitiva WinSCAT (Análogo Terrestre)",
        "namespace": "research",
        "origin_type": "public_dataset",
        "capture_method": "import",
        "study_context": (
            "ANÁLOGO TERRESTRE EN CAMA (experimento MR085G, 3 sujetos, antes/durante/después de bed rest). "
            "NO son mediciones en vuelo espacial."
        ),
        "is_inflight_measurement": False,
        "is_personal_radiation_dose": False,
        "included_in_personal_calculations": False,
        "row_count": 30,
        "sha256": "9a2498e33bed26b33087ed6f087289c14a0b1026422ffb10cdee7d61d9a297c3",
        "limitations": (
            "Datos de laboratorio análogo en Tierra, no en vuelo. Las sesiones 1 a 3 corresponden a sesiones "
            "de práctica con efecto de aprendizaje. No se mezcla con el espacio demo."
        ),
        "source_reference": "NASA Life Sciences Portal (NLSP) — Experiment MR085G (MR085G_Campaign_1_WinSCAT).",
        "quality_flag": "ok",
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "20000000-0000-4000-8000-000000000003",
        "dataset_key": "inspiration4_blood_long",
        "file_name": "inspiration4_blood_long.csv",
        "title": "NASA OSDR OSD-575 / OSD-569 — Paneles hematológicos y metabólicos Inspiration4 (REAL NASA OSDR)",
        "namespace": "research",
        "origin_type": "public_dataset",
        "capture_method": "import",
        "study_context": (
            "Misión orbital comercial de corta duración (3 días, 4 tripulantes civiles C001-C004, "
            "7 puntos temporales pre-vuelo L-92/L-44/L-3 y post-vuelo R+1/R+45/R+82/R+194)."
        ),
        "is_inflight_measurement": False,
        "is_personal_radiation_dose": False,
        "included_in_personal_calculations": False,
        "row_count": 1064,
        "sha256": "062a05aa790585ea3d09040b840791fa6e26c87b4f91be578633fbd0f0e59656",
        "limitations": (
            "Muestras tomadas antes y después de un vuelo de 3 días (sin extracciones en vuelo). "
            "Incluye 4 valores marcados con review_note por posibles artefactos pre-analíticos. "
            "No debe utilizarse para entrenar alertas diarias ni inferir respuesta en misiones largas."
        ),
        "source_reference": (
            "NASA Open Science Data Repository (OSDR) OSD-575 (CMP) & OSD-569 (CBC); "
            "Overbey EG et al. (2024), Nature Communications / npj Microgravity."
        ),
        "quality_flag": "pending_review",
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "20000000-0000-4000-8000-000000000004",
        "dataset_key": "iss_radiation_daily_clean",
        "file_name": "iss_radiation_daily_clean.csv",
        "title": "NASA CDAWeb ISS_DOSANL_TEPC — Radiación ambiental histórica en ISS (Ambiental, NO Dosis Personal)",
        "namespace": "research",
        "origin_type": "public_dataset",
        "capture_method": "sensor",
        "study_context": (
            "SERIE AMBIENTAL HISTÓRICA medida por el detector TEPC dentro de la ISS (2017-03-01 a 2017-08-27). "
            "NO representa dosis personal ni exposición individual de ningún astronauta."
        ),
        "is_inflight_measurement": True,
        "is_personal_radiation_dose": False,
        "included_in_personal_calculations": False,
        "row_count": 180,
        "sha256": "fe93743babc7f8ba5cadcf0d6d75f11a25f19d69a504c8351503ad0005d521df",
        "limitations": (
            "Medición ambiental de área del instrumento TEPC en 2017, con 20 días imputados y 35 días "
            "parciales escalados a 24 h. Prohibido interpretarla como dosimetría personal o dosis efectiva "
            "individual de la tripulación ficticia."
        ),
        "source_reference": "NASA CDAWeb ISS_DOSANL_TEPC (NASA Space Radiation Analysis Group, JSC).",
        "quality_flag": "imputed",
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "20000000-0000-4000-8000-000000000005",
        "dataset_key": "crew_daily_log_clean",
        "file_name": "crew_daily_log_clean.csv",
        "title": "Bitácora diaria de tripulación SIM-ISS-180 (SIMULADO — Fuente Principal Demo)",
        "namespace": "research",
        "origin_type": "synthetic",
        "capture_method": "import",
        "study_context": (
            "DATASET SIMULADO (6 perfiles ficticios CM-01 a CM-06 durante 180 días). "
            "Los 92 valores imputados o fuera de rango se excluyen del análisis (value=null, source_value conservado)."
        ),
        "is_inflight_measurement": False,
        "is_personal_radiation_dose": False,
        "included_in_personal_calculations": False,
        "row_count": 1080,
        "sha256": "1748a068c0af4c811b791bdf452b406b05a96da09dd3db2ac02dc11d6fb5d00d",
        "limitations": (
            "Datos 100% sintéticos generados mediante simulación calibrada. Las columnas derivadas, "
            "semáforos (status_*), overall_status y risk_score del CSV se excluyen del producto."
        ),
        "source_reference": "Generador sintético local ARTEMIS (scripts/prepare_demo.py -> data/demo/observations.json).",
        "quality_flag": "ok",
        "created_at": "2026-03-01T00:00:00Z",
    },
    {
        "id": "20000000-0000-4000-8000-000000000006",
        "dataset_key": "astronaut_health_observations_excluded",
        "file_name": "astronaut_health_observations.csv",
        "title": "Archivo integrado multipropósito (EXCLUIDO como fuente principal — Pendiente de reconciliación)",
        "namespace": "research",
        "origin_type": "synthetic",
        "capture_method": "import",
        "study_context": (
            "EXCLUIDO DE CÁLCULOS: mezcla datos sintéticos, paneles calibrados simulated_from_real, "
            "radiación ambiental repetida por tripulante y estudios análogos."
        ),
        "is_inflight_measurement": False,
        "is_personal_radiation_dose": False,
        "included_in_personal_calculations": False,
        "row_count": 20080,
        "sha256": "b56c8ecce2cbcfe1f425221e6c13be51ddaaf4596c98a8e9c1c7f2e2931f35b9",
        "limitations": (
            "No se utiliza como fuente principal por inconsistencia documental detectada en la auditoría "
            "(DATA_DICTIONARY.md declara 14.612 filas mientras el CSV real y CLEANING_REPORT.md contienen "
            "20.080 filas) y por mezclar distintas procedencias en una misma tabla."
        ),
        "source_reference": "Auditoría interna docs/dataset-audit.json y docs/review.md.",
        "quality_flag": "pending_review",
        "created_at": "2026-03-01T00:00:00Z",
    },
)


def load_packaged_demo_observations() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Load the verified 4,320 demo observations and manifest from data/demo/."""
    demo_dir = PROJECT_ROOT / "data" / "demo"
    obs_path = demo_dir / "observations.json"
    manifest_path = demo_dir / "manifest.json"
    if not obs_path.exists() or not manifest_path.exists():
        return [], {}
    observations = json.loads(obs_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return observations, manifest
