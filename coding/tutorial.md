# Skill Authoring Tutorial

## Flow

```
/draft-skill-input  →  skills/input/<name>-in.md  →  /compile-skill  →  skills/output/<name>.md  →  .claude/skills/<name>/SKILL.md
```

## 1. Draft the Authoring Prompt (`skills/input/<name>-in.md`)

Two paths:

**a) From project docs** — run `/draft-skill-input`. It asks which `todo.md` item (W##/A##/B##/C##) or free-text purpose, suggests a kebab-case name for confirmation, reads only the source docs listed for that target (`phases.md` entry, relevant `gr/*.md`, `guardrails.md` §3 cross-refs), classifies planning-artifact vs not, and produces the draft. HITL accept required before write. Clobber-gated on existing files (Reopen / Self-check only).

**b) Hand-authored** — write it yourself using `skills/input/distill-idea-in.md` as the reference example.

Key sections (either path):

- **Metadata** — skill_id, phase, depends_on, feeds_into
- **Scope** — one thing it does; explicit list of what it does NOT do
- **Self-Containment Mandate** — source docs are author-time only; all rules must be inlined
- **Source Documents** — what to read during compilation (author-time only)
- **Skill Behaviors** — numbered runtime steps (what the *skill* does, not compile-skill)
- **Constraints** — `must`/`must not` clauses → become Hard Rules in output

**Planning-artifact skills** (produce `idea.md`, PRD, ticket, etc.) must also specify:
- Artifact path: `plan/<WI>/<file>.md`, `<WI>` human-confirmed slug
- `status_<artifact>.md` emitted on every successful write (`wip` by default; `done` only on explicit human confirm)

## 2. Compile

> compile skill `<name>`

`compile-skill` gates: asks before overwriting, detects input/spec drift, self-checks that every `must`/`must not` is present and no source-doc links leaked into the output.

## 3. Test

> test skill `<name>`

Runs the compiled skill inline. All HITL gates remain in force. **Does not sandbox writes** — planning artifacts will be created.

## 4. Install

Copy compiled output to `.claude/skills/<name>/SKILL.md`.

---

## Critical Rules

- Compiled skill is a **leaf artifact** — no links to `gr/`, `phases.md`, `guardrails.md`, or the input file
- **No auto-accept** on HITL gates
- Planning artifacts go to `plan/<WI>/`, never repo root
- `status: done` only on explicit human confirmation, never auto-flipped
