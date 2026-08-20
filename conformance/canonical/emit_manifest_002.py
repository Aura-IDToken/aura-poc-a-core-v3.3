"""Emit the CANONICAL-002 corpus manifest.

The manifest is an index, not evidence. Like the CANONICAL-001 manifest it
records the input, references to both execution artifacts, and the gate wiring.

Two things differ from CANONICAL-001:

1. **The reference values are read from the executions, not hardcoded.**
   CANONICAL-001 was published with its reference values already frozen, so its
   manifest emitter carries them as literals. CANONICAL-002's values were
   established by the execution round that produced the two artifacts, so this
   emitter reads them back and refuses to write a manifest unless RI-PY and
   RI-RS independently agree. A value that only one engine produced can never
   become the frozen reference.

2. **A discrimination record.** The manifest stores the ordinary sorted-JSON
   serialization of the same input so that the gate can assert, without ever
   invoking a canonicalizer, that RFC 8785 and sorted JSON diverge on this
   fixture. This is the property CANONICAL-001 lacks.

The sorted-JSON serialization below is a *negative reference*. It is never used
as, compared as, or substituted for canonical bytes; its only purpose is to
prove that the two differ.

Usage::

    python -m conformance.canonical.emit_manifest_002
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "canonical-002"
OUTPUT_PATH = CORPUS / "manifest.json"


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact(name: str) -> dict[str, object]:
    return json.loads((CORPUS / name).read_text(encoding="utf-8"))


def _artifact_ref(
    name: str, source_repository: str, source_path: str
) -> dict[str, object]:
    path = CORPUS / name
    artifact = _artifact(name)
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


def _naive_sorted_json(value: object) -> bytes:
    """Ordinary sorted-JSON serialization — the NEGATIVE reference.

    This is deliberately *not* RFC 8785. It is the serializer a
    non-conforming implementation would plausibly use, recorded so the gate can
    show that CANONICAL-002 separates the two. It never touches an artifact.
    """
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build_manifest() -> dict[str, object]:
    input_path = CORPUS / "input.json"
    input_value = json.loads(input_path.read_text(encoding="utf-8"))

    ri_py = _artifact("ri-py.json")
    ri_rs = _artifact("ri-rs.json")

    # The frozen reference is only allowed to exist because two independent
    # engines produced it. Refuse to invent one from a single side.
    for field in ("canonical_bytes_hex", "sha256", "leaf_sha256"):
        if ri_py[field] != ri_rs[field]:
            raise SystemExit(
                f"refusing to write manifest: RI-PY and RI-RS disagree on {field}\n"
                f"  RI-PY={ri_py[field]}\n  RI-RS={ri_rs[field]}"
            )

    canonical = bytes.fromhex(str(ri_py["canonical_bytes_hex"]))
    naive = _naive_sorted_json(input_value)
    if naive == canonical:
        raise SystemExit(
            "refusing to write manifest: sorted-JSON output equals the canonical "
            "bytes, so CANONICAL-002 is JCS-degenerate and cannot demonstrate "
            "RFC 8785 conformance"
        )

    return {
        "fixture": "CANONICAL-002",
        "purpose": (
            "JCS-discriminating cross-language fixture. CANONICAL-001 is "
            "JCS-degenerate; CANONICAL-002 exercises UTF-16 code-unit member "
            "ordering, raw UTF-8 output, ECMAScript number form, negative-zero "
            "normalisation, exponent form, recursive canonicalisation, array "
            "order preservation and minimal escaping."
        ),
        "protocol": {
            "canonicalization": "RFC8785",
            "digest": "SHA-256",
            "leaf": "SHA-256(0x00 || canonical_bytes)",
            "leaf_domain": "0x00",
        },
        "input": {
            "path": "input.json",
            "sha256": _file_sha256(input_path),
            "value": input_value,
        },
        "expected": {
            "note": (
                "Frozen reference values, established by independent RI-PY and "
                "RI-RS execution agreeing byte-for-byte. SECONDARY cross-check "
                "only. Never used to produce, patch or backfill an artifact."
            ),
            "canonical_bytes_hex": ri_py["canonical_bytes_hex"],
            "canonical_bytes_len": ri_py["canonical_bytes_len"],
            "sha256": ri_py["sha256"],
            "leaf_sha256": ri_py["leaf_sha256"],
        },
        "discrimination": {
            "note": (
                "NEGATIVE reference. Ordinary sorted-JSON serialization of the "
                "same input. Recorded to prove that RFC 8785 and sorted JSON "
                "diverge on this fixture. Never compared as canonical bytes."
            ),
            "naive_serializer": (
                'json.dumps(value, sort_keys=True, separators=(",", ":"))'
            ),
            "naive_sorted_json_bytes_hex": naive.hex(),
            "naive_sorted_json_len": len(naive),
            "naive_sorted_json_sha256": hashlib.sha256(naive).hexdigest(),
            "canonical_bytes_len": len(canonical),
            "differs_from_canonical": naive != canonical,
        },
        "ri_py": _artifact_ref(
            "ri-py.json",
            "Aura-IDToken/aura-poc-a-core-v3.3",
            "conformance/corpus/canonical-002/ri-py.json",
        ),
        "ri_rs": _artifact_ref(
            "ri-rs.json",
            "Aura-IDToken/aura-guard-v1.3",
            "conformance/corpus/canonical-002/ri-rs.json",
        ),
        "gate": {
            "runner": "conformance/canonical/test_cross_language_canonical_002.py",
            "negative_controls": (
                "conformance/canonical/negative_controls_canonical_002.py"
            ),
            "primary": "RI-PY actual == RI-RS actual",
            "secondary": "RI-PY actual == expected and RI-RS actual == expected",
            "discrimination": "canonical bytes != sorted-JSON bytes",
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
