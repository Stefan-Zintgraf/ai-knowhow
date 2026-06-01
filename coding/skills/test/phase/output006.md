# Evaluation Criteria

## Requirements Tested
- PTM8 (coding_plan.md §PTM / phases.md §5): exit artifact guard — idea.md absent → rejected

## Pass Criteria
- Skill rejects the exit with explicit reason: `idea.md` not found
- `phase_status.md` NOT updated (no write)
- Missing artifact named explicitly in output

## Fail Criteria
- Skill allows exit when idea.md absent
- Skill writes `phase_status: exited` despite missing artifact
- No diagnostic about the missing artifact

## Example Output

Rejected: cannot exit `ide` — required artifact missing.

Missing: `plan/9_redesign-onboarding/idea.md`

Run `/distill-idea` to produce the goal list, then retry `/phase exit ide`.
