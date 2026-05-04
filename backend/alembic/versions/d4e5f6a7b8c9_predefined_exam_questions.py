"""generic predefined_exam_questions table; migrate pmp_exam_questions data

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-05-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the generic table.
    op.create_table(
        'predefined_exam_questions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('content_hash', sa.String(length=64), nullable=False),
        sa.Column('subject_slug', sa.String(length=64), nullable=False),
        sa.Column('chapter_slug', sa.String(length=64), nullable=False),
        sa.Column('stem', sa.String(), nullable=False),
        sa.Column('quiz_type', sa.String(length=32), nullable=False, server_default='single_choice'),
        sa.Column('options', sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column('correct_index', sa.Integer(), nullable=True),
        sa.Column('correct_option_indices', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('explanation', sa.String(), nullable=False),
        sa.Column('source', sa.String(length=255), nullable=False),
        sa.Column('difficulty', sa.String(length=16), nullable=False, server_default='medium'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_predefined_exam_questions_content_hash', 'predefined_exam_questions', ['content_hash'], unique=True)
    op.create_index('ix_predefined_exam_questions_subject_slug', 'predefined_exam_questions', ['subject_slug'])
    op.create_index('ix_predefined_exam_questions_chapter_slug', 'predefined_exam_questions', ['chapter_slug'])

    # 2. Move existing PMP rows over, tagging them with subject_slug='pmp'.
    #    Wrapped in a guard so the migration is safe on environments where
    #    pmp_exam_questions never existed (fresh DB).
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_name = 'pmp_exam_questions'
            ) THEN
                INSERT INTO predefined_exam_questions (
                    id, content_hash, subject_slug, chapter_slug, stem, quiz_type,
                    options, correct_index, correct_option_indices, explanation,
                    source, difficulty, created_at
                )
                SELECT
                    id, content_hash, 'pmp', chapter_slug, stem, quiz_type,
                    options, correct_index, correct_option_indices, explanation,
                    source, difficulty, created_at
                FROM pmp_exam_questions
                ON CONFLICT (content_hash) DO NOTHING;

                DROP TABLE pmp_exam_questions;
            END IF;
        END $$;
        """
    )


def downgrade() -> None:
    # Recreate pmp_exam_questions and copy 'pmp'-tagged rows back into it.
    op.create_table(
        'pmp_exam_questions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('content_hash', sa.String(length=64), nullable=False),
        sa.Column('chapter_slug', sa.String(length=64), nullable=False),
        sa.Column('stem', sa.String(), nullable=False),
        sa.Column('quiz_type', sa.String(length=32), nullable=False, server_default='single_choice'),
        sa.Column('options', sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column('correct_index', sa.Integer(), nullable=True),
        sa.Column('correct_option_indices', sa.dialects.postgresql.JSONB(), nullable=True),
        sa.Column('explanation', sa.String(), nullable=False),
        sa.Column('source', sa.String(length=255), nullable=False),
        sa.Column('difficulty', sa.String(length=16), nullable=False, server_default='medium'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_pmp_exam_questions_content_hash', 'pmp_exam_questions', ['content_hash'], unique=True)
    op.create_index('ix_pmp_exam_questions_chapter_slug', 'pmp_exam_questions', ['chapter_slug'])

    op.execute(
        """
        INSERT INTO pmp_exam_questions (
            id, content_hash, chapter_slug, stem, quiz_type,
            options, correct_index, correct_option_indices, explanation,
            source, difficulty, created_at
        )
        SELECT
            id, content_hash, chapter_slug, stem, quiz_type,
            options, correct_index, correct_option_indices, explanation,
            source, difficulty, created_at
        FROM predefined_exam_questions
        WHERE subject_slug = 'pmp'
        ON CONFLICT (content_hash) DO NOTHING;
        """
    )

    op.drop_index('ix_predefined_exam_questions_chapter_slug', table_name='predefined_exam_questions')
    op.drop_index('ix_predefined_exam_questions_subject_slug', table_name='predefined_exam_questions')
    op.drop_index('ix_predefined_exam_questions_content_hash', table_name='predefined_exam_questions')
    op.drop_table('predefined_exam_questions')
