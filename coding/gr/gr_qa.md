# Guardrail: Manual QA

Purpose: define how a human-driven quality check of a runnable slice is conducted, so that taste, product judgment, and real-world behavior verification are reintroduced after agent implementation — and so findings are routed back into the workflow rather than patched ad hoc.

Scope: applies to the `qa` phase (see [phases.md](../phases.md)). `qa` is a **mandatory sequential checkpoint** after `ral` / `par` and before `done`.

Origin: Pocock — "Manual QA as Taste Preservation" (Workflow 8). "Reintroduce human taste, product judgment, and real-world behavior checking after agent implementation."

---

## Apply When

- A vertical slice produced by `ral` / `par` is runnable and behaviorally testable.
- A slice exposes user-visible behavior, UI, copy, or domain-judgment surface.
- A migration, schema change, or integration point was introduced and needs real-world exercise beyond automated tests.

---

## QA Model in This Repo

QA is performed by the **human**, not the agent. The agent's role is to:

1. Confirm slice preconditions (running app, implemented surface, available test data).
2. Surface the PRD / user stories / acceptance criteria for human reference.
3. Receive findings and route them per Q5 (fix-now vs. backlog).

Manual QA does not replace automated review (`rev`); it complements it. `rev` checks the diff in the smart zone; `qa` checks the running behavior against human judgment.

---

## Rules

### Q1. Slice Must Be Runnable Before QA Begins

QA does not start until the slice runs end-to-end in a real or near-real environment. A slice that compiles but cannot be exercised by a human is not ready for `qa` — it returns to `ral` / `par` for completion.

### Q2. Exercise the User Path, Not Only the Happy Path

The human must walk at least one realistic user persona's full path through the new behavior, including:

- Empty / first-use state.
- Error and validation paths.
- Boundary / unusual inputs the PRD called out.
- Permissions / role variants if the slice touches authz.

Happy-path-only QA is an anti-pattern (Pocock failure mode #1).

### Q3. Inspect Surface That Tests Cannot Judge

The human explicitly checks dimensions automated tests do not cover well:

- UI layout, spacing, hierarchy, accessibility.
- Copy quality, tone, terminology consistency with the domain language.
- Interaction feel, latency, perceived responsiveness.
- Naming of routes, fields, buttons, errors.
- Migration / schema effects visible in the running system.

### Q4. Every Finding Becomes an Issue

No finding is patched ad hoc. Each finding is filed as an issue and triaged. Inline fixes during QA bypass the workflow and lose traceability (Pocock failure mode #2).

### Q5. Human Triages Each Finding: Fix-Now or Backlog

For each finding, the human decides:

- **Fix-now**: blocks the slice. New issue is added to `iss`, slice loops back to `ral` / `par`, then re-enters `qa`.
- **Backlog**: does not block. New issue is filed for later. Slice can pass `qa`.
- **No-op**: explicitly rejected as not-an-issue (with rationale recorded).

Default when in doubt: **fix-now** for safety-critical, destructive, data-integrity, or user-trust-affecting findings; **backlog** for cosmetic or polish items.

### Q6. QA Output Format

QA output is structured:

- **Verdict**: pass / pass-with-backlog / fail (fix-now required).
- **Slice exercised**: which user path(s) were walked.
- **Findings**: list, each with severity, category (UI / copy / behavior / data / perf / a11y / other), and triage decision (fix-now / backlog / no-op).
- **Coverage gaps**: dimensions or paths the QA pass did not exercise (so they are not silently treated as covered).

### Q7. QA Throughput Must Not Lag Implementation Throughput

If agent throughput exceeds QA capacity, the implementation queue is paused, not the QA queue (Pocock failure mode #3). Unreviewed slices are not allowed to stack into a hard-to-QA batch.

### Q8. Recurring QA Categories Become Automated Tests

Findings that repeat across slices (same category, same kind of bug) are converted into automated tests during `ica` or as part of the fix-now follow-up. QA is for taste; recurring mechanical failures should not need human eyes.

---

## Anti-Patterns

- Skipping `qa` because "tests passed."
- Walking only the happy path.
- Patching a finding inline during the QA session without filing an issue.
- Treating every finding as fix-now (workflow grinds) or every finding as backlog (quality decays).
- Letting the implementation queue outrun QA capacity.
- Recording a verdict without listing which paths were exercised — implicit coverage claims.
- Using `qa` to do the work `rev` should have done (or vice versa).

---

## Notes on Interaction with Other Guardrails

- Pairs with `gr_review.md` — `rev` checks the diff, `qa` checks the running behavior. Both are required for user-visible changes (cross-reference: Rev13).
- Findings routed to `iss` re-enter the standard issue flow with HITL/AFK tagging per `gr_governance.md`.
- Recurring findings feed `gr_modules.md` / `ica` (Q8): module boundaries and test boundaries may need rework.
- Cross-reference: `gr_alignment.md` — visual taste and domain judgment surfaced during `aln` are the same dimensions verified during `qa`.

---

## Status

Skeleton — rules drafted, not yet validated against real QA sessions. To be refined during initial use.
