# Step 4 — TTS pre-screen all current phrases

**Status:** [x]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

---

## Goal

Batch-generate TTS for **every** test phrase (~40), run **Vosk** on each WAV using the **same pipeline** as live use (`corpus_tts` / whisper worker path). Produce a **TTS evaluation report** and set registry **`tts_status`** to **`tts_pass`** or **`tts_fail`**.

Strategy reference: §4.4, §10 Step 4. **TTS is screening only** — not final acceptance.

---

## Tasks

1. Reuse or extend `ger_mode_cmds_test/corpus_tts.py` (or equivalent) per architecture doc.

2. For each phrase, record: expected phrase, recognized text, exact match, edit distance.

3. Update `command_registry.json` **`tts_status`** fields.

4. Write machine-readable summary (`tts_report.json`) optional but recommended.

---

## Verifiable result

- [x] All ~40 phrases processed without manual clicks.
- [x] Report matches strategy §4.4 shape (totals, PASS list, FAIL list).
- [x] Registry reflects `tts_pass` / `tts_fail` per row (and per test phrase if schema splits rows).
- [x] Git: report + registry updates committed. TTS WAVs are ephemeral (generated on the fly) and not committed.

---

## Automated gate

```bash
python user/talon_german/generate_candidates.py --phase tts-screen-current
# or dedicated script; must exit 0 on full pass of the batch job
```

---

## Notes for the agent

- Fixed audio params for TTS batch should match “reasonable defaults” documented in the script.
- Failures are **expected**; non-zero exit should mean tool error, not “any tts_fail”.
- **Re-screen:** If upstream phrases or registry change, re-run this step; see [rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md) before Step 5.
