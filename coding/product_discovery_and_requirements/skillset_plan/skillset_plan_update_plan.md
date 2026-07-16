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

Items are ordered. Items 1–3 close the §1 gaps; items 4–8 ensure the external contributions survive the transition from analysis to plan and then to authored skills; items 9–10 operationalize the cross-cutting method contracts (decision ownership; vision stability).

**Reference-map sync rule (map-wide).** Any edit — by these ordered items or any later revision — that changes a lifecycle element's first-class concept set, its grounding, or a deliberate deviation must update that element's row in the [resources.md reference map](../resources.md#reference-map) in the same edit. This applies to every row, including the cross-cutting collaboration-and-decision-ownership row; it generalizes the rule item 1 previously stated for the discovery row alone.

1. **Close Gap 1 — add solution alternatives to `discover-product` (§5.4 of the plan):**
   - Insert a “generate alternatives” phase between opportunity mapping and assumption exposure, per method doc step 4. Require multiple materially different directions, including process, policy, manual-service, and no-build options where plausible.
   - Add a `SOL#` ID family to the trace model and ID lists; decide whether its durable representation is `solutions.md` or a section of `opportunities.md` and record the decision.
   - Reserve `SOL` in `create-vision-companion`'s Phase 0 ID inventory.
   - Re-anchor `ASM#`: assumptions cite the `SOL#` they belong to, or `OPP#` for genuinely solution-independent assumptions; `EXP#` cards test `ASM`s in the context of a named `SOL` when applicable.
   - Add “alternative solutions were considered” to the wrap-up gate. Refuse to rank solution assumptions when only one direction exists unless an explicit `DEC#` records why alternatives were not viable.
   - Update the artifact table, method-doc coverage table, traceability description, loop diagram, discovery phase description, linter rules, and reference-topic scoring rubric together. The product-discovery row of the [resources.md reference map](../resources.md#reference-map) already names solution alternatives and experiments and cites their lineage (Torres ideation, Bland/Osterwalder, Lean Startup, Mom Test); further changes fall under the map-wide reference-map sync rule above.
2. **Close Gap 2 — add a workspace linter as a first-class component:**
   - Specify a deterministic script, not an LLM skill, that parses the companion bundle and loop workspace.
   - At minimum check ID uniqueness/format, reserved-family collisions, dangling and invalid upward citations, orphaned spine artifacts, `EV` rows without human-supplied source/date/strength, `SOL`/`ASM`/`EXP` relationship validity, `REL`s without hypothesis/success/guardrail/stop criteria, `REQ`s without verification method or explicit open marker, `QAS`s missing any of the six parts (source, stimulus, environment, artifact, response, response measure) or lacking a measurable response measure — with an explicit open marker required where a field is legitimately unresolved (matching specify-requirements-contributions.md lines 47 and 80) — and reserved-name collisions.
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
   - Make [overview.md](../overview.md) a post-authoring deliverable: once the skills are authored, reconcile the collection's entry document — the lifecycle diagram and clarifications, documents list, pragmatic workflow, and minimum useful discovery package — with what was actually built (skill set, artifact schema including the strategy section, ceremony-gated roadmap, `SOL#`, one-pagers, and linter). The skillset update is not complete while overview.md describes a different method than the skills enforce; reconcile any other method doc the implementation diverged from at the same time.

9. **Operationalize collaboration and decision ownership:**
   - Extend `lifecycle-onepager.md` so each consequential decision or stage names one accountable owner, required contributors, specialist authorities, formal approvers, escalation path, and evidence-based reopen trigger; role groups alone are not valid accountable owners.
   - Translate the method contract into applicable behavior and gates for `tailor-lifecycle`, `brainstorm-vision`, `discover-product`, `define-release`, `specify-requirements`, and `validate-release`, while preserving the future design skillset's authority over design decisions.
   - Require early engineering, design, operations, security, compliance, domain, or other specialist participation where feasibility, quality attributes, operational viability, or regulated constraints are material; product management must not manufacture specialist evidence.
   - Preserve collaborative authorship while keeping decision authority explicit: accountability does not imply sole authorship, and consultation does not imply joint accountability.
   - Add reference-topic cases that fail on a group-only owner, missing required specialist or engineering input, a department-boundary handoff, or refusal to reopen upstream artifacts when design or operational evidence invalidates them.
   - Keep these rules inside existing lifecycle and skill artifacts; do not create a standalone ownership skill or mandatory runtime document.

10. **Operationalize vision stability — vision vs. strategy, vision pivots vs. discovery pivots:**
   - Use the glossary terms in skill prose and artifacts: an adapt decision in `discover-product` or a reopening from `validate-release` is a **discovery pivot** — routine, and never a silent edit of the vision.
   - Gate vision changes as **vision pivots**: `brainstorm-vision` and `create-vision-companion` may revise the vision only through an explicit `DEC#` citing the evidence that invalidates the intended future or target need; routine findings must first be routed to opportunities, solutions, scope, or strategy.
   - Extend item 7's `validate-release` backtracking triggers accordingly: only "evidence contradicts a foundational assumption" maps to the vision; all other routes reopen downstream artifacts.
   - Give **product strategy** its recorded home: a thin ordered-outcomes section in the vision companion (with `create-vision-companion` reserving the corresponding fields or ID family). `discover-product` and `define-release` check opportunity selection against it; reordering it on evidence is a routine discovery pivot, requiring no vision-pivot gate. No standalone strategy skill or stage.
   - Make the **product roadmap** a ceremony-gated optional artifact: `tailor-lifecycle` decides adoption per the ceremony drivers (coordination cost, sponsor communication, product lifetime) and records adoption or skip in the lifecycle one-pager; when adopted, `define-release` maintains it as an outcome-based rolling now/next/later view. The linter rejects roadmap entries that name features or dates without an outcome; low-ceremony topics must not be forced to produce one.
   - Add reference-topic cases: a failed experiment wrongly escalated into a vision rewrite (must be refused and rerouted downstream), a genuinely vision-invalidating finding that passes the vision-pivot gate with its `DEC#` and evidence recorded, a low-ceremony topic that correctly skips the roadmap, and a high-coordination topic that adopts and maintains it.

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
- [ ] Vision changes are gated as vision pivots (explicit `DEC#` citing invalidating evidence) in every skill that can touch the vision; discovery and validation findings route downstream first as discovery pivots; product strategy is recorded as a thin ordered-outcomes layer in the vision companion and checked during opportunity selection; the product roadmap is ceremony-gated via `tailor-lifecycle` and outcome-based, rolling, and feature/date-free when adopted; and reference-topic validation covers a wrongly escalated vision rewrite, a genuine vision pivot, a roadmap skip on a low-ceremony topic, and a roadmap adoption on a high-coordination topic.
- [ ] The plan schedules a post-authoring reconciliation of [overview.md](../overview.md) (and any other affected method docs) against the implemented skillset, and completion of the skillset update is gated on the entry document accurately reflecting the achieved results.
- [ ] A final coverage review compares the revised plan against the fit analysis's §§2, 3, and 5, the §1 gaps above, and all seven ledgers and records zero unexplained omissions.
- [ ] The [resources.md reference map](../resources.md#reference-map) agrees with the revised plan: every row whose element's concept set, grounding, or deliberate deviations an ordered edit changed was updated in the same edit per the map-wide sync rule, including the collaboration-and-decision-ownership row.
- [ ] All links in the planning bundle resolve after its move into `skillset_plan/`.

The final coverage review should produce a short change map: contribution ID → plan section → future skill file/test. That change map is the evidence that useful external input was evaluated deliberately rather than merely mentioned.

### 2.5 Scope and housekeeping

Stage-doc housekeeping (the moved `huntsyea/product-skills` URL and deanpeters license annotation) was applied directly on 2026-07-15 and needs no further action.

The product-discovery row of the [resources.md reference map](../resources.md#reference-map) was applied directly on 2026-07-16: its label previously omitted solution alternatives and experiments (both first-class in the method doc's loop and in this plan's Gap 1 and item 6), and its lineage omitted Bland/Osterwalder's *Testing Business Ideas* (assumption mapping, experiment card), *The Lean Startup* (validated learning, pre-declared criteria), and *The Mom Test* (past-behavior evidence discipline). That revision brought those solution-alternative and experiment concepts and their grounding into the row; the non-build-alternatives widening beyond Torres is flagged in its assessment as a deliberate collection choice. It did not, however, name the loop's decide-and-record step (proceed/adapt/pause/abandon) or evidence capture, so the row did not yet name every first-class stage concept — completed in the follow-up recorded at the end of this section. No further action beyond the map-wide sync rule in §2.3.

Two cross-cutting reference-map findings from the row analyses (RefMapAnalysation_Row3–9.md) were applied directly on 2026-07-16: the item-1 sync obligation was generalized into the map-wide reference-map sync rule in §2.3 (with a matching §2.4 gate), and the collaboration-and-decision-ownership contract received its own reference-map row in resources.md (lineage: RACI/DACI, Cagan, Torres, ISO 12207/29148, last responsible moment; assessment flags it as a cross-cutting contract, not a lifecycle stage). Both are removed from the per-row analysis files; the remaining findings there await discussion.

The product-discovery row received a follow-up on 2026-07-16 after the RefMapAnalysation_Row3 review. Its label was extended with **decisions** and **evidence** — the loop's decide-and-record step 7 (proceed/adapt/pause/abandon) and its first-class evidence/`EV#` capture, both previously unnamed — with the decision step grounded via Ries' pivot-or-persevere and Cagan's [Vision Pivots vs. Discovery Pivots](https://www.svpg.com/vision-pivots-vs-discovery-pivots/) (already cited in row 1) and evidence already grounded by *The Mom Test*, so no new external source was introduced. Its assessment now flags the four-way proceed/adapt/pause/abandon vocabulary, each cycle ending in one decision recorded with a single named accountable owner, as this collection's synthesis extending Lean Startup's pivot/persevere and the collaboration-and-decision-ownership contract — parallel to the existing non-build-alternatives flag, and pre-satisfying item 9's effect on this row. With this, the row names every first-class stage concept and the completeness note earlier in this section is corrected accordingly.

The product-definition row (row 4) was revised directly on 2026-07-16 after the RefMapAnalysation_Row4 review, disposing of all five recommendations under the map-wide sync rule (no new external source introduced). Its label gained **opportunity selection** (first-class activity 1, named in the glossary's "Product definition" entry); the release cut was left to row 7 with an assessment pointer rather than duplicated in the label. Its lineage now credits **Patton** for prioritization and release slicing and adds **Wiegers/Beatty** *Software Requirements* for requirements prioritization (both already in the collection), names **Pichler's *Strategize*** (already cited in row 1) as the grounding for the vision–strategy separation, thin ordered-outcomes strategy, and outcome-based rolling roadmap, and recasts **Discover to Deliver** as an early, dated practitioner integration consistent with the Closest-books caveat. Its assessment now states that opportunity selection is checked against the recorded strategy and the roadmap is maintained where adopted (mirroring row 1 and pre-satisfying item 10's effect on this row), and flags the prioritization stance — labeling methods as communication devices over stated criteria, learning value as tie-breaker — as a deliberate collection position, parallel to the row-1 and row-3 deviation flags. With this, the row names every first-class stage concept it owns. The RefMapAnalysation_Row4.md analysis file is marked completed.

The requirements-and-domain-discovery row (row 5) was revised directly on 2026-07-16 after the RefMapAnalysation_Row5 review, disposing of all five recommendations under the map-wide sync rule (no new external source introduced — every cited source is already in the collection). Its label gained **verification** and **traceability** (first-class in requirements_engineering.md's Traceability model section and its "viable verification method" completion check, and mechanical in this plan's linter rules). Its lineage now credits **Wiegers/Beatty** *Software Requirements* for the practitioner process including verification-method selection and traceability (already reading order #4 and Closest books #4), names **Mavin's EARS** for the trigger–response–constraint requirement form (already cited in requirements_engineering.md References and made normative by `specify-requirements` §5.6), adds **example mapping** to the domain-methods list (a co-equal core technique in domain_discovery.md alongside the already-cited EventStorming and Domain Storytelling), and grounds acceptance examples in **Adzic's *Specification by Example*** (already in use_cases_and_story_mapping.md Books). Its assessment now flags two previously unflagged deliberate deviations: the relocation of release-level prioritization to product definition (mirroring row 4 from the RE side), and the typed `EV/OPP → CAP → UC/REQ/QAS` trace spine as this collection's arrangement of standards-required traceability. With this, the row names every first-class stage concept it owns. The RefMapAnalysation_Row5.md analysis file is marked completed.

The quality-attribute-scenarios row (row 6) was revised directly on 2026-07-16 after the RefMapAnalysation_Row6 review, disposing of all four recommendations under the map-wide sync rule. Its label gained **utility-tree prioritization** and **recorded trade-offs** (both first-class in quality_attributes.md alongside the already-named six-part scenario, and already named in this file's own technique index at resources.md line 29 and the glossary's "Utility tree" term). Its lineage now credits **SAiP's evaluation chapters and SEI's ATAM** (Kazman, Klein, Clements) for the utility tree and its trade-off prioritization — attributed through the already-cited Bass/Clements/Kazman rather than as a new external link — and adds the **ISO/IEC 25010** product-quality model (already the basis of ledger row SR-EXT-06) for the common quality-attribute catalog. Its previously terse assessment now flags four deliberate syntheses per the table's flag-the-deviation convention: early-discovery placement of architecture-changing qualities among the riskiest assumptions (with Cagan's feasibility risk), the addition of *uncertainty* to ATAM's importance/difficulty ranking, the SRE/*Release It!*-flavored operational-quality widening, and QAW adopted as inspiration rather than as its full documented step sequence. In the same review, item-2's QAS linter rule (§2.3, formerly "`QAS`s without measurable stimulus/response") was aligned with the ledger's six-field requirement (specify-requirements-contributions.md lines 47 and 80). With this, the row names every first-class stage concept it owns. The RefMapAnalysation_Row6.md analysis file is marked completed.

The coherent-slice row (row 7, "Coherent slice with success and stop criteria") was revised directly on 2026-07-16 after the RefMapAnalysation_Row7 review, disposing of all four recommendations under the map-wide sync rule (no new external source introduced — every cited source is already in the collection). Its label gained **hypothesis** and **guardrail** — the release-definition four-field set (hypothesis, success, guardrail, stop) that is first-class in product_definition.md activity 6 and its one-pager template, defined in the glossary ("Release hypothesis", "Guardrail measure"), and enforced by the `define-release` guardrail and this plan's edit-2 linter rule — becoming "Coherent slice with hypothesis, success, guardrail, and stop criteria" (the row-4 assessment pointer and the label quoted in row 7's own assessment were synced in the same edit). Its lineage now names **Jeff Patton's *User Story Mapping*** (already reading order #2 and Closest books #2) for vertical slicing and story mapping, and adds **Kohavi, Tang, and Xu's *Trustworthy Online Controlled Experiments*** (already cited with its link in the validation-and-feedback row and Closest books #9) for the release hypothesis, pre-declared success measures, and guardrail measures. Its assessment now flags the deliberate synthesis of pulling guardrail definition *forward* into pre-delivery release definition rather than only post-release validation — this collection's choice, not a prescription of either source. Walking skeleton, MVP, appetite/bet-sizing, and instrumentation were confirmed correctly excluded (not first-class element concepts; instrumentation is housed in the validation-and-feedback row). With this, the row names every first-class stage concept it owns. The RefMapAnalysation_Row7.md analysis file is marked completed.

The software-design-implementation-and-release row (row 8) was revised directly on 2026-07-16 after the RefMapAnalysation_Row8 review, disposing of its four recommendations under the map-wide sync rule. Row 8 is structurally unusual — the only lifecycle element with **no stage document in this collection**, because the collection deliberately covers only what happens before and alongside software design and delegates this stage to the neighboring software_design collection and a planned design skillset. R1 and R2 were applied to the assessment: it now states the scope boundary and destination (the [software_design collection](../software_design/software_design.md), already linked under Related local material, plus the planned design skillset — per the §2.4 coverage-gate principle that "out of scope" must name a destination), and names this element's handover contract (the **coherent slice with hypothesis, success, guardrail, and stop criteria** from row 7 and the **readiness-for-software-design checklist** in overview.md), flagging the seven-question checklist as this collection's synthesis over grounded ingredients (Wiegers/Beatty, Bass/Clements/Kazman, Torres) — closing findings F1, F2, and F4. R3 added named grounding to the previously source-less lineage: Humble and Farley's *Continuous Delivery* for the CI/CD tradition the row already invoked but never sourced (the one genuinely new external source, canonical for a tradition already named in the row), Bass/Clements/Kazman's *Software Architecture in Practice* (already Closest books #7) for architecture decisions consuming row 6's `QAS` output, a cross-reference to the *Site Reliability Engineering* material (already row 9 / Closest books #10) for the release-into-operation end, and the dual-track primary sources — Cagan's [Dual-Track Agile](https://www.svpg.com/dual-track-agile/) and Patton's [Dual Track Development is not Duality](https://www.jpattonassociates.com/dual-track-development/) (both authors already in the collection) — supplementing rather than replacing the Agile Alliance experience report; the optional Fowler CI article and Sy 2007 origin paper were left out to keep new authorities minimal. The assessment's evidence-flow clause was also extended so design or operational evidence that invalidates upstream artifacts (edit 9) joins released evidence in informing ongoing discovery. R4 (routing the edit through edit 8's reconciliation) was rejected as moot: its condition ("if R1–R3 are not applied directly") is false, and edit 8's post-authoring reconciliation clause already covers any method doc the implementation diverges from. The RefMapAnalysation_Row8.md analysis file is marked completed.

The validation-and-feedback row (row 9) was revised directly on 2026-07-16 after the RefMapAnalysation_Row9 review, disposing of both recommendations (R1, and R2 accepted in modified form) under the map-wide sync rule (no new external source introduced — every cited source is already in the collection). Its label gained **qualitative signals** and **evidence-routed decisions** — the fourth first-class "What to measure" bullet (validation_and_feedback.md) alongside the already-named outcomes/guardrails/operational-evidence, and the decide-and-record step (persevere/adapt/pause/retire, defined in the glossary and central to edits 7 and 10) plus the reopening-arrow routing. Its lineage now credits **Ries' *The Lean Startup*** pivot-or-persevere for the four-way decision, adds **Google's HEART framework** and **Croll and Yoskovitz's *Lean Analytics*** (both already in the stage's Further material) for qualitative and leading post-release signals, and grounds evidence-strength recording in **Bland and Osterwalder's *Testing Business Ideas*** (already cited in the product-discovery row) — the modified R2, folded into the row lineage as method grounding rather than as a linter/ledger traceability edit. Its assessment now adds a rarity clause (only the vision route is a **vision pivot**, per Interpretation caution 2 and row 1; all other routes are **discovery pivots**), closing finding 7's nit, and flags the four-way **persevere/adapt/pause/retire** vocabulary and the pre-shipping scheduled outcome review with a named owner as this collection's deliberate operating rules, extending Lean Startup's binary pivot-or-persevere through the collaboration-and-decision-ownership contract — parallel to the row-3 decision-vocabulary flag. With this, the row names every first-class stage concept it owns. The RefMapAnalysation_Row9.md analysis file is marked completed.

The 14 repositories inspected for the fit analysis define the external source universe for this revision. The plan may discover additional sources later, but doing so reopens the relevant ledgers rather than bypassing them. The plan and method docs remain authoritative where external advice conflicts with the proprietary spine or the chosen lifecycle.
