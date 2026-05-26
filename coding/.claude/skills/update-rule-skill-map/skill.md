---
name: update-rule-skill-map
description: Synchronize `Skills:` annotations on every named rule in source docs (gr/*.md, wf/*.md, phases.md) against the authoritative mapping tables in coding_plan.md. Use when rules changed, files added/renamed/deleted, skills added/renamed, or mapping tables updated. Triggers on "update skill map", "sync annotations", "fix skill annotations", or "/update-rule-skill-map".
version: 1.0.0
---

Ensure every named rule/topic in the source-doc tree carries a correct, up-to-date `Skills:` annotation line. The authoritative source of truth for which skill owns which rule is `coding_plan.md` (Phase Skills table, Cross-Cutting Skills table, Templates table, per-item detail blocks, and `phases.md` section 5 Skill map). This skill reads the tables, scans the docs, diffs, and applies fixes.

## Preflight

**Gate A — Scope selection.** `AskUserQuestion`:
- `Full scan` — check every source doc against every mapping table. Default.
- `Single file` — check one file the user names. Faster for targeted edits.
- `Deleted/renamed audit` — detect stale annotations referencing skills or files that no longer exist.

**Gate B — Dry-run preference.** `AskUserQuestion`:
- `Apply fixes` — write corrected annotations directly. Default.
- `Report only` — print the diff table, write nothing. Human applies manually.

## Steps

### 1. Build the authoritative rule-to-skill map

Read `coding_plan.md` and extract every rule-to-skill binding from these sources (in priority order):

1. **Phase Skills table** — each row's `Source doc` column names the file(s) and optional rule range (e.g., `gr_idea.md Idea8–Idea11`). The `Skill name` column gives the owning skill. When a rule range is specified, only those rules map; when no range, all rules in the file map.
2. **Cross-Cutting Skills / Hooks table** — each row's `Source doc` column names specific rules (e.g., `gr_algn.md Aln6; gr_rev.md Rev7`). The `Name` column gives the owning skill.
3. **Templates and Conventions table** — each row's `Source doc` column names specific rules. The `Used by` column lists consuming skills.
4. **`phases.md` section 5 Skill map table** — phase-to-skill bindings; cross-ref with phases.md section 1 phase headings.
5. **Per-item detail blocks in `coding_plan.md`** — W-items, A-items, B-items often name specific rules in prose (e.g., "Aln17 wires B11"). These are secondary to tables but catch cross-cutting bindings the tables abbreviate.

**Output of this step:** an in-memory map: `{ rule_id → Set<skill_name> }`. Example: `Aln6 → {align-concept, hidden-constraint-checklist}`.

The map uses **kebab-case skill names** as they appear in the Phase Skills table `Skill name` column (e.g., `distill-idea`, not `A11`).

### 2. Discover source-doc files

Scan for every file that may contain annotatable rules:

- `gr/*.md` — guardrail detail docs.
- `wf/*.md` — workflow docs.
- `phases.md` — phase definitions and skill map.

**Detect changes since last run:**
- **New files** — present on disk but not referenced in any mapping table row. Flag for human: "new file `gr/gr_foo.md` has no mapping table entry — add a row to coding_plan.md first, or skip?"
- **Deleted files** — referenced in mapping tables but absent on disk. Flag: "file `gr/gr_bar.md` referenced in A-table row X but missing on disk — stale table entry?"
- **Renamed files** — heuristic: a mapping table references `gr/gr_old.md` (absent) while `gr/gr_new.md` (present, untracked or recently added) contains rules with the same ID prefix. Surface both and ask human to confirm rename.

Frozen reference files (`*Ref.md`, `*-ref.md`, `*_ref.md`) are excluded — do not scan, annotate, or report.

### 3. Scan rules in each file

For each source-doc file, extract every named rule heading. Recognized patterns:

- `### <Prefix><N>. <Title>` — e.g., `### Idea1. Output Is 3–6 Major Goals`, `### Aln17. Grill With Docs...`, `### TDD11. Direct-Edit Mode Exemption`.
- `### <Prefix><N><suffix>. <Title>` — e.g., `### M3a. Gray-Box Labor Partition`, `### Rev5a. API Snapshot...`, `### Res10a. Cross-Feature Reuse...`.
- `### <phase_code> — <Title>` — phase headings in phases.md section 1, e.g., `### ide — Idea`.
- `### <Section Title>` in wf/*.md — named sections like `## Steps`, `### Transition protocol`.

For each heading, check the **next non-blank line** for a `Skills:` annotation. Recognized format:

```
Skills: skill-a, skill-b, skill-c
```

States:
- **Present and correct** — annotation matches the Step 1 map.
- **Present but wrong** — annotation exists but differs from the map (missing skills, extra skills, or wrong skills).
- **Missing** — no annotation line; the map says one should exist.
- **Orphaned** — annotation exists but the rule ID is not in the Step 1 map (rule was deleted from tables, or skill was renamed/removed).

### 4. Diff and report

Print a summary table:

```
Source doc          | Rules | Correct | Wrong | Missing | Orphaned
--------------------|-------|---------|-------|---------|--------
gr/gr_idea.md       |    12 |      10 |     1 |       1 |       0
gr/gr_algn.md       |    19 |      19 |     0 |       0 |       0
...
TOTAL               |   105 |      98 |     2 |       4 |       1
```

Then list every non-correct entry with:
- File, rule ID, current annotation (or `<none>`), expected annotation, diff type (wrong/missing/orphaned).

For orphaned annotations, classify:
- **Skill renamed** — old name not in any table, but a similar name exists. Suggest replacement.
- **Skill removed** — old name not in any table, no similar name. Suggest removal.
- **Rule removed from tables** — rule heading still exists in the file but no table row references it. Ask human: deliberate exclusion or table oversight?

### 5. Apply fixes (if Gate B = `Apply fixes`)

For each non-correct entry:

- **Missing:** insert `Skills: <comma-separated list>` on the line immediately after the heading, before the next blank line or paragraph.
- **Wrong:** replace the existing `Skills:` line with the corrected one.
- **Orphaned:** `AskUserQuestion` per orphan — `Remove annotation` / `Keep as-is (manual override)` / `Update to <suggested replacement>`. Never silently remove.

Write changes file-by-file. After all writes, re-scan to confirm zero discrepancies (catch any edit collisions).

### 6. Report new rules without table coverage

After fixing annotations, list any rule headings found in source docs that have **no entry in any mapping table** in `coding_plan.md`. These are rules that exist in the docs but no skill claims ownership. For each:

- Rule ID, file, heading text.
- Suggested action: "Add a mapping row to coding_plan.md" or "This rule is cross-cutting context, not skill-owned — consider excluding from annotation."

This step is informational — no writes. The human decides whether to update `coding_plan.md`.

### 7. Return

```
update-rule-skill-map — status=<clean|fixed|report-only>, scope=<full|single-file|audit>
  files scanned: <N>
  rules scanned: <N>
  correct: <N>  fixed: <N>  orphaned: <N> (removed: <N>, kept: <N>)
  unmapped rules: <N> (no table entry)
  new files without table entry: <list or none>
  deleted files still in tables: <list or none>
```

## Hard Rules

- The authoritative mapping lives in `coding_plan.md` tables + `phases.md` section 5. This skill NEVER invents mappings — it reads tables and applies them. If a rule has no table entry, it is flagged to the human, not auto-assigned.
- Annotation format is exactly `Skills: skill-a, skill-b` — one line, comma-separated, kebab-case, alphabetically sorted. No markdown formatting, no backticks, no brackets.
- Never edit rule content, headings, or any text other than the `Skills:` annotation line. If a heading looks malformed, report it — do not fix it.
- Never read, edit, or cite frozen reference files (`*Ref.md`, `*-ref.md`, `*_ref.md`).
- Orphaned annotations require HITL confirmation before removal. No silent deletions.
- New files not in any mapping table are flagged, not auto-annotated. The human must add a `coding_plan.md` row first.
- When a skill name appears in a table, use the exact kebab-case form from the `Skill name` column (e.g., `distill-idea`), not the row ID (`A11`) or phase code (`ide`).
- Cross-cutting skills (B-series) are included in annotations when their `Source doc` column names a specific rule. A B-skill that applies to a phase but names no specific rule does NOT get annotated on every rule in that phase's doc.
- `coding_plan.md` itself is NOT annotated (it is the mapping source, not a mapping target). `guardrails.md` core rules (section 3.x) are NOT annotated — only `gr/*.md`, `wf/*.md`, and `phases.md` carry annotations.
- If `coding_plan.md` tables conflict with each other (e.g., Phase Skills says skill X owns rule R, but Cross-Cutting says skill Y owns rule R), include BOTH — the mapping is n:m. Flag the potential conflict to the human.
- Re-scan after writes to confirm zero discrepancies. If the re-scan still shows errors, report them and stop — do not loop.
