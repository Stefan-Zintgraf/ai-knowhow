# Step 1 — Build command registry

**Status:** [x]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

---

## Goal

Produce **`user/talon_german/command_registry.json`** as the single inventory of German commands: ids, modes, actions, `current_phrase`, empty `candidates`, `selected_phrase: null`, `aliases: []`, `tts_status: "pending"`, `real_voice_status: "none"`.

**Source of extraction:** `GERMAN_COMMANDS`, `parse_dictation_command()` routing surface, `_try_system_command()` — see strategy §4.3, §10 Step 1.

**Parametric patterns:** one registry row each; document **two test phrases** per row (singular `N=1`, plural `N=2` wording) where applicable.

**Extended inventory (Step 1 refresh):** command-mode **neue zeile** (Shift+Enter, newline without send vs **eingabe**); dictation **line/paragraph/page/document/indent** phrases (`markiere zeile`, `geh dokument anfang`, `einrücken`, …) — see `german_dictation_commands.py` and `build_command_registry.py`. Current totals: **53** patterns, **62** test phrases.

---

## Registry schema

Each entry in `command_registry.json` must have exactly these fields:

```json
{
  "id": "cmd_save",
  "mode": "command",
  "action": "edit.save",
  "description": "Save the current file",
  "current_phrase": "speichern",
  "test_phrases": ["speichern"],
  "candidates": [],
  "selected_phrase": null,
  "aliases": [],
  "tts_status": "pending",
  "real_voice_status": "none",
  "groq_status": null
}
```

For **parametric commands**, `test_phrases` contains both the singular and plural forms:

```json
{
  "id": "dict_nav_up",
  "mode": "dictation",
  "action": "nav_up",
  "description": "Move cursor up N lines",
  "current_phrase": "geh hoch {N} zeile(n)",
  "test_phrases": ["geh hoch eins zeilen", "geh hoch zwei zeilen"],
  "candidates": [],
  "selected_phrase": null,
  "aliases": [],
  "tts_status": "pending",
  "real_voice_status": "none",
  "groq_status": null
}
```

For non-parametric commands, `test_phrases` contains one entry identical to `current_phrase`.

## Tasks

1. Implement a script (or one-off extractor) that parses the codebase and writes JSON matching the schema above (derived from strategy §4.3 with the addition of the `test_phrases` and `groq_status` fields).

2. Ensure **stable `id`** values align with **`test_corpus.py`** entry ids wherever there is a 1:1 mapping.

3. Include human-readable `description` per row for Phase 2 prompts.

4. Validate JSON loads; no duplicate `id`.

---

## Verifiable result

- [x] `command_registry.json` exists under `user/talon_german/` (not under `ger_mode_cmds_plan2/`).
- [x] Every command mode, dictation pattern, and system command from strategy §4.3 is represented.
- [x] Parametric rows have `test_phrases` with both singular and plural forms; non-parametric rows have `test_phrases` with one entry matching `current_phrase`.
- [x] Corpus id alignment documented in a short comment block or README snippet if any id is synthetic ([`../step1_corpus_alignment.md`](../step1_corpus_alignment.md)).
- [x] `talon_cheat_sheet_ger.md` (repository root) reflects the same `current_phrase` / representative `test_phrases` as the registry bootstrap (user-facing quick reference).
- [x] Git: committed when implementation lands.

---

## Automated gate

From repository root (`%APPDATA%/talon`):

```bash
python user/talon_german/validate_registry.py
```

Regenerate `command_registry.json` after editing `build_command_registry.py`:

```bash
python user/talon_german/build_command_registry.py
```

Gate confirms: valid JSON; row count within the validator band; all required keys present; every dictation `test_phrase` parses via `parse_dictation_command()`.

---

## Notes for the agent

- Registry is a **planning artifact immediately**; runtime load happens only in Step 11.
- If extraction is ambiguous, prefer explicit rows over merging behaviors.
- **Phrase / inventory churn:** If you change this registry after Step 4 has already run, follow [rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md) before Step 5.
