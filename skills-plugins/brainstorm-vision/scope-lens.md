# brainstorm-vision — Scope lens

The **scope lens** (see [`GLOSSARY.md`](GLOSSARY.md)) pass for a saturated **divergence** session. It runs at **every** **saturation**, once wrap-up is agreed, **before** any finalize handoff — never jump from saturation straight to [`finalizing.md`](finalizing.md). Only a **closed** **ladder** proceeds to the wrap-up gate.

<one-rung-proposal>

**Propose exactly one rung — never a ladder.**

1. **Privately** consider what the current **anchor** is a special case of — the next level of abstraction up. Draw on the accumulated **scope signals** parked with the `(scope signal)` tag and on any **use-cases** already straining the anchor (needs the current scope can't quite hold). These are the evidence for where the vision *wants* to grow.
2. Pick the **one** most natural next **rung**. One only. Never present a full **ladder**, never sketch two rungs "to compare" — a full ladder drafted here anchors the divergence just as drafting it up front would.
3. Present that rung in **plain language**, with a *taste of the territory* it would unlock: two or three one-line sketches of the kind of **use-case** that becomes possible once the anchor widens to it. Enough for the human to feel the reach, not a diverged list.
4. Recommend **climb** or **close** — honestly, on the evidence. Say which you'd pick and why; the strength of the scope signals is the tell.

**The human decides. Always.**

</one-rung-proposal>

<climb>

**Climb** — the human accepts the proposed **rung**:

1. Append the rung as the next **scope item** `S<n>` in `## Vision scope` — it becomes the new **anchor**. Append-only, never renumber (see the format rules in [`brainstorming.md`](brainstorming.md)).
2. Update the anchor lead-in of `## Vision scope` to name the new anchor.
3. Re-file any parked **scope signals** that now fit *inside* the new anchor — promote each from the **parking lot** into a proper **use-case** or **vision point** at its natural altitude (keep numbers; file points under the anchor group).
4. **Pause** — write `## Resume notes` marking **"scope widened to `S<n>`, divergence NOT saturated at the new scope — resume re-enters diverge focused on the new rung"**, then do the **fresh-context handoff** ([`SKILL.md`](SKILL.md) step 3).

Do not read [`finalizing.md`](finalizing.md) on a climb — a climbed ladder is still open.

</climb>

<close>

**Close** — the human declines the proposed **rung**:

1. Record the declined rung as the **horizon** line in `## Vision scope`: `*Beyond the horizon:* <the rung, one line>` — named so the build phase keeps the door open, explicitly **not** part of this vision. It feeds the sweep's **generalization door** and binds nothing.
2. Proceed to the existing wrap-up handoff — the fresh-session finalize gate ([`finalizing.md`](finalizing.md)), **unchanged**. The ladder is now **closed** (provisional, not terminal: the sweep's route-back rule can reopen it).

</close>

<completion-criterion>

The scope-lens pass ends **only** when **one** **rung** has been proposed in plain language **and** the human has explicitly chosen **climb** or **close**. Not "the scope feels right" — that is fuzzy and gives way to **premature completion** (declaring scope settled just to reach finalize). On **close**, the **horizon** line being written **is** the proof the pass is done.

</completion-criterion>
