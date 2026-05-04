You are continuing work on the German voice command optimization pipeline for Talon.

## Session protocol

1. Read these files in order:
   - `user/talon_german/ger_mode_cmds_plan2/ger_mode_cmds_plan2.md` (overview — find which step is next by looking at the Status column: the first `[ ]` is your step)
   - The step file for that step (e.g. `ger_mode_cmds_plan2.step2.md`)
   - `user/talon_german/ger_mode_cmds_plan2/ger_mode_cmds_architecture2.md`
   - `user/talon_german/ger_mode_cmds_plan2/ger_mode_cmds_test2.md`
2. Run `git status` and `git log --oneline -10` to confirm prior steps are committed and the workspace is clean.
3. Implement **only** the current step. Run its automated gate. Commit all new/changed artifacts. Mark `[x]` in both the step file's Status and the overview's Status table. Then **stop**.

## Constraints

- All implementation outputs go under `user/talon_german/`, NOT under the plan folder.
- Do not modify existing `.talon` or `.py` command files unless the step explicitly requires it.
- **Do not automatically change `command_registry.json` `test_phrases[]`** (or otherwise rewrite inventory test strings) to fix TTS failure, closure gaps, or Phase 1 **`tts_status`** / **`needs_manual_redesign`**. Follow [Test phrase stability (manual redesign)](user/talon_german/ger_mode_cmds_plan2/ger_mode_cmds_plan2.md#test-phrase-stability-manual-redesign) in the Plan 2 overview: candidates and synonyms first; explicit human phrase edits only when the plan calls for that kind of inventory change. (**`real_voice_status`** is separate — Phase 2 backlog vs **`tts_status`** Phase 1.)
- Do not proceed to the next step.
- Do not skip the automated gate.
- If something is unclear or blocked, stop and ask rather than guessing.

## Workspace

- Repository root: `%APPDATA%/talon` (Windows)
- Feature directory: `user/talon_german/`
- Plan docs (read-only unless updating status checkboxes): `user/talon_german/ger_mode_cmds_plan2/`
- Shell: bash (Git Bash on Windows)
- Python is available in the path.

**Step 6 dry tests (mocked):** `python -m pytest user/talon_german/test_select_best_phrase_flow.py -v -m "not integration"` (Repo-Root). Optional TTS+Vosk-Kette: `-m integration`.
