# R1-JCS-DISCRIMINATING — Conformance Contract

Status: **PASS (executed, cross-language)**

Scope: conformance only. No production runtime, serializer, hashing, Merkle core
or protocol semantics were modified in either reference implementation. R1 does
**not** close DQ-006 or DQ-002 and does not authorise wiring JCS into the
production path.

## Why R1 exists

CANONICAL-001 established that both reference implementations *can* execute an
RFC 8785 engine. It did not establish that RFC 8785 was *required*, because its
fixture is not discriminating:

```json
{"event_type":"AUDIT_RECORD","protocol_version":"1.0","schema_version":"1.0","payload":{"value":42}}
```

Every key is ASCII and the only number is a small integer, so

```text
RFC 8785 JCS  ==  json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False)
RFC 8785 JCS  ==  serde_json::to_vec
```

byte-for-byte. **A non-JCS implementation passes CANONICAL-001.** That is
measured, not asserted — see the wrong-engine control in
`corpus/r1-jcs-discriminating/EXECUTION-EVIDENCE.md`, where substituting a
conventional serializer leaves CANONICAL-001 fully green in both languages while
R1 fails in both.

## Contract

```text
JSON object
    -> RFC 8785 JCS
    -> canonical UTF-8 bytes
    -> SHA-256(canonical_bytes)
    -> SHA-256(0x00 || canonical_bytes)      (RFC 6962 leaf domain)
```

Identical to CANONICAL-001. Only the fixture changes.

## Fixture

`conformance/corpus/r1-jcs-discriminating/input.json`
(SHA-256 `64b737306d2421092cd9f28a5deb525437100c788ab7c39891aaf6b61cd472ca`),
stored byte-identically in both repositories:

```json
{
  "Ｚ": -0.0,
  "a": 1.0,
  "😀": 1e-7
}
```

Three keys, three numbers, 27 canonical bytes. The file's own key order is
non-canonical under *both* candidate orderings, so ordering remains the engine's
job rather than the fixture's.

### D1 — UTF-16 code-unit key ordering (RFC 8785 §3.2.3)

RFC 8785 sorts object keys by UTF-16 code unit. Conventional serializers sort by
Unicode code point (Python `str` ordering; `serde_json`'s `BTreeMap<String, _>`
UTF-8 byte ordering, which is equivalent). The two disagree exactly when a
supplementary-plane key meets a BMP key above `U+DBFF`:

| key | code point | UTF-16 code units | first sort unit |
| --- | --- | --- | --- |
| `😀` `U+1F600` GRINNING FACE | `0x1F600` | `D83D DE00` | `0xD83D` |
| `Ｚ` `U+FF3A` FULLWIDTH LATIN CAPITAL LETTER Z | `0xFF3A` | `FF3A` | `0xFF3A` |

`0xD83D < 0xFF3A`, so JCS emits `😀` **first**. `0xFF3A < 0x1F600`, so code-point
sorting emits it **last**. The orderings are inverted, not merely different.

### D2 — ECMAScript `Number::toString` (RFC 8785 §3.2.2.3)

| JSON input | RFC 8785 | Python `json.dumps` | `serde_json::to_vec` |
| --- | --- | --- | --- |
| `1.0` | `1` | `1.0` | `1.0` |
| `-0.0` | `0` | `-0.0` | `-0.0` |
| `1e-7` | `1e-7` | `1e-07` | `1e-7` |

D1 and D2 are independent: repairing one leaves the other detecting a
substituted engine.

## Observed values

Produced by execution, never written by hand. Cross-language identical.

```text
canonical_bytes (UTF-8)  {"a":1,"😀":1e-7,"Ｚ":0}
canonical_bytes (hex)    7b2261223a312c22f09f9880223a31652d372c22efbcba223a307d
canonical_bytes_len      27
SHA-256(canonical)       a8c01577f4cc4ef73b258cbe66da0103b009fdd88be480c0b811ff2c1ad0946c
SHA-256(0x00||canonical) fb988d990e39fa4f2f35f9158aaa9bac88aad84add3aaf47fb27426eb450656d
```

Conventional (non-JCS) serializations of the same input, recorded as
discrimination evidence and never hashed:

```text
Python json.dumps   {"a":1.0,"Ｚ":-0.0,"😀":1e-07}   33 bytes
serde_json::to_vec  {"a":1.0,"Ｚ":-0.0,"😀":1e-7}    32 bytes
```

Note that the two conventional serializers do not even agree with *each other*.
Only the RFC 8785 outputs converge.

## No external oracle

CANONICAL-001's expected values came from aura-specification. R1 has no such
oracle: RFC 8785 output for this input is defined by the standard, and the only
honest way to obtain it is to run a conforming engine. R1's reference values are
therefore the **recorded consensus of two independent executions** — RI-PY
`rfc8785` 0.1.4 and RI-RS `serde_json_canonicalizer` 0.3.2 — and
`emit_r1_manifest.py` refuses to write a manifest unless that consensus already
holds and both digests recompute from the bytes.

Consequently the R1 gate has no compare-against-a-frozen-constant stage that
could pass on its own. The primary gate is the only gate: RI-PY actual == RI-RS
actual, with every digest recomputed from the bytes each side produced.

## Engines

| Implementation | Repository | Engine | Version | Isolation |
| --- | --- | --- | --- | --- |
| RI-PY | `Aura-IDToken/aura-poc-a-core-v3.3` | `rfc8785` | `0.1.4` | `conformance/requirements-conformance.txt`, never installed into the production runtime |
| RI-RS | `Aura-IDToken/aura-guard-v1.3` | `serde_json_canonicalizer` | `=0.3.2` | `[dev-dependencies]` only |

Both adapters are byte-identical to the ones CANONICAL-001 uses. R1 introduces
no second canonicalization implementation:

```text
conformance/canonical/jcs.py  sha256 8f6c3b440221113721a82c6ff3ff61dcfbaccbcbe972ce7ae635d00444b8b5a4
conformance/canonical/jcs.rs  sha256 cab24c297a4a989e7423e6f0f0c85bbe05ed508dc67fe59a64cdef194a2a9f12
```

## Runners

| Gate | Command |
| --- | --- |
| RI-PY execution + discrimination | `python -m pytest -q conformance/canonical/test_r1_jcs_discriminating.py` |
| RI-RS execution + discrimination | `cargo test --locked --test r1_jcs_discriminating` (aura-guard-v1.3) |
| Cross-language equality | `python -m pytest -q conformance/canonical/test_cross_language_r1.py` |
| Negative controls A–E | `python -m conformance.canonical.negative_controls_r1` |
| Artifact emission | `python -m conformance.canonical.emit_ri_py_r1_artifact` |
| Manifest emission | `python -m conformance.canonical.emit_r1_manifest` |

## Boundaries

* `core/`, `audit/` and `compliance/` are **not** modified. The three
  incompatible `json.dumps` canonicalization sites recorded in the repository's
  own baseline audit (`audit/merkle.py:85`, `compliance/certificate.py:69`,
  `core/merkle.py:8`) remain exactly as they were. R1 characterises the gap
  between them and RFC 8785; it does not repair it.
* `conformance/canonical/r1_conventional.py` is **evidence, not
  implementation**. Its only legitimate consumer is the assertion that its
  output *differs* from RFC 8785.
* In RI-RS, `src/` and `Cargo.lock` are unchanged. `Cargo.toml` gains a
  `[[test]]` target registration and nothing else — neither `[dependencies]` nor
  `[dev-dependencies]` is touched.
* R1 does not demonstrate that the production runtime is RFC 8785 conformant. It
  demonstrates that the *conformance boundary* is, on an input where that claim
  has content.

See `conformance/corpus/r1-jcs-discriminating/EXECUTION-EVIDENCE.md` for the
executions, commands, artifacts, negative controls and the JCS-B01…B06 coverage
audit that motivated the fixture design.
