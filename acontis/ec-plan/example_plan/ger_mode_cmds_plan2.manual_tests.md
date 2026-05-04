# Plan 2 — Manual live smoke (post-integration)

This checklist complements [ger_mode_cmds_plan2.step11.md](ger_mode_cmds_plan2.step11.md). Run after **automated suites are green** and **`command_registry.json`** drives runtime phrases. Assumes Plan 2 Phase 1 (through Step **5b** / Pre-5 rework as applicable) is complete per [ger_mode_cmds_plan2.md](ger_mode_cmds_plan2.md).

**Rule:** Run **twice**: once with **Vosk**, once with **Groq**. Switch backends using the registry's `selected_phrase` for the backend-switch commands. Complete all sections **2–10** for one backend, then switch and repeat.

**Phrase lookup:** Every "Say" column below uses **placeholder names** (e.g. *phrase for save*). Before testing, look up the actual `selected_phrase` in `command_registry.json` for each referenced command id. If a phrase was renamed during optimization, use the new wording.

---

## 1. Before you start

1. Run `test_text_level.py` full suite and `test_recognition_level.py` (or project-standard recognition gate).
2. Run `verify_commands.py --batch-replay` if you changed `whisper.config` or aliases since last green.
3. Enter **German mode** and open a scratch buffer.

---

## 2. Mode and system routing

Perform in **dictation** or **command** as indicated.

| Step | Mode | Say (registry id) | Expected |
|------|------|-------------------|----------|
| 2.1 | command | `sys_diktat` phrase | Switches to dictation input mode. |
| 2.2 | dictation | `sys_kommando` phrase | Switches to command input mode. |
| 2.3 | dictation | backend-switch phrase (e.g. `sys_vosk` / `sys_groq`) | Backend switches to the one you requested. |
| 2.4 | dictation | `sys_englisch` phrase | Exits German mode. Re-enter before continuing. |

---

## 3. Dictation — next-word formatting

Stay in **dictation** (`sys_diktat` phrase if needed).

| Step | Say (registry id) | Then / note | Expected |
|------|-------------------|-------------|----------|
| 3.1 | `dict_fmt_gross` phrase | then plain text, e.g. `hallo welt` | Next insertion is capitalized. |
| 3.2 | `dict_fmt_klein` phrase | then `HELLO` or similar | Next insertion lowercased. |
| 3.3 | `dict_fmt_kein_leerzeichen` phrase | then text that would add a space | Next insert obeys "no space before" behavior. |

---

## 4. Dictation — retroactive commands

Stay in **dictation**. For each row, **prepare** the buffer so the last dictated chunk matches the scenario, then say the command.

| Step | Prepare | Say (registry id) | Expected |
|------|---------|-------------------|----------|
| 4.1 | Dictate text so last insert is multi-word | `dict_retro_gross_das` phrase | Prior chunk capitalized. |
| 4.2 | Fresh buffer, **no** prior dictation insert | `dict_retro_gross_das` phrase | No destructive edit; optional noop notification. |
| 4.3 | Last insert e.g. `Hello` | `dict_retro_klein_das` phrase | Last chunk lowercased. |
| 4.4 | Last insert contains a removable space | `dict_retro_kein_leerzeichen_das` phrase | Space removed / merged per spec. |
| 4.5 | Last insert single token, no space | `dict_retro_kein_leerzeichen_das` phrase | Safe behavior (replace or no-op). |
| 4.6 | Last insert e.g. `mist` | `dict_retro_streich_das` phrase | Last insert deleted. |
| 4.7 | No prior insert | `dict_retro_streich_das` phrase | No destructive edit; optional noop notification. |
| 4.8 | Last insert e.g. `auswahl` | `dict_retro_markiere_das` phrase | Selection extends over last insert. |
| 4.9 | No prior insert | `dict_retro_markiere_das` phrase | No selection harm; optional noop notification. |

---

## 5. Dictation — navigation (parametric)

Stay in **dictation**. Use a buffer with multiple lines/words to see movement. Use both **singular and plural** `test_phrases` from the registry for each parametric family.

| Step | Say (registry id + test form) | Expected |
|------|-------------------------------|----------|
| 5.1 | `dict_nav_up` plural phrase (e.g. N=3) | Cursor moves up. |
| 5.2 | `dict_nav_up` singular phrase (e.g. N=1) | Cursor moves up one line. |
| 5.3 | `dict_nav_down` phrase | Cursor moves down. |
| 5.4 | `dict_nav_left` phrase (word unit) | Word-left movement. |
| 5.5 | `dict_nav_right` phrase (word unit) | Word-right movement. |
| 5.6 | `dict_nav_line_start` phrase | Cursor to line start. |
| 5.7 | `dict_nav_line_end` phrase | Cursor to line end. |

---

## 6. Dictation — invalid navigation (negative / fallthrough)

Stay in **dictation**. **Expected:** phrase is **inserted as plain text**, not executed as navigation.

| Step | Say | Expected |
|------|-----|----------|
| 6.1 | Navigation phrase with invalid word-number (e.g. `einundzwanzig`) | Inserted verbatim. |
| 6.2 | Navigation phrase with zero count | Inserted verbatim. |
| 6.3 | Navigation phrase incomplete (missing count) | Insert fallthrough. |
| 6.4 | Navigation phrase with invalid unit (e.g. `bananen`) | Insert fallthrough. |

---

## 7. Dictation — selection, deletion, correction

Stay in **dictation**.

| Step | Say (registry id) | Expected |
|------|-------------------|----------|
| 7.1 | `dict_sel_left` phrase (e.g. 3 words) | Selection extends left by words. |
| 7.2 | `dict_sel_right` phrase (e.g. 2 characters) | Selection extends right by characters. |
| 7.3 | `dict_del_left` phrase (e.g. 2 words) | Deletes left extent. |
| 7.4 | `dict_corr_streich_markierung` phrase | Clears current selection. |

---

## 8. Dictation — literal and spelling

Stay in **dictation**.

| Step | Say (registry id) | Expected |
|------|-------------------|----------|
| 8.1 | `dict_lit` phrase + payload (e.g. `foo bar`) | Inserts `foo bar` (literal path). |
| 8.2 | `dict_fmt_gross` phrase, then `dict_lit` phrase + `test` | Literal respects pending capitalize. |
| 8.3 | `dict_lit` phrase **only** (no payload) | Inserts the literal keyword as normal text (fallthrough). |
| 8.4 | `dict_spell` phrase + letters (e.g. `a b c`) | Inserts spelled letters per spec. |

---

## 9. Command mode — `schreib` and registry commands

Switch to **command** (`sys_kommando` phrase). Use scratch buffer.

| Step | Say | Expected |
|------|-----|----------|
| 9.1 | `schreib hallo` | Inserts `hallo`, does **not** run an unrelated command. |
| 9.2 | `schreib` alone | Prefix only -- empty payload handling (notification / no insert per spec). |
| 9.3 | `schreib speichern` | Inserts the **word** "speichern", does **not** trigger save. |
| 9.4 | `schreiben etwas` | **No** `schreib` prefix match -- unrecognized / no insert. |
| 9.5 | `cmd_save` phrase | Registry: save action fires. |
| 9.6 | `cmd_enter` phrase | Registry: enter key fires. |
| 9.7 | Say an **old** phrase kept as **alias** (if any exist) | Same behavior as new phrase. |

---

## 10. Routing — cross-mode and false-positive checks

| Step | Mode | Say | Expected |
|------|------|-----|----------|
| 10.1 | dictation | `cmd_save` phrase (e.g. `speichern`) | Text **inserted**, not save. |
| 10.2 | command | unrecognized phrase (e.g. `nix da`) | Unrecognized command path (log / no exec). |
| 10.3 | dictation | normal German prose | Plain dictation insert. |
| 10.4 | dictation | Construct a sentence that contains a command keyword | Command does **not** fire; text inserted as dictation. |

---

## 11. Repeat for the other backend

1. In **dictation**, say the backend-switch phrase to select the backend you have **not** yet used.
2. Repeat **sections 2–10** (you may shorten section 2 if mode switching is already verified).

---

## 12. Completion checklist

Manual testing is satisfied when **all** apply:

- [ ] Sections **2–10** completed with **Vosk**; no blocking wrong behavior.
- [ ] Sections **2–10** completed with **Groq**; same criterion.
- [ ] If you changed code after manual testing: full `test_text_level.py` and `test_recognition_level.py --backend all` pass again.
- [ ] Any failure notes recorded (backend, step id, misrecognition vs. bug).

---

## 13. After microphone or PC change

1. Run `select_best_phrase.py --reset <id>` for affected commands **or** `--reset-all` if needed.
2. Re-run Steps 7–9 (tune, batch replay, Groq) before trusting production.

---

## Related documents

- [ger_mode_cmds_test2.md](ger_mode_cmds_test2.md)
- [ger_mode_cmds_plan2.step11.md](ger_mode_cmds_plan2.step11.md)
