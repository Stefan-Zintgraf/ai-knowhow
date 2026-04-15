# Step 2 — Map Artifacts to Products

**Status:** [ ]

**Session rule:** Complete this step, run the gate, mark `[x]`, then stop.

**Prerequisites:** Step 1 (artifact registry) must be complete.

---

## Goal

Create a cross-reference showing which artifacts ship in which product(s), identifying shared components.

---

## Input

- Output from Step 1: `01_artifact_registry\*.md`
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\CfgDefault.bat` (product flags and directory mappings)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\Build.bat` (`:SubCreateProducts` logic)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\bld80_setup\bld40_Setup*.bat` (per-product setup scripts)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Workspace\WindowsVS2015\Setup\*.wixproj` (WiX product definitions)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\*\Setup\Wix\` directories (per-product WiX sources)

## Tasks

1. Parse `CfgDefault.bat` for the 7 product definitions and their directory/flag mappings.
2. For each product, trace the build flow through `Build.bat` → `BuildSub.bat` → `bld50_*` → `bld80_setup`.
3. Examine WiX `.wxs` source files under each product's `Setup\Wix\` to find which binaries are included in each installer.
4. Cross-reference with the artifact registry from Step 1.
5. Identify artifacts shared across multiple products vs. product-specific artifacts.

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\02_product_artifact_map\`:

- `index.md` — Cross-reference matrix (rows=artifacts, columns=products)
- `product_vxwin.md` — VxWin artifact list
- `product_cewin.md` — CeWin artifact list
- `product_vmfwin.md` — VmfWin artifact list
- `product_rtos32win.md` — RTOS32Win artifact list
- `product_ecwinrtos32.md` — EC-WinRTOS-32 artifact list
- `product_lxwin.md` — LxWin artifact list
- `product_hypervisor.md` — Hypervisor (RTOSVisor) artifact list

Each per-product file lists all artifacts with their role and whether shared or exclusive.

---

## Agent prompt

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

---

## Verifiable result

- [ ] `02_product_artifact_map\index.md` exists with cross-reference matrix.
- [ ] Per-product files exist for all 7 products (plus index = 8 files total).
- [ ] Shared vs. exclusive artifacts are clearly marked in per-product files.
- [ ] All files are non-empty.

---

## Gate

```bash
# Verify all 8 output files exist and are non-empty
for f in index.md product_vxwin.md product_cewin.md product_vmfwin.md product_rtos32win.md product_ecwinrtos32.md product_lxwin.md product_hypervisor.md; do
  test -s "02_product_artifact_map/$f" && echo "PASS: $f" || echo "FAIL: $f"
done

# Verify index.md contains a cross-reference matrix
grep -qi "matrix\|cross-reference\|artifact.*product\|product.*artifact" 02_product_artifact_map/index.md && echo "PASS: matrix present" || echo "FAIL: no matrix"
```

**Human interaction:** None required.
