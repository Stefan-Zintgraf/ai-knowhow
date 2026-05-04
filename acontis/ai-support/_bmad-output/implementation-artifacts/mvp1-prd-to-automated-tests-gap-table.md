# MVP1 PRD → automated test coverage (gap table)

**Purpose:** Map [`support_rag_mvp1_prd.md`](support_rag_mvp1_prd.md) requirements to what is (or is planned to be) checked **automatically** in CI or scripted jobs—so gaps are explicit. “Manual” or “ops-only” is called out. **Automation backlog / policy:** [`mvp1-prd-automation-first-gap-table.md`](mvp1-prd-automation-first-gap-table.md).

**BMad quick dev:** This file is listed in `_bmad/custom/bmad-quick-dev.toml` as a `persistent_fact`, so it is **loaded on every** `bmad-quick-dev` run (with `project-context.md` if present). When a row moves from gap to covered, update the table in the same commit as the tests.

**Legend**

| Status | Meaning |
|--------|---------|
| **Covered** | Automated test and/or job exists; running it is the agent/CI default or documented one-liner. |
| **Partial** | Some behavior asserted (mock, unit, or slice); not full PRD surface. |
| **Planned** | Named in a `spec-*.md` that is not fully executed, or in `deferred-work.md`. |
| **Missing** | No committed plan in implementation artifacts; add a spec or extend an existing one. |

**Key artifacts**

- Done: `spec-mvp1-prd-verification-hardening.md`, `spec-golden-set-hybrid-vs-dense-eval.md` (incl. `eval/eval_hybrid_vs_dense.py`), `spec-mvp1-admin-filters-and-erasure-tests.md` (qfilter, admin index/delete, erasure unit).
- Done (OTel + MCP smoke): `spec-mvp1-otel-and-mcp-smoke.md`.
- Done (Gateway `X-Slot` R-15/R-16): `spec-mvp1-gateway-slot-headers.md` (`test_gateway_slot_headers.py`).
- Done (retrieve vertical slice R-1..R-7): `spec-mvp1-retrieve-vertical-slice.md` (`test_retrieve_*.py`, `test_retrieve_min_score.py`).
- Done (MCP REST parity R-19, R-20): `spec-mvp1-mcp-rest-parity.md` (`tests/contract/test_mcp_http_binding.py`).
- Backlog: `deferred-work.md`.
- **Planned (ready-for-dev / draft specs for bmad-quick-dev):** run in the order below; each spec lists tasks, ACs, and files to add or change.
  1. ~~`spec-mvp1-gateway-slot-headers.md` — R-15, R-16.~~ **Done** (see `tests/unit/test_gateway_slot_headers.py`).
  2. ~~`spec-mvp1-ci-eval-nfr-perf-gating.md` — §2.8(1)(2)(3), NFR-1, NFR-2.~~ **Done** (GitLab [`.gitlab-ci.yml`](../../.gitlab-ci.yml) tag `rag-mvp1-eval`, [README — MVP1 eval + perf CI](../../README.md#mvp1-eval--perf-ci-gitlab)).
  3. ~~`spec-mvp1-mcp-rest-parity.md` — R-19, R-20.~~ **Done** — `tests/contract/test_mcp_http_binding.py` (+ `tests/test_mcp_tools.py` name smoke).
  4. ~~`spec-mvp1-allow-remote-false-acceptance.md` + `spec-mvp1-automation-backlog-ci-e2e-deliverables-deferred.md` — §2.8(5), preflight, `e2e_privacy`, runbook, GitLab.~~ **Done** — `e2e_privacy_allow_remote`, `mvp1_script_help_golden` ([`.gitlab-ci.yml`](../../.gitlab-ci.yml)).
  5. ~~`spec-mvp1-prd-residual-gaps.md` — R-8, R-9, R-11, R-12, R-14, R-18, NFR-4, NFR-5, NFR-6, §2.8#4 opt.~~ **Done** (residual tests + README; Langfuse+gateway: extended in `spec-mvp1-automation-backlog-health-langfuse-gateway-roundtrip.md`).
  6. ~~`spec-mvp1-automation-backlog-qdrant-filters-erasure.md` — R-5, R-11, R-12, §2.8#4 live Qdrant.~~ **Done** — `tests/integration/test_qdrant_filters_erasure_live.py` (`RUN_INTEGRATION=1`).

**Tests today (illustrative, not exhaustive):** `tests/contract/test_auth_health.py`, `test_retrieve_*.py`, `test_service_gateway_roundtrip.py`, `test_admin_index_delete.py`, `test_index_request_validation.py`, `test_mcp_http_binding.py`, `test_health_capabilities.py`, `test_chunk_id_ingest_idempotent.py`, `test_retrieval_hybrid_flag.py`, `test_otel_routes.py`, `test_no_provider_sdk.py`, `test_chunk_id.py`, `tests/unit/test_qfilter.py`, `tests/unit/test_retrieve_min_score.py`, `tests/unit/test_service_delete_erasure.py`, `tests/unit/test_gateway_slot_headers.py`, `tests/unit/test_chunk_metadata_nfr5.py`, `tests/unit/test_index_replace_by_parent_id_r12.py`, `tests/unit/test_chunking_kb_vs_tickets_r9.py`, `tests/unit/test_cross_encoder_r18_smoke.py`, `tests/unit/test_service_lifecycle_nfr6.py`, `tests/integration/test_qdrant_optional_r11_r14.py`, `tests/integration/test_qdrant_filters_erasure_live.py`, `tests/test_gateway_trace_ctx.py`, `tests/test_mcp_tools.py`, `tests/conftest.py`.

---

## Functional (R-1 – R-20)

| ID | Requirement (summary) | Status | Where / how | Gap / next test idea |
|----|------------------------|--------|-------------|------------------------|
| **R-1** | `POST /rag/retrieve` wire contract | **Covered (offline)** | `tests/contract/test_retrieve_http.py` (401/200, JSON shape) | Deeper: live HTTP vs ASGI is same stack; optional integration. |
| **R-2** | Hybrid, RRF, top_k bounds | **Covered (offline)** | `test_retrieval_hybrid_flag.py` + `test_retrieve_vector_query_params.py` + `tests/unit/test_rrf_k_lists_r2.py` (`_rrf_k_lists` merge order) | Optional: live hybrid Qdrant. |
| **R-3** | Reranker on by default, order vs fusion | **Covered (offline)** | `test_retrieve_rerank_path.py` — `predict` stub with sigmoid order + `min_score` | Optional: real `CrossEncoder` in `slow` / integration. |
| **R-4** | Query rewrite (n≤3), HyDE optional | **Covered (offline)** | `test_retrieve_rewrite.py` (mocks + httpx `X-Slot` for rewrite and HyDE-only) + R-16 roundtrip | Optional: HyDE+rewrite combination depth. |
| **R-5** | Metadata filters → Qdrant | **Covered (integration)** | Unit/slice: `test_qfilter.py`, `test_retrieve_filters_aquery.py`. Live: `tests/integration/test_qdrant_filters_erasure_live.py` (`RUN_INTEGRATION=1`). | — |
| **R-6** | Chunk fields (`id`, `parent_id`, `score`, metadata…) | **Covered (offline)** | `test_retrieve_chunk_shape.py` | — |
| **R-7** | `min_score` truncates; empty valid | **Covered (offline)** | `tests/unit/test_retrieve_min_score.py` (rerank path) | — |
| **R-8** | `POST /rag/index/{namespace}` document list | **Covered (offline)** | `test_admin_index_delete.py` + `test_index_request_validation.py` (422 on bad bodies) | Deeper: live index against Qdrant. |
| **R-9** | KB vs tickets chunking strategies | **Covered (offline)** | `tests/unit/test_chunking_kb_vs_tickets_r9.py` — kb vs tickets counts; **token** max per `chunk_size` (`SentenceSplitter` + `SentenceWindowNodeParser`); smaller `chunk_size` → more chunks | Optional: larger FR-13 goldens. |
| **R-10** | Deterministic chunk IDs | **Covered** | `test_chunk_id_ingest_idempotent.py` (+ `test_chunk_id.py`) | — |
| **R-11** | `DELETE` by `parent_id` removes chunks | **Covered (integration)** | Offline: `test_admin_index_delete.py`, `test_service_delete_erasure.py`. Live Qdrant count: `tests/integration/test_qdrant_filters_erasure_live.py` (`RUN_INTEGRATION=1`). | — |
| **R-12** | Incremental/dedup ingest behavior | **Covered (integration)** | Unit: `tests/unit/test_index_replace_by_parent_id_r12.py`. Live replace: `tests/integration/test_qdrant_filters_erasure_live.py` (`RUN_INTEGRATION=1`). | — |
| **R-13** | `GET /rag/health` JSON shape | **Covered** | `test_health_capabilities.py` (+ auth route) | — |
| **R-14** | Capabilities match runtime | **Covered (offline matrix)** | `test_health_capabilities.py` parametrize `hybrid` + `retrieval.rerank_enabled` vs `health()`; `RetrievalConfig.rerank_enabled` in `config.py` | Optional: live gateway `describe()` non-empty (`RUN_INTEGRATION=1`). |
| **R-15** | Embeddings via gateway + `X-Slot: embedding` | **Covered (retrieve path)** | `tests/unit/test_gateway_slot_headers.py` (client) + `tests/contract/test_service_gateway_roundtrip.py` (`test_retrieve_async_embed_uses_x_slot_and_trace_r15`) | — |
| **R-16** | Chat (rewrite) via `retrieval_llm` slot | **Covered (retrieve path)** | `test_service_gateway_roundtrip.py` (`test_retrieve_rewrite_chat_uses_retrieval_slot_and_trace_r16`) + slot unit tests | Deeper: HyDE+rewrite combo is optional. |
| **R-17** | No provider SDKs | **Covered** | `test_no_provider_sdk.py` | — |
| **R-18** | Local cross-encoder reranker | **Covered (default MR / offline gate)** | `tests/unit/test_cross_encoder_r18_smoke.py` — `test_reranker_model_id_frozen_on_service` in GitLab `mvp1_script_help_golden`; `slow` Hub load is optional | Full CrossEncoder in retrieve path still mocked elsewhere; `slow` smoke not a merge gate. |
| **R-19** | MCP: `rag.retrieve`, `rag.index`, `rag.health` | **Covered (offline)** | `tests/test_mcp_tools.py` (names); `tests/contract/test_mcp_http_binding.py` (path + service bearer for health/retrieve) | Optional: stdio E2E. |
| **R-20** | `rag.index` admin token vs service on retrieve | **Covered (offline)** | `test_mcp_http_binding.py` (admin bearer on index; `RuntimeError` if admin token unset) | REST still `test_admin_index_delete.py` / `test_auth_health`. |

---

## Non-functional (NFR-1 – NFR-7) & observability

| ID | Requirement (summary) | Status | Where / how | Gap / next test idea |
|----|------------------------|--------|-------------|------------------------|
| **NFR-1** | p95 `retrieve` ≤ 2.0s | **Covered (scheduled / tagged runner)** | [`.gitlab-ci.yml`](../../.gitlab-ci.yml) job `nfr_retrieve_smoke` + [scripts/nfr_retrieve_smoke.py](../../scripts/nfr_retrieve_smoke.py); `NFR_ENFORCE` for blocking vs report-only | Budget is corpus-specific; default job is `allow_failure: true` until SLOs are stable. |
| **NFR-2** | ≥5 concurrent retrieves | **Covered (scheduled / tagged runner)** | Same `nfr_retrieve_smoke` (5 parallel `retrieve` calls) | Tune workers in compose; script reports `concurrent_errors`. |
| **NFR-3** | On-prem; only gateway outbound | **Not automatable in unit** | Policy/deployment | Checklist or smoke from locked-down network profile (out of default pytest). |
| **NFR-4** | OTel spans; gateway correlated | **Partial** | `test_otel_routes.py` (spans); `test_gateway_trace_ctx.py` (`_slot_headers`, `embed_sync` + `chat_completion_sync` with Langfuse + `traceparent` on `MockTransport`); `test_service_gateway_roundtrip` (service retrieve) | Real OTLP/collector: optional profile. |
| **NFR-5** | `chunker_version` + embedding id on metadata | **Covered (offline)** | `tests/unit/test_chunk_metadata_nfr5.py` (chunker + `embedding_model` on index path) | Live pipeline stamp: optional. |
| **NFR-6** | Stateless, restart safe | **Covered (unit) + automatable (process)** | Unit: `tests/unit/test_service_lifecycle_nfr6.py`. Compose/process: `tests/integration/test_nfr6_compose_restart.py` with `RUN_INTEGRATION=1` and `RUN_NFR6_COMPOSE=1` (restarts `support-rag`). | On-demand/self-hosted; not default shared-runner MR. |
| **NFR-7** | Bearer on endpoints; admin for index/delete | **Covered (offline contract)** | `tests/contract/test_protected_routes_401.py` (parametrized 401 + OpenAPI coverage guard); success paths in `test_auth_health`, `test_retrieve_http`, `test_admin_index_delete` | Add `PUBLIC_ROUTES` if a future `/rag` route is anonymous. |

---

## §2.8 Acceptance criteria (MVP1)

| # | Criterion | Status | Where / how | Gap / next test idea |
|---|-----------|--------|-------------|------------------------|
| **1** | Contract tests: hybrid beats dense on golden; chunk IDs; capabilities | **Covered (scheduled / tagged runner)** | `eval_hybrid_vs_dense` + `hybrid_golden_eval` in [`.gitlab-ci.yml`](../../.gitlab-ci.yml); not default MR **merge** gate (see [README](../../README.md#mvp1-eval--perf-ci-gitlab)) | Optional `ENFORCE_THRESHOLDS=1` on the GitLab job. |
| **2** | ≥10% quality lift | **Partial (automated + human)** | Same script; `ENFORCE_THRESHOLDS=1` enforces the margin for the **smoke** set | Human labeling of gold docs remains. |
| **3** | p95 ≤ 2.0s | **Covered (scheduled / tagged runner)** | NFR-1 row + `nfr_retrieve_smoke` | **Report-only** until `NFR_ENFORCE=1` and SLO sign-off. |
| **4** | Erasure: delete then retrieve empty | **Covered (integration)** | Unit: `tests/unit/test_service_delete_erasure.py`. Live: `tests/integration/test_qdrant_filters_erasure_live.py` (`RUN_INTEGRATION=1`). | — |
| **5** | `allow_remote: false` E2E | **Covered (scheduled / tagged runner)** | `e2e_privacy_allow_remote` in [`.gitlab-ci.yml`](../../.gitlab-ci.yml) + in-repo: `scripts/e2e_gateway_preflight.py`, `RUN_E2E_PRIVACY=1 pytest -m e2e_privacy`, runbook | Same **rules** as `hybrid_golden_eval` (not default MR). Stack must be on self-hosted `rag-mvp1-eval` host. |
| **6** | No provider SDKs | **Covered** | `test_no_provider_sdk.py` | — |
| **7** | MCP callable from desktop | **Not CI-equivalent** | Tool smoke = proxy | **Manual** or E2E outside pytest; keep smoke in CI. |

---

## Suggested next steps (ordered)

Implementation artifacts (see **Key artifacts** above) map 1:1 to these steps. Execute **in order** for quick-dev unless dependencies allow parallel work (e.g. gateway slot tests are independent of retrieve slice).

1. **Done** — `spec-mvp1-retrieve-vertical-slice.md` (R-1..R-7 offline contract slice).

2. ~~**Gateway slot headers (R-15 / R-16)** — One module test on `LLMGatewayClient` with `httpx` mock to assert `X-Slot`~~ **Done** — `spec-mvp1-gateway-slot-headers.md` / `tests/unit/test_gateway_slot_headers.py`.

3. ~~**Eval / perf gating** — **Wired:** [`.gitlab-ci.yml`](../../.gitlab-ci.yml) + [README](../../README.md#mvp1-eval--perf-ci-gitlab). **→** `spec-mvp1-ci-eval-nfr-perf-gating.md` (done)~~

4. ~~**MCP (R-19 / R-20) depth** — **→** `spec-mvp1-mcp-rest-parity.md`~~ **Done** (`test_mcp_http_binding.py`).

5. ~~**§2.8(5) privacy path** — preflight, `e2e_privacy`, runbook, **`e2e_privacy_allow_remote`** (GitLab).~~ **Done** (see `spec-mvp1-allow-remote-false-acceptance.md`, `spec-mvp1-automation-backlog-ci-e2e-deliverables-deferred.md`).

6. **Re-run this table** after each spec lands—status column should be updated so “full PRD automation” is either achieved or honestly scoped (e.g. “manual eval labeling remains human”).

7. **Residual PRD rows** (optional batch after 1–6): R-8, R-9, R-12, R-18, NFR-5, NFR-6, etc. **→** `spec-mvp1-prd-residual-gaps.md`

---

## Spec change log

- 2026-04-25 — R-15, R-16: updated after `spec-mvp1-gateway-slot-headers` (`test_gateway_slot_headers.py`).
- 2026-04-25 — R-1..R-7: updated after `spec-mvp1-retrieve-vertical-slice` implementation (`test_retrieve_*`, `test_retrieve_min_score`).
- 2026-04-25 — Initial gap table and next steps.
- 2026-04-25 — Documented wiring into `bmad-quick-dev` via `_bmad/custom/bmad-quick-dev.toml`.
- 2026-04-25 — NFR-4 / R-19: updated after `spec-mvp1-otel-and-mcp-smoke` implementation (OTel + gateway + MCP name tests).
- 2026-04-25 — R-5, R-8, R-11, R-20, NFR-7, §2.8#4: updated after `spec-mvp1-admin-filters-and-erasure-tests` (qfilter, admin, erasure unit).
- 2026-04-25 — Added seven implementation specs for remaining gap table coverage: retrieve vertical slice, gateway slots, CI eval/NFR (draft), MCP REST parity, `allow_remote` E2E (draft), and residual gaps; cross-linked in **Key artifacts** and **Suggested next steps**.
- 2026-04-25 — §2.8#5: **Partial** after `spec-mvp1-allow-remote-false-acceptance` implementation (preflight, `e2e_privacy`, smoke scripts, runbook).
- 2026-04-25 — §2.8#5: **Covered (scheduled / tagged runner)** after `e2e_privacy_allow_remote` in `.gitlab-ci.yml` + `spec-mvp1-automation-backlog-ci-e2e-deliverables-deferred` (MR gate: `mvp1_script_help_golden` for §2.11 scripts + golden line count).
- 2026-04-25 — §2.8(1)(2)(3), NFR-1, NFR-2: updated after `spec-mvp1-ci-eval-nfr-perf-gating` (GitLab `hybrid_golden_eval` + `nfr_retrieve_smoke`, [README](../../README.md#mvp1-eval--perf-ci-gitlab)).
- 2026-04-25 — R-19, R-20: **Covered (offline)** after `spec-mvp1-mcp-rest-parity` (`test_mcp_http_binding.py`, README).
- 2026-04-25 — R-8, R-9, R-11, R-12, R-14, R-18, NFR-5, NFR-6: updated after `spec-mvp1-prd-residual-gaps` (new unit/contract/integration tests, README).
- 2026-04-25 — NFR-6, NFR-7, R-18: updated after `spec-mvp1-automation-backlog-nfr6-nfr7-r18-ci-gate` (`test_nfr6_compose_restart.py`, `test_protected_routes_401.py`, GitLab R-18 `not slow` gate, README).
- 2026-04-25 — R-9 (KB `chunk_size` / strategies): **Covered** after `spec-mvp1-automation-backlog-kb-chunking-r9` — `tests/unit/test_chunking_kb_vs_tickets_r9.py`, `chunker_version.kb` → `kb-v2`.
- 2026-04-25 — R-5, R-11, R-12, §2.8#4: **Covered (integration)** after `spec-mvp1-automation-backlog-qdrant-filters-erasure` — `tests/integration/test_qdrant_filters_erasure_live.py` (`RUN_INTEGRATION=1`).
- 2026-04-25 — R-2, R-3, R-4: **Covered (offline)** after `spec-mvp1-automation-backlog-retrieve-rrf-rerank-rewrite` — `test_rrf_k_lists_r2.py`, extended `test_retrieve_rerank_path.py`, `test_retrieve_rewrite.py` (httpx).
