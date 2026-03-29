"""add oauth_states table

Revision ID: b4e3d2c1f0a9
Revises: a3f2c1d4e5b6
Create Date: 2026-03-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b4e3d2c1f0a9'
down_revision: Union[str, Sequence[str], None] = 'a3f2c1d4e5b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'oauth_states',
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('redirect_uri', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('state')
    )
    op.create_index(op.f('ix_oauth_states_state'), 'oauth_states', ['state'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_oauth_states_state'), table_name='oauth_states')
    op.drop_table('oauth_states')
