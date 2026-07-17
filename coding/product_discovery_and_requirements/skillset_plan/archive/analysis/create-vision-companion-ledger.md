# Phase 0 digest — `create-vision-companion` ledger audit

**Source ledger:** `skillset_plan/create-vision-companion-contributions.md`
**Contract scope:** ordered updates 1, 4, 10 (plus ledger rules in "Contribution ledgers")
**Method docs consulted:** `product_vision.md` (cited by VC-M01/VC-M02) — targeted check only.

## 1. Row inventory

### External-contribution rows (VC-E01–VC-E14)

| ID | Source | License | Reuse mode | Disposition | Intended incorporation (one line) |
| --- | --- | --- | --- | --- | --- |
| VC-E01 | shinpr/claude-code-discover | MIT | pattern | Adapt | Add derived `discovery-seeds.md` index, README-linked, in bundle completeness checks |
| VC-E02 | shinpr/claude-code-discover | MIT | pattern | Adopt | Fresh-context builder/critic separation; critics never see builder reasoning |
| VC-E03 | shinpr/claude-code-discover | MIT | reference | Defer → `discover-product` | Seeds may cite candidate assumptions but never create `EXP#` or copy hypothesis schema |
| VC-E04 | RafaelGorski/Problem-Based-SRS | MIT | pattern | Adapt | Phase 9 mechanical gates validate companion graph: coverage, uniqueness, resolvable refs, reserved-namespace absence |
| VC-E05 | ForceInjection/domain-driven-design-skills | WIP — verify before copying | pattern | Adapt | Backtracking/re-entry matrix routing every defect category to an owning phase |
| VC-E06 | ForceInjection/domain-driven-design-skills | WIP — verify before copying | pattern | Adapt | Golden fixtures + mutation tests for fresh build, upgrade, vision diff, failure recovery |
| VC-E07 | huntsyea/product-skills | MIT | pattern | Adopt (already satisfied) | Preserve progressive-disclosure split; new rules go to owning sub-files |
| VC-E08 | phuryn/pm-skills | MIT | pattern | Adopt | Handoff UX: finalize names next lifecycle stage + `discovery-seeds.md` as its input |
| VC-E09 | jacksoncalling/argo-continuous-discovery | Unverified — verify before copying | pattern | Adopt (corroborating) | Durable status/review files, Phase 11 human gate; gaps routed, never silently repaired |
| VC-E10 | DavidROliverBA/Daves-Claude-Code-Skills | Not established | pattern + reference | Adopt (corroboration) | Parallel independent critic reviews with companion-specific rubrics; no NFR content imported |
| VC-E11 | deanpeters/Product-Manager-Skills | CC BY-NC-SA 4.0 — no distillation | reference | "reference only" (non-contract term — see §2) | Preserve `V#` promises + realization coverage in `vision-index.md`; copy/call nothing |
| VC-E12 | Cross-cutting (fit analysis) | N/A | pattern | Adopt | Single proprietary bundle/ID spine; no PRD, CP/CN/FR, or third-party workspace structures |
| VC-E13 | Cross-cutting (fit analysis) | N/A (recheck provenance pre-release) | pattern | Adopt | No runtime third-party calls; pattern sources recorded with repo, license, retrieval date |
| VC-E14 | Cross-cutting (fit analysis) | Proprietary test design | pattern | Adopt | Authoring gate + fixture matrix (§5.7 of ledger) is release-blocking |

### Method-owned rows (VC-M01–VC-M10)

| ID | Method source | Intended incorporation (one line) |
| --- | --- | --- |
| VC-M01 | product_vision.md — structure | Map present vision sections to companion concerns; route absent/open sections to coverage signals + seeds |
| VC-M02 | product_vision.md — completion checks | Expose (never conceal or repair) vision gaps via coverage checks and seed/judgment routing |
| VC-M03 | overview.md — lifecycle/readiness | README load-order + final handoff name downstream consumers without claiming readiness |
| VC-M04 | lifecycle_tailoring.md | Require finalized vision; respect lifecycle one-pager; no companion for deliberately skipped vision stages |
| VC-M05 | product_discovery.md | Seeds expose questions/candidates only; never promote to `OPP#/ASM#/EV#/SOL#/EXP#` |
| VC-M06 | domain_discovery.md | Rename to `domain-glossary.md`; label context readings as hypotheses; route ambiguity to `decisions.md` |
| VC-M07 | quality_attributes.md | Route architecture lens; preserve source UCs/constraints; never invent `QAS#` |
| VC-M08 | glossary.md (method) | Keep method vocabulary distinct from product ubiquitous language; rename bundle artifact |
| VC-M09 | validation_and_feedback.md | Surface missing/weak outcome & guardrail definitions as seeds/coverage findings |
| VC-M10 | resources.md | Every companion file/seed category states its consumer and decision purpose |

## 2. Compliance audit against contract ledger rules

- **Required fields:** Every VC-E row has stable ID, source, license/provenance note, reuse mode, intended incorporation, disposition, and objective verification evidence. Every VC-M row has stable ID, source, incorporation, and verification evidence. **No missing-field rows.**
- **Pending rows:** **None.** No row is `Pending` or "under consideration."
- **Disposition vocabulary mismatch (flag):** The ledger's local vocabulary is adopt/adapt/**reference**/defer/reject; the contract allows Adopt/Adapt/Call/Reject/Defer. **VC-E11** carries the non-contract disposition "reference only". Recommended contract-vocabulary mapping for the write agent (update 4): treat VC-E11 as **Reject (license: CC BY-NC-SA, no distillation permitted) with the surviving behavior recorded as a method-owned mechanism** — the `V#` promise-coverage duty in `vision-index.md` is proprietary, not derived from Dean Peters content. VC-E03's "defer" and VC-E10's "pattern + reference" otherwise map cleanly (Defer, Adopt-mechanism-only).
- **Realizing-artifact citations:** All accepted rows cite a concrete realizing mechanism (fixture, gate, matrix, file, or contract) in the "Required verification evidence" column — see §3. Compliant.
- **License caveats on accepted rows (flag, non-blocking):** VC-E05/VC-E06 (WIP license), VC-E09 (unverified), VC-E10 (not established) are all **pattern/mechanism-only with no copied content**, so acceptance is permissible under the contract's "unlicensed material as reference-only" rule — but the write agent must carry the "verify license before any copying" note into the plan, and the drift gate (§5.9) already forces re-audit.

## 3. Accepted rows — realizing mechanism the revised plan must contain (update 4)

| ID | Realizing mechanism required in plan |
| --- | --- |
| VC-E01 | `discovery-seeds.md` in bundle schema; README link + load-order; bundle-completeness check includes it (ledger §3.1, §5.2) |
| VC-E02 | Builder/critic independence gate: separate fresh contexts, critic brief = frozen vision + draft + template + rubric only (ledger §5.5) |
| VC-E04 | Phase 9 deterministic gate set: source-ID coverage, derived-ID uniqueness, resolvable references, explicit coverage gaps, reserved-namespace absence (ledger §5.3) — integration point for the update-2 workspace linter |
| VC-E05 | Backtracking/re-entry matrix (ledger §5.6) — every finding category → owning phase; no "review later" route |
| VC-E06 | End-to-end fixture matrix, 17 scenarios (ledger §5.7) + drift gate (§5.9) |
| VC-E07 | File-responsibility map; new rules land in owning sub-files (progressive disclosure preserved) |
| VC-E08 | Handoff gate (ledger §5.8): finalize response names bundle path, `discovery-seeds.md`, open-decision state, next lifecycle skill; chaining must not override lifecycle tailoring (contract update 7 overlap) |
| VC-E09 | Durable `_status.md`/review files; Phase 11 human gate; gaps become routed seeds/judgment rows — never silent vision edits (also realizes update-10 no-silent-edit rule) |
| VC-E10 | Documented independent multi-critic review architecture with companion-specific rubrics |
| VC-E12 | Schema inventory containing only proprietary artifacts/IDs; taxonomy guardrail |
| VC-E13 | Dependency inventory + source ledger with repo/license/retrieval date; no runtime fetches (realizes update 5 policy for this skill) |
| VC-E14 | Release-blocking authoring coverage gate (ledger §5) with repeatable pass/fail evidence |
| Defer VC-E03 | Plan must show `discover-product` as receiver of hypothesis/experiment schema; companion seed schema forbids `EXP#`, method, time budget, criteria |

## 4. `distill` rows

**None.** This ledger contains no `distill` rows — all external rows are `pattern` or `reference`; nothing is vendored or scheduled for vendoring.

- **deanpeters CC BY-NC-SA check:** VC-E11 is the only deanpeters row; it is reference-only with explicit "no distillation" and evidence that "no external content is included." §6 exclusions repeat the prohibition. **Compliant** — no CC BY-NC-SA content is scheduled for copying or distillation.
- Consequence for the write agent: this skill needs no donor-audit task under acceptance-gate bullet 5; only the pattern-provenance recording duty (VC-E13).

## 5. `Call` rows

**None.** The companion calls no version-pinned specialists. §6 explicitly routes `ai-analyst-lab/north-star` to definition/validation skills ("Called by definition/validation, not by companion derivation") and `45ck/software-architecture-skills` (QAS writer) to `specify-requirements`. For update 4's specialists table the write agent should record: **neither `north-star` nor `quality-attribute-scenario-writer` is invocable from `create-vision-companion`** — no bounded role/pinning/fallback needed here, and this negative must be stated so the specialists cannot acquire spine-artifact ownership via the companion.

## 6. `Defer` rows — destinations named?

| Row | Destination | Named? |
| --- | --- | --- |
| VC-E03 | `discover-product` | Yes |
| §6 Dean Peters sequences/press-release | `brainstorm-vision` (upstream input only) | Yes |
| §6 huntsyea discovery/JTBD | `discover-product` | Yes |
| §6 Assimovt interview/validation/experiment/scope/metric | discovery, definition, or validation skills | Yes (multi-skill; acceptable) |
| §6 Argo interview rubric + evidence-confidence cap | `discover-product` evidence model | Yes |
| §6 45ck QAS authoring | `specify-requirements` | Yes |
| §6 ddd-crew, ForceInjection tactical DDD, lagz0ne/design-skill | future design skillset | Yes |
| §6 north-star | definition/validation skills | Yes |
| §6 florianbonnet14 analytics | validation-analysis planning (no license → no distillation) | Yes |

All deferrals name a receiving skill or the future design skillset. **Compliant.**

## 7. Method-owned rows required by updates 1, 9, 10 but missing — proposals

### Already satisfied (no new row needed)

- **Update 1 — reserve `SOL` in companion Phase 0:** ledger §3.2 already reserves `ASM, EV, OPP, SOL, EXP, REL, REQ, QAS, DEC`, §3.4 excludes `solutions.md` from the bundle, and VC-M05 forbids promotion into `SOL#`. The update-1 write agent only needs to make the plan section cite ledger §3.2/§3.4 explicitly; no new ledger row required.
- **Update 10 — no silent vision edits / route routine findings to seeds:** covered by §1 governing rule, §5.4 derived-only gate, VC-E09, VC-M01/VC-M02. Mechanism exists but is not yet expressed as an explicit vision-stability method-owned row (folded into VC-M12 below).

### Missing rows — proposed additions (update 10 mandates reopening this ledger)

| Proposed ID | Method source | Rule covered | Intended incorporation | Objective evidence |
| --- | --- | --- | --- | --- |
| **VC-M11** | `product_vision.md` — "Strategy (ordered outcomes)" + "Strategy and roadmap" sections (present in the method doc; **absent from VC-M01's structure list**, which stops at outcomes/signals and critical assumptions) | Update 10: companion **derives and indexes** the strategy section and **reserves required fields/IDs** | Add strategy (ordered outcomes + target segments) to the companion's derived index (e.g., in `vision-index.md` or a strategy index section); expose a missing or stubbed strategy section as a visible coverage finding and discovery seed; reserve the strategy field set/ID representation chosen by the plan so `discover-product`/`define-release` can check opportunity selection against it; strategy reordering is a discovery pivot and never a companion edit | Fixtures for populated, stubbed, and absent strategy sections; index round-trips ordered outcomes without reordering or rewriting them; linter/gate flags a bundle whose index omits a present strategy section |
| **VC-M12** | `product_vision.md` — stability rule ("discovery pivots ... under a stable vision; a vision pivot is rare ...") + contract update 10 | Update 10: vision pivot only via explicit `DEC#` citing invalidating evidence; `discovery pivot` must not silently edit the vision; routine findings route to opportunities/solutions/scope/strategy | Extend §5.4 derived-only gate and §5.6 backtracking matrix: the "vision drift → user-confirmed full rebuild" route additionally requires an explicit loop `DEC#` (recorded outside the bundle — `DEC` is reserved per §3.2) citing the invalidating evidence before rebuild; all other findings become seeds or judgment rows | Fixture: evidence-driven vision-change attempt without a cited `DEC#` is refused and rerouted to seeds; fixture with genuine invalidating evidence + `DEC#` proceeds to user-confirmed rebuild (aligns with update-3 regression scenarios 8–9) |
| **VC-M13** *(applicability note)* | `product_vision.md` decision-ownership norms + contract update 9 | Singular accountable ownership of companion finalize/adjudication decisions | Update 9 does **not** list `create-vision-companion` among implementing skills, so a row is optional; if the write agent adds one, it should state that Phase 11 adjudication and rebuild/upgrade confirmations name one accountable human owner (the solo expert), never "the team", and that the companion fabricates no specialist evidence (it invents no evidence at all per §5.4) | `_status.md`/`decisions.md` fixture shows a named confirmer on every judgment row; finalize refuses group-only confirmation |

### Open decision for the write agent (update 10)

The concrete **representation of the reserved strategy fields/IDs** is undecided: whether strategy outcomes get their own ID family (which would extend §3.2's reserved list and §5.3's namespace gate) or remain ordered fields indexed under existing `V#`/vision-index structure. The plan must record this choice; whichever is chosen must be synchronized with §3.2 (reservations), §5.3 (namespace gate), the update-2 linter, and `brainstorm-vision`'s elicit/stub duty (BV-M01 counterpart).

## 8. Other notes for write-phase agents (updates 1, 4, 10)

1. **Update 1 touchpoints in this skill are narrow:** SOL reservation (§3.2, done in ledger), `solutions.md` exclusion from bundle (§3.4), seed rule "avoid prescribing a solution" + rejection fixture (§3.1, §5.7 item 17), and VC-M05's no-promotion rule. The plan's `SOL#` section should cite these as the companion-side guarantees.
2. **Update 4 integration hooks:** the ledger's §5 gates (5.1–5.9) are the objective verification targets; plan sections should reference them by gate name. VC-E04's mechanical gates are where the update-2 deterministic linter plugs into this skill (finalize-time invocation per update 2).
3. **`DEC` ID-scoping task (§3.2):** the ledger requires the companion's local judgment IDs to be mechanically distinguishable from the loop's reserved `DEC` family ("clearly scoped as bundle-review IDs or renamed"). This is an unresolved naming decision the plan revision should settle (relevant to update-2 linter's reserved-family collision check and to VC-M12's cross-boundary `DEC#` citation).
4. **Vocabulary normalization:** when applying update 4, restate ledger dispositions in contract vocabulary (Adopt/Adapt/Call/Reject/Defer); only VC-E11 needs a substantive re-labeling decision (§2 above).
5. **Handoff/chaining overlap:** VC-E08's handoff realizes part of update 7; the update-4 agent should place it once and cross-reference, not duplicate.
6. **Bundle-schema renames** (`glossary.md` → `domain-glossary.md`, ledger §3.3) touch fingerprint/upgrade logic — any plan section enumerating companion artifacts must use the new name and include `discovery-seeds.md`.
7. **Strategy is derived, not owned:** update 10 keeps strategy as a section of the foundation vision one-pager, elicited/stubbed by `brainstorm-vision`. The companion's duty (VC-M11) is derive/index/reserve only — consistent with the derived-only constraint; no wording in the plan may give the companion write access to the strategy section.
