"""
German Grammar A1 (CEFR) agent package.

Exposes the stable identity (instructions, subject metadata) and the
knowledge-base helpers (chapter lookup, corpus text). Routers import from this
package via `agents/__init__.py`'s registry.

Note: this subject ships WITHOUT a seed exam bank. Questions are generated
on-demand from the chapter corpus + instructions.md style guide alone.
"""

from pathlib import Path

from .config import (
    DEUTSCH_A1_SUBJECT_COLOR,
    DEUTSCH_A1_SUBJECT_ICON,
    DEUTSCH_A1_SUBJECT_NAME,
)
from .knowledge_base.chapters import (
    DEUTSCH_A1_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
)

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "DEUTSCH_A1_SUBJECT_NAME",
    "DEUTSCH_A1_SUBJECT_COLOR",
    "DEUTSCH_A1_SUBJECT_ICON",
    "DEUTSCH_A1_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
]
