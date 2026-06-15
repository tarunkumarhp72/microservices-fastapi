"""add created_at to users remove follower model

Revision ID: 67f141ac2709
Revises: 254f6ecf6744
Create Date: 2026-06-08 13:18:00.370225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67f141ac2709'
down_revision: Union[str, Sequence[str], None] = '254f6ecf6744'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add created_at column to users table
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Remove created_at column from users table
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###
