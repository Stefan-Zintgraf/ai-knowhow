# Skill Authoring Tutorial

Three use-cases: checking what to do next, creating a skill from scratch, or updating existing skills after a guardrail change.

## Contents

- [Use-Case 1: What's Next?](#use-case-1-whats-next)
- [Use-Case 2: Create a New Skill](#use-case-2-create-a-new-skill)
  - [Step 1 — Draft the Authoring Prompt](#step-1--draft-the-authoring-prompt)
  - [Step 2 — Compile](#step-2--compile)
  - [Step 3 — Test](#step-3--test)
  - [Step 4 — Install](#step-4--install)
  - [One-Shot Shortcut](#one-shot-shortcut)
- [Use-Case 3: Update Skills After Guardrail Change](#use-case-3-update-skills-after-guardrail-change)
  - [When to Use](#when-to-use)
  - [Step 1 — Edit the guardrail doc](#step-1--edit-the-guardrail-doc)
  - [Step 2 — Identify affected skills](#step-2--identify-affected-skills)
  - [Step 3 — Rebuild each affected skill](#step-3--rebuild-each-affected-skill)
  - [Step 4 — Update test fixtures](#step-4--update-test-fixtures)
  - [Step 5 — Run tests](#step-5--run-tests)
  - [Step 6 — Refresh the rule-skill map](#step-6--refresh-the-rule-skill-map)
  - [Step 7 — Verify](#step-7--verify)
  - [Decision: /make-skill vs. individual skills](#decision-make-skill-vs-individual-skills)
  - [Quick reference](#quick-reference)
- [Critical Rules](#critical-rules)

---

## Use-Case 1: What's Next?

Starting a new session and unsure where to pick up? Run `/status`.

### What it does

`/status` runs 4 PowerShell scripts under `scripts/status/` to produce a compact dashboard with three sections:

1. **Current WI + phase** — reads `plan/ACTIVE` (single-line file pointing to the active work-item, e.g. `1_ai-mail`) and that WI's `plan/<WI>/phase_status.md` to show current phase, mode, blockers, and tripwire-halt state. If no WI is active, it reports "no active WI."
2. **Skill Freshness** — compares git timestamps of each skill's source docs (`gr/*.md`, `wf/*.md`, `phases.md`) against `skills/output/<name>.md` and `skills/input/<name>-in.md`. Flags stale skills with the exact command to fix them (`/make-skill <name>` or `/draft-skill-input <name>`).
3. **Next Action** — priority-ordered list: tripwire halts first, then stale rule-skill map, stale inputs, stale compiled skills, and finally the first unchecked `- [ ]` item from `coding_plan.md`.

### What it creates

`/status` saves its output to `.claude/skills/status/latest_status.md` so you can refer back without re-running. This file is overwritten on each run.

### When to use

- **Session start** — orient yourself before doing anything else.
- **After rebuilding skills** — verify all freshness checks pass (Use-Case 3, Step 7).
- **After completing a work item** — confirm nothing was left stale.

The dashboard tells you exactly what to do next and which command to run. Follow its recommendations, then pick the matching use-case below.

---

## Use-Case 2: Create a New Skill

### Pipeline

```
/draft-skill-input  →  skills/input/<name>-in.md  →  /compile-skill  →  skills/output/<name>.md  →  .claude/skills/<name>/SKILL.md
```

### Step 1 — Draft the Authoring Prompt

Two paths:

**a) From project docs** — run `/draft-skill-input`. It asks which `coding_plan.md` item (W##/A##/B##/C##) or free-text purpose, suggests a kebab-case name for confirmation, reads only the source docs listed for that target (`phases.md` entry, relevant `gr/*.md`, `guardrails.md` §3 cross-refs), classifies planning-artifact vs not, and produces the draft. HITL accept required before write. Clobber-gated on existing files (Reopen / Self-check only).

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

### Step 2 — Compile

> `/compile-skill <name>`

Gates: asks before overwriting, detects input/spec drift, self-checks that every `must`/`must not` is present and no source-doc links leaked into the output.

### Step 3 — Test

> `/test-skill <name>`

Runs the compiled skill inline. All HITL gates remain in force. **Does not sandbox writes** — planning artifacts will be created.

### Step 4 — Install

Copy compiled output to `.claude/skills/<name>/SKILL.md`.

### One-Shot Shortcut

`/make-skill <name>` chains draft → compile → verify in a single loop (up to 3 fix iterations). Preferred when building from a `coding_plan.md` row.

**Example:**

```
Run /make-skill distill-idea for the W15 row in coding_plan.md.
Test with the following input:
AI-driven mail handling. Goals: search mails by NL prompt, draft replies, use mail content as a knowledge base for Q&A.
```

HITL gates still fire at each stage — no auto-accept.

---

## Use-Case 3: Update Skills After Guardrail Change

When a guardrail is created or changed (`guardrails.md`, `gr/gr_*.md`), affected skills must be rebuilt to stay in sync.

### When to Use

- A new guardrail rule is added to `guardrails.md` or a `gr/gr_*.md` file.
- An existing rule is reworded, scoped differently, or removed.
- A new `gr/gr_*.md` file is created for a new guardrail category.

### Step 1 — Edit the guardrail doc

Edit `guardrails.md` or the relevant `gr/gr_*.md` file directly. No skills involved.

If adding a new category, also add a routing entry in `guardrails.md` §4 and create the `gr/gr_<category>.md` file.

### Step 2 — Identify affected skills

Check which skills list the changed file in their `Source doc` column in `coding_plan.md` (Phase Skills table). Those need rebuilding.

Run `/status` first if unsure — the Skill Freshness section flags stale input/output automatically once source docs change.

### Step 3 — Rebuild each affected skill

| Situation | Command | What it does |
| --- | --- | --- |
| Minor rule reword, structure unchanged | `/compile-skill <name>` | Recompiles from existing input prompt |
| Rule added, removed, or meaningfully changed | `/make-skill <name>` | Full loop: re-drafts input → recompiles → verifies coverage |
| Input prompt needs targeted edits only | `/draft-skill-input <name>` then `/compile-skill <name>` | Two-step manual control |

Prefer `/make-skill` when in doubt — it verifies that every rule from the source docs appears in the compiled output. Runs up to 3 fix iterations automatically, then hands off if gaps remain.

### Step 4 — Update test fixtures

Run `/draft-skill-tests <name>` for each rebuilt skill if:

- The guardrail change alters observable skill behavior (different output shape, new rejection case, new HITL prompt).
- Source docs changed more recently than the existing fixture files.

If behavior is unchanged (e.g. wording only), existing fixtures are likely still valid — verify in step 5.

### Step 5 — Run tests

Run `/test-skill <name>` for each affected skill.

With `skills/test/<name>/test-plan.md`: fixture mode (LLM-as-judge, human confirms each verdict).
Without fixtures: freeform mode (quick smoke-test).

### Step 6 — Refresh the rule-skill map

Run `/update-rule-skill-map` after all skills are rebuilt.

Adds or corrects `Skills:` annotation lines on each named rule heading in `gr/*.md`, `wf/*.md`, and `phases.md`.

### Step 7 — Verify

Run `/status`. Skill Freshness section should show all affected skills as current (✓). Any remaining `⚠` = skill whose input or output is still older than its source docs.

### Decision: `/make-skill` vs. individual skills

```
guardrail change
       │
       ├─ wording only, no new rule ──► /compile-skill <name>
       │
       ├─ rule added / removed / scope changed
       │         │
       │         └─ use /make-skill <name>   (draft → compile → verify, up to 3 rounds)
       │
       └─ multiple skills affected ──► run steps 3–5 per skill, then one /update-rule-skill-map
```

### Quick reference

```
1. Edit  gr/gr_<category>.md  (or guardrails.md)
2. /make-skill <name>          (per affected skill)
3. /draft-skill-tests <name>   (if behavior changed)
4. /test-skill <name>          (run fixtures)
5. /update-rule-skill-map      (refresh annotations)
6. /status                     (verify all ✓)
```

---

## Critical Rules

- Compiled skill is a **leaf artifact** — no links to `gr/`, `phases.md`, `guardrails.md`, or the input file
- **No auto-accept** on HITL gates
- Planning artifacts go to `plan/<WI>/`, never repo root
- `status: done` only on explicit human confirmation, never auto-flipped
