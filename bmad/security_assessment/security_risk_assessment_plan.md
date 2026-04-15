# Security Risk Assessment Plan for the acontis Hypervisor Product Family

## Purpose

This document describes a step-by-step plan to produce a comprehensive, AI-agent-driven security risk assessment of the acontis hypervisor product family. The goal is to generate structured markdown documentation that:

1. Catalogs all binary artifacts produced by the automated build process
2. Maps artifacts to the products they ship in
3. Documents inter-component interfaces and attack surfaces
4. Describes internal details of each artifact (linked to source code)
5. Performs a systematic security risk assessment per component and per product

The plan is designed for **minimal human interaction** — each step can be executed by an AI agent in a fresh chat session, with the output of one step feeding the next.

---

## External Tools Used

This plan integrates the BMAD method and three open-source security tools alongside AI agent analysis:

| Tool | Purpose in This Plan | Installation |
|---|---|---|
| **BMAD Method** | Baseline project documentation (`document-project` workflow), custom security agent with persistent CRA/EN context (agent customization), and adversarial review for threat model / risk assessment validation. Used in Step 0 and as validation passes after Steps 5 and 6 | `npx bmad-method install` — see [BMAD-METHOD repo](https://github.com/bmad-code-org/BMAD-METHOD) |
| **Fabric** (Daniel Miessler) | Curated prompt patterns (`create_threat_model`, `find_vulnerabilities`, `extract_architecture`) used as structured templates for agent prompts in Steps 3 and 5 | `go install github.com/danielmiessler/fabric@latest` or see [fabric repo](https://github.com/danielmiessler/fabric) |
| **Threagile** | Threat-modeling-as-code: generates risk assessments and architectural threat diagrams from a YAML model. Used in Step 5b to produce reproducible, versionable threat output | `docker pull threagile/threagile` or download binary from [threagile.io](https://threagile.io) |
| **Semgrep** | Static analysis (SAST) with custom rules targeting trust boundaries. Used in Steps 7a-7b for automated vulnerability scanning of source code | `pip install semgrep` or `brew install semgrep` |

**Data privacy note:** Fabric by default sends content to a cloud LLM API. For proprietary source code, either (a) configure Fabric with a local model via Ollama, or (b) only pipe the *generated markdown descriptions* through Fabric patterns, never raw source. The agent prompts in this plan use Fabric's pattern structures inline, so running the Fabric CLI is optional — the patterns are embedded directly in the prompts.

---

## Harmonised Standards Reference (CRA Vertical Standards)

The EU Cyber Resilience Act mandates conformity with essential cybersecurity requirements. **Harmonised European Standards** (hEN) provide a voluntary means of demonstrating conformity — compliance with their normative clauses creates a **presumption of conformity** with the corresponding CRA requirements once cited in the EU Official Journal. Two draft harmonised standards are directly applicable to the acontis hypervisor product family:

| Standard | Title | Status | Pages | Applies To |
|---|---|---|---|---|
| **ETSI EN 304 626** V0.1.0 (2025-12) | Cybersecurity requirements for Operating Systems (OS) | Interim mature draft; target publication H2 2026 | 91 | **Linux host OS layer** (kernel, out-of-tree kernel modules, target runtime), **RTOSVisor host OS** scheduling/memory/process management |
| **ETSI EN 304 635** V0.0.10 (2025-12) | Cybersecurity requirements for Virtualisation Execution Stack (VES) and Container Execution Stack (CES), including hypervisors and container runtime systems | Interim mature draft; target publication H2 2026 | 249 | **Hypervisor (RTOSVisor)** product as a whole, **HvWeb** management/orchestration system |

**Location:**
```
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\
├── EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf
└── EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
```

### Why Both Standards Apply

The acontis hypervisor is a **Type I or Type II hypervisor** (EN 304 635 §4.1.2.2) that includes an **operating system layer** (the Linux host). EN 304 635 §4.6.3 explicitly references other harmonised standards (including EN 304 626) for security functions provided by the host OS. This creates a layered compliance model:

```
EN 304 635 (Virtualisation/Container)     EN 304 626 (Operating Systems)
┌─────────────────────────────────────┐   ┌──────────────────────────────────┐
│ §5.1.1 Hypervisor Requirements      │   │ §5.2 Technical Security Reqs     │
│   - VM Isolation                    │   │   - TR-MISO: Memory isolation    │
│   - Control Plane Isolation         │   │   - TR-MSAF: Memory safety       │
│   - Network Plane Separation        │   │   - TR-LMII: Limit impact       │
│   - Boot Chain Integrity            │   │   - TR-SDEF: Secure defaults     │
│   - Guest VM Image Integrity        │   │   - TR-SCUD: Secure updates      │
│   - Runtime Integrity               │   │   - TR-AUTH: Authentication      │
│   - Remote Attestation              │   │   - TR-AVAI: Availability        │
│   - Authentication / Authorization  │   │   - TR-LOGG: Logging             │
│   - Confidentiality Protection      │   │   - TR-VULH: Vuln handling       │
│   - Availability / Resilience       │   │   - ... (18 TR-* requirements)   │
│   - Logging                         │   │                                  │
│   - Patches and Updates             │   │ §Annex C: Risk Assessment        │
│   - Secure Configuration            │   │   - 18 Risk Factors (RF-*)       │
│   - Data Minimization               │   │   - 13 Threats (TH-*)           │
│                                     │   │   - Security Profiles (SP-*)     │
│ §5.1.3 M&O System Requirements      │   │                                  │
│   (applies to HvWeb)                │   │ §Annex D: Risk Evaluation        │
│                                     │   │   - Risk-to-requirement mapping  │
│ §4.4.2 Threat Catalog (VES)         │   │                                  │
│   - Type I / Type II threats        │   │                                  │
│   - M&O system threats              │   │                                  │
│                                     │   │                                  │
│ §6.3.1 Assessment Cases (AC-H-*)    │   │ §6 Conformity Assessment         │
│   ~70 assessment cases for notified │   │                                  │
│   body evaluation                   │   │                                  │
│                                     │   │                                  │
│ §Annex B: Risk Assessment           │   │                                  │
│   - Risk Factor Scoring             │   │                                  │
│   - Likelihood/Impact calculation   │   │                                  │
│   - Use Case risk evaluation        │   │                                  │
└─────────────────────────────────────┘   └──────────────────────────────────┘
         ▼ Hypervisor product                    ▼ Linux host OS components
```

### Product-to-Standard Mapping

| Product / Component | EN 304 635 (VES) | EN 304 626 (OS) | Notes |
|---|---|---|---|
| **RTOSVisor (Type I Hypervisor)** | **Primary** — §5.1.1 (all Hypervisor reqs), §6.3.1 (assessment cases), §4.4.2.1 (Type I threats) | **Secondary** — for Linux host OS layer | Both standards apply; EN 304 635 is the lead standard |
| **LxWin (Type II Hypervisor, representative)** | **Primary** — §5.1.1 (Hypervisor reqs), §4.4.2.2 (Type II threats) | **Secondary** — EN 304 626 applies to the Windows host OS layer | Assessed as representative for all Type II products |
| **Other Type II products** (VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32) | **Primary** — same as LxWin (shared VMF Core + Windows drivers) | Same as LxWin | Covered by LxWin assessment for shared components; product-specific deltas where guest integration differs |
| **HvWeb (management UI)** | **Primary** — §5.1.3 (M&O System reqs) | N/A | Management and Orchestration system requirements (RTOSVisor only) |
| **Linux kernel/drivers** | Referenced as operational environment dependency | **Primary** — §5.2 (TR-MISO, TR-MSAF, TR-LMII, etc.) | EN 304 626 Annex C risk factors apply (RTOSVisor only) |
| **VMF Core (Framework)** | **Primary** — §5.1.1.1 (Isolation), §5.1.1.2 (Integrity) | N/A | Core hypervisor isolation and integrity — shared across all products |
| **Windows Drivers (RtosDrv, etc.)** | **Primary** — guest-host interface for Type II products | **Secondary** — EN 304 626 applies to Windows host OS | Assessed as part of LxWin; shared across all Type II products |

### Key EN 304 635 Content for This Assessment

**Threat catalog (§4.4.2)** — pre-defined threats for Type I and Type II hypervisors that must be addressed:
- Guest VM escape / breakout
- Unauthorized VM creation/modification/deletion
- Side-channel information leakage between VMs
- Control plane compromise (management interface)
- Network plane breach (inter-VM communication)
- Boot chain tampering
- Insecure default configuration

**Security objectives (§4.5)** — twelve objectives that structure the requirements:
Isolation, Integrity Protection, Authentication, Authorization, Confidentiality Protection, Availability/Resilience, Logging, Patches/Updates, Secure Configuration/Default, Data Minimization, Time Synchronization

**Requirement classes (§4.7)** — three levels: Basic, Elevated, Advanced. Products must determine their Security Category Level (SCL) and apply the corresponding requirement class.

**Assessment cases (§6.3.1)** — ~70 specific assessment cases (AC-H-*) that a notified body will use to evaluate the Hypervisor. These are effectively the **test plan** for conformity assessment.

### Key EN 304 626 Content for This Assessment

**Technical requirements (§5.2)** — 18 requirement groups (TR-*), each with specific mitigations (MI-*):
TR-NKEV (no known exploitable vulns), TR-SSDD (secure design/dev), TR-MISO (memory isolation), TR-MSAF (memory safety), TR-LMII (limit incident impact), TR-MINI (minimize external impact), TR-SDEF (secure defaults), TR-SCUD (secure updates), TR-AUTH (authentication), TR-CDST (data confidentiality at rest), TR-CDTX (data confidentiality in transit), TR-CRYP (encryption), TR-IDST (data integrity at rest), TR-IDTX (data integrity in transit), TR-DMIN (data minimization), TR-AVAI (availability), TR-LMAS (minimize attack surface), TR-LOGG (logging), TR-SCDL (secure deletion), TR-SDTR (secure data transfer), TR-VULH (vulnerability handling)

**Risk factors (Annex C.2)** — 18 environmental risk factors (RF-*) that determine the security profile:
RF-NUSR, RF-CUSR, RF-PPII, RF-SNDS, RF-SNDT, RF-SENF, RF-PHYS, RF-UEIN, RF-LOSS, RF-HWMD, RF-SWMD, RF-DVCS, RF-TNET, RF-FNET, RF-CONF, RF-ADMN, RF-SUPP

**Threat catalog (Annex C.4)** — 13 threats (TH-*) with risk assessment methodology:
TH-UEVU, TH-KEVU, TH-UAPP, TH-UAPS, TH-UAPN, TH-UADT, TH-PDOS, TH-DDOS, TH-MQSE, TH-LEAK

**Important note:** These are interim drafts subject to change before final publication (expected H2 2026). The assessment should target the current draft requirements but must be re-evaluated when the final standards are published.

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

From `buildprogram\CfgDefault.bat` product flags and `rtv` directory structure:

| Product | Hypervisor Type | Config Flag | Source Root | Platform |
|---|---|---|---|---|
| **Hypervisor (RTOSVisor)** | **Type I** | `RTE_BuildProductHypervisor` | `rtv\Hypervisor\`, `rtv\Linux\` | Full hypervisor (Linux host + guests) |
| VxWin | Type II | `RTE_BuildProductVxWin` | `rtv\VxWin\` | VxWorks guest on Windows host |
| CeWin | Type II | `RTE_BuildProductCeWin` | `rtv\CeWin\` | Windows CE guest on Windows host |
| **LxWin** | **Type II** | `RTE_BuildProductLxWin` | `rtv\LxWin\` | RT-Linux guest on Windows |
| VmfWin | Type II | `RTE_BuildProductVmfWin` | `rtv\Framework\`, `rtv\Windows\` | VMF standalone on Windows |
| RTOS32Win | Type II | `RTE_BuildProductRTOS32Win` | `rtv\RTOS32Win\`, `rtv\Common\Rt32\` | RTOS-32 guest on Windows |
| EC-WinRTOS-32 | Type II | `RTE_BuildProductEcWinRtos32` | `rtv\EC-WinRTOS-32\` | EtherCAT + RTOS-32 on Windows |

**All products are hypervisor products** and fall under CRA Important Class 2 (see classification below). The Type I Hypervisor (RTOSVisor) runs directly on a Linux host. The Type II Hypervisor products run on a Windows host OS. acontis will perform the full risk assessment for the Type I Hypervisor (RTOSVisor) and for **LxWin** as the representative Type II Hypervisor product. The remaining Type II products share the same VMF Framework Core and Windows driver stack as LxWin, so LxWin findings are largely transferable.

Shared components used across products:

| Component | Source Root | Role |
|---|---|---|
| Framework (VMF Core) | `rtv\Framework\Source\Core\` | Virtual Machine Framework kernel |
| Common SDK | `rtv\Common\All\SDK\Inc\` | Shared API headers (`vmfInterface.h`, `rtosLib.h`) |
| Windows Drivers | `rtv\Windows\Source\Driver\` | Kernel-mode drivers (RtosDrv, RtosVnet, RtosPnp) |
| Windows RtosLib | `rtv\Windows\Source\RtosLib\` | User-mode runtime library |
| Windows RtosService | `rtv\Windows\Source\RtosService\` | Windows service for VMF |
| Windows SystemManager | `rtv\Windows\Source\SystemManager\` | WPF management application |
| Linux Drivers | `rtv\Linux\Source\Driver\` | Out-of-tree kernel modules |
| Linux Target Runtime | `rtv\Linux\target\hv\` | Hypervisor runtime (services, scripts, templates) |
| HvWeb | `rtv\Hypervisor\Source\HvWeb\` | ASP.NET + Angular web management UI |

---

## CRA Product Classification and Risk Assessment Format

### EU Cyber Resilience Act Classification

The CRA classifies products with digital elements into four tiers, each with different conformity assessment requirements. **All acontis hypervisor products** "support virtualised execution of operating systems" and therefore fall under Important Class 2:

| Product | CRA Classification | Conformity Assessment | Rationale |
|---|---|---|---|
| **All acontis hypervisor products** (RTOSVisor, VxWin, CeWin, LxWin, VmfWin, RTOS32Win, EC-WinRTOS-32) | **Important Class 2** | Mandatory third-party assessment by a notified body | CRA Annex III explicitly lists "hypervisors and container runtime systems that support virtualised execution of operating systems" as Important Class 2. All products in this family virtualise one or more guest operating systems. |

### Assessment Scope Decision

While all products require CRA Important Class 2 conformity assessment, acontis will perform the full risk assessment for:

- **RTOSVisor** (Type I Hypervisor) — the Linux-hosted hypervisor with HvWeb management, representing the broadest attack surface
- **LxWin** (Type II Hypervisor) — the representative Windows-hosted product, chosen because it shares the VMF Framework Core, Windows driver stack, and user-mode libraries with all other Type II products (VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32)

The remaining Type II products differ primarily in their guest OS integration (VxWorks BSP, WinCE runtime, RTOS-32 loader, etc.) but share the same host-side security-relevant components. Findings from the LxWin assessment are therefore **transferable** to the other Type II products, with product-specific deltas documented where guest integration creates unique attack surfaces.

This classification has a direct impact on the depth and formality of the required risk assessment and the choice of documentation format.

### Why the AT3350 FMEA Format Is Insufficient for the Hypervisor Products

acontis uses the AT3350 format (FMEA-style: Likelihood × Impact → RPN in a flat risk table) for the EC-Master EtherCAT master stack. While this format works well for EC-Master — a single software library with a bounded attack surface (RAS, EoE, ENI, EtherCAT frames) and ~30 risk entries — it is **insufficient for the hypervisor products** for the following reasons:

1. **Missing structured trust boundary analysis.** The Hypervisor spans kernel drivers, user-mode libraries, a web management UI, guest runtimes, shared memory regions (IVSHMEM), virtio interfaces, and MQTT messaging. A flat risk table cannot model the layered guest→host→network→web trust architecture. Attack paths in the Hypervisor are multi-hop (e.g., guest exploits VMF call → gains host kernel access → pivots to web management interface), requiring hierarchical threat modeling that the AT3350 format does not support.

2. **No CRA Annex I traceability.** As an Important Class 2 product, the Hypervisor must undergo mandatory conformity assessment by a notified body. This requires documented traceability from each CRA Annex I essential cybersecurity requirement (items a–m) to specific countermeasures and risk treatment decisions. The AT3350 format provides no such mapping. By contrast, the QuBA-libre format auto-generates an Annex I 1.2 report linking requirements to implemented countermeasures.

3. **No systematic countermeasure catalog.** AT3350 tracks risks but does not maintain a structured catalog of countermeasures (mapped to IEC 62443, ETSI EN 303 645, or CRA requirements) with their effectiveness against specific attack steps. For a multi-component system like the Hypervisor, tracking which countermeasure mitigates which attack path across which trust boundary is essential.

4. **No assumption management.** Hypervisor security depends heavily on customer deployment assumptions (trusted networks, physical access restrictions, guest OS trustworthiness). These assumptions must be formally documented, assigned to stakeholders, and tracked — the AT3350 format has no mechanism for this.

5. **Scale.** The Hypervisor's attack surface would generate 200+ risk entries, making the flat table structure unwieldy and error-prone compared to the automated risk calculation in QuBA-libre's formula-driven approach.

### Recommended Approach: Layered Assessment

This plan serves as the **deep technical investigation and evidence-generation layer**. Its outputs (Steps 1–7) feed into a formal risk register for compliance documentation:

```
This Plan (Steps 1-7)                    Formal Risk Assessment Document
┌────────────────────────┐               ┌─────────────────────────────────┐
│ Step 1: Artifact Registry ──────────►  │                                 │
│ Step 2: Product-Artifact Map ───────►  │  RTOSVisor (Type I Hypervisor): │
│ Step 3: Component Documentation ────►  │    QuBA-libre format            │
│ Step 4: Interface & Trust Boundaries ► │    - Questionnaire-driven       │
│ Step 5: STRIDE Threat Model ────────►  │    - Automated CRA Annex I map  │
│ Step 5b: Threagile Analysis ────────►  │    - Countermeasure catalog      │
│ Step 6: Risk Assessment ────────────►  │    - Assumption tracking         │
│ Step 7: Semgrep + Code Audit ───────►  │    - Required for notified body  │
│                                  │     │                                 │
│  (evidence, findings, analysis)  ├──►  │  LxWin (Type II representative):│
│                                  │     │    QuBA-libre format            │
│                                  │     │    (representative for all      │
│                                  │     │     Type II products)           │
│                                  │     │                                 │
│                                  └──►  │  Other Type II products:        │
│                                        │    Delta assessment only         │
│                                        │    (product-specific guest       │
└────────────────────────┘               │     integration differences)    │
                                         └─────────────────────────────────┘
```

**Step 8** (below) describes how to consolidate this plan's outputs into the QuBA-libre format for RTOSVisor and LxWin, and how to produce delta assessments for the remaining Type II products.

---

## Output Directory Structure

All generated artifacts are written under a single output tree for traceability:

```
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\
├── 01_artifact_registry\
│   ├── index.md                        # Master artifact list
│   ├── windows_artifacts.md            # Windows DLLs, EXEs, SYS drivers
│   ├── linux_artifacts.md              # Linux SOs, binaries, kernel modules
│   ├── installer_artifacts.md          # MSI, WiX bundles, setup EXEs
│   └── prebuilt_external.md            # Third-party / prebuilt binaries
├── 02_product_artifact_map\
│   ├── index.md                        # Cross-reference: artifact → product(s)
│   ├── product_vxwin.md
│   ├── product_cewin.md
│   ├── product_vmfwin.md
│   ├── product_rtos32win.md
│   ├── product_ecwinrtos32.md
│   ├── product_lxwin.md
│   └── product_hypervisor.md
├── 03_component_documentation\
│   ├── index.md                        # Component overview + navigation
│   ├── framework_vmf_core.md
│   ├── windows_drivers.md
│   ├── windows_rtoslib.md
│   ├── windows_rtosservice.md
│   ├── windows_systemmanager.md
│   ├── linux_drivers.md
│   ├── linux_target_runtime.md
│   ├── hypervisor_hvweb.md
│   ├── hypervisor_hvdevicemgr.md
│   ├── hypervisor_virtio_events.md
│   ├── lxwin_yocto_drivers.md
│   ├── vxwin_bsp.md
│   ├── common_sdk.md
│   └── common_vmfcall_interface.md
├── 04_interface_map\
│   ├── index.md                        # Interface overview + trust boundaries
│   ├── kernel_user_interfaces.md       # Driver ↔ user-mode boundaries
│   ├── vmf_call_interface.md           # VMF call dispatch (host ↔ guest)
│   ├── network_interfaces.md           # RtosVnet, IVSHMEM, MQTT, virtio
│   ├── ipc_shared_memory.md            # IVSHMEM, shared memory regions
│   ├── web_api_interfaces.md           # HvWeb REST/WebSocket, SystemManager
│   └── installer_deployment.md         # Setup chains, signing, privilege escalation
├── 05_threat_model\
│   ├── index.md                        # STRIDE summary + risk matrix
│   ├── threat_model_vmf_core.md        # VMF framework threats
│   ├── threat_model_drivers.md         # Kernel driver threats
│   ├── threat_model_network.md         # Network-facing component threats
│   ├── threat_model_web.md             # HvWeb + SystemManager threats
│   ├── threat_model_guest_escape.md    # Guest-to-host escape vectors
│   ├── threat_model_supply_chain.md    # Build process + third-party threats
│   ├── threat_model_deployment.md      # Installer, signing, update threats
│   └── adversarial_review.md           # BMAD adversarial review findings (Step 5-review)
├── 05b_threagile\
│   ├── threagile.yaml                  # Threagile model (generated by agent)
│   ├── threagile_report.md             # Summary of Threagile output
│   └── output\                         # Threagile-generated reports and diagrams
│       ├── report.pdf                  #   Full risk report
│       ├── risks.json                  #   Machine-readable risk data
│       ├── data-flow-diagram.png       #   Architectural data-flow diagram
│       └── ...                         #   Additional Threagile output files
├── 06_risk_assessment\
│   ├── index.md                        # Consolidated risk register (STRIDE + Threagile merged)
│   ├── risk_matrix.md                  # Probability × Impact scoring
│   ├── adversarial_review.md           # BMAD adversarial review findings (Step 6-review)
│   ├── per_product_risk.md             # Risk summary per product
│   └── recommendations.md             # Prioritized remediation actions
├── 07_semgrep\
│   ├── index.md                        # Semgrep scan summary and findings overview
│   ├── builtin_scan_results.md         # Results from standard Semgrep rule packs
│   ├── custom_rules\                   # Agent-generated Semgrep rules (YAML)
│   │   ├── vmf_call_validation.yaml    #   VMF call parameter checking rules
│   │   ├── ioctl_input_validation.yaml #   Driver IOCTL buffer validation rules
│   │   ├── ivshmem_bounds.yaml         #   IVSHMEM shared memory bounds rules
│   │   └── web_injection.yaml          #   HvWeb injection/auth rules
│   └── custom_scan_results.md          # Results from custom rule scans
├── 08_compliance_consolidation\
│   ├── index.md                        # Consolidation strategy, format rationale, EN standard overview
│   ├── hypervisor_quba_inputs.md       # QuBA-libre questionnaire answer recommendations
│   ├── hypervisor_attack_steps.md      # Hypervisor-specific attack step extensions
│   ├── hypervisor_countermeasures.md   # Countermeasure catalog extensions
│   ├── hypervisor_assumptions.md       # Deployment assumptions and stakeholder assignments
│   ├── lxwin_quba_inputs.md            # LxWin-specific QuBA-libre questionnaire answers
│   ├── type2_product_deltas.md         # Per-product delta assessments (VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32)
│   ├── cra_annex_i_checklist.md        # Gap analysis: CRA Annex I (a)–(m) coverage status
│   ├── en304_635_compliance.md         # EN 304 635 §5.1.1/§5.1.3 requirement compliance matrix
│   ├── en304_635_assessment_cases.md   # EN 304 635 §6.3.1 assessment case evidence mapping (~70 AC-H-* cases)
│   ├── en304_626_compliance.md         # EN 304 626 §5.2 TR-* technical requirement compliance matrix
│   ├── en304_626_risk_factors.md       # EN 304 626 Annex C.2 RF-* risk factor scoring + security profile
│   └── en304_635_risk_factors.md       # EN 304 635 Annex B risk factor scoring + SCL determination
└── 00_plan_execution_log.md            # Execution tracking (which steps done)
```

---

## Execution Steps

Each step is designed to be run as a **single AI agent session** (fresh chat). The instructions for each step include the exact prompt to use.

### Prerequisites

- AI IDE (Cursor, Claude Code, or similar) with file system access to both `buildprogram` and `rtv`
- **BMAD Method installed** in the `rtv` repository (`npx bmad-method install`) — used for `document-project` baseline (Step 0), agent customization, and adversarial review
- Each step should be run in a **fresh chat session** to avoid context pollution
- After each step, verify the output files exist and are non-empty before proceeding

**Tool installations (needed for Steps 5b, 7a, 7b):**

```bash
# Threagile (Step 5b) — Docker is the easiest option
docker pull threagile/threagile

# Semgrep (Steps 7a, 7b) — Python package
pip install semgrep

# Fabric (optional — patterns are embedded in prompts, but CLI is useful for iteration)
# Requires Go 1.22+
go install github.com/danielmiessler/fabric@latest
fabric --setup  # configure with your preferred LLM API key or local Ollama endpoint
```

---

### Step 0: BMAD Baseline — Document Project and Create Security Agent

This step leverages the BMAD method directly to (a) generate baseline project documentation and (b) create a custom security-assessment agent that provides persistent context for all subsequent steps.

#### Step 0a: Run `document-project` (BMAD Analyst Workflow)

**Goal:** Produce comprehensive baseline documentation of the `rtv` codebase — architecture, technology stack, source tree, integration points, dependencies — so that subsequent security analysis steps (especially Step 3) can build on this foundation rather than rediscovering the same information.

**Method:**

1. Open a fresh chat session in your AI IDE
2. Load the BMAD Analyst agent: `bmad-analyst`
3. Run: `document-project`
4. When prompted for scan depth, select **Deep Scan** or **Exhaustive Scan** (not Quick — the security assessment needs source-level detail)
5. Point the workflow at the `rtv` repository root: `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\`
6. The workflow will classify the project, detect components and parts, scan technology stacks, and generate structured documentation under `_bmad-output/`
7. After the full scan completes, run **deep-dive** sessions for the six component groups defined in Step 3 (Framework VMF Core, Windows Drivers, Windows User-Mode, Linux Components, Hypervisor Components, LxWin/VxWin/SDK)

**Output:** BMAD-generated documentation in `rtv\_bmad-output\` including:
- `index.md` (master project documentation index)
- `project-overview.md`
- `architecture.md` (or per-part architecture files)
- `source-tree-analysis.md`
- Deep-dive files for each component group

**Why this matters:** The `document-project` workflow already knows how to systematically scan codebases, classify project types, map dependencies, identify architecture patterns, and generate source tree analyses. Step 3 of this plan asks the AI to do much of the same work but with a security lens. By running `document-project` first, Step 3 can **consume the baseline documentation as input** and focus exclusively on the security overlay (trust boundaries, privilege contexts, security-relevant patterns, harmonised standard mapping) instead of also having to discover the basic architecture.

**Human interaction:** Minimal — select scan depth, confirm project classification, and choose deep-dive targets.

#### Step 0b: Create Custom Security-Assessment Agent (BMAD Agent Customization)

**Goal:** Create a BMAD custom agent with persistent memories and context so that every subsequent step inherits a consistent understanding of the CRA classification, applicable harmonised standards, trust boundary definitions, and product-to-standard mapping — without having to repeat this context in every prompt.

**Method:**

1. In the `rtv` project's `_bmad/_config/agents/` directory, create or edit the DEV agent customization file (`.customize.yaml`) with the following content:

```yaml
# Security Risk Assessment Agent Customization
persona:
  name: 'Security Analyst'
  role: 'Security risk analyst specializing in CRA compliance for hypervisor/virtualization systems'
  communication_style: 'Security-first, compliance-aware, evidence-citing'
  principles:
    - 'Every finding must reference specific source files and line ranges'
    - 'Trust boundaries are the primary lens for all analysis'
    - 'Harmonised standard requirements drive completeness checks'

memories:
  - 'CRA Classification: ALL acontis hypervisor products = Important Class 2 (mandatory notified body assessment). RTOSVisor = Type I Hypervisor (Linux host). VxWin/CeWin/LxWin/VmfWin/RTOS32Win/EC-WinRTOS-32 = Type II Hypervisors (Windows host). Full assessment for RTOSVisor + LxWin (representative Type II). Other Type II products: delta assessment only.'
  - 'Applicable harmonised standards: EN 304 635 (Virtualisation/Container) for hypervisor and M&O components; EN 304 626 (Operating Systems) for Linux host OS layer.'
  - 'EN 304 635 key sections: §5.1.1 Hypervisor Requirements (Isolation, Integrity, Auth, AuthZ, Confidentiality, Availability, Logging, Updates, Secure Config, Data Minimization), §5.1.3 M&O System Requirements (for HvWeb), §4.4.2 Threat Catalog, §6.3.1 Assessment Cases (~70 AC-H-*).'
  - 'EN 304 626 key sections: §5.2 Technical Requirements (TR-MISO, TR-MSAF, TR-LMII, TR-SDEF, TR-SCUD, TR-AUTH, TR-AVAI, TR-LOGG, TR-VULH, etc.), Annex C Risk Factors (RF-*), Annex C.4 Threats (TH-*).'
  - 'Trust boundaries: Guest VM ↔ VMF Core (VMF calls), Kernel ↔ User-mode (IOCTLs), Host ↔ Network (RtosVnet, IVSHMEM, MQTT, virtio), Web Client ↔ HvWeb (REST/WebSocket), Build system ↔ Deployed artifacts (signing).'
  - 'Products: RTOSVisor (Hypervisor), VxWin, CeWin, LxWin, VmfWin, RTOS32Win, EC-WinRTOS-32. Shared component: VMF Framework Core.'
  - 'Risk register formats: QuBA-libre for RTOSVisor and LxWin (Important Class 2, full assessment). Delta assessment for other Type II products referencing LxWin findings.'
  - 'EN standard PDFs at: C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf and EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf'

critical_actions:
  - 'Before starting any analysis: read the BMAD project documentation at rtv\_bmad-output\index.md for baseline architecture context'
  - 'For every component analysis: check trust boundary crossings and map findings to applicable EN standard requirements'
  - 'Always ignore folders named brainstormingPlatform or brainstormingPlatformPlus'

menu:
  - trigger: run-step-1
    description: 'Step 1: Extract Artifact Registry from Build Scripts'
  - trigger: run-step-2
    description: 'Step 2: Map Artifacts to Products'
  - trigger: run-step-3
    description: 'Step 3: Document Components (Security Overlay)'
  - trigger: run-step-4
    description: 'Step 4: Map Interfaces and Trust Boundaries'
  - trigger: run-step-5
    description: 'Step 5: STRIDE Threat Modeling'
  - trigger: run-step-6
    description: 'Step 6: Risk Assessment and Recommendations'
```

2. Recompile agents to apply the customization

**Why this matters:** Without this agent, every step requires a multi-paragraph preamble in the prompt explaining the CRA context, products, trust boundaries, and EN standard references. With the custom agent, this context is loaded automatically — the agent *remembers* it across every session. This is directly analogous to BMAD's Healthcare Compliance Agent example, but for CRA/hypervisor security.

**Human interaction:** One-time setup (~10 min).

---

### Step 1: Extract Artifact Registry from Build Scripts

**Goal:** Produce a complete inventory of every binary artifact (DLL, EXE, SYS, SO, kernel module, setup package) built by the automated build process.

**Input:**
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\` (all `bld*.bat` files)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\CfgDefault.bat`

**Method:**
1. Parse `CfgDefault.bat` to extract all `RTE_Build*`, `RTE_Dir*`, `RTE_Binary*`, `RTE_Product*` variables
2. Scan all `bld*.bat` files for patterns indicating artifact outputs:
   - `devenv.com ... /rebuild` or `msbuild` invocations → identify `.dll`, `.exe`, `.sys` outputs
   - `copy` / `xcopy` commands targeting release/output directories
   - `Sign.bat` invocations (signed artifacts are deployed binaries)
   - `candle` / `light` (WiX) invocations → MSI/EXE installer outputs
3. Scan `rtv\Workspace\WindowsVS2015\Setup\*.wixproj` for packaged artifact names
4. For Linux artifacts, scan `bld50_lx\`, `bld50_hv\` for remote build outputs and delivery paths
5. Record for each artifact: **name**, **type** (DLL/EXE/SYS/SO/MSI), **build script**, **output path pattern**, **signing status**

**Output files:**
- `01_artifact_registry\index.md`
- `01_artifact_registry\windows_artifacts.md`
- `01_artifact_registry\linux_artifacts.md`
- `01_artifact_registry\installer_artifacts.md`
- `01_artifact_registry\prebuilt_external.md`

**Agent prompt (copy into fresh chat):**
```
You are a build system analyst. Your task is to extract a complete inventory of every
binary artifact produced by the acontis hypervisor automated build process.

Scan these locations:
- C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\ (all bld*.bat files and CfgDefault.bat)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Workspace\WindowsVS2015\Setup\ (*.wixproj files)

For each artifact found, record: name, type (DLL/EXE/SYS/SO/KO/MSI/EXE-installer),
source build script, output path pattern, whether it is signed, and platform (Windows/Linux).

Look for these patterns in .bat files:
- devenv.com or msbuild invocations (the project file reveals the output binary name)
- copy/xcopy to release/delivery directories (reveals binary filenames)
- Sign.bat calls (reveals which files are signed)
- candle/light (WiX MSI builds)
- Remote Linux build outputs (plink, ssh, scp commands referencing .so or binary names)

Organize output into four markdown files under:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\01_artifact_registry\

Files: index.md (master list with counts), windows_artifacts.md, linux_artifacts.md,
installer_artifacts.md, prebuilt_external.md (for third-party/prebuilt binaries).

Use tables with columns: Artifact Name | Type | Build Script | Output Path | Signed | Notes.

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Human interaction:** None required. Review output for completeness afterward.

---

### Step 2: Map Artifacts to Products

**Goal:** Create a cross-reference showing which artifacts ship in which product(s), identifying shared components.

**Input:**
- Output from Step 1 (`01_artifact_registry\*.md`)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\CfgDefault.bat` (product flags and directory mappings)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\Build.bat` (`:SubCreateProducts` logic)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\bld80_setup\bld40_Setup*.bat` (per-product setup scripts)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Workspace\WindowsVS2015\Setup\*.wixproj` (WiX product definitions)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\*\Setup\Wix\` directories (per-product WiX sources)

**Method:**
1. Parse `CfgDefault.bat` for the 7 product definitions and their directory/flag mappings
2. For each product, trace the build flow through `Build.bat` → `BuildSub.bat` → `bld50_*` → `bld80_setup`
3. Examine WiX `.wxs` source files under each product's `Setup\Wix\` to find which binaries are included in each installer
4. Cross-reference with the artifact registry from Step 1
5. Identify artifacts shared across multiple products vs. product-specific artifacts

**Output files:**
- `02_product_artifact_map\index.md` (cross-reference matrix)
- `02_product_artifact_map\product_<name>.md` (one per product, listing all artifacts)

**Agent prompt (copy into fresh chat):**
```
You are a build system analyst. Your task is to map binary artifacts to the products
they ship in for the acontis hypervisor product family.

Read the artifact registry at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\01_artifact_registry\

Then analyze:
- C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\CfgDefault.bat (product definitions)
- C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\Build.bat (product creation flow)
- C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\bld80_setup\bld40_Setup*.bat (per-product setups)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\*\Setup\Wix\ directories (WiX source .wxs files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Workspace\WindowsVS2015\Setup\ (WiX projects)

Products to map: VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32, LxWin, Hypervisor.

Create:
- index.md: matrix table (rows=artifacts, columns=products, cells=included/not)
- One file per product (product_vxwin.md, product_cewin.md, etc.) listing all
  artifacts in that product with their role and whether they are shared or exclusive.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\02_product_artifact_map\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Human interaction:** None required.

---

### Step 3: Document Components (Source-Level Analysis)

**Goal:** For each major component, produce a markdown document describing its purpose, source structure, internal architecture, key data flows, and external dependencies.

**Tools:** This step uses the structure from **Fabric's `extract_architecture` pattern** to ensure consistent, security-relevant output across all component docs.

**Input:**
- `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\` (source code)
- **BMAD baseline documentation from Step 0:** `rtv\_bmad-output\index.md` and associated files (architecture, source tree, deep-dive docs). The agent should read this first to understand the already-documented architecture, dependencies, and source structure — then focus on adding the security-specific sections (trust boundaries, privilege context, security patterns, EN standard mapping) that the BMAD baseline does not cover.
- Existing documentation at `rtv\ai\`, `rtv\Hypervisor\Doc\`, component READMEs

**Method:**

This step should be executed as **multiple parallel agent sessions**, one per component group, to manage context size. If the BMAD custom security agent (Step 0b) is active, it will automatically load the CRA context and trust boundary definitions into each session. Suggested grouping:

| Session | Components to Document |
|---|---|
| 3a | Framework VMF Core (`Framework\Source\Core\`) |
| 3b | Windows Drivers (`Windows\Source\Driver\*`) |
| 3c | Windows User-Mode (`Windows\Source\RtosLib\`, `RtosService\`, `SystemManager\`, `VmfInterfaceUserMode\`) |
| 3d | Linux Components (`Linux\Source\*`, `Linux\target\hv\`) |
| 3e | Hypervisor Components (`Hypervisor\Source\*`) |
| 3f | LxWin/VxWin/SDK (`LxWin\Source\*`, `VxWin\Source\*`, `Common\All\*`) |

For each component, the agent should document (following the Fabric `extract_architecture` output structure):
1. **Purpose and role** within the product(s)
2. **Source files and directory structure** (with file counts and languages)
3. **Key data structures and algorithms** (from reading source)
4. **External dependencies** (libraries, OS APIs, third-party code)
5. **Input/output behavior** (what data enters, what leaves)
6. **Privilege level** (kernel, user, service, web)
7. **Configuration and runtime parameters**
8. **Security-relevant patterns found** (crypto usage, authentication, input validation, memory management)
9. **Data flow summary** (one-paragraph description suitable for threat modeling input)
10. **Trust boundary position** (which trust zones does this component straddle?)
11. **Applicable harmonised standard requirements** — map to EN 304 635 (VES/hypervisor) and/or EN 304 626 (OS) requirements with preliminary compliance status

**Output files:**
- `03_component_documentation\index.md`
- `03_component_documentation\<component_name>.md` (one per component)

**Agent prompt template (copy into fresh chat, adjust component paths per session):**

This prompt incorporates the structure from Fabric's `extract_architecture` pattern to produce security-analysis-ready output:

```
You are a security-focused source code analyst. Your task is to document the
following component(s) of the acontis hypervisor system for a security risk assessment.

FIRST: Read the BMAD baseline documentation for architecture context:
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\_bmad-output\index.md (master index)
- Any architecture or deep-dive files relevant to the component(s) below
Use this as your starting point — do not rediscover what BMAD already documented
(architecture patterns, source tree structure, dependencies, technology stack).
Focus your effort on the SECURITY-SPECIFIC sections that the baseline does not cover.

Component(s) to analyze:
- [INSERT COMPONENT NAME]: C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\[INSERT PATH]

For each component, produce a markdown file with these sections (based on Fabric's
extract_architecture pattern, adapted for security analysis):

## 1. Overview
Purpose and role (1-2 paragraphs). What problem does this component solve?

## 2. Source Structure
Directory listing, file counts, languages used.

## 3. Architecture & Key Data Structures
Key data structures, algorithms, and design patterns (read key source/header files).
Include a brief data-flow description: what enters, what exits, through which interfaces.

## 4. External Dependencies
OS APIs, third-party libraries, other RTV components this depends on.
Flag any dependencies that are security-sensitive (crypto libs, network libs, OS kernel APIs).

## 5. Interfaces Provided and Consumed
- APIs/interfaces this component EXPOSES (with calling convention, parameters)
- APIs/interfaces this component CONSUMES from other components
- For each: data format, validation performed, authentication required

## 6. Privilege & Trust Context
- Privilege level (kernel-mode, user-mode, service, elevated, web)
- Which trust zone(s) this component operates in
- Which trust boundaries it crosses or straddles

## 7. Configuration & Runtime Parameters
Registry keys, config files, environment variables, command-line args.
Flag any security-relevant defaults (e.g., auth disabled by default, open ports).

## 8. Security-Relevant Patterns
For each category below, note what you find (or explicitly note "not found"):
- Cryptographic operations (algorithms, key management)
- Authentication / authorization (mechanisms, enforcement points)
- Input validation / sanitization (where, how thorough)
- Memory management (allocations, buffer handling, bounds checking)
- File system access (paths, permissions, symlink handling)
- Network communication (protocols, TLS, certificate validation)
- IPC mechanisms (shared memory, pipes, sockets, IOCTLs)
- Error handling patterns (fail-open vs. fail-closed, information leakage in errors)

## 9. Data Flow Summary
One paragraph suitable as input for STRIDE threat modeling and Threagile YAML generation.
Describe: source of input → processing → output destination, with trust levels annotated.

## 10. Applicable Harmonised Standard Requirements
This component must be assessed against specific requirements from the CRA harmonised
standards. Based on the component type, identify the applicable requirements:

For hypervisor/virtualization components (VMF Core, virtio, IVSHMEM, guest management):
  Reference EN 304 635 §5.1.1 — list which Hypervisor Requirements apply:
  Isolation (§5.1.1.1), Integrity Protection (§5.1.1.2), Authentication (§5.1.1.3),
  Authorization (§5.1.1.4), Confidentiality (§5.1.1.5), Availability (§5.1.1.6),
  Logging (§5.1.1.7), Patches/Updates (§5.1.1.8), Secure Config (§5.1.1.9),
  Data Minimization (§5.1.1.10).

For management/orchestration components (HvWeb, SystemManager):
  Reference EN 304 635 §5.1.3 — list which M&O System Requirements apply:
  Authentication (§5.1.3.1), Authorization (§5.1.3.2), Secure Config (§5.1.3.3),
  Communication Security (§5.1.3.4), Integrity (§5.1.3.5), Patches/Updates (§5.1.3.7).

For Linux host OS components (kernel modules, drivers, target runtime):
  Reference EN 304 626 §5.2 — list which Technical Requirements apply:
  TR-MISO (memory isolation), TR-MSAF (memory safety), TR-LMII (limit impact),
  TR-SDEF (secure defaults), TR-SCUD (secure updates), TR-AUTH (authentication),
  TR-AVAI (availability), TR-LOGG (logging), TR-VULH (vulnerability handling), etc.

For each applicable requirement, briefly note:
- Current compliance status based on observed code patterns (Met / Partially Met / Not Met / Unknown)
- Evidence (cite specific file/function if compliance is visible in code)
- Gaps (what is missing or unclear)

The harmonised standard PDFs are located at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf

Read the actual source files — do not guess or hallucinate file contents.
Cite specific file paths and line ranges where relevant.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Human interaction:** Minimal — choose which component sessions to run first based on priority. All 6 sessions can run independently.

---

### Step 4: Map Interfaces and Trust Boundaries

**Goal:** Document all inter-component interfaces, data flows crossing trust boundaries, and external-facing surfaces.

**Input:**
- Component documentation from Step 3 (`03_component_documentation\*.md`)
- Key interface headers:
  - `rtv\Common\All\SDK\Inc\vmfInterface.h` (VMF API)
  - `rtv\Common\All\SDK\Inc\rtosLib.h` (RtosLib API)
  - `rtv\Windows\Source\Driver\RtosDrv\Vmf\vmfDrvInterface.cpp`
  - `rtv\Linux\Source\Driver\hrtosdrv\Vmf\vmfDrvInterface.cpp`
  - `rtv\Linux\Source\HostRtosDrvInterfaceUserMode\HostRtosDrvIf.h`
  - `rtv\Hypervisor\Source\HvWeb\` (web API endpoints)
  - `rtv\Hypervisor\Source\virtio_events\` (virtio event interface)
  - `rtv\Hypervisor\Source\MQTTnet\` (MQTT messaging)

**Method:**
1. Identify all trust boundary crossings:
   - **Guest → Host** (VMF calls, virtio, IVSHMEM shared memory)
   - **User-mode → Kernel-mode** (driver IOCTLs, system calls)
   - **Network → Application** (HvWeb HTTP/WebSocket, MQTT, SystemManager)
   - **Unprivileged → Privileged** (service interfaces, installer elevation)
   - **External → Internal** (file uploads, configuration inputs, USB passthrough)
2. For each interface, document: calling convention, data format, validation performed, authentication required, error handling
3. Draw a text-based interface diagram showing trust zones

**Output files:**
- `04_interface_map\index.md` (overview with ASCII trust boundary diagram)
- `04_interface_map\kernel_user_interfaces.md`
- `04_interface_map\vmf_call_interface.md`
- `04_interface_map\network_interfaces.md`
- `04_interface_map\ipc_shared_memory.md`
- `04_interface_map\web_api_interfaces.md`
- `04_interface_map\installer_deployment.md`

**Agent prompt (copy into fresh chat):**
```
You are a security architect performing interface analysis on the acontis hypervisor product family.

Read the component documentation at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\

Then analyze these key interface files in the source:
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Common\All\SDK\Inc\vmfInterface.h
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Common\All\SDK\Inc\rtosLib.h
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Windows\Source\Driver\RtosDrv\Vmf\ (vmfDrvInterface)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Linux\Source\Driver\hrtosdrv\Vmf\ (vmfDrvInterface)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Linux\Source\HostRtosDrvInterfaceUserMode\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Hypervisor\Source\HvWeb\ (web API)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Hypervisor\Source\virtio_events\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Hypervisor\Source\MQTTnet\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Windows\Source\SystemManager\
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Framework\Source\Core\ (IVSHMEM headers)

Identify and document ALL inter-component interfaces, organized by trust boundary:
1. Guest-to-Host boundaries (VMF calls, virtio, IVSHMEM shared memory)
2. User-mode to Kernel-mode boundaries (driver IOCTLs)
3. Network-facing interfaces (HTTP, WebSocket, MQTT)
4. IPC / shared memory interfaces
5. Installer / deployment privilege transitions
6. External input surfaces (config files, USB, PCI passthrough)

For each interface document: protocol/mechanism, data format, input validation,
authentication, error handling, privilege levels on each side.

Create an ASCII trust-boundary diagram in index.md showing trust zones and crossings.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Human interaction:** None required.

---

### Step 5: STRIDE Threat Modeling

**Goal:** Perform systematic STRIDE threat analysis for each interface and component, producing a categorized threat catalog.

**Tools:** This step uses the structure from **Fabric's `create_threat_model` pattern** for consistent threat documentation. The output also prepares input for Threagile in Step 5b.

**Input:**
- Interface map from Step 4 (`04_interface_map\*.md`)
- Component documentation from Step 3 (`03_component_documentation\*.md`)
- Artifact registry from Step 1 (`01_artifact_registry\*.md`)

**Method:**

Apply the STRIDE framework systematically to each trust boundary and component (following the Fabric `create_threat_model` output structure):

| STRIDE Category | Question to Ask |
|---|---|
| **S**poofing | Can an attacker impersonate a legitimate component, user, or guest VM? |
| **T**ampering | Can data in transit or at rest be modified (VMF calls, shared memory, configs)? |
| **R**epudiation | Can actions be performed without attribution/logging? |
| **I**nformation Disclosure | Can sensitive data leak across trust boundaries (memory, network, logs)? |
| **D**enial of Service | Can availability be impacted (resource exhaustion, driver crashes, infinite loops)? |
| **E**levation of Privilege | Can guest code gain host privileges, or user-mode gain kernel-mode? |

For a hypervisor product, special focus areas:
- **VM escape** (guest-to-host privilege escalation via VMF, virtio, IVSHMEM)
- **Driver vulnerabilities** (kernel-mode code reachable from user-mode IOCTLs)
- **Web management surface** (HvWeb authentication, injection, CSRF)
- **Supply chain** (build process integrity, third-party components, code signing)
- **Shared memory** (IVSHMEM data integrity, race conditions, bounds checking)

**Output files:**
- `05_threat_model\index.md` (STRIDE summary matrix and overall risk landscape)
- `05_threat_model\threat_model_vmf_core.md`
- `05_threat_model\threat_model_drivers.md`
- `05_threat_model\threat_model_network.md`
- `05_threat_model\threat_model_web.md`
- `05_threat_model\threat_model_guest_escape.md`
- `05_threat_model\threat_model_supply_chain.md`
- `05_threat_model\threat_model_deployment.md`

**Agent prompt (copy into fresh chat):**

This prompt incorporates the structure from Fabric's `create_threat_model` pattern:

```
You are a security threat modeler specializing in hypervisor and virtualization systems.
Follow the structured threat modeling approach below (based on Fabric's create_threat_model
pattern, adapted for hypervisor systems).

Read these analysis documents:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\01_artifact_registry\ (all files)

For each threat model file, use this structure:

## System Description
Brief description of the component/boundary being modeled and its role in the system.

## Assets
What valuable assets does this component handle or protect? (data, keys, privileges, hardware)

## Trust Boundaries
Which trust boundaries are relevant? List each with the trust levels on each side.

## Threat Analysis (STRIDE)
For each STRIDE category, enumerate threats:

### Spoofing
- **T-XXX-001**: [Threat title]
  - Scenario: [Concrete attack description]
  - Affected component(s): [names]
  - Affected interface(s): [from Step 4 interface map]
  - Likelihood: Low/Medium/High
  - Impact: Low/Medium/High/Critical
  - Existing controls: [what mitigations exist today, if any]
  - Recommended mitigation: [specific action]

(Repeat for Tampering, Repudiation, Information Disclosure, Denial of Service,
Elevation of Privilege)

## Attack Tree Summary
For each High/Critical threat, provide a brief attack tree:
1. Attacker goal
2. Required preconditions
3. Attack steps
4. Required attacker capability (network access, local user, guest VM code execution, etc.)

## Hypervisor-Specific Focus
Pay SPECIAL attention to:
- VM escape vectors (VMF call handling, virtio device emulation, IVSHMEM)
- Kernel driver attack surface (IOCTL handling, memory mapping)
- Web management surface (HvWeb: auth bypass, injection, CSRF, WebSocket)
- Build/supply chain (third-party binaries, code signing, build integrity)

## Harmonised Standard Threat Cross-Reference
For each threat you identify, cross-reference it against the threat catalogs in the
CRA harmonised standards. Read the threat sections from:

EN 304 635 (Virtualisation/Container) — §4.4.2 Hypervisor threats:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
  Focus on §4.4.2.1 (Hyper Type I threats), §4.4.2.2 (Hyper Type II threats),
  §4.4.2.3 (Orchestration/Management threats).

EN 304 626 (Operating Systems) — Annex C.4 Threats:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf
  Focus on threats: TH-UEVU, TH-KEVU, TH-UAPP, TH-UAPS, TH-UAPN, TH-UADT,
  TH-PDOS, TH-DDOS, TH-MQSE, TH-LEAK.

For each threat entry in the output, add a line:
  - EN reference: [EN 304 635 §4.4.2.x threat name] or [EN 304 626 TH-xxxx] or "No direct EN mapping"

In the index.md file, include a coverage matrix showing:
- Which EN 304 635 §4.4.2 threats are covered by identified STRIDE threats
- Which EN 304 626 Annex C.4 threats (TH-*) are covered
- Any EN threats NOT covered by the STRIDE analysis (gaps to investigate)

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Human interaction:** None required for generation. After generation, run the adversarial review validation (Step 5-review below).

#### Step 5 Validation: BMAD Adversarial Review of Threat Model

**Goal:** Apply BMAD's adversarial review technique to the STRIDE threat model output, forcing a second-pass thoroughness check that catches blind spots and gaps.

**Method:** BMAD adversarial review mandates that the reviewer **must** find issues — "zero findings triggers a halt." This is a natural fit for threat modeling, where completeness is critical.

1. Open a **fresh chat session** (or use the BMAD custom security agent from Step 0b)
2. Instruct the agent to perform an adversarial review of the Step 5 output:

```
You are performing a BMAD adversarial review of a STRIDE threat model for a
hypervisor system. The core rule: you MUST find issues. No "looks good" allowed.
Adopt a cynical stance — assume the threat model has gaps and find them.

Read the complete threat model:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)

Also read the EN standard threat catalogs for cross-reference:
- EN 304 635 §4.4.2 (Hypervisor threats): EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
- EN 304 626 Annex C.4 (OS threats): EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf

For each finding, rate severity (HIGH/MEDIUM/LOW) and provide:
1. What is missing or wrong
2. Why it matters for a CRA Important Class 2 product
3. Specific recommendation to fix it

Focus your adversarial review on:
- Missing threat scenarios (what attack vectors are NOT modeled?)
- EN standard threats (§4.4.2 / TH-*) that have no STRIDE mapping
- Inconsistent severity ratings (is a Critical really Critical?)
- Missing attack trees for High/Critical threats
- Threats that assume mitigations exist but don't cite evidence
- Multi-hop attack paths that cross multiple trust boundaries
- Supply chain and build integrity gaps

Write findings to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\adversarial_review.md
```

3. Review the adversarial findings — dismiss noise, incorporate valid findings back into the threat model files before proceeding to Step 5b

**Human interaction:** Review adversarial findings (~15-20 min). Expect false positives — the adversarial stance intentionally over-reports to force attention. You decide what's real.

---

### Step 5b: Generate Threagile Model and Risk Report

**Goal:** Translate the architecture and threat analysis into a Threagile YAML model, then run Threagile to produce automated risk assessments and architectural threat diagrams.

**Tools:** **Threagile** (threat-modeling-as-code). The AI agent generates the YAML; Threagile CLI produces the reports.

**Input:**
- Component documentation from Step 3 (`03_component_documentation\*.md`) — especially the "Data Flow Summary" and "Trust Boundary Position" sections
- Interface map from Step 4 (`04_interface_map\*.md`)
- STRIDE threat model from Step 5 (`05_threat_model\*.md`)

**Method:**

This step has two parts:

**Part A — Agent generates `threagile.yaml` (AI session):**

The agent reads the component docs and interface maps, then outputs a valid Threagile model file defining:
- `technical_assets` — one per component (with type, size, technology, confidentiality/integrity/availability ratings)
- `trust_boundaries` — host kernel, host user-mode, guest VMs, network DMZ, web UI
- `communication_links` — all interfaces from Step 4 mapped as data flows between assets
- `shared_runtimes` — IVSHMEM, VMF framework shared across products
- `data_assets` — configuration data, VM images, credentials, logs

**Part B — Run Threagile CLI (shell command, no AI needed):**

```bash
# From the security_assessment directory:
docker run --rm -v "%cd%\05b_threagile:/app/work" threagile/threagile \
  -model /app/work/threagile.yaml \
  -output /app/work/output
```

Or without Docker (if Threagile binary is installed):
```bash
threagile -model 05b_threagile\threagile.yaml -output 05b_threagile\output
```

Threagile will generate:
- `report.pdf` — comprehensive risk report with diagrams
- `risks.json` — machine-readable risk findings
- `data-flow-diagram.png` — architectural data-flow diagram showing trust boundaries
- `risks.xlsx` — spreadsheet of all identified risks

**Output files:**
- `05b_threagile\threagile.yaml` (agent-generated model)
- `05b_threagile\threagile_report.md` (agent-written summary of Threagile output)
- `05b_threagile\output\` (Threagile-generated reports and diagrams)

**Agent prompt for Part A (copy into fresh chat):**
```
You are a security architect generating a Threagile threat model YAML file for the
acontis hypervisor product family.

Read these documents:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\index.md

Generate a valid Threagile YAML model file (threagile.yaml) that maps the acontis hypervisor
system architecture. The YAML must follow the Threagile schema
(see https://threagile.io for schema documentation).

Include these sections in the YAML:

threagile_version: 1.0.0

title: "acontis Hypervisor Security Threat Model"

business_overview:
  description: Multi-product hypervisor family for real-time virtualization
  criticality: mission-critical

technical_overview:
  description: (summarize from component docs)

trust_boundaries:
  Map these zones (from the interface map):
  - host-kernel (VMF core, drivers — highest privilege)
  - host-usermode (RtosLib, RtosService, SystemManager)
  - guest-vm (VxWorks, CE, RTOS-32, Linux guests — untrusted relative to host)
  - network-zone (HvWeb, MQTT, management interfaces)
  - build-infrastructure (build servers, signing, third-party)

technical_assets:
  One entry per major component. For each, set:
  - type, size, technology, tags
  - confidentiality, integrity, availability ratings
  - whether it processes or stores sensitive data

communication_links:
  One entry per interface from the interface map. For each, set:
  - source and target technical_asset
  - protocol, authentication, encryption
  - data_assets_sent and data_assets_received
  - whether it crosses a trust boundary

data_assets:
  - VM disk images, configuration files, credentials/keys, management API tokens,
    log data, IVSHMEM shared memory regions, VMF call parameters

Additionally, encode the EN 304 635 security objectives as tags or custom attributes
on each technical_asset to enable traceability. The twelve security objectives from
EN 304 635 §4.5 are:
  - Isolation (§4.5.2)
  - Integrity Protection (§4.5.3)
  - Authentication (§4.5.4)
  - Authorization (§4.5.5)
  - Confidentiality Protection (§4.5.6)
  - Availability and Resilience (§4.5.7)
  - Logging (§4.5.8)
  - Patches and Updates (§4.5.9)
  - Secure Configuration and Default (§4.5.10)
  - Data Minimization (§4.5.11)
  - Time Synchronization (§4.5.12)

For each technical_asset, add tags indicating which EN 304 635 security objectives
apply (e.g., tags: [en635-isolation, en635-integrity, en635-auth]).
For Linux host OS assets, additionally tag with applicable EN 304 626 technical
requirements (e.g., tags: [en626-TR-MISO, en626-TR-MSAF, en626-TR-LMII]).

Read the harmonised standard PDFs for reference:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf

Write the YAML file to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\threagile.yaml

After writing the YAML, also create a brief summary file:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\threagile_report.md
documenting: how many technical assets, trust boundaries, communication links, and
data assets were modeled, and any assumptions or simplifications made.

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Shell command for Part B (run after Part A completes):**
```bash
cd C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment
docker run --rm -v "%cd%\05b_threagile:/app/work" threagile/threagile -model /app/work/threagile.yaml -output /app/work/output
```

**Human interaction:** Minimal. If the Threagile run fails with a YAML validation error, either fix the YAML manually or paste the error message back into a fresh agent session with the instruction to fix the YAML file. Expect 0-2 rounds of correction on the first run.

---

### Step 6: Risk Assessment and Recommendations

**Goal:** Consolidate all findings — STRIDE threat model (Step 5) and Threagile automated analysis (Step 5b) — into a unified, scored risk register with prioritized remediation recommendations.

**Input:**
- STRIDE threat model from Step 5 (`05_threat_model\*.md`)
- Threagile output from Step 5b (`05b_threagile\output\risks.json` and `report.pdf`)
- Product-artifact map from Step 2 (`02_product_artifact_map\*.md`)

**Method:**
1. Merge findings from both sources: the STRIDE analysis (agent-generated, hypervisor-focused) and the Threagile report (automated, schema-driven). De-duplicate threats that appear in both; note where they agree or disagree on severity.
2. For each threat, compute risk score: **Risk = Likelihood × Impact**

   | | Impact: Low (1) | Impact: Medium (2) | Impact: High (3) | Impact: Critical (4) |
   |---|---|---|---|---|
   | **Likelihood: High (3)** | 3 | 6 | 9 | 12 |
   | **Likelihood: Medium (2)** | 2 | 4 | 6 | 8 |
   | **Likelihood: Low (1)** | 1 | 2 | 3 | 4 |

   Risk levels: **Critical** (9-12), **High** (6-8), **Medium** (4-5), **Low** (1-3)

3. Cross-reference STRIDE threat IDs with Threagile risk IDs — note coverage gaps (threats found by one method but not the other)
4. Aggregate per-product risk profiles using the product-artifact map
5. Identify the top-10 highest-risk items across all products
6. Produce prioritized remediation recommendations grouped by effort level:
   - **Quick wins** (configuration changes, input validation additions)
   - **Medium effort** (code changes, additional authentication)
   - **Major effort** (architectural changes, redesign of trust boundaries)

**Output files:**
- `06_risk_assessment\index.md` (executive summary)
- `06_risk_assessment\risk_matrix.md` (full scored register, sorted by risk score)
- `06_risk_assessment\per_product_risk.md` (risk profile per product)
- `06_risk_assessment\recommendations.md` (prioritized actions)

**Agent prompt (copy into fresh chat):**
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

Merge and de-duplicate findings from both sources. For each identified threat:
1. Score: Risk = Likelihood (1-3) × Impact (1-4). Levels: Critical(9-12), High(6-8), Medium(4-5), Low(1-3)
2. Map to affected product(s)
3. Identify existing mitigations (if mentioned in component docs) vs. gaps
4. Note the source(s): STRIDE-only, Threagile-only, or both

Produce:
- index.md: Executive summary (total threats, critical/high/medium/low counts,
  top-5 risks, overall posture assessment). Include a section comparing
  STRIDE vs Threagile coverage: what each method found that the other missed.
- risk_matrix.md: Full risk register table sorted by score descending.
  Columns: Threat ID | Source (STRIDE/Threagile/Both) | Category | Description |
  Component | Product(s) | Likelihood | Impact | Risk Score | Risk Level |
  Existing Mitigation | Gap
- per_product_risk.md: For each product, list its risk profile
  (count of threats per level, unique attack surfaces, overall risk posture)
- recommendations.md: Prioritized remediation actions grouped as:
  Quick Wins (config/validation), Medium Effort (code changes), Major Effort (architecture).
  Each recommendation references specific threat IDs.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\
```

**Human interaction:** None required for generation. After generation, run the adversarial review validation (Step 6-review below).

#### Step 6 Validation: BMAD Adversarial Review of Risk Assessment

**Goal:** Apply BMAD's adversarial review to the consolidated risk assessment, checking for scoring inconsistencies, missing mitigations, and recommendations that don't match the actual risk landscape.

**Method:**

1. Open a **fresh chat session** (or use the BMAD custom security agent from Step 0b)
2. Instruct the agent:

```
You are performing a BMAD adversarial review of a consolidated security risk
assessment for a hypervisor product family. The core rule: you MUST find issues.

Read the complete risk assessment:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\ (all files)

Also read the threat model it was derived from:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)

For each finding, rate severity (HIGH/MEDIUM/LOW) and categorize:

Focus your adversarial review on:
- Scoring consistency: Are similar threats scored differently? Are Likelihood/Impact
  ratings justified or arbitrary?
- Missing threats: Are there STRIDE or Threagile findings that didn't make it
  into the consolidated register?
- Mitigation gaps: Do recommendations actually address the root cause?
- Product coverage: Are all 7 products covered proportionally, or are some neglected?
- Prioritization bias: Are "Quick Wins" truly quick? Are "Major Effort" items
  correctly classified?
- CRA compliance: Would a notified body find this assessment sufficient for an
  Important Class 2 product?
- Actionability: Can a developer actually implement each recommendation?

Write findings to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\adversarial_review.md
```

3. Review findings and update the risk assessment files as needed before proceeding to Steps 7-8

**Human interaction:** Review adversarial findings (~15-20 min). Update risk scores and recommendations where the review identifies legitimate issues.

---

### Step 7a: Semgrep Built-in Scans

**Goal:** Run Semgrep's standard security rule packs against the source code to find known vulnerability patterns automatically.

**Tools:** **Semgrep** (SAST). No AI agent needed for this step — it's a direct CLI execution.

**Input:**
- Source code in `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\`

**Method:**

Run Semgrep with curated rule packs targeting each major language/framework in the codebase. Execute these commands from the `rtv` directory:

```bash
cd C:\Users\s.zintgraf.ACONTIS\PROJ\rtv

# C/C++ security rules — VMF core, drivers, RtosLib
semgrep --config=p/c-lang-security --include="*.c" --include="*.cpp" --include="*.h" \
  Framework/ Windows/Source/Driver/ Windows/Source/RtosLib/ \
  Linux/Source/ LxWin/Source/ Common/ \
  --json -o ../ai-knowhow/bmad/security_assessment/07_semgrep/raw_c_results.json

# .NET / C# security rules — HvWeb, SystemManager, HvDeviceMgr
semgrep --config=p/csharp-security --include="*.cs" \
  Hypervisor/Source/HvWeb/ Hypervisor/Source/HvDeviceMgr/ \
  Windows/Source/SystemManager/ \
  --json -o ../ai-knowhow/bmad/security_assessment/07_semgrep/raw_csharp_results.json

# OWASP Top 10 rules — web-facing components
semgrep --config=p/owasp-top-ten --include="*.cs" --include="*.ts" --include="*.js" \
  Hypervisor/Source/HvWeb/ \
  --json -o ../ai-knowhow/bmad/security_assessment/07_semgrep/raw_owasp_results.json

# JavaScript/TypeScript rules — HvWeb Angular ClientApp
semgrep --config=p/javascript-security --include="*.ts" --include="*.js" \
  Hypervisor/Source/HvWeb/ClientApp/ \
  --json -o ../ai-knowhow/bmad/security_assessment/07_semgrep/raw_js_results.json
```

After running, use an agent session to convert the JSON results into a readable markdown summary.

**Output files:**
- `07_semgrep\raw_*.json` (raw Semgrep output — machine-readable)
- `07_semgrep\builtin_scan_results.md` (agent-generated human-readable summary)
- `07_semgrep\index.md` (overview with finding counts and severity breakdown)

**Agent prompt for summarization (copy into fresh chat after Semgrep runs complete):**
```
You are a security analyst summarizing Semgrep SAST scan results.

Read the Semgrep JSON output files at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\raw_*.json

For each finding, extract: rule ID, severity, file path, line number, message, and CWE (if present).
Group findings by severity (Error > Warning > Info) and by component area.
De-duplicate identical findings across rule packs.

Produce:
- index.md: Overview with total finding counts per severity and per component area.
  Include a table of which Semgrep rule packs were run and what they cover.
- builtin_scan_results.md: Full findings table grouped by component area.
  Columns: Severity | Rule ID | CWE | File | Line | Description | Component Area.
  Sort by severity descending, then by component.

Cross-reference with the threat model:
Read C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\index.md
For each Semgrep finding, note if it confirms or is related to a STRIDE threat ID.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\
```

**Human interaction:** None for running scans. If Semgrep reports errors about unsupported syntax in older C files, those can be safely ignored.

---

### Step 7b: Custom Semgrep Rules for Trust Boundaries

**Goal:** Have an AI agent write custom Semgrep rules that target the specific trust boundaries and interface patterns identified in Step 4, then run them against the codebase.

**Tools:** **Semgrep** (custom YAML rules) + AI agent (rule generation).

**Input:**
- Interface map from Step 4 (`04_interface_map\*.md`)
- Component documentation from Step 3 (`03_component_documentation\*.md`)
- Built-in scan results from Step 7a (`07_semgrep\builtin_scan_results.md`) — to avoid duplicating existing coverage

**Method:**

The agent reads the interface documentation to understand the exact function signatures, parameter types, and calling patterns at each trust boundary, then writes Semgrep rules to detect:

| Trust Boundary | Custom Rules To Generate |
|---|---|
| **VMF call dispatch** | Flag `vmfCall*` handlers that read size/length/offset parameters without bounds checking before use |
| **Driver IOCTLs** | Flag IOCTL handlers that use `ProbeForRead`/`ProbeForWrite` or `copy_from_user` with user-supplied length without prior validation |
| **IVSHMEM shared memory** | Flag shared memory offset/index accesses without bounds validation against region size |
| **HvWeb API endpoints** | Flag controller actions missing `[Authorize]` attributes; flag string concatenation in queries |
| **Configuration parsing** | Flag config file reads where parsed values are used as sizes/offsets without range checking |

**Output files:**
- `07_semgrep\custom_rules\vmf_call_validation.yaml`
- `07_semgrep\custom_rules\ioctl_input_validation.yaml`
- `07_semgrep\custom_rules\ivshmem_bounds.yaml`
- `07_semgrep\custom_rules\web_injection.yaml`
- `07_semgrep\custom_scan_results.md` (results from running these rules)

**Agent prompt (copy into fresh chat):**
```
You are a security engineer writing custom Semgrep rules for the acontis hypervisor product family.

Read the interface documentation to understand the exact patterns at each trust boundary:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)

Also read the existing Semgrep results to avoid duplicating built-in rule coverage:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\builtin_scan_results.md

Read key source files at trust boundaries to understand function signatures and patterns:
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Common\All\SDK\Inc\vmfInterface.h
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Windows\Source\Driver\RtosDrv\Vmf\ (vmfDrvInterface files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Linux\Source\Driver\hrtosdrv\Vmf\ (vmfDrvInterface files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Framework\Source\Core\ (IVSHMEM-related files)

Write Semgrep rules (YAML format) for these trust boundaries:

1. vmf_call_validation.yaml — Detect VMF call handlers that use size/length/offset
   parameters from the call arguments without bounds checking before memory operations.
   Look at actual vmfCall* function patterns in the source to write accurate patterns.

2. ioctl_input_validation.yaml — Detect IOCTL dispatch handlers that pass user-supplied
   buffer lengths to ProbeForRead/ProbeForWrite/memcpy/copy_from_user without prior
   validation. Target both Windows (RtosDrv) and Linux (hrtosdrv) driver patterns.

3. ivshmem_bounds.yaml — Detect shared memory offset/index accesses that lack bounds
   checking against the region size. Look at actual IVSHMEM access patterns in
   Framework/Source/Core/.

4. web_injection.yaml — For HvWeb (.NET/C# + Angular/TypeScript): detect controller
   actions missing [Authorize], string concatenation in database queries, unsanitized
   user input in command execution, and missing CSRF tokens.

Each rule YAML file should follow Semgrep rule syntax:
rules:
  - id: rtv-xxx-001
    patterns:
      - pattern: ...
    message: ...
    severity: WARNING or ERROR
    languages: [c, cpp] or [csharp] or [typescript]
    metadata:
      cwe: CWE-XXX
      confidence: HIGH or MEDIUM
      references:
        - (link to relevant interface map section)

Write the rule files to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\custom_rules\

After writing the rules, provide the shell commands to run them. Example:
  semgrep --config=07_semgrep/custom_rules/ --include="*.c" --include="*.cpp" rtv/ --json

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**After the agent generates rules, run them:**
```bash
cd C:\Users\s.zintgraf.ACONTIS\PROJ

# Run all custom rules against the full source tree
semgrep --config=ai-knowhow/bmad/security_assessment/07_semgrep/custom_rules/ \
  --include="*.c" --include="*.cpp" --include="*.h" --include="*.cs" --include="*.ts" \
  rtv/ \
  --json -o ai-knowhow/bmad/security_assessment/07_semgrep/raw_custom_results.json
```

Then run the same summarization agent prompt from Step 7a on the custom results, writing to `07_semgrep\custom_scan_results.md`.

**Human interaction:** Minimal. The agent-generated Semgrep rules may need 1-2 rounds of tuning if they produce too many false positives or if the pattern syntax doesn't match the actual code patterns. Paste Semgrep errors back into a fresh agent session to fix.

---

### Step 7c: AI-Driven Code Vulnerability Deep-Dive

**Goal:** Targeted manual (agent-driven) deep-dive into the highest-risk code areas that automated tools (Semgrep) cannot fully analyze — cross-function logic, complex race conditions, architectural weaknesses.

**Input:**
- Top threats from `06_risk_assessment\risk_matrix.md` (Critical and High items)
- Semgrep findings from Steps 7a-7b (`07_semgrep\*.md`) — to focus on gaps not covered by SAST
- Source code in `rtv\`

**Method:**
For each Critical/High threat **not already covered by Semgrep findings**, the agent reads the specific source files involved and looks for issues that require cross-function or cross-file reasoning:
- Buffer overflows involving size calculations across multiple function calls
- Integer overflows in size calculations before memory allocation
- Race conditions in shared memory access (IVSHMEM) — TOCTOU patterns
- Use-after-free patterns in driver code (object lifetime across callbacks)
- Authentication/authorization bypasses in HvWeb (logic flaws, not just missing attributes)
- Complex injection vulnerabilities (second-order injection, path traversal)
- Hardcoded credentials or keys
- Insecure default configurations
- Logic errors in VMF call parameter validation

**Output:** Append findings to the relevant `05_threat_model\threat_model_*.md` files as a "## Code-Level Findings" section, and update `06_risk_assessment\risk_matrix.md` with refined scores.

**Agent prompt template (copy into fresh chat, one session per high-risk area):**

This prompt incorporates the approach from Fabric's `find_vulnerabilities` pattern:

```
You are a security code auditor performing a deep vulnerability analysis on the
acontis hypervisor product family. This analysis focuses on vulnerabilities that SAST tools
like Semgrep CANNOT find — cross-function logic, race conditions, architectural flaws.

Read the threat model for [AREA]:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\threat_model_[AREA].md

Read the Semgrep results to see what has ALREADY been found by automated scanning:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\builtin_scan_results.md
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\custom_scan_results.md

For each Critical or High threat NOT already confirmed by a Semgrep finding, read
the specific source files cited and perform deep analysis looking for:

1. Cross-function data flow issues (tainted input flowing through multiple functions
   before reaching a sensitive operation without validation at any point)
2. Race conditions (TOCTOU in shared memory, concurrent access to shared state)
3. Object lifetime issues (use-after-free, dangling pointers across callbacks)
4. Logic flaws in authentication/authorization (correct attributes present but
   bypassable through parameter manipulation or state confusion)
5. Complex injection chains (second-order injection, path traversal combining
   multiple user inputs)
6. Cryptographic misuse (weak algorithms, predictable IVs, key reuse)
7. Error handling that leaks sensitive information or fails open

Follow Fabric's find_vulnerabilities output structure:
For each finding:
- Vulnerability title
- CWE classification
- Severity: Critical/High/Medium/Low
- Affected file(s) and line number(s) — cite EXACT paths and lines
- Description: what the vulnerability is and how it could be exploited
- Proof of concept: concrete attack scenario
- Recommended fix: specific code change

Append a "## Code-Level Findings" section to the existing threat model file at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\threat_model_[AREA].md

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Human interaction:** Choose which high-risk areas to audit first based on the risk matrix from Step 6.

---

### Step 8: Compliance Consolidation — From Findings to Formal Risk Register

**Goal:** Transform the technical findings from Steps 1–7 into formal risk assessment documents suitable for CRA compliance and (for the Hypervisor) review by a notified body. This step produces the bridge between the deep technical investigation performed above and the structured risk register formats used by acontis.

**Why this step is necessary:**

Steps 1–7 produce rich technical evidence (architecture documentation, STRIDE threat models, Threagile reports, Semgrep findings, code-level vulnerability analysis), but this evidence is in free-form markdown and JSON — not in the structured formats required for CRA conformity assessment. This step translates findings into the QuBA-libre format required for Important Class 2 products:

- **RTOSVisor (Type I Hypervisor)** → **QuBA-libre format** (full assessment, mandatory for Important Class 2 notified body review)
- **LxWin (Type II Hypervisor, representative)** → **QuBA-libre format** (full assessment, representative for all Type II products)
- **Other Type II products** (VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32) → **Delta assessment** referencing LxWin findings, documenting only product-specific guest integration differences

**Input:**
- Risk register from Step 6 (`06_risk_assessment\*.md`)
- Threagile risk data from Step 5b (`05b_threagile\output\risks.json`)
- Semgrep findings from Step 7 (`07_semgrep\*.md`)
- Code-level findings from Step 7c (appended to `05_threat_model\*.md`)
- Component documentation from Step 3 (`03_component_documentation\*.md`) — especially §10 (EN requirement mapping)
- Interface and trust boundary map from Step 4 (`04_interface_map\*.md`)
- QuBA-libre reference template (`security_assessment\QuBA-libre\QuBA-libre.xlsx`)
- AT9310 template (`security_assessment\QuBA-libre\Template AT9310 'AT9310_Risk-Assessment-Template'.xltx`)
- AT3350 EC-Master example (`security_assessment\QuBA-libre\Risk Assessment AT3350 'AT3350_EC-Master_Risk_Assessment'.xlsx`)
- **EN 304 635** (`EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf`) — §5.1.1, §5.1.3, §6.3.1, §4.7, Annex B
- **EN 304 626** (`EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf`) — §5.2, Annex C.2, C.4, C.6

**Method — Part A: Hypervisor QuBA-libre Consolidation**

The AI agent reads all findings and maps them to the QuBA-libre methodology:

1. **Questionnaire answer recommendations** (`hypervisor_quba_inputs.md`): For each QuBA-libre question (QI1–QI16 impact questions, QA1–QA21 attack potential questions), derive the appropriate answer from the technical findings:
   - QI questions: Determine worst-case impact ratings from the STRIDE threat model and risk matrix
   - QA questions: Characterize the Hypervisor's actual attack surface from the interface map and Semgrep findings (connectivity, exposed services, debug interfaces, supply chain)
   - Include rationale text for each answer, citing specific findings from Steps 4–7

2. **Hypervisor-specific attack step extensions** (`hypervisor_attack_steps.md`): QuBA-libre's built-in 42 attack steps (AS1–AS41) are generic and do not cover Hypervisor-specific vectors. Generate additional attack step definitions for:
   - VMF call exploitation (guest→host privilege escalation via crafted VMF calls)
   - Kernel driver IOCTL abuse (RtosDrv, RtosVnet, RtosPnp)
   - IVSHMEM shared memory corruption (cross-VM data injection)
   - HvWeb management interface attacks (REST API abuse, WebSocket hijacking, Angular XSS)
   - Guest-to-host escape via virtio device emulation
   - MQTT message injection (inter-component communication spoofing)
   - Installer/MSI privilege escalation during deployment
   - Linux kernel module loading attacks on the host

   For each new attack step, define: Description, Required Attack Potential (RAP) factors (Elapsed Time, Expertise, Knowledge of TOE, Window of Opportunity, Equipment), and relevant CRA Annex I requirements.

3. **Countermeasure catalog extensions** (`hypervisor_countermeasures.md`): For each high/critical risk from Step 6, propose countermeasures in QuBA-libre format:
   - Countermeasure ID and description
   - Mapping to IEC 62443 or ETSI EN 303 645 controls where applicable
   - RAP reduction factors (which attack potential factors are reduced and by how much)
   - Damage scenario transformations (which damage scenarios are removed or reduced)
   - Implementation status: Existing (already in code) vs. Recommended (new)

4. **Deployment assumptions** (`hypervisor_assumptions.md`): Document security assumptions derived from the threat model:
   - Which threats are mitigated by customer deployment constraints (network segmentation, physical access)
   - Stakeholder assignment (acontis vs. OEM vs. end-user responsibility)
   - Conditions under which risk levels change (e.g., "if web management is exposed to the internet, re-classify web threats as Critical")

5. **CRA Annex I gap analysis** (`cra_annex_i_checklist.md`): Walk through CRA Annex I Part I (2) requirements (a)–(m) and for each:
   - State whether the requirement is covered by identified countermeasures
   - Cite specific findings, countermeasures, or assumptions that provide coverage
   - Flag gaps where no countermeasure exists

**Method — Part C: Harmonised Standard Compliance Matrices**

This part produces the compliance evidence that maps findings to the EN 304 635 and EN 304 626 harmonised standard requirements — the documents a notified body will assess against.

6. **EN 304 635 Hypervisor requirement compliance matrix** (`en304_635_compliance.md`): For each requirement in EN 304 635 §5.1.1 (Hypervisor Requirements), assess compliance:

   | Requirement Section | Requirement ID | Applicable? | Status | Evidence | Gaps |
   |---|---|---|---|---|---|
   | §5.1.1.1.1 VM Isolation | ... | Yes | Met/Partial/Not Met | cite Step 3/5/7 findings | what's missing |
   | §5.1.1.1.2 Control Plane Isolation | ... | Yes | ... | ... | ... |
   | §5.1.1.1.3 Network Plane Separation | ... | Yes | ... | ... | ... |
   | §5.1.1.2.1 Boot chain integrity | ... | ... | ... | ... | ... |
   | ... through §5.1.1.10 Data Minimization | ... | ... | ... | ... | ... |

   Additionally, for the M&O System (HvWeb), assess §5.1.3 requirements (Authentication, Authorization, Secure Config, Communication Security, Integrity, Patches/Updates).

   For each requirement at Basic/Elevated/Advanced level, indicate which level the Hypervisor currently meets and what would be needed for the next level.

7. **EN 304 635 assessment case preparation** (`en304_635_assessment_cases.md`): EN 304 635 §6.3.1 defines ~70 specific assessment cases (AC-H-*) that a notified body will use. For each assessment case:
   - State the assessment case ID and title (e.g., AC-H-VM-ISO-001: "VM Isolation Assessment")
   - Describe what evidence the notified body will require
   - Map to specific findings from Steps 3–7 that serve as evidence
   - Flag assessment cases where evidence is insufficient or missing
   - Note the requirement class (Basic/Elevated/Advanced) and whether the Hypervisor's target SCL meets it

   Group by security objective: Isolation, Integrity, Authentication, Authorization, Confidentiality, Availability, Logging, Updates, Configuration, Data Minimization.

8. **EN 304 626 OS requirement compliance matrix** (`en304_626_compliance.md`): For each Technical Requirement (TR-*) in EN 304 626 §5.2, assess compliance of the Linux host OS components:

   | Requirement | Mitigations | Applicable? | Status | Evidence | Gaps |
   |---|---|---|---|---|---|
   | TR-NKEV: No known exploitable vulns | MI-KEVD, MI-KEVA, MI-KEVM, MI-KEVT, MI-SCAN | Yes | ... | ... | ... |
   | TR-SSDD: Secure design/development | MI-SSCA, MI-FZ95, MI-IMSL, MI-BTIN, MI-SCFS | Yes | ... | ... | ... |
   | TR-MISO: Memory isolation | MI-MMAC, MI-CCON, MI-UCON, MI-PMSC, MI-TRMD | Yes | ... | ... | ... |
   | TR-MSAF: Memory safety | MI-MSAF-1 through MI-MSAF-6 | Yes | ... | ... | ... |
   | ... through TR-VULH: Vulnerability handling | ... | ... | ... | ... | ... |

   For each TR-* requirement, list which specific mitigations (MI-*) are applicable and their implementation status.

9. **EN 304 626 risk factor scoring** (`en304_626_risk_factors.md`): Score each of the 18 risk factors (RF-*) from EN 304 626 Annex C.2 based on the product characteristics identified in Steps 1-4:

   | Risk Factor | ID | Score | Rationale |
   |---|---|---|---|
   | Number of User Accounts | RF-NUSR | ... | Based on HvWeb user management analysis |
   | User Account Concurrency | RF-CUSR | ... | ... |
   | Potential for PII Collection | RF-PPII | ... | Based on data flow analysis |
   | Sensitivity of Data Stored | RF-SNDS | ... | Based on VM image, credential analysis |
   | ... through Support/Updates | RF-SUPP | ... | Based on product lifecycle analysis |

   Map the scored risk factors to the appropriate Security Profile (SP-*) and determine the Security Assurance Level per EN 304 626 §C.6.

10. **EN 304 635 risk factor scoring** (`en304_635_risk_factors.md`): Similarly, apply the risk assessment methodology from EN 304 635 Annex B:
    - Score risk factors per Annex B.2
    - Calculate Likelihood and Impact scores per Annex B.3
    - Apply the Risk Matrix from Annex B.4
    - Determine the Security Category Level (SCL) per §4.7
    - Map to Use Case risk evaluation (Annex B.5.1 for Hypervisor Type I/II)

**Method — Part A2: LxWin QuBA-libre Consolidation (Type II Representative)**

Apply the same QuBA-libre methodology as Part A, but for LxWin as the representative Type II Hypervisor product:

1. **Reuse shared findings**: The VMF Framework Core, Windows drivers, and user-mode libraries are identical between LxWin and RTOSVisor's VMF layer. Reference the RTOSVisor QuBA-libre inputs for these shared components rather than duplicating.
2. **Type II-specific differences**: Document the Windows host OS trust model (EN 304 635 §4.4.2.2 Type II threats), Windows driver attack surface, and LxWin-specific guest integration (RT-Linux guest).
3. **LxWin-specific questionnaire answers** (`lxwin_quba_inputs.md`): Where LxWin differs from RTOSVisor (e.g., no HvWeb, no Linux host OS, different deployment model), provide LxWin-specific answers.
4. **LxWin-specific attack steps and countermeasures** as needed.

**Method — Part B: Type II Product Delta Assessments**

For VxWin, CeWin, VmfWin, RTOS32Win, and EC-WinRTOS-32, generate a delta assessment document (`type2_product_deltas.md`) that identifies product-specific differences from the LxWin baseline:

1. For each product, identify guest OS integration components that differ from LxWin (e.g., VxWorks BSP for VxWin, WinCE runtime for CeWin, RTOS-32 loader for RTOS32Win, EtherCAT integration for EC-WinRTOS-32)
2. Document any additional attack surfaces introduced by the product-specific guest integration
3. Flag risks from the LxWin assessment that do NOT apply to this product (reduced scope)
4. Flag risks that are unique to this product and not covered by the LxWin assessment
5. Reference the LxWin QuBA-libre assessment for all shared components (VMF Core, Windows drivers, user-mode libraries)

**Output files:**
- `08_compliance_consolidation\index.md` (consolidation strategy, format rationale, format comparison table)
- `08_compliance_consolidation\hypervisor_quba_inputs.md` (QuBA-libre questionnaire answer recommendations with rationale)
- `08_compliance_consolidation\hypervisor_attack_steps.md` (Hypervisor-specific attack step extensions)
- `08_compliance_consolidation\hypervisor_countermeasures.md` (countermeasure catalog extensions)
- `08_compliance_consolidation\hypervisor_assumptions.md` (deployment assumptions and stakeholder assignments)
- `08_compliance_consolidation\lxwin_quba_inputs.md` (LxWin-specific QuBA-libre questionnaire answers)
- `08_compliance_consolidation\type2_product_deltas.md` (per-product delta assessments for VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32)
- `08_compliance_consolidation\cra_annex_i_checklist.md` (CRA Annex I coverage gap analysis)
- `08_compliance_consolidation\en304_635_compliance.md` (EN 304 635 Hypervisor + M&O requirement compliance matrix)
- `08_compliance_consolidation\en304_635_assessment_cases.md` (EN 304 635 §6.3.1 assessment case evidence mapping)
- `08_compliance_consolidation\en304_626_compliance.md` (EN 304 626 OS technical requirement compliance matrix)
- `08_compliance_consolidation\en304_626_risk_factors.md` (EN 304 626 Annex C.2 risk factor scoring and security profile)
- `08_compliance_consolidation\en304_635_risk_factors.md` (EN 304 635 Annex B risk factor scoring and SCL determination)

**Agent prompt (copy into fresh chat — due to the scope of this step, it may require 2 sessions: one for Parts A+B, one for Part C):**
```
You are a CRA compliance specialist consolidating security findings from a
technical risk assessment into formal risk register formats for the
acontis hypervisor product family.

Read the following context:

QuBA-libre analysis (methodology reference):
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\QuBA-libre\QuBA-libre_analyzation.md

Consolidated risk register:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\06_risk_assessment\ (all files)

Threagile risk data:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\output\risks.json (if exists)
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\threagile_report.md

Interface and trust boundary map:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)

STRIDE threat model:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\ (all files)

Semgrep findings:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\index.md

Component documentation (with EN standard requirement mapping):
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)

Product-artifact mapping:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\02_product_artifact_map\ (all files)

AT3350 EC-Master example (for AT3350 format reference):
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\QuBA-libre\Risk Assessment AT3350 'AT3350_EC-Master_Risk_Assessment'.xlsx

CRA Harmonised Standards (read the relevant sections):
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf
  - §5.1.1 Hypervisor Requirements (for compliance matrix)
  - §5.1.3 M&O System Requirements (for HvWeb compliance)
  - §6.3.1 Assessment Cases AC-H-* (for assessment case preparation)
  - §4.7 Requirement Classes and Security Category Levels
  - Annex B Risk Assessment Methodology (for risk factor scoring)

C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf
  - §5.2 Technical Security Requirements TR-* (for Linux host compliance)
  - Annex C.2 Risk Factors RF-* (for risk factor scoring)
  - Annex C.4 Threats TH-* (for threat coverage verification)
  - Annex C.6 Security Profiles and Assurance Levels

ALL acontis hypervisor products are classified as CRA Important Class 2.
Full QuBA-libre assessments are produced for:
- RTOSVisor (Type I Hypervisor, Linux host)
- LxWin (Type II Hypervisor, Windows host — representative for all Type II products)
The remaining Type II products (VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32)
receive delta assessments referencing the LxWin findings.

Produce the following outputs:

--- Part A: QuBA-libre Consolidation (Hypervisor) ---

1. `08_compliance_consolidation\index.md` — strategy document explaining the
   assessment approach, explaining why QuBA-libre is used for all acontis hypervisor
   products (all are CRA Important Class 2), the rationale for
   full assessment on RTOSVisor + LxWin with delta assessments for other
   Type II products, and documenting the CRA Class 2 conformity assessment
   requirements (structured trust boundaries, Annex I traceability,
   systematic countermeasure management, assumption tracking). Include a
   section on how EN 304 635 and EN 304 626 relate to the assessment outputs.

2. `08_compliance_consolidation\hypervisor_quba_inputs.md` — for each QuBA-libre
   question (QI1-QI16, QA1-QA21), provide the recommended answer for the
   Hypervisor with rationale citing specific findings from the threat model,
   interface map, and Semgrep results.

3. `08_compliance_consolidation\hypervisor_attack_steps.md` — define 15-25
   Hypervisor-specific attack steps not covered by the standard QuBA-libre
   catalog. Each must include: ID, Name, Description, RAP factors, CRA
   Annex I mapping. Focus on: VMF call exploitation, driver IOCTL abuse,
   IVSHMEM corruption, HvWeb attacks, guest escape vectors, MQTT injection,
   installer privilege escalation, kernel module attacks.

4. `08_compliance_consolidation\hypervisor_countermeasures.md` — for each
   Critical/High risk, define countermeasures in QuBA-libre format with:
   ID, Description, IEC 62443 / ETSI EN 303 645 mapping, RAP reduction
   factors, damage scenario transformations, implementation status.

5. `08_compliance_consolidation\hypervisor_assumptions.md` — list all deployment
   assumptions that affect risk levels. For each: ID, Description, Stakeholder
   assignment (acontis / OEM / end-user), affected risks, condition under
   which assumption is invalid.

--- Part A2: LxWin QuBA-libre Consolidation (Type II Representative) ---

6. `08_compliance_consolidation\lxwin_quba_inputs.md` — apply the same QuBA-libre
   methodology as Part A but for LxWin. Reuse shared-component findings from
   RTOSVisor (VMF Core, Windows drivers). Document Type II-specific differences:
   Windows host trust model, EN 304 635 §4.4.2.2 Type II threats, LxWin guest
   integration. Provide LxWin-specific questionnaire answers where they differ.

--- Part B: Type II Product Delta Assessments ---

7. `08_compliance_consolidation\type2_product_deltas.md` — for each remaining
   Type II product (VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32), produce
   a delta assessment: what guest-integration-specific risks differ from LxWin,
   what risks do NOT apply, and reference the LxWin assessment for all shared
   components.

8. `08_compliance_consolidation\cra_annex_i_checklist.md` — for CRA Annex I
   Part I (2) items (a) through (m), state coverage status (Covered /
   Partially Covered / Gap), cite the specific countermeasures or assumptions
   providing coverage, and flag gaps requiring additional work.

--- Part C: Harmonised Standard Compliance Evidence ---

8. `08_compliance_consolidation\en304_635_compliance.md` — for EVERY requirement
   in EN 304 635 §5.1.1 (Hypervisor) and §5.1.3 (M&O System / HvWeb),
   produce a compliance row: Requirement ID | Section | Applicable (Y/N) |
   Status (Met / Partially Met / Not Met / Unknown) | Evidence (cite specific
   findings from Steps 3-7) | Gaps (what is missing). For each requirement,
   indicate the requirement class level (Basic/Elevated/Advanced) and what
   the product currently achieves.

9. `08_compliance_consolidation\en304_635_assessment_cases.md` — for each
   assessment case in EN 304 635 §6.3.1 (AC-H-VM-ISO-001 through
   AC-H-DM-002, approximately 70 cases), produce:
   Assessment Case ID | Title | Required Evidence | Available Evidence
   (cite Steps 3-7 findings) | Evidence Gaps | Recommendation.
   Group by security objective (Isolation, Integrity, Authentication, etc.).
   This document directly prepares the evidence package for a notified body.

10. `08_compliance_consolidation\en304_626_compliance.md` — for each Technical
    Requirement (TR-*) in EN 304 626 §5.2, assess compliance of the Linux
    host OS components: TR ID | Mitigations (MI-*) | Applicable | Status |
    Evidence | Gaps. Cover all TR-NKEV through TR-VULH.

11. `08_compliance_consolidation\en304_626_risk_factors.md` — score each of
    the 18 risk factors (RF-NUSR through RF-SUPP) from EN 304 626 Annex C.2
    based on product characteristics from Steps 1-4. Determine the Security
    Profile (SP-*) and Security Assurance Level per Annex C.6. Include the
    rationale for each score.

12. `08_compliance_consolidation\en304_635_risk_factors.md` — apply the EN 304 635
    Annex B risk assessment methodology: score risk factors per B.2, calculate
    Likelihood/Impact per B.3, apply the Risk Matrix from B.4, determine the
    Security Category Level (SCL) per §4.7, and map to the applicable Use Case
    risk evaluation from B.5.1 (Hypervisor Type I or Type II).

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

**Human interaction:** Review the generated QuBA-libre inputs before manually entering them into the QuBA-libre Excel workbook. The agent produces the *recommended answers and rationale* — a human must transfer these into the actual Excel file and verify the automated risk calculations. This is the primary human touchpoint in the entire plan.

---

## Execution Summary

| Step | Type | Sessions | Est. Duration | Depends On | Human Interaction |
|---|---|---|---|---|---|
| **0a: BMAD document-project** | **BMAD workflow** | **1 + 6 deep-dives** | **30-120 min** | **None** | **Select scan depth, confirm classification, choose deep-dive targets** |
| **0b: BMAD custom agent setup** | **Manual config** | **—** | **~10 min** | **None** | **One-time setup of `.customize.yaml`** |
| 1: Artifact Registry | AI agent | 1 | 15-30 min | None | None |
| 2: Product-Artifact Map | AI agent | 1 | 15-30 min | Step 1 | None |
| 3: Component Docs (Security Overlay) | AI agent | 6 (parallel) | 15-30 min each | Step 0a | Minimal (choose order) |
| 4: Interface Map | AI agent | 1 | 20-30 min | Step 3 | None |
| 5: STRIDE Threat Model (Fabric-enhanced) | AI agent | 1-2 | 30-45 min | Steps 3, 4 | None |
| **5-review: Adversarial Review of Threat Model** | **BMAD adversarial** | **1** | **15-25 min** | **Step 5** | **Review findings, dismiss noise (~15-20 min)** |
| 5b-A: Threagile YAML Generation | AI agent | 1 | 20-30 min | Steps 3, 4, 5 | None |
| 5b-B: Threagile CLI Execution | Shell command | — | 2-5 min | Step 5b-A | Fix YAML if validation fails (0-2 rounds) |
| 6: Risk Assessment (STRIDE + Threagile merged) | AI agent | 1 | 20-30 min | Steps 2, 5, 5b | None |
| **6-review: Adversarial Review of Risk Assessment** | **BMAD adversarial** | **1** | **15-25 min** | **Step 6** | **Review findings, update scores (~15-20 min)** |
| 7a: Semgrep Built-in Scans | Shell + AI agent | 1 | 10-20 min | None (can run in parallel with Steps 1-6) | None |
| 7b: Custom Semgrep Rules | AI agent + Shell | 1-2 | 30-45 min | Steps 4, 7a | Tune rules if needed (0-2 rounds) |
| 7c: AI Code Vulnerability Deep-Dive | AI agent | 2-5 (parallel) | 30-60 min each | Steps 6, 7a, 7b | Choose priority areas |
| **8a: Compliance Consolidation (Parts A+B)** | **AI agent** | **1** | **30-45 min** | **Steps 2, 4, 5, 5b, 6, 7** | **Review QuBA-libre inputs before Excel entry** |
| **8b: EN Standard Compliance (Part C)** | **AI agent** | **1** | **45-60 min** | **Steps 3, 4, 5, 6, 7, EN PDFs** | **Review compliance matrices and gap analysis** |

**Total estimated effort:** 12-16 agent sessions (Steps 0a + 1-6 + reviews + 7a-7b + 8a-8b), plus optional 2-5 sessions for Step 7c.
**Total estimated wall-clock time:** 7-10 hours for Steps 0-8 (with parallel Step 3 sessions and parallel Semgrep scans). Step 0a adds 30-120 min upfront but **reduces Step 3 duration** (security overlay only, not full architecture rediscovery).
**Human time required:** ~2-3.5 hours total (BMAD setup, reviewing adversarial findings, launching sessions, fixing Threagile YAML / Semgrep rules if needed, transferring QuBA-libre inputs into Excel workbook, reviewing EN compliance matrices).

### Parallelization Opportunities

Several steps can run concurrently to minimize wall-clock time:

```
Timeline:
├─ Step 0a: BMAD document-project (~60-120 min)  ← run first, provides baseline for Step 3
├─ Step 0b: Custom agent setup (~10 min)          ← can do while 0a runs
│
├─ Steps 1-2 (sequential, ~45 min)               ← start simultaneously with Step 0a
├─ Step 7a: Semgrep built-in scans (~15 min)      ← start as soon as rtv is accessible
│
│  ... wait for Step 0a to complete ...
│
├─ Step 3a-3f (all 6 in parallel, ~25 min)        ← security overlay only (faster with BMAD baseline)
│
│  ... wait for Steps 1-3 to complete ...
│
├─ Step 4 (~25 min)
├─ Step 5 (~40 min)
├─ Step 5-review: Adversarial review (~20 min)    ← human reviews findings
├─ Step 5b-A: Threagile YAML (~25 min)
├─ Step 5b-B: Threagile CLI (~5 min)
├─ Step 7b: Custom Semgrep rules (~40 min)        ← can start after Step 4
│
│  ... wait for Steps 5, 5b, 7a, 7b ...
│
├─ Step 6: Final risk assessment (~25 min)
├─ Step 6-review: Adversarial review (~20 min)    ← human reviews findings
├─ Step 7c: Deep-dive (optional, ~2-3 hours)      ← after Step 6
│
│  ... wait for Steps 6, 7 ...
│
├─ Step 8a: Compliance consolidation Parts A+B (~40 min)  ← after Step 6
├─ Step 8b: EN standard compliance Part C (~50 min)       ← can run parallel with 8a
│
│  ... human reviews compliance matrices and transfers QuBA-libre inputs into Excel (~30-60 min) ...
```

---

## Maintenance and Updates

After the initial assessment:

1. **Re-run BMAD `document-project`** (Step 0a) as a full rescan whenever the codebase changes significantly — the BMAD workflow supports incremental rescans and deep-dives for specific areas, so the baseline stays current
2. **Re-run Step 1** whenever the build scripts change to detect new artifacts
3. **Re-run Step 3** for specific components when their source code changes significantly — the BMAD baseline update (item 1) should precede this so Step 3 always works from current architecture documentation
4. **Re-run Steps 5-6 with adversarial reviews** quarterly or after major releases to refresh the threat model
4. **Re-run Threagile** (Step 5b-B) after updating `threagile.yaml` — the YAML model is versionable and diffable, making it easy to track how the threat landscape changes over time
5. **Re-run Semgrep scans** (Step 7a) on every commit or as part of CI — built-in rule packs catch regressions automatically
6. **Maintain custom Semgrep rules** (Step 7b) as a living asset — update rules when new interfaces are added or existing trust boundaries change; commit the `custom_rules\` directory to version control
7. Use the generated documentation as **context for ongoing AI-assisted development** — agents can reference the interface maps and threat models when implementing new features
8. **Re-run Step 8** after re-assessments to update the QuBA-libre inputs and Type II delta assessments — the CRA requires continuous risk assessment throughout the product's support period, so Step 8 outputs should be versioned and the QuBA-libre Excel updated accordingly
9. **Track countermeasure implementation** using the `hypervisor_countermeasures.md` status column — as countermeasures move from "Recommended" to "Implemented", re-run Step 8 to update the CRA Annex I coverage analysis
10. **Re-evaluate EN compliance when final standards are published** — the EN 304 635 and EN 304 626 documents used in this plan are interim drafts (V0.0.10 and V0.1.0 respectively, dated December 2025). When the final versions are published (expected H2 2026) and cited in the EU Official Journal, re-run Step 8 Part C against the final normative text. Pay attention to: requirement numbering changes, new/removed assessment cases, modified risk factor definitions, and updated Security Category Level mappings
11. **Monitor for additional harmonised standards** — ETSI is developing additional vertical standards under the CRA standardisation request. If new standards become applicable (e.g., EN 304 627 for network equipment, EN 304 628 for industrial IoT), add them to the Harmonised Standards Reference section and extend Step 8 accordingly

---

## Relationship to BMAD Method

This plan **actively integrates** three BMAD features to avoid duplicating work and to improve consistency across steps:

| BMAD Feature | Where Used | Value Added |
|---|---|---|
| **`document-project` workflow** | Step 0a (precursor to Step 3) | Generates baseline architecture, source tree, dependency, and technology documentation. Step 3 then adds the security-specific overlay (trust boundaries, privilege context, EN standard mapping) instead of rediscovering the entire architecture from scratch. |
| **Agent Customization** | Step 0b (persistent context for all steps) | A custom security-assessment agent carries CRA classification, EN standard references, trust boundary definitions, and product mappings as persistent memories. Every subsequent step inherits this context automatically — no need to copy-paste multi-paragraph preambles into each prompt. |
| **Adversarial Review** | Steps 5-review and 6-review (validation passes) | BMAD's forced-finding review technique is applied to the threat model and risk assessment outputs. The reviewer *must* find issues, breaking confirmation bias and catching gaps before findings flow into the formal compliance documents (Step 8). |

**What remains independent of BMAD:**
- The threat model and risk assessment steps (5, 5b, 6) use domain-specific methodologies (STRIDE, Threagile) that go beyond BMAD's scope
- The Fabric prompt patterns, Semgrep scanning, and Threagile YAML generation are custom to this plan
- The compliance consolidation (Step 8) with QuBA-libre and EN standard mapping is entirely security-domain-specific
- BMAD's four-phase workflow (Analysis → Planning → Solutioning → Implementation) does not apply — this plan produces analysis artifacts, not software

## External Tool Integration Summary

| Tool | Where Used | Role | Output |
|---|---|---|---|
| **BMAD Method** | Step 0a, 0b, 5-review, 6-review | `document-project` workflow for baseline architecture documentation; agent customization for persistent security context; adversarial review for threat model and risk assessment validation | Baseline project docs (`_bmad-output/`), custom agent config, adversarial review findings |
| **Fabric** | Steps 3, 5, 7c | Prompt pattern templates (`extract_architecture`, `create_threat_model`, `find_vulnerabilities`) embedded in agent prompts for consistent, security-focused output structure | Structured markdown (via agent) |
| **Threagile** | Step 5b | Automated threat-model-as-code: agent generates YAML, Threagile CLI produces reproducible risk reports and architectural diagrams | `report.pdf`, `risks.json`, `data-flow-diagram.png` |
| **Semgrep** | Steps 7a, 7b | SAST scanning with both built-in rule packs (standard vulnerability patterns) and custom rules (trust-boundary-specific patterns generated by AI agent) | JSON findings → markdown summaries |
| **QuBA-libre** | Step 8 | Formal risk register for CRA Important Class 2 conformity — questionnaire-driven risk assessment with automated Annex I mapping, countermeasure catalogs (IEC 62443, ETSI EN 303 645), and assumption management | Completed Excel workbook with CRA Annex I 1.2 report, JSON export |
| **AT3350 / AT9310** | Reference only | FMEA-style risk register used by acontis for EC-Master (not used for the acontis hypervisor products — all are Important Class 2 requiring QuBA-libre). The AT9310 template serves as a reference for risk scoring conventions. | N/A for this assessment |
| **EN 304 635** | Steps 3, 5, 5b, 8b | CRA harmonised standard for Virtualisation/Container — defines hypervisor requirements (§5.1.1), M&O system requirements (§5.1.3), threat catalog (§4.4.2), assessment cases (§6.3.1), and risk methodology (Annex B) | Compliance matrix, assessment case evidence mapping, SCL determination |
| **EN 304 626** | Steps 3, 5, 8b | CRA harmonised standard for Operating Systems — defines technical requirements (§5.2 TR-*), risk factors (Annex C.2 RF-*), threat catalog (Annex C.4 TH-*), and security profiles (Annex C.6) | Compliance matrix, risk factor scoring, security profile determination |

**How the tools and standards complement each other:**

- **BMAD Method** provides the *foundation layer*: `document-project` generates baseline architecture documentation that the security analysis builds on (avoiding redundant codebase discovery), agent customization ensures consistent domain context across all sessions, and adversarial review catches gaps in threat models and risk assessments before they flow into formal compliance documents
- **Fabric patterns** ensure the AI agent produces *consistently structured* documentation and threat analysis across all sessions, regardless of which model or IDE is used
- **Threagile** provides *automated, reproducible* risk scoring and *visual diagrams* that the AI agent alone cannot produce — its findings are schema-validated and diffable across versions
- **Semgrep** finds *concrete code-level vulnerabilities* with exact file/line citations — unlike the AI agent's threat modeling (which identifies theoretical threats) and Threagile (which identifies architectural risks), Semgrep proves that a vulnerability exists in the actual code
- **QuBA-libre** provides the *formal CRA compliance documentation* that a notified body requires for Important Class 2 products — it translates the technical findings into a structured, auditable risk register with explicit Annex I traceability
- **AT3350/AT9310** is used by acontis for EC-Master but is *not used for the acontis hypervisor products* — since all acontis hypervisor products are Important Class 2, they all require QuBA-libre-level assessment. The AT9310 template is referenced only for risk scoring conventions
- **EN 304 635 and EN 304 626** provide the *harmonised standard requirements and assessment cases* that a notified body will evaluate against — pre-mapping evidence to these standards creates the **presumption of conformity** with the CRA and dramatically reduces the effort of the formal conformity assessment. The EN threat catalogs also serve as a cross-check on the STRIDE analysis completeness
- **The AI agent** (Steps 0-6, 7c, 8) ties everything together by performing *cross-function reasoning, contextual analysis, natural-language threat scenarios, and compliance mapping* that none of the automated tools can do alone
