---
name: compile-skill
description: Compile an authoring prompt at skills/input/<name>-in.md into a self-contained Claude Code skill file at skills/output/<name>.md. Use when user says "compile skill", "build skill from input", or references a skills/input/*-in.md file to generate.
version: 2.1.0
---

Generate `skills/output/<name>.md` from `skills/input/<name>-in.md`.

## Preflight (run BEFORE Step 1 — non-negotiable gates)

Both checks below MUST run before any compile work. They are gates, not steps. Do not read input, do not plan, do not call any tool other than the ones required here until both gates pass.

**Gate A — Resolve target.** If `<name>` arg missing: list files in `skills/input/` and ask which one via AskUserQuestion. Strip trailing `-in` if human supplied full input filename.

**Gate B — Refuse to clobber silently.** If `skills/output/<name>.md` exists, you MUST call AskUserQuestion with exactly these options (labels verbatim):
- `Reopen (recompile + overwrite)` — re-run full compile, overwrite, show diff summary first.
- `Self-check only` — run Step 7 read-only against existing file. No writes unless human approves fixes.

No third option. No `cancel` / `proceed` / `skip`. Human cancels via Esc — that is the runtime affordance, not a menu item you offer.

**Gate C — Drift detection.** Runs ONLY if Gate B fired (output exists). Read existing output frontmatter; compute SHA-256 of current input. Compare:

- `source-sha256` mismatch (input changed) → fold into Gate B prompt: "Input drift detected. Pick mode:" with same two options. Do not add a re-stamp option — content changed, must recompile or self-check.
- `source-sha256` match AND `compiled-against` mismatch (spec drift, content unchanged):
  - **PATCH diff** (e.g. 1.1.0 → 1.1.1): silently re-stamp `compiled-against` + `compiled` fields. Print log line: `re-stamped <old-ver> → <new-ver>, no content change`. Skip Gate B entirely.
  - **MINOR diff** (e.g. 1.1.0 → 1.2.0): AskUserQuestion with options `Re-stamp only` / `Reopen (recompile + overwrite)` / `Self-check only`. On `Re-stamp only`: update stamps, print log line, exit. On the other two: proceed as Gate B.
  - **MAJOR diff** (e.g. 1.x → 2.0): auto-run Step 7 self-check against current spec first. Classify each failure:
    - **Surgical-eligible**: wording drift, missing clause inside existing section, stale pointer, forbidden-token leak.
    - **Reopen-required**: missing mandatory section, changed artifact path, removed/renamed feature, scope-boundary violation.

    Then AskUserQuestion. Always offer `Reopen (recompile + overwrite)` and `Self-check only`. Offer `Surgical fix + re-stamp` ONLY if every failure is surgical-eligible (any reopen-required fail hides this option). Show classified self-check results in the prompt body.

    **Worked examples (anchor classification):**
    - Hard Rule says "must" where new spec says "MUST" → **surgical** (wording drift).
    - Return section missing one bullet from new spec's list → **surgical** (missing clause inside existing section).
    - Output contains "see skills/input/foo-in.md §3" → **surgical** (stale pointer; spec forbids back-references).
    - Forbidden token from input appears in output → **surgical** (forbidden-token leak).
    - Planning-artifact skill has no `status_<artifact>.md` emission block, new spec mandates it → **reopen-required** (missing mandatory section).
    - Output emits shared `status.md` instead of artifact-scoped `status_<artifact>.md` → **reopen-required** (changed artifact path).
    - Output writes artifact to repo root; new spec mandates `<artifacts>/<WI>/` → **reopen-required** (changed artifact path).
    - Output orchestrates a downstream phase that input explicitly excluded → **reopen-required** (scope-boundary violation).
    - New spec drops the old "Args" section entirely; output still has one → **reopen-required** (removed feature).

    Borderline: if a fail could plausibly fit both, classify as **reopen-required**. Conservative bias — surgical path is the exception, not the default.
- Both stamps match → proceed to Gate B unchanged.

### Anti-patterns (do not do these)

- ❌ Offering a `Cancel` / `Proceed` / `Yes, compile` menu instead of `Reopen` / `Self-check only`.
- ❌ Skipping Gate B when output exists ("file is small, just recompile").
- ❌ Reading input before Gate B fires (wastes context if human picks self-check).
- ❌ Collapsing the two gate options into one ("Reopen?" yes/no).

## Args

Resolved in Preflight Gate A. See above.

## Steps

1. **Locate input.** Read `skills/input/<name>-in.md`. If absent, stop and report missing file.

2. **Clobber check.** Handled in Preflight Gate B. If you reached this step, the human already chose `Reopen` (continue to Step 3) or `Self-check only` (jump to Step 7).

3. **Distill.** The input is an *authoring prompt* — scaffolding, metadata, source-doc pointers, scope notes. The output is a *runtime skill* — self-contained, leaf artifact. Extract from input:
   - One-paragraph role statement (purpose, scope boundary).
   - Ordered **Steps** section (one sentence per step; expand only where ambiguity would cause wrong behavior).
   - **Hard Rules** block (imperative, no source references).
   - **Return** / **Handoff** section specifying success and failure signal shape.

   **Planning-artifact skills** (skills whose purpose is to produce a planning file — idea, goals, alignment, PRD, design, ticket, etc.): the generated skill MUST write its artifact to `<artifacts>/<WI>/<filename>.md`, where `<WI>` is a unique work-item slug (e.g. `ai_mail`, `fix_crash_abc`). The skill MUST prompt the human for `<WI>`, suggesting a slug derived from the brief; the human confirms or overrides. Create the `<artifacts>/<WI>/` directory if missing. Never write planning artifacts to repo root or any other location.

   **Status tracking.** Every planning-artifact skill MUST also write/update its OWN dedicated status file `<artifacts>/<WI>/status_<artifact>.md` on every run, where `<artifact>` is the basename of the artifact the skill produces (e.g. `distill-idea` → `idea.md` → `status_idea.md`; a `compose-prd` skill → `prd.md` → `status_prd.md`). One status file per planning artifact — never a shared `status.md`. Format:
   ```
   ---
   status: open | wip | done
   updated: <YYYY-MM-DD>
   ---
   ```
   State machine:
   - `open` — folder exists but skill not yet run / no artifact generated (rare; only if human pre-created folder).
   - `wip` — skill ran, artifact drafted or partial. Default on first skill run.
   - `done` — set ONLY after explicit human confirmation. Skill may propose `done` when it judges the artifact complete, but MUST ask the human to confirm before flipping. Never auto-flip.

   On every run the generated skill MUST: (a) refresh the `updated:` date to today, (b) set `status: wip` by default, (c) ask the human "mark done?" at end of every run UNLESS it is absolutely obvious and undoubtable that the artifact is still open/wip (e.g. under-budget failure, human rejected the draft, no human acceptance reached, count gate not passed) — in those clear-incomplete cases skip the prompt, (d) preserve an existing `done` unless human explicitly reopens — on reopen, flip `done → wip` (never back to `open`). Never auto-flip to `done` without explicit human yes.

4. **Inline everything.** Embed any rule the skill needs at runtime. Strip all "see X", "per guardrails §Y", file-path pointers to author-time source docs. The output must execute correctly as the only file in the repo.

5. **Honor scope boundaries declared in the input.** If the input says "does not hand off to X" or "no phase orchestration", do not introduce those concerns in the output.

6. **Write** the result to `skills/output/<name>.md`. Output frontmatter MUST include:
   ```
   compiled-against: compile-skill v<MAJOR.MINOR.PATCH>
   source: skills/input/<name>-in.md
   source-sha256: <64-hex>
   source-modified: <YYYY-MM-DD HH:MM>
   compiled: <YYYY-MM-DD HH:MM>
   ```
   Read compile-skill's own `version:` from its frontmatter — do not hardcode. Compute SHA-256 of input file bytes; this is the source of truth for drift detection. mtime kept as human-readable hint only. Local time, 24h, minute precision.

7. **Self-check.** Read-only verification. Print pass/fail per item; if any fail, ask human before modifying the output file. Check:
   - Every "must / must not" clause from the input is present as a Hard Rule or Step.
   - Format requirements and forbidden tokens honored.
   - Output is leaf — no links to input or author-time docs.
   - If planning-artifact skill: writes to `<artifacts>/<WI>/<filename>.md` AND emits `<artifacts>/<WI>/status_<artifact>.md` (artifact-scoped, never shared `status.md`) per Status tracking spec (open/wip/done state machine, human-only `done`, reopen flips `done → wip`).
   - Scope boundaries from input respected (no introduced handoffs/orchestration).

   If human approves fixing a failed item: apply a **surgical edit** targeting only the failing clause. Never trigger a full recompile from this path — manual edits to the output must be preserved. If multiple fails require sweeping changes, report that and ask the human to choose `reopen` instead.

8. **Return.** One-line summary: path written + step/rule counts + self-check result.

## Versioning

compile-skill uses semantic versioning (`MAJOR.MINOR.PATCH`), bumped manually in this file's frontmatter when spec changes:

- **MAJOR** — breaking change to generated-skill contract (new mandatory section, changed artifact paths, removed feature). All prior outputs need `reopen` recompile.
- **MINOR** — additive change (new optional check, new advisory clause). Prior outputs still valid; recompile optional.
- **PATCH** — clarification, typo, internal refactor. No recompile needed.

On every run, compare the existing output's stamps to current state:

- **Spec drift** — `compiled-against:` vs current `version:`. MAJOR differs → warn + recommend `reopen`. MINOR differs → advisory. PATCH differs → silent.
- **Input drift** — `source-sha256:` vs SHA-256 of current input file. Mismatch → warn at MAJOR-equivalent level, force reopen-vs-self-check-only choice. mtime mismatch alone (hash unchanged) → silent.

If both spec drift and input drift fire, combine into a single warning.

## Hard Rules

- Output path is exactly `skills/output/<name>.md`. No other writes.
- Output skill is leaf — no links back to input or author-time docs.
- Preserve every "must" and "must not" from the input as a Hard Rule or Step in the output.
- Forbidden tokens declared in input stay out of the output verbatim.
- HITL on overwrite. Never silently replace an existing output file.
- No invention. If the input is silent on a section, omit it — do not pad with generic skill boilerplate.
- Planning-artifact skills MUST emit `<artifacts>/<WI>/status_<artifact>.md` (one per artifact, never shared `status.md`) per the Status tracking spec above. Non-planning skills MUST NOT.
