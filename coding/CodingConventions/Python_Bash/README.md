# Python/Bash Coding Conventions -- Entry Point

> **Read this file first.** It is the index and routing map for this folder.
> Do not load individual guardrail or guideline files until you have identified
> your use case in section 2.

## 1 What this folder is

A reusable, agent-oriented convention framework for projects written in
**Python** and (optionally) **Bash**. It provides:

- enforceable coding rules with stable IDs (`PY-MUST-*`, `SH-MUST-*`)
- a mandatory code review gate that runs before any test execution
- an execution contract that tells an AI agent exactly what to read, in what
  order, and what evidence to produce
- templates to copy into a new project, plus one worked project instantiation

It is **not** a runnable project. Nothing here is executed; everything is
policy, templates, and reference material.

## 2 Routing map -- what to read for which task

| Your task | Read, in this order |
| --- | --- |
| Implement or change **Python** code in a project that adopted this framework | `impl_guidelines_*.md` -> `impl_guardrails_*.md` -> `guardrails/python_guardrails.md` -> mapped modules in `guardrails/python/` -> `code_review.md` |
| Implement or change **Bash** code | `impl_guidelines_*.md` -> `impl_guardrails_*.md` -> `guardrails/bash_guardrails.md` -> mapped modules in `guardrails/bash/` -> `code_review.md` |
| Change touches **both** languages | Both rows above; both rule sets apply in full |
| Review code before tests | `code_review.md` + `guardrails/compliance_matrix_template.md` |
| Bootstrap this framework into a **new** project | `impl_guidelines_template.md` -> `impl_guidelines_project.md` -> `impl_guardrails_template.md` -> `impl_guardrails_project.md` (see section 5) |
| Understand or amend a rule's rationale | `guardrails/sources/` (local snapshots of the upstream style guides) |

## 3 File inventory

### 3.1 Top level -- workflow controls

| File | Role |
| --- | --- |
| `README.md` | This file. Index and routing map. |
| `impl_guidelines_template.md` | **Template.** Cross-cutting project rules, sections 1-12: language strategy, host prerequisites, repo structure, interface contracts, version pinning, output conventions, decomposition policy, testing architecture, readiness gate. |
| `impl_guidelines_project.md` | **Instantiation.** Checklist form of the above; tick the sections a given project adopts and record project-specific decisions. |
| `impl_guardrails_template.md` | **Template.** Agent execution contract, sections G1-G6: applicability, per-step and per-test workflow, non-negotiable rules, required checks baseline, compliance matrix, completion report. |
| `impl_guardrails_project.md` | **Instantiation.** The SBOM project's filled-in version of G1-G6, including run-config and progress-tracking specifics. |
| `code_review.md` | **Mandatory pre-test gate.** Review workflow, finding severities (`BLOCKER`/`MAJOR`/`MINOR`), exit criteria, and the review record format. Tests must not run until this passes. |

### 3.2 `guardrails/` -- enforceable rules

| File | Role |
| --- | --- |
| `guardrails/README.md` | Folder-level index and required workflow. |
| `guardrails/python_guardrails.md` | `PY-MUST-01` .. `PY-MUST-09` plus SHOULD rules and the Python quality-gate commands. |
| `guardrails/bash_guardrails.md` | `SH-MUST-01` .. `SH-MUST-11` plus SHOULD rules and the Bash quality-gate commands. |
| `guardrails/compliance_matrix_template.md` | The evidence table. Every applicable rule ID gets `PASS`, `N/A` (with rationale), or `FAIL`. |
| `guardrails/python/` | Detail modules: `typing_interfaces.md`, `imports_structure.md`, `error_and_resource_safety.md`, `function_design_and_state.md`, `documentation_and_todos.md`, `quality_gates.md`. |
| `guardrails/bash/` | Detail modules: `script_scaffold_and_entrypoint.md`, `quoting_and_expansion.md`, `variables_and_scope.md`, `error_handling.md`, `quality_gates.md`. |
| `guardrails/sources/` | Local HTML snapshots of the upstream basis: Google Python Style Guide, Google Shell Style Guide, Hitchhiker's Guide to Python, ShellCheck Wiki, Defensive Bash Programming. Reference only -- never normative over the rule files. |

### 3.3 Rule ID -> detail module map

Python:

| Rule IDs | Module |
| --- | --- |
| `PY-MUST-01` | `guardrails/python/typing_interfaces.md` |
| `PY-MUST-02` | `guardrails/python/imports_structure.md` |
| `PY-MUST-03`, `PY-MUST-04` | `guardrails/python/error_and_resource_safety.md` |
| `PY-MUST-05`, `PY-MUST-06` | `guardrails/python/function_design_and_state.md` |
| `PY-MUST-07`, `PY-MUST-08` | `guardrails/python/documentation_and_todos.md` |
| `PY-MUST-09` | `guardrails/python/quality_gates.md` |

Bash:

| Rule IDs | Module |
| --- | --- |
| `SH-MUST-01`, `SH-MUST-02`, `SH-MUST-06`, `SH-MUST-07` | `guardrails/bash/script_scaffold_and_entrypoint.md` |
| `SH-MUST-03`, `SH-MUST-09`, `SH-MUST-10` | `guardrails/bash/quoting_and_expansion.md` |
| `SH-MUST-04`, `SH-MUST-05` | `guardrails/bash/variables_and_scope.md` |
| `SH-MUST-08` | `guardrails/bash/error_handling.md` |
| `SH-MUST-11` | `guardrails/bash/quality_gates.md` |

## 4 The core loop (condensed)

For any implementation step:

1. Read the project's guidelines + guardrails files.
2. Identify the changed language(s); load **all** applicable `MUST` rules.
3. Load the mapped detail modules for those rule IDs.
4. Implement only the scoped requirements of the current step.
5. Run the required checks (section 4.1).
6. Run the `code_review.md` gate; fix every `BLOCKER` and `MAJOR`.
7. Only then run tests.
8. Produce the completion report with a filled compliance matrix.

### 4.1 Required checks baseline

Canonical source: `impl_guardrails_*.md` section G4. If a command changes,
change it there first, then align `code_review.md` and the language guardrails.

Python:

```bash
ruff check .
ruff format --check .
mypy .
pytest -q
```

Bash:

```bash
shfmt -d .
find . -type f -name '*.sh' -print0 | xargs -0 shellcheck
```

## 5 Template vs. project files

Files come in pairs. `*_template.md` is the generic, reusable version with
`<placeholders>`; `*_project.md` is a concrete instantiation (currently for the
SBOM project). Section numbers are deliberately aligned between the two so a
project file can be traced back to its template section.

To adopt this framework in a new project:

1. Copy `impl_guidelines_template.md` and `impl_guardrails_template.md` into the
   project's `plan/` folder, plus the whole `guardrails/` tree.
2. Create project instantiations modelled on `impl_guidelines_project.md` and
   `impl_guardrails_project.md`: fill placeholders, mark inapplicable sections
   `N/A`, and drop the Bash sections if Bash is out of scope.
3. Confirm the readiness gate (guidelines section 12) before coding starts.

## 6 Precedence

1. Project step specification -- authoritative for step-specific domain behavior.
2. `impl_guardrails_*.md` -- authoritative for workflow, checks, and evidence.
3. `impl_guidelines_*.md` -- authoritative for cross-cutting project rules.
4. `guardrails/*_guardrails.md` -- authoritative for the rule text and IDs.
5. `guardrails/<lang>/*.md` -- authoritative for rule detail and examples.
6. `guardrails/sources/` -- background rationale only, never normative.

If a step file conflicts with a cross-cutting rule, fix the cross-cutting file
first, then align the step files.

## 7 Maintenance rules

- Rule IDs are stable. Never renumber; retire an ID rather than reuse it.
- Adding a `MUST` rule requires: an entry in the language guardrail table, a
  mapped detail module, and a new row in `compliance_matrix_template.md`.
- Any change to the quality-gate commands must be made in `impl_guardrails_*.md`
  G4 first, then propagated to `code_review.md` and the language guardrails.
- Update this README's inventory whenever a file is added or removed.

---

## Revision History

<!-- Latest entries first. Add new rows directly below the header row. -->

<!-- Same-day revisions: append .2, .3, ... to the date (e.g. 2026-07-29.2). -->

| Date | Change |
| ---- | ------ |
| 2026-07-29 | Initial version. Added folder entry point with routing map, file inventory, rule-ID map, core loop, and precedence rules. |
