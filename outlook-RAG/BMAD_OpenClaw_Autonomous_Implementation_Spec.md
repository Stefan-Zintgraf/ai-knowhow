---
description: BMAD Agile-AI Driven Development Brainstorming Framework
name: bmad-method
---

# BMAD → OpenClaw Integration

## Autonomous Implementation Specification

Version: 1.0 Purpose: Machine-executable build instructions

------------------------------------------------------------------------

# 0. OBJECTIVE

Integrate the BMAD (Agile-AI Driven Development) brainstorming framework
into an existing OpenClaw workspace with:

1.  Skill-based BMAD execution (MVP)
2.  Optional native `/bmad_*` slash command support (Plugin)
3.  Compatibility with Telegram channel
4.  Compatibility with voice pipelines (STT/TTS external)

The implementing agent MUST: - Not assume undocumented OpenClaw
features - Use official skill + plugin extension mechanisms - Keep
Telegram as transport layer only

------------------------------------------------------------------------

# 1. ENVIRONMENT ASSUMPTIONS

-   OpenClaw is already installed
-   A workspace exists
-   Telegram channel is configured OR will be configured later
-   Node.js available (for plugin option)
-   Python optional (only for external voice services)

------------------------------------------------------------------------

# 2. PHASE 1 --- SKILL-BASED BMAD INTEGRATION (REQUIRED)

## 2.1 Create Skill Directory

Inside workspace root:

    skills/bmad-method/

## 2.2 Create File

    skills/bmad-method/SKILL.md

## 2.3 SKILL.md CONTENT (MANDATORY)

# ROLE

You are operating strictly under the BMAD methodology.

# COMMAND CONTRACT

The skill must interpret structured commands:

bmad_help bmad_brainstorm `<topic>`{=html} bmad_refine `<idea>`{=html}
bmad_validate `<concept>`{=html}

If input does not match one of these patterns, request clarification.

# BEHAVIOR DEFINITIONS

## bmad_help

Explain: - BMAD philosophy - Brainstorming workflow - Available
commands - How to invoke skill

## bmad_brainstorm

Execution steps: 1. Clarify objective 2. Define constraints 3. Generate
3--7 structured idea clusters 4. Expand top 3 ideas 5. Recommend next
actions

Output format: - Clear headings - Bullet clusters - Action steps

## bmad_refine

1.  Improve clarity
2.  Identify weaknesses
3.  Improve positioning
4.  Suggest iteration

## bmad_validate

1.  Identify assumptions
2.  Identify failure risks
3.  Suggest experiments
4.  Suggest validation metrics

------------------------------------------------------------------------

## 2.4 Restart Gateway

After file creation:

    openclaw gateway restart

------------------------------------------------------------------------

## 2.5 Invocation Method

Telegram or CLI:

    /skill bmad-method bmad_brainstorm AI-powered robotics

The implementing agent MUST confirm working invocation.

------------------------------------------------------------------------

# 3. PHASE 2 --- OPTIONAL NATIVE SLASH COMMANDS (PLUGIN)

This phase enables:

    /bmad_help
    /bmad_brainstorm
    /bmad_refine
    /bmad_validate

## 3.1 Create Plugin Project

    bmad-plugin/
        package.json
        src/index.ts

## 3.2 package.json

{ "name": "openclaw-bmad-plugin", "version": "1.0.0", "main":
"dist/index.js", "type": "module", "dependencies": {} }

## 3.3 src/index.ts

export default { id: "bmad", commands: \[ { name: "bmad_help",
description: "BMAD help", handler: async (ctx) =\> { return "Use
/bmad_brainstorm `<topic>`{=html} to begin."; }, }, { name:
"bmad_brainstorm", description: "Run BMAD brainstorm", handler: async
(ctx) =\> { const topic = ctx.args.join(" "); return { forwardToSkill: {
skill:"bmad-method", input: `bmad_brainstorm ${topic}` } }; }, }, {
name: "bmad_refine", handler: async (ctx) =\> { const idea =
ctx.args.join(" "); return { forwardToSkill: { skill:"bmad-method",
input: `bmad_refine ${idea}` } }; }, }, { name: "bmad_validate",
handler: async (ctx) =\> { const concept = ctx.args.join(" "); return {
forwardToSkill: { skill:"bmad-method", input: `bmad_validate ${concept}`
} }; }, } \], };

NOTE: If OpenClaw plugin API requires adaptation, the implementing agent
must align with official plugin interface.

## 3.4 Build Plugin

    npm install
    npm run build

## 3.5 Install Plugin

    openclaw plugins install ./bmad-plugin

Restart gateway.

------------------------------------------------------------------------

# 4. TELEGRAM INTEGRATION

Telegram must be configured via:

    openclaw channels login telegram

Verify slash commands are allowed.

Optional configuration:

commands: allowFrom: - telegram

------------------------------------------------------------------------

# 5. VOICE PIPELINE (EXTERNAL)

Voice handling is OUTSIDE OpenClaw core.

The implementing agent may optionally:

1.  Receive Telegram voice
2.  Convert OGG → WAV
3.  Transcribe via Whisper
4.  Send transcript to OpenClaw
5.  Convert response to speech
6.  Send voice reply

This layer MUST remain external.

------------------------------------------------------------------------

# 6. VALIDATION CHECKLIST

The implementing agent MUST verify:

\[ \] Skill loads without error \[ \] /skill bmad-method works \[ \]
Structured brainstorm output is generated \[ \] Plugin installs
successfully (if implemented) \[ \] /bmad_brainstorm works natively (if
plugin implemented) \[ \] Telegram transport functions

------------------------------------------------------------------------

# 7. ARCHITECTURE RULES

-   BMAD logic MUST reside in skill layer
-   Plugin MUST only route commands
-   Telegram MUST remain transport-only
-   No hardcoded model-specific logic
-   No undocumented OpenClaw features

------------------------------------------------------------------------

END OF SPECIFICATION
