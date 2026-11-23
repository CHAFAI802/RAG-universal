import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    Index,
    String,
    func,
    text,
)
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class CredentialType(str, Enum):
    USERNAME_PASSWORD = "USERNAME_PASSWORD"


class CredentialStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class Credential(Base):
    __tablename__ = "credentials"

    __table_args__ = (
        CheckConstraint(
            "username = lower(username)",
            name="ck_credentials_username_lowercase",
        ),
        Index(
            "uq_credentials_username_ci",
            func.lower(text("username")),
            unique=True,
        ),
    )

    credential_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    identity_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "identities.identity_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    credential_type: Mapped[CredentialType] = mapped_column(
        SQLAlchemyEnum(
            CredentialType,
            native_enum=False,
            name="credential_type",
        ),
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    status: Mapped[CredentialStatus] = mapped_column(
        SQLAlchemyEnum(
            CredentialStatus,
            native_enum=False,
            name="credential_status",
        ),
        nullable=False,
        default=CredentialStatus.ACTIVE,
        server_default=text("'ACTIVE'"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
