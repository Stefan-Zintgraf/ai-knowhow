# `brainstorm-vision` — contribution and coverage assurance

**Status:** Authoring contract for the planned adjustment  
**Skill:** `brainstorm-vision`  
**Purpose:** Ensure that the adjusted skill incorporates every relevant method requirement and deliberately considers every relevant contribution identified in [`github_skillsets.md`](./github_skillsets.md), without weakening the proprietary vision artifact or importing incompatible external orchestration.

## 1. Scope and governing rule

This file is a completeness contract, not a mandate to adopt everything.

The adjusted skill must preserve its proprietary divergent core:

- one-question-at-a-time vision exploration;
- stable `S#`, `V#`, `UC#`, and `BV#` identifiers;
- the scope ladder and human-controlled climb/close decisions;
- pause/resume through the `.wip.md` artifact;
- the architecture-significance sweep;
- a finalized `<slug>-foundation-vision.md` as its canonical output.

Every contribution below must end in one explicit disposition:

- **adopt** — use substantially as identified;
- **adapt** — incorporate the mechanism in a spine-compatible form;
- **reference** — retain as authoring background without copying or depending on it;
- **defer** — route to the named later skill;
- **reject** — do not use, with the reason recorded.

No contribution may remain merely “interesting” or “to consider” when authoring is complete.

## 2. External-contribution ledger

| ID | Source | Exact contribution considered | Mode | Proposed incorporation | Disposition | License / provenance constraint | Required verification evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BV-E01 | `deanpeters/Product-Manager-Skills` — `press-release` | Amazon Working Backwards-style press release as a test of whether a vision describes an outcome in plain language rather than a feature list | pattern + reference | Add an optional convergent stress test after divergence and before final acceptance: attempt to explain the intended future, beneficiary, and value in press-release language; route exposed gaps back to the relevant vision section | **adapt** | CC BY-NC-SA 4.0. Do not copy prompts, sequences, examples, or wording. Use only the abstract idea already independently represented in [`product_vision.md`](../product_vision.md) | Skill instructions identify the optional stress test; a fixture shows a feature-shaped vision failing it and being reopened; provenance note cites the repository and retrieval date |
| BV-E02 | `deanpeters/Product-Manager-Skills` — three-tier taxonomy | Separation of workflow/orchestration, interactive coaching, and reusable components | pattern + reference | Keep orchestration in `SKILL.md`, interview behavior in phase sub-files, and reusable checks/templates in focused references; do not reproduce the source taxonomy text | **adapt** | Same CC BY-NC-SA restriction; structural inspiration only | File-responsibility map demonstrates that orchestration, interactive behavior, and reusable checks are separated without copied content |
| BV-E03 | `phuryn/pm-skills` | Command-chaining UX: each completed skill names the appropriate next step | pattern | Final response names `create-vision-companion` as the normal greenfield successor and points non-greenfield or deliberately skipped flows back to the tailored lifecycle | **adopt** | MIT, but no runtime dependency is needed | Finalization fixture verifies a concrete handoff, artifact path, and next skill; no generic “what next?” ending |
| BV-E04 | `huntsyea/product-skills` — `jobs-to-be-done` | Stable-progress framing independent of a solution | reference | Retain JTBD as one optional vision lens through the method-owned guidance in [`product_vision.md`](../product_vision.md); do not vendor the external workflow into the brainstorm because evidence-oriented JTBD interviewing belongs to `discover-product` | **defer** to `discover-product` for distillation | MIT; if later distilled, preserve source pointer and retrieval date | `brainstorm-vision` does not contain vendored Huntsyea prompts; its optional JTBD wording traces to the method doc; deferral is named in this ledger |
| BV-E05 | `assimovt/productskills` | Compact, low-ceremony skill shape suitable for solo developers | pattern + reference | Ensure the vision adjustment adds only bounded finalize checks and honors configured use-case limits and lifecycle tailoring; do not import discovery-interview content | **adapt** | MIT; no content needs to be copied | A low-ceremony fixture completes with the minimum useful vision artifact and explicit open stubs, without invoking unrelated discovery exercises |
| BV-E06 | `jacksoncalling/argo-continuous-discovery` | Explicit human gates before scope-changing decisions and explicit routing of findings | pattern | Preserve human ownership of every scope-ladder climb/close choice; route a scope-significant architecture-sweep finding back through the scope lens rather than widening automatically | **adopt** as a corroborating pattern | License must be rechecked before copying; no source expression is needed | Tests show that the agent cannot silently climb the ladder and that a scope-significant sweep finding follows the documented route-back |
| BV-E07 | `shinpr/claude-code-discover` | Durable product-context artifacts stored beside the code | pattern | Preserve the repository-resident `.wip.md` and finalized foundation vision as the durable record; do not adopt Shinpr’s competing artifact taxonomy | **adopt** as an already-satisfied pattern | MIT; no runtime dependency | Static test confirms all durable session state needed for resume is in repository artifacts, not only chat |
| BV-E08 | `ForceInjection/domain-driven-design-skills` | Explicit backtracking-trigger matrices rather than informal “reopen if needed” prose | pattern | Add or retain an explicit route table for: completion-check failure → relevant finalize section; scope-significant sweep finding → scope lens; changed vision after reopening → affected finalize checks and companion rerun | **adapt** | WIP source; verify current license before any copying. Adopt mechanism only | A route table exists and tests cover every trigger and destination; no trigger terminates in an unspecified “revisit” action |
| BV-E09 | Cross-cutting finding in [`github_skillsets.md`](./github_skillsets.md) | Runtime dependencies move and external taxonomies collide with the proprietary spine | pattern | `brainstorm-vision` has no runtime third-party dependency. External material is either method-owned, pattern-only, or explicitly deferred | **adopt** | Record source, repository, license, and retrieval date for every retained reference | Dependency inventory for the skill is empty except local owned files; authoring review confirms no live fetch or external trigger dependency |
| BV-E10 | Cross-cutting finding in [`github_skillsets.md`](./github_skillsets.md) | Method docs should become output shapes, gates, and guardrails rather than optional reading | pattern | Treat the method-doc coverage ledger below as normative authoring input and add a drift/review trigger when a consumed method doc changes | **adopt** | Proprietary local method docs | Each consumed provision has an implementation location or explicit exclusion; source status/date is recorded in the skill |
| BV-E11 | `ai-analyst-lab/north-star` | Deterministic audit of outcome metrics and rejection of vanity metrics | reference | Keep `Outcomes and signals` at vision level and mark it open when not mature; do not call the metric-audit skill during divergent vision work | **defer** to `define-release` and `validate-release` | MIT code; embedded Amplitude-derived content has separate copyright constraints | No runtime call from `brainstorm-vision`; handoff/open stub makes clear that metric audit occurs later |
| BV-E12 | `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` | Plan an analysis before running it | reference | No vision-stage incorporation; the contribution belongs to post-release validation planning | **defer** to `validate-release` | No stated license; do not copy or redistribute content | Explicit deferral remains recorded; no copied material exists in the skill |

## 3. Method-document coverage ledger

| ID | Method source | Required coverage | Proposed incorporation | Verification evidence |
| --- | --- | --- | --- | --- |
| BV-M01 | [`product_vision.md`](../product_vision.md) — questions and recommended structure | Context; actors and beneficiaries; desired change; value and differentiation; product principles; scope boundaries; outcomes and signals; critical assumptions | Preserve the existing vision points/use-cases/scope ladder and add explicit finalize coverage for missing method sections. A section may be populated or marked `OPEN`, but may not disappear silently | Finalized artifact fixture maps every recommended section to content or an explicit open stub |
| BV-M02 | [`product_vision.md`](../product_vision.md) — six completion checks | Outcome rather than feature; actor conflicts; evidence/assumption/aspiration distinction; actionable principles; meaningful exclusions; observable outcomes with guardrails | Make all six checks a named finalize gate. Failures reopen the relevant section or produce an explicit open stub; they are never silently passed | Gate report or test fixture demonstrates pass, reopen, and explicit-open outcomes for all six checks |
| BV-M03 | [`product_vision.md`](../product_vision.md) — ways to develop the vision | Vision narrative, press release, JTBD, principles workshop, premortem | Keep them as optional lenses selected for the uncertainty at hand, not mandatory ceremony. Press release is the external-pattern stress test; the rest remain method-owned | Skill guidance states when each lens is useful and that none replaces the core divergent interview |
| BV-M04 | [`overview.md`](../overview.md) — lifecycle position | Vision is a slow-changing anchor; discovery/definition/requirements form the faster loop; uncertainty may remain but must be visible | Final response distinguishes “vision finalized” from “product validated” and hands unresolved assumptions to downstream discovery | Fixture confirms the skill never claims that finalizing the vision proves demand, feasibility, or viability |
| BV-M05 | [`overview.md`](../overview.md) — minimum useful package and readiness | One-page product vision, named actors/outcomes, visible uncertainty, boundaries, and quality risks | Ensure the adjusted output is sufficient to seed the minimum package but does not attempt to produce downstream discovery or requirements artifacts | Output schema and handoff tests |
| BV-M06 | [`lifecycle_tailoring.md`](../lifecycle_tailoring.md) | Vision is the entry point for greenfield work; other entry points normally reuse an existing vision; ceremony scales with risk | At start, inspect or point to `lifecycle-onepager.md` when present. For a non-greenfield request, warn that an existing vision may need extension rather than replacement; do not hard-refuse | Greenfield and non-greenfield fixtures show different start behavior |
| BV-M07 | [`glossary.md`](../glossary.md) | Consistent meanings for actor, assumption, capability, evidence, guardrail, outcome, principle, signal, vision, lifecycle, and workflow | Align prompts, artifact headings, and gates with the method vocabulary; keep the product’s domain terms separate | Terminology lint or review finds no conflicting local definitions |
| BV-M08 | [`product_discovery.md`](../product_discovery.md) | Evidence is distinct from opinion; critical assumptions and alternative solutions remain downstream discovery work | Capture only vision-level evidence references and assumptions. Do not fabricate `EV#`, `ASM#`, `OPP#`, `SOL#`, or `EXP#` artifacts; leave explicit seeds for `discover-product` | Fixture verifies that the vision contains seeds/open stubs but no invented loop IDs or evidence |
| BV-M09 | [`quality_attributes.md`](../quality_attributes.md) | Architecture-changing qualities must surface early, but vague qualities are not requirements | Retain the architecture-significance sweep as a user-needs lens. Park genuine technical constraints and pass them forward; do not write premature `QAS#` scenarios | Sweep fixture distinguishes a user use case, a parked constraint, and a later measurable QAS |
| BV-M10 | [`validation_and_feedback.md`](../validation_and_feedback.md) | Outcome, guardrail, and qualitative-signal semantics; a vision whose outcome cannot be observed cannot be validated | Finalize gate checks that outcomes/signals are observable or explicitly open and that guardrails are not silently omitted | Fixture rejects “feature shipped” and bare usage as sufficient outcome definitions |
| BV-M11 | [`resources.md`](../resources.md) | Adopt a method only when it reduces uncertainty or improves a consequential decision; scale ceremony with risk | Optional lenses must state their decision purpose. No framework is run solely to complete a template | Review confirms each optional micro-phase has a selection rule and a skip path |

## 4. Authoring coverage gate

The adjusted `brainstorm-vision` skill is complete only when all conditions below pass.

### 4.1 Ledger completeness

- Every `BV-E#` and `BV-M#` row has a final disposition.
- No row contains unresolved language such as “consider,” “maybe,” or “TBD.”
- Every adopted or adapted external input names its implementation location.
- Every deferral names the receiving skill.
- Every rejection or exclusion records a reason.
- Repository, license, and retrieval date are recorded for every external source used as more than background.

### 4.2 Proprietary-spine preservation

- `S#`, `V#`, `UC#`, and `BV#` retain their current meanings and stable numbering rules.
- The skill writes no loop IDs (`ASM`, `EV`, `OPP`, `SOL`, `EXP`, `REL`, `REQ`, `QAS`, `DEC`).
- No external artifact taxonomy is introduced.
- Scope changes remain human decisions.
- The finalized output remains `<slug>-foundation-vision.md`.
- No output artifact is named `product_vision.md` or otherwise collides with a method-document filename.

### 4.3 Vision-method completeness

A finalized artifact contains, or explicitly marks open:

- present situation/context;
- differentiated actors and beneficiaries;
- desired change;
- value and differentiation;
- product principles;
- in-scope and outside-the-vision boundaries;
- outcomes, signals, and guardrails;
- critical assumptions.

All six completion checks from [`product_vision.md`](../product_vision.md) run at finalize. “Open” is an explicit result, not a passing result hidden behind polished prose.

### 4.4 External-input proof

- The optional press-release stress test is implemented without copied Dean Peters content.
- The finish response names the next stage.
- The scope-lens route-back behavior is explicit and tested.
- No runtime fetch or unpinned external skill call exists.
- The authoring notes show how each retained pattern changed the skill or why it was already satisfied.

### 4.5 Behavioral test matrix

At minimum, fixtures cover:

1. a low-ceremony greenfield product;
2. a high-risk product with conflicting actors;
3. a feature-shaped initial vision exposed by the press-release stress test;
4. missing principles/outcomes/assumptions becoming visible open stubs;
5. a non-greenfield request routed toward reuse or extension;
6. pause and resume in each existing resume state;
7. an architecture-sweep finding that stays in scope;
8. an architecture-sweep finding that reopens the scope ladder;
9. a genuine technical constraint routed to the parking lot;
10. a reopened finalized vision whose changed IDs remain stable and whose finalize checks rerun.

### 4.6 Drift gate

The skill records the consumed method-doc status or retrieval date. A change to [`product_vision.md`](../product_vision.md), [`overview.md`](../overview.md), [`lifecycle_tailoring.md`](../lifecycle_tailoring.md), [`glossary.md`](../glossary.md), [`product_discovery.md`](../product_discovery.md), [`quality_attributes.md`](../quality_attributes.md), or [`validation_and_feedback.md`](../validation_and_feedback.md) triggers a coverage-ledger review before the next release of the skill.

## 5. Explicit exclusions and deferrals

| Source | Exclusion / deferral |
| --- | --- |
| `huntsyea/product-skills` continuous-discovery workflows | Evidence gathering, opportunity mapping, and assumption testing belong to `discover-product`; they must not turn the vision brainstorm into a full discovery pipeline |
| `assimovt/productskills` interview, validation, experiment, scope, and bet content | Route to `discover-product` or `define-release`; retain only the low-ceremony structural lesson here |
| Argo interview-quality rubric and confidence cap | Route to `discover-product`’s `EV#` strength model; a vision brainstorm does not score fabricated or second-hand evidence |
| Shinpr hypothesis-file format and verifier | Route to experiment cards and the AFK requirements review; the vision does not create hypotheses as loop artifacts |
| `RafaelGorski/Problem-Based-SRS` | Requirements traceability and validation belong to `specify-requirements` and the workspace linter |
| `45ck/software-architecture-skills` | QAS authoring belongs to `specify-requirements`; the architecture sweep remains a user-needs lens |
| `DavidROliverBA/Daves-Claude-Code-Skills` | NFR completeness/measurability/feasibility review belongs to the QAS gate |
| `ddd-crew/ddd-starter-modelling-process` | Reference for domain modeling and the future design skillset |
| `ForceInjection/domain-driven-design-skills` tactical DDD content | Future design skillset; only the backtracking-trigger mechanism is relevant here |
| `lagz0ne/design-skill` | Begins after requirements; future design skillset |
| `ai-analyst-lab/north-star` | Metric audit belongs to `define-release` and `validate-release`, not divergent vision creation |
| `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` | Validation-analysis planning only; unlicensed content must not be distilled |

These exclusions prevent skill creep while proving that the named contributions were considered.
