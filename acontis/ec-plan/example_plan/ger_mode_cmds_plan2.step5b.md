# Step 5b — TTS closure (per test phrase)

**Status:** [x]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

---

## Goal

Close **Phase 1 TTS** so that **every** entry in **`test_phrases[]`** has at least one **assigned** surface phrase (keep the original wording **or** choose a ranked **candidate**) that **passes** the same TTS → Vosk screen as Step 4 (**normalized exact match** between expected and recognized text).

- **Per-variant (required):** Parametric rows (e.g. singular vs plural) are **not** satisfied at row-level only — **each** `test_phrases[]` index must have its own passing assignment.
- Rows that cannot close after bounded automated iteration are marked **`needs_manual_redesign`** (or equivalent) with an explicit reason — only when the playbook allows manual escape.
- **Do not rewrite `test_phrases[]`** to force closure. Closure assigns an **`assigned_phrase`** per index (original or ranked candidate). Unresolved cases get **`needs_manual_redesign`** until a **human** applies an explicit inventory edit per [Test phrase stability (manual redesign)](ger_mode_cmds_plan2.md#test-phrase-stability-manual-redesign).

**Registry file safety:** Do **not** use `git restore`, `git checkout --`, or any other command that **replaces or discards** the working copy of `user/talon_german/command_registry.json` (or reverts it to `HEAD`) to unwind a bad closure run or automation. That can **erase the operator’s uncommitted edits**. If recovery is needed, **stop**, preserve or stash the user’s changes first, and **ask the user** before resetting tracked files.

Strategy reference: Plan 2 supplements [ger_mode_optim_strategy2.md](ger_mode_optim_strategy2.md) §4.6–4.7; final Plan 2 state **supersedes** a deliverable where candidates remain TTS-false in production.

**Depends on:** [Step 5](ger_mode_cmds_plan2.step5.md) (`candidates_ready` / ranked candidates). Registry JSON may need **per–test-phrase** candidate binding when implemented (e.g. candidates keyed by `test_phrase_index`); see [ger_mode_cmds_architecture2.md](ger_mode_cmds_architecture2.md).

---

## Tasks

1. Implement or extend **`generate_candidates.py`** (or sibling) with a **`--phase tts-closure`** (or equivalent) that verifies per-index closure and updates registry **`tts_status`** (e.g. `tts_closure_pass` — see architecture doc).
2. Emit a machine-readable **closure report** (e.g. `tts_closure_report.json`) listing each `(registry id, test_phrase_index)` and its assigned phrase + `exact_match: true`.
3. Document escape: **`needs_manual_redesign`** when no vocab-valid phrase can be found or TTS cannot be closed automatically — **without** automatically changing `test_phrases[]` (see overview [Test phrase stability](ger_mode_cmds_plan2.md#test-phrase-stability-manual-redesign)).

---

## Verifiable result

- [x] Every `test_phrases[]` index has an assigned phrase with **exact** TTS match (same normalization as Step 4), **or** the row is explicitly flagged **`needs_manual_redesign`** with reason.
- [x] Report artifact committed; registry `tts_status` values updated.
- [x] Git: report + registry updates committed.

---

## Automated gate

```bash
python user/talon_german/generate_candidates.py --phase tts-closure
```

(Exact flag name may match implementation; must exit 0 when the closure job completes without tool failure — same convention as Step 4: individual phrase failures are reported, not necessarily a non-zero exit unless the tool errors.)

---

## Notes for the agent

- **TTS is still not real-voice acceptance** — Step 6+ remains required.
- Run **after** Step 5 and **before** Step 6.
- **Step 6 entry:** [Step 6](ger_mode_cmds_plan2.step6.md) must not start while any row remains `needs_manual_redesign`. If this step (or Step 5c afterward) leaves such rows in the registry, **end the session there**, commit, and resolve Phase 1 before opening a new session for Step 6 ([overview](ger_mode_cmds_plan2.md) Phase 1 exit).
