"""Repository factory and FastAPI dependency provider."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from artemis_health.core.config import get_settings
from artemis_health.repositories.base import WellnessRepository
from artemis_health.repositories.sqlite_repository import SQLiteWellnessRepository
from artemis_health.repositories.supabase_repository import SupabasePostgresRepository

_SQLITE_CACHE: Dict[Path, SQLiteWellnessRepository] = {}
_OVERRIDE_REPOSITORY: Optional[WellnessRepository] = None


def set_repository_override(repo: Optional[WellnessRepository]) -> None:
    """Set or clear a repository override (used for testing Supabase failures or custom DBs)."""
    global _OVERRIDE_REPOSITORY
    _OVERRIDE_REPOSITORY = repo


def get_repository() -> WellnessRepository:
    """Resolve the active repository instance according to current Settings."""
    if _OVERRIDE_REPOSITORY is not None:
        return _OVERRIDE_REPOSITORY

    settings = get_settings()
    if settings.active_backend_type in ("postgres", "supabase_rest"):
        return SupabasePostgresRepository(settings=settings)

    db_path = settings.sqlite_path.resolve()
    if db_path not in _SQLITE_CACHE:
        _SQLITE_CACHE[db_path] = SQLiteWellnessRepository(db_path=db_path, auto_seed=True)
    return _SQLITE_CACHE[db_path]


def reset_repository_cache() -> None:
    """Clear cached SQLite repository instances (e.g. when simulating service restart)."""
    _SQLITE_CACHE.clear()
