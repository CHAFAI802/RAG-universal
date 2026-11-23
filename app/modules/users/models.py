import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "identity_id",
            "user_id",
            name="uq_users_identity_user_id",
        ),
    )

    def __init__(
        self,
        *,
        identity_id: uuid.UUID,
        user_id: uuid.UUID | None = None,
        status: UserStatus = UserStatus.ACTIVE,
    ):
        self.user_id = user_id if user_id is not None else uuid.uuid4()
        self.identity_id = identity_id
        self.status = status

    user_id: Mapped[uuid.UUID] = mapped_column(
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

    status: Mapped[UserStatus] = mapped_column(
        SQLAlchemyEnum(
            UserStatus,
            native_enum=False,
            name="user_status",
        ),
        nullable=False,
        default=UserStatus.ACTIVE,
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
