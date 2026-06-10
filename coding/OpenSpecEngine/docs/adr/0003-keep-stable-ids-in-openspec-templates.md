# Keep Stable FR/NFR/UC/BR/ADR IDs in OpenSpec Templates (DEC3)

**Status:** proposed

> Not yet grilled — authored by a free-style prompt (2026-06-09), not via `grill-with-docs`. Status reset
> `accepted → proposed`; awaits ratification or amendment at `M1-P0` (see `openspec_migration.md`).

## Context

OpenSpec specs use named requirements (`### Requirement: <name>`) with no numeric IDs. The ai-mail
traceability lenses (`trace-check`, `tracker-trace-check`), `usecase-spec`, and `spec-to-prd` all hinge
on stable `FR/NFR/C/UC/BR/ADR-###` IDs. OpenSpec templates are fully user-owned, and the lenses already
**discover** id patterns from the files rather than hard-coding them. Date: 2026-06-09. See
`openspec_migration.md` §7, Appendix B.

## Decision

**Keep the stable IDs**, carried verbatim inside the OpenSpec templates — e.g.
`### Requirement: FR-### — <name>` and `FR-001` rows in the requirements catalog. The lenses' existing
convention-discovery resolves these unchanged, so traceability keeps working with no lens rewrite.

## Considered Options

- **Keep IDs inside the templates (chosen)** — a one-column / one-line choice in the `requirements` and
  `specs` templates; near-zero cost because the lenses discover id patterns.
- **Adopt OpenSpec named requirements (rejected)** — aligns with vanilla OpenSpec and its `verify`, but
  throws away the ID-based traceability the whole AIUP chain is built on and forces rebuilding the lenses
  around heading-name matching.

## Consequences

- `requirements.md` keeps `FR/NFR/C/OOS-###` ID columns; the `specs` delta node carries the ID into the
  requirement/scenario heading (`### Requirement: FR-### — …`).
- `config.yaml` `rules` reinforce the convention ("every row has a stable unique ID"; "carry FR/UC/BR IDs
  into headings so trace-check resolves them").
- No change required to `trace-check` / `tracker-trace-check` id-discovery.
