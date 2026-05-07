---
name: lateral
description: "Inject random creative perspectives into any question by launching parallel agents, each given a random dictionary word as a lens. Use when exploring a topic from unexpected angles, breaking out of linear thinking, debating ideas, or when /research or /strategy would benefit from creative reframing. Triggers on 'lateral', 'random angles', 'fresh perspectives', 'creative reframe', 'break it open'."
argument-hint: "[topic or question to explore]"
allowed-tools: Bash(python3 *)
---

# Lateral Thinking via Random Injection

Launch N parallel agents, each given a random dictionary word as a creative lens on a question. The randomness forces unexpected connections that linear thinking misses.

## Process

### Step 1: Sample Random Words

Default 10 agents. User can specify a different count (e.g. `/lateral 5 [topic]`).

```bash
python3 scripts/sample-words.py 10
```

The script auto-downloads the dictionary on first run if missing. If words are obscure, that's fine — obscurity forces more creative interpretation. Don't re-roll for "better" words. The randomness is the point.

### Step 2: Launch Parallel Agents

Launch ALL agents in a single message (one Agent tool call per word). Use `model: sonnet` for speed and cost.

Each agent gets this prompt template (fill in the topic and word):

```
You are contributing one perspective to a multi-agent creative synthesis.

**Topic**: {the user's question or topic}

**Your assigned random word is: {WORD}**

Use this word as a creative lens, metaphor, or unexpected connection point to generate a fresh insight about the topic. Interpret the word however produces the most interesting thought — literally, metaphorically, historically, scientifically, etymologically.

Rules:
- Respond in exactly 2-3 tight paragraphs
- Take a clear position — don't hedge
- Be original — the value is in unexpected connections
- Don't explain the exercise or meta-comment on the process
```

If the word is obscure, add a brief definition in the prompt so the agent has something to work with.

### Step 3: Synthesise

Once all agents return, pull the results together:

1. **Read all responses** and identify the 3-5 strongest threads that emerged across multiple agents
2. **Name each thread** with a short heading
3. **For each thread**, synthesise the best insights from the contributing agents into 1-2 paragraphs
4. **Note surprising connections** — where did two random words converge on the same insight from different angles?
5. **State the consensus position** if one emerged, or the key tension if the agents split

Format as a tight synthesis, not a list of agent outputs. The user doesn't need to see 10 separate essays — they need the distilled insight.

### Step 4: Offer Next Steps

- **Capture**: Offer to save as a concept note if the synthesis produced genuinely new thinking
- **Deepen**: Suggest running `/research` on the strongest thread
- **Rerun**: Offer to run again with fresh words if the first batch was flat

## Configuration

- **Default agents**: 10
- **Model**: sonnet (fast, cheap, good enough for creative riffing)
- **Dictionary**: `words.txt` (370k English words, bundled with skill)
- **Word filter**: 4-9 characters, alphabetic only

## Integration

This skill is used by:
- **`/research`**: As an optional creative reframe step after vault search
- **`/strategy`**: During stress-testing to surface unexpected failure modes or reframe the diagnosis
- **`/business-idea`**: Before scoring, to expose assumptions about the problem

Other skills can invoke `/lateral` whenever a question would benefit from breaking out of the obvious framing.
