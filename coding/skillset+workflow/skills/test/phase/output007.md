# Evaluation Criteria

## Requirements Tested
- G3.37 (guardrails.md §3.37): tripwire resolution records the human's explicit decision and clears the halt
- PTM1 (coding_plan.md §PTM): `/phase` sole writer — writes phase_status.md on resolve-tripwire
- PTM2 (coding_plan.md §PTM): B-style — history entry appended for resolution

## Pass Criteria
- Skill confirms tripwire resolved for WI `5_refactor-auth`
- `tripwire_halt` set to `false` in Current block
- `last_actor` set to `human`
- History entry appended recording the resolution reason
- Skill mentions updating the GH issue body with the resolution
- `blockers` cleared or updated to reflect resolution
- No rejection or error emitted

## Fail Criteria
- Skill rejects the resolve when tripwire is active and reason is provided
- `tripwire_halt` remains `true` after resolution
- No history entry for the resolution
- Resolution reason not recorded in history or on GH issue
- Skill silently clears tripwire without recording the decision

## Example Output

Tripwire halt resolved for WI `5_refactor-auth`.

Reason recorded: "Approved narrow edit: only touch auth token refresh logic, not full auth module. Scope confirmed with team lead."

Updated phase_status.md:
- tripwire_halt: false
- last_actor: human

History appended: 2026-05-24T16:15:00Z | resolve-tripwire | reason: Approved narrow edit...

GH issue #5 updated with resolution record.
