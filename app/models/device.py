from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.models.enums import RiskLevel
from app.models.trust import TrustState


class Device(BaseModel):
    device_id: str = Field(min_length=3, max_length=100)
    device_name: str = Field(min_length=1, max_length=200)
    device_type: str = Field(min_length=1, max_length=50)
    owner_id: str = Field(min_length=1, max_length=100)

    trusted: bool = False
    trust_state: TrustState = TrustState.UNKNOWN

    active: bool = True
    risk_level: RiskLevel = RiskLevel.LOW

    registered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )