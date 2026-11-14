"""Common API schemas for health status, errors, and shared metadata."""
from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall API health status ('ok' or 'degraded').")
    service: str = Field(default="ARTEMIS HEALTH API")
    version: str = Field(default="1.0.0")
    mode: str = Field(default="demo")
    storage_backend: str = Field(..., description="Active persistence backend ('postgres', 'supabase_rest', 'sqlite').")
    database_connected: bool = Field(..., description="True when database connection check succeeded.")
    database_checked: bool = Field(default=True)
    supabase_configured: bool = Field(..., description="True if remote Supabase credentials are configured.")
    disclaimer: str = Field(..., description="Non-clinical scope notice.")


class ErrorDetail(BaseModel):
    code: str
    message: str
    fields: Dict[str, Any] = Field(default_factory=dict)
    request_id: str


class ErrorResponse(BaseModel):
    status: str = "error"
    code: str
    message: str
    detail: str
    fields: Dict[str, Any] = Field(default_factory=dict)
    request_id: str
    save_status: Optional[str] = None
    error: ErrorDetail
