# Guardrail: Research

Purpose: cache hard-to-recover external knowledge (third-party APIs, uncommon services, unfamiliar codebase regions) into a sprint-scoped artifact so downstream agent runs don't re-explore from a fresh context window each time — and retire the artifact before it rots.

Source: Pocock 7-phases workflow, phase 2 (Research). See [the-7-phases-of-ai-driven-development.md](../the-7-phases-of-ai-driven-development.md) §"Research Caching".

---

## Apply When

- Work touches an external API, SDK, or service whose surface the agent cannot infer (Stripe-style, uncommon protocols, internal services without local types).
- Codebase region is large or unfamiliar enough that re-exploration on every agent run is wasteful.
- Alignment (`aln`) surfaces unknowns the agent must answer with facts before a PRD can be written.
- Skip when: target is a well-known library the agent already handles fluently, or the task is small enough that re-exploration cost is below caching cost.

---

## Rules

### Res1. Research Is Sprint-Scoped

Research artifacts exist only for the duration of the sprint / feature they serve. They are not long-lived documentation. Their job ends when the feature ships.

### Res2. Cache in a Known Location

Research lives at `research/<topic>.md` (or `research.md` for a single-topic sprint) in the repo working tree. Agents read it; humans skim it. One canonical path so downstream skills can find it without guessing.

### Res3. Retire at Sprint Close (Prevent Rot)

When the feature ships (or sprint closes), the research file is **deleted** in the same PR that closes the work. Stale research actively misleads future agent runs because it looks authoritative but reflects yesterday's API or yesterday's codebase. Parallel to Doc11 (PRD retirement) but distinct: PRDs move to external trackers, research files are deleted outright.

Trigger: the `owner-issue` (Res4) closes. The PR that closes that issue must delete the file. `qa` verifies in Q11 before merge; pre-commit lint rejects research files missing the `owner-issue` field (so no orphan can be authored). No GitHub Action, no webhook — the gate is human + lint, and `qa` is mandatory before merge anyway.

### Res4. Mark Provenance, Date, and Owner Issue

Each research file opens with a header containing:

- `owner-issue: #NNN` — the **PRD / feature epic issue** the research serves. Exactly one. Decomposed sub-tickets that cite the research do not own it; the epic owns it (it naturally closes last). No file on disk without this field. Pre-PRD exploratory research is forbidden — create the epic stub first (one click) and reference it.
- Source URLs.
- Date the research was performed.
- Agent / human who produced it.

A reader (human or agent) can then judge staleness at a glance and a lint can verify owner provenance mechanically.

### Res5. Facts Over Speculation

Research captures **observed facts** — API responses, schema shapes, error codes, code locations, function signatures actually present in the source. Speculation, recommended approaches, or design opinions belong in the PRD, not in research. This keeps research stable across alignment iterations.

### Res6. No Fabrication

Op13 applies in full. A research file that invents API endpoints, config keys, or symbols is worse than no research file — it launders fabrication into "verified context." If a fact cannot be confirmed against a primary source (docs, code, response capture), it is flagged as an open question, not stated.

### Res7. Reference, Don't Duplicate

If authoritative docs exist (OpenAPI spec, generated types, schema files), the research file links to them rather than copying. Copies drift; links don't.

### Res8. Scope Tight

Research covers only what the current sprint needs. A "while I'm here, let me document the whole API" pass produces a sprawling file that rots faster and obscures the relevant subset. One topic per file; one sprint per file.

### Res9. Subagent for Exploration

Research is typically gathered by a subagent (see B10) with an isolated context window, returning a summary the main agent persists. Caller's context stays clean; expensive exploration happens once.

### Res10a. Cross-Feature Reuse: Copy Facts, Don't Share Files

If a different feature needs facts from an existing (or already-retired) research file, **copy the relevant facts** into the new feature's `research/<topic>.md` under its own `owner-issue`. Do not share-own a single file across features, do not symlink, do not resurrect a deleted file. Each act of copying forces the writer to ask "is this fact still true today?" — which is the entire point of sprint-scoping. Facts durable enough to outlive multiple features belong in code comments, ADRs (Doc8), or generated docs (Doc5), not in `research/`.

### Res10. Invoke `pro` for Build-to-Learn Facts

When a research question can only be answered by building (e.g., the actual shape of a third-party webhook payload, real latency of an integration under realistic load, observed behavior of a rate limiter), `res` invokes phase `pro` instead of speculating. The integration-flavor variant (gr_prototype.md Pro2) hits the real or vendor-sandbox service and captures observed responses; the captured facts then flow back into the research file. Distinction: `res` decides "we need facts"; `pro` is one tool `res` uses when only a spike produces those facts. Spike code itself is throwaway (Pro3) and does not survive into the research file — only the captured facts do.

---

## Anti-Patterns

- Keeping `research.md` in the repo after the feature ships ("might be useful later").
- Treating research as canonical documentation — it isn't; it's a context-window cache.
- Writing speculative design discussion into research instead of into the PRD.
- One giant `research.md` accumulating multiple sprints' findings.
- Research files without dates or source links — staleness becomes invisible.
- Research files without an `owner-issue` field, or with `owner-issue: TBD` — orphan files survive merges and rot silently.
- Sharing one research file across multiple feature epics (multi-owner) — when one feature ships, retirement either deletes facts the other still needs or leaves the file stranded forever.
- Resurrecting a deleted research file for a new feature instead of copying the still-true facts into a fresh one.
- Fabricated endpoints or "probable" config keys presented as facts.
- Re-exploring the same external API on every Ralph loop iteration because no cache exists.

---

## Pulling This Document

Pulled when:

1. Phase `res` is entered.
2. `aln` grilling surfaces an external-dependency unknown and the agent considers whether to spin up a research pass.
3. Review (`rev`) of work that consumed a `research.md` — reviewer verifies Res5/Res6 (facts vs. fabrication) against the diff.

Not pulled for: normal implementation work where research already exists or is unnecessary.
