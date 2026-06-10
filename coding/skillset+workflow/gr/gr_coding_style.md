# Guardrail: Coding Style and Conventions

Purpose: protect readability, consistency, and predictable behavior at the code level.

---

## Apply When

- Any implementation task that produces or modifies code.

---

## Rules

### C1. Follow Existing Conventions

Match the existing style of the file, module, and project — formatting, naming, error handling, file layout. Do not introduce a new style.

### C2. Naming Reflects Intent

Names describe purpose, not type or implementation. No `data`, `tmp`, `handler2` unless the surrounding code already establishes that style.

### C3. Error Handling Style Is Consistent

Use the error mechanism the project uses (exceptions, result types, error codes). Do not mix styles in one module.

### C4. Logging Is Intentional

Logs have a clear purpose, level, and audience. No print statements left in production code. No logging of sensitive data (see `gr_security_compliance.md`).

### C5. Concurrency Rules Match Existing Model

Threading, async, locks, and shared state follow the existing concurrency model of the module. New concurrency primitives require approval.

### C6. Resource Management Is Explicit

Files, sockets, connections, locks, transactions are released deterministically (RAII, `with`, `using`, `defer`, try/finally). No reliance on garbage collection for non-memory resources.

### C7. Respect Performance-Sensitive Paths

Code marked as performance-sensitive (hot path, real-time, large dataset) is not changed without measuring impact.

### C8. No Speculative Abstractions

No interfaces, base classes, generics, or hooks added for hypothetical needs. Concrete first; abstract only when a second concrete case appears.

### C9. No Unrelated Cleanup

The agent does not reformat, rename, or rewrite code that is not part of the current change.

### C10. Do Not Mix Concerns

One change = one concern (feature, fix, refactor, format). Combining concerns is forbidden unless explicitly approved.

### C11. Comments Explain Why, Not What

Comments cover non-obvious rationale, constraints, or invariants. They do not narrate code or duplicate identifiers.

### C12. Default to No Comment

If the code is self-explanatory, no comment is needed. Bad comments are worse than no comment.

### C13. Keep Functions Small and Cohesive

A function does one thing at one level of abstraction. Long, mixed-level functions are split — only when the current task touches them.

### C14. Backward Compatibility Within the Module

Internal helpers within a module may be refactored, but signatures used by other modules follow the API compatibility rule (see `gr_architecture.md` A6).

---

## Anti-Patterns

- "While I'm here" refactor in an unrelated file.
- Rewriting a function in a personal style.
- Adding `IFooFactory` for a single `Foo`.
- Catch-and-swallow exceptions.
- `// added by AI` comments.
- Restating the identifier in the comment ("// increment counter").
