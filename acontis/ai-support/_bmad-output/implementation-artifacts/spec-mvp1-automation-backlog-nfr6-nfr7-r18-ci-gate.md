---
title: 'MVP1 automation backlog — NFR-6 restart, NFR-7 401 matrix, R-18 merge gate'
type: 'feature'
created: '2026-04-25T12:00:00Z'
status: 'done'
baseline_commit: '2abd5ca'
context:
  - '_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md'
  - '_bmad-output/implementation-artifacts/mvp1-prd-automation-first-gap-table.md'
  - '.gitlab-ci.yml'
  - 'docker-compose.yaml'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The automation-first gap table lists **NFR-6**, **NFR-7**, and **R-18** as must-automate. Today **NFR-6** is only covered by in-process doubles (`tests/unit/test_service_lifecycle_nfr6.py`), not a real process or container restart. **NFR-7** is partially covered by separate contract modules (`test_auth_health.py`, `test_retrieve_http.py`, `test_admin_index_delete.py`); a new protected route can be missed because there is no single maintainable list. **R-18** relies on a `@pytest.mark.slow` Hub load that skips when offline; the default GitLab `test` job only runs `tests/unit/test_mvp1_deliverable_cli.py`, so merge-pipeline policy for the cross-encoder smoke must be made explicit (cache, stub, or job scope).

**Approach:** Add **compose- or process-level** automation (or a documented, still-automated GitLab job) that restarts the API, waits for readiness, and repeats a minimal smoke (health and/or retrieve). Replace ad hoc 401 tests with a **parametrized contract** driven by one source of truth (canonical route/method list or **FastAPI router introspection** filtered to dependencies that use `require_service` / `require_admin`, with documented public-route exceptions if any are added later). For **R-18**, either **cache** the CrossEncoder model path in CI, provide a **deterministic test double** for the merge gate, or **define** in README + `.gitlab-ci.yml` that the cross-encoder check runs only in a specific job and the default job does not need the Hub—without nondeterministic failures when the chosen policy is satisfied.

## Boundaries & Constraints

**Always:** Every change stays automatable in CI or a documented tagged runner; NFR-7 must not assert 401 on routes that are intentionally public (none under `/rag` today—if that changes, document exceptions in the test module). R-18 must not break the default pipeline with random Hugging Face outages once the policy is applied.

**Ask First:** Whether NFR-6 runs on every MR (e.g. lightweight compose on shared runner) or only on `web` / `schedule` / self-hosted—pick one and document the recipe in README.

**Never:** Manual-only verification as the only proof; duplicating 401 cases in multiple hand-written test functions without a shared source after this work; leaving R-18’s merge-gate story ambiguous in README.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| NFR-6 happy path | Stack up; `docker compose restart` (or equivalent) on `support-rag`; Qdrant still up | After readiness, `GET /rag/health` with service bearer returns 200; optional: minimal `POST /rag/retrieve` succeeds | Fail with clear log if service does not become ready within timeout |
| NFR-6 isolation | N/A | Test documents service name `support-rag` from `docker-compose.yaml` | N/A |
| NFR-7 no bearer | For each protected method/path | HTTP **401** | N/A |
| NFR-7 wrong bearer | Invalid `Authorization` | **401** (existing behavior) | May stay as separate test or same matrix with variant |
| R-18 merge policy A | Hub/cache available | `test_r18_cross_encoder_instantiate_smoke` runs green in the job that defines merge policy | N/A |
| R-18 merge policy B | `TRANSFORMERS_OFFLINE=1` or stub | Test uses stub/double or is excluded from the gate with explicit doc | No uncached download required for the gate job |

</frozen-after-approval>

## Code Map

- `docker-compose.yaml` — service name **`support-rag`**, port 8080, env tokens; restart target for NFR-6.
- `support_rag/app.py` — `APIRouter` prefix `/rag`; `require_service` on health + retrieve; `require_admin` on index/delete; **single place** to reason about which routes require which dependency.
- `tests/unit/test_service_lifecycle_nfr6.py` — in-process lifecycle only; remains as fast unit signal; NFR-6 **adds** process-level coverage elsewhere.
- `tests/contract/test_auth_health.py`, `test_retrieve_http.py`, `test_admin_index_delete.py` — current 401 coverage; to be **consolidated or superseded** by NFR-7 parametrized test (avoid duplicate failure modes).
- `tests/unit/test_cross_encoder_r18_smoke.py` — R-18 slow smoke + skip conditions.
- `.gitlab-ci.yml` — `mvp1_script_help_golden` (default test); eval jobs tagged `rag-mvp1-eval`; **where** R-18 policy is enforced must be written down.

## Tasks & Acceptance

**Execution:**

- [x] `tests/` (new `tests/integration/` or documented script + pytest wrapper) -- Add **NFR-6** automation: after restart of API container/process, wait for health, run minimal smoke; wire into CI or README so the path is not manual-only.
- [x] `tests/contract/` + optionally `support_rag/app.py` -- **NFR-7:** One parametrized test (or introspection-based generator) for **all** protected routes: no `Authorization` → **401**; include **GET /rag/health**, **POST /rag/retrieve**, **POST/DELETE /rag/index/{namespace}**; remove or trim redundant 401 tests once the matrix is live.
- [x] `tests/unit/test_cross_encoder_r18_smoke.py` + `.gitlab-ci.yml` + `README.md` -- **R-18:** Implement **either** GitLab `cache` for the model directory used by `CrossEncoder`, **or** a deterministic stub/double for the merge gate, **or** an explicit statement that the cross-encoder test is not part of the default MR job and which job is authoritative—so the default merge pipeline is stable.
- [x] `_bmad-output/implementation-artifacts/mvp1-prd-to-automated-tests-gap-table.md` -- Set **NFR-6, NFR-7, R-18** rows to covered when the above are true in repo policy.

**Acceptance Criteria:**

- **Given** a compose stack with API and dependencies, **when** the **support-rag** (or equivalent) service restarts, **then** a documented smoke request still succeeds (**NFR-6**).
- **Given** no bearer token, **when** each protected **/rag/** route is called with valid shape/params, **then** the response status is **401** (**NFR-7**).
- **Given** the **documented** default merge (or gating) pipeline, **when** CI runs, **then** **R-18** is satisfied per README + `.gitlab-ci.yml` without nondeterministic Hub failures for that policy.

## Design Notes

- **NFR-7 introspection:** `app.router.routes` + dependency closure is fragile; prefer a small **explicit table** in `tests/contract/` (single module) that lists `(method, path pattern)` and fails CI if a new protected endpoint is not registered—optionally assert the table against `app.openapi()` or a one-time snapshot. If introspection is used, restrict to the `api` router’s routes under `/rag` and match `require_service` / `require_admin` via dependency objects.

## Verification

**Commands:**

- `python -m pytest tests/ -q` — expected: full suite green after changes (mind `slow` / integration markers if split).
- `python -m pytest tests/contract/ -q` — expected: NFR-7 matrix passes.
- Optional local: `docker compose up -d` then restart recipe from README.

**Manual checks:** Run the NFR-6 restart recipe once on a developer machine to confirm timeouts and service names.

## Spec Change Log

- **2026-04-25** — Draft from automation-first backlog; expanded to template with codebase investigation (contract tests, single CI test job, `docker-compose` service name).
- **2026-04-25** — (Review loop 0) Implemented NFR-6 integration test, NFR-7 `test_protected_routes_401.py` + contract trim, R-18 `not slow` in `mvp1_script_help_golden` + cache paths + gap table; no change to frozen intent.

## Suggested Review Order

**NFR-7**

- Canonical `(method, path)` table plus OpenAPI guard so new `/rag` routes cannot miss 401 coverage.
  [`test_protected_routes_401.py:40`](../../tests/contract/test_protected_routes_401.py#L40)

- Admin routes reject the service bearer alone (not only missing or wrong tokens).
  [`test_protected_routes_401.py:104`](../../tests/contract/test_protected_routes_401.py#L104)

**R-18**

- MR job: deliverable CLI tests plus `CrossEncoder` non-slow tests; cache dirs for HF / sentence-transformers.
  [`.gitlab-ci.yml:6`](../../.gitlab-ci.yml#L6)

- Docstring: merge gate vs optional `@pytest.mark.slow` Hub load.
  [`test_cross_encoder_r18_smoke.py:1`](../../tests/unit/test_cross_encoder_r18_smoke.py#L1)

**NFR-6**

- Compose `restart` on `support-rag`, poll `GET /rag/health` until 200 (double-gated: `RUN_INTEGRATION` + `RUN_NFR6_COMPOSE`).
  [`test_nfr6_compose_restart.py:56`](../../tests/integration/test_nfr6_compose_restart.py#L56)

**Test wiring**

- `nfr6_compose` double-gate with `RUN_INTEGRATION` and `RUN_NFR6_COMPOSE`.
  [`conftest.py:18`](../../tests/conftest.py#L18)

**Docs & coverage table**

- README: NFR-6/7/18 and `mvp1_script_help_golden` behavior.
  [`README.md:31`](../../README.md#L31)

- Gap table rows for NFR-6, NFR-7, R-18.
  [`mvp1-prd-to-automated-tests-gap-table.md:64`](./mvp1-prd-to-automated-tests-gap-table.md#L64)
