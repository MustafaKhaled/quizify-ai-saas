"""
PMP agent package.

Exposes the stable "identity" of the PMP quiz generator (instructions,
subject metadata) and the knowledge-base helpers (chapter lookup, corpus
text). Routers import from this package; nothing imports from internal
submodules directly.
"""

from pathlib import Path

from .config import PMP_SUBJECT_COLOR, PMP_SUBJECT_ICON, PMP_SUBJECT_NAME
from .knowledge_base.chapters import (
    PMP_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
)
from .knowledge_base.retrieval import format_exemplars, get_exemplars

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "PMP_SUBJECT_NAME",
    "PMP_SUBJECT_COLOR",
    "PMP_SUBJECT_ICON",
    "PMP_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
    "get_exemplars",
    "format_exemplars",
]
