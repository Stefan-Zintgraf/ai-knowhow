# Quality Attributes

**Status:** Second draft

Quality attributes describe how well a system must behave under meaningful conditions. They frequently shape architecture more strongly than functional requirements, so the important ones must be discovered early: start during [product discovery](./product_discovery.md), where architecture-changing qualities belong among the riskiest assumptions. The requirements stage sharpens them into measurable scenarios; it does not begin them.

Terms used here are defined in the [glossary](./glossary.md).

“Fast,” “secure,” and “scalable” are aspirations, not actionable requirements. Express qualities as scenarios with measurable responses and explicit trade-offs.

## Common quality attributes

- Availability and reliability
- Performance and latency
- Scalability and capacity
- Security and privacy
- Safety
- Usability and accessibility
- Auditability and accountability
- Maintainability and modifiability
- Interoperability and compatibility
- Resilience and recoverability
- Data integrity and consistency
- Observability and operability
- Portability and deployability
- Energy or resource efficiency

The relevant set depends on the product. Do not turn this list into a requirement checklist without evidence.

## Quality-attribute scenario

Use six parts:

1. **Source** — who or what produces the stimulus?
2. **Stimulus** — what happens?
3. **Environment** — under which operating conditions?
4. **Artifact** — which system or part is affected?
5. **Response** — what must the system do?
6. **Response measure** — how will success be measured?

Example:

```markdown
Attribute: Recoverability
Source: Regional cloud failure
Stimulus: The active region becomes unavailable
Environment: Peak business hours with 2,000 active sessions
Artifact: Customer-facing ordering service
Response: Traffic moves to a healthy region and accepted orders are retained
Measure: Service restored within 5 minutes; no acknowledged order is lost
```

## Discovery techniques

- Interview users about unacceptable delays, loss, exposure, or confusion.
- Ask operators about incidents, support burden, deployment, and recovery.
- Review regulation, contracts, threat models, and service-level objectives.
- Run architecture-quality or premortem workshops.
- Examine peak-load, failure, abuse, migration, and degraded-mode scenarios.
- Rank scenarios by business impact, architectural difficulty, and uncertainty.

## Trade-offs

Quality attributes interact:

- Strong consistency can reduce availability or increase latency.
- Additional security controls can add friction.
- General modifiability can increase present complexity.
- Detailed observability can conflict with privacy and cost.
- High availability can increase operational complexity and expense.

Record the chosen trade-off and rationale. “Maximize everything” is not a strategy.

## Quality-attribute utility tree

For a high-risk system:

1. Put the product's value or mission at the root.
2. Add relevant quality attributes.
3. Add concrete scenarios beneath each attribute.
4. Rank each scenario by importance and implementation difficulty or uncertainty.
5. Investigate the high-importance, high-risk scenarios first.

## Operational quality

Include the system's human and organizational operation:

- Can failures be detected and diagnosed?
- Can operators degrade service safely?
- Are recovery steps tested and time-bounded?
- Can changes be deployed, rolled back, and audited?
- Are support and incident responsibilities clear?
- Does telemetry avoid exposing sensitive data?

## Completion checks

- Each important quality is grounded in a stakeholder or business consequence.
- Critical scenarios name conditions and measurable responses.
- Expected scale and workload shape are explicit.
- Failure, attack, recovery, and degraded-mode behavior are represented.
- Conflicting qualities have explicit priorities or trade-offs.
- A verification method exists for each critical scenario.
- Architectural decisions can trace back to these scenarios.

## Further material

**Examples:**

- A payments team builds a utility tree expecting latency to dominate. Ranking scenarios by business impact and uncertainty instead puts *auditability* at the top — a regulator can fine them, slow searches cannot — and the first architectural spike targets the audit trail, not the cache.
- A cart-and-checkout system records the trade-off explicitly: the cart tolerates eventual consistency (a briefly stale item count is harmless), checkout requires strong consistency (double-charging is not). One sentence of recorded rationale prevents the "why is this inconsistent?" debate from recurring.

**References:** [arc42 quality model](https://quality.arc42.org/); [List of system quality attributes — Wikipedia](https://en.wikipedia.org/wiki/List_of_system_quality_attributes); [Threat Modeling — OWASP](https://owasp.org/www-community/Threat_Modeling).

**Agent rule sets:** [`45ck/software-architecture-skills`](https://github.com/45ck/software-architecture-skills) — platform-neutral pack of 14 skills including `quality-attribute-scenario-writer`, `tradeoff-analysis-writer`, and `architecture-risk-assessor`, with templates and examples; [`DavidROliverBA/Daves-Claude-Code-Skills`](https://github.com/DavidROliverBA/Daves-Claude-Code-Skills) — architecture and analysis skills covering non-functional requirements management, change impact, and scenario comparison, several using multi-agent parallel analysis.

**Books:** *Software Architecture in Practice* — Len Bass, Paul Clements, Rick Kazman; *Release It!* — Michael T. Nygard; *Threat Modeling* — Adam Shostack.

