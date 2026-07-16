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
| DP-007 | Experiment-design guardrails | `assimovt/productskills` — `experiment-design` | Distill | Improve method selection, criteria, and decision linkage without replacing the proprietary `EXP#` schema | Adopt subject to source audit | MIT | Every `EXP#` cites a decision and assumption and preregisters support/refute/inconclusive outcomes |
| DP-008 | Interview-quality rubric: Rich / Mixed / Thin | `jacksoncalling/argo-continuous-discovery` | Pattern | Define a rubric for story quality versus opinion and classify every interview-derived `EV#` | Adapt | License not established by comparison; pattern only unless verified | Golden fixtures classify representative evidence consistently |
| DP-009 | Confidence capped by evidence quality | `jacksoncalling/argo-continuous-discovery` | Pattern | Prevent quantity of weak evidence from producing high confidence; exceeding the evidence ceiling needs an explicit `DEC#` override | Adapt | Pattern only; independently specify rules | Test proves that three Thin items do not mechanically become Rich evidence |
| DP-010 | Opportunity routing: add / merge / escalate / park | `jacksoncalling/argo-continuous-discovery` | Pattern | Require a routing decision when evidence yields an opportunity; preserve provenance on merge and reasons on park/escalate | Adapt | Pattern only | Fixture verifies all four routes and their `EV#` links |
| DP-011 | Human gate before solutioning | `jacksoncalling/argo-continuous-discovery` | Pattern | Do not silently convert evidence into solutions; confirm the selected opportunity or mark AFK proposals as awaiting review | Adapt | Pattern only | Interview and AFK fixtures demonstrate the gate and authority |
| DP-012 | At least three materially different solution directions | Argo solution phase; huntsyea ideation; phuryn brainstorming chain | Pattern / distill | Generate multiple alternatives for a selected `OPP#`, including process, policy, manual-service, and no-build where meaningful; record as `SOL#` | Adopt | Respect each donor license; independently implement the convergent method requirement | Finalize blocks one solution unless an explicit `DEC#` explains why alternatives are not meaningful |
| DP-013 | Explicit `SOL#` trace layer | Gap analysis plus method-doc step 4 | Proprietary correction | Add `SOL#`; solution cites `OPP#`; solution-specific `ASM#` cites `SOL#`; solution-independent assumptions may cite `OPP#`; `EXP#` tests named `ASM#` | Adopt | Proprietary | Linter validates `OPP → SOL → ASM → EXP` and reports dangling links |
| DP-014 | Hypothesis/experiment file format | `shinpr/claude-code-discover` | Pattern | Merge the method card with confidence per risk dimension and a time budget | Adapt | MIT | Schema verifies decision, assumption, evidence needed, method, budget, preregistered criteria, result/confidence, and next step |
| DP-015 | Context-separated critical review | `shinpr/claude-code-discover` hypothesis verifier | Pattern | Use a separated critic for derived maps/cards where useful; critic checks traceability and unsupported certainty without inventing evidence | Adapt for discovery; primary use remains in `specify-requirements` | MIT | AFK fixture gives the critic artifacts/rules but not builder expectations |
| DP-016 | Auto-maintained index discipline | `shinpr/claude-code-discover` | Pattern | Keep all `EV/OPP/SOL/ASM/EXP/DEC` records discoverable through the plan’s workspace/index mechanism | Adapt | MIT | Linter/index test detects an unindexed artifact |
| DP-017 | Chained workflow and next-step handover | `phuryn/pm-skills` | Pattern | At wrap-up, name proceed/adapt/pause/abandon, next selected lifecycle stage, and exact input artifacts | Adapt | MIT; no wholesale installation | Each verdict fixture produces an appropriate handover |
| DP-018 | Preferred-solution validation warning and failure-mode coaching | `deanpeters/Product-Manager-Skills` discovery material | Pattern / reference only | Independently author prompts that surface premature convergence; do not distill its questions or text | Adapt | CC BY-NC-SA 4.0; no copying/distillation | Reference-only audit passes; preferred-solution fixture triggers alternatives guardrail |
| DP-019 | Cheapest trustworthy test | Method docs, strengthened by reviewed discovery packs | Pattern / distill | Select method by riskiest assumption and evidence needed; allow prototype, concierge/Wizard-of-Oz, spike, data analysis, demand test, policy/security/legal review, or pilot | Adopt | Proprietary orchestration; donor content follows license | Fixtures cover all four risks and reject impressive but non-diagnostic tests |
| DP-020 | `prototype` handoff | Existing proprietary skill | Call / reuse | Call only when a prototype is the smallest trustworthy test; pass `EXP#`, `ASM#`, criteria, and decision context | Adopt | Internal dependency; pin compatible contract | Integration test returns findings to the same `EXP#` and requires recorded observation before treating output as evidence |
| DP-021 | Early quality-attribute risk surfacing | Proprietary quality method | Policy | Ask which qualities could change architecture or invalidate a solution; record them as appropriately classified assumptions | Adopt | Proprietary | Fixture surfaces security/reliability/latency risk without prematurely writing final `QAS#` |
| DP-022 | Domain-work trigger | Proprietary domain method and `domain-modeling` | Call / reuse | Invoke/recommend domain work when contested terminology, rules, ownership, events, or boundaries affect discovery | Adopt | Internal dependency | Fixture updates canonical domain artifacts rather than creating a competing glossary |
| DP-023 | Deterministic traceability validation | Problem-Based-SRS validation pattern plus gap analysis | Pattern / shared script | Run the shared linter at finalize; validate IDs, citations, source-bearing `EV#`, `SOL#` chains, `EXP#` fields, and reserved names | Adopt | Problem-Based-SRS is MIT; linter remains proprietary | Mutation tests demonstrate each violation is detected |
| DP-024 | Explicit backtracking/reopen triggers | `ForceInjection/domain-driven-design-skills` | Pattern | Turn proceed/adapt/pause/abandon into explicit next-stage or reopen instructions tied to artifacts and conditions | Adapt | Pattern only unless license confirmed | Adapt fixture reopens a named `SOL#` or `ASM#` rather than restarting indiscriminately |
| DP-025 | Blind-run validation against a canonical case | `ForceInjection/domain-driven-design-skills` | Pattern | Run discovery against a fixed reference topic and score method checks, ledger rules, and deliberate failures | Adapt | Pattern only | Versioned report gives every failure a disposition |
| DP-026 | External dependency and source policy | Cross-cutting finding | Policy | Distilled files carry source path, revision, license, attribution, and date; calls are pinned; no live fetching | Adopt | Mandatory | Source/dependency manifest passes review |
| DP-027 | Full focused donor audit | Coverage assurance requirement | Authoring process | Inspect assigned skill/reference/workflow files, not only READMEs or summary; add every relevant candidate to this ledger | Adopt | Verify license before copying | No required path remains uninspected and no candidate remains Pending audit |
| DP-028 | Evidence non-fabrication | Proprietary invariant | Policy | Agent may organize, classify, question, and challenge evidence but may not create an observation or source not supplied by a human or actual system | Adopt | Mandatory | Adversarial test leaves missing evidence as an explicit gap |
| DP-029 | Preserve one proprietary spine | Cross-cutting finding | Policy | Do not import donor IDs, folders, PRDs, `tree.html`, or pipeline taxonomies; adapt mechanisms to `EV/OPP/SOL/ASM/EXP/DEC` | Adopt | Mandatory | Output/dependency audit finds no competing graph |
| DP-030 | Decision thresholds prevent endless research | Method failure mode, reinforced by timeboxed external flows | Policy | Define before testing what evidence causes proceed/adapt/pause/abandon and when research stops | Adopt | Proprietary | Endless-research fixture cannot complete without thresholds or explicit open decision |
| DP-031 | Alternative and rejected-direction memory | Method requirement plus shinpr rejected-alternative pattern | Pattern | Preserve considered solutions, rejection/defer reasons, and supporting evidence so later sessions do not rediscover them as new | Adapt | MIT for shinpr; proprietary IDs remain authoritative | Fixture verifies rejected `SOL#` remains traceable and is not silently deleted |

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

| Method source | Required coverage in `discover-product` | Verification |
| --- | --- | --- |
| [Product discovery](../product_discovery.md) — four risks | Classify assumptions across value, usability, feasibility, and viability; allow multiple dimensions | Fixtures include all four risks and cross-cutting assumptions |
| Product discovery — 1. Frame an outcome | Start from observable/measurable change, why it matters, and to whom; reject feature requests as outcomes | Outcome fixture distinguishes outcome from output |
| Product discovery — 2. Gather evidence | Support interviews, observation, analytics/support/search/workarounds, journeys, alternatives research, and expert/stakeholder evidence; prefer past behavior | Evidence fixtures cover source types and quality levels |
| Product discovery — 3. Map opportunities | Record needs, pains, desires, and obstacles under an outcome; keep `OPP#` solution-neutral | Critic flags feature-shaped opportunities |
| Product discovery — 4. Generate alternatives | Create materially different `SOL#` directions, including non-software/no-build where meaningful | Finalize requires alternatives or explicit `DEC#` exception |
| Product discovery — 5. Expose assumptions | Attach assumptions to solutions or, when solution-independent, opportunities; rank by importance and lack of evidence | Schema/fixtures verify anchors and ranking |
| Product discovery — 6. Test cheaply | Select the smallest trustworthy test and preregister support/refute/inconclusive criteria | Card and method-selection fixtures pass |
| Product discovery — 7. Decide and record | Record proceed/adapt/pause/abandon, evidence strength, remaining uncertainty, and next decision | Every increment ends with `DEC#` and handover |
| Product discovery — artifacts | Treat optional artifacts as thinking tools selected by tailoring while preserving mandatory trace records | Low-ceremony fixture avoids unnecessary artifacts without breaking traceability |
| Product discovery — experiment card | Preserve decision, assumption, evidence needed, method, criteria, result/confidence, and next step; extend with risk confidence and budget | `EXP#` schema passes |
| Product discovery — failure modes | Guard against preferred-solution validation, users designing the product, opinion inflation, low-risk testing, unused maps, separation from delivery, and endless research | Every failure mode maps to an instruction and adversarial test |
| Product discovery — completion checks | Explicit outcome/opportunity; visible ranked assumptions; proportionate evidence; alternatives; success/guardrail measures; visible uncertainty | Scored report has one result per check |
| [Domain discovery](../domain_discovery.md) | Trigger domain work for contested language, rules, events, ownership, hotspots, and boundaries; keep canonical artifacts outside loop workspace | Fixture calls `domain-modeling` without duplicating glossary |
| [Quality attributes](../quality_attributes.md) | Surface architecture-changing quality risks during discovery; explore consequences/trade-offs without finalizing `QAS#` | Fixture records early quality assumptions and hands them forward |
| [Resources](../resources.md) | Route uncertainty to an appropriate technique and adopt it only when it improves a decision | Technique-selection fixtures pass |
| [Glossary](../glossary.md) | Use outcome, evidence, opportunity, solution, assumption, experiment, signal, success, guardrail, and stop criteria consistently | Terminology audit passes; add canonical solution-candidate terminology if needed |
| [Overview](../overview.md) | Support the minimum useful discovery package and carry evidence toward readiness for design | End-to-end topic retains visible uncertainty and evidence-supported scope |
| [Lifecycle tailoring](../lifecycle_tailoring.md) | Read `lifecycle-onepager.md`, respect selected artifacts/cadence/authority, and record deliberate deviation | Low- and high-ceremony fixtures pass |
| [GitHub skillset analysis](./github_skillsets.md) + [revision contract](./skillset_plan_update_plan.md) | Apply all relevant integration items, the three gap corrections (ordered updates 1–3), dependency rules, source audit, and validation | Ledger has no undecided row |
| [Skillset plan](./prod_discovery_requirements_skillset_plan.md) | Seed from vision/companion; maintain proprietary IDs; call internal skills only through defined handoffs; end with lifecycle-aware next step | End-to-end trace/handover tests pass |

## Required artifact and trace contract

| Artifact / record | Required trace |
| --- | --- |
| `EV#` | Human- or system-supplied source, date, evidence type, quality/strength, relevant actor/context |
| `OPP#` | Desired outcome and relevant vision/actor IDs; supporting `EV#`; routing decision |
| `SOL#` | Selected `OPP#`; materially distinct direction; product/process/policy/manual/no-build category where relevant |
| `ASM#` | Risk class(es), importance, evidence status, and `SOL#` anchor, or `OPP#` when genuinely solution-independent |
| `EXP#` | Decision, tested `ASM#`, evidence needed, method, budget, support/refute/inconclusive criteria, result, confidence by risk, next decision |
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
- [ ] Every `EXP#` cites a named `ASM#`.
- [ ] Every `EXP#` contains decision, evidence needed, method, budget, preregistered support/refute/inconclusive criteria, result, risk confidence, and next step.
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
