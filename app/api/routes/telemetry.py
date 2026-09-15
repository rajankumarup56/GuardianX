from typing import Any

from fastapi import APIRouter

from app.services.telemetry_service import TelemetryService


router = APIRouter(prefix="/telemetry", tags=["telemetry"])
telemetry_service = TelemetryService()


@router.post("/normalize")
def normalize_telemetry(telemetry: dict[str, Any]) -> dict[str, Any]:
    """Normalize telemetry received from a device or simulator."""
    return telemetry_service.normalize(telemetry)