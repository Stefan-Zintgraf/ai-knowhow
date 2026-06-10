---
skill: triage-idea
source_docs:
  - gr/gr_idea.md
  - guardrails.md
  - phases.md
source_docs_hash: 340c940
generated: 2026-05-26
---

# Test Plan: triage-idea

## Automated Tests

### 000 — Trivial brief scores all-low, proposes direct-edit

- **Category:** happy-path
- **Requirements:** Idea8 ([gr_idea.md](gr/gr_idea.md)), Idea4 ([gr_idea.md](gr/gr_idea.md)), 3.29 ([guardrails.md](guardrails.md))
- **Input:** `input000.md`
- **Output:** `output000.md`
- [ ] Pass

### 001 — Medium brief with partial test coverage, proposes mini

- **Category:** happy-path
- **Requirements:** Idea8 ([gr_idea.md](gr/gr_idea.md)), Idea4 ([gr_idea.md](gr/gr_idea.md)), 3.29 ([guardrails.md](guardrails.md))
- **Input:** `input001.md`
- **Output:** `output001.md`
- [ ] Pass

### 002 — Complex auth replacement scores high on multiple axes, proposes full

- **Category:** happy-path
- **Requirements:** Idea8 ([gr_idea.md](gr/gr_idea.md)), Idea4 ([gr_idea.md](gr/gr_idea.md)), 3.29 ([guardrails.md](guardrails.md))
- **Input:** `input002.md`
- **Output:** `output002.md`
- [ ] Pass

### 003 — Tripwire surface (public API) forces full despite low axis scores

- **Category:** edge
- **Requirements:** Idea8 ([gr_idea.md](gr/gr_idea.md)), 3.29 ([guardrails.md](guardrails.md)), 3.37 ([guardrails.md](guardrails.md)), Idea4 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input003.md`
- **Output:** `output003.md`
- [ ] Pass

### 004 — --remode mid-WI upgrade from mini to full on concurrency tripwire

- **Category:** edge
- **Requirements:** Idea11 ([gr_idea.md](gr/gr_idea.md)), 3.37 ([guardrails.md](guardrails.md)), 3.16 ([guardrails.md](guardrails.md))
- **Input:** `input004.md`
- **Output:** `output004.md`
- [ ] Pass

### 005 — Exploration budget exceeded triggers auto-recommend mini

- **Category:** edge
- **Requirements:** Idea10 ([gr_idea.md](gr/gr_idea.md)), Idea8 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input005.md`
- **Output:** `output005.md`
- [ ] Pass

## Manual Tests

### M000 — Real HITL mode confirmation with human override

- **Category:** happy-path
- **Requirements:** Idea4 ([gr_idea.md](gr/gr_idea.md)), Idea8 ([gr_idea.md](gr/gr_idea.md)), 3.16 ([guardrails.md](guardrails.md))
- **Why manual:** Requires real HITL interaction during skill execution — human must override the agent's proposed mode to verify the skill accepts the override gracefully
- **Test procedure:**
  1. Run `/triage-idea` with a medium-complexity brief (e.g., input001.md content)
  2. Agent proposes `mini` mode
  3. Human overrides to `direct-edit` (downgrade) or `full` (upgrade)
  4. Observe that the skill accepts the override without resistance and adjusts its chain output accordingly
- **Pass criteria:** Skill accepts the human override, updates the mode proposal, and does not re-argue or silently revert to its original recommendation
- [ ] Pass

### M001 — Issue dedupe and creation flow via gh CLI

- **Category:** happy-path
- **Requirements:** Idea9 ([gr_idea.md](gr/gr_idea.md))
- **Why manual:** Requires real GitHub repository state and `gh` CLI interaction — dedupe search results depend on existing issues, and issue creation has external side effects
- **Test procedure:**
  1. Run `/triage-idea` with a brief that matches an existing open issue's title keywords
  2. Observe the dedupe search (`gh issue list --state open --search`)
  3. Verify top 3-5 matches are displayed
  4. Pick "new" — verify issue is created with correct title, body, and `mode:*` label
  5. Verify `plan/<N>_<slug>/` folder is created for mini/full mode (or not created for direct-edit)
- **Pass criteria:** Dedupe search runs before create; human sees matches; new issue gets correct label; folder creation matches mode
- [ ] Pass
