"""CROSS-LANGUAGE-001 equality gate for CANONICAL-001.

This module is an *artifact comparator*, not a canonicalizer.

Hard constraints (anti-fabrication):

* It MUST NOT import, invoke or link either JCS implementation.
* It MUST NOT re-serialize ``input.json``.
* It MUST NOT construct canonical bytes.
* It MUST NOT normalise, repair or overwrite either artifact.

Its only inputs are two independently produced execution artifacts:

    conformance/corpus/canonical-001/ri-py.json   (produced by RI-PY / rfc8785)
    conformance/corpus/canonical-001/ri-rs.json   (produced by RI-RS / serde_json_canonicalizer)

The corpus directory may be redirected with the ``AURA_CORPUS_DIR``
environment variable. That hook exists so the negative controls can run *this
exact gate* against deliberately mutated temporary copies; it never points at
the committed corpus during a negative-control run.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS = REPO_ROOT / "conformance" / "corpus" / "canonical-001"

LEAF_DOMAIN = b"\x00"

# Frozen CANONICAL-001 reference values. SECONDARY cross-check only (Phase 7).
# The primary gate is RI-PY actual == RI-RS actual; these constants are never
# used to build, patch or backfill an artifact.
FROZEN_CANONICAL_BYTES_HEX = (
    "7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f6164"
    "223a7b2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e"
    "30222c22736368656d615f76657273696f6e223a22312e30227d"
)
FROZEN_SHA256 = "b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6"
FROZEN_LEAF_SHA256 = "ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039"


def corpus_dir() -> Path:
    override = os.environ.get("AURA_CORPUS_DIR")
    return Path(override).resolve() if override else DEFAULT_CORPUS


def _load(name: str) -> dict[str, Any]:
    path = corpus_dir() / name
    if not path.is_file():
        raise FileNotFoundError(f"CANONICAL-001 artifact missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class CheckResult:
    """Outcome of a single equality-gate check."""

    check: str
    name: str
    ok: bool
    detail: str


def _check(check: str, name: str, ok: bool, detail: str) -> CheckResult:
    return CheckResult(check=check, name=name, ok=ok, detail=detail)


def evaluate(ri_py: dict[str, Any], ri_rs: dict[str, Any]) -> list[CheckResult]:
    """Run the seven CROSS-LANGUAGE-001 checks over two execution artifacts."""
    py_hex = ri_py["canonical_bytes_hex"]
    rs_hex = ri_rs["canonical_bytes_hex"]
    py_bytes = bytes.fromhex(py_hex)
    rs_bytes = bytes.fromhex(rs_hex)

    py_sha_actual = hashlib.sha256(py_bytes).hexdigest()
    rs_sha_actual = hashlib.sha256(rs_bytes).hexdigest()
    py_leaf_actual = hashlib.sha256(LEAF_DOMAIN + py_bytes).hexdigest()
    rs_leaf_actual = hashlib.sha256(LEAF_DOMAIN + rs_bytes).hexdigest()

    return [
        _check(
            "CHECK 1",
            "canonical bytes equality",
            py_hex == rs_hex,
            f"RI-PY={py_hex} RI-RS={rs_hex}",
        ),
        _check(
            "CHECK 2",
            "RI-PY sha256 independently verifies",
            py_sha_actual == ri_py["sha256"],
            f"recomputed={py_sha_actual} claimed={ri_py['sha256']}",
        ),
        _check(
            "CHECK 3",
            "RI-RS sha256 independently verifies",
            rs_sha_actual == ri_rs["sha256"],
            f"recomputed={rs_sha_actual} claimed={ri_rs['sha256']}",
        ),
        _check(
            "CHECK 4",
            "sha256 equality",
            ri_py["sha256"] == ri_rs["sha256"],
            f"RI-PY={ri_py['sha256']} RI-RS={ri_rs['sha256']}",
        ),
        _check(
            "CHECK 5",
            "RI-PY leaf independently verifies",
            py_leaf_actual == ri_py["leaf_sha256"],
            f"recomputed={py_leaf_actual} claimed={ri_py['leaf_sha256']}",
        ),
        _check(
            "CHECK 6",
            "RI-RS leaf independently verifies",
            rs_leaf_actual == ri_rs["leaf_sha256"],
            f"recomputed={rs_leaf_actual} claimed={ri_rs['leaf_sha256']}",
        ),
        _check(
            "CHECK 7",
            "leaf equality",
            ri_py["leaf_sha256"] == ri_rs["leaf_sha256"],
            f"RI-PY={ri_py['leaf_sha256']} RI-RS={ri_rs['leaf_sha256']}",
        ),
    ]


def failures(results: list[CheckResult]) -> list[CheckResult]:
    return [r for r in results if not r.ok]


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------


@pytest.fixture(scope="module")
def ri_py() -> dict[str, Any]:
    return _load("ri-py.json")


@pytest.fixture(scope="module")
def ri_rs() -> dict[str, Any]:
    return _load("ri-rs.json")


@pytest.fixture(scope="module")
def results(ri_py: dict[str, Any], ri_rs: dict[str, Any]) -> list[CheckResult]:
    return evaluate(ri_py, ri_rs)


# --------------------------------------------------------------------------
# provenance guards — the artifacts must be distinguishable execution evidence
# --------------------------------------------------------------------------


def test_artifacts_declare_distinct_implementations(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    assert ri_py["fixture"] == "CANONICAL-001"
    assert ri_rs["fixture"] == "CANONICAL-001"
    assert ri_py["implementation"] == "RI-PY"
    assert ri_rs["implementation"] == "RI-RS"
    assert ri_py["repository"] == "Aura-IDToken/aura-poc-a-core-v3.3"
    assert ri_rs["repository"] == "Aura-IDToken/aura-guard-v1.3"


def test_artifacts_declare_distinct_engines(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    assert (ri_py["engine"], ri_py["engine_version"]) == ("rfc8785", "0.1.4")
    assert (ri_rs["engine"], ri_rs["engine_version"]) == (
        "serde_json_canonicalizer",
        "0.3.2",
    )
    assert ri_py["engine"] != ri_rs["engine"]


def test_artifacts_are_traceable_to_commits(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    for artifact in (ri_py, ri_rs):
        commit = artifact["commit"]
        assert isinstance(commit, str) and len(commit) == 40
        int(commit, 16)


# --------------------------------------------------------------------------
# CHECK 1..7 — the primary gate
# --------------------------------------------------------------------------


@pytest.mark.parametrize("index", range(7))
def test_cross_language_check(results: list[CheckResult], index: int) -> None:
    result = results[index]
    assert result.ok, f"{result.check} ({result.name}) FAILED: {result.detail}"


def test_cross_language_gate_overall(results: list[CheckResult]) -> None:
    bad = failures(results)
    assert not bad, "CROSS-LANGUAGE-001 FAIL: " + "; ".join(
        f"{r.check} {r.name}: {r.detail}" for r in bad
    )


# --------------------------------------------------------------------------
# Phase 7 — SECONDARY cross-check against the frozen reference values
# --------------------------------------------------------------------------


@pytest.mark.parametrize("impl", ["ri_py", "ri_rs"])
def test_secondary_frozen_expected_cross_check(
    impl: str, ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    artifact = ri_py if impl == "ri_py" else ri_rs
    assert artifact["canonical_bytes_hex"] == FROZEN_CANONICAL_BYTES_HEX
    assert artifact["sha256"] == FROZEN_SHA256
    assert artifact["leaf_sha256"] == FROZEN_LEAF_SHA256
