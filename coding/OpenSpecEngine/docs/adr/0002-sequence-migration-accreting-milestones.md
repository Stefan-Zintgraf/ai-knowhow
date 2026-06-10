# Sequence the Migration as Accreting Milestones (M1 Basic/Pure first) (DEC2)

**Status:** accepted — ratified + amended via grill 2026-06-10 (M1-P0).

## Context

OpenSpec is natively in-repo: planning lives in `openspec/changes/<change>/`, and "done" =
`/opsx:archive` merges delta specs into `openspec/specs/`. ai-mail additionally projects its spine onto
GitHub issues for AFK-agent execution. Whether that tracker stays (Hybrid) or is dropped (Pure) is a
product decision, not a technical one. See `openspec_migration.md` §8.

## Decision

Don't fork Pure vs. Hybrid — **sequence capability as an open-ended series of accreting milestones**, each
a Pareto slice. The count is *not* fixed at two.

- **M1 — Basic (Pure OpenSpec):** the smallest proven slice. The full authoring spine runs in-repo;
  execution is `tasks.md` + `/opsx:apply`; "done" is `/opsx:archive`. `spec-to-prd`, `to-issues`, `triage`,
  and `tracker-trace-check` are out of scope. Proves the engine on the smallest surface.
- **M2 — the remainder so far:** everything deferred past M1, bundled by *exclusion* from the smallest
  slice, not by a theme. Currently two independent items: (1) the Hybrid GitHub execution bridge
  (`spec-to-prd` `prd` node, `to-issues`, `triage`, `tracker-trace-check`) layered on the proven spine;
  (2) the engine-enforced `review` gate (M2-A6, deferred from ADR-0001) — which is **not** gated on the
  tracker and could ship without it. Prerequisite: M1 proven.
- **M3, M4… may follow** as scope grows. The spine accretes via delta-specs (ADR-0004); it never forks
  (§6), so each milestone is a delta change, not a re-run of the chain.

## Considered Options

- **Sequenced accreting milestones, M1 Basic/Pure first (chosen)** — applies the project's own Pareto /
  one-slice discipline to the migration; de-risks the engine before tracker complexity; keeps the GitHub
  investment available without forcing it on day one.
- **Hybrid from the start (rejected)** — largest surface first; couples engine-proving to tracker wiring
  and the two-"done" reconciliation before the spine itself is validated.
- **Pure only, permanently (rejected)** — simplest, but discards the `ready-for-agent` AFK-agent issue
  loop and triage that ai-mail already invested in.

## Consequences

- M1's in-repo `apply`/`archive` is the **canonical "done"**; the M2 GitHub projection is *additive*, never
  a replacement. No later milestone supersedes in-repo execution — it bolts a tracker onto it. (Settles the
  open M2-A2 supersede-vs-coexist question.)
- M2 layering is **strictly additive** to the M1 spine: the `prd` node is downstream (`requires` existing
  nodes), no M1 artifact is re-authored, no `requires` edge mutated. Sequencing carries no hidden spine
  rework.
- M1 has no `tracker-trace-check`; in-repo `openspec/specs/` is the only source of truth — this forces
  ADR-0004's delta adoption.
- `spec-to-prd`/`to-issues`/`triage`/`tracker-trace-check` are deferred, not retired.
- The migration can deliver value (a working in-repo spine) after M1 alone.
