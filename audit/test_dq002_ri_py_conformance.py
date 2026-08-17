"""CK-003 DQ-002 RI-PY conformance gate.

These tests intentionally target the CURRENT audit/merkle.py implementation.
They are expected to fail until RI-PY adopts the approved RI-RS hash domain:

    leaf = SHA-256(0x00 || canonical_bytes)
    node = SHA-256(0x01 || left_raw_32 || right_raw_32)

This file is a conformance gate, not a remediation. Do not weaken the
expected values to make the current implementation pass.
"""

import hashlib
import json
from pathlib import Path

from audit import merkle


FIXTURE = Path(__file__).parent / "fixtures" / "ck003_dq002_001.json"


def _load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_ri_py_leaf_matches_dq002_fixture():
    """RI-PY leaf hashing must use raw bytes with the 0x00 domain byte."""
    fixture = _load_fixture()
    canonical = bytes.fromhex(fixture["canonical_bytes_utf8_hex"])
    expected = fixture["leaf_digest_hex"]

    # Current RI-PY public primitive is string-based and has no domain byte.
    # Calling it here exposes non-conformance without modifying production code.
    actual = merkle.sha256(canonical.decode("utf-8"))

    assert actual == expected, (
        "RI-PY leaf hash is non-conformant: expected "
        f"SHA-256(0x00 || canonical_bytes)={expected}, got {actual}."
    )


def test_ri_py_node_matches_dq002_fixture():
    """RI-PY node hashing must use raw 32-byte child digests plus 0x01."""
    fixture = _load_fixture()
    left = fixture["node_left_hex"]
    right = fixture["node_right_hex"]
    expected = fixture["node_digest_hex"]

    # Exercise the current MerkleTree node path with already-hashed leaves.
    tree = merkle.MerkleTree([left, right], leaves_are_hashed=True)
    actual = tree.get_root()

    assert actual == expected, (
        "RI-PY node hash is non-conformant: expected "
        f"SHA-256(0x01 || left_raw || right_raw)={expected}, got {actual}."
    )


def test_fixture_values_are_independently_reproducible():
    """Guard the fixture itself against accidental transcription errors."""
    fixture = _load_fixture()

    leaf_input = bytes.fromhex(fixture["leaf_input_hex"])
    node_input = bytes.fromhex(fixture["node_input_hex"])

    assert hashlib.sha256(leaf_input).hexdigest() == fixture["leaf_digest_hex"]
    assert hashlib.sha256(node_input).hexdigest() == fixture["node_digest_hex"]

    assert leaf_input[0] == 0x00
    assert node_input[0] == 0x01
    assert len(node_input) == 65
    assert len(bytes.fromhex(fixture["node_left_hex"])) == 32
    assert len(bytes.fromhex(fixture["node_right_hex"])) == 32
