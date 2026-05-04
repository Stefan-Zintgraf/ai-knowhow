import uuid

from support_rag.chunk_id import stable_chunk_id


def test_stable_chunk_id_deterministic():
    a = stable_chunk_id("kb", "p1", 0, "kb-v1")
    b = stable_chunk_id("kb", "p1", 0, "kb-v1")
    assert a == b
    uuid.UUID(a)  # must be a valid UUID


def test_different_index_changes_id():
    a = stable_chunk_id("kb", "p1", 0, "kb-v1")
    c = stable_chunk_id("kb", "p1", 1, "kb-v1")
    assert a != c
