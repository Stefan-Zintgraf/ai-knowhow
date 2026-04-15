# Step 6-review — BMAD Adversarial Review of Risk Assessment

**Status:** [ ]

**Session rule:** Complete this review, write findings, mark `[x]`, then stop.

**Prerequisites:** Step 6 (risk assessment) must be complete.

---

## Goal

Apply BMAD's adversarial review to the consolidated risk assessment, checking for scoring inconsistencies, missing mitigations, and recommendations that don't match the actual risk landscape.

**Core rule:** The review must be adversarial and evidence-seeking. Start by assuming the register has inconsistencies, but do not invent findings to satisfy a quota. If no material gaps remain, document what was checked and why.

---

## Agent prompt

```
You are performing a BMAD adversarial review of a consolidated security risk
assessment for a hypervisor product family. Default to a skeptical stance and look
for inconsistencies, but do not manufacture findings. If a focus area appears sound,
document what you checked and why it is sufficient.

Read the complete risk assessment:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\ (all files)

Also read the threat model it was derived from:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)

For each finding, rate severity (HIGH/MEDIUM/LOW) and categorize.

If you do not find any material gaps after checking the focus areas below, add an
explicit conclusion section describing what you checked and why the risk assessment
is adequate as written.

Focus your adversarial review on:
- Scoring consistency: Are similar threats scored differently?
- Missing threats: Are there STRIDE or Threagile findings not in the register?
- Mitigation gaps: Do recommendations address the root cause?
- Product coverage: Are all 7 products covered proportionally?
- Prioritization bias: Are effort classifications accurate?
- CRA compliance: Would a notified body find this sufficient for Important Class 2?
- Actionability: Can a developer implement each recommendation?

Write findings to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\adversarial_review.md
```

---

## Output file

- `06_risk_assessment\adversarial_review.md`

---

## Verifiable result

- [ ] `adversarial_review.md` exists and is non-empty.
- [ ] Each finding has a severity rating and a concrete corrective action.
- [ ] If no HIGH/MEDIUM findings remain, the review explicitly documents coverage across the listed focus areas and explains why no material gaps were found.
- [ ] HIGH-severity findings are addressed in the risk assessment files or documented as accepted risks.

---

## Gate

Verify that:
- `06_risk_assessment\adversarial_review.md` exists and is non-empty.
- Every finding includes severity and a concrete corrective action.
- If no material findings remain, the review records the focus areas checked and the rationale for that conclusion.

**Human interaction:** Review adversarial findings (~15-20 min). Update risk scores and recommendations where legitimate issues are identified.
