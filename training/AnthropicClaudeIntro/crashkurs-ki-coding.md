# Crashkurs: KI-gestütztes Coden für Entwickler

**Dauer:** 90 Minuten
**Zielgruppe:** Entwickler ohne oder mit wenig Erfahrung mit KI-Coding-Tools
**Lernziel:** Nach dem Kurs können die Teilnehmer Claude Code und KI-Plugins produktiv im Entwickleralltag einsetzen.

---

## 1. Einführung & Motivation (10 Min)

### 1.1 Warum KI beim Coden?
- Produktivitätsgewinn durch Automatisierung wiederkehrender Aufgaben
- Bessere Codequalität durch Reviews, Tests und Refactoring-Vorschläge
- Schnellere Einarbeitung in fremde Codebasen
- KI als "Pair Programmer", nicht als Ersatz

### 1.2 Landschaft der KI-Coding-Tools
- Claude Code (CLI / Agent)
- GitHub Copilot & Copilot Chat
- Cursor / Windsurf (KI-native IDEs)
- Visual Studio & VS Code Plugins (Claude, Copilot, Continue.dev)
- Unterschiede: Chat-Assistenz vs. agentisches Arbeiten

### 1.3 Grundbegriffe
- Prompt, Kontext, Context Window
- Tool Use / Function Calling
- Agenten vs. Autocomplete
- Modelle: Claude, GPT, Gemini – wann welches?

---

## 2. Claude Code – Hands-on (25 Min)

### 2.1 Installation & Setup
- Voraussetzungen (Node.js, API-Zugang / Abo)
- Installation via npm
- Authentifizierung
- Projektverzeichnis initialisieren mit `/init` und `CLAUDE.md`

### 2.2 Erste Schritte im Terminal
- Chat starten und Dateien lesen lassen
- Änderungen durchführen und reviewen (Diff-Ansicht)
- Git-Integration: Commits, PRs, Branches erstellen lassen
- Tests ausführen lassen und Fehler automatisch beheben

### 2.3 Wichtige Features
- Slash Commands (`/review`, `/security-review`, `/init`)
- Subagents für komplexe Aufgaben
- MCP-Server (Model Context Protocol) für externe Tools
- Hooks & Plugins
- Permissions & Sandbox verstehen

### 2.4 Live-Demo: Feature von A–Z
- Anforderung aufnehmen → Plan erstellen lassen → Implementierung → Tests → Commit

---

## 3. IDE-Integration: Visual Studio & VS Code (20 Min)

### 3.1 Claude-Plugin für VS Code
- Installation und Konfiguration
- Inline-Chat & Side-Panel
- Kontext aus offenen Dateien, Selektion und gesamtem Workspace
- Integration mit Claude Code CLI

### 3.2 Alternativen im Überblick
- GitHub Copilot & Copilot Chat
- Continue.dev (Open Source, modell-agnostisch)
- Cursor / Windsurf für KI-first Workflow

### 3.3 Typische IDE-Workflows
- Inline-Vorschläge (Tab-Completion) sinnvoll nutzen
- Refactoring per Selektion & Prompt
- Debugging mit KI-Unterstützung
- Dokumentation und Kommentare generieren

---

## 4. Praktische Workflows & Use Cases (15 Min)

### 4.1 Entwickleralltag
- Neues Feature implementieren (inkl. Tests)
- Bugfix anhand von Stacktrace oder Issue
- Code-Review automatisieren
- Legacy-Code verstehen und dokumentieren
- Migrationen (z. B. Framework-Upgrade)

### 4.2 Generierung von Tests & Dokumentation
- Unit-Tests aus bestehender Funktion ableiten
- README & API-Docs generieren
- Commit-Messages und PR-Beschreibungen

### 4.3 Daten- und Konfigurationsaufgaben
- SQL-Queries, Regex, Shell-Skripte
- YAML-/JSON-Konfiguration erstellen und validieren

---

## 5. Best Practices & Prompt Engineering (10 Min)

### 5.1 Gute Prompts schreiben
- Kontext, Ziel, Randbedingungen klar angeben
- Positiv- und Negativbeispiele geben
- Schrittweises Vorgehen einfordern ("plan first, then code")
- Ausgabeformat spezifizieren

### 5.2 Kontext effektiv nutzen
- Relevante Dateien gezielt einbinden
- `CLAUDE.md` / Projekt-Guidelines pflegen
- Lange Sessions konsolidieren statt endlos fortführen

### 5.3 Iteratives Arbeiten
- Kleine Schritte statt „alles auf einmal"
- Zwischenergebnisse reviewen und committen
- KI-Ausgaben immer verifizieren (Tests, Lint, manueller Review)

---

## 6. Fallstricke, Qualität & Sicherheit (7 Min)

### 6.1 Typische Fehler
- Halluzinierte APIs und Bibliotheken
- Veraltete Syntax
- Übermäßiges Vertrauen in generierten Code

### 6.2 Sicherheit & Compliance
- Keine Secrets/Credentials in Prompts
- Lizenzfragen bei generiertem Code
- Umgang mit sensiblen Daten & interne Policies
- Review-Pflicht vor Merge

### 6.3 Kostenbewusstsein
- Token-Verbrauch verstehen
- Modelle je nach Aufgabe wählen (Haiku vs. Sonnet vs. Opus)

---

## 7. Ausblick & Q&A (3 Min)

### 7.1 Nächste Schritte im Team
- Gemeinsame `CLAUDE.md`-Konventionen
- MCP-Server für interne Tools anbinden
- Erfahrungen teilen (Slack-Channel / Wiki)

### 7.2 Weiterführende Ressourcen
- Offizielle Doku: docs.claude.com
- Anthropic Prompt Engineering Guide
- Interne Beispiele & Best-Practice-Repo

### 7.3 Fragen & Diskussion

---

## Anhang: Vorbereitung für Teilnehmer

- Laptop mit installierter IDE (VS Code oder Visual Studio)
- Node.js ≥ 18
- Zugang zu Claude Code / API-Key (vorher verteilen!)
- Beispiel-Repository lokal geklont
- Git konfiguriert
