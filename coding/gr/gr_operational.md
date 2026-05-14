# Guardrail: Operational and Agent Execution

Purpose: define what the agent must do during execution and what evidence it must produce. This is the operational contract for *how* the agent works, not *what* the code looks like.

---

## Apply When

- Any implementation task.

---

## Rules

### Op1. Discover Build and Test Commands Before Acting
The agent identifies the project's build, test, lint, and format commands (from `AGENTS.md`, `README`, `package.json`, `Makefile`, `pyproject.toml`, etc.) before making changes.

### Op2. Run Verification Locally
Before claiming the task is done, the agent runs the relevant build, tests, and static checks and reports the result.

### Op3. Definition of Done
A task is done only when:
- code change is complete,
- relevant tests pass (existing + new),
- linter and type checker pass,
- docs updated when behavior changed,
- verification evidence is included in the final response.

### Op4. Final-Response Format
The final response includes:
- a concise summary of what changed,
- which files were changed (or a diff summary),
- which verification commands were run and their outcome,
- any check that was skipped, with reason,
- any open question or follow-up.

### Op5. Use Project Tools, Not Personal Preferences
The agent uses the project's tooling versions and configurations. It does not switch package managers, formatters, or runtimes to suit itself.

### Op6. No Side Effects on the Developer Environment
The agent does not change global config, global packages, shell profiles, or other repositories without explicit instruction.

### Op7. Don't Skip Hooks or Checks
Pre-commit hooks, CI checks, and security scans are not bypassed (`--no-verify`, `--skip`, disabling rules) without explicit human decision and a recorded reason.

### Op8. Reproducible Steps
Anything the agent does should be reproducible: state the commands, inputs, and expected outputs.

### Op9. Cite Evidence for Claims
Claims about code state ("X is unused", "Y is covered by tests") cite the evidence (search result, test name, file path).

### Op10. Stop Cleanly on Failure
If a step fails (tests red, build broken), the agent stops, reports the failure, and asks rather than masking it.

### Op11. Generated-Code Volume Awareness
Very large diffs (many files, many lines) require explicit human approval before being produced or applied.

### Op12. No Silent Retry of Risky Operations
A failed risky operation (push, deploy, migration) is not retried automatically. The agent reports and waits.

---

## Anti-Patterns

- "All tests pass" without having run them.
- Bypassing a failing pre-commit hook with `--no-verify`.
- Installing a missing dependency globally on the user's machine.
- Auto-formatting the entire repo while fixing one bug.
- Disabling a linter rule to make the commit succeed.
- Claiming code is unused without showing the search that proves it.
