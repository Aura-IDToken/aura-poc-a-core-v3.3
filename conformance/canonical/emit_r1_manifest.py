"""Emit the R1-JCS-DISCRIMINATING corpus manifest.

The manifest is an index, not evidence. It records:

* INPUT      — the frozen fixture and its file digest.
* PROTOCOL   — the canonicalization / digest / leaf contract under test.
* DISCRIMINATION — which RFC 8785 properties this fixture exercises.
* REFERENCE  — see below.
* RI-PY      — a *reference* to the RI-PY execution artifact, by path and file
               digest. The manifest never restates RI-PY's observed values.
* RI-RS      — a *reference* to the RI-RS execution artifact, likewise.

Keeping the observed values out of the RI-PY/RI-RS blocks is deliberate: a
manifest that restated them could be mistaken for, or silently substituted for,
the execution evidence itself.

The ``reference`` block is the one exception, and it is not an oracle. Unlike
CANONICAL-001 — whose expected values came from aura-specification — R1 has no
external oracle: RFC 8785 output for this fixture is defined by the standard,
and the only honest way to obtain it is to run a conforming engine. The
reference block therefore records the **consensus of two independent
executions**, and this script refuses to write it unless RI-PY and RI-RS
already agree and both digests recompute from the bytes. It exists as a
regression anchor for future runs, never as a source to backfill an artifact
from.

Usage::

    python -m conformance.canonical.emit_r1_manifest
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "r1-jcs-discriminating"
OUTPUT_PATH = CORPUS / "manifest.json"

FIXTURE = "R1-JCS-DISCRIMINATING"
LEAF_DOMAIN = b"\x00"


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(name: str) -> dict[str, object]:
    return json.loads((CORPUS / name).read_text(encoding="utf-8"))


def _artifact_ref(
    name: str, source_repository: str, source_path: str
) -> dict[str, object]:
    path = CORPUS / name
    artifact = _load(name)
    return {
        "artifact": name,
        "artifact_sha256": _file_sha256(path),
        "implementation": artifact["implementation"],
        "source_repository": source_repository,
        "source_repository_path": source_path,
        "source_commit": artifact["commit"],
        "engine": artifact["engine"],
        "engine_version": artifact["engine_version"],
        "conventional_serializer": artifact["discrimination"]["conventional_serializer"],
    }


def _consensus_reference() -> dict[str, object]:
    """Return the recorded consensus of the two executions, or refuse."""
    ri_py = _load("ri-py.json")
    ri_rs = _load("ri-rs.json")

    if ri_py["canonical_bytes_hex"] != ri_rs["canonical_bytes_hex"]:
        raise SystemExit(
            "REFUSING to write a manifest: RI-PY and RI-RS canonical bytes differ. "
            "There is no consensus to record."
        )

    canonical = bytes.fromhex(str(ri_py["canonical_bytes_hex"]))
    sha256 = hashlib.sha256(canonical).hexdigest()
    leaf = hashlib.sha256(LEAF_DOMAIN + canonical).hexdigest()

    for label, artifact in (("RI-PY", ri_py), ("RI-RS", ri_rs)):
        if artifact["sha256"] != sha256 or artifact["leaf_sha256"] != leaf:
            raise SystemExit(
                f"REFUSING to write a manifest: {label} digests do not recompute "
                "from its own canonical bytes."
            )
        if not artifact["discrimination"]["differs_from_jcs"]:
            raise SystemExit(
                f"REFUSING to write a manifest: {label} recorded no discrimination; "
                "R1 would not be a discriminating fixture."
            )

    return {
        "note": (
            "Recorded CONSENSUS of two independent executions (rfc8785 0.1.4 and "
            "serde_json_canonicalizer 0.3.2), not an external oracle. Regression "
            "anchor only. Never used to produce, patch or backfill an artifact."
        ),
        "canonical_bytes_hex": canonical.hex(),
        "canonical_bytes_len": len(canonical),
        "canonical_bytes_utf8": canonical.decode("utf-8"),
        "sha256": sha256,
        "leaf_sha256": leaf,
    }


def build_manifest() -> dict[str, object]:
    input_path = CORPUS / "input.json"
    return {
        "fixture": FIXTURE,
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
        "discrimination": {
            "claim": (
                "RFC 8785 output differs from a conventional sorted-key JSON "
                "serializer on this input."
            ),
            "properties": [
                {
                    "id": "D1",
                    "property": "UTF-16 code-unit key ordering (RFC 8785 §3.2.3)",
                    "detail": (
                        "U+1F600 (supplementary, UTF-16 D83D DE00) sorts before "
                        "U+FF3A (BMP) by code unit, and after it by code point."
                    ),
                },
                {
                    "id": "D2",
                    "property": "ECMAScript Number::toString (RFC 8785 §3.2.2.3)",
                    "detail": "1.0 -> 1, -0.0 -> 0, 1e-7 -> 1e-7.",
                },
            ],
            "not_discriminating_here": [
                "nested object ordering",
                "string escaping",
                "raw UTF-8 emission",
                "empty object / array",
            ],
        },
        "reference": _consensus_reference(),
        "ri_py": _artifact_ref(
            "ri-py.json",
            "Aura-IDToken/aura-poc-a-core-v3.3",
            "conformance/corpus/r1-jcs-discriminating/ri-py.json",
        ),
        "ri_rs": _artifact_ref(
            "ri-rs.json",
            "Aura-IDToken/aura-guard-v1.3",
            "conformance/corpus/r1-jcs-discriminating/ri-rs.json",
        ),
        "gate": {
            "ri_py_runner": "conformance/canonical/test_r1_jcs_discriminating.py",
            "cross_language_runner": "conformance/canonical/test_cross_language_r1.py",
            "ri_rs_runner": (
                "conformance/canonical/r1_jcs_discriminating.rs "
                "(Aura-IDToken/aura-guard-v1.3)"
            ),
            "negative_controls": "conformance/canonical/negative_controls_r1.py",
            "primary": "RI-PY actual == RI-RS actual",
            "discrimination": "RFC 8785 actual != conventional serializer actual",
        },
    }


def main() -> int:
    manifest = build_manifest()
    OUTPUT_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
