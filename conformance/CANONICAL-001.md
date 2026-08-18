# RI-PY CANONICAL-001 Conformance

Status: PASS (executed)

The RI-PY JCS boundary now exists at `conformance/canonical/jcs.py`, bound by the
frozen protocol contract to `rfc8785==0.1.4` (pinned in
`conformance/requirements-conformance.txt`). It is conformance-scoped and does not
touch the production hash/Merkle core.

This test MUST execute the exact CANONICAL-001 object from aura-specification.

Required outputs:
1. canonical_bytes_hex
2. SHA-256(canonical_bytes)
3. SHA-256(0x00 || canonical_bytes)

Expected independent oracle:
- canonical_bytes_hex = 7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f6164223a7b2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e30222c22736368656d615f76657273696f6e223a22312e30227d
- SHA-256(canonical_bytes) = b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6
- leaf = ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039

A PASS requires equality of all three values. If the Core has no RFC 8785 JCS boundary, the result MUST remain BLOCKED.


## Execution status

RI-PY executes CANONICAL-001 via `conformance/canonical/test_canonical_001.py`
and all three required outputs equal the independent oracle above.

Cross-language equality against RI-RS (`Aura-IDToken/aura-guard-v1.3`,
`serde_json_canonicalizer` 0.3.2) is established by CROSS-LANGUAGE-001. See
`conformance/corpus/canonical-001/EXECUTION-EVIDENCE.md` for the execution
evidence, artifacts and negative controls.
