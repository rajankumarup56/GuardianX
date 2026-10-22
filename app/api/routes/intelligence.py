from fastapi import APIRouter

from app.models.behaviour import BehaviourProfile
from app.services.intelligence_service import IntelligenceService

router = APIRouter(
    prefix="/intelligence",
    tags=["intelligence"],
)

intelligence_service = IntelligenceService()


@router.post("/analyze")
def analyze_intelligence(
    profile: BehaviourProfile,
    speed: float | None = None,
    altitude: float | None = None,
    temperature: float | None = None,
    trend_increasing: bool = False,
) -> dict:
    """Run GuardianX behaviour, risk, prediction and decision analysis."""

    return intelligence_service.analyze(
        profile=profile,
        speed=speed,
        altitude=altitude,
        temperature=temperature,
        trend_increasing=trend_increasing,
    )