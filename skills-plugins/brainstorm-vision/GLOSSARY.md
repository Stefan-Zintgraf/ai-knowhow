# brainstorm-vision — Glossary

The skill's **domain model** — one authoritative home for its vocabulary, grouped by the axis
each term serves. Each guard/failure term sits beside the lever it protects. **Bold** = a
cross-reference to another entry.

---

## Divergence — going wide at a fixed altitude

- **Divergence** — the core move: push past the obvious first answers to open the **widest
  possible high-level vision**. Never cut short while ideas still flow; ends only at
  **saturation**.
- **Breadth axes** — the default coverage set that keeps **divergence** from narrowing to one
  persona or moment: **emotion** (what people feel), **kinds of user** (the whole stakeholder
  chain), and **the whole lifecycle** (before → arrival → acting → finding again → what should
  have been automatic). A floor, not a ceiling — add a product's own natural axis of breadth if
  it has one. Walked afresh for each new **rung**.
- **Saturation** — the completion bound for **divergence**: the **breadth axes** are genuinely
  covered and fresh questions only restate ideas already captured. Both the floor for going
  wide *and* the signal the session may wrap. Checked per **anchor** — a **climb** re-opens
  divergence, so saturation must be re-reached at the new **rung**.
- **Vision point (press release)** — a terse, punchy statement (`V1`, `V2`, …) in the
  future-won voice, capturing the whole-world feeling after the product won, under a short
  narrative lead-in. Fragments are good. Differs from a **use-case** by *altitude, not length*.
  Mechanics in `brainstorming.md`'s *Numbering & sorting*.
- **Use-case** — a plain-language, user-POV need ("As <a kind of user> …, I can finally … /
  I get to …", numbered `UC1…`). Kept as **one flat list in arrival order** — unsorted.
  Mechanics in `brainstorming.md`'s *Numbering & sorting*.
- **Provisional vision** — the loose north-star draft (one rough lead-in paragraph plus a few
  rough **vision points**) sketched early and kept explicitly editable. Accumulating
  **use-cases** push it around; finalized only at the **wrap-up gate**, never before.
- **Scope discipline** *(guard for the vision's purity)* — **vision points** and **use-cases**
  stay plain language the target audience would nod at: no architecture, modules, technology,
  MVP/versioning, or edge cases. A **rudder, not a muzzle** — wild ideas breathe in the
  *conversation*, but the two captured sections stay pure. Out-of-scope keepers go to the
  **parking lot**.
- **Parking lot** *(guard: catches what scope discipline keeps out)* — a separate, flat,
  numbered section (`BV1`, `BV2`, …) holding genuine out-of-scope items *as themselves* — an
  integration, a hard constraint, a tech leaning, an MVP call — in engineer's shorthand (the
  audience test does **not** apply). Entry is gated by the **challenge protocol** (name it +
  two pros/two cons + the human decides). Unlike the **architecture-significance sweep** (which
  surfaces *use-cases*), the parking lot captures out-of-scope items the moment they arise.
  Appears only if at least one item was parked.

---

## Scope & altitude — climbing the abstraction ladder

**Rungs** are discovered one at a time by the **scope lens**, never drafted up front — drafting
the whole ladder would anchor **divergence** at the widest framing before the concrete one is
exhausted. Each climb is a *reviewed decision*.

- **Ladder** — the chain of abstraction **rungs** the vision could occupy, from the product's
  concrete job upward. Discovered one **rung** at a time by the **scope lens**, never whole. A
  closed ladder is provisional — the route-back rule can reopen it.
- **Rung** — one abstraction level. A **scope item** is a rung *recorded in the file*.
- **Scope item (`S1…Sn`)** — a recorded, in-scope **rung**. `S1` is the product's job as
  settled at session start; each **climb** appends one. Numbered in climb order (= concrete →
  **anchor**), append-only, never renumbered. **Vision points** are sorted under scope items;
  every vision point sits under exactly one.
- **Anchor** — the top **scope item** so far; everything at or below it is in scope.
  **Divergence** runs at the anchor. Moves up exactly one **rung** per **climb**. Carried in
  the per-turn scope steer.
- **Climb / close** — the two outcomes of a **scope-lens** pass; the pass completes only once
  the human has explicitly chosen one.
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
- **Scope lens** — the phase (`scope-lens.md`) that runs at every **saturation**, *before* the
  **architecture-significance sweep**. Proposes exactly **one rung** above the current
  **anchor** in plain language and recommends **climb** or **close**, honestly.
- **Generalization door** *(cross-cutting sweep dimension)* — the **horizon** **rung** treated
  as a **one-way door**: if the declined rung ever becomes real, which decisions made for the
  **anchor** become expensive? (E.g. a task manager whose horizon is "runs your whole work
  life" but whose anchor is "tracks your open tasks": a data model shaped around discrete tasks
  vs. one representing goals and acting unprompted.) Added to the **architecture-significance
  sweep**'s cross-cutting spine.

---

## Wrap-up — the two-step finalize gate

- **Wrap-up gate** — the two-step gate that ends a saturated session; never jump straight to
  finalizing. Step 1 is the **architecture-significance sweep**; step 2 is finalize (mechanics
  in `finalizing.md`). Reached only once the **ladder** is **closed** and the sweep surfaced no
  scope-significant use-case that reopened it.
- **Architecture-significance sweep** — step 1 of the **wrap-up gate**, the last completeness
  backstop. Uses architecture as a *lens, not a layer*: think in architecturally-loaded terms
  privately, capture only plain-language **use-cases**. Builds a reviewed, saved lens
  (`<slug>-architecture-lens.md`) from the template, then walks it to **saturation**, hunting
  **use-cases** behind **one-way-door** decisions. **Route-back rule**: a surfaced use-case
  that only makes sense one **rung** up is *not* appended — it is handed back to the **scope
  lens** as a **scope signal**, reopening the **climb/close** gate.
- **One-way door** — the sweep's invariant: a decision *cheap to make now, expensive to
  discover after building starts* — architecture, platform, data model. What the
  **architecture-significance sweep** hunts. The **generalization door** is one such door
  applied to the **horizon**.

---

## Session state — pause, resume, steering, the working file

- **`.wip.md`** — the working file's suffix (`<slug>-foundation-vision.wip.md`) while the
  session is unfinished. An on-disk `*.wip.md` *is* a paused, resumable session. Renamed to
  drop `.wip` only at final finalize.
- **Resume notes** — a `## Resume notes` section holding just enough session state to pick up
  cleanly; stripped at finalize. Marks which of **four** states the session is in, which
  determines where a resume re-enters — see the table in `SKILL.md`'s Pause and resume section.
- **Scope steering** — a hook that re-injects the scope boundary (carrying the current
  **anchor**) every turn to counter **context rot**. ON at session start, OFF at every
  pause/session-end. Mechanics in `scope-steering.md` / `scope_boundary.md` / `scope-steer.sh`.
- **Use-case cap** *(guard: bounds a single sitting)* — the sole mid-session checkpoint
  control: a hard, human-configured limit (in `config.md`, key `max_new_use_cases`, with a
  companion `warn_before` for advance notice) that forces a checkpoint **pause** once that many
  **use-cases** have been newly added in the current sitting. Off / absent = no cap; the session
  runs to natural **saturation**. Enforcement mechanics in `usecase-cap.md` / `usecase-cap.sh`.
