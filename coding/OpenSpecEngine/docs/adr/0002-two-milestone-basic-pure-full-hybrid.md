# Two-Milestone Migration: Basic / Pure then Full / Hybrid (DEC2)

**Status:** proposed

> Not yet grilled — authored by a free-style prompt (2026-06-09), not via `grill-with-docs`. Status reset
> `accepted → proposed`; awaits ratification or amendment at `M1-P0` (see `openspec_migration.md`).

## Context

OpenSpec is natively in-repo: planning lives in `openspec/changes/<change>/`, and "done" =
`/opsx:archive` merges delta specs into `openspec/specs/`. ai-mail additionally projects its spine onto
GitHub issues (`spec-to-prd` → `to-issues` → `triage`, audited by `tracker-trace-check`) for AFK-agent
execution. Whether the GitHub tracker stays (Hybrid) or is dropped (Pure) is a genuine product decision,
not a technical one. Date: 2026-06-09. See `openspec_migration.md` §8.

## Decision

Do not choose Pure vs. Hybrid — **sequence them as two migration milestones**:

- **Milestone 1 — Basic (Pure OpenSpec).** The full authoring spine runs entirely in-repo; execution is
  `tasks.md` + `/opsx:apply`; "done" is `/opsx:archive`. `spec-to-prd`, `to-issues`, `triage`, and
  `tracker-trace-check` are **out of scope**. This proves the engine on the smallest surface.
- **Milestone 2 — Full (Hybrid).** Layer the GitHub execution bridge (`spec-to-prd` `prd` node,
  `to-issues`, `triage`, `tracker-trace-check`) on the **proven** Basic spine. "Done" is two-staged:
  issues close on the tracker **and** the change archives into `openspec/specs/`. Prerequisite:
  Milestone 1 proven (M1-B1).

## Considered Options

- **Two milestones, Basic/Pure → Full/Hybrid (chosen)** — applies the project's own Pareto / one-slice
  discipline to the migration; de-risks the engine before adding tracker complexity; keeps the GitHub
  investment available without forcing it on day one.
- **Hybrid from the start (rejected)** — largest surface first; couples engine-proving to tracker wiring
  and the two-"done" reconciliation before the spine itself is validated.
- **Pure only, permanently (rejected)** — simplest, but discards the `ready-for-agent` AFK-agent issue
  loop and triage that ai-mail already invested in.

## Consequences

- Milestone 1 has no `tracker-trace-check`; the in-repo `openspec/specs/` is the only source of truth
  (this forces ADR 0004's delta adoption).
- `spec-to-prd`/`to-issues`/`triage`/`tracker-trace-check` are deferred, not retired — they return as
  Milestone 2 work items, re-pointed at `openspec/specs ↔ GitHub`.
- The migration can deliver value (a working in-repo spine) after Milestone 1 alone.
