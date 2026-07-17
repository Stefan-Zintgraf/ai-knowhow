# Product Definition

**Status:** First draft

Product definition turns discovery evidence and strategy into a coherent scope: which opportunities to pursue now, which capabilities the product must provide, which journeys those capabilities serve, and in what order. It sits between discovery and requirements — discovery establishes what is worth pursuing, definition commits to what will be pursued next, and requirements makes the committed behavior precise.

Terms used here are defined in the [glossary](./glossary.md).

## Inputs

- [Product vision](./product_vision.md) and its strategy: direction, principles, scope boundaries, and the ordered outcomes the next investment should serve
- [Lifecycle tailoring](./lifecycle_tailoring.md): whether the optional roadmap was adopted or skipped, and why
- [Discovery](./product_discovery.md) evidence: opportunities, tested assumptions, experiment results
- [Domain discovery](./domain_discovery.md) outputs where they exist: capability map, domain glossary
- Constraints: dates, budgets, contracts, platform commitments

## Core activities

### 1. Select opportunities

Choose which validated opportunities the next investment addresses. Check the selection against the strategy's ordered outcomes: a selection that fights the strategy needs an explicit `DEC#` recording a strategy reorder or a deliberate exception (and a roadmap update where one exists), not silent reordering or divergence. Strategy reordering is a discovery pivot, never a silent vision edit. Record which opportunities are deferred and why — an unrecorded deferral gets re-litigated in every planning conversation.

### 2. Define capabilities

Name what the product must enable, in solution-neutral capability language: "share a document with revocable access," not "add a revoke button to the sharing dialog." Feature and UI language this early freezes the solution before requirements and design have examined it.

### 3. Shape the journeys

Lay the capabilities into the journeys they serve. The [story map](./use_cases_and_story_mapping.md) is definition's main instrument here: it exposes omissions and shows whether the proposed scope forms a coherent end-to-end experience or a pile of disconnected parts.

### 4. Draw the scope boundary

State what is in this release, what is out, and what is deferred to a later one. Check the boundary against the vision's scope exclusions; scope that crosses them needs a vision conversation, not silent expansion.

### 5. Prioritize

Prioritize capabilities and release slices, not individual stories — story-level ordering is a delivery concern. Weigh:

- Contribution to the desired outcome
- Risk reduction and learning value
- Legal, safety, security, or contractual necessity
- Dependencies and sequencing
- Cost of delay
- Implementation cost and reversibility

Any labeling method (MoSCoW, WSJF, buy-a-feature) is a communication device; the criteria above do the actual work. Every "must" needs a stated consequence explaining why it is mandatory, and ties are broken by learning value — prefer the item that reduces the most uncertainty.

Classify each mandatory scope driver by the consequence of not meeting it:

- **Obligation** — an external party imposes a defined penalty: a law, regulation, contract, or binding commitment. The consequence is named and verifiable ("the data-residency clause voids the enterprise contract"), and it is what makes the item mandatory. An obligation whose consequence nobody can state is not an obligation.
- **Expectation** — no external penalty, but stakeholders or users will judge the release as incomplete or broken without it. The consequence is reputational or behavioral ("submitters abandon the form"), not contractual.
- **Hope** — someone wants it and nothing measurable happens if it is absent. A hope is not mandatory; the classification exists so it can be argued down out of the mandatory set rather than smuggled through as a "must."

The classification is only worth its cost because the consequence is what gets argued, not the label. An unclassified "must," or an obligation with no consequence recorded, is the failure this catches.

### 6. Cut the release and name its hypothesis

Select a thin, coherent, end-to-end slice and state the belief it tests. Define success criteria, guardrail measures, and stop criteria before work starts. A release without a hypothesis can only be judged by whether it shipped.

### 7. Record the decisions

Log what was selected, deferred, and rejected, with the supporting evidence and its strength. These entries are what [validation and feedback](./validation_and_feedback.md) later reopens.

## Optional rolling roadmap

Maintain a roadmap only when `lifecycle-onepager.md` records its adoption. The view is outcome-based and rolling: **now** mirrors the committed release outcome, while **next** and **later** reflect the strategy's remaining ordered outcomes. Revise it as evidence arrives; feature-only and date-only entries are invalid. When tailoring records a skip, create no roadmap and let the vision strategy plus decision log carry the ordering and deferrals. This conditional view may live in the product's existing planning surface; this method introduces no mandatory roadmap file.

## Definition one-pager template

```markdown
# <Release or increment name>

## Outcome this release pursues
...

## Opportunities addressed
- ...

## Opportunities deferred (with reason)
- ...

## Capabilities in scope
- ...

## Out of scope for this release
- ...

## Priority order and rationale
1. ...

## Hypothesis this release tests
We believe ...

## Success, guardrail, and stop criteria
Success: ...
Guardrail: ...
Stop: ...

## Constraints and dependencies
- ...

## Decision owner and date
...
```

## Common failure modes

- Scope assembled from stakeholder requests instead of evidence
- Feature and UI language before capability language, freezing the solution prematurely
- Everything marked "must," so priority carries no information
- A release that is small but not coherent — one technical layer instead of a thin journey
- Definition without stop criteria, so scope only ever grows
- Deferrals not recorded, so every planning round re-argues them
- Treating the definition as final rather than as the current best commitment

## Completion checks

- Every in-scope capability traces to an opportunity and its evidence.
- Deferred and rejected items are recorded with reasons.
- Opportunity selection follows the strategy order or cites the `DEC#` that records a reorder or exception.
- Priorities are justified by criteria, not by rank position alone.
- Every mandatory scope driver is classified obligation, expectation, or hope, and each obligation records the consequence that makes it mandatory.
- The release is a coherent journey with a named hypothesis.
- Success, guardrail, and stop criteria exist before work starts.
- Product, engineering, and domain participants describe the scope identically.
- If the lifecycle one-pager adopts a roadmap, its now/next/later entries are outcome-based and current; if it skips one, no downstream step requires it.

## Further material

**Examples:**

- An expense-report product cuts release 1 from the story map as "one submitter, one approver, no policy engine" — a thin end-to-end journey whose hypothesis is "managers will approve within a day if approval takes one tap." Success is median approval latency; the stop criterion is approval rates below paper-form baseline after four weeks.
- CSV bulk import is deferred with the recorded reason "no evidence yet that migration effort blocks adoption — revisit after ten onboardings." The next three planning rounds cite the entry instead of re-arguing the feature.

**References:** [Shape Up — Ryan Singer, Basecamp](https://basecamp.com/shapeup); [The New Backlog (story mapping) — Jeff Patton](https://www.jpattonassociates.com/the-new-backlog/); [RICE prioritization — Intercom](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/).

**Agent rule sets:** [`shinpr/claude-code-discover`](https://github.com/shinpr/claude-code-discover) — keeps hypotheses, validation results, and PRDs in the repo beside the code, so the coding agent sees rejected alternatives and the evidence behind each scope decision; [`assimovt/productskills`](https://github.com/assimovt/productskills) — includes `prd-writing` and `scope-cutting` skills; [`huntsyea/product-skills`](https://github.com/huntsyea/product-skills) (formerly `rohanpatriot/product-skills`) — includes a `shape-up` skill (appetite, pitches, betting) for the commitment step.

**Books:** *Escaping the Build Trap* — Melissa Perri; *Shape Up* — Ryan Singer; *The Lean Product Playbook* — Dan Olsen.
