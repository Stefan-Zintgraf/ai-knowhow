---
name: status
description: Compact project dashboard — current WI + phase, skill freshness, next action. Use when user says "/status", "show status", "what's next", or wants a project overview.
---

# `/status` — Project Dashboard

Show a compact dashboard: current work-item + phase, skill freshness, and the highest-priority next action. Results are stored in `latest_status.md` inside the skill folder for later reference.

## Hard Rules

1. **Scripts are authoritative.** All staleness checks and WI state come from the 4 scripts in `.claude/skills/status/`. Never compute git timestamps yourself.
2. **Parse Phase Skills table fresh each run.** Read `coding_plan.md` and extract the table under `### Phase Skills table`. Build `$SkillsJson` from it — do not hardcode.
3. **A12 gate.** If `skills/output/phase.md` does not exist, skip the Current WI block and print: `⚠ A12 (/phase) not yet built — WI block unavailable`.
4. **Repo root.** Pass `-RepoRoot` as the absolute path of the repo root (the folder containing `coding_plan.md`).
5. **Skill folder.** The skill folder is the directory containing this `skill.md` file. Resolve it as an absolute path. Scripts live here; output files are written here too.
6. **No writes outside skill folder or `latest_status.md`.** This skill never modifies repo files.

## Steps

### 1 — Locate paths

- `$RepoRoot` — absolute path of the directory containing `coding_plan.md`.
- `$SkillDir` — absolute path of the directory containing this `skill.md` (`.claude/skills/status/`).

### 2 — Check A12 gate

Check whether `$RepoRoot/skills/output/phase.md` exists.  
Set `$a12Built = true` if it exists, `false` otherwise.

### 3 — Parse Phase Skills table → build and save SkillsJson

Read `$RepoRoot/coding_plan.md`.  
Find the section `### Phase Skills table`.  
Extract every data row (skip the header and separator rows).  
For each row, extract:
- `id` — column `#` (e.g. `A11`)
- `name` — column `Skill name` (strip backticks)
- `source_docs` — column `Source doc`: extract all file paths that match `\w[\w/._-]+\.md` (strip markdown link syntax `[text](path)`)

Skip rows where `source_docs` would be empty (e.g. `A5 parallel-loop` with `—`).

Produce a JSON object and write it to `$SkillDir/skills.json`:
```json
{
  "created_at": "<ISO timestamp of now>",
  "skills": [
    { "id": "A11", "name": "distill-idea", "source_docs": ["gr/gr_idea.md"] },
    ...
  ]
}
```

Pass the `skills` array (as a JSON string) to the scripts as `$SkillsJson`.

### 4 — Run scripts 1–3

Scripts live in `$SkillDir`. Run all three. Capture each stdout as a JSON string.

```powershell
$ps = "powershell.exe"   # or "pwsh" if available

$activeWIJson = & $ps -NonInteractive -NoProfile -File "$SkillDir/Get-ActiveWI.ps1" `
    -RepoRoot $RepoRoot

$freshnessJson = & $ps -NonInteractive -NoProfile -File "$SkillDir/Get-SkillFreshness.ps1" `
    -RepoRoot $RepoRoot -SkillsJson $SkillsJson

$mapTestJson = & $ps -NonInteractive -NoProfile -File "$SkillDir/Get-MapAndTestFreshness.ps1" `
    -RepoRoot $RepoRoot -SkillsJson $SkillsJson
```

If any script exits with a non-zero code, show its stderr and stop with an error message.

### 5 — Run script 4

```powershell
$nextActionJson = & $ps -NonInteractive -NoProfile -File "$SkillDir/Get-NextAction.ps1" `
    -RepoRoot $RepoRoot `
    -ActiveWIJson $activeWIJson `
    -FreshnessJson $freshnessJson `
    -MapTestJson $mapTestJson
```

### 6 — Format dashboard

Parse all four JSON strings. Build the dashboard markdown using the format below.

---

#### Section A — Current WI

If `$a12Built` is false:
```
⚠ A12 (/phase) not yet built — WI block unavailable
```

If `$a12Built` is true and `activeWI.found` is false and `activeWI.error` is null:
```
**Current WI:** none — run `/triage-idea` to start
```

If `$a12Built` is true and `activeWI.found` is false and `activeWI.error` is non-null:
```
**Current WI:** error — <error>
```

If `$a12Built` is true and `activeWI.found` is true and `activeWI.error` is non-null:
```
**Current WI:** <wi> — error: <error>
```

If `$a12Built` is true and `activeWI.found` is true and `activeWI.error` is null:
```
**Current WI:** <wi>
**Phase:** <current_phase> (<phase_status>) | mode: <mode> | actor: <last_actor>
**Entered:** <entered_at>
**Blockers:** <blockers joined by "; " or "none">
**Tripwire halt:** <tripwire_halt>
```

---

#### Section B — Skill Freshness

Header: `## Skill Freshness`

If `freshness.any_stale` is false:
```
All skills current ✓
```

For each skill in `freshness.skills`:
- If `stale_input` is true: `⚠ [<id>] <name>  stale input → <cmd_input>`
- Else if `stale_compiled` is true: `⚠ [<id>] <name>  stale compiled → <cmd>`
- Else: `✓ [<id>] <name>`

Then check `mapTest.rule_skill_map`:
- If `stale` is true: `⚠ rule-skill map stale → /update-rule-skill-map`
- Else: `✓ rule-skill map`

Then for each entry in `mapTest.test_fixtures`:
- If `cmd_compile` is set: `⚠ [test] <name>  skill not compiled`
- Else if `cmd` is set: `⚠ [test] <name>  fixtures stale → <cmd>`
- Else: `✓ [test] <name>`

---

#### Section C — Next Action

Header: `## Next Action`

If `nextAction.top_action` is null:
```
Nothing to do — all items complete.
```

If `nextAction.top_action.priority` is 5 and `fallback_next_todo` is not null:
```
**Priority 5 — next todo:**
> <fallback_next_todo>
```

For priority 1–4, group actions at the same priority:
```
**Priority <N> — <reason>:**
  <cmd1>
  <cmd2>
```

---

### 7 — Save to latest_status.md and print

Prepend a timestamp header to the dashboard markdown:
```
# Status — <ISO timestamp of now>
```

Write the full result to `$SkillDir/latest_status.md` (overwrite if exists).

Print the same content to the user.
