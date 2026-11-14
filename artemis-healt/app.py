"""Vercel entrypoint for the existing FastAPI + React application.

Keeps the team's application intact; only deployment imports and the public
demo's write boundary are configured here.
"""
from pathlib import Path
import sys

from fastapi.responses import JSONResponse

source = str(Path(__file__).resolve().parent / "src")
if source not in sys.path:
    sys.path.insert(0, source)

from artemis_health.main import app  # noqa: E402


@app.middleware("http")
async def read_only_deployment(request, call_next):
    """Public deployment is read-only until an authenticated write flow exists."""
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        return JSONResponse(
            status_code=403,
            content={"code": "READ_ONLY_DEMO", "message": "Demo de solo lectura. La observación no fue guardada."},
        )
    return await call_next(request)
