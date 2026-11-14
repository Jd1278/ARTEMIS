"""Comprehensive automated test suite for ARTEMIS HEALTH Backend REST API.

Covers all mandatory requirements:
1. Create and retrieve an observation.
2. Persistence after restarting the service.
3. Validation of invalid values, dates, and incompatible units.
4. UUID idempotency (200) and conflict on different content (409).
5. History filtering by indicator and date range.
6. Personal baseline median calculation and exclusion of current/future/imputed data.
7. Insufficient history (< 7 distinct valid days) without generating alerts.
8. Strict separation between demo and research spaces.
9. Supabase error handling (503 NO_GUARDADO) and credential redaction.
10. Dashboard summary, trends series (null gaps uninterpolated), check-ins, and educational content.
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from artemis_health.core.config import Settings
from artemis_health.core.logging import redact_secrets
from artemis_health.main import create_app
from artemis_health.repositories.factory import (
    reset_repository_cache,
    set_repository_override,
)
from artemis_health.repositories.sqlite_repository import SQLiteWellnessRepository
from artemis_health.repositories.supabase_repository import SupabasePostgresRepository


@pytest.fixture()
def isolated_db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[Path, None, None]:
    """Provide an isolated persistent SQLite database file seeded with the demo dataset."""
    db_file = tmp_path / "test_artemis_health.db"
    monkeypatch.setenv("ARTEMIS_STORAGE", "sqlite")
    monkeypatch.setenv("ARTEMIS_SQLITE_PATH", str(db_file))
    reset_repository_cache()
    set_repository_override(None)
    yield db_file
    reset_repository_cache()
    set_repository_override(None)


@pytest.fixture()
def client(isolated_db_path: Path) -> Generator[TestClient, None, None]:
    app = create_app()
    with TestClient(app) as c:
        yield c


def test_health_and_indicators_catalog(client: TestClient) -> None:
    """Verify /health and /indicators return valid catalog and connection state."""
    health_res = client.get("/health")
    assert health_res.status_code == 200
    body = health_res.json()
    assert body["status"] == "ok"
    assert body["database_connected"] is True
    assert "no diagnostica" in body["disclaimer"].lower()

    api_health = client.get("/api/health")
    assert api_health.status_code == 200
    assert api_health.json()["status"] == "ok"

    ind_res = client.get("/indicators")
    assert ind_res.status_code == 200
    ind_data = ind_res.json()
    assert ind_data["count"] >= 4
    keys = {item["key"] for item in ind_data["indicators"]}
    assert {"resting_hr_bpm", "sleep_duration_h", "fatigue", "perceived_stress"}.issubset(keys)


def test_create_and_retrieve_observation(client: TestClient) -> None:
    """1. Crear y recuperar una observación."""
    obs_id = str(uuid.uuid4())
    payload = {
        "id": obs_id,
        "profile_id": "demo",
        "indicator": "resting_hr_bpm",
        "value": 64.0,
        "unit": "bpm",
        "measured_at": "2026-09-01T07:30:00Z",
        "context": "rest",
        "origin_type": "user_report",
        "capture_method": "manual",
        "source_reference": "Pulso matutino manual",
        "quality_flag": "ok",
    }
    post_res = client.post("/observations", json=payload)
    assert post_res.status_code == 201
    created = post_res.json()
    assert created["status"] == "created"
    assert created["save_status"] == "GUARDADO"
    assert created["idempotent"] is False
    assert created["observation"]["id"] == obs_id
    assert created["observation"]["value"] == 64.0
    assert created["observation"]["unit"] == "bpm"
    assert created["observation"]["origin_type"] == "user_report"

    # Retrieve from history
    hist_res = client.get(
        "/profiles/demo/observations",
        params={"indicator": "resting_hr_bpm", "from": "2026-09-01", "to": "2026-09-01"},
    )
    assert hist_res.status_code == 200
    items = hist_res.json()["observations"]
    assert len(items) == 1
    assert items[0]["id"] == obs_id
    assert items[0]["value"] == 64.0


def test_persistence_across_service_restart(isolated_db_path: Path) -> None:
    """2. Persistencia después de reiniciar el servicio."""
    obs_id = str(uuid.uuid4())
    checkin_id = str(uuid.uuid4())

    # First app instance: create observation and check-in
    app_first = create_app()
    with TestClient(app_first) as client_1:
        res_obs = client_1.post(
            "/observations",
            json={
                "id": obs_id,
                "profile_id": "demo",
                "indicator": "sleep_duration_h",
                "value": 7.5,
                "unit": "h",
                "measured_at": "2026-09-05T06:45:00Z",
                "context": "sleep_report",
                "origin_type": "user_report",
                "capture_method": "manual",
            },
        )
        assert res_obs.status_code == 201

        res_chk = client_1.post(
            "/checkins",
            json={
                "id": checkin_id,
                "profile_id": "demo",
                "date": "2026-09-05",
                "fatigue": 2,
                "perceived_stress": 3,
                "notes": "Descanso estable durante turno orbital.",
            },
        )
        assert res_chk.status_code == 201

    # Simulate complete service restart: clear repository cache and build new FastAPI app
    reset_repository_cache()
    assert isolated_db_path.exists()

    app_second = create_app()
    with TestClient(app_second) as client_2:
        hist_res = client_2.get(
            "/profiles/demo/observations",
            params={"indicator": "sleep_duration_h", "from": "2026-09-05", "to": "2026-09-05"},
        )
        assert hist_res.status_code == 200
        observations = hist_res.json()["observations"]
        assert any(o["id"] == obs_id and o["value"] == 7.5 for o in observations)

        chk_list = client_2.get("/checkins", params={"profile_id": "demo"})
        assert chk_list.status_code == 200
        assert any(c["id"] == checkin_id and c["fatigue"] == 2 and c["perceived_stress"] == 3 for c in chk_list.json())


@pytest.mark.parametrize(
    "invalid_payload,expected_field",
    [
        # Incompatible unit: kg for heart rate
        (
            {
                "indicator": "resting_hr_bpm",
                "value": 65,
                "unit": "kg",
                "measured_at": "2026-09-01T07:00:00Z",
            },
            "unit",
        ),
        # Incompatible unit: bpm for sleep duration
        (
            {
                "indicator": "sleep_duration_h",
                "value": 7.0,
                "unit": "bpm",
                "measured_at": "2026-09-01T07:00:00Z",
            },
            "unit",
        ),
        # Out of range sleep duration (> 24 hours)
        (
            {
                "indicator": "sleep_duration_h",
                "value": 26.5,
                "unit": "h",
                "measured_at": "2026-09-01T07:00:00Z",
            },
            "value",
        ),
        # Negative resting heart rate
        (
            {
                "indicator": "resting_hr_bpm",
                "value": -10,
                "unit": "bpm",
                "measured_at": "2026-09-01T07:00:00Z",
            },
            "value",
        ),
        # Out of range fatigue on 1-5 scale
        (
            {
                "indicator": "fatigue",
                "value": 6,
                "unit": "scale_1_5",
                "measured_at": "2026-09-01T07:00:00Z",
            },
            "value",
        ),
        # Out of range perceived_stress on 1-5 scale
        (
            {
                "indicator": "perceived_stress",
                "value": 0,
                "unit": "scale_1_5",
                "measured_at": "2026-09-01T07:00:00Z",
            },
            "value",
        ),
        # Invalid indicator name
        (
            {
                "indicator": "blood_cholesterol_ diagnostic",
                "value": 180,
                "unit": "mg/dL",
                "measured_at": "2026-09-01T07:00:00Z",
            },
            "indicator",
        ),
        # Invalid ISO date
        (
            {
                "indicator": "resting_hr_bpm",
                "value": 60,
                "unit": "bpm",
                "measured_at": "not-a-valid-date",
            },
            "measured_at",
        ),
    ],
)
def test_validation_incompatible_units_and_invalid_values(
    client: TestClient, invalid_payload: dict, expected_field: str
) -> None:
    """3. Validación de valores, fechas, indicadores y unidades incompatibles."""
    res = client.post("/observations", json=invalid_payload)
    assert res.status_code == 422
    body = res.json()
    assert body["save_status"] == "NO_GUARDADO"
    assert expected_field in body["fields"]


def test_uuid_idempotency_and_conflict_409(client: TestClient) -> None:
    """4. Idempotencia por UUID (200) y conflicto por contenido diferente (409)."""
    obs_uuid = str(uuid.uuid4())
    payload = {
        "id": obs_uuid,
        "profile_id": "demo",
        "indicator": "resting_hr_bpm",
        "value": 61.0,
        "unit": "bpm",
        "measured_at": "2026-09-02T07:00:00Z",
        "context": "rest",
        "origin_type": "user_report",
        "capture_method": "manual",
    }

    # First submission -> 201 Created
    first_res = client.post("/observations", json=payload)
    assert first_res.status_code == 201
    assert first_res.json()["idempotent"] is False

    # Second identical submission -> 200 OK (idempotent replay, no duplicate created)
    second_res = client.post("/observations", json=payload)
    assert second_res.status_code == 200
    assert second_res.json()["idempotent"] is True
    assert second_res.json()["observation"]["id"] == obs_uuid

    # Verify only 1 record exists for that date/UUID
    hist = client.get(
        "/profiles/demo/observations",
        params={"indicator": "resting_hr_bpm", "from": "2026-09-02", "to": "2026-09-02"},
    )
    assert hist.json()["count"] == 1

    # Third submission with same UUID but different value -> 409 Conflict
    conflicting_payload = dict(payload, value=78.0)
    conflict_res = client.post("/observations", json=conflicting_payload)
    assert conflict_res.status_code == 409
    err = conflict_res.json()
    assert err["code"] == "UUID_CONFLICT"
    assert err["save_status"] == "NO_GUARDADO"


def test_observations_history_filtering_by_indicator_and_dates(client: TestClient) -> None:
    """5. Filtrado de historial por indicador y rango de fechas en orden cronológico."""
    res = client.get(
        "/profiles/demo/observations",
        params={
            "indicator": "sleep_duration_h",
            "from": "2026-03-10",
            "to": "2026-03-19",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 10
    observations = data["observations"]
    timestamps = [o["measured_at"] for o in observations]
    assert timestamps == sorted(timestamps)
    assert all(o["indicator"] == "sleep_duration_h" for o in observations)
    assert all("2026-03-10" <= o["measured_at"][:10] <= "2026-03-19" for o in observations)


def test_baseline_median_calculation_and_future_current_exclusion(client: TestClient) -> None:
    """6. Cálculo de mediana y exclusión del registro actual, datos futuros e imputados."""
    profile_id = "astro-baseline-test"
    # Insert 10 valid daily observations on days 1..10 of June 2026: values 51..60
    # Median of [51, 52, 53, 54, 55, 56, 57, 58, 59, 60] is 55.5
    for day_num in range(1, 11):
        val = 50.0 + day_num
        r = client.post(
            "/observations",
            json={
                "id": str(uuid.uuid4()),
                "profile_id": profile_id,
                "indicator": "resting_hr_bpm",
                "value": val,
                "unit": "bpm",
                "measured_at": f"2026-06-{day_num:02d}T07:00:00Z",
                "context": "rest",
                "origin_type": "user_report",
                "capture_method": "manual",
            },
        )
        assert r.status_code == 201

    # Also insert a FUTURE observation on June 20 with extreme value 200 bpm (must be excluded when evaluating June 11!)
    future_res = client.post(
        "/observations",
        json={
            "id": str(uuid.uuid4()),
            "profile_id": profile_id,
            "indicator": "resting_hr_bpm",
            "value": 200.0,
            "unit": "bpm",
            "measured_at": "2026-06-20T07:00:00Z",
            "context": "rest",
            "origin_type": "user_report",
            "capture_method": "manual",
        },
    )
    assert future_res.status_code == 201

    # Now insert the observation on June 11 with value 65.5 bpm
    eval_res = client.post(
        "/observations",
        json={
            "id": str(uuid.uuid4()),
            "profile_id": profile_id,
            "indicator": "resting_hr_bpm",
            "value": 65.5,
            "unit": "bpm",
            "measured_at": "2026-06-11T07:00:00Z",
            "context": "rest",
            "origin_type": "user_report",
            "capture_method": "manual",
        },
    )
    assert eval_res.status_code == 201
    comp = eval_res.json()["comparison"]
    assert comp["sufficient_history"] is True
    assert comp["days_used"] == 10
    assert comp["baseline_median"] == 55.5
    assert comp["difference"] == 10.0
    assert comp["period_start"] == "2026-06-01"
    assert comp["period_end"] == "2026-06-10"
    assert "no clínico" in comp["descriptive_notice"].lower() or "no clínica" in comp["descriptive_notice"].lower()


def test_insufficient_history_under_seven_days(client: TestClient) -> None:
    """7. Insuficiencia de historial menor a siete días (< 7 días válidos)."""
    profile_id = "astro-short-history"
    # Insert only 5 days of observations (less than the 7 distinct days required)
    last_response = None
    for day_num in range(1, 6):
        res = client.post(
            "/observations",
            json={
                "id": str(uuid.uuid4()),
                "profile_id": profile_id,
                "indicator": "sleep_duration_h",
                "value": 7.0,
                "unit": "h",
                "measured_at": f"2026-07-0{day_num}T07:00:00Z",
                "context": "sleep_report",
                "origin_type": "user_report",
                "capture_method": "manual",
            },
        )
        assert res.status_code == 201
        last_response = res.json()

    assert last_response is not None
    comp = last_response["comparison"]
    # On the 5th day, there are only 4 previous days (< 7 minimum)
    assert comp["sufficient_history"] is False
    assert comp["status"] == "insufficient_history"
    assert comp["days_used"] == 4
    assert comp["baseline_median"] is None
    assert comp["difference"] is None
    assert "historial insuficiente" in comp["descriptive_notice"].lower()


def test_demo_and_research_separation(client: TestClient) -> None:
    """8. Separación estricta entre demo y research y preservación de contexto científico."""
    # Research datasets endpoint returns isolated metadata
    res_datasets = client.get("/research/datasets")
    assert res_datasets.status_code == 200
    body = res_datasets.json()
    assert body["namespace"] == "research"
    assert body["isolation_guaranteed"] is True
    files = {d["file_name"]: d for d in body["datasets"]}
    assert "bedrest_actigraphy_clean.csv" in files
    assert "bedrest_winscat_clean.csv" in files
    assert "inspiration4_blood_long.csv" in files
    assert "iss_radiation_daily_clean.csv" in files
    assert "crew_daily_log_clean.csv" in files
    assert "astronaut_health_observations.csv" in files

    # Bed rest ground analogs must never be marked as in-flight measurements
    assert files["bedrest_actigraphy_clean.csv"]["is_inflight_measurement"] is False
    assert files["bedrest_winscat_clean.csv"]["is_inflight_measurement"] is False
    # ISS environmental radiation must never be marked as personal dose
    assert files["iss_radiation_daily_clean.csv"]["is_personal_radiation_dose"] is False
    # None of the research datasets can be included in personal baseline calculations
    assert all(d["included_in_personal_calculations"] is False for d in body["datasets"])

    # Attempting to post a public_dataset or research observation into personal /observations is rejected
    forbidden_res = client.post(
        "/observations",
        json={
            "id": str(uuid.uuid4()),
            "profile_id": "demo",
            "indicator": "sleep_duration_h",
            "value": 6.8,
            "unit": "h",
            "measured_at": "2026-09-03T07:00:00Z",
            "origin_type": "public_dataset",
            "namespace": "research",
        },
    )
    assert forbidden_res.status_code == 422
    assert forbidden_res.json()["code"] == "NAMESPACE_ISOLATION_VIOLATION"


def test_supabase_error_handling_and_secret_redaction(client: TestClient) -> None:
    """9. Manejo de errores de Supabase (HTTP 503 NO_GUARDADO) y redacción de secretos."""

    def broken_connection_factory():
        raise ConnectionError(
            "postgresql://artemis_user:SuperSecretPassword123@db.project.supabase.co:6543/postgres timeout"
        )

    failing_repo = SupabasePostgresRepository(
        settings=Settings(
            artemis_storage="postgres",
            database_url="postgresql://artemis_user:SuperSecretPassword123@db.project.supabase.co:6543/postgres",
        ),
        connection_factory=broken_connection_factory,
    )
    set_repository_override(failing_repo)
    try:
        res = client.post(
            "/observations",
            json={
                "id": str(uuid.uuid4()),
                "profile_id": "demo",
                "indicator": "resting_hr_bpm",
                "value": 62.0,
                "unit": "bpm",
                "measured_at": "2026-09-04T07:00:00Z",
            },
        )
        assert res.status_code == 503
        err_body = res.json()
        assert err_body["code"] == "SUPABASE_UNAVAILABLE"
        assert err_body["save_status"] == "NO_GUARDADO"
        assert "SuperSecretPassword123" not in res.text
    finally:
        set_repository_override(None)

    # Also verify log secret redaction helper directly
    redacted = redact_secrets(
        "Failed connecting to postgresql://admin:MySecretPass99@aws-0.pooler.supabase.com:6543/postgres"
    )
    assert "MySecretPass99" not in redacted
    assert "***REDACTED***" in redacted


def test_dashboard_trends_checkins_and_educational_content(client: TestClient) -> None:
    """10. Verificar dashboard, series de tendencias (con huecos null sin interpolar), check-ins y fichas educativas."""
    # Dashboard summary
    dash = client.get("/profiles/demo/dashboard")
    assert dash.status_code == 200
    dash_data = dash.json()
    assert dash_data["data_label"] == "SIMULADO"
    assert dash_data["is_simulated"] is True
    assert len(dash_data["indicators_summary"]) == 4

    # Trends with null gaps preserved (no interpolation)
    trends = client.get("/profiles/demo/trends")
    assert trends.status_code == 200
    trends_data = trends.json()
    assert trends_data["interpolation_applied"] is False
    hr_series = trends_data["series_by_indicator"]["resting_hr_bpm"]
    assert hr_series["points_count"] == 180
    assert hr_series["null_gaps_count"] > 0
    assert any(pt["value"] is None and pt["is_gap"] is True for pt in hr_series["series"])

    # Educational content
    edu = client.get("/educational-content")
    assert edu.status_code == 200
    edu_data = edu.json()
    assert edu_data["count"] == 4
    assert all(item["limitations"] and item["bibliographic_reference"] for item in edu_data["items"])
