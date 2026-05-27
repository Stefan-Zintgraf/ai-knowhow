# Evaluation Criteria

## Requirements Tested
- PTM6 (coding_plan.md §PTM): fresh-session UX — reads plan/ACTIVE, finds <none>, reports no active WI
- PTM9 (coding_plan.md §PTM / phases.md §5): status is read-only — no files written

## Pass Criteria
- Skill reports no active WI (equivalent to "ACTIVE=<none>" or "no active work item")
- Skill suggests a next action (e.g., run `/triage-idea`)
- No file is written or modified

## Fail Criteria
- Skill crashes or errors on missing plan/<WI>/ folder
- Skill fabricates a WI or phase state
- Any file is written

## Example Output

No active work item.
plan/ACTIVE = <none>

Run `/triage-idea` to start a new work item and enter the `ide` phase.
