# Coding

This folder collects notes and working documents on how to use **AI coding agents** safely and effectively — especially in large, production-critical brownfield systems.

The focus is not on coding tools themselves, but on the **guardrails, rules, and workflows** that should surround an AI agent when it plans or implements changes, so that quality, architecture, and domain invariants are preserved.

## Contents

- **[ai_coding_challenges.md](ai_coding_challenges.md)** — Risks and problem classes of using coding agents in large brownfield systems (context barrier, implicit business logic, technical-debt amplification, scaling issues, etc.). The starting point that motivates the rest.
- **[ChatGPT-AI Coding Guardrails.md](ChatGPT-AI%20Coding%20Guardrails.md)** — Exported Socratic discussion that explores which categories of guardrails are needed (product/domain, architecture, DDD, change-planning, coding style, testing, review, …). Source material / brainstorming.
- **[guardrails.md](guardrails.md)** — Compact guardrail **overview**: core rule set plus a routing index that points to detailed guardrail documents in the [`gr/`](gr/) folder. The agent loads only the detail docs relevant to the current task.
- **[phases.md](phases.md)** — Named workflow phases (aln, prd, iss, ral, par, rev, ica) used by `guardrails.md` and `AI_Coding_Workflow.md`. Each phase is backed by a skill or template. Includes the phase → guardrail bucket mapping.
- **[AI_Coding_Workflow.md](AI_Coding_Workflow.md)** — First draft of the **workflow** that leads from an initial request to a minimal, safe, shared plan before any implementation starts — intended to prevent premature coding and uncontrolled scope.

## Purpose in one sentence

Develop a reusable set of guardrails and a planning workflow that constrains AI coding agents enough to make them trustworthy in real, complex codebases — instead of relying on "vibe coding".
