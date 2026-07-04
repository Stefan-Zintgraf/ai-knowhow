# brainstorm-vision — Finalize

The **wrap-up gate** (see [`GLOSSARY.md`](GLOSSARY.md)) for a saturated **divergence** session. Entered **only via a closed ladder** — from the **scope lens**'s **close** ([`scope-lens.md`](scope-lens.md)), or a resume marked **"ready to finalize, sweep done, ladder closed"**. Never reached from an open **ladder**, and never jumped to straight from **saturation**.

<wrap-up-gate>

Wrap-up is a **two-step gate — never jump straight to finalizing.**

- **Step 1 — Architecture-significance sweep (automatic).** Before finalizing, run the **architecture-significance sweep** (see below and [`GLOSSARY.md`](GLOSSARY.md)) without being asked. When it reaches **saturation** *and* has surfaced no scope-significant use-case that reopened the **ladder** (see the route-back rule below), the session is **ready to finalize** — say so, then move to step 2.
- **Step 2 — Finalize.** Re-read the file and read it back to the user for a final sanity pass — the **vision points** grouped under their **scope items**, the full flat **use-case** list, and any **parked** items — invite cuts/merges/sharpening, then **finalize**:
  - **Walk the scope section:** every **vision point** sits under the right `S<n>` **scope item**, no scope item is empty, and the `*Beyond the horizon:*` line is present. Fix any point filed under the wrong item (keep its number).
  - strip any `## Resume notes` section;
  - rename `<name>.wip.md` → `<name>.md` so the final artifact obeys the format (`## Vision scope`, grouped Vision points, flat Use-cases, plus the `## Beyond the vision (parking lot)` section if anything was parked);
  - if use-cases **or scope items** changed since step 1, reconcile the `<slug>-architecture-lens.md` artifact's `UC<n>` **and** `S<n>` cross-references so they still point at the right use-cases and scope items;
  - rename the steering flag to `_off` (see [`scope-steering.md`](scope-steering.md)).

</wrap-up-gate>

<architecture-significance-sweep>

Step 1 of the **wrap-up gate**, and the last completeness backstop before finalizing. The vision stayed deliberately out of architecture — but some user needs, if they only surface *after* building has begun, force expensive rework of **one-way-door** decisions. The **architecture-significance sweep** catches the **use-cases** behind those doors while changing them is still free. (Terms: [`GLOSSARY.md`](GLOSSARY.md).)

**It is a lens, not a layer.** Think in architecturally-loaded terms privately; capture only what an ordinary user would say. Everything kept is still a plain user-POV use-case ("As someone …, I can finally …") — never a note about offline-sync, schemas, hosting, or tenancy. **Scope discipline** (see [`GLOSSARY.md`](GLOSSARY.md)) holds in full; you are only aiming the divergence at the one-way doors. (If the sweep surfaces a genuine architecture *constraint* rather than a use-case — something the build phase must honour — that's a **parking-lot** item, not a use-case; run the parking-lot challenge on it instead. See Parking lot in [`brainstorming.md`](brainstorming.md).)

**Method — build the product's lens, then walk it.**

1. **Build the lens (explicit, reviewed, saved).** Open [`architecture-significance-lens-template.md`](architecture-significance-lens-template.md) — the seed, not the product's lens; its invariant is the one-way-door test. Derive the axis list for *this specific* product: **first actively generate its own one-way doors from the invariant**, then walk the cross-cutting spine and the fitting family cluster as a backstop to catch what you missed. The spine now includes the **generalization door** — the **horizon** rung the scope lens closed on, treated as a one-way door; walk it like any other axis (defined in the template, see [`architecture-significance-lens-template.md`](architecture-significance-lens-template.md) and [`GLOSSARY.md`](GLOSSARY.md)). **Play the derived axes back to the user** — keep/sharpen/drop — so the lens is reviewed, not improvised. Do this only now, at wrap-up: deriving it earlier would pull architecture thinking into the divergent phase and anchor the vision. Write the agreed lens to a **separate build-phase artifact**, `<output-dir>/<slug>-architecture-lens.md` (engineer shorthand, like the parking lot — *not* end-user language) — but if that file already exists (a resumed or re-opened session), **read it first and extend/reconcile it**, never overwrite. It is a sibling of the vision file and a handoff to the next phase; it **never** enters the vision file's Vision points/Use-cases sections, which stay pure.

2. **Walk the lens.** For each agreed axis, ask yourself: *is there a user whose need on this axis we haven't captured yet?* If so, offer one candidate use-case in plain language and let the user keep, sharpen, or drop it — new use-cases re-open brief divergence on those axes. These axes overlap the three **breadth axes** (emotion / kinds of user / lifecycle) but cut a different way. This is a **stateful walk kept in a single fresh context** — one axis at a time, not one fresh session per use-case (which would only force repeated re-reads of the vision + lens artifact). Keep sweeping until the lens reaches **saturation** — that, *plus* the route-back check below coming up empty, is the signal step 1 is done and the session is ready to finalize.

3. **Route-back rule — a scope-significant use-case reopens the ladder through the scope lens.** If a use-case the sweep surfaces is **scope-significant** — it only makes sense one **rung** above the current **anchor** — do **not** append it here, and do **not** force it into the vision below its natural altitude. Hand it back to the **scope lens** as a **scope signal**: re-enter [`scope-lens.md`](scope-lens.md) at its `<one-rung-proposal>` section and re-propose that rung as a fresh **climb/close** decision (the **ladder**'s close was provisional, not terminal).
   - **Climb** → the normal climb pause fires: the session pauses and re-enters focused **divergence** at the new rung ([`scope-lens.md`](scope-lens.md) `<climb>`). The sweep resumes only after that rung saturates and closes.
   - **Close** (declined again) → the use-case is dropped or **parked**, never appended below its altitude.

   This is the one loop between the two lenses: the sweep can reopen a closed ladder, but **only through the scope lens's climb/close gate** — never by silently widening scope itself. Finalize (step 2) is reached only when the ladder is closed *and* the sweep produced no scope-significant use-case that reopened it.

</architecture-significance-sweep>

<lens-artifact-format>

The artifact's shape — one flat section:

```markdown
# <Product> — Architecture lens

Derived at vision wrap-up. The one-way-door axes for this product — decisions
cheap to make now, expensive to discover after building starts — each with the
user need behind it. Build-phase handoff; not part of the vision.

- **<axis>** — <the one-way-door decision it forces> · surfaced by UC<n>, UC<n>
- …
```

Cross-reference each axis to the use-case numbers it surfaced (`UC<n>`) so the lens ties back to the vision's use-cases without restating them.

</lens-artifact-format>
