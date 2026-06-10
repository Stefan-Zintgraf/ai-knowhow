---
name: run-skill
description: Execute a compiled skill from skills/output/ inline as if it were an installed Claude Code skill. Use when user says "run skill", "execute skill", or wants to manually try a skill without installing it.
---

# `/run-skill` — Execute Compiled Skill Inline

Run a compiled skill from `skills/output/<name>.md` directly in this conversation, exactly as if it were installed at `.claude/skills/<name>/skill.md` and invoked by the user. No copying, no test harness — just execute the skill body.

## Preflight

**Gate A — Resolve target.** If `<name>` arg missing: list `.md` files in `skills/output/` (excluding `*Ref.md`, `*-ref.md`, `*_ref.md`) and ask which one via AskUserQuestion. Strip `.md` suffix if human supplied full filename.

**Gate B — Source exists.** Read `skills/output/<name>.md`. If absent → stop, report missing file.

## Steps

1. **Read skill.** Read `skills/output/<name>.md` in full.

2. **Extract body.** Strip YAML frontmatter (everything between and including the leading and trailing `---` delimiters). What remains is the skill body.

3. **Set artifacts folder.** Resolve `<artifacts>` = `./skills/run/plan`. When the skill body references `<artifacts>/`, substitute this path. Create the folder if it does not exist before any skill write.

4. **Execute.** Follow the skill body exactly as written — steps, hard rules, HITL gates, return spec. Supply `<artifacts>` = `./skills/run/plan` as the caller-supplied artifacts folder (overrides the skill's default of `plan`). The skill runs as if it were a native installed skill invoked by the user. All HITL requirements in the skill remain in force.

5. **Return.** When the skill reaches its own return/handoff step, emit that output normally.

## Hard Rules

- Skill body is executed verbatim — no edits, no softening, no skipping steps.
- All HITL gates in the skill stay in force — do not bypass or auto-answer them.
- Artifacts folder is always `./skills/run/plan` — never `./plan` or any other root. Inform the user of the output path after any artifact write.
- Scope: one skill per invocation. If the skill hands off to another skill, stop at the handoff boundary and report it; do not chain.
- Frozen reference files (`*Ref.md`, `*-ref.md`, `*_ref.md`) in `skills/output/` are never listed or runnable.
