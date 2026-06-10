# Evaluation Criteria

## Requirements Tested
- PTM-close exited guard (coding_plan.md §PTM L133–L134): close refuses unless `phase_status` = `exited`
- PTM1 sole writer integrity (coding_plan.md §PTM): on rejection, no write to phase_status.md or plan/ACTIVE
- PTM2 (coding_plan.md §PTM): existing history rows preserved on rejection

## Pass Criteria
- Skill returns rejection signal of shape `status: rejected, reason: <msg naming current_phase and the in-progress/not-exited condition>` — e.g. `status: rejected, reason: current phase qa is in-progress, not exited`
- No write to `plan/7_add-dark-mode/phase_status.md` (Current block + history unchanged)
- No write to `plan/ACTIVE` (still `7_add-dark-mode`)
- Reason message identifies the current phase AND its phase_status

## Fail Criteria
- Skill returns `status: ok` or proceeds with the close
- `plan/ACTIVE` flipped to `<none>`
- History row appended
- Skill auto-exits the phase (close must NOT silently invoke `exit qa` to satisfy its own guard)
- Rejection reason omits `phase_status` value

## Example Output

Close rejected.

`status: rejected, reason: current phase qa is in-progress, not exited. Call /phase exit qa first (after required artifacts present and HITL ack), then /phase close.`

No changes written to `plan/7_add-dark-mode/phase_status.md` or `plan/ACTIVE`.
