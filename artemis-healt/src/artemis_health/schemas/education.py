"""Schemas for educational content cards."""
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class EducationalContentOut(BaseModel):
    id: str
    indicator: str
    title: str
    description: str
    unit: str
    limitations: str
    bibliographic_reference: str
    created_at: str


class EducationalContentListResponse(BaseModel):
    count: int
    disclaimer: str
    items: List[EducationalContentOut]
