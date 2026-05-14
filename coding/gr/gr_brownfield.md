# Guardrail: Brownfield Change Rules

Purpose: preserve invisible intent in existing systems. Brownfield code carries undocumented invariants, edge cases, and "weird but intentional" behavior.

---

## Apply When

- Existing production code is modified.
- Legacy logic is touched, even peripherally.
- Established behavior could be affected.
- Code with sparse or missing tests is changed.

---

## Rules

### B1. Respect Existing Behavior as Intentional
Strange-looking code, dead-looking branches, and odd defaults are assumed intentional until evidence proves otherwise.

### B2. Preserve Behavior First
The order is: preserve behavior → improve structure → add new behavior. These three must not be mixed silently in one change.

### B3. Characterization Tests Before Refactor
Before refactoring untested code, capture current behavior in characterization tests. The refactor must keep those tests green.

### B4. Identify Hidden Invariants Before Changing
Before changing a function, the agent identifies invariants the function may protect (data shape, ordering, idempotency, side-effect order) and states them.

### B5. Small, Reversible Diffs
Brownfield changes are kept small and reversible. Large mechanical refactors require explicit approval and a rollback plan.

### B6. No Opportunistic Cleanup
Reformatting, renaming, restructuring, or "cleanup" that is not part of the task is forbidden. Such work belongs to a separate change.

### B7. Don't Remove "Dead" Code Without Proof
Code that looks unused may serve regulatory, recovery, or edge-case purposes. Removal requires evidence (search, owner confirmation, telemetry).

### B8. Respect Existing Integration Points
External callers, batch jobs, scripts, and downstream consumers may depend on current behavior. The agent must consider integration surface before changing it.

### B9. Rollback Strategy Is Stated
For any non-trivial brownfield change, the agent states how to revert (revert commit, feature flag, deploy back, data backfill).

### B10. Ask Before Touching Off-Limits Areas
Areas marked off-limits (CODEOWNERS, AI-rules file, README warnings, code comments saying "do not change") are not modified without explicit approval.

---

## Anti-Patterns

- Refactoring a payment workflow "while fixing a typo."
- Deleting an "if" branch because it "looks unreachable."
- Mixing bug fix + reformat + dependency upgrade in one PR.
- Renaming a public function during a behavior change.
- Replacing a legacy adapter without checking who calls it.
