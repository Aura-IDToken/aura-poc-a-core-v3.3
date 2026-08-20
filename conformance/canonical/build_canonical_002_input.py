"""Generate the frozen CANONICAL-002 fixture input.

CANONICAL-002 is the JCS-*discriminating* counterpart to CANONICAL-001.
CANONICAL-001 is JCS-degenerate: an ordinary sorted-JSON serializer reproduces
its canonical bytes exactly, so agreement on it cannot distinguish a conforming
RFC 8785 engine from a non-conforming one. CANONICAL-002 exists to remove that
ambiguity.

Every element below is present because RFC 8785 requires something an ordinary
``json.dumps(obj, sort_keys=True, separators=(",", ":"))`` does not do:

======  ==========================================================  =========================================
Case    Property exercised                                          Why a naive serializer diverges
======  ==========================================================  =========================================
A       Member ordering by UTF-16 code unit                         Naive sorts by code point, so the two
                                                                    supplementary-plane keys land after
                                                                    U+FB00/U+FFFF instead of before them
B       Non-ASCII emitted as raw UTF-8                              Naive defaults to ``ensure_ascii=True``
                                                                    and emits ``\\uXXXX``
C       ECMAScript number form: ``1.0`` -> ``1``                    Naive emits ``1.0``
D       Negative zero normalises to ``0``                           Naive emits ``-0.0``
E       Exponent form: ``1e-7`` -> ``1e-7``, ``1e-6`` -> plain      Naive emits ``1e-07`` / ``1e-06``
F       Recursive canonicalisation of nested members                (ordering, applied at depth)
G       Array element order preserved, never sorted                 (a serializer that sorts arrays diverges)
H       Minimal string escaping; solidus NOT escaped                (a serializer that escapes ``/`` diverges)
======  ==========================================================  =========================================

This script only writes the fixture *input*. It computes no canonical bytes and
no digests. The expected canonical form is whatever the frozen engines produce
when they are executed against this file.

Member order here is deliberately NON-canonical: keys are emitted in an order
that no correct canonicalizer would preserve, so an engine that merely echoes
its input cannot pass.

Usage::

    python -m conformance.canonical.build_canonical_002_input
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "conformance" / "corpus" / "canonical-002" / "input.json"

# Keys chosen so that UTF-16 code-unit order differs from code-point order.
#
#   key          code point   UTF-16 code units   code-point rank   UTF-16 rank
#   "z"          U+007A       007A                1                 1
#   "é"     U+00E9       00E9                2                 2
#   "€"     U+20AC       20AC                3                 3
#   "ﬀ"     U+FB00       FB00                4                 6
#   "￿"     U+FFFF       FFFF                5                 7
#   "\U00010000" U+10000      D800 DC00           6                 4
#   "\U0001f600" U+1F600      D83D DE00           7                 5
#
# The two supplementary-plane keys sort LAST by code point and MIDDLE by UTF-16
# code unit. That single difference is enough to separate RFC 8785 from any
# sorted-JSON serializer.
FIXTURE: dict[str, object] = {
    # -- deliberately non-canonical input order ---------------------------
    "￿": "key_u_ffff",
    "strings": {
        "escapes": 'quote" backslash\\ newline\n tab\t ctrl\u0001 solidus/ end',
        "unicode": "eacute é euro € emoji \U0001f600 bmp ﬀ",
    },
    "z": "key_ascii_z",
    "numbers": {
        "one_point_zero": 1.0,
        "negative_zero": -0.0,
        "small_exponent": 1e-7,
        "exponent_boundary": 1e-6,
        "large_exponent": 1e21,
        "plain_integer": 42,
        "negative_fraction": -1.5,
    },
    "\U0001f600": "key_u_1f600",
    "array_order": [3, 1, 2, {"y": 1, "x": 2}, "c", "a", "b"],
    "ﬀ": "key_u_fb00",
    "nested": {
        "zebra": {"inner_z": 1, "inner_a": [9, 8, 7]},
        "alpha": {"￿": True, "\U00010000": False, "m": None},
    },
    "\U00010000": "key_u_10000",
    "é": "key_u_00e9",
    "€": "key_u_20ac",
    "protocol_version": "1.0",
    "schema_version": "1.0",
    "event_type": "AUDIT_RECORD",
}


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # ensure_ascii=True keeps the committed fixture pure ASCII, so the file is
    # unambiguous under any editor, terminal or diff tool. The *parsed* value is
    # what both engines canonicalize, so this choice cannot affect the result.
    # indent=2 and the scrambled key order above keep the input visibly
    # non-canonical.
    text = json.dumps(FIXTURE, indent=2, ensure_ascii=True, sort_keys=False) + "\n"
    OUTPUT_PATH.write_text(text, encoding="utf-8")

    raw = OUTPUT_PATH.read_bytes()
    print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"bytes      : {len(raw)}")
    print(f"sha256     : {hashlib.sha256(raw).hexdigest()}")
    print(f"top members: {len(FIXTURE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
