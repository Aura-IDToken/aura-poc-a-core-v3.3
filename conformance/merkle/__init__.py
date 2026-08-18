"""RI-PY DQ-002 Merkle conformance surface.

Scope
-----
CONFORMANCE ONLY. This package is the RI-PY reference implementation of the
DQ-002 normative Merkle hash domain (RFC 6962). It is deliberately separate
from the production audit path.

`audit/merkle.py` implements a different, legacy Merkle contract (UTF-8 string
leaves, hexadecimal-text node concatenation, duplicated odd nodes). That module
is NOT modified here. Per ADR-CK003-DQ002-HASH-DOMAIN "Compatibility and
migration rule", existing evidence MUST retain its original algorithm identity,
so historical roots may not be silently recomputed under the RFC 6962 domain.
Migrating the production audit path is a separate, gated action that requires
the ADR to be APPROVED and a version/profile boundary to be defined.
"""
