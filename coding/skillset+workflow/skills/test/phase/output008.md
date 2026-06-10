# Evaluation Criteria

## Requirements Tested
- PTM7 (coding_plan.md §PTM / phases.md §5): enter tripwire-halt guard — entry refused when tripwire_halt=true
- G3.37 (guardrails.md §3.37): tripwire blocks forward progress until human resolves

## Pass Criteria
- Skill rejects the enter with explicit reason: tripwire halt is active
- Rejection message mentions `/phase resolve-tripwire` as the resolution path
- No write to `phase_status.md` or `plan/ACTIVE`
- `current_phase` remains `aln`, not updated to `ral`

## Fail Criteria
- Skill allows entry to `ral` while tripwire is active
- Any file written before or after rejection
- Rejection message omits the tripwire reason or resolution path
- Skill silently clears tripwire and allows entry

## Example Output

Rejected: tripwire halt active — cannot enter `ral`.

Blocker: auth module scope exceeds mini mode.

Call `/phase resolve-tripwire <reason>` to clear the halt before entering any phase.
