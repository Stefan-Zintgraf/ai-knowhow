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

---

## Anti-Patterns

- A new `NOTES.md` after every task.
- Block comments restating what the function signature already says.
- Architecture overview that contradicts the current code.
- Long migration guides nobody reads.
- Copy-pasted API tables that drift from the schema.
