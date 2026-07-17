# Authoring Assurance: `specify-requirements`

**Status:** Required authoring contract  
**Applies to:** `specify-requirements` skill implementation and every material revision  
**Primary outputs:** `releases/REL<n>-requirements.md`, `quality-scenarios.md`

**Planning sources:** [skillset plan](./prod_discovery_requirements_skillset_plan.md) · [GitHub skillset fit analysis](./github_skillsets.md)  
**Primary method sources:** [Requirements engineering](../requirements_engineering.md) · [Use cases and story mapping](../use_cases_and_story_mapping.md) · [Quality attributes](../quality_attributes.md)

## 1. Purpose and scope

This file ensures that requirements rigor is preserved while external techniques are used only where they strengthen the proprietary traceability spine.

The skill must transform a committed release slice into reviewable use cases, requirements, quality-attribute scenarios, constraints, and verification intent. It may draft content autonomously, but it may not silently invent stakeholder judgment, domain rules, failure behavior, or measurable targets.

The skill is authoring-complete only when its builder/reviewer separation, deterministic linter, QAS/NFR gates, human confirmation points, and downstream handover have all been verified. Allowed contribution dispositions are `adopt`, `adapt`, `call` (a version-pinned specialist with a bounded contract that never owns spine artifacts), `reject`, or `defer`; no row may remain `pending`.

## 2. External-contribution ledger

Before authoring, replace every source pointer with the exact repository URL, commit SHA or release, files inspected, retrieval date, and verified license.

| ID | Source | Exact contribution to assess | Mode | Required incorporation | Disposition | License and provenance requirement | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SR-EXT-01 | `shinpr/claude-code-discover` — `hypothesis-verifier` | Context-separated verification in which the critic does not inherit the author’s expectations | pattern | Run the requirements critic in a separate context. Give it authoritative source artifacts, candidate outputs, schemas, and gates, but not builder reasoning or expected conclusions | adopt | MIT; record exact verifier/agent files and commit | Seeded plausible errors are detected by the critic; reviewer result is stable when builder rationale is removed |
| SR-EXT-02 | `shinpr/claude-code-discover` — repository product context and index discipline | Durable in-repo context, explicit rejected alternatives, maintained indexes, implementation handoff | pattern | Keep artifacts in the proprietary workspace; preserve explicit unresolved/rejected choices and ensure indexes/handover remain current | adapt | MIT; exact files and commit required | Stale-index and missing-rejected-alternative fixtures fail validation |
| SR-EXT-03 | `RafaelGorski/Problem-Based-SRS` — `validate` action | Mechanical validation of a complete trace chain | pattern | Implement a workspace linter for the proprietary chain `EV/OPP -> CAP -> UC/REQ/QAS`, including rationale and verification links; do not introduce `.spec` JSON or `CP/CN/FR` IDs | adapt *(finalized in revision-contract update 4)* | MIT; record exact validation action/reference files and commit | Final rationale (update 4): adapt — the mechanical-validation mechanism is translated onto the proprietary spine as the shared `lint-workspace` script (plan §2.2), while the donor's `.spec` JSON and `CP/CN/FR` taxonomy are explicitly excluded; that translation is Adapt, not Adopt-as-identified. Positive, broken-link, orphan, duplicate-ID, and missing-rationale fixtures |
| SR-EXT-04 | `RafaelGorski/Problem-Based-SRS` — problem/need/requirement discipline | Preserve the reason behind each requirement and distinguish externally mandatory needs from expectations and hopes | pattern | Consume the O/E/H classification from `REL`; require each `REQ/QAS` to trace to a need, risk, constraint, or obligation and preserve the consequence/rationale | adapt | MIT; exact source audit required | Orphan requirement and unsupported “shall” fixtures fail |
| SR-EXT-05 | `45ck/software-architecture-skills` — `quality-attribute-scenario-writer` | Potential specialist support for six-part QAS construction | conditional call | Audit actual skill depth first. Call only if it materially exceeds the local QAS reference, is version-pinned, and returns content for validation through the proprietary gate | call, conditional *(finalized in revision-contract update 4; condition explicit — see verification)* | Reported MIT; verify exact skill, repository license, commit, examples, and generated-pack depth | Final adoption condition (update 4, wired into plan §3.1): the call is adopted only if the authoring-time depth audit shows all three legs pass — (a) the specialist materially exceeds the local QAS reference ([quality_attributes.md](../quality_attributes.md): six parts, utility tree, trade-offs, operational quality); (b) the repository license, exact skill files, commit, examples, and generated-pack depth are verified; (c) a comparative fixture scores called output at least as well as local-only output through the same QAS gate (§6, dimensions per SR-EXT-07). If any leg fails, the row converts to `reject` and the skill uses local QAS drafting per SR-MTH-07. The specialist drafts candidate scenarios only; it never owns or writes spine artifacts, and every candidate passes the proprietary QAS gate before a `QAS#` is assigned |
| SR-EXT-06 | `DavidROliverBA/Daves-Claude-Code-Skills` — `nfr-capture` | ISO 25010-oriented NFR capture with measurable criteria | pattern | Use relevant completeness prompts without importing Obsidian schemas, tags, or vault layout | adapt | Verify repository/file license before using any content; pattern-level use only until confirmed | QAS coverage fixture includes relevant operational and stakeholder consequences without checklist inflation |
| SR-EXT-07 | `DavidROliverBA/Daves-Claude-Code-Skills` — `nfr-review` | Review dimensions: complete, measurable, feasible; independent review lanes | pattern | Make completeness, measurability, and feasibility explicit QAS gate dimensions. Separation is mandatory; multi-agent fan-out is optional, not required | adapt *(finalized in revision-contract update 4)* | Verify exact license and files; no vault-coupled material | Final rationale (update 4): adapt — the complete/measurable/feasible review dimensions are translated into the proprietary QAS gate (§6) with independent review lanes kept optional and the license unverified, so nothing is used as identified. Each QAS receives three recorded gate results; seeded defects fail the matching dimension |
| SR-EXT-08 | `huntsyea/product-skills` — `story-mapping` | Alternatives, failures, handoffs, operational tasks, and slice boundaries discovered during story mapping | distilled upstream input | Validate and elaborate the committed story-map slice into use cases; do not recreate release scope or silently add out-of-scope stories | adapt | MIT; record exact files, commit, and retrieval date | UC elaboration fixture preserves slice boundary while surfacing unresolved paths |
| SR-EXT-09 | `deanpeters/Product-Manager-Skills` — `user-story-mapping` | Additional story-map question sequences | reference only | Compare for conceptual gaps; use the method doc and MIT donor as implementation sources | reject for distillation | CC BY-NC-SA 4.0; no copying or distillation | Audit records comparison and confirms no protected content entered the skill |
| SR-EXT-10 | `phuryn/pm-skills` — command chaining | Explicit next-stage handover | pattern | Final output names design-readiness status, exact artifacts, open questions, required human confirmations, validation hooks, and next workflow selected by tailoring | adopt | Pattern only; cite inspected commands and commit | Downstream consumer starts from durable artifacts without chat history |
| SR-EXT-11 | `ForceInjection/domain-driven-design-skills` | Backtracking triggers and validation thresholds | pattern | Define triggers returning to `define-release`, `discover-product`, `domain-modeling`, or human confirmation instead of forcing completion | adapt | WIP; record exact files, commit, language/version, and provenance | Every failed gate routes to a named artifact and owner |
| SR-EXT-12 | `ddd-crew/ddd-starter-modelling-process`, `ForceInjection` tactical DDD skills, and `lagz0ne/design-skill` | Strategic/tactical modeling and requirements-to-design catalogs | reference/defer | Preserve as candidates for the future design skillset; use existing `domain-modeling` only when requirements reveal domain gaps | defer | CC BY 4.0 / WIP or repository-specific terms; verify during design planning | Exclusion review confirms that `specify-requirements` does not produce architecture prematurely |

## 3. Method-document coverage ledger

| ID | Method document | Required use in `specify-requirements` | Verification |
| --- | --- | --- | --- |
| SR-MTH-01 | [Overview](../overview.md) | Preserve the discovery-definition-requirements lifecycle, minimum useful package, and readiness-for-design exit criteria | End-to-end readiness fixture |
| SR-MTH-02 | [Lifecycle tailoring](../lifecycle_tailoring.md) | Respect topic entry point, selected artifacts, ceremony, decision authority, and explicit skips | Compliance-entry and low-ceremony fixtures |
| SR-MTH-03 | [Product definition](../product_definition.md) | Treat `REL` scope, hypothesis, deferrals, constraints, instrumentation intent, and O/E/H classing as authoritative inputs | Scope-drift fixture fails |
| SR-MTH-04 | [Requirements engineering](../requirements_engineering.md) | Implement all requirement types, six-step process, sentence guidance, trace rationale, prioritization, change policy, failure guardrails, and completion checks | Field and process conformance suite |
| SR-MTH-05 | [Use cases and story mapping](../use_cases_and_story_mapping.md) | Elaborate actor goals, guarantees, main flow, extensions, rules, qualities, open questions, and acceptance examples | UC completeness and failure-path tests |
| SR-MTH-06 | [Domain discovery](../domain_discovery.md) | Trigger canonical domain work for contested terminology, tacit rules, invariants, ownership, or context meanings; feed results back without duplicating artifacts | Domain-gap routing test |
| SR-MTH-07 | [Quality attributes](../quality_attributes.md) | Use all six QAS parts, stakeholder consequence, trade-offs, operational quality, ranking where warranted, and verification method | Complete/measurable/feasible QAS suite |
| SR-MTH-08 | [Validation and feedback](../validation_and_feedback.md) | Specify production observation for outcome and guardrail measures; preserve transition requirements and later trace to observed outcomes | Instrumentation and retirement fixtures |
| SR-MTH-09 | [Product vision](../product_vision.md) | Preserve actors, principles, boundaries, outcome signals, and architecture-lens seeds through references rather than reinvention | Vision-conflict routes upstream |
| SR-MTH-10 | [Product discovery](../product_discovery.md) | Resolve upstream evidence, opportunity, assumption, and experiment rationale in the trace chain | Broken-upstream-trace fixture |
| SR-MTH-11 | [Glossary](../glossary.md) | Apply canonical method language and distinguish method glossary from domain language | Terminology lint |
| SR-MTH-12 | [Resources](../resources.md) | Select elicitation, modeling, and validation techniques proportionate to uncertainty and ceremony | Authoring trace records why each technique is used |

### Method-owned rows (collaboration and decision ownership — revision-contract update 9)

Method-owned rows carry no external license or disposition (revision-contract ledger rules).

| ID | Method document | Required use in `specify-requirements` | Verification |
| --- | --- | --- | --- |
| SR-M01 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — singular accountable ownership (core rules 2–3, decision language) | Every consequential requirements decision the human gate resolves — invented failure paths, target values, domain rules, scope changes, consequential trade-offs — is recorded in its `DEC#` with the one named accountable owner from `lifecycle-onepager.md`'s decision-authority record (plan §5.3, §5.6); a group or department as owner is refused; the handover lists unresolved decisions with their owners | Regression scenario RTS-07: a group-only owner is detected and refused; fixture: a `DEC#` without a named individual owner fails the finalize check |
| SR-M02 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — specialist verdicts on feasibility (core rule 4) | The QAS gate's Feasible dimension (§6) passes only on a recorded engineering/domain/operations/security reviewer verdict or a blocking-uncertainty `OPEN:` marker escalated to the human gate — never auto-passed (plan §5.6) | Regression scenario RTS-08: missing required specialist/engineering input is detected and refused; fixture: Feasible marked pass without recorded reviewer evidence fails the gate |
| SR-M03 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — no fabricated specialist evidence (core rules 4–5) | The builder must not invent stakeholder judgment, domain rules, failure behavior, or measurable targets as settled fact: inventions stay flagged proposals that cannot pass as completed values (§4 step 2, LNT-05), and the critic checks for unmarked invention (plan §5.6) | Mutation fixture: a proposal silently converted to a confirmed value is caught by the linter or critic; a seeded fabricated "engineering says feasible" claim fails review (RTS-05, RTS-08) |
| SR-M04 | [Collaboration and decision ownership](../collaboration_and_decision_ownership.md) — evidence-based reopening; refusal to proceed on invalidated upstream artifacts (core rule 6, tailoring the defaults) | Failed gates route to the named upstream artifact with the owner and escalation path from the one-pager (SR-EXT-11); the skill refuses to elaborate a `REL` slice whose upstream `OPP`/`ASM`/`REL` has been invalidated unless perseverance is recorded with its rationale as a `DEC#` (plan §5.6) | Regression scenarios RTS-10 (refusal to reopen invalidated upstream artifacts) and RTS-05 (requirements gap needing human review) pass; every failed gate names artifact and owner |

## 4. Builder/reviewer protocol

1. The builder reads the committed `REL`, referenced companion artifacts, discovery artifacts, domain artifacts, lifecycle one-pager, and applicable method references.
2. It drafts use cases, `REQ#`, and `QAS#` outputs. Any invented path, target, term, or rule is marked as a proposal requiring confirmation.
3. The mechanical linter runs before semantic review.
4. A fresh critic context receives:
   - authoritative input artifacts;
   - candidate requirements and QAS outputs;
   - schemas, completion gates, and lint results;
   - no builder reasoning, expected verdict, or persuasive summary.
5. The critic checks correctness, omissions, scope drift, traceability, ambiguity, QAS completeness/measurability/feasibility, and verification viability.
6. The human gate resolves invented failure paths, conflicting stakeholder needs, target values, domain rules, and consequential trade-offs.
7. The builder applies approved corrections and reruns linter and critic.
8. Remaining uncertainty is preserved in durable open markers and `DEC` entries; it is never silently converted into a requirement.

## 5. Deterministic checks

The workspace linter must validate at least:

- Unique and syntactically valid `REQ#` and `QAS#` identifiers.
- All referenced `REL#`, `EV#`, `OPP#`, `CAP#`, `UC#`, `BR#`, `INV#`, `DEC#`, and constraints resolve.
- No `REQ/QAS` lies outside committed `REL` scope without an explicit change decision.
- Each important requirement traces to a capability/use case and to a need, risk, constraint, or obligation, with rationale.
- Every requirement has type, normative statement or justified alternative notation, verification method, status, and source.
- Open markers are machine-recognizable and cannot pass as completed values.
- Important UC alternative, failure, permission, cancellation, and minimal-guarantee paths are present or explicitly not applicable.
- Every QAS contains source, stimulus, environment, artifact, response, and measurable response measure.
- Every critical QAS identifies stakeholder/business consequence, expected scale/workload where relevant, verification method, and trade-off/priority where qualities conflict.
- Each outcome/guardrail criterion has an instrumentation or observation requirement.
- Transition requirements exist for migration, coexistence, rollout, training, decommissioning, or retired scope when applicable.
- Index and handover references match files actually present.

## 6. QAS/NFR gate

Every critical quality concern must pass:

| Dimension | Pass condition |
| --- | --- |
| Grounded | Traces to a stakeholder consequence, evidence, risk, obligation, or explicit decision |
| Complete | Contains all six scenario parts and relevant operational/failure conditions |
| Measurable | Response measure, units, threshold/range, and observation method are explicit |
| Feasible | Engineering/domain reviewer finds a viable realization path or records a blocking uncertainty |
| Verifiable | A concrete review, test, analysis, monitoring, or inspection method exists |
| Prioritized | Importance and architectural difficulty/uncertainty are recorded where risk warrants |
| Trade-off aware | Conflicting qualities have an explicit priority or unresolved decision |
| Traceable | Architectural work can later point back to the `QAS#` without inventing rationale |

## 7. Authoring coverage gate

- [ ] Every external row has a final disposition and reason.
- [ ] Every adopted contribution links to its concrete implementation and test.
- [ ] Source files, commit, date, license, notices, and redistribution implications are verified.
- [ ] Conditional `45ck` reuse has a recorded depth comparison and fallback.
- [ ] The builder and critic run in separated contexts.
- [ ] Human confirmation is required for invented paths, rules, target values, and scope changes.
- [ ] All method rows map to skill references, templates, prompts, guardrails, or tests.
- [ ] UC, REQ, QAS, instrumentation, transition, and change-policy gates are implemented.
- [ ] Complete/measurable/feasible NFR checks each have positive and negative fixtures.
- [ ] The linter detects every intentional broken trace, duplicate ID, orphan, missing verification method, unresolved open marker, and incomplete QAS.
- [ ] Low-ceremony mode can produce a minimum useful specified slice without weakening load-bearing gates.
- [ ] High-risk mode supports full traceability, utility-tree prioritization, and formal review.
- [ ] Handover identifies readiness-for-design status, exact artifacts, open decisions, and correct upstream re-entry points.

## 8. Cross-cutting skillset validation

The shared validation strategy must include:

1. A full reference topic from vision companion through discovery, `REL`, `REQ/QAS`, release review, and targeted re-entry.
2. Entry-point fixtures for greenfield, fast-follow, compliance mandate, rework, and platform initiatives.
3. Low-, medium-, and high-ceremony variants.
4. Golden-schema tests plus semantic fixtures; snapshots alone are insufficient.
5. Mutation tests that break one trace link, remove one QAS field, introduce vague language, cross the release boundary, omit a failure path, or remove a verification method.
6. Blind critic runs and human-resolution fixtures.
7. Round-trip tests showing that an approved requirement change updates affected traces, tests, instrumentation, and decisions.
8. Source-coverage and license/provenance gates for every external contribution.

## 9. Exclusions and deferrals

- Do not adopt the Problem-Based-SRS identifier taxonomy or `.spec` workspace.
- Do not adopt Shinpr’s PRD/lifecycle taxonomy.
- Do not import Dave’s Obsidian frontmatter, vault, or tag ecosystem.
- Do not use Dean Peters material as a distillation source.
- Do not accept a generated QAS specialist without the proprietary QAS gate.
- Do not make multi-agent fan-out mandatory; independent context and objective gates are mandatory.
- Do not design services, aggregates, interfaces, UI, or data architecture.
- DDD tactical design, EventStorming-to-design catalogs, architecture trade-off analysis, and interface design remain in the future design skillset.

## 10. Plan-to-authoring traceability (revision-contract update 8)

Maps every accepted row to its plan location and **planned** skill-file destination (paths relative to the future `skills/specify-requirements/` directory; the skill is not authored yet). Governing rules — replace-planned-with-actual, reopen, date capture, post-authoring reconciliation — are in [plan §3.3](./prod_discovery_requirements_skillset_plan.md), whose donor-audit task table carries this ledger's distill row (SR-EXT-08, sharing DR-EXT-01's provenance record). **Date capture:** the §2 preamble's replace-every-source-pointer instruction (exact repository URL, commit SHA/release, files inspected, retrieval date, verified license) is an explicit authoring-time task for every external row (plan §3.3); no row records these values yet. The method-coverage rows SR-MTH-01..12 each have their own plan location, planned file/section, and objective fixture, linter check, or regression target below; SR-MTH-07 backs the §3.1 specialist fallback and SR-MTH-08 owns the LNT-09/10/12 instrumentation/transition chain.

| Row | Plan § | Planned destination (path/section) |
| --- | --- | --- |
| SR-EXT-01 | §5.6 | Fresh-critic protocol in the orchestration (`SKILL.md` + critic-brief template; ledger §4 steps 3–5) |
| SR-EXT-02 | §5.6, LNT-04 | Durable-workspace rules: rejected/unresolved alternatives preserved; index/handover consistency |
| SR-EXT-03 | §2.2, §5.6 | Shared `lint-workspace` wiring for the `EV/OPP → CAP → UC/REQ/QAS` chain (no `.spec` JSON, no `CP/CN/FR`) |
| SR-EXT-04 | §2.2 (LNT-16), §5.6 | Trace-rationale fields on `REQ#`/`QAS#` templates consuming O/E/H from the `REL` |
| SR-EXT-05 | §3.1, §5.6 | Conditional `quality-attribute-scenario-writer` call step (depth-audit condition, pin, local-drafting fallback per plan §3.1) |
| SR-EXT-06 | §5.6 | QAS elicitation prompts (ISO 25010-flavoured, no Obsidian schemas) |
| SR-EXT-07 | §5.6 | QAS gate dimensions Complete/Measurable/Feasible in the gate rubric (ledger §6) |
| SR-EXT-08 | §3.3, §5.6, LNT-16 | UC-elaboration guidance bound to the committed story-map slice; slice-boundary fixture |
| SR-EXT-09 | reject (for distillation) | — no destination; documented comparison only |
| SR-EXT-10 | §4.1, §5.6 | Final-output handover section (design-readiness status, artifacts, open questions, confirmations, next workflow) |
| SR-EXT-11 | §4.2, §5.6 | Failed-gate backtracking routes (named target artifact + owner) |
| SR-EXT-12 | defer → future design skillset | — no destination; interim behavior via `domain-modeling` (plan §3.1) |
| SR-MTH-01 | §2.1, §4, §5.6, §6 | `SKILL.md` sections **Lifecycle position** and **Readiness-for-design gate**; reference-topic fixture `fixtures/specification-to-readiness` verifies the specified slice closes the loop without pretending uncertainty is absent |
| SR-MTH-02 | §2.1, §4.1, §5.3, §5.6, §6 | `SKILL.md` start gate **Read lifecycle one-pager** and ceremony/skip controls; `fixtures/tailored-specification` covers compliance entry, low ceremony, explicit skips, and authority (RTS-01/RTS-02) |
| SR-MTH-03 | §2 (`REL` input), §2.1, §2.2 (LNT-15, LNT-16), §§5.5–5.6 | `SKILL.md` section **Authoritative release boundary**; `fixtures/rel-scope-drift` fails unapproved scope expansion, changed deferrals/constraints, or lost O/E/H and instrumentation intent |
| SR-MTH-04 | §2 (`releases/REL<n>-requirements.md`), §2.1, §2.2 (LNT-03, LNT-05, LNT-10, LNT-12, LNT-16), §5.6, §6 | `references/requirements-template.md`, `references/finalize-rubric.md`, and the six-step orchestration in `SKILL.md`; `fixtures/requirements-conformance` covers every type/process step, sentence form, change rule, failure guardrail, and completion check |
| SR-MTH-05 | §2 (`releases/REL<n>-requirements.md`), §2.1, §5.6 | `references/use-case-template.md` and `SKILL.md` section **UC elaboration**; `fixtures/use-case-completeness` checks actors, guarantees, main/extension/failure paths, rules, qualities, open questions, and acceptance examples |
| SR-MTH-06 | §2.1, §3.1, §4.2 (condition 7), §5.6 | `SKILL.md` section **Domain-gap routing**; `fixtures/domain-gap-routing` checks the pinned `domain-modeling` call/manual fallback, canonical artifact update, and prohibition on duplicate domain artifacts |
| SR-MTH-07 | §2 (`quality-scenarios.md`), §2.1, §2.2 (LNT-11), §3.1, §5.6 | `references/qas-template.md` plus `references/qas-gate.md`; `fixtures/qas-complete-measurable-feasible` checks six fields, consequence, trade-off, operational quality, ranking, verification, and local fallback |
| SR-MTH-08 | §2.1, §2.2 (LNT-09, LNT-10, LNT-12), §§5.5–5.7 | `references/requirements-template.md` sections **Observation requirements** and **Transition requirements**; `fixtures/instrumentation-and-retirement` proves criteria are observable and retired scope creates migration/coexistence/decommissioning work |
| SR-MTH-09 | §2 (vision and architecture-lens inputs), §2.1, §4, §5.6 | `SKILL.md` section **Vision references and upstream conflicts**; `fixtures/vision-conflict-routing` preserves actors/principles/boundaries/signals/seeds and routes conflict upstream without reinvention |
| SR-MTH-10 | §2.1, §2.2 (LNT-03, LNT-16), §§5.4–5.6 | `SKILL.md` section **Upstream discovery trace** plus `REQ#`/`QAS#` rationale fields; `fixtures/broken-upstream-trace` fails unresolved evidence, opportunity, assumption, experiment, or scope rationale |
| SR-MTH-11 | §2.1, §5.6 | `SKILL.md` section **Method terminology contract**; `fixtures/terminology-audit` checks canonical requirements/use-case/QAS terms and separates method glossary from product domain language |
| SR-MTH-12 | §2.1, §5.6 | `SKILL.md` section **Proportionate elicitation, modeling, and validation techniques**; `fixtures/specification-technique-selection` records why each technique is used and rejects ceremony-only selection |
| SR-M01 | §5.6 | Human-gate step: `DEC#` owner recording per the one-pager's decision-authority record (§5.3); group-only owner refused; handover lists unresolved decisions with owners (RTS-07) |
| SR-M02 | §5.6 | QAS gate rubric: Feasible dimension requires a recorded specialist verdict or an escalated blocking-uncertainty `OPEN:` marker (RTS-08) |
| SR-M03 | §5.6 | Builder-protocol proposal flagging + critic unmarked-invention check (LNT-05) |
| SR-M04 | §5.6 | Failed-gate backtracking routes carrying owner and escalation path; invalidated-upstream refusal with perseverance `DEC#` (RTS-10) |
