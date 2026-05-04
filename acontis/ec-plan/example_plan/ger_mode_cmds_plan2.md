# German Mode Commands - Optimization Plan (Plan 2)

## Purpose

Execute the four-phase pipeline in [ger_mode_optim_strategy2.md](ger_mode_optim_strategy2.md): vocabulary-bound candidate generation, real-voice selection with multi-take evidence, global audio tuning with regression replay, Groq compatibility on the same WAVs, optional re-verification, then code integration with `command_registry.json` as the eventual single source of truth.

This plan is an execution contract alongside:

- [Architecture](ger_mode_cmds_architecture2.md) - boundaries, registry, matching, file map
- [Test strategy](ger_mode_cmds_test2.md) - gates per layer (TTS, real voice, batch replay, Groq)

### Session rule

Each step is implemented in its own fresh session when doing implementation work (one step = one conversation).

- On entry: read this overview, the architecture doc, the test strategy doc, and the current step file. Inspect git status so you know what is already done.
- On completion: run that step's automated or documented gate, commit when code/artifacts change, mark the checkbox, then stop.

Planning artifacts in this folder may be edited in one session; implementation still follows the session rule per step.

**Entry — Phase 1 input drift (after [Step 5c](ger_mode_cmds_plan2.step5c.md) is implemented):** Before treating the execution table’s first `[ ]` as the next implementation step, run `python user/talon_german/check_phase1_inputs.py` when that script exists. If it reports **STALE**, reconcile Phase 1 first (see [rework_pre_step5](ger_mode_cmds_plan2.rework_pre_step5.md) and the refresh sequence under [Phrase changes at any project stage](#phrase-changes-at-any-project-stage)) — do **not** skip ahead to Step 6+ on stale Phase 1 inputs.

**Pre–Step 5 (ordering, without changing [implementation_prompt.md](implementation_prompt.md)):** The first unchecked row in the table below is the next work item **subject to** the entry rule above and **Step 5c** ordering below. When **[Pre-5](ger_mode_cmds_plan2.rework_pre_step5.md)** is unchecked, complete that playbook **or** mark it `[x]` per its **N/A** rule **before** starting Step 5. The Pre-5 session **stops** after commit; **Step 5** starts in a **new** session. Same pattern between Step 5 and **Step 5b** (separate sessions).

**Step 5c (ordering):** When **[5c](ger_mode_cmds_plan2.step5c.md)** is unchecked, complete that step **or** mark it `[x]` per its **N/A** rule **before** starting Step 6. The 5c session **stops** after commit; **Step 6** starts in a **new** session. Step 5c is a **one-time** automation pass (Phase 1 input fingerprint); greenfield clones where 5c is already merged treat it like Pre-5 N/A.

**Step 6 entry:** Do **not** start Step 6 while **`command_registry.json` has any row with `tts_status` in `needs_manual_redesign`, `manual_redesign_pass`, or `text_corpus_pass`** ([Phase 1 exit](#phase-1-exit-before-step-6--real-voice) item 5). If Phase 1 still has any of those after **[Step 5](ger_mode_cmds_plan2.step5.md)**, **[Step 5b](ger_mode_cmds_plan2.step5b.md)**, or **[Step 5c](ger_mode_cmds_plan2.step5c.md)** (whichever was last in your session), **stop there**, commit, and resolve the rows before a **new** session begins Step 6.

**Step 6 — manual redesign during or after recording:** If real-voice selection yields new **`real_voice_status`: `needs_manual_redesign`** backlog rows or the operator cannot proceed, **the user** decides whether to continue, pause, or re-enter Phase 1 — agents must not revert the registry or rewrite inventory strings to force Step 6 “done”. See [Step 6](ger_mode_cmds_plan2.step6.md).

## Workspace conventions

- Repository root: `%APPDATA%/talon`
- Feature directory: `user/talon_german`
- This plan (documentation only): `user/talon_german/ger_mode_cmds_plan2/`
- **Implementation outputs (scripts, JSON, vocab, audio, configs):** `user/talon_german/` — not under `ger_mode_cmds_plan2/`. Example: `user/talon_german/command_registry.json`, `user/talon_german/build_command_registry.py`, `user/talon_german/validate_registry.py`.
- **User-facing phrase list (repo root):** `talon_cheat_sheet_ger.md` — quick reference for German mode; must stay aligned with `user/talon_german/command_registry.json` (`current_phrase` during optimization; `selected_phrase` and documented aliases after integration). Update when registry phrases change materially: at minimum after Step 1 (bootstrap) and Step 11 (final phrases), and whenever a step changes spoken wording users rely on. After [Step 5c](ger_mode_cmds_plan2.step5c.md), the cheat sheet must include a short **“Changing test phrases and spoken phrases”** section (where to edit, validation, Phase 1 refresh, pointer to [Phrase changes at any project stage](#phrase-changes-at-any-project-stage)).
- Existing tests and corpus: `user/talon_german/ger_mode_cmds_test/`
- Strategy reference: [ger_mode_optim_strategy2.md](ger_mode_optim_strategy2.md)

### Clarification on strategy references

The strategy file remains read-only. Where it contains stale step numbering or wording that conflicts with this plan, this plan and the step files are authoritative for execution.

## Acceptance criteria

The optimization track is complete for integration when all of the following hold:

1. Inventory: **53** command patterns and **62** test phrases derived from code (`GERMAN_COMMANDS`, `parse_dictation_command()`, `_try_system_command()`, plus the `schreib` prefix path), with parametric coverage and extended editing/chat phrases, recorded in `user/talon_german/command_registry.json`.
2. Vocabulary: all accepted spoken phrases are fully in-vocabulary for `vosk-model-de-0.6` (per `words.txt`).
3. Real voice: every runtime-bound command reaches **`real_voice_status`: `selected`** with at least **`MIN_TAKES = 2`** passing takes saved under `verify_audio/` (Step 6 also supports **open-ended** optional extra takes after the minimum until **`[o]`**, and optional boolean **`real_voice_fragile`** when the operator confirms fragility after optional no-matches). **Step 6 does not run** until Phase 1 has **no** blocking `tts_status` values (`needs_manual_redesign`, `manual_redesign_pass`, `text_corpus_pass`). **Before Step 11**, every runtime-bound row must be **`real_voice_status`: `selected`** or explicitly out of scope; unresolved **`real_voice_status`: `needs_manual_redesign`** blocks later pipeline steps. During Step 6, rows may still land in real-voice backlog if selection exhausts candidates; those block Step 7+ until resolved.
4. Global audio: `energy_threshold` and `audio_gain` chosen by replay over all takes; `verify_commands.py --batch-replay` is green.
5. Groq: `verify_groq.py` reports `groq_pass` for every selected command on all takes.
6. Corpus: `test_corpus.py` `spoken` fields updated to match final phrases before merge.
7. Real-fixture gate: `recognition_xfail_real.json` is only updated when the Step 12 real-voice fixture gate is green.
8. Integration (Step 11): parser/command modules load from registry + alias matching; full automated suites pass.

Phase 4 (`verified` status) is optional and not a blocker for Step 11.

### Phase 1 exit (before Step 6 / real voice)

The following must hold before starting **Phase 2** (interactive real-voice selection):

1. **Per test phrase:** For every index in each row’s **`test_phrases[]`**, there is an assigned surface phrase (original or candidate) that passes the **Step 4** TTS → Vosk screen (normalized exact match). Parametric rows require a passing assignment **per variant**, not only row-level.
2. **Steps 5 + 5b:** [Step 5](ger_mode_cmds_plan2.step5.md) produces ranked, vocab-valid candidates for failing variants; [Step 5b](ger_mode_cmds_plan2.step5b.md) closes TTS so every variant is covered or explicitly flagged **`needs_manual_redesign`** (allowed as an intermediate outcome while iterating closure).
3. **Rework:** If phrase inventory or Step 4 outputs were revised after earlier steps, [Pre-5 rework](ger_mode_cmds_plan2.rework_pre_step5.md) was satisfied or marked N/A before Step 5.
4. **Step 5c (optional but recommended once implemented):** [Phase 1 input fingerprint](ger_mode_cmds_plan2.step5c.md) is present so manual registry / synonym edits can be detected before Phase 2; mark N/A if the repo already includes 5c.
5. **Step 6 entry — Phase 1 `tts_status` clear:** Before starting [Step 6](ger_mode_cmds_plan2.step6.md), **`command_registry.json` must contain no row whose `tts_status` is `needs_manual_redesign`, `manual_redesign_pass`, or `text_corpus_pass`** (`text_corpus_pass` is the corpus-only marker from `iterate_registry_phrases.py` — finish Phase 1 with **`tts-closure`** via `iterate_registry_phrases.py --refresh-phase1` or the manual chain). **`manual_redesign_pass`** is a Step-6-blocking TTS state until a successful **`tts-closure`** run promotes the row to **`tts_closure_pass`**. Resolve escapes by **synonym and ranked-candidate work first** ([Step 5](ger_mode_cmds_plan2.step5.md) / [Step 5b](ger_mode_cmds_plan2.step5b.md)); only then, if still stuck, follow **[Test phrase stability (manual redesign)](#test-phrase-stability-manual-redesign)** for *explicit* inventory edits. Re-run Steps 4–5–5b until every variant has TTS-exact closure with **`tts_status`: `tts_closure_pass`** (and **`real_voice_status`: `none`** for not-yet-recorded commands). Only then begin real-voice selection.

### Phrase changes at any project stage

Authoritative edits to spoken surface forms use **`user/talon_german/command_registry.json`** (`test_phrases`, `current_phrase`, optional `candidates`) and, for generation seeds, **`user/talon_german/synonym_table.json`**. Reasons such as unpleasant wording in daily use do not change *where* to edit.

### Test phrase stability (manual redesign)

**Do not change `test_phrases[]` automatically** — not as a script default, not as a shortcut when Step 4 fails, not to “fix” closure or clear `needs_manual_redesign`, and not because an agent or tool suggests a different wording.

**Allowed resolution order when a variant is stuck:**

1. **Ranked candidates** (Step 5): assign a passing surface from the candidate list while **keeping** the original `test_phrases[]` entry as the variant key (closure maps the index to `assigned_phrase`, which may differ from the literal test string — see Step 5b).
2. **`synonym_table.json`** and generator seeds: broaden or tune generation without rewriting inventory strings.
3. **`needs_manual_redesign`:** flag the row for a **human** decision with a recorded reason.
4. **Explicit `test_phrases[]` / `current_phrase` edits** only as a **deliberate product/inventory change**: same constraints as any phrase edit (parser semantics, [Step 1](ger_mode_cmds_plan2.step1.md) / `test_corpus.py` / `talon_cheat_sheet_ger.md` alignment when those apply, then Phase 1 refresh per the table below). Treat this like changing a API contract, not like retry-until-green.

Automation and implementation sessions **must not** silently rewrite `test_phrases[]` to bypass TTS or manual redesign.

**Working-tree safety (Steps 5–5c, tooling, agents):** Do **not** run `git restore`, `git checkout --`, or similar on `user/talon_german/command_registry.json` (or other Phase 1 JSON) to recover from a failed gate or script — that can **discard the operator’s uncommitted edits**. If a reset is considered, **stop**, preserve the user’s changes (e.g. stash or copy), and obtain **explicit user consent** before reverting tracked files. See [Step 5](ger_mode_cmds_plan2.step5.md), [Step 5b](ger_mode_cmds_plan2.step5b.md), and [Step 5c](ger_mode_cmds_plan2.step5c.md) for the same rule.

**What the Phase 1 checker does (after Step 5c lands):** `check_phase1_inputs.py` only tests whether those inputs still match the **last Step 5b** baseline. It does **not** validate real-voice WAVs, tuning, Groq, corpus text, or CI fixtures.

| Project state when you edit phrases | Minimum follow-up (in addition to `validate_registry.py`) |
|-------------------------------------|------------------------------------------------------------|
| Through Step 5b only | Phase 1 refresh: Steps 2–3 as needed → 4 → 5 → 5b; baseline updates at end of 5b when 5c is implemented. |
| After Step 6 (`verify_audio/`) | Phase 1 refresh for changed rows **plus** new real-voice takes for affected commands (see Step 6; superseded phrases invalidate old WAVs as evidence). |
| After Step 7 | Re-run global tune when the WAV set or phrases change materially (Step 7 doc). |
| After Step 8 | `verify_commands.py --batch-replay` green on relevant takes. |
| After Step 9 | `verify_groq.py` green for affected commands. |
| After Step 11 | Corpus `spoken` fields, runtime alignment, `talon_cheat_sheet_ger.md` per plan. |
| After Step 12 (promoted fixtures, `recognition_xfail_real.json`) | Re-promote or replace fixtures per Step 12; harness green before shrinking xfails. |

## Key deliverables

Paths below are under `user/talon_german/` unless noted.

| File | Created in | Role |
|------|------------|------|
| `talon_cheat_sheet_ger.md` | Step 1 (bootstrap) + Step 11 (integration); revise when phrases change | Repo root; user phrase quick reference aligned with `command_registry.json` |
| `command_registry.json` | Step 1 (skeleton) -> updated 1-10 | Single source of truth for phrases, candidates, aliases, `tts_status`, `real_voice_status` |
| `vosk_vocabulary.txt` | Step 2 | Hard vocabulary boundary |
| `synonym_table.json` | Step 3 | Manual seed for candidate generation |
| `generate_candidates.py` | Steps 4–5b; Step 5c extends | TTS screen; candidate gen/rank (Step 5); TTS closure (Step 5b); baseline write (Step 5c) |
| `check_phase1_inputs.py` | Step 5c | Compare live hashes to `phase1_inputs_baseline.json` |
| `phase1_inputs_baseline.json` | Step 5c | Last committed SHA-256 snapshot of canonical registry + synonym JSON |
| `tts_report.json` | Step 4 | TTS evaluation for current phrases |
| `tts_closure_report.json` (or equivalent) | Step 5b | Per–test-phrase TTS closure evidence |
| [rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md) | Before Step 5 when triggers apply | Ordered redo of Steps 2–4 after phrase/inventory churn |
| `select_best_phrase.py` | Step 6 | Interactive real-voice selection, resume, `--reset*` |
| `whisper.config` | Step 7 | Globally tuned params written here |
| `verify_commands.py` | Steps 6-8, 10 | Batch replay + optional Phase 4 |
| `verify_groq.py` | Step 9 | Groq batch replay |
| `verify_audio/` | Step 6+ | Regression WAV fixtures |
| `verification_log.json` | Step 10 (optional) | Phase 4 / combined logs |

## Execution order

| Step | File | Strategy section | Focus | Gate | Status |
|------|------|------------------|-------|------|--------|
| 1 | [step1](ger_mode_cmds_plan2.step1.md) | §4.2–4.3 | Build `command_registry.json` from code (53 patterns, 62 test phrases; full branch coverage) | Registry JSON validates; ids align with corpus where 1:1 | [x] |
| 2 | [step2](ger_mode_cmds_plan2.step2.md) | §4.2 | Extract `vosk_vocabulary.txt`; flag OOV tokens in registry phrases | Vocab file exists; OOV report | [x] |
| 3 | [step3](ger_mode_cmds_plan2.step3.md) | §4.5, §6.2 | Author `synonym_table.json`; vocab-validate entries | Validator green | [x] |
| 4 | [step4](ger_mode_cmds_plan2.step4.md) | §4.4 | TTS pre-screen all current phrases -> `tts_pass` / `tts_fail` | Summary report; registry statuses | [x] |
| Pre-5 | [rework_pre_step5](ger_mode_cmds_plan2.rework_pre_step5.md) | — | When triggers apply: redo Steps 2–4 in order; or mark N/A | Per rework doc; then fresh session | [x] |
| 5 | [step5](ger_mode_cmds_plan2.step5.md) | §4.5–4.7 | Generate, TTS-screen, rank candidates **per failing test phrase** | `candidates_ready`; ranked arrays | [x] |
| 5b | [step5b](ger_mode_cmds_plan2.step5b.md) | §4.6–4.7 (Plan 2) | TTS closure: every `test_phrases[]` index has exact TTS match or `needs_manual_redesign` | `--phase tts-closure`; closure report | [x] |
| 5c | [step5c](ger_mode_cmds_plan2.step5c.md) | — | One-time: Phase 1 input fingerprint + checker; plan/cheat-sheet updates; baseline at end of 5b | `check_phase1_inputs.py` OK; `validate_registry.py` | [x] |
| 6 | [step6](ger_mode_cmds_plan2.step6.md) | §5.1–5.9 | `select_best_phrase.py`; multi-take real voice; alias harvest | All rows either `selected` or explicitly blocked as `needs_manual_redesign` | [ ] |
| 7 | [step7](ger_mode_cmds_plan2.step7.md) | §5.10 | Global audio grid search on all WAVs; write `whisper.config` | Tune completes; best params recorded | [ ] |
| 8 | [step8](ger_mode_cmds_plan2.step8.md) | §5.11 | Batch replay + regression repair loop | `verify_commands.py --batch-replay` green | [ ] |
| 9 | [step9](ger_mode_cmds_plan2.step9.md) | §7 | `verify_groq.py` on all takes | All `groq_pass` | [ ] |
| 10 | [step10](ger_mode_cmds_plan2.step10.md) | §8 | Optional `verify_commands.py` fresh-take pass | Optional `verified` / logs | [ ] |
| 11 | [step11](ger_mode_cmds_plan2.step11.md) | §9.3 | Load registry at runtime; update corpus, `whisper_text`, and `talon_cheat_sheet_ger.md`; keep `record_real_voice.py` compatibility until tests no longer import it | Full text/TTS suites + manual smoke | [ ] |
| 12 | [step12](ger_mode_cmds_plan2.step12.md) | §10 Step 12 | Promote WAVs to real fixtures; update real-voice harness/xfail; remove compatibility wrapper only when safe | Real-voice `test_recognition_level` / eval green | [ ] |

## Version control rule

A step is complete only when:

1. Every checkbox under Verifiable result for that step is satisfied.
2. Required artifacts are committed. See WAV storage policy in the [architecture doc](ger_mode_cmds_architecture2.md) for binary fixtures.
3. The Status column above is updated from `[ ]` to `[x]`.

## Scope guardrails

- Do not treat the old ~20 recorded real-voice subset as sufficient baseline; strategy assumes full re-validation.
- Do not accept phrases on TTS alone.
- Do not tune per-command audio during Phase 2.
- Do not integrate registry-as-runtime until Groq and batch replay gates pass.
- Do not perform a partial runtime migration: Step 11 is blocked until there are zero unresolved `needs_manual_redesign` rows.
- **Escalation:** If more than 5 commands remain `needs_manual_redesign` after Step 6 (all candidates exhausted), pause and review the synonym table and candidate generation strategies before continuing. This avoids investing in Steps 7–9 when a significant fraction of commands will require re-entry anyway.

## Model scope

Command optimization targets the **small** German Vosk model **`vosk-model-de-0.6`** only. Swapping to a larger model is **out of scope** for this track (see strategy §1.3). Tools `tune_lab/`, `offline_eval.py`, and `run_offline_eval.ps1` are relevant for Steps 7–8 and Step 12 (see [ger_mode_cmds_test2.md](ger_mode_cmds_test2.md)).

## Related documents

- [ger_mode_optim_strategy2.md](ger_mode_optim_strategy2.md)
- [ger_mode_cmds_architecture2.md](ger_mode_cmds_architecture2.md)
- [ger_mode_cmds_test2.md](ger_mode_cmds_test2.md)
- [ger_mode_cmds_plan2.manual_tests.md](ger_mode_cmds_plan2.manual_tests.md)
- [ger_mode_cmds_plan2.rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md) (conditional, before Step 5)
- [ger_mode_cmds_plan2.step5b.md](ger_mode_cmds_plan2.step5b.md) (TTS closure)
- [ger_mode_cmds_plan2.step5c.md](ger_mode_cmds_plan2.step5c.md) (Phase 1 input fingerprint; one-time / N/A)
