# `discover-product` — contribution and coverage assurance

**Status:** Authoring contract  
**Applies to:** `discover-product`  
**Plan:** [Product discovery and requirements skillset plan](./prod_discovery_requirements_skillset_plan.md)  
**External analysis:** [Existing GitHub skillsets — fit analysis](./github_skillsets.md)

## Purpose and scope

This file ensures that `discover-product` incorporates the strongest relevant material from the reviewed GitHub skillsets without surrendering the proprietary traceability spine or method contract.

The skill is authoring-complete only when all seven discovery-loop phases are implemented; solution alternatives and the `SOL#` trace layer are explicit; all assigned donor material has been inspected and dispositioned; evidence quality, opportunity routing, experiment design, handover, deterministic validation, and end-to-end validation are verifiable; and the agent cannot fabricate evidence or decisions.

Allowed dispositions are **Adopt**, **Adapt**, **Call**, **Reject**, **Defer**, and **Pending audit**. Any Pending audit item blocks completion.

Contribution IDs are stable. New findings receive new IDs; existing IDs must not be renumbered or reused.

## Contribution ledger

| ID | Source contribution | Source | Mode | Required incorporation or decision | Disposition | License / dependency constraint | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DP-001 | Outcome-setting, opportunity mapping, solution ideation, and assumption testing workflows | `huntsyea/product-skills` — `continuous-discovery` | Distill | Audit all relevant references/workflows; distill useful techniques and phase anti-patterns while preserving the method’s seven-step sequence | Adopt subject to source audit | MIT; vendor selected material with source path, pinned revision, attribution, and date | Source manifest maps each distilled item to its destination and test |
| DP-002 | JTBD switch-interview and forces techniques | `huntsyea/product-skills` — `jobs-to-be-done` | Distill | Use optionally when uncertainty concerns motivation, switching, alternatives, or workarounds | Adopt subject to source audit | MIT; attribution required | Technique-routing fixture recommends JTBD only for appropriate uncertainty and records past behavior |
| DP-003 | Phase-specific discovery anti-pattern catalogue | `huntsyea/product-skills` references | Distill | Map every relevant anti-pattern to a prompt guardrail, finalize check, exclusion, or explicit rejection | Adopt subject to source audit | MIT | Anti-pattern coverage table has no unassigned relevant item |
| DP-004 | Past-behavior interviewing / Mom Test guardrails | `assimovt/productskills` — `user-interview` | Distill | Ask for concrete recent behavior; distinguish stories/actions/facts from opinions and hypothetical enthusiasm | Adopt subject to source audit | MIT | Fixtures classify hypothetical enthusiasm as weak and never create an `EV#` without a supplied source |
| DP-005 | Problem-validation rubric | `assimovt/productskills` — `problem-validation` | Distill | Consider frequency, intensity, and willingness to pay or a justified substitute; do not treat the rubric as universal certainty | Adapt subject to source audit | MIT | Fixture records applicability and avoids unsupported confidence |
| DP-006 | Opportunity-mapping guardrails | `assimovt/productskills` — `opportunity-mapping` | Distill | Compare against the proprietary `OPP#` model and incorporate useful solution-neutrality/hierarchy checks | Adapt subject to source audit | MIT | Audit records each guardrail as incorporated, redundant, or rejected with reasons; the ledger row itself is not left pending |
| DP-007 | Experiment-design guardrails | `assimovt/productskills` — `experiment-design` | Distill | Improve method selection, criteria, and decision linkage without replacing the proprietary `EXP#` schema | Adopt subject to source audit | MIT | Every `EXP#` carries the complete eleven-field schema: decision to inform, explicit assumption/hypothesis, target `ASM#`, applicable `SOL#`, evidence needed, method, time budget, predeclared support/refute/inconclusive criteria, result, confidence per relevant risk dimension, and resulting `DEC#` |
| DP-008 | Interview-quality rubric: Rich / Mixed / Thin | `jacksoncalling/argo-continuous-discovery` | Pattern | Define a rubric for story quality versus opinion and classify every interview-derived `EV#` | Adapt | License not established by comparison; pattern only unless verified | Golden fixtures classify representative evidence consistently |
| DP-009 | Confidence capped by evidence quality | `jacksoncalling/argo-continuous-discovery` | Pattern | Prevent quantity of weak evidence from producing high confidence; exceeding the evidence ceiling needs an explicit `DEC#` override | Adapt | Pattern only; independently specify rules | Test proves that three Thin items do not mechanically become Rich evidence |
| DP-010 | Opportunity routing: add / merge / escalate / park | `jacksoncalling/argo-continuous-discovery` | Pattern | Require a routing decision when evidence yields an opportunity; preserve provenance on merge and reasons on park/escalate | Adapt | Pattern only | Fixture verifies all four routes and their `EV#` links |
| DP-011 | Human gate before solutioning | `jacksoncalling/argo-continuous-discovery` | Pattern | Do not silently convert evidence into solutions; confirm the selected opportunity or mark AFK proposals as awaiting review | Adapt | Pattern only | Interview and AFK fixtures demonstrate the gate and authority |
| DP-012 | At least three materially different solution directions | Argo solution phase; huntsyea ideation; phuryn brainstorming chain | Pattern / distill | Generate multiple alternatives for a selected `OPP#`, including process, policy, manual-service, and no-build where meaningful; record as `SOL#` | Adopt | Respect each donor license; independently implement the convergent method requirement | Finalize blocks one solution unless an explicit `DEC#` explains why alternatives are not meaningful |
| DP-013 | Explicit `SOL#` trace layer | Gap analysis plus method-doc step 4 | Proprietary correction | Add `SOL#`; solution cites `OPP#`; solution-specific `ASM#` cites `SOL#`; solution-independent assumptions may cite `OPP#`; every `EXP#` carries explicit assumption/hypothesis content, cites its target `ASM#` and applicable `SOL#`, carries the complete DP-014 card, and records the resulting `DEC#` when the decision is made | Adopt | Proprietary | LNT-07 validates the `OPP → SOL → ASM → EXP` citations; LNT-19 validates the complete card including its explicit hypothesis and resulting `DEC#`; dangling links or missing required fields fail |
| DP-014 | Hypothesis/experiment file format | `shinpr/claude-code-discover` | Pattern | Merge the method card with the spine as eleven fields: decision to inform, explicit assumption/hypothesis, target `ASM#`, applicable `SOL#`, evidence needed, method, time budget, predeclared support/refute/inconclusive criteria, result, confidence per relevant risk dimension, and resulting `DEC#` | Adapt | MIT | LNT-19 schema verification requires all eleven fields, requires the assumption/hypothesis to be resolved, permits canonical `OPEN:` only for result, per-risk confidence, and resulting `DEC#` until the experiment and decision occur, and relies on LNT-03/LNT-07 for citation resolution |
| DP-015 | Context-separated critical review | `shinpr/claude-code-discover` hypothesis verifier | Pattern | Use a separated critic for derived maps/cards where useful; critic checks traceability and unsupported certainty without inventing evidence | Adapt for discovery; primary use remains in `specify-requirements` | MIT | AFK fixture gives the critic artifacts/rules but not builder expectations |
| DP-016 | Auto-maintained index discipline | `shinpr/claude-code-discover` | Pattern | Keep all `EV/OPP/SOL/ASM/EXP/DEC` records discoverable through the plan’s workspace/index mechanism | Adapt | MIT | Linter/index test detects an unindexed artifact |
| DP-017 | Chained workflow and next-step handover | `phuryn/pm-skills` | Pattern | At wrap-up, name proceed/adapt/pause/abandon, next selected lifecycle stage, and exact input artifacts | Adapt | MIT; no wholesale installation | Each verdict fixture produces an appropriate handover |
| DP-018 | Preferred-solution validation warning and failure-mode coaching | `deanpeters/Product-Manager-Skills` discovery material | Pattern / reference only | Independently author prompts that surface premature convergence; do not distill its questions or text | Adapt | CC BY-NC-SA 4.0; no copying/distillation | Reference-only audit passes; preferred-solution fixture triggers alternatives guardrail |
| DP-019 | Cheapest trustworthy test | Method docs, strengthened by reviewed discovery packs | Pattern / distill | Select method by riskiest assumption and evidence needed; allow prototype, concierge/Wizard-of-Oz, spike, data analysis, demand test, policy/security/legal review, or pilot | Adopt | Proprietary orchestration; donor content follows license | Fixtures cover all four risks and reject impressive but non-diagnostic tests |
| DP-020 | `prototype` handoff | Existing proprietary skill | Call / reuse | Call only when a prototype is the smallest trustworthy test; pass and return the complete eleven-field `EXP#` card, including its explicit assumption/hypothesis, target `ASM#`, applicable `SOL#`, predeclared criteria, decision context, result fields, and resulting `DEC#` field | Call | Internal dependency; pin compatible contract — the pin names the local `prototype` skill and its version/commit in the skills repo at authoring; contract changes reopen this row | Integration test returns findings to the same `EXP#`, preserves every card field, and requires recorded observation before treating output as evidence; result, per-risk confidence, and resulting `DEC#` follow the LNT-19 open-marker policy. Fallback (added in revision-contract update 4): when `prototype` is unavailable or its contract is incompatible, the gap is recorded on the `EXP#` and the skill selects the next-cheapest trustworthy method per DP-019 (concierge, Wizard-of-Oz, spike, demand test, …) or the human runs the prototype step manually; the experiment card records the substitution — the call is never silently skipped and no evidence is fabricated |
| DP-021 | Early quality-attribute risk surfacing | Proprietary quality method | Policy | Ask which qualities could change architecture or invalidate a solution; record them as appropriately classified assumptions | Adopt | Proprietary | Fixture surfaces security/reliability/latency risk without prematurely writing final `QAS#` |
| DP-022 | Domain-work trigger | Proprietary domain method and `domain-modeling` | Call / reuse | Invoke/recommend domain work when contested terminology, rules, ownership, events, or boundaries affect discovery | Call | Internal dependency; pinning (added in revision-contract update 4): the pin names the local `domain-modeling` skill and its version/commit in the skills repo at authoring; contract changes reopen this row | Fixture updates canonical domain artifacts rather than creating a competing glossary. Fallback (added in revision-contract update 4): when `domain-modeling` is unavailable, the skill recommends a manual domain-modeling session and records the contested term/rule/boundary as an explicit `OPEN:` marker on the affected artifact; discovery continues without inventing domain rulings, and canonical domain artifacts stay authoritative |
| DP-023 | Deterministic traceability validation | Problem-Based-SRS validation pattern plus gap analysis | Pattern / shared script | Run the shared linter at finalize; validate IDs, citations, source-bearing `EV#`, the LNT-07 `SOL#` chain, the complete eleven-field LNT-19 `EXP#` card including its required-resolved explicit assumption/hypothesis and resulting `DEC#`, and reserved names | Adopt | Problem-Based-SRS is MIT; linter remains proprietary | Mutation tests demonstrate each citation, field-completeness (including a missing hypothesis), open-marker, and reserved-name violation is detected |
| DP-024 | Explicit backtracking/reopen triggers | `ForceInjection/domain-driven-design-skills` | Pattern | Turn proceed/adapt/pause/abandon into explicit next-stage or reopen instructions tied to artifacts and conditions | Adapt | Pattern only unless license confirmed | Adapt fixture reopens a named `SOL#` or `ASM#` rather than restarting indiscriminately |
| DP-025 | Blind-run validation against a canonical case | `ForceInjection/domain-driven-design-skills` | Pattern | Run discovery against a fixed reference topic and score method checks, ledger rules, and deliberate failures | Adapt | Pattern only | Versioned report gives every failure a disposition |
| DP-026 | External dependency and source policy | Cross-cutting finding | Policy | Distilled files carry source path, revision, license, attribution, and date; calls are pinned; no live fetching | Adopt | Mandatory | Source/dependency manifest passes review |
| DP-027 | Full focused donor audit | Coverage assurance requirement | Authoring process | Inspect assigned skill/reference/workflow files, not only READMEs or summary; add every relevant candidate to this ledger | Adopt | Verify license before copying | No required path remains uninspected and no candidate remains Pending audit |
| DP-028 | Evidence non-fabrication | Proprietary invariant | Policy | Agent may organize, classify, question, and challenge evidence but may not create an observation or source not supplied by a human or actual system | Adopt | Mandatory | Adversarial test leaves missing evidence as an explicit gap |
| DP-029 | Preserve one proprietary spine | Cross-cutting finding | Policy | Do not import donor IDs, folders, PRDs, `tree.html`, or pipeline taxonomies; adapt mechanisms to `EV/OPP/SOL/ASM/EXP/DEC` | Adopt | Mandatory | Output/dependency audit finds no competing graph |
| DP-030 | Decision thresholds prevent endless research | Method failure mode, reinforced by timeboxed external flows | Policy | Define before testing what evidence causes proceed/adapt/pause/abandon and when research stops | Adopt | Proprietary | Endless-research fixture cannot complete without thresholds or explicit open decision |
| DP-031 | Alternative and rejected-direction memory | Method requirement plus shinpr rejected-alternative pattern | Pattern | Preserve considered solutions, rejection/defer reasons, and supporting evidence so later sessions do not rediscover them as new | Adapt | MIT for shinpr; proprietary IDs remain authoritative | Fixture verifies rejected `SOL#` remains traceable and is not silently deleted |
| DP-M01 | Discovery pivot vs. vision pivot | [product_vision.md](../product_vision.md), [product_discovery.md](../product_discovery.md), revision-contract update 10 | Method-owned policy | Every adapt decision is a discovery pivot within a stable vision; never edit the vision. Route only intended-future/target-need-invalidating evidence to `brainstorm-vision` through an explicit `DEC#`; refuse and reroute failed experiments or weak features (plan §4, §5.4) | Adopt | Proprietary method docs; no external license | RTS-11 refused/rerouted with vision untouched; RTS-12 genuine route passes only with evidence-citing `DEC#` |
| DP-M02 | Opportunity selection vs. thin ordered-outcomes strategy | [product_vision.md](../product_vision.md), revision-contract update 10 | Method-owned policy | Read the companion-derived strategy index; selecting against the order needs an explicit `DEC#` exception or reorder. A reorder is a discovery pivot applied by the accountable human owner and followed by companion refresh, never a companion or vision pivot (plan §2, §5.4) | Adopt | Proprietary method doc; no external license | Off-strategy selection blocks without `DEC#`; reorder fixture records the decision, updates the field set, and refreshes the index |
| DP-M03 | Singular accountable decision ownership: the owner of every proceed/adapt/pause/abandon `DEC#` is one named accountable individual; a group, trio, or department is never an owner | [collaboration_and_decision_ownership.md](../collaboration_and_decision_ownership.md) (core rules 2–3, decision language) — method-owned, revision-contract update 9 | Method-owned policy | The `DEC#` owner field names the one accountable individual recorded in `lifecycle-onepager.md`'s decision-authority section (plan §5.3, §5.4); a group-, trio-, or department-valued owner is refused at decision time; the escalation path comes from the same one-pager record | Adopt | Proprietary method doc; no external license | Regression scenario RTS-07: a group-only owner is detected and refused; fixture rejects a `DEC#` whose owner is not a named individual |
| DP-M04 | Required specialist participation: material feasibility/viability/quality evidence requires actual engineering/design/operations/security/compliance/domain input; the agent never fabricates specialist evidence | [collaboration_and_decision_ownership.md](../collaboration_and_decision_ownership.md) (core rules 4–5, collaboration across the lifecycle) — method-owned, revision-contract update 9 | Method-owned policy | When a decision's feasibility, viability, or quality evidence is material, the named specialist authorities from `lifecycle-onepager.md` supply it (plan §5.3, §5.4); the missing input stays an explicit `OPEN:` gap and the decision is refused until the input is supplied or the accountable owner records the gap in the `DEC#` — extends DP-021's classified-assumption discipline and DP-028's evidence non-fabrication | Adopt | Proprietary method doc; no external license | Regression scenario RTS-08: missing required specialist/engineering input is detected and refused; adversarial fixture leaves the gap as an explicit `OPEN:` marker, never invented specialist evidence |

### FIT disposition trace — stage-document source classification

This trace closes a source-classification warning rather than adding a skill contribution, so the stable FIT key is retained and no new `DP-*` mechanism is introduced.

| FIT key | Final disposition | Completed trace | Authority / license boundary |
| --- | --- | --- | --- |
| `FIT-2-dddcrew-02` | **Adapt** | [`domain_discovery.md`](../domain_discovery.md) now classifies `ddd-crew/ddd-starter-modelling-process` as a human modelling-process reference, separately from agent rule sets | Canonical domain artifacts remain under existing domain authority and design work remains deferred to the future design skillset; CC BY 4.0 attribution is required if content is ever used, and no copying or distillation is scheduled |

## Focused external source-audit manifest

Before authoring can pass, inspect and record pinned revisions and relevant paths for:

| Repository | Required audit scope | Audit objective |
| --- | --- | --- |
| `huntsyea/product-skills` | Complete `continuous-discovery` and `jobs-to-be-done` skill, reference, and workflow trees, especially outcome, opportunities, ideation, assumptions, interviews, and anti-patterns | Inventory every useful technique, checklist, rubric, guardrail, failure mode, and completion signal |
| `assimovt/productskills` | `user-interview`, `problem-validation`, `opportunity-mapping`, and `experiment-design` | Identify concise guardrails suitable for the minimum-ceremony path |
| `jacksoncalling/argo-continuous-discovery` | Interview assessment, opportunity extraction/routing, human gate, solution phase, and experiment cards | Specify evidence-quality, confidence-cap, routing, and alternative mechanisms independently |
| `shinpr/claude-code-discover` | Hypothesis format, verifier separation, rejected alternatives, and index maintenance | Strengthen `EXP#`, critic separation, alternative memory, and discoverability |
| `phuryn/pm-skills` | `/discover` and underlying ideate, assumption, prioritization, experiment, and handover commands | Identify workflow/handover improvements without importing the marketplace |
| `deanpeters/Product-Manager-Skills` | Discovery workflow and failure-mode descriptions | Reference-only audit; prove no protected material was distilled |
| `RafaelGorski/Problem-Based-SRS` | Mechanical validation and trace checks | Inform linter architecture, not its ID taxonomy |
| `ForceInjection/domain-driven-design-skills` | Backtracking triggers, validation checklists, and blind-run scoring | Inform re-entry and skillset validation patterns |

For each file record repository/URL, pinned commit/tag/release, path, date, license/attribution, candidate contribution, destination, disposition/reason, and verification. Newly discovered relevant candidates receive new `DP-*` IDs.

## Method-document coverage ledger

| ID | Method source | Required coverage in `discover-product` | Verification |
| --- | --- | --- | --- |
| DP-MTH-01 | [Product discovery](../product_discovery.md) — four risks | Classify assumptions across value, usability, feasibility, and viability; allow multiple dimensions | Fixtures include all four risks and cross-cutting assumptions |
| DP-MTH-02 | Product discovery — 1. Frame an outcome | Start from observable/measurable change, why it matters, and to whom; reject feature requests as outcomes | Outcome fixture distinguishes outcome from output |
| DP-MTH-03 | Product discovery — 2. Gather evidence | Support interviews, observation, analytics/support/search/workarounds, journeys, alternatives research, and expert/stakeholder evidence; prefer past behavior | Evidence fixtures cover source types and quality levels |
| DP-MTH-04 | Product discovery — 3. Map opportunities | Record needs, pains, desires, and obstacles under an outcome; keep `OPP#` solution-neutral | Critic flags feature-shaped opportunities |
| DP-MTH-05 | Product discovery — 4. Generate alternatives | Create materially different `SOL#` directions, including non-software/no-build where meaningful | Finalize requires alternatives or explicit `DEC#` exception |
| DP-MTH-06 | Product discovery — 5. Expose assumptions | Attach assumptions to solutions or, when solution-independent, opportunities; rank by importance and lack of evidence | Schema/fixtures verify anchors and ranking |
| DP-MTH-07 | Product discovery — 6. Test cheaply | Select the smallest trustworthy test and preregister support/refute/inconclusive criteria | Card and method-selection fixtures pass |
| DP-MTH-08 | Product discovery — 7. Decide and record | Record proceed/adapt/pause/abandon, evidence strength, remaining uncertainty, and next decision | Every increment ends with `DEC#` and handover |
| DP-MTH-09 | Product discovery — artifacts | Treat optional artifacts as thinking tools selected by tailoring while preserving mandatory trace records | Low-ceremony fixture avoids unnecessary artifacts without breaking traceability |
| DP-MTH-10 | Product discovery — experiment card | Preserve the complete merged card: decision to inform, explicit assumption/hypothesis from the method card's `## Assumption`, target `ASM#`, applicable `SOL#`, evidence needed, method, time budget, predeclared support/refute/inconclusive criteria, result, confidence per relevant risk dimension, and resulting `DEC#` | LNT-19 rejects a missing or unresolved hypothesis; the full schema and LNT-03/LNT-07 citation checks pass |
| DP-MTH-11 | Product discovery — failure modes | Guard against preferred-solution validation, users designing the product, opinion inflation, low-risk testing, unused maps, separation from delivery, and endless research | Every failure mode maps to an instruction and adversarial test |
| DP-MTH-12 | Product discovery — completion checks | Explicit outcome/opportunity; visible ranked assumptions; proportionate evidence; alternatives; success/guardrail measures; visible uncertainty | Scored report has one result per check |
| DP-MTH-13 | [Domain discovery](../domain_discovery.md) | Trigger domain work for contested language, rules, events, ownership, hotspots, and boundaries; keep canonical artifacts outside loop workspace | Fixture calls `domain-modeling` without duplicating glossary |
| DP-MTH-14 | [Quality attributes](../quality_attributes.md) | Surface architecture-changing quality risks during discovery; explore consequences/trade-offs without finalizing `QAS#` | Fixture records early quality assumptions and hands them forward |
| DP-MTH-15 | [Resources](../resources.md) | Route uncertainty to an appropriate technique and adopt it only when it improves a decision | Technique-selection fixtures pass |
| DP-MTH-16 | [Glossary](../glossary.md) | Use outcome, evidence, opportunity, solution, assumption, experiment, signal, success, guardrail, and stop criteria consistently | Terminology audit passes; add canonical solution-candidate terminology if needed |
| DP-MTH-17 | [Overview](../overview.md) | Support the minimum useful discovery package and carry evidence toward readiness for design | End-to-end topic retains visible uncertainty and evidence-supported scope |
| DP-MTH-18 | [Product vision](../product_vision.md) | Check targeted opportunities against the thin ordered-outcomes strategy; distinguish routine discovery pivots from `DEC#`-gated vision re-entry | Off-strategy, RTS-11, and RTS-12 fixtures pass |
| DP-MTH-19 | [Lifecycle tailoring](../lifecycle_tailoring.md) | Read `lifecycle-onepager.md`, respect selected artifacts/cadence/authority, and record deliberate deviation | Low- and high-ceremony fixtures pass |
| DP-MTH-20 | [GitHub skillset analysis](./github_skillsets.md) + [revision contract](./skillset_plan_update_plan.md) | Apply all relevant integration items, the three gap corrections (ordered updates 1–3), dependency rules, source audit, and validation | Ledger has no undecided row |
| DP-MTH-21 | [Skillset plan](./prod_discovery_requirements_skillset_plan.md) | Seed from vision/companion; maintain proprietary IDs; call internal skills only through defined handoffs; end with lifecycle-aware next step | End-to-end trace/handover tests pass |

## Required artifact and trace contract

| Artifact / record | Required trace |
| --- | --- |
| `EV#` | Human- or system-supplied source, date, evidence type, quality/strength, relevant actor/context |
| `OPP#` | Desired outcome and relevant vision/actor IDs; supporting `EV#`; routing decision |
| `SOL#` | Selected `OPP#`; materially distinct direction; product/process/policy/manual/no-build category where relevant |
| `ASM#` | Risk class(es), importance, evidence status, and `SOL#` anchor, or `OPP#` when genuinely solution-independent |
| `EXP#` | Decision to inform; explicit assumption/hypothesis; target `ASM#`; applicable `SOL#`; evidence needed; method; time budget; predeclared support/refute/inconclusive criteria; result; confidence per relevant risk dimension; resulting `DEC#` |
| `DEC#` | Owner, proceed/adapt/pause/abandon verdict, supporting evidence/strength, remaining uncertainty, and artifact/stage reopened or handed to |

The shared linter validates code-checkable parts. The critic and human review cover judgment such as whether alternatives are materially different or evidence is trustworthy.

## Objective authoring coverage gate

`discover-product` is authoring-complete only when all of the following are true:

- [ ] Every contribution row has a stable `DP-*` ID.
- [ ] Every contribution has a final disposition; none remains Pending audit.
- [ ] Every rejection/deferral has a reason; every deferral names an owner.
- [ ] Every donor path was inspected at a pinned revision.
- [ ] Every distilled item records source, path, revision, date, license, attribution, destination, and verification.
- [ ] No deanpeters content was copied or distilled.
- [ ] Argo or ForceInjection use beyond independently implemented patterns passed license review.
- [ ] All seven discovery phases exist in documented order or have an explicit tailoring rule.
- [ ] `SOL#` exists in the ID inventory, artifact model, companion reservation, trace model, linter, and fixtures.
- [ ] At least three materially different directions are generated unless an explicit `DEC#` explains why not.
- [ ] Process, policy, manual-service, and no-build alternatives are considered where applicable.
- [ ] `ASM#` cites `SOL#` except documented solution-independent assumptions citing `OPP#`.
- [ ] Every `EXP#` cites its target `ASM#` and the applicable `SOL#`; both citations resolve under LNT-03/LNT-07.
- [ ] Every `EXP#` contains the complete eleven-field card: decision to inform, explicit assumption/hypothesis, target `ASM#`, applicable `SOL#`, evidence needed, method, time budget, predeclared support/refute/inconclusive criteria, result, confidence per relevant risk dimension, and resulting `DEC#`; the first eight fields are required-resolved, so a missing or `OPEN:` hypothesis fails, and only result, per-risk confidence, and resulting `DEC#` may carry canonical `OPEN:` markers until the experiment and decision occur (LNT-19).
- [ ] Every `EV#` has a real human- or system-supplied source and date.
- [ ] Rich/Mixed/Thin or its final equivalent has reproducible examples.
- [ ] Confidence is capped by evidence quality.
- [ ] Opportunity routing supports add, merge, escalate, and park while preserving provenance.
- [ ] Human gate before solution generation is explicit; AFK proposals remain visibly unconfirmed.
- [ ] Every method failure mode maps to a guardrail and adversarial test.
- [ ] Every method completion check appears in the finalize rubric.
- [ ] Early quality risks are surfaced and handed forward without becoming disguised requirements.
- [ ] Domain ambiguity routes to canonical artifacts through `domain-modeling`.
- [ ] `prototype` handoff passes and returns the same IDs and criteria.
- [ ] Linter detects duplicate/malformed IDs, dangling citations, source-less `EV#`, invalid `OPP/SOL/ASM/EXP` links, missing card fields, and reserved-name collisions.
- [ ] Judgment review is distinct from deterministic output.
- [ ] Wrap-up records verdict, remaining uncertainty, and lifecycle-aware next step.
- [ ] Canonical reference topic ran in interview and AFK/light-derive modes.
- [ ] Reference scoring uses every applicable completion check and ledger invariant.
- [ ] Mutation tests catch preferred-solution bias, hypothetical enthusiasm, weak-evidence inflation, low-risk testing, endless research, and fabricated evidence.
- [ ] Every failed reference/mutation test caused a revision or accepted exception.
- [ ] Opportunity selection follows the derived strategy order or cites a `DEC#` exception/reorder; discovery never silently edits the vision.
- [ ] No donor workspace, PRD taxonomy, HTML tree, foreign IDs, or competing spine was introduced.
- [ ] License and attribution review passes.

Any unchecked item blocks “authoring complete.”

## Exclusions and deferrals

- Do not adopt Argo’s folder layout, single-outcome operator, demo data, or `tree.html`.
- Do not adopt shinpr’s competing artifact taxonomy, PRD pipeline, vision/persona/blueprint stages, or design workflow.
- Do not install the full phuryn marketplace.
- Do not copy or distill deanpeters material.
- Do not fabricate interviews, observations, analytics, sources, results, or confidence.
- Do not equate repeated weak opinions with strong evidence.
- Do not let the agent silently choose a solution for the decision owner.
- Do not turn early quality concerns into final `QAS#`; `specify-requirements` owns them.
- Do not commit release scope; `define-release` owns it.
- Do not elaborate full use cases or requirements; `specify-requirements` owns them.
- Do not perform design, architecture, implementation planning, or UI exploration beyond a bounded `prototype` experiment.
- Story mapping, Shape Up, scope cutting, bet sizing, and Obligation/Expectation/Hope belong to `define-release`.
- North-star metric auditing belongs to `define-release` and `validate-release`.
- NFR review and quality-scenario writing belong to `specify-requirements`.
- Post-release analysis planning belongs to `validate-release`.
- Tactical DDD, architecture, EventStorming-to-design workflows, and design catalogs remain deferred to the future design skillset.

## Plan-to-authoring traceability (revision-contract update 8)

Maps every accepted row to its plan location and **planned** skill-file destination (paths relative to the future `skills/discover-product/` directory; the skill is not authored yet). Governing rules — replace-planned-with-actual, reopen, date capture, post-authoring reconciliation — are in [plan §3.3](./prod_discovery_requirements_skillset_plan.md), whose donor-audit task table carries this ledger's nine distill rows (DP-001..DP-007, DP-012, DP-019). **Date capture:** no row records a pinned commit/retrieval date yet; executing the eight-repo source-audit manifest above with full provenance fields is an explicit authoring-time task (plan §3.3). The keyed method-coverage rows DP-MTH-01..21 each have their own plan location, planned file/section, and objective fixture, linter check, or regression target below.

| Row | Plan § | Planned destination (path/section) |
| --- | --- | --- |
| DP-001 | §3.2, §3.3, §5.4 | Vendored technique/anti-pattern reference sub-files (per-phase, with provenance headers) + source manifest |
| DP-002 | §3.3, §5.4 | Optional JTBD lens reference + technique-routing rule (motivation/switching uncertainty only) |
| DP-003 | §3.3, §5.4 | Anti-pattern coverage table (reference file) mapping each item to guardrail/finalize check/rejection |
| DP-004 | §3.3, §5.4 | Evidence-gathering phase guardrails (past-behavior prompts); weak-evidence classification fixtures |
| DP-005 | §3.3, §5.4 | Problem-validation rubric in the evidence/opportunity assessment phase, with applicability limits |
| DP-006 | §3.3, §5.4 | Solution-neutrality/hierarchy checks merged into the `OPP#` mapping phase; per-guardrail disposition table from the audit |
| DP-007 | §3.3, §5.4 | Experiment-card design guidance inside `experiments/EXP<n>.md`; complete eleven-field schema, including required-resolved explicit assumption/hypothesis, exposed to LNT-19, with target `ASM#`/applicable `SOL#` citations exposed to LNT-03/LNT-07 and resulting `DEC#` retained |
| DP-008, DP-009 | §2 (`evidence-log.md`), §5.4, LNT-18 | Rich/Mixed/Thin rubric reference + confidence-cap rule with `DEC#` override; golden fixtures |
| DP-010, DP-011 | §2 (`opportunities.md`), §5.4 | Opportunity-routing step (add/merge/escalate/park) + human gate before solutioning; AFK awaiting-review marker |
| DP-012 | §2 (`solutions.md`), §3.3, §5.4 | Generate-alternatives phase (≥3 materially different directions); ranking-time + finalize refusal (RTS-04) |
| DP-013 | §2, §2.2 (LNT-07, LNT-19), §5.4 | `solutions.md`, `assumptions.md`, and `experiments/EXP<n>.md` trace fields: `OPP# → SOL# → ASM# → EXP#`, the experiment's explicit assumption/hypothesis, applicable `SOL#`, and resulting `DEC#`; chain/card validation wired to the shared linter |
| DP-014 | §2 (`experiments/EXP<n>.md`), §2.2 (LNT-19), §5.4 | Merged eleven-field experiment-card template: decision to inform, explicit assumption/hypothesis, target `ASM#`, applicable `SOL#`, evidence needed, method, time budget, predeclared support/refute/inconclusive criteria, result, confidence per relevant risk dimension, resulting `DEC#` |
| DP-015 | §5.4 | Separated-critic instructions for derived maps/cards (artifacts + rules, no builder expectations) |
| DP-016 | §5.4, LNT-04 | Workspace-index maintenance step; unindexed-artifact detection |
| DP-017 | §4.1, §5.4 | Wrap-up handover section (verdict, next stage, exact input artifacts) |
| DP-018 | §5.4 | Independently authored premature-convergence prompts; reference-only audit record |
| DP-019 | §3.1 (prototype fallback), §3.3, §5.4 | Cheapest-trustworthy-test method-selection guidance (all four risks) |
| DP-020 | §3.1, §5.4 | `prototype` call contract wiring: pass/return the same complete eleven-field `EXP#` card, including explicit assumption/hypothesis, target `ASM#`, applicable `SOL#`, predeclared criteria, result/confidence fields, and resulting `DEC#` field; fallback per §3.1 |
| DP-021 | §5.4 | Early quality-risk prompt producing classified assumptions (not `QAS#`) |
| DP-022 | §3.1, §4.2 (condition 7), §5.4 | `domain-modeling` call contract wiring + fallback per §3.1 |
| DP-023 | §2.2, §5.4 | Finalize linter invocation (LNT-01, LNT-03–07, LNT-18, LNT-19), including `EXP#` target/applicable citations, complete eleven-field cards, required-resolved explicit hypotheses, and resulting `DEC#`; missing-hypothesis mutation test |
| DP-024 | §4.2, §5.4 | Adapt-verdict reopen instructions naming affected `SOL#`/`ASM#` (route schema per §4.2) |
| DP-025 | §6, §5.4 | Blind reference-topic run + scored report (feeds the §6 regression suite) |
| DP-026 | §3.2, §5.4 | Skill source/dependency manifest (provenance on distilled files, pinned calls, no live fetch) |
| DP-027 | §3.3 | Executed donor-audit manifest (the eight-repo table above); new candidates get new `DP-*` IDs |
| DP-028 | §5.4 | Evidence non-fabrication guardrail; adversarial fixture leaves gaps explicit |
| DP-029 | §5.4 | Single-spine guardrail: no donor IDs/folders/taxonomies; output/dependency audit |
| DP-030 | §5.4 | Predeclared decision-threshold prompts; endless-research fixture |
| DP-031 | §2 (`solutions.md`) | Rejected/parked-`SOL#` retention rules in the solutions template; linter-visible |
| DP-MTH-01 | §2.1, §5.4, §6 | `SKILL.md` section **Four-risk assumption classification** plus `references/assumption-rubric.md`; `fixtures/four-risks` covers value, usability, feasibility, viability, and a multi-risk assumption |
| DP-MTH-02 | §2.1, §5.4, §6 | `SKILL.md` phase **Frame an outcome**; `fixtures/outcome-vs-output` rejects a feature request as an outcome and requires actor, observable change, and rationale |
| DP-MTH-03 | §2 (`evidence-log.md`), §2.1, §2.2 (LNT-06, LNT-18), §5.4, §6 | `SKILL.md` phase **Gather evidence** plus `references/evidence-quality.md`; `fixtures/evidence-sources-and-strength` covers named source types and RTS-03 weak-evidence/confidence-cap mutations |
| DP-MTH-04 | §2 (`opportunities.md`), §2.1, §5.4 | `SKILL.md` phase **Map opportunities** and the `OPP#` template section **Solution-neutral wording**; `fixtures/feature-shaped-opportunity` requires the critic to reject a disguised solution |
| DP-MTH-05 | §2 (`solutions.md`), §2.1, §2.2 (LNT-07), §5.4, §6 | `SKILL.md` phase **Generate alternatives** and `solutions.md` template guidance; RTS-04 plus `fixtures/materially-different-solutions` requires three directions or a cited exception `DEC#` |
| DP-MTH-06 | §2 (`assumptions.md`), §2.1, §2.2 (LNT-07), §5.4, §6 | `SKILL.md` phase **Expose and rank assumptions** plus the `ASM#` template; `fixtures/assumption-anchors-and-ranking` checks `SOL#`/solution-independent `OPP#` anchors and ranking-time refusal |
| DP-MTH-07 | §2 (`experiments/EXP<n>.md`), §2.1, §2.2 (LNT-19), §3.1, §5.4 | `SKILL.md` phase **Test cheaply** plus `references/test-selection.md`; `fixtures/cheapest-trustworthy-test` covers all four risks and LNT-19 rejects a missing/unresolved hypothesis, post-hoc criteria, or missing budget |
| DP-MTH-08 | §2 (`decision-log.md`), §2.1, §§4.1–4.2, §5.4 | `SKILL.md` phase **Decide, record, and hand over**; `fixtures/discovery-verdicts` requires each verdict to write a `DEC#`, remaining uncertainty, and a route-aware handover |
| DP-MTH-09 | §2 (discovery artifacts), §2.1, §5.3, §5.4, §6 | `SKILL.md` section **Tailored artifact selection**; `fixtures/low-ceremony-discovery` proves optional tools may be skipped without losing mandatory trace records (RTS-01/RTS-02) |
| DP-MTH-10 | §2 (`experiments/EXP<n>.md`), §2.1, §2.2 (LNT-03, LNT-07, LNT-19), §5.4 | `references/experiment-card-template.md` with all eleven fields; `fixtures/experiment-card-schema` checks required/open-markable fields (including rejection of a missing hypothesis), citations, and resulting `DEC#` |
| DP-MTH-11 | §2.1, §5.4, §6 | `references/discovery-guardrails.md` section **Method failure modes**; `fixtures/discovery-failure-modes` has one adversarial test per listed failure and no unassigned failure mode |
| DP-MTH-12 | §2.1, §5.4, §6 (axis 1) | `references/finalize-rubric.md` section **Discovery completion checks**; `fixtures/discovery-completion-report` requires one scored result per check, including alternatives and visible uncertainty |
| DP-MTH-13 | §2.1, §3.1, §4.2 (condition 7), §5.4 | `SKILL.md` section **Domain-work trigger**; `fixtures/contested-domain-language` checks the pinned `domain-modeling` call/manual fallback and forbids a competing glossary |
| DP-MTH-14 | §2.1, §5.4 | `SKILL.md` section **Early quality-risk surfacing** plus `ASM#` risk-class prompts; `fixtures/architecture-changing-quality-risk` verifies handoff as an assumption and rejects premature `QAS#` creation |
| DP-MTH-15 | §2.1, §5.4 | `references/test-selection.md` section **Uncertainty-to-technique routing**; `fixtures/technique-selection` proves the chosen method improves the named decision and rejects ceremony/completeness-only choices |
| DP-MTH-16 | §2.1, §5.4 | `SKILL.md` section **Method terminology contract**; `fixtures/terminology-audit` checks outcome/evidence/opportunity/solution/assumption/experiment/signal/success/guardrail/stop meanings |
| DP-MTH-17 | §2.1, §4, §5.4, §6 | `SKILL.md` sections **Minimum discovery package** and **Readiness handoff**; reference-topic fixture `fixtures/discovery-to-readiness` preserves uncertainty and evidence-supported scope |
| DP-MTH-18 | §2 (strategy representation), §2.1, §4, §5.4, §6 | `SKILL.md` section **Strategy and pivot gate**; `fixtures/off-strategy-selection` plus RTS-11/RTS-12 require `DEC#`-gated divergence/vision re-entry and leave the vision untouched otherwise |
| DP-MTH-19 | §2.1, §4.1, §5.3, §5.4, §6 | `SKILL.md` start gate **Read lifecycle one-pager** and closing handover; `fixtures/tailoring-compliance` covers low/high ceremony, explicit deviation, skips, cadence, and authority (RTS-01/RTS-02/RTS-13) |
| DP-MTH-20 | §2.1, §§3.2–3.3, §5.4, §6 (axis 2) | `references/source-audit-manifest.md` plus `SKILL.md` authoring gate; `fixtures/contribution-coverage` fails an undecided row, absent ordered-update mechanism, missing provenance, or unpinned dependency |
| DP-MTH-21 | §2.1, §3.1, §4.1, §5.4, §6 | `SKILL.md` sections **Inputs**, **ID spine**, **Internal calls**, and **Handover**; reference-topic fixture `fixtures/discovery-end-to-end-trace` verifies companion seeds, proprietary IDs, bounded calls, and lifecycle-aware next step |
| DP-M01 | §4, §5.4 | Wrap-up pivot classifier and external `DEC#` vision-reentry route; RTS-11/RTS-12 fixtures |
| DP-M02 | §2, §5.4 | Opportunity-selection strategy check, explicit `DEC#` exception/reorder path, companion-index refresh fixture |
| DP-M03 | §5.4 | Decision-recording step: `DEC#` owner field bound to the one-pager's decision-authority record (§5.3); group-only owner refused at decision time (RTS-07) |
| DP-M04 | §5.4 | Decision guardrails: required specialist input per the one-pager's named specialist authorities; explicit `OPEN:` gap plus decision refusal when missing (RTS-08) |
