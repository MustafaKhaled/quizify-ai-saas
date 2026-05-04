"""
German Grammar A2 (CEFR) agent package.

Builds on A1 — assumes the learner already controls Nominativ, Akkusativ,
Perfekt, Modalverben, etc. — and introduces Dativ, Wechselpräpositionen,
Präteritum, Komparativ/Superlativ, Konjunktiv II (politeness), Nebensätze,
Reflexivverben, Adjektivdeklination, and Relativsätze.

Like A1, this subject ships WITHOUT a seed exam bank. Questions are generated
on-demand from the chapter corpus + instructions.md style guide.
"""

from pathlib import Path

from .config import (
    DEUTSCH_A2_SUBJECT_COLOR,
    DEUTSCH_A2_SUBJECT_ICON,
    DEUTSCH_A2_SUBJECT_NAME,
)
from .knowledge_base.chapters import (
    DEUTSCH_A2_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
)

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "DEUTSCH_A2_SUBJECT_NAME",
    "DEUTSCH_A2_SUBJECT_COLOR",
    "DEUTSCH_A2_SUBJECT_ICON",
    "DEUTSCH_A2_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
]
