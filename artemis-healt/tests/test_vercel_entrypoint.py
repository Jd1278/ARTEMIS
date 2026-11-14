"""Deployment-only checks: preserve API/SPA routing and deny public writes."""
from pathlib import Path
import importlib.util

from fastapi.testclient import TestClient


def test_vercel_entrypoint_is_read_only_and_serves_spa(monkeypatch, tmp_path):
    monkeypatch.setenv("ARTEMIS_STORAGE", "sqlite")
    monkeypatch.setenv("ARTEMIS_SQLITE_PATH", str(tmp_path / "deployment-test.db"))
    entrypoint = Path(__file__).resolve().parents[1] / "app.py"
    spec = importlib.util.spec_from_file_location("vercel_entrypoint_test", entrypoint)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with TestClient(module.app) as client:
        schema = client.get("/openapi.json")
        assert schema.status_code == 200
        assert "/api/profiles" in schema.json()["paths"]
        denied = client.post("/api/observations", json={})
        assert denied.status_code == 403
        assert denied.json()["code"] == "READ_ONLY_DEMO"
        dist = entrypoint.parent / "frontend" / "dist"
        if dist.is_dir():
            for route in ("/", "/history", "/log"):
                response = client.get(route)
                assert response.status_code == 200
                assert '<div id="root">' in response.text
            assert client.get("/api/not-a-route").status_code == 404
            assert client.get("/assets/missing.js").status_code == 404
