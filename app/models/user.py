from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.models.enums import UserRole


class User(BaseModel):
    user_id: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=100)

    role: UserRole = UserRole.VIEWER

    active: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )