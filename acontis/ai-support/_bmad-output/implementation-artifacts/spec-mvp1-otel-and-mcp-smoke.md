---
title: 'MVP1 PRD — OTel spans on index/delete, gateway trace headers, MCP tool smoke'
type: 'feature'
created: '2026-04-25T18:00:00Z'
status: 'done'
baseline_commit: 'bbc7bdebd96c9a7f28937d2f595246dd1f515a5a'
context:
  - 'support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/spec-mvp1-prd-verification-hardening.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** NFR-4 says every `retrieve` and `index` call emits a span. `app.py` wraps `POST /rag/retrieve` in a span, but **index** and **delete** do not. R-19/20 require a discoverable `support-rag` MCP; there is no CI check that the module loads and exposes `rag.health`, `rag.retrieve`, `rag.index`. NFR-4 also implies **correlation** to gateway calls — the safest automated check is to assert `LLMGatewayClient._slot_headers` (or a thin wrapper) passes through `traceparent` when `trace_ctx` is set, without a live HTTP server.

**Approach:** Add `opentelemetry` spans for `post_index` and `del_index` matching `post_retrieve` (same `trace.get_tracer("support_rag")` pattern). In tests, use `opentelemetry-sdk` `InMemorySpanExporter` (or `TestSpanExporter` pattern) in a test-only `TracerProvider` if needed to avoid flakiness, or assert `tracer` mock calls. Add `tests/test_gateway_trace_ctx.py` for header merge. Add `tests/test_mcp_tools.py` that imports `support_rag.mcp_server` and lists tools (or checks `mcp` object attributes) — if `mcp` is optional, add it to `dev` extras and document. Update README for OTel and MCP test deps.

## Boundaries & Constraints

**Always:** No OTLP required in default pytest; in-process export only. No provider SDKs.

**Ask First:** Whether MCP smoke should **import-only** (no `fastmcp` runtime) or require full `mcp` package in CI `dev` extras.

**Never:** Add production OTLP to tests; do not add Langfuse server dependency.

## I/O & Edge-Case Matrix

| Scenario | Input | Expected |
|----------|--------|----------|
| Span on index | Client posts to `/rag/index/...` | Span with name e.g. `rag.index` recorded |
| Span on delete | Client DELETE to `/rag/index/...` | Span e.g. `rag.delete` |
| Gateway headers | `trace_ctx={"traceparent": "00-..."}` | Keys merged into post headers to gateway |
| MCP | `import support_rag.mcp_server` | Three R-19 tools discoverable |

</frozen-after-approval>

## Code Map

- `support_rag/app.py` — `post_retrieve` span; add for `post_index`, `del_index`.
- `support_rag/gateway.py` — `_slot_headers` + `trace_ctx`.
- `support_rag/mcp_server.py` — `FastMCP` tools.
- `pyproject.toml` — `dev` / optional `mcp` for CI import path.

## Tasks & Acceptance

**Execution:**

- [x] `support_rag/app.py` — `with tracer.start_as_current_span("rag.index")` / `rag.delete` around index/delete bodies; pass `_trace_ctx(request)`.
- [x] `tests/contract/test_otel_routes.py` — Mocked `get_tracer` and assert `start_as_current_span` names (avoids global `TracerProvider` issues).
- [x] `tests/test_gateway_trace_ctx.py` — Direct `_slot_headers` check for `traceparent` in `trace_ctx`.
- [x] `tests/test_mcp_tools.py` — `mcp.list_tools()` smoke for R-19 names.
- [x] `README.md` (no `pyproject.toml` dep change: `mcp` already a core dependency).

**Acceptance Criteria:**

- Given a test that enables in-process span export, when index and delete routes are hit, then at least one span per request is created with names `rag.index` and `rag.delete` (or consistent documented naming).
- Given `trace_ctx` includes `traceparent`, when the gateway client builds request headers, then that value is present on outbound calls.
- Given CI installs `dev` (and MCP as decided), when `tests/test_mcp_tools.py` runs, then the three tool identifiers for R-19 are found.

## Spec Change Log

- 2026-04-25 — Added **Risks / pre-mortem** (elicitation) for NFR-4/MCP scope and `app.py` coordination.
- 2026-04-25 — Implementation: spans on index/delete, `RAGService.delete(..., trace_ctx=...)`; tests use mocked tracer; FastAPI `Request` before body on index/delete for correct binding; gap table and README updated.

## Design Notes

If `TestSpanExporter` setup fights FastAPI lifespans, fall back to `unittest.mock` on `trace.get_tracer` and assert `start_as_current_span` call count for the route under test (still satisfies “span emitted” for NFR-4 if product agrees).

## Risks / pre-mortem

*Failure imagined:* Spans and MCP tests pass in CI, but NFR-4 or R-19 still fail in a real run (collector, or MCP actually invoked).

- **Span in CI vs trace in the collector** — A span *name* in tests may not match production wiring (e.g. index/delete work outside the span, async gap). If stable enough, add that the same handler body runs under the active span, or document that MVP1 NFR-4 here means “span emitted in offline tests” unless OTLP is added later.
- **MCP import-only** — Discovering three tool *identifiers* does not prove tools call the right handlers. If **Ask First** allows, add a minimal invoke/call with mocks; otherwise document that R-19 in this spec is discoverability, not E2E behavior.
- **Gateway** — `traceparent` in `_slot_headers` is the right unit seam; a full E2E trace is still not required.
- **`app.py` with `spec-mvp1-admin-filters-and-erasure-tests.md`** — Both specs edit `app.py`. Merge in one go or follow an explicit order to avoid partial span coverage (e.g. index wrapped, delete not).

## Verification

**Commands:** `python -m pytest tests/ -q` · `python -m ruff check support_rag tests`

## Suggested Review Order

- `Request` then body on index/delete so FastAPI binds JSON and W3C headers correctly; spans wrap only the awaited service calls.
  [`app.py:112`](../../support_rag/app.py#L112)

- Optional `trace_ctx` on `delete` keeps the route and service call signatures aligned with `index` and retrieve.
  [`service.py:362`](../../support_rag/service.py#L362)

- Mocked `get_tracer` records span **names** without fighting OTel’s “no TracerProvider override” during teardown.
  [`test_otel_routes.py:1`](../../tests/contract/test_otel_routes.py#L1)

- `traceparent` merge is asserted on the real `_slot_headers` helper used by all gateway posts.
  [`test_gateway_trace_ctx.py:1`](../../tests/test_gateway_trace_ctx.py#L1)

- R-19 tool identifiers via `list_tools()` (full `mcp` package as already required by `mcp_server`).
  [`test_mcp_tools.py:1`](../../tests/test_mcp_tools.py#L1)

- User-facing test notes for NFR-4 and MCP in the README; gap table points at the new rows.
  [`README.md:37`](../../README.md#L37)
