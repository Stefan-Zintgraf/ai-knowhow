# Evaluation Criteria

## Requirements Tested
- PTM-close terminal-phase guard (coding_plan.md §PTM L133–L134): close refuses unless `current_phase` is the terminal legal phase for `mode`
- PTM7 mode-phase legality (coding_plan.md §PTM / phases.md §4): `full` mode's terminal phase is `qa`; `aln` is mid-sequence
- PTM1 sole writer integrity (coding_plan.md §PTM): on rejection, no write to phase_status.md or plan/ACTIVE

## Pass Criteria
- Skill returns rejection signal of shape `status: rejected, reason: <msg naming current_phase and mode and the not-terminal condition>` — e.g. `status: rejected, reason: current phase aln is not the terminal phase for mode full`
- No write to `plan/12_payment-gateway/phase_status.md` (history unchanged)
- No write to `plan/ACTIVE` (still `12_payment-gateway`)
- Reason message identifies BOTH the current phase (`aln`) AND the mode (`full`) so the human can diagnose

## Fail Criteria
- Skill returns `status: ok` or proceeds with the close
- `plan/ACTIVE` flipped to `<none>` (must remain `12_payment-gateway`)
- History row appended
- Rejection reason is generic (e.g. just "not allowed") without naming the current phase and mode
- Skill silently advances to a later phase or invokes another skill

## Example Output

Close rejected.

`status: rejected, reason: current phase aln is not the terminal phase for mode full (terminal phase is qa). Close is allowed only from the terminal phase exited cleanly.`

No changes written to `plan/12_payment-gateway/phase_status.md` or `plan/ACTIVE`.
