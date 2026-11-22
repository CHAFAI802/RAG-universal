import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, String, func
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class IdentityType(str, Enum):
    HUMAN = "HUMAN"
    SERVICE = "SERVICE"


class IdentityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class Identity(Base):
    __tablename__ = "identities"

    def __init__(
        self,
        *,
        identity_type: IdentityType,
        display_name: str,
        identity_id: uuid.UUID | None = None,
        status: IdentityStatus = IdentityStatus.ACTIVE,
    ):
        self.identity_id = identity_id if identity_id is not None else uuid.uuid4()
        self.identity_type = identity_type
        self.display_name = display_name
        self.status = status

    identity_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    identity_type: Mapped[IdentityType] = mapped_column(
        SQLAlchemyEnum(
            IdentityType,
            native_enum=False,
            name="identity_type",
        ),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    status: Mapped[IdentityStatus] = mapped_column(
        SQLAlchemyEnum(
            IdentityStatus,
            native_enum=False,
            name="identity_status",
        ),
        nullable=False,
        default=IdentityStatus.ACTIVE,
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
