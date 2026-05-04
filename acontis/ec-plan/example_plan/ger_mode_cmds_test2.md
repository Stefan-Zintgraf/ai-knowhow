# Test Strategy: German Mode Command Optimization (Plan 2)

## Goal

Define automated and interactive gates for optimizing German commands against `vosk-model-de-0.6`, without duplicating semantics outside `test_corpus.py`. Success is recognition match (phrase + aliases) on real audio, then both backends (Vosk + Groq) on the same WAVs, plus regression replay after any global setting change.

See [ger_mode_optim_strategy2.md](ger_mode_optim_strategy2.md) for rationale. See [ger_mode_cmds_architecture2.md](ger_mode_cmds_architecture2.md) for boundaries.

## Test layers

### Layer A - Vocabulary and registry integrity

- `vosk_vocabulary.txt` exists and is parseable.
- Every token in `current_phrase`, each candidate, and each `selected_phrase` appears in the vocabulary (or generation must not emit OOV).
- Registry rows reference corpus ids where applicable; no orphan ids.

Gate: automated check script or unit test invoked from Step 1-2 verification.

### Layer B - Phase 1 TTS screening (not acceptance)

- For all ~62 test phrases (every `test_phrases[]` entry): synthesize audio -> run Vosk -> record `recognized_as`, `exact_match`, `edit_distance` ([Step 4](ger_mode_cmds_plan2.step4.md)).
- For failing variants: candidates generated, TTS-screened, ranked (exact match > edit distance > shorter phrase) ([Step 5](ger_mode_cmds_plan2.step5.md)).
- Diversity: dedupe candidates with >50% token overlap.
- **Closure:** [Step 5b](ger_mode_cmds_plan2.step5b.md) — **every** test phrase index has an assigned phrase with **exact** TTS match under the Step 4 normalization rule, **or** the row is explicitly **`tts_status`: `needs_manual_redesign`**. Phase 1 is not complete until this holds (see [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) “Phase 1 exit”).

Gate: `tts_report.json` (Step 4); ranked candidates + `candidates_ready` (Step 5); closure report + `tts_closure_pass` / agreed **`tts_status`** (Step 5b; reports use `registry_tts_status`). Optional after [Step 5c](ger_mode_cmds_plan2.step5c.md): `check_phase1_inputs.py` OK vs `phase1_inputs_baseline.json`. Pre–Step 5 phrase churn: [rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md).

**Policy:** `test_phrases[]` must not be changed automatically to pass TTS or clear **`tts_status`** `needs_manual_redesign` — see [overview — Test phrase stability (manual redesign)](ger_mode_cmds_plan2.md#test-phrase-stability-manual-redesign).

### Layer C - Phase 2 real-voice selection

- **Entry:** Before Step 6, **`tts_status`** has no `needs_manual_redesign`, `manual_redesign_pass`, or `text_corpus_pass` rows (see [overview](ger_mode_cmds_plan2.md) Phase 1 exit item 5).
- Interactive `select_best_phrase.py` with **`MIN_TAKES = 2`** successful recognitions per accepted trial phrase, open-ended optional Phase B extras (finish with **`[o]`**), and stable/fragile confirmation when applicable (varied speed/volume).
- Persist every accepted take to `verify_audio/{command_id}_takeN.wav`.
- Resume and `--reset` behaviors must be manually smoke-tested once; automated tests can mock audio only where feasible.

Gate: Step 6 may **end** with rows marked **`real_voice_status`: `needs_manual_redesign`** (for example all real-voice candidates exhausted), but those rows are backlog only. Step 11 remains blocked until every runtime-bound row has **`real_voice_status`: `selected`**.

### Layer D - Global audio tuning + regression replay

- Grid search over saved WAVs (all takes, all commands) via existing `tune_agent.py` patterns.
- `verify_commands.py --batch-replay`: each command passes only if every take matches under current params and alias set.

Gate: zero regressions before Phase 3; if regressions, repair loop until batch replay is green.

### Layer E - Groq replay (Phase 3)

- `verify_groq.py`: same WAVs -> Groq -> same `check_match` logic.
- `groq_status: groq_pass` required for every selected command before integration.

Gate: 100% `groq_pass` on selected commands. No runtime integration with unresolved Groq failures.

### Layer F - Optional verification (Phase 4)

- Up to 3 fresh takes; skip / accept early allowed.
- Not a merge blocker; failures may trigger re-entry to Phase 2 via `--reset`.

Gate: none for integration; optional `verified` status in registry + `verification_log.json`.

### Layer G - Post-integration real-voice regression

- Promote stable WAVs to `ger_mode_cmds_test/audio/real/` (or agreed location) and wire `test_recognition_level.py` / offline eval.
- Target: `recognition_xfail_real.json` empty for Vosk real-voice entries.

Gate: only after the real-voice suite is green should `recognition_xfail_real.json` be reduced or cleared.

## Matching contract

Shared helper (conceptually):

```python
def check_match(recognized: str, phrase: str, aliases: list[str]) -> tuple[bool, str]:
    ...
```

Rules: exact, aliases, then justified fuzzy (for example `dass` -> `das`). Tests for `check_match` should live next to the implementation to avoid drift between Phase 2, batch replay, and Groq verification.

## Corpus synchronization

- Do not fork expected behavior: `test_corpus.py` stays the definition of what each command should do.
- After phrase finalization, update each entry's `spoken` to match `selected_phrase` (and parametric variants as two entries or two registry test rows).
- Text-level tests continue to run on normalized text as today; recognition tests run on audio.

## Coverage matrix

| Area | Must verify |
|------|-------------|
| Command mode | All `GERMAN_COMMANDS` patterns represented in registry |
| Dictation | All `parse_dictation_command()` branches represented |
| System | `_try_system_command()` entries (mode switch, backend switch, etc.) |
| Parametric | Singular and plural test phrase for each parametric pattern |
| Aliases | Harvested aliases round-trip through `check_match` |
| Regression | Batch replay after `whisper.config` or phantom-word list changes |
| Groq | Every take of every selected command |
| Real fixtures | Step 12 runs `test_recognition_level.py` against `audio/real` with `recognition_xfail_real.json` |

## Automation vs human

| Activity | Automated | Human |
|----------|-----------|-------|
| Registry + vocab extract | Yes | - |
| Synonym table | Validated automatically | Author entries |
| TTS screen | Yes | - |
| Candidate gen + rank | Yes | - |
| Speak phrases | - | Yes |
| Global tune + batch replay | Yes | - |
| Groq replay | Yes | - |
| Optional Phase 4 | Script | Speak / skip |

## Related documents

- [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) - step table and acceptance criteria
- [ger_mode_cmds_plan2.manual_tests.md](ger_mode_cmds_plan2.manual_tests.md) - live smoke after integration
- [ger_mode_optim_strategy2.md](ger_mode_optim_strategy2.md) - full procedural detail
