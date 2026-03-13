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

Add a BMAD slash-command plugin that registers convenience slash commands
(`/brainstorm`, `/discuss`, `/refine`, `/validate`) and the umbrella `/bmad`
command, matching the existing plugin patterns (`hello`, `testnode`).

These slash commands are not possible at the skill layer — OpenClaw skills
can only register a single command derived from their `name` field (in this
case `/bmad-brainstorm`). The plugin layer uses `api.registerCommand()` to
register arbitrary command names that execute before skill commands in the
dispatch chain.

The plugin does NOT contain brainstorming logic — it parses arguments and
forwards them into the agent session where the `bmad-brainstorm` skill
handles the actual work.

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
| Phase 1 skill | `workspace-wolfgang/skills/bmad-brainstorm/SKILL.md` (must exist) |

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
  "description": "Adds /brainstorm, /discuss, /refine, /validate, and /bmad slash commands for the BMAD brainstorming framework.",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

## 2.3 index.js

The plugin registers five commands. The convenience commands (`/brainstorm`,
`/discuss`, `/refine`, `/validate`) forward directly to the agent where the
`bmad-brainstorm` skill handles them. The `/bmad` umbrella command provides
help and subcommand routing.

```javascript
export default function (api) {
  const HELP_TEXT = [
    "**BMAD — Brainstorming Framework**",
    "",
    "Commands:",
    "  /brainstorm <topic>  — structured brainstorm session",
    "  /discuss <topic>     — alias for /brainstorm",
    "  /refine <idea>       — refine and improve an idea",
    "  /validate <concept>  — validate assumptions and risks",
    "  /bmad help           — show this help",
    "",
    "You can also just describe what you want to brainstorm in natural language.",
  ].join("\n");

  // /brainstorm <topic> — forward to agent as a brainstorm request
  api.registerCommand({
    name: "brainstorm",
    description: "Start a structured BMAD brainstorming session",
    acceptsArgs: true,
    handler: async (ctx) => {
      const topic = (ctx.args || "").trim();
      return {
        text: topic
          ? `[BMAD brainstorm] ${topic}`
          : "[BMAD brainstorm] (no topic provided — please specify)",
        forwardToAgent: true,
      };
    },
  });

  // /discuss <topic> — alias for /brainstorm
  api.registerCommand({
    name: "discuss",
    description: "Start a structured BMAD discussion (alias for /brainstorm)",
    acceptsArgs: true,
    handler: async (ctx) => {
      const topic = (ctx.args || "").trim();
      return {
        text: topic
          ? `[BMAD brainstorm] ${topic}`
          : "[BMAD brainstorm] (no topic provided — please specify)",
        forwardToAgent: true,
      };
    },
  });

  // /refine <idea> — forward to agent as a refine request
  api.registerCommand({
    name: "refine",
    description: "Refine and improve an idea using the BMAD framework",
    acceptsArgs: true,
    handler: async (ctx) => {
      const idea = (ctx.args || "").trim();
      return {
        text: idea
          ? `[BMAD refine] ${idea}`
          : "[BMAD refine] (no idea provided — please specify)",
        forwardToAgent: true,
      };
    },
  });

  // /validate <concept> — forward to agent as a validate request
  api.registerCommand({
    name: "validate",
    description: "Validate assumptions and risks for a concept using BMAD",
    acceptsArgs: true,
    handler: async (ctx) => {
      const concept = (ctx.args || "").trim();
      return {
        text: concept
          ? `[BMAD validate] ${concept}`
          : "[BMAD validate] (no concept provided — please specify)",
        forwardToAgent: true,
      };
    },
  });

  // /bmad [subcommand] — umbrella command with help and routing
  api.registerCommand({
    name: "bmad",
    description: "BMAD brainstorming framework. Usage: /bmad [help|brainstorm|discuss|refine|validate] [topic]",
    acceptsArgs: true,
    handler: async (ctx) => {
      const raw = (ctx.args || "").trim();
      const parts = raw.split(/\s+/);
      const sub = (parts[0] || "help").toLowerCase();
      const rest = parts.slice(1).join(" ");

      switch (sub) {
        case "help":
          return { text: HELP_TEXT };
        case "brainstorm":
        case "discuss":
          return {
            text: `[BMAD brainstorm] ${rest || "(no topic provided — please specify)"}`,
            forwardToAgent: true,
          };
        case "refine":
          return {
            text: `[BMAD refine] ${rest || "(no idea provided — please specify)"}`,
            forwardToAgent: true,
          };
        case "validate":
          return {
            text: `[BMAD validate] ${rest || "(no concept provided — please specify)"}`,
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
agent session where the `bmad-brainstorm` skill picks it up. If the OpenClaw
plugin API does not support `forwardToAgent`, the implementing agent must adapt
to the actual API — check plugin docs or the `testnode` plugin for the correct
routing mechanism.

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

- [ ] Phase 1 skill is deployed (`workspace-wolfgang/skills/bmad-brainstorm/SKILL.md` exists)
- [ ] `examples/plugins/bmad/openclaw.plugin.json` exists with correct manifest
- [ ] `examples/plugins/bmad/index.js` exports a default function registering all five commands
- [ ] Plugin path added to `plugins.load.paths` in `openclaw.json`
- [ ] Gateway restarted without plugin load errors
- [ ] `/bmad help` returns inline help text listing all commands
- [ ] `/brainstorm <topic>` routes through the plugin into the agent and triggers the skill
- [ ] `/discuss <topic>` routes through the plugin (alias for brainstorm)
- [ ] `/refine <idea>` routes through the plugin and triggers the refine mode
- [ ] `/validate <concept>` routes through the plugin and triggers the validate mode
- [ ] `/bmad brainstorm <topic>` also routes correctly via the umbrella command

---

# 4. ARCHITECTURE RULES

- The plugin MUST only parse arguments and route to the agent — no brainstorming logic
- BMAD logic lives in the `bmad-brainstorm` skill (Phase 1) — the plugin is a thin command router
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
