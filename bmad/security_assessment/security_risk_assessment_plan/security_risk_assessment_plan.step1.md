# Step 1 — Extract Artifact Registry from Build Scripts

**Status:** [ ]

**Session rule:** Complete this step, run the gate, mark `[x]`, then stop.

**Prerequisites:** None (can run in parallel with Step 0a).

---

## Goal

Produce a complete inventory of every binary artifact (DLL, EXE, SYS, SO, kernel module, setup package) built by the automated build process.

---

## Input

- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\` (all `bld*.bat` files)
- `C:\Users\s.zintgraf.ACONTIS\PROJ\buildprogram\CfgDefault.bat`
- `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Workspace\WindowsVS2015\Setup\*.wixproj`

## Tasks

1. Parse `CfgDefault.bat` to extract all `RTE_Build*`, `RTE_Dir*`, `RTE_Binary*`, `RTE_Product*` variables.
2. Scan all `bld*.bat` files for artifact output patterns:
   - `devenv.com ... /rebuild` or `msbuild` invocations → `.dll`, `.exe`, `.sys` outputs
   - `copy` / `xcopy` commands targeting release/output directories
   - `Sign.bat` invocations (signed artifacts are deployed binaries)
   - `candle` / `light` (WiX) invocations → MSI/EXE installer outputs
3. Scan `rtv\Workspace\WindowsVS2015\Setup\*.wixproj` for packaged artifact names.
4. For Linux artifacts, scan `bld50_lx\`, `bld50_hv\` for remote build outputs and delivery paths.
5. Record for each artifact: **name**, **type** (DLL/EXE/SYS/SO/MSI), **build script**, **output path pattern**, **signing status**.

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\01_artifact_registry\`:

- `index.md` — Master artifact list with counts
- `windows_artifacts.md` — Windows DLLs, EXEs, SYS drivers
- `linux_artifacts.md` — Linux SOs, binaries, kernel modules
- `installer_artifacts.md` — MSI, WiX bundles, setup EXEs
- `prebuilt_external.md` — Third-party / prebuilt binaries

Use tables with columns: **Artifact Name | Type | Build Script | Output Path | Signed | Notes**.

---

## Agent prompt

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

---

## Verifiable result

- [ ] `01_artifact_registry\index.md` exists, non-empty, contains artifact counts.
- [ ] `01_artifact_registry\windows_artifacts.md` exists, non-empty, contains artifact table.
- [ ] `01_artifact_registry\linux_artifacts.md` exists, non-empty, contains artifact table.
- [ ] `01_artifact_registry\installer_artifacts.md` exists, non-empty, contains artifact table.
- [ ] `01_artifact_registry\prebuilt_external.md` exists (may be empty if no prebuilt binaries found; document that).

---

## Gate

```bash
# Verify all output files exist and are non-empty
for f in index.md windows_artifacts.md linux_artifacts.md installer_artifacts.md prebuilt_external.md; do
  test -s "01_artifact_registry/$f" && echo "PASS: $f" || echo "FAIL: $f"
done

# Verify index.md contains artifact count summary
grep -qi "total\|count\|artifact" 01_artifact_registry/index.md && echo "PASS: counts present" || echo "FAIL: no counts"
```

**Human interaction:** None required. Review output for completeness afterward.
