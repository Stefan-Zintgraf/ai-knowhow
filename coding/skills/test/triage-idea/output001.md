# Evaluation Criteria

## Requirements Tested
- Idea8: 4-axis triage must identify at least one medium axis (partial test coverage or some design ambiguity) and propose `mini` mode
- Idea4: Agent must present axis scores and proposed mode to human for confirmation
- 3.29: Medium task uses `mini` chain: `ide → aln(collapsed) → ral → qa`

## Pass Criteria
- Output contains a 4-axis scoring table with values for all four axes
- At least one axis scored at medium level (e.g., partial test coverage, some design ambiguity)
- No axis scored at high level
- Proposed mode is `mini`
- Output includes an explicit prompt asking human to confirm mode
- No tripwire surfaces identified that would force `full`

## Fail Criteria
- Mode proposed is `direct-edit` (task has partial coverage — not all-low)
- Mode proposed is `full` (no axis is at high level, no tripwire)
- Fewer than 4 axes scored
- Mode auto-picked without HITL confirmation prompt
- Output contains full goal distillation at triage stage (distillation happens after triage, not during)

## Example Output

**Triage Assessment**

| Axis | Score | Reasoning |
|---|---|---|
| Design ambiguity | some | Validation approach needs a decision (regex vs library vs HTML5 pattern) |
| Blast radius | local | One component, no public API change |
| Reversibility | trivial | Additive change, no migration |
| Existing test coverage | partial | Happy path tested, validation edge cases not covered |

**Proposed mode: `mini`**
Chain: `ide → aln(collapsed) → ral → qa`
No tripwire surfaces detected.

Confirm this mode? [human responds]
