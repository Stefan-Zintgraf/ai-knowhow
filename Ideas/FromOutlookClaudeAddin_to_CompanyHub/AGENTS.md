# Agent instructions – OutlookClaudeAddin

When working in this repo, **refer to [CLAUDE.md](CLAUDE.md)** for:

- **Environment**: Windows (win32), use PowerShell for commands and file operations (not bash).
- **Building**: MSBuild path, build command, and the requirement to quote `'Any CPU'` in PowerShell.
- **Certificate / signing**: Self-signed cert setup, thumbprint, and that manifest signing cannot be disabled for VSTO.
- **Build output**: What is produced in `OutlookClaudeAddin\bin\Debug\` after a successful build.

Use the conventions and commands documented in CLAUDE.md for builds, file listing, and signing so that instructions work correctly on this Windows setup.
