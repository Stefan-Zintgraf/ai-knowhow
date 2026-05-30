# Workflow Phases

Purpose: define the named phases used by `guardrails.md` (in the `Fires:` lines) and by `AI_Coding_Workflow.md`.

Each phase is backed by a concrete skill, command, or template. The agent is never given a vague phase command — the backing artifact defines the exact behavior. Skills may evolve over time; the phase name and intent stay stable.

---

## 1. Sequential Phases

### ide — Idea
Skills: distill-idea, triage-idea

Distill a raw brief, backlog item, or stakeholder ask into **3–6 major goals** that anchor the rest of the pipeline. No details (no module map, no APIs, no UX specifics, no acceptance criteria). Negative goals welcome. HITL only. Output feeds `aln` grilling; it does not replace it. Ephemeral — folded into the PRD's Goals section once `prd` lands; no in-tree artifact. Collapsible (3.29) when the upstream artifact already names goals explicitly.

### aln — Alignment
Skills: align-concept

Reach alignment / shared design concept between human and agent before any planning artifact exists. **Document-anchored** per Aln17 (Pocock's `/grill-with-docs`): reads `context.md` (the ubiquitous-language glossary, gr_domain_language.md L8) at session start via the `CLAUDE.md` pointer (L9), updates it in-session as terms emerge or shift, and drafts ADRs (`docs/adr/NNNN-<slug>.md` per gr_adr.md / 3.34) for any decision crossing the Adr1 threshold. Byproducts of `aln` therefore include: alignment transcript, module map (Aln12), `context.md` diffs, and zero or more new ADRs.

### res — Research (Optional)
Skills: do-research

Cache hard-to-recover external knowledge (third-party APIs, uncommon services, unfamiliar codebase regions) into a sprint-scoped `research/<topic>.md` so downstream agent runs don't re-explore from a fresh context window. Optional: only triggered when `aln` surfaces external-dependency unknowns the agent must answer with facts. Artifact is **deleted at sprint close** (see `gr/gr_res.md` Res3) — distinct from PRDs which move to external trackers.

### pro — Prototype (Optional)
Skills: prototype

Resolve a hard-to-reverse design decision by building 2–3 throwaway variants and letting the human pick. Optional: only triggered when grilling cannot resolve the decision in words AND the Pro1 gate holds (irreversibility OR cost asymmetry — wrong-choice cost >> 2–3 throwaway variants). Three flavors: FE/UX, architecture, integration (see `gr/gr_proto.md` Pro2). Entry from `aln` (design ambiguity) or `res` (build-to-learn spike). Sandbox code is **deleted before** production impl (Pro3). HITL by construction (Pro6).

### prd — Destination Doc
Skills: compose-prd

Summarize the alignment into a destination document — problem, solution, user stories, implementation decisions, testing decisions, **out-of-scope** items, proposed module map.

### iss — Issue Decomposition
Skills: prd-to-dag

Decompose the PRD into independently grabbable issues with explicit blocking edges and AFK/human-in-loop tags.

### ral — Ralph Loop (Single-Agent Implementation)
Skills: afk-loop

Sequential AFK implementation. Run a single agent that picks the next available issue, implements it via TDD, runs feedback loops, and commits.

### par — Parallel Loop
Skills: parallel-loop

Parallelize implementation across multiple agents.

### qa — Manual QA
Skills: qa

Human-driven check of a runnable slice. Reintroduces taste, product judgment, and real-world behavior verification after agent implementation. Mandatory checkpoint after `ral` / `par`. Findings are triaged by the human into either fix-now issues (loop back to `iss`) or backlog issues (slice still passes).

---

## 2. Cross-Phase Activities

These are not steps in the sequence. They may run alongside, between, or after any sequential phase.

### rev — Review
Skills: review

Have an agent review code — fresh context, in the smart zone, not the dumb zone.

### ica — Improve Codebase Architecture
Skills: arch-review

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

- **`direct-edit`** — `ide → ral → qa`. `<artifacts>/<slug>/` folder exists (minted by `/triage-idea`) but holds only `triage-decision.json` (audit); GH issue body is the work record. (Per [ADR-0001](docs/adr/0001-phase-bootstrap-sequence.md) — C6 relaxed for symmetric audit footprint.)
- **`mini`** — `ide → aln`(collapsed per Aln19) `→ ral → qa`. Issue + `<artifacts>/<slug>/idea.md` + collapsed `aln` artifacts.
- **`full`** — the diagram above.

Mode is recorded as a label on the GH issue (`mode:direct-edit` / `mode:mini` / `mode:full`) and may be changed mid-WI per Idea11.

`ide` produces 3–6 major goals from the raw brief. Collapses to a one-line confirmation when the upstream brief already names goals explicitly (per 3.29). For `mini`/`full`, the goal list is persisted as `<artifacts>/<slug>/idea.md` (per Idea7) — the WI anchor that downstream phases read; PRD Goals fold it but do not replace it, and the artifact retires with `<artifacts>/<slug>/` at WI close (3.33). For `direct-edit`, no `<artifacts>/<slug>/` is created — the GH issue body carries the brief.

`res` is optional and fires only when `aln` surfaces external-dependency unknowns (see `gr/gr_res.md` Apply When). `res` may also fire mid-`aln` if grilling cannot proceed without the facts.

`pro` is optional and fires only when grilling cannot resolve a design decision in words AND the Pro1 gate holds (irreversibility OR cost asymmetry — see `gr/gr_proto.md`). Entry from `aln` (design ambiguity) or `res` (build-to-learn spike). `pro` returns a chosen direction; rejected variants are recorded as Aln15 negative decisions.

`ral` and `par` are alternative modes of the same implementation step, chosen per task. Not both at once.

`qa` is mandatory after `ral` / `par`. Outcome routing is human-decided per finding: fix-now findings loop back to `iss`; backlog findings are filed but do not block.

---

## 5. Phase–Skill Binding

Each phase is backed by one or more skills. The `/phase` skill (A12) orchestrates transitions — no phase skill writes `phase_status.md` or `<artifacts>/ACTIVE` directly.

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
Skills: phase

A single orchestration skill owns all phase **state** (`phase_status.md` + `<artifacts>/ACTIVE`). Phase skills own their own **artifacts** (`idea.md`, ADRs, PRD, `research/*.md`, ...) but never touch state files. Design rationale and full contract list: [ADR-0001](docs/adr/0001-phase-bootstrap-sequence.md).

| Subcommand       | What it does                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| `/phase` or `/phase next` | **Default verb.** Reads `ACTIVE` + `phase_status.md`, computes `next_phase` against §4 chains, prints **full paste-ready command** for the next step. Also consumes any pending payload (`<artifacts>/.pending-bootstrap` + `<slug>/.pending-{triage,retriage}.json`) before computing. When `ACTIVE = <none>`, prints `"no active WI. run: /triage-idea"` and stops (two-command bootstrap — `/phase` never invokes other skills). |
| `/phase enter <code>` | **Recovery / jump escape hatch** (not the everyday verb). Guards entry: mode legal for this phase? Previous phase exited cleanly? Tripwire-halt clear? Writes `phase_status.md`. |
| `/phase exit <code>`  | Guards exit: phase-required artifacts present? HITL ack recorded? Updates `phase_status.md` history.          |
| `/phase status`       | Read-only. Same computation as `next`, without the consume step.                                              |

State file: `<artifacts>/<WI>/phase_status.md` (template: `tpl/tpl_phase_status.md`). Active-WI pointer: `<artifacts>/ACTIVE`. Internal skill-signature registry: one row per A-table skill (name + arg shape), used to format paste-ready commands.

### `ide` phase call sequence (all modes)

```
Bootstrap:
  1. /phase                          → "no active WI. run: /triage-idea"
  2. /triage-idea                    → HITL 4-axis pass. Mints <artifacts>/<slug>/.
                                       Writes <slug>/.pending-triage.json + <artifacts>/.pending-bootstrap.
                                       Prints: "now run: /phase"
  3. /phase                          → Consumes pending. Persists ACTIVE + phase_status.
                                       Moves pending → <slug>/triage-decision.json (audit).
                                       Prints next paste-ready command per mode:
                                         direct-edit → "run: /phase next"   (advances straight to ral)
                                         mini / full → "run: /distill-idea <slug>"

  4. (mini/full only) /distill-idea <slug>  → Writes <slug>/idea.md.
                                              Prints: "now run: /phase next"
  5. /phase next                            → ide → aln transition (mode chain continues).

Mid-WI re-triage (Idea11):
  /phase                       → "run: /triage-idea --remode <slug>"
  /triage-idea --remode <slug> → Writes <slug>/.pending-retriage.json.
  /phase                       → Consumes; moves to retriage-decision-<ts>.json.
```

Per [ADR-0001](docs/adr/0001-phase-bootstrap-sequence.md): `/phase enter ide` / `/phase exit ide` is **not used** for the standard bootstrap — the prior `enter ide → triage → exit ide` pattern had a chicken/egg guard problem (mode unknown until triage runs) and produced empty-phase ceremony for `direct-edit`.

### Belt-and-suspenders: B1 hook

B1 (`routing-step-enforcer`) warns if a phase skill ran but no `/phase` call followed in the same turn. Secondary enforcement — `/phase` is primary.

Full skill definitions, dependency edges, and build status: see `coding_plan.md` §"Phase Skills table".
