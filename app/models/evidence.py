from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    evidence_id: str = Field(min_length=3, max_length=100)

    source_type: str = Field(min_length=1, max_length=100)
    source_id: str = Field(min_length=1, max_length=100)

    observation_id: str | None = None
    device_id: str | None = None
    mission_id: str | None = None

    evidence_type: str = Field(min_length=1, max_length=100)
    data: dict[str, Any] = Field(default_factory=dict)

    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    collected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )