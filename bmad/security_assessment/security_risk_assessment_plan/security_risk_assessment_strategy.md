# Security Risk Assessment Strategy for the acontis Hypervisor Product Family

## Table of Contents

- [Goal](#goal)
- [Products Under Assessment](#products-under-assessment)
- [Applicable Standards](#applicable-standards)
- [Approach: Layered Assessment](#approach-layered-assessment)
- [Steps Overview](#steps-overview)
  - [Phase A: Foundation (Steps 0–2)](#phase-a-foundation-steps-02)
  - [Phase B: Architecture & Threat Analysis (Steps 3–6)](#phase-b-architecture--threat-analysis-steps-36)
  - [Phase C: Code-Level Scanning (Step 7)](#phase-c-code-level-scanning-step-7)
  - [Phase D: Compliance Consolidation (Step 8)](#phase-d-compliance-consolidation-step-8)
- [Tools Used](#tools-used)
- [Final Deliverables](#final-deliverables)
- [Effort Estimate](#effort-estimate)
- [Detailed Plan](#detailed-plan)
- [Glossary](#glossary)

---

## Goal

Produce a comprehensive, evidence-based security risk assessment of the entire acontis hypervisor product family to satisfy EU Cyber Resilience Act (CRA) conformity requirements. **All acontis hypervisor products** virtualise guest operating systems and are therefore classified as **CRA Important Class 2**, requiring mandatory third-party assessment by a notified body.

acontis will perform the full risk assessment for **RTOSVisor** (Type I Hypervisor, Linux host) and **LxWin** (Type II Hypervisor, Windows host) as the representative products. The remaining Type II products share the same VMF Core and Windows driver stack as LxWin, so LxWin findings are transferable with product-specific deltas.

The assessment is AI-agent-driven with minimal human interaction — each step runs as an independent AI agent session, with outputs feeding the next step.

---

## Products Under Assessment

All acontis hypervisor products are classified as **CRA Important Class 2**:

| Product | Hypervisor Type | Assessment Scope | Conformity Route |
|---|---|---|---|
| **RTOSVisor** | Type I (Linux host) | **Full assessment** | Notified body assessment |
| **LxWin** | Type II (Windows host) | **Full assessment** (representative for all Type II) | Notified body assessment |
| VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32 | Type II (Windows host) | Delta assessment (references LxWin) | Notified body assessment |

All products share the **VMF Framework Core** — the hypervisor kernel that manages virtual machines, trust boundaries, and host-guest communication. The Type II products additionally share the Windows driver stack and user-mode libraries.

---

## Applicable Standards

| Standard | Scope |
|---|---|
| **ETSI EN 304 635** (Virtualisation/Container) | Hypervisor requirements, M&O system (HvWeb), threat catalog, ~70 assessment cases |
| **ETSI EN 304 626** (Operating Systems) | Linux host OS layer — memory isolation, secure updates, authentication, logging |

Compliance with these harmonised standards creates a **presumption of conformity** with the CRA.

---

## Approach: Layered Assessment

The strategy follows a two-layer architecture:

```
┌─────────────────────────────────────────┐     ┌──────────────────────────────────┐
│   Layer 1: Technical Investigation      │     │   Layer 2: Formal Compliance     │
│   (AI-driven, Steps 0–7)               │     │   (Steps 8a–8b)                 │
│                                         │     │                                  │
│  Build inventory → Architecture docs →  │────►│  RTOSVisor (Type I):             │
│  Interface maps → STRIDE threats →      │     │    QuBA-libre risk register      │
│  Threagile analysis → Risk scoring →    │     │    (full assessment)             │
│  Semgrep code scans → Code deep-dives   │     │                                  │
│                                         │────►│  LxWin (Type II representative): │
│  (evidence, findings, analysis)         │     │    QuBA-libre risk register      │
│                                         │     │    (full assessment)             │
│                                         │────►│                                  │
│                                         │     │  Other Type II products:         │
│                                         │     │    Delta assessments             │
│                                         │     │    (referencing LxWin)           │
└─────────────────────────────────────────┘     └──────────────────────────────────┘
```

**Layer 1** generates all the raw technical evidence. **Layer 2** packages it into QuBA-libre format for the two fully-assessed products and produces delta assessments for the remaining Type II products.

---

## Steps Overview

### Phase A: Foundation (Steps 0–2)

| Step | What It Does |
|---|---|
| **0a** BMAD Document Project | Runs the BMAD `document-project` workflow to generate baseline architecture, source tree, dependency, and technology documentation for the `rtv` codebase. Avoids rediscovering the architecture in later steps. |
| **0b** BMAD Custom Agent | Creates a security-assessment agent with persistent memories (CRA classification, EN standards, trust boundaries, product mappings) so every subsequent step inherits consistent context. |
| **1** Artifact Registry | Scans all build scripts to inventory every binary artifact (DLL, EXE, SYS, SO, MSI) with build source, output path, and signing status. |
| **2** Product-Artifact Map | Cross-references artifacts to products, identifying shared components and per-product bundles. |

### Phase B: Architecture & Threat Analysis (Steps 3–6)

| Step | What It Does |
|---|---|
| **3** Component Documentation | Produces security-focused documentation for each major component — trust boundaries, privilege context, security patterns, and EN standard requirement mapping. Builds on the BMAD baseline from Step 0a. |
| **4** Interface & Trust Boundary Map | Documents all inter-component interfaces and data flows that cross trust boundaries (kernel↔user, guest↔host, host↔network, client↔web). |
| **5** STRIDE Threat Modeling | Systematic threat analysis (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) for each trust boundary and component. Cross-references against EN 304 635 and EN 304 626 threat catalogs. |
| **5-review** Adversarial Review | BMAD adversarial review of the threat model — the reviewer *must* find gaps. Catches missing EN threat mappings, inconsistent severity ratings, and overlooked multi-hop attack paths. |
| **5b** Threagile Analysis | Translates the architecture into a Threagile YAML model, then generates automated risk reports and data-flow diagrams. |
| **6** Risk Assessment | Merges STRIDE and Threagile findings into a unified, scored risk register (Likelihood × Impact). Produces per-product risk profiles and prioritized remediation recommendations. |
| **6-review** Adversarial Review | BMAD adversarial review of the risk assessment — checks scoring consistency, mitigation gaps, and CRA sufficiency. |

### Phase C: Code-Level Scanning (Step 7)

| Step | What It Does |
|---|---|
| **7a** Semgrep Built-in Scans | Runs standard SAST rule packs against the source code for known vulnerability patterns. |
| **7b** Custom Semgrep Rules | AI-generated Semgrep rules targeting trust-boundary-specific patterns (VMF call validation, IOCTL input checking, IVSHMEM bounds, web injection). |
| **7c** AI Code Deep-Dive | Targeted source code review of high-risk areas identified by Steps 5–7b, with line-level vulnerability citations. |

### Phase D: Compliance Consolidation (Step 8)

| Step | What It Does |
|---|---|
| **8a** Risk Register Generation | Consolidates all findings into QuBA-libre format for RTOSVisor and LxWin (with CRA Annex I traceability, countermeasure catalog, assumption tracking). Produces delta assessments for the remaining Type II products referencing LxWin findings. |
| **8b** EN Standard Compliance | Produces compliance matrices against EN 304 635 and EN 304 626, maps evidence to ~70 assessment cases, scores risk factors, and identifies gaps. |

---

## Tools Used

| Tool | Role |
|---|---|
| **BMAD Method** | Baseline project documentation, persistent agent context, adversarial review |
| **Fabric** | Structured prompt patterns for consistent security-focused output |
| **Threagile** | Automated threat-model-as-code with reproducible risk reports |
| **Semgrep** | Static analysis with built-in and custom rules |
| **QuBA-libre** | Formal CRA risk register for all products (Important Class 2, notified body ready) |

---

## Final Deliverables

| Deliverable | Purpose | Audience |
|---|---|---|
| **Artifact registry** with product mapping | Complete inventory of what ships where | Internal engineering, auditors |
| **Component security documentation** | Architecture, trust boundaries, security patterns per component | Development team, security reviewers |
| **Interface and trust boundary map** | All data flows crossing privilege boundaries | Threat modelers, architects |
| **STRIDE threat model** with EN cross-reference | Categorized threats with severity, mitigations, and attack trees | Security team, notified body |
| **Threagile risk report** with data-flow diagrams | Automated, schema-validated, versionable risk analysis | Security team, management |
| **Scored risk register** with per-product profiles | Consolidated Likelihood × Impact scoring, top-10 risks, remediation priorities | Management, product owners |
| **Semgrep scan results** (built-in + custom) | Concrete code-level vulnerabilities with file/line citations | Development team |
| **QuBA-libre inputs** for RTOSVisor and LxWin | Questionnaire answers, countermeasure catalog, assumption register, CRA Annex I mapping | Notified body, compliance team |
| **Type II product delta assessments** | Product-specific differences from LxWin baseline for VxWin, CeWin, VmfWin, RTOS32Win, EC-WinRTOS-32 | Notified body, compliance team |
| **EN 304 635 / EN 304 626 compliance matrices** | Requirement-by-requirement compliance status with evidence links and gap analysis | Notified body, compliance team |

---

## Effort Estimate

| Metric | Estimate |
|---|---|
| Total agent sessions | 12–16 (plus 2–5 optional for code deep-dives) |
| Wall-clock time | 7–10 hours (with parallelization) |
| Human time required | ~2–3.5 hours (setup, reviews, compliance transfer) |

---

## Detailed Plan

The full step-by-step plan with exact agent prompts, input/output specifications, and tool configurations is in:

[security_risk_assessment_plan.md](security_risk_assessment_plan.md)

---

## Glossary

| Term | Definition |
|---|---|
| **Adversarial Review** | A structured review technique (from the BMAD method) where the reviewer is explicitly tasked with finding flaws, gaps, and inconsistencies in a document. Unlike a conventional review, the reviewer *must* produce findings — the goal is to stress-test completeness before the output moves to the next stage. |
| **BMAD Method** | An AI-driven development methodology that provides reusable workflows for project documentation (`document-project`), customizable AI agent personas with persistent context (memories), and adversarial review processes. Used here to generate baseline architecture documentation and maintain consistent domain knowledge across agent sessions. |
| **Compliance Matrix** | A document that maps each requirement from a standard (e.g., EN 304 635 §5.1.1) to the evidence demonstrating conformity — specific test results, design documents, or code references. Gaps are explicitly flagged. |
| **CRA (Cyber Resilience Act)** | EU Regulation 2024/2847 establishing mandatory cybersecurity requirements for products with digital elements sold in the EU. Manufacturers must perform risk assessments, implement security-by-design, provide vulnerability handling, and undergo conformity assessment before placing products on the market. |
| **Delta Assessment** | An assessment that does not repeat the full analysis but instead documents only the differences between a product and an already-assessed reference product. Here, the Type II products are assessed by documenting their deviations from the fully-assessed LxWin baseline. |
| **Denial of Service (DoS)** | STRIDE category. Threats that aim to make a system or resource unavailable to legitimate users — e.g., exhausting memory, flooding a network interface, or triggering a crash in a kernel driver. |
| **Elevation of Privilege** | STRIDE category. Threats where an attacker gains higher access rights than intended — e.g., a guest VM escaping to host kernel, or a user-mode process gaining kernel-mode execution. |
| **Fabric** | An open-source framework by Daniel Miessler that provides reusable prompt patterns (e.g., `extract_architecture`, `create_threat_model`, `find_vulnerabilities`) for consistent, structured AI output. Used here to ensure agent prompts produce comparable results across sessions. |
| **Harmonised European Standard (hEN)** | A standard developed by a European Standardisation Organisation (ETSI, CEN, CENELEC) and cited in the EU Official Journal. Compliance with a harmonised standard creates a *presumption of conformity* with the corresponding EU regulation — in this case, the CRA. |
| **Important Class 2** | The second-highest CRA product classification tier. Products in this category (including hypervisors) require mandatory third-party conformity assessment by a notified body — self-assessment is not permitted. |
| **Information Disclosure** | STRIDE category. Threats where confidential data is exposed to unauthorized parties — e.g., a guest VM reading host memory, or unencrypted credentials transmitted over a network interface. |
| **Notified Body** | An independent organization designated by an EU member state to perform third-party conformity assessments. For CRA Important Class 2 products, the notified body audits the manufacturer's technical documentation, risk assessment, and security measures before the product may carry the CE mark. |
| **Presumption of Conformity** | A legal concept where compliance with a harmonised standard is accepted as sufficient evidence of meeting the corresponding regulatory requirements, unless challenged. Eliminates the need to prove conformity requirement-by-requirement from first principles. |
| **QuBA-libre** | An open-source, questionnaire-based risk assessment tool designed for CRA conformity. Produces structured risk registers with CRA Annex I traceability, countermeasure catalogs (referencing IEC 62443, ETSI EN 303 645), and assumption tracking. Its output format is designed to be directly consumable by a notified body. |
| **Repudiation** | STRIDE category. Threats where an actor can deny having performed an action due to insufficient logging or audit trails — e.g., an administrator modifying VM configuration with no record of the change. |
| **Risk Register** | A structured document listing all identified security risks with their severity scoring (Likelihood × Impact), current mitigations, residual risk, and recommended remediation actions. Serves as the central artifact for CRA conformity assessment. |
| **SAST (Static Application Security Testing)** | Automated analysis of source code (without executing it) to find security vulnerabilities such as buffer overflows, injection flaws, or insecure API usage. Semgrep is the SAST tool used in this assessment. |
| **Semgrep** | An open-source SAST tool that matches code patterns using lightweight, declarative rules. Supports built-in rule packs for common vulnerabilities and custom rules for project-specific patterns (e.g., unchecked IOCTL inputs, missing VMF call validation). |
| **Spoofing** | STRIDE category. Threats where an attacker impersonates another entity — e.g., a malicious process posing as a legitimate VM management client, or a forged network packet claiming to be from a trusted host. |
| **STRIDE Threat Modeling** | A systematic threat identification methodology developed at Microsoft. Each system component and data flow is analyzed against six threat categories: **S**poofing, **T**ampering, **R**epudiation, **I**nformation Disclosure, **D**enial of Service, and **E**levation of Privilege. Ensures comprehensive coverage by forcing analysis of every category at every trust boundary. |
| **Tampering** | STRIDE category. Threats involving unauthorized modification of data or code — e.g., altering a VM disk image, modifying shared memory between guest and host, or injecting malicious firmware during an update. |
| **Threagile** | An open-source "threat-modeling-as-code" tool. Takes a YAML description of the system architecture (components, data flows, trust boundaries) and automatically generates risk reports, data-flow diagrams, and risk scores. Results are schema-validated and version-controllable. |
| **Trust Boundary** | A boundary in the system architecture where the level of trust changes — data crossing a trust boundary is potentially untrusted and must be validated. Key trust boundaries in this assessment include guest↔host, kernel↔user-mode, host↔network, and web client↔server. |
