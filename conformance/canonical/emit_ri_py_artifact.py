"""Emit an RI-PY canonical-fixture execution artifact.

This script produces ``conformance/corpus/<fixture>/ri-py.json`` from an
*actual* execution of the frozen RI-PY JCS boundary. It defaults to
CANONICAL-001; CANONICAL-002 (the JCS-discriminating fixture) is selected with
``--fixture canonical-002``. The default invocation and its output are
byte-for-byte what they were before CANONICAL-002 existed.

Anti-fabrication rules enforced here:

* The canonical bytes are whatever ``conformance.canonical.jcs.canonical_bytes``
  (a direct delegation to ``rfc8785``) returns for the parsed fixture input.
  They are never constructed, patched or compared-and-corrected.
* No expected/frozen reference constant is read by this script. The frozen
  reference values are a *secondary* cross-check performed elsewhere, after the
  artifact exists.
* No other implementation's artifact is read by this script.

Usage::

    python -m conformance.canonical.emit_ri_py_artifact
    python -m conformance.canonical.emit_ri_py_artifact --fixture canonical-002
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

from conformance.canonical import jcs

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_ROOT = REPO_ROOT / "conformance" / "corpus"

REPOSITORY = "Aura-IDToken/aura-poc-a-core-v3.3"
LEAF_DOMAIN = b"\x00"

DEFAULT_FIXTURE_DIR = "canonical-001"

BASE_COMMAND = "python -m conformance.canonical.emit_ri_py_artifact"


def execution_command(fixture_dir: str) -> str:
    """Return the exact command that produced an artifact.

    The default fixture keeps the original command string verbatim, so the
    committed CANONICAL-001 artifact remains reproducible unchanged.
    """
    if fixture_dir == DEFAULT_FIXTURE_DIR:
        return BASE_COMMAND
    return f"{BASE_COMMAND} --fixture {fixture_dir}"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def build_artifact(fixture_dir: str = DEFAULT_FIXTURE_DIR) -> dict[str, object]:
    """Execute the RI-PY canonical path and package the observed evidence."""
    corpus = CORPUS_ROOT / fixture_dir
    input_path = corpus / "input.json"
    fixture_id = fixture_dir.upper()

    fixture_input = json.loads(input_path.read_text(encoding="utf-8"))

    # --- the only place canonical bytes come into existence -----------------
    canonical = jcs.canonical_bytes(fixture_input)
    # -----------------------------------------------------------------------

    digest = hashlib.sha256(canonical).hexdigest()
    leaf = hashlib.sha256(LEAF_DOMAIN + canonical).hexdigest()

    adapter_path = Path(jcs.__file__).resolve()

    return {
        "fixture": fixture_id,
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
        "provenance": {
            "input_path": str(input_path.relative_to(REPO_ROOT)),
            "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
            "adapter_path": str(adapter_path.relative_to(REPO_ROOT)),
            "adapter_sha256": hashlib.sha256(adapter_path.read_bytes()).hexdigest(),
            "execution_command": execution_command(fixture_dir),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        default=DEFAULT_FIXTURE_DIR,
        help="corpus directory under conformance/corpus (default: canonical-001)",
    )
    args = parser.parse_args(argv)

    artifact = build_artifact(args.fixture)
    output_path = CORPUS_ROOT / args.fixture / "ri-py.json"
    output_path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(artifact, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
