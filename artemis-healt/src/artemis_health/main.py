"""Main FastAPI application entrypoint for ARTEMIS HEALTH."""
from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

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


class SPAStaticFiles(StaticFiles):
    """Serve the React build and fall back to index.html for client-side routes (/history, /log...).

    API routers are registered before this mount, so /api/* and the backend's own paths keep priority;
    only unknown paths that are not files in frontend/dist reach the fallback.
    """

    async def get_response(self, path: str, scope):  # type: ignore[override]
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            normalized = path.replace("\\", "/")  # StaticFiles uses OS separators (backslashes on Windows)
            if exc.status_code != 404 or normalized.startswith(("api/", "assets/")) or "." in normalized.rsplit("/", 1)[-1]:
                raise
            return await super().get_response("index.html", scope)


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
        application.mount("/", SPAStaticFiles(directory=dist, html=True), name="frontend")

    return application


app = create_app()
