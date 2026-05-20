---
name: test-skill
description: Run a compiled skill file inline without creating folders or artifacts. Use when user says "test skill", "run skill", or wants to try a skill from skills/output/ without side effects.
version: 1.0.0
---

Execute a skill from `skills/output/` inline in the current conversation. No folders, no copies, no links created.

## Preflight

**Gate A — Resolve target.** If `<name>` arg missing: list files in `skills/output/` and ask which one via AskUserQuestion. Strip `.md` suffix if human supplied full filename.

## Steps

1. **Locate skill.** Read `skills/output/<name>.md`. If absent, stop and report missing file.

2. **Extract content.** Strip YAML frontmatter (everything between and including the leading and trailing `---` delimiters). What remains is the skill body.

3. **Announce.** One line: `Running skill: <name> (inline, no writes unless the skill itself requires them).`

4. **Execute.** Follow the skill body exactly as written — steps, hard rules, return spec. The skill runs as if invoked normally. All HITL requirements in the skill remain in force.

5. **Return.** When the skill reaches its own return/handoff step, emit that output. Append one line: `[test-skill: run complete]`.

## Hard Rules

- No test infrastructure created (no folders, no copies, no wrapper files).
- Skill hard rules and HITL gates stay fully in force — do not bypass or soften them.
- If the skill writes artifacts (e.g. planning files), it still does so — this skill does not sandbox writes.
- Scope: one skill per invocation. If the skill hands off to another skill, stop at the handoff boundary and report it; do not chain.
