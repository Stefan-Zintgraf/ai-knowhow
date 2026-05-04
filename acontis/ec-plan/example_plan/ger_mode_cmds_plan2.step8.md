# Step 8 — Regression check and repair

**Status:** [ ]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

**Prerequisites:** [Step 7](ger_mode_cmds_plan2.step7.md) (or current `whisper.config` baseline) and Phase 2 WAVs from [Step 6](ger_mode_cmds_plan2.step6.md). Execution order: [overview](ger_mode_cmds_plan2.md).

---

## Goal

Implement and run **`verify_commands.py --batch-replay`**: replay **every** saved take through Vosk with **current** `whisper.config` and alias tables. A command **passes** only if **all** takes match. If any regress: log, re-enter selection for affected commands (Step 6), optionally re-run Step 7, repeat until **zero regressions**.

Strategy reference: §5.11, §10 Step 8.

---

## Tasks

1. Implement batch replay mode (no microphone).

2. Per-command output: PASS / REGRESSED with per-take transcripts.

3. Document repair loop: alias first, next candidate, re-record.

4. Integrate with CI or `run_offline_eval.ps1` if appropriate (optional in this step).

---

## Verifiable result

- [ ] `verify_commands.py --batch-replay` exits 0 with all commands full take pass.
- [ ] Regression log format is machine-readable or grep-friendly.
- [ ] Repair iterations documented in commit messages or `OPTIMIZATION_LOG.md` only if user wants — default: registry git history.
- [ ] Git: verifier script + green state registry/config.

---

## Automated gate

```bash
python user/talon_german/verify_commands.py --batch-replay
```

---

## Notes for the agent

- This gate must run after **any** future change to phantom words, aliases, or audio params.
