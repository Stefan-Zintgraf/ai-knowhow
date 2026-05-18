# Workflow Phases

Purpose: define the named phases used by `guardrails.md` (in the `Fires:` lines) and by `AI_Coding_Workflow.md`.

Each phase is backed by a concrete skill, command, or template. The agent is never given a vague phase command — the backing artifact defines the exact behavior. Skills may evolve over time; the phase name and intent stay stable.

---

## 1. Sequential Phases

### ide — Idea

Distill a raw brief, backlog item, or stakeholder ask into **3–6 major goals** that anchor the rest of the pipeline. No details (no module map, no APIs, no UX specifics, no acceptance criteria). Negative goals welcome. HITL only. Output feeds `aln` grilling; it does not replace it. Ephemeral — folded into the PRD's Goals section once `prd` lands; no in-tree artifact. Collapsible (3.29) when the upstream artifact already names goals explicitly.

### aln — Alignment

Reach alignment / shared design concept between human and agent before any planning artifact exists.

### res — Research (Optional)

Cache hard-to-recover external knowledge (third-party APIs, uncommon services, unfamiliar codebase regions) into a sprint-scoped `research/<topic>.md` so downstream agent runs don't re-explore from a fresh context window. Optional: only triggered when `aln` surfaces external-dependency unknowns the agent must answer with facts. Artifact is **deleted at sprint close** (see `gr/gr_research.md` Res3) — distinct from PRDs which move to external trackers.

### pro — Prototype (Optional)

Resolve a hard-to-reverse design decision by building 2–3 throwaway variants and letting the human pick. Optional: only triggered when grilling cannot resolve the decision in words AND the Pro1 gate holds (irreversibility OR cost asymmetry — wrong-choice cost >> 2–3 throwaway variants). Three flavors: FE/UX, architecture, integration (see `gr/gr_prototype.md` Pro2). Entry from `aln` (design ambiguity) or `res` (build-to-learn spike). Sandbox code is **deleted before** production impl (Pro3). HITL by construction (Pro6).

### prd — Destination Doc

Summarize the alignment into a destination document — problem, solution, user stories, implementation decisions, testing decisions, **out-of-scope** items, proposed module map.

### iss — Issue Decomposition

Decompose the PRD into independently grabbable issues with explicit blocking edges and AFK/human-in-loop tags.

### ral — Ralph Loop (Single-Agent Implementation)

Sequential AFK implementation. Run a single agent that picks the next available issue, implements it via TDD, runs feedback loops, and commits.

### par — Parallel Loop

Parallelize implementation across multiple agents.

### qa — Manual QA

Human-driven check of a runnable slice. Reintroduces taste, product judgment, and real-world behavior verification after agent implementation. Mandatory checkpoint after `ral` / `par`. Findings are triaged by the human into either fix-now issues (loop back to `iss`) or backlog issues (slice still passes).

---

## 2. Cross-Phase Activities

These are not steps in the sequence. They may run alongside, between, or after any sequential phase.

### rev — Review

Have an agent review code — fresh context, in the smart zone, not the dumb zone.

### ica — Improve Codebase Architecture

Scan the repo for opportunities to deepen modules / consolidate test boundaries.

---

## 3. Guardrail Bucket Mapping

`guardrails.md` uses a three-bucket model in the `Fires:` lines of each core rule: **Plan**, **Implement**, **Verify**. The mapping from phase to bucket:

| Phase | Bucket(s)                             |
| ----- | ------------------------------------- |
| ide   | Plan                                  |
| aln   | Plan                                  |
| res   | Plan                                  |
| pro   | Plan                                  |
| prd   | Plan                                  |
| iss   | Plan                                  |
| ral   | Implement                             |
| par   | Implement                             |
| qa    | Verify                                |
| rev   | Plan + Implement + Verify (all three) |
| ica   | Plan + Implement + Verify (all three) |

`rev` and `ica` deliberately span all buckets — a review or architecture pass can surface planning, implementation, or verification gaps. The agent must consider all buckets when operating in those phases.

---

## 4. Phase Sequence (Typical)

```
ide → aln → [res?] → [pro?] → prd → iss → (ral | par) → qa ─┬─ pass → done
              ▲        ▲                   ▲                 │
              │        │                   └─ fix-now ◄──────┘
              │        │                   └─ backlog ─ done (issue filed for later)
              │        │                                     ^
              │        │                                     └── rev and ica may run at any point
              │        └─ may also be invoked from res (build-to-learn spike)
              └─ may also fire mid-aln when grilling stalls on facts
```

`ide` produces 3–6 major goals from the raw brief. Collapses to a one-line confirmation when the upstream brief already names goals explicitly (per 3.29). Output is folded into the PRD's Goals section; no in-tree artifact survives.

`res` is optional and fires only when `aln` surfaces external-dependency unknowns (see `gr/gr_research.md` Apply When). `res` may also fire mid-`aln` if grilling cannot proceed without the facts.

`pro` is optional and fires only when grilling cannot resolve a design decision in words AND the Pro1 gate holds (irreversibility OR cost asymmetry — see `gr/gr_prototype.md`). Entry from `aln` (design ambiguity) or `res` (build-to-learn spike). `pro` returns a chosen direction; rejected variants are recorded as Aln15 negative decisions.

`ral` and `par` are alternative modes of the same implementation step, chosen per task. Not both at once.

`qa` is mandatory after `ral` / `par`. Outcome routing is human-decided per finding: fix-now findings loop back to `iss`; backlog findings are filed but do not block.
