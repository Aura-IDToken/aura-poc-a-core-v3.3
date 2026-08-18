"""Negative controls for the CROSS-LANGUAGE-001 equality gate.

A gate that always says PASS proves nothing. These controls demonstrate that
the gate in ``test_cross_language_canonical_001.py`` actually discriminates.

Method: copy the committed corpus into a throwaway temporary directory, mutate
the copy, and run the *real* gate against the copy via ``AURA_CORPUS_DIR``.
Each control is expected to FAIL the gate.

The committed corpus is never mutated. This script verifies that by hashing
every corpus file before and after the run and refusing to report success if
any committed byte changed.

Usage::

    python -m conformance.canonical.negative_controls_canonical_001
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "canonical-001"
GATE = "conformance/canonical/test_cross_language_canonical_001.py"

LEAF_DOMAIN_WRONG = b"\x01"


def _corpus_fingerprint() -> dict[str, str]:
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(CORPUS.iterdir())
        if p.is_file()
    }


def _mutate_bytes(corpus: Path) -> str:
    """Control A: flip one byte of the RI-RS canonical bytes."""
    path = corpus / "ri-rs.json"
    artifact: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    original = artifact["canonical_bytes_hex"]
    raw = bytearray(bytes.fromhex(original))
    raw[-1] ^= 0x01
    artifact["canonical_bytes_hex"] = raw.hex()
    path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return "RI-RS canonical_bytes_hex final byte flipped"


def _mutate_sha(corpus: Path) -> str:
    """Control B: corrupt the RI-PY SHA-256 while leaving the bytes intact."""
    path = corpus / "ri-py.json"
    artifact: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    digest = bytearray(bytes.fromhex(artifact["sha256"]))
    digest[0] ^= 0xFF
    artifact["sha256"] = digest.hex()
    path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return "RI-PY sha256 first byte corrupted"


def _mutate_leaf_domain(corpus: Path) -> str:
    """Control C: recompute both leaves under domain 0x01 instead of 0x00.

    Note that this mutation keeps the two leaves *equal to each other*, so
    CHECK 7 still passes. Only the independent leaf verifications (CHECK 5 and
    CHECK 6) can catch it — which is precisely the property under test.
    """
    for name in ("ri-py.json", "ri-rs.json"):
        path = corpus / name
        artifact: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        raw = bytes.fromhex(artifact["canonical_bytes_hex"])
        artifact["leaf_sha256"] = hashlib.sha256(LEAF_DOMAIN_WRONG + raw).hexdigest()
        artifact["leaf_domain"] = "0x01"
        path.write_text(
            json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return "leaf domain separator changed from 0x00 to 0x01 in both artifacts"


CONTROLS: list[tuple[str, str, Callable[[Path], str]]] = [
    ("A", "Modified bytes", _mutate_bytes),
    ("B", "Modified SHA", _mutate_sha),
    ("C", "Wrong leaf domain", _mutate_leaf_domain),
]


def _run_gate(corpus: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, AURA_CORPUS_DIR=str(corpus))
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", GATE],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def main() -> int:
    before = _corpus_fingerprint()

    baseline = _run_gate(CORPUS)
    print("=== BASELINE (unmutated corpus, expected PASS) ===")
    print(baseline.stdout.strip() or baseline.stderr.strip())
    if baseline.returncode != 0:
        print("BASELINE DID NOT PASS -- negative controls are not meaningful.")
        return 1
    print("baseline: PASS\n")

    all_correct = True
    for label, name, mutate in CONTROLS:
        with tempfile.TemporaryDirectory(prefix=f"canonical-001-neg-{label}-") as tmp:
            copy = Path(tmp) / "canonical-001"
            shutil.copytree(CORPUS, copy)
            description = mutate(copy)
            proc = _run_gate(copy)
            detected = proc.returncode != 0
            all_correct &= detected
            print(f"=== NEGATIVE CONTROL {label} — {name} ===")
            print(f"mutation: {description}")
            print(f"gate exit code: {proc.returncode}")
            print(proc.stdout.strip() or proc.stderr.strip())
            print(f"control {label}: {'PASS (mutation detected)' if detected else 'FAIL (mutation NOT detected)'}\n")

    after = _corpus_fingerprint()
    corpus_intact = before == after
    print("=== COMMITTED CORPUS INTEGRITY ===")
    for name, digest in sorted(after.items()):
        print(f"{digest}  {name}")
    print(f"committed corpus unmodified: {corpus_intact}")

    ok = all_correct and corpus_intact
    print(f"\nNEGATIVE CONTROLS: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
