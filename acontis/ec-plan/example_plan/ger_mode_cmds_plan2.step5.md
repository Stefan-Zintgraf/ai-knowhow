# Step 5 — Generate and rank candidates

**Status:** [x]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

**Prerequisites:** [Pre-5 rework](ger_mode_cmds_plan2.rework_pre_step5.md) must be complete or marked N/A (overview **Pre-5** row `[x]`) **before** this step. After this session, stop; run [Step 5b](ger_mode_cmds_plan2.step5b.md) in a **fresh** session.

---

## Goal

For each **`test_phrases[]` index** that failed the Step 4 TTS screen (and any row-level `tts_fail`), auto-generate **5 candidates** (min 3, max 10) using strategies: inflection, synonym table, structural rewrite, length variants — **vocabulary-filtered**. **Per-variant coverage:** parametric rows need candidates that address **each** failing variant, not only one phrase per row. TTS-screen each candidate; **rank** by exact match, then edit distance, then shorter phrase. Apply **diversity dedup** (>50% token overlap). Set **`tts_status`** **`candidates_ready`**.

Individual candidates may still show `tts_match: false` until [Step 5b](ger_mode_cmds_plan2.step5b.md) closes Phase 1.

**Test phrases:** Do **not** change `test_phrases[]` to work around failures — see [Test phrase stability (manual redesign)](ger_mode_cmds_plan2.md#test-phrase-stability-manual-redesign) in the overview. Generation adjusts **candidates**, not the inventory test strings.

**Registry file safety:** Do **not** use `git restore`, `git checkout --`, or any other command that **replaces or discards** the working copy of `user/talon_german/command_registry.json` (or reverts it to `HEAD`) in order to recover from a bad script run, a failed gate, or agent error. That can **erase the operator’s uncommitted edits** (including deliberate `test_phrases[]` / `current_phrase` work). If recovery is needed, **stop**, preserve or stash the user’s changes first, and **ask the user** before resetting tracked files.

Strategy reference: §4.5–§4.7, §10 Step 5. Plan 2 final state: [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) “Phase 1 exit”.

---

## Tasks

1. Implement generation pipeline in `generate_candidates.py` (or sibling module).

2. Enforce **every word ∈ vosk_vocabulary.txt** before TTS.

3. Store ranked candidate objects in registry; schema may need **per–`test_phrase_index`** binding so each variant can be satisfied separately (see [architecture](ger_mode_cmds_architecture2.md)).

4. For `tts_pass` rows (all variants passing), leave `candidates` empty but keep note that Phase 2 still records real voice (on-the-fly candidates if surprise fail).

---

## Verifiable result

- [x] Every failing **test phrase variant** has ≥3 ranked candidates (or `needs_manual_redesign` with explicit flag if generation empty).
- [x] No candidate contains OOV tokens.
- [x] Diversity rule applied (document algorithm in code comment).
- [x] Git: registry + any generator code committed.

---

## Automated gate

```bash
python user/talon_german/generate_candidates.py --phase generate-and-rank
```

---

## Notes for the agent

- **On-the-fly** candidate generation for TTS-pass rows can share the same module; defer wiring to Step 6 if needed.
- If the registry still has any `needs_manual_redesign` row after this step (or after Step 5b in the next session), **stop** at the end of Phase 1 work; do **not** start Step 6 until those rows are cleared ([overview](ger_mode_cmds_plan2.md) Step 6 entry).
