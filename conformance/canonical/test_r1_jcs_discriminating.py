"""R1-JCS-DISCRIMINATING — RI-PY execution and discrimination proof.

CANONICAL-001 proved that RI-PY *can* run an RFC 8785 engine. It could not
prove that RFC 8785 was actually required: its fixture uses ASCII keys and a
single small integer, for which ``json.dumps(sort_keys=True,
separators=(",", ":"))`` produces byte-identical output. A non-JCS
implementation passes CANONICAL-001.

R1 closes that hole. Its fixture is chosen so that the conventional serializer
and RFC 8785 disagree on the emitted bytes, in two independent dimensions:

**D1 — key ordering.** RFC 8785 §3.2.3 sorts object keys by UTF-16 code unit.
Python's ``sort_keys=True`` sorts by Unicode code point. The two orderings
differ exactly when a supplementary-plane character (whose UTF-16 encoding
begins with a high surrogate in ``U+D800..U+DBFF``) is compared against a BMP
character above ``U+DBFF``. The fixture contains such a pair:

===================  ===========  ==================  ===================
key                  code point   UTF-16 code units   sorts before ``Ｚ``?
===================  ===========  ==================  ===================
``U+1F600`` 😀       ``0x1F600``  ``D83D DE00``       UTF-16: yes
``U+FF3A``  Ｚ       ``0xFF3A``   ``FF3A``            code point: no
===================  ===========  ==================  ===================

**D2 — number serialization.** RFC 8785 §3.2.2.3 mandates the ECMAScript
``Number::toString`` algorithm. The fixture's three values each expose a
distinct disagreement with Python's float formatting:

==========  ==============  ==================
JSON input  RFC 8785 emits  ``json.dumps`` emits
==========  ==============  ==================
``1.0``     ``1``           ``1.0``
``-0.0``    ``0``           ``-0.0``
``1e-7``    ``1e-7``        ``1e-07``
==========  ==============  ==================

Scope: conformance only. Nothing here is wired into the production runtime,
serializer, hash or Merkle path.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
import rfc8785

from conformance.canonical import jcs, r1_conventional
from conformance.canonical.emit_ri_py_r1_artifact import build_artifact

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "r1-jcs-discriminating"
INPUT_PATH = CORPUS / "input.json"
ARTIFACT_PATH = CORPUS / "ri-py.json"

LEAF_DOMAIN = b"\x00"

#: The three fixture keys, by code point, so the test does not depend on the
#: source file of this module being read back in any particular encoding.
KEY_ASCII_A = "a"
KEY_FULLWIDTH_Z = "Ｚ"
KEY_GRINNING_FACE = "\U0001f600"


@pytest.fixture(scope="module")
def fixture_input() -> Any:
    return json.loads(INPUT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def canonical(fixture_input: Any) -> bytes:
    """Canonical bytes, produced by actually running the engine."""
    return jcs.canonical_bytes(fixture_input)


@pytest.fixture(scope="module")
def conventional(fixture_input: Any) -> bytes:
    return r1_conventional.conventional_bytes(fixture_input)


# ---------------------------------------------------------------------------
# fixture integrity — R1 only means something if the input really is the one
# described above
# ---------------------------------------------------------------------------


def test_fixture_contains_the_intended_discriminating_keys(fixture_input: Any) -> None:
    assert set(fixture_input) == {KEY_ASCII_A, KEY_FULLWIDTH_Z, KEY_GRINNING_FACE}

    # The supplementary-plane key must genuinely be outside the BMP, otherwise
    # the UTF-16 / code-point orderings could not disagree.
    assert ord(KEY_GRINNING_FACE) > 0xFFFF
    assert len(KEY_GRINNING_FACE.encode("utf-16-be")) == 4
    high_surrogate = int.from_bytes(KEY_GRINNING_FACE.encode("utf-16-be")[:2], "big")
    assert 0xD800 <= high_surrogate <= 0xDBFF

    # The BMP key must sort *after* that high surrogate but *before* the
    # supplementary code point. That inversion is the whole point.
    assert ord(KEY_FULLWIDTH_Z) > high_surrogate
    assert ord(KEY_FULLWIDTH_Z) < ord(KEY_GRINNING_FACE)


def test_fixture_numbers_are_not_plain_integers(fixture_input: Any) -> None:
    values = list(fixture_input.values())
    assert all(isinstance(v, float) for v in values), values
    assert fixture_input[KEY_ASCII_A] == 1.0
    assert str(fixture_input[KEY_FULLWIDTH_Z]) == "-0.0"
    assert fixture_input[KEY_GRINNING_FACE] == 1e-7


def test_fixture_file_key_order_is_not_canonical() -> None:
    """Ordering is the engine's job; the source file must not pre-sort."""
    raw = INPUT_PATH.read_text(encoding="utf-8")
    file_order = [
        k for k, _ in sorted(
            ((k, raw.index(json.dumps(k, ensure_ascii=False))) for k in
             (KEY_ASCII_A, KEY_FULLWIDTH_Z, KEY_GRINNING_FACE)),
            key=lambda kv: kv[1],
        )
    ]
    utf16_order = [KEY_ASCII_A, KEY_GRINNING_FACE, KEY_FULLWIDTH_Z]
    codepoint_order = [KEY_ASCII_A, KEY_FULLWIDTH_Z, KEY_GRINNING_FACE]
    assert file_order != utf16_order
    assert file_order != codepoint_order


# ---------------------------------------------------------------------------
# D1 — UTF-16 code-unit key ordering
# ---------------------------------------------------------------------------


def test_d1_jcs_orders_keys_by_utf16_code_unit(canonical: bytes) -> None:
    text = canonical.decode("utf-8")
    pos_a = text.index(f'"{KEY_ASCII_A}"')
    pos_emoji = text.index(f'"{KEY_GRINNING_FACE}"')
    pos_z = text.index(f'"{KEY_FULLWIDTH_Z}"')

    assert pos_a < pos_emoji < pos_z, (
        "RFC 8785 must order the supplementary-plane key before the BMP key "
        f"U+FF3A; got {text}"
    )


def test_d1_conventional_orders_keys_by_code_point(conventional: bytes) -> None:
    text = conventional.decode("utf-8")
    pos_a = text.index(f'"{KEY_ASCII_A}"')
    pos_emoji = text.index(f'"{KEY_GRINNING_FACE}"')
    pos_z = text.index(f'"{KEY_FULLWIDTH_Z}"')

    assert pos_a < pos_z < pos_emoji, (
        "json.dumps(sort_keys=True) is expected to order by code point; "
        f"got {text}"
    )


def test_d1_the_two_orderings_are_actually_inverted(
    canonical: bytes, conventional: bytes
) -> None:
    def order(data: bytes) -> list[str]:
        text = data.decode("utf-8")
        return sorted(
            (KEY_ASCII_A, KEY_FULLWIDTH_Z, KEY_GRINNING_FACE),
            key=lambda k: text.index(f'"{k}"'),
        )

    assert order(canonical) != order(conventional)


# ---------------------------------------------------------------------------
# D2 — ECMAScript number serialization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "jcs_form", "conventional_form"),
    [
        (1.0, b"1", b"1.0"),
        (-0.0, b"0", b"-0.0"),
        (1e-7, b"1e-7", b"1e-07"),
    ],
)
def test_d2_number_forms_disagree(
    value: float, jcs_form: bytes, conventional_form: bytes
) -> None:
    assert jcs.canonical_bytes(value) == jcs_form
    assert r1_conventional.conventional_bytes(value) == conventional_form
    assert jcs_form != conventional_form


def test_d2_number_forms_appear_in_the_fixture_output(
    canonical: bytes, conventional: bytes
) -> None:
    assert b":1," in canonical, "1.0 must canonicalize to 1"
    assert b":0}" in canonical, "-0.0 must canonicalize to 0"
    assert b":1e-7," in canonical

    assert b":1.0," in conventional
    assert b":-0.0," in conventional
    assert b":1e-07}" in conventional


# ---------------------------------------------------------------------------
# The R1 headline claim
# ---------------------------------------------------------------------------


def test_r1_is_discriminating(canonical: bytes, conventional: bytes) -> None:
    """JCS output MUST differ from the conventional serializer's output.

    If this ever passes trivially (i.e. the two agree), R1 has stopped being a
    discriminating fixture and MUST be redesigned. It is never acceptable to
    weaken this assertion.
    """
    assert canonical != conventional, (
        "R1 is NOT discriminating: RFC 8785 and "
        f"{r1_conventional.SERIALIZER} produced identical bytes"
    )
    assert len(canonical) != len(conventional)


def test_canonical_001_would_not_have_caught_this() -> None:
    """Characterisation: the CANONICAL-001 fixture is *not* discriminating.

    This is the gap R1 exists to close, asserted rather than asserted-about so
    that it cannot silently stop being true.
    """
    canonical_001 = json.loads(
        (REPO_ROOT / "conformance" / "corpus" / "canonical-001" / "input.json").read_text(
            encoding="utf-8"
        )
    )
    assert jcs.canonical_bytes(canonical_001) == r1_conventional.conventional_bytes(
        canonical_001
    )


# ---------------------------------------------------------------------------
# engine binding and adapter integrity
# ---------------------------------------------------------------------------


def test_adapter_is_a_direct_delegation_to_rfc8785(fixture_input: Any) -> None:
    assert jcs.ENGINE == "rfc8785"
    assert jcs.engine_version() == "0.1.4"
    assert jcs.canonical_bytes(fixture_input) == rfc8785.dumps(fixture_input)


def test_canonicalization_is_input_order_independent(fixture_input: Any) -> None:
    reordered = dict(reversed(list(fixture_input.items())))
    assert list(reordered) != list(fixture_input)
    assert jcs.canonical_bytes(reordered) == jcs.canonical_bytes(fixture_input)


# ---------------------------------------------------------------------------
# digests, recomputed from the produced bytes
# ---------------------------------------------------------------------------


def test_leaf_preimage_is_raw_0x00_followed_by_canonical_bytes(canonical: bytes) -> None:
    preimage = LEAF_DOMAIN + canonical
    assert preimage[0] == 0x00
    assert preimage[1:] == canonical
    assert len(preimage) == len(canonical) + 1


# ---------------------------------------------------------------------------
# the committed artifact must equal a live execution
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def committed() -> dict[str, Any]:
    return json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))


def test_committed_artifact_matches_live_execution(
    committed: dict[str, Any], canonical: bytes
) -> None:
    live = build_artifact()

    assert committed["canonical_bytes_hex"] == live["canonical_bytes_hex"]
    assert committed["canonical_bytes_hex"] == canonical.hex()
    assert committed["canonical_bytes_len"] == len(canonical)
    assert committed["sha256"] == hashlib.sha256(canonical).hexdigest()
    assert committed["leaf_sha256"] == hashlib.sha256(LEAF_DOMAIN + canonical).hexdigest()
    assert committed["engine"] == "rfc8785"
    assert committed["engine_version"] == "0.1.4"
    assert committed["leaf_domain"] == "0x00"


def test_committed_artifact_records_the_discrimination(
    committed: dict[str, Any], conventional: bytes
) -> None:
    disc = committed["discrimination"]
    assert disc["differs_from_jcs"] is True
    assert disc["conventional_bytes_hex"] == conventional.hex()
    assert disc["conventional_serializer"] == r1_conventional.SERIALIZER
    assert disc["conventional_bytes_hex"] != committed["canonical_bytes_hex"]
