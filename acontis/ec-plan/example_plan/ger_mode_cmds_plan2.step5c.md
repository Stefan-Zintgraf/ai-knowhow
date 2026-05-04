# Step 5c — Phase 1 input fingerprint (one-time automation)

**Status:** [x]

**Session rule:** Treat as **one** implementation session: deliver the artifacts below, run gates, commit, mark this file and the [overview](ger_mode_cmds_plan2.md) **Step 5c** row `[x]`, then **stop**. Do **not** start [Step 6](ger_mode_cmds_plan2.step6.md) in the same conversation — use a **fresh** session for Step 6. If **`needs_manual_redesign`** is still present anywhere in `command_registry.json` after upstream Phase 1 steps, **stop** after 5c (or after 5b if 5c is N/A); Step 6 remains blocked until those rows are cleared ([overview](ger_mode_cmds_plan2.md) Step 6 entry). ([implementation_prompt.md](implementation_prompt.md) stays unchanged; ordering is documented here and in the overview.)

---

## Goal

Add **objective** detection of when **`command_registry.json`** or **`synonym_table.json`** have changed since the last successful **Step 5b** (`tts-closure`) run, so implementers and agents can refresh Phase 1 (Steps 2–4–5–5b as needed) **before** treating the execution table’s next unchecked row (typically Step 6) as current work.

Also document **where** to edit phrases, **how** to re-run Phase 1 after edits, and the **re-validation ladder** when phrases change **after** later steps (including after Step 12). See [overview — Phrase changes at any project stage](ger_mode_cmds_plan2.md#phrase-changes-at-any-project-stage).

This step is **infrastructure** only: no `.talon` files or parser command modules unless a gate explicitly requires it.

**Registry file safety:** Do **not** use `git restore`, `git checkout --`, or any other command that **replaces or discards** the working copy of `user/talon_german/command_registry.json` (or reverts it to `HEAD`) to fix a **STALE** baseline or a bad checker run without the operator’s consent. Uncommitted registry edits (including deliberate phrase work) must not be thrown away to make automation green. **Stop**, preserve or stash changes, and **ask the user** before reverting tracked JSON.

---

## Tasks

1. **`phase1_inputs_baseline.json`** (under `user/talon_german/`) — store SHA-256 hashes of **canonical** JSON for `command_registry.json` and `synonym_table.json` (stable key order and separators so formatting-only edits do not flip the hash). Optional: `recorded_at`, `last_phase1_through: "5b"`.
2. **`check_phase1_inputs.py`** — recompute hashes, compare to baseline; print `OK` vs `STALE` (and which input diverged); exit **0** when OK, **non-zero** when STALE; optional `--json` for tooling.
3. **`generate_candidates.py`** — at successful end of `--phase tts-closure`, **rewrite** the baseline file so it matches the registry and synonym table **as committed after** Step 5b (including registry `tts_status` / `candidates` updates).
4. **Plan docs** — update [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) (entry precedence for STALE vs next step; lifecycle table if not already present) and [rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md) triggers (pointer to checker).
5. **`talon_cheat_sheet_ger.md`** — add a short section **“Changing test phrases and spoken phrases”**: where (`command_registry.json`, optional `synonym_table.json`), `validate_registry.py`, run `check_phase1_inputs.py`, Phase 1 refresh commands, pointer to overview for post–Step 6 / post–Step 12 follow-up.

---

## Verifiable result

- [x] Baseline + checker committed; `tts-closure` updates baseline on success.
- [x] `python user/talon_german/check_phase1_inputs.py` exits **0** immediately after a committed `--phase tts-closure` run that wrote the baseline.
- [x] `python user/talon_german/validate_registry.py` passes.
- [x] Overview Step 5c row and this file’s Status updated to `[x]`.
- [x] Cheat sheet section present per Tasks §5.

---

## Automated gate

```bash
python user/talon_german/validate_registry.py
python user/talon_german/check_phase1_inputs.py
```

(After implementation, the second command must report **OK** when inputs match the baseline.)

---

## N/A rule (skip this step)

Same spirit as [Pre-5](ger_mode_cmds_plan2.rework_pre_step5.md): if the repository **already** contains the Step 5c deliverables (merged from another branch or a template created after 5c landed), mark **Step 5c `[x]`** in the overview and this file, document **N/A** in the commit or a one-line note, and **do not** re-implement. Future tracks that start with 5c already complete proceed directly to [Step 6](ger_mode_cmds_plan2.step6.md) when it is next.

---

## Notes for the agent

- The checker validates **Phase 1 input files** vs the last 5b baseline; it does **not** replace re-validation of real-voice WAVs, `whisper.config`, Groq, corpus, or CI fixtures — see the [overview lifecycle table](ger_mode_cmds_plan2.md#phrase-changes-at-any-project-stage).
- Run **after** [Step 5b](ger_mode_cmds_plan2.step5b.md) is complete in the repo history; **before** starting Step 6 in a greenfield run.

---

## Related

- [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) — execution order and entry precedence  
- [ger_mode_cmds_plan2.step5b.md](ger_mode_cmds_plan2.step5b.md) — prerequisite closure phase  
