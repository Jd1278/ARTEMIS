"""Main FastAPI application entrypoint for ARTEMIS HEALTH."""
from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from artemis_health.core.config import get_settings
from artemis_health.core.constants import NON_CLINICAL_DISCLAIMER
from artemis_health.core.exceptions import register_exception_handlers
from artemis_health.routers import (
    checkins,
    education,
    health,
    indicators,
    observations,
    profiles,
    research,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    application = FastAPI(
        title="ARTEMIS HEALTH",
        description=NON_CLINICAL_DISCLAIMER,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Accept", "X-Request-ID"],
    )

    register_exception_handlers(application)

    # Primary REST routes required by specification
    for mod in (health, indicators, profiles, observations, checkins, education, research):
        application.include_router(mod.router)
        application.include_router(mod.router, prefix="/api")

    dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if dist.is_dir():
        application.mount("/", StaticFiles(directory=dist, html=True), name="frontend")

    return application


app = create_app()
