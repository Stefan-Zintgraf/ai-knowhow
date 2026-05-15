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

Large diffs hide unintended changes. The agent stops and asks for explicit approval before producing or applying a change that crosses any of these defaults:

- more than 5 files touched (excluding lockfiles, generated code, snapshots),
- more than 200 LOC added+removed in non-generated files,
- more than one module/package boundary crossed,
- any single file with more than 100 LOC changed.

Projects may override these numbers in `AGENTS.md` or an equivalent root-level config; the project's numbers win when present.

### Op12. No Silent Retry of Risky Operations

A failed risky operation (push, deploy, migration) is not retried automatically. The agent reports and waits.

### Op13. No Fabrication

The agent does not invent code-level facts. Function names, types, file paths, library APIs, config keys, CLI flags, error codes, and version numbers referenced in plans, code, or messages must be verified against the actual source (grep, read, official docs) before being stated. If verification is not possible in the current context, the item is marked as an assumption per Gov2 — never asserted as fact.

### Op14a. Keep Persistent Context Small

Always-on instructions (system prompt, `CLAUDE.md`-equivalent, project AI rules) push the agent toward the dumb zone before work begins. The agent and project maintainers keep the persistent context minimal: only what every task needs. Detail documents (guardrail categories, conventions, architecture notes, domain glossaries) are kept retrievable, not pushed by default.

Rationale: attention-relationship cost grows sharply with tokens. Large persistent prompts consume budget before the task starts.

### Op14b. Push vs Pull for Standards

The default delivery of coding standards and guardrail detail documents depends on the agent's role:

- **Implementer (`ral`, `par`, ad-hoc implementation)** — standards are **pulled**: retrieved on demand when the routing step (`guardrails.md` §5) selects a category. The implementer does not load every detail document by default.
- **Reviewer (`rev`)** — standards are **pushed**: the routed detail documents are loaded into the reviewer's context up front, because review compares the diff against the standards (cross-reference: gr_review.md Rev2).
- **Aligner (`aln`) and planner (`prd`, `iss`)** — standards are pulled on demand, biased toward planning-relevant categories (governance, architecture, modules, alignment).

A change to a standard updates the pulled detail document; the implementer picks up the change on the next routing pass. A reviewer setup explicitly re-loads the pushed set per review session.

### Op14. Read Before Write

Before modifying a function, type, file, or configuration value, the agent reads the affected unit and its callers/consumers within the current context budget. "Read" means actual file contents loaded in this session — not memory of similar code or pattern recognition from the name. Edits to code the agent has not read must be flagged as such, and the agent must ask before proceeding. This rule reinforces Op13: reading first is the primary defense against fabrication.

---

## Anti-Patterns

- "All tests pass" without having run them.
- Bypassing a failing pre-commit hook with `--no-verify`.
- Installing a missing dependency globally on the user's machine.
- Auto-formatting the entire repo while fixing one bug.
- Disabling a linter rule to make the commit succeed.
- Claiming code is unused without showing the search that proves it.
- Writing `import { foo } from "lib"` without checking that `lib` actually exports `foo`.
- Citing a config key (`app.cache.ttl`) that does not exist in the project.
- Referencing a "well-known" function from memory rather than the project's actual code.
- Quoting an error code or CLI flag without verifying it.
- Editing a function whose body was never opened in this session.
- Renaming a symbol without searching for its references.
- Adding a parameter to a function without checking call sites.
- Changing a config value without reading what consumes it.
- Loading every guardrail detail document into the implementer's context "just in case."
- Reviewing a diff with standards only available on demand instead of pushed up front.
- Letting the always-on system prompt grow until the first task starts in the dumb zone.
