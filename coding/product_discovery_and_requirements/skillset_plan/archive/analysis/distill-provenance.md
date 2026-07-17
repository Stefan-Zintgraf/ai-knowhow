# Distill donor audit — provenance digest (Phase 0)

**Scope:** Every ledger row across the seven contribution ledgers whose reuse mode is (or includes) `distill`.
**Method:** Read-only audit of the seven ledgers plus a filesystem sweep for vendored donor material. No network fetches performed.
**Governing rules:** Contract ledger rules for `distill` rows (6-point donor-audit record: repo+path; commit/tag or retrieval date; license+attribution; candidates; per-candidate disposition; destination file/section), ordered update 5 (`distill` = vendored content with source file, commit/tag or retrieval date, license, attribution), and the acceptance-gate item "Every `distill` row has a future authoring-time donor-audit task plus license and provenance requirements; incompatible and unlicensed content is not scheduled for copying."

## Global findings

1. **No donor material is vendored locally.** A full sweep of `c:/PROJ/ai-knowhow/coding/product_discovery_and_requirements/` (including `skillset_plan/`) finds only method docs, the plan, the fit analysis, the contract, and the seven ledgers. There is no `vendor/` directory, no donor snapshot, and no provenance manifest. **Vendoring is an authoring-time task for every distill row.**
2. **No distill row records a commit/tag or retrieval date.** Every ledger instead instructs that these be captured "before authoring" (define-release §2 and specify-requirements §2 open with that instruction; discover-product and tailor-lifecycle carry source-audit manifests demanding pinned revisions). This is contract-consistent for a planning-stage ledger, but no row is yet provenance-complete in the update-5 sense.
3. **Donor paths are recorded at skill/directory granularity only** (e.g. `huntsyea/product-skills — story-mapping references/workflows`), never as exact files. Exact-file identification is deferred to the authoring-time audit.
4. **Candidate-level dispositions are not yet enumerated.** Rows name candidate technique classes and a row-level disposition (often "adopt/adapt subject to source audit"), but the per-candidate inventory the contract's point 4–6 requires does not yet exist anywhere.
5. **No license-blocked content is scheduled for distillation.** All distill donors are recorded MIT. Every `deanpeters/Product-Manager-Skills` row in every ledger is `reference only` / `reject for distillation` with the CC BY-NC-SA prohibition explicitly recorded (BV-E01/02, TL-002/003, DP-018, DR-EXT-10, SR-EXT-09, VC-E11). The unlicensed `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` is pattern-only/no-distillation (VR-EXT-03, BV-E12). One caveat: hybrid row DP-012 lists Argo (license "not established") among its donors — its distill portion must be confined to the MIT donors (huntsyea, phuryn) unless Argo's license is verified.
6. **Ledgers with zero distill rows:** `brainstorm-vision` (BV-E04 explicitly *defers* JTBD distillation to `discover-product`, requiring "source pointer and retrieval date" if later distilled), `create-vision-companion`, `tailor-lifecycle` (TL-009/TL-010 define the distill *policy* and donor-audit *process* but distill nothing), `validate-release`.

## Per-row records

Field key: (1) ledger+ID · (2) donor repo/path · (3) commit/retrieval date · (4) license/attribution · (5) vendored locally? · (6) candidates + dispositions · (7) destination · (8) authoring-time donor-audit task.

### discover-product (`discover-product-contributions.md`) — 7 pure distill, 2 hybrid

#### DP-001 — mode: Distill
2. `huntsyea/product-skills` — `continuous-discovery` skill, references, workflows (no exact files named).
3. Commit/tag: **missing**. Retrieval date: **missing**.
4. MIT recorded. Row requires vendoring "with source path, pinned revision, attribution, and date" — requirements stated, values absent.
5. Not vendored; authoring-time task.
6. Candidates: outcome-setting, opportunity-mapping, solution-ideation, assumption-testing workflows; phase anti-patterns. Row disposition "Adopt subject to source audit" — per-candidate dispositions **not yet recorded**.
7. Destination: `discover-product` phases (must preserve the method's seven-step sequence). Exact skill file/section **not yet recorded**.
8. Task: inspect the complete `continuous-discovery` skill/reference/workflow trees at a pinned revision (per the ledger's source-audit manifest); inventory every technique/checklist/rubric/guardrail/failure mode/completion signal; assign each a disposition and destination; vendor adopted material with source path, revision, license, attribution, date; produce the source manifest mapping each distilled item to destination and test.

#### DP-002 — mode: Distill
2. `huntsyea/product-skills` — `jobs-to-be-done`.
3. **Missing** (both).
4. MIT; "attribution required".
5. Not vendored.
6. Candidates: JTBD switch-interview and forces techniques. "Adopt subject to source audit"; per-candidate dispositions **missing**. Cross-ledger note: `brainstorm-vision` BV-E04 defers its JTBD contribution here and requires source pointer + retrieval date on distillation.
7. Destination: optional technique routing in `discover-product` (uncertainty about motivation/switching/alternatives/workarounds). Exact file/section **missing**.
8. Task: audit `jobs-to-be-done` tree at pinned revision; distill interview/forces techniques with provenance; wire into technique-routing guidance + fixture (recommends JTBD only for appropriate uncertainty, records past behavior); satisfy BV-E04's deferred-provenance condition.

#### DP-003 — mode: Distill
2. `huntsyea/product-skills` — references (anti-pattern catalogue); exact files **missing**.
3. **Missing**.
4. MIT.
5. Not vendored.
6. Candidates: phase-specific discovery anti-patterns. Row requires each relevant anti-pattern mapped to a prompt guardrail, finalize check, exclusion, or explicit rejection — that mapping ("anti-pattern coverage table") **does not exist yet**.
7. Destination: guardrails/finalize checks across `discover-product` phases; exact locations **missing**.
8. Task: enumerate the full anti-pattern catalogue at pinned revision; build the coverage table with no unassigned relevant item; vendor distilled text with provenance.

#### DP-004 — mode: Distill
2. `assimovt/productskills` — `user-interview`.
3. **Missing**.
4. MIT.
5. Not vendored.
6. Candidates: past-behavior/Mom Test interviewing guardrails (concrete recent behavior; stories/actions/facts vs opinions/hypothetical enthusiasm). "Adopt subject to source audit"; per-candidate dispositions **missing**.
7. Destination: evidence-gathering phase guardrails; fixtures classifying hypothetical enthusiasm as weak; no `EV#` without supplied source. Exact file/section **missing**.
8. Task: audit `user-interview` at pinned revision; distill guardrails with provenance; implement classification fixtures.

#### DP-005 — mode: Distill
2. `assimovt/productskills` — `problem-validation`.
3. **Missing**.
4. MIT.
5. Not vendored.
6. Candidates: problem-validation rubric (frequency, intensity, willingness-to-pay or justified substitute). Row disposition "Adapt subject to source audit" — rubric must not be treated as universal certainty.
7. Destination: evidence/opportunity assessment in `discover-product`; exact section **missing**.
8. Task: audit at pinned revision; adapt rubric onto the proprietary evidence model; record applicability limits; fixture avoiding unsupported confidence; vendor with provenance.

#### DP-006 — mode: Distill
2. `assimovt/productskills` — `opportunity-mapping`.
3. **Missing**.
4. MIT.
5. Not vendored.
6. Candidates: solution-neutrality and hierarchy checks for opportunities. "Adapt subject to source audit". Row explicitly requires the audit to record each guardrail as **incorporated, redundant, or rejected with reasons** — the clearest per-candidate-disposition demand in this ledger; none recorded yet.
7. Destination: comparison against the proprietary `OPP#` model; exact file/section **missing**.
8. Task: audit at pinned revision; per-guardrail disposition table (incorporated/redundant/rejected + reason); vendor incorporated items with provenance.

#### DP-007 — mode: Distill
2. `assimovt/productskills` — `experiment-design`.
3. **Missing**.
4. MIT.
5. Not vendored.
6. Candidates: experiment method-selection, criteria, and decision-linkage guardrails. "Adopt subject to source audit"; must not replace the proprietary `EXP#` schema.
7. Destination: `EXP#` design guidance (every `EXP#` cites decision + assumption, preregisters support/refute/inconclusive). Interacts with ordered update 6 (strengthened `EXP#` schema). Exact section **missing**.
8. Task: audit at pinned revision; distill guardrails into the update-6 merged experiment-card schema; vendor with provenance; expose required/open fields to the linter.

#### DP-012 — mode: Pattern / distill (hybrid)
2. Three donors: `jacksoncalling/argo-continuous-discovery` solution phase; `huntsyea/product-skills` ideation; `phuryn/pm-skills` brainstorming chain.
3. **Missing** for all three.
4. huntsyea MIT; phuryn MIT; **Argo license "not established"** elsewhere in this ledger (DP-008: "pattern only unless verified"). Row says "Respect each donor license; independently implement the convergent method requirement." **Flag:** any distilled text must come only from the MIT donors unless Argo's license is verified at audit time; otherwise Argo stays pattern-only (reference).
5. Not vendored.
6. Candidates: generating >= 3 materially different solution directions incl. process/policy/manual-service/no-build. Disposition: Adopt (final at row level).
7. Destination: `SOL#` alternatives-generation step (ordered update 1); finalize check blocking single-solution without `DEC#`.
8. Task: audit all three donors' ideation/solution material at pinned revisions; verify Argo license before any copying (else pattern-only); distill MIT material with provenance; per-candidate dispositions.

#### DP-019 — mode: Pattern / distill (hybrid)
2. "Method docs, strengthened by reviewed discovery packs" — donor set **not precisely identified** (implicitly the discovery packs above: huntsyea, assimovt, Argo, shinpr).
3. **Missing**.
4. "Proprietary orchestration; donor content follows license" — per-donor license duties inherit from the packs actually drawn on.
5. Not vendored.
6. Candidates: cheapest-trustworthy-test selection (prototype, concierge/Wizard-of-Oz, spike, data analysis, demand test, policy/security/legal review, pilot). Disposition: Adopt.
7. Destination: experiment method-selection guidance; fixtures covering all four risks, rejecting non-diagnostic tests. Exact section **missing**.
8. Task: during the pack audits (DP-001..DP-007 and Argo/shinpr scopes in the manifest), tag any distilled test-selection material with its actual donor, revision, license, attribution, date; keep orchestration independently authored.

### define-release (`define-release-contributions.md`) — 5 distill rows

Ledger-level provenance instruction (§2): "Before authoring, replace every source pointer below with the exact repository URL, commit SHA or release, files inspected, retrieval date, and verified license." None replaced yet.

#### DR-EXT-01 — mode: distill
2. `huntsyea/product-skills` — `story-mapping` references/workflows.
3. **Missing**. Note: row additionally requires recording the "former `rohanpatriot` location" — a repo-relocation provenance nuance unique to this donor.
4. MIT.
5. Not vendored.
6. Candidates: journey backbone, task decomposition, omission finding, thin end-to-end slicing, flat-backlog anti-patterns. Disposition: adopt (final at row level); per-candidate dispositions **missing**.
7. Destination: a progressive-disclosure story-mapping reference used when shaping journeys and cutting a coherent release (a named reference file inside `define-release` — exact filename **not recorded**).
8. Task: audit exact files at pinned commit; record former rohanpatriot location; vendor the reference with full provenance; fixture proving end-to-end slice passes and single-layer slice fails.

#### DR-EXT-02 — mode: distill
2. `huntsyea/product-skills` — `shape-up` references/workflows.
3. **Missing**.
4. MIT; "exact source-file audit required".
5. Not vendored.
6. Candidates: appetite, pitch shaping, commitment/betting discipline, boundaries, risks, no-go decisions. Disposition: adapt — translate onto the proprietary `REL` artifact; no competing pitch artifact.
7. Destination: optional shaping path in `define-release`; exact file/section **missing**.
8. Task: audit at pinned commit; distill only what translates into `REL`; vendor with provenance; high- and low-ceremony fixtures (appetite constrains scope without becoming mandatory).

#### DR-EXT-03 — mode: distill
2. `assimovt/productskills` — `scope-cutting`.
3. **Missing**.
4. MIT; "record exact file and commit".
5. Not vendored.
6. Candidates: scope-reduction checks; coherent-slice guardrails ("small" vs "coherent"). Disposition: adopt.
7. Destination: scope-cutting prompts and failure checks in `define-release`; exact section **missing**.
8. Task: audit at pinned commit; vendor with provenance; negative fixture (disconnected items fail finalization).

#### DR-EXT-04 — mode: distill
2. `assimovt/productskills` — `bet-sizing`.
3. **Missing**.
4. MIT.
5. Not vendored.
6. Candidates: sizing investment against uncertainty, reversibility, learning value. Disposition: adapt (complements lifecycle ceremony and stop criteria).
7. Destination: proportional-investment check in `define-release`; exact section **missing**.
8. Task: audit at pinned commit; vendor with provenance; fixture (reversible uncertainty gets smaller bet than irreversible regulated commitment).

#### DR-EXT-05 — mode: distill
2. `assimovt/productskills` — `prd-writing`.
3. **Missing**.
4. MIT; "exact source-file audit required".
5. Not vendored.
6. Candidates: evidence-first scope-rationale guardrails **only** — the PRD form and artifact taxonomy are explicitly excluded. Disposition: adapt.
7. Destination: scope-decision guardrails (every scope decision resolves to evidence or carries explicit `DEC` override); exact section **missing**.
8. Task: audit at pinned commit; distill only evidence-first guardrails; confirm no PRD taxonomy leaks in; vendor with provenance.

### specify-requirements (`specify-requirements-contributions.md`) — 1 distill row

#### SR-EXT-08 — mode: distilled upstream input
2. `huntsyea/product-skills` — `story-mapping` (same donor as DR-EXT-01; here consumed as the *upstream distilled* material).
3. **Missing**; row requires "exact files, commit, and retrieval date".
4. MIT.
5. Not vendored.
6. Candidates: alternatives, failures, handoffs, operational tasks, slice boundaries discovered during story mapping. Disposition: adapt — validate/elaborate the committed slice into use cases; no scope recreation or silent out-of-scope stories.
7. Destination: UC-elaboration guidance in `specify-requirements`; exact file/section **missing**.
8. Task: reuse the DR-EXT-01 vendored donor audit (single shared provenance record for this donor); confirm the same pinned revision serves both consumers; fixture (UC elaboration preserves slice boundary while surfacing unresolved paths). If DR-EXT-01 and SR-EXT-08 audit different revisions, the ledgers must record and reconcile the divergence.

### Ledgers with no distill rows

| Ledger | Distill rows | Notes |
| --- | --- | --- |
| `brainstorm-vision-contributions.md` | 0 | BV-E04 defers JTBD distillation to `discover-product` (met by DP-002); BV-E01/E02 use deanpeters as pattern/reference only under the CC BY-NC-SA prohibition. |
| `create-vision-companion-contributions.md` | 0 | All pattern/reference; VC-E11 keeps deanpeters reference-only ("no distillation"). |
| `tailor-lifecycle-contributions.md` | 0 | TL-009 (distill policy fields) and TL-010 (donor-audit process) are policy/process rows, not distill rows; its source-audit manifest audits six donors for pattern extraction only. |
| `validate-release-contributions.md` | 0 | VR-EXT-03 is explicitly "no content distillation" for the unlicensed florianbonnet14 repo; all others call/pattern/reference. |

## License-sensitivity check (contract: no CC BY-NC-SA / unlicensed distillation)

- `deanpeters/Product-Manager-Skills` (CC BY-NC-SA 4.0): appears in all seven ledgers' orbit; **never in distill mode**. Explicit no-copy/no-distill markers: BV-E01, BV-E02, VC-E11, TL-002, TL-003, DP-018, DR-EXT-10 ("reject for distillation"), SR-EXT-09 ("reject for distillation"). Compliant as planned.
- `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` (no stated license): BV-E12 defer/no-copy; VR-EXT-03 pattern-only, independently authored. Not scheduled for distillation. Compliant.
- `jacksoncalling/argo-continuous-discovery` (license not established): pattern-only everywhere except its inclusion among DP-012's donors — **verify license at audit time or confine DP-012 distillation to MIT donors**.
- `ForceInjection/domain-driven-design-skills` (WIP/unverified license): pattern-only in all ledgers; no distill exposure.

## Summary table

| Metric | Count | Detail |
| --- | --- | --- |
| Distill rows total | **15** | discover-product 9 (DP-001..007 pure; DP-012, DP-019 hybrid pattern/distill), define-release 5 (DR-EXT-01..05), specify-requirements 1 (SR-EXT-08); brainstorm-vision 0, create-vision-companion 0, tailor-lifecycle 0, validate-release 0 |
| Fully provenance-complete (all 6 contract fields) | **0** | No row has commit/tag or retrieval date; none vendored; no per-candidate dispositions; no exact destination file/section |
| Missing commit/tag or retrieval date | 15 of 15 | All defer pinning to authoring time |
| Missing exact donor file paths (repo+skill dir only) | 15 of 15 | Exact-file audit is an authoring-time task in every row |
| License recorded | 15 of 15 | All MIT (DP-012 partially: Argo component unverified — pattern-only until verified; DP-019 inherits per actual donor) |
| Vendored locally | 0 of 15 | No vendor directory or provenance manifest exists anywhere under `product_discovery_and_requirements/` |
| License-blocked distill rows | **0** | No CC BY-NC-SA or unlicensed material is scheduled for distillation; deanpeters and florianbonnet14 correctly excluded in every ledger |
| Rows with a concrete authoring-time donor-audit task derivable | 15 of 15 | Each row's audit task is recorded above; acceptance-gate item "every distill row has a future authoring-time donor-audit task plus license and provenance requirements" is satisfiable — update 8 should make these tasks explicit in the plan |

**Distinct donor repositories behind all distill rows: 2 (+2 conditional).** `huntsyea/product-skills` (DP-001/002/003/012/019, DR-EXT-01/02, SR-EXT-08 — note former `rohanpatriot` location for story-mapping) and `assimovt/productskills` (DP-004/005/006/007, DR-EXT-03/04/05); conditional/partial: `jacksoncalling/argo-continuous-discovery` and `phuryn/pm-skills` inside hybrid DP-012. Two pinned donor snapshots would cover nearly the entire distill surface; DR-EXT-01 and SR-EXT-08 should share one provenance record.
