# Guardrail: Architectural Decision Records (ADRs)

Purpose: capture the *why* of non-obvious, hard-to-reverse, tradeoff-heavy decisions in durable in-tree records so future agents and humans don't relitigate them.

Scope: applies whenever a decision crossing the Adr1 threshold is made — typically during `aln`, `prd`, `rev`, or `ica`. ADRs may also be authored retroactively when `rev` surfaces an undocumented surprise.

Origin: Pocock — "language sharpening does not capture every important decision" (transcripts `i-stopped-using-grill-me-for-coding-heres-what-i-use-instead_*.md`). ADRs are the second documentation layer next to `context.md` (gr_domain_language.md). Nygard's lightweight ADR format is the canonical shape.

---

## Apply When

- A design decision is made that is **hard to reverse** AND **would be surprising without context** AND is the **result of a real tradeoff** with downstream consequences.
- Grilling (`aln`) produces such a decision and the rationale would be lost if not captured.
- Review (`rev`) surfaces a surprising choice in the diff whose rationale is not in the diff itself, the PRD, or `context.md`.
- An architecture pass (`ica`) consolidates or splits modules in a way that is non-obvious to a future reader.

---

## Rules

### Adr1. Three-Part Threshold

Write an ADR only when **all three** hold:

1. **Hard to reverse** — undoing the decision requires migration, breaking-change, or significant rework.
2. **Surprising without context** — a future reader (human or agent) would ask "why was this done this way?" and not find the answer in code or `context.md`.
3. **Real tradeoff** — alternatives were considered and have non-trivial consequences.

If any one fails, do not write an ADR. Interchangeable choices, easily-reversible refactors, and routine style choices are out of scope. ADR noise dilutes signal.

### Adr2. ADRs Are Durable, In-Tree

ADRs live at `docs/adr/NNNN-<kebab-slug>.md` where `NNNN` is a zero-padded monotonic integer (`0001`, `0002`, …). They are **not retired** like PRDs (3.24) or research files (3.27). An ADR persists as long as the decision it documents is in force; it is **superseded** by a later ADR, never deleted silently.

### Adr3. ADRs Are Distinct From Aln15 Negative Decisions

Aln15 captures rejected options (the road not taken) inside the alignment transcript. An ADR captures the *chosen* non-obvious decision and its rationale, in a separately discoverable file. The two are complementary, not interchangeable. A single decision may produce both (a chosen variant ADR + several rejected-variant Aln15 entries).

### Adr4. ADRs Are Distinct From the PRD

The PRD summarizes alignment (Aln13). It states the chosen solution. The ADR explains *why* a specific surprising choice was made — typically a sub-decision inside the PRD scope that a casual reader of the PRD would not understand from the PRD alone. PRDs retire externally; ADRs stay.

### Adr5. Required Sections

Every ADR has, in order:

1. **Title** — `# NNNN. <one-line summary>`.
2. **Status** — `proposed` | `accepted` | `superseded by NNNN` | `deprecated`.
3. **Context** — what forces are in play, what constraint led to needing this decision.
4. **Decision** — the chosen direction, stated imperatively.
5. **Consequences** — what becomes easier, harder, or impossible because of this decision; observable downstream effects.
6. **Alternatives Considered** — at least one rejected alternative with a one-line reason it lost. Without this, the tradeoff claim (Adr1.3) is unverifiable.

Optional sections: `Date`, `Related ADRs`, `Related Aln15 entries`, `References`.

### Adr6. Author at Decision Time, Not Retroactively (When Possible)

Prefer drafting the ADR in the same session the decision is made (typically `aln` per Aln17). Retroactive ADRs authored in `rev` are allowed and important — but in-session capture is higher fidelity.

### Adr7. Supersede, Don't Mutate

When a decision is reversed or replaced, the original ADR's `Status` flips to `superseded by NNNN` and a new ADR is written referencing it. The original body is not edited (other than the status line). This preserves the historical trail.

### Adr8. Agent May Draft, Human Must Accept

ADRs are HITL artifacts. The agent drafts (in `aln` per Aln17, or in `rev` when surfacing a gap) and presents to the human. Status flips from `proposed` → `accepted` only on explicit human acceptance. Silent commits of `accepted` ADRs are forbidden.

### Adr9. ADRs Are a Pull-Source for Implementation

When `ral`/`par` touches code that an ADR governs, the implementer pulls the ADR into context (per 3.17 / Op14b). Routing (§5 of guardrails.md) should surface the ADR when its topic matches the task. ADR filenames carry the slug so grep is reliable.

### Adr10. Review Verifies ADR Coverage

`rev` (gr_rev.md) checks: did any decision in the diff cross the Adr1 threshold without an ADR? If yes, the reviewer flags it and either drafts the missing ADR or routes back to `aln`.

---

## Anti-Patterns

- Writing an ADR for an interchangeable choice ("we picked library X over equally good Y").
- Editing an existing ADR's body after `accepted`. (Use supersession instead — Adr7.)
- Treating an ADR as the source of *what* was decided (that's the PRD's job — Adr4) instead of *why*.
- Capturing a rejected option in an ADR. (Rejected options live in Aln15 — Adr3.)
- Letting an ADR document creep into a design doc. ADRs are short — typically under one page.
- Numbering by date (`2026-05-21-foo.md`) instead of monotonic integer. Date numbering breaks Adr7 supersession chains and re-introduces ordering ambiguity when two ADRs land the same day.
- Drafting an ADR without an `Alternatives Considered` section — the tradeoff claim becomes unverifiable.

---

## Notes on Interaction with Other Guardrails

- **3.34 / 4.20** — core-rule mirror and routing entry.
- **Aln17 (gr_algn.md)** — `align-concept` proposes ADRs in-session during grilling.
- **Aln15 (gr_algn.md)** — captures rejected options; complementary to ADRs (Adr3).
- **Aln13 (gr_algn.md)** — PRD summarizes alignment; ADRs explain non-obvious sub-decisions (Adr4).
- **3.24 (PRD retirement)** — PRDs retire externally; ADRs stay (Adr2).
- **3.27 (research retirement)** — research retires on owner-issue close; ADRs stay (Adr2).
- **3.17 / Op14b** — ADRs are pulled by implementer when relevant (Adr9).
- **Rev (gr_rev.md)** — review verifies ADR coverage (Adr10).
- **gr_domain_language.md** — `context.md` (the ubiquitous-language glossary) is the *first* documentation layer; ADRs are the *second*. Together they form the durable in-tree knowledge surface that `/grill-with-docs` reads and updates.

---

## Pulling This Document

Pull this document when:

1. A grilling session (`aln`) produces a decision that smells non-obvious.
2. A review (`rev`) sees a surprising choice with no ADR cited.
3. An architecture pass (`ica`) makes a consolidation/split decision.
4. Authoring or compiling A1 (`align-concept`) — Aln17 wiring needs this doc's threshold and format.
