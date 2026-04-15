# Step 5b — Generate Threagile Model and Risk Report

**Status:** [ ]

**Session rule:** Complete Part A (YAML generation) in one session, then run Part B (CLI) manually. Mark `[x]` when both are done, then stop.

**Prerequisites:** Steps 3 (component docs), 4 (interface map), and 5 (STRIDE) must be complete.

---

## Goal

Translate the architecture and threat analysis into a Threagile YAML model, then run Threagile to produce automated risk assessments and architectural threat diagrams.

---

## Part A — Agent generates `threagile.yaml` (AI session)

### Input

- Component documentation from Step 3: `03_component_documentation\*.md`
- Interface map from Step 4: `04_interface_map\*.md`
- STRIDE threat model from Step 5: `05_threat_model\index.md`

### Tasks

The agent reads the component docs and interface maps, then outputs a valid Threagile model file defining:
- `technical_assets` — one per component
- `trust_boundaries` — host kernel, host user-mode, guest VMs, network DMZ, web UI
- `communication_links` — all interfaces from Step 4 as data flows
- `shared_runtimes` — IVSHMEM, VMF framework
- `data_assets` — config data, VM images, credentials, logs

Tag each technical_asset with applicable EN 304 635 security objectives and EN 304 626 technical requirements.

### Agent prompt

```
You are a security architect generating a Threagile threat model YAML file for the
acontis hypervisor product family.

Read these documents:
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\03_component_documentation\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\04_interface_map\ (all files)
- C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05_threat_model\index.md

Generate a valid Threagile YAML model file (threagile.yaml) that maps the acontis hypervisor
system architecture. Follow the Threagile schema (see https://threagile.io).

Include: threagile_version, title, business_overview, technical_overview, trust_boundaries,
technical_assets, communication_links, data_assets.

Tag each technical_asset with applicable EN 304 635 security objectives
(e.g., tags: [en635-isolation, en635-integrity]) and EN 304 626 technical requirements
for Linux host OS assets (e.g., tags: [en626-TR-MISO, en626-TR-MSAF]).

Write the YAML file to:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\threagile.yaml

Also create a summary file:
C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\threagile_report.md
documenting: how many technical assets, trust boundaries, communication links, and
data assets were modeled, and any assumptions or simplifications made.

IMPORTANT: Ignore all folders named brainstormingPlatform or brainstormingPlatformPlus.
```

---

## Part B — Run Threagile CLI (shell command)

```bash
cd C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment
docker run --rm -v "%cd%\05b_threagile:/app/work" threagile/threagile -model /app/work/threagile.yaml -output /app/work/output
```

Or without Docker:
```bash
threagile -model 05b_threagile\threagile.yaml -output 05b_threagile\output
```

---

## Output files

Write to `C:\Users\s.zintgraf.ACONTIS\PROJ\ai-knowhow\bmad\security_assessment\05b_threagile\`:

- `threagile.yaml` — Agent-generated model
- `threagile_report.md` — Summary of what was modeled
- `output\` — Threagile-generated: `report.pdf`, `risks.json`, `data-flow-diagram.png`, etc.

---

## Verifiable result

- [ ] `threagile.yaml` exists and is valid YAML.
- [ ] `threagile_report.md` exists with model summary (asset/boundary/link counts).
- [ ] Threagile CLI runs without error (or YAML validation errors are fixed and re-run).
- [ ] `output\` directory contains Threagile-generated files (at minimum `risks.json`).

---

## Gate

```bash
# Part A gate
test -s "05b_threagile/threagile.yaml" && echo "PASS: YAML exists" || echo "FAIL: no YAML"
test -s "05b_threagile/threagile_report.md" && echo "PASS: report exists" || echo "FAIL: no report"
python -c "import yaml; yaml.safe_load(open('05b_threagile/threagile.yaml'))" && echo "PASS: valid YAML" || echo "FAIL: invalid YAML"

# Part B gate (after Threagile CLI run)
test -d "05b_threagile/output" && echo "PASS: output dir exists" || echo "FAIL: no output dir"
test -s "05b_threagile/output/risks.json" && echo "PASS: risks.json" || echo "FAIL: no risks.json"
```

**Human interaction:** Minimal. If Threagile fails with YAML validation, paste the error into a fresh session to fix. Expect 0-2 correction rounds.
