# BMad Concepts

This document explains the fundamental concepts, principles, and philosophy behind the BMad Method. Understanding these concepts will help you make better decisions about when and how to use BMad effectively.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
   - [1.1 What Are Agents?](#11-what-are-agents)
   - [1.2 What Are Workflows?](#12-what-are-workflows)
   - [1.3 What Are Modules?](#13-what-are-modules)
2. [Architecture Philosophy](#2-architecture-philosophy)
   - [2.1 The Four Phases](#21-the-four-phases)
   - [2.2 Why Solutioning Matters](#22-why-solutioning-matters)
   - [2.3 Preventing Agent Conflicts](#23-preventing-agent-conflicts)
3. [Design Principles](#3-design-principles)
   - [3.1 Facilitation Over Generation](#31-facilitation-over-generation)
   - [3.2 Testing as Engineering](#32-testing-as-engineering)
4. [TEA Principles](#4-tea-principles)
   - [4.1 Risk-Based Testing Philosophy](#41-risk-based-testing-philosophy)
   - [4.2 Test Quality Standards](#42-test-quality-standards)
   - [4.3 Fixture Architecture Pattern](#43-fixture-architecture-pattern)
   - [4.4 Network-First Patterns](#44-network-first-patterns)
   - [4.5 Knowledge Base System](#45-knowledge-base-system)

---

## 1 Core Concepts

### 1.1 What Are Agents?

Agents are AI assistants that help you accomplish tasks. Each agent has a unique personality, specialized capabilities, and an interactive menu.

#### Agent Types

BMad has two primary agent types:

**Simple Agents**
- Self-contained, focused, ready to use
- Complete in a single file
- Best for: Single-purpose assistants, quick deployment, projects that don't require persistent memory

**Expert Agents**
- Powerful, memory-equipped, domain specialists
- Have a **sidecar** - a companion folder containing additional instructions, workflows, and memory files
- Remember context across sessions
- Best for: Domain specialists, tasks requiring persistent memory, complex workflows with multiple stages

#### Agent Components

All agents share these building blocks:

- **Persona** - Role, identity, communication style, and principles
- **Capabilities** - Skills, tools, and knowledge mapped to menu commands
- **Menu** - Interactive command list with triggers, descriptions, and handlers
- **Critical Actions** (optional) - Instructions that execute before the agent starts

#### When to Use Which

Choose **Simple** for focused, one-off tasks with no memory needs. Choose **Expert** when you need persistent context and complex workflows.

---

### 1.2 What Are Workflows?

Workflows are structured processes where the AI executes steps sequentially to accomplish a task. They harness the power of LLMs through progressive disclosure—breaking complex tasks into focused steps that execute sequentially.

#### The Power of Progressive Disclosure

The AI only sees the current step. It doesn't know about step 5 when it's on step 2. It can't get ahead of itself, skip steps, or lose focus. Each step gets the AI's full attention, completing fully before the next step loads.

This is the opposite of a giant prompt that tries to handle everything at once and inevitably misses details or loses coherence.

#### Workflow Types

Workflows exist on a spectrum:

- **Interactive workflows** - Guide users through complex decisions via collaboration and facilitation
- **Automated workflows** - Run with minimal user input, processing documents or executing tasks
- **Hybrid workflows** - Combine both—some steps need user input, others run automatically

#### Sequential Execution

Workflows execute in strict sequence: `step-01 → step-02 → step-03 → ... → step-N`

The AI cannot skip steps or optimize the sequence. It must complete each step fully before loading the next. This ensures thoroughness and prevents shortcuts that compromise quality.

#### Continuable Workflows

Some workflows can span multiple sessions. These "continuable workflows" track which steps are complete in the output document's frontmatter, so users can stop and resume later without losing progress.

#### The Tri-Modal Pattern

For critical workflows that produce important artifacts, BMad uses a tri-modal structure: Create, Validate, and Edit. Each mode is a separate workflow path that can run independently or flow into the others.

- **Create mode** - Builds new artifacts from scratch (can also function as a conversion tool)
- **Validate mode** - Runs standalone and checks artifacts against standards
- **Edit mode** - Modifies existing artifacts while enforcing standards

#### Why Workflows Matter

Workflows solve three fundamental problems with AI interactions:

- **Focus** - Each step contains only instructions for that phase
- **Continuity** - Workflows can span multiple sessions
- **Quality** - Sequential enforcement prevents shortcuts

---

### 1.3 What Are Modules?

Modules are organized collections of agents and workflows that solve specific problems or address particular domains.

#### What is a Module?

A module is a self-contained package that includes:

- **Agents** - Specialized AI assistants
- **Workflows** - Step-by-step processes
- **Configuration** - Module-specific settings
- **Documentation** - Usage guides and reference

#### Official BMad Modules

**Core Module** (Always installed)
- Global configuration
- Core workflows (Party Mode, Advanced Elicitation, Brainstorming)
- Common tasks (document indexing, sharding, review)

**BMad Method (BMM)**
- Software and game development
- Project planning workflows
- Implementation agents (Dev, PM, QA, Scrum Master)
- Testing and architecture guidance

**BMad Builder (BMB)**
- Agent creation workflows
- Workflow authoring tools
- Module scaffolding

**Additional Official Modules:**
- **Creative Intelligence Suite (CIS)** - Innovation and creativity
- **BMad Game Dev (BMGD)** - Game development specialization

#### Custom Modules

You can create your own modules containing:
- Custom agents for your domain
- Organizational workflows
- Team-specific configurations

Custom modules are installed the same way as official modules.

---

## 2 Architecture Philosophy

### 2.1 The Four Phases

BMad Method uses a four-phase approach that adapts to project complexity while ensuring consistent quality.

#### Phase Overview

| Phase | Name | Purpose | Required? |
|-------|------|---------|-----------|
| **Phase 1** | Analysis | Exploration and discovery | Optional |
| **Phase 2** | Planning | Requirements definition | Required |
| **Phase 3** | Solutioning | Technical design | Track-dependent |
| **Phase 4** | Implementation | Building the software | Required |

#### Why Four Phases?

The four phases separate concerns and prevent premature decisions:

- **Phase 1 (Analysis)** - Explore and validate ideas before committing to requirements
- **Phase 2 (Planning)** - Define **what** to build and **why** (business requirements)
- **Phase 3 (Solutioning)** - Define **how** to build it (technical design)
- **Phase 4 (Implementation)** - Build it (execution)

**Key Principle:** Planning defines **what** and **why**. Solutioning defines **how**. Implementation builds it.

#### Phase Flow by Track

**Quick Flow:**
```
Phase 2 (tech-spec) → Phase 4 (implement)
```
Skip Phases 1 and 3 for simple changes.

**BMad Method:**
```
Phase 1 (optional) → Phase 2 (PRD) → Phase 3 (architecture) → Phase 4 (implement)
```
Full methodology for complex projects.

**Enterprise:**
```
Phase 1 → Phase 2 (PRD) → Phase 3 (architecture + extended) → Phase 4 (implement)
```
Same as BMad Method with optional extended workflows.

---

### 2.2 Why Solutioning Matters

Phase 3 (Solutioning) translates **what** to build (from Planning) into **how** to build it (technical design). This phase prevents agent conflicts in multi-epic projects by documenting architectural decisions before implementation begins.

#### The Problem Without Solutioning

```
Agent 1 implements Epic 1 using REST API
Agent 2 implements Epic 2 using GraphQL
Result: Inconsistent API design, integration nightmare
```

When multiple agents implement different parts of a system without shared architectural guidance, they make independent technical decisions that may conflict.

#### The Solution With Solutioning

```
architecture workflow decides: "Use GraphQL for all APIs"
All agents follow architecture decisions
Result: Consistent implementation, no conflicts
```

By documenting technical decisions explicitly, all agents implement consistently and integration becomes straightforward.

#### Solutioning vs Planning

| Aspect   | Planning (Phase 2)      | Solutioning (Phase 3)             |
| -------- | ----------------------- | --------------------------------- |
| Question | What and Why?           | How? Then What units of work?     |
| Output   | FRs/NFRs (Requirements) | Architecture + Epics/Stories      |
| Agent    | PM                      | Architect → PM                    |
| Audience | Stakeholders            | Developers                        |
| Document | PRD (FRs/NFRs)          | Architecture + Epic Files         |
| Level    | Business logic          | Technical design + Work breakdown |

#### Key Principle

**Make technical decisions explicit and documented** so all agents implement consistently.

This prevents:
- API style conflicts (REST vs GraphQL)
- Database design inconsistencies
- State management disagreements
- Naming convention mismatches
- Security approach variations

#### When Solutioning is Required

| Track | Solutioning Required? |
|-------|----------------------|
| Quick Flow | No - skip entirely |
| BMad Method Simple | Optional |
| BMad Method Complex | Yes |
| Enterprise | Yes |

**Rule of Thumb:** If you have multiple epics that could be implemented by different agents, you need solutioning.

#### The Cost of Skipping

Skipping solutioning on complex projects leads to:

- **Integration issues** discovered mid-sprint
- **Rework** due to conflicting implementations
- **Longer development time** overall
- **Technical debt** from inconsistent patterns

**Cost Multiplier:** Catching alignment issues in solutioning is 10× faster than discovering them during implementation.

---

### 2.3 Preventing Agent Conflicts

When multiple AI agents implement different parts of a system, they can make conflicting technical decisions. Architecture documentation prevents this by establishing shared standards.

#### Common Conflict Types

**API Style Conflicts**

Without architecture:
- Agent A uses REST with `/users/{id}`
- Agent B uses GraphQL mutations
- Result: Inconsistent API patterns, confused consumers

With architecture:
- ADR specifies: "Use GraphQL for all client-server communication"
- All agents follow the same pattern

**Database Design Conflicts**

Without architecture:
- Agent A uses snake_case column names
- Agent B uses camelCase column names
- Result: Inconsistent schema, confusing queries

With architecture:
- Standards document specifies naming conventions
- All agents follow the same patterns

**State Management Conflicts**

Without architecture:
- Agent A uses Redux for global state
- Agent B uses React Context
- Result: Multiple state management approaches, complexity

With architecture:
- ADR specifies state management approach
- All agents implement consistently

#### How Architecture Prevents Conflicts

**1. Explicit Decisions via ADRs**

Every significant technology choice is documented with:
- Context (why this decision matters)
- Options considered (what alternatives exist)
- Decision (what we chose)
- Rationale (why we chose it)
- Consequences (trade-offs accepted)

**2. FR/NFR-Specific Guidance**

Architecture maps each functional requirement to technical approach:
- FR-001: User Management → GraphQL mutations
- FR-002: Mobile App → Optimized queries

**3. Standards and Conventions**

Explicit documentation of:
- Directory structure
- Naming conventions
- Code organization
- Testing patterns

#### Architecture as Shared Context

Think of architecture as the shared context that all agents read before implementing:

```
PRD: "What to build"
     ↓
Architecture: "How to build it"
     ↓
Agent A reads architecture → implements Epic 1
Agent B reads architecture → implements Epic 2
Agent C reads architecture → implements Epic 3
     ↓
Result: Consistent implementation
```

#### Key ADR Topics

Common decisions that prevent conflicts:

| Topic | Example Decision |
|-------|-----------------|
| API Style | GraphQL vs REST vs gRPC |
| Database | PostgreSQL vs MongoDB |
| Auth | JWT vs Sessions |
| State Management | Redux vs Context vs Zustand |
| Styling | CSS Modules vs Tailwind vs Styled Components |
| Testing | Jest + Playwright vs Vitest + Cypress |

#### Anti-Patterns to Avoid

**Common Mistakes:**
- **Implicit Decisions** — "We'll figure out the API style as we go" leads to inconsistency
- **Over-Documentation** — Documenting every minor choice causes analysis paralysis
- **Stale Architecture** — Documents written once and never updated cause agents to follow outdated patterns

**Correct Approach:**
- Document decisions that cross epic boundaries
- Focus on conflict-prone areas
- Update architecture as you learn
- Use `correct-course` for significant changes

---

## 3 Design Principles

### 3.1 Facilitation Over Generation

BMad workflows take a fundamentally different approach from typical AI prompts. Instead of generating solutions directly, workflows act as facilitators who guide you through discovery processes, helping you arrive at insights and decisions yourself.

#### The Problem with Generation

Traditional AI approaches to creative and knowledge work typically follow this pattern:

**User:** "I need a comprehensive UX design for my e-commerce app"

**AI:** [Immediately generates] "Here's a complete UX specification with modern dark theme, card-based product grid, left navigation, and checkout flow..."

This approach:
- Produces generic, predictable outputs that may not fit your actual needs
- Removes your ownership and understanding of the solution
- Misses critical context, constraints, and nuance
- Limits creative exploration to the AI's training data patterns
- Creates deliverables you can't explain or iterate on effectively

#### The Facilitation Approach

Facilitative workflows use strategic questioning and guided discovery:

**User:** "I need a comprehensive UX design for my e-commerce app"

**Workflow:** "Welcome! I'll act as your UX facilitator to help you discover the right approach. First, let me understand what documents you already have—do you have a product brief, PRD, or any research?"

**User:** "I have a product brief and some user research"

**Workflow:** "Great! Let me load those. [Loads documents] Now, what are the primary user goals for your e-commerce experience? What should users be able to accomplish?"

This approach:
- Draws out insights and expertise already within you
- Maintains your ownership and understanding of decisions
- Captures your specific context, constraints, and goals
- Enables deeper exploration of your unique situation
- Creates outputs you can confidently explain and iterate on

#### Key Principles

**1. Questions Over Answers**

Facilitative workflows ask strategic questions rather than providing direct answers. This:
- Activates your own creative and analytical thinking
- Uncovers assumptions you didn't know you had
- Reveals blind spots in your understanding
- Builds on your domain expertise and context

**2. Multi-Turn Conversation**

Facilitation uses progressive discovery, not interrogation:
- Ask 1-2 questions at a time, not laundry lists
- Think about responses before asking follow-ups
- Probe to understand deeper, not just collect facts
- Use conversation to explore, not just extract

**3. Intent-Based Guidance**

Workflows specify goals and approaches, not exact scripts:
- "Guide the user through discovering X" (intent)
- NOT "Say exactly: 'What is X?'" (prescriptive)

This allows the workflow to adapt naturally to your responses while maintaining structured progress.

**4. Process Trust**

Facilitative workflows use proven methodologies:
- Design Thinking's phases (Empathize, Define, Ideate, Prototype, Test)
- Structured brainstorming and creativity techniques
- Root cause analysis frameworks
- Innovation strategy patterns

You're not just having a conversation—you're following time-tested processes adapted to your specific situation.

**5. YOU Are the Expert**

Facilitative workflows operate on a core principle: **you are the expert on your situation**. The workflow brings:
- Process expertise (how to think through problems)
- Facilitation skills (how to guide exploration)
- Technique knowledge (proven methods and frameworks)

You bring:
- Domain knowledge (your specific field or industry)
- Context understanding (your unique situation and constraints)
- Decision authority (what will actually work for you)

#### When Generation is Appropriate

Facilitative workflows DO generate when appropriate:
- Synthesizing and structuring outputs after you've made decisions
- Documenting your choices and rationale
- Creating structured artifacts based on your input
- Providing technique examples or option templates
- Formatting and organizing your conclusions

But the **core creative and analytical work** happens through facilitated discovery, not generation.

#### The Distinction: Facilitator vs Generator

| Facilitative Workflow                 | Generative AI                           |
| ------------------------------------- | --------------------------------------- |
| "What are your goals?"                | "Here's the solution"                   |
| Asks 1-2 questions at a time          | Produces complete output immediately    |
| Multiple turns, progressive discovery | Single turn, bulk generation            |
| "Let me understand your context"      | "Here's a generic answer"               |
| Offers options, you choose            | Makes decisions for you                 |
| Documents YOUR reasoning              | No reasoning visible                    |
| You can explain every decision        | You can't explain why choices were made |
| Ownership and understanding           | Outputs feel alien                      |

#### Benefits

**For Individuals:**
- **Deeper insights** than pure generation—ideas connect to your actual knowledge
- **Full ownership** of creative outputs and decisions
- **Skill development** in structured thinking and problem-solving
- **More memorable and actionable** results—you understand the "why"

**For Teams:**
- **Shared creative experience** building alignment and trust
- **Aligned understanding** through documented exploration
- **Documented rationale** for future reference and onboarding
- **Stronger buy-in** to outcomes because everyone participated in discovery

**For Implementation:**
- **Outputs match reality** because they emerged from your actual constraints
- **Easier iteration** because you understand the reasoning behind choices
- **Confident implementation** because you can defend every decision
- **Reduced rework** because facilitation catches issues early

---

### 3.2 Testing as Engineering

AI-generated tests frequently fail in production because they lack systematic quality standards. This document explains the problem and presents a solution combining three components: Playwright-Utils, TEA (Test Architect), and Playwright MCPs.

#### The Problem with AI-Generated Tests

When teams use AI to generate tests without structure, they often produce what can be called "slop factory" outputs:

| Issue | Description |
|-------|-------------|
| Redundant coverage | Multiple tests covering the same functionality |
| Incorrect assertions | Tests that pass but don't actually verify behavior |
| Flaky tests | Non-deterministic tests that randomly pass or fail |
| Unreviewable diffs | Generated code too verbose or inconsistent to review |

The core problem is that prompt-driven testing paths lean into nondeterminism, which is the exact opposite of what testing exists to protect.

**The Paradox:** AI excels at generating code quickly, but testing requires precision and consistency. Without guardrails, AI-generated tests amplify the chaos they're meant to prevent.

#### The Solution: A Three-Part Stack

The solution combines three components that work together to enforce quality:

**1. Playwright-Utils**

Bridges the gap between Cypress ergonomics and Playwright's capabilities by standardizing commonly reinvented primitives through utility functions:

- api-request - API calls with schema validation
- auth-session - Authentication handling
- intercept-network-call - Network mocking and interception
- recurse - Retry logic and polling
- log - Structured logging
- network-recorder - Record and replay network traffic
- burn-in - Smart test selection for CI
- network-error-monitor - HTTP error detection
- file-utils - CSV/PDF handling

These utilities eliminate the need to reinvent authentication, API calls, retries, and logging for every project.

**2. TEA (Test Architect Agent)**

A quality operating model packaged as eight executable workflows spanning test design, CI/CD gates, and release readiness. TEA encodes test architecture expertise into repeatable processes:

- `*test-design` - Risk-based test planning per epic
- `*framework` - Scaffold production-ready test infrastructure
- `*ci` - CI pipeline with selective testing
- `*atdd` - Acceptance test-driven development
- `*automate` - Prioritized test automation
- `*test-review` - Test quality audits (0-100 score)
- `*nfr-assess` - Non-functional requirements assessment
- `*trace` - Coverage traceability and gate decisions

**Key Insight:** TEA doesn't just generate tests—it provides a complete quality operating model with workflows for planning, execution, and release gates.

**3. Playwright MCPs**

Model Context Protocols enable real-time verification during test generation. Instead of inferring selectors and behavior from documentation, MCPs allow agents to:

- Run flows and confirm the DOM against the accessibility tree
- Validate network responses in real-time
- Discover actual functionality through interactive exploration
- Verify generated tests against live applications

#### How They Work Together

The three components form a quality pipeline:

| Stage | Component | Action |
|-------|-----------|--------|
| Standards | Playwright-Utils | Provides production-ready patterns and utilities |
| Process | TEA Workflows | Enforces systematic test planning and review |
| Verification | Playwright MCPs | Validates generated tests against live applications |

**Before (AI-only):** 20 tests with redundant coverage, incorrect assertions, and flaky behavior.

**After (Full Stack):** Risk-based selection, verified selectors, validated behavior, reviewable code.

#### Why This Matters

Traditional AI testing approaches fail because they:

- **Lack quality standards** — No consistent patterns or utilities
- **Skip planning** — Jump straight to test generation without risk assessment
- **Can't verify** — Generate tests without validating against actual behavior
- **Don't review** — No systematic audit of generated test quality

The three-part stack addresses each gap:

| Gap | Solution |
|-----|----------|
| No standards | Playwright-Utils provides production-ready patterns |
| No planning | TEA `*test-design` workflow creates risk-based test plans |
| No verification | Playwright MCPs validate against live applications |
| No review | TEA `*test-review` audits quality with scoring |

This approach is sometimes called *context engineering*—loading domain-specific standards into AI context automatically rather than relying on prompts alone. TEA's `tea-index.csv` manifest loads relevant knowledge fragments so the AI doesn't relearn testing patterns each session.

---

## 4 TEA Principles

### 4.1 Risk-Based Testing Philosophy

Risk-based testing is TEA's core principle: testing depth scales with business impact. Instead of testing everything equally, focus effort where failures hurt most.

#### The Problem

**Equal Testing for Unequal Risk**

Traditional testing approaches treat all features equally:
- Every feature gets same test coverage
- Same level of scrutiny regardless of impact
- No systematic prioritization
- Testing becomes checkbox exercise

**No Objective Prioritization**

Without risk-based testing:
- Subjective decisions, no data
- Political debates about what to test
- No guidance on when you have enough tests

#### The Solution: Probability × Impact Scoring

**Risk Score = Probability × Impact**

**Probability** (How likely to fail?)
- **1 (Low):** Stable, well-tested, simple logic
- **2 (Medium):** Moderate complexity, some unknowns
- **3 (High):** Complex, untested, many edge cases

**Impact** (How bad if it fails?)
- **1 (Low):** Minor inconvenience, few users affected
- **2 (Medium):** Degraded experience, workarounds exist
- **3 (High):** Critical path broken, business impact

**Score Range:** 1-9

#### Risk Scoring Matrix

| Impact | Probability: 1 (Low) | Probability: 2 (Medium) | Probability: 3 (High) |
|--------|---------------------|------------------------|----------------------|
| **3 (High)** | Score: 3 (Low Risk) | Score: 6 (HIGH RISK - Mitigation Required) | Score: 9 (CRITICAL - Blocks Release) |
| **2 (Medium)** | Score: 2 (Low Risk) | Score: 4 (Medium Risk) | Score: 6 (HIGH RISK - Mitigation Required) |
| **1 (Low)** | Score: 1 (Low Risk) | Score: 2 (Low Risk) | Score: 3 (Low Risk) |

**Legend:**
- 🔴 Red (Score 9): CRITICAL - Blocks release
- 🟠 Orange (Score 6-8): HIGH RISK - Mitigation required
- 🟡 Yellow (Score 4-5): MEDIUM - Mitigation recommended
- 🟢 Green (Score 1-3): LOW - Optional mitigation

#### Test Priorities (P0-P3)

Risk scores inform test priorities (but aren't the only factor):

**P0 - Critical Path**
- **Risk Scores:** Typically 6-9 (high risk)
- **Coverage Target:** 100%
- **Test Levels:** E2E + API
- **Example:** Login, checkout, payment processing

**P1 - High Value**
- **Risk Scores:** Typically 4-6 (medium-high risk)
- **Coverage Target:** 90%
- **Test Levels:** API + selective E2E
- **Example:** Profile editing, search, filters

**P2 - Medium Value**
- **Risk Scores:** Typically 2-4 (medium risk)
- **Coverage Target:** 50%
- **Test Levels:** API happy path only
- **Example:** Export features, advanced settings

**P3 - Low Value**
- **Risk Scores:** Typically 1-2 (low risk)
- **Coverage Target:** 20% (smoke test)
- **Test Levels:** E2E smoke test only
- **Example:** Theme customization, experimental features

#### Mitigation Plans

**Scores ≥6 require documented mitigation:**

**Gate Rules:**
- **Score = 9** (Critical): Mandatory FAIL - blocks release without mitigation
- **Score 6-8** (High): Requires mitigation plan, becomes CONCERNS if incomplete
- **Score 4-5** (Medium): Mitigation recommended but not required
- **Score 1-3** (Low): No mitigation needed

#### When to Use Risk-Based Testing

**Always Use For:**
- Enterprise projects (high stakes, revenue, compliance, security)
- Large codebases (can't test everything exhaustively)
- Regulated industries (must justify testing decisions)

**Consider Skipping For:**
- Tiny projects (5 features total, can test everything thoroughly)
- Prototypes (throw-away code, speed over quality)

---

### 4.2 Test Quality Standards

Test quality standards define what makes a test "good" in TEA. These aren't suggestions - they're the Definition of Done that prevents tests from rotting in review.

#### TEA's Quality Principles

- **Deterministic** - Same result every run
- **Isolated** - No dependencies on other tests
- **Explicit** - Assertions visible in test body
- **Focused** - Single responsibility, appropriate size
- **Fast** - Execute in reasonable time

**Why these matter:** Tests that violate these principles create maintenance burden, slow down development, and lose team trust.

#### The Problem

**Tests That Rot in Review**

AI-generated tests without quality guardrails often produce:
- Hard waits (`waitForTimeout`) - Flaky, wastes time
- Conditionals for flow control - Non-deterministic behavior
- Try-catch for flow control - Hides failures
- Too large - Hard to maintain
- Vague names - Unclear purpose
- No explicit assertions - What's being tested?

**Result:** PR review comments: "This test is flaky, please fix" → never merged → test deleted → coverage lost

#### The Solution: TEA's Quality Standards

**1. Determinism (No Flakiness)**

**Rule:** Test produces same result every run.

**Requirements:**
- ❌ No hard waits (`waitForTimeout`)
- ❌ No conditionals for flow control (`if/else`)
- ❌ No try-catch for flow control
- ✅ Use network-first patterns (wait for responses)
- ✅ Use explicit waits (waitForSelector, waitForResponse)

**2. Isolation (No Dependencies)**

**Rule:** Test runs independently, no shared state.

**Requirements:**
- ✅ Self-cleaning (cleanup after test)
- ✅ No global state dependencies
- ✅ Can run in parallel
- ✅ Can run in any order
- ✅ Use unique test data

**3. Explicit Assertions (No Hidden Validation)**

**Rule:** Assertions visible in test body, not abstracted.

**Requirements:**
- ✅ Assertions in test code (not helper functions)
- ✅ Specific assertions (not generic `toBeTruthy`)
- ✅ Meaningful expectations (test actual behavior)

**4. Focused Tests (Appropriate Size)**

**Rule:** Test has single responsibility, reasonable size.

**Requirements:**
- ✅ Test size < 300 lines
- ✅ Single responsibility (test one thing well)
- ✅ Clear describe/test names
- ✅ Appropriate scope (not too granular, not too broad)

**5. Fast Execution (Performance Budget)**

**Rule:** Individual test executes in < 1.5 minutes.

**Requirements:**
- ✅ Test execution < 90 seconds
- ✅ Efficient selectors (getByRole > XPath)
- ✅ Minimal redundant actions
- ✅ Parallel execution enabled

#### TEA's Quality Scoring

TEA reviews tests against these standards in `*test-review`:

**Scoring Categories (100 points total):**
- **Determinism (35 points):** No hard waits (10), No conditionals (10), No try-catch flow (10), Network-first patterns (5)
- **Isolation (25 points):** Self-cleaning (15), No global state (5), Parallel-safe (5)
- **Assertions (20 points):** Explicit in test body (10), Specific and meaningful (10)
- **Structure (10 points):** Test size < 300 lines (5), Clear naming (5)
- **Performance (10 points):** Execution time < 1.5 min (10)

**Score Interpretation:**
- **90-100:** Excellent - Production-ready, minimal changes
- **80-89:** Good - Minor improvements recommended
- **70-79:** Acceptable - Address recommendations before release
- **60-69:** Needs Work - Fix critical issues
- **< 60:** Critical - Significant refactoring needed

---

### 4.3 Fixture Architecture Pattern

Fixture architecture is TEA's pattern for building reusable, testable, and composable test utilities. The core principle: build pure functions first, wrap in framework fixtures second.

#### The Pattern

1. Write utility as pure function (unit-testable)
2. Wrap in framework fixture (Playwright, Cypress)
3. Compose fixtures with mergeTests (combine capabilities)
4. Package for reuse across projects

#### Why This Order?

- Pure functions are easier to test
- Fixtures depend on framework (less portable)
- Composition happens at fixture level
- Reusability maximized

#### The Problem

**Framework-First Approach (Common Anti-Pattern)**

Building utilities as fixtures from the start:
- Cannot unit test (requires Playwright context)
- Tied to framework (not reusable in other tools)
- Hard to compose with other fixtures
- Difficult to mock for testing the utility itself

**Copy-Paste Utilities**

Repeating the same code in every test:
- Code duplication (violates DRY)
- Inconsistent error handling
- Hard to update (change 50 tests)
- No shared behavior

#### The Solution: Three-Step Pattern

**Step 1: Pure Function**

Write utility as pure function with dependency injection:

```typescript
// helpers/api-request.ts
export async function apiRequest({
  request,  // Passed in (dependency injection)
  method,
  url,
  data,
  headers = {}
}: ApiRequestParams): Promise<ApiResponse> {
  // Pure function logic
  // ✅ Can unit test this function!
}
```

**Step 2: Fixture Wrapper**

Wrap pure function in framework fixture:

```typescript
// fixtures/api-request.ts
export const test = base.extend<{ apiRequest: typeof apiRequestFn }>({
  apiRequest: async ({ request }, use) => {
    // Inject framework dependency (request)
    await use((params) => apiRequestFn({ request, ...params }));
  }
});
```

**Step 3: Composition with mergeTests**

Compose all fixtures into one test:

```typescript
// fixtures/index.ts
export const test = mergeTests(
  apiRequestTest,
  authSessionTest,
  logTest
);
```

**Usage:**
```typescript
test('should update profile', async ({ apiRequest, authToken, log }) => {
  // Use multiple fixtures in one test
});
```

#### Benefits

- Each fixture is unit-testable
- Compose only what you need
- Reuse individual fixtures
- Easy to maintain (small files)
- Can swap frameworks by changing wrapper only

---

### 4.4 Network-First Patterns

Network-first patterns are TEA's solution to test flakiness. Instead of guessing how long to wait with fixed timeouts, wait for the actual network event that causes UI changes.

#### The Core Principle

**UI changes because APIs respond. Wait for the API response, not an arbitrary timeout.**

#### The Problem

**Hard Waits Create Flakiness**

```typescript
// ❌ The flaky test pattern
await page.click('button');
await page.waitForTimeout(2000);  // Hope 2 seconds is enough
await expect(page.locator('.success')).toBeVisible();
```

**Why this fails:**
- Fast network: Wastes 1.5 seconds waiting
- Slow network: Not enough time, test fails
- CI environment: Slower than local, fails randomly
- Under load: API takes 3 seconds, test fails

**Result:** "Works on my machine" syndrome, flaky CI.

#### The Solution: Intercept-Before-Navigate

**Network-First Approach:**

```typescript
// ✅ Good: Network-first pattern
const responsePromise = page.waitForResponse(
  resp => resp.url().includes('/api/submit') && resp.ok()
);

await page.click('button');
await responsePromise;  // Wait for actual response
await expect(page.locator('.success')).toBeVisible();
```

**Why this works:**
- Wait set up BEFORE navigation (no race)
- Wait for actual API response (deterministic)
- No fixed timeout (fast when API is fast)
- Validates API response (catch backend errors)

#### Intercept-Before-Navigate Pattern

**Key insight:** Set up wait BEFORE triggering the action.

**Pattern: Intercept → Action → Await**

```typescript
// 1. Intercept (set up wait)
const promise = page.waitForResponse(matcher);

// 2. Action (trigger request)
await page.click('button');

// 3. Await (wait for actual response)
await promise;
```

**Why this order:**
- `waitForResponse()` starts listening immediately
- Then trigger the action that makes the request
- Then wait for the promise to resolve
- No race condition possible

#### Common Misconceptions

**"I Already Use waitForSelector"**

```typescript
// This is still a hard wait in disguise
await page.click('button');
await page.waitForSelector('.success', { timeout: 5000 });
```

**Problem:** Waiting for DOM, not for the API that caused DOM change.

**Better:**
```typescript
await page.waitForResponse(matcher);  // Wait for root cause
await page.waitForSelector('.success');  // Then validate UI
```

**"My Tests Are Fast, Why Add Complexity?"**

**Short-term:** Tests are fast locally

**Long-term problems:**
- Different environments (CI slower)
- Under load (API slower)
- Network variability (random)
- Scaling test suite (100 → 1000 tests)

**Network-first prevents these issues before they appear.**

---

### 4.5 Knowledge Base System

TEA's knowledge base system is how context engineering works - automatically loading domain-specific standards into AI context so tests are consistently high-quality regardless of prompt variation.

#### The Problem

**Prompt-Driven Testing = Inconsistency**

Without a knowledge base:
- Quality depends on prompt engineering skill
- No consistency across sessions
- Team A uses pattern X, Team B uses pattern Y
- Patterns drift over time
- No single source of truth

#### The Solution: tea-index.csv Manifest

**How It Works:**

1. **Manifest Defines Fragments**

`src/bmm/testarch/tea-index.csv`:
```csv
id,name,description,tags,fragment_file
test-quality,Test Quality,Execution limits and isolation rules,quality;standards,knowledge/test-quality.md
network-first,Network-First Safeguards,Intercept-before-navigate workflow,network;stability,knowledge/network-first.md
fixture-architecture,Fixture Architecture,Composable fixture patterns,fixtures;architecture,knowledge/fixture-architecture.md
```

2. **Workflow Loads Relevant Fragments**

When user runs `*atdd`:
- TEA reads tea-index.csv
- Identifies fragments needed for ATDD
- Loads only these fragments (not all 33)
- Generates tests following these patterns

3. **Consistent Output**

Every time `*atdd` runs:
- Same fragments loaded
- Same patterns applied
- Same quality standards
- Consistent test structure

**Result:** Tests look like they were written by the same expert, every time.

#### Fragment Structure

Each fragment follows this structure:

```markdown
# Fragment Name

## Principle
[One sentence - what is this pattern?]

## Rationale
[Why use this instead of alternatives?]

## Pattern Examples
[Code examples showing the pattern]

## Anti-Patterns
[What not to do and why]
```

#### Workflow-Specific Loading

**Different workflows load different fragments:**

| Workflow | Fragments Loaded | Purpose |
|----------|-----------------|---------|
| `*framework` | fixture-architecture, playwright-config, fixtures-composition | Infrastructure patterns |
| `*test-design` | test-quality, test-priorities-matrix, risk-governance | Planning standards |
| `*atdd` | test-quality, component-tdd, network-first, data-factories | TDD patterns |
| `*automate` | test-quality, test-levels-framework, selector-resilience | Comprehensive generation |
| `*test-review` | All quality/resilience/debugging fragments | Full audit patterns |

**Benefit:** Only load what's needed (focused context, no bloat).

#### Benefits of Knowledge Base System

**1. Consistency**

**Before:** Test quality varies by who wrote it  
**After:** All tests follow same patterns (TEA-generated or reviewed)

**2. Onboarding**

**Before:** New team member reads 20 documents, asks 50 questions  
**After:** New team member runs `*atdd`, sees patterns in generated code, learns by example

**3. Quality Gates**

**Before:** "Is this test good?" → subjective opinion  
**After:** "*test-review" → objective score against knowledge base

**4. Pattern Evolution**

**Before:** Update tests manually across 100 files  
**After:** Update fragment once, all new tests use new pattern

**5. Cross-Project Reuse**

**Before:** Reinvent patterns for each project  
**After:** Same fragments across all BMad projects (consistency at scale)

---

For detailed practical guides on using these concepts, see:
- [BMad Know-How Document](./bmad_knowhow.md) - Practical workflows and procedures
- [BMad Method Documentation](../BMAD-METHOD/docs/index.md) - Complete reference
