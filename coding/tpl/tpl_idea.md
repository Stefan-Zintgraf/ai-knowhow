# Template: Idea Goal List (C8)

Purpose: canonical shape for the `ide`-phase output — the 3–6 major goals that anchor downstream grilling, PRD authoring, issue decomposition, review, and QA retirement check. Single parse target for all consumers.

Source: [`gr/gr_idea.md`](../gr/gr_idea.md) Idea1–Idea7; retirement [`guardrails.md`](../guardrails.md) §3.33.

Emitted by: `distill-idea` skill (A11, W15).
Consumed by: `grill-me` (A1, anchors grilling), `write-prd` (A2, folds into PRD Goals section), `review` (A6, verifies coverage), `qa` (A8, Q11 retirement lint).

Format: two paired files per work-item, both under `plan/<WI>/`. The idea file is markdown-only (no frontmatter); the status file is frontmatter-only (no body required).

---

## File Naming

```
plan/<WI>/idea.md           # the goal list
plan/<WI>/status_idea.md    # WI anchor: status + owner-issue
```

`<WI>` is a human-confirmed snake_case slug, derived from the brief and confirmed via HITL before the first write. Examples: `ai_mail`, `fix_crash_abc`, `add_oauth_provider`. Single `idea.md` per WI — never a shared `idea.md`, never multiple idea files under one WI.

---

## `plan/<WI>/idea.md` Shape

Plain markdown. No YAML frontmatter. Body structure:

```markdown
# Goals

1. <goal sentence — what the work must serve, not how>
2. <goal sentence>
3. Non-goal: <explicit exclusion sentence>
4. <goal sentence>
5. Non-goal: <explicit exclusion sentence>

Stripped detail: <implementation specific that leaked from brief and was removed>
Stripped detail: <another>
```

### Rules

- Between **3 and 6** numbered entries, inclusive (Idea1). Negative goals count toward the budget when they materially shape the work (Idea3).
- One sentence per goal. No nested bullets. No prose paragraphs.
- Negative goals prefixed exactly `Non-goal: ` (capital N, space after colon).
- Forbidden inside any goal body (Idea2): module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices (library X, pattern Y), effort or timeline estimates.
- If a detail leaks from the brief, strip it from the goal text and add one `Stripped detail: <item>` line per stripped item below the numbered list. **Never** write `deferred to <phase>` or any phase token in the stripped-detail line.
- Heading is literally `# Goals` (so consumers can locate the list without parsing surrounding prose).

---

## `plan/<WI>/status_idea.md` Shape

Frontmatter only. Body optional and ignored by consumers.

```markdown
---
status: open | wip | done
updated: <YYYY-MM-DD>
owner-issue: "#NNN"
---
```

### Fields

| Field         | Required | Notes                                                                                   |
| ------------- | -------- | --------------------------------------------------------------------------------------- |
| `status`      | yes      | `open` = placeholder created, no artifact yet; `wip` = artifact written; `done` = human accepted as complete. |
| `updated`     | yes      | ISO date. Refreshed on every run of the skill, regardless of state change.              |
| `owner-issue` | yes      | The WI's owning external issue (GitHub / Linear / etc.) — anchors 3.33 retirement. Sibling artifacts under `plan/<WI>/` inherit this owner; do not duplicate the field in sibling status files. |

### State Machine

- Initial successful artifact write → `status: wip` (default).
- `wip → done` only on explicit human confirmation. Never auto-flip. The skill prompts "mark done?" at the end of every successful run unless the run is a clear-incomplete (under-budget failure, human rejected the draft, no acceptance reached) — in those cases skip the prompt and leave status as it is.
- `done → wip` on explicit human reopen. Never `done → open`.
- `open → wip` on first successful write.
- On failure runs (no artifact written), do NOT create or modify `status_idea.md`. Status file is never created without a paired `idea.md`.

---

## Retirement (3.33)

`plan/<WI>/` retires as a unit when the WI's owner-issue closes:

1. The PR that closes the owner-issue MUST delete the entire `plan/<WI>/` directory in the same diff.
2. `qa` runs the Q11 check #3: walks every `plan/<WI>/` in the working tree, reads `status_idea.md` owner-issue, fails the merge if the owner is closing and the directory survives.
3. Partial retirement is a fail-now finding — deleting `idea.md` while leaving sibling artifacts (or vice versa) under `plan/<WI>/` blocks the merge.

---

## Anti-Patterns

- Writing the goal list to any path other than `plan/<WI>/idea.md` — no `idea/<topic>.md`, no shared `idea.md`, no `<WI>.md` at the repo root.
- Inlining the goal list into the PRD without first writing `plan/<WI>/idea.md` — downstream skills (A1, A6, A8) expect the file at the canonical path.
- Adding YAML frontmatter to `idea.md`. The pair is split deliberately: idea body is human-edited markdown; status is machine-parsed frontmatter.
- Adding a body to `status_idea.md`. Consumers read frontmatter only.
- Auto-flipping `status` to `done` after a successful write. Human-only `done`.
- Omitting `owner-issue` from `status_idea.md`. Without it, Q11 retirement cannot fire — the directory becomes orphaned.
- Stripped-detail lines that reference a phase (e.g. `Stripped detail: API shape deferred to prd`). Drop the phase reference: `Stripped detail: API shape`.

---

## Notes on Interaction

- `grill-me` (A1) reads `idea.md` to anchor the grilling target. The goal list narrows what `aln` grills over; it does not shortcut grilling (Idea6).
- `write-prd` (A2) folds the goal list into the PRD's Goals/Objectives section. PRD does not replace `idea.md` — both coexist until WI close (3.33 retires both: PRD via 3.24 external move, idea via 3.33 directory delete).
- `review` (A6) verifies the PRD's Goals section faithfully reflects `idea.md` (no drift, no silent narrowing).
- `qa` (A8) Q11 #3 enforces 3.33 retirement at merge time.
- Pattern parallel: `tpl_idea.md` (this) ↔ `tpl_var_pres.md` (C6) — both pair a machine-readable shape with a human-editable body, both carry an `owner-issue` provenance field, both retire on owner close.
