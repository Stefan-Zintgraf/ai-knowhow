# Step 8 — Compliance Consolidation (QuBA-libre + EN Standard Matrices)

**Status:** [ ]

**Session rule:** Due to scope, this step may require 2 sessions: one for Parts A+B, one for Part C. Run the gate after both are done, mark `[x]`, then stop.

**Prerequisites:** Steps 2, 3, 4, 5, 5-review, 5b, 6, 6-review, 7a, and 7b must be complete. Step 7c is optional and is included only if it was actually performed.

---

## Goal

Transform the technical findings from Steps 1-7 into formal risk assessment documents suitable for CRA compliance and review by a notified body. Produce the bridge between deep technical investigation and structured risk register formats.

### Assessment format rationale

- **RTOSVisor (Type I)** → **QuBA-libre** (full assessment, mandatory for Important Class 2)
- **LxWin (Type II representative)** → **QuBA-libre** (full assessment, representative for all Type II)
- **Other Type II products** → **Delta assessment** referencing LxWin findings

### Why QuBA-libre (not AT3350)

AT3350 FMEA format is insufficient for the hypervisor products because it lacks:
1. Structured trust boundary analysis (hypervisor spans kernel drivers, user-mode, web UI, shared memory, virtio, MQTT)
2. CRA Annex I traceability (mandatory for notified body review)
3. Systematic countermeasure catalog (mapped to IEC 62443/ETSI EN 303 645)
4. Assumption management (customer deployment constraints)
5. Scale (200+ risk entries vs. ~30 for EC-Master)

---

## Input

- Risk register from Step 6: `06_risk_assessment\*.md`
- Threagile risk data from Step 5b: `05b_threagile\output\risks.json`
- Semgrep findings from Step 7: `07_semgrep\*.md`
- Optional code-level findings from Step 7c (if performed): appended to `05_threat_model\*.md`
- Component docs from Step 3: `03_component_documentation\*.md` (§10 EN mapping)
- Interface map from Step 4: `04_interface_map\*.md`
- QuBA-libre reference: `security_assessment\QuBA-libre\QuBA-libre_analyzation.md`
- EN 304 635 and EN 304 626 PDFs

## Part A: Hypervisor QuBA-libre Consolidation

1. **Questionnaire answer recommendations** (`hypervisor_quba_inputs.md`): For each QI1-QI16 and QA1-QA21, derive answers from findings with rationale.
2. **Hypervisor-specific attack step extensions** (`hypervisor_attack_steps.md`): 15-25 additional attack steps (VMF exploitation, driver IOCTL abuse, IVSHMEM, HvWeb, guest escape, MQTT, installer, kernel modules) with RAP factors and CRA Annex I mapping.
3. **Countermeasure catalog extensions** (`hypervisor_countermeasures.md`): Per Critical/High risk, countermeasures with IEC 62443/ETSI mapping, RAP reduction, implementation status.
4. **Deployment assumptions** (`hypervisor_assumptions.md`): Security assumptions with stakeholder assignments (acontis/OEM/end-user).
5. **CRA Annex I gap analysis** (`cra_annex_i_checklist.md`): Walk through items (a)-(m), flag gaps.

## Part A2: LxWin QuBA-libre Consolidation

6. **LxWin-specific questionnaire answers** (`lxwin_quba_inputs.md`): Reuse shared findings; document Type II differences (Windows host, no HvWeb, EN 304 635 §4.4.2.2 threats).

## Part B: Type II Product Delta Assessments

7. **Delta assessments** (`type2_product_deltas.md`): Per-product differences from LxWin baseline (VxWin/CeWin/VmfWin/RTOS32Win/EC-WinRTOS-32).

## Part C: Harmonised Standard Compliance Matrices

8. **EN 304 635 compliance matrix** (`en304_635_compliance.md`): §5.1.1 + §5.1.3 requirement compliance per row.
9. **EN 304 635 assessment cases** (`en304_635_assessment_cases.md`): ~70 AC-H-* cases with evidence mapping.
10. **EN 304 626 compliance matrix** (`en304_626_compliance.md`): §5.2 TR-* requirement compliance.
11. **EN 304 626 risk factors** (`en304_626_risk_factors.md`): 18 RF-* scores + security profile.
12. **EN 304 635 risk factors** (`en304_635_risk_factors.md`): Annex B risk methodology + SCL determination.

---

## Agent prompt (Parts A+B)

```
You are a CRA compliance specialist consolidating security findings into formal
risk register formats for the acontis hypervisor product family.

Read:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\QuBA-libre\QuBA-libre_analyzation.md
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\index.md
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\02_product_artifact_map\ (all files)

ALL acontis hypervisor products are CRA Important Class 2.
Full QuBA-libre assessments for RTOSVisor + LxWin (representative Type II).
Delta assessments for other Type II products.

Produce output files 1-8 as defined in the step file (security_risk_assessment_plan.step8.md),
Parts A, A2, and B.

Write to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\08_compliance_consolidation\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

## Agent prompt (Part C)

```
You are a CRA compliance specialist producing harmonised standard compliance evidence
for the acontis hypervisor product family.

Read:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\index.md

Read the harmonised standard PDFs:
- EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
  (§5.1.1, §5.1.3, §6.3.1, §4.7, Annex B)
- EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf
  (§5.2, Annex C.2, C.4, C.6)

Produce output files 8-12 as defined in the step file (security_risk_assessment_plan.step8.md),
Part C.

Write to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\08_compliance_consolidation\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\08_compliance_consolidation\`:

| # | File | Part |
|---|---|---|
| 1 | `index.md` | Strategy, format rationale, EN overview |
| 2 | `hypervisor_quba_inputs.md` | A |
| 3 | `hypervisor_attack_steps.md` | A |
| 4 | `hypervisor_countermeasures.md` | A |
| 5 | `hypervisor_assumptions.md` | A |
| 6 | `lxwin_quba_inputs.md` | A2 |
| 7 | `type2_product_deltas.md` | B |
| 8 | `cra_annex_i_checklist.md` | B |
| 9 | `en304_635_compliance.md` | C |
| 10 | `en304_635_assessment_cases.md` | C |
| 11 | `en304_626_compliance.md` | C |
| 12 | `en304_626_risk_factors.md` | C |
| 13 | `en304_635_risk_factors.md` | C |

---

## Verifiable result

- [ ] All 13 output files exist under `08_compliance_consolidation\` and are non-empty.
- [ ] `hypervisor_quba_inputs.md` covers QI1-QI16 and QA1-QA21 with rationale.
- [ ] `hypervisor_attack_steps.md` defines 15-25 hypervisor-specific attack steps with RAP factors.
- [ ] `en304_635_compliance.md` covers all §5.1.1 and §5.1.3 requirements.
- [ ] `en304_635_assessment_cases.md` covers ~70 AC-H-* assessment cases.
- [ ] `en304_626_compliance.md` covers all TR-* requirements.
- [ ] `cra_annex_i_checklist.md` covers items (a) through (m).

---

## Gate

Verify that:
- All 13 output files listed in the table above exist under `08_compliance_consolidation\` and are non-empty.
- `cra_annex_i_checklist.md` covers CRA Annex I items (a) through (m).
- `hypervisor_quba_inputs.md` addresses QI1-QI16 and QA1-QA21.
- `en304_635_compliance.md` covers §5.1.1 and §5.1.3 requirements.
- `en304_626_compliance.md` covers all TR-* requirements.

**Human interaction:** Review QuBA-libre inputs before manually entering into the Excel workbook. The agent produces recommended answers and rationale — a human transfers these into the actual Excel file and verifies automated risk calculations. This is the primary human touchpoint in the entire plan.
