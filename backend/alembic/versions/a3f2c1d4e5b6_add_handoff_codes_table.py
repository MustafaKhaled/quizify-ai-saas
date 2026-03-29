"""add handoff_codes table

Revision ID: a3f2c1d4e5b6
Revises: f1000bf5fa50
Create Date: 2026-03-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a3f2c1d4e5b6'
down_revision: Union[str, Sequence[str], None] = 'f1000bf5fa50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'handoff_codes',
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('used', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('code')
    )
    op.create_index(op.f('ix_handoff_codes_code'), 'handoff_codes', ['code'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_handoff_codes_code'), table_name='handoff_codes')
    op.drop_table('handoff_codes')
