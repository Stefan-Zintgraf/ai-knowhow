---
name: draft-skill-tests
description: Generate deterministic test fixture pairs (input/output) for a compiled skill under skills/test/<name>/. Derives scenarios from the skill's source docs and compiled behavior, presents them for human approval, then writes the fixture files. Use when user says "draft skill tests", "create skill tests", "generate test fixtures", or when source docs / guardrails for a skill have changed and fixtures need updating.
version: 1.0.0
---

Generate deterministic test fixture pairs (`input<NNN>.md` / `output<NNN>.md`) for a compiled skill so that `make-skill` Step 6a and `test-skill` can regression-test it. Does not run the fixtures — only authors them. Each fixture is an independent test case: input drives the skill deterministically, output is the expected byte-exact return.

## Preflight (run BEFORE Step 1 — non-negotiable gates)

**Gate A — Resolve target.** If `<name>` is missing, call `AskUserQuestion`:
- List every compiled skill found in `skills/output/*.md` (exclude `*Ref.md`, `*-ref.md`, `*_ref.md`).
- Human picks one or types a name.
- Resolve to kebab-case `<name>`. Verify `skills/output/<name>.md` exists — if not, stop: "Compile the skill first."

**Gate B — Existing fixtures check.** Scan `skills/test/<name>/`:
- If folder absent → mode is `create` (fresh fixture set).
- If folder exists with pairs → call `AskUserQuestion`:
  - `Replace all` — delete existing fixtures, generate from scratch. Confirm destructive action.
  - `Append` — keep existing fixtures, add new ones starting at next available `<NNN>`.
  - `Rebuild selectively` — human picks which existing pairs to keep; rest are regenerated.

**Gate C — Source-doc freshness.** Check whether source docs for this skill have changed since the existing fixtures were last written:
- Use `git log --since='90 days ago' -- <paths>` on the skill's source docs (from `coding_plan.md` row).
- If source docs changed more recently than existing fixture files → warn human: "Source docs changed since fixtures were written. Recommend `Replace all`."
- This gate is informational only — human decides.

### Anti-patterns

- ❌ Running fixtures after writing — that is `make-skill` Step 6a or `test-skill`'s job.
- ❌ Writing fixtures without human approval of each scenario.
- ❌ Generating non-deterministic fixtures (outputs depending on timestamps, random values, or external state).
- ❌ Editing `skills/input/<name>-in.md` or `skills/output/<name>.md` — those are tool-managed by other skills.
- ❌ Reading or citing frozen reference files (`*Ref.md`, `*-ref.md`, `*_ref.md`).

## Steps

1. **Load compiled skill.** Read `skills/output/<name>.md`. Extract:
   - Steps (the skill's behavioral sequence)
   - Hard Rules (constraints that must hold)
   - Return / Handoff shape (what the skill emits on completion)
   - HITL gates (prompts the skill asks — fixtures must answer these inline)
   - Failure / rejection conditions (when the skill refuses or emits `status: not_produced`)

2. **Load source docs.** From `coding_plan.md`, find the row for `<name>`. Extract its `Source doc` column entries and every `gr/<file>.md` referenced. Read each. Purpose: identify the full requirement surface that fixtures should exercise.

3. **Derive scenario categories.** From Steps 1–2, classify scenarios into:
   - **Happy path** — standard input that exercises the main success path end-to-end. At least one required.
   - **Edge / boundary** — inputs at limits of the skill's acceptance criteria (e.g., minimum viable input, maximum complexity the skill handles).
   - **Rejection / failure** — inputs the skill should refuse or mark `status: not_produced` (e.g., under-budget, out-of-scope, malformed).
   - **Heuristic shortcut** — if the skill has a pre-structured-input detection path (like distill-idea's "goals already shaped" check), test both the match and the miss.
   - **Detail stripping** — if the skill strips implementation details, test that stripping works correctly with detail-laden input.

   Not every category applies to every skill. Only propose categories that the compiled skill's logic actually exercises.

4. **Propose scenarios.** Present the scenario list to the human via `AskUserQuestion` or inline review:
   - For each scenario: one-line description, which category it falls in, what behavior it tests.
   - Human can: approve all, drop scenarios, add scenarios, rewrite descriptions.
   - Minimum: 2 fixtures (one happy path + one failure/edge). Maximum: recommend no more than 8 unless the skill has exceptional branching.

5. **Draft fixture pairs.** For each approved scenario, write:

   **`input<NNN>.md`**: Plain text content that a user would provide to the skill. Must:
   - Be self-contained — no references to external state or files.
   - Answer every HITL prompt the skill will ask (inline, in the order the skill asks them).
   - Be deterministic — no dates, timestamps, random values, or session-dependent content.
   - Be realistic — plausible domain content, not lorem ipsum.

   **`output<NNN>.md`**: The exact text the skill should return when given this input. Must:
   - Match the skill's Return spec format exactly (headings, status lines, structure).
   - Include every field the skill emits (status, paths, summaries — whatever the Return step specifies).
   - Be byte-exact — this is the comparison target. Whitespace, newlines, heading levels all matter.

   Numbering: zero-padded 3-digit, starting at `000` (or next available if appending).

6. **Present drafts for review.** Show each fixture pair to the human:
   - Display `input<NNN>.md` content.
   - Display `output<NNN>.md` content.
   - For each: "Does this input deterministically produce this output when the skill runs?" Human confirms, edits, or rejects per pair.
   - Rejected pairs are dropped. Edited pairs use the human's version.

7. **Write fixtures.** On human approval:
   - Create `skills/test/<name>/` if absent.
   - Write each confirmed `input<NNN>.md` and `output<NNN>.md`.
   - If `Replace all` mode: delete prior contents of `skills/test/<name>/` before writing.
   - If `Rebuild selectively`: delete only the pairs the human chose to replace.

8. **Return.** Summary:
   ```
   draft-skill-tests <name> — status=<done|partial|aborted>
     fixtures written: skills/test/<name>/
     pairs created: <N> (input000–input<NNN>)
     categories covered: <list of categories with counts>
     mode: <create|replace-all|append|rebuild-selective>
     note: run /make-skill <name> or /test-skill <name> to execute fixtures
   ```

## Hard Rules

- Never run fixtures — only author them. Execution belongs to `make-skill` Step 6a or `test-skill`.
- Never edit `skills/input/<name>-in.md` or `skills/output/<name>.md`. Those are tool-managed by `draft-skill-input` and `compile-skill`.
- Never read, edit, or cite frozen reference files (`*Ref.md`, `*-ref.md`, `*_ref.md`).
- HITL on: target resolution (Gate A), existing-fixture handling (Gate B), scenario approval (Step 4), each fixture pair review (Step 6), destructive replace (Gate B + Step 7).
- Fixtures must be deterministic. No timestamps, random values, external state, or session-dependent content in input or output files.
- Output files are byte-exact comparison targets. Trailing newlines, whitespace, heading levels — all must match what the skill actually emits.
- Minimum 2 fixtures per skill (one happy path + one failure/edge). If the skill has no failure path, minimum is 2 happy-path variants exercising different branches.
- Input files must be self-contained: every HITL answer the skill needs is embedded in the input content, in the order the skill asks.
- Zero-padded 3-digit numbering (`000`, `001`, …). When appending, continue from the highest existing number + 1.
- Scope: one skill per invocation. Do not chain to other skills or generate fixtures for multiple skills at once.
- If the compiled skill does not exist at `skills/output/<name>.md`, stop immediately — do not attempt to derive fixtures from input files or source docs alone. The compiled skill is the specification.
