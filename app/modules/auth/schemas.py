from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.identity.models import IdentityStatus, IdentityType


class RegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    display_name: str = Field(min_length=1, max_length=150)

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_.-]{3,50}$",
    )

    password: str = Field(min_length=12, max_length=128)

    @field_validator("display_name")
    @classmethod
    def normalize_display_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Le nom d'affichage est obligatoire.")

        return value


class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    identity_id: UUID
    identity_type: IdentityType
    display_name: str
    username: str
    status: IdentityStatus
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_.-]{3,50}$",
    )
    password: str = Field(min_length=1, max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
