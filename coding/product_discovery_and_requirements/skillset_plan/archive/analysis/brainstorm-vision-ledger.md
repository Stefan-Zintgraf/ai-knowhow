# Phase 0 digest — `brainstorm-vision` ledger audit

**Ledger:** `skillset_plan/brainstorm-vision-contributions.md`
**Method docs consulted (cited by ledger):** `product_vision.md`, `overview.md`
**Contract basis:** `skillset_plan_update_plan.md` — ledger rules + ordered updates 4, 9, 10

## 1. Row inventory

### External rows (BV-E)

| ID | Source | License | Reuse mode | Disposition | Intended incorporation (one line) |
| --- | --- | --- | --- | --- | --- |
| BV-E01 | deanpeters/Product-Manager-Skills — `press-release` | CC BY-NC-SA 4.0 (no copy/distill) | pattern + reference | Adapt | Optional post-divergence press-release stress test; gaps route back to the failing vision section |
| BV-E02 | deanpeters/Product-Manager-Skills — three-tier taxonomy | CC BY-NC-SA 4.0 (structural inspiration only) | pattern + reference | Adapt | Separate orchestration (SKILL.md), interview behavior (phase sub-files), reusable checks (references) |
| BV-E03 | phuryn/pm-skills | MIT | pattern | Adopt | Final response names `create-vision-companion` as greenfield successor; non-greenfield routed to tailored lifecycle |
| BV-E04 | huntsyea/product-skills — `jobs-to-be-done` | MIT | reference | Defer → `discover-product` | JTBD stays an optional method-owned lens here; external workflow distilled later in discovery |
| BV-E05 | assimovt/productskills | MIT | pattern + reference | Adapt | Low-ceremony shape: bounded finalize checks, honor use-case limits and lifecycle tailoring |
| BV-E06 | jacksoncalling/argo-continuous-discovery | License unverified — recheck before any copying | pattern | Adopt (corroborating pattern) | Human owns every scope-ladder climb/close; scope-significant sweep findings route through the scope lens |
| BV-E07 | shinpr/claude-code-discover | MIT | pattern | Adopt (already satisfied) | Repo-resident `.wip.md` + finalized foundation vision remain the durable resume record |
| BV-E08 | ForceInjection/domain-driven-design-skills | WIP source — verify license before any copying | pattern | Adapt | Explicit backtracking route table (check failure, sweep finding, reopened vision) replacing informal "reopen" prose |
| BV-E09 | Cross-cutting finding, `github_skillsets.md` | n/a (finding) | pattern | Adopt | No runtime third-party dependency; external material is method-owned, pattern-only, or deferred |
| BV-E10 | Cross-cutting finding, `github_skillsets.md` | n/a (finding) | pattern | Adopt | Method-doc coverage ledger is normative; drift/review trigger when a consumed method doc changes (§4.6) |
| BV-E11 | ai-analyst-lab/north-star | MIT code; embedded Amplitude-derived content separately constrained | reference | Defer → `define-release`, `validate-release` | No metric-audit call at vision stage; outcomes/signals may stay OPEN; handoff notes audit occurs later |
| BV-E12 | florianbonnet14/ThePowerOfAnalytics_ClaudeSkills | No stated license — reference-only, never copy | reference | Defer → `validate-release` | Analysis-planning idea belongs to post-release validation; nothing incorporated here |

### Method-owned rows (BV-M)

| ID | Method source | Intended incorporation (one line) |
| --- | --- | --- |
| BV-M01 | `product_vision.md` — recommended structure | Every recommended section present or explicitly `OPEN` at finalize; none disappears silently |
| BV-M02 | `product_vision.md` — six completion checks | All six checks are a named finalize gate; failure reopens or produces explicit open stub |
| BV-M03 | `product_vision.md` — ways to develop the vision | Narrative/press-release/JTBD/principles/premortem as optional uncertainty-selected lenses |
| BV-M04 | `overview.md` — lifecycle position | Distinguish "vision finalized" from "product validated"; hand unresolved assumptions downstream |
| BV-M05 | `overview.md` — minimum useful package | Output seeds the minimum package without producing downstream discovery/requirements artifacts |
| BV-M06 | `lifecycle_tailoring.md` | Inspect/point to `lifecycle-onepager.md` at start; warn (not refuse) on non-greenfield |
| BV-M07 | `glossary.md` | Prompts/headings/gates use method vocabulary; product domain terms kept separate |
| BV-M08 | `product_discovery.md` | Vision-level evidence/assumptions only; never fabricate `EV/ASM/OPP/SOL/EXP` IDs; leave seeds |
| BV-M09 | `quality_attributes.md` | Architecture-significance sweep as user-needs lens; park technical constraints; no premature `QAS#` |
| BV-M10 | `validation_and_feedback.md` | Finalize gate: outcomes/signals observable or explicitly open; guardrails never silently omitted |
| BV-M11 | `resources.md` | Each optional lens states its decision purpose and skip path; no template-completion ceremony |

### §5 exclusions table

Twelve explicit exclusion/deferral entries (huntsyea discovery workflows, assimovt interview/experiment content, Argo evidence rubric, Shinpr hypothesis format, RafaelGorski/Problem-Based-SRS, 45ck QAS authoring, DavidROliverBA NFR review, ddd-crew, ForceInjection tactical DDD, lagz0ne design, north-star metric audit, florianbonnet14 analysis planning). Each names a destination (`discover-product`, `define-release`, `specify-requirements`, workspace linter, QAS gate, future design skillset, `validate-release`). Preserve verbatim per contract ("Preserve rejected and deferred rows").

## 2. Compliance audit against contract ledger rules

- **Pending rows: 0.** Every BV-E and BV-M row has a final disposition. No "consider/maybe/TBD" language found.
- **Required fields:** all BV-E rows have stable ID, source, license note, reuse mode, intended incorporation, disposition, and objective evidence (last column). All BV-M rows have stable ID, incorporation, and verification evidence (no license/disposition needed — contract-compliant).
- **Realizing-artifact citations:** every accepted row's evidence column names a concrete verification target (fixture, static test, route table, dependency inventory, file-responsibility map, gate report). None terminates in prose-only acknowledgment.
- **Gaps to fix in the write phase:**
  1. **Disposition vocabulary mismatch.** Ledger uses `adopt/adapt/reference/defer/reject`; contract allows `Adopt/Adapt/Call/Reject/Defer`. No row's *final* disposition is bare "reference" (BV-E04/E11/E12 resolve to Defer), but the ledger's §1 vocabulary should be normalized or explicitly mapped (`reference` mode ≈ contract `pattern` with inspiration recorded, per update 5).
  2. **No retrieval dates recorded.** The ledger's own gate (§4.1) and BV-E09's evidence require repository, license, and retrieval date for every source used as more than background; no row carries a commit/tag or retrieval date yet. Must be added when rows are applied (update 8 traceability also needs this).
  3. **Two unresolved licenses:** BV-E06 (argo — "recheck before copying") and BV-E08 (ForceInjection — "WIP source"). Both are pattern-only with no copying planned, so acceptable, but the write phase must record them as reference-only until verified (contract: "Treat unlicensed material as reference-only").
  4. **No plan-location column.** Rows name skill-level mechanisms but not plan sections (update 8: "Give each accepted ledger row a plan location and planned skill-file destination"). Update-4 agent must add these.
  5. **Reject disposition unused** — not a defect; nothing was rejected outright (exclusions in §5 serve that role with reasons).

## 3. Accepted rows — realizing mechanism required in the revised plan (update 4)

| ID | Mechanism the plan must contain |
| --- | --- |
| BV-E01 | Optional convergent press-release stress test phase after divergence, before acceptance; failure routes to the specific vision section; fixture: feature-shaped vision fails and is reopened. Pattern-only — zero Dean Peters wording. |
| BV-E02 | File-responsibility contract: SKILL.md = orchestration, phase sub-files = interview behavior, reference files = reusable checks/templates. |
| BV-E03 | Handover UX (also update 7): finish response names next stage (`create-vision-companion` for greenfield; tailored lifecycle otherwise), artifact path, and progression gate — never a generic "what next?". |
| BV-E05 | Low-ceremony guarantee: only bounded finalize checks added; configured use-case limits and lifecycle tailoring honored; low-ceremony fixture completes with minimum artifact + explicit OPEN stubs. |
| BV-E06 | Human-gate rule: agent cannot climb/close the scope ladder; scope-significant sweep findings follow a documented route-back. Corroborates update 9 decision-ownership gates. |
| BV-E07 | Durable-state rule (already satisfied): all resume state lives in `.wip.md` / foundation-vision files; static test confirms. |
| BV-E08 | Backtracking route table (update 4 "backtracking triggers"): completion-check failure → finalize section; scope-significant sweep finding → scope lens; reopened changed vision → affected finalize checks + companion rerun. Every trigger has a destination; tests cover all. |
| BV-E09 | Empty external-dependency inventory for this skill; no runtime fetch or unpinned external call (feeds update 5 policy). |
| BV-E10 | Method-doc coverage ledger treated as normative authoring input + drift trigger (§4.6) on any consumed-doc change. |

## 4. `distill` rows

**None in this ledger.** BV-E04 explicitly defers the only distillation candidate (huntsyea JTBD workflow) to `discover-product`; if distilled there, source pointer and retrieval date must be preserved (noted in the row).

**Dean Peters CC BY-NC-SA check:** BV-E01 and BV-E02 touch `deanpeters/Product-Manager-Skills` but are pattern-only adapts with explicit no-copy constraints ("Do not copy prompts, sequences, examples, or wording" / "structural inspiration only"). Compliant with the contract's prohibition; the write phase must keep these rows pattern-only and never convert them to distill. Nothing vendored, nothing to vendor.

## 5. `Call` rows

**None.** No version-pinning or fallback obligations arise from this ledger. Relevant negative constraint: BV-E11 forbids any runtime call to `north-star` from `brainstorm-vision`; when update 4 adds `north-star` as a callable specialist to the skills table, its invocation scope must exclude `brainstorm-vision` (metric audit occurs at `define-release`/`validate-release`; the vision handoff notes this via an open stub).

## 6. `Defer` rows — receiver named?

| ID | Receiver | Named? |
| --- | --- | --- |
| BV-E04 | `discover-product` (JTBD distillation) | Yes |
| BV-E11 | `define-release` and `validate-release` (metric audit) | Yes |
| BV-E12 | `validate-release` (analysis planning) | Yes |

All §5 exclusion entries also name destinations, including the future design skillset for DDD/design sources. No unnamed deferral.

## 7. Missing method-owned rows (contract updates 9 & 10)

Verified against `product_vision.md` (template §"Strategy (ordered outcomes)" line 90; §"Strategy and roadmap" lines 95–99; stability paragraph line 118) and `overview.md` (thin-strategy anchor line 23; pivot rule line 52). The current ledger has **no row** covering strategy, vision-pivot discipline, or decision ownership. Propose three new rows:

### BV-M12 — Strategy section (closes the gap the contract names in update 10)

- **Source:** `product_vision.md` — template section "Strategy (ordered outcomes)" and §"Strategy and roadmap"; `overview.md` thin-strategy anchor.
- **Intended incorporation:** `brainstorm-vision` elicits or explicitly stubs a thin ordered-outcomes strategy section (`outcome — target segment — why this order`) in the foundation vision one-pager. It never expands into a roadmap (roadmap adoption is a `tailor-lifecycle` ceremony decision); strategy reordering is documented as a discovery pivot. `create-vision-companion` will derive/index it (reserve its fields/IDs there, not here).
- **Objective evidence:** finalized-artifact fixture shows the Strategy section populated or as an explicit `OPEN` stub; BV-M01's section list and §4.3 completeness list are amended to include it; finalize gate covers it; a fixture confirms no roadmap artifact is produced at vision stage.

### BV-M13 — Vision-pivot discipline (update 10)

- **Source:** `product_vision.md` stability rule (line 118); `overview.md` pivot rule (line 52); contract update 10.
- **Intended incorporation:** when `brainstorm-vision` reopens a finalized vision, a `vision pivot` requires an explicit `DEC#` citing evidence that invalidates the intended future or target need. A failed experiment or weak feature is refused as pivot grounds and rerouted (opportunities/solutions/scope/strategy). Extends the BV-E08 route table with this trigger/refusal.
- **Objective evidence:** two fixtures matching update-3 regression scenarios — (a) failed experiment wrongly escalated to a vision rewrite is refused and rerouted; (b) genuine vision-invalidating evidence proceeds with the `DEC#` recorded and finalize checks rerun. Note: `DEC#` is a loop ID that `brainstorm-vision` does not write (§4.2) — the DEC must be supplied/cited from the loop workspace, not fabricated; the row must state this reconciliation explicitly.

### BV-M14 — Decision ownership and specialist participation (update 9)

- **Source:** the collaboration/decision-ownership method doc (not cited by the current ledger and outside this agent's read set — the update-9 write agent must pull exact provisions); contract update 9.
- **Intended incorporation:** the vision finalize/reopen decision has one named accountable owner recorded per `lifecycle-onepager.md`; a group or department is refused as owner. Scope-ladder climb/close stays human-owned (aligns BV-E06). The skill must not fabricate specialist (engineering/design/ops/security/compliance/domain) evidence — the architecture-significance sweep parks genuine technical constraints for specialists instead of inventing answers (aligns BV-M09). No standalone ownership skill or mandatory runtime document.
- **Objective evidence:** fixture where a group-only owner is detected and refused (update-3 scenario); finalize output records the accountable owner and consulted specialists or explicit absence; static check that no specialist evidence is agent-invented.

**Consequential edits:** BV-M06's incorporation (inspect `lifecycle-onepager.md`) should note the ownership fields added by update 9; the §4.6 drift-gate doc list must add the collaboration/decision-ownership method doc once BV-M14 exists; §4.5 test matrix gains the three fixtures above.

## 8. Other notes for the update 4/9/10 write agents

- **Spine preservation constraints to respect verbatim (ledger §4.2):** skill writes only `S#/V#/UC#/BV#`; no loop IDs; output stays `<slug>-foundation-vision.md`; no filename collision with method docs. BV-M13's `DEC#` citation must be phrased as *citing* an externally recorded decision, not writing one.
- **SOL reservation (update 1)** lands in `create-vision-companion` Phase 0, not here; BV-M08 already forbids fabricating `SOL#` — consistent, no ledger change needed beyond keeping the seed language.
- **Reference-map sync:** BV-M11 cites `resources.md` (off-limits to this Phase 0 agent). Any write-phase edit touching brainstorm-vision's first-class concepts (Strategy section, pivot gate, ownership fields) must update the corresponding reference-map row(s) in the same change, including the cross-cutting collaboration row.
- **Update 8 hook:** when applying rows, add plan-location and planned-skill-file-destination columns/fields and retrieval dates (gaps 2 and 4 in §2 above).
- **Ledger reopen:** update 10 explicitly reopens this ledger; the additions above (BV-M12–M14, vocabulary normalization, dates) constitute that reopen — preserve all existing rows, including §5 exclusions, unchanged in substance.
