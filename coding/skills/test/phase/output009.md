# Evaluation Criteria

## Requirements Tested
- PTM1 (coding_plan.md §PTM): `/phase` is sole writer — close writes phase_status.md AND plan/ACTIVE
- PTM5 (coding_plan.md §PTM): plan/ACTIVE flips from `<N>_<slug>` to `<none>` only via `/phase close`
- PTM-close (coding_plan.md §PTM L133–L134): close guards — phase_status=exited, current_phase is terminal-for-mode, tripwire_halt=false; all three pass here
- PTM2 (coding_plan.md §PTM): B-style file preserved — history row appended, prior rows unchanged

## Pass Criteria
- Skill returns success signal of shape `status: ok, closed: 7_add-dark-mode`
- Skill describes or produces a write to `plan/7_add-dark-mode/phase_status.md` appending a history row `<timestamp> | close | mini` at the top of `## History`
- Skill describes or produces a write to `plan/ACTIVE` containing the literal string `<none>`
- Existing history rows preserved
- Current block field `last_actor` updated to `human`
- `plan/7_add-dark-mode/` folder is NOT deleted (close ≠ folder retirement)

## Fail Criteria
- Skill emits `status: rejected` or `status: error` (all guards pass — qa is terminal for mini, exited cleanly, tripwire clear)
- `plan/ACTIVE` not written, or written with anything other than `<none>`
- History rows lost or overwritten
- Skill deletes `plan/7_add-dark-mode/` folder
- Skill calls another skill or attempts to update a GH issue

## Example Output

WI `7_add-dark-mode` closed.

Updated `plan/7_add-dark-mode/phase_status.md`:
- Current block: `last_actor: human`
- History prepended: `2026-05-26T11:00:00Z | close | mini`

Updated `plan/ACTIVE` → `<none>`.

Folder `plan/7_add-dark-mode/` retained (folder retirement is a separate ritual).
