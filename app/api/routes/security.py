from fastapi import APIRouter

from app.models.command import Command
from app.models.device import Device
from app.models.user import User
from app.services.security_engine import SecurityEngine


router = APIRouter(prefix="/security", tags=["security"])

engine = SecurityEngine()


@router.post("/evaluate")
def evaluate_command(
    user: User,
    device: Device,
    command: Command,
) -> dict:
    """Evaluate a command through the GuardianX security engine."""

    return engine.evaluate(
        user=user,
        device=device,
        command=command,
    )