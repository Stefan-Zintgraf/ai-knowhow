# Authoring Prompt: `distill-idea` Skill (A11)

## Metadata

```yaml
skill_id: A11
skill_name: distill-idea
phase: ide
status: todo
workflow_ref: W15
depends_on: []
feeds_into: [A1]  # A1 grill-me consumes the goal list as grilling target
```

## Scope

Distill a raw brief, backlog item, Slack note, ticket, or vague stakeholder ask into a list of **3–6 major goals** that will anchor downstream `aln` grilling.

Does NOT:

- Produce module map, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or effort estimates (those belong to `aln` / `prd` / `iss`).
- Write any file to the working tree (output is ephemeral per Idea7).
- Run any grilling, research, or design step itself — it only frames goals.
- Decide whether to invoke `ide` at all, or what phase comes next (that is the caller's / phase-orchestration concern).
- Run AFK / Ralph-loop / autonomous mode — HITL only by construction.

## Self-Containment Mandate

The compiled runtime skill MUST run with only its own file in context — no source-document lookups. Every Hard Rule, behavior step, forbidden-token list, and collapse-mode trigger from the sources below MUST be inlined verbatim into the compiled skill. The compiled skill must not contain "see gr/gr_idea.md" / "see guardrails.md" / "per §3.32" references. Source docs are author-time scaffolding only.

## Source Documents (author-time only)

| File            | Relevant sections                                |
| --------------- | ------------------------------------------------ |
| `gr/gr_idea.md` | Apply When; Idea1–Idea7; Anti-Patterns; Notes    |
| `phases.md`     | §1 `ide — Idea`; §4 sequence diagram (ide → aln) |
| `guardrails.md` | §3.32 (idea); §4.19 (routing); §3.29 (collapse)  |

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. Output is a list of **between 3 and 6 major goals** — never fewer than 3, never more than 6.
2. Fewer than 3 candidate goals → the brief is too narrow for goal framing; report that the work should go directly to `aln` with the raw brief and stop.
3. More than 6 candidate goals → decompose or merge before presenting; do not present a >6 list and ask the human to trim.
4. Each goal names *what the work must serve*, never *how*.
5. Forbidden in goal text: module names, file paths, API shapes, UX specifics (screens, components, layouts), acceptance criteria, tech choices (library X, pattern Y), effort or timeline estimates.
6. If a detail leaks from the brief, strip it from the goal and note it once as "deferred to aln/prd" — do not silently retain.
7. Explicit non-goals (negative goals) are first-class and count toward the 3–6 budget when they materially shape the work.
8. HITL only. The skill proposes; the human edits, accepts, or rejects. Never finalize without explicit human acceptance.
9. The original brief is **input**, not output. Even a well-written brief gets restated as a 3–6 goal list — the act of distilling surfaces missing goals and unstated assumptions.
10. The goal list is the *starter* for downstream grilling, not a substitute. Do not produce design content, PRD content, issue content, or any artifact beyond the goal list itself.
11. The goal list is **ephemeral**. Do not write `idea/<topic>.md`, `plan/<WI>/idea.md`, or any other in-tree file. Output is conversational only.
12. **Collapse mode.** If the upstream artifact (memo, ticket body, PRD draft) already names 3–6 explicit goals, do NOT run a full distillation pass. Quote the existing goals back in a one-line confirmation, ask the human to accept or amend, and stop.

## Skill Behaviors

1. Read the raw brief (provided inline, pasted, or referenced by the human).
2. **Collapse check.** Scan the brief for an explicit goal list of 3–6 items. If found: quote them back verbatim, ask the human to confirm/amend in one turn, stop on acceptance. Skip steps 3–7.
3. **Distill.** Read the brief and identify the small set of intents (positive + negative) the work must serve. Strip every implementation detail per Rule 5; for each stripped detail, hold it for the closing "deferred to aln/prd" note.
4. **Size.** If candidates < 3, report "too narrow for goal framing; proceed to `aln` with the brief directly" and stop. If candidates > 6, merge / decompose internally to land in [3, 6] before presenting.
5. **Present.** Show the proposed 3–6 goal list to the human, with each goal one sentence, no nested bullets, no detail. Mark negative goals explicitly (e.g. "Non-goal: …"). Append the one-line "deferred to aln/prd" note if any details were stripped.
6. **HITL.** Wait for explicit human accept / edit / reject. Iterate on edits. Do not assume silence = acceptance.
7. **Return.** On accept, emit the final goal list as the skill's return value (conversational text). Do not write any file. Do not invoke `aln` or any other phase — return control to the caller.

## Constraints (must appear as Hard Rules inside the skill)

- MUST produce between 3 and 6 goals, inclusive.
- MUST NOT include module names, file paths, API shapes, UX specifics, acceptance criteria, tech choices, or effort/timeline estimates in any goal.
- MUST treat the brief as input, not output — restate even when the brief reads well.
- MUST surface negative goals as first-class entries when they materially shape the work.
- MUST be HITL — no AFK, no Ralph loop, no autonomous acceptance.
- MUST NOT write any file in the working tree — output is conversational only.
- MUST detect the collapse case (existing 3–6 explicit goals in upstream artifact) and short-circuit to a one-line confirmation.
- MUST stop and report "proceed to `aln` directly with the brief" when fewer than 3 goal candidates are found — do not pad.
- MUST NOT produce design, PRD, issue, or research content; MUST NOT invoke or recommend a next phase beyond returning the goal list.

## Output Format (for the generated skill)

The compiled runtime skill MUST contain, in order:

1. A one-paragraph role statement naming the skill, the phase (`ide`), and the single deliverable (3–6 major goals; ephemeral; HITL).
2. A `## Hard Rules` block enumerating every constraint above as imperative statements, with no references to external documents.
3. A `## Steps` section mirroring the Skill Behaviors above (collapse check first, then distill / size / present / HITL / return).
4. A `## Return` section specifying the conversational return shape: a numbered list of goals (with negatives marked), optionally followed by the single "deferred to aln/prd" line.

Forbidden tokens in the compiled skill (must not appear anywhere in its body): `see gr/`, `see guardrails.md`, `per §`, `idea/<topic>.md`, `plan/`, `status_idea.md`, `AFK`, `ralph`, any reference to writing a file.

No planning-artifact outputs — this skill produces no `plan/<WI>/<artifact>.md`, no `status_<artifact>.md`, no `open`/`wip`/`done` state machine. The goal list lives only in the conversation and is consumed by the caller (typically `grill-me` / A1) which folds it later into the PRD.
