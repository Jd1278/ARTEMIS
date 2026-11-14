from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI(title="ARTEMIS HEALTH")
@app.get("/api/health")
def health():
    return {"status": "scaffold", "database_checked": False}
dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if dist.is_dir():
    app.mount("/", StaticFiles(directory=dist, html=True), name="frontend")
