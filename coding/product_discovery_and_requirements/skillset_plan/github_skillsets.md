# Existing GitHub Skillsets — Fit Analysis

**Status:** Revised draft — decision input for the [skillset plan](./prod_discovery_requirements_skillset_plan.md); the actionable consequences live in the [revision contract](./skillset_plan_update_plan.md)
**Question answered:** Can the agent rule sets referenced in the stage docs' *Further material* sections replace, shorten, or improve the proprietary skillset planned for the discovery–definition–requirements loop — and how should we continue?

All 14 referenced repositories were inspected (README + structure) as of 2026-07-15.

## 1. Fit criteria

A candidate is measured against what the [plan](./prod_discovery_requirements_skillset_plan.md) actually requires, not against "is it a good PM tool":

| # | Criterion | Why it is load-bearing |
| --- | --- | --- |
| C1 | **Traceability spine** — artifacts cite upward into the companion's IDs (`S/V/UC/BV/INV/CAP`) and extend them (`ASM/EV/OPP/EXP/REL/REQ/QAS/DEC`) | Design principle 3; the loop's whole value is that every requirement answers "why" mechanically |
| C2 | **Repo-artifact workspace** — durable markdown artifacts in the product repo (`docs/product/<topic>/`), not chat output | Design principle 2; artifacts must survive the session and feed the next skill |
| C3 | **Two skill modes** — interview where the human supplies evidence/judgment; AFK derive (builder/critic + `decisions.md`) where content is restructured | Design principle 1 |
| C4 | **Method-doc fidelity** — consumes *this collection's* stage docs (templates → output shapes, completion checks → gates, failure modes → guardrails) | Design principle 6 |
| C5 | **Tailored ceremony** — degrades to the minimum useful package; skipped stages recorded, not silent | Design principle 5 |
| C6 | **License & maintenance** — usable in this context, alive, not a link-rot risk | Practical |

No external pack satisfies C1 — that is the headline finding. C1 is also the criterion that cannot be bolted on from outside: it requires knowing the companion bundle's ID scheme.

## 2. Per-skillset analysis

Grouped by the lifecycle stage whose doc references them. Verdict vocabulary: **replace** (could substitute a planned skill), **call** (reuse as a callable step, like `prototype`), **distill** (pull specific content into proprietary skill sub-files, with source pointer), **pattern** (adopt an idea into the plan), **reference** (background reading only), **out-of-scope** (belongs to a later skillset).

### 2.1 Product vision

#### `deanpeters/Product-Manager-Skills` — 56 skills, 3 tiers (workflow / interactive / component)

- **What it is:** The most mature PM pack found: pedagogic skills with named failure modes, an "Adaptive Decision Ladder" interview pattern, active releases (v0.82, 2026-07). `press-release` (Amazon Working Backwards), `discovery-process`, `opportunity-solution-tree`, `user-story-mapping`, `prd-development`.
- **Fit:** The interactive tier is the same interview mode as `brainstorm-vision`/`grill-me` (C3 ✓). But output is coaching + documents for a human PM, with no ID scheme (C1 ✗), no repo-artifact convention (C2 ✗), and its frameworks (Working Backwards, MITRE ITK) overlap but do not equal our method docs (C4 ✗).
- **Benefit over proprietary:** battle-tested question sequences and failure-mode catalogs we would otherwise have to invent; the three-tier taxonomy is a ready answer to plan open question 3 (skill granularity).
- **Disadvantage:** **CC BY-NC-SA 4.0 — non-commercial, share-alike.** Distilling its content into our skills would contaminate them with the share-alike clause; commercial use is off the table. Interaction-heavy skills also don't compose into an AFK pipeline.
- **Verdict:** **pattern + reference.** Take the tier taxonomy and the "press-release as vision stress test" idea (optional `brainstorm-vision` micro-phase). Do **not** copy content (license).

#### `phuryn/pm-skills` — 68 skills, 42 commands, 9 plugins (MIT)

- **What it is:** The largest marketplace; chained commands (`/discover` = ideate → assumptions → prioritize → experiments) that mirror a PM workflow; CI-tested; actively maintained.
- **Fit:** `/discover` covers the same ground as `discover-product`'s middle phases but stops at experiment design — no `EV` ledger with source-strength, no `ASM` ranking persisted, no decision log (C1/C2 ✗). Breadth (pricing, GTM, resumes, NDAs) is noise for this loop; installing all 9 plugins floods the trigger namespace and risks shadowing proprietary skill triggers.
- **Benefit:** the *command-chaining UX* — every command ends by suggesting the next one — is exactly how loop skills should hand over per the `lifecycle-onepager.md`. `north-star-metric` and metric-tree skills are solid seeds for `validate-release`.
- **Disadvantage:** PRD-shaped and feature-shaped; no requirements engineering at all; wholesale adoption buys 80% irrelevant surface.
- **Verdict:** **pattern (hand-over UX) + cherry-pick call** (`north-star-metric` as an alternative to `ai-analyst-lab/north-star`, see §2.6). Not a marketplace to install wholesale.

### 2.2 Product discovery

#### `rohanpatriot/product-skills` → **moved to `huntsyea/product-skills`** — 4 skills (MIT)

- **What it is:** `continuous-discovery` (Torres), `jobs-to-be-done` (Moesta), `shape-up` (Singer), `story-mapping` (Patton). Each skill = SKILL.md + `references/` (distilled source text: anti-patterns, principles, techniques) + `workflows/` (step procedures). Highest quality-per-skill of everything reviewed; the structure *is* the progressive-disclosure layout our plan intends.
- **Fit:** `continuous-discovery`'s workflows (set-outcomes, map-opportunities, ideate, test-assumptions) map 1:1 onto `discover-product`'s phases; `story-mapping`/`shape-up` map onto `define-release` (journey shaping, appetite/commitment). No IDs, no evidence ledger, no repo workspace (C1/C2 ✗) — it teaches the method superbly but records nothing durably.
- **Benefit:** its `references/` files (28 Torres anti-patterns by phase, JTBD forces framework, Patton slicing principles) are precisely the "failure modes → guardrails" material design principle 6 demands — already distilled, MIT-licensed.
- **Disadvantage:** the repo transfer (`rohanpatriot` → `huntsyea`) shows the link-rot risk of runtime dependencies on third-party repos (C6 ⚠); the stage-doc references should be updated.
- **Verdict:** **distill (first choice) or call.** Vendor the relevant `references/` files into `discover-product` / `define-release` sub-files with source pointers. Calling the installed skills live is workable but couples the loop to an external repo's trigger phrasing. (The moved URL has been corrected in the three referencing stage docs.)

#### `jacksoncalling/argo-continuous-discovery` — folder-based discovery operator

- **What it is:** A workspace (not a skill): five phase folders each with own CONTEXT.md, accumulating artifacts (interview snapshots, experiment cards, an interactive `tree.html`). Interview-quality assessment (story vs. opinion), opportunity confidence *capped by interview quality*, explicit human gate before solutioning, routing decisions (add/merge/escalate/park).
- **Fit:** Closest in *spirit* to the plan of anything reviewed: durable artifacts (C2 ✓), human gates (C3 ✓), coaching guardrails (C4-adjacent). But it is a competing workspace layout, not a component — adopting it means adopting its folder scheme and `tree.html` instead of the companion-ID'd markdown artifacts (C1 ✗). Single-outcome per instance; demo-grade maturity (community-challenge project, ships with demo data) (C6 ⚠).
- **Benefit over proprietary:** three mechanisms worth stealing outright: (1) the interview-quality rubric (Rich/Mixed/Thin) as the `EV#` strength model, (2) confidence capped by evidence quality — "three weak interviews don't equal one good one", (3) the routing decision table for extracted opportunities.
- **Verdict:** **pattern.** Fold those three mechanisms into `discover-product`; do not adopt the operator.

#### `assimovt/productskills` — 16 compact skills, 50–150 lines each (MIT)

- **What it is:** Opinionated single-purpose skills: `user-interview` (Mom Test), `problem-validation` (frequency × intensity × WTP), `opportunity-mapping`, `scope-cutting`, `bet-sizing`, `prd-writing` (evidence-first), `experiment-design`, `metrics-framework`.
- **Fit:** The right *ceremony level* for the solo-developer floor (C5 ✓) — these are what the minimum useful package looks like as skills. Same structural gaps as the rest: no IDs, no cross-skill artifact chain (C1 ✗).
- **Benefit:** shortest path to good guardrails ("never accept hypothetical enthusiasm" is literally the Mom Test skill's core rule — the same guardrail `discover-product` §5.4 specifies); MIT, trivially vendorable.
- **Disadvantage:** so compact that each skill assumes the human orchestrates; nothing connects an interview note to a scope decision.
- **Verdict:** **distill.** Primary guardrail/checklist donor for `discover-product` (evidence coaching), `define-release` (scope-cutting, bet-sizing).

### 2.3 Product definition

#### `shinpr/claude-code-discover` — plugin: 8 recipes + 5 context-separated agents (MIT)

- **What it is:** The only pack that shares the plan's *core thesis*: product context (hypotheses with success/failure criteria, validation results, PRDs with per-story confidence, rejected alternatives) lives **in the repo beside the code** so the coding agent sees it. Artifacts under `docs/product|discovery|prd/` with an auto-maintained `INDEX.md`; PRD user stories trace to hypothesis files; hands off to a sibling implementation-workflow plugin.
- **Fit:** C2 ✓ emphatically; C3 ✓ (its `hypothesis-verifier` runs in a separate context *without seeing the author's expectations* — a cleaner builder/critic separation than ours). But it is a **whole competing pipeline**: its own artifact taxonomy, PRD-shaped output, its own vision/persona/blueprint stages (blueprint + prototypes belong to our future *design* skillset), no vision-companion spine, no use cases, no QAS, no requirements engineering (C1/C4 ✗). Adopting it means adopting its lifecycle — that is option (a) below, with the quality loss the plan forbids.
- **Benefit over proprietary:** answers plan open question 4 directly — the AFK-safe part of `specify-requirements` is exactly what a context-separated critic that hasn't seen the builder's expectations can verify. Its hypothesis-file format (assumption statement, success/failure criteria, confidence per risk dimension, time budget) is a better `EXP#` card than our sketch. `INDEX.md` auto-maintenance validates the `discovery-seeds.md` idea.
- **Verdict:** **pattern (strongest single donor).** Steal: hypothesis-file format → `experiments/EXP<n>.md`; verifier context separation → `specify-requirements` review gate; INDEX discipline → companion `discovery-seeds.md`.

### 2.4 Requirements engineering

#### `RafaelGorski/Problem-Based-SRS` — one skill, 6-step methodology, peer-reviewed (MIT)

- **What it is:** The only serious RE agent skill in the ecosystem (the stage doc already notes RE is thinly covered). Traceability chain CP → CN → FR/NFR aligned with ISO/IEC/IEEE 29148; problem classification Obligation/Expectation/Hope; a `validate` action that mechanically checks the chain is complete; single-skill + `reference/<action>.md` architecture (same progressive-disclosure shape as ours).
- **Fit:** The traceability *discipline* is exactly C1's spirit — but rooted in its own ID families (CP/CN/FR) and `.spec/` JSON artifacts. Two trace spines in one repo would be worse than one; remapping its chain onto `EV/OPP → CAP → UC/REQ/QAS` means rewriting its core. It also drags its own upstream (business context, software glance/vision) that duplicates our vision + definition stages. Copilot canvas app is baggage.
- **Benefit over proprietary:** the `validate` command is an idea the plan *lacks*: a mechanical traceability check across the whole loop workspace. The Obligation/Expectation/Hope classing is a cleaner "every must needs a consequence" enforcement than prose.
- **Verdict:** **pattern.** Add a traceability-validation step (or micro-skill) to the plan; adopt problem classing into `define-release` prioritization. Keep our spine.

### 2.5 Use cases, quality attributes, domain discovery

#### `45ck/software-architecture-skills` — 14 architecture skills (MIT)

- **Fit:** `quality-attribute-scenario-writer` is the only piece relevant to this loop (the QAS format for [quality_attributes.md](../quality_attributes.md)); the other 13 belong to the future design skillset. The repo is one of ~30 near-identical, evidently semi-generated sibling packs from the same author (C6 ⚠ — depth unverified).
- **Verdict:** **call (conditional)** — audit `quality-attribute-scenario-writer`'s actual SKILL.md depth first; if thin, our own QAS sub-file distilled from [quality_attributes.md](../quality_attributes.md) is safer. Rest: out-of-scope (design skillset candidate list).

#### `DavidROliverBA/Daves-Claude-Code-Skills` — 42 skills, BA/architecture + Obsidian vault

- **Fit:** `nfr-capture` (ISO 25010, measurable acceptance criteria) and `nfr-review` (completeness/measurability/feasibility via 3 parallel agents) overlap `specify-requirements`' QAS work. Deeply coupled to an Obsidian-vault ecosystem (frontmatter schemas, tag taxonomies) we don't run (C2 mismatch).
- **Verdict:** **pattern.** The nfr-review dimensions (complete? measurable? feasible?) become `specify-requirements`' QAS gate checks. The multi-agent fan-out review pattern is already ours via `create-vision-companion`.

#### `ddd-crew/ddd-starter-modelling-process` — process documentation (CC BY 4.0)

- **What it is:** Not an agent skill at all — the canonical human 8-step DDD process with canvases (Bounded Context Canvas, Core Domain Charts, Aggregate Design Canvas).
- **Verdict:** **reference** for `domain-modeling` and the future design skillset. Nothing to install. The stage doc's "Agent rule sets" label slightly misfiles it.

#### `ForceInjection/domain-driven-design-skills` — 9 `ddd-*` skills, 5 phases (WIP)

- **What it is:** Surprisingly rigorous engineering: standardized SKILL contract (inputs, outputs, validation checklist, *backtracking triggers* — e.g. "invariant expression rate < 60% → return to `ddd-aggregates`"), blind-run validation against the canonical Cargo sample with scoring (85.8%). Docs primarily Chinese; explicitly WIP (C6 ⚠).
- **Fit:** Scope is domain modeling → tactical design → spec bridge; it overlaps `domain-modeling` and the design skillset, not this loop.
- **Verdict:** **pattern (for the whole skillset program):** its explicit backtracking-trigger matrix is the formalized version of our loop's "reopen" arrows — worth imitating when specifying re-entry conditions (`validate-release` → which artifact reopens). Otherwise out-of-scope here; revisit when planning the design skillset.

#### `lagz0ne/design-skill` — EventStorming → Mermaid design catalog

- **Fit:** Its 5 phases start where our loop *ends* (requirements → big picture → processes → data → integration). Phase 1 "Requirements" is a brief interactive Q&A, far below [requirements_engineering.md](../requirements_engineering.md)'s bar.
- **Verdict:** **out-of-scope** — candidate for the design skillset (§6 of the plan). Not a substitute for any loop skill.

### 2.6 Validation and feedback

#### `ai-analyst-lab/north-star` — North Star Metric coach with deterministic checks (MIT code)

- **What it is:** A real Claude Code skill with Python-backed deterministic checks: `audit` (7-question grading, refuses vanity metrics), `drivers`, `inputs` (input tree, checks each input is a driver, not the NSM renamed), `explain`, `triage`. Cited line-by-line to Amplitude's playbook. CI-tested.
- **Fit:** Best-engineered single-purpose skill reviewed. Doesn't touch our artifacts (C1/C2 n/a) — but it doesn't need to: metric hygiene is a self-contained judgment call inside `define-release` (success/guardrail criteria) and `validate-release` (outcome measures). Note: playbook-derived content remains © Amplitude (educational use).
- **Verdict:** **call — reuse as-is**, the same way the plan reuses `prototype`. Wire it in as the optional "audit the success metric" step of `define-release` and `validate-release`.

#### `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` — 10 analytics skills (book-derived)

- **Fit:** Overlaps `north-star` (NSM agent, KPI trees) with lower engineering maturity (manual install, no tests, no stated license — C6 ✗ for redistribution). `analysis-planner` (structure the investigation before touching data) is a nice idea for `validate-release`'s review prep.
- **Verdict:** **reference.** Prefer `ai-analyst-lab/north-star`; borrow the "plan the analysis before running it" step as a `validate-release` guardrail.

## 3. Cross-cutting findings

1. **Nobody has the spine.** No external pack writes artifacts that cite a vision-companion ID scheme, and none could — C1 is inherently proprietary. Everything downstream of that (definition citing evidence, requirements citing capabilities, validation reopening specific artifacts) is the plan's unique value and survives every comparison.
2. **The ecosystem divides into coaches and pipelines.** Coaches (deanpeters, huntsyea, assimovt) teach a human through an interview and leave no durable artifact. Pipelines (shinpr, Problem-Based-SRS, ForceInjection) produce repo artifacts but each imposes its own taxonomy that collides with ours and with each other. Mixing two pipelines is worse than owning one.
3. **The best material is reference content, not orchestration.** The distilled source-text `references/` files (huntsyea), compact guardrails (assimovt), and rubrics (argo) plug into design principle 6's distill-at-authoring-time mechanism perfectly — they shortcut *writing* the proprietary skills without replacing them.
4. **Requirements engineering remains the thin spot** — confirmed. One serious skill exists (Problem-Based-SRS) and it's spine-incompatible. `specify-requirements` has no buy option.
5. **Licenses matter and differ:** MIT (phuryn, huntsyea, assimovt, shinpr, Gorski, 45ck, lagz0ne, north-star code), CC BY 4.0 (ddd-crew), **CC BY-NC-SA (deanpeters — do not distill)**, unlicensed (florianbonnet14), © Amplitude content inside north-star.
6. **Runtime dependencies on third-party repos are fragile:** one of thirteen references already moved (`rohanpatriot` → `huntsyea`) within months. Anything we depend on should be vendored (content) or version-pinned (installed skills), never fetched live.

## 4. Options evaluated

| Option (from the decision request) | Assessment |
| --- | --- |
| **(a) Adjust lifecycle/workflow to fit an existing skillset** | Only `shinpr/claude-code-discover` offers a coherent enough lifecycle to adjust toward. Cost: lose the vision-companion spine, use cases, QAS, and RE rigor — a real quality loss, which the option explicitly excludes. **Rejected.** |
| **(d) Only use existing skills** | Fails C1 everywhere and C4 almost everywhere; two+ packs cannot be composed because their artifact taxonomies collide (finding 2). **Rejected.** |
| **(e) Enhance existing skills to fill the gaps** | Means maintaining forks of several third-party repos and pushing our ID scheme into codebases that don't want it; upstream drift makes every fork a liability; blocked outright for deanpeters (share-alike). **Rejected as primary strategy** (PR-ing small fixes upstream is still fine). |
| **(b) Keep proprietary skillsets, use existing ones as input/enhancement** | Matches finding 3. Low risk, keeps the spine, and the plan already works this way (`prototype`, `domain-modeling` reuse). **Adopted — as part of (c).** |
| **(c) Mix of proprietary and existing** | The proprietary skills own every artifact-producing loop stage; existing skills participate in two bounded roles: *callable specialist steps* and *distilled reference content*. **Recommended, see §5.** |

## 5. Recommendation

**Keep the proprietary skillset plan as the orchestrating spine (option c = b + selective reuse).** The loop stages that produce spine artifacts — `tailor-lifecycle`, `discover-product`, `define-release`, `specify-requirements`, `validate-release` — stay proprietary. External skills integrate in exactly three modes, each with one rule:

- **Call** (runtime dependency, version-pinned install): only for self-contained judgment steps that don't touch the artifact spine.
- **Distill** (vendored content in skill sub-files, with source pointer + date): for technique/guardrail/checklist material; MIT/CC-BY sources only.
- **Pattern** (idea adopted into the plan, no dependency): for mechanisms.

### 5.1 Integration map

| Proprietary skill | External input | Mode |
| --- | --- | --- |
| `brainstorm-vision` (adjust) | deanpeters `press-release` idea (Working Backwards as vision stress test) | pattern (optional finalize micro-phase) |
| `discover-product` | huntsyea `continuous-discovery` + `jobs-to-be-done` references | distill |
| `discover-product` | assimovt `user-interview`, `problem-validation`, `experiment-design` | distill (guardrails) |
| `discover-product` | argo: interview-quality rubric (Rich/Mixed/Thin), confidence capped by evidence quality, opportunity routing table | pattern |
| `discover-product` → `experiments/EXP<n>.md` | shinpr hypothesis-file format (success/failure criteria, confidence per risk, time budget) | pattern |
| `define-release` | huntsyea `story-mapping` + `shape-up` references; assimovt `scope-cutting`, `bet-sizing` | distill |
| `define-release` | Problem-Based-SRS Obligation/Expectation/Hope classing for "every must needs a consequence" | pattern |
| `define-release` / `validate-release` | `ai-analyst-lab/north-star` — audit success/outcome metrics | **call** |
| `specify-requirements` | shinpr `hypothesis-verifier` context separation → the AFK review gate (answers plan open question 4) | pattern |
| `specify-requirements` | Problem-Based-SRS `validate` → mechanical traceability check over the loop workspace | pattern (new step or micro-skill) |
| `specify-requirements` (QAS) | 45ck `quality-attribute-scenario-writer` (audit depth first); Dave's `nfr-review` check dimensions | call (conditional) / pattern |
| `validate-release` | florianbonnet14 "plan the analysis before running it" | pattern (guardrail) |
| all loop skills | phuryn command-chaining UX: every skill ends by naming the next stage per `lifecycle-onepager.md` | pattern |
| loop re-entry spec | ForceInjection backtracking-trigger matrix style for the reopen table | pattern |
| future design skillset | 45ck pack, lagz0ne `design-skill`, ForceInjection `ddd-*`, ddd-crew process | defer to that plan (§6 of skillset plan) |

### 5.2 Amendments to the skillset plan

1. **Add an external-dependency policy** (new design principle or §6 note): call = version-pinned; distill = vendored with source pointer + retrieval date; never runtime-fetch third-party repos. This also resolves open question 9 in the *distill* direction for external material.
2. **Extend §3 skills table** with two `existing — reuse as-is` rows: `north-star` (validation/definition metric audit) and, conditionally, `quality-attribute-scenario-writer`.
3. **Adopt the `EXP#` card format** from shinpr's hypothesis files (§2.3 above) in the §2 artifacts table.
4. **Add a traceability-check step** (Problem-Based-SRS `validate` pattern) to `specify-requirements`' finalize gate — or as a tiny standalone utility skill the whole loop can run.
5. **Record the license constraints** where skills distill external content (no deanpeters content; attribute CC-BY).

## 6. Actionable follow-up (moved)

The actionable consequences of this comparison — the ordered plan edits (including the three gap closures: solution alternatives, deterministic linter, regression validation), the contribution-coverage contract, and the acceptance gate — now live in the [revision contract](./skillset_plan_update_plan.md). Open that file when revising the skillset plan; this analysis remains the evidence base behind it, and the full gap narratives are preserved in its git history.

