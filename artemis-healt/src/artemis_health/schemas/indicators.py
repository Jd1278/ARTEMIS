"""Schemas for the wellness indicators catalog."""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class IndicatorOut(BaseModel):
    key: str = Field(..., description="Canonical indicator key.")
    label: str = Field(..., description="Human-readable indicator name.")
    description: str = Field(..., description="Non-clinical explanation of the indicator.")
    unit: str = Field(..., description="Canonical measurement unit.")
    allowed_units: List[str] = Field(..., description="Accepted unit strings for input validation.")
    context: str = Field(..., description="Default measurement context.")
    minimum: Optional[float] = Field(None, description="Minimum valid technical value.")
    maximum: Optional[float] = Field(None, description="Maximum valid technical value.")
    integer_only: bool = Field(default=False, description="Whether only integer values are permitted.")


class IndicatorListResponse(BaseModel):
    count: int
    disclaimer: str
    indicators: List[IndicatorOut]
