# Discovery–Definition–Requirements Skillset Planning Bundle

This folder contains the planning and assurance documents for the proprietary discovery–definition–requirements skillset.

## Documents

- [Skillset plan](./prod_discovery_requirements_skillset_plan.md) — the proposed lifecycle, artifacts, traceability spine, and per-skill design.
- [Existing GitHub skillsets — fit analysis](./github_skillsets.md) — comparison of the external source universe and the reuse recommendation. Reference material; open only when the reasoning behind a contribution is needed.
- [Skillset plan update plan](./skillset_plan_update_plan.md) — the plan gaps, ordered revision edits, and the normative contribution-coverage contract. Open this when revising the skillset plan.
- Seven `*-contributions.md` files — per-skill contribution ledgers, method coverage, and authoring acceptance gates.

The method documents used by the skillset remain in the [parent folder](../). They describe how the lifecycle stages work; this folder describes how those methods will be turned into skills.

## Required sequence

1. Revise the skillset plan using the [update plan](./skillset_plan_update_plan.md).
2. Resolve every contribution-ledger row to an explicit disposition and fill its plan evidence.
3. Pass the plan-level coverage gate.
4. Author or adjust one skill at a time, auditing the exact donor files named by its ledger.
5. Replace planned evidence with actual skill-file, linter-rule, and test references.
6. Run the worked reference topic and the skill's authoring gate before declaring that skill complete.

No planning or authoring phase is complete merely because an external source is mentioned. Completion requires traceable evidence that each accepted contribution changed a concrete mechanism, and that every rejected or deferred contribution has a recorded reason.
