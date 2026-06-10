# Evaluation Criteria

## Requirements Tested
- Idea8: 4-axis triage must score all-low (no ambiguity, local scope, trivial reversibility, covered by existing tests) and propose `direct-edit` mode
- Idea4: Agent must present axis scores and proposed mode to human for confirmation (HITL pick mandatory)
- 3.29: Trivial task collapses phases — `direct-edit` chain is `ide → ral → qa`

## Pass Criteria
- Output contains a 4-axis scoring table or equivalent with values for: design ambiguity, blast radius, reversibility, existing test coverage
- All four axes scored at lowest level (none/local/trivial/covers-it or equivalent)
- Proposed mode is `direct-edit`
- Output includes an explicit prompt or question asking the human to confirm the mode choice
- No tripwire surfaces identified

## Fail Criteria
- Mode proposed is `mini` or `full` for this trivial typo fix
- Axis scores missing or incomplete (fewer than 4 axes scored)
- Mode auto-picked without asking human for confirmation
- Output contains goal distillation (Idea1 goals) — `direct-edit` skips distillation per Idea8

## Example Output

**Triage Assessment**

| Axis | Score | Reasoning |
|---|---|---|
| Design ambiguity | none | Single typo correction, no design decisions |
| Blast radius | local | One file, one string, no public API |
| Reversibility | trivial | One-line text change, trivially revertible |
| Existing test coverage | covers it | Login component has snapshot tests covering error messages |

**Proposed mode: `direct-edit`**
Chain: `ide → ral → qa`
No tripwire surfaces detected.

Confirm this mode? [human responds]
