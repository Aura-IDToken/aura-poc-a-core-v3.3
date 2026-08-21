"""CROSS-LANGUAGE gate for the R1-JCS-DISCRIMINATING fixture.

This module is an *artifact comparator*, not a canonicalizer.

Hard constraints (anti-fabrication):

* It MUST NOT import, invoke or link either JCS implementation.
* It MUST NOT re-serialize ``input.json``.
* It MUST NOT construct canonical bytes.
* It MUST NOT normalise, repair or overwrite either artifact.

Its only inputs are two independently produced execution artifacts:

    conformance/corpus/r1-jcs-discriminating/ri-py.json   (RI-PY / rfc8785 0.1.4)
    conformance/corpus/r1-jcs-discriminating/ri-rs.json   (RI-RS / serde_json_canonicalizer 0.3.2)

The seven equality/verification checks are reused verbatim from the
CROSS-LANGUAGE-001 gate (``evaluate``) rather than reimplemented, so the two
corpora cannot drift apart in what "equal" means.

Unlike CANONICAL-001, R1 has **no external oracle**. Its reference values are a
*recorded consensus* of two independent executions, so this gate deliberately
has no "compare against a frozen expected constant" stage that could pass on
its own. The primary gate is the only gate: RI-PY actual == RI-RS actual, with
both digests recomputed from the bytes.

The corpus directory may be redirected with ``AURA_R1_CORPUS_DIR``. That hook
exists so the negative controls can run *this exact gate* against deliberately
mutated temporary copies; it never points at the committed corpus during a
negative-control run.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from conformance.canonical.test_cross_language_canonical_001 import (
    CheckResult,
    evaluate,
    failures,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS = REPO_ROOT / "conformance" / "corpus" / "r1-jcs-discriminating"

FIXTURE = "R1-JCS-DISCRIMINATING"


def corpus_dir() -> Path:
    override = os.environ.get("AURA_R1_CORPUS_DIR")
    return Path(override).resolve() if override else DEFAULT_CORPUS


def _load(name: str) -> dict[str, Any]:
    path = corpus_dir() / name
    if not path.is_file():
        raise FileNotFoundError(f"{FIXTURE} artifact missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ri_py() -> dict[str, Any]:
    return _load("ri-py.json")


@pytest.fixture(scope="module")
def ri_rs() -> dict[str, Any]:
    return _load("ri-rs.json")


@pytest.fixture(scope="module")
def results(ri_py: dict[str, Any], ri_rs: dict[str, Any]) -> list[CheckResult]:
    return evaluate(ri_py, ri_rs)


# ---------------------------------------------------------------------------
# provenance guards — the artifacts must be distinguishable execution evidence
# ---------------------------------------------------------------------------


def test_artifacts_declare_distinct_implementations(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    assert ri_py["fixture"] == FIXTURE
    assert ri_rs["fixture"] == FIXTURE
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


def test_both_implementations_consumed_the_same_input_bytes(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    """The fixture file must be byte-identical across the two repositories."""
    py_input = ri_py["provenance"]["input_sha256"]
    rs_input = ri_rs["provenance"]["input_sha256"]
    assert py_input == rs_input, (
        "the two implementations canonicalized different input files: "
        f"RI-PY={py_input} RI-RS={rs_input}"
    )


def test_leaf_domain_is_declared_as_0x00(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    assert ri_py["leaf_domain"] == "0x00"
    assert ri_rs["leaf_domain"] == "0x00"


# ---------------------------------------------------------------------------
# CHECK 1..7 — the primary gate
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("index", range(7))
def test_cross_language_check(results: list[CheckResult], index: int) -> None:
    result = results[index]
    assert result.ok, f"{result.check} ({result.name}) FAILED: {result.detail}"


def test_cross_language_gate_overall(results: list[CheckResult]) -> None:
    bad = failures(results)
    assert not bad, f"{FIXTURE} CROSS-LANGUAGE FAIL: " + "; ".join(
        f"{r.check} {r.name}: {r.detail}" for r in bad
    )


# ---------------------------------------------------------------------------
# R1-specific — the fixture must still be discriminating in both artifacts
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("impl", ["ri_py", "ri_rs"])
def test_each_implementation_recorded_a_real_discrimination(
    impl: str, ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    """A green cross-language gate on a non-discriminating fixture is worthless.

    Each side must have independently observed that its own conventional
    serializer disagrees with RFC 8785 on this input.
    """
    artifact = ri_py if impl == "ri_py" else ri_rs
    disc = artifact["discrimination"]

    assert disc["differs_from_jcs"] is True, f"{impl} recorded no discrimination"
    assert disc["conventional_bytes_hex"] != artifact["canonical_bytes_hex"]
    assert disc["conventional_bytes_len"] != artifact["canonical_bytes_len"]


def test_the_two_conventional_serializers_are_different_tools(
    ri_py: dict[str, Any], ri_rs: dict[str, Any]
) -> None:
    """The discrimination is not an artefact of one language's json library.

    Two unrelated conventional serializers — Python's ``json.dumps`` and Rust's
    ``serde_json::to_vec`` — both disagree with RFC 8785 here. They need not
    agree with *each other*, and in fact do not: their float formatting differs.
    """
    py_conv = ri_py["discrimination"]["conventional_serializer"]
    rs_conv = ri_rs["discrimination"]["conventional_serializer"]
    assert py_conv != rs_conv

    assert (
        ri_py["discrimination"]["conventional_bytes_hex"]
        != ri_rs["discrimination"]["conventional_bytes_hex"]
    ), "the two conventional serializers were expected to disagree with each other too"
