# Workflow Phases

Purpose: define the named phases used by `guardrails.md` (in the `Fires:` lines) and by `AI_Coding_Workflow.md`.

Each phase is backed by a concrete skill, command, or template. The agent is never given a vague phase command — the backing artifact defines the exact behavior. Skills may evolve over time; the phase name and intent stay stable.

---

## 1. Sequential Phases

### ide — Idea

Distill a raw brief, backlog item, or stakeholder ask into **3–6 major goals** that anchor the rest of the pipeline. No details (no module map, no APIs, no UX specifics, no acceptance criteria). Negative goals welcome. HITL only. Output feeds `aln` grilling; it does not replace it. Ephemeral — folded into the PRD's Goals section once `prd` lands; no in-tree artifact. Collapsible (3.29) when the upstream artifact already names goals explicitly.

### aln — Alignment

Reach alignment / shared design concept between human and agent before any planning artifact exists. **Document-anchored** per Aln17 (Pocock's `/grill-with-docs`): reads `context.md` (the ubiquitous-language glossary, gr_domain_language.md L8) at session start via the `CLAUDE.md` pointer (L9), updates it in-session as terms emerge or shift, and drafts ADRs (`docs/adr/NNNN-<slug>.md` per gr_adr.md / 3.34) for any decision crossing the Adr1 threshold. Byproducts of `aln` therefore include: alignment transcript, module map (Aln12), `context.md` diffs, and zero or more new ADRs.

### res — Research (Optional)

Cache hard-to-recover external knowledge (third-party APIs, uncommon services, unfamiliar codebase regions) into a sprint-scoped `research/<topic>.md` so downstream agent runs don't re-explore from a fresh context window. Optional: only triggered when `aln` surfaces external-dependency unknowns the agent must answer with facts. Artifact is **deleted at sprint close** (see `gr/gr_res.md` Res3) — distinct from PRDs which move to external trackers.

### pro — Prototype (Optional)

Resolve a hard-to-reverse design decision by building 2–3 throwaway variants and letting the human pick. Optional: only triggered when grilling cannot resolve the decision in words AND the Pro1 gate holds (irreversibility OR cost asymmetry — wrong-choice cost >> 2–3 throwaway variants). Three flavors: FE/UX, architecture, integration (see `gr/gr_proto.md` Pro2). Entry from `aln` (design ambiguity) or `res` (build-to-learn spike). Sandbox code is **deleted before** production impl (Pro3). HITL by construction (Pro6).

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

> The diagram below shows `full` mode. `direct-edit` and `mini` collapse
> parts of the chain — see [gr_idea.md](gr/gr_idea.md) Idea8 for the
> triage matrix and per-mode chain shape. A summary follows the diagram.

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

### Modes

`ide` triages every entering task into one of three modes (per Idea8):

- **`direct-edit`** — `ide → ral → qa`. No `plan/<N>_<slug>/` folder; issue body is the record.
- **`mini`** — `ide → aln`(collapsed per Aln19) `→ ral → qa`. Issue + `plan/<N>_<slug>/idea.md` + collapsed `aln` artifacts.
- **`full`** — the diagram above.

Mode is recorded as a label on the GH issue (`mode:direct-edit` / `mode:mini` / `mode:full`) and may be changed mid-WI per Idea11.

`ide` produces 3–6 major goals from the raw brief. Collapses to a one-line confirmation when the upstream brief already names goals explicitly (per 3.29). For `mini`/`full`, the goal list is persisted as `plan/<N>_<slug>/idea.md` (per Idea7) — the WI anchor that downstream phases read; PRD Goals fold it but do not replace it, and the artifact retires with `plan/<N>_<slug>/` at WI close (3.33). For `direct-edit`, no `plan/<N>_<slug>/` is created — the GH issue body carries the brief.

`res` is optional and fires only when `aln` surfaces external-dependency unknowns (see `gr/gr_res.md` Apply When). `res` may also fire mid-`aln` if grilling cannot proceed without the facts.

`pro` is optional and fires only when grilling cannot resolve a design decision in words AND the Pro1 gate holds (irreversibility OR cost asymmetry — see `gr/gr_proto.md`). Entry from `aln` (design ambiguity) or `res` (build-to-learn spike). `pro` returns a chosen direction; rejected variants are recorded as Aln15 negative decisions.

`ral` and `par` are alternative modes of the same implementation step, chosen per task. Not both at once.

`qa` is mandatory after `ral` / `par`. Outcome routing is human-decided per finding: fix-now findings loop back to `iss`; backlog findings are filed but do not block.

---

## 5. Phase–Skill Binding

Each phase is backed by one or more skills. The `/phase` skill (A12) orchestrates transitions — no phase skill writes `phase_status.md` or `plan/ACTIVE` directly.

### Skill map

| Phase | Primary skill(s)                          | Guardrail source                     | Notes                                                                 |
| ----- | ----------------------------------------- | ------------------------------------ | --------------------------------------------------------------------- |
| `ide` | `/triage-idea` (A13) + `/distill-idea` (A11) | [gr_idea.md](gr/gr_idea.md)         | Triage (Idea8–11) runs first; distillation (Idea1–5,7,12) follows for `mini`/`full` only |
| `aln` | `/align-concept` (A1)                     | [gr_algn.md](gr/gr_algn.md)         | Collapsed per Aln19 in `mini` mode                                    |
| `res` | `/do-research` (A10)                      | [gr_res.md](gr/gr_res.md)           | Optional — fires when `aln` surfaces external unknowns                |
| `pro` | `/prototype` (A9)                         | [gr_proto.md](gr/gr_proto.md)       | Optional — Pro1 gate (irreversibility or cost asymmetry)              |
| `prd` | `/compose-prd` (A2)                       | [gr_algn.md](gr/gr_algn.md)         |                                                                       |
| `iss` | `/prd-to-dag` (A3)                        | [gr_tdd.md](gr/gr_tdd.md)           |                                                                       |
| `ral` | `/afk-loop` (A4)                          | [gr_tdd.md](gr/gr_tdd.md)           |                                                                       |
| `par` | `/parallel-loop` (A5)                     | —                                    | Blocked — substrate TBD                                               |
| `qa`  | `/qa` (A8)                                | [gr_qa.md](gr/gr_qa.md)             |                                                                       |
| `rev` | `/review` (A6)                            | [gr_rev.md](gr/gr_rev.md)           | Cross-phase — may run alongside any sequential phase                  |
| `ica` | `/arch-review` (A7)                       | [gr_mod.md](gr/gr_mod.md)           | Cross-phase — may run alongside any sequential phase                  |

### Transition protocol: `/phase` (A12)

A single orchestration skill owns all phase state. Phase skills never write `phase_status.md` or `plan/ACTIVE` directly.

| Subcommand       | What it does                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| `/phase enter <code>` | Guards entry: mode legal for this phase? Previous phase exited cleanly? Tripwire-halt clear? Writes `phase_status.md`. |
| `/phase exit <code>`  | Guards exit: phase-required artifacts present? HITL ack recorded? Updates `phase_status.md` history.          |
| `/phase status`       | Read-only. Computes `next_phase` from `mode` + `current_phase` + flags (`needs_research`, `pro_gate_tripped`) against §4 chains. |

State file: `plan/<WI>/phase_status.md` (template: `tpl/tpl_phase_status.md`). Active-WI pointer: `plan/ACTIVE`.

### `ide` phase call sequence by mode

```
direct-edit:  /phase enter ide → /triage-idea →                     /phase exit ide
mini / full:  /phase enter ide → /triage-idea → /distill-idea →     /phase exit ide
mid-WI re-triage (Idea11):  /triage-idea --remode  (standalone, no phase enter/exit)
```

### Belt-and-suspenders: B1 hook

B1 (`routing-step-enforcer`) warns if a phase skill ran but no `/phase` call followed in the same turn. Secondary enforcement — `/phase` is primary.

Full skill definitions, dependency edges, and build status: see `coding_plan.md` §"Phase Skills table".
