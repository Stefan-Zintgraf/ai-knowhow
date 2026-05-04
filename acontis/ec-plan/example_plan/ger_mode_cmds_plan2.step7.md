# Step 7 - Global audio parameter tuning

**Status:** [ ]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

**Prerequisites:** [Step 6](ger_mode_cmds_plan2.step6.md) complete with `verify_audio/` populated; Phase 1 closed per [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) (Steps 5b + Pre-5 as applicable).

## Goal

After all phrases are `selected`, run a grid search over `energy_threshold` x `audio_gain` replaying all WAVs from `verify_audio/` through Vosk. Score: count commands where every take matches. Write optimal values to `whisper.config`.

Strategy reference: Section 5.10, Step 7. Reuse existing `tune_agent.py` patterns.

## `whisper.config` target keys

The tuning step writes to the existing `talon_german/whisper.config` (JSON). The two keys under optimization are top-level:

```json
{
  "energy_threshold": 0.028,
  "audio_gain": 7.0
}
```

See `whisper_config.py` for the loader and validation. Do not add new top-level keys; only update `energy_threshold` and `audio_gain`.

## Tasks

1. Collect all `*_take*.wav` paths grouped by `command_id`.
2. Integrate or invoke the existing tune infrastructure (`tune_agent.py`); document grid bounds in script or config.
3. Persist winning parameters to `whisper.config` (`energy_threshold`, `audio_gain`).
4. Write a separate tuning report or log with timestamp and score summary. Do not rely on comments in `whisper.config`; it is JSON.

## Verifiable result

- [ ] Tuning uses all takes; a command fails the score if any take mismatches.
- [ ] Best params recorded and reproducible from the tuning log.
- [ ] `whisper.config` updated and committed.
- [ ] Git: tuning script changes + config if applicable.

## Automated gate

```bash
python user/talon_german/tune_agent.py
# or a plan2 wrapper that calls the shared API; document the exact command in the commit
```

## Notes for the agent

- Expect regressions after tuning; Step 8 exists to catch them.
- If tuning cannot improve the corpus, document revert to pre-tune defaults.
