# Template: Prototype Variant Presentation (C6)

Purpose: present 2–3 prototype variants to the human picker with observable facts only. Enforces Pro4 (no agent self-judging) by schema: there is no `recommendation` field. Subjective preference language in body forbidden — see [Body Rules](#body-rules).

Source: [`gr/gr_proto.md`](../gr/gr_proto.md) Pro2, Pro4, Pro7. Emitted by W14e prototype skill (A9). Consumed by human in `pro` step 5; rejected variants flow into Aln15 negative-decision capture (W14d).

Format: YAML frontmatter (machine-parseable schema) + markdown body (human-readable context). Skill owns the YAML. Human edits body only.

---

## File Naming

`prototype/<topic-slug>/variants.md` inside the sandbox directory (sandbox deleted at `pro` exit per Pro3). `topic-slug` matches the unresolved-decision restatement from `wf_proto.md` step 1.

---

## Schema

```yaml
---
decision: "<one-sentence restatement of the unresolved decision>"
flavor: fe | architecture | integration   # exactly one (Pro2)
trigger:
  irreversibility: true | false
  cost_asymmetry: true | false
  # at least one MUST be true (Pro1)
owner_issue: "<issue-id>"                  # provenance, mirrors Res4 / W14a
sandbox_path: "<dir under prototype/>"     # deleted at pro exit (Pro3)
variants:
  - id: A
    summary: "<one-line neutral description>"
    facts:
      loc_delta: <int>
      deps_added: ["<pkg@version>", ...]
      latency_ms_p50: <number | null>
      latency_ms_p99: <number | null>
      captured_responses: ["<path>", ...]   # integration flavor; Pro8
      other: ["<observable fact>", ...]     # only measured/observed values
    hidden_constraints:                      # Pro7, one entry per class
      security: covered | not_applicable | missing
      permissions: covered | not_applicable | missing
      retention: covered | not_applicable | missing
      migrations: covered | not_applicable | missing
      observability: covered | not_applicable | missing
      api_compat: covered | not_applicable | missing
      concurrency: covered | not_applicable | missing
    blocking_constraint: null | "<class>: <fact>"   # set if any class = missing
  - id: B
    # ... same shape ...
  - id: C    # optional; 2-3 variants total (Pro4)
    # ...
decision_outcome:                            # filled by human, not agent
  chosen: null                               # "A" | "B" | "C"
  rejected: []                               # ["A", "B"] — feeds Aln15
  rationale_by_human: null                   # free text; agent leaves null
---
```

Forbidden fields (schema rejects): `recommendation`, `preferred`, `best`, `agent_pick`, `score`, `ranking`. Pro4 hard-enforced.

---

## Body Rules

Body sections, in order:

1. `## Context` — restate the decision and Pro1 trigger evidence. No flavor of "I think".
2. `## Variant A`, `## Variant B`, (`## Variant C`) — one section per variant. Each contains only:
   - `### What it does` — neutral mechanism description.
   - `### Observable facts` — bulleted list mirroring `facts:` YAML.
   - `### Hidden-constraint check` — one line per class with covered / N/A / missing.
   - `### Tradeoff axes` — neutral axis labels only (e.g., "memory vs. latency", "build-time vs. runtime"). No "better" / "worse" / "cleaner" / "simpler".
3. `## Sandbox` — path, run instructions per variant, deletion command.
4. `## Decision` — empty placeholder for human; agent never fills.

Subjective vocabulary forbidden in body: better, worse, cleaner, simpler, more elegant, recommended, preferred, ideally, obviously, clearly, the right choice, the wrong choice. Reviewer (`rev`) of `pro` output flags any occurrence.

---

## Example (FE flavor, condensed)

```yaml
---
decision: "How should the variant chooser surface trade-offs to non-technical reviewers?"
flavor: fe
trigger: { irreversibility: false, cost_asymmetry: true }
owner_issue: "PROTO-142"
sandbox_path: "prototype/variant-chooser-ui/"
variants:
  - id: A
    summary: "Side-by-side columns, sortable by fact column."
    facts:
      loc_delta: 184
      deps_added: []
      latency_ms_p50: 12
      latency_ms_p99: 41
      captured_responses: []
      other: ["3 facts visible without scroll on 1280px viewport"]
    hidden_constraints:
      security: not_applicable
      permissions: not_applicable
      retention: not_applicable
      migrations: not_applicable
      observability: not_applicable
      api_compat: covered
      concurrency: not_applicable
    blocking_constraint: null
  - id: B
    summary: "Tabbed view, one variant per tab; diff toggle across tabs."
    facts:
      loc_delta: 232
      deps_added: ["@tanstack/react-tabs@1.2.0"]
      latency_ms_p50: 18
      latency_ms_p99: 55
      captured_responses: []
      other: ["1 variant visible at a time; diff toggle adds 1 extra click"]
    hidden_constraints:
      security: not_applicable
      permissions: not_applicable
      retention: not_applicable
      migrations: not_applicable
      observability: not_applicable
      api_compat: covered
      concurrency: not_applicable
    blocking_constraint: null
decision_outcome:
  chosen: null
  rejected: []
  rationale_by_human: null
---
```

Body would then carry `## Context`, `## Variant A`, `## Variant B`, `## Sandbox`, `## Decision` per [Body Rules](#body-rules).

---

## Validation Hooks (future)

- Schema lint: reject any forbidden field; require `variants.length in {2,3}`; require ≥1 trigger flag true; require all 7 hidden-constraint classes present per variant.
- Vocabulary lint: scan body for forbidden subjective terms; fail emission.
- Sandbox-retirement gate (W14a): `owner_issue` field + sandbox path tracked for deletion at `pro` exit.

Implementation deferred until skill substrate (D1) settled. Schema and rules are the contract; lints enforce mechanically once substrate exists.

---

## Notes on Interaction

- Emitted by: W14e (A9 prototype skill).
- Consumed by: human (Pro4 picker); the caller phase (Pro5 caller-persists) — `aln` reads C6 and writes Aln15 + Aln12 (intake contract: gr_algn.md Aln15 "Intake from `pro`"), `res` appends facts to `research/<topic>.md`, `prd` cites in implementation-decisions; reviewer (`rev`) verifies Pro3/Pro4/Pro7/Pro8 against this artifact. Read order: caller reads C6 **before** Pro3 deletes the sandbox.
- Retired with sandbox at `pro` exit (Pro3). The `decision_outcome` block migrates to the alignment transcript / PRD implementation-decisions section before deletion (Pro5).
