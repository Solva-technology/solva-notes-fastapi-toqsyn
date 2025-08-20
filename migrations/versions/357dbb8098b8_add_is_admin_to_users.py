"""Add is_admin to users

Revision ID: 357dbb8098b8
Revises: f229ec8d1da2
Create Date: 2025-08-20 04:04:36.903170

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '357dbb8098b8'
down_revision: Union[str, Sequence[str], None] = 'f229ec8d1da2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false"))
    )


def downgrade():
    op.drop_column("users", "is_admin")
