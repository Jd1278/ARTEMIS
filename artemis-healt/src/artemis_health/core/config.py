"""Environment-based application configuration for ARTEMIS HEALTH.

Never logs or exposes SUPABASE_SERVICE_ROLE_KEY, DATABASE_URL, or DATABASE_ADMIN_URL
to API clients or frontend responses.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _parse_origins(raw: str) -> List[str]:
    items = [item.strip() for item in raw.split(",") if item.strip()]
    return items or ["http://localhost:5173", "http://localhost:3000", "https://artemis-health.vercel.app"]


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings loaded from environment variables."""

    app_name: str = "ARTEMIS HEALTH API"
    app_version: str = "1.0.0"
    artemis_mode: str = field(default_factory=lambda: os.environ.get("ARTEMIS_MODE", "demo").strip() or "demo")
    artemis_storage: str = field(
        default_factory=lambda: os.environ.get("ARTEMIS_STORAGE", "auto").strip().lower() or "auto"
    )
    database_url: str = field(default_factory=lambda: os.environ.get("DATABASE_URL", "").strip())
    database_admin_url: str = field(default_factory=lambda: os.environ.get("DATABASE_ADMIN_URL", "").strip())
    supabase_url: str = field(default_factory=lambda: os.environ.get("SUPABASE_URL", "").strip())
    supabase_anon_key: str = field(default_factory=lambda: os.environ.get("SUPABASE_ANON_KEY", "").strip())
    supabase_service_role_key: str = field(
        default_factory=lambda: os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    )
    sqlite_path: Path = field(
        default_factory=lambda: Path(
            os.environ.get("ARTEMIS_SQLITE_PATH", str(PROJECT_ROOT / "var" / "artemis_health.db"))
        )
    )
    cors_origins: List[str] = field(
        default_factory=lambda: _parse_origins(
            os.environ.get(
                "CORS_ORIGINS",
                os.environ.get(
                    "FRONTEND_ORIGIN",
                    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,https://artemis-health.vercel.app",
                ),
            )
        )
    )
    log_level: str = field(default_factory=lambda: os.environ.get("LOG_LEVEL", "INFO").upper())

    @property
    def has_postgres_config(self) -> bool:
        return bool(self.database_url)

    @property
    def has_supabase_rest_config(self) -> bool:
        return bool(self.supabase_url and (self.supabase_service_role_key or self.supabase_anon_key))

    @property
    def active_backend_type(self) -> str:
        if self.artemis_storage in ("postgres", "supabase_pg"):
            return "postgres"
        if self.artemis_storage == "supabase_rest":
            return "supabase_rest"
        if self.artemis_storage == "sqlite":
            return "sqlite"
        if self.has_postgres_config:
            return "postgres"
        if self.has_supabase_rest_config:
            return "supabase_rest"
        return "sqlite"


def get_settings() -> Settings:
    """Return a fresh settings snapshot from the current environment."""
    return Settings()
