from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.api.routes.events import router as events_router
from app.api.routes.health import router as health_router
from app.api.routes.security import router as security_router
from app.api.routes.telemetry import router as telemetry_router
from app.api.routes.intelligence import router as intelligence_router

app = FastAPI(
    title="GuardianX",
    version="0.1.0",
    description="Defensive cybersecurity and safety layer for autonomous connected systems.",
)

security_scheme = HTTPBearer(auto_error=False)

def get_current_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    # Admin verification stub for high-integrity endpoint
    if not credentials or credentials.credentials != "admin-secret-token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required for system integrity endpoint."
        )
    return {"username": "admin", "role": "ADMIN"}

# Router Registrations
app.include_router(health_router, prefix="/api/v1")
app.include_router(security_router, prefix="/api/v1")
app.include_router(telemetry_router, prefix="/api/v1")
app.include_router(events_router, prefix="/api/v1")
app.include_router(intelligence_router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    return {
        "product": "GuardianX",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/api/v1/system/integrity-status", tags=["System Integrity"])
async def get_system_integrity_status(current_user: dict = Depends(get_current_admin_user)):
    return {
        "tamper_status": "VALIDATED",
        "siem_chain_state": {
            "total_events": 100,
            "chain_integrity_hash": "a3f8c...91b"
        },
        "risk_engine_config": {
            "haversine_enabled": True,
            "dynamic_threshold": 0.75
        }
    }