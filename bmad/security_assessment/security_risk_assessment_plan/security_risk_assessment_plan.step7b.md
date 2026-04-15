# Step 7b — Custom Semgrep Rules for Trust Boundaries

**Status:** [ ]

**Session rule:** Complete this step (rule generation + scan), run the gate, mark `[x]`, then stop.

**Prerequisites:** Step 4 (interface map) must be complete. Step 7a (built-in scans) should be complete to avoid duplication.

---

## Goal

Have an AI agent write custom Semgrep rules that target the specific trust boundaries and interface patterns identified in Step 4, then run them against the codebase.

---

## Input

- Interface map from Step 4: `04_interface_map\*.md`
- Component documentation from Step 3: `03_component_documentation\*.md`
- Built-in scan results from Step 7a: `07_semgrep\builtin_scan_results.md`

## Custom rules to generate

| Trust Boundary | Rule Target |
|---|---|
| **VMF call dispatch** | Flag `vmfCall*` handlers that read size/length/offset without bounds checking |
| **Driver IOCTLs** | Flag IOCTL handlers using `ProbeForRead`/`copy_from_user` with user-supplied length without validation |
| **IVSHMEM shared memory** | Flag shared memory offset/index accesses without bounds validation |
| **HvWeb API endpoints** | Flag controller actions missing `[Authorize]`; string concatenation in queries |
| **Configuration parsing** | Flag config reads where parsed values are used as sizes without range checking |

---

## Agent prompt

```
You are a security engineer writing custom Semgrep rules for the acontis hypervisor product family.

Read the interface documentation:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)

Read existing Semgrep results to avoid duplicating coverage:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\builtin_scan_results.md

Read key source files at trust boundaries:
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Common\All\SDK\Inc\vmfInterface.h
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Windows\Source\Driver\RtosDrv\Vmf\ (vmfDrvInterface files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Linux\Source\Driver\hrtosdrv\Vmf\ (vmfDrvInterface files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\rtv\Framework\Source\Core\ (IVSHMEM-related files)

Write Semgrep rules (YAML format) for these trust boundaries:
1. vmf_call_validation.yaml
2. ioctl_input_validation.yaml
3. ivshmem_bounds.yaml
4. web_injection.yaml

Each rule file should follow Semgrep syntax with: id, patterns, message, severity, languages, metadata (cwe, confidence).

Write rule files to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\custom_rules\

After writing rules, provide the shell commands to run them.

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

### After rule generation, run the custom rules:

```bash
cd C:\Users\s.zintgraf.ACONTIS\PROJ
semgrep --config=ai-knowhow/bmad/security_assessment/07_semgrep/custom_rules/ \
  --exclude="**/brainstormingPlatform/**" --exclude="**/brainstormingPlatformPlus/**" \
  --include="*.c" --include="*.cpp" --include="*.h" --include="*.cs" --include="*.ts" \
  rtv/ \
  --json -o ai-knowhow/bmad/security_assessment/07_semgrep/raw_custom_results.json
```

Then summarize results into `custom_scan_results.md` using the same summarization approach as Step 7a.

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\`:

- `custom_rules\vmf_call_validation.yaml`
- `custom_rules\ioctl_input_validation.yaml`
- `custom_rules\ivshmem_bounds.yaml`
- `custom_rules\web_injection.yaml`
- `raw_custom_results.json` — Raw scan results
- `custom_scan_results.md` — Human-readable findings

---

## Verifiable result

- [ ] All 4 custom rule YAML files exist under `custom_rules\`.
- [ ] Each rule file is valid Semgrep YAML (has `rules:` key with at least one rule).
- [ ] `raw_custom_results.json` exists (scan was run).
- [ ] `custom_scan_results.md` exists with findings summary.

---

## Gate

```bash
cd 07_semgrep
for f in custom_rules/vmf_call_validation.yaml custom_rules/ioctl_input_validation.yaml custom_rules/ivshmem_bounds.yaml custom_rules/web_injection.yaml; do
  test -s "$f" && echo "PASS: $f" || echo "FAIL: $f"
done

# Verify rules are valid YAML with 'rules' key
for f in custom_rules/*.yaml; do
  grep -q "^rules:" "$f" && echo "PASS: $f has rules" || echo "FAIL: $f missing rules key"
done

test -s raw_custom_results.json && echo "PASS: scan results" || echo "FAIL: no scan results"
test -s custom_scan_results.md && echo "PASS: summary" || echo "FAIL: no summary"
```

**Human interaction:** Minimal. Agent-generated rules may need 1-2 rounds of tuning for false positives.
