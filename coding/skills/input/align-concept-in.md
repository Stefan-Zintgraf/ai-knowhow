# Authoring Prompt: `align-concept` Skill (A1)

## Metadata

```yaml
skill_id: A1
skill_name: align-concept
phase: aln
status: todo
workflow_ref: W1
depends_on: []
feeds_into: [A2-compose-prd]
```

---

## Scope

The skill does **one** thing: run a grilling session that turns a brief (and, when available, a pre-distilled goal list) into a shared design concept — an alignment transcript plus an agreed module map — and persist it to `plan/<WI>/alignment.md`.

The skill does **not**:

- Manage workflow transitions or name downstream phases in its output.
- Hand off to, invoke, or describe any other skill or phase.
- Write a PRD, decompose issues, or describe what happens after the artifact is written.
- Decide whether the work proceeds after the artifact is accepted.

Phase orchestration is the caller's job. The skill's return is just: the transcript, the module map, the artifact path, plus a status signal.

---

## Self-Containment Mandate

The output skill must run **without** `gr/gr_algn.md`, `phases.md`, or `guardrails.md` in context or on disk. Every rule the skill needs at runtime must be **inlined** into the skill file. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Source Documents (author-time only)

| File                                                                          | Relevant sections                                                                                                                            |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `gr/gr_algn.md`                                                               | Aln1–Aln7, Aln9–Aln12, Aln15 (in-session rejections only), Aln16; Anti-Patterns (drop bullets that name phases or PRD)                       |
| `videos/matt_pocock_full_walkthrough_workflow_gpt55pro.md` §0:13:45–0:21:43   | "grill me" demo — one-question-at-a-time, recommend-an-answer, walk-every-branch, subagent for codebase facts                                |

Note: `phases.md`, `guardrails.md` routing/collapse sections, Aln8 (cross-refs upstream phase), Aln13 (PRD coupling), Aln14 (re-route on discovery), and Aln15 "Intake from `pro`" subsection (cross-phase artifact mechanics) are phase-management concerns. Out of scope for this skill — do not embed.

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. **HITL only** — no AFK execution. The human must be present and engaged throughout. Wait for explicit human acceptance before any artifact write.
2. **One question per turn.** Multi-question batches are forbidden; each branch is walked, not jumped.
3. **Every question carries a recommended answer** with reasoning. A question without a recommendation is a quiz, not a design conversation. The human accepts, modifies, or rejects.
4. **Walk every branch with a real decision**, including the ones that look obvious. Resolve dependencies in order — question B is not asked until question A is resolved.
5. **Brief is input, not truth.** The original brief (Slack message, ticket, email, prior goal list) is the prompt for grilling — never the alignment itself. Even when a clean goal list exists, grill against it.
6. **Subagent for codebase facts.** When the session needs facts about the existing codebase, dispatch a subagent with an isolated context that returns a summary. The grilling agent's main context stays uncluttered.
7. **Hidden-constraint checklist before close.** Before the session is allowed to close, raise each class explicitly and record `covered` / `not_applicable` / `missing` per the human:
   - Security (auth, secrets, input validation, PII)
   - Permissions / authorization
   - Data retention
   - Migrations (schema or data)
   - Observability (logs, metrics, traces)
   - Public API compatibility
   - Concurrency (multiple agents, users, processes on same state)
   - Out-of-scope
   Silent omission of a class is forbidden.
8. **Negative decisions are captured.** Every "we will not do X" answer is recorded as a negative decision in the transcript with its rationale. Negative decisions are how scope is defended later.
9. **Module map is an output, not an afterthought.** By the end of the session, the human and agent agree on which modules will be touched, which are new, and what each new module's public interface looks like. Module-shape decisions belong here.
10. **Decision-tree visualization.** Maintain and display a visual map of the decision tree (e.g. Mermaid `graph TD`) throughout the session — root goal, walked branches with the decision made, pending branches with the open question. Refresh after every accepted answer.
11. **Length is open-ended.** Sessions may run dozens to ~100 questions. Do not shortcut to "be helpful." On human fatigue, offer to pause and resume; never offer to skip remaining branches.
12. **Pair with the right human.** Flag the kind of human each pending question needs — domain expert, developer, or both. When the wrong human is in the loop, say so rather than push through.
13. **Domain transcripts are inputs, not replacements.** A supplied meeting transcript or written source-of-truth may be fed into the session to validate or generate questions against it. It does not stand in for grilling.
14. **Single canonical artifact.** On accept, write the transcript + module map to `plan/<WI>/alignment.md` and nowhere else. `<WI>` is a human-confirmed snake_case slug. No writes on failure.
15. **Status file always paired.** On every successful artifact write, write/update `plan/<WI>/status_alignment.md` with frontmatter `status` + `updated` + `owner-issue`. Human-only `done`; never auto-flip. `owner-issue:` mandatory.

---

## Skill Behaviors

In order:

1. **Pre-structured-input check.**
   Heuristically scan the input for an already-shaped goal list or prior alignment artifact at `plan/<WI>/alignment.md`. If it fires, ask the human via an explicit choice prompt: "Input already looks like <shape>: [summary]. Treat as confirmed anchor and grill from there, or run full pass from raw brief?" — never silently quote-back-and-confirm. If "treat as confirmed", use it as anchor for step 3. Otherwise proceed. If heuristic does not fire, proceed silently.

2. **Initialize decision tree.**
   Render the root goal(s) as the root of a Mermaid `graph TD` and display it. Add a placeholder pending branch per major area implied by the input. Refresh the rendered tree after every accepted answer in step 3.

3. **Grilling loop.**
   Repeat until every branch with a real decision is resolved: pick the next unresolved branch respecting dependencies; ask exactly one question; offer a recommended answer with reasoning; record human accept / modify / reject as the resolved decision; update the tree. Walk obvious branches explicitly. Capture every "we will not do X" answer as a negative decision in the transcript with rationale.

4. **Subagent dispatch.**
   When a question requires facts about the existing codebase, dispatch a subagent with isolated context, receive a summary, and resume grilling. Do not pollute the main context with raw exploration output.

5. **Right-human check.**
   Before asking a domain question of a developer (or vice versa), flag the mismatch and offer to pause until the right human is in the loop.

6. **Hidden-constraint checklist.**
   Before declaring the session closed, walk the eight classes explicitly (Security, Permissions, Retention, Migrations, Observability, Public API compatibility, Concurrency, Out-of-scope). Record `covered` / `not_applicable` / `missing` per class with one-line rationale. If any class is `missing`, the session is not closeable — return to step 3 with a branch for that class.

7. **Module map proposal.**
   Propose a module map: modules touched, modules new, public interface sketch per new module. Run it past the human for explicit accept / modify.

8. **Count gate / pause gate.**
   If the session ends with fewer than ~5 resolved decisions and no `not_applicable`-everywhere hidden-constraint pass: return `status: not_produced` with `reason: under-grilled`. **Forbidden phrases in the failure string**: any phase token, `proceed to <phase>`, `deferred to <phase>`, `next phase`. If the human signals fatigue mid-session, offer pause-and-resume (preserve tree + transcript state); never offer to skip remaining branches.

9. **HITL accept.**
   Present the assembled transcript + module map + hidden-constraint checklist + negative-decision list to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating acknowledgement as acceptance.

10. **Artifact write.**
    Derive a candidate `<WI>` slug from the input (short, snake_case — e.g. `ai_mail`, `fix_crash_abc`). Prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Then prompt: "Owner issue (e.g. `#123`)?" — required; the WI anchor for retirement. If the human has no issue number yet, accept a placeholder `#TBD` and explicitly warn that merge-gate retirement enforcement will fail until replaced. Create `plan/<WI>/` if missing. Write to `plan/<WI>/alignment.md` with sections in this order: `# Root Goals`, `# Decision Tree` (Mermaid block), `# Resolved Decisions` (numbered Q/A with rationale), `# Negative Decisions` (numbered with rationale), `# Hidden-Constraint Checklist` (table of 8 classes × covered/not_applicable + one-line note), `# Module Map` (touched / new / public interfaces).

11. **Status file write.**
    Write/update `plan/<WI>/status_alignment.md` with frontmatter:
    ```
    ---
    status: open|wip|done
    updated: <today YYYY-MM-DD>
    owner-issue: #NNN   # mandatory on the anchor artifact; siblings inherit
    ---
    ```
    Rules: (a) refresh `updated:` to today on every run; (b) default `status: wip` after a successful artifact write; (c) ask the human "mark done?" at end of run UNLESS the run is a clear-incomplete (under-grilled, human rejected, no acceptance) — in those cases skip the prompt; flip to `done` only on explicit human yes, never auto-flip; (d) preserve existing `done` unless the human explicitly reopens — on reopen, flip `done → wip` (never back to `open`). On failure runs (no artifact written), do NOT create or modify the status file.

12. **Return.**
    Emit:
    - The resolved decision list, negative-decision list, hidden-constraint checklist, and module map (inline summary).
    - Path written: `plan/<WI>/alignment.md`.
    - Status file: `plan/<WI>/status_alignment.md` (`status: wip` unless human confirmed `done`).
    - A success signal: `status: ok` plus one-line summary ("Resolved N decisions across M branches; module map agreed.").
    On failure (under-grilled, human rejected, no acceptance reached), emit `status: not_produced` plus the reason. Write nothing. No phase names. No "next step" / "proceed to" / "deferred to" language anywhere in the failure string.

---

## Constraints (must appear as Hard Rules inside the skill)

- **One question per turn**: multi-question batches forbidden.
- **Recommendation mandatory**: never ask without an offered answer + reasoning.
- **No silent branch-skipping**: every real-decision branch is walked.
- **No silent constraint omission**: all eight hidden-constraint classes raised explicitly before close.
- **Subagent for codebase facts**: main context is not polluted with raw exploration output.
- **HITL only**: explicit human acceptance required; no AFK execution.
- **Single canonical artifact path**: `plan/<WI>/alignment.md`. No alternative locations. No writes on failure.
- **Status file paired**: every successful artifact write produces/updates `plan/<WI>/status_alignment.md` per the spec in Step 11. One status file per artifact — never a shared `status.md`.
- **owner-issue mandatory**: `status_alignment.md` frontmatter MUST carry `owner-issue:`. Prompt the human at write-time; accept `#TBD` only with an explicit warning that merge-gate retirement enforcement will fail until replaced.
- **No phase orchestration**: the skill does not name, invoke, or hand off to other phases or skills. Output is the transcript, module map, artifact path, and a status signal — nothing more.

---

## Output Format (for the generated skill)

The output skill (`skills/output/align-concept.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill runs a grilling session that produces a shared design concept (alignment transcript + module map) and writes it to `plan/<WI>/alignment.md`. It does not manage workflow phases.
- Contains an inlined **Hard Rules** block (the 15 Rules above plus the Constraints, brief imperative form). No "see gr_algn.md §X" / "see guardrails.md §X" references.
- Has an ordered **Steps** section mapping to the 12 behaviors above (one sentence per step; expand only where ambiguity would cause wrong behavior).
- Includes the artifact path (`plan/<WI>/alignment.md`), the status file path (`plan/<WI>/status_alignment.md`), the full frontmatter spec (`status` + `updated` + `owner-issue` on the anchor), and the state-machine rules inlined verbatim.
- Has a **Return** section specifying the success/failure signal shape.
- Does **not** link to `gr/gr_algn.md`, `phases.md`, or `guardrails.md`. Does **not** mention any phase token anywhere in the body outside its `Metadata.phase` field: `aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`. This applies to Rules, Steps, Return, prose, examples, anti-pattern bullets, and failure messages.
- Does **not** contain forbidden phrasings: `proceed to <phase>`, `deferred to <phase>`, `hand off to <phase>`, `feeds into <phase>`, `next phase`. Use `status: not_produced` + `reason:` for failure outcomes.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.
