# Evaluation Criteria

## Requirements Tested
- PTM1 (coding_plan.md §PTM): `/phase` is sole writer — skill writes phase_status.md, no delegation
- PTM2 (coding_plan.md §PTM): B-style file preserved — Current block updated, history row kept
- PTM3 (coding_plan.md §PTM): all required fields present in updated Current block
- PTM5 (coding_plan.md §PTM): plan/ACTIVE unchanged (WI already active)
- PTM7 (coding_plan.md §PTM / phases.md §5): all enter guards pass — mode `mini` legal for `aln`, `ide` exited cleanly, tripwire_halt=false

## Pass Criteria
- Skill confirms entering phase `aln` for WI `7_add-dark-mode`
- Describes or produces write to phase_status.md: `current_phase: aln`, `phase_status: in-progress`
- Existing `ide` history row preserved
- `plan/ACTIVE` not changed
- No rejection or error emitted
- `mode: mini` preserved in Current block

## Fail Criteria
- Skill rejects the enter when all guards should pass
- `current_phase` not updated to `aln`
- `ide` history row lost or overwritten
- Any required Current block field missing after update

## Example Output

Phase `aln` entered for WI `7_add-dark-mode`.

Updated `plan/7_add-dark-mode/phase_status.md` Current block:
- current_phase: aln
- phase_status: in-progress
- entered_at: 2026-05-26T09:00:00Z
- mode: mini (unchanged)
- tripwire_halt: false

History: ide row preserved. Ready to run `/align-concept`.
