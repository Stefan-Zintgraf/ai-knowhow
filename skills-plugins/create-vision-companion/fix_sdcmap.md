# FIX: `subdomains-and-context-map.md` allows contradictory paired context-map labels

**Status:** open — deferred fix (do NOT fix mid-run; captured during a Phase 11 review, 2026-07-09).
**Affected output file:** `subdomains-and-context-map.md` (the S7 artifact).
**Severity:** medium — produces a self-contradictory strategic-design tag and an un-loadable file, both survive the per-phase critic today.

---

## Symptom (what was observed)

In a produced bundle, the **Context-map relationships** table tagged six boundary rows
**`Conformist + ACL`** (external mail provider, chat providers, system-of-record read,
silent portal, world-events feed, omni-format sources).

`Conformist` and `Anticorruption Layer (ACL)` are **mutually-exclusive** responses to the
same situation (an upstream you cannot influence):

- **Conformist** — you adopt the upstream model *wholesale, with no translation layer*; the
  foreign model is allowed into your context.
- **ACL** — you build a *translation layer* precisely so the foreign model does **not** enter
  your context.

Building an ACL is the act of *refusing* to be a Conformist. So `Conformist + ACL` is
contradictory at a single altitude. It is also an **altitude slip**: the row punted the
Conformist-vs-ACL choice to "the architecture phase to confirm," but choosing the context-map
relationship is a **strategic-design** decision (Evans, *DDD* Part IV / Ch. 14, Context
Mapping) — it is *this bundle's* job, not the tactical/architecture phase's. Only the ACL's
*implementation* (adapters/facades/translators) is tactical and correctly deferred.

## Root cause (two defects in the skill)

1. **No single-pattern-per-boundary rule + no decision rule.**
   - `strategies.md` S7 part 2 (≈ lines 107–111) lists the vocabulary and says a mail-provider
     boundary is "*likely Conformist or ACL*" but never states the two are exclusive, and gives
     no rule for choosing between them.
   - `templates.md` Context-map section (≈ lines 211–221) seeds the bug directly: the example
     row (line 221) shows a cell literally reading **`Conformist / ACL`**, which invites a
     paired tag.
   - `rubrics-1-8.md` Phase 5 critic checks (≈ lines 78–80) have a generic "Right readings"
     gate but **no gate that rejects a contradictory paired/hybrid relationship label**, so the
     defect passes every per-phase and whole-bundle critic.

2. **No legend requirement → file is not independently loadable.**
   The template names the fixed DDD vocabulary (Partnership, Shared Kernel, Customer/Supplier,
   Conformist, ACL, Open Host Service, Published Language, Separate Ways) but never requires the
   output file to **define** those patterns. A reader without DDD background cannot decode the
   tags from the bundle alone — a violation of the "independently loadable" gate. (The patterns
   are DDD *method* vocabulary, so they correctly stay OUT of `glossary.md`, which holds the
   *product's* ubiquitous language; the definitions belong in a legend inside
   `subdomains-and-context-map.md` itself.)

## How to fix

### Fix 1 — enforce exactly one relationship pattern per boundary
- **`strategies.md` S7 part 2:** state that each boundary gets **exactly one** pattern from the
  fixed vocabulary (they are mutually exclusive), and add the decision rule:
  > *Any boundary where the foreign payload is wrapped/translated into our own model = **ACL**.
  > A boundary where we genuinely adopt the upstream model with no translation = **Conformist**.
  > Choosing the relationship is a strategic decision made here; only its implementation is
  > deferred to the architecture phase.*
  A composite boundary that genuinely differs by direction may name **read vs write separately**
  (e.g. "ACL to read; Customer/Supplier to write") — that is two boundaries, not one hybrid tag.
- **`templates.md` Context-map section (line ~221):** change the example cell from
  `Conformist / ACL` to a single value (e.g. `ACL`) and add a note: "one pattern per row; no
  `X + Y` hybrids."

### Fix 2 — add a Phase 5 critic gate
- **`rubrics-1-8.md` Phase 5 critic checks:** add a gate, e.g.
  > *Each context-map boundary carries **exactly one** relationship pattern from the fixed
  > vocabulary. Reject any contradictory/hybrid label (e.g. `Conformist + ACL`) — resolve it to
  > the single correct pattern via the S7 decision rule and log the call to `decisions.md`.*

### Fix 3 — require a pattern legend (independently-loadable)
- **`templates.md` Context-map section:** require the output file to include a one-line-per-
  pattern **legend** defining each DDD relationship pattern it uses, so the file stands alone.
- Optionally add a matching bullet to the Phase 5 / Phase 9 "independently loadable" checks.

## Cross-reference

Surfaced while reviewing **decision row 24** of the `ai-mail-vision-ai-spec` bundle
(`docs/brainstorming/ai-mail-vision-ai-spec/`). Row 24 only cited 3 of the 6 affected
boundaries — a reminder that the fix should also make the builder cite **every** affected
boundary when it logs such a call, not a subset.
