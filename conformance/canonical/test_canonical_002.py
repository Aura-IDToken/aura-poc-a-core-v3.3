"""CANONICAL-002 — RI-PY execution of the JCS-discriminating fixture.

CANONICAL-001 is JCS-degenerate: an ordinary sorted-JSON serializer reproduces
its canonical bytes exactly, so a test that only checks CANONICAL-001 cannot
tell a conforming RFC 8785 engine from a non-conforming one. This module
exercises the properties where the two provably diverge, and asserts each one
against the bytes the engine actually produced.

Unlike ``test_canonical_001.py`` this file carries **no expected hex constant**.
CANONICAL-002's reference values were established by the RI-PY/RI-RS execution
round that produced the corpus artifacts; the frozen values live in
``conformance/corpus/canonical-002/manifest.json`` and are cross-checked by the
cross-language gate. Hardcoding them here would make a copied value
indistinguishable from an executed one.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from conformance.canonical.jcs import canonical_bytes

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / "conformance" / "corpus" / "canonical-002"
INPUT_PATH = CORPUS / "input.json"


@pytest.fixture(scope="module")
def fixture_input() -> Any:
    return json.loads(INPUT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def canonical(fixture_input: Any) -> bytes:
    """The only place canonical bytes come into existence in this module."""
    return canonical_bytes(fixture_input)


@pytest.fixture(scope="module")
def text(canonical: bytes) -> str:
    return canonical.decode("utf-8")


def test_output_is_utf8_bytes(canonical: bytes) -> None:
    assert isinstance(canonical, bytes)
    canonical.decode("utf-8")


def test_members_are_ordered_by_utf16_code_unit(text: str) -> None:
    """The property that separates RFC 8785 from any sorted-JSON serializer.

    ``U+10000`` encodes as the surrogate pair ``D800 DC00``, so its first UTF-16
    code unit (``0xD800``) is smaller than ``U+FB00`` and ``U+FFFF``. It must
    therefore sort *before* them, even though its code point is larger.
    """
    supplementary = text.index('"\U00010000"')
    ligature = text.index('"ﬀ"')
    bmp_max = text.index('"￿"')

    assert supplementary < ligature
    assert supplementary < bmp_max

    # The premise, verified rather than assumed: by code point the
    # supplementary key is the largest of the three...
    assert ord("\U00010000") > ord("￿") > ord("ﬀ")
    # ...but its first UTF-16 code unit is the smallest.
    assert "\U00010000".encode("utf-16-be")[:2] < "ﬀ".encode("utf-16-be")[:2]
    assert "\U00010000".encode("utf-16-be")[:2] < "￿".encode("utf-16-be")[:2]


def test_utf16_ordering_applies_recursively(text: str) -> None:
    """Nested members obey the same ordering, not just the top level."""
    alpha = text[text.index('"alpha":{') : text.index('"zebra"')]
    assert alpha.index('"m"') < alpha.index('"\U00010000"') < alpha.index('"￿"')


def test_non_ascii_is_raw_utf8(canonical: bytes, text: str) -> None:
    assert "é" in text
    assert "€" in text
    assert "\U0001f600" in text
    assert "ﬀ" in text
    # Raw UTF-8, never \u escapes.
    assert "\\u00e9" not in text
    assert "\\u20ac" not in text
    assert b"\xc3\xa9" in canonical
    assert b"\xe2\x82\xac" in canonical
    assert b"\xf0\x9f\x98\x80" in canonical


def test_ecmascript_number_serialisation(text: str) -> None:
    assert '"one_point_zero":1,' in text, "1.0 must serialise as 1"
    assert '"negative_zero":0,' in text, "-0.0 must normalise to 0"
    assert '"small_exponent":1e-7' in text, "1e-7 keeps exponent form, unpadded"
    assert '"exponent_boundary":0.000001' in text, "1e-6 becomes plain decimal"
    assert '"large_exponent":1e+21' in text, "1e21 becomes 1e+21"
    assert '"plain_integer":42' in text
    assert '"negative_fraction":-1.5' in text
    assert "-0.0" not in text, "negative zero must not survive canonicalisation"
    assert "1e-07" not in text, "exponents must not be zero-padded"


def test_array_order_is_preserved(text: str) -> None:
    """Array order is data. Only object members get canonicalised."""
    assert '"array_order":[3,1,2,{"x":2,"y":1},"c","a","b"]' in text
    assert '"inner_a":[9,8,7]' in text


def test_string_escaping_is_minimal(text: str) -> None:
    # The control character appears as the six-character escape
    # backslash-u-0-0-0-1, never as a raw octet.
    assert r"quote\" backslash\\ newline\n tab\t ctrl\u0001 solidus/ end" in text
    assert "\\/" not in text, "solidus must not be escaped"


def test_no_insignificant_whitespace(canonical: bytes, text: str) -> None:
    """Whitespace may appear only inside string literals."""
    in_string = False
    escaped = False
    for ch in text:
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        assert not ch.isspace(), f"insignificant whitespace {ch!r} outside a string"


def test_canonicalisation_is_input_order_independent(fixture_input: Any) -> None:
    """Reordering the input members must not change the canonical bytes."""
    reversed_top = dict(reversed(list(fixture_input.items())))
    assert canonical_bytes(reversed_top) == canonical_bytes(fixture_input)


def test_fixture_is_jcs_discriminating(fixture_input: Any, canonical: bytes) -> None:
    """The fixture must not be reproducible by an ordinary sorted-JSON dump.

    If this ever passes trivially, CANONICAL-002 has lost the only property that
    distinguishes it from CANONICAL-001 and the cross-language result would
    again prove agreement rather than RFC 8785 conformance.
    """
    naive = json.dumps(fixture_input, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    assert naive != canonical
    assert hashlib.sha256(naive).hexdigest() != hashlib.sha256(canonical).hexdigest()


def test_digests_are_computed_over_canonical_bytes(canonical: bytes) -> None:
    """Digest and leaf are derived from the produced bytes, in the right domain."""
    digest = hashlib.sha256(canonical).hexdigest()
    leaf = hashlib.sha256(b"\x00" + canonical).hexdigest()

    assert digest != leaf
    # The leaf preimage is exactly one raw octet longer than the bytes.
    assert hashlib.sha256(bytes([0x00]) + canonical).hexdigest() == leaf
    # Hashing the ASCII text "0x00" would be a different, wrong domain.
    assert hashlib.sha256(b"0x00" + canonical).hexdigest() != leaf
    # So would the wrong RFC 6962 domain.
    assert hashlib.sha256(b"\x01" + canonical).hexdigest() != leaf


def test_artifact_matches_live_execution(canonical: bytes) -> None:
    """The committed RI-PY artifact must match a fresh execution.

    This is what makes the corpus reproducible rather than merely present.
    """
    artifact = json.loads((CORPUS / "ri-py.json").read_text(encoding="utf-8"))
    assert artifact["canonical_bytes_hex"] == canonical.hex()
    assert artifact["canonical_bytes_len"] == len(canonical)
    assert artifact["sha256"] == hashlib.sha256(canonical).hexdigest()
    assert artifact["leaf_sha256"] == hashlib.sha256(b"\x00" + canonical).hexdigest()
