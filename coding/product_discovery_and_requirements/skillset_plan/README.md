# Discovery–Definition–Requirements Skillset Planning Bundle

This folder holds the plan for the discovery–definition–requirements skillset: seven skills shipping as one `product-loop` plugin.

## Documents

- [Skillset plan](./prod_discovery_requirements_skillset_plan.md) — the authoring spec: lifecycle, artifacts, traceability spine, deterministic linter, per-skill design, and regression suite. Self-contained; to author a skill you need this plus the one stage method doc it links.
- [Plan review brief](./plan-review-brief.md) — seven open findings against the plan, with stable `REV-xx` IDs. Read before authoring: two of them are linter checks resting on vocabulary no method doc defines.
- [Existing GitHub skillsets — fit analysis](./github_skillsets.md) — survey of the external source universe behind the plan's donor set. Reference only.
- [`archive/`](./archive/) — superseded planning and acceptance evidence. Not an input to authoring.

The method documents the skillset consumes live in the [parent folder](../). They describe how the lifecycle stages work; this folder describes how those methods become skills.

## Authoring sequence

1. Author one skill at a time, auditing the exact donor files named in the plan's §3.3 before vendoring anything.
2. Record each vendored item's source path, pinned revision, retrieval date, license, and attribution (§3.2).
3. Run the reference topic (§6) and score it on the four axes before declaring that skill complete.
4. Reconcile the method docs with what was actually implemented (§3.3, post-authoring reconciliation).

No phase is complete merely because an external source is mentioned. Completion requires traceable evidence that each accepted contribution changed a concrete mechanism, and that every rejected or deferred contribution has a recorded reason.
