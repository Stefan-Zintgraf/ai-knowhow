# OpenSpec 1.4.1 — migration & re-use review

**Date:** 2026-06-09
**Question:** Can the ai-mail workflow/skillset (`skills/`) be **adjusted to / re-used in** OpenSpec
1.4.1, rather than reinvented? It is partly derived from `matt_pocock_skills`, the `aiup-core`
skillset, and the guardrails in `coding/gr/*.md`. The goal is to **keep the best ideas** from those
sources and host them on OpenSpec where OpenSpec earns its keep.
**Basis:** read of `C:\PROJ\github\OpenSpec.1.4.1` v1.4.1 (`package.json` → `1.4.1`) — `README.md`,
`docs/opsx.md`, `docs/concepts.md`, `docs/customization.md`, `docs/migration-guide.md`,
`schemas/spec-driven/schema.yaml` + templates, `src/core/templates/workflows/*.ts`; cross-read of
`skills/workflow.md`, `skills/skills_overview.md`, `skills/artifacts.md`, `skills/skillfactory/*`,
`skills/CLAUDE.md`, and `coding/gr/gr_*.md`.
**Scope:** this is an **exploratory architecture review + work-item plan**, not an execution order.
It does **not** start the migration (mirrors `skill_genericity_review.md`). It is a `skillfactory`
analysis doc, so — like `milestone_review.md` — it names ai-mail specifics; the *target schema content*
it prescribes still keeps every skill project-agnostic (`skills/CLAUDE.md`), with project values
arriving via OpenSpec's own `config.yaml`.

## Project layout & source of truth (read-only ai-mail)

This migration is its **own standalone project** at `C:\PROJ\ai-knowhow\coding\OpenSpecEngine\`,
**separate from the ai-mail product project** — it does not modify ai-mail.

- **Source (read-only):** ai-mail at `C:\PROJ\ai-mail\`. Every reference in this document and its ADRs to
  `skills/…`, `docs/…`, `todo.md`, or `plan/…` is a **read-only pointer into that repo** — the material
  being migrated *from*. `coding/gr/…` = `C:\PROJ\ai-knowhow\coding\gr\` (the guardrail rules), also
  read-only.
- **Target (all writes):** `OpenSpecEngine/`. **All new artifacts** — the OpenSpec schema, `config.yaml`,
  the generic skills, and this project's own docs/ADRs — are **created here**, never in ai-mail.
- **Override:** this rule **supersedes** any work-item phrasing below that implies editing ai-mail (e.g.
  "update the skillfactory docs", "made generic in place"). Such items instead **create the generic
  OpenSpecEngine equivalent** from the read-only ai-mail original. The only ai-mail file this effort
  touches is a one-line back-pointer already added to its `todo.md`.

---

## TL;DR

1. **Feasible, and a genuinely strong fit for the authoring spine.** OpenSpec's OPSX workflow *is* a
   schema-driven **artifact DAG** (`schema.yaml`: `artifacts: [{id, generates, template, instruction,
   requires}]`) driven by a CLI state machine and thin per-tool skills. The ai-mail **authoring chain**
   (`declare-milestone → vision → grill → requirements → entity-model → use-case diagram → use-case spec
   → testing → prd`) is *already* that exact shape — `workflow.md` is a hand-written topological sort of
   the same DAG. Re-housing it as a **custom OpenSpec schema** is a transcription, not a rewrite.
2. **The two halves of the skillset migrate very differently.**
   - **Authoring skills** (produce a chain artifact) → OpenSpec **schema artifacts** (`instruction` +
     `template` + `requires`). Clean 1:1.
   - **Lens skills** (step-agnostic, cross-cutting: `ubiquitous-language-guard`, `pareto-scope-cut`,
     `adr-threshold-gate`, `hidden-constraint-sweep`, `trace-check`, `tracker-trace-check`) have **no
     native OpenSpec equivalent** — OpenSpec has no "gate that runs on every artifact." Keep them as
     **portable Claude Code skills composed on top**, *referenced from* each artifact's `instruction`,
     plus one **`review` (verify-style) artifact** that makes the fail-closed coverage/trace gate
     schema-visible.
3. **Guardrails map onto OpenSpec's own injection points.** `gr_*.md` rule clusters → `config.yaml`
   **`context`** (the always-on digest) + per-artifact **`rules`** (`<rules>` blocks). The
   `skills_overview.md` "Relation to guardrail items" sections are *already written as per-artifact rule
   lists* — they transpose almost verbatim into `rules:`.
4. **`milestone` ≡ OpenSpec `change`.** This resolves the tension `milestone_review.md` wrestled with:
   OpenSpec already owns "one unit of in-scope work = one self-contained folder." `declare-milestone`
   becomes **change creation** (`/opsx:new`/`/opsx:propose`) + `.openspec.yaml` metadata. Milestone N+1
   becomes a **delta change** against the accumulated `openspec/specs/` — which is *better* than ai-mail's
   "re-run the whole chain," and is the single biggest thing OpenSpec gives ai-mail for free.
5. **Three real tensions, all surmountable, but they cost rigor unless compensated** — (a) OpenSpec is
   deliberately **fluid / "dependencies are enablers, not gates,"** whereas ai-mail's value is
   **fail-closed coverage + HITL between every step**; (b) OpenSpec specs use **named** `### Requirement:`
   blocks, ai-mail's traceability hinges on **stable `FR/NFR/UC/BR/ADR` IDs**; (c) OpenSpec is
   **delta/brownfield**-first, ai-mail is **greenfield-spine**-first. None is a blocker; each needs a
   deliberate decision (see §9).
6. **Recommendation: stage it as two milestones, fused with the genericity refactor.** Build a project-agnostic
   **custom schema** that hosts the ai-mail authoring chain on OpenSpec's engine, inject guardrails via
   `config.yaml`, keep the lenses as composed skills. **Milestone 1 (Basic) = Pure OpenSpec** — the spine
   runs fully in-repo (`tasks.md` + `/opsx:apply` + `/opsx:archive` merging deltas into `openspec/specs/`),
   no GitHub tracker; this proves the engine on the smallest surface. **Milestone 2 (Full) = Hybrid** —
   layer the GitHub execution bridge (`spec-to-prd`/`to-issues`/`tracker-trace-check`/`triage`) on the
   proven Basic spine. **Run the migration as ONE project-agnostic pass with the in-flight genericity
   refactor** (`skill_genericity_review.md`, `domain-requirements`, `declare-milestone`) — DEC5 = Option D:
   migrating a skill into a generic OpenSpec node *is* making it generic, so the two efforts fuse and there
   is no double-transcription (§10). The two-milestone split is itself the Pareto / one-slice discipline the
   skillset preaches, applied to its own migration.

---

## 1 · What OpenSpec 1.4.1 actually is (and is not)

OpenSpec is an **npm CLI + a generated skill layer**, not a framework you import. Its current ("OPSX")
workflow has four moving parts:

| Part | What it is | Where it lives |
|---|---|---|
| **Schema** | A DAG of *artifacts*: `{id, generates (file/glob), template, instruction, requires[]}` + an `apply:` block. Defines the whole workflow. | `openspec/schemas/<name>/schema.yaml` (project-local, version-controlled) or `~/.local/share/openspec/schemas/` (global) |
| **Templates** | Markdown skeletons (section headers + HTML-comment guidance) injected when an artifact is created. | `openspec/schemas/<name>/templates/*.md` |
| **Project config** | `context:` (prepended to **all** artifact instructions, `<context>` tags) + `rules:` (per-artifact, `<rules>` tags) + default `schema:`. 50 KB context cap. | `openspec/config.yaml` |
| **Generated skills/commands** | Thin, schema-agnostic drivers (`/opsx:propose|explore|new|continue|ff|apply|verify|sync|archive`). They call `openspec status --json` / `openspec instructions <artifact> --json`, read the returned `template`/`instruction`/`context`/`rules`/`dependencies`, then create **one** artifact. | `.claude/skills/openspec-*/SKILL.md` (regenerated by `openspec init` / `update`) |

Two storage areas (`docs/concepts.md`):

- **`openspec/specs/`** — the **source of truth**: how the system *currently* behaves, as
  `### Requirement:` / `#### Scenario:` (RFC-2119 SHALL/MUST, Given/When/Then).
- **`openspec/changes/<change>/`** — a **self-contained change folder** (`proposal.md`, `design.md`,
  `tasks.md`, `.openspec.yaml`, and **delta specs** `specs/<cap>/spec.md` as `ADDED`/`MODIFIED`/`REMOVED`).
  **Archive** merges the deltas into `openspec/specs/` and moves the folder to `changes/archive/`.

Design philosophy (`README.md`, `docs/concepts.md`): *fluid not rigid · iterative not waterfall · easy
not complex · brownfield-first.* Explicitly: **"dependencies are enablers, not gates."** `requires`
controls *ordering*, never a *quality gate* and never a *human-review* gate.

The closest thing to an ai-mail "lens" is the **`verify`** workflow (`verify-change.ts`): a
completeness/correctness/coherence report (`CRITICAL`/`WARNING`/`SUGGESTION`) — but it checks
**implementation vs. artifacts**, not **artifact-internal quality** (no language audit, no scope cut, no
ADR gate, no FR↔UC coverage). So the lenses are net-new value OpenSpec does not have.

**Customization path is first-class:** `openspec schema fork spec-driven <name>` /
`openspec schema init <name>` / `openspec schema validate <name>` / `openspec schema which`. The whole
point of OPSX over legacy OpenSpec was to move the workflow *out of TypeScript* into editable
YAML+Markdown (`docs/opsx.md` "Why This Exists"). That is exactly the seam a migration needs.

## 2 · The ai-mail skillset, classified by how it migrates

| Class | Skills | Produces | Migration target |
|---|---|---|---|
| **Authoring** | `declare-milestone`, vision step, `domain-requirements`, `domain-model`, `usecase-diag`, `usecase-spec`, `testing-strategy`, `spec-to-prd` | a fixed-name chain artifact | **schema `artifact`** (`instruction`+`template`+`requires`) |
| **Lens** (step-agnostic) | `ubiquitous-language-guard`, `pareto-scope-cut`, `adr-threshold-gate`, `hidden-constraint-sweep`, `trace-check`, `tracker-trace-check` | a report + HITL write-back | **composed portable skill** + one `review` artifact (§4) |
| **External** (matt_pocock) | `bmad-brainstorming`, `grill-with-docs`, `prototype`, `to-issues`, `tdd` | inception / glossary / issues / code | mostly **unchanged**; `apply`/tasks bridge (§8) |
| **Meta** | `review-skills`, `refactor-skills` | skill-maintenance worklists | **unchanged** — orthogonal to OpenSpec |
| **Rule source** | `coding/gr/gr_*.md` (L/G/D/A/Adr/Aln/Rev/Gov/Doc…) | the discipline each skill operationalizes | **`config.yaml` `context` + per-artifact `rules`** (§5) |

The load-bearing observation: **`workflow.md` and `create_skills.md` already *are* OpenSpec's engine,
hand-rolled.** `workflow.md` is the topological sort; `create_skills.md`'s orchestration rule (one cold
sub-agent per unit, strict order, flip the checkbox on POST) is a bespoke `openspec status` + `instructions`
+ `continue` loop. Migration is mostly *letting OpenSpec's CLI own the state/ordering you currently
maintain by hand.*

## 3 · The core mapping — authoring chain → custom schema

Each authoring step becomes one artifact node. The `requires:` edges are read straight off `workflow.md`.

| ai-mail step (artifact) | OpenSpec artifact `id` | `requires` | Notes |
|---|---|---|---|
| `declare-milestone` | *(change creation)* | — | Not an artifact — it is **creating the change** + `.openspec.yaml`. Milestone ≡ change (§6). |
| vision (`vision_template.md` → `vision.md`) | `vision` | `[]` | Root node — plays the role `proposal` plays in `spec-driven`. |
| `grill-with-docs` → `CONTEXT.md` + ADRs | `glossary` (+ ADRs as decisions) | `[vision]` | Seeds the ubiquitous language **before** requirements (the load-bearing ordering rule in `workflow.md`). |
| `domain-requirements` → `requirements.md` | `requirements` | `[vision, glossary]` | The FR/NFR/C/OOS catalog. Template carries `FR-###` etc. (§7). |
| `domain-model` → `entity_model.md` | `entity-model` | `[requirements]` | Conceptual model + invariants. |
| `usecase-diag` → `use_cases.puml` | `use-cases-diagram` | `[requirements, entity-model]` | `generates: use_cases.puml`. Forward FR→UC coverage. |
| `usecase-spec` → `use_cases/*.md` | `use-cases-spec` | `[use-cases-diagram]` | `generates: 'use_cases/**/*.md'` (glob). Reverse FR→spec coverage + `BR-###`. |
| FR + UC scenarios → behaviour contract | `specs` | `[use-cases-spec, entity-model]` | `generates: 'specs/**/*.md'`. Delta specs (`### Requirement: FR-### …` / `#### Scenario`) that accrete into `openspec/specs/` on archive — **DEC4 adopt** (§6, §7). |
| `testing-strategy` → `testing/<m>.md` | `testing` | `[requirements]` | One per change. |
| `spec-to-prd` → tracker PRD | `prd` *(GitHub bridge)* | `[requirements, use-cases-spec, testing]` | **Milestone 2 only** — the GitHub projection (§8). |
| — *(new)* coverage/trace gate | `review` | `[specs, use-cases-spec, entity-model]` | A `verify`-style artifact hosting `trace-check`'s A–D + FR↔UC coverage (§4). |

The matt_pocock spine (`to-issues` → `tdd`) maps onto OpenSpec's terminal artifacts/actions: `tasks`
(generated from the PRD/spine) + `apply:` (`tracks: tasks.md`) is exactly the `to-issues`→`tdd` loop.

What an artifact node looks like (sketch — generic; project values come from `config.yaml`):

```yaml
- id: requirements
  generates: requirements.md
  template: requirements.md
  instruction: |
    Author the requirements catalog from the vision and glossary (read both deps).
    Emit FR (user-story), NFR (measurable), Constraints, and Out-of-Scope tables, each row
    with a stable ID and a filled Status. Use glossary terms VERBATIM (L1). Flag — never coin
    — new terms (L6). Carry the vision's non-goals into Out-of-Scope (Aln15).
    AFTER writing, run the composed lenses: ubiquitous-language-guard, pareto-scope-cut,
    hidden-constraint-sweep. Resolve or record their findings before this artifact is "done".
  requires: [vision, glossary]
```

## 4 · The lenses — the one part OpenSpec has no slot for

Lenses are **step-agnostic** (one lens runs on requirements *and* the entity model *and* the use-case
spec *and* the PRD draft) and **HITL** (write-back only on approval). OpenSpec artifacts are
**single-position DAG nodes**. So a lens is the wrong shape for an artifact node. Three options, ranked:

1. **Composed portable skills, referenced from `instruction`/`rules` (recommended).** The lenses stay in
   `skills/` exactly as they are (portable, generic, already gr-mapped). Every artifact's `instruction`
   ends with *"after writing, run `ubiquitous-language-guard` + `hidden-constraint-sweep` …"*. OpenSpec
   owns the DAG + state; the lenses stay independent. **Keeps the genericity investment, doesn't fight the
   "no gates" grain, zero rewrite.**
2. **One `review` (verify-style) artifact** for the checks that *must* be a visible gate — `trace-check`
   A–D + the fail-closed FR↔UC coverage. This is the only lens that benefits from being a schema node
   (it depends on the *whole* spine being present), and it gives the migration a place to re-introduce
   the **fail-closed** behaviour OpenSpec's philosophy otherwise drops. Model it on `verify-change.ts`'s
   report structure, but check *artifact-internal* coverage, not implementation.
3. ✗ **One lens = one artifact** — rejected. You'd need N copies of each lens (one per position) and you'd
   distort a cross-cutting check into a node, losing exactly what makes it step-agnostic.

Net: **lenses 1–5 stay as skills (option 1); `trace-check` additionally gets a `review` node (option 2);
`tracker-trace-check` survives only if the GitHub tracker survives (§8).**

## 5 · Guardrails → `config.yaml` (the cleanest mapping in the whole exercise)

`gr_*.md` is *content*, and OpenSpec has two injection points purpose-built for it:

- **`context:`** — a tight digest of the always-on discipline (ubiquitous language L1/L6, greenfield
  Pareto G1/G3/G9/G10, "infrastructure out of the domain" A9/A10). Injected into **every** artifact.
  50 KB cap → digest, don't paste the gr files. Mirror of the `project.md → config.yaml` migration the
  OpenSpec guide itself prescribes (`docs/migration-guide.md`).
- **`rules:`** keyed by artifact `id` — the *per-artifact* gr subset. The `skills_overview.md` "Relation
  to guardrail items" sections are already exactly this list:

```yaml
rules:
  requirements: [ "Use glossary terms verbatim (L1)", "Flag, never coin, new terms (L6)",
                  "Carry non-goals into Out-of-Scope (Aln15)", "requirements.md SUMMARIZES alignment (Aln13)" ]
  entity-model: [ "Classify every term Entity/VO/Aggregate (D1/D2/D5)", "No surrogate ids / infra in conceptual mode (A9)" ]
  specs:        [ "RFC-2119 SHALL/MUST", "Given/When/Then scenarios", "≥1 scenario per requirement" ]
```

This is the single highest-leverage, lowest-risk piece of the migration and is reversible.

## 6 · `milestone` ≡ `change` — the conceptual bridge

`milestone_review.md` concluded a milestone is "the in-scope slice one PRD-loop iteration ships," declared
up front by `declare-milestone`, feeding a milestone-bound vision, **without forking the spine**. OpenSpec
*is built around exactly this unit*: a **change** is "one planned piece of work … a self-contained folder."
So:

- `declare-milestone` ≈ `/opsx:new <change>` (scaffold) + `.openspec.yaml` (record the committed
  capability/`F`-set + predecessor as metadata). The Pareto/dependency/shipped-state selection logic stays
  — it just writes a change folder instead of a `## Milestones` register line.
- **The milestone-N+1 loop-back is where OpenSpec pays off.** Today ai-mail re-runs the whole chain per
  milestone. OpenSpec instead opens a **new change** whose `specs/` are **deltas** (`ADDED`/`MODIFIED`/
  `REMOVED`) against the accumulated `openspec/specs/`, and **archive** merges them. The spine is *not*
  forked (satisfying `milestone_review.md` §5); the source of truth **accretes**. This is strictly better
  than the status-column reconstruction for N≥2.

## 7 · Stable IDs & traceability vs. named requirements

OpenSpec specs use `### Requirement: <name>` (no numeric IDs); ai-mail's `trace-check`,
`tracker-trace-check`, `usecase-spec`, and `spec-to-prd` hinge on `FR/NFR/UC/BR/ADR-###` IDs. Two paths:

- **(A, recommended) Keep ai-mail IDs *inside* OpenSpec templates.** Templates are fully user-owned, so
  `### Requirement: FR-001 — <name>` is legal and free. Crucially, the ai-mail lenses already **discover
  id patterns from the files** (`trace-check` "discovers conventions rather than assuming them"), so they
  keep working against OpenSpec-housed artifacts with **no change**. Cost: near-zero.
- **(B) Adopt named requirements, rebuild traceability around names.** Aligns with vanilla OpenSpec and
  its `verify`, but throws away the ID-based traceability the whole AIUP chain is built on. Cost: high.

Take (A). The FR→Requirement and UC-scenario→Scenario shapes line up so well that ai-mail's use-case
scenarios *are* OpenSpec scenarios with IDs bolted on.

## 8 · The tracker boundary — keep GitHub, or go in-repo?

ai-mail Phase 4 projects the spine onto **GitHub issues** (`spec-to-prd` → `to-issues` → `triage`, audited
by `tracker-trace-check`). OpenSpec has **no tracker** — "done" = `archive` merges deltas into
`openspec/specs/`. Two models:

- **Hybrid (recommended).** OpenSpec owns *planning + spec evolution* (the spine, `specs/`, archive).
  `spec-to-prd`/`to-issues` stay as the **bridge to GitHub** for AFK-agent *execution*; `tdd` ≈ `apply`.
  `tracker-trace-check` becomes the `openspec/specs ↔ tracker` drift audit. You keep the AFK-agent issue
  flow ai-mail already invested in, and gain OpenSpec's spec accretion.
- **Pure OpenSpec.** Drop the GitHub projection; execute via `tasks.md` + `/opsx:apply`. Simpler, but
  loses the issue-tracker/triage machinery and the `ready-for-agent` AFK loop. Only worth it if the
  GitHub tracker is not actually load-bearing.

**Resolution (DEC2): sequenced, not chosen.** **Milestone 1 (Basic) adopts Pure** (smallest surface — the
spine on OpenSpec, in-repo, no tracker; `spec-to-prd`/`to-issues`/`tracker-trace-check`/`triage` are out of
scope). **Milestone 2 (Full) adds the Hybrid GitHub bridge** on top of the proven Basic spine. So Pure is
not a rejected option — it is the first slice; Hybrid is the second. The two-milestone work-item plan below
is organised this way.

## 9 · The honest tensions (what the migration costs)

1. **Rigor vs. fluidity.** ai-mail's worth is *fail-closed coverage + HITL between every step*. OpenSpec
   removes gates by design. `requires` gives ordering, not gates. **Mitigation:** the lenses (§4 option 1)
   + the `review` node (§4 option 2) + HITL phrasing in `instruction`s re-introduce the gates as
   *discipline*, not *engine-enforced*. Accept that some rigor moves from "the tool blocks you" to "the
   instruction tells you to block yourself."
2. **Delta model reshaping.** To get the §6 payoff you must express the behaviour-contract layer (FRs +
   use-case scenarios) as `openspec/specs/<cap>/spec.md`. The upstream reasoning artifacts (vision,
   entity model, ADRs, testing) stay as plain planning artifacts. That reshaping is real work for the
   *requirements + use-case* artifacts specifically.
3. **Two engines, one job.** Adopting OpenSpec means **retiring or subordinating** `workflow.md` as the
   orchestrator and letting `openspec` own state. Half-adopting (OpenSpec for some steps, hand-rolled for
   others) is the worst outcome — two sources of truth for "what's next." → flagged HITL (§D-DEC1).
4. **WIP target.** The skillset is mid-refactor (`todo.md`: `declare-milestone` just built,
   `domain-requirements` being made generic, `skill_genericity_review.md` open). Migrating now means
   re-transcribing every artifact again after the refactor lands.

## 10 · Recommendation

**Yes — host the ai-mail authoring chain on OpenSpec as a custom schema, keeping the lenses as composed
skills, staged as two migration milestones (Basic/Pure → Full/Hybrid) and fused with the genericity
refactor as one project-agnostic pass (DEC5 = Option D).**

Target architecture:

- A project-agnostic custom schema (generic name, e.g. `spec-spine`) = the §3 artifact DAG.
- `config.yaml` = guardrail digest (`context`) + per-artifact gr subsets (`rules`), §5.
- Lenses = unchanged portable skills, referenced from `instruction`s; `trace-check` also a `review` node, §4.
- `milestone` ≡ `change`; N+1 via delta specs + archive, §6. Stable IDs kept in templates, §7.
- GitHub execution tracker (`spec-to-prd`/`to-issues`) is **Milestone 2 (Full)** only; **Milestone 1
  (Basic)** executes in-repo via `tasks.md` + `/opsx:apply`. OpenSpec owns the spine throughout, §8.
- `review-skills`/`refactor-skills` are **out of scope** — not migrated, not adjusted. They keep operating
  on the remaining lens SKILL.md files; the dissolved authoring nodes' QA moves to `openspec schema
  validate` + the `review` node + dry runs. Extending the meta-layer to review schema nodes is a
  **separate future enhancement, not part of this migration**.

**Why this honours "don't reinvent":**

- **From OpenSpec** ← the DAG engine + CLI state machine (`status`/`instructions`/`apply`/`archive`), the
  change-folder + delta-spec + archive→specs accretion, `config.yaml` injection, cross-editor skill
  generation. *Replaces* the hand-rolled `workflow.md`/`create_skills.md` orchestration and the
  per-milestone "re-run the chain."
- **From aiup/ai-mail** ← the *content*: authoring instructions, the gr rule-mappings, the lenses, the
  stable-ID traceability, `declare-milestone`, `testing-strategy`. *Becomes* `instruction`/`template`/
  `rules` + composed skills.
- **From matt_pocock** ← `spec-to-prd`/`to-issues` (GitHub bridge) + `tdd` (≈ `apply`) + `prototype`/
  `bmad-brainstorming`/`grill-with-docs` for inception.
- **From the guardrails** ← `context` digest + per-artifact `rules`.

**Timing (DEC5 = Option D):** run the genericity refactor and the migration as **one project-agnostic
pass** — migrating a skill into a generic OpenSpec node *is* making it generic, so there is no
double-transcription and no reason to sequence them. The todo.md "cleanup all skills from ai-mail-specific
stuff" items *become* migration work items. The cheap, reversible **first taste** is still the smart opener
(§M1-A0): `config.yaml` context/rules against the *default* `spec-driven` schema — no schema authoring,
proves the guardrail injection, throwaway — then M1-A1's churn-independent schema skeleton.

---

## Evidence index

- `package.json`:version → **1.4.1**.
- `docs/opsx.md`:55–58,592–606,624–645 — schema DAG (`id/generates/requires/template/instruction`),
  `schema fork/init/validate/which`, "dependencies are enablers, not gates."
- `docs/concepts.md`:196–344,490–549,646–700 — specs vs. changes, delta specs (ADDED/MODIFIED/REMOVED),
  archive→specs merge, `### Requirement:`/`#### Scenario:` format.
- `docs/customization.md`:60–80,150–200,340–351 — `context`/`rules` injection (`<context>`/`<rules>`),
  schema fields, community-schema distribution model.
- `docs/migration-guide.md`:160–256 — `project.md → config.yaml` (the guardrail-injection precedent).
- `schemas/spec-driven/schema.yaml` — the canonical artifact-DAG + `apply:` block this plan forks.
- `src/core/templates/workflows/{continue,verify}-change.ts` — generated skills are thin CLI drivers
  (`openspec status/instructions --json`); `verify` is impl-vs-spec, not artifact-internal (the lens gap).
- `skills/workflow.md` — the existing hand-rolled DAG (= the schema, pre-transcription).
- `skills/skills_overview.md` "Relation to guardrail items" per skill — = the per-artifact `rules:` lists.
- `skills/skillfactory/milestone_review.md` §2–§6 — milestone ≡ change; "no per-milestone spine fork."
- `coding/gr/gr_*.md` — the rule clusters that become `context` + `rules`.

---

## Work items — orchestrated migration plan (2 milestones)

> Staged as **Milestone 1 — Basic (Pure OpenSpec)** then **Milestone 2 — Full (Hybrid + GitHub bridge)**
> (DEC2). In a fresh session, tell the agent: *"apply the Milestone 1 Part A build in
> `docs/openspec_migration.md` (this project) using sub-agents."* Each Part A is
> documentation/config only and self-contained. **Do not start Milestone 1 until D-DEC3/D-DEC4/D-DEC5 are
> settled with the human** (D-DEC1/D-DEC2 are decided) — they fix Milestone 1's schema shape. **Milestone 2
> starts only after Milestone 1 is proven (M1-B1).**

### Orchestration rule (same as `milestone_review.md` §8 / `create_skills.md`)

Carried out by a single **driver session** that spawns **one cold sub-agent per unit**, runs them
**strictly sequentially in number order, never in parallel**, and flips each `- [ ]` to `- [x]` **only
after** that sub-agent reports its POST self-check passed. On a blocker the driver leaves the box `- [ ]`,
appends `> blocked: <reason>` after the heading, continues with the rest, and surfaces all blockers at the
end. Each unit is self-contained: the driver hands its sub-agent the matching unit block **plus** §1–§10 of
this review **plus** the named target files — nothing else.

**Ordering:** within each milestone, **`*-A1` produces the schema skeleton the later `*-A#` fill**, so A1
completes first; **Part B (validate) runs after Part A**; **Milestone 2 runs only after Milestone 1's B1
proves the spine.** The still-open D-DEC3/D-DEC4/D-DEC5 fix Milestone 1's schema shape and must be settled
first. **No skill is *run* in any Part A** (it authors schema/config *text*), so no run-time HITL gate
fires; a sub-agent hitting a genuinely unspecified choice **stops and records `> blocked:`** rather than
guessing.

### Execution method per work-type

*How* to carry out the units below — routed by work-type, biased toward the project's own tooling rather
than a single framework. **The recursion has two OpenSpec levels — keep them apart (DEC6):**

- **Level 1 — the custom `<spine-name>` schema** (the deliverable). Does not exist yet, so it cannot manage
  its own construction (chicken/egg). This is the *only* place that objection holds.
- **Level 2 — OpenSpec's stock `spec-driven` schema + OPSX CLI** (change folder, `tasks.md`, `apply`,
  `archive`). Exists today; **used to manage the remaining build as a change** (the dogfood envelope, DEC6)
  and as the engine under test in Part B. No chicken/egg.

The trap (DEC6): the migration's own Orchestration rule (strict sequential, flip the box **only** on POST
pass — fail-closed) is the rigor §9.1 says OpenSpec lacks. So OpenSpec owns the **envelope + Part B**, but
the **driver keeps Part A sequencing**.

| Work-type in this plan | Units | Method | Why |
|---|---|---|---|
| Align the migration **itself** (glossary + ratify the free-styled ADRs) | `M1-P0` (pre-flight) | **grill-with-docs** → `CONTEXT.md` + amended ADRs | all 6 ADRs were free-styled, not grilled, and `CONTEXT.md` was never produced — downstream nodes must use its terms verbatim (L1). |
| Manage the remaining build as one unit of work (change folder, ordering, tracking, "done") | `M1-P1` (bootstrap) + all of M1/M2 | **OpenSpec stock `spec-driven` change — dogfooded (Level 2, DEC6)** | cheapest validation of the central bet (0001) before the custom schema depends on it; `M1-A0`'s `openspec init` folds in here. |
| Settle / re-open a design fork | a re-opened `D-DEC#`; any `> blocked:` an A-unit records | **grill-with-docs** → ADR in `docs/adr/` | keeps the decision trail; how 0001–0006 *should* have been captured. Free-style loses the ADR. |
| Author `schema.yaml` / templates / `config.yaml` **text** | `M1-A1…A7`, `M2-A1…A5` | **free-style in the cold sub-agent; the driver — not OPSX — owns the fail-closed sequencing** (DEC6) | transcription from §3 + Appendix B; OpenSpec *tracks* these as `tasks.md` but does not generate them, and surrendering Part A to `/opsx:continue` would drop the POST gate (§9.1). |
| (Re-)create a **lens** as a generic portable `SKILL.md` (DEC5) | the lens re-creation behind `M1-A2`'s composed-lens lines | **closest fit = the coding_workflow `/make-skill` chain**; else free-style from the read-only ai-mail original | lenses become standalone generic SKILL.md — what `draft→compile→test` produces. Not a clean 1:1 (make-skill is tuned to coding_workflow's own docs), so fall back to free-style if it fights. |
| Validate / dry-run the **custom** schema | `M1-B1`, `M1-B2`, `M2-B1`, `M2-B2` | **OpenSpec CLI** (`schema validate`, `/opsx:new → continue → apply → archive`) | the engine under test; Part B is where OpenSpec earns its keep (§1, §10). |
| A `M1-B1`/`M2-B1` dry-run fails | conditional | **`diagnose`** (matt_pocock) | the one other Pocock skill with surface here; reproduce → instrument → fix the schema/config. |
| Inception **before** `vision` *when the finished schema is later run on a real project* (not a unit in this plan) | — | **grill-with-docs / prototype / bmad-brainstorming** (matt_pocock, unchanged) | §10 keeps these as-is; they feed the `vision` root node of the **product** spine, not the build of this schema. |

> **Note — Pocock-skill surface is genuinely thin here, and that is correct, not a gap.** Most Pocock
> skills target *code-building* (`tdd`, `diagnose`) or *product-spine inception* (`to-prd`, `to-issues`,
> `prototype`); this build authors **schema/config text**, which is neither. So `grill-with-docs` (P0 +
> reopened forks) and a conditional `diagnose` (B1 failure) are the honest extent — forcing more would be
> cargo-culting.

> **Decisions (prerequisites — drafted 2026-06-09, NOT yet ratified).** These forks are each **ADR-worthy**
> and **captured as ADRs in `OpenSpecEngine/docs/adr/0001–0006`**. **⚠ All six are `proposed`, not
> `accepted`** — 0001–0005 were authored by a free-style prompt and never grilled; 0006 (dogfood OpenSpec
> for the build) was reasoned deliberately but still wants grilling. They fix Milestone 1's schema shape, so
> **`M1-P0` must ratify or amend them (flip `proposed → accepted`) before Part A authoring begins.** D-DEC6
> additionally gates `M1-P1` (the dogfood envelope). The summaries below are the *draft* positions entering
> that grill:
>
> - **D-DEC1 · Orchestrator — ✅ DECIDED (2026-06-09): OpenSpec replaces `workflow.md` as the single
>   authoritative orchestrator.** `schema.yaml` becomes the one source of "what's next"; `workflow.md`'s
>   content is **harvested, not duplicated** — Job A (ordering) → `requires` edges; Jobs B & C
>   (between-step HITL reviews + operational sub-procedures like the 5a–5f gap loop) → node `instruction`s
>   + the `review` node. **Enable the EXPANDED profile** (`/opsx:continue` one-artifact-at-a-time — *not*
>   core `/opsx:propose`, which generates the whole spine in one shot and would destroy
>   review-between-every-step). **Gate handling:** the mechanical coverage/trace gate is a **fail-closed
>   `review` node** (sub-fork option 2); the soft "human, look at this" reviews are the
>   stop-after-each-`/opsx:continue` pauses + instruction-tail prompts (option 1). **Lenses are relocated,
>   not removed** — their SKILL.md files stay portable; only their standalone workflow lines disappear,
>   moving into node `instruction`s (+ lightweight `config.yaml` reminders), with `trace-check` promoted to
>   the `review` node. `workflow.md` is **retired-but-kept** as an annotated "harvested-from" source map
>   until B1 proves the schema, then archived. Phase-0 setup folds into `openspec init` + `config.yaml` +
>   the kept `/setup-matt-pocock-skills`.
> - **D-DEC2 · Tracker boundary — ✅ DECIDED (2026-06-09): sequenced, not chosen.** **Milestone 1
>   (Basic) = Pure** (in-repo; `spec-to-prd`/`to-issues`/`tracker-trace-check`/`triage` out of scope);
>   **Milestone 2 (Full) = Hybrid** (adds the GitHub bridge on the proven Basic spine). §8.
> - **D-DEC3 · ID convention — ✅ DECIDED (2026-06-09): keep stable IDs.** `FR/NFR/UC/BR/ADR-###` IDs are
>   carried verbatim in the templates (`### Requirement: FR-### — <name>`); the lenses discover ID patterns
>   so traceability keeps working unchanged. §7.
> - **D-DEC4 · Delta adoption — ✅ DECIDED (2026-06-09): adopt (10-node Basic).** The behaviour-contract
>   layer is a `specs` node generating `specs/**/*.md` delta specs that accrete into `openspec/specs/` on
>   archive (the §6 N+1 payoff). This makes Milestone 1 a **10-node** schema (adds `specs` between
>   `use-cases-spec` and `review`). §6, §9.2.
> - **D-DEC5 · Timing/approach — ✅ DECIDED (2026-06-09): Option D — fuse the genericity refactor and the
>   OpenSpec migration into ONE project-agnostic pass.** Migrating a skill into a node *is* making it
>   generic (OpenSpec's schema instructions/templates are project-agnostic by design; project specifics
>   live in `config.yaml`), so there is no double-transcription — D dissolves the earlier "refactor first"
>   rationale. **Consequence:** authoring skills **dissolve into schema nodes** (SKILL.md retires, made
>   generic in the node — single home, no Doc5 duplication); **lens skills are re-created as generic
>   portable SKILL.md in OpenSpecEngine** (from the read-only ai-mail originals); project specifics →
>   `config.yaml`. The todo.md
>   "cleanup all skills from ai-mail-specific stuff" items *become* migration work items. **Out of scope:
>   `review-skills` / `refactor-skills`** — not migrated, not adjusted; they keep running over the remaining
>   lens SKILL.md set, and extending them to QA schema nodes is a separate future enhancement. §10.
> - **D-DEC6 · Dogfood OpenSpec for the build — DRAFT (2026-06-09): manage the build as a Level-2 OpenSpec
>   change, but keep the fail-closed driver for Part A.** OpenSpec (stock `spec-driven`) owns the **change
>   envelope** (`design.md` → pointer to this doc + ADRs; `tasks.md` ← the M1/M2 units; `archive` on done)
>   and **Part B** (engine under test); the **strict cold-sub-agent driver keeps Part A sequencing** because
>   `/opsx:continue`'s "enablers, not gates" model would drop the POST gate (§9.1, recreated one level up).
>   Implemented by `M1-P1`. See [ADR-0006](adr/0006-dogfood-openspec-for-migration-build.md). Ratify at
>   `M1-P0`.

## Milestone 1 — Basic (Pure OpenSpec; in-repo, no tracker)

**Goal.** The full ai-mail authoring spine running end-to-end on OpenSpec, entirely in-repo. Execution is
`tasks.md` + `/opsx:apply`; "done" is `/opsx:archive` merging the change's delta specs into
`openspec/specs/`. **Out of scope (→ Milestone 2):** `spec-to-prd`, `to-issues`, `triage`,
`tracker-trace-check`.
**Nodes (10):** `vision`, `glossary`, `requirements`, `entity-model`, `use-cases-diagram`,
`use-cases-spec`, `specs` (behaviour-contract deltas → `openspec/specs/`), `review`, `testing`, `tasks`
(no `prd` node — Pure mode ends the planning DAG at `tasks`; DEC4 = adopt).
**Lenses:** language-guard, scope-cut, adr-gate, constraint-sweep (composed into nodes) + trace-check (the
`review` node). **Not** tracker-trace-check.
**Method (per work-type):** P0 = **grill-with-docs → `CONTEXT.md` + ratified ADRs** (run **first**); P1 =
**bootstrap the dogfood OpenSpec change envelope** (DEC6); Part A authoring = **free-style in cold
sub-agents, driver owns sequencing**; lens re-creation = **`/make-skill` chain** (else free-style); Part B =
**OpenSpec CLI**; re-opened decision = **grill-with-docs → ADR**. See
[Execution method per work-type](#execution-method-per-work-type).

### Milestone 1 · Part 0 — alignment + build-envelope bootstrap (human-in-the-loop)

**- [ ] M1-P0 · Grill the migration decisions → produce `CONTEXT.md` + ratify/amend ADRs**
- **Files:** `OpenSpecEngine/docs/CONTEXT.md` (new), `docs/adr/0001–0006` (amend in place + flip Status if grilling moves them).
- **Why:** ADRs 0001–0005 were authored by a **free-style prompt** and 0006 deliberately but unratified —
  **none grilled** — and **`CONTEXT.md` was never produced**, yet every downstream node
  `instruction`/`template` (M1-A2/A3) and the `context`/`rules` digest (M1-A4) must use the project glossary
  **verbatim** (L1). This pre-flight backfills the glossary and pressure-tests the decisions before they are
  baked into the schema.
- **Change:** run `grill-with-docs` **ONE ADR per fresh session** to avoid context rot — grill the
  lowest-numbered ADR whose box is still `[ ]` in the *ADR ratification progress* checklist below, and
  **only that one ADR**. Read the matching `openspec_migration.md` sections as *evidence only* (never
  amended) — §3 + §9 (DEC1/4/5), §6 + §7 + §8 (DEC2/3/4), §1 + §4 as glossary-source reads. One question
  at a time; surface unstated assumptions (hit hardest on DEC1 retire-`workflow.md` and DEC5 fuse-refactor;
  don't rubber-stamp DEC2/3/4; DEC6 is the only un-free-styled ADR). Extend the ubiquitous-language
  glossary in `CONTEXT.md` with the terms *this* ADR sharpens (cumulative target across all six sessions:
  schema, node, artifact, lens, change, milestone, delta-spec, fail-closed gate, EXPANDED profile, OPSX,
  envelope, driver, spine). Amend the ADR if the grill moves it, or leave a one-line ratified note if it
  survives; then flip its checklist box to `[x]` and **stop** — the next ADR is a separate fresh session.
- **ADR ratification progress** (the fresh-session agent reads this to pick the next ADR; flip the box
  when that ADR's grill completes, and record the outcome inline):
  - [x] 0001 · OpenSpec replaces `workflow.md` as orchestrator — ratified + amended 2026-06-10 (honest-discipline gate; hook → M2-A6)
  - [ ] 0002 · Two-milestone Basic/Pure → Full/Hybrid
  - [ ] 0003 · Keep stable FR/NFR/UC/BR/ADR IDs in templates
  - [ ] 0004 · Adopt delta/specs model (10-node Basic)
  - [ ] 0005 · Fuse genericity refactor with migration (Option D)
  - [ ] 0006 · Dogfood OpenSpec for the build (envelope + Part B)
- **Cross-ADR carry-overs** (reconciliations one grill owes a *later* ADR. The fresh-session agent MUST
  read the entries tagged to its selected ADR **before** grilling, address them during the session, then
  strike them through `~~like this~~` with a one-line outcome. When *your* amendment creates a new work
  item or changes another ADR's scope, **append** a new entry here tagged to that ADR):
  - → **0002:** M2-A6 (the deferred archive-time enforcement hook, added when ADR-0001 was ratified
    2026-06-10) is a new Milestone-2 work item that ADR-0002's M2 scope does not yet list. The 0002 grill
    must reconcile this — the hook is arguably a third M2 concern alongside the GitHub bridge. Amend
    ADR-0002's Decision/Consequences if it agrees.
- **Prompt (paste verbatim in a fresh session).** `grill-with-docs` grills "a plan/design in the
  conversation" — a fresh session has none, so the subject must be handed to it explicitly:

  ````text
  /grill-with-docs

  Grill me on ONE architecture decision for the OpenSpec migration — the next un-ratified ADR —
  to ratify or amend it and extend the project glossary. This is M1-P0 in
  docs/openspec_migration.md, run ONE ADR per fresh session to avoid context rot.

  WHICH ADR — open docs/openspec_migration.md, read the "ADR ratification progress" checklist in
  M1-P0, and grill the LOWEST-numbered ADR whose box is still [ ]. Grill ONLY that one ADR.

  SUBJECT — grill ONLY that single ADR (docs/adr/000X). It is the only thing you ratify or
  amend this session.

  EVIDENCE — read openspec_migration.md to pressure-test each DEC, but NEVER amend it. It is
  the frozen 2026-06-09 analysis; the ADR is the decision-of-record, not the prose. Where to
  read for each DEC:
  - §3 + §9 → DEC1 / DEC4 / DEC5
  - §6 (milestone≡change) + §7 (stable IDs vs named requirements) + §8 (tracker boundary)
    → DEC2 / DEC3 / DEC4 — their trade-offs live HERE, since the free-styled ADRs are thin
  - §1 + §4 → glossary-source reads (sharpen terms only)
  - §10, the work-item plan, README.md → consistency cross-check only
  ERRATA: if the grill finds a defect in migration.md's prose that is NOT itself a decision
  (stale cross-ref, wrong cell in a §3 mapping row, a gap in §9), add a dated inline errata
  note AT the defect (e.g. `> **Errata 2026-06-10:** superseded by ADR-000X — …`) pointing to
  the governing ADR — do NOT rewrite the analysis in place.

  WRITE TARGETS: docs/adr/0001–0006 (+ docs/adr/0007 if a new decision surfaces) and
  docs/CONTEXT.md. The openspec_migration.md §1–§10 ANALYSIS is frozen — only a dated errata note may
  be appended (see ERRATA). EXCEPTION: the M1-P0 "ADR ratification progress" checklist and "Cross-ADR
  carry-overs" list are LIVE process state — flip your box and add/strike carry-over entries there.

  GOALS:
  1. One question at a time. Pressure-test the SELECTED decision only. Sharpest angle per ADR:
     DEC1 (retire workflow.md) — rigor-as-discipline vs engine-enforcement; DEC5 (fuse genericity
     refactor + migration) — double-transcription claim; DEC6 (dogfood OpenSpec for the build) —
     the only deliberately-reasoned ADR, still unratified. DEC2/DEC3/DEC4: no rubber-stamp —
     DEC3 path-A reversibility (§7 A-vs-B), DEC4 delta-reshaping cost (§9.2), DEC2 Pure-first
     vs hidden Milestone-2 rework (§8 "sequenced, not chosen").
  2. As terms sharpen, write/extend the ubiquitous-language glossary in docs/CONTEXT.md (create if
     absent), adding the terms THIS ADR sharpens. Cumulative target across the six sessions:
     schema, node, artifact, lens, change, milestone, delta-spec, fail-closed gate,
     EXPANDED profile, OPSX, envelope, driver, spine.
  3. When the decision survives, flip its ADR Status proposed→accepted and add a
     "ratified via grill <current date>" note. When it moves, amend the ADR's Decision +
     Consequences inline. If the grill surfaces a hard-to-reverse decision not already in
     0001–0006, draft docs/adr/0007. THEN flip this ADR's box to [x] in the M1-P0 "ADR
     ratification progress" checklist and STOP — the next ADR is a separate fresh session.
  4. Write the ADR LEAN — it is re-read cold later, so keep ONLY: the decision, why, rejected
     alternatives with reasons, and consequences a future maintainer must not re-litigate. CUT process
     narration — grill mechanics, dates beyond the one-line ratified note, repo paths, and any evidence
     already in openspec_migration.md (cite it by § instead of restating — Doc5). The Status line carries
     the ratified/amended note; do NOT add a multi-line ratification banner.
  5. CARRY-OVERS — BEFORE grilling, read the M1-P0 "Cross-ADR carry-overs" list and address every entry
     tagged to YOUR ADR, then strike it through with its outcome. If your amendment adds a work item or
     changes another ADR's scope, APPEND a carry-over entry tagged to the affected later ADR so it is
     reconciled when that ADR is grilled.

  CONSTRAINTS: OpenSpecEngine is the only write target. ai-mail (C:\PROJ\ai-mail) and
  coding/gr are read-only sources — never edit them. This is a planning-only grill: no
  issue tracker / docs/agents/ setup is needed to grill and write CONTEXT.md + ADRs.
  ````
- **POST (per session):** the one selected ADR is re-affirmed (with a "ratified via grill <date>" note) or
  amended with the surfaced consequence; its `proposed → accepted` flip is done where it survives; its box in
  the *ADR ratification progress* checklist is flipped to `[x]`; `CONTEXT.md` exists and has been extended
  with the terms that ADR sharpened; no part of that decision left merely asserted.
- **POST (unit complete):** M1-P0 is done only when **all six** checklist boxes are `[x]` (six fresh
  sessions) and `CONTEXT.md` covers the cumulative load-bearing terms.

**- [ ] M1-P1 · Switch the build onto OpenSpec — bootstrap the dogfood change envelope (DEC6)**
> Gated by `M1-P0` ratifying DEC6. If the grill *rejects* DEC6, skip this unit and run the build under the
> markdown driver alone (the existing Orchestration rule), touching OpenSpec only at `M1-A0`/Part B.
- **Files:** a Level-2 OpenSpec change folder (stock `spec-driven`): `openspec/changes/<build-change>/`
  (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`). **Distinct** from the Level-1 custom
  `<spine-name>` schema authored by Part A — keep the two OpenSpec contexts in separate folders and name
  them explicitly (ADR-0006 §Consequences).
- **Change:** `openspec init` (this is where `M1-A0`'s init folds in); `/opsx:new <build-change>`; write
  `design.md` as a **pointer** to `openspec_migration.md` §1–§10 + `docs/adr/0001–0006` (restate nothing —
  Doc5); transcribe the M1 (then M2) work items into `tasks.md` as the checklist. Record the reconciliation
  rule: **the markdown Orchestration rule is authoritative for Part A "what's next" and "done"; `tasks.md`
  mirrors status** — one source of truth per unit, no drift. Part B units (`M1-B*`) and `/opsx:apply`/
  `/opsx:archive` then operate through this envelope.
- **POST:** the build-change folder exists and validates; `design.md` points at (does not duplicate) the doc
  + ADRs; `tasks.md` carries the M1 units; the Level-1/Level-2 folder separation is explicit; the
  driver↔`tasks.md` authority split is written down. A negative ergonomics finding here is **first-class
  feedback on DEC1** — record it, don't suppress it.

### Milestone 1 · Part A — author schema, templates & config (documentation/config-only)

**- [ ] M1-A0 · Reversible smoke test — `config.yaml` on the default schema (no schema authoring)**
- **Files:** a throwaway `openspec/config.yaml` (+ `openspec init` in a scratch dir, or the repo if safe).
- **Change:** write only `schema: spec-driven` + a tight guardrail `context:` digest + one `rules:` entry,
  run `/opsx:propose` on a trivial idea, confirm the `<context>`/`<rules>` injection lands in the produced
  artifact. Prove the §5 mechanism end-to-end before committing to the full schema.
- **POST:** an `openspec` change was produced whose generation visibly honoured the injected context/rules;
  no custom schema authored yet; scratch artifacts discardable.

**- [ ] M1-A1 · Scaffold the Basic schema by forking `spec-driven`**
- **Files:** `openspec/schemas/<spine-name>/schema.yaml` + `templates/` (via `openspec schema fork spec-driven <spine-name>`).
- **Change:** fork, then lay down the **Basic node skeleton** — the 10 nodes above (incl. the `specs` delta-spec node, D-DEC4), `requires` per §3, and
  the `apply:` block tracking `tasks.md`. **No `prd` node.** Node `id`s, `generates`, `requires` only
  (instructions/templates filled by M1-A2/A3). Keep the schema name and every node body **generic**
  (`skills/CLAUDE.md`); no ai-mail term. Run `openspec schema validate`.
- **Idempotent:** if the schema folder exists, verify it matches §3 rather than re-forking.
- **POST:** `openspec schema validate <spine-name>` passes; node set = the 10 Basic nodes (no prd/tracker
  nodes); `requires` edges match §3; no project-specific identifiers.

**- [ ] M1-A2 · Fill each authoring node's `instruction` from its SKILL.md (+ composed-lens lines)**
- **Files:** `openspec/schemas/<spine-name>/schema.yaml`.
- **Change:** for each authoring node, distill the matching SKILL.md's *process + POST self-check* into the
  node `instruction`, and append the composed-lens invocation line (§4 option 1: language-guard,
  scope-cut, adr-gate, constraint-sweep as the node calls for). Generic; project values via `config.yaml`.
  Carry stable IDs per D-DEC3. **The `specs` node has no 1:1 SKILL.md** — its `instruction` is the
  FR + use-case-scenario → delta-spec projection (D-DEC4): one `### Requirement: FR-### — <name>` per
  in-scope FR, `#### Scenario` blocks from the use-case flows, IDs carried into the headings.
- **POST:** every authoring node's `instruction` is traceable to its SKILL.md; lens invocations present
  where the SKILL.md composed them; no project specifics.

**- [ ] M1-A3 · Author the `templates/*.md`**
- **Files:** `openspec/schemas/<spine-name>/templates/*.md` (one per node).
- **Change:** transcribe each artifact's output skeleton (vision, FR/NFR/C/OOS tables, entity-table
  layout, PlantUML skeleton, use-case-spec layout, testing-entry layout, tasks checklist) into a template
  with HTML-comment guidance, **carrying stable-ID placeholders** per D-DEC3. For the behaviour-contract
  layer, use OpenSpec's `### Requirement:`/`#### Scenario:` shape per D-DEC4.
- **POST:** one template per node; ID placeholders present; behaviour-contract templates use the
  Requirement/Scenario shape; generic.

**- [ ] M1-A4 · Write `config.yaml` — guardrail `context` + per-artifact `rules`**
- **Files:** `openspec/config.yaml`.
- **Change:** distill the always-on gr discipline into a ≤50 KB `context:` digest; transpose each
  `skills_overview.md` "Relation to guardrail items" list into `rules:` keyed by the node `id` (§5).
- **POST:** `context` under cap; every `rules:` key is a real Basic-node `id` (`openspec schemas --json`
  clean); rule lists trace to the overview.

**- [ ] M1-A5 · Add the `review` (verify-style) fail-closed gate node**
- **Files:** `schema.yaml` (`review` node) + `templates/review.md`.
- **Change:** add a `review` node `requires: [specs, use-cases-spec, entity-model]` whose `instruction` runs
  `trace-check`'s Check 0 + A–D and the fail-closed FR↔UC coverage, emitting a PASS/PARTIAL/BREAKS report
  (model on `verify-change.ts` structure, but artifact-internal). This is where the §9.1 rigor lost to
  "no gates" is re-introduced.
- **POST:** `review` node validates; its instruction enumerates Check 0/A–D + FR↔UC coverage; fail-closed
  wording present; generic.

**- [ ] M1-A6 · Keep/adapt the `tasks` node + `apply:` block (Pure-mode execution)**
- **Files:** `schema.yaml` (`tasks` node + `apply:`), `templates/tasks.md`.
- **Change:** the `tasks` node (`requires: [use-cases-spec, testing]`) generates the implementation
  checklist **directly from the spine** — this replaces the tracker projection in Pure mode. Confirm
  `apply.tracks: tasks.md`; reference the `tdd` skill's discipline from the `apply` instruction.
- **POST:** `tasks` node + `apply:` validate; tasks derive from the spine; `/opsx:apply` can track them.

**- [ ] M1-A7 · Author OpenSpecEngine's own workflow / overview / mapping docs (Basic scope)**
- **Files (created in OpenSpecEngine):** `OpenSpecEngine/docs/workflow.md`, `…/skills_overview.md`,
  `…/artifacts.md` (or one combined mapping doc). **ai-mail is read-only — do NOT edit its skillfactory docs.**
- **Change:** author OpenSpecEngine docs that (a) name `schema.yaml` the authoritative sequence (D-DEC1),
  (b) map each ai-mail authoring skill (read-only source) → its OpenSpec node `id` and each lens → its
  composed/`review` role, and (c) record the `docs/* → openspec/changes/<change>/ → openspec/specs/`
  location mapping (Basic). Reference the ai-mail originals read-only; the "retired" status of ai-mail's
  `workflow.md` is *noted here*, not by editing it.
- **POST:** OpenSpecEngine carries its own workflow/overview/mapping docs; `schema.yaml` is named the
  authoritative sequence; ai-mail untouched.

### Milestone 1 · Part B — wire & validate (runs the CLI)

**- [ ] M1-B1 · End-to-end dry run + archive on a throwaway change**
- **Change:** `openspec schema validate`, then drive `/opsx:new` → `/opsx:continue` through the full DAG
  on a trivial scratch idea (each node reads its `dependencies`, honours `context`/`rules`); confirm the
  `review` node **blocks on a seeded coverage gap**; run `/opsx:apply` over `tasks.md`; run `/opsx:archive`
  and confirm the delta specs merge into `openspec/specs/`. Discard the scratch change.
- **POST:** every node creatable in order; `review` demonstrably fail-closed on a planted gap; archive
  merges deltas → `openspec/specs/`; no schema errors. **This is the gate Milestone 2 depends on.**

**- [ ] M1-B2 · Bridge `declare-milestone` ↔ change creation + the N+1 delta loop (no tracker)**
- **Change:** document how `declare-milestone` maps to `/opsx:new <change>` + `.openspec.yaml` metadata
  (committed `F`-set + predecessor), and how milestone N+1 opens a **delta** change against accumulated
  `openspec/specs/` with `archive` merging it. No GitHub hand-off in Basic.
- **POST:** a written milestone↔change bridge exists; N+1 delta loop described; `declare-milestone`'s
  selection logic preserved (only its output location moved).

---

## Milestone 2 — Full (Hybrid: + GitHub execution bridge)

**Goal.** Layer the GitHub tracker on the **proven** Basic spine, restoring the AFK-agent issue loop.
Adds the `prd` projection (`spec-to-prd`), `to-issues`, `triage`, and `tracker-trace-check`. "Done" is
**two-staged**: issues close on the tracker **and** the change archives into `openspec/specs/`.
**Prerequisite:** Milestone 1 complete and proven (M1-B1).
**Method (per work-type):** Part A bridge authoring = **free-style in cold sub-agents**; Part B Hybrid dry-run =
**OpenSpec CLI + the GitHub bridge skills** (`spec-to-prd`/`to-issues`/`tracker-trace-check`, unchanged). See
[Execution method per work-type](#execution-method-per-work-type).

### Milestone 2 · Part A — add the bridge (documentation/config-only)

**- [ ] M2-A1 · Add the `prd` node (the `spec-to-prd` projection)**
- **Files:** `schema.yaml` (`prd` node) + `templates/prd.md`.
- **Change:** add `prd` `requires: [requirements, use-cases-spec, testing]` whose `instruction` is
  `spec-to-prd`'s projection — **links** the spine's `FR/UC/BR/ADR` IDs (restates no content; Doc5),
  authors fresh only the module + testing-decisions sections, publishes to the tracker reached abstractly
  via `docs/agents/issue-tracker.md`. Generic; tracker specifics never hard-coded.
- **POST:** `prd` node validates; instruction links IDs (no spine duplication); tracker reached abstractly.

**- [ ] M2-A2 · Wire `to-issues` as the post-`prd` step**
- **Files:** `schema.yaml` (terminal note / `apply` variant) + docs.
- **Change:** record that in Full mode the PRD is broken into tracer-bullet vertical-slice issues by the
  external `to-issues` skill. Decide and document whether this **supersedes** or **runs alongside** the
  Pure-mode `tasks` → `/opsx:apply` path, so there is one authoritative execution surface.
- **POST:** the `prd → to-issues → implement` path is documented; the Pure-mode `tasks` path's status in
  Full mode is stated explicitly (kept / superseded).

**- [ ] M2-A3 · Re-point `tracker-trace-check` at `openspec/specs ↔ GitHub`**
- **Files:** the inputs `tracker-trace-check` resolves (via its fallback chains — no hard paths).
- **Change:** the authoritative in-repo side is now `openspec/specs/` (+ the change folder), not `docs/`;
  the tracker side is the published PRD/issues. Confirm its convention-discovery still derives the ID
  families; run dangling-ref + forward-coverage + semantic-divergence.
- **POST:** `tracker-trace-check` resolves references against `openspec/specs/`; forward-coverage runs at
  the milestone marker; no hard-coded paths introduced.

**- [ ] M2-A4 · Confirm/keep the triage + issue-tracker wiring**
- **Files:** `docs/agents/{issue-tracker,triage-labels}.md` (read), docs.
- **Change:** verify the issue-tracker abstraction and the `ready-for-agent` / triage label vocabulary are
  still valid against the OpenSpec spine; the `triage` skill is unchanged.
- **POST:** tracker + triage wiring confirmed against the OpenSpec spine; no changes needed beyond docs, or
  the needed changes are listed.

**- [ ] M2-A5 · Update `config.yaml` + docs for Full/Hybrid**
- **Files:** `openspec/config.yaml`, `skills/{workflow,skills_overview,artifacts}.md`.
- **Change:** record the **two "done" surfaces**, the `milestone ≡ change ≡ (optional) GitHub-native
  Milestone` mapping (`milestone_review.md` §6), and the Full node set (adds `prd`). Switch the active
  config to Full.
- **POST:** docs describe the two-staged done + the milestone/change/GitHub-Milestone mapping; `prd` node
  present in the Full schema; `rules:` keys still valid.

**- [ ] M2-A6 · Make the fail-closed `review` gate engine-enforced (ADR-0001 deferred hook)**
> Added at M1-P0 ratification of ADR-0001 (grill 2026-06-10). M1 ships the `review` node as
> *honest-discipline* — "fail-closed" is instruction wording only, since OpenSpec treats dependencies as
> "enablers, not gates" and will not block `/opsx:archive` on a failed review. This unit hardens that for the
> product spine, where (unlike the build, DEC6) there is no cold-sub-agent driver enforcing POST-pass.
- **Files:** an archive-time enforcement mechanism — a git pre-commit/pre-push hook, a CI step, or an
  `openspec validate` extension (decide which during the unit; keep it generic — no project paths).
- **Change:** add a real blocker so a `review.md` reporting `BREAKS FOUND (N)` or any uncovered in-scope FR
  **prevents** `/opsx:archive` (or fails the merge), converting the §9.1 rigor from instruction wording into
  an actual gate. Generic; the check reads the `review` node's PASS/PARTIAL/BREAKS result, not a hard-coded
  path. Do **not** weaken OpenSpec's "enablers, not gates" default for *ordering* — this gate is the single
  quality exception, applied only at archive.
- **POST:** a seeded failing `review` demonstrably blocks archive/merge; a passing one does not; the gate is
  generic and documented as the engine-enforced counterpart to the M1 honest-discipline `review` node;
  ADR-0001's deferred-hook consequence is satisfied.

### Milestone 2 · Part B — wire & validate

**- [ ] M2-B1 · End-to-end Hybrid dry run**
- **Change:** on a throwaway milestone, drive the spine → `prd` published → `to-issues` → run
  `tracker-trace-check`; confirm **forward coverage PASS** (every in-scope FR reached the tracker) and no
  dangling refs.
- **POST:** spine→PRD→issues path works; `tracker-trace-check` PASS (or its breaks are understood);
  scratch discarded.

**- [ ] M2-B2 · Document the two-staged "done" + milestone/GitHub-Milestone mapping**
- **Change:** write when issues close vs when the change archives, and how `tracker-trace-check` reconciles
  the tracker against `openspec/specs/` across the boundary.
- **POST:** a written "done" definition exists for Full mode; the reconciliation path is documented.

---

## Appendix · Quick mapping card

```
ai-mail                                   OpenSpec 1.4.1
─────────────────────────────────────     ─────────────────────────────────────
workflow.md (the sequence)            →    schema.yaml artifacts DAG
create_skills.md orchestration        →    openspec status/instructions/continue (CLI)
declare-milestone                     →    /opsx:new <change> + .openspec.yaml   (milestone ≡ change)
vision / requirements / entity-model  →    artifact nodes (instruction + template + requires)
  / use-cases / testing
FR/UC scenarios (behaviour contract)  →    openspec/specs/<cap>/spec.md  (### Requirement / #### Scenario)
milestone N+1                         →    delta change (ADDED/MODIFIED/REMOVED) + archive→specs
lenses (language/scope/adr/sweep)     →    composed portable skills (referenced from instructions)
trace-check (coverage/traceability)   →    a `review` (verify-style) artifact node
gr_*.md guardrails                    →    config.yaml: context (all) + rules (per-artifact)
spec-to-prd / to-issues / tdd         →    M1 Basic: tasks.md + /opsx:apply (pure) · M2 Full: + GitHub bridge
review-skills / refactor-skills       →    OUT OF SCOPE — unchanged; still run on the remaining lens SKILL.md
```

---

## Appendix B · Concrete M1 nodes (illustrative — DEC3 IDs + DEC4 deltas)

Build reference for `M1-A2` / `M1-A3`. **Generic** — project specifics arrive via `config.yaml`, never the
schema. Not final wording.

**`requirements` node** — DEC3: stable IDs in the catalog.

```yaml
- id: requirements
  generates: requirements.md
  template: requirements.md
  instruction: |
    Author the catalog from vision + glossary (both deps). Four non-mixed tables:
    FR (user story), NFR (measurable), Constraints, Out-of-Scope.
    Every row: a STABLE UNIQUE ID (FR-###/NFR-###/C-###/OOS-###) + a Status.        # DEC3
    Glossary terms VERBATIM; actors from glossary actor terms (L1). Flag — never
    coin — new terms (L6). Carry vision non-goals into Out-of-Scope (Aln15).
    AFTER writing run: ubiquitous-language-guard, pareto-scope-cut, hidden-constraint-sweep.
  requires: [vision, glossary]
```

**`specs` node** — DEC4: this node *existing* is the decision; the accreting behaviour contract.

```yaml
- id: specs
  generates: "specs/**/*.md"        # change-folder deltas → merge to openspec/specs/ on archive
  template: spec.md
  instruction: |
    Project IN-SCOPE FRs + their use-case scenarios into one delta spec per capability
    (specs/<capability>/spec.md). Under "## ADDED Requirements", per in-scope FR:
      ### Requirement: FR-### — <name>          # DEC3 (ID in heading)
      <normative SHALL/MUST contract>
      #### Scenario: <name>                      # from use-case main + alt flows
      - WHEN <condition>
      - THEN <outcome>
    Carry FR/UC/BR IDs into headings so trace-check resolves them. On /opsx:archive these
    merge into openspec/specs/, so milestone N+1 emits ADDED/MODIFIED/REMOVED (DEC4).
  requires: [use-cases-spec, entity-model]
```

**`review` node** — the fail-closed gate (§4 option 2).

```yaml
- id: review
  generates: review.md
  template: review.md
  instruction: |
    Run trace-check Check 0 + Checks A–D over this change's spine, PLUS fail-closed FR↔UC
    coverage (every in-scope FR realised by >=1 UC AND cited by >=1 use-case spec; every UC
    traces to >=1 FR). Emit: Result: PASS | PARTIAL | BREAKS FOUND (N).
    A BREAK or any uncovered in-scope FR is FAIL-CLOSED — do NOT mark done; route the fix and
    re-run. Never "document a gap" and pass.
  requires: [specs, use-cases-spec, entity-model]
```

**`templates/requirements.md`** — DEC3 visible in the table.

```markdown
<!-- Source: <vision path> + <glossary path> -->
## Functional Requirements
| ID | Requirement (As a <role>, I want <goal> so that <benefit>) | Priority | Status |
|--------|------|------|------|
| FR-001 | <user story; role verbatim from glossary> | <P> | Open |
## Out-of-Scope / Non-Goals
| ID | Non-goal | Source |
|--------|------|------|
| OOS-001 | <deferred/rejected item> | vision non-goals |
```

**`config.yaml` rules** — DEC3/DEC4 as passive reminders (complement the lenses, §5).

```yaml
rules:
  requirements:
    - "Every FR/NFR/C/OOS row has a stable unique ID and a filled Status"            # DEC3
    - "Glossary terms verbatim; flag (never coin) new terms (L1/L6)"
  specs:
    - "### Requirement: FR-### — <name>, normative SHALL/MUST; >=1 #### Scenario each" # DEC3+DEC4
    - "Carry FR/UC/BR IDs into headings so trace-check resolves them"
  review:
    - "Fail-closed: a BREAK or uncovered in-scope FR blocks 'done'"
```
