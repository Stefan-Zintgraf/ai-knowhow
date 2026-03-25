# Migration Plan: From No‑Code n8n RAG Prototype → Sophisticated (Optionally Self‑Hosted) AI Support Agent

**Audience:** Support / engineering / operations  
**Starting point:** DataCouch “No‑Code RAG Workflow with n8n” tutorial (n8n Cloud + Google Drive + Qdrant Cloud + Gemini)  
**Goal:** Quickly validate whether an AI Support agent can answer new requests from ~1 GB historical support emails + datasheets, then iteratively harden quality, governance, and (optionally) move to a fully self‑hosted stack.


---

## 0) Outcomes and design principles

### Primary outcomes
1. **Feasibility (POC):** In <1–2 days of effort, answer representative support questions with citations to your content.
2. **Quality (MVP):** Reduce wrong answers (hallucinations) with grounded retrieval, “I don’t know” behavior, and sources.
3. **Operational readiness:** Enable human-in-the-loop review, logging, and continuous improvement.
4. **Scale & privacy:** Support 1 GB+ content, handle PII safely, and optionally run fully on-prem / self-host.

### Principles
- **RAG before fine-tuning:** You usually get the biggest gains from better retrieval, chunking, prompts, and evaluation before model training.
- **Always cite sources:** The agent should include “why” (snippets / doc references) with each answer.
- **Fail safely:** Prefer “I don’t know / need more info” over confident guessing.
- **Iterate with evidence:** Every improvement should be justified by evaluation results.

---

## 1) What you are building (high-level architecture)

### Minimal RAG chatbot (starting point)
1. **Ingest** documents (Google Drive or local files)
2. **Split** into chunks (Recursive Character Splitter)
3. **Embed** chunks (embedding model)
4. **Store** embeddings + metadata in a vector DB (Qdrant)
5. **Query**: embed user question → retrieve top‑k chunks
6. **Generate** answer using LLM constrained to retrieved context

### Target “support agent” (final state)
In addition to the above:
- Ticket intake (email/Zendesk/Jira SM/etc.)
- Intent + product/version classification
- Multi-stage retrieval (hybrid + rerank)
- Guardrails and policy checks (PII / compliance)
- Tool use (fetch logs, check compatibility matrices, run diagnostics)
- Human approval loop (draft → review → send)
- Continuous evaluation + monitoring + retraining (optional)

---

## 2) Phase 0 — Preparation (fast, high leverage)

### 2.1 Data inventory (emails + datasheets)
**Inputs:** ~1 GB text files (likely includes PII and repeated threads)

Create a simple inventory table (CSV/Sheet):
- Source: `support_emails`, `datasheets`, `manuals`, `release_notes`, etc.
- Format: `.txt`, `.eml`, `.pdf`, `.md`, `.html`
- Language(s)
- Product / version tags (if available)
- Size
- Sensitivity: PII/Confidential/Public

**Key recommendation:** For a first POC, ingest a *representative subset* (e.g., last 3–6 months OR top 5 product lines).  
1 GB can easily turn into **hundreds of thousands to millions of chunks** depending on splitter settings, which slows indexing and increases cost.

### 2.2 Define your evaluation set (“golden tickets”)
Create a test set of **50–200 real support questions** with expected outcomes:
- 30% common questions (FAQ-ish)
- 30% tricky (requires cross-referencing datasheet + past case)
- 20% ambiguous (should ask clarifying questions)
- 20% out-of-scope (should say “not in knowledge base”)

For each question, store:
- `question`
- `expected_answer` (or expected key points)
- `expected_sources` (optional)
- `severity` (high/medium/low)
- `product`, `version`

> This becomes your regression test suite for every migration step.

### 2.3 Security / compliance baseline
- Decide whether you can send content to external LLM APIs.
- If not, plan to move earlier to **self-hosted embeddings + LLM** (see Phase 5+).
- Add a **PII stripping step** (at minimum: emails, phone numbers, addresses, serial numbers if sensitive).

---

## 3) Phase 1 — Implement the DataCouch starting point (No‑code POC)

This phase mirrors the DataCouch flow:
- n8n Cloud account
- Google Drive connector
- Qdrant Cloud collection
- Default Data Loader + Recursive splitter
- Embeddings + Q&A chain with Gemini (or another LLM)

### 3.1 Implement the tutorial as-is (single document)
Follow the steps from the DataCouch post:
- Create n8n Cloud account
- Manually triggered workflow
- Connect Google Drive (OAuth client + redirect URI)
- Set up Qdrant Cloud and create a collection (example uses cosine distance and 1536 vector size)
- Add Qdrant Vector Store node (Insert Documents)
- Add embedding model and Default Data Loader + Recursive Character Splitter
- Add Q&A Chain and connect:
  - Generator (Gemini via Google AI Studio)
  - Retriever (Qdrant; example retrieval limit = 4)

**Acceptance criteria (POC baseline):**
- You can ask 10 representative questions and get answers with relevant citations/snippets.

### 3.2 Adapt the ingestion for ~1 GB email + datasheet text
The tutorial focuses on a PDF in Google Drive. For your dataset:

**Option A (still no-code, still in n8n Cloud):**  
Put text files into Google Drive folders (organized by product/version), then read them via Drive nodes.

**Option B (recommended for 1 GB):**  
Self-host n8n early (Phase 5) and read files from disk / mounted storage. n8n templates (e.g., “Basic RAG chat”) can read files from disk.

### 3.3 Practical preprocessing for support emails (high impact)
Before embedding, normalize emails:
- Remove signatures, disclaimers, “external email” banners
- Collapse repeated quoted threads (keep the *final resolution* if possible)
- Extract key fields:
  - subject, product, version, error codes, platform, firmware, etc.
- Deduplicate near-identical replies/macros

**No-code heuristic:** Use n8n text nodes / regex + “code node” only if necessary.

### 3.4 Chunking guidance (first pass)
Use Recursive Character Splitter with:
- **Chunk size:** 800–1500 characters (start here)
- **Overlap:** 100–200 characters  
Tune based on evaluation.

For datasheets and manuals, prefer splitting on headings/sections if possible (Markdown/HTML-aware splitting).

### 3.5 Metadata (very important for support)
Attach metadata per chunk (store with each vector):
- `source_type`: email | datasheet | manual | release_note
- `product`
- `version`
- `date`
- `language`
- `doc_id` / `file_path`
- `permissions` / `team` (if relevant)

This enables filtering (“only retrieve for product X vY”).

---

## 4) Phase 2 — Make it a “Support Answer Drafting” MVP (still mostly no-code)

### 4.1 UX: Draft answers + cite sources
Change the response format to:
- **Short answer** (2–5 sentences)
- **Step-by-step resolution**
- **Sources** (top 3 snippets with doc references)
- **Confidence + next questions**

Example response schema (structured):
```json
{
  "answer": "…",
  "steps": ["…", "…"],
  "clarifying_questions": ["…"],
  "sources": [
    {"title":"…", "snippet":"…", "doc_id":"…", "section":"…"}
  ],
  "confidence": "low|medium|high"
}
```

### 4.2 Add a guardrail prompt (strongly recommended)
System message ideas:
- “Use ONLY retrieved context; if missing, say you don’t know.”
- “Cite sources for every claim.”
- “If question is ambiguous, ask 1–3 clarifying questions.”
- “Never output secrets or personal data.”

### 4.3 Add product/version routing
Route questions into separate retrievers:
- A separate Qdrant collection per product/version **or**
- One collection with metadata filters

Start simple:
- `collection = support_v1`
- Filter by `product` if you can infer it from subject/body.

### 4.4 Human-in-the-loop
For real support operation:
- Agent generates a draft
- Human approves/edits
- Approved answers are stored as:
  - labeled training data (optional for fine-tuning later)
  - feedback for retrieval improvements

n8n can implement approval steps (manual review nodes / Slack/Teams approvals).

---

## 5) Phase 3 — Add evaluation and quality gates (turn “chatbot” into an engineering system)

### 5.1 Build an evaluation workflow in n8n
Automate testing your “golden tickets” set:
- Input: CSV/Google Sheet of test questions
- For each question:
  - run retrieval + generation
  - store output, retrieved sources, latency, token usage
- Output:
  - report table (CSV)
  - pass/fail summary
  - diff vs last run

### 5.2 Use multi-metric scoring
Minimum:
- **Groundedness:** does answer cite retrieved text?
- **Correctness (human):** quick review of top failures
- **Coverage:** % questions with at least one relevant snippet retrieved
- **Refusal quality:** out-of-scope questions trigger safe response

Optional automated metrics:
- LLM-as-judge for helpfulness + groundedness (with strong constraints)
- Similarity to expected key points

### 5.3 Quality gates (release criteria)
Before enabling “draft for support agents”:
- ≥ 80% correct on common questions
- ≥ 95% groundedness (citations present and relevant)
- ≤ 5% “confident wrong” answers (high severity)

---

## 6) Phase 4 — Retrieval upgrades (largest quality gains after baseline)

This phase is where you improve *answers* without changing the base LLM.

### 6.1 Hybrid retrieval (vector + keyword)
Support tickets often depend on:
- error codes
- part numbers
- protocol names
- firmware version strings

Vector search alone may miss these. Add:
- keyword/BM25 search
- combined scoring / re-ranking

Approaches:
- Use a search engine (OpenSearch/Elasticsearch) alongside Qdrant
- Or use a vector DB / search service that supports hybrid + rerank

### 6.2 Add reranking
Pipeline:
1. Retrieve top‑k=20 by vector similarity
2. Rerank to top‑k=4 with:
   - cross-encoder reranker (open-source) OR
   - LLM reranker (careful with cost)

### 6.3 Query rewriting
Rewrite user questions before retrieval:
- Normalize product names
- Expand abbreviations
- Extract error codes into a structured query
- Translate language if needed

### 6.4 Better chunking strategies
For emails:
- Prefer “resolution summary” extraction (use LLM summarization)
- Store both:
  - original chunk
  - extracted “resolution” chunk

For datasheets:
- Split by sections + tables (if PDFs, consider conversion to Markdown first)

### 6.5 Add “citations you can click”
Store `file_path` or `drive_url` + `section` or `line-range` in metadata so agents can verify quickly.

---

## 7) Phase 5 — Migration to self-host (privacy + scale + cost control)

This phase preserves the workflow logic but changes deployment.

### 7.1 Self-host n8n (recommended baseline)
Reasons:
- Read large local datasets directly
- Keep credentials and logs in your environment
- Easier to integrate with internal systems

Typical deployment: Docker Compose + Postgres.

### 7.2 Self-host Qdrant
Start with Qdrant Cloud in POC; migrate to self-host for:
- data residency
- lower recurring cost
- performance tuning

### 7.3 Optional: self-host embeddings and LLM
If external APIs are a concern:
- Embeddings: use open models (e.g., BGE/E5 family)
- LLM: run local via Ollama or vLLM

> n8n explicitly supports agentic workflows and can integrate local models (via Ollama node or HTTP).

### 7.4 Reference Docker Compose (starter)
**Note:** Adjust CPU/GPU and storage paths for your environment.
```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n
      POSTGRES_DB: n8n
    volumes:
      - ./data/postgres:/var/lib/postgresql/data

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - N8N_ENCRYPTION_KEY=CHANGE_ME
    volumes:
      - ./data/n8n:/home/node/.n8n
      - ./data/knowledge:/data/knowledge
    depends_on:
      - postgres

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - ./data/qdrant:/qdrant/storage

  # Optional local LLM runtime
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./data/ollama:/root/.ollama
```

### 7.5 Data migration plan (Cloud → self-host)
- Export embeddings/chunks from Qdrant Cloud (via snapshots) if available
- Or re-index from source (often simpler and safer)
- Validate with golden ticket evaluation after migration

---

## 8) Phase 6 — Turn “chatbot” into an autonomous Support Agent (agentic workflows)

### 8.1 Core agent capabilities
- Understand request, ask clarifying questions
- Retrieve evidence (RAG)
- Propose troubleshooting steps
- Draft a reply in your support tone
- Create internal notes (what was tried, next steps)
- Escalate to humans when uncertainty is high

### 8.2 Tool use
Add tools the agent can call:
- Ticket system (create/update, add internal note)
- CRM lookup
- Product compatibility matrix (DB/API)
- Knowledge base update (create draft article)

### 8.3 Human-in-the-loop as a first-class step
For production:
- Always draft; never auto-send at first
- Add “approve” / “reject” / “edit” controls
- Capture feedback tags: wrong retrieval, missing doc, wrong reasoning, etc.

### 8.4 Policy enforcement
Before generating final draft:
- PII scrub (do not repeat customer secrets)
- Security policy check (do not leak internals)
- “Do not invent steps that aren’t in sources”

---

## 9) Phase 7 — Fine-tuning strategy (optional, only after RAG is strong)

### 9.1 What fine-tuning is good for
- Consistent tone and formatting
- Better question-clarification behavior
- Better extraction of structured fields (product/version/error codes)
- Domain jargon fluency

### 9.2 What fine-tuning is *not* good for
- “Learning” your 1 GB knowledge base.  
That’s what RAG is for. Fine-tuning won’t reliably store all facts and will quickly go stale.

### 9.3 Recommended fine-tuning order
1. **Prompt + retrieval optimization** (Phases 2–6)
2. **Reranker tuning / better embeddings**
3. **Supervised fine-tuning (SFT)** on:
   - (question, retrieved context) → ideal answer
   - real approved support replies
4. **Preference optimization (optional):**
   - compare two drafts; pick best (DPO-style)

### 9.4 Data set creation for SFT (safe + high quality)
- Source: approved support responses + internal notes
- Remove PII
- Store structured labels (product/version, severity, etc.)
- Keep a held-out test set (never train on it)

### 9.5 When to fine-tune
Only after:
- retrieval recall is high (agent finds the right info)
- evaluation shows the model’s language/tone is the limiting factor

---

## 10) Phase 8 — “Most sophisticated” end state (optionally fully on-prem)

### 10.1 Target architecture options

**Option A (n8n remains orchestrator):**
- n8n self-hosted
- Qdrant self-hosted
- OpenSearch/Elasticsearch for keyword/hybrid
- Local embeddings model server
- Local LLM via vLLM (GPU) or Ollama (simpler)
- Observability: Prometheus/Grafana + centralized logs

**Option B (n8n for automation, custom RAG service for core):**
- n8n triggers and tool integrations
- RAG service (LangChain/LlamaIndex/Haystack) provides:
  - advanced retrieval
  - caching
  - evaluation harness
  - A/B testing
- Same self-host vector DB / model servers

### 10.2 Advanced features (choose by ROI)
- Multi-hop retrieval (follow-up searches based on first evidence)
- GraphRAG / knowledge graphs for entity-heavy domains
- “Case-based reasoning”: detect similar past tickets and reuse resolution
- Auto-KB drafting: turn solved tickets into articles (human reviewed)
- Multi-lingual support (translate query + sources)

### 10.3 Governance
- Access control by team/product (metadata + auth)
- Audit trail: who asked what, what sources used, what was sent
- Retention policies for logs and embeddings
- Regular red-teaming for hallucinations and prompt injection

---

## 11) Migration roadmap (summary table)

| Phase | What changes | What stays the same | Why it’s worth it | “Done when…” |
|---|---|---|---|---|
| 1 | n8n Cloud + Drive + Qdrant Cloud + LLM API | RAG concept | fastest feasibility | 10–20 questions answered with citations |
| 2 | Support-specific formatting + metadata routing | same stack | answers become usable as drafts | agents can verify sources quickly |
| 3 | Evaluation workflow + gates | same stack | prevents regressions | repeatable report & thresholds met |
| 4 | Hybrid + rerank + better chunking | same LLM | big quality gains | fewer wrong answers, better recall |
| 5 | Self-host n8n + Qdrant | same logic | privacy, scale, cost | self-hosted + eval parity |
| 6 | Agentic tools + approvals | retrieval remains | workflow automation value | drafts integrated into ticket system |
| 7 | Fine-tuning | RAG still core | tone/behavior improvements | measurable gains on test set |
| 8 | Full on-prem “best-in-class” | design principles | maximum control | SLOs met, audited & governed |

---

## 12) Agent-friendly task list (semi-automatable)

Below is a task list designed so an “AI implementation agent” can execute it step-by-step.

### 12.1 Variables (fill these first)
```yaml
project:
  name: "support-rag-agent"
  primary_language: "en"
  products: ["<productA>", "<productB>"]
data:
  source_root: "/data/knowledge"
  drive_folder_ids: ["<optional>"]
security:
  allow_external_llm_api: false  # set true if allowed
  pii_redaction: true
models:
  embedding_model: "<openai|gemini|local-bge|local-e5>"
  llm_model: "<gemini|gpt|local-llama|mistral>"
vector_db:
  type: "qdrant"
  collection: "support_v1"
retrieval:
  top_k: 4
  chunk_size_chars: 1200
  chunk_overlap_chars: 150
evaluation:
  golden_set_path: "/data/knowledge/eval/golden_tickets.csv"
  pass_threshold_correct: 0.80
  pass_threshold_grounded: 0.95
```

### 12.2 Phase-by-phase automation tasks
#### Phase 1 tasks (POC)
- [ ] Create n8n workflow: ingest subset of files into Qdrant
- [ ] Create n8n workflow: chat/Q&A chain using retriever + generator
- [ ] Run 10–20 test questions manually; record results

#### Phase 2 tasks (MVP)
- [ ] Add metadata fields to chunks (product/version/date/source_type)
- [ ] Add system message guardrails + JSON output schema
- [ ] Add routing/filtering by product/version (if possible)

#### Phase 3 tasks (Evaluation)
- [ ] Import golden tickets CSV
- [ ] Batch-run evaluation workflow
- [ ] Export report (CSV) and compute pass/fail metrics

#### Phase 4 tasks (Retrieval upgrades)
- [ ] Increase top‑k retrieval, add rerank stage (top‑20 → top‑4)
- [ ] Add keyword/hybrid retrieval for error codes and part numbers
- [ ] Re-run evaluation; compare to baseline

#### Phase 5 tasks (Self-host)
- [ ] Deploy docker-compose (n8n + Postgres + Qdrant)
- [ ] Re-index from source; validate parity with golden tickets
- [ ] Implement secrets management (env vars, vault, etc.)

#### Phase 6 tasks (Agentic support)
- [ ] Integrate ticket system API (create draft reply, add internal note)
- [ ] Add human approval workflow
- [ ] Add logging + monitoring dashboards

#### Phase 7 tasks (Fine-tune, optional)
- [ ] Build training set from approved answers (PII removed)
- [ ] Train LoRA/SFT for formatting + clarifying behavior
- [ ] Evaluate vs held-out set; roll out behind feature flag

---

## 13) Practical “what to do first” checklist (your next 2 hours)

1. Pick **one product** + **one language** + **last 3 months** of emails + latest datasheets.
2. Build the **exact** DataCouch POC in n8n with Qdrant + Q&A chain.
3. Add **metadata** and force **citations** in every answer.
4. Create **50 golden tickets** and run them as a batch.
5. Decide: external APIs allowed?  
   - yes → keep cloud models for now  
   - no → move to Phase 5 (self-host) sooner

---

## References (starting point + key docs)
- DataCouch tutorial: https://datacouch.io/blog/how-to-build-a-no-code-rag-chatbot-with-n8n-to-chat-with-your-data/
- n8n RAG docs: https://docs.n8n.io/advanced-ai/rag-in-n8n/
- n8n AI Agent node: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
- n8n RAG chatbot blog guide: https://blog.n8n.io/rag-chatbot/
- n8n “Basic RAG chat” template: https://n8n.io/workflows/5028-basic-rag-chat/
