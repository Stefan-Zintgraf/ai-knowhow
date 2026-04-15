# QuBA-libre Folder Analysis

## 1. Overview

The `QuBA-libre` folder contains a collection of resources for performing cybersecurity risk assessments in compliance with the EU Cyber Resilience Act (CRA). It includes the original open-source QuBA-libre tool, supporting reference documents, and acontis-specific adaptations targeting the **EC-Master** EtherCAT master stack product.

### File Inventory

| File | Type | Purpose |
|---|---|---|
| `QuBA-libre.xlsx` | Excel (LAMBDA) | Original QuBA-libre risk assessment template/tool (v1.0.0, August 2025) |
| `Risk Assessment AT3350 'AT3350_EC-Master_Risk_Assessment'.xlsx` | Excel | acontis custom risk assessment for EC-Master (non-QuBA format) |
| `Risk Assessment AT3351 'AT3351_EC-Master_Risk_Assessment_QuBA-libre'.xlsx` | Excel | acontis risk assessment for EC-Master using the QuBA-libre approach |
| `Template AT9310 'AT9310_Risk-Assessment-Template'.xltx` | Excel Template | acontis generic risk assessment template (non-QuBA format) |
| `CRA Gids v2.0 september 2025 UK.pdf` | PDF | Dutch government CRA compliance guide (v2.0, September 2025) |
| `CRA-RiskManagement-202506.pdf` | PDF | ATHENE/Fraunhofer white paper on CRA risk management (v1.0, July 2025) |
| `ey-gl-practical-refrence-architecture-for-cra-compliance-11-2025.pdf` | PDF | EY/Silitics/Cumulocity reference architecture for CRA compliance (October 2025) |
| `README.MD` | Markdown | QuBA-libre usage and feature overview |
| `CONTRIBUTING.md` | Markdown | QuBA-libre contribution guidelines |
| `LICENSE.txt` | Text | Creative Commons Attribution Share Alike 4.0 International license |

---

## 2. QuBA-libre Tool (`QuBA-libre.xlsx`)

### 2.1 Origin and License

QuBA-libre was developed by **Fraunhofer AISEC** and **SICK AG**, building on the Modular Risk Assessment (MoRA) methodology. It is licensed under **CC BY-SA 4.0**, allowing modification and redistribution with attribution.

### 2.2 Architecture and Sheet Structure

The workbook contains **24 sheets** organized into four functional categories:

**Catalogs (Light Grey — do not edit during analysis):**
- **Definitions**: Assessment model configuration — damage categories (Personal Data, Loss of IP, Financial/Legal, Safety, Function/Availability), damage criteria with severity levels (Low/Medium/High/Critical), risk matrix, RAP factor definitions, stakeholder types
- **Questions**: 57 questionnaire elements (21 impact questions QI1–QI16, 21 attack potential questions QA1–QA21, plus headings), structured with two-level answer trees (first answer → optional second question)
- **Damage Scenarios**: 19 pre-defined damage scenarios (DS1–DS19) automatically activated based on questionnaire answers, mapping impacts to confidentiality/integrity/availability loss
- **Attack Steps**: 42 attack steps (AS1–AS41) covering the full attack lifecycle — from gaining physical/network access through exploitation to IP extraction — each with Required Attack Potential (RAP) factors and CRA Annex I mappings
- **Assumptions**: 45 security design requirements (SDR) and assumptions (A1–A45) that can reduce risk by modifying attack feasibility or removing damage scenarios
- **Countermeasures**: 64 countermeasures (C0–C35, CM1–CM28) mapped to IEC 62443 controls, ETSI EN 303 645, and custom security controls, each with RAP reduction factors and damage scenario transformations

**Analysis Sheets (Dark Grey — fill during assessment):**
- **Documentation**: Product metadata (Target of Evaluation, authors, contacts, change history, illustrations)
- **Questionnaire**: Interactive assessment interface with conditional questions, info texts, and rationale fields
- **Mitigation**: Attack step-by-step countermeasure and assumption assignment

**Results (Blue — auto-calculated):**
- **DS Overview**: Active damage scenario summary
- **Risks**: Full risk calculation (Attack Path × Damage Scenario × RAP = Risk Level)
- **Risk Treatment**: Accept/Avoid/Mitigate/Transfer decisions with residual risk
- **Result Summary**: Aggregated assumptions and countermeasures with stakeholder assignments
- **Annex I 1.2 Report**: Direct mapping to CRA Annex I Part I (2) requirements (a–m)
- **Tracing**: Planned vs. confirmed countermeasure tracking

**Operational Sheets:**
- **Tasks**: TODO tracking linked to cells across all sheets
- **Quality Indicators**: Assessment completeness metrics
- **JSON**: Machine-readable export of assessment data
- **Version History**, **User Information**, **Profile Definitions**, **Helper**: Configuration and metadata

### 2.3 Risk Assessment Methodology

The QuBA-libre methodology follows this flow:

1. **Impact Rating (QI questions)**: Assess worst-case impact across three CIA dimensions:
   - Confidentiality loss → Personal Data, IP, Financial/Legal
   - Availability loss → Safety, Function/Availability, Financial/Legal
   - Integrity loss → Safety, Personal Data/IP, Function/Availability, Financial/Legal

2. **Required Attack Potential (QA questions)**: Characterize the product's attack surface:
   - Connectivity (physical, logical, wireless, Internet)
   - Interface exposure (configuration, debug, services)
   - Hardware accessibility and production security
   - Supply chain trustworthiness
   - Product lifetime and support duration

3. **Automated Risk Calculation**: The tool automatically:
   - Activates relevant damage scenarios based on answers
   - Computes attack paths (combinations of attack steps)
   - Calculates RAP per attack path using five factors: Elapsed Time, Expertise, Knowledge of TOE, Window of Opportunity, Equipment
   - Determines risk level from the risk matrix (Damage Level × RAP)

4. **Mitigation**: Assign countermeasures and assumptions to reduce RAP or transform/remove damage scenarios

5. **Risk Treatment**: Make explicit accept/avoid/mitigate/transfer decisions on residual risks

6. **CRA Reporting**: Auto-generates mapping to CRA Annex I requirements

### 2.4 Key Design Strengths

- Fully formula-driven (LAMBDA functions, no VBA) — transparent and auditable
- Pre-built catalogs aligned to IEC 62443 and CRA
- Conditional question activation prevents irrelevant questions
- Damage scenario transformations model partial mitigations
- JSON export enables integration with external tools
- Task tracking system links TODOs to specific cells

### 2.5 Key Limitations

- Requires Microsoft 365 desktop Excel (LAMBDA support)
- Single-product focus — no multi-product portfolio view
- Excel-based merging is impractical for team collaboration
- Attack step catalog is generic (not product-specific)
- No automated connection to vulnerability databases (CVE, NVD)

---

## 3. acontis AT Files (EC-Master Adaptations)

### 3.1 AT3350 — Custom Risk Assessment (`AT3350_EC-Master_Risk_Assessment.xlsx`)

This is an **independent, acontis-designed** risk assessment for the EC-Master stack, **not** using the QuBA-libre methodology.

**Structure:**
- 11 sheets: Info, RiskAssessment, RiskMatrix (chart), AttackRiskStep, DamageCategory, Stakeholder, Likelihood, Impact, RPN, ActionStatus, Owner
- Uses a classic FMEA-style approach: Risk = Likelihood × Impact → Risk Priority Number (RPN)

**Product Context:**
- Company: acontis technology GmbH
- Product: EC-Master stack (EtherCAT master software library)
- Assessment created: February 2026

**Risk Entries (29 identified risks, RID 1–29):**

Key risk scenarios identified for the EC-Master:

| RID | Attack Path | Description | Category | Likelihood | Impact |
|---|---|---|---|---|---|
| 1 | AS1→AS3 | Physical access + software vulnerability exploitation | Safety & Security | Unlikely | Catastrophic |
| 3–4 | AS1/AS2→AS4 | DoS attack via trusted environment or local network (RAS, EAP, MbxGateway) | Function & Availability | Possible | Catastrophic |
| 5–6 | AS1/AS2→AS6 | Wireshark sniffing/manipulation of EtherCAT or RAS communication | Safety & Security | Negligible | Catastrophic |
| 7–8 | AS1/AS2→AS7 | Spoofing incoming EtherCAT/RAS frames (process data injection) | Safety & Security | Possible/Unlikely | Catastrophic |
| 13–16 | AS1/AS2→AS14/AS16 | Communication disruption and configuration manipulation via RAS | Safety & Security | Possible | Catastrophic |
| 17–18 | AS21/AS22→AS23 | Physical access leading to ENI file manipulation | Safety & Security | Possible/Likely | Catastrophic |
| 19 | AS31 | Cross-customer network access via EoE gateway | Safety & Security | Likely | Catastrophic |
| 20–21 | AS32 | IP theft by customer or internal employee | Financial & Legal | Likely | Major/Moderate |
| 22 | AS37 | Production manipulation (intentional or accidental) | Safety & Security | Possible | Catastrophic |
| 23 | AS38 | Supply chain attack (eXpat dependency) | Safety & Security | Unlikely | Catastrophic |
| 24 | AS3 (supply chain) | CVE in unmaintained supply chain component (eXpat) | Safety & Security | Unlikely | Moderate |
| 29 | AS42 | License circumvention/bypassing | Financial & Legal | Possible | Moderate |

**Notable product-specific attack surfaces:**
- **RAS (Remote Access Server)**: TCP-based remote control interface — major exposure point
- **EoE (Ethernet over EtherCAT)**: Protocol gateway functionality enabling cross-network attacks
- **ENI (EtherCAT Network Information) file**: XML configuration file — manipulation can alter variable mappings
- **eXpat**: XML parser dependency in the supply chain
- **EC-Engineer**: Configuration tool accessing volatile memory via RAS

### 3.2 AT3351 — QuBA-libre Based Assessment (`AT3351_EC-Master_Risk_Assessment_QuBA-libre.xlsx`)

This file adapts the QuBA-libre methodology to the EC-Master product. It appears to be based on an earlier QuBA-libre version (pre-1.0.0, as the template dates from 2025-07-30 while the folder's QuBA-libre.xlsx is v1.0.0 from August 2025).

**Key observations from filled questionnaire data:**

The questionnaire has been partially filled for what appears to be an **industrial RFID/sensor device** example (from the SICK product catalog, not the EC-Master). This is visible from references to:
- RFID tags, sensors, cameras
- AGVs (Automated Guided Vehicles)
- Airport luggage systems, production sites
- OPC UA server, MQTT, Profinet connectivity
- WLAN and RF communication

**Selected answers and risk implications identified in the data:**

| Question | Answer | Rationale / Notes |
|---|---|---|
| QI1 (Cameras/sensors recognizing people) | — | Product has sensors |
| QI7 (Availability relevant for environment) | Yes / Major disturbance | Production halted scenario |
| QI10 (Manipulated product endangers health) | No | AGVs only transport items |
| QI11 (Disclose personal data) | Yes / Personal data (significant) | RFID tags + network interface |
| QI13 (Disclose crypto material) | Yes / < 200,000 EUR | OPC UA server credentials |
| QI14 (Affect operation of environment) | Yes / Critical disturbance | Wrong luggage routing, production damage |
| QA1 (Connectivity) | Yes | Network-connected product |
| QA2 (Gateway) | No | Ring topology, no routing/firewalling |
| QA3 (Point-to-point) | Yes / Trusted | Within production site |
| QA4 (Local network) | Yes / Trusted | Within production site |
| QA5 (Wireless) | Yes / Trusted | RF + WLAN communication |
| QA6 (Internet/mobile) | No | USB-C only when plugged in |
| QA7 (Network services) | Yes | OPC UA, MQTT, Profinet |
| QA8 (Configuration interface) | Yes / Protected | Username + password, OPC UA certificates |
| QA9 (IP stack) | Yes | Ethernet, IP, TCP, Profinet, OPC UA, MQTT |
| QA17 (Debug interfaces) | Yes / Yes (remote) | Physically internal only, USB potential |

**Assessment Status:** The mitigation sheet shows all attack steps currently at "No Risk" (likely because the questionnaire is not fully completed or the risk table hasn't been recalculated). The countermeasures catalog references are populated in the proposed columns.

### 3.3 AT9310 — Generic Risk Assessment Template

This is the acontis-internal **template** (`.xltx` format) matching the AT3350 structure. It provides the same FMEA-style framework with empty rows for up to 499 risk entries, pre-configured lookup sheets for:
- Attack/Risk Steps (AS1–AS42 with descriptions)
- Damage Categories
- Stakeholder definitions
- Likelihood and Impact scales
- RPN (Risk Priority Number) calculation matrix
- Action Status tracking
- Owner assignment

---

## 4. Reference Documents (PDFs)

### 4.1 CRA Guide v2.0 (Dutch Government, September 2025)

A **20-page practical guide** explaining the CRA for manufacturers, importers, and distributors of products with digital elements. Key content:

- **Scope**: All products with digital elements on the EU market, including separate software/hardware components
- **Timeline**: Reporting obligations effective September 11, 2026; full compliance by December 11, 2027
- **Product Classification**: Regular → Important Class 1 → Important Class 2 → Critical
- **Hypervisors are explicitly listed as Important Class 2** products (Section 3.2.3), requiring mandatory assessment by a conformity assessment body
- **Conformity Assessment**: Internal control for regular products; notified body required for Important Class 2 and Critical
- **Vulnerability Reporting**: 24h early warning → 72h notification → 14-day final report for actively exploited vulnerabilities
- **Technical Documentation Requirements**: Product description, design/development documentation, cybersecurity risk assessment, SBOM, conformity assessment results

**Relevance to acontis**: The EC-Master stack, being an EtherCAT master software library, likely falls under regular products or potentially Important Class 1 (depending on whether it qualifies as a network management system or operates in industrial control). For the acontis hypervisor products, the CRA explicitly classifies hypervisors as Important Class 2.

### 4.2 CRA Risk Management (ATHENE/Fraunhofer, July 2025)

A **20-page white paper** providing implementation guidance for CRA risk management. Key insights:

- **Product-centric vs. organization-centric risk**: The CRA focuses on product-level risks (unlike ISO 27001 which focuses on organizational assets) — this is a fundamental conceptual difference
- **Risk definition**: CRA Art. 3(37) defines risk as "potential for loss or disruption caused by an incident, expressed as magnitude × likelihood"
- **SecDevOps integration mapping** (Table 2):
  - Plan/Design: Threat modeling (STRIDE, OWASP Threat Dragon)
  - Build/Test: SAST, DAST, SCA, container scanning
  - Release: Signed artifacts, secure OTA updates
  - Operate: Continuous monitoring, CVD processes
- **Requirements engineering methodologies** compared (Table 3): INCOSE, NIST SP 800-160, ISO 62443, OWASP SAMM, MITRE ATT&CK, STPA-Sec, SQUARE, SAFe — with CRA alignment ratings
- **Continuous risk assessment**: Must be updated throughout the support period

**Relevance to QuBA-libre**: QuBA-libre directly addresses the CRA requirement for a documented cybersecurity risk assessment. Its questionnaire-based approach maps to the "risk framing" and "risk assessment" steps described in this paper. The Annex I 1.2 Report sheet provides the CRA conformity documentation.

### 4.3 EY Reference Architecture (EY/Silitics/Cumulocity, October 2025)

A **12-page practical architecture** paper addressing CRA technical challenges. Key components:

- **Rugix Ctrl**: Runtime foundation for secure embedded Linux devices (secure boot, A/B updates, factory reset)
- **Cumulocity**: IoT fleet management platform (device monitoring, vulnerability tracking, coordinated updates)
- **Software Composition Analysis**: SBOM-based CVE monitoring (Dependency-Track, BlackDuck)
- **Disclosure Infrastructure**: CSAF-based vulnerability advisory publication

**Technical challenges mapped to CRA requirements:**
1. SBOM generation and vulnerability monitoring
2. Coordinated Vulnerability Disclosure (CVD)
3. Secure and robust update processes
4. Device integrity and confidentiality
5. Logging and security monitoring
6. Secure factory reset and data deletion

**Relevance to acontis**: Primarily relevant for the hypervisor/embedded Linux products. The EC-Master as a software library has different deployment characteristics but the SBOM and vulnerability monitoring aspects apply universally.

---

## 5. Comparative Analysis: AT3350 vs. AT3351 (QuBA-libre)

The two EC-Master risk assessments represent fundamentally different approaches:

| Aspect | AT3350 (Custom) | AT3351 (QuBA-libre) |
|---|---|---|
| **Methodology** | FMEA-style (Likelihood × Impact → RPN) | QuBA-libre (Questionnaire → Attack Paths → RAP × Damage Level) |
| **Attack Modeling** | Manual attack path definition (ASx → ASy → ASz) | Automated attack path derivation from questionnaire answers |
| **Risk Scoring** | 5-level Likelihood × 5-level Impact matrix | Multi-factor RAP (5 factors) × 4-level Damage matrix |
| **Countermeasures** | Not visible in extracted data | Pre-built catalog (IEC 62443, ETSI EN 303 645) |
| **CRA Mapping** | None visible | Built-in Annex I 1.2 report |
| **Product Specificity** | Highly product-specific (RAS, EoE, ENI, eXpat) | Generic questionnaire with product-specific answers |
| **Completeness** | 29 risks identified and characterized | Partially filled (appears to use SICK example data, not EC-Master) |
| **Stakeholder Separation** | acontis vs. customer | Customer, OEM, Other (per assumption) |
| **Supply Chain Coverage** | Explicit eXpat dependency tracking | Generic supply chain questions (QA18, QA19) |

### Observations

1. **AT3351 appears to contain example/demo data from a SICK product**, not actual EC-Master assessment data. References to RFID tags, AGVs, airports, OPC UA, and MQTT are inconsistent with an EtherCAT master stack. This suggests the file was created to evaluate the QuBA-libre methodology using existing SICK example data rather than being a completed EC-Master assessment.

2. **AT3350 contains genuine EC-Master risk data** with product-specific attack scenarios, component-level detail (RAS, EoE, ENI, eXpat), and realistic likelihood/impact ratings.

3. **Neither assessment is complete**: AT3350 has 29 of 499 possible risk entries filled; AT3351 has all mitigation rows showing "No Risk" (likely due to incomplete questionnaire).

---

## 6. Gap Analysis for acontis Products

### 6.1 What QuBA-libre Provides

- Structured, repeatable risk assessment methodology aligned to CRA
- Pre-built catalogs of attack steps, assumptions, and countermeasures
- Automated risk calculation with auditable formulas
- Direct CRA Annex I mapping for compliance documentation
- JSON export for tool integration

### 6.2 What Is Missing for a Complete CRA Compliance Workflow

| Gap | Description | Potential Solution |
|---|---|---|
| **Product-specific attack steps** | QuBA-libre's 42 generic attack steps don't cover EC-Master-specific vectors (RAS protocol attacks, ENI manipulation, EoE gateway abuse, EtherCAT frame injection) | Extend the Attack Steps catalog with product-specific entries |
| **SBOM integration** | No connection to software bill of materials or automated CVE monitoring | Integrate with Dependency-Track or similar SCA tools; feed SBOM data into QuBA's supply chain questions |
| **Vulnerability tracking** | QuBA is a point-in-time assessment; CRA requires continuous monitoring | Implement periodic re-assessment workflow; link to CVE monitoring |
| **Multi-product management** | Each product requires a separate Excel file; no portfolio-level risk view | Consider a database-backed solution or use QuBA's JSON export to aggregate |
| **Conformity assessment documentation** | QuBA generates the Annex I report but not the full technical documentation package | Complement with architecture documents, SBOM, test reports, and CVD policy |
| **Automated testing integration** | No connection to SAST/DAST/fuzzing results | Feed Semgrep/SAST results into risk assessment as evidence for countermeasure effectiveness |
| **Team collaboration** | Excel-based; no merge capability | Consider version-controlled JSON export + regeneration workflow |

### 6.3 Recommendations for acontis

1. **Complete the AT3351 assessment** with actual EC-Master data instead of the SICK example data currently present. Use AT3350's risk inventory as input.

2. **Extend the QuBA-libre catalogs** with EC-Master-specific attack steps, particularly for:
   - RAS protocol exploitation (unauthenticated access, command injection)
   - ENI file manipulation (variable mapping attacks)
   - EoE cross-network lateral movement
   - EtherCAT frame-level attacks (process data spoofing)
   - License mechanism bypass

3. **Establish a mapping between AT3350 and AT3351** to ensure no risks identified in the custom assessment are lost in the QuBA-libre transition.

4. **For the acontis hypervisor products**: Note that the CRA explicitly classifies hypervisors as **Important Class 2** products requiring mandatory third-party conformity assessment. The QuBA-libre approach can serve as the risk assessment foundation, but the conformity assessment must be performed by a notified body.

5. **Leverage the JSON export** from QuBA-libre to feed data into the security risk assessment pipeline described in `security_risk_assessment_plan.md`, particularly for integration with Threagile (YAML threat model generation) and Fabric (structured prompt patterns).

---

## 7. Summary

The QuBA-libre folder represents acontis's initial steps toward CRA-compliant cybersecurity risk assessment for the EC-Master product. The collection includes the open-source QuBA-libre assessment tool, two complementary risk assessment approaches (custom FMEA-style and QuBA-libre-based), a reusable template, and three authoritative CRA reference documents.

The most significant finding is that the **AT3351 QuBA-libre assessment contains SICK example data rather than actual EC-Master data**, meaning the QuBA-libre evaluation for EC-Master has not yet been performed. The AT3350 custom assessment is more advanced with 29 identified risks, but lacks the CRA traceability that QuBA-libre provides.

The recommended path forward is to complete the AT3351 assessment with genuine EC-Master data, extend the QuBA-libre catalogs with product-specific attack steps derived from AT3350, and integrate the assessment outputs into the broader security risk assessment pipeline for automated CRA compliance workflows.
