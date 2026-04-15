# Step 6-review — BMAD Adversarial Review of Risk Assessment

**Status:** [ ]

**Session rule:** Complete this review, write findings, mark `[x]`, then stop.

**Prerequisites:** Step 6 (risk assessment) must be complete.

---

## Goal

Apply BMAD's adversarial review to the consolidated risk assessment, checking for scoring inconsistencies, missing mitigations, and recommendations that don't match the actual risk landscape.

**Core rule:** You MUST find issues. No "looks good" allowed.

---

## Agent prompt

```
You are performing a BMAD adversarial review of a consolidated security risk
assessment for a hypervisor product family. The core rule: you MUST find issues.

Read the complete risk assessment:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\ (all files)

Also read the threat model it was derived from:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)

For each finding, rate severity (HIGH/MEDIUM/LOW) and categorize.

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
- [ ] Contains at least 5 findings with severity ratings.
- [ ] HIGH-severity findings are addressed in the risk assessment files or documented as accepted risks.

---

## Gate

```bash
test -s "06_risk_assessment/adversarial_review.md" && echo "PASS: file exists" || echo "FAIL: missing"
grep -c "HIGH\|MEDIUM\|LOW" 06_risk_assessment/adversarial_review.md  # Expect >= 5
```

**Human interaction:** Review adversarial findings (~15-20 min). Update risk scores and recommendations where legitimate issues are identified.
