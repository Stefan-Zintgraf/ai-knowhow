# Guardrail: Review

Purpose: define how a code-review pass is conducted by an agent so that review happens in the **smart zone**, not the dumb zone, and so that coding standards are actually applied to the diff.

Scope: applies to the `rev` phase (see [phases.md](../phases.md)).

Origin: Pocock — "automated review should absolutely happen, but ideally after clearing context. If the same long implementation context reviews itself, it reviews in the dumb zone." Also: "push for reviewers, pull for implementers."

---

## Apply When

- A change has been implemented and needs review before merge.
- An AFK loop (`ral` / `par`) just produced commits.
- A human asks the agent to review a diff, branch, or PR.
- An `ica` (improve codebase architecture) pass is running over a recent change.

---

## Reviewer Model in This Repo

Review is performed by the **same agent process** running with a **fresh context** — not by a separately orchestrated agent. The fresh context is what makes it a review rather than self-justification. Future setups (e.g. Sand-Castle-style orchestration with a dedicated reviewer process) may change this; the principles below still apply.

---

## Rules

### Rev1. Review Runs in a Fresh Context

The reviewer agent must start with a context that does not contain the implementer's prior conversation, plan, or scratch reasoning. If the same session implemented the change, the context is cleared (or a new session is started) before the review begins. Reviewing inside the implementer's own context is forbidden — it produces self-justification, not review.

### Rev2. Standards Are Pushed, Not Pulled

For review, the relevant guardrail documents and coding standards are loaded into the reviewer's context up front (push), not retrieved on demand. The reviewer compares the diff against the standards, so the standards must be present. This is the inverse of the implementer rule (cross-reference: gr_operational.md push/pull rule).

### Rev3. Routing Still Applies — and Is Pushed

The reviewer performs the routing step from `guardrails.md` §5: which guardrail categories apply to this diff. Unlike the implementer, the reviewer loads the routed detail documents into context before reading the diff.

### Rev4. Review Order: Tests First, Then Code

The reviewer reads tests before reading the implementation. Tests describe intended behavior and reveal cheating (e.g. assertions that match whatever the code happens to do). Reading code first biases the reviewer toward accepting the code's implicit definition of correctness.

### Rev5. Verify Behavior, Not Just Style

The review must include a behavior check, not only a style check:

- Does the diff do what the issue / PRD / plan said it would do?
- Are edge cases from the alignment session covered?
- Do the tests actually exercise the new behavior, or do they pass trivially?
- Are all newly exported public APIs properly documented with standard, machine-readable docstrings (per `Doc12`) to guarantee successful auto-generation of API docs?

### Rev5a. API Snapshot Comparison

If the project maintains an auto-generated API overview file (e.g., `public_api.md`), the reviewer must run the generation script to produce a fresh snapshot. If the new snapshot differs from the committed one, the reviewer explicitly flags that a public API boundary has changed. Per `Gov3`, public API changes require explicit human approval. If approved, the updated snapshot must be included in the diff.

### Rev6. Check Module Depth Explicitly

The reviewer applies the module-depth dimension from [gr_mod.md](gr_mod.md), explicitly referencing the heuristics in M11:

- Did the change deepen a module, leave depth unchanged, or shallowen it?
- For new/greenfield modules: does the module expose a narrow interface relative to its internal complexity (e.g., high LOC ratio, low parameter count)?
- Were new files added that expose narrow interfaces over small internals?
- Did dependency arrows (fan-out) multiply across module boundaries?

Shallow-module drift is flagged. A diff that adds many small files with dense imports is suspect by default.

### Rev7. Check Hidden-Constraint Coverage

The reviewer explicitly checks classes of concern that grilling often misses (cross-reference: gr_algn.md):

- Security (auth, secrets, input validation, PII).
- Permissions and authorization paths.
- Data retention and migrations.
- Observability (logs, metrics, traces).
- Public API compatibility.
- Concurrency.

A "not applicable" verdict is stated, not assumed.

### Rev8. Check for Fabrication

The reviewer treats every code-level claim in the diff and its commit messages as suspect until verified: function names, imported symbols, config keys, error codes, file paths, library APIs. Op13 (no fabrication) is applied as a positive check during review, not assumed.

### Rev9. Check Scope Discipline

The diff must match the agreed scope. The reviewer flags:

- Out-of-scope changes (formatting, unrelated refactors, drive-by edits).
- Horizontal slicing (building a single layer rather than a vertical slice/tracer bullet crossing layers).
- Mixed concerns (cross-reference: Core rule 3.2).
- Silent dependency changes (cross-reference: Dep1).
- Silent abstraction additions or removals.

### Rev10. Reviewer Disagrees Visibly

If the diff appears wrong, risky, or in violation of a guardrail, the reviewer states the disagreement clearly and refuses to rubber-stamp. Reaffirmation rules from Gov12 apply — including the hard-stop exception for safety-critical, destructive, or high-risk decisions.

### Rev11. Reviewer Output Format

Review output is structured:

- **Verdict:** approve / approve-with-comments / request-changes / block.
- **Routing applied:** which guardrail categories were active for this review.
- **Findings:** grouped by guardrail category, each with diff location and rationale.
- **Behavior check:** what was verified, what was not.
- **Hidden-constraint coverage:** explicit statement per class (security, perms, retention, migrations, observability, API compat, concurrency) — "covered" / "not applicable" / "missing".
- **Module-depth assessment:** deepened / unchanged / shallowened, with rationale.

### Rev12. Use a Stronger Model When Available

Where the operating environment supports model selection, review uses a model at least as capable as the implementer's. Pocock's pattern: stronger model for review (Opus-class), faster model for implementation (Sonnet-class). The principle generalizes: review needs more reasoning headroom because it must reconstruct intent from artifacts.

### Rev13. Manual QA Is Still Required for User-Visible Behavior

Automated agent review does not replace human QA for UI, UX, or domain-judgment-sensitive changes (cross-reference: gr_algn.md — visual taste / domain judgment remain human concerns).

---

## Anti-Patterns

- Implementer agent reviews its own diff in the same session.
- Review reads code before tests.
- Review approves a diff without naming which standards were checked.
- Review without an explicit module-depth assessment.
- Review that only checks style and misses a behavior regression.
- Review that silently accepts an out-of-scope refactor.
- Review that fails to flag a horizontal slice masquerading as a feature increment.
- Review that omits the hidden-constraint checklist because "the task wasn't security-related."
- Review that uses a weaker model than the implementer.
- Review verdict without a routing statement.

---

## Notes on Interaction with Other Guardrails

- Inverts the push/pull default of `gr_operational.md`: implementer pulls, reviewer is pushed.
- Pairs with `gr_mod.md` (Rev6) — module depth is a first-class review dimension.
- Pairs with `gr_algn.md` (Rev7) — hidden constraints surfaced in grilling become a review checklist.
- Reinforces `gr_operational.md` Op13 (no fabrication) and Op14 (read before write) as positive checks during review (Rev8).
- Reinforces `gr_governance.md` Gov12 (disagree visibly) for the reviewer role (Rev10).
