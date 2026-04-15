# Step 6 — Risk Assessment and Recommendations

**Status:** [ ]

**Session rule:** Complete this step, run the gate, mark `[x]`, then stop. After this step, run Step 6-review in a **fresh** session.

**Prerequisites:** Steps 2 (product map), 5 (STRIDE), and 5b (Threagile) must be complete.

---

## Goal

Consolidate all findings — STRIDE threat model (Step 5) and Threagile automated analysis (Step 5b) — into a unified, scored risk register with prioritized remediation recommendations.

---

## Input

- STRIDE threat model from Step 5: `05_threat_model\*.md`
- Threagile output from Step 5b: `05b_threagile\output\risks.json` and `threagile_report.md`
- Product-artifact map from Step 2: `02_product_artifact_map\*.md`

## Risk Scoring

**Risk = Likelihood × Impact**

| | Impact: Low (1) | Impact: Medium (2) | Impact: High (3) | Impact: Critical (4) |
|---|---|---|---|---|
| **Likelihood: High (3)** | 3 | 6 | 9 | 12 |
| **Likelihood: Medium (2)** | 2 | 4 | 6 | 8 |
| **Likelihood: Low (1)** | 1 | 2 | 3 | 4 |

Risk levels: **Critical** (9-12), **High** (6-8), **Medium** (4-5), **Low** (1-3)

## Tasks

1. Merge findings from STRIDE and Threagile. De-duplicate; note agreement/disagreement on severity.
2. Score each threat: Risk = Likelihood × Impact.
3. Cross-reference STRIDE threat IDs with Threagile risk IDs — note coverage gaps.
4. Aggregate per-product risk profiles using the product-artifact map.
5. Identify top-10 highest-risk items.
6. Produce prioritized recommendations grouped by effort:
   - **Quick wins** (configuration changes, input validation)
   - **Medium effort** (code changes, additional authentication)
   - **Major effort** (architectural changes, redesign)

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\`:

- `index.md` — Executive summary (total threats, counts by level, top-5, STRIDE vs Threagile comparison)
- `risk_matrix.md` — Full scored register sorted by score descending
- `per_product_risk.md` — Risk profile per product
- `recommendations.md` — Prioritized remediation actions

---

## Agent prompt

```
You are a security risk analyst producing the final risk assessment for the
acontis hypervisor product family. You are merging findings from two sources:
AI-driven STRIDE analysis and automated Threagile analysis.

Read ALL of these inputs:

STRIDE threat model (agent-generated):
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)

Threagile automated analysis:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\threagile_report.md
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\output\risks.json (if exists)

Product-artifact mapping:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\02_product_artifact_map\ (all files)

Merge and de-duplicate findings. For each threat:
1. Score: Risk = Likelihood (1-3) × Impact (1-4)
2. Map to affected product(s)
3. Identify existing mitigations vs. gaps
4. Note source(s): STRIDE-only, Threagile-only, or both

Produce 4 output files as defined in step file (security_risk_assessment_plan.step6.md).

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\
```

---

## Verifiable result

- [ ] All 4 output files exist under `06_risk_assessment\` and are non-empty.
- [ ] `risk_matrix.md` contains a scored register with columns: Threat ID, Source, Category, Description, Component, Product(s), Likelihood, Impact, Risk Score, Risk Level, Existing Mitigation, Gap.
- [ ] `index.md` includes STRIDE vs Threagile coverage comparison.
- [ ] `recommendations.md` groups actions by effort level (Quick/Medium/Major).
- [ ] Each recommendation references specific threat IDs.

---

## Gate

```bash
cd 06_risk_assessment
for f in index.md risk_matrix.md per_product_risk.md recommendations.md; do
  test -s "$f" && echo "PASS: $f" || echo "FAIL: $f"
done

# Verify scored register structure
grep -c "|" risk_matrix.md  # Expect many table rows (risk entries)

# Verify recommendations reference threat IDs
grep -qi "T-\|threat" recommendations.md && echo "PASS: threat refs" || echo "FAIL: no threat refs"
```

**Human interaction:** None for generation. Run Step 6-review next.
