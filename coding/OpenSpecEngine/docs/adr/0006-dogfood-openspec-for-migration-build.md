# Dogfood OpenSpec to Manage the Migration Build — Envelope + Part B, Not Part A Sequencing (DEC6)

**Status:** proposed

> Deliberately left **proposed**, not accepted. ADRs 0001–0005 were authored by a free-style prompt and
> never grilled (see `openspec_migration.md` `M1-P0`). This decision is to be **ratified or amended via
> `grill-with-docs` at `M1-P0`**, alongside 0001–0005 — not free-styled like them.

## Context

This project bets the entire authoring spine on OpenSpec being a good engine (0001 retires `workflow.md`
in its favour). The cheapest validation of that bet is to **use OpenSpec on real work before committing the
custom schema to it**. `M1-A0` already runs `openspec init`, so the project touches OpenSpec at step one
regardless. Date: 2026-06-09. See `openspec_migration.md` §1, §8–§10, and the "Execution method per
work-type" routing table.

Two distinct OpenSpec levels were previously conflated, and the distinction is load-bearing here:

- **Level 1 — the custom `<spine-name>` schema** (the deliverable). It does not exist yet, so it cannot
  manage its own construction (chicken/egg). This is the only place the chicken/egg objection holds.
- **Level 2 — OpenSpec's stock `spec-driven` schema + OPSX CLI** (change folder, `tasks.md`, `apply`,
  `archive`). This exists today and *can* manage the remaining migration **as a change**, with no
  chicken/egg.

The trap: the migration's own Orchestration rule (one cold sub-agent per unit, strict sequential order,
flip `- [ ]` to `- [x]` **only** after that unit's POST self-check passes — fail-closed) is *exactly the
rigor §9.1 / D-DEC1 say OpenSpec lacks* ("dependencies are enablers, not gates"). Driving Part A execution
through `/opsx:continue` would replace the fail-closed driver with OpenSpec's fluid model — recreating
tension §9.1 one level up, and reintroducing the §9.3 "two engines, one job / two sources of truth for
what's next" hazard at the meta level.

## Decision

**Dogfood OpenSpec to manage the migration build at Level 2, but only where it is genuinely the engine
under test — not where it would dilute the fail-closed rigor the migration exists to preserve.**

- **Change envelope — OpenSpec (stock `spec-driven`).** Manage the remaining build as a single OpenSpec
  change: one change folder, `design.md` that **points to** `openspec_migration.md` and the ADRs (does not
  duplicate them — Doc5), `tasks.md` carrying the M1 (then M2) work items, `/opsx:archive` on done.
- **Part B (validate / dry-run) — OpenSpec CLI.** Already the engine under test (`schema validate`,
  `/opsx:new → continue → apply → archive` on the custom schema). Unchanged.
- **Part A (author `schema.yaml` / templates / `config.yaml` text) — keep the strict cold-sub-agent
  driver.** OpenSpec *tracks* these units as tasks; it does **not** generate them, and the **driver — not
  OPSX — owns the fail-closed, POST-gated sequencing**. The driver remains the single authority for "what's
  next" within Part A.

This keeps OpenSpec where it earns real learning (the change/`tasks`/`apply`/`archive` loop and the Part B
engine) and keeps the fail-closed driver where the migration's value lives.

## Considered Options

- **Option A — dogfood the envelope + Part B, keep the driver for Part A (chosen).** Real OPSX ergonomics
  on real work before betting the custom schema; fail-closed rigor preserved where it matters; the
  meta-level "two engines" hazard is bounded to a one-off build, not a recurring workflow.
- **Option B — full switch: drive Part A through `/opsx:continue` too (rejected).** Surrenders the
  fail-closed POST-gated sequencing to OpenSpec's "enablers, not gates" model — recreating §9.1 at the meta
  level and making OPSX the authority for "what's next" *before* it has been proven (B1). Maximum dogfood,
  but trades away the exact rigor under migration.
- **Option C — no dogfood; build entirely under the markdown driver, touch OpenSpec only at `M1-A0`/Part B
  (rejected).** Safest, lowest ceremony, but forgoes the cheapest validation of the central bet and learns
  OPSX ergonomics late, when the custom schema already depends on them.

## Consequences

- **Two OpenSpec contexts coexist and must not be confused:** (1) the stock `spec-driven` change managing
  the build; (2) the custom `<spine-name>` schema being authored as the deliverable. Keep them in separate
  folders and name them explicitly, or the §9.3 confusion bites at the meta level.
- `M1-A0`'s `openspec init` folds into setting up the dogfood change (one init, up front).
- The driver's Orchestration rule and OpenSpec's `tasks.md` are **two views of the same unit list** — the
  driver is authoritative for Part A sequencing; `tasks.md` mirrors status. A reconciliation note is owed
  so there is one source of truth for "done" per unit.
- A negative dogfood result is a **first-class outcome**: if driving the build through the OPSX change feels
  worse than the markdown driver, that is direct signal on 0001 (retire `workflow.md`) and should feed back
  into the P0 grill.
- This decision is added to the `M1-P0` grill scope (now seven ADRs: 0001–0007).
