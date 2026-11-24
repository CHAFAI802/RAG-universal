"""create ingestions table

Revision ID: 4c9e2b7a1d3f
Revises: e0a6046463d5
Create Date: 2026-11-23 21:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c9e2b7a1d3f"
down_revision: Union[str, Sequence[str], None] = "e0a6046463d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the temporary original-source ingestion registry."""

    op.create_table(
        "ingestions",
        sa.Column("ingestion_id", sa.Uuid(), nullable=False),
        sa.Column("identity_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("source_identifier", sa.String(length=1024), nullable=True),
        sa.Column("document_name", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=255), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "RECEIVING",
                "RECEIVED",
                "FAILED",
                name="ingestion_status",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("storage_path", sa.String(length=1024), nullable=True),
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["identity_id", "user_id"],
            ["users.identity_id", "users.user_id"],
            name="fk_ingestions_identity_user_users",
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "size_bytes >= 0",
            name="ck_ingestions_size_non_negative",
        ),
        sa.PrimaryKeyConstraint("ingestion_id"),
    )

    op.create_index(
        "ix_ingestions_owner_created_at",
        "ingestions",
        ["identity_id", "user_id", "created_at"],
        unique=False,
    )

    op.create_index(
        "ix_ingestions_owner_checksum",
        "ingestions",
        ["identity_id", "user_id", "checksum_sha256"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the ingestion registry."""

    op.drop_index(
        "ix_ingestions_owner_checksum",
        table_name="ingestions",
    )
    op.drop_index(
        "ix_ingestions_owner_created_at",
        table_name="ingestions",
    )
    op.drop_table("ingestions")
