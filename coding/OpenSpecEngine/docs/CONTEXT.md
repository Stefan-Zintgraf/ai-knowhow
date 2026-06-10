# OpenSpecEngine — Ubiquitous Language

The shared vocabulary for migrating the ai-mail authoring skillset onto OpenSpec 1.4.1. Built
incrementally during the M1-P0 ADR grills (one ADR per session). Terms here are canonical: schema
nodes, templates, `config.yaml`, and skills must use them verbatim. This is a glossary only — no
implementation detail, no decisions (those live in `docs/adr/`).

## Language

### The engine (OpenSpec, Level 2)

**OpenSpec**:
The npm CLI + generated thin skill layer this project hosts the authoring chain on. Not a framework
you import — a state machine over a schema.
_Avoid_: framework, library

**OPSX**:
OpenSpec's current workflow mode (the `/opsx:*` commands). Moves the workflow out of TypeScript into
editable YAML + Markdown. The seam the migration plugs into.

**Schema**:
The YAML file (`schema.yaml`) defining the whole workflow as a DAG of nodes. Project-agnostic and
forkable. The migration's deliverable is a custom schema (working name **spine**).
_Avoid_: workflow definition, config

**Node** (= **artifact** node):
One vertex of the schema DAG: `{id, generates, template, instruction, requires}`. Authoring a node
*creates one artifact file*. "Node" = the schema definition; "artifact" = the file it generates.
_Avoid_: step, stage, task (those are ai-mail-era words for the same thing)

**Artifact**:
The file a node generates (e.g. `requirements.md`). Has status `ready` / `blocked` / `done` per its
`requires` edges.

**EXPANDED profile**:
The OPSX mode where `/opsx:continue` creates exactly **one** artifact per invocation and STOPs, vs
core `/opsx:propose` which generates the whole spine in one shot. DEC1 enables EXPANDED so a human
stop point exists at every DAG edge.
_Avoid_: continue-mode, step mode

**Orchestrator**:
The single authoritative source of "what's next." Post-DEC1 this is `schema.yaml` + the OpenSpec CLI,
**replacing** ai-mail's hand-written `workflow.md`. There must be exactly one.

### The authoring chain (Level 1)

**Spine**:
The authoring chain itself — the ordered set of nodes (`vision → glossary → requirements → … →
tasks`) that produces a milestone's planning artifacts. The custom schema *is* the spine.
_Avoid_: pipeline, chain (informal only)

**Lens**:
A step-agnostic, cross-cutting check that runs on many artifacts (language-guard, scope-cut,
adr-gate, constraint-sweep, trace-check). Has no native OpenSpec slot; kept as a portable skill
referenced from node `instruction`s.
_Avoid_: gate (a lens is not necessarily fail-closed), validator

**Driver**:
The orchestrating session that runs one cold sub-agent per unit, strictly sequentially, flipping a
checkbox only after that unit's POST self-check passes. Fail-closed by construction. DEC6 keeps the
driver for the build's Part A.

### Milestones & changes

**Milestone**:
A sequenced Pareto slice of the migration — the in-scope capability one planning loop ships. Milestones
form an **open-ended series** (M1, M2, M3…), not a fixed count: M1 is the smallest proven slice (the Pure
in-repo spine); each later milestone adds capability deferred from the smaller slice. The spine accretes
via delta-specs and never forks (ADR-0002). ≡ **change**.
_Avoid_: phase, release, sprint

**Change**:
The OpenSpec unit a milestone maps to: a self-contained `openspec/changes/<change>/` folder.
`/opsx:archive` merges its delta-specs into `openspec/specs/`. `milestone ≡ change` is the conceptual
bridge (§6); opening a new change for milestone N+1 is what lets the spec accrete instead of re-running
the chain.
_Avoid_: PR, ticket, issue

### Requirements & traceability

**Stable ID**:
A `FR/NFR/C/UC/BR/ADR-###` identifier that is the **permanent identity** of a requirement (or use case,
business rule, decision): assigned once, **never reused** for the project's lifetime, carried verbatim
into artifacts. Traceability and the lenses key on it. Per ADR-0003 the `### Requirement:` heading **is**
the bare `FR-###` (the human name lives in the body), so the ID is OpenSpec's delta match key.
_Avoid_: name, slug, requirement title (those are the mutable label, not the identity)

**Delta-spec**:
A change-folder `specs/<capability>/spec.md` file written as `## ADDED / MODIFIED / REMOVED / RENAMED
Requirements` operations against the accumulated `openspec/specs/`. `/opsx:archive` merges it, so the
source of truth accretes instead of being re-authored. The `specs` node generates these (ADR-0004).
OpenSpec matches each delta to an existing requirement by the **whole heading string** — which is why
ADR-0003 makes that heading the stable ID.
_Avoid_: spec delta, diff-spec

### Rigor & gating

**Fail-closed gate**:
A check that **blocks** progress until it passes (no "document the gap and move on"). In M1 the
`review` node is fail-closed *as discipline only* — its instruction says block, but OpenSpec
("enablers, not gates") will not enforce it. Engine-enforcement is deferred to M2-A6 (ADR-0001).
_Avoid_: validation, soft gate (a soft review is a *stop*, not a gate)

**`review` node**:
The one schema node modelled on OpenSpec's `verify` workflow that hosts `trace-check` + fail-closed
FR↔UC coverage, emitting PASS / PARTIAL / BREAKS. Re-introduces the rigor OpenSpec's "no gates"
philosophy drops — see fail-closed gate for its M1 limit.

## Example dialogue

> **Dev:** Can I just `/opsx:propose` the whole spine and review at the end?
> **Architect:** No — DEC1 runs the **EXPANDED profile**, so you `/opsx:continue` one **node** at a
> time and it STOPs. The stop *is* the review point.
> **Dev:** And the `review` node blocks me if coverage breaks?
> **Architect:** In M1 only by **discipline** — it's a **fail-closed gate** in wording, but OpenSpec
> won't physically stop your `/opsx:archive`. The engine-enforced blocker is M2-A6.
> **Dev:** So what does the engine actually enforce in M1?
> **Architect:** Ordering. `requires` makes a node `blocked` until its deps are `done`. That's the one
> thing the **orchestrator** guarantees; everything else is the **driver**'s job or your own.
