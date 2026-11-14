"""Transactional, parameterized SQLite repository for local execution and automated tests.

Automatically seeds the 4,320 synthetic demo observations from data/demo/observations.json,
fictional profiles, indicator catalog, educational content, and research dataset metadata.
"""
from __future__ import annotations

import json
import math
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional, Tuple

from artemis_health.core.constants import DEFAULT_DEMO_PROFILES, INDICATOR_CATALOG
from artemis_health.core.exceptions import ObservationConflictError, SupabaseUnavailableError
from artemis_health.database.connection import get_sqlite_connection
from artemis_health.database.seed import (
    DEFAULT_EDUCATIONAL_CARDS,
    DEFAULT_RESEARCH_DATASETS,
    load_packaged_demo_observations,
)
from artemis_health.models.entities import (
    CheckinRecord,
    EducationalContentRecord,
    IndicatorRecord,
    ObservationRecord,
    ProfileRecord,
    ResearchDatasetRecord,
)
from artemis_health.repositories.base import WellnessRepository


def _values_equal(a: Optional[float], b: Optional[float]) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-9)


def _primary_flag(flags: List[str], explicit_flag: Optional[str] = None) -> str:
    if explicit_flag and explicit_flag != "ok":
        return explicit_flag
    for f in flags:
        if f.endswith("_imputed") or f == "imputed":
            return "imputed"
        if f.endswith("_out_of_range") or f == "out_of_range":
            return "out_of_range"
        if f in ("missing", "stale", "incompatible", "pending_review"):
            return f
    return explicit_flag or "ok"


class SQLiteWellnessRepository(WellnessRepository):
    """Persistent SQLite repository using parameterized SQL and atomic transactions."""

    def __init__(self, db_path: Optional[Path] = None, *, auto_seed: bool = True) -> None:
        self._db_path = db_path
        self._auto_seed = auto_seed
        self._ensure_initialized()

    def _conn(self):
        try:
            return get_sqlite_connection(self._db_path)
        except Exception as exc:
            raise SupabaseUnavailableError(
                "Error al conectar con el almacenamiento persistente. El registro NO FUE GUARDADO."
            ) from exc

    def _ensure_initialized(self) -> None:
        with self._conn() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    id TEXT PRIMARY KEY,
                    profile_uuid TEXT NOT NULL UNIQUE,
                    display_name TEXT NOT NULL,
                    alias TEXT NOT NULL,
                    profile_type TEXT NOT NULL DEFAULT 'fictional_astronaut',
                    role TEXT NOT NULL DEFAULT 'Crew Member',
                    mission TEXT NOT NULL DEFAULT 'SIM-ISS-180',
                    namespace TEXT NOT NULL DEFAULT 'demo' CHECK (namespace IN ('demo', 'research')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS indicators (
                    key TEXT PRIMARY KEY,
                    label TEXT NOT NULL,
                    description TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    allowed_units TEXT NOT NULL,
                    context TEXT NOT NULL,
                    minimum REAL,
                    maximum REAL,
                    integer_only INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS observations (
                    id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL,
                    namespace TEXT NOT NULL DEFAULT 'demo' CHECK (namespace IN ('demo', 'research')),
                    indicator TEXT NOT NULL,
                    value REAL,
                    source_value REAL,
                    unit TEXT NOT NULL,
                    context TEXT NOT NULL,
                    measured_at TEXT NOT NULL,
                    mission_day INTEGER,
                    origin_type TEXT NOT NULL CHECK (origin_type IN ('synthetic', 'user_report', 'public_dataset')),
                    capture_method TEXT NOT NULL CHECK (capture_method IN ('manual', 'sensor', 'import')),
                    source_reference TEXT,
                    quality_flag TEXT NOT NULL DEFAULT 'ok',
                    quality_flags TEXT NOT NULL DEFAULT '["ok"]',
                    source_file TEXT,
                    source_row INTEGER,
                    import_batch_id TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (profile_id) REFERENCES profiles(id)
                );

                CREATE INDEX IF NOT EXISTS idx_observations_history
                    ON observations (profile_id, indicator, origin_type, context, measured_at DESC);

                CREATE TABLE IF NOT EXISTS checkins (
                    id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL,
                    namespace TEXT NOT NULL DEFAULT 'demo' CHECK (namespace = 'demo'),
                    checkin_date TEXT NOT NULL,
                    fatigue INTEGER NOT NULL CHECK (fatigue BETWEEN 1 AND 5),
                    perceived_stress INTEGER NOT NULL CHECK (perceived_stress BETWEEN 1 AND 5),
                    notes TEXT,
                    origin_type TEXT NOT NULL DEFAULT 'user_report',
                    capture_method TEXT NOT NULL DEFAULT 'manual',
                    quality_flag TEXT NOT NULL DEFAULT 'ok',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (profile_id) REFERENCES profiles(id)
                );

                CREATE INDEX IF NOT EXISTS idx_checkins_profile_date
                    ON checkins (profile_id, checkin_date DESC);

                CREATE TABLE IF NOT EXISTS educational_content (
                    id TEXT PRIMARY KEY,
                    indicator TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    limitations TEXT NOT NULL,
                    bibliographic_reference TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS research_datasets (
                    id TEXT PRIMARY KEY,
                    dataset_key TEXT NOT NULL UNIQUE,
                    file_name TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    namespace TEXT NOT NULL DEFAULT 'research',
                    origin_type TEXT NOT NULL,
                    capture_method TEXT NOT NULL,
                    study_context TEXT NOT NULL,
                    is_inflight_measurement INTEGER NOT NULL DEFAULT 0,
                    is_personal_radiation_dose INTEGER NOT NULL DEFAULT 0,
                    included_in_personal_calculations INTEGER NOT NULL DEFAULT 0 CHECK (included_in_personal_calculations = 0),
                    row_count INTEGER NOT NULL,
                    sha256 TEXT NOT NULL,
                    limitations TEXT NOT NULL,
                    source_reference TEXT NOT NULL,
                    quality_flag TEXT NOT NULL DEFAULT 'ok',
                    created_at TEXT NOT NULL
                );
                """
            )
            conn.execute("BEGIN IMMEDIATE;")
            try:

                now_iso = "2026-03-01T00:00:00Z"
                for p in DEFAULT_DEMO_PROFILES:
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO profiles
                        (id, profile_uuid, display_name, alias, profile_type, role, mission, namespace, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            p["id"],
                            p["profile_uuid"],
                            p["display_name"],
                            p["alias"],
                            p["profile_type"],
                            p["role"],
                            p["mission"],
                            p["namespace"],
                            now_iso,
                            now_iso,
                        ),
                    )

                for spec in INDICATOR_CATALOG.values():
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO indicators
                        (key, label, description, unit, allowed_units, context, minimum, maximum, integer_only)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            spec.key,
                            spec.label,
                            spec.description,
                            spec.canonical_unit,
                            json.dumps(list(spec.allowed_units)),
                            spec.default_context,
                            spec.minimum,
                            spec.maximum,
                            1 if spec.integer_only else 0,
                        ),
                    )

                for card in DEFAULT_EDUCATIONAL_CARDS:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO educational_content
                        (id, indicator, title, description, unit, limitations, bibliographic_reference, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            card["id"],
                            card["indicator"],
                            card["title"],
                            card["description"],
                            card["unit"],
                            card["limitations"],
                            card["bibliographic_reference"],
                            card["created_at"],
                        ),
                    )

                for ds in DEFAULT_RESEARCH_DATASETS:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO research_datasets
                        (id, dataset_key, file_name, title, namespace, origin_type, capture_method,
                         study_context, is_inflight_measurement, is_personal_radiation_dose,
                         included_in_personal_calculations, row_count, sha256, limitations,
                         source_reference, quality_flag, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            ds["id"],
                            ds["dataset_key"],
                            ds["file_name"],
                            ds["title"],
                            ds["namespace"],
                            ds["origin_type"],
                            ds["capture_method"],
                            ds["study_context"],
                            1 if ds["is_inflight_measurement"] else 0,
                            1 if ds["is_personal_radiation_dose"] else 0,
                            0,
                            ds["row_count"],
                            ds["sha256"],
                            ds["limitations"],
                            ds["source_reference"],
                            ds["quality_flag"],
                            ds["created_at"],
                        ),
                    )

                if self._auto_seed:
                    existing_synthetic = conn.execute(
                        "SELECT count(*) AS n FROM observations WHERE origin_type = 'synthetic'"
                    ).fetchone()["n"]
                    if existing_synthetic == 0:
                        demo_rows, manifest = load_packaged_demo_observations()
                        batch_id = manifest.get("output_sha256", "demo_seed_v1")
                        if demo_rows:
                            conn.executemany(
                                """
                                INSERT OR IGNORE INTO observations
                                (id, profile_id, namespace, indicator, value, source_value, unit, context,
                                 measured_at, mission_day, origin_type, capture_method, source_reference,
                                 quality_flag, quality_flags, source_file, source_row, import_batch_id, created_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """,
                                [
                                    (
                                        r["id"],
                                        r["profile_id"],
                                        r.get("namespace", "demo"),
                                        r["indicator"],
                                        r["value"],
                                        r.get("source_value"),
                                        r["unit"],
                                        r["context"],
                                        r["timestamp"],
                                        r.get("mission_day"),
                                        r.get("origin_type", "synthetic"),
                                        r.get("capture_method", "import"),
                                        r.get("source_file", "crew_daily_log_clean.csv"),
                                        _primary_flag(r.get("quality_flags", ["ok"])),
                                        json.dumps(r.get("quality_flags", ["ok"])),
                                        r.get("source_file"),
                                        r.get("source_row"),
                                        batch_id,
                                        r["timestamp"],
                                    )
                                    for r in demo_rows
                                ],
                            )
                conn.execute("COMMIT;")
            except Exception:
                if conn.in_transaction:
                    conn.execute("ROLLBACK;")
                raise

    def check_health(self) -> Tuple[bool, str]:
        with self._conn() as conn:
            row = conn.execute("SELECT 1 AS ok").fetchone()
            return bool(row and row["ok"] == 1), "sqlite"

    def list_profiles(self, namespace: str = "demo") -> List[ProfileRecord]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM profiles WHERE namespace = ? ORDER BY id ASC",
                (namespace,),
            ).fetchall()
            return [self._row_to_profile(r) for r in rows]

    def get_profile(self, profile_id: str, namespace: str = "demo") -> Optional[ProfileRecord]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM profiles WHERE id = ? AND namespace = ?",
                (profile_id, namespace),
            ).fetchone()
            return self._row_to_profile(row) if row else None

    def ensure_demo_profile(self, profile_id: str) -> ProfileRecord:
        existing = self.get_profile(profile_id, namespace="demo")
        if existing:
            return existing
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        profile_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"artemis:profile:{profile_id}"))
        record = ProfileRecord(
            id=profile_id,
            profile_uuid=profile_uuid,
            display_name=f"{profile_id} (DEMO)",
            alias=f"Astronauta Ficticio {profile_id} (SIMULADO)",
            profile_type="fictional_astronaut",
            role="Crew Member",
            mission="SIM-ISS-180",
            namespace="demo",
            created_at=now_iso,
            updated_at=now_iso,
        )
        with self._conn() as conn:
            conn.execute("BEGIN IMMEDIATE;")
            try:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO profiles
                    (id, profile_uuid, display_name, alias, profile_type, role, mission, namespace, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.id,
                        record.profile_uuid,
                        record.display_name,
                        record.alias,
                        record.profile_type,
                        record.role,
                        record.mission,
                        record.namespace,
                        record.created_at,
                        record.updated_at,
                    ),
                )
                conn.execute("COMMIT;")
            except Exception:
                if conn.in_transaction:
                    conn.execute("ROLLBACK;")
                raise
        return self.get_profile(profile_id, namespace="demo") or record

    def list_indicators(self) -> List[IndicatorRecord]:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM indicators ORDER BY key ASC").fetchall()
            return [
                IndicatorRecord(
                    key=r["key"],
                    label=r["label"],
                    description=r["description"],
                    unit=r["unit"],
                    allowed_units=json.loads(r["allowed_units"]),
                    context=r["context"],
                    minimum=r["minimum"],
                    maximum=r["maximum"],
                    integer_only=bool(r["integer_only"]),
                )
                for r in rows
            ]

    def get_observation_by_id(self, observation_id: str) -> Optional[ObservationRecord]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM observations WHERE id = ?",
                (observation_id,),
            ).fetchone()
            return self._row_to_observation(row) if row else None

    def save_observation(self, observation: ObservationRecord) -> Tuple[ObservationRecord, bool]:
        self.ensure_demo_profile(observation.profile_id)
        with self._conn() as conn:
            conn.execute("BEGIN IMMEDIATE;")
            try:
                existing_row = conn.execute(
                    "SELECT * FROM observations WHERE id = ?",
                    (observation.id,),
                ).fetchone()
                if existing_row is not None:
                    existing = self._row_to_observation(existing_row)
                    same_payload = (
                        existing.profile_id == observation.profile_id
                        and existing.indicator == observation.indicator
                        and _values_equal(existing.value, observation.value)
                        and existing.unit == observation.unit
                        and existing.context == observation.context
                        and existing.measured_at == observation.measured_at
                        and existing.origin_type == observation.origin_type
                        and existing.capture_method == observation.capture_method
                    )
                    conn.execute("COMMIT;")
                    if same_payload:
                        return existing, True
                    raise ObservationConflictError(
                        f"El UUID '{observation.id}' ya existe con contenido diferente. No se sobrescribió el registro.",
                        fields={
                            "id": [observation.id],
                            "existing_indicator": existing.indicator,
                            "existing_value": existing.value,
                            "existing_measured_at": existing.measured_at,
                        },
                    )

                now_iso = observation.created_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                q_flag = _primary_flag(observation.quality_flags, observation.quality_flag)
                conn.execute(
                    """
                    INSERT INTO observations
                    (id, profile_id, namespace, indicator, value, source_value, unit, context,
                     measured_at, mission_day, origin_type, capture_method, source_reference,
                     quality_flag, quality_flags, source_file, source_row, import_batch_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        observation.id,
                        observation.profile_id,
                        observation.namespace,
                        observation.indicator,
                        observation.value,
                        observation.source_value if observation.source_value is not None else observation.value,
                        observation.unit,
                        observation.context,
                        observation.measured_at,
                        observation.mission_day,
                        observation.origin_type,
                        observation.capture_method,
                        observation.source_reference,
                        q_flag,
                        json.dumps(observation.quality_flags or [q_flag]),
                        observation.source_file,
                        observation.source_row,
                        observation.import_batch_id,
                        now_iso,
                    ),
                )
                inserted_row = conn.execute(
                    "SELECT * FROM observations WHERE id = ?",
                    (observation.id,),
                ).fetchone()
                conn.execute("COMMIT;")
                return self._row_to_observation(inserted_row), False
            except ObservationConflictError:
                raise
            except Exception as exc:
                if conn.in_transaction:
                    conn.execute("ROLLBACK;")
                raise SupabaseUnavailableError(
                    "Error transaccional al guardar la observación. El registro NO FUE GUARDADO."
                ) from exc

    def list_observations(
        self,
        profile_id: str,
        *,
        indicator: Optional[str] = None,
        compatible_indicators: Optional[Tuple[str, ...]] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        origin_type: Optional[str] = None,
        namespace: str = "demo",
        limit: Optional[int] = None,
    ) -> List[ObservationRecord]:
        profile_ids = ("demo", "CM-01") if profile_id == "demo" else (profile_id,)
        placeholders = ",".join("?" for _ in profile_ids)
        clauses = [f"profile_id IN ({placeholders})", "namespace = ?"]
        params: List[Any] = [*profile_ids, namespace]

        if compatible_indicators:
            ind_placeholders = ",".join("?" for _ in compatible_indicators)
            clauses.append(f"indicator IN ({ind_placeholders})")
            params.extend(compatible_indicators)
        elif indicator:
            clauses.append("indicator = ?")
            params.append(indicator)

        if origin_type:
            clauses.append("origin_type = ?")
            params.append(origin_type)

        if from_timestamp:
            clauses.append("measured_at >= ?")
            params.append(from_timestamp)

        if to_timestamp:
            clauses.append("measured_at <= ?")
            params.append(to_timestamp)

        sql = f"SELECT * FROM observations WHERE {' AND '.join(clauses)} ORDER BY measured_at ASC, id ASC"
        if limit is not None and limit > 0:
            sql += " LIMIT ?"
            params.append(int(limit))

        with self._conn() as conn:
            rows = conn.execute(sql, tuple(params)).fetchall()
            return [self._row_to_observation(r) for r in rows]

    def save_checkin(self, checkin: CheckinRecord) -> Tuple[CheckinRecord, bool]:
        self.ensure_demo_profile(checkin.profile_id)
        with self._conn() as conn:
            conn.execute("BEGIN IMMEDIATE;")
            try:
                existing_row = conn.execute(
                    "SELECT * FROM checkins WHERE id = ?",
                    (checkin.id,),
                ).fetchone()
                if existing_row is not None:
                    existing = self._row_to_checkin(existing_row)
                    same_payload = (
                        existing.profile_id == checkin.profile_id
                        and existing.checkin_date == checkin.checkin_date
                        and existing.fatigue == checkin.fatigue
                        and existing.perceived_stress == checkin.perceived_stress
                        and (existing.notes or None) == (checkin.notes or None)
                    )
                    conn.execute("COMMIT;")
                    if same_payload:
                        return existing, True
                    raise ObservationConflictError(
                        f"El check-in con UUID '{checkin.id}' ya existe con valores diferentes.",
                        fields={"id": [checkin.id]},
                    )

                now_iso = checkin.created_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                conn.execute(
                    """
                    INSERT INTO checkins
                    (id, profile_id, namespace, checkin_date, fatigue, perceived_stress,
                     notes, origin_type, capture_method, quality_flag, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        checkin.id,
                        checkin.profile_id,
                        checkin.namespace,
                        checkin.checkin_date,
                        checkin.fatigue,
                        checkin.perceived_stress,
                        checkin.notes,
                        checkin.origin_type,
                        checkin.capture_method,
                        checkin.quality_flag,
                        now_iso,
                    ),
                )
                inserted_row = conn.execute(
                    "SELECT * FROM checkins WHERE id = ?",
                    (checkin.id,),
                ).fetchone()
                conn.execute("COMMIT;")
                return self._row_to_checkin(inserted_row), False
            except ObservationConflictError:
                raise
            except Exception as exc:
                if conn.in_transaction:
                    conn.execute("ROLLBACK;")
                raise SupabaseUnavailableError(
                    "Error transaccional al guardar el check-in. El registro NO FUE GUARDADO."
                ) from exc

    def list_checkins(self, profile_id: str) -> List[CheckinRecord]:
        profile_ids = ("demo", "CM-01") if profile_id == "demo" else (profile_id,)
        placeholders = ",".join("?" for _ in profile_ids)
        with self._conn() as conn:
            rows = conn.execute(
                f"SELECT * FROM checkins WHERE profile_id IN ({placeholders}) AND namespace = 'demo' ORDER BY checkin_date DESC, created_at DESC",
                tuple(profile_ids),
            ).fetchall()
            return [self._row_to_checkin(r) for r in rows]

    def list_educational_content(self, indicator: Optional[str] = None) -> List[EducationalContentRecord]:
        with self._conn() as conn:
            if indicator:
                rows = conn.execute(
                    "SELECT * FROM educational_content WHERE indicator = ? ORDER BY indicator ASC",
                    (indicator,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM educational_content ORDER BY created_at ASC, indicator ASC"
                ).fetchall()
            return [
                EducationalContentRecord(
                    id=r["id"],
                    indicator=r["indicator"],
                    title=r["title"],
                    description=r["description"],
                    unit=r["unit"],
                    limitations=r["limitations"],
                    bibliographic_reference=r["bibliographic_reference"],
                    created_at=r["created_at"],
                )
                for r in rows
            ]

    def list_research_datasets(self) -> List[ResearchDatasetRecord]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM research_datasets WHERE namespace = 'research' ORDER BY dataset_key ASC"
            ).fetchall()
            return [
                ResearchDatasetRecord(
                    id=r["id"],
                    dataset_key=r["dataset_key"],
                    file_name=r["file_name"],
                    title=r["title"],
                    namespace=r["namespace"],
                    origin_type=r["origin_type"],
                    capture_method=r["capture_method"],
                    study_context=r["study_context"],
                    is_inflight_measurement=bool(r["is_inflight_measurement"]),
                    is_personal_radiation_dose=bool(r["is_personal_radiation_dose"]),
                    included_in_personal_calculations=bool(r["included_in_personal_calculations"]),
                    row_count=int(r["row_count"]),
                    sha256=r["sha256"],
                    limitations=r["limitations"],
                    source_reference=r["source_reference"],
                    quality_flag=r["quality_flag"],
                    created_at=r["created_at"],
                )
                for r in rows
            ]

    @staticmethod
    def _row_to_profile(row: sqlite3.Row) -> ProfileRecord:
        return ProfileRecord(
            id=row["id"],
            profile_uuid=row["profile_uuid"],
            display_name=row["display_name"],
            alias=row["alias"],
            profile_type=row["profile_type"],
            role=row["role"],
            mission=row["mission"],
            namespace=row["namespace"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _row_to_observation(row: sqlite3.Row) -> ObservationRecord:
        flags = json.loads(row["quality_flags"]) if row["quality_flags"] else ["ok"]
        return ObservationRecord(
            id=row["id"],
            profile_id=row["profile_id"],
            namespace=row["namespace"],
            indicator=row["indicator"],
            value=float(row["value"]) if row["value"] is not None else None,
            source_value=float(row["source_value"]) if row["source_value"] is not None else None,
            unit=row["unit"],
            context=row["context"],
            measured_at=row["measured_at"],
            mission_day=int(row["mission_day"]) if row["mission_day"] is not None else None,
            origin_type=row["origin_type"],
            capture_method=row["capture_method"],
            source_reference=row["source_reference"],
            quality_flag=row["quality_flag"],
            quality_flags=flags,
            source_file=row["source_file"],
            source_row=row["source_row"],
            import_batch_id=row["import_batch_id"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _row_to_checkin(row: sqlite3.Row) -> CheckinRecord:
        return CheckinRecord(
            id=row["id"],
            profile_id=row["profile_id"],
            namespace=row["namespace"],
            checkin_date=row["checkin_date"],
            fatigue=int(row["fatigue"]),
            perceived_stress=int(row["perceived_stress"]),
            notes=row["notes"],
            origin_type=row["origin_type"],
            capture_method=row["capture_method"],
            quality_flag=row["quality_flag"],
            created_at=row["created_at"],
        )
