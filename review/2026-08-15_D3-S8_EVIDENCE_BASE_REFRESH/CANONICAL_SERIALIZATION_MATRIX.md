# CANONICAL_SERIALIZATION_MATRIX — D3-S8

**Phase 4.** Every regime re-derived from source. **No canonical format is chosen.**
**Normative effect: NONE.**

## 1. Regime inventory

| Field | **R1** | **R2** | **R2-impl** | **R3** |
|---|---|---|---|---|
| **Regime ID** | Guard entry-chain preimage | POC-A Canonical Event | POC-A JSON canonicalization | APS-200 §8 |
| **Source** | `aura-guard-v1.3` `src/chain.rs:36-47` | `aura-poc-a-core-v3.3` `docs/specs/AUDIT_LAYER_SPEC.md` §1 | `audit/merkle.py:85`, `core/merkle.py:8`, `compliance/certificate.py:69` | `aura-specification` `aps/APS-200_CANONICAL_DATA_MODEL.md:211-218` |
| **Normative / implementation status** | **Implementation only.** `chain_hash` occurs 0× in the APS corpus | **Declared NORMATIVE** (`:4`), Author "Aura Protocol Custodian" (`:8`), "Last Frozen: 2026-07-24" (`:9`) | **Implementation only** — no governing document found | **Normative but deferred** — canonical format is a TODO (`:218`) |
| **Encoding** | UTF-8 (`crypto.rs:10`) | UTF-8, "mandatory" (`:51`) | UTF-8 | **Unstated.** JSON/CBOR/protobuf all MAY (`:213`) |
| **Field order** | Fixed array literal: `prev_hash, decision, policy_set, policy_hash, context, input_hash, shadow_hash, seq, timestamp` (`chain.rs:37-45`) | Fixed, specified: `agent_id, ari, drift, ts` (`:33-41`) | `sort_keys=True` — **lexicographic**, not declaration order | **Unstated** |
| **Separator** | `\|` = `const SEP: &str` (`chain.rs:20`) | `\|` field, `=` key-value (`:52-53`) | JSON `,` — **two variants**: `(",", ":")` at `merkle.py:85`; **Python default `", "`** at `core/merkle.py:8`, `certificate.py:69` | **Unstated** |
| **Timestamp representation** | **`2026-01-01T00:00:00+00:00`** — explicit offset (verified from exported bytes) | **`ts=2026-01-01T00:00:00Z`** — "UTC, **no timezone offset**" (`:41,46`) | ISO-8601, form unspecified | **Unstated** |
| **Optional-field representation** | **Omitted entirely** — `skip_serializing_if = "Option::is_none"` on `request_id` (`models.rs:65`) and `Violation::validator` (`models.rs:40`). *(Neither is inside R1's preimage today.)* | **Not addressed** | Not addressed | **Unstated** — but REQ-002-021 (`SPEC-002:215`) requires it to be defined |
| **Numeric encoding** | `seq`: `u64::to_string()` → **decimal ASCII, unpadded** (`chain.rs:44`) | `ari`, `drift`: **int32 scaled 10^5** (`:39-40`) | JSON number | **Unstated** |
| **Escaping** | **NONE** | **NONE** | JSON string escaping | Unstated |
| **Length prefix / type tag** | NONE | NONE | NONE | Unstated |
| **Unicode normalization** | NONE | Not addressed | Not addressed | Unstated |
| **Hash input** | The joined string's UTF-8 bytes → SHA-256 → lowercase hex (`crypto.rs:8-12`) | Canonical Event string's UTF-8 bytes → SHA-256 → lowercase hex (`:83-91`) | JSON bytes → SHA-256 hex, or HMAC-SHA256 (`signing.py:89`) | `integrity_hash` = "SHA-256 of the canonical serialization" (`:58`) — input undefined |
| **Cross-language verification** | **NOT VERIFIED** — not found in inspected scope | **NOT VERIFIED** | **NOT VERIFIED** | **NOT VERIFIED** |
| **Status** | **EVIDENCE SUFFICIENT** as description of current behaviour; **fails `SPEC-002:195` REQ-002-020** (not reproducible without reading the RI) | **EVIDENCE SUFFICIENT** as a specification; **would satisfy REQ-002-020** for its object | **CONFLICT** — internally inconsistent (two JSON separator conventions) | **EVIDENCE MISSING** |

## 2. The one exported canonical byte stream

**FACT.** `D3_REAL_CHAIN_CANONICAL.bin` exists only on branch
`d3/real-chain-observability` @ `70b9881` (**not an ancestor of `main`**).

**FACT — re-verified independently during D3-S8**, by piping the blob straight from the
object store:

| Property | Value | Method |
|---|---|---|
| Length | **315 bytes** | `git show 70b9881:D3_REAL_CHAIN_CANONICAL.bin \| wc -c` |
| SHA-256 | `6eb514bf3ce334676d894e669e3d9598d594cc7e21c9bb694daad017f8c20222` | `… \| sha256sum` (GNU coreutils — an oracle independent of the Rust code) |

**FACT — field decomposition** (from `od -c`), with widths summing to 315:

`prev_hash`(64) `|` `DENY`(4) `|` `finance-v1`(10) `|` `policy_hash`(64) `|`
`Finance Bot`(11) `|` `input_hash`(64) `|` `shadow_hash`(64) `|` `0`(1) `|`
`2026-01-01T00:00:00+00:00`(25) — eight `U+007C` separators, no leading or trailing
separator, no BOM, no padding.

Arithmetic: 64+1+4+1+10+1+64+1+11+1+64+1+64+1+1+1+25 = **315** ✔

**FACT.** `context` = `Finance Bot` **contains a space** — confirming free-form,
unescaped, unquoted, length-prefix-free text reaches the preimage.

## 3. Is there a single protocol-wide canonical serialization?

**NO — EVIDENCE MISSING.** Four regimes coexist. R1 and R2 agree on separator (`|`),
encoding (UTF-8) and digest form (SHA-256 lowercase hex) and **disagree** on timestamp
form, field labelling and numeric encoding. R2-impl contradicts itself. R3 defers.

**FACT — the regimes govern different objects.** R1 serializes a Guard audit decision;
R2 serializes a POC-A measurement event. **This is not a contradiction about the same
object**, and D3-S8 safety rule 9 forbids merging their semantics merely because
`APS-950:132-133` designates the two repositories RI-PY and RI-RS.

**INFERENCE.** The R1/R2 divergence nonetheless demonstrates that two independently
authored Aura canonicalizations, already convergent on the easy choices, still produce
incompatible bytes. It is evidence about the *difficulty*, not evidence of a same-object
conflict.

## 4. Why the divergence is currently undetectable

| Test | Procedure (exact) | What it verifies |
|---|---|---|
| CONF-003 (INV-003) | "Serialize ENT-001 through ENT-008 objects **twice independently (fresh process each time)**" (`:40`); "Both serializations MUST be byte-identical" (`:46`) | **Intra-implementation determinism** |
| CONF-002 (INV-002) | "replay the execution **on the same implementation**" (`:40`) | **Intra-implementation replay** |
| CONF-006 (INV-006) | "Run FIX-001 on **two different hardware architectures**" (`:40`) | **Same implementation, different CPU** |
| INV-014 | Conformance Test = **`— (TODO)`** (`INVARIANT_REGISTRY.md:319`) | nothing — no test exists |

**FACT.** `INVARIANT_REGISTRY.md:51` states INV-002 as reproduction "**on every
conformant implementation**"; `:75` states INV-003's rationale as "Multiple valid
serializations of the same object would produce different hashes, breaking integrity
verification"; `:323` calls fixtures "**the cross-implementation comparability
mechanism**".

**INFERENCE.** The invariants state a cross-implementation requirement; the tests verify
only the intra-implementation property; and the mechanism named to close the gap
(fixtures) has no test and **no computed values** (`FIX-001:8,17,18,19` = `"TODO"`).

## 5. Governing-direction contradiction (bears on which regime could ever govern)

| Source | Statement | Status |
|---|---|---|
| `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md:17-19` | "Implementation is the source of truth. If this document conflicts with the implementation, **the implementation governs** and this document must be corrected." | Declared **NORMATIVE**, Author "Aura Protocol Custodian" |
| `aura-specification/README.md:17` | "**If documentation and implementation disagree, documentation wins.**" | README, unversioned |
| `aura-specification/specification/SPEC-002…:37` | "This direction **MUST NOT be reversed**. Implementation behaviour does not constitute normative evidence…" | **"Normative effect: NONE until APPROVED"** (`:12`), Owner "Protocol Custodian" |

**CONFLICT.** Two documents attributed to the same role state opposite directions of
authority, and the question they disagree about is exactly which regime could become
canonical. **Not reconciled here.**
