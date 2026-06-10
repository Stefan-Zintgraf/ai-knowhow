# Evaluation Criteria

## Requirements Tested
- PTM7 (coding_plan.md §PTM / phases.md §5): enter mode-legal guard — direct-edit has no aln phase
- PH4.4 (phases.md §4): direct-edit chain is ide→ral→qa; aln not in it
- Idea8 (gr_idea.md): HITL-picked mode governs accessible phases; mode is binding

## Pass Criteria
- Skill rejects the enter with clear reason: `aln` not in `direct-edit` chain
- Skill names the correct next phase: `ral`
- No write to `phase_status.md` or `plan/ACTIVE`

## Fail Criteria
- Skill allows `aln` entry for a `direct-edit` WI
- Any file written before or after rejection
- Rejection message omits the mode or valid next phase

## Example Output

Rejected: `aln` is not part of the `direct-edit` chain.

direct-edit chain: ide → ral → qa

Valid next phase: `ral`. Run `/phase enter ral` to continue.
