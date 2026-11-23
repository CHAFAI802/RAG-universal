from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.users.models import UserStatus


class UserCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_.-]{3,50}$",
    )

    password: str = Field(min_length=12, max_length=128)


class UserResponse(BaseModel):
    user_id: UUID
    identity_id: UUID
    username: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime
