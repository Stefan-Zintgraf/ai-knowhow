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

Allowed contribution dispositions are `adopt`, `adapt`, `call` (a version-pinned specialist with a bounded contract that never owns spine artifacts), `reject`, or `defer`. No row may remain `pending` when the skill is declared authoring-complete. Adoption is not automatic: preservation of the proprietary artifact model, license compatibility, method fidelity, and proportional ceremony take priority.

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
| DR-EXT-07 | `ai-analyst-lab/north-star` | Deterministic audit of success metrics, rejection of vanity metrics, driver/input distinction | call | Offer a version-pinned metric-audit step for release success measures; write the audit outcome or justified skip into the `REL` review metadata | call *(normalized from `adopt` per revision-contract update 4: call-mode rows carry the `call` disposition)* | MIT code; verify the pinned version and preserve notices; Amplitude-derived content requires provenance review and must not be vendored casually | Fixture rejects a pure usage/vanity metric as sufficient outcome evidence. Call contract (update 4, plan §3.1): inputs = candidate outcome/guardrail metrics plus the `REL` hypothesis and criteria as decomposition context; outputs = audit result, warnings, and triage, written into the `REL` review metadata by the calling skill (the specialist writes no spine artifact); version pin = exact commit/release recorded in the skillset dependency manifest at authoring, never a floating ref, upgrades only via ledger reopen; fallback = justified skip recorded in review metadata, or a transparent local metric review against [validation_and_feedback.md](../validation_and_feedback.md) |
| DR-EXT-08 | `phuryn/pm-skills` — `north-star-metric` and metric-tree material | Alternative metric decomposition | pattern | Evaluate against `ai-analyst-lab/north-star`; retain only complementary metric-tree ideas that do not justify a second runtime dependency | adapt *(finalized in revision-contract update 4)* | MIT; record comparison and source version | Final rationale (update 4): adapt — the MIT-licensed outcome/driver/input metric-tree decomposition is retained as locally authored prompt material that prepares candidate metrics for the DR-EXT-07 audit or its local fallback (plan §5.5); it never becomes a second runtime dependency, and any idea duplicating the audit itself is excluded. Ledger records why each complementary idea was adopted or rejected at authoring |
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

### Method-owned rows (revision-contract updates 9–10)

Method-owned rows carry no external license or disposition (revision-contract ledger rules).

| ID | Method document | Required use in `define-release` | Verification |
| --- | --- | --- | --- |
| DR-M01 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — singular accountable ownership (core rules 2–3, decision language) | The `REL` decision metadata (the owner/date/review fields LNT-15 checks) carries the full seven-field decision-authority depth for the release commitment per `lifecycle-onepager.md` (plan §5.3, §5.5): one named accountable owner — a group or department as owner fails finalize — plus required contributors, specialist authorities, formal approvers where applicable, the evidence required to decide, the escalation path, and the evidence-based reopen trigger | Regression scenario RTS-07: a group-only owner is detected and refused; finalize fixture with a department as decision owner fails |
| DR-M02 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — required specialist participation; no fabricated specialist evidence (core rules 4–5) | When usability, feasibility, viability, or quality evidence is material to scope, the named design/engineering/operations/security/compliance/domain input is present before the release finalizes (plan §5.5); a missing required specialist input blocks finalize or is recorded as an explicit `DEC#` skip with the gap carrying an `OPEN:` marker; the skill fabricates no specialist evidence | Regression scenario RTS-08: missing required specialist/engineering input is detected and refused; missing-input fixture fails finalize or records the explicit `DEC#` skip |
| DR-M03 | [Product vision](../product_vision.md) — thin ordered-outcomes strategy; revision-contract update 10 | Check selected `OPP#`s against the companion-derived strategy order; contradiction needs an explicit `DEC#` exception or strategy reorder, never silent divergence, reorder, or vision edit (plan §2, §5.5) | Off-strategy selection fixture blocks without `DEC#`; reorder fixture records a discovery pivot and refreshes the derived index |
| DR-M04 | [Lifecycle tailoring](../lifecycle_tailoring.md) — optional roadmap ceremony gate; revision-contract update 10 | Only when the one-pager adopts it, maintain an outcome-based rolling now/next/later view; skip creates no roadmap and no downstream requirement. Feature/date-only entries fail LNT-14 (plan §5.3, §5.5) | RTS-13 paired variants pass; LNT-14 rejects a feature-only or date-only entry |
| DR-M05 | [Product vision](../product_vision.md) — discovery-pivot/vision-pivot routing; revision-contract update 10 | Route routine conflicts to discovery, scope, or strategy. A vision-boundary conflict becomes a `DEC#`-carrying re-entry request to `brainstorm-vision`; `define-release` never edits the vision (plan §4, §5.5) | RTS-11 refuses failed-release/weak-feature escalation; RTS-12 permits genuine vision re-entry only with the evidence-citing `DEC#` |

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
- When the one-pager adopts a roadmap, each now/next/later entry names an outcome; feature-only or date-only entries fail. When skipped, no roadmap is required.

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
- [ ] Strategy conflicts and vision re-entry use explicit `DEC#` routes, and RTS-11/RTS-12 pass.
- [ ] Both RTS-13 roadmap variants pass and adopted views fail LNT-14 on feature/date-only entries.

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

## 8. Plan-to-authoring traceability (revision-contract update 8)

Maps every accepted row to its plan location and **planned** skill-file destination (paths relative to the future `skills/define-release/` directory; the skill is not authored yet). Governing rules — replace-planned-with-actual, reopen, date capture, post-authoring reconciliation — are in [plan §3.3](./prod_discovery_requirements_skillset_plan.md), whose donor-audit task table carries this ledger's five distill rows (DR-EXT-01..05). **Date capture:** the §2 preamble's replace-every-source-pointer instruction (exact repository URL, commit SHA/release, files inspected, retrieval date, verified license) is an explicit authoring-time task for every external row (plan §3.3); no row records these values yet. The method-coverage rows DR-MTH-01..12 each have their own plan location, planned file/section, and objective fixture, linter check, or regression target below; DR-MTH-09 is the instrumentation contract's producing end through LNT-09.

| Row | Plan § | Planned destination (path/section) |
| --- | --- | --- |
| DR-EXT-01 | §3.3, §5.5, LNT — §2.2 via §4 checks | Vendored progressive-disclosure story-mapping reference file; end-to-end-slice fixture |
| DR-EXT-02 | §3.3, §5.5 | Optional shaping/appetite path (ceremony-gated) recorded inside the `REL` template |
| DR-EXT-03 | §3.3, §5.5 | Scope-cutting prompts + coherent-slice finalize check; disconnected-items negative fixture |
| DR-EXT-04 | §3.3, §5.5 | Proportional-investment (bet-sizing) check tied to ceremony and stop criteria |
| DR-EXT-05 | §2.2 (LNT-15), §3.3, §5.5 | Evidence-first scope-rationale guardrails; `DEC` override path |
| DR-EXT-06 | §2.2 (LNT-15), §5.5 | O/E/H classification fields in the `REL` template + consequence rule |
| DR-EXT-07 | §3.1, §5.5 | `north-star` call step (invocation condition, inputs/outputs, pin, fallback per plan §3.1); review-metadata fields in `REL` |
| DR-EXT-08 | §5.5 | Locally authored metric-tree prompts preparing the DR-EXT-07 audit / local fallback |
| DR-EXT-09 | §5.5, LNT-08 | Enriched `REL` hypothesis section (predeclared interpretation, per-risk confidence, time budget, investment boundary) |
| DR-EXT-10 | reject (for distillation) | — no destination; documented comparison only |
| DR-EXT-11 | §4.1, §5.5 | Final-response handover section (next stage, input files, blockers, resume point) |
| DR-EXT-12 | §4.2, §5.5 | Backtracking-trigger matrix reference file (one artifact, owner, next skill per trigger) |
| DR-MTH-01 | §2.1, §4, §5.5, §6 | `SKILL.md` sections **Lifecycle position** and **Readiness handover**; reference-topic fixture `fixtures/definition-to-readiness` traces the coherent slice into the final readiness review |
| DR-MTH-02 | §2.1, §4.1, §5.3, §5.5, §6 | `SKILL.md` start gate **Read lifecycle one-pager** and ceremony/skip controls; `fixtures/tailored-definition` covers low/high ceremony and explicit skips, including RTS-01/RTS-02/RTS-13 |
| DR-MTH-03 | §2 (vision/strategy inputs), §2.1, §4, §5.5, §6 | `SKILL.md` section **Vision boundary and principle check** plus `references/backtracking-matrix.md`; `fixtures/vision-boundary-conflict` requires a routed, evidence-citing `DEC#` and exercises RTS-11/RTS-12 |
| DR-MTH-04 | §2 (discovery inputs), §2.1, §2.2 (LNT-03, LNT-15), §5.5 | `SKILL.md` section **Authoritative discovery inputs**; `fixtures/missing-discovery-evidence` rejects manufactured `EV/OPP/ASM/EXP/DEC` data and requires an override or discovery return |
| DR-MTH-05 | §2 (`releases/REL<n>-definition.md`), §2.1, §2.2 (LNT-08, LNT-09, LNT-15), §5.5, §6 | `references/release-definition-template.md` plus `references/finalize-rubric.md`; `fixtures/product-definition-conformance` checks all seven activities, every one-pager field, failure guardrails, and completion checks |
| DR-MTH-06 | §2.1, §5.5 | `references/story-mapping.md` and `SKILL.md` section **Journey shaping and slicing**; `fixtures/coherent-end-to-end-slice` rejects a single-layer slice and verifies outcome/learning purpose |
| DR-MTH-07 | §2.1, §3.1, §5.5 | `SKILL.md` section **Canonical domain-language gate**; `fixtures/terminology-conflict` invokes the pinned `domain-modeling` contract/manual fallback without creating a competing glossary |
| DR-MTH-08 | §2.1, §5.5 | `SKILL.md` section **Architecture-changing quality risk and trade-off check**; `fixtures/load-bearing-quality-risk` fails a release that silently defers a scope-changing operational concern |
| DR-MTH-09 | §2.1, §2.2 (LNT-09), §5.5, §5.6 | `references/release-definition-template.md` outcome/guardrail observation fields and instrumentation handoff; `fixtures/instrumentation-handoff` proves `specify-requirements` receives actionable measurement needs |
| DR-MTH-10 | §2 (`validation/REL<n>-review.md` contract), §2.1, §2.2 (LNT-08, LNT-09, LNT-17), §5.5, §5.7 | `references/release-definition-template.md` precommitted criteria/review-owner fields; `fixtures/validate-without-retrofit` proves `validate-release` can judge the `REL` without invented or rewritten criteria |
| DR-MTH-11 | §2.1, §5.5 | `SKILL.md` section **Method terminology contract**; `fixtures/terminology-audit` checks canonical terms and enforces separation from `domain-glossary.md` |
| DR-MTH-12 | §2.1, §5.5 | `SKILL.md` section **Technique selection by uncertainty and ceremony**; `fixtures/definition-technique-selection` records chosen and deliberately unused techniques and rejects completeness-only use |
| DR-M01 | §5.5 | `REL` decision-metadata fields carrying the seven-field ownership record from `lifecycle-onepager.md` (§5.3); finalize refusal of a group-only owner (RTS-07) |
| DR-M02 | §5.5 | Specialist-participation finalize check: named specialist input present, or explicit `DEC#` skip with `OPEN:` gap (RTS-08) |
| DR-M03 | §2, §5.5 | Strategy-order selection gate plus `DEC#` exception/reorder path and index-refresh fixture |
| DR-M04 | §2.2 (LNT-14), §5.3, §5.5 | Conditional now/next/later maintenance; RTS-13 adopt/skip fixtures |
| DR-M05 | §4, §5.5 | Backtracking matrix vision route requiring evidence-citing `DEC#`; RTS-11/RTS-12 fixtures |
