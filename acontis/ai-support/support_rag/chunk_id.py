import hashlib
import uuid


def stable_chunk_id(namespace: str, parent_id: str, chunk_index: int, chunker_version: str) -> str:
    """Deterministic UUID derived from SHA-256 (R-10 / PRD 2.7).

    Qdrant requires point IDs to be unsigned integers or UUIDs.
    """
    s = f"{namespace}|{parent_id}|{chunk_index}|{chunker_version}"
    return str(uuid.UUID(hashlib.sha256(s.encode("utf-8")).hexdigest()[:32]))
