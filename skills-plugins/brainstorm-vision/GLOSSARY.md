# brainstorm-vision — Glossary

The skill's **domain model**: one authoritative home for its full vocabulary. Every other
file **bolds the term and points here** rather than restating it. This is disclosed
reference — loaded on demand, self-contained — so it costs nothing until reached.

Terms are grouped by the axis they serve. Each guard/failure term sits beside the lever it
protects. **Bold** marks a cross-reference to another entry.

---

## Divergence — going wide at a fixed altitude

- **Divergence** — the core move of the session: push past the obvious first answers to open
  the **widest possible high-level vision**. A divergent session is never cut short while
  ideas still flow; it ends only at **saturation**. Opposite of converging on a plan or a
  feature set.
- **Breadth axes** — the default coverage set that keeps **divergence** from narrowing to one
  persona or moment: **emotion** (what people feel), **kinds of user** (the whole stakeholder
  chain), and **the whole lifecycle** (before → arrival → acting → finding again → what should
  have been automatic). The floor, not the ceiling — if a product has its own natural axis of
  breadth, name it and drive it too. Walked afresh for each new **rung** during focused
  re-entered divergence.
- **Saturation** — the completion bound for **divergence**: the point where the **breadth
  axes** are genuinely covered and fresh questions only restate ideas already captured. Both
  the floor for going wide *and* the signal the session may wrap. It is checked per **anchor** —
  a **climb** re-opens divergence, so saturation must be re-reached at the new **rung**.
- **Vision point (press release)** — a terse, punchy statement (`V1`, `V2`, …) in the
  future-won voice, capturing the whole-world feeling after the product won, under a short
  narrative lead-in. Fragments are good. What separates it from a **use-case** is *altitude,
  not length*: a vision point speaks to the narrative whole, a use-case pins one persona's
  need. Numbered continuously and **never renumbered** — numbers are references, not positions.
  Sorted under **scope items** (grouped, not renumbered); a point spanning all rungs lives
  under the **anchor**.
- **Use-case** — a plain-language, user-POV need ("As <a kind of user> …, I can finally … /
  I get to …"), numbered `UC1…` continuously and never renumbered. Kept as **one flat list**
  in arrival order — the loose, unsorted shape is load-bearing and deliberately *not* grouped
  by **scope item**.
- **Provisional vision** — the loose north-star draft (one rough lead-in paragraph plus a few
  rough **vision points**) sketched early and kept explicitly editable. Accumulating
  **use-cases** push it around; it is finalized only at the **wrap-up gate**, never before.
- **Scope discipline** *(guard for the vision's purity)* — the rule that **vision points** and
  **use-cases** stay plain language the target audience would nod at: no architecture, modules,
  technology, MVP/versioning, or edge cases. A **rudder, not a muzzle** — wild ideas breathe in
  the *conversation*, but the two captured sections stay pure. Out-of-scope ideas worth keeping
  go to the **parking lot**.
- **Parking lot** *(guard: catches what scope discipline keeps out)* — a separate, flat,
  numbered section (`BV1`, `BV2`, …) holding genuine out-of-scope items *as themselves* — an
  integration, a hard constraint, a tech leaning, an MVP call — in engineer's shorthand (the
  audience test does **not** apply). Entry is gated by the **challenge protocol** (name it +
  two pros/two cons + the human decides). Distinct from the **architecture-significance sweep**,
  which surfaces *use-cases* in plain language; the parking lot captures out-of-scope items the
  moment they arise. Appears only if at least one item was parked.

---

## Scope & altitude — climbing the abstraction ladder (new)

Every product vision is a special case of a higher abstraction level, and that higher level
*pulls* on a divergent session. These terms make each climb a *reviewed decision*, discovered
one rung at a time — never drafted up front, which would anchor the **divergence** toward the
widest framing before the concrete one is exhausted.

- **Ladder** — the chain of abstraction **rungs** the vision could occupy, from the product's
  concrete job upward. Never drafted whole; discovered one **rung** at a time by the
  **scope lens**. A closed ladder is **provisional, not terminal** — the route-back rule can
  reopen it.
- **Rung** — one abstraction level. A **scope item** is a rung *recorded in the file*.
- **Scope item (`S1…Sn`)** — a recorded, in-scope **rung**. `S1` is the product's job as
  settled at session start; each **climb** appends one. Numbered in climb order (= concrete →
  **anchor**), append-only, never renumbered. **Vision points** are sorted under scope items;
  every vision point sits under exactly one.
- **Anchor** — the top **scope item** so far; everything at or below it is in scope.
  **Divergence** runs at the anchor. Moves up exactly one **rung** per **climb**. Carried in
  the per-turn scope steer so a long session remembers *where* the boundary sits, not just
  that there is one.
- **Climb / close** — the two outcomes of a **scope-lens** pass; the pass's completion
  criterion is that the human has explicitly chosen one.
  - **Climb** = accept the proposed **rung**: it becomes the new **anchor** and the next
    `S<n>`, the session **pauses** and re-enters focused **divergence** at the new rung.
  - **Close** = decline it: record the **horizon**, then proceed to the **architecture-
    significance sweep**.
  - *The human decides. Always.*
- **Horizon** — the one **rung** the **scope lens** proposed and the user **closed** on.
  Recorded in the file (`*Beyond the horizon:*`), feeds the sweep's **generalization door**,
  and binds nothing. Provisional: the route-back rule can reopen it as a fresh **climb/close**.
- **Scope signal** *(guard: keeps mid-divergence altitude drift from being acted on
  silently)* — a mid-**divergence** idea that doesn't fit the current **anchor**. Not climbed
  at once: named in one line, run through the **parking-lot** challenge, and if parked tagged
  `(scope signal)` so the **scope lens** finds it as evidence for the next **climb/close**.
- **Scope lens** — the phase (in `scope-lens.md`) that runs at every **saturation**, *before*
  the **architecture-significance sweep**. Proposes exactly **one** **rung** above the current
  **anchor** in plain language and recommends **climb** or **close**, honestly. Mirrors the
  sweep structurally (a deliberate, reviewed pass). Reuses the skill's existing **lens** word
  so the two phases link for free.
- **Generalization door** *(new cross-cutting sweep dimension)* — the **horizon** **rung**
  treated as a **one-way door**: if the declined rung ever becomes real, which decisions made
  for the **anchor** become expensive? (AI-Mail, horizon = "a trusted chief-of-staff for your
  whole life", the declined rung above the "everything that asks something of you" anchor: a
  data model shaped around incoming items to handle vs. one representing your whole life and
  acting on your goals unprompted.) Added to the **architecture-significance sweep**'s
  cross-cutting spine.

---

## Wrap-up — the two-step finalize gate

- **Wrap-up gate** — the two-step gate that ends a saturated session; never jump straight to
  finalizing. Step 1 is the **architecture-significance sweep**; step 2 is finalize (read-back,
  strip **resume notes**, rename `*.wip.md` → `*.md`, reconcile references, turn the steering
  flag off). Reached only once the **ladder** is **closed** and the sweep surfaced no
  scope-significant use-case that reopened it.
- **Architecture-significance sweep** — step 1 of the **wrap-up gate**, the last completeness
  backstop. Uses architecture as a *lens, not a layer*: think in architecturally-loaded terms
  privately, capture only plain-language **use-cases**. Builds a reviewed, saved lens
  (`<slug>-architecture-lens.md`) from the template, then walks it to **saturation**, hunting
  **use-cases** behind **one-way-door** decisions. **Route-back rule**: a surfaced use-case
  that only makes sense one **rung** up is *not* appended — it is handed back to the **scope
  lens** as a **scope signal**, reopening the **climb/close** gate.
- **One-way door** — the sweep's invariant: a decision *cheap to make now, expensive to
  discover after building starts* — the architecture, platform, data model. What the
  **architecture-significance sweep** hunts. The **generalization door** is one such door
  applied to the **horizon**.

---

## Session state — pause, resume, steering, the working file

- **`.wip.md`** — the working file's suffix (`<slug>-foundation-vision.wip.md`) while the
  session is unfinished. An on-disk `*.wip.md` *is* a paused, resumable session. Renamed to
  drop `.wip` only at final finalize.
- **Resume notes** — a `## Resume notes` section holding just enough session state to pick up
  cleanly; stripped at finalize. It marks which of **four** states the session is in, which
  determines where a resume re-enters:

  | Resume-notes state | Resume enters |
  |---|---|
  | checkpoint / break, **divergence** not saturated | diverge, same **anchor** |
  | **scope widened to `S<n>`** | diverge, focused on the new **rung** |
  | **divergence** saturated, wrap-up agreed, **ladder** open | **scope lens** |
  | ready to finalize (sweep done) | finalize step 2 |
- **Scope steering** — a `UserPromptSubmit` hook (gated by a flag file, toggled on/off by
  rename) that re-injects the scope boundary every turn to counter **context rot**. Turned ON
  at session start, OFF at every pause/session-end. Its steer text now also carries the current
  **anchor**, refreshed on each **climb**. Mechanics live in `scope-steering.md` /
  `scope_boundary.md` / `scope-steer.sh`.
