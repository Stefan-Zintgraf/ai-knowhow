"""Kerio Connect Client API (JSON-RPC) helpers."""

from kerio_mail.client import KerioClient, KerioRpcError
from kerio_mail.mail import find_drafts_folder_id, iter_mails_pages

__all__ = [
    "KerioClient",
    "KerioRpcError",
    "find_drafts_folder_id",
    "iter_mails_pages",
    "__version__",
]
__version__ = "0.1.0"
