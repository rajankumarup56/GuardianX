from typing import Any

from fastapi import APIRouter

from app.services.risk_service import RiskService
from app.services.telemetry_service import TelemetryService


router = APIRouter(prefix="/telemetry", tags=["telemetry"])

telemetry_service = TelemetryService()
risk_service = RiskService()


@router.post("/normalize")
def normalize_telemetry(telemetry: dict[str, Any]) -> dict[str, Any]:
    """Normalize telemetry received from a device or simulator."""
    return telemetry_service.normalize(telemetry)


@router.post("/evaluate")
def evaluate_telemetry(telemetry: dict[str, Any]) -> dict[str, Any]:
    """Evaluate telemetry risk using deterministic security rules."""
    normalized = telemetry_service.normalize(telemetry)

    risk_level, risk_score = risk_service.calculate_telemetry_risk(
        battery=normalized.get("battery"),
        temperature=normalized.get("temperature"),
        speed=normalized.get("speed"),
    )

    return {
        "telemetry": normalized,
        "risk_level": risk_level.value,
        "risk_score": risk_score,
    }