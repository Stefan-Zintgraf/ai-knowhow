# Step 11 - Integration (registry as runtime source of truth)

**Status:** [ ]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

## Goal

Load `command_registry.json` at runtime in `german_commands.py` and `german_dictation_commands.py` (replace hardcoded `GERMAN_COMMANDS` / long `if/elif` chains where planned). Add alias matching. Update `test_corpus.py` `spoken` fields and `whisper_text.py` normalization as needed. Retire `record_real_voice.py` as the preferred workflow, but keep a compatibility wrapper until tests no longer import it.

Strategy reference: Section 9.3, Step 11.

## Hard gate before starting

Step 11 is blocked unless all of the following are already true:

- Phase 1 complete per [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) (including Step **5b** TTS closure / Pre-5 rework as applicable).
- Step 8 is green.
- Step 9 is green.
- Every runtime-bound registry row is `selected`.
- There are zero unresolved `needs_manual_redesign` rows.

Do not perform a partial registry/legacy runtime split.

## Tasks

1. Define a stable path to the registry (relative to module or user config).
2. Implement loader + alias resolution; keep parser pure-test seams intact.
3. Sync corpus `spoken` text to `selected_phrase` (and parametric variants).
4. Update `talon_cheat_sheet_ger.md` so listed phrases match finalized `selected_phrase` (and user-facing aliases) in `command_registry.json`.
5. Preserve the current test-facing interface of `record_real_voice.py` until the real-voice harness no longer imports it. A thin redirect/wrapper is acceptable.
6. Do not clear `recognition_xfail_real.json` in this step; that belongs to Step 12 once the real-voice fixture gate is green.

## Verifiable result

- [ ] Talon loads without error; representative manual smoke passes (see [manual_tests.md](ger_mode_cmds_plan2.manual_tests.md)).
- [ ] `python user/talon_german/ger_mode_cmds_test/test_text_level.py` full suite passes.
- [ ] `python user/talon_german/ger_mode_cmds_test/test_recognition_level.py --backend all` passes for the default TTS path.
- [ ] `talon_cheat_sheet_ger.md` matches integrated registry phrases (`selected_phrase` / aliases users should speak).
- [ ] Git: integration commit includes migration notes for users (old phrases as aliases where promised).
- [ ] If `record_real_voice.py` changed, the compatibility contract used by tests still works.

## Automated gate

```bash
python user/talon_german/ger_mode_cmds_test/test_text_level.py
python user/talon_german/ger_mode_cmds_test/test_recognition_level.py --backend all
```

## Notes for the agent

- The acceptance gate for runtime migration is phrases stable + Step 8 green + Step 9 green + zero unresolved rows.
- The real-voice suite and `recognition_xfail_real.json` are validated in Step 12, not here.
