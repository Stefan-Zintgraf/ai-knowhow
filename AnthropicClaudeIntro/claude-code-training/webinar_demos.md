# Webinar Demo Scripts

## Demo 1: Zero to Hero (Web App)
**Directory**: `~/temp/lyrics-demo` (Create fresh)

**Script**:
1.  `mkdir -p ~/temp/lyrics-demo && cd ~/temp/lyrics-demo`
2.  `claude`
3.  **Prompt**: "Create a simple web app that displays a song's lyrics. It should have a clean, dark-mode interface. Include Next and Previous buttons to cycle through lines, and a big Play/Pause button that auto-advances the lyrics every 3 seconds."
4.  *Wait for generation.*
5.  Run `python3 -m http.server` (or `npx serve`) and open the localhost URL.
6.  **Refinement**: "This is great. Please add a progress bar at the bottom showing how far we are through the song."
7.  *Show the updated UI.*
8.  **Add Playwright MCP**: `claude mcp add playwright -- npx -y @anthropic-ai/mcp-server-playwright`
9.  **Test the UI**: "Use the Playwright MCP to test the lyrics display app. Verify that the Next/Previous buttons work and that auto-play advances the lyrics correctly."
10. *Show the generated test running against the app.*

**Key Talking Points**:
- No boilerplate setup needed.
- CSS/JS handled automatically.
- Iterative refinement flow.
- MCP extends Claude's capabilities (Playwright for UI testing).

---

## Demo 2: Legacy Code Analysis
**Directory**: `exercises/java/shopping-service`

**Script**:
1.  `cd exercises/java/shopping-service`
2.  `claude`
3.  **Prompt**: "Analyze this project. What framework is it using and what is the main business logic?"
4.  *Highlight the analysis.*
5.  **Visualize**: "Create a Mermaid diagram showing the high-level architecture of the system and how the components interact."
6.  *Show the rendered Mermaid diagram in the terminal.*
7.  **Branch first**: `git checkout -b demo-refactor`
8.  **Refactor**: "The `updateProduct` method in ProductService.groovy is messy. Please refactor it to be more readable and robust using modern idioms."
9.  *Show diff.*
10. **Test**: "Generate a Spock specification (unit test) for this service."
11. **Custom Slash Command**: "Now let me show you how to automate common workflows."
12. Show the `/commit` command: Type `/commit` to demonstrate a custom slash command that creates a conventional commit message.
13. *Explain that teams can share commands via `.claude/commands/` in the repo.*

**Key Talking Points**:
- Polyglot support (Java/Groovy).
- Understanding legacy frameworks.
- Branch-first workflow for safe experimentation.
- Custom slash commands automate repetitive tasks.

---

## Demo 2.5: Security Review with Skills
**Directory**: `exercises/python/flask-api`

**Script**:
1.  `cd exercises/python/flask-api`
2.  `claude`
3.  **Set the stage**: "This is a Flask API that was written quickly. Let's see if there are any security issues."
4.  **Invoke the Skill**: "Use the security-review skill to audit this codebase."
5.  *Watch Claude identify vulnerabilities with severity ratings.*
6.  *Highlight a critical finding (likely SQL injection or hardcoded secrets).*
7.  **Fix one issue**: "Fix the most critical vulnerability you found."
8.  *Show the diff with the remediation.*

**Key Talking Points**:
- **Skills** provide domain expertise and structured workflows.
- Skills live in `.claude/skills/` and can be shared across teams.
- Security review catches issues before they reach production.
- Skills vs Slash Commands: Skills provide richer context and guidance.

---

## Demo 3: Advanced Agentic Workflows
**Directory**: `exercises/python/weather-app`

**Script**:
1.  `cd exercises/python/weather-app`
2.  `claude`
3.  **Live Test**: "My `OPENWEATHERMAP_API_KEY` environment variable is set. Fetch the current weather for Boston to verify the API works."
4.  *Show the live API response.*
5.  **Enable Plan Mode**: Press `Shift+Tab+Tab`.
6.  **Prompt**: "Plan a comprehensive update:
    1. Add a retry mechanism to the API calls.
    2. Cache the weather results in a local JSON file to avoid hitting the API too often.
    Use the Context7 MCP to check the latest docs for 'tenacity' (a Python retry library)."
7.  *Walk through the plan that Claude proposes.*
8.  *Approve and execute the plan.*
9.  *Show the resulting changes and verify the app still works.*

**Key Talking Points**:
- **Plan Mode**: Think before acting on complex changes.
- **Context7 MCP**: Fetching up-to-date library documentation.
- **Human-in-the-loop**: You approve the plan before execution.


