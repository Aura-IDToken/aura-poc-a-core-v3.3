"""Isolated RFC 8785 JCS adapter for protocol conformance only.

This module deliberately does not modify the production hash/Merkle core.

Engine binding is frozen by the CANONICAL-001 protocol contract:
RI-PY canonical bytes are produced by ``rfc8785`` 0.1.4 and by nothing else.
The adapter is a direct delegation: it performs no pre-normalisation,
no post-processing and no byte construction of its own.
"""

from __future__ import annotations

from typing import Any

import rfc8785

#: Engine identity, recorded verbatim in CANONICAL-001 execution artifacts.
ENGINE = "rfc8785"


def engine_version() -> str:
    """Return the installed version of the frozen JCS engine."""
    from importlib.metadata import version

    return version(ENGINE)


def canonical_bytes(value: Any) -> bytes:
    """Return RFC 8785 JCS UTF-8 bytes for a JSON-compatible value."""
    return rfc8785.dumps(value)
