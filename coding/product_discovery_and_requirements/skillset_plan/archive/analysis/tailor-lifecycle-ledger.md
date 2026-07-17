# Phase 0 digest — `tailor-lifecycle` ledger audit

**Source ledger:** `skillset_plan/tailor-lifecycle-contributions.md` (read 2026-07-16)
**Method doc consulted:** `../lifecycle_tailoring.md` (cited by the ledger's method-document coverage table)
**Frozen input for Phase 1 write agents applying updates 4, 7, 9, 10.**

## 1. Row inventory

| ID | Source | License | Mode | Disposition | Intended incorporation (one line) |
| --- | --- | --- | --- | --- | --- |
| TL-001 | `phuryn/pm-skills` | MIT | Pattern | Adapt | End every tailoring session by naming selected entry skill, later stages, reason, and input artifact |
| TL-002 | `deanpeters/Product-Manager-Skills` | CC BY-NC-SA 4.0 | Pattern / reference only | Adapt | Keep the skill a short interactive workflow that selects components; independently authored, attributed design influence only |
| TL-003 | `deanpeters/Product-Manager-Skills` (Adaptive Decision Ladder) | CC BY-NC-SA 4.0 | Pattern / reference only | Adapt | Adaptive interview depth: ask only enough to resolve entry point, ceremony, cadence, artifacts, authority, revisit trigger |
| TL-004 | `assimovt/productskills` | MIT | Pattern | Adapt | Preserve minimum-useful-package path for low-risk solo work; full ceremony never the default |
| TL-005 | `ForceInjection/domain-driven-design-skills` | Not established (pattern-only unless audit confirms) | Pattern | Adapt | Turn the one-pager revisit trigger into concrete evidence conditions naming the reconsidered tailoring decision |
| TL-006 | `RafaelGorski/Problem-Based-SRS` | MIT | Pattern | Adapt | Run the shared loop-workspace linter at finalize; applicable failures block except under open-marker policy |
| TL-007 | `ai-analyst-lab/north-star` | MIT code (metric content not used) | Pattern | Adapt | Separate code-checkable completeness (shared linter) from judgment-based review |
| TL-008 | `ForceInjection/domain-driven-design-skills` | Not confirmed (pattern-only) | Pattern | Adapt | Include the skill in the scored end-to-end reference-topic run against method completion checks |
| TL-009 | Cross-cutting finding in `github_skillsets.md` | Mandatory policy | Policy | Adopt | Pinned runtime calls; distilled material carries full provenance; never fetch donor repos at runtime |
| TL-010 | Coverage assurance requirement | Audit-before-copy | Authoring process | Adopt | Inspect assigned donor material directly; record every candidate in the audit manifest |
| TL-011 | Proprietary glossary and spine | Proprietary | Policy | Adopt | Use canonical method vocabulary exactly as defined |
| TL-012 | Cross-cutting finding | Mandatory | Policy | Adopt | Produce only `lifecycle-onepager.md`; import no donor workspace/taxonomy/stage-artifact scheme |
| TL-013 | Proprietary method (+ ceremony comparison) | Proprietary | Policy | Adopt | Every unselected lifecycle stage is listed with a reason |
| TL-014 | Proprietary method + phuryn UX pattern | No external dependency | Pattern | Adapt | Derive the suggested next stage from entry point and selected stages (rework→validation evidence, mandate→requirements, fast-follow→definition) |
| TL-015 | Proprietary method | Proprietary | Policy | Adopt | Exactly one accountable owner per consequential decision; no group labels; escalation recorded |
| TL-016 | Proprietary method + compact-coach comparison | Proprietary | Policy | Adopt | Recommend stages/artifacts only when they reduce an important uncertainty or improve a consequential decision |

**Counts:** 16 rows — Adapt 9 (TL-001..008, TL-014), Adopt 7 (TL-009..013, TL-015, TL-016), Call 0, Reject 0, Defer 0, Pending 0.

## 2. Compliance audit against contract ledger rules

- **Required fields:** every row has stable ID, source, license/dependency constraint, reuse mode, intended incorporation, disposition, and objective evidence (Verification column). No missing fields.
- **Pending:** none. The ledger's own gate ("none remains Pending audit") is satisfiable as written.
- **Realizing evidence:** every accepted row cites a concrete verification target — acceptance-test fixtures (TL-001, TL-004, TL-005, TL-014, TL-016), skill-structure/terminology review (TL-002, TL-011), question-budget fixtures (TL-003), finalize/linter tests (TL-006, TL-007, TL-013), reference-run report (TL-008), dependency/audit manifests (TL-009, TL-010), file-output test (TL-012), ownership validator/rubric (TL-015). All map to the contract's allowed evidence classes (fixture, finalize check, linter rule, validation scenario, manifest).
- **License caveats (non-blocking but must be carried into the plan):**
  - TL-005 and TL-008: `ForceInjection/domain-driven-design-skills` license not established — correctly held to pattern-only (local implementation, inspiration recorded) unless the donor audit confirms terms. Write phase must not schedule any copying from this repo.
  - TL-002/TL-003: CC BY-NC-SA — mode is pattern/reference-only with an explicit no-copy/no-distill constraint and a manifest objective to "prove no CC BY-NC-SA text was distilled". Compliant with the contract's deanpeters prohibition; keep the attribution-as-design-influence note.
- **Deviation from contract vocabulary (minor):** the ledger's local disposition list includes "Pending audit" as an allowed transient state; contract allows only the five final dispositions. No row uses it, so no correction needed — but the write phase should not import "Pending audit" into the plan.

## 3. Accepted rows — realizing mechanism the revised plan must contain (update 4)

| ID | Mechanism the plan section for `tailor-lifecycle` must state |
| --- | --- |
| TL-001 / TL-014 | Handover UX: every successful run ends by naming the selected entry skill, later enabled stages, reason, and required input artifact; next stage derived from entry point + selected stages, not a hard-coded order. (Also realizes update 7 for this skill.) |
| TL-002 | Skill stays a short interactive component-selecting workflow; no absorption of routed-to stages. |
| TL-003 | Adaptive interview depth with a 10–15-question target for low-risk topics; deepen only on risk/ambiguity, with recorded reason. |
| TL-004 / TL-016 | Minimum-ceremony default path; stage/artifact recommendation strictly uncertainty-driven; completeness-driven selection is a guarded failure mode. |
| TL-005 | Revisit trigger must be concrete evidence conditions naming which tailoring decision is reconsidered (backtracking/re-entry trigger — update 7 hook). |
| TL-006 / TL-007 | Shared deterministic linter runs at finalize; deterministic results reported separately from judgment-rubric results; applicable failures block except under open-marker policy (update 2 linkage). |
| TL-008 | Skill included in the canonical reference-topic regression run and scored against the six lifecycle-tailoring completion checks (update 3 linkage). |
| TL-009 | External-dependency policy: pinned calls, vendored provenance, no runtime fetch (update 5 linkage). |
| TL-010 | Authoring-time focused donor audit per the manifest table (six repos listed in the ledger). |
| TL-011 / TL-012 | Canonical terminology; sole output `lifecycle-onepager.md`; no external taxonomy displaces the proprietary model. |
| TL-013 | Finalize fails when a known stage is neither selected nor explicitly skipped with a reason (update 7 skip-recording). |
| TL-015 | Ownership gate: exactly one named accountable owner per consequential decision type, escalation path required, group labels rejected (update 9 base). |

## 4. `distill` rows

**None.** No row uses `distill` mode; all external reuse is Pattern or Policy. Nothing is vendored and nothing needs vendoring for this skill. The two `deanpeters` rows (TL-002, TL-003) are CC BY-NC-SA but explicitly reference-only with a no-copy/no-distill constraint and a manifest proof obligation — flag for the distill-provenance auditor only as a negative check (confirm nothing was distilled), not as donor content. The donor-audit manifest (ledger section "Focused external source-audit manifest") is an authoring-time task list, still unexecuted: no pinned commits/tags or retrieval dates recorded yet. Update 4/8 write agents should carry it forward as a future authoring-time task, per the acceptance gate's distill/audit checkbox.

## 5. `Call` rows

**None.** `tailor-lifecycle` has no callable specialists. Consistent with its exclusions: north-star metric auditing belongs to `define-release`/`validate-release`; QAS work belongs elsewhere. Update 4's `north-star` and `quality-attribute-scenario-writer` skills-table additions do NOT create obligations for this skill. TL-007 reuses `ai-analyst-lab/north-star` only as an engineering pattern (MIT code), not as a call — no version-pinning or fallback needed here.

## 6. `Defer` rows

**No formal Defer rows.** Deferrals live in the "Exclusions and deferrals" prose section, and each names its receiver: press-release stress test → `brainstorm-vision`; north-star metric auditing → `define-release` + `validate-release`; `SOL#`/evidence scoring/opportunity routing/experiment cards → `discover-product`; requirements trace validation → shared linter + `specify-requirements`; DDD tactical design/architecture/EventStorming/interface skills → future design skillset. All named — compliant in substance. One genuinely open plan-level decision is recorded there: **whether out-of-order execution warns or refuses** — the write phase (update 7) must resolve or explicitly assign this, since the ledger requires the implemented behavior to be explicit and tested.

## 7. Method-owned row gaps (updates 9 & 10) — proposed new rows

TL-015 covers single accountable owner + escalation, but two update-9 obligations and the update-10 roadmap obligation have **no row**. `lifecycle_tailoring.md` already carries the method content (Step 5 + completion checks reference contributors/specialists/approvers; Step 3 contains the ceremony-gated roadmap paragraph), so these are method-owned rows (no external license/disposition needed):

| Proposed ID | Rule (contract source) | Intended incorporation | Objective evidence |
| --- | --- | --- | --- |
| **TL-M01** | Update 9: one-pager records, per consequential decision/stage, the accountable owner, required contributors, specialist authorities, formal approvers, evidence required to decide, escalation path, and evidence-based reopen trigger; a group/department is not an accountable owner | Extend the lifecycle one-pager Decision-authority section (template in `lifecycle_tailoring.md`) beyond `<decision type> — <owner>` to all seven fields; tailoring interview elicits them; finalize blocks on missing fields or group-only owner | Golden-file/schema test on the extended one-pager section; finalize/ownership-validator fixture where a group-only owner or missing approver field is refused (regression scenario "group-only owner") |
| **TL-M02** | Update 9: require early specialist participation (engineering, design, ops, security, compliance, domain) where their evidence is material; product must not fabricate specialist evidence | Tailoring interview asks which specialist evidence is material for the topic and names required contributors/specialist authorities in the one-pager; downstream skills gate on them | Fixture in which required specialist/engineering input is missing and the skillset detects and refuses (regression scenario "missing required specialist/engineering input"); one-pager fixture naming specialist authorities per decision type |
| **TL-M03** | Update 10: roadmap optional and ceremony-gated; `tailor-lifecycle` records adoption or skip based on coordination cost, sponsor communication, and product lifetime; when adopted, `define-release` maintains an outcome-based rolling now/next/later view; never required for low-ceremony topics | One-pager Artifacts section records an explicit roadmap adopt/skip decision with the driving ceremony driver(s); adoption hands the maintenance obligation to `define-release`; skip cites the vision strategy list + decision log as the substitute (per `lifecycle_tailoring.md` Step 3) | Paired fixtures: low-ceremony topic records roadmap skipped with reason; high-coordination topic records adoption (regression scenario "roadmap skipped for low ceremony and adopted for high coordination"); linter rule "roadmap entries: outcome mandatory, feature/date-only invalid" |

No update-10 vision-pivot/discovery-pivot row is needed here: update 10 assigns pivot mechanics and ledger-reopening to `brainstorm-vision`, `create-vision-companion`, `discover-product`, `define-release`, `validate-release` — `tailor-lifecycle` participates only via the roadmap gate (TL-M03).

## 8. Other notes for the write-phase agents (updates 4, 7, 9, 10)

- **Update 7:** realizing rows already exist — TL-001/TL-014 (handover), TL-013 (recorded skips), TL-005 (re-entry triggers). Two additions needed in the plan text: (a) the contract clause "command chaining must not override lifecycle tailoring" has no explicit guardrail row or fixture — attach it to TL-001/TL-014's realization or fold into TL-M01/handover prose with a fixture; (b) resolve the open out-of-order warn-vs-refuse decision (see §6). `validate-release` backtracking-condition mapping is out of this skill's scope except that the one-pager revisit trigger (TL-005) is the receiving mechanism on the tailoring side.
- **Update 9:** keep rules inside `tailor-lifecycle` + `lifecycle-onepager.md`; no standalone ownership skill — consistent with the ledger's exclusions. TL-015 + TL-M01 + TL-M02 together realize update 9 for this skill.
- **Update 10:** `lifecycle_tailoring.md` Step 3 already states the roadmap ceremony-gating rule verbatim (drivers: coordination cost, sponsor communication, product lifetime; outcome-based now/next/later; never features-and-dates), so TL-M03 is a ledger/plan sync, not a method change.
- **Update 4 wiring targets:** the plan's `tailor-lifecycle` section must carry handover UX (TL-001/TL-014), decision ownership/participation (TL-015, TL-M01, TL-M02), linter invocation (TL-006/TL-007), provenance/dependency policy (TL-009/TL-010), deterministic validation split (TL-007), and backtracking triggers (TL-005) — all six categories update 4 names are represented once TL-M01..M03 are added.
- **Ledger hygiene:** when adding TL-M01..M03, also remove/ignore the local "Pending audit" disposition option (contract allows only five final dispositions) and preserve all existing rows and IDs unchanged (IDs are stable; do not renumber).
- The ledger's coverage gate already demands the six completion checks in the finalize rubric; `lifecycle_tailoring.md` now lists **seven** completion checks (the contributors/specialists/approvers check was added). The write phase should reconcile the "all six" count in the ledger gate with the method doc's current seven-item list.
