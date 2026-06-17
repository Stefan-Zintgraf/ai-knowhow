# OpenSpecEngine — Artifacts

The authoritative reference for what each schema node produces, what it contains, and where it
lives. Covers M1 (Basic / Pure) and M2 (Hybrid / GitHub bridge). The schema (`schema.yaml`) is the
executable counterpart — `generates:` and `requires:` there must match this document.

> **Deferred (not yet scoped):** the **pre-change** entry point — `declare-milestone`
> (→ `.openspec.yaml`, §3/§6) and the ai-mail brainstorming/foundation artifacts
> (`plan/painlist_*.md` `P##`/`A##`, `plan/01-foundation.md` `M#`/`F##`). The schema currently
> starts at `vision`; whether these upstream steps are in scope, out of scope, or replaced is
> an open question to settle later.

---

## Artifacts created per change — M1 (Basic / Pure)

> **Settled decisions:**
> 
> - All artifacts live in `openspec/changes/<change>/` unless marked project-level.
> - Every node is authored by one `/opsx:continue` invocation (EXPANDED profile — one node, then STOP).
> - `specs/<cap>/spec.md` is the **only** artifact that accretes on archive: `/opsx:archive` merges
>   it into `openspec/specs/<cap>/spec.md`. All other change-folder files remain in the change folder.
> - `tasks.md` is tracked by the `apply:` block; `/opsx:apply` drives execution against it.

### Production Sequence

| Artifact              | Node                | Produced by                          | Requires                                |
| --------------------- | ------------------- | ------------------------------------ | --------------------------------------- |
| `vision.md`           | `vision`            | `/opsx:continue`                     | `[]`                                    |
| `glossary.md`         | `glossary`          | `/opsx:continue` + `grill-with-docs` | `[vision]`                              |
| `requirements.md`     | `requirements`      | `/opsx:continue`                     | `[vision, glossary]`                    |
| `entity_model.md`     | `entity-model`      | `/opsx:continue`                     | `[requirements]`                        |
| `use_cases.puml`      | `use-cases-diagram` | `/opsx:continue`                     | `[requirements, entity-model]`          |
| `use_cases/*.md`      | `use-cases-spec`    | `/opsx:continue`                     | `[use-cases-diagram]`                   |
| `specs/<cap>/spec.md` | `specs`             | `/opsx:continue`                     | `[use-cases-spec, entity-model]`        |
| `testing.md`          | `testing`           | `/opsx:continue`                     | `[requirements]`                        |
| `review.md`           | `review`            | `/opsx:continue`                     | `[specs, use-cases-spec, entity-model]` |
| `tasks.md`            | `tasks`             | `/opsx:continue`                     | `[use-cases-spec, testing]`             |

> **Note — `glossary` node:** `generates: glossary.md` (change-local vocabulary coined or refined
> in this change). The project-level `docs/CONTEXT.md` is the accumulated glossary; it is
> maintained by `grill-with-docs` sessions, not by the schema. ADRs authored during the glossary
> step are project-level side-products (`docs/adr/####-*.md`), not schema `generates:` outputs.

### Content

| Artifact              | Content                                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `vision.md`           | Mission, target user, dogfood context, golden-path scenario, out-of-scope list                                                  |
| `glossary.md`         | Canonical term definitions + avoid-lists for terms coined or refined in this change                                             |
| `requirements.md`     | `FR-###` functional requirements + `NFR-###` non-functionals + `C-###` constraints + Out-of-Scope, scoped by change             |
| `entity_model.md`     | Aggregates, value objects, relationships, invariants — glossary-aligned                                                         |
| `use_cases.puml`      | PlantUML actor/use-case diagram; every in-scope FR maps to ≥1 use case                                                          |
| `use_cases/*.md`      | Per-use-case: actors, preconditions, main flow, alt flows, `BR-###`, `FR-###` trace line                                        |
| `specs/<cap>/spec.md` | Behaviour contract as delta specs: `## ADDED / MODIFIED / REMOVED Requirements`, each `### FR-###` with `#### Scenario` entries |
| `testing.md`          | Testing strategy: module/test-surface priorities, test-double policy, `NFR-###`/`C-###` thresholds referenced by ID             |
| `review.md`           | Trace-check report: `trace-check` A–D + FR↔UC forward/reverse coverage; emits PASS / PARTIAL / BREAKS                           |
| `tasks.md`            | Implementation checklist derived from use-case scenarios + testing strategy; tracked by `apply:`                                |

### Delta Information

| Artifact              | New information (not present in input artifacts)                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `vision.md`           | Names the change; mission, target user, and the in-scope golden-path scenario                                      |
| `glossary.md`         | First authoritative definitions for terms coined in this change                                                    |
| `requirements.md`     | Stable `FR-###`/`NFR-###`/`C-###` IDs and the authoritative what-must-be-built list, change-scoped                 |
| `entity_model.md`     | Aggregates, value objects, relationships, and entity-level invariants — the data structure behind the FRs          |
| `use_cases.puml`      | The use cases themselves and the forward `FR→UC` mapping — proof every in-scope FR is realised                     |
| `use_cases/*.md`      | Per-use-case scenarios (pre/postconditions, main + alt flows, `BR-###`) and reverse `UC→FR` traceability           |
| `specs/<cap>/spec.md` | The distilled behaviour contract in delta form — the only artifact that accretes into `openspec/specs/` on archive |
| `testing.md`          | The project-specific *how* of verification — module/test-surface picks, test-double policy, prior art              |
| `review.md`           | Coverage verdict — whether every in-scope FR traces to ≥1 scenario; surfaces gaps before implementation begins     |
| `tasks.md`            | The ordered implementation checklist — derived from scenarios + testing strategy, not authored anywhere upstream   |

### Redundancies

| Artifact              | Redundant information (restates content from upstream artifacts)                                                                          |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `vision.md`           | N/A — first artifact in the change                                                                                                        |
| `glossary.md`         | N/A — canonical definitions; downstream artifacts restate its terms, not vice-versa                                                       |
| `requirements.md`     | Scope boundary echoes vision's out-of-scope list                                                                                          |
| `entity_model.md`     | Invariants overlap with `C-###`/`NFR-###` in `requirements.md`                                                                            |
| `use_cases.puml`      | Actor list restates roles already defined in `glossary.md`                                                                                |
| `use_cases/*.md`      | Actor reference resolves against `glossary.md`; `FR→UC` mapping duplicates `use_cases.puml`                                               |
| `specs/<cap>/spec.md` | Each `### FR-###` entry restates the requirement's scope from `requirements.md`; scenarios restate `use_cases/*.md` content in delta form |
| `testing.md`          | References `NFR-###`/`C-###` thresholds by ID, never restates them; universal test philosophy referenced from `tdd` skill, not copied     |
| `review.md`           | Restates FR/UC IDs from upstream; verdict summarises coverage already visible in `use_cases/*.md` + `specs/`                              |
| `tasks.md`            | Derives from `use_cases/*.md` scenarios + `testing.md` — no new requirements, only sequencing                                             |

---

## Artifacts added per change — M2 (Hybrid / GitHub bridge)

> **Settled decisions:**
> 
> - The `prd` node is **M2 only** — gated on M1-B1 proving the spine. See ADR-0002.
> - The thin PRD is a **projection**, not an authored origin: it lives on the tracker (not in the
>   repo), links spine IDs (`FR/UC/BR/ADR`), and duplicates no spine content. Only the
>   module-decomposition and testing-decisions sections are authored fresh.

### Production Sequence

| Artifact                          | Node  | Produced by                      | Requires                                  |
| --------------------------------- | ----- | -------------------------------- | ----------------------------------------- |
| thin PRD *(on tracker, not repo)* | `prd` | `/opsx:continue` + `spec-to-prd` | `[requirements, use-cases-spec, testing]` |

### Content

| Artifact | Content                                                                                                                                                                                                                                                           |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| thin PRD | 7-section PRD (Problem · Solution · User Stories · Implementation Decisions · Testing Decisions · Out of Scope · Further Notes); **links** spine IDs, restates no spine content; authors fresh only module decomposition + testing decisions. One PRD per change. |

### Delta Information

| Artifact | New information (not present in input artifacts)                               |
| -------- | ------------------------------------------------------------------------------ |
| thin PRD | Module decomposition and testing decisions — not present in any spine artifact |

### Redundancies

| Artifact | Redundant information (restates content from upstream artifacts)                         |
| -------- | ---------------------------------------------------------------------------------------- |
| thin PRD | Deliberately duplicates nothing — links `FR/UC/BR/ADR` IDs rather than restating content |
