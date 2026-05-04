# MVP1 PRD — automation-first gap table

**Canonical PRD:** [`support_rag_mvp1_prd.md`](support_rag_mvp1_prd.md) (this folder).

**Companion (detailed coverage map):** [`mvp1-prd-to-automated-tests-gap-table.md`](mvp1-prd-to-automated-tests-gap-table.md) — row-level “where tested” and historical status.

**Purpose:** Record MVP1 requirements against a single rule: **everything that can be tested automatically must be tested** (default `pytest`, opt-in integration markers, GitLab scheduled jobs, or documented one-command scripts in CI). Rows below list **mandated automation** to close gaps; only **non-automatable** items may stay manual or ops-only.

**Legend**

| Automation state | Meaning |
|------------------|---------|
| **Done** | Automated in default CI path or documented tagged/scheduled job; no further test work required for MVP1. |
| **Must automate** | Automatable but still mock-only, partial, or skipped — **add or extend tests** (same PR as behavior fixes). |
| **Human / ops** | Not machine-verifiable in-repo (e.g. deployment policy, subjective labeling) — document owner; no pytest fiction. |

---

## Policy

1. **No “Partial” without a ticket:** If a requirement is automatable, **Partial** is a temporary state. Close it with a test or a scripted check; update both this file and [`mvp1-prd-to-automated-tests-gap-table.md`](mvp1-prd-to-automated-tests-gap-table.md) in the same change.
2. **Integration is automation:** Qdrant round-trips, live filter/delete, and gateway+retrieve E2E may live behind `RUN_INTEGRATION=1`, `pytest -m integration`, or GitLab services — they still count as automated if CI runs them on a schedule or protected branch.
3. **Perf SLOs:** NFR-1/NFR-2 must remain in `nfr_retrieve_smoke` (or equivalent); flipping `NFR_ENFORCE=1` is an ops decision, not an excuse to skip the script.

---

## Implementation deviation (fix code or PRD)

| Topic | Issue | Mandated action |
|--------|--------|-----------------|
| **R-9 / §2.6 KB chunking** | _(resolved 2026-04-25)_ Previously `chunk_size` ignored. | **Done** — `support_rag/chunking.py`: `SentenceSplitter.split_text` as `sentence_splitter` for `SentenceWindowNodeParser` (token-bounded segments + windows). Tests: `tests/unit/test_chunking_kb_vs_tickets_r9.py`. `chunker_version.kb` → `kb-v2`. |

---

## Functional requirements (R-1 – R-20)

| ID | Summary | Automation state | Mandated tests / notes |
|----|---------|------------------|-------------------------|
| **R-1** | `POST /rag/retrieve` contract | **Done** | Keep `tests/contract/test_retrieve_http.py` (and slice tests) green. |
| **R-2** | Hybrid, RRF, top_k bounds | **Done** | `tests/unit/test_rrf_k_lists_r2.py` — merge order for two synthetic lists via `_rrf_k_lists` (config/`VectorStoreQuery` still covered by existing tests). |
| **R-3** | Cross-encoder rerank default | **Done** | `tests/contract/test_retrieve_rerank_path.py` — fixed stub `predict` + sigmoid order + `min_score` filter. Optional: real `CrossEncoder` in `slow` unchanged. |
| **R-4** | Query rewrite (≤3), HyDE off by default | **Done** | `tests/contract/test_retrieve_rewrite.py` — httpx `X-Slot` on rewrite + HyDE-only; existing offline mocks + `test_service_gateway_roundtrip` R-16. |
| **R-5** | Filters → Qdrant | **Done** | `RUN_INTEGRATION=1`: `tests/integration/test_qdrant_filters_erasure_live.py` (`test_r5_filters_hit_and_miss_live`). |
| **R-6** | Chunk fields | **Done** | `test_retrieve_chunk_shape.py` etc. |
| **R-7** | `min_score` | **Done** | `tests/unit/test_retrieve_min_score.py`. |
| **R-8** | `POST /rag/index/{ns}` | **Done** | Admin + validation tests. |
| **R-9** | KB vs tickets chunking | **Done** | `tests/unit/test_chunking_kb_vs_tickets_r9.py` (counts, token bound, smaller `chunk_size` → more chunks). |
| **R-10** | Deterministic chunk IDs | **Done** | `test_chunk_id_ingest_idempotent.py`, `test_chunk_id.py`. |
| **R-11** | DELETE by `parent_id` | **Done** | `RUN_INTEGRATION=1`: `tests/integration/test_qdrant_filters_erasure_live.py` (`test_r11_delete_removes_points_live`). |
| **R-12** | Replace-by-`parent_id` ingest | **Done** | `RUN_INTEGRATION=1`: `tests/integration/test_qdrant_filters_erasure_live.py` (`test_r12_reindex_replaces_content_live`). |
| **R-13** | `GET /rag/health` shape | **Done** | `test_health_capabilities.py`. |
| **R-14** | Capabilities match runtime | **Done** | `retrieval.rerank_enabled` + `test_health_capabilities_r14_matrix`; optional: live `describe()` job. |
| **R-15** | Embeddings via gateway + slot | **Done** | `test_service_gateway_roundtrip.py` (async embed from `retrieve` + `X-Slot` + trace) + `test_gateway_slot_headers.py`. |
| **R-16** | Chat completions via `retrieval_llm` | **Done** | `test_service_gateway_roundtrip.py` (rewrite `chat_completion_sync` from `retrieve` + slot + trace) + client slot tests. |
| **R-17** | No provider SDKs | **Done** | `test_no_provider_sdk.py` + CI. |
| **R-18** | Local cross-encoder | **Must automate** | Keep `test_cross_encoder_r18_smoke.py`; **require** CI cache for model or deterministic stub for merge gate; slow job downloads. |
| **R-19** | MCP tools | **Done** | `test_mcp_http_binding.py`, `test_mcp_tools.py`. |
| **R-20** | Admin token on `rag.index` | **Done** | MCP + REST admin tests. |

---

## Non-functional (NFR-1 – NFR-7)

| ID | Summary | Automation state | Mandated tests / notes |
|----|---------|------------------|-------------------------|
| **NFR-1** | p95 retrieve ≤ 2s | **Done** (job) | `scripts/nfr_retrieve_smoke.py` + GitLab; enforce when SLO signed. |
| **NFR-2** | ≥5 concurrent retrieves | **Done** (job) | Same script. |
| **NFR-3** | On-prem; gateway-only egress | **Human / ops** | Network policy checklist; optional future smoke from locked-down VM. |
| **NFR-4** | OTel + trace correlation | **Done** (gateway headers) | `test_gateway_trace_ctx.py` Langfuse + `traceparent` on `post`; service round-trip; OTLP receiver test remains optional. |
| **NFR-5** | `chunker_version`, embedding id on metadata | **Done** | `test_chunk_metadata_nfr5.py`. |
| **NFR-6** | Stateless / restart-safe | **Must automate** | Compose or process-level test: restart API container, repeat retrieve (extend lifecycle test). |
| **NFR-7** | Bearer; admin on index/delete | **Must automate** | Fuzz: every route returns 401 without token (parametrized route list). |

---

## §2.8 Acceptance criteria

| # | Criterion | Automation state | Mandated tests / notes |
|---|-----------|------------------|-------------------------|
| **1** | Contract: hybrid vs dense, stable IDs, capabilities | **Done** (tagged CI) | `hybrid_golden_eval` + chunk/capability tests; optional default-branch gate. |
| **2** | ≥10% hybrid lift | **Human / ops** (labels) + **Done** (script) | `ENFORCE_THRESHOLDS=1` when golden set owned; labeling remains human. |
| **3** | p95 ≤ 2s | **Done** (job) | NFR-1. |
| **4** | Erasure | **Done** | `RUN_INTEGRATION=1`: `tests/integration/test_qdrant_filters_erasure_live.py` (`test_erasure_retrieve_empty_after_delete_live`). |
| **5** | `allow_remote: false` E2E | **Done** | GitLab `e2e_privacy_allow_remote` (preflight + `e2e_privacy`); same tag/rules as `hybrid_golden_eval`; documented YAML in runbook. |
| **6** | No provider SDKs | **Done** | R-17. |
| **7** | MCP from desktop | **Human / ops** | CI cannot prove Claude Desktop; keep smoke + runbook; periodic manual check. |

---

## Deliverables (§2.11) — traceability

| Deliverable | Automated check |
|-------------|-----------------|
| `support_rag/` package | Import smoke + pytest suite. |
| Docker / compose | Optional: `docker compose config` in CI. |
| `config.example.yaml` | Optional: schema or load test. |
| MCP descriptor | `test_mcp_*`. |
| `scripts/reindex.py`, `scripts/seed_kb.py` | **Done** | `argparse` `--help`; MR pipeline `mvp1_script_help_golden` + `tests/unit/test_mvp1_deliverable_cli.py`. |
| `eval/golden/` ≥30 pairs | **Done** | Same job + test (`questions.jsonl` line count). |
| README bring-up | **Human / ops** review; optional link check. |

---

## Change log

- **2026-04-25** — Initial table: automation-first policy, PRD co-located in `implementation-artifacts`, deviation row for KB `chunk_size`, mandated backlog for former “Partial” rows.
- **2026-04-25** — §2.8#5, §2.11 reindex/seed/golden: **Done** per `.gitlab-ci.yml` (`e2e_privacy_allow_remote`, `mvp1_script_help_golden`) and `test_mvp1_deliverable_cli.py`.
- **2026-04-25** — R-9 KB `chunk_size` + deviation row: **Done** (`spec-mvp1-automation-backlog-kb-chunking-r9` implementation).
- **2026-04-25** — R-5, R-11, R-12, §2.8#4: **Done** — `spec-mvp1-automation-backlog-qdrant-filters-erasure` + `tests/integration/test_qdrant_filters_erasure_live.py` (`RUN_INTEGRATION=1`).
- **2026-04-25** — R-2, R-3, R-4: **Done** — `spec-mvp1-automation-backlog-retrieve-rrf-rerank-rewrite` + `test_rrf_k_lists_r2.py`, `test_retrieve_rerank_path.py` (order/min_score), `test_retrieve_rewrite.py` (httpx slot + HyDE).
