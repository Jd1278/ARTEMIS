"""Export all API routers."""
from artemis_health.routers import (
    checkins,
    education,
    health,
    indicators,
    observations,
    profiles,
    research,
)

__all__ = [
    "checkins",
    "education",
    "health",
    "indicators",
    "observations",
    "profiles",
    "research",
]
