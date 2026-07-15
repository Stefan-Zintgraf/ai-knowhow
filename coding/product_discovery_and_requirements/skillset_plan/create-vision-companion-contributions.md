# `create-vision-companion` — contribution and coverage assurance

**Status:** Authoring contract for the planned adjustment  
**Skill:** `create-vision-companion`  
**Purpose:** Ensure that the adjusted companion derives a complete, mechanically checked bridge from the frozen foundation vision into the proprietary traceability spine, while incorporating every relevant external mechanism identified in [`github_skillsets.md`](./github_skillsets.md).

## 1. Scope and governing rule

The companion remains a derived-only bundle.

It may restructure, index, cross-reference, classify, and flag readings of the frozen vision. It must not:

- edit the foundation vision;
- invent evidence;
- create discovery commitments;
- assign loop IDs;
- place loop artifacts inside the vision bundle;
- adopt a third-party artifact taxonomy.

Every contribution below must end in an explicit disposition: **adopt**, **adapt**, **reference**, **defer**, or **reject**. Authoring is incomplete while any contribution remains merely “under consideration.”

## 2. External-contribution ledger

| ID | Source | Exact contribution considered | Mode | Proposed incorporation | Disposition | License / provenance constraint | Required verification evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VC-E01 | `shinpr/claude-code-discover` | Product context stored as durable repository artifacts with an auto-maintained index | pattern | Add `discovery-seeds.md` as an explicit, derived index of companion signals useful to discovery. Link it from `README.md` and include it in bundle completeness checks | **adapt** | MIT; use the indexing discipline, not Shinpr’s artifact taxonomy or wording | Bundle fixture contains `discovery-seeds.md`, README load-order guidance, valid internal links, and no Shinpr-style PRD/hypothesis directories |
| VC-E02 | `shinpr/claude-code-discover` | Context-separated verifier that does not see the builder’s expectations | pattern | Preserve and strengthen fresh-context builder/critic separation. Critic briefs contain the frozen vision, draft artifact, template, and rubric—but not builder reasoning | **adopt** | MIT; mechanism only | Orchestrator contract and tests prove separate contexts and prohibited builder-reasoning leakage |
| VC-E03 | `shinpr/claude-code-discover` | Hypothesis format with success/failure criteria, confidence by risk, and time budget | reference | `discovery-seeds.md` may point to candidate assumptions requiring experiment design, but must not create `EXP#` cards or copy the hypothesis schema | **defer** to `discover-product` | MIT | Seed fixture contains source-cited candidate assumptions only; no experiment method, time budget, criteria, or `EXP#` ID appears |
| VC-E04 | `RafaelGorski/Problem-Based-SRS` | Deterministic validation of a complete trace chain | pattern | Extend Phase 9 mechanical gates to validate the companion’s own graph: every source ID covered, every derived ID unique, references resolvable, coverage gaps explicit, reserved loop namespaces unused | **adapt** | MIT; keep the proprietary `S/V/UC/BV/INV/CAP` spine rather than CP/CN/FR | Automated gate fails fixtures with missing IDs, duplicate IDs, broken references, orphaned capabilities, or reserved-namespace collisions |
| VC-E05 | `ForceInjection/domain-driven-design-skills` | Explicit backtracking triggers with named prior phases | pattern | Add a companion re-entry matrix: each gate/critic defect routes to the phase that owns the artifact; cross-phase defects reopen the minimal closure and then rerun global gates | **adapt** | WIP; verify current license before copying. Mechanism only | Every mechanical and critic finding category maps to an owning phase; tests show no unspecified “fix later” route |
| VC-E06 | `ForceInjection/domain-driven-design-skills` | Blind-run validation against a canonical sample with scoring | pattern | Add end-to-end golden fixtures and mutation tests for fresh build, upgrade, vision diff, and failure recovery. Use objective pass/fail assertions rather than importing the source scoring scheme | **adapt** | WIP; do not copy its sample or rubric without license confirmation | Test suite and fixture manifest demonstrate reproducible whole-skill validation |
| VC-E07 | `huntsyea/product-skills` | Progressive-disclosure structure: orchestration plus focused references/workflows | pattern | Preserve the current split among `SKILL.md`, strategies, templates, rubrics, rerun guidance, and debug guidance. Put new output shape and checks in their owning sub-files instead of expanding the orchestrator indiscriminately | **adopt** as an already-satisfied pattern | MIT; no external runtime dependency | File-responsibility map identifies the owner of each new rule; cold-path instructions do not load rerun/debug material unnecessarily |
| VC-E08 | `phuryn/pm-skills` | Command-chaining UX | pattern | On successful finalize, name the appropriate next lifecycle stage—normally `discover-product` for greenfield—and point to `discovery-seeds.md` as its starting input | **adopt** | MIT; no runtime dependency | Final-response fixture includes bundle path, open-decision state, discovery-seed path, and next skill |
| VC-E09 | `jacksoncalling/argo-continuous-discovery` | Durable artifacts, explicit human gates, and routing rather than silent reconciliation | pattern | Preserve durable status/review files and the Phase 11 human gate. Coverage gaps become routed discovery seeds or judgment rows; they are never silently repaired by editing the vision | **adopt** as a corroborating pattern | License must be verified before copying; no copied material required | Fixture shows an unrealized promise and low-confidence reading surviving into visible review/seed artifacts |
| VC-E10 | `DavidROliverBA/Daves-Claude-Code-Skills` | Parallel independent reviews for completeness, measurability, and feasibility | pattern + reference | Retain independent multi-agent review as a structural quality pattern. Do not import NFR content; the companion’s critics use companion-specific rubrics | **adopt** as corroboration of the existing critic architecture | License not established in [`github_skillsets.md`](./github_skillsets.md); mechanism only | Review architecture is documented; no Dave-specific templates or Obsidian schema appear |
| VC-E11 | `deanpeters/Product-Manager-Skills` | Press-release layer as a way to preserve the product promise | reference | Preserve `V#` promises and their realization coverage in `vision-index.md`; do not copy or call the external skill | **reference** only; upstream input belongs to `brainstorm-vision` | CC BY-NC-SA 4.0; no distillation | `vision-index.md` retains every `V#` and flags unrealized promises; no external content is included |
| VC-E12 | Cross-cutting finding in [`github_skillsets.md`](./github_skillsets.md) | Third-party pipelines impose competing taxonomies | pattern | Keep one proprietary bundle and ID spine. External mechanisms may improve validation but may not introduce PRD, CP/CN/FR, or third-party workspace structures | **adopt** | N/A | Schema inventory contains only the planned proprietary artifacts and IDs |
| VC-E13 | Cross-cutting finding in [`github_skillsets.md`](./github_skillsets.md) | Runtime dependencies are fragile; vendored content and calls require provenance/version control | pattern | The companion has no runtime third-party calls or live fetches. Pattern sources are recorded with repository, license, and retrieval date | **adopt** | Recheck provenance before skill release | Dependency inventory and source ledger pass review |
| VC-E14 | Cross-cutting finding in [`github_skillsets.md`](./github_skillsets.md) | The whole skillset needs end-to-end validation, not only prose completion checks | pattern | Treat the authoring gate and fixture matrix below as release-blocking | **adopt** | Proprietary test design | CI or repeatable local validation produces pass/fail evidence for every gate |

## 3. Planned bundle adjustments

The following adjustments are mandatory and must be reflected consistently across orchestration, templates, strategies, rubrics, status tracking, rerun logic, and tests.

### 3.1 `discovery-seeds.md`

Add a derived-only file that surfaces:

- unrealized `V#` promises;
- unpromised `UC#` entries;
- unpromised `CAP#` entries;
- coverage gaps;
- unresolved or low-confidence `decisions.md` readings relevant to value, usability, feasibility, viability, actors, boundaries, or outcomes;
- explicit critical-assumption and outcomes/signals stubs present in the foundation vision.

Every seed must:

- cite at least one stable source or derived ID;
- identify why it matters;
- state a candidate downstream type, such as `candidate opportunity`, `candidate assumption`, `coverage question`, or `evidence question`;
- remain explicitly unconfirmed;
- carry no loop ID;
- contain no invented evidence;
- avoid prescribing a solution.

The file is input to `discover-product`; it is not itself an opportunity map, assumption map, evidence log, or experiment set.

### 3.2 Reserved ID families

Phase 0 must reserve:

`ASM`, `EV`, `OPP`, `SOL`, `EXP`, `REL`, `REQ`, `QAS`, and `DEC`.

The companion must reject:

- accidental use of a reserved family for companion-derived content;
- duplicate IDs within a family;
- malformed IDs;
- collisions caused by reruns or migrations.

`DEC` is reserved for the loop’s decision log. The companion’s existing local judgment IDs must therefore be clearly scoped as bundle-review IDs or renamed if ambiguity remains; the plan must make this distinction mechanical rather than relying on context.

### 3.3 `glossary.md` → `domain-glossary.md`

Rename the bundle artifact and update every reference to it in:

- `SKILL.md`;
- strategies;
- templates;
- rubrics;
- phase tables;
- `README.md`;
- actor, capability, context, UC, and vision artifacts;
- critic instructions;
- status and rerun guidance;
- hash/fingerprint inputs where applicable;
- upgrade and migration logic;
- tests and fixtures.

A current-method bundle must contain `domain-glossary.md` and must not contain the old artifact as a second canonical glossary.

For an existing finalized bundle, the upgrade path must:

1. detect the old filename;
2. reopen only after user confirmation;
3. migrate the file and all internal references;
4. preserve confirmed decisions where their meaning is unchanged;
5. rerun global mechanical and whole-bundle checks;
6. finalize only after the human review gate is satisfied.

### 3.4 Derived-only boundary

No planned adjustment may place `assumptions.md`, `evidence-log.md`, `opportunities.md`, `solutions.md`, experiments, release definitions, requirements, quality scenarios, or loop decision logs inside `<slug>-vision-ai-spec/`.

## 4. Method-document coverage ledger

| ID | Method source | Required coverage | Proposed incorporation | Verification evidence |
| --- | --- | --- | --- | --- |
| VC-M01 | [`product_vision.md`](../product_vision.md) — recommended structure | Preserve context, actors, desired change, value/differentiation, principles, scope boundaries, outcomes/signals, and critical assumptions without inventing missing content | Map present content into the existing companion concerns; route absent or open sections into visible coverage signals and `discovery-seeds.md` | Fixtures cover populated, absent, and explicitly open sections |
| VC-M02 | [`product_vision.md`](../product_vision.md) — completion checks | Companion must expose, not conceal, failures in actor coverage, evidence/assumption distinction, principles, exclusions, or observable outcomes | Add coverage checks and seed/judgment routing; never “complete” the frozen vision on its behalf | Whole-bundle critic detects each deliberately injected vision gap |
| VC-M03 | [`overview.md`](../overview.md) — lifecycle and readiness | Companion is the bridge from slow-changing vision into the faster discovery loop and later design readiness | README load-order and final handoff explain which companion artifacts seed discovery and which support later requirements/design | Handoff fixture names the downstream consumers without claiming readiness by companion generation alone |
| VC-M04 | [`lifecycle_tailoring.md`](../lifecycle_tailoring.md) | Companion normally runs only when a finalized foundation vision is in use; skipped stages must remain explicit | Require a finalized vision and respect a lifecycle one-pager if present. Do not manufacture a companion for a topic whose tailored lifecycle deliberately reuses another anchor | Fixtures cover greenfield, existing vision, and deliberately skipped vision stages |
| VC-M05 | [`product_discovery.md`](../product_discovery.md) | Opportunities remain separate from solutions; assumptions, evidence, alternatives, and experiment criteria are discovery commitments | `discovery-seeds.md` exposes questions and candidates only. It must not promote them into `OPP#`, `ASM#`, `EV#`, `SOL#`, or `EXP#` artifacts | Schema lint and adversarial fixture verify no premature commitments |
| VC-M06 | [`domain_discovery.md`](../domain_discovery.md) | Glossary, rules, invariants, capabilities, and candidate contexts are learning artifacts, not automatically validated architecture | Name the artifact `domain-glossary.md`; label derived context boundaries and domain readings as hypotheses where appropriate; route ambiguous readings to `decisions.md` | Critic fixture catches an invented term, an unsupported invariant, and a context presented as settled architecture |
| VC-M07 | [`quality_attributes.md`](../quality_attributes.md) | Architecture-significant qualities begin early, must remain grounded in consequences, and later become measurable scenarios | Cite and route the sibling architecture lens; preserve its source UCs and constraints. Do not invent `QAS#` scenarios inside the companion | Fixture distinguishes a vision-derived invariant/seed from a later quality scenario |
| VC-M08 | [`glossary.md`](../glossary.md) | Keep method vocabulary distinct from the product’s ubiquitous language | Rename the bundle artifact; use method terms consistently in orchestration and seed types; never merge the method glossary into the product glossary | Naming and terminology lint; no artifact collision remains |
| VC-M09 | [`validation_and_feedback.md`](../validation_and_feedback.md) | Outcome and guardrail gaps must remain observable because later validation depends on them | Surface missing or weak outcome/guardrail definitions as discovery seeds or coverage findings | Fixture with a usage-only “success” statement produces a visible outcome-quality seed |
| VC-M10 | [`resources.md`](../resources.md) | Adopt artifacts and techniques only when they reduce uncertainty or improve a consequential decision | Every companion file and new seed category states its consumer and decision purpose; no file exists merely for completeness | Bundle README and template review show a consumer and purpose for each file |

## 5. Authoring coverage gate

The adjusted `create-vision-companion` skill is complete only when all conditions below pass.

### 5.1 Ledger completeness

- Every `VC-E#` and `VC-M#` row has a final disposition.
- Every adopted/adapted item names its implementation location.
- Every deferral names its receiving skill.
- Every exclusion records a reason.
- Every source has repository, license status, and retrieval date.
- No contribution remains “pending audit” at skill release; a failed license/depth audit converts the item to reference, defer, or reject.

### 5.2 Bundle-schema completeness

- `domain-glossary.md` replaces `glossary.md` everywhere.
- `discovery-seeds.md` is present and linked from `README.md`.
- All existing companion files remain owned by exactly one concern.
- Templates, phase tables, rubrics, status tracking, rerun guidance, and tests agree on the exact file set.
- The skill fingerprint includes every output-shaping file changed by this adjustment.
- Current bundles contain no stale internal link to `glossary.md`.

### 5.3 Traceability and namespace gate

Mechanical validation proves:

- every `S#`, `V#`, `UC#`, and `BV#` in the frozen vision is accounted for;
- every `INV#` and `CAP#` is unique and cited;
- every internal link resolves;
- every UC has its required actor and primary capability;
- unrealized promises, unpromised UCs, and unpromised capabilities remain explicitly visible;
- every discovery seed cites at least one valid ID;
- reserved loop ID families are absent from companion-derived artifacts;
- no duplicate or malformed ID survives;
- no source ID is silently renumbered during rerun.

### 5.4 Derived-only gate

The whole-bundle critic confirms:

- no evidence was invented;
- no candidate seed was promoted into a commitment;
- no solution was smuggled in as an opportunity;
- no loop artifact exists inside the bundle;
- no third-party taxonomy was introduced;
- every derived interpretation either follows mechanically or appears in the human review surface;
- the foundation vision remains byte-identical for the duration of the run.

### 5.5 Builder/critic independence gate

- Builders and critics run in separate fresh contexts.
- Critics receive the frozen source, current artifact, relevant template, and rubric.
- Critics do not receive hidden builder reasoning or expectations.
- Clear defects may be fixed mechanically.
- Residual judgment is routed to `decisions.md`.
- The whole-bundle critic reruns after human adjudication before finalization.

### 5.6 Backtracking gate

A documented matrix routes at least:

| Finding | Reopen |
| --- | --- |
| Source coverage or ID defect | Owning derivation phase |
| Unsupported invariant | Invariants phase and dependent closure |
| Glossary merge/split defect | Domain-glossary phase and dependent actor/capability/context artifacts |
| Actor defect | Actors phase and affected UC rows |
| Capability clustering defect | Capability phase and dependent context/vision/UC indexes |
| Promise/UC coverage defect | Vision-index phase |
| Parking-lot routing defect | Deferred-inputs phase |
| Discovery-seed classification or citation defect | Discovery-seeds phase |
| Cross-phase inconsistency | Minimal owning closure, followed by global Phase 9 and whole-bundle critic |
| Vision drift affecting many or renumbered IDs | User-confirmed full rebuild |
| Skill-method drift | User-confirmed upgrade review or rebuild |

No failure route may end in an unspecified “review later.”

### 5.7 End-to-end validation matrix

At minimum, repeatable fixtures cover:

1. a clean fresh vision with no parking lot;
2. a vision with `BV#` inputs;
3. unrealized `V#`, unpromised `UC#`, and unpromised `CAP#`;
4. ambiguous terminology and a low-confidence domain reading;
5. an explicit critical-assumptions stub;
6. missing or usage-only outcomes/signals;
7. an architecture-lens constraint;
8. a duplicate derived ID;
9. a reserved loop-ID collision;
10. a broken internal link;
11. a paused build resumed mid-phase;
12. a finalized old bundle upgraded from `glossary.md`;
13. a small vision diff with scoped derivation and global verification;
14. a large or renumbered vision diff routed to rebuild;
15. a changed skill fingerprint with unchanged vision;
16. a critic residual requiring Phase 11 human confirmation;
17. a discovery seed that attempts to invent evidence or prescribe a solution and is rejected.

### 5.8 Handoff gate

On successful finalization:

- `_status.md` says `finalized`;
- all judgment rows are confirmed;
- the whole-bundle critic is reconciled;
- the response names the bundle path;
- the response names `discovery-seeds.md`;
- the response names the appropriate next lifecycle skill;
- no claim is made that discovery, definition, or requirements are complete.

### 5.9 Drift gate

Changes to consumed method docs or to any output-shaping skill file trigger a ledger and fixture review. A hash change alone identifies drift; it does not authorize automatic rebuilding or overwriting.

## 6. Explicit exclusions and deferrals

| Source | Exclusion / deferral |
| --- | --- |
| Dean Peters question sequences and press-release content | Upstream `brainstorm-vision` input only; CC BY-NC-SA material must not be distilled |
| `phuryn/pm-skills` marketplace | Do not install wholesale; only the handoff UX pattern is used |
| Huntsyea continuous-discovery/JTBD content | `discover-product`; the companion supplies seeds but performs no discovery interview |
| Assimovt interview, problem-validation, experiment, scope, and metric content | Route to discovery, definition, or validation skills |
| Argo interview-quality rubric and evidence-confidence cap | `discover-product`’s evidence model; the companion has no evidence ledger |
| Shinpr PRD, hypothesis, persona, blueprint, prototype, and implementation artifacts | Competing pipeline and taxonomy; only index discipline and context-separated verification are used |
| Problem-Based-SRS CP/CN/FR IDs and `.spec/` JSON | Rejected because they would create a second traceability spine; only the deterministic validation mechanism is adapted |
| `45ck/software-architecture-skills` | QAS authoring belongs to `specify-requirements`; the companion only preserves architecture-lens inputs |
| Dave’s NFR templates and Obsidian schemas | Out of scope and workspace-incompatible; only independent-review structure is relevant |
| `ddd-crew/ddd-starter-modelling-process` | Reference for human domain modeling and the future design skillset |
| ForceInjection tactical DDD artifacts | Future design skillset; only backtracking and blind-run-validation mechanisms are adapted |
| `lagz0ne/design-skill` | Starts after requirements; future design skillset |
| `ai-analyst-lab/north-star` | Called by definition/validation, not by companion derivation |
| `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` | Validation-analysis planning only; no stated license, so no distillation |

These exclusions preserve the companion’s narrow role: a trustworthy, derived, mechanically checked bridge from the vision into the proprietary lifecycle spine.
