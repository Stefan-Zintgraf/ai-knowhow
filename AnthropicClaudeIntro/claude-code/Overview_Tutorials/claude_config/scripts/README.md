# Claude Code Helper Scripts

This directory contains useful scripts for working with Claude Code.

## claude-show-prompts

Extracts and displays your prompts from the current Claude Code session.

**Installation:**
```bash
# Copy to your bin directory
cp claude-show-prompts ~/bin/
chmod +x ~/bin/claude-show-prompts

# Add ~/bin to PATH (if not already there)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Usage:**
```bash
# Show all your prompts from current session
claude-show-prompts

# Or run directly:
~/bin/claude-show-prompts
```

**What it does:**
- Finds your most recent Claude Code session transcript
- Extracts only your actual typed prompts (filters out system messages)
- Shows timestamps and prompt content
- Skips bash outputs, command results, and other system-generated messages

**Example output:**
```
Current Session Transcript
File: eb579296-de22-424a-a454-a7ecd7e2ce65.jsonl
========================================

[#1] 2026-01-11T15:34:35.667Z
------------------------------------------------------------
i have copied these files to /etc/claude-code...

[#2] 2026-01-11T15:45:51.819Z
------------------------------------------------------------
how can i determine the raw json data...

Total user prompts: 7
```

**Location of transcripts:**
All Claude Code session transcripts are stored in:
```
~/.claude/projects/<project-hash>/<session-id>.jsonl
```
