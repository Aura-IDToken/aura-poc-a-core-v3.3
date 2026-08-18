# RI-PY JCS Conformance — Execution Evidence

Scope: RI-PY / DQ-006 — JCS-B01…B06 + CANONICAL-001.
Status: PASS (RI-PY execution evidence).

This document records real execution output. It is evidence, not a claim.

## Environment

| Item | Value |
| --- | --- |
| Repository | Aura-IDToken/aura-poc-a-core-v3.3 |
| Python | 3.11.15 (Linux x86_64) |
| pytest | 9.1.1 |
| Engine | `rfc8785` 0.1.4 |
| Engine location | `/usr/local/lib/python3.11/dist-packages/rfc8785/__init__.py` |
| Engine license | Apache-2.0 (Trail of Bits) |
| Engine dependencies | none |
| Engine scope | CONFORMANCE-ONLY (`conformance/requirements-conformance.txt`) |

## JCS boundary audit

`conformance/canonical/jcs.py` delegates directly:

```
canonical_bytes(value) -> rfc8785.dumps(value) -> bytes
```

Engine source audit (`rfc8785/_impl.py`, 254 lines) confirms a real RFC 8785
implementation rather than a `json.dumps` approximation:

- object members sorted on `key.encode("utf-16be")` (RFC 8785 §3.2.3), not on
  Unicode code points;
- ECMAScript `Number::toString` float serialisation (RFC 8785 §3.2.2.3);
- JSON short escapes plus lowercase `\uXXXX` for other control characters;
- non-ASCII emitted literally as UTF-8;
- integers outside the IEEE-754 safe domain rejected (`IntegerDomainError`);
- non-finite floats rejected (`FloatDomainError`).

## JCS-B01…B06

Command:

```
python -m pytest -q conformance/canonical/test_jcs_behavior.py
```

Result: `41 passed`.

| ID | Coverage | Result |
| --- | --- | --- |
| JCS-B01 | Property ordering; insertion-order independence; UTF-16 code-unit key sort | PASS |
| JCS-B02 | Nested objects; recursive member sort; array order preserved; no whitespace | PASS |
| JCS-B03 | Two-character escapes, `\uXXXX` control escapes, unescaped solidus, key escaping | PASS |
| JCS-B04 | Raw UTF-8 output, supplementary plane, no Unicode normalisation | PASS |
| JCS-B05 | ECMAScript number serialisation, `-0` → `0`, `1e-7`, safe-integer and non-finite rejection | PASS |
| JCS-B06 | `{}` / `[]`, nested empty containers, empty key and value | PASS |

### Adversarial negative control

The adapter was temporarily rewired to
`json.dumps(value, sort_keys=True, separators=(",", ":"))` and the suite re-run:

```
15 failed, 27 passed
```

The adapter was then restored. This demonstrates the suite is not vacuous — it
detects substitution of a non-JCS serializer.

Important secondary finding: under that substitution **CANONICAL-001 alone still
passed**, because its fixture (ASCII keys, string values, one small integer)
does not exercise any point where JCS and `json.dumps` diverge. CANONICAL-001 is
therefore necessary but *not sufficient* as JCS evidence; the B01…B06 suite
carries the discriminating power.

## CANONICAL-001

Command:

```
python -m pytest -q conformance/canonical/test_canonical_001.py
```

Result: `1 passed`.

Fixture:

```json
{"event_type":"AUDIT_RECORD","protocol_version":"1.0","schema_version":"1.0","payload":{"value":42}}
```

| Quantity | Actual (RI-PY execution) | Expected (RI-RS FROZEN) | Equal |
| --- | --- | --- | --- |
| canonical bytes (hex) | `7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f6164223a7b2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e30222c22736368656d615f76657273696f6e223a22312e30227d` | identical | PASS |
| SHA-256(canonical_bytes) | `b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6` | identical | PASS |
| SHA-256(0x00 ‖ canonical_bytes) | `ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039` | identical | PASS |

Canonical bytes decoded:

```
{"event_type":"AUDIT_RECORD","payload":{"value":42},"protocol_version":"1.0","schema_version":"1.0"}
```

Digests are computed from the bytes returned by the engine, not from the
published hex constant.

## Independent cross-check (secondary evidence)

Two paths independent of the RI-PY execution reproduce the same digests:

1. A hand-constructed canonical byte string, written directly from RFC 8785
   ordering and whitespace rules, is byte-identical to the engine output and
   yields the same SHA-256 and RFC-6962 leaf.
2. Digests recomputed from `bytes.fromhex(expected_hex)` — never touching the
   engine — match the expected SHA-256 and leaf.

This is corroboration only. It does not substitute for the RI-PY execution
recorded above.

## Test suite

| Suite | Result |
| --- | --- |
| `conformance/canonical/test_jcs_behavior.py` | 41 passed |
| `conformance/canonical/test_canonical_001.py` | 1 passed |
| `conformance/canonical/` | 42 passed |
| Full repository (`python -m pytest -q --continue-on-collection-errors`) | 160 passed, 3 errors, 5 subtests passed, 4 warnings |

The 3 errors are pre-existing and environmental, reproduced identically on the
unmodified baseline (changes stashed):

1. `core/test_ari_observability.py` — collection `NameError: name 'unittest' is
   not defined` (missing import in a production test module; unchanged by this
   work and out of scope).
2. `audit/test_audit_db_integration.py` — requires docker-compose PostgreSQL.
3. `core/test_cr003_statelessness.py` — requires docker-compose PostgreSQL.

Baseline (this work stashed): `1 failed, 118 passed, 3 errors`. The single
baseline failure was CANONICAL-001 itself, because the adapter imported a `jcs`
module that is not the approved engine and is not installed.

## Production integrity

`core/`, `audit/`, `audit/merkle.py`: unchanged (empty `git diff`). No
production hashing, Merkle, event-type, or protocol runtime semantics were
touched. All changes are confined to `conformance/`.
