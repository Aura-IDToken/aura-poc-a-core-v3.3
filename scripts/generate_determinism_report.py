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
import subprocess
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
INT32_BYTE_ENCODING = "little-endian signed int32 (4 bytes)"

# ---------------------------------------------------------------------------
# Deterministic test vectors
# ---------------------------------------------------------------------------

# INSECURE TEST FIXTURE KEY — deterministic vector reproducibility only.
# MUST NEVER be used for production ETC signing or any operational credentials.
_INSECURE_TEST_KEY_DO_NOT_USE_IN_PROD = b"aura-v3.3-determinism-test-key-0"

# Canonical events — fixed strings used as Merkle leaves.
CANONICAL_EVENTS = [
    "agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000|ts=2026-01-01T00:00:00Z",
    "agent_id=MACHINE_ACCOUNT_002|ari=80000|drift=20000|ts=2026-01-01T00:01:00Z",
    "agent_id=MACHINE_ACCOUNT_003|ari=68000|drift=32000|ts=2026-01-01T00:02:00Z",
    "agent_id=MACHINE_ACCOUNT_004|ari=72000|drift=28000|ts=2026-01-01T00:03:00Z",
]


def hash_int32_array(array):
    """Hash an int32 array as little-endian signed int32 bytes."""
    buf = bytearray()
    for v in array:
        buf.extend(v.to_bytes(4, byteorder="little", signed=True))
    return hashlib.sha256(buf).hexdigest()


def get_commit_sha() -> str:
    """Get current git commit SHA."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "UNKNOWN"


def resolve_constitution_vector():
    """Resolve canonical constitution vector used by determinism evidence."""
    return generate_sample_constitution()


def build_constitution_vector_provenance(constitution, commit_sha: str) -> dict:
    """Build machine-verifiable provenance identity for constitution vector."""
    return {
        "schema_version": "1.0",
        "instrument": "Aura Protocol v3.3 Iron Core",
        "constitution_vector_source": "core.offline_normalizer.generate_sample_constitution",
        "dimension": len(constitution),
        "scaling_factor": 100000,
        "integer_representation": "int32",
        "byte_encoding": INT32_BYTE_ENCODING,
        "vector_sha256": hash_int32_array(constitution),
        "tested_commit_sha": commit_sha,
    }


def compute_vectors(constitution=None):
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
    if constitution is None:
        constitution = resolve_constitution_vector()
    ari_vector_hash = hash_int32_array(constitution[:1000])
    constitution_vector_sha256 = hash_int32_array(constitution)

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
    signer = HMACSigner(_INSECURE_TEST_KEY_DO_NOT_USE_IN_PROD)
    hmac_signature_hex = signer.sign(etc._signing_payload()).hex()

    return {
        "ari_vector_hash": ari_vector_hash,
        "constitution_vector_sha256": constitution_vector_sha256,
        "canonical_event_hash": canonical_event_hash,
        "merkle_root": merkle_root,
        "etc_hash": etc_hash,
        "hmac_signature_hex": hmac_signature_hex,
    }


def generate_report(output_path: Path, provenance_output_path: Path | None = None) -> dict:
    """Generate the determinism report and write it to *output_path*."""
    constitution = resolve_constitution_vector()
    vectors = compute_vectors(constitution)
    commit_sha = get_commit_sha()
    provenance = build_constitution_vector_provenance(constitution, commit_sha)

    report = {
        "schema_version": "1.0",
        "instrument": "Aura Protocol v3.3 Iron Core",
        "engine_version": ENGINE_VERSION,
        "commit_sha": commit_sha,
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
        },
        "determinism_vectors": vectors,
        "constitution_vector_provenance": provenance,
        "comparison_result": "NOT_COMPARED",
    }

    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if provenance_output_path is not None:
        provenance_output_path.write_text(json.dumps(provenance, indent=2), encoding="utf-8")
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
        "constitution_vector_sha256",
        "canonical_event_hash",
        "merkle_root",
        "etc_hash",
        "hmac_signature_hex",
    ):
        if vectors_a.get(field) != vectors_b.get(field):
            mismatches.append((field, vectors_a.get(field), vectors_b.get(field)))

    provenance_fields = (
        "dimension",
        "scaling_factor",
        "integer_representation",
        "byte_encoding",
        "vector_sha256",
    )
    provenance_a = report_a.get("constitution_vector_provenance", {})
    provenance_b = report_b.get("constitution_vector_provenance", {})
    for field in provenance_fields:
        if provenance_a.get(field) != provenance_b.get(field):
            mismatches.append(
                (f"constitution_vector_provenance.{field}", provenance_a.get(field), provenance_b.get(field))
            )

    return ("FAIL" if mismatches else "PASS", mismatches)


if __name__ == "__main__":
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else _REPO_ROOT / "determinism-report.json"
    provenance_output = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    report = generate_report(output, provenance_output)

    print("=" * 70)
    print("Aura Protocol v3.3 — Determinism Report")
    print("=" * 70)
    print(f"Platform : {report['platform']['system']} / {report['platform']['machine']}")
    print(f"Python   : {report['platform']['python_version']}")
    print(f"Engine   : {report['engine_version']}")
    print(f"Commit   : {report['commit_sha']}")
    print()
    for k, v in report["determinism_vectors"].items():
        print(f"  {k}: {v}")
    print()
    provenance = report["constitution_vector_provenance"]
    print("CONSTITUTION VECTOR PROVENANCE")
    print(f"dimension = {provenance['dimension']}")
    print(f"scaling_factor = {provenance['scaling_factor']}")
    print(f"encoding = {provenance['byte_encoding']}")
    print(f"vector_sha256 = {provenance['vector_sha256']}")
    print(f"commit_sha = {provenance['tested_commit_sha']}")
    print()
    print(f"Result   : {report['comparison_result']}")
    print(f"Output   : {output}")
    if provenance_output is not None:
        print(f"Provenance Output   : {provenance_output}")
    print("=" * 70)
