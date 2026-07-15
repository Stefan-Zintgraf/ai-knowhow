# Use Cases and Story Mapping

**Status:** Second draft

Use cases and story maps describe product behavior from the perspective of people or external systems trying to achieve goals. They connect discovery to delivery without prematurely deciding internal architecture.

Terms used here are defined in the [glossary](./glossary.md).

## When to use each tool

### Use cases

Use cases are strongest when a goal has meaningful alternatives, business rules, failure paths, or interactions across actors and systems.

### User story maps

Story maps are strongest for seeing the end-to-end journey, finding omissions, and selecting coherent release slices.

### User stories

User stories are small prompts for delivery conversations. A flat list of stories is not a substitute for a behavioral model.

## Use-case template

```markdown
# UC-<id>: <Actor goal>

## Goal and scope
<What outcome does the primary actor seek, and what system is in scope?>

## Primary actor
...

## Supporting actors and systems
- ...

## Trigger
...

## Preconditions
- ...

## Minimal guarantee
<What remains true even if the use case fails?>

## Success guarantee
<What is true when it succeeds?>

## Main success scenario
1. Actor ...
2. System ...

## Extensions
- 2a. If ...
  1. System ...

## Business rules
- BR-...

## Quality and operational concerns
- ...

## Open questions
- ...
```

Write steps as intentions and observable responsibilities. “System validates the request” is usually more appropriate than “controller calls validation service.”

## Story-mapping process

1. Name the user and the outcome represented by the map.
2. Lay out major activities from left to right in narrative order.
3. Break each activity into user tasks.
4. Add alternatives, failures, handoffs, and operational tasks.
5. Place candidate implementation stories beneath the tasks.
6. Walk realistic scenarios through the map with users and domain experts.
7. Cut a thin end-to-end release across the map.
8. Name the hypothesis or outcome that release tests.

The first release should be coherent, not merely small. A narrow end-to-end journey often teaches more than completing one technical layer.

Steps 7 and 8 are the instrument of [product definition](./product_definition.md): record the resulting scope, priorities, hypothesis, and success/stop criteria in its definition one-pager.

## From use case to acceptance examples

Turn important paths and rules into concrete examples:

```gherkin
Given a sharing link has been revoked
When a recipient follows the old link after the revocation window
Then access is denied
And the attempt is recorded in the audit log
```

Examples clarify requirements but do not replace the broader purpose and variations expressed by a use case.

## Useful distinctions

- **Actor:** a role interacting with the system, not necessarily one named person.
- **Goal:** the result the actor seeks.
- **Scenario:** one path through a use case.
- **Use case:** the goal plus its relevant scenarios.
- **Story:** a negotiable slice prepared for delivery.
- **Task:** a step users perform within a broader activity.
- **Release slice:** a coherent subset of the map that provides or tests value.

## Completion checks

- The primary actor and goal are unambiguous.
- The main scenario is understandable without implementation knowledge.
- Important alternatives, failures, permissions, and cancellation paths are present.
- Business rules are referenced rather than silently embedded in prose.
- Quality concerns are linked where they affect the interaction.
- The story map shows an end-to-end journey and explicit release boundaries.
- Each planned slice has an outcome or learning purpose.

## Further material

**Examples:**

- A library writes the use case "Borrow an item." The extensions — borrower has unpaid fines, item is reserved by someone else, item returns damaged — surface three business rules that existed only in the head of the front-desk staff and had never been written down.
- An HR team maps the employee-onboarding journey. The walking-skeleton slice "one new hire, IT equipment only" exposes a handoff between HR and IT that no single stakeholder owned — invisible in the flat backlog, obvious on the map.

**References:** [The New Backlog — Jeff Patton](https://www.jpattonassociates.com/the-new-backlog/); [Use case — Wikipedia](https://en.wikipedia.org/wiki/Use_case); [Example Mapping introduction — Cucumber](https://cucumber.io/blog/bdd/example-mapping-introduction/).

**Agent rule sets:** [`rohanpatriot/product-skills`](https://github.com/rohanpatriot/product-skills) — includes a `story-mapping` skill (Patton) that builds maps, slices releases, and escapes the flat-backlog trap; [`deanpeters/Product-Manager-Skills`](https://github.com/deanpeters/Product-Manager-Skills) — includes a `user-story-mapping` skill that asks whose journey is being mapped, then builds backbone → tasks → slices. Use cases proper (Cockburn-style, with extensions and guarantees) have no well-made agent rule set yet.

**Books:** *Writing Effective Use Cases* — Alistair Cockburn; *User Story Mapping* — Jeff Patton, Peter Economy; *Specification by Example* — Gojko Adzic.

