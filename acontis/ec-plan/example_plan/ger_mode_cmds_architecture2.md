# Architecture: German Mode Command Optimization (Vosk Small Model)

## Goal

Make every German voice command work reliably with `vosk-model-de-0.6`, using real voice as the acceptance signal, while keeping automation as high as possible. Phrases must also pass Groq (`whisper-large-v3`) on replay of the same WAVs before integration.

This document is the structural counterpart to [ger_mode_optim_strategy2.md](ger_mode_optim_strategy2.md). It fixes boundaries between planning artifacts, scripts, the existing test corpus, and eventual runtime loading from `command_registry.json`.

## Problem boundary

- The small Vosk model has a hard vocabulary limit (`graph/words.txt`). Candidate phrases must be filtered so every token is in that list.
- TTS screens candidate quality cheaply; TTS pass does not accept a phrase. Real-voice selection requires at least **two** passing takes (`MIN_TAKES`); Step 6 then supports **open-ended** optional additional takes until the operator finishes Phase B with **`[o]`**.
- Global audio parameters (`energy_threshold`, `audio_gain`) are tuned after phrase selection on all saved WAVs, then validated by batch replay of every take.

## Pipeline overview

```text
Phase 1 (automated)
  extract vocabulary -> build registry -> TTS-screen all ~40 phrases
  -> generate/rank candidates (vocab-filtered) -> TTS-screen candidates
  -> Step 5b: TTS closure per test_phrase index (see plan2 step5b)
  -> Step 5c (one-time): Phase 1 input fingerprint + checker (see plan2 step5c)

Phase 2 (interactive)
  select_best_phrase.py: per command, multi-take real voice, alias harvest
  -> verify_audio/{command_id}_take*.wav + registry updates

  -> global param sweep (tune_agent-style) on all WAVs
  -> verify_commands.py --batch-replay (full regression; all takes must pass)

Phase 3 (automated)
  verify_groq.py: replay all Phase-2 WAVs through Groq; groq_status per command

Phase 4 (optional, anytime)
  verify_commands.py: fresh takes, skip/accept early; not an integration gate
```

## Single source of truth: `command_registry.json`

During optimization, the registry is the authoritative list of:

- stable `id` (aligned with `test_corpus.py` entry ids where the command maps 1:1)
- `mode`: `command` | `dictation` | `system`
- `action` / routing target (for example `edit.save`, parsed dictation kind)
- `current_phrase`, `candidates[]`, `selected_phrase`, `aliases[]`, **`tts_status`** (Phase 1 / TTS pipeline), **`real_voice_status`** (Phase 2: `none` → `selected`, or real-voice `needs_manual_redesign` backlog), optional **`real_voice_fragile`** (Step 6: human-assessed after optional no-matches), `groq_status`

**Plan 2 — Phase 1 (`tts_status`) flow (high level):** `pending` (after Step 1 bootstrap) → Step 4 sets **`tts_pass`** / **`tts_fail`** per row from current phrases → Step 5 sets **`candidates_ready`** when ranked candidates exist for failing variants → Step 5b sets **`tts_closure_pass`** when **every** `test_phrases[]` index has a TTS-exact assigned phrase (including promotion from prior **`needs_manual_redesign`** or **`manual_redesign_pass`** when a full closure pass succeeds), or **`needs_manual_redesign`** where closure is impossible. **`manual_redesign_pass`** may remain on rows until the next successful **`tts-closure`** run promotes them to **`tts_closure_pass`**. Do not use a single overloaded `status` field — always set/read `tts_status` vs `real_voice_status` explicitly.

**Phase 2 (`real_voice_status`):** Step 6 sets **`selected`** when real-voice selection succeeds (keep **`tts_status`: `tts_closure_pass`**). Real-voice failure / backlog uses **`real_voice_status`: `needs_manual_redesign`** without demoting **`tts_status`** when TTS was already OK.

**Step 6 entry:** Phase 2 starts only when **`tts_status`** has **no** `needs_manual_redesign`, **no** `manual_redesign_pass`, and **no** `text_corpus_pass` rows ([overview](ger_mode_cmds_plan2.md) Phase 1 exit).

Parametric patterns (for example `geh hoch N zeilen`) are one registry row but two test phrases: singular (`N=1`) and plural (`N=2`) wording. **Plan 2:** each index must pass TTS closure independently ([Step 5b](ger_mode_cmds_plan2.step5b.md)); row-level-only success is insufficient.

**Per-variant candidates:** If `candidates[]` is only a flat list, generation must still record which candidate applies to which **`test_phrase_index`** (parallel structure or nested objects). Otherwise Step 5b cannot prove per-variant closure.

**Test phrase stability:** `test_phrases[]` are inventory keys for coverage and Step 4 measurement; they are **not** auto-rewritten when TTS fails or when a row is flagged `needs_manual_redesign`. Resolve with candidates, synonyms, then explicit human registry edits — see [overview — Test phrase stability (manual redesign)](ger_mode_cmds_plan2.md#test-phrase-stability-manual-redesign).

Transition to runtime is late: after phrases stabilize, `german_commands.py` and `german_dictation_commands.py` may load commands from the registry instead of hardcoded dicts and long `if/elif` chains. That migration is Step 11 and is not required to start Phase 1.

## Module and script boundaries

Paths below are **`user/talon_german/<file>`** (same folder as `german_commands.py`).

| Artifact | Responsibility |
|----------|----------------|
| `command_registry.json` | All command definitions, `tts_status`, `real_voice_status`, candidates, aliases, Groq status |
| `vosk_vocabulary.txt` | Parsed from `vosk-model-de-0.6/graph/words.txt` |
| `synonym_table.json` | Curated rewrite rules; manual seed; vocab-validated before use |
| `generate_candidates.py` | Phase 1: registry import path, TTS batch, candidate generation/ranking; Step 5c: write `phase1_inputs_baseline.json` after `tts-closure` |
| `check_phase1_inputs.py` | Step 5c: compare canonical hashes of `command_registry.json` + `synonym_table.json` to baseline |
| `phase1_inputs_baseline.json` | Step 5c: committed SHA-256 snapshot after successful Step 5b |
| `select_best_phrase.py` | Phase 2: record, Vosk match, persist takes, resume, `--reset*` |
| `verify_groq.py` | Phase 3: batch Groq replay |
| `verify_commands.py` | Phase 4 optional + batch-replay regression (`--batch-replay`) |

Reuse existing infrastructure:

- `ger_mode_cmds_test/corpus_tts.py` (or equivalent) for TTS -> Vosk screening
- `user/talon_german/tune_agent.py` for grid search over `energy_threshold` x `audio_gain`
- `whisper_engine.py` / `whisper_worker.py` for the same preprocessing path as live Talon

New scripts should not bypass phantom-word handling or gain/threshold logic used in production.

### Compatibility rule for `record_real_voice.py`

`record_real_voice.py` is retired as the preferred recording workflow once plan2 scripts exist, but its test-facing interface must be preserved until the recognition harness no longer imports it. The safe migration path is:

1. Move any shared helpers to a neutral module if useful.
2. Keep `record_real_voice.py` as a thin compatibility wrapper during Step 11.
3. Remove the wrapper only in Step 12, after the real-voice recognition gate is green and imports have been updated.

## Matching and normalization

Recognition output is matched against `selected_phrase` / trial phrase plus `aliases` using shared logic:

- normalize (trim, lower, collapse spaces)
- exact phrase match
- alias match (including auto-harvested Vosk distortions)
- built-in homophone helper where justified (for example `dass` -> `das` for retroactive `das` commands)

Compatibility policy: when a spoken phrase changes, the plan must record whether the old phrase remains an alias, is dropped, or is transition-only.

## Corpus alignment

`test_corpus.py` remains semantic ground truth for expected routing and state. The registry must:

- reuse corpus `id` where one test entry maps to one command row
- keep `spoken` fields in the corpus in sync with `selected_phrase` after integration (Step 11)

Do not introduce a second competing semantics document.

**User-facing cheat sheet:** `talon_cheat_sheet_ger.md` (repository root) summarizes accepted phrases for quick reference. It is **derived documentation**: it must match `user/talon_german/command_registry.json` (and after Step 11, finalized `selected_phrase` / user-relevant aliases). When the registry’s spoken surface changes, update the cheat sheet in the same change set or immediately after — see [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) workspace conventions. After [Step 5c](ger_mode_cmds_plan2.step5c.md), include a short subsection on **how and where** to change phrases (registry paths, validation, Phase 1 refresh, pointer to the plan’s lifecycle table).

## File map (implementation deliverables)

Implementation artifacts below are under **`user/talon_german/`**. The plan docs live only in `user/talon_german/ger_mode_cmds_plan2/`.

| File | Role |
|------|------|
| `talon_cheat_sheet_ger.md` (repo root) | End-user phrase reference; keep in sync with `command_registry.json` |
| `command_registry.json` | Registry |
| `vosk_vocabulary.txt` | Extracted vocabulary |
| `synonym_table.json` | Synonym/rewrite seeds |
| `generate_candidates.py` | Phase 1 automation (+ Step 5c baseline hook) |
| `check_phase1_inputs.py` | Step 5c drift gate |
| `phase1_inputs_baseline.json` | Step 5c last-good input snapshot |
| `select_best_phrase.py` | Phase 2 interactive |
| `verify_groq.py` | Phase 3 |
| `verify_commands.py` | Phase 4 + batch replay |
| `verify_audio/` | Real-voice WAV fixtures |
| `verification_log.json` | Optional consolidated log output |
| `build_command_registry.py` | Step 1: (re)generate registry from inventory |
| `validate_registry.py` | Step 1: schema + parse gate for `command_registry.json` |

## WAV storage policy

`verify_audio/` WAVs are **committed to git**. This ensures batch replay (Steps 7–9), the regression gate, and Groq verification work on any checkout without re-recording.

After a microphone or PC change, re-record via `select_best_phrase.py --reset-all`, re-run Steps 7–9, and commit the new WAVs.

Step 12 promotes WAVs from `verify_audio/` to `ger_mode_cmds_test/audio/real/` for the CI/offline eval fixture set. Both directories are committed.

## Key decisions

| # | Question | Resolution |
|---|----------|------------|
| 1 | Exact optimization inventory? | Step 1 registry: **53** patterns, **62** test phrases (includes extended editing + chat newline); derived from `GERMAN_COMMANDS`, `parse_dictation_command()`, `_try_system_command()` + `build_command_registry.py`. |
| 2 | Phrase change vs alias? | Per-command row: document alias / drop / transition; prefer keeping old phrase as alias when feasible. |
| 3 | When does registry become runtime input? | Step 11 only, after phrases are stable, Step 8 is green, Step 9 is green, and there are zero unresolved `needs_manual_redesign` rows. |
| 4 | Historical vs active fixtures? | Pre-plan2 `audio/real/` and `recognition_xfail_real.json` are reference only until replaced; coverage is treated as unknown until Step 12. |
| 5 | Acceptance before integration? | `MIN_TAKES = 2` real-voice passes per command under fixed Phase-2 params; then global tune + batch replay all takes; then Groq pass on all takes. |
| 6 | Weak on Vosk, OK on Groq? | Not acceptable for integrated phrases in this track. Resolve the phrase or keep integration blocked. |

## Risk-driven constraints

- Vocabulary: reject any candidate with an OOV token.
- Collisions: no candidate may be a substring/prefix of another command or common dictation.
- Dictation false positives: prefer multi-word phrases; Phase 4 false-positive test where applicable.
- Runtime migration: do not mix registry-driven runtime commands with legacy fallbacks for unresolved rows.

## Rejected alternatives

| Option | Why rejected |
|--------|--------------|
| Accept phrases on TTS alone | acoustic mismatch vs real microphone/speaker |
| Per-command audio tuning during Phase 2 | overfits; breaks other commands |
| Skip Groq check | dual-backend requirement is explicit |
| Ignore batch replay after param changes | regressions would ship silently |
| Partial runtime migration with unresolved rows | undefined runtime behavior and high regression risk |
