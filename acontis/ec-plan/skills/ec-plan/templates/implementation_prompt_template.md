You are continuing work on <task name / purpose>.

## Session protocol

1. Read these files in order:
   - `<plan folder>/<plan_name>.md` (overview — the next step is the first `[ ]` in the Status column, subject to any entry / ordering rules noted there).
   - The step file for that step (e.g. `<plan_name>.step<N>.md`).
   - `<plan folder>/<plan_name>.architecture.md` (remove if this plan has no architecture doc).
   - `<plan folder>/<plan_name>.test_strategy.md` (remove if this plan has no test strategy doc).
2. Run `git status` and `git log --oneline -10` to confirm prior steps are committed and the workspace is clean.
3. Implement **only** the current step. Run its automated gate. Commit all new/changed artifacts. Mark `[x]` in both the step file's `Status` and the overview's Status table. Then **stop**.

## Constraints

- All implementation outputs go under `<feature directory>`, **not** under the plan folder.
- Do not modify files the current step does not explicitly require.
- Do not skip or weaken the automated gate.
- Do not rewrite source-of-truth data / contracts to force a gate green; resolve via the documented escalation path or stop and ask.
- Do not run destructive VCS commands (`git restore`, `git checkout --`, hard reset) on tracked data without explicit user consent.
- Do not proceed to the next step.
- If something is unclear or blocked, stop and ask rather than guessing.

## Workspace

- Repository root: `<path>`
- Feature directory: `<path>`
- Plan docs (read-only unless updating status checkboxes): `<plan folder>/`
- Shell: `<bash | powershell | ...>`
- Runtime(s): `<Python / Node / ...>`
