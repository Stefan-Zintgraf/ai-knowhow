# Claude Code Managed Settings

This is a backup of the `/etc/claude-code` folder containing Claude Code configuration files.

IMPORTANT: the files in /etc/claude-code are the ones that are active. Change them there and only then copy them into this folder where the readme.md file is located.

IMPORTANT: do never copy readme.md to /etc/claude-code!


**Note:** Just in case you had made changes here, alwasy copy the files to `/etc/claude-code` (do not copy readme.md!):
```bash
sudo cp /home/dev/proj/claude.code/Overview_Tutorials/claude_config/etc/claude-code/*.json /etc/claude-code/
sudo cp /home/dev/proj/claude.code/Overview_Tutorials/claude_config/etc/claude-code/*.sh /etc/claude-code/
```

## Files

### statusline.sh
Custom statusline script that displays:
- Workspace folder (truncated if longer than 40 chars, showing trailing portion)
- Model name (Sonnet 4.5)
- Token usage (current/total)
- Progress bar
- Percentage used
- Session cost

**Example output:**
```
...ials/ec-embedded/ec-embedded.copy/Doc | Sonnet 4.5 | 25k/200k [█░░░░░░░░░] 12.6% | $1.23
```

**Configuration:**
Edit `statusline.sh` to customize:
```bash
DEBUG=0              # Set to 1 to enable JSON logging to /tmp/claude-statusline-*
MAX_WORKSPACE_LEN=40 # Maximum workspace path length before truncation
```

When enabled, JSON data is saved to:
- `/tmp/claude-statusline-latest.json` - Most recent data
- `/tmp/claude-statusline-history.log` - Historical log with timestamps

### managed-settings.json
Main configuration file for Claude Code managed settings including:
- Permissions (denying access to .env files, dangerous commands)
- Company announcements
- Statusline command configuration

### managed-mcp.json
MCP (Model Context Protocol) server configuration.


