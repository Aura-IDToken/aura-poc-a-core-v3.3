from __future__ import annotations

from conformance.canonical.jcs import canonical_bytes


def test_jcs_b01_property_ordering() -> None:
    value = {"z": 1, "a": 2, "m": 3}
    assert canonical_bytes(value) == b'{"a":2,"m":3,"z":1}'


def test_jcs_b02_nested_objects() -> None:
    value = {"outer": {"z": 1, "a": {"y": 2, "b": 3}}}
    assert canonical_bytes(value) == b'{"outer":{"a":{"b":3,"y":2},"z":1}}'


def test_jcs_b03_strings_and_escaping() -> None:
    value = {"text": 'quote: "\\ newline:\n'}
    assert canonical_bytes(value) == b'{"text":"quote: \\\"\\\\ newline:\\n"}'


def test_jcs_b04_unicode() -> None:
    value = {"text": "Łódź — 日本語 — 😀"}
    assert canonical_bytes(value).decode("utf-8") == '{"text":"Łódź — 日本語 — 😀"}'


def test_jcs_b05_number_serialization() -> None:
    value = {"integer": 42, "negative": -7, "fraction": 1.5, "zero": 0}
    assert canonical_bytes(value) == b'{"fraction":1.5,"integer":42,"negative":-7,"zero":0}'


def test_jcs_b06_empty_values() -> None:
    value = {"array": [], "object": {}}
    assert canonical_bytes(value) == b'{"array":[],"object":{}}'
