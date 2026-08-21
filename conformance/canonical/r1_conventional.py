"""Conventional (non-JCS) JSON serializer — R1 discrimination evidence only.

This module exists so that R1 can *prove* that RFC 8785 JCS is not merely
"sorted, whitespace-free JSON". It serializes with the serializer a project
would reach for by reflex:

.. code-block:: python

    json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

.. danger::

   This is **evidence, not implementation**. It MUST NOT be used to produce
   canonical bytes, a digest, a Merkle leaf, or any protocol value. The only
   legitimate consumer is the R1 discrimination check, which asserts that the
   output of this function **differs** from the RFC 8785 output.

   The three production sites in this repository that already canonicalize with
   ``json.dumps(sort_keys=True, ...)`` (``audit/merkle.py``,
   ``compliance/certificate.py``, ``core/merkle.py``) are untouched by R1. R1
   characterises the gap; it does not repair it.
"""

from __future__ import annotations

import json
from typing import Any

#: Human-readable identity of the conventional serializer, recorded in evidence.
SERIALIZER = 'json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False)'


def conventional_bytes(value: Any) -> bytes:
    """Return the conventional ``json.dumps`` UTF-8 bytes for ``value``.

    Sorting here is by Unicode **code point** (Python's ``str`` ordering), and
    numbers are formatted by Python's ``repr``-derived float formatting. RFC 8785
    mandates neither: it sorts by UTF-16 **code unit** and formats numbers with
    the ECMAScript ``Number::toString`` algorithm. On the R1 fixture those two
    disagreements are observable in the emitted bytes.
    """
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
