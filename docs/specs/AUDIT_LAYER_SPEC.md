# AUDIT_LAYER_SPEC — Normative Specification for the Aura Protocol Audit Layer

**Instrument:** Aura Protocol v3.3 Iron Core  
**Status:** FROZEN — normative  
**Layer:** Layer 1 (`audit/`)  
**Document version:** 1.0.0  
**Jurisdiction:** EU AI Act / Polish Regulatory Sandbox (MC-READY 2026)

---

## 0. Scope and Authority

This document is the **normative specification** for the Audit Layer of the Aura
Protocol deterministic measurement protocol.

The Audit Layer sits between:

- **Layer 0** (`core/`) — pure measurement (ARI calculation, no I/O)
- **Layer 2** (`compliance/`) — policy decisions and certificate rendering

The Audit Layer receives raw measurement outputs from Layer 0, constructs
cryptographic proofs of those outputs, and delivers verifiable Event Trust
Certificates (ETCs) to Layer 2 consumers.

Every paragraph in this document describes the **implementation exactly** as it
exists in `audit/merkle.py`, `audit/verify.py`, and `audit/signing.py`.

---

## 1. Canonical Event

### 1.1 Required Fields

A Canonical Event is a dictionary with exactly the following keys:

| Field      | Type   | Description                                         |
|------------|--------|-----------------------------------------------------|
| `agent_id` | string | MACHINE_ACCOUNT identifier (non-empty, UTF-8)       |
| `ari`      | int    | Agent Reliability Index (int32, scaled by 10^5)     |
| `drift`    | int    | Drift value (int32, scaled by 10^5)                 |

No additional fields may appear in the canonical serialization.

### 1.2 Serialization

Canonical serialization is **JSON** with the following constraints:

1. **Key order:** keys sorted lexicographically (Python `sort_keys=True`).
2. **Separators:** no extra whitespace — `,` between items, `:` between key and value.
3. **Encoding:** UTF-8, no BOM.
4. **Numbers:** integers represented as decimal digits without leading zeros.
5. **Strings:** standard JSON string escaping; no Unicode escapes unless required.

Canonical form example:

```
{"agent_id":"MACHINE_ACCOUNT_REF_001","ari":100000,"drift":0}
```

### 1.3 Ordering

When multiple events form a batch, they are ordered by the sequence in which
they were produced by Layer 0.  Insertion order is preserved and is part of the
immutable audit record.

---

## 2. Canonical Hash

### 2.1 Algorithm

**SHA-256** (FIPS 180-4).

SHA-256 is used exclusively throughout the Audit Layer.  No other hash
algorithm is permitted in this version of the instrument.

### 2.2 Canonical Payload

The canonical payload for an event hash is the **canonical serialization**
(§ 1.2) encoded as UTF-8 bytes.

```
payload = canonical_json(event).encode("utf-8")
hash    = sha256(payload).hexdigest()          # 64 hex characters
```

### 2.3 Hash Procedure

1. Construct the Canonical Event dictionary (§ 1.1).
2. Serialize to canonical JSON (§ 1.2).
3. Encode the resulting string as UTF-8 bytes.
4. Apply SHA-256 to the byte sequence.
5. Represent the digest as a lowercase hexadecimal string of exactly 64 characters.

Implementation reference: `audit/merkle.py :: sha256(data: str) -> str`

```python
def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
```

---

## 3. Append-Only Event Log

### 3.1 Allowed Operations

| Operation | Description                                  |
|-----------|----------------------------------------------|
| `append`  | Add a new event hash to the end of the log.  |
| `read`    | Read any event hash by index.                |

### 3.2 Forbidden Operations

| Operation | Reason                                                        |
|-----------|---------------------------------------------------------------|
| `delete`  | Violates immutability; destroys audit trail.                  |
| `update`  | Destroys bit-identity; invalidates existing Merkle proofs.    |
| `reorder` | Changes Merkle tree structure; invalidates all existing proofs.|
| `truncate`| Equivalent to mass delete; forbidden.                         |

### 3.3 Integrity Guarantees

The Merkle root (§ 4) commits to the complete, ordered set of event hashes in
the log at any point in time.  Any modification to any event — including
deletion, reordering, or substitution — produces a different Merkle root and is
therefore detectable by any party holding the original root.

---

## 4. Merkle Tree

### 4.1 Construction

The Merkle tree is built from a list of leaf hashes (one per event).

```
Level 0 (leaves): [h0, h1, h2, h3, ...]
Level 1:          [sha256(h0 + h1), sha256(h2 + h3), ...]
...
Root:             sha256(left + right)
```

Concatenation uses raw hex strings: `sha256(left_hex + right_hex)`.

**Single-leaf degenerate case:** When the tree has exactly one leaf, the root
equals the leaf hash (no pairing step is executed).

Implementation reference: `audit/merkle.py :: MerkleTree._build_tree`

### 4.2 Odd-Leaf Handling

When a level has an **odd number of nodes**, the last node is paired with
**itself**:

```
parent = sha256(last_node + last_node)
```

This rule propagates up every level until the root.

Implementation reference: `audit/merkle.py :: MerkleTree._build_tree` lines
`right = current_level[i + 1] if i + 1 < len(current_level) else left`.

### 4.3 Proof Format

A Merkle proof for leaf at index `i` is a list of `(sibling_hash, direction)`
tuples, one per level from the leaf up to (but not including) the root.

`direction` values:

| Value    | Meaning                                              |
|----------|------------------------------------------------------|
| `"left"` | The sibling is on the left; compute `sha256(sibling + current)`. |
| `"right"`| The sibling is on the right; compute `sha256(current + sibling)`. |

Example:

```json
[
  {"sibling": "abc123...", "direction": "right"},
  {"sibling": "def456...", "direction": "left"}
]
```

Implementation reference: `audit/merkle.py :: MerkleTree.get_proof`

### 4.4 Verification Algorithm

Given `leaf_hash`, `proof`, and `expected_root`:

```
current = leaf_hash
for (sibling, direction) in proof:
    if direction == "left":
        current = sha256(sibling + current)
    else:
        current = sha256(current + sibling)
return current == expected_root
```

Implementation reference: `audit/merkle.py :: verify_proof` and
`audit/verify.py :: verify_proof`.

---

## 5. Event Trust Certificate (ETC)

### 5.1 Normative Schema

An ETC is a structured record with the following fields:

| Field           | Type                       | Required | Description                            |
|-----------------|----------------------------|----------|----------------------------------------|
| `event_hash`    | string (64 hex chars)      | yes      | SHA-256 hash of the canonical event    |
| `merkle_root`   | string (64 hex chars)      | yes      | Merkle root of the event batch         |
| `merkle_proof`  | list of `{sibling, direction}` | yes  | Proof path from leaf to root           |
| `timestamp`     | string (ISO-8601)          | yes      | Timestamp of event batch creation      |
| `batch_id`      | string or null             | no       | Optional identifier for the event batch|

### 5.2 Field Definitions

**`event_hash`**  
The SHA-256 hash of the canonical event serialization (§ 2).
This field uniquely identifies the event and is the leaf of the Merkle tree.

**`merkle_root`**  
The root hash of the Merkle tree constructed from the batch of events
containing this event.  Any party with this value and the proof can verify
the event is part of the batch without access to other events.

**`merkle_proof`**  
An ordered list of `{sibling: <hex>, direction: <"left"|"right">}` objects
as defined in § 4.3.  The proof is self-contained and sufficient for
independent verification.

**`timestamp`**  
ISO-8601 datetime string (e.g., `2026-07-24T20:56:30Z`) indicating when the
ETC was issued.  This field is not part of the canonical event hash and is
not committed to by the Merkle root.  It is informational only.

**`batch_id`**  
Optional opaque string identifying the batch.  May be null.

### 5.3 Versioning

ETCs issued by Aura Protocol v3.3 Iron Core are identified by the instrument
version `v3.3`.  Any change to the ETC schema creates a new instrument
version, not a new ETC version.

### 5.4 Serialization

ETCs are serialized to dictionaries via `EventTrustCertificate.to_dict()`:

```json
{
  "event_hash": "<64 hex chars>",
  "merkle_root": "<64 hex chars>",
  "merkle_proof": [
    {"sibling": "<64 hex chars>", "direction": "left|right"},
    ...
  ],
  "timestamp": "<ISO-8601>",
  "batch_id": "<string or null>"
}
```

Implementation reference: `audit/merkle.py :: EventTrustCertificate.to_dict`

---

## 6. Signature

### 6.1 Current Implementation: HMAC-SHA256

The Audit Layer uses **HMAC-SHA256** as its signing algorithm.

Implementation reference: `audit/signing.py :: HMACSigner` / `HMACVerifier`

### 6.2 Signing Payload

The signing payload is the UTF-8-encoded canonical JSON serialization of the
ETC dictionary (§ 5.4), with keys sorted and no extra whitespace:

```python
payload = json.dumps(etc.to_dict(), sort_keys=True, separators=(",", ":"))
         .encode("utf-8")
signature = hmac_signer.sign(payload)
```

### 6.3 Signature Encoding

The signature is a lowercase hexadecimal string of exactly 64 characters
(the HMAC-SHA256 digest).

### 6.4 Verification Process

```python
payload  = json.dumps(etc.to_dict(), sort_keys=True, separators=(",", ":"))
           .encode("utf-8")
is_valid = hmac_verifier.verify(payload, claimed_signature)
```

Verification uses `hmac.compare_digest` (constant-time) to prevent
timing-oracle attacks.

### 6.5 Key Requirements

| Property         | Requirement                                |
|------------------|--------------------------------------------|
| Format           | Raw bytes (not hex or base64)              |
| Minimum length   | 1 byte (enforced by HMACSigner constructor)|
| Recommended length | 32 bytes (256 bits) or longer            |
| Storage          | Outside this repository (secure store)    |
| Rotation         | Creates a new instrument instance; requires re-signing all ETCs |

### 6.6 Signing Abstraction

The signing API is defined by two abstract base classes:

```python
class Signer(ABC):
    def sign(self, payload: bytes) -> str: ...
    def algorithm(self) -> str: ...

class Verifier(ABC):
    def verify(self, payload: bytes, signature: str) -> bool: ...
    def algorithm(self) -> str: ...
```

**Current implementation:** `HMACSigner` / `HMACVerifier` (HMAC-SHA256).

**Future migration path:** `FutureEd25519Signer` / `FutureEd25519Verifier` stubs
are provided in `audit/signing.py`.  They raise `NotImplementedError` and are
not intended for production use in v3.3.  Introducing Ed25519 requires a new
instrument version.

---

## 7. Independent Verification

Any party with the following inputs can verify an ETC without access to the
original system:

**Required inputs:**
1. The canonical event (§ 1) — `agent_id`, `ari`, `drift`
2. The ETC (§ 5)
3. The HMAC key (§ 6.5) — for signature verification only

### 7.1 Step-by-Step Verification Algorithm

```
Step 1. Recompute the event hash
        payload = canonical_json(event).encode("utf-8")
        computed_event_hash = sha256(payload)

Step 2. Compare event hash
        IF computed_event_hash != etc.event_hash → FAIL

Step 3. Replay the Merkle proof
        current = etc.event_hash
        FOR (sibling, direction) IN etc.merkle_proof:
            IF direction == "left":
                current = sha256(sibling + current)
            ELSE:
                current = sha256(current + sibling)

Step 4. Compare Merkle root
        IF current != etc.merkle_root → FAIL

Step 5. Verify signature (requires HMAC key)
        payload  = canonical_json(etc.to_dict()).encode("utf-8")
        expected = HMAC-SHA256(key, payload)
        IF NOT constant_time_compare(expected, claimed_signature) → FAIL

Step 6. Return PASS
```

### 7.2 PASS Criteria

All of the following must hold:

- `computed_event_hash == etc.event_hash`
- Merkle proof replays to `etc.merkle_root`
- HMAC signature matches (when key is available)

### 7.3 FAIL Criteria

Any of the following causes FAIL:

| Condition                          | Interpretation                            |
|------------------------------------|-------------------------------------------|
| `computed_event_hash != etc.event_hash` | Event data has been modified.        |
| Merkle replay ≠ `etc.merkle_root`  | Proof is invalid or root is incorrect.    |
| Signature mismatch                 | Certificate has been tampered with or the wrong key was used. |
| Any field missing from ETC         | Incomplete / malformed certificate.       |

---

## 8. Reference Implementation

| Component            | File                         |
|----------------------|------------------------------|
| SHA-256 hash         | `audit/merkle.py :: sha256`  |
| Merkle tree          | `audit/merkle.py :: MerkleTree` |
| Merkle proof         | `audit/merkle.py :: verify_proof` |
| Event Trust Certificate | `audit/merkle.py :: EventTrustCertificate` |
| Proof verification   | `audit/verify.py :: verify_proof` |
| ETC verification     | `audit/verify.py :: verify_etc` |
| Signing abstraction  | `audit/signing.py`           |
| Current signer       | `audit/signing.py :: HMACSigner` |
| Future signer (stub) | `audit/signing.py :: FutureEd25519Signer` |

---

## 9. Determinism Guarantee

All operations defined in this specification are deterministic:

- SHA-256 is a pure function with no platform-dependent behaviour.
- JSON serialization with `sort_keys=True` and fixed separators is deterministic.
- HMAC-SHA256 with a fixed key and payload is deterministic.
- Integer arithmetic (ARI, drift) uses Python's arbitrary-precision integers;
  there is no floating-point in Layer 0 or Layer 1 at runtime.

Cross-platform verification is performed in CI on x86_64 and ARM64.
Results are compared by `scripts/compare_determinism_reports.py`.
WASM compatibility is verified by `WASMCompatibilityTest` in
`core/test_bitwise_replay.py` (operational confirmation pending native WASM
runtime integration; this is an architectural goal for a future instrument version).

---

*Document version: 1.0.0 — frozen with Aura Protocol v3.3 Iron Core*
