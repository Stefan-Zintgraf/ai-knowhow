# Phase 2 acceptance gate

**Verdict: FAIL**

**Audit scope:** the exact 33-file staged planning bundle under `coding/product_discovery_and_requirements/`. All 33 files were read. No network access or third-party repository access was used. This report is the only write.

**Failed acceptance checkboxes:** AG-01, AG-02, AG-04, AG-08, AG-11, AG-12, AG-14.

## Counts

| Measure | Result |
| --- | --- |
| Files read | 33/33 |
| FIT §5.1 keys reviewed | 15/15; all 15 have contribution mappings |
| FIT §2 keys reviewed | 49/49; 48 have explicit final dispositions, 1 does not (`FIT-2-dddcrew-02`) |
| Explicitly requested FIT rows | `FIT-2-argo-04` → `DP-011` Adapt; `FIT-2-daves-02` → `SR-EXT-06` Adapt; `FIT-2-forceinjection-02` → `DP-025` Adapt, reinforced by `VC-E06` and `TL-008` |
| Literal Pending contribution rows | 0 |
| Non-contract final disposition | 1: `VC-E11` remains `reference only` rather than Adopt/Adapt/Call/Reject/Defer |
| Distill rows | 15/15 audited; all 15 have an explicit authoring-time donor-audit task and license/provenance obligations |
| Call rows | 6/6 audited: `DP-020`, `DP-022`, `DR-EXT-07`, `SR-EXT-05`, `VR-EXT-01`, `VR-EXT-09`; all six have bounded roles, pin policies, fallbacks, and no-spine-ownership rules through plan §3.1 |
| Required contribution/method mapping rows | 213 |
| Precise ID → plan → planned file/test mappings | 143/213 |
| Incomplete mapping rows | 70: 34 method-coverage rows have no stable IDs; 36 ID-bearing `DR/SR/VR-MTH-*` rows have only blanket, non-row-specific destination statements |
| Local Markdown link occurrences checked | 346 |
| Broken/unresolvable local-link occurrences | 7 occurrences, 6 unique source→target pairs; a valid `README.md` directory link is not counted broken |
| External URL occurrences | 68; recorded but not network-checked |

## Acceptance checklist

### AG-01 — FAIL — fit-analysis §§5.1 and 2

All 15 §5.1 recommendations map to contribution IDs, and all 49 §2 keys were reviewed. One §2 warning has no final disposition: `FIT-2-dddcrew-02` says the stage doc's **Agent rule sets** label misfiles `ddd-crew/ddd-starter-modelling-process`, but `domain_discovery.md` still lists that process under **Agent rule sets**. `SR-EXT-12` defers the process to the future design skillset, but neither that row nor the final plan explicitly accepts or rejects the stage-label correction. This is the one unclosed FIT-2 disposition.

The three keys named by the gate are explicit rather than inferred:

- `FIT-2-argo-04` → `DP-011`, **Adapt**: human gate before solutioning; plan §5.4.
- `FIT-2-daves-02` → `SR-EXT-06`, **Adapt**: `nfr-capture` completeness prompts without Obsidian schemas; plan §5.6.
- `FIT-2-forceinjection-02` → `DP-025`, **Adapt**: blind scored reference-topic run; `VC-E06` and `TL-008` independently apply the same validation mechanism; plan §6.

### AG-02 — FAIL — ordered updates 1–3 wiring

The deterministic linter and regression-validation update are broadly wired: plan §2.2 defines LNT-01–LNT-19; §3 and every artifact-producing skill invoke applicable checks; §6 defines the reference topic, five scoring axes, failure handling, and RTS-01–RTS-13.

Solution-alternative wiring contains a direct trace-diagram conflict. Plan §2's `SOL#` decision and `DP-012` require **at least three** materially different directions unless a `DEC#` records the exception, but the plan's §4 diagram says `≥2 directions or DEC#`. The diagram therefore does not agree with the artifact decision, contribution ledger, and planned skill destination. Update 1 is not consistently wired through every named surface.

### AG-03 — PASS — accepted contributions and design/domain deferrals

Accepted external and method-owned rows have plan locations, planned destinations, and objective verification targets in each ledger's final traceability section. Rejected/deferred rows retain reasons or receivers. Design/domain deferrals name the future design skillset, notably `SR-EXT-12` and the explicit exclusion/deferral sections.

This pass does not waive the method-coverage mapping defect in AG-04/AG-12 or the invalid `VC-E11` disposition in AG-11.

### AG-04 — FAIL — method-document coverage destinations

Plan §2.1 maps every method document to consuming skills, and ledger coverage tables contain verification targets. The per-row plan-to-authoring contract is incomplete:

- 13 `tailor-lifecycle` method-coverage rows have no stable IDs and no row-specific plan/destination triples.
- 21 `discover-product` method-coverage rows have no stable IDs; its traceability preamble gives only the blanket destination “phase sub-file or finalize gate.”
- `DR-MTH-01..12`, `SR-MTH-01..12`, and `VR-MTH-01..12` have stable IDs and objective verification targets, but their traceability sections give only blanket destinations such as “skill prompt, gate, or fixture,” not a planned skill file/section per row.

Thus 70 method-coverage rows cannot satisfy the contract's row-specific plan location and planned skill-file destination requirement.

### AG-05 — PASS — distill audit, license, and provenance

Plan §§3.2–3.3 enumerate all 15 distill rows and an explicit six-point authoring-time audit task for each. The plan records exact donor scope, candidate-level disposition duties, destination-file/section duties, pin/date/license/attribution requirements, and the shared `DR-EXT-01`/`SR-EXT-08` provenance rule. The license exclusions are explicit: Dean Peters content is never distilled; unlicensed Florian Bonnet content remains pattern/reference only; Argo stays pattern-only inside `DP-012` unless its license is verified; North Star's Amplitude-derived content stays call-only.

### AG-06 — PASS — call contracts

The six call-mode rows are covered by plan §3.1:

| Contribution | Contract evidence |
| --- | --- |
| `DP-020` | `prototype`: experiment-only role, local version/commit pin, next-cheapest-test/manual fallback, caller records observations |
| `DP-022` | `domain-modeling`: contested-domain role, local version/commit pin, manual-session/`OPEN:` fallback, canonical domain artifacts only |
| `DR-EXT-07`, `VR-EXT-01` | `north-star`: metric audit only, exact commit/release pin, local review/justified-skip fallback, calling skill writes review metadata |
| `SR-EXT-05` | conditional QAS writer: candidate drafting only, three-leg depth/license/comparison gate, exact pin if accepted, local QAS drafting fallback |
| `VR-EXT-09` | `qa`/`triage`: source-addressable evidence intake only, local version/commit pin, human evidence-intake fallback |

Plan §3.1 explicitly states that no callee owns, writes, or mutates companion or loop spine artifacts.

### AG-07 — PASS — cross-cutting handover, ownership, linter, validation, provenance, skip, and re-entry

Plan §§3.2–3.3, 4.1–4.2, and 5.1–5.7 wire these rules into affected skills. The ledgers contain the corresponding rows: handover (`BV-E03`, `VC-E08`, `TL-001/014`, `DP-017`, `DR-EXT-11`, `SR-EXT-10`, `VR-EXT-05`); ownership/specialist participation (the `*-M` update-9 rows); linter/finalize invocation; provenance; explicit skip handling; and named-artifact re-entry routes. RTS-02 and RTS-07–RTS-10 provide the required regression scenarios.

### AG-08 — FAIL — `SOL#` / `EXP#` consistency

The plan's artifact table, LNT-07, LNT-19, §5.4 skill prose, and RTS-04 correctly require `EXP#` to cite the applicable `SOL#` and include the resulting `DEC#`. The final `discover-product` ledger is stale:

- `DP-013` says only that `EXP#` tests a named `ASM#`.
- `DP-014`'s verification schema omits applicable `SOL#` and resulting `DEC#`.
- **Required artifact and trace contract** lists `EXP#` without applicable `SOL#` or resulting `DEC#`.
- The authoring gate requires every `EXP#` to cite an `ASM#`, but does not require the applicable `SOL#`.

Additionally, the plan diagram uses `≥2` alternatives while `DP-012` and the plan's representation decision require `≥3`. The required surfaces do not agree.

### AG-09 — PASS — collaboration/ownership and vision stability

The final ledgers include applicable method-owned rows: `BV-M12..14`, `VC-M11..12`, `TL-M01..02`, `DP-M01..04`, `DR-M01..05`, `SR-M01..04`, and `VR-M01..04`. Plan §§4 and 5 operationalize their fields, gates, refusals, and routes; RTS-07–RTS-12 provide passing scenarios. No standalone ownership or strategy skill/stage and no new mandatory runtime ownership/strategy document is introduced.

### AG-10 — PASS — post-authoring reconciliation rule

No planned skills are authored in this bundle. For the future authoring boundary, plan §3.3 explicitly requires replacing planned evidence with actual files/tests, reopening affected rows on method/donor/schema change, and reconciling `overview.md`, affected method docs, implemented skills, lifecycle, artifact schema, strategy, roadmap, `SOL#`, one-pagers, and linter before authoring completes.

### AG-11 — FAIL — unexplained omissions / ledger conformance

The final audit found these unexplained or inconsistent items:

1. `FIT-2-dddcrew-02` remains undispositioned and the stage label remains unchanged.
2. `VC-E11` still uses final disposition **reference only**, outside the contract's allowed set `Adopt/Adapt/Call/Reject/Defer`. Its traceability row calls it “reference-only (no adoption),” so this is not merely formatting.
3. The `discover-product` `EXP#` contract remains stale relative to ordered updates 1 and 6, as detailed under AG-08.
4. The row-specific plan-to-authoring mapping is incomplete for 70 method-coverage rows, as detailed under AG-04/AG-12.

Literal Pending rows are nevertheless zero, and rejected/deferred rows retain reasons/destinations.

### AG-12 — FAIL — contribution ID → plan → skill file/test mapping

The compact mapping audit below covers all 213 required rows. Only 143 have precise triples. The remaining 70 are reported explicitly as missing rather than inferred.

### AG-13 — PASS — reference-map synchronization and Update 11

`resources.md`'s reference map is synchronized across product vision, discovery, definition, requirements/domain, validation, lifecycle tailoring, and collaboration/ownership. The lifecycle-tailoring row names entry point, ceremony, stage/artifact selection, cadence, and decision authority; its assessment carries all seven ceremony drivers, six entry-point classes, roadmap adopt/skip, the one-pager, seven-field authority, handover, and out-of-order rules. The cross-cutting collaboration row carries the seven-field ownership record. Plan §9 records confirmed/rejected Update-11 candidates and closes the review.

### AG-14 — FAIL — local Markdown links

Of 346 local-link occurrences, seven escape the exact staged bundle and therefore do not resolve within the 33-file gate scope:

| Source | Target | Occurrences |
| --- | --- | ---: |
| `glossary.md` | `../software_design/glossary.md` | 1 |
| `resources.md` | `../software_design/software_design.md` | 2 |
| `resources.md` | `../software_design/strategic_tactical_design.md` | 1 |
| `resources.md` | `../software_design/glossary.md` | 1 |
| `skillset_plan/prod_discovery_requirements_skillset_plan.md` | `../../../skills-plugins/brainstorm-vision/SKILL.md` | 1 |
| `skillset_plan/prod_discovery_requirements_skillset_plan.md` | `../../../skills-plugins/create-vision-companion/SKILL.md` | 1 |

All in-bundle file and anchor targets checked successfully. The `skillset_plan/README.md` link to `../` resolves to the staged bundle root and is not a broken link. Sixty-eight external URLs were recorded and not network-checked, as required.

## FIT §5.1 mapping — 15/15 reviewed

| Key | Final contribution mapping |
| --- | --- |
| `FIT-5.1-01` | `BV-E01` Adapt |
| `FIT-5.1-02` | `DP-001`, `DP-002` Adopt, audit-conditioned |
| `FIT-5.1-03` | `DP-004`, `DP-005`, `DP-007` Adopt/Adapt, audit-conditioned |
| `FIT-5.1-04` | `DP-008`, `DP-009`, `DP-010` Adapt |
| `FIT-5.1-05` | `DP-014` Adapt |
| `FIT-5.1-06` | `DR-EXT-01..04` Adopt/Adapt |
| `FIT-5.1-07` | `DR-EXT-06` Adapt |
| `FIT-5.1-08` | `DR-EXT-07`, `VR-EXT-01` Call |
| `FIT-5.1-09` | `SR-EXT-01` Adopt |
| `FIT-5.1-10` | `SR-EXT-03` Adapt; shared linter also realized by `DP-023` |
| `FIT-5.1-11` | `SR-EXT-05` conditional Call; `SR-EXT-07` Adapt |
| `FIT-5.1-12` | `VR-EXT-03` Adopt as independently authored guardrail |
| `FIT-5.1-13` | `BV-E03`, `VC-E08`, `TL-001/014`, `DP-017`, `DR-EXT-11`, `SR-EXT-10`, `VR-EXT-05` |
| `FIT-5.1-14` | `VR-EXT-04` Adapt; reinforced by `BV-E08`, `VC-E05`, `TL-005`, `DP-024`, `DR-EXT-12`, `SR-EXT-11` |
| `FIT-5.1-15` | `SR-EXT-12` Defer to future design skillset; matching exclusion/deferral sections preserved in other ledgers |

## FIT §2 disposition audit — 49/49 reviewed

Every key appears below exactly once. `FAIL` marks the sole missing disposition.

| Repository | Key → final evidence |
| --- | --- |
| deanpeters | `01`→`BV-E02`/`TL-002` Adapt; `02`→`BV-E01` Adapt; `03`→`DP-018` and vision rows, independent pattern only; `04`→`DR-EXT-10`/`SR-EXT-09` Reject distillation; `05`→plan §1 two-mode design plus `BV-E09` no runtime dependency |
| phuryn | `01`→handover rows listed at FIT-5.1-13; `02`→`DR-EXT-08`/`VR-EXT-02` Adapt into local fallback, no second call; `03`→wholesale-marketplace rejection in ledger exclusions and plan §3.1 routing exclusions; `04`→`VC-E12`/`DP-029` competing-pipeline rejection |
| huntsyea | `01`→`DP-001..003`, `DR-EXT-01/02`, `SR-EXT-08`; `02`→same structural donor rows; `03`→`VC-E07`/`BV-E02` progressive-disclosure layout; `04`→`DP-026`/`TL-009` vendor, never live-call |
| argo | `01`→`DP-008` Adapt; `02`→`DP-009` Adapt; `03`→`DP-010` Adapt; **`04`→`DP-011` Adapt**; `05`→`DP-029` plus explicit Argo workspace exclusions |
| assimovt | `01`→`DP-004`; `02`→`DP-004..007`, `DR-EXT-03/04`; `03`→`TL-004`; `04`→`DP-029` plus single-spine rules |
| shinpr | `01`→`DP-014`; `02`→`SR-EXT-01`; `03`→`VC-E01`; `04`→`VC-E01`/plan §1 repo-artifact confirmation; `05`→`VC-E12`/`DP-029` reject pipeline taxonomy |
| gorski | `01`→`SR-EXT-03`/`DP-023`; `02`→`DR-EXT-06`; `03`→`SR-EXT-03` explicit `.spec`/`CP/CN/FR` exclusion; `04`→`VC-E12` competing-upstream rejection |
| 45ck | `01`→`SR-EXT-05` conditional Call; `02`→same row's three-leg audit and local fallback; `03`→`SR-EXT-12` Defer |
| daves | `01`→`SR-EXT-07` Adapt; **`02`→`SR-EXT-06` Adapt**; `03`→`SR-EXT-06`/ledger exclusions reject vault ecosystem; `04`→`VC-E10` existing independent-review architecture |
| dddcrew | `01`→`SR-EXT-12` Defer/reference with CC BY attribution duty; **`02`→FAIL: no final disposition; `domain_discovery.md` still uses the misclassifying heading** |
| forceinjection | `01`→`VR-EXT-04`/`DR-EXT-12` Adapt; **`02`→`DP-025`, `VC-E06`, `TL-008` Adapt**; `03`→`SR-EXT-12` Defer |
| lagz0ne | `01`→`SR-EXT-12` Defer |
| northstar | `01`→`DR-EXT-07`/`VR-EXT-01` Call; `02`→same call contracts and plan §3.1 justification; `03`→plan §§3.1–3.2 call-only copyright/provenance rule |
| florianbonnet | `01`→`VR-EXT-03` independently authored guardrail; `02`→same row's unlicensed/no-copy restriction |

## Compact contribution mapping audit

“Mapped” means the ledger's **Plan-to-authoring traceability** section supplies a plan section and planned skill destination that names a file/section or concrete fixture/linter/test. The ID lists below are the complete accepted/method-owned set. Rejected and deferred rows are intentionally excluded from destination mapping and retain their reasons/receivers in their ledgers.

| Ledger | Required | Precisely mapped | Mapping evidence / missing set |
| --- | ---: | ---: | --- |
| `brainstorm-vision` | 23 | 23 | Traceability §6 maps `BV-E01,E02,E03,E05,E06,E07,E08,E09,E10` and `BV-M01..M14` to plan §§2–6 and planned phase/reference/finalize files plus fixtures. Deferred: `BV-E04,E11,E12`. |
| `create-vision-companion` | 24 | 24 | Traceability §7 maps `VC-E01,E02,E04,E05,E06,E07,E08,E09,E10,E12,E13,E14` and `VC-M01..M12` to plan §§2–6 and planned templates, phases, rubrics, linter wiring, and fixtures. `VC-E03` is deferred; `VC-E11` is excluded from this count because its disposition is invalid/non-adoptive. |
| `tailor-lifecycle` | 31 | 18 | Final mapping covers `TL-001..TL-016,TL-M01,TL-M02`. **Missing 13 method-coverage triples and IDs:** Overview; Lifecycle Tailoring Step 1, Step 2, Step 3, Step 4, Step 5, one-pager template, failure modes, completion checks; Resources; Glossary; GitHub analysis/contract; Skillset plan. |
| `discover-product` | 56 | 35 | Final mapping covers `DP-001..DP-031,DP-M01..DP-M04`. **Missing 21 method-coverage triples and IDs:** Product Discovery four risks, phases 1–7, artifacts, experiment card, failure modes, completion checks; Domain Discovery; Quality Attributes; Resources; Glossary; Overview; Product Vision; Lifecycle Tailoring; GitHub analysis/contract; Skillset plan. |
| `define-release` | 28 | 16 | Final mapping covers accepted `DR-EXT-01..09,DR-EXT-11,DR-EXT-12` and `DR-M01..M05`. **Missing row-specific destinations:** `DR-MTH-01..DR-MTH-12`; each has verification evidence but only a blanket “skill prompt, gate, or fixture” destination. `DR-EXT-10` is rejected for distillation. |
| `specify-requirements` | 26 | 14 | Final mapping covers `SR-EXT-01..08,SR-EXT-10,SR-EXT-11` and `SR-M01..M04`. **Missing row-specific destinations:** `SR-MTH-01..SR-MTH-12`; each has verification evidence but only a blanket destination. `SR-EXT-09` is rejected; `SR-EXT-12` is deferred. |
| `validate-release` | 25 | 13 | Final mapping covers `VR-EXT-01..09` and `VR-M01..M04`. **Missing row-specific destinations:** `VR-MTH-01..VR-MTH-12`; each has verification evidence but only a blanket destination. |
| **Total** | **213** | **143** | **70 incomplete; AG-04 and AG-12 fail.** |

For the 143 mapped rows, the authoritative triples are the corresponding ledger traceability-table rows; their destination cells include the objective fixture/linter/test. The gate does not invent triples for the 70 incomplete rows.

## Minimal targeted fix envelopes

Run these sequentially where write sets overlap. Preserve the ordered-update decisions (`solutions.md`, no strategy ID family, `BRV#`, `OPEN:`, seven-field authority, optional roadmap) and do not renumber existing contribution IDs.

### F1 — close FIT/ledger conformance and `EXP#` drift

**Reads:** `skillset_plan_update_plan.md`; `analysis/fit-map.md`; `github_skillsets.md`; `domain_discovery.md`; `skillset_plan/create-vision-companion-contributions.md`; `skillset_plan/discover-product-contributions.md`; plan §§2, 3.1–3.3, 5.2, 5.4, 6.

**Writes:** `domain_discovery.md`; `skillset_plan/create-vision-companion-contributions.md`; `skillset_plan/discover-product-contributions.md`.

**Done:** disposition `FIT-2-dddcrew-02` explicitly and correct or explicitly retain/reason the stage label; normalize `VC-E11` to one allowed final disposition while preserving its no-copy/no-adoption intent; synchronize every discovery-ledger `EXP#` schema/trace/gate occurrence with applicable `SOL#` and resulting `DEC#`; preserve donor/license decisions.

### F2 — synchronize the plan's solution count

**Reads:** `skillset_plan_update_plan.md`; plan §§2, 4, 5.4, 6; `discover-product-contributions.md` (`DP-012`); `product_discovery.md`.

**Writes:** `skillset_plan/prod_discovery_requirements_skillset_plan.md` only.

**Done:** the trace diagram and every plan surface use the already-decided `≥3 materially different directions or DEC#` rule; no ordered-update decision changes; artifact table, diagram, skill prose, LNT-07/LNT-19, and RTS-04 agree.

### F3 — complete method-coverage traceability

**Reads:** contract; plan §§2.1, 3.3, 5.3–5.7, 6; all method docs; `tailor-lifecycle-contributions.md`; `discover-product-contributions.md`; `define-release-contributions.md`; `specify-requirements-contributions.md`; `validate-release-contributions.md`.

**Writes:** those five contribution ledgers only.

**Done:** add stable, non-renumbering IDs to the 34 unkeyed tailoring/discovery method-coverage rows; give all 70 affected rows a row-specific plan section, planned skill file/section, and objective fixture/linter/test; preserve every existing verification and disposition; totals become 213/213 precisely mapped.

### F4 — make the staged link boundary explicit and resolvable

**Reads:** the six unique unresolved target references listed under AG-14 plus the staging/package manifest that defines the Phase 2 bundle.

**Writes:** staging/package manifest and, if packaging is the selected resolution, only these staged target paths: `coding/software_design/glossary.md`, `coding/software_design/software_design.md`, `coding/software_design/strategic_tactical_design.md`, `skills-plugins/brainstorm-vision/SKILL.md`, `skills-plugins/create-vision-companion/SKILL.md`.

**Done:** either include those targets in the declared gate bundle/read allow-list or deliberately replace the six cross-bundle links with semantically equivalent resolvable targets; re-run the offline checker with 0 broken local-link occurrences. Do not silently weaken or remove the cross-collection references.

### Final rerun

After F1–F4 integrate, run the full 33-plus-declared-target bundle gate in a new fresh context. It must re-review 15/15 FIT §5.1 and 49/49 FIT §2, verify 0 Pending and 0 invalid dispositions, audit 15 distill and 6 Call rows, obtain 213/213 precise mappings, and report 0 broken local links before returning PASS.
