"""Emit the CANONICAL-001 corpus manifest.

The manifest is an index, not evidence. It records:

* INPUT     — the frozen fixture and its file digest.
* EXPECTED  — the frozen CANONICAL-001 reference values (secondary check only).
* RI-PY     — a *reference* to the RI-PY execution artifact, by path and file
              digest. The manifest never restates RI-PY's observed values.
* RI-RS     — a *reference* to the RI-RS execution artifact, likewise.

Keeping the observed values out of the manifest is deliberate: a manifest that
restated them could be mistaken for, or silently substituted for, the execution
evidence itself.

Usage::

    python -m conformance.canonical.emit_manifest
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "canonical-001"
OUTPUT_PATH = CORPUS / "manifest.json"

FROZEN_CANONICAL_BYTES_HEX = (
    "7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f6164"
    "223a7b2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e"
    "30222c22736368656d615f76657273696f6e223a22312e30227d"
)
FROZEN_SHA256 = "b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6"
FROZEN_LEAF_SHA256 = "ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039"


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_ref(name: str, source_repository: str, source_path: str) -> dict[str, object]:
    path = CORPUS / name
    artifact = json.loads(path.read_text(encoding="utf-8"))
    return {
        "artifact": name,
        "artifact_sha256": _file_sha256(path),
        "implementation": artifact["implementation"],
        "source_repository": source_repository,
        "source_repository_path": source_path,
        "source_commit": artifact["commit"],
        "engine": artifact["engine"],
        "engine_version": artifact["engine_version"],
    }


def build_manifest() -> dict[str, object]:
    input_path = CORPUS / "input.json"
    return {
        "fixture": "CANONICAL-001",
        "protocol": {
            "canonicalization": "RFC8785",
            "digest": "SHA-256",
            "leaf": "SHA-256(0x00 || canonical_bytes)",
            "leaf_domain": "0x00",
        },
        "input": {
            "path": "input.json",
            "sha256": _file_sha256(input_path),
            "value": json.loads(input_path.read_text(encoding="utf-8")),
        },
        "expected": {
            "note": (
                "Frozen reference values. SECONDARY cross-check only. Never used "
                "to produce, patch or backfill an execution artifact."
            ),
            "canonical_bytes_hex": FROZEN_CANONICAL_BYTES_HEX,
            "sha256": FROZEN_SHA256,
            "leaf_sha256": FROZEN_LEAF_SHA256,
        },
        "ri_py": _artifact_ref(
            "ri-py.json",
            "Aura-IDToken/aura-poc-a-core-v3.3",
            "conformance/corpus/canonical-001/ri-py.json",
        ),
        "ri_rs": _artifact_ref(
            "ri-rs.json",
            "Aura-IDToken/aura-guard-v1.3",
            "conformance/corpus/canonical-001/ri-rs.json",
        ),
        "gate": {
            "runner": "conformance/canonical/test_cross_language_canonical_001.py",
            "negative_controls": (
                "conformance/canonical/negative_controls_canonical_001.py"
            ),
            "primary": "RI-PY actual == RI-RS actual",
            "secondary": "RI-PY actual == expected and RI-RS actual == expected",
        },
    }


def main() -> int:
    manifest = build_manifest()
    OUTPUT_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
