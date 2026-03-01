# Development Guide

**Generated:** 2026-02-26 | **Scan Level:** Deep

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Visual Studio | 2022 Professional | Must include "Office/SharePoint development" workload |
| .NET Framework | 4.7.2 | Target framework (not .NET Core/5+/6+) |
| Microsoft Outlook | 2013+ (Office 15.0+ PIAs) | Required for debugging and runtime |
| VSTO Runtime | 4.0 | Visual Studio 2010 Tools for Office Runtime |
| Anthropic API Key | — | Required at first run; obtain from console.anthropic.com |

## Getting Started

### 1. Clone the Repository

```
git clone <repo-url>
cd OutlookClaudeAddin
```

### 2. Restore NuGet Packages

Open `OutlookClaudeAddin.sln` in Visual Studio 2022. NuGet should auto-restore `Newtonsoft.Json` 13.0.3 from `packages.config`.

Or manually:
```powershell
nuget restore OutlookClaudeAddin.sln
```

### 3. Set Up Code Signing Certificate

VSTO mandates manifest signing — builds fail without a valid certificate.

```powershell
$cert = New-SelfSignedCertificate -Subject 'CN=OutlookClaudeAddin' -CertStoreLocation 'Cert:\CurrentUser\My' -KeyUsage DigitalSignature -Type CodeSigningCert -NotAfter (Get-Date).AddYears(10)
Export-PfxCertificate -Cert $cert -FilePath 'OutlookClaudeAddin\OutlookClaudeAddin_TemporaryKey.pfx' -Password (New-Object System.Security.SecureString)
```

If the thumbprint changes, update `<ManifestCertificateThumbprint>` in `OutlookClaudeAddin.csproj`.

Current thumbprint: `4EB164A0BAD21C91F2AEF51C0A8C72B58C216ACA`

### 4. Build

**Via Visual Studio:** F6 or Build → Build Solution

**Via command line (PowerShell):**
```powershell
& 'C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe' 'OutlookClaudeAddin.sln' /p:Configuration=Debug '/p:Platform=Any CPU' /v:minimal
```

The space in "Any CPU" must be inside a single-quoted string in PowerShell, otherwise MSBuild fails with `MSB1008`.

### 5. Debug

Press **F5** in Visual Studio. This:
1. Builds the solution
2. Deploys the add-in to Outlook via ClickOnce
3. Launches Outlook with the add-in loaded
4. Task pane appears docked on the right (380px wide)
5. First run prompts for Anthropic API key (persisted in user settings)

## Build Output

Successful build produces in `OutlookClaudeAddin\bin\Debug\`:

| File | Description |
|---|---|
| `OutlookClaudeAddin.dll` | Compiled add-in assembly |
| `OutlookClaudeAddin.dll.manifest` | ClickOnce application manifest |
| `OutlookClaudeAddin.vsto` | VSTO deployment descriptor |
| `OutlookClaudeAddin.pdb` | Debug symbols |
| `Newtonsoft.Json.dll` | JSON library |
| Various VSTO runtime DLLs | Office tools utilities |

## Project Structure

```
OutlookClaudeAddin/
├── Core/           # Domain models, caching, folder navigation
├── Services/       # Claude API client, conversation management
├── Tools/          # 19 Outlook tools invokable by Claude
├── UI/             # WPF chat interface (MVVM)
│   └── Converters/ # WPF value converters
└── Properties/     # Assembly info, user settings
```

See [Source Tree Analysis](./source-tree-analysis.md) for full annotated tree.

## Adding a New Tool

Three files must be updated in sync:

### Step 1: Implement the Tool

Create a class implementing `IOutlookTool`:

```csharp
public class MyNewTool : IOutlookTool
{
    public string Name => "my_new_tool";

    public Task<object> ExecuteAsync(JObject parameters)
    {
        // Tool logic here
        return Task.FromResult<object>(new
        {
            type = "text",
            text = "Result message"
        });
    }
}
```

For search-type tools, extend `SearchToolBase` instead.

### Step 2: Add Schema

In `ToolDefinitions.GetAllToolSchemas()`, add:

```csharp
MakeTool("my_new_tool",
    "Description for Claude",
    new JObject
    {
        ["type"] = "object",
        ["properties"] = new JObject
        {
            ["param1"] = Prop("string", "Parameter description")
        },
        ["required"] = new JArray("param1")
    }),
```

### Step 3: Register

In `OutlookToolExecutor.RegisterAllTools()`, add:

```csharp
Register(new MyNewTool(/* dependencies */));
```

All three must stay in sync. A schema without registration causes silent failure; a registration without a schema means Claude will never call it.

## Key Development Rules

### Language & Localization
- User-facing strings (UI, dialogs, system messages): **German**
- Tool result strings returned to Claude API: **English**
- Claude system prompt instructs the model to respond in German

### COM Interop Safety
- Always cast folder items via `as Outlook.MailItem` with null check
- Wrap all COM property access in `SafeGet<T>()` / `TryGet<T>()`
- Never use LINQ on COM collections (`folder.Items`, `folder.Folders`)
- Import as `using Outlook = Microsoft.Office.Interop.Outlook;`

### Framework Constraints
- Use `Newtonsoft.Json` exclusively (not `System.Text.Json`)
- Force TLS 1.2 via `ServicePointManager.SecurityProtocol`
- `Application.Current` is null in VSTO — use stored `Dispatcher.CurrentDispatcher`
- Async: `Task.FromResult` for sync tools, true `async/await` only for HTTP

### Privacy
- Never access `mail.Body` or `mail.HTMLBody` — architectural constraint
- API key stored in user-scoped settings only — never commit or log

## Testing

**Current state:** No automated tests exist. All testing is manual via Outlook.

**Testable without mocking:**
- `EmailCache` — pure in-memory data structure
- `EmailData.ToSummary()`, `ToMetadataOnly()` — formatting logic
- `SearchToolBase.MatchesSearch()` — string matching logic

**Requires COM mocking:**
- All tool implementations (depend on `Outlook.Application`)
- `FolderNavigator` (depends on `Outlook.Session`)

**HTTP testing:**
- `ClaudeService` can be tested by injecting custom `HttpMessageHandler`

## Configuration

### User Settings (`app.config` / Properties)

| Setting | Type | Scope | Description |
|---|---|---|---|
| `AnthropicApiKey` | string | User | Anthropic API key, persisted in `%LOCALAPPDATA%` |

### Hardcoded Constants (`ClaudeService.cs`)

| Constant | Value | Description |
|---|---|---|
| `ApiUrl` | `https://api.anthropic.com/v1/messages` | Anthropic API endpoint |
| `Model` | `claude-sonnet-4-6` | AI model identifier |
| `MaxTokens` | 4096 | Maximum response tokens |
| `MaxToolLoops` | 10 | Safety limit for tool_use iterations |

### Build Configuration

| Config | Platform | Output |
|---|---|---|
| Debug | Any CPU | `bin\Debug\` |
| Release | Any CPU | `bin\Release\` |
