---
name: start-brainstorming
description: Starts a new BMAD brainstorming session by creating a topic subfolder and installing the BMAD method (CIS module) there. Use when the user asks to start a new brainstorming session, begin brainstorming, set up a brainstorming topic, or similar. Collects topic name, input language, output language, and runs install-bmad.bat with platform "claude-code".
---

# Start Brainstorming Session

## When to use

Apply this skill when the user says they want to:
- Start a new brainstorming session
- Begin a brainstorming (session)
- Set up brainstorming for a topic
- Create a new BMAD brainstorming folder
- Install BMAD for a topic

## Workflow

1. **Topic**
   - If the user did **not** provide a topic name, ask: *"What topic should the brainstorming session use? (Use a single word or words separated by underscores, no spaces.)"*
   - Normalize the topic: replace spaces with underscores, remove leading/trailing spaces. Reject or ask again if it still contains spaces.
   - Example: "my great idea" → `my_great_idea`

2. **Input language**
   - If not already clear, ask: *"Which language for communication and input? (English or German)"*
   - Only `English` and `German` are valid. **Default: German.**

3. **Output language**
   - If not already clear, ask: *"Which language for document output? (English or German)"*
   - Same rule: only English or German. **Default: English.**

4. **Platform**
   - **Required.** Use platform **claude-code** for this skill unless the user explicitly wants another. Do not omit platform.

5. **Run install**
   - Locate `install-bmad.bat` using this search order:
     1. **Working directory** (current project root)
     2. **Skill directory** (provided at runtime in the header: `Base directory for this skill: <path>`)
   - Use whichever location is found first. If neither exists, report an error.
   - Arguments: `topic` `platform` [lang] [outlang]. Topic and platform are required; lang/outlang default to German and English if omitted.
   - Example (script found in working dir):
     ```bash
     cd "<working_dir>" && .\install-bmad.bat my_great_idea claude-code German English
     ```
   - Example (script found in skill dir):
     ```bash
     cd "<skill_base_dir>" && .\install-bmad.bat my_great_idea claude-code German English
     ```

6. **Result**
   - If the script exits 0: tell the user the session is ready in `<script_dir>\brainstormings\<topic>` and they can open that folder or continue there.
   - If the script fails: show the script output and suggest fixing topic (no spaces), languages (English/German), or platform. The batch file prints specific errors for invalid topic, language, or platform.
   - If `install-bmad.bat` was not found in either location: inform the user and show both paths that were checked.

## Script location and invocation

- Search order: **working directory first**, then **skill directory**.
- The skill base directory is provided at runtime in the header: `Base directory for this skill: <path>`
- Invoke from the directory where the script was found:
  - `.\install-bmad.bat <topic> <platform> [lang] [outlang]`
  - Defaults: lang=German, outlang=English. Topic and platform are required.

## Valid values (batch script enforces)

- **Topic**: No spaces; words separated by underscores. **Required.**
- **Languages**: `English` or `German` only. Defaults: input German, output English.
- **Platform**: **Required.** `claude-code` for this skill. Valid codes in BMAD-METHOD/tools/platform-codes.yaml.

## Shortcuts

- If the user says e.g. "start brainstorming for product_launch in German", use topic `product_launch`, input language German; default output to English unless they say otherwise.
- If they say "new session, topic: my_topic", use that topic, default input German and output English, platform claude-code.
