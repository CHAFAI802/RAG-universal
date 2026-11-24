import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum as SQLAlchemyEnum,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class IngestionStatus(str, Enum):
    PENDING = "PENDING"
    RECEIVING = "RECEIVING"
    RECEIVED = "RECEIVED"
    FAILED = "FAILED"


class Ingestion(Base):
    """Réception d'une source originale, avant toute phase de nettoyage.

    La source originale est conservée dans le stockage temporaire. Ce module
    ne supprime jamais une source reçue : la suppression relève du futur
    processus de nettoyage, une fois le contenu durable enregistré.
    """

    __tablename__ = "ingestions"

    __table_args__ = (
        ForeignKeyConstraint(
            ["identity_id", "user_id"],
            ["users.identity_id", "users.user_id"],
            name="fk_ingestions_identity_user_users",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "size_bytes >= 0",
            name="ck_ingestions_size_non_negative",
        ),
        Index(
            "ix_ingestions_owner_created_at",
            "identity_id",
            "user_id",
            "created_at",
        ),
        Index(
            "ix_ingestions_owner_checksum",
            "identity_id",
            "user_id",
            "checksum_sha256",
        ),
    )

    def __init__(
        self,
        *,
        identity_id: uuid.UUID,
        user_id: uuid.UUID,
        source_type: str,
        document_name: str,
        source_identifier: str | None = None,
        ingestion_id: uuid.UUID | None = None,
        status: IngestionStatus = IngestionStatus.PENDING,
    ):
        self.ingestion_id = (
            ingestion_id if ingestion_id is not None else uuid.uuid4()
        )
        self.identity_id = identity_id
        self.user_id = user_id
        self.source_type = source_type
        self.source_identifier = source_identifier
        self.document_name = document_name
        self.size_bytes = 0
        self.status = status

    ingestion_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    identity_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
    )

    # Type de source extensible : UPLOAD, LOCAL_FILE, LOCAL_FOLDER, WEB,
    # TEXT, STRUCTURED, CONNECTOR... Une chaîne permet d'ajouter des
    # connecteurs sans migration de schéma.
    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_identifier: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True,
    )

    document_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Type MIME détecté côté serveur, jamais celui déclaré par le client.
    content_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
    )

    checksum_sha256: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    status: Mapped[IngestionStatus] = mapped_column(
        SQLAlchemyEnum(
            IngestionStatus,
            native_enum=False,
            name="ingestion_status",
        ),
        nullable=False,
        default=IngestionStatus.PENDING,
    )

    # Emplacement absolu interne ; l'API n'expose qu'un chemin relatif.
    storage_path: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True,
    )

    error_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
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
