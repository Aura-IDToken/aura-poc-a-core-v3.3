# CROSS-LANGUAGE-001 — CANONICAL-001 Execution Evidence

Scope: conformance only. No production runtime, hashing, Merkle core or
protocol semantics were modified in either repository.

## Protocol contract (frozen)

| Element | Value |
| --- | --- |
| Fixture | `CANONICAL-001` |
| Canonicalization | RFC 8785 JCS |
| Digest | `SHA-256(canonical_bytes)` |
| Leaf | `SHA-256(0x00 \|\| canonical_bytes)` (RFC 6962) |
| RI-PY engine | `rfc8785` 0.1.4 |
| RI-RS engine | `serde_json_canonicalizer` 0.3.2 |

Fixture input (`input.json`, SHA-256
`649bb748464ce78fe1a1d7104689d2dee736fb80777db6569592bc0d3d039261`), stored
byte-identically in both repositories:

```json
{
  "event_type": "AUDIT_RECORD",
  "protocol_version": "1.0",
  "schema_version": "1.0",
  "payload": {
    "value": 42
  }
}
```

## RI-PY — actual execution

| Field | Value |
| --- | --- |
| Repository | `Aura-IDToken/aura-poc-a-core-v3.3` |
| Branch | `claude/cross-language-canonical-001-n4v2c5` |
| Commit at execution | `49d0e4f67e90a7a47e9f067bfc42ab40ee59a56f` (clean worktree) |
| Python | CPython 3.11.15, Linux-6.18.5-fc-v20-x86_64-with-glibc2.39 |
| Engine | `rfc8785` 0.1.4 |
| Adapter | `conformance/canonical/jcs.py` (pure delegation to `rfc8785.dumps`) |

Commands:

```text
python -m pytest -q conformance/canonical/test_jcs_behavior.py     -> 13 passed
python -m pytest -q conformance/canonical/test_canonical_001.py    ->  1 passed
python -m conformance.canonical.emit_ri_py_artifact                -> ri-py.json
```

Observed values:

```text
canonical_bytes_hex = 7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f6164223a7b2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e30222c22736368656d615f76657273696f6e223a22312e30227d
canonical_bytes_len = 100
sha256              = b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6
leaf_sha256         = ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039
```

Artifact: `conformance/corpus/canonical-001/ri-py.json`
(file SHA-256 `6b5b5ccd54901181b9af45421d051ea5ea53096fbf632ab1e25a66705f2b856c`)

## RI-RS — actual execution

| Field | Value |
| --- | --- |
| Repository | `Aura-IDToken/aura-guard-v1.3` |
| Branch | `claude/cross-language-canonical-001-n4v2c5` |
| Commit at execution | `4e9e2284ccdac6d2f40e038e33b4eaeec847aaa2` (clean worktree) |
| Rust | `rustc 1.94.1 (e408947bf 2026-03-25)`, `cargo 1.94.1`, x86_64 linux |
| Engine | `serde_json_canonicalizer` 0.3.2 (resolved from `conformance/Cargo.lock`, checksum `fe52319a927259afbfa5180c5157cd8167edfd3e8c254f9558c7fef44c5649f2`) |
| Adapter | `conformance/canonical/jcs.rs` (pure delegation to `serde_json_canonicalizer::to_vec`) |

Command (run from `conformance/` in the RI-RS repository):

```text
cargo test --locked --test canonical_001    -> 4 passed; 0 failed
```

Observed values:

```text
canonical_bytes_hex = 7b226576656e745f74797065223a2241554449545f5245434f5244222c227061796c6f6164223a7b2276616c7565223a34327d2c2270726f746f636f6c5f76657273696f6e223a22312e30222c22736368656d615f76657273696f6e223a22312e30227d
canonical_bytes_len = 100
sha256              = b6c3660ce6dee498b37443a92bf87c5efead6fe863fcf19197c0baeda139a4e6
leaf_sha256         = ce6b36733d97699230f37d80a14e14104c19d2e787526a6fc3aaae6b6648c039
```

Artifact: written by the Rust test to
`conformance/corpus/canonical-001/ri-rs.json` in `aura-guard-v1.3`, then
transported byte-identically into this corpus. Both copies hash to
`a6ebad019118a7806ae927c4802a60056cb9e0c90f3cb1ef2a5e0cf359af329c`.

## Independence

The two artifacts were produced by separate toolchains, in separate
repositories, from separate JCS engines. Neither side reads the other:

* `emit_ri_py_artifact.py` imports only the RI-PY adapter. It reads no frozen
  reference constant and no RI-RS file.
* `canonical/test/canonical_001.rs` and `canonical/jcs.rs` reference no RI-PY
  value, path or artifact. The RI-RS artifact is written before its assertions
  run, so a divergence would have been recorded rather than suppressed.
* Neither artifact was edited after generation.

## Equality gate

Runner: `conformance/canonical/test_cross_language_canonical_001.py`.
It loads only `ri-py.json` and `ri-rs.json`. It imports no canonicalizer, does
not re-serialize `input.json`, and does not construct canonical bytes.

```text
python -m pytest -q conformance/canonical/test_cross_language_canonical_001.py
13 passed
```

| Check | Assertion | Result |
| --- | --- | --- |
| CHECK 1 | RI-PY `canonical_bytes_hex` == RI-RS `canonical_bytes_hex` | PASS |
| CHECK 2 | `SHA-256(decoded RI-PY bytes)` == RI-PY `sha256` | PASS |
| CHECK 3 | `SHA-256(decoded RI-RS bytes)` == RI-RS `sha256` | PASS |
| CHECK 4 | RI-PY `sha256` == RI-RS `sha256` | PASS |
| CHECK 5 | `SHA-256(0x00 \|\| RI-PY bytes)` == RI-PY `leaf_sha256` | PASS |
| CHECK 6 | `SHA-256(0x00 \|\| RI-RS bytes)` == RI-RS `leaf_sha256` | PASS |
| CHECK 7 | RI-PY `leaf_sha256` == RI-RS `leaf_sha256` | PASS |

Provenance guards also passed: the artifacts declare distinct implementations,
distinct repositories, distinct engines (`rfc8785` vs
`serde_json_canonicalizer`), and 40-hex-digit source commits.

## Secondary cross-check against the frozen reference values

Both artifacts equal the frozen CANONICAL-001 reference for all three values.
This is a secondary check; the primary gate remains RI-PY actual == RI-RS
actual.

## Negative controls

Runner: `conformance/canonical/negative_controls_canonical_001.py`. Each
control copies the committed corpus into a temporary directory, mutates the
copy, and runs the *real* gate against it via `AURA_CORPUS_DIR`.

```text
python -m conformance.canonical.negative_controls_canonical_001   -> exit 0
```

| Control | Mutation | Gate exit | Checks that fired | Result |
| --- | --- | --- | --- | --- |
| baseline | none | 0 | — | PASS (13 passed) |
| A | RI-RS `canonical_bytes_hex` final byte flipped | 1 | CHECK 1, 3, 6 | detected |
| B | RI-PY `sha256` first byte corrupted | 1 | CHECK 2, 4 | detected |
| C | both leaves recomputed under domain `0x01` | 1 | CHECK 5, 6 | detected |

Control C is the sharpest: because both leaves were mutated consistently,
CHECK 7 (leaf equality) still passed. Only the independent leaf recomputations
in CHECK 5 and CHECK 6 caught it — which is exactly the property those checks
exist to provide.

Committed corpus integrity after the controls (unchanged):

```text
649bb748464ce78fe1a1d7104689d2dee736fb80777db6569592bc0d3d039261  input.json
6b5b5ccd54901181b9af45421d051ea5ea53096fbf632ab1e25a66705f2b856c  ri-py.json
a6ebad019118a7806ae927c4802a60056cb9e0c90f3cb1ef2a5e0cf359af329c  ri-rs.json
```

No negative-control mutation remains in either repository.

## Production integrity

| Repository | Command | Result |
| --- | --- | --- |
| RI-PY | `git diff -- core/ audit/` | empty |
| RI-RS | `git diff -- src/ Cargo.toml Cargo.lock` | empty |

The RI-RS JCS engine is confined to a separate `conformance/` package with its
own workspace root and its own lockfile, so the production `aura-guard`
dependency graph does not gain a canonicalizer.

## Verdict

`CROSS-LANGUAGE-001: PASS` — RI-PY and RI-RS produce byte-identical CANONICAL-001
canonical bytes, SHA-256 and RFC 6962 leaf under independent execution.
