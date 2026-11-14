"""Profiles, Dashboard, Observations history, Trends, and Baseline Comparison endpoints."""
from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, Path, Query

from artemis_health.routers.dependencies import get_wellness_service
from artemis_health.schemas.observations import (
    BaselineComparisonOut,
    DashboardResponse,
    ObservationListResponse,
    TrendsResponse,
)
from artemis_health.schemas.profiles import ProfileListResponse
from artemis_health.services.wellness_service import WellnessService

router = APIRouter(tags=["Profiles & Dashboard"])


@router.get(
    "/profiles",
    response_model=ProfileListResponse,
    summary="Listar perfiles ficticios de demostración (DEMO / SIMULADO)",
)
def list_profiles(service: WellnessService = Depends(get_wellness_service)) -> ProfileListResponse:
    return service.list_profiles()


@router.get(
    "/profiles/{profile_id}/dashboard",
    response_model=DashboardResponse,
    summary="Resumen de los cuatro indicadores y último registro disponible con línea base personal",
)
def get_profile_dashboard(
    profile_id: str = Path(..., description="ID del perfil ficticio (ej. 'demo' o 'CM-01'..'CM-06')"),
    at: Optional[str] = Query(None, description="Cursor temporal opcional ISO 8601 (YYYY-MM-DD o timestamp UTC)"),
    service: WellnessService = Depends(get_wellness_service),
) -> DashboardResponse:
    return service.get_dashboard(profile_id, at_timestamp=at)


@router.get(
    "/profiles/{profile_id}/observations",
    response_model=ObservationListResponse,
    summary="Consultar historial de observaciones con filtros por indicador y rango de fechas",
)
def get_profile_observations(
    profile_id: str = Path(..., description="ID del perfil ficticio (ej. 'demo' o 'CM-01')"),
    indicator: Optional[str] = Query(None, description="Filtrar por indicador (resting_hr_bpm, sleep_duration_h, fatigue, perceived_stress)"),
    from_date: Optional[str] = Query(None, alias="from", description="Fecha inicial inclusiva (ISO 8601)"),
    start_date: Optional[str] = Query(None, description="Alias opcional de fecha inicial (ISO 8601)"),
    to_date: Optional[str] = Query(None, alias="to", description="Fecha final inclusiva (ISO 8601)"),
    end_date: Optional[str] = Query(None, description="Alias opcional de fecha final (ISO 8601)"),
    origin_type: Optional[str] = Query(None, description="Filtrar por origen (synthetic o user_report)"),
    strict_indicator: bool = Query(False, description="Si es True, no aplica equivalencia de escala entre samn_perelli/fatigue"),
    limit: Optional[int] = Query(None, ge=1, le=5000, description="Límite opcional de registros"),
    service: WellnessService = Depends(get_wellness_service),
) -> ObservationListResponse:
    effective_from = from_date or start_date
    effective_to = to_date or end_date
    return service.list_observations(
        profile_id,
        indicator=indicator,
        from_date=effective_from,
        to_date=effective_to,
        origin_type=origin_type,
        strict_indicator=strict_indicator,
        limit=limit,
    )


@router.get(
    "/profiles/{profile_id}/trends",
    response_model=TrendsResponse,
    summary="Obtener series cronológicas para gráficas sin interpolación de huecos",
)
def get_profile_trends(
    profile_id: str = Path(..., description="ID del perfil ficticio (ej. 'demo' o 'CM-01')"),
    indicator: Optional[str] = Query(None, description="Filtrar serie por un indicador específico"),
    from_date: Optional[str] = Query(None, alias="from", description="Fecha inicial inclusiva (ISO 8601)"),
    start_date: Optional[str] = Query(None, description="Alias opcional de fecha inicial (ISO 8601)"),
    to_date: Optional[str] = Query(None, alias="to", description="Fecha final inclusiva (ISO 8601)"),
    end_date: Optional[str] = Query(None, description="Alias opcional de fecha final (ISO 8601)"),
    origin_type: Optional[str] = Query(None, description="Filtrar por origen (synthetic o user_report)"),
    service: WellnessService = Depends(get_wellness_service),
) -> TrendsResponse:
    effective_from = from_date or start_date
    effective_to = to_date or end_date
    return service.get_trends(
        profile_id,
        indicator=indicator,
        from_date=effective_from,
        to_date=effective_to,
        origin_type=origin_type,
    )


@router.get(
    "/profiles/{profile_id}/comparison",
    response_model=BaselineComparisonOut,
    summary="Comparar el dato actual con la mediana histórica personal compatible (regla baseline_v1)",
)
def get_profile_comparison(
    profile_id: str = Path(..., description="ID del perfil ficticio (ej. 'demo' o 'CM-01')"),
    indicator: str = Query(..., description="Indicador a comparar"),
    at: Optional[str] = Query(None, description="Cursor temporal opcional ISO 8601"),
    origin_type: Optional[str] = Query(None, description="Origen compatible (synthetic o user_report)"),
    service: WellnessService = Depends(get_wellness_service),
) -> BaselineComparisonOut:
    return service.get_comparison(
        profile_id,
        indicator=indicator,
        at_timestamp=at,
        origin_type=origin_type,
    )
