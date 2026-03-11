---
description: "BMAD Phase 2: Optional /bmad slash-command plugin for the wolfgang workspace"
name: bmad-method-plugin
---

# BMAD → OpenClaw — Phase 2: Plugin (Optional)

Version: 2.0
Purpose: Machine-executable build instructions for the **wolfgang** workspace
Prerequisite: Phase 1 skill must be deployed first (`BMAD_Phase1_Skill.md`)

---

# 0. OBJECTIVE

Add a `/bmad` slash-command plugin that provides inline help and subcommand
routing, matching the existing plugin patterns (`hello`, `testnode`).

The plugin does NOT contain brainstorming logic — it parses subcommands and
forwards them into the agent session where the `bmad-method` skill handles
the actual work.

The implementing agent MUST:

- Follow existing plugin patterns in `examples/plugins/` (`hello`, `testnode`)
- Use `openclaw.plugin.json` manifest + `index.js` ES module with `api.registerCommand`
- Register the plugin path in `openclaw.json`
- Verify Phase 1 skill is already deployed before starting

---

# 1. ENVIRONMENT

| Item | Value |
|---|---|
| State dir (`OPENCLAW_STATE_DIR`) | `mele/user.openclaw` |
| Agent | `wolfgang` (default agent) |
| Existing plugins dir | `${OPENCLAW_STATE_DIR}/examples/plugins/` |
| Existing plugins | `hello`, `testnode` |
| Config file | `${OPENCLAW_STATE_DIR}/openclaw.json` |
| Channels | Telegram (`wolfgang` account), WhatsApp (`default` account) — both already bound |
| Gateway restart | `systemctl --user restart openclaw-gateway` |
| Phase 1 skill | `workspace-wolfgang/skills/bmad-method/SKILL.md` (must exist) |

---

# 2. IMPLEMENTATION STEPS

## 2.1 Create Plugin Directory

```
examples/plugins/bmad/
    openclaw.plugin.json
    index.js
```

## 2.2 openclaw.plugin.json

```json
{
  "id": "bmad",
  "name": "BMAD",
  "description": "Adds /bmad slash commands for brainstorming, refining, and validating ideas.",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

## 2.3 index.js

```javascript
export default function (api) {
  api.registerCommand({
    name: "bmad",
    description: "BMAD brainstorming framework. Usage: /bmad [help|brainstorm|refine|validate] [topic]",
    acceptsArgs: true,
    handler: async (ctx) => {
      const raw = (ctx.args || "").trim();
      const parts = raw.split(/\s+/);
      const sub = (parts[0] || "help").toLowerCase();
      const rest = parts.slice(1).join(" ");

      switch (sub) {
        case "help":
          return {
            text: [
              "**BMAD — Brainstorming Framework**",
              "",
              "Commands:",
              "  /bmad help              — show this help",
              "  /bmad brainstorm <topic> — structured brainstorm session",
              "  /bmad refine <idea>     — refine and improve an idea",
              "  /bmad validate <concept> — validate assumptions and risks",
              "",
              "You can also just describe what you want to brainstorm in natural language.",
            ].join("\n"),
          };
        case "brainstorm":
        case "refine":
        case "validate":
          return {
            text: `[BMAD ${sub}] ${rest || "(no topic provided — please specify)"}`,
            forwardToAgent: true,
          };
        default:
          return {
            text: `[BMAD brainstorm] ${raw}`,
            forwardToAgent: true,
          };
      }
    },
  });
}
```

**NOTE:** The `forwardToAgent: true` pattern sends the formatted text into the
agent session where the `bmad-method` skill picks it up. If the OpenClaw plugin
API does not support `forwardToAgent`, the implementing agent must adapt to the
actual API — check plugin docs or the `testnode` plugin for the correct routing
mechanism.

## 2.4 Register Plugin in openclaw.json

Add the plugin path to `plugins.load.paths`:

```json
"plugins": {
  "load": {
    "paths": [
      "${OPENCLAW_STATE_DIR}/examples/plugins/hello",
      "${OPENCLAW_STATE_DIR}/examples/plugins/testnode",
      "${OPENCLAW_STATE_DIR}/examples/plugins/bmad"
    ]
  }
}
```

Plugins are already enabled for both channels:

```json
"plugins": {
  "entries": {
    "whatsapp": { "enabled": true },
    "telegram": { "enabled": true }
  }
}
```

## 2.5 Restart Gateway

```bash
systemctl --user restart openclaw-gateway
```

---

# 3. VALIDATION CHECKLIST

The implementing agent MUST verify:

- [ ] Phase 1 skill is deployed (`workspace-wolfgang/skills/bmad-method/SKILL.md` exists)
- [ ] `examples/plugins/bmad/openclaw.plugin.json` exists with correct manifest
- [ ] `examples/plugins/bmad/index.js` exports a default function using `api.registerCommand`
- [ ] Plugin path added to `plugins.load.paths` in `openclaw.json`
- [ ] Gateway restarted without plugin load errors
- [ ] `/bmad` slash command appears in Telegram command list
- [ ] `/bmad help` returns inline help text
- [ ] `/bmad brainstorm <topic>` routes through the plugin into the agent and triggers the skill

---

# 4. ARCHITECTURE RULES

- The plugin MUST only parse subcommands and route to the agent — no brainstorming logic
- BMAD logic lives in the skill layer (Phase 1) — the plugin is a thin command router
- Telegram and WhatsApp are transport layers only — no channel-specific logic
- No undocumented OpenClaw features — follow existing patterns from `hello`, `testnode` plugins
- All file paths relative to `${OPENCLAW_STATE_DIR}`

---

# 5. FILES

| File | Purpose |
|---|---|
| `examples/plugins/bmad/openclaw.plugin.json` | Plugin manifest |
| `examples/plugins/bmad/index.js` | Slash-command handler |
| `openclaw.json` (`plugins.load.paths`) | Register plugin for loading |

---

END OF SPECIFICATION
