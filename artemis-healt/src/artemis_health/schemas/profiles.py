"""Schemas for fictional astronaut profiles."""
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class ProfileOut(BaseModel):
    id: str = Field(..., description="Profile identifier (e.g. 'demo', 'CM-01').")
    uuid: str = Field(..., description="Deterministic UUID of the fictional profile.")
    alias: str = Field(..., description="Fictional display alias (explicitly marked DEMO/SIMULADO).")
    display_name: str = Field(..., description="Display name for UI selectors.")
    profile_type: str = Field(default="fictional_astronaut")
    role: str = Field(default="Crew Member")
    mission: str = Field(default="SIM-ISS-180")
    namespace: str = Field(default="demo")
    is_simulated: bool = Field(default=True)
    created_at: str
    updated_at: str


class ProfileListResponse(BaseModel):
    namespace: str = "demo"
    data_label: str = "SIMULADO"
    count: int
    profiles: List[ProfileOut]
