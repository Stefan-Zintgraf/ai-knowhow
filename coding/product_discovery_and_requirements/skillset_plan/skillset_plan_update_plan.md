# Skillset Plan Update Plan — Gaps and Revision Contract

**Status:** Normative for the next revision of the [skillset plan](./prod_discovery_requirements_skillset_plan.md)
**Source:** [Existing GitHub Skillsets — Fit Analysis](./github_skillsets.md). That file holds the per-repository analysis, cross-cutting findings, and recommendation; this file holds the actionable consequences — the gaps to close and the plan-adjustment/coverage contract. Read this file when revising the plan; open the fit analysis only when the reasoning behind a specific contribution is needed.

## 1. What the comparison reveals is missing from the plan itself

Beyond the fit analysis's [§5.2 amendments](./github_skillsets.md#52-amendments-to-the-skillset-plan), holding the plan against 14 alternatives exposed three genuine gaps in the plan — not in any external pack's favor, but as blind spots the ecosystem's convergence makes visible. The spine, the two skill modes, the derived-only companion, and tailoring all survived the comparison; these gaps are coverage and assurance problems, not architecture problems.

### Gap 1 — `discover-product` skips its own method doc's "Generate alternatives" step

[product_discovery.md](../product_discovery.md)'s discovery loop step 4 is **"Generate alternatives — multiple materially different ways to address the selected opportunity (including process, policy, manual-service, and no-build options)"**, and step 5 exposes assumptions *per solution*. The plan's §5.4 goes straight from "map opportunities separately from solutions" to "expose and rank assumptions":

- No ideation phase in the skill.
- No artifact and **no ID family for solution candidates** (there is no `SOL#`), so `ASM#` rows have nothing to hang off — "what must be true" is only answerable about a named solution direction.
- The method doc's completion check *"alternative solutions were considered"* has no gate to live in.

This violates design principle 6 (every stage doc consumed in full) and invites the method doc's **first listed failure mode**: "treating discovery as validation of a preferred solution" — assumption testing without named alternatives degenerates into testing the one idea you already had. Every external discovery pack has this step explicitly (Torres's *ideate-solutions* workflow in huntsyea, argo's phase `04-solutions` with its "3+ distinct solutions, PM picks one" rule, phuryn's `brainstorm-ideas`); the ecosystem converged on it for this reason.

### Gap 2 — Zero deterministic enforcement; every gate is the LLM checking its own prose

The plan's value proposition is a typed, cross-referenced artifact graph (14 ID families, every artifact citing upward), yet nothing mechanical ever verifies it: no check for dangling citations, duplicate IDs, orphaned `OPP`s, `EV` rows without a human source, `REQ`s without a verification method, `REL`s without stop criteria. The fit analysis's [§5.2 amendment 4](./github_skillsets.md#52-amendments-to-the-skillset-plan) (a Problem-Based-SRS-style `validate` step) undersells this — that's still the LLM checking itself.

The three best-engineered external projects all pair LLM judgment with **deterministic, non-LLM checks**: `north-star`'s Python validators, Problem-Based-SRS's mechanical traceability validation, ForceInjection's scored verification. The missing component is a **workspace linter** — a script, not a skill — that parses the loop workspace and reports spine violations; runnable by every skill's finalize gate, as a Claude Code hook, or in CI. Guardrails that matter ("an `EV` row without a human-supplied source is invalid") should be enforced by code where they are code-checkable.

### Gap 3 — No validation strategy for the skillset itself

The plan proposes five new skills plus two adjustments with no worked reference topic, no acceptance test, and no open question asking "how do we know the skills work." ForceInjection blind-runs its skill chain against a canonical reference case (the Cargo DDD sample), scores the output against ground truth, and feeds failures back into the skills — a feedback loop the plan lacks entirely. Since these skills exist to enforce discipline on a human, an untested enforcement mechanism is a real risk. Minimum viable version: one small worked topic (real or synthetic) run end-to-end through the loop after each skill is authored, with the method docs' completion checks as the scoring rubric.

*(A debatable fourth gap — deanpeters and argo treat teaching the practitioner as a co-equal goal ("Always Be Coaching", the learning system), while the plan treats the human purely as evidence supplier — is judged a deliberate non-goal for a solo expert workflow, not a miss.)*

### New normative method input — collaboration and decision ownership

[Collaboration and Decision Ownership](../collaboration_and_decision_ownership.md) was created after the external fit analysis and is therefore not a fourth comparison gap. It is a new cross-cutting method contract: lifecycle stages are not department boundaries, consequential decisions have one named accountable owner, and required contributors, specialist authorities, approvers, escalation paths, and reopen triggers are explicit.

The next plan revision must operationalize this contract across every affected skill. A link in the method-doc coverage table is necessary but not sufficient: its rules require ledger rows, skill behavior, lifecycle-onepager fields, gates, and reference-topic scenarios. It does **not** justify a standalone skill or a separate runtime artifact.

## 2. Plan-adjustment and contribution-coverage contract

The next revision of [prod_discovery_requirements_skillset_plan.md](./prod_discovery_requirements_skillset_plan.md) must maximize justified reuse without weakening the proprietary traceability spine. “Use all the goodies” therefore means **every relevant contribution identified in the fit analysis is deliberately dispositioned and evidenced**; it does not mean copying every external technique regardless of fit, quality, scope, or license.

This section is normative for the plan revision. The revision is incomplete until all ordered edits and the coverage gate in §2.4 pass.

### 2.1 Per-skill contribution ledgers

Each adjusted or new proprietary skill has a companion ledger. These files turn the prose findings in the fit analysis's §§2, 3, and 5 and the gaps in §1 above into authoring requirements:

| Skill | Contribution and coverage file |
| --- | --- |
| `brainstorm-vision` | [brainstorm-vision-contributions.md](./brainstorm-vision-contributions.md) |
| `create-vision-companion` | [create-vision-companion-contributions.md](./create-vision-companion-contributions.md) |
| `tailor-lifecycle` | [tailor-lifecycle-contributions.md](./tailor-lifecycle-contributions.md) |
| `discover-product` | [discover-product-contributions.md](./discover-product-contributions.md) |
| `define-release` | [define-release-contributions.md](./define-release-contributions.md) |
| `specify-requirements` | [specify-requirements-contributions.md](./specify-requirements-contributions.md) |
| `validate-release` | [validate-release-contributions.md](./validate-release-contributions.md) |

Every ledger row has a stable contribution ID, source and license, reuse mode, intended incorporation, disposition, and objective evidence that must exist in the revised plan or authored skill. Allowed dispositions are:

- **Adopt** — use the contribution substantially as identified.
- **Adapt** — preserve the mechanism while translating it onto this collection's method and ID spine.
- **Call** — use a version-pinned external specialist without allowing it to own spine artifacts.
- **Reject** — deliberately do not use it, with a recorded fit, quality, duplication, or license reason.
- **Defer** — preserve it for a named later skillset or decision, with an explicit destination.

`Pending` is a working state, not an acceptable final disposition. “Mentioned in the plan” is not sufficient evidence: an accepted contribution must point to the artifact field, phase, prompt/guardrail, finalize check, integration contract, linter rule, or validation scenario that realizes it.

Because the collaboration and decision-ownership contract is a proprietary method input rather than an external contribution, each affected ledger must also contain method-owned rows for its applicable rules. Those rows need stable local IDs, intended incorporation, and objective evidence, but no external license or reuse-mode disposition.

### 2.2 Source-audit rule

The ledgers cover every contribution already identified by the fit analysis. During skill authoring, each `distill` row must also receive a focused audit of the exact donor files assigned to that skill. This protects against losing useful details that were compressed out of the repository-level summaries.

For each audited donor, record:

1. repository and file path;
2. commit/tag or retrieval date;
3. license and attribution requirement;
4. candidate techniques, questions, rubrics, templates, failure modes, and checks found;
5. one disposition for every candidate; and
6. the resulting local skill file and section for every adopted/adapted item.

This is an **authoring-time audit**, never a runtime fetch. Distilled material is vendored with provenance; callable specialists are version-pinned. CC BY-NC-SA material from `deanpeters/Product-Manager-Skills` may inspire a pattern but must not be copied or distilled. Unlicensed material is reference-only unless permission is established.

### 2.3 Ordered plan edits

Items are ordered. Items 1–3 close the §1 gaps; items 4–8 ensure the external contributions survive the transition from analysis to plan and then to authored skills; item 9 operationalizes the new cross-cutting method contract.

1. **Close Gap 1 — add solution alternatives to `discover-product` (§5.4 of the plan):**
   - Insert a “generate alternatives” phase between opportunity mapping and assumption exposure, per method doc step 4. Require multiple materially different directions, including process, policy, manual-service, and no-build options where plausible.
   - Add a `SOL#` ID family to the trace model and ID lists; decide whether its durable representation is `solutions.md` or a section of `opportunities.md` and record the decision.
   - Reserve `SOL` in `create-vision-companion`'s Phase 0 ID inventory.
   - Re-anchor `ASM#`: assumptions cite the `SOL#` they belong to, or `OPP#` for genuinely solution-independent assumptions; `EXP#` cards test `ASM`s in the context of a named `SOL` when applicable.
   - Add “alternative solutions were considered” to the wrap-up gate. Refuse to rank solution assumptions when only one direction exists unless an explicit `DEC#` records why alternatives were not viable.
   - Update the artifact table, method-doc coverage table, traceability description, loop diagram, discovery phase description, linter rules, and reference-topic scoring rubric together.
2. **Close Gap 2 — add a workspace linter as a first-class component:**
   - Specify a deterministic script, not an LLM skill, that parses the companion bundle and loop workspace.
   - At minimum check ID uniqueness/format, reserved-family collisions, dangling and invalid upward citations, orphaned spine artifacts, `EV` rows without human-supplied source/date/strength, `SOL`/`ASM`/`EXP` relationship validity, `REL`s without hypothesis/success/guardrail/stop criteria, `REQ`s without verification method or explicit open marker, `QAS`s without measurable stimulus/response, and reserved-name collisions.
   - Define which checks are deterministic and which remain judgment gates. Every artifact-producing skill must run the applicable deterministic checks at finalize; CI/hook integration may be optional, but the finalize contract is not.
   - This absorbs the Problem-Based-SRS `validate` pattern while retaining this collection's trace spine.
3. **Close Gap 3 — add a skillset validation strategy:**
   - Define one small worked reference topic that runs end-to-end after each skill is authored or materially changed.
   - Score it against the method docs' completion checks, the per-skill coverage gates, linter results, handover correctness, and re-entry behavior.
   - Include at least one low-ceremony path, one skipped-stage path with recorded reason, one weak-evidence case, one single-solution exception, one requirements gap requiring human review, and one post-release result that reopens an earlier artifact.
   - Record failures and feed them back into the skill or plan; passing once does not waive regression runs after relevant changes.
4. **Apply every per-skill ledger:**
   - Add the accepted contribution IDs to the relevant per-skill sections in the plan, with the concrete mechanism that will realize each contribution.
   - Extend the skills table with callable specialists (`north-star`; conditionally `quality-attribute-scenario-writer`) and state their bounded role, version policy, inputs, outputs, and fallback.
   - Add cross-cutting contributions—handover UX, decision ownership and required participation, linter invocation, provenance, deterministic validation, and backtracking triggers—to every affected skill rather than mentioning them once globally.
   - Preserve rejected and deferred rows in the ledgers; do not silently delete them after deciding not to adopt them.
5. **Add the external-dependency and provenance policy:**
   - `call` = version-pinned install with a bounded contract and fallback;
   - `distill` = vendored content with source file, commit/tag or retrieval date, license, and attribution;
   - `pattern` = locally expressed mechanism with the inspiration recorded but no runtime dependency;
   - never runtime-fetch third-party repositories; and
   - never distill content whose license is incompatible with the intended use.
6. **Adopt the strengthened `EXP#` card:**
   - Merge the method doc's experiment-card template with shinpr's hypothesis fields: success, failure, and inconclusive criteria; confidence per relevant risk dimension; time budget; target `ASM#`; applicable `SOL#`; result; and resulting `DEC#`.
   - Make the schema and its required/open fields linter-visible.
7. **Formalize handover and re-entry contracts:**
   - Every skill ends by naming the next applicable stage from `lifecycle-onepager.md`, the artifacts changed, unresolved decisions, and the exact gate that allows progression.
   - Express `validate-release` backtracking triggers as explicit conditions mapping evidence to the artifact/skill reopened, following the ForceInjection pattern.
   - Record intentional skips; never let command chaining silently override lifecycle tailoring.
8. **Add plan-to-authoring traceability:**
   - Give each accepted ledger row a plan location and planned skill-file destination.
   - When a skill is authored, replace planned evidence with the actual file/section/test reference.
   - Treat method-doc changes, donor-version changes, and altered artifact schemas as triggers to reopen the affected ledger rows and rerun their gates.

9. **Operationalize collaboration and decision ownership:**
   - Extend `lifecycle-onepager.md` so each consequential decision or stage names one accountable owner, required contributors, specialist authorities, formal approvers, escalation path, and evidence-based reopen trigger; role groups alone are not valid accountable owners.
   - Translate the method contract into applicable behavior and gates for `tailor-lifecycle`, `brainstorm-vision`, `discover-product`, `define-release`, `specify-requirements`, and `validate-release`, while preserving the future design skillset's authority over design decisions.
   - Require early engineering, design, operations, security, compliance, domain, or other specialist participation where feasibility, quality attributes, operational viability, or regulated constraints are material; product management must not manufacture specialist evidence.
   - Preserve collaborative authorship while keeping decision authority explicit: accountability does not imply sole authorship, and consultation does not imply joint accountability.
   - Add reference-topic cases that fail on a group-only owner, missing required specialist or engineering input, a department-boundary handoff, or refusal to reopen upstream artifacts when design or operational evidence invalidates them.
   - Keep these rules inside existing lifecycle and skill artifacts; do not create a standalone ownership skill or mandatory runtime document.

### 2.4 Coverage gate for accepting the revised plan

The revised skillset plan may advance from draft only when all of the following are true:

- [ ] Every recommendation in the fit analysis's [§5.1 integration map](./github_skillsets.md#51-integration-map) maps to at least one per-skill contribution ID.
- [ ] Every relevant mechanism, benefit, and warning identified in the fit analysis's [§2 per-skillset analysis](./github_skillsets.md#2-per-skillset-analysis) has an `Adopt`, `Adapt`, `Call`, `Reject`, or `Defer` disposition; no row remains `Pending`.
- [ ] Every §1 gap is closed in all affected plan sections, not only acknowledged in prose.
- [ ] Every accepted contribution has a concrete plan location and objective verification target; “consider during authoring” is not accepted as a terminal state.
- [ ] Every method doc maps to its consuming skill and every template, completion check, failure mode, and guardrail has a planned destination or explicit reason for exclusion.
- [ ] Every `distill` source has a future source-audit task plus license/provenance requirements; incompatible and unlicensed content is not scheduled for copying.
- [ ] Every `call` dependency has a bounded role, version pinning strategy, fallback, and confirmation that it does not write proprietary spine artifacts.
- [ ] Cross-cutting mechanisms appear in every affected skill ledger: lifecycle-aware handover, applicable linter checks, reference-topic validation, and explicit re-entry/skip behavior.
- [ ] The artifact table, ID model, trace diagram, per-skill prose, linter specification, and validation rubric agree on `SOL#` and the strengthened `EXP#` schema.
- [ ] Deferred design/domain material has a named destination in the future design-skillset backlog; “out of scope” is not allowed to mean “forgotten.”
- [ ] The collaboration and decision-ownership method input maps to method-owned rows in every affected ledger and to concrete skill behavior, artifact fields, gates, and validation scenarios.
- [ ] Every consequential decision represented by the plan has one named accountable owner plus applicable contributors, specialist authorities, approvers, escalation path, and reopen trigger; a department or role group alone is not accepted as the owner.
- [ ] Reference-topic validation covers group-only ownership, missing specialist or engineering participation, department-boundary handoffs, and evidence-driven reopening during design or operation.
- [ ] The ownership rules remain cross-cutting requirements of existing skills and artifacts; no standalone skill or mandatory runtime artifact has been introduced.
- [ ] A final coverage review compares the revised plan against the fit analysis's §§2, 3, and 5, the §1 gaps above, and all seven ledgers and records zero unexplained omissions.
- [ ] All links in the planning bundle resolve after its move into `skillset_plan/`.

The final coverage review should produce a short change map: contribution ID → plan section → future skill file/test. That change map is the evidence that useful external input was evaluated deliberately rather than merely mentioned.

### 2.5 Scope and housekeeping

Stage-doc housekeeping (the moved `huntsyea/product-skills` URL and deanpeters license annotation) was applied directly on 2026-07-15 and needs no further action.

The 14 repositories inspected for the fit analysis define the external source universe for this revision. The plan may discover additional sources later, but doing so reopens the relevant ledgers rather than bypassing them. The plan and method docs remain authoritative where external advice conflicts with the proprietary spine or the chosen lifecycle.
