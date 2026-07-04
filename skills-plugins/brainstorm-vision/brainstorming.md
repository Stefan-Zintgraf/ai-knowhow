# brainstorm-vision — Diverge

The **divergence** phase (see [`GLOSSARY.md`](GLOSSARY.md)): run the interview and fill the vision file. Stay here until **saturation** (see [`GLOSSARY.md`](GLOSSARY.md)), and don't steer the session toward wrap-up.

<the-interview>

Ask **one question at a time**. For each, offer your own recommended answer or a provocation — don't just interrogate. Drive the three **breadth axes** (see [`GLOSSARY.md`](GLOSSARY.md)) so the vision isn't quietly narrowed to one persona or one moment. The axis *labels* hold for any product; re-populate the examples for its audience — consumer/prosumer end-users, a technical or no-UI product (library, stack, protocol, infra, API), or internal/developer tooling:

- **Emotion** — what people feel. Consumer: overwhelm, dread, guilt, relief, delight. Technical: trust, risk, the fear of a 3am line-down, certification anxiety, the confidence of a thing that comes up right the first time. For an experiential product (a game, a toy, a creative tool) the desired feeling *is* the goal — wonder, tension, triumph, flow — not a problem to be removed.
- **Kinds of user** — the whole stakeholder chain, not one persona. Consumer: the swamped pro, the freelancer, the parent, the student, the novice. Technical: the evaluator running a PoC, the integrator, the maintainer debugging in the field, the buyer who signs off, the downstream operator who never sees the product directly.
- **The whole lifecycle** — before / arrival / acting / finding again / what should have been automatic. For a technical product this is the adoption arc: evaluate → integrate → bring-up → ship / certify → operate → debug in the field → port → maintain.

The **breadth axes** are the **floor, not the ceiling**: if the product has its own natural axis of breadth the three don't capture, name it and drive it too — the range of things a creative tool lets people *make*, the two *sides* of a marketplace, the *environments* a library gets embedded in, the *moods* a game plays in. Actively look for it — don't just rotate the three.

When an answer sounds like "the thing we were already going to build," push past it explicitly.

**Re-entered passes are focused.** After a **climb** (see [`GLOSSARY.md`](GLOSSARY.md)) the session re-enters divergence at a new **rung**. Walk the **breadth axes** over the *new rung's territory — the delta — only*; do not re-run them over ground already **saturated** at lower rungs. Revisit an existing item only where the wider frame genuinely re-frames it: move it to the new **scope item**'s group and **keep its number**.

</the-interview>

<framing>

These principles hold whether or not a brief was supplied.

- **Clean slate.** Forget the implementation, the platform, and every earlier decision. Nothing from a prior session or sibling artifact is a precondition. Start from the *person and their problem or desire*, not from a feature someone already picked.
- **Two shapes of value.** A product either *relieves a pain* or *fulfils a desire / creates an experience* — often some of both. Most tools sit on the pain side ("I can finally stop suffering X"); games, toys, entertainment, and creative products sit on the desire side ("I get to feel / make / explore Y"). Don't force an experiential product into problem-relief grammar — name the desire directly.
- **Push past the obvious.** The magic is in the later ideas, the ones that only surface once the easy answers are spent — keep going. The first handful of use-cases are the warm-up, not the answer; treat them as the floor. Don't anchor to a fixed count (a small product may have few use-cases, a broad one many) — instead keep generating until **saturation** (see [`GLOSSARY.md`](GLOSSARY.md)), checked per **anchor**.
- **The audience test.** The output must be readable by the product's target audience without the team's *internal* jargon — plain language, human benefit, no implementation. Pick the right floor of comprehension: for consumer software it's a relative who isn't in the field; for a technical or no-UI product it's a peer engineer or the buyer evaluating you, not an insider on the build team. If that reader couldn't follow it, it's pitched wrong.

</framing>

<capture>

Maintain one markdown file. By default, propose a path under `docs/brainstorming/` (e.g. `docs/brainstorming/<product-slug>-foundation-vision.md`) and let the user confirm or override it; remember the chosen path for the session. While the session is unfinished the working file carries a **`.wip.md`** suffix (see [`GLOSSARY.md`](GLOSSARY.md)); it is renamed to drop `.wip` only at final wrap-up (see [`finalizing.md`](finalizing.md)). It holds a `## Vision scope` section, a list of **vision points (press release)** grouped under **scope items**, and a growing flat list of **use-cases** — see the file format below. Append as items firm up; mention it in passing, don't interrupt with save dialogs.

**File each new point under its scope item as it lands.** A **vision point** sits under exactly one **scope item** (see [`GLOSSARY.md`](GLOSSARY.md)); on the first pass — before any **climb** — everything is filed under `S1`. Grouping never renumbers: a point keeps its `V`-number for the life of the file (see *Numbering & sorting* below).

**Vision points and use-cases co-evolve.** The **vision points** are not a summary of the **use-cases** — they're the same picture at a different altitude (the narrative whole, the feeling of the world after the product won). Keep each point **terse — a punchy fragment is good, often better than a full sentence**; the short narrative lead-in above the list carries the voice and altitude, so the points themselves can stay dense. Sketch a **provisional vision** (see [`GLOSSARY.md`](GLOSSARY.md)) early as a loose north star — one rough lead-in paragraph plus a few rough points is fine — and keep it explicitly editable. Let accumulating use-cases push it around; the use-cases reveal what the vision is really about. Finalize the vision points at wrap-up, not before.

</capture>

<scope-discipline>

**Scope discipline** (see [`GLOSSARY.md`](GLOSSARY.md)) keeps the **vision points** and **use-cases** in plain language the target audience would nod at — the benefit in their terms, not something an engineer could build from.

**Keep these OUT of the vision points and use-cases** (they don't disappear — the important ones go to the **parking lot**; see below):

- architecture / data flows ("the system fetches/parses/indexes…")
- modules / services / layers / seams — not even a coarse map
- technology / platform / vendor — clients, protocols, models, file formats, hosting
- MVP / v1 / Must-Should-Could / "what ships first" / tracer bullets
- edge cases / detailed requirements

**Rudder, not muzzle.** Let wild, half-formed ideas breathe in the *conversation* — that's where novelty comes from. The Vision points and Use-cases sections stay pure: when an out-of-scope idea is about to land *there*, name the drift in one line and restate the user-facing benefit as a use-case. But don't throw the idea itself away — if it's worth keeping for a later phase, park it. Never halt to lecture.

</scope-discipline>

<parking-lot>

A vision session keeps throwing off ideas that aren't vision or use-cases — an integration worth having, an architectural instinct, a hard "this has to work offline" constraint, a hunch about what v1 should be. Dropping them loses good thinking the *next* phase (architecture, design, scoping) would want. So instead of forbidding them, catch the important ones in the **parking lot** (see [`GLOSSARY.md`](GLOSSARY.md)) — without polluting the vision or use-cases.

**The challenge protocol.** When a non-vision item surfaces — whether the **user** raises it or **you** do — don't silently redirect *and* don't silently capture. Briefly challenge whether it's worth parking:

1. **Name it** in one line and flag that it's beyond the vision's scope.
2. Give **two pros and two cons** of capturing it — is it important enough to write down for a later phase, or just noise that would clutter the parking lot?
3. **The human decides. Always.** If yes, append it to the parking-lot section, numbered (`BV1`, `BV2`, …); if no, let it go and return to the vision.

Keep it light — one short exchange, then back to diverging. The parking lot must never become the session.

**You may raise items too.** If you notice an architecture- or integration-significant idea the user hasn't named, surface it yourself with the same challenge (one line + two pros + two cons).

**Scope signals — altitude drift, not scope creep.** A mid-**divergence** idea that doesn't fit the current **anchor** is a **scope signal** (see [`GLOSSARY.md`](GLOSSARY.md)) — a pull *up* a **rung**, not an out-of-scope aside. **Never climb mid-divergence.** Name it in one line, run the challenge protocol above, and if the human parks it, tag the entry `(scope signal)` so the **scope lens** finds it as evidence for the next **climb / close**. Then back to diverging at the current anchor.

**What belongs here.** Exactly the things **scope discipline** keeps out of the vision. Each is a terse note for a later phase, in engineer's shorthand — **the plain-language audience test does *not* apply here.**

**Not the same as the architecture-significance sweep** (step 1 of wrap-up, in [`finalizing.md`](finalizing.md)). That sweep uses architecture as a *lens* to surface missing **use-cases**, phrased in plain user language. The parking lot is the opposite: it captures genuine out-of-scope items, *as themselves*, the moment they come up mid-session. Both can run in one session — don't conflate them.

</parking-lot>

<file-format>

```markdown
# <Product> — Foundation Vision

## Vision scope

One or two sentences naming the current **anchor**: what this vision commits to,
in plain language. Then the **scope items** — one per **rung** climbed:

- **S1.** <the product's core job, as settled at session start>
- **S2.** <first climbed rung>
- **S3.** <second climbed rung — the anchor>

*Beyond the horizon:* <the declined rung, one line — named so the build phase
can keep the door open, explicitly NOT part of this vision.>

## Vision points (press release)

A short narrative lead-in — one or two sentences from the user's point of
view, set in the future where this product already won. It sets the altitude
and the feeling for the points below. Plain language; no jargon, no features list.

### S1 — <scope item title>

- **V1.** A terse, punchy point in the future-won voice — the whole-world feeling
  after the product won. Fragments are good; no jargon or feature/implementation lines.
- **V2.** …

### S2 — <scope item title>

- **V6.** …
- **V8.** …

### S3 — <scope item title>

- **V7.** …

## Use-cases

- **UC1.** As <a kind of user> facing <the problem> / wanting <the experience>, I can finally … / I get to …
- **UC2.** As a <kind of user>, I can finally …
- **UC3.** As a <kind of user>, I can finally …

## Beyond the vision (parking lot)

Out-of-scope ideas kept for the architecture/design/scoping phase — integrations,
hard constraints, tech leanings, MVP calls. Terse engineer's notes, NOT user
language. Present only if at least one item was parked.

- **BV1.** <one line — what it is and why it might matter later>
- **BV2.** …
```

**Three sections carry the vision — Vision scope, Vision points, Use-cases.** `## Vision scope` names the **anchor** and lists the **scope items** (`S1…Sn`) plus the *Beyond the horizon* line; on a zero-**climb** session it degrades to a single `S1` group plus the horizon line. `## Vision points` is **grouped under scope items** — one `### S<n> — <title>` heading per item, its points beneath. `## Use-cases` stays **one flat list**. A fourth section, **`## Beyond the vision (parking lot)`**, appears only if the human chose to park at least one item; omit it entirely when empty. (A paused **`.wip.md`** may also carry a `## Resume notes` section — working state, stripped at finalize. No other metadata, TOC, or design notes.)

**Numbering & sorting** (co-located here, beside the phase that writes the file):

- **Scope items** are numbered `S1…Sn` in **climb order** — which is also concrete → **anchor**, since each **climb** goes exactly one **rung** up. Append-only, **never renumbered**.
- **Vision points** keep **one global, continuous `V` numbering** across all groups. Sorting means *grouping*, never renumbering: append a new point at the end of the group it belongs to, so V-numbers are not monotonic down the page — that's fine, numbers are references, not positions. A point that later moves to a different group **keeps its number**.
- Every **vision point** sits under **exactly one** scope item. A point that genuinely spans all rungs (an **all-rung invariant**, e.g. AI-Mail's "you're always in charge") belongs under the **anchor** item — the widest in-scope rung — not duplicated.
- **Use-cases** stay a **flat, continuously-numbered list** (`UC1…`) in the order ideas arrived, no grouping or headings — the divergent looseness is load-bearing; scope structure lives in the vision points only. The **parking lot** is likewise a flat, numbered running list (`BV1…`). Never renumber on insert — append at the end so existing numbers stay stable references.

Avoid adding obvious near-duplicates; if a new idea restates an existing one, sharpen the existing bullet instead. **Within a single use-case, keep it to one persona and one relief** — cut restated destination lists and duplicate metaphors that say the same thing twice, and don't double any already mentioned guardrails. Tighten *redundancy*, never *voice*: this is a press-release doc read whole (by humans and agents alike), so the warm wording is load-bearing and every redundant word is a token paid 95× over — trim repetition, not the human register. Before every write, **re-read the file from disk** — the user may have edited, reordered, or cut items between turns; preserve their changes. Append or edit in place on request; never silently overwrite.

</file-format>

<long-session-checkpoint>

**Offer a checkpoint pause once you've asked roughly 15–20 questions without reaching saturation.** Offer it once, gently, the same way you'd offer wrap-up — never force it; ideas may still be flowing, and the human may want to push on. Frame it as *both* a good moment to `/clear` for a fresh context *and* a natural spot to take a short break. If the user would rather keep going, drop the offer and re-raise after about 4-6 further questions.

On agreement, follow the **Pause** flow in `SKILL.md` — but mark in the **`## Resume notes`** (see [`GLOSSARY.md`](GLOSSARY.md)) that this is a **context/break checkpoint, divergence NOT saturated**, so resuming drops straight back here into diverging (not the scope lens or finalize gate).

</long-session-checkpoint>

<reaching-saturation>

When you reach **saturation** or the user signals done, return to `SKILL.md` step 3: offer to wrap up and, once agreed, follow its fresh-session handoff.

</reaching-saturation>
