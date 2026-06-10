---
skill: phase
source_docs:
  - coding_plan.md
  - phases.md
  - guardrails.md
  - gr/gr_idea.md
source_docs_hash: 7b500a52
generated: 2026-05-28
---

# Test Plan: phase

## Automated Tests

### 000 — enter aln with clean mini-mode state succeeds and updates phase_status.md

- **Category:** happy-path
- **Requirements:** PTM1 ([coding_plan.md](coding_plan.md)), PTM2 ([coding_plan.md](coding_plan.md)), PTM3 ([coding_plan.md](coding_plan.md)), PTM5 ([coding_plan.md](coding_plan.md)), PTM7 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md))
- **Input:** `input000.md`
- **Output:** `output000.md`
- [x] Pass

### 001 — exit ide with idea.md present and HITL ack appends history row

- **Category:** happy-path
- **Requirements:** PTM1 ([coding_plan.md](coding_plan.md)), PTM2 ([coding_plan.md](coding_plan.md)), PTM8 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md))
- **Input:** `input001.md`
- **Output:** `output001.md`
- [x] Pass

### 002 — status with plan/ACTIVE=<none> reports no active WI

- **Category:** happy-path
- **Requirements:** PTM6 ([coding_plan.md](coding_plan.md)), PTM9 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md))
- **Input:** `input002.md`
- **Output:** `output002.md`
- [x] Pass

### 003 — status with needs_research=true computes next_phase=res at read time

- **Category:** edge
- **Requirements:** PTM4 ([coding_plan.md](coding_plan.md)), PTM9 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md)), PH4.2 ([phases.md](phases.md)), PH4.3 ([phases.md](phases.md))
- **Input:** `input003.md`
- **Output:** `output003.md`
- [x] Pass

### 004 — status with tripwire_halt=true surfaces halt and blocks forward progress

- **Category:** edge
- **Requirements:** G3.37 ([guardrails.md](guardrails.md)), PTM9 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md))
- **Input:** `input004.md`
- **Output:** `output004.md`
- [x] Pass

### 005 — enter aln rejected because direct-edit mode has no aln phase

- **Category:** rejection
- **Requirements:** PTM7 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md)), PH4.4 ([phases.md](phases.md)), Idea8 ([gr_idea.md](gr/gr_idea.md))
- **Input:** `input005.md`
- **Output:** `output005.md`
- [x] Pass

### 006 — exit ide rejected because required artifact idea.md is missing

- **Category:** rejection
- **Requirements:** PTM8 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md))
- **Input:** `input006.md`
- **Output:** `output006.md`
- [x] Pass

### 007 — resolve-tripwire clears halt, records reason in history and GH issue

- **Category:** happy-path
- **Requirements:** G3.37 ([guardrails.md](guardrails.md)), PTM1 ([coding_plan.md](coding_plan.md)), PTM2 ([coding_plan.md](coding_plan.md))
- **Input:** `input007.md`
- **Output:** `output007.md`
- [x] Pass

### 008 — enter rejected because tripwire_halt is true

- **Category:** rejection
- **Requirements:** PTM7 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md)), G3.37 ([guardrails.md](guardrails.md))
- **Input:** `input008.md`
- **Output:** `output008.md`
- [x] Pass

### 009 — close from terminal phase clears plan/ACTIVE and appends close history row

- **Category:** happy-path
- **Requirements:** PTM1 ([coding_plan.md](coding_plan.md)), PTM2 ([coding_plan.md](coding_plan.md)), PTM5 ([coding_plan.md](coding_plan.md)), PTM-close ([coding_plan.md](coding_plan.md) L133–L134)
- **Input:** `input009.md`
- **Output:** `output009.md`
- [x] Pass

### 010 — close rejected because current_phase is not the terminal phase for mode

- **Category:** rejection
- **Requirements:** PTM-close terminal-phase guard ([coding_plan.md](coding_plan.md) L133–L134), PTM7 ([coding_plan.md](coding_plan.md) / [phases.md](phases.md)), PTM1 ([coding_plan.md](coding_plan.md))
- **Input:** `input010.md`
- **Output:** `output010.md`
- [x] Pass

### 011 — close rejected because phase_status is in-progress, not exited

- **Category:** rejection
- **Requirements:** PTM-close exited guard ([coding_plan.md](coding_plan.md) L133–L134), PTM1 ([coding_plan.md](coding_plan.md)), PTM2 ([coding_plan.md](coding_plan.md))
- **Input:** `input011.md`
- **Output:** `output011.md`
- [x] Pass

## Manual Tests

### M000 — phase skills do not write phase_status.md or plan/ACTIVE directly

- **Category:** rejection
- **Requirements:** PH5.3 ([phases.md](phases.md)), PTM1 ([coding_plan.md](coding_plan.md))
- **Why manual:** requires running an actual phase skill (e.g., `/distill-idea`) and observing filesystem state — an AI agent cannot verify a no-write constraint without executing real tool calls in a live environment
- **Test procedure:**
  1. Set up a WI with `plan/ACTIVE` and `phase_status.md` in a known state
  2. Run a phase skill (e.g., `/distill-idea`) without calling `/phase enter` or `/phase exit`
  3. Inspect `phase_status.md` and `plan/ACTIVE` — confirm neither file was modified by the phase skill
  4. Confirm all writes came only from explicit `/phase` subcommand calls
- **Pass criteria:** `phase_status.md` and `plan/ACTIVE` unchanged after phase skill run; only `/phase` calls produce writes to those files
- [ ] Pass

### M001 — mid-WI tripwire triggers halt and mode re-triage via Idea11

- **Category:** edge
- **Requirements:** Idea11 ([gr_idea.md](gr/gr_idea.md)), G3.37 ([guardrails.md](guardrails.md))
- **Why manual:** requires real HITL interaction — human must choose between the two 3.37 resolution paths (approve narrow edit vs. re-triage); AI agent cannot simulate the human decision and verify audit trail on GH issue body
- **Test procedure:**
  1. Start a `mini` WI and enter the `aln` phase
  2. During `aln`, surface a tripwire discovery (e.g., task touches auth)
  3. Set `tripwire_halt: true` in `phase_status.md` via `/phase`
  4. Human chooses resolution path (i) narrow edit or (ii) `/triage-idea --remode`
  5. Verify chosen path is recorded on the GH issue body
  6. Verify `tripwire_halt` cleared only after resolution, not silently
- **Pass criteria:** GH issue body contains resolution record; `tripwire_halt` cleared only after human decision; no silent scope expansion occurred
- [ ] Pass

## Untestable Requirements

None. All requirements covered by automated or manual tests above.

---

**Coverage summary:**

| Requirement | Test(s) |
|-------------|---------|
| PTM1 | 000, 001, 007, 009, 010, 011, M000 |
| PTM2 | 000, 001, 007, 009, 011 |
| PTM3 | 000 |
| PTM4 | 003 |
| PTM5 | 000, 009 |
| PTM6 | 002 |
| PTM7 (mode-legal) | 000, 005, 010 |
| PTM7 (prev-exited) | 000 |
| PTM7 (tripwire-halt) | 008 |
| PTM8 (artifacts) | 001, 006 |
| PTM8 (HITL ack) | 001 |
| PTM9 | 002, 003, 004 |
| PTM-close (terminal-phase guard) | 009, 010 |
| PTM-close (exited guard) | 009, 011 |
| PTM-close (ACTIVE clear) | 009 |
| PH4.2 | 003 |
| PH4.3 | 003 |
| PH4.4 | 005 |
| PH5.3 | M000 |
| G3.37 | 004, 007, 008, M001 |
| Idea8 | 005 |
| Idea11 | M001 |
