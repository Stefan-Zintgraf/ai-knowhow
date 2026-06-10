# Guardrail: Documentation

Purpose: keep documentation concise, durable, and aligned with the code.

---

## Apply When

- README, architecture notes, API docs, or user-facing docs are created or changed.
- Code comments are added or modified.
- Decisions worth recording outlive the current task.

---

## Rules

### Doc1. Don't Create Docs the User Didn't Ask For

The agent does not produce extra Markdown files (plans, summaries, retrospectives, "AI notes") unless explicitly requested.

### Doc2. Document the Why, Not the What

Documentation captures rationale, constraints, and non-obvious decisions. It does not narrate code or restate identifiers.

### Doc3. Keep Documentation Close to Code

Documentation lives near the code it describes (same module, same file, or a `README.md` in the directory). Long-distance docs rot fast.

### Doc4. Update Docs When Behavior Changes

A behavior change must update the docs that describe that behavior, in the same change.

### Doc5. No Duplication of Authoritative Sources

If the truth lives in code, generated API specs, or schemas, the docs link to it rather than copy it.

### Doc6. Comments Default to None

Default to no comment. Add a comment only when the *why* is non-obvious and would surprise a future reader.

### Doc7. No "Added by AI" or Task-Referencing Comments

Comments do not mention the AI, the current task, the PR, or the ticket. Such references rot.

### Doc8. Architecture Decisions Are Recorded Briefly

If a decision is durable (technology choice, boundary, trade-off), record it in one short ADR or note. Long essays are discouraged.

### Doc9. Examples Are Minimal and Tested

Code examples in docs are short, runnable, and ideally covered by a test so they stay correct.

### Doc10. Match the Project's Documentation Style

Follow the project's existing structure, tone, and Markdown conventions. Don't introduce a new doc system.

### Doc11. Retire Stale PRDs and Plans (Prevent Doc Rot)

Old PRDs and implementation plans must not be kept indefinitely in the repository files. Stale documentation can actively poison the context of future agents. Store journey documents and PRDs in external systems (e.g., GitHub Issues) and close them when the work is complete to preserve architectural history without polluting the active codebase.

Enforcement: PRD bodies are forbidden in the working tree entirely — no tree artifact exists to "retire," so the gate is "prevent it from being authored in-tree in the first place." Pre-commit lint rejects paths matching `prd/**`, `**/PRD-*.md`, or `**/*_prd.md`; the canonical PRD location is the owning GitHub Issue. `qa` Q11 verifies the same condition at the merge gate as a belt-and-braces check. (Distinct from Res3 research retirement, where the artifact legitimately lives in-tree during the sprint and must be deleted on owner-issue close.)

### Doc12. Document Public Interfaces (APIs)

Any function, class, or type exported for cross-module or external consumption constitutes a "Public API." While internal implementation comments should be rare (`Doc6`), every public API must have a clear docstring/comment defining its behavioral contract, expected inputs, and error states. This documentation serves as the "cognitive handle" for both humans and agents. The project should maintain an auto-generated snapshot file (e.g., `public_api.md` generated via Python/AST script). Agents must not manually edit this file; instead, it is regenerated to objectively detect public API drift during review.

---

## Anti-Patterns

- A new `NOTES.md` after every task.
- Keeping old PRDs in the repository forever.
- Block comments restating what the function signature already says.
- Exporting a cross-module function without documenting its behavioral contract.
- Architecture overview that contradicts the current code.
- Long migration guides nobody reads.
- Copy-pasted API tables that drift from the schema.
