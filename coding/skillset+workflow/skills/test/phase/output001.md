# Evaluation Criteria

## Requirements Tested
- PTM1 (coding_plan.md §PTM): `/phase` sole writer — writes phase_status.md on exit
- PTM2 (coding_plan.md §PTM): B-style — history row appended, Current block updated
- PTM8 (coding_plan.md §PTM / phases.md §5): exit guards pass — idea.md present, HITL ack recorded

## Pass Criteria
- Skill confirms `ide` exited for WI `7_add-dark-mode`
- `phase_status` updated to `exited` in Current block
- New history row for `ide` appended with `entered_at` and `exited_at`
- No rejection or error

## Fail Criteria
- Skill rejects exit when artifact present and HITL ack given
- History row not appended after successful exit
- `phase_status` remains `in-progress`

## Example Output

Phase `ide` exited for WI `7_add-dark-mode`.

Updated Current block: phase_status=exited, last_actor=human.

History row appended:
| ide | exited | 2026-05-25T14:00:00Z | 2026-05-25T14:30:00Z | human |

Next: run `/phase enter aln` or `/phase status`.
