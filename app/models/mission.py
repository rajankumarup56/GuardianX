from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Mission(BaseModel):
    mission_id: str = Field(min_length=3, max_length=100)
    mission_name: str = Field(min_length=1, max_length=200)
    mission_type: str = Field(min_length=1, max_length=100)

    owner_id: str = Field(min_length=1, max_length=100)
    device_ids: list[str] = Field(default_factory=list)

    active: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )