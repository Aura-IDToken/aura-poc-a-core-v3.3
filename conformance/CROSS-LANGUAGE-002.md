# RI-PY CROSS-LANGUAGE-002 Conformance — DQ-002 Merkle Hash Domain

**Status:** CONDITIONAL PASS (RI-PY execution evidence recorded below).

**Full evidence ledger:**
`aura-specification` → `ck003/dq-002-hash-domain/CROSS-LANGUAGE-002-EVIDENCE.md`

This document is the RI-PY-side summary. It does not approve
`ADR-CK003-DQ002-HASH-DOMAIN` (status: PROPOSED) and does not close DQ-002.

## What was required

RI-PY must implement the DQ-002 normative Merkle contract identically to RI-RS:

```
leaf  : SHA-256(0x00 || canonical_bytes)
node  : SHA-256(0x01 || left_digest_raw_32 || right_digest_raw_32)
empty : SHA-256("")
shape : RFC 6962 recursive split at the largest power of two strictly < n;
        unpaired node promoted unchanged, never duplicated
bytes : raw 32-byte digests at every hash boundary; hexadecimal text is never
        a hash input
```

## What RI-PY had

`audit/merkle.py` implements a different contract:

| Aspect | `audit/merkle.py` | DQ-002 |
| --- | --- | --- |
| leaf | `SHA-256(UTF-8(leaf_string))` — no domain prefix (`merkle.py:16`) | `SHA-256(0x00 ‖ bytes)` |
| node | `SHA-256(UTF-8(left_hex + right_hex))` (`merkle.py:163`) | `SHA-256(0x01 ‖ raw ‖ raw)` |
| odd nodes | duplicated: `right = left` (`merkle.py:162`) | promoted unchanged |
| shape | pairwise level-by-level | RFC 6962 recursive split |
| digest form | hexadecimal `str` throughout | raw `bytes` |
| empty tree | `ValueError` (`merkle.py:138`) | `SHA-256("")` |

Every one of the six rows is a GAP. It is not a partially conformant
implementation; it is a different algorithm.

## What was changed, and what deliberately was not

**Added:** `conformance/merkle/` — an RI-PY implementation of the DQ-002
contract, with its conformance suite, vector emitter, and frozen cross-language
evidence.

**Not changed:** `audit/merkle.py`, `core/merkle.py`, and every existing
production call site.

That restraint is required, not incidental. `ADR-CK003-DQ002-HASH-DOMAIN`
states: *"Existing evidence MUST retain its original algorithm identity. No
historical digest may be recomputed and presented as unchanged evidence."* It
also states the ADR *"does not authorize immediate changes to RI-PY or RI-RS"*.
The CK-003 workspace rule adds: *"No production implementation change is
implied by a CK-003 evidence artifact."*

Rewriting `audit/merkle.py` in place would silently reinterpret every
historical ETC root under a new domain — exactly the migration hazard the ADR
names. Migrating the production audit path is a separate, gated action
requiring the ADR to be APPROVED and a version/profile boundary to be defined.

`test_dq002_rfc6962.py::test_legacy_audit_merkle_root_differs_from_dq002_root`
pins the divergence so it cannot be erased by accident.

## Direction of evidence

Expected values come from a **third** implementation, not from RI-PY:

| Producer | Implementation | Role |
| --- | --- | --- |
| Oracle | GNU coreutils `sha256sum` (`ck003/dq-002-hash-domain/tools/rfc6962_oracle.sh`) | produces expected roots and audit paths |
| RI-PY | CPython `hashlib` | asserted against the oracle |
| RI-RS | Rust `sha2` crate | asserted against the oracle |

An RI-PY bug cannot mask itself, because RI-PY never supplies its own expected
values.

## Executable evidence

| File | Covers |
| --- | --- |
| `conformance/merkle/rfc6962.py` | the DQ-002 primitive |
| `conformance/merkle/test_dq002_rfc6962.py` | domains, byte discipline, tree shape, N = 0…8, proofs, NC-1…NC-10 |
| `conformance/merkle/test_cross_language_002.py` | RI-PY ≡ RI-RS equality gate |
| `conformance/merkle/emit_vectors.py` | RI-PY half of the cross-language vector set |
| `conformance/merkle/evidence/RI-RS-VECTORS.json` | frozen RI-RS emission (pinned by digest) |
| `conformance/merkle/fixtures/` | vendored DQ-002 fixtures (pinned by digest) |

## Execution

```
$ python3 -m pytest -q conformance/merkle/
158 passed in 0.11s                                          exit 0
```

```
$ python3 -m pytest -q
1 error in 0.24s                                             exit 2
```

Bare collection fails on a **pre-existing** defect unrelated to DQ-002:
`core/test_ari_observability.py:211` uses `unittest.TestCase` while importing
only `from unittest import mock`. Present at HEAD `a7f4d2a2`, untouched here.
Not fixed in this change — see `DEFECT-DQ002-F3.md` in aura-specification.

```
$ python3 -m pytest -q --ignore=core/test_ari_observability.py
319 passed, 4 warnings, 2 errors, 5 subtests passed in 0.91s exit 1
```

0 failed. Both errors are environmental: `audit/test_audit_db_integration.py`
and `core/test_cr003_statelessness.py` need a Docker daemon
(`pgvector/pgvector:pg16`), absent on this runner. Those suites are
**NOT EXECUTED**, not failed.

| Item | Value |
| --- | --- |
| Python | 3.11.15 |
| pytest | 9.1.1 |
| Platform | Linux x86_64, Ubuntu 24.04.4 LTS |
| Commit under test | `a7f4d2a219e3153a084b74716054a0e4a4379a28` + this change |
| CI execution | NOT EXECUTED — local runner only |

## Result

RI-PY's DQ-002 vector set is identical to RI-RS's across canonical input bytes,
leaf hashes, internal node hashes, roots for N = 0…8, all 36 audit paths, and
the complete verification decision matrix including every negative control.
Both match the independent oracle.

Three findings remain open and are why this is CONDITIONAL PASS, not PASS:
`DEFECT-DQ002-F1` (wrong digest recorded in a fixture marked
`NORMATIVE_TEST_VECTOR`, deliberately left uncorrected), `DEFECT-DQ002-F2`
(DQ-002 silent on tree-size binding), `DEFECT-DQ002-F3` (this repository's
suite cannot be collected without `--ignore`). No CI run exists. The ADR is
still `PROPOSED`.

**DQ-002 remains OPEN.**
