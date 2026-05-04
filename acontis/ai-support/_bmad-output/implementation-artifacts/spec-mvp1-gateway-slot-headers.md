---
title: 'MVP1 PRD — gateway X-Slot headers (R-15, R-16)'
type: 'feature'
created: '2026-04-25T20:00:00Z'
status: 'done'
baseline_commit: 'ba724e275e455dfe7a534a4da20db555ae76a437'
context:
  - 'support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** R-15 (embeddings via gateway with `X-Slot: embedding`) and R-16 (chat/rewrite via `retrieval_llm` slot) are **Missing** in the gap table. The implementation lives in `LLMGatewayClient`, but there is no focused automated assert that outgoing `httpx` calls include the correct `X-Slot` (and that slot names match config).

**Approach:** Add **unit tests** in `tests/unit/` (or `tests/contract/`) that mock `httpx` transport / `AsyncClient` and assert request headers for `embed`, `embed_sync`, `chat_completion`, and `chat_completion_sync` include `X-Slot` with values from `AppConfig` (`embedding_slot`, retrieval LLM slot as implemented).

## Boundaries & Constraints

**Always:** No real HTTP; use `respx`, `httpx.MockTransport`, or library-appropriate mock. No provider SDKs.

**Ask First:** If gateway adds new slot kinds, extend the test matrix in a follow task.

**Never:** Change gateway URL contract beyond what the PRD requires; this spec is **header observability** only.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected | Error handling |
|----------|---------------|----------|----------------|
| R-15 embed | `embed([text], kind=query\|doc)` | Request headers include `X-Slot: <embedding_slot from config>` | Gateway errors surface as today |
| R-16 chat | `chat_completion` with messages | Request headers include slot for retrieval LLM per `gateway.py` | Same |

</frozen-after-approval>

## Code Map

- `support_rag/gateway.py` — `LLMGatewayClient`, `_headers` or inline `X-Slot`, `embed`, `embed_sync`, `chat_completion`, `chat_completion_sync`.
- `support_rag/config.py` — `embedding_slot`, model display / slot config for retrieval LLM.
- `support_rag/embeddings.py` — `GatewayEmbeddings` calls `gateway.embed` (indirect coverage if unit tests call `LLMGatewayClient` directly with mocked transport).

## Tasks & Acceptance

**Execution:**

- [x] `tests/unit/test_gateway_slot_headers.py` — Construct minimal `AppConfig` + `LLMGatewayClient` with mock transport; for each of embed (async/sync) and chat (async/sync), assert captured request headers `X-Slot` match configured embedding and retrieval LLM slots (R-15, R-16).
- [x] `README.md` — Optional one-liner that slot header behavior is covered under pytest.

**Acceptance Criteria:**

- Given mocked HTTP layer, when `embed` is called, then the outgoing request includes `X-Slot` equal to the configured embedding slot (R-15).
- Given mocked HTTP layer, when `chat_completion` is called for retrieval-style use, then the outgoing request includes the expected retrieval LLM `X-Slot` (R-16).
- Given default `pytest`, when the suite runs, then these tests do not require network or docker.

## Spec Change Log

- 2026-04-25 — Authored from gap table “Suggested next steps” item 2.
- 2026-04-25 — Implemented: `test_gateway_slot_headers.py`, README line; spec marked `done`.

## Design Notes

Keep tests hermetic: build config from a dict or `AppConfig` factory used elsewhere in tests. Prefer capturing the last request in a list on the mock transport.

## Verification

**Commands:** `python -m pytest tests/unit/test_gateway_slot_headers.py -q` · `ruff check support_rag tests`

**Manual checks:** None.

## Suggested Review Order

- MockTransport plus patched `httpx` clients; saved real `Async`/`Client` refs avoid shared-module patch recursion
  [`test_gateway_slot_headers.py:20`](../../tests/unit/test_gateway_slot_headers.py#L20)

- R-15: `X-Slot` equals `embedding_slot` for async and sync `embed`
  [`test_gateway_slot_headers.py:64`](../../tests/unit/test_gateway_slot_headers.py#L64)

- R-16: default `retrieval_slot` and explicit `slot=` on `chat_completion` (async/sync)
  [`test_gateway_slot_headers.py:98`](../../tests/unit/test_gateway_slot_headers.py#L98)

- README points reviewers at the new module
  [`README.md:45`](../../README.md#L45)
