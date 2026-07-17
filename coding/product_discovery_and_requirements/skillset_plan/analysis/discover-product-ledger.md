# Phase 0 digest — `discover-product` ledger audit

**Frozen input for write-phase agents.** Sources read: `skillset_plan_update_plan.md` (contract), `discover-product-contributions.md` (ledger), and ledger-cited method docs `product_discovery.md`, `lifecycle_tailoring.md`. Primary consumers: ordered updates 1 (owner), 4, 6, 9, 10.

## 1. Row inventory

31 external/proprietary rows, DP-001 … DP-031. No gaps, no duplicate IDs.

| ID | Source | License | Mode | Final disposition | Intended incorporation (one line) |
| --- | --- | --- | --- | --- | --- |
| DP-001 | huntsyea/product-skills `continuous-discovery` | MIT | Distill | Adopt (audit-conditioned) | Distill techniques/anti-patterns while preserving the seven-step loop |
| DP-002 | huntsyea/product-skills `jobs-to-be-done` | MIT | Distill | Adopt (audit-conditioned) | Optional JTBD switch-interview/forces routing for motivation uncertainty |
| DP-003 | huntsyea references | MIT | Distill | Adopt (audit-conditioned) | Map each anti-pattern to a guardrail, finalize check, or explicit rejection |
| DP-004 | assimovt/productskills `user-interview` | MIT | Distill | Adopt (audit-conditioned) | Mom-Test past-behavior guardrails; opinions/hypotheticals classified weak |
| DP-005 | assimovt `problem-validation` | MIT | Distill | Adapt (audit-conditioned) | Frequency/intensity/willingness-to-pay rubric, non-universal |
| DP-006 | assimovt `opportunity-mapping` | MIT | Distill | Adapt (audit-conditioned) | Solution-neutrality/hierarchy checks merged into `OPP#` model |
| DP-007 | assimovt `experiment-design` | MIT | Distill | Adopt (audit-conditioned) | Method selection/criteria/decision linkage without replacing `EXP#` schema |
| DP-008 | jacksoncalling/argo | Not established | Pattern | Adapt | Rich/Mixed/Thin interview-quality rubric on every interview `EV#` |
| DP-009 | jacksoncalling/argo | Pattern only | Pattern | Adapt | Confidence capped by evidence quality; ceiling override needs `DEC#` |
| DP-010 | jacksoncalling/argo | Pattern only | Pattern | Adapt | Opportunity routing add/merge/escalate/park with provenance |
| DP-011 | jacksoncalling/argo | Pattern only | Pattern | Adapt | Human gate before solutioning; AFK proposals marked awaiting review |
| DP-012 | Argo + huntsyea + phuryn (convergent) | Per-donor; independent impl. | Pattern/Distill | Adopt | ≥3 materially different `SOL#` directions incl. process/policy/manual/no-build |
| DP-013 | Gap analysis + method step 4 | Proprietary | Proprietary correction | Adopt | `SOL#` layer: `OPP → SOL → ASM → EXP`; linter validates chain |
| DP-014 | shinpr/claude-code-discover | MIT | Pattern | Adapt | Experiment card merged with per-risk confidence + time budget |
| DP-015 | shinpr hypothesis verifier | MIT | Pattern | Adapt | Context-separated critic for maps/cards (primary home: `specify-requirements`) |
| DP-016 | shinpr | MIT | Pattern | Adapt | All `EV/OPP/SOL/ASM/EXP/DEC` discoverable via workspace index |
| DP-017 | phuryn/pm-skills | MIT | Pattern | Adapt | Wrap-up handover: verdict, next lifecycle stage, exact input artifacts |
| DP-018 | deanpeters/Product-Manager-Skills | CC BY-NC-SA 4.0 | Pattern/reference-only | Adapt (independent authoring) | Premature-convergence warning authored independently; no copying |
| DP-019 | Method docs + discovery packs | Proprietary orch.; donor per license | Pattern/Distill | Adopt | Cheapest-trustworthy-test method selection across all four risks |
| DP-020 | Proprietary `prototype` skill | Internal | Call/reuse | Adopt | Bounded prototype handoff passing `EXP#`/`ASM#`/criteria/decision context |
| DP-021 | Proprietary quality method | Proprietary | Policy | Adopt | Surface architecture-changing quality risks as classified assumptions, not `QAS#` |
| DP-022 | Proprietary domain method + `domain-modeling` | Internal | Call/reuse | Adopt | Trigger domain work on contested terminology/rules/boundaries |
| DP-023 | Problem-Based-SRS pattern + gap analysis | SRS MIT; linter proprietary | Pattern/shared script | Adopt | Shared deterministic linter at finalize (IDs, citations, `SOL` chains, `EXP` fields) |
| DP-024 | ForceInjection/ddd-skills | Pattern only (license unconfirmed) | Pattern | Adapt | Verdicts become explicit reopen instructions tied to named artifacts |
| DP-025 | ForceInjection/ddd-skills | Pattern only | Pattern | Adapt | Blind-run validation against fixed reference topic with scored report |
| DP-026 | Cross-cutting finding | Mandatory | Policy | Adopt | Provenance on distilled files; pinned calls; no live fetching |
| DP-027 | Coverage assurance requirement | — | Authoring process | Adopt | Full donor-file audit; new candidates get new `DP-*` IDs |
| DP-028 | Proprietary invariant | Mandatory | Policy | Adopt | Evidence non-fabrication; missing evidence stays an explicit gap |
| DP-029 | Cross-cutting finding | Mandatory | Policy | Adopt | One proprietary spine; no donor IDs/folders/taxonomies imported |
| DP-030 | Method failure mode | Proprietary | Policy | Adopt | Predeclared decision thresholds end research |
| DP-031 | Method requirement + shinpr pattern | MIT (shinpr) | Pattern | Adapt | Rejected/deferred `SOL#` remain traceable, never silently deleted |

**Counts:** Adopt 17 (DP-001–004, 007, 012, 013, 019–023, 026–030) · Adapt 14 (DP-005, 006, 008–011, 014–018, 024, 025, 031) · Call 2 of the Adopts are call-mode (DP-020, DP-022) · Reject 0 · Defer 0 · Pending 0.

## 2. Compliance audit against contract ledger rules

- **Required fields:** every row has stable ID, source, mode, incorporation, disposition, and objective evidence (Verification column). License present on all rows; DP-008/024/025 record "pattern only unless/until license confirmed" — acceptable as a constraint, not a missing field. DP-027 has no license field (pure authoring-process row; nothing to license).
- **Pending:** zero rows are `Pending audit`. Seven distill rows carry the qualifier "subject to source audit" — a scheduled authoring-time condition, not a Pending disposition. This matches the acceptance-gate requirement that every distill row have a future donor-audit task, but write-phase agents should keep the qualifier visible in the plan so it is not mistaken for completed vendoring.
- **Realizing artifacts:** every accepted row cites a concrete verification target (fixture, linter/mutation test, schema check, finalize gate, or integration test). None is prose-only.
- **Rejected/deferred rows:** no `Reject`/`Defer` rows exist; rejections and deferrals live in the prose "Exclusions and deferrals" section. Contract says "preserve rejected and deferred rows" — the prose section satisfies preservation, but update 4 should not expect row-level Reject/Defer IDs from this ledger. Minor gap: prose deferrals have no stable IDs (see §6).

## 3. Accepted rows — realizing mechanism the revised plan must contain (update 4)

- DP-001/002/003/019 — distilled technique/anti-pattern content vendored into skill reference files; anti-pattern coverage table; technique-routing rules.
- DP-004/005 — interview and problem-validation guardrail prompts; evidence-classification fixtures; no `EV#` without a supplied source.
- DP-006/013/016/023 — `OPP#`/`SOL#` model checks in the shared deterministic linter (ID format, dangling `OPP→SOL→ASM→EXP` links, unindexed artifacts, reserved names) run at finalize.
- DP-007/014/019 — `EXP#` schema fields (decision, `ASM#`, evidence needed, method, budget, preregistered support/refute/inconclusive, result, per-risk confidence, next step) exposed to the linter — feeds update 6.
- DP-008/009 — Rich/Mixed/Thin rubric plus confidence-cap rule with `DEC#` override; golden fixtures.
- DP-010/011 — routing decision (add/merge/escalate/park) required per opportunity; explicit human gate before solution generation; AFK-mode "awaiting review" marker.
- DP-012 — finalize refusal: single solution direction blocks unless an explicit `DEC#` records why alternatives are not viable — the update-1 refusal gate.
- DP-015 — separated critic contract (critic gets artifacts/rules, not builder expectations).
- DP-017/024 — handover block: verdict, next lifecycle stage from the one-pager, changed artifacts, reopen instructions naming `SOL#`/`ASM#` — feeds update 7 but must appear in the plan's skill section per update 4.
- DP-018 — independently authored premature-convergence prompts; reference-only audit proving no deanpeters text.
- DP-020/022 — bounded internal calls (see §5).
- DP-021 — early quality-risk prompt producing classified assumptions, explicitly not `QAS#`.
- DP-025 — reference-topic blind run scored against completion checks (feeds update 3).
- DP-026–030 — plan-level policy statements: provenance manifest, full donor audit, non-fabrication, single spine, decision thresholds.
- DP-031 — rejected-alternative memory: rejected `SOL#` retained with reasons, linter-visible.

## 4. `distill` rows — provenance status

| Row | Donor repo/path | Commit/tag or date | License/attribution | Vendored? |
| --- | --- | --- | --- | --- |
| DP-001 | huntsyea/product-skills — `continuous-discovery` tree | **Not recorded** | MIT; attribution required | No |
| DP-002 | huntsyea/product-skills — `jobs-to-be-done` | **Not recorded** | MIT | No |
| DP-003 | huntsyea/product-skills — references | **Not recorded** | MIT | No |
| DP-004 | assimovt/productskills — `user-interview` | **Not recorded** | MIT | No |
| DP-005 | assimovt/productskills — `problem-validation` | **Not recorded** | MIT | No |
| DP-006 | assimovt/productskills — `opportunity-mapping` | **Not recorded** | MIT | No |
| DP-007 | assimovt/productskills — `experiment-design` | **Not recorded** | MIT | No |
| DP-012 | (partial distill) huntsyea ideation; phuryn brainstorming chain | **Not recorded** | Per-donor; convergent requirement implemented independently | No |
| DP-019 | (partial distill) discovery packs | **Not recorded** | Donor content per license | No |

No pinned revisions and no vendored material exist yet. The ledger's "Focused external source-audit manifest" (8 repos, required paths, per-file recording rules) is the scheduled authoring-time donor-audit task the acceptance gate requires; the plan must carry it forward explicitly.

**deanpeters flag:** DP-018 is the only deanpeters row. It is correctly reference-only (CC BY-NC-SA 4.0, "no copying/distillation", verification includes a reference-only audit). No deanpeters distill exists. Keep the prohibition wired into the plan's provenance policy.

## 5. `Call` rows

| Row | Callee | Bounded role | Version pinning | Fallback |
| --- | --- | --- | --- | --- |
| DP-020 | `prototype` (internal skill) | Only when a prototype is the smallest trustworthy test; passes `EXP#`, `ASM#`, criteria, decision context; findings return to the same `EXP#`; recorded observation required before output counts as evidence | "Pin compatible contract" (stated) | **Missing** — no behavior defined when `prototype` is unavailable |
| DP-022 | `domain-modeling` (internal skill) | Invoke/recommend when contested terminology, rules, ownership, events, or boundaries affect discovery; updates canonical domain artifacts, no competing glossary | **Not stated** | **Missing** |

Neither call owns spine artifacts (compliant). Update 4 should add explicit fallbacks (e.g. record the gap and continue with a cheaper test / recommend manual domain session) and a pinning statement for DP-022.

**`north-star` specialist (contract update 4):** no `discover-product` row exists, and none is needed — the ledger's Exclusions section explicitly routes "North-star metric auditing belongs to `define-release` and `validate-release`." Update 4 must not attach `north-star` to `discover-product`.

## 6. `Defer` rows

No `Defer` ledger rows. Prose deferrals in "Exclusions and deferrals" all name a receiving owner:

- Story mapping, Shape Up, scope cutting, bet sizing, Obligation/Expectation/Hope, release-scope commitment → `define-release`.
- North-star metric auditing → `define-release` and `validate-release`.
- NFR review, quality-scenario writing, final `QAS#`, full use cases/requirements → `specify-requirements`.
- Post-release analysis planning → `validate-release`.
- Tactical DDD, architecture, EventStorming-to-design, design catalogs → future design skillset.

All destinations named (acceptance-gate compliant). Optional hardening: promote the design-skillset deferral to a stable ID if the gate's "every deferred design/domain item names its future design-skillset destination" check demands row-level traceability.

## 7. Update-1 readiness (solution alternatives — this ledger is primary)

**Already in place (ledger + product_discovery.md):**

- `product_discovery.md` already contains loop step "4. Generate alternatives" between "3. Map opportunities" and "5. Expose assumptions", with process/policy/manual-service/no-build options, and the completion check "Alternative solutions were considered". Update 1's phase insertion is a **plan-level** sync, not a method-doc change.
- DP-012: ≥3 materially different directions; finalize blocks a single solution unless an explicit `DEC#` explains why alternatives are not meaningful.
- DP-013: full `SOL#` trace layer — `SOL#` cites `OPP#`; solution-specific `ASM#` cites `SOL#`; solution-independent `ASM#` may cite `OPP#`; linter validates `OPP → SOL → ASM → EXP` and reports dangling links.
- DP-031: rejected/deferred `SOL#` memory.
- Artifact/trace contract has a `SOL#` row (selected `OPP#`, materially distinct direction, category). Coverage-gate checkboxes require `SOL#` in ID inventory, artifact model, companion reservation, trace model, linter, and fixtures — including the companion `SOL` reservation update 1 mandates.

**What update 1 must still add (not decided/present in ledger or method doc):**

1. **Durable representation choice** — `solutions.md` vs a section of `opportunities.md`. Nowhere decided; update 1 must choose and record it.
2. **`EXP#` → `SOL#` citation** — contract requires `EXP#` to cite the applicable `SOL#`. The ledger's `EXP#` artifact-contract row and DP-013/DP-014 only require citing `ASM#` (and decision). This field is absent everywhere in the ledger; update 1 (and update 6's schema merge) must add it.
3. **Refusal-gate placement** — contract: refuse **solution-assumption ranking** with only one direction (unless `DEC#`). Ledger places the block at **finalize** (DP-012). Update 1 should wire the refusal at ranking time as well as finalize.
4. **Plan-wide synchronization** — artifact table, method-doc coverage, trace description/diagram, loop and discovery phases, linter spec, and reference-topic rubric in the target plan; the ledger already anticipates these via gate checkboxes but the plan sections are the write targets.
5. **`SOL` reservation in `create-vision-companion` Phase 0** — the coverage gate names "companion reservation", but the realizing edit belongs to the plan's companion section (cross-skill; not this ledger's write scope).
6. **Update-6 tie-in** — merge target confirmed: `product_discovery.md` experiment card (decision, assumption, evidence needed, method, criteria, result/confidence, next step) + DP-014's per-risk confidence and time budget + missing `SOL#` and resulting `DEC#` fields, all linter-exposed (DP-007, DP-023).

## 8. Method-owned rows missing for updates 9 & 10

The ledger has **no method-owned rows** for collaboration/decision-ownership or vision-stability. Applicable rules and proposed rows (pattern mirrors `BV-M01` naming; no external license/disposition needed):

| Proposed ID | Rule (source) | Intended incorporation | Objective evidence |
| --- | --- | --- | --- |
| DP-M01 | Discovery pivot vs vision pivot: adapt decisions are discovery pivots within a stable vision; `discover-product` never edits the vision; vision-invalidating evidence is routed to `brainstorm-vision` via explicit `DEC#` recommendation (product_discovery.md §7; contract update 10) | Wrap-up guardrail + `DEC#` routing rule + finalize check | Regression scenarios: "failed experiment wrongly escalated to a vision rewrite" refused/rerouted; "genuine vision-invalidating evidence with explicit `DEC#`" passes |
| DP-M02 | Opportunity selection checked against the product-strategy ordered-outcomes section of the vision one-pager; divergence needs an explicit `DEC#`; strategy reordering is itself a discovery pivot, never a vision edit (contract update 10) | Opportunity-selection prompt + finalize check reading the companion-derived strategy index | Fixture: off-strategy `OPP#` selection blocks without `DEC#`; strategy-reorder fixture records a discovery-pivot `DEC#` |
| DP-M03 | Singular accountable decision ownership: every proceed/adapt/pause/abandon `DEC#` names one accountable owner per `lifecycle-onepager.md`; a group/trio/department is not an owner; escalation path recorded (lifecycle_tailoring.md step 5; contract update 9) | `DEC#` owner field validation (owner already a `DEC#` field in the artifact contract — tighten to named individual) + refusal behavior | Regression scenario: "group-only owner" detected and refused; linter/fixture rejects group-valued owner |
| DP-M04 | Required specialist participation: when feasibility/viability/quality evidence is material, actual engineering/design/ops/security/compliance/domain input is required; the agent must not fabricate specialist evidence and must flag the gap (contract update 9; extends DP-021, DP-028) | Evidence-gathering prompt + explicit-gap marker + finalize check | Regression scenario: "missing required specialist/engineering input" detected and refused; adversarial fixture leaves gap explicit |

Update 10's ledger-reopen list includes `discover-product`; these four rows are the applicable additions (roadmap ceremony-gating belongs to `tailor-lifecycle`/`define-release`, not here; department-boundary handoff belongs to handover, partially covered by DP-017/DP-024 and can be referenced rather than duplicated).

## Blocking issues (ranked)

1. `EXP#`→`SOL#` citation absent from every `EXP#` definition in the ledger (updates 1 and 6 must add it consistently).
2. Durable `SOL#` representation (`solutions.md` vs `opportunities.md` section) undecided.
3. No method-owned rows for updates 9–10 (proposals above).
4. Distill rows have no pinned revisions and nothing vendored — future donor-audit task must be carried into the plan verbatim.
5. Call rows DP-020/DP-022 lack fallbacks; DP-022 lacks a pinning statement.
6. Refusal gate currently finalize-only; contract requires it at solution-assumption ranking.
