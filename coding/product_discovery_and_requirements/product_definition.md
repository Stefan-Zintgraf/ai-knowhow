# Product Definition

**Status:** First draft

Product definition turns discovery evidence and strategy into a coherent scope: which opportunities to pursue now, which capabilities the product must provide, which journeys those capabilities serve, and in what order. It sits between discovery and requirements — discovery establishes what is worth pursuing, definition commits to what will be pursued next, and requirements makes the committed behavior precise.

Terms used here are defined in the [glossary](./glossary.md).

## Inputs

- [Product vision](./product_vision.md) and its strategy: direction, principles, scope boundaries, and the ordered outcomes the next investment should serve
- [Discovery](./product_discovery.md) evidence: opportunities, tested assumptions, experiment results
- [Domain discovery](./domain_discovery.md) outputs where they exist: capability map, domain glossary
- Constraints: dates, budgets, contracts, platform commitments

## Core activities

### 1. Select opportunities

Choose which validated opportunities the next investment addresses. Check the selection against the strategy's ordered outcomes: a selection that fights the strategy needs a strategy conversation (and a roadmap update where one exists), not silent reordering. Record which opportunities are deferred and why — an unrecorded deferral gets re-litigated in every planning conversation.

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

### 6. Cut the release and name its hypothesis

Select a thin, coherent, end-to-end slice and state the belief it tests. Define success criteria, guardrail measures, and stop criteria before work starts. A release without a hypothesis can only be judged by whether it shipped.

### 7. Record the decisions

Log what was selected, deferred, and rejected, with the supporting evidence and its strength. These entries are what [validation and feedback](./validation_and_feedback.md) later reopens.

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
- Priorities are justified by criteria, not by rank position alone.
- The release is a coherent journey with a named hypothesis.
- Success, guardrail, and stop criteria exist before work starts.
- Product, engineering, and domain participants describe the scope identically.

## Further material

**Examples:**

- An expense-report product cuts release 1 from the story map as "one submitter, one approver, no policy engine" — a thin end-to-end journey whose hypothesis is "managers will approve within a day if approval takes one tap." Success is median approval latency; the stop criterion is approval rates below paper-form baseline after four weeks.
- CSV bulk import is deferred with the recorded reason "no evidence yet that migration effort blocks adoption — revisit after ten onboardings." The next three planning rounds cite the entry instead of re-arguing the feature.

**References:** [Shape Up — Ryan Singer, Basecamp](https://basecamp.com/shapeup); [The New Backlog (story mapping) — Jeff Patton](https://www.jpattonassociates.com/the-new-backlog/); [RICE prioritization — Intercom](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/).

**Agent rule sets:** [`shinpr/claude-code-discover`](https://github.com/shinpr/claude-code-discover) — keeps hypotheses, validation results, and PRDs in the repo beside the code, so the coding agent sees rejected alternatives and the evidence behind each scope decision; [`assimovt/productskills`](https://github.com/assimovt/productskills) — includes `prd-writing` and `scope-cutting` skills; [`huntsyea/product-skills`](https://github.com/huntsyea/product-skills) (formerly `rohanpatriot/product-skills`) — includes a `shape-up` skill (appetite, pitches, betting) for the commitment step.

**Books:** *Escaping the Build Trap* — Melissa Perri; *Shape Up* — Ryan Singer; *The Lean Product Playbook* — Dan Olsen.
