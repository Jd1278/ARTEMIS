"""Database connection providers for PostgreSQL (Supabase) and persistent local SQLite."""
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from artemis_health.core.config import get_settings
from artemis_health.core.exceptions import SupabaseUnavailableError


@contextmanager
def postgres_connection(*, admin: bool = False) -> Generator[Any, None, None]:
    """Open a short-lived TLS PostgreSQL connection compatible with Supabase Supavisor pooling."""
    key = "DATABASE_ADMIN_URL" if admin else "DATABASE_URL"
    url = os.environ.get(key, "").strip()
    if not url:
        raise RuntimeError(f"{key} is not configured")
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as exc:
        raise SupabaseUnavailableError(
            "El controlador PostgreSQL (psycopg) no está disponible en este entorno."
        ) from exc

    try:
        with psycopg.connect(
            url,
            sslmode="require",
            connect_timeout=10,
            prepare_threshold=None,
            row_factory=dict_row,
        ) as conn:
            yield conn
    except Exception as exc:
        raise SupabaseUnavailableError(
            "No fue posible establecer conexión segura con Supabase PostgreSQL. El registro NO FUE GUARDADO."
        ) from exc


@contextmanager
def get_sqlite_connection(db_path: Path | None = None) -> Generator[sqlite3.Connection, None, None]:
    """Open a transactional SQLite connection with foreign keys enabled."""
    target_path = db_path or get_settings().sqlite_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path), timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        yield conn
    finally:
        conn.close()
