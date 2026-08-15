# D3-S6 / DQ-006 — Canonical Serialization / Canonical Bytes

**Question:** what is, and what should be, the canonical byte sequence fed to the protocol's hash functions
**Document class:** forensic serialization and byte-level analysis. **Normative effect: NONE.**
**Prepared by:** Claude, analysis agent. **Not** the Architecture Owner.
**Date:** 2026-08-15
**Status:** **PROPOSED / NOT APPROVED**
**Code changed:** NO. **Normative documents changed:** NO. **DQ-006 decision:** NOT MADE.

---

## 0. Premise, authority and method

### 0.1 Premise as instructed

| Decision | State carried into this document |
|---|---|
| **DQ-001** | **ACCEPTED — Option B, explicit adapter architecture.** Frozen. |
| **DQ-002** | **OPEN — not yet decided.** Confirmed with the Architecture Owner before this analysis began. The hash-domain model is therefore treated as **undetermined**, and every byte question that cannot close until DQ-002 resolves is marked **BLOCKED BY DQ-002**. |
| **CONFLICT-DQ002-01** | **UNRESOLVED** — escalated to the Protocol Custodian in `review/2026-08-15_D3-S5_DQ-002_LAYERED_HASH_DOMAINS/`. |
| DQ-005, DQ-004, DQ-003, DQ-007, DQ-008 | OPEN, untouched. |

**Consequence of DQ-002 being open.** DQ-006 asks "what are the canonical bytes?" That
question is well-posed only *per hash domain*. With the domain model undetermined, this
document can establish **what bytes exist today**, **what the corpus requires of them**,
and **what must be decided** — but it cannot enumerate one canonical byte sequence per
domain, because the domain set is not settled. This is stated once here and not repeated
as a caveat on every finding.

### 0.2 Authority boundary

Confirmed with the Architecture Owner: this is a **forensic analysis package**, not an
authoring exercise. **No normative canonical serialization is authored here**, and none
is proposed as text. Options are evaluated; none is selected.

### 0.3 Labels and pinned revisions

**FACT** (verifiable at a cited `file:line` in a pinned revision, or produced by an
executed command) · **INFERENCE** (derived from FACTs, no normative weight) · **UNKNOWN**.
Negative results read *"not found in inspected scope"*.

| Repository | Revision | State |
|---|---|---|
| `AuraIDToken/aura-guard-v1.3` | `443f72e` (+ branch `d3/real-chain-observability` @ `70b9881`) | full history, read-only |
| `AuraIDToken/aura-poc-a-core-v3.3` | `98f2f43` | full history (unshallowed in DQ-001-H) |
| `AuraIDToken/aura-specification` | `62d2d6b` | full history, read-only |

---

## 1. Executive summary

**There is no canonical serialization in the Aura Protocol. There are three
canonicalization regimes, authored independently, that disagree at the byte level — and
the corpus's own conformance machinery cannot detect the disagreement.**

**FACT — one real canonical byte sequence exists, and I reproduced it.** Branch
`d3/real-chain-observability` @ `70b9881` carries `D3_REAL_CHAIN_CANONICAL.bin`: **315
bytes**, SHA-256 `6eb514bf3ce334676d894e669e3d9598d594cc7e21c9bb694daad017f8c20222`.
Both were **independently re-verified during this audit** by `wc -c` and GNU coreutils
`sha256sum` against the blob read straight out of the object store. This is the only
artifact anywhere in the three repositories containing an actual canonical byte stream.

**FACT — the three regimes.**

| Regime | Where | Shape | Status |
|---|---|---|---|
| **R1 — Guard entry chain** | `aura-guard-v1.3` `chain.rs:36-47` | 9 fields, **positional**, `"\|"`-joined, UTF-8 | implementation only; **no specification** |
| **R2 — POC-A Canonical Event** | `aura-poc-a-core-v3.3` `docs/specs/AUDIT_LAYER_SPEC.md` §1 | 4 fields, **`key=value`**, `"\|"`-joined, UTF-8 | **declared NORMATIVE**, "Last Frozen: 2026-07-24" |
| **R3 — APS-200 §8** | `aura-specification` `aps/APS-200_CANONICAL_DATA_MODEL.md:213-218` | formats **MAY** differ (JSON/CBOR/protobuf) | **canonical format is a TODO** |

**FACT — R1 and R2 disagree on a concrete, demonstrable byte.** Both use `"|"` and UTF-8
and SHA-256-lowercase-hex. They disagree on timestamp representation:

| Regime | Timestamp form | Evidence |
|---|---|---|
| R2 (POC-A, normative) | `ts=2026-01-01T00:00:00Z` — "UTC, **no timezone offset**" | `AUDIT_LAYER_SPEC.md:41,46` |
| R1 (guard, implemented) | `2026-01-01T00:00:00+00:00` — **explicit `+00:00` offset** | `D3_REAL_CHAIN_CANONICAL.bin`, verified this audit |

**INFERENCE.** These encode the same instant and produce different bytes, therefore
different digests. RFC 3339 permits both forms; neither regime cites the other. This is
not a hypothetical cross-language hazard — it is present in the two artifacts today.

**FACT — HARD STOP: the authority direction is contradicted, on this exact question.**

| Source | Statement |
|---|---|
| `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md:17-19` | "**Implementation is the source of truth.** If this document conflicts with the implementation, **the implementation governs** and this document must be corrected." |
| `aura-specification/README.md:17` | "**If documentation and implementation disagree, documentation wins.**" |
| `aura-specification/specification/SPEC-002…:37` | "This direction **MUST NOT be reversed**. **Implementation behaviour does not constitute normative evidence** unless an approved governance artifact explicitly grants that implementation normative authority." |

Both `AUDIT_LAYER_SPEC.md` (`:8`, "Author: Aura Protocol Custodian") and SPEC-002 (`:7`,
"Owner: Protocol Custodian") are attributed to the **same role**, and they state opposite
directions of authority — on the document that defines canonical bytes. **Reported, not
reconciled (§13).**

**FACT — the corpus cannot detect a canonicalization divergence.** CONF-003, the only
conformance test for INV-003 Canonical Serialization, reads: "Serialize ENT-001 through
ENT-008 objects **twice independently (fresh process each time)**… Both serializations
MUST be byte-identical" (`CONF-003:40,46`). That tests **intra-implementation
determinism**, not canonicality. **Two implementations could each pass CONF-003 while
producing entirely different bytes.** CONF-002 replays "on the **same** implementation"
(`CONF-002:40`); CONF-006 compares "two different **hardware architectures**"
(`CONF-006:40`). **No
conformance test in the corpus compares two implementations' bytes** — not found in
inspected scope.

**Answer:** canonical bytes are **NOT ESTABLISHED** protocol-wide. One regime is
executable and fully reconstructible (R1); one is declared normative but describes a
different object and disagrees with R1 (R2); the specification defers the question
entirely (R3).

**AGENT RECOMMENDATION — REQUIRES ARCHITECTURE OWNER APPROVAL: Option 3 — define
canonical bytes per hash domain, deferred until DQ-002 fixes the domain set**, with the
R1 byte sequence recorded now as a *characterized baseline* rather than adopted as the
canonical form. See §11.

---

## 2. Scope

**In scope.** Every byte-producing serialization path that feeds a hash; the normative
requirements bearing on canonical form; the divergences between them.

**Explicitly not decided here.** No canonical format is selected. No encoding, ordering,
numeric representation or optional-field rule is chosen. Specifically deferred:

| To | What |
|---|---|
| **DQ-002** | The hash-domain set — how many canonical byte sequences are required, and for what |
| **DQ-005** | Whether `violations`, `audit_id`, `request_id`, `schema` enter any canonical form |
| **DQ-004** | What "the event payload" denotes, and therefore what a payload canonical form covers |
| **DQ-003** | Version markers inside or alongside canonical bytes |
| **DQ-007** | Numeric representation — `seq` encoding, and the `f32` in `Violation` |
| **Protocol Custodian** | CONFLICT-DQ002-01, and CONFLICT-DQ006-01/02 raised here |

---

## 3. The one real canonical byte sequence (R1), verified

**FACT — independent re-verification performed during this audit**, not quoted from the
prior report:

```
$ git show 70b9881:D3_REAL_CHAIN_CANONICAL.bin | wc -c
315
$ git show 70b9881:D3_REAL_CHAIN_CANONICAL.bin | sha256sum
6eb514bf3ce334676d894e669e3d9598d594cc7e21c9bb694daad017f8c20222
```

**FACT — the byte stream, decomposed** (from `od -c` of the blob):

| # | Field | Bytes | Width | Encoding observed |
|---|---|---|---|---|
| 1 | `prev_hash` | `b93b4ade…3623562d` | 64 | lowercase hex; here = `genesis_hash()` |
| 2 | `decision` | `DENY` | 4 | bare ASCII, **variable width**, no quoting |
| 3 | `policy_set` | `finance-v1` | 10 | bare ASCII, **variable width**, no quoting |
| 4 | `policy_hash` | `5e9ab2b2…f082b35d` | 64 | lowercase hex |
| 5 | `context` | `Finance Bot` | 11 | **free-form, contains a space, unescaped, unquoted, no length prefix** |
| 6 | `input_hash` | `c2e55221…a3dd1413a` | 64 | lowercase hex |
| 7 | `shadow_hash` | `534b346b…455c12a6` | 64 | lowercase hex |
| 8 | `seq` | `0` | 1 | **decimal ASCII, variable width, unpadded** (`u64::to_string()`) |
| 9 | `timestamp` | `2026-01-01T00:00:00+00:00` | 25 | **RFC 3339 with explicit `+00:00`, not `Z`** |

Separators: eight single `U+007C`. **No leading or trailing separator. No BOM, no length
prefix, no padding, no type tag, no version marker, no Unicode normalization.**

Arithmetic check (performed this audit): 64+1+4+1+10+1+64+1+11+1+64+1+64+1+1+1+25 = **315**. ✔

**FACT — R1's byte-level properties.**

| Property | Value | Evidence |
|---|---|---|
| Text or bytes | **Text** — a Rust `String` from `[&str; 9]::join` | `chain.rs:36-47` |
| Encoding | UTF-8 via `str::as_bytes()` | `crypto.rs:10` |
| Field order | Fixed array literal order, **unchanged since `d03eb65` (2026-05-13)** | `chain.rs:37-45` |
| Value transformation | **Only** `seq`: `u64::to_string()`. The other eight verbatim | `chain.rs:44` |
| Digest encoding | Lowercase hex, 64 chars | `crypto.rs:11` |
| Escaping | **NONE** | `chain.rs:36-47` |

**FACT — R1 is fully reconstructible from source.** `compute_chain_hash` takes all nine
fields as explicit parameters and reads no ambient state (`chain.rs:25-49`); the clock,
sequence and head dependencies live in its caller (`api/audit.rs:116-118`). **Hard-stop
condition "hash inputs cannot be reconstructed from source" is NOT triggered for R1.**

**FACT — provenance and standing of the artifact.** `70b9881` is Claude-authored,
2026-08-15, on branch `d3/real-chain-observability`, **not an ancestor of `main`**. Its
commit body records identical digests before and after instrumentation and pins the value
in `tests/d3_chain_observability.rs`. **INFERENCE:** it is a characterization record of
existing behaviour, not a normative artifact, and it carries no authority. Its factual
claims (315 bytes, the digest) were re-verified here against an independent oracle.

**FACT — R1 has no specification.** `chain_hash` occurs **0 times** in the entire
`aura-specification` corpus, at HEAD and across all history (established in DQ-002 §1 and
re-confirmed here). The nine-field order and the `"|"` separator exist **only** in
`chain.rs`.

---

## 4. The second canonical regime (R2) — POC-A's declared normative spec

**FACT.** `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md`:
**Document Status: NORMATIVE** (`:4`), Version 1.0.0, **Author: Aura Protocol Custodian**
(`:8`), **Last Frozen: 2026-07-24** (`:9`).

**FACT — §1.2 Canonical Event required fields**, in fixed order, `"|"`-separated:

| Position | Field | Type | Note |
|---|---|---|---|
| 1 | `agent_id` | string | MACHINE_ACCOUNT identifier |
| 2 | `ari` | int32 | scaled by 10^5 |
| 3 | `drift` | int32 | scaled by 10^5 |
| 4 | `ts` | ISO-8601 | **"UTC, no timezone offset"** (`:41`) |

**FACT — the normative example** (`:46`):
`agent_id=MACHINE_ACCOUNT_001|ari=95000|drift=5000|ts=2026-01-01T00:00:00Z`

**FACT — §1.3 serialisation rules** (`:51-56`): UTF-8 mandatory; field separator `|`;
**key-value separator `=`**; no trailing newline; no leading/trailing whitespace; fixed
field order. **§2.3** (`:88-91`): UTF-8 bytes → SHA-256 → lowercase 64-char hex.

**INFERENCE — R2 is a genuine, complete canonical-bytes specification.** It is the only
document in any of the three repositories that specifies encoding, separator, ordering,
whitespace and digest representation together. It is more complete on canonical bytes
than APS-200 is.

### 4.1 R1 vs R2 — byte-level comparison

| Dimension | R1 (guard, implemented) | R2 (POC-A, declared normative) | Same? |
|---|---|---|---|
| Encoding | UTF-8 | UTF-8 (`:51`) | **YES** |
| Field separator | `\|` (`chain.rs:20`) | `\|` (`:52`) | **YES** |
| Digest | SHA-256, lowercase hex 64 | SHA-256, lowercase hex 64 (`:88-91`) | **YES** |
| Field labelling | **positional, no keys** | **`key=value`** (`:53`) | **NO** |
| Timestamp | `…+00:00` (verified §3) | `…Z`, "no timezone offset" (`:41,46`) | **NO** |
| Field set | 9 audit-decision fields | 4 measurement fields | **NO** — different objects |
| Numeric encoding | `u64::to_string()` decimal | int32 scaled 10^5 (`:39-40`) | **NO** |
| Escaping | none | none | same gap |
| Trailing newline | none | explicitly none (`:54`) | **YES** |

**INFERENCE.** R1 and R2 are **convergent in mechanism and divergent in every detail that
determines bytes.** They describe different objects — a Guard audit decision versus a
POC-A measurement event — so this is not a contradiction *about the same object*. But it
demonstrates that two independently-authored Aura canonicalizations, both using `"|"` and
UTF-8, still disagree on `Z` vs `+00:00`, on keyed versus positional fields, and on
numeric encoding. **INFERENCE:** absent a single normative definition, convergence on the
easy choices does not produce byte compatibility.

---

## 5. The specification's position (R3) — APS-200 and the invariants

### 5.1 APS-200 §8

**FACT** (`aps/APS-200_CANONICAL_DATA_MODEL.md:211-218`):

> Implementations **MAY** use different formats (JSON, CBOR, Protocol Buffers), provided:
> - Full model semantics are preserved
> - Deterministic serialization is guaranteed **where required by the protocol**
> - INV-003 (Canonical Serialization) is not violated
>
> **TODO**: Define the canonical serialization format for interoperability between RI-PY and RI-RS.

**FACT.** `APS-200:224` — "**TODO**: Publish JSON Schema definitions for each entity."

**INFERENCE.** APS-200 grants format freedom and then names the resulting interoperability
gap as an open item against itself. The phrase "where required by the protocol" is not
resolved anywhere: **not found in inspected scope** — no APS document states where
deterministic serialization *is* required.

### 5.2 The invariants

| Invariant | Requirement text | Designated test | What the test actually does |
|---|---|---|---|
| **INV-003** Canonical Serialization | `APS-100:65` "Every protocol object MUST have an unambiguous serialization representation"; `INVARIANT_REGISTRY.md:73` "…unambiguous **canonical** serialization" | **CONF-003** | "Serialize … **twice independently (fresh process each time)**" (`CONF-003:40`) — **intra-implementation determinism** |
| **INV-002** Bit-Perfect Replay | `INVARIANT_REGISTRY.md:51` "…MUST reproduce an identical Evaluation Result **on every conformant implementation**" | **CONF-002** | "replay the execution **on the same implementation**" (`CONF-002:40`) — **intra-implementation** |
| **INV-006** Platform Independence | conformant results regardless of platform | **CONF-006** | "two different **hardware architectures**" (`CONF-006:40`) — **same implementation, different CPU** |
| **INV-014** Reference Compatibility | `INVARIANT_REGISTRY.md:321` "MUST pass all applicable Reference Fixtures"; rationale `:323` "**Fixtures are the cross-implementation comparability mechanism**" | **— (TODO)** (`:319`) | no test exists |

### 5.3 CONFLICT-DQ006-01 — the invariants require cross-implementation equality; no test verifies it

**FACT.** INV-002's requirement is explicitly cross-implementation ("on **every**
conformant implementation", `INVARIANT_REGISTRY.md:51`). Its designated conformance test
CONF-002 verifies replay "on the **same** implementation" (`CONF-002:40`).

**FACT.** INV-003's rationale states the purpose plainly (`INVARIANT_REGISTRY.md:75`):
"Cryptographic hashes require a canonical byte representation. **Multiple valid
serializations of the same object would produce different hashes, breaking integrity
verification.**" Its designated test CONF-003 compares an implementation only against
itself.

**FACT.** INV-014 — the invariant whose own rationale names it "the cross-implementation
comparability mechanism" — has **no conformance test** (`INVARIANT_REGISTRY.md:319`,
`— (TODO)`), and **APS-500 fixtures contain no computed values**: `FIX-001…:19`
`"input_hash": "TODO"`; `templates/FIXTURE_TEMPLATE.json:19,33` `"integrity_hash": "TODO — SHA-256"`.

**INFERENCE.** The corpus states the cross-implementation requirement in its invariants
and verifies only the intra-implementation property in its tests. **A conformance run
that fully passed CONF-002, CONF-003 and CONF-006 would establish nothing about whether
RI-PY and RI-RS produce the same bytes** — which is the exact property `APS-200:218`
flags as its open TODO. **Reported, not reconciled (§13).**

### 5.4 SPEC-002 — the method, and its scope limit

**FACT.** `SPEC-002:12` — "**Normative effect: NONE until APPROVED.**"

**FACT.** `SPEC-002:215` **REQ-002-021** — the future specification MUST define **exactly
one** canonical serialization format, "including field set, field order, encoding, and
representation of absent or optional fields."

**FACT.** `SPEC-002:216` **REQ-002-022** — MUST define **exactly one** canonical byte
sequence **per hash domain, per representation**; separate representations are "**SEPARATE
definitions**… and **MUST NOT be treated as a single universal byte sequence**". Required
per representation: representation-to-bytes transformation, field ordering, encoding,
numeric representation, **absent or optional field handling**, byte-level boundaries,
hash-domain membership.

**FACT.** `SPEC-002:195` **REQ-002-020** — definitions MUST suffice for an independent
implementer to reproduce the exact byte sequence "**without inspecting any Reference
Implementation**."

**FACT.** `SPEC-002:382` — **AD-CA-008** ("Canonical serialization format, canonical byte
sequence, and hash domain definitions") is **UNRESOLVED**, "Blocks REQ-002-017 through
REQ-002-022".

**INFERENCE — REQ-002-020 is the sharpest available test of the current state, and R1
fails it.** R1's field order and separator exist only in `chain.rs`; an independent
implementer cannot reproduce the 315-byte sequence without reading the Rust source. R2
would *pass* REQ-002-020 for its own object, since `AUDIT_LAYER_SPEC.md` §1.2-§1.3 is
implementation-independent.

**FACT — scope limit.** SPEC-002's subject is the Constitution Artifact/Vector. It
mentions `AuditEntry`, `Audit Record`, `ENT-007`, `chain_hash`, `integrity_hash`,
`event_payload_hash` **zero times each** (established in DQ-002 §7, re-confirmed). Its
requirements are **methodologically on point and formally out of scope**.

---

## 6. POC-A's implemented canonicalization (R2-impl) vs its own spec

**FACT — POC-A's implemented canonicalization is JSON-based, not the `"|"` Canonical
Event form:**

| Site | Construction |
|---|---|
| `audit/merkle.py:85` | `json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")` — ETC signing payload |
| `core/merkle.py:8` | `hashlib.sha256(json.dumps(data, sort_keys=True).encode())` — **no `separators`**, so Python's default `", "` / `": "` **with spaces** |
| `compliance/certificate.py:69` | `json.dumps(self.to_dict(), sort_keys=True)` — **no `separators`** |
| `scripts/generate_determinism_report.py:101` | `json.dumps(etc_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")` |

**FACT — POC-A is internally inconsistent about JSON canonicalization.** Two sites pass
`separators=(",", ":")` (compact) and two do not (default, space-padded). These produce
**different bytes for the same object**.

**INFERENCE.** POC-A therefore has *three* serialization behaviours in play: the declared
`"|"`-joined Canonical Event (`AUDIT_LAYER_SPEC.md` §1), compact JSON, and default-spaced
JSON. **Not found in inspected scope:** any document reconciling them, or stating which
governs which object.

**FACT.** POC-A's Merkle parent hashing is plain concatenation, `sha256(left + right)`
(`audit/merkle.py:163`), with no RFC 6962 `0x00`/`0x01` tags — versus the guard's tagged
construction (`merkle.rs:31,40`). Established in DQ-002 §10; **not re-litigated**, noted
because it is a canonical-bytes divergence.

---

## 7. Canonical-bytes comparison matrix

| Dimension | R1 Guard entry chain | R2 POC-A Canonical Event (spec) | R2-impl POC-A JSON | R3 APS-200 | Classification |
|---|---|---|---|---|---|
| Normative status | **none** — implementation only | **declared NORMATIVE**, frozen 2026-07-24 | none | **TODO** (`:218`) | **CONFLICT** on which governs |
| Container | flat delimited string | flat delimited string | JSON object | JSON/CBOR/protobuf all **MAY** | **NOT ESTABLISHED** |
| Encoding | UTF-8 | UTF-8 | UTF-8 | unstated | **MATCH** (R1/R2) |
| Field separator | `\|` | `\|` | JSON `,` (two variants) | unstated | **MATCH** (R1/R2) |
| Field labelling | positional | `key=value` | JSON keys | unstated | **CONFLICT** |
| Field ordering | fixed array order | fixed, specified | `sort_keys=True` | unstated | **CONFLICT** (declaration vs lexicographic) |
| Timestamp | `+00:00` **(verified)** | `Z`, "no offset" | ISO-8601 unspecified | unstated | **CONFLICT** |
| Integer encoding | decimal ASCII, unpadded | int32 scaled 10^5 | JSON number | unstated | **CONFLICT** |
| Optional-field handling | **omitted entirely** (`skip_serializing_if`, `models.rs:40,65`) | not addressed | not addressed | unstated | **UNRESOLVED — DQ-006 core** |
| Escaping | none | none | JSON escaping | unstated | **UNRESOLVED** |
| Length prefix / type tag | none | none | none | unstated | **ABSENT everywhere** |
| Unicode normalization | none | not addressed | not addressed | unstated | **UNRESOLVED** |
| Digest encoding | lowercase hex 64 | lowercase hex 64 | lowercase hex 64 | "string" | **MATCH** |
| Reproducible without reading the RI? | **NO** | **YES** | NO | n/a | **R1 fails REQ-002-020** |

**Zero rows are MATCH across all three regimes.** Four dimensions match between R1 and R2;
six conflict; three are unresolved everywhere.

---

## 8. The optional-field problem — DQ-006's hardest concrete case

**FACT.** `models.rs:65` — `AuditEntry::request_id` carries
`#[serde(default, skip_serializing_if = "Option::is_none")]`.
`models.rs:40` — `Violation::validator` carries the same.

**FACT.** The field is therefore **omitted entirely** from the JSONL line when `None`,
rather than serialized as `null`.

**INFERENCE — this is the single most consequential open byte question, and it is
currently invisible.** Neither `request_id` nor `violations` is an input to `chain_hash`
(`chain.rs:36-47`), so today the omission cannot affect a digest. **The moment any
canonical form covers the whole record — which is exactly what
`integrity_hash` (`APS-200:58`) requires — "absent" and "present-but-null" become two
different byte sequences for the same logical record.**

**FACT.** REQ-002-021 (`SPEC-002:215`) and REQ-002-022 (`:216`) both explicitly require
"representation of absent or optional fields" to be defined. **Not found in inspected
scope:** any statement of that rule in APS-200, APS-300, `AUDIT_LAYER_SPEC.md`, or any ADR.

**Status: BLOCKED BY DQ-002** (whether a whole-record domain exists at all) **and
DQ-005** (whether `violations` is in it).

---

## 9. Historical trace

| Date | Commit | Repo | Change | Interpretation |
|---|---|---|---|---|
| 2026-01-17 | `80ec4ad` | POC-A | ETC + JSON `sort_keys` canonicalization introduced | **FACT.** POC-A's JSON regime predates everything else |
| **2026-05-13** | **`d03eb65`** | Guard | **R1's 9-field `"\|"` preimage present in full at first commit** | **FACT.** R1 has been **byte-stable for its entire existence** — no migration, no reordering, no separator change |
| 2026-05-19 | `31a60de` | Guard | `segment_chain_preimage` added — a **second** `"\|"`-joined regime (5 fields) | **FACT.** The delimited-string pattern was reused, not specified |
| 2026-07-23 | `b68181e` | Spec | APS-200 §8 created **already containing** the `:218` TODO | **FACT.** The canonical-format gap is not a regression; it shipped open |
| **2026-07-24** | — | POC-A | `AUDIT_LAYER_SPEC.md` "Last Frozen", declared NORMATIVE with the implementation-governs clause | **FACT.** Frozen **one day after** APS-200 was created. **UNKNOWN:** whether its author knew of APS-200 §8 |
| 2026-08-14 | `39ecd2f` | POC-A | P0-6 **D-3 CLOSED — DECISION DOMAIN**; **"D-3 concrete semantic value: NOT ESTABLISHED"** | **FACT.** Governance has explicitly closed the *process* and explicitly **not** established the *value* |
| 2026-08-15 | `70b9881` | Guard | R1 preimage exported and pinned; digest identical before/after | **FACT.** Characterization only, unmerged branch |

**FACT — the P0-6 governance boundary is directly binding on DQ-006.**
`review/2026-08-14_P0_6_D3_D4_DECISION_RECORD/D3_D4_DECISION_RECORD.md` §5 lists as
explicit non-decisions: "canonical byte encoding", "serialization format", "ordering
rule", "float representation", "hash-domain representation". §7 states those values
"**cannot be inferred** from this closure record… **cannot be supplied by an implementing
agent**… cannot be treated as settled by any downstream package that cites this record."

**INFERENCE.** This document is such a downstream package. It therefore records R1's
bytes as **characterized fact about existing code**, and at no point treats them as an
established canonical value. That distinction is the reason §11 recommends deferral
rather than adoption.

---

## 10. Architectural options

### OPTION 1 — Adopt R1 (the guard's existing 315-byte form) as the canonical serialization

- **For:** it exists, is executable, is byte-stable since 2026-05-13, is fully
  reconstructible from source, and has a pinned regression test. Zero migration for the guard.
- **Against:** **decisive.** It fails REQ-002-020 — not reproducible without reading the
  Rust source. It covers 9 of 14 `AuditEntry` fields, so it cannot serve a whole-record
  domain such as `integrity_hash`. It has no escaping, no length prefix and no type tag
  (§12). It is guard-specific: POC-A has no `decision`, `policy_set`, `shadow_hash` or
  chain link. Adopting it would make the implementation the source of truth — the exact
  direction `SPEC-002:37` forbids and CONFLICT-DQ006-02 disputes.
- **Consequences:** POC-A must adopt a foreign shape or be declared out of scope.
- **Migration:** LOW for guard, **VERY HIGH** for POC-A. **Testing:** guard tests unchanged.
- **Serialization dependency:** none — it *is* the serialization. **Cross-language:** poor.
- **Auditability:** good for the guard, nil protocol-wide. **Security:** inherits the §12 gaps.
- **Reversibility:** **VERY LOW** once evidence is anchored to it.

### OPTION 2 — Adopt R2 (POC-A's declared Canonical Event) as the canonical serialization

- **For:** it is the **only** implementation-independent canonical-bytes specification in
  the ecosystem; it satisfies REQ-002-020 for its object; it is already declared NORMATIVE
  and frozen; it specifies encoding, separator, ordering, whitespace and digest form.
- **Against:** its four fields (`agent_id`, `ari`, `drift`, `ts`) describe a **measurement
  event**, not an audit record — it cannot express `decision`, `policy_hash`, `context` or
  a chain link. Its `key=value` form and `Z` timestamp both conflict with R1 (§4.1),
  so adopting it **breaks every existing guard digest**. Its own authority clause
  (`:17-19`) subordinates it to POC-A's implementation, which contradicts its normative status.
- **Consequences:** the guard's chain, Merkle roots and RFC 3161 tokens all re-root.
- **Migration:** **VERY HIGH.** **Testing:** every guard fixture and the pinned digest invalidated.
- **Cross-language:** good in principle. **Auditability:** good. **Security:** same §12 gaps.
- **Reversibility:** **VERY LOW.**

### OPTION 3 — Define canonical bytes **per hash domain**, deferred until DQ-002 fixes the domain set

- **For:** it is what `REQ-002-022` already requires — "exactly one canonical byte
  sequence for each … representation within its respective hash domain … **MUST NOT be
  treated as a single universal byte sequence**". It matches the observed reality: the
  guard already runs four stacked domains with **different** byte disciplines (delimited
  UTF-8 at the entry and segment layers; tagged raw bytes in the Merkle layer). It
  forecloses nothing. It respects the P0-6 boundary by not supplying a value governance
  has recorded as NOT ESTABLISHED. It is the only option that survives DQ-002 being open.
- **Against:** it does not produce canonical bytes **today** — the deliverable is a
  decision framework, not a byte sequence. It is contingent on DQ-002 closing first.
- **Consequences:** DQ-006 closes by fixing the *method* and the *required content* per
  domain, and by recording R1 as a characterized baseline. No bytes move.
- **Migration:** **NONE now.** **Testing:** unchanged; the pinned digest stays valid.
- **Serialization dependency:** self-referential by design — it sequences the work.
- **Cross-language:** best — a per-domain definition is what would finally let RI-PY and
  RI-RS be compared, and would close `APS-200:218`.
- **Auditability:** improved — the gap becomes explicit and enumerated.
- **Security:** neutral now; enables the §12 gaps to be addressed per domain later.
- **Reversibility:** **VERY HIGH.**

### OPTION 4 — Declare canonical serialization out of scope for the Aura Protocol

- **For:** `APS-200:213` already permits differing formats; if implementations never need
  byte equality, no canonical form is required.
- **Against:** **directly contradicted by four normative statements** — INV-003 (`APS-100:65`),
  INV-002's "every conformant implementation" (`INVARIANT_REGISTRY.md:51`), INV-014's
  cross-implementation rationale (`:323`), and `APS-200:218`'s own TODO. It would also
  make `integrity_hash` (`APS-200:58`) permanently uncomputable.
- **Reversibility:** LOW — withdrawing a stated invariant requires a new APS version.
- **Verdict: REFUTED by evidence.**

---

## 11. Agent recommendation

> ## AGENT RECOMMENDATION — REQUIRES ARCHITECTURE OWNER APPROVAL
>
> ### **OPTION 3 — define canonical bytes per hash domain, deferred until DQ-002 fixes the domain set**
>
> …with **R1's 315-byte sequence recorded as a characterized baseline**, explicitly **not**
> adopted as the canonical form.
>
> Conditional on Protocol Custodian resolution of **CONFLICT-DQ006-02** (authority
> direction) and **CONFLICT-DQ002-01**.
>
> Advisory only. Not a decision. Not approved. DQ-006 is not closed.

**1. What the evidence proves.**

- **FACT.** Exactly one real canonical byte sequence exists in the ecosystem: 315 bytes,
  digest `6eb514bf…0222`, independently re-verified this audit.
- **FACT.** It has **no specification** — `chain_hash` appears 0 times in the corpus — and
  fails REQ-002-020's independent-reproduction test.
- **FACT.** A second regime (R2) is **declared normative and frozen**, is implementation-
  independent, and disagrees with R1 on timestamp form, field labelling and numeric encoding.
- **FACT.** APS-200 defers the question (`:218` TODO) while its invariants require the
  property, and **no conformance test in the corpus compares two implementations**.
- **FACT.** POC-A is internally inconsistent about JSON canonicalization (§6).
- **FACT.** Governance has recorded the D-3 canonical-representation **semantic value as
  NOT ESTABLISHED** and forbidden downstream packages from supplying it.

**2. What the evidence does not prove.**

- It does **not** establish how many canonical byte sequences the protocol needs — that is
  DQ-002.
- It does **not** establish whether R1's bytes are *correct*, only that they are stable,
  reconstructible and undocumented.
- It does **not** establish that R1 and R2 contradict each other *about the same object* —
  they describe different objects (§4.1).
- It does **not** establish any exploitable consequence of the missing escaping (§12).

**3. Which canonical form should be treated as authoritative, IF supported.** **None
yet.** On the evidence, R2 is the better *model* of how a canonical-bytes specification
should be written — implementation-independent, complete on encoding/order/whitespace —
and R1 is the better *baseline of what is actually running*. Recording both, and adopting
neither, is what the evidence supports.

**4. What must remain deferred.**

- **To DQ-002:** the domain set, hence the number of canonical byte sequences (§0.1).
- **To DQ-005:** whether `violations`, `audit_id`, `request_id`, `schema` are inside any
  canonical form — which determines whether §8's optional-field question becomes live.
- **To DQ-004:** what "the event payload" is, hence what a payload canonical form covers.
- **To DQ-007:** `seq` encoding and the `f32` `confidence`.
- **To the Protocol Custodian:** CONFLICT-DQ006-01, CONFLICT-DQ006-02, CONFLICT-DQ002-01.

**5. Reversibility. VERY HIGH.** Option 3 emits no bytes, adopts no format, and freezes no
value. R1's digests, Merkle roots and RFC 3161 tokens are untouched; the pinned test stays
green. Options 1, 2 and 4 all remain fully available afterward. Options 1 and 2 are each
VERY LOW reversibility, because each anchors evidence to a byte form while APS-200 is
still `1.0-DRAFT` and "may change freely" (`VERSIONING.md:38`).

**What would falsify this recommendation.**

1. A Custodian ruling that `AUDIT_LAYER_SPEC.md`'s implementation-governs clause is void
   and APS-200 §8 governs → the path opens for a specification-first canonical form.
2. A DQ-002 resolution establishing a single universal hash domain → Option 1 or 2 becomes
   coherent, since only one byte sequence would then be needed.
3. Discovery of an approved ADR defining canonical bytes. **Searched across all three
   repositories, all branches: not found.**
4. A decision that RI-PY and RI-RS need not interoperate → Option 4 becomes available.

---

## 12. Byte-level structural findings (recorded, not remediated)

**No cryptographic redesign is proposed. These are properties of existing byte forms.**

| # | Finding | Status |
|---|---|---|
| B-1 | R1 has **no escaping** of the `"\|"` separator, and `context` is caller-supplied verbatim (`api/audit.rs:140`) with no validation found in `validators.rs`/`config.rs`. The verified sample contains a space (`Finance Bot`), confirming free-form content reaches the preimage | **ABSENT.** Carried from DQ-002 §13; exploitability **NOT ESTABLISHED** and not pursued |
| B-2 | R1 and the segment regime share an untagged `"\|"`-joined UTF-8 shape with no domain separator between them | **ABSENT** |
| B-3 | R2 likewise specifies no escaping of `\|` or `=` (`AUDIT_LAYER_SPEC.md:51-56`) — an `agent_id` containing either would be ambiguous | **ABSENT** |
| B-4 | No regime uses length prefixes or type tags. The Merkle layer is the sole exception (`0x00`/`0x01`, `merkle.rs:31,40`) | **ABSENT except Merkle** |
| B-5 | No regime specifies Unicode normalization (NFC/NFD). Both R1 and R2 hash UTF-8 bytes of free-form text | **UNRESOLVED** |
| B-6 | `seq` is variable-width decimal ASCII, unpadded (`chain.rs:44`; verified as `0`, 1 byte) — a fixed-width or big-endian encoding would produce different bytes | **DEFER TO DQ-007** |
| B-7 | `chain.rs:11` states the preimage is "unambiguous" because of the separator; `chain.rs:18-19` scopes that claim to hex/base64/timestamp characters, which does not cover `context` | **Documentation over-claim.** Recorded; adjacent to HG-10 (DQ-002), which is DQ-008 territory |

---

## 13. Hard-stop assessment and conflicts

| # | Condition | Triggered? | Disposition |
|---|---|---|---|
| Hash inputs not reconstructible from source | **NO for R1/R2; YES for R3** | R1 reconstructed exactly and re-verified (§3); R2 fully specified (§4). APS-200's canonical form is **TODO** and cannot be reconstructed — recorded as UNKNOWN, never filled by convention |
| Normative sources materially disagree | **YES ×2** | **CONFLICT-DQ006-01** (§5.3) and **CONFLICT-DQ006-02** (below) |
| Deciding canonical bytes requires deciding DQ-002 | **YES** | Explicit in §0.1. This is the primary reason Option 3 is recommended over 1/2 |
| Deciding canonical bytes requires deciding DQ-005/DQ-004/DQ-007 | **YES, for a whole-record form** | §8, B-6. All left open |
| Evidence insufficient to distinguish implemented from normative bytes | **NO** | R1 (implemented), R2 (declared normative), R3 (deferred) are cleanly separated throughout |
| Cross-repository relationship inferred without evidence | **NO** | R1, R2 and R3 are reported as three separate regimes; §7 returns NOT ESTABLISHED across them |

### CONFLICT-DQ006-01 — invariants require cross-implementation byte equality; no conformance test verifies it

| Field | Content |
|---|---|
| Source A | `INVARIANT_REGISTRY.md:51` (INV-002) — "on **every conformant implementation**"; `:75` (INV-003 rationale) — "Multiple valid serializations … would produce different hashes, breaking integrity verification"; `:323` (INV-014 rationale) — "Fixtures are the cross-implementation comparability mechanism" |
| Source B | `CONF-002:40` — "on the **same** implementation"; `CONF-003:40` — "twice independently (**fresh process each time**)"; `CONF-006:40` — "two different **hardware architectures**"; INV-014's test = **TODO** (`:319`) |
| Subject | Whether canonical serialization is verified across implementations |
| Consequence | An implementation could pass every canonical-serialization conformance test in the corpus while being byte-incompatible with the other RI — the precise failure `APS-200:218` exists to prevent |
| Resolution mechanism in corpus | None found. APS-400 defines no cross-implementation procedure |
| **Status** | **UNRECONCILED. Escalated to the Protocol Custodian.** |

### CONFLICT-DQ006-02 — opposite authority directions, on the canonical-bytes document itself

| Field | Content |
|---|---|
| Source A | `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md:17-19` — "**Implementation is the source of truth.** If this document conflicts with the implementation, **the implementation governs**". Document Status **NORMATIVE** (`:4`), Author "**Aura Protocol Custodian**" (`:8`), Last Frozen 2026-07-24 (`:9`) |
| Source B | `aura-specification/README.md:17` — "**If documentation and implementation disagree, documentation wins**"; `SPEC-002:37` — "This direction **MUST NOT be reversed**. Implementation behaviour does not constitute normative evidence…". Owner "**Protocol Custodian**" (`SPEC-002:7`) |
| Subject | Which governs the canonical byte definition — the specification or the code |
| Apparent precedence | Undeterminable. Both are attributed to the Protocol Custodian role. Source B's own document carries "Normative effect: NONE until APPROVED" (`SPEC-002:12`), while Source A declares itself NORMATIVE and frozen |
| Why material to DQ-006 | Under A, R1's implemented bytes are authoritative by virtue of existing, and DQ-006 reduces to documenting `chain.rs`. Under B, R1 has no standing at all and canonical bytes must be specified before implementation. **The two readings produce opposite DQ-006 outcomes** |
| Relationship to prior findings | Same family as OQ-A-CONFLICT-001/002 (`review/2026-08-12_OQ-A_GOVERNANCE_JURISDICTION/10_CONFLICT_REGISTER.md`), but **distinct**: those concern document hierarchy, this concerns the doc-vs-code direction on a specific frozen artifact |
| **Status** | **UNRECONCILED. Escalated to the Protocol Custodian.** |

---

## 14. Open evidence gaps

| ID | Gap | Blocks | Owner |
|---|---|---|---|
| CG-1 | CONFLICT-DQ006-02 — authority direction on canonical bytes | Any DQ-006 outcome | Protocol Custodian |
| CG-2 | CONFLICT-DQ006-01 — no cross-implementation conformance test | Verifying any canonical form once defined | Protocol Custodian / APS-400 |
| CG-3 | CONFLICT-DQ002-01 unresolved; DQ-002 open | The domain set, hence the number of byte sequences | Protocol Custodian / DQ-002 |
| CG-4 | `APS-200:218` canonical format TODO | R3 having any content | Protocol Custodian |
| CG-5 | `APS-200:224` no published JSON Schema | Machine-checkable canonical form | Protocol Custodian |
| CG-6 | Optional-field representation undefined (REQ-002-021/022 require it) | Any whole-record canonical form | DQ-006 + DQ-005 |
| CG-7 | Unicode normalization unspecified in every regime | Byte equality over non-ASCII text | DQ-006 |
| CG-8 | Escaping unspecified in R1 and R2 | Unambiguity by construction | DQ-006 |
| CG-9 | POC-A internally inconsistent on JSON `separators` (§6) | POC-A's own byte determinism | Separate decision |
| CG-10 | `APS-200:215` "where required by the protocol" never resolved | Knowing which objects need determinism | Protocol Custodian |
| CG-11 | All APS-500 fixtures carry `TODO` instead of computed values | REQ-002-020 independent reproduction | Protocol Custodian |
| CG-12 | AD-CA-008 UNRESOLVED (`SPEC-002:382`) | REQ-002-017…022 | Protocol Custodian |
| CG-13 | `AUDIT_LAYER_SPEC.md` frozen 2026-07-24, one day after APS-200; relationship never stated | Whether R2 is in or out of APS jurisdiction | Architecture Owner |

---

## 15. Implementation impact

**Nothing is implemented. This is anticipatory only.**

| Area | Option 1 (adopt R1) | Option 2 (adopt R2) | **Option 3 (recommended)** |
|---|---|---|---|
| `chain.rs` | NOT REQUIRED | **REQUIRED** — breaks every digest | **NOT REQUIRED** |
| `models.rs` | NOT REQUIRED | **REQUIRED** | **NOT REQUIRED** |
| Merkle / segment / RFC 3161 | NOT REQUIRED | **REQUIRED** — full re-root | **NOT REQUIRED** |
| POC-A `audit/`, `core/` | **REQUIRED** | POSSIBLE | **NOT REQUIRED** |
| `AUDIT_LAYER_SPEC.md` | **REQUIRED** (contradicted) | NOT REQUIRED | POSSIBLE — annotate relationship to APS-200 |
| APS-200 §8 | **REQUIRED** (Custodian only) | **REQUIRED** (Custodian only) | **REQUIRED eventually** (Custodian only) |
| CONF-003 / APS-400 | POSSIBLE | POSSIBLE | **REQUIRED** — CG-2 |
| APS-500 fixtures | **REQUIRED** | **REQUIRED** | BLOCKED BY DQ-002 |
| DQ-001 adapter | BLOCKED BY DQ-002 | BLOCKED BY DQ-002 | BLOCKED BY DQ-002 |
| Tests / pinned digest | unchanged | **invalidated** | **unchanged** |

---

## 16. Evidence references

**Guard:** `src/chain.rs:11,18-20,25-49,36-47,44`; `src/crypto.rs:8-12,10,11`;
`src/models.rs:40,65,95`; `src/api/audit.rs:116-118,140`; `src/merkle.rs:31,40`;
`src/segment.rs:91-106`; `tests/d3_chain_observability.rs`;
`D3_REAL_CHAIN_CANONICAL.bin` and `D3_REAL_CHAIN_OBSERVABILITY_REPORT.md` @ `70b9881`
(branch `d3/real-chain-observability`, not an ancestor of `main`); commits `d03eb65`,
`31a60de`, `70b9881`.

**Specification:** `aps/APS-200_CANONICAL_DATA_MODEL.md:58,211-218,224`;
`aps/APS-100_PROTOCOL_INVARIANTS.md:61,65`;
`aps/APS-500_REFERENCE_FIXTURES.md:16,24-27`;
`invariants/INVARIANT_REGISTRY.md:51,73,75,319,321,323`;
`conformance/CONF-002_REPLAY_VERIFICATION.md:40`;
`conformance/CONF-003_CANONICAL_SERIALIZATION.md:40,46`;
`conformance/CONF-006_PLATFORM_INDEPENDENCE.md:40`;
`specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:7,12,25-37,195,215,216,382`;
`fixtures/core/FIX-001_BASIC_EVALUATION.json:19`; `templates/FIXTURE_TEMPLATE.json:19,33`;
`README.md:17`; `VERSIONING.md:38`; commit `b68181e`.

**POC-A:** `docs/specs/AUDIT_LAYER_SPEC.md:4,8,9,17-19,33-41,46,51-56,83-91`;
`audit/merkle.py:85,163`; `core/merkle.py:8`; `compliance/certificate.py:69`;
`compliance/renderer.py:30`; `scripts/generate_determinism_report.py:101`;
`review/2026-08-14_P0_6_D3_D4_DECISION_RECORD/D3_D4_DECISION_RECORD.md` §5, §6, §7;
`review/2026-08-12_OQ-A_GOVERNANCE_JURISDICTION/10_CONFLICT_REGISTER.md`;
`review/2026-08-15_D3-S5_DQ-002_LAYERED_HASH_DOMAINS/`; commits `80ec4ad`, `39ecd2f`.

---

## 17. Declarations

- **No production source code was modified** in any repository.
- **No APS document, SPEC-002, `AUDIT_LAYER_SPEC.md`, or existing ADR was modified.**
  `aura-guard-v1.3` and `aura-specification` were **read only**.
- **No canonical serialization was authored, selected, or proposed as normative text.**
- **No test, fixture, hash algorithm, encoding or field name was changed.**
- **DQ-006 was not frozen and no decision was made.** DQ-002, DQ-005, DQ-004, DQ-003,
  DQ-007 and DQ-008 remain OPEN and untouched. DQ-002 was **not** resolved in passing.
- The P0-6 boundary was respected: **no D-3 semantic value is asserted or inferred**
  anywhere in this document.
- **No PR was opened. No merge. No freeze.**
- The only change produced by this investigation is this single forensic artifact.
