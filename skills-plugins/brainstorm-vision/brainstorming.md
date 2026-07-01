# brainstorm-vision — Diverge

The divergent phase: run the interview and fill the vision file. Stay here until **saturation** (defined in Framing). This file is loaded for the whole session; the wrap-up gate lives in [`finalizing.md`](finalizing.md) and is read **only once saturation is reached** — don't peek at it early, and don't steer toward it.

<the-interview>

Ask **one question at a time**. For each, offer your own recommended answer or a provocation — don't just interrogate. Drive breadth across three axes so the vision isn't quietly narrowed to one persona or one moment:

- **Emotion** — what people feel (overwhelm, dread, guilt, relief, delight).
- **Kinds of user** — the swamped pro, the freelancer, the parent, the student, the novice.
- **The whole lifecycle** — before / arrival / acting / finding again / what should have been automatic.

When an answer sounds like "the thing we were already going to build," push past it explicitly.

</the-interview>

<framing>

These principles always hold, whether or not a brief was supplied — the skill must work the same with no foundation file at all.

- **Clean slate.** Forget the implementation, the platform, and every earlier decision. Nothing from a prior session or sibling artifact is a precondition. Start from the *person and their problem*, not from a feature someone already picked.
- **Push past the obvious.** The first answer is usually "the thing we were already going to build." The magic is in the later ideas, the ones that only surface once the easy answers are spent — keep going. The first handful of use-cases are the warm-up, not the answer; treat them as the floor. Don't anchor to a fixed count (a small product may have few use-cases, a broad one many) — instead keep generating until **saturation**: the point where the three breadth axes are genuinely covered and fresh questions only restate use-cases already captured. Saturation is both the floor for going wide *and* the signal the session is ready to wrap.
- **The audience test.** The output must be readable by a typical, non-technical end user. If a relative who is not in the field couldn't follow it, it's pitched wrong. Plain language, human benefit, no jargon.

</framing>

<capture>

Maintain one markdown file. By default, propose a path under `docs/brainstorming/` (e.g. `docs/brainstorming/<product-slug>-foundation-vision.md`) and let the user confirm or override it; remember the chosen path for the session. While the session is unfinished the working file carries a `.wip.md` suffix (`<product-slug>-foundation-vision.wip.md`); it is renamed to drop `.wip` only at final wrap-up (see [`finalizing.md`](finalizing.md)). It has exactly two parts: a **press-release-style vision** and a growing list of **human use-cases** — see the file format below. Append as items firm up; mention it in passing, don't interrupt with save dialogs.

**Vision and use-cases co-evolve.** The vision is not a summary of the use-cases — it's the same picture at a different altitude (the narrative whole, the feeling of the world after the product won). Sketch a *provisional* vision early as a loose north star — one rough paragraph is fine — and keep it explicitly editable. Let accumulating use-cases push it around; the use-cases reveal what the vision is really about. Finalize the vision at wrap-up, not before.

</capture>

<scope-discipline>

The **vision and use-cases** are plain language an ordinary user would nod at — not something an engineer could build from.

**Keep these OUT of the vision and use-cases** (they don't disappear — the important ones go to the parking lot; see below):

- architecture / data flows ("the system fetches/parses/indexes…")
- modules / services / layers / seams — not even a coarse map
- technology / platform / vendor — clients, protocols, models, file formats, hosting
- MVP / v1 / Must-Should-Could / "what ships first" / tracer bullets
- edge cases / detailed requirements

**Rudder, not muzzle.** Let wild, half-formed ideas breathe in the *conversation* — that's where novelty comes from. The Vision and Use-cases sections stay pure: when an out-of-scope idea is about to land *there*, name the drift in one line and restate the user-facing benefit as a use-case. But don't throw the idea itself away — if it's worth keeping for a later phase, park it. Never halt to lecture.

</scope-discipline>

<parking-lot>

A vision session keeps throwing off ideas that aren't vision or use-cases — an integration worth having, an architectural instinct, a hard "this has to work offline" constraint, a hunch about what v1 should be. Dropping them loses good thinking the *next* phase (architecture, design, scoping) would want. So instead of forbidding them, **catch the important ones in a separate parking lot** — without polluting the vision or use-cases.

**The challenge protocol.** When a non-vision item surfaces — whether the **user** raises it or **you** do — don't silently redirect *and* don't silently capture. Briefly challenge whether it's worth parking:

1. **Name it** in one line and flag that it's beyond the vision's scope.
2. Give **two pros and two cons** of capturing it — is it important enough to write down for a later phase, or just noise that would clutter the parking lot?
3. **The human decides. Always.** If yes, append it to the parking-lot section, numbered (`BV1`, `BV2`, …); if no, let it go and return to the vision.

Keep it light — one short exchange, then back to diverging on the vision. The parking lot must never become the session; the vision and use-cases are still the point.

**You may raise items too.** If you notice an architecture- or integration-significant idea the user hasn't named, surface it yourself with the same challenge (one line + two pros + two cons) and let the human decide. Never decide for them.

**What belongs here.** Exactly the things scope discipline keeps out of the vision (integrations, architecture/data-flow instincts, tech/platform/vendor leanings, MVP/scoping calls, hard constraints, edge cases). Each is a terse note for a later phase — **the plain-language audience test does *not* apply here.** Engineer's shorthand is fine, because this section is explicitly for the build phase, not the end user.

**Not the same as the architecture-significance sweep** (step 1 of wrap-up, in [`finalizing.md`](finalizing.md)). That sweep uses architecture as a *lens* to surface missing **use-cases**, phrased in plain user language. The parking lot is the opposite: it captures genuine out-of-scope items, *as themselves*, the moment they come up mid-session. Both can run in one session — don't conflate them.

</parking-lot>

<file-format>

```markdown
# <Product> — Foundation Vision

## Vision (press release)

A few short paragraphs from the user's point of view, set in the future
where this product already won. Plain language; no jargon, no features list.

## Use-cases

- **UC1.** As someone overwhelmed by <the problem>, I can finally …
- **UC2.** As a <kind of user>, I can finally …
- **UC3.** As a <kind of user>, I can finally …

## Beyond the vision (parking lot)

Out-of-scope ideas kept for the architecture/design/scoping phase — integrations,
hard constraints, tech leanings, MVP calls. Terse engineer's notes, NOT user
language. Present only if at least one item was parked.

- **BV1.** <one line — what it is and why it might matter later>
- **BV2.** …
```

(Examples are placeholders — fill them with the actual product's users and problem.)

**Two sections are mandatory — Vision and Use-cases.** A third, **`## Beyond the vision (parking lot)`**, appears only if the human chose to park at least one item; omit it entirely when empty. (A paused `.wip.md` may also carry a `## Resume notes` section — working state, stripped at finalize. No other metadata, TOC, or design notes.) Keep the use-case list **flat** — one running list in the order ideas arrived, no grouping or headings (clustering would sneak structure into a list that's meant to stay loose and divergent); the parking lot is likewise a flat, numbered running list. Number items continuously (`UC1…`, `BV1…`) and never renumber on insert — append new items at the end so existing numbers stay stable references. Avoid adding obvious near-duplicates; if a new idea restates an existing one, sharpen the existing bullet instead. Before every write, **re-read the file from disk** — the user may have edited, reordered, or cut items between turns; preserve their changes. Append or edit in place on request; never silently overwrite.

</file-format>

<reaching-saturation>

**Saturation** (defined in Framing) is the completion criterion for this phase — and only then does the session become ready to wrap.

When you reach saturation (or the user signals done), return to `SKILL.md` step 3: offer to wrap up, and once agreed, read [`finalizing.md`](finalizing.md). Do not open it before saturation.

</reaching-saturation>
