# Claude Code Training Course

A comprehensive training presentation and hands-on lab exercises for using Claude Code in professional software development workflows.

## 🎯 What You'll Learn

This course teaches professional developers how to:
- Create complete projects from scratch using Claude Code
- Navigate and understand complex codebases with AI assistance
- Implement the "branch-first" workflow for safe experimentation
- Generate comprehensive tests and documentation
- Refactor legacy code and modernize applications
- Use advanced Claude Code features like Plan Mode and custom commands
- Extend capabilities with Skills and Plugins for specialized workflows
- Customize output styles for different learning preferences
- Understand and leverage subagents for complex multi-step tasks
- Implement sophisticated automation with hooks and event-driven workflows

## 🚀 Course Materials

This repository contains all the materials for the Claude Code Training course:

- **`slides.md`**: The main Slidev presentation with interactive demos
- **`lab_handout.md`**: Progressive hands-on labs from beginner to advanced
- **`instructor-guide.md`**: Instructor-led demos and exercises using real codebases
- **`half-day-outline.md`**: Condensed outline for half-day training sessions
- **`events/`**: Event-specific descriptions and course configurations
- **`custom-commands.md`**: Showcase of powerful custom slash commands for workflow automation
- **`commands/`**: Ready-to-use custom command files for students
- **`skills-and-plugins/`**: Examples of custom skills and plugin configurations
- **`hooks-examples/`**: Advanced hook patterns for workflow automation
- **`exercises/`**: A collection of diverse sample projects:
  - **Python**: Flask web app (`weather-app`) and legacy API (`flask-api`)
  - **JavaScript/TypeScript**: Interactive web application (`lyrics-trainer`)
  - **Java**: Modern Spring Boot service (`certificate-service`) and legacy Grails app (`shopping-service`)

## 🏃‍♀️ Running the Presentation

1.  **Install dependencies:**
    ```bash
    pnpm install
    ```

2.  **Start the presentation:**
    ```bash
    pnpm dev
    ```

3.  Open your browser at <http://localhost:3030>

## 📚 Getting Started with the Labs

### Prerequisites
- Claude Code installed and configured
- API key set: `export ANTHROPIC_API_KEY="your-key"`
- Development environment for Python, JavaScript/TypeScript, and Java
- VS Code (optional, for IDE integration demonstrations)
- Docker (optional, for MCP and containerized workflow examples)

### Lab Structure
The `lab_handout.md` contains six progressive labs:

0. **Project Creation from Scratch** - Build a lyrics display app (recreates the `lyrics-trainer` origin story)
1. **Claude Code Basics** - Interface and project exploration
2. **Code Exploration** - Understanding complex codebases
3. **Test Generation** - Automated testing with AI
4. **Documentation Creation** - Professional documentation workflows
5. **Legacy Code Refactoring** - Modernizing Grails/Groovy applications
6. **Advanced Workflows** - Plan Mode, Skills, Plugins, Output Styles, Hooks, CLAUDE.md, and custom commands

### Custom Commands
Students can explore and use pre-built custom slash commands:
- Copy commands from `commands/` to `~/.claude/commands/`
- See `custom-commands.md` for detailed explanations and usage examples
- Commands include Java modernization, Spring generators, security reviews, and more

### Teaching Notes
The `instructor-guide.md` file contains detailed instructor guidance with specific prompts and a progressive story arc using the `flask-api` project as the primary demonstration vehicle.

## 🏗️ Course Philosophy

- **Branch-First Workflow**: Emphasizes safe experimentation through Git branching
- **Practical Learning**: Real-world projects across multiple languages and frameworks
- **Progressive Complexity**: From simple tasks to advanced enterprise workflows
- **Best Practices**: Professional development patterns and security considerations
- **Extensibility First**: Skills and plugins provide persistent, reusable domain expertise
- **Adaptive Learning**: Output styles and hooks adapt to diverse learning contexts
- **Intelligent Automation**: Subagents handle specialized tasks automatically for optimal performance

## 👤 Author

**Ken Kousen**
- Email: ken.kousen@kousenit.com
- Website: kousenit.com
- Course: Professional Claude Code Training
