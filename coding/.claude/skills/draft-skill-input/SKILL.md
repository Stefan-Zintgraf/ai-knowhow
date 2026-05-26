---
name: draft-skill-input
description: Draft a new skills/input/<name>-in.md authoring prompt from project documentation (coding_plan.md, phases.md, guardrails.md, gr/*.md). Use when user says "draft skill input", "new skill input", "author a skill input from docs", or wants to create the input file for a skill described in coding_plan.md before running /compile-skill.
version: 1.0.0
---

Generate `skills/input/<name>-in.md` from project documentation. The output is the authoring prompt that `compile-skill` consumes — it is NOT the runtime skill.

## Preflight (run BEFORE Step 1 — non-negotiable gates)

**Gate A — Resolve purpose.** If neither a skill name nor a `coding_plan.md` item identifier was passed as an argument, ask the human via `AskUserQuestion`:
- "What skill do you want to draft an input for?" — offer at minimum these option shapes:
  - `Pick from coding_plan.md` — show the available coding_plan.md items below.
  - `Describe a new skill purpose` — free-text purpose (one or two sentences).
- If `Pick from coding_plan.md`: list every entry in `coding_plan.md` tables (Workflows W*, Phase Skills A*, Cross-Cutting B*, Templates C*) that has status `todo` or `wip` and no existing `skills/input/<derived-name>-in.md`. Ask which one.
- If `Describe a new skill purpose`: capture the free-text purpose. This becomes the basis for steps 4–7 (no coding_plan.md row to look up — rely on the purpose + the general project docs).

**Gate B — Suggest name and confirm.** Derive a kebab-case skill name:
- From a coding_plan.md row: use the skill name already shown (e.g. `A11. distill-idea` → `distill-idea`).
- From a free-text purpose: produce a short verb-noun kebab-case suggestion (e.g. "summarize a code review into action items" → `summarize-review`).
Then `AskUserQuestion`: "Suggested skill name: `<name>`. Accept or override?" Options: `Accept` / `Override` (free text).

**Gate C — Clobber check.** If `skills/input/<name>-in.md` already exists, `AskUserQuestion` with exactly these two options (labels verbatim):
- `Reopen (rewrite full draft)` — re-run full draft, overwrite on acceptance, show a brief diff summary first.
- `Self-check only` — run Step 8 read-only against the existing file. No writes unless human approves surgical fixes.

No third option. No `cancel` / `proceed` / `skip`. Human cancels via Esc.

### Anti-patterns

- ❌ Auto-naming without confirmation.
- ❌ Silently overwriting an existing input file.
- ❌ Collapsing Gate C options into a yes/no.
- ❌ Inventing source docs or skill metadata not present in `coding_plan.md`.

## Steps

1. **Purpose + name** — handled in Preflight A and B.

2. **Clobber gate** — handled in Preflight C. If reached this step, human chose `Reopen` (continue) or `Self-check only` (jump to Step 8).

3. **Locate skill record.** Read `coding_plan.md`. Find the target in the Workflows / Phase Skills / Cross-Cutting / Templates tables. Extract: `skill_id` (e.g. A11), `phase` (e.g. `ide`), `workflow_ref` (e.g. W15), `depends_on`, `feeds_into` (often a hand-off to A1 / A2 etc. — infer from the workflow chain), `status`, `source doc list`, and the full per-item detail section (W## / A## / B## / C## block). If the human used free-text purpose, skip table lookup; record `skill_id: none`, `phase: none`, `workflow_ref: none`.

4. **Read source docs — narrowly.** Read each source document listed for the target:
   - For coding_plan.md entries: every `gr/*.md` file linked in the row's "Source doc" column AND any others referenced in the per-item detail section.
   - Read the matching `phases.md` entry **only to understand context — never to derive rules**. `phases.md` is phase-management; rules from it do not belong in the skill body. By default, DO NOT list `phases.md` in the draft's Source Documents table.
   - For `guardrails.md`: extract only **substantive** rules (e.g. §3.32 idea-substance). Skip phase-routing (§4.x) and collapse-mode (§3.29) entries — those are caller concerns. By default, DO NOT list routing or collapse-mode sections in the draft's Source Documents table.
   - Do NOT load every `gr/*.md`. Only the ones the target references.
   - For each `gr/<file>.md`, identify which numbered rules are phase-coupling (mention phase tokens, hand-offs, routing) and mark them for the Step 6 strip — do NOT carry them into Rules.

4a. **Read referenced Pocock SKILL.md bodies (mandatory).** For the target row, identify every Pocock reference skill named in the row's "Pocock reference skill" column AND any names embedded in the per-item "Pocock skill as additional input" line. Resolve each name to its current path via the `coding_plan.md` section "Pocock skill index (authoritative names, May 2026)". Read the **full SKILL.md body** at `..\skills-plugins\matt_pocock_skills\skills\<category>\<name>\SKILL.md` (relative to the project root `c:/PROJ/ai-knowhow/coding/`).

   Rules for this step:
   - Walkthrough excerpts are **historical-only** when a current Pocock skill exists. The current SKILL.md is the source of truth; walkthrough phrasing only supplements when no current Pocock skill covers the topic.
   - If a Pocock reference name in coding_plan.md does not resolve in the Pocock index (rename / drop / split), STOP and ask the human — do not silently substitute.
   - If multiple Pocock skills are cited for one row (e.g. W1 cites both `grill-me` and `grill-with-docs`, W3 cites `to-issues` + `triage`), load **all** named bodies before drafting.
   - List each loaded Pocock SKILL.md path in the draft's `## Source Documents (author-time only)` table, marked `(Pocock reference — author-time only, do not embed wholesale)`.
   - Do NOT copy Pocock rules verbatim into our Rules section. Treat Pocock content as **comparison material**: where our `gr/*.md` already covers a rule, prefer ours; where Pocock has substantive coverage our `gr/*.md` lacks AND it survives the Step 6 phase-strip, surface the gap to the human in Step 8 — flag it, do not silently adopt.
   - Reconciliation rule: if Pocock SKILL.md and our `gr/*.md` directly contradict, the draft must NOT silently pick one. List the contradiction in Step 8 review output for human decision.

5. **Classify: planning-artifact or not.** Default: **planning-artifact**. Almost every phase skill writes a single canonical file under `plan/<WI>/<artifact>.md` + `plan/<WI>/status_<artifact>.md` with the open/wip/done state machine (Idea7-style; see also 3.27, 3.33). The draft input file MUST include:
   - the artifact filename (`plan/<WI>/<artifact>.md`),
   - the status file (`plan/<WI>/status_<artifact>.md`) with full frontmatter spec — `status: open|wip|done`, `updated: <YYYY-MM-DD>`, `owner-issue: #NNN` on the anchor artifact (idea); inherited by siblings,
   - an explicit **owner-issue prompt at write-time** in the artifact-write step — required field; `#TBD` placeholder allowed only with a warning that merge-gate retirement enforcement will fail until replaced,
   - the state-machine rules: refresh `updated:` every run, default `wip` on write, human-only `done`, never auto-flip, `done → wip` on reopen, no writes on failure.

   Ephemeral exception: ONLY if `coding_plan.md` AND the source `gr/*.md` BOTH explicitly forbid in-tree artifacts for this skill AND the human confirms when asked. Two-source agreement plus HITL gate — otherwise default wins. Borderline cases → ask the human.

6. **Strip phase-management concerns aggressively.** Read the source docs critically. Mark as out-of-scope (Scope "does not" bullets) — never as Hard Rules — any rule that:
   - Names a phase token (e.g. `aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`).
   - Describes hand-off to / invocation of another phase or skill.
   - Describes routing, collapse-to-confirmation between phases, or "proceed to X" behavior.
   - Names a downstream consumer by phase rather than by skill name.
   
   The draft's Scope section should explicitly say "Phase orchestration is the caller's job. The skill's return is just: the output, plus a status signal."
   
   **The strip applies to Rules, Behaviors, Constraints, Return shape, AND every piece of prose in the draft — including failure messages, stripped-detail notes, collapse-mode prompts, and example return strings.** Common leak patterns to hunt and rewrite:
   - "proceed to `<phase>` directly" → `status: not_produced, reason: <short>`.
   - "deferred to `<phase>`" / "deferred to `<phase>/<phase>`" → "Stripped detail: `<item>`" (per item, no phase name).
   - "feeds into `<phase>`" / "hands off to `<phase>`" → name the consuming skill (`A1 align-concept`) or drop entirely.
   - "next phase is `<phase>`" → drop; return-to-caller is silent.
   - Collapse-mode that silently quotes back upstream goals → must offer the human an explicit choice ("treat as confirmed, or run full pass?") — never silent short-circuit.

7. **Draft the input file from the template.** Read `template_skill_in.md` (alongside this SKILL.md). Fill every placeholder; do not deviate from the section order or `---` separators. The template defines:

   - `# Authoring Prompt: \`<name>\` Skill (<skill_id>)` header.
   - `## Metadata` YAML — `feeds_into` uses `[<A##-name>]` form (name embedded), not bare `[A##]` with a comment that names a phase.
   - `## Scope` — one paragraph stating the single thing; bulleted "does not" list (out-of-scope from Step 6); closing line on caller ownership.
   - `## Self-Containment Mandate` — name the excluded source docs explicitly.
   - `## Source Documents (author-time only)` — only docs read in Step 4 and surviving Step 6; include a `Note:` line listing explicitly excluded files/sections and why.
   - `## Content That Must Be Embedded → ### Rules` — numbered, imperative, no phase tokens, no "see X" references. Aim for the minimum substantive set (typically 4–8 rules); behavior mechanics live in Steps, not Rules.
   - `## Skill Behaviors` — ordered; count-gate / failure cases use `status: not_produced, reason: …` not "proceed to <phase>".
   - `## Constraints` — bulleted must/must-not, including an explicit "No phase orchestration" constraint.
   - `## Output Format (for the generated skill)` — list the phase tokens this skill MUST NOT mention (derive from Step 6's strip list).

8. **HITL review.** Present the full draft to the human. Wait for explicit accept / edit / reject. Forbidden: auto-write, treating silence or acknowledgement as acceptance.

9. **Self-check** (runs after Step 8 acceptance OR when invoked via Gate C `Self-check only`). Read-only verification of the draft (or existing file) against source docs. Print pass/fail per item:
   - Every **substantive** `must` / `must not` from source docs appears in Rules or Constraints (phase-management rules are exempt — they should be absent).
   - Scope matches `coding_plan.md` item description (no expansion, no narrowing).
   - Planning-artifact classification correct: default is artifact-producing; ephemeral requires both-source agreement (Step 5) — if only one source says ephemeral, fail.
   - For planning-artifact skills: artifact path, status file path, full frontmatter spec (`status` + `updated` + `owner-issue`), explicit owner-issue prompt at write-time (with `#TBD` fallback + warning), and state-machine rules (`wip` default, human-only `done`, `done→wip` on reopen, no writes on failure) all present in the draft.
   - No invented behavior (no rule without a source doc origin).
   - Self-containment mandate present and names excluded source docs.
   - **Zero phase tokens** in the **entire body** outside the `Metadata.phase` field — grep across Rules, Behaviors, Constraints, Return shape, prose, examples, and failure messages for `aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`. Any hit outside metadata is a fail. Hot spots: count-gate failure strings, stripped-detail notes, collapse-mode prompts, return-section examples, anti-pattern bullets.
   - **Zero forbidden phrasings**: grep for `proceed to`, `deferred to <phase>`, `hand off to`, `feeds into <phase>`, `next phase`. Any hit is a fail.
   - Failure outcomes use `status: not_produced` + `reason:` language exclusively.
   - Collapse-mode (if present) offers human an explicit choice; no silent quote-back-and-confirm.
   - Template section order and `---` separators preserved.
   - **Pocock SKILL.md coverage**: every Pocock skill named in the target coding_plan.md row appears in the draft's Source Documents table, marked author-time-only. Any contradiction with our `gr/*.md` is explicitly listed for human review (not silently resolved).
   
   If any fail and human approves: apply surgical edits. If multiple sweeping fails: ask human to choose `Reopen` instead.

10. **Write.** On human acceptance, write `skills/input/<name>-in.md`. No other writes. On reopen path: overwrite existing. On self-check-only path: apply only approved surgical fixes.

11. **Compile (post-draft chain, opt-in).** After a successful write in Step 10, ask the human via `AskUserQuestion`: "Compile `skills/input/<name>-in.md` now via `compile-skill`?" Options (in this order — default is the second):
    - `Compile now` — invoke the `compile-skill` skill → produces `skills/output/<name>.md`. Required precondition for Step 12.
    - `Skip compile (default)` — exit pipeline after draft; Step 12 is skipped regardless of `-ref.md` presence.

    Skipped entirely on self-check-only path unless the human explicitly requests a recompile.

12. **Reference reconciliation (generic-only).** Precondition: Step 11 produced `skills/output/<name>.md`. If Step 11 was `Skip compile`, skip this step entirely — no diff, no prompt, no log entry. Otherwise, if `skills/output/<name>-ref.md` exists:
    - Diff `skills/output/<name>.md` against `skills/output/<name>-ref.md`.
    - Present each delta to the human with two readings side-by-side:
      - **Specific reading** — what the delta means if treated as a `<name>`-only fix (forbidden to apply).
      - **Generic reading** — what pattern-level improvement to `draft-skill-input/SKILL.md` or `template_skill_in.md` would cover this delta for any future skill (e.g. missing section type, ordering rule, phrasing convention, classification heuristic, template gap).
    - Human decides per delta whether the generic reading is real or whether the delta is `<name>`-specific noise. Do not apply a heuristic; ask.
    - Via `AskUserQuestion` per delta, options:
      - `Apply generic edit` — patch SKILL.md and/or template with the generic reading. HITL on the exact edit text. Forbidden: embedding `<name>`'s name, domain, source docs, or rule wording.
      - `Discard as skill-specific` — log and move on.
      - `Skip reconciliation` — abort remaining deltas, exit.
    - If no `-ref.md` exists, skip silently.

13. **Return.** One-line summary: drafted path + compiled path (if Step 11 ran) + reconciliation outcome (none / skipped / N edits-applied) + section/rule/step counts + planning-artifact flag + self-check result. On rejection or failure: emit nothing written and reason.

## Hard Rules

- Output path is exactly `skills/input/<name>-in.md`. No other writes.
- No invention — every rule, behavior, and constraint in the draft must trace to a source document or the user-supplied purpose. If silent, omit.
- HITL on accept — explicit human acceptance required before any write.
- HITL on overwrite — never silently replace an existing input file.
- HITL on name — never write without explicit human confirmation of the skill name.
- Scope faithfulness — draft Scope section matches `coding_plan.md` item description (or user purpose) exactly — no expansion, no narrowing.
- Planning-artifact classification is mandatory and must be correct. Default = artifact-producing; ephemeral requires Step 5's two-source-plus-HITL gate. Getting it wrong causes `compile-skill` to produce a broken output skill.
- Phase orchestration is the caller's concern — do not embed phase-routing or hand-off-to-X language as Hard Rules, Behaviors, Constraints, or Return prose of the target skill (Step 6).
- Zero phase tokens (`aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`) anywhere in the draft body outside the `Metadata.phase` field — including failure messages, stripped-detail notes, examples, and collapse-mode prompts.
- Zero forbidden phrasings: `proceed to <phase>`, `deferred to <phase>`, `hand off to <phase>`, `feeds into <phase>`, `next phase`.
- Use `template_skill_in.md` as the structural skeleton — section order and `---` separators are not optional.
- Prefer `status: ok` / `status: not_produced` + `reason:` over "proceed to <phase>" language for failure or short-circuit outcomes.
- `phases.md` and `guardrails.md` routing/collapse sections are author-time context only — never list them as source docs in the draft, never derive Hard Rules from them.
- Do not load source docs not listed for the target skill. Read narrowly.
