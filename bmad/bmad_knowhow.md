# BMad Know-How

This document is a know how document, how to work with BMad.

---

## Table of Contents

1. [Installation](#1-installation)
   - [1.1 Prerequisites](#11-prerequisites)
   - [1.2 Installation](#12-installation)
   - [1.3 Installing Custom Modules](#13-installing-custom-modules)
   - [1.4 Troubleshooting](#14-troubleshooting)
   - [1.5 Quick Path](#15-quick-path)
2. [Workflows](#2-workflows)
   - [Workflow Organization](#workflow-organization)
   - [Phase 1: Analysis (Optional)](#phase-1-analysis-optional)
   - [Phase 2: Planning (Required)](#phase-2-planning-required)
   - [Phase 3: Solutioning (BMad Method/Enterprise Only)](#phase-3-solutioning-bmad-methodenterprise-only)
   - [Phase 4: Implementation](#phase-4-implementation)
   - [Testing & Quality Workflows (TEA Agent)](#testing--quality-workflows-tea-agent)
   - [Setup & Configuration Workflows](#setup--configuration-workflows)
   - [Planning Tracks](#planning-tracks)
   - [Typical Workflow Sequence](#typical-workflow-sequence)
   - [Key Principles](#key-principles)
   - [Documentation](#documentation)
3. [Brownfield Development](#3-brownfield-development)
   - [3.1 What is Brownfield Development?](#31-what-is-brownfield-development)
   - [3.2 Initial Setup](#32-initial-setup)
   - [3.3 Documenting Existing Projects](#33-documenting-existing-projects)
   - [3.4 Adding Features to Existing Projects](#34-adding-features-to-existing-projects)
   - [3.5 Quick Fixes and Ad-Hoc Changes](#35-quick-fixes-and-ad-hoc-changes)
   - [3.6 Best Practices](#36-best-practices)
4. [Document Sharding](#4-document-sharding)
   - [4.1 Introduction](#41-introduction)
   - [4.2 When to Shard Documents](#42-when-to-shard-documents)
   - [4.3 Sharding Workflow](#43-sharding-workflow)
   - [4.4 Best Practices](#44-best-practices)
5. [Agent Customization](#5-agent-customization)
   - [5.1 Introduction](#51-introduction)
   - [5.2 When to Customize Agents](#52-when-to-customize-agents)
   - [5.3 How to Customize Agents](#53-how-to-customize-agents)
   - [5.4 Integration into Workflows](#54-integration-into-workflows)
   - [5.5 Best Practices](#55-best-practices)
   - [5.6 Example: Healthcare Compliance Agent](#56-example-healthcare-compliance-agent)
   - [5.7 Example: Code Review Agent](#57-example-code-review-agent)
6. [Features & Capabilities](#6-features--capabilities)
   - [6.1 Party Mode](#61-party-mode)
   - [6.2 TEA Overview](#62-tea-overview)
   - [6.3 Quick Flow](#63-quick-flow)
   - [6.4 Advanced Elicitation](#64-advanced-elicitation)
   - [6.5 Web Bundles](#65-web-bundles)
7. [TEA Testing Strategy](#7-tea-testing-strategy)
   - [7.1 TEA Engagement Models](#71-tea-engagement-models)
   - [7.2 Choosing Your Model](#72-choosing-your-model)
   - [7.3 Practical Application](#73-practical-application)

---

## 1 Installation

### 1.1 Prerequisites

- **Node.js 20+** — Required for the installer
- **Git** — Recommended for version control
- **AI-powered IDE** — Claude Code, Cursor, Windsurf, or similar
- **A project idea** — Even a simple one works for learning

### 1.2 Installation

#### When to Use This

- Starting a new project with BMad
- Adding BMad to an existing codebase
- Updating an existing BMad installation

#### Installation Steps

**1. Run the Installer**

Open a terminal in your project directory and run:

```bash
npx bmad-method@alpha install
```

**2. Choose Installation Location**

The installer will ask where to install BMad files:

- Current directory (recommended for new projects if you created the directory yourself and ran from within the directory)
- Custom path

**3. Select Your AI Tools**

Choose which AI tools you'll be using:

- Claude Code
- Cursor
- Windsurf
- Many others to choose from

The installer configures BMad for your selected tools by setting up commands that will call the UI.

**4. Choose Modules**

Select which modules to install:

| Module   | Purpose                                   |
| -------- | ----------------------------------------- |
| **BMM**  | Core methodology for software development |
| **BMGD** | Game development workflows                |
| **CIS**  | Creative intelligence and facilitation    |
| **BMB**  | Building custom agents and workflows      |

**5. Add Custom Content (Optional)**

If you have custom agents, workflows, or modules, point to their location and the installer will integrate them.

**6. Configure Settings**

For each module, either accept recommended defaults (faster) or customize settings (more control).

#### What You Get

After installation, you'll have:

```
your-project/
├── _bmad/
│   ├── bmm/            # Method module
│   │   ├── agents/     # Agent files
│   │   ├── workflows/  # Workflow files
│   │   └── config.yaml # Module config
│   ├── core/           # Core utilities
│   └── ...
├── _bmad-output/       # Generated artifacts
└── .claude/            # IDE configuration (if using Claude Code)
```

#### Verify Installation

1. Check the `_bmad/` directory exists
2. Load an agent in your AI tool
3. Run `/workflow-init` which will autocomplete to the full command to see available commands

#### Configuration

Edit `_bmad/[module]/config.yaml` to customize. For example, these could be changed:

```yaml
output_folder: ./_bmad-output
user_name: Your Name
communication_language: english
```

### 1.3 Installing Custom Modules

Use the BMad installer to add custom agents, workflows, and modules that extend BMad's functionality.

#### When to Use This

- Adding third-party BMad modules to your project
- Installing your own custom agents or workflows
- Sharing custom content across projects or teams

#### Prerequisites

- BMad installed in your project
- Custom content with a valid `module.yaml` file

#### Steps

**1. Prepare Your Custom Content**

Your custom content needs a `module.yaml` file. Choose the appropriate structure:

**For a cohesive module** (agents and workflows that work together):

```
module-code/
  module.yaml
  agents/
  workflows/
  tools/
  templates/
```

**For standalone items** (unrelated agents/workflows):

```
module-name/
  module.yaml        # Contains unitary: true
  agents/
    larry/larry.agent.md
    curly/curly.agent.md
  workflows/
```

Add `unitary: true` in your `module.yaml` to indicate items don't depend on each other.

**2. Run the Installer**

**New project:**

```bash
npx bmad-method@alpha install
```

When prompted "Would you like to install a local custom module?", select 'y' and provide the path to your module folder.

**Existing project:**

```bash
npx bmad-method@alpha install
```

1. Select `Modify BMad Installation`
2. Choose the option to add, modify, or update custom modules
3. Provide the path to your module folder

**3. Verify Installation**

Check that your custom content appears in the `_bmad/` directory and is accessible from your AI tool.

#### What You Get

- Custom agents available in your AI tool
- Custom workflows accessible via `*workflow-name`
- Content integrated with BMad's update system

#### Content Types

BMad supports several categories of custom content:

| Type                    | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| **Stand Alone Modules** | Complete modules with their own agents and workflows |
| **Add On Modules**      | Extensions that add to existing modules              |
| **Global Modules**      | Content available across all modules                 |
| **Custom Agents**       | Individual agent definitions                         |
| **Custom Workflows**    | Individual workflow definitions                      |

#### Updating Custom Content

When BMad Core or module updates are available, the quick update process:

1. Applies updates to core modules
2. Recompiles all agents with your customizations
3. Retains your custom content from cache
4. Preserves your configurations

You don't need to keep source module files locally—just point to the updated location during updates.

#### Tips

- **Use unique module codes** — Don't use `bmm` or other existing module codes
- **Avoid naming conflicts** — Each module needs a distinct code
- **Document dependencies** — Note any modules your custom content requires
- **Test in isolation** — Verify custom modules work before sharing
- **Version your content** — Track updates with version numbers

**Naming Conflicts:** Don't create custom modules with codes like `bmm` (already used by BMad Method). Each custom module needs a unique code.

#### Example Modules

Find example custom modules in the `samples/sample-custom-modules/` folder of the [BMad repository](https://github.com/bmad-code-org/BMAD-METHOD). Download either sample folder to try them out.

### 1.4 Troubleshooting

**"Command not found: npx"** — Install Node.js 20+:

```bash
brew install node
```

**"Permission denied"** — Check npm permissions:

```bash
npm config set prefix ~/.npm-global
```

**Installer hangs** — Try running with verbose output:

```bash
npx bmad-method@alpha install --verbose
```

### 1.5 Quick Path

- **Install**: `npx bmad-method@alpha install`
- **Initialize**: Load Analyst agent, run `workflow-init`
- **Plan**: PM creates PRD, Architect creates architecture
- **Build**: SM manages sprints, DEV implements stories

**Always use fresh chats** for each workflow to avoid context issues.


## 2 Workflows

This chapter provides a comprehensive overview of all workflows available in the BMad Method, organized by development phase.

### Workflow Organization

BMad workflows are organized into four main phases:

1. **Analysis** - Exploration and ideation (optional)
2. **Planning** - Requirements definition (required)
3. **Solutioning** - Architecture and breakdown (BMad Method/Enterprise only)
4. **Implementation** - Build cycle

The planning track you choose (Quick Flow, BMad Method, or Enterprise) determines which workflows are used.

---

### Phase 1: Analysis (Optional)

These workflows help explore and define the project before formal planning begins.

#### brainstorm-project
- **Agent**: Analyst
- **Purpose**: Guided ideation using 60+ brainstorming techniques
- **When to Use**: When you need to explore ideas or generate creative solutions
- **Output**: Brainstorming results and insights

#### research
- **Agent**: Analyst
- **Purpose**: Market and technical research
- **When to Use**: When you need to understand market conditions, competitors, or technical feasibility
- **Output**: Research findings

#### product-brief
- **Agent**: Analyst
- **Purpose**: Create a foundation document that captures project vision and scope
- **When to Use**: Recommended before creating a PRD for complex projects
- **Output**: Product brief document

---

### Phase 2: Planning (Required)

These workflows create the requirements documents that guide development.

#### create-prd
- **Agent**: PM (Product Manager)
- **Purpose**: Create a Product Requirements Document with Functional Requirements (FRs) and Non-Functional Requirements (NFRs)
- **When to Use**: 
  - Medium to large feature sets
  - Multi-screen user experiences
  - Complex business logic
  - Multiple system integrations
  - Phased delivery required
- **Track**: BMad Method, Enterprise
- **Output**: `PRD.md`

#### quick-spec
- **Agent**: PM or Barry (Quick Flow Solo Dev)
- **Purpose**: Create a quick technical specification
- **When to Use**: Simple features, bug fixes, clear scope (1-15 stories)
- **Track**: Quick Flow
- **Output**: Technical specification document
- **Note**: See [Quick Flow](#63-quick-flow) section for detailed explanation

#### bmgd-quick-flow
- **Agent**: Analyst
- **Purpose**: Quick-flow guide for simple changes
- **When to Use**: Very simple changes that don't need full planning
- **Track**: Quick Flow
- **Output**: Quick specification

#### Barry (Quick Flow Solo Dev Agent)
- **Agent**: Barry (Quick Flow Solo Dev)
- **Purpose**: Elite solo developer who takes projects from concept to deployment with ruthless efficiency
- **When to Use**: 
  - Quick Flow development (small to medium features)
  - Technical specification creation
  - Direct development when requirements are clear
  - Performance-critical features
- **Workflow**: `quick-spec` → `quick-dev` → `code-review` (optional)
- **Best For**: Rapid delivery, no handoffs, solo execution
- **See**: [Quick Flow](#63-quick-flow) section for details

#### create-ux-design
- **Agent**: UX-Designer
- **Purpose**: Create UX design specifications
- **When to Use**: Projects with user interfaces (optional)
- **Prerequisites**: PRD completed
- **Output**: UX design document

---

### Phase 3: Solutioning (BMad Method/Enterprise Only)

These workflows design the technical solution and break down work.

#### create-architecture
- **Agent**: Architect
- **Purpose**: Create system architecture with technical decisions to prevent agent conflicts during implementation
- **When to Use**: 
  - Multi-epic projects (BMad Method, Enterprise)
  - Cross-cutting technical concerns
  - Multiple agents implementing different parts
  - Integration complexity exists
  - Technology choices need alignment
- **When to Skip**: 
  - Quick Flow (simple changes)
  - BMad Method Simple with straightforward tech stack
  - Single epic with clear technical approach
- **Prerequisites**: PRD completed
- **Output**: Architecture document with technical decisions

#### create-epics-and-stories
- **Agent**: PM
- **Purpose**: Break down PRD into epics and stories (created after architecture in V6)
- **When to Use**: After architecture is complete, to create technically-informed stories
- **Prerequisites**: PRD and Architecture completed
- **Output**: Epic and story files in `epics/` directory

#### run-implementation-readiness
- **Agent**: Architect
- **Purpose**: Validate cohesion across all planning documents (highly recommended)
- **When to Use**: Before starting implementation to ensure all planning is aligned
- **Prerequisites**: PRD, Architecture, and Epics/Stories completed
- **Output**: Implementation readiness assessment

---

### Phase 4: Implementation

These workflows handle the actual building of the project.

#### sprint-planning
- **Agent**: SM (Scrum Master)
- **Purpose**: Initialize sprint tracking file and organize work for implementation
- **When to Use**: 
  - Once at the start of Phase 4 (Implementation)
  - After implementation-readiness gate passes
  - When starting a new sprint cycle
- **Prerequisites**: Epic files created from `create-epics-and-stories`
- **Output**: `sprint-status.yaml` for tracking all epics and stories

#### create-story
- **Agent**: SM
- **Purpose**: Create story file from epic
- **When to Use**: When ready to start implementing a specific story
- **Prerequisites**: Sprint planning completed, epic exists
- **Output**: Story file

#### implement-story (dev-story)
- **Agent**: DEV
- **Purpose**: Implement a story with tests following the architecture and conventions
- **When to Use**: 
  - After create-story has prepared the story file
  - When ready to write code for a story
  - Story dependencies are marked DONE
- **Prerequisites**: Story file created, Architecture and tech-spec available
- **Output**: Implemented code and tests

#### run-code-review
- **Agent**: DEV
- **Purpose**: Quality validation of implemented code
- **When to Use**: After implementing a story (recommended)
- **Prerequisites**: Story implementation completed
- **Output**: Code review feedback

#### run-automate
- **Agent**: TEA (Test Engineering Agent)
- **Purpose**: Generate guardrail tests
- **When to Use**: Optional, after story implementation
- **Prerequisites**: Story implementation completed
- **Output**: Automated test suite

---

### Testing & Quality Workflows (TEA Agent)

These workflows are handled by the TEA (Test Engineering Agent) for comprehensive testing.

#### run-atdd
- **Agent**: TEA
- **Purpose**: Acceptance Test-Driven Development
- **When to Use**: When you want to follow ATDD practices
- **Output**: Acceptance tests

#### run-test-design
- **Agent**: TEA
- **Purpose**: Design comprehensive test suites
- **When to Use**: When planning test coverage
- **Output**: Test design specifications

#### run-test-review
- **Agent**: TEA
- **Purpose**: Review and validate test quality
- **When to Use**: After test creation to ensure quality
- **Output**: Test review feedback

#### run-trace
- **Agent**: TEA
- **Purpose**: Traceability analysis between requirements and tests
- **When to Use**: When you need to verify test coverage of requirements
- **Output**: Traceability matrix

#### run-nfr-assess
- **Agent**: TEA
- **Purpose**: Non-Functional Requirements assessment
- **When to Use**: When validating NFRs from the PRD
- **Output**: NFR assessment report

#### setup-test-framework
- **Agent**: TEA
- **Purpose**: Set up test framework for the project
- **When to Use**: At the beginning of a project or when adding testing
- **Output**: Configured test framework

---

### Setup & Configuration Workflows

These workflows help initialize and manage BMad projects.

#### workflow-init
- **Agent**: Analyst
- **Purpose**: Initialize a new BMad project and recommend a planning track
- **When to Use**: At the very beginning of a new project
- **Output**: `bmm-workflow-status.yaml` to track progress through all phases

#### workflow-status
- **Agent**: Any
- **Purpose**: Check progress and identify next recommended or required workflow
- **When to Use**: Anytime you're unsure what to do next
- **Output**: Status report with next steps

#### setup-ci
- **Agent**: TEA
- **Purpose**: Set up CI pipeline
- **When to Use**: When you want to configure continuous integration
- **Output**: CI pipeline configuration

#### setup-party-mode
- **Agent**: Any
- **Purpose**: Set up party mode for multi-agent collaboration
- **When to Use**: When you want multiple agents to work together
- **Output**: Party mode configuration

---

### Planning Tracks

BMad offers three planning tracks based on project complexity:

| Track           | Best For                                               | Documents Created                      | Workflows Used                    |
| --------------- | ------------------------------------------------------ | -------------------------------------- | --------------------------------- |
| **Quick Flow**  | Bug fixes, simple features, clear scope (1-15 stories) | Tech-spec only                         | quick-spec → implementation       |
| **BMad Method** | Products, platforms, complex features (10-50+ stories) | PRD + Architecture + UX                | Full workflow (all phases)        |
| **Enterprise**  | Compliance, multi-tenant systems (30+ stories)         | PRD + Architecture + Security + DevOps | Full workflow + additional checks |

---

### Typical Workflow Sequence

### Quick Flow Track
1. `workflow-init` (Analyst)
2. `quick-spec` or `bmgd-quick-flow` (PM)
3. `sprint-planning` (SM)
4. `create-story` → `dev-story` → `code-review` (repeat for each story)

### BMad Method/Enterprise Track
1. `workflow-init` (Analyst)
2. **Phase 1 (Optional)**: `brainstorm-project`, `research`, `product-brief` (Analyst)
3. **Phase 2**: `create-prd` (PM) → `create-ux-design` (UX-Designer, optional)
4. **Phase 3**: `create-architecture` (Architect) → `create-epics-and-stories` (PM) → `run-implementation-readiness` (Architect)
5. **Phase 4**: `sprint-planning` (SM) → `create-story` (SM) → `dev-story` (DEV) → `code-review` (DEV) → `automate` (TEA, optional)

---

### Key Principles

- **Always use fresh chats** for each workflow to avoid context limitations
- **Let workflow-status guide you** - ask any agent for status when unsure
- **Track matters** - Quick Flow uses tech-spec; Method/Enterprise need PRD and architecture
- **Tracking is automatic** - Status files update themselves
- **Agents are flexible** - Use menu numbers, shortcuts (`*prd`), or natural language

---

### Documentation

All workflow documentation is available at:
`C:\PROJ\BMAD-METHOD\docs\how-to\workflows\`

For more information, see:
- [Getting Started Guide](../BMAD-METHOD/docs/tutorials/getting-started/getting-started-bmadv6.md)
- [BMad Method Documentation](../BMAD-METHOD/docs/index.md)

---

## 3 Brownfield Development

This chapter covers workflows and best practices for working with existing codebases using the BMad Method.

### 3.1 What is Brownfield Development?

**Brownfield** refers to working on existing projects with established codebases and patterns, as opposed to **greenfield** which means starting from scratch with a clean slate.

When working with brownfield projects, BMad agents need to:
- Understand existing architecture and patterns
- Respect current conventions and code organization
- Integrate new features with existing systems
- Avoid reinventing solutions that already exist

---

### 3.2 Initial Setup

#### Clean Up Completed Planning Artifacts

If you have completed all PRD epics and stories through the BMad process, clean up those files. Archive them, delete them, or rely on version history if needed. Do not keep these files in:

- `docs/`
- `_bmad-output/planning-artifacts/`
- `_bmad-output/implementation-artifacts/`

#### Maintain Quality Project Documentation

Your `docs/` folder should contain succinct, well-organized documentation that accurately represents your project:

- Intent and business rationale
- Business rules
- Architecture
- Any other relevant project information

#### Initialize for Brownfield Work

Run `workflow-init`. It should recognize you are in an existing project. If not, explicitly clarify that this is brownfield development for a new feature.

---

### 3.3 Documenting Existing Projects

#### document-project

- **Agent**: Analyst
- **Purpose**: Scan your entire codebase and generate comprehensive documentation about its current state
- **When to Use**: 
  - Starting work on an undocumented legacy project
  - Documentation is outdated and needs refresh
  - AI agents need context about existing code patterns
  - Onboarding new team members
- **Output**: `project-documentation-{date}.md` with project overview, technology stack, architecture patterns, business rules, and integration points

**How to Use:**

1. Load the Analyst agent
2. Run: `document-project` workflow
3. The workflow offers runtime variants (quick, deep, exhaustive) that will scan your entire project and document its actual current state
4. Review the generated documentation for accuracy and completeness

**What You Get:**

- **Project overview** - High-level description of what the project does
- **Technology stack** - Detected frameworks, libraries, and tools
- **Architecture patterns** - Code organization and design patterns found
- **Business rules** - Logic extracted from the codebase
- **Integration points** - External APIs and services

**Best Practice:** Always run `document-project` before planning brownfield projects. AI agents need existing codebase context to make informed decisions.

---

### 3.4 Adding Features to Existing Projects

#### Choosing Your Approach

The scope of your feature determines which workflow track to use:

| Feature Scope | Recommended Approach | Workflows |
|---------------|---------------------|-----------|
| **Small (1-5 stories)** | Quick Flow with tech-spec | `quick-spec` or `quick-flow-solo-dev` → implementation |
| **Medium (5-15 stories)** | BMad Method with PRD | `create-prd` → `sprint-planning` → implementation |
| **Large (15+ stories)** | Full BMad Method with architecture | `create-prd` → `create-architecture` → `create-epics-and-stories` → implementation |

#### Workflow Steps

**1. Run workflow-init**

The workflow should recognize you're in an existing project. If not, explicitly clarify that this is brownfield development.

**2. Document First (if needed)**

If your project is undocumented or documentation is outdated, run `document-project` first to create baseline documentation.

**3. Create Planning Documents**

**For Quick Flow:**
- Load PM agent
- Run `quick-spec` or `quick-flow-solo-dev` workflow
- The agent will analyze your existing codebase and create a context-aware spec

**For BMad Method:**
- Load PM agent
- Run `create-prd` workflow
- Ensure the agent reads your existing documentation
- Review that integration points are clearly identified

**4. Consider Architecture Impact**

If your feature affects system architecture:

- Load Architect agent
- Run `create-architecture` workflow
- Ensure alignment with existing patterns
- Pay close attention to prevent reinventing the wheel or making decisions that misalign with your existing architecture
- Document any new ADRs (Architecture Decision Records)

**5. UX Considerations**

UX work is optional. The decision depends not on whether your project has a UX, but on:

- Whether you will be working on UX changes
- Whether significant new UX designs or patterns are needed

If your changes amount to simple updates to existing screens you are happy with, a full UX process is unnecessary.

**6. Implement**

Follow the standard Phase 4 implementation workflows:

1. `sprint-planning` - Organize your work
2. `create-story` - Prepare each story
3. `dev-story` - Implement with tests
4. `code-review` - Quality assurance

---

### 3.5 Quick Fixes and Ad-Hoc Changes

For bug fixes, small refactorings, or targeted code improvements that don't require the full BMad method or Quick Flow, use the **DEV agent** directly.

#### When to Use Direct DEV Agent

- Bug fixes
- Small refactorings
- Targeted code improvements
- Learning about your codebase
- One-off changes that don't need planning

#### How to Use

1. Load the DEV agent (or Quick Flow Solo Dev for slightly larger changes)
2. Simply describe the change:
   ```
   Fix the login validation bug that allows empty passwords
   ```
   or
   ```
   Refactor the UserService to use async/await instead of callbacks
   ```
3. The agent will:
   - Analyze the relevant code
   - Propose a solution
   - Implement the change
   - Run tests (if available)
4. Review and commit when satisfied

#### Learning Your Codebase

This approach is also excellent for exploring unfamiliar code:

```
Explain how the authentication system works in this codebase
```

```
Show me where error handling happens in the API layer
```

LLMs are excellent at interpreting and analyzing code—whether it was AI-generated or not. Use the agent to:

- Learn about your project
- Understand how things are built
- Explore unfamiliar parts of the codebase

#### When to Upgrade to Formal Planning

Consider using Quick Flow or full BMad Method when:

- The change affects multiple files or systems
- You're unsure about the scope
- The fix keeps growing in complexity
- You need documentation for the change

---

### 3.6 Best Practices

#### Documentation First

- **Always run `document-project`** before planning brownfield projects if documentation is missing or outdated
- Keep your `docs/` folder updated with accurate project information
- Ensure agents read existing documentation during planning

#### Context Awareness

- During PRD creation, ensure the agent:
  - Finds and analyzes your existing project documentation
  - Reads the proper context about your current system
  - Understands existing architecture and patterns

- During architecture work, ensure the architect:
  - Uses the proper documented files
  - Scans the existing codebase
  - Aligns with existing patterns

#### Integration Considerations

- Pay close attention to integration points with existing code
- Follow existing conventions unless deliberately changing them
- Document why you're adding new patterns (if any)
- Prevent reinventing solutions that already exist

#### Workflow Selection

- **Small updates or additions**: Use `quick-flow-solo-dev` to create a tech-spec and implement the change. The full four-phase BMad method is likely overkill.
- **Major changes or additions**: Start with the BMad method, applying as much or as little rigor as needed.

#### Fresh Chats

- **Always use fresh chats** for each workflow to avoid context limitations
- This is especially important in brownfield projects where context can become complex

#### Agent Guidance

- You can guide agents explicitly to ensure they read your existing documentation
- The goal is to ensure new features integrate well with your existing system
- Use `workflow-status` to check progress and identify next steps

---

For detailed brownfield guides, see:
- [Brownfield Development Guide](../BMAD-METHOD/docs/how-to/brownfield/index.md)
- [Document Existing Project](../BMAD-METHOD/docs/how-to/brownfield/document-existing-project.md)
- [Add Feature to Existing Project](../BMAD-METHOD/docs/how-to/brownfield/add-feature-to-existing.md)
- [Quick Fix in Brownfield](../BMAD-METHOD/docs/how-to/brownfield/quick-fix-in-brownfield.md)

---

## 4 Document Sharding

This chapter covers document sharding, a technique for optimizing how BMad workflows load and use large planning documents.

### 4.1 Introduction

Document sharding is a **user-initiated optimization technique** that splits large markdown files into smaller, section-based files. This enables workflows to load only the sections they need, dramatically reducing token usage and improving efficiency.

**Important:** Sharding is a **manual task** - agents do not automatically shard documents or proactively suggest sharding. You are responsible for recognizing when sharding would be beneficial and manually invoking the tool.

#### How It Works

Document sharding splits large markdown files into smaller, organized files based on level 2 headings (`## Heading`). This enables:

- **Selective Loading** - Workflows load only the sections they need
- **Reduced Token Usage** - Massive efficiency gains for large projects
- **Better Organization** - Logical section-based file structure
- **Maintained Context** - Index file preserves document structure

#### Workflow Discovery System

BMad workflows use a **dual discovery system** that works transparently:

1. **Try whole document first** - Look for `document-name.md`
2. **Check for sharded version** - Look for `document-name/index.md`
3. **Priority rule** - Whole document takes precedence if both exist - remove the whole document if you want the sharded version to be used instead

All BMM workflows support both formats automatically, so sharding is completely transparent to workflows once done.

#### Why Manual?

- Workflows support both whole and sharded documents automatically
- Sharding is optional - workflows work perfectly fine with either format
- You control when to optimize for token efficiency
- It's a proactive optimization, not a requirement

---

### 4.2 When to Shard Documents

Sharding is most beneficial for large documents that are frequently referenced during implementation. Consider sharding when you have:

- **Very large complex PRDs** - Documents with extensive FRs/NFRs across multiple epics
- **Architecture documents with multiple system layers** - Complex technical designs covering frontend, backend, data, security, deployment, etc.
- **Epic files with 4+ epics** - Especially important for Phase 4 workflows that repeatedly load epic files
- **UX design specs covering multiple subsystems** - Large design documents with many screens and interaction patterns

#### Signs You Should Shard

Watch for these indicators that sharding might help:

- Documents that feel unwieldy to navigate
- Workflows that seem slow or hit context limits
- Phase 4 workflows repeatedly loading large documents
- Documents exceeding 20-30k tokens
- Multiple level 2 headings (10+ sections)

#### When Sharding Is Most Valuable

Sharding is **most valuable in Phase 4 (Implementation)**, where workflows repeatedly reference planning documents. The selective loading capability means:

- `dev-story` only loads relevant epic sections
- `create-story` only loads the epic being worked on
- `sprint-planning` can efficiently scan multiple epics
- Token usage drops dramatically for large projects

---

### 4.3 Sharding Workflow

The sharding process is straightforward and interactive.

#### Step 1: Invoke the Shard-Doc Tool

Use the BMad core tool command:

```bash
/bmad:core:tools:shard-doc
```

#### Step 2: Follow the Interactive Process

The tool will guide you through the process:

```
Agent: Which document would you like to shard?
User: docs/PRD.md

Agent: Default destination: docs/prd/
       Accept default? [y/n]
User: y

Agent: Sharding PRD.md...
       ✓ Created 12 section files
       ✓ Generated index.md
       ✓ Complete!
```

#### Step 3: Review the Output

After sharding, you'll get:

**Directory structure:**
```
docs/
└── prd/
    ├── index.md                    # Table of contents with descriptions
    ├── overview.md                 # Section 1
    ├── user-requirements.md        # Section 2
    ├── technical-requirements.md   # Section 3
    └── ...                         # Additional sections
```

**index.md structure:**
```markdown
## Sections

1. [Overview](./overview.md) - Project vision and objectives
2. [User Requirements](./user-requirements.md) - Feature specifications
3. [Epic 1: Authentication](./epic-1-authentication.md) - User auth system
4. [Epic 2: Dashboard](./epic-2-dashboard.md) - Main dashboard UI
   ...
```

**Individual section files:**
- Named from heading text (kebab-case)
- Contains complete section content
- Preserves all markdown formatting
- Can be read independently

#### Step 4: Handle the Original Document

**Important:** After sharding, delete or archive the original document to avoid confusion. The sharding guide recommends removing the whole document if you want the sharded version to be used, since whole documents take precedence in the discovery system.

You can:
- Delete the original (recommended)
- Move it to an archive folder
- Keep it only if you need both versions temporarily

---

### 4.4 Best Practices

#### Timing

- **Shard before Phase 4** - Do sharding after planning documents are complete but before starting implementation
- **Shard after major updates** - If you significantly expand a document, consider re-sharding
- **Don't shard mid-workflow** - Complete your planning workflows first, then shard

#### Document Structure

- **Ensure proper heading hierarchy** - Sharding works best with clear level 2 headings (`##`)
- **Review section names** - The tool creates file names from headings - ensure they're descriptive
- **Check the index** - Review the generated `index.md` to ensure sections are properly organized

#### Workflow Integration

- **Transparent to workflows** - Once sharded, workflows automatically use the sharded version
- **No workflow changes needed** - All BMM workflows support both formats automatically
- **Verify discovery** - After sharding, workflows should automatically find `document-name/index.md`

#### Maintenance

- **Update sharded files, not originals** - Once sharded, make all edits to the individual section files
- **Keep index.md updated** - If you manually reorganize sections, update the index
- **Version control** - Commit the sharded structure to version control for team consistency

#### When Not to Shard

Sharding isn't always necessary:

- **Small documents** - Documents under 10-15k tokens may not benefit significantly
- **Single-purpose documents** - If a document is always loaded in full, sharding adds complexity without benefit
- **Frequently changing documents** - If you're still actively editing structure, wait until it stabilizes

#### Common Patterns

**PRD Sharding:**
```
docs/prd/
├── index.md
├── overview.md
├── user-requirements.md
├── functional-requirements.md
├── non-functional-requirements.md
└── success-metrics.md
```

**Architecture Sharding:**
```
docs/architecture/
├── index.md
├── system-overview.md
├── data-architecture.md
├── api-architecture.md
├── frontend-architecture.md
├── security-architecture.md
└── deployment-architecture.md
```

**Epic Files Sharding:**
```
docs/epics/
├── index.md
├── epic-1-authentication.md
├── epic-2-dashboard.md
├── epic-3-payments.md
└── epic-4-reporting.md
```

---

For detailed sharding documentation, see:
- [Document Sharding Guide](../BMAD-METHOD/docs/how-to/customization/shard-large-documents.md)

---

## 5 Agent Customization

This chapter covers how to customize BMad agents to add project-specific memories, context, and workflows without modifying core files.

### 5.1 Introduction

Agent customization allows you to personalize BMad agents for your specific project needs using `.customize.yaml` files. All customizations persist through updates and are stored per-project in `_bmad/_config/agents/`.

#### What You Can Customize

- **Agent Name** - Change how the agent introduces itself
- **Persona** - Modify role, identity, communication style, and principles
- **Memories** - Add persistent context the agent always remembers
- **Critical Actions** - Add instructions that execute before the agent starts
- **Custom Menu Items** - Add your own workflows to the agent's menu
- **Custom Prompts** - Define reusable prompts for menu handlers

#### Key Benefits

- **Project-Specific Context** - Agents remember your project's unique requirements
- **Consistent Enforcement** - Rules and conventions applied automatically
- **Team Alignment** - Shared agent customizations ensure everyone follows the same standards
- **Update-Safe** - Customizations survive all BMad updates
- **Per-Project** - Different projects can have different agent behaviors

---

### 5.2 When to Customize Agents

Customize agents when you need to:

#### Domain-Specific Requirements
- Healthcare (HIPAA compliance, PHI handling)
- Finance (PCI-DSS, financial regulations)
- Legal (data retention, compliance)
- Industry-specific terminology and patterns

#### Compliance and Security
- Regulatory requirements (HIPAA, GDPR, SOC 2)
- Security standards and patterns
- Audit trail requirements
- Data handling protocols

#### Team Conventions
- Coding standards and naming conventions
- Architectural patterns and decisions
- Testing approaches
- Documentation requirements

#### Technology Constraints
- Legacy system integration patterns
- Specific framework requirements
- Performance constraints
- Platform-specific considerations

#### Business Rules
- Complex domain logic that must be consistently applied
- Business process requirements
- Integration patterns with external systems

---

### 5.3 How to Customize Agents

#### Step 1: Locate Customization Files

After installation, find agent customization files in:

```
_bmad/_config/agents/
├── core-bmad-master.customize.yaml
├── bmm-dev.customize.yaml
├── bmm-pm.customize.yaml
└── ... (one file per installed agent)
```

#### Step 2: Edit the Customization File

Open the `.customize.yaml` file for the agent you want to modify. All sections are optional - customize only what you need.

#### Step 3: Rebuild the Agent

**CRITICAL:** After editing, you must rebuild the agent to apply changes:

```bash
npx bmad-method@alpha build <agent-name>
```

For example:
```bash
npx bmad-method@alpha build bmm-dev
npx bmad-method@alpha build bmm-pm
npx bmad-method@alpha build core-bmad-master
```

#### Customization File Structure

```yaml
# Agent name override
agent:
  metadata:
    name: 'Custom Agent Name'

# Replace entire persona (not merged)
persona:
  role: 'Senior Full-Stack Engineer'
  identity: 'Expert in specific domain'
  communication_style: 'Clear and concise'
  principles:
    - 'Principle 1'
    - 'Principle 2'

# Add persistent memories
memories:
  - 'Project-specific memory 1'
  - 'Project-specific memory 2'

# Add critical actions (executed before agent starts)
critical_actions:
  - 'Always check git status before making changes'
  - 'Use conventional commit messages'

# Add custom menu items
menu:
  - trigger: my-workflow
    workflow: '{project-root}/_bmad/custom-workflows/my-workflow.yaml'
    description: My custom workflow
  - trigger: my-action
    action: '#my-prompt-id'
    description: My custom action

# Add custom prompts (for action="#id" handlers)
prompts:
  - id: my-prompt-id
    content: |
      Prompt instructions here
```

**Important Notes:**
- The persona section replaces the entire default persona (not merged)
- Don't include `*` prefix or `help`/`exit` items in menu - these are auto-injected
- Menu items are appended to the base menu
- Memories persist across all agent sessions

---

### 5.4 Integration into Workflows

#### Standard Workflow Integration

Customized agents work seamlessly with existing workflows. When you load a customized agent and run a workflow, the agent automatically:

1. **Applies memories** - All project-specific memories are active
2. **Executes critical actions** - Pre-workflow checks run automatically
3. **Uses custom menu items** - Your custom workflows appear in the menu

#### Example: Using a Customized Agent

1. **Load the agent:**
   ```
   /bmm-dev
   ```

2. **Run standard workflows:**
   ```
   *dev-story
   *code-review
   ```

3. **Use custom menu items:**
   ```
   *compliance-check
   *review-architecture-compliance
   ```

The agent's memories and critical actions are active in all workflows, ensuring consistent behavior.

#### Custom Workflow Integration

You can create custom workflows that leverage agent memories:

1. **Create workflow file:**
   ```
   _bmad/custom-workflows/compliance-review.yaml
   ```

2. **Reference in agent customization:**
   ```yaml
   menu:
     - trigger: compliance-check
       workflow: '{project-root}/_bmad/custom-workflows/compliance-review.yaml'
       description: Run compliance review
   ```

3. **Rebuild agent:**
   ```bash
   npx bmad-method@alpha build bmm-dev
   ```

4. **Use the workflow:**
   ```
   /bmm-dev
   *compliance-check
   ```

---

### 5.5 Best Practices

#### Start Small
- Customize one section at a time
- Test after each change
- Rebuild and verify before adding more

#### Backup Customizations
- Copy customization files before major changes
- Version control your `_bmad/_config/` folder
- Share customizations with your team via version control

#### Update-Safe
- Customizations in `_config/` survive all BMad updates
- Per-project customizations allow different behaviors per project
- No need to reapply customizations after updates

#### Memory Management
- Keep memories concise and specific
- Focus on rules that must be consistently applied
- Update memories as requirements evolve
- Don't duplicate information already in architecture docs

#### Workflow Design
- Custom workflows should complement, not replace, standard workflows
- Use memories for enforcement, architecture docs for source of truth
- Design workflows that leverage agent memories effectively

#### Team Collaboration
- Commit `_bmad/_config/` to version control
- Document why customizations exist
- Review customizations during code reviews
- Keep customizations aligned with project standards

#### Troubleshooting

**Changes not appearing?**
- Make sure you ran `npx bmad-method@alpha build <agent-name>` after editing
- Check YAML syntax is valid (indentation matters!)
- Verify the agent name matches the file name pattern

**Agent not loading?**
- Check for YAML syntax errors
- Ensure required fields aren't left empty if you uncommented them
- Try reverting to the template and rebuilding

**Need to reset?**
- Delete the `.customize.yaml` file
- Run `npx bmad-method@alpha build <agent-name>` to regenerate defaults

---

### 5.6 Example: Healthcare Compliance Agent

This example shows how to customize the DEV agent for a HIPAA-compliant patient portal project.

#### Use Case

Building a healthcare application that handles Protected Health Information (PHI) requires strict compliance with HIPAA regulations. The DEV agent needs to remember:
- HIPAA compliance requirements
- PHI handling protocols
- Security patterns specific to healthcare
- Testing requirements for healthcare data

#### Customization File

**File:** `_bmad/_config/agents/bmm-dev.customize.yaml`

```yaml
# Customize DEV agent for healthcare project
agent:
  metadata:
    name: 'Healthcare DEV'

# Add project-specific memories
memories:
  - 'Project handles Protected Health Information (PHI) - all data access must be logged and audited'
  - 'HIPAA compliance required: encryption at rest and in transit, access controls, audit trails'
  - 'Never log PHI in console.log or error messages - use sanitized identifiers only'
  - 'All API endpoints handling patient data must require authentication and authorization'
  - 'Project uses HL7 FHIR standards for healthcare data exchange'
  - 'Database fields containing PHI must be marked with @PHI annotation in code comments'
  - 'All user actions accessing PHI must be logged to audit_log table with timestamp and user_id'
  - 'Testing: Use synthetic test data only - never real patient information'

# Add critical actions specific to healthcare compliance
critical_actions:
  - 'Before committing: Verify no PHI is exposed in logs, errors, or console output'
  - 'Check that all database queries filtering PHI include proper access control checks'
  - 'Ensure audit logging is implemented for any new PHI access points'

# Add custom menu item for compliance review workflow
menu:
  - trigger: compliance-check
    workflow: '{project-root}/_bmad/custom-workflows/compliance-review.yaml'
    description: Run HIPAA compliance review for current changes
```

#### Complete Example with All Sections

```yaml
# Healthcare DEV Agent Customization
agent:
  metadata:
    name: 'Healthcare DEV'

persona:
  role: 'Senior Full-Stack Engineer specializing in healthcare compliance'
  identity: 'Expert in HIPAA, HL7 FHIR, and secure healthcare application development'
  communication_style: 'Security-first, compliance-aware, detail-oriented'
  principles:
    - 'Privacy and security are non-negotiable'
    - 'Always assume data is PHI unless explicitly marked otherwise'
    - 'Audit trails are as important as functionality'

memories:
  - 'Project handles Protected Health Information (PHI) - all data access must be logged and audited'
  - 'HIPAA compliance required: encryption at rest and in transit, access controls, audit trails'
  - 'Never log PHI in console.log or error messages - use sanitized identifiers only'
  - 'All API endpoints handling patient data must require authentication and authorization'
  - 'Project uses HL7 FHIR standards for healthcare data exchange'
  - 'Database fields containing PHI must be marked with @PHI annotation in code comments'
  - 'All user actions accessing PHI must be logged to audit_log table with timestamp and user_id'
  - 'Testing: Use synthetic test data only - never real patient information'
  - 'Current tech stack: React, Node.js, PostgreSQL with row-level security enabled'

critical_actions:
  - 'Before committing: Verify no PHI is exposed in logs, errors, or console output'
  - 'Check that all database queries filtering PHI include proper access control checks'
  - 'Ensure audit logging is implemented for any new PHI access points'
  - 'Run security linter before finalizing code'

menu:
  - trigger: compliance-check
    workflow: '{project-root}/_bmad/custom-workflows/compliance-review.yaml'
    description: Run HIPAA compliance review for current changes
  - trigger: audit-log-review
    action: '#audit-log-prompt'
    description: Review audit log implementation for current feature

prompts:
  - id: audit-log-prompt
    content: |
      Review the current implementation for audit logging:
      1. Identify all points where PHI is accessed
      2. Verify each access point logs to audit_log table
      3. Confirm logs include: user_id, timestamp, action_type, resource_id
      4. Check that logs cannot be modified or deleted by application users
```

#### How to Use

1. **Edit the customization file:**
   - Open `_bmad/_config/agents/bmm-dev.customize.yaml`
   - Add the memories and customizations above

2. **Rebuild the agent:**
   ```bash
   npx bmad-method@alpha build bmm-dev
   ```

3. **Load and use the agent:**
   ```
   /bmm-dev
   *dev-story
   ```

4. **The agent will automatically:**
   - Remember HIPAA requirements when writing code
   - Avoid logging PHI
   - Include audit logging
   - Follow healthcare domain patterns

5. **Use custom workflows:**
   ```
   *compliance-check
   ```

#### Benefits

- **Consistent Compliance** - HIPAA rules always remembered
- **Automatic Enforcement** - Critical actions run before commits
- **Team Alignment** - All developers get the same context
- **Quality Assurance** - Built-in compliance checks

---

### 5.7 Example: Code Review Agent

This example shows how to customize the DEV agent for enhanced code review that enforces architectural rules and naming conventions.

#### Use Case

Large teams or complex projects need consistent code reviews that verify:
- Architectural decision compliance (ADRs)
- Naming conventions
- Code organization patterns
- Project-specific standards

While the `code-review` workflow already checks architecture alignment, customizing the agent ensures these rules are always remembered and consistently applied.

#### Customization File

**File:** `_bmad/_config/agents/bmm-dev.customize.yaml`

```yaml
# Code Review Enhanced DEV Agent
agent:
  metadata:
    name: 'Code Review Specialist'

persona:
  role: 'Senior Code Reviewer specializing in architecture compliance'
  identity: 'Expert in enforcing architectural decisions, naming conventions, and code quality standards'
  communication_style: 'Thorough, constructive, standards-focused'
  principles:
    - 'Architecture decisions are non-negotiable - refer to ADRs'
    - 'Naming conventions prevent confusion and bugs'
    - 'Code review is a teaching moment, not just gatekeeping'

memories:
  # Architectural Rules
  - 'All API endpoints must follow GraphQL schema per ADR-003'
  - 'Database columns use snake_case, TypeScript interfaces use camelCase per standards'
  - 'State management: Redux for global state, React Context for component trees (ADR-005)'
  - 'Component structure: /components/{feature}/{ComponentName}.tsx per architecture.md'
  
  # Naming Conventions
  - 'Functions: camelCase, descriptive verbs (getUserData, validateEmail)'
  - 'Components: PascalCase, noun-based (UserProfile, OrderSummary)'
  - 'Constants: UPPER_SNAKE_CASE (MAX_RETRY_COUNT, API_BASE_URL)'
  - 'Private methods: prefix with underscore (_validateInput, _formatDate)'
  - 'Test files: *.test.ts or *.spec.ts matching source file name'
  
  # Code Organization Rules
  - 'One component per file, co-locate tests in same directory'
  - 'Hooks in /hooks directory, utilities in /utils, types in /types'
  - 'No circular dependencies - verify import graph before approving'
  - 'API calls must use centralized client from /lib/api-client.ts'
  
  # Project-Specific Patterns
  - 'Error handling: Use Result<T, Error> type, never throw in business logic'
  - 'Async operations: Always use try/catch with proper error logging'
  - 'Form validation: Use Zod schemas, defined in /schemas directory'
  - 'Date handling: Use date-fns, never native Date methods directly'

critical_actions:
  - 'Before review: Read architecture.md and relevant ADRs for context'
  - 'Verify naming conventions match project standards exactly'
  - 'Check that new code follows existing patterns in codebase'
  - 'Ensure no architectural decisions are violated (check ADRs)'
  - 'Validate directory structure matches conventions'
  - 'Confirm no circular dependencies introduced'

menu:
  - trigger: review-architecture-compliance
    action: '#architecture-compliance-prompt'
    description: Deep review focusing on ADR and standards compliance
  - trigger: review-naming-conventions
    action: '#naming-conventions-prompt'
    description: Review all naming against project conventions

prompts:
  - id: architecture-compliance-prompt
    content: |
      Perform deep architecture compliance review:
      1. Read architecture.md and all relevant ADRs
      2. Verify every architectural decision is followed
      3. Check for any violations of ADR decisions
      4. Ensure new code integrates with existing patterns
      5. Report any deviations with specific ADR references
      
  - id: naming-conventions-prompt
    content: |
      Review all naming in changed files:
      1. Functions: camelCase, descriptive verbs
      2. Components: PascalCase, noun-based
      3. Constants: UPPER_SNAKE_CASE
      4. Files: match component/function naming
      5. Directories: kebab-case for multi-word
      6. Report any violations with suggested corrections
```

#### How to Use

1. **Edit the customization file:**
   - Open `_bmad/_config/agents/bmm-dev.customize.yaml`
   - Add the memories and customizations above

2. **Rebuild the agent:**
   ```bash
   npx bmad-method@alpha build bmm-dev
   ```

3. **Standard code review:**
   ```
   /bmm-dev
   *code-review
   ```
   The agent will automatically remember all architectural rules and naming conventions.

4. **Enhanced review options:**
   ```
   *review-architecture-compliance  # Deep ADR compliance check
   *review-naming-conventions       # Focused naming review
   ```

#### Benefits

- **Complements Architecture Docs** - Memories enforce, docs remain source of truth
- **Faster Reviews** - Agent doesn't need to re-read standards each time
- **Consistent Enforcement** - Same rules applied every time
- **Team Alignment** - Shared agent = shared standards
- **Learning Opportunity** - Agent explains violations with references

#### When This Is Most Valuable

- **Large Teams** - Multiple developers need consistent reviews
- **Complex Projects** - Many architectural rules to remember
- **Strict Compliance** - Regulatory or security requirements
- **Evolving Standards** - Rules that change and need updates
- **Brownfield Projects** - Existing conventions to enforce

---

For detailed customization documentation, see:
- [Agent Customization Guide](../BMAD-METHOD/docs/how-to/customization/customize-agents.md)

---

## 6 Features & Capabilities

This chapter covers key features and capabilities available in BMad that enhance your development workflow.

### 6.1 Party Mode

Party Mode brings all your AI agents together in one conversation for multi-agent collaboration.

#### What is Party Mode?

Type `/bmad:core:workflows:party-mode` (or `*party-mode` from any agent), and you've got **all your AI agents** in one conversation. PM, Architect, DEV, UX Designer and more that you can choose from.

#### How It Works

1. Party mode reads `_bmad/_config/agent-manifest.csv`
2. Loads ALL installed agents (already includes your customizations from install)
3. BMad Master orchestrates - picks 2-3 relevant agents per message based on topic
4. Agents respond in character, can agree/disagree/build on each other's ideas
5. Discussion continues until you type "exit" or reach natural conclusion

**That's it.** No complex merging, no runtime magic. Just agents talking.

#### When to Use Party Mode

- **After complex workflows** - Debrief with the whole team about what worked, what didn't
- **Big decisions with tradeoffs** - Get technical, creative, and strategic perspectives simultaneously
- **Brainstorming sessions** - Watch ideas evolve through cross-pollination
- **When things go wrong** - Call out failures, watch agents defend their decisions, let them debate whose fault it was
- **Sprint retrospectives** - Party mode powers the retrospective workflow
- **Sprint planning** - Multi-agent collaboration for planning sessions

#### Quick Start

```bash
/bmad:core:workflows:party-mode

*party-mode

# Include specific agents
/bmad:core:workflows:party-mode and include also in the party Santa Clause and Einstein

# Ask questions, respond to agents, direct the conversation
# Type: exit
```

#### Example Use Cases

**Technical Decision:**
```
You: "Monolith or microservices for MVP?"

Architect: "Start monolith. Microservices add complexity you don't need at 1000 users."
PM: "Agree. Time to market matters more than theoretical scalability."
DEV: "Monolith with clear module boundaries. We can extract services later if needed."
```

**Creative Brainstorming:**
```
You: "How do we make onboarding feel magical instead of boring?"

UX Designer: "Start with progressive disclosure - reveal features as users need them..."
Storyteller: "What if onboarding was a story? Each step reveals a character's journey..."
Game Designer: "Building on that - what if the first 'quest' is actually solving a real user problem?"
```

**Better decisions through diverse perspectives. Welcome to party mode.**

---

### 6.2 TEA Overview

The Test Architect (TEA) is a specialized agent focused on quality strategy, test automation, and release gates in BMad Method projects.

#### What is TEA?

- **Persona:** Murat, Master Test Architect and Quality Advisor focused on risk-based testing, fixture architecture, ATDD, and CI/CD governance.
- **Mission:** Deliver actionable quality strategies, automation coverage, and gate decisions that scale with project complexity and compliance demands.
- **Use When:** BMad Method or Enterprise track projects, integration risk is non-trivial, brownfield regression risk exists, or compliance/NFR evidence is required. (Quick Flow projects typically don't require TEA)

#### TEA's 8 Workflows

| Command        | Purpose                                                                               | When to Use |
| -------------- | ------------------------------------------------------------------------------------- | ----------- |
| `*framework`   | Scaffold Playwright/Cypress test infrastructure                                       | When no production-ready harness exists |
| `*ci`          | Configure CI pipeline with selective testing                                          | When setting up CI/CD |
| `*test-design` | Risk-based test planning (system-level or epic-level)                                 | Before implementation, per epic |
| `*atdd`        | Generate failing acceptance tests before implementation                               | TDD workflow, before dev |
| `*automate`    | Generate prioritized test specs after implementation                                  | After story implementation |
| `*test-review` | Audit test quality with 0-100 scoring                                                 | After test creation |
| `*nfr-assess`  | Assess Non-Functional Requirements (security/performance/reliability)               | Enterprise track, validate NFRs |
| `*trace`       | Coverage traceability + gate decision (PASS/CONCERNS/FAIL/WAIVED)                    | Release gates, coverage tracking |

#### TEA Workflow Lifecycle

**Phase 3: Solutioning**
- `*test-design` (system-level) → testability review
- `*framework` → test infrastructure setup
- `*ci` → CI/CD pipeline configuration

**Phase 4: Implementation (Per Epic)**
- `*test-design` (epic-level) → risk assessment for THIS epic
- (Optional) `*atdd` → failing tests before dev
- `*automate` → expand coverage after implementation
- (Optional) `*test-review` → quality audit
- `*trace` Phase 1 → refresh coverage

**Release Gate:**
- (Optional) `*test-review` → final audit
- (Optional) `*nfr-assess` → validate NFRs
- `*trace` Phase 2 → gate decision

#### TEA Engagement Models

TEA is optional and flexible. There are five valid ways to engage with TEA:

1. **No TEA** - Skip all TEA workflows, use existing testing approach
2. **TEA Solo** - Use TEA standalone without BMad Method
3. **TEA Lite** - Beginner approach using just `*automate`
4. **TEA Integrated (Greenfield)** - Full BMad Method integration from scratch
5. **TEA Integrated (Brownfield)** - Full BMad Method integration with existing code

See [TEA Testing Strategy](#7-tea-testing-strategy) section for detailed guidance on choosing and using engagement models.

#### Why TEA Is Different

TEA spans multiple phases (Phase 3, Phase 4, and the release gate). Most BMad agents operate in a single phase. That multi-phase role is paired with a dedicated testing knowledge base so standards stay consistent across projects.

#### Optional Integrations

**Playwright Utils (`@seontechnologies/playwright-utils`)**
- Production-ready fixtures and utilities
- Install: `npm install -D @seontechnologies/playwright-utils`
- Impacts: `*framework`, `*atdd`, `*automate`, `*test-review`, `*ci`

**Playwright MCP Enhancements**
- Live browser verification for test design and automation
- Two MCP servers: `playwright` and `playwright-test`
- Helps validate actual UI behavior and verify selectors

For detailed TEA documentation, see:
- [TEA Overview](../BMAD-METHOD/docs/explanation/features/tea-overview.md)
- [TEA Testing Strategy](#7-tea-testing-strategy) section below

---

### 6.3 Quick Flow

Quick Flow is a streamlined alternative to the full BMad Method for rapid development. Instead of going through Product Brief → PRD → Architecture, you go straight to a context-aware technical specification and start coding.

#### When to Use Quick Flow

**Use Quick Flow when:**
- Single bug fix or small enhancement
- Small feature with clear scope (typically 1-15 stories)
- Rapid prototyping or experimentation
- Adding to existing brownfield codebase
- You know exactly what you want to build

**Use BMad Method or Enterprise when:**
- Building new products or major features
- Need stakeholder alignment
- Complex multi-team coordination
- Requires extensive planning and architecture

**Not Sure?** Run `workflow-init` to get a recommendation based on your project's needs.

#### What Makes It Quick

- No Product Brief needed
- No PRD needed
- No Architecture doc needed
- Auto-detects your stack
- Auto-analyzes brownfield code
- Auto-validates quality
- Story context optional (tech-spec is comprehensive)

#### Smart Context Discovery

Quick Flow automatically discovers and uses:

**Existing Documentation:**
- Product briefs (if they exist)
- Research documents
- `document-project` output (brownfield codebase map)

**Project Stack:**
- **Node.js:** package.json → frameworks, dependencies, scripts
- **Python:** requirements.txt, pyproject.toml → packages, tools
- **Ruby:** Gemfile → gems and versions
- **Java:** pom.xml, build.gradle → Maven/Gradle dependencies
- **Go:** go.mod → modules
- **Rust:** Cargo.toml → crates

**Brownfield Code Patterns:**
- Directory structure and organization
- Existing code patterns (class-based, functional, MVC)
- Naming conventions
- Test frameworks and patterns
- Code style configurations

**Convention Confirmation:**

Quick Flow detects your conventions and **asks for confirmation**:

```
I've detected these conventions in your codebase:

Code Style:
- ESLint with Airbnb config
- Prettier with single quotes

Test Patterns:
- Jest test framework
- .test.js file naming

Should I follow these existing conventions? (yes/no)
```

**You decide:** Conform to existing patterns or establish new standards!

#### Auto-Validation

Quick Flow **automatically validates** everything:
- Context gathering completeness
- Definitiveness (no "use X or Y" statements)
- Brownfield integration quality
- Stack alignment
- Implementation readiness

#### Quick Flow Process

**Step 1: Technical Specification (`quick-spec`)**
- Load PM agent or Barry (Quick Flow Solo Dev)
- Run `quick-spec` workflow
- Creates context-rich tech spec with implementation-ready stories

**Step 2: Development (`quick-dev` or `dev-story`)**
- Load DEV agent or Barry
- Run `quick-dev` (Barry) or `dev-story` (DEV) workflow
- Implement based on tech spec

**Step 3: Code Review (Optional)**
- Load DEV agent
- Run `code-review` workflow
- Quality validation

#### Barry: Quick Flow Solo Dev Agent

Barry is the elite solo developer who takes projects from concept to deployment with ruthless efficiency—no handoffs, no delays, just pure focused development.

**When to Use Barry:**
- Quick Flow Development - Small to medium features that need rapid delivery
- Technical Specification Creation - When you need detailed implementation plans
- Direct Development - When requirements are clear and you want to skip extensive planning
- Code Reviews - When you need senior-level technical validation
- Performance-Critical Features - When optimization and scalability are paramount

**Barry's Workflow:**
1. `quick-spec` - Architect a technical spec with implementation-ready stories
2. `quick-dev` - Ship features from spec or direct instructions - no handoffs
3. `code-review` - Review code for quality, patterns, and acceptance criteria (optional)

**Load Barry:**
```bash
/bmad:bmm:agents:quick-flow-solo-dev
```

For more details, see:
- [Barry Agent Documentation](../BMAD-METHOD/docs/explanation/agents/barry-quick-flow.md)

#### Comparison: Quick Flow vs Full BMM

| Aspect                | Quick Flow Track             | BMad Method/Enterprise Tracks      |
| --------------------- | ---------------------------- | ---------------------------------- |
| **Setup**             | None (standalone)            | workflow-init recommended          |
| **Planning Docs**     | tech-spec.md only            | Product Brief → PRD → Architecture |
| **Time to Code**      | Minutes                      | Hours to days                      |
| **Best For**          | Bug fixes, small features    | New products, major features       |
| **Context Discovery** | Automatic                    | Manual + guided                    |
| **Validation**        | Auto-validates everything    | Manual validation steps            |
| **Brownfield**        | Auto-analyzes and conforms   | Manual documentation required      |

#### When to Graduate to BMad Method

Start with Quick Flow, but switch to BMad Method when:
- Project grows beyond initial scope
- Multiple teams need coordination
- Stakeholders need formal documentation
- Product vision is unclear
- Architectural decisions need deep analysis
- Compliance/regulatory requirements exist

**Transition Tip:** You can always run `workflow-init` later to transition from Quick Flow to BMad Method.

---

### 6.4 Advanced Elicitation

Advanced Elicitation pushes the LLM to rethink its work through 50+ reasoning methods—essentially, LLM brainstorming.

#### What is Advanced Elicitation?

Advanced Elicitation is the inverse of Brainstorming. Instead of pulling ideas out of you, the LLM applies sophisticated reasoning techniques to re-examine and enhance content it has just generated. It's the LLM brainstorming with itself to find better approaches, uncover hidden issues, and discover improvements it missed on the first pass.

#### When to Use It

- After a workflow generates a section of content and you want to explore alternatives
- When the LLM's initial output seems adequate but you suspect there's more depth available
- For high-stakes content where multiple perspectives would strengthen the result
- To stress-test assumptions, explore edge cases, or find weaknesses in generated plans
- When you want the LLM to "think again" but with structured reasoning methods

#### How It Works

**1. Context Analysis**
The LLM analyzes the current content, understanding its type, complexity, stakeholder needs, risk level, and creative potential.

**2. Smart Method Selection**
Based on context, 5 methods are intelligently selected from a library of 50+ techniques and presented to you:

| Option            | Description                              |
| ----------------- | ---------------------------------------- |
| **1-5**           | Apply the selected method to the content |
| **[r] Reshuffle** | Get 5 new methods selected randomly      |
| **[a] List All**  | Browse the complete method library       |
| **[x] Proceed**   | Continue with enhanced content           |

**3. Method Execution & Iteration**
- The selected method is applied to the current content
- Improvements are shown for your review
- You choose whether to apply changes or discard them
- The menu re-appears for additional elicitations
- Each method builds on previous enhancements

**4. Party Mode Integration (Optional)**
If Party Mode is active, BMad agents participate randomly in the elicitation process, adding their unique perspectives to the methods.

#### Method Categories

| Category          | Focus                               | Example Methods                                                |
| ----------------- | ----------------------------------- | -------------------------------------------------------------- |
| **Core**          | Foundational reasoning techniques   | First Principles Analysis, 5 Whys, Socratic Questioning        |
| **Collaboration** | Multiple perspectives and synthesis | Stakeholder Round Table, Expert Panel Review, Debate Club      |
| **Advanced**      | Complex reasoning frameworks        | Tree of Thoughts, Graph of Thoughts, Self-Consistency          |
| **Competitive**   | Adversarial stress-testing          | Red Team vs Blue Team, Shark Tank Pitch, Code Review Gauntlet  |
| **Technical**     | Architecture and code quality       | Decision Records, Rubber Duck Debugging, Algorithm Olympics    |
| **Creative**      | Innovation and lateral thinking     | SCAMPER, Reverse Engineering, Random Input Stimulus            |
| **Research**      | Evidence-based analysis             | Literature Review Personas, Thesis Defense, Comparative Matrix |
| **Risk**          | Risk identification and mitigation  | Pre-mortem Analysis, Failure Mode Analysis, Chaos Monkey       |
| **Learning**      | Understanding verification          | Feynman Technique, Active Recall Testing                       |
| **Philosophical** | Conceptual clarity                  | Occam's Razor, Ethical Dilemmas                                |
| **Retrospective** | Reflection and lessons              | Hindsight Reflection, Lessons Learned Extraction               |

#### Key Features

- **50+ reasoning methods** — Spanning core logic to advanced multi-step reasoning frameworks
- **Smart context selection** — Methods chosen based on content type, complexity, and stakeholder needs
- **Iterative enhancement** — Each method builds on previous improvements
- **User control** — Accept or discard each enhancement before proceeding
- **Party Mode integration** — Agents can participate when Party Mode is active

#### Workflow Integration

Advanced Elicitation is a core workflow designed to be invoked by other workflows during content generation. When called from a workflow:

1. Receives the current section content that was just generated
2. Applies elicitation methods iteratively to enhance that content
3. Returns the enhanced version when user selects 'x' to proceed
4. The enhanced content replaces the original section in the output document

**Example:** A specification generation workflow could invoke Advanced Elicitation after producing each major section (requirements, architecture, implementation plan). The workflow would pass the generated section, and Advanced Elicitation would offer methods like "Stakeholder Round Table" to gather diverse perspectives on requirements, or "Red Team vs Blue Team" to stress-test the architecture for vulnerabilities.

#### Advanced Elicitation vs. Brainstorming

|              | **Advanced Elicitation**                          | **Brainstorming**                             |
| ------------ | ------------------------------------------------- | --------------------------------------------- |
| **Source**   | LLM generates ideas through structured reasoning  | User provides ideas, AI coaches them out      |
| **Purpose**  | Rethink and improve LLM's own output              | Unlock user's creativity                      |
| **Methods**  | 50+ reasoning and analysis techniques             | 60+ ideation and creativity techniques        |
| **Best for** | Enhancing generated content, finding alternatives | Breaking through blocks, generating new ideas |

---

### 6.5 Web Bundles

Web bundles package BMad agents as self-contained files that work in Gemini Gems and Custom GPTs.

#### What Are Web Bundles?

Web bundles package BMad agents as self-contained files that work in Gemini Gems and Custom GPTs. Everything the agent needs - instructions, workflows, dependencies - is bundled into a single file for easy upload.

#### What's Included

- Complete agent persona and instructions
- All workflows and dependencies
- Interactive menu system
- Party mode for multi-agent collaboration
- No external files required

#### Use Cases

**Perfect for:**
- Uploading a single file to a Gemini GEM or Custom GPT
- Using BMad Method from the Web
- Cost savings (generally lower cost than local usage)
- Quick sharing of agent configurations

**Trade-offs:**
- Some quality reduction vs local usage
- Less convenient than full local installation
- Limited to agent capabilities (no workflow file access)

#### Status

:::caution[Status]
The Web Bundling Feature is being rebuilt from the ground up. Current v6 bundles may be incomplete or missing functionality.
:::

---

## 7 TEA Testing Strategy

This chapter provides practical guidance on choosing and using TEA (Test Architect) engagement models for your project.

### 7.1 TEA Engagement Models

TEA is optional and flexible. There are five valid ways to engage with TEA - choose intentionally based on your project needs and methodology.

#### Overview

**TEA is not mandatory.** Pick the engagement model that fits your context:

1. **No TEA** - Skip all TEA workflows, use existing testing approach
2. **TEA Solo** - Use TEA standalone without BMad Method
3. **TEA Lite** - Beginner approach using just `*automate`
4. **TEA Integrated (Greenfield)** - Full BMad Method integration from scratch
5. **TEA Integrated (Brownfield)** - Full BMad Method integration with existing code

#### Model 1: No TEA

**What:** Skip all TEA workflows, use your existing testing approach.

**When to Use:**
- Team has established testing practices
- Quality is already high
- Testing tools already in place
- TEA doesn't add value

**What You Miss:**
- Risk-based test planning
- Systematic quality review
- Gate decisions with evidence
- Knowledge base patterns

**What You Keep:**
- Full control
- Existing tools
- Team expertise
- No learning curve

**Verdict:** Valid choice if existing approach works.

---

#### Model 2: TEA Solo

**What:** Use TEA workflows standalone without full BMad Method integration.

**When to Use:**
- Non-BMad projects
- Want TEA's quality operating model only
- Don't need full planning workflow
- Bring your own requirements

**Typical Sequence:**
```
1. *test-design (system or epic)
2. *atdd or *automate
3. *test-review (optional)
4. *trace (coverage + gate decision)
```

**You Bring:**
- Requirements (user stories, acceptance criteria)
- Development environment
- Project context

**TEA Provides:**
- Risk-based test planning (`*test-design`)
- Test generation (`*atdd`, `*automate`)
- Quality review (`*test-review`)
- Coverage traceability (`*trace`)

**Optional:**
- Framework setup (`*framework`) if needed
- CI configuration (`*ci`) if needed

**Verdict:** Best for teams wanting TEA benefits without BMad Method commitment.

---

#### Model 3: TEA Lite

**What:** Beginner approach using just `*automate` to test existing features.

**When to Use:**
- Learning TEA fundamentals
- Want quick results
- Testing existing application
- No time for full methodology

**Workflow:**
```
1. *framework (setup test infrastructure)
2. *test-design (optional, risk assessment)
3. *automate (generate tests for existing features)
4. Run tests (they pass immediately)
```

**What You Get:**
- Working test framework
- Passing tests for existing features
- Learning experience
- Foundation to expand

**What You Miss:**
- TDD workflow (ATDD)
- Risk-based planning (test-design depth)
- Quality gates (trace Phase 2)
- Full TEA capabilities

**Verdict:** Perfect entry point for beginners.

**Getting Started:** See [TEA Lite Quickstart Tutorial](../BMAD-METHOD/docs/tutorials/getting-started/tea-lite-quickstart.md) - 30-minute beginner guide.

---

#### Model 4: TEA Integrated (Greenfield)

**What:** Full BMad Method integration with TEA workflows across all phases.

**When to Use:**
- New projects starting from scratch
- Using BMad Method or Enterprise track
- Want complete quality operating model
- Testing is critical to success

**Lifecycle:**

**Phase 2: Planning**
- PM creates PRD with NFRs
- (Optional) TEA runs `*nfr-assess` (Enterprise only)

**Phase 3: Solutioning**
- Architect creates architecture
- TEA runs `*test-design` (system-level) → testability review
- TEA runs `*framework` → test infrastructure
- TEA runs `*ci` → CI/CD pipeline
- Architect runs `*implementation-readiness` (fed by test design)

**Phase 4: Implementation (Per Epic)**
- SM runs `*sprint-planning`
- TEA runs `*test-design` (epic-level) → risk assessment for THIS epic
- SM creates stories
- (Optional) TEA runs `*atdd` → failing tests before dev
- DEV implements story
- TEA runs `*automate` → expand coverage
- (Optional) TEA runs `*test-review` → quality audit
- TEA runs `*trace` Phase 1 → refresh coverage

**Release Gate:**
- (Optional) TEA runs `*test-review` → final audit
- (Optional) TEA runs `*nfr-assess` → validate NFRs
- TEA runs `*trace` Phase 2 → gate decision (PASS/CONCERNS/FAIL/WAIVED)

**What You Get:**
- Complete quality operating model
- Systematic test planning
- Risk-based prioritization
- Evidence-based gate decisions
- Consistent patterns across epics

**Verdict:** Most comprehensive TEA usage, best for structured teams.

---

#### Model 5: TEA Integrated (Brownfield)

**What:** Full BMad Method integration with TEA for existing codebases.

**When to Use:**
- Existing codebase with legacy tests
- Want to improve test quality incrementally
- Adding features to existing application
- Need to establish coverage baseline

**Differences from Greenfield:**

**Phase 0: Documentation (if needed)**
```
- Run *document-project
- Create baseline documentation
```

**Phase 2: Planning**
```
- TEA runs *trace Phase 1 → establish coverage baseline
- PM creates PRD (with existing system context)
```

**Phase 3: Solutioning**
```
- Architect creates architecture (with brownfield constraints)
- TEA runs *test-design (system-level) → testability review
- TEA runs *framework (only if modernizing test infra)
- TEA runs *ci (update existing CI or create new)
```

**Phase 4: Implementation**
```
- TEA runs *test-design (epic-level) → focus on REGRESSION HOTSPOTS
- Per story: ATDD → dev → automate
- TEA runs *test-review → improve legacy test quality
- TEA runs *trace Phase 1 → track coverage improvement
```

**Brownfield-Specific:**
- Baseline coverage BEFORE planning
- Focus on regression hotspots (bug-prone areas)
- Incremental quality improvement
- Compare coverage to baseline (trending up?)

**Verdict:** Best for incrementally improving legacy systems.

---

### 7.2 Choosing Your Model

#### Quick Decision Tree

**Question 1:** Are you using BMad Method?
- **No** → TEA Solo or TEA Lite or No TEA
- **Yes** → TEA Integrated or No TEA

**Question 2:** Is this a new project?
- **Yes** → TEA Integrated (Greenfield) or TEA Lite
- **No** → TEA Integrated (Brownfield) or TEA Solo

**Question 3:** What's your testing maturity?
- **Beginner** → TEA Lite
- **Intermediate** → TEA Solo or Integrated
- **Advanced** → TEA Integrated or No TEA (already expert)

**Question 4:** Do you need compliance/quality gates?
- **Yes** → TEA Integrated (Enterprise)
- **No** → Any model

**Question 5:** How much time can you invest?
- **30 minutes** → TEA Lite
- **Few hours** → TEA Solo
- **Multiple days** → TEA Integrated

#### Recommendation Matrix

| Your Context | Recommended Model | Alternative |
|--------------|------------------|-------------|
| BMad Method + new project | TEA Integrated (Greenfield) | TEA Lite (learning) |
| BMad Method + existing code | TEA Integrated (Brownfield) | TEA Solo |
| Non-BMad + need quality | TEA Solo | TEA Lite |
| Just learning testing | TEA Lite | No TEA (learn basics first) |
| Enterprise + compliance | TEA Integrated (Enterprise) | TEA Solo |
| Established QA team | No TEA | TEA Solo (supplement) |

#### By Project Type

| Project Type | Recommended Model | Why |
|--------------|------------------|-----|
| **New SaaS product** | TEA Integrated (Greenfield) | Full quality operating model from day one |
| **Existing app + new feature** | TEA Integrated (Brownfield) | Improve incrementally while adding features |
| **Bug fix** | TEA Lite or No TEA | Quick flow, minimal overhead |
| **Learning project** | TEA Lite | Learn basics with immediate results |
| **Non-BMad enterprise** | TEA Solo | Quality model without full methodology |
| **High-quality existing tests** | No TEA | Keep what works |

#### By Team Maturity

| Team Maturity | Recommended Model | Why |
|---------------|------------------|-----|
| **Beginners** | TEA Lite → TEA Solo | Learn basics, then expand |
| **Intermediate** | TEA Solo or Integrated | Depends on methodology |
| **Advanced** | TEA Integrated or No TEA | Full model or existing expertise |

#### By Compliance Needs

| Compliance | Recommended Model | Why |
|------------|------------------|-----|
| **None** | Any model | Choose based on project needs |
| **Light** (internal audit) | TEA Solo or Integrated | Gate decisions helpful |
| **Heavy** (SOC 2, HIPAA) | TEA Integrated (Enterprise) | NFR assessment mandatory |

---

### 7.3 Practical Application

#### Switching Between Models

**Can Change Models Mid-Project**

**Scenario:** Start with TEA Lite, expand to TEA Solo

```
Week 1: TEA Lite
- Run *framework
- Run *automate
- Learn basics

Week 2: Expand to TEA Solo
- Add *test-design
- Use *atdd for new features
- Add *test-review

Week 3: Continue expanding
- Add *trace for coverage
- Setup *ci
- Full TEA Solo workflow
```

**Benefit:** Start small, expand as comfortable.

**Can Mix Models**

**Scenario:** TEA Integrated for main features, No TEA for bug fixes

```
Main features (epics):
- Use full TEA workflow
- Risk assessment, ATDD, quality gates

Bug fixes:
- Skip TEA
- Quick Flow + manual testing
- Move fast

Result: TEA where it adds value, skip where it doesn't
```

**Benefit:** Flexible, pragmatic, not dogmatic.

#### Common Patterns

**Pattern 1: TEA Lite for Learning, Then Choose**

```
Phase 1 (Week 1-2): TEA Lite
- Learn with *automate on demo app
- Understand TEA fundamentals
- Low commitment

Phase 2 (Week 3-4): Evaluate
- Try *test-design (planning)
- Try *atdd (TDD)
- See if value justifies investment

Phase 3 (Month 2+): Decide
- Valuable → Expand to TEA Solo or Integrated
- Not valuable → Stay with TEA Lite or No TEA
```

**Pattern 2: TEA Solo for Quality, Skip Full Method**

```
Team decision:
- Don't want full BMad Method (too heavyweight)
- Want systematic testing (TEA benefits)

Approach: TEA Solo only
- Use existing project management (Jira, Linear)
- Use TEA for testing only
- Get quality without methodology commitment
```

**Pattern 3: Integrated for Critical, Lite for Non-Critical**

```
Critical features (payment, auth):
- Full TEA Integrated workflow
- Risk assessment, ATDD, quality gates
- High confidence required

Non-critical features (UI tweaks):
- TEA Lite or No TEA
- Quick tests, minimal overhead
- Move fast
```

#### Comparison Table

| Aspect | No TEA | TEA Lite | TEA Solo | Integrated (Green) | Integrated (Brown) |
|--------|--------|----------|----------|-------------------|-------------------|
| **BMad Required** | No | No | No | Yes | Yes |
| **Learning Curve** | None | Low | Medium | High | High |
| **Setup Time** | 0 | 30 min | 2 hours | 1 day | 2 days |
| **Workflows Used** | 0 | 2-3 | 4-6 | 8 | 8 |
| **Test Planning** | Manual | Optional | Yes | Systematic | + Regression focus |
| **Quality Gates** | No | No | Optional | Yes | Yes + baseline |
| **NFR Assessment** | No | No | No | Optional | Recommended |
| **Coverage Tracking** | Manual | No | Optional | Yes | Yes + trending |
| **Best For** | Experts | Beginners | Standalone | New projects | Legacy code |

#### Real-World Examples

**Example 1: Startup (TEA Lite → TEA Integrated)**

**Month 1:** TEA Lite
- Team: 3 developers, no QA
- Testing: Manual only
- Decision: Start with TEA Lite
- Result: Run *framework (Playwright setup), Run *automate (20 tests generated), Learning TEA basics

**Month 3:** TEA Solo
- Team: Growing to 5 developers
- Testing: Automated tests exist
- Decision: Expand to TEA Solo
- Result: Add *test-design (risk assessment), Add *atdd (TDD workflow), Add *test-review (quality audits)

**Month 6:** TEA Integrated
- Team: 8 developers, 1 QA
- Testing: Critical to business
- Decision: Full BMad Method + TEA Integrated
- Result: Full lifecycle integration, Quality gates before releases, NFR assessment for enterprise customers

**Example 2: Enterprise (TEA Integrated - Brownfield)**

**Project:** Legacy banking application

**Challenge:**
- 500 existing tests (50% flaky)
- Adding new features
- SOC 2 compliance required

**Model:** TEA Integrated (Brownfield)

**Phase 2:**
- *trace baseline → 45% coverage (lots of gaps)
- Document current state

**Phase 3:**
- *test-design (system) → identify regression hotspots
- *framework → modernize test infrastructure
- *ci → add selective testing

**Phase 4:**
Per epic:
- *test-design → focus on regression + new features
- Fix top 10 flaky tests
- *atdd for new features
- *automate for coverage expansion
- *test-review → track quality improvement
- *trace → compare to baseline

**Result after 6 months:**
- Coverage: 45% → 85%
- Quality score: 52 → 82
- Flakiness: 50% → 2%
- SOC 2 compliant (traceability + NFR evidence)

#### Transitioning Between Models

**TEA Lite → TEA Solo**

**When:** Outgrow beginner approach, need more workflows.

**Steps:**
1. Continue using `*framework` and `*automate`
2. Add `*test-design` for planning
3. Add `*atdd` for TDD workflow
4. Add `*test-review` for quality audits
5. Add `*trace` for coverage tracking

**Timeline:** 2-4 weeks of gradual expansion

**TEA Solo → TEA Integrated**

**When:** Adopt BMad Method, want full integration.

**Steps:**
1. Install BMad Method (see installation guide)
2. Run planning workflows (PRD, architecture)
3. Integrate TEA into Phase 3 (system-level test design)
4. Follow integrated lifecycle (per epic workflows)
5. Add release gates (trace Phase 2)

**Timeline:** 1-2 sprints of transition

**TEA Integrated → TEA Solo**

**When:** Moving away from BMad Method, keep TEA.

**Steps:**
1. Export BMad artifacts (PRD, architecture, stories)
2. Continue using TEA workflows standalone
3. Skip BMad-specific integration
4. Bring your own requirements to TEA

**Timeline:** Immediate (just skip BMad workflows)

---

For detailed TEA documentation, see:
- [TEA Overview](../BMAD-METHOD/docs/explanation/features/tea-overview.md)
- [TEA Engagement Models](../BMAD-METHOD/docs/explanation/tea/engagement-models.md)
- [TEA Workflow Guides](../BMAD-METHOD/docs/how-to/workflows/) - All 8 workflows with step-by-step instructions
