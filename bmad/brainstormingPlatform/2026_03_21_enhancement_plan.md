# Enhancement Plan: Brainstorming Skill — Dual-Mode Support + Testing

## Context

The `start-brainstorming` skill currently only supports creating brainstorming sessions inside `BRAINSTORMING_FOLDER`. The enhancement adds an alternative: brainstorming directly in the current folder (e.g., for project-specific brainstorming). Additionally, the `BRAINSTORMING_FOLDER` env var handling should be more user-friendly (create if missing, confirm if exists). Finally, the skill must be automatically tested with Sonnet and test logs produced.

---

## Step 1: Modify `install-bmad.bat`

**File**: `install-bmad.bat`

Add a `--mode` flag as the first argument to support two modes:

```
install-bmad.bat --mode folder  <topic> <platform> [lang] [outlang]   # existing behavior
install-bmad.bat --mode current <platform> [lang] [outlang]           # new: install in CWD
```

Changes:
- **Parse `--mode`**: If `%1` is `--mode`, consume `%2` as MODE (`folder`|`current`), shift args by 2. If no `--mode`, default to `folder` (backward compat).
- **`folder` mode**: Existing behavior — require `BRAINSTORMING_FOLDER`, require topic, create `%BRAINSTORMING_FOLDER%\<topic>`, install with `--modules cis`.
- **`current` mode**: Skip `BRAINSTORMING_FOLDER` check, skip topic, set `PROJECT_DIR=%CD%`, skip mkdir/exists-check, install with `--modules cis,bmm`.

Backward compat: `install-bmad.bat topic platform lang outlang` (no `--mode`) still works as folder mode.

---

## Step 2: Update SKILL.md (3 files)

**Files**:
1. `.claude\skills\start-brainstorming\SKILL.md` (claude-code, local)
2. `%USERPROFILE%\.claude\skills\start-brainstorming\SKILL.md` (claude-code, global)
3. `.cursor\skills\start-brainstorming\SKILL.md` (cursor)

New workflow inserts a **Step 0 — Location choice** before the existing steps:

> "Where do you want to brainstorm?
> (a) In the BRAINSTORMING_FOLDER (dedicated brainstorming directory)
> (b) In the current folder (brainstorm within this project)"

### Option (a) — BRAINSTORMING_FOLDER mode:
1. Check if `BRAINSTORMING_FOLDER` env var is set.
2. If set: show path, ask user to confirm or provide new path.
3. If not set: ask user for a path, then `setx BRAINSTORMING_FOLDER "<path>"` + `set` for current session.
4. Continue with existing flow: ask topic, languages.
5. Run: `install-bmad.bat --mode folder <topic> <platform> <lang> <outlang>`

### Option (b) — Current folder mode:
1. Skip BRAINSTORMING_FOLDER handling.
2. Skip topic question.
3. Ask languages only.
4. Run: `install-bmad.bat --mode current <platform> <lang> <outlang>`
5. Report: "BMAD installed in current directory with CIS + BMM modules."

Also update: description frontmatter, "When to use" triggers, shortcuts section.

---

## Step 3: Update `readme.md`

- Document the new `--mode` parameter.
- Add "Option B: Brainstorm in current folder" section.
- Note that `BRAINSTORMING_FOLDER` is now handled interactively by the skill.

---

## Step 4: Automated Testing

### 4a: Batch-level tests — `test-brainstorming.bat`

Test cases (output logged to `test-logs\` folder):

| # | Case | Expected |
|---|------|----------|
| 1 | Folder mode, happy path | Exit 0, dir created |
| 2 | Folder mode, missing BRAINSTORMING_FOLDER | Exit 1, error msg |
| 3 | Folder mode, topic with spaces | Exit 1, error msg |
| 4 | Folder mode, duplicate topic | Exit 1 on 2nd run |
| 5 | Current mode, happy path | Exit 0, installed in CWD with cis,bmm |
| 6 | Backward compat (no --mode flag) | Exit 0, folder mode |
| 7 | Invalid platform | Exit 1 |
| 8 | Invalid language | Exit 1 |

### 4b: Skill-level tests via `claude` CLI with Sonnet

```bash
claude --model sonnet -p "<prompt>" 2>&1 | tee test-logs/skill-test-X.log
```

Test prompts:
- A1: "Start brainstorming" -> should ask location choice
- A2: "Start brainstorming in BRAINSTORMING_FOLDER for topic test_sonnet" -> folder mode
- B1: "Brainstorm here" -> current-folder mode
- B2: "Start brainstorming in the current folder, English" -> current-folder mode

---

## Implementation Order

1. `install-bmad.bat` — foundation for both modes
2. SKILL.md (all 3 copies) — new workflow
3. `readme.md` — documentation
4. `test-brainstorming.bat` — create and run batch tests
5. Skill tests with Sonnet — run and capture logs
6. Review logs, verify all use cases pass
