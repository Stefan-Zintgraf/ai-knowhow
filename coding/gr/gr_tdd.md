# Guardrail: Test-Driven Development (TDD)

Purpose: define the discipline an agent must follow when producing logic in an implementation phase (`ral` / `par`). TDD is the loop that keeps an autonomous agent honest — a failing test it wrote is the only evidence that the code it then wrote does what was asked.

Scope: applies to any task that produces or modifies executable logic in `ral` / `par`. Also referenced from `rev` (review checks the loop was followed) and `ica` (architecture passes may surface test-boundary problems).

Origin: Pocock — "Agentic TDD" (Workflow 6). Cross-references core rule §3.22 in [guardrails.md](../guardrails.md). Supersedes the former T12 / T12a entries in [gr_testing_verification.md](gr_testing_verification.md).

---

## Apply When

- Implementing any logic change in `ral` / `par`, regardless of layer (backend, frontend, CLI, infra-as-code with assertable behavior).
- Fixing a bug: a failing reproduction test comes first.
- Refactoring legacy code: characterization tests come first (see also `gr_brownfield.md`).
- Reviewing (`rev`): verifying the loop below was actually followed, not just that tests exist.

Not applicable to: pure formatting / comment-only changes, dependency-version bumps with no behavior change, doc-only edits.

---

## The Loop

```
Red    → write one failing test, run it, confirm it fails for the expected reason
Green  → write the minimum code to make it pass, run the test, confirm it passes
Refactor → improve structure with tests still green; rerun after each change
```

One trip around the loop = one tightly-scoped behavior. Multiple behaviors = multiple trips, not one big test + one big implementation.

---

## Rules

### TDD1. Red Before Green

The agent writes a failing test before writing implementation code. Writing tests after the implementation is forbidden — a test that has never been red proves nothing about the code under it.

### TDD2. Prove the Red is Real (No False Greens)

If a newly written test passes immediately, treat it as a false green — framework misconfiguration, test-filtering, wrong path, or a tautological assertion. Intentionally break the assertion (e.g. `expect(true).toBe(false)`), rerun, and confirm the framework actually executes and fails the file. Restore the real assertion before continuing.

### TDD3. Red Must Fail for the Right Reason

A test that fails because of a syntax error, missing import, or unrelated exception is not a valid Red. The failure message must point at the behavior under test. If the failure cause is wrong, fix the test before writing implementation.

### TDD4. Green Means Minimum Code

In the Green step, write only enough code to satisfy the current failing test. Adding code for tests not yet written is speculation (cross-ref §3.5 / C8). Each additional behavior gets its own Red first.

### TDD5. Refactor Is Mandatory, Not Optional

Green is not done. After Green, refactor with tests staying green: rename for clarity, remove duplication, deepen modules where shallow ones emerged (cross-ref §3.19 / M1). Skipping the Refactor step is the most common failure mode of agentic TDD — it produces working code that decays into shallow-module sprawl over many loop iterations.

### TDD6. Mock Discipline

- **Mock external surfaces only** — network, filesystem, clock, randomness, third-party SDKs.
- **Do not mock code you own.** If owned code is hard to test without mocks, the design is wrong; fix the design, not the test.
- **Never mock to make a Red turn Green.** A mock that exists solely to satisfy an assertion proves the assertion is asking the wrong question.
- Prefer fakes / in-memory implementations over mocks when the surface is non-trivial.

### TDD7. One Failing Test at a Time

The agent does not stack multiple failing tests and then implement. One Red, one Green, one Refactor, then the next Red. Batching breaks the "fails for the right reason" check and lets unrelated failures hide each other.

### TDD8. TDD Applies to Frontend and Visual Tasks

Frontend and visual work is not exempt. Use component tests, browser automation, snapshot tests with intentional change-review, or visual-regression tooling. "It's just UI" is not a reason to skip Red.

### TDD9. No Retroactive Tests

Tests added in the same change as the implementation, with no recorded Red phase, are treated as documentation, not verification. They do not satisfy §3.6 / T1. In review, the absence of an observed Red is a finding.

### TDD10. Refactor Step Must Not Change Behavior

During Refactor, no test is added, removed, weakened, or made to assert something new. If a refactor surfaces a missing behavior, finish the refactor first (tests still green), then open a new Red for the missing behavior.

---

## Anti-Patterns

- Writing the implementation, then writing a test that happens to pass.
- Accepting an initial green without breaking-then-restoring the assertion to verify framework execution.
- Stacking many failing tests before implementing, so failures mask each other.
- Skipping Refactor because Green felt like done.
- Mocking owned code to dodge a real design problem.
- Adding behavior during Refactor.
- "Disabling for now" a failing test instead of fixing cause (cross-ref T10).
- Treating TDD as backend-only — frontend changes ship without a Red.

---

## Notes on Interaction with Other Guardrails

- §3.6 / T1 (Verify Changes): TDD is the default mechanism for satisfying this rule during `ral` / `par`.
- §3.5 / C8 (No Speculative Design): TDD4 enforces minimum-code Green; adding code for unwritten tests is the same anti-pattern.
- §3.19 / M1 (Deep Modules): Refactor step (TDD5) is the natural moment to deepen shallow modules surfaced by the test pressure.
- `gr_brownfield.md`: refactor of legacy code requires characterization tests as the Red.
- `gr_rev.md` (Rev4 reads tests first): reviewer verifies the loop was followed, not just that tests exist.
- `gr_algn.md`: behaviors agreed in `aln` are the unit of one Red — if alignment is vague, TDD7 surfaces it immediately.

---

## Pulling This Document (Op14b)

TDD detail is **pulled**, not always-on. Pull triggers:

1. **Routing index entry §4.16** in [guardrails.md](../guardrails.md) — any task whose routing identifies "Test-Driven Development" loads this file. Routing happens before implementation per §5.
2. **Skill precondition (A4 `ralph-loop`)** — the skill prompt loads `gr_tdd.md` on entry to `ral`, before the first test or src edit, since AFK loops cannot be trusted to route on their own.
3. **Reviewer push (Rev2, Op14b)** — `rev` pushes this file into context up front to verify the loop was followed.

If a task in `ral` / `par` proceeds without this file pulled, it is a routing violation — stop, declare routing, then continue.
