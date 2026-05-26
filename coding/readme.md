# Coding

Notes and working documents on using **AI coding agents** safely in large, production-critical brownfield systems. Focus: the guardrails, phases, and workflows that surround an agent — not the tools themselves.

## Purpose

Develop a reusable system of guardrails and a phased planning workflow that constrains AI coding agents enough to make them trustworthy in real, complex codebases — instead of relying on vibe coding.

## Key Documents

| File | Role |
|---|---|
| [ai_coding_challenges.md](ai_coding_challenges.md) | Problem motivation — risks of coding agents in brownfield systems |
| [guardrails.md](guardrails.md) | Core rules + routing index to `gr/` detail docs |
| [phases.md](phases.md) | Phase definitions (`ide → aln → res → pro → prd → iss → ral/par → qa → rev → ica`) |
| [coding_plan.md](coding_plan.md) | Operationalization tracker — skills, hooks, templates status |

## Folder Structure

```
gr/      guardrail detail docs (one per category, loaded on demand)
wf/      workflow docs (one per complex phase)
tpl/     templates (PRD, issue, variant presentation, …)
skills/  skill authoring: input/ (prompts), output/ (compiled skills)
```

## Status

Guardrail docs and phases: largely complete. Skills operationalizing the phases: in progress — see `coding_plan.md`.
