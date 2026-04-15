# Security Risk Assessment Plan for the acontis Hypervisor Product Family

## Purpose

Execute a comprehensive, AI-agent-driven security risk assessment of the acontis hypervisor product family. The goal is to generate structured markdown documentation that:

1. Catalogs all binary artifacts produced by the automated build process
2. Maps artifacts to the products they ship in
3. Documents inter-component interfaces and attack surfaces
4. Describes internal details of each artifact (linked to source code)
5. Performs a systematic security risk assessment per component and per product
6. Consolidates findings into formal CRA compliance documentation (QuBA-libre format)

This plan is an execution contract alongside:

- [Strategy](security_risk_assessment_strategy.md) — high-level assessment strategy and rationale
- [QuBA-libre Analysis](../QuBA-libre/QuBA-libre_analyzation.md) — QuBA-libre methodology reference

### Session rule

Each step is implemented in its own fresh session when doing implementation work (one step = one conversation).

- On entry: read this overview, the strategy doc, and the current step file. Inspect the output directory to know what is already done.
- On completion: run that step's gate, verify the output files exist and are non-empty, mark the checkbox, then stop.

Planning artifacts in this folder may be edited in one session; implementation still follows the session rule per step.

---

## External Tools Used

| Tool | Purpose in This Plan | Installation |
|---|---|---|
| **BMAD Method** | Baseline project documentation (`document-project` workflow), custom security agent with persistent CRA/EN context, and adversarial review for threat model / risk assessment validation. Used in Steps 0a/0b and as validation passes after Steps 5 and 6 | `npx bmad-method install` |
| **Fabric** (Daniel Miessler) | Curated prompt patterns (`create_threat_model`, `find_vulnerabilities`, `extract_architecture`) used as structured templates for agent prompts in Steps 3 and 5 | `go install github.com/danielmiessler/fabric@latest` |
| **Threagile** | Threat-modeling-as-code: generates risk assessments and architectural threat diagrams from a YAML model. Used in Step 5b | `docker pull threagile/threagile` |
| **Semgrep** | Static analysis (SAST) with custom rules targeting trust boundaries. Used in Steps 7a-7b | `pip install semgrep` |

**Data privacy note:** Fabric by default sends content to a cloud LLM API. For proprietary source code, either (a) configure Fabric with a local model via Ollama, or (b) only pipe the *generated markdown descriptions* through Fabric patterns, never raw source. The agent prompts in this plan use Fabric's pattern structures inline, so running the Fabric CLI is optional.

---

## Harmonised Standards Reference (CRA Vertical Standards)

The EU Cyber Resilience Act mandates conformity with essential cybersecurity requirements. **Harmonised European Standards** (hEN) provide a voluntary means of demonstrating conformity.

| Standard | Title | Status | Applies To |
|---|---|---|---|
| **ETSI EN 304 626** V0.1.0 (2025-12) | Cybersecurity requirements for Operating Systems (OS) | Interim mature draft; target H2 2026 | **Linux host OS layer**, **RTOSVisor host OS** scheduling/memory/process management |
| **ETSI EN 304 635** V0.0.10 (2025-12) | Cybersecurity requirements for Virtualisation Execution Stack (VES) and Container Execution Stack (CES) | Interim mature draft; target H2 2026 | **Hypervisor (RTOSVisor)** product, **HvWeb** management/orchestration system |

**Location:**
```
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\
├── EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf
└── EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
```

### Why Both Standards Apply

The acontis hypervisor is a **Type I or Type II hypervisor** (EN 304 635 §4.1.2.2) that includes an **operating system layer** (the Linux host). EN 304 635 §4.6.3 explicitly references other harmonised standards (including EN 304 626) for security functions provided by the host OS.

### Product-to-Standard Mapping

| Product / Component | EN 304 635 (VES) | EN 304 626 (OS) | Notes |
|---|---|---|---|
| **RTOSVisor (Type I Hypervisor)** | **Primary** — §5.1.1, §6.3.1, §4.4.2.1 | **Secondary** — for Linux host OS layer | Both standards apply |
| **LxWin (Type II Hypervisor, representative)** | **Primary** — §5.1.1, §4.4.2.2 | **Secondary** — EN 304 626 applies to Windows host OS | Representative for all Type II |
| **Other Type II products** (VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32) | **Primary** — same as LxWin | Same as LxWin | Covered by LxWin assessment for shared components |
| **HvWeb (management UI)** | **Primary** — §5.1.3 | N/A | M&O system requirements (RTOSVisor only) |
| **VMF Core (Framework)** | **Primary** — §5.1.1.1, §5.1.1.2 | N/A | Core isolation and integrity |

---

## Repositories Under Analysis

| Repository | Path | Purpose |
|---|---|---|
| **buildprogram** | `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram` | Batch-driven build orchestration, product definitions, installer generation |
| **rtv** | `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv` | All source code, documentation, SDK headers, WiX installer definitions, framework |

### Excluded Folders

All folders named `brainstormingPlatform` or `brainstormingPlatformPlus` must be ignored in every step.

---

## Products Identified

| Product | Hypervisor Type | Source Root | Platform |
|---|---|---|---|
| **Hypervisor (RTOSVisor)** | **Type I** | `rtv\Hypervisor\`, `rtv\Linux\` | Linux host + guests |
| **LxWin** | **Type II** | `rtv\LxWin\` | RT-Linux guest on Windows |
| VxWin | Type II | `rtv\VxWin\` | VxWorks guest on Windows |
| CeWin | Type II | `rtv\CeWin\` | Windows CE guest on Windows |
| VmfWin | Type II | `rtv\Framework\`, `rtv\Windows\` | VMF standalone on Windows |
| RTOS32Win | Type II | `rtv\RTOS32Win\`, `rtv\Common\Rt32\` | RTOS-32 guest on Windows |
| EC-WinRTOS-32 | Type II | `rtv\EC-WinRTOS-32\` | EtherCAT + RTOS-32 on Windows |

**Assessment scope:** Full assessment for RTOSVisor + LxWin (representative Type II). Delta assessment for remaining Type II products.

### CRA Classification

**All acontis hypervisor products** = **Important Class 2** (CRA Annex III: "hypervisors and container runtime systems that support virtualised execution of operating systems"). Mandatory third-party assessment by a notified body.

### Assessment Format: QuBA-libre (Not AT3350)

The AT3350 FMEA format used for EC-Master is insufficient for the hypervisor products due to missing trust boundary analysis, no CRA Annex I traceability, no systematic countermeasure catalog, no assumption management, and scale (200+ risk entries). See [Step 8](security_risk_assessment_plan.step8.md) for the consolidation into QuBA-libre format.

---

## Output Directory Structure

All generated artifacts are written under:
```
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\
├── 01_artifact_registry\        # Step 1 output
├── 02_product_artifact_map\     # Step 2 output
├── 03_component_documentation\  # Step 3 output
├── 04_interface_map\            # Step 4 output
├── 05_threat_model\             # Step 5 + 5-review output
├── 05b_threagile\               # Step 5b output
├── 06_risk_assessment\          # Step 6 + 6-review output
├── 07_semgrep\                  # Steps 7a, 7b output
├── 08_compliance_consolidation\ # Step 8 output
└── 00_plan_execution_log.md     # Execution tracking
```

---

## Execution Order

| Step | File | Focus | Gate | Status |
|------|------|-------|------|--------|
| 0a | [step0a](security_risk_assessment_plan.step0a.md) | BMAD `document-project` baseline for `rtv` | `_bmad-output\index.md` exists with architecture + deep-dives | [ ] |
| 0b | [step0b](security_risk_assessment_plan.step0b.md) | Create custom BMAD security-assessment agent | `.customize.yaml` in agents config, agent compiles | [ ] |
| 1 | [step1](security_risk_assessment_plan.step1.md) | Extract artifact registry from build scripts | All 4 output files exist, non-empty, artifact counts documented | [ ] |
| 2 | [step2](security_risk_assessment_plan.step2.md) | Map artifacts to products | Cross-reference matrix + per-product files exist | [ ] |
| 3 | [step3](security_risk_assessment_plan.step3.md) | Document components (security overlay on BMAD baseline) | All component docs have §1-§10 sections, EN requirement mapping | [ ] |
| 4 | [step4](security_risk_assessment_plan.step4.md) | Map interfaces and trust boundaries | Trust boundary diagram + per-boundary interface docs | [ ] |
| 5 | [step5](security_risk_assessment_plan.step5.md) | STRIDE threat modeling (Fabric-enhanced) | STRIDE matrix + per-component threat files, EN threat cross-ref | [ ] |
| 5-review | [step5_review](security_risk_assessment_plan.step5_review.md) | BMAD adversarial review of threat model | `adversarial_review.md` with findings, all HIGH findings addressed | [ ] |
| 5b | [step5b](security_risk_assessment_plan.step5b.md) | Threagile YAML generation + CLI risk report | `threagile.yaml` validates, Threagile output generated | [ ] |
| 6 | [step6](security_risk_assessment_plan.step6.md) | Risk assessment (STRIDE + Threagile merged) | Scored risk register + recommendations | [ ] |
| 6-review | [step6_review](security_risk_assessment_plan.step6_review.md) | BMAD adversarial review of risk assessment | `adversarial_review.md` with findings, scoring validated | [ ] |
| 7a | [step7a](security_risk_assessment_plan.step7a.md) | Semgrep built-in scans | Raw JSON results + summarized markdown | [ ] |
| 7b | [step7b](security_risk_assessment_plan.step7b.md) | Custom Semgrep rules for trust boundaries | Custom YAML rules + scan results | [ ] |
| 7c | [step7c](security_risk_assessment_plan.step7c.md) | AI-driven code vulnerability deep-dive | Code-level findings appended to threat model, risk matrix updated | [ ] |
| 8 | [step8](security_risk_assessment_plan.step8.md) | Compliance consolidation (QuBA-libre + EN matrices) | All 12 output files in `08_compliance_consolidation\` | [ ] |

## Version control rule

A step is complete only when:

1. Every checkbox under **Verifiable result** for that step is satisfied.
2. Required output artifacts exist and are non-empty.
3. The **Status** column above is updated from `[ ]` to `[x]`.

## Scope guardrails

- All products are CRA Important Class 2 — use QuBA-libre format (not AT3350 FMEA).
- Full assessment for RTOSVisor + LxWin; delta assessment for other Type II products.
- EN 304 635 and EN 304 626 are interim drafts — re-evaluate when final standards publish (expected H2 2026).
- Do not skip adversarial reviews (Steps 5-review, 6-review) — they catch blind spots.
- Do not proceed to Step 8 without completed Steps 5-7.

## Parallelization Opportunities

```
├─ Step 0a: BMAD document-project (~60-120 min)  ← run first
├─ Step 0b: Custom agent setup (~10 min)          ← while 0a runs
│
├─ Steps 1-2 (sequential, ~45 min)               ← can start with Step 0a
├─ Step 7a: Semgrep built-in scans (~15 min)      ← can start immediately
│
│  ... wait for Step 0a ...
│
├─ Step 3a-3f (all 6 in parallel, ~25 min)        ← security overlay only
│
│  ... wait for Steps 1-3 ...
│
├─ Step 4 (~25 min) → Step 5 (~40 min) → Step 5-review (~20 min)
├─ Step 5b (~30 min) ← after Step 5
├─ Step 7b (~40 min) ← after Step 4
│
│  ... wait for Steps 5, 5b, 7a, 7b ...
│
├─ Step 6 (~25 min) → Step 6-review (~20 min)
├─ Step 7c (optional, ~2-3 hours) ← after Step 6
│
│  ... wait for Steps 6, 7 ...
│
├─ Step 8a: Parts A+B (~40 min) ← after Step 6
├─ Step 8b: Part C (~50 min)    ← parallel with 8a
```

**Total:** 12-16 agent sessions, ~7-10 hours wall-clock, ~2-3.5 hours human time.

## Related documents

- [security_risk_assessment_strategy.md](security_risk_assessment_strategy.md)
- [QuBA-libre_analyzation.md](../QuBA-libre/QuBA-libre_analyzation.md)
- [implementation_prompt.md](implementation_prompt.md)
