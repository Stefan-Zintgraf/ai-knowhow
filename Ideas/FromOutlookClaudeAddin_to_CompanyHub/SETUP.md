# Outlook Claude Add-In - Setup-Anleitung

## Voraussetzungen

1. **Visual Studio 2022** (Community oder höher)
2. **Office/SharePoint Development Workload** installiert
   - VS Installer → Ändern → "Office/SharePoint-Entwicklung" aktivieren
3. **Microsoft Outlook** (klassisch, nicht "neues Outlook")
4. **Anthropic API Key** von https://console.anthropic.com

## Projekt erstellen

### Schritt 1: VSTO Projekt anlegen

1. Visual Studio öffnen
2. Datei → Neues Projekt → "Outlook VSTO Add-in" suchen
3. Projektname: `OutlookClaudeAddin`
4. Speicherort: `C:\Users\HMz\Documents\Source\OutlookClaudeAddin\`
5. Framework: **.NET Framework 4.7.2** oder höher
6. Erstellen

### Schritt 2: NuGet Packages installieren

```
Install-Package Newtonsoft.Json
Install-Package System.Net.Http
```

Hinweis: Die offizielle Anthropic C# SDK benötigt .NET Standard 2.0+.
Falls sie nicht mit .NET Framework 4.7.2 kompatibel ist, verwenden wir
direkte HTTP-Aufrufe (bereits im Code implementiert).

### Schritt 3: WPF-Referenz hinzufügen

1. Rechtsklick auf Projekt → Verweis hinzufügen
2. Assemblies → Framework → folgende aktivieren:
   - `PresentationCore`
   - `PresentationFramework`
   - `WindowsBase`
   - `WindowsFormsIntegration`
   - `System.Xaml`

### Schritt 4: Dateien einfügen

Die vorbereiteten Dateien aus dem Source-Ordner in das Projekt kopieren:

```
OutlookClaudeAddin/
├── ThisAddIn.cs                    ← ERSETZEN (nicht die .Designer.cs!)
├── UI/
│   ├── TaskPaneHost.cs             ← Hinzufügen
│   ├── ChatView.xaml               ← Hinzufügen (als WPF UserControl)
│   ├── ChatView.xaml.cs            ← Hinzufügen
│   ├── ChatViewModel.cs            ← Hinzufügen
│   ├── ChatMessage.cs              ← Hinzufügen
│   ├── ApiKeyDialog.xaml           ← Hinzufügen (als WPF Window)
│   ├── ApiKeyDialog.xaml.cs        ← Hinzufügen
│   └── Converters/
│       └── MessageConverters.cs    ← Hinzufügen
├── Services/
│   ├── ClaudeService.cs            ← Hinzufügen
│   └── ConversationManager.cs      ← Hinzufügen
├── Tools/
│   ├── IOutlookTool.cs             ← Hinzufügen
│   ├── ToolDefinitions.cs          ← Hinzufügen
│   ├── OutlookToolExecutor.cs      ← Hinzufügen
│   ├── SearchTools.cs              ← Hinzufügen
│   ├── ViewingTools.cs             ← Hinzufügen
│   ├── EmailOperationTools.cs      ← Hinzufügen
│   └── FolderTools.cs              ← Hinzufügen
└── Core/
    ├── EmailCache.cs               ← Hinzufügen
    ├── EmailData.cs                ← Hinzufügen
    └── FolderNavigator.cs          ← Hinzufügen
```

### Schritt 5: Settings anlegen

1. Rechtsklick Projekt → Properties → Settings
2. Neue Einstellung:
   - Name: `AnthropicApiKey`
   - Typ: `string`
   - Bereich: `Benutzer`
   - Wert: (leer lassen)

### Schritt 6: Build & Test

1. **F5** drücken (Debug starten)
2. Outlook öffnet sich automatisch
3. Rechts erscheint der "Claude Email Assistant" Task Pane
4. Beim ersten Start: API Key eingeben
5. Test: "Zeig mir alle Ordner" tippen

## Fehlerbehebung

### "Die Datei konnte nicht geladen werden"
→ Stell sicher, dass die XAML-Dateien als "Page" (Build Action) gesetzt sind.

### Outlook startet, aber kein Task Pane
→ Outlook → Datei → Optionen → Add-Ins → COM Add-Ins verwalten → Prüfen ob aktiviert.

### API Key Reset
→ Die Settings werden unter `%LOCALAPPDATA%\OutlookClaudeAddin\` gespeichert.
   Lösche den Ordner um den API Key zurückzusetzen.

## Architektur

```
User tippt Nachricht
    ↓
ChatViewModel → ClaudeService.SendMessageAsync()
    ↓
Claude API (mit 19 Tool-Definitionen)
    ↓
Claude antwortet mit tool_use (z.B. search_email_by_subject)
    ↓
OutlookToolExecutor.ExecuteToolAsync() → SearchTools.cs
    ↓
Outlook COM API (direkt im Prozess)
    ↓
Ergebnisse → zurück an Claude API
    ↓
Claude formuliert Antwort auf Deutsch
    ↓
Antwort erscheint im Chat
```
