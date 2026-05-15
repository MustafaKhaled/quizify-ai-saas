"""add unsubscribed_at to users

Revision ID: e7d8c9b0a1f2
Revises: d4e5f6a7b8c9
Create Date: 2026-05-15 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7d8c9b0a1f2'
down_revision: Union[str, Sequence[str], None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema — add unsubscribed_at gate for non-transactional email."""
    op.add_column('users', sa.Column('unsubscribed_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'unsubscribed_at')
