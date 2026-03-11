---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary']
inputDocuments:
  - brainstorming/brainstorming-session-2026-03-11-001.md
documentCounts:
  briefs: 0
  research: 0
  brainstorming: 1
  projectDocs: 0
classification:
  projectType: 'Developer Tool / AI Platform Framework'
  domain: 'AI Developer Tooling'
  complexity: 'medium'
  projectContext: 'greenfield'
workflowType: 'prd'
---

# Product Requirements Document - brainstormingPlatform

**Author:** Stefan
**Date:** 2026-03-11

## Executive Summary

brainstormingPlatform is a persistent, AI-agnostic brainstorming workspace that extends the BMad Method's proven facilitation engine (60+ techniques) with multi-topic management, cross-platform portability, voice interaction, and multi-agent persona discussions. It solves a specific problem: the best thinking happens away from the desk — on a walk, on the ergometer, in bed at 2am — and today it evaporates when the conversation ends or when you switch AI tools. This platform makes structured brainstorming persistent, portable, and progressively richer across sessions, devices, and AI providers.

The platform targets a single power user today (the creator) but is architected for open source release. All state lives in Markdown files and YAML — no databases, no servers, no API keys. Any AI tool with file access can pick up any topic cold. Users who cannot use file access work in an assisted mode where the AI outputs content for manual saving. The platform wraps BMad without forking it: when BMad ships improved techniques or facilitation, the platform benefits automatically through a thin, stable interface contract.

### What Makes This Special

- **Go where you think.** Voice-first interaction enables brainstorming while walking, exercising, or lying awake. The platform meets you where ideas actually happen, not where keyboards are.
- **No lock-in, ever.** Works across Claude, Gemini, Cursor, OpenClaw, and future local models. The filesystem is the only integration layer. Switching AI tools is as simple as switching text editors.
- **BMad is the brain, not the body.** The platform orchestrates; BMad facilitates. Session output is PRD-structured, flowing directly into downstream BMad workflows (Create PRD, Create Architecture, Implement Story). Brainstorming becomes the upstream thinking layer of a full development lifecycle.
- **Multi-agent personas as collaborative team members.** The endgame: multiple AI personas (Critic, Enthusiast, Logical Thinker) brainstorm together on your topic via file-based exchange. Through OpenClaw integration, these personas can participate in real human meetings as additional team members — AI not as a tool, but as a colleague.
- **Self-building, self-testing.** The platform is built by AI agents using its own spec files. A Python spec runner orchestrates autonomous build-test-fix loops. The brainstorming session output is the requirements document — no translation step.

## Project Classification

- **Project Type:** Developer Tool / AI Platform Framework
- **Domain:** AI Developer Tooling
- **Complexity:** Medium — novel architecture patterns (filesystem-as-truth, AI-agnostic portability, multi-agent file-based communication) but no regulatory burden
- **Project Context:** Greenfield — new product, no existing codebase
