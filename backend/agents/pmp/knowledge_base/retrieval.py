"""
Exam-bank retrieval helpers.

Powers exemplar-mode generation: fetch K real PMP questions matching the
user's focus chapters (or any chapter when no focus is set) and format them
as a prompt-injectable style reference. Gemini uses these as style anchors,
not as content to copy.
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from db.models import PMPExamQuestion


def get_exemplars(
    db: Session,
    chapter_slugs: list[str] | None = None,
    k: int = 3,
) -> list[PMPExamQuestion]:
    """Return up to k random exam questions, optionally filtered by chapter_slug."""
    if k <= 0:
        return []
    query = db.query(PMPExamQuestion)
    if chapter_slugs:
        query = query.filter(PMPExamQuestion.chapter_slug.in_(chapter_slugs))
    return query.order_by(func.random()).limit(k).all()


def format_exemplars(exemplars: list[PMPExamQuestion]) -> str:
    """Render exemplars as a prompt-friendly text block. Empty string if none."""
    if not exemplars:
        return ""
    parts = []
    for i, q in enumerate(exemplars, 1):
        opts = "\n".join(f"  {chr(65 + j)}. {o}" for j, o in enumerate(q.options or []))
        parts.append(
            f"Example {i} — chapter: {q.chapter_slug}\n"
            f"Q: {q.stem}\n"
            f"{opts}\n"
            f"Explanation: {q.explanation}"
        )
    return "\n\n".join(parts)
