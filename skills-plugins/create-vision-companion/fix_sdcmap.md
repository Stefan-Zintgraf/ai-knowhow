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

Leading word for all three sites: the relationship vocabulary is an **enum** — a closed set,
exactly one value per boundary. One token carries "mutually exclusive, no hybrids, no free-form
labels" everywhere it appears.

### Fix 1 — `strategies.md` S7 part 2: the enum rule + decision rule (single source of truth)
State that the vocabulary is an **enum**: each boundary takes exactly one value (the patterns
are mutually exclusive responses to a boundary), and add the decision rule:
> *Any boundary where the foreign payload is wrapped/translated into our own model = **ACL**.
> A boundary where we genuinely adopt the upstream model with no translation = **Conformist**.
> Choosing the relationship is a strategic decision made here; only its implementation is
> deferred to the architecture phase.*

A boundary that genuinely differs by direction is **two rows** (e.g. "ACL to read;
Customer/Supplier to write"), never one hybrid tag. The rule lives **only here**; the template
and rubric conform to it or point at it — they do not restate it.

### Fix 2 — `templates.md` section 6: conforming example + shipped legend
- Change the example cell (line ~221) from `Conformist / ACL` to a single value (`ACL`).
  No accompanying rule text — the rule is Fix 1's; a corrected example plus the enum
  pre-check (Fix 3) covers the template's share.
- Add a **Legend** block to the skeleton with the eight one-line pattern definitions
  **pre-written verbatim** (builder deletes unused rows, or keeps all eight). Shipping the
  text instead of requiring the builder to write it removes generation variance, makes the
  file independently loadable, and puts the Conformist/ACL one-liners — which encode the
  decision rule — at the point of use. (Method vocabulary, so it stays out of `glossary.md`,
  which holds the *product's* ubiquitous language.)

### Fix 3 — `rubrics-1-8.md` Phase 5: extend the mechanical pre-check (not a new critic gate)
"Exactly one pattern" is decidable by inspection, so it belongs in the existing
**Pre-check (mechanical)** line, not a judgment gate. Extend it:
- every `Relationship` cell is **exactly one enum value** (no `/`, `+`, or free-form text);
- no row pairs `Conformist` with `Translation needed? = yes` (translation ⟹ ACL, per S7);
- the legend covers every pattern used.

No new critic gate: whether the single value chosen is *right* is the existing
**Right readings** gate, now decidable via the S7 rule. When a hybrid is resolved, the
`decisions.md` row must cite **every** affected boundary, not a subset.

### Non-fix
The "independently loadable" gate exists only in Phases 9/10 (`rubrics-9-12.md`) — Phase 5 has
none, and none is needed: the legend lives in the template skeleton (Fix 2) and its presence is
mechanically pre-checked (Fix 3), so the generic Phase 9/10 gate needs no new bullet.

## Cross-reference

Surfaced while reviewing **decision row 24** of the `ai-mail-vision-ai-spec` bundle
(`docs/brainstorming/ai-mail-vision-ai-spec/`). Row 24 only cited 3 of the 6 affected
boundaries — the origin of Fix 3's cite-every-boundary clause.
