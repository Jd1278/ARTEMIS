"""FastAPI dependencies for injecting WellnessService and WellnessRepository."""
from __future__ import annotations

from fastapi import Depends

from artemis_health.repositories.base import WellnessRepository
from artemis_health.repositories.factory import get_repository
from artemis_health.services.wellness_service import WellnessService


def get_wellness_service(repo: WellnessRepository = Depends(get_repository)) -> WellnessService:
    return WellnessService(repository=repo)
