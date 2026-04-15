# Step 5-review — BMAD Adversarial Review of Threat Model

**Status:** [ ]

**Session rule:** Complete this review, write findings, mark `[x]`, then stop.

**Prerequisites:** Step 5 (STRIDE threat model) must be complete.

---

## Goal

Apply BMAD's adversarial review technique to the STRIDE threat model output, forcing a second-pass thoroughness check that catches blind spots and gaps.

**Core rule:** The review must be adversarial and evidence-seeking. Start from the assumption that the threat model has gaps, but do not invent findings to satisfy a quota. If no material gaps remain, document what was stress-tested and why.

---

## Agent prompt

```
You are performing a BMAD adversarial review of a STRIDE threat model for a
hypervisor system. Default to a cynical stance and actively look for gaps, but do
not manufacture findings. If a focus area appears complete, state what you checked
and why it is sufficient.

Read the complete threat model:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)

Also read the EN standard threat catalogs for cross-reference:
- EN 304 635 §4.4.2 (Hypervisor threats): EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
- EN 304 626 Annex C.4 (OS threats): EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf

For each finding, rate severity (HIGH/MEDIUM/LOW) and provide:
1. What is missing or wrong
2. Why it matters for a CRA Important Class 2 product
3. Specific recommendation to fix it

If you do not find any material gaps after checking the focus areas below, add an
explicit conclusion section describing what you checked and why the threat model is
adequate as written.

Focus your adversarial review on:
- Missing threat scenarios (what attack vectors are NOT modeled?)
- EN standard threats (§4.4.2 / TH-*) that have no STRIDE mapping
- Inconsistent severity ratings
- Missing attack trees for High/Critical threats
- Threats that assume mitigations exist but don't cite evidence
- Multi-hop attack paths that cross multiple trust boundaries
- Supply chain and build integrity gaps

Write findings to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\adversarial_review.md
```

---

## Output file

- `05_threat_model\adversarial_review.md`

---

## Verifiable result

- [ ] `adversarial_review.md` exists and is non-empty.
- [ ] Each finding has severity rating (HIGH/MEDIUM/LOW) and recommendation.
- [ ] If no HIGH/MEDIUM findings remain, the review explicitly documents coverage across the listed focus areas and explains why no material gaps were found.
- [ ] HIGH-severity findings are addressed: either incorporated into Step 5 threat files or documented as accepted risks with rationale.

---

## Gate

Verify that:
- `05_threat_model\adversarial_review.md` exists and is non-empty.
- Every finding includes severity and a concrete recommendation.
- If no material findings remain, the review records the focus areas checked and the rationale for that conclusion.

**Human interaction:** Review adversarial findings (~15-20 min). Dismiss noise, incorporate valid findings back into threat model files before proceeding to Step 5b.
