"""enforce credential user identity consistency

Revision ID: e0a6046463d5
Revises: e3f68f325b42
Create Date: 2026-11-23 18:32:17.315509

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e0a6046463d5"
down_revision: Union[str, Sequence[str], None] = "e3f68f325b42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enforce that a User and its Credential belong to the same Identity."""

    op.create_unique_constraint(
        "uq_users_identity_user_id",
        "users",
        ["identity_id", "user_id"],
    )

    op.drop_constraint(
        "fk_credentials_user_id_users",
        "credentials",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_credentials_identity_user_users",
        "credentials",
        "users",
        ["identity_id", "user_id"],
        ["identity_id", "user_id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    """Restore the previous single-column foreign key."""

    op.drop_constraint(
        "fk_credentials_identity_user_users",
        "credentials",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_credentials_user_id_users",
        "credentials",
        "users",
        ["user_id"],
        ["user_id"],
        ondelete="RESTRICT",
    )

    op.drop_constraint(
        "uq_users_identity_user_id",
        "users",
        type_="unique",
    )
