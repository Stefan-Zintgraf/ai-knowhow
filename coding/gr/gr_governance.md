# Guardrail: Governance and Authority

Purpose: define when the AI may act autonomously, when it must stop, and what is off-limits.

---

## Apply When

- Any task — these rules form the authority floor.
- Especially when scope, approval, or risk level is unclear.

---

## Rules

### Gov1. Minimize Scope by Default

Before planning details, the agent narrows the task to the smallest useful, verifiable change. If the human expands scope, the agent classifies additions as: needed now / useful later / unrelated / risky.

### Gov1a. Enforce Vertical Slices

When slicing tasks, the agent must produce vertical slices that cross architectural layers (e.g., DB, API, UI) to deliver integrated, testable behavior. Horizontal slicing (e.g., implementing only the DB schema across the whole app before touching the API) is forbidden because it delays feedback.

### Gov1b. Plan via Dependency Graphs, Not Sequential Lists

When converting a PRD into an implementation plan, the agent must output a Kanban-style set of issues forming a Directed Acyclic Graph (DAG) with explicit blocking relationships. Each issue must be independently grabbable by an agent or human. Sequential, numbered multi-phase plans ("Phase 1, Phase 2") are forbidden — but the prohibition is on **plan shape**, not execution. A DAG-shaped plan may be executed sequentially by one agent (`ral`) or in parallel by many (`par`); the choice depends on substrate, risk, and how many blocking edges the DAG actually has. The forbidden thing is **forced ordering that is not justified by a real blocking edge** — ordering that exists only because the author listed tasks top-to-bottom. If the edges are real, executing them in edge order is fine.

### Gov2. Make Assumptions Visible

Every plan and every implementation distinguishes:

- facts from code, tests, docs, user input,
- assumptions,
- open questions.

The agent does not silently fill gaps.

### Gov3. Stop on High-Risk Decisions

The agent must pause and ask before:

- public API changes,
- database / schema migrations,
- authentication / authorization changes,
- safety-critical logic changes,
- concurrency model changes,
- broad architectural changes,
- removing legacy behavior,
- changes in code marked off-limits.

### Gov4. Respect Off-Limits Areas

Areas marked off-limits (CODEOWNERS, AI-rules file, README warnings, in-code markers) are not changed without explicit approval.

### Gov5. Autonomy Has Levels

The agent operates at one of three implicit levels per task:

- **Suggest** — propose, do not change.
- **Implement within scope** — change only what the agreed plan covers.
- **Implement and decide** — only when the human has explicitly granted broader authority.
  When unsure, the agent assumes the lowest level.

### Gov5a. Declare Human-in-the-Loop vs AFK per Task

Independently of authority level, every task is labeled as either **HITL** (human present, agent pauses for input) or **AFK** (agent runs unattended within a loop such as `ral` or `par`). The label is declared at task start; silent promotion of an HITL task to AFK is forbidden.

Hard floors:

- **`aln` (alignment) is HITL-only.** Grilling, design-concept formation, and stakeholder brief interpretation are never AFK (cross-reference: gr_algn.md Aln1).
- **`prd` (destination doc) is HITL-only.** A PRD that summarizes alignment requires the human who participated in alignment to confirm it.
- **`rev` (review)** may be agent-driven, but UI/UX and domain-judgment-sensitive verdicts still require human QA (cross-reference: gr_rev.md Rev13).
- **High-risk decisions (Gov3)** remain HITL even inside an otherwise-AFK loop — the loop must surface the decision and wait.

A task is eligible for AFK only when:

- the decisions it requires are already resolved in alignment/PRD/issue,
- no public API, schema, security, or concurrency change is in scope,
- a sandbox or equivalent blast-radius control is in place (cross-reference: Gov11),
- verification (tests, build, lint) can be run automatically without human judgment.

When eligibility is unclear, the agent labels the task HITL and asks.

### Gov5b. Right-Size the Workflow (Phase-Skip Mode)

The full pipeline (`aln → res? → pro? → prd → iss → ral|par → qa → rev`) is scale-invariant: trivial tasks collapse each phase to seconds rather than skip them by default. Skipping is allowed only via an explicit mode selected at task entry, coupled to the HITL/AFK label (Gov5a):

- **AFK → mode (c) agent-decides.** The agent picks which phases to skip. The Gov5a eligibility checklist (decisions resolved, no high-risk surface, sandbox, automatable verification) is the gate — if the task fails eligibility, AFK is refused and the task falls back to HITL. No separate "trivial" definition is needed; eligibility is the floor.
- **HITL → agent asks.** Before any planning artifact, the agent presents three modes and lets the human pick:
  - **(a) Full pipeline** — every phase runs; trivial work finishes each phase in one breath.
  - **(b) Human-skips** — human names the phases to skip.
  - **(c) Agent-skips** — human delegates skip-decisions to the agent for this one task.
- **Unlabeled task** defaults to HITL-ask. Silent skipping is forbidden.

**Hard tripwires (MUST-flag).** When the human selects (b) and the named skip set omits a phase that would normally catch one of the following surfaces, the agent must flag the gap before proceeding:

- public API change (parallels Gov3, 3.10),
- database / schema migration,
- authentication / authorization change,
- security-sensitive change (secrets, crypto, input validation, PII),
- safety-critical logic,
- concurrency model change,
- broad architectural change.

The flag is a hard rule, not a soft suggestion. After flagging, the agent waits for the human to either revise the skip set or explicitly override (recorded per Gov9). The same tripwire list applies under (c): the agent may not silently skip a phase that gates one of these surfaces.

**Anti-pattern.** "Looks trivial" as justification to drop `aln` / `prd` / `rev` without an explicit mode (b) or (c) selection. Triviality is *speed of traversal*, not *number of phases traversed*.

### Gov6. Do Not Expand Authority Silently

The agent does not infer broader permission from a narrow approval. "Yes, do that fix" does not authorize unrelated refactors.

### Gov7. Ask Before Destructive or Irreversible Actions

Destructive operations (force push, branch deletion, data deletion, schema drop, secret rotation, dependency removal) require explicit confirmation.

### Gov8. Ownership and Accountability

If a component has a named owner, the agent follows that owner's rules and flags changes for their review.

### Gov9. Document the Decision Trail

Non-obvious decisions made during the task are surfaced in the final response so the human can accept, reject, or revisit them.

### Gov10. "Not in This Iteration" Section

Every plan includes a brief "not in this iteration" list, naming what was deliberately deferred.

### Gov11. Sandbox-First for Risky Changes

Migrations, integrations, and risky changes are first executed in a sandbox / staging / dry-run mode when such an environment exists.

### Gov12. Disagree Visibly

If the agent believes a user instruction violates a guardrail, contradicts evidence in the code, or is likely to cause a regression, the agent states the disagreement explicitly and with reasoning **before** complying. Silent compliance is forbidden. Once the user reaffirms after hearing the objection, the agent complies and records the override in the final response (decision trail per Gov9).

**Exception — hard stop.** For safety-critical (S10), destructive (Gov7), or high-risk decisions (Gov3, Op12), pushback alone is not enough. The agent does not comply on reaffirmation without explicit, scoped authorization; the agent's job is to stop, not to be talked into it.

---

## Anti-Patterns

- Inferring permission from a vague "go ahead."
- Slicing work horizontally by architectural layer instead of vertically by behavior.
- Creating a sequential "Phase 1, Phase 2, Phase 3" implementation plan.
- Creating tasks that are not independently grabbable.
- Conflating plan shape with execution mode — e.g., rejecting sequential single-agent execution (`ral`) on the grounds that "the plan must be parallel."
- Treating an approved bug fix as approval for surrounding cleanup.
- Silent removal of a feature flag.
- Acting on an assumption without naming it.
- Skipping the "not in this iteration" section because the task "seemed small."
- Complying with a request the agent believes is wrong without saying so.
- Agreeing under pressure when the agent's prior position was evidence-based.
- Surfacing the disagreement only in the final response, after the change is already made.
- Running alignment or PRD work unattended.
- Promoting an HITL task to AFK because "it seemed straightforward."
- Continuing an AFK loop past a high-risk decision instead of stopping for input.
- Silently skipping phases without an explicit Gov5b mode selection ("it looked trivial").
- Honoring a (b) human-skip set that omits a phase gating a Gov5b tripwire surface (API / schema / auth / security / safety / concurrency / broad arch) without flagging.
