# Documentación de Endpoints REST — ARTEMIS HEALTH

> **Aviso de alcance no clínico:** ARTEMIS HEALTH es una plataforma informativa y educativa de seguimiento de bienestar para perfiles ficticios de astronauta. No es un dispositivo médico: no diagnostica, no predice enfermedades, no prescribe tratamientos ni genera recomendaciones clínicas.

Todos los endpoints están disponibles tanto en la raíz (`/health`, `/indicators`, `/profiles/demo/dashboard`, etc.) como bajo el prefijo `/api` (`/api/health`, `/api/indicators`, `/api/profiles/demo/dashboard`, etc.) para máxima compatibilidad con el frontend React/Vite/Recharts.

---

## 1. `GET /health` (y `GET /api/health`)
Verifica el estado del servicio API y la conectividad activa con la base de datos (Supabase PostgreSQL o motor persistente local).

### Ejemplo de respuesta (`200 OK`)
```json
{
  "status": "ok",
  "service": "ARTEMIS HEALTH API",
  "version": "1.0.0",
  "mode": "demo",
  "storage_backend": "postgres",
  "database_connected": true,
  "database_checked": true,
  "supabase_configured": true,
  "disclaimer": "ARTEMIS HEALTH es una plataforma informativa y educativa de seguimiento de bienestar para perfiles ficticios. No es un dispositivo médico: no diagnostica, no predice enfermedades, no prescribe tratamientos ni emite recomendaciones clínicas."
}
```

---

## 2. `GET /indicators` (y `GET /api/indicators`)
Devuelve el catálogo de indicadores permitidos, sus unidades canónicas, alias de unidades aceptadas y dominios técnicos de validación.

### Ejemplo de respuesta (`200 OK`)
```json
{
  "count": 6,
  "disclaimer": "ARTEMIS HEALTH es una plataforma informativa y educativa...",
  "indicators": [
    {
      "key": "resting_hr_bpm",
      "label": "Frecuencia cardíaca en reposo",
      "description": "Frecuencia cardíaca matutina medida en condición de reposo (latidos por minuto).",
      "unit": "bpm",
      "allowed_units": ["bpm", "lpm", "beats/min"],
      "context": "rest",
      "minimum": 20.0,
      "maximum": 250.0,
      "integer_only": false
    },
    {
      "key": "sleep_duration_h",
      "label": "Duración del sueño",
      "description": "Duración total del episodio principal de sueño en el ciclo diario de misión (horas).",
      "unit": "h",
      "allowed_units": ["h", "hours", "horas", "hr", "hrs"],
      "context": "sleep_report",
      "minimum": 0.0,
      "maximum": 24.0,
      "integer_only": false
    },
    {
      "key": "fatigue",
      "label": "Fatiga percibida (escala 1-5)",
      "description": "Nivel de fatiga percibida autoinformada en escala discreta de 1 (alerta) a 5 (fatiga elevada).",
      "unit": "scale_1_5",
      "allowed_units": ["scale_1_5", "1-5", "points_1_5", "points", "escala_1_5", "score"],
      "context": "fatigue_report",
      "minimum": 1.0,
      "maximum": 5.0,
      "integer_only": false
    },
    {
      "key": "perceived_stress",
      "label": "Estrés percibido (escala 1-5)",
      "description": "Nivel de estrés percibido autoinformado en escala discreta de 1 (bajo) a 5 (alto).",
      "unit": "scale_1_5",
      "allowed_units": ["scale_1_5", "1-5", "points_1_5", "points", "escala_1_5", "score"],
      "context": "stress_report",
      "minimum": 1.0,
      "maximum": 5.0,
      "integer_only": false
    }
  ]
}
```

---

## 3. `GET /profiles/demo/dashboard` (y `GET /profiles/{profile_id}/dashboard`)
Devuelve el resumen de los cuatro indicadores de bienestar del perfil ficticio (`demo` o `CM-01`..`CM-06`), el último registro disponible de cada indicador y la comparación descriptiva contra su mediana histórica personal compatible (`baseline_v1`).

### Parámetros Query opcionales
- `at`: Cursor temporal ISO 8601 (`YYYY-MM-DD` o `YYYY-MM-DDTHH:MM:SSZ`) para inspeccionar el estado en un día específico de la misión.

### Ejemplo de respuesta (`200 OK`)
```json
{
  "profile": {
    "id": "demo",
    "uuid": "00000000-0000-5000-8000-000000000000",
    "alias": "Cmdr. Alex Vega (DEMO SIMULADO)",
    "display_name": "Cmdr. Alex Vega (DEMO)",
    "profile_type": "fictional_astronaut",
    "role": "Commander",
    "mission": "SIM-ISS-180",
    "namespace": "demo",
    "is_simulated": true,
    "created_at": "2026-03-01T00:00:00Z",
    "updated_at": "2026-03-01T00:00:00Z"
  },
  "namespace": "demo",
  "data_label": "SIMULADO",
  "is_simulated": true,
  "cursor_timestamp": null,
  "latest_recorded_at": "2026-08-27T06:51:00Z",
  "disclaimer": "ARTEMIS HEALTH es una plataforma informativa y educativa...",
  "indicators_summary": [
    {
      "slot": "resting_hr_bpm",
      "indicator": "resting_hr_bpm",
      "label": "Frecuencia cardíaca en reposo",
      "unit": "bpm",
      "context": "rest",
      "latest_observation": {
        "id": "...",
        "profile_id": "CM-01",
        "indicator": "resting_hr_bpm",
        "value": 61.0,
        "unit": "bpm",
        "context": "rest",
        "measured_at": "2026-08-27T06:51:00Z",
        "origin_type": "synthetic",
        "capture_method": "import",
        "quality_flag": "ok",
        "quality_flags": ["ok"]
      },
      "comparison": {
        "indicator": "resting_hr_bpm",
        "unit": "bpm",
        "context": "rest",
        "origin_type": "synthetic",
        "rule_version": "baseline_v1",
        "current_value": 61.0,
        "baseline_median": 59.5,
        "difference": 1.5,
        "sufficient_history": true,
        "status": "comparison_available",
        "days_used": 14,
        "minimum_days_required": 7,
        "window_days": 30,
        "max_days": 14,
        "period_start": "2026-08-13",
        "period_end": "2026-08-26",
        "descriptive_notice": "Regla baseline_v1: valor actual 61.0 bpm frente a mediana personal de 59.5 bpm (variación descriptiva de +1.5 bpm), calculada con 14 días compatibles entre 2026-08-13 y 2026-08-26. Aviso descriptivo no clínico."
      }
    }
  ]
}
```

---

## 4. `POST /observations` (y `POST /api/observations`)
Registra una observación manual o de sensor de manera transaccional con validación completa de dominios, unidades, fechas e idempotencia por UUID.
- **`201 Created`**: Observación nueva creada.
- **`200 OK`**: Reenvío idéntico del mismo UUID (`idempotent: true`).
- **`409 Conflict`**: El UUID ya existe con valores o campos diferentes (`code: "UUID_CONFLICT"`).
- **`422 Unprocessable Entity`**: Valor fuera de rango, unidad incompatible o intento de mezclar `public_dataset` en `demo`.

### Ejemplo de solicitud
```json
{
  "id": "b7c8e910-32a4-4f19-9a1b-001122334455",
  "profile_id": "demo",
  "indicator": "resting_hr_bpm",
  "value": 63.0,
  "unit": "bpm",
  "measured_at": "2026-09-01T07:15:00Z",
  "context": "rest",
  "origin_type": "user_report",
  "capture_method": "manual",
  "source_reference": "Automedición matutina",
  "quality_flag": "ok"
}
```

---

## 5. `GET /profiles/demo/observations` (y `GET /profiles/{profile_id}/observations`)
Consulta el historial cronológico de observaciones con filtros opcionales:
- `indicator`: `resting_hr_bpm`, `sleep_duration_h`, `fatigue`, `perceived_stress`, `samn_perelli`, `stress_vas`.
- `from` (o `start_date`): Fecha inicial inclusiva ISO 8601.
- `to` (o `end_date`): Fecha final inclusiva ISO 8601.
- `origin_type`: `synthetic` o `user_report`.

---

## 6. `GET /profiles/demo/trends` (y `GET /profiles/{profile_id}/trends`)
Devuelve las series temporales listas para graficar en Recharts. Los valores faltantes o imputados excluidos se entregan con `value: null` e `is_gap: true` (`interpolation_applied: false`).

---

## 7. `POST /checkins` (y `GET /checkins`)
Registra un seguimiento diario de bienestar con fatiga (`1-5`), estrés percibido (`1-5`) y notas opcionales no identificables (máximo 500 caracteres, sin datos clínicos personales).

### Ejemplo de solicitud
```json
{
  "id": "e4d909c2-90d0-4fb5-9d88-7c6b5a4e3f21",
  "profile_id": "demo",
  "date": "2026-09-01",
  "fatigue": 2,
  "perceived_stress": 3,
  "notes": "Jornada de mantenimiento estándar sin contratiempos."
}
```

---

## 8. `GET /educational-content` (y `GET /educational-content/{indicator}`)
Devuelve las fichas educativas de los cuatro indicadores con descripción, unidad, limitaciones de interpretación y referencia bibliográfica verificada.

---

## 9. `GET /research/datasets`
Devuelve el catálogo de metadatos de datasets científicos (`bedrest_actigraphy_clean.csv`, `bedrest_winscat_clean.csv`, `inspiration4_blood_long.csv`, `iss_radiation_daily_clean.csv`, `crew_daily_log_clean.csv` y el estado excluido/auditado de `astronaut_health_observations.csv`), garantizando `included_in_personal_calculations: false` y el aislamiento estricto respecto al espacio `demo`.
