# Product Vision

**Status:** Second draft

A product vision describes the future change the product is intended to create. It aligns discovery without freezing a feature list or prescribing an architecture.

The vision is not the product strategy: the vision names the destination, the strategy the path — which outcomes, segments, and opportunities to pursue in which order. Strategy changes far more often than the vision. Record it as a thin ordered-outcomes layer alongside the vision (see [Strategy and roadmap](#strategy-and-roadmap) below); it is exercised through opportunity selection and prioritization in [product discovery](./product_discovery.md) and [product definition](./product_definition.md).

Terms used here are defined in the [glossary](./glossary.md).

## Questions the vision should answer

- Who experiences the problem or opportunity?
- In what situation does it arise?
- What progress should become possible?
- Why does that change matter to users and to the organization?
- What makes this product distinct?
- Which principles must guide trade-offs?
- What is outside the intended product?
- What evidence would show that the vision is becoming real?

## Recommended structure

### 1. Context

Describe the present situation and why it deserves attention. Separate observed facts from interpretations and assumptions.

### 2. Actors and beneficiaries

Identify users, customers, operators, administrators, regulators, and affected non-users. Do not collapse people with different goals into a generic “user.”

### 3. Desired change

Describe the improved future from the actor's point of view. Prefer outcomes over solution language.

### 4. Value and differentiation

Explain why the change is valuable and why the proposed product could provide it better than current alternatives, including manual work and doing nothing.

### 5. Product principles

Record durable rules that guide later choices, for example:

- The user remains in control of consequential actions.
- Every automated decision can be explained and audited.
- The product should fit the existing workflow before asking users to replace it.

### 6. Scope boundaries

State what the product intends to become, what it will not become, and which adjacent opportunities are explicitly deferred.

### 7. Outcomes and signals

Define outcome measures, guardrail measures, and qualitative signals. Avoid treating shipped features or usage alone as proof of value. These measures are what [validation and feedback](./validation_and_feedback.md) checks after release — a vision whose outcomes cannot be observed cannot be validated.

### 8. Strategy (ordered outcomes)

Keep strategy thin: an ordered list of *outcome — target segment — why this order*. Each entry cites the `V#`/`S#` vision items it serves. The list is a field set inside the foundation vision rather than a new ID family, standalone strategy artifact, skill, or lifecycle stage; a legitimately unresolved list is an explicit `OPEN:` section.

## Lightweight vision template

```markdown
# <Product> Foundation Vision

## Present situation
<Who is struggling, in what context, and what evidence do we have?>

## Desired future
<What becomes easier, safer, faster, or newly possible?>

## Actors
<Actor — goal — current obstacle>

## Value proposition
<Why this change matters and why this approach is promising>

## Product principles
- ...

## In scope
- ...

## Outside the vision
- ...

## Outcomes and signals
- Outcome: ...
  Signal: ...
  Guardrail: ...

## Critical assumptions
- ...

## Strategy (ordered outcomes)
1. <outcome — target segment — why this order>
2. ...
```

## Strategy and roadmap

The strategy section of the vision one-pager answers "what beyond the next slice": an ordered list of the outcomes and target segments on the path to the vision. Reordering it when discovery or validation evidence demands is a routine discovery pivot, not a vision pivot; record the reorder as a `DEC#`, update the section through its accountable human owner, and refresh the derived companion index.

Where coordination cost, sponsor communication, or product lifetime warrants the ceremony, expand the strategy into a **product roadmap**: an outcome-based, rolling now/next/later view, revised as evidence arrives. Never commit features and dates. Whether to adopt the roadmap artifact at all is a [lifecycle tailoring](./lifecycle_tailoring.md) decision; low-ceremony topics skip it and rely on the strategy list and the decision log's recorded deferrals.

## Ways to develop the vision

- **Vision narrative:** tell a concrete before-and-after story from a user's viewpoint.
- **Press release:** announce the future product in plain language and explain why it matters.
- **Jobs to Be Done:** phrase the stable progress sought independently of a particular solution.
- **Product principles workshop:** turn recurring trade-offs into explicit decision rules.
- **Premortem:** imagine the product failed and expose assumptions or missing constraints.

## Completion checks

- A reader can explain the intended user change without reciting features.
- Important actors and conflicting interests are visible.
- Evidence, assumptions, and aspirations are distinguishable.
- Principles are specific enough to resolve a real trade-off.
- Scope exclusions prevent obvious interpretations that would derail discovery.
- Success signals describe changed outcomes, with guardrails against harmful optimization.

The vision should be stable enough to orient work but revisable when its underlying evidence changes. Expect frequent discovery pivots — changed opportunities, solutions, scope, and strategy — under a stable vision; they must not silently edit the vision. A vision pivot is rare and is permitted only through an explicit `DEC#` citing evidence that invalidates the intended future or target need, not a weak feature or failed experiment. The vision workflow cites that loop decision; it does not fabricate it.

## Further material

**Examples:**

- A field-service startup writes a one-page vision: solo electricians lose their evenings to paperwork; the intended change is "the invoice is sent before the van leaves the driveway," with the principle "never make the tradesperson learn accounting vocabulary." The principle later settles a real dispute about whether to expose VAT ledger codes in the UI.
- A team drafts an internal press release announcing the finished product two years out. Writing the customer quote proves impossible without the word "dashboard" — a signal that the vision is feature-shaped rather than outcome-shaped, and needs another pass.

**References:** [Product Vision Board — Roman Pichler](https://www.romanpichler.com/tools/product-vision-board/); [Product Vision FAQ — Silicon Valley Product Group](https://www.svpg.com/product-vision-faq/); [Amazon Working Backwards — product-frameworks.com](https://www.product-frameworks.com/Amazon-Working-Backwards.html).

**Agent rule sets:** [`deanpeters/Product-Manager-Skills`](https://github.com/deanpeters/Product-Manager-Skills) — **license: CC BY-NC-SA 4.0 (non-commercial, share-alike — do not distill content into skills)**; battle-tested PM skill framework (workflow, interactive, and foundation tiers) including a `press-release` skill that applies Amazon Working Backwards to clarify the vision before any spec; [`phuryn/pm-skills`](https://github.com/phuryn/pm-skills) — large, actively maintained PM skill marketplace covering vision, strategy, and positioning alongside discovery and launch.

**Books:** *Inspired* — Marty Cagan; *Working Backwards* — Colin Bryar, Bill Carr; *Strategize* — Roman Pichler.
