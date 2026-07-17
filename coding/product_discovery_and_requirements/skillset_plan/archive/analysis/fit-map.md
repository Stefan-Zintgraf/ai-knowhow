# Fit-analysis map (Phase 0 digest)

**Source:** [github_skillsets.md](../github_skillsets.md) §2 (per-skillset analysis) and §5.1 (integration map), read 2026-07-16.
**Purpose:** Normalized checklist for the acceptance gate: every §5.1 recommendation must map to a contribution ID; every relevant §2 mechanism (M), benefit (B), and warning (W) must have a final disposition (`Adopt`/`Adapt`/`Call`/`Reject`/`Defer`). Rows marked type D are disposition notes from the fit analysis itself. §5.1 names no contribution IDs, so every row's ID is "to be matched in ledger".

Repo slugs used in keys: `deanpeters`, `phuryn`, `huntsyea` (ex-rohanpatriot), `argo` (jacksoncalling/argo-continuous-discovery), `assimovt`, `shinpr` (claude-code-discover), `gorski` (RafaelGorski/Problem-Based-SRS), `45ck` (software-architecture-skills), `daves` (DavidROliverBA), `dddcrew`, `forceinjection`, `lagz0ne`, `northstar` (ai-analyst-lab/north-star), `florianbonnet`.

## 1. §5.1 integration map — one row per recommendation

| Key | Source repo/skillset | Recommendation (condensed, near-verbatim) | Target skill(s) named | Contribution ID |
| --- | --- | --- | --- | --- |
| FIT-5.1-01 | deanpeters | `press-release` idea (Working Backwards as vision stress test) as optional finalize micro-phase — pattern | `brainstorm-vision` (adjust) | to be matched in ledger |
| FIT-5.1-02 | huntsyea | Distill `continuous-discovery` + `jobs-to-be-done` references | `discover-product` | to be matched in ledger |
| FIT-5.1-03 | assimovt | Distill `user-interview`, `problem-validation`, `experiment-design` as guardrails | `discover-product` | to be matched in ledger |
| FIT-5.1-04 | argo | Pattern: interview-quality rubric (Rich/Mixed/Thin), confidence capped by evidence quality, opportunity routing table | `discover-product` | to be matched in ledger |
| FIT-5.1-05 | shinpr | Pattern: hypothesis-file format (success/failure criteria, confidence per risk, time budget) for `experiments/EXP<n>.md` | `discover-product` | to be matched in ledger |
| FIT-5.1-06 | huntsyea + assimovt | Distill huntsyea `story-mapping` + `shape-up` references; assimovt `scope-cutting`, `bet-sizing` | `define-release` | to be matched in ledger |
| FIT-5.1-07 | gorski | Pattern: Obligation/Expectation/Hope classing for "every must needs a consequence" | `define-release` | to be matched in ledger |
| FIT-5.1-08 | northstar | **Call**: `ai-analyst-lab/north-star` to audit success/outcome metrics | `define-release`, `validate-release` | to be matched in ledger |
| FIT-5.1-09 | shinpr | Pattern: `hypothesis-verifier` context separation → the AFK review gate (answers plan open question 4) | `specify-requirements` | to be matched in ledger |
| FIT-5.1-10 | gorski | Pattern: `validate` → mechanical traceability check over the loop workspace (new step or micro-skill) | `specify-requirements` | to be matched in ledger |
| FIT-5.1-11 | 45ck + daves | Call (conditional, audit depth first): 45ck `quality-attribute-scenario-writer`; pattern: Dave's `nfr-review` check dimensions | `specify-requirements` (QAS) | to be matched in ledger |
| FIT-5.1-12 | florianbonnet | Pattern (guardrail): "plan the analysis before running it" | `validate-release` | to be matched in ledger |
| FIT-5.1-13 | phuryn | Pattern: command-chaining UX — every skill ends by naming the next stage per `lifecycle-onepager.md` | all loop skills | to be matched in ledger |
| FIT-5.1-14 | forceinjection | Pattern: backtracking-trigger matrix style for the reopen table | loop re-entry spec (`validate-release` reopen table) | to be matched in ledger |
| FIT-5.1-15 | 45ck, lagz0ne, forceinjection, dddcrew | Defer 45ck pack (13 non-QAS skills), lagz0ne `design-skill`, ForceInjection `ddd-*`, ddd-crew process to the future design skillset plan (§6 of skillset plan) | future design skillset (none of the seven) | to be matched in ledger (expected `Defer`) |

## 2. §2 per-skillset analysis — one row per mechanism/benefit/warning

Type: M = mechanism, B = benefit, W = warning, D = disposition note recorded by §2 itself. "Concerns" = which of the seven skills the row plausibly touches.

### 2.1 `deanpeters/Product-Manager-Skills` (§2.1) — verdict: pattern + reference

| Key | Type | Statement (condensed) | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-deanpeters-01 | M | Three-tier skill taxonomy (workflow / interactive / component) is a ready answer to plan open question 3 (skill granularity) | plan-level / all seven skills | pattern |
| FIT-2-deanpeters-02 | M | `press-release` (Amazon Working Backwards) as vision stress test — optional finalize micro-phase | `brainstorm-vision` | pattern (= FIT-5.1-01) |
| FIT-2-deanpeters-03 | B | Battle-tested question sequences, "Adaptive Decision Ladder" interview pattern, named failure-mode catalogs — would otherwise have to be invented | `brainstorm-vision`, `discover-product` | blocked from distill by license; ideas only |
| FIT-2-deanpeters-04 | W | **CC BY-NC-SA 4.0** — non-commercial, share-alike; distilling content contaminates our skills; do **not** copy content | all seven skills / ledger policy | reference only, no copy |
| FIT-2-deanpeters-05 | W | Interaction-heavy skills do not compose into an AFK pipeline | AFK modes of all loop skills | noted as disadvantage |

### 2.2 `phuryn/pm-skills` (§2.1) — verdict: pattern + cherry-pick call

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-phuryn-01 | M | Command-chaining UX: every command ends by suggesting the next one — how loop skills should hand over per `lifecycle-onepager.md` | all seven skills (handover) | pattern (= FIT-5.1-13) |
| FIT-2-phuryn-02 | B | `north-star-metric` and metric-tree skills are solid seeds for `validate-release`; named as alternative call to `ai-analyst-lab/north-star` | `validate-release`, `define-release` | cherry-pick call (alternative) |
| FIT-2-phuryn-03 | W | Installing all 9 plugins floods the trigger namespace and risks shadowing proprietary skill triggers | all seven skills | not a marketplace to install wholesale |
| FIT-2-phuryn-04 | W | PRD-shaped and feature-shaped; no requirements engineering; wholesale adoption buys ~80% irrelevant surface | `specify-requirements`, plan-level | reject wholesale adoption |

### 2.3 `huntsyea/product-skills` (ex-`rohanpatriot`) (§2.2) — verdict: distill (first choice) or call

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-huntsyea-01 | M | `references/` files (28 Torres anti-patterns by phase, JTBD forces framework, Patton slicing principles) are the "failure modes → guardrails" material design principle 6 demands — MIT, already distilled | `discover-product`, `define-release` | distill, vendor with source pointers |
| FIT-2-huntsyea-02 | B | `continuous-discovery` workflows (set-outcomes, map-opportunities, ideate, test-assumptions) map 1:1 onto `discover-product` phases; `story-mapping`/`shape-up` map onto `define-release` (journey shaping, appetite/commitment) | `discover-product`, `define-release` | structural confirmation for distill targets |
| FIT-2-huntsyea-03 | B | SKILL.md + `references/` + `workflows/` structure *is* the progressive-disclosure layout the plan intends — highest quality-per-skill reviewed | all seven skills (authoring layout) | validation of planned layout |
| FIT-2-huntsyea-04 | W | Repo transfer (`rohanpatriot` → `huntsyea`) demonstrates link-rot risk of runtime dependencies (C6); calling installed skills couples the loop to external trigger phrasing; stage-doc URLs already corrected | external-dependency policy (all skills) | vendor, don't call live |

### 2.4 `jacksoncalling/argo-continuous-discovery` (§2.2) — verdict: pattern

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-argo-01 | M | Interview-quality rubric (Rich/Mixed/Thin — story vs. opinion) as the `EV#` strength model | `discover-product` | pattern, fold in (= FIT-5.1-04) |
| FIT-2-argo-02 | M | Confidence capped by evidence quality — "three weak interviews don't equal one good one" | `discover-product` | pattern, fold in (= FIT-5.1-04) |
| FIT-2-argo-03 | M | Routing decision table for extracted opportunities (add/merge/escalate/park) | `discover-product` | pattern, fold in (= FIT-5.1-04) |
| FIT-2-argo-04 | M | Explicit human gate before solutioning (candidate — §2 credits it in fit but the verdict names only the three mechanisms above) | `discover-product` | not explicitly dispositioned; needs ledger decision |
| FIT-2-argo-05 | W | Competing workspace layout (folder scheme + `tree.html`), single-outcome per instance, demo-grade maturity (C6) — do not adopt the operator itself | `discover-product` | reject adoption of operator |

### 2.5 `assimovt/productskills` (§2.2) — verdict: distill

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-assimovt-01 | M | Mom Test core rule "never accept hypothetical enthusiasm" — same guardrail `discover-product` §5.4 specifies | `discover-product` | distill (guardrail) |
| FIT-2-assimovt-02 | M | Primary guardrail/checklist donor: `user-interview`, `problem-validation` (frequency × intensity × WTP), `experiment-design` → `discover-product`; `scope-cutting`, `bet-sizing` → `define-release` | `discover-product`, `define-release` | distill (= FIT-5.1-03, -06) |
| FIT-2-assimovt-03 | B | Right ceremony level for the solo-developer floor (C5) — model of the minimum useful package as skills; MIT, trivially vendorable | `tailor-lifecycle` (ceremony floor), all loop skills | ceremony-floor exemplar |
| FIT-2-assimovt-04 | W | So compact each skill assumes the human orchestrates; nothing connects an interview note to a scope decision (no artifact chain) | `discover-product`, `define-release` | distill content only, keep our chaining |

### 2.6 `shinpr/claude-code-discover` (§2.3) — verdict: pattern (strongest single donor)

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-shinpr-01 | M | Hypothesis-file format (assumption statement, success/failure criteria, confidence per risk dimension, time budget) — a better `EXP#` card than the plan's sketch → `experiments/EXP<n>.md` | `discover-product` (EXP# schema; contract update 6) | pattern, steal (= FIT-5.1-05) |
| FIT-2-shinpr-02 | M | `hypothesis-verifier` runs in a separate context *without seeing the author's expectations* — cleaner builder/critic separation; → `specify-requirements` AFK review gate; answers plan open question 4 | `specify-requirements` | pattern, steal (= FIT-5.1-09) |
| FIT-2-shinpr-03 | M | Auto-maintained `INDEX.md` discipline validates the `discovery-seeds.md` idea → companion index | `create-vision-companion` | pattern, steal |
| FIT-2-shinpr-04 | B | Shares the plan's core thesis: product context lives in the repo beside the code so the coding agent sees it (C2 emphatic) | plan-level validation | confirmation, no separate action |
| FIT-2-shinpr-05 | W | A whole competing pipeline: own artifact taxonomy, own vision/persona/blueprint stages, no spine/UC/QAS/RE — adopting it means adopting its lifecycle (option (a), rejected) | plan-level | reject pipeline adoption; patterns only |

### 2.7 `RafaelGorski/Problem-Based-SRS` (§2.4) — verdict: pattern

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-gorski-01 | M | `validate` action mechanically checks the traceability chain is complete — an idea the plan *lacks*: mechanical traceability check across the whole loop workspace | `specify-requirements` (finalize gate), deterministic linter (contract update 2) | pattern (= FIT-5.1-10) |
| FIT-2-gorski-02 | M | Obligation/Expectation/Hope problem classing — cleaner "every must needs a consequence" enforcement than prose | `define-release` (prioritization) | pattern (= FIT-5.1-07) |
| FIT-2-gorski-03 | W | Rooted in its own ID families (CP/CN/FR) and `.spec/` JSON artifacts; two trace spines in one repo would be worse than one — keep our spine | `specify-requirements`, spine policy | reject remap/adoption of its chain |
| FIT-2-gorski-04 | W | Drags its own upstream (business context, software glance/vision) duplicating our vision + definition stages; Copilot canvas app is baggage | `brainstorm-vision`, `define-release` | reject upstream adoption |

### 2.8 `45ck/software-architecture-skills` (§2.5) — verdict: call (conditional) / out-of-scope rest

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-45ck-01 | M | `quality-attribute-scenario-writer` — the QAS format for quality_attributes.md — as a conditional callable specialist | `specify-requirements` (QAS) | call (conditional) (= FIT-5.1-11) |
| FIT-2-45ck-02 | W | One of ~30 near-identical, evidently semi-generated sibling packs (C6 — depth unverified); audit its SKILL.md depth first; if thin, own QAS sub-file distilled from quality_attributes.md is safer | `specify-requirements` | precondition + named fallback |
| FIT-2-45ck-03 | D | Other 13 skills belong to the future design skillset (candidate list) | none of the seven | out-of-scope / defer (= FIT-5.1-15) |

### 2.9 `DavidROliverBA/Daves-Claude-Code-Skills` (§2.5) — verdict: pattern

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-daves-01 | M | `nfr-review` dimensions (complete? measurable? feasible?) become `specify-requirements`' QAS gate checks | `specify-requirements` | pattern (= FIT-5.1-11) |
| FIT-2-daves-02 | M | `nfr-capture` (ISO 25010, measurable acceptance criteria) overlaps QAS work (candidate — §2 notes the overlap; verdict names only the nfr-review dimensions) | `specify-requirements` | not explicitly dispositioned; needs ledger decision |
| FIT-2-daves-03 | W | Deeply coupled to an Obsidian-vault ecosystem (frontmatter schemas, tag taxonomies) we don't run (C2 mismatch) | `specify-requirements` | reject direct reuse |
| FIT-2-daves-04 | D | Multi-agent fan-out review pattern is already ours via `create-vision-companion` — nothing new to adopt | `create-vision-companion` | no action (already covered) |

### 2.10 `ddd-crew/ddd-starter-modelling-process` (§2.5) — verdict: reference

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-dddcrew-01 | D | Not an agent skill; canonical human 8-step DDD process with canvases — reference for `domain-modeling` and the future design skillset; nothing to install; CC BY 4.0 (attribute if any content used) | none of the seven directly | reference / defer (= FIT-5.1-15) |
| FIT-2-dddcrew-02 | W | Stage doc's "Agent rule sets" label slightly misfiles it | stage-doc hygiene | noted correction |

### 2.11 `ForceInjection/domain-driven-design-skills` (§2.5) — verdict: pattern (for the whole skillset program)

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-forceinjection-01 | M | Explicit backtracking-trigger matrix (per-skill: inputs, outputs, validation checklist, quantified triggers, e.g. "invariant expression rate < 60% → return to X") — the formalized version of the loop's "reopen" arrows; imitate when specifying re-entry conditions (`validate-release` → which artifact reopens) | `validate-release`, handover/re-entry spec (contract update 7) | pattern (= FIT-5.1-14) |
| FIT-2-forceinjection-02 | B | Blind-run validation against the canonical Cargo sample with scoring (85.8%) — rigorous skill-validation practice (candidate relevance to regression validation, contract update 3; §2 does not disposition it) | skillset regression validation | not explicitly dispositioned; needs ledger decision |
| FIT-2-forceinjection-03 | W | Explicitly WIP, docs primarily Chinese (C6); scope (domain modeling → tactical design) overlaps `domain-modeling`/design skillset, not this loop | none of the seven directly | out-of-scope here; revisit for design skillset (= FIT-5.1-15) |

### 2.12 `lagz0ne/design-skill` (§2.5) — verdict: out-of-scope

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-lagz0ne-01 | D | Its 5 phases start where the loop ends; Phase 1 "Requirements" Q&A is far below requirements_engineering.md's bar — not a substitute for any loop skill; candidate for the design skillset | none of the seven | out-of-scope / defer (= FIT-5.1-15) |

### 2.13 `ai-analyst-lab/north-star` (§2.6) — verdict: call, reuse as-is

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-northstar-01 | M | Call as-is (like `prototype`): optional "audit the success metric" step — `audit` (7-question grading, refuses vanity metrics), `drivers`, `inputs` (input tree, each input a driver not the NSM renamed), `explain`, `triage` | `define-release`, `validate-release` | call (= FIT-5.1-08) |
| FIT-2-northstar-02 | B | Best-engineered single-purpose skill reviewed: Python-backed deterministic checks, CI-tested, cited line-by-line to Amplitude's playbook; metric hygiene is self-contained, doesn't need spine access (C1/C2 n/a) | `define-release`, `validate-release` | justification for call mode |
| FIT-2-northstar-03 | W | Playbook-derived content remains © Amplitude (educational use); code is MIT | license/provenance policy | license note to record |

### 2.14 `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` (§2.6) — verdict: reference

| Key | Type | Statement | Concerns | §2 disposition |
| --- | --- | --- | --- | --- |
| FIT-2-florianbonnet-01 | M | `analysis-planner` — "plan the analysis (structure the investigation) before touching data" — borrow as `validate-release` review-prep guardrail | `validate-release` | pattern/guardrail (= FIT-5.1-12) |
| FIT-2-florianbonnet-02 | W | No stated license (C6 fails for redistribution), manual install, no tests; overlaps north-star with lower maturity — prefer `ai-analyst-lab/north-star`; idea only, no content copy | `validate-release`, license policy | reference only |

## 3. Coverage expectations

### Repositories with no actionable contribution to the seven loop skills

Per the fit analysis itself, these contribute nothing to be adopted/adapted/called inside the seven loop-skill ledgers — expected ledger disposition `Defer` (to the future design skillset) or `Reject`/reference:

- `lagz0ne/design-skill` — out-of-scope entirely (FIT-2-lagz0ne-01).
- `ddd-crew/ddd-starter-modelling-process` — reference only, nothing to install (FIT-2-dddcrew-01).
- `ForceInjection/domain-driven-design-skills` — out-of-scope for the loop *except* the backtracking-trigger pattern FIT-2-forceinjection-01, which is actionable.
- `45ck/software-architecture-skills` — out-of-scope *except* `quality-attribute-scenario-writer` (FIT-2-45ck-01, conditional call).

Every other repository (deanpeters, phuryn, huntsyea, argo, assimovt, shinpr, gorski, daves, northstar, florianbonnet) has at least one actionable pattern/distill/call row above and must appear in at least one ledger.

### License warnings (must surface in ledger dispositions and the external-dependency policy)

| Source | License | Constraint |
| --- | --- | --- |
| deanpeters/Product-Manager-Skills | **CC BY-NC-SA 4.0** | Do **not** copy or distill any content (non-commercial + share-alike contamination). Patterns/ideas only. Matches the revision contract's explicit prohibition. |
| florianbonnet14/ThePowerOfAnalytics_ClaudeSkills | **Unlicensed** | Reference-only; no redistribution or distill. |
| ai-analyst-lab/north-star | MIT (code); playbook content **© Amplitude** (educational use) | Call the skill; do not vendor the Amplitude-derived content as ours. |
| ddd-crew/ddd-starter-modelling-process | CC BY 4.0 | Attribution required if any content is ever used. |
| phuryn, huntsyea, assimovt, shinpr, gorski, 45ck, lagz0ne | MIT | Distill/call permitted with source pointer + retrieval date per the vendoring policy. |
| DavidROliverBA/Daves-Claude-Code-Skills | Not stated in fit analysis | Verify license before any distill; §2 verdict is pattern-only, which needs no content copy. |
| jacksoncalling/argo-continuous-discovery | Not stated in fit analysis | Verify license before any distill; §2 verdict is pattern-only. |

### Cross-cutting expectations for the gate agent

- No external pack satisfies C1 (traceability spine) — any ledger row proposing spine ownership by an external tool contradicts the fit analysis.
- Runtime third-party fetches are prohibited; one of the 14 references already moved repos (rohanpatriot → huntsyea).
- Three rows above are flagged "not explicitly dispositioned; needs ledger decision": FIT-2-argo-04, FIT-2-daves-02, FIT-2-forceinjection-02 — plus the two license-unknown verifications (daves, argo). The gate must find an explicit disposition for each.
