# German Mode Command Optimization Strategy

**Goal:** Every German voice command works reliably with the **small Vosk model** (`vosk-model-de-0.6`) using real voice input. The optimization process shall be **as automated as possible**.

**Date:** 2026-04-10

**Registry fields:** Plan 2 execution uses **`tts_status`** (Phase 1) and **`real_voice_status`** (Phase 2), not a single `status` column — see [ger_mode_cmds_architecture2.md](ger_mode_cmds_architecture2.md).

---

## 1. Problem Analysis

### 1.1 Core issue

The small Vosk model (`vosk-model-de-0.6`) has a limited vocabulary and acoustic model. Many current command phrases are misrecognized because they contain:

- **Rare or compound words** the model's lexicon doesn't cover well (e.g. `zeilenanfang`, `buchstabiere`, `leerzeichen`)
- **Short single-syllable words** that are acoustically ambiguous (e.g. `klein` → "leiden", `groß` → "groß" works but `groß das` → "groß dass")
- **Loanwords / product names** absent from German training data (e.g. `vosk`, `groq`)
- **Verb stems without inflection** that Vosk normalizes to inflected forms (e.g. `streich` → "streicht", `buchstabiere` → "buchstabieren")

### 1.2 Current state: almost nothing has been tested

The existing `recognition_xfail_real.json` lists 10 failures, but this is **not** a meaningful baseline — only ~20 out of ~40 total test phrases were ever recorded and tested. The remaining ~20 phrases have **unknown** Vosk recognition status. There are no existing real-voice recordings or verification results to build on.

**This strategy treats every command as untested.** All ~40 test phrases go through the full pipeline from scratch: TTS screening, candidate generation, real-voice selection, and verification.

The 10 known failures are useful only as **anecdotal evidence** of the types of problems to expect:

| Known failure pattern | Examples |
|-----------------------|----------|
| Loanwords / product names | `vosk` → "vor", `groq` → "grog" |
| Short ambiguous words | `klein` → "leiden" |
| Uninflected verb stems | `streich` → "streicht", `buchstabiere` → "buchstabieren" |
| Compound nouns | `zeilenanfang` → garbage |
| Unstable short function words | `geh` → "ge", "die" |
| Homophones | `das` → "dass" |

These patterns inform the candidate generation strategies (Section 4.5) but do not reduce the scope of work — every command must be verified.

### 1.3 What we can change

1. **The spoken command phrases** — swap words that Vosk misrecognizes for words it handles well
2. **Audio parameters** — `energy_threshold`, `audio_gain` to improve signal quality
3. **Phantom word lists** — pre/post-processing to strip or normalize Vosk artifacts
4. **Fuzzy matching / alias tables** — accept known Vosk distortions as valid matches
5. **The command parser** — adapt to accept rephrased commands

We **cannot** change the Vosk model itself (constraint: must work with `vosk-model-de-0.6`).

---

## 2. Planning Principles

### 2.1 Prefer the smallest effective intervention

Planning should prefer this order of intervention, escalating only when the lighter option is insufficient:

1. Better spoken phrase (swap words Vosk misrecognizes for words it handles well)
2. Explicit alias acceptance for predictable ASR variants (e.g. `dass`→`das`)
3. Normalization/postprocess adjustment where clearly justified
4. Parser or routing changes
5. Larger architectural refactor

### 2.2 Preserve compatibility consciously

If a phrase changes, the plan must explicitly decide whether the old phrase:

- remains supported as an alias (preferred — preserves muscle memory),
- is dropped immediately, or
- is kept only during a transition period.

This must be a tracked decision per command, not an accidental side effect.

### 2.3 Reuse the existing corpus as semantic ground truth

`test_corpus.py` already captures expected behavior, routing, and pre-state. Planning artifacts should reuse corpus IDs and expected behavior wherever possible instead of inventing a second competing semantics source.

### 2.4 TTS is for screening, not for acceptance

TTS is useful to flag obvious failures, rank candidates, and detect out-of-vocabulary phrases early. TTS is **not** sufficient to accept a phrase. Final phrase acceptance must be based on replayable real-voice evidence.

---

## 3. Strategy Overview

The optimization follows a **four-phase pipeline**, each phase building on the previous:

```
Phase 1: Vocabulary Analysis & Candidate Generation (mostly automated)
  → Extract Vosk's known vocabulary (hard boundary)
  → Build synonym table (manual, vocabulary-validated)
  → TTS-screen ALL ~40 test phrases through Vosk at once
  → Output: complete picture of what works / what doesn't before any manual work
  → For each TTS failure, auto-generate 5 candidate phrases (min 3, max 10)
  → TTS-screen all candidates, rank by recognition accuracy

Phase 2: Real-Voice Selection (interactive, user speaks)
  → For each command: user speaks phrase; **MIN_TAKES = 2** required; then **optional** open-ended extra takes (Phase B) until **`[o]`**
  → User controls: re-speak / next trial phrase / optional-phase **`[o]`** / **`[r]`/`[n]`/`[d]`**; stable vs fragile when optional no-matches occurred
  → Multiple WAVs per phrase capture speaking speed & style variations
  → Global audio param tuning + regression protection after selection

Phase 3: Groq Compatibility Check (fully automated)
  → Replay ALL saved WAVs from Phase 2 through the Groq backend
  → Verify that phrases optimized for Vosk also work with Groq (whisper-large-v3)
  → Flag any Groq-specific failures for resolution before integration

Phase 4: Verification (optional, can run any time)
  → Re-verify selected commands with up to 3 fresh takes
  → User controls pacing: skip, accept early, or quit at any time
  → False-positive test for commands that overlap with natural speech
  → Not a blocker for integration — Phase 2 "selected" status is sufficient
```

---

## 4. Phase 1: Vocabulary Analysis & Candidate Generation (fully automated)

### 4.1 Goal

For **every** command (~32 distinct patterns, expanding to ~40 test phrases with parametric variants — see Section 4.3), determine whether the current phrase works with Vosk, and if not, **automatically generate, test, and rank multiple candidate phrases** — all without any human interaction. The output is: commands that pass TTS as-is, plus a shortlist of ranked candidates per failing command, ready for real-voice confirmation in Phase 2.

**Starting point: zero prior data.** No existing recordings, test results, or xfail entries are relied upon. Everything is tested fresh.

### 4.2 Step 1a: Extract Vosk vocabulary (hard boundary)

1. Parse `vosk-model-de-0.6/graph/words.txt` (Kaldi word list) to get all words the model knows
2. This gives the hard boundary: words not in this file **cannot** be recognized
3. Store as `vosk_vocabulary.txt` for reference

### 4.3 Step 1b: Build the command registry

Extract all commands from `GERMAN_COMMANDS`, `parse_dictation_command()`, and `_try_system_command()` into a single **`command_registry.json`**:

```json
[
  {
    "id": "cmd_save",
    "mode": "command",
    "action": "edit.save",
    "description": "Save the current file",
    "current_phrase": "speichern",
    "candidates": [],
    "selected_phrase": null,
    "aliases": [],
    "status": "pending"
  }
]
```

All commands live in this one file — it is the **single source of truth** for what the system recognizes. After optimization, `german_commands.py` and `german_dictation_commands.py` will load their command definitions from this registry at runtime, replacing the hardcoded `GERMAN_COMMANDS` dict and if/elif chains in the parser.

**Timing note:** The registry serves as the optimization work artifact from the start (Phase 1). The runtime migration (making it the load source for the parser) is a **separate, late step** (Step 11 — Integration). These are distinct decisions: the optimization workflow needs the registry immediately; the runtime architecture change only happens after phrases stabilize and should be evaluated on its own merits at that point.

**Command count:** The codebase contains ~32 distinct command patterns (13 in `GERMAN_COMMANDS`, ~15 in `parse_dictation_command()`, 4 in `_try_system_command()`).

**Parametric commands** (e.g. `geh hoch N zeilen`) are registered as a single pattern entry but expand to **two test phrases** each:
- One with singular wording: `geh hoch eine zeile` (N=1)
- One with plural wording: `geh hoch zwei zeilen` (N=2)

Both test phrases must pass — if either fails, the pattern's carrier words need redesign. This covers the acoustic difference between singular and plural inflections while keeping the registry manageable.

**Estimated total: ~40 test phrases** (32 patterns + ~8 extra phrases from parametric expansions).

### 4.4 Step 1c: TTS batch evaluation of ALL current phrases

This is the **starting point of the entire optimization**. Before any human speaks a single word, TTS evaluates every command at once to produce a complete picture:

1. Generate TTS audio for every `current_phrase` in the registry (all ~40 test phrases)
2. Run Vosk on every TTS audio file in a single batch
3. Produce a **summary report**:

```
=== TTS Evaluation Report ===
Total test phrases: 40
TTS pass:  25 (63%)   ← current phrase recognized correctly
TTS fail:  15 (37%)   ← need candidate phrases

PASS:
  ✓ speichern       → "speichern"
  ✓ eingabe         → "eingabe"
  ✓ kopieren        → "kopieren"
  ...

FAIL:
  ✗ klein           → "leiden"          (substitution)
  ✗ streich das     → "streicht das"    (inflection)
  ✗ geh zeilenanfang → "geze ilan fang" (compound split)
  ...
```

This report is the **decision basis** for all subsequent work. It tells us exactly how many commands need redesign and what failure patterns to expect, before investing any manual recording time.

### 4.5 Step 1d: Auto-generate candidate phrases for failures

For each command with `status: "tts_fail"`, automatically generate alternative phrases:

**Generation strategies (applied in order):**

1. **Inflection variants** — if the command uses a verb stem (`streich`, `lösch`, `buchstabiere`), generate inflected forms (`streiche`, `lösche`, `buchstabieren`) that Vosk's language model expects. Only forms present in `vosk_vocabulary.txt` are kept.

2. **Synonym substitution** — replace failing words with synonyms from a curated synonym table, filtered against `vosk_vocabulary.txt`:
   - `geh` → `nach`, `cursor`, `spring`
   - `klein` → `kleine buchstaben`, `winzig`
   - `wörtlich` → `genau`, `direkt`, `rein`
   - `zeilenanfang` → `anfang zeile`, `zeile start`
   - etc.

3. **Structural rewrite** — split compounds, add/remove carrier words, reorder:
   - `geh zeilenanfang` → `anfang der zeile`, `zeile anfang`, `zum anfang`
   - `modell vosk` → `wechsel lokal`, `motor lokal`, `offline modus`
   - `kein leerzeichen` → `ohne abstand`, `kein abstand`

4. **Length variants** — for single-word commands that are acoustically ambiguous, generate two-word alternatives that give Vosk more context:
   - `klein` → `klein schreiben`, `kleine schrift`
   - `groß` → `groß schreiben`, `große schrift`

Each strategy only emits candidates whose **every word** appears in `vosk_vocabulary.txt`. Candidates that use out-of-vocabulary words are discarded immediately.

**Target: 5 candidates per failing command** (minimum 3, hard cap 10). Since TTS-screening is fully automated and fast, the cost of generating more candidates is low — the cap exists only to keep the synonym table manageable and avoid combinatorial explosion from structural rewrites.

### 4.6 Step 1e: TTS-screen all candidates (fully automated)

For each candidate phrase:

1. Generate TTS audio
2. Run Vosk recognition
3. Record: `{ candidate, recognized_as, exact_match: bool, edit_distance: int }`

**Candidate ranking** (determines the order in which candidates are presented for real-voice testing in Phase 2):
1. Exact TTS match (yes/no) — exact matches first
2. Edit distance (lower is better)
3. Phrase length (prefer shorter, all else equal — easier to speak quickly)

**Candidate diversity requirement:** Candidates for the same command must be **meaningfully different** from each other — not just minor spelling or inflection variants of the same phrase. The generation strategies (inflection, synonym, structural rewrite, length) naturally produce diverse candidates because they attack the problem from different angles. As an explicit check, candidates sharing >50% of their words (after normalization) with another candidate for the same command are deduplicated — only the higher-ranked one survives. This ensures that real-voice testing in Phase 2 covers genuinely different phrasings rather than wasting time on near-duplicates.

### 4.7 Deliverable

Updated `command_registry.json` with a `candidates` array per failing command:

```json
{
  "id": "dict_lowercase_next",
  "current_phrase": "klein",
  "candidates": [
    { "phrase": "klein schreiben", "tts_recognized": "klein schreiben", "tts_match": true, "rank": 1 },
    { "phrase": "kleine schrift",  "tts_recognized": "kleine schrift",  "tts_match": true, "rank": 2 },
    { "phrase": "winzig",          "tts_recognized": "winzig",          "tts_match": true, "rank": 3 },
    { "phrase": "kleinbuchstabe",  "tts_recognized": "kleiner schafe",  "tts_match": false, "rank": 99 }
  ],
  "status": "candidates_ready"
}
```

Commands that pass TTS have no candidates yet, but still require real-voice confirmation in Phase 2 (TTS-pass does not guarantee real-voice-pass). If a TTS-pass command fails real voice, candidates are generated on the fly.

---

## 5. Phase 2: Real-Voice Selection for All Commands

### 5.1 Goal

**Every** command gets real-voice tested — not just the ones that failed TTS. TTS is a useful pre-filter, but TTS-pass does not guarantee real-voice-pass (different acoustic characteristics, microphone noise, speaker variation). The human's only job is speaking — the script decides which phrase works best.

### 5.2 Audio parameters: fixed during selection

Phase 2 uses **fixed audio parameters** (`energy_threshold`, `audio_gain`) throughout. No per-command tuning happens here — the goal is to find phrases that work with reasonable default settings. Audio parameter optimization is a separate step that happens later (see Section 5.10) and operates globally across all commands.

**Rationale:** If we tuned audio params per-command, the optimal settings for command #50 might break commands #1–49. By fixing params during phrase selection, we ensure that phrase quality — not parameter overfitting — drives the results.

### 5.3 Selection script (`select_best_phrase.py`)

The script walks **`command_registry.json`** in order (respecting Step 6 entry gates on **`tts_status`**). For each variant’s ranked **trial phrases**, it records real audio, runs Vosk + shared **`check_match`**, and keeps WAVs under `verify_audio/`.

**Phase A — minimum takes:** Record until **`MIN_TAKES`** (2) passing takes for the current trial phrase. On no-match **before** the minimum is reached: **`[r]`** discards the take and retries; **`[n]`** abandons this trial phrase and tries the next ranked phrase (failed take is discarded). **`[q]`** saves **`phase2_selection_checkpoint.json`** (including partial good passes and optional-phase progress).

**Phase B — optional extras:** After Phase A succeeds, the operator may record **any number** of additional takes using the same record → transcribe → match flow, until they press **`[o]`** in the Phase B main menu to finish (equivalent to skipping extras if chosen immediately). On optional no-match **while** `len(good) >= MIN_TAKES`: **`[r]`** discards that WAV and retries the same optional slot; **`[n]`** deletes **all** WAVs recorded for this trial phrase (including the passing minimum) and advances to the next ranked trial phrase; **`[d]`** discards only the failed optional WAV and finalizes the phrase with the passing takes already on disk.

**Stable vs fragile:** If **any** optional take had `match=False` in Phase B (even if later fixed by **`[r]`**), the script asks **`[s]`** stable vs **`[f]`** fragile before writing the registry. If the operator never records an optional take that fails to match, there is no fragile prompt (including when they exit Phase B immediately with **`[o]`**). **`real_voice_fragile`** is set **only** from that answer (never inferred automatically). Omit the field when stable.

**The user can quit at any time** — checkpoint captures mid–optional menus and mid–fragile prompt where applicable. **`--reset`*** clears Phase 2 fields including **`real_voice_fragile`**.

Implementation detail: see `run_trial_phrase_workflow()` in `select_best_phrase.py` and `test_select_best_phrase_flow.py` (mocked tests).

### 5.4 Multiple takes: proving stability

Recording a single WAV per phrase is fragile — a phrase that works when spoken slowly and carefully might fail at natural speaking speed. Multiple takes prove that recognition is **stable, not lucky**:

- **Minimum 2 takes required** to accept a phrase — all must be recognized correctly (Phase A).
- The user should vary speaking speed and volume between takes (normal, fast, slow).
- All passing takes are saved as `verify_audio/{command_id}_take1.wav`, `_take2.wav`, etc. (or `_tp{i}_takeN` for multi-variant).
- **Before `MIN_TAKES`:** a no-match with **`[n]`** (next ranked trial phrase) abandons the current phrase attempt; failed takes are discarded; the operator moves on without accepting that phrase.
- **After `MIN_TAKES` (optional Phase B):** a no-match does **not** by itself reject the phrase — **`[r]`**, **`[n]`**, or **`[d]`** apply as in §5.3. **`[n]`** here deletes **all** WAVs for this trial phrase and moves to the next ranked phrase.
- During regression checks (Section 5.11), **all takes** kept on disk for a command are replayed — a phrase must pass on all of them, not just one.

This means the regression test corpus automatically contains speaking-speed variation, making it much more robust than a single "careful" recording.

### 5.5 User control: stability over luck

The goal of multiple takes is to **prove that recognition is stable** — not just lucky on a single recording. All passing takes are kept as evidence; the phrase is only accepted if it works consistently.

**After each take, the script reports the result and offers:**

- **On successful recognition (Phase A):** the take counts toward **`MIN_TAKES`**; continue until the minimum is met.

- **After the minimum number of takes (2) all passed:** Phase B runs until the operator chooses **`[o]`** to finish (or **`[d]`** after an optional no-match finalizes early). Each optional take uses the same record/review loop; optional no-match uses **`[r]` / `[n]` / `[d]`** (§5.3–5.4).

- **If a take fails recognition before `MIN_TAKES` is met:**
  - **"Discard & retry" (`[r]`)** — bad sample; the failed WAV is removed; try again toward the minimum.
  - **"Next trial phrase" (`[n]`)** — abandon this ranked phrase for now; move to the next candidate wording for the same variant (failed take discarded).

- **If a take fails recognition in optional Phase B (minimum already met):**
  - **`[r]`** — discard this optional take and retry the same optional slot.
  - **`[n]`** — delete **all** WAVs for this trial phrase and move to the next ranked phrase.
  - **`[d]`** — discard only the failed optional WAV; keep at least `MIN_TAKES` passing files; then stable/fragile confirmation if any optional no-match occurred in this Phase B.

**Acceptance rule:** A phrase is accepted when it has at least `MIN_TAKES` (2) passing recordings with varied speaking speed/volume. Optional extras add evidence; optional failures are handled with **`[r]` / `[n]` / `[d]`**, not automatic phrase rejection.

**What "rejected" means (pre-minimum or via `[n]`):** Trial phrase abandoned for this pass; **`[n]`** after optional failure removes all takes for that phrase from disk. Exhausting ranked phrases without a full variant set marks **`real_voice_status`: `needs_manual_redesign`** as today.

### 5.6 Session persistence: stop and resume

The recording phase may take 30+ minutes. The user must be able to **stop at any time and resume later** without losing progress.

**How it works:**

- **All state lives on disk**, not in memory:
  - `command_registry.json` — each command's `status`, `selected_phrase`, `candidate_index` are written after every status change
  - `verify_audio/{command_id}_take*.wav` — WAV files are saved to disk immediately after each accepted take, not buffered in memory
- **On quit (`[q]`)**: partial progress for the current command (takes recorded so far, which candidate is being tested) is saved. The script prints a summary: "15 of 60 commands completed. Resume with: `select_best_phrase.py`"
- **On resume**: the script reads `command_registry.json`, skips all commands with `status: "selected"`, and picks up the current command where it left off (including any partial takes already on disk)
- **Crash-safe**: even if the script is killed (Ctrl+C, power loss), the worst case is losing the current in-progress take. All previously accepted takes and completed commands are already on disk.

**Example session flow:**
```
Session 1:  Commands 1–20 completed, quit
Session 2:  Commands 21–40 completed, quit
Session 3:  Commands 41–60 completed, done
```

### 5.7 Manual re-recording: resetting a confirmed phrase

After completing the recording phase, the user may decide that a previously accepted phrase should be re-recorded — for example, after discovering during daily use that a phrase is less reliable than the 2-take test suggested, or after changing microphone hardware.

**How to reset a command for re-recording:**

```
select_best_phrase.py --reset cmd_save
```

This:
1. Sets `command.status` back to `"pending"` (or `"tts_pass"` / `"candidates_ready"` depending on original TTS result)
2. Deletes all WAV files for that command from `verify_audio/`
3. Clears `selected_phrase` and `aliases`
4. On next run of `select_best_phrase.py`, this command will be presented for recording again (starting from the current phrase or first candidate, as if it had never been tested)

**Batch reset:**
```
# By command line arguments:
select_best_phrase.py --reset cmd_save dict_fmt_gross dict_nav_up

# By file (one id per line, blank lines and #comments ignored):
select_best_phrase.py --reset-file reset_list.txt

# Reset everything:
select_best_phrase.py --reset-all
```

`reset_list.txt` example:
```
# Re-record after microphone change
cmd_save
dict_fmt_gross
dict_nav_up
# dict_fmt_klein   ← commented out, skip this one
```

**The reset does NOT re-run Phase 1** (TTS screening, candidate generation). Those results are stable and reusable. It only resets the real-voice selection state for the specified commands.

### 5.8 Candidate progression

Candidates are tested in rank order (best TTS score first). The flow per command:

1. If `tts_pass`: try the current phrase first. If the user accepts it, done.
2. If current phrase is rejected (by user or by recognition failure): fall through to ranked candidates.
3. Test candidate #1, then #2, etc. — **stop at first user-accepted match**.
4. If all candidates exhausted: flag as `needs_manual_redesign`.

**Fallback on surprise failures**: if a TTS-pass command fails real voice, candidates are generated on the fly (same synonym table + vocabulary filter from Phase 1) and tested immediately.

### 5.9 Alias harvesting

During selection, if Vosk consistently produces a distortion across multiple takes (e.g. `"groß dass"` for `"groß das"`), the script auto-adds it as an alias:

```json
{
  "selected_phrase": "groß das",
  "aliases": ["groß dass"],
  "alias_source": "auto-harvested from vosk output during selection"
}
```

With multiple takes per phrase, alias harvesting is more robust — a distortion that appears in 2+ takes is clearly systematic (Vosk model behavior), not a one-off artifact.

### 5.10 Global audio parameter tuning (after all phrases are selected)

Once all commands have a `selected_phrase`, a **global audio parameter sweep** is run across the full set of saved recordings:

```
1. Collect ALL WAVs from Phase 2 selection (multiple takes per command, ~120–180 files)
2. Grid-search over energy_threshold × audio_gain combinations
   (reuses existing tune_agent.py infrastructure)
3. For each parameter combination:
   - Replay ALL saved WAVs through Vosk (every take of every command)
   - Score: number of commands where ALL takes are correctly recognized
     (a command counts as "pass" only if every take matches — not just the best one)
4. Select the parameter set that maximizes the total number of fully-passing commands
5. Write optimal params to whisper.config
```

**Why after, not during:** Tuning params per-command during Phase 2 would overfit — settings optimized for command #1 might degrade command #50. By tuning globally on the full recording set (with multiple takes covering speaking speed variation), we find the sweet spot that works for the **entire command set under realistic conditions**.

**If tuning changes break previously-passing commands:** This triggers the regression loop (Section 5.11).

### 5.11 Regression protection: re-verify after every change

Any change that could affect recognition (new audio params, new phantom words, new aliases) triggers a **full batch replay** of all saved WAVs:

```
verify_commands.py --batch-replay
  → Replay ALL saved WAVs (every take of every command) through Vosk with current settings
  → A command passes only if ALL its takes are recognized correctly
  → Report: PASS / REGRESSED per command (with per-take details)
```

**If regressions are detected** (a previously-passing command now fails):

```
For each regressed command:
  1. Log the regression: old params → passed, new params → failed
  2. Re-enter the selection loop for this command:
     - Try current phrase with new params (maybe an alias fixes it)
     - If not: test the next-ranked candidate from Phase 1
     - If not: record new real-voice candidates
  3. After fixing, re-run batch-replay on ALL commands again
  4. Repeat until zero regressions
```

**This creates a feedback loop:**
```
  Select phrases → Tune params globally → Batch replay ALL
       ↑                                        |
       |              regressions?               |
       +────── YES ← ─────────────────────────── +
                      NO → proceed to Phase 3 (Groq check)
```

The loop converges because:
- Each iteration fixes regressions by finding phrases that work under the new params
- The param sweep re-runs on the updated recording set
- In the worst case, params revert to the pre-tuning defaults (which all phrases were originally selected under)

### 5.12 Deliverable

Finalized `command_registry.json` with `selected_phrase` and `aliases` for every command, verified under globally-optimized audio parameters. All commands must reach status `"selected"` before integration; any interim `"needs_manual_redesign"` rows must be resolved first.

---

## 6. Redesign Rules (applied during candidate generation)

### 6.1 Constraints

1. **Keep working commands unchanged** — don't fix what isn't broken
2. **Every word must be in `vosk_vocabulary.txt`** — hard filter, no exceptions
3. **No collisions** — a candidate phrase must not be a prefix/substring of another command or common dictation text
4. **Prefer longer phrases** over short ones — Vosk has more acoustic context (e.g. `klein` alone is ambiguous, `klein schreiben` gives two words of context)
5. **Use common, high-frequency German words** — they have better acoustic models in Vosk
6. **Avoid compound nouns** — split them (e.g. `zeilenanfang` → `anfang zeile`)
7. **Use inflected verb forms** that Vosk expects — Vosk's language model predicts standard grammar (e.g. `streich` → `streiche`)
8. **Avoid English loanwords** in command phrases — replace `groq`/`vosk` with German carrier phrases
9. **Add fuzzy aliases** — accept known Vosk distortions (e.g. `dass` = `das`)

### 6.2 Initial redesign candidates for known failures

| Current command | Problem | Candidate pool (filtered by vocabulary) |
|----------------|---------|----------------------------------------|
| `klein` | → "leiden" | `klein schreiben`, `kleine schrift`, `winzig` |
| `streich das` | → "streicht das" | `streiche das`, + alias `streicht das` |
| `groß das` | → "groß dass" | keep + alias `dass`→`das` |
| `geh hoch N zeilen` | "geh" unstable | `nach oben N zeilen`, `hoch N zeilen`, `oben N zeilen` |
| `geh rechts ein wort` | "geh" → "die" | `nach rechts ein wort`, `rechts ein wort` |
| `geh zeilenanfang` | compound garbled | `anfang der zeile`, `zum anfang`, `zeile anfang` |
| `modell vosk` | "vosk" → "vor" | `wechsel lokal`, `motor lokal`, `offline modus` |
| `modell groq` | "groq" → "grog" | `wechsel wolke`, `motor online`, `wolke modus` |
| `wörtlich X` | → "wirklich" | `genau X`, `direkt X`, `rein X` |
| `buchstabiere das` | → "buchstabieren" | `buchstabieren das` (accept inflection), + alias |

These are starting points — the automated pipeline will test all of them and may discover better options.

---

## 7. Phase 3: Groq Compatibility Check (fully automated)

### 7.1 Goal

Phrases optimized for the small Vosk model must also work with the Groq backend (`whisper-large-v3`). Since Groq is a much more capable model, most phrases should pass — but phrase redesigns (e.g. splitting compounds, adding carrier words) could introduce unexpected Groq failures. This phase catches them before integration.

### 7.2 Batch replay through Groq

This phase is **fully automated** — it replays existing WAVs from Phase 2 through Groq, no new recordings needed:

```
For each command in command_registry.json where status == "selected":
  phrase = selected_phrase or current_phrase
  
  for each saved WAV (all takes from Phase 2):
    recognized = groq_recognize(wav)
    match = check_match(recognized, phrase, command.aliases)
    log(command.id, wav_file, "groq", recognized, match)
  
  if all takes match:
    command.groq_status = "groq_pass"
  else:
    command.groq_status = "groq_fail"
```

### 7.3 Handling Groq failures

Groq failures on Vosk-optimized phrases are expected to be rare but possible. For each failure:

1. **Check if it's an alias issue** — Groq may produce a different (but correct) transcription. Add a Groq-specific alias if the output is a predictable variant (e.g. different capitalization, punctuation, or homophone choice)
2. **Check if the phrase is too unusual** — a phrase designed to fit Vosk's small vocabulary might sound unnatural enough that Whisper normalizes it differently. In that case, the Phase 1 candidate list may have an alternative that works for both backends
3. **Re-enter Phase 2 if needed** — select a different phrase that passes both Vosk and Groq. The candidate ranking in Phase 1 can be extended to include a "Groq TTS pre-screen" as a tiebreaker

**Constraint:** A phrase is only acceptable if it works with **both** backends. A phrase that passes Vosk but fails Groq (or vice versa) must be replaced.

### 7.4 Deliverable

Updated `command_registry.json` with `groq_status` per command. All commands must have `groq_status: "groq_pass"` before proceeding to integration.

---

## 8. Phase 4: Verification (optional)

Phase 4 is an **optional** confirmation pass that can be run **at any time** — immediately after Phase 2, days later, or after a microphone change. It is not a gate for integration; Phase 2's `"selected"` status is sufficient.

**Why run it?** Phases 2–3 prove that a phrase works with both backends. Phase 4 proves it *still* works under different conditions — after the user's vocal patterns settle, speaking speed normalizes, or hardware changes. Running it on a different day than Phase 2 maximizes its value.

### 8.1 Verification script (`verify_commands.py`)

The script records up to 3 fresh takes per command, but the user has full control over pacing:

```
For each command in command_registry.json where status == "selected":
  phrase = selected_phrase or current_phrase
  takes = []

  TAKE_LOOP:
    take_number = len(takes) + 1
    print(f"[{take_number}/3] Say: '{phrase}'")
    print(f"[Enter] Record  [s] Skip this command  [q] Quit session")
    
    choice = prompt_user()
    if choice == "skip":
      # leave status unchanged ("selected"), move on
      → NEXT COMMAND
    if choice == "quit":
      save_partial_progress(command, takes)
      → EXIT SCRIPT

    audio = record_audio()
    recognized = vosk_recognize(audio)
    match = check_match(recognized, phrase, command.aliases)
    log(command.id, take_number, recognized, match)

    if match:
      save_take_to_disk(command, audio, take_number)
      takes.append(audio)
      print(f"✓ Recognized: '{recognized}'  [{len(takes)}/3]")
      
      if len(takes) >= 3:
        command.status = "verified"
        save_registry()
        → NEXT COMMAND
      
      choice2 = prompt_user("[Enter] Next take  [a] Accept (enough takes)  [s] Skip to next command")
      if choice2 == "accept":
        command.status = "verified"
        save_registry()
        → NEXT COMMAND
      elif choice2 == "skip":
        → NEXT COMMAND   # keeps takes recorded so far, status stays "selected"
      else:
        → TAKE_LOOP
    
    else:  # no match
      print(f"✗ Recognized: '{recognized}'  (expected: '{phrase}')")
      choice3 = prompt_user("[d] Discard (bad sample)  [s] Skip to next command")
      if choice3 == "skip":
        command.status = "verification_failed"
        save_registry()
        → NEXT COMMAND
      else:
        → TAKE_LOOP   # retry
```

**Key differences from Phase 2:**
- The user can **skip** any command at any time — no obligation to record all 3 takes
- A skipped command retains its `"selected"` status from Phase 2 (it still works, just isn't re-verified)
- The user can **accept early** after fewer than 3 takes if satisfied
- Failed recognition does not auto-reject the phrase — it may just be a bad take; the user decides whether to retry or skip

### 8.2 Matching logic

```python
def check_match(recognized: str, phrase: str, aliases: list[str]) -> tuple[bool, str]:
    norm_rec = normalize(recognized)
    
    # Exact match on primary phrase
    if norm_rec == normalize(phrase):
        return True, "exact"
    
    # Alias match (includes auto-harvested distortions from Phase 2)
    for alias in aliases:
        if norm_rec == normalize(alias):
            return True, f"alias:{alias}"
    
    # Built-in fuzzy: dass/das normalization (ubiquitous Vosk quirk)
    if norm_rec.replace("dass", "das") == normalize(phrase):
        return True, "dass→das"
    
    return False, "no_match"
```

### 8.3 Verification log

`verification_log.json`:
```json
[
  {
    "id": "cmd_save",
    "phrase": "speichern",
    "selection_takes": [
      { "file": "verify_audio/cmd_save_take1.wav", "recognized": "speichern", "match": "exact" },
      { "file": "verify_audio/cmd_save_take2.wav", "recognized": "speichern", "match": "exact" },
      { "file": "verify_audio/cmd_save_take3.wav", "recognized": "speichern", "match": "exact" }
    ],
    "verification_attempts": [
      { "file": "verify_audio/cmd_save_verify1.wav", "recognized": "speichern", "match": "exact" },
      { "file": "verify_audio/cmd_save_verify2.wav", "recognized": "speichern", "match": "exact" },
      { "file": "verify_audio/cmd_save_verify3.wav", "recognized": "speichern", "match": "exact" }
    ],
    "status": "verified",
    "timestamp": "2026-04-10T14:30:00Z"
  }
]
```

### 8.4 Handling failures

If any commands end up with `status: "verification_failed"` after a verification run, the user can:

1. **Ignore** — the command still has `"selected"` status from Phase 2 and works; the verification failure may be transient
2. **Re-enter Phase 2** — reset the command (see Section 5.7) and re-select with `select_best_phrase.py`
3. **Re-run only failed commands** — `verify_commands.py --only-failed`
4. **Re-enter Phase 2 later** — if the command still needs redesign for Vosk

### 8.5 Batch re-verify mode

Same as Section 5.11 (regression protection), but now includes Phase 4 verification WAVs in addition to Phase 2 selection takes. Run via `verify_commands.py --batch-replay`. Fully automated, no human interaction.

### 8.6 Acceptance criteria

- **Minimum: all commands reach `"selected"`** after Phase 2 (sufficient for integration)
- **Ideal: all commands reach `"verified"`** via Phase 4 (additional confidence)
- A command is "verified" if correctly recognized across all takes (selection takes + verification takes)
- Commands that remain `"needs_manual_redesign"` after an initial pass must be resolved before Step 11 integration
- Phase 4 is not a blocker — it can be run incrementally, skipping commands as needed

---

## 9. Implementation: Files and Scripts

### 9.1 Vosk integration path

The optimization scripts need to invoke Vosk recognition on WAV files. The existing infrastructure already supports this:

- **`corpus_tts.py`** (in `ger_mode_cmds_test/`) — generates TTS WAVs and runs Vosk recognition; reused for Phase 1 TTS screening
- **`tune_agent.py`** — runs grid-search over audio parameters by replaying WAVs through Vosk; reused for Phase 2 global tuning (Step 7)
- **`whisper_engine.py` / `whisper_worker.py`** — the Vosk recognition pipeline; the new scripts call into this for real-time recording + recognition

The new scripts (`generate_candidates.py`, `select_best_phrase.py`, `verify_commands.py`) build on this existing infrastructure rather than calling the Vosk Python API directly. This ensures consistent audio preprocessing (gain, energy threshold, phantom word filtering).

### 9.2 New files (all under `user/talon_german/`)

| File | Purpose |
|------|---------|
| `command_registry.json` | Single source of truth: all commands with phrases, candidates, aliases, action mapping, status. Becomes the runtime command source after integration (Step 11) |
| `vosk_vocabulary.txt` | Extracted word list from the Vosk model (hard boundary for candidate generation) |
| `synonym_table.json` | Curated synonym/rewrite rules for candidate generation (input to Step 5). Must be authored before candidate generation runs |
| `generate_candidates.py` | Phase 1: extract vocabulary, TTS-screen current phrases, generate & rank candidates |
| `select_best_phrase.py` | Phase 2: interactive real-voice candidate selection (user speaks, script picks winner) |
| `verify_groq.py` | Phase 3: batch-replay all Phase 2 WAVs through Groq backend; fully automated |
| `verify_commands.py` | Phase 4: optional end-to-end re-verification with fresh takes |
| `verification_log.json` | Phase 3+4 output: per-command verification results with all attempts |
| `verify_audio/` | Directory for verification WAV recordings (become regression fixtures) |

**User documentation (repository root, not under `user/talon_german/`):** `talon_cheat_sheet_ger.md` — quick reference for spoken phrases; must stay aligned with `command_registry.json` (bootstrap after Step 1, final pass at integration; see Plan 2).

### 9.3 Modified files (after optimization is complete)

| File | Change |
|------|--------|
| `german_commands.py` | Load commands from `command_registry.json` at runtime instead of hardcoded `GERMAN_COMMANDS` dict; add alias matching |
| `german_dictation_commands.py` | Replace if/elif parser with registry-driven matching + aliases |
| `whisper_text.py` | Add normalization rules derived from verification (e.g. dass→das) |
| `test_corpus.py` | Update `spoken` fields to match new command phrases |
| `talon_cheat_sheet_ger.md` | Update listed phrases to match registry `selected_phrase` / user-facing aliases (same intent as corpus) |
| `recognition_xfail_real.json` | Cleared after the real-voice fixture gate is green; target: empty file |
| `record_real_voice.py` | Retired as the preferred workflow; compatibility wrapper kept until the test harness no longer imports it |

---

## 10. Execution Order

### Step 1: Build command registry (automated)
- Script parses `GERMAN_COMMANDS`, `parse_dictation_command()`, and `_try_system_command()` → writes `command_registry.json`
- Include: id, action, description, current phrase, mode (command/dictation/system)
- Parametric commands expand to two test phrases: singular (N=1, e.g. `geh hoch eins zeilen`) and plural (N=2, e.g. `geh hoch zwei zeilen`) — wording must match the parser in `german_dictation_commands.py`
- **Estimate: ~32 distinct command patterns → ~40 test phrases** (13 command-mode + ~15 dictation patterns + 4 system + ~8 parametric expansions)

### Step 2: Extract Vosk vocabulary (automated)
- Parse `vosk-model-de-0.6/graph/words.txt` → `vosk_vocabulary.txt`
- Cross-reference: flag every command word that is NOT in the vocabulary

### Step 3: Build synonym table (manual + automated validation)
- Create `synonym_table.json` with rewrite rules informed by the known failure patterns (Section 6.2)
- Each entry maps a failing word/phrase to alternative candidates
- All candidate words are validated against `vosk_vocabulary.txt` — entries with out-of-vocabulary words are flagged
- This is the **only manual authoring step** in Phase 1; it seeds the automated candidate generator

### Step 4: TTS pre-screen ALL current phrases (automated)
- Generate TTS for each `current_phrase` (all ~40 test phrases), run through Vosk
- Mark commands as `tts_pass` or `tts_fail`
- The failure rate is unknown in advance — this step discovers it

### Step 5: Generate & rank candidates for ALL TTS failures (automated)
- For each `tts_fail` command: generate 5 candidate phrases (min 3, max 10) using synonym table + vocabulary filter
- TTS-screen every candidate through Vosk
- Rank by: exact match > edit distance > phrase length
- Store ranked candidates in `command_registry.json`
- **No human interaction required for this step**

### Step 6: Real-voice selection for ALL commands (interactive)
- Run `select_best_phrase.py`
- For `tts_pass` commands: user speaks the current phrase for multi-take confirmation (MIN_TAKES = 2); if it fails, candidates are generated on the fly
- For `tts_fail` commands: user speaks candidates in rank order; **stop at first match** (no need to test all 5)
- Auto-harvests consistent Vosk distortions as aliases
- **Human role: speak ~40 phrases × 2 takes minimum (best case: every command works on first try)**

### Step 7: Global audio parameter tuning (automated)
- Grid-search `energy_threshold` × `audio_gain` over ALL saved WAVs from Step 6, reusing the existing `tune_agent.py` infrastructure
- Select params that maximize total match count across the entire command set
- **No human interaction — fully automated replay of existing recordings**

### Step 8: Regression check & repair (automated + interactive if regressions found)
- Batch-replay ALL saved WAVs with the new audio params
- If any previously-passing command now fails (regression):
  - Re-enter selection loop for that command (try aliases, next-ranked candidate, or new recording)
  - Re-run global tuning on updated recording set
  - Repeat until zero regressions
- **If no regressions: proceed. If regressions: the loop is mostly automated (batch replay), with human re-recording only for commands that need a new phrase.**

### Step 9: Groq compatibility check (automated)
- Run `verify_groq.py` — batch-replay ALL saved WAVs from Step 6 through the Groq backend (`whisper-large-v3`)
- Verify that every `selected_phrase` is correctly recognized by Groq (with aliases)
- If a phrase fails Groq: add a Groq-specific alias, or re-enter Phase 2 to select a phrase that works with both backends
- **A phrase must pass both Vosk and Groq to be accepted**
- **No human interaction — fully automated replay of existing recordings**

### Step 10: Verification pass (optional, interactive)
- Run `verify_commands.py` on all `"selected"` commands — can be run any time, not a blocker for integration
- Each command: up to 3 fresh takes; user can skip or accept early at any point
- **False-positive test:** for multi-word commands that overlap with natural speech, speak the command phrase in a dictation context and verify it does NOT trigger the command
- Failures can be addressed via Phase 2 re-selection or ignored if transient

### Step 11: Integration
- Update `german_commands.py` to load from `command_registry.json` at runtime (registry becomes the single source of truth)
- Update `german_dictation_commands.py` parser to be driven by registry data + alias matching
- Update test corpus
- Keep `record_real_voice.py` compatibility if the test harness still imports it
- Run full test suite

### Step 12: Regression gate
- All verification WAVs become the new real-voice test fixtures in `audio/real/`
- `test_recognition_level.py` runs against them
- Clear xfail entries
- Retire the existing `record_real_voice.py` compatibility wrapper once the test harness no longer imports it
- CI/offline eval ensures no regressions

---

## 11. Automation Boundaries

| Task | Automation level | Human effort |
|------|-----------------|--------------|
| Extracting commands into registry | **Fully automated** (parse Python source) | None |
| Extracting Vosk vocabulary | **Fully automated** (parse model files) | None |
| Building synonym table | **Manual** (curated rewrite rules, vocab-validated) | Author ~15–20 entries |
| TTS pre-screening current phrases | **Fully automated** | None |
| Generating candidate phrases | **Fully automated** (synonym table + vocab filter) | None |
| TTS-screening all candidates | **Fully automated** | None |
| Ranking candidates | **Fully automated** (match rate + edit distance) | None |
| Real-voice selection (all commands) | **Automated decision**, human speaks | Speak ~40 phrases × 2+ takes |
| Alias harvesting from Vosk output | **Fully automated** | None |
| Global audio parameter tuning | **Fully automated** (grid search over saved WAVs via `tune_agent.py`) | None |
| Regression check (batch replay) | **Fully automated** (replay ALL WAVs after any change) | None |
| Regression repair (re-selection) | **Mostly automated**, human re-records if needed | Re-speak only regressed commands |
| Groq compatibility check | **Fully automated** (replay WAVs through Groq) | None |
| Verification (optional) | **Automated decision**, human speaks | Up to 3x per command; skip/accept early allowed |
| Code integration | **Manual** (registry becomes runtime source of truth) | Developer work |

**Overall: ~80% automated.** The human's role is reduced to **speaking phrases when prompted** and authoring the initial synonym table. The script generates candidates, tests them, ranks them, selects the first match, tunes audio params globally, detects regressions, and triggers re-selection — all without human decision-making. The only non-automatable steps are producing real voice audio and curating the synonym/rewrite rules.

---

## 12. Risk Mitigation

### 12.1 Vosk vocabulary too small
Some concepts may simply not have good single-word representations in the small model. Mitigation:
- Use two-word phrases (more acoustic context)
- Accept fuzzy matching with documented aliases
- Last resort: redesign the phrase and re-run Phase 2 later rather than integrating a command that only works on Groq

### 12.2 Speaker dependence
The optimization is tuned to one speaker's voice. Mitigation:
- Keep audio parameters moderate (don't over-tune)
- Prefer phrase changes over parameter hacks
- Document that re-verification is needed for new speakers

### 12.3 Dictation mode ambiguity
If command phrases are common German words, they'll be misrecognized during dictation. Mitigation:
- Prefer multi-word commands (lower collision with natural speech)
- Keep the `wörtlich` escape hatch (or its replacement) for edge cases
- Test in dictation mode specifically: speak the command phrase as regular text and verify it does NOT trigger the command (false-positive test)

### 12.4 Regression risk
Changing command phrases breaks muscle memory. Mitigation:
- Only change phrases that currently don't work anyway
- Keep old phrases as aliases where possible
- Document all changes in a migration table

---

## 13. Key Decisions The Planning Artifacts Must Address

The planning step files should answer these questions explicitly rather than leaving them implicit:

1. What is the exact optimization target inventory, derived from current code and corpus?
2. Which phrases are allowed to change, and which should prefer alias-based compatibility?
3. At what point does `command_registry.json` transition from planning artifact to runtime input — and what is the acceptance gate for that transition?
4. What historical recording artifacts remain in the repo as reference vs. active test fixtures?
5. What is the acceptance rule for a phrase before code integration (MIN_TAKES, both-backend pass)?
6. What is the policy for commands that remain weak on small Vosk but work on Groq?

---

## 14. Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Test phrases with real-voice Vosk verification | ~20 of ~40 (~50%) | **40 of 40 (100%)** |
| Test phrases passing real-voice Vosk | unknown (incomplete data) | **100%** |
| Test phrases passing Groq (replay) | untested | **100%** (both backends must pass) |
| xfail entries (real voice, Vosk) | 10 (incomplete — most commands untested) | **0** |
| Manual steps per command verification | many (ad-hoc manual process) | **1** (speak when prompted) |
| Time to verify all commands | never completed | **~30 min** (automated loop, all ~40 test phrases) |
| Command source of truth | hardcoded Python dicts + if/elif chains | **`command_registry.json`** (single file, loaded at runtime) |

---

## Plan 2 addendum (execution contract)

The [Plan 2 overview](ger_mode_cmds_plan2.md) and step files **supersede** the illustrative §4.7 JSON example where a candidate may remain `tts_match: false` in the **final** Phase 1 deliverable. Under Plan 2, **Step 5b** requires **per–`test_phrases[]` index** TTS closure (normalized exact match for an assigned phrase) **or** an explicit **`needs_manual_redesign`** flag while iterating closure — but **Phase 2 entry** ([Step 6](ger_mode_cmds_plan2.step6.md)) requires **`needs_manual_redesign` absent everywhere** in `command_registry.json` (resolve escapes and re-close first). Optional [Pre-5 rework](ger_mode_cmds_plan2.rework_pre_step5.md) runs when phrase inventory or Step 4 outputs are stale. The repository [implementation_prompt.md](implementation_prompt.md) is unchanged; session ordering for Pre-5 / Step 5 / 5b is documented in the overview and rework playbook.

---

*This strategy document is the input for building a detailed implementation plan with concrete file changes, script implementations, and a step-by-step execution checklist.*
