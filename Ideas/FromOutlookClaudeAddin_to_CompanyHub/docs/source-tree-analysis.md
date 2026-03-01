# Source Tree Analysis

**Generated:** 2026-02-26 | **Scan Level:** Deep

## Annotated Directory Tree

```
OutlookClaudeAddin/                          # Repository root
├── OutlookClaudeAddin.sln                   # Visual Studio solution (single project)
├── AGENTS.md                                # AI agent instructions (points to CLAUDE.md)
├── CLAUDE.md                                # Build/environment session notes
│
├── OutlookClaudeAddin/                      # Main VSTO project
│   ├── OutlookClaudeAddin.csproj            # Project file (.NET 4.7.2, VSTO Outlook)
│   ├── OutlookClaudeAddin_TemporaryKey.pfx  # Code signing certificate (self-signed)
│   ├── packages.config                      # NuGet package manifest (Newtonsoft.Json)
│   ├── app.config                           # Runtime config (user settings, .NET version)
│   ├── ThisAddIn.cs                         # ★ ENTRY POINT - VSTO add-in lifecycle
│   ├── ThisAddIn.Designer.cs                # Auto-generated VSTO designer (DO NOT EDIT)
│   ├── ThisAddIn.Designer.xml               # VSTO host item definition
│   │
│   ├── Core/                                # Domain models and infrastructure
│   │   ├── EmailData.cs                     # Email DTO with summary/metadata formatters
│   │   ├── EmailCache.cs                    # Thread-safe in-memory cache (sorted, paged)
│   │   └── FolderNavigator.cs               # Outlook MAPI folder traversal/resolution
│   │
│   ├── Services/                            # External integrations and orchestration
│   │   ├── ClaudeService.cs                 # Anthropic API client + tool_use loop
│   │   └── ConversationManager.cs           # Conversation history (reserved for future)
│   │
│   ├── Tools/                               # 19 Claude-invokable Outlook automation tools
│   │   ├── IOutlookTool.cs                  # Tool interface: Name + ExecuteAsync
│   │   ├── ToolDefinitions.cs               # JSON schemas for all 19 tools
│   │   ├── OutlookToolExecutor.cs           # Tool registry + dispatch by name
│   │   ├── SearchTools.cs                   # 5 tools: list, search by subject/sender/recipient/body
│   │   ├── ViewingTools.cs                  # 4 tools: view cache, get by number, load folder, clear
│   │   ├── EmailOperationTools.cs           # 5 tools: reply, compose, move, delete, batch forward
│   │   └── FolderTools.cs                   # 5 tools: list, subfolders, create, remove, move
│   │
│   ├── UI/                                  # WPF presentation layer (MVVM)
│   │   ├── ChatView.xaml                    # Main chat interface (dark theme)
│   │   ├── ChatView.xaml.cs                 # Code-behind (scroll-to-bottom, BoolToVis)
│   │   ├── ChatViewModel.cs                 # ViewModel: messages, input, commands + RelayCommand
│   │   ├── ChatMessage.cs                   # Message model (role, content, timestamp)
│   │   ├── TaskPaneHost.cs                  # WinForms-to-WPF bridge (ElementHost)
│   │   ├── ApiKeyDialog.xaml                # API key setup dialog (dark theme, instructions)
│   │   ├── ApiKeyDialog.xaml.cs             # Dialog logic (validation, hyperlinks)
│   │   └── Converters/
│   │       └── MessageConverters.cs         # 3 converters: alignment, background, foreground
│   │
│   └── Properties/
│       ├── AssemblyInfo.cs                  # Assembly metadata (v1.0.0.0)
│       ├── Settings.settings                # User settings definition (API key)
│       └── Settings.Designer.cs             # Auto-generated settings accessor
│
├── docs/                                    # Generated project documentation (this folder)
│
├── _bmad-output/                            # BMAD workflow outputs
│   └── project-context.md                   # Comprehensive AI agent coding rules
│
├── brainstorming/                           # Sprint planning documents
│   ├── BMAD_Sprint_1_Discovery.md
│   ├── BMAD_Sprint_2_Stability.md
│   └── BMAD_Sprint_3_Modernization.md
│
└── _bmad/                                   # BMAD framework (installed modules)
```

## Critical Folders

| Folder | Purpose | Key Files |
|---|---|---|
| `OutlookClaudeAddin/` | Sole project in solution | `.csproj`, `ThisAddIn.cs` |
| `Core/` | Domain models, caching, folder navigation | `EmailCache.cs`, `FolderNavigator.cs` |
| `Services/` | Claude API integration | `ClaudeService.cs` |
| `Tools/` | All 19 Outlook tools for Claude | `OutlookToolExecutor.cs`, `ToolDefinitions.cs` |
| `UI/` | WPF chat interface and dialogs | `ChatView.xaml`, `ChatViewModel.cs` |
| `Properties/` | Assembly info, user settings | `Settings.settings` |

## Entry Points

| Entry Point | File | Trigger |
|---|---|---|
| VSTO Startup | `ThisAddIn.cs` → `ThisAddIn_Startup` | Outlook loads the add-in |
| API Key Dialog | `ApiKeyDialog.xaml` | First run or missing API key |
| Chat Input | `ChatViewModel.SendMessageAsync` | User presses Enter or Send |
| Tool Dispatch | `OutlookToolExecutor.ExecuteToolAsync` | Claude returns `tool_use` block |

## File Statistics

| Category | Count | Description |
|---|---|---|
| C# Source | 22 | All business logic |
| XAML UI | 2 | ChatView, ApiKeyDialog |
| Config/Manifest | 4 | .csproj, packages.config, app.config, .pfx |
| Solution | 1 | OutlookClaudeAddin.sln |
| Documentation | 4 | AGENTS.md, CLAUDE.md, project-context.md, brainstorming/ |
