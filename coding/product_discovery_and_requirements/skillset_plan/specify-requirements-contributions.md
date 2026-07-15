# Authoring Assurance: `specify-requirements`

**Status:** Required authoring contract  
**Applies to:** `specify-requirements` skill implementation and every material revision  
**Primary outputs:** `releases/REL<n>-requirements.md`, `quality-scenarios.md`

**Planning sources:** [skillset plan](./prod_discovery_requirements_skillset_plan.md) · [GitHub skillset fit analysis](./github_skillsets.md)  
**Primary method sources:** [Requirements engineering](../requirements_engineering.md) · [Use cases and story mapping](../use_cases_and_story_mapping.md) · [Quality attributes](../quality_attributes.md)

## 1. Purpose and scope

This file ensures that requirements rigor is preserved while external techniques are used only where they strengthen the proprietary traceability spine.

The skill must transform a committed release slice into reviewable use cases, requirements, quality-attribute scenarios, constraints, and verification intent. It may draft content autonomously, but it may not silently invent stakeholder judgment, domain rules, failure behavior, or measurable targets.

The skill is authoring-complete only when its builder/reviewer separation, deterministic linter, QAS/NFR gates, human confirmation points, and downstream handover have all been verified. Allowed contribution dispositions are `adopt`, `adapt`, `reject`, or `defer`; no row may remain `pending`.

## 2. External-contribution ledger

Before authoring, replace every source pointer with the exact repository URL, commit SHA or release, files inspected, retrieval date, and verified license.

| ID | Source | Exact contribution to assess | Mode | Required incorporation | Disposition | License and provenance requirement | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SR-EXT-01 | `shinpr/claude-code-discover` — `hypothesis-verifier` | Context-separated verification in which the critic does not inherit the author’s expectations | pattern | Run the requirements critic in a separate context. Give it authoritative source artifacts, candidate outputs, schemas, and gates, but not builder reasoning or expected conclusions | adopt | MIT; record exact verifier/agent files and commit | Seeded plausible errors are detected by the critic; reviewer result is stable when builder rationale is removed |
| SR-EXT-02 | `shinpr/claude-code-discover` — repository product context and index discipline | Durable in-repo context, explicit rejected alternatives, maintained indexes, implementation handoff | pattern | Keep artifacts in the proprietary workspace; preserve explicit unresolved/rejected choices and ensure indexes/handover remain current | adapt | MIT; exact files and commit required | Stale-index and missing-rejected-alternative fixtures fail validation |
| SR-EXT-03 | `RafaelGorski/Problem-Based-SRS` — `validate` action | Mechanical validation of a complete trace chain | pattern | Implement a workspace linter for the proprietary chain `EV/OPP -> CAP -> UC/REQ/QAS`, including rationale and verification links; do not introduce `.spec` JSON or `CP/CN/FR` IDs | adopt/adapt | MIT; record exact validation action/reference files and commit | Positive, broken-link, orphan, duplicate-ID, and missing-rationale fixtures |
| SR-EXT-04 | `RafaelGorski/Problem-Based-SRS` — problem/need/requirement discipline | Preserve the reason behind each requirement and distinguish externally mandatory needs from expectations and hopes | pattern | Consume the O/E/H classification from `REL`; require each `REQ/QAS` to trace to a need, risk, constraint, or obligation and preserve the consequence/rationale | adapt | MIT; exact source audit required | Orphan requirement and unsupported “shall” fixtures fail |
| SR-EXT-05 | `45ck/software-architecture-skills` — `quality-attribute-scenario-writer` | Potential specialist support for six-part QAS construction | conditional call | Audit actual skill depth first. Call only if it materially exceeds the local QAS reference, is version-pinned, and returns content for validation through the proprietary gate | defer until audit, then adopt or reject | Reported MIT; verify exact skill, repository license, commit, examples, and generated-pack depth | Comparative fixture scores local-only and called output against the same QAS gate |
| SR-EXT-06 | `DavidROliverBA/Daves-Claude-Code-Skills` — `nfr-capture` | ISO 25010-oriented NFR capture with measurable criteria | pattern | Use relevant completeness prompts without importing Obsidian schemas, tags, or vault layout | adapt | Verify repository/file license before using any content; pattern-level use only until confirmed | QAS coverage fixture includes relevant operational and stakeholder consequences without checklist inflation |
| SR-EXT-07 | `DavidROliverBA/Daves-Claude-Code-Skills` — `nfr-review` | Review dimensions: complete, measurable, feasible; independent review lanes | pattern | Make completeness, measurability, and feasibility explicit QAS gate dimensions. Separation is mandatory; multi-agent fan-out is optional, not required | adopt/adapt | Verify exact license and files; no vault-coupled material | Each QAS receives three recorded gate results; seeded defects fail the matching dimension |
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
