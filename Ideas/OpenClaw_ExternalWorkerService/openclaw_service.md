# Zusammenfassung: Anbindung eines externen Python-Services an OpenClaw

## 1. Aufgabenstellung und Requirements
- **Ziel:** Ein externer, eigenständiger Python-Service soll in eine OpenClaw-Umgebung (Gateway) integriert werden.
- **Aufgabe des Services:** Automatisierte Recherche im Internet und Beschaffung von Dokumenten (PDFs, Markdown-Dateien, Web-Scrapes).
- **Bidirektionaler Dateizugriff (Neu):** Nicht nur der Service schreibt auf den Gateway, sondern der Gateway (PC 1) muss auch direkten, dateisystemähnlichen Zugriff auf definierte Verzeichnisse des Service-PCs (PC 2) haben (z. B. um lokale Dateien auf dem Service-PC zu lesen, zu bearbeiten und wieder zurückzuschreiben).
- **Speicherort:** Die primären ermittelten Dateien werden auf dem Dateisystem des OpenClaw Gateways in dynamisch generierbaren Unterverzeichnissen abgelegt. Temporäre oder service-spezifische Dateien liegen auf PC 2.
- **Schnittstelle:** Die Dateisystemzugriffe sollen sich auf beiden Seiten wie "normale" lokale Dateioperationen anfühlen (Abstraktion der Netzwerkkomplexität durch Virtual File Systems).
- **Dynamik:** Der Service muss sich beim Gateway selbstständig anmelden (Discovery/Registration), damit der Gateway dessen IP und Fähigkeiten kennt.

## 2. Lösungsarchitektur
Die Architektur basiert auf einem verteilten System mit bidirektionalen "Virtual File System"-Komponenten (VFS). Beide PCs fungieren sowohl als Client als auch als Server für Dateioperationen.

- **PC 1: Der Gateway (OpenClaw / Master)**
  - **OpenClaw Core:** Führt die Workflows (Claws/Nodes) aus.
  - **Service Registry (API):** Ein Endpunkt, der Anmeldungen von externen Services entgegennimmt und verwaltet.
  - **File Receiver/Provider (FastAPI):** Ein Endpunkt (z. B. `GET/PUT /files/{path}`), der Dateiströme empfängt und ausliefert. Verwaltet das Root-Verzeichnis auf PC 1.
  - **VFS-Client (`fsspec`):** Nutzt HTTP, um transparent auf freigegebene Dateien des Service-PCs (PC 2) zuzugreifen.

- **PC 2: Der externe Service (Python / Worker)**
  - **Recherche-Logik:** Führt Web-Scraping und Downloads durch.
  - **FastAPI / Worker-Prozess:** Bietet Endpunkte an, um Arbeitsaufträge vom Gateway entgegenzunehmen.
  - **File Provider/Receiver (FastAPI) (Neu):** Stellt ein lokales Arbeitsverzeichnis (Workspace) per HTTP (`GET/PUT /workspace/{path}`) für den Gateway zur Verfügung.
  - **VFS-Client (`fsspec`):** Nutzt das `HTTPFileSystem`, um Daten über das Netzwerk an den Gateway zu streamen.

## 3. Ablauf Verbindungsaufnahme, Überwachung und Ende
- **Verbindungsaufnahme (Handshake):**
  1. Der Python-Service auf PC 2 startet.
  2. Er sendet einen HTTP POST-Request an den Gateway (PC 1) (z. B. `/register-service`).
  3. Payload: Eigene IP-Adresse (`192.168.1.50`), Port (`8000`), eindeutige ID, Fähigkeiten und **neu:** den Basis-URL-Pfad für seinen lokalen Workspace (z. B. `http://192.168.1.50:8000/workspace/`).
  4. Der Gateway speichert diese Instanz in seiner Registry.
- **Überwachung (Heartbeat/Health Check):**
  - Der Gateway ruft periodisch einen `/health`-Endpunkt auf PC 2 auf, um die Erreichbarkeit zu prüfen.
- **Ende (Graceful Shutdown):**
  - Der Service meldet sich per `/deregister` ab, bevor er beendet wird.

## 4. Ablauf einer Kommunikationsanfrage

### a) Vom Gateway initiiert (Pull / Auftrag)
*Beispiel: "Suche Infos über Thema Humanoids und lege diese in max. 10 Dateien ab."*
1. **Auftragserteilung:** Gateway sendet POST-Request an PC 2 mit Thema und Zielpfad (`/projekte/humanoids/`).
2. **Bestätigung:** PC 2 antwortet mit HTTP 202 Accepted.
3. **Upload via fsspec:** PC 2 nutzt `fsspec`, um die gefundenen Dateien an den File-Receiver von PC 1 (`PUT /files/...`) zu streamen. PC 1 legt bei Bedarf Unterverzeichnisse an.

### b) Vom Python Service initiiert (Push / Event)
*Beispiel: "Ich habe neue Informationen über Aktienkurse."*
1. **Anfrage:** PC 2 fragt beim Gateway via POST an, ob er neue Daten ablegen darf.
2. **Freigabe:** Gateway antwortet mit dem erlaubten Zielpfad.
3. **Upload via fsspec:** PC 2 streamt die Dateien exakt in das vorgegebene Verzeichnis auf PC 1.

### c) Bidirektionaler Dateizugriff (Gateway bearbeitet Datei auf PC 2) (Neu)
*Beispiel: "Service bittet Gateway, eine lokale Textdatei auf PC 2 von CRLF nach LF zu konvertieren."*
1. **Delegation / Event:** PC 2 sendet eine Anfrage an PC 1: "Bitte konvertiere die Datei in meinem Workspace unter `/workspace/temp/raw_data.txt`".
2. **Remote Read (Gateway liest von PC 2):** Der OpenClaw-Node auf PC 1 nutzt seinen `fsspec`-Client, um die Datei von PC 2 zu streamen (`with fs_pc2.open('temp/raw_data.txt', 'r') as f:`).
3. **Verarbeitung im Gateway:** PC 1 liest den Stream zeilenweise, wandelt die Zeilenumbrüche um (CRLF zu LF) und hält die verarbeiteten Daten im RAM (oder in einer lokalen Temp-Datei).
4. **Remote Write (Gateway schreibt auf PC 2 zurück):** PC 1 nutzt erneut `fsspec`, um die bereinigte Datei wieder auf PC 2 zu überschreiben oder unter neuem Namen abzulegen (`with fs_pc2.open('temp/clean_data.txt', 'w') as f:`).
5. **Abschluss:** PC 1 meldet PC 2 per HTTP-Response oder separatem Call: "Konvertierung abgeschlossen, Datei liegt unter `clean_data.txt`".

## 5. Weitere sinnvolle Informationen für die Weiterarbeit
- **Bidirektionales fsspec:** Da nun beide Seiten als VFS-Server (FastAPI) und VFS-Client (`fsspec`) agieren, ist der Code auf beiden Seiten sehr symmetrisch. Es empfiehlt sich, eine gemeinsame Python-Bibliothek oder ein Modul für beide PCs zu schreiben, das die FastAPI-Routen für `GET/PUT /files` bereitstellt.
- **Sicherheit und Isolation:** PC 2 muss sein freigegebenes Dateisystem streng auf einen bestimmten Workspace-Ordner limitieren (z. B. `./service_workspace/`). Ansonsten könnte ein kompromittierter Gateway kritische Systemdateien auf PC 2 auslesen oder überschreiben. **Path Traversal Protection** ist auf *beiden* Seiten zwingend erforderlich.
- **Streaming-Effizienz:** Die Konvertierung (z.B. CRLF nach LF) kann auf dem Gateway "on the fly" passieren. PC 1 liest einen Chunk von PC 2, konvertiert ihn und schreibt ihn direkt als Chunk auf das eigene Laufwerk oder streamt ihn direkt wieder zu PC 2 zurück. Das verhindert Memory-Leaks bei riesigen Log-Dateien.
- **Locking/Concurrency:** Wenn beide Systeme gleichzeitig auf dieselbe Datei auf PC 2 zugreifen wollen, kann es zu Schreibkonflikten kommen. Es sollte überlegt werden, ob Dateien während der Bearbeitung durch den Gateway mit einem Suffix (z.B. `.lock` oder `.processing`) versehen werden.
