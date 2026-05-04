---
title: 'MVP1 PRD — MCP tool binding and admin vs service token (R-19, R-20)'
type: 'feature'
created: '2026-04-25T20:00:00Z'
status: 'done'
baseline_commit: '96222fbfb400475dc1ee04f082687bc7f52bc011'
context:
  - 'support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** R-19 and R-20 are **Partial**: `tests/test_mcp_tools.py` only checks tool **names** exist. The PRD requires MCP to mirror REST: `rag.health` and `rag.retrieve` use the **service** token; `rag.index` uses the **admin** token. There is no automated proof that the MCP layer sends the right bearer to the right path or that a service token cannot call admin-only `POST /rag/index/{namespace}` through the tool.

**Approach:** Extend **pytest** with `httpx` / `respx` (or `unittest.mock` on `httpx.AsyncClient`) to (1) invoke MCP tool callables in-process with **mocked** HTTP so no real server is required, and (2) assert URL, method, and `Authorization` header for each tool. Add negative case: `rag.index` with only `RAG_SERVICE_TOKEN` env (or wrong token) does not send admin bearer and surfaces expected failure (or skip if implementation raises at tool entry before HTTP).

## Boundaries & Constraints

**Always:** No live RAG process in default CI. Import `support_rag.mcp_server` and patch `httpx.AsyncClient` (or the request function) at module level used by tools.

**Ask First:** Whether to test subprocess MCP stdio; default should stay in-process.

**Never:** Weaken REST admin gating; tests **observe** `mcp_server.py` contract only.

## I/O & Edge-Case Matrix

| Tool | Token | Expected URL / method | Error |
|------|--------|------------------------|-------|
| `rag.health` | service | `GET .../rag/health` with service `Authorization` | httpx 401 if server would reject (mock 401 path optional) |
| `rag.retrieve` | service | `POST .../rag/retrieve` | same |
| `rag.index` | admin | `POST .../rag/index/{ns}` with admin `Authorization` | If admin token missing, `RuntimeError` at `_h(False)` (assert message) |
| R-20 | service token used for `rag.index` | Should not succeed — expect exception before 200 or mock returns 401 | N/A |

</frozen-after-approval>

## Code Map

- `support_rag/mcp_server.py` — `rag_health`, `rag_retrieve`, `rag_index`, `_h(service: bool)`.
- `support_rag/app.py` — REST routes the MCP calls (reference only).
- `tests/test_mcp_tools.py` — extend with new tests or `tests/contract/test_mcp_rest_parity.py`.

## Tasks & Acceptance

**Execution:**

- [x] `tests/test_mcp_tools.py` or new `tests/contract/test_mcp_http_binding.py` — Parametrize env: set `RAG_MCP_BASE_URL` to a dummy; patch `httpx.AsyncClient` to capture the last request per call; run `await rag_retrieve(...)` and assert POST body JSON matches `RetrievalRequest` fields and path ends with `/rag/retrieve` with service bearer.
- [x] Assert `rag_health` issues GET to `/rag/health` with service bearer.
- [x] Assert `rag_index` issues POST to `/rag/index/{namespace}` with **admin** bearer from `RAG_ADMIN_TOKEN` (R-19, R-20).
- [x] **Negative (R-20):** With `RAG_ADMIN_TOKEN` unset and `RAG_SERVICE_TOKEN` set, when `rag_index` is invoked, then the tool raises or the mock receives no valid admin call (per current `mcp_server.py` behavior — document expected behavior in test docstring).
- [x] `README.md` — MCP test subsection: in-process binding tests, no stdio required for CI.

**Acceptance Criteria:**

- Given patched `httpx`, when `rag.retrieve` runs, then the request uses the service token header and correct path (R-19).
- Given patched `httpx`, when `rag.index` runs with admin env, then the request uses the admin token header (R-20).
- Given service token only, when an operator attempts `rag.index`, then the failure mode matches the PRD (no silent success with service credentials).

## Spec Change Log

- 2026-04-25 — Authored from gap table “Suggested next steps” item 4.
- 2026-04-25 — Implemented: `tests/contract/test_mcp_http_binding.py` + README MCP binding paragraph; in-review.
- 2026-04-25 — Review trail appended; `status: done` after local verification (pytest + gap table).

## Design Notes

`mcp_server` uses `RetrievalRequest.model_dump_json()` for retrieve — assert content-type and body shape. If `list_tools` smoke stays separate, keep one file import cost tolerable (lazy import already in test).

## Verification

**Commands:** `python -m pytest tests/test_mcp_tools.py tests/contract/test_mcp_http_binding.py -q` · `ruff check support_rag tests`

**Manual checks:** None.

## Suggested Review Order

- Mock `httpx.AsyncClient` on the MCP module and route responses by path shape.
  [`test_mcp_http_binding.py:22`](../../tests/contract/test_mcp_http_binding.py#L22)

- R-19: `rag_health` → GET, service bearer, health JSON body returned.
  [`test_mcp_http_binding.py:60`](../../tests/contract/test_mcp_http_binding.py#L60)

- R-19: `rag_retrieve` → POST body matches `RetrievalRequest`, service bearer.
  [`test_mcp_http_binding.py:79`](../../tests/contract/test_mcp_http_binding.py#L79)

- R-20: `rag_index` → POST with admin bearer and `docs` payload; path includes namespace.
  [`test_mcp_http_binding.py:115`](../../tests/contract/test_mcp_http_binding.py#L115)

- R-20: service-only token cannot index — `RuntimeError` before HTTP.
  [`test_mcp_http_binding.py:136`](../../tests/contract/test_mcp_http_binding.py#L136)

- Contract reference: same bearer rule as `mcp_server._h` (unchanged in this work).
  [`mcp_server.py:22`](../../support_rag/mcp_server.py#L22)

- README: documents in-process binding tests, no stdio in CI.
  [`README.md:45`](../../README.md#L45)
