"""Educational content endpoints (/educational-content and /api/education)."""
from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, Path, Query

from artemis_health.routers.dependencies import get_wellness_service
from artemis_health.schemas.education import EducationalContentListResponse, EducationalContentOut
from artemis_health.services.wellness_service import WellnessService

router = APIRouter(tags=["Educational Content"])


@router.get(
    "/educational-content",
    response_model=EducationalContentListResponse,
    summary="Consultar fichas educativas con unidades, limitaciones y referencias bibliográficas",
)
def list_educational_content(
    indicator: Optional[str] = Query(None, description="Filtrar ficha por indicador opcional"),
    service: WellnessService = Depends(get_wellness_service),
) -> EducationalContentListResponse:
    return service.get_educational_content(indicator=indicator)


@router.get(
    "/educational-content/{indicator}",
    response_model=EducationalContentOut,
    summary="Consultar la ficha educativa de un indicador específico",
)
def get_educational_content_by_indicator(
    indicator: str = Path(..., description="Indicador (resting_hr_bpm, sleep_duration_h, fatigue, perceived_stress)"),
    service: WellnessService = Depends(get_wellness_service),
) -> EducationalContentOut:
    res = service.get_educational_content(indicator=indicator)
    return res.items[0]


@router.get(
    "/education",
    response_model=EducationalContentListResponse,
    summary="Alias de catálogo de fichas educativas",
)
def list_education_alias(
    indicator: Optional[str] = Query(None),
    service: WellnessService = Depends(get_wellness_service),
) -> EducationalContentListResponse:
    return service.get_educational_content(indicator=indicator)


@router.get(
    "/education/{indicator}",
    response_model=EducationalContentOut,
    summary="Alias para consultar ficha educativa por indicador",
)
def get_education_alias(
    indicator: str = Path(...),
    service: WellnessService = Depends(get_wellness_service),
) -> EducationalContentOut:
    res = service.get_educational_content(indicator=indicator)
    return res.items[0]
