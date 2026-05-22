# Authoring Prompt: `distill-idea` Skill (A11)

## Metadata

```yaml
skill_id: A11
skill_name: distill-idea
phase: ide
status: todo
workflow_ref: W15
depends_on: []
feeds_into: [A1-align-concept]
```

---

## Scope

The skill does **one** thing: distill a raw brief (ticket, Slack note, email, vague backlog item, verbal ask) into a confirmed list of **3–6 major goals** and persist the list to `plan/<WI>/idea.md` plus its companion `plan/<WI>/status_idea.md`.

The skill does **not**:

- Triage incoming work into workflow modes (`direct-edit` / `mini` / `full`), score the 4-axis matrix, or pick which downstream pipeline runs. That is the caller's entry-triage concern.
- Create, search, dedupe, or label GH issues. Issue emission is the caller's concern.
- Generate the `<WI>` slug from a GH issue number. The caller supplies the `<WI>` slug; the skill prompts only if missing.
- Dispatch sub-agents for codebase exploration, score reversibility, or apply tripwire halts.
- Propose or execute mode upgrades / downgrades, or react to discovered tripwires mid-task.
- Hand off, route, invoke, or name any downstream skill or phase.
- Read source documents at runtime. All rules below are inlined.

Phase orchestration, mode selection, issue management, and downstream routing are the caller's job. The skill's return is just: the persisted goal list (path), a status signal, and a one-line summary.

---

## Self-Containment Mandate

The output skill must run **without** `gr/gr_idea.md`, `guardrails.md`, `tpl/tpl_idea.md`, or `phases.md` in context or on disk. Every rule the skill needs at runtime must be **inlined** into the skill file. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Source Documents (author-time only)

| File                | Relevant sections                                                                 |
| ------------------- | --------------------------------------------------------------------------------- |
| `gr/gr_idea.md`     | Idea1, Idea2, Idea3, Idea4, Idea5, Idea7 only. (Idea6 / Idea8–Idea11 stripped.)   |
| `guardrails.md`     | §3.32 (substantive distillation rule), §3.33 (retire-with-WI + status state machine). |
| `tpl/tpl_idea.md`   | File-naming, body shape for `idea.md`, frontmatter shape for `status_idea.md`, field semantics, state machine. |

Note: explicitly excluded — `phases.md` (phase routing, author-time context only), `guardrails.md` §3.29 (mode-selection routing, caller concern), `guardrails.md` §3.37 (tripwire halt + mode re-triage, caller concern), `gr/gr_idea.md` Idea6 (hand-off to downstream phase), Idea8 (mode triage matrix), Idea9 (issue emission + dedupe), Idea10 (exploration budget), Idea11 (mode transitions). Pocock: W15 names no Pocock reference skill — none loaded.

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. **Output is exactly 3–6 numbered goals.** Fewer than 3 means the brief is too narrow for goal-shaped framing; more than 6 means the goals are not yet major — decompose or merge before finalizing.
2. **No details in any goal.** Forbidden inside any goal body: module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices (library / pattern names), effort or timeline estimates. A goal names *what the work must serve*, not *how*.
3. **Negative goals are first-class.** Explicit non-goals (e.g. "not a mobile app", "no real-time updates") count toward the 3–6 budget when they materially shape the work. Prefix them exactly `Non-goal: ` (capital N, space after colon).
4. **HITL only.** No AFK / autonomous execution. The skill proposes a goal list; the human edits, accepts, or rejects. Acknowledgement is not acceptance — only an explicit accept finalizes.
5. **Brief is input, not output.** Even a well-written brief is restated as a 3–6 goal list; do not pass the brief through verbatim as the goal list.
6. **Stripped detail leaks are logged.** When implementation specifics leak from the brief into a candidate goal, strip them from the goal body and append one line per stripped item below the numbered list using exactly the format `Stripped detail: <item>` — never name any downstream phase or skill in the line.
7. **Single canonical artifact path.** The confirmed goal list is written only to `plan/<WI>/idea.md`. No `idea/<topic>.md`, no shared `idea.md`, no `<WI>.md` at repo root, no multiple idea files under one WI. The companion status file lives only at `plan/<WI>/status_idea.md`.
8. **`idea.md` is plain markdown (no frontmatter).** Heading is literally `# Goals`. One sentence per goal, no nested bullets, no prose paragraphs. The status file is frontmatter-only; body is ignored.
9. **`status_idea.md` carries mandatory `owner-issue:`.** The frontmatter MUST contain `status`, `updated`, and `owner-issue`. `owner-issue` is required because `status_idea.md` is the WI anchor; sibling artifacts under `plan/<WI>/` inherit this owner.
10. **State machine for `status_idea.md`.** `open → wip` on first successful artifact write; default `status: wip` after every successful write. `wip → done` only on explicit human confirmation — never auto-flip. `done → wip` on explicit human reopen — never `done → open`. Refresh `updated:` to today on every run. On failure runs (under-budget, human rejected, no human acceptance), write nothing — no `idea.md`, no `status_idea.md`.

---

## Skill Behaviors

In order:

1. **Pre-structured-input check.**
   Heuristically scan the incoming brief for an already-shaped goal list: a top-level `# Goals` (or near-equivalent) heading followed by 3–6 numbered single-sentence items. If it fires, ask the human via an explicit choice prompt: "Input already looks like a goal list: [list the items verbatim]. Treat as confirmed, or run a full distillation pass?" — never silently quote-back-and-confirm. If "treat as confirmed", carry that list into the HITL accept step unchanged. Otherwise proceed to step 2. If the heuristic does not fire, proceed silently.

2. **Distill the brief into a candidate goal list.**
   Read the raw brief once. Produce 3–6 candidate goals, one sentence each, expressing *what the work must serve* — not how. Include negative goals (`Non-goal: …`) where the brief implies explicit exclusions or where a non-goal materially shapes the work. Restate even well-written briefs in goal form (Rule 5); do not pass the brief through verbatim.

3. **Detail-leak strip.**
   Walk each candidate goal. Remove any forbidden detail per Rule 2 (module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, effort/timeline). For every stripped item, append one line below the numbered list using exactly the format: `Stripped detail: <item>` (one per item, no downstream-phase or skill names — never `deferred to <…>`).

4. **Count gate.**
   If the post-strip candidate count is `< 3`: return `status: not_produced` with `reason: brief too narrow for 3–6 goal framing — likely a direct task without goal-shaped intent`. Forbidden in the failure string: any phase token, `proceed to <…>`, `deferred to <…>`, `next phase`, `hand off to <…>`. If the count is `> 6`: prompt the human to merge or drop candidates until the list is 3–6 before continuing. Do not silently truncate.

5. **HITL accept.**
   Present the candidate list (numbered goals + any `Stripped detail:` lines) to the human for edit / accept / reject. Iterate edits as needed. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating acknowledgement or silence as acceptance. On explicit reject without acceptance reached, return `status: not_produced` with `reason: human rejected the draft, no acceptance reached`.

6. **Artifact write.**
   If `<WI>` was not supplied by the caller, derive a candidate snake_case slug from the brief (short, descriptive — e.g. `ai_mail`, `fix_crash_abc`, `add_oauth_provider`) and prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Then prompt: "Owner issue (e.g. `#123`)?" — required; this anchors the WI for retirement enforcement at WI close. If the human has no issue number yet, accept the placeholder `#TBD` and explicitly warn that the merge-gate retirement check will fail until `#TBD` is replaced with a real issue number. Create `plan/<WI>/` if missing. Write the accepted goal list to `plan/<WI>/idea.md` as plain markdown:

   ```markdown
   # Goals

   1. <goal sentence>
   2. <goal sentence>
   3. Non-goal: <exclusion sentence>
   4. <goal sentence>

   Stripped detail: <item>
   Stripped detail: <item>
   ```

   No YAML frontmatter on `idea.md`. The heading is literally `# Goals`.

7. **Status file write.**
   Write or update `plan/<WI>/status_idea.md` with frontmatter only (body optional and ignored):

   ```
   ---
   status: open|wip|done
   updated: <today YYYY-MM-DD>
   owner-issue: "#NNN"
   ---
   ```

   Rules: (a) refresh `updated:` to today on every run; (b) default `status: wip` after a successful artifact write; (c) ask the human "mark done?" at end of run UNLESS the run is a clear-incomplete (under-budget, human rejected, no acceptance) — in those cases skip the prompt; flip to `done` only on explicit human yes, never auto-flip; (d) preserve existing `done` unless the human explicitly reopens — on reopen, flip `done → wip` (never back to `open`); (e) `owner-issue:` is mandatory and prompted at write-time per behavior 6. On failure runs (no artifact written in step 6), do NOT create or modify the status file.

8. **Return.**
   Emit:
   - The path written: `plan/<WI>/idea.md`.
   - The status path: `plan/<WI>/status_idea.md`.
   - A success signal: `status: ok` plus a one-line summary (e.g. `distilled N goals (incl. M non-goals); K stripped detail(s); status: wip`).

   On failure (under-budget, human rejected, no acceptance reached), emit `status: not_produced` plus the reason. No phase tokens. No `proceed to <…>` / `deferred to <…>` / `next phase` / `hand off to <…>` language anywhere in the failure string.

---

## Constraints (must appear as Hard Rules inside the skill)

- **3–6 goal budget**: enforce inclusively. Below 3 → `status: not_produced`. Above 6 → HITL merge/drop before finalize.
- **No implementation detail in goals**: stripped items go in `Stripped detail:` lines, never inside a goal body.
- **`Non-goal:` prefix exact**: capital N, space after colon. Counts toward the 3–6 budget.
- **HITL only**: explicit human acceptance required before any artifact write.
- **Single canonical path**: `plan/<WI>/idea.md` + `plan/<WI>/status_idea.md` — no alternates.
- **owner-issue mandatory**: `status_idea.md` frontmatter MUST carry `owner-issue:`. Prompt the human at write-time; accept `#TBD` only with an explicit warning that the merge-gate retirement check will fail until replaced.
- **Human-only `done`**: never auto-flip `status_idea.md` to `done`. `done → wip` on explicit reopen; never `done → open`.
- **No status file without artifact**: on failure runs (no `idea.md` written), do NOT create or modify `status_idea.md`.
- **No phase orchestration**: the skill does not name, invoke, hand off to, or route to other phases or skills. Output is the persisted goal list (path) plus a status signal — nothing more.

---

## Output Format (for the generated skill)

The output skill (`skills/output/distill-idea.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill distills a raw brief into 3–6 major goals and writes them to `plan/<WI>/idea.md` + `plan/<WI>/status_idea.md`. It does not manage workflow phases.
- Contains an inlined **Hard Rules** block (Rules 1–10 above plus the Constraints, brief imperative form). No "see <doc> §X" references.
- Has an ordered **Steps** section mapping to behaviors 1–8 above (one sentence per step; expand only where ambiguity would cause wrong behavior — the artifact-write and status-file steps need the literal frontmatter and body shapes inlined).
- Includes the artifact path `plan/<WI>/idea.md`, the status file path `plan/<WI>/status_idea.md`, the full frontmatter spec (`status` + `updated` + `owner-issue` on the anchor), and the state-machine rules inlined verbatim.
- Has a **Return** section specifying the success/failure signal shape (`status: ok` + summary, vs `status: not_produced` + `reason:`).
- Does **not** link to `gr/gr_idea.md`, `guardrails.md`, `tpl/tpl_idea.md`, or `phases.md`. Does **not** mention any phase token anywhere in the body outside its `Metadata.phase` field: `aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`. This applies to Rules, Steps, Return, prose, examples, anti-pattern bullets, and failure messages.
- Does **not** contain forbidden phrasings: `proceed to <phase>`, `deferred to <phase>`, `hand off to <phase>`, `feeds into <phase>`, `next phase`. Use `status: not_produced` + `reason:` for failure outcomes; use `Stripped detail: <item>` (per item, no phase names) for leak notes.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.
