# Phase 0 digest — `define-release` ledger audit

**Source ledger:** `skillset_plan/define-release-contributions.md` (read 2026-07-16)
**Method docs opened (cited by ledger):** `../validation_and_feedback.md`, `../product_definition.md`
**Status:** frozen input for Phase 1 write agents (esp. updates 2, 4, 9, 10).

## 1. Row inventory

### External rows (§2)

| ID | Source | License | Mode | Disposition | Intended incorporation (one line) |
| --- | --- | --- | --- | --- | --- |
| DR-EXT-01 | `huntsyea/product-skills` `story-mapping` | MIT | distill | adopt | Progressive-disclosure story-mapping reference for shaping journeys and cutting a coherent release |
| DR-EXT-02 | `huntsyea/product-skills` `shape-up` | MIT | distill | adapt | Optional appetite/shaping path translated into the proprietary `REL` artifact, no competing pitch artifact |
| DR-EXT-03 | `assimovt/productskills` `scope-cutting` | MIT | distill | adopt | Scope-cutting prompts and failure checks; distinguish "small" from "coherent" |
| DR-EXT-04 | `assimovt/productskills` `bet-sizing` | MIT | distill | adapt | Proportional-investment check complementing ceremony and release stop criteria |
| DR-EXT-05 | `assimovt/productskills` `prd-writing` | MIT | distill | adapt | Evidence-first scope-rationale guardrails only; no PRD artifact or taxonomy import |
| DR-EXT-06 | `RafaelGorski/Problem-Based-SRS` | MIT | pattern | adapt | Obligation/Expectation/Hope classification of mandatory scope drivers; obligation requires a consequence; no `CP/CN/FR` IDs |
| DR-EXT-07 | `ai-analyst-lab/north-star` | MIT (code); Amplitude-derived content needs provenance review | call | adopt | Version-pinned metric-audit step for release success measures; audit outcome or justified skip written into `REL` review metadata |
| DR-EXT-08 | `phuryn/pm-skills` north-star-metric / metric tree | MIT | reference/pattern | **adapt or reject (conditional — not final)** | Retain only metric-tree ideas complementary to DR-EXT-07; no second runtime dependency |
| DR-EXT-09 | `shinpr/claude-code-discover` hypothesis format | MIT | pattern | adapt | Strengthen release-hypothesis section (success/failure criteria, confidence by risk dimension, time budget, rejected alternatives) within the `REL` schema |
| DR-EXT-10 | `deanpeters/Product-Manager-Skills` `user-story-mapping` | **CC BY-NC-SA 4.0** | reference only | reject (for distillation) | Documented coverage comparison only; no text or protected sequence copied |
| DR-EXT-11 | `phuryn/pm-skills` command chaining | MIT (pattern only) | pattern | adopt | Final response names next stage per `lifecycle-onepager.md`, input files, blockers, resume point |
| DR-EXT-12 | `ForceInjection/domain-driven-design-skills` | **WIP / uncertain** | pattern | adapt | Quantitative backtracking-trigger matrix: precise triggers for returning to discovery, reopening vision, requesting domain work, or stopping definition |

### Method-coverage rows (§3)

DR-MTH-01..12 map all twelve method docs (overview, lifecycle_tailoring, product_vision, product_discovery, product_definition, use_cases_and_story_mapping, domain_discovery, quality_attributes, requirements_engineering, validation_and_feedback, glossary, resources) to required uses and verifications. All twelve rows are complete (ID, doc, required use, verification). These are coverage rows, not the contract's "method-owned rows" for updates 9–10 — see §8.

## 2. Compliance audit vs contract ledger rules

- **Required fields:** every external row has stable ID, source, license, reuse mode, intended incorporation ("Required incorporation"), disposition, and objective evidence ("Verification"). No field is empty.
- **Pending rows:** zero rows literally `Pending`. **One effectively unresolved: DR-EXT-08 disposition is "adapt or reject"** — a conditional pending the DR-EXT-07 comparison. Update-4 agent must resolve it to a single final disposition (or split the row).
- **Commit/SHA + retrieval date:** absent for every row. The §2 preamble intentionally defers this to pre-authoring ("replace every source pointer below with the exact repository URL, commit SHA or release, files inspected, retrieval date, and verified license"). This satisfies the acceptance-gate requirement of a *future authoring-time donor-audit task*, but no row is audit-complete today.
- **Realizing artifact citation:** accepted rows cite fixtures/checks in the Verification column, and ledger §4 (deterministic checks) plus §5 (coverage gate) realize most of them. What accepted rows do *not* yet cite is a plan section — update 4 must add plan locations (contract update 8 later requires actual file/section/test).
- **Disposition vocabulary:** ledger uses lowercase `adopt/adapt/reject/defer` vs contract's `Adopt/Adapt/Call/Reject/Defer`. DR-EXT-07 is disposition `adopt` with mode `call`; under the contract's vocabulary its final disposition should read `Call`. Cosmetic but worth normalizing in update 4.

## 3. Accepted rows — realizing mechanism required in the revised plan (update 4)

| ID | Realizing mechanism the plan must contain |
| --- | --- |
| DR-EXT-01 | Story-mapping reference file in `define-release` (progressive disclosure); linter/fixture: slice spans end-to-end journey, single-layer slice rejected (§4 bullet 8) |
| DR-EXT-02 | Optional shaping/appetite path in skill prose, ceremony-gated; appetite recorded inside `REL`, never a separate pitch artifact; low/high-ceremony fixtures |
| DR-EXT-03 | Scope-cutting prompts + finalize failure check; negative fixture with disconnected items fails finalization |
| DR-EXT-04 | Proportional-investment (bet-sizing) check tied to ceremony and stop criteria; reversibility fixture |
| DR-EXT-05 | Evidence-first guardrail: every scope decision resolves to evidence or carries explicit `DEC` override (linter §4 bullet 3) |
| DR-EXT-06 | O/E/H classification field on mandatory scope items; deterministic check: unclassified "must" or obligation without consequence fails (§4 bullet 5) |
| DR-EXT-07 | Skills-table entry for callable specialist `north-star` (contract update 4 names it explicitly): bounded role, version policy, inputs, outputs, fallback; audit-or-justified-skip recorded in `REL` review metadata; vanity-metric fixture |
| DR-EXT-09 | Enriched `REL` hypothesis section: predeclared success/failure/inconclusive interpretation, confidence per risk dimension, time budget, investment boundary; post-ship judgeability fixture (dovetails with update 6's `EXP#` schema work) |
| DR-EXT-11 | Handover contract: final response names next stage from `lifecycle-onepager.md`, exact input artifacts, unresolved blockers, resume point; handover test into `specify-requirements` (feeds update 7) |
| DR-EXT-12 | Backtracking-trigger matrix: each trigger maps to one artifact, decision owner, and next skill; ambiguous "go back" fails review (feeds updates 4 and 7) — pattern-mode local implementation only, given WIP license |

## 4. `distill` rows — provenance status

| ID | Donor repo/path | Commit/retrieval date | License/attribution | Vendored? |
| --- | --- | --- | --- | --- |
| DR-EXT-01 | `huntsyea/product-skills` — `story-mapping` refs/workflows | **not recorded** (must also record former `rohanpatriot` location) | MIT, attribution required | **No** |
| DR-EXT-02 | `huntsyea/product-skills` — `shape-up` refs/workflows | not recorded | MIT | No |
| DR-EXT-03 | `assimovt/productskills` — `scope-cutting` | not recorded | MIT | No |
| DR-EXT-04 | `assimovt/productskills` — `bet-sizing` | not recorded | MIT | No |
| DR-EXT-05 | `assimovt/productskills` — `prd-writing` | not recorded | MIT | No |

Nothing is vendored yet; all donor audits are deferred to authoring time per §2 preamble (per-file audit, commit/tag, retrieval date, attribution). **deanpeters flag:** DR-EXT-10 (CC BY-NC-SA) is correctly *not* a distill row — reference-only, reject-for-distillation, comparison documented, "no text or protected sequence copied" verification. Ledger §7 repeats the prohibition. Compliant with the contract's deanpeters rule; no deanpeters content is scheduled for vendoring.

## 5. `Call` rows

Single call row: **DR-EXT-07** (`ai-analyst-lab/north-star`).

- **Bounded role:** present — metric-audit step for release success measures only; writes audit outcome (or justified skip) into `REL` review metadata; does not own spine artifacts.
- **Version-pinning:** required by the row ("verify the pinned version and preserve notices") but **no concrete pin recorded** — write phase must state the version policy in the skills table.
- **Fallback:** partially present — "justified skip" path in the row and gate checkbox "every runtime call is version-pinned and has a documented unavailable/failed-call fallback" (§5), but **no explicit failed/unavailable-call behavior defined per row** (skip vs block vs manual audit). Update 4 must define inputs, outputs, and fallback explicitly.
- **Caveat recorded:** Amplitude-derived content requires provenance review and must not be vendored casually.
- DR-EXT-08 is the guard against a *second* runtime dependency; its resolution depends on DR-EXT-07 evaluation.

## 6. `Defer` rows

**No external row carries disposition `defer`.** Deferrals exist only as §7 prose: external design packs — `45ck` beyond QAS, `lagz0ne`, DDD tactical-design skills, DDD Crew canvases — "remain deferred to the future design-skillset plan." The destination *is* named (future design-skillset plan), satisfying the acceptance-gate destination requirement, but these deferrals have **no stable row IDs** and thus cannot be preserved/traced as rows per the contract ("Preserve rejected and deferred rows"). Recommend the update-4 agent either confirm these are owned by other ledgers or add ID'd defer rows here.

## 7. Update-2 readiness — REL checks the deterministic linter must enforce

Ledger §4 already specifies a near-complete REL check set; contract update 2 and the cited method docs add the rest.

From ledger §4 (existing, keep):
1. `REL#` unique; filename and internal identifier agree.
2. Every cited `OPP#`, `EV#`, `CAP#`, `UC#`, `ASM#`, `EXP#`, `DEC#` resolves.
3. In-scope capability → selected opportunity + evidence, unless dated `DEC#` override with owner and rationale.
4. Deferred/rejected opportunities have reasons.
5. O/E/H classification on every mandatory item; each obligation has a consequence (DR-EXT-06).
6. Exactly one named hypothesis plus success, guardrail, and stop criteria (matches contract update 2's REL bullet).
7. Every outcome and guardrail measure has an observation or instrumentation handoff (matches update 2's "instrumentation/observation requirements for outcome and guardrail criteria").
8. Slice spans an end-to-end journey, or a recorded deliberate story-mapping skip.
9. Vision-boundary-conflicting scope marked unresolved; cannot silently pass.
10. Decision owner, decision date, next review owner, intended review timing exist.
11. Handover fields name next stage and exact input artifacts.

From `validation_and_feedback.md` (instrumentation contract — update 2 requires mapping it to `define-release`, `specify-requirements`, `validate-release` in the method-doc coverage table):
- "Instrumentation is a requirement, not an afterthought": how each outcome and guardrail will be observed in production is defined during product definition and requirements engineering; "a release whose outcome cannot be observed cannot be validated." → linter check 7 above is the deterministic realization; the handoff target is `specify-requirements` (DR-MTH-09's "instrumentation handoff test").
- First outcome review scheduled **before ship** with a named owner; guardrails monitored continuously → realized by check 10 (review owner + timing).
- Usage ≠ outcome / vanity-metric rejection → judgment-gate side (DR-EXT-07 call), not deterministic; linter only checks presence, the audit checks quality. Keep the deterministic/judgment separation explicit.

From `product_definition.md`: hypothesis + success/guardrail/stop must exist *before work starts* (activity 6, completion checks) — consistent with checks 6/10.

**Gap vs contract update 2:** ledger §4 has **no roadmap-entry check** ("an outcome is mandatory; feature/date-only entries are invalid"). Since update 10 makes `define-release` the maintainer of the ceremony-gated now/next/later roadmap, the update-2 agent must add this check for topics where the roadmap is adopted (see proposed DR-M04).

## 8. Missing method-owned rows (updates 9 & 10) — proposals

The ledger has no method-owned rows for collaboration/decision-ownership or vision-stability. DR-MTH-03 (vision boundary) and §4 checks 9–10 partially cover the behavior, but the contract requires explicit method-owned rows with stable local IDs, intended incorporation, and objective evidence. Proposed:

| Proposed ID | Rule (contract source) | Intended incorporation | Objective evidence |
| --- | --- | --- | --- |
| DR-M01 | Singular accountable decision ownership (update 9): one named accountable owner per release decision — a group or department is not an owner — plus required contributors, specialist authorities, approvers, evidence required, escalation path, evidence-based reopen trigger | `REL` decision-metadata fields + finalize gate; linter extends existing owner/date check to reject group-only owners; per-decision escalation path and reopen trigger recorded per `lifecycle-onepager.md` | Regression scenario "group-only owner" (contract update 3) is detected and refused; linter mutation fixture with a department as owner fails |
| DR-M02 | Required specialist participation (update 9): early engineering/design/ops/security/compliance/domain input when their evidence is material; product must not fabricate specialist evidence | Participation prompts + finalize check in `define-release`; missing required specialist input blocks finalize or records an explicit `DEC#` skip | Regression scenario "missing required specialist/engineering input" refused; missing-input fixture fails finalize |
| DR-M03 | Opportunity-selection-vs-strategy check (update 10; `product_definition.md` activity 1): selection checked against the strategy's thin ordered-outcomes section; a selection fighting the strategy needs a strategy conversation, not silent reordering; strategy reordering is a discovery pivot | Explicit strategy-check step in scope selection; conflict routes to strategy conversation/`DEC#`, never a silent vision or strategy edit | Fixture: selection contradicting ordered outcomes is flagged and cannot pass without a recorded strategy decision |
| DR-M04 | Ceremony-gated outcome-based rolling now/next/later roadmap (update 10): when `tailor-lifecycle` records adoption, `define-release` maintains it; never required for low-ceremony topics | Optional roadmap section maintained by `define-release`; linter rule: roadmap entries must carry an outcome, feature/date-only entries invalid (closes the §7 gap above) | Regression scenarios "roadmap skipped for low ceremony" and "adopted for high coordination" (update 3) both pass; feature-only roadmap entry fails lint |
| DR-M05 | Discovery-pivot vs vision-pivot routing (update 10): `define-release` escalates vision-boundary conflicts and evidence findings downstream (opportunities, solutions, scope, strategy); it never edits the vision; only `brainstorm-vision`/`create-vision-companion` may vision-pivot via explicit `DEC#` | Backtracking-trigger matrix (DR-EXT-12) entries route vision conflicts to a vision re-entry request, not a vision edit; sharpens DR-MTH-03 | Boundary-conflict fixture produces a re-entry request with `DEC#`, and the "failed experiment wrongly escalated to a vision rewrite" scenario is refused |

These rows need no external license or disposition (contract, ledger-rules section).

## Top blocking issues

1. **DR-EXT-08 has a conditional disposition ("adapt or reject")** — violates "no row may remain Pending" in spirit; must be resolved in update 4.
2. **No method-owned rows exist** for updates 9–10; five proposed above (DR-M01..M05), including the roadmap linter rule absent from ledger §4.
3. **DR-EXT-07 call contract is incomplete**: no concrete version pin, no explicit inputs/outputs, no defined failed-call behavior beyond "justified skip".
4. **§7 deferrals lack row IDs**; confirm ownership or convert to `Defer` rows.
5. **DR-EXT-12 license is WIP/uncertain** — keep strictly pattern-mode (local implementation, inspiration recorded, no copied text) per the unlicensed-material rule.
