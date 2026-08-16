# HASH_DOMAIN_MATRIX — D3-S8

**Phase 3.** Rebuilt from source by enumerating **every** `Sha256::`, `sha256_hex`,
`sha256_bytes_hex` and `hashlib.sha256` call site, not from any prior inventory.
**Normative effect: NONE.**

## 1. Enumeration method

**FACT.** `grep -rn "Sha256::\|sha256_hex\|sha256_bytes_hex" src/` over
`aura-guard-v1.3` @ `443f72e` returns every construction site. Each was read and
classified individually. Similarly `grep -rn "hashlib\|json.dumps"` over
`aura-poc-a-core-v3.3` @ `98f2f43`.

## 2. Implementation hash domains — `aura-guard-v1.3` @ `443f72e`

| # | Name | File:line | Algorithm | Input | Field order | Separator | Encoding | Self-inclusion | Prev hash? | Payload? | Violations? | Normative source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G-1 | `input_hash` | `api/audit.rs:109` | SHA-256 | `format!("{} {} {}", context, prompt, response)` | fixed | **space** | UTF-8 → hex | no | no | **YES, raw** | no | `APS-200:88` (ENT-002 — **different entity**) |
| G-2 | `shadow_hash` | `api/audit.rs:110` | SHA-256 | `shadow_normalize(original)` | n/a | n/a | UTF-8 → hex | no | no | YES, normalized | no | **NONE FOUND** |
| G-3 | `policy_hash` | `policy.rs:188` | SHA-256 | **raw policy file bytes** (`sha256_bytes_hex`) | n/a | n/a | raw → hex | no | no | no | no | `APS-200:121` (ENT-004) |
| G-4 | **`chain_hash`** | `chain.rs:36-48` | SHA-256 | **9 fields** | `prev_hash, decision, policy_set, policy_hash, context, input_hash, shadow_hash, seq, timestamp` | **`\|`** (`chain.rs:20`) | UTF-8 → hex | **N/A — not a field of its own preimage** | **YES** (pos. 1) | indirect (digests) | **NO** | **NONE FOUND** |
| G-5 | `genesis_hash` | `crypto.rs:27-29` | SHA-256 | literal `"AURA-GUARD-GENESIS-v1.3"` | n/a | n/a | UTF-8 → hex | no | seed | no | no | **NONE FOUND** |
| G-6 | **`segment_genesis_hash`** | `segment.rs:47-50` | SHA-256 | literal `b"AURA-GUARD-SEGMENT-GENESIS-v1"` | n/a | n/a | raw → hex | no | seed | no | no | **NONE FOUND** |
| G-7 | Merkle `leaf_hash` | `merkle.rs:29-34` | SHA-256 | **`0x00 \|\| data`** where data = hex-decoded `chain_hash` (32 raw bytes) | n/a | **1-byte tag** | raw → `[u8;32]` | no | indirect | no | no | **NONE FOUND** |
| G-8 | Merkle `node_hash` | `merkle.rs:38-44` | SHA-256 | **`0x01 \|\| L \|\| R`** | n/a | **1-byte tag** | raw | no | n/a | no | no | **NONE FOUND** |
| G-9 | `empty_root` | `merkle.rs:48-50` | SHA-256 | `""` | n/a | n/a | raw | no | n/a | no | no | **NONE FOUND** |
| G-10 | `segment_chain_hash` | `segment.rs:109-118`, `sealer.rs:367`, `segment.rs:189` | SHA-256 | **5 fields** | `prev_segment_chain_hash, merkle_root, first_seq, last_seq, sealed_at` | **`\|`** (`segment.rs:105`) | UTF-8 → hex | no | **YES** (pos. 1) | no | no | **NONE FOUND** |
| G-11 | `tsa_message_imprint` | `segment.rs:123-132` | SHA-256 | **identical preimage to G-10** | same | same | UTF-8 → `[u8;32]` | no | inherits | no | no | **NONE FOUND** |
| G-12 | RFC 3161 request digest | `rfc3161.rs:138` | SHA-256 | caller-supplied `preimage` bytes | n/a | n/a | raw → `[u8;32]` | no | n/a | no | no | **NONE FOUND** |
| G-13 | TST verification digests | `tst_verify.rs:657,839` | SHA-256 | TSA message / cert bytes | n/a | n/a | raw | no | n/a | no | no | RFC 3161 (external) |

**Count: 13 distinct SHA-256 construction sites.** Also present but not a hash domain:
Ed25519 detached-signature verification over policy bytes (`crypto.rs:44-59`).

## 3. Implementation hash domains — `aura-poc-a-core-v3.3` @ `98f2f43`

| # | Name | File:line | Algorithm | Input | Domain separation | Normative source |
|---|---|---|---|---|---|---|
| P-1 | `sha256(str)` | `audit/merkle.py:14-16` | SHA-256 | UTF-8 → hex | n/a | `AUDIT_LAYER_SPEC.md:70-91` (repo-local) |
| P-2 | Merkle parent | `audit/merkle.py:163` | SHA-256 | **`left + right` string concatenation** | **ABSENT** — no `0x00`/`0x01` | repo-local |
| P-3 | Merkle proof step | `audit/merkle.py:109,111,259,261` | SHA-256 | `sibling + current` / `current + sibling` | ABSENT | repo-local |
| P-4 | Empty root | `audit/merkle.py:145` | SHA-256 | `""` | n/a | repo-local |
| P-5 | ETC signing payload | `audit/merkle.py:80-85` | HMAC-SHA256 (`signing.py:89`) | `json.dumps({event_hash, merkle_root, timestamp}, sort_keys=True, separators=(",",":"))` | n/a | repo-local |
| P-6 | Leaf generation | `core/merkle.py:8` | SHA-256 | `json.dumps(data, sort_keys=True)` — **no `separators`**, Python default spacing | n/a | **NONE FOUND** |
| P-7 | Certificate fingerprint | `compliance/certificate.py:69-70` | SHA-256 | `json.dumps(self.to_dict(), sort_keys=True)` — **no `separators`** | n/a | **NONE FOUND** |

**FACT — POC-A is internally inconsistent.** P-5 uses compact separators; P-6 and P-7 use
Python's space-padded defaults. These produce **different bytes for the same object**.

## 4. Normative hash fields — `aura-specification` @ `62d2d6b`

| Name | Location | Definition (exact) | Algorithm stated? | Implemented anywhere? |
|---|---|---|---|---|
| `integrity_hash` | `APS-200:58` | "SHA-256 hash of the canonical serialization of this object" | YES | **NO — 0 files, 0 commits in guard; 0 outside `review/` in POC-A** |
| `event_payload_hash` | `APS-200:159` | "Hash of the event payload" | **NO** | **NO — 0 / 0** |
| `previous_record_hash` | `APS-200:158` | "Hash of the previous Audit Record (chain link)" | **NO** | **NO** (concept present as `prev_hash`, name absent) |
| `evidence_hash` | `APS-300:69` | "SHA-256 hash of this Evidence object (**excluding this field**)" | YES | **NO** |
| `previous_evidence_hash` | `APS-300:70` | "Hash of the previous Evidence object (if chain exists)" — **SHOULD** | NO | **NO** |
| `input_hash` | `APS-200:88`, `APS-300:67` | "SHA-256 hash of the canonical input payload" | YES | guard G-1 (different entity scope) |
| `output_hash` | `APS-200:105`, `APS-300:68` | "SHA-256 hash of the canonical output payload" | YES | **NO** |
| `policy_hash` | `APS-200:121` | "SHA-256 hash of the policy content" | YES | guard G-3 |
| `attestation_hash` | `APS-200:143` | "SHA-256 hash of attestation content" | YES | **NO** |
| `chain_hash` | — | — | — | **0 occurrences in the entire corpus, all history** |

## 5. Relationship classification

| Hash / Domain | Implementation | Normative source | Relationship | Status |
|---|---|---|---|---|
| `chain_hash` | G-4 | none | **IMPLEMENTATION ONLY** | EVIDENCE SUFFICIENT (that it is unspecified) |
| `prev_hash` | G-4 field 1 | `previous_record_hash` `APS-200:158` | **DERIVED** — same concept, different name, algorithm unstated normatively | EVIDENCE PARTIAL |
| `integrity_hash` | none | `APS-200:58` | **DIRECTLY SPECIFIED, UNIMPLEMENTED** — and **CONFLICTING** with `APS-300:69` | **CONFLICT** |
| `event_payload_hash` | none | `APS-200:159` | **DIRECTLY SPECIFIED, UNIMPLEMENTED** — input undefined ("event payload" not defined anywhere) | EVIDENCE MISSING |
| `evidence_hash` | none | `APS-300:69` | **DIRECTLY SPECIFIED, UNIMPLEMENTED** — algorithm TODO `APS-300:73` | **CONFLICT** |
| `input_hash` | G-1 | `APS-200:88` (ENT-002) | **DERIVED** — guard's covers `context+prompt+response`; ENT-002's covers "the canonical input payload" of a different entity | EVIDENCE PARTIAL |
| `shadow_hash` | G-2 | none | **IMPLEMENTATION ONLY** | EVIDENCE SUFFICIENT |
| `policy_hash` | G-3 | `APS-200:121` (ENT-004) | **DERIVED** | EVIDENCE PARTIAL |
| `segment_chain_hash` | G-10 | none | **IMPLEMENTATION ONLY** | EVIDENCE SUFFICIENT |
| Merkle leaf/node | G-7/G-8 | none | **IMPLEMENTATION ONLY** (RFC 6962 external) | EVIDENCE SUFFICIENT |
| `tsa_message_imprint` | G-11 | none | **IMPLEMENTATION ONLY** (RFC 3161 external) | EVIDENCE SUFFICIENT |
| genesis constants | G-5, G-6 | none | **IMPLEMENTATION ONLY** | EVIDENCE SUFFICIENT |

**Zero rows are DIRECTLY SPECIFIED **and** implemented.**

## 6. HASH FIELD LINEAGE TABLE

| Field | First appearance | Commit | Repo | Changed since? | Semantic change? |
|---|---|---|---|---|---|
| `chain_hash` | 2026-05-13 | `d03eb65` | guard | **NO** — 9-field preimage byte-identical at `d03eb65` and `443f72e` | **NONE** |
| `prev_hash` | 2026-05-13 | `d03eb65` | guard | no | none |
| `input_hash`, `shadow_hash`, `policy_hash`, `genesis_hash` | 2026-05-13 | `d03eb65` | guard | no | none |
| Merkle leaf/node, `segment_chain_hash`, `segment_genesis_hash` | 2026-05-19 | `31a60de` | guard | no | none — **added above** `chain_hash`, not replacing it (`CHANGELOG.md:64-72`) |
| `tsa_message_imprint` | 2026-05-20 | `1e801c3` | guard | no | none |
| `event_hash` (POC-A) | 2026-01-17 | `80ec4ad` | POC-A | — | — |
| `integrity_hash`, `event_payload_hash`, `previous_record_hash`, `evidence_hash` | **2026-07-23** | `b68181e` | **spec** | no | **never implemented** |

## 7. Special DQ-002 questions — answered independently

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Does APS-200 define `integrity_hash`? | **YES**, as a MUST field of every entity — but by reference to a canonical serialization that `APS-200:218` marks TODO, and **without stating self-exclusion**, making it circular as written | `APS-200:49,58,218` |
| 2 | Does APS-200 define `event_payload_hash`? | **PARTIALLY** — names it MUST, states **no algorithm** and does not define "event payload" | `APS-200:159` |
| 3 | Does APS-200 define `previous_record_hash`? | **PARTIALLY** — names it MUST with the role "chain link", **no algorithm** | `APS-200:158` |
| 4 | Does APS-300 define a conflicting integrity construction? | **YES** — `evidence_hash` "excluding this field" vs `integrity_hash` "of this object". Same object class (ENT-005 is an APS-200 entity per `APS-200:41`; `:129` delegates its fields to APS-300 §5, whose MUST-list **omits** `object_id`, `object_type`, `created_at`, `integrity_hash`) | `APS-200:41,49,58,129`; `APS-300:56,59-71` |
| 5 | Do APS-400/500 resolve any ambiguity? | **NO.** APS-400 contains no hash-domain definition; APS-500 defines fixture *structure* only | `APS-400`, `APS-500:35-44` |
| 6 | Does any fixture define these bytes? | **NO.** `FIX-001:8,17,18,19` = `"TODO"`; `FIXTURE_TEMPLATE.json:19,33` = `"TODO — SHA-256"` | as cited |
| 7 | Does any cross-language test compare the bytes? | **NO.** Not found in inspected scope — CONF-002 "same implementation", CONF-003 "twice… fresh process", CONF-006 "two hardware architectures". `grep -i "cross-impl\|between implementations\|two implementations"` over `aps/APS-400*` and `conformance/` returns **nothing** | `CONF-002:40`, `CONF-003:40`, `CONF-006:40` |
| 8 | Does Aura-Guard implement any of these fields directly? | **NO.** `integrity_hash`, `event_payload_hash`, `previous_record_hash`: **0 files @HEAD, 0 commits in full history** | `git grep` + `git log --all -S` |
| 9 | Does `chain_hash` have a normative relationship to any APS field? | **NO.** `chain_hash` occurs 0 times in the corpus. The only *conceptual* neighbour is `previous_record_hash`, and only via `prev_hash` | corpus grep |
| 10 | Relationship classification | **MISSING for `chain_hash`↔APS; CONFLICT for `integrity_hash`↔`evidence_hash`** | §5 |

## 8. Domain separation — corrected from the prior DQ-002 finding

| Mechanism | Entry chain (G-4) | Segment chain (G-10) | Merkle (G-7/G-8) | Normative model |
|---|---|---|---|---|
| Per-preimage type tag | **ABSENT** | **ABSENT** | **PRESENT** (`0x00`/`0x01`, `merkle.rs:31,40`) | ABSENT |
| Distinct genesis context string | **PRESENT** — `"AURA-GUARD-GENESIS-v1.3"` (`crypto.rs:28`) | **PRESENT** — `b"AURA-GUARD-SEGMENT-GENESIS-v1"` (`segment.rs:48`) | n/a | ABSENT |
| Length prefix | ABSENT | ABSENT | n/a (fixed 32-byte operands) | ABSENT |
| Field escaping | ABSENT | ABSENT | n/a | ABSENT |

**CORRECTION TO PRIOR ANALYSIS.** The D3-S5/DQ-002 artifact recorded domain separation
between the entry chain and the segment chain as flatly **"ABSENT"**. That is an
**overstatement**. `segment.rs:47-50` defines a **second, distinct genesis constant**
(`AURA-GUARD-SEGMENT-GENESIS-v1`) separate from `crypto.rs:28`
(`AURA-GUARD-GENESIS-v1.3`). The two chains are therefore **seeded from different
context strings**, which distinguishes them at the root even though no per-preimage tag
distinguishes them element by element. The accurate classification is **PARTIAL**, not
ABSENT. `segment_genesis_hash` was **absent from the prior inventory entirely**.
