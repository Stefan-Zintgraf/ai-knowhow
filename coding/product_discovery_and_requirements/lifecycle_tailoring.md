# Lifecycle Tailoring

**Status:** First draft

The rest of this collection describes the full lifecycle. A specific topic rarely needs all of it, and not every topic enters at the top. Tailoring derives a **specific lifecycle for a specific topic**: an entry point, a set of stages and artifacts, a cadence, and named decision authority. Record the result as a lifecycle one-pager (template below) and revisit it when evidence changes.

Terms used here are defined in the [glossary](./glossary.md).

## Step 1 — Choose the entry point

Enter the lifecycle where the real uncertainty is, not where the process diagram begins.

### Greenfield product

No product, prior evidence, or existing artifacts exist. Enter at [product vision](./product_vision.md) and run the full loop, at the smallest ceremony the risk allows. The common trap is skipping evidence-gathering because "there is nothing to observe yet" — there is always a present situation: observe how the intended actors solve the problem today, including workarounds, manual processes, and doing nothing. Greenfield does not mean evidence-free; it means the evidence lives outside your product.

### New capability in an existing product

A vision, domain glossary, and quality scenarios already exist. Enter at [product discovery](./product_discovery.md) for the capability's own value and usability risks. Reuse the existing vision and check the capability against its scope boundaries — a capability that fights the vision needs a vision conversation, not a backlog entry.

### Improvement or rework of existing behavior

The starting evidence is post-release: outcome measures, incidents, support cases, observed workarounds. Enter at [validation and feedback](./validation_and_feedback.md) evidence and work backwards to the decision it reopens. Reuse existing requirements, use cases, and the domain model; the work is usually correcting a specific earlier decision, not rediscovering the product.

### Compliance or contract mandate

The outcome is fixed externally; "whether" is not in question. Enter at [requirements engineering](./requirements_engineering.md) with the mandate as a constraint. Discovery still applies to *how*: usability and feasibility assumptions remain open even when the obligation is not, and a compliant-but-unusable implementation fails both users and auditors.

### Fast-follow on strong prior evidence

Evidence already exists — a competitor's traction, a successful pilot, a validated internal prototype. Enter at [product definition](./product_definition.md), but first verify the evidence transfers: your users, context, and constraints may differ from where the evidence was produced.

### Technical or platform initiative

The actors are internal: developers, operators, support. Enter at [product discovery](./product_discovery.md) with internal users as the actors and their workflows as the journeys. [Quality attributes](./quality_attributes.md) usually dominate; the value risk is that no internal team adopts the platform.

Whatever the entry point, two things are never skipped: **named actors with a desired outcome**, and **success and stop criteria for the next investment**.

## Step 2 — Size the ceremony

Scale ceremony with these drivers, not with organizational habit:

- **Risk of harm** — safety, security, money, reputation, legal exposure
- **Irreversibility** — how costly it is to change course after committing
- **Regulation and contract** — externally imposed completeness and evidence obligations
- **Coordination cost** — number of teams, organizations, and external parties involved
- **Sponsor communication** — whether sponsors need a durable view beyond the next committed slice
- **Product lifetime** — how long the decisions must hold
- **Genuine uncertainty** — how much is actually unknown, versus merely undocumented

When the drivers are low: the [minimum useful discovery package](./overview.md#minimum-useful-discovery-package), conversation-level requirements, and acceptance examples instead of specifications.

When the drivers are high: full requirements engineering with traceability, formal validation reviews, quality-attribute utility trees, and gated decisions.

Most topics are mixed — high on one driver, low on the rest. Apply ceremony per driver (e.g., full traceability for the regulated data flows only), not uniformly.

## Step 3 — Select stages and artifacts

Adopt an artifact when it reduces an important uncertainty or improves a consequential decision — never because its template looks complete.

Mandatory minimum for any topic:

- Named actors and the outcome being pursued
- The riskiest assumptions, made visible
- Success and stop criteria for the next investment
- A decision log entry for each consequential choice

Then weight the stages by where the dominant uncertainty sits (the [practical technique index](./resources.md#practical-technique-index) maps uncertainties to techniques):

| Dominant uncertainty | Emphasize |
| --- | --- |
| Whether the problem is worth solving | [Product discovery](./product_discovery.md) |
| What to build next, and how much | [Product definition](./product_definition.md) and story mapping |
| Complex behavior, rules, failure paths | [Use cases](./use_cases_and_story_mapping.md) |
| Tacit or contested domain knowledge | [Domain discovery](./domain_discovery.md) |
| Architectural risk from non-functional needs | [Quality attributes](./quality_attributes.md) |
| Contractual or regulated completeness | [Requirements engineering](./requirements_engineering.md) |
| Whether shipped work created value | [Validation and feedback](./validation_and_feedback.md) |

The product roadmap is the canonical ceremony-gated artifact. Record an explicit **adopt** or **skip** decision in the lifecycle one-pager, based on coordination cost, sponsor communication, and product lifetime. When adopted, `define-release` maintains an outcome-based rolling now/next/later view (never features and dates); when skipped, low-ceremony topics rely on the vision's strategy list and the decision log instead, and no downstream stage may demand a roadmap.

Record skipped stages with the reason. A deliberate skip is a decision; a silent skip is a blind spot.

## Step 4 — Choose the cadence

Define what one cycle of the loop produces: at least one tested assumption and one recorded decision — not artifacts alone.

- **Continuous discovery.** Weekly user contact; the loop runs permanently alongside delivery. Fits durable product teams with direct access to users.
- **Timeboxed discovery cycles.** Fixed iterations (one to four weeks), each ending in a proceed/adapt/pause/abandon decision. Fits project settings, limited user access, or teams new to discovery.
- **Gated milestones.** Stage reviews with formal exit criteria and sign-off. Fits regulated, contractual, or high-coordination work. Guard against gates becoming document reviews instead of decision points.

The cadence also sets the [validation review](./validation_and_feedback.md#review-cadence) rhythm after release.

## Step 5 — Assign decision authority

Every consequential decision type needs exactly one named owner. Unowned decisions default to "continue," which is how discovery loops run forever and scope only grows.

Use [Collaboration and decision ownership](./collaboration_and_decision_ownership.md) to distinguish the accountable owner from required contributors, specialist authorities, formal approvers, and facilitators. A joint product-trio review still needs one named decision owner.

| Decision | Typical owner |
| --- | --- |
| Change the vision or its scope boundaries | Product lead; sponsor approval where required |
| Proceed / adapt / pause / abandon after an experiment | Product lead, after product-trio review |
| Cut or defer scope from a release | Product lead |
| Accept or reject a requirement change | Requirement owner named in the change record |
| Release go / no-go | Delivery or service owner, after operations review |
| Reopen an earlier decision after validation evidence | Owner of the reopened artifact |

Name an escalation path for disagreements, and record each decision in the decision log with the evidence and its strength.

## Lifecycle one-pager template

```markdown
# <Topic> lifecycle

## Entry point and rationale
<Greenfield / new capability / rework / mandate / fast-follow / platform — and why>

## Stages in use
- ...

## Stages deliberately skipped
- <stage> — <reason>

## Artifacts
Mandatory: ...
Optional: ...
Roadmap: <adopt / skip — coordination-cost, sponsor-communication, or product-lifetime reason>

## Cadence
<Model, cycle length, what one cycle must produce, review ritual>

## Consequential decisions and stages
Repeat this block for every consequential decision type and stage in use:

### <decision type or stage>
- Accountable owner: <one named person; never a group or department>
- Required contributors: <named people and the contribution/evidence required from each>
- Specialist authorities: <named qualified authorities, or `None — <reason>`>
- Formal approvers: <named required approvers, or `None — <reason>`>
- Evidence required: <evidence and strength needed to decide or complete the stage>
- Escalation path: <named person/path and triggering condition>
- Evidence-based reopen trigger: <event or evidence that reopens this decision or stage>

## Success and stop criteria for the next investment
- ...

## Revisit trigger
<What evidence reopens this tailoring itself>
```

## Common failure modes

- Running full ceremony on a reversible one-week topic
- Skipping discovery because the mandate is fixed, though usability and feasibility remain open
- Choosing the entry point by organizational habit instead of by where the uncertainty is
- Treating greenfield as evidence-free instead of observing the present situation
- Tailoring once and never revisiting when evidence changes
- No named owner for the pause/abandon decision, so the loop never ends
- Gates that review documents instead of making decisions

## Completion checks

- The entry point matches where the real uncertainty sits.
- Skipped stages are recorded with reasons.
- Roadmap adoption or skip is explicit and justified by coordination cost, sponsor communication, or product lifetime.
- Ceremony matches risk, irreversibility, and regulation — per driver, not uniformly.
- One cycle has a defined decision output.
- Every consequential decision type has one named owner and an escalation path.
- Required contributors, specialist authorities, and formal approvers are named where applicable.
- The tailoring itself has a revisit trigger.
