# Goals

1. Define end-to-end coding workflow covering both greenfield and brownfield work.
2. Establish guardrails that protect system intent without bloating always-on agent context.
3. Operationalize the workflow and guardrails as enforceable agent behavior (skills, hooks, templates), not prose-only docs.
4. Keep planning effort proportionate — workflow must reach real code quickly, not stall in exhaustive upstream planning.
5. Provide shortcuts for small coding tasks so the full pipeline collapses appropriately rather than being skipped silently.

# Starting Point

Origin: distilled from Matt Pocock YouTube videos; current folder content built on that distillation.

Anchor documents:
- [todo.md](../../todo.md) — current list of work items (skills, hooks, templates, open decisions).
- [guardrails.md](../../guardrails.md) — core rules + routing index to detail docs under [gr/](../../gr/).
- [phases.md](../../phases.md) — phase definitions referenced by guardrails' `Fires:` lines.

Stripped detail (not part of goals; kept here for traceability):
- Stripped detail: phase names (ide/aln/res/pro/prd/iss/ral/par/qa/rev/ica).
- Stripped detail: specific skill slots (A1–A11, B1–B10, C1–C8).
- Stripped detail: substrate decisions (skill format D1, sandbox D4).

# Design contracts settled 2026-05-22

A /grill-with-docs session on 2026-05-22 settled 12 design contracts (C1–C12) covering entry-triage, three workflow modes (`direct-edit` / `mini` / `full`), a 4-axis triage matrix, the issue-creation invariant, mode-dependent ceremony scaling, and mode-transition rules. These contracts are **distributed across the topical detail docs** (per the routing model — each rule lives in its topical home so the routing index in `guardrails.md` §5 surfaces it correctly):

- **Mode selection, triage matrix, issue invariant, exploration budget, mode transitions** — [`gr/gr_idea.md`](../../gr/gr_idea.md) Idea8, Idea9, Idea10, Idea11.
- **`plan/<N>_<slug>/` mode-dependent persistence + WI naming** — [`gr/gr_idea.md`](../../gr/gr_idea.md) Idea7 (revised).
- **TDD exemption for `direct-edit` (existing-tests carve-out + behavior-free carve-out)** — [`gr/gr_tdd.md`](../../gr/gr_tdd.md) TDD11; cross-ref in [`guardrails.md`](../../guardrails.md) §3.22.
- **Collapsed `aln` spec for `mini` mode** — [`gr/gr_algn.md`](../../gr/gr_algn.md) Aln19.
- **Mode-dependent `qa` shape** — [`gr/gr_qa.md`](../../gr/gr_qa.md) Q12.
- **Tripwire mid-task halt + mode re-triage** — new core rule [`guardrails.md`](../../guardrails.md) §3.37; parallel-table row in §9.
- **`guardrails.md` §3.29 rewritten** to point at `ide`-owned mode selection.

The pre-migration capture (the "Settled Contracts (2026-05-22)" section that briefly lived in this file) is preserved in `git log` around 2026-05-22 for traceability.

# Regeneration

See [`idea_recreation.md`](idea_recreation.md) for the step-by-step recipe (skill chain + concrete prompts + anchor-doc list) that regenerates this file.
