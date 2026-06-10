# Status Skill — PowerShell Script Interfaces

Four scripts, each emitting JSON to stdout. The skill invokes all four,
merges outputs, formats the dashboard. LLM cost = formatting only.

Repo root passed as `-RepoRoot` to every script (default: `.`).

---

## 1. `Get-ActiveWI.ps1` — Active Work-Item + Phase

### Purpose
Read `plan/ACTIVE`, resolve `plan/<WI>/phase_status.md`, extract YAML
frontmatter fields.

### Parameters
| Param       | Type   | Required | Default |
|-------------|--------|----------|---------|
| `-RepoRoot` | string | no       | `.`     |

### Output (JSON)
```jsonc
{
  "found": true,               // false when plan/ACTIVE missing or == "<none>"
  "wi": "7_add-dark-mode",     // null when !found
  "current_phase": "aln",      // from frontmatter
  "phase_status": "in-progress",
  "mode": "mini",
  "blockers": [],
  "tripwire_halt": false,
  "entered_at": "2026-05-25T14:00:00Z",
  "last_actor": "human",
  "error": null                 // non-null string if phase_status.md missing or unparseable
}
```

### Edge cases
| Condition | Behavior |
|-----------|----------|
| `plan/ACTIVE` missing | `{ "found": false, "error": "no_active_file" }` |
| `plan/ACTIVE` == `<none>` | `{ "found": false, "error": null }` |
| `phase_status.md` missing | `{ "found": true, "wi": "…", "error": "phase_status_missing" }` |
| YAML parse failure | `{ "found": true, "wi": "…", "error": "yaml_parse_error: <detail>" }` |

### Implementation notes
- Parse YAML frontmatter between `---` fences. Only need key: value lines,
  no nested structures except `blockers` (a YAML list).
- PowerShell `ConvertTo-Json` for output.

---

## 2. `Get-SkillFreshness.ps1` — Skill & Input Staleness

### Purpose
For each skill in the Phase Skills table, compare last-commit timestamps of
source docs vs compiled output and input files.

### Parameters
| Param        | Type     | Required | Default |
|--------------|----------|----------|---------|
| `-RepoRoot`  | string   | no       | `.`     |
| `-SkillsJson`| string   | **yes**  | —       |

`-SkillsJson` is a JSON array describing the skills to check. The skill
(LLM) parses the Phase Skills table once and passes this in. This keeps the
script free of markdown parsing.

```jsonc
[
  {
    "name": "distill-idea",
    "source_docs": ["gr/gr_idea.md"],
    "id": "A11"
  },
  {
    "name": "align-concept",
    "source_docs": ["gr/gr_algn.md"],
    "id": "A1"
  }
  // ...
]
```

### Output (JSON)
```jsonc
{
  "skills": [
    {
      "id": "A11",
      "name": "distill-idea",
      "compiled_exists": true,
      "input_exists": true,
      "source_last_commit": "2026-05-27T10:00:00Z",  // latest across all source_docs
      "input_last_commit": "2026-05-26T08:00:00Z",    // skills/input/<name>-in.md
      "compiled_last_commit": "2026-05-25T12:00:00Z",  // skills/output/<name>.md
      "stale_compiled": true,      // source_last_commit > compiled_last_commit
      "stale_input": true,         // source_last_commit > input_last_commit
      "cmd": "/make-skill distill-idea",               // when stale_compiled && !stale_input
      "cmd_input": "/draft-skill-input distill-idea"   // when stale_input
    }
  ],
  "any_stale": true
}
```

### Timestamp logic
- `git log -1 --format=%aI -- <path>` per file. If file untracked or never
  committed → treat as epoch 0 (always stale).
- `source_last_commit` = max across all `source_docs` entries.
- `stale_compiled` = `source_last_commit > compiled_last_commit` (or compiled missing).
- `stale_input` = `source_last_commit > input_last_commit` (or input missing).
- `cmd` populated only when `stale_compiled && !stale_input`.
- `cmd_input` populated only when `stale_input`.

### Edge cases
| Condition | Behavior |
|-----------|----------|
| Compiled file missing | `compiled_exists: false`, `stale_compiled: true` |
| Input file missing | `input_exists: false`, `stale_input: true` |
| Source doc never committed | `source_last_commit: null`, `stale_*: false` (nothing to be stale against) |
| No git repo | Exit code 1, stderr message |

---

## 3. `Get-MapAndTestFreshness.ps1` — Rule-Skill Map + Test Fixtures

### Purpose
Two checks in one script (both are simple timestamp comparisons):
1. Rule-skill map freshness: any `gr/*.md` newer than `skills/rule_skill_map.md`.
2. Test fixture freshness: for each `skills/test/<name>/`, compare fixture
   timestamps against source docs and compiled skill.

### Parameters
| Param        | Type   | Required | Default |
|--------------|--------|----------|---------|
| `-RepoRoot`  | string | no       | `.`     |
| `-SkillsJson`| string | **yes**  | —       |

Same `-SkillsJson` format as script 2 (reuse the same object).

### Output (JSON)
```jsonc
{
  "rule_skill_map": {
    "exists": true,
    "stale": true,
    "map_last_commit": "2026-05-20T12:00:00Z",
    "gr_latest_commit": "2026-05-27T09:00:00Z",
    "cmd": "/update-rule-skill-map"     // only when stale
  },
  "test_fixtures": [
    {
      "name": "distill-idea",
      "fixtures_exist": true,
      "compiled_exists": true,
      "source_newer_than_fixtures": true,
      "fixtures_last_commit": "2026-05-24T10:00:00Z",
      "cmd": "/draft-skill-tests distill-idea"    // when source_newer_than_fixtures
    },
    {
      "name": "phase",
      "fixtures_exist": true,
      "compiled_exists": false,
      "source_newer_than_fixtures": false,
      "cmd_compile": "skill not compiled"         // when fixtures_exist && !compiled_exists
    }
  ]
}
```

### Timestamp logic
- **Map**: `gr_latest_commit` = max `git log -1 --format=%aI` across all `gr/*.md`.
  `stale` = `gr_latest_commit > map_last_commit` (or map file missing).
- **Fixtures**: `fixtures_last_commit` = max commit time across all files in
  `skills/test/<name>/`. `source_newer_than_fixtures` = `source_last_commit`
  (from SkillsJson source_docs) > `fixtures_last_commit`.
- Test dirs discovered by listing `skills/test/*/` — not limited to SkillsJson
  entries (catches orphaned test dirs too).

### Edge cases
| Condition | Behavior |
|-----------|----------|
| `skills/rule_skill_map.md` missing | `exists: false`, `stale: true` |
| No `gr/*.md` files | `stale: false` (nothing to compare) |
| Test dir exists but is empty | `fixtures_exist: false` |
| Test dir for skill not in SkillsJson | Still reported; `source_newer_than_fixtures: null` (can't determine) |

---

## 4. `Get-NextAction.ps1` — Priority-Ordered Next Step

### Purpose
Consumes output of scripts 1–3 (piped as JSON) and emits the single
highest-priority next action plus the full ordered list.

### Parameters
| Param             | Type   | Required | Default |
|-------------------|--------|----------|---------|
| `-RepoRoot`       | string | no       | `.`     |
| `-ActiveWIJson`   | string | **yes**  | —       |
| `-FreshnessJson`  | string | **yes**  | —       |
| `-MapTestJson`    | string | **yes**  | —       |

Each param receives the JSON string output of its respective script.

### Output (JSON)
```jsonc
{
  "actions": [
    {
      "priority": 1,
      "reason": "tripwire_halt is set",
      "cmd": "/triage-idea --remode"
    }
  ],
  "top_action": {
    "priority": 1,
    "reason": "tripwire_halt is set",
    "cmd": "/triage-idea --remode"
  },
  "fallback_next_todo": null   // populated at priority 5: first unchecked item text
}
```

### Priority rules (hardcoded)
| Priority | Condition | Action |
|----------|-----------|--------|
| 1 | `ActiveWIJson.tripwire_halt == true` | `"/triage-idea --remode"` |
| 2 | `MapTestJson.rule_skill_map.stale == true` | `"/update-rule-skill-map"` |
| 3 | Any skill with `stale_input == true` | `"/draft-skill-input <name>"` per skill |
| 4 | Any skill with `stale_compiled == true` (and input fresh) | `"/make-skill <name>"` per skill |
| 5 | All current | grep first `- [ ]` line from `coding_plan.md` work items section |

### Edge cases
| Condition | Behavior |
|-----------|----------|
| No active WI | Skip priority 1 check; don't error |
| Multiple stale at same priority | Emit all as separate `actions` entries at that priority |
| No `- [ ]` found | `fallback_next_todo: "all work items complete"` |

---

## Skill ↔ Script contract

```
┌──────────────────────────────────┐
│         /status skill (LLM)      │
│                                  │
│  1. Parse Phase Skills table     │
│     → build SkillsJson array     │
│                                  │
│  2. Invoke scripts in parallel:  │
│     Get-ActiveWI.ps1             │
│     Get-SkillFreshness.ps1       │
│     Get-MapAndTestFreshness.ps1  │
│                                  │
│  3. Pass outputs to:             │
│     Get-NextAction.ps1           │
│                                  │
│  4. Format combined JSON →       │
│     dashboard markdown           │
└──────────────────────────────────┘
```

### What the LLM does (not scriptable)
- Parse Phase Skills table from `coding_plan.md` into `-SkillsJson` (table
  format may evolve; LLM handles markdown parsing flexibility).
- Format final dashboard output (markdown sections, human-readable).
- Handle the "A12 not yet built" warning (check if `skills/output/phase.md`
  exists; if not, skip WI block and print warning).

### What scripts do (deterministic)
- All git timestamp comparisons.
- All file existence checks.
- All staleness logic.
- Priority ordering of next actions.
- YAML frontmatter parsing of `phase_status.md`.

---

## File locations

```
scripts/status/
├── Get-ActiveWI.ps1
├── Get-SkillFreshness.ps1
├── Get-MapAndTestFreshness.ps1
└── Get-NextAction.ps1
```

Scripts live in `scripts/status/` (repo root), not inside `skills/` —
they're general-purpose helpers, not skill I/O artifacts.
