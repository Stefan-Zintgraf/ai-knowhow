# Step 10 — Optional verification pass (`verify_commands.py`)

**Status:** [ ]

**Session rule:** Complete this step only if the user wants Phase 4 artifacts; otherwise mark N/A and skip `[x]` in the main plan table or add a note “optional skipped”.

**Prerequisites:** [Step 9](ger_mode_cmds_plan2.step9.md) Groq gate per project rules. Optional step — see [overview](ger_mode_cmds_plan2.md).

---

## Goal

Optional interactive **`verify_commands.py`** session: up to **3** fresh takes per command; user may **skip**, **accept early**, or **quit** with resume. Updates optional **`verified`** status and **`verification_log.json`**. **Not** a blocker for Step 11.

Strategy reference: §8, §10 Step 10.

---

## Tasks

1. Implement Phase 4 loop per strategy §8.1.

2. False-positive spot checks: speak command-like phrases in dictation context where strategy calls for it (document cases).

3. Append to `verification_log.json` structure §8.3.

---

## Verifiable result

- [ ] Script runs; skip leaves `selected` unchanged.
- [ ] `verification_failed` path documented for follow-up.
- [ ] Git: optional log + verify WAV naming convention if stored.

---

## Automated gate

```bash
python user/talon_german/verify_commands.py --verify
```

The `--verify` flag runs the Phase 4 interactive loop (up to 3 fresh takes per command, skip/accept early). This is distinct from `--batch-replay` (automated regression, no mic) and `--only-failed` (retry only `verification_failed` rows). All three flags must be implemented in `verify_commands.py`.

Primary verification remains **manual**; gate = script exits cleanly after completed session or `[q]`.

---

## Notes for the agent

- Batch replay from §8.5 reuses `--batch-replay` with extended fixture set if verify WAVs are kept.
