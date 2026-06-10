# No Fork of OpenSpec — Officially-Supported Customization Only (DEC7)

**Status:** proposed

> Drafted 2026-06-10 from a direct project constraint, not yet grilled. Ratify or amend at `M1-P0` via
> `grill-with-docs`, like 0001–0006.

## Context

The migration hosts the ai-mail authoring spine on OpenSpec 1.4.1, consumed as a stock npm dependency.
OpenSpec's whole value proposition is that the workflow moved *out of TypeScript* into editable
YAML + Markdown — `schema.yaml`, `templates/*.md`, `config.yaml` (`openspec_migration.md` §1). Every
adjustment the plan needs is reachable through that supported surface: a custom schema via
`openspec schema fork spec-driven <spine>`, templates, `context`/`rules`, the EXPANDED profile, and
exploiting OpenSpec's existing heading-string delta-merge key (ADR-0003). The one place the plan reached
*past* that surface was M2-A6, which offered "an `openspec validate` extension" as a way to make the
`review` gate a real blocker — that means editing OpenSpec's `Validator` (a fixed Zod class with no
plugin point; `src/core/validation/validator.ts`), i.e. forking the package.

## Decision

**Use only OpenSpec's officially-supported customization surface; the OpenSpec package is never forked or
patched.** All adjustments live in: custom `schema.yaml` + `templates/` (`openspec schema fork`),
`openspec/config.yaml` (`context`/`rules`/`schema`), profile selection (`openspec config profile`), and
the regenerated thin skills. Behaviour OpenSpec does not offer natively is layered *around* the CLI as an
external tool — never by modifying its source.

For the one disputed case — the fail-closed `review` gate — hard enforcement is an **external
archive-time wrapper** (a git pre-commit/pre-push hook or CI step that reads the `review` node's
PASS/PARTIAL/BREAKS result and blocks the commit/merge). The `openspec validate` extension option is
withdrawn (amends ADR-0001, M2-A6).

## Considered Options

- **Supported-surface-only, gate enforced by an external wrapper (chosen)** — survives `openspec update`
  and upgrades, no parallel fork to rebase, keeps OpenSpec a swappable dependency and the cross-editor
  generated-skill story intact. Cost: the quality gate can never live *inside* the engine; it is always a
  layer around it.
- **Fork/patch OpenSpec to add a custom validation rule or block archive on `review` (rejected)** — gives
  a truly engine-internal gate, but creates a maintained fork that must be rebased on every OpenSpec
  release and breaks the regenerated-skill portability. Disproportionate for one gate.

## Consequences

- §1's enumerated customization surface (schema / templates / config / profile) is the **complete** set of
  allowed adjustments.
- "Engine-enforced" elsewhere in these docs means *enforced by an external gate wrapping the engine*,
  **except** where the behaviour is already native and needs no wrapper: ordering via `requires`, and the
  never-reuse invariant via the heading-string match key (ADR-0003).
- M2-A6's mechanism is fixed to git hook / CI; the `openspec validate` extension option is removed from
  M2-A6 and ADR-0001.
- Inside OpenSpec the `review` node stays honest-discipline for the product spine's whole life; the
  external wrapper is the only hard blocker (M2).
- Re-evaluate only if OpenSpec ships an official validation-plugin or archive-gate hook — the wrapper
  could then move onto that supported surface (still no fork).
