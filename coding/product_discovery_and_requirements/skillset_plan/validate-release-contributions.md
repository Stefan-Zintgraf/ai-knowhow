# Authoring Assurance: `validate-release`

**Status:** Required authoring contract  
**Applies to:** `validate-release` skill implementation and every material revision  
**Primary output:** `validation/REL<n>-review.md`, plus new `EV#` and `DEC#` entries

**Planning sources:** [skillset plan](./prod_discovery_requirements_skillset_plan.md) · [GitHub skillset fit analysis](./github_skillsets.md)  
**Primary method sources:** [Validation and feedback](../validation_and_feedback.md) · [Product definition](../product_definition.md) · [Requirements engineering](../requirements_engineering.md)

## 1. Purpose and scope

This file ensures that `validate-release` closes the loop with evidence rather than ceremony.

The skill must plan the analysis before inspecting results, compare observed behavior against precommitted outcome, guardrail, and stop criteria, judge evidence strength, record a verdict, and route each significant finding to a specific earlier decision or artifact. It must distinguish usage from outcome, avoid vanity metrics, preserve uncertainty, and produce an executable re-entry handover.

No external contribution is accepted merely because it is useful in isolation. It must fit the proprietary evidence and decision model, have an explicit disposition, and be covered by tests. Allowed dispositions are `adopt`, `adapt`, `reject`, or `defer`; no row may remain `pending`.

## 2. External-contribution ledger

Before authoring, replace every source pointer with exact repository URL, commit SHA or release, inspected files, retrieval date, and verified license. Runtime dependencies must be version-pinned.

| ID | Source | Exact contribution to assess | Mode | Required incorporation | Disposition | License and provenance requirement | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VR-EXT-01 | `ai-analyst-lab/north-star` | Deterministic metric audit, vanity-metric refusal, driver/input decomposition, and metric triage | call | Run a version-pinned audit when outcome-metric hygiene is material; preserve result, warnings, and justified skip in the review | adopt | MIT code; verify exact release/commit and notices; Amplitude-derived material requires provenance review | Vanity usage metric fails as sole proof of success; unavailable-call fallback still completes a transparent local review |
| VR-EXT-02 | `phuryn/pm-skills` — North Star and metric-tree material | Alternative decomposition of outcomes, drivers, and inputs | reference/pattern | Compare with the preferred North Star dependency; adopt only complementary, license-compatible ideas without installing the marketplace | adapt or reject | MIT; record exact files and comparison | Contribution ledger explains every adopted/rejected difference |
| VR-EXT-03 | `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` — `analysis-planner` | Structure the investigation before touching data | pattern only | Require an analysis plan containing question, hypothesis/criteria, populations, time window, data sources, quality checks, guardrails, segmentation, limitations, and decision rules before results are examined | adopt as general guardrail, no content distillation | No stated license; do not copy wording, templates, or files; cite repository as inspiration and independently author the mechanism | Test proves the review plan is timestamped before findings and changes are visible |
| VR-EXT-04 | `ForceInjection/domain-driven-design-skills` | Explicit backtracking-trigger matrix and threshold-based routing | pattern | Implement a re-entry matrix whose triggers identify challenged decision, reopened artifact, owner, required evidence, next skill, and completion condition | adopt/adapt | WIP; record exact files, commit, language/version, and provenance | Each seeded finding routes deterministically; generic “revisit earlier work” fails |
| VR-EXT-05 | `phuryn/pm-skills` — command chaining | Clear next-action handover | pattern | End every review with verdict, reopened artifacts, named owners, next skill, exact input files, urgency, and preserved non-reopened decisions | adopt | Pattern only; cite inspected commands and commit | Re-entry skill starts using artifacts alone |
| VR-EXT-06 | `shinpr/claude-code-discover` — context-separated verifier | Independent verification without inheriting author expectations | pattern | Where the review includes substantial derive work, separate evidence extraction from verdict review; the verifier sees raw evidence, precommitted criteria, candidate findings, and gates, not the analyst’s intended conclusion | adapt | MIT; exact verifier files and commit | Confirmation-bias fixture is caught by an independent review |
| VR-EXT-07 | `RafaelGorski/Problem-Based-SRS` — mechanical trace validation | Deterministic chain validation | shared pattern | Run the shared linter before routing findings so reopened `REQ/QAS/CAP/OPP` references resolve and affected downstream links are enumerated | adopt through shared linter | MIT; exact validation files and commit | Broken re-entry reference and incomplete impact list fail |
| VR-EXT-08 | `jacksoncalling/argo-continuous-discovery` | Rich/Mixed/Thin evidence rubric and confidence capped by evidence quality | shared pattern | Reuse the canonical `EV#` strength semantics when recording post-release evidence; volume must not inflate confidence beyond source quality | adapt through shared evidence model | Record source commit/date and provenance; repository maturity noted | Three weak anecdotes cannot produce a stronger verdict than their evidence cap |
| VR-EXT-09 | `qa` / `triage` existing skills | Intake of support, defect, incident, and external-feedback evidence | call/orchestrate | Import only source-addressable observations; preserve issue IDs/URLs, dates, and provenance; do not treat issue labels as outcome conclusions | adopt | Existing local skills; pin/configure according to skillset policy | Duplicate, unsupported, and opinion-only evidence fixtures are detected |

## 3. Method-document coverage ledger

| ID | Method document | Required use in `validate-release` | Verification |
| --- | --- | --- | --- |
| VR-MTH-01 | [Validation and feedback](../validation_and_feedback.md) | Implement measurement classes, cadence, evidence-routing table, persevere/adapt/pause/retire decisions, failure modes, and completion checks | Primary conformance suite |
| VR-MTH-02 | [Product definition](../product_definition.md) | Treat precommitted release hypothesis, success, guardrail, stop criteria, scope, deferrals, and owner as authoritative | Criteria cannot be rewritten after results without an explicit decision |
| VR-MTH-03 | [Requirements engineering](../requirements_engineering.md) | Validate instrumentation/observation requirements, assess impacted requirements, and create transition requirements for retired scope | Impact and retirement fixtures |
| VR-MTH-04 | [Product discovery](../product_discovery.md) | Record new evidence with strength; route value/usability/feasibility/viability findings to opportunities and assumptions | Assumption-reentry fixtures |
| VR-MTH-05 | [Use cases and story mapping](../use_cases_and_story_mapping.md) | Route misuse, workarounds, failure-path, handoff, permission, or cancellation findings to the affected journey/use case | Journey-reentry fixture |
| VR-MTH-06 | [Quality attributes](../quality_attributes.md) | Evaluate operational evidence, guardrail breaches, incidents, degraded mode, attack/recovery behavior, and trade-offs | QAS-reentry fixture |
| VR-MTH-07 | [Domain discovery](../domain_discovery.md) | Route terminology, ownership, rule, invariant, or context confusion to canonical domain artifacts | Domain-reentry fixture |
| VR-MTH-08 | [Product vision](../product_vision.md) | Reopen vision only when evidence challenges a foundational actor/outcome/value/principle/boundary assumption | Over-escalation and under-escalation tests |
| VR-MTH-09 | [Lifecycle tailoring](../lifecycle_tailoring.md) | Follow review cadence and decision authority; allow evidence to reopen tailoring itself | Cadence and owner tests |
| VR-MTH-10 | [Overview](../overview.md) | Preserve the loop’s feedback purpose and readiness questions; shipping is not success | Shipped-without-outcome fixture |
| VR-MTH-11 | [Glossary](../glossary.md) | Distinguish outcome, signal, usage, evidence, validation of requirements, and post-release validation | Terminology lint |
| VR-MTH-12 | [Resources](../resources.md) | Select analytical and qualitative techniques appropriate to uncertainty and evidence quality | Analysis-plan review |

## 4. Analysis-planning gate

Before inspecting results, the skill must write a durable analysis plan containing:

- `REL#`, review question, and named decision owner;
- unchanged precommitted hypothesis, success, guardrail, and stop criteria;
- metric definitions and distinction between outcome, driver, input, usage, and guardrail;
- analysis population, exclusions, segments, comparison/baseline, and time window;
- qualitative and operational evidence sources;
- data provenance, freshness, missingness, instrumentation changes, and known quality limitations;
- planned calculations or qualitative synthesis;
- confounders and alternative explanations to examine;
- evidence-strength rules and inconclusive conditions;
- decision rules for persevere, adapt, pause, or retire; and
- routing rules for value, usability, scope, requirement, QAS, domain, and vision findings.

Any post-hoc change to this plan must be dated and justified as a `DEC#`; the original remains visible.

## 5. Re-entry/backtracking matrix

The authored skill must include at least these routes:

| Finding | Reopens | Next action |
| --- | --- | --- |
| Capability used, intended outcome unmoved | Opportunity selection / `REL` scope | `define-release` with affected `OPP#`, `CAP#`, evidence, and alternative explanation |
| Capability barely used | Value assumption | `discover-product` with affected `ASM#`/`OPP#` |
| Misuse or workarounds | Journey or usability assumption | `discover-product` and/or `specify-requirements` with affected `UC#` |
| Guardrail breached | Release scope, requirement, or QAS; possibly vision principle | Route to the lowest challenged artifact; escalate only with evidence |
| Incident, support burden, poor recovery, or degraded-mode failure | `QAS#` and related `REQ#` | `specify-requirements` |
| Audit/compliance finding | Obligation, trace, requirement, or transition behavior | `specify-requirements`; return to `define-release` if scope commitment changes |
| Terminology/rule/ownership confusion | Domain glossary, rule, invariant, or context | `domain-modeling`, then affected requirements |
| Foundational actor/outcome/value/boundary assumption contradicted | Vision | `brainstorm-vision` / companion refresh, preserving the evidence chain |
| Evidence too weak or instrumentation invalid | Analysis plan and observation requirement | No scope verdict; repair measurement or gather evidence |
| Scope retired | Transition requirements | `specify-requirements` with migration, communication, coexistence, and decommissioning work |

Every route must identify exact artifact IDs, decision owner, preserved decisions, required new evidence, urgency, and the condition for closing re-entry.

## 6. Deterministic checks

The linter must validate at least:

- The reviewed `REL#` exists and its precommitted criteria resolve.
- Review owner, scheduled date, actual evidence window, and review date are present.
- The analysis plan predates or explicitly versions all findings.
- Every `EV#` has source, date, strength, and provenance.
- Every significant finding cites one or more `EV#`.
- Every verdict maps to predeclared criteria; post-hoc criteria changes cite a `DEC#`.
- Outcome and guardrail measures are not silently replaced with usage metrics.
- Missing or invalid instrumentation produces an inconclusive/measurement-repair outcome rather than a fabricated verdict.
- Every reopened `OPP#`, `ASM#`, `CAP#`, `UC#`, `REQ#`, `QAS#`, vision item, domain item, or tailoring item resolves.
- Each re-entry has one owner, next skill, exact files, rationale, and closure condition.
- Perseverance is recorded with rationale just as reopening is.
- Retired scope has transition-requirement handoff.
- Evidence confidence does not exceed the configured source-quality cap.

## 7. Authoring coverage gate

- [ ] Every external contribution has a final disposition and reason.
- [ ] Adopted contributions link to implementation locations and tests.
- [ ] Exact source files, commit, retrieval date, license, notices, and redistribution implications are verified.
- [ ] The North Star runtime dependency is pinned and has an explicit local fallback.
- [ ] No unlicensed Florian Bonnet content has been copied or distilled.
- [ ] Analysis planning occurs before result inspection and post-hoc changes remain visible.
- [ ] Evidence extraction and verdict review are context-separated for substantial derive work.
- [ ] All method rows map to prompts, schemas, guardrails, routing rules, or tests.
- [ ] The linter catches broken sources, post-hoc criteria changes, vanity metrics, missing instrumentation, inflated evidence confidence, and invalid re-entry links.
- [ ] The skill can return `inconclusive` without forcing a scope decision.
- [ ] Every significant finding either reopens a named decision or records perseverance with rationale.
- [ ] Re-entry points identify the lowest challenged artifact and avoid reopening unrelated upstream work.
- [ ] Retire decisions create a transition-requirements handoff.
- [ ] The final handover names owner, next skill, exact files, preserved decisions, urgency, and closure condition.

## 8. Cross-cutting skillset validation

The shared suite must include:

1. A complete reference topic from companion IDs through `EV/OPP/ASM/EXP`, `REL`, `REQ/QAS`, post-release evidence, verdict, and targeted re-entry.
2. Greenfield, fast-follow, compliance, rework, platform, low-ceremony, and regulated variants.
3. Success, failure, guardrail breach, inconclusive, retirement, invalid-instrumentation, and contradictory-evidence scenarios.
4. Mutation tests for vanity metrics, missing evidence sources, changed criteria, inflated confidence, broken IDs, absent owners, and over-broad re-entry.
5. Blind verifier tests designed to expose confirmation bias and sunk-cost reasoning.
6. Round-trip tests proving a reopened artifact can be revised and the affected trace returns to a valid state.
7. Handover-only tests in which the next skill receives no chat history.
8. Coverage and provenance checks proving every adopted external input is represented in implementation and tests.

## 9. Exclusions and deferrals

- Do not treat shipping, raw usage, issue count, or stakeholder enthusiasm as outcome evidence.
- Do not install the full Phuryn marketplace.
- Do not redistribute or distill unlicensed analytics material.
- Do not let the North Star call write or mutate proprietary artifacts directly.
- Do not reopen the vision when a lower-level opportunity, scope, journey, requirement, or QAS explains the evidence.
- Do not reopen every decision because of one weak anecdote; preserve evidence-strength caps.
- Do not perform product analytics implementation, dashboard construction, experimentation-platform engineering, or software remediation inside this skill.
- Architecture and implementation changes remain downstream consequences of the reopened product artifacts.
