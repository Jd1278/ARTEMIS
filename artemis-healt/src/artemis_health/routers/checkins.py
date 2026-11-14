"""Daily wellness check-in endpoints (/checkins and /api/checkins)."""
from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, Query, Response, status

from artemis_health.routers.dependencies import get_wellness_service
from artemis_health.schemas.checkins import CheckinCreate, CheckinCreateResponse, CheckinOut
from artemis_health.services.wellness_service import WellnessService

router = APIRouter(tags=["Check-ins"])


@router.post(
    "/checkins",
    response_model=CheckinCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un seguimiento diario de bienestar (fatiga 1-5 y estrés percibido 1-5)",
)
def create_checkin(
    payload: CheckinCreate,
    response: Response,
    service: WellnessService = Depends(get_wellness_service),
) -> CheckinCreateResponse:
    result, http_status = service.create_checkin(payload)
    response.status_code = http_status
    return result


@router.get(
    "/checkins",
    response_model=List[CheckinOut],
    summary="Listar seguimientos diarios de bienestar de un perfil ficticio",
)
def list_checkins(
    profile_id: str = Query("demo", description="ID del perfil ficticio"),
    service: WellnessService = Depends(get_wellness_service),
) -> List[CheckinOut]:
    records = service._repo.list_checkins(profile_id)
    return [
        CheckinOut(
            id=r.id,
            profile_id=r.profile_id,
            namespace=r.namespace,
            date=r.checkin_date,
            fatigue=r.fatigue,
            perceived_stress=r.perceived_stress,
            notes=r.notes,
            origin_type=r.origin_type,
            capture_method=r.capture_method,
            quality_flag=r.quality_flag,
            created_at=r.created_at,
        )
        for r in records
    ]
