
# TODO

Option A: New chat, Agent mode, direct spec writing
Start a new chat in Agent mode. No special command needed — just tell the agent what you want:
> "I'm building a brainstorming platform. Read my brainstorming session at _bmad-output/brainstorming/brainstorming-session-2026-03-11-001.md, specifically the Session 4 section on POC Build Phases. I need to write the Phase 1 spec files (SPEC-000 through SPEC-006) in a specs/ folder. Start with SPEC-000 (Spec File Format) — the self-describing bootstrap spec."
The agent reads the session file, has full context from your architectural decisions, and starts writing real spec files.
Option B: New brainstorming chat to design SPEC-000 first
If you want to interactively explore what the spec file format should look like before committing, use /bmad-brainstorming, continue the session, and brainstorm the SPEC-000 format. Then move to Agent mode for writing.
My recommendation: Option A. You've already made all the key decisions — SPEC-000 needs to contain build instructions, test assertions (Layer 1 structural + Layer 2 behavioral), dependencies, phase tags, and REPL step coverage (from SCAMPER decisions C-4, A-1, M-3, P-1). That's specific enough to write directly. If the first draft isn't right, you iterate in the same chat.