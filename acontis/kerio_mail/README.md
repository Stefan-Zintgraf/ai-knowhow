# kerio-mail-read

Python helpers and CLIs for Kerio Connect mailboxes via the **Client JSON-RPC API** (`/webmail/api/jsonrpc/`): list mail, create drafts, export attachments. Copy `.env.example` to `.env`, set `KERIO_BASE_URL`, `KERIO_USERNAME`, and `KERIO_PASSWORD`, then run `read-mailbox --help`, `create-draft --help`, or `export-attachments --help`.

**Tests:** from this directory, `pip install -e ".[dev]"` then `pytest` — unit tests use mocks; integration tests run only when `KERIO_INTEGRATION=1` and credentials are set (see `.env.example`).
