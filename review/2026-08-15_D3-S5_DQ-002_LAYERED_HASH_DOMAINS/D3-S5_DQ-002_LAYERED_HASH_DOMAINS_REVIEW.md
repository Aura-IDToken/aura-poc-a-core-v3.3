# D3-S5 / DQ-002 — Layered Hash Domains

**Question:** the normative and implemented relationship between `chain_hash`, `integrity_hash` and `event_payload_hash`
**Document class:** forensic architecture / specification / cryptographic-domain analysis. **Normative effect: NONE.**
**Prepared by:** Claude, analysis agent. **Not** the Architecture Owner.
**Date:** 2026-08-15
**Premise (frozen for this investigation):** DQ-001 accepted — **Option B, explicit adapter architecture**.
**Code changed:** NO. **Normative documents changed:** NO. **DQ-002 decision:** NOT MADE.

---

## 0. Labels, method, pinned revisions

Every material statement is **FACT** (verifiable at a cited `file:line` in a pinned
revision), **INFERENCE** (derived from FACTs, no normative weight), or **UNKNOWN**.
Negative results are stated as *"not found in inspected scope"*.

**Two method rules were applied throughout, per the task constraints:**

1. **No cryptographic meaning was inferred from a field name.** Every hash below was
   classified by reading its construction site, not its identifier.
2. **No gap was filled with conventional cryptographic practice.** Where the corpus is
   silent, the entry reads `UNKNOWN` or `DEFER TO DQ-006`, never a convention.

| Repository | Revision | State |
|---|---|---|
| `AuraIDToken/aura-guard-v1.3` | `443f72e` | full history, 105 commits, all branches (read-only) |
| `AuraIDToken/aura-poc-a-core-v3.3` | `98f2f43` | full history, 276 commits (unshallowed in DQ-001-H) |
| `AuraIDToken/aura-specification` | `62d2d6b` | full history, 44 commits (read-only) |

---

## 1. Executive summary

**The three names do not inhabit a common namespace. They are drawn from two disjoint
vocabularies that have never met.**

**FACT — the decisive census.** Across full histories and all branches:

| Name | `aura-guard-v1.3` | `aura-specification` | `aura-poc-a-core-v3.3` |
|---|---|---|---|
| `chain_hash` | **23 files @HEAD, 9 commits** | **0 files, 0 commits** | 0 outside `review/` + `docs/ADR_P0_6_*` |
| `integrity_hash` | **0 files, 0 commits** | 4 files @HEAD | **0 outside `review/`** |
| `event_payload_hash` | **0 files, 0 commits** | 1 file @HEAD (`APS-200:159`) | **0 outside `review/`** |

**INFERENCE.** `chain_hash` is an implementation concept with **no normative
counterpart**. `integrity_hash` and `event_payload_hash` are normative concepts with
**no implementation anywhere**. The question "are these one concept or several?" cannot
be answered by comparing them directly, because **they have never been co-located in a
single artifact.** Any relation between them would be created by the DQ-001 adapter, not
discovered in existing code.

**FACT — the implementation has more hash domains than the question assumes.**
`aura-guard-v1.3` computes **nine** distinct SHA-256 constructions (§3), not one or
three. Of these, `chain_hash` is only the entry-level link; a parallel
`segment_chain_hash`, an RFC 6962 Merkle layer, and an RFC 3161 message imprint sit
above it.

**FACT — the normative corpus also has more than three, and two of them collide.**
APS-200 and APS-300 between them define `integrity_hash`, `event_payload_hash`,
`previous_record_hash`, `input_hash`, `output_hash`, `evidence_hash`,
`previous_evidence_hash` and `policy_hash` (§5). **Two are record-level self-hashes with
incompatible self-inclusion semantics** — see the hard stop below.

**FACT — domain separation is present in one layer and absent in another.**
`src/merkle.rs:29-44` applies explicit RFC 6962 `0x00`/`0x01` prefixes with a stated
rationale ("defeating second-preimage attacks", `:13-15`). `src/chain.rs:36-47` and
`src/segment.rs:91-106` both produce a `"|"`-joined UTF-8 preimage with **no type tag,
no length prefix and no context string** distinguishing the two domains from one another.

**FACT — HARD STOP CONDITION 1 IS MET AND REPORTED, NOT RECONCILED.** APS-200:58 defines
`integrity_hash` as "SHA-256 hash of the canonical serialization of **this object**"
(self-inclusion unstated, therefore circular as written). APS-300:69 defines
`evidence_hash` as "SHA-256 hash of this Evidence object (**excluding this field**)".
ENT-005 Evidence is an APS-200 entity and so is bound by APS-200 §4's "Every entity
MUST", yet APS-300 §5's own MUST-list omits `object_id`, `object_type`, `created_at` and
`integrity_hash` entirely. **Two normative documents specify the record-level integrity
hash differently for the same object.** See §5.4 and §20.

**Answer to the primary question: D — the implementation contains hash concepts whose
normative relationship has not been established**, with a **C-shaped** structure visible
on the implementation side alone. The evidence does **not** support A (one concept) and
does **not yet** support C as a *normative* finding, because the normative side of two of
the three names is unimplemented and internally divergent.

**AGENT RECOMMENDATION — REQUIRES ARCHITECTURE OWNER APPROVAL: Option D**, with the
three-domain reading recorded as the *implementation* finding that a future DQ-002
resolution should normalize. See §19.

---

## 2. Scope

**In scope.** The three named hashes, every SHA-256 construction that produces or
consumes them, their normative definitions, and the dependency relationships between
them.

**Explicitly NOT decided here** (recorded where encountered, never resolved):

| Deferred to | What is left open |
|---|---|
| **DQ-006** Canonical Serialization | Every byte-level question — field encoding, ordering, integer encoding, optional-field representation, cross-language byte equality (§14) |
| **DQ-005** Integrity Binding | Whether `violations` (or any currently-uncovered field) enters an integrity domain |
| **DQ-004** Event Semantics | What `event_type` is, and therefore what "the event payload" of `event_payload_hash` denotes |
| **DQ-003** Versioning | Hash-domain version markers and migration discriminators |
| **DQ-007** Numeric Representation | Encoding of `seq`, and of the `f32` in `Violation` |

**Repository boundaries were maintained.** POC-A and Aura-Guard were traced separately
(§10) and no equivalence between their hash models is assumed anywhere in this document.

---

## 3. Current implementation trace (Phase 1)

### 3.1 `aura-guard-v1.3` — every SHA-256 construction

**FACT.** Primitives: `sha256_hex(&str)` hashes **UTF-8 bytes** and hex-encodes
(`src/crypto.rs:8-12`); `sha256_bytes_hex(&[u8])` hashes raw bytes
(`:16-20`). No truncation anywhere.

| # | Hash | Producer | Exact input | Algorithm | Output | Prev-hash dependency | Evidence |
|---|---|---|---|---|---|---|---|
| G-1 | `input_hash` | `api/audit.rs:109` | `format!("{} {} {}", context, prompt, response)` — space-joined, UTF-8 | SHA-256 | hex string | none | `api/audit.rs:104-109` |
| G-2 | `shadow_hash` | `api/audit.rs:110` | `shadow_normalize(original)` — the SHADOW_SPEC regex evaluation surface | SHA-256 | hex string | none | `api/audit.rs:108,110` |
| G-3 | `policy_hash` | `policy.rs:188` | **raw bytes of the policy file** (`sha256_bytes_hex(&policy_bytes)`) | SHA-256 | hex string | none | `policy.rs:188` |
| G-4 | **`chain_hash`** | `chain.rs:36-48` via `api/audit.rs:119-129` | **9 fields joined by `"\|"`**, UTF-8: `prev_hash \| decision \| policy_set \| policy_hash \| context \| input_hash \| shadow_hash \| seq.to_string() \| timestamp` | SHA-256 | hex string | **YES** — `prev_hash` is field 1 | `chain.rs:20,36-48` |
| G-5 | `genesis_hash` | `crypto.rs:27-29` | the literal string `"AURA-GUARD-GENESIS-v1.3"` | SHA-256 | hex string | n/a (seed) | `crypto.rs:22-29` |
| G-6 | Merkle `leaf_hash` | `merkle.rs:29-34` | `0x00 \|\| data`, where `data` = the **raw 32 bytes** obtained by hex-decoding an entry's `chain_hash` | SHA-256 | `[u8; 32]` | indirect (via `chain_hash`) | `merkle.rs:29-34`; `segment.rs:140-148` |
| G-7 | Merkle `node_hash` | `merkle.rs:38-44` | `0x01 \|\| left \|\| right` (32-byte digests) | SHA-256 | `[u8; 32]` | n/a | `merkle.rs:38-44` |
| G-8 | `segment_chain_hash` | `segment.rs:109-118` | **5 fields joined by `"\|"`**, UTF-8: `prev_segment_chain_hash \| merkle_root \| first_seq \| last_seq \| sealed_at` | SHA-256 | hex string | **YES** — `prev_segment_chain_hash` is field 1 | `segment.rs:91-118` |
| G-9 | `tsa_message_imprint` | `segment.rs:123-132` | **the same preimage as G-8**, hashed again | SHA-256 | `[u8; 32]` → RFC 3161 | inherits G-8's | `segment.rs:120-132` |

**FACT.** `empty_root()` = `SHA-256("")` (`merkle.rs:48-50`), used only for a leafless
tree.

**FACT — Ed25519 is a signature, not a hash domain.** `crypto.rs:44-59` verifies a
detached Ed25519 signature over policy bytes. Recorded for completeness; it is not one of
the domains under analysis.

### 3.2 Consumers of `chain_hash`

| Consumer | Role | Evidence |
|---|---|---|
| `models.rs:96` | Persisted struct field | — |
| `log_writer.rs:96` | `serde_json::to_string(entry)` → one JSONL line | `log_writer.rs:88-113` |
| `api/audit.rs:45` | Returned verbatim in the HTTP response body | `openapi.yaml:91` |
| `chain.rs:53-65` | `recompute_for_entry` — replay recomputation | — |
| `chain.rs:71-92` | `verify_chain` — walks links, seeds from `genesis_hash()` | `chain.rs:72` |
| `segment.rs:140-148` | Hex-decoded to 32 raw bytes, becomes a Merkle leaf | — |
| `segment.rs:81` | Recorded as `head_chain_hash_at_close` in the manifest | — |

**FACT — `chain_hash` is the only entry-level digest persisted.** No other per-entry hash
is stored: `input_hash`, `shadow_hash` and `policy_hash` are stored as *fields*, and are
also *inputs* to `chain_hash`; there is no second per-entry digest over the record.

### 3.3 `integrity_hash` and `event_payload_hash` in the implementation

**FACT.** `git grep` at HEAD and `git log --all -S` over the full 105-commit history of
`aura-guard-v1.3` return **zero files and zero commits** for both names. Also zero for
`previous_record_hash`. **Not found in inspected scope: any producer, consumer, field,
test or fixture for either concept.**

---

## 4. Hash construction graph (Phase 2)

**FACT.** The implementation's actual structure — derived only from construction sites,
with no assumed ordering:

```
policy file bytes ──SHA-256(raw bytes)──────────────► policy_hash ──┐
                                                                    │
context + " " + prompt + " " + response                             │
        ├──SHA-256(UTF-8)────────────────────────────► input_hash ──┤
        └──shadow_normalize──SHA-256(UTF-8)──────────► shadow_hash ─┤
                                                                    │
decision, policy_set, context, seq, timestamp ──────────────────────┤
                                                                    │
prev_hash (= previous entry's chain_hash) ──────────────────────────┤
"AURA-GUARD-GENESIS-v1.3" ──SHA-256──► genesis_hash ────(entry 0)───┤
                                                                    ▼
                                          ┌─────────────────────────────────────┐
                                          │ DOMAIN 1 — ENTRY CHAIN              │
                                          │ SHA-256( f1|f2|…|f9 ) as UTF-8      │
                                          │ separator "|", no type tag          │
                                          └──────────────┬──────────────────────┘
                                                         ▼
                                                    chain_hash  (hex)
                                                         │
                                   ┌─────────────────────┴──────────────────┐
                                   │ hex-decode → 32 raw bytes              │
                                   ▼                                        ▼
                    ┌──────────────────────────────┐          persisted verbatim in
                    │ DOMAIN 2 — RFC 6962 MERKLE   │          JSONL + HTTP response
                    │ leaf: SHA-256(0x00 || data)  │
                    │ node: SHA-256(0x01 || L || R)│  ◄── EXPLICIT domain separation
                    └──────────────┬───────────────┘
                                   ▼
                              merkle_root (hex)
                                   │
   prev_segment_chain_hash ────────┤
   first_seq, last_seq, sealed_at ─┤
                                   ▼
                    ┌──────────────────────────────────────┐
                    │ DOMAIN 3 — SEGMENT CHAIN             │
                    │ SHA-256( g1|g2|g3|g4|g5 ) as UTF-8   │
                    │ separator "|", no type tag           │  ◄── SAME shape as DOMAIN 1
                    └──────────────┬───────────────────────┘
                                   ├──────────────► segment_chain_hash (hex)
                                   │
                                   └──SHA-256(same preimage)──► tsa_message_imprint
                                                                        │
                                                                        ▼
                                                          ┌──────────────────────────┐
                                                          │ DOMAIN 4 — RFC 3161 TSA  │
                                                          └──────────────────────────┘
```

**FACT — what the implementation does NOT do.** It does **not** compute
`H(serialized AuditEntry)`. It does **not** compute `H(violation set)`. There is no
digest anywhere over the whole record. **FACT:** four of the 14 `AuditEntry` fields —
`violations`, `audit_id`, `request_id`, `schema` — are outside every one of the nine
domains (pre-registered in `docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` §2.2, status
CONFIRMED; **not reopened here**, and the question of whether they *should* be bound is
**DQ-005**).

**FACT — G-9 is a re-hash, not a new domain input.** `tsa_message_imprint`
(`segment.rs:123-132`) hashes the *same* preimage string as `segment_chain_hash`
(`:109-118`). **INFERENCE:** the RFC 3161 imprint and `segment_chain_hash` are the same
digest value under two names, one hex-encoded and one as raw bytes. This is the single
place in the implementation where two names denote one computation — and neither of them
is one of the three names under investigation.

---

## 5. APS-200 evidence (Phase 4)

**Document status:** `APS-200`, Version `1.0-DRAFT`, Status **DRAFT**, Classification
"Normative Specification" (`aps/APS-200_CANONICAL_DATA_MODEL.md:3-6`).
`VERSIONING.md:38` defines DRAFT as "Under active authoring; **may change freely**".

### 5.1 Every normative hash occurrence in APS-200

| Line | Field / text | Requirement level | Content |
|---|---|---|---|
| `:58` | `integrity_hash` | **MUST** | "SHA-256 hash of the canonical serialization of this object" |
| `:88` | `input_hash` (ENT-002) | **MUST** | "SHA-256 hash of the canonical input payload" |
| `:105` | `output_hash` (ENT-003) | **MUST** | "SHA-256 hash of the canonical output payload" |
| `:121` | `policy_hash` (ENT-004) | **MUST** | "SHA-256 hash of the policy content" |
| `:143` | `attestation_hash` (ENT-006) | **MUST** | "SHA-256 hash of attestation content" |
| `:158` | `previous_record_hash` (ENT-007) | **MUST** | "Hash of the previous Audit Record (chain link)" — **algorithm unstated** |
| `:159` | `event_payload_hash` (ENT-007) | **MUST** | "Hash of the event payload" — **algorithm unstated, "payload" undefined** |
| `:206` | integrity validation | **MUST** (validation rule 4) | "Integrity validation (`integrity_hash` matches computed hash)" |
| `:213-216` | §8 serialization | **MAY** / provided-that | formats MAY differ provided semantics preserved, determinism guaranteed where required, INV-003 not violated |
| `:218` | §8 | **TODO** | "Define the canonical serialization format for interoperability between RI-PY and RI-RS" |
| `:224` | §9 | **TODO** | "Publish JSON Schema definitions for each entity" |
| `:238` | §10 traceability | descriptive | `ENT-007 \| INV-012 \| EVID-AUDIT \| —` — **no CONF test** |

**FACT.** `chain_hash` occurs **0 times** in APS-200 and **0 times** in the entire
`aura-specification` repository, at HEAD and across all history.

### 5.2 Does APS-200 define the hashes?

| Hash | APS-200's treatment | Determination |
|---|---|---|
| `integrity_hash` | Names the algorithm (SHA-256) and the input *by reference* ("the canonical serialization of this object") — but that serialization is recorded as **TODO** at `:218` | **INDIRECTLY DEFINED, AND NOT COMPUTABLE.** Its input is defined in terms of an artifact the same document says does not yet exist |
| `event_payload_hash` | Names neither algorithm nor input encoding. "the event payload" is not defined in APS-200, APS-000 terminology, or `glossary/GLOSSARY.md` | **LEFT OPEN** |
| `chain_hash` | Not mentioned | **NOT MENTIONED** |

**FACT — `integrity_hash` is circular as written.** `:58` requires the hash of "the
canonical serialization of **this object**", and `integrity_hash` is itself a MUST field
of that object (`:49` "Every entity MUST contain the following fields"). APS-200 does
**not** state that the field is excluded from its own input. **Not found in inspected
scope:** any APS-200 text resolving the self-reference.

### 5.3 The fixture and schema evidence is empty

**FACT.** `fixtures/schemas/common-object-contract.schema.json:48-51` types
`integrity_hash` as a plain string and states "TODO: define canonical serialization
algorithm"; the file header reads `"_status": "TODO — pending finalization of APS-200"`.
`templates/FIXTURE_TEMPLATE.json:19,33` carry `"integrity_hash": "TODO — SHA-256"`.
`fixtures/core/FIX-001_BASIC_EVALUATION.json:19` carries `"input_hash": "TODO"`.
**No fixture in the corpus contains a computed hash value of any kind.**

### 5.4 CONFLICT-DQ002-01 — two record-level integrity hashes, incompatibly specified

**FACT.**

| Source | Field | Definition |
|---|---|---|
| `aps/APS-200_CANONICAL_DATA_MODEL.md:58` | `integrity_hash` | "SHA-256 hash of the canonical serialization of **this object**" — exclusion of the field itself **not stated** |
| `aps/APS-300_EVIDENCE_MODEL.md:69` | `evidence_hash` | "SHA-256 hash of this Evidence object (**excluding this field**)" |

**FACT.** These apply to the **same object**. `APS-200:49` binds the Common Object
Contract to "**Every entity**", and ENT-005 Evidence is an entity (`APS-200:41`).
`APS-200:129` delegates: "The canonical Evidence object fields are defined in APS-300 §5."

**FACT.** APS-300 §5's list is introduced with "Every Evidence object MUST contain **at
minimum**" (`:56`) and contains `evidence_id`, `protocol_version`, `schema_version`,
`implementation_id`, `execution_id`, `timestamp`, `policy_reference`, `input_hash`,
`output_hash`, `evidence_hash`, `previous_evidence_hash`, `attestation_reference`
(`:59-71`). It **omits** `object_id`, `object_type`, `created_at` and `integrity_hash`,
and substitutes `evidence_id` for `object_id`.

**FACT.** `APS-300:73` — "**TODO**: Define the canonical algorithm for computing
`evidence_hash`. Must reference INV-011 and specify whether the hash covers the full JSON
serialization or a field-ordered canonical form."

**INFERENCE.** For an Evidence object the corpus requires, simultaneously, a
self-inclusive-by-omission `integrity_hash` and a self-excluding `evidence_hash`, over
overlapping content, under two names, with the second's algorithm marked TODO. The two
documents do not agree on how the record-level integrity hash of an APS entity is
constructed, nor on whether there is one such hash or two.

**This is hard-stop condition 1. It is reported and escalated, not reconciled (§20).**

**Bearing on DQ-002.** The conflict sits on `integrity_hash` — one of the three names
under investigation. It means the normative side of the question is not merely
unimplemented but **internally divergent**, which is why §19 recommends D rather than C.

---

## 6. APS-100 evidence (Phase 5)

**Document status:** `1.0-DRAFT`. Named in the FROZEN Constitution's Article V hierarchy
(`constitution/AURA_CONSTITUTION.md:80`).

| Question | Finding | Evidence |
|---|---|---|
| Defines integrity semantics? | **Partially, at property level only.** INV-011: "The integrity of Evidence MUST be cryptographically verifiable." Scope is **Evidence**, not Audit Record | `APS-100:89`; `INVARIANT_REGISTRY.md:251` |
| Defines hash chaining? | **NO.** The words "chain", "chaining" and "chain_hash" do not appear in APS-100 | grep over `APS-100` |
| Defines audit trail integrity? | **Only as a property.** INV-012: "Every protocol-governed execution MUST leave an audit trail conformant with APS requirements" — no hash construction | `APS-100:92` |
| Inherits APS-200 hash semantics? | **NO — and the dependency runs the other way.** APS-100 never references APS-200; APS-200's Authority line names APS-100 (`APS-200:7`) | grep: 0 hits |
| Constrains hash domains? | **Indirectly.** INV-003: "Every protocol object MUST have an unambiguous serialization representation" — a property, not a domain definition | `APS-100:64` |
| Defines record binding? | **NO.** Not found in inspected scope | — |

**FACT.** INV-011's registry entry scopes it to `APS-300 §7` with Conformance Test
**CONF-010** (`INVARIANT_REGISTRY.md:248-249`) — i.e. the only cryptographic-integrity
invariant with a CONF test is bound to the **Evidence** model, not to ENT-007.

**Per the task constraint, no invariant is upgraded into an implementation requirement.**
INV-011 and INV-003 state properties that a hash design must satisfy; neither prescribes
a domain count, a layering, or a construction.

---

## 7. SPEC-002 evidence (Phase 6)

**Document status:** `0.3-DRAFT`. **`SPEC-002:12` — "Normative effect: NONE until
APPROVED."** `:37` — "Implementation behaviour does not constitute normative evidence."

### 7.1 REQ-002-017 … REQ-002-022

| Requirement | Exact meaning | Constrains | Implementation evidence | Classification |
|---|---|---|---|---|
| **REQ-002-017** (`:192`) | The future spec MUST explicitly define the **Vector Hash** domain: exact input bytes, preceding serialization, algorithm, output encoding, output representation | Hash domain — **Constitution Vector** | none — no Constitution Vector exists in either implementation | **NOT APPLICABLE to DQ-002's three names** |
| **REQ-002-018** (`:193`) | Same, for the **Artifact Hash** domain | Hash domain — **Constitution Artifact** | none | **NOT APPLICABLE** |
| **REQ-002-019** (`:194`) | MUST explicitly state which fields are **included in and excluded from** each hash input | Field binding — **principle is directly on point** | `chain.rs:36-47` covers 9 of 14 `AuditEntry` fields; inclusion/exclusion is implemented but nowhere normatively stated | **PRINCIPLE APPLICABLE, SUBJECT NOT** |
| **REQ-002-020** (`:195`) | Domain definitions MUST suffice for an independent implementer to reproduce the exact byte sequence **without inspecting any Reference Implementation** | Verification / independence | **Currently unsatisfiable for `chain_hash`:** the 9-field order and `"\|"` separator exist only in `chain.rs`; no specification states them | **PRINCIPLE APPLICABLE, SUBJECT NOT** |
| **REQ-002-021** (`:215`) | The future spec MUST define **exactly one** canonical serialization format, including field set, field order, encoding, and representation of absent/optional fields | Canonical serialization | `#[serde(skip_serializing_if)]` on `Violation::validator` (`models.rs:40`) and `AuditEntry::request_id` (`:65`) makes optional-field representation live | **DEFER TO DQ-006** |
| **REQ-002-022** (`:216`) | The future spec MUST define **exactly one** canonical byte sequence **per hash domain, per representation**; the Artifact and Vector byte sequences are **SEPARATE definitions** and **MUST NOT be treated as a single universal byte sequence** | Domain multiplicity | — | **PRINCIPLE DIRECTLY ON POINT** |

### 7.2 The governing principle and the architecture note

**FACT.** `SPEC-002:186-190` §4.5 Hash Domains — "There MUST be **at minimum** a Vector
Hash domain and an Artifact Hash domain. However, the future specification is **NOT
restricted to exactly these two domains**; it MUST explicitly define every hash domain it
uses and **MUST NOT silently rely on additional undeclared domains**."

**FACT.** `SPEC-002:208-211` — "**ARCHITECTURE NOTE — Hash Domains are UNRESOLVED
(AD-CA-007, AD-CA-008).** This draft MUST NOT itself approve any concrete hash formula…
Such formulas do not exist in any approved normative source and remain unresolved. The
future architecture decision MUST define each hash domain completely. **Governing
principle: Hash domain MUST be explicitly defined and independently reproducible.**"

**FACT.** `SPEC-002:381-382` — AD-CA-007 (numeric representation) and AD-CA-008
(canonical serialization, canonical byte sequence, hash domain definitions) are both
**UNRESOLVED**, and AD-CA-008 "Blocks REQ-002-017 through REQ-002-022".

**INFERENCE — SPEC-002's subject is disjoint from DQ-002's, but its method is directly
transferable.** SPEC-002 governs the Constitution Artifact/Vector, not `AuditEntry` or
ENT-007; it mentions none of the three names (`AuditEntry`, `Audit Record`, `ENT-007`,
`chain_hash`, `integrity_hash`, `event_payload_hash` — **0 occurrences each across all
631 lines**). But it is the **only** document in the corpus that states a *methodology*
for hash domains: enumerate every domain, define each completely, never rely on an
undeclared one, and keep separate representations in separate domains.

**Hard-stop condition 2 assessed: NOT triggered.** APS-200 and SPEC-002 do not define
*incompatible* hash domains — they define **disjoint** ones over different subject
matter. No contradiction was found.

---

## 8. ADR and invariant evidence (Phase 7)

| Source | Status | What it establishes | What it does NOT establish |
|---|---|---|---|
| `aura-guard-v1.3/docs/adrs/0001-hash-chain.md` | **Accepted in v1.3, still current** (`:3`) | Chose "SHA-256 chained between entries (Bitcoin-style block-header chain)" over per-entry-only and over Merkle. Records the genesis constant and that `chain_hash` covers "canonical fields incl. `prev_hash`" | **Does not enumerate the 9 fields.** Does not name a domain separator. Does not mention APS-200, `integrity_hash` or `event_payload_hash`. `:38-45` records that Merkle segments were *layered on top* rather than replacing the decision |
| `aura-guard-v1.3/docs/adrs/0002-ed25519-policy-signing.md` | Accepted | Policy signing | Not a hash domain for audit records |
| `aura-poc-a-core-v3.3/docs/ADR_005_NO_FLOAT_RUNTIME.md` | — | Zero-float runtime (POC-A) | No hash domain content |
| `aura-poc-a-core-v3.3/docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` | **DRAFT — NON-NORMATIVE — REQUIRES HUMAN APPROVAL** | Records as CONFIRMED that `violations`, `audit_id`, `request_id`, `schema` are outside `chain_hash` | Explicitly **does not** select a serialization, choose a hash domain, or resolve D-1…D-7 (`§0`) |
| `aura-specification/adrs/` | ADR-001 **PROPOSED** | Document model | No hash content — `grep ENT-\|APS-200\|hash` over `adrs/` returns nothing relevant |

| Invariant | Text | Bearing on DQ-002 |
|---|---|---|
| INV-001 (`APS-100:58`) | Identical inputs MUST produce identical outputs | Property. Satisfied by any deterministic domain |
| INV-002 (`:61`) | Replay MUST reproduce an identical result on every conformant implementation | **Cross-implementation** byte equality — **DEFER TO DQ-006** |
| INV-003 (`:64`) | Every protocol object MUST have an **unambiguous** serialization representation | The closest normative hook for domain separation. Property only — no construction |
| INV-006 (`:73`) | Platform independence | Property |
| INV-009 (`:83`) | Evidence, Protocol, Data Model MUST reference compatible document versions | Document-level; bears on DQ-003 |
| INV-011 (`:89`) | Integrity of **Evidence** MUST be cryptographically verifiable by an independent party | Scoped to Evidence; CONF-010 |
| INV-012 (`:92`) | Every execution MUST leave an audit trail conformant with APS requirements | Carries **CONFLICT-DQ001-01** (APS-100 "audit trail" vs `INVARIANT_REGISTRY.md:273` "Audit Record (ENT-007)"), registered in the DQ-001 review and **not reopened** |

**FACT — no existing decision, in any repository, establishes a hash-domain count, a
layering, or a binding between the three names.** Not found in inspected scope.

---

## 9. Historical trace (Phase 8)

| Date | Commit | Repository | Hash concept | Change | Evidence | Interpretation |
|---|---|---|---|---|---|---|
| 2026-01-04 | `befddfa` | POC-A | `sha256`, Merkle | `merkle.py` created | `git log --diff-filter=A` | **FACT.** POC-A's hash layer predates the guard by 129 days |
| 2026-01-17 | `80ec4ad` | POC-A | `event_hash`, `merkle_root` | `EventTrustCertificate` introduced | `audit/merkle.py:20,38-43` | **FACT.** POC-A's record-level concepts. **INFERENCE:** independent of any APS text, which did not exist |
| **2026-05-13** | **`d03eb65`** | **Guard** | **`chain_hash`, `prev_hash`, `input_hash`, `shadow_hash`, `policy_hash`, `genesis_hash`** | All introduced together in the monolithic v1.3.1 import. **The 9-field preimage is present in full at this commit** | `git show d03eb65:src/chain.rs:36-48` | **FACT.** **The `chain_hash` domain has been byte-stable since introduction** |
| 2026-05-13 | `d03eb65` | Guard | `chain_hash` **doc-comment** | Documents a **7-field** preimage: `prev_hash \|\| decision \|\| policy_set \|\| input_hash \|\| shadow_hash \|\| seq \|\| timestamp` — omitting `policy_hash` and `context` | `git show d03eb65:src/models.rs:87` | **FACT.** The documentation was **wrong from the first commit**, not degraded later. Still wrong at HEAD (`models.rs:95`, identical text) |
| 2026-05-14 | `b189a1e` | Guard | `chain_hash` | "OSS-professional polish" | `git log -S` | No semantic change found |
| **2026-05-19** | **`31a60de`** | **Guard** | **`leaf_hash`, `node_hash`, `merkle_root`, `segment_chain_hash`** | v1.4 — "Merkle batching (RFC 6962) + optional RFC 3161 timestamping". **Adds three domains above `chain_hash`** | `CHANGELOG.md:64-72` | **FACT.** The layered structure is a v1.4 addition. **INFERENCE:** layering arose from batching/anchoring needs, not from a protocol contract — APS-200 did not exist |
| 2026-05-20 | `1e801c3` | Guard | `tsa_message_imprint` | v1.5 — full RFC 3161/5652/5816 verifier | `CHANGELOG.md:18,138` | **FACT.** `messageImprint == SHA-256(segment_chain_preimage)` |
| **2026-07-23** | **`b68181e`** | **Spec** | **`integrity_hash`, `event_payload_hash`, `previous_record_hash`, `evidence_hash`** | All four born in the single commit that created the entire APS corpus | `git log --diff-filter=A` | **FACT.** The normative vocabulary arrives **71 days after** `chain_hash` and **65 days after** the Merkle layer |
| 2026-07-26 | `025f092`, `51bcdd2` | Guard | `chain_hash` | Test-coverage expansion touching `chain.rs` | `git log -S` | **FACT.** No preimage change — the 9 fields at HEAD are identical to `d03eb65` |
| 2026-08-15 | `70b9881` | Guard | `chain_hash` preimage | `chain_preimage()` accessor extracted **verbatim**; commit records identical digests before/after (`6eb514bf…`) and pins the value in `tests/d3_chain_observability.rs` | commit body | **FACT.** Instrumentation only, on an unmerged branch. **Explicitly "Recorded, NOT resolved": the `models.rs:95` 7-vs-9 divergence** |

**Hard-stop condition 3 assessed: NOT triggered.** Historical evidence does not
*contradict* current normative evidence — the two have never intersected. The `chain_hash`
domain never changed, so there is no historical/normative divergence to adjudicate.

**UNKNOWN.** Why `policy_hash` and `context` were included in the preimage but omitted
from its documentation. No commit message, ADR or issue explains it.

---

## 10. Cross-repository comparison (Phase 9)

**Repository boundaries maintained; no equivalence assumed.**

**FACT — POC-A's hash model** (`aura-poc-a-core-v3.3` @ `98f2f43`):

| Construction | Site | Input |
|---|---|---|
| `sha256(data: str)` | `audit/merkle.py:14-16` | UTF-8 → hex |
| Merkle parent | `audit/merkle.py:163` | `sha256(left + right)` — **string concatenation, NO 0x00/0x01 prefixes** |
| Merkle proof step | `audit/merkle.py:109,111,259,261` | `sha256(sibling + current)` / `sha256(current + sibling)` |
| Empty root | `audit/merkle.py:145` | `sha256("")` |
| ETC signing payload | `audit/merkle.py:80-85` | `json.dumps({event_hash, merkle_root, timestamp}, sort_keys=True, separators=(",",":"))` → UTF-8 |
| ETC signature | `audit/signing.py:89` | **HMAC-SHA256, symmetric** over that payload |
| Leaf generation | `core/merkle.py:8` | `sha256(json.dumps(data, sort_keys=True))` |
| Certificate fingerprint | `compliance/certificate.py:70` | `sha256(payload UTF-8)` |

| Concept | POC-A | Aura-Guard | APS-200 | Classification |
|---|---|---|---|---|
| Payload-level hash | `event_hash` (`audit/merkle.py:38`) | `input_hash` **and** `shadow_hash` (two) | `event_payload_hash` (`:159`), `input_hash` (`:88`) | **NOT ESTABLISHED** — three different shapes, no mapping anywhere |
| Record-level self-hash | **none** — ETC has no self-digest; identity is carried by an HMAC signature | **none** — no digest over the whole record | `integrity_hash` (`:58`), `evidence_hash` (APS-300:69) | **MISSING in both implementations; CONFLICTED in the corpus** |
| Chain link | **none** — batch Merkle only, no per-record predecessor link | `prev_hash` → `chain_hash` | `previous_record_hash` (`:158`) | **NOT ESTABLISHED** — POC-A has no analogue at all |
| Merkle domain separation | **ABSENT** — plain concatenation | **PRESENT** — RFC 6962 `0x00`/`0x01` | not specified | **CONFLICT between implementations** |
| Canonicalization before hashing | JSON `sort_keys=True, separators=(",",":")` | `"\|"`-joined field concatenation | **TODO** (`APS-200:218`) | **NOT ESTABLISHED** |
| Signature | HMAC-SHA256 **symmetric** | Ed25519 **asymmetric** (over policy, not record) | not specified for ENT-007 | **NOT ESTABLISHED** |

**Determination.**

- **POC-A hash model = Guard hash model? → NOT ESTABLISHED.** They share only the
  SHA-256 primitive. Different Merkle rules produce **different roots for identical
  leaves** (`review/2026-08-11_ENGINEERING_BASELINE/03_LANGUAGE_BOUNDARY.md:50`),
  different canonicalization, different signature cryptography, and only one of the two
  has a per-record chain link.
- **Either = APS-200 hash model? → NOT ESTABLISHED.** `RI-RS_AURA_GUARD.md:50` records
  INV-003 as "PARTIAL | JSON; **no APS-200 canonical object schema**";
  `RI-PY_AURA_POC_A_CORE.md:27` records the audit interface as "**not APS-200 ENT-007**".

**Hard-stop condition 8 assessed: NOT triggered.** No cross-repository hash relationship
is inferred anywhere in this document; all three models are reported as separate.

---

## 11. Hash domain matrix (Phase 10)

| Hash | Producer | Input | Byte representation | Incl. previous hash? | Incl. payload? | Incl. violations? | Incl. metadata? | Algorithm | Output | Normative source | Classification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **`chain_hash`** | `chain.rs:36-48` | 9 fields `"\|"`-joined | UTF-8 of the joined string; field encodings **UNKNOWN** beyond `seq.to_string()` — **DEFER TO DQ-006** | **YES** (`prev_hash`, position 1) | **Indirectly** — via `input_hash`/`shadow_hash` digests, never raw payload | **NO** | **Partially** — `decision`, `policy_set`, `policy_hash`, `context`, `seq`, `timestamp`; **not** `schema`, `audit_id`, `request_id` | SHA-256 | 64-char hex | **NONE FOUND** | **EXTRA** |
| **`integrity_hash`** | *no producer* | "the canonical serialization of this object" (`APS-200:58`) | **UNKNOWN** — the serialization is TODO (`APS-200:218`) | **UNKNOWN** — unstated | **UNKNOWN** | **UNKNOWN** — DQ-005 | **UNKNOWN**; self-inclusion unstated → circular | SHA-256 (stated) | string (unspecified encoding) | `APS-200:58`, `:206` | **MISSING** — and **CONFLICT** vs `APS-300:69` (§5.4) |
| **`event_payload_hash`** | *no producer* | "the event payload" (`APS-200:159`) | **UNKNOWN** | **UNKNOWN** | by name yes; "payload" **undefined** — depends on **DQ-004** | **UNKNOWN** — DQ-005 | **UNKNOWN** | **UNSTATED** | string (unspecified) | `APS-200:159` | **MISSING** |
| `prev_hash` | `api/audit.rs:118` | previous entry's `chain_hash` | 64-char hex | is the value | no | no | no | (copied) | hex | `APS-200:158` `previous_record_hash` | **DERIVED** — concept matches, name and algorithm-statement do not |
| `input_hash` | `api/audit.rs:109` | `context + " " + prompt + " " + response` | UTF-8, space-joined | no | **YES** — raw payload | no | **YES** — `context` is inside | SHA-256 | hex | `APS-200:88` (ENT-002), `APS-300:67` | **DERIVED** — normative counterpart is scoped to a different entity |
| `shadow_hash` | `api/audit.rs:110` | `shadow_normalize(original)` | UTF-8 | no | **YES** — normalized payload | no | yes (context inside) | SHA-256 | hex | **NONE FOUND** | **EXTRA** |
| `policy_hash` | `policy.rs:188` | raw policy file bytes | raw bytes | no | no | no | policy content | SHA-256 | hex | `APS-200:121` (ENT-004) | **DERIVED** |
| `genesis_hash` | `crypto.rs:27-29` | `"AURA-GUARD-GENESIS-v1.3"` | UTF-8 | n/a — seed | no | no | version string | SHA-256 | hex | **NONE FOUND** | **EXTRA** |
| Merkle `leaf_hash` | `merkle.rs:29-34` | `0x00 \|\| chain_hash_raw32` | raw bytes, **explicit 1-byte tag** | indirect | no | no | no | SHA-256 | `[u8;32]` | **NONE FOUND** | **EXTRA** |
| Merkle `node_hash` | `merkle.rs:38-44` | `0x01 \|\| L \|\| R` | raw bytes, **explicit 1-byte tag** | n/a | no | no | no | SHA-256 | `[u8;32]` | **NONE FOUND** | **EXTRA** |
| `segment_chain_hash` | `segment.rs:109-118` | 5 fields `"\|"`-joined | UTF-8; `first_seq`/`last_seq` via `.to_string()` — **DEFER TO DQ-006** | **YES** (`prev_segment_chain_hash`) | no | no | seq range, `sealed_at` | SHA-256 | hex | **NONE FOUND** | **EXTRA** |
| `tsa_message_imprint` | `segment.rs:123-132` | **identical preimage to `segment_chain_hash`** | as above | inherits | no | no | as above | SHA-256 | `[u8;32]` | **NONE FOUND** | **EXTRA** |
| `evidence_hash` | *no producer* | "this Evidence object (excluding this field)" | **UNKNOWN** — `APS-300:73` TODO | no | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | SHA-256 | string | `APS-300:69` | **MISSING** — and **CONFLICT** vs `APS-200:58` |

**Tally: 8 EXTRA · 3 MISSING · 3 DERIVED · 0 MATCH · 2 CONFLICT.**

**FACT — there is not a single MATCH.** No implemented hash corresponds to a defined
normative cryptographic concept with a compatible representation.

---

## 12. Domain graph (Phase 11)

**Evidence-backed. Only established relationships are drawn. The expected architecture is
not forced.**

```
IMPLEMENTED (aura-guard-v1.3 @ 443f72e) — four stacked domains, one direction

    raw payload ──► input_hash ──┐
    normalized  ──► shadow_hash ─┤
    policy bytes ─► policy_hash ─┤──► [D1 entry chain] ──► chain_hash
    prev entry ───► prev_hash ───┘         "|"-joined            │
                                                                 ▼
                                            [D2 RFC 6962 Merkle] ──► merkle_root
                                              0x00/0x01 tagged        │
                                                                      ▼
                                            [D3 segment chain] ──► segment_chain_hash
                                              "|"-joined              │
                                                                      ▼
                                            [D4 RFC 3161] ──► tsa_message_imprint
                                              (same preimage as D3)

NORMATIVE (APS-200 / APS-300 @ 62d2d6b) — flat, unlayered, no dependencies stated

    ENT-007 ──┬──► event_payload_hash   "hash of the event payload"   (algorithm UNSTATED)
              ├──► previous_record_hash "chain link"                  (algorithm UNSTATED)
              └──► integrity_hash       "SHA-256(canonical serialization of this object)"
                                        └── input is TODO (APS-200:218); self-inclusion UNSTATED

    ENT-005 ──┬──► evidence_hash        "SHA-256(this object EXCLUDING this field)"
              └──► previous_evidence_hash (SHOULD)
                        ▲
                        └── CONFLICT-DQ002-01 with integrity_hash (§5.4)

BETWEEN THE TWO GRAPHS

    ╳  no edge exists in either direction, at any commit, in any repository
```

**FACT.** APS-200 states **no dependency** among `event_payload_hash`,
`previous_record_hash` and `integrity_hash`. They are three sibling MUST fields in one
table (`:156-159` + `:58`). **The corpus does not assert a layering.**

**INFERENCE.** The "layered hash domains" framing describes the **implementation**
accurately (D1→D2→D3→D4 is a real, evidenced dependency chain) and describes the
**normative model** not at all. Per the instruction not to assume layering from the DQ's
name: layering is confirmed on one side only.

---

## 13. Domain separation analysis (Phase 12)

**No new cryptographic scheme is designed here. Only PRESENT / ABSENT / UNRESOLVED.**

| Mechanism | D1 entry chain | D2 Merkle | D3 segment chain | D4 TSA | Normative model |
|---|---|---|---|---|---|
| Domain separator / type tag | **ABSENT** | **PRESENT** — `0x00`/`0x01` (`merkle.rs:31,40`) | **ABSENT** | inherits D3 | **ABSENT** |
| Length prefix | **ABSENT** | ABSENT (fixed 32-byte operands) | **ABSENT** | — | **ABSENT** |
| Explicit context string | **ABSENT** in the preimage; **PRESENT** once as the seed `"AURA-GUARD-GENESIS-v1.3"` (`crypto.rs:28`) | ABSENT | ABSENT | — | **ABSENT** |
| Canonical field ordering | **PRESENT** — fixed array order (`chain.rs:36-46`), stable since `d03eb65` | n/a | **PRESENT** (`segment.rs:98-105`) | — | **ABSENT** — no ordering specified |
| Structured encoding | **ABSENT** — flat string join, not a structured encoder | PRESENT (fixed-width) | **ABSENT** | — | **UNRESOLVED** — `APS-200:213` permits JSON/CBOR/protobuf |
| Field escaping | **ABSENT** | n/a | **ABSENT** | — | **ABSENT** |

### 13.1 Can two different semantic objects produce the same hash input domain?

**FACT — D1 and D3 are structurally indistinguishable at the domain level.** Both compute
`SHA-256(UTF-8("…"|"…"))` with the same separator and no tag. Nothing in either preimage
identifies which domain produced it. **Cross-domain separation between the entry chain
and the segment chain is ABSENT.**

**FACT — exactly one D1 field is caller-controlled and unconstrained.** Of the nine:
`prev_hash`, `input_hash`, `shadow_hash`, `policy_hash` are fixed-width hex; `seq` is an
integer; `timestamp` is server-generated RFC 3339; `decision` is server-selected from
`DENY`/`REVIEW`/`ALLOW`; `policy_set` must resolve against the pre-warmed cache
(`api/audit.rs:82`). **`context` is echoed verbatim from the request
(`api/audit.rs:140`).** Not found in inspected scope: any validation, escaping, charset
restriction or length limit on `context` — `src/validators.rs` and `src/config.rs`
contain no `context` constraint; the only bound is the global
`DefaultBodyLimit::max(max_body_bytes)` (`api/mod.rs:54,76`).

**FACT.** `chain.rs:11` asserts "Field separator is `\|` so the input is unambiguous."
`chain.rs:18-19` adds that `SEP` "Must never overlap with hex, base64 or any timestamp
character." **INFERENCE:** that constraint is stated against the *hex/timestamp* fields
and is satisfied for them; it is **not** satisfied by construction for `context`, which
may contain `\|`. Unambiguity of D1 therefore rests on the fixed-format nature of the
eight non-`context` fields rather than on the separator alone.

**Practical exploitability: NOT ESTABLISHED — and deliberately not pursued.** Producing a
second preimage would require a second request whose server-generated tail
(`input_hash`, `shadow_hash`, `seq`, `timestamp`) matched attacker-injected content,
which the caller does not control. **This is recorded as a structural property of the
domain, not as a claimed vulnerability**, and no mitigation is proposed — designing one
would be a cryptographic redesign, which is outside this authority boundary.

### 13.2 Determination

| Question | Answer |
|---|---|
| Is domain separation present within the Merkle layer? | **PRESENT** |
| Is domain separation present between D1 and D3? | **ABSENT** |
| Is domain separation present in the normative model? | **ABSENT** — APS-200 specifies no separator, tag, prefix or ordering for any of its hashes |
| Is the byte-level adequacy of D1/D3 decidable now? | **DEFER TO DQ-006** |
| Does `SPEC-002:190`'s "MUST NOT silently rely on additional undeclared domains" bear on this? | **YES in principle, NO in force** — SPEC-002 has `Normative effect: NONE` and a disjoint subject (§7.2) |

---

## 14. DQ-006 dependencies (Phase 13)

**DQ-002 → DQ-006 dependency list.** Each item is **isolated, not solved**.

| # | Question | Why DQ-002 cannot settle it | Anchor |
|---|---|---|---|
| **DEP-1** | Exact byte encoding of `integrity_hash`'s input | Defined as "the canonical serialization of this object"; that serialization is **TODO** | `APS-200:58`, `:218` |
| **DEP-2** | Is `integrity_hash` computed over the object **including or excluding** itself? | Unstated in APS-200; APS-300 says "excluding" for its analogue → **CONFLICT-DQ002-01** | `APS-200:58` vs `APS-300:69` |
| **DEP-3** | Field ordering in any canonical form | `APS-200:213` permits JSON/CBOR/protobuf; serde emits declaration order — not a specified canonical order | `APS-200:213-218`; `models.rs:49` |
| **DEP-4** | Integer encoding of `seq` / `first_seq` / `last_seq` | Implementation uses `.to_string()` decimal; no normative encoding exists. Also bears on **DQ-007** | `chain.rs:44`; `segment.rs:101-102` |
| **DEP-5** | Optional-field representation | `skip_serializing_if = "Option::is_none"` omits `request_id` and `Violation::validator` **entirely** when absent — REQ-002-021 requires this to be defined | `models.rs:40,65`; `SPEC-002:215` |
| **DEP-6** | String encoding and normalization | Implementation assumes UTF-8; no normative statement (NFC/NFD unaddressed) | `crypto.rs:8-12` |
| **DEP-7** | Cross-language byte equality RI-PY ↔ RI-RS | POC-A uses JSON `sort_keys`; guard uses `"\|"` join. INV-002 requires identical replay results | `APS-200:218`; `APS-100:61` |
| **DEP-8** | Whether a domain separator becomes part of the canonical byte sequence | Domain separation is a serialization-layer property once a canonical form exists | §13 |
| **DEP-9** | Output encoding of every normative hash | `APS-200` says "string"; hex vs base64 unstated. REQ-002-017/018 require it | `APS-200:58,158,159` |
| **DEP-10** | Whether `f32` `confidence` can appear in any hashed byte sequence | Float determinism; also **DQ-007** | `models.rs:38` |

**Hard-stop condition 5 assessed: PARTIALLY TRIGGERED, and scoped.** Canonical
serialization is **not** required to distinguish the domains *semantically* — record-level
(`integrity_hash`), payload-level (`event_payload_hash`) and link-level (`chain_hash` /
`previous_record_hash`) are separable by their stated purposes alone, which is what makes
the §19 recommendation possible. It **is** required to distinguish them *at the byte
level*, and every such question is listed above and left open.

---

## 15. Architectural options (Phase 14)

### OPTION A — ONE HASH CONCEPT (aliases of a single conceptual hash)

- **Evidence supporting:** all are SHA-256-based (or presumed so); all are hex-ish
  strings; `tsa_message_imprint` and `segment_chain_hash` demonstrate that this codebase
  *does* reuse one computation under two names (`segment.rs:117` vs `:131`).
- **Evidence against:** **decisive.** `chain_hash` includes `prev_hash` by construction
  (`chain.rs:37`), so it is order-dependent; `integrity_hash` is defined over a single
  object with no predecessor; `event_payload_hash` covers payload only. APS-200 lists
  `previous_record_hash` and `event_payload_hash` and (via §4) `integrity_hash` as
  **three separate MUST fields on one entity** (`:58,158,159`) — a specification does not
  mandate three fields for one value. Merging them would make the record-level hash
  order-dependent and the chain link content-complete, destroying both properties.
- **Consequences:** collapses tamper-evidence and record identity into one value.
- **Migration:** HIGH — requires redefining `chain_hash` or dropping two MUST fields.
- **Testing:** every chain test invalidated. **Serialization:** forces DQ-006 immediately.
- **Cross-language:** worse — one over-constrained value both RIs must match exactly.
- **Auditability:** reduced — cannot verify a record without its predecessor.
- **Security:** **negative** — loses the leaf/node separation rationale at `merkle.rs:13-15`.
- **Reversibility:** VERY LOW once emitted.
- **Verdict: REFUTED by evidence.**

### OPTION B — TWO-LAYER MODEL (`event_payload_hash` → `integrity_hash` → chain linkage)

- **Evidence supporting:** the implementation *is* layered (§12), and D1 does consume
  payload digests (`input_hash`, `shadow_hash`) as inputs — a genuine
  payload→record→link progression in spirit.
- **Evidence against:** the specific two-layer nesting is **asserted nowhere**. APS-200
  states no dependency among the three (`:58,158,159`). The implementation's layering is
  D1→D2→D3→D4 (entry→Merkle→segment→TSA), which is **not** the proposed
  payload→integrity→chain nesting. `chain_hash` consumes `input_hash` and `shadow_hash`
  **as two separate digests**, not one `event_payload_hash` — and which of the two is
  "the payload" is **DQ-004**.
- **Consequences:** adapter must synthesize a nesting the corpus does not define.
- **Migration:** MEDIUM. **Testing:** new equivalence tests. **Serialization:** blocked on DEP-1/2.
- **Cross-language:** requires both RIs to agree on the nesting — POC-A has no chain link at all.
- **Auditability:** good if defined. **Security:** neutral. **Reversibility:** MEDIUM.
- **Verdict: PLAUSIBLE BUT UNEVIDENCED.** It would be a design choice, not a finding.

### OPTION C — THREE-DOMAIN MODEL (three distinct semantic/cryptographic domains)

- **Evidence supporting:** **strong on the implementation side.** Nine distinct
  constructions with different inputs, different byte representations (UTF-8 join vs raw
  bytes vs tagged bytes) and different dependency structures. `SPEC-002:190` states the
  matching principle — every domain declared, none silently relied upon — and
  `REQ-002-022` states that separate representations are **separate domains** that "MUST
  NOT be treated as a single universal byte sequence". APS-200 listing three sibling MUST
  fields is consistent with three purposes.
- **Evidence against:** **the count is wrong, and one of the three is contested.** The
  implementation has **nine** domains, not three; `chain_hash` alone is a distinct domain
  the specification does not have. `integrity_hash` is subject to **CONFLICT-DQ002-01**
  and is not computable (`APS-200:218` TODO). `event_payload_hash`'s subject is undefined
  pending **DQ-004**. Declaring three normative domains now would freeze a count that the
  evidence does not support and would pre-empt DQ-004/DQ-005.
- **Consequences:** correct direction, premature precision.
- **Migration:** MEDIUM–HIGH. **Testing:** per-domain reproduction tests, none of which
  can be written before DQ-006. **Serialization:** blocked on all ten DEPs.
- **Cross-language:** requires resolving POC-A/guard divergence (§10) first.
- **Auditability:** best in the limit. **Security:** best — makes separation explicit.
- **Reversibility:** LOW once domains are published and evidence is anchored.
- **Verdict: RIGHT DIRECTION, NOT YET SUPPORTED AS A NORMATIVE FINDING.**

### OPTION D — CURRENT IMPLEMENTATION IS UNNORMATIVE

- **Evidence supporting:** **overwhelming and direct.**
  - `chain_hash`: **0 occurrences** in the entire specification corpus, all history.
  - `integrity_hash`, `event_payload_hash`: **0 occurrences** in the entire guard, all history.
  - **Zero MATCH rows** in the §11 matrix.
  - `RI-RS_AURA_GUARD.md:50` — INV-003 "PARTIAL | JSON; no APS-200 canonical object schema"; `:7` "**NOT CERTIFIED**".
  - `APS-200:218` and `:224` — the serialization and schema that `integrity_hash` depends on are **TODO**.
  - `APS-200:238` — **no CONF test for ENT-007**; `INVARIANT_REGISTRY.md:283` — "TODO: Define a Conformance Test for INV-012".
  - `SPEC-002:208-211` — the corpus's own architecture note declares hash domains **UNRESOLVED**, blocked on AD-CA-008.
  - **CONFLICT-DQ002-01** — the corpus does not agree with itself on the record-level hash.
  - No fixture anywhere contains a computed hash value (§5.3).
- **Evidence against:** the guard's domains are internally coherent, stable since
  `d03eb65`, executable and independently verifiable *within the guard* — "unnormative"
  understates their engineering maturity. D is a statement about the **relationship**, not
  about implementation quality.
- **Consequences:** DQ-002 closes by *recording* the relationship as undefined and
  specifying what must be defined — no code moves.
- **Migration:** **LOW/NONE.** Nothing changes. **Testing:** unchanged; the pinned digest
  in `tests/d3_chain_observability.rs` stays valid.
- **Serialization:** **none** — D is the only option that does not force DQ-006.
- **Cross-language:** unchanged; the RI-PY/RI-RS divergence is recorded, not resolved.
- **Auditability:** improved — the gap becomes explicit rather than implicit.
- **Security:** neutral — no cryptographic change. **Reversibility:** **VERY HIGH.**
- **Verdict: BEST SUPPORTED.**

---

## 16. Consequences summary

| Dimension | A — One | B — Two-layer | C — Three-domain | D — Unnormative |
|---|---|---|---|---|
| Contradicted by direct evidence | **YES** | partially | count is wrong | no |
| Forces DQ-006 now | **YES** | **YES** | **YES** | **NO** |
| Pre-empts DQ-004 / DQ-005 | yes | **yes** | **yes** | no |
| Survives CONFLICT-DQ002-01 unresolved | no | no | **no** | **yes** |
| Existing `chain_hash` / Merkle / TSA preserved | **no** | yes | yes | **yes** |
| Requires a normative count of domains | 1 | 2 | 3 | none yet |
| Reversibility | VERY LOW | MEDIUM | LOW | **VERY HIGH** |

---

## 17. Migration impact

**Options A/B/C** all require, before a single conformant value can be written: DQ-006
(all ten DEPs), resolution of CONFLICT-DQ002-01, DQ-004 (what "event payload" means), and
DQ-005 (whether `violations` enters an integrity domain). A additionally breaks
`chain_hash`, which re-roots every Merkle segment and invalidates every RFC 3161 token
already issued.

**Option D** requires nothing. Nothing is emitted, nothing is renamed, nothing is
re-rooted. The DQ-001 adapter continues to be specifiable in shape while its
`integrity_hash` output stays blocked — which is the state the accepted DQ-001 decision
already anticipated.

---

## 18. Reversibility

| Option | Rating | Why |
|---|---|---|
| A | **VERY LOW** | Merging domains destroys the order-independence of record identity; once evidence is anchored and timestamped it cannot be unmerged |
| B | **MEDIUM** | A nesting can be re-nested before publication; after external publication the emitted values are referenced facts |
| C | **LOW** | A published domain count and per-domain byte definition become governed artifacts requiring RFC/ADR to change (`VERSIONING.md:40`) |
| **D** | **VERY HIGH** | Records the absence of a relationship. Creates no value, freezes no count, emits no bytes. Every one of A/B/C remains fully available afterward |

**What becomes expensive after D: nothing.** D is the only option under which no future
choice is foreclosed. **What stays expensive regardless of D:** changing `chain_hash`
itself, because Merkle roots (`segment.rs:141`) and RFC 3161 tokens already depend on it
— that cost predates DQ-002 and is unaffected by it.

---

## 19. Agent recommendation (Phase 15)

> ## AGENT RECOMMENDATION — REQUIRES ARCHITECTURE OWNER APPROVAL
>
> ### **OPTION D — the normative relationship between the three hashes has not been established**
>
> …with the **three-domain reading recorded as the implementation finding** that a future
> DQ-002 resolution should normalize, once its blockers clear.
>
> Advisory only. Not a decision. Not approved. DQ-002 is not closed.

**1. What the evidence proves.**

- **FACT.** `chain_hash` has no normative counterpart: 0 occurrences in the entire
  specification corpus, at HEAD and across all history.
- **FACT.** `integrity_hash` and `event_payload_hash` have no implementation: 0
  occurrences in `aura-guard-v1.3`, at HEAD and across all 105 commits.
- **FACT.** The §11 matrix contains **zero MATCH** rows.
- **FACT.** The implementation operates **nine** SHA-256 domains in a real four-level
  dependency stack (§12), stable since `d03eb65` (2026-05-13).
- **FACT.** APS-200 asserts **no dependency** among its three hash fields; the layering
  exists only on the implementation side.
- **FACT.** Domain separation is **PRESENT** in the Merkle layer (`0x00`/`0x01`) and
  **ABSENT** between the entry-chain and segment-chain domains.
- **FACT.** The corpus contradicts itself on the record-level hash
  (**CONFLICT-DQ002-01**), and its own `SPEC-002:208-211` declares hash domains
  **UNRESOLVED**.

**2. What the evidence does not prove.**

- It does **not** prove the three are one concept — A is refuted, not merely unsupported.
- It does **not** prove a two-layer nesting; B is a design choice with no textual basis.
- It does **not** establish that exactly **three** domains are correct: the implementation
  has nine and the corpus has at least eight names.
- It does **not** establish any relationship between POC-A's and the guard's hash models
  (§10), nor between either and APS-200.
- It does **not** establish whether `integrity_hash` includes itself — the two documents
  that address the question disagree.

**3. Which domains should be treated as distinct, IF supported.** On the **implementation
side only**, the evidence supports treating these as distinct domains, because each has a
different input, a different byte representation and a different dependency structure:
**(i)** payload digests (`input_hash`, `shadow_hash`); **(ii)** the entry chain
(`chain_hash`, order-dependent); **(iii)** the RFC 6962 Merkle domain (explicitly
tagged); **(iv)** the segment chain / RFC 3161 imprint. **This is an observation about
existing code, not a proposed normative domain count.** Recording it does not require
approving it.

**4. What must remain deferred.**

- **To DQ-006:** all ten dependencies DEP-1…DEP-10 (§14). No byte-level statement is made.
- **To DQ-005:** whether `violations`, `audit_id`, `request_id`, `schema` enter an
  integrity domain. **Hard-stop condition 6 assessed: NOT triggered** — D is selectable
  *because* it makes no binding claim; A/B/C would each require DQ-005 first, which is
  precisely why they are not recommended.
- **To DQ-004:** the meaning of "the event payload", without which
  `event_payload_hash` cannot be given an input.
- **To the Protocol Custodian:** CONFLICT-DQ002-01.

**5. Reversibility.** **VERY HIGH** — see §18. D records a state of the evidence rather
than creating a cryptographic fact. It is the only option that leaves A, B and C all
fully available, and the only one selectable while CONFLICT-DQ002-01 is open.

**What would falsify this recommendation.**

1. An approved normative text defining `integrity_hash`'s exact input bytes and
   resolving its self-inclusion → C becomes available.
2. A Custodian ruling that `APS-300:69`'s "excluding this field" governs `APS-200:58` →
   removes CONFLICT-DQ002-01, the main blocker to C.
3. Discovery of an approved ADR defining a hash-domain count. **Searched across all three
   repositories, all branches: not found.**
4. A decision that `chain_hash` itself becomes normative (e.g. via `EVIDENCE_SPEC v1.1`,
   guard `docs/ROADMAP.md:80`) → reframes DQ-002 entirely.

---

## 20. Open evidence gaps and hard-stop assessment

### 20.1 Hard-stop conditions

| # | Condition | Triggered? | Disposition |
|---|---|---|---|
| 1 | **Hash semantics differ materially between normative documents** | **YES** | **CONFLICT-DQ002-01** (§5.4): `APS-200:58` `integrity_hash` = "canonical serialization of this object" (self-inclusion unstated → circular); `APS-300:69` `evidence_hash` = "this Evidence object **excluding this field**". Same object class, two names, incompatible self-inclusion; APS-300 §5 also omits four Common Object Contract fields that `APS-200:49` makes mandatory. **Reported and escalated to the Protocol Custodian. Not reconciled.** |
| 2 | APS-200 and SPEC-002 define incompatible hash domains | **NO** | They are **disjoint**, not incompatible — SPEC-002's domains are Vector/Artifact (Constitution), and it mentions none of the three names (§7) |
| 3 | Historical evidence contradicts current normative evidence | **NO** | `chain_hash`'s domain never changed since `d03eb65`; the two vocabularies never intersected, so there is nothing to contradict (§9) |
| 4 | Hash inputs cannot be reconstructed from source | **NO — for the implementation. YES — for the normative side** | All nine guard domains were reconstructed exactly from source (§3). `integrity_hash` and `event_payload_hash` **cannot** be reconstructed — no producer exists and `APS-200:218` marks their serialization TODO. Recorded as **MISSING/UNKNOWN**, never filled by convention |
| 5 | Canonical serialization required to distinguish domains | **PARTIALLY** | **Not** required to distinguish them semantically (record vs payload vs link) — which is what makes D selectable. **Is** required for every byte-level question; all ten isolated in §14 as **DEFER TO DQ-006** |
| 6 | Deciding the hash model requires deciding DQ-005 | **NO for D; YES for A/B/C** | Recorded as a discriminating criterion (§15, §19). No DQ-005 question is answered anywhere in this document |
| 7 | A hash field is cryptographically significant but its construction cannot be established | **YES — for two of the three** | `integrity_hash` (`APS-200:58`) and `event_payload_hash` (`:159`) are both **MUST** fields — cryptographically significant by definition — and neither has an establishable construction. `event_payload_hash` states **no algorithm at all**. This is a principal reason the recommendation is D |
| 8 | A cross-repository relationship is inferred without evidence | **NO** | §10 reports POC-A, guard and APS-200 as three separate models and returns **NOT ESTABLISHED** for every pairing |

**Three conditions (1, 4-partial, 7) are met and reported.** None was resolved by
convention or cryptographic best practice. DQ-002 is **not closed**, and the §19
recommendation is explicitly conditional on Custodian resolution of CONFLICT-DQ002-01.

### 20.2 Gap register

| ID | Gap | Blocks | Owner |
|---|---|---|---|
| HG-1 | CONFLICT-DQ002-01 unresolved | Any normative statement about record-level integrity | Protocol Custodian |
| HG-2 | `integrity_hash` self-inclusion unstated (`APS-200:58`) | Computability of the field | Protocol Custodian |
| HG-3 | `event_payload_hash` states no algorithm and no input (`APS-200:159`) | Any implementation of ENT-007's payload hash | Protocol Custodian |
| HG-4 | "Event payload" undefined in APS-200, APS-000, `GLOSSARY.md` | HG-3 | DQ-004 |
| HG-5 | Canonical serialization TODO (`APS-200:218`) | DEP-1…DEP-10 | DQ-006 |
| HG-6 | `evidence_hash` algorithm TODO (`APS-300:73`) | ENT-005 integrity | Protocol Custodian |
| HG-7 | No CONF test for ENT-007 (`APS-200:238`); INV-012 CONF test TODO (`INVARIANT_REGISTRY.md:283`) | Executable conformance evidence for **any** option | DQ-006 / APS-400 |
| HG-8 | No fixture in the corpus contains a computed hash (§5.3) | Independent reproduction per REQ-002-020 | Protocol Custodian |
| HG-9 | Domain separation ABSENT between D1 and D3; `context` unescaped in D1 | Byte-level adequacy of the entry-chain domain | DQ-006 (byte level) + Architecture Owner (design) |
| HG-10 | `models.rs:95` documents 7 preimage fields; `chain.rs:36-46` implements 9 — **wrong since `d03eb65`** | Documentation accuracy; pre-registered, **not reopened** | DQ-008 |
| HG-11 | POC-A Merkle lacks the domain separation the guard has (§10) | Cross-RI interoperability (`APS-200:218`) | Separate decision |
| HG-12 | AD-CA-007 / AD-CA-008 UNRESOLVED (`SPEC-002:381-382`) | REQ-002-017…022 | Protocol Custodian |

---

## 21. Full evidence references

**Pinned:** `aura-guard-v1.3` `443f72e` · `aura-poc-a-core-v3.3` `98f2f43` ·
`aura-specification` `62d2d6b`.

**Guard:** `src/crypto.rs:8-12,16-20,22-29,44-59`; `src/chain.rs:11,18-20,25-49,53-65,71-92`;
`src/models.rs:38,40,49,65,95,96`; `src/api/audit.rs:19-23,45,82,104-110,113,116-129,131-146`;
`src/api/mod.rs:54,76`; `src/policy.rs:188`; `src/log_writer.rs:88-113,96`;
`src/merkle.rs:1-24,29-34,38-44,48-50`;
`src/segment.rs:67-87,91-118,120-132,140-148,182-189`;
`docs/adrs/0001-hash-chain.md:3,38-45`; `docs/openapi.yaml:91`; `CHANGELOG.md:18,64-72,138,167`;
commits `d03eb65`, `b189a1e`, `31a60de`, `1e801c3`, `025f092`, `51bcdd2`, `70b9881`, `6661982`.

**Specification:** `aps/APS-200_CANONICAL_DATA_MODEL.md:3-6,41,49,58,88,105,121,129,143,156-159,206,213-218,224,238`;
`aps/APS-300_EVIDENCE_MODEL.md:56,59-71,73,91,107,120`;
`aps/APS-100_PROTOCOL_INVARIANTS.md:58,61,64,73,83,89,92`;
`invariants/INVARIANT_REGISTRY.md:241-253,273,283`;
`specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:12,37,186-195,208-216,381-382,412-417`;
`fixtures/schemas/common-object-contract.schema.json:14,48-51`;
`fixtures/core/FIX-001_BASIC_EVALUATION.json:19`; `templates/FIXTURE_TEMPLATE.json:19,20,33,47`;
`conformance/CONF-010_CRYPTOGRAPHIC_VERIFICATION.md:40`; `evidence/README.md:32`;
`reference/RI-RS_AURA_GUARD.md:7,50,52,60`; `reference/RI-PY_AURA_POC_A_CORE.md:27`;
`VERSIONING.md:38,40`; `constitution/AURA_CONSTITUTION.md:80`; commit `b68181e`.

**POC-A:** `audit/merkle.py:14-16,20,38-43,80-85,109,111,143,145,163,233-236,259,261`;
`audit/signing.py:89,110`; `core/merkle.py:8`; `compliance/certificate.py:70`;
`docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` §0, §2.2;
`review/2026-08-11_ENGINEERING_BASELINE/03_LANGUAGE_BOUNDARY.md:49-54`;
`review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/`;
`review/2026-08-15_D3-S4_DQ-001-H_CROSS_REPOSITORY_LINEAGE/`;
commits `befddfa`, `80ec4ad`.

---

## 22. Declarations

- **No production source code was modified** in any repository.
- **No APS-200, APS-100, APS-300, SPEC-002 or existing ADR was modified.**
  `aura-guard-v1.3` and `aura-specification` were **read only**.
- **No test, fixture, serialization, hash algorithm or field name was changed.**
- **No hash redesign was implemented or proposed.** §13.1 records a structural property
  and explicitly declines to propose a mitigation.
- **DQ-002 was not frozen and no decision was made.** DQ-006, DQ-005, DQ-004, DQ-003,
  DQ-007 and DQ-008 are untouched and remain OPEN.
- **No PR was opened. No merge. No freeze.**
- The only change produced by this investigation is this single forensic artifact.
