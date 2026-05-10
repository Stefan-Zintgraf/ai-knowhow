---
theme: seriph
background: https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80
addons:
  - slidev-component-progress
  - slidev-addon-asciinema
  - slidev-addon-qrcode
  - slidev-addon-bluesky
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Claude Code Webinar
  
  By Kenneth Kousen
  
  Learn more at [KouseniT](https://kousenit.com)
drawings:
  persist: false
transition: slide-left
title: "Claude Code: The Highlights"
mdc: true
slidev:
  slide-number: true
  controls: true
  progress: true
css: unocss
---

<style>
.slidev-page-num {
  display: block !important;
  opacity: 1 !important;
  visibility: visible !important;
  position: fixed !important;
  bottom: 1rem !important;
  right: 1rem !important;
  z-index: 100 !important;
  color: #666 !important;
  font-size: 0.875rem !important;
}
.tip-box {
  background: rgba(59, 130, 246, 0.35);
  border: 1px solid rgba(59, 130, 246, 0.6);
  border-left: 4px solid #3b82f6;
  padding: 1rem 1.25rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}
.tip-box code {
  background: rgba(255, 255, 255, 0.15);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
}
</style>

# Claude Code: The Highlights
## Accelerating Development with AI

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---

# About the Instructor

**Ken Kousen**<br>
*Java Champion*<br>
*Professor of Practice, CS Dept., Trinity College (Hartford, CT)*

- Authorship:
    - *Help Your Boss Help You*
    - *Mockito Made Clear*
    - *Modern Java Recipes*
    - *Gradle Recipes for Android*
    - *Kotlin Cookbook*
    - *Making Java Groovy*
- **Kousen IT, Inc.** (Training & Consulting)

---

# What is Claude Code?

<v-clicks>

- **Command-line AI tool** that lives in your terminal
- **Context-aware**: Understands your entire project structure
- **Agentic**: Can plan, execute, debug, and verify work
- **Integrated**: Works directly with your git, filesystem, and tools
- **Secure**: Designed for enterprise workflows

</v-clicks>

---

# Pricing Plans

<v-clicks>

- **Pro Plan** ($20/month)
  - Good for light usage (~10-40 prompts/5h)
- **Max Plan 5x** ($100/month)
  - Serious development (~50-200 prompts/5h)
- **Max Plan 20x** ($200/month)
  - Heavy agentic workflows (~200-800 prompts/5h)

</v-clicks>

<v-click>

<div class="tip-box">
  <strong>TIP:</strong> Use <code>Sonnet</code> for speed and cost-efficiency. Use <code>Opus</code> for complex planning.
</div>

</v-click>

---

# Core Productivity Features

<v-clicks>

- **Exploration**: "Explain how the authentication flow works"
- **Refactoring**: "Extract this logic into a separate service"
- **Testing**: "Generate edge-case tests for this class"
- **Debugging**: "Analyze this stack trace and fix the issue"
- **Git Integration**: "Commit these changes with a conventional message"

</v-clicks>

---
layout: section
---

# Demo 1: The "Magical" Start
## Building a Web App from Scratch

---

# Demo 1 Recap

<v-clicks>

- **Started from nothing**: Empty directory
- **Natural Language**: Defined requirements in English
- **Multi-file creation**: HTML, CSS, JS created instantly
- **Iterative Refinement**: Added features based on visual feedback
- **MCP Integration**: Playwright for automated UI testing

</v-clicks>

---
layout: section
---

# Demo 2: Taming Legacy Code
## Understanding & Refactoring Java

---

# Demo 2 Recap

<v-clicks>

- **Architecture Analysis**: Claude understood the Spring/Groovy structure
- **Intelligent Refactoring**: Modernized code while preserving logic
- **Test Generation**: Created safeguards before changing code
- **Slash Commands**: Automate repetitive workflows like commits

</v-clicks>

---
layout: section
---

# Demo 2.5: Security Review
## Skills in Action

---

# Demo 2.5 Recap

<v-clicks>

- **Skills**: Domain expertise packaged as reusable workflows
- **Security Review**: OWASP-based vulnerability scanning
- **Actionable Output**: Severity ratings + remediation code
- **Team Sharing**: Skills live in `.claude/skills/`

</v-clicks>

---
layout: section
---

# Demo 3: Advanced Workflows
## Plan Mode & MCP

---

# Advanced Features: Plan Mode

<v-clicks>

- **Shift+Tab+Tab** to enter Plan Mode
- **Subagents**:
    - **Planner**: Breaks down complex tasks
    - **Explorer**: Gathers necessary context
    - **Coder**: Implements the changes
    - **Tester**: Verifies the implementation
- **Human-in-the-loop**: You approve the plan before execution

</v-clicks>

---

# Extended Capabilities: MCP

**Model Context Protocol (MCP)** connects Claude to your tools.

<v-clicks>

- **Context7**: Fetch real-time library documentation
- **PostgreSQL**: Query your database directly
- **GitHub**: Manage issues and PRs
- **Custom Servers**: Connect to your internal APIs

</v-clicks>

---

# Key Takeaways

<v-clicks>

1.  **Speed**: Bootstrap projects in minutes, not hours.
2.  **Understanding**: Dive into legacy code with an expert pair programmer.
3.  **Power**: Orchestrate complex workflows with Plan Mode.
4.  **Control**: You are always in the driver's seat.

</v-clicks>

---

# Q&A

Thank you!

- **Email**: ken.kousen@kousenit.com
- **Website**: https://kousenit.com
- **Newsletter**: https://kenkousen.substack.com

