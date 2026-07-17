# Skillset Plan Revision Contract

**Status:** Normative for the next revision of the [skillset plan](./prod_discovery_requirements_skillset_plan.md).

**Target:** [prod_discovery_requirements_skillset_plan.md](./prod_discovery_requirements_skillset_plan.md)

**Inputs:** The method docs and contribution ledgers below. The [fit analysis](./github_skillsets.md) is reference material; open it only when the reasoning behind a specific contribution is needed.

**Constraints:** Preserve the proprietary traceability spine, the two skill modes, the derived-only companion, and lifecycle tailoring. These updates close coverage and assurance gaps; they are not an architecture redesign. Maximize justified reuse without weakening those constraints. The existing plan and method docs remain authoritative when external guidance conflicts with them or the chosen lifecycle.

**Non-goal:** Practitioner coaching is not a co-equal objective for this solo-expert workflow.

## Contribution ledgers

| Skill | Ledger |
| --- | --- |
| `brainstorm-vision` | [brainstorm-vision-contributions.md](./brainstorm-vision-contributions.md) |
| `create-vision-companion` | [create-vision-companion-contributions.md](./create-vision-companion-contributions.md) |
| `tailor-lifecycle` | [tailor-lifecycle-contributions.md](./tailor-lifecycle-contributions.md) |
| `discover-product` | [discover-product-contributions.md](./discover-product-contributions.md) |
| `define-release` | [define-release-contributions.md](./define-release-contributions.md) |
| `specify-requirements` | [specify-requirements-contributions.md](./specify-requirements-contributions.md) |
| `validate-release` | [validate-release-contributions.md](./validate-release-contributions.md) |

Each external-contribution row must contain a stable ID, source and license, reuse mode, intended incorporation, disposition, and objective evidence. Allowed final dispositions:

- `Adopt`: use substantially as identified.
- `Adapt`: preserve the mechanism while translating it onto this method and ID spine.
- `Call`: use a version-pinned specialist with a bounded contract; it must not own spine artifacts.
- `Reject`: record the fit, quality, duplication, or license reason.
- `Defer`: name the later skillset or decision that receives it.

No row may remain `Pending`. Preserve rejected and deferred rows. Accepted rows must cite the realizing artifact field, phase, prompt/guardrail, finalize check, integration contract, linter rule, or validation scenario.

Add method-owned rows, with stable local IDs, intended incorporation, and objective evidence, for applicable collaboration/decision-ownership and vision-stability rules. These rows need no external license or disposition.

For every `distill` row, audit each donor file during authoring and record:

1. repository and path;
2. commit/tag or retrieval date;
3. license and attribution;
4. candidate techniques, questions, rubrics, templates, failure modes, and checks;
5. each candidate's disposition; and
6. destination skill file and section for each adopted/adapted item.

Never fetch third-party repositories at runtime. Vendor distilled material with provenance. Version-pin callable specialists. Treat unlicensed material as reference-only. Do not copy or distill CC BY-NC-SA material from `deanpeters/Product-Manager-Skills`.

## Execution model (orchestration)

This revision is executed by an **orchestrator** (the main session) that dispatches every unit of work to a **fresh-context sub-agent**. The orchestrator holds no working state beyond this contract; it dispatches tasks, integrates returned results, enforces the reference-map sync rule, and runs the acceptance gate. **The orchestrator performs no analysis or authoring itself** — its only direct edits are trivial integration bookkeeping (e.g. moving a returned digest into place). Every substantive read, decision, or edit happens inside a sub-agent that starts cold with only its scoped inputs.

### Task envelope

Each sub-agent is dispatched with an explicit envelope:

- **Reads** — the exact files it may open (its own ledger/artifact plus named static reference/method docs). It may not open files outside this set.
- **Writes** — the exact output path(s) it owns. It may write nowhere else.
- **Done-definition** — the concrete artifact or edit that completes the task, including the reference-map row(s) to sync.
- **Return** — a short structured summary the orchestrator uses to gate the next step (no raw file dumps).

### Phase 0 — analysis fan-out (PARALLEL, read-only)

The following run **concurrently**. Safe because each reads its own ledger plus unchanging shared reference docs and writes **only its own unique digest file** — no shared-file writes, no write/read overlap, only concurrent reads of static docs. Digests are written under `analysis/` and treated as frozen inputs by the write phase.

| Agent | Reads | Writes |
| --- | --- | --- |
| Ledger audit ×7 (one per ledger) | that ledger + cited method docs | `analysis/<skill>-ledger.md` |
| Distill donor audit | vendored donor material + provenance sources | `analysis/distill-provenance.md` |
| Fit-analysis mapping | `github_skillsets.md` §§2, 5.1 | `analysis/fit-map.md` |

The orchestrator dispatches all Phase 0 agents together and waits for every digest before starting Phase 1. No Phase 0 agent may touch the target plan, `resources.md`, `overview.md`, method docs (write), or skill files.

### Phase 1 — ordered updates (SEQUENTIAL, one write-phase sub-agent per update)

Each numbered update below is one fresh-context sub-agent. They run **strictly one at a time** because they share write targets — the **shared-write set**:

- `prod_discovery_requirements_skillset_plan.md` (the target plan)
- `../resources.md` (reference map)
- `../overview.md` and affected method docs (updates 8–10)
- affected skill / lifecycle-onepager files (updates 9–10)

No two write-phase sub-agents may run at once, since each may edit the target plan and reference map. Each write-phase sub-agent receives: this contract, the relevant Phase 0 digest(s), and its task envelope; it applies exactly one numbered update, syncs the reference-map row(s), and returns a summary. The orchestrator verifies the return and the shared-write files are consistent before dispatching the next update.

### Phase 2 — acceptance gate (SEQUENTIAL sub-agent)

The final review (see [Acceptance gate](#acceptance-gate)) runs as its own fresh-context sub-agent with read access to the full bundle, producing the `contribution ID → plan section → skill file/test` mapping and the gate verdict. The orchestrator does not self-certify.

## Ordered updates

Apply these in order, each as one Phase 1 write-phase sub-agent per the task envelope above. For any edit—including these updates and later revisions—that changes a lifecycle element's first-class concepts, grounding, or deliberate deviations, update that element's row in the [resources.md reference map](../resources.md#reference-map) in the same change. This map-wide rule applies to every row, including the cross-cutting collaboration-and-decision-ownership row.

### 1. Add solution alternatives to `discover-product`

- Insert `generate alternatives` between opportunity mapping and assumption exposure. Require materially different directions, including process, policy, manual-service, and no-build options where plausible.
- Add `SOL#` to every ID/trace model. Choose and record its durable representation: `solutions.md` or a section of `opportunities.md`.
- Reserve `SOL` in `create-vision-companion` Phase 0.
- Require `ASM#` to cite its `SOL#`, or `OPP#` only when solution-independent. Require `EXP#` to cite the applicable `SOL#`.
- Add the finalize check `alternative solutions were considered`. Refuse solution-assumption ranking with only one direction unless a `DEC#` records why alternatives are not viable.
- Synchronize the artifact table, method-doc coverage, trace description/diagram, loop and discovery phases, linter, and reference-topic rubric.

### 2. Add a deterministic workspace linter

Specify a script, not an LLM skill, that parses the companion bundle and loop workspace. Separate deterministic checks from judgment gates. Every artifact-producing skill must run applicable deterministic checks at finalize; CI/hook integration is optional.

Check at minimum:

- ID format/uniqueness, reserved-family collisions, invalid/dangling upward citations, and orphaned spine artifacts;
- `EV`: human-supplied source, date, and strength;
- valid `SOL`–`ASM`–`EXP` relationships;
- `REL`: hypothesis, success, guardrail, stop criteria, and instrumentation/observation requirements for outcome and guardrail criteria;
- `REQ`: verification method or explicit open marker;
- `QAS`: require all six fields—source, stimulus, environment, artifact, response, and response measure. Each legitimately unresolved field must contain an explicit open marker; when resolved, the response measure must be measurable;
- transition-requirement handoffs when scope is retired;
- artifact filenames that collide with method-doc names; and
- roadmap entries: an outcome is mandatory; feature/date-only entries are invalid.

Map [validation_and_feedback.md](../validation_and_feedback.md)'s instrumentation contract to `define-release`, `specify-requirements`, and `validate-release` in the method-doc coverage table.

### 3. Add skillset regression validation

Create one small reference topic and run it end-to-end after each skill is authored or materially changed. Score method-doc completion checks, ledger coverage gates, linter results, handover, and re-entry. Record failures and update the responsible skill or plan.

Cover these scenarios:

- low ceremony;
- intentionally skipped stage with a recorded reason;
- weak evidence;
- single-solution exception;
- requirements gap requiring human review;
- post-release evidence reopening an earlier artifact;
- group-only owner, missing required specialist/engineering input, department-boundary handoff, and refusal to reopen invalidated upstream artifacts — each of which the skillset must detect and refuse;
- failed experiment wrongly escalated to a vision rewrite, which must be refused and rerouted;
- genuine vision-invalidating evidence with an explicit `DEC#`; and
- roadmap skipped for low ceremony and adopted for high coordination.

### 4. Apply every ledger

- Put every accepted contribution ID and its realizing mechanism in the relevant plan section.
- Add callable specialists `north-star` and, conditionally, `quality-attribute-scenario-writer` to the skills table. Define bounded role, version policy, inputs, outputs, and fallback.
- Add applicable handover UX, decision ownership/participation, linter invocation, provenance, deterministic validation, and backtracking triggers to each affected skill.

### 5. Define external-dependency policy

- `call`: version-pinned install, bounded contract, fallback, and no ownership of spine artifacts.
- `distill`: vendored content with source file, commit/tag or retrieval date, license, and attribution.
- `pattern`: local implementation with inspiration recorded and no runtime dependency.
- Never runtime-fetch third-party repositories or distill license-incompatible content.

### 6. Strengthen the `EXP#` schema

Merge the complete experiment-card template in [product_discovery.md](../product_discovery.md)—decision to inform, assumption/hypothesis, evidence needed, method, predeclared support/refute/inconclusive criteria, and result—with confidence per relevant risk dimension, a time budget, target `ASM#`, applicable `SOL#`, and resulting `DEC#`. Expose required and open fields to the linter.

### 7. Define handover and re-entry

Every skill must end with the next applicable stage from `lifecycle-onepager.md`, changed artifacts, unresolved decisions, and the progression gate. Record intentional skips. Command chaining must not override lifecycle tailoring. Map each `validate-release` backtracking condition to the artifact and skill reopened.

### 8. Add plan-to-authoring traceability

- Give each accepted ledger row a plan location and planned skill-file destination.
- Replace planned evidence with the actual file/section/test when authored.
- Reopen affected ledger rows and rerun gates after method-doc, donor-version, or artifact-schema changes.
- After authoring, reconcile [overview.md](../overview.md) and every affected method doc with the implemented skills, lifecycle, artifact schema, strategy section, ceremony-gated roadmap, `SOL#`, one-pagers, and linter. Do not complete the update while documentation and implementation differ.

### 9. Operationalize collaboration and decision ownership

- In `lifecycle-onepager.md`, record for every consequential decision/stage: one named accountable owner, required contributors, specialist authorities, formal approvers, the evidence required to decide, escalation path, and evidence-based reopen trigger. A group or department is not an accountable owner.
- Implement applicable behavior and gates in `tailor-lifecycle`, `brainstorm-vision`, `discover-product`, `define-release`, `specify-requirements`, and `validate-release`. Preserve the future design skillset's authority over design decisions.
- Require early engineering, design, operations, security, compliance, domain, and other specialist participation when their evidence is material. Product management must not fabricate specialist evidence.
- Preserve collaborative authorship while keeping accountability singular and explicit.
- Keep these rules in existing skills and lifecycle artifacts; create no standalone ownership skill or mandatory runtime document.

### 10. Operationalize vision stability

- Use `discovery pivot` for routine discovery/validation adaptation. It must not silently edit the vision.
- Permit `brainstorm-vision` and `create-vision-companion` to make a `vision pivot` only through an explicit `DEC#` citing evidence that invalidates the intended future or target need. Route routine findings to opportunities, solutions, scope, or strategy.
- Route only evidence contradicting a foundational assumption from `validate-release` to the vision; reopen downstream artifacts for all other evidence.
- Keep product strategy as a thin ordered-outcomes section in the foundation vision one-pager. `brainstorm-vision` elicits or stubs it; `create-vision-companion` derives and indexes it and reserves required fields/IDs; `discover-product` and `define-release` check opportunity selection against it. Strategy reordering is a discovery pivot. Create no standalone strategy skill or stage.
- Make the roadmap optional and ceremony-gated. `tailor-lifecycle` records adoption/skip based on coordination cost, sponsor communication, and product lifetime. When adopted, `define-release` maintains an outcome-based rolling now/next/later view. Do not require it for low-ceremony topics.
- Reopen the `brainstorm-vision`, `create-vision-companion`, `discover-product`, `define-release`, and `validate-release` ledgers and add applicable method-owned rows, including the Strategy section missing from `BV-M01`.

### 11. Complete reference-map row 10

Review lifecycle-tailoring row 10 for all first-class concepts. Candidate finding to confirm or reject: its label names entry points and ceremony but may omit stage/artifact selection, cadence, and decision authority. Confirm that its assessment still covers ceremony drivers, entry points, and the lifecycle one-pager. Apply only confirmed corrections, record the disposition of rejected candidates, and complete the review before accepting the plan.

## Acceptance gate

The revised plan may advance from draft only when all of the following are true:

- [ ] Every fit-analysis [§5.1](./github_skillsets.md#51-integration-map) recommendation maps to a contribution ID; every relevant [§2](./github_skillsets.md#2-per-skillset-analysis) mechanism, benefit, and warning has a final disposition.
- [ ] Ordered updates 1–3 (solution alternatives, deterministic linter, regression validation) are wired into every affected section—artifact table, ID model, trace diagram, skill prose, linter, and rubric—not merely acknowledged in prose.
- [ ] Every accepted contribution has a plan location, authoring destination, and objective verification target. Every deferred design/domain item names its future design-skillset destination.
- [ ] Every method doc maps to all consuming skills; every template, completion check, failure mode, and guardrail has a destination or explicit exclusion.
- [ ] Every `distill` row has a future authoring-time donor-audit task plus license and provenance requirements; incompatible and unlicensed content is not scheduled for copying.
- [ ] Every `call` dependency has a bounded role, version-pinning strategy, fallback, and confirmation that it does not own or write proprietary spine artifacts.
- [ ] Cross-cutting handover, ownership/participation, linter, validation, provenance, skip, and re-entry rules appear in every affected skill and ledger.
- [ ] Artifact table, ID model, trace diagram, skill prose, linter, and validation rubric agree on `SOL#` and `EXP#`.
- [ ] Collaboration/ownership and vision-stability rules have method-owned ledger rows, artifact fields, gates, and passing reference-topic scenarios without new standalone skills/stages or mandatory runtime documents.
- [ ] Post-authoring reconciliation leaves `overview.md`, affected method docs, and implemented skills consistent.
- [ ] The final review finds no unexplained omission against fit-analysis §§2, 3, and 5, all seven ledgers, and this contract.
- [ ] The final review produces `contribution ID → plan section → skill file/test` mappings.
- [ ] The reference map is synchronized, including collaboration/decision ownership and row 10.
- [ ] All planning-bundle links resolve.

The 14 repositories in the fit analysis are the external-source scope for this revision. Reopen affected ledgers before adding sources.
