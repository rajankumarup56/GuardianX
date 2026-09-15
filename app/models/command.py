from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class Command(BaseModel):
    command_id: str = Field(min_length=3, max_length=100)
    device_id: str = Field(min_length=3, max_length=100)
    issued_by: str = Field(min_length=3, max_length=100)

    command_type: str = Field(min_length=1, max_length=100)
    parameters: dict[str, Any] = Field(default_factory=dict)

    issued_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )