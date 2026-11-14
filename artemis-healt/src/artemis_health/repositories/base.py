"""Abstract repository interface for ARTEMIS HEALTH persistence."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from artemis_health.models.entities import (
    CheckinRecord,
    EducationalContentRecord,
    IndicatorRecord,
    ObservationRecord,
    ProfileRecord,
    ResearchDatasetRecord,
)


class WellnessRepository(ABC):
    """Persistence contract implemented by SQLite and Supabase/PostgreSQL backends."""

    @abstractmethod
    def check_health(self) -> Tuple[bool, str]:
        """Verify database connectivity and return (is_connected, backend_name)."""

    @abstractmethod
    def list_profiles(self, namespace: str = "demo") -> List[ProfileRecord]:
        """Return all profiles in the requested namespace."""

    @abstractmethod
    def get_profile(self, profile_id: str, namespace: str = "demo") -> Optional[ProfileRecord]:
        """Return a single profile by ID or None if not found."""

    @abstractmethod
    def ensure_demo_profile(self, profile_id: str) -> ProfileRecord:
        """Return existing demo profile or create a fictional demo profile entry."""

    @abstractmethod
    def list_indicators(self) -> List[IndicatorRecord]:
        """Return catalog of wellness indicators."""

    @abstractmethod
    def save_observation(self, observation: ObservationRecord) -> Tuple[ObservationRecord, bool]:
        """Atomically persist an observation.

        Returns (stored_record, is_idempotent_replay).
        Raises ObservationConflictError (409) if UUID exists with different content.
        """

    @abstractmethod
    def get_observation_by_id(self, observation_id: str) -> Optional[ObservationRecord]:
        """Retrieve a single observation by UUID."""

    @abstractmethod
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
        """Return observations ordered chronologically (measured_at ASC, id ASC)."""

    @abstractmethod
    def save_checkin(self, checkin: CheckinRecord) -> Tuple[CheckinRecord, bool]:
        """Atomically persist a daily wellness check-in with UUID idempotency."""

    @abstractmethod
    def list_checkins(self, profile_id: str) -> List[CheckinRecord]:
        """Return check-ins for a profile ordered by date DESC."""

    @abstractmethod
    def list_educational_content(self, indicator: Optional[str] = None) -> List[EducationalContentRecord]:
        """Return educational content cards, optionally filtered by indicator."""

    @abstractmethod
    def list_research_datasets(self) -> List[ResearchDatasetRecord]:
        """Return public/analog research dataset metadata (isolated from demo)."""
