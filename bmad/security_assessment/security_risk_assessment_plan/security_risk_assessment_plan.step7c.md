# Step 7c — AI-Driven Code Vulnerability Deep-Dive

**Status:** [ ]

**Session rule:** Complete one or more deep-dive sessions, run the gate, mark `[x]`, then stop.

**Prerequisites:** Steps 6 (risk assessment) and 7a-7b (Semgrep) must be complete.

---

## Goal

Targeted agent-driven deep-dive into the highest-risk code areas that Semgrep cannot fully analyze — cross-function logic, complex race conditions, architectural weaknesses.

Uses the approach from **Fabric's `find_vulnerabilities` pattern**.

---

## Input

- Top threats from `06_risk_assessment\risk_matrix.md` (Critical and High items)
- Semgrep findings from Steps 7a-7b: `07_semgrep\*.md`
- Source code in `rtv\`

## Vulnerability categories to investigate

For each Critical/High threat **not already covered by Semgrep findings**:

1. Cross-function data flow issues (tainted input flowing through multiple functions)
2. Race conditions (TOCTOU in shared memory, concurrent access)
3. Object lifetime issues (use-after-free, dangling pointers across callbacks)
4. Logic flaws in authentication/authorization (bypassable through parameter manipulation)
5. Complex injection chains (second-order injection, path traversal)
6. Cryptographic misuse (weak algorithms, predictable IVs, key reuse)
7. Error handling that leaks sensitive information or fails open
8. Hardcoded credentials or keys
9. Insecure default configurations
10. Logic errors in VMF call parameter validation

## Sessions

Run 2-5 parallel sessions, one per high-risk area:

| Session | Focus Area | Source Paths |
|---|---|---|
| 7c-1 | VMF Core + Guest Escape | `Framework\Source\Core\`, `Common\All\SDK\Inc\vmfInterface.h` |
| 7c-2 | Kernel Drivers | `Windows\Source\Driver\`, `Linux\Source\Driver\` |
| 7c-3 | HvWeb + SystemManager | `Hypervisor\Source\HvWeb\`, `Windows\Source\SystemManager\` |
| 7c-4 | Network (MQTT, virtio, IVSHMEM) | `Hypervisor\Source\MQTTnet\`, `Hypervisor\Source\virtio_events\`, IVSHMEM in Core |
| 7c-5 | Build/Supply Chain | `buildprogram\`, signing scripts, third-party binaries |

---

## Agent prompt template

```
You are a security code auditor performing a deep vulnerability analysis on the
acontis hypervisor product family. Focus on vulnerabilities that SAST tools like
Semgrep CANNOT find — cross-function logic, race conditions, architectural flaws.

Read the threat model for [AREA]:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\threat_model_[AREA].md

Read the Semgrep results to see what has ALREADY been found:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\builtin_scan_results.md
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\custom_scan_results.md

For each Critical/High threat NOT confirmed by Semgrep, read the source files and
perform deep analysis. For each finding, provide (Fabric find_vulnerabilities structure):
- Vulnerability title, CWE, Severity
- Affected file(s) and line number(s) — cite EXACT paths and lines
- Description and exploitation scenario
- Recommended fix

Append a "## Code-Level Findings" section to the existing threat model file at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\threat_model_[AREA].md

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

---

## Output

- Code-level findings appended to existing `05_threat_model\threat_model_*.md` files as `## Code-Level Findings` sections.
- Updated `06_risk_assessment\risk_matrix.md` with refined scores where code-level evidence changes severity.

---

## Verifiable result

- [ ] At least 2 threat model files have a `## Code-Level Findings` section appended.
- [ ] Each code-level finding cites specific file paths and line numbers.
- [ ] `risk_matrix.md` is updated where findings change severity.

---

## Gate

```bash
# Check at least 2 threat model files have code-level findings
count=0
for f in 05_threat_model/threat_model_*.md; do
  grep -q "Code-Level Findings" "$f" && count=$((count+1))
done
[ "$count" -ge 2 ] && echo "PASS: $count files with code findings" || echo "FAIL: only $count files"
```

**Human interaction:** Choose which high-risk areas to audit first based on Step 6 risk matrix.
