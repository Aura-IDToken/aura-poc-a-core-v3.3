# CROSS-LANGUAGE-002 — RI-PY Remediation

## Scope

Remediate the Python Merkle implementation to the DQ-002 normative contract without changing the specification, `main`, or unrelated audit semantics.

## Normative target

- Leaf: `SHA-256(0x00 || canonical_bytes)`
- Interior node: `SHA-256(0x01 || left_digest || right_digest)`
- Child digests are raw 32-byte values.
- Tree shape follows RFC 6962; an unpaired node is promoted, not duplicated.
- Canonical serialization is external to this module and follows the DQ-006 JCS decision.

## Current gate

CROSS-LANGUAGE-002 remains OPEN until RI-PY and RI-RS execute the same fixture and independently agree on leaf, node, root, and proof verification results.

## Constraint

This remediation branch MUST NOT modify `aura-specification`, DQ-002 decision text, or `main`.
