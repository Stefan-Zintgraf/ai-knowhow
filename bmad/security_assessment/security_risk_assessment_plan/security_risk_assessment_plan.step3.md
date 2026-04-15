# Step 3 — Document Components (Source-Level Analysis)

**Status:** [ ]

**Session rule:** Complete this step (or one sub-session), run the gate, mark `[x]`, then stop.

**Prerequisites:** Step 0a (BMAD baseline) should be complete for maximum efficiency. Can start without it but will be slower.

---

## Goal

For each major component, produce a markdown document describing its purpose, source structure, internal architecture, key data flows, external dependencies, and — critically — the security overlay: trust boundaries, privilege context, security-relevant patterns, and EN harmonised standard requirement mapping.

This step uses the structure from **Fabric's `extract_architecture` pattern** to ensure consistent output.

---

## Input

- `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\` (source code)
- **BMAD baseline documentation from Step 0a:** `rtv\_bmad-output\index.md` and associated files
- Existing documentation at `rtv\ai\`, `rtv\Hypervisor\Doc\`, component READMEs

## Sessions

Execute as **multiple parallel agent sessions**, one per component group:

| Session | Components to Document | Output File(s) |
|---|---|---|
| 3a | Framework VMF Core (`Framework\Source\Core\`) | `framework_vmf_core.md` |
| 3b | Windows Drivers (`Windows\Source\Driver\*`) | `windows_drivers.md` |
| 3c | Windows User-Mode (`Windows\Source\RtosLib\`, `RtosService\`, `SystemManager\`, `VmfInterfaceUserMode\`) | `windows_rtoslib.md`, `windows_rtosservice.md`, `windows_systemmanager.md` |
| 3d | Linux Components (`Linux\Source\*`, `Linux\target\hv\`) | `linux_drivers.md`, `linux_target_runtime.md` |
| 3e | Hypervisor Components (`Hypervisor\Source\*`) | `hypervisor_hvweb.md`, `hypervisor_hvdevicemgr.md`, `hypervisor_virtio_events.md` |
| 3f | LxWin/VxWin/SDK (`LxWin\Source\*`, `VxWin\Source\*`, `Common\All\*`) | `lxwin_yocto_drivers.md`, `vxwin_bsp.md`, `common_sdk.md`, `common_vmfcall_interface.md` |

## Required sections per component (Fabric `extract_architecture` structure)

1. **Overview** — Purpose and role (1-2 paragraphs)
2. **Source Structure** — Directory listing, file counts, languages
3. **Architecture & Key Data Structures** — Data structures, algorithms, design patterns, data-flow description
4. **External Dependencies** — OS APIs, third-party libraries, security-sensitive dependencies
5. **Interfaces Provided and Consumed** — APIs exposed/consumed, data formats, validation, auth
6. **Privilege & Trust Context** — Privilege level, trust zones, boundary crossings
7. **Configuration & Runtime Parameters** — Security-relevant defaults
8. **Security-Relevant Patterns** — Crypto, auth, input validation, memory management, network, IPC, error handling
9. **Data Flow Summary** — One paragraph for STRIDE/Threagile input
10. **Applicable Harmonised Standard Requirements** — EN 304 635 and/or EN 304 626 mapping with compliance status (Met/Partially Met/Not Met/Unknown), evidence, gaps

---

## Agent prompt template

```
You are a security-focused source code analyst. Your task is to document the
following component(s) of the acontis hypervisor system for a security risk assessment.

FIRST: Read the BMAD baseline documentation for architecture context:
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\_bmad-output\index.md (master index)
- Any architecture or deep-dive files relevant to the component(s) below
Use this as your starting point — do not rediscover what BMAD already documented.
Focus your effort on the SECURITY-SPECIFIC sections that the baseline does not cover.

Component(s) to analyze:
- [INSERT COMPONENT NAME]: C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\[INSERT PATH]

For each component, produce a markdown file with sections §1-§10 as defined in the
step file (security_risk_assessment_plan.step3.md).

For §10 (Applicable Harmonised Standard Requirements):

For hypervisor/virtualization components: Reference EN 304 635 §5.1.1.
For management/orchestration components: Reference EN 304 635 §5.1.3.
For Linux host OS components: Reference EN 304 626 §5.2 (TR-* requirements).

The harmonised standard PDFs are located at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-626_V0.1.0_2025-12-23_Operating-Systems_Mature-draft.pdf
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\EN-304-635_V0.0.10_2025-12-09_Virtualisation-Container_Mature-draft.pdf

Read the actual source files — do not guess or hallucinate file contents.
Cite specific file paths and line ranges where relevant.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\`:

- `index.md` — Component overview + navigation
- `framework_vmf_core.md`
- `windows_drivers.md`
- `windows_rtoslib.md`
- `windows_rtosservice.md`
- `windows_systemmanager.md`
- `linux_drivers.md`
- `linux_target_runtime.md`
- `hypervisor_hvweb.md`
- `hypervisor_hvdevicemgr.md`
- `hypervisor_virtio_events.md`
- `lxwin_yocto_drivers.md`
- `vxwin_bsp.md`
- `common_sdk.md`
- `common_vmfcall_interface.md`

---

## Verifiable result

- [ ] All 15 component documentation files (14 components + index) exist under `03_component_documentation\`.
- [ ] Each component file has all 10 required sections (§1 through §10).
- [ ] §10 (EN requirement mapping) contains at least one compliance status entry per component.
- [ ] §9 (Data Flow Summary) is suitable as Threagile/STRIDE input.
- [ ] All files are non-empty.

---

## Gate

```bash
# Verify all expected files exist and are non-empty
cd 03_component_documentation
for f in index.md framework_vmf_core.md windows_drivers.md windows_rtoslib.md windows_rtosservice.md windows_systemmanager.md linux_drivers.md linux_target_runtime.md hypervisor_hvweb.md hypervisor_hvdevicemgr.md hypervisor_virtio_events.md lxwin_yocto_drivers.md vxwin_bsp.md common_sdk.md common_vmfcall_interface.md; do
  test -s "$f" && echo "PASS: $f" || echo "FAIL: $f"
done

# Verify section completeness (spot-check one file)
grep -c "^## " framework_vmf_core.md  # Expect >= 10 sections
```

**Human interaction:** Minimal — choose which component sessions to run first based on priority. All 6 sessions can run independently.
