# Fuse the Genericity Refactor with the Migration — One Project-Agnostic Pass (DEC5)

**Status:** proposed

> Not yet grilled — authored by a free-style prompt (2026-06-09), not via `grill-with-docs`. Status reset
> `accepted → proposed`; awaits ratification or amendment at `M1-P0` (see `openspec_migration.md`).

## Context

The ai-mail skillset is mid-refactor to remove ai-mail-specific content and make every skill
project-agnostic (`skill_genericity_review.md`; `domain-requirements` in progress; `declare-milestone`
recently built). Separately, the migration moves the authoring chain onto OpenSpec. The earlier
recommendation was to do the refactor first and migrate after, to avoid transcribing a moving target
twice. But OpenSpec's architecture already separates generic from project-specific: `schema.yaml`
instructions and `templates/*.md` are project-agnostic by design (forkable/shareable), and project
specifics live in `config.yaml` `context`/`rules`. That is the *same boundary* the genericity refactor
is drawing. Date: 2026-06-09. See `openspec_migration.md` §10, D-DEC5.

## Decision

**Run the genericity refactor and the OpenSpec migration as ONE project-agnostic pass (Option D).**
Migrating a skill into a node *is* making it generic, so there is no double-transcription and no reason
to sequence them. Everything migrated, adjusted, or created must be project-agnostic — no `ai-mail`,
`acontis`, `M#`/`F##`, or repo paths in any schema node, template, or skill; project values arrive via
`config.yaml`. Structural split:

- **Authoring skills dissolve into schema nodes** — their SKILL.md retires (single home; no `Doc5`
  duplication), made generic in the node.
- **Lens skills are re-created as generic portable SKILL.md in OpenSpecEngine** — from the read-only
  ai-mail originals; OpenSpec-independent and may proceed in parallel.
- **Project specifics → `config.yaml`.**

The migration is its own standalone project at `C:\PROJ\ai-knowhow\coding\OpenSpecEngine\`; ai-mail
(`C:\PROJ\ai-mail\`) is referenced **read-only**, and **all new artifacts are created in OpenSpecEngine**,
never in ai-mail.

## Considered Options

- **Option D — fuse (chosen)** — one boundary designed once, in OpenSpec's vocabulary; no
  double-transcription; the todo.md "cleanup all skills from ai-mail-specific stuff" items *become* the
  migration work items.
- **Option A — refactor first, migrate after (rejected)** — designs the generic/specific boundary twice
  (once for generic SKILL.md args, once for `config.yaml`); double transcription.
- **Option B — migrate now, ignore refactor churn (rejected)** — re-transcribes node instructions after
  the refactor lands.
- **Option C — refactor-independent slice now (subsumed)** — the cheap opener (config smoke test +
  churn-independent schema skeleton) is retained inside Option D as the first work items, not a separate
  strategy.

## Consequences

- `review-skills` / `refactor-skills` are **out of scope** — not migrated, not adjusted. They keep
  running over the remaining lens SKILL.md files; the dissolved authoring nodes' QA shifts to
  `openspec schema validate` + the `review` node + dry runs. Extending the meta-layer to review schema
  nodes is a separate future enhancement.
- The migration's deliverable for the authoring skills changes from "generic SKILL.md" to "generic
  schema node + `config.yaml` split."
- Build is gated behind the genericity refactor it is now fused with; the cheap, reversible opener is
  `M1-A0` (config smoke test) + `M1-A1` (churn-independent schema skeleton).
