# Architecture Documentation

**Generated:** 2026-02-26 | **Scan Level:** Deep | **Project Type:** Desktop (VSTO Outlook Add-in)

## 1. Architecture Overview

OutlookClaudeAddin follows a **layered architecture** combining MVVM for the UI, a service layer for API integration, and a command/tool pattern for Outlook automation. The add-in runs as an in-process COM component inside Microsoft Outlook, surfacing a WPF chat interface through VSTO's Custom Task Pane mechanism.

### Architecture Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    Microsoft Outlook                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │              VSTO Runtime (Host)                   │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │         ThisAddIn (Entry Point)              │  │  │
│  │  │                                              │  │  │
│  │  │  ┌──────────────┐   ┌────────────────────┐  │  │  │
│  │  │  │ TaskPaneHost  │   │   ClaudeService    │  │  │  │
│  │  │  │ (WinForms)    │   │  (HTTP → Claude)   │  │  │  │
│  │  │  │ ┌──────────┐  │   │                    │  │  │  │
│  │  │  │ │ ChatView  │  │   │  Tool-Use Loop:   │  │  │  │
│  │  │  │ │ (WPF)     │  │   │  send → tool_use  │  │  │  │
│  │  │  │ │           │  │   │  → execute → send  │  │  │  │
│  │  │  │ └──────────┘  │   │  → repeat          │  │  │  │
│  │  │  └──────────────┘   └────────────────────┘  │  │  │
│  │  │                                              │  │  │
│  │  │  ┌──────────────────────────────────────┐    │  │  │
│  │  │  │       OutlookToolExecutor             │   │  │  │
│  │  │  │  19 Tools (IOutlookTool)              │   │  │  │
│  │  │  │  ┌─────────┐ ┌─────────┐ ┌────────┐  │   │  │  │
│  │  │  │  │ Search  │ │ Viewing │ │ Email  │  │   │  │  │
│  │  │  │  │ Tools(4)│ │Tools(4) │ │ Ops(5) │  │   │  │  │
│  │  │  │  └─────────┘ └─────────┘ └────────┘  │   │  │  │
│  │  │  │  ┌─────────┐ ┌─────────┐             │   │  │  │
│  │  │  │  │ Folder  │ │  Batch  │             │   │  │  │
│  │  │  │  │Tools(5) │ │  (1)    │             │   │  │  │
│  │  │  │  └─────────┘ └─────────┘             │   │  │  │
│  │  │  └──────────────────────────────────────┘    │  │  │
│  │  │                                              │  │  │
│  │  │  ┌──────────────────────────────────────┐    │  │  │
│  │  │  │             Core Layer                │   │  │  │
│  │  │  │  EmailCache · EmailData · FolderNav   │   │  │  │
│  │  │  └──────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│              Outlook COM Object Model (PIAs)            │
│       (MailItem, MAPIFolder, Session, Store, etc.)      │
└─────────────────────────────────────────────────────────┘
           │
           │ HTTPS (TLS 1.2)
           ▼
   ┌───────────────────┐
   │  Anthropic Claude  │
   │  API (REST)        │
   │  claude-sonnet-4-6 │
   └───────────────────┘
```

## 2. Layer Breakdown

### 2.1 Entry Point Layer (`ThisAddIn.cs`)

The VSTO add-in lifecycle is managed by `ThisAddIn`, which:
1. Retrieves or prompts for the Anthropic API key
2. Instantiates `ClaudeService` and `OutlookToolExecutor`
3. Creates the WPF chat UI inside a WinForms `TaskPaneHost`
4. Registers the Custom Task Pane with Outlook (docked right, 380px wide)

Key constraint: VSTO requires WinForms controls for task panes, so `TaskPaneHost` bridges WPF via `ElementHost`.

### 2.2 UI Layer (`UI/`)

**Pattern:** MVVM (Model-View-ViewModel)

| Component | Role |
|---|---|
| `ChatView.xaml` | WPF UserControl — dark-themed chat interface with message list, input box, send button |
| `ChatView.xaml.cs` | Code-behind — registers `BoolToVisConverter`, exposes `ScrollToBottom()` |
| `ChatViewModel.cs` | ViewModel — message collection, input binding, send/new-chat commands, loading state |
| `ChatMessage.cs` | Model — role (user/assistant/system), content, timestamp |
| `ApiKeyDialog.xaml` | WPF Window — API key setup with step-by-step instructions |
| `TaskPaneHost.cs` | WinForms UserControl — hosts WPF via `ElementHost` |
| `MessageConverters.cs` | 3 IValueConverters for message alignment, background color, foreground color |

**UI Threading:** `Application.Current` is null in VSTO. The ViewModel captures `Dispatcher.CurrentDispatcher` at construction and marshals all UI updates through it.

**Theme:** Dark (#1E1E1E background), user messages in Outlook blue (#0078D4), assistant in dark gray (#323232), system in dark red (#781E1E).

### 2.3 Service Layer (`Services/`)

| Component | Role |
|---|---|
| `ClaudeService` | Manages HTTP communication with the Anthropic API, implements the full tool_use loop (up to 10 iterations), maintains conversation history |
| `ConversationManager` | Reserved for future expansion (chat persistence, multiple conversations). Currently unused — history managed in `ClaudeService` |

**Tool-Use Loop Flow:**
1. User message added to conversation history
2. POST to `https://api.anthropic.com/v1/messages` with all 19 tool schemas
3. If `stop_reason == "tool_use"`: extract tool calls, execute via `OutlookToolExecutor`, append results, loop
4. If `stop_reason == "end_turn"`: extract text response, return to UI

### 2.4 Tool Layer (`Tools/`)

**Pattern:** Command/Strategy with registry-based dispatch

| Component | Role |
|---|---|
| `IOutlookTool` | Interface: `Name` property + `ExecuteAsync(JObject)` |
| `ToolDefinitions` | Static class generating all 19 tool JSON schemas for the Claude API |
| `OutlookToolExecutor` | Registry (Dictionary<string, IOutlookTool>) + dispatch + error wrapping |
| `SearchToolBase` | Abstract base for search tools — provides `ExecuteSearch()`, `MatchesSearch()`, `ExtractEmailData()`, `SafeGet<T>()` |

**19 Registered Tools:**

| Category | Tools | Count |
|---|---|---|
| Search | `list_recent_emails`, `search_email_by_subject`, `search_email_by_sender_name`, `search_email_by_recipient_name` | 4 |
| Viewing | `view_email_cache`, `get_email_by_number`, `load_emails_by_folder`, `clear_email_cache` | 4 |
| Email Operations | `reply_to_email`, `compose_email`, `move_email`, `delete_email`, `batch_forward_email` | 5 |
| Folder Management | `get_folder_list`, `list_subfolders`, `create_folder`, `remove_folder`, `move_folder` | 5 |
| **Total** | | **18** |

Note: `search_email_by_body` exists in code but is not registered in the executor — removed by design (privacy restriction). The schema defines 19 tools but only 18 are active.

**Adding a new tool requires 3 synchronized changes:**
1. Implement `IOutlookTool` (or extend `SearchToolBase`)
2. Add schema in `ToolDefinitions.GetAllToolSchemas()`
3. Register in `OutlookToolExecutor.RegisterAllTools()`

### 2.5 Core Layer (`Core/`)

| Component | Role |
|---|---|
| `EmailData` | DTO representing extracted email metadata — includes `ToSummary()`, `ToMetadataOnly()`, `ToBasicText()`, `ToEnhancedText()` formatters |
| `AttachmentInfo` | Nested DTO for attachment metadata (filename, size, embedded flag) |
| `EmailCache` | Thread-safe in-memory cache using `Dictionary<string, EmailData>` + `List<string>` for ordering. Sorted newest-first via binary search insert. Paged retrieval (5 per page). 1-based numbering. |
| `FolderNavigator` | Resolves Outlook MAPI folder paths supporting multiple stores, default folder shortcuts, and German folder name aliases |

## 3. Data Flow

### 3.1 User Message Flow

```
User types message → ChatViewModel.SendMessageAsync()
  → ClaudeService.SendMessageAsync(text, toolExecutor)
    → POST to Anthropic API (with 19 tool schemas)
    ← Response with tool_use blocks
    → OutlookToolExecutor.ExecuteToolAsync(name, params)
      → IOutlookTool.ExecuteAsync(JObject)
        → Outlook COM operations (via PIAs)
      ← JSON result string
    → Append tool_result to history, re-POST
    ← Final text response (stop_reason: end_turn)
  → ChatViewModel.AddMessage("assistant", response)
    → UI update via Dispatcher
```

### 3.2 Email Cache Flow

```
Search/Load tool invoked → Cache.Clear()
  → Iterate Outlook folder.Items (sorted by ReceivedTime desc)
    → ExtractEmailData(MailItem) — metadata only, no body
    → Cache.Add(EmailData) — binary search insert
  ← Return count message

View tool invoked → Cache.GetPage(pageNum)
  ← Return paginated summaries (5 per page)

Get-by-number → Cache.GetByNumber(n)
  ← Return metadata-only text representation

Move/Delete → Outlook COM operation → Cache.Clear()
```

## 4. State Management

| State | Location | Lifecycle |
|---|---|---|
| Conversation history | `ClaudeService._conversationHistory` (List<JObject>) | Per session, cleared on "New Chat" |
| Email cache | `EmailCache._cache` + `_order` | In-memory, cleared on search/move/delete |
| API key | `Properties.Settings.Default.AnthropicApiKey` | Persisted to `%LOCALAPPDATA%` |
| UI state | `ChatViewModel` (Messages, InputText, IsLoading) | Per session |
| Task pane | `ThisAddIn._chatTaskPane` | Per Outlook session |

## 5. Security Architecture

- **API key storage:** User-scoped .NET settings (not committed, not logged)
- **TLS enforcement:** `ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12` applied before first API call
- **Privacy restriction:** Email body content (`Body`, `HTMLBody`) is never accessed — hardcoded architectural constraint in all tools
- **Tool loop safety:** Maximum 10 iterations per user message (`MaxToolLoops`)
- **HTTP timeout:** 120 seconds for Claude API calls
- **Input validation:** API key must start with `sk-`, tool parameters validated per-tool
- **Error containment:** Tool execution errors returned as JSON to Claude, never thrown to UI

## 6. Deployment Architecture

- **Build system:** MSBuild via Visual Studio 2022 Professional
- **Output:** DLL + VSTO manifest + ClickOnce descriptor (`bin\Debug\`)
- **Signing:** Self-signed certificate (`OutlookClaudeAddin_TemporaryKey.pfx`), VSTO mandates `<SignManifests>true</SignManifests>`
- **Installation:** VSTO ClickOnce deployment (F5 debug deploys automatically)
- **Runtime dependency:** VSTO 4.0 Runtime must be installed on target machine
- **Target:** Microsoft Outlook (Office 15.0+ PIAs)

## 7. Known Limitations and Technical Debt

1. **No automated tests** — all testing is manual via Outlook
2. **`ConversationManager` is unused** — history managed directly in `ClaudeService`
3. **`search_email_by_body` exists in code but is disabled** — dead code that should be removed
4. **No retry/backoff on API failures** — single attempt, errors shown to user
5. **No conversation persistence** — history lost on Outlook restart or "New Chat"
6. **Fixed model and token limit** — `claude-sonnet-4-6` and 4096 tokens hardcoded
7. **Single-threaded tool execution** — tools run sequentially even when Claude requests parallel calls
8. **No localization framework** — German strings hardcoded in source
