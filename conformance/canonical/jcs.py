"""Isolated RFC 8785 JCS adapter for protocol conformance only.

This module deliberately does not modify the production hash/Merkle core.

Scope
-----
CONFORMANCE ONLY. ``rfc8785`` MUST NOT be introduced into the production Core
runtime (``core/``, ``audit/``). The adapter is a thin delegation boundary: it
performs no canonicalization of its own and MUST NOT be replaced by
``json.dumps(sort_keys=True)`` or any other approximation of RFC 8785.
"""

from __future__ import annotations

from typing import Any

import rfc8785


def canonical_bytes(value: Any) -> bytes:
    """Return RFC 8785 JCS UTF-8 bytes for a JSON-compatible value.

    Delegates directly to the approved RFC 8785 engine (``rfc8785==0.1.4``).
    """
    return rfc8785.dumps(value)
