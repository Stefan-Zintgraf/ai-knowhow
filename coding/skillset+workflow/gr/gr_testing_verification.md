# Guardrail: Testing and Verification

Purpose: define proof that a change is correct and safe before it is considered done.

---

## Apply When

- Behavior change, bug fix, refactoring, legacy code change.
- Public API change.
- Any change with regression risk.

---

## Rules

### T1. Verification Plan Before Implementation
Before changing code, the agent states how the change will be verified (which tests, which checks, which manual review).

### T2. Required Test Levels Match the Change
- Pure logic change: unit test.
- Module-internal behavior: unit or integration test.
- Cross-module / IO behavior: integration test.
- External contract: contract or end-to-end test.
The agent picks the smallest level that proves the change.

### T2a. Vertical Slices Demand Integration Tests
When implementing a vertical slice or tracer bullet crossing architectural layers (e.g., DB + API + UI), the verification must include an integration or end-to-end test exercising the full path. Relying solely on isolated unit tests for a vertical slice is forbidden because it fails to prove the layers actually connect.

### T3. Regression Test Before Behavior Change
If a bug fix or refactor risks regression, an automated test that fails *before* the change and passes *after* must exist. No silent fixes.

### T4. Characterization Tests for Legacy Behavior
Before refactoring legacy code without specs, capture current behavior in tests (golden-master / characterization). The refactor must not change those tests.

### T5. No Mocking of the Unit Under Test
Mocks replace collaborators, not the code being verified. Tests must exercise real behavior of the target.

### T6. Tests Are Deterministic
No reliance on wall-clock time, random seeds, network, or order of execution unless explicitly controlled.

### T7. Tests Belong to the Domain They Test
Test names and assertions use the ubiquitous language. A failing test must read like a domain statement, not an implementation trace.

### T8. Static Analysis and Build Must Pass
Linter, type checker, and build run clean before the change is considered done.

### T9. Definition of Done Is Explicit
A change is done only when: code change + verification evidence + (when relevant) updated docs + no broken existing tests.

### T10. Don't Suppress Failing Tests
The agent must not skip, comment out, or weaken an existing failing test without explicit human decision and a recorded reason.

### T11. Evidence in the Final Response
The final response lists which commands were run, which tests passed, and any check that was skipped (with reason). See `gr_operational.md`.

### T12. Test-Driven Development — See `gr_tdd.md`

The TDD loop (Red-Green-Refactor), false-green verification, mock discipline, and frontend/visual applicability are defined in their own document: [gr_tdd.md](gr_tdd.md). Routing index entry §4.16. Core rule §3.22.

---

## Anti-Patterns

- Adding a test that re-asserts the implementation, not the behavior.
- Verifying a vertical slice / tracer bullet using only isolated unit tests without an integration path.
- Marking a flaky test as `skip` instead of fixing it.
- Refactoring legacy code with no characterization tests.
- Claiming "all tests pass" without running them.

(TDD-specific anti-patterns — retroactive tests, unverified initial greens, missing Refactor — live in [gr_tdd.md](gr_tdd.md).)
