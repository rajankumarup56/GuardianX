from pydantic import BaseModel, Field

from app.models.enums import RiskLevel


class RiskContext(BaseModel):
    security_risk: RiskLevel = RiskLevel.LOW
    safety_risk: RiskLevel = RiskLevel.LOW

    security_score: int = Field(default=0, ge=0, le=100)
    safety_score: int = Field(default=0, ge=0, le=100)

    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    reasons: list[str] = Field(default_factory=list)