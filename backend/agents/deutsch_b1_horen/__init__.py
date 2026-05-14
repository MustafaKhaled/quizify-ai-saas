"""
German B1 Hören (Listening) agent package.

Models the four Teile of the Goethe-Zertifikat B1 / telc B1 / ÖSD B1 listening
section. Unlike the grammar tracks, this agent's "questions" are audio scripts
plus comprehension items — a TTS layer renders the script to MP3 before
serving to the candidate. See agents/_tools/horen_script_generator.py for
offline script generation; the audio pipeline is Phase 1b.
"""

from pathlib import Path

from .config import (
    DEUTSCH_B1_HOREN_SUBJECT_COLOR,
    DEUTSCH_B1_HOREN_SUBJECT_ICON,
    DEUTSCH_B1_HOREN_SUBJECT_NAME,
)
from .knowledge_base.chapters import (
    DEUTSCH_B1_HOREN_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
    topics_for_teil,
)

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "DEUTSCH_B1_HOREN_SUBJECT_NAME",
    "DEUTSCH_B1_HOREN_SUBJECT_COLOR",
    "DEUTSCH_B1_HOREN_SUBJECT_ICON",
    "DEUTSCH_B1_HOREN_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
    "topics_for_teil",
]
