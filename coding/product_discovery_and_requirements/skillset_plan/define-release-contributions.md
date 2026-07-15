# Authoring Assurance: `define-release`

**Status:** Required authoring contract  
**Applies to:** `define-release` skill implementation and every material revision  
**Primary output:** `releases/REL<n>-definition.md`

**Planning sources:** [skillset plan](./prod_discovery_requirements_skillset_plan.md) · [GitHub skillset fit analysis](./github_skillsets.md)  
**Primary method sources:** [Product definition](../product_definition.md) · [Use cases and story mapping](../use_cases_and_story_mapping.md) · [Validation and feedback](../validation_and_feedback.md)

## 1. Purpose and scope

This file prevents useful method content and external contributions from disappearing between planning and skill authoring. The `define-release` skill is not complete merely because it can write a release definition. It is complete only when:

- all relevant method-document requirements have been incorporated and verified;
- every relevant external contribution has an explicit disposition;
- the release definition remains part of the proprietary traceability spine;
- the skill works at both minimum and high-ceremony levels;
- deterministic checks catch structural defects that prose review could miss; and
- end-to-end tests show that its output can be consumed by `specify-requirements` and later reopened by `validate-release`.

Allowed contribution dispositions are `adopt`, `adapt`, `reject`, or `defer`. No row may remain `pending` when the skill is declared authoring-complete. Adoption is not automatic: preservation of the proprietary artifact model, license compatibility, method fidelity, and proportional ceremony take priority.

## 2. External-contribution ledger

Before authoring, replace every source pointer below with the exact repository URL, commit SHA or release, files inspected, retrieval date, and verified license. Runtime calls must be version-pinned. Distilled material must retain source and attribution metadata.

| ID | Source | Exact contribution to assess | Mode | Required incorporation | Disposition | License and provenance requirement | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DR-EXT-01 | `huntsyea/product-skills` — `story-mapping` references/workflows | Journey backbone, task decomposition, omission finding, thin end-to-end slicing, and flat-backlog anti-patterns | distill | Provide a progressive-disclosure story-mapping reference used when shaping journeys and cutting a coherent release | adopt | MIT; record exact files, commit, retrieval date, and former `rohanpatriot` location | Fixture proves a slice crosses the journey end to end and rejects a single-layer slice |
| DR-EXT-02 | `huntsyea/product-skills` — `shape-up` references/workflows | Appetite, pitch shaping, commitment/betting discipline, boundaries, risks, and no-go decisions | distill | Add an optional shaping path for topics where appetite and commitment are useful; translate its concepts into the proprietary `REL` artifact rather than importing a competing pitch artifact | adapt | MIT; exact source-file audit required | High-ceremony and low-ceremony fixtures show that appetite constrains scope without becoming a mandatory artifact |
| DR-EXT-03 | `assimovt/productskills` — `scope-cutting` | Concrete scope-reduction checks and coherent-slice guardrails | distill | Add scope-cutting prompts and failure checks; distinguish “small” from “coherent” | adopt | MIT; record exact file and commit | Negative fixture with disconnected items fails finalization |
| DR-EXT-04 | `assimovt/productskills` — `bet-sizing` | Size the investment against uncertainty, reversibility, and learning value | distill | Add a proportional-investment check that complements lifecycle ceremony and release stop criteria | adapt | MIT; record exact file and commit | Fixture shows a reversible uncertainty receives a smaller bet than an irreversible regulated commitment |
| DR-EXT-05 | `assimovt/productskills` — `prd-writing` | Evidence-first scope rationale | distill | Use only the evidence-first guardrails; do not turn the output into a PRD or import its artifact taxonomy | adapt | MIT; exact source-file audit required | Every scope decision either resolves to evidence or carries an explicit `DEC` override |
| DR-EXT-06 | `RafaelGorski/Problem-Based-SRS` | Obligation / Expectation / Hope classification and the rule that mandatory claims require a consequence | pattern | Classify each mandatory scope driver as obligation, expectation, or hope; record the consequence that makes an obligation mandatory; do not introduce `CP/CN/FR` identifiers | adapt | MIT; cite inspected action/reference files and commit | Mechanical check rejects an unclassified “must” or one without a stated consequence |
| DR-EXT-07 | `ai-analyst-lab/north-star` | Deterministic audit of success metrics, rejection of vanity metrics, driver/input distinction | call | Offer a version-pinned metric-audit step for release success measures; write the audit outcome or justified skip into the `REL` review metadata | adopt | MIT code; verify the pinned version and preserve notices; Amplitude-derived content requires provenance review and must not be vendored casually | Fixture rejects a pure usage/vanity metric as sufficient outcome evidence |
| DR-EXT-08 | `phuryn/pm-skills` — `north-star-metric` and metric-tree material | Alternative metric decomposition | reference/pattern | Evaluate against `ai-analyst-lab/north-star`; retain only complementary metric-tree ideas that do not justify a second runtime dependency | adapt or reject | MIT; record comparison and source version | Ledger records why each complementary idea was adopted or rejected |
| DR-EXT-09 | `shinpr/claude-code-discover` — hypothesis format | Explicit success and failure criteria, confidence by risk dimension, time budget, and rejected alternatives | pattern | Strengthen the release-hypothesis section while keeping the `REL` schema and traceability spine; include expected outcome, failure/stop interpretation, unresolved risks, and investment boundary where useful | adapt | MIT; record exact hypothesis template and commit | Fixture proves that the release can be judged as success, failure, or inconclusive after shipping |
| DR-EXT-10 | `deanpeters/Product-Manager-Skills` — `user-story-mapping` | Question flow for identifying the journey, backbone, tasks, and slices | reference only | Compare its coverage with the proprietary method and the MIT-licensed Huntsyea donor; record any unfilled conceptual gap without copying protected content | reject for distillation | CC BY-NC-SA 4.0; no distillation into a commercial proprietary skill | Source audit records comparison and confirms that no text or protected sequence was copied |
| DR-EXT-11 | `phuryn/pm-skills` — command chaining | Every stage ends by naming the next useful action | pattern | Final response names the next stage selected by `lifecycle-onepager.md`, all required input files, unresolved blockers, and the correct resume/re-entry point | adopt | Pattern only; cite repository and inspected command examples | Handover test proves `specify-requirements` can start without rediscovering files or state |
| DR-EXT-12 | `ForceInjection/domain-driven-design-skills` | Explicit quantitative backtracking-trigger matrices | pattern | Define precise triggers for returning to discovery, reopening vision, requesting domain work, or stopping definition | adapt | WIP; record commit, language/version reviewed, and provenance; copy no unlicensed or uncertain text | Each trigger maps to one artifact, decision owner, and next skill; ambiguous “go back” instructions fail review |

## 3. Method-document coverage ledger

| ID | Method document | Required use in `define-release` | Verification |
| --- | --- | --- | --- |
| DR-MTH-01 | [Overview](../overview.md) | Preserve lifecycle position, minimum useful package, coherent-slice handoff, and readiness-for-design questions | End-to-end fixture traces definition into the final readiness review |
| DR-MTH-02 | [Lifecycle tailoring](../lifecycle_tailoring.md) | Respect entry point, ceremony level, selected artifacts, skipped-stage reasons, cadence, and decision authority | Low- and high-ceremony fixtures produce proportionate outputs |
| DR-MTH-03 | [Product vision](../product_vision.md) | Check scope against the vision boundary, principles, actors, outcomes, and `S#` ladder; escalate conflicts rather than silently expanding scope | Boundary-conflict fixture triggers vision re-entry |
| DR-MTH-04 | [Product discovery](../product_discovery.md) | Consume real `OPP`, `EV`, `ASM`, `EXP`, and `DEC` inputs without manufacturing evidence | Missing-evidence fixture requires an override or returns to discovery |
| DR-MTH-05 | [Product definition](../product_definition.md) | Use all seven activities, the one-pager shape, prioritization criteria, failure modes, and completion checks | Field-by-field conformance test and finalize gate |
| DR-MTH-06 | [Use cases and story mapping](../use_cases_and_story_mapping.md) | Shape journeys, expose omissions, cut a thin end-to-end slice, and name its outcome or learning purpose | Story-map coverage and coherent-slice tests |
| DR-MTH-07 | [Domain discovery](../domain_discovery.md) | Reuse solution-neutral capabilities and canonical language; request domain work when terms, ownership, or rules are contested | Terminology-conflict fixture calls the canonical domain workflow |
| DR-MTH-08 | [Quality attributes](../quality_attributes.md) | Surface architecture-changing qualities, explicit trade-offs, operational consequences, and guardrails early enough to affect scope | Risk fixture prevents deferring a load-bearing quality concern silently |
| DR-MTH-09 | [Requirements engineering](../requirements_engineering.md) | Preserve constraints and transition concerns; state how outcome and guardrail measures will be observable | Instrumentation handoff test gives `specify-requirements` actionable measurement needs |
| DR-MTH-10 | [Validation and feedback](../validation_and_feedback.md) | Define observable success, guardrail, and stop criteria; schedule ownership and make later reopening possible | `validate-release` fixture can evaluate the `REL` without inventing criteria |
| DR-MTH-11 | [Glossary](../glossary.md) | Use canonical method terms and keep the method glossary distinct from `domain-glossary.md` | Terminology lint and review |
| DR-MTH-12 | [Resources](../resources.md) | Use only techniques appropriate to the dominant uncertainty and ceremony | Authoring review records selected and deliberately unused techniques |

## 4. Deterministic checks

The workspace linter must validate at least:

- `REL#` is unique and the filename and internal identifier agree.
- Every addressed `OPP#`, cited `EV#`, reused `CAP#`, `UC#`, `ASM#`, `EXP#`, and `DEC#` resolves.
- Every in-scope capability resolves to at least one selected opportunity and supporting evidence, unless a dated `DEC#` override names owner and rationale.
- Every deferred or rejected opportunity has a reason.
- Every mandatory scope item has an Obligation / Expectation / Hope classification; each obligation has a consequence.
- The release has one named hypothesis plus success, guardrail, and stop criteria.
- Each outcome and guardrail measure has an observation or instrumentation handoff.
- The release slice spans an end-to-end journey or records why story mapping was deliberately skipped.
- Scope conflicting with vision boundaries is marked unresolved and cannot silently pass.
- Decision owner, decision date, next review owner, and intended review timing exist.
- Handover fields name the next stage and exact input artifacts.

## 5. Authoring coverage gate

`define-release` is authoring-complete only when all boxes are checked:

- [ ] Every external row has an `adopt`, `adapt`, `reject`, or `defer` disposition and an evidence-backed reason.
- [ ] Every adopted/distilled item links to the resulting skill file, section, prompt, template field, guardrail, or test.
- [ ] Every runtime call is version-pinned and has a documented unavailable/failed-call fallback.
- [ ] Every source’s exact files, commit, retrieval date, license, attribution, and redistribution implications have been reverified.
- [ ] All method rows map to concrete implementation locations and tests.
- [ ] The skill supports both an existing story map and creation of the minimum useful map.
- [ ] Scope cutting, Shape Up/appetite, bet sizing, and O/E/H classification remain optional or proportional where ceremony demands it, without weakening traceability.
- [ ] The North Star audit is callable but not a prerequisite when it is irrelevant; a justified skip is recorded.
- [ ] The mechanical linter passes the positive fixtures and fails every intentional trace mutation.
- [ ] Separate builder and reviewer runs confirm that a plausible but unsupported scope does not pass merely because the prose is polished.
- [ ] The handover names `specify-requirements`, required artifacts, open decisions, and any domain or instrumentation work.
- [ ] A `validate-release` fixture can later assess the output without retroactively inventing success criteria.

## 6. Cross-cutting skillset validation

The shared end-to-end suite must include:

1. Greenfield, fast-follow, compliance, rework, platform, low-ceremony, and high-risk/regulated scenarios.
2. A full reference topic from companion IDs through discovery, `REL`, `REQ/QAS`, review, and targeted re-entry.
3. Mutation tests for broken identifiers, missing rationale, absent stop criteria, vanity metrics, incoherent slices, and vision-boundary violations.
4. Blind review: the critic sees authoritative inputs, candidate output, and gates, but not the builder’s expectations or reasoning.
5. Handover tests that start the next skill using only durable artifacts and the final handover.
6. Source-coverage tests proving every adopted external contribution appears in an implementation location and at least one fixture.
7. License/provenance review as a release gate for the skill itself.

## 7. Exclusions and deferrals

- Do not adopt an external PRD, pitch, `CP/CN/FR`, or discovery-workspace taxonomy.
- Do not copy or distill `deanpeters` content because of CC BY-NC-SA restrictions; retain only a documented comparison.
- Do not install the full Phuryn marketplace.
- Do not let story-level delivery prioritization replace release-level capability prioritization.
- Do not make story mapping or Shape Up ceremony mandatory where a capability-by-journey table is sufficient.
- Architecture design, UI solutioning, implementation planning, backlog generation, and delivery remain downstream.
- External design packs (`45ck` beyond QAS, `lagz0ne`, DDD tactical-design skills, and DDD Crew canvases) remain deferred to the future design-skillset plan.
