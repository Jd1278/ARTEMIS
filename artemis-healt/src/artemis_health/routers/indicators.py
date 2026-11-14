"""Indicators catalog endpoints (/indicators and /api/indicators)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from artemis_health.routers.dependencies import get_wellness_service
from artemis_health.schemas.indicators import IndicatorListResponse
from artemis_health.services.wellness_service import WellnessService

router = APIRouter(tags=["Indicators"])


@router.get(
    "/indicators",
    response_model=IndicatorListResponse,
    summary="Catálogo de indicadores de bienestar, unidades y dominios técnicos",
)
def get_indicators(service: WellnessService = Depends(get_wellness_service)) -> IndicatorListResponse:
    return service.list_indicators()
