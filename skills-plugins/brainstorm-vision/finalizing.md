# brainstorm-vision — Finalize

Read this **only once the divergent phase has reached saturation** (see [`brainstorming.md`](brainstorming.md)) and wrap-up is agreed. This is the wrap-up gate.

<wrap-up-gate>

Wrap-up is a **two-step gate — never jump straight to finalizing.**

- **Step 1 — Architecture-significance sweep (automatic).** Before finalizing, run the sweep without being asked. See below. When it reaches saturation the session is **ready to finalize** — say so, then move to step 2.
- **Step 2 — Finalize.** Re-read the file, read the vision, the full use-case list, and any parked items back to the user for a final sanity pass, invite cuts/merges/sharpening, then **finalize**:
  - strip any `## Resume notes` section;
  - rename `<name>.wip.md` → `<name>.md` so the final artifact obeys the format (Vision and Use-cases, plus the `## Beyond the vision (parking lot)` section if anything was parked);
  - if use-cases changed since step 1, reconcile the `<slug>-architecture-lens.md` artifact's `UC<n>` cross-references so they still point at the right use-cases;
  - rename the steering flag to `_off` (see [`scope-steering.md`](scope-steering.md)).

</wrap-up-gate>

<architecture-significance-sweep>

Step 1 of the gate, and the last completeness backstop before finalizing. The vision stayed deliberately out of architecture — but some user needs, if they only surface *after* building has begun, force expensive rework of one-way-door decisions: the overall architecture, the software design, the platform/language, the data model. This sweep catches the use-cases behind those decisions while changing them is still free.

**It is a lens, not a layer.** Think in architecturally-loaded terms privately; capture only what an ordinary user would say. Everything kept is still a plain user-POV use-case ("As someone …, I can finally …") — never a note about offline-sync, schemas, hosting, or tenancy. Scope discipline holds in full; you are only aiming the divergence at corners that are cheap to decide now and dear to change later. (If the sweep surfaces a genuine architecture *constraint* rather than a use-case — something the build phase must honour — that's a parking-lot item, not a use-case; run the parking-lot challenge on it instead. See Parking lot in [`brainstorming.md`](brainstorming.md).)

**Method — build the product's lens, then walk it.**

1. **Build the lens (explicit, reviewed, saved).** Open [`architecture-significance-lens-template.md`](architecture-significance-lens-template.md) — the seed, not the product's lens. Its invariant is the one-way-door test — *which decisions are cheap now and expensive to discover after building starts?* Using the template's dimensions as seeds, derive the axis list for *this specific* product: **first actively generate its own one-way doors from the invariant** — the defining door is often one no list names — then walk the cross-cutting spine and the fitting family cluster as a backstop to catch what you missed. **Play the derived axes back to the user** — keep/sharpen/drop — so the lens is reviewed, not improvised. Do this only now, at wrap-up: deriving it earlier would pull architecture thinking into the divergent phase and anchor the vision. Write the agreed lens to a **separate build-phase artifact**, `<output-dir>/<slug>-architecture-lens.md` (engineer shorthand, like the parking lot — *not* end-user language) — but if that file already exists (a resumed or re-opened session), **read it first and extend/reconcile it**, never overwrite. It is a sibling of the vision file and a handoff to the next phase; it **never** enters the vision file's Vision/Use-cases sections, which stay pure.

2. **Walk the lens.** For each agreed axis, ask yourself: *is there a user whose need on this axis we haven't captured yet?* If so, offer one candidate use-case in plain language and let the user keep, sharpen, or drop it — new use-cases re-open brief divergence on those axes. These axes overlap the three breadth axes (emotion / kinds of user / lifecycle) but cut a different way. Keep sweeping until the lens reaches **saturation** — that's the signal step 1 is done and the session is ready to finalize.

</architecture-significance-sweep>

<lens-artifact-format>

The architecture-lens artifact (`<slug>-architecture-lens.md`) is a *separate* sibling file, written at wrap-up (step 1), never mixed into the vision file. It holds the product's derived one-way-door axes for the build phase — engineer shorthand, **not** end-user language (same audience as the parking lot). One flat section:

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
