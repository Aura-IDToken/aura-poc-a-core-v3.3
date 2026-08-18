"""RI-PY implementation of the DQ-002 normative Merkle contract (RFC 6962).

Normative source
----------------
`aura-specification/ck003/dq-002-hash-domain/ADR-CK003-DQ002-HASH-DOMAIN.md`

    leaf  : SHA-256(0x00 || leaf_data_bytes)
    node  : SHA-256(0x01 || left_hash_bytes || right_hash_bytes)
    empty : SHA-256("")
    shape : RFC 6962 recursive split at the largest power of two strictly
            less than n. A single unpaired node is promoted unchanged;
            the last node is NEVER duplicated.

Byte discipline
---------------
Every value crossing a hash boundary is `bytes`. Digests are raw 32-byte
values. Hexadecimal text is a presentation form only and is never hashed.
The module refuses `str` inputs rather than silently encoding them.

Scope discipline
----------------
Canonical serialization is governed separately (DQ-006 / RFC 8785) and is
deliberately outside this module: the primitives accept opaque `bytes`. There
is no JSON handling, no floating-point arithmetic, no global mutable state, no
nondeterministic ordering, and no network access.
"""

from __future__ import annotations

import hashlib
from typing import List, Sequence

__all__ = [
    "LEAF_PREFIX",
    "NODE_PREFIX",
    "DIGEST_SIZE",
    "leaf_hash",
    "node_hash",
    "empty_root",
    "merkle_root",
    "audit_path",
    "verify_audit_path",
]

LEAF_PREFIX = b"\x00"
NODE_PREFIX = b"\x01"
DIGEST_SIZE = 32


def _require_bytes(name: str, value: object) -> bytes:
    """Reject anything that is not a byte string.

    `str` is rejected explicitly: implicit UTF-8 encoding at a hash boundary is
    exactly the representation ambiguity DQ-002 exists to eliminate.
    """
    if isinstance(value, str):
        raise TypeError(
            f"{name} must be bytes, not str; encode explicitly at the "
            f"canonical-serialization boundary"
        )
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes, got {type(value).__name__}")
    return bytes(value)


def _require_digest(name: str, value: object) -> bytes:
    raw = _require_bytes(name, value)
    if len(raw) != DIGEST_SIZE:
        raise ValueError(
            f"{name} must be a raw {DIGEST_SIZE}-byte digest, got {len(raw)} bytes"
        )
    return raw


def leaf_hash(data: bytes) -> bytes:
    """SHA-256(0x00 || data) -> raw 32 bytes."""
    return hashlib.sha256(LEAF_PREFIX + _require_bytes("data", data)).digest()


def node_hash(left: bytes, right: bytes) -> bytes:
    """SHA-256(0x01 || left || right) -> raw 32 bytes.

    Both children MUST be raw 32-byte digests.
    """
    return hashlib.sha256(
        NODE_PREFIX + _require_digest("left", left) + _require_digest("right", right)
    ).digest()


def empty_root() -> bytes:
    """RFC 6962 §2.1: MTH({}) = SHA-256("")."""
    return hashlib.sha256(b"").digest()


def _largest_power_of_two_lt(n: int) -> int:
    """Largest power of two strictly less than n (n >= 2)."""
    if n < 2:
        raise ValueError("n must be >= 2")
    k = 1
    while k < n:
        k <<= 1
    return k >> 1


def _check_leaves(leaves: Sequence[bytes]) -> List[bytes]:
    return [_require_digest(f"leaves[{i}]", h) for i, h in enumerate(leaves)]


def merkle_root(leaves: Sequence[bytes]) -> bytes:
    """Merkle Tree Hash over a sequence of *leaf hashes*.

    The input is the already-prefixed leaf hashes (see `leaf_hash`), not raw
    payloads. Ordering is caller-supplied and preserved exactly.
    """
    return _merkle_root(_check_leaves(leaves))


def _merkle_root(leaves: List[bytes]) -> bytes:
    n = len(leaves)
    if n == 0:
        return empty_root()
    if n == 1:
        return leaves[0]
    k = _largest_power_of_two_lt(n)
    return node_hash(_merkle_root(leaves[:k]), _merkle_root(leaves[k:]))


def audit_path(index: int, leaves: Sequence[bytes]) -> List[bytes]:
    """RFC 6962 audit path (inclusion proof) for `index`, leaf level upward.

    Returns an empty list for a single-leaf tree.
    """
    checked = _check_leaves(leaves)
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("index must be int")
    if index < 0 or index >= len(checked):
        raise IndexError(f"leaf index {index} out of range for tree size {len(checked)}")
    out: List[bytes] = []
    _audit_path(index, checked, out)
    return out


def _audit_path(index: int, leaves: List[bytes], out: List[bytes]) -> None:
    n = len(leaves)
    if n <= 1:
        return
    k = _largest_power_of_two_lt(n)
    if index < k:
        _audit_path(index, leaves[:k], out)
        out.append(_merkle_root(leaves[k:]))
    else:
        _audit_path(index - k, leaves[k:], out)
        out.append(_merkle_root(leaves[:k]))


def verify_audit_path(
    leaf: bytes,
    leaf_index: int,
    tree_size: int,
    path: Sequence[bytes],
    expected_root: bytes,
) -> bool:
    """Verify an RFC 6962 inclusion proof.

    This is the RFC 6962 §2.1.1 verification recurrence expressed over
    (leaf_index, tree_size - 1), deliberately independent of the tree-building
    recursion above so that a construction bug cannot verify itself.

    Returns False — never raises — for malformed or non-matching input:
    out-of-range index, zero tree size, wrong path length, malformed digest,
    tampered leaf/sibling/root.
    """
    if not isinstance(leaf_index, int) or isinstance(leaf_index, bool):
        return False
    if not isinstance(tree_size, int) or isinstance(tree_size, bool):
        return False
    if tree_size <= 0 or leaf_index < 0 or leaf_index >= tree_size:
        return False
    try:
        node = _require_digest("leaf", leaf)
        root = _require_digest("expected_root", expected_root)
        siblings = [_require_digest(f"path[{i}]", s) for i, s in enumerate(path)]
    except (TypeError, ValueError):
        return False

    fn = leaf_index
    sn = tree_size - 1
    for sibling in siblings:
        if sn == 0:
            # Path is longer than the tree admits.
            return False
        if (fn & 1) or fn == sn:
            node = node_hash(sibling, node)
            while fn != 0 and (fn & 1) == 0:
                fn >>= 1
                sn >>= 1
        else:
            node = node_hash(node, sibling)
        fn >>= 1
        sn >>= 1

    # Path must be exactly long enough to consume the tree.
    return sn == 0 and node == root
