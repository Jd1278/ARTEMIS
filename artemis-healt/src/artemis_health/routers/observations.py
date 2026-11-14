"""Observations registration endpoint (/observations and /api/observations)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from artemis_health.routers.dependencies import get_wellness_service
from artemis_health.schemas.observations import ObservationCreate, ObservationCreateResponse
from artemis_health.services.wellness_service import WellnessService

router = APIRouter(tags=["Observations"])


@router.post(
    "/observations",
    response_model=ObservationCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una observación con validación técnica completa e idempotencia por UUID",
)
def create_observation(
    payload: ObservationCreate,
    response: Response,
    service: WellnessService = Depends(get_wellness_service),
) -> ObservationCreateResponse:
    result, http_status = service.create_observation(payload)
    response.status_code = http_status
    return result
