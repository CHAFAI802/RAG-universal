from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.identity.models import IdentityStatus, IdentityType


class HumanIdentityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    display_name: str = Field(
        min_length=1,
        max_length=150,
    )

    @field_validator("display_name")
    @classmethod
    def normalize_display_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Le nom d'affichage est obligatoire.")

        return value


class IdentityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    identity_id: UUID
    identity_type: IdentityType
    display_name: str
    status: IdentityStatus
    created_at: datetime
    updated_at: datetime
