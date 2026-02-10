"""add topics to quiz

Revision ID: c36f9ad22cee
Revises: 0f991b56a029
Create Date: 2026-02-10 02:15:32.785393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c36f9ad22cee'
down_revision: Union[str, Sequence[str], None] = '0f991b56a029'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # No-op: topics column already added in 0f991b56a029
    pass

def downgrade() -> None:
    # No-op: topics column removed in 0f991b56a029 downgrade
    pass
