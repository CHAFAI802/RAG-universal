from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class IngestionResponse(BaseModel):
    ingestion_id: UUID
    identity_id: UUID
    user_id: UUID
    source_type: str
    source_identifier: str | None
    document_name: str
    content_type: str | None
    size_bytes: int
    checksum_sha256: str | None
    status: str
    temporary_location: str | None
    error_code: str | None
    error_message: str | None
    received_at: datetime | None
    created_at: datetime
    updated_at: datetime


class CreateIngestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_name: str = Field(min_length=1, max_length=255)
    source_type: str = Field(
        default="UPLOAD",
        min_length=1,
        max_length=50,
        pattern=r"^[A-Z][A-Z0-9_]*$",
    )
    source_identifier: str | None = Field(default=None, max_length=1024)
