"""Kerio Connect Client API — JSON-RPC over HTTPS."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional, Sequence
from urllib.parse import urljoin

import requests


class KerioRpcError(Exception):
    """JSON-RPC `error` object returned by Kerio (HTTP 200 with error payload)."""

    def __init__(self, error: Mapping[str, Any]) -> None:
        self.error = dict(error)
        code = self.error.get("code")
        message = self.error.get("message", "")
        super().__init__(f"Kerio JSON-RPC error {code}: {message}")


class KerioClient:
    """JSON-RPC client for `/webmail/api/jsonrpc/` with session cookies and X-Token."""

    def __init__(self, base_url: str, *, verify_ssl: bool = True) -> None:
        origin = base_url.rstrip("/")
        self._base_url = origin
        self._rpc_url = f"{origin}/webmail/api/jsonrpc/"
        self._session = requests.Session()
        self._session.verify = verify_ssl
        self._next_id = 1
        self._token: Optional[str] = None

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def rpc_url(self) -> str:
        return self._rpc_url

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def token(self) -> Optional[str]:
        return self._token

    def call(self, method: str, params: Optional[Mapping[str, Any]] = None) -> Any:
        req_id = self._next_id
        self._next_id += 1
        body: dict[str, Any] = {
            "jsonrpc": "2.0",
            "method": method,
            "params": dict(params) if params is not None else {},
            "id": req_id,
        }
        headers: MutableMapping[str, str] = self._session.headers
        headers["Content-Type"] = "application/json"
        if self._token:
            headers["X-Token"] = self._token

        r = self._session.post(self._rpc_url, json=body)
        r.raise_for_status()
        data = r.json()
        if data.get("error") is not None:
            raise KerioRpcError(data["error"])
        return data.get("result")

    def login(
        self,
        username: str,
        password: str,
        *,
        application: Mapping[str, str],
    ) -> str:
        """Call `Session.login`, store token, and set `X-Token` for subsequent RPCs."""
        self._token = None
        self._session.headers.pop("X-Token", None)

        result = self.call(
            "Session.login",
            {
                "userName": username,
                "password": password,
                "application": dict(application),
            },
        )
        if not isinstance(result, dict) or "token" not in result:
            raise KerioRpcError(
                {"code": -1, "message": "Session.login missing token in result"},
            )
        token = str(result["token"])
        self._token = token
        self._session.headers["X-Token"] = token
        return token

    def folders_get(self) -> Any:
        """Call ``Folders.get`` — folder tree for the logged-in user (requires login)."""
        return self.call("Folders.get", {})

    def mails_get(
        self,
        folder_ids: Sequence[Any],
        query: Mapping[str, Any],
    ) -> Any:
        """
        Call ``Mails.get`` with ``folderIds`` and ``SearchQuery`` (``start``, ``limit``, etc.).
        """
        return self.call(
            "Mails.get",
            {
                "folderIds": list(folder_ids),
                "query": dict(query),
            },
        )

    def mails_get_by_id(self, ids: Sequence[Any]) -> Any:
        """Call ``Mails.getById`` — full ``Mail`` structs (requires login)."""
        return self.call("Mails.getById", {"ids": list(ids)})

    def mails_create(self, mails: Sequence[Mapping[str, Any]]) -> Any:
        """Call ``Mails.create`` — save mail(s) (e.g. draft in Drafts folder). Requires login."""
        return self.call("Mails.create", {"mails": [dict(m) for m in mails]})

    def mails_export_attachments(self, attachment_ids: Sequence[Any]) -> Any:
        """
        Call ``Mails.exportAttachments`` — zip of attachments (all ids must be from one mail).

        Requires login. Result includes ``fileDownload`` (``Download``: ``url``, ``name``, ``length``).
        """
        return self.call(
            "Mails.exportAttachments",
            {"attachmentIds": list(attachment_ids)},
        )

    def download_get(self, url: str) -> bytes:
        """
        HTTP GET for a ``Download.url`` from ``Mails.exportAttachments`` using the same session
        (cookies + ``X-Token``). Relative paths are resolved against ``base_url``.
        """
        full = self._resolve_download_url(url)
        r = self._session.get(full)
        r.raise_for_status()
        return r.content

    def _resolve_download_url(self, url: str) -> str:
        u = url.strip()
        if u.startswith(("http://", "https://")):
            return u
        return urljoin(self._base_url + "/", u.lstrip("/"))
