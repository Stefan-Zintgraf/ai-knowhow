---
name: backup
description: Create a password-protected backup zip of all OpenClaw configuration
user-invocable: true
---

When /backup is invoked:

1. The user provides only the password after the command (no -pw= prefix). Example: /backup ThisIsThePassword
2. If nothing is provided after /backup, reply with this exact error and stop:
   Usage: /backup PASSWORD
3. If a password was provided, call the exec tool with this exact command:
   bash $OPENCLAW_STATE_DIR/backup.sh -cred -n=wolfgang -v -pw=PASSWORD
   where PASSWORD is exactly what the user typed after /backup (trimmed). If the password contains spaces or special characters, pass it as a single argument to the script (e.g. quote it in the shell command).

Wait for the command to complete and report the output zip file path.
Do NOT run the script without a password — it will hang waiting for stdin input.
