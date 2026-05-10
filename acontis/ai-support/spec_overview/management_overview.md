---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
  }
  h1 {
    color: #1a5276;
  }
  h2 {
    color: #2874a6;
  }
  table {
    font-size: 0.85em;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# AI-Assisted Support System

## Management Overview

**Zammad RAG Integration for First-Response Drafting**

---

# Executive Summary & Goals

<div class="columns">
<div>

## What We're Building

AI assistant **drafts responses** based on knowledge base and historical tickets.

## Key Principles

- **Human-in-the-Loop** — every reply reviewed
- **Privacy First** — PII anonymization
- **Flexibility** — local ↔ cloud models
- **Grounded** — RAG-based responses

</div>
<div>

## Business Goals

1. **Speed up support** via AI drafts
2. **Ensure quality** through mandatory review
3. **Protect privacy** — PII stays local
4. **Stay flexible** — no vendor lock-in

</div>
</div>

---

# System Scope

<div class="columns">
<div>

## In Scope ✅

- Zammad ticket integration
- PII anonymization pipeline
- RAG indexing of:
  - Historical tickets
  - Company knowledge
- Draft generation as internal note
- Model configuration layer

</div>
<div>

## Out of Scope ❌

- Auto-sending to customers
- Multi-language generation
- Voice/phone channels
- Real-time chat

</div>
</div>

---

# Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          Zammad                                 │
│    Ticket Events ──► Webhook ──► REST API                       │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│               Orchestrator (Python Service)                     │
└───────┬─────────────────┬───────────────────────┬───────────────┘
        │                 │                       │
        ▼                 ▼                       ▼
┌────────────┐   ┌─────────────────────┐   ┌───────────────────────┐
│ Anonymizer │   │    RAG Service      │   │  LLM Gateway          │
│ (Presidio) │   │  Hybrid: Vector+    │──►│  (LiteLLM)            │
└────────────┘   │  BM25 + Reranker    │   │  ┌───────┬─────────┐  │
                 │ (LlamaIndex+Qdrant) │   │  │Local  │ Cloud   │  │
                 └─────────────────────┘   │  │Ollama │ Claude  │  │
                                           │  └───────┴─────────┘  │
                                           └───────────────────────┘
```

---

# Component Overview (1/2)

| #     | Component           | Responsibility                                         | Default Implementation |
| ----- | ------------------- | ------------------------------------------------------ | ---------------------- |
| **A** | Ticket Gateway      | Source/sink of tickets: events, notes, reassignment    | Zammad REST Adapter    |
| **B** | Privacy Service     | Anonymize ↔ deanonymize text; owns placeholder mapping | Microsoft Presidio     |
| **C** | Knowledge Retrieval | Return ranked, cited chunks for a query                | LlamaIndex + Qdrant    |

![bg right:25% 90%](https://img.icons8.com/color/512/module.png)

---

# Component Overview (2/2)

| #     | Component    | Responsibility                                                  | Default Implementation |
| ----- | ------------ | --------------------------------------------------------------- | ---------------------- |
| **D** | LLM Gateway  | Single entry for all AI completions; enforces privacy & budgets | LiteLLM Proxy          |
| **E** | Orchestrator | Drives the workflow end-to-end; exposes observability           | Python Service         |

## Key Design Principle

> **Only 5 major components** — each deployable as its own service.  
> Sub-components (embedder, vector store, reranker) are **internal details**.

---

# Technology Stack

<div class="columns">
<div>

## Core Components

| Concern            | Technology               |
| ------------------ | ------------------------ |
| Zammad Integration | `it-at-m/zammad-ai` fork |
| Anonymization      | Microsoft Presidio       |
| RAG Framework      | LlamaIndex               |
| Vector Database    | Qdrant                   |
| Provider Router    | LiteLLM                  |
| Observability      | Langfuse + OpenTelemetry |

</div>
<div>

## AI Models (Configurable)

| Slot          | Default              |
| ------------- | -------------------- |
| Embeddings    | `bge-m3` (Ollama)    |
| Retrieval LLM | Llama 3.1 8B (local) |
| Answer LLM    | Claude Opus (cloud)  |
| Reranker      | `bge-reranker-v2-m3` |

**All models swappable via config** — no code changes required.

</div>
</div>

---

# Implementation Phases

| Phase               | Focus           | Key Deliverables                                           | Status  |
| ------------------- | --------------- | ---------------------------------------------------------- | ------- |
| **1 — RAG Core**    | Retrieval setup | LlamaIndex + Qdrant, hybrid search, reranker, LiteLLM      | **MVP** |
| **2 — Integration** | Full pipeline   | Zammad integration, Presidio anonymization, internal notes | Later   |
| **3 — Quality**     | Ops & eval      | Query rewriting/HyDE, Ragas eval, Langfuse, curation       | Later   |
| **4 — Advanced**    | Scale & cost    | GraphRAG, multi-tenant routing, cost-aware routing         | Later   |

---

# Risks & Mitigations

| Risk                       | Mitigation                                                             |
| -------------------------- | ---------------------------------------------------------------------- |
| **Anonymization gaps**     | Human review mandatory; Presidio + custom recognizers; periodic audits |
| **Hallucinated citations** | Enforce drafts cite only retrieved chunk IDs; reject unknown citations |
| **Stale knowledge**        | Incremental indexing + scheduled re-curation                           |
| **Privacy leakage**        | Anonymized text only to remote LLMs; `allow_remote: false` option      |

**Safety Guarantee:** The AI agent user has **no permission** to create customer-facing articles in Zammad.

---

# Acceptance Criteria & Next Steps

<div class="columns">
<div>

## MVP Success Criteria

| Criterion        | Target            |
| ---------------- | ----------------- |
| Pipeline trigger | < 10 s            |
| Draft (local)    | < 60 s (p95)      |
| Draft (Claude)   | < 30 s (p95)      |
| Human review     | **100%**          |
| PII recall       | ≥ 95%             |
| RAG improvement  | ≥ 10% vs baseline |

</div>
<div>

## Key Guarantees

✅ Human always in control  
✅ Full privacy protection  
✅ Complete audit trail  

</div>
</div>
