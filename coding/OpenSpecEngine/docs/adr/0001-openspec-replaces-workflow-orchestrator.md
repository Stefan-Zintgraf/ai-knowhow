# OpenSpec Replaces workflow.md as the Authoritative Orchestrator (DEC1)

**Status:** proposed

> Not yet grilled — authored by a free-style prompt (2026-06-09), not via `grill-with-docs`. Status reset
> `accepted → proposed`; awaits ratification or amendment at `M1-P0` (see `openspec_migration.md`).

## Context

The ai-mail skillset's run order lives in `skills/workflow.md` (a hand-written topological sort of the
authoring chain) plus the `create_skills.md` orchestration rule (a bespoke driver that runs one
sub-agent per unit and flips checkboxes on POST). OpenSpec 1.4.1's OPSX workflow *is* the same thing
generalised: a schema-driven artifact DAG (`schema.yaml` → `{id, generates, template, instruction,
requires}`) driven by a CLI state machine (`openspec status` / `instructions`) and thin per-tool skills.
Running both would mean two sources of truth for "what's next" — the worst outcome. Date: 2026-06-09.
See `docs/openspec_migration.md` §1–§4, §9.3. (ai-mail at `C:\PROJ\ai-mail\` is referenced
read-only.)

## Decision

OpenSpec **replaces** `workflow.md` as the single authoritative orchestrator. `schema.yaml` becomes the
one source of "what's next"; `workflow.md`'s content is **harvested, not duplicated** — its ordering
edges become `requires:` edges, and its between-step HITL reviews and operational sub-procedures move
into node `instruction`s and a fail-closed `review` node. The **expanded `/opsx:*` profile** is enabled
(`/opsx:continue` creates one artifact at a time — *not* core `/opsx:propose`, which would generate the
whole spine in one shot and destroy review-between-every-step). Lenses are **relocated, not removed**:
their SKILL.md files stay portable; only their standalone workflow lines move into node instructions,
with `trace-check` promoted to the `review` node. `workflow.md` is retired-but-kept as a
"harvested-from" source map until the schema is proven, then archived.

## Considered Options

- **Replace `workflow.md` with the OpenSpec schema (chosen)** — one orchestrator, lets the maintained
  CLI own state/ordering, gains cross-editor skill generation; cost is re-homing the review gates as
  discipline rather than engine-enforcement.
- **Coexist / half-adopt (rejected)** — OpenSpec for some steps, the hand-rolled sequence for others;
  produces two conflicting "what's next" surfaces.
- **Keep the hand-rolled workflow, ignore OpenSpec (rejected)** — forgoes the DAG engine, the
  delta/archive spec accretion, and cross-editor portability that motivated the migration.

## Consequences

- The review gates that `workflow.md` enforced between steps become (a) the natural `/opsx:continue`
  stop points + instruction-tail prompts (soft reviews) and (b) the fail-closed `review` node (the
  mechanical coverage/trace gate). Some rigor shifts from "the tool blocks you" to "the instruction
  tells you to block yourself."
- Phase-0 setup folds into `openspec init` + `config.yaml` + the kept tracker-bootstrap step.
- Documentation must name `schema.yaml` the authoritative sequence exactly once; `skills/workflow.md`,
  `skills_overview.md`, and `artifacts.md` are annotated, not deleted.
