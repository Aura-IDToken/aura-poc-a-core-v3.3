#!/usr/bin/env python3
"""
Aura Protocol v3.3 — Determinism Report Generator
CORE-006 Part A: Cross-platform determinism verification

Produces determinism-report.json containing:
  - platform (system, machine, architecture, python_version)
  - engine_version
  - determinism_vectors (fixed test-vector hash values)
  - comparison_result (NOT_COMPARED)

Usage (standalone):
    python scripts/generate_determinism_report.py [output_path]

The output path defaults to determinism-report.json in the repo root.

CI Usage:
    Runs on each platform (x86_64, ARM64).
    A separate compare job downloads both reports and checks that all
    hash values are identical.
"""

import hashlib
import json
import platform
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo root on PYTHONPATH
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from core.offline_normalizer import generate_sample_constitution
from audit.merkle import MerkleTree, sha256
from audit.signing import HMACSigner

# ---------------------------------------------------------------------------
# Engine version
# ---------------------------------------------------------------------------

ENGINE_VERSION = "v3.3-iron-core"

# ---------------------------------------------------------------------------
# Deterministic test vectors
# ---------------------------------------------------------------------------

# Fixed key — not a secret; used only for determinism verification.
_TEST_KEY = b"aura-v3.3-determinism-test-key-0"

# Canonical events — fixed strings used as Merkle leaves.
CANONICAL_EVENTS = [
    "agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000|ts=2026-01-01T00:00:00Z",
    "agent_id=MACHINE_ACCOUNT_002|ari=80000|drift=20000|ts=2026-01-01T00:01:00Z",
    "agent_id=MACHINE_ACCOUNT_003|ari=68000|drift=32000|ts=2026-01-01T00:02:00Z",
    "agent_id=MACHINE_ACCOUNT_004|ari=72000|drift=28000|ts=2026-01-01T00:03:00Z",
]


def _hash_int32_array(array):
    """Hash an int32 array as little-endian bytes (deterministic across platforms)."""
    buf = bytearray()
    for v in array:
        buf.extend(v.to_bytes(4, byteorder="little", signed=True))
    return hashlib.sha256(buf).hexdigest()


def compute_vectors():
    """
    Compute all determinism vectors.

    Returns a dict with:
      ari_vector_hash       — SHA-256 of the int32 constitution vector (1000 elems)
      canonical_event_hash  — SHA-256 of CANONICAL_EVENTS[0]
      merkle_root           — Merkle root of all CANONICAL_EVENTS
      etc_hash              — SHA-256 of the ETC for event 0 (dict, sort_keys)
      hmac_signature_hex    — HMAC-SHA256(key, signing_payload) for ETC 0
    """
    # ARI / constitution vector
    constitution = generate_sample_constitution()
    ari_vector_hash = _hash_int32_array(constitution[:1000])

    # Canonical event hash (event 0)
    canonical_event_hash = sha256(CANONICAL_EVENTS[0])

    # Merkle tree
    tree = MerkleTree(CANONICAL_EVENTS)
    merkle_root = tree.root

    # ETC for event 0
    etc = tree.create_etc(
        leaf_index=0,
        timestamp="2026-01-01T00:00:00Z",
        batch_id="determinism-batch-001",
    )
    etc_dict = etc.to_dict()
    etc_hash = hashlib.sha256(
        json.dumps(etc_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    # HMAC signature of ETC signing payload
    signer = HMACSigner(_TEST_KEY)
    hmac_signature_hex = signer.sign(etc._signing_payload()).hex()

    return {
        "ari_vector_hash": ari_vector_hash,
        "canonical_event_hash": canonical_event_hash,
        "merkle_root": merkle_root,
        "etc_hash": etc_hash,
        "hmac_signature_hex": hmac_signature_hex,
    }


def generate_report(output_path: Path) -> dict:
    """Generate the determinism report and write it to *output_path*."""
    vectors = compute_vectors()

    report = {
        "schema_version": "1.0",
        "instrument": "Aura Protocol",
        "instrument_version": "v3.3 Iron Core",
        "engine_version": ENGINE_VERSION,
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
        },
        "determinism_vectors": vectors,
        "comparison_result": "NOT_COMPARED",
    }

    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def compare_reports(report_a: dict, report_b: dict) -> tuple:
    """
    Compare two determinism reports.

    Returns (result, mismatches) where result is "PASS" or "FAIL" and
    mismatches is a list of (field, value_a, value_b) tuples.
    """
    mismatches = []
    vectors_a = report_a["determinism_vectors"]
    vectors_b = report_b["determinism_vectors"]

    for field in (
        "ari_vector_hash",
        "canonical_event_hash",
        "merkle_root",
        "etc_hash",
        "hmac_signature_hex",
    ):
        if vectors_a.get(field) != vectors_b.get(field):
            mismatches.append((field, vectors_a.get(field), vectors_b.get(field)))

    return ("FAIL" if mismatches else "PASS", mismatches)


if __name__ == "__main__":
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else _REPO_ROOT / "determinism-report.json"
    report = generate_report(output)

    print("=" * 70)
    print("Aura Protocol v3.3 — Determinism Report")
    print("=" * 70)
    print(f"Platform : {report['platform']['system']} / {report['platform']['machine']}")
    print(f"Python   : {report['platform']['python_version']}")
    print(f"Engine   : {report['engine_version']}")
    print()
    for k, v in report["determinism_vectors"].items():
        print(f"  {k}: {v}")
    print()
    print(f"Result   : {report['comparison_result']}")
    print(f"Output   : {output}")
    print("=" * 70)
