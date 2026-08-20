"""Negative controls for the CROSS-LANGUAGE-002 equality gate.

A gate that always says PASS proves nothing. These controls demonstrate that
the gate in ``test_cross_language_canonical_002.py`` actually discriminates.

Method: copy the committed corpus into a throwaway temporary directory, mutate
the copy, and run the *real* gate against the copy via ``AURA_CORPUS_DIR``.
Each control is expected to FAIL the gate.

Controls
--------

``A`` .. ``C`` are the CANONICAL-001 controls, re-run against this fixture:
mutated bytes, mutated digest, and a wrong leaf domain applied consistently to
both sides (which CHECK 7 alone cannot catch).

``D`` is new, and is the reason CANONICAL-002 exists. It replaces one side's
canonical bytes with the output of an ordinary sorted-JSON serializer over the
*same* input. On CANONICAL-001 that substitution is undetectable — sorted JSON
reproduces the canonical bytes exactly — so the gate would still pass. Here it
must fail. Control D is therefore the executable proof that this fixture
distinguishes RFC 8785 from a plausible non-conforming serializer.

**The incorrect serializer is confined to this file and to temporary copies.**
It is never installed as an adapter, never written to the committed corpus, and
never reachable from ``conformance/canonical/jcs.py``. The committed corpus is
hashed before and after the run; the script refuses to report success if any
committed byte changed.

Usage::

    python -m conformance.canonical.negative_controls_canonical_002
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
CORPUS = REPO_ROOT / "conformance" / "corpus" / "canonical-002"
GATE = "conformance/canonical/test_cross_language_canonical_002.py"

LEAF_DOMAIN_WRONG = b"\x01"


def _corpus_fingerprint() -> dict[str, str]:
    return {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(CORPUS.iterdir())
        if p.is_file()
    }


def _write(path: Path, artifact: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _mutate_bytes(corpus: Path) -> str:
    """Control A: flip one byte of the RI-RS canonical bytes."""
    path = corpus / "ri-rs.json"
    artifact: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    raw = bytearray(bytes.fromhex(artifact["canonical_bytes_hex"]))
    raw[-1] ^= 0x01
    artifact["canonical_bytes_hex"] = raw.hex()
    _write(path, artifact)
    return "RI-RS canonical_bytes_hex final byte flipped"


def _mutate_sha(corpus: Path) -> str:
    """Control B: corrupt the RI-PY SHA-256 while leaving the bytes intact."""
    path = corpus / "ri-py.json"
    artifact: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    digest = bytearray(bytes.fromhex(artifact["sha256"]))
    digest[0] ^= 0xFF
    artifact["sha256"] = digest.hex()
    _write(path, artifact)
    return "RI-PY sha256 first byte corrupted"


def _mutate_leaf_domain(corpus: Path) -> str:
    """Control C: recompute both leaves under domain 0x01 instead of 0x00.

    This mutation keeps the two leaves *equal to each other*, so CHECK 7 still
    passes. Only the independent leaf verifications (CHECK 5, CHECK 6) can catch
    it — which is precisely the property under test.
    """
    for name in ("ri-py.json", "ri-rs.json"):
        path = corpus / name
        artifact: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        raw = bytes.fromhex(artifact["canonical_bytes_hex"])
        artifact["leaf_sha256"] = hashlib.sha256(LEAF_DOMAIN_WRONG + raw).hexdigest()
        artifact["leaf_domain"] = "0x01"
        _write(path, artifact)
    return "leaf domain separator changed from 0x00 to 0x01 in both artifacts"


def _substitute_incorrect_serializer(corpus: Path) -> str:
    """Control D: replace RI-RS output with an ordinary sorted-JSON serializer.

    This simulates an implementation that believes ``json.dumps(sort_keys=True,
    separators=(",", ":"))`` is RFC 8785. The substituted artifact is internally
    *consistent* — its digest and leaf are recomputed over the substituted bytes
    — so CHECK 2, 3, 5 and 6 all still pass. Only CHECK 1, 4 and 7 catch it.

    On CANONICAL-001 this control would not fire at all: sorted JSON and RFC 8785
    produce identical bytes for that fixture. That it fires here is the whole
    point of CANONICAL-002.
    """
    value = json.loads((corpus / "input.json").read_text(encoding="utf-8"))
    wrong = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")

    path = corpus / "ri-rs.json"
    artifact: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    artifact["canonical_bytes_hex"] = wrong.hex()
    artifact["canonical_bytes_len"] = len(wrong)
    artifact["sha256"] = hashlib.sha256(wrong).hexdigest()
    artifact["leaf_sha256"] = hashlib.sha256(b"\x00" + wrong).hexdigest()
    _write(path, artifact)
    return (
        "RI-RS canonical bytes replaced by sorted-JSON serialization of the same "
        f"input ({len(wrong)} bytes), with digest and leaf recomputed to match"
    )


CONTROLS: list[tuple[str, str, Callable[[Path], str]]] = [
    ("A", "Modified bytes", _mutate_bytes),
    ("B", "Modified SHA", _mutate_sha),
    ("C", "Wrong leaf domain", _mutate_leaf_domain),
    ("D", "Incorrect serializer (sorted JSON, not RFC 8785)", _substitute_incorrect_serializer),
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
        with tempfile.TemporaryDirectory(prefix=f"canonical-002-neg-{label}-") as tmp:
            copy = Path(tmp) / "canonical-002"
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
    print(f"\nNEGATIVE CONTROLS: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
