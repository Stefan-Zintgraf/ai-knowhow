---
title: "Hello World Python: Complete BMad Workflow Tutorial"
description: Step-by-step tutorial building a Hello World Python app using all BMad phases
---

# Hello World Python: Complete BMad Workflow Tutorial

This tutorial walks you through building a simple "Hello World" Python application using the complete BMad Method workflow. You'll experience all four phases: Analysis, Planning, Solutioning, and Implementation, including TEA testing workflows.

**Time:** ~45-60 minutes  
**Prerequisites:** Node.js 20+, Python 3.8+, Git, Claude Code IDE

---

## What You'll Build

A simple Python command-line application that:
- Displays "Hello, World!" when run
- Accepts an optional name parameter
- Includes proper project structure
- Has automated tests

**Why Hello World?** While simple, this tutorial demonstrates the complete BMad workflow end-to-end, showing how all phases connect in practice.

---

## Table of Contents

1. [Setup](#1-setup)
2. [Phase 1: Analysis - Brainstorming](#phase-1-analysis---brainstorming)
3. [Phase 2: Planning - Create PRD](#phase-2-planning---create-prd)
4. [Phase 3: Solutioning](#phase-3-solutioning)
   - [Create Architecture](#31-create-architecture)
   - [Create Epics and Stories](#32-create-epics-and-stories)
   - [Implementation Readiness](#33-implementation-readiness)
5. [Phase 4: Implementation](#phase-4-implementation)
   - [Sprint Planning](#41-sprint-planning)
   - [Create Story](#42-create-story)
   - [Implement Story](#43-implement-story)
   - [Generate Tests with TEA](#44-generate-tests-with-tea)
   - [Code Review](#45-code-review)
6. [Verification](#verification)
7. [Summary](#summary)

---

## 1. Setup

:::tip[Related Documentation]
For detailed installation instructions and troubleshooting, see [Installation (bmad_knowhow.md)](bmad_knowhow.md#1-installation).
:::

### Step 1.1: Create Project Directory

Open a terminal and create a new directory:

```bash
mkdir hello-world-bmad
cd hello-world-bmad
```

### Step 1.2: Install BMad Method

Run the BMad installer:

```bash
npx bmad-method@alpha install
```

**Interactive prompts:**

1. **Where to install BMad files?**
   - Choose: `Current directory` (press Enter)

2. **Select your AI tools:**
   - Choose: `Claude Code` (press Space to select, then Enter)

3. **Select modules to install:**
   - Choose: `BMM: BMad Method` (press Space, then Enter)

4. **Project name:**
   - Enter: `hello-world-bmad` (or press Enter for default)

5. **Experience level:**
   - Choose: `beginner` (or your preference)

6. **Planning artifacts folder:**
   - Press Enter for default: `_bmad-output`

7. **Implementation artifacts folder:**
   - Press Enter for default: `_bmad-output`

8. **Project knowledge folder:**
   - Press Enter for default: `_bmad-output`

9. **Enable TEA Playwright MCP enhancements?**
   - Choose: `No` (for this simple tutorial)

10. **Using playwright-utils?**
    - Choose: `No` (for this simple tutorial)

**Expected output:**
```
✓ BMad Method installed successfully!
✓ Created _bmad/ directory
✓ Created _bmad-output/ directory
```

### Step 1.3: Verify Installation

Check that BMad is installed:

```bash
ls _bmad/
```

You should see:
```
_bmad/
├── bmm/
│   ├── agents/
│   ├── workflows/
│   └── config.yaml
└── core/
```

**✓ Setup complete!** You're ready to start the workflow.

:::note[Installation Help]
If you encounter any issues during installation, see [Troubleshooting (bmad_knowhow.md)](bmad_knowhow.md#14-troubleshooting) for common solutions.
:::

---

## Phase 1: Analysis - Brainstorming

**Purpose:** Explore ideas and approaches for our Hello World application.

:::tip[Related Documentation]
Learn more about brainstorming and other analysis workflows in [Phase 1: Analysis (bmad_knowhow.md)](bmad_knowhow.md#phase-1-analysis-optional).
:::

### Step 1.1: Load Analyst Agent

1. Open **Claude Code** (or your AI IDE)
2. Start a **fresh chat** (important: always use fresh chats for each workflow)
3. Type in the chat:

```
/analyst
```

**Expected:** The Analyst agent loads and shows a menu of available workflows.

### Step 1.2: Run Brainstorming Workflow

In the same chat, type:

```
*brainstorm-project
```

**Expected:** The agent asks about your project idea.

### Step 1.3: Describe Your Project

Respond with:

```
I want to build a simple Hello World Python application. It should:
- Display "Hello, World!" when run
- Optionally accept a name parameter to personalize the greeting
- Be a command-line application
- Follow Python best practices
```

**Expected:** The agent explores different approaches:
- **Architecture track:** CLI vs. GUI, argument parsing options
- **UX track:** User interaction patterns
- **Integration track:** How it could be packaged/distributed
- **Value track:** Learning Python basics, demonstrating BMad workflow

### Step 1.4: Review Brainstorming Results

The agent presents multiple solution approaches. For this tutorial, we'll proceed with:
- **Approach:** Simple CLI application using Python's `argparse`
- **Rationale:** Simple, standard, demonstrates best practices

**Note:** You can skip brainstorming for very simple projects, but it's included here to show the complete workflow. For more brainstorming techniques, see [brainstorm-project (bmad_knowhow.md)](bmad_knowhow.md#brainstorm-project).

**✓ Phase 1 complete!** You've explored different approaches.

---

## Phase 2: Planning - Create PRD

**Purpose:** Create a formal Product Requirements Document defining what we'll build.

:::tip[Related Documentation]
For more details on planning workflows and PRD creation, see [Phase 2: Planning (bmad_knowhow.md)](bmad_knowhow.md#phase-2-planning-required).
:::

### Step 2.1: Load PM Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
/pm
```

**Expected:** The PM (Product Manager) agent loads with its workflow menu.

### Step 2.2: Run PRD Workflow

Type:

```
*create-prd
```

Or use the shortcut:

```
*prd
```

**Expected:** The agent asks about your project scope.

### Step 2.3: Provide Project Context

Respond with:

```
I'm building a Hello World Python application. The requirements are:
- Display "Hello, World!" by default
- Accept an optional --name parameter to personalize the greeting
- Be a command-line application
- Follow Python best practices (proper structure, docstrings, error handling)
- Include automated tests

This is a learning project to demonstrate the BMad workflow.
```

**Expected:** The agent asks follow-up questions about:
- Target users (developers learning Python/BMad)
- Success criteria (working application, tests pass)
- Non-functional requirements (code quality, maintainability)

### Step 2.4: Define Requirements

Work with the agent to define:

**Functional Requirements (FRs):**
- FR-001: Application displays "Hello, World!" when run without arguments
- FR-002: Application accepts --name parameter to personalize greeting
- FR-003: Application handles invalid input gracefully

**Non-Functional Requirements (NFRs):**
- NFR-001: Code follows PEP 8 style guidelines
- NFR-002: Code includes docstrings
- NFR-003: Application includes automated tests

### Step 2.5: Review PRD

The agent generates `_bmad-output/PRD.md`.

**Expected file structure:**
```
_bmad-output/
└── PRD.md
```

**Key sections in PRD.md:**
- Executive Summary
- Problem Statement
- User Personas
- Functional Requirements (FR-001, FR-002, FR-003)
- Non-Functional Requirements (NFR-001, NFR-002, NFR-003)
- Success Metrics
- Risks and Assumptions

**✓ Phase 2 complete!** You have a formal requirements document.

:::note[PRD Details]
For more information on creating PRDs and understanding the requirements process, see [create-prd (bmad_knowhow.md)](bmad_knowhow.md#create-prd).
:::

---

## Phase 3: Solutioning

**Purpose:** Design the technical architecture and break work into implementable stories.

:::tip[Related Documentation]
Learn about solutioning workflows in [Phase 3: Solutioning (bmad_knowhow.md)](bmad_knowhow.md#phase-3-solutioning-bmad-methodenterprise-only).
:::

### 3.1: Create Architecture

#### Step 3.1.1: Load Architect Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
/architect
```

**Expected:** The Architect agent loads.

#### Step 3.1.2: Run Architecture Workflow

Type:

```
*create-architecture
```

**Expected:** The agent asks about technical decisions.

#### Step 3.1.3: Provide Technical Context

Respond with:

```
I'm building a Hello World Python CLI application. The PRD is in _bmad-output/PRD.md.

Key decisions needed:
- Python version (3.8+)
- Project structure (simple module or package)
- Argument parsing (argparse vs. click)
- Testing framework (pytest)
- Code organization
```

**Expected:** The agent asks clarifying questions and proposes architectural options.

#### Step 3.1.4: Make Architecture Decisions

Work with the agent to decide:

**ADR-001: Python Version**
- **Decision:** Python 3.8+ (compatibility)
- **Rationale:** Widely supported, modern features

**ADR-002: Project Structure**
- **Decision:** Simple module structure
- **Rationale:** Single-file application, no need for complex package structure

**ADR-003: Argument Parsing**
- **Decision:** Use `argparse` (standard library)
- **Rationale:** Built-in, no external dependencies

**ADR-004: Testing Framework**
- **Decision:** Use `pytest`
- **Rationale:** Industry standard, simple syntax

#### Step 3.1.5: Review Architecture Document

The agent generates `_bmad-output/architecture.md`.

**Expected file structure:**
```
_bmad-output/
├── PRD.md
└── architecture.md
```

**Key sections in architecture.md:**
- Architecture Overview
- System Architecture (simple CLI diagram)
- Standards and Conventions (PEP 8, docstrings, project structure)
- ADRs (ADR-001 through ADR-004)
- FR/NFR-Specific Guidance

**✓ Architecture complete!**

:::note[Architecture Details]
Learn more about architecture workflows and ADRs in [create-architecture (bmad_knowhow.md)](bmad_knowhow.md#create-architecture).
:::

### 3.2: Create Epics and Stories

#### Step 3.2.1: Load PM Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
/pm
```

#### Step 3.2.2: Run Epics and Stories Workflow

Type:

```
*create-epics-and-stories
```

**Expected:** The agent asks for PRD and Architecture documents.

#### Step 3.2.3: Provide Context

Respond with:

```
The PRD is in _bmad-output/PRD.md
The Architecture is in _bmad-output/architecture.md

Please create epics and stories based on these documents.
```

**Expected:** The agent analyzes the documents and creates epics.

#### Step 3.2.4: Review Epics and Stories

The agent generates epic files in `_bmad-output/epics/`.

**Expected file structure:**
```
_bmad-output/
├── PRD.md
├── architecture.md
└── epics/
    └── epic-1-hello-world-core.md
```

**Example epic-1-hello-world-core.md:**
```markdown
# Epic 1: Hello World Core

## Objective
Implement the core Hello World functionality with optional name parameter.

## Stories

### Story 1.1: Basic Hello World Display
**Priority:** P0
**Acceptance Criteria:**
- [ ] Running `python hello_world.py` displays "Hello, World!"
- [ ] Exit code is 0
- [ ] No errors or warnings

**Dependencies:** None

### Story 1.2: Personalized Greeting
**Priority:** P0
**Acceptance Criteria:**
- [ ] Running `python hello_world.py --name Alice` displays "Hello, Alice!"
- [ ] Handles names with spaces (quotes)
- [ ] Handles empty name gracefully

**Dependencies:** Story 1.1

### Story 1.3: Add Tests
**Priority:** P1
**Acceptance Criteria:**
- [ ] Tests for default greeting
- [ ] Tests for personalized greeting
- [ ] Tests for edge cases
- [ ] All tests pass with pytest

**Dependencies:** Story 1.1, Story 1.2
```

**✓ Epics and Stories complete!**

:::note[Epics and Stories]
For more details on breaking down requirements into stories, see [create-epics-and-stories (bmad_knowhow.md)](bmad_knowhow.md#create-epics-and-stories).
:::

### 3.3: Implementation Readiness

#### Step 3.3.1: Load Architect Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
/architect
```

#### Step 3.3.2: Run Implementation Readiness Workflow

Type:

```
*implementation-readiness
```

**Expected:** The agent validates all planning documents.

#### Step 3.3.3: Review Gate Decision

The agent generates `_bmad-output/implementation-readiness.md` with a gate decision.

**Expected sections:**
- Executive Summary (PASS/CONCERNS/FAIL)
- Completeness Assessment
- Alignment Assessment
- Gate Decision

**For Hello World, you should see:**
- **Gate Decision:** PASS ✅
- **Rationale:** All documents complete and aligned

**✓ Phase 3 complete!** Ready for implementation.

:::note[Implementation Readiness]
Learn more about the gate check process in [run-implementation-readiness (bmad_knowhow.md)](bmad_knowhow.md#run-implementation-readiness).
:::

---

## Phase 4: Implementation

**Purpose:** Build the application story by story.

:::tip[Related Documentation]
For comprehensive implementation workflow details, see [Phase 4: Implementation (bmad_knowhow.md)](bmad_knowhow.md#phase-4-implementation).
:::

### 4.1: Sprint Planning

#### Step 4.1.1: Load SM Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
/sm
```

**Expected:** The SM (Scrum Master) agent loads.

#### Step 4.1.2: Run Sprint Planning Workflow

Type:

```
*sprint-planning
```

**Expected:** The agent asks for epic files.

#### Step 4.1.3: Provide Context

Respond with:

```
The epic files are in _bmad-output/epics/
```

**Expected:** The agent creates `_bmad-output/sprint-status.yaml`.

**Expected file structure:**
```
_bmad-output/
├── PRD.md
├── architecture.md
├── epics/
│   └── epic-1-hello-world-core.md
├── implementation-readiness.md
└── sprint-status.yaml
```

**Example sprint-status.yaml:**
```yaml
epics:
  - id: epic-1
    title: Hello World Core
    status: backlog
    stories:
      - id: story-1.1
        title: Basic Hello World Display
        status: TODO
        priority: P0
        dependencies: []
      - id: story-1.2
        title: Personalized Greeting
        status: TODO
        priority: P0
        dependencies: [story-1.1]
      - id: story-1.3
        title: Add Tests
        status: TODO
        priority: P1
        dependencies: [story-1.1, story-1.2]
```

**✓ Sprint planning complete!**

:::note[Sprint Planning]
For more details on sprint planning and tracking, see [sprint-planning (bmad_knowhow.md)](bmad_knowhow.md#sprint-planning).
:::

### 4.2: Create Story

#### Step 4.2.1: Load SM Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
/sm
```

#### Step 4.2.2: Run Create Story Workflow

Type:

```
*create-story
```

**Expected:** The agent reads `sprint-status.yaml` and identifies the next story.

#### Step 4.2.3: Confirm Story Selection

The agent should identify Story 1.1 (Basic Hello World Display) as the first story.

Respond:

```
Yes, create Story 1.1
```

**Expected:** The agent creates `_bmad-output/epics/story-1-1-basic-hello-world-display.md`.

**Expected file structure:**
```
_bmad-output/
├── PRD.md
├── architecture.md
├── epics/
│   ├── epic-1-hello-world-core.md
│   └── story-1-1-basic-hello-world-display.md
├── implementation-readiness.md
└── sprint-status.yaml
```

**Example story file:**
```markdown
# Story 1.1: Basic Hello World Display

## Objective
Implement the basic Hello World functionality that displays "Hello, World!" when run.

## Acceptance Criteria
- [ ] Running `python hello_world.py` displays "Hello, World!"
- [ ] Exit code is 0
- [ ] No errors or warnings
- [ ] Code follows PEP 8
- [ ] Code includes docstrings

## Technical Notes
- Use argparse for argument parsing (ADR-003)
- Follow project structure from architecture (ADR-002)
- Python 3.8+ (ADR-001)

## Dependencies
- None (first story)

## Definition of Done
- All acceptance criteria pass
- Code review approved
- Tests written (in Story 1.3)
```

**✓ Story created!**

:::note[Create Story]
Learn more about story creation in [create-story (bmad_knowhow.md)](bmad_knowhow.md#create-story).
:::

### 4.3: Implement Story

#### Step 4.3.1: Load DEV Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
/dev
```

**Expected:** The DEV agent loads.

#### Step 4.3.2: Run Dev Story Workflow

Type:

```
*dev-story
```

**Expected:** The agent asks for the story file.

#### Step 4.3.3: Provide Story Context

Respond with:

```
The story file is _bmad-output/epics/story-1-1-basic-hello-world-display.md
The architecture is in _bmad-output/architecture.md
The PRD is in _bmad-output/PRD.md
```

**Expected:** The agent reads the story and implements it.

#### Step 4.3.4: Review Implementation

The agent creates `hello_world.py` in the project root.

**Expected file structure:**
```
hello-world-bmad/
├── _bmad/
├── _bmad-output/
├── hello_world.py
└── ...
```

**Example hello_world.py:**
```python
#!/usr/bin/env python3
"""
Hello World application.

A simple command-line application that displays a greeting.
"""

import argparse
import sys


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Display a Hello World greeting"
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Name to personalize the greeting"
    )
    
    args = parser.parse_args()
    
    if args.name:
        print(f"Hello, {args.name}!")
    else:
        print("Hello, World!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Note:** The agent may implement both Story 1.1 and 1.2 together since they're closely related. That's fine!

#### Step 4.3.5: Test the Implementation

Run the application:

```bash
python hello_world.py
```

**Expected output:**
```
Hello, World!
```

Test with name parameter:

```bash
python hello_world.py --name Alice
```

**Expected output:**
```
Hello, Alice!
```

**✓ Implementation complete!**

:::note[Dev Story]
For more details on the implementation workflow, see [implement-story (dev-story) (bmad_knowhow.md)](bmad_knowhow.md#implement-story-dev-story).
:::

### 4.4: Generate Tests with TEA

:::tip[Related Documentation]
Learn about TEA workflows and testing strategies in [Testing & Quality Workflows (TEA Agent) (bmad_knowhow.md)](bmad_knowhow.md#testing--quality-workflows-tea-agent) and [TEA Testing Strategy (bmad_knowhow.md)](bmad_knowhow.md#7-tea-testing-strategy).
:::

#### Step 4.4.1: Load TEA Agent

1. Start a **new fresh chat** in Claude Code
2. Type:

```
*tea
```

**Expected:** The TEA (Test Architect) agent loads.

#### Step 4.4.2: Run Automate Workflow

Type:

```
*automate
```

**Expected:** The agent asks what you're testing.

#### Step 4.4.3: Provide Test Context

Respond with:

```
I'm testing the Hello World Python application we just implemented.

Story: _bmad-output/epics/story-1-1-basic-hello-world-display.md
Implementation: hello_world.py

Generate unit tests using pytest. Test:
- Default greeting (no arguments)
- Personalized greeting (--name parameter)
- Edge cases (empty name, special characters)
```

**Expected:** The agent asks about test framework.

#### Step 4.4.4: Specify Test Framework

Respond with:

```
Use pytest for unit tests. The application is a simple CLI script.
```

**Expected:** The agent generates test files.

#### Step 4.4.5: Review Generated Tests

The agent creates `tests/test_hello_world.py`.

**Expected file structure:**
```
hello-world-bmad/
├── _bmad/
├── _bmad-output/
├── hello_world.py
├── tests/
│   └── test_hello_world.py
└── ...
```

**Example test_hello_world.py:**
```python
"""Tests for hello_world.py"""

import pytest
import subprocess
import sys


def test_default_greeting():
    """Test that default greeting displays correctly."""
    result = subprocess.run(
        [sys.executable, "hello_world.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Hello, World!" in result.stdout


def test_personalized_greeting():
    """Test personalized greeting with name parameter."""
    result = subprocess.run(
        [sys.executable, "hello_world.py", "--name", "Alice"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Hello, Alice!" in result.stdout


def test_empty_name():
    """Test handling of empty name."""
    result = subprocess.run(
        [sys.executable, "hello_world.py", "--name", ""],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Hello, !" in result.stdout
```

#### Step 4.4.6: Install pytest (if needed)

```bash
pip install pytest
```

#### Step 4.4.7: Run Tests

```bash
pytest tests/test_hello_world.py -v
```

**Expected output:**
```
======================== test session starts ========================
tests/test_hello_world.py::test_default_greeting PASSED
tests/test_hello_world.py::test_personalized_greeting PASSED
tests/test_hello_world.py::test_empty_name PASSED
======================== 3 passed in 0.05s ========================
```

**✓ Tests generated and passing!**

:::note[TEA Automate]
Learn more about TEA's automate workflow in [run-automate (bmad_knowhow.md)](bmad_knowhow.md#run-automate).
:::

### 4.5: Code Review

#### Step 4.5.1: Load DEV Agent

1. Start a **new fresh chat** in Claude Code (or continue from dev-story)
2. Type:

```
/dev
```

#### Step 4.5.2: Run Code Review Workflow

Type:

```
*code-review
```

**Expected:** The agent asks what to review.

#### Step 4.5.3: Provide Review Context

Respond with:

```
Please review:
- hello_world.py (main implementation)
- tests/test_hello_world.py (test file)

Check for:
- Code quality
- PEP 8 compliance
- Test coverage
- Best practices
```

**Expected:** The agent reviews the code and provides feedback.

#### Step 4.5.4: Review Feedback

The agent may suggest improvements like:
- Adding more docstrings
- Improving error handling
- Adding more test cases
- Code style improvements

**If suggestions are made:** Work with the agent to implement improvements.

**✓ Code review complete!**

:::note[Code Review]
For more information on code review workflows, see [run-code-review (bmad_knowhow.md)](bmad_knowhow.md#run-code-review).
:::

---

## Verification

### Final Project Structure

Your project should now look like:

```
hello-world-bmad/
├── _bmad/                    # BMad configuration
│   ├── bmm/
│   └── core/
├── _bmad-output/             # Generated artifacts
│   ├── PRD.md
│   ├── architecture.md
│   ├── epics/
│   │   ├── epic-1-hello-world-core.md
│   │   └── story-1-1-basic-hello-world-display.md
│   ├── implementation-readiness.md
│   └── sprint-status.yaml
├── hello_world.py            # Main application
├── tests/
│   └── test_hello_world.py  # Tests
└── README.md (optional)
```

### Run Final Tests

```bash
pytest tests/test_hello_world.py -v
```

All tests should pass.

### Run the Application

```bash
python hello_world.py
python hello_world.py --name "Your Name"
```

Both should work correctly.

---

## Summary

Congratulations! You've completed the full BMad workflow:

### ✅ What You Accomplished

1. **Phase 1: Analysis** - Explored ideas through brainstorming
2. **Phase 2: Planning** - Created a formal PRD with FRs and NFRs
3. **Phase 3: Solutioning** - Designed architecture, created epics/stories, validated readiness
4. **Phase 4: Implementation** - Built the application, generated tests with TEA, reviewed code

### 📚 Key Learnings

- **Always use fresh chats** for each workflow to avoid context issues - See [Key Principles (bmad_knowhow.md)](bmad_knowhow.md#key-principles)
- **Workflows are sequential** - Each phase builds on the previous - See [Typical Workflow Sequence (bmad_knowhow.md)](bmad_knowhow.md#typical-workflow-sequence)
- **Agents are specialized** - Each agent has specific workflows
- **TEA integrates seamlessly** - Testing happens after implementation - See [TEA Overview (bmad_knowhow.md)](bmad_knowhow.md#62-tea-overview)
- **Documents track progress** - Status files show where you are

### 🚀 Next Steps

Now that you understand the workflow:

1. **Try a more complex project** - Apply BMad to a real application
2. **Explore more workflows** - Try `*test-design`, `*atdd`, or other TEA workflows
3. **Customize agents** - Adapt agents to your team's needs
4. **Read the full docs** - Deep dive into specific workflows

### 📖 Related Documentation

**BMad Know-How Guide:**
- [Installation (bmad_knowhow.md)](bmad_knowhow.md#1-installation) - Detailed installation and setup
- [Workflows (bmad_knowhow.md)](bmad_knowhow.md#2-workflows) - Complete workflow reference
- [Phase 1: Analysis (bmad_knowhow.md)](bmad_knowhow.md#phase-1-analysis-optional) - Brainstorming and research
- [Phase 2: Planning (bmad_knowhow.md)](bmad_knowhow.md#phase-2-planning-required) - PRD and requirements
- [Phase 3: Solutioning (bmad_knowhow.md)](bmad_knowhow.md#phase-3-solutioning-bmad-methodenterprise-only) - Architecture and epics
- [Phase 4: Implementation (bmad_knowhow.md)](bmad_knowhow.md#phase-4-implementation) - Development workflows
- [Testing & Quality Workflows (bmad_knowhow.md)](bmad_knowhow.md#testing--quality-workflows-tea-agent) - TEA workflows
- [TEA Testing Strategy (bmad_knowhow.md)](bmad_knowhow.md#7-tea-testing-strategy) - TEA engagement models
- [Key Principles (bmad_knowhow.md)](bmad_knowhow.md#key-principles) - Best practices
- [Typical Workflow Sequence (bmad_knowhow.md)](bmad_knowhow.md#typical-workflow-sequence) - Standard workflow flow

**Additional Resources:**
- [Getting Started Guide](/docs/tutorials/getting-started/getting-started-bmadv6.md) - Overview of BMad
- [Workflow Reference](/docs/reference/workflows/index.md) - All available workflows
- [TEA Overview](/docs/explanation/features/tea-overview.md) - Testing workflows
- [Agent Roles](/docs/explanation/core-concepts/agent-roles.md) - Understanding agents

---

**Happy building with BMad! 🎉**
