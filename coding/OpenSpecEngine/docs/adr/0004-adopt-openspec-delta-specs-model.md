# Adopt OpenSpec's Delta/Specs Model — 10-Node Basic Schema (DEC4)

**Status:** proposed

> Not yet grilled — authored by a free-style prompt (2026-06-09), not via `grill-with-docs`. Status reset
> `accepted → proposed`; awaits ratification or amendment at `M1-P0` (see `openspec_migration.md`).

## Context

OpenSpec's headline feature is its brownfield delta model: a change's `specs/<cap>/spec.md` files are
`ADDED`/`MODIFIED`/`REMOVED` deltas against `openspec/specs/`, and `/opsx:archive` merges them so the
source of truth accretes. ai-mail's authoring chain is greenfield-spine-first. The open question was
whether to express the behaviour-contract layer (in-scope FRs + their use-case scenarios) as OpenSpec
delta specs, or to run OpenSpec as a bare DAG runner over the existing `docs/*` shapes. Milestone 1 is
Pure (ADR 0002) — with no GitHub tracker, `openspec/specs/` is the only possible source of truth. Date:
2026-06-09. See `openspec_migration.md` §6, §9.2, Appendix B.

## Decision

**Adopt the delta/specs model.** The behaviour-contract layer becomes a dedicated **`specs` node**
(`generates: "specs/**/*.md"`) that projects each in-scope FR + its use-case scenarios into
`### Requirement: FR-### — <name>` / `#### Scenario` delta specs, which accrete into `openspec/specs/`
on archive. This makes **Milestone 1 a 10-node schema** (the `specs` node sits between `use-cases-spec`
and `review`; `review` and `tasks` depend on it). Milestone N+1 is then a delta change
(`ADDED`/`MODIFIED`/`REMOVED`) against the accumulated truth, replacing ai-mail's "re-run the whole
chain per milestone."

## Considered Options

- **Adopt for the behaviour-contract layer (chosen)** — gains the milestone-N+1 delta + archive
  accretion (OpenSpec's main value); required anyway in Pure/M1 since `openspec/specs/` is the only
  source of truth. Cost: reshaping FRs + use-case scenarios into Requirement/Scenario form.
- **Bare DAG runner over `docs/*` (rejected)** — no `specs` node; simpler transcription, but archive
  merges nothing meaningful and the headline feature is forfeited; incompatible with Pure mode's need
  for an in-repo source of truth.

## Consequences

- Milestone 1 is **10 nodes**: `vision`, `glossary`, `requirements`, `entity-model`,
  `use-cases-diagram`, `use-cases-spec`, **`specs`**, `review`, `testing`, `tasks`.
- The upstream reasoning artifacts (vision, entity model, ADRs, testing) stay as plain change-folder
  planning artifacts; only the behaviour contract is expressed as deltas.
- The `specs` node has no 1:1 SKILL.md — its `instruction` is the FR + use-case-scenario → delta-spec
  projection.
