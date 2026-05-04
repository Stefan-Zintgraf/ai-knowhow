# Step 2 — Extract Vosk vocabulary

**Status:** [x]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

---

## Goal

Parse **`vosk-model-de-0.6/graph/words.txt`** into **`vosk_vocabulary.txt`** (one word per line or documented format). Cross-reference every token in each registry `current_phrase` and parametric test phrases; emit an **OOV report** for tokens not in the vocabulary.

Strategy reference: §4.2, §10 Step 2.

---

## Tasks

1. Implement vocabulary extraction (path to model configurable or relative to known Talon layout).

2. Normalize tokens consistently (lowercase if model list is lowercase; document).

3. Flag OOV tokens per registry row; write `registry_oov_report.txt` or stdout summary.

---

## Verifiable result

- [x] `vosk_vocabulary.txt` exists and line count matches `words.txt`.
- [x] OOV report lists every phrase containing OOV tokens (expect some before optimization).
- [x] Script is repeatable on a clean checkout.
- [x] Git: vocabulary snapshot committed.

---

## Automated gate

```bash
python user/talon_german/extract_vosk_vocabulary.py
# Expect: vosk_vocabulary.txt + OOV summary non-zero exit if broken paths
```

---

## Notes for the agent

- Model path may differ per machine; fail fast with a clear message if `words.txt` is missing.
- **Phrase / inventory churn:** If registry phrases change after Step 4 ran, follow [rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md) before Step 5.
