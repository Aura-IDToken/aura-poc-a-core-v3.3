"""CROSS-LANGUAGE-002 equality gate for CANONICAL-002.

Same architecture as the CANONICAL-001 gate: this module is an *artifact
comparator*, not a canonicalizer.

Hard constraints (anti-fabrication):

* It MUST NOT import, invoke or link either JCS implementation.
* It MUST NOT re-serialize ``input.json``.
* It MUST NOT construct canonical bytes.
* It MUST NOT normalise, repair or overwrite either artifact.

Its only inputs are two independently produced execution artifacts::

    conformance/corpus/canonical-002/ri-py.json   (RI-PY / rfc8785 0.1.4)
    conformance/corpus/canonical-002/ri-rs.json   (RI-RS / serde_json_canonicalizer 0.3.2)

Difference from CANONICAL-001
-----------------------------

CANONICAL-001 is JCS-degenerate: an ordinary sorted-JSON serializer reproduces
its canonical bytes exactly, so passing that gate demonstrates *agreement*
without demonstrating conformance to RFC 8785. CANONICAL-002 is built so that
RFC 8785 and sorted JSON provably diverge, which is what
``test_fixture_is_jcs_discriminating`` below asserts — using no canonicalizer,
only the corpus manifest's recorded divergence evidence.

The CANONICAL-001 gate carries its frozen reference values as inline
constants. This gate deliberately does not: CANONICAL-002's reference values
were established by *this* execution round, so the secondary cross-check reads
them from ``manifest.json`` instead. Hardcoding them here would make a copied
value indistinguishable from an executed one.

The corpus directory may be redirected with ``AURA_CORPUS_DIR`` so the negative
controls can run *this exact gate* against deliberately mutated temporary
copies.
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
DEFAULT_CORPUS = REPO_ROOT / "conformance" / "corpus" / "canonical-002"

LEAF_DOMAIN = b"\x00"


def corpus_dir() -> Path:
    override = os.environ.get("AURA_CORPUS_DIR")
    return Path(override).resolve() if override else DEFAULT_CORPUS


def _load(name: str) -> dict[str, Any]:
    path = corpus_dir() / name
    if not path.is_file():
        raise FileNotFoundError(f"CANONICAL-002 artifact missing: {path}")
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
    """Run the seven CROSS-LANGUAGE-002 checks over two execution artifacts."""
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
            f"RI-PY len={len(py_bytes)} RI-RS len={len(rs_bytes)}",
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
def manifest() -> dict[str, Any]:
    return _load("manifest.json")


@pytest.fixture(scope="module")
def results(ri_py: dict[str, Any], ri_rs: dict[str, Any]) -> list[CheckResult]:
    return evaluate(ri_py, ri_rs)


# --------------------------------------------------------------------------
# provenance guards — the artifacts must be distinguishable execution evidence
# --------------------------------------------------------------------------


def test_artifacts_declare_distinct_implementations(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    assert ri_py["fixture"] == "CANONICAL-002"
    assert ri_rs["fixture"] == "CANONICAL-002"
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


def test_both_sides_consumed_the_same_input(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    """Byte equality is only meaningful if both engines read the same bytes."""
    assert (
        ri_py["provenance"]["input_sha256"] == ri_rs["provenance"]["input_sha256"]
    ), "the two implementations did not canonicalize the same fixture input"


# --------------------------------------------------------------------------
# CHECK 1..7 — the primary gate
# --------------------------------------------------------------------------


@pytest.mark.parametrize("index", range(7))
def test_cross_language_check(results: list[CheckResult], index: int) -> None:
    result = results[index]
    assert result.ok, f"{result.check} ({result.name}) FAILED: {result.detail}"


def test_cross_language_gate_overall(results: list[CheckResult]) -> None:
    bad = failures(results)
    assert not bad, "CROSS-LANGUAGE-002 FAIL: " + "; ".join(
        f"{r.check} {r.name}: {r.detail}" for r in bad
    )


# --------------------------------------------------------------------------
# discrimination — the property CANONICAL-001 could not provide
# --------------------------------------------------------------------------


def test_fixture_is_jcs_discriminating(
    manifest: dict[str, Any], ri_py: dict[str, Any]
) -> None:
    """The fixture must separate RFC 8785 from ordinary sorted JSON.

    The manifest records the sorted-JSON serialization of the same input,
    produced by ``emit_manifest_002`` at corpus-build time. If that serialization
    ever equalled the canonical bytes, CANONICAL-002 would be as degenerate as
    CANONICAL-001 and this gate would prove nothing about RFC 8785 conformance.
    """
    naive_hex = manifest["discrimination"]["naive_sorted_json_bytes_hex"]
    canonical_hex = ri_py["canonical_bytes_hex"]

    assert naive_hex != canonical_hex, (
        "CANONICAL-002 is JCS-degenerate: a sorted-JSON serializer reproduces "
        "the canonical bytes, so this fixture cannot demonstrate RFC 8785 "
        "conformance"
    )
    assert hashlib.sha256(bytes.fromhex(naive_hex)).hexdigest() != ri_py["sha256"]


def test_utf16_ordering_is_actually_exercised(ri_py: dict[str, Any]) -> None:
    """Independently verify the UTF-16 vs code-point ordering claim.

    Decodes the canonical bytes and checks that the supplementary-plane key
    precedes ``U+FB00`` and ``U+FFFF``. Code-point ordering would place it last.
    No canonicalizer is used: this reads the produced bytes only.
    """
    text = bytes.fromhex(ri_py["canonical_bytes_hex"]).decode("utf-8")

    supplementary = text.index('"\U00010000"')
    ligature = text.index('"ﬀ"')
    bmp_max = text.index('"￿"')

    assert supplementary < ligature
    assert supplementary < bmp_max

    # Sanity-check the premise: by code point the supplementary key is largest.
    assert ord("\U00010000") > ord("ﬀ")
    assert ord("\U00010000") > ord("￿")
    # ...but its first UTF-16 code unit is smaller.
    assert "\U00010000".encode("utf-16-be")[:2] < "ﬀ".encode("utf-16-be")[:2]


def test_ecmascript_number_forms_are_present(ri_py: dict[str, Any]) -> None:
    """Independently verify the number forms in the produced bytes."""
    text = bytes.fromhex(ri_py["canonical_bytes_hex"]).decode("utf-8")

    assert '"one_point_zero":1,' in text
    assert '"negative_zero":0,' in text
    assert '"small_exponent":1e-7' in text
    assert '"exponent_boundary":0.000001' in text
    assert '"large_exponent":1e+21' in text
    assert "-0.0" not in text
    assert "1e-07" not in text


# --------------------------------------------------------------------------
# SECONDARY cross-check against the manifest's recorded reference values
# --------------------------------------------------------------------------


@pytest.mark.parametrize("impl", ["ri_py", "ri_rs"])
def test_secondary_frozen_expected_cross_check(
    impl: str,
    manifest: dict[str, Any],
    ri_py: dict[str, Any],
    ri_rs: dict[str, Any],
) -> None:
    artifact = ri_py if impl == "ri_py" else ri_rs
    expected = manifest["expected"]
    assert artifact["canonical_bytes_hex"] == expected["canonical_bytes_hex"]
    assert artifact["sha256"] == expected["sha256"]
    assert artifact["leaf_sha256"] == expected["leaf_sha256"]
