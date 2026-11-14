"""Schemas for isolated public/analog research dataset metadata."""
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class ResearchDatasetOut(BaseModel):
    id: str
    dataset_key: str
    file_name: str
    title: str
    namespace: str = "research"
    origin_type: str
    capture_method: str
    study_context: str
    is_inflight_measurement: bool
    is_personal_radiation_dose: bool
    included_in_personal_calculations: bool = False
    row_count: int
    sha256: str
    limitations: str
    source_reference: str
    quality_flag: str
    created_at: str


class ResearchDatasetsResponse(BaseModel):
    namespace: str = "research"
    isolation_guaranteed: bool = True
    isolation_notice: str = Field(
        default=(
            "Espacio 'research' estrictamente separado del espacio 'demo'. "
            "Los datasets públicos, análogos terrestres en cama (bedrest) y series ambientales "
            "de radiación nunca se mezclan en los cálculos ni líneas base personales."
        )
    )
    count: int
    datasets: List[ResearchDatasetOut]
