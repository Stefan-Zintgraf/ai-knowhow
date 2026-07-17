# Authoring Evidence — Traceability Map (AUDIT-ONLY)

**Status:** Companion to the [skillset plan](./prod_discovery_requirements_skillset_plan.md). Extracted from that plan without changing any decision.

**What this is.** This file is the **audit/traceability companion** to the [Discovery–Definition–Requirements skillset plan](./prod_discovery_requirements_skillset_plan.md). It exists so a future *authoring* session can load a lean design spec (the plan) while every inline ledger-ID citation that proves the design conforms to the seven per-skill contribution ledgers survives here, reachable for **re-gating**.

**Who needs it.** The acceptance-gate / re-gating reviewer, *not* the authoring agent. Nothing here is required to build a skill; it is required to prove a built skill still satisfies its contribution ledgers. When re-gating, read a plan section, then read the same section below to see which ledger rows (and which linter checks / regression scenarios) that section realizes.

**How the split works.**
- The **plan** keeps everything an author needs to build: design prose, interfaces, guardrails, phases, the deterministic linter check *definitions* (`LNT-01`–`LNT-19`, §2.2), the regression scenario *table* (`RTS-01`–`RTS-13`, §6), the donor-audit task list and external-dependency policy (§3.2–§3.3), the artifact / ID / trace models, and the handover & re-entry contracts. Inline `LNT-xx` / `RTS-xx` wiring stays in the plan because it names the check or test an author must build.
- This **companion** holds the dense inline ledger-ID citations (`DP-*`, `DR-*`, `SR-*`, `VR-*`, `TL-*`, `BV-*`, `VC-*`, and the method-owned `-M##` / `-MTH-##` rows) that were stripped from the plan's prose, reconstructed as a **plan section → ledger IDs it realizes** map. The "Also wires" column notes the `LNT-*` / `RTS-*` each item connects to (those tokens also remain in the plan's tables).

**ID conservation.** The plan originally carried **181** unique ID tokens. The **133** ledger-family IDs are all captured below (each also, where protected, still visible in plan §3.2–§3.3). The remaining **48** — the 16 spine `#` families (`S# V# UC# BV# INV# CAP# ASM# EV# OPP# SOL# EXP# REL# REQ# QAS# DEC# BRV#`), `LNT-01`–`LNT-19`, and `RTS-01`–`RTS-13` — stay in the plan's design prose and tables. Union across both files = the original 181; nothing was lost.

---

## Plan §2 — Artifacts

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| `evidence-log.md` — observations, interview notes, analytics pointers, each dated with strength; strength uses the canonical Rich/Mixed/Thin rubric, and confidence is capped by source quality — the cap is overridable only by a cited `DEC#` | DP-008, DP-009, VR-EXT-08 | — |
| `opportunities.md` — opportunity map under the framed outcome, separate from solutions; every opportunity carries an explicit routing decision — add / merge / escalate / park — with provenance preserved on merge and reasons on park/escalate | DP-010 | — |
| `experiments/EXP<n>.md` — experiment cards following the complete experiment-card template of the method doc, merged with the spine: decision to inform, explicit assumption/hypothesis, target `ASM#`, applicable `SOL#`, evidence needed, method, time budget, predeclared support/refute/inconclusive criteria, result, confidence per relevant risk dimension, resulting `DEC#` | DP-007, DP-014, DP-020 | LNT-19 |
| `validation/REL<n>-review.md` — outcome vs. success/guardrail criteria; what to reopen; opens with the durable, timestamped **analysis plan** written before any result is inspected — post-hoc plan changes are dated `DEC#` entries with the original kept visible; metric-audit result, warnings, or justified skip from the `north-star` call land in its review metadata | DR-EXT-07, VR-EXT-01, VR-EXT-03 | LNT-17 |
| `SOL#` representation decision | DP-012, DP-013, DP-031 | — |
| Strategy representation decision | BV-M12, DP-M02, DR-M03, VC-M11 | LNT-01, LNT-02, LNT-04, LNT-05 |

*All ledger IDs realized by §2: BV-M12, DP-007, DP-008, DP-009, DP-010, DP-012, DP-013, DP-014, DP-020, DP-031, DP-M02, DR-EXT-07, DR-M03, VC-M11, VR-EXT-01, VR-EXT-03, VR-EXT-08*

## Plan §2.1 — Method-doc coverage

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Method doc: collaboration_and_decision_ownership.md | BV-M14, DP-M03, DR-M01, SR-M01, TL-M01, VR-M01 | RTS-07, RTS-10 |
| Method doc: product_vision.md | BV-M12, DP-M01, DP-M02, DR-M03, VC-M01, VC-M11, VR-M03 | RTS-11, RTS-13 |
| Ledger method-coverage rows binding the table (final paragraph) | BV-E10, BV-M01, DP-M01, DR-M01, DR-MTH-01, DR-MTH-09, SR-MTH-01, SR-MTH-08, VC-M01, VR-M01, VR-MTH-01, VR-MTH-03 | — |

*All ledger IDs realized by §2.1: BV-E10, BV-M01, BV-M12, BV-M14, DP-M01, DP-M02, DP-M03, DR-M01, DR-M03, DR-MTH-01, DR-MTH-09, SR-M01, SR-MTH-01, SR-MTH-08, TL-M01, VC-M01, VC-M11, VR-M01, VR-M03, VR-MTH-01, VR-MTH-03*

## Plan §2.2 — Deterministic workspace linter

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| LNT-15 | DR-EXT-05, DR-EXT-06 | LNT-15 |
| LNT-16 | SR-EXT-04 | LNT-16 |
| LNT-17 | VR-EXT-03 | LNT-17 |
| LNT-18 | DP-009, VR-EXT-08 | LNT-18 |
| LNT-19 | DP-007, DP-014 | LNT-03, LNT-07, LNT-19 |

*All ledger IDs realized by §2.2: DP-007, DP-009, DP-014, DR-EXT-05, DR-EXT-06, SR-EXT-04, VR-EXT-03, VR-EXT-08*

## Plan §3 — Skills overview

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| `prototype` | DP-020 | — |
| `domain-modeling` | DP-022 | — |
| `qa` / `triage` | VR-EXT-09 | — |
| `north-star` | DR-EXT-07, VR-EXT-01 | — |
| `quality-attribute-scenario-writer` | SR-EXT-05 | — |

*All ledger IDs realized by §3: DP-020, DP-022, DR-EXT-07, SR-EXT-05, VR-EXT-01, VR-EXT-09*

## Plan §3.1 — Callable specialists and internal call contracts

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| `north-star` | DR-EXT-07, VR-EXT-01 | — |
| `quality-attribute-scenario-writer` | SR-EXT-05, SR-EXT-07, SR-MTH-07 | — |
| `prototype` | DP-019, DP-020 | — |
| `domain-modeling` | DP-022 | — |
| `qa` / `triage` | VR-EXT-09 | — |
| Routing exclusions | BV-E09, BV-E11, VC-E13 | — |

*All ledger IDs realized by §3.1: BV-E09, BV-E11, DP-019, DP-020, DP-022, DR-EXT-07, SR-EXT-05, SR-EXT-07, SR-MTH-07, VC-E13, VR-EXT-01, VR-EXT-09*

## Plan §3.2 — External-dependency policy

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| `distill` — vendored content with full provenance | DP-001, DP-007, DP-012, DP-019, DR-EXT-01, SR-EXT-08 | — |
| `pattern` — local implementation, inspiration recorded | BV-E09, DP-026, TL-009, VC-E13 | — |
| No license-incompatible distillation | DP-012 | — |

*All ledger IDs realized by §3.2: BV-E09, DP-001, DP-007, DP-012, DP-019, DP-026, DR-EXT-01, SR-EXT-08, TL-009, VC-E13*

## Plan §3.3 — Plan-to-authoring traceability

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Traceability record | BV-E02, VC-E07 | — |
| Authoring-time donor-audit tasks — the 15 distill rows | DP-027, TL-010 | — |
| DP-001 | DP-001 | — |
| DP-002 | BV-E04, DP-002 | — |
| DP-003 | DP-003 | — |
| DP-004 | DP-004 | — |
| DP-005 | DP-005 | — |
| DP-006 | DP-006 | — |
| DP-007 | DP-007 | LNT-19 |
| DP-012 | DP-012 | — |
| DP-019 | DP-001, DP-007, DP-019 | — |
| DR-EXT-01 | DR-EXT-01 | — |
| DR-EXT-02 | DR-EXT-02 | — |
| DR-EXT-03 | DR-EXT-03 | — |
| DR-EXT-04 | DR-EXT-04 | — |
| DR-EXT-05 | DR-EXT-05 | — |
| SR-EXT-08 | DR-EXT-01, SR-EXT-08 | — |

*All ledger IDs realized by §3.3: BV-E02, BV-E04, DP-001, DP-002, DP-003, DP-004, DP-005, DP-006, DP-007, DP-012, DP-019, DP-027, DR-EXT-01, DR-EXT-02, DR-EXT-03, DR-EXT-04, DR-EXT-05, SR-EXT-08, TL-010, VC-E07*

## Plan §4.1 — Handover contract (skillset-wide)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Handover field 5 — Recorded skips | TL-013 | RTS-02 |
| Out-of-order execution — decided: refuse silent violations; warn-and-record legitimate recorded deviations | TL-013 | — |

*All ledger IDs realized by §4.1: TL-013*

## Plan §4.2 — Re-entry definition (skillset-wide)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Backtracking-conditions → routes table | VR-EXT-04 | — |
| Re-entry condition 7 — terminology/rule/ownership (domain-modeling call) | DP-022 | — |
| Tailoring re-entry | TL-005 | — |
| In-loop backtracking | BV-E08, DP-024, DR-EXT-12, SR-EXT-11, VC-E05 | — |

*All ledger IDs realized by §4.2: BV-E08, DP-022, DP-024, DR-EXT-12, SR-EXT-11, TL-005, VC-E05, VR-EXT-04*

## Plan §5.1 — `brainstorm-vision` (adjust)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Optional press-release stress test | BV-E01 | — |
| File-responsibility contract | BV-E02 | — |
| Handover UX | BV-E03, BV-E11 | — |
| Low-ceremony guarantee | BV-E05 | — |
| Human gate on scope; decision ownership | BV-E06, BV-M09, BV-M14 | RTS-07, RTS-08 |
| Durable-state rule | BV-E07 | — |
| Strategy section | BV-M01, BV-M12, VC-M11 | LNT-14 |
| Backtracking route table; vision-pivot gate | BV-E08, BV-M13 | RTS-11, RTS-12 |
| Provenance and dependency discipline | BV-E09, BV-E10, BV-E11 | — |

*All ledger IDs realized by §5.1: BV-E01, BV-E02, BV-E03, BV-E05, BV-E06, BV-E07, BV-E08, BV-E09, BV-E10, BV-E11, BV-M01, BV-M09, BV-M12, BV-M13, BV-M14, VC-M11*

## Plan §5.2 — `create-vision-companion` (adjust)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Expose discovery seeds | VC-E01, VC-E03 | — |
| Phase 9's mechanical gates run as the shared linter at finalize | VC-E04 | LNT-01, LNT-02, LNT-05, LNT-13 |
| Builder/critic independence gate | VC-E02, VC-E10 | — |
| Backtracking/re-entry matrix | VC-E05 | — |
| Durable status and human gate; vision-pivot gate | VC-E05, VC-E09, VC-M12 | LNT-02, RTS-11, RTS-12 |
| Strategy derivation and reserved fields | VC-M11 | LNT-02, LNT-04 |
| Handoff gate | VC-E08 | — |
| Schema and dependency guardrails | VC-E07, VC-E12, VC-E13, VC-E14 | — |

*All ledger IDs realized by §5.2: VC-E01, VC-E02, VC-E03, VC-E04, VC-E05, VC-E07, VC-E08, VC-E09, VC-E10, VC-E12, VC-E13, VC-E14, VC-M11, VC-M12*

## Plan §5.3 — `tailor-lifecycle` (new)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Mode | TL-002, TL-003 | — |
| Does | TL-011, TL-012 | — |
| Key behavior | TL-004, TL-013, TL-016 | — |
| Handover | TL-001, TL-013, TL-014 | — |
| Revisit trigger | TL-005 | — |
| Ownership gate — the seven-field decision-authority record | TL-005, TL-015, TL-M01, TL-M02 | LNT-05, RTS-07, RTS-08, RTS-09 |
| Provenance | TL-009, TL-010 | — |
| Finalize | TL-006, TL-007 | LNT-05, LNT-13, LNT-14, RTS-13 |
| Regression hooks | TL-008 | RTS-01, RTS-02, RTS-13 |

*All ledger IDs realized by §5.3: TL-001, TL-002, TL-003, TL-004, TL-005, TL-006, TL-007, TL-008, TL-009, TL-010, TL-011, TL-012, TL-013, TL-014, TL-015, TL-016, TL-M01, TL-M02*

## Plan §5.4 — `discover-product` (new)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Distilled technique base | DP-001, DP-003, DP-018, DP-019 | — |
| Evidence quality | DP-004, DP-005, DP-008, DP-009 | LNT-18 |
| Opportunity routing and the human gate | DP-010, DP-011 | — |
| Integrations | DP-015, DP-016, DP-020, DP-022 | LNT-04 |
| Guardrail | DP-028 | — |
| Guardrail — alternative-count refusal | DP-012 | RTS-04 |
| Guardrails — discipline | DP-021, DP-029, DP-030 | — |
| Experiment-card schema | DP-007, DP-014, DP-019, DP-020, DP-030 | LNT-03, LNT-07, LNT-19 |
| Wrap-up and backtracking | DP-017, DP-024 | — |
| Discovery-pivot vs. vision-pivot routing | DP-M01 | RTS-11, RTS-12 |
| Opportunity selection vs. strategy | DP-M02, VC-M11 | — |
| Decision ownership and specialist participation | DP-021, DP-028, DP-M03, DP-M04 | RTS-07, RTS-08 |
| Finalize runs the deterministic linter | DP-023, DP-025 | LNT-01, LNT-03, LNT-06, LNT-07, LNT-18, LNT-19 |

*All ledger IDs realized by §5.4: DP-001, DP-003, DP-004, DP-005, DP-007, DP-008, DP-009, DP-010, DP-011, DP-012, DP-014, DP-015, DP-016, DP-017, DP-018, DP-019, DP-020, DP-021, DP-022, DP-023, DP-024, DP-025, DP-028, DP-029, DP-030, DP-M01, DP-M02, DP-M03, DP-M04, VC-M11*

## Plan §5.5 — `define-release` (new)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Journey shaping and slice discipline | DR-EXT-01, DR-EXT-03 | — |
| Proportional ceremony | DR-EXT-02, DR-EXT-04 | — |
| Mandatory-scope classification | DR-EXT-06, SR-EXT-04 | LNT-15, LNT-16 |
| Hypothesis quality | DR-EXT-09 | LNT-08, LNT-17 |
| Metric audit | DR-EXT-07, DR-EXT-08 | — |
| Guardrails | DR-EXT-05 | — |
| Handover and backtracking | DR-EXT-11, DR-EXT-12, DR-M05 | RTS-11, RTS-12 |
| Opportunity selection vs. strategy | DR-M03, VC-M11 | — |
| Ceremony-gated roadmap maintenance | DR-M04 | LNT-14, RTS-13 |
| Decision-metadata ownership and specialist participation | DR-M01, DR-M02 | LNT-15, RTS-07, RTS-08 |

*All ledger IDs realized by §5.5: DR-EXT-01, DR-EXT-02, DR-EXT-03, DR-EXT-04, DR-EXT-05, DR-EXT-06, DR-EXT-07, DR-EXT-08, DR-EXT-09, DR-EXT-11, DR-EXT-12, DR-M01, DR-M02, DR-M03, DR-M04, DR-M05, SR-EXT-04, VC-M11*

## Plan §5.6 — `specify-requirements` (new)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Fresh-critic protocol | SR-EXT-01 | — |
| Durable-workspace discipline | SR-EXT-02 | LNT-04 |
| Slice boundary contract | SR-EXT-08 | LNT-16 |
| Trace rationale | SR-EXT-03, SR-EXT-04 | LNT-16 |
| QAS elicitation and gate | SR-EXT-05, SR-EXT-06, SR-EXT-07 | — |
| Integrations | DP-022 | — |
| Handover and backtracking | SR-EXT-10, SR-EXT-11 | — |
| Singular accountable ownership and specialist verdicts | SR-M01, SR-M04 | LNT-05, RTS-07, RTS-08, RTS-10 |

*All ledger IDs realized by §5.6: DP-022, SR-EXT-01, SR-EXT-02, SR-EXT-03, SR-EXT-04, SR-EXT-05, SR-EXT-06, SR-EXT-07, SR-EXT-08, SR-EXT-10, SR-EXT-11, SR-M01, SR-M04*

## Plan §5.7 — `validate-release` (new)

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| Analysis-planning gate | VR-EXT-03 | LNT-17 |
| Does | VR-EXT-08, VR-EXT-09 | LNT-18 |
| Metric audit | VR-EXT-01, VR-EXT-02 | — |
| Context-separated verifier | VR-EXT-06 | — |
| Re-entry matrix and handover | DP-022, VR-EXT-04, VR-EXT-05 | — |
| Vision-stability escalation guard | VR-M03 | RTS-11, RTS-12 |
| Review and re-entry ownership; specialist evidence | VR-EXT-09, VR-M01, VR-M02, VR-M04 | RTS-07, RTS-08, RTS-09, RTS-10 |
| Runs the deterministic linter before routing findings | VR-EXT-07 | LNT-01, LNT-03, LNT-05, LNT-09, LNT-17, LNT-18 |

*All ledger IDs realized by §5.7: DP-022, VR-EXT-01, VR-EXT-02, VR-EXT-03, VR-EXT-04, VR-EXT-05, VR-EXT-06, VR-EXT-07, VR-EXT-08, VR-EXT-09, VR-M01, VR-M02, VR-M03, VR-M04*

## Plan §6 — Skillset regression validation

| Plan item | Ledger IDs it realizes | Also wires (LNT / RTS) |
| --- | --- | --- |
| RTS-03 | DP-008, DP-009, VR-EXT-08 | LNT-06, LNT-18, RTS-03 |
| Per-skill fixture obligations feed the suite | DP-025, TL-008, VC-E06, VC-E14, VR-EXT-06 | — |

*All ledger IDs realized by §6: DP-008, DP-009, DP-025, TL-008, VC-E06, VC-E14, VR-EXT-06, VR-EXT-08*
