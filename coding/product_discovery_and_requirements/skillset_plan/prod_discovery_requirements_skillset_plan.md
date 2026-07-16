# Skillset Plan: The Discovery–Definition–Requirements Loop

**Status:** First draft — for discussion

**Revision contract:** Before this plan advances beyond draft, apply the ordered edits and pass the contribution-coverage gate in the [skillset plan revision contract](./skillset_plan_update_plan.md) (derived from the [GitHub skillsets fit analysis](./github_skillsets.md)). The seven per-skill contribution ledgers beside that analysis are part of the acceptance evidence.

## 1. Goal

Build a skillset/workflow that implements the **discovery–definition–requirements loop** from the [overview](../overview.md) as agent skills, extending the two existing vision-stage skills:

- [`brainstorm-vision`](../../../skills-plugins/brainstorm-vision/SKILL.md) — divergent vision brainstorm → `*-foundation-vision.md` (the slow-changing anchor)
- [`create-vision-companion`](../../../skills-plugins/create-vision-companion/SKILL.md) — frozen vision → derived companion bundle (`*-vision-ai-spec/`: actors, glossary, invariants, capability map, UC/vision indexes)

Today the lifecycle's top box is covered; the fast loop underneath is not. The skillset adds the loop stages — **product discovery**, **product definition**, **requirements engineering** — plus the **lifecycle tailoring** entry step and the **validation** re-entry, wired together by the companion bundle's stable ID scheme.

### Design principles

1. **Two skill modes, chosen per stage.** *Interview skills* (the `brainstorm-vision` / `grill-me` pattern) where the human supplies knowledge the agent cannot have — evidence, priorities, business judgment. *AFK derive skills* (the `create-vision-companion` pattern: orchestrator + builder/critic sub-agents, `decisions.md`, human reviews at the end) where the work is restructuring already-captured content. Discovery and definition are interview-heavy; specification and index maintenance are derive-heavy.
2. **The companion bundle stays derived-only.** Loop artifacts are *not* derivable from the frozen vision (they add evidence and commitments), so they live in a separate **loop workspace**, citing companion IDs. The `*-vision-ai-spec/` bundle is never extended with loop content.
3. **One traceability spine, extended.** The companion's IDs (`S#`, `V#`, `UC#`, `BV#`, `INV#`, `CAP#`) are the anchor. The loop adds its own ID families (below) and every loop artifact cites upward: opportunity → outcome/vision, capability-in-scope → opportunity + evidence, requirement → capability/UC.
4. **Reuse existing skills as loop steps.** `prototype` (discovery's "test cheaply"), `domain-modeling` (domain discovery), `grill-with-docs` (requirements validation), `qa` / `triage` (validation intake). The new skills orchestrate around them, not replace them. Skills that belong to later phases (design, implementation planning) are *not* part of this skillset — see §6.
5. **Ceremony is tailored, not fixed.** The tailoring step decides which loop skills a topic actually runs; skills must degrade gracefully to a low-ceremony solo-developer setting ([minimum useful discovery package](../overview.md#minimum-useful-discovery-package)).
6. **The method docs in the parent folder are the skills' source material — all of them.** Each skill *must* consume its stage doc(s): templates become the skill's output shapes, completion checks become its finalize gates, failure modes become its guardrails. §2.1 maps every method document in the parent folder to its consuming skill so nothing is orphaned. (Mechanism — distill into skill sub-files at authoring time with a source pointer, vs. read the docs live at runtime — is an open question, §7.)
7. **No artifact may share a name with a method doc.** The method docs in the parent folder describe *how to do the work*; the artifacts (product repo, `docs/product/<topic>/`) record *the work done for one product*. Identical filenames invite confusion, so artifact names must differ from every method-doc name. The one existing collision — the companion bundle's `glossary.md` vs. the method [glossary.md](../glossary.md) — is resolved by renaming the artifact to `domain-glossary.md` (part of the `create-vision-companion` adjustments, §5.2).

## 2. Artifacts

The loop workspace lives parallel to the vision, e.g. `docs/product/` (name open — see §6). Proposed starter set, mapped to the collection's stage documents:

| Artifact (product repo) | Method doc it follows (parent folder) | ID family | Produced / maintained by |
| --- | --- | --- | --- |
| `lifecycle-onepager.md` — entry point, stages in use, cadence, decision authority | [Lifecycle tailoring](../lifecycle_tailoring.md) | — | `tailor-lifecycle` (new) |
| `<product>-foundation-vision.md` | [Product vision](../product_vision.md) | `S`, `V`, `UC`, `BV` | `brainstorm-vision` (existing, adjust) |
| `<product>-vision-ai-spec/` bundle | [Product vision](../product_vision.md) | `INV`, `CAP` | `create-vision-companion` (existing, adjust) |
| `assumptions.md` — assumption map ranked by importance × evidence, with the four risk classes (value/usability/feasibility/viability) | [Product discovery](../product_discovery.md) | `ASM#` | `discover-product` (new) |
| `evidence-log.md` — observations, interview notes, analytics pointers, each dated with strength | [Product discovery](../product_discovery.md) | `EV#` | `discover-product` (new) |
| `opportunities.md` — opportunity map under the framed outcome, separate from solutions | [Product discovery](../product_discovery.md) | `OPP#` | `discover-product` (new) |
| `experiments/EXP<n>.md` — experiment cards (decision, assumption, method, criteria, result) | [Product discovery](../product_discovery.md) | `EXP#` | `discover-product` (new), executing via `prototype` where applicable |
| `releases/REL<n>-definition.md` — definition one-pager: opportunities addressed/deferred, capabilities in scope, hypothesis, success/guardrail/stop criteria | [Product definition](../product_definition.md) | `REL#` | `define-release` (new) |
| `releases/REL<n>-requirements.md` — use cases (elaborated, with failure paths), functional requirements, interface/data/transition requirements for the committed slice | [Requirements engineering](../requirements_engineering.md), [Use cases](../use_cases_and_story_mapping.md) | `REQ#`, elaborated `UC#` | `specify-requirements` (new) |
| `quality-scenarios.md` — measurable quality-attribute scenarios; architecture-significant ones flagged | [Quality attributes](../quality_attributes.md) | `QAS#` | `specify-requirements` (new); seeded from the brainstorm's `*-architecture-lens.md` |
| `decision-log.md` — consequential choices with evidence and strength; the loop's shared memory | all stages | `DEC#` | every skill appends; owned by none |
| `validation/REL<n>-review.md` — outcome vs. success/guardrail criteria; what to reopen | [Validation and feedback](../validation_and_feedback.md) | — | `validate-release` (new) |

Domain-discovery artifacts (glossary, rules, context boundaries) are deliberately **not** duplicated here: the companion's `domain-glossary.md` (renamed from `glossary.md`, §5.2) + the repo's `CONTEXT.md`/ADRs (via `domain-modeling`) remain canonical, and loop skills consult/extend those.

### 2.1 Method-doc coverage

Every method document in the parent folder must be consumed by at least one skill (design principle 6). The mapping — and *what* of each doc the skill uses:

| Method doc | Consumed by | What the skill takes from it |
| --- | --- | --- |
| [overview.md](../overview.md) | `tailor-lifecycle` | The lifecycle model, the pragmatic workflow, the minimum useful discovery package, the readiness-for-design checklist (the loop's exit criterion) |
| [lifecycle_tailoring.md](../lifecycle_tailoring.md) | `tailor-lifecycle` | Entry-point classification, ceremony drivers, stage/artifact selection, cadence models, decision-authority table, one-pager template |
| [collaboration_and_decision_ownership.md](../collaboration_and_decision_ownership.md) | all skills | One named accountable owner per consequential decision; required contributors and specialist authorities; cross-functional participation; architecture-overlap, escalation, and reopening rules |
| [product_vision.md](../product_vision.md) | `brainstorm-vision` (adjust), `define-release` | Vision template sections → the finalize stubs (§5.1); **completion checks → the finalize gate**; scope-boundaries section → `define-release`'s scope check |
| [product_discovery.md](../product_discovery.md) | `discover-product` | The 7-step discovery loop as phase structure, four risk classes, experiment-card template, failure modes → guardrails, completion checks → wrap-up gate |
| [product_definition.md](../product_definition.md) | `define-release` | The 7 core activities as phase structure, one-pager template → `REL<n>-definition.md`, prioritization criteria, failure modes → guardrails, completion checks → gate |
| [requirements_engineering.md](../requirements_engineering.md) | `specify-requirements` | Requirement types, core process, requirement sentence form, traceability model, change policy, completion checks → gate |
| [use_cases_and_story_mapping.md](../use_cases_and_story_mapping.md) | `define-release` (journey shaping), `specify-requirements` (UC elaboration) | Story-map structure, use-case format with alternative/failure paths |
| [domain_discovery.md](../domain_discovery.md) | `discover-product`, `specify-requirements` (both via `domain-modeling`) | When to trigger domain work; what the canonical domain artifacts are |
| [quality_attributes.md](../quality_attributes.md) | `discover-product` (early QA risk surfacing), `specify-requirements` (measurable `QAS` scenarios) | Scenario format, "quality attributes start early" rule |
| [validation_and_feedback.md](../validation_and_feedback.md) | `validate-release` | Review cadence, outcome/guardrail measures, the reopen decision table |
| [glossary.md](../glossary.md) | all skills | The method terminology every skill's prose and prompts must use consistently (distinct from the product's `domain-glossary.md`) |
| [resources.md](../resources.md) | `tailor-lifecycle`, `discover-product` | The practical technique index (uncertainty → technique) for recommending methods |
| this plan | — | Meta: not consumed by skills |

## 3. Skills overview

| Skill | Status | Mode | Stage |
| --- | --- | --- | --- |
| `tailor-lifecycle` | **new** | interview (short) | Lifecycle tailoring — entry point, ceremony, cadence, which skills below run |
| `brainstorm-vision` | existing — **adjust** | interview | Product vision (divergence) |
| `create-vision-companion` | existing — **adjust** | AFK derive | Vision → structured spine |
| `discover-product` | **new** | interview + light derive | Product discovery — outcome framing, evidence capture, opportunity/assumption mapping, experiment cards |
| `define-release` | **new** | interview | Product definition — select, scope, prioritize, cut a release with a hypothesis |
| `specify-requirements` | **new** | AFK derive + review gate | Requirements engineering — use cases, requirements, quality scenarios for the committed slice |
| `validate-release` | **new** | interview (short) | Validation and feedback — measure against criteria, decide what to reopen |
| `prototype` | existing — **reuse as-is** | interview + build | Discovery's "test cheaply" step (state-model branch only; the UI branch belongs to design) |
| `domain-modeling` | existing — **reuse as-is** | interview | Domain discovery (a stage of this collection); also serves the later design skillset |
| `grill-with-docs` | existing — **reuse as-is** | interview | Requirements validation — stress-test the specified slice against the domain docs |
| `qa` / `triage` | existing — **reuse as-is** | interview / AFK | Validation intake — post-release evidence arriving as issues |

## 4. The loop — sequence and re-entry

```text
tailor-lifecycle  ──────────────  once per topic; picks entry point + which stages run
      │
      ▼  (greenfield entry only)
brainstorm-vision ──► create-vision-companion        [vision anchor + spine]
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│  THE LOOP (cadence per lifecycle.md)                        │
│                                                             │
│  discover-product                                           │
│    frame outcome → capture evidence → map OPP/ASM           │
│    → test riskiest ASM cheaply (may call `prototype`)       │
│    → DEC: proceed / adapt / pause / abandon                 │
│      │                                                      │
│      ▼                                                      │
│  define-release                                             │
│    select OPPs → capabilities in scope (CAP language)       │
│    → REL one-pager with hypothesis + stop criteria          │
│    → scope check against vision S-ladder                    │
│      │  (scope fights the vision → re-open brainstorm-vision)│
│      ▼                                                      │
│  specify-requirements                                       │
│    elaborate UCs (failure paths) → REQ set → QAS scenarios  │
│    → may call domain-modeling / grill-with-docs             │
└──────┬──────────────────────────────────────────────────────┘
       │  coherent slice, success + stop criteria
       ▼
  ── end of this skillset ──
  (design → implementation → release: future skillsets, not yet fixed — see §6)
       │
       ▼
  validate-release   (evidence may arrive via qa / triage)
       ↺  reopens: vision (rare) / opportunities / scope / requirements
          — re-enter the loop at the reopened artifact, per tailoring
```

The loop's exit criterion is the [readiness-for-design checklist](../overview.md#readiness-for-software-design): the skillset is done with a topic when those questions are answerable. What happens next (design, implementation) is outside this plan; `validate-release` re-enters from post-release evidence whenever it arrives.

Entry points other than greenfield (per [lifecycle tailoring](../lifecycle_tailoring.md)) skip forward: *new capability* enters at `discover-product`; *rework* enters at `validate-release` evidence; *compliance mandate* enters at `specify-requirements` with the mandate as a constraint; *fast-follow* enters at `define-release`.

## 5. Per-skill sections

### 5.1 `brainstorm-vision` (adjust)

Small, targeted changes only — the skill's divergent core is untouched:

The skill's output file stays `<slug>-foundation-vision.md` — it never creates a file named after the method doc.

- **Emit visible gaps at finalize.** The finalized vision should end with stub sections for what the brainstorm deliberately does not elicit — *product principles*, *outcomes and signals*, *critical assumptions* — so the completion checks of the [product_vision.md method doc](../product_vision.md) fail loudly, not silently. `discover-product` picks the assumptions stub up as its seed.
- **Adopt the method doc's completion checks as the finalize gate.** The skill's finalize phase runs the six checks from [product_vision.md](../product_vision.md); sections the brainstorm doesn't cover are marked as open stubs (above), not silently passed.
- **Tailoring pointer.** One line at session start: for non-greenfield topics, suggest `tailor-lifecycle` first (an existing vision may just need extending, not a new session).
- **Optional principles micro-phase.** Consider a short convergent add-on after the ladder closes: harvest recurring trade-offs from the session into 3–5 product principles. (Open question — may instead belong in `discover-product` or the companion. See §7.)

### 5.2 `create-vision-companion` (adjust)

- **Expose discovery seeds.** The bundle already computes discovery-relevant signals — *unpromised UCs*, coverage gaps in `vision-index.md`, low-confidence `decisions.md` rows. Add a small derived file (e.g. `discovery-seeds.md`) that lists them explicitly as candidate `OPP`/`ASM` inputs, so `discover-product` starts from the spine instead of re-reading the bundle.
- **Reserve the loop's ID families** (`ASM`, `EV`, `OPP`, `EXP`, `REL`, `REQ`, `QAS`, `DEC`) in the Phase 0 ID inventory so no collision arises later.
- **Rename the bundle's `glossary.md` → `domain-glossary.md`** (naming rule, design principle 7): the artifact is the *product's* ubiquitous language, distinct from the method terms in [glossary.md](../glossary.md).
- Otherwise unchanged — in particular the derived-only principle: **no loop artifacts inside the bundle**.

### 5.3 `tailor-lifecycle` (new)

- **Mode:** short interview (10–15 questions max); output is one file.
- **Does:** classify the topic (greenfield / new capability / rework / mandate / fast-follow / platform), size ceremony per driver, select which loop skills and artifacts this topic uses, set cadence and decision owners. Writes `lifecycle-onepager.md` from the [one-pager template](../lifecycle_tailoring.md#lifecycle-one-pager-template).
- **Key behavior:** for a solo/low-ceremony topic it should recommend the *minimum* package and explicitly record skipped stages with reasons ("a silent skip is a blind spot"). Other loop skills read `lifecycle-onepager.md` at start and respect it.

### 5.4 `discover-product` (new)

- **Mode:** interview for evidence and judgment; light derive for restructuring maps.
- **Does:** the [discovery loop](../product_discovery.md#discovery-loop) — frame the outcome; coach the human through evidence capture (`EV#` — the agent asks about *specific past behavior*, never accepts hypothetical enthusiasm as strong evidence); map opportunities (`OPP#`) separately from solutions; expose and rank assumptions (`ASM#`) by the four risks; draft experiment cards (`EXP#`) with success/failure/inconclusive criteria; record the proceed/adapt/pause/abandon decision (`DEC#`).
- **Integrations:** seeds from the companion's `discovery-seeds.md` and the vision's critical-assumptions stub; "test cheaply" may hand off to `prototype`; pause/resume via the `brainstorm-vision` `.wip` pattern.
- **Guardrail:** the skill *coaches* evidence-gathering, it never fabricates evidence. An `EV` row without a human-supplied source is invalid.

### 5.5 `define-release` (new)

- **Mode:** interview — selection and prioritization are human judgment; the agent enforces the discipline.
- **Does:** [product definition](../product_definition.md)'s activities — select `OPP`s (record deferrals with reasons); express scope as capabilities in solution-neutral language (reusing/extending the companion's `CAP` map); check the boundary against the vision's `S`-ladder and escalate to a vision conversation when scope fights it; prioritize with the stated criteria (every "must" needs a consequence; ties break by learning value); cut a thin coherent slice and name the hypothesis it tests, with success/guardrail/stop criteria. Writes `releases/REL<n>-definition.md`.
- **Guardrails:** refuses a release without a hypothesis or stop criteria; refuses scope items that trace to no `OPP`/evidence without an explicit `DEC` override.

### 5.6 `specify-requirements` (new)

- **Mode:** AFK derive with a human review gate (the companion's builder/critic + `decisions.md` pattern, at smaller scale) — most content is restructuring the committed slice; conflicts and gaps go to the human.
- **Does:** for one `REL`: elaborate the in-scope `UC`s with alternative and failure paths ([use cases doc](../use_cases_and_story_mapping.md)); specify functional/interface/data/transition requirements (`REQ#`) in the trigger–response–constraint form from [requirements_engineering.md](../requirements_engineering.md); sharpen quality attributes into measurable scenarios (`QAS#`), seeding from the `*-architecture-lens.md`; maintain traceability `EV/OPP → CAP → UC/REQ/QAS`.
- **Integrations:** calls `domain-modeling` when new terms/rules surface (`domain-glossary.md` and `CONTEXT.md` stay canonical); `grill-with-docs` as the validation review. Its output — the specified slice — is this skillset's terminal artifact; what consumes it is the future design skillset's concern (§6).
- **Guardrails:** flags vague terms ("fast", "secure") without measurable criteria; every `REQ` needs a verification method or an explicit open marker.

### 5.7 `validate-release` (new)

- **Mode:** short interview per review cadence.
- **Does:** compare observed outcomes against `REL`'s success/guardrail/stop criteria; pull in evidence accumulated via `qa`/`triage` issues; record the verdict and — the essential part — **what it reopens** (vision / opportunities / scope / requirements) as `DEC` entries plus new `EV` rows, then point at the loop re-entry.
- **Guardrail:** shipping is not success; a review that measures nothing but "it shipped" is flagged as such.

## 6. Downstream skillsets — hints only, not fixed

This skillset ends at the readiness-for-design checklist. The following is **not part of this plan** — just orientation for the phase-classification of existing skills and ideas for the next planning round:

- **Design skillset (next, separate plan):** would consume the specified slice (`REL<n>-definition.md` + `REL<n>-requirements.md` + `quality-scenarios.md` + the companion bundle). Candidate existing skills: `design-an-interface`, `codebase-design`, `improve-codebase-architecture`, `prototype` (UI-variations branch), `grill-with-docs` (design-entry stress test), `domain-modeling` (ADRs during design).
- **Implementation-planning / delivery:** `to-prd` and `to-issues` live here — they convert committed scope into tracker artifacts. Deliberately *excluded* from this skillset so the loop's output stays a product artifact, not a backlog.
- **Implementation / testing:** `tdd`, `implement`, `verify`, `review`, `code-review` — far downstream; only relevant to this plan as the source of the post-release evidence that `validate-release` consumes (via `qa`/`triage`).

## 7. Open questions (to discuss before building)

1. **Workspace location and naming** — `docs/product/` vs. extending `docs/brainstorming/`; one workspace per product vs. per topic.
2. **Where do product principles live?** Vision stub (elicited when?), companion derivation, or first `discover-product` session.
3. **Skill granularity** — is `discover-product` one skill or two (`map-opportunities` interview + `run-experiment` wrapper around `prototype`)? Current lean: one skill, sub-files per phase, like `brainstorm-vision`.
4. **How much of `specify-requirements` is AFK-safe?** Use-case elaboration invents failure paths — that's judgment. Maybe builder drafts + human confirms per UC rather than end-review only.
5. **Story mapping** — the collection gives it a large role in definition ([use_cases_and_story_mapping.md](../use_cases_and_story_mapping.md)); is a markdown story map useful enough in a solo/agent workflow, or does the `CAP` × journey table in `REL-definition.md` suffice?
6. **Decision-log mechanics** — single append-only `decision-log.md` vs. per-stage logs; and whether `DEC` rows should follow the companion's confidence-tag convention for a single review surface.
7. **Cadence enforcement** — should skills read `lifecycle-onepager.md` and *refuse* to run out of order, or only warn? (Lean: warn; tailoring is a guide, not a gate.)
8. **Naming** — skill names above are placeholders (`discover-product`, `define-release`, `specify-requirements`, `validate-release`, `tailor-lifecycle`); align with existing naming style before creating.
9. **Method-doc consumption mechanism** — distill each stage doc into the skill's sub-files at authoring time (self-contained, portable, but drifts when the doc evolves) vs. skills reading the docs live from the parent method folder at runtime (always current, but couples skills to this machine's layout). Lean: distill + cite the source doc with its status/date, and treat doc updates as a trigger to revisit the skill.
