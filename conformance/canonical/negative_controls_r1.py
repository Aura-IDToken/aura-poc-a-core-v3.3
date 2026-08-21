"""Negative controls for the R1-JCS-DISCRIMINATING gate.

A gate that always says PASS proves nothing. These controls demonstrate that
the R1 gates actually discriminate.

Method: copy the committed corpus into a throwaway temporary directory, mutate
the copy, and run the *real* gate against the copy via ``AURA_R1_CORPUS_DIR``.
Each control is expected to FAIL the gate.

Controls
--------

===  ====================  ==========================================  ==========
id   name                  mutation                                    mandate
===  ====================  ==========================================  ==========
A    Modified bytes        flip one byte of RI-RS canonical bytes      §8
B    Modified SHA          corrupt RI-PY sha256, bytes intact          §8
C    Wrong leaf domain     recompute both leaves under 0x01            §11
D    Wrong engine          regenerate RI-PY bytes with json.dumps      §10
E    Non-discriminating    swap in the CANONICAL-001 fixture values    §9
===  ====================  ==========================================  ==========

Control C keeps the two leaves *equal to each other*, so leaf equality still
passes. Only the independent leaf recomputations can catch it — which is
precisely the property under test.

Control D is the wrong-engine control. Rather than editing
``conformance/canonical/jcs.py`` in place — which would leave the repository
transiently holding a non-conforming implementation — it recomputes the RI-PY
artifact from the real fixture input using
``conformance.canonical.r1_conventional`` (plain ``json.dumps``), writes that
into the throwaway copy, and runs the real gate. This is the same substitution
with the same expected outcome, executed in a sandbox that cannot leak.

Control E is the R1-specific control: it replaces the corpus with artifacts
built from a fixture on which JCS and ``json.dumps`` agree (CANONICAL-001).
Cross-language equality still holds there, so checks 1..7 pass — and the gate
must still FAIL, because a corpus that records no discrimination is not R1.

The committed corpus is never mutated. This script verifies that by hashing
every corpus file before and after the run and refusing to report success if
any committed byte changed.

Usage::

    python -m conformance.canonical.negative_controls_r1
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

from conformance.canonical import jcs, r1_conventional

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "r1-jcs-discriminating"
CANONICAL_001_INPUT = (
    REPO_ROOT / "conformance" / "corpus" / "canonical-001" / "input.json"
)

GATES = [
    "conformance/canonical/test_cross_language_r1.py",
]

LEAF_DOMAIN_WRONG = b"\x01"


def _corpus_fingerprint() -> dict[str, str]:
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(CORPUS.iterdir())
        if p.is_file()
    }


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, artifact: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# controls
# ---------------------------------------------------------------------------


def _mutate_bytes(corpus: Path) -> str:
    """Control A: flip one byte of the RI-RS canonical bytes."""
    path = corpus / "ri-rs.json"
    artifact = _read(path)
    raw = bytearray(bytes.fromhex(artifact["canonical_bytes_hex"]))
    raw[-1] ^= 0x01
    artifact["canonical_bytes_hex"] = raw.hex()
    _write(path, artifact)
    return "RI-RS canonical_bytes_hex final byte flipped"


def _mutate_sha(corpus: Path) -> str:
    """Control B: corrupt the RI-PY SHA-256 while leaving the bytes intact."""
    path = corpus / "ri-py.json"
    artifact = _read(path)
    digest = bytearray(bytes.fromhex(artifact["sha256"]))
    digest[0] ^= 0xFF
    artifact["sha256"] = digest.hex()
    _write(path, artifact)
    return "RI-PY sha256 first byte corrupted"


def _mutate_leaf_domain(corpus: Path) -> str:
    """Control C: recompute both leaves under domain 0x01 instead of 0x00."""
    for name in ("ri-py.json", "ri-rs.json"):
        path = corpus / name
        artifact = _read(path)
        raw = bytes.fromhex(artifact["canonical_bytes_hex"])
        artifact["leaf_sha256"] = hashlib.sha256(LEAF_DOMAIN_WRONG + raw).hexdigest()
        _write(path, artifact)
    return (
        "leaf domain separator changed from 0x00 to 0x01 in both artifacts "
        "(leaf equality deliberately preserved)"
    )


def _mutate_wrong_engine(corpus: Path) -> str:
    """Control D: regenerate the RI-PY artifact with a conventional serializer.

    This is the wrong-engine substitution required by §10, executed against a
    throwaway copy so the committed implementation is never non-conforming.
    """
    fixture_input = json.loads(
        (CORPUS / "input.json").read_text(encoding="utf-8")
    )
    # The substituted "canonicalization": json.dumps instead of rfc8785.
    wrong = r1_conventional.conventional_bytes(fixture_input)

    path = corpus / "ri-py.json"
    artifact = _read(path)
    artifact["canonical_bytes_hex"] = wrong.hex()
    artifact["canonical_bytes_len"] = len(wrong)
    artifact["sha256"] = hashlib.sha256(wrong).hexdigest()
    artifact["leaf_sha256"] = hashlib.sha256(b"\x00" + wrong).hexdigest()
    # A substituted engine would honestly report itself as self-consistent:
    # every digest below recomputes correctly from the wrong bytes.
    artifact["discrimination"]["conventional_bytes_hex"] = wrong.hex()
    artifact["discrimination"]["conventional_bytes_len"] = len(wrong)
    artifact["discrimination"]["differs_from_jcs"] = False
    _write(path, artifact)
    return (
        "RI-PY JCS path replaced by "
        f"{r1_conventional.SERIALIZER} (all digests internally consistent)"
    )


def _mutate_non_discriminating(corpus: Path) -> str:
    """Control E: replace R1 with a fixture on which JCS and json.dumps agree."""
    fixture_input = json.loads(CANONICAL_001_INPUT.read_text(encoding="utf-8"))
    canonical = jcs.canonical_bytes(fixture_input)
    conventional = r1_conventional.conventional_bytes(fixture_input)
    assert canonical == conventional, "CANONICAL-001 was expected to be non-discriminating"

    for name in ("ri-py.json", "ri-rs.json"):
        path = corpus / name
        artifact = _read(path)
        artifact["canonical_bytes_hex"] = canonical.hex()
        artifact["canonical_bytes_len"] = len(canonical)
        artifact["sha256"] = hashlib.sha256(canonical).hexdigest()
        artifact["leaf_sha256"] = hashlib.sha256(b"\x00" + canonical).hexdigest()
        artifact["discrimination"]["conventional_bytes_hex"] = conventional.hex()
        artifact["discrimination"]["conventional_bytes_len"] = len(conventional)
        artifact["discrimination"]["differs_from_jcs"] = False
        _write(path, artifact)
    return (
        "corpus rebuilt on the CANONICAL-001 fixture, for which RFC 8785 and "
        "json.dumps agree; cross-language equality still holds"
    )


CONTROLS: list[tuple[str, str, Callable[[Path], str]]] = [
    ("A", "Modified bytes", _mutate_bytes),
    ("B", "Modified SHA", _mutate_sha),
    ("C", "Wrong leaf domain", _mutate_leaf_domain),
    ("D", "Wrong engine", _mutate_wrong_engine),
    ("E", "Non-discriminating fixture", _mutate_non_discriminating),
]


def _run_gate(corpus: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, AURA_R1_CORPUS_DIR=str(corpus))
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", *GATES],
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
        with tempfile.TemporaryDirectory(prefix=f"r1-neg-{label}-") as tmp:
            copy = Path(tmp) / "r1-jcs-discriminating"
            shutil.copytree(CORPUS, copy)
            description = mutate(copy)
            proc = _run_gate(copy)
            detected = proc.returncode != 0
            all_correct &= detected
            print(f"=== NEGATIVE CONTROL {label} — {name} ===")
            print(f"mutation: {description}")
            print(f"gate exit code: {proc.returncode}")
            print(proc.stdout.strip() or proc.stderr.strip())
            verdict = (
                "PASS (mutation detected)" if detected else "FAIL (mutation NOT detected)"
            )
            print(f"control {label}: {verdict}\n")

    after = _corpus_fingerprint()
    corpus_intact = before == after
    print("=== COMMITTED CORPUS INTEGRITY ===")
    for name, digest in sorted(after.items()):
        print(f"{digest}  {name}")
    print(f"committed corpus unmodified: {corpus_intact}")

    ok = all_correct and corpus_intact
    print(f"\nR1 NEGATIVE CONTROLS: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
