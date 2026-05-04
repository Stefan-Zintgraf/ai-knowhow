---
title: 'MVP1 PRD — §2.8(5) allow_remote: false E2E smoke'
type: 'feature'
created: '2026-04-25T20:00:00Z'
status: 'done'
baseline_commit: '33951aaf2ed9d55d641d0f92df91f5a7db2dd594'
context:
  - 'support_rag_mvp1_prd.md'
  - 'support_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md'
  - 'docker-compose.yaml'
  - 'config.example.yaml'
  - 'config.e2e.example.yaml'
  - 'support_rag/gateway.py'
  - 'docs/runbook-allow-remote-false-e2e.md'
  - 'docs/litellm-ollama-e2e.example.yaml'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** §2.8 acceptance item **5** (per `support_rag_mvp1_prd.md`) requires that with **LLM Gateway** configured to `allow_remote: false`, indexing and retrieval still work with **local** embedder and retrieval LLM only. [`mvp1-prd-to-automated-tests-gap-table.md`](mvp1-prd-to-automated-tests-gap-table.md) marks this **Partial** until a scheduled self-hosted runner proves it; see [`mvp1-prd-automation-first-gap-table.md`](mvp1-prd-automation-first-gap-table.md) for automation mandate. It is an **E2E** and **gateway-policy** test, not a `support_rag` unit test alone.

**Approach:** Use the **official gateway HTTP interface** only — the same contract as production `LLMGatewayClient` (`llm_gateway.base_url`, `POST /v1/embeddings` and `POST /v1/chat/completions` with `X-Slot` set to `embedding_slot` and `retrieval_slot`; R-17: no provider SDKs). The **documented E2E stack** is **`support_rag` → LiteLLM (OpenAI-compatible API) → Ollama** serving **`all-minilm`** and **`llama3.2:1b`**. **For this testing path, only local models are used** — Ollama pulls only; **no** OpenAI/Anthropic/Azure (or other cloud) routes in the E2E LiteLLM profile. **LiteLLM** must be configured for **`allow_remote: false`** (or equivalent) on the relevant slots so the smoke matches `support_prd.md` / PRD local-only intent. Add a **small, dedicated test path in this repo** (scripts + env-gated `pytest` `e2e_privacy`, skipped by default) that: (1) runs a **preflight** to **LiteLLM**’s `base_url` to verify **embedding and retrieval-LLM** routes return **200**; if not, **exit non-zero and print** clear errors — including that **Ollama** may need **`ollama pull`** for the model IDs in **`config.e2e.example.yaml`**, and that **LiteLLM** must be running and reachable; (2) with preflight green, run **minimal** index + retrieve through `support_rag` against that LiteLLM; (3) document compose/env in the runbook. Optional: start LiteLLM via compose `profiles` or run it on the host per org.

## Boundaries & Constraints

**Always:** The **only** allowed way to talk to the LLM for this spec’s automated checks is the **same** OpenAI-compatible surface `support_rag` uses in production (paths, headers, JSON shapes per `LLMGatewayClient`); the **assumed** deployment points `llm_gateway.base_url` at **LiteLLM** (not directly at Ollama’s port unless LiteLLM is colocated/transparent in your setup). **Preflight and smoke** call that URL via **reused** `LLMGatewayClient` or a thin script that **must not** introduce a second, unofficial API. Fail closed on privacy: **LiteLLM** (not `support_rag`) enforces `allow_remote: false` / local-only routes — assert at the **LiteLLM** boundary and logs as documented. **If models or LiteLLM are unavailable, fail loudly** with the prescribed user-facing error text (no tracebacks-only failures).

**Ask First:** For **all-local, no-Docker** defaults, use **`docs/runbook-allow-remote-false-e2e.md` §9** (recorded) and **§2.1** / **§3.1** (simple `model`-based LiteLLM routing, how to check auth). **E2E model tags:** `config.e2e.example.yaml` (`all-minilm`, `llama3.2:1b`).

**Never:** Mark this as default `pytest` on developer laptops if it requires a full stack. **Never** use mock transports or a fake ad-hoc JSON API for the **E2E preflight** — only the official gateway interface; mocks stay in unit/contract tests elsewhere. **Never** register **cloud** LLM providers for the **documented E2E** LiteLLM config — **local Ollama models only** for preflight and `e2e_privacy`.

## I/O & Edge-Case Matrix

| Step | State | Expected |
|------|--------|----------|
| LiteLLM up | `allow_remote: false` (or equivalent) + Ollama backends | Slots route to local Ollama models only; no cloud fallback |
| Index | Admin token, small doc | 200, chunks written |
| Retrieve | Service token, query | 200, non-empty or empty valid |
| Preflight | Embed + chat **missing**, LiteLLM down, or Ollama not serving models | **Non-zero**; **stderr** lists **LiteLLM** URL, **Ollama** + `ollama pull …` (from `config.e2e.example.yaml`) |
| Preflight | LiteLLM + Ollama paths **ok** for embed + chat | Continue to E2E index/retrieve |

</frozen-after-approval>

## Default local endpoints (E2E smoke)

Documented **host ports** for the runbook, preflight, and `e2e_privacy` (override only via env if needed):

| Service | Default URL |
|---------|-------------|
| **LiteLLM** (`llm_gateway.base_url`) | `http://127.0.0.1:4000` |
| **support_rag** (HTTP, index/retrieve) | `http://127.0.0.1:8080` |
| **Qdrant** | `http://127.0.0.1:6333` |

## Code Map

- `support_rag_mvp1_prd.md` — §2.8 item 5; defines acceptance for local-only path.
- `support_prd.md` — FR-23, YAML examples for per-slot `allow_remote`.
- `docker-compose.yaml` — optional **Qdrant + RAG** in Docker for other workflows; the **E2E runbook** is **all-local, no Docker** (see `docs/runbook-allow-remote-false-e2e.md`). **Default** triple: **4000** / **8080** / **6333** on `127.0.0.1`.
- `config.example.yaml` / runtime `config.yaml` — default dev (1024-d vectors in example).
- `config.e2e.example.yaml` — **E2E profile:** `llm_gateway.base_url` → **LiteLLM**; `display_models` names **`all-minilm`** and **`llama3.2:1b`**; **`qdrant.vector_size: 384`**, **`support_rag_e2e_`**. Use with `RAG_CONFIG=config.e2e.yaml`.
- `docs/litellm-ollama-e2e.example.yaml` — **LiteLLM** `model_list` mapping logical names **`embedding`** and **`retrieval`** (request JSON body from `LLMGatewayClient`) to **`ollama/all-minilm`** and **`ollama/llama3.2:1b`**. `X-Slot` headers are still sent for R-15/R-16; routing is typically by **`model`** — confirm for your LiteLLM version (see runbook §9).
- `docs/runbook-allow-remote-false-e2e.md` — operator runbook: ports, start order, env, smoke curls, evidence, preflight error template, **open questions** §9.
- `support_rag/gateway.py` — `LLMGatewayClient`; **authoritative** contract (`/v1/embeddings` + `/v1/chat/completions`, body `model` **`embedding`** / **`retrieval`**, `X-Slot` from config slots).
- `scripts/e2e_gateway_preflight.py` (name flexible) — load `AppConfig` (`RAG_CONFIG` → **LiteLLM** `base_url`), `LLMGatewayClient`, hit **(a)** `GET /v1/models` if usable, **(b)** minimal `POST /v1/embeddings` + `POST /v1/chat/completions` so embed + chat paths return **200**; on failure, **stderr**: unreachable **LiteLLM**, and/or **Ollama** with **`ollama pull all-minilm`** / **`ollama pull llama3.2:1b`** (from `config.e2e.example.yaml`). Exit non-zero. No mocks.
- `scripts/smoke_allow_remote.sh` (or `.ps1`) — optional orchestration: run **preflight** first, then Qdrant + RAG health, then index/retrieve; fail fast on preflight.
- `tests/conftest.py` — skip `e2e_privacy` unless `RUN_E2E_PRIVACY=1` (parallel to `RUN_INTEGRATION`); for `e2e_privacy` collection, either invoke the same preflight as subprocess/import **before** tests or a session-scoped fixture that calls it once — **do not** start long-running Ollama from pytest.
- `tests/e2e/test_allow_remote_privacy.py` — `@pytest.mark.e2e_privacy`: `httpx` to **`http://127.0.0.1:8080`** (or `E2E_RAG_BASE_URL` if implemented) for minimal index/retrieve; require HTTP 200, valid JSON. Docstring: `RUN_E2E_PRIVACY=1`, ports **4000/8080/6333**, `RAG_CONFIG` / models.
- `pyproject.toml` — register `e2e_privacy` in `[tool.pytest.ini_options].markers`.
- `tests/conftest.py` — (see above) also preserves skip for `integration` / `requires_services` when `RUN_INTEGRATION` unset; `e2e_privacy` is orthogonal.

## Tasks & Acceptance

**Execution:**

- [x] `docs/runbook-allow-remote-false-e2e.md` — **Done:** stack, ports **4000/8080/6333**, env, LiteLLM + Ollama, smoke curls, evidence, preflight template, **§9 open questions** for org-specific follow-up.
- [x] `docs/litellm-ollama-e2e.example.yaml` — **Done:** Ollama-only `model_list` for `embedding` + `retrieval` logical model names.
- [x] `README.md` — **Done:** links to runbook + LiteLLM example; E2E section updated.
- [x] `scripts/e2e_gateway_preflight.py` — **Done:** `LLMGatewayClient` embed + chat; stderr template + non-zero on failure; config path from CWD or repo root.
- [x] `docker-compose.yaml` — **N/A (documented):** default `docker-compose.yaml` keeps Qdrant + RAG only; E2E uses **host** LiteLLM + Ollama per runbook. Optional future `profiles` for a gateway service is not required for acceptance.
- [x] `scripts/smoke_allow_remote.sh` and `scripts/smoke_allow_remote.ps1` — **Done:** preflight, Qdrant + RAG health wait, index + retrieve; no `allow_remote: true` in the documented profile.
- [x] `pyproject.toml` — **Done:** marker `e2e_privacy`.
- [x] `tests/conftest.py` — **Done:** skip `e2e_privacy` unless `RUN_E2E_PRIVACY=1`.
- [x] `tests/e2e/test_allow_remote_privacy.py` — **Done:** session fixture runs preflight subprocess; `httpx` index + retrieve with 200 and `chunks` in body.

**Acceptance Criteria:**

- Given the **documented** gateway URL and the same `AppConfig` / `LLMGatewayClient` the service uses, when **`scripts/e2e_gateway_preflight` (or equivalent)** runs, then it **verifies** that the **embedding** and **retrieval LLM** backends respond successfully via the **official** API; when either is missing or unreachable, the process **exits non-zero** and **prints** a clear message: what is missing, that **Ollama** may need to be installed and running, and the **exact** `ollama pull <model>` lines for the **model IDs named in the runbook** (embed + LLM), plus pointer to the runbook.
- Given **LiteLLM** configured with `allow_remote: false` (or equivalent) per `support_prd.md` for the slots `support_rag` uses, when the runbook (or `RUN_E2E_PRIVACY=1 pytest -m e2e_privacy` after a green preflight) is executed, then a minimal **index** and **retrieve** complete with HTTP 200, and the runbook’s **evidence** step confirms no remote provider path was used.
- Given default developer `pytest` without `RUN_E2E_PRIVACY=1` (and without the full stack), when the suite runs, then `e2e_privacy` tests are **skipped**, not failed.
- Given a maintainer following only committed artifacts, when they read `README.md` and the runbook, then they can reproduce the smoke (preflight + optional pytest) with **LiteLLM**, **Ollama**, and **pulled** models, without guesswork.

## Spec Change Log

- 2026-04-25 — Authored from gap table “Suggested next steps” item 5; **draft** until gateway integration path is fixed (may live outside this repo).
- 2026-04-25 — **Planning (step-02):** Filled from repo investigation: compose has no in-tree gateway; conftest/marker tasks added; runbook + script + optional pytest e2e path.
- 2026-04-25 — **Update:** E2E must use the **official** `LLMGatewayClient` interface only; add in-repo `scripts/e2e_gateway_preflight.py` (or equivalent) + env-gated pytest path; on missing embed/LLM, **actionable** stderr (install **Ollama**, `ollama pull` for runbook model IDs).
- 2026-04-25 — **Update:** Add `config.e2e.example.yaml` with **`all-minilm`** (embed), **`llama3.2:1b`**, `vector_size: 384`, `support_rag_e2e_` prefix; document in `README.md`.
- 2026-04-25 — **Update:** E2E gateway is **LiteLLM** in front of **Ollama**; `allow_remote: false` enforced on LiteLLM; `llm_gateway.base_url` → LiteLLM, not Ollama port directly (unless runbook says otherwise).
- 2026-04-25 — **Update:** Default E2E ports locked: **LiteLLM 4000**, **support_rag 8080**, **Qdrant 6333** (`http://127.0.0.1`).
- 2026-04-25 — **Update:** E2E / preflight **local models only** (Ollama); no cloud providers in the documented LiteLLM profile.
- 2026-04-25 — **Update:** Add **`docs/runbook-allow-remote-false-e2e.md`**, **`docs/litellm-ollama-e2e.example.yaml`**, **README** links; `Ask First` defers to runbook **§9**.
- 2026-04-25 — **Update:** Runbook: **all-local, no Docker**; LiteLLM **pip latest**; **simple** routing by `embedding`/`retrieval` (no `X-Slot` config on LiteLLM); §3.1 how to check **auth**; Qdrant without Docker (binary); recorded decisions in **§9**.
- 2026-04-25 — **Human approval [A]:** Spec approved; status `ready-for-dev` — frozen block locked; implementation (step-03) to follow.
- 2026-04-25 — **Implementation (step-03):** `e2e_gateway_preflight.py`, `e2e_privacy` marker + conftest + `tests/e2e/test_allow_remote_privacy.py`, `smoke_allow_remote` scripts; docker-compose left unchanged (N/A; host runbook).
- 2026-04-25 — **Review (steps 4–5):** triage: no spec revert; patch `e2e` preflight subprocess timeout; defer explicit LiteLLM `allow_remote` YAML to `deferred-work.md`; Suggested Review Order (file:line) appended; status `done`.

## Design Notes

**Repository reality:** `docker-compose.yaml` does not start **LiteLLM**; run it on the host or add an optional **compose profile** later. The **documented** path is **LiteLLM (OpenAI API) → Ollama (models)**. Preflight hits **LiteLLM**’s `base_url` (same as `LLMGatewayClient`); that proves connectivity through the **real** gateway layer. If full automation is infeasible in CI, update `mvp1-prd-to-automated-tests-gap-table.md` **§2.8 row 5** to **Partial (manual runbook)** with a pointer to the runbook.

**LiteLLM + Ollama (local-only testing):** The E2E profile uses **only** **Ollama**-served models (`all-minilm`, `llama3.2:1b`); no cloud endpoints. Retrieve text/embeddings are **nondeterministic**; E2E asserts HTTP/JSON only. **Canonical RAG config:** `config.e2e.example.yaml` — **384-d** for **`all-minilm`**, **do not** mix with default **1024-d** `config.yaml` collections; **`support_rag_e2e_`** prefix.

**Correlation:** `spec-mvp1-gateway-slot-headers.md` proves `X-Slot` to LiteLLM offline; this spec adds **Live LiteLLM + Ollama** and **allow_remote** evidence.

## Verification

**Commands:**

- `py -3.12` **preflight** entry point as implemented (e.g. `python scripts/e2e_gateway_preflight.py`) with `RAG_CONFIG` / env aligned to the smoke stack — expect: **0** when embed + chat paths return 200; **non-zero** with stderr guidance when not.
- `py -3.12 -m pytest tests/ -q` — expect: **no** new failures; `e2e_privacy` tests skipped.
- `RUN_E2E_PRIVACY=1 py -3.12 -m pytest -m e2e_privacy -q` — expect: after green preflight, tests run; on missing stack, preflight or fixture fails with the same user-visible messages (not collection errors).

**Manual checks:**

- Operator reviews **LiteLLM** config (and Ollama model tags) for `allow_remote: false` and correct slot → model routing before sign-off.

## Suggested Review Order

- **Security / privacy:** no `allow_remote: true` in the documented profile for this smoke; tokens only via env in examples.
- **CI:** default pipeline unchanged; optional scheduled job sets `RUN_E2E_PRIVACY=1` only where Qdrant + **LiteLLM** + Ollama + models exist.

**E2E gateway & preflight**

- CLIs `LLMGatewayClient` embed+chat; TCP hint then stderr template with `ollama pull` lines and runbook link.
  [`e2e_gateway_preflight.py:91`](../../scripts/e2e_gateway_preflight.py#L91)

- Operator stack, evidence §7, ports 4000/8080/6333, no Docker default.
  [`runbook-allow-remote-false-e2e.md:1`](../../docs/runbook-allow-remote-false-e2e.md#L1)

- Ollama-only `model_list` for logical names `embedding` / `retrieval`. No cloud keys in the committed example.
  [`litellm-ollama-e2e.example.yaml:15`](../../docs/litellm-ollama-e2e.example.yaml#L15)

- E2E RAG: `llm_gateway.base_url` → LiteLLM, 384-d vectors, `support_rag_e2e_` prefix.
  [`config.e2e.example.yaml:1`](../../config.e2e.example.yaml#L1)

**RAG service & Qdrant IDs**

- `LLMGatewayClient` (OpenAI shape, `X-Slot`); any changes to request paths affect preflight and prod.
  [`gateway.py:19`](../../support_rag/gateway.py#L19)

- Index/retrieve paths and gateway usage for the live E2E smoke.
  [`service.py:63`](../../support_rag/service.py#L63)

- Deterministic UUID chunk ids for Qdrant compatibility (E2E uses same code path as prod).
  [`chunk_id.py:5`](../../support_rag/chunk_id.py#L5)

**Pytest `e2e_privacy`**

- Marker and skip when `RUN_E2E_PRIVACY` unset; keeps default `pytest` laptop-safe.
  [`conftest.py:17`](../../tests/conftest.py#L17)

- Session preflight subprocess (with timeout) before HTTP tests; fails fast on dead gateway.
  [`e2e/conftest.py:16`](../../tests/e2e/conftest.py#L16)

- httpx health + index + retrieve; asserts 200 and `chunks` list shape only.
  [`test_allow_remote_privacy.py:24`](../../tests/e2e/test_allow_remote_privacy.py#L24)

**Scripts & project wiring**

- Bash/PowerShell smoke: preflight, health waits, no `allow_remote: true` in the documented path.
  [`smoke_allow_remote.ps1:1`](../../scripts/smoke_allow_remote.ps1#L1)

- Registers `e2e_privacy` marker for discoverability.
  [`pyproject.toml:58`](../../pyproject.toml#L58)

- Gap table row §2.8(5) — Partial / manual; points here and runbook.
  [`mvp1-prd-to-automated-tests-gap-table.md:83`](./mvp1-prd-to-automated-tests-gap-table.md#L83)
