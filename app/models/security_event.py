from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import RiskLevel, SecurityDecision


class SecurityEvent(BaseModel):
    event_id: str = Field(min_length=3, max_length=100)
    device_id: str = Field(min_length=3, max_length=100)

    event_type: str = Field(min_length=1, max_length=100)
    source: str = Field(min_length=1, max_length=100)

    risk_level: RiskLevel = RiskLevel.LOW
    decision: SecurityDecision = SecurityDecision.ALLOW

    message: str = Field(min_length=1, max_length=1000)
    details: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )