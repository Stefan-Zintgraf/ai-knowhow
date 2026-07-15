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

| Method source | Required coverage in `tailor-lifecycle` | Verification |
| --- | --- | --- |
| [Overview](../overview.md) | Preserve the lifecycle model; use the pragmatic workflow only as a default; support the minimum useful discovery package; retain readiness-for-design as the eventual exit criterion | Fixtures cover every entry point and both low- and high-ceremony variants; output never implies that every topic begins at vision |
| [Lifecycle tailoring](../lifecycle_tailoring.md) — Step 1 | Classify greenfield, new capability, improvement/rework, mandate, fast-follow, and technical/platform topics by where uncertainty sits | One fixture per entry point; each includes rationale |
| Lifecycle tailoring — Step 2 | Size ceremony independently by harm, irreversibility, regulation/contract, coordination cost, lifetime, and genuine uncertainty | Mixed-risk fixture applies extra ceremony only to the high-risk concern |
| Lifecycle tailoring — Step 3 | Select stages and artifacts because they reduce uncertainty or improve a decision; preserve the mandatory minimum | Output always contains actors/outcome, visible risky assumptions, success/stop criteria, and consequential decision logging |
| Lifecycle tailoring — Step 4 | Select continuous, timeboxed, or gated cadence and define what one cycle produces | Finalize rejects a cadence that gives time only but no tested assumption and recorded decision |
| Lifecycle tailoring — Step 5 | Assign exactly one owner to each consequential decision type and name an escalation path | Finalize reports missing, ambiguous, or multiply-owned decisions |
| Lifecycle tailoring — one-pager template | Produce every template section using the non-colliding name `lifecycle-onepager.md` | Golden-file/schema test verifies all sections |
| Lifecycle tailoring — failure modes | Guard against excessive ceremony, mandate-equals-no-discovery, habitual entry point, evidence-free greenfield, stale tailoring, unowned stop decisions, and document-review gates | Every failure mode maps to a prompt guardrail or acceptance fixture |
| Lifecycle tailoring — completion checks | Use all six checks as the judgment-based finalize rubric | Scored finalize report contains one result per check |
| [Resources](../resources.md) | Use the practical technique index to map uncertainty to stages/techniques; apply the evaluation rule | Fixtures show recommendations vary by uncertainty and never select artifacts just for completeness |
| [Glossary](../glossary.md) | Use canonical method vocabulary | Terminology audit passes |
| [GitHub skillset analysis](./github_skillsets.md) | Apply external dependency policy, handover UX, re-entry pattern, linter use, source audit, and validation strategy | Contribution ledger has no undecided item |
| [Skillset plan](./prod_discovery_requirements_skillset_plan.md) | Remain a short interview producing one file; record deliberate skips; control downstream handover; be respected by later skills | End-to-end reference run confirms later skills read and follow the one-pager |

## Objective authoring coverage gate

`tailor-lifecycle` is authoring-complete only when all of the following are true:

- [ ] Every contribution row has a stable `TL-*` ID.
- [ ] Every contribution has a final Adopt, Adapt, Call, Reject, or Defer disposition; none remains Pending audit.
- [ ] Every rejection or deferral gives a reason; every deferral names an owning future skill or plan.
- [ ] The source-audit manifest records repository, pinned revision/release, inspected paths, date, license, findings, disposition, and verification.
- [ ] No CC BY-NC-SA material from `deanpeters/Product-Manager-Skills` was copied, distilled, or bundled.
- [ ] Every method-coverage row links to a concrete instruction, reference file, guardrail, fixture, or validator.
- [ ] All six lifecycle-tailoring completion checks appear in the finalize rubric.
- [ ] Every lifecycle-tailoring failure mode has an implemented guardrail and at least one test.
- [ ] Fixtures cover all six entry-point classes.
- [ ] Fixtures cover low, mixed, and high ceremony.
- [ ] A mixed-risk fixture demonstrates per-driver rather than uniform ceremony.
- [ ] A valid one-pager includes entry rationale, selected stages, skipped stages with reasons, artifacts, cadence and decision output, authority, success/stop criteria, and a concrete revisit trigger.
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
- Whether out-of-order execution warns or refuses is a plan-level decision; the implemented behavior must be explicit and tested.
