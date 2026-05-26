---
name: make-skill
description: Closed-loop drafting, compiling, and verifying a single skill end-to-end. Wraps draft-skill-input → compile-skill → requirements verification → targeted fix, looping until the compiled skill satisfies every requirement in its source docs (coding_plan.md, guardrails.md, gr/*.md). Use when user says "make skill", "build skill end-to-end", "redo skill from changed docs", or "/make-skill <name>".
version: 1.2.1
---

Orchestrate a full skill build: draft input → compile output → verify against source docs → fix gaps → re-verify, until clean or human aborts. Wraps the existing `draft-skill-input`, `compile-skill`, and `test-skill` skills. Does not author skill content directly — only routes between them and runs the requirements-coverage gate.

## Preflight (run BEFORE Step 1 — non-negotiable gates)

**Gate A — Resolve target.** If `<name>` (or coding_plan.md row id like `A11`, `A1`) is missing, call `AskUserQuestion`:
- "Which skill do you want to make?" with two option shapes:
  - `Pick from coding_plan.md` — list every `todo`/`wip` row in the Workflows / Phase Skills / Cross-Cutting / Templates tables of `coding_plan.md`.
  - `By name` — free-text kebab-case skill name (must resolve to a row in `coding_plan.md` OR be flagged as new).
- Resolve to: `skill_id` (e.g. `A11`), kebab-case `<name>` (e.g. `distill-idea`), and the row's source-doc list.

**Gate B — State scan.** Without writing anything, record presence of:
- `skills/input/<name>-in.md` (exists / absent)
- `skills/output/<name>.md` (exists / absent)
- Recent edits to any source doc listed for the row (`coding_plan.md`, `guardrails.md`, every `gr/<file>.md` named in the row's Source doc column or per-item detail block) — use `git status` + `git log --since='30 days ago' -- <path>` to detect drift.

Frozen reference files (matching `*Ref.md`, `*-ref.md`, `*_ref.md`) are out of scope — do not read, edit, or cite. Treat as absent.

**Gate C — Mode selection.** Based on Gate B, call `AskUserQuestion` with the appropriate subset (labels verbatim):
- `Full build` — run draft → compile → verify. Default when input absent.
- `Re-draft + recompile` — source docs changed; rewrite input, then recompile. Default when source docs newer than `skills/input/<name>-in.md`.
- `Recompile only` — input unchanged; spec/source-sha drift only. Default when only `compile-skill` version moved.
- `Verify only` — read-only requirements check against existing output. No writes unless human approves surgical fixes.

No `cancel` / `proceed` / `skip`. Human cancels via Esc.

### Anti-patterns

- ❌ Editing `skills/input/<name>-in.md` or `skills/output/<name>.md` directly — those are tool-managed by `draft-skill-input` / `compile-skill`. This skill only invokes them.
- ❌ Looping silently — every iteration past the first MUST surface what changed and ask the human to continue.
- ❌ Auto-adjusting `draft-skill-input/skill.md` to paper over a single skill's gap. Pattern-level edits to the drafting skill require explicit human consent and a generic justification (not "<name> needs X").
- ❌ Treating verification "warnings" as pass — only an explicit clean run counts.

## Steps

1. **Resolve target and mode** — handled by Preflight A–C.

2. **Load source-doc set.** From `coding_plan.md`, extract the row's `Source doc` column entries and every `gr/<file>.md` referenced in the per-item detail block. Add `coding_plan.md` itself (the row text is a requirement source) and the substantive sections of `guardrails.md` referenced in the row. Do NOT load `phases.md` routing or `guardrails.md` §4.x routing / §3.29 collapse-mode — those are caller concerns, not skill content. List the resolved set back to the human before proceeding.

3. **Branch on mode.**
   - `Full build` → Step 4 (draft) → Step 5 (compile) → Step 6 (verify) → Step 7 (fix loop).
   - `Re-draft + recompile` → Step 4 → Step 5 → Step 6 → Step 7.
   - `Recompile only` → Step 5 → Step 6 → Step 7.
   - `Verify only` → Step 6 (read-only) → Step 7 (surgical-only path).

4. **Draft.** Invoke `draft-skill-input` with `<name>` (or coding_plan.md row id). That skill owns its own HITL gates (name confirm, clobber check, source-doc strip, self-check, write). Do not duplicate them here. On its `Skip compile` exit, surface that to the human — Step 5 will still run unless the human aborts.

5. **Compile.** Invoke `compile-skill` with `<name>`. That skill owns its own gates (clobber, drift, self-check). Capture: written path, version stamp, self-check pass/fail summary. If `compile-skill` errored or wrote nothing, stop and report.

6. **Verify requirements coverage.** Read `skills/output/<name>.md` and walk every item in the Step 2 source-doc set. For each numbered rule, "must" / "must not" clause, or behavior contract:
   - **Covered** — appears verbatim or as faithful paraphrase in a Hard Rule, Step, or Return spec of the output.
   - **Stripped (legitimate)** — phase-management / routing / hand-off content correctly excluded per `draft-skill-input` Step 6 strip rules.
   - **Missing** — substantive requirement absent from output AND not eligible for the strip.
   - **Contradicted** — output says something incompatible with the source doc.
   
   Print a per-source-doc table: `gr/<file>.md — N covered / M stripped / K missing / J contradicted`. Required: walk `gr/*.md` rule-by-rule (the row's anchor docs), not just spot-check. `coding_plan.md` row text and `guardrails.md` substantive sections get the same treatment.

6a. **Run fixture tests (only if Step 6 clean).** If Step 6 had any missing or contradicted, skip this step — fix coverage first. Otherwise:
   - **Pre-condition check.** Look for `skills/test/<name>/`. If absent → log "no fixture tests defined" and skip to Step 7 with tests recorded as `skipped`. Do NOT fail the build for missing fixtures; absence is allowed.
   - **Enumerate fixture pairs.** List `skills/test/<name>/input<NNN>.md` files (zero-padded 3-digit). For each, the paired reference is `skills/test/<name>/output<NNN>.md`. **Each pair is an independent test case** — when multiple pairs exist (e.g. `skills/test/distill-idea/` has 4 pairs `000`–`003`), every one must execute and every one must pass. If a paired output is missing → log as `fixture incomplete: input<NNN>.md has no output<NNN>.md`, treat as a failed test case. Orphan `output<NNN>.md` without a matching `input<NNN>.md` is also a fail. Run all cases — do not short-circuit on first failure; the human needs the full pass/fail picture per iteration.
   - **Execute each fixture.** For each pair `(input<NNN>.md, output<NNN>.md)`:
     - Invoke the compiled skill at `skills/output/<name>.md` inline (test-skill semantics: read body, strip frontmatter, follow steps). Feed `input<NNN>.md` content as the driving user-side context — it should contain whatever inputs / answers the skill needs to run deterministically end-to-end (skill HITL prompts are answered from the fixture's content).
     - Capture the skill's complete output (return value, plus any files it would write — capture intended writes without committing them; fixture runs are non-destructive).
     - Diff captured output against `output<NNN>.md`. Exact byte match = **pass**. Any divergence = **fail** (record the diff).
   - **Report.** Print a per-fixture table: `input<NNN>.md → pass | fail (<short reason>)`. Roll up: `tests: <P> passed / <F> failed / <S> skipped`.

7. **Fix loop.** If Step 6 shows zero missing AND zero contradicted AND Step 6a shows zero failed (or skipped), jump to Step 9. Otherwise, classify each gap:
   - **A. Output-only surgical fix** — the missing clause is present in the input file but was dropped by `compile-skill`. Action: re-run `compile-skill` self-check path; if it persists, log as a `compile-skill` bug — surface to human, do NOT hand-patch `skills/output/<name>.md`.
   - **B. Input-file gap** — the input file itself is missing the requirement. Action: `AskUserQuestion` with options `Re-draft via draft-skill-input` (preferred — regenerates from source docs) / `Hand-edit input file` (requires explicit human consent to bypass the tool-managed rule) / `Defer this gap` (log + continue). On `Re-draft`, return to Step 4. On `Hand-edit`, the human edits — this skill does not write `skills/input/*` itself.
   - **C. Drafting-skill pattern gap** — multiple skills would hit the same gap because `draft-skill-input` or its template doesn't ask for / preserve this kind of requirement. Action: surface a one-line *generic* edit proposal for `draft-skill-input/skill.md` or `template_skill_in.md`. `AskUserQuestion`: `Apply generic edit to draft-skill-input` / `Treat as <name>-specific (go to B)` / `Defer`. Forbidden: embedding `<name>`'s name, domain, source docs, or rule wording in the generic edit.
   - **D. Source-doc gap** — the requirement the human expected isn't actually in any source doc. Action: stop and report — this is a docs-layer issue, not a skill-build issue. The human decides whether to update `gr/<file>.md` / `guardrails.md` / `coding_plan.md` first.
   - **E. Fixture-test divergence** (from Step 6a). Sub-classify per failing fixture:
     - **E1. Skill output drift** — skill behaves differently than the reference expects. Likely needs recompile (after re-draft if input changed) or a real fix path A/B/C. Route to the appropriate sub-classifier.
     - **E2. Stale reference** — the reference `output<NNN>.md` no longer reflects the intended skill behavior (source docs evolved). `AskUserQuestion`: `Update reference output<NNN>.md` (human-confirmed, write to `skills/test/<name>/output<NNN>.md`) / `Treat as E1 instead` / `Defer`. Reference updates are the ONLY hand-writes this skill performs under `skills/test/`.
     - **E3. Non-determinism** — same fixture, different output across runs. Stop and report — fixture or skill needs to be made deterministic before automation is meaningful.

8. **Log + iterate.** After EVERY verify cycle (Step 6) — pass or fail — write TWO log files sharing the same iteration counter `<NNN>` (zero-padded 3-digit, starts at `000`, increments per iteration of this build session). Create the folders if missing.

   **Input-side log** — `skills/input/log/<name>_<NNN>.md`:
   ```
   ---
   iteration: <N>
   timestamp: <YYYY-MM-DD HH:MM>
   input_sha256: <SHA-256 of skills/input/<name>-in.md at this iteration>
   ---

   ## Draft action this iteration
   <re-drafted via draft-skill-input | reused (unchanged) | hand-edited by human (confirmed) | n/a (recompile-only mode)>

   ## Source-doc set used
   <bulleted list resolved in Step 2>
   ```

   **Output-side log** — `skills/output/log/<name>_<NNN>.md`:
   ```
   ---
   iteration: <N>
   timestamp: <YYYY-MM-DD HH:MM>
   compile_version: <compile-skill ver stamped on output>
   output_sha256: <SHA-256 of skills/output/<name>.md at this iteration>
   ---

   ## Coverage table
   <the Step 6 per-source-doc table verbatim>

   ## Fixture tests
   <Step 6a per-fixture table; or "skipped — no skills/test/<name>/"; or "skipped — coverage unclean">

   ## Gap classification
   <Step 7 classification per gap: A/B/C/D/E + one-line rationale>

   ## Action taken next
   <recompile | re-draft | generic edit to draft-skill-input | hand-edit input | update fixture reference | deferred | none — clean pass | handoff_to_human>
   ```

   Then: if Step 6 was clean → jump to Step 9. If unclean AND iteration count < 3 → return to Step 6 after the Step 7 action completes. If iteration count == 3 AND still unclean → **hard stop, handoff to human**. Do NOT ask "continue?" — the cap is fixed. Emit a handoff summary (Step 10 format) with `status: handoff_to_human` and the full list of unresolved gaps + their last classification. Human resumes manually by re-invoking `/make-skill <name>` (which starts a fresh build session, iteration counter resets to 0) after addressing the root cause.

9. **Return.** One-line summary per artifact touched plus the final coverage + test tables:
    ```
    make-skill <name> — status=<clean|handoff_to_human|aborted>, mode=<chosen mode>, iterations=<N>/3
      draft: <wrote|reused|skipped> skills/input/<name>-in.md
      compile: <wrote|reused|skipped> skills/output/<name>.md (v<ver>)
      verify: <X covered> / <Y stripped> / <Z missing> / <W contradicted> across <D> source docs
      tests: <P passed> / <F failed> / <S skipped or "no fixtures">
      logs: skills/input/log/<name>_000…<NNN>.md + skills/output/log/<name>_000…<NNN>.md
      unresolved gaps: <list or none>
    ```

## Hard Rules

- Never hand-edit `skills/input/<name>-in.md` or `skills/output/<name>.md` from this skill. Routing only — `draft-skill-input` owns input writes, `compile-skill` owns output writes. Human-authorised hand-edits to input files happen outside this skill's tool calls.
- Never read, edit, or cite frozen reference files (`*Ref.md`, `*-ref.md`, `*_ref.md`).
- HITL on every mode branch (Gate C), every input-file change path (Step 7B), every generic drafting-skill edit (Step 7C). No silent loops.
- Hard cap: 3 verify iterations per build session. On the 3rd unclean verify, stop and hand off to the human — never prompt to continue past 3. Counter resets only on a fresh `/make-skill` invocation.
- Every verify cycle writes TWO log files sharing iteration counter `<NNN>` (zero-padded, starts at 000): `skills/input/log/<name>_<NNN>.md` (draft-side) and `skills/output/log/<name>_<NNN>.md` (compile+verify-side). Append-only across iterations; never overwrite a prior iteration's logs. The `skills/input/log/` and `skills/output/log/` subfolders are the ONLY hand-writable locations under `skills/input/` and `skills/output/` — the input and output skill files themselves remain tool-managed.
- Verification in Step 6 is rule-by-rule against the resolved source-doc set — not a spot-check, not a vibe pass. The coverage table is mandatory output.
- Strip phase-management / routing / hand-off content from the verification expectation set — those legitimately do not appear in the output skill (per `draft-skill-input` Step 6). Counting them as "missing" is a bug in this skill, not the output.
- A "pass" is zero missing AND zero contradicted AND zero failed fixture tests (skipped/no-fixtures is allowed). Surgical compile-skill self-check warnings that persist after one rerun → escalate to human as a `compile-skill` bug, do not silently mark pass.
- Fixture tests at `skills/test/<name>/` run automatically after a clean Step 6 — never opt-in. Absence of the folder = `skipped`, not a failure. Test outputs are byte-compared to `output<NNN>.md` references; deterministic skills only.
- When multiple `(input<NNN>.md, output<NNN>.md)` pairs exist, each is an independent test case. ALL must execute and ALL must pass for the build to be considered clean — a single failing case fails the build. Do not short-circuit on first failure; run every case so the per-iteration log captures the full pass/fail picture.
- Fixture runs are non-destructive — capture intended writes from the skill under test without committing them. The skill under test's HITL prompts are answered from the fixture's `input<NNN>.md` content.
- Hand-writes under `skills/test/` are forbidden EXCEPT updating `output<NNN>.md` reference files via the Step 7 E2 path (human-confirmed). Never create or hand-edit `input<NNN>.md` from this skill.
- Do not load `phases.md` rules or `guardrails.md` §4.x routing / §3.29 collapse-mode as verification requirements.
- Generic edits to `draft-skill-input/skill.md` or `template_skill_in.md` must be pattern-level. Embedding `<name>`, its source docs, or its domain in those edits is forbidden.
- Scope: one skill per invocation. If the build reveals a dependency skill is also missing (e.g. `A1` needs `A11` shape), stop and report — do not chain builds.
