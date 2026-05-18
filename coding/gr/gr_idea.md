# Guardrail: Idea

Purpose: distill a raw stakeholder brief, backlog item, or vague ask into **3–6 major goals** that seed the `aln` grilling session. Idea is not design and not a PRD — it is the *starter*. No details, no module map, no APIs, no acceptance criteria. Just the small set of intents the work must serve.

Scope: applies to the `ide` phase (see [phases.md](../phases.md)).

Origin: Pocock — "Idea" is phase 1 of the 7-phase pipeline. Local placement: precedes `aln`. Idea fixes the small risk that grilling drifts because the *target* of grilling was never named.

---

## Apply When

- A new feature, change, or initiative enters the workflow from a brief, Slack note, ticket, email, or verbal ask.
- A backlog item is vague enough that `aln` would not know where to start grilling.
- Before any `aln` grilling, `res` research, or planning artifact is produced.

Skip when: the upstream artifact already names 3–6 explicit goals (e.g. a written product memo). In that case `ide` collapses to a one-line confirmation, per 3.29 (collapse, not skip).

---

## Rules

### Idea1. Output Is 3–6 Major Goals

The `ide` phase produces a short list — between **3 and 6** major goals. Fewer than 3 means the brief is too narrow for goal-shaped framing (probably a direct task — go to `aln` with the brief). More than 6 means the goals are not yet major (decompose or merge before leaving `ide`).

### Idea2. No Details

A goal in `ide` names *what the work must serve*, not *how*. Forbidden in `ide` output:

- Module names, file paths, API shapes.
- UX specifics (screens, components, layouts).
- Acceptance criteria.
- Tech choices (library X, pattern Y).
- Effort or timeline estimates.

Details belong to `aln` (concept), `prd` (specification), or `iss` (tasks). If a detail leaks into `ide`, the agent strips it and notes it as "deferred to aln/prd."

### Idea3. Negative Goals Are Welcome

Explicit non-goals are first-class in `ide` and count toward the 3–6 budget when they materially shape the work. Examples: "not a mobile app," "no real-time updates," "no migration from system X." Negative goals here become Aln15 negative decisions later.

### Idea4. HITL Only

`ide` is human-in-the-loop. The agent proposes a goal list from the brief; the human edits, accepts, or rejects. AFK / Ralph loops are forbidden during `ide` — the same reason `aln` is HITL-only (Aln1, Gov5a): the goal set anchors every later phase, so a wrong anchor compounds.

### Idea5. Brief Is Input, Not Output

The original brief (Slack, ticket, email) is the raw material the agent distills. The brief is **not** the `ide` output. Even a well-written brief gets restated as a 3–6 goal list, because the act of distilling surfaces missing goals and unstated assumptions. Cross-reference: Aln8 (treat brief as input, not truth) — Idea5 extends Aln8 one step earlier.

### Idea6. Output Feeds `aln`, Does Not Replace It

The goal list is the *starter* for grilling, not a substitute for it. `aln` walks every branch of every goal. An agent that reads a goal list and jumps to `prd` violates 3.21. The goal list narrows what `aln` grills over; it does not shortcut the grilling.

### Idea7. Ephemeral

The goal list lives only long enough to seed `aln`. Once `aln` produces the design concept and `prd` summarizes it, the goal list is folded into the PRD (typically as the "Goals" or "Objectives" section) and the standalone artifact is discarded. No `idea/<topic>.md` files in the working tree.

---

## Anti-Patterns

- Producing 10+ "goals" that are actually requirements or features.
- Skipping `ide` and starting `aln` against a vague Slack brief — grilling drifts without a target.
- Letting implementation detail (module names, API shapes) leak into the goal list.
- Treating the goal list as the design — jumping from `ide` straight to `prd`.
- Running `ide` AFK / via Ralph loop.
- Keeping the goal list in the repo after the PRD lands.

---

## Notes on Interaction with Other Guardrails

- Precedes [gr_alignment.md](gr_alignment.md). Idea6 is the explicit hand-off.
- Idea5 extends Aln8 (brief as input) one phase earlier.
- Idea3 (negative goals) feeds Aln15 (negative decisions captured).
- Idea4 (HITL) follows the same hard floor as Aln1, Gov5a.
- Idea7 (ephemeral) follows the same shape as 3.24 (PRD retire) and 3.27 (research retire), but no in-tree artifact ever exists, so no lint or Q11 gate is needed.
