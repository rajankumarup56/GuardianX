from fastapi import FastAPI

from app.api.routes.events import router as events_router
from app.api.routes.health import router as health_router
from app.api.routes.security import router as security_router
from app.api.routes.telemetry import router as telemetry_router


app = FastAPI(
    title="GuardianX",
    version="0.1.0",
    description="Defensive cybersecurity and safety layer for autonomous connected systems.",
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(security_router, prefix="/api/v1")
app.include_router(telemetry_router, prefix="/api/v1")
app.include_router(events_router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    return {
        "product": "GuardianX",
        "status": "running",
        "version": "0.1.0",
    }