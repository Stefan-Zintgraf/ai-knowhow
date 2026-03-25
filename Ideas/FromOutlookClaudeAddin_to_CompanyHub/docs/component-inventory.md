# Component Inventory

**Generated:** 2026-02-26 | **Scan Level:** Deep

## UI Components (WPF)

### Views

| Component | Type | File | Description |
|---|---|---|---|
| `ChatView` | UserControl | `UI/ChatView.xaml` | Main chat interface — message list (ItemsControl + ScrollViewer), text input, send button, "New" button header. Dark theme (#1E1E1E). |
| `ApiKeyDialog` | Window | `UI/ApiKeyDialog.xaml` | Modal dialog for API key setup. Step-by-step instructions with hyperlinks to Anthropic console. Dark theme with monospace input. |

### ViewModels

| Component | File | Bindings |
|---|---|---|
| `ChatViewModel` | `UI/ChatViewModel.cs` | `Messages` (ObservableCollection), `InputText` (string), `IsLoading` (bool), `SendMessageCommand` (ICommand), `NewChatCommand` (ICommand), `ScrollToBottomRequested` (event) |

### Models

| Component | File | Properties |
|---|---|---|
| `ChatMessage` | `UI/ChatMessage.cs` | `Role` (user/assistant/system), `Content`, `Timestamp`, computed: `IsUser`, `IsAssistant`, `IsSystem` |

### Value Converters

| Converter | File | Input → Output |
|---|---|---|
| `MessageAlignmentConverter` | `UI/Converters/MessageConverters.cs` | Role → HorizontalAlignment (user=Right, others=Left) |
| `MessageBackgroundConverter` | `UI/Converters/MessageConverters.cs` | Role → SolidColorBrush (user=#0078D4, assistant=#323232, system=#781E1E) |
| `MessageForegroundConverter` | `UI/Converters/MessageConverters.cs` | Role → Brushes.White (all roles) |

### WinForms Bridge

| Component | File | Description |
|---|---|---|
| `TaskPaneHost` | `UI/TaskPaneHost.cs` | WinForms UserControl hosting WPF `ChatView` via `ElementHost`. Required by VSTO Custom Task Pane API. |

### Helper Classes

| Component | File | Description |
|---|---|---|
| `RelayCommand` | `UI/ChatViewModel.cs` | ICommand implementation supporting both sync and async delegates. `CanExecuteChanged` hooks `CommandManager.RequerySuggested`. |

## Tool Components (19 Tool Schemas, 18 Active)

### Search Tools (4 active + 1 disabled)

| Tool | Class | File | Description |
|---|---|---|---|
| `list_recent_emails` | `ListRecentEmailsTool` | `SearchTools.cs` | Load emails from past N days into cache |
| `search_email_by_subject` | `SearchBySubjectTool` | `SearchTools.cs` | Search subjects with AND/OR matching |
| `search_email_by_sender_name` | `SearchBySenderTool` | `SearchTools.cs` | Search by sender display name |
| `search_email_by_recipient_name` | `SearchByRecipientTool` | `SearchTools.cs` | Search by To field name |
| ~~`search_email_by_body`~~ | `SearchByBodyTool` | `SearchTools.cs` | **DISABLED** — exists in code but not registered (privacy) |

All search tools extend `SearchToolBase` which provides `ExecuteSearch()`, `MatchesSearch()`, `ExtractEmailData()`, and `SafeGet<T>()`.

### Viewing Tools (4)

| Tool | Class | File | Description |
|---|---|---|---|
| `view_email_cache` | `ViewEmailCacheTool` | `ViewingTools.cs` | Paginated cache view (5/page) |
| `get_email_by_number` | `GetEmailByNumberTool` | `ViewingTools.cs` | Get metadata by 1-based cache position |
| `load_emails_by_folder` | `LoadEmailsByFolderTool` | `ViewingTools.cs` | Load specific folder with day/count limits |
| `clear_email_cache` | `ClearEmailCacheTool` | `ViewingTools.cs` | Clear all cached emails |

### Email Operation Tools (5)

| Tool | Class | File | Description |
|---|---|---|---|
| `reply_to_email` | `ReplyToEmailTool` | `EmailOperationTools.cs` | Reply/ReplyAll with optional custom recipients |
| `compose_email` | `ComposeEmailTool` | `EmailOperationTools.cs` | Create and send new email |
| `move_email` | `MoveEmailTool` | `EmailOperationTools.cs` | Move email to target folder (clears cache) |
| `delete_email` | `DeleteEmailTool` | `EmailOperationTools.cs` | Move to Deleted Items (clears cache) |
| `batch_forward_email` | `BatchForwardEmailTool` | `EmailOperationTools.cs` | Forward to CSV recipient list via BCC (500/batch) |

### Folder Management Tools (5)

| Tool | Class | File | Description |
|---|---|---|---|
| `get_folder_list` | `GetFolderListTool` | `FolderTools.cs` | Hierarchical folder tree for all stores |
| `list_subfolders` | `ListSubfoldersTool` | `FolderTools.cs` | Direct children of a folder |
| `create_folder` | `CreateFolderTool` | `FolderTools.cs` | Create subfolder under specified parent |
| `remove_folder` | `RemoveFolderTool` | `FolderTools.cs` | Delete a folder |
| `move_folder` | `MoveFolderTool` | `FolderTools.cs` | Move folder (with all emails) to new parent |

## Core Components

| Component | File | Description |
|---|---|---|
| `EmailData` | `Core/EmailData.cs` | Email metadata DTO — subject, sender, recipients, date, status, attachments. Formatters: `ToSummary()`, `ToMetadataOnly()`, `ToBasicText()`, `ToEnhancedText()` |
| `AttachmentInfo` | `Core/EmailData.cs` | Attachment DTO — filename, size, embedded flag |
| `EmailCache` | `Core/EmailCache.cs` | Thread-safe Dictionary+List cache. Binary search insert for sorted order. Paged retrieval. Lock-based concurrency. |
| `FolderNavigator` | `Core/FolderNavigator.cs` | MAPI folder resolver — multi-store, path-based, German aliases. Methods: `GetFolder()`, `GetFolderTree()`, `GetSubfolders()` |

## Service Components

| Component | File | Description |
|---|---|---|
| `ClaudeService` | `Services/ClaudeService.cs` | Anthropic REST client. Conversation history. Tool-use loop (max 10). System prompt (German). TLS 1.2 enforcement. |
| `ConversationManager` | `Services/ConversationManager.cs` | **Unused** — reserved for future chat persistence. Methods: `AddUserMessage()`, `AddAssistantMessage()`, `AddToolResults()`, `Clear()` |

## Infrastructure Components

| Component | File | Description |
|---|---|---|
| `IOutlookTool` | `Tools/IOutlookTool.cs` | Tool contract interface |
| `ToolDefinitions` | `Tools/ToolDefinitions.cs` | Static JSON schema generator for all 19 tools |
| `OutlookToolExecutor` | `Tools/OutlookToolExecutor.cs` | Tool registry, dispatch, error handling |
| `SearchToolBase` | `Tools/SearchTools.cs` | Abstract base with common search/extract logic |
