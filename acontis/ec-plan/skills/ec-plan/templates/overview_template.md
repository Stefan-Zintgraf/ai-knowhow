# <Plan Title>

## Purpose

<One paragraph. What this plan achieves and, if applicable, which strategy/architecture it executes.>

This plan is an execution contract alongside:

- [Architecture](<plan_name>.architecture.md) — structural boundaries (remove if not used)
- [Strategy](<plan_name>.strategy.md) — rationale and principles (remove if not used)
- [Test strategy](<plan_name>.test_strategy.md) — gates per layer (remove if not used)

### Session rule

Each step is implemented in its own fresh session (one step = one conversation).

- On entry: read this overview, the architecture/strategy/test-strategy docs if present, and the current step file. Run `git status` / `git log --oneline -10` to confirm the workspace is clean and prior steps are committed.
- On completion: run that step's automated gate, commit when code/artifacts change, mark the checkbox here and in the step file, then stop.

## Workspace conventions

- Repository root: `<path>`
- Feature directory: `<path>`
- This plan (documentation only): `<plan folder>/`
- **Implementation outputs** (scripts, data, configs): `<feature directory>/` — **not** under the plan folder.
- Shell: `<bash | powershell | ...>`
- Runtime(s): `<Python / Node / ...>` versions as relevant.

## Acceptance criteria

The plan is complete when all of the following hold:

1. <criterion 1>
2. <criterion 2>
3. ...

## Key deliverables

| File | Created in | Role |
|------|------------|------|
| `<path>` | Step N | <role> |
| `<path>` | Step M | <role> |

## Execution order

| Step | File | Focus | Gate | Status |
|------|------|-------|------|--------|
| 1 | [step1](<plan_name>.step1.md) | <short focus> | <gate command or "manual primary"> | [ ] |
| 2 | [step2](<plan_name>.step2.md) | <short focus> | <gate> | [ ] |
| 3 | [step3](<plan_name>.step3.md) | <short focus> | <gate> | [ ] |

The first unchecked row is the next implementation target, subject to any entry / ordering rules below.

## Version control rule

A step is complete only when:

1. Every checkbox under **Verifiable result** for that step is satisfied.
2. Required artifacts are committed.
3. The **Status** column above and the step file's `Status` header are both updated from `[ ]` to `[x]`.

## Scope guardrails

- Do not modify artifacts the current step does not list.
- Do not skip or weaken the automated gate.
- Do not rewrite source-of-truth data to force a gate green; resolve via the documented escalation path or stop and ask.
- Do not perform partial migrations while unresolved backlog rows exist (if applicable).
- Do not run destructive VCS commands (`git restore`, `git checkout --`, hard reset) on tracked data without explicit user consent.

## Related documents

- [implementation_prompt.md](implementation_prompt.md)
- [<plan_name>.architecture.md](<plan_name>.architecture.md) — remove if not used
- [<plan_name>.strategy.md](<plan_name>.strategy.md) — remove if not used
- [<plan_name>.test_strategy.md](<plan_name>.test_strategy.md) — remove if not used
