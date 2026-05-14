# Workflow Phases

Purpose: define the named phases used by `guardrails.md` (in the `Fires:` lines) and by `AI_Coding_Workflow.md`.

Each phase is backed by a concrete skill, command, or template. The agent is never given a vague phase command — the backing artifact defines the exact behavior. Skills may evolve over time; the phase name and intent stay stable.

---

## 1. Sequential Phases

### aln — Alignment

Reach alignment / shared design concept between human and agent before any planning artifact exists.

### prd — Destination Doc

Summarize the alignment into a destination document — problem, solution, user stories, implementation decisions, testing decisions, **out-of-scope** items, proposed module map.

### iss — Issue Decomposition

Decompose the PRD into independently grabbable issues with explicit blocking edges and AFK/human-in-loop tags.

### ral — Ralph Loop (Single-Agent Implementation)

Sequential AFK implementation. Run a single agent that picks the next available issue, implements it via TDD, runs feedback loops, and commits.

### par — Parallel Loop

Parallelize implementation across multiple agents.

---

## 2. Cross-Phase Activities

These are not steps in the sequence. They may run alongside, between, or after any sequential phase.

### rev — Review

Have an agent review code — fresh context, in the smart zone, not the dumb zone.

### ica — Improve Codebase Architecture

Scan the repo for opportunities to deepen modules / consolidate test boundaries.

---

## 3. Guardrail Bucket Mapping

`guardrails.md` uses a three-bucket model in the `Fires:` lines of each always-on rule: **Plan**, **Implement**, **Verify**. The mapping from phase to bucket:

| Phase | Bucket(s)                             |
| ----- | ------------------------------------- |
| aln   | Plan                                  |
| prd   | Plan                                  |
| iss   | Plan                                  |
| ral   | Implement                             |
| par   | Implement                             |
| rev   | Plan + Implement + Verify (all three) |
| ica   | Plan + Implement + Verify (all three) |

`rev` and `ica` deliberately span all buckets — a review or architecture pass can surface planning, implementation, or verification gaps. The agent must consider all buckets when operating in those phases.

---

## 4. Phase Sequence (Typical)

```
aln → prd → iss → (ral | par) → done
                                    ^
                                    └── rev and ica may run at any point
```

`ral` and `par` are alternative modes of the same implementation step, chosen per task. Not both at once.

---

## 5. Skill Backing

Each phase has (or will have) a backing skill or template that defines its exact behavior:

| Phase | Backing artifact                                       |
| ----- | ------------------------------------------------------ |
| aln   | (skill TBD)                                            |
| prd   | `skills/engineering/to-prd/SKILL.md` (may be replaced) |
| iss   | (skill TBD)                                            |
| ral   | (skill TBD)                                            |
| par   | (skill TBD)                                            |
| rev   | (skill TBD)                                            |
| ica   | (skill TBD)                                            |

The agent always operates inside a named phase with a backing artifact. It does not receive vague phase commands.
