"""Internal domain dataclasses representing persisted entities and calculation outputs."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProfileRecord:
    id: str
    profile_uuid: str
    display_name: str
    alias: str
    profile_type: str
    role: str
    mission: str
    namespace: str
    created_at: str
    updated_at: str


@dataclass
class IndicatorRecord:
    key: str
    label: str
    description: str
    unit: str
    allowed_units: List[str]
    context: str
    minimum: Optional[float]
    maximum: Optional[float]
    integer_only: bool


@dataclass
class ObservationRecord:
    id: str
    profile_id: str
    namespace: str
    indicator: str
    value: Optional[float]
    source_value: Optional[float]
    unit: str
    context: str
    measured_at: str
    mission_day: Optional[int]
    origin_type: str
    capture_method: str
    source_reference: Optional[str]
    quality_flag: str
    quality_flags: List[str] = field(default_factory=lambda: ["ok"])
    source_file: Optional[str] = None
    source_row: Optional[int] = None
    import_batch_id: Optional[str] = None
    created_at: str = ""


@dataclass
class CheckinRecord:
    id: str
    profile_id: str
    namespace: str
    checkin_date: str
    fatigue: int
    perceived_stress: int
    notes: Optional[str]
    origin_type: str
    capture_method: str
    quality_flag: str
    created_at: str


@dataclass
class EducationalContentRecord:
    id: str
    indicator: str
    title: str
    description: str
    unit: str
    limitations: str
    bibliographic_reference: str
    created_at: str


@dataclass
class ResearchDatasetRecord:
    id: str
    dataset_key: str
    file_name: str
    title: str
    namespace: str
    origin_type: str
    capture_method: str
    study_context: str
    is_inflight_measurement: bool
    is_personal_radiation_dose: bool
    included_in_personal_calculations: bool
    row_count: int
    sha256: str
    limitations: str
    source_reference: str
    quality_flag: str
    created_at: str


@dataclass
class BaselineComparison:
    indicator: str
    unit: str
    context: str
    origin_type: str
    rule_version: str
    reference_timestamp: str
    current_value: Optional[float]
    baseline_median: Optional[float]
    difference: Optional[float]
    sufficient_history: bool
    status: str
    days_used: int
    minimum_days_required: int
    window_days: int
    max_days: int
    period_start: Optional[str]
    period_end: Optional[str]
    descriptive_notice: str
    reference_observation_ids: List[str] = field(default_factory=list)
