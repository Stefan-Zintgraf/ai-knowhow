---
name: test-skill
description: Run a compiled skill file inline without creating folders or artifacts. Use when user says "test skill", "run skill", or wants to try a skill from skills/output/ without side effects.
version: 1.0.0
---

Execute a skill from `skills/output/` inline in the current conversation, optionally against test fixtures. Two modes: **freeform** (no fixtures — skill runs with live HITL) and **fixture** (runs against `skills/test/<name>/` test plan and fixtures with LLM-as-judge evaluation).

## Preflight

**Gate A — Resolve target.** If `<name>` arg missing: list files in `skills/output/` and ask which one via AskUserQuestion. Strip `.md` suffix if human supplied full filename.

**Gate B — Mode selection.** Check if `skills/test/<name>/test-plan.md` exists:
- If absent → **freeform mode** (Steps 1–5 below).
- If present → ask human: "Test plan found. Run in fixture mode (against test plan) or freeform?" Default: fixture mode.

**Gate C — Staleness check (fixture mode only).** Read `test-plan.md` frontmatter. Compare `source_docs_hash` against current state of files listed in `source_docs`:
- **Match** → proceed.
- **Drift detected** → warn: "Source docs changed since test plan was generated. Tests may be outdated." Ask: "Update tests first (re-run /draft-skill-tests)?" — yes → exit with instruction to run `draft-skill-tests`; no → proceed with current tests.

**Gate D — Checklist state (fixture mode only).** Read all checklist items in `test-plan.md`:
- **All checked** → ask human: "All tests previously passed. Run again?" — yes → uncheck all items in `test-plan.md`, proceed; no → exit, keep checkmarks.
- **Some/all unchecked** → proceed with unchecked tests only.

**Gate E — Judge mode (fixture mode only).** Unless the caller passed `auto_judge: true` (e.g. invoked from `make-skill`), ask via `AskUserQuestion`:
- `Human-in-the-loop (default)` — human confirms every verdict (current behavior, with opt-out offer after first test).
- `Auto-judge` — LLM judge verdict is accepted automatically; no human confirmation per test.

Record the choice as `judge_mode` (`hitl` or `auto`). When `auto_judge: true` is passed by the caller, skip the question and set `judge_mode = auto`.

## Steps — Freeform Mode

1. **Locate skill.** Read `skills/output/<name>.md`. If absent, stop and report missing file.

2. **Extract content.** Strip YAML frontmatter (everything between and including the leading and trailing `---` delimiters). What remains is the skill body.

3. **Announce.** One line: `Running skill: <name> (freeform, no writes unless the skill itself requires them).`

4. **Execute.** Follow the skill body exactly as written — steps, hard rules, return spec. The skill runs as if invoked normally. All HITL requirements in the skill remain in force.

5. **Return.** When the skill reaches its own return/handoff step, emit that output. Append one line: `[test-skill: freeform run complete]`.

## Steps — Fixture Mode

1. **Locate skill.** Read `skills/output/<name>.md`. If absent, stop and report missing file.

2. **Extract content.** Strip YAML frontmatter. What remains is the skill body.

3. **Load test plan.** Read `skills/test/<name>/test-plan.md`. Parse the test entries (H3 sections under `## Tests`). Identify unchecked tests to run.

4. **For each unchecked test** (in order):

   a. **Announce.** `Test <NNN>: <purpose sentence from test plan>`

   b. **Run setup (if declared).** If the test entry in `test-plan.md` has a `**Setup:**` field, execute the commands described there (e.g., create directories). Setup runs before any skill execution. If setup fails, mark test FAIL with reason "setup failed" and continue to next test.

   c. **Load input.** Read `skills/test/<name>/input<NNN>.md`. This content serves as the user input for the skill.

   d. **Execute skill with tracking.** Run the skill body against the input content. All skill hard rules remain in force. HITL prompts embedded in the input are answered from the input content (answers are pre-embedded in fixture inputs by `draft-skill-tests`). During execution, maintain a tool-call log: for each tool invocation, record the tool name and a one-line summary of arguments. This log feeds tool-call assertions in step g2.

   e. **Capture output.** Collect the skill's emitted output.

   f. **Load criteria.** Read `skills/test/<name>/output<NNN>.md`. Parse the evaluation criteria (pass criteria, fail criteria, requirements tested, example output).

   g. **Check filesystem assertions (if declared).** If the output fixture contains a `## Filesystem Assertions` section, verify each assertion before LLM-as-judge runs:
      - `EXISTS <path>` — file must exist.
      - `NOT_EXISTS <path>` — file must not exist.
      - `CONTAINS <path> <pattern>` — file content must match the pattern (plain substring or `/regex/`).
      - `FRONTMATTER <path> <key> <value>` — YAML frontmatter field must equal value. Value `<today>` expands to current date `YYYY-MM-DD`.
      - Collect all assertion results (pass/fail + details) and include them in the judge input.

   g2. **Check tool-call assertions (if declared).** If the output fixture contains a `## Tool Call Assertions` section, evaluate the tool-call log from step d:
      - `MAX_COUNT <tool> <N>` — skill invoked `<tool>` at most N times.
      - `MIN_COUNT <tool> <N>` — skill invoked `<tool>` at least N times.
      - `ZERO <tool>` — skill never invoked `<tool>`.
      - Tool names match the harness tool names (Read, Edit, Write, Bash, Glob, Grep, Agent).
      - Collect all assertion results and include them in the judge input.
      - **Accuracy note:** tool-call tracking relies on LLM self-monitoring during inline execution. A programmatic test runner would enforce counts externally; this harness provides best-effort tracking.

   h. **LLM-as-judge evaluation.** Evaluate the captured output AND filesystem/tool-call assertion results against the criteria:
      - Check each pass criterion — is it met?
      - Check each fail criterion — is any triggered?
      - If any filesystem or tool-call assertion failed, the overall verdict is FAIL regardless of text output quality.
      - Compare against the example output for structural/intent alignment (not exact match).
      - Write a brief reasoning summary: which criteria passed, which failed, and why.

   i. **Run teardown (if declared).** If the test entry has a `**Teardown:**` field, execute the commands described there (e.g., delete directories). Teardown runs regardless of pass/fail — always clean up.

   j. **Present to human.** Show:
      - The skill's output (or a summary if very long).
      - Filesystem assertion results (if any).
      - Tool-call assertion results (if any).
      - The evaluation reasoning.
      - Verdict: PASS or FAIL with specific criteria cited.

   k. **Verdict resolution.** Branch on `judge_mode`:

      **If `judge_mode = auto`:** Accept the LLM judge verdict directly. PASS → check the item in `test-plan.md` (`- [x] Pass`). FAIL → item stays unchecked. No human prompt. Continue to next test.

      **If `judge_mode = hitl`:** Present verdict to human for confirmation.
      - If this is NOT the first test in the run, skip straight to confirmation (the opt-out offer was already made or declined).
      - If this IS the first test in the run AND more unchecked tests remain, use `AskUserQuestion` with three options:
        - `Approve` — confirm this verdict, keep human-in-the-loop for remaining tests.
        - `Approve + auto-judge remaining` — confirm this verdict, switch `judge_mode = auto` for all subsequent tests.
        - `Reject` — override to FAIL.
      - For subsequent tests (or if only one test): standard two-option confirm/reject.
      - Human approves PASS → check the item in `test-plan.md` (`- [x] Pass`). Write the file.
      - Human rejects (overrides to FAIL, or confirms FAIL) → item stays unchecked. Continue to next test.

5. **Summary.** After all unchecked tests are processed:
   ```
   test-skill <name> — fixture mode
     tests run: <N>
     passed: <N> (human-confirmed)
     failed: <N>
     skipped (already checked): <N>
     test plan: skills/test/<name>/test-plan.md
   ```
   Append: `[test-skill: fixture run complete]`.

## Hard Rules

- No test infrastructure created (no folders, no copies, no wrapper files) — except setup/teardown declared in test-plan entries.
- Skill hard rules and HITL gates stay fully in force — do not bypass or soften them.
- If the skill writes artifacts (e.g. planning files), it still does so — this skill does not sandbox writes.
- Scope: one skill per invocation. If the skill hands off to another skill, stop at the handoff boundary and report it; do not chain.
- **test-plan.md is the sole file test-skill writes to** — checkmark updates only. This is the single exception to the no-side-effects principle.
- **Setup/teardown are declared in test-plan.md, not invented.** The harness only runs setup/teardown steps that appear in the test entry. Never infer additional setup.
- **Teardown is mandatory after setup.** If a test declares setup, it must declare teardown. The harness always runs teardown, even on failure or early exit.
- **LLM-as-judge must show reasoning** — never silently pass or fail. Human always sees the evaluation logic before confirming.
- **Human has final say in HITL mode** — when `judge_mode = hitl`, LLM judge proposes verdict, human confirms or overrides. In `auto` mode, LLM verdict is accepted directly. Auto mode requires explicit opt-in (Gate E question or caller flag).
- **Staleness warning is mandatory** — never skip Gate C in fixture mode. Proceeding with stale tests is allowed only after human acknowledges.
