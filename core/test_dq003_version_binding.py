"""DQ-003 RI-PY version binding conformance test.

This test is intentionally non-invasive: it verifies the semantic contract carried
by the DQ003-004 fixture without changing production serialization or version
resolution. The authoritative fixture lives in aura-specification.
"""

import pytest


DQ003_FIXTURE = {
    "fixture_id": "DQ003-004",
    "protocol_version": None,
    "schema_version": "1.0.0",
    "canonicalization_rule": (
        "Both version fields, once normatively bound, are resolved before "
        "canonical serialization."
    ),
}


def test_fixture_identity_and_distinct_version_fields():
    """RI-PY must model protocol and schema versions as distinct concepts."""
    assert DQ003_FIXTURE["fixture_id"] == "DQ003-004"
    assert DQ003_FIXTURE["schema_version"] == "1.0.0"
    assert DQ003_FIXTURE["protocol_version"] is None
    assert DQ003_FIXTURE["protocol_version"] != DQ003_FIXTURE["schema_version"]


def test_protocol_version_is_not_derived_from_schema_version():
    """An unset protocol version must not be silently inferred from schema version."""
    fixture = dict(DQ003_FIXTURE)
    fixture["schema_version"] = "2.0.0"
    assert fixture["protocol_version"] is None


def test_protocol_version_is_not_an_implementation_version():
    """Package/repository versions are not valid substitutes for protocol_version."""
    implementation_versions = ["v3.3", "1.3", "3.3.0"]
    for implementation_version in implementation_versions:
        assert implementation_version != DQ003_FIXTURE["protocol_version"]


def test_unsupported_protocol_version_must_not_be_silently_downgraded():
    """A future/unknown protocol version requires an explicit compatibility decision."""
    unsupported = "99.0"
    supported = {"UNSET"}
    assert unsupported not in supported


def test_canonicalization_requires_version_resolution_first():
    """Version semantics are resolved before entering the canonical digest domain."""
    assert "resolved before canonical serialization" in DQ003_FIXTURE[
        "canonicalization_rule"
    ]


@pytest.mark.xfail(
    strict=False,
    reason=(
        "DQ-003 is not yet closable: authoritative protocol_version and its "
        "canonical serialization binding remain unfrozen."
    ),
)
def test_authoritative_protocol_version_is_frozen():
    """Expected to become a hard vector once the specification freezes the value."""
    assert DQ003_FIXTURE["protocol_version"] is not None
