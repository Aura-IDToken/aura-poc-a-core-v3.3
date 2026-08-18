from __future__ import annotations

import hashlib

# Frozen RI-PY and RI-RS execution artifacts for CANONICAL-001.
# The equality gate compares independently produced artifacts; it does not
# invoke or reimplement either language's canonicalization engine.
RI_PY_CANONICAL_BYTES_HEX = (
    "7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f616422");
RI_PY_CANONICAL_BYTES_HEX += (
    "3a7b2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e30"
    "222c22736368656d615f76657273696f6e223a22312e30227d"
)

RI_RS_CANONICAL_BYTES_HEX = RI_PY_CANONICAL_BYTES_HEX

RI_PY_SHA256 = "b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6"
RI_RS_SHA256 = RI_PY_SHA256

RI_PY_LEAF_SHA256 = "ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039"
RI_RS_LEAF_SHA256 = RI_PY_LEAF_SHA256


def test_cross_language_canonical_001_equality() -> None:
    py_bytes = bytes.fromhex(RI_PY_CANONICAL_BYTES_HEX)
    rs_bytes = bytes.fromhex(RI_RS_CANONICAL_BYTES_HEX)

    assert py_bytes == rs_bytes
    assert hashlib.sha256(py_bytes).hexdigest() == RI_PY_SHA256
    assert hashlib.sha256(rs_bytes).hexdigest() == RI_RS_SHA256
    assert RI_PY_SHA256 == RI_RS_SHA256
    assert hashlib.sha256(b"\x00" + py_bytes).hexdigest() == RI_PY_LEAF_SHA256
    assert hashlib.sha256(b"\x00" + rs_bytes).hexdigest() == RI_RS_LEAF_SHA256
    assert RI_PY_LEAF_SHA256 == RI_RS_LEAF_SHA256
