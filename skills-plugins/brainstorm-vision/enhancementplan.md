# brainstorm-vision — Enhancement plan: scope lens & scoped vision points

**Status: proposal — not yet applied.** This file is the plan for the change, not part of the
skill; delete it once the enhancement lands.

## Why

Two gaps, one root cause: the skill diverges **sideways** (more personas, emotions, lifecycle
moments) but never **upward** — and the resulting vision file never states its own altitude.

- **Altitude is an accident, not a decision.** Every product vision is a special case of a
  higher abstraction level, and that higher level *pulls* on a divergent session. Evidence:
  the AI-Mail foundation vision started as "email handled" and quietly climbed to paper
  letters, voicemail, phone calls (V6), chat apps (V8), non-email channels (UC76), watching
  the world beyond the inbox (UC80) — without the climb ever being named or chosen. The
  skill should make each climb a *reviewed decision* and catch drift when it happens.
- **The file's scope is implicit.** A reader must infer the vision's reach from ~30 points and
  ~90 use-cases. The scope itself should be a first-class part of the output file, and the
  vision points should be **sorted under scope items** so the structure shows, at a glance,
  which points live at which level of the vision's reach.

## The two enhancements

1. **Scope lens** — a new phase that runs at every divergence saturation, **before** the
   architecture lens. It proposes exactly **one** abstraction rung above the current scope;
   if the user climbs, the session **pauses** and **re-enters the brainstorming phase** with
   the widened scope. Only when the user declines to climb does the session proceed to the
   architecture lens and finalize. The ladder is thus *discovered one rung at a time*, never
   drafted up front.
2. **Vision scope in the output file** — a new `## Vision scope` section (scope items
   `S1…Sn`, one per rung climbed), with the `## Vision points` section grouped by scope
   item instead of flat.

## Why one rung at a time, in a separate phase

- Climbing the whole ladder at session start would anchor the divergence — the session would
  brainstorm toward the widest framing instead of exhausting the concrete one first.
- Each scope is diverged to **saturation before widening**, so no rung gets skimmed.
- The pause between rungs is the skill's existing fresh-context move (same as the finalize
  handoff): each scope gets a clean context, and the divergence transcript of the previous
  rung is dropped at no cost.
- The lens mirrors the architecture-significance sweep structurally — a deliberate,
  reviewed pass with its own doc — so the session's rhythm becomes:
  **diverge → scope lens (loop) → architecture lens → finalize.**

## Vocabulary

This section is the **seed for the skill's `GLOSSARY.md`** (see *Skill-craft* below). The
terms are built to be **leading words** — each recruits a pretraining prior so it earns its
tokens: you *climb* a *ladder* one *rung*; an *anchor* holds you where you are; a *horizon* is
seen but not reached; a *lens* is aimed. Reuse over coinage: **lens** is the skill's existing
word (architecture lens → scope lens), so the model links the two phases for free.

- **Ladder** — the chain of abstraction rungs the vision could occupy, from the product's
  concrete job upward. Never drafted whole; discovered one rung at a time by the scope lens.
- **Rung** — one abstraction level. A **scope item** is a rung *recorded in the file*.
- **Scope item (`S1…Sn`)** — a recorded, in-scope rung. `S1` is the product's job as settled
  at session start; each **climb** appends one. Vision points are sorted under scope items.
- **Anchor** — the top scope item so far; everything at or below it is in scope. Moves up
  exactly one rung per **climb**.
- **Climb / close** — the two outcomes of a scope-lens pass. *Climb* = accept the proposed
  rung (new anchor, pause, re-enter diverge). *Close* = decline it (record the horizon,
  proceed to the architecture lens).
- **Horizon** — the one rung the scope lens proposed and the user **closed** on. Recorded in
  the file, feeds the architecture lens's generalization door, binds nothing. Provisional:
  the route-back rule can reopen it.
- **Scope signal** — a mid-divergence idea that doesn't fit the current anchor. Not acted on
  at once: named in one line, parked, and used later as evidence by the scope lens.

*(Existing skill terms this enhancement leans on — **saturation**, **breadth axes**, **parking
lot**, **scope discipline**, the **wrap-up gate** — move into the same `GLOSSARY.md`, since it
holds the skill's **full** vocabulary, not just the new terms. See *Skill-craft* below.)*

Worked example (AI-Mail), as the loop would have played it:

| Pass | Scope after the pass | How it got there |
|---|---|---|
| Initial diverge | **S1.** Your inbox genuinely handled | topic settled at start |
| Scope lens #1 → climb | **S2.** All your correspondence handled — paper, calls, chat, voice | pause, re-enter diverge |
| Scope lens #2 → climb | **S3.** Everything that asks something of you is handled | pause, re-enter diverge |
| Scope lens #3 → decline | *Horizon:* a trusted chief-of-staff for your whole life | proceed to architecture lens |

## New output file format (sketch)

```markdown
# <Product> — Foundation Vision

## Vision scope

One or two sentences naming the current anchor: what this vision commits to,
in plain language. Then the scope items — one per rung climbed:

- **S1.** <the product's core job, as settled at session start>
- **S2.** <first climbed rung>
- **S3.** <second climbed rung — the anchor>

*Beyond the horizon:* <the declined rung, one line — named so the build phase
can keep the door open, explicitly NOT part of this vision.>

## Vision points (press release)

The short narrative lead-in, unchanged — one or two sentences in the future-won voice.

### S1 — <scope item title>

- **V1.** …
- **V2.** …

### S2 — <scope item title>

- **V6.** …
- **V8.** …

### S3 — <scope item title>

- **V7.** …

## Use-cases

(unchanged — one flat, continuously numbered list; deliberately NOT sorted)

## Beyond the vision (parking lot)

(unchanged)
```

## Numbering & sorting rules

- Scope items are numbered `S1…Sn` in the order the rungs were climbed — which is also
  concrete → anchor, since each climb goes exactly one rung up. Append-only, never
  renumbered.
- Vision points keep **one global, continuous `V` numbering** across all scope groups.
  Sorting means *grouping*, never renumbering: a new point is appended at the end of the
  group it belongs to, so V-numbers are not monotonic down the page — that's fine, numbers
  are references, not positions. A point that later moves to a different group **keeps its
  number**.
- Every vision point sits under exactly one scope item. A point that genuinely spans all
  rungs (e.g. AI-Mail's "you're always in charge" invariant) belongs under the **anchor**
  item — the widest in-scope rung — not duplicated.
- Use-cases stay a **flat list**. The divergent looseness of the UC list is load-bearing;
  scope structure lives in the vision points only.

## The session loop, end to end

1. **Session start** (`SKILL.md`) — settle the topic as today; additionally write the
   `## Vision scope` section with a single item `S1` (the product's job in one plain line).
   No ladder is drafted, mentioned, or hinted at. Cheap: one line, no extra questions.
2. **Diverge** (`brainstorming.md`) — as today, at the current anchor. New points are filed
   under their scope item as they land (first pass: everything under S1). When an idea
   doesn't fit the anchor, it's a **scope signal**: name it in one line, run the existing
   parking-lot challenge, and if parked, tag it `(scope signal)` so the lens finds it. No
   climbing mid-divergence.
3. **Scope lens** (new doc, `scope-lens.md`) — runs at every divergence saturation, once
   wrap-up is agreed, *before* any finalize handoff:
   - Privately consider what the current anchor is a special case of; pick the **one** most
     natural next rung — informed by the accumulated scope signals and any use-cases already
     straining the anchor. Never present a full ladder; one rung only.
   - Present it in plain language with a taste of the territory it would unlock (two or
     three one-line sketches of the kind of use-case that becomes possible). Recommend
     climb or close, honestly.
   - **The human decides. Always.**
   - **Climb:** append the rung as the next `S<n>` (it becomes the new anchor); update the
     scope lead-in; re-file any parked scope signals that now fit inside the new anchor as
     proper use-cases/points; then **pause** — write `## Resume notes` marking **"scope
     widened to S<n>, divergence NOT saturated at the new scope — resume re-enters diverge
     focused on the new rung"**, turn steering OFF, tell the user the file path and to
     `/clear` and re-invoke, then stop. The fresh session resumes straight into step 2.
   - **Close:** record the declined rung as the horizon line in `## Vision scope`, then
     proceed to the existing wrap-up handoff (fresh-session finalize gate), unchanged.
4. **Re-entered diverge** — a *focused* divergence: the three breadth axes are walked for the
   **new rung's territory** (the delta), not re-run over ground already saturated at lower
   rungs. Existing items are only revisited where the wider frame genuinely re-frames a
   point (move it, keep its number). Runs to saturation → back to step 3.
5. **Architecture lens + finalize** (`finalizing.md`) — as today, entered only after the
   scope lens closes. Two additions:
   - The lens template gains one cross-cutting dimension, the **generalization door**: the
     horizon rung as a one-way door — if the declined rung ever becomes real, which
     decisions made for the anchor become expensive? (For AI-Mail: an email-shaped data
     model vs. a channel-agnostic "correspondence" model.)
   - Step-2 read-back also walks the scope section (every point under the right item, no
     empty items, horizon line present), and reconciles `S<n>` references in the lens
     artifact the same way `UC<n>` references are reconciled today.
   - **Route back to the scope lens, don't reset.** The sweep surfaces use-cases one axis at
     a time (a stateful walk kept in a single fresh context — deliberately *not* one
     fresh session per use-case, which would only force repeated re-reads of the vision +
     lens artifact). But if a surfaced use-case is **scope-significant** — it only makes
     sense one rung above the current anchor — it is *not* appended here. Instead, hand it
     back to the **scope lens** as a scope signal: it becomes evidence that the ladder isn't
     actually closed, and the scope lens re-proposes that rung as a climb/close decision. If
     the user climbs, the normal climb pause fires (re-enter focused diverge at the new
     rung); if they decline again, the use-case is dropped or parked, not forced into the
     vision below its natural altitude. This is the one loop between the two lenses: the
     architecture sweep can *reopen* a closed ladder, but only through the scope lens's
     climb/close gate, never by silently widening scope itself.

### Pause/resume state machine (updated)

`## Resume notes` can now mark four states instead of three:

| State | Resume enters |
|---|---|
| checkpoint / break, divergence not saturated | diverge, same scope |
| **scope widened to S\<n\>** (new) | diverge, focused on the new rung |
| divergence saturated, wrap-up agreed | scope lens *(changed: was finalize step 1)* |
| ready to finalize (sweep done) | finalize step 2 |

Note the third row's meaning shifts: "wrap-up agreed" now lands in the scope lens first;
only a **closed** ladder proceeds to the architecture sweep. The resume-notes vocabulary in
`SKILL.md` must distinguish "wrap-up agreed, ladder open" from "ladder closed".

"Closed" is **provisional, not terminal.** The architecture sweep (step 5) can reopen a
closed ladder via the route-back rule — a scope-significant use-case sends the session back
through the scope lens, and from there potentially into a focused divergence at a new rung.
So the flow is a loop, not a one-way funnel: **diverge → scope lens → (climb ↺ diverge) →
architecture sweep → (scope-significant UC ↺ scope lens) → finalize.** Finalize is reached
only when the ladder is closed *and* the sweep produced no scope-significant use-case that
reopened it.

## Scope steering

Add one line to the re-injected steer carrying the **current anchor** in a few words, so long
sessions don't just remember *that* there's a boundary but *where* it sits. The anchor changes
per climb, so the steer text must be refreshed as part of the climb step. No change to the
flag mechanics or `scope-steer.sh`.

## Migration: existing / old-format visions

The **extend a finished vision** flow (SKILL.md, pause-and-resume) gains a retrofit step for
files that predate this format (no `## Vision scope` section):

1. Derive the rungs *from the evidence* — the existing points already show which rungs the
   vision lives on (for AI-Mail, V6/V8 alone prove a second rung exists).
2. Play the derived items back for review; the user confirms the anchor.
3. Insert the `## Vision scope` section and sort the existing points into `### S<n>` groups —
   **numbers untouched**, order within a group preserving the original relative order.
4. Any existing grouping headings (e.g. AI-Mail's "For individuals" / "For businesses") are
   reconciled: either they map onto scope items, or the audience split is re-expressed as
   scope items of their own — the user decides once, during retrofit.
5. The re-opened session then proceeds normally — including the scope-lens loop at its next
   saturation, which may climb further.

Never retrofit silently: it's a structural rewrite of a finalized artifact, so it only runs
inside an explicit re-open, and the file goes back through the finalize gate afterwards.

## Skill-craft: applying `writing-great-skills`

This enhancement adds a phase, a vocabulary, and a file — exactly the moment sediment and
sprawl creep in. Apply the discipline as we land it, not after.

### Leading words (do this first — it's the cheapest quality lever)

Standardise on the words in *Vocabulary* above and use them **as tokens, never re-explained
as sentences**, across every touched file. Concretely: prefer `climb`/`close` over
"widen"/"decline it", `anchor` over "current scope", `horizon` over "the rung above". The
payoff is double — fewer tokens, and the model reaches for the same behaviour every time the
token appears. The `SKILL.md` description line (this is a **user-invoked** skill, so the
description costs no per-turn context load — but the human still types it) should carry the
words a user would reach for: *scope lens*, *abstraction*, *widen the vision*.

### Disclose the vocabulary to `GLOSSARY.md` (single source of truth)

The new terms interlock (climb changes the anchor, which is a rung on the ladder, which the
horizon sits one above). Left inline, each would be re-defined in `SKILL.md`, `scope-lens.md`,
`brainstorming.md`, and `finalizing.md` — four **single sources of truth** for one meaning,
i.e. **duplication**. Instead, add a `GLOSSARY.md` (following the `writing-great-skills`
model: bold cross-refs, terms co-located) holding the *Vocabulary* set, and have every file
**bold the term and point at the glossary** rather than restate it. The glossary is disclosed
**reference** — loaded on demand — so it costs nothing until reached.

**Cover the whole vocabulary, not just the enhancement's.** The `brainstorm-vision` skill has
no glossary today; its existing terms (saturation, breadth axes, divergence, press-release
vision points, use-cases, parking lot, scope discipline, provisional vision, wrap-up gate,
architecture-significance sweep, one-way door, `.wip.md`, resume notes) are defined inline,
scattered across four files. A glossary that held *only* the new terms would leave two
conventions in one skill — new terms in the glossary, old terms inline — which is itself a
single-source-of-truth split. So the glossary is the skill's **domain model**: it holds the
**full vocabulary set**, existing and new, and every md file points at it.

Migration is part of this change, not a "later pass": each existing inline definition moves
*into* the glossary as its single source of truth, and its original site becomes a bold term
+ pointer (the same treatment the new terms get). This is more edit surface, but it's a
one-time consolidation that leaves exactly one home per meaning — the state the whole
discipline is aimed at. Group the glossary by axis the way `writing-great-skills` does
(e.g. *Divergence*, *Scope & altitude*, *Wrap-up*, *Session state*), with each **failure/guard
term** beside the lever it serves.

### Which file cuts earn their keep — and which would just be sprawl

The discipline is *split only when the cut earns it*. Judged that way:

- **`scope-lens.md` — earns it.** It's a distinct **branch** (a whole phase), it mirrors
  `finalizing.md`, and keeping it out of `SKILL.md` means the wrap-up handoff can read it in
  a fresh context (same reason `finalizing.md` is separate today — the model must *not* read
  it inline during divergence, or the finalize/scope machinery anchors the diverge phase).
- **`GLOSSARY.md` — earns it.** Disclosed reference, consulted on demand, one home for the
  interlocking vocabulary.
- **Do NOT split out the file-format / S-numbering rules.** They belong **co-located** in
  `brainstorming.md`, beside the diverge phase that writes the file. Fragmenting them into
  their own file would scatter one meaning across two — the opposite of co-location, and no
  branch needs them in isolation.
- **Do NOT make a file per new concept.** Anchor, climb, horizon are glossary *entries*, not
  files. A file each would be sprawl dressed as structure.

### Completion criteria for the new phase

A phase without a checkable **completion criterion** invites **premature completion** — the
agent declaring the scope settled to get on to finalize. Make the scope-lens pass end on a
sharp, checkable bound: *one rung proposed in plain language, and the human has explicitly
chosen climb or close.* Not "scope feels right" (fuzzy, gives way). On climb, the pause is a
real context boundary, so the finalize/architecture steps ahead are hidden — no lookahead to
rush toward. On close, the horizon line being written **is** the criterion that the pass is
done.

## File-by-file change list

All prose below uses the leading words as tokens and points at `GLOSSARY.md` for definitions
rather than restating them.

| File | Change |
|---|---|
| `GLOSSARY.md` | **New doc** — the skill's domain model, disclosed reference holding the **full vocabulary** (new: ladder, rung, scope item, anchor, climb/close, horizon, scope signal — *and* existing: saturation, breadth axes, divergence, vision points, use-cases, parking lot, scope discipline, provisional vision, wrap-up gate, architecture sweep, one-way door, resume notes). `writing-great-skills` model: grouped by axis, bold cross-refs, guard terms beside their lever. |
| *all four existing `.md` files* | Each inline definition of an existing term is **replaced by a bold term + glossary pointer**, migrating the definition into `GLOSSARY.md`. One-time consolidation; folded into the edits already listed per file below. |
| `scope-lens.md` | **New doc** — the scope-lens phase: one-rung proposal method, climb/close protocol, pause handoff, scope-signal re-filing, and the pass **completion criterion** (climb-or-close chosen). Sibling of `finalizing.md`. |
| `SKILL.md` | Sequencing: at saturation, read `scope-lens.md` before any finalize handoff; new resume state "scope widened"; retrofit in "extend a finished vision"; description line carries the user's trigger words (*scope lens*, *abstraction*, *widen the vision*). |
| `brainstorming.md` | File format: `## Vision scope`, grouped vision points, S-numbering rules — all **co-located** here beside the diverge phase, not split out; capture rules for filing points under items; scope-signal handling (name → parking-lot challenge → tag); focused-divergence rules for re-entered passes. |
| `finalizing.md` | Entered only via a closed ladder; scope walk + `S<n>` reconciliation in step 2; pointer to the generalization door; **route-back rule** — a scope-significant use-case surfaced by the sweep goes back to the scope lens as a signal, reopening the climb/close gate rather than being appended below its altitude. |
| `architecture-significance-lens-template.md` | Add **generalization door** to the cross-cutting spine. |
| `scope_boundary.md` | One line carrying the current anchor in the per-turn steer; refreshed on each climb. |
| `scope-steer.sh` | No change expected. |

## Open questions

1. **Should use-cases get an optional `S<n>` tag?** Pro: the lens and build phase could
   slice UCs by scope item. Con: tagging 90+ UCs adds friction and sneaks structure into
   the deliberately loose list. Current lean: no — keep UCs flat and untagged.
2. **May the scope lens propose a rung it already had declined territory-adjacent signals
   for?** i.e. if scope signals cluster somewhere that isn't the "natural" next abstraction,
   does the lens follow the evidence or the ladder? Current lean: follow the evidence — the
   signals are the better guide to where the vision wants to grow.
3. **Is there a cap on climbs?** Current lean: no hard cap — the human declines when it
   stops being their product; the one-rung-per-pass rhythm plus a full focused divergence
   per rung is a natural brake.
4. **Can a session have zero climbs?** Yes by design — the user declines the first proposal,
   the file has a single `S1` group plus a horizon line, and the format degrades gracefully
   to today's shape plus one heading.
5. **Does a climb re-trigger the steering verification (checks A–C)?** Current lean: the
   climb pause turns steering OFF and the resumed session re-runs the normal start logic,
   so verification happens for free on re-entry; nothing extra needed.

## Execution: sequential sub-agent phases

This plan is long because it's a **spec** — executing it shouldn't drag the whole spec through
one context. Slice it into **sequential phases, one sub-agent per phase**, each a **cold
session** that reads only its slice (the named plan sections + its target files + `GLOSSARY.md`)
and returns a short handoff. The **main agent only orchestrates**: it holds the phase list and
the one-paragraph handoffs, never the target-file contents, and dispatches phase N+1 only after
phase N reports done. Phases run **sequentially** — they form a dependency chain, and the first
two produce **contracts** the rest lean on:

- **Vocabulary contract** — `GLOSSARY.md` (P0). Every later phase *points* terms at it, never
  re-defines.
- **Format contract** — the `## Vision scope` + grouped-points + S-numbering spec in
  `brainstorming.md` (P1). Every later phase writes to that shape.

Each dispatch brief is the same shape: *"Read `enhancementplan.md` §X, §Y and files A, B.
Make the edits. Return a ≤10-line handoff: what changed, any contract detail the next phase
needs, anything you couldn't resolve."* That brief — not the conversation — is the sub-agent's
whole context, which is where the savings come from.

**P0 — Vocabulary contract.**
- Reads: *Vocabulary*, *Skill-craft*→glossary; skim the existing `.md` files for inline defs.
- Writes: `GLOSSARY.md` (full vocab, authoritative defs) + a **migration map** — each existing
  term → its current definition site, to be swapped for a pointer by the phase that owns that
  file (a term whose file no later phase touches is pointer-swapped here).
- Handoff: the leading-word set + the migration map.
- Done when: every term has exactly one glossary entry; the map lists every inline site.

**P1 — Format contract (`brainstorming.md`).** · depends: P0
- Reads: `GLOSSARY.md`, migration map, `brainstorming.md`; plan *New output file format*,
  *Numbering & sorting rules*, session-loop steps 1–2 & 4.
- Writes: format sections, capture rules, scope-signal handling, focused-divergence rules;
  swaps this file's inline defs for glossary pointers.
- Handoff: the frozen file-format spec.
- Done when: format matches plan; S-numbering rules present; pointers resolve.

**P2 — Scope lens & session wiring (`scope-lens.md` new, `SKILL.md`, `scope_boundary.md`).** · depends: P0, P1
- Reads: `GLOSSARY.md`, `SKILL.md`, `finalizing.md` (structure to mirror), `scope_boundary.md`;
  plan *session loop*, *pause/resume state machine*, *scope steering*, completion-criterion note.
- Writes: `scope-lens.md`; SKILL sequencing loop + four resume states + retrofit + description;
  anchor line in the steer; pointer-swaps for SKILL's inline defs.
- Handoff: the resume-state vocabulary + the loop wiring.
- Done when: diverge→scope-lens→(climb ↺)→finalize is wired; the four resume states are named.

**P3 — Finalize & architecture lens (`finalizing.md`, `…lens-template.md`).** · depends: P0–P2
- Reads: `GLOSSARY.md`, `finalizing.md`, `architecture-significance-lens-template.md`,
  `scope-lens.md` (route-back target); plan session-loop step 5, route-back rule, generalization
  door.
- Writes: scope walk + `S<n>` reconciliation in step 2; generalization door in template +
  pointer; route-back rule; pointer-swaps for finalize's inline defs.
- Handoff: route-back wired both directions.
- Done when: route-back reopens the scope lens; generalization door is in the spine.

**P4 — Prune & acceptance dry-run** (a **fresh** agent on purpose — cold eyes). · depends: P0–P3
- Reads: all touched files + `GLOSSARY.md`; plan acceptance criteria.
- Does: hunt **no-ops** and **duplication** (any term re-explained instead of pointed at the
  glossary, any leading word left as a sentence — the sediment guard); verify every pointer
  resolves to one glossary home; run the AI-Mail retrofit dry-run — the rungs derived from its
  existing points reproduce the worked example, every existing V-point finds exactly one home,
  and the re-opened session's next scope-lens pass proposes the chief-of-staff rung.
- Done when: no no-ops/dupes remain; every pointer resolves; the dry-run passes.

**Orchestration note.** The main agent runs these with the sub-agent/`Agent` tool, one at a
time, `run_in_background: false` so each completes before the next is dispatched. It never edits
files itself; if a handoff surfaces an unresolved contract question, the main agent settles it
(or asks the user) before dispatching the dependent phase, so a bad assumption never propagates
down the chain.
