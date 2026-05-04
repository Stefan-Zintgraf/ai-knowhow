# Step 9 - Groq compatibility check

**Status:** [ ]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

**Prerequisites:** [Step 8](ger_mode_cmds_plan2.step8.md) batch-replay green (or project-agreed baseline). See [overview](ger_mode_cmds_plan2.md).

## Goal

Run `verify_groq.py`: for each `selected` command, transcribe every Phase-2 WAV with Groq (`whisper-large-v3`). Use the same `check_match` logic. Set `groq_status` to `groq_pass` / `groq_fail`. Integration requires 100% `groq_pass`.

Strategy reference: Section 7, Step 9.

## Tasks

1. Reuse `groq_utils.py` / existing backend hooks.
2. Log per-file transcript and match result.
3. Update registry `groq_status` field.
4. For failures: try alias; else consider alternate candidate from the Phase 1 list; else re-enter Step 6.

## Verifiable result

- [ ] All selected commands `groq_pass` on all takes.
- [ ] Git: script + registry Groq fields.

## Automated gate

```bash
python user/talon_german/verify_groq.py
```

Requires Groq credentials in the environment; fail fast if missing.

## Notes for the agent

- Treat every Groq failure as blocking until resolved.
