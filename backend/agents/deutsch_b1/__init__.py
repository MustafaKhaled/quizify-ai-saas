"""
German Grammar B1 (CEFR) agent package.

Builds on A1 + A2 — assumes the learner already controls all A1 and A2 grammar
(Nominativ, Akkusativ, Dativ, Wechselpräpositionen, Perfekt, Präteritum, Modalverben,
basic Konjunktiv II for politeness, basic Nebensätze, Reflexivverben, basic
Adjektivdeklination, basic Relativsätze, Passiv Präsens). B1 introduces:
Konjunktiv II (irreale Bedingungen / Wünsche), Plusquamperfekt, Passiv in all
tenses + Modalverben, Indirekte Rede (Konjunktiv I basics), full temporal /
final / konzessive / konditional Nebensätze, advanced Relativsätze (was, wo,
relativpronomen mit Präpositionen), full Adjektivdeklination, N-Deklination,
Verben + Präposition mit da-/wo-Komposita, full Genitiv, Partizipien als
Adjektive, subjektive Modalverben, Futur I/II, and Konnektoren-Adverbien.

Like A1 and A2, this subject ships WITHOUT a seed exam bank. Questions are
generated on-demand from the chapter corpus + instructions.md style guide.
"""

from pathlib import Path

from .config import (
    DEUTSCH_B1_SUBJECT_COLOR,
    DEUTSCH_B1_SUBJECT_ICON,
    DEUTSCH_B1_SUBJECT_NAME,
)
from .knowledge_base.chapters import (
    DEUTSCH_B1_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
)

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "DEUTSCH_B1_SUBJECT_NAME",
    "DEUTSCH_B1_SUBJECT_COLOR",
    "DEUTSCH_B1_SUBJECT_ICON",
    "DEUTSCH_B1_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
]
