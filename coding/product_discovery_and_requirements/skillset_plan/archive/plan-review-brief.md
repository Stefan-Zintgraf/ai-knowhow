# Plan review brief — product-loop skillset

> **CLOSED — all seven findings resolved and applied. Archived; not an input to authoring.**
>
> This brief is kept as the record of what was decided and why. **Three of its findings rest on source attributions that proved wrong** — read the dispositions below before trusting any claim in the body. Everything it asked for has been applied to the plan and the method docs; the verification greps under *Working notes* are inverted by design and no longer describe the current state.
>
> | ID | Disposition |
> | --- | --- |
> | `REV-01` | **Resolved — premise corrected.** O/E/H is not "donor-derived or invented": it is `RafaelGorski/Problem-Based-SRS` (MIT, `pattern`/adapt), accepted as `DR-EXT-06`/`SR-EXT-04`. Defined as method in [product_definition.md](../../product_definition.md), added to [glossary.md](../../glossary.md), grounded in [resources.md](../../resources.md). |
> | `REV-02` | **Resolved — attribution wrong, and a real bug found.** `Rich` never appeared in `resources.md`; the rubric is `jacksoncalling/argo-continuous-discovery` (`DP-008`, unverified license → `pattern`-only, so its wording *must not* be copied). The written entry also graded source quality and sample representativeness with one label, making **Rich unreachable**. Axes split; re-grounded to Fitzpatrick and Bland & Osterwalder; defined as method in [product_discovery.md](../../product_discovery.md). |
> | `REV-03` | **Resolved — reframed.** The lens was not merely unspecified, it was routed against [quality_attributes.md](../../quality_attributes.md):5, which places architecture-changing qualities at *discovery*. The plan's own §5.4 already agreed. Lens deleted; `QAS#` seeded from the foundation vision plus discovery's feasibility `ASM#`/`EV#`. |
> | `REV-04` | **Resolved — differently.** Renaming "companion" → "vision spine" was rejected: method docs name zero skillset artifacts, and "vision spine" is plan-only vocabulary. The clause was de-skilled instead, keeping the `DEC#` and accountable-owner obligations. Update-10 stripped. |
> | `REV-05` | **Resolved — not accepted.** §3.3 does *not* carry provenance independently; its table is keyed to the `distill` surface only. The coverage axis was re-founded on the per-skill source/dependency manifests (§3.2's own "realizing record"). Five axes restored. |
> | `REV-06` | **Resolved per entry.** *Instrumentation* ratified unchanged. *Solution direction* corrected — it contradicted `LNT-07`'s own `DEC#` exception. *Analysis plan* is not from `validation_and_feedback.md`; it is `florianbonnet14/ThePowerOfAnalytics_ClaudeSkills` (`VR-EXT-03`, no stated license), now given a method home and grounded to Kohavi/Tang/Xu. |
> | `REV-07` | **Resolved — kept and reconciled.** [github_skillsets.md](../github_skillsets.md) stays: it is the only live record behind §3.2's license hard rules and the `pattern`-mode donors §3.3 omits. Its retired vocabulary and two dangling links were reconciled. |
>
> **The lesson worth carrying forward:** `REV-01`, `REV-02`, and `REV-06`'s *Analysis plan* were one defect wearing three masks — a linter check (`LNT-15`/`LNT-16`, `LNT-06`/`LNT-18`, `LNT-17`) resting on vocabulary that lived only in the plan. All three took the same fix: define in the owning method doc, add to the glossary, ground in the reference map. Every corrected attribution was recoverable from this archive — the brief was written without reading it.

Seven findings the plan cannot answer for itself.

The discovery–definition–requirements skillset plan was renamed, de-referenced, and stripped of history. That pass surfaced problems it had no authority to fix. Each finding below names what is wrong, where, and the decision it waits on.

**Scope:** [prod_discovery_requirements_skillset_plan.md](../prod_discovery_requirements_skillset_plan.md) · [../glossary.md](../../glossary.md)

Findings carry stable IDs so a review pass can report against them (`REV-03 resolved`), mirroring the plan's own `LNT-xx` / `RTS-xx` discipline. Severity is the reviewer's claim, not the plan's:

- **Blocking** — a linter check rests on undefined vocabulary.
- **Gap** — something is referenced but unspecified.
- **Ratify** — a judgment call was made on the author's behalf and needs confirming.

---

## Baseline — what the plan now is

Read this first: it is the state the findings assume. Nothing below is a request to undo it.

| | |
| --- | --- |
| **Skills** | Seven, all new: `tailor-lifecycle`, `establish-vision`, `derive-vision-spine`, `discover-product`, `define-release`, `specify-requirements`, `validate-release` — one `product-loop` plugin. |
| **Retired vocabulary** | Zero occurrences. No `brainstorm-vision`, `create-vision-companion`, "companion", "bundle", `*-vision-ai-spec/`, or `docs/brainstorming/`. The spine artifact is `<product>-vision-spine/`; its judgment rows are `SRV#`. |
| **Backward compatibility** | None, by decision. The skills assume no pre-existing workspace. Every migration clause, legacy resume scan, and the `glossary.md` → `domain-glossary.md` rename are gone; the file is simply born `domain-glossary.md`. |
| **Regression scoring** | Four axes, was five: completion checks · linter · handover · re-entry. The ledger-coverage axis went with the ledgers — see REV-05. |

---

## Findings

### REV-01 — Blocking

**The plan enforces a classification no method doc defines.**

*Location:* §2.2 LNT-15 · §2.2 LNT-16 · §5.5

LNT-15 fails any mandatory scope item lacking an **Obligation / Expectation / Hope** classification, and LNT-16 consumes that classification downstream in `specify-requirements`. But the words *Expectation* and *Hope* appear in **no method document in the collection**. *Obligation* appears only in `collaboration_and_decision_ownership.md` and `lifecycle_tailoring.md`, in the unrelated contractual sense. The scheme is either donor-derived or invented, and design principle 6 says the method docs are the source material.

> **Decide:** define O/E/H in `product_definition.md` and add it to the glossary — or record it as a distilled donor contribution with provenance under §3.2 — or drop the classification and rewrite LNT-15/LNT-16. Do not leave a linter check enforcing undefined vocabulary.

### REV-02 — Blocking

**"The canonical Rich/Mixed/Thin rubric" was not canonical anywhere.**

*Location:* §2 artifacts · §2.2 LNT-06, LNT-18 · `../glossary.md` (Evidence strength)

The plan calls evidence strength *canonical* and builds two linter checks on it: LNT-06 requires a strength on every `EV#` row, LNT-18 caps confidence by it. Yet *Mixed* appears in no method doc, and *Rich* only in `resources.md`, citing Bland & Osterwalder's evidence-strength grading. The rubric was load-bearing and undefined.

A definition now exists in the glossary — **but I wrote it.** The three grade boundaries (real actor under real stakes / partial or proxy / opinion or hypothetical) are my synthesis, not the collection's and not Osterwalder's.

> **Decide:** ratify, correct, or replace those grade boundaries against the cited source before any skill is authored against them. Everything LNT-18 caps depends on where the lines fall.

### REV-03 — Gap

**The architecture-lens file is written, read, and never specified.**

*Location:* §2 artifact table · §5.1 "Does" · §5.6 "Does"

`establish-vision` writes `<product>-foundation-vision-architecture-lens.md`, and `specify-requirements` seeds `quality-scenarios.md` from it — the §2 artifact table says so in the `QAS#` row. But the lens has **no row of its own**: no method doc mapped to it, no ID family, no shape, no linter scope, no place in the §2.1 coverage table. An artifact that seeds architecture-significant quality scenarios is not a detail.

> **Decide:** give it a §2 row with its method doc and ID family, or fold its content into the foundation vision and delete the separate file. The references are wired; the spec was not invented.

### REV-04 — Gap

**Retired vocabulary and revision history survive in the method docs.**

*Location:* `../product_discovery.md` · `../product_vision.md` · `../resources.md`

The plan is clean; the collection is not. Three method docs still say *"the companion"*, naming a skill that no longer exists in any plan. `resources.md` is worse: it carries an **"Update-10 reference-map synchronization"** section — the exact revision-history framing just stripped from the plan — and inside it, the sentence "derived/indexed but never owned by the companion".

§3.3's post-authoring reconciliation clause covers method-doc drift in principle, but it fires *after* authoring. This naming is wrong now, and the docs are the skills' source material.

> **Decide:** reconcile the three docs to `derive-vision-spine` / "vision spine" now rather than at reconciliation time, and strip the Update-10 section from `resources.md` under the same rule applied to the plan.

### REV-05 — Ratify

**Acceptance lost its contribution-coverage gate.**

*Location:* §6 scoring axes · `archive/analysis/`

§6 scored every reference-topic run on five axes. Axis 2 — *ledger coverage gates* — checked that a run exhibited the realizing mechanisms of the accepted rows in the seven contribution ledgers. Those ledgers are acceptance history and are now archived, so the axis went with them and scoring is four axes. Two stale cross-references (§4.1, §4.2) were renumbered to match.

The consequence is real: nothing now verifies that an authored skill actually *implements* the contributions the plan accepted. The per-row dispositions still exist in `archive/analysis/distill-provenance.md` and the archived ledgers.

> **Decide:** accept four axes as sufficient — the §3.3 donor audits carry provenance independently — or re-found a coverage gate on something that is not archived history.

### REV-06 — Ratify

**Four glossary entries are mine, not the collection's.**

*Location:* `../glossary.md` — Analysis plan, Evidence strength, Instrumentation, Solution direction

The glossary defines *method* terms, so only terms the method docs use but never defined were added: **Analysis plan** (from `validation_and_feedback.md`), **Evidence strength** (see REV-02), **Instrumentation** (from `validation_and_feedback.md`'s "instrumentation is a requirement, not an afterthought"), and **Solution direction** (from `product_discovery.md`). Each closes a gap the plan's linter or gates depend on. The wording is mine.

> **Decide:** read all four for terminological fit before they harden into skill prompts. *Solution direction* in particular asserts that a single direction on the table means alternatives were never explored — that is LNT-07's premise stated as method.

### REV-07 — Ratify

**One survivor of the archive sweep is arguably history too.**

*Location:* `skillset_plan/` · `github_skillsets.md`

`authoring-evidence.md`, the seven `*-contributions.md` ledgers, `skillset_plan_update_plan.md`, and the whole `analysis/` tree moved to `archive/` — all of it acceptance evidence, and two ledgers were named after the retired skills. `github_skillsets.md` stayed, but the old README described it as material to "open only when the reasoning behind a contribution is needed", which is the definition of what was removed everywhere else.

It was kept because it is the donor survey standing behind §3.3's audit table, and discarding the record of which sources were considered and rejected is harder to reverse than keeping it.

> **Decide:** keep it as donor reference, or archive it for consistency with the no-history rule. `README.md` was rewritten either way and no longer points at archived files.

---

## Working notes

### What a review pass should check first

- **REV-01 and REV-02 gate authoring.** Both are linter checks resting on undefined vocabulary. A skill authored against either will encode the guess.
- **The spine rename touched three ID surfaces.** `BRV#` → `SRV#` in LNT-01's family list, LNT-02's reservation rule, and §5.2. Verify nothing outside the plan referenced `BRV`.
- **First-party reuse is now out of scope of §3.2.** A sentence was added stating that patterns carried from other skills in the collection need no license, commit, or attribution record — only a note of what was carried. Without it the ledgers imply your own phase structure came from a stranger's repository.
- **§3.3 is self-contained.** The donor table is keyed by repository and path rather than by ledger row ID, so the audits survive the archive.

### Verify the state for yourself

```bash
cd c:/PROJ/ai-knowhow/coding/product_discovery_and_requirements

# retired vocabulary in the plan — expect no matches
grep -ni "companion\|bundle\|brainstorm-vision\|BRV#\|vision-ai-spec" \
  skillset_plan/prod_discovery_requirements_skillset_plan.md

# REV-01 — expect no matches at all
grep -rl "Expectation\|Hope" --include=*.md . | grep -v skillset_plan

# REV-04 — expect three method docs
grep -rli "companion" --include=*.md . | grep -v skillset_plan
```
