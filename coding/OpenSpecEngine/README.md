# OpenSpecEngine

A **standalone project** (`C:\PROJ\ai-knowhow\coding\OpenSpecEngine\`) that migrates an authoring
skillset/workflow onto **OpenSpec 1.4.1 (OPSX)** as a custom schema — re-using the best of the existing
ai-mail skills, the matt_pocock skills, and the `coding/gr/*.md` guardrails, fused with a genericity
refactor so everything created here is project-agnostic.

## Source of truth (read-only) vs. writes

- **Source (read-only):** ai-mail at `C:\PROJ\ai-mail\` (and the guardrails at
  `C:\PROJ\ai-knowhow\coding\gr\`). Documents here reference `skills/…`, `docs/…`, `todo.md`, `plan/…`,
  `coding/gr/…` as **read-only pointers** into those locations — the material being migrated *from*.
  **ai-mail is never modified.**
- **Writes:** everything new — the OpenSpec schema, `config.yaml`, the generic skills, and this project's
  own docs — is **created here, under `OpenSpecEngine/`**.
- **No OpenSpec fork (ADR-0007):** OpenSpec is a **stock dependency, never forked or patched**. All
  adjustments use its officially-supported surface (custom `schema.yaml` + `templates/`, `config.yaml`,
  profile); behaviour OpenSpec lacks is wrapped *around* the CLI (git hook / CI), not patched into it.

## Contents

- [`docs/openspec_migration.md`](docs/openspec_migration.md) — the full analysis, the
  two-milestone work-item plan (Milestone 1 Basic / Pure → Milestone 2 Full / Hybrid), and Appendix B
  concrete node YAML. **Authoritative plan.**
- [`docs/adr/`](docs/adr/) — the architecture decisions (DEC1–DEC7) that shape the migration. They
  entered as `proposed` and are ratified one-per-session at `M1-P0`; see each ADR's **Status** line for
  its current state.

## Status

Plan + decisions complete (2026-06-09). **Build not started** — it runs as one project-agnostic pass
together with the genericity refactor (ADR 0005). Cheap opener: `M1-A0` (config smoke test) + `M1-A1`
(churn-independent schema skeleton).
