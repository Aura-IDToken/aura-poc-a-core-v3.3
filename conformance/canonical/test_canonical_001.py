from __future__ import annotations

import hashlib

from conformance.canonical.jcs import canonical_bytes

OBJECT = {
    "event_type": "AUDIT_RECORD",
    "protocol_version": "1.0",
    "schema_version": "1.0",
    "payload": {"value": 42},
}

EXPECTED_BYTES_HEX = (
    "7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f6164223a7b"
    "2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e30222c2273"
    "6368656d615f76657273696f6e223a22312e30227d"
)
EXPECTED_CANONICAL_SHA256 = "b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6"
EXPECTED_LEAF_SHA256 = "ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039"


def test_canonical_001_jcs_bytes_and_hashes() -> None:
    data = canonical_bytes(OBJECT)
    assert data.hex() == EXPECTED_BYTES_HEX
    assert hashlib.sha256(data).hexdigest() == EXPECTED_CANONICAL_SHA256
    assert hashlib.sha256(b"\x00" + data).hexdigest() == EXPECTED_LEAF_SHA256
