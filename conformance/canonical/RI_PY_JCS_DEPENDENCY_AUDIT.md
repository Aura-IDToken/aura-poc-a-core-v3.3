# RI-PY JCS Dependency Audit

## Decision

Use `rfc8785==0.1.4` as the **conformance-only** JCS engine for RI-PY.

Do not introduce the dependency into production Core runtime.

## Rationale

The RI-PY boundary requires an implementation of RFC 8785 that emits raw UTF-8 canonical bytes. The adapter must delegate canonicalization to the RFC 8785 engine rather than reconstructing JCS with `json.dumps(sort_keys=True)` or equivalent heuristics.

`rfc8785` is selected as the dedicated RFC 8785 implementation for the conformance boundary. Its API returns canonical UTF-8 bytes directly, matching the protocol boundary contract:

`canonical object -> RFC 8785 JCS -> canonical bytes`

## Repository Scope

The dependency is used only by `conformance/canonical/jcs.py` and the associated conformance tests.

No changes are made to `core/`, `audit/merkle.py`, production hashing, Merkle semantics, event semantics, or protocol runtime behavior.

## Version Policy

Exact version pin:

`rfc8785==0.1.4`

No floating dependency range is permitted for the conformance fixture execution.

## Verification Required

Before RI-PY CANONICAL-001 receives a PASS, the execution environment must verify:

1. the installed package is exactly version `0.1.4`;
2. the import resolves to the intended package;
3. the engine executes RFC 8785 canonicalization;
4. JCS boundary tests JCS-B01 through JCS-B06 pass;
5. CANONICAL-001 produces the frozen canonical bytes, SHA-256 digest, and RFC-6962 leaf digest;
6. the production Core remains unchanged.

## Status

**APPROVED — dependency decision.**

This document does not itself constitute RI-PY conformance evidence. The execution evidence is produced by the JCS behavior suite and CANONICAL-001 test run.
