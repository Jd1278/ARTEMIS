"""Research datasets metadata endpoints (/research/datasets and /api/research/datasets)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from artemis_health.routers.dependencies import get_wellness_service
from artemis_health.schemas.research import ResearchDatasetsResponse
from artemis_health.services.wellness_service import WellnessService

router = APIRouter(tags=["Research Datasets (Isolated Space)"])


@router.get(
    "/research/datasets",
    response_model=ResearchDatasetsResponse,
    summary="Consultar metadatos y limitaciones de datasets científicos públicos/análogos (aislados de demo)",
)
def get_research_datasets(
    service: WellnessService = Depends(get_wellness_service),
) -> ResearchDatasetsResponse:
    return service.get_research_datasets()
