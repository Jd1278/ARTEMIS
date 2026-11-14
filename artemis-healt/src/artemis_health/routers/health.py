"""Health check endpoints (/health and /api/health)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from artemis_health.routers.dependencies import get_wellness_service
from artemis_health.schemas.common import HealthResponse
from artemis_health.services.wellness_service import WellnessService

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Estado de la API y conexión a base de datos / Supabase",
)
def get_health(service: WellnessService = Depends(get_wellness_service)) -> HealthResponse:
    return service.get_health()
