# `tailor-lifecycle` — contribution and coverage assurance

**Status:** Authoring contract  
**Applies to:** `tailor-lifecycle`  
**Plan:** [Product discovery and requirements skillset plan](./prod_discovery_requirements_skillset_plan.md)  
**External analysis:** [Existing GitHub skillsets — fit analysis](./github_skillsets.md)

## Purpose and scope

This file makes the authoring completeness of `tailor-lifecycle` auditable.

The skill is not complete merely because it implements the short description in the plan. It must cover every assigned method requirement, explicitly consider every relevant external contribution, apply the skillset-wide assurance mechanisms, and record an evidence-backed disposition for every contribution.

Allowed dispositions are:

- **Adopt** — use substantially as described.
- **Adapt** — incorporate the mechanism into the proprietary method and artifact model.
- **Call** — invoke a pinned external skill for a self-contained judgment.
- **Reject** — deliberately exclude, with a reason.
- **Defer** — assign to a named later skill or skillset.
- **Pending audit** — not yet decided; this blocks the authoring gate.

“Considered” does not mean copied or adopted. The proprietary lifecycle, artifact names, traceability spine, method vocabulary, and tailoring rules remain authoritative whenever an external contribution conflicts with them.

Contribution IDs are stable. New findings receive new IDs; existing IDs must not be renumbered or reused.

## Contribution ledger

| ID | Source contribution | Source | Mode | Required incorporation or decision | Disposition | License / dependency constraint | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TL-001 | Command-chaining handover UX: finish by naming the next appropriate command or stage | `phuryn/pm-skills` | Pattern | End every successful tailoring session by naming the selected entry skill and later enabled stages; name the reason and input artifact | Adapt | MIT; no runtime dependency required | Acceptance tests verify that greenfield, rework, mandate, fast-follow, and platform topics produce different handovers |
| TL-002 | Three-tier distinction between workflow, interactive, and component behavior | `deanpeters/Product-Manager-Skills` | Pattern / reference only | Keep `tailor-lifecycle` a short interactive workflow that selects components rather than absorbing the stages it routes to | Adapt | CC BY-NC-SA 4.0; do not copy or distill text | Skill structure is independently authored; source is recorded only as an attributed design influence |
| TL-003 | Adaptive interview depth | `deanpeters/Product-Manager-Skills` Adaptive Decision Ladder | Pattern / reference only | Ask only enough questions to resolve entry point, ceremony, cadence, artifacts, authority, and revisit trigger; deepen only when risk or ambiguity requires it | Adapt | CC BY-NC-SA 4.0; no copied questions or reference files | Low-risk fixture stays within the 10–15-question target; higher-risk fixture records why extra depth or open items are needed |
| TL-004 | Compact ceremony floor | `assimovt/productskills` single-purpose style | Pattern | Preserve the minimum-useful-package path for low-risk solo work; do not make full ceremony the default | Adapt | MIT; inspect the relevant compact skills before final authoring | Low-risk fixture selects only justified artifacts and records every skipped stage |
| TL-005 | Explicit backtracking and re-entry triggers | `ForceInjection/domain-driven-design-skills` | Pattern | Turn the one-pager revisit trigger into concrete evidence conditions and identify which tailoring decision is reconsidered | Adapt | License not established by the comparison; pattern only unless audit confirms reuse terms | Fixture contains a specific trigger and target decision, not “revisit when needed” |
| TL-006 | Mechanical validation instead of self-review alone | `RafaelGorski/Problem-Based-SRS` validation pattern | Pattern | Run the shared loop-workspace linter at finalize and treat applicable failures as blocking except where an explicit open-marker policy applies | Adapt | MIT | Finalize test shows malformed structure, reserved-name collisions, and other applicable violations are reported deterministically |
| TL-007 | Deterministic checks separated from judgment | `ai-analyst-lab/north-star` engineering pattern | Pattern | Keep code-checkable completeness separate from judgment-based review; use the shared linter for code-checkable rules | Adapt | MIT code; Amplitude-derived metric content is not needed here | Gate and test report identify deterministic checks separately from human/LLM judgments |
| TL-008 | Scored blind-run validation | `ForceInjection/domain-driven-design-skills` | Pattern | Include `tailor-lifecycle` in the canonical end-to-end reference-topic run and score it against the method completion checks | Adapt | Pattern only unless license is confirmed | Reference-run report links each failed rubric item to a skill revision or documented accepted exception |
| TL-009 | External-content dependency discipline | Cross-cutting finding in `github_skillsets.md` | Policy | Runtime calls are pinned; distilled material records repository, path, revision, license, attribution, and retrieval date; never fetch donor repositories at runtime | Adopt | Mandatory | Dependency/source manifest has all required fields and contains no unpinned call or live fetch |
| TL-010 | Focused donor-source audit | Coverage assurance requirement | Authoring process | Inspect actual assigned donor material rather than relying only on the summary; record every useful candidate found | Adopt | Audit the pinned revision and license before copying anything | Audit manifest lists inspected paths, revision, date, candidate contribution, and final disposition; no Pending audit remains |
| TL-011 | Shared method terminology | Proprietary glossary and spine | Policy | Use lifecycle, workflow, entry point, cadence, outcome, evidence, success criteria, stop criteria, and decision authority exactly as defined | Adopt | Proprietary | Terminology review and fixtures contain no conflicting meanings |
| TL-012 | Preserve the proprietary artifact model | Cross-cutting finding | Policy | Produce only `lifecycle-onepager.md`; do not import a donor workspace, taxonomy, or stage-artifact scheme | Adopt | Mandatory | File-output test confirms that no external artifact taxonomy is introduced |
| TL-013 | Record skipped stages rather than silently omitting them | Proprietary method, reinforced by ceremony comparison | Policy | Every lifecycle stage not selected is listed with a reason | Adopt | Proprietary | Finalize fails when a known stage is neither selected nor explicitly skipped |
| TL-014 | Handover follows tailoring, not a hard-coded order | Proprietary method plus phuryn UX pattern | Pattern | Derive the suggested next stage from entry point and selected stages | Adapt | No external dependency | Rework starts from validation evidence, mandate from requirements, and fast-follow from definition |
| TL-015 | One owner per consequential decision and explicit escalation | Proprietary method; externally reinforced workflow discipline | Policy | Do not accept group labels or missing ownership where one accountable owner is required; record escalation | Adopt | Proprietary | Ownership validator/rubric detects missing, ambiguous, or multiple owners |
| TL-016 | Deliberate stage selection by uncertainty | Proprietary method plus compact-coach comparison | Policy | Recommend stages and artifacts only when they reduce an important uncertainty or improve a consequential decision | Adopt | Proprietary | Technique-routing fixtures vary by dominant uncertainty and avoid completeness-driven artifact selection |
| TL-M01 | Seven-field decision-authority record; a group or department is never an accountable owner | [collaboration_and_decision_ownership.md](../collaboration_and_decision_ownership.md) ("Tailoring the defaults", decision language) — method-owned, revision-contract update 9 | Method-owned policy | Extend the one-pager decision-authority section beyond `<decision type> — <owner>` to all seven fields — one named accountable owner, required contributors, specialist authorities, formal approvers, evidence required to decide, escalation path, evidence-based reopen trigger; the interview elicits them; finalize blocks on a missing field or a group-only owner (plan §5.3) | Adopt | Proprietary method doc; no external license | Golden-file/schema test on the extended one-pager decision-authority section; finalize/ownership-validator fixture refuses a group-only owner or missing approver field (regression scenario RTS-07; boundary handoffs scored by RTS-09) |
| TL-M02 | Early specialist participation where specialist evidence is material; no fabricated specialist evidence | [collaboration_and_decision_ownership.md](../collaboration_and_decision_ownership.md) ("Collaboration across the lifecycle", core rules 4–5) — method-owned, revision-contract update 9 | Method-owned policy | The tailoring interview asks which specialist evidence (engineering, design, operations, security, compliance, domain, other) is material for the topic and names the required contributors and specialist authorities in the one-pager; downstream skills gate on them; design/architecture decisions stay under engineering authority (plan §5.3, §7) | Adopt | Proprietary method doc; no external license | One-pager fixture names specialist authorities per decision type; missing required specialist/engineering input is detected and refused downstream (regression scenario RTS-08) |

## Focused external source-audit manifest

Before authoring can pass, inspect and record the pinned revision and relevant paths for:

| Repository | Required audit scope | Audit objective |
| --- | --- | --- |
| `phuryn/pm-skills` | Chained discovery commands and end-of-command handovers | Identify reusable handover and next-step UX without importing its lifecycle or trigger namespace |
| `deanpeters/Product-Manager-Skills` | Tier taxonomy and Adaptive Decision Ladder descriptions | Extract design ideas only; prove that no CC BY-NC-SA text was distilled |
| `assimovt/productskills` | Compact skill contracts relevant to discovery and scoping | Check whether the minimum-ceremony structure improves the one-pager interview |
| `ForceInjection/domain-driven-design-skills` | Backtracking-trigger matrices and blind-run validation material | Identify general re-entry and validation patterns without adopting its DDD workflow |
| `RafaelGorski/Problem-Based-SRS` | Mechanical `validate` action | Identify deterministic validation ideas suitable for the shared linter |
| `ai-analyst-lab/north-star` | Deterministic validator organization only | Learn the boundary between scripted checks and judgment; do not import metric content |

For every inspected source, record repository and canonical URL, pinned commit/tag/release, paths, retrieval date, detected license, attribution duty, candidate contribution, destination, final disposition, reason, and verification. New candidates receive new `TL-*` IDs.

## Method-document coverage ledger

| ID | Method source | Required coverage in `tailor-lifecycle` | Verification |
| --- | --- | --- | --- |
| TL-MTH-01 | [Overview](../overview.md) | Preserve the lifecycle model; use the pragmatic workflow only as a default; support the minimum useful discovery package; retain readiness-for-design as the eventual exit criterion | Fixtures cover every entry point and both low- and high-ceremony variants; output never implies that every topic begins at vision |
| TL-MTH-02 | [Lifecycle tailoring](../lifecycle_tailoring.md) — Step 1 | Classify greenfield, new capability, improvement/rework, mandate, fast-follow, and technical/platform topics by where uncertainty sits | One fixture per entry point; each includes rationale |
| TL-MTH-03 | Lifecycle tailoring — Step 2 | Size ceremony independently by harm, irreversibility, regulation/contract, coordination cost, lifetime, and genuine uncertainty | Mixed-risk fixture applies extra ceremony only to the high-risk concern |
| TL-MTH-04 | Lifecycle tailoring — Step 3 | Select stages and artifacts because they reduce uncertainty or improve a decision; preserve the mandatory minimum | Output always contains actors/outcome, visible risky assumptions, success/stop criteria, and consequential decision logging |
| TL-MTH-05 | Lifecycle tailoring — Step 4 | Select continuous, timeboxed, or gated cadence and define what one cycle produces | Finalize rejects a cadence that gives time only but no tested assumption and recorded decision |
| TL-MTH-06 | Lifecycle tailoring — Step 5 | Assign exactly one owner to each consequential decision type and name an escalation path | Finalize reports missing, ambiguous, or multiply-owned decisions |
| TL-MTH-07 | Lifecycle tailoring — one-pager template | Produce every template section using the non-colliding name `lifecycle-onepager.md` | Golden-file/schema test verifies all sections |
| TL-MTH-08 | Lifecycle tailoring — failure modes | Guard against excessive ceremony, mandate-equals-no-discovery, habitual entry point, evidence-free greenfield, stale tailoring, unowned stop decisions, and document-review gates | Every failure mode maps to a prompt guardrail or acceptance fixture |
| TL-MTH-09 | Lifecycle tailoring — completion checks | Use all eight checks as the judgment-based finalize rubric, including both the explicit, justified roadmap adopt/skip check and the check that required contributors, specialist authorities, and formal approvers are named where applicable | Scored finalize report contains one result per check; the roadmap result uses the paired RTS-13 variants, with LNT-14 applied when the roadmap is adopted |
| TL-MTH-10 | [Resources](../resources.md) | Use the practical technique index to map uncertainty to stages/techniques; apply the evaluation rule | Fixtures show recommendations vary by uncertainty and never select artifacts just for completeness |
| TL-MTH-11 | [Glossary](../glossary.md) | Use canonical method vocabulary | Terminology audit passes |
| TL-MTH-12 | [GitHub skillset analysis](./github_skillsets.md) + [revision contract](./skillset_plan_update_plan.md) | Apply external dependency policy, handover UX, re-entry pattern, linter use, source audit, and validation strategy | Contribution ledger has no undecided item |
| TL-MTH-13 | [Skillset plan](./prod_discovery_requirements_skillset_plan.md) | Remain a short interview producing one file; record deliberate skips; control downstream handover; be respected by later skills | End-to-end reference run confirms later skills read and follow the one-pager |

## Objective authoring coverage gate

`tailor-lifecycle` is authoring-complete only when all of the following are true:

- [ ] Every contribution row has a stable `TL-*` ID.
- [ ] Every contribution has a final Adopt, Adapt, Call, Reject, or Defer disposition; none remains Pending audit.
- [ ] Every rejection or deferral gives a reason; every deferral names an owning future skill or plan.
- [ ] The source-audit manifest records repository, pinned revision/release, inspected paths, date, license, findings, disposition, and verification.
- [ ] No CC BY-NC-SA material from `deanpeters/Product-Manager-Skills` was copied, distilled, or bundled.
- [ ] Every method-coverage row links to a concrete instruction, reference file, guardrail, fixture, or validator.
- [ ] All eight lifecycle-tailoring completion checks appear in the finalize rubric (per the current [lifecycle_tailoring.md](../lifecycle_tailoring.md) list, including explicit, justified roadmap adoption/skip and named contributors/specialist authorities/approvers); the paired RTS-13 variants cover the roadmap decision and LNT-14 applies to the adopted variant.
- [ ] Every lifecycle-tailoring failure mode has an implemented guardrail and at least one test.
- [ ] Fixtures cover all six entry-point classes.
- [ ] Fixtures cover low, mixed, and high ceremony.
- [ ] A mixed-risk fixture demonstrates per-driver rather than uniform ceremony.
- [ ] A valid one-pager includes entry rationale, selected stages, skipped stages with reasons, an explicit and justified roadmap adopt/skip decision, artifacts, cadence and decision output, authority, success/stop criteria, and a concrete revisit trigger.
- [ ] Every consequential decision type has exactly one owner and an escalation path.
- [ ] Handover derives the next skill from the selected lifecycle and names the required input artifact.
- [ ] The shared deterministic linter runs during finalize and surfaces its failures accurately.
- [ ] Judgment-based checks are distinct from deterministic linter results.
- [ ] The canonical reference topic has run through this skill and then through the selected downstream loop.
- [ ] Reference-run failures caused a revision or a documented accepted exception.
- [ ] No external workspace, artifact taxonomy, or traceability spine displaced the proprietary model.
- [ ] Final source attribution and dependency records pass license review.

Any unchecked item blocks “authoring complete.”

## Exclusions and deferrals

- The skill does not perform vision, discovery, definition, requirements, design, implementation, or validation work; it selects and configures them.
- It does not import any external PM lifecycle or artifact taxonomy.
- It does not install the full `phuryn/pm-skills` marketplace.
- It does not distill `deanpeters/Product-Manager-Skills` content.
- The Working Backwards press-release stress test belongs to `brainstorm-vision`.
- North-star metric auditing belongs to `define-release` and `validate-release`.
- `SOL#`, evidence scoring, opportunity routing, and experiment cards belong to `discover-product`.
- Requirements trace validation belongs to the shared linter and `specify-requirements`; this skill runs only applicable shared checks.
- DDD tactical design, architecture, EventStorming, and interface skills remain deferred to the future design skillset.
- Whether out-of-order execution warns or refuses is a plan-level decision; the implemented behavior must be explicit and tested. *(Decided in the plan, §4.1: refuse silent violations; warn-and-record legitimate recorded deviations.)*

## Plan-to-authoring traceability (revision-contract update 8)

Maps every accepted row to its plan location and **planned** skill-file destination (paths relative to the future `skills/tailor-lifecycle/` directory; the skill is not authored yet). Governing rules — replace-planned-with-actual, reopen, date capture, post-authoring reconciliation — are in [plan §3.3](./prod_discovery_requirements_skillset_plan.md). **Date capture:** no row records a pinned commit/retrieval date yet; the source-audit manifest above is executed at authoring time, and capturing repository URL, inspected files, commit/tag or retrieval date, and verified license for every external source is an explicit authoring-time task (plan §3.3).

| Row | Plan § | Planned destination (path/section) |
| --- | --- | --- |
| TL-001 | §4.1, §5.3 | Handover section of `SKILL.md` (entry skill, enabled stages, reason, input artifact) |
| TL-002 | §5.3 | `SKILL.md` overall shape: short component-selecting interview workflow |
| TL-003 | §5.3 | Interview phase sub-file: adaptive depth, 10–15-question target, recorded deepening reason |
| TL-004 | §5.3 | Default-path rules: minimum-ceremony package; low-risk fixture |
| TL-005 | §4.2, §5.3 | One-pager template's revisit-trigger section: concrete evidence conditions naming the reconsidered decision |
| TL-006 | §2.2, §5.3 | Finalize step invoking the shared `lint-workspace` script (LNT-05, LNT-13) |
| TL-007 | §2.2, §5.3 | Finalize report: deterministic results separated from judgment rubric |
| TL-008 | §6, §5.3 | Inclusion in the reference-topic regression run (RTS-01/02/13) |
| TL-009 | §3.2, §5.3 | Skill dependency/source manifest per the external-dependency policy |
| TL-010 | §3.2, §3.3, §5.3 | Executed source-audit manifest (the six-repo table above) with full provenance fields |
| TL-011 | §5.3 | Canonical method terminology across prompts/output; terminology review |
| TL-012 | §5.3 | Output contract: sole output `lifecycle-onepager.md`; file-output test |
| TL-013 | §4.1, §5.3 | Skipped-stage recording in the one-pager template + finalize failure when a stage is neither selected nor skipped |
| TL-014 | §4.1, §5.3 | Handover derivation rules (rework→validation evidence, mandate→requirements, fast-follow→definition) |
| TL-015 | §5.3 | One-pager decision-authority section + ownership validator (one named owner, escalation, group labels rejected) |
| TL-016 | §5.3 | Stage/artifact recommendation rules: uncertainty-driven selection; technique-routing fixtures |
| TL-MTH-01 | §2.1, §4, §5.3, §6 | `SKILL.md` section **Lifecycle model and exit criterion**; `fixtures/lifecycle-entry-points` verifies all six entry classes, low/high ceremony, and that vision is not a universal start (RTS-01/RTS-02) |
| TL-MTH-02 | §2.1, §4, §5.3, §6 | `SKILL.md` section **Entry-point classification**; `fixtures/entry-points` provides one rationale-bearing case for greenfield, capability, rework, mandate, fast-follow, and platform |
| TL-MTH-03 | §2.1, §5.3, §6 | `SKILL.md` section **Ceremony sizing**; `fixtures/mixed-risk-ceremony` proves per-driver depth instead of uniform ceremony (RTS-01/RTS-13) |
| TL-MTH-04 | §2.1, §5.3, §6 | `SKILL.md` section **Stage and artifact selection** plus `references/lifecycle-onepager-template.md`; `fixtures/stage-selection` verifies the mandatory minimum and fails a stage neither selected nor reasoned as skipped (RTS-02/RTS-13) |
| TL-MTH-05 | §2.1, §5.3 | `SKILL.md` section **Cadence and cycle output**; `fixtures/cadence-decision-output` rejects a cadence with elapsed time but no tested assumption and recorded decision |
| TL-MTH-06 | §2.1, §5.3, §6 | `SKILL.md` section **Decision authority** plus the one-pager authority fields; `fixtures/decision-authority` rejects missing, ambiguous, multiple, or group-only owners and missing escalation (RTS-07/RTS-09) |
| TL-MTH-07 | §2 (artifact table), §2.1, §2.2 (LNT-05, LNT-13, LNT-14), §5.3 | `references/lifecycle-onepager-template.md` with every method section and roadmap adopt/skip field; `fixtures/lifecycle-onepager-golden` verifies schema/name and the RTS-13 paired variants |
| TL-MTH-08 | §2.1, §5.3 | `references/finalize-rubric.md` section **Failure-mode guardrails**; `fixtures/lifecycle-failure-modes` contains one adversarial case for each of the seven listed failures |
| TL-MTH-09 | §2.1, §5.3, §6 (axis 1) | `references/finalize-rubric.md` section **Lifecycle completion checks**; `fixtures/finalize-eight-checks` requires one scored result for each of the eight checks and keeps deterministic results separate; its roadmap result runs the paired RTS-13 variants and applies LNT-14 to the adopted variant |
| TL-MTH-10 | §2.1, §5.3 | `SKILL.md` section **Technique routing by uncertainty**; `fixtures/dominant-uncertainty-routing` proves recommendations vary by uncertainty and rejects completeness-only selection |
| TL-MTH-11 | §2.1, §5.3 | `SKILL.md` section **Method terminology contract**; `fixtures/terminology-audit` checks canonical lifecycle, workflow, entry-point, cadence, outcome, evidence, success/stop, and authority meanings |
| TL-MTH-12 | §2.1, §§3.2–3.3, §5.3, §6 (axis 2) | `references/source-audit-manifest.md` plus `SKILL.md` authoring gate; `fixtures/contribution-coverage` fails an undecided row, missing provenance field, live fetch, or unpinned call |
| TL-MTH-13 | §2.1, §4.1, §5.3, §6 | `SKILL.md` sections **Output contract**, **Finalize**, and **Handover**; reference-topic fixture `fixtures/tailored-downstream-handover` proves later skills read the one-pager and honor skips/order (RTS-01/RTS-02/RTS-13) |
| TL-M01 | §5.3 | One-pager template: seven-field decision-authority section; interview phase eliciting all seven fields; finalize ownership validator refusing a missing field or group-only owner (RTS-07) |
| TL-M02 | §5.3 | Interview phase: specialist-participation question; named contributor/specialist-authority fields in the one-pager that downstream ownership gates read (RTS-08) |
