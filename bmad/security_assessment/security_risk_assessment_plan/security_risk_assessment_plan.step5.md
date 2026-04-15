# Step 5 — STRIDE Threat Modeling

**Status:** [ ]

**Session rule:** Complete this step, run the gate, mark `[x]`, then stop. After this step, run Step 5-review in a **fresh** session.

**Prerequisites:** Steps 3 (component docs) and 4 (interface map) must be complete.

---

## Goal

Perform systematic STRIDE threat analysis for each interface and component, producing a categorized threat catalog. Uses the structure from **Fabric's `create_threat_model` pattern**. Output also prepares input for Threagile (Step 5b).

---

## Input

- Interface map from Step 4: `04_interface_map\*.md`
- Component documentation from Step 3: `03_component_documentation\*.md`
- Artifact registry from Step 1: `01_artifact_registry\*.md`

## STRIDE Framework

| STRIDE Category | Question to Ask |
|---|---|
| **S**poofing | Can an attacker impersonate a legitimate component, user, or guest VM? |
| **T**ampering | Can data in transit or at rest be modified (VMF calls, shared memory, configs)? |
| **R**epudiation | Can actions be performed without attribution/logging? |
| **I**nformation Disclosure | Can sensitive data leak across trust boundaries? |
| **D**enial of Service | Can availability be impacted (resource exhaustion, driver crashes)? |
| **E**levation of Privilege | Can guest code gain host privileges, or user-mode gain kernel-mode? |

### Hypervisor-specific focus areas

- **VM escape** (guest-to-host privilege escalation via VMF, virtio, IVSHMEM)
- **Driver vulnerabilities** (kernel-mode code reachable from user-mode IOCTLs)
- **Web management surface** (HvWeb authentication, injection, CSRF)
- **Supply chain** (build process integrity, third-party components, code signing)
- **Shared memory** (IVSHMEM data integrity, race conditions, bounds checking)

## Required structure per threat model file (Fabric `create_threat_model`)

Each output file must contain:
1. **System Description** — Component/boundary being modeled
2. **Assets** — Valuable assets handled or protected
3. **Trust Boundaries** — Relevant boundaries with trust levels
4. **Threat Analysis (STRIDE)** — For each category, enumerate threats with:
   - `T-XXX-NNN`: Threat title
   - Scenario, affected component(s), affected interface(s)
   - Likelihood (Low/Medium/High), Impact (Low/Medium/High/Critical)
   - Existing controls, recommended mitigation
   - **EN reference:** EN 304 635 §4.4.2.x or EN 304 626 TH-xxxx or "No direct EN mapping"
5. **Attack Tree Summary** — For each High/Critical threat
6. **Harmonised Standard Threat Cross-Reference** — Coverage matrix against EN catalogs

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\`:

- `index.md` — STRIDE summary matrix, EN threat coverage matrix, overall risk landscape
- `threat_model_vmf_core.md`
- `threat_model_drivers.md`
- `threat_model_network.md`
- `threat_model_web.md`
- `threat_model_guest_escape.md`
- `threat_model_supply_chain.md`
- `threat_model_deployment.md`

---

## Agent prompt

```
You are a security threat modeler specializing in hypervisor and virtualization systems.
Follow the structured threat modeling approach below (based on Fabric's create_threat_model
pattern, adapted for hypervisor systems).

Read these analysis documents:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\01_artifact_registry\ (all files)

For each threat model file, use the structure defined in the step file
(security_risk_assessment_plan.step5.md): System Description, Assets, Trust Boundaries,
STRIDE Threat Analysis (with EN standard cross-references), Attack Tree Summary.

Include in index.md a coverage matrix showing:
- Which EN 304 635 §4.4.2 threats are covered by identified STRIDE threats
- Which EN 304 626 Annex C.4 threats (TH-*) are covered
- Any EN threats NOT covered (gaps to investigate)

Read the EN standard threat catalogs:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

---

## Verifiable result

- [ ] All 8 output files exist under `05_threat_model\` and are non-empty.
- [ ] Each threat file follows the required structure (System Description, Assets, Trust Boundaries, STRIDE, Attack Trees).
- [ ] Each threat entry has an EN standard cross-reference line.
- [ ] `index.md` contains an EN threat coverage matrix (EN 304 635 + EN 304 626 threats mapped).
- [ ] High/Critical threats have attack tree summaries.

---

## Gate

```bash
cd 05_threat_model
for f in index.md threat_model_vmf_core.md threat_model_drivers.md threat_model_network.md threat_model_web.md threat_model_guest_escape.md threat_model_supply_chain.md threat_model_deployment.md; do
  test -s "$f" && echo "PASS: $f" || echo "FAIL: $f"
done

# Verify STRIDE structure
grep -c "^### " threat_model_vmf_core.md  # Expect >= 6 (one per STRIDE category)

# Verify EN cross-reference
grep -qi "EN reference\|EN 304" threat_model_vmf_core.md && echo "PASS: EN refs" || echo "FAIL: no EN refs"

# Verify coverage matrix in index
grep -qi "coverage\|matrix\|gap" index.md && echo "PASS: coverage matrix" || echo "FAIL: no coverage matrix"
```

**Human interaction:** None for generation. Run Step 5-review (adversarial review) in a fresh session afterward.
