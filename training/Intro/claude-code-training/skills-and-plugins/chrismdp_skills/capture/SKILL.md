---
name: capture
description: Capture atomic thoughts into the Obsidian vault following Zettelkasten principles. Use when user says "capture this", "capture that thought", "make sure you've got that", "save this thought", or when extracting insights from discussions, articles, or meetings.
argument-hint: "[thought to capture]"
---

# Capture Atomic Thought

Quickly capture a discrete thought, insight, or concept into the vault following Zettelkasten principles.

## When to Use

- During conversation when a valuable thought emerges
- When user says "capture this" or "save this thought"
- For extracting insights from discussions, articles, or meetings
- Called by `/triage` and `/weekly-review` for atomic thought creation

## Step 1: Identify the Thought

If the thought isn't explicitly provided, summarise it from the recent conversation:

1. Ask: "What thought would you like to capture?"
2. Or summarise: "I'd suggest capturing: [brief summary]. Does that capture it?"

Keep the thought atomic: one concept per note.

## Step 2: Search for Existing Concepts and Active Projects

**ALWAYS search before creating.** Duplicates waste the knowledge web, and a thought that informs live work needs to flow back into that work — not just sit as an abstract concept.

Use leann semantic search:
```bash
leann search obs-vault "the core concept/thought" --top-k 5
```

The leann index covers concept notes AND `projects/*/PROJECT.md` together — both kinds of hits show up in the same result list. Triage the results into two buckets:

- **Concept hits** (anything not under `projects/`) — exact matches, related concepts, mergeable notes. Used in Step 3.
- **Project hits** (paths matching `projects/*/PROJECT.md`) — live work the thought might tie into. Used in Step 5.

## Step 3: Decide Create vs Merge

**If similar concept exists:**
1. Show the existing note(s) to user
2. Ask: "This seems related to [[Existing Note]]. Should I update that note or create a new one?"
3. If merge: add the new insight to the existing note with today's date reference

**If no similar concept:**
1. Proceed to create new atomic note

## Step 4: Create Atomic Note

### File Naming
- Use descriptive, specific names (not generic)
- No colons in filenames
- Good: "AI Pair Programming Reduces Context Switching"
- Bad: "AI Thoughts" or "Programming: Context"

### Note Structure

```markdown
---
type: concept
first_mentioned: [[YYYY-MM-DD]]
---

[The thought itself - kept SHORT, preserving original wording]

## Active Projects

- [[projects/SLUG/PROJECT|Project Name]] — one-line note on how this thought informs the project

## Related Thoughts

- [[Related Concept 1]]
- [[Related Concept 2]]

## References

- First captured from [[YYYY-MM-DD]] discussion
```

Omit the `## Active Projects` section entirely if no active projects matched in Step 5.

### Type Options
- `concept` - ideas, insights, observations (most common)
- `person` - information about a person
- `project` - project-related note
- `structure-note` - hub that links multiple concepts

### Content Guidelines

- **Keep it SHORT** - only the actual thought, not interpretations
- **Preserve original wording** - don't expand unless asked
- **No H1 headers** - filename serves as title

## Step 5: Tie Into Active Projects

A captured thought often informs live work, not just the abstract concept layer. When the leann results from Step 2 include hits under `projects/*/PROJECT.md`, link the new note bidirectionally so the project sees the thinking and the thought references the live work.

### Identify active project hits

For each leann result whose path matches `projects/*/PROJECT.md`:

1. Read the project's frontmatter (split on `---` delimiters — never grep the full file, decision trails contain stale `status:` lines that produce false matches)
2. Keep only projects with `status: todo` or `status: doing`
3. Discard `done`, `someday`, and anything under `projects/archive/`

If none of the leann hits qualify, skip the rest of this step.

### Confirm (interactive only)

In an interactive session, list the matched active projects and confirm before linking — Chris may want to drop tangential matches or add one leann missed.

In autonomous mode (transcript processing, `/triage`, `/weekly-review`), link all active project hits without prompting. False positives are cheap to remove and the bigger risk is silently failing to surface live work.

### Concept → project (in the new note)

Add an `## Active Projects` section to the new concept note immediately above `## Related Thoughts`:

```markdown
## Active Projects

- [[projects/SLUG/PROJECT|Project Name]] — one-line note on how this thought informs the project
```

Use the full `projects/SLUG/PROJECT` wikilink so it points at the project file directly, not a similarly-named concept note.

### Project → concept (in each PROJECT.md)

For each linked project, edit its `PROJECT.md` to add the new concept under a `## Related Captures` section near the bottom of the body (before any decision trail or events log if present). Create the section if it doesn't exist; otherwise append:

```markdown
## Related Captures

- [[YYYY-MM-DD]] — [[New Concept Note Name]] — one-line context on the link
```

**Rules:**
- Never modify the project's frontmatter from this skill (no status changes, no `assignee` shuffles, no `next_action` rewrites — that's the worker's or Chris's job)
- Append to the existing list rather than replacing it
- One bullet per capture; keep the context line short

## Step 6: Add Backlinks

1. **Link from concept to daily note**: Already done in first_mentioned and References
2. **Link from daily note to concept**: Edit today's daily note to add a wikilink where the thought originated

If processing a specific date's notes (not today):
- Use that date for first_mentioned
- Add backlink to that daily note instead

## Step 7: Cross-Link Related Concepts

**After creating multiple concepts from the same source**, ensure they link to each other where relevant.

1. Review all newly created concepts
2. For each concept, check if it relates to other new concepts from this batch
3. Update the "Related Thoughts" section of each note to include cross-links
4. Add brief context for why they're related (e.g., `[[Other Concept]] - explains the underlying cause`)

**Also link to existing concepts found during search:**
- Even if you didn't merge, related existing concepts should be linked
- This builds the knowledge web and aids discoverability

Example cross-linking pattern:
```markdown
## Related Thoughts

- [[Newly Created Concept A]] - related because X
- [[Existing Concept Found in Search]] - provides broader context
- [[Another New Concept]] - addresses the same problem from different angle
```

## Step 8: Confirm Completion

Report to user:
- Created: `[[Note Name]]`
- Linked from: `[[YYYY-MM-DD]]`
- Related to: [list of linked concepts]
- Tied into active projects: [list of linked projects, or "none" if none matched]

## Integration

This skill is used by:
- **`/triage`**: For capturing thoughts from daily note inbox
- **`/weekly-review`**: For extracting atomic thoughts from the week's notes
- **Direct invocation**: When user wants to capture a thought mid-conversation
- **Automatic transcript processing**: Called via `claude -p` from `vault-sync.sh` when new transcripts arrive in `transcripts/`. When running autonomously (no interactive user), skip confirmation prompts and create/merge without asking.

## Important Notes

- **Vault path**: `/home/cp/vault/`
- **Atomic = one concept per note**
- **Search first, create second**
- **Cross-link everything** - new concepts should link to each other and to existing related concepts
- **Tie captures into live work** — captures aren't just for the abstract concept layer. When leann surfaces an active project (`status: todo` or `doing`), bidirectionally link it (Step 5). The thought should feed the work it belongs to, not just sit in the wiki
- **leann indexes are rebuilt periodically** — no action needed after creating notes
- **Don't duplicate knowledge base skills**: When insights come from a knowledge base skill (e.g. `/lenny`), the abstract concepts already live in that skill's reference material. Don't create standalone atomic notes for general frameworks — instead, add a summary section to the relevant project/business-idea note (formatted like the expert insights section in [[Autonote]]). Only create atomic notes for genuinely new thoughts that emerged from the analysis, not the source material itself.
- **Attribute ideas to their source**: When capturing thoughts from transcripts, meetings, or conversations, always note who said it. Add `source_person: [[Person Name]]` to the YAML frontmatter and mention them in the note body (e.g. "[[James Steiner]] observed that..."). Don't present other people's ideas as free-floating concepts — the attribution is part of the knowledge.
