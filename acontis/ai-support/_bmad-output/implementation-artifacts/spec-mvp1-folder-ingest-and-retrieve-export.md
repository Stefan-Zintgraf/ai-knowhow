---
title: "MVP1: folder ingest and retrieve-to-file (CLI)"
type: "feature"
created: "2026-04-25"
status: "done"
baseline_commit: "421242b8c4f431e5de680e1839f5d8ee013af839"
context:
  - "_bmad-output/implementation-artifacts/support_rag_mvp1_prd.md"
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Operators and testers need to load a corpus from local files into the RAG service without hand-building JSON, and to capture retrieval output in a file for diffing, CI fixtures, and manual review.

**Approach:** Add two small CLI entrypoints (same `scripts/` + env conventions as `seed_kb.py` / `reindex.py`) that call the existing `POST /rag/index/{namespace}` and `POST /rag/retrieve` APIs: one walks a directory and POSTs one document per eligible file; the other runs a test query and writes the `RetrievalResponse` JSON to a path. No in-process embedding of server-side filesystem paths into the API for MVP1 (client-side path resolution only).

## Boundaries & Constraints

**Always:** Use `RAG_MCP_BASE_URL` (or equivalent documented base URL), `RAG_ADMIN_TOKEN` for index, and `RAG_SERVICE_TOKEN` for retrieve, matching existing scripts. `namespace` must be `kb` or `tickets` (per `support_rag/app.py`). Document IDs must be stable, unique under the target namespace, and safe for the vector store; metadata must follow existing patterns (`source_uri` or `file_path` as string, optional `product`/`lang` if supplied via flags). Text files are read as UTF-8; invalid UTF-8 is skipped with a non-zero log line to stderr. Resolve paths to absolute, canonical form before walking; do not follow symlinks for directory walk (skip symlink entries) to reduce path surprises.

**Ask First:** If a future need arises for `multipart` or server-side "upload this folder" on the API, that is a separate spec (not in this work). Expanding file-type support beyond the agreed set (e.g. PDF) requires new dependencies or parsers — **HALT and ask** before adding heavy deps.

**Never:** Add provider SDKs to scripts (PRD R-17). Do not add new RAG API routes or MCP tools in this spec unless a blocker appears; the deliverable is **CLI** using existing JSON APIs.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|----------------------------|----------------|
| Happy ingest | Folder with `.md` and `.txt` | Single batch or chunked POSTs to index with one `id` per file (e.g. POSIX relative path under root) | N/A |
| Empty folder | No matching files | Exit 0 with message "0 files" (or similar); no index call | N/A |
| Binary / bad UTF-8 | Non-text or decode error | Skip file; count skipped; continue | Exit 1 if **all** files skipped, else 0 with summary |
| Path escape | `..` or path outside root after resolve | Reject with clear error; no partial index | Non-zero exit |
| Happy retrieve | Valid query + outfile path | Write pretty-printed or compact JSON of `RetrievalResponse` to file | N/A |
| Retrieve failure | 4xx/5xx from API | No output file; print body snippet; non-zero exit | Non-zero exit |

## Code Map

- `scripts/seed_kb.py` — pattern for `httpx` + `RAG_ADMIN_TOKEN` + `POST /rag/index/...`
- `scripts/reindex.py` — batching JSONL → index
- `support_rag/app.py` — `POST /rag/index/{namespace}`, `POST /rag/retrieve`
- `support_rag/schemas.py` — `IndexRequest`, `RetrievalRequest`, `RetrievalResponse` shapes
- `tests/contract/test_admin_index_delete.py` — index contract tests (existing)

## Tasks & Acceptance

**Execution:**

- [x] `scripts/ingest_folder.py` -- CLI: `--root` (folder), `--namespace` (`kb`|`tickets`), optional `--include` glob(s) or default `*.md`/`*.txt`/`*.rst` only, optional `--batch-size` to split large corpora, optional `--dry-run` listing planned ids without POST -- mirrors operational need without manual JSON
- [x] `scripts/retrieve_to_file.py` -- CLI: `--query` (or stdin), `--out` path, optional `--top-k`, `--namespace`/`--filters` JSON string aligned with `RetrievalRequest` -- captures retrieval for testing
- [x] `tests/scripts/test_ingest_folder.py` (or `tests/unit/test_ingest_folder_cli.py`) -- unit test: id generation from path, skip rules, error on escape (no real HTTP) -- locks behavior
- [x] `tests/scripts/test_retrieve_to_file.py` -- mock `httpx` or test client: successful write, HTTP error path
- [x] `README.md` (repo root) -- short subsections: "Ingest a folder" and "Export retrieve results" with copy-pastable env vars and examples

**Acceptance Criteria:**

- Given a directory with at least one UTF-8 `.md` or `.txt` file and valid `RAG_ADMIN_TOKEN`, when `ingest_folder.py` is run with that directory and `kb`, then `POST /rag/index/kb` succeeds and subsequent `retrieve` with a related query returns chunks whose metadata or text reflects ingested content.
- Given a running RAG service and `RAG_SERVICE_TOKEN`, when `retrieve_to_file.py` is run with a query and output path, then the output file contains valid JSON matching the `RetrievalResponse` contract (at minimum `chunks` list structure).
- Given a path with only broken/skipped files, when ingest runs, then the script exits with failure code and does not claim success.
- Given the frozen intent above, when a reviewer runs `pytest` on the new tests, then they pass without `RUN_INTEGRATION=1` (offline/mocked).

## Spec Change Log

## Design Notes

- Default `id` for each file: path relative to `--root` with forward slashes (e.g. `docs/notes/intro.md`), collision-checked within the run. If a path segment is too long for downstream limits, use a hash suffix — document the rule in the script help text.
- Cap single-request payload size: if the batch is large, split `docs` per `--batch-size` (default 32 or 50) like operational safety.

## Verification

**Commands:**

- `py -3.12 -m pytest tests/scripts/ -q` (or the chosen test paths) -- expected: all new tests pass
- `ruff check scripts/ingest_folder.py scripts/retrieve_to_file.py` (or project linter) -- expected: clean

**Manual checks (if no CLI):**

- After implementation, one manual run: ingest two small files, then `retrieve_to_file` and inspect JSON for expected chunk text.

## Suggested Review Order

- CLI entry, env tokens, and batched index `POST` with HTTP and network failure handling
  [`ingest_folder.py:139`](../../scripts/ingest_folder.py#L139)

- Walk rules: skip symlinks, glob filter, UTF-8 errors, long-path `id` hashing, and duplicate detection
  [`ingest_folder.py:43`](../../scripts/ingest_folder.py#L43)

- Request body for retrieve plus flags mapping to `RetrievalRequest` fields
  [`retrieve_to_file.py:18`](../../scripts/retrieve_to_file.py#L18)

- HTTP call, error paths, and JSON write for offline fixtures
  [`retrieve_to_file.py:45`](../../scripts/retrieve_to_file.py#L45)

- Unit tests: path and `id` rules plus ingest `main` exit when every file is skipped
  [`test_ingest_folder.py:70`](../../tests/scripts/test_ingest_folder.py#L70)

- Mocked `httpx` success and failure for retrieve CLI
  [`test_retrieve_to_file.py:60`](../../tests/scripts/test_retrieve_to_file.py#L60)

- Operator-facing copy-paste for both CLIs
  [`README.md:31`](../../README.md#L31)

</frozen-after-approval>
