# Brainstorming Platform

Run BMAD brainstorming sessions with AI-assisted coaching. This repo provides the **start-brainstorming** skill and **install-bmad.bat** to set up brainstorming — either in a dedicated topic folder or directly in your current project.

---

## Quick start

1. **Set up** (one-time): copy the skill and script, optionally set `BRAINSTORMING_FOLDER`.
2. **Start a session**: in chat, say e.g. *"Start new brainstorming about &lt;topic&gt;"* or *"Brainstorm here"*.
3. **Work in the topic folder**: open the new folder (or stay in current) and run `/bmad-brainstorming` in a fresh chat.

---

## Prerequisites

- **Node.js** with `npx` (used by `install-bmad.bat` to run `bmad-method install`).
- **BRAINSTORMING_FOLDER** environment variable (optional — the skill will help you set it if needed when using folder mode).

---

## Setup (one-time)

1. **Copy the skill**
   Copy the `start-brainstorming` skill to your global skills folder, for example:
   - Cursor: `%USERPROFILE%\.cursor\skills\`
   - Claude Code: `%USERPROFILE%\.claude\skills\`

2. **Copy the script**
   Copy `install-bmad.bat` to the **same folder** that will be the parent of your topic folders (or ensure it's on `PATH` and you run it from that parent).
   Typically this is the folder pointed to by `BRAINSTORMING_FOLDER`.

3. **Set the environment variable** (optional for current-folder mode)
   Set `BRAINSTORMING_FOLDER` to the root directory for brainstorming topic folders, e.g.:
   - `C:\PROJ\brainstormings`
   - `%USERPROFILE%\brainstormings`

   The skill will prompt you to set this if it's missing when you choose folder mode.

---

## Starting a brainstorming session

### Option A: In a dedicated brainstorming folder (folder mode)

Creates a topic subfolder under `BRAINSTORMING_FOLDER` and installs the **CIS** module.

In your AI assistant chat, say for example:
- *"Start new brainstorming about weather"*
- *"Begin a brainstorming session for product_launch"*

The skill will:
1. Ask where to brainstorm (or infer from your request)
2. Check/set `BRAINSTORMING_FOLDER`
3. Ask for topic, input language, output language
4. Run `install-bmad.bat --mode folder <topic> <platform> <lang> <outlang>`

When done, open the new topic folder and start a new chat; run **/bmad-brainstorming** to use the BMAD brainstorming workflow.

### Option B: In the current folder (current mode)

Installs **CIS + BMM** modules directly in your current working directory — useful for brainstorming within an existing project.

In your AI assistant chat, say for example:
- *"Brainstorm here"*
- *"Start brainstorming in the current folder"*

The skill will:
1. Ask for input language and output language
2. Run `install-bmad.bat --mode current <platform> <lang> <outlang>`

When done, run **/bmad-brainstorming** in the same chat to begin.

### Option C: Manual script run

```batch
REM Folder mode (dedicated brainstorming folder):
install-bmad.bat --mode folder <topic> <platform> [lang] [outlang]

REM Current folder mode:
install-bmad.bat --mode current <platform> [lang] [outlang]

REM Legacy (backward compatible, defaults to folder mode):
install-bmad.bat <topic> <platform> [lang] [outlang]
```

- **--mode** — `folder` (default) or `current`.
- **topic** — Subfolder name (required in folder mode). No spaces; use underscores (e.g. `my_great_idea`).
- **platform** — IDE/platform code (required). For Cursor use `cursor`, for Claude Code use `claude-code`. See `../../BMAD-METHOD/tools/platform-codes.yaml` for all codes.
- **lang** — Communication and default document language: `English` or `German`. Default: `German`.
- **outlang** — Document output language: `English` or `German`. Default: `English`.

Examples:

```batch
install-bmad.bat --mode folder my_great_idea cursor German English
install-bmad.bat --mode current claude-code English English
install-bmad.bat my_great_idea cursor   REM backward compatible, folder mode
```

---

## After installation

- **Folder mode**: The topic folder contains the BMAD method with the **CIS** module and tools for your platform.
- **Current folder mode**: The current directory now has the BMAD method with **CIS + BMM** modules.
- Open the relevant folder in your IDE, start a **new chat**, and run **/bmad-brainstorming** to begin the coached brainstorming workflow.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `BRAINSTORMING_FOLDER` not set | The skill will prompt you to set it. Or set it manually and restart the terminal/IDE. |
| "topic must not contain blanks" | Use underscores in the topic name (e.g. `my_great_idea`). |
| "topic folder already exists" | Pick another topic name or remove/rename the existing folder. |
| "invalid platform" | Use a valid code from `../../BMAD-METHOD/tools/platform-codes.yaml` (e.g. `cursor`, `claude-code`). |
| "invalid mode" | Use `folder` or `current` with the `--mode` flag. |
| "language must be English or German" | Use exactly `English` or `German` for `lang` and `outlang`. |
| Install fails (npx / bmad-method) | Ensure Node.js and `npx` are available; check the script output for the exact error. |

---

## More about BMAD brainstorming

- **Brainstorming techniques**: [Brainstorming Techniques](../../BMAD-METHOD/docs/explanation/features/brainstorming-techniques.md)
- **Run a session (how-to)**: [Run Brainstorming Session](../../BMAD-METHOD/docs/how-to/workflows/run-brainstorming-session.md)
- **BMad knowledge index**: see [AGENTS.md](../AGENTS.md) in the BMad repo.
