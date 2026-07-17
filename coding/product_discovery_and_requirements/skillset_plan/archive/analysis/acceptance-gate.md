# Phase 2 acceptance gate — final fresh-context rerun

**Verdict: PASS**

**Failed acceptance checkboxes:** none.

**Audit scope:** the exact 33 authoritative planning-bundle files specified by the revision contract. `acceptance-gate-initial-fail.md` and the prior version of this report were consulted only as audit history to verify F1–F4 and R1–R5 closure, never as authority. The five declared cross-bundle link targets were checked only for target existence; their contents and outgoing links were not audited. No network access was used. This report is the only write.

## Counts

| Measure | Result |
| --- | --- |
| Authoritative planning files read | 33/33 |
| Ordered updates | 11/11 reconciled across the plan, method docs, ledgers, reference map, linter, and regression rubric |
| FIT §5.1 recommendations | 15/15 mapped to contribution IDs and final dispositions |
| FIT §2 mechanisms/benefits/warnings | 49/49 with final dispositions, including `FIT-2-dddcrew-02` |
| Literal Pending contribution rows | 0 |
| Invalid final dispositions | 0 |
| Distill rows | 15/15 with explicit future six-point donor-audit tasks and license/provenance constraints |
| Call rows | 6/6 with bounded role, pin policy, fallback, and no-spine-ownership rule |
| Accepted/method-owned contribution mappings | 213/213; 213 unique IDs; 0 duplicate IDs; 0 missing plan/destination/objective triples |
| Method-coverage mappings | TL-MTH 13/13; DP-MTH 21/21; DR-MTH 12/12; SR-MTH 12/12; VR-MTH 12/12 |
| Lifecycle-tailoring completion checks | 8/8; roadmap adopt/skip is the explicit justified third check; RTS-13 covers adopt and skip; LNT-14 applies only on adoption |
| Separate fit-disposition trace rows | 1: `FIT-2-dddcrew-02`; correctly excluded from the established 213 denominator |
| Local Markdown-link occurrences | 347 checked from the 33 authoritative sources; 0 broken |
| External URL occurrences | 68 recorded; not network-checked |

## Prior-failure closure

| Repair | Result | Closure evidence |
| --- | --- | --- |
| F1 — FIT/ledger and `EXP#` drift | PASS | FIT §5.1 is 15/15 and FIT §2 is 49/49. `discover-product-contributions.md` gives `FIT-2-dddcrew-02` a separate **Adapt** trace to the corrected human-modelling-reference heading in `domain_discovery.md`. `VC-E11` is **Reject**, an allowed final disposition. `DP-013`, `DP-014`, the required artifact/trace table, authoring gate, linter destinations, and plan surfaces require the complete eleven-field card, including an explicit assumption/hypothesis distinct from target `ASM#`, applicable `SOL#`, and resulting `DEC#`. |
| F2 — alternative-count synchronization | PASS | The plan artifact table, representation decision, method coverage, LNT-07, trace diagram, §5.4, and RTS-04 all say **≥3 materially different directions or `DEC#`**. No stale `≥2` remains in a current plan/ledger/method surface; the only `≥2` text is historical evidence inside the prior failed-gate report. |
| F3 — method-coverage traceability | PASS | Stable IDs and row-specific plan/file/test triples now exist for TL-MTH-01..13, DP-MTH-01..21, DR-MTH-01..12, SR-MTH-01..12, and VR-MTH-01..12. Machine extraction of all seven final trace tables yields 213/213 unique accepted/method-owned mappings, with no missing or duplicate triple. |
| F4 — staged link boundary | PASS | All five declared extra targets exist. Rechecking every local Markdown link originating in the 33 authoritative files gives 347 occurrences and 0 broken targets. The checker did not recurse into outgoing links from the five extras. |

## Final-review closure

| Finding | Result | Closure evidence |
| --- | --- | --- |
| R1 — `EXP#` schema | PASS | Contract Update 6 keeps **assumption/hypothesis** separate from target `ASM#`. The plan artifact table, §2.1, LNT-19, §3.1 `prototype` contract, §3.3 DP-007 donor task, and §5.4 schema/finalize text all carry the same eleven fields. In the discovery ledger, DP-007/013/014/020/023, DP-MTH-10, the required artifact table, authoring gate, and final trace destinations agree. The first eight fields are required-resolved; a missing or `OPEN:` hypothesis fails LNT-19. |
| R2 — Call semantics | PASS | `DP-020` and `DP-022` have final dispositions exactly **Call**, not inferred from reuse-mode text. Their ledger rows and plan §3.1 preserve named callers/conditions, bounded inputs and outputs, local skill/version-or-commit pinning, explicit manual/local fallback, and the global rule that callees never own, write, or mutate spine artifacts. Counting all final Call dispositions yields exactly 6/6: DP-020, DP-022, DR-EXT-07, SR-EXT-05, VR-EXT-01, VR-EXT-09. |
| R3 — lifecycle template | PASS | `lifecycle_tailoring.md`'s one-pager says to repeat one block for every consequential decision type and stage in use. That block exposes exactly the seven required fields: accountable owner, required contributors, specialist authorities, formal approvers, evidence required, escalation path, and evidence-based reopen trigger. The separate global `## Revisit trigger` remains, and the plan/ledger preserve `lifecycle-onepager.md` as the sole output. |
| R4 — Markdown and audit durability | PASS | `specify-requirements-contributions.md` has coherent top-level order `## 3. Method-document coverage ledger` → `## 4. Builder/reviewer protocol` → `## 5. Deterministic checks`; its references to ledger §4 resolve to the builder/reviewer steps. `acceptance-gate-initial-fail.md` exists in this repository mirror and remains the durable F1–F4 failure record. |
| R5 — lifecycle completion-count repair | PASS | `lifecycle_tailoring.md` is authoritative and has exactly eight completion checks; the explicit justified roadmap adopt/skip decision is check 3. Plan §5.3 enumerates those same eight checks in the same order. `TL-MTH-09`, the current authoring gate, and `fixtures/finalize-eight-checks` all say eight, require a separate result for each check, use the paired RTS-13 adopt/skip variants, and apply LNT-14 only to adoption. No current authority retains a stale seven-check count/name; the seven ceremony drivers and seven decision-authority fields remain legitimate, distinct contracts. Frozen analysis/history retains its historical six/seven finding as input provenance only. |

## Acceptance checklist

| Gate | Result | Precise evidence |
| --- | --- | --- |
| AG-01 — FIT §§5.1 and 2 | PASS | The complete FIT tables below account for 15/15 §5.1 keys and 49/49 §2 keys. The formerly missing `FIT-2-dddcrew-02` is explicitly Adapted in the discovery ledger and realized in `domain_discovery.md`. |
| AG-02 — ordered updates 1–3 wired | PASS | Update 1: plan §§2, 2.1, 2.2/LNT-07, 4 diagram, 5.4 and 6/RTS-04 agree on `SOL#`, ≥3-or-`DEC#`, ranking-time refusal, and the completion check. Update 2: §2.2 defines a deterministic script, LNT-01..19, open-marker semantics, and separate judgment reporting; §§3 and 5 invoke applicable checks. Update 3: §6 defines the fixed blind reference topic, five axes, failure attribution/re-run, and RTS-01..13. |
| AG-03 — accepted contributions and deferrals | PASS | The seven final trace sections map every accepted/method-owned row to plan and authoring evidence. Rejected/deferred rows retain reasons/receivers; design/domain items, including `SR-EXT-12`, name the future design skillset. |
| AG-04 — method-doc coverage | PASS | Plan §2.1 maps all 13 method docs to consuming skills. The repaired method rows total TL 13/13, DP 21/21, DR 12/12, SR 12/12, and VR 12/12, each with a concrete plan/file/test triple. In particular, TL-MTH-09 maps the authoritative eight-check lifecycle rubric—including explicit justified roadmap adopt/skip as check 3—to `fixtures/finalize-eight-checks`; RTS-13 supplies both variants and LNT-14 is adoption-only. |
| AG-05 — Distill policy | PASS | Plan §§3.2–3.3 enumerate all 15 rows and require the contract's six audit fields before vendoring. Dean Peters and unlicensed Florian Bonnet material remain no-copy/no-distill; Argo remains pattern-only unless its license is verified; North Star remains call-only. |
| AG-06 — Call contracts | PASS | The six rows are counted from their final Call dispositions/semantics, not reuse-mode inference. Plan §3.1 gives each named callers/condition, inputs/outputs, exact-version policy, fallback, and the global rule that callees never own/write/mutate spine artifacts. |
| AG-07 — cross-cutting handover/re-entry/ownership/linter/validation/provenance/skips | PASS | Plan §§3.2–3.3, 4.1–4.2 and 5.1–5.7 instantiate all fields per affected skill. Ledgers carry handover rows, method-owned ownership/specialist rows, linter calls, source duties, recorded skips, and exact-artifact re-entry routes; RTS-02 and RTS-07..10 exercise the refusal paths. |
| AG-08 — `SOL#`/`EXP#` consistency | PASS | Artifact table, ID/trace model, diagram, §5.4, LNT-03/LNT-07/LNT-19, DP-007/013/014/020/023, DP-MTH-05/06/07/10, required trace table, authoring gate, and RTS-04 agree on the complete eleven-field card, explicit assumption/hypothesis distinct from target `ASM#`, applicable `SOL#`, resulting `DEC#`, required/open semantics, and ≥3-or-`DEC#`. |
| AG-09 — collaboration/ownership and vision stability | PASS | Applicable method-owned rows exist (`BV-M12..14`, `VC-M11..12`, `TL-M01..02`, `DP-M01..04`, `DR-M01..05`, `SR-M01..04`, `VR-M01..04`). Plan §§4–5 supplies fields, gates, refusals and routes; RTS-07..13 covers them. No standalone ownership/strategy skill or mandatory runtime document is introduced. |
| AG-10 — post-authoring reconciliation | PASS | Plan §3.3 requires planned evidence to be replaced by actual files/tests, reopens rows on method/donor/schema change, and blocks authoring completion until `overview.md`, affected method docs, implemented skills, lifecycle/artifacts, strategy/roadmap, `SOL#`, one-pagers, and linter agree. No skill authoring is claimed by this planning bundle. |
| AG-11 — no unexplained omission | PASS | 33/33 authoritative files were read; 0 Pending and 0 invalid dispositions remain; FIT is 15/15 + 49/49; Distill is 15/15 and Call is 6/6. Accepted/method-owned mappings are 213/213 unique and complete, distributed 23/24/31/56/28/26/25 across the seven ledgers. R5 changes completion-check depth, not the mapping denominator: lifecycle completion is exactly 8/8, while the separate seven ceremony drivers and seven ownership fields remain intact. All nine frozen digests, fit §§2/3/5, ordered updates, dependency/license exclusions, and the final plan were reconciled. |
| AG-12 — complete contribution mapping | PASS | The per-ledger tables below enumerate every accepted/method-owned ID and its plan location plus planned file/section and objective test: 213/213, no duplicate or missing triple. |
| AG-13 — reference-map synchronization and Update 11 | PASS | `resources.md` carries synchronized vision/discovery/definition/requirements/validation/tailoring/collaboration rows. Row 10 names entry point, ceremony, stage/artifact selection, cadence and authority, including seven drivers, six entry classes, roadmap adopt/skip, one-pager, authority record and handover/out-of-order enforcement. Plan §9 records the confirmed/rejected Update-11 candidates. |
| AG-14 — planning-bundle links | PASS | 347 local occurrences from the exact 33 sources resolve, including the five declared cross-bundle targets; 0 broken. 68 external URLs were not network-checked. |

## FIT §5.1 — 15/15

| Key | Final mapping/disposition |
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
| `FIT-5.1-15` | `SR-EXT-12` Defer to the future design skillset; matching explicit exclusions remain in other ledgers |

## FIT §2 — 49/49

Every key is explicit below; semicolon-separated numeric suffixes are individual FIT keys for the named repository.

| Repository | Key → final evidence/disposition |
| --- | --- |
| deanpeters | `01`→`BV-E02`/`TL-002` Adapt; `02`→`BV-E01` Adapt; `03`→`DP-018` Adapt, independently authored/no-copy; `04`→`DR-EXT-10`/`SR-EXT-09` Reject distillation; `05`→plan two-mode architecture + `BV-E09` no runtime dependency |
| phuryn | `01`→handover rows at FIT-5.1-13; `02`→`DR-EXT-08`/`VR-EXT-02` Adapt local fallback, no second call; `03`→wholesale-marketplace Reject in exclusions/routing; `04`→`VC-E12`/`DP-029` Reject competing pipeline |
| huntsyea | `01`→`DP-001..003`, `DR-EXT-01/02`, `SR-EXT-08`; `02`→same donor rows; `03`→`VC-E07`/`BV-E02` progressive-disclosure layout; `04`→`DP-026`/`TL-009` vendor, never live-call |
| argo | `01`→`DP-008` Adapt; `02`→`DP-009` Adapt; `03`→`DP-010` Adapt; `04`→`DP-011` Adapt; `05`→`DP-029` + explicit workspace/operator Reject |
| assimovt | `01`→`DP-004` Adopt; `02`→`DP-004..007`, `DR-EXT-03/04`; `03`→`TL-004` Adapt; `04`→`DP-029` single-spine Adapt/competing-chain Reject |
| shinpr | `01`→`DP-014` Adapt; `02`→`SR-EXT-01` Adopt; `03`→`VC-E01` Adapt; `04`→`VC-E01`/plan repo-artifact confirmation; `05`→`VC-E12`/`DP-029` Reject pipeline taxonomy |
| gorski | `01`→`SR-EXT-03`/`DP-023` Adapt; `02`→`DR-EXT-06` Adapt; `03`→`SR-EXT-03` rejects `.spec`/`CP/CN/FR`; `04`→`VC-E12` Reject competing upstream |
| 45ck | `01`→`SR-EXT-05` conditional Call; `02`→same row's three-leg audit + local fallback; `03`→`SR-EXT-12` Defer |
| daves | `01`→`SR-EXT-07` Adapt; `02`→`SR-EXT-06` Adapt; `03`→`SR-EXT-06`/exclusions Reject vault ecosystem; `04`→`VC-E10` already-covered independent review |
| dddcrew | `01`→`SR-EXT-12` Defer/reference with CC BY attribution; `02`→separate FIT trace **Adapt**, correcting `domain_discovery.md` to “Human modelling-process reference” |
| forceinjection | `01`→`VR-EXT-04`/`DR-EXT-12` Adapt; `02`→`DP-025`, `VC-E06`, `TL-008` Adapt; `03`→`SR-EXT-12` Defer |
| lagz0ne | `01`→`SR-EXT-12` Defer |
| northstar | `01`→`DR-EXT-07`/`VR-EXT-01` Call; `02`→same bounded call contracts; `03`→plan §§3.1–3.2 call-only copyright/provenance rule |
| florianbonnet | `01`→`VR-EXT-03` independently authored Adapt; `02`→same row's unlicensed/no-copy restriction |

## Distill and Call audits

| Mode | Rows | Result |
| --- | --- | --- |
| Distill (15) | `DP-001`, `DP-002`, `DP-003`, `DP-004`, `DP-005`, `DP-006`, `DP-007`, `DP-012`, `DP-019`, `DR-EXT-01`, `DR-EXT-02`, `DR-EXT-03`, `DR-EXT-04`, `DR-EXT-05`, `SR-EXT-08` | 15/15 scheduled in plan §3.3 with the six-point authoring-time donor audit; no incompatible/unlicensed copy is scheduled |
| Call (6) | `DP-020`, `DP-022`, `DR-EXT-07`, `SR-EXT-05`, `VR-EXT-01`, `VR-EXT-09` | 6/6 counted from final Call dispositions/semantics and covered by plan §3.1's role/pin/input/output/fallback table and no-spine-ownership rule |

## Complete contribution → plan → planned file/section + objective test mapping

The following is a compact extraction of the seven machine-scannable final trace sections, joined to each ledger row's verification field. Rejected/deferred rows are intentionally outside the accepted/method-owned denominator. Each listed ID is included once.

### `brainstorm-vision` — 23/23

| ID(s) | Plan | Planned file/section + objective test |
| --- | --- | --- |
| `BV-E01` | §5.1 | Optional press-release stress-test phase; feature-shaped-vision reopen fixture |
| `BV-E02` | §5.1 | `SKILL.md` file-responsibility map; static separation review |
| `BV-E03` | §§4.1, 5.1 | `SKILL.md` finalize/handover template; artifact-path/next-skill fixture |
| `BV-E05` | §5.1 | Bounded finalize checks; low-ceremony minimum-artifact fixture |
| `BV-E06` | §5.1 | Scope-lens human gate/route-back; silent-climb refusal tests |
| `BV-E07` | §5.1 | `.wip.md`/foundation-vision resume handling; durable-state test |
| `BV-E08` | §§4.2, 5.1 | Backtracking route table; one test per trigger/destination |
| `BV-E09` | §§3.1, 3.2, 5.1 | Empty dependency manifest; no-live-fetch/unpinned-call audit |
| `BV-E10` | §§2.1, 5.1 | `SKILL.md` drift-gate note; consumed-provision implementation audit |
| `BV-M01` | §§2.1, 5.1 | Finalize coverage stubs; recommended-section fixture |
| `BV-M02` | §§2.1, 5.1 | Six-check finalize gate; pass/reopen/explicit-open report |
| `BV-M03` | §§2.1, 5.1 | Optional-lens reference; selection/skip-path review |
| `BV-M04` | §§2.1, 5.1 | Finish-response wording; no-false-validation fixture |
| `BV-M05` | §§2.1, 5.1 | Output schema/handoff; minimum-package/no-loop-artifact test |
| `BV-M06` | §§2.1, 5.1 | Session-start one-pager inspection; greenfield/non-greenfield fixtures |
| `BV-M07` | §2.1 | Method-vocabulary alignment; terminology lint |
| `BV-M08` | §§2.1, 5.1 | Seed/stub finalize rules; no-invented-loop-ID fixture |
| `BV-M09` | §§2.1, 5.1 | Architecture-significance sweep; parked-constraint/no-premature-QAS test |
| `BV-M10` | §§2.1, 5.1 | Observable-or-`OPEN:` outcome gate; shipment/usage rejection fixture |
| `BV-M11` | §2.1 | Per-lens decision-purpose rules; selection/skip review |
| `BV-M12` | §§2, 2.1, 5.1 | Strategy finalize section; populated/open/missing + no-roadmap RTS-13 fixtures |
| `BV-M13` | §§4, 5.1 | Vision-pivot route table; RTS-11/RTS-12 |
| `BV-M14` | §§2.1, 5.1 | Ownership/specialist fields in finalize/scope-lens files; RTS-07/08 |

### `create-vision-companion` — 24/24

| ID(s) | Plan | Planned file/section + objective test |
| --- | --- | --- |
| `VC-E01` | §5.2 | `discovery-seeds.md` template/builder/README; bundle-completeness test |
| `VC-E02` | §5.2 | `SKILL.md` orchestrator + critic briefs; reasoning-leakage tests |
| `VC-E04` | §§2.2, 5.2 | Phase-9 shared-linter wiring; mechanical-gate mutations |
| `VC-E05` | §§4.2, 5.2 | Re-entry matrix; every failure routes to an owning phase |
| `VC-E06` | §§5.2, 6 | Fresh/upgrade/diff/recovery fixture suite |
| `VC-E07` | §5.2 | File-responsibility map; owning-file static review |
| `VC-E08` | §§4.1, 5.2 | Finalize/handoff section; five-field handoff fixture |
| `VC-E09` | §5.2 | `_status.md`/review files + Phase-11 gate; durable-state test |
| `VC-E10` | §5.2 | Multi-critic architecture/rubrics; independent-verdict fixtures |
| `VC-E12` | §5.2 | Proprietary-only schema inventory; taxonomy guardrail test |
| `VC-E13` | §§3.1, 3.2, 5.2 | Dependency/pattern-source ledger; no-runtime-call/provenance audit |
| `VC-E14` | §§5.2, 6 | Release-blocking authoring gate + validation matrix feeding regression |
| `VC-M01` | §§2.1, 5.2 | Coverage rubrics; recommended-section coverage fixtures |
| `VC-M02` | §§2.1, 5.2 | Seed/judgment routing; unsupported-promotion test |
| `VC-M03` | §§2.1, 5.2 | README load order/handoff; downstream-consumer fixture |
| `VC-M04` | §§2.1, 5.2 | Start gate; finalized-vision/one-pager tests |
| `VC-M05` | §§2.1, 5.2 | Seed schema; no-loop-ID promotion test |
| `VC-M06` | §§2.1, 5.2 | `domain-glossary.md` rename; collision/terminology test |
| `VC-M07` | §§2.1, 5.2 | Architecture-lens routing; no-invented-QAS test |
| `VC-M08` | §§2.1, 5.2 | Method-vocabulary orchestration; naming lint |
| `VC-M09` | §§2.1, 5.2 | Outcome/guardrail gap findings; missing/usage-only fixtures |
| `VC-M10` | §§2.1, 5.2 | Per-file purpose/consumer statements; README/template review |
| `VC-M11` | §§2, 2.1, 5.2 | Strategy index derivation; source-order and populated/stubbed/absent fixtures |
| `VC-M12` | §§4, 5.2 | Derived-only `DEC#` rebuild gate; RTS-11/12 |

### `tailor-lifecycle` — 31/31

| ID | Plan | Planned file/section + objective test |
| --- | --- | --- |
| `TL-001` | §§4.1, 5.3 | `SKILL.md` handover; entry-class handover fixtures |
| `TL-002` | §5.3 | Compact interactive `SKILL.md`; independent-structure review |
| `TL-003` | §5.3 | Interview phase; low/high-risk depth fixtures |
| `TL-004` | §5.3 | Minimum-ceremony defaults; low-risk selection/skip fixture |
| `TL-005` | §§4.2, 5.3 | One-pager revisit triggers; concrete-trigger test |
| `TL-006` | §§2.2, 5.3 | Finalize shared-linter call; malformed/collision mutations |
| `TL-007` | §§2.2, 5.3 | Separate deterministic/judgment report; report-schema test |
| `TL-008` | §§5.3, 6 | Reference-topic run; scored failure-disposition report |
| `TL-009` | §§3.2, 5.3 | Dependency/source manifest; pin/provenance/no-fetch review |
| `TL-010` | §§3.2, 3.3, 5.3 | Executed source-audit manifest; no-Pending audit test |
| `TL-011` | §5.3 | Canonical terminology; terminology fixtures |
| `TL-012` | §5.3 | Sole-output contract; file-output test |
| `TL-013` | §§4.1, 5.3 | Skipped-stage section; silent-skip finalize failure |
| `TL-014` | §§4.1, 5.3 | Entry-derived handover rules; rework/mandate/fast-follow fixtures |
| `TL-015` | §5.3 | Authority section/validator; missing/group/multiple-owner tests |
| `TL-016` | §5.3 | Uncertainty-driven stage/artifact rules; routing fixtures |
| `TL-MTH-01` | §§2.1, 4, 5.3, 6 | `SKILL.md` lifecycle model; six-entry/ceremony RTS-01/02 fixtures |
| `TL-MTH-02` | §§2.1, 4, 5.3, 6 | Entry-point classification; six rationale-bearing fixtures |
| `TL-MTH-03` | §§2.1, 5.3, 6 | Ceremony sizing; mixed-risk per-driver RTS-01/13 fixture |
| `TL-MTH-04` | §§2.1, 5.3, 6 | Stage/artifact selection + one-pager template; silent-skip RTS-02/13 test |
| `TL-MTH-05` | §§2.1, 5.3 | Cadence/cycle-output section; no-decision-output rejection |
| `TL-MTH-06` | §§2.1, 5.3, 6 | Decision-authority fields; group/missing/escalation RTS-07/09 |
| `TL-MTH-07` | §§2, 2.1, 2.2, 5.3 | One-pager template; golden schema + roadmap-pair RTS-13 |
| `TL-MTH-08` | §§2.1, 5.3 | Failure-mode rubric; seven adversarial fixtures |
| `TL-MTH-09` | §§2.1, 5.3, 6 | Eight-check lifecycle completion rubric; one separated result per check, including explicit justified roadmap adopt/skip as check 3; paired RTS-13 variants, with LNT-14 only on adoption |
| `TL-MTH-10` | §§2.1, 5.3 | Technique routing; dominant-uncertainty fixtures |
| `TL-MTH-11` | §§2.1, 5.3 | Terminology contract; terminology audit |
| `TL-MTH-12` | §§2.1, 3.2–3.3, 5.3, 6 | Source-audit manifest/gate; undecided/provenance/fetch/pin mutations |
| `TL-MTH-13` | §§2.1, 4.1, 5.3, 6 | Output/finalize/handover; tailored-downstream handover fixture |
| `TL-M01` | §5.3 | Seven-field authority template/interview/validator; RTS-07 |
| `TL-M02` | §5.3 | Specialist-participation question/fields; RTS-08 |

### `discover-product` — 56/56

| ID | Plan | Planned file/section + objective test |
| --- | --- | --- |
| `DP-001` | §§3.2, 3.3, 5.4 | Vendored per-phase techniques/anti-patterns + manifest; item→destination/test audit |
| `DP-002` | §§3.3, 5.4 | Optional JTBD lens; uncertainty-routing fixture |
| `DP-003` | §§3.3, 5.4 | Anti-pattern coverage table; no-unassigned-item test |
| `DP-004` | §§3.3, 5.4 | Evidence-phase past-behavior guardrails; weak-evidence fixtures |
| `DP-005` | §§3.3, 5.4 | Problem-validation rubric; applicability/confidence fixture |
| `DP-006` | §§3.3, 5.4 | `OPP#` neutrality/hierarchy checks; per-guardrail disposition audit |
| `DP-007` | §§3.3, 5.4 | `EXP` design guidance; eleven-field LNT-19/LNT-03/07 tests, including missing/`OPEN:` hypothesis failure |
| `DP-008` | §§2, 5.4, LNT-18 | Evidence-quality rubric; Rich/Mixed/Thin golden fixtures |
| `DP-009` | §§2, 5.4, LNT-18 | Confidence cap; weak-evidence inflation test |
| `DP-010` | §§2, 5.4 | Opportunity routing; four-route/provenance fixtures |
| `DP-011` | §§2, 5.4 | Human gate/awaiting-review marker; interview/AFK authority fixtures |
| `DP-012` | §§2, 3.3, 5.4 | Generate-alternatives phase; ≥3 ranking/finalize RTS-04 |
| `DP-013` | §§2, 2.2, 5.4 | `OPP→SOL→ASM→EXP` fields + resulting `DEC`; LNT-07/19 mutations |
| `DP-014` | §§2, 2.2, 5.4 | Eleven-field experiment-card template; LNT-19 schema/open-marker tests |
| `DP-015` | §5.4 | Separated critic instructions; no-builder-expectation fixture |
| `DP-016` | §5.4, LNT-04 | Workspace-index step; unindexed-artifact mutation |
| `DP-017` | §§4.1, 5.4 | Wrap-up handover; verdict/next-stage/artifact fixtures |
| `DP-018` | §5.4 | Independently authored convergence prompts; no-copy/preferred-solution test |
| `DP-019` | §§3.1, 3.3, 5.4 | Cheapest-trustworthy-test guidance; four-risk method-selection fixtures |
| `DP-020` | §§3.1, 5.4 | `prototype` contract; same-card/observation/fallback integration test |
| `DP-021` | §5.4 | Early quality-risk prompt; classified-assumption/no-premature-QAS fixture |
| `DP-022` | §§3.1, 4.2, 5.4 | `domain-modeling` contract; canonical-artifact/manual-fallback fixture |
| `DP-023` | §§2.2, 5.4 | Finalize linter; citation/card/open/reserved-name mutations |
| `DP-024` | §§4.2, 5.4 | Adapt reopen instructions; named `SOL`/`ASM` route fixture |
| `DP-025` | §§5.4, 6 | Blind reference-topic run; scored report |
| `DP-026` | §§3.2, 5.4 | Source/dependency manifest; provenance/pin/no-fetch review |
| `DP-027` | §3.3 | Executed donor-audit manifest; path/candidate completeness test |
| `DP-028` | §5.4 | Evidence non-fabrication guardrail; missing-evidence adversarial test |
| `DP-029` | §5.4 | Single-spine guardrail; output/dependency audit |
| `DP-030` | §5.4 | Predeclared thresholds; endless-research rejection fixture |
| `DP-031` | §2 | Rejected/parked `SOL` retention; deletion/traceability fixture |
| `DP-MTH-01` | §§2.1, 5.4, 6 | Four-risk section/rubric; four + multi-risk fixtures |
| `DP-MTH-02` | §§2.1, 5.4, 6 | Frame-outcome phase; feature-vs-outcome fixture |
| `DP-MTH-03` | §§2, 2.1, 2.2, 5.4, 6 | Gather-evidence phase/rubric; source/strength + RTS-03 mutations |
| `DP-MTH-04` | §§2, 2.1, 5.4 | Map-opportunities phase/template; feature-shaped rejection |
| `DP-MTH-05` | §§2, 2.1, 2.2, 5.4, 6 | Generate-alternatives phase/template; ≥3-or-`DEC` RTS-04 |
| `DP-MTH-06` | §§2, 2.1, 2.2, 5.4, 6 | Assumption phase/template; anchor/ranking-time refusal fixture |
| `DP-MTH-07` | §§2, 2.1, 2.2, 3.1, 5.4 | Test-cheaply phase/reference; method-fit + LNT-19 tests |
| `DP-MTH-08` | §§2, 2.1, 4.1–4.2, 5.4 | Decide/handover phase; four-verdict route fixture |
| `DP-MTH-09` | §§2, 2.1, 5.3, 5.4, 6 | Tailored-artifact section; low-ceremony RTS-01/02 fixture |
| `DP-MTH-10` | §§2, 2.1, 2.2, 5.4 | Experiment-card template; eleven-field/citation/open-marker fixture |
| `DP-MTH-11` | §§2.1, 5.4, 6 | Failure-mode reference; one adversarial test per mode |
| `DP-MTH-12` | §§2.1, 5.4, 6 | Completion rubric; one scored result per check |
| `DP-MTH-13` | §§2.1, 3.1, 4.2, 5.4 | Domain-work trigger; pinned-call/fallback/no-duplicate-glossary fixture |
| `DP-MTH-14` | §§2.1, 5.4 | Early-quality-risk section; assumption/no-QAS fixture |
| `DP-MTH-15` | §§2.1, 5.4 | Test-selection reference; decision-fit technique fixture |
| `DP-MTH-16` | §§2.1, 5.4 | Terminology contract; terminology audit |
| `DP-MTH-17` | §§2.1, 4, 5.4, 6 | Minimum package/readiness; discovery-to-readiness trace fixture |
| `DP-MTH-18` | §§2, 2.1, 4, 5.4, 6 | Strategy/pivot gate; off-strategy + RTS-11/12 |
| `DP-MTH-19` | §§2.1, 4.1, 5.3, 5.4, 6 | Read-one-pager start/handover; tailoring RTS-01/02/13 |
| `DP-MTH-20` | §§2.1, 3.2–3.3, 5.4, 6 | Source-audit/gate; undecided/update/provenance/pin failures |
| `DP-MTH-21` | §§2.1, 3.1, 4.1, 5.4, 6 | Inputs/spine/calls/handover; end-to-end trace fixture |
| `DP-M01` | §§4, 5.4 | Pivot classifier/vision route; RTS-11/12 |
| `DP-M02` | §§2, 5.4 | Strategy selection gate; exception/reorder/index-refresh fixture |
| `DP-M03` | §5.4 | `DEC` owner binding; group-only-owner RTS-07 |
| `DP-M04` | §5.4 | Specialist-input guard; missing-input RTS-08 |

### `define-release` — 28/28

| ID | Plan | Planned file/section + objective test |
| --- | --- | --- |
| `DR-EXT-01` | §§3.3, 5.5, 2.2 | Story-mapping reference; end-to-end vs single-layer slice fixture |
| `DR-EXT-02` | §§3.3, 5.5 | Ceremony-gated shaping/appetite in `REL`; proportional-path fixture |
| `DR-EXT-03` | §§3.3, 5.5 | Scope-cutting prompts/check; disconnected-items rejection |
| `DR-EXT-04` | §§3.3, 5.5 | Proportional-investment check; reversible/irreversible fixture |
| `DR-EXT-05` | §§2.2, 3.3, 5.5 | Evidence-first scope guardrails; untraced-scope mutation |
| `DR-EXT-06` | §§2.2, 5.5 | O/E/H fields; unclassified-must/consequence tests |
| `DR-EXT-07` | §§3.1, 5.5 | `north-star` call/review metadata; call/skip/fallback fixtures |
| `DR-EXT-08` | §5.5 | Local metric-tree prompts; local-fallback review fixture |
| `DR-EXT-09` | §5.5, LNT-08 | Enriched `REL` hypothesis; precommit/card-schema tests |
| `DR-EXT-11` | §§4.1, 5.5 | Final handover; start-without-rediscovery fixture |
| `DR-EXT-12` | §§4.2, 5.5 | Backtracking matrix; exact-artifact/owner/next-skill tests |
| `DR-MTH-01` | §§2.1, 4, 5.5, 6 | Lifecycle/readiness sections; definition-to-readiness fixture |
| `DR-MTH-02` | §§2.1, 4.1, 5.3, 5.5, 6 | One-pager start gate; tailored-definition RTS-01/02/13 |
| `DR-MTH-03` | §§2, 2.1, 4, 5.5, 6 | Vision boundary/backtracking; RTS-11/12 conflict fixture |
| `DR-MTH-04` | §§2, 2.1, 2.2, 5.5 | Discovery-input gate; missing/fabricated input rejection |
| `DR-MTH-05` | §§2, 2.1, 2.2, 5.5, 6 | Release template/rubric; full method conformance fixture |
| `DR-MTH-06` | §§2.1, 5.5 | Story-mapping section; coherent-slice fixture |
| `DR-MTH-07` | §§2.1, 3.1, 5.5 | Canonical-language gate; pinned-call/no-duplicate-glossary fixture |
| `DR-MTH-08` | §§2.1, 5.5 | Quality-risk/trade-off check; silent-deferral rejection |
| `DR-MTH-09` | §§2.1, 2.2, 5.5–5.6 | Observation fields/handoff; instrumentation fixture |
| `DR-MTH-10` | §§2, 2.1, 2.2, 5.5, 5.7 | Precommitted criteria/review owner; no-retrofit fixture |
| `DR-MTH-11` | §§2.1, 5.5 | Terminology contract; terminology audit |
| `DR-MTH-12` | §§2.1, 5.5 | Technique-selection section; used/unused technique fixture |
| `DR-M01` | §5.5 | Seven-field `REL` decision metadata; RTS-07 |
| `DR-M02` | §5.5 | Specialist-participation finalize check; RTS-08 |
| `DR-M03` | §§2, 5.5 | Strategy-order gate; exception/reorder/index-refresh fixture |
| `DR-M04` | §§2.2, 5.3, 5.5 | Conditional roadmap; RTS-13 pair |
| `DR-M05` | §§4, 5.5 | Evidence/`DEC` vision route; RTS-11/12 |

### `specify-requirements` — 26/26

| ID | Plan | Planned file/section + objective test |
| --- | --- | --- |
| `SR-EXT-01` | §5.6 | Fresh-critic orchestration/brief; withheld-rationale fixtures |
| `SR-EXT-02` | §5.6, LNT-04 | Durable alternatives/index/handover; stale-index mutation |
| `SR-EXT-03` | §§2.2, 5.6 | Shared trace-linter wiring; chain mutations/no foreign IDs |
| `SR-EXT-04` | §§2.2, 5.6 | REQ/QAS rationale fields; O/E/H scope-trace tests |
| `SR-EXT-05` | §§3.1, 5.6 | Conditional QAS-writer call; depth/pin/local-fallback comparison |
| `SR-EXT-06` | §5.6 | ISO-flavoured QAS prompts; no-vault-schema review |
| `SR-EXT-07` | §5.6 | Complete/Measurable/Feasible rubric; QAS gate fixtures |
| `SR-EXT-08` | §§3.3, 5.6, LNT-16 | UC guidance bound to slice; scope-boundary fixture |
| `SR-EXT-10` | §§4.1, 5.6 | Final handover; readiness/artifact/open-confirmation test |
| `SR-EXT-11` | §§4.2, 5.6 | Failed-gate routes; named target/owner fixture |
| `SR-MTH-01` | §§2.1, 4, 5.6, 6 | Lifecycle/readiness gate; specification-to-readiness fixture |
| `SR-MTH-02` | §§2.1, 4.1, 5.3, 5.6, 6 | One-pager start gate; tailored-spec RTS-01/02 |
| `SR-MTH-03` | §§2, 2.1, 2.2, 5.5–5.6 | Release-boundary section; scope-drift fixture |
| `SR-MTH-04` | §§2, 2.1, 2.2, 5.6, 6 | Requirements template/rubric/orchestration; full conformance fixture |
| `SR-MTH-05` | §§2, 2.1, 5.6 | Use-case template/section; completeness fixture |
| `SR-MTH-06` | §§2.1, 3.1, 4.2, 5.6 | Domain-gap route; call/fallback/canonical-update fixture |
| `SR-MTH-07` | §§2, 2.1, 2.2, 3.1, 5.6 | QAS template/gate; six-field/quality/fallback fixture |
| `SR-MTH-08` | §§2.1, 2.2, 5.5–5.7 | Observation/transition sections; instrumentation/retirement fixture |
| `SR-MTH-09` | §§2, 2.1, 4, 5.6 | Vision-reference/conflict route; preservation fixture |
| `SR-MTH-10` | §§2.1, 2.2, 5.4–5.6 | Upstream trace section/fields; broken-trace fixture |
| `SR-MTH-11` | §§2.1, 5.6 | Terminology contract; terminology audit |
| `SR-MTH-12` | §§2.1, 5.6 | Proportionate technique section; selection/ceremony rejection fixture |
| `SR-M01` | §5.6 | Human-gate owner/handover; RTS-07 |
| `SR-M02` | §5.6 | QAS feasible-specialist verdict; RTS-08 |
| `SR-M03` | §5.6 | Proposal flags + critic invention check; LNT-05 fixture |
| `SR-M04` | §5.6 | Owned/escalated backtracking + invalidation refusal; RTS-10 |

### `validate-release` — 25/25

| ID | Plan | Planned file/section + objective test |
| --- | --- | --- |
| `VR-EXT-01` | §§3.1, 5.7 | `north-star` call/review result; call/skip/fallback fixture |
| `VR-EXT-02` | §5.7 | Local metric-tree fallback; local-review fixture |
| `VR-EXT-03` | §§2, 2.2, 5.7 | Timestamped analysis-plan gate; post-hoc-plan mutation |
| `VR-EXT-04` | §§4.2, 5.7 | Ten-condition re-entry matrix; route fixtures |
| `VR-EXT-05` | §§4.1, 5.7 | Closing handover; exact-ID/owner/skill/file fixture |
| `VR-EXT-06` | §§5.7, 6 | Context-separated verifier; confirmation-bias fixture |
| `VR-EXT-07` | §§2.2, 5.7 | Pre-routing linter; citation/index/review mutations |
| `VR-EXT-08` | §§2, 2.2, 5.7 | Post-release EV strength/cap; confidence mutation |
| `VR-EXT-09` | §§3.1, 5.7 | QA/triage intake; source-addressed/manual fallback fixture |
| `VR-MTH-01` | §§2, 2.1, 2.2, 4.2, 5.7, 6 | Review/re-entry/rubric references; full validation conformance fixture |
| `VR-MTH-02` | §§2, 2.1, 2.2, 5.5–5.7 | Precommitted-input section; post-hoc criteria rejection |
| `VR-MTH-03` | §§2.1, 2.2, 4.2, 5.6–5.7 | Requirement-impact/measurement-repair route; retirement fixture |
| `VR-MTH-04` | §§2, 2.1, 2.2, 4.2, 5.4–5.7 | Discovery-evidence routing; exact OPP/ASM re-entry fixture |
| `VR-MTH-05` | §§2.1, 4.2, 5.7 | Journey/use-case route; misuse/workaround/failure fixture |
| `VR-MTH-06` | §§2.1, 4.2, 5.7 | Quality/operational route; QAS/REQ fixture |
| `VR-MTH-07` | §§2.1, 3.1, 4.2, 5.7 | Domain route; call/fallback/canonical-update fixture |
| `VR-MTH-08` | §§2.1, 4, 4.2, 5.7, 6 | Vision-stability gate; RTS-11/12 + over/under-escalation fixture |
| `VR-MTH-09` | §§2.1, 4.2, 5.3, 5.7, 6 | Cadence/authority + retailoring route; RTS-07/09 fixture |
| `VR-MTH-10` | §§2.1, 4, 5.7, 6 | Outcome-not-shipping section; shipped-without-outcome rejection |
| `VR-MTH-11` | §§2.1, 5.7 | Validation terminology contract; terminology audit |
| `VR-MTH-12` | §§2.1, 5.7 | Analysis-plan technique/evidence section; pre-result method-fit fixture |
| `VR-M01` | §5.7 | Analysis/route owner fields; RTS-07 |
| `VR-M02` | §5.7 | Specialist-EV/`OPEN:` intake; RTS-08 |
| `VR-M03` | §§4, 5.7 | Pivot labels/foundational-only gate; RTS-11/12 |
| `VR-M04` | §5.7 | Authority-boundary/closure fields; RTS-09/10 |

## Link boundary evidence

The five declared targets all exist:

- `coding/software_design/glossary.md`
- `coding/software_design/software_design.md`
- `coding/software_design/strategic_tactical_design.md`
- `skills-plugins/brainstorm-vision/SKILL.md`
- `skills-plugins/create-vision-companion/SKILL.md`

The source set remained exactly the 33 authoritative planning files. The link audit did not expand into any outgoing link from these five targets.

## Final gate decision

All 14 acceptance checkboxes pass. F1–F4 and R1–R5 are closed, and no targeted fix envelope is required. The revised plan may advance from draft subject to the repository's normal human approval process.
