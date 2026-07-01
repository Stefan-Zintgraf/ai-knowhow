---
name: brainstorm-vision
description: Coach a divergent product-vision brainstorm, captured as a press-release vision plus user-POV use-cases.
disable-model-invocation: true
---

<what-to-do>

Run a relentless, one-question-at-a-time brainstorming session that opens up the **widest possible high-level vision** of a product, and capture the results in a single living markdown file.

This works for any product, software preferred. The session is **divergent**: push past the obvious first answers — the good ideas live in the territory you reach only after the easy ones are spent.

**Starting context.** If the user passes a brief/foundation file (or one is open), read it first and treat its topic and goal as already chosen. Confirm in one line and begin — do not re-elicit what the brief already settled. If there is no brief, ask once what product or problem we're opening up, then start.

**The interview.** Ask one question at a time. For each, offer your own recommended answer or a provocation — don't just interrogate. Drive breadth across three axes so the vision isn't quietly narrowed to one persona or one moment:

- **Emotion** — what people feel (overwhelm, dread, guilt, relief, delight).
- **Kinds of user** — the swamped pro, the freelancer, the parent, the student, the novice.
- **The whole lifecycle** — before / arrival / acting / finding again / what should have been automatic.

When an answer sounds like "the thing we were already going to build," push past it explicitly.

**Capture.** Maintain one markdown file. By default, propose a path under `docs/brainstorming/` (e.g. `docs/brainstorming/<product-slug>-foundation-vision.md`) and let the user confirm or override it; remember the chosen path for the session. While the session is unfinished the working file carries a `.wip.md` suffix (`<product-slug>-foundation-vision.wip.md`); it is renamed to drop `.wip` only at final wrap-up. Before opening a fresh file, check for an existing paused session — see Pause and resume. It has exactly two parts: a **press-release-style vision** (the future where this product already won, from the user's POV) and a growing list of **human use-cases** ("as someone who …, I can finally …"). See the file format below. Append as items firm up; mention it in passing, don't interrupt with save dialogs.

**Vision and use-cases co-evolve.** The vision is not a summary of the use-cases — it's the same picture at a different altitude (the narrative whole, the feeling of the world after the product won). Sketch a *provisional* vision early as a loose north star — one rough paragraph is fine — and keep it explicitly editable. Let accumulating use-cases push it around; the use-cases reveal what the vision is really about. Finalize the vision at wrap-up, not before.

</what-to-do>

<framing>

These principles always hold, whether or not a brief was supplied — the skill must work the same with no foundation file at all.

- **Clean slate.** Forget the implementation, the platform, and every earlier decision. Nothing from a prior session or sibling artifact is a precondition. Start from the *person and their problem*, not from a feature someone already picked.
- **Push past the obvious.** The first answer is usually "the thing we were already going to build." The magic is in the later ideas, the ones that only surface once the easy answers are spent — keep going. The first handful of use-cases are the warm-up, not the answer; treat them as the floor. Don't anchor to a fixed count (a small product may have few use-cases, a broad one many) — instead keep generating until **saturation**: the point where the three breadth axes are genuinely covered and fresh questions only restate use-cases already captured. Saturation is both the floor for going wide *and* the signal the session is ready to wrap.
- **The audience test.** The output must be readable by a typical, non-technical end user. If a relative who is not in the field couldn't follow it, it's pitched wrong. Plain language, human benefit, no jargon.

</framing>

<session-end>

The session ends when the user signals it ("done", "that's enough", "wrap up"), **or** when the coach judges breadth has reached **saturation** (see Framing). When the coach senses that point, it **offers** to wrap up (once, gently — never forces it; a divergent session shouldn't be cut short while ideas are still flowing).

**Wrap-up is a two-step gate — never jump straight to finalizing.**

**Step 1 — Architecture-significance sweep (automatic).** Before finalizing, run the sweep without being asked — the last completeness backstop. See Architecture-significance sweep. When it reaches saturation the session is **ready to finalize** — say so, then move to step 2.

**Step 2 — Finalize.** Re-read the file, read the vision, the full use-case list, and any parked items back to the user for a final sanity pass, invite cuts/merges/sharpening, then **finalize** — strip any `## Resume notes` section and rename `<name>.wip.md` → `<name>.md` so the final artifact obeys the format (Vision and Use-cases, plus the `## Beyond the vision (parking lot)` section if anything was parked). If use-cases changed since step 1, reconcile the `<slug>-architecture-lens.md` artifact's `UC<n>` cross-references so they still point at the right use-cases. Then rename the steering flag to `_off` (see below).

A session can also be **paused** mid-flight and resumed in a later sitting — including at the "ready to finalize" milestone between the two steps. See Pause and resume.

</session-end>

<architecture-significance-sweep>

Step 1 of the wrap-up gate, and the last completeness backstop before finalizing. The vision stayed deliberately out of architecture — but some user needs, if they only surface *after* building has begun, force expensive rework of one-way-door decisions: the overall architecture, the software design, the platform/language, the data model. This sweep catches the use-cases behind those decisions while changing them is still free.

**It is a lens, not a layer.** Think in architecturally-loaded terms privately; capture only what an ordinary user would say. Everything kept is still a plain user-POV use-case ("As someone …, I can finally …") — never a note about offline-sync, schemas, hosting, or tenancy. Scope discipline holds in full; you are only aiming the divergence at corners that are cheap to decide now and dear to change later. (If the sweep surfaces a genuine architecture *constraint* rather than a use-case — something the build phase must honour — that's a parking-lot item, not a use-case; run the parking-lot challenge on it instead. See Parking lot.)

**Method — build the product's lens, then walk it.**

1. **Build the lens (explicit, reviewed, saved).** Open `architecture-significance-lens-template.md` — the seed, not the product's lens. Its invariant is the one-way-door test — *which decisions are cheap now and expensive to discover after building starts?* Using the template's example clusters as seeds, derive the axis list for *this specific* product: pick the closest cluster, then close by asking the invariant of the product to catch the defining door no cluster names (a hypervisor's core/device partitioning, a simulator's fidelity-vs-speed). **Play the derived axes back to the user** — keep/sharpen/drop — so the lens is reviewed, not improvised. Do this only now, at wrap-up: deriving it earlier would pull architecture thinking into the divergent phase and anchor the vision. Write the agreed lens to a **separate build-phase artifact**, `<output-dir>/<slug>-architecture-lens.md` (engineer shorthand, like the parking lot — *not* end-user language) — but if that file already exists (a resumed or re-opened session), **read it first and extend/reconcile it**, never overwrite. It is a sibling of the vision file and a handoff to the next phase; it **never** enters the vision file's Vision/Use-cases sections, which stay pure.

2. **Walk the lens.** For each agreed axis, ask yourself: *is there a user whose need on this axis we haven't captured yet?* If so, offer one candidate use-case in plain language and let the user keep, sharpen, or drop it — new use-cases re-open brief divergence on those axes. These axes overlap the three breadth axes (emotion / kinds of user / lifecycle) but cut a different way. Keep sweeping until the lens reaches **saturation** — that's the signal step 1 is done and the session is ready to finalize.

</architecture-significance-sweep>

<pause-and-resume>

A vision session can span multiple sittings. The working file keeps its `.wip.md` suffix for as long as the session is unfinished, so an on-disk `*.wip.md` in the output directory *is* a paused, resumable session — even if the previous sitting ended abruptly without a clean pause.

**Resuming or extending (at session start).** Before proposing a new path, look in the output directory (default `docs/brainstorming/`) for prior work — both `*.wip.md` (a paused session) **and** finalized `*-foundation-vision.md` (a completed vision that can be re-opened to add use-cases). If any exist, **always ask the user** what to do — never auto-continue. Name the file(s) and topic(s), then offer the choice:

- **Resume a paused session** (`*.wip.md`) — read the whole file (vision, use-cases, and the `## Resume notes` if present), play back in two or three sentences where you left off and what's still open, then continue from there. Don't re-elicit settled ground. If the notes say the session is **ready to finalize** (the step-1 sweep is already done), go straight to step 2 — unless use-cases changed since the sweep, which warrants a quick re-sweep of the affected axes first.
- **Extend a finished vision** (`*-foundation-vision.md`) — re-open it: rename it back to `<name>.wip.md`, turn scope steering ON, and continue appending use-cases from where it stands (continuous numbering — never renumber existing items). At the next wrap-up its `<slug>-architecture-lens.md` is reconciled if present, or generated from scratch if absent (e.g. a vision finalized before the lens artifact existed).
- **Start fresh** — leave existing files untouched and begin a new `.wip.md` for the new topic.

If there are several candidates, list them and ask which (if any) to resume or extend.

**Pausing (on request — "pause", "stop for now", "let's continue later").**

1. Make sure the `.wip.md` is current (vision + use-cases written, per the file format).
2. Add or refresh a `## Resume notes` section at the end, capturing just enough session state to pick up cleanly: which breadth axes (emotion / kinds of user / lifecycle) are well covered vs. thin, threads left open, the next question you would have asked, and whether the provisional vision still feels right. If you've reached the wrap-up gate, note how far the step-1 sweep got — which axes in the `<slug>-architecture-lens.md` artifact are covered vs. open (the artifact itself holds the axes; don't duplicate them here) — and, if it's complete, that the session is **ready to finalize** (so resuming can skip straight to step 2). This is where the "ready to finalize" state lives when a session pauses between the two steps.
3. Turn scope steering OFF — a pause is a mini session-end (see the steering hook).
4. Tell the user the file path and that re-invoking the skill will resume from it. Then stop.

</pause-and-resume>

<scope-discipline>

The **vision and use-cases** are plain language an ordinary user would nod at — not something an engineer could build from.

**Keep these OUT of the vision and use-cases** (they don't disappear — the important ones go to the parking lot; see below):

- architecture / data flows ("the system fetches/parses/indexes…")
- modules / services / layers / seams — not even a coarse map
- technology / platform / vendor — clients, protocols, models, file formats, hosting
- MVP / v1 / Must-Should-Could / "what ships first" / tracer bullets
- edge cases / detailed requirements

**Rudder, not muzzle.** Let wild, half-formed ideas breathe in the *conversation* — that's where novelty comes from. The Vision and Use-cases sections stay pure: when an out-of-scope idea is about to land *there*, name the drift in one line and restate the user-facing benefit as a use-case. But don't throw the idea itself away — if it's worth keeping for a later phase, park it (see Parking lot). Never halt to lecture.

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

**Not the same as the architecture-significance sweep.** That sweep (step 1 of wrap-up) uses architecture as a *lens* to surface missing **use-cases**, phrased in plain user language, and keeps architecture notes out of the file. The parking lot is the opposite: it captures genuine out-of-scope items, *as themselves*, the moment they come up mid-session. Both can run in one session — don't conflate them.

</parking-lot>

<scope-steering-hook>

Some repos ship a `UserPromptSubmit` hook that re-injects the scope boundary every turn so it never fades over a long session. This counters **context rot** — as the conversation grows, a steer given once near the top loses salience even while still technically in context (the model keeps the words but quietly down-weights them); re-stating it at the end of each prompt restores it to the highest-attention position. (It also survives compaction, when the original may be summarized away entirely — but rot is the everyday reason, present from turn one.) It is gated by a flag file in the **current git submodule's root** (`$CLAUDE_PROJECT_DIR`), toggled by renaming:

- `brainstorm_scope_boundary_on.md` → steering ON
- `brainstorm_scope_boundary_off.md` → steering OFF (resting state)

Both names are git-ignored local state, so on a fresh clone neither may exist.

**At session start**, ensure steering is ON in `$CLAUDE_PROJECT_DIR`:

- if `brainstorm_scope_boundary_off.md` exists → rename it to `brainstorm_scope_boundary_on.md`;
- else if neither exists → create `brainstorm_scope_boundary_on.md` (contents irrelevant; only its existence matters).

The hook fires at prompt-submit, so steering kicks in from the turn *after* this — fine; the kickoff turn doesn't need it. This skill carries the same discipline self-contained, so it works even in repos without the hook.

**At session end** — and equally when the session is **paused** — rename `brainstorm_scope_boundary_on.md` back to `brainstorm_scope_boundary_off.md` so steering doesn't bleed into unrelated work. **Resuming** a paused session re-runs the same start logic, turning it back ON.

</scope-steering-hook>

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

**Two sections are mandatory — Vision and Use-cases.** A third, **`## Beyond the vision (parking lot)`**, appears only if the human chose to park at least one item (see Parking lot); omit it entirely when empty. (A paused `.wip.md` may also carry a `## Resume notes` section — working state, stripped at finalize; see Pause and resume. No other metadata, TOC, or design notes.) Keep the use-case list **flat** — one running list in the order ideas arrived, no grouping or headings (clustering would sneak structure into a list that's meant to stay loose and divergent); the parking lot is likewise a flat, numbered running list. Number items continuously (`UC1…`, `BV1…`) and never renumber on insert — append new items at the end so existing numbers stay stable references. Avoid adding obvious near-duplicates; if a new idea restates an existing one, sharpen the existing bullet instead. Before every write, **re-read the file from disk** — the user may have edited, reordered, or cut items between turns; preserve their changes. Append or edit in place on request; never silently overwrite.

**The architecture-lens artifact (`<slug>-architecture-lens.md`)** is a *separate* sibling file, written at wrap-up (step 1), never mixed into the vision file. It holds the product's derived one-way-door axes for the build phase — engineer shorthand, **not** end-user language (same audience as the parking lot). One flat section:

```markdown
# <Product> — Architecture lens

Derived at vision wrap-up. The one-way-door axes for this product — decisions
cheap to make now, expensive to discover after building starts — each with the
user need behind it. Build-phase handoff; not part of the vision.

- **<axis>** — <the one-way-door decision it forces> · surfaced by UC<n>, UC<n>
- …
```

Cross-reference each axis to the use-case numbers it surfaced (`UC<n>`) so the lens ties back to the vision's use-cases without restating them.

</file-format>
