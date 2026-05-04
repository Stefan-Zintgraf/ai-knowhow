# Pre–Step 5 rework (conditional)

**Status:** [x]

**Session rule:** When this playbook applies, treat it as **one** implementation session: follow the checklist, run gates, commit, mark this file and the [overview](ger_mode_cmds_plan2.md) **Pre-5** row `[x]`, then **stop**. Do **not** start [Step 5](ger_mode_cmds_plan2.step5.md) in the same conversation — use a **fresh session** for Step 5. (The repo [implementation_prompt.md](implementation_prompt.md) is unchanged; ordering lives here and in the overview.)

---

## When this applies (triggers)

Run the rework sequence if **any** of the following is true **before** you begin Step 5:

1. **`command_registry.json`** was changed after the last **Step 4** TTS screen (inventory, `current_phrase`, or `test_phrases`).
2. **Step 2** vocabulary / OOV check may be stale (new tokens, model path change, or phrases edited).
3. **`synonym_table.json`** was extended or fixed to support candidate generation — downstream TTS screening should see a consistent baseline.
4. **`tts_report.json`** / registry `tts_pass` / `tts_fail` from Step 4 no longer match the phrases you are about to optimize (any phrase surface drift).
5. **After [Step 5c](ger_mode_cmds_plan2.step5c.md) is implemented:** `python user/talon_german/check_phase1_inputs.py` reports **STALE** (registry or synonym canonical content drift vs `phase1_inputs_baseline.json`).

If **none** of the triggers apply (registry and Step 4 artifacts are already consistent with starting Step 5), you may **skip** the rework sequence: document “N/A” in the commit message or a one-line note, mark **Pre-5** `[x]` in the overview, and proceed — Step 5 still starts in a **new** session per the usual one-step-per-session rule.

---

## Ordered rework sequence

Repeat until stable (same ordering every time):

1. **Align registry** — [Step 1](ger_mode_cmds_plan2.step1.md) tools / manual edits as needed; run `validate_registry.py` when the registry changes.
2. **Vocabulary** — [Step 2](ger_mode_cmds_plan2.step2.md): ensure `vosk_vocabulary.txt` and OOV reporting match current phrases.
3. **Synonyms** — [Step 3](ger_mode_cmds_plan2.step3.md): extend `synonym_table.json` if generation will need new seeds; run the Step 3 validator.
4. **TTS pre-screen** — [Step 4](ger_mode_cmds_plan2.step4.md): re-run `generate_candidates.py --phase tts-screen-current`; refresh `tts_report.json` and registry `tts_pass` / `tts_fail`.

**Cheatsheet:** If user-visible wording in `command_registry.json` changes during rework, update [talon_cheat_sheet_ger.md](../../../talon_cheat_sheet_ger.md) in the same change set or immediately after (see [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) workspace conventions).

**Git:** Commit artifacts after each wave; do not skip automated gates.

---

## Verifiable result

- [x] Triggers evaluated and documented: **N/A** — no commits after Step 4 (`3049b90`) touched `command_registry.json`, `vosk_vocabulary.txt`, `synonym_table.json`, or `tts_report.json`; inventory and TTS baseline remain aligned.
- [x] Rework sequence skipped (not required). Prior Steps 2–4 artifacts and gates remain authoritative.
- [x] Overview **Pre-5** Status and this file’s Status updated to `[x]`.

---

## Automated gate

No single global command — use the gates defined in Steps 2, 3, and 4 in sequence. If N/A, no command run is required.

---

## Related

- [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md) — execution order and session rules  
- [ger_mode_cmds_plan2.step5.md](ger_mode_cmds_plan2.step5.md) — next step after Pre-5 is complete  
