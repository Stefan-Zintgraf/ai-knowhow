# Phase 0 digest — `specify-requirements` ledger audit

**Source ledger:** `skillset_plan/specify-requirements-contributions.md`
**Contract:** `skillset_plan/skillset_plan_update_plan.md` (updates 2, 4, 9)
**Method docs consulted (ledger-cited):** `requirements_engineering.md` (SR-MTH-04), `quality_attributes.md` (SR-MTH-07), `validation_and_feedback.md` (SR-MTH-08)
**Status:** frozen input for Phase 1 write agents

## 1. Row inventory

### External rows (ledger §2)

| ID | Source | License | Reuse mode | Final disposition | Intended incorporation (one line) |
| --- | --- | --- | --- | --- | --- |
| SR-EXT-01 | `shinpr/claude-code-discover` — `hypothesis-verifier` | MIT | pattern | adopt | Fresh-context requirements critic that never sees builder reasoning or expected verdicts |
| SR-EXT-02 | `shinpr/claude-code-discover` — context/index discipline | MIT | pattern | adapt | Durable workspace artifacts, preserved rejected alternatives, current indexes/handover |
| SR-EXT-03 | `RafaelGorski/Problem-Based-SRS` — `validate` action | MIT | pattern | adopt/adapt (compound — see §2) | Deterministic linter for `EV/OPP -> CAP -> UC/REQ/QAS` chain; no `.spec` JSON or `CP/CN/FR` IDs |
| SR-EXT-04 | `RafaelGorski/Problem-Based-SRS` — problem/need discipline | MIT | pattern | adapt | Each `REQ/QAS` traces to need/risk/constraint/obligation with rationale; consume O/E/H from `REL` |
| SR-EXT-05 | `45ck/software-architecture-skills` — `quality-attribute-scenario-writer` | Reported MIT (unverified) | conditional call | defer-until-audit, then adopt or reject (conditional — see §5) | Version-pinned QAS-drafting specialist, output validated through the proprietary QAS gate |
| SR-EXT-06 | `DavidROliverBA/Daves-Claude-Code-Skills` — `nfr-capture` | Unverified | pattern | adapt | ISO 25010-flavoured completeness prompts, without Obsidian schemas/tags/vault layout |
| SR-EXT-07 | `DavidROliverBA/Daves-Claude-Code-Skills` — `nfr-review` | Unverified | pattern | adopt/adapt (compound — see §2) | Complete/measurable/feasible as explicit QAS gate dimensions; separation mandatory, fan-out optional |
| SR-EXT-08 | `huntsyea/product-skills` — `story-mapping` | MIT | distilled upstream input | adapt | Elaborate the committed story-map slice into UCs without recreating or expanding release scope |
| SR-EXT-09 | `deanpeters/Product-Manager-Skills` — `user-story-mapping` | CC BY-NC-SA 4.0 | reference only | reject (for distillation) | Conceptual-gap comparison only; no copying or distillation |
| SR-EXT-10 | `phuryn/pm-skills` — command chaining | Pattern-only (commands cited) | pattern | adopt | Handover output: design-readiness status, artifacts, open questions, confirmations, next workflow |
| SR-EXT-11 | `ForceInjection/domain-driven-design-skills` | WIP (unverified) | pattern | adapt | Backtracking triggers to `define-release`/`discover-product`/`domain-modeling`/human, not forced completion |
| SR-EXT-12 | `ddd-crew/ddd-starter-modelling-process`, ForceInjection tactical DDD, `lagz0ne/design-skill` | CC BY 4.0 / WIP / repo-specific | reference/defer | defer | Candidates for the future design skillset; use existing `domain-modeling` for domain gaps only |

### Method-doc coverage rows (ledger §3)

SR-MTH-01 … SR-MTH-12, one per method doc (overview, lifecycle tailoring, product definition, requirements engineering, use cases/story mapping, domain discovery, quality attributes, validation and feedback, product vision, product discovery, glossary, resources). All have required use + verification. These are coverage rows, not the collaboration/vision-stability "method-owned rows" the contract's ledger rules require — see §8.

**Counts:** 12 external rows + 12 method-doc rows. External dispositions: adopt 2 (01, 10), adapt 5 (02, 04, 06, 08, 11), compound adopt/adapt 2 (03, 07), conditional call 1 (05), reject 1 (09), defer 1 (12).

## 2. Compliance audit against contract ledger rules

- **Literal `Pending` rows: 0.**
- **Rows without a single final disposition from the allowed set {Adopt, Adapt, Call, Reject, Defer}: 3.**
  - SR-EXT-03 and SR-EXT-07: `adopt/adapt` compound. Update-4 writer should resolve each to one disposition (recommended: **Adapt** for both — each translates the mechanism onto the proprietary spine/gate rather than using it as identified).
  - SR-EXT-05: `defer until audit, then adopt or reject`. The contract itself sanctions a *conditional* specialist (update 4), so this is acceptable only if the plan records the condition, the decision point, and both branches; recommended normalization: **Call (conditional)** with the audit as the gating check (see §5).
- **Required fields:** every row has stable ID, source, license note, reuse mode, intended incorporation, disposition, and objective evidence (Verification column). Missing across ALL external rows: exact repo URL, commit SHA/release, files inspected, retrieval date — the ledger preamble defers these to "before authoring". Acceptable for pattern rows; must be scheduled as authoring-time tasks for SR-EXT-05 (call) and SR-EXT-08 (distill).
- **Unverified licenses:** SR-EXT-06, SR-EXT-07 (DavidROliverBA) and SR-EXT-11 (ForceInjection, WIP). Per contract, treat as reference-only until verified; the rows already self-limit to pattern-level use, which conforms, but the plan must carry the verification task.
- **Realizing-artifact citations:** all accepted rows cite a validation scenario/fixture in the Verification column, and the ledger's §§4–7 (builder/reviewer protocol, deterministic checks, QAS gate, coverage gate) provide the realizing mechanisms. What no row yet cites is a **plan section or skill-file destination** — that is exactly update 8's traceability work; update 4 must place each ID in the plan.
- Rejected (SR-EXT-09) and deferred (SR-EXT-12) rows are preserved with reasons — conforms.

## 3. Accepted rows → realizing mechanism required in the revised plan (update 4)

| ID | Mechanism the plan must contain |
| --- | --- |
| SR-EXT-01 | Builder/reviewer protocol phase: fresh critic context receiving inputs, candidates, schemas, gates, lint results — never builder reasoning (ledger §4 steps 3–5); regression check: seeded-error detection, verdict stable without builder rationale |
| SR-EXT-02 | Linter rule + finalize check: indexes/handover match files present; rejected/unresolved alternatives preserved as durable artifacts (ledger §5 last bullet) |
| SR-EXT-03 | The update-2 deterministic workspace linter itself: ID validity/uniqueness, dangling citations, orphans, missing rationale on the `EV/OPP -> CAP -> UC/REQ/QAS` chain; explicit exclusion of `.spec` JSON and `CP/CN/FR` taxonomy |
| SR-EXT-04 | Artifact fields + linter rule: every `REQ/QAS` carries trace to need/risk/constraint/obligation + rationale; O/E/H classification consumed from `REL` as integration contract; orphan-requirement and unsupported-"shall" fixtures |
| SR-EXT-05 | Conditional `quality-attribute-scenario-writer` entry in the skills table with bounded role, version pin, inputs/outputs, fallback (see §5) |
| SR-EXT-06 | QAS elicitation prompts/guardrails in skill prose (operational + stakeholder consequences, no checklist inflation) |
| SR-EXT-07 | QAS gate dimensions Complete/Measurable/Feasible recorded per QAS (ledger §6); separation mandatory, multi-agent fan-out explicitly optional |
| SR-EXT-08 | Integration contract with `define-release`: committed story-map slice is the authoritative boundary; UC elaboration surfaces unresolved paths without scope creep; slice-boundary fixture |
| SR-EXT-10 | Handover/finalize check: design-readiness status, exact artifacts, open questions, required human confirmations, validation hooks, next workflow from tailoring (feeds update 7 too) |
| SR-EXT-11 | Backtracking triggers mapped to named target artifact + owner: `define-release`, `discover-product`, `domain-modeling`, human confirmation (feeds updates 4 and 7) |

## 4. `distill` rows

Only one row touches distillation for this skill:

- **SR-EXT-08** — donor `huntsyea/product-skills`, path `story-mapping`. License MIT. **No commit/tag or retrieval date recorded; not vendored yet** — the row itself requires "record exact files, commit, and retrieval date" at authoring time. Note: the distillation itself is an *upstream* input (story-mapping content feeding the release slice); `specify-requirements` consumes the distilled output. The plan must carry the donor-audit task (contract distill checklist items 1–6) wherever the vendoring lands.
- **deanpeters flag:** SR-EXT-09 (`deanpeters/Product-Manager-Skills`, CC BY-NC-SA 4.0) is correctly `reject` for distillation, reference-only, with an audit verification that no protected content entered the skill. No CC BY-NC-SA content is scheduled for copying. Conforms to the contract prohibition.

## 5. `Call` rows

One row, and it is the one the contract's update 4 makes conditional:

- **SR-EXT-05** — `45ck/software-architecture-skills` `quality-attribute-scenario-writer`, mode "conditional call".
  - **Bounded role:** present in substance — drafts six-part QAS candidates; output must pass the proprietary QAS gate (ledger §6); §9 exclusion "Do not accept a generated QAS specialist without the proprietary QAS gate". **Missing:** an explicit statement that it does not own or write spine artifacts (contract requires this for every `Call`).
  - **Version-pinning:** required by the row ("version-pinned") but **no commit/release recorded yet** — the pin is an authoring-time task; the plan must state the pinning strategy now.
  - **Fallback:** **implicit only.** The comparative fixture ("local-only vs called output against the same QAS gate") implies the local QAS reference (the six-part template + gate grounded in `quality_attributes.md`) is the fallback, but no row field names it. The plan must make the fallback explicit: local QAS drafting per SR-MTH-07.
  - **What the condition should hinge on (for update 4):** (a) authoring-time depth audit shows the skill *materially exceeds* the local QAS reference (`quality_attributes.md` six parts, utility tree, trade-offs, operational quality); (b) verified repository license, exact skill files, commit, examples, generated-pack depth; (c) comparative fixture scoring called vs local output through the same QAS gate. If any leg fails → reject and fall back to local-only. Related row: SR-EXT-07 supplies the gate dimensions the comparison is scored against.

## 6. `Defer` rows

- **SR-EXT-12** — names its receiver: "the future design skillset" (DDD strategic/tactical modeling, requirements-to-design catalogs); interim behavior named (`domain-modeling` for domain gaps); verification is an exclusion review. **Conforms.**
- **SR-EXT-05** — deferred *until* a named decision (the authoring-time depth audit feeding update 4's conditional specialist). The receiving decision exists but has no named owner/point in the plan yet; update 4 should pin it to the skills-table entry.

## 7. Update-2 readiness (deterministic linter: REQ + QAS checks)

What the ledger and cited docs already establish, per contract update-2 minimum checks:

- **`REQ`: verification method or explicit open marker.**
  - `requirements_engineering.md` completion checks: "Each important requirement has a viable verification method"; requirement quality = necessary, clear, singular, feasible, **verifiable**, traceable; EARS-style sentence shape (trigger / system / observable response / measurable constraint / rationale).
  - Ledger §5: "Every requirement has type, normative statement or justified alternative notation, **verification method, status, and source**" — i.e., the linter's REQ field set is already specified, and is a superset of the contract minimum.
- **`QAS`: six fields.**
  - `quality_attributes.md` defines exactly the six parts the contract names — Source, Stimulus, Environment, Artifact, Response, Response measure — with a labeled-field example block (`Attribute:/Source:/Stimulus:/Environment:/Artifact:/Response:/Measure:`) that is directly linter-parseable. Note the doc's example labels the sixth field `Measure:` while prose says "Response measure" — update 2 should fix one canonical field label.
  - Ledger §5 adds beyond the contract minimum: critical QAS also needs stakeholder/business consequence, expected scale/workload, verification method, and trade-off/priority; ledger §6 gate adds Grounded/Feasible/Prioritized/Trade-off-aware/Traceable — these are judgment gates; the linter owns only field presence + open markers + measurability-when-resolved. The update-2 writer must keep this deterministic/judgment split (contract mandates it).
- **Open-marker convention:** ledger §5 requires "Open markers are machine-recognizable and cannot pass as completed values" and §4 step 8 requires uncertainty preserved "in durable open markers and `DEC` entries". **No concrete token/syntax is defined anywhere in this ledger or the cited docs** — update 2 must define the canonical marker syntax (single spine-wide token) so the linter can enforce "unresolved field ⇒ marker present; resolved ⇒ response measure measurable (units + threshold/range + observation method, per ledger §6 Measurable)".
- **Instrumentation mapping (contract update 2, last paragraph):** `validation_and_feedback.md` states the contract's source rule — "Instrumentation is a requirement, not an afterthought… define during product definition and requirements engineering how each outcome and guardrail will be observed in production." Ledger §5 realizes it: "Each outcome/guardrail criterion has an instrumentation or observation requirement," plus transition-requirements-on-retirement (also in `validation_and_feedback.md` "Retiring scope … needs transition requirements"). SR-MTH-08 is the coverage row to cite when mapping `validation_and_feedback.md` → `specify-requirements` in the method-doc coverage table.
- Additional linter material this ledger contributes to update 2 (beyond the contract minimum): out-of-scope `REQ/QAS` without change decision; important UC alternative/failure/permission/cancellation/minimal-guarantee paths present or explicitly N/A; index/handover consistency.

## 8. Method-owned rows for update 9 (collaboration/decision ownership) — gaps and proposals

Update-9 rules that apply to `specify-requirements` but currently have **no method-owned ledger row** (SR-MTH-01..12 are doc-coverage rows; §4 step 6 and §6 "Feasible" imply the behavior but nothing owns it in the ledger):

| Proposed ID | Rule | Intended incorporation | Objective evidence |
| --- | --- | --- | --- |
| SR-M01 | Singular accountable ownership — every consequential requirements decision (invented paths, target values, domain rules, scope changes, trade-offs) is resolved by one named accountable owner; a group/department is not an owner | Human-gate step (ledger §4 step 6) records owner name in the resulting `DEC#`; handover (SR-EXT-10 output) lists unresolved decisions with owners; lifecycle-onepager rows for the requirements stage | Regression scenario "group-only owner" is detected and refused (contract update 3); fixture: `DEC#` without a named individual owner fails the finalize check |
| SR-M02 | Required specialist/engineering participation — QAS feasibility and consequential trade-offs require engineering/domain/ops/security reviewer input when their evidence is material | QAS gate "Feasible" dimension (ledger §6) requires a recorded specialist verdict or a blocking-uncertainty open marker plus escalation to the human gate; never auto-passed | Regression scenario "missing required specialist/engineering input" is detected and refused; fixture: Feasible marked pass without recorded reviewer evidence fails the gate |
| SR-M03 | No fabricated specialist evidence — the builder must not invent stakeholder judgment, domain rules, failure behavior, or measurable targets as settled fact | Builder protocol step 2 (proposals flagged) + linter open-marker rule: proposals cannot pass as completed values; critic checks for unmarked invention | Mutation fixture: a proposal silently converted to a confirmed value is caught by linter or critic; seeded fabricated "engineering says feasible" claim fails review |
| SR-M04 | Evidence-based reopen / refusal to proceed on invalidated upstream artifacts — failed gates route to the named upstream artifact and owner instead of forcing completion | Backtracking triggers (SR-EXT-11) bound to owner + escalation path; skill refuses to elaborate a `REL` slice whose upstream `OPP/ASM/REL` was invalidated | Regression scenarios "refusal to reopen invalidated upstream artifacts" and "requirements gap requiring human review" (contract update 3) pass; every failed gate names artifact + owner |

Vision-stability rows (update 10) are **not required here**: update 10's reopen list names `brainstorm-vision`, `create-vision-companion`, `discover-product`, `define-release`, `validate-release` — not `specify-requirements`. Existing SR-MTH-09 (vision conflicts route upstream, never edited locally) already covers this skill's part.

## 9. Blocking issues (ranked)

1. SR-EXT-05 (`quality-attribute-scenario-writer`): fallback and no-spine-ownership not explicit; version pin and license unverified — update 4 must define bounded role/pin policy/fallback in the skills table and record the audit condition.
2. SR-EXT-03 / SR-EXT-07: compound `adopt/adapt` dispositions must be resolved to a single allowed disposition (recommend Adapt for both).
3. No canonical open-marker syntax defined anywhere — update 2 must define it; two REQ/QAS linter checks depend on it.
4. Unverified licenses (SR-EXT-06/07 DavidROliverBA; SR-EXT-11 ForceInjection WIP) — reference-only until verified; verification tasks must appear in the plan.
5. SR-EXT-08 distill provenance (commit/retrieval date, vendoring) unrecorded — must be a scheduled authoring-time donor-audit task.
6. Update-9 collaboration/ownership rules have no method-owned rows — add SR-M01..SR-M04 (§8).
7. Minor: `quality_attributes.md` example uses field label `Measure:` vs prose "Response measure" — pick one canonical label for the linter.
