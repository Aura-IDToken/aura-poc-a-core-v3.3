# INFRA-001 — Hash Domain Test Harness

**Type:** infrastructure. **Normative effect: NONE.**
**Date:** 2026-08-15
**Code repository:** `AuraIDToken/aura-guard-v1.3`, branch
`claude/auditentry-adapter-dq-001-h0os71`, commit **`9c6bc37`**
**Artifact repository:** this repository (the `review/` convention lives here)
**Production cryptographic semantics changed:** **NO** — `git diff` over tracked files is
empty; the commit adds new untracked test paths only.

---

## 1. Objective

Provide tooling that answers mechanically, for the constructions the repository
implements **today**:

1. What bytes does the implementation hash?
2. In what order are fields assembled?
3. What encoding is used?
4. What SHA-256 digest results?
5. Can the same bytes reproduce the same digest later?
6. Can the construction be replayed from a stored fixture?

The harness **observes**. It does not redefine, and it authorises nothing.

---

## 2. Existing hash constructions observed

Enumerated by reading `src/` directly (`grep -rn "Sha256::new\|Sha256::digest\|sha256_hex\|sha256_bytes_hex"`),
**not** carried from the D3-S8 figure. The result is **15 construction entries plus 2
primitives** — the earlier "13" counted distinct constructions and omitted repeat call
sites of the segment-chain construction and the `aura_seal` CLI digest.

| ID | Source | Algorithm | Input | Encoding | Status |
|---|---|---|---|---|---|
| `entry_chain_hash` | `src/chain.rs:25-49` | SHA-256 | 9 fields joined by `U+007C`: `prev_hash, decision, policy_set, policy_hash, context, input_hash, shadow_hash, seq, timestamp` | UTF-8 → lowercase hex | **OBSERVED** — HD-001 |
| `segment_chain_hash` | `src/segment.rs:91-118` | SHA-256 | 5 fields joined by `U+007C`: `prev_segment_chain_hash, merkle_root, first_seq, last_seq, sealed_at` | UTF-8 → lowercase hex | **OBSERVED** — HD-002 |
| `entry_genesis_hash` | `src/crypto.rs:22-29` | SHA-256 | literal `"AURA-GUARD-GENESIS-v1.3"` | UTF-8 → lowercase hex | **OBSERVED** — HD-003 |
| `segment_genesis_hash` | `src/segment.rs:46-50` | SHA-256 | literal `b"AURA-GUARD-SEGMENT-GENESIS-v1"` | raw bytes → lowercase hex | **OBSERVED** — HD-004 |
| `merkle_leaf_hash` | `src/merkle.rs:27-34` | SHA-256 | `0x00 \|\| data` | raw bytes | **OBSERVED** — HD-005 |
| `merkle_node_hash` | `src/merkle.rs:36-44` | SHA-256 | `0x01 \|\| left \|\| right` | raw bytes | **OBSERVED** — HD-006 |
| `merkle_empty_root` | `src/merkle.rs:46-50` | SHA-256 | empty input | raw bytes | **OBSERVED** — HD-007 |
| `policy_hash` | `src/policy.rs:188` | SHA-256 | raw policy file bytes | raw bytes → lowercase hex | **OBSERVED** — HD-008 |
| `input_hash` | `src/api/audit.rs:104-109` | SHA-256 | `context + " " + prompt + " " + response` | UTF-8 → lowercase hex | **OBSERVED** — HD-009 |
| `shadow_hash` | `src/api/audit.rs:108,110` | SHA-256 | `shadow_normalize(combined)` | UTF-8 → lowercase hex | **OBSERVED** — HD-010 |
| `tsa_message_imprint` | `src/segment.rs:120-132` | SHA-256 | **same preimage string as `segment_chain_hash`** | UTF-8 → 32 raw bytes | **OBSERVED** — HD-011 |
| `rfc3161_request_digest` | `src/rfc3161.rs:138` | SHA-256 | caller-supplied preimage; field order **UNKNOWN** (caller-determined) | raw bytes → 32 raw bytes | **NOT EXERCISED** — needs a live TSA |
| `tst_verify_digest_message_imprint` | `src/tst_verify.rs:657` | SHA-256 | TST-embedded bytes; order **UNKNOWN** | raw bytes | **NOT EXERCISED** — private parsing path |
| `tst_verify_digest_signed_attrs` | `src/tst_verify.rs:839` | SHA-256 | CMS signed attributes; order **UNKNOWN** (DER) | DER bytes | **NOT EXERCISED** — private CMS path |
| `aura_seal_cli_digest` | `src/bin/aura_seal.rs:500` | SHA-256 | segment preimage string | UTF-8 → 32 raw bytes | **NOT EXERCISED** — binary target |
| *primitive* `sha256_hex` | `src/crypto.rs:8-12` | SHA-256 | UTF-8 string | → lowercase hex | used by 4 constructions |
| *primitive* `sha256_bytes_hex` | `src/crypto.rs:16-20` | SHA-256 | raw bytes | → lowercase hex | used by 2 constructions |

---

## 3. Harness design

**Location.** `tests/hash_domains.rs` plus `tests/fixtures/hash_domains/`. The task
suggested `tests/hash_domains/`, but Rust integration tests are per-file crates under
`tests/`; a bare directory would not be compiled or run. The chosen layout matches the
repository's existing convention (`tests/golden.rs`, `tests/integration.rs`,
`tests/fixtures/tsa/`).

**No production seam was added.** Everything needed is already `pub`:
`chain::compute_chain_hash`, `crypto::{sha256_hex, sha256_bytes_hex, genesis_hash}`,
`merkle::{leaf_hash, node_hash, empty_root}`, `segment::{segment_genesis_hash,
SegmentManifest}`, `normalizer::shadow_normalize`.

**The one non-obvious problem, and how it was solved without touching production.**
`compute_chain_hash` builds its preimage into a function-local and returns only the
digest, so the entry-chain bytes are not directly exportable on `main`. Rather than add
an accessor to production, the harness **reconstructs** the preimage from the same nine
inputs and then **proves the reconstruction faithful**:

```
assert_eq!(sha256_hex(&reconstructed), compute_chain_hash(..));
```

If production ever changes its field set, ordering, separator or encoding, that equality
breaks and HD-001 fails. The reconstruction is therefore **self-validating**, not assumed
— which is what makes a zero-seam approach sound here.

**Fixture lifecycle.** Fixtures are committed. `HASH_DOMAINS_RECORD=1 cargo test --test
hash_domains` regenerates them; a normal run only reads and replays. A changed preimage
fails with a message stating that the harness does not authorise the change.

---

## 4. Fixture format

```json
{
  "fixture_id": "HD-001_entry_chain_preimage",
  "construction_id": "entry_chain_hash",
  "source_ref": "src/chain.rs:25-49 (compute_chain_hash); separator src/chain.rs:20",
  "status": "AS-IS IMPLEMENTATION BYTES — OBSERVED PREIMAGE",
  "not_canonical": "DQ-002 and DQ-006 unresolved; these bytes carry no specification standing.",
  "input_bytes_hex": "…",
  "input_length": 315,
  "input_utf8": "…",
  "sha256": "…"
}
```

`input_bytes_hex` is **authoritative for replay**; `input_utf8` is a convenience view and
is `null` when the preimage is not valid UTF-8 (e.g. HD-005/HD-006, which begin with a
`0x00`/`0x01` tag byte).

Every fixture carries the `status` and `not_canonical` fields, so the terminology
boundary travels with the data rather than living only in this document.

---

## 5. Replay results

**11 fixtures + 1 inventory generated. 17 tests, all passing.**

Replay chain per fixture: *stored hex → bytes → SHA-256 → must equal the stored digest
**and** the digest the implementation produces now.*

**Independent verification.** Four fixtures were additionally verified with an oracle
outside the Rust toolchain (Python `binascii` + GNU coreutils `sha256sum`):

| Fixture | Digest | External oracle |
|---|---|---|
| HD-001 entry chain preimage | `506549e15dad5fda9b498087b2f543d4425bcbcf6461eeced29e4ceadf0a2ecd` | **MATCH** |
| HD-002 segment chain preimage | `3495bd0749297644c7d5d1fd8036b0cd5fdf23993581f9374821516d31ed48ef` | **MATCH** |
| HD-005 merkle leaf | `422f11735dab4f6b2a478b9443903c2460dc24a7281190a8c5fe0172a6f6bfa1` | **MATCH** |
| HD-008 policy hash | `5e9ab2b25e6a748aeff8610b341f1ec9ba4b281df9e22304b1066fadf082b35d` | **MATCH** |

**Structural cross-check.** HD-001's observed preimage is **315 bytes** and contains the
same `prev_hash` (`b93b4ade…`) and `policy_hash` (`5e9ab2b2…`) values as the artifact on
the unmerged branch `d3/real-chain-observability`. The digests differ because this
harness uses a different prompt/response pair, so `input_hash` and `shadow_hash` differ —
exactly as expected. Same structure, same widths, same genesis, same policy digest,
independently re-derived.

**Observed implementation dependencies** — recorded as implementation facts only:

```
entry_chain_hash digest ──hex-decode 32 bytes──► merkle_leaf_hash   (src/segment.rs:135-148)
merkle root ──────────────────────────────────► segment_chain_hash (src/segment.rs:91-106)
segment_chain_hash preimage ──────────────────► tsa_message_imprint(src/segment.rs:120-132)
```

Two further observed properties, each with its own test:

- The entry and segment chains are seeded from **distinct** constants (HD-003 vs HD-004).
- Merkle leaf and node tags differ, so the same 32 bytes hash differently in each
  position.

Neither is presented as evidence of domain-separation adequacy; both are recorded
observations of the current code.

---

## 6. Negative test

Two, both **harness integrity checks only — not cryptographic security claims**:

| Test | Preimage type | Result |
|---|---|---|
| `negative_single_byte_change_alters_digest` | UTF-8 (HD-001 entry chain, 315 bytes) — low bit of the final byte flipped | digest changes ✔ |
| `negative_single_byte_change_alters_merkle_leaf_digest` | raw bytes (Merkle leaf input) | digest changes ✔ |

Covering both a UTF-8 and a raw-byte preimage proves the harness would notice a change in
either encoding regime.

---

## 7. Unknown / unobservable constructions

| Construction | Why not exercised | UNKNOWN properties |
|---|---|---|
| `rfc3161_request_digest` (`src/rfc3161.rs:138`) | Requires a live RFC 3161 TSA over the network; out of scope for a hermetic test | field order (caller-determined) |
| `tst_verify_digest_message_imprint` (`src/tst_verify.rs:657`) | Reached only through private TST parsing paths. Already covered behaviourally by `tests/tst_verify.rs` (9 tests, passing) | field order |
| `tst_verify_digest_signed_attrs` (`src/tst_verify.rs:839`) | Reached only through private CMS verification paths | field order (DER) |
| `aura_seal_cli_digest` (`src/bin/aura_seal.rs:500`) | Lives in a binary target, not the library surface | — |

Each is recorded in `INVENTORY.json` with `"exercised": false` and an explicit
`reason_not_exercised`. **No property was inferred**; where the source does not establish
one, the inventory says `UNKNOWN`.

---

## 8. Files changed

**`AuraIDToken/aura-guard-v1.3`** @ `9c6bc37` — 13 files, 1059 insertions, **all new**:

| File | Lines |
|---|---|
| `tests/hash_domains.rs` | 725 |
| `tests/fixtures/hash_domains/INVENTORY.json` | 213 |
| `tests/fixtures/hash_domains/HD-001…HD-011*.json` (11 files) | 11 each |

**`git diff --stat` over tracked files: empty.** No existing file was modified. Nothing
under `src/` was touched.

This repository: this artifact only.

---

## 9. Tests

| Metric | Value |
|---|---|
| Tests added | **17** |
| Tests passed | **17 / 17** in `--test hash_domains`; **257 / 257** across the full suite |
| Tests failed | **0** |
| Fixtures generated | **11** + 1 inventory |
| Constructions enumerated | **15** (+ 2 primitives) |
| Constructions exercised | **11** |
| Constructions not exercised | **4** (§7) |
| `cargo fmt --check` | clean |
| `cargo clippy --tests --all-targets` | clean — 0 errors, 0 warnings |

Suite before INFRA-001: 240 tests. After: 257.

---

## 10. DQ-002 boundary

> **INFRA-001 does not resolve DQ-002 and does not establish any normative hash-domain
> relationship.**

Concretely, the harness records that `entry_chain_hash` feeds `merkle_leaf_hash`, which
feeds `segment_chain_hash`, which feeds `tsa_message_imprint`. Those are **implementation
dependencies read out of the source**. The harness does **not** assert, and must not be
cited as evidence, that:

- `chain_hash` **is** `integrity_hash`;
- `event_payload_hash` feeds `integrity_hash`;
- any construction here corresponds to an APS-200 field;
- any observed byte sequence is canonical.

`integrity_hash`, `event_payload_hash` and `previous_record_hash` remain **unimplemented**
in this repository and are therefore absent from the harness. The fixtures are labelled
**AS-IS IMPLEMENTATION BYTES / OBSERVED PREIMAGE**, and the words *canonical*,
*normative*, *protocol-mandated*, *compliant* and *ENT-007* appear nowhere in the harness
except in this boundary statement.

The harness is **not evidence that the implementation conforms to APS-200.**

---

## 11. Final status

```
INFRA-001              = COMPLETE
DQ-002                 = UNCHANGED / CONFLICT
Architecture Decision  = NOT MADE
```

**Also unchanged:** DQ-001 (CONFLICT/OPEN), DQ-003…DQ-008, CONFLICT-DQ002-01,
CONFLICT-DQ006-01/02, CONFLICT-DQ008-01. No normative document was read for authority,
modified, or created. No ADR. No PR.
