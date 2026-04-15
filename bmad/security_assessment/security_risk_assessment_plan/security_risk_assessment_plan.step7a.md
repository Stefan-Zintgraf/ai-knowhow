# Step 7a — Semgrep Built-in Scans

**Status:** [ ]

**Session rule:** Run the scans, summarize results, run the gate, mark `[x]`, then stop.

**Prerequisites:** None (can run in parallel with Steps 1-6). Source code at `rtv\` must be accessible.

---

## Goal

Run Semgrep's standard security rule packs against the source code to find known vulnerability patterns automatically. No AI agent needed for the scan itself — only for summarization.

---

## Part A — Run Semgrep CLI (shell commands)

Execute from `C:\Users\s.zintgraf.ACONTIS\PROJ\rtv`:

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

---

## Part B — Summarize results (AI agent session)

### Agent prompt

```
You are a security analyst summarizing Semgrep SAST scan results.

Read the Semgrep JSON output files at:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\raw_*.json

For each finding, extract: rule ID, severity, file path, line number, message, CWE.
Group findings by severity (Error > Warning > Info) and by component area.
De-duplicate identical findings across rule packs.

Produce:
- index.md: Overview with total finding counts per severity and per component area.
  Include a table of which Semgrep rule packs were run.
- builtin_scan_results.md: Full findings table grouped by component area.
  Columns: Severity | Rule ID | CWE | File | Line | Description | Component Area.

Cross-reference with the threat model:
Read C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\index.md
For each Semgrep finding, note if it confirms a STRIDE threat ID.

Write output to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\
```

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\07_semgrep\`:

- `raw_c_results.json` — Raw C/C++ scan
- `raw_csharp_results.json` — Raw C# scan
- `raw_owasp_results.json` — Raw OWASP scan
- `raw_js_results.json` — Raw JS/TS scan
- `index.md` — Summary with counts
- `builtin_scan_results.md` — Human-readable findings

---

## Verifiable result

- [ ] At least one `raw_*.json` file exists (scans completed).
- [ ] `index.md` exists with finding counts per severity and component area.
- [ ] `builtin_scan_results.md` exists with findings table.

---

## Gate

```bash
cd 07_semgrep
ls raw_*.json 2>/dev/null | wc -l  # Expect >= 1 JSON file
test -s index.md && echo "PASS: index" || echo "FAIL: no index"
test -s builtin_scan_results.md && echo "PASS: results" || echo "FAIL: no results"
```

**Human interaction:** None. Ignore Semgrep errors about unsupported syntax in older C files.
