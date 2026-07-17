# Phase 0 digest — `validate-release` ledger audit

**Source ledger:** `skillset_plan/validate-release-contributions.md`
**Method doc opened (cited by ledger):** `validation_and_feedback.md` (VR-MTH-01; required by contract update 2)
**Contract:** `skillset_plan_update_plan.md` — audited against the "Contribution ledgers" rules and updates 2, 4, 7, 9, 10.

## 1. Row inventory

### External-contribution rows (ledger §2)

| ID | Source | License (as recorded) | Reuse mode | Final disposition (as recorded) | Intended incorporation (one line) |
| --- | --- | --- | --- | --- | --- |
| VR-EXT-01 | `ai-analyst-lab/north-star` | MIT (Amplitude-derived material needs provenance review) | call | adopt | Version-pinned metric audit (vanity-metric refusal, driver/input decomposition) invoked when outcome-metric hygiene is material; result/warnings/justified skip preserved in `REL<n>-review.md` |
| VR-EXT-02 | `phuryn/pm-skills` (North Star / metric-tree material) | MIT | reference/pattern | **adapt or reject** (not final) | Comparison source only; adopt complementary license-compatible ideas vs VR-EXT-01; no marketplace install |
| VR-EXT-03 | `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` — `analysis-planner` | **No stated license** (reference-only) | pattern only | adopt (as general guardrail, no content distillation) | Analysis-planning gate (ledger §4): durable, timestamped analysis plan before results are inspected; mechanism independently authored |
| VR-EXT-04 | `ForceInjection/domain-driven-design-skills` | **WIP** (unverified) | pattern | **adopt/adapt** (not final) | Re-entry/backtracking matrix (ledger §5): trigger → challenged decision, reopened artifact, owner, evidence, next skill, closure condition |
| VR-EXT-05 | `phuryn/pm-skills` — command chaining | Pattern only (cite inspected commands + commit) | pattern | adopt | Handover format: verdict, reopened artifacts, named owners, next skill, exact input files, urgency, preserved decisions |
| VR-EXT-06 | `shinpr/claude-code-discover` — context-separated verifier | MIT | pattern | adapt | Separate evidence extraction from verdict review for substantial derive work; verifier sees evidence + precommitted criteria, not intended conclusion |
| VR-EXT-07 | `RafaelGorski/Problem-Based-SRS` — mechanical trace validation | MIT | shared pattern | adopt (through shared linter) | Shared linter runs before routing so reopened `REQ/QAS/CAP/OPP` references resolve and downstream impact is enumerated |
| VR-EXT-08 | `jacksoncalling/argo-continuous-discovery` | Provenance to be recorded; repo maturity noted | shared pattern | adapt (through shared evidence model) | Canonical `EV#` strength semantics for post-release evidence; confidence capped by source quality, not volume |
| VR-EXT-09 | Local `qa` / `triage` skills | Local (pin per skillset policy) | call/orchestrate | adopt | Import source-addressable support/defect/incident/external-feedback observations with issue IDs/URLs, dates, provenance; labels are not outcome conclusions |

### Method-document coverage rows (ledger §3) — internal, no license/disposition needed

| ID | Method doc | Intended incorporation (one line) |
| --- | --- | --- |
| VR-MTH-01 | validation_and_feedback.md | Measurement classes, cadence, evidence-routing table, persevere/adapt/pause/retire, failure modes, completion checks — primary conformance suite |
| VR-MTH-02 | product_definition.md | Precommitted `REL` hypothesis/success/guardrail/stop/scope/owner authoritative; no post-hoc rewrite without decision |
| VR-MTH-03 | requirements_engineering.md | Validate instrumentation/observation requirements; impacted-requirement assessment; transition requirements for retired scope |
| VR-MTH-04 | product_discovery.md | New `EV#` with strength; route value/usability/feasibility/viability findings to `OPP#`/`ASM#` |
| VR-MTH-05 | use_cases_and_story_mapping.md | Route misuse/workaround/failure-path/handoff/permission/cancellation findings to journeys/use cases |
| VR-MTH-06 | quality_attributes.md | Operational evidence, guardrail breaches, incidents, degraded mode, trade-offs → `QAS#` |
| VR-MTH-07 | domain_discovery.md | Terminology/ownership/rule/invariant confusion → canonical domain artifacts |
| VR-MTH-08 | product_vision.md | Reopen vision only on foundational actor/outcome/value/principle/boundary contradiction; over/under-escalation tests |
| VR-MTH-09 | lifecycle_tailoring.md | Review cadence + decision authority; evidence may reopen tailoring itself |
| VR-MTH-10 | overview.md | Loop feedback purpose; shipping is not success |
| VR-MTH-11 | glossary.md | Terminology lint: outcome vs signal vs usage vs evidence vs the two validation senses |
| VR-MTH-12 | resources.md | Technique selection appropriate to uncertainty and evidence quality |

## 2. Compliance audit against contract ledger rules

**Required fields (stable ID, source+license, reuse mode, intended incorporation, disposition, objective evidence):**

- All 9 external rows have stable IDs, source, mode, incorporation, disposition column, and a "Verification" column supplying objective evidence. Structurally complete.
- **Non-final dispositions (contract: "No row may remain Pending"):** VR-EXT-02 (`adapt or reject`) and VR-EXT-04 (`adopt/adapt`) are unresolved either/or dispositions — functionally Pending. **Both must be finalized in update 4.**
- **Disposition-vocabulary mismatch:** the contract's allowed set is `Adopt/Adapt/Call/Reject/Defer`, but the ledger's own §1 lists only `adopt/adapt/reject/defer` (omits `Call`). VR-EXT-01 and VR-EXT-09 are `mode: call` with `disposition: adopt`; under the contract they should carry final disposition **`Call`**. Recommend the write phase normalize: VR-EXT-01 → `Call`, VR-EXT-09 → `Call`, and fix §1's vocabulary line.
- **Provenance incompleteness (authoring-time, per ledger §2 preamble and contract):** no row yet records exact commit/SHA/release, inspected files, or retrieval date — the ledger itself defers this to "before authoring". Not a blocker for the plan revision, but update 8 must carry these as explicit authoring-time tasks. VR-EXT-04's license is literally "WIP" and must be verified before any adoption beyond pattern-inspiration.
- **Unlicensed material handled correctly:** VR-EXT-03 is explicitly no-copy/no-distill, independently authored, repository cited as inspiration only — conforms to "treat unlicensed material as reference-only".
- **Accepted rows citing a realizing mechanism:** yes — every accepted row's Verification cites a test fixture, linter rule, or validation scenario (e.g. vanity-metric failure, timestamped-plan test, confirmation-bias fixture, evidence-cap test). What is missing until update 8: **plan section location and planned skill-file destination** for each.
- **Method rows:** all 12 have verification targets (conformance suite, fixtures, lint). Compliant with "method-owned rows need no external license or disposition."

## 3. Accepted rows — realizing mechanism the revised plan must contain (update 4)

| ID | Realizing mechanism required in the plan |
| --- | --- |
| VR-EXT-01 | `north-star` in the **skills table as a callable specialist** with bounded role (metric audit only), version policy (pinned release/commit), inputs (candidate outcome/guardrail metrics + decomposition context), outputs (audit result, warnings, triage), and **explicit local fallback** (transparent local review when unavailable). Must not write/mutate spine artifacts (ledger §9). |
| VR-EXT-03 | **Analysis-planning gate** (ledger §4 field list) as a phase preceding result inspection; post-hoc plan changes dated as `DEC#`; linter rule "analysis plan predates or explicitly versions all findings". |
| VR-EXT-05 | **Handover contract** at skill end: verdict, reopened artifacts + exact IDs, named owner per re-entry, next skill, exact input files, urgency, preserved decisions, closure condition — feeding update 7's handover/re-entry definition. |
| VR-EXT-06 | **Context-separated verifier** step for substantial derive work; blind-verifier / confirmation-bias fixtures in the regression suite (contract update 3 overlap). |
| VR-EXT-07 | `validate-release` **invokes the shared deterministic linter** (update 2 artifact) before routing findings; dangling reopened-reference and incomplete-impact-list failures. |
| VR-EXT-08 | Shared **`EV#` strength model with source-quality confidence cap** in the artifact schema + linter rule "evidence confidence does not exceed the configured source-quality cap". |
| VR-EXT-09 | `qa`/`triage` listed as **called local skills** with an intake contract (source-addressable observations only, issue IDs/URLs/dates preserved); duplicate/unsupported/opinion-only fixtures. |
| VR-EXT-04 (once finalized) | The **re-entry/backtracking matrix** (ledger §5) as a first-class skill artifact — the direct input to update 7. |
| VR-EXT-02 (once finalized) | If adapt: named complementary ideas folded into VR-EXT-01's audit; if reject: recorded duplication reason. No standalone mechanism otherwise. |

## 4. `distill` rows

**None.** This ledger contains no `distill` rows — all reuse is `call`, `pattern`, or `shared pattern`. Nothing is vendored or scheduled for vendoring. **No deanpeters/Product-Manager-Skills content appears anywhere in this ledger** (CC BY-NC-SA constraint satisfied trivially). The distill-provenance Phase 0 agent has no donor obligations originating here.

## 5. `Call` rows

| ID | Bounded role | Version-pinning | Fallback |
| --- | --- | --- | --- |
| VR-EXT-01 `north-star` | Present: deterministic metric audit only; §9 forbids it writing/mutating proprietary artifacts | Required by row + §7 gate ("pinned"), but **no concrete pin (release/commit) recorded yet** — authoring-time task | Present: "unavailable-call fallback still completes a transparent local review"; §7 requires "explicit local fallback" |
| VR-EXT-09 `qa`/`triage` (local) | Present: intake of source-addressable observations only; labels ≠ conclusions | **Vague**: "pin/configure according to skillset policy" — no policy reference resolved; update 5 (external-dependency policy) should be cited once it exists | **Missing**: no behavior defined when `qa`/`triage` are absent or their tracker is unreachable — write phase should add (e.g. manual evidence-intake fallback) |

Update 4 explicitly requires `north-star` in the skills table with bounded role, version policy, inputs, outputs, and fallback — **inputs/outputs are not yet enumerated in the ledger** and must be defined by the update-4 sub-agent (suggested above in §3).

## 6. `Defer` rows

**None.** No row defers to a later skillset or decision, so the "name the receiving skillset/decision" rule is vacuously satisfied. Note: ledger §9 exclusions ("architecture and implementation changes remain downstream consequences"; no analytics implementation/dashboards inside this skill) function as scope exclusions, not deferrals — they name no receiving skillset. If the write phase wants the design-skillset boundary explicit, the architecture-consequence exclusion could become a Defer row naming the future design skillset; optional, not required by the current rows.

## 7. Update-7 / update-10 readiness

### Backtracking conditions → artifact and skill reopened (update 7 mapping)

From ledger §5 (authoritative, superset of `validation_and_feedback.md`'s routing table):

| # | Condition (finding) | Artifact reopened | Skill reopened |
| --- | --- | --- | --- |
| 1 | Capability used, outcome unmoved | Opportunity selection / `REL` scope (`OPP#`, `CAP#`) | `define-release` |
| 2 | Capability barely used | Value assumption (`ASM#`/`OPP#`) | `discover-product` |
| 3 | Misuse or workarounds | Journey/usability assumption (`UC#`) | `discover-product` and/or `specify-requirements` |
| 4 | Guardrail breached | Lowest challenged artifact: release scope, `REQ#`, `QAS#`; vision principle only with escalating evidence | `define-release` / `specify-requirements`; vision path only via condition 8 |
| 5 | Incident, support burden, poor recovery, degraded mode | `QAS#` + related `REQ#` | `specify-requirements` |
| 6 | Audit/compliance finding | Obligation, trace, requirement, transition behavior | `specify-requirements`; `define-release` if scope commitment changes |
| 7 | Terminology/rule/ownership confusion | Domain glossary, rule, invariant, context | `domain-modeling` (existing local skill — **not one of the seven skillset skills**; update 7 must state this is an external/local call, then affected requirements) |
| 8 | Foundational actor/outcome/value/boundary assumption contradicted | Vision (explicit `DEC#` required per update 10) | `brainstorm-vision` / `create-vision-companion` refresh, evidence chain preserved |
| 9 | Evidence too weak or instrumentation invalid | Analysis plan + observation requirement | None — no scope verdict; measurement repair / gather evidence (stays in `validate-release`) |
| 10 | Scope retired | Transition requirements | `specify-requirements` (migration, communication, coexistence, decommissioning) |

Every route must carry: exact artifact IDs, single decision owner, preserved decisions, required new evidence, urgency, closure condition (ledger §5 tail + §6 linter checks). Handover contract per VR-EXT-05. Intentional skips and perseverance are recorded with rationale (§6: "perseverance is recorded with rationale just as reopening is").

### Evidence routing: vision vs downstream (update 10)

- **To vision (only):** evidence contradicting a **foundational actor/outcome/value/principle/boundary assumption** — condition 8. Requires an explicit `DEC#` citing the invalidating evidence; `validate-release` routes, it never edits the vision. Sources: VR-MTH-08, ledger §9 ("do not reopen the vision when a lower-level opportunity, scope, journey, requirement, or QAS explains the evidence"), `validation_and_feedback.md` "route a finding downstream first… only the last is a vision pivot".
- **Downstream (everything else):** conditions 1–7, 9, 10 are **discovery pivots** — routed to opportunities, assumptions, scope, journeys, requirements, QAS, domain artifacts, analysis plan, or transition requirements.
- **Refusal behaviors the plan must wire** (align with contract update 3 scenarios): failed-experiment/failed-release evidence wrongly escalated to a vision rewrite → refuse and reroute downstream (over-escalation test, VR-MTH-08); genuine vision-invalidating evidence without `DEC#` → block (under-escalation test covers the inverse); one weak anecdote reopening everything → evidence-strength cap (VR-EXT-08); sunk-cost reopening nothing → perseverance-with-rationale rule.

## 8. Missing method-owned rows (updates 9 & 10)

The ledger has fragments of ownership/vision rules scattered in §§4–6, 9 but **no method-owned rows** as the contract requires ("Add method-owned rows… for applicable collaboration/decision-ownership and vision-stability rules"; update 10 explicitly reopens the `validate-release` ledger). Proposed rows:

| Proposed ID | Rule | Intended incorporation | Objective evidence |
| --- | --- | --- | --- |
| VR-M01 | **Singular accountable review ownership** — every review and every re-entry has exactly one named accountable owner; a group or department is not an owner; escalation path per `lifecycle-onepager.md` | Analysis-plan gate field (§4 "named decision owner"), re-entry-route owner field (§5), linter rules "review owner present" and "each re-entry has one owner" (§6) extended to **reject group/department owners** | Group-only-owner fixture is refused (contract update 3 scenario); linter fails a re-entry route with a team name as owner |
| VR-M02 | **Required specialist evidence; no fabrication** — engineering/ops/security/compliance/domain input is imported when material to a finding (operational evidence, guardrail breach, compliance finding); product management must not fabricate specialist evidence | Evidence-intake contract (VR-EXT-09 path) + analysis-plan "qualitative and operational evidence sources" + prompt guardrail: findings in specialist territory require a source-addressable specialist `EV#` or an explicit open marker | Missing-required-specialist-input fixture detected and refused (contract update 3 scenario); a guardrail-breach verdict without operational `EV#` fails the linter |
| VR-M03 | **Vision-stability escalation guard** — vision reopening only via explicit `DEC#` citing foundational-assumption-invalidating evidence; all other findings are discovery pivots routed downstream; `validate-release` never edits the vision | Re-entry matrix condition 8 gate; prompt guardrail; linter rule "vision re-entry cites a `DEC#` with invalidating evidence"; each re-entry labeled discovery pivot vs vision pivot | Over-escalation fixture (failed release → vision rewrite) refused and rerouted; genuine vision-invalidating fixture passes only with `DEC#` (contract update 3 scenarios) |
| VR-M04 | **Refusal to proceed on invalidated upstream artifacts / boundary handoff** — when evidence invalidates an upstream artifact, continuing dependent work without reopening it is refused; re-entries crossing a decision-authority (department) boundary name owner + escalation path from `lifecycle-onepager.md` | Handover contract (VR-EXT-05) extended with authority-boundary field; finalize check: no route closed while its reopened artifact is unresolved unless perseverance is recorded with rationale | Refusal-to-reopen fixture and department-boundary-handoff fixture detected (contract update 3 scenarios) |

(Update 10's strategy-section and roadmap rules do not apply to `validate-release` — strategy checks land in `discover-product`/`define-release`, roadmap in `tailor-lifecycle`/`define-release`. No rows proposed for those here.)

## Additional note for update 2 (instrumentation contract)

`validation_and_feedback.md`'s instrumentation contract ("Instrumentation is a requirement, not an afterthought… a release whose outcome cannot be observed cannot be validated") maps to `validate-release` as the **consuming end**: linter rules already in ledger §6 — outcome/guardrail measures observable; missing/invalid instrumentation → inconclusive/measurement-repair outcome, never a fabricated verdict; first review scheduled with named owner **before** shipping. The producing end (`define-release` defines instrumentation/observation requirements; `specify-requirements` carries them as `REQ#`) belongs to those ledgers; the update-2 sub-agent must state the three-skill mapping in the method-doc coverage table.
