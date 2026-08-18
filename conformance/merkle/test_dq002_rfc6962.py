"""RI-PY conformance suite for DQ-002 (RFC 6962 Merkle hash domain).

Evidence discipline
-------------------
Expected values are read from the DQ-002 fixtures, which were produced by an
independent oracle (`ck003/dq-002-hash-domain/tools/rfc6962_oracle.sh`, GNU
coreutils SHA-256). The implementation under test never supplies its own
expected values. Every assertion drives the implementation forward from raw
payload bytes to a digest and compares against a frozen constant.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Dict, List

import pytest

from conformance.merkle import rfc6962

FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"
TWO_LEAF_PATH = FIXTURE_DIR / "FIX-CK003-DQ002-RFC6962-2LEAF.json"
EDGE_MATRIX_PATH = FIXTURE_DIR / "FIX-CK003-DQ002-RFC6962-EDGE-MATRIX.json"


def _load(path: pathlib.Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


TWO_LEAF = _load(TWO_LEAF_PATH)
EDGE_MATRIX = _load(EDGE_MATRIX_PATH)

EDGE_PAYLOADS: List[bytes] = [
    p.encode("utf-8") for p in EDGE_MATRIX["leaf_payloads_utf8"]
]


# --------------------------------------------------------------------------
# Fixture integrity — the suite must fail loudly if a fixture is swapped.
# --------------------------------------------------------------------------

FIXTURE_DIGESTS = {
    "FIX-CK003-DQ002-RFC6962-2LEAF.json":
        "bf21d2b8f3c947ebaf23bc7662f1ac8e590ef6c3a77850e27c84422967ce9aae",
    "FIX-CK003-DQ002-RFC6962-EDGE-MATRIX.json":
        "dfa5320cb06ba1a3eb88ad60424869e9722384b29f310ee9978390811f9f3eb8",
}


@pytest.mark.parametrize("name,expected", sorted(FIXTURE_DIGESTS.items()))
def test_fixture_file_digests_are_pinned(name: str, expected: str) -> None:
    actual = hashlib.sha256((FIXTURE_DIR / name).read_bytes()).hexdigest()
    assert actual == expected, f"{name} changed; refresh PROVENANCE.md deliberately"


# --------------------------------------------------------------------------
# A. leaf domain / B. node domain / C. raw digest handling
# --------------------------------------------------------------------------


def test_leaf_domain_prefix_is_0x00() -> None:
    assert rfc6962.LEAF_PREFIX == b"\x00"
    assert rfc6962.leaf_hash(b"a") == hashlib.sha256(b"\x00" + b"a").digest()


def test_node_domain_prefix_is_0x01() -> None:
    assert rfc6962.NODE_PREFIX == b"\x01"
    left = rfc6962.leaf_hash(b"a")
    right = rfc6962.leaf_hash(b"b")
    assert rfc6962.node_hash(left, right) == hashlib.sha256(
        b"\x01" + left + right
    ).digest()


def test_primitives_return_raw_32_byte_digests() -> None:
    assert isinstance(rfc6962.leaf_hash(b"a"), bytes)
    assert len(rfc6962.leaf_hash(b"a")) == 32
    assert len(rfc6962.node_hash(rfc6962.leaf_hash(b"a"), rfc6962.leaf_hash(b"b"))) == 32
    assert len(rfc6962.empty_root()) == 32


def test_node_hash_rejects_non_32_byte_children() -> None:
    good = rfc6962.leaf_hash(b"a")
    with pytest.raises(ValueError):
        rfc6962.node_hash(b"\x00" * 31, good)
    with pytest.raises(ValueError):
        rfc6962.node_hash(good, b"\x00" * 33)


# --------------------------------------------------------------------------
# D. hex representation handling — hex text must never reach a hash boundary
# --------------------------------------------------------------------------


def test_hex_text_is_rejected_at_the_node_boundary() -> None:
    left = rfc6962.leaf_hash(b"a")
    right = rfc6962.leaf_hash(b"b")
    with pytest.raises(TypeError):
        rfc6962.node_hash(left.hex(), right.hex())  # type: ignore[arg-type]
    # A 64-char hex string encoded to bytes is 64 bytes, not 32.
    with pytest.raises(ValueError):
        rfc6962.node_hash(left.hex().encode(), right.hex().encode())


def test_str_is_rejected_at_the_leaf_boundary() -> None:
    with pytest.raises(TypeError):
        rfc6962.leaf_hash("a")  # type: ignore[arg-type]


# --------------------------------------------------------------------------
# E. RFC 6962 split algorithm
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "n,k",
    [(2, 1), (3, 2), (4, 2), (5, 4), (6, 4), (7, 4), (8, 4), (9, 8), (17, 16)],
)
def test_largest_power_of_two_strictly_less_than_n(n: int, k: int) -> None:
    assert rfc6962._largest_power_of_two_lt(n) == k


def test_five_leaf_tree_is_left_heavy() -> None:
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:5]]
    expected = rfc6962.node_hash(rfc6962.merkle_root(leaves[:4]), leaves[4])
    assert rfc6962.merkle_root(leaves) == expected


# --------------------------------------------------------------------------
# F. odd-node handling — no duplication anywhere
# --------------------------------------------------------------------------


def test_odd_node_is_promoted_not_duplicated() -> None:
    """N=3 is the minimal case that exposes last-leaf duplication."""
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:3]]
    rfc6962_root = rfc6962.merkle_root(leaves)

    promoted = rfc6962.node_hash(rfc6962.node_hash(leaves[0], leaves[1]), leaves[2])
    duplicated = rfc6962.node_hash(
        rfc6962.node_hash(leaves[0], leaves[1]),
        rfc6962.node_hash(leaves[2], leaves[2]),
    )

    assert rfc6962_root == promoted
    assert rfc6962_root != duplicated


# --------------------------------------------------------------------------
# G/H/I/J/K/L. tree sizes, driven from the independent edge-matrix fixture
# --------------------------------------------------------------------------


def test_empty_tree_root_is_sha256_of_empty_input() -> None:
    assert rfc6962.merkle_root([]) == hashlib.sha256(b"").digest()
    assert rfc6962.merkle_root([]).hex() == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_single_leaf_root_equals_the_leaf_hash() -> None:
    leaf = rfc6962.leaf_hash(b"leaf-0")
    assert rfc6962.merkle_root([leaf]) == leaf


def test_two_leaf_root_matches_normative_two_leaf_fixture() -> None:
    expected = TWO_LEAF["expected"]
    leaf_a = rfc6962.leaf_hash(bytes.fromhex(TWO_LEAF["inputs"]["leaf_a_bytes_hex"]))
    leaf_b = rfc6962.leaf_hash(bytes.fromhex(TWO_LEAF["inputs"]["leaf_b_bytes_hex"]))

    assert leaf_a.hex() == expected["leaf_a_hash_hex"]
    assert leaf_b.hex() == expected["leaf_b_hash_hex"]
    assert rfc6962.merkle_root([leaf_a, leaf_b]).hex() == expected["root_hash_hex"]


def test_leaf_hashes_match_edge_matrix_fixture() -> None:
    for payload, expected_hex in zip(EDGE_PAYLOADS, EDGE_MATRIX["leaf_hashes_hex"]):
        assert rfc6962.leaf_hash(payload).hex() == expected_hex


@pytest.mark.parametrize("tree", EDGE_MATRIX["trees"], ids=lambda t: f"N{t['tree_size']}")
def test_root_matches_independent_oracle(tree: Dict) -> None:
    n = tree["tree_size"]
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    assert rfc6962.merkle_root(leaves).hex() == tree["root_hex"]


# --------------------------------------------------------------------------
# M/N. inclusion proof generation and verification
# --------------------------------------------------------------------------


@pytest.mark.parametrize("tree", EDGE_MATRIX["trees"], ids=lambda t: f"N{t['tree_size']}")
def test_audit_paths_match_independent_oracle(tree: Dict) -> None:
    n = tree["tree_size"]
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    for entry in tree["audit_paths"]:
        m = entry["leaf_index"]
        path = rfc6962.audit_path(m, leaves)
        assert [s.hex() for s in path] == entry["path_hex"], f"N={n} m={m}"


@pytest.mark.parametrize("tree", EDGE_MATRIX["trees"], ids=lambda t: f"N{t['tree_size']}")
def test_every_audit_path_reconstructs_the_root(tree: Dict) -> None:
    n = tree["tree_size"]
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = rfc6962.merkle_root(leaves)
    for m in range(n):
        path = rfc6962.audit_path(m, leaves)
        assert rfc6962.verify_audit_path(leaves[m], m, n, path, root), f"N={n} m={m}"


def test_single_leaf_proof_is_empty_and_verifies() -> None:
    leaf = rfc6962.leaf_hash(b"leaf-0")
    assert rfc6962.audit_path(0, [leaf]) == []
    assert rfc6962.verify_audit_path(leaf, 0, 1, [], leaf)


def test_audit_path_index_out_of_range_raises() -> None:
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:3]]
    with pytest.raises(IndexError):
        rfc6962.audit_path(3, leaves)
    with pytest.raises(IndexError):
        rfc6962.audit_path(-1, leaves)


# --------------------------------------------------------------------------
# NEGATIVE CONTROLS (Phase 6)
#
# These reimplement the *forbidden* constructions locally, purely to prove
# that the conformant implementation does not silently agree with them.
# None of this leaks into rfc6962.py.
# --------------------------------------------------------------------------


def _undomained_leaf(data: bytes) -> bytes:
    """FORBIDDEN: leaf without the 0x00 prefix."""
    return hashlib.sha256(data).digest()


def _undomained_node(left: bytes, right: bytes) -> bytes:
    """FORBIDDEN: node without the 0x01 prefix."""
    return hashlib.sha256(left + right).digest()


def _hex_text_node(left: bytes, right: bytes) -> bytes:
    """FORBIDDEN: hashing hex(left) + hex(right) as UTF-8 text (legacy RI-PY)."""
    return hashlib.sha256((left.hex() + right.hex()).encode("utf-8")).digest()


def _duplicating_root(leaves: List[bytes]) -> bytes:
    """FORBIDDEN: Bitcoin-style duplication of the last node on odd levels."""
    if not leaves:
        return hashlib.sha256(b"").digest()
    level = list(leaves)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(rfc6962.node_hash(left, right))
        level = nxt
    return level[0]


# NC-1
def test_nc1_leaf_without_domain_prefix_differs() -> None:
    assert rfc6962.leaf_hash(b"a") != _undomained_leaf(b"a")


# NC-2
def test_nc2_node_without_domain_prefix_differs() -> None:
    left, right = rfc6962.leaf_hash(b"a"), rfc6962.leaf_hash(b"b")
    assert rfc6962.node_hash(left, right) != _undomained_node(left, right)


# NC-3
def test_nc3_hex_text_node_differs_from_raw_byte_node() -> None:
    left, right = rfc6962.leaf_hash(b"a"), rfc6962.leaf_hash(b"b")
    normative = rfc6962.node_hash(left, right)
    assert normative != _hex_text_node(left, right)
    assert normative.hex() == TWO_LEAF["expected"]["root_hash_hex"]


# NC-4
@pytest.mark.parametrize("n", [3, 5, 6, 7])
def test_nc4_odd_node_duplication_differs(n: int) -> None:
    """Duplication and promotion must disagree for every odd-shaped tree."""
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    assert rfc6962.merkle_root(leaves) != _duplicating_root(leaves)


@pytest.mark.parametrize("n", [1, 2, 4, 8])
def test_nc4b_duplication_coincides_only_on_powers_of_two(n: int) -> None:
    """Control on the control: powers of two legitimately agree, so a passing
    NC-4 at n in {3,5,6,7} is a real discriminator, not an artefact."""
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    assert rfc6962.merkle_root(leaves) == _duplicating_root(leaves)


# NC-5
@pytest.mark.parametrize("n", [2, 3, 4, 5, 7, 8])
def test_nc5_altered_leaf_is_rejected(n: int) -> None:
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = rfc6962.merkle_root(leaves)
    tampered = rfc6962.leaf_hash(b"tampered")
    for m in range(n):
        path = rfc6962.audit_path(m, leaves)
        assert not rfc6962.verify_audit_path(tampered, m, n, path, root)


# NC-6
@pytest.mark.parametrize("n", [2, 3, 4, 5, 7, 8])
def test_nc6_altered_sibling_is_rejected(n: int) -> None:
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = rfc6962.merkle_root(leaves)
    for m in range(n):
        path = rfc6962.audit_path(m, leaves)
        for i in range(len(path)):
            bad = list(path)
            flipped = bytearray(bad[i])
            flipped[0] ^= 0xFF
            bad[i] = bytes(flipped)
            assert not rfc6962.verify_audit_path(leaves[m], m, n, bad, root)


# NC-7
@pytest.mark.parametrize("n", [2, 3, 5, 8])
def test_nc7_altered_root_is_rejected(n: int) -> None:
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = bytearray(rfc6962.merkle_root(leaves))
    root[31] ^= 0x01
    for m in range(n):
        path = rfc6962.audit_path(m, leaves)
        assert not rfc6962.verify_audit_path(leaves[m], m, n, path, bytes(root))


# NC-8
def test_nc8_malformed_and_incorrect_proofs_are_rejected() -> None:
    n = 7
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = rfc6962.merkle_root(leaves)
    path = rfc6962.audit_path(2, leaves)

    # too short
    assert not rfc6962.verify_audit_path(leaves[2], 2, n, path[:-1], root)
    # too long
    assert not rfc6962.verify_audit_path(leaves[2], 2, n, path + [path[0]], root)
    # reordered
    assert not rfc6962.verify_audit_path(leaves[2], 2, n, list(reversed(path)), root)
    # empty
    assert not rfc6962.verify_audit_path(leaves[2], 2, n, [], root)
    # malformed digest lengths — must return False, not raise
    assert not rfc6962.verify_audit_path(leaves[2], 2, n, [b"\x00" * 31] * len(path), root)
    assert not rfc6962.verify_audit_path(b"\x00" * 31, 2, n, path, root)
    assert not rfc6962.verify_audit_path(leaves[2], 2, n, path, b"\x00" * 16)
    # hex-text proof material — must return False, not raise
    assert not rfc6962.verify_audit_path(
        leaves[2], 2, n, [s.hex() for s in path], root  # type: ignore[arg-type]
    )
    # another leaf's valid proof presented for this index
    other = rfc6962.audit_path(5, leaves)
    assert not rfc6962.verify_audit_path(leaves[2], 2, n, other, root)


# NC-9
#
# FINDING F-2 (recorded, not silently accommodated): an RFC 6962 audit path
# does NOT uniquely bind the tree size. Verification decisions are driven by
# the bit pattern of (leaf_index, tree_size - 1); several tree sizes can
# require the identical path shape, so a claimed size within that class
# verifies against the true root. This is a property of RFC 6962 itself, not
# of either implementation: RI-PY and RI-RS accept the *same* size set. Tree
# size is bound by a signed tree head / consistency proof, not by an audit
# path. DQ-002 does not currently state this; see the CROSS-LANGUAGE-002
# report. The test pins the shared behaviour so any future divergence fails.
_RI_RS_VECTORS = json.loads(
    (pathlib.Path(__file__).resolve().parent / "evidence" / "RI-RS-VECTORS.json")
    .read_text(encoding="utf-8")
)

# Expectations are taken from the RI-RS emission, never from RI-PY's own
# output, so this pin is a cross-implementation assertion rather than a
# tautology.
_RS_ACCEPTED_SIZES = sorted(
    ((tree["tree_size"], case["leaf_index"]), case["accepted_tree_sizes"])
    for tree in _RI_RS_VECTORS["verification_matrix"]
    for case in tree["cases"]
)


@pytest.mark.parametrize("key,expected", _RS_ACCEPTED_SIZES, ids=lambda x: str(x))
def test_nc9_tree_size_acceptance_set_matches_ri_rs(key, expected) -> None:
    n, m = key
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = rfc6962.merkle_root(leaves)
    path = rfc6962.audit_path(m, leaves)
    accepted = [
        s for s in range(0, 10) if rfc6962.verify_audit_path(leaves[m], m, s, path, root)
    ]
    assert accepted == expected
    assert n in accepted, "true tree size must always be accepted"


def test_nc9b_structurally_invalid_tree_sizes_are_rejected() -> None:
    """Sizes that change the required path shape must be rejected outright."""
    n = 5
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = rfc6962.merkle_root(leaves)
    path = rfc6962.audit_path(1, leaves)
    for wrong_size in (0, 1, 2, 3, 4, 9, -1):
        assert not rfc6962.verify_audit_path(leaves[1], 1, wrong_size, path, root), (
            f"tree_size={wrong_size} accepted"
        )
    assert rfc6962.verify_audit_path(leaves[1], 1, n, path, root)


def test_nc9c_index_beyond_tree_size_is_always_rejected() -> None:
    for n in (1, 2, 3, 5, 7, 8):
        leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
        root = rfc6962.merkle_root(leaves)
        for m in range(n):
            path = rfc6962.audit_path(m, leaves)
            assert not rfc6962.verify_audit_path(leaves[m], n, n, path, root)
            assert not rfc6962.verify_audit_path(leaves[m], m, 0, path, root)


# NC-10
def test_nc10_incorrect_leaf_index_is_rejected() -> None:
    n = 7
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:n]]
    root = rfc6962.merkle_root(leaves)
    for m in range(n):
        path = rfc6962.audit_path(m, leaves)
        for wrong in range(n):
            if wrong == m:
                continue
            assert not rfc6962.verify_audit_path(leaves[m], wrong, n, path, root), (
                f"proof for {m} accepted at index {wrong}"
            )
        # out of range
        assert not rfc6962.verify_audit_path(leaves[m], n, n, path, root)
        assert not rfc6962.verify_audit_path(leaves[m], -1, n, path, root)


# --------------------------------------------------------------------------
# Legacy contrast — documents, and pins, the divergence DQ-002 exists to close.
# --------------------------------------------------------------------------


def test_legacy_audit_merkle_root_differs_from_dq002_root() -> None:
    """`audit/merkle.py` is a different algorithm identity and MUST NOT be
    reinterpreted as RFC 6962 evidence (ADR migration rule)."""
    from audit.merkle import MerkleTree

    legacy_root_hex = MerkleTree(["a", "b"]).get_root()
    dq002_root_hex = rfc6962.merkle_root(
        [rfc6962.leaf_hash(b"a"), rfc6962.leaf_hash(b"b")]
    ).hex()

    assert legacy_root_hex != dq002_root_hex
    assert dq002_root_hex == TWO_LEAF["expected"]["root_hash_hex"]


# --------------------------------------------------------------------------
# Determinism / purity
# --------------------------------------------------------------------------


def test_repeated_computation_is_bit_identical() -> None:
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS]
    first = (rfc6962.merkle_root(leaves), [rfc6962.audit_path(i, leaves) for i in range(8)])
    for _ in range(5):
        assert (
            rfc6962.merkle_root(leaves),
            [rfc6962.audit_path(i, leaves) for i in range(8)],
        ) == first


def test_input_sequence_is_not_mutated() -> None:
    leaves = [rfc6962.leaf_hash(p) for p in EDGE_PAYLOADS[:5]]
    snapshot = list(leaves)
    rfc6962.merkle_root(leaves)
    rfc6962.audit_path(3, leaves)
    assert leaves == snapshot


def test_module_imports_no_json_or_network() -> None:
    source = pathlib.Path(rfc6962.__file__).read_text(encoding="utf-8")
    body = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    for forbidden in ("import json", "import socket", "import requests", "urllib"):
        assert forbidden not in body, f"{forbidden} present in Merkle primitive"
