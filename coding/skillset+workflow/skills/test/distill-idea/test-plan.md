---
skill: distill-idea
source_docs:
  - gr/gr_idea.md
  - guardrails.md
  - phases.md
source_docs_hash: 340c940
generated: 2026-05-26
---

# Test Plan: distill-idea

## Automated Tests

### 000 — Happy path: full brief distilled into 3–6 goals

- **Category:** happy-path
- **Requirements:** Idea1 ([gr_idea.md](gr/gr_idea.md)), Idea2 ([gr_idea.md](gr/gr_idea.md)), Idea5 ([gr_idea.md](gr/gr_idea.md)), Idea6 ([gr_idea.md](gr/gr_idea.md)), Idea7 ([gr_idea.md](gr/gr_idea.md)), 3.32 ([guardrails.md](guardrails.md))
- **Input:** `input000.md`
- **Output:** `output000.md`
- [ ] Pass

### 001 — Detail stripping: implementation details removed, non-goal preserved

- **Category:** detail-stripping
- **Requirements:** Idea1 ([gr_idea.md](gr/gr_idea.md)), Idea2 ([gr_idea.md](gr/gr_idea.md)), Idea3 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input001.md`
- **Output:** `output001.md`
- [ ] Pass

### 002 — Heuristic shortcut: pre-shaped goals trigger 3.29 collapse

- **Category:** heuristic-shortcut
- **Requirements:** 3.29 ([guardrails.md](guardrails.md)), Idea1 ([gr_idea.md](gr/gr_idea.md)), Idea2 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input002.md`
- **Output:** `output002.md`
- [ ] Pass

### 003 — Rejection: trivially narrow brief produces not_produced

- **Category:** rejection
- **Requirements:** Idea1 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input003.md`
- **Output:** `output003.md`
- [ ] Pass

### 004 — Sub-brief concept sharpening: vague notion triggers Idea12

- **Category:** edge
- **Requirements:** Idea12 ([gr_idea.md](gr/gr_idea.md)), Idea1 ([gr_idea.md](gr/gr_idea.md)), Idea2 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input004.md`
- **Output:** `output004.md`
- [ ] Pass

### 005 — Upper boundary: 8+ concerns consolidated to ≤6 goals

- **Category:** happy-path
- **Requirements:** Idea1 ([gr_idea.md](gr/gr_idea.md)), Idea2 ([gr_idea.md](gr/gr_idea.md)), Idea5 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input005.md`
- **Output:** `output005.md`
- [ ] Pass

### 006 — File persistence: idea.md + status_idea.md written to plan/\<WI\>/

- **Category:** happy-path
- **Requirements:** Idea7 ([gr_idea.md](gr/gr_idea.md))
- **Setup:** create directory `plan/999_test-slug/`
- **Teardown:** delete directory `plan/999_test-slug/`
- **Input:** `input006.md`
- **Output:** `output006.md`
- [ ] Pass

### 007 — HITL gate: mocked edits/rejections reflected in output

- **Category:** edge
- **Requirements:** Idea4 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input007.md`
- **Output:** `output007.md`
- [ ] Pass

### 008 — Exploration budget: ≤5 file reads during triage exploration

- **Category:** edge
- **Requirements:** Idea10 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input008.md`
- **Output:** `output008.md`
- [ ] Pass

### 009 — Artifact retirement: plan/\<WI\>/ cleaned up at WI close

- **Category:** edge
- **Requirements:** 3.33 ([guardrails.md](guardrails.md)), Idea7 ([gr_idea.md](gr/gr_idea.md))
- **Setup:** create directory `plan/999_test-slug/` with dummy `idea.md` and `status_idea.md`
- **Teardown:** delete directory `plan/999_test-slug/` (if still present)
- **Input:** `input009.md`
- **Output:** `output009.md`
- [ ] Pass

## Manual Tests

No manual tests required for `distill-idea` — triage responsibilities (Idea8, Idea9, Idea11, 3.29, 3.37) are owned by `/triage-idea` (A13) and covered in `skills/test/triage-idea/test-plan.md`.

