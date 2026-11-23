import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class CredentialType(str, Enum):
    USERNAME_PASSWORD = "USERNAME_PASSWORD"


class CredentialOwnerType(str, Enum):
    """Type de propriétaire du credential, distinct de la méthode d'authentification."""

    IDENTITY_ADMIN = "IDENTITY_ADMIN"
    USER = "USER"


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
        UniqueConstraint(
            "user_id",
            name="uq_credentials_user_id",
        ),
        CheckConstraint(
            "(owner_type = 'IDENTITY_ADMIN' AND user_id IS NULL) "
            "OR (owner_type = 'USER' AND user_id IS NOT NULL)",
            name="ck_credentials_owner_user_consistency",
        ),
        ForeignKeyConstraint(
            ["identity_id", "user_id"],
            ["users.identity_id", "users.user_id"],
            name="fk_credentials_identity_user_users",
            ondelete="RESTRICT",
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

    owner_type: Mapped[CredentialOwnerType] = mapped_column(
        SQLAlchemyEnum(
            CredentialOwnerType,
            native_enum=False,
            name="credential_owner_type",
        ),
        nullable=False,
        default=CredentialOwnerType.IDENTITY_ADMIN,
        server_default=text("'IDENTITY_ADMIN'"),
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        nullable=True,
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
