"""Database connection providers for PostgreSQL (Supabase) and persistent local SQLite."""
from __future__ import annotations

import os
import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from urllib.parse import urlsplit

from artemis_health.core.config import get_settings
from artemis_health.core.exceptions import SupabaseUnavailableError

logger = logging.getLogger(__name__)


def connection_failure_category(exc: Exception) -> str:
    """Classify failures without logging connection strings or driver messages."""
    message = str(exc).lower()
    for fragments, category in (
        (("circuit breaker", "too many authentication errors"), "pooler_auth_lockout"),
        (("password authentication failed", "invalid password"), "authentication"),
        (("no password supplied", "password is required"), "missing_password"),
        (("tenant or user not found",), "pooler_user"),
        (("network is unreachable", "no route to host", "cannot assign requested address"), "network_unreachable"),
        (("ssl", "certificate", "tls"), "tls"),
        (("could not translate host", "failed to resolve host", "name or service not known"), "dns"),
        (("connection refused",), "connection_refused"),
        (("timeout", "timed out"), "timeout"),
        (("invalid connection option", "missing \"=\"", "invalid percent", "invalid integer value"), "connection_format"),
    ):
        if any(fragment in message for fragment in fragments):
            return category
    return type(exc).__name__


@contextmanager
def postgres_connection(*, admin: bool = False) -> Generator[Any, None, None]:
    """Open a short-lived TLS PostgreSQL connection compatible with Supabase Supavisor pooling."""
    key = "DATABASE_ADMIN_URL" if admin else "DATABASE_URL"
    url = os.environ.get(key, "").strip()
    if not url:
        logger.warning("PostgreSQL unavailable: category=missing_url")
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
        try:
            target = urlsplit(url)
            host = target.hostname or ""
            host_kind = "shared_pooler" if host.endswith(".pooler.supabase.com") else "direct_supabase" if host.endswith(".supabase.co") else "other"
            target_summary = "host_kind=%s port=%s has_password=%s" % (host_kind, target.port, bool(target.password))
        except ValueError:
            target_summary = "invalid_uri=True"
        logger.warning(
            "PostgreSQL unavailable: category=%s sqlstate=%s %s",
            connection_failure_category(exc), getattr(exc, "sqlstate", None), target_summary,
        )
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
