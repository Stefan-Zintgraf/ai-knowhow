# Step 3 — Build synonym table

**Status:** [x]

**Session rule:** Complete this step, run the automated gate, commit, mark `[x]`, then stop.

---

## Goal

Author **`synonym_table.json`**: curated rewrite rules (failing fragment → candidate substitutions / structural hints) informed by strategy §6.2 and §4.5. **Validate** that suggested replacement tokens exist in **`vosk_vocabulary.txt`**.

This is the **primary manual authoring** step in Phase 1; all downstream candidate generation depends on it.

---

## Tasks

1. Create JSON structure (documented in script readme or top of file): e.g. list of `{ "trigger": "...", "replacements": ["...", ...], "notes": "..." }`.

2. Run validator against `vosk_vocabulary.txt`; flag or strip OOV replacements.

3. Cover known failure families: `geh`, `klein`, compounds (`zeilenanfang`), loanwords (`vosk`, `groq`), stems (`streich`, `buchstabiere`), `wörtlich`.

---

## Verifiable result

- [x] `synonym_table.json` exists and validates against schema.
- [x] Validator reports **zero OOV** replacement tokens (or explicitly quarantined entries with `enabled: false`).
- [x] At least the rows implied by strategy §6.2 table are present or superseded by better entries with rationale in commit message.
- [x] Git: committed.

---

## Automated gate

```bash
python user/talon_german/validate_synonym_table.py
```

---

## Notes for the agent

- Prefer **high-frequency German** multi-word phrases over rare compounds.
- Keep the table small and maintainable (~15–20 core entries per strategy §11).
- **Phrase / synonym churn:** If you extend this table after Step 4, follow [rework_pre_step5.md](ger_mode_cmds_plan2.rework_pre_step5.md) before Step 5 (typically re-run Steps 2–4 in order).
