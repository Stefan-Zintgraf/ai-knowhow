# Brainstorming Platform

Run BMAD brainstorming sessions with AI-assisted coaching. This repo provides the **start-brainstorming** skill and **install-bmad.bat** to create topic folders and install the BMAD method (CIS module) for your IDE.

---

## Quick start

1. **Set up** (one-time): copy the skill and script, set `BRAINSTORMING_FOLDER`.
2. **Start a session**: in chat, say e.g. *"Start new brainstorming about &lt;topic&gt;"*.
3. **Work in the topic folder**: open the new folder and run `/bmad-brainstorming` in a fresh chat.

---

## Prerequisites

- **Node.js** with `npx` (used by `install-bmad.bat` to run `bmad-method install`).
- **BRAINSTORMING_FOLDER** environment variable set to your root folder for brainstorming topics (e.g. `C:\PROJ\brainstormings` or `%USERPROFILE%\brainstormings`).

---

## Setup (one-time)

1. **Copy the skill**  
   Copy the `start-brainstorming` skill to your global skills folder, for example:
   - Cursor: `%USERPROFILE%\.cursor\skills\`
   - Claude Code: `%USERPROFILE%\.claude\skills\`

2. **Copy the script**  
   Copy `install-bmad.bat` to the **same folder** that will be the parent of your topic folders (or ensure it’s on `PATH` and you run it from that parent).  
   Typically this is the folder pointed to by `BRAINSTORMING_FOLDER`.

3. **Set the environment variable**  
   Set `BRAINSTORMING_FOLDER` to the root directory for brainstorming topic folders, e.g.:
   - `C:\PROJ\brainstormings`
   - `%USERPROFILE%\brainstormings`

---

## Starting a brainstorming session

### Option A: Via the skill (recommended)

In your AI assistant chat, say for example:

- *"Start new brainstorming about weather"*
- *"Begin a brainstorming session for product_launch"*
- *"Set up brainstorming for my_great_idea"*

The skill will ask for topic (if needed), input language, and output language, then run `install-bmad.bat` with platform **cursor** (or the platform you choose). When it succeeds, open the new topic folder and start a new chat there; run **/bmad-brainstorming** to use the BMAD brainstorming workflow.

### Option B: Manual script run

From the directory that contains `install-bmad.bat` (usually your `BRAINSTORMING_FOLDER`):

```batch
install-bmad.bat <topic> <platform> [lang] [outlang]
```

- **topic** — Subfolder name (required). No spaces; use underscores (e.g. `my_great_idea`).
- **platform** — IDE/platform code (required). For Cursor use `cursor`. See `../../BMAD-METHOD/tools/platform-codes.yaml` for all codes.
- **lang** — Communication and default document language: `English` or `German`. Default: `German`.
- **outlang** — Document output language: `English` or `German`. Default: `English`.

Example:

```batch
install-bmad.bat my_great_idea cursor German English
```

After a successful run, open the new folder `%BRAINSTORMING_FOLDER%\<topic>`, start a new chat, and run **/bmad-brainstorming**.

---

## After installation

- The topic folder contains the BMAD method with the **CIS** module and tools for your platform.
- Open that folder in your IDE, start a **new chat**, and run **/bmad-brainstorming** to begin the coached brainstorming workflow.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `BRAINSTORMING_FOLDER` not set | Set it to your root brainstorming directory (e.g. `C:\PROJ\brainstormings`) and restart the terminal/IDE. |
| “topic must not contain blanks” | Use underscores in the topic name (e.g. `my_great_idea`). |
| “topic folder already exists” | Pick another topic name or remove/rename the existing folder. |
| “invalid platform” | Use a valid code from `../../BMAD-METHOD/tools/platform-codes.yaml` (e.g. `cursor`, `claude-code`). |
| “language must be English or German” | Use exactly `English` or `German` for `lang` and `outlang`. |
| Install fails (npx / bmad-method) | Ensure Node.js and `npx` are available; check the script output for the exact error. |

---

## More about BMAD brainstorming

- **Brainstorming techniques**: [Brainstorming Techniques](../../BMAD-METHOD/docs/explanation/features/brainstorming-techniques.md)
- **Run a session (how-to)**: [Run Brainstorming Session](../../BMAD-METHOD/docs/how-to/workflows/run-brainstorming-session.md)
- **BMad knowledge index**: see [AGENTS.md](../AGENTS.md) in the BMad repo.
