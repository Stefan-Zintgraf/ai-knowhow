# Collaboration and Decision Ownership

**Status:** First draft

This document defines how product management, product design, engineering, domain experts, and governance specialists collaborate across product discovery, requirements work, software design, delivery, and validation. It is a cross-cutting method contract for the collection, not a phase owned by one department.

Terms used here are defined in the [glossary](./glossary.md). Apply these defaults through [lifecycle tailoring](./lifecycle_tailoring.md), which names the actual people, decision authority, contributors, and escalation paths for a specific topic.

## Purpose and scope

The lifecycle describes kinds of uncertainty and decisions, not a sequence of departmental ownership. Work that happens before or alongside software architecture does not therefore belong entirely to product management.

Product management usually leads decisions about intended outcomes, target users, business value, product boundaries, and priority. Other roles lead decisions requiring their own competence: design leads user experience and research quality; engineering leads feasibility and architecture; domain experts lead domain correctness; legal, compliance, security, and operations lead judgments within their specialist authority.

This document is:

- A default collaboration and accountability model
- A tailoring input for assigning named decision authority
- A guardrail against product-to-design handoffs and role overreach
- A normative input to the discovery-definition-requirements skillset and the future design skillset

It is not:

- A new standalone skill
- A per-topic product artifact that teams must produce
- A universal organization chart or mandatory set of job titles
- A replacement for local governance, professional obligations, or regulatory approvals

## Core rules

1. **A lifecycle stage is not a department.** Product discovery, definition, requirements, design, and validation are cross-functional work.
2. **Accountability is not sole authorship.** Exactly one named person is accountable for each consequential decision, but that person must obtain the evidence and specialist contributions the decision requires.
3. **Joint review does not mean group ownership.** A product trio can shape and review a decision together while one named person remains accountable for making or escalating it.
4. **Specialist judgments remain with qualified specialists.** A product lead can prioritize business risk but cannot unilaterally declare an unsafe design secure, a prohibited behavior compliant, or an infeasible solution feasible.
5. **Architecture starts when technical uncertainty can change the product decision.** Feasibility, integration, security, performance, operability, data, and configurability risks are explored during discovery; architecture is not postponed until a requirements handoff.
6. **Requirements continue through design and delivery.** Design reveals constraints, edge cases, and trade-offs that can reopen scope, requirements, or earlier assumptions.
7. **Tailor roles to the context.** One person may hold several roles in a small team, but the decision accountabilities must still be explicit.

## Decision language

| Term | Meaning |
| --- | --- |
| Accountable owner | The one named person who decides, records the rationale, or invokes the escalation path. |
| Contributor | A participant whose evidence, analysis, or perspective is required before the decision is made. |
| Specialist authority | A contributor whose qualified judgment governs a particular concern, such as legal interpretation, security acceptance, or domain policy. |
| Approver | A formally required signatory in a contractual, regulatory, funding, or organizational governance process. Approval does not replace the accountable owner. |
| Facilitator | A person who structures the conversation or method but does not acquire decision authority merely by facilitating it. |

A role name in the tables below is only a default. Tailoring replaces it with an actual person and records required contributors, specialist authorities, approvers, and escalation.

## Default decision ownership

| Decision | Typical accountable role | Required contributors or authorities |
| --- | --- | --- |
| Set or change the product vision and its scope boundaries | Product lead | Sponsor, product design, engineering lead, commercial leadership, affected domain owners |
| Select target segments and the value proposition | Product lead | Product research/design, sales, marketing, customer-facing teams, engineering |
| Choose the research approach and judge research quality | Product research or design lead | Product lead, data/analytics, engineering, relevant domain experts |
| Define the desired outcome, success measures, and guardrails | Product lead | Product design, engineering, data/analytics, operations, sponsor |
| Proceed, adapt, pause, or abandon after an experiment | Product lead | Product design and engineering leads, research/data specialists, affected stakeholders |
| Accept the interaction model and usability evidence | Product design lead | Product lead, users or representatives, engineering, accessibility specialists |
| Accept a feasibility assessment or technical-risk disposition | Engineering lead | Architects, security, operations, data specialists, product and design |
| Commit, cut, or defer release scope | Product lead | Product design and engineering leads, delivery participants, affected domain owners |
| Define or change a business rule or invariant | Named domain owner | Domain experts, business analysis, product, engineering, compliance when applicable |
| Accept or reject a requirement change | Named requirement owner | Product, design, engineering, domain owner, affected specialist authorities |
| Set the business priority and acceptable trade-offs for a quality target | Product or service lead | Engineering/architecture, operations, security, legal/compliance, affected users |
| Define a measurable quality scenario and its technical response | Engineering or architecture lead | Product/service lead, operations, security, domain specialists |
| Interpret a legal, regulatory, contractual, or security obligation | Relevant specialist authority | Product, engineering, domain owner, delivery/service owner |
| Choose the software architecture and technical design | Engineering or architecture lead | Engineering team, product, design, security, operations, data and domain experts as needed |
| Make the release go/no-go decision | Delivery or service owner | Product, engineering, operations, security/compliance and other required approvers |
| Reopen an earlier decision after new evidence | Owner of the decision or artifact being reopened | Source of evidence and the contributors required for the new decision |

When a local governance model assigns a different accountable role, record the deviation during tailoring. Do not silently convert a required collaboration into either unilateral authority or committee ownership.

## Collaboration across the lifecycle

| Lifecycle work | Essential participation | Why |
| --- | --- | --- |
| Product vision | Product leadership, sponsor, design, engineering, commercial and domain voices | Direction must be valuable, credible, bounded, and compatible with organizational intent. |
| Product discovery | Product, design/research, and engineering, with users and domain experts | Desirability, value, feasibility, viability, and domain assumptions must be exposed together. |
| Product definition | Product, design, engineering, delivery and affected domain owners | Scope and slices must be valuable, usable, feasible, coherent, and measurable. |
| Requirements and domain discovery | Product, business/domain experts, design, engineering and relevant specialists | Observable behavior, rules, constraints, failure paths, and verification need multiple forms of expertise. |
| Quality-attribute discovery | Engineering/architecture, product/service ownership, operations, security and affected stakeholders | Quality targets are business priorities expressed through technically measurable scenarios and trade-offs. |
| Software design and delivery | Engineering leads, with continued product, design, domain and specialist participation | Technical decisions can expose product consequences and reopen earlier assumptions. |
| Validation and feedback | Product, design/research, engineering, data, operations and evidence sources | Outcome, usability, reliability, incident, and operational evidence must route back to the right decision owner. |

Participation should be proportional to risk. Not every contributor attends every meeting, but their necessary evidence or judgment must be present before the relevant decision.

## Architecture begins before a design phase

Software architecture is owned by engineering, but architectural thinking starts as soon as a technical risk could invalidate an opportunity, solution, scope, cost model, or success criterion. Early work may include:

- Feasibility spikes and technical prototypes
- Context, dependency, and data-flow sketches
- Quality-attribute scenarios and utility trees
- Threat modeling and privacy analysis
- Integration and migration experiments
- Operability, observability, capacity, and failure analysis
- Configuration-versus-customization analysis

These activities reduce uncertainty; they do not require premature commitment to a complete architecture. Decisions should be made at the last responsible moment while preserving enough evidence to avoid knowingly infeasible or unsafe product commitments.

Conversely, product and requirements work does not stop when design begins. Architecture and implementation can reveal a hidden domain rule, an unaffordable quality target, an unusable workflow, or a missing operational constraint. The affected decision is then reopened through the lifecycle rather than patched silently in design.

## Tailoring the defaults

For each consequential decision type in the lifecycle one-pager, record:

- One named accountable owner
- Required contributors
- Any specialist authority or formal approver
- The evidence required to decide
- The escalation path for unresolved disagreement
- The event or evidence that can reopen the decision

In a small team, one person may be product lead, researcher, and domain expert. Record the roles separately even when the name repeats; this exposes missing perspectives and conflicts of interest.

In regulated or safety-critical work, additional review and approval may be mandatory. Add those controls without diffusing accountability for preparing the decision, assembling evidence, and acting on the result.

Revisit ownership when team composition, product scope, regulation, operational responsibility, or risk changes.

## Common failure modes

- Treating the product manager as the sole author of everything before design
- Asking design to improve usability only after scope and behavior have been committed
- Inviting engineering after discovery and then discovering that the chosen solution is infeasible
- Calling the product trio the owner without naming who decides or escalates
- Letting a facilitator or artifact template acquire authority that belongs to a decision owner
- Allowing commercial commitments to bypass discovery, feasibility, or product boundaries
- Treating security, legal, compliance, domain, or operational review as optional feedback
- Letting architecture make product-priority decisions by default because product ownership is absent
- Freezing requirements before design and hiding later discoveries as implementation details
- Using responsibility matrices as ceremony without connecting decisions to evidence and escalation

## Relationship to the skillset

This document does not create another user-invoked skill. It constrains how existing and planned skills allocate authority, request participation, validate outputs, and hand work downstream.

| Skill or skillset area | Required consequence |
| --- | --- |
| Lifecycle tailoring | Name one accountable person, required contributors, specialist authorities, and escalation for every consequential decision type; reject group-only ownership. |
| Vision skills | Keep product direction accountable to the product lead while requiring sponsor, design, engineering, commercial, and domain input where material. |
| Product discovery | Require product, design/research, and engineering perspectives; do not let a product manager manufacture user evidence or technical feasibility alone. |
| Product definition | Make the product lead accountable for scope while requiring design and engineering review of usability, coherence, feasibility, and measurement. |
| Requirements specification | Route domain rules, quality attributes, compliance, security, operations, and external constraints to the appropriate owners and authorities; do not invent architecture prematurely. |
| Release validation | Route evidence to the owner of the affected decision and preserve the contributors needed to reassess it. |
| Future software-design skillset | Make engineering accountable for architecture while preserving product, design, domain, security, and operations participation and explicit backtracking triggers. |

Skill authors should translate these provisions into prompts, required fields, routing rules, gates, and test fixtures. They should not merely link this document as optional reading. Runtime skills need load it only when assigning or resolving decision ownership; the relevant distilled rules should already exist in each skill's normal workflow.

## Completion checks

- Every consequential decision has exactly one named accountable owner.
- Required contributors and specialist authorities are explicit.
- Joint review is not mistaken for group accountability.
- Product management is not assigned specialist or architectural authority by default.
- Engineering participates early enough to expose feasibility and architecture-driving risk.
- Product, design, domain, and specialist participation continues when design reveals product consequences.
- Escalation and reopening paths are defined.
- Skill behavior implements the relevant rules rather than treating this document as optional background.

