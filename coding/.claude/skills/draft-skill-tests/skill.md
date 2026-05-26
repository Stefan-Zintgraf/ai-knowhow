---
name: draft-skill-tests
description: Generate deterministic test fixture pairs (input/output) for a compiled skill under skills/test/<name>/. Derives scenarios from the skill's source docs (coding_plan.md, guardrails.md, phases.md, gr/*.md), presents them for human approval, then writes the fixture files. Use when user says "draft skill tests", "create skill tests", "generate test fixtures", or when source docs / guardrails for a skill have changed and fixtures need updating.
version: 1.0.0
---

Generate test fixtures (`input<NNN>.md` / `output<NNN>.md`) and a `test-plan.md` for a compiled skill so that `make-skill` Step 6a and `test-skill` can regression-test it. Does not run the fixtures — only authors them. Each fixture is an independent test case: input drives the skill, output defines evaluation criteria (not byte-exact) that `test-skill`'s LLM-as-judge evaluates against. See [`tpl/tpl_test_plan.md`](../../tpl/tpl_test_plan.md) for the test plan format.

## Preflight (run BEFORE Step 1 — non-negotiable gates)

**Gate A — Resolve target.** If `<name>` is missing, call `AskUserQuestion`:
- List every skill found in `coding_plan.md` (exclude `*Ref.md`, `*-ref.md`, `*_ref.md`).
- Human picks one or types a name.
- Resolve to kebab-case `<name>`. Verify source docs exist for it in `coding_plan.md` — if not, stop: "No source docs found for this skill."

**Gate B — Existing fixtures check.** Scan `skills/test/<name>/`:
- If folder absent → mode is `create` (fresh fixture set).
- If folder exists with pairs → default behavior is `adjust`: read each existing pair, compare against source-doc requirements, and update in place. Only delete a pair if it is mostly wrong (i.e., testing obsolete or incorrect behavior). Only create new pairs if no existing pair can sensibly be enhanced to cover a missing scenario. Call `AskUserQuestion` to confirm the proposed adjust plan (which pairs to update, delete, or keep as-is, and whether new pairs are needed).

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

1. **Load source docs (the spec).** From `coding_plan.md`, find the row for `<name>`. Extract its `Source doc` column entries and every `gr/<file>.md` referenced. Also read `guardrails.md` and `phases.md` for cross-cutting requirements. These source docs are the specification — not the compiled skill. Extract:
   - Required behaviors and steps
   - Hard constraints and guardrails
   - Expected output shape / format
   - HITL gates (prompts the skill should ask — fixtures must answer these inline)
   - Failure / rejection conditions (when the skill should refuse or emit `status: not_produced`)

   **Build a requirements inventory:** enumerate every named rule (e.g., Idea1, Idea2, …, Idea12; 3.29, 3.32, etc.) from the source docs, recording which document each rule comes from. This inventory drives coverage checking in Step 3b.

2. **Optionally consult compiled skill.** If `skills/output/<name>.md` exists, read it to understand the skill's current implementation of the spec. Use only to inform fixture realism (e.g., exact heading levels, status line format). If the compiled skill diverges from source docs, source docs win — fixtures must test source-doc requirements, not compiled-skill quirks.

3. **Derive scenario categories and check coverage.** From Steps 1–2:

   **3a. Classify scenarios into categories:**
   - **Happy path** — standard input that exercises the main success path end-to-end. At least one required.
   - **Edge / boundary** — inputs at limits of the skill's acceptance criteria (e.g., minimum viable input, maximum complexity the skill handles).
   - **Rejection / failure** — inputs the skill should refuse or mark `status: not_produced` (e.g., under-budget, out-of-scope, malformed).
   - **Heuristic shortcut** — if the skill has a pre-structured-input detection path (like distill-idea's "goals already shaped" check), test both the match and the miss.
   - **Detail stripping** — if the skill strips implementation details, test that stripping works correctly with detail-laden input.

   Not every category applies to every skill. Only propose categories that the source docs' requirements actually exercise.

   **3b. Coverage check — automated vs manual.**  For each requirement in the inventory (Step 1), decide:
   - **Automated** — the requirement's behavior can be tested by providing input to the skill and evaluating its output. Most requirements fall here.
   - **Manual** — the requirement cannot be tested by an AI agent because it depends on: real HITL interaction during skill execution (not simulated inline answers), visual/UI inspection, external system state, timing/concurrency behavior, or subjective human judgment that cannot be reduced to observable output criteria.

   Every requirement must appear in at least one test (automated or manual). If a scenario covers multiple requirements, list all of them. After assigning scenarios, verify that the requirements inventory has zero uncovered items. If any requirement is uncovered, add a scenario for it or add it to an existing scenario's requirements list.

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

   **`output<NNN>.md`**: Evaluation criteria for judging the skill's output, plus one example. Format per [`tpl/tpl_test_plan.md`](../../tpl/tpl_test_plan.md) "Output File Format" section:

   ```markdown
   # Evaluation Criteria

   ## Requirements Tested
   - <RuleID>: <what this rule requires in context of this test>

   ## Pass Criteria
   - <specific, observable condition>

   ## Fail Criteria
   - <condition that means the test failed>

   ## Example Output

   <one realistic example of a passing output>
   ```

   Must:
   - List every requirement (rule ID from gr files) this test exercises under "Requirements Tested."
   - Define pass criteria that are specific and observable — not subjective ("looks right").
   - Define fail criteria capturing anti-patterns or inverse conditions.
   - Include one realistic example output for LLM-judge reference (not an exact-match target).
   - For rejection/failure tests: pass criteria describe what the skill should do instead (refuse, ask clarification); fail criteria describe what it must NOT do.

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

8. **Generate test plan.** Write `skills/test/<name>/test-plan.md` per [`tpl/tpl_test_plan.md`](../../tpl/tpl_test_plan.md):
   - Frontmatter: `skill`, `source_docs` (paths from Step 1), `source_docs_hash` (fingerprint of source doc contents at generation time — use git hash or content hash), `generated` (today's date).
   - Body split into two sections:
     - **`## Automated Tests`**: one H3 entry per fixture pair with one-sentence purpose, category, requirement IDs **with document references** (e.g., `Idea1 ([gr_idea.md](gr/gr_idea.md))`), input/output filenames, and unchecked `- [ ] Pass` item.
     - **`## Manual Tests`**: one H3 entry per manual test (numbered `M000`, `M001`, …) with category, requirement IDs with document references, `Why manual` reason, `Test procedure` steps, `Pass criteria`, and unchecked `- [ ] Pass` item. No fixture files for manual tests.
   - Requirement IDs always include the source document reference in parentheses so readers can trace back to the spec.
   - If test plan already exists and mode is `adjust`: update entries for changed/added/removed fixtures; preserve checkmarks on unchanged entries.
   - If `Replace all`: regenerate entire plan from scratch (all items unchecked).
   - **Coverage verification**: after generating, cross-check the requirements inventory from Step 1 against all test entries (automated + manual). Every requirement must appear in at least one test. If any is missing, add it before finalizing.

9. **Return.** Summary:
   ```
   draft-skill-tests <name> — status=<done|partial|aborted>
     fixtures written: skills/test/<name>/
     test plan: skills/test/<name>/test-plan.md
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
- Input fixtures must be deterministic. No timestamps, random values, external state, or session-dependent content.
- Output files define evaluation criteria + one example — not byte-exact targets. Criteria must be specific and observable. Example output is for LLM-judge reference, not exact matching.
- Minimum 2 fixtures per skill (one happy path + one failure/edge). If the skill has no failure path, minimum is 2 happy-path variants exercising different branches.
- Input files must be self-contained: every HITL answer the skill needs is embedded in the input content, in the order the skill asks.
- Zero-padded 3-digit numbering (`000`, `001`, …). When appending, continue from the highest existing number + 1.
- Scope: one skill per invocation. Do not chain to other skills or generate fixtures for multiple skills at once.
- Prefer adjusting existing fixtures over creating new ones. New fixtures only when no existing pair can sensibly be enhanced to cover the scenario. Delete only when mostly wrong.
- Source docs (coding_plan.md, guardrails.md, phases.md, gr/*.md) are the specification. The compiled skill is consulted for output format realism but never overrides source-doc requirements.
- If no source docs can be found for the skill in `coding_plan.md`, stop immediately — do not attempt to derive fixtures from the compiled skill alone.
- Every requirement from source docs must appear in at least one test (automated or manual). Zero uncovered requirements at plan completion.
- Requirement IDs in the test plan always include a document reference: `RuleID ([source_doc.md](path))`.
- Test plan must have both `## Automated Tests` and `## Manual Tests` sections. Manual section may be empty with a note "No manual tests required" if all requirements are AI-testable, but the section heading must exist.
- Manual tests: no fixture files. Procedure and pass criteria are inline in the test plan entry.
