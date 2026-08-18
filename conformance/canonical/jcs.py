"""Isolated RFC 8785 JCS adapter for protocol conformance only.

This module deliberately does not modify the production hash/Merkle core.
"""

from __future__ import annotations

from typing import Any

import rfc8785


def canonical_bytes(value: Any) -> bytes:
    """Return RFC 8785 JCS UTF-8 bytes for a JSON-compatible value."""
    return rfc8785.dumps(value)
