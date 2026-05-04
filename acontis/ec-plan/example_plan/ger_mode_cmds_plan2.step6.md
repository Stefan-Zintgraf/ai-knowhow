# Step 6 - Real-voice selection (`select_best_phrase.py`)

**Status:** [ ]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

**Prerequisites:** [Step 5b](ger_mode_cmds_plan2.step5b.md) (and [Step 5c](ger_mode_cmds_plan2.step5c.md) when applicable) per [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) Phase 1 exit: **`command_registry.json` must contain no row with `tts_status` in `needs_manual_redesign`, `manual_redesign_pass`, or `text_corpus_pass`** before Step 6. (`text_corpus_pass` is set by the fast `iterate_registry_phrases.py` path after corpus-only success; run `iterate_registry_phrases.py --refresh-phase1` or the manual Phase 1 chain so **`tts-closure`** updates `tts_status` before real-voice work.) **`manual_redesign_pass` blocks Step 6** until a successful **`tts-closure`** run promotes the row to **`tts_closure_pass`**. If any row is still in those blocking states when you finish Step 5, 5b, or 5c, **stop** there (commit, new session later); do not start this step until Phase 1 clears every such row.

**User decision when manual redesign appears:** Phase 1 entry to Step 6 requires **no blocking `tts_status` values** (see Prerequisites). During Step 6, a row may still end with **`real_voice_status`: `needs_manual_redesign`** after real-voice selection exhausts candidates ([overview](ger_mode_cmds_plan2.md) acceptance criteria). In that situation — or if the operator is blocked on any command — **the user** decides what happens next: e.g. pause recording, return to Phase 1 (synonyms / candidates / explicit inventory edits per policy), accept a backlog row for later, or adjust strategy. **Agents and automation must not** “complete” Step 6 by reverting `command_registry.json`, rewriting `test_phrases[]`, or discarding the user’s working-tree edits to clear flags. **Stop** and let the user choose before continuing.

## Goal

Interactive script: for every registry command, record real audio with **`MIN_TAKES = 2`** successful Vosk matches per accepted trial phrase (Phase A), then an **open-ended** optional Phase B (extra takes until **`[o]`**). Persist WAVs to `verify_audio/{command_id}_takeN.wav` (or `{id}_tp{i}_takeN.wav`); update `selected_phrase`, `aliases` (auto-harvest), **`real_voice_status`: `selected`** (keep **`tts_status`: `tts_closure_pass`**). If Phase B had any optional no-match, the script asks **stable vs fragile** and may set optional boolean **`real_voice_fragile`** (human-assessed; omitted when stable). Support quit/resume (including mid–optional phase via `phase2_selection_checkpoint.json`), `--reset`, `--reset-file`, `--reset-all`.

Strategy reference: Section 5, Step 6.

## Tasks

1. Implement `select_best_phrase.py` flow as in the strategy (Phase A minimum takes; open-ended Phase B until **`[o]`**; English prompts).
2. Use shared `check_match()` with alias list and normalization.
3. Keep audio params fixed during selection. No per-command tuning.
4. **Before `MIN_TAKES`:** on no-match, **`[r]`** / **`[n]`** as today; **`[n]`** advances to the next ranked trial phrase for the variant.
5. **After `MIN_TAKES` (optional phase):** open-ended loop of extra takes until the operator finishes with **`[o]`** in the Phase B main menu; on optional no-match, **`[r]`** / **`[n]`** (delete all WAVs for this trial phrase) / **`[d]`** (finalize with passing takes only). If any optional no-match occurred in that Phase B, **`[s]`** / **`[f]`** stable vs fragile before writing the registry.
6. Automated tests (mocked I/O):  
   `python -m pytest user/talon_german/test_select_best_phrase_flow.py -v -m "not integration"`  
   Optional end-to-end audio check (Vosk + Edge TTS when deps/network allow):  
   `python -m pytest user/talon_german/test_select_best_phrase_flow.py -v -m integration`

## Verifiable result

- [x] Script runs end-to-end; resume after `[q]` restores partial state (`phase2_selection_checkpoint.json`).
- [x] `--reset` / `--reset-file` / `--reset-all` clears WAVs + relevant registry fields per the strategy.
- [ ] Operator — **entry**: registry has **no** blocking **`tts_status`** rows (see Prerequisites). **Exit**: every eligible row (`tts_closure_pass` + `real_voice_status` `none`) ends as **`real_voice_status`: `selected`** after recording, or **`real_voice_status`: `needs_manual_redesign`** only when real-voice selection exhausts all candidates during the session.
- [ ] Operator: at least two WAVs per selected command on disk; commit `verify_audio/` per the [architecture doc](ger_mode_cmds_architecture2.md).

## Automated gate

Manual primary gate (human speaks). Supplementary checks:

1. **Schema / entry (no microphone):**  
   `python user/talon_german/select_best_phrase.py --dry-run-schema`  
   Validates registry + closure inputs before recording.

2. **Workflow regression (pytest):** [`test_select_best_phrase_flow.py`](../test_select_best_phrase_flow.py) exercises `run_trial_phrase_workflow` with mocked I/O; optional integration test runs Edge TTS → WAV → Vosk when dependencies allow. Run from repo root:

```bash
python -m pytest user/talon_german/test_select_best_phrase_flow.py -v -m "not integration"
python -m pytest user/talon_german/test_select_best_phrase_flow.py -v -m integration
```

See the module docstring at the top of that file for purpose and when to run each mode.

Mark Step 6 complete only after the human selection pass is done or rows that still fail after real-voice passes are explicitly marked with **`real_voice_status`: `needs_manual_redesign`** with owner follow-up (not carried in from Phase 1 — entry prerequisite is zero blocking **`tts_status`** rows).

## Implementation landed (session artifact)

- `user/talon_german/select_best_phrase.py` — interactive recording, `--dry-run-schema`, `--reset*`; English prompts; checkpoint resume (including optional phase + fragile prompt); WAV naming `{id}_takeN.wav` or `{id}_tp{i}_takeN.wav` for multi-variant; optional `real_voice_fragile`.
- `user/talon_german/test_select_best_phrase_flow.py` — pytest: mocked workflow tests; optional `@pytest.mark.integration` TTS→Vosk chain.
- `user/talon_german/phrase_match.py` — shared `normalize` / `check_match` (strategy §8.2).
- `user/talon_german/verify_audio/.gitkeep` — output directory for committed WAVs.
- Automated gates: `--dry-run-schema` (above); pytest [`test_select_best_phrase_flow.py`](../test_select_best_phrase_flow.py) (above). Primary gate remains the operator recording pass.

Mark **Status** `[x]` in this file and the [overview](ger_mode_cmds_plan2.md) only after the Verifiable result checkboxes above are all satisfied (including operator recording and committing WAVs).

## Notes for the agent

- **Test phrases:** Do not rewrite `test_phrases[]` because real-voice selection is hard or a row is flagged — same policy as Phase 1: [Test phrase stability (manual redesign)](ger_mode_cmds_plan2.md#test-phrase-stability-manual-redesign).
- Alias harvest: only promote distortions seen consistently (for example 2+ takes).
- Keep UX identical between fresh run and resume.
- Conservative policy: **`real_voice_status`: `needs_manual_redesign`** assigned **during** Step 6 (candidates exhausted) is acceptable for closing Step 6, but it does **not** permit partial runtime integration in Step 11. Those rows must be resolved before runtime migration.
