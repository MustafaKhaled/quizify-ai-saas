# PMP Hybrid RAG — Summary

## Goal
Generate PMP quiz questions that look and feel like real exam questions, without copying them verbatim and without paying for embeddings infrastructure.

## Approach: Light RAG + Exemplar Injection
A two-layer hybrid that grounds Gemini Flash-Lite in PMP material:

1. **Corpus grounding (light RAG)** — Static chapter notes (summaries, formulas, glossary) live in `agents/pmp/knowledge_base/` and are filtered by chapter slug at request time. No embeddings, no vector DB — just in-memory chapter selection.
2. **Exemplar injection** — Up to 3 real past PMP exam questions are pulled from the database (filtered by the user's focus chapters) and injected into the prompt as a "Style Reference" block. The model is instructed to mirror their tone/complexity/distractor pattern but **not copy** them.

Why not pgvector? Filtering by chapter tag is enough for this corpus size. Embeddings would add infra cost and latency without measurable quality gain at this scale.

## Folder Structure
```
backend/agents/
  __init__.py
  pmp/
    __init__.py            # public API — re-exports everything routers need
    config.py              # subject metadata (name, color, icon)
    instructions.md        # stable system prompt (agent identity)
    knowledge_base/
      chapters.py          # 12 chapters: slug, name, summary, content
      glossary.md          # PMP terms reference
      formulas.md          # EVM, comm channels, PERT, EMV, etc.
      retrieval.py         # get_exemplars() + format_exemplars()
      ingest.py            # validates + upserts seed/exam_bank.json into DB
      seed/
        exam_bank.json     # 30 real PMP questions (chapter-tagged)
        README.md          # schema doc + copyright note
```

This pattern is reusable: a future `agents/german/` would mirror the same layout.

## Database
- **New table**: `pmp_exam_questions` (added in migration `b2c3d4e5f6a7`)
- **Idempotency key**: `content_hash = sha256(stem + source)` — avoids BTree row-size limits with long stems and lets us re-run ingest safely after editing the seed.
- **Indexed on**: `content_hash` (unique), `chapter_slug`.

## Request Flow (`POST /predefined/pmp/quiz`)
1. Resolve focus chapters → allowed topic names + filtered corpus text.
2. `get_exemplars(db, focus_chapters, k=3)` → random matching exam questions.
3. `format_exemplars(...)` → renders them as a prompt-friendly text block.
4. Build the prompt: `INSTRUCTIONS` (from `instructions.md`) + per-request directives + `style_block` + `## Corpus`.
5. Call Gemini 2.5 Flash-Lite with `thinking_budget: 0`.
6. Parse JSON, validate question count, persist as a `Quiz`.

## Cost
- Full bank into prompt: ~$0.023/quiz
- 3 exemplars only: ~$0.00008/quiz

## Production Setup
On a fresh environment:
```bash
alembic upgrade head
python -m agents.pmp.knowledge_base.ingest
```
Re-run the ingest whenever `exam_bank.json` changes — `content_hash` upsert keeps it idempotent.

## Files Touched
| File | Purpose |
|------|---------|
| `backend/agents/pmp/__init__.py` | Public API surface |
| `backend/agents/pmp/config.py` | Subject metadata |
| `backend/agents/pmp/instructions.md` | Stable system prompt |
| `backend/agents/pmp/knowledge_base/chapters.py` | 12-chapter corpus |
| `backend/agents/pmp/knowledge_base/glossary.md` | Terms |
| `backend/agents/pmp/knowledge_base/formulas.md` | Formulas |
| `backend/agents/pmp/knowledge_base/retrieval.py` | Exemplar retrieval |
| `backend/agents/pmp/knowledge_base/ingest.py` | Seed → DB upsert |
| `backend/agents/pmp/knowledge_base/seed/exam_bank.json` | 30 real PMP questions |
| `backend/db/models.py` | `PMPExamQuestion` model |
| `backend/alembic/versions/b2c3d4e5f6a7_add_pmp_exam_questions.py` | Migration |
| `backend/db/routers/predefined/predefined_router.py` | Wires retrieval + injection into the quiz prompt |
| `backend/db/routers/recommendations/recommendations_router.py` | Updated to import from `agents.pmp` |
