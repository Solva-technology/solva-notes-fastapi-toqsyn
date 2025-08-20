"""Add ON DELETE CASCADE to user_profiles.user_id

Revision ID: f229ec8d1da2
Revises: 6e902c716883
Create Date: 2025-08-20 03:56:27.766988

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f229ec8d1da2'
down_revision: Union[str, Sequence[str], None] = '6e902c716883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop old FK
    op.drop_constraint(
        "user_profiles_user_id_fkey", "user_profiles", type_="foreignkey"
    )
    # Add new FK with ON DELETE CASCADE
    op.create_foreign_key(
        "user_profiles_user_id_fkey",
        "user_profiles", "users",
        ["user_id"], ["id"],
        ondelete="CASCADE"
    )


def downgrade():
    # Revert back to old FK (without cascade)
    op.drop_constraint(
        "user_profiles_user_id_fkey", "user_profiles", type_="foreignkey"
    )
    op.create_foreign_key(
        "user_profiles_user_id_fkey",
        "user_profiles", "users",
        ["user_id"], ["id"]
    )
