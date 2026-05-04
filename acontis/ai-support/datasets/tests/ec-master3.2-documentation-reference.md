# EC-Master Documentation Reference

> **Purpose:** This file provides a complete map of the EC-Master V3.2 online HTML documentation structure. It is intended to be used as context (e.g., being referenced in a `memory.md`, `claude.md`, or project knowledge file) so that any prompt referencing EC-Master documentation can produce answers with accurate deep links — without needing to re-specify URLs each time.

---

## Manuals Overview Page

https://developer.acontis.com/ec-master#manuals

---

## EC-Master V3.2 Online HTML Manuals

### Base URLs

| Manual | HTML Base URL |
|--------|--------------|
| Class B User Manual | `https://public.acontis.com/manuals/EC-Master/3.2/html/ec-master-class-b/` |
| Class A Add-On User Manual | `https://public.acontis.com/manuals/EC-Master/3.2/html/ec-master-class-a/` |
| Python Programming Interface | `https://public.acontis.com/manuals/EC-Master/3.2/html/ec-master-python/` |

### PDF Downloads

| Document | URL |
|----------|-----|
| Quickstart Guide | `https://public.acontis.com/manuals/EC-Master/3.2/EC-Master_QuickStart_Guide.pdf` |
| Class B User Manual (PDF) | `https://public.acontis.com/manuals/EC-Master/3.2/EC-Master_UserManual.pdf` |
| Class A Add-On Manual (PDF) | `https://public.acontis.com/manuals/EC-Master/3.2/EC-Master_ClassA.pdf` |
| Python Programming Interface (PDF) | `https://public.acontis.com/manuals/EC-Master/3.2/EC-Master_Python.pdf` |
| Release Notes (PDF) | `https://public.acontis.com/manuals/EC-Master/3.2/EC-Master_ReleaseNotes.pdf` |
| Performance Data Sheet (PDF) | `https://public.acontis.com/manuals/EC-Master/3.2/EC-Master_PerformanceDataSheet.pdf` |

### Other Version-Independent Manuals (V3.x)

| Manual | HTML URL |
|--------|----------|
| Supported Operating Systems | `https://public.acontis.com/manuals/EC-Master/3.x/html/ec-master-os/index.html` (approx.) |
| Runtime Licensing User Manual | PDF only |

---

## Class B User Manual — Complete Section Map

Base: `https://public.acontis.com/manuals/EC-Master/3.2/html/ec-master-class-b/`

### 1. Introduction (`intro.html`)

| Section | Anchor | Full URL |
|---------|--------|----------|
| 1. Introduction | `intro.html` | `.../ec-master-class-b/intro.html` |
| 1.1. What is EtherCAT? | `#what-is-ethercat` | `.../ec-master-class-b/intro.html#what-is-ethercat` |
| 1.2. The EC-Master - Features | `#the-ec-master-features` | `.../ec-master-class-b/intro.html#the-ec-master-features` |
| 1.3. Protected version | `#protected-version` | `.../ec-master-class-b/intro.html#protected-version` |
| 1.4. License | `#license` | `.../ec-master-class-b/intro.html#license` |
| 1.5. Versioning | `#versioning` | `.../ec-master-class-b/intro.html#versioning` |

### 2. Getting Started (`gettingstarted.html`)

| Section | Anchor |
|---------|--------|
| 2. Getting Started | `gettingstarted.html` |
| 2.1. EC-Master Architecture | `#ec-master-architecture` |
| 2.2. EtherCAT Network Configuration (ENI) | `#ethercat-network-configuration-eni` |
| 2.3. Operating system configuration | `#operating-system-configuration` |
| 2.4. Running EcMasterDemo | `#running-ecmasterdemo` |
| 2.5. Compiling the EcMasterDemo | `#compiling-the-ecmasterdemo` |

### 3. Software Integration (`software-integration.html`)

| Section | Anchor |
|---------|--------|
| 3. Software Integration | `software-integration.html` |
| 3.1. Network Timing | `#network-timing` |
| 3.2. Example application | `#example-application` |
| 3.3. Master startup | `#master-startup` |
| 3.4. EtherCAT Network Configuration ENI | `#ethercat-network-configuration-eni` |
| 3.5. Process Data Access | `#process-data-access` |
| 3.6. Process Data Memory | `#process-data-memory` |
| 3.7. Error detection and diagnosis | `#error-detection-and-diagnosis` |
| 3.8. EtherCAT traffic logging in application | `#ethercat-traffic-logging-in-application` |
| 3.9. Trace Data | `#trace-data` |
| 3.10. EtherCAT Master Stack Source Code | `#ethercat-master-stack-source-code` |
| **3.10.2. Excluding features** | **`#excluding-features`** |
| 3.11. Reduced Feature Set | `#reduced-feature-set` |

> **Note:** Section 3.10.2 "Excluding features" documents compile-time defines such as `EXCLUDE_DC_SUPPORT`, `EXCLUDE_EOE_ENDPOINT`, `EXCLUDE_HOTCONNECT`, etc. This is where Class A features can be excluded at build time.

### 4. Platform and Operating Systems (OS)

| Section | Page |
|---------|------|
| 4. Platform and Operating Systems (OS) | `toc_os.html` |
| 4.1. CMSIS-RTOS for STM32 | `os_cmsis-rtos.html` |
| 4.2. eCos | `os_ecos.html` |
| 4.3. FreeRTOS | `os_freertos.html` |
| 4.4. tenAsys INtime | `os_intime.html` |
| 4.5. Linux | `os_linux.html` |
| 4.6. PC / BIOS | `os_pc-bios.html` |
| 4.7. QNX Neutrino | `os_qnx.html` |
| 4.8. Renesas | `os_renesas.html` |
| 4.9. IntervalZero RTX | `os_rtx.html` |
| 4.10. SylixOS | `os_sylixos.html` |
| 4.11. TI-RTOS | `os_ti-rtos.html` |
| 4.12. µC3 for STM32 | `os_uc3.html` |
| 4.13. µC3 for Renesas RZ/T2 | `os_uc3.html#c3-for-renesas-rz-t2` |
| 4.14. µC3 for Renesas RZ/N2H | `os_uc3.html#c3-for-renesas-rz-n2h` |
| 4.15. Windriver VxWorks | `os_vxworks.html` |
| 4.16. Microsoft Windows | `os_windows.html` |
| 4.17. Microsoft Windows CE | `os_windows-ce.html` |
| 4.18. Xenomai | `os_xenomai.html` |
| 4.19. Zephyr | `os_zephyr.html` |

### 5. Real-time Ethernet Driver (`emll.html`)

| Section | Page |
|---------|------|
| 5. Real-time Ethernet Driver | `emll.html` |
| 5.1. Real-time Ethernet Driver initialization | `emll_init.html` |

Individual driver pages follow the pattern: `emll<drivername>.html`
Examples: `emllicss.html`, `emllintelgbe.html`, `emllndis.html`, `emllsockraw.html`, etc.

### 6. Application Programming Interface (API) Reference

| Section | Page / Anchor |
|---------|---------------|
| 6. API reference (overview) | `toc_api.html` |
| 6.1. Generic API return status values | `api.html` |
| 6.2. Multiple EtherCAT Bus Support | `api.html#multiple-ethercat-bus-support` |
| 6.3. General functions | `api.html#general-functions` |
| 6.4. Process Data Access | `api.html#process-data-access` |
| 6.5. Generic notification interface | `api.html#generic-notification-interface` |
| 6.6. Slave control and status functions | `api.html#slave-control-and-status-functions` |
| 6.7. Diagnosis, error detection, error notifications | `api.html#diagnosis-error-detection-error-notifications` |
| 6.8. Performance Measurement | `api_perfmeas.html` |

Individual API function pages follow the pattern: `em<functionname>.html`
Examples: `eminitmaster.html`, `emconfiguremaster.html`, `emstart.html`, `emstop.html`, etc.

### 7. RAS-Server for EC-Lyser and EC-Engineer (`ras.html`)

| Section | Anchor |
|---------|--------|
| 7. RAS-Server | `ras.html` |
| 7.1. Integration Requirements | `#integration-requirements` |
| 7.2. API reference | `#application-programming-interface-reference` |

### 8. Error Codes (`error-codes.html`)

| Section | Anchor |
|---------|--------|
| 8. Error Codes | `error-codes.html` |
| 8.1. Groups | `#groups` |
| 8.2. Generic Error Codes | `#generic-error-codes` |
| 8.3. DCM Error Codes | `#dcm-error-codes` |
| 8.4. ADS over EtherCAT (AoE) Error Codes | `#ads-over-ethercat-aoe-error-codes` |
| 8.5. CAN application protocol over EtherCAT (CoE) SDO Error Codes | `#can-application-protocol-over-ethercat-coe-sdo-error-codes` |

---

## Class A Add-On User Manual — Complete Section Map

Base: `https://public.acontis.com/manuals/EC-Master/3.2/html/ec-master-class-a/`

### 1. Synchronization with Distributed Clocks (DC)

| Section | Page / Anchor |
|---------|---------------|
| 1. Synchronization with Distributed Clocks (DC) | `dc.html` |
| 1.1. Technical overview | `dc_technical.html` |
| 1.1.1. Support slaves and topologies | `dc_technical.html#support-slaves-and-topologies` |
| 1.2. Configuration with ET9000 | `dc_config.html` |
| 1.3. Configuration with EC-Engineer | `dc_config.html#configuration-with-ec-engineer` |
| 1.4. Programmer's Guide (DC API) | `dc_api.html` |

**DC API functions (anchors on `dc_api.html`):**
- `#emdcconfigure` — emDcConfigure
- `#emdcisenabled` — emDcIsEnabled
- `#emgetbustime` — emGetBusTime
- `#emdccontdelaycompenable` — emDcContDelayCompEnable
- `#emdccontdelaycompdisable` — emDcContDelayCompDisable
- `#emiocontrol-ec-ioctl-dc-slv-sync-status-get` — EC_IOCTL_DC_SLV_SYNC_STATUS_GET
- `#emiocontrol-ec-ioctl-dc-setsyncstartoffset` — EC_IOCTL_DC_SETSYNCSTARTOFFSET
- `#emiocontrol-ec-ioctl-dc-first-dc-slv-as-ref-clock` — EC_IOCTL_DC_FIRST_DC_SLV_AS_REF_CLOCK
- `#emfindinpvarbyname-inputs-bustime` — emFindInpVarByName (BusTime)

### 2. Master Synchronization (DCM)

| Section | Page / Anchor |
|---------|---------------|
| 2. Master synchronization (DCM) | `dcm.html` |
| 2.1. Technical overview | `dcm_technical.html` |
| 2.2. Configuration with ET9000 | `dcm_config.html` |
| 2.3. Programmer's Guide (DCM API) | `dcm_api.html` |
| 2.4. Code example | `dcm_example.html` |

### 3. Running EcMasterDemoDc (`ecmasterdemodc.html`)

| Section | Page / Anchor |
|---------|---------------|
| 3. Running EcMasterDemoDc | `ecmasterdemodc.html` |
| 3.1. Command line parameters | `ecmasterdemodc.html#command-line-parameters` |

---

## Python Programming Interface Manual — Section Map

Base: `https://public.acontis.com/manuals/EC-Master/3.2/html/ec-master-python/`

| Section | Page / Anchor |
|---------|---------------|
| 1. Introduction | `introduction.html` |
| 1.1. Requirements | `introduction.html#requirements` |
| 1.2. Architecture | `introduction.html#architecture` |
| 2. Programmers Guide | `programmers-guide.html` |
| 2.1. Sample Scripts | `programmers-guide.html#sample-scripts` |
| 2.2. Sample Code | `programmers-guide.html#sample-code` |
| 2.3. Wrapper | `programmers-guide.html#wrapper` |
| 2.3.1. Modules | `programmers-guide.html#modules` |
| 2.4. Supported IDEs | `programmers-guide.html#supported-ides` |
| 3. FAQ | `faq.html` |

---

## Key Cross-Reference: Common Topics → Best Link

This quick-reference table maps commonly asked topics to the most specific documentation page:

| Topic | Best Link |
|-------|-----------|
| Feature comparison (Class A vs B) | `.../ec-master-class-b/intro.html#the-ec-master-features` |
| Licensing & protected version | `.../ec-master-class-b/intro.html#protected-version` |
| License key procedure | `.../ec-master-class-b/intro.html#license` |
| ENI file / network configuration | `.../ec-master-class-b/gettingstarted.html#ethercat-network-configuration-eni` |
| Architecture overview | `.../ec-master-class-b/gettingstarted.html#ec-master-architecture` |
| Running the demo application | `.../ec-master-class-b/gettingstarted.html#running-ecmasterdemo` |
| Compiling the demo | `.../ec-master-class-b/gettingstarted.html#compiling-the-ecmasterdemo` |
| Network timing / cycle time | `.../ec-master-class-b/software-integration.html#network-timing` |
| Master startup sequence | `.../ec-master-class-b/software-integration.html#master-startup` |
| Process data access | `.../ec-master-class-b/software-integration.html#process-data-access` |
| Excluding features (EXCLUDE_*) | `.../ec-master-class-b/software-integration.html#excluding-features` |
| Reduced feature set | `.../ec-master-class-b/software-integration.html#reduced-feature-set` |
| Source code integration | `.../ec-master-class-b/software-integration.html#ethercat-master-stack-source-code` |
| Error detection & diagnosis | `.../ec-master-class-b/software-integration.html#error-detection-and-diagnosis` |
| Error codes reference | `.../ec-master-class-b/error-codes.html` |
| DCM error codes | `.../ec-master-class-b/error-codes.html#dcm-error-codes` |
| API reference overview | `.../ec-master-class-b/toc_api.html` |
| General API functions | `.../ec-master-class-b/api.html#general-functions` |
| Notification interface | `.../ec-master-class-b/api.html#generic-notification-interface` |
| Slave control functions | `.../ec-master-class-b/api.html#slave-control-and-status-functions` |
| Performance measurement | `.../ec-master-class-b/api_perfmeas.html` |
| Multiple bus support | `.../ec-master-class-b/api.html#multiple-ethercat-bus-support` |
| RAS-Server / Remote API | `.../ec-master-class-b/ras.html` |
| Link layer driver overview | `.../ec-master-class-b/emll.html` |
| Link layer initialization | `.../ec-master-class-b/emll_init.html` |
| Linux platform setup | `.../ec-master-class-b/os_linux.html` |
| Windows platform setup | `.../ec-master-class-b/os_windows.html` |
| FreeRTOS platform setup | `.../ec-master-class-b/os_freertos.html` |
| DC overview (Class A) | `.../ec-master-class-a/dc.html` |
| DC technical details | `.../ec-master-class-a/dc_technical.html` |
| DC configuration (EC-Engineer) | `.../ec-master-class-a/dc_config.html#configuration-with-ec-engineer` |
| DC Programmer's Guide / API | `.../ec-master-class-a/dc_api.html` |
| DCM overview | `.../ec-master-class-a/dcm.html` |
| DCM Programmer's Guide | `.../ec-master-class-a/dcm_api.html` |
| DCM code example | `.../ec-master-class-a/dcm_example.html` |
| Running DC demo | `.../ec-master-class-a/ecmasterdemodc.html` |
| Python interface | `.../ec-master-python/index.html` |
| Python sample code | `.../ec-master-python/programmers-guide.html#sample-code` |

---

## URL Pattern Rules

When constructing deep links, these patterns apply:

1. **All base URLs** use the pattern: `https://public.acontis.com/manuals/EC-Master/3.2/html/<manual-name>/`
2. **Section anchors** are lowercase, hyphen-separated slugs of the section title (e.g., "Excluding features" → `#excluding-features`)
3. **Individual API function pages** in Class B follow: `em<functionname>.html` (all lowercase, e.g., `eminitmaster.html`)
4. **OS-specific pages** follow: `os_<osname>.html` (e.g., `os_linux.html`, `os_windows.html`)
5. **Link-layer driver pages** follow: `emll<drivername>.html` (e.g., `emllicss.html`, `emllintelgbe.html`)
6. **Always prefer a specific page + anchor** over linking to `index.html` or the developer.acontis.com overview

---

*Last updated: March 2026 — based on EC-Master V3.2 documentation*
