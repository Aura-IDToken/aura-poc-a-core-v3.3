"""Emit the RI-PY DQ-002 cross-language vector set as JSON.

The RI-RS counterpart is `tests/dq002_cross_language.rs` in
`Aura-IDToken/aura-guard-v1.3`. Both emit the same schema so that an
independent comparator can diff them without invoking either implementation.

The case set is fully deterministic and defined here in one place:

  * leaf payloads: "leaf-0" .. "leaf-7"
  * trees:         N = 0..8
  * audit paths:   every leaf index of every tree
  * verification:  for every (tree, index), the exact set of tree sizes and
                   leaf indices the verifier accepts, plus tamper decisions

Usage:
    python -m conformance.merkle.emit_vectors > RI-PY-VECTORS.json
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

from conformance.merkle import rfc6962

PRODUCER = "RI-PY"
MAX_LEAVES = 8
TREE_SIZES = list(range(0, MAX_LEAVES + 1))
PROBE_SIZES = list(range(0, MAX_LEAVES + 2))  # 0..9, deliberately overshooting

PAYLOADS = [f"leaf-{i}".encode("utf-8") for i in range(MAX_LEAVES)]
TAMPER_PAYLOAD = b"tampered"

# CK003-DQ002-001 canonical bytes (canonical serialization is out of DQ-002
# scope; the bytes are consumed here as an opaque, fixture-supplied payload).
CK003_CANONICAL_HEX = (
    "6167656e745f69643d413030317c6172693d39353030307c64726966743d3530"
    "30307c74733d323032362d30312d30315430303a30303a30305a"
)
CK003_NODE_LEFT_HEX = "00" * 32
CK003_NODE_RIGHT_HEX = "ff" * 32


def _flip_first(digest: bytes) -> bytes:
    b = bytearray(digest)
    b[0] ^= 0xFF
    return bytes(b)


def _flip_last(digest: bytes) -> bytes:
    b = bytearray(digest)
    b[31] ^= 0x01
    return bytes(b)


def _verification_cases(n: int, leaves: List[bytes]) -> List[Dict[str, Any]]:
    root = rfc6962.merkle_root(leaves)
    tampered_leaf = rfc6962.leaf_hash(TAMPER_PAYLOAD)
    cases: List[Dict[str, Any]] = []

    for m in range(n):
        path = rfc6962.audit_path(m, leaves)
        long_path = path + [path[0]] if path else [leaves[m]]
        cases.append(
            {
                "leaf_index": m,
                "valid": rfc6962.verify_audit_path(leaves[m], m, n, path, root),
                "accepted_tree_sizes": [
                    s
                    for s in PROBE_SIZES
                    if rfc6962.verify_audit_path(leaves[m], m, s, path, root)
                ],
                "accepted_leaf_indices": [
                    j
                    for j in range(0, n + 1)
                    if rfc6962.verify_audit_path(leaves[m], j, n, path, root)
                ],
                "tampered_leaf_accepted": rfc6962.verify_audit_path(
                    tampered_leaf, m, n, path, root
                ),
                "tampered_root_accepted": rfc6962.verify_audit_path(
                    leaves[m], m, n, path, _flip_last(root)
                ),
                "tampered_sibling_accepted": [
                    rfc6962.verify_audit_path(
                        leaves[m],
                        m,
                        n,
                        [_flip_first(s) if k == i else s for k, s in enumerate(path)],
                        root,
                    )
                    for i in range(len(path))
                ],
                "short_path_accepted": rfc6962.verify_audit_path(
                    leaves[m], m, n, path[:-1], root
                ),
                "long_path_accepted": rfc6962.verify_audit_path(
                    leaves[m], m, n, long_path, root
                ),
                "reversed_path_accepted": rfc6962.verify_audit_path(
                    leaves[m], m, n, list(reversed(path)), root
                ),
            }
        )
    return cases


def build_vectors() -> Dict[str, Any]:
    leaf_hashes = [rfc6962.leaf_hash(p) for p in PAYLOADS]

    trees: List[Dict[str, Any]] = []
    verification: List[Dict[str, Any]] = []
    for n in TREE_SIZES:
        leaves = leaf_hashes[:n]
        trees.append(
            {
                "tree_size": n,
                "root_hex": rfc6962.merkle_root(leaves).hex(),
                "audit_paths": [
                    {
                        "leaf_index": m,
                        "path_hex": [s.hex() for s in rfc6962.audit_path(m, leaves)],
                    }
                    for m in range(n)
                ],
            }
        )
        verification.append(
            {"tree_size": n, "cases": _verification_cases(n, leaves)}
        )

    canonical = bytes.fromhex(CK003_CANONICAL_HEX)

    return {
        "schema": "aura/dq-002/cross-language-vectors/1",
        "hash_domain": "RFC6962",
        "leaf_payloads_utf8": [p.decode("utf-8") for p in PAYLOADS],
        "leaf_hashes_hex": [h.hex() for h in leaf_hashes],
        "empty_root_hex": rfc6962.empty_root().hex(),
        "fixture_2leaf": {
            "leaf_a_hex": rfc6962.leaf_hash(b"a").hex(),
            "leaf_b_hex": rfc6962.leaf_hash(b"b").hex(),
            "root_hex": rfc6962.merkle_root(
                [rfc6962.leaf_hash(b"a"), rfc6962.leaf_hash(b"b")]
            ).hex(),
        },
        "fixture_ck003_dq002_001": {
            "canonical_bytes_hex": CK003_CANONICAL_HEX,
            "canonical_length_bytes": len(canonical),
            "leaf_digest_hex": rfc6962.leaf_hash(canonical).hex(),
            "node_digest_hex": rfc6962.node_hash(
                bytes.fromhex(CK003_NODE_LEFT_HEX), bytes.fromhex(CK003_NODE_RIGHT_HEX)
            ).hex(),
        },
        "trees": trees,
        "verification_matrix": verification,
    }


def main() -> int:
    json.dump(build_vectors(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
