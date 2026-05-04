---
title: 'MVP1 automation backlog — R-14 capabilities, R-15/R-16 retrieve round-trip, NFR-4 Langfuse'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '197c92b93cea139d4ed99dfd15762165d8de6e01'
context:
  - '_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** R-14, R-15, R-16, and NFR-4 are **Must automate** in the gap table. Health is only tested for one config; `X-Slot` is covered on isolated `LLMGatewayClient`, not on async `embed` from `RAGService`; Langfuse + `traceparent` are not verified on real outbound gateway calls.

**Approach:** Parametrized health contract tests; service tests with `httpx.MockTransport` on the service’s gateway for retrieve (embed + rewrite); extend trace tests for Langfuse and `traceparent` on `post`.

## Boundaries & Constraints

**Always:** Hermetic `pytest` (`rag_service_offline`, `MockTransport`). If code blocks a test (e.g. `rerank` hardcoded), fix product code in the same PR — no long-lived skips.

**Ask First:** Optional integration job for live `GET /v1/models` only if CI already supports `RUN_INTEGRATION=1`.

**Never:** Mandatory OTLP collector or new default CI services. New tests complement `tests/unit/test_gateway_slot_headers.py`, do not copy it.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected | Error |
|----------|---------------|----------|-------|
| R-14 | `hybrid` / new `rerank_enabled` vary | `health().capabilities` matches | Degraded test unchanged |
| R-15 | `retrieve` + mock transport | `/v1/embeddings` has `X-Slot` + trace when `trace_ctx` set | — |
| R-16 | rewrite on + `req.rewrite` | `/v1/chat/completions` has retrieval `X-Slot` + trace | — |
| NFR-4 | `trace_ctx` has Langfuse name + `traceparent` | Same on outbound `POST` | No invented headers |

</frozen-after-approval>

## Code Map

- `support_rag/service.py` — `health`, `retrieve` (`embed`, rewrite), `index` (`embed_sync`)
- `support_rag/gateway.py` — `embed` / `embed_sync` / `chat_completion_sync`, `_slot_headers`, `describe_models`
- `support_rag/app.py` — `_trace_ctx`
- `support_rag/config.py` — add `retrieval.rerank_enabled`, document in YAML
- `tests/contract/test_health_capabilities.py`, new `test_service_gateway_roundtrip` (or similar), `tests/test_gateway_trace_ctx.py`

## Tasks & Acceptance

**Execution:**

- [x] `support_rag/config.py` -- Add `rerank_enabled: bool = True` to `RetrievalConfig`; document in `config.example.yaml` (and e2e yaml if needed).
- [x] `support_rag/service.py` -- `capabilities["rerank"]` from `retrieval.rerank_enabled`.
- [x] `tests/contract/test_health_capabilities.py` -- Parametrize hybrid + `rerank_enabled`; mock `describe_models` (R-14).
- [x] `tests/contract/test_service_gateway_roundtrip.py` (new) -- Mock transport on service gateway; stub `aquery`; assert embed `X-Slot` + trace (R-15).
- [x] Same file -- Rewrite path: `X-Slot` = retrieval slot + trace (R-16).
- [x] `tests/test_gateway_trace_ctx.py` -- Langfuse + `traceparent` on real `post` from gateway methods (NFR-4).
- [x] `mvp1-prd-to-automated-tests-gap-table.md` + `mvp1-prd-automation-first-gap-table.md` -- Update rows when tests land.

**Acceptance Criteria:**

- Given `RetrievalConfig` differs only in `hybrid` and `rerank_enabled`, when `health()` runs, then `capabilities.hybrid` and `capabilities.rerank` match (R-14).
- Given mock transport on the service gateway and a retrieve that calls async `embed`, when the request is captured, then it has `X-Slot` = embedding slot and trace headers when `trace_ctx` is set (R-15).
- Given query rewrite and `req.rewrite`, when the rewrite LLM runs, then `/v1/chat/completions` has retrieval `X-Slot` and trace headers (R-16).
- Given `trace_ctx` includes the Langfuse header name and `traceparent`, when the gateway `POST`s, then those headers are present (NFR-4).

## Spec Change Log

- **2026-04-25** — Draft from automation-first backlog.
- **2026-04-25** — Plan: `rerank_enabled`, I/O matrix, service round-trip tests (step-02).
- **2026-04-25** — Implemented: `rerank_enabled`, R-14 matrix tests, `test_service_gateway_roundtrip.py` (R-15/R-16), NFR-4 `post` header tests, gap tables updated.

## Design Notes

- `rerank_enabled` default `True` keeps current health behavior; enables a real matrix for R-14.
- Prioritize `retrieve()` for R-15/R-16; `index()` uses `embed_sync` and is secondary if time-boxed. Use `ServiceConfig.langfuse_header_name` in tests, not a hardcoded header string.

## Verification

**Commands:**

- `pytest tests/unit/test_gateway_slot_headers.py tests/test_gateway_trace_ctx.py tests/contract/test_health_capabilities.py tests/contract/test_service_gateway_roundtrip.py -q`
- `pytest tests/ -q`
- `ruff check .`

**Manual (optional):** `RUN_INTEGRATION=1` — non-empty `describe_models` on a real gateway.

## Suggested Review Order

**Health capabilities (R-14)**

- New `rerank_enabled` on `RetrievalConfig`; health `capabilities.rerank` reads it.
  [`config.py:55`](../../support_rag/config.py#L55)

- Health JSON exposes `r.rerank_enabled` instead of a literal.
  [`service.py:402`](../../support_rag/service.py#L402)

- Parametrized matrix over hybrid × rerank vs `service.health()`.
  [`test_health_capabilities.py:11`](../../tests/contract/test_health_capabilities.py#L11)

**Service → gateway (R-15 / R-16)**

- MockTransport + `retrieve`: async embed and rewrite paths assert `X-Slot` and trace headers.
  [`test_service_gateway_roundtrip.py:106`](../../tests/contract/test_service_gateway_roundtrip.py#L106)

- Same file: rewrite path uses retrieval slot on outbound chat.
  [`test_service_gateway_roundtrip.py:161`](../../tests/contract/test_service_gateway_roundtrip.py#L161)

**NFR-4 (headers on POST)**

- Langfuse + `traceparent` on `embed_sync` and `chat_completion_sync` through MockTransport.
  [`test_gateway_trace_ctx.py:77`](../../tests/test_gateway_trace_ctx.py#L77)

**Docs / examples**

- Sample YAML documents `retrieval.rerank_enabled` for operators.
  [`config.example.yaml:29`](../../config.example.yaml#L29)

- Gap table rows (R-14, R-15, R-16, NFR-4) and test list.
  [`mvp1-prd-to-automated-tests-gap-table.md:49`](mvp1-prd-to-automated-tests-gap-table.md#L49)
