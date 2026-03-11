# Risiken und Probleme beim Einsatz von Coding‑Agenten in großen, produktionskritischen Brownfield‑Systemen

## 1. Typische Problemklassen

- **Kontextbarriere & implizite Business‑Logik**  
  Legacy‑Systeme enthalten Jahrzehnte an implizitem Wissen in undokumentierten Regeln, Side‑Effects und Architekturentscheidungen, die ein Agent nicht aus dem Code allein rekonstruieren kann.  
  → Ergebnis: syntaktisch korrekter Code, der zentrale, nur im Kopf erfahrener Entwickler vorhandene Invarianten verletzt – in Produktionssystemen potentiell katastrophal.  
  Quelle: https://www.linkedin.com/pulse/why-your-ai-coding-agents-fail-brownfield-project-how-sandeep-sgv4c  

- **Skalierungsproblem großer Repositories**  
  Sobald der relevante Ausschnitt des Codes nicht mehr in ein Kontextfenster passt, haben Agenten Mühe, die wirklich relevanten Stellen zu finden, bestehende Muster einzuhalten und globale Invarianten zu respektieren.  
  → Folge sind lokale Fixes, die übergreifende Systemannahmen an anderer Stelle brechen (Broken‑Windows‑Effekt).  
  Quellen:  
  - https://www.arguingwithalgorithms.com/posts/legacy-codebases.html  
  - https://news.ycombinator.com/item?id=46788196  

- **Technische‑Schulden‑Amplifikation**  
  In monolithischen, eng gekoppelten Brownfield‑Systemen erzeugen Agenten Code, der für sich genommen funktioniert, aber System‑Wechselwirkungen ignoriert.  
  Studien berichten z.B. von deutlich mehr statischen Warnungen und erhöhter kognitiver Komplexität in Repositories, die stark KI‑Code verwenden.  
  Quelle (Studie): https://arxiv.org/html/2601.13597  

## 2. Konkrete Beispiele aus Praxis und Studien

- **Brownfield‑Praxisbericht: Scheitern von Coding‑Agenten**  
  Ein LinkedIn‑Artikel beschreibt, dass Unternehmen in reifen Brownfield‑Systemen statt der erwarteten 30–40 % Produktivitätsgewinn sogar Verlangsamung bei Senior‑Entwicklern beobachten, weil sie Agent‑Vorschläge permanent korrigieren müssen.  
  Typischer Vorfall: Ein Agent refaktoriert einen „harmlosen“ Zahlungsworkflow und entfernt scheinbar toten Code, der in Wahrheit regulatorische Sonderfälle abdeckt.  
  Link: https://www.linkedin.com/pulse/why-your-ai-coding-agents-fail-brownfield-project-how-sandeep-sgv4c  

- **BeyondSWE‑ähnliche Benchmarks / Realistische Tasks**  
  Neue Benchmark‑Studien zu KI‑Code‑Agenten in komplexeren, realitätsnahen Szenarien (z.B. repo‑weite Refactorings, abhängigkeitssensitive Migrationsläufe) zeigen, dass Erfolgsraten von über 80 % bei einfachen Aufgaben auf unter 45 % sinken.  
  Diese Ergebnisse unterstreichen, dass „ein kleines Open‑Source‑Issue lösen“ nicht mit einem groß angelegten Eingriff in ein produktionskritisches Legacy‑System vergleichbar ist.  
  Link (Beispielstudie, BeyondSWE):  
  https://www.mind-verse.de/news/neue-benchmark-studie-herausforderungen-ki-code-agenten-entwicklungsumgebungen  

- **Legacy‑Refactoring‑Erfahrungen**  
  Praktische Erfahrungsberichte zu Refactorings großer Legacy‑Codebasen betonen, dass Agenten erst dann verlässlichere Ergebnisse liefern, wenn der Code vorher „LLM‑tauglich“ gemacht wurde: bessere Modularisierung, klarere Namensgebung und verlässliche Tests.  
  Ohne belastbares Testnetz bleiben großflächige, automatisierte Refactorings mit Agenten extrem riskant.  
  Beispielartikel: https://www.arguingwithalgorithms.com/posts/legacy-codebases.html  

## 3. Produktions‑ und Sicherheitsrisiken

- **Unsichtbare Qualitätsdegradation**  
  Langzeit‑Analysen zu autonomen Coding‑Agenten zeigen signifikant steigende Komplexität und mehr statische Warnungen in Repositories, die verstärkt KI‑Code nutzen – obwohl Features subjektiv „schneller“ geliefert werden.  
  In produktionskritischen Umgebungen (z.B. Fertigung, Safety‑relevante Systeme) ist diese schleichende Erosion besonders gefährlich, weil sie sich erst spät in Ausfällen oder Sicherheitsvorfällen niederschlägt.  
  Studie: https://arxiv.org/html/2601.13597  

- **Sicherheitslücken & Geheimnislecks**  
  Security‑Analysen zu KI‑Code‑Assistenten heben hervor, dass unsichere Patterns aus Trainingsdaten übernommen werden (z.B. fehlende Input‑Validierung, hartkodierte Secrets) und dass vertrauliche Informationen leicht unbemerkt in Code oder Logs landen.  
  In großen Brownfield‑Systemen ist die Menge an generiertem Code so groß, dass klassische manuelle Security‑Reviews kaum Schritt halten können.  
  Beispiele:  
  - https://www.devopsdigest.com/the-rise-of-genai-code-assistants-and-the-security-risks-lurking-beneath-the-surface  
  - https://www.securecodewarrior.com/article/ai-coding-assistants-with-maximum-productivity-comes-amplified-risks  
  - https://www.blackduck.com/blog/ai-coding-assistant-security-risks-benefits-devsecops-2025.html  

- **Fehlende Governance & „Vibe‑Coding“**  
  Ein aktueller t3n‑Artikel beschreibt, wie KI‑Agenten in Unternehmen ohne klare Governance eingesetzt werden und Projekte daran scheitern, dass Verantwortlichkeiten, Evaluationskriterien und Sicherheitsprozesse fehlen.  
  In einem Beispiel wurden große Teile einer Plattform weitgehend von einem Assistenten erzeugt; fehlende Reviews führten zu exponierten Datenbanken und API‑Keys im Klartext.  
  Link: https://t3n.de/news/nicht-das-modell-ist-das-problem-ki-agenten-1730278/  

## 4. Spezifische Probleme bei großen Brownfield‑Produktionssystemen

- **Komplexe Abhängigkeiten & Migrationswellen**  
  Repo‑weite Änderungen (Bibliotheks‑Updates, Framework‑Migrationen, Austausch von Industrie‑Protokoll‑Stacks) sind für heutige Agenten schwer sauber durchzuziehen, ohne versteckte Breakages zu erzeugen.  
  Besonders kritisch sind versteckte, nicht dokumentierte Integrationspunkte, herstellerspezifische Hacks und Workarounds, die Agenten nicht erkennen.  
  Quellen:  
  - https://www.mind-verse.de/news/neue-benchmark-studie-herausforderungen-ki-code-agenten-entwicklungsumgebungen  
  - https://www.arguingwithalgorithms.com/posts/legacy-codebases.html  

- **Safety, Normen & Regulatorik**  
  Agenten können Safety‑Patterns und Normen (z.B. IEC‑Normen in der Automatisierung) verletzen, weil diese oft nicht explizit im Code, sondern in Prozessen, Toolchains oder externen Dokumenten verankert sind.  
  Dadurch wird formale Compliance unbemerkt unterlaufen, obwohl Unit‑ und Integrationstests grünes Licht geben.  
  Quellen:  
  - https://www.linkedin.com/pulse/why-your-ai-coding-agents-fail-brownfield-project-how-sandeep-sgv4c  
  - https://arxiv.org/html/2601.13597  

- **Operative Robustheit der Agenten**  
  Erfahrungsberichte nennen Probleme wie Endlosschleifen, hohe Latenzen, instabile Tools, mangelnde Observability und fehlende verlässliche Evaluationsframeworks.  
  Für 24/7‑Fertigungsumgebungen mit engen Wartungsfenstern ist diese operative Unzuverlässigkeit schwer akzeptabel.  
  Beispiele:  
  - Diskussion über operative Probleme bei KI‑Agenten:  
    https://www.reddit.com/r/AI_Agents/comments/1r413m4/discussion_what_are_your_biggest_pains_running_ai/  
  - Allgemeine Gründe für das Scheitern von KI‑Projekten:  
    https://www.mm-software.com/more-the-newsroom/detail/am-problem-vorbeigebaut-warum-so-viele-ai-projekte-schon-am-start-scheitern  

## 5. High‑Level‑Muster zur Risikobegrenzung

- **Einsatzfokus verschieben**  
  Empfehlenswert ist zunächst der Einsatz von Agenten für Low‑Risk‑High‑Leverage‑Aufgaben:  
  - Generierung und Ergänzung von Tests  
  - Dokumentation und Kommentar‑Verbesserungen  
  - Statische Analysen, Dependency‑Mapping, Code‑Standardisierung  
  Nicht empfohlen ist der direkte, autonome Eingriff in Safety‑kritische Produktionspfade.  
  Quellen:  
  - https://www.mind-verse.de/news/neue-benchmark-studie-herausforderungen-ki-code-agenten-entwicklungsumgebungen  
  - https://www.linkedin.com/pulse/why-your-ai-coding-agents-fail-brownfield-project-how-sandeep-sgv4c  

- **„LLM‑ifizierung“ der Codebasis**  
  Systematische Verbesserung von Testabdeckung, Modularisierung und Inline‑Dokumentation erhöht die Chance, dass Agenten Änderungen vornehmen können, ohne globale Invarianten zu brechen.  
  Dazu gehören klare API‑Verträge, explizit dokumentierte Business‑Regeln und automatisierte Regressionstests.  
  Quellen:  
  - https://www.arguingwithalgorithms.com/posts/legacy-codebases.html  
  - https://news.ycombinator.com/item?id=46788196  

- **Strenge Governance & Prozesse**  
  Empfohlene Maßnahmen:  
  - Verpflichtende Reviews für KI‑generierten Code  
  - Automatisierte Security‑ und Compliance‑Scans im CI/CD  
  - Sandbox‑Deployments mit Telemetrie vor Rollout in die Produktion  
  - Klare Policies, in welchen Domänen Agenten **nicht** eingesetzt werden dürfen (z.B. Safety‑Kernlogik, kryptographische Komponenten).  
  Quellen:  
  - https://t3n.de/news/nicht-das-modell-ist-das-problem-ki-agenten-1730278/  
  - https://www.devopsdigest.com/the-rise-of-genai-code-assistants-and-the-security-risks-lurking-beneath-the-surface  
  - https://www.securecodewarrior.com/article/ai-coding-assistants-with-maximum-productivity-comes-amplified-risks  
  - https://arxiv.org/html/2601.13597  

---

## Referenzlinks (Sammlung)

- Why Your AI Coding Agents Fail in Brownfield Projects:  
  https://www.linkedin.com/pulse/why-your-ai-coding-agents-fail-brownfield-project-how-sandeep-sgv4c  

- Benchmark‑Studie zu Herausforderungen von KI‑Code‑Agenten (BeyondSWE):  
  https://www.mind-verse.de/news/neue-benchmark-studie-herausforderungen-ki-code-agenten-entwicklungsumgebungen  

- Legacy‑Codebases & LLM‑Einsatz:  
  https://www.arguingwithalgorithms.com/posts/legacy-codebases.html  

- Diskussionen/Erfahrungen zu Legacy‑Refactoring mit Agenten:  
  https://news.ycombinator.com/item?id=46788196  
  https://www.reddit.com/r/AI_Agents/comments/1pxhuvf/has_anyone_refactored_a_legacy_codebase_using/  

- Security‑Risiken von KI‑Code‑Assistenten:  
  https://www.devopsdigest.com/the-rise-of-genai-code-assistants-and-the-security-risks-lurking-beneath-the-surface  
  https://www.securecodewarrior.com/article/ai-coding-assistants-with-maximum-productivity-comes-amplified-risks  
  https://www.blackduck.com/blog/ai-coding-assistant-security-risks-benefits-devsecops-2025.html  

- Governance‑Fehler und organisatorische Hürden:  
  https://t3n.de/news/nicht-das-modell-ist-das-problem-ki-agenten-1730278/  
  https://www.mm-software.com/more-the-newsroom/detail/am-problem-vorbeigebaut-warum-so-viele-ai-projekte-schon-am-start-scheitern  

- Forschungsarbeit zu Effekten von Coding‑Agenten auf Codequalität:  
  https://arxiv.org/html/2601.13597  
