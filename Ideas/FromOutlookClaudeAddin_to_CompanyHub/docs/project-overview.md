# OutlookClaudeAddin - Project Overview

**Generated:** 2026-02-26 | **Scan Level:** Deep | **Version:** 1.0.0

## Executive Summary

OutlookClaudeAddin is a **VSTO (Visual Studio Tools for Office) Outlook Add-in** that integrates Anthropic's Claude AI as an interactive email assistant. It surfaces as a custom task pane docked to the right side of Microsoft Outlook, providing a chat-based interface where users issue natural language commands in German to search, view, organize, compose, and manage emails.

The add-in communicates with Claude via the Anthropic REST API using the `tool_use` protocol, exposing 19 Outlook automation tools that Claude can invoke to interact with the user's mailbox. A privacy-first design prevents access to email body content — only metadata (subject, sender, recipients, dates, attachments) is available to the AI.

## Tech Stack Summary

| Category | Technology | Version |
|---|---|---|
| Language | C# | .NET Framework 4.7.2 |
| IDE / Build | Visual Studio 2022 Professional | MSBuild 17 |
| Host Framework | VSTO 4.0 | Office Runtime 10.0 |
| Office Interop | Outlook PIA | 15.0 |
| UI Framework | WPF (hosted via WinForms ElementHost) | .NET 4.7.2 |
| JSON Library | Newtonsoft.Json | 13.0.3 |
| AI Integration | Anthropic Claude API | 2023-06-01 |
| AI Model | claude-sonnet-4-6 | 4096 max tokens |

## Architecture Classification

| Property | Value |
|---|---|
| Repository Type | Monolith |
| Project Type | Desktop (VSTO Outlook Add-in) |
| Architecture Pattern | MVVM + Service Layer + Tool/Command Pattern |
| Parts | 1 |
| Source Files | 22 C# files |
| XAML Files | 2 (ChatView, ApiKeyDialog) |
| Total LOC | ~2,400 |

## Key Characteristics

- **German-language UI and AI responses** — system prompt, dialogs, and error messages in German; tool result strings in English (consumed by Claude API)
- **Privacy by design** — email body content is never loaded, cached, or sent to the API
- **Tool-use loop** — Claude can chain up to 10 tool invocations per user message
- **Thread-safe caching** — in-memory email cache with lock-based concurrency and binary search insertion
- **Bilingual folder navigation** — supports both English and German Outlook folder names (Inbox/Posteingang, Sent Items/Gesendete Elemente, etc.)
- **Certificate signing required** — VSTO mandates manifest signing; self-signed PFX included

## Links to Detailed Documentation

- [Architecture](./architecture.md)
- [Source Tree Analysis](./source-tree-analysis.md)
- [Component Inventory](./component-inventory.md)
- [Development Guide](./development-guide.md)
- [Master Index](./index.md)
