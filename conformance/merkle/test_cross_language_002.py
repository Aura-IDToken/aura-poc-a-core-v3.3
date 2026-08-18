"""CROSS-LANGUAGE-002 equality gate: RI-PY vs RI-RS, DQ-002 Merkle contract.

This test recomputes the RI-PY vector set in-process and compares it to the
RI-RS vector set emitted by `tests/dq002_cross_language.rs` in
`Aura-IDToken/aura-guard-v1.3` and vendored here under `evidence/`.

Direction of evidence
---------------------
RI-PY never supplies its own expected values. Roots, leaf hashes and audit
paths are additionally checked against
`fixtures/FIX-CK003-DQ002-RFC6962-EDGE-MATRIX.json`, which was produced by a
third, independent implementation (GNU coreutils SHA-256; see
`ck003/dq-002-hash-domain/tools/rfc6962_oracle.sh` in aura-specification).
An RI-PY bug therefore cannot mask itself.

Refreshing
----------
`evidence/RI-RS-VECTORS.json` is a frozen artifact. Regenerate it in the
aura-guard repository (`cargo test --test dq002_cross_language`) and copy it
here deliberately; do not edit it by hand.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any, Dict

import pytest

from conformance.merkle.emit_vectors import build_vectors

EVIDENCE_DIR = pathlib.Path(__file__).resolve().parent / "evidence"
RI_RS_VECTORS_PATH = EVIDENCE_DIR / "RI-RS-VECTORS.json"

# Frozen digest of the RI-RS emission, so a silent substitution fails loudly.
RI_RS_VECTORS_SHA256 = (
    "82e47587b046bfdb121a5170b967a44403dd98ccd6cbbfedd2321db010e8a67b"
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


@pytest.fixture(scope="module")
def ri_rs() -> Dict[str, Any]:
    return json.loads(RI_RS_VECTORS_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ri_py() -> Dict[str, Any]:
    return build_vectors()


def test_ri_rs_vector_file_is_the_pinned_artifact() -> None:
    actual = hashlib.sha256(RI_RS_VECTORS_PATH.read_bytes()).hexdigest()
    assert actual == RI_RS_VECTORS_SHA256, (
        "RI-RS vector file changed; re-run the aura-guard emitter and update "
        "the pin deliberately"
    )


def test_schema_matches(ri_py: Dict[str, Any], ri_rs: Dict[str, Any]) -> None:
    assert ri_py["schema"] == ri_rs["schema"] == "aura/dq-002/cross-language-vectors/1"
    assert ri_py["hash_domain"] == ri_rs["hash_domain"] == "RFC6962"


def test_canonical_input_bytes_agree(ri_py: Dict[str, Any], ri_rs: Dict[str, Any]) -> None:
    assert ri_py["leaf_payloads_utf8"] == ri_rs["leaf_payloads_utf8"]
    assert (
        ri_py["fixture_ck003_dq002_001"]["canonical_bytes_hex"]
        == ri_rs["fixture_ck003_dq002_001"]["canonical_bytes_hex"]
    )
    assert (
        ri_py["fixture_ck003_dq002_001"]["canonical_length_bytes"]
        == ri_rs["fixture_ck003_dq002_001"]["canonical_length_bytes"]
        == 58
    )


def test_leaf_hashes_agree(ri_py: Dict[str, Any], ri_rs: Dict[str, Any]) -> None:
    assert ri_py["leaf_hashes_hex"] == ri_rs["leaf_hashes_hex"]
    assert ri_py["fixture_2leaf"] == ri_rs["fixture_2leaf"]


def test_internal_node_hash_agrees(ri_py: Dict[str, Any], ri_rs: Dict[str, Any]) -> None:
    assert (
        ri_py["fixture_ck003_dq002_001"]["node_digest_hex"]
        == ri_rs["fixture_ck003_dq002_001"]["node_digest_hex"]
    )
    assert (
        ri_py["fixture_ck003_dq002_001"]["leaf_digest_hex"]
        == ri_rs["fixture_ck003_dq002_001"]["leaf_digest_hex"]
    )


def test_empty_root_agrees(ri_py: Dict[str, Any], ri_rs: Dict[str, Any]) -> None:
    assert ri_py["empty_root_hex"] == ri_rs["empty_root_hex"]


@pytest.mark.parametrize("n", list(range(0, 9)))
def test_roots_agree_for_every_tree_size(
    n: int, ri_py: Dict[str, Any], ri_rs: Dict[str, Any]
) -> None:
    py = next(t for t in ri_py["trees"] if t["tree_size"] == n)
    rs = next(t for t in ri_rs["trees"] if t["tree_size"] == n)
    assert py["root_hex"] == rs["root_hex"]


@pytest.mark.parametrize("n", list(range(0, 9)))
def test_audit_paths_agree_for_every_tree_size(
    n: int, ri_py: Dict[str, Any], ri_rs: Dict[str, Any]
) -> None:
    py = next(t for t in ri_py["trees"] if t["tree_size"] == n)
    rs = next(t for t in ri_rs["trees"] if t["tree_size"] == n)
    assert py["audit_paths"] == rs["audit_paths"]


@pytest.mark.parametrize("n", list(range(0, 9)))
def test_verification_decisions_agree_for_every_tree_size(
    n: int, ri_py: Dict[str, Any], ri_rs: Dict[str, Any]
) -> None:
    """Every accept/reject decision, including every negative control."""
    py = next(t for t in ri_py["verification_matrix"] if t["tree_size"] == n)
    rs = next(t for t in ri_rs["verification_matrix"] if t["tree_size"] == n)
    assert py["cases"] == rs["cases"]


def test_whole_vector_set_is_bit_identical(
    ri_py: Dict[str, Any], ri_rs: Dict[str, Any]
) -> None:
    py_digest = hashlib.sha256(_canonical(ri_py)).hexdigest()
    rs_digest = hashlib.sha256(_canonical(ri_rs)).hexdigest()
    assert py_digest == rs_digest, "RI-PY and RI-RS vector sets diverge"


def test_negative_controls_are_discriminating(ri_py: Dict[str, Any]) -> None:
    """Guard against a verifier that accepts everything."""
    rejections = 0
    for tree in ri_py["verification_matrix"]:
        for case in tree["cases"]:
            assert case["valid"]
            assert not case["tampered_leaf_accepted"]
            assert not case["tampered_root_accepted"]
            assert not any(case["tampered_sibling_accepted"])
            assert case["accepted_leaf_indices"] == [case["leaf_index"]]
            rejections += 1
    assert rejections >= 36, "matrix too small to be meaningful"
