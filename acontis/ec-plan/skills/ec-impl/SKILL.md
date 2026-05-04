---
name: ec-impl
description: Continue an EC-style step-wise implementation plan by executing the next unchecked step in its own session (one step = one conversation). Use when the user asks to "continue the plan", "do the next step", "implement the next step", "resume the plan", "ec-impl", or points at a plan folder containing an `implementation_prompt.md` and a `<plan_name>.md` overview with a Status table.
---

# ec-impl

Execute the **next unchecked step** of an EC-style plan, strictly following the plan's session protocol: read the relevant docs, run `git status` / `git log`, implement only that step, run its automated gate, commit, mark `[x]` in both the step file and the overview, then **stop**.

The authoritative rules for this plan style are in **[`ec-plan/plan_rules.md`](../ec-plan/plan_rules.md)** (sibling to this skill: copy the whole `skills/` tree so `ec-plan` stays next to `ec-impl`). Consult it if the plan's own docs are ambiguous.

## Locate the plan

If the user did not point at a plan folder, look for one by detecting the combination:

- a `*.md` file whose name matches `<plan_name>.md` and contains an **"Execution order"** (or similarly named) table with `Status` column entries `[ ]` / `[x]`,
- an `implementation_prompt.md` sibling file,
- optional `<plan_name>.step<N>.md` siblings.

If multiple plan folders are present, ask the user which one. If none, stop and ask for the path.

## Session protocol (authoritative)

Follow the plan's own `implementation_prompt.md` verbatim. It is the runtime contract. If it is missing, fall back to the generic protocol below (from `plan_rules.md §6`):

1. **Read, in order:**
   - `<plan folder>/<plan_name>.md` (overview). Find the next step: the **first `[ ]`** in the Status column, subject to any entry / ordering rules stated immediately above the table.
   - The step file for that step (e.g. `<plan_name>.step<N>.md`).
   - `<plan folder>/<plan_name>.architecture.md` if it exists.
   - `<plan folder>/<plan_name>.test_strategy.md` if it exists.
   - The strategy doc **only** if the step file or overview references it directly; otherwise skip.
2. **Verify clean state:** run `git status` and `git log --oneline -10`. If the tree is dirty with unrelated changes or prior steps look uncommitted, **stop and ask the user** before touching files.
3. **Check prerequisites:** confirm each prerequisite referenced by the step is marked `[x]` (or explicitly N/A). If any is open, stop and ask.
4. **Implement only the current step.** Do exactly the tasks listed. Produce exactly the artifacts in the step's "Verifiable result" list.
5. **Run the automated gate** exactly as written in the step file. If it fails:
   - Iterate **within the step** if the fix is obvious and on-scope.
   - Otherwise **stop and ask** the user. Do not mutate contracts, rewrite inventory, or silence the gate to force it green.
6. **Commit** all new/changed artifacts with a short, descriptive message referencing the step (e.g. `step <N>: <short summary>`).
7. **Update Status** to `[x]` in **both** the step file's header and the overview's execution-order table, in the same commit as the artifact changes (or a follow-up commit if the hook setup requires it).
8. **Stop.** Do not start the next step. Report to the user: which step was done, what was committed, and what the next step is.

## Hard constraints

- **One step per session.** If the user asks for "two steps at once", decline and do just one; explain that the plan's session rule requires separate sessions.
- **Scope discipline.** Do not edit files the step does not list. If something outside scope looks broken, note it at the end of the session; do not fix it inline.
- **Do not skip or weaken the gate.** If the gate is manual (operator action required), say so, report current status, and hand control back to the user instead of fabricating a pass.
- **Do not rewrite source-of-truth data** (registry, inventory, fixture lists, contracts) to clear a failing gate. Resolve via the documented escalation path in the step / overview, or stop and ask.
- **Do not run destructive VCS commands** (`git restore`, `git checkout --`, `git reset --hard`) on tracked plan data or implementation artifacts without **explicit** user consent. Operator may have uncommitted edits.
- **Plan folder is documentation.** Implementation artifacts go to the feature directory declared in the overview's workspace conventions.

## When to stop and ask

Stop (do not guess) when any of these happen:

- The working tree is dirty with unrelated changes.
- A prerequisite is not marked `[x]` and the step file does not provide an N/A path.
- The next step is ambiguous (multiple `[ ]` rows with no ordering note, or conflicting entry rules).
- The gate fails for reasons the step file does not anticipate.
- The obvious fix would require editing files the step did not list.
- You are tempted to rewrite inventory / contracts to clear a gate.
- The step is marked as needing an operator action (e.g. recording audio, manual acceptance) that cannot be automated here.

Report clearly what you observed and what options the user has. Do not proceed.

## Session close-out message

End every session with a short summary:

```
Step <N> — <name>: [done | paused]
Gate: <gate command> → <pass/fail/manual>
Commits: <hashes or short list>
Status updates: step file [x], overview [x]
Next step: <N+1> — <name>  (run ec-impl again in a new session)
```

If paused, state exactly what is blocking and what the user needs to decide or provide.

## Optional: status snapshot

If the user just wants a status check (not execution), offer to read the overview and report the first unchecked row + any blocking notes without touching anything else. Confirm with the user before switching from "status only" to "execute".

## Reference

- Rules: [`../ec-plan/plan_rules.md`](../ec-plan/plan_rules.md)
- Example plan: `ger_mode_cmds_plan2/` (e.g. `ec-plan/ger_mode_cmds_plan2/` in this repo, or a clone in your `tools-talon/.../ger_mode_cmds_plan2/`)
- Sister skill for creating a plan: `ec-create-plan` (sibling under `skills/`)
