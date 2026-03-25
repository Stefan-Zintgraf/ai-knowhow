---
project_name: 'OutlookClaudeAddin'
user_name: 'S.zintgraf'
date: '2026-02-26'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'code_quality_style', 'workflow_rules', 'critical_rules']
status: 'complete'
rule_count: 42
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **C# / .NET Framework 4.7.2** -- VSTO add-in (classic .NET, NOT .NET Core/5+/6+)
- **Visual Studio 2022 Professional** (v17.14) -- MSBuild build system
- **VSTO 4.0** (Microsoft.VisualStudio.Tools.Office.Runtime v10.0) -- Outlook Add-In host
- **Microsoft Outlook Interop / Office PIAs** v15.0 -- COM-based Outlook automation
- **WPF** (PresentationFramework) -- UI layer, hosted inside WinForms via `ElementHost`
- **WinForms** (System.Windows.Forms) -- VSTO task pane bridge (`TaskPaneHost`)
- **Newtonsoft.Json** 13.0.3 -- JSON serialization (NuGet, `packages.config`)
- **System.Net.Http** (framework-bundled) -- HTTP client for Anthropic API
- **Anthropic Claude API** (REST, `anthropic-version: 2023-06-01`) -- Model: `claude-sonnet-4-6`, max 4096 tokens

### Version Constraints

- .NET Framework 4.7.2 does NOT default to TLS 1.2 -- must force via `ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12`
- No Anthropic C# SDK for .NET Framework -- use direct HTTP calls only
- VSTO requires `<SignManifests>true</SignManifests>` -- cannot be disabled; PFX certificate must exist on build machine
- `Application.Current` is null in VSTO -- use `Dispatcher.CurrentDispatcher` for UI thread marshaling
- NuGet packages managed via `packages.config` (not `PackageReference`)

## Critical Implementation Rules

### C# / .NET Framework Rules

- **Async wrapping**: Synchronous tool methods return `Task.FromResult<object>(...)`. True `async/await` only for HTTP calls (`ClaudeService`). `async void` only in `ICommand.Execute` handlers.
- **COM interop safety**: Always wrap Outlook COM property access in `SafeGet<T>()` / `TryGet<T>()` with fallback defaults -- any COM property can throw at runtime.
- **MailItem casting**: Items from `folder.Items` are `object` -- cast via `as Outlook.MailItem` and null-check. Folders contain non-mail items (meeting requests, contacts, etc.).
- **COM collection iteration**: Use `foreach` on COM collections after `.Sort()`. Never use LINQ directly on COM collections.
- **Outlook alias**: Always import as `using Outlook = Microsoft.Office.Interop.Outlook;`
- **Namespaces follow folder structure**: `OutlookClaudeAddin.{Layer}` or `OutlookClaudeAddin.{Layer}.{SubNamespace}` (e.g., `Tools.SearchTools`, `UI.Converters`). Multiple classes per file is normal within tool sub-namespaces.
- **Error surfaces**: Tool execution errors are caught and returned as JSON `{ error, tool, type }` -- never thrown to the caller. User-facing UI errors in German. Tool results returned to Claude API in English.
- **JSON library**: Exclusively `Newtonsoft.Json` (`JObject`, `JArray`, `JsonConvert`). Do NOT use `System.Text.Json`. Tool schemas built manually with `JObject` constructors.

### VSTO / WPF / Outlook COM Rules

**VSTO Add-In Lifecycle:**
- Entry point: `ThisAddIn.cs` with `ThisAddIn_Startup` / `ThisAddIn_Shutdown`, wired via `InternalStartup()` in the designer partial class. Never modify `ThisAddIn.Designer.cs` manually.
- Custom Task Pane via `CustomTaskPanes.Add(winFormsControl, title)` -- must pass a WinForms `UserControl`, not WPF directly.
- API key persisted in `Properties.Settings.Default.AnthropicApiKey` (user-scoped, stored in `%LOCALAPPDATA%`).

**WPF-in-WinForms Bridge:**
- `TaskPaneHost` (WinForms) hosts `ChatView` (WPF) via `ElementHost` with `Dock = Fill`.
- `DataContext` set externally in `ThisAddIn_Startup` -- not inside XAML.
- No `App.xaml` exists -- converters/resources declared per-control in `<UserControl.Resources>`.

**UI Threading (critical):**
- `Application.Current` is **always null** in VSTO -- never use it. Capture `Dispatcher.CurrentDispatcher` at ViewModel construction time and use that stored reference.
- `AddMessage()` and `OnPropertyChanged()` must check `_uiDispatcher.CheckAccess()` and marshal via `_uiDispatcher.Invoke()` when off UI thread.

**MVVM Pattern:**
- `ChatViewModel` implements `INotifyPropertyChanged` with `[CallerMemberName]`.
- Custom `RelayCommand` supports both sync `Action<object>` and async `Func<object, Task>`. `CanExecuteChanged` hooks `CommandManager.RequerySuggested`.
- Dark theme: background `#1E1E1E`, user messages Outlook blue `#0078D4`, assistant `#323232`, system `#781E1E`.

**Tool Architecture:**
- All tools implement `IOutlookTool`: `string Name { get; }` + `Task<object> ExecuteAsync(JObject parameters)`.
- Tools registered by name in `OutlookToolExecutor._tools` dictionary, dispatched via `ExecuteToolAsync(toolName, JObject)`.
- Search tools inherit `SearchToolBase` (provides `ExecuteSearch()`, `MatchesSearch()`, `ExtractEmailData()`, `SafeGet<T>()`). Non-search tools implement `IOutlookTool` directly.
- Tool results are anonymous objects: `{ type = "text", text = "..." }` or `{ type = "json", data = ... }`.

### Testing Rules

- No test project exists yet. If adding tests, create a separate .NET Framework 4.7.2 class library project in the same solution.
- COM-dependent code (tools, folder navigator) requires mocking `Outlook.Application`, `Outlook.MailItem`, etc. Consider interface wrappers if testability becomes a goal.
- `ClaudeService` HTTP calls can be tested by injecting `HttpMessageHandler` into `HttpClient`.
- Pure logic classes are testable without COM mocking: `EmailCache`, `EmailData.ToSummary()`, `SearchToolBase.MatchesSearch()`.

### Code Quality & Style Rules

**File & Folder Organization:**
- Layers by folder: `Core/`, `Services/`, `Tools/`, `UI/`, `UI/Converters/`, `Properties/`.
- One class per file for most classes. Exception: tool sub-namespace files group related tool classes (e.g., `SearchTools.cs` contains `SearchToolBase` + 5 tool classes).
- XAML files paired with `.xaml.cs` code-behind in `UI/`.

**Naming Conventions:**
- PascalCase: classes, methods, properties, events.
- `_camelCase`: private fields (e.g., `_emailCache`, `_httpClient`).
- Tool name strings: `snake_case` matching Claude API convention (`"list_recent_emails"`).
- Tool class names: PascalCase + `Tool` suffix (`ListRecentEmailsTool`, `MoveEmailTool`).

**Documentation:**
- XML doc comments (`/// <summary>`) on public classes, interfaces, and key public methods.
- No XML docs on private methods or individual tool `Execute` implementations.
- Section separators: `// ===== Tool N: tool_name =====`.

**Localization (critical):**
- User-facing strings (UI labels, system prompt, error dialogs): **German**.
- Tool result messages returned to Claude API: **English**.
- Claude system prompt instructs model to respond in German.

**Formatting:**
- No `.editorconfig`, StyleCop, or Roslyn analyzers. Follow existing code style: standard C# formatting, 4-space indentation.

### Development Workflow Rules

**Build:**
- MSBuild via VS 2022: `& 'C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe'`
- Use PowerShell for CLI builds -- bash quoting breaks with spaces in paths.
- Platform must be single-quoted in PowerShell: `'/p:Platform=Any CPU'` (space in value causes MSB1008 otherwise).
- Output in `OutlookClaudeAddin\bin\Debug\`: `.dll`, `.dll.manifest`, `.vsto`, `.pdb`.

**Certificate / Signing:**
- VSTO mandates `<SignManifests>true</SignManifests>` -- cannot be disabled; build hard-fails without it.
- Self-signed cert in `OutlookClaudeAddin_TemporaryKey.pfx` (empty password). Must exist in `Cert:\CurrentUser\My` on the build machine.
- New machine: regenerate cert and update `<ManifestCertificateThumbprint>` in `.csproj`.

**Debug:**
- F5 launches Outlook with the add-in loaded. Task pane appears on the right.
- First run prompts for Anthropic API key (persisted to user settings).
- No automated tests -- manual testing only via Outlook.

### Critical Don't-Miss Rules

**Never Do This:**
- NEVER use `Application.Current` -- it is null in VSTO. Use the stored `_uiDispatcher` reference.
- NEVER use `System.Text.Json` -- project uses Newtonsoft.Json exclusively on .NET Framework 4.7.2.
- NEVER access `mail.Body` or `mail.HTMLBody` in tools -- privacy restriction by design. All tools return metadata only.
- NEVER skip the `as Outlook.MailItem` null check when iterating folder items -- non-mail items (meetings, contacts, tasks) will be present.
- NEVER use LINQ (`.ToList()`, `.Where()`, etc.) on `folder.Items` or `folder.Folders` -- COM collections don't support it reliably.
- NEVER modify `ThisAddIn.Designer.cs` or `ThisAddIn.Designer.xml` manually.

**Edge Cases:**
- Outlook COM objects can throw on any property access -- always wrap in `SafeGet<T>()` / `TryGet<T>()`.
- Folder paths: `"Inbox"` (default store) or `"user@company.com/Inbox/SubFolder"` (specific store). `FolderNavigator` handles both plus German aliases (`"Posteingang"`, `"Gesendete Elemente"`, `"Entwürfe"`, `"Papierkorb"`, etc.).
- `EmailCache` is thread-safe via `lock`, uses 1-based numbering for user-facing references, sorted newest-first.
- Search tools always clear cache before loading. Move/delete operations also clear cache.

**Security:**
- API key in user-scoped settings only -- never commit, never log.
- Force TLS 1.2 before any HTTPS call: `ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12`.
- `HttpClient` timeout: 120 seconds. Tool loop safety limit: 10 iterations (`MaxToolLoops`).

**Adding a New Tool (3-step checklist):**
1. Create class implementing `IOutlookTool` (or extend `SearchToolBase` for search tools).
2. Add tool schema in `ToolDefinitions.GetAllToolSchemas()`.
3. Register instance in `OutlookToolExecutor.RegisterAllTools()`.
All three must stay in sync -- a schema without a registered tool causes silent failure; a registered tool without a schema is never called by Claude.

---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code in this project.
- Follow ALL rules exactly as documented -- especially the "Never Do This" section.
- When in doubt, prefer the more restrictive option.
- Update this file if new patterns emerge during implementation.

**For Humans:**
- Keep this file lean and focused on agent needs.
- Update when technology stack or patterns change.
- Review periodically for outdated rules.
- Remove rules that become obvious over time.

Last Updated: 2026-02-26
