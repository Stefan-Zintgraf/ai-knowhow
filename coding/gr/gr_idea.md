# Guardrail: Idea

Purpose: distill a raw stakeholder brief, backlog item, or vague ask into **3–6 major goals** that seed the `aln` grilling session. Idea is not design and not a PRD — it is the *starter*. No details, no module map, no APIs, no acceptance criteria. Just the small set of intents the work must serve.

Scope: applies to the `ide` phase (see [phases.md](../phases.md)).

Origin: Pocock — "Idea" is phase 1 of the 7-phase pipeline. Local placement: precedes `aln`. Idea fixes the small risk that grilling drifts because the *target* of grilling was never named.

---

## Apply When

- A new feature, change, or initiative enters the workflow from a brief, Slack note, ticket, email, or verbal ask.
- A backlog item is vague enough that `aln` would not know where to start grilling.
- Before any `aln` grilling, `res` research, or planning artifact is produced.

Skip when: the upstream artifact already names 3–6 explicit goals (e.g. a written product memo). In that case `ide` collapses to a one-line confirmation, per 3.29 (collapse, not skip) — the confirmed list is still written to `plan/<WI>/idea.md` per Idea7; collapse short-circuits the distillation work, not the artifact.

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

### Idea7. Persisted to `plan/<WI>/idea.md`

The confirmed goal list is written to `plan/<WI>/idea.md`. `<WI>` is a human-confirmed snake_case slug (e.g. `ai_mail`, `fix_crash_abc`) — single artifact per WI, never a shared `idea.md`, never multiple idea files under one WI. Downstream phases (`aln`, `prd`, `iss`, ...) read this file as the anchor for goals; PRD Goals section folds it but does not replace it.

Companion status file: `plan/<WI>/status_idea.md` with frontmatter:

```
---
status: open|wip|done
updated: <YYYY-MM-DD>
owner-issue: #NNN   # the WI's owning issue/PR; anchors 3.33 retirement
---
```

Refresh `updated:` on every run. Default `status: wip` on a successful artifact write. Human-only `done` — never auto-flip. On reopen, flip `done → wip` (never back to `open`). `owner-issue:` is mandatory — `status_idea.md` is the WI anchor; sibling artifacts under `plan/<WI>/` inherit the same owner, so the field is set once here. On failure runs (under-budget, human rejected, no human acceptance), write nothing — no `idea.md`, no `status_idea.md`.

Retirement: the goal list is WI-scoped, not durable. Deleted with the rest of `plan/<WI>/` at WI close per 3.33 — same retirement model as 3.27 (research). Persistence is bounded; documentation-rot risk that 3.24 (PRD) and 3.27 (research) address is handled here by 3.33's close-time deletion, not by avoiding the artifact altogether.

---

## Anti-Patterns

- Producing 10+ "goals" that are actually requirements or features.
- Skipping `ide` and starting `aln` against a vague Slack brief — grilling drifts without a target.
- Letting implementation detail (module names, API shapes) leak into the goal list.
- Treating the goal list as the design — jumping from `ide` straight to `prd`.
- Running `ide` AFK / via Ralph loop.
- Writing the goal list anywhere other than `plan/<WI>/idea.md` — no `idea/<topic>.md`, no shared `idea.md`, no scattered locations. Single canonical path per WI.
- Auto-flipping `status_idea.md` to `done`. Human-only `done`.
- Leaving `plan/<WI>/` behind after the WI closes (3.33 violation).

---

## Notes on Interaction with Other Guardrails

- Precedes [gr_algn.md](gr_algn.md). Idea6 is the explicit hand-off.
- Idea5 extends Aln8 (brief as input) one phase earlier.
- Idea3 (negative goals) feeds Aln15 (negative decisions captured).
- Idea4 (HITL) follows the same hard floor as Aln1, Gov5a.
- Idea7 (persisted to `plan/<WI>/idea.md`) follows the same retirement model as 3.27 (research): in-tree, WI-scoped, deleted at WI close. Enforcement = 3.33 + Q11 merge-gate check that `plan/<WI>/` is gone when the WI's PR closes. Distinct from 3.24 (PRD), which goes external entirely.
