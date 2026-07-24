# AUDIT LAYER SPECIFICATION
## Aura Protocol v3.3 Iron Core — Normative Specification

**Document Status:** NORMATIVE  
**Version:** 1.0.0  
**Layer:** 1 (audit/)  
**Jurisdiction:** EU AI Act / Polish Regulatory Sandbox (MC-READY 2026)  
**Author:** Aura Protocol Custodian  
**Last Frozen:** 2026-07-24  

---

> **Constitutional Note**  
> This specification describes the Audit Layer of the Aura Protocol
> deterministic measurement protocol exactly as implemented in
> `audit/merkle.py`, `audit/verify.py`, and `audit/signing.py`.
> Implementation is the source of truth.
> If this document conflicts with the implementation, the implementation
> governs and this document must be corrected.

---

## 1. Canonical Event

### 1.1 Definition

A **Canonical Event** is a deterministic, UTF-8 encoded string
representation of a single measurement event produced by the
Aura Protocol core engine (Layer 0).

### 1.2 Required Fields

A Canonical Event string **MUST** include the following fields in the
order specified, separated by the `|` character:

| Position | Field         | Type        | Description                                  |
|----------|---------------|-------------|----------------------------------------------|
| 1        | `agent_id`    | string      | MACHINE_ACCOUNT identifier (no human IDs)    |
| 2        | `ari`         | int32       | Agent Reliability Index (scaled by 10^5)     |
| 3        | `drift`       | int32       | Semantic drift (scaled by 10^5)              |
| 4        | `ts`          | ISO-8601    | Event timestamp (UTC, no timezone offset)    |

**Example:**

```
agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000|ts=2026-01-01T00:00:00Z
```

### 1.3 Serialisation

- Encoding: **UTF-8** (mandatory)
- Field separator: `|`
- Key-value separator: `=`
- No trailing newline
- No leading or trailing whitespace
- Field order is fixed as specified in §1.2

### 1.4 Ordering

Events within a batch are ordered by the sequence in which they were
appended to the log.  The first appended event is leaf 0 in the
Merkle tree.

---

## 2. Canonical Hash

### 2.1 Algorithm

**SHA-256** as defined in FIPS 180-4.

Python reference implementation (`audit/merkle.py`):

```python
import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
```

### 2.2 Canonical Payload

The input to SHA-256 is the **UTF-8 byte encoding** of the Canonical
Event string (§1).

### 2.3 Hash Procedure

1. Encode the Canonical Event string as UTF-8 bytes.
2. Compute SHA-256 over those bytes.
3. Encode the resulting 32-byte digest as a lowercase hexadecimal string
   (64 characters).

The output is a **deterministic, platform-independent** 64-character
hex string.

### 2.4 Determinism Guarantee

The same Canonical Event string **MUST** produce the same 64-character
hex digest on:
- x86_64 (Verified)
- ARM64  (Verified — CI cross-platform job confirms bit-identity)
- WASM   (Architectural goal; CI verifies WASM-safe patterns only, not full WASM runtime execution)

---

## 3. Append-Only Event Log

### 3.1 Allowed Operations

- **Append**: Add a new Canonical Event to the tail of the log.

### 3.2 Forbidden Operations

- **Mutation**: Modifying any existing event in the log is forbidden.
- **Deletion**: Removing any event from the log is forbidden.
- **Reordering**: Changing the order of events is forbidden.
- **Insertion**: Inserting an event at any position other than the tail is forbidden.

### 3.3 Integrity Guarantees

Log integrity is enforced cryptographically:

1. Each event produces a Merkle leaf hash (§2).
2. All leaf hashes are combined into a Merkle tree (§4).
3. The Merkle root commits to the entire log; any mutation produces a
   different root.
4. An Event Trust Certificate (§5) carries the root and a Merkle proof
   for each event, allowing third-party verification without access to
   the full log.

---

## 4. Merkle Tree

### 4.1 Construction

Given a batch of `n` Canonical Events, the Merkle tree is built as
follows:

1. **Leaf level**: Each event string is hashed using the Canonical Hash
   procedure (§2).  The resulting hashes form the leaf level.
2. **Internal nodes**: Pairs of adjacent nodes at level `k` are
   concatenated (left ‖ right) and hashed to produce a node at level
   `k+1`.
3. The process repeats until a single node remains: the **Merkle root**.

Python reference (`audit/merkle.py`, `MerkleTree._build_tree`):

```python
for i in range(0, len(current_level), 2):
    left = current_level[i]
    right = current_level[i + 1] if i + 1 < len(current_level) else left
    parent = sha256(left + right)
    next_level.append(parent)
```

### 4.2 Odd-Leaf Handling

When a level contains an **odd** number of nodes, the last node is
**duplicated** as its own right sibling:

```
right = current_level[i + 1] if i + 1 < len(current_level) else left
```

This is the only permitted handling for odd-count levels.

### 4.3 Proof Format

A Merkle proof for leaf at index `i` is a list of `(sibling_hash,
direction)` tuples:

- `sibling_hash` — the 64-character hex hash of the sibling node.
- `direction` — `"left"` if the sibling is to the left of the current
  node; `"right"` if the sibling is to the right.

The list contains one tuple per level of the tree, from the leaf level
to the root level (exclusive).

### 4.4 Verification Algorithm

Given:
- `leaf_hash` — the Canonical Hash of the event being verified
- `proof` — the list of `(sibling_hash, direction)` tuples
- `expected_root` — the Merkle root from the Event Trust Certificate

```python
current = leaf_hash
for sibling, direction in proof:
    if direction == "left":
        current = sha256(sibling + current)
    else:
        current = sha256(current + sibling)
return current == expected_root
```

Python reference: `audit/merkle.py::verify_proof` and
`audit/verify.py::verify_proof`.

---

## 5. Event Trust Certificate (ETC)

### 5.1 Normative Schema

An Event Trust Certificate is a dataclass with the following fields
(`audit/merkle.py::EventTrustCertificate`):

| Field           | Type                     | Required | Description                                  |
|-----------------|--------------------------|----------|----------------------------------------------|
| `event_hash`    | `str` (64 hex chars)     | Yes      | SHA-256 of the Canonical Event               |
| `merkle_root`   | `str` (64 hex chars)     | Yes      | Merkle root of the batch                     |
| `merkle_proof`  | `List[Tuple[str, str]]`  | Yes      | Ordered proof steps (sibling_hash, direction) |
| `timestamp`     | `str` (ISO-8601 UTC)     | Yes      | Event timestamp                              |
| `batch_id`      | `str` or `None`          | No       | Optional batch identifier                   |
| `signature`     | `bytes` or `None`        | No       | Optional HMAC-SHA256 signature (§6)          |

### 5.2 Serialised Form

The canonical serialised form of an ETC is produced by
`EventTrustCertificate.to_dict()`:

```json
{
  "event_hash": "<64 hex chars>",
  "merkle_root": "<64 hex chars>",
  "merkle_proof": [
    {"sibling": "<64 hex chars>", "direction": "left|right"},
    ...
  ],
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "batch_id": "<string or null>",
  "signature": "<64 hex chars>"  // present only when signed
}
```

### 5.3 Field Definitions

- **event_hash**: SHA-256(Canonical Event string encoded as UTF-8).
  This is the leaf hash in the Merkle tree.
- **merkle_root**: The root hash of the Merkle tree for the entire
  batch containing this event.
- **merkle_proof**: The ordered sequence of (sibling, direction) pairs
  that reconstructs the root from the leaf.
- **timestamp**: ISO-8601 UTC timestamp as provided by the event source.
- **batch_id**: Optional identifier for the batch.  Not included in
  the signing payload (§6.1).
- **signature**: HMAC-SHA256 of the signing payload (§6.1), encoded as
  a lowercase hex string (64 characters = 32 bytes).

### 5.4 Versioning

This specification covers ETC schema version 1.0.0.  Future schema
changes require a new document version and a new instrument lineage.

---

## 6. Signature

### 6.1 Signing Payload

The payload submitted to the signing algorithm is the **UTF-8 byte
encoding** of the following deterministic JSON object:

```json
{"event_hash":"<64 hex chars>","merkle_root":"<64 hex chars>","timestamp":"<ISO-8601>"}
```

Rules:
- Keys in alphabetical order (sort_keys=True).
- No whitespace between tokens (separators `(",", ":")`).
- UTF-8 encoding, no BOM.
- The fields `batch_id` and `merkle_proof` are **excluded** from the
  signing payload so that the signature is stable across batches.

Python reference (`audit/merkle.py::EventTrustCertificate._signing_payload`):

```python
canonical = {
    "event_hash": self.event_hash,
    "merkle_root": self.merkle_root,
    "timestamp": self.timestamp,
}
return json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
```

### 6.2 Current Algorithm: HMAC-SHA256

The current implementation uses **HMAC-SHA256** as defined in
RFC 2104.

- **Signer**: `audit/signing.py::HMACSigner`
- **Verifier**: `audit/signing.py::HMACVerifier`
- Key type: `bytes`
- Output: 32-byte digest

```python
import hmac, hashlib

def sign(key: bytes, payload: bytes) -> bytes:
    return hmac.new(key, payload, hashlib.sha256).digest()

def verify(key: bytes, payload: bytes, signature: bytes) -> bool:
    expected = hmac.new(key, payload, hashlib.sha256).digest()
    return hmac.compare_digest(expected, signature)
```

### 6.3 Signing Abstraction

The Audit Layer exposes an abstract interface that decouples callers
from the concrete signing algorithm:

| Class          | Role                              | Implementation     |
|----------------|-----------------------------------|--------------------|
| `Signer`       | Abstract signing interface        | ABC                |
| `Verifier`     | Abstract verification interface   | ABC                |
| `HMACSigner`   | Current implementation            | HMAC-SHA256        |
| `HMACVerifier` | Current implementation            | HMAC-SHA256        |

Future migration to asymmetric signing (e.g., Ed25519) requires only
implementing new `Signer` / `Verifier` subclasses.  The ETC schema,
the Audit Layer API, and all callers remain unchanged.

### 6.4 Key Requirements

- Keys must be `bytes` (not `str`).
- Key material must be managed outside the Aura Protocol core.
- The same key must be used for signing and verification.
- Key storage and rotation are the responsibility of the calling system.

### 6.5 Verification Process

1. Reconstruct the signing payload from the ETC fields (§6.1).
2. Compute HMAC-SHA256(key, payload).
3. Compare the result to `etc.signature` using `hmac.compare_digest`
   (constant-time comparison).
4. Return `True` if equal, `False` otherwise.

---

## 7. Independent Verification

A third party can verify any ETC without access to the original log
or the signing key, using only:
- The Canonical Event string.
- The ETC (event_hash, merkle_root, merkle_proof, timestamp).

Optional (requires shared key):
- The ETC signature and the verification key.

### 7.1 Step-by-Step Verification Algorithm

**Step 1 — Compute leaf hash**

```python
leaf_hash = sha256(canonical_event_string)
```

**Step 2 — Check event_hash matches leaf**

```python
assert leaf_hash == etc.event_hash, "Event hash mismatch"
```

**Step 3 — Verify Merkle proof**

```python
current = etc.event_hash
for sibling, direction in etc.merkle_proof:
    if direction == "left":
        current = sha256(sibling + current)
    else:
        current = sha256(current + sibling)
assert current == etc.merkle_root, "Merkle proof invalid"
```

**Step 4 (optional) — Verify signature**

```python
payload = json.dumps(
    {"event_hash": etc.event_hash, "merkle_root": etc.merkle_root, "timestamp": etc.timestamp},
    sort_keys=True, separators=(",", ":"),
).encode("utf-8")
expected = hmac.new(key, payload, hashlib.sha256).digest()
assert hmac.compare_digest(expected, etc.signature), "Signature invalid"
```

### 7.2 PASS Criteria

All of the following must hold:

- ✅ `sha256(canonical_event)` == `etc.event_hash`
- ✅ Merkle proof recomputes to `etc.merkle_root`
- ✅ (If signed) HMAC-SHA256(key, payload) == `etc.signature`

### 7.3 FAIL Criteria

Any one of the following constitutes a verification failure:

- ❌ `sha256(canonical_event)` ≠ `etc.event_hash` → Event was modified.
- ❌ Merkle proof does not recompute to `etc.merkle_root` → Proof is invalid or root was modified.
- ❌ (If signed) Signature does not match → Key mismatch or certificate was tampered.

---

## 8. Cross-Platform Determinism Status

| Platform | Status                        | Evidence                                      |
|----------|-------------------------------|-----------------------------------------------|
| x86_64   | ✅ Verified                   | CI execution-checks job (ubuntu-latest)        |
| ARM64    | ✅ Verified                   | CI execution-checks job (ubuntu-24.04-arm)     |
| WASM     | 🔶 Architectural Goal         | WASM-safe patterns verified; full runtime TBD |

Cross-platform verification is performed by the `compare-determinism`
CI job which runs `scripts/compare_determinism_reports.py` on reports
from both x86_64 and ARM64 runners.

---

## References

- `audit/merkle.py` — MerkleTree, EventTrustCertificate, sha256, verify_proof
- `audit/signing.py` — Signer, Verifier, HMACSigner, HMACVerifier
- `audit/verify.py` — verify_proof, verify_etc
- `audit/test_audit.py` — Normative test suite for the Audit Layer
- `docs/architecture.md` — System architecture
- `docs/mathematical_foundation.md` — ARI formula and fixed-point arithmetic
- `docs/regulatory_compliance.md` — EU AI Act mapping
- FIPS 180-4 — SHA-256 specification
- RFC 2104 — HMAC specification

---

**Document Version**: 1.0.0  
**Instrument**: Aura Protocol v3.3 Iron Core  
**Status**: FROZEN — MC-READY 2026
