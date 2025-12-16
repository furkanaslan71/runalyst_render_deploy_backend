"""add google auth fields and nullable password

Revision ID: 976136ebd876
Revises: 3dcdceec3f6b
Create Date: 2025-12-16 21:22:09.216335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '976136ebd876'
down_revision: Union[str, Sequence[str], None] = '3dcdceec3f6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1) hashed_password nullable
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=255),
        nullable=True
    )

    # 2) add auth_provider + google_sub
    op.add_column("users", sa.Column("auth_provider", sa.String(length=32), server_default="local", nullable=False))
    op.add_column("users", sa.Column("google_sub", sa.String(length=64), nullable=True))

    # 3) unique constraint for google_sub
    op.create_unique_constraint("uq_users_google_sub", "users", ["google_sub"])


def downgrade():
    op.drop_constraint("uq_users_google_sub", "users", type_="unique")
    op.drop_column("users", "google_sub")
    op.drop_column("users", "auth_provider")

    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=255),
        nullable=False
    )
