# Guardrail: Idea

Purpose: distill a raw stakeholder brief, backlog item, or vague ask into **3–6 major goals** that seed the `aln` grilling session. Idea is not design and not a PRD — it is the *starter*. No details, no module map, no APIs, no acceptance criteria. Just the small set of intents the work must serve.

Scope: applies to the `ide` phase (see [phases.md](../phases.md)).

Origin: Pocock — "Idea" is phase 1 of the 7-phase pipeline. Local placement: precedes `aln`. Idea fixes the small risk that grilling drifts because the *target* of grilling was never named.

---

## Apply When

- **Every** task entering the workflow. `ide` is the only always-entered phase (Idea8). It owns the entry-triage decision, not just goal distillation.
- A new feature, change, or initiative enters the workflow from a brief, Slack note, ticket, email, or verbal ask.
- A backlog item is vague enough that `aln` would not know where to start grilling.
- Before any `aln` grilling, `res` research, or planning artifact is produced.

Skip when: never. `ide` is the entry phase and always runs. What collapses is what `ide` *does* after triage (per Idea8): for `direct-edit` mode, distillation is skipped; for `mini`/`full`, distillation runs. The upstream-artifact-names-goals shortcut (per 3.29 collapse) reduces distillation to a one-line confirmation but does not skip the phase itself.

---

## Rules

### Idea1. Output Is 3–6 Major Goals
Skills: distill-idea

The `ide` phase produces a short list — between **3 and 6** major goals. Fewer than 3 means the brief is too narrow for goal-shaped framing (probably a direct task — go to `aln` with the brief). More than 6 means the goals are not yet major (decompose or merge before leaving `ide`).

### Idea2. No Details
Skills: distill-idea

A goal in `ide` names *what the work must serve*, not *how*. Forbidden in `ide` output:

- Module names, file paths, API shapes.
- UX specifics (screens, components, layouts).
- Acceptance criteria.
- Tech choices (library X, pattern Y).
- Effort or timeline estimates.

Details belong to `aln` (concept), `prd` (specification), or `iss` (tasks). If a detail leaks into `ide`, the agent strips it and notes it as "deferred to aln/prd."

### Idea3. Negative Goals Are Welcome
Skills: distill-idea

Explicit non-goals are first-class in `ide` and count toward the 3–6 budget when they materially shape the work. Examples: "not a mobile app," "no real-time updates," "no migration from system X." Negative goals here become Aln15 negative decisions later.

### Idea4. HITL Only
Skills: distill-idea, triage-idea

`ide` is human-in-the-loop. The agent proposes a goal list from the brief; the human edits, accepts, or rejects. AFK / Ralph loops are forbidden during `ide` — the same reason `aln` is HITL-only (Aln1, Gov5a): the goal set anchors every later phase, so a wrong anchor compounds.

### Idea5. Brief Is Input, Not Output
Skills: distill-idea

The original brief (Slack, ticket, email) is the raw material the agent distills. The brief is **not** the `ide` output. Even a well-written brief gets restated as a 3–6 goal list, because the act of distilling surfaces missing goals and unstated assumptions. Cross-reference: Aln8 (treat brief as input, not truth) — Idea5 extends Aln8 one step earlier.

### Idea6. Output Feeds `aln`, Does Not Replace It
Skills: distill-idea

The goal list is the *starter* for grilling, not a substitute for it. `aln` walks every branch of every goal. An agent that reads a goal list and jumps to `prd` violates 3.21. The goal list narrows what `aln` grills over; it does not shortcut the grilling.

### Idea7. Persisted to `<artifacts>/<slug>/idea.md`
Skills: distill-idea

The confirmed goal list is written to `<artifacts>/<slug>/idea.md`. `<slug>` is kebab-case derived from the brief title (or, for `direct-edit`/`mini` where the issue lands at `ide`, the GH issue title), stopwords stripped, truncated ≤40 chars. The folder name does **not** encode the GH issue number — the issue is resolved via `status_idea.md` `owner-issue:` frontmatter (set at `ide` for direct-edit/mini, populated at `iss` for `full`). Single artifact per WI, never a shared `idea.md`, never multiple idea files under one WI. Downstream phases (`aln`, `prd`, `iss`, ...) read this file as the anchor for goals; PRD Goals section folds it but does not replace it.

**Mode-dependent persistence (per Idea8):**
- `full` and `mini` modes — create `<artifacts>/<slug>/idea.md` + `status_idea.md` as defined below.
- `direct-edit` mode — **no `<artifacts>/<slug>/` files created.** The GH issue body carries the brief verbatim and the verification record; that is the complete WI record. Retirement (3.33) does not apply because no files exist. No `status_idea.md` flip needed.

Slug collision: if two open issues would generate the same slug after truncation, suffix `-2`, `-3` and surface to human at folder-create time.

Companion status file: `<artifacts>/<WI>/status_idea.md` with frontmatter:

```
---
status: open|wip|done
updated: <YYYY-MM-DD>
owner-issue: #NNN   # the WI's owning issue/PR; anchors 3.33 retirement
---
```

Refresh `updated:` on every run. Default `status: wip` on a successful artifact write. Human-only `done` — never auto-flip. On reopen, flip `done → wip` (never back to `open`). `owner-issue:` is the WI's authoritative issue pointer — set to `#N` once the issue lands (at `ide` for `direct-edit`/`mini`, at `iss` for `full`); until then it is `pending` and `iss` is responsible for populating it. `status_idea.md` is the WI anchor; sibling artifacts under `<artifacts>/<WI>/` inherit the same owner, so the field is set once here. On failure runs (under-budget, human rejected, no human acceptance), write nothing — no `idea.md`, no `status_idea.md`.

Retirement: the goal list is WI-scoped, not durable. Deleted with the rest of `<artifacts>/<WI>/` at WI close per 3.33 — same retirement model as 3.27 (research). Persistence is bounded; documentation-rot risk that 3.24 (PRD) and 3.27 (research) address is handled here by 3.33's close-time deletion, not by avoiding the artifact altogether.

### Idea8. Triage and Mode Selection (Entry Decision)
Skills: triage-idea

`ide` is the entry phase for **every** task. Its first act, before any goal distillation, is to triage the incoming brief and pick a workflow mode. Three modes:

- **`direct-edit`** — `ide` → `ral` → `qa`. Skips `aln`/`prd`/`iss`. No `<artifacts>/<slug>/` files; issue body is the record. TDD exemption may apply per TDD11.
- **`mini`** — `ide` → `aln`(collapsed per Aln19) → `ral` → `qa`. Issue + `<artifacts>/<slug>/idea.md` + collapsed `aln` artifacts.
- **`full`** — `ide` → `aln` → [`res`?] → [`pro`?] → `prd` → `iss` → `ral`\|`par` → `qa`. Full pipeline.

**Triage matrix (4 axes).** The agent scores each axis with the human present (HITL per Idea4):

| Axis | Values |
| --- | --- |
| Design ambiguity | none / some / lots |
| Blast radius | local (≤1 file, no public API) / module / system |
| Reversibility | trivial / costly / hard |
| Existing test coverage | covers it / partial / none |

**Decision rule:**

- All-low (no ambiguity, local, trivial, fully covered) → **`direct-edit`**.
- Any one axis at medium (some ambiguity OR module-scope OR partial coverage OR costly reversibility) → **`mini`**.
- Any axis at high (lots of ambiguity OR system blast OR hard-reverse OR uncovered behavior change) → **`full`**.
- **Tripwire override**: any task touching a tripwire surface (the 3.29 list — public API, schema, auth, security, safety-critical logic, concurrency, broad architecture) forces **`full`** regardless of axis scores.

**HITL pick is mandatory.** The agent proposes a mode + axis scores + reason; the human confirms or overrides. Silent auto-pick is forbidden (Idea4, 3.16). Exploration budget for triage-time codebase reads: see Idea10.

**Idea8 collapse:** for `direct-edit`, distillation (Idea1) is skipped entirely — the brief verbatim is the implicit single goal recorded on the issue. For `mini`/`full`, distillation proceeds per Idea1.

### Idea9. Issue Invariant: Exactly One Issue Before Any `ral`
Skills: triage-idea

Before any `ral` invocation, **exactly one GH issue exists** for the WI. Emitter depends on mode (Idea8):

- `direct-edit`, `mini` — `ide` emits the issue.
- `full` — `iss` emits issue(s); `ide` emits no issue, only the `<artifacts>/<slug>/idea.md` anchor.

**Dedupe protocol (before any issue create).** Agent runs `gh issue list --state open --search "<key terms from brief>"`, displays top 3–5 matches, human picks:

- **new** — create new issue via `gh issue create --title --body --label ready-for-agent`; capture `#N` via `--json number`.
- **link to #N** — reuse the existing folder if one is already mapped to `#N` in `<artifacts>/INDEX.md` (its `owner-issue:` in `status_idea.md` = `#N`); else create with the current slug and populate `owner-issue: #N`.
- **abort** — `ide` exits; no issue, no folder; clean state.

**Folder creation:** for `mini`, `mkdir <artifacts>/<slug>/` after issue create and write `owner-issue: #N` into `status_idea.md`. For `full`, `mkdir <artifacts>/<slug>/` at `ide` before any issue exists; `owner-issue:` is left blank/`pending` in `status_idea.md` and populated by `iss` when the issue lands. For `direct-edit`, no folder.

**`<artifacts>/INDEX.md`** is auto-regenerated from `gh issue list --state open` + folder listing — never hand-maintained.

Mode is recorded on the issue body and as a label (`mode:direct-edit` / `mode:mini` / `mode:full`) so downstream automation can read it without parsing body text.

### Idea10. `ide`-Time Exploration Budget
Skills: triage-idea

The agent may need light codebase exploration during triage (Idea8) to score the 4 axes honestly. Mechanism: dispatch B10 (subagent-for-exploration, see gr_algn.md Aln7) with a **strict budget cap of ≤5 file reads, summary only**.

Budget rule:

- Within budget → score axes, propose mode.
- Budget exceeded → **auto-recommend mode upgrade to `mini`**. Rationale: a task whose triage needs deeper exploration is not direct-edit. Surface this to the human as a triage finding.

No edits during `ide` exploration. No deep reads. The B10 dispatch follows the same isolated-context discipline as in `aln` (Aln7) — main context stays clean.

### Idea12. Concept Sharpening (Sub-Brief Input)
Skills: distill-idea

When the incoming input is a **vague notion** rather than a formed brief — no clear problem statement, no identifiable user, no articulated value — the agent runs a structured sharpening step before Idea1 goal distillation.

**Trigger:** agent judges the input too thin for direct goal extraction. Surfaced to the human: "Input looks sub-brief — running concept sharpening before goal distillation." Human may override ("skip, just distill").

**Sharpening produces five fields:**

| Field | What it captures |
| --- | --- |
| Problem | Why does this need to exist? |
| Target user | Who is this for? |
| Core value | What makes it worth doing? |
| Key assumptions | What are we taking for granted? |
| Open questions | What don't we know yet? |

**Ephemeral intermediates (not persisted):** working title and one-sentence pitch help the conversation converge but carry no independent value once goals are distilled. Working title feeds the issue title (Idea9); pitch is consumed by distillation.

**Persistence:** the five fields are written as a **Context** section at the top of `idea.md`, above the goal list. No separate file — Idea7's single-artifact rule holds. Structure:

```markdown
## Context

**Problem:** ...
**Target user:** ...
**Core value:** ...
**Key assumptions:** ...
**Open questions:** ...

## Goals

1. ...
2. ...
```

When input is already a formed brief, Idea12 is skipped — Idea1 runs directly and `idea.md` contains only the Goals section.

**Idea2 applies to Idea12 output.** The five fields name *what* and *why*, never *how*. If implementation detail leaks into any field, the agent strips it (same discipline as Idea2).

**Downstream value:** `aln` reads the Context section to ground its grilling — problem and target-user framing prevents drift. Key assumptions and open questions seed grilling branches directly (cross-ref Aln8, Aln15).

### Idea11. Mode Transitions: Symmetric, Human-Approved Either Way
Skills: triage-idea

Once a mode is picked in `ide`, it can be changed (upgrade or downgrade) under these rules:

- **Either direction may be proposed by either party.** Agent may suggest upgrade ("touched auth — should we move to full?") or downgrade ("scope shrunk after grilling — could collapse to mini?"). Human may suggest either direction at any point.
- **Human approves either direction.** No mode change without explicit human acceptance.
- **Silent change is forbidden** (extension of 3.16 disagree-visibly). Equally forbidden: silently *not* surfacing a mode change the agent believes is warranted.
- **Mid-task upgrade trigger** — see core rule 3.37 (tripwire discovery): agent halts, does not edit, surfaces to human; human picks (i) approve narrow edit with reasoning logged on issue, or (ii) re-enter `ide` for mode re-triage.
- **Audit trail**: every mode change is recorded on the GH issue body (old mode → new mode + reason + who proposed). The `mode:*` label is updated on the issue.

`mini` → `full` auto-recommendation triggers (during `aln`): Adr1 ADR-worthy decision surfaces; >3 unresolved questions after first grilling round; Pro1 prototype gate hits. Agent surfaces; human approves the upgrade.

---

## Anti-Patterns

- Producing 10+ "goals" that are actually requirements or features.
- Skipping `ide` and starting `aln` against a vague Slack brief — grilling drifts without a target.
- Letting implementation detail (module names, API shapes) leak into the goal list.
- Treating the goal list as the design — jumping from `ide` straight to `prd`.
- Running `ide` AFK / via Ralph loop.
- Writing the goal list anywhere other than `<artifacts>/<slug>/idea.md` — no `idea/<topic>.md`, no shared `idea.md`, no scattered locations. Single canonical path per WI.
- Auto-flipping `status_idea.md` to `done`. Human-only `done`.
- Leaving `<artifacts>/<slug>/` behind after the WI closes (3.33 violation).
- Picking a mode silently (Idea8 violation) — mode pick is HITL by construction.
- Skipping the triage step on "obviously trivial" tasks — every entry runs triage, even if it resolves in one turn.
- Creating duplicate issues by skipping the Idea9 dedupe search.
- Exceeding the Idea10 exploration budget without auto-recommending a mode upgrade.
- Silent mode change (Idea11 violation) — either direction needs HITL approval and an audit trail.
- Running Idea12 sharpening on a well-formed brief — wastes a turn when goals can be distilled directly.
- Letting "smallest useful version," market research, or feature lists into the Idea12 fields — those belong to `aln`/`res`/`prd`.

---

## Notes on Interaction with Other Guardrails

- Precedes [gr_algn.md](gr_algn.md). Idea6 is the explicit hand-off.
- Idea5 extends Aln8 (brief as input) one phase earlier.
- Idea3 (negative goals) feeds Aln15 (negative decisions captured).
- Idea4 (HITL) follows the same hard floor as Aln1, Gov5a.
- Idea7 (persisted to `<artifacts>/<WI>/idea.md`) follows the same retirement model as 3.27 (research): in-tree, WI-scoped, deleted at WI close. Enforcement = 3.33 + Q11 merge-gate check that `<artifacts>/<WI>/` is gone when the WI's PR closes. Distinct from 3.24 (PRD), which goes external entirely.
- Idea12 Context section feeds `aln` directly: problem/target-user ground the grilling, key assumptions + open questions seed branches (Aln8, Aln15).
