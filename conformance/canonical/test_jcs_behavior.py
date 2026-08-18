"""Behavioural conformance of the RI-PY JCS boundary (RFC 8785).

These tests characterise the *engine* rather than the CANONICAL-001 fixture.
They exist so that a silent engine substitution or a silent engine upgrade
cannot pass unnoticed underneath the CANONICAL-001 execution evidence.
"""

from __future__ import annotations

import pytest
import rfc8785

from conformance.canonical import jcs
from conformance.canonical.jcs import canonical_bytes


def test_engine_binding_is_frozen() -> None:
    """The frozen protocol contract binds RI-PY to rfc8785 0.1.4."""
    assert jcs.ENGINE == "rfc8785"
    assert jcs.engine_version() == "0.1.4"


def test_adapter_delegates_directly_to_engine() -> None:
    """The adapter must be a pass-through, not a re-implementation."""
    obj = {"z": 1, "a": {"n": [1, 2, 3]}}
    assert canonical_bytes(obj) == rfc8785.dumps(obj)


def test_output_is_utf8_bytes() -> None:
    data = canonical_bytes({"k": "v"})
    assert isinstance(data, bytes)
    data.decode("utf-8")


def test_object_keys_are_sorted_by_utf16_code_unit() -> None:
    assert canonical_bytes({"b": 1, "a": 2, "C": 3}) == b'{"C":3,"a":2,"b":1}'


def test_no_insignificant_whitespace() -> None:
    data = canonical_bytes({"a": [1, 2], "b": {"c": 3}})
    assert data == b'{"a":[1,2],"b":{"c":3}}'
    assert b" " not in data
    assert b"\n" not in data


def test_array_order_is_preserved() -> None:
    assert canonical_bytes([3, 1, 2]) == b"[3,1,2]"


def test_integers_are_emitted_without_exponent_or_fraction() -> None:
    assert canonical_bytes({"value": 42}) == b'{"value":42}'
    assert canonical_bytes(0) == b"0"
    assert canonical_bytes(-1) == b"-1"


def test_es6_number_serialisation() -> None:
    assert canonical_bytes(1.0) == b"1"
    assert canonical_bytes(1.5) == b"1.5"
    assert canonical_bytes(1e21) == b"1e+21"


def test_non_finite_numbers_are_rejected() -> None:
    with pytest.raises(rfc8785.CanonicalizationError):
        canonical_bytes(float("nan"))
    with pytest.raises(rfc8785.CanonicalizationError):
        canonical_bytes(float("inf"))


def test_string_escaping_is_minimal() -> None:
    assert canonical_bytes('a"b\\c') == b'"a\\"b\\\\c"'
    assert canonical_bytes("\n") == b'"\\n"'
    assert canonical_bytes("\u0001") == b'"\\u0001"'


def test_non_ascii_is_emitted_as_raw_utf8() -> None:
    assert canonical_bytes("é") == '"é"'.encode("utf-8")
    assert canonical_bytes("€") == '"€"'.encode("utf-8")


def test_literals() -> None:
    assert canonical_bytes(True) == b"true"
    assert canonical_bytes(False) == b"false"
    assert canonical_bytes(None) == b"null"


def test_canonicalisation_is_input_order_independent() -> None:
    a = {"event_type": "AUDIT_RECORD", "payload": {"value": 42}}
    b = {"payload": {"value": 42}, "event_type": "AUDIT_RECORD"}
    assert canonical_bytes(a) == canonical_bytes(b)
