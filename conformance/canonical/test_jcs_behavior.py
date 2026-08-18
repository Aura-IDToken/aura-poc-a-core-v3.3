"""RI-PY JCS behaviour conformance suite (JCS-B01 ... JCS-B06).

Every test drives the engine forward:

    JSON-compatible object -> canonical_bytes() -> actual bytes -> comparison

Expected values are derived from RFC 8785 itself, never from engine output that
is then fed back into the assertion. Several cases deliberately assert that the
canonical form differs from what ``json.dumps`` would produce, so that a silent
substitution of a non-JCS serializer fails the suite.
"""

from __future__ import annotations

import importlib.metadata
import json

import pytest

import rfc8785
from conformance.canonical.jcs import canonical_bytes

APPROVED_ENGINE = "rfc8785"
APPROVED_VERSION = "0.1.4"


def test_engine_is_the_approved_rfc8785_pin() -> None:
    """The adapter must delegate to rfc8785==0.1.4 and return raw UTF-8 bytes."""
    assert importlib.metadata.version(APPROVED_ENGINE) == APPROVED_VERSION
    assert canonical_bytes({"a": 1}) is not None
    assert canonical_bytes({"a": 1}) == rfc8785.dumps({"a": 1})
    assert isinstance(canonical_bytes({"a": 1}), bytes)


# ---------------------------------------------------------------------------
# JCS-B01 - property ordering
# ---------------------------------------------------------------------------


def test_jcs_b01_property_order_is_independent_of_insertion_order() -> None:
    """RFC 8785 3.2.3: object members are sorted, not emitted in input order."""
    inserted_forward = {"a": 1, "b": 2, "c": 3}
    inserted_reverse = {"c": 3, "b": 2, "a": 1}
    inserted_shuffled = {"b": 2, "a": 1, "c": 3}

    expected = b'{"a":1,"b":2,"c":3}'

    assert canonical_bytes(inserted_forward) == expected
    assert canonical_bytes(inserted_reverse) == expected
    assert canonical_bytes(inserted_shuffled) == expected


def test_jcs_b01_keys_are_sorted_by_utf16_code_units() -> None:
    """RFC 8785 3.2.3 sorts on UTF-16 code units, not on Unicode code points.

    For a supplementary-plane key (U+10000 -> surrogate pair D800 DC00) versus
    U+FFFF the two orderings disagree, so this discriminates a real JCS engine
    from a code-point sort such as ``json.dumps(sort_keys=True)``.
    """
    obj = {"￿": 1, "\U00010000": 2}

    canonical = canonical_bytes(obj)

    assert canonical == '{"\U00010000":2,"￿":1}'.encode("utf-8")
    assert canonical != json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def test_jcs_b01_ordering_is_not_locale_or_length_dependent() -> None:
    assert canonical_bytes({"b": 1, "A": 2, "": 3, "aa": 4, "a": 5}) == b'{"":3,"A":2,"a":5,"aa":4,"b":1}'


# ---------------------------------------------------------------------------
# JCS-B02 - nested objects
# ---------------------------------------------------------------------------


def test_jcs_b02_nested_objects_are_canonicalised_recursively() -> None:
    value = {
        "z": {"b": [1, {"y": 2, "x": 3}], "a": 1},
        "a": {},
    }

    assert canonical_bytes(value) == b'{"a":{},"z":{"a":1,"b":[1,{"x":3,"y":2}]}}'


def test_jcs_b02_array_order_is_preserved_while_members_are_sorted() -> None:
    """RFC 8785 3.2.3: arrays keep their order; only object members are sorted."""
    value = {"list": [{"b": 1, "a": 2}, {"d": 3, "c": 4}]}

    assert canonical_bytes(value) == b'{"list":[{"a":2,"b":1},{"c":4,"d":3}]}'
    assert canonical_bytes([3, 1, 2]) == b"[3,1,2]"


def test_jcs_b02_deep_nesting_has_no_insignificant_whitespace() -> None:
    value = {"a": {"b": {"c": {"d": [{"f": False, "e": True, "g": None}]}}}}

    assert canonical_bytes(value) == b'{"a":{"b":{"c":{"d":[{"e":true,"f":false,"g":null}]}}}}'


# ---------------------------------------------------------------------------
# JCS-B03 - string escaping
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ('a"b', b'"a\\"b"'),
        ("back\\slash", b'"back\\\\slash"'),
        ("tab\there", b'"tab\\there"'),
        ("nl\nhere", b'"nl\\nhere"'),
        ("cr\rhere", b'"cr\\rhere"'),
        ("ff\fhere", b'"ff\\fhere"'),
        ("bs\bhere", b'"bs\\bhere"'),
        ("", b'""'),
    ],
)
def test_jcs_b03_two_character_escapes(value: str, expected: bytes) -> None:
    """RFC 8785 3.2.2.2: the short escape forms are mandatory where they exist."""
    assert canonical_bytes(value) == expected


def test_jcs_b03_other_control_characters_use_lowercase_hex_u_escapes() -> None:
    assert canonical_bytes("\u0001") == b'"\\u0001"'
    assert canonical_bytes("\u001f") == b'"\\u001f"'


def test_jcs_b03_solidus_and_printables_are_not_escaped() -> None:
    """RFC 8785 3.2.2.2 does not escape '/', and leaves printable ASCII literal."""
    assert canonical_bytes("a/b") == b'"a/b"'
    assert canonical_bytes("plain text 123") == b'"plain text 123"'


def test_jcs_b03_escaping_applies_to_object_keys_too() -> None:
    assert canonical_bytes({'k"1': "v\nx"}) == b'{"k\\"1":"v\\nx"}'


# ---------------------------------------------------------------------------
# JCS-B04 - Unicode / UTF-8
# ---------------------------------------------------------------------------


def test_jcs_b04_output_is_raw_utf8_bytes_not_ascii_escapes() -> None:
    """RFC 8785 3.2.2.2: non-ASCII is emitted literally, encoded as UTF-8."""
    canonical = canonical_bytes({"k": "é€"})

    assert isinstance(canonical, bytes)
    assert canonical == b'{"k":"\xc3\xa9\xe2\x82\xac"}'
    assert canonical.decode("utf-8") == '{"k":"é€"}'
    # json.dumps defaults to \uXXXX escaping, which is not the canonical form.
    assert canonical != json.dumps({"k": "é€"}, separators=(",", ":")).encode("utf-8")


def test_jcs_b04_supplementary_plane_is_encoded_as_four_utf8_bytes() -> None:
    canonical = canonical_bytes("\U0001f600")

    assert canonical == b'"\xf0\x9f\x98\x80"'
    assert canonical.decode("utf-8") == '"\U0001f600"'


def test_jcs_b04_unicode_is_not_normalised_by_the_engine() -> None:
    """RFC 8785 canonicalises serialisation, not Unicode composition."""
    precomposed = "é"  # é
    decomposed = "é"  # e + combining acute

    assert canonical_bytes(precomposed) == b'"\xc3\xa9"'
    assert canonical_bytes(decomposed) == b'"e\xcc\x81"'
    assert canonical_bytes(precomposed) != canonical_bytes(decomposed)


# ---------------------------------------------------------------------------
# JCS-B05 - number serialisation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        # ECMAScript number-to-string drops a redundant fraction: 1.0 -> "1".
        (1.0, b"1"),
        (100.0, b"100"),
        # RFC 8785 3.2.2.3: negative zero serialises as "0".
        (-0.0, b"0"),
        (0.0, b"0"),
        # Exponent form has no zero padding: 1e-07 (Python repr) -> "1e-7".
        (1e-7, b"1e-7"),
        (1e21, b"1e+21"),
        (1e30, b"1e+30"),
        (0.1, b"0.1"),
        (333333333.33333329, b"333333333.3333333"),
        (42, b"42"),
        (-42, b"-42"),
    ],
)
def test_jcs_b05_number_serialisation_follows_ecmascript_rules(value: object, expected: bytes) -> None:
    assert canonical_bytes(value) == expected


@pytest.mark.parametrize("value", [1.0, 100.0, -0.0, 1e-7])
def test_jcs_b05_diverges_from_plain_json_serialisation(value: float) -> None:
    """These are exactly the values where json.dumps is not RFC 8785."""
    assert canonical_bytes(value) != json.dumps(value).encode("utf-8")


def test_jcs_b05_integers_outside_the_safe_domain_are_rejected() -> None:
    """RFC 8785 3.2.2.3 restricts numbers to the IEEE-754 double domain."""
    assert canonical_bytes(2**53 - 1) == b"9007199254740991"
    with pytest.raises(rfc8785.IntegerDomainError):
        canonical_bytes(2**53)


def test_jcs_b05_non_finite_numbers_are_rejected() -> None:
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(rfc8785.FloatDomainError):
            canonical_bytes(value)


# ---------------------------------------------------------------------------
# JCS-B06 - empty object / array
# ---------------------------------------------------------------------------


def test_jcs_b06_empty_object_and_array() -> None:
    assert canonical_bytes({}) == b"{}"
    assert canonical_bytes([]) == b"[]"


def test_jcs_b06_empty_containers_nested_in_a_document() -> None:
    assert canonical_bytes({"b": [], "a": {}}) == b'{"a":{},"b":[]}'
    assert canonical_bytes([[], {}, [{}]]) == b'[[],{},[{}]]'


def test_jcs_b06_empty_string_key_and_value() -> None:
    assert canonical_bytes({"": ""}) == b'{"":""}'
