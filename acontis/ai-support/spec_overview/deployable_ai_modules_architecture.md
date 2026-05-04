# Deployable AI Modules Platform Architecture

**Document type:** Internal technical architecture document  
**Status:** Draft  
**Date:** 2026-05-03  
**Scope:** General platform, deployment, module, adapter, and roadmap architecture  
**Application-specific scope:** Intentionally excluded except where needed as examples

---

## 1. Purpose

This document defines a general implementation approach for a product that can run deployable AI application modules in different customer environments.

The first release will contain one concrete application module, but the architecture must not be limited to that module. The long-term goal is to create a reusable platform foundation that can support multiple AI modules, multiple deployment models, and different levels of customer or vendor responsibility for LLMs, RAG systems, storage, payment, licensing, and integrations.

The architecture must support the following starting point:

```text
Release 1 = Deployment V1 + Application V1 + AI Responsibility Mode B1
```

Where:

```text
Deployment V1: Local customer-hosted deployment, for example via Docker
Application V1: First paid application module, concrete functionality intentionally abstract here
AI Responsibility B1: Customer provides both LLM and RAG system
```

The design should also preserve a road toward managed cloud hosting, hybrid deployments, integrated local LLM/RAG components, and multiple application modules.

---

## 2. Product Vision

The product should evolve from a single local AI application into a platform for deployable AI modules.

The platform should provide common capabilities that every module can reuse:

```text
- Configuration
- Licensing and entitlements
- LLM access
- RAG access
- Input resources
- Output artifacts
- Logging and diagnostics
- Adapter management
- Deployment packaging
```

Application modules should focus only on their domain logic. They must not directly implement infrastructure concerns such as LLM integration, RAG integration, payment handling, file system access, secrets handling, or deployment-specific behavior.

The guiding principle is:

```text
Build Release 1 as a focused product, but draw its boundaries so that it can become a platform.
```

---

## 3. Core Architectural Principle

The central architectural principle is separation between:

```text
1. Deployment architecture
2. AI responsibility model
3. Application module functionality
4. Platform-provided interfaces
5. Customer-specific provider adapters
```

These concerns must not be mixed.

A module should not know whether it runs:

```text
- locally on a customer computer
- on a customer server
- in a managed cloud environment
- in a hybrid deployment
```

A module should not know whether an LLM is:

```text
- local
- cloud-based
- customer-hosted
- vendor-hosted
- accessed through a custom adapter
```

A module should only depend on stable platform interfaces.

---

## 4. Version Axes

The roadmap should not be modeled as one linear sequence such as V1 -> V2 -> V3. Instead, the product evolves along several independent axes.

### 4.1 Axis A: Deployment Architecture

```text
A1: Local deployment
A2: Managed cloud deployment
A3: Hybrid deployment
```

#### A1: Local Deployment

The customer runs the product locally, for example on a workstation, local server, or internal VM.

Characteristics:

```text
- Customer controls runtime environment
- Customer controls data
- Customer provides external AI infrastructure in the first release
- Docker-based packaging is preferred
- Offline or limited-connectivity scenarios should be considered
```

#### A2: Managed Cloud Deployment

The company hosts and maintains the product for the customer in a cloud environment.

Characteristics:

```text
- Company operates infrastructure
- Customer does not manage Docker/runtime updates
- Multi-tenant or single-tenant cloud architecture may be used
- Stronger requirements for security, monitoring, backups, tenant isolation, and uptime
```

#### A3: Hybrid Deployment

The product is split into a managed control plane and a customer-controlled data plane.

Characteristics:

```text
- Company may host UI, configuration, billing, monitoring, and management
- Customer may host sensitive data, local LLMs, RAG systems, and connectors
- Useful for enterprise customers requiring privacy and control
```

---

### 4.2 Axis B: AI Responsibility Model

```text
B1: Customer provides LLM and RAG
B1.5: Customer provides LLM/RAG, platform provides guided configuration and diagnostics
B2: Customer provides LLM, platform provides optional RAG
B3: Platform provides managed LLM and RAG
B4: Product ships with integrated local LLM and/or RAG components
```

#### B1: Customer Provides LLM and RAG

This is the required mode for the first release.

Characteristics:

```text
- Customer provides LLM endpoint
- Customer provides RAG endpoint if the application requires RAG
- Platform only consumes these services through documented interfaces
- Lowest responsibility for the vendor
- Highest setup responsibility for the customer
```

#### B1.5: Guided Configuration

The platform still does not own the LLM or RAG stack, but it makes setup easier.

Examples:

```text
- Tested configuration templates
- Endpoint validation
- Model capability checks
- Health diagnostics
- Recommended local LLM/RAG setups
- Clear error messages
```

#### B2: Optional Platform-Provided RAG

The customer may still bring their own LLM, but the platform can provide a built-in or managed RAG component.

This may be useful when customers do not want to maintain retrieval infrastructure but still want to control generation models.

#### B3: Managed LLM and RAG

The platform provides the complete AI stack.

Characteristics:

```text
- Highest convenience
- Highest vendor responsibility
- Requires cost control, data privacy controls, and operational monitoring
- Fits managed cloud deployment especially well
```

#### B4: Integrated Local LLM and/or RAG

The product ships with a configurable local LLM and/or local RAG stack.

Characteristics:

```text
- Improves local ease of use
- Reduces customer need to understand models, embeddings, and RAG internals
- Introduces hardware, performance, model update, and quality responsibilities
- May require large downloads, GPU/CPU fallback, memory checks, and model selection logic
```

B4 should be treated as a significant product responsibility layer, not as a small feature.

---

### 4.3 Axis C: Application Module Layer

```text
C1: First paid application module
C2: Second application module
C3: Additional modules
C4: Module ecosystem or marketplace-style extension model
```

Application modules are the domain-specific units of value.

Examples could include:

```text
- Data transformation workflows
- Knowledge-base generation
- Support automation
- Quality evaluation
- Document analysis
- Reporting
- Domain-specific assistants
```

The exact first application is intentionally out of scope for this document. The architecture must allow it to be replaced or supplemented by future modules.

---

## 5. Release 1 Definition

Release 1 is the smallest commercially useful product release.

```text
Release 1 = A1 + B1 + C1
```

Meaning:

```text
- Local customer-hosted deployment
- Customer provides LLM
- Customer provides RAG if required by the application
- One paid application module is included
- Platform foundation is intentionally minimal but reusable
```

### 5.1 Release 1 Goals

```text
- Run locally via Docker or Docker Compose
- Provide a stable module execution runtime
- Provide platform interfaces for common AI module needs
- Allow the first application module to use customer-provided LLM/RAG systems
- Avoid hard-coding application logic into deployment, licensing, or connector layers
- Provide logs and diagnostics sufficient for customer-side support
```

### 5.2 Release 1 Non-Goals

```text
- No managed cloud operation
- No complex multi-tenant SaaS architecture
- No plugin marketplace
- No dynamic in-process plugin loading
- No built-in LLM/RAG stack unless explicitly required later
- No direct Paddle dependency inside application modules
- No application-specific infrastructure coupling
```

---

## 6. High-Level Architecture

```text
+-------------------------------------------------------------+
|                    Platform Runtime                         |
|                                                             |
|  +-------------------+     +-----------------------------+  |
|  | Application       |     | Platform Core               |  |
|  | Module(s)         | --> | - Config                    |  |
|  |                   |     | - Entitlements              |  |
|  | Domain logic only |     | - LLM interface             |  |
|  +-------------------+     | - RAG interface             |  |
|                            | - Input resources           |  |
|                            | - Output artifacts          |  |
|                            | - Diagnostics/logging       |  |
|                            +-----------------------------+  |
|                                      |                      |
|                                      v                      |
|                            +-----------------------------+  |
|                            | Provider Clients            |  |
|                            +-----------------------------+  |
+--------------------------------------|----------------------+
                                       |
                                       v
+-------------------------------------------------------------+
|                 External Provider Adapters                  |
|                                                             |
|  - LLM adapter service                                      |
|  - RAG adapter service                                      |
|  - Input adapter service                                    |
|  - Output adapter service                                   |
|  - Customer-specific integration services                   |
+-------------------------------------------------------------+
```

The platform runtime owns standard interfaces. External provider adapters implement those interfaces for specific customer systems.

---

## 7. Platform Core

The platform core is the reusable base that all application modules use.

### 7.1 Required Core Responsibilities

```text
- Load and validate configuration
- Manage secrets through controlled mechanisms
- Check license and entitlement status
- Provide LLM interface to modules
- Provide RAG interface to modules
- Provide input resource interface
- Provide output artifact interface
- Provide diagnostics and structured logging
- Provide error handling, timeouts, and retry policies
- Provide health checks for configured providers
- Provide module execution lifecycle
```

### 7.2 Recommended Initial Technology Baseline

For Release 1:

```text
Language: Python
Backend/API: FastAPI if a local API or UI is needed
CLI: Python CLI, for example Typer or argparse
Packaging: Docker / Docker Compose
Storage: Local filesystem and/or SQLite
Configuration: YAML or TOML
LLM/RAG integration: HTTP-based provider interfaces
Logging: Structured logs
Licensing: Local license or entitlement file, independent from module logic
```

The frontend may be deferred if a CLI-first product is sufficient. If a UI is needed, a local browser UI backed by FastAPI is preferred.

---

## 8. Application Module Contract

Application modules define domain behavior. They must not implement platform responsibilities internally.

A module should declare its required capabilities, for example:

```yaml
module:
  id: application_v1
  name: First Application Module
  version: 1.0.0
  requires:
    - llm.chat
    - rag.retrieve
    - inputs.read
    - artifacts.write
    - entitlements.check
    - diagnostics.log
```

The platform checks these requirements before executing the module.

### 8.1 Modules Are Allowed To Do

```text
- Define domain-specific workflow logic
- Transform inputs into outputs
- Create prompts or structured requests
- Ask platform interfaces for LLM/RAG/input/output services
- Return structured results and metadata
- Report progress through platform diagnostics
```

### 8.2 Modules Must Not Do Directly

Application modules must not directly handle:

```text
- LLM interfacing
- RAG interfacing
- Payment handling
- License validation
- Quota enforcement
- Secrets handling
- Environment variable parsing
- Configuration file parsing
- Direct file system access
- Direct database access
- Direct external HTTP calls unless routed through approved platform interfaces
- Logging implementation
- Monitoring implementation
- Retry and timeout policy
- Deployment-specific behavior
- User authentication
- Authorization and permission checks
- Job scheduling and concurrency primitives
```

This protects portability and allows modules to run under local, cloud, or hybrid deployments without modification.

---

## 9. Minimal Platform Interfaces

The initial platform should provide a small set of stable interfaces that cover most future AI modules.

### 9.1 LLM Interface

Purpose:

```text
Provide text generation, chat, and potentially structured output capabilities.
```

Initial capability:

```text
llm.chat
```

Potential future capabilities:

```text
llm.structured_output
llm.tool_call
llm.embeddings
llm.model_info
```

### 9.2 RAG Interface

Purpose:

```text
Retrieve relevant context from a customer-provided or platform-provided knowledge system.
```

Initial capability:

```text
rag.retrieve
```

Potential future capabilities:

```text
rag.index
rag.delete
rag.workspace_info
rag.query_with_filters
```

### 9.3 Entitlement Interface

The module should not know whether entitlement comes from Paddle, a local license file, an enterprise contract, or an offline activation.

Purpose:

```text
Check whether an operation is allowed and record usage if needed.
```

Initial capabilities:

```text
entitlements.check
entitlements.require
entitlements.record_usage
```

This is broader and more useful than a narrow billing interface.

### 9.4 Input Resource Interface

Purpose:

```text
Give modules access to input data without exposing storage details.
```

Initial capabilities:

```text
inputs.list
inputs.read
inputs.metadata
```

Possible input sources:

```text
- Mounted local folder
- Uploaded ZIP file
- Database export
- Ticketing system export
- Customer adapter service
- Cloud storage in later deployment versions
```

### 9.5 Output Artifact Interface

Purpose:

```text
Allow modules to write outputs without knowing the target storage or export format implementation.
```

Initial capabilities:

```text
artifacts.create
artifacts.write
artifacts.finalize
```

Possible output targets:

```text
- Local folder
- JSONL export
- Markdown export
- CSV export
- ZIP package
- Database rows
- RAG import package
- External system adapter
```

### 9.6 Diagnostics Interface

Purpose:

```text
Provide consistent logging, progress reporting, health checks, and support diagnostics.
```

Initial capabilities:

```text
diagnostics.log
diagnostics.progress
diagnostics.warning
diagnostics.error
```

Diagnostics should be included in Release 1. Without it, local customer deployments become difficult to support.

---

## 10. Provider / Adapter Model

The platform defines interfaces. Providers implement those interfaces.

```text
Interface: What the platform needs
Provider: A configured implementation of that interface
Adapter: The code or service that connects the provider to a concrete customer system
```

Examples:

```text
LLM interface
- OpenAI-compatible provider
- Ollama provider
- Claude provider
- Customer custom HTTP provider

RAG interface
- Simple HTTP retrieval provider
- AnythingLLM provider
- Customer custom RAG provider

Input interface
- Local folder provider
- ZIP file provider
- Customer ticket export provider

Output interface
- Local folder provider
- JSONL provider
- Markdown provider
- Customer import provider
```

The key rule is:

```text
Customers implement adapters, not application modules.
```

This keeps application logic generic and prevents customer-specific integrations from polluting the module layer.

---

## 11. Adapter Strategy V1: External HTTP Services

For Release 1, customer-specific integrations should run outside the platform as external HTTP services.

```text
Platform container -> HTTP -> Customer adapter service
```

### 11.1 Rationale

External HTTP adapters are preferred because they provide:

```text
- Stronger isolation
- Language independence
- Easier customer ownership
- Better compatibility with local, cloud, and hybrid deployments
- Reduced risk of customer code crashing the platform
- Cleaner security boundary for customer secrets
```

### 11.2 Tradeoffs

External adapters introduce:

```text
- More moving parts
- Network configuration
- Timeouts and retries
- Health checks
- Service discovery or endpoint configuration
```

These tradeoffs are acceptable because the architecture is intended to support enterprise customization and future hybrid deployment.

### 11.3 Deferred Option: In-Process Plugins

In-process plugins may be considered later if there is a strong reason, such as:

```text
- Performance-critical execution
- Simplified packaging for trusted local deployments
- Offline single-binary style distribution
```

However, in-process plugins should not be part of the initial architecture.

---

## 12. Configuration Model

The platform should be driven by explicit configuration.

Example conceptual configuration:

```yaml
deployment:
  mode: local

license:
  mode: local_license_file
  license_file: ./license.json

providers:
  llm:
    type: http
    endpoint: http://host.docker.internal:11434/v1/chat/completions
    auth: optional

  rag:
    type: http
    endpoint: http://host.docker.internal:3001/retrieve
    auth: optional

  inputs:
    type: local_folder
    path: /data/input

  artifacts:
    type: local_folder
    path: /data/output

modules:
  application_v1:
    enabled: true
```

The exact schema should be defined later, but the principle is clear:

```text
Deployment, providers, licensing, and modules are configured outside application code.
```

---

## 13. Payment, Licensing, and Entitlements

Payment handling should be separate from application modules.

For local Release 1, the runtime should not depend on live payment calls during normal operation. Paddle or another payment provider may be used to sell licenses, subscriptions, or usage rights, but modules should only interact with the platform entitlement interface.

Recommended abstraction:

```text
Payment provider -> license/entitlement state -> platform entitlement service -> module access decision
```

Modules should never call Paddle directly.

### 13.1 Entitlement Responsibilities

```text
- Validate license or subscription state
- Check whether a module may run
- Enforce quotas if applicable
- Record usage events if needed
- Support offline/local mode where appropriate
```

### 13.2 Future Cloud Mode

In managed cloud deployment, the entitlement service may connect directly to Paddle webhooks, subscription state, customer accounts, and usage billing.

The module interface should remain unchanged.

---

## 14. Deployment Evolution Roadmap

The deployment roadmap can evolve independently from application modules.

### 14.1 Deployment A1: Local Docker

```text
- Docker or Docker Compose package
- Local configuration
- Local license file or activation
- Customer-provided LLM/RAG endpoints
- Local input/output volumes
```

### 14.2 Deployment A2: Managed Cloud

```text
- Company-hosted runtime
- Customer tenants or dedicated instances
- Managed updates
- Centralized monitoring
- Cloud storage and database
- Integrated billing and customer management
```

### 14.3 Deployment A3: Hybrid Enterprise

```text
- Company-hosted control plane
- Customer-hosted data plane
- Local connectors for sensitive systems
- Cloud UI and management
- Customer-controlled LLM/RAG/data where required
```

This can become the preferred enterprise model when customers want both convenience and control.

---

## 15. AI Responsibility Roadmap

The AI responsibility model can evolve independently from deployment.

Possible steps:

```text
B1: Customer provides LLM and RAG
B1.5: Guided customer configuration
B2: Optional platform-provided RAG
B3: Fully managed LLM and RAG
B4: Integrated local LLM/RAG bundle
```

These do not need to be implemented in this exact order. Customer demand should determine the sequence.

### 15.1 Likely Development Paths

#### Enterprise-Control Path

```text
A1 + B1 -> A3 + B1 -> A3 + B2
```

Focus:

```text
- Privacy
- Customer-controlled data
- Customer-controlled AI systems
- Hybrid management
```

#### Ease-of-Use Path

```text
A1 + B1 -> A1 + B1.5 -> A1 + B4 -> A2 + B4
```

Focus:

```text
- Local setup simplicity
- Bundled components
- Less customer AI expertise required
```

#### Managed-Service Path

```text
A1 + B1 -> A2 + B1 -> A2 + B3
```

Focus:

```text
- Reduced customer operations burden
- Subscription-style managed service
- Vendor-operated infrastructure
```

---

## 16. Application Module Roadmap

Application modules can evolve independently from deployment and AI responsibility.

```text
C1: First paid module
C2: Second module
C3: Additional modules
C4: Platform for reusable deployable AI modules
```

The platform becomes real when future modules can reuse the same core capabilities without rewriting:

```text
- Configuration
- LLM access
- RAG access
- Input resource access
- Output artifact handling
- Entitlements
- Diagnostics
- Deployment packaging
```

A practical test:

```text
A second module should mostly be implemented under a new module directory, without changing platform core.
```

---

## 17. Suggested Repository Structure

Example structure:

```text
repo/
  platform/
    config/
    entitlements/
    interfaces/
      llm.py
      rag.py
      inputs.py
      artifacts.py
      diagnostics.py
    providers/
      http_llm/
      http_rag/
      local_folder_inputs/
      local_folder_artifacts/
    runtime/
    diagnostics/

  modules/
    application_v1/
      module.py
      manifest.yaml
      prompts/
      tests/

  adapters/
    examples/
      simple_http_rag_adapter/
      simple_input_adapter/

  deployment/
    docker/
    docker-compose.yml

  docs/
```

The first application module may be included in the same repository at first. Later, modules may move into separate repositories if needed.

---

## 18. Recommended Implementation Order for Release 1

```text
1. Define platform interface contracts
2. Define module manifest format
3. Define configuration schema
4. Implement local runtime and module runner
5. Implement entitlement interface with local license mode
6. Implement input resource provider for mounted local folders
7. Implement output artifact provider for mounted local folders
8. Implement LLM HTTP provider
9. Implement RAG HTTP provider if required by Application V1
10. Implement diagnostics and health checks
11. Implement Application V1 using only platform interfaces
12. Package with Docker / Docker Compose
13. Add example external HTTP adapters and documentation
14. Add automated tests for module/platform boundary
```

The order is intentionally platform-boundary-first, not UI-first.

---

## 19. Architectural Guardrails

These guardrails should be enforced throughout implementation.

```text
- Application modules depend on platform interfaces only
- Provider adapters implement interfaces but do not contain application logic
- Payment provider integration is hidden behind entitlements
- Customer-specific code belongs in adapters, not modules
- Direct infrastructure calls from modules are forbidden
- Local deployment must not prevent later cloud deployment
- Cloud deployment must not require rewriting modules
- RAG and LLM ownership must remain configurable
- Diagnostics are a first-class platform feature, not an afterthought
```

---

## 20. Key Risks

### 20.1 Overbuilding the Platform Too Early

Risk:

```text
The team spends too much time building marketplace/plugin infrastructure before proving Application V1 value.
```

Mitigation:

```text
Build only the minimal platform shell required to keep boundaries clean.
```

### 20.2 Underbuilding the Platform Boundary

Risk:

```text
Application V1 becomes tightly coupled to local files, specific LLMs, specific RAG systems, or licensing details.
```

Mitigation:

```text
Require Application V1 to use only platform interfaces.
```

### 20.3 Customer Adapter Complexity

Risk:

```text
Customers struggle to implement custom adapters if interfaces are too complex.
```

Mitigation:

```text
Keep adapter APIs small, provide examples, provide health checks, and validate configuration clearly.
```

### 20.4 Support Burden in Local Deployments

Risk:

```text
Failures in customer LLM/RAG systems appear to be product failures.
```

Mitigation:

```text
Provide diagnostics that clearly show provider reachability, latency, errors, and configuration state.
```

### 20.5 Integrated Local LLM/RAG Responsibility

Risk:

```text
Bundling LLM/RAG later creates hardware, model quality, performance, and update responsibilities.
```

Mitigation:

```text
Introduce guided configuration before full bundling, and define hardware support levels explicitly.
```

---

## 21. Open Questions

The following questions should be answered before or during detailed design.

```text
1. What is the exact module manifest schema?
2. What is the minimal HTTP contract for LLM providers?
3. What is the minimal HTTP contract for RAG providers?
4. What is the minimal input resource interface?
5. What is the minimal output artifact interface?
6. How should local license activation work?
7. Should Release 1 be CLI-first, local web UI-first, or both?
8. Which provider adapters are built in, and which are customer-owned?
9. What diagnostics must be available in the first release?
10. What must be logged for customer support without exposing sensitive data?
11. What compatibility promise should be made for module and adapter interfaces?
12. How should updates and version migrations work for local deployments?
```

---

## 22. Summary

The recommended architecture is a locally deployable platform foundation for AI modules.

The first release should be deliberately narrow:

```text
A1: Local customer-hosted deployment
B1: Customer provides LLM and RAG
C1: One paid application module
```

At the same time, the implementation must establish durable boundaries:

```text
- Application modules contain domain logic only
- Platform core provides common capabilities
- Provider adapters connect to customer systems
- External HTTP adapters are the initial extension mechanism
- Entitlements hide payment and licensing details from modules
```

This preserves future options:

```text
- Managed cloud deployment
- Hybrid enterprise deployment
- Integrated local LLM/RAG bundle
- Platform-provided RAG or fully managed AI stack
- Multiple deployable AI application modules
```

The most important success condition for the architecture is not the number of features in Release 1. It is whether Application V2 can be added later without rewriting deployment, licensing, configuration, LLM/RAG access, input handling, output handling, and diagnostics.
