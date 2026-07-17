# Product Discovery

**Status:** Second draft

Product discovery reduces uncertainty about whether a problem is worth solving, for whom, and which solution direction is desirable, usable, viable, and feasible. Its output is evidence and decisions—not merely ideas or a backlog.

Terms used here are defined in the [glossary](./glossary.md).

## Four recurring risks

- **Value:** Will people choose or benefit from it?
- **Usability:** Can the intended people understand and use it?
- **Feasibility:** Can it be delivered with the available technology, data, skills, and time?
- **Viability:** Does it work for the business, operations, policy, ethics, and legal environment?

## Discovery loop

How often the loop runs — continuously, in timeboxed cycles, or between gates — is a tailoring decision; see [lifecycle tailoring](./lifecycle_tailoring.md).

### 1. Frame an outcome

Start with a measurable or observable change, not a requested feature. Record why the outcome matters and to whom.

### 2. Gather evidence

Use several sources where practical:

- Interviews about specific past behavior
- Direct observation or contextual inquiry
- Existing analytics, support cases, searches, and workarounds
- Journey mapping or service blueprints
- Competitive and alternative-solution research
- Subject-matter expert and stakeholder interviews

Ask about actual situations and choices. Hypothetical enthusiasm is weak evidence.

### 3. Map opportunities

Organize user needs, pain points, desires, and obstacles beneath the desired outcome. An Opportunity Solution Tree is one useful structure. Keep opportunities separate from proposed solutions. Check a targeted opportunity against the vision's thin ordered-outcomes strategy: selecting against the recorded order needs an explicit `DEC#` recording the exception or strategy reorder, never silent divergence. A strategy reorder is a discovery pivot applied by the strategy section's accountable human owner, followed by a refresh of its derived companion index.

### 4. Generate alternatives

Develop multiple materially different ways to address the selected opportunity. Include process, policy, manual-service, and no-build options.

### 5. Expose assumptions

For each solution, list what must be true. Classify assumptions by value, usability, feasibility, and viability. Rank them by importance and lack of evidence.

### 6. Test cheaply

Choose the smallest trustworthy test of the riskiest assumption:

- Prototype or usability task
- Concierge or Wizard-of-Oz service
- Technical spike
- Data feasibility analysis
- Landing-page or demand test
- Policy, security, or legal review
- Limited pilot

Define success, failure, and inconclusive criteria before running the test.

### 7. Decide and record

Proceed, adapt, pause, or abandon. An adapt decision is a discovery pivot — changing the opportunity, solution direction, scope, or strategy within a stable vision; it is routine, must not silently edit the vision, and does not by itself reopen the vision. Record evidence strength, remaining uncertainty, and the next decision—not just experiment results. Only evidence invalidating the intended future or target need may be routed to a vision re-entry, and that route requires an explicit `DEC#` citing the evidence; a failed experiment or weak feature is rerouted to the lowest challenged downstream artifact. Selected opportunities and tested solution directions feed [product definition](./product_definition.md), where they are committed into scope.

## Discovery artifacts

- Research questions and evidence log
- Actor or stakeholder map
- Jobs-to-be-Done statements
- Current journey or service blueprint
- Opportunity Solution Tree
- Assumption map and experiment cards
- Prototype and findings
- Decision log
- Candidate story map or use cases

These are thinking tools, not mandatory deliverables.

## Experiment card

```markdown
## Decision
What decision will this evidence inform?

## Assumption
We believe ...

## Evidence needed
We need to observe ...

## Method
We will ...

## Criteria
Support: ...
Refute: ...
Inconclusive: ...

## Result and confidence
...

## Decision / next step
...
```

## Common failure modes

- Treating discovery as validation of a preferred solution
- Asking users to design the product
- Counting opinions as strongly as observed behavior
- Testing low-risk details while core value remains uncertain
- Producing personas or maps that never influence a decision
- Separating discovery entirely from engineering and delivery
- Running endless research without explicit decision thresholds

## Completion checks for an increment

- The intended outcome and selected opportunity are explicit.
- The selected opportunity follows the strategy's ordered outcomes or has an explicit `DEC#` recording the exception or reorder.
- The major assumptions are visible and ranked.
- Evidence is adequate for the size and reversibility of the next investment.
- Alternative solutions were considered.
- The next release or experiment has success and guardrail measures.
- Remaining uncertainty is carried forward rather than disguised as certainty.

## Further material

**Examples:**

- A team framed the outcome "raise trial-to-paid conversion," ran weekly customer interviews, and organized findings in an Opportunity Solution Tree. The riskiest assumption — "users understand the pricing model by day 3" — was tested with a fake-door pricing page before any billing code was written.
- Instead of asking "would you use an automated reminder feature?", an interviewer asks "walk me through the last time you chased an unpaid invoice." The concrete story reveals that reminders are already automated through the bank app; the real pain is reconciling partial payments — an opportunity no feature request had mentioned.

**References:** [Opportunity Solution Trees — Teresa Torres, Product Talk](https://www.producttalk.org/opportunity-solution-tree/); [Product Discovery — Silicon Valley Product Group](https://www.svpg.com/product-discovery/); [Framework for Innovation / Double Diamond — Design Council](https://www.designcouncil.org.uk/our-resources/framework-for-innovation/).

**Agent rule sets:** [`huntsyea/product-skills`](https://github.com/huntsyea/product-skills) (formerly `rohanpatriot/product-skills`) — four skills built from the source texts, including `continuous-discovery` (Torres) and `jobs-to-be-done` (Moesta switch interviews, forces diagrams); [`jacksoncalling/argo-continuous-discovery`](https://github.com/jacksoncalling/argo-continuous-discovery) — a folder-based operator for the full Continuous Discovery Habits workflow, from outcome through opportunity extraction to assumption tests, with interview-quality coaching; [`assimovt/productskills`](https://github.com/assimovt/productskills) — compact, opinionated skills (Mom Test, JTBD, opportunity mapping), 50–150 lines each.

**Books:** *Continuous Discovery Habits* — Teresa Torres; *The Mom Test* — Rob Fitzpatrick; *Testing Business Ideas* — David J. Bland, Alexander Osterwalder.
