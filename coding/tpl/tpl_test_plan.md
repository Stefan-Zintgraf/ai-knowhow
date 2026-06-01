# Template: Skill Test Plan

Purpose: canonical shape for the test plan that accompanies test fixtures under `skills/test/<name>/`. Consumed by `test-skill` (execution + checklist management) and `draft-skill-tests` (generation). Single file per skill test suite.

Source: design session 2026-05-26 (test plan design for skill testing).

Emitted by: `draft-skill-tests` skill.
Consumed by: `test-skill` skill.

---

## File Naming

```
skills/test/<name>/test-plan.md
```

`<name>` matches the skill's kebab-case identifier (same as `skills/output/<name>.md`).

---

## Shape

YAML frontmatter + markdown body. Tests split into two sections: automated (AI-runnable) and manual (human-only).

```markdown
---
skill: <name>
source_docs:
  - <path to gr file, e.g. gr/gr_idea.md>
  - <path to another source doc>
source_docs_hash: <short hash or timestamp fingerprint of source docs at generation time>
generated: <YYYY-MM-DD>
---

# Test Plan: <name>

## Automated Tests

### 000 — <one-sentence purpose>

- **Category:** happy-path | edge | rejection | heuristic-shortcut | detail-stripping
- **Requirements:** Idea1 ([gr_idea.md](gr/gr_idea.md)), Idea2 ([gr_idea.md](gr/gr_idea.md)), 3.29 ([guardrails.md](guardrails.md))
- **Input:** `input000.md`
- **Output:** `output000.md`
- [ ] Pass

### 001 — <one-sentence purpose>

- **Category:** rejection
- **Requirements:** Idea1 ([gr_idea.md](gr/gr_idea.md)) — under-budget rejection
- **Input:** `input001.md`
- **Output:** `output001.md`
- [ ] Pass

<!-- repeat for each fixture pair -->

## Manual Tests

### M000 — <one-sentence purpose>

- **Category:** <category>
- **Requirements:** Idea4 ([gr_idea.md](gr/gr_idea.md))
- **Why manual:** <reason this cannot be tested by AI agent — e.g., requires real HITL interaction, visual inspection, external system>
- **Test procedure:** <step-by-step instructions for the human tester>
- **Pass criteria:** <observable conditions>
- [ ] Pass

<!-- repeat for each manual test -->
```

---

## Frontmatter Fields

| Field              | Required | Notes                                                                                      |
| ------------------ | -------- | ------------------------------------------------------------------------------------------ |
| `skill`            | yes      | Kebab-case skill name. Must match folder name under `skills/test/`.                        |
| `source_docs`      | yes      | List of source doc paths used to derive the tests. Used by `test-skill` for staleness check.|
| `source_docs_hash` | yes      | Fingerprint of source docs at generation time. `test-skill` compares against current state. |
| `generated`        | yes      | ISO date when `draft-skill-tests` created/updated this plan.                               |

---

## Body Rules

### Test Sections

The test plan has two sections:

- **`## Automated Tests`** — tests runnable by an AI agent via `test-skill`. Each has input/output fixture pairs. Numbered `000`, `001`, etc.
- **`## Manual Tests`** — tests requiring real human interaction, visual inspection, or external systems that an AI agent cannot simulate. Numbered `M000`, `M001`, etc. No fixture files — procedure is described inline.

### Automated Test Entries

Each test is an H3 under `## Automated Tests`, formatted as `### <NNN> — <purpose>`.

Required fields per test:
- **Category** — one of: `happy-path`, `edge`, `rejection`, `heuristic-shortcut`, `detail-stripping`. Only categories exercised by source-doc requirements appear.
- **Requirements** — comma-separated rule IDs with document references in parentheses, e.g., `Idea1 ([gr_idea.md](gr/gr_idea.md)), 3.29 ([guardrails.md](guardrails.md))`. Links traceability from test to spec and its source document.
- **Input** — filename of the input fixture.
- **Output** — filename of the output fixture (contains evaluation criteria, not byte-exact expected output).
- **Checklist item** — `- [ ] Pass` (unchecked) or `- [x] Pass` (checked). Managed by `test-skill`.

### Manual Test Entries

Each test is an H3 under `## Manual Tests`, formatted as `### M<NNN> — <purpose>`.

Required fields per test:
- **Category** — same categories as automated tests.
- **Requirements** — same format as automated tests (rule IDs with document references).
- **Why manual** — one-line reason this test cannot be automated (e.g., "requires real HITL interaction during skill execution", "needs visual inspection of rendered output", "depends on external system state").
- **Test procedure** — step-by-step instructions for a human tester.
- **Pass criteria** — observable conditions the human checks.
- **Checklist item** — `- [ ] Pass` (unchecked) or `- [x] Pass` (checked). Managed by the human tester.

### Requirements Coverage

Every requirement (rule ID) found in the skill's source docs must appear in at least one test — automated or manual. The test plan must achieve full traceability: no source-doc requirement left untested.

If a requirement cannot be tested at all (neither automated nor manual), it must be listed in a `## Untestable Requirements` section at the bottom with a reason.

### Checklist Management (by `test-skill`)

1. On run start: if all items are checked, ask human "Run tests again?" — yes → uncheck all; no → keep and exit.
2. On run start (items unchecked): proceed with unchecked tests.
3. After each test: LLM evaluates output against criteria in the output file, writes reasoning, presents to human.
4. Human confirms pass → `test-skill` checks the item (`- [x] Pass`).
5. Human rejects → item stays unchecked; `test-skill` reports failure and continues to next test.
6. On run end: summary of pass/fail counts.

### Staleness Detection (by `test-skill`)

Before running tests, `test-skill` compares `source_docs_hash` in frontmatter against current source doc state:
- **Match** → proceed normally.
- **Drift detected** → warn human: "Source docs changed since test plan was generated. Tests may be outdated." Ask: "Update tests? (requires re-running draft-skill-tests)" — yes → exit with instruction; no → proceed with current tests (mark existing tests as valid for updated source docs, pending human confirmation).

---

## Output File Format (Criteria-Based)

Output files (`output<NNN>.md`) use criteria-based evaluation instead of byte-exact matching:

```markdown
# Evaluation Criteria

## Requirements Tested
- <RuleID>: <what this rule requires in context of this test>

## Pass Criteria
- <criterion 1: specific, observable condition the output must meet>
- <criterion 2>
- <criterion 3>

## Fail Criteria
- <condition that means the test failed>

## Example Output

<one realistic example of what a passing output looks like — for reference, not exact match>
```

### Rules for Output Files

- **Pass criteria** are specific and observable — "output contains exactly 4 goals" not "output looks right."
- **Fail criteria** capture the inverse or specific anti-patterns — "output contains module names" (for an Idea2 test).
- **Requirements tested** links each criterion back to a rule ID from `gr/*.md`.
- **Example output** is one realistic sample. LLM judge uses it as reference, not as exact-match target.
- For **negative tests** (rejection category): pass criteria describe what the skill should do instead (ask clarification, refuse, emit status: not_produced). Fail criteria describe what it must NOT do (produce a goal list from bad input).

---

## Anti-Patterns

- Byte-exact output comparison for LLM-generated skill output — use criteria-based evaluation instead.
- Missing requirements traceability — every test must link to at least one rule ID.
- Requirements without document references — rule IDs must include `([source.md](path))` so readers find the spec.
- Checklist items managed by hand — only `test-skill` checks/unchecks automated items; human manages manual items.
- Stale test plan used without staleness warning — `test-skill` must check `source_docs_hash`.
- Output file without example — the example grounds the LLM judge and prevents criteria-only drift.
- Output file without fail criteria — knowing what fails is as important as knowing what passes.
- Incomplete coverage — source-doc requirements missing from all tests. Every requirement must appear in at least one automated or manual test.
- Classifying AI-testable items as manual — only truly human-dependent tests go in the manual section.
- HITL-dependent tests in the automated section — tests that require real human interaction during execution belong in manual.

---

## Notes on Interaction

- `draft-skill-tests` generates `test-plan.md` alongside fixture pairs. Plan is always regenerated when fixtures are created or updated.
- `test-skill` reads `test-plan.md` to know which tests to run, in what order, and writes checkmarks back to it (sole exception to test-skill's no-side-effects rule).
- `make-skill` chains: `draft-skill-input` → `compile-skill` → `draft-skill-tests` (generates plan + fixtures) → `test-skill` (runs against plan).
- Staleness check bridges `draft-skill-tests` and `test-skill`: when source docs change, `test-skill` detects and routes human to `draft-skill-tests` for update.
