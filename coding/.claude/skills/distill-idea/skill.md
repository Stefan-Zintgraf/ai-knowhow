---
name: distill-idea
description: Distill a raw brief into 3–6 major goals and persist the confirmed list to plan/<WI>/idea.md. Use at the very start of a new work-item.
compiled-against: compile-skill v2.1.0
source: skills/input/distill-idea-in.md
source-sha256: 58112c64b89771a01191b985fedd0be7cd893fcfef34732de25cdeefcbefef01
source-modified: 2026-05-22 14:40
compiled: 2026-05-22 14:46
---

This skill distills a brief (Slack note, ticket, email, stakeholder ask, backlog item) into 3–6 major goals and persists the confirmed list as `plan/<WI>/idea.md` paired with `plan/<WI>/status_idea.md`. It does not manage workflow phases, pick modes, emit or label issues, dispatch exploration subagents, decompose goals into tasks, write acceptance criteria, touch `CONTEXT.md` / ADRs / PRDs, or retire artifacts. Output is two file paths plus a status signal — nothing more.

## Hard Rules

1. **3–6 entries, strict.** Successful return has between 3 and 6 numbered entries inclusive. Negative goals count toward the budget when they materially shape the work. Under-budget → clear-incomplete; over-budget → block until the human merges or decomposes.
2. **No details in any goal.** Forbidden inside any goal body: module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices (library X, pattern Y), effort or timeline estimates. A goal names *what the work must serve*, not *how*.
3. **Negative goals are first-class.** Capture explicit non-goals as numbered entries prefixed exactly `Non-goal: ` (capital N, space after the colon).
4. **HITL only.** No AFK / loop execution. Agent proposes, human edits / accepts / rejects. No write without explicit human acceptance. Acknowledgement or silence is not acceptance.
5. **Brief is input, not output.** Even a well-written brief is restated as the 3–6 goal list. Do not pass the brief through verbatim.
6. **One sentence per goal. No nested bullets. No prose paragraphs.** Heading is literally `# Goals`.
7. **Single canonical path.** Artifact is exactly `plan/<WI>/idea.md` paired with `plan/<WI>/status_idea.md`. Never a shared `idea.md`, never multiple idea files under one `<WI>`, never any other location (no `idea/<topic>.md`, no `<WI>.md` at repo root).
8. **`owner-issue` mandatory** on `status_idea.md` frontmatter. Prompt the human at write-time. Accept `#TBD` only with an explicit warning that downstream merge-gate retirement enforcement will fail until replaced.
9. **No phase orchestration.** Do not name, invoke, route to, or hand off to other phases or skills. Do not pick or change a workflow mode. Do not search or create issues. Do not retire your own artifact.
10. **No silent collapse.** When the pre-structured-input heuristic fires, give the human an explicit choice between "treat as confirmed" and "full pass" — never silent quote-back-and-confirm.
11. **Strip-leak notes use exact format.** For each forbidden detail removed from a goal, append one line below the numbered list using exactly `Stripped detail: <item>`. No phase names in the line. Never write `deferred to <anywhere>` or any orchestration token.
12. **Forbidden phrasings.** Never emit anywhere in skill output, prompts, or return strings: `proceed to <phase>`, `deferred to <phase>`, `hand off to <phase>`, `feeds into <phase>`, `next phase`.
13. **Status file paired with artifact.** On failure runs (no `idea.md` written), do NOT create or modify `status_idea.md`. Status file never exists without a paired `idea.md`.

## Steps

1. **Pre-structured-input check.** Scan the brief for an already-shaped goal list (numbered list with 3–6 entries, no forbidden detail per Rule 2). If it fires, ask the human via an explicit choice: "Input already looks like a goal list: [render the detected list verbatim]. Treat as confirmed, or run full distillation pass?" If "treat as confirmed", carry the detected list into Step 5 unchanged. If "full pass", continue with Step 2. If the heuristic does not fire, continue silently.

2. **Distill candidate goals.** Read the brief end to end. Surface the small set of intents the work must serve — what would make it succeed or fail. Restate each as one sentence. Aim for 3–6. Mark non-goals with `Non-goal: ` prefix.

3. **Detail-leak strip.** Remove any forbidden detail (Rule 2) from each goal sentence. For every item stripped, append a line under the numbered list using exactly: `Stripped detail: <item>`. One line per stripped item.

4. **Count gate.**
   - **Under-budget** (fewer than 3 entries after strip): return `status: not_produced` with `reason: too narrow for goal-shaped framing — fewer than 3 distinct major goals identified`. Do not write any files. Do not name a downstream destination.
   - **Over-budget** (more than 6 entries): prompt the human to merge or decompose entries. Do not write until the count is between 3 and 6 inclusive.

5. **HITL accept.** Present the candidate list (numbered, with any `Non-goal:` and `Stripped detail:` lines) to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Treating acknowledgement or silence as acceptance is forbidden.

6. **Work-item slug + owner-issue prompts.** Derive a candidate `<WI>` slug from the brief (short, snake_case — e.g. `ai_mail`, `fix_crash_abc`, `add_oauth_provider`). Prompt: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Then prompt: "Owner issue (e.g. `#123`)?" — required. If the human has no number yet, accept the placeholder `#TBD` and warn explicitly that downstream merge-gate retirement enforcement will fail until the placeholder is replaced.

7. **Artifact write.** Create `plan/<WI>/` if missing. Write `plan/<WI>/idea.md` in this exact shape:

   ```markdown
   # Goals

   1. <goal sentence>
   2. <goal sentence>
   3. Non-goal: <explicit exclusion sentence>
   4. <goal sentence>

   Stripped detail: <item>
   Stripped detail: <item>
   ```

   Plain markdown — no YAML frontmatter. Heading literally `# Goals`. Numbering contiguous (1, 2, 3, …). `Non-goal: ` prefix exact. `Stripped detail:` lines (if any) live below the numbered list.

8. **Status file write.** Write `plan/<WI>/status_idea.md` with frontmatter only (body optional and ignored):

   ```markdown
   ---
   status: open | wip | done
   updated: <today YYYY-MM-DD>
   owner-issue: "#NNN"
   ---
   ```

   State machine:
   - (a) Refresh `updated:` to today on every run, regardless of whether `status:` changes.
   - (b) Default `status: wip` on a successful artifact write from `open` or first-write.
   - (c) Ask the human "mark done?" at the end of every successful run UNLESS the run is clear-incomplete (under-budget failure, human rejected, no acceptance reached) — in those cases skip the prompt. Flip to `done` only on explicit human yes. Never auto-flip.
   - (d) Preserve existing `done` unless the human explicitly reopens. On reopen, flip `done → wip` (never back to `open`).
   - (e) On failure runs (no `idea.md` written), do NOT create or modify `status_idea.md`.

9. **Return.**
   - **Success:** emit the written `plan/<WI>/idea.md` path, the written `plan/<WI>/status_idea.md` path, and a one-line summary: `status: ok` plus `goals: <N>` (count) plus `mode: <distilled|confirmed>` (full pass vs pre-structured shortcut).
   - **Failure** (under-budget, human rejected, no acceptance reached): emit `status: not_produced` plus the reason. No phase names anywhere in the failure string. None of the forbidden phrasings from Hard Rule 12.

## Return

On success:
```
plan/<WI>/idea.md
plan/<WI>/status_idea.md
status: ok | goals: <N> | mode: <distilled|confirmed>
```

On failure:
```
status: not_produced
reason: <short reason — no phase names, no forbidden phrasings>
```
