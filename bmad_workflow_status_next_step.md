# BMAD Brainstorming — Status + Next Step (Resume Later)

## Current artifact

- **Session file**: `tutorial1/_bmad-output/analysis/brainstorming-session-2025-01-18.md`
- **Session topic**: Build a **BMAD step-by-step tutorial** (methodology-focused, not domain-specific) using **CRA vulnerability handling** as the first practice project; also support a second use case: **code/documentation analysis → hierarchical MD outputs for AI agent integration**.
- **Approach selected**: **AI-recommended progressive flow**
- **Techniques queued**:
  - Phase 1: **Cross-Pollination**
  - Phase 2: **Morphological Analysis**
  - Phase 3: **Decision Tree Mapping**
  - Phase 4: **Solution Matrix**
- **Status**: paused **immediately after technique selection**; no ideation has been captured yet.

## Related references (from `agents.md` section 5.1)

- **Brainstorming feature overview**: `../BMAD-METHOD/docs/explanation/features/brainstorming-techniques.md`
- **Practical how-to (workflow)**: `../BMAD-METHOD/docs/how-to/workflows/run-brainstorming-session.md`

## What’s missing (why this session isn’t “done” yet)

The session file currently contains setup + technique choice only. Per the Brainstorming feature expectations, a complete artifact should also include:

- **Ideas generated** (your contributions during each technique)
- **How each technique was applied** (prompts + responses + synthesized output)
- **Organization** (themes/clusters + prioritization)
- **Action planning** (next steps, resources, success metrics)

## Important nuance (workflow shape mismatch to be aware of)

The how-to doc `run-brainstorming-session.md` describes the `*brainstorm-project` workflow, which produces **parallel “tracks”** (Architecture/UX/Integration/Value).

Your existing session file is structured as a **progressive technique journey** (Cross-Pollination → Morphological → Decision Tree → Solution Matrix).

Both are valid brainstorming modes, but when resuming you should choose **one** of these and stick with it for coherence:

- **Option A (recommended for continuity)**: Continue the existing **progressive flow** and keep outputs in the same session document style.
- **Option B**: Re-run as `*brainstorm-project` (track-based), then optionally map the best results into the progressive flow phases afterward.

## Next step plan (to continue the progressive flow)

### Phase 1 — Cross-Pollination (goal: 30+ tutorial structure ideas)

Generate at least 30 distinct tutorial-structure concepts by borrowing patterns from other domains (examples):

- incident-response playbooks, flight training checklists, university syllabi, cooking recipes, martial arts belts, apprenticeship programs, choose-your-own-adventure branching, lab manuals

**Constraints to enforce while generating**:

- Must cover **two entry paths**:
  - research-heavy projects: internet + local docs → documents
  - code/doc analysis projects: source + docs → hierarchical MD files for AI agent integration
- Must include an **Introduction section** design (purpose, scope, learning objectives)
- Must include hands-on practice case #1: **CRA vulnerability handling**
- Must include practice case #2: **software library analysis**

### Phase 2 — Morphological Analysis (goal: pick best combinations)

Build a morphology grid with dimensions like:

- learner level, pacing/timebox, artifact outputs, checkpoints, “research vs repo” entrypoint, evaluation rubric, required tools, agent roles/workflows invoked

Select the strongest combinations and explain why.

### Phase 3 — Decision Tree Mapping (goal: reusable learning path)

Turn the chosen structure into a decision tree:

- “If I have a repo…” vs “If I only have docs/internet…”
- “If I’m a beginner…” vs “If I’m experienced…”
- “If it’s security/vuln work…” vs “If it’s library analysis…”

### Phase 4 — Solution Matrix (goal: implementable plan)

Map tutorial components → deliverables:

- file tree (where MD outputs go), templates, success metrics, and concrete “next actions” to produce the tutorial.

## Resume script (paste into a brand-new AI session)

Copy/paste this whole block into a new chat:

---
You are facilitating a BMAD brainstorming session to design a methodology-focused BMAD tutorial (not domain-specific).

We already completed session setup and selected the **AI-recommended progressive flow**:
- Phase 1: Cross-Pollination
- Phase 2: Morphological Analysis
- Phase 3: Decision Tree Mapping
- Phase 4: Solution Matrix

Context:
- Practice project #1: CRA vulnerability handling (research-heavy: internet + local docs → documents)
- Practice project #2: software library analysis (code/doc analysis: source + docs → hierarchical MD files for AI agent integration)
- Tutorial must include an Introduction section (purpose, scope, learning objectives)

Task:
Resume at **Phase 1 (Cross-Pollination)** and produce **30+ distinct tutorial structure ideas**, ensuring each idea explicitly supports both entry paths (research + repo/code) and preserves the two practice projects. After Phase 1, ask me which 5–7 ideas to take into Phase 2.

Output format:
- Numbered list for Phase 1 ideas
- Each idea: 1–2 sentence description + named pattern inspiration + “how it handles research path” + “how it handles repo/code path”
---

## Where to store the continuation output

When you resume, append outputs to:

- `tutorial1/_bmad-output/analysis/brainstorming-session-2025-01-18.md`

Tip: keep each phase output under its own heading so the file remains navigable.

