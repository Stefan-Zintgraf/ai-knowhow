You are continuing work on the security risk assessment for the acontis hypervisor product family.

## Session protocol

1. Read these files in order:
   - `bmad/security_assessment/security_risk_assessment_plan/security_risk_assessment_plan.md` (overview — find which step is next by looking at the Status column: the first `[ ]` is your step)
   - The step file for that step (e.g. `security_risk_assessment_plan.step1.md`)
   - `bmad/security_assessment/security_risk_assessment_plan/security_risk_assessment_strategy.md` (strategy reference)
2. Inspect the output directory structure under `bmad/security_assessment/` to confirm which prior steps have produced output and the workspace is ready.
3. Implement **only** the current step. Run its gate (verify output files exist and are non-empty, check file structure). Mark `[x]` in both the step file's Status and the overview's Status table. Then **stop**.

## Constraints

- All analysis outputs go under `bmad/security_assessment/` in the designated output subdirectory (e.g. `01_artifact_registry/`, `02_product_artifact_map/`, etc.) — NOT under the plan folder.
- The plan folder (`security_risk_assessment_plan/`) contains only planning documents (this prompt, the overview, step files). Do not write analysis output there.
- Do not proceed to the next step.
- Do not skip the gate verification.
- If something is unclear or blocked, stop and ask rather than guessing.
- **IMPORTANT:** Ignore all folders named `brainstormingPlatform` or `brainstormingPlatformPlus` in every analysis step.

## Workspace

- Repository root: `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow`
- Plan documents (read-only unless updating status checkboxes): `bmad/security_assessment/security_risk_assessment_plan/`
- Analysis output root: `bmad/security_assessment/`
- Source code repositories:
  - `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram` (build scripts)
  - `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv` (source code, docs, SDK)
- Harmonised standard PDFs: `bmad/security_assessment/EN-304-*.pdf`
- QuBA-libre reference: `bmad/security_assessment/QuBA-libre/`

## Context

- **All** acontis hypervisor products are CRA **Important Class 2** (mandatory notified body assessment).
- Full assessment for **RTOSVisor** (Type I) + **LxWin** (Type II representative). Delta assessment for other Type II products.
- Applicable harmonised standards: **EN 304 635** (Virtualisation/Container) for hypervisor/M&O. **EN 304 626** (Operating Systems) for Linux host OS layer.
- Trust boundaries: Guest VM ↔ VMF Core (VMF calls), Kernel ↔ User-mode (IOCTLs), Host ↔ Network (RtosVnet, IVSHMEM, MQTT, virtio), Web Client ↔ HvWeb (REST/WebSocket), Build system ↔ Deployed artifacts (signing).
- Risk register format: **QuBA-libre** (not AT3350 FMEA).
