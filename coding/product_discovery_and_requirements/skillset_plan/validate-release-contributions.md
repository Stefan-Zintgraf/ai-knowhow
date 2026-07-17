# Authoring Assurance: `validate-release`

**Status:** Required authoring contract  
**Applies to:** `validate-release` skill implementation and every material revision  
**Primary output:** `validation/REL<n>-review.md`, plus new `EV#` and `DEC#` entries

**Planning sources:** [skillset plan](./prod_discovery_requirements_skillset_plan.md) · [GitHub skillset fit analysis](./github_skillsets.md)  
**Primary method sources:** [Validation and feedback](../validation_and_feedback.md) · [Product definition](../product_definition.md) · [Requirements engineering](../requirements_engineering.md)

## 1. Purpose and scope

This file ensures that `validate-release` closes the loop with evidence rather than ceremony.

The skill must plan the analysis before inspecting results, compare observed behavior against precommitted outcome, guardrail, and stop criteria, judge evidence strength, record a verdict, and route each significant finding to a specific earlier decision or artifact. It must distinguish usage from outcome, avoid vanity metrics, preserve uncertainty, and produce an executable re-entry handover.

No external contribution is accepted merely because it is useful in isolation. It must fit the proprietary evidence and decision model, have an explicit disposition, and be covered by tests. Allowed dispositions are `adopt`, `adapt`, `call` (a version-pinned specialist with a bounded contract that never owns spine artifacts), `reject`, or `defer`; no row may remain `pending`.

## 2. External-contribution ledger

Before authoring, replace every source pointer with exact repository URL, commit SHA or release, inspected files, retrieval date, and verified license. Runtime dependencies must be version-pinned.

| ID | Source | Exact contribution to assess | Mode | Required incorporation | Disposition | License and provenance requirement | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VR-EXT-01 | `ai-analyst-lab/north-star` | Deterministic metric audit, vanity-metric refusal, driver/input decomposition, and metric triage | call | Run a version-pinned audit when outcome-metric hygiene is material; preserve result, warnings, and justified skip in the review | call *(normalized from `adopt` per revision-contract update 4: call-mode rows carry the `call` disposition)* | MIT code; verify exact release/commit and notices; Amplitude-derived material requires provenance review | Vanity usage metric fails as sole proof of success; unavailable-call fallback still completes a transparent local review. Call contract (update 4, plan §3.1): inputs = candidate outcome/guardrail metrics with the precommitted `REL` criteria and decomposition context; outputs = audit result, warnings, and metric triage, preserved in `validation/REL<n>-review.md` by the calling skill (the specialist writes no spine artifact); version pin = exact commit/release recorded in the skillset dependency manifest at authoring, never a floating ref, upgrades only via ledger reopen; fallback = transparent local metric review against [validation_and_feedback.md](../validation_and_feedback.md), with the skip/fallback recorded in the review |
| VR-EXT-02 | `phuryn/pm-skills` — North Star and metric-tree material | Alternative decomposition of outcomes, drivers, and inputs | pattern | Compare with the preferred North Star dependency; adopt only complementary, license-compatible ideas without installing the marketplace | adapt *(finalized in revision-contract update 4)* | MIT; record exact files and comparison | Final rationale (update 4): adapt — mirrors DR-EXT-08: the MIT-licensed outcome/driver/input decomposition is retained as locally authored material that structures the VR-EXT-01 local-fallback review; it never justifies a second runtime dependency, and ideas duplicating the audit are excluded. Contribution ledger explains every adopted/rejected difference at authoring |
| VR-EXT-03 | `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` — `analysis-planner` | Structure the investigation before touching data | pattern only | Require an analysis plan containing question, hypothesis/criteria, populations, time window, data sources, quality checks, guardrails, segmentation, limitations, and decision rules before results are examined | adopt as general guardrail, no content distillation | No stated license; do not copy wording, templates, or files; cite repository as inspiration and independently author the mechanism | Test proves the review plan is timestamped before findings and changes are visible |
| VR-EXT-04 | `ForceInjection/domain-driven-design-skills` | Explicit backtracking-trigger matrix and threshold-based routing | pattern | Implement a re-entry matrix whose triggers identify challenged decision, reopened artifact, owner, required evidence, next skill, and completion condition | adapt *(finalized in revision-contract update 4)* | WIP; record exact files, commit, language/version, and provenance | Final rationale (update 4): adapt, strictly pattern-mode — the donor license is literally “WIP”/unverified, so per the contract's unlicensed-material rule nothing may be adopted or distilled verbatim; the re-entry matrix (§5) is independently authored on the proprietary spine with the repository recorded as inspiration only. Each seeded finding routes deterministically; generic “revisit earlier work” fails |
| VR-EXT-05 | `phuryn/pm-skills` — command chaining | Clear next-action handover | pattern | End every review with verdict, reopened artifacts, named owners, next skill, exact input files, urgency, and preserved non-reopened decisions | adopt | Pattern only; cite inspected commands and commit | Re-entry skill starts using artifacts alone |
| VR-EXT-06 | `shinpr/claude-code-discover` — context-separated verifier | Independent verification without inheriting author expectations | pattern | Where the review includes substantial derive work, separate evidence extraction from verdict review; the verifier sees raw evidence, precommitted criteria, candidate findings, and gates, not the analyst’s intended conclusion | adapt | MIT; exact verifier files and commit | Confirmation-bias fixture is caught by an independent review |
| VR-EXT-07 | `RafaelGorski/Problem-Based-SRS` — mechanical trace validation | Deterministic chain validation | shared pattern | Run the shared linter before routing findings so reopened `REQ/QAS/CAP/OPP` references resolve and affected downstream links are enumerated | adopt through shared linter | MIT; exact validation files and commit | Broken re-entry reference and incomplete impact list fail |
| VR-EXT-08 | `jacksoncalling/argo-continuous-discovery` | Rich/Mixed/Thin evidence rubric and confidence capped by evidence quality | shared pattern | Reuse the canonical `EV#` strength semantics when recording post-release evidence; volume must not inflate confidence beyond source quality | adapt through shared evidence model | Record source commit/date and provenance; repository maturity noted | Three weak anecdotes cannot produce a stronger verdict than their evidence cap |
| VR-EXT-09 | `qa` / `triage` existing skills | Intake of support, defect, incident, and external-feedback evidence | call/orchestrate | Import only source-addressable observations; preserve issue IDs/URLs, dates, and provenance; do not treat issue labels as outcome conclusions | call *(normalized from `adopt` per revision-contract update 4: call-mode rows carry the `call` disposition)* | Existing local skills; version pin deferred to the external-dependency policy (revision-contract update 5) — see the anchor at plan §3.1 | Duplicate, unsupported, and opinion-only evidence fixtures are detected. Call contract (update 4, plan §3.1): inputs = the issue tracker / feedback sources named in the lifecycle one-pager; outputs = source-addressable observations (issue IDs/URLs, dates, provenance) that `validate-release` records as `EV#` rows; fallback (added in update 4) = when `qa`/`triage` are unavailable or the tracker is unreachable, the human supplies the observations directly in the interview and each is recorded as a source-addressed `EV#` — never a fabricated or label-derived conclusion |

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

### Method-owned rows (revision-contract updates 9–10)

Method-owned rows carry no external license or disposition (revision-contract ledger rules).

| ID | Method document | Required use in `validate-release` | Verification |
| --- | --- | --- | --- |
| VR-M01 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — singular accountable review ownership (core rules 2–3, decision language) | The analysis plan's decision owner (§4) and every re-entry route's owner (§5) are one named accountable individual per `lifecycle-onepager.md`'s decision-authority record (plan §5.3, §5.7); a team or department as owner fails the review or route | Regression scenario RTS-07: a group-only owner is detected and refused; fixture: a re-entry route with a team name as owner fails |
| VR-M02 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — required specialist evidence; no fabrication (core rules 4–5) | Findings in specialist territory — operational evidence, guardrail breaches, incidents, audit/compliance findings — require a source-addressable specialist `EV#` (via the VR-EXT-09 intake or the analysis plan's operational-evidence sources) or an explicit `OPEN:` marker; specialist evidence is never fabricated (plan §5.7) | Regression scenario RTS-08: missing required specialist input is detected and refused; fixture: a guardrail-breach verdict without an operational `EV#` fails |
| VR-M03 | [Product vision](../product_vision.md) — vision-stability escalation guard; revision-contract update 10 | Label each route discovery pivot or vision pivot; only foundational actor/outcome/value/principle/boundary contradiction may reach the vision, through an explicit `DEC#` citing the evidence. All other findings reopen the lowest downstream artifact; validation never edits the vision (plan §4, §5.7) | RTS-11 refuses and reroutes failed-release/experiment escalation; RTS-12 passes genuine vision re-entry only with `DEC#`; linter fixture rejects a vision route without it |
| VR-M04 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — boundary handoff; refusal to proceed on invalidated upstream artifacts (core rule 6, tailoring the defaults) | A re-entry crossing a decision-authority boundary names the owner and escalation path from the one-pager (plan §5.7); no route is closed — and no dependent work continued — while its reopened artifact is unresolved, unless perseverance is recorded with its rationale as a `DEC#` | Regression scenarios RTS-09 (department-boundary handoff) and RTS-10 (refusal to reopen invalidated upstream artifacts) are detected and refused; fixture: closing a route with an unresolved reopened artifact and no perseverance `DEC#` fails |

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
| Foundational actor/outcome/value/principle/boundary assumption contradicted | Vision | Only through an explicit `DEC#` citing the invalidating evidence: `brainstorm-vision`, then companion refresh; validation never edits the vision |
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
- Every route is labeled discovery pivot or vision pivot; a vision route without an evidence-citing `DEC#` fails.
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
9. RTS-11 over-escalation refusal and RTS-12 genuine `DEC#`-gated vision re-entry.

## 9. Exclusions and deferrals

- Do not treat shipping, raw usage, issue count, or stakeholder enthusiasm as outcome evidence.
- Do not install the full Phuryn marketplace.
- Do not redistribute or distill unlicensed analytics material.
- Do not let the North Star call write or mutate proprietary artifacts directly.
- Do not reopen the vision when a lower-level opportunity, scope, journey, requirement, or QAS explains the evidence.
- Do not reopen every decision because of one weak anecdote; preserve evidence-strength caps.
- Do not perform product analytics implementation, dashboard construction, experimentation-platform engineering, or software remediation inside this skill.
- Architecture and implementation changes remain downstream consequences of the reopened product artifacts.

## 10. Plan-to-authoring traceability (revision-contract update 8)

Maps every accepted row to its plan location and **planned** skill-file destination (paths relative to the future `skills/validate-release/` directory; the skill is not authored yet). Governing rules — replace-planned-with-actual, reopen, date capture, post-authoring reconciliation — are in [plan §3.3](./prod_discovery_requirements_skillset_plan.md). This ledger has no distill rows; nothing is scheduled for vendoring. **Date capture:** the §2 preamble's replace-every-source-pointer instruction (exact repository URL, commit SHA/release, inspected files, retrieval date, verified license) is an explicit authoring-time task for every external row (plan §3.3); no row records these values yet. The method-coverage rows VR-MTH-01..12 each have their own plan location, planned file/section, and objective fixture, linter check, or regression target below; VR-MTH-01/03 are the instrumentation contract's consuming end.

| Row | Plan § | Planned destination (path/section) |
| --- | --- | --- |
| VR-EXT-01 | §3.1, §5.7 | `north-star` call step (inputs/outputs, pin, local-fallback per plan §3.1); result/skip preserved in `validation/REL<n>-review.md` |
| VR-EXT-02 | §5.7 | Locally authored metric-tree material structuring the VR-EXT-01 local-fallback review |
| VR-EXT-03 | §2 (review artifact), §2.2 (LNT-17), §5.7 | Analysis-planning gate: plan template + timestamp rule at the head of `validation/REL<n>-review.md` |
| VR-EXT-04 | §4.2, §5.7 | Re-entry/backtracking matrix reference file (the ten-condition map, plan §4.2) |
| VR-EXT-05 | §4.1, §5.7 | Closing-handover section (verdict, reopened IDs, owners, next skill, files, urgency, preserved decisions) |
| VR-EXT-06 | §5.7, §6 | Context-separated verifier step; confirmation-bias fixtures in the regression suite |
| VR-EXT-07 | §2.2, §5.7 | Pre-routing linter invocation (LNT-01, LNT-03–05, LNT-17, LNT-18) |
| VR-EXT-08 | §2 (`evidence-log.md`), §2.2 (LNT-18), §5.7 | Shared `EV#` strength/confidence-cap semantics for post-release evidence |
| VR-EXT-09 | §3.1, §5.7 | `qa`/`triage` call step: intake contract + manual-intake fallback per plan §3.1 |
| VR-MTH-01 | §2 (`validation/REL<n>-review.md`, `evidence-log.md`), §2.1, §2.2 (LNT-17, LNT-18), §4.2, §5.7, §6 | `references/review-template.md`, `references/reentry-matrix.md`, and `references/finalize-rubric.md`; `fixtures/validation-method-conformance` covers measurement classes, cadence, routing, four verdicts, failure modes, and every completion check |
| VR-MTH-02 | §2 (`REL` criteria consumed by review), §2.1, §2.2 (LNT-08, LNT-09, LNT-17), §§5.5–5.7 | `SKILL.md` section **Precommitted release inputs** and the review-template criteria snapshot; `fixtures/post-hoc-criteria-change` fails an unversioned rewrite and requires a dated `DEC#` with the original visible |
| VR-MTH-03 | §2.1, §2.2 (LNT-03, LNT-09, LNT-10, LNT-12, LNT-17), §4.2 (conditions 5, 6, 9, 10), §§5.6–5.7 | `SKILL.md` section **Requirement impact and measurement repair** plus transition handoff fields in `references/reentry-matrix.md`; `fixtures/requirement-impact-and-retirement` checks impacted `REQ#`, invalid instrumentation, and retired-scope transition work |
| VR-MTH-04 | §2 (`evidence-log.md`, discovery traces), §2.1, §2.2 (LNT-03, LNT-18), §4.2 (conditions 1–4), §§5.4–5.7 | `SKILL.md` section **Discovery-evidence routing**; `fixtures/assumption-reentry` records strength-capped `EV#` and routes value/usability/feasibility/viability findings to exact `OPP#`/`ASM#` IDs |
| VR-MTH-05 | §2.1, §4.2 (condition 3), §5.7 | `references/reentry-matrix.md` section **Journey and use-case findings**; `fixtures/journey-reentry` routes misuse, workaround, failure, handoff, permission, and cancellation evidence to the affected `UC#` |
| VR-MTH-06 | §2.1, §4.2 (conditions 4–5), §5.7 | `references/reentry-matrix.md` section **Quality and operational findings**; `fixtures/qas-reentry` routes guardrail, incident, degraded-mode, attack/recovery, and trade-off evidence to exact `QAS#`/`REQ#` IDs |
| VR-MTH-07 | §2.1, §3.1, §4.2 (condition 7), §5.7 | `references/reentry-matrix.md` section **Domain findings**; `fixtures/domain-reentry` checks the pinned `domain-modeling` route/manual fallback and updates canonical domain artifacts without duplication |
| VR-MTH-08 | §2.1, §4, §4.2 (condition 8), §5.7, §6 | `SKILL.md` section **Vision-stability escalation guard** plus the vision row in `references/reentry-matrix.md`; RTS-11/RTS-12 and `fixtures/vision-over-under-escalation` require a foundational contradiction and evidence-citing `DEC#` |
| VR-MTH-09 | §2.1, §4.2 (tailoring re-entry), §5.3, §5.7, §6 | `SKILL.md` start gate **Review cadence and authority** plus the tailoring route in `references/reentry-matrix.md`; `fixtures/review-cadence-owner-and-retailoring` checks scheduled cadence, named owner, and concrete one-pager revisit trigger (RTS-07/RTS-09) |
| VR-MTH-10 | §2.1, §4, §5.7, §6 | `SKILL.md` section **Outcome review, not shipping ceremony**; `fixtures/shipped-without-outcome` refuses success based on shipment/usage alone and preserves readiness questions |
| VR-MTH-11 | §2.1, §5.7 | `SKILL.md` section **Validation terminology contract**; `fixtures/terminology-audit` distinguishes outcome, signal, usage, evidence, requirements validation, and post-release validation |
| VR-MTH-12 | §2.1, §5.7 | `references/analysis-plan-template.md` section **Technique choice and evidence quality**; `fixtures/analysis-plan-technique-selection` checks analytical/qualitative method fit before result inspection and rejects technique-by-habit choices |
| VR-M01 | §5.7 | Analysis-plan owner field + per-route owner rules (one named individual per the one-pager's decision-authority record, §5.3) (RTS-07) |
| VR-M02 | §5.7 | Specialist-evidence intake rule: source-addressable specialist `EV#` or explicit `OPEN:` marker; no fabrication (RTS-08) |
| VR-M03 | §4, §5.7 | Re-entry matrix pivot label and foundational-only `DEC#` vision gate; RTS-11/RTS-12 fixtures |
| VR-M04 | §5.7 | Handover/route fields: authority-boundary owner and escalation path; route closure blocked while the reopened artifact is unresolved unless a perseverance `DEC#` exists (RTS-09, RTS-10) |
