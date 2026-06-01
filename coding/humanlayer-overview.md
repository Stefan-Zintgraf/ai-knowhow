# HumanLayer GitHub — Resources for AI-Assisted Coding

> Research summary: https://github.com/humanlayer
> Focus: Workflows, skillsets, commands, and agents useful for greenfield and brownfield AI coding projects

---

## Key Repositories at a Glance

| Repository | Stars | What it is |
|---|---|---|
| `humanlayer/humanlayer` | ⭐ 10.8k | Main repo — Claude Code commands, agents, RPI framework |
| `humanlayer/12-factor-agents` | ⭐ 18.6k | Principles for production-grade LLM applications |
| `humanlayer/advanced-context-engineering-for-coding-agents` | ⭐ 1.7k | ACE-FCA methodology document (brownfield focus) |
| `humanlayer/agentcontrolplane` | ⭐ 348 | Distributed agent scheduler with MCP support |

---

## The Core: `humanlayer/humanlayer`

**Tagline:** "The best way to get AI coding agents to solve hard problems in complex codebases."

This repo contains a battle-tested `.claude/` directory that you can drop directly into your project. It implements the **Research-Plan-Implement (RPI) workflow** with **Frequent Intentional Compaction (FIC)** as the underlying technique.

### What is Frequent Intentional Compaction (FIC)?

The core idea: design your entire development workflow around context management, keeping context window utilization in the **40–60% range**. Instead of letting the context fill up with grep results, file reads, and build logs, you deliberately distill progress into structured markdown artifacts before moving to the next phase.

---

## Slash Commands (`.claude/commands/`)

These are invoked with `/command_name` inside Claude Code.

### `/research_codebase`
Spawns parallel sub-agents to comprehensively map a codebase. The agents act as **documentarians, not critics** — they describe what exists, where it lives, and how it works, without suggesting changes or identifying problems.

Typical output: a structured research document in `thoughts/shared/research/` covering:
- Relevant files and their locations
- How data flows between components
- Architectural patterns in use
- Potential root causes (only when asked)

### `/create_plan`
Before writing any code, spawns research agents in parallel to understand the codebase, then proposes a phased implementation plan. Produces a markdown plan file in `thoughts/shared/plans/` covering:
- Implementation phases with precise verification steps
- Files to edit and how
- Edge cases and performance considerations
- Open design questions requiring human input

Variants: `/create_plan_nt` (no-thoughts variant, for repos without a `thoughts/` directory)

### `/implement_plan <path-to-plan.md>`
Executes the plan phase by phase. Key behavior:
- Updates checkboxes in the plan file as work progresses
- Pauses after each phase for **human verification** before continuing
- Communicates clearly when actual codebase state diverges from the plan
- If multiple phases are approved in advance, skips intermediate pauses

### `/iterate_plan <path-to-plan.md>`
Updates an existing plan based on feedback. Skeptical and grounded — re-researches the codebase before confirming changes.

### `/validate_plan`
Checks whether the implementation matches the plan. Runs automated checks and lists any manual verification steps needed.

### `/commit`
Generates a structured commit message based on what was implemented.

### `/describe_pr`
Generates a pull request description from the plan and implementation.

### `/create_handoff` / `/resume_handoff <path>`
Saves the current session state to a handoff document, so work can be resumed in a fresh context window without losing progress.

---

## Specialized Sub-Agents (`.claude/agents/`)

These are called by commands (or directly) to handle specific research tasks in isolated context windows — keeping the main agent's context clean.

### `codebase-locator`
**Role:** File finder and mapper.

Specializes in finding *where* code lives. Uses grep, glob, and directory traversal to locate all files relevant to a feature or topic. Returns an organized map — not analysis. Does not suggest improvements.

Language-aware: knows to look in `src/`, `components/`, `pages/` for TypeScript; `src/`, `lib/`, `pkg/` for Python; etc.

### `codebase-analyzer`
**Role:** Implementation detail specialist.

Analyzes *how* code works: traces data flow, explains technical workings, provides exact `file:line` references. Strictly descriptive — never suggests refactoring or identifies "problems" unless explicitly asked.

### `codebase-pattern-finder`
**Role:** Pattern discovery.

Finds examples of how existing features or patterns are implemented elsewhere in the codebase. Used by `/create_plan` to ensure new code follows established conventions.

### `thoughts-locator`
**Role:** Document finder in `thoughts/`.

The `codebase-locator` equivalent for the `thoughts/` directory (where specs, research notes, tickets, and plans live). Finds relevant prior decisions or documents for a given topic.

### `thoughts-analyzer`
**Role:** Insight extractor.

Deep-dives into specific thought documents and returns only the most relevant, actionable insights — filtering out noise and surfacing key decisions with their rationale and current relevance.

### `web-search-researcher`
**Role:** External research.

Performs web searches for modern patterns, library documentation, or external context. Returns links alongside findings so they can be included in the research report.

---

## The Full Workflow in Practice

```
1. /research_codebase  →  research doc saved to thoughts/shared/research/
2. /create_plan        →  plan doc saved to thoughts/shared/plans/
3. Review & approve plan (human step)
4. /implement_plan thoughts/shared/plans/YYYY-MM-DD-feature.md
   → Phase 1 → automated checks → PAUSE for human verification
   → Phase 2 → automated checks → PAUSE for human verification
   → ...
5. /validate_plan
6. /commit
7. /describe_pr
```

For long or interrupted work:
```
/create_handoff   →  save progress
(new session)
/resume_handoff thoughts/shared/handoffs/latest-handoff.md
```

---

## Why This Matters for Brownfield Projects

The ACE-FCA methodology explicitly addresses the brownfield problem. Stanford research found that AI tools are often **counter-productive in large, established codebases** — more rework, more "slop", harder to maintain quality.

The HumanLayer approach counters this by:

1. **Never starting from scratch each session** — research and plan docs persist across sessions
2. **Keeping the main context clean** — sub-agents handle exploration so the main agent starts with a precise, curated summary
3. **Spec-driven development** — the plan is the source of truth; AI writes to a spec, not to vibes
4. **Structured human checkpoints** — mandatory verification after each phase, not just at the end
5. **Context utilization discipline** — compacting state into markdown instead of letting the window flood

Validated on a 300k LOC Rust codebase (BAML) by someone who had never worked in it before.

---

## For Greenfield Projects

The same workflow applies, but the research phase is lighter (less existing code to understand). The value is primarily in:
- Spec-first development from day one
- Consistent plan → implement → verify cycle
- No "context drift" as the project grows

---

## Community Forks Worth Knowing

### `jeffh/claude-plugins`
A plugin marketplace for Claude Code. Install with `/plugin install humanlayer@jeffh-claude-plugins` inside Claude Code. Packages all 6 HumanLayer commands and 6 agents, plus Jujutsu (jj) VCS workflows.

### `acampb/claude-rpi-framework`
A cleaned-up, standalone RPI setup with a download script. Good starting point if you want the commands without the full HumanLayer repo structure.

### `visualitypl/visuality-humanlayer`
Adaptation for a specific team's workflow — useful as a reference for how to customize the base commands.

---

## Quick Start

```bash
# Option 1: Copy directly from humanlayer/humanlayer
git clone https://github.com/humanlayer/humanlayer /tmp/humanlayer
cp -r /tmp/humanlayer/.claude/commands/ /path/to/your-project/.claude/commands/
cp -r /tmp/humanlayer/.claude/agents/  /path/to/your-project/.claude/agents/

# Option 2: Via jeffh/claude-plugins (inside Claude Code)
/plugin install humanlayer@jeffh-claude-plugins
```

Then create the thoughts directory structure:
```
thoughts/
  shared/
    research/
    plans/
    handoffs/
```

And start with:
```
/research_codebase
> How does [feature X] work? What files are involved?
```

---

## Key Links

- Main repo: https://github.com/humanlayer/humanlayer
- ACE-FCA blog post: https://www.humanlayer.dev/blog/advanced-context-engineering
- 12-factor agents: https://github.com/humanlayer/12-factor-agents
- YC talk (video): https://hlyr.dev/ace
- Plugin marketplace: https://github.com/jeffh/claude-plugins
- RPI framework (standalone): https://github.com/acampb/claude-rpi-framework
