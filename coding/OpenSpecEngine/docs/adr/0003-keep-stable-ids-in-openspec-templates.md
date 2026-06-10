# Keep Stable FR/NFR/UC/BR/ADR IDs in OpenSpec Templates (DEC3)

**Status:** accepted — ratified + amended via grill 2026-06-10 (heading shape moved to ID-only; see Decision)

## Context

OpenSpec specs use named requirements (`### Requirement: <name>`) with no numeric IDs. The ai-mail
traceability lenses (`trace-check`, `tracker-trace-check`), `usecase-spec`, and `spec-to-prd` hinge on
stable `FR/NFR/C/UC/BR/ADR-###` IDs, and the project treats those IDs as **permanent identity — a number
is assigned once and never reused for the project's lifetime.** OpenSpec templates are fully user-owned,
and the lenses already **discover** ID patterns from the files. See `openspec_migration.md` §7, Appendix B.

The non-obvious fact that decides the heading shape: OpenSpec's delta merge keys requirements on the
**entire `### Requirement:` heading string** (`normalizeRequirementName` = `.trim()`; `specs-apply.ts`).
The `FR-###` prefix is invisible to the engine unless it *is* the whole heading.

## Decision

**Keep the stable IDs, and make the ID the requirement's heading — `### Requirement: FR-001` alone, with
the human-readable name as the first body line** (`**<name>.** The system SHALL …`). The ID is therefore
the engine's match key, not a decoration. The lenses' convention-discovery resolves these unchanged.

Consequences of keying on the bare ID:

- **The never-reuse invariant is engine-enforced for free.** Re-`ADD`ing an existing `FR-###` throws
  `ADDED failed … already exists` — a rare hard gate in an engine whose default is "enablers, not gates."
- **Reword is free.** The mutable prose lives in the body, so editing it never changes the match key;
  milestone N+1 `MODIFIED` always resolves. `RENAMED` is needed only to renumber — which DEC3 forbids — so
  it is effectively never used.

## Considered Options

- **ID-only heading `### Requirement: FR-001`, name in body (chosen)** — ID is the engine match key;
  never-reuse and reword-stability come for free. Cost: terser headings; `openspec show`/`verify` list
  requirements as "FR-001" rather than a prose name (mitigated by the bold name on the first body line).
- **ID + name in heading `### Requirement: FR-001 — <name>` (rejected)** — readable, but the engine keys
  on `FR-001 — <name>`, so (a) the never-reuse invariant is unenforced (a different name re-using `FR-001`
  does not collide) and (b) every prose reword in N+1 forces a `## RENAMED` delta or archive halts. The ID
  becomes decorative to the engine — the opposite of "permanent identity."
- **Adopt OpenSpec named requirements, drop IDs (rejected)** — aligns with vanilla OpenSpec but discards
  the ID-based traceability the whole AIUP chain depends on and forces rebuilding the lenses around
  heading-name matching.

## Consequences

- `requirements.md` keeps `FR/NFR/C/OOS-###` ID columns. The `specs` delta node emits
  `### Requirement: FR-###` (ID-only heading), human name + normative SHALL/MUST in the body, `####
  Scenario` blocks from the use-case flows.
- `config.yaml` `rules` reinforce: "every row has a stable unique ID, never reused"; "the `### Requirement:`
  heading is the bare `FR-###` — the engine match key; put the name in the body."
- No change to `trace-check` / `tracker-trace-check` id-discovery — they read the ID from the heading.
- **Interacts with DEC4:** because the match key is the bare ID, milestone N+1 reword is a plain `MODIFIED`
  (no `RENAMED`). The 0004 grill must reconcile its drafted `FR-### — <name>` heading shape to this.
