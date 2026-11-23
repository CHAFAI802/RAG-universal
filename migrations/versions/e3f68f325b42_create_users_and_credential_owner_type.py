"""create users and credential owner type

Revision ID: e3f68f325b42
Revises: 675ea612d49c
Create Date: 2026-11-23 16:56:30.075375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3f68f325b42'
down_revision: Union[str, Sequence[str], None] = '675ea612d49c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('identity_id', sa.Uuid(), nullable=False),
        sa.Column(
            'status',
            sa.Enum(
                'ACTIVE',
                'DISABLED',
                name='user_status',
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['identity_id'],
            ['identities.identity_id'],
            ondelete='RESTRICT',
        ),
        sa.PrimaryKeyConstraint('user_id'),
    )

    op.add_column(
        'credentials',
        sa.Column(
            'owner_type',
            sa.Enum(
                'IDENTITY_ADMIN',
                'USER',
                name='credential_owner_type',
                native_enum=False,
            ),
            server_default=sa.text("'IDENTITY_ADMIN'"),
            nullable=False,
        ),
    )
    op.add_column(
        'credentials',
        sa.Column('user_id', sa.Uuid(), nullable=True),
    )

    op.create_foreign_key(
        'fk_credentials_user_id_users',
        'credentials',
        'users',
        ['user_id'],
        ['user_id'],
        ondelete='RESTRICT',
    )
    op.create_unique_constraint(
        'uq_credentials_user_id',
        'credentials',
        ['user_id'],
    )
    op.create_check_constraint(
        'ck_credentials_owner_user_consistency',
        'credentials',
        "(owner_type = 'IDENTITY_ADMIN' AND user_id IS NULL) "
        "OR (owner_type = 'USER' AND user_id IS NOT NULL)",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'ck_credentials_owner_user_consistency',
        'credentials',
        type_='check',
    )
    op.drop_constraint(
        'uq_credentials_user_id',
        'credentials',
        type_='unique',
    )
    op.drop_constraint(
        'fk_credentials_user_id_users',
        'credentials',
        type_='foreignkey',
    )
    op.drop_column('credentials', 'user_id')
    op.drop_column('credentials', 'owner_type')
    op.drop_table('users')
