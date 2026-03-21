---
name: start-brainstorming
description: Starts a new BMAD brainstorming session. Supports two modes: (a) create a topic subfolder in the dedicated BRAINSTORMING_FOLDER (CIS module), or (b) install brainstorming directly in the current folder (CIS + BMM modules). Use when the user asks to start brainstorming, begin a brainstorming session, brainstorm here, or set up a brainstorming topic.
---

# Start Brainstorming Session

## When to use

Apply this skill when the user says they want to:
- Start a new brainstorming session
- Begin a brainstorming (session)
- Set up brainstorming for a topic
- Create a new BMAD brainstorming folder
- Install BMAD for a topic
- Brainstorm here / brainstorm in this project / brainstorm in the current folder

## Workflow

### Step 1 — Location choice

Ask the user:

> *"Where do you want to brainstorm?*
> *(a) In the BRAINSTORMING_FOLDER (dedicated brainstorming directory)*
> *(b) In the current folder (brainstorm within this project)"*

If the user's request already makes the choice clear (e.g. "brainstorm here" → option b, "start brainstorming about weather" → option a), skip asking and proceed with the implied option.

---

### Option (a) — BRAINSTORMING_FOLDER mode

**1. Handle BRAINSTORMING_FOLDER environment variable**
   - Check if `BRAINSTORMING_FOLDER` is set by running: `echo %BRAINSTORMING_FOLDER%`.
   - **If set**: show the path to the user and ask: *"BRAINSTORMING_FOLDER is set to `<path>`. Use this folder, or provide a new path?"*
     - If user confirms → proceed.
     - If user provides a new path → run `setx BRAINSTORMING_FOLDER "<new_path>"` to persist it, and `set BRAINSTORMING_FOLDER=<new_path>` for the current session.
   - **If not set**: ask the user: *"BRAINSTORMING_FOLDER is not set. Please provide a path for your brainstorming topics (e.g. C:\PROJ\brainstormings)."*
     - Run `setx BRAINSTORMING_FOLDER "<path>"` to persist and `set BRAINSTORMING_FOLDER=<path>` for the current session.

**2. Topic**
   - If the user did **not** provide a topic name, ask: *"What topic should the brainstorming session use? (Use a single word or words separated by underscores, no spaces.)"*
   - Normalize the topic: replace spaces with underscores, remove leading/trailing spaces. Reject or ask again if it still contains spaces.
   - Example: "my great idea" → `my_great_idea`

**3. Input language**
   - If not already clear, ask: *"Which language for communication and input? (English or German)"*
   - Only `English` and `German` are valid. **Default: German.**

**4. Output language**
   - If not already clear, ask: *"Which language for document output? (English or German)"*
   - Same rule: only English or German. **Default: English.**

**5. Platform**
   - **Required.** Use platform **cursor** for this skill unless the user explicitly wants another. Do not omit platform.

**6. Run install**
   - Call the batch script from the project root:
     ```bash
     .\install-bmad.bat --mode folder <topic> cursor <lang> <outlang>
     ```
   - On Windows use `.\install-bmad.bat` or `install-bmad.bat` from the brainstormings folder.

**7. Result**
   - If the script exits 0: tell the user the session is ready in `<BRAINSTORMING_FOLDER>\<topic>` and they can open that folder or continue there.
   - If the script fails: show the script output and suggest fixes.

---

### Option (b) — Current folder mode

**1. Determine and confirm the target folder**
   - The user may say "this folder", "here", "current folder", "in this project", or similar vague references.
   - **If you can determine the working directory** (e.g. the IDE or tool has set a project root / current working directory): show it to the user and ask for confirmation:
     *"I'll install BMAD brainstorming in `<working_directory>`. Is this the correct folder?"*
   - **If you cannot determine a specific folder** from context (no working directory available, ambiguous reference): do NOT guess or suggest a folder. Instead ask:
     *"Which folder should I install brainstorming in? Please provide the full path."*
   - Only proceed after the user has confirmed or provided the target folder.
   - Store the confirmed path as `<target_dir>` for use in step 5.

**2. Input language**
   - If not already clear, ask: *"Which language for communication and input? (English or German)"*
   - Only `English` and `German` are valid. **Default: German.**

**3. Output language**
   - If not already clear, ask: *"Which language for document output? (English or German)"*
   - Same rule: only English or German. **Default: English.**

**4. Platform**
   - **Required.** Use platform **cursor** for this skill. Do not omit platform.

**5. Run install**
   - **IMPORTANT**: Run the script **from the target folder**, not from the script directory. The script uses `%CD%` to determine where to install, so the working directory must be the user's target folder.
     ```bash
     cd "<target_dir>" && "<script_dir>\install-bmad.bat" --mode current cursor <lang> <outlang>
     ```
   - Note: use the full path to `install-bmad.bat` since you are cd'ing to the target folder, not the script folder.

**6. Result**
   - If the script exits 0: tell the user "BMAD brainstorming (CIS + BMM modules) is installed in `<target_dir>`. You can now run **/bmad-brainstorming** to start the coached brainstorming workflow."
   - If the script fails: show the script output and suggest fixes.

---

## Script location and invocation

- The script is at the workspace root: `install-bmad.bat` (same folder as this skill's project, e.g. `brainstormings`).
- Invoke from the directory that contains `install-bmad.bat`:
  - Folder mode: `.\install-bmad.bat --mode folder <topic> <platform> [lang] [outlang]`
  - Current mode: `.\install-bmad.bat --mode current <platform> [lang] [outlang]`
  - Legacy (backward compat): `.\install-bmad.bat <topic> <platform> [lang] [outlang]` (defaults to folder mode)

## Valid values (batch script enforces)

- **Mode**: `folder` or `current`. Default: `folder`.
- **Topic**: No spaces; words separated by underscores. **Required in folder mode only.**
- **Languages**: `English` or `German` only. Defaults: input German, output English.
- **Platform**: **Required.** `cursor` for this skill. Valid codes in BMAD-METHOD/tools/platform-codes.yaml.

## Shortcuts

- If the user says "start brainstorming for product_launch in German" → option (a), topic `product_launch`, input German, output English.
- If they say "new session, topic: my_topic" → option (a), topic `my_topic`, defaults.
- If they say "brainstorm here" or "brainstorm in this project" → option (b), defaults.
- If they say "brainstorm here in English" → option (b), input English, output English.
