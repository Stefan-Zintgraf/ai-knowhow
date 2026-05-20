# Authoring Prompt: `<skill-name>` Skill (<skill-id>)

## Metadata

```yaml
skill_id: <A##|B##|C##|none>
skill_name: <kebab-case-name>
phase: <code|none>
status: <todo|wip|done|blocked>
workflow_ref: <W##|none>
depends_on: []
feeds_into: [<A##-name>]    # name embedded, no phase tokens elsewhere
```

---

## Scope

The skill does **one** thing: <one-sentence outcome, no phase names, no downstream verbs like "hand off to X">.

The skill does **not**:

- <out-of-scope item — typically phase orchestration concerns>
- <out-of-scope item — typically downstream artifact production>
- <out-of-scope item — typically workflow routing>

<one line: who owns the out-of-scope concerns; the skill's return is just: the output + a status signal.>

---

## Self-Containment Mandate

The output skill must run **without** <list source docs> in context or on disk. Every rule the skill needs at runtime must be **inlined** into the skill file. No links to source docs. No "see X" references. The skill is a leaf artifact.

Source docs below are author-time scaffolding only — read them, distill them, embed the distilled content into the skill.

---

## Source Documents (author-time only)

| File              | Relevant sections                                                  |
| ----------------- | ------------------------------------------------------------------ |
| `gr/<file>.md`    | <only the rule IDs that survive the phase-management strip>        |
| `guardrails.md`   | <only substantive rules; strip phase-routing/collapse-mode language> |

Note: <list explicitly excluded files/sections and why — e.g. `phases.md` and §X.Y / §X.Z are phase-management concerns. Out of scope for this skill — do not embed.>

---

## Content That Must Be Embedded in the Output Skill

### Rules (inline as Hard Rules, no source references)

1. <substantive rule, imperative, no phase tokens>
2. <substantive rule>
3. <substantive rule>
4. **HITL only** — no AFK execution. Wait for explicit human acceptance.
5. <substantive rule>
6. <artifact-persistence rule if planning-artifact, else omit>

---

## Skill Behaviors

In order:

1. **Pre-structured-input check** (if applicable).
   Heuristically scan input for an already-shaped result. If it fires, ask the human via an explicit choice prompt: "Input already looks like <shape>: [list]. Treat as confirmed, or run full pass?" — never silently quote-back-and-confirm. If "treat as confirmed", skip to the HITL accept step with that input. Otherwise proceed. If heuristic does not fire, proceed silently.

2. **<core work step>.**
   <one paragraph; mechanics for detail-handling, leak-strip, etc. live here rather than in Rules>

3. **Detail-leak strip** (if applicable).
   Remove forbidden detail per Rules. Append a one-line note per stripped item using the exact format: `Stripped detail: <item>` (one per item, no phase names — never "deferred to <phase>" or "deferred to <phase>/<phase>").

4. **<additional core step>.**
   <…>

5. **Count gate / sizing gate** (if applicable).
   On under-budget: return `status: not_produced` with `reason: <short>`. **Forbidden phrases in the failure string**: any phase token, `proceed to <phase>`, `deferred to <phase>`, `next phase`. On over-budget: prompt the human to merge/drop before proceeding.

6. **HITL accept.**
   Present the draft to the human for edit / accept / reject. Do not finalize until the human explicitly accepts. Forbidden: auto-accepting, treating acknowledgement as acceptance.

7. **Artifact write** (if planning-artifact).
   Derive a candidate `<WI>` slug from the input (short, snake_case — e.g. `ai_mail`, `fix_crash_abc`). Prompt the human: "Work-item slug? Suggested: `<slug>`." Accept confirm or override. Then prompt: "Owner issue (e.g. `#123`)?" — required; the WI anchor for 3.33 retirement. If the human has no issue number yet, accept a placeholder `#TBD` and explicitly warn that Q11 merge-gate retirement enforcement will fail until replaced. Create `plan/<WI>/` if missing. Write the confirmed output to `plan/<WI>/<artifact>.md`.

8. **Status file write** (if planning-artifact).
   Write/update `plan/<WI>/status_<artifact>.md` with frontmatter:
   ```
   ---
   status: open|wip|done
   updated: <today YYYY-MM-DD>
   owner-issue: #NNN   # mandatory on the anchor artifact; siblings inherit
   ---
   ```
   Rules: (a) refresh `updated:` to today on every run; (b) default `status: wip` after a successful artifact write; (c) ask the human "mark done?" at end of run UNLESS the run is a clear-incomplete (under-budget, human rejected, no acceptance) — in those cases skip the prompt; flip to `done` only on explicit human yes, never auto-flip; (d) preserve existing `done` unless the human explicitly reopens — on reopen, flip `done → wip` (never back to `open`). On failure runs (no artifact written), do NOT create or modify the status file.

9. **Return.**
   Emit:
   - <primary output>
   - <path written, if planning-artifact>
   - A success signal: `status: ok` plus one-line summary.
   On failure (under-budget, human rejected, no acceptance reached), emit `status: not_produced` plus the reason. No phase names. No "next step" / "proceed to" / "deferred to" language anywhere in the failure string.

---

## Constraints (must appear as Hard Rules inside the skill)

- **<constraint>**: <short imperative>.
- **<constraint>**: <short imperative>.
- **HITL only**: explicit human acceptance required.
- **owner-issue mandatory** (if planning-artifact): `status_<artifact>.md` frontmatter MUST carry `owner-issue:`. Prompt the human at write-time; accept `#TBD` only with an explicit warning that merge-gate retirement enforcement will fail until replaced.
- **No phase orchestration**: the skill does not name, invoke, or hand off to other phases or skills. Output is the <primary output> and a status signal — nothing more.

---

## Output Format (for the generated skill)

The output skill (`skills/output/<skill-name>.md`) must be a Claude Code SKILL.md — a single self-contained markdown prompt file that:

- Opens with a one-paragraph role statement: this skill <does one thing> and returns it. It does not manage workflow phases.
- Contains an inlined **Hard Rules** block (the rules above plus the Constraints, brief imperative form). No "see <doc> §X" references.
- Has an ordered **Steps** section mapping to the behaviors above (one sentence per step; expand only where ambiguity would cause wrong behavior).
- For planning-artifact skills: includes the artifact path, the status file path, the full frontmatter spec (`status` + `updated` + `owner-issue` on the anchor), and the state-machine rules inlined verbatim.
- Has a **Return** section specifying the success/failure signal shape.
- Does **not** link to <source docs>. Does **not** mention any phase token anywhere in the body outside its `Metadata.phase` field: `aln`, `prd`, `iss`, `res`, `pro`, `qa`, `rev`, `ica`, `ral`, `par`, `ide`. This applies to Rules, Steps, Return, prose, examples, anti-pattern bullets, and failure messages.
- Does **not** contain forbidden phrasings: `proceed to <phase>`, `deferred to <phase>`, `hand off to <phase>`, `feeds into <phase>`, `next phase`. Use `status: not_produced` + `reason:` for failure outcomes; use `Stripped detail: <item>` (per item) for leak notes.
- Passes the test: if the skill file were the only file in the repo, an agent reading it could still execute correctly.
