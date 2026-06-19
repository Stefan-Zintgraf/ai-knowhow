# Plan — Producing an AI-Friendly Version of a Foundation Vision

> **What this is.** A plan for converting a finalized `*-foundation-vision.md`
> (the human, divergent, flat-list artifact this skill produces) into an
> **AI-friendly companion set** that a downstream agent can use to generate
> architecture, requirements, and an implementation plan with minimal
> misreading.
>
> **Pilot document:** [ai-mail-foundation-vision.md](../../../ai-mail/ai-mail.pocock/docs/brainstorming/ai-mail-foundation-vision.md)
> (1 press-release vision + 67 use-cases). The plan is written to generalize to
> any vision this skill emits.
>
> Created: 2026-06-19.

---

## 1. The problem we are solving

The vision artifact is deliberately optimized for a **human** reader: narrative,
emotional, one running flat list, plain language, no structure. That is correct
for what it is — but it is *not* what a build-phase agent wants. The friction is
**structural, not length**:

1. **Cross-cutting invariants are restated dozens of times** instead of once.
   In the pilot, nearly every UC re-asserts the same load-bearing constraints:
   *nothing sent/deleted without my nod* (human-in-the-loop), *never deletes —
   only sets aside* (non-destructive), *shows its reasoning* (explainability /
   audit), *what it learns stays mine* (privacy / ownership), *earns trust step
   by step* (progressive autonomy), *holds & is overridable* (reversibility),
   *knows it's all one person* (identity resolution). To an agent this is both
   the most important signal **and** repetition that invites inconsistent
   re-derivation.
2. **No clustering.** The pilot's 67 flat UCs collapse to ~12 underlying
   capabilities. The agent has to do that clustering itself, possibly
   differently each run.
3. **No ubiquitous language.** The same entity is named many ways ("the quiet
   read-only corner", "set aside", "for-your-information"). The agent needs one
   term per concept.
4. **No traceability spine.** Stable IDs exist (`UC1…`, `BV1…`) but nothing maps
   them to actors, capabilities, or the invariants they depend on.

## 2. Design principles (the non-negotiables)

- **Do not compress the vision.** Keep the source artifact intact and canonical
  — it is the record of *intent and priority*, and its emotional framing is the
  cheap insurance that stops an agent making locally-clever, globally-wrong
  tradeoffs. Token count is not the bottleneck; structure is.
- **Derive, don't replace.** The AI-friendly version is a *companion set* built
  *from* the vision, never an edit of it. The vision stays the single source of
  truth; derived docs cite back to it by UC ID.
- **Split by pipeline role, not by feature.** Each derived doc owns exactly one
  concern (invariants / language / capabilities / actors / traceability).
  Splitting doesn't reduce total tokens — it enables **selective loading**: an
  architecture agent pulls invariants + capability map + glossary; a
  requirements agent for one capability pulls that cluster + invariants. That is
  the real win and the shape a multi-agent pipeline wants.
- **Legitimate compression happens once, in the right place.** The only place we
  shorten anything is the *normalized* one-line restatement of each UC in the
  traceability index — and only by factoring out the repeated invariant
  boilerplate into invariant references. The rich original sentence stays
  untouched in the vision.
- **Bidirectional traceability or it didn't happen.** Every derived claim points
  back to the UC(s) it came from; every UC points forward to its capability and
  invariants. No orphans on either side.

## 3. Target artifact set

**Locked (2026-06-19):** the companion set lives **parallel to the vision** in the
product repo's `docs/brainstorming/`, in a tidy subfolder
(`ai-mail-vision-ai-spec/`). Markdown-first — no machine layer yet. Executed as a
**one-off pilot** for the ai-mail vision; skill-ization is a later decision.

| File | Concern | Key contents |
|------|---------|--------------|
| `README.md` | Map + load order | What each file is, which to load for which downstream task |
| `invariants.md` | Cross-cutting constraints, stated **once** | `INV1…` — statement, rationale, the UCs that assert it |
| `glossary.md` | Ubiquitous language | Canonical entity/term per concept + the vision's synonyms it replaces |
| `capability-map.md` | UC clusters → capabilities | `CAP1…` — name, intent, member UCs, key entities, depended-on invariants |
| `actors.md` | Personas / actor types | individual · business owner · team member · manager (+ any others) |
| `uc-index.md` | **Traceability spine** | One row per UC: id · actor(s) · capability · invariants · source line · normalized one-liner |

Optional machine layer (decide in §6): a generated `uc-index.yaml` mirroring the
index table for programmatic consumption.

## 4. Work plan (phased)

Each phase is a discrete, reviewable deliverable. Phases 1–5 can be drafted in
parallel but must reconcile in Phase 6.

- **Phase 0 — Freeze & conventions.** Confirm output path; mark the vision
  read-only/canonical; lock ID schemes (`UC`, `BV`, new `INV`, `CAP`); restate
  the no-compression rule in the companion `README.md`.
- **Phase 1 — Extract invariants.** Sweep all UCs; collect every repeated
  cross-cutting constraint; dedupe into `INV1…` with rationale and the list of
  asserting UCs. (Pilot starting set: HITL approval, non-destructive,
  explainability/audit, privacy/ownership, progressive autonomy, reversibility,
  identity-as-one-person — verify against the text, don't assume.)
- **Phase 2 — Build the glossary.** Identify every distinct entity/term; pick one
  canonical name; list the vision's synonyms each one absorbs. Feed the project's
  `CONTEXT.md` ubiquitous-language convention if applicable.
- **Phase 3 — Cluster into capabilities.** Group UCs into `CAP1…`; for each,
  write intent, member UCs, key entities (from glossary), depended-on invariants.
  Flag UCs that resist clustering — they are a useful gap-check on the vision.
- **Phase 4 — Build the traceability index.** One row per UC with actor(s),
  capability, invariants, source line reference, and the normalized one-liner
  (invariant boilerplate factored out to `INV` refs).
- **Phase 5 — Actors.** Extract the distinct actor types and tag each UC's actor
  in the index.
- **Phase 6 — Consistency & gap pass.** Enforce the quality gates in §5; resolve
  orphans, unused invariants, and synonym collisions.
- **Phase 7 — Human review & finalize.** Read the companion set back to the user;
  invite cuts/merges; finalize.

> **Execution note.** This is a fan-out-friendly task (per-UC tagging, per-cluster
> drafting, adversarial consistency checks) and a good candidate for a
> multi-agent workflow — but only run one if the user explicitly opts in.
> Otherwise execute the phases inline.

## 5. Quality gates (acceptance criteria)

- **Vision unchanged** — byte-identical source; companion set only adds files.
- **Total coverage** — 100% of UCs appear in `uc-index.md` with ≥1 capability and
  ≥1 actor. Zero orphan UCs.
- **Invariants factored** — no invariant is restated verbatim inside a
  normalized UC line or capability description; it is referenced by `INV` id.
  Every `INV` is cited by ≥1 UC (no invented constraints).
- **Single language** — every concept has exactly one canonical glossary term;
  all known synonyms mapped to it.
- **Bidirectional links** — capability→UCs, UC→capability, invariant→UCs all
  resolve; pick any UC and trace it forward and back.
- **Independently loadable** — each derived doc makes sense loaded alone with the
  glossary + invariants, supporting selective context for downstream agents.

## 6. Decisions

**Resolved (2026-06-19):**

1. **Output location** — product repo `docs/brainstorming/`, parallel to the
   vision, in subfolder `ai-mail-vision-ai-spec/`.
2. **Machine layer** — markdown-first; no YAML/JSON until a real programmatic
   consumer appears.
3. **Reusability** — one-off pilot for ai-mail now; companion-skill
   (`vision-to-spec`) deferred.

**Still open (resolve during execution):**

4. **Parking-lot (`BV`) items** — the pilot vision currently parks nothing, so no
   `constraints.md` is needed yet. If `BV` items appear later, route them there
   rather than into UC clusters.
5. **Priority / phasing** — 67 UCs is a lot; a core-vs-later signal may help a
   downstream agent. The vision deliberately omits it; treat as a *separate*
   later artifact, out of scope for this pilot.
