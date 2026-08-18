"""Deterministic RFC 6962 Merkle audit primitives.

CROSS-LANGUAGE-002 remediation:
- leaf = SHA-256(0x00 || canonical_bytes)
- node = SHA-256(0x01 || left_digest || right_digest)
- raw 32-byte digests at hash boundaries
- RFC 6962 tree shape; no odd-node duplication

The public MerkleTree/ETC interface retains hexadecimal strings at the API
boundary for compatibility. Hex is representation only; it is never used as
input to a cryptographic hash.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence, Tuple

from .signing import Signer, Verifier

Digest = bytes


def sha256(data: str) -> str:
    """Compatibility helper: SHA-256 of UTF-8 application data.

    Merkle hashing MUST use ``leaf_hash`` and ``node_hash`` below.
    """
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def leaf_hash(data: bytes) -> Digest:
    """RFC 6962 leaf hash: SHA-256(0x00 || canonical_bytes)."""
    if not isinstance(data, bytes):
        raise TypeError("leaf_hash requires canonical bytes")
    return hashlib.sha256(b"\x00" + data).digest()


def node_hash(left: Digest, right: Digest) -> Digest:
    """RFC 6962 interior hash over two raw 32-byte child digests."""
    if len(left) != 32 or len(right) != 32:
        raise ValueError("node_hash requires two 32-byte digests")
    return hashlib.sha256(b"\x01" + left + right).digest()


def empty_root() -> Digest:
    """RFC 6962 empty-tree hash."""
    return hashlib.sha256(b"").digest()


def _largest_power_of_two_lt(n: int) -> int:
    if n < 2:
        raise ValueError("n must be >= 2")
    return 1 << (n.bit_length() - 1) if n & (n - 1) else n // 2


def merkle_root(leaves: Sequence[Digest]) -> Digest:
    """Compute RFC 6962 MTH from already-hashed leaves."""
    n = len(leaves)
    if n == 0:
        return empty_root()
    if any(len(x) != 32 for x in leaves):
        raise ValueError("all leaves must be 32-byte digests")
    if n == 1:
        return leaves[0]
    k = _largest_power_of_two_lt(n)
    return node_hash(merkle_root(leaves[:k]), merkle_root(leaves[k:]))


def audit_path(index: int, leaves: Sequence[Digest]) -> list[Digest]:
    """Build an RFC 6962 inclusion path for ``index``."""
    n = len(leaves)
    if n == 0 or index < 0 or index >= n:
        raise IndexError("leaf index out of range")
    if n == 1:
        return []
    k = _largest_power_of_two_lt(n)
    if index < k:
        return [*audit_path(index, leaves[:k]), merkle_root(leaves[k:])]
    return [*audit_path(index - k, leaves[k:]), merkle_root(leaves[:k])]


def _proof_length(index: int, size: int) -> int:
    if size <= 1:
        return 0
    k = _largest_power_of_two_lt(size)
    return _proof_length(index, k) + 1 if index < k else _proof_length(index - k, size - k) + 1


def verify_audit_path(
    leaf: Digest,
    leaf_index: int,
    tree_size: int,
    path: Sequence[Digest],
    expected_root: Digest,
) -> bool:
    """Verify an RFC 6962 inclusion path."""
    if len(leaf) != 32 or len(expected_root) != 32:
        return False
    if tree_size <= 0 or leaf_index < 0 or leaf_index >= tree_size:
        return False

    def rebuild(index: int, size: int, siblings: Sequence[Digest]) -> Optional[Digest]:
        if size == 1:
            return leaf if not siblings else None
        k = _largest_power_of_two_lt(size)
        if index < k:
            left_len = _proof_length(index, k)
            if len(siblings) != left_len + 1:
                return None
            left = rebuild(index, k, siblings[:left_len])
            return None if left is None else node_hash(left, siblings[left_len])
        if not siblings:
            return None
        right = rebuild(index - k, size - k, siblings[:-1])
        return None if right is None else node_hash(siblings[-1], right)

    rebuilt = rebuild(leaf_index, tree_size, list(path))
    return rebuilt == expected_root


@dataclass
class EventTrustCertificate:
    event_hash: str
    merkle_root: str
    merkle_proof: List[Tuple[str, str]]
    timestamp: str
    batch_id: Optional[str] = None
    signature: Optional[bytes] = field(default=None, repr=False)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "event_hash": self.event_hash,
            "merkle_root": self.merkle_root,
            "merkle_proof": [
                {"sibling": sibling, "direction": direction}
                for sibling, direction in self.merkle_proof
            ],
            "timestamp": self.timestamp,
            "batch_id": self.batch_id,
        }
        if self.signature is not None:
            result["signature"] = self.signature.hex()
        return result

    def _signing_payload(self) -> bytes:
        payload = {
            "event_hash": self.event_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def sign(self, signer: Signer) -> "EventTrustCertificate":
        import dataclasses
        return dataclasses.replace(self, signature=signer.sign(self._signing_payload()))

    def verify(self) -> bool:
        current = bytes.fromhex(self.event_hash)
        for sibling, direction in self.merkle_proof:
            sibling_digest = bytes.fromhex(sibling)
            current = node_hash(sibling_digest, current) if direction == "left" else node_hash(current, sibling_digest)
        return current.hex() == self.merkle_root

    def verify_signature(self, verifier: Verifier) -> bool:
        return self.signature is not None and verifier.verify(self._signing_payload(), self.signature)


class MerkleTree:
    """RFC 6962 Merkle tree with the existing hexadecimal API boundary."""

    def __init__(self, leaves: List[str], leaves_are_hashed: bool = False):
        if not leaves:
            raise ValueError("Cannot create Merkle tree with empty leaves")
        if leaves_are_hashed:
            self._leaf_digests = [bytes.fromhex(x) for x in leaves]
            if any(len(x) != 32 for x in self._leaf_digests):
                raise ValueError("pre-hashed leaves must be 32-byte digests")
        else:
            self._leaf_digests = [leaf_hash(x.encode("utf-8")) for x in leaves]
        self.leaves = [x.hex() for x in self._leaf_digests]
        self.root = merkle_root(self._leaf_digests).hex()

    def get_root(self) -> str:
        return self.root

    def get_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        if leaf_index < 0 or leaf_index >= len(self._leaf_digests):
            raise IndexError(f"Leaf index {leaf_index} out of range")
        path = audit_path(leaf_index, self._leaf_digests)
        directions: list[str] = []

        def collect(index: int, size: int) -> None:
            if size <= 1:
                return
            k = _largest_power_of_two_lt(size)
            if index < k:
                collect(index, k)
                directions.append("right")
            else:
                collect(index - k, size - k)
                directions.append("left")

        collect(leaf_index, len(self._leaf_digests))
        return [(digest.hex(), direction) for digest, direction in zip(path, directions)]

    def create_etc(self, leaf_index: int, timestamp: str, batch_id: Optional[str] = None) -> EventTrustCertificate:
        return EventTrustCertificate(
            event_hash=self.leaves[leaf_index],
            merkle_root=self.root,
            merkle_proof=self.get_proof(leaf_index),
            timestamp=timestamp,
            batch_id=batch_id,
        )


def verify_proof(leaf: str, proof: List[Tuple[str, str]], root: str) -> bool:
    """Verify a presentation-layer proof using the RFC 6962 node domain."""
    current = bytes.fromhex(leaf)
    for sibling, direction in proof:
        sibling_digest = bytes.fromhex(sibling)
        current = node_hash(sibling_digest, current) if direction == "left" else node_hash(current, sibling_digest)
    return current.hex() == root
