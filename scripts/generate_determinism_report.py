#!/usr/bin/env python3
"""
Generate a cross-platform determinism report for Aura Protocol v3.3.

Computes reference values from the frozen measurement core and writes
them to determinism-report.json.  CI collects this artifact from each
platform (x86_64 / ARM64) and the compare_determinism_reports script
verifies that every hash value is bit-identical.

Output fields:
  platform              — OS / CPU / Python info
  engine_version        — Instrument version tag
  hash_values:
    ari                 — int32 ARI for the reference input vector
    drift               — int32 drift for the reference input vector
    canonical_event_hash — SHA-256 of the canonical event JSON
    merkle_root         — Merkle root of a single-event tree
    audit_certificate_hash — SHA-256 of the audit certificate payload
  comparison_result     — PASS (set by this script; updated by compare script)
"""

import json
import hashlib
import platform
import sys
import os

# Ensure repository root is on the path when called from CI
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.evaluator import PoCAEvaluator
from core.offline_normalizer import generate_sample_constitution
from audit.merkle import MerkleTree

ENGINE_VERSION = "v3.3"
REFERENCE_AGENT_ID = "MACHINE_ACCOUNT_REF_001"


def canonical_event_hash(agent_id: str, ari: int, drift: int) -> str:
    """
    Hash of the canonical event payload.

    Serialization: JSON, keys sorted, no extra whitespace, UTF-8.
    Algorithm:     SHA-256.
    """
    event = {
        "agent_id": agent_id,
        "ari": ari,
        "drift": drift,
    }
    payload = json.dumps(event, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def audit_certificate_hash(event_hash: str, merkle_root: str) -> str:
    """
    Hash of the audit certificate payload.

    Serialization: JSON, keys sorted, no extra whitespace, UTF-8.
    Algorithm:     SHA-256.
    """
    cert = {
        "engine_version": ENGINE_VERSION,
        "event_hash": event_hash,
        "merkle_root": merkle_root,
    }
    payload = json.dumps(cert, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main(output_path: str = "determinism-report.json") -> None:
    # --- Deterministic test vectors ---
    constitution = generate_sample_constitution()
    evaluator = PoCAEvaluator(constitution)

    # Reference input: constitution vector itself (perfect alignment)
    result = evaluator.evaluate(REFERENCE_AGENT_ID, constitution, valid_schema=True)
    ari = result["ari"]
    drift = result["drift"]

    # --- Canonical hashes ---
    ev_hash = canonical_event_hash(REFERENCE_AGENT_ID, ari, drift)
    tree = MerkleTree([ev_hash], leaves_are_hashed=True)
    m_root = tree.get_root()
    cert_hash = audit_certificate_hash(ev_hash, m_root)

    report = {
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture()[0],
        },
        "engine_version": ENGINE_VERSION,
        "hash_values": {
            "ari": ari,
            "drift": drift,
            "canonical_event_hash": ev_hash,
            "merkle_root": m_root,
            "audit_certificate_hash": cert_hash,
        },
        "comparison_result": "PASS",
    }

    with open(output_path, "w") as fh:
        json.dump(report, fh, indent=2)

    print(f"Determinism report written to: {output_path}")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "determinism-report.json"
    main(out)
