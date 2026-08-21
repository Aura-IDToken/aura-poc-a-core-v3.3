"""Emit the RI-PY R1-JCS-DISCRIMINATING execution artifact.

This script produces ``conformance/corpus/r1-jcs-discriminating/ri-py.json``
from an *actual* execution of the frozen RI-PY JCS boundary.

Anti-fabrication rules enforced here:

* The canonical bytes are whatever ``conformance.canonical.jcs.canonical_bytes``
  (a direct delegation to ``rfc8785``) returns for the parsed fixture input.
  They are never constructed, patched or compared-and-corrected.
* No expected/frozen reference constant is read by this script.
* No other implementation's artifact is read by this script. RI-RS values never
  enter this process.
* The conventional (non-JCS) serialization is recorded alongside, as
  *discrimination evidence*. It is computed from the same parsed input and is
  never used to produce a digest or a leaf.

Usage::

    python -m conformance.canonical.emit_ri_py_r1_artifact
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

from conformance.canonical import jcs, r1_conventional

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "r1-jcs-discriminating"
INPUT_PATH = CORPUS / "input.json"
OUTPUT_PATH = CORPUS / "ri-py.json"

REPOSITORY = "Aura-IDToken/aura-poc-a-core-v3.3"
FIXTURE = "R1-JCS-DISCRIMINATING"
LEAF_DOMAIN = b"\x00"

EXECUTION_COMMAND = "python -m conformance.canonical.emit_ri_py_r1_artifact"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def build_artifact() -> dict[str, object]:
    """Execute the RI-PY canonical path and package the observed evidence."""
    fixture_input = json.loads(INPUT_PATH.read_text(encoding="utf-8"))

    # --- the only place canonical bytes come into existence -----------------
    canonical = jcs.canonical_bytes(fixture_input)
    # -----------------------------------------------------------------------

    digest = hashlib.sha256(canonical).hexdigest()
    leaf = hashlib.sha256(LEAF_DOMAIN + canonical).hexdigest()

    # Discrimination evidence. Never a digest input.
    conventional = r1_conventional.conventional_bytes(fixture_input)

    adapter_path = Path(jcs.__file__).resolve()

    return {
        "fixture": FIXTURE,
        "implementation": "RI-PY",
        "repository": REPOSITORY,
        "commit": _git("rev-parse", "HEAD"),
        "worktree_clean": _git("status", "--porcelain") == "",
        "engine": jcs.ENGINE,
        "engine_version": jcs.engine_version(),
        "canonical_bytes_hex": canonical.hex(),
        "canonical_bytes_len": len(canonical),
        "sha256": digest,
        "leaf_sha256": leaf,
        "leaf_domain": "0x00",
        "canonicalization": "RFC8785",
        "discrimination": {
            "note": (
                "Evidence only. The conventional serialization is never hashed, "
                "never becomes a protocol value, and never replaces RFC 8785."
            ),
            "conventional_serializer": r1_conventional.SERIALIZER,
            "conventional_bytes_hex": conventional.hex(),
            "conventional_bytes_len": len(conventional),
            "differs_from_jcs": conventional != canonical,
        },
        "provenance": {
            "input_path": str(INPUT_PATH.relative_to(REPO_ROOT)),
            "input_sha256": hashlib.sha256(INPUT_PATH.read_bytes()).hexdigest(),
            "adapter_path": str(adapter_path.relative_to(REPO_ROOT)),
            "adapter_sha256": hashlib.sha256(adapter_path.read_bytes()).hexdigest(),
            "execution_command": EXECUTION_COMMAND,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
    }


def main() -> int:
    artifact = build_artifact()
    OUTPUT_PATH.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(artifact, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
