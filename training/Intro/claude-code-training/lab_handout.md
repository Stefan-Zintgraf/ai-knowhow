# Claude Code Training Labs

This document contains hands-on exercises for learning to use Claude Code for professional development workflows.

## Table of Contents

0. [Lab 0: Project Creation from Scratch](#lab-0-project-creation-from-scratch)
1. [Lab 1: First Steps with Claude Code](#lab-1-first-steps-with-claude-code)
2. [Lab 2: Code Exploration](#lab-2-code-exploration)
3. [Lab 3: Test Generation](#lab-3-test-generation)
4. [Lab 4: Documentation Creation](#lab-4-documentation-creation)
5. [Lab 5: Legacy Code Refactoring](#lab-5-legacy-code-refactoring)
6. [Lab 6: Advanced Workflows](#lab-6-advanced-workflows)

## Prerequisites

- Claude Code installed and configured
- API key set in environment: `export ANTHROPIC_API_KEY="your-key"`
- Git repository access
- Development environment for multiple languages (Python, JavaScript/TypeScript, Java)

## Lab 0: Project Creation from Scratch

**Duration**: 20 minutes  
**Goal**: Create a lyrics display application from scratch (this is how the `lyrics-trainer` project began, which we'll look at later)

### Setup

1. Create a new empty directory: `mkdir lyrics-display && cd lyrics-display`
2. Initialize git: `git init`
3. Start Claude Code: `claude`
4. Create your first branch: `git checkout -b basic-lyrics-app`
5. Find song lyrics: Google any song title + "lyrics" and copy the lyrics to a text file called `lyrics.txt`. Or use the sample provided in the repo root:
   ```bash
   cp ../wichita_lineman_lyrics.txt lyrics.txt
   ```

### Exercises

1. **Project foundation**:
   ```
   I have song lyrics saved in lyrics.txt. Create a web application that displays these lyrics one line at a time with three buttons: Next, Previous, and Play. The Play button should automatically advance through lines with a 2-second delay.
   ```

2. **Enhanced functionality**:
   ```
   Add line numbering, show progress (e.g., 'Line 5 of 32'), and make the Play button toggle to Pause when active. Style it to look modern and clean.
   ```

3. **Visual improvements**:
   ```
   Add smooth transitions between lines, better typography, and responsive design. Make it visually appealing with a music-themed color scheme.
   ```

4. **Advanced features**:
   ```
   Add keyboard shortcuts: spacebar for play/pause, arrow keys for next/previous. Also add a progress bar showing position in the song.
   ```

5. **Documentation and structure**:
   ```
   Create a README.md explaining the project, and organize the code into separate CSS and JavaScript files for better maintainability.
   ```

6. **Version control and experimentation**:
   ```
   Help me commit this work, then create a new branch called 'speed-control' and add a slider to control the playback speed.
   ```

### Expected Outcomes

- Build a real, useful application from nothing
- See how Claude Code handles file interactions and user interface logic
- Experience the full development cycle: concept → working app → enhancements
- Understand that this is exactly how the `lyrics-trainer` project started
- Practice iterative development with AI assistance

**Note**: This exercise recreates the origin story of the `lyrics-trainer` project in the exercises folder - you're experiencing the same process that created one of our example applications!

[← Back to Table of Contents](#table-of-contents)

## Lab 1: First Steps with Claude Code

**Duration**: 5 minutes
**Goal**: Get comfortable with the basic Claude Code interface

### Setup

1. Navigate to any existing project directory
2. Start Claude Code: `claude`
3. Verify the interface responds to basic commands

### Exercises

1. **Basic interaction**: Ask Claude Code to explain what it can do
   ```
   What are your main capabilities for helping with development?
   ```

2. **Project overview**: Get a high-level understanding
   ```
   Give me an overview of this project structure
   ```

3. **File exploration**: Find specific files
   ```
   Show me the main application files in this project
   ```

### Expected Outcomes

- Understand Claude Code's conversational interface
- See how it analyzes project structure
- Practice natural language interaction

[← Back to Table of Contents](#table-of-contents)

## Lab 2: Code Exploration

**Duration**: 10 minutes  
**Goal**: Use Claude Code to understand a complex codebase

### Setup

Choose one of the provided exercise projects:
- `exercises/java/certificate-service` (Spring Boot PDF generation)
- `exercises/java/shopping-service` (Legacy Grails/Groovy application)
- `exercises/javascript/lyrics-trainer` (TypeScript web app)
- `exercises/python/weather-app` (Flask application)

### Exercises

1. **Architecture analysis**: 
   ```
   Analyze the architecture of this application and explain the main components
   ```

2. **Technology stack identification**:
   ```
   What frameworks and libraries does this project use?
   ```

3. **Entry point discovery**:
   ```
   Show me the main entry points and how the application starts
   ```

4. **Configuration analysis**:
   ```
   Explain the configuration files and their purposes
   ```

5. **Dependency mapping**:
   ```
   Trace the flow from the main controller to the service layer
   ```

### Expected Outcomes

- Quickly understand unfamiliar codebases
- Identify key architectural patterns
- Learn to ask effective exploration questions

[← Back to Table of Contents](#table-of-contents)

## Lab 3: Test Generation

**Duration**: 15 minutes  
**Goal**: Generate comprehensive test suites with Claude Code

### Setup

Use the same project from Lab 2, focusing on service classes or core business logic.

### Exercises

1. **Unit test generation**:
   ```
   Create unit tests for the [ServiceName] class with comprehensive coverage
   ```

2. **Edge case identification**:
   ```
   What edge cases should I test for the [methodName] method? Generate tests for them
   ```

3. **Integration test creation**:
   ```
   Create integration tests for the [ControllerName] that test the full request/response cycle
   ```

4. **Mock setup**:
   ```
   Generate tests with proper mocking for external dependencies
   ```

5. **Test data generation**:
   ```
   Create realistic test data and fixtures for these test cases
   ```

### Expected Outcomes

- Understand automated test generation
- Learn about edge case identification
- Practice test-driven development with AI assistance

[← Back to Table of Contents](#table-of-contents)

## Lab 4: Documentation Creation

**Duration**: 15 minutes  
**Goal**: Generate professional documentation with Claude Code

### Setup

Continue with your chosen project, focusing on undocumented areas.

### Exercises

1. **README generation**:
   ```
   Create a comprehensive README file for this project including setup, usage, and examples
   ```

2. **API documentation**:
   ```
   Generate API documentation for all the REST endpoints in this application
   ```

3. **Code comments**:
   ```
   Add meaningful JavaDoc/docstring comments to the main service classes
   ```

4. **Architecture documentation**:
   ```
   Create an architectural overview document explaining the system design
   ```

5. **Troubleshooting guide**:
   ```
   Generate a troubleshooting guide for common issues with this application
   ```

### Expected Outcomes

- Create professional-quality documentation
- Learn different documentation formats
- Understand how to maintain documentation

[← Back to Table of Contents](#table-of-contents)

## Lab 5: Legacy Code Refactoring

**Duration**: 15 minutes  
**Goal**: Modernize legacy code using Claude Code assistance

### Setup

Use the `exercises/java/shopping-service` (Grails/Groovy) project or any legacy code you have available.

### Exercises

1. **Code modernization**:
   ```
   Refactor this class to use modern Java features like records, switch expressions, and optional
   ```

2. **Spring Boot updates**:
   ```
   Update this Spring configuration to use modern Spring Boot patterns and annotations
   ```

3. **Exception handling improvement**:
   ```
   Improve the error handling in this service class with proper exception types and messages
   ```

4. **Performance optimization**:
   ```
   Review this code for performance issues and suggest optimizations
   ```

5. **Security review**:
   ```
   Review this controller for security vulnerabilities and suggest fixes
   ```

### Expected Outcomes

- Learn systematic refactoring approaches
- Understand modern development patterns
- Practice security-focused code review

[← Back to Table of Contents](#table-of-contents)

## Lab 6: Advanced Workflows

**Duration**: 60 minutes
**Goal**: Master advanced Claude Code features including Plan Mode, Skills, Plugins, Output Styles, Hooks, MCP, Agent Teams, and Surfaces

### Setup

Navigate to the `exercises/python/weather-app` directory for this lab.

### Exercises

#### Part A: Plan Mode and Subagents (5 minutes)

1. **Plan Mode usage**:
   - Type `/plan` to activate Plan Mode (or cycle with `Shift+Tab`)
   ```
   Plan a comprehensive improvement to add error handling and logging to this Flask application
   ```
   - Review the plan before execution
   - Observe that Plan Mode uses the Plan subagent
   - Execute step by step or approve the entire plan

2. **Understanding Subagents and Effort Levels**:
   ```
   Explain which subagents you use and when they activate automatically
   ```
   - Learn about Explore, Plan, and General-purpose subagents
   - Understand how Claude selects the right agent for each task
   - **Effort levels**: `/effort low|medium|high` controls reasoning depth
   - **Keyboard shortcuts**: `Alt+P` switches models mid-conversation

#### Part B: Skills and Plugins (15 minutes)

> **Note**: Skills (`.claude/skills/`) are the primary extensibility mechanism. Custom slash commands (`.claude/commands/`) remain as a lightweight alternative. Skills support YAML frontmatter for `effort`, `model`, `paths`, and more. Hot-reload — edit a SKILL.md and changes take effect immediately.

3. **Explore Built-in Skills**:
   ```
   Create a quarterly weather report as an Excel spreadsheet with charts showing temperature trends
   ```
   - The xlsx skill will activate automatically
   - Observe how skills load progressively

4. **Install and Test a Custom Skill**:
   ```bash
   # Copy example skill to your local skills directory
   # (Run from the claude-code-training project root)
   cp -r skills-and-plugins/api-documentation-skill ~/.claude/skills/
   ```

   Then ask:
   ```
   Generate comprehensive API documentation for the weather app's REST endpoints
   ```
   - The API Documentation skill should activate
   - Review the generated documentation format

5. **Create Your Own Skill**:
   ```
   Help me create a custom skill for Python Flask best practices that includes:
   - Constructor injection patterns
   - Error handling conventions
   - Logging standards
   - Testing requirements
   Save it to ~/.claude/skills/flask-best-practices/
   ```

6. **Explore Plugins** (Discussion):
   - Review `skills-and-plugins/plugin-examples/team-standards-plugin.md` (from project root)
   - Discuss how plugins bundle commands, skills, hooks, and MCP servers
   - Understand use cases for team-wide plugin distribution

#### Part C: Output Styles (5 minutes)

7. **Test Built-in Output Styles**:
   ```bash
   # Exit current session, start with explanatory style
   claude --output-style explanatory
   ```

   Ask the same question twice with different styles:
   ```
   Explain how the weather API integration works
   ```

   Exit and try learning style:
   ```bash
   claude --output-style learning
   ```
   ```
   Explain how the weather API integration works
   ```
   - Compare the verbosity and teaching approach

8. **Create Custom Output Style**:
   ```
   Help me create a custom output style called 'production' that:
   - Is concise and action-focused
   - Skips explanations unless asked
   - Assumes expert-level knowledge
   - Shows code without preambles
   Save it to ~/.claude/output-styles/production.md
   ```

#### Part D: Hooks and Automation (10 minutes)

9. **Configure a SessionEnd Hook**:
   ```bash
   # Copy example hook (run from project root)
   mkdir -p ~/.claude/hooks
   cp hooks-examples/session-end-summary.sh ~/.claude/hooks/
   chmod +x ~/.claude/hooks/session-end-summary.sh
   ```

   Then configure it:
   ```
   Add a SessionEnd hook to my ~/.claude/settings.json that runs ~/.claude/hooks/session-end-summary.sh using the current hook array format
   ```

10. **Test PreToolUse Hook** - Security Validator:
   ```bash
   # Copy security hook (run from project root)
   cp hooks-examples/security-validator.sh ~/.claude/hooks/
   chmod +x ~/.claude/hooks/security-validator.sh
   ```

   Configure it:
   ```
   Add a PreToolUse hook for Write operations that runs ~/.claude/hooks/security-validator.sh to check for hardcoded secrets. Use the current hook array format with an "if" matcher.
   ```

   Test it:
   ```
   Create a config file with: API_KEY = 'sk_live_1234567890abcdef'
   ```
   - The hook should block this and explain why
   - Try again with environment variable approach

11. **Create Your Own Hook**:
   ```
   Create a hook that runs prettier to auto-format Python files before any Edit operation. Save it to ~/.claude/hooks/format-python.sh
   ```

#### Part E: MCP Server Integration (5 minutes)

> **Note**: MCP Tool Search (lazy loading) is now enabled by default. Instead of loading all tool definitions upfront, Claude discovers tools on demand — reducing context usage by ~95% with many MCP tools.

12. **List and Explore MCP Servers**:
   ```bash
   # List currently configured MCP servers
   claude mcp list
   ```

   Then in Claude Code:
   ```
   What MCP servers are available and what tools do they provide?
   ```

13. **Add Context7 MCP Server** (for up-to-date documentation):
   ```bash
   # Add Context7 for fetching latest library docs
   claude mcp add --transport http context7 https://mcp.context7.com/mcp
   ```

   Test it:
   ```
   Using Context7, look up the latest Flask documentation for error handling
   ```

14. **Import from Claude Desktop** (if you have Claude Desktop installed):
   ```bash
   # Import any MCP servers configured in Claude Desktop
   claude mcp add-from-claude-desktop
   ```

15. **Explore MCP Tools**:
   ```
   Show me what tools are available from the MCP servers and demonstrate one
   ```
   - Observe how MCP extends Claude's capabilities
   - Note the `mcp__` prefix on tool names

#### Part F: CLAUDE.md and Custom Commands (5 minutes)

16. **CLAUDE.md creation**:
   ```
   Create a CLAUDE.md file for this weather app with Python coding standards, dependencies, and project context
   ```

   Note that the built-in slash command `/init` creates the `CLAUDE.md` file, but you can simply ask Claude to create it.

17. **Custom slash command**:
   ```
   Help me create a custom slash command called 'update-deps' for updating Python dependencies safely with backup and testing
   ```

#### Part G: Feature Enhancement with All Tools (5 minutes)

18. **Comprehensive Enhancement**:

   Now use Plan Mode with all your new tools:
   ```
   Using Plan Mode, add comprehensive error handling and structured logging to this application. The security hook should verify no secrets are added, and generate API documentation using the skill when done.
   ```

   - Observe how multiple advanced features work together
   - Note subagent selection, skill activation, and hook execution

#### Part H: Agent Teams (10 minutes)

> **Note**: Agent Teams is a research preview feature. Enable it with:
> ```bash
> export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
> ```

19. **Launch an Agent Team**:

   Navigate to the `exercises/java/certificate-service` directory:
   ```
   Create a team of agents to improve this project. One agent should review
   the test suite and identify coverage gaps, another should review the code
   for security issues, and a third should update the documentation.
   Coordinate the work and give me a summary when done.
   ```

   Observe:
   - The lead agent creates a task list and assigns teammates
   - Each teammate works independently in its own context
   - Teammates report back as they complete tasks
   - The lead agent synthesizes results

20. **Monitor Team Progress**:

   While the team works, observe:
   - Task status updates in the output
   - Inter-agent messages (DMs between teammates)
   - How idle teammates wake up when assigned new work
   - The shared task list with dependencies

21. **Simpler Team Exercise** (alternative if time is short):
   ```
   Create a team with two agents: one to add input validation to the
   certificate controller, and another to write tests for that validation.
   The test agent should wait until the validation agent finishes.
   ```

   This demonstrates task dependencies (`blocks`/`blockedBy`).

22. **Background Agents and Worktree Isolation**:
   ```bash
   # Start Claude in an isolated worktree
   claude -w
   ```
   ```
   Refactor the PdfService to use the builder pattern, then run all tests
   ```
   - Notice you're on a separate branch in an isolated directory
   - Changes don't affect your main working tree
   - On exit, you'll be asked to keep or remove the worktree

#### Part I: Surfaces & Remote Workflows (10 minutes, optional)

23. **Explore `/powerup`** (Self-learning):
   ```
   /powerup
   ```
   - Browse interactive lessons on Claude Code features
   - Try a lesson on a feature you haven't used before

24. **Try Remote Session** (if claude.ai/code access available):
   ```bash
   # Start a cloud session from your terminal
   claude --remote "Analyze the weather-app for potential performance improvements"
   ```
   - Observe the session running on Anthropic cloud
   - Visit claude.ai/code to see the session in browser
   - Try `/teleport` to pull it back to your terminal

25. **Discussion: Surfaces & Dispatch**:
   - Review the 5 surfaces: CLI, VS Code, JetBrains, Desktop app, Web
   - Discuss Dispatch: sending tasks from phone to desktop
   - When would you use each surface?
   - How do scheduled tasks differ across surfaces?

### Expected Outcomes

After completing this lab, you will:
- Master Plan Mode and understand subagent architecture
- Know when and how to use Skills for domain expertise
- Understand plugin system for team collaboration
- Customize output styles for different contexts
- Implement hooks for workflow automation
- Configure and use MCP servers for extended capabilities
- Create reusable project configurations with CLAUDE.md
- Build custom slash commands for common workflows
- Orchestrate multiple advanced features together
- **Launch and coordinate Agent Teams for parallel work**
- **Use worktree isolation for safe experimentation**
- **Run background agents for concurrent workflows**
- **Understand the 5 Claude Code surfaces and when to use each**
- **Use `/powerup` for self-directed feature learning**

### Troubleshooting

**Skills not activating?**
- Check that SKILL.md has proper YAML frontmatter
- Verify skill directory is in `~/.claude/skills/`
- Ask Claude if the skill loaded: `/skills list` (if available)

**Hooks not running?**
- Verify hook script has execute permissions: `chmod +x hook.sh`
- Check settings.json syntax is valid JSON
- Review hook output - errors appear as user messages

**Output style not changing?**
- Verify file is in `~/.claude/output-styles/`
- Check YAML frontmatter format
- Restart claude with `--output-style` flag

**MCP servers not working?**
- Run `claude mcp list` to verify server is configured
- Check that remote servers are accessible (network/firewall)
- For local servers, verify the command exists and is executable
- Restart Claude Code after adding new MCP servers
- Note: MCP Tool Search (lazy loading) means tools aren't visible until used

**Agent Teams not starting?**
- Verify the environment variable: `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
- Must be set to `1` before starting Claude Code
- Teams require sufficient plan credits (each teammate uses tokens independently)
- If teammates seem stuck, the lead agent will typically retry or reassign

**Worktree issues?**
- Must be in a git repository to use `claude -w`
- Worktree is created under `.claude/worktrees/` in the repo
- If a worktree wasn't cleaned up, use `git worktree list` and `git worktree remove`

[← Back to Table of Contents](#table-of-contents)

## Tips for Success

### Effective Prompting
- Be specific about what you want to achieve
- Provide context about your goals and constraints
- Use iterative refinement for complex tasks
- Include examples when possible

### Best Practices
- Start with clean git state before major changes
- Commit checkpoints regularly during development
- Review all AI-generated code before accepting
- Test generated code thoroughly

### Common Issues and Solutions

**Issue**: Claude Code doesn't understand the project  
**Solution**: Ask it to explore the project first: "Analyze this project structure"

**Issue**: Generated code doesn't follow project conventions  
**Solution**: Create a CLAUDE.md file with your coding standards

**Issue**: Tests fail after code generation  
**Solution**: Ask Claude to fix: "These tests are failing, please analyze and fix them"

**Issue**: Code is too verbose or not optimized  
**Solution**: Request refinement: "Make this code more concise and efficient"

## Next Steps

After completing these labs:

1. **Practice regularly**: Use Claude Code for daily development tasks
2. **Share with team**: Introduce colleagues to effective workflows
3. **Customize**: Create project-specific CLAUDE.md files and slash commands
4. **Iterate**: Refine your prompting techniques based on results
5. **Stay updated**: Follow Claude Code updates and new features

## Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Best Practices Guide](https://www.anthropic.com/engineering/claude-code-best-practices)
- [MCP Server Directory](https://github.com/modelcontextprotocol/servers)