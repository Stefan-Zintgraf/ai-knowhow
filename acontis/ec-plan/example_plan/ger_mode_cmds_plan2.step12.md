# Step 12 - Regression gate (fixtures + CI / offline eval)

**Status:** [ ]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

**Prerequisites:** [Step 11](ger_mode_cmds_plan2.step11.md) integration complete or project-agreed baseline; see [overview](ger_mode_cmds_plan2.md).

## Goal

Promote optimized `verify_audio/` WAVs to the canonical real-voice fixture location (for example `ger_mode_cmds_test/audio/real/<corpus_id>.wav`). Ensure `test_recognition_level.py` and `run_offline_eval.ps1` (or CI) run against them. Target: `recognition_xfail_real.json` empty for Vosk.

## Tasks

1. Map `command_id` -> corpus `id`; copy/rename with documented convention.
2. Update the test harness to prefer new fixtures where ids align.
3. Run offline eval; record the log under `tune_lab/eval/runs/` if that is project convention.
4. Remove stale `recognition_xfail_real.json` entries only with proof from the real-voice suite / eval log.
5. If Step 11 kept `record_real_voice.py` as a compatibility wrapper, remove that wrapper only after the harness no longer imports it.

## Verifiable result

- [ ] Every corpus entry that expects real-voice coverage has a non-empty WAV (or explicit exclusion list).
- [ ] `test_recognition_level.py` passes against the real-voice fixture directory.
- [ ] `recognition_xfail_real.json` has no stale entries for fixed commands.
- [ ] Any Step 11 compatibility wrapper around `record_real_voice.py` is removed only after imports are updated and tests are green.
- [ ] Git: promoted fixtures committed to `ger_mode_cmds_test/audio/real/`.

## Automated gate

```bash
python user/talon_german/ger_mode_cmds_test/test_recognition_level.py --audio-dir audio/real --xfail user/talon_german/ger_mode_cmds_test/recognition_xfail_real.json --backend all
# Optional:
powershell -File user/talon_german/tune_lab/run_offline_eval.ps1
```

**Note:** `test_recognition_level.py` already supports `--audio-dir`, `--xfail`, and `--backend` flags. No harness extension should be needed for this gate.

## Notes for the agent

- WAVs are committed directly (no Git LFS). Follow existing `ger_mode_cmds_test` conventions for fixture naming.
- This is the step that proves real fixtures, clears `recognition_xfail_real.json`, and finishes the retirement of old recording-path compatibility.
