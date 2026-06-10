# OpenSpec Replaces workflow.md as the Authoritative Orchestrator (DEC1)

**Status:** accepted — ratified + amended via grill 2026-06-10 (M1-P0).

## Context

ai-mail's run order lived in two hand-rolled places: `skills/workflow.md` (a topological sort of the
authoring chain) and `create_skills.md`'s driver (one sub-agent per unit, checkbox flipped on POST).
OpenSpec's OPSX is the same thing generalised — a schema-driven artifact DAG (`schema.yaml`:
`{id, generates, template, instruction, requires}`) run by a CLI state machine. Keeping both = two
sources of truth for "what's next." See `openspec_migration.md` §1–§4, §9.3.

## Decision

OpenSpec **replaces** `workflow.md` as the single orchestrator; `schema.yaml` is the one source of
"what's next." `workflow.md` is **harvested, not duplicated**: ordering → `requires:` edges;
between-step reviews + sub-procedures → node `instruction`s + a fail-closed `review` node. Enable the
**EXPANDED profile** (`/opsx:continue`, one artifact at a time) — not core `/opsx:propose` (whole spine
in one shot, kills review-between-steps). Lenses are **relocated, not removed**: SKILL.md files stay
portable, only their standalone workflow lines move into node instructions; `trace-check` is promoted to
the `review` node. `workflow.md` is retired-but-kept as a "harvested-from" map until the schema is
proven, then archived.

## Considered Options

- **Replace with the OpenSpec schema (chosen)** — one orchestrator; the maintained CLI owns
  state/ordering; gains cross-editor skill generation. Cost: review gates become discipline, not
  engine-enforcement.
- **Coexist / half-adopt (rejected)** — two conflicting "what's next" surfaces.
- **Keep `workflow.md`, ignore OpenSpec (rejected)** — forgoes the DAG engine, delta/archive accretion,
  and cross-editor portability that motivated the migration.

## Consequences

- **Engine-enforced: ordering only.** `openspec status` marks nodes `ready`/`blocked` by `requires`;
  `/opsx:continue` serves one `ready` node at a time, then stops (`continue-change.ts`). Sequence is now
  enforced — `workflow.md` never was.
- **Discipline only: the quality/HITL gate.** Per OpenSpec's "enablers, not gates," nothing blocks
  `/opsx:archive` on a `review` node reporting `BREAKS FOUND (N)` — "fail-closed" is instruction wording,
  not engine behaviour, and the soft between-step reviews are `/opsx:continue` *stops*, not forced
  reviews. This also drops `create_skills.md`'s "flip the box only after POST passes" (DEC6 keeps that
  driver for the build's Part A; the product spine has none).
- **Real archive-time enforcement is deferred to M2** (`openspec_migration.md` M2-A6: an external git
  hook / CI step that reads the `review` result and blocks the commit/merge on a failed `review`). Out of
  M1 scope by choice — adding it now fights the "enablers, not gates" grain and isn't needed to prove the
  engine. M1 ships honest-discipline; M2 hardens it. **Amended 2026-06-10 (ADR-0007):** the enforcement is
  an *external wrapper only*; the earlier "`openspec validate` extension" option is withdrawn — extending
  the `Validator` would fork OpenSpec, which the project forbids.
- `schema.yaml` must be named the authoritative sequence exactly once; `workflow.md` /
  `skills_overview.md` / `artifacts.md` are annotated, not deleted.
