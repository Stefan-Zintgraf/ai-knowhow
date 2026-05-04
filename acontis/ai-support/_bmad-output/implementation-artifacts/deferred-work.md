# Deferred work

Entries are append-only. Pulled in when you start a new quick-dev or story that references this file.

## 2026-04-25 — NFR-1 / NFR-2 (perf) from `support_rag_mvp1_prd.md`

**Superseded (wiring) by** [`spec-mvp1-ci-eval-nfr-perf-gating.md`](spec-mvp1-ci-eval-nfr-perf-gating.md): GitLab jobs `nfr_retrieve_smoke` + [README MVP1 eval + perf CI](../../README.md#mvp1-eval--perf-ci-gitlab) document **report-only vs enforce** and runner tag `rag-mvp1-eval`. **Remaining (ops):** point `RAG_EVAL_BASE_URL` at your stack, tune `uvicorn` workers in compose for your load, and flip `NFR_ENFORCE` / `allow_failure` when ready to gate.

**Goal (unchanged for traceability):** p95 `retrieve` ≤ 2.0s (NFR-1) and ≥5 concurrent retrieves (NFR-2).

## 2026-04-25 — split from `spec-mvp1-prd-verification-hardening.md`

**Status:** Script and README golden-set section are **done**; scheduled GitLab `hybrid_golden_eval` is in [`.gitlab-ci.yml`](../../.gitlab-ci.yml) (see `spec-mvp1-ci-eval-nfr-perf-gating.md`).

**Original goal (met in repo):** `eval/eval_hybrid_vs_dense.py`, `ENFORCE_THRESHOLDS`, golden seeding in `README.md`, CI on tagged runner.

## 2026-04-25 — `allow_remote: false` E2E: LiteLLM key + automated evidence

**From `spec-mvp1-allow-remote-false-acceptance` review (defer):** Runbook and `docs/litellm-ollama-e2e.example.yaml` use **Ollama-only** routes as the practical local-only check. **Wired in CI (schedule/web/API):** GitLab job `e2e_privacy_allow_remote` in [`.gitlab-ci.yml`](../../.gitlab-ci.yml) runs `e2e_gateway_preflight` + `RUN_E2E_PRIVACY=1 pytest -m e2e_privacy` on the **`rag-mvp1-eval`** tag (see [README — MVP1 eval + perf CI](../../README.md#mvp1-eval--perf-ci-gitlab)). If your LiteLLM build documents an explicit `allow_remote`-style (or per-slot) **YAML** key, add it to the **committed** example and cross-link from the runbook; the example file comments on PRD naming vs. upstream keys. Optional: assert or scrape LiteLLM startup logs when debugging a red E2E job.

## 2026-04-25 — KB `chunk_size` vs LlamaIndex `SentenceWindowNodeParser`

**Superseded by** [`spec-mvp1-automation-backlog-kb-chunking-r9.md`](spec-mvp1-automation-backlog-kb-chunking-r9.md) (2026-04-25): `chunk_kb` uses `SentenceSplitter.split_text` as `sentence_splitter` for `SentenceWindowNodeParser` (`support_rag/chunking.py`); `chunker_version.kb` is `kb-v2`; tests in `tests/unit/test_chunking_kb_vs_tickets_r9.py`.

_Original note:_ `SentenceWindowNodeParser.from_defaults` did not take `chunk_size`; `config.chunking.kb.chunk_size` was unused until the wiring above.
