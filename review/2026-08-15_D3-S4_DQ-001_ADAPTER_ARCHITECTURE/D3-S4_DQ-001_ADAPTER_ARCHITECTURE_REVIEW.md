# D3-S4 / DQ-001 — Adapter Architecture Review

**Question:** `AuditEntry` ↔ APS-200 ENT-007 / Common Object Contract
**Document class:** forensic architecture / repository analysis. **Normative effect: NONE.**
**Prepared by:** Claude, acting as forensic architecture/repository analysis agent (Aura-Guard v1.3), under `CLAUDE.md` conformance-audit role.
**Date:** 2026-08-15
**Authority:** Claude is **not** the Architecture Owner. Nothing in this document decides, freezes, or closes DQ-001.
**Code changed:** NO. **Normative documents modified:** NO. **ADR approved:** NO.

---

## 0. Reading rules and labels

Every material statement below carries one of five labels. Only **FACT** is verified.

| Label | Meaning |
|---|---|
| **FACT** | Verifiable at a cited `file:line` in a pinned commit, or produced by an executed command |
| **OBSERVATION** | A consequence derived from FACTs; carries no normative weight |
| **ALTERNATIVE** | One of several defensible designs; listed, never selected |
| **RECOMMENDATION (NON-NORMATIVE)** | Advisory opinion of the analysis agent. Not a decision. Not approved. |
| **OPEN DECISION** | Reserved to the Architecture Owner / Protocol Custodian; unresolved here |

### 0.1 Evidence sources and pinned revisions

| Source | Repository | Pinned revision | Role |
|---|---|---|---|
| APS-000/100/200/300/950, INVARIANT_REGISTRY, TRACEABILITY_MATRIX, SPEC-002, Constitution, fixtures/schemas | `AuraIDToken/aura-specification` | `62d2d6b` (`docs(spec-002): SPEC-002 v0.3-DRAFT …`) | Normative / spec corpus |
| `src/models.rs`, `src/chain.rs`, `src/api/audit.rs`, `src/log_writer.rs`, `src/segment.rs`, `src/sealer.rs`, `docs/openapi.yaml`, `docs/adrs/` | `AuraIDToken/aura-guard-v1.3` | `443f72e` (`Update codeql.yml`) | Current implementation of `AuditEntry` |
| `review/**`, `docs/ADR_P0_6_*`, `AGENTS.md`, `CLAUDE.md`, `docs/GAP-001.md` | `AuraIDToken/aura-poc-a-core-v3.3` | `98f2f43` (`Merge pull request #65 …`) | Prior audit record / governance |

**FACT — repository resolution note.** The task names `src/models.rs`. No `.rs` file
of that path exists in `aura-poc-a-core-v3.3`; the repository contains zero Rust
source files. `AuditEntry` is defined in a **different repository**,
`AuraIDToken/aura-guard-v1.3`, at `src/models.rs:50`. This attribution is
independently corroborated by the prior audit record
`review/2026-08-11_ENGINEERING_BASELINE/03_LANGUAGE_BOUNDARY.md:49` and
`docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md:69` (both cite `AuditEntry` at
`src/models.rs:50` in `aura-guard-v1.3`). The referent of DQ-001 is therefore
unambiguous. Filing this review in `aura-poc-a-core-v3.3` follows the precedent set
by `docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md:0` §0 ("filed here as the **audit
record** only").

**FACT — task-premise identifiers not found.** The strings `DQ-001`, `D3-S7` and
`D3-S4` occur **zero times** across `aura-poc-a-core-v3.3` @ `98f2f43`,
`aura-specification` @ `62d2d6b`, and `aura-guard-v1.3` @ `443f72e` (all branches,
full history). The decision ordering DQ-001→…→DQ-008 attributed to D3-S7 is
therefore an **unverifiable premise** carried from the task instruction. It is
accepted as scoping input only; it is not treated as evidence. The `D3_REAL_CHAIN_*`
artifacts in `aura-guard-v1.3` history refer to **P0-6 decision D-3**
(canonical representation), a different identifier space.

---

## 1. Executive conclusion

**FACT.** APS-200 ENT-007 and the Common Object Contract were both located and are
quoted verbatim in §3. Neither hard-stop condition ("cannot be located") is met.

**FACT.** `AuditEntry` (`aura-guard-v1.3` `src/models.rs:50-97`) carries **14 fields**.
ENT-007 requires **10 MUST fields** (6 from the Common Object Contract, 4 entity-specific).
Of the 10, **2** have a concept-and-representation match, **4** are derived, **1** is in
conflict, and **3** have no representation at all. **7** of `AuditEntry`'s fields have no
ENT-007 counterpart.

**FACT.** The string `APS-200`, `APS-100`, `ENT-007`, `object_id`, `object_type`,
`protocol_version`, `schema_version` and `integrity_hash` occur **zero times** across
`aura-guard-v1.3` `src/`, `tests/` and `docs/` @ `443f72e`. There is **no adapter, no
mapping layer, and no protocol binding of any kind** in the implementation.

**FACT.** The word `adapter` occurs **zero times** in the entire `aura-specification`
repository @ `62d2d6b`. No normative adapter or extension mechanism is defined.

**OBSERVATION — the AS-IS answer.** As implemented today, `AuditEntry` is **none of
A, B or C**. It is an unconnected, repository-local domain object with no declared,
documented or executable relationship to ENT-007. The spec corpus states this in its
own words: `reference/RI-RS_AURA_GUARD.md:74` lists "**No canonical APS-200 data
model objects**" as a Key Gap, `:26` records RI-001 as `PARTIAL — no APS-200 canonical
object headers`, and `:62` records INV-015 as `❌ — No APS-000 identifiers in evidence
objects`. DQ-001 is therefore not a question about what the code *is*; it is a
question about what binding the Architecture Owner **elects to create**.

**OBSERVATION — the decisive normative sentence.** `APS-200:16` states:

> "Every conformant implementation MUST represent information in accordance with this
> document. **Internal structures MAY differ, but data semantics and contract MUST be
> equivalent.**"

This is the highest-ranked located text bearing directly on DQ-001. It **does not
require** structural identity, and it **explicitly permits** an internal structure that
differs from the canonical model provided semantics and contract are equivalent. A
structure that may differ but must be semantically equivalent is, definitionally, a
structure reached through a **mapping**. This sentence is evidence *against* Option A
being mandatory and evidence *for* an explicit mapping boundary.

**FACT — a material normative conflict was detected and is NOT reconciled here.**
INV-012 is stated in two normative-corpus documents with **different scope**:

| Source | Text |
|---|---|
| `aps/APS-100_PROTOCOL_INVARIANTS.md:92` | "Every protocol-governed execution MUST leave an **audit trail** conformant with APS requirements." |
| `invariants/INVARIANT_REGISTRY.md:273` | "Every protocol-governed execution MUST leave an **Audit Record (ENT-007)** conformant with APS requirements." |

This is a hard-stop condition ("normative sources conflict materially"). It is
**reported, not worked around** — see §9 and §16.1. Per `CLAUDE.md` §"Authority
Precedence", a conflict is escalated, never silently reconciled.

**AGENT RECOMMENDATION — REQUIRES ARCHITECTURE OWNER APPROVAL:** **Option B**
(explicit adapter), conditional on Custodian resolution of CONFLICT-DQ001-01. See §13.

---

## 2. Current implementation trace (Phase 1)

**Definition:** `aura-guard-v1.3` @ `443f72e`, `src/models.rs:49-97`.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]   // models.rs:49
pub struct AuditEntry {                            // models.rs:50
```

### 2.1 Complete field set

| # | Field | Type | Line | Producer | Consumers | Semantic purpose | Externally visible | Crypto-relevant | Documented as normative |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `schema` | `String` | `models.rs:52` | `api/audit.rs:132` literal `"aura-guard.audit.v1"` | JSONL reader `log_writer.rs:137,162`; `/health` echo `api/health.rs:43` | Vendor schema tag of the entry | **Yes** (HTTP body + JSONL) | **No** — not in `chain.rs:36-47` | No |
| 2 | `seq` | `u64` | `models.rs:55` | `api/audit.rs:116` ← `log.next_seq()` | `chain.rs:44`; `segment.rs:143`; `sealer.rs` | Monotonic per-log ordinal, 0-based | **Yes** | **Yes** — `chain.rs:44` | No |
| 3 | `audit_id` | `String` | `models.rs:58` | `api/audit.rs:134` (UUIDv4) | log lines, error path `api/audit.rs:152` | Unique per-request identifier | **Yes** | **No** | No |
| 4 | `request_id` | `Option<String>` | `models.rs:66` | `api/audit.rs:135` ← `X-Request-ID` header | tracing `api/audit.rs:153` | Cross-service correlation | **Yes** (omitted when `None`, `models.rs:65`) | **No** | No |
| 5 | `timestamp` | `String` | `models.rs:69` | `api/audit.rs:117` `Utc::now().to_rfc3339()` | `chain.rs:45` | RFC 3339 UTC decision time | **Yes** | **Yes** — `chain.rs:45` | No |
| 6 | `decision` | `String` | `models.rs:72` | `api/audit.rs:113` `evaluate(…)` | `chain.rs:38`; metrics `api/audit.rs:160` | `DENY` / `REVIEW` / `ALLOW` | **Yes** | **Yes** — `chain.rs:38` | No |
| 7 | `policy_set` | `String` | `models.rs:75` | `api/audit.rs:138` ← `policy.name` | `chain.rs:39` | Policy pack evaluated | **Yes** | **Yes** — `chain.rs:39` | No |
| 8 | `policy_hash` | `String` | `models.rs:78` | `api/audit.rs:139` ← `policy.policy_hash` | `chain.rs:40` | SHA-256 of policy file (provenance pin) | **Yes** | **Yes** — `chain.rs:40` | No |
| 9 | `context` | `String` | `models.rs:81` | `api/audit.rs:140` ← request verbatim | `chain.rs:41` | Caller-supplied context string | **Yes** | **Yes** — `chain.rs:41` | No |
| 10 | `input_hash` | `String` | `models.rs:84` | `api/audit.rs:109` `sha256_hex(context+prompt+response)` | `chain.rs:42` | SHA-256 of original input payload | **Yes** | **Yes** — `chain.rs:42` | No |
| 11 | `shadow_hash` | `String` | `models.rs:87` | `api/audit.rs:110` over `shadow_normalize(…)` | `chain.rs:43` | SHA-256 of normalized regex surface | **Yes** | **Yes** — `chain.rs:43` | No |
| 12 | `violations` | `Vec<Violation>` | `models.rs:90` | `api/audit.rs:113` `evaluate(…)` | HTTP response; JSONL | Rule matches explaining the decision | **Yes** | **NO** — absent from `chain.rs:36-47` | No |
| 13 | `prev_hash` | `String` | `models.rs:93` | `api/audit.rs:118` `log.current_head()` | `chain.rs:37`, `chain.rs:71` | Previous entry's `chain_hash` (chain link) | **Yes** | **Yes** — `chain.rs:37` | No |
| 14 | `chain_hash` | `String` | `models.rs:96` | `api/audit.rs:119-129` `compute_chain_hash(…)` | `chain.rs:53,71`; `segment.rs:141` Merkle leaf | Tamper-evidence digest | **Yes** | **Yes** (is the digest) | No |

`Violation` (`models.rs:31-42`): `rule: String`, `action: String`, `confidence: f32`
(`:38` — the only float in the persisted record), `validator: Option<String>` with
`skip_serializing_if = "Option::is_none"` (`:40` — omitted entirely when `None`).

### 2.2 Production sites

| Concern | Location | FACT |
|---|---|---|
| **Construction** | `api/audit.rs:131-146` | The single construction site. All 14 fields populated inline; `schema` hard-coded. |
| **Serialization** | `#[derive(Serialize, Deserialize)]` `models.rs:49`; `log_writer.rs:96` `serde_json::to_string` | serde-JSON default field order = declaration order. No canonicalizer. |
| **Deserialization** | `log_writer.rs:137`, `log_writer.rs:162` | `serde_json::from_str` per JSONL line. |
| **Hashing** | `chain.rs:25-49` `compute_chain_hash`; `chain.rs:53-…` `recompute_for_entry` | 9 fields, `"\|"`-joined (`chain.rs:20` `SEP`), then SHA-256. |
| **Persistence** | `log_writer.rs:88-113` `append` | Append-only JSONL + `sync_data`; fail-closed halt flag. |
| **API exposure** | `api/audit.rs:45` returns `Json<AuditEntry>`; `docs/openapi.yaml:91` schema `AuditEntry` | The struct **is** the public HTTP contract *and* the on-disk format (`models.rs:44-48`). |
| **Verification** | `chain.rs:71` `verify_chain`; `src/bin/aura_replay.rs` | Linear recompute-and-compare. |
| **Evidence batching** | `segment.rs:140-157` `entry_leaf_hash` / `segment_merkle_root` | Merkle leaf = `leaf_hash(hex_decode(chain_hash))` — the leaf covers only `chain_hash`. |
| **Mapping to another object** | — | **NONE EXISTS.** |

### 2.3 Chain coverage

**FACT.** `chain.rs:36-47` hashes exactly nine fields:
`prev_hash`, `decision`, `policy_set`, `policy_hash`, `context`, `input_hash`,
`shadow_hash`, `seq`, `timestamp`.

**FACT.** Not covered (4, excluding the self-referential `chain_hash`):
`violations`, `audit_id`, `request_id`, `schema`.

**FACT.** `chain.rs:11-12` asserts "Tampering with any field — *or with the order of
records* — breaks the chain." That statement is inaccurate as written. This is a
pre-existing, already-registered finding
(`docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` §2.2, status CONFIRMED); it is
**not reopened, re-decided or corrected here**.

---

## 3. APS-200 / ENT-007 trace (Phase 2)

**Located:** `aura-specification` @ `62d2d6b`, `aps/APS-200_CANONICAL_DATA_MODEL.md`.
Document ID `APS-200`, Version `1.0-DRAFT`, Status **DRAFT**, Classification
"Normative Specification", Authority `APS-001 · APS-100` (`:3-7`).

### 3.1 Common Object Contract — `APS-200:47-58` (verbatim)

> ## 4. Common Object Contract
> Every entity MUST contain the following fields:

| Field | Type | Requirement | Description | Line |
|---|---|---|---|---|
| `object_id` | string | MUST | Globally unique identifier (UUID v4 or canonical format) | `:53` |
| `object_type` | string | MUST | APS-000 canonical type name (e.g., `EvaluationRequest`) | `:54` |
| `protocol_version` | string | MUST | APS version this object conforms to (e.g., `1.0`) | `:55` |
| `schema_version` | string | MUST | Schema version of this entity definition | `:56` |
| `created_at` | string (ISO 8601) | MUST | Timestamp of object creation (UTC) | `:57` |
| `integrity_hash` | string | MUST | SHA-256 hash of the canonical serialization of this object | `:58` |

Machine-readable counterpart: `fixtures/schemas/common-object-contract.schema.json`,
`"_status": "TODO — pending finalization of APS-200"`. All six fields in `required`.
`additionalProperties` is **not set** (JSON Schema default `true`). `object_type` is an
`enum` whose Audit-Record member is the literal **`"AuditRecord"`**.

### 3.2 ENT-007 — `APS-200:149-159` (verbatim)

> ### ENT-007 — Audit Record
> **Purpose**: Immutable record of a single auditable event.

| Field | Type | Requirement | Description | Line |
|---|---|---|---|---|
| Common Object Contract fields | — | MUST | See §4 | `:155` |
| `event_type` | string | MUST | Canonical event type | `:156` |
| `sequence_number` | integer | MUST | Monotonically increasing sequence number within a session | `:157` |
| `previous_record_hash` | string | MUST | Hash of the previous Audit Record (chain link) | `:158` |
| `event_payload_hash` | string | MUST | Hash of the event payload | `:159` |

Supporting definitions: `APS-200:42` (entity table), `APS-000:46-47` TERM-008,
`glossary/GLOSSARY.md:21-22`, traceability `APS-200:238` (`ENT-007 | INV-012 |
EVID-AUDIT | —` — **no CONF test**).

### 3.3 The ten questions

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Is ENT-007 a concrete schema? | **Partially.** A concrete *field table*; no published JSON Schema. | `APS-200:153-159`; `:224` "**TODO**: Publish JSON Schema definitions for each entity" |
| 2 | Is it an abstract/common contract? | **Both.** ENT-007 is concrete; §4 Common Object Contract is a mixin applied to every entity. | `APS-200:49`, `:155` |
| 3 | Is it prescriptive? | **Yes as to semantics and contract; explicitly NOT as to internal structure.** | `APS-200:16` |
| 4 | Is every field mandatory? | **Yes.** All 10 are MUST. No SHOULD/MAY field exists on ENT-007. | `APS-200:53-58`, `:155-159` |
| 5 | Are additional fields permitted? | **Yes, by design principle; not by an explicit ENT-007 clause.** §2 "**Extensible** — new fields MAY be added without breaking existing contracts" (`:25`). The schema fixture leaves `additionalProperties` unset (default `true`). **No clause forbids extra fields.** | `APS-200:25`; `fixtures/schemas/common-object-contract.schema.json` |
| 6 | Are field names normative? | **UNRESOLVED.** Names are given in normative MUST tables, but `:16` permits differing internal structures and `:213` permits differing formats, without stating whether names survive the mapping. No clause resolves this. | `APS-200:16`, `:53-58`, `:213` |
| 7 | Are field semantics normative? | **Yes, unambiguously.** "data semantics and contract MUST be equivalent"; §2 "**Unambiguous** — no field has multiple valid interpretations". | `APS-200:16`, `:23` |
| 8 | Does ENT-007 define an extension mechanism? | **NO.** No extension mechanism, no `extensions` field, no profile mechanism, no adapter clause. `APS-100:148-156` "Extension Rules" governs new **Invariants**, not object fields. | `APS-200:149-159`; `APS-100:148-156` |
| 9 | Does APS-200 explicitly require direct implementation? | **NO — the opposite.** `:16` explicitly permits differing internal structures. | `APS-200:16` |
| 10 | Does APS-200 permit adapters or domain-specific representations? | **It permits the *outcome* an adapter produces; it does not name or define an adapter.** `:16` permits differing internal structure under semantic equivalence; `:213-216` permits differing serialization formats under preserved semantics. The word "adapter" occurs **zero times** in the entire repository. | `APS-200:16`, `:213-216`; repo-wide grep |

### 3.4 Additional binding APS-200 clauses

**FACT.** `APS-200:203-207` §7 Validation Rules — every object MUST pass: structure
validation (required fields present), type validation, required-field validation,
integrity validation (`integrity_hash` matches computed hash), APS-100 invariant
validation. **OBSERVATION:** this attaches to "every object" — it defines what the
*protocol-facing* object must satisfy, and is silent on internal representations.

**FACT.** `APS-200:196` §6 — "Every relationship MUST be traceable via `object_id`
references." **OBSERVATION:** `AuditEntry` emits no `object_id` and references no other
entity's `object_id`; the ENT-002→003→005→006→007 chain (`:181-193`) is unrepresented.

**FACT — open TODOs inside ENT-007's own contract:** `APS-200:218` "**TODO**: Define
the canonical serialization format for interoperability between RI-PY and RI-RS";
`:224` "**TODO**: Publish JSON Schema definitions for each entity". `integrity_hash`
(`:58`) is defined *in terms of* "the canonical serialization", which `:218` records
as undefined.

---

## 4. APS-100 trace (Phase 3)

`aps/APS-100_PROTOCOL_INVARIANTS.md`, Version `1.0-DRAFT`, Status **DRAFT**,
Authority `APS-001` (`:3-7`).

| Question | Finding | Evidence |
|---|---|---|
| Defines inheritance from APS-200? | **NO.** APS-100 never references APS-200. Direction is the reverse: APS-200's Authority line names APS-100 (`APS-200:7`). | grep `APS-200` in `APS-100` → 0 hits |
| Constrains object identity? | **YES.** INV-015 Canonical Identity: "Every protocol artifact MUST have a unique identifier conformant with APS-000." | `APS-100:101` |
| Constrains field semantics? | **Indirectly.** INV-003 Canonical Serialization: "Every protocol object MUST have an unambiguous serialization representation." INV-001/002 determinism and bit-perfect replay. | `APS-100:64`, `:61`, `:58` |
| Defines compatibility rules? | **YES, at document level.** INV-009 Version Consistency: "Evidence, Protocol, and Data Model MUST reference compatible document versions." INV-014 Reference Compatibility: "An implementation MUST pass all applicable Reference Fixtures." | `APS-100:83`, `:98` |
| Defines adapter/extension semantics? | **NO.** §7 "Extension Rules" (`:148-156`) governs the addition and removal of **Invariants** only. No object-level adapter or extension semantics anywhere. | `APS-100:148-156` |
| Imposes additional requirements on ENT-007? | **YES — INV-012, and this is where the conflict lies.** | `APS-100:92` vs `invariants/INVARIANT_REGISTRY.md:273` |

### 4.1 CONFLICT-DQ001-01 — INV-012 scope divergence

| Field | Content |
|---|---|
| **Source A** | `aura-specification/aps/APS-100_PROTOCOL_INVARIANTS.md:92` |
| **Claim A** | "Every protocol-governed execution MUST leave an **audit trail** conformant with APS requirements." |
| **Status A** | APS-100 v1.0-DRAFT. **Named in the FROZEN Constitution's canonical hierarchy** (`constitution/AURA_CONSTITUTION.md:80`, Article V, level 3). |
| **Source B** | `aura-specification/invariants/INVARIANT_REGISTRY.md:273` |
| **Claim B** | "Every protocol-governed execution MUST leave an **Audit Record (ENT-007)** conformant with APS requirements." |
| **Status B** | INV-REG-001 v1.0-DRAFT (`releases/v0.1.0/DOCUMENT_STATUS.md`). **Not named in Article V.** |
| **Apparent precedence** | Article V ranks APS-100 above unlisted documents ⇒ A. **But** `APS-100:33` itself delegates: "Full definitions: `../invariants/INVARIANT_REGISTRY.md`" ⇒ B is the designated full definition. The delegation and the hierarchy point opposite ways. |
| **Third source** | `compliance/TRACEABILITY_MATRIX.md:29` binds `INV-012 → ENT-007`, but its own verification columns read `NOT VERIFIED \| NOT VERIFIED`, and its CONF and fixture columns read `TODO`. |
| **Why material to DQ-001** | Under A, an audit trail conformant with APS requirements satisfies INV-012 **without being an ENT-007 object** → supports B/C. Under B, the audit trail **must be** an ENT-007 Audit Record → pressures toward A/B. The two readings do not select the same option set. |
| **Resolution mechanism in the corpus** | None that adjudicates a parent-document/registry delegation inversion. |
| **Status** | **UNRECONCILED. Escalated to the Protocol Custodian.** |

**OBSERVATION.** CONFLICT-DQ001-01 discriminates between {A, B} and {B, C}. **Option B
is in the intersection and is the only option consistent with both readings.** The
conflict therefore constrains, but does not invalidate, the §13 recommendation.

### 4.2 Pre-existing registered conflicts (not reopened)

`review/2026-08-12_OQ-A_GOVERNANCE_JURISDICTION/10_CONFLICT_REGISTER.md`
OQ-A-CONFLICT-001 (Decree vs Specification precedence) and OQ-A-CONFLICT-002 (two
hierarchies inside the spec corpus — **Article V does not name APS-200; only the
un-versioned `README.md:63-83` places it**). Both remain UNRESOLVED and are carried
forward as inherited jurisdictional uncertainty over any APS-200-based decision.

---

## 5. SPEC-002 trace (Phase 4)

`specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md`, Version `0.3-DRAFT`,
Status **DRAFT**, Owner Protocol Custodian, Authority includes APS-200 (`:3-9`).

**FACT.** `SPEC-002:12` — "**Normative effect: NONE until APPROVED.** No requirement in
this document, including any REQ-002-* identifier, constitutes an approved
architectural or implementation decision while this document remains in DRAFT status."

**FACT — targeted search results (all 631 lines):**

| Search term | Hits |
|---|---|
| `AuditEntry` | **0** |
| `Audit Record` | **0** |
| `ENT-007` | **0** |
| `Common Object Contract` | **0** |
| `adapter` | **0** |
| `schema compatibility` | 0 |
| `interoperability` | 0 |

**FACT.** SPEC-002's subject is the **Constitution Artifact / Constitution Vector**, not
the audit object. Its APS-200 citations concern canonicalization and hash domains only:
`REQ-002-007` (`:402`), `REQ-002-011` (`:406`), `REQ-002-017/018/019` (`:412-414`),
`REQ-002-021` (`:416`), `REQ-002-022` (`:417`).

**OBSERVATION.** SPEC-002 contributes **no requirement bearing on DQ-001**. Its only
relevance is negative-and-scoping: `REQ-002-021` (one canonical serialization format,
including field set, field order, encoding, and representation of absent/optional
fields) and `REQ-002-017/018/019` (hash-domain definition and field
inclusion/exclusion) are the *same class of undecided question* that `APS-200:58`
`integrity_hash` depends on. Those are **DQ-002/DQ-003 territory and are left OPEN**.

---

## 6. Source history (Phase 5)

| # | SHA | Date | Author | Repo / file | Fact | Interpretation |
|---|---|---|---|---|---|---|
| H-1 | `d03eb65` | 2026-05-13 | `aura.idtokenkontakt` | `aura-guard-v1.3` `src/models.rs` (added) | First appearance of `AuditEntry` (11 fields: no `request_id`; `prev_hash`/`chain_hash` present). Part of the monolithic "Aura-Guard v1.3.1" import. | Introduced as an internal DTO for the HTTP+JSONL contract. |
| H-2 | `36fd12f` | 2026-05-13 | `Aura-IDToken` | `aura-guard-v1.3` initial commit | `README.md` only, 2 lines. | Repository predates the spec corpus. |
| H-3 | `d2b12cd` / `b68181e` | **2026-07-23** | `Aura-IDToken` / `copilot-swe-agent[bot]` | `aura-specification` initial commit; `aps/APS-200_CANONICAL_DATA_MODEL.md` (added) | The spec repository — and ENT-007 — **first exist on 2026-07-23**. | **`AuditEntry` predates ENT-007 by ~71 days.** |
| H-4 | `025f092` | 2026-07-26 | — | `aura-guard-v1.3` `src/chain.rs` | `policy_hash` present in the chain preimage. | Chain preimage evolved on internal grounds. |
| H-5 | `75f1052` | 2026-07-26 | `Copilot` | `aura-guard-v1.3` `src/models.rs` | `request_id` **added** — "Log analysis for observability metrics (#23)". | A field added **after** ENT-007 existed, for observability. It has no ENT-007 counterpart. No APS-200 alignment was attempted at the one moment the schema was extended post-spec. |
| H-6 | `9dd8757` | 2026-07-27 | `Aura-IDToken` | `aura-guard-v1.3` `src/models.rs` | Doc fixes / header guards; `request_id` test constructors fixed. | Last substantive `models.rs` change. No protocol content. |
| H-7 | `56f7b64` → `c5e162e` | 2026-07-27/28 | `Aura-IDToken` | `aura-guard-v1.3` | Revert pair; net-zero on `models.rs`. | No semantic change. |
| H-8 | `6661982`, `70b9881` | 2026-08-15 | `Claude` | `aura-guard-v1.3` | P0-6 **D-3** reconnaissance + chain-preimage instrumentation. Commit body: "`models.rs` is a pure DTO module"; records the `models.rs:95` (7-field) vs `chain.rs` (9-field) preimage divergence, "Recorded, NOT resolved". | Independent confirmation that `models.rs` carries no protocol role. |
| H-9 | `f8ff209` | 2026-08-11 | `Claude` | `aura-poc-a-core-v3.3` `review/2026-08-11_ENGINEERING_BASELINE/03_LANGUAGE_BOUNDARY.md:49` | `EventTrustCertificate` (Py) vs `AuditEntry` (Rs): "**No** — disjoint field sets, disjoint semantics". | The two RIs' audit objects are not merely un-adapted to ENT-007; they are un-adapted to **each other**. |

**FACT — negative history result.** `git log --all -S` over `aura-guard-v1.3`
(105 commits) returns **zero** commits introducing `ENT-007`, `APS-200`, `object_id`,
`protocol_version` or `integrity_hash`. No commit message in any of the three
repositories records an intent to bind `AuditEntry` to ENT-007.

**OBSERVATION (per the "do not infer intent solely from a field's existence"
constraint).** The chronology (H-1/H-3) establishes that `AuditEntry` **could not have
been** a direct implementation of ENT-007 at the time it was written — ENT-007 did not
exist. H-5 establishes that the single post-spec schema extension did not adopt the
Common Object Contract. Neither fact proves a *deliberate* separation (Option C
intent); it proves **absence of any protocol binding**, which is a weaker and different
claim. That distinction is load-bearing in §9 and §12.

---

## 7. Field-level traceability matrix (Phase 6)

Direction 1 — **ENT-007 MUST fields → `AuditEntry`** (10 fields):

| AuditEntry field | APS-200 ENT-007 field | APS-100 | SPEC-002 | Current implementation | Classification | Evidence |
|---|---|---|---|---|---|---|
| `audit_id` | `object_id` | INV-015 (identifier conformant with APS-000) | — | UUIDv4 minted at `api/audit.rs:134`; never used as a cross-entity reference | **DERIVED** | `models.rs:57-58`; `APS-200:53`; `APS-100:101`; `RI-RS_AURA_GUARD.md:62` INV-015 `❌` |
| — | `object_type` | — | — | Absent. `schema="aura-guard.audit.v1"` is a vendor tag, not the enum literal `"AuditRecord"` | **MISSING** | `APS-200:54`; `fixtures/schemas/common-object-contract.schema.json` enum; `api/audit.rs:132` |
| — | `protocol_version` | INV-009 | — | Absent. Zero `APS` strings in `src/` | **MISSING** | `APS-200:55`; `APS-100:83`; grep `src/` → 0 |
| `schema` | `schema_version` | INV-009 | — | One opaque string conflating vendor + object + version | **DERIVED** | `models.rs:51-52`; `api/audit.rs:132`; `APS-200:56` |
| `timestamp` | `created_at` | — | — | RFC 3339 UTC of **decision production**, not object creation | **DERIVED** | `models.rs:68-69`; `api/audit.rs:117`; `APS-200:57` |
| `chain_hash` | `integrity_hash` | INV-003, INV-011 | REQ-002-017/018/019, REQ-002-021/022 (*undecided*) | SHA-256 over **9 of 14** fields, `"\|"`-joined — **not** the canonical serialization of the object | **CONFLICT** | `chain.rs:36-48` vs `APS-200:58`; `chain.rs:11-12` doc claim vs `chain.rs:36-47` code (`ADR_P0_6…` §2.2, CONFIRMED) |
| — | `event_type` | — | — | Absent. `decision` is an outcome, not an event type; every entry is the same implicit event | **MISSING** | `APS-200:156`; `models.rs:71-72` |
| `seq` | `sequence_number` | INV-012 | — | `u64`, 0-based, monotonic per log file (`api/audit.rs:116`) | **MATCH** | `models.rs:54-55`; `APS-200:157` |
| `prev_hash` | `previous_record_hash` | INV-011 | — | Hex SHA-256 of the previous entry's `chain_hash`; genesis `SHA-256("AURA-GUARD-GENESIS-v1.3")` | **MATCH** | `models.rs:92-93`; `APS-200:158`; `docs/adrs/0001-hash-chain.md` |
| `input_hash` | `event_payload_hash` | — | — | SHA-256 of `context + prompt + response`. **Two** payload hashes exist (`input_hash`, `shadow_hash`) where ENT-007 defines one. Name collision: `input_hash` is also an ENT-**002** MUST field (`APS-200:88`), a different entity | **DERIVED** | `models.rs:83-84,86-87`; `api/audit.rs:104-110`; `APS-200:159`, `:88` |

Direction 2 — **`AuditEntry` fields with no ENT-007 counterpart** (7 fields):

| AuditEntry field | APS-200 ENT-007 field | APS-100 | SPEC-002 | Current implementation | Classification | Evidence |
|---|---|---|---|---|---|---|
| `decision` | none *(cf. ENT-003 `decision`, `APS-200:104` — a different entity)* | INV-013 | — | `DENY`/`REVIEW`/`ALLOW`; hashed | **EXTRA** | `models.rs:71-72`; `APS-200:104` |
| `policy_set` | none *(cf. ENT-004, `APS-200:112-121`)* | INV-013 | — | Policy pack name; hashed | **EXTRA** | `models.rs:74-75`; `APS-200:119` |
| `policy_hash` | none *(cf. ENT-004 `policy_hash`, `APS-200:121`)* | INV-013 | — | SHA-256 of policy file; hashed | **EXTRA** | `models.rs:77-78`; `APS-200:121` |
| `context` | none | — | — | Caller string, verbatim; hashed | **EXTRA** | `models.rs:80-81` |
| `shadow_hash` | none | — | — | SHADOW_SPEC-normalized surface; guard-specific; hashed | **EXTRA** | `models.rs:86-87`; `api/audit.rs:108,110` |
| `violations` | none | INV-012 (contested — §4.1) | — | `Vec<Violation>`; contains `f32`; **not hashed** | **EXTRA** | `models.rs:89-90`, `:38`; `chain.rs:36-47`; `ADR_P0_6…` §2.2 |
| `request_id` | none | — | — | Optional correlation id; omitted when `None`; not hashed | **EXTRA** | `models.rs:60-66`; `api/audit.rs:135` |

### 7.1 Tally

| Classification | Count | Fields |
|---|---|---|
| **MATCH** | 2 | `seq`→`sequence_number`, `prev_hash`→`previous_record_hash` |
| **DERIVED** | 4 | `audit_id`→`object_id`, `schema`→`schema_version`, `timestamp`→`created_at`, `input_hash`→`event_payload_hash` |
| **MISSING** | 3 | `object_type`, `protocol_version`, `event_type` |
| **CONFLICT** | 1 | `chain_hash`↔`integrity_hash` |
| **EXTRA** | 7 | `decision`, `policy_set`, `policy_hash`, `context`, `shadow_hash`, `violations`, `request_id` |
| **UNRESOLVED** | 0 field mappings; **2 contract-level questions** — see §7.2 |

**Zero fields MATCH by name.** The two MATCH classifications rest on concept and
representation, per the stated prohibition on name-similarity matching.

### 7.2 UNRESOLVED at contract level (not field level)

| ID | Question | Why unresolved | Evidence |
|---|---|---|---|
| **U-1** | Are ENT-007 field **names** normative across a mapping boundary? | `APS-200:16` permits differing internal structures and `:213` differing formats; neither states whether names survive. No clause resolves it. | `APS-200:16`, `:53-58`, `:213` |
| **U-2** | Does `sequence_number`'s "**within a session**" scope match `seq`'s per-log-file scope? | The word "session" occurs **exactly once** in the entire spec corpus — in `APS-200:157` itself — and is **never defined** (not in APS-000 terminology, not in `glossary/GLOSSARY.md`). | grep `session` across `aps/`, `glossary/`, `invariants/` → 1 hit |

U-2 qualifies the `seq`→`sequence_number` MATCH: the concept and representation match;
the *scoping* term on the normative side is undefined. This is a defect in ENT-007, not
a mismatch in `AuditEntry`.

---

## 8. Evidence classification

| Rank | Source | Located? | Status | Weight for DQ-001 |
|---|---|---|---|---|
| 1 | Constitutional Decree / AURA Constitution v1.0 | Yes | **FROZEN** | **Indirect.** Article V (`:73-91`) does not name APS-200 → OQ-A-CONFLICT-002 |
| 2 | APS-200 normative text | **Yes** | **DRAFT** — "may change freely" (`VERSIONING.md:38`) | **Decisive but provisional.** `:16` is the single most on-point sentence |
| 3 | APS-100 normative text | **Yes** | **DRAFT** | **Material.** INV-012 / INV-003 / INV-015 / INV-009; source of CONFLICT-DQ001-01 |
| 4 | SPEC-002 | **Yes** | **DRAFT, "Normative effect: NONE"** (`:12`) | **NIL on DQ-001** — 0 hits on every DQ-001 term |
| 5 | Explicit ADRs | Partially | `aura-specification/adrs/ADR-001_DOCUMENT_MODEL.md` **PROPOSED**; `aura-guard-v1.3/docs/adrs/0001-hash-chain.md` **Accepted** (scope: hash chain, not object model) | **No ADR decides DQ-001 in any repository** |
| 6 | Repository / commit history | **Yes**, complete (105 + 226 + full spec history) | — | **Strong negative evidence** (§6): no binding was ever attempted |
| 7 | Current implementation | **Yes** @ `443f72e` | — | Shows an unconnected domain object; **not normative** (`SPEC-002:37`: "Implementation behaviour does not constitute normative evidence") |
| 8 | Documentation / comments | Yes | — | `chain.rs:11-12` **known-inaccurate**; `models.rs:95` doc-comment **known-stale** — both already registered, both **excluded** from load-bearing use here |
| 9 | Spec-corpus RI status docs | **Yes** | DRAFT | `RI-RS_AURA_GUARD.md:22,50,62,74` — the spec corpus' own assessment that no APS-200 objects exist |

**Evidence-strength caveat (applies to the whole review).** Every APS document bearing
on DQ-001 is `1.0-DRAFT`. `VERSIONING.md:36-38` defines DRAFT as "Under active
authoring; **may change freely** — Mutable: Yes". The lifecycle is
`DRAFT → REVIEW → APPROVED → FROZEN` (`:32`); APS-200 has not entered REVIEW. Any
DQ-001 decision taken now is taken against a mutable normative base.

---

## 9. Architectural options (Phase 7)

### 9.1 OPTION A — DIRECT MODEL (`AuditEntry` ≡ ENT-007)

**1. Description.** `AuditEntry` is redefined to *be* the ENT-007 object: it carries all
six Common Object Contract fields plus the four ENT-007 fields, using the normative
names, and the HTTP/JSONL wire form is the protocol object.

**2. Evidence for.** `APS-200:49` "Every entity MUST contain the following fields" is
unconditional. `APS-200:203-207` §7 validation applies to "every object". Under
CONFLICT-DQ001-01 **Source B** (`INVARIANT_REGISTRY.md:273`), execution must leave an
"Audit Record (ENT-007)" — read strictly, that is the object itself. `APS-950:23`
requires an RI to "Implement all mandatory APS requirements". Simplest possible
traceability: no mapping to audit.

**3. Evidence against.** `APS-200:16` explicitly says internal structures **MAY**
differ — a direct model is permitted but **nowhere required**. Under CONFLICT-DQ001-01
**Source A** (`APS-100:92`), only an "audit trail" is required. `AuditEntry` is
simultaneously the public HTTP response body (`api/audit.rs:45`; `openapi.yaml:91`) and
the on-disk log format (`models.rs:44-48`) — collapsing three roles into one. 7 of its
14 fields (§7) have no ENT-007 counterpart, and ENT-007 defines no extension mechanism
(§3.3 Q8) to legitimize them. `integrity_hash` is defined in terms of a canonical
serialization that `APS-200:218` records as **TODO**.

**4. Consequences.** Every one of the 14 existing fields must be renamed, retyped,
re-scoped or justified as an extension. The `f32` in `Violation` (`models.rs:38`)
enters the protocol object and collides with INV-007/INV-001. The undefined
"session" scope (U-2) must be decided before `sequence_number` can be emitted.

**5. Compatibility impact.** **Breaking.** The HTTP response body and the JSONL format
change simultaneously. Every existing log line becomes non-conformant. `aura-replay`
and `aura-seal` must handle two eras.

**6. Migration impact.** **Highest.** Requires a format version discriminator (P0-6
**D-7**, prepared but semantic value **NOT ESTABLISHED**), a dual-read path, and a
decision on historical entries — all before a single conformant record can be written.

**7. Testing impact.** Every fixture, golden test (`tests/golden.rs`), integration test
and property test that names an `AuditEntry` field must change. `tests/d3_chain_observability.rs`
pins a digest that would move.

**8. Serialization impact.** Forces the canonical-serialization decision immediately —
`integrity_hash` (`APS-200:58`) cannot be computed without it. **This pulls DQ-003 (and
DQ-002 via hash domain) into DQ-001, which the task explicitly forbids.**

**9. Hash/evidence impact.** `chain_hash` and `integrity_hash` must be reconciled: one
covers 9 selected fields, the other the whole canonical serialization. Merkle leaves
(`segment.rs:141`) are derived from `chain_hash`; any change re-roots every segment and
invalidates existing RFC 3161 tokens.

**10. API impact.** Breaking change to the sole public endpoint's response schema.

**11. Future extensibility.** **Poor.** ENT-007 defines no extension mechanism; each
future guard-specific field becomes an unauthorized addition to a protocol object.

**12. Reversibility.** **VERY LOW.** Once conformant records are emitted, signed and
timestamped, the object model is embedded in immutable evidence.

**13. Risk.** **HIGH.** Commits the deepest change against a `1.0-DRAFT`, freely-mutable
specification with two open TODOs inside the very contract being adopted.

---

### 9.2 OPTION B — ADAPTER (`AuditEntry` → explicit adapter → ENT-007)

**1. Description.** `AuditEntry` remains the guard's internal DTO, unchanged in shape.
A single, explicitly-named, testable adapter component maps it to an ENT-007 object
carrying the Common Object Contract. The ENT-007 object is what crosses the protocol
boundary (evidence export, conformance runs, cross-RI interop). Two layers, one
mapping.

**2. Evidence for.**
- `APS-200:16` — "Internal structures MAY differ, but data semantics and contract MUST
  be equivalent." A structure that may differ but must be semantically equivalent is
  reached by exactly one mechanism: a mapping. **This is the single most on-point
  normative sentence located, and it describes Option B.**
- `APS-200:213-216` §8 — implementations MAY use different formats provided full model
  semantics are preserved. Same permission at the serialization layer.
- **CONFLICT-DQ001-01 neutrality:** B satisfies Source A (an audit trail exists, and it
  is conformant *via* the mapping) and Source B (an ENT-007 Audit Record is produced).
  It is the only option in the intersection (§4.1).
- §7 tally: 2 MATCH + 4 DERIVED = 6 of 10 ENT-007 fields are already recoverable from
  existing values; only 3 are MISSING and 1 is in CONFLICT. A mapping is small and
  mostly mechanical.
- The 7 EXTRA fields (`shadow_hash`, `violations`, `context`, …) are load-bearing guard
  semantics with no ENT-007 home; keeping them out of the protocol object avoids
  needing an extension mechanism ENT-007 does not define (§3.3 Q8).
- Chronology (§6 H-1/H-3): `AuditEntry` was authored 71 days before ENT-007 existed. A
  post-hoc mapping is the historically honest reconstruction; a claim of prior
  conformance is not available.
- `RI-RS_AURA_GUARD.md:22,74` describes the gap as missing "APS-200 canonical object
  **headers**" / "canonical APS-200 data model **objects**" — i.e. an absent
  protocol-facing object, not a defective internal one.

**3. Evidence against.**
- The word `adapter` occurs **zero times** in the entire spec corpus. No normative
  source names, defines, authorizes or constrains an adapter. B is *permitted by*
  `APS-200:16` but not *prescribed by* anything.
- The adapter cannot be fully specified today: its `integrity_hash` output requires the
  canonical serialization that `APS-200:218` marks **TODO** (DQ-003) and a hash domain
  (DQ-002).
- `APS-200:196` requires relationships traceable via `object_id`; the adapter must mint
  `object_id`s and, for the ENT-002→…→ENT-007 chain (`:181-193`), reference objects the
  guard does not currently produce.
- Two representations of one truth is a standing drift risk absent a conformance test —
  and `APS-200:238` records **no CONF test for ENT-007**.

**4. Consequences.** `models.rs`, `chain.rs`, `log_writer.rs`, `api/audit.rs` and the
existing wire format are untouched. A new, separately-testable module owns the mapping.
The 3 MISSING fields become adapter-supplied constants/derivations
(`object_type = "AuditRecord"`, `protocol_version` = declared APS version,
`event_type` = a canonical value to be decided). The CONFLICT field is quarantined:
`chain_hash` stays the chain link, `integrity_hash` becomes a distinct adapter output
whose definition waits on DQ-002/DQ-003.

**5. Compatibility impact.** **None on existing consumers.** The HTTP contract, the
JSONL format and every historical log line remain valid and verifiable.

**6. Migration impact.** **Low and additive.** No format version bump, no dual-read
path, no historical rewrite. Historical entries can be adapted retroactively because
the mapping reads the record rather than replacing it.

**7. Testing impact.** **Additive.** New mapping tests + a round-trip/equivalence
property. Existing fixtures, `tests/golden.rs` and the pinned digest in
`tests/d3_chain_observability.rs` are unaffected.

**8. Serialization impact.** **Isolated at the boundary.** The canonical-serialization
decision applies only to the adapter's output. **DQ-003 stays open and is not
prejudged** — the adapter is specifiable in shape now and in bytes later.

**9. Hash/evidence impact.** `chain_hash` (`chain.rs:36-48`), Merkle leaves
(`segment.rs:141`), segment manifests and RFC 3161 tokens are all preserved bit-for-bit.
`integrity_hash` is a new, additional digest.

**10. API impact.** **None** to `/v1/audit`. A protocol-facing export surface would be
new and separate.

**11. Future extensibility.** **Good.** Guard-specific fields evolve internally without
touching the protocol object; ENT-007 revisions are absorbed in one module.

**12. Reversibility.** **HIGH** before conformant evidence is published externally;
**MEDIUM** after. See §12.

**13. Risk.** **LOW–MEDIUM.** The main residual risk is semantic drift between the two
representations, mitigable by an equivalence test — which is also what
`APS-200:238`'s missing CONF entry ultimately requires.

---

### 9.3 OPTION C — SEPARATE DOMAIN LAYERS (`AuditEntry` → Aura protocol/domain layer → ENT-007)

**1. Description.** Three layers. `AuditEntry` stays the guard's internal DTO; a
distinct **Aura protocol/domain layer** — its own model, with its own identity,
versioning and semantics, shared across RI-RS and RI-PY — sits between; ENT-007 is
reached from that layer.

**The B/C distinction (required, not collapsed).** B has **two** models and **one**
mapping; the second model *is* ENT-007. C has **three** models and **two** mappings;
the middle model is a **new Aura-owned artifact that no normative source defines**.
B asks "how do we express our record as the protocol's record?" C asks "what is Aura's
own canonical audit domain, independent of both the guard and APS-200?" C is a superset
of B plus an act of specification authorship.

**2. Evidence for.**
- `review/2026-08-11_ENGINEERING_BASELINE/03_LANGUAGE_BOUNDARY.md:49` — the Python
  `EventTrustCertificate` (`audit/merkle.py:37`) and the Rust `AuditEntry` are
  "**No** — disjoint field sets, disjoint semantics", with disjoint Merkle algorithms
  (`:50`), disjoint canonical bytes (`:51`), disjoint signatures (`:52`) and disjoint
  numeric models (`:53`). Two RIs diverging this far is the classic argument for a
  shared intermediate domain.
- `APS-200:218` — the "canonical serialization format **for interoperability between
  RI-PY and RI-RS**" is explicitly an open item; a shared domain layer is one way to
  discharge it.
- `APS-200:16`'s permission for differing internal structures is not limited to one
  level of indirection.

**3. Evidence against.**
- **No normative source defines, names or authorizes an intermediate layer.** APS-200
  §6 (`:181-193`) defines relationships *among ENT entities*; there is no tier between
  an implementation and the canonical model.
- Constructing the middle layer requires deciding its identity model, versioning,
  collection semantics and canonical form — i.e. **deciding DQ-002 (hash domain),
  DQ-003 (canonical serialization), DQ-004 and DQ-007 (versioning) as a precondition**.
  The task forbids exactly this. P0-6 records D-3/D-4 as **"CLOSED — DECISION DOMAIN"**
  with **"concrete semantic value: NOT ESTABLISHED"**
  (`review/2026-08-14_P0_6_D3_D4_DECISION_RECORD/D3_D4_DECISION_RECORD.md` §4), and
  states that no concrete value may be derived from implementation behaviour,
  candidate lists, comments, RI-PY, ADR-0001 or engineering judgement. **C cannot be
  specified without values that governance has explicitly declared unestablished.**
- C adds a second mapping and a second drift surface while `APS-200:238` still records
  **no CONF test for ENT-007**.

**4. Consequences.** A new Aura-owned specification artifact must be authored,
identified, versioned and governed before any code exists. Two adapters to maintain.

**5. Compatibility impact.** None on the guard's existing surfaces (same as B), but the
protocol-facing surface is defined by an artifact that does not yet exist.

**6. Migration impact.** **Highest of the three in elapsed governance time** — low code
churn, but blocked behind authoring and approving a new normative artifact.

**7. Testing impact.** Two mapping suites plus a conformance suite for the new layer.

**8. Serialization impact.** **Forces the canonical-serialization decision at the middle
layer** — i.e. pulls DQ-003 forward. Directly violates the DQ-001 scope boundary.

**9. Hash/evidence impact.** Existing digests preserved, but a third digest domain
(guard chain / domain layer / ENT-007) must be reconciled — expanding DQ-002's surface
before DQ-002 is opened.

**10. API impact.** None immediately.

**11. Future extensibility.** **Best in the limit** — the right shape *if* Aura commits
to a first-class shared audit domain across RI-PY and RI-RS.

**12. Reversibility.** **LOW.** A published intermediate specification is itself a
governed artifact requiring RFC/ADR to change (`VERSIONING.md:40`).

**13. Risk.** **HIGH — primarily governance risk, not technical risk.** C is defensible
architecture, but adopting it now means authoring normative content while the base
(APS-200 `1.0-DRAFT`) is freely mutable and the dependent decisions are formally
unestablished.

---

## 10. Consequences summary

| Dimension | A — Direct | B — Adapter | C — Separate layers |
|---|---|---|---|
| Existing HTTP contract | **Breaks** | Preserved | Preserved |
| Existing JSONL log | **Breaks** | Preserved | Preserved |
| Historical entries | Non-conformant | Adaptable retroactively | Adaptable retroactively |
| `chain_hash` / Merkle / RFC 3161 | **Re-rooted** | Bit-identical | Bit-identical |
| Forces DQ-002/DQ-003 now | **YES** | **NO** | **YES** |
| Requires new normative artifact | No | No | **YES** |
| Consistent with `APS-100:92` (Source A) | Over-satisfies | **Yes** | Yes |
| Consistent with `INV-REG:273` (Source B) | **Yes** | **Yes** | Yes (indirectly) |
| Needs an extension mechanism ENT-007 lacks | **YES** (7 EXTRA fields) | No | No |
| Reversibility | VERY LOW | HIGH → MEDIUM | LOW |

---

## 11. Migration impact

**Option A.** Format-version discriminator (P0-6 D-7 — prepared, semantic value **NOT
ESTABLISHED**); dual-read path in `log_writer.rs`; decision on historical entries;
re-issue of every segment manifest and every RFC 3161 token; coordinated client
release. Blocked behind DQ-002 and DQ-003.

**Option B.** Additive. No discriminator, no dual-read, no re-rooting. New adapter
module + tests + a protocol-facing export surface. The `integrity_hash` field alone is
blocked behind DQ-002/DQ-003; **the mapping's shape is specifiable without them**, so
DQ-001 can close while DQ-002/DQ-003 stay open — which is precisely what the D3-S7
ordering requires.

**Option C.** Option B's work, twice, preceded by authoring and approving a new
normative artifact under `VERSIONING.md:32` (`DRAFT → REVIEW → APPROVED → FROZEN`) and
Constitution Article VII governance.

---

## 12. Reversibility (Phase 10)

**Recommended decision (Option B): reversibility = HIGH.**

**Why HIGH.** B changes nothing that is already immutable. `models.rs`, `chain.rs`, the
9-field preimage, the JSONL format, Merkle roots and TSA tokens are untouched, so no
existing evidence artifact encodes the decision. The adapter is a single leaf module
with one inbound type and one outbound type; deleting it returns the system exactly to
`443f72e` behaviour. B also **defers** rather than consumes the DQ-002/DQ-003/DQ-007
decision space, so it forecloses nothing downstream. If the Architecture Owner later
prefers A, B is a strict waypoint: the mapping already enumerates every field A must
supply. If C is later preferred, the adapter splits in two.

**What degrades it to MEDIUM.** The moment ENT-007 objects produced by the adapter are
**published externally** — exported in an Evidence Pack, attested, timestamped, or
consumed by a third party — the emitted `object_id`s, `event_type` values and
`integrity_hash` construction become referenced facts. Reversal then requires a
compatibility statement, not just a deletion.

### 12.1 Changes that become expensive after choosing B

| Change | Cost after B | Why |
|---|---|---|
| Renaming/retyping `AuditEntry`'s internal fields | **Unchanged (cheap)** | B deliberately leaves them free |
| Reversing to Option A | **Medium** | The mapping is a migration blueprint; but published `object_id`s must be reconciled |
| Moving to Option C | **Medium** | Requires authoring the middle artifact, then splitting the adapter |
| Changing the emitted `object_id` scheme | **Expensive once published** | `APS-200:196` makes `object_id` the cross-entity reference key |
| Changing the `event_type` vocabulary | **Expensive once published** | Becomes a de-facto canonical vocabulary the spec never defined |
| Deciding `integrity_hash`'s canonical serialization (DQ-003) | **Unchanged (still open)** | B is explicitly designed not to prejudge it |
| Binding `violations` into the integrity domain (P0-6 D-1/D-2) | **Unchanged** | B does not touch `chain.rs` |

**OBSERVATION.** The expensive-after items are precisely the three MISSING fields
(§7). If the Architecture Owner approves B, the highest-value follow-on constraint is
to **defer publishing** adapter output externally until `object_id` and `event_type`
schemes are themselves decided.

---

## 13. Agent recommendation (Phase 8)

> ## AGENT RECOMMENDATION — REQUIRES ARCHITECTURE OWNER APPROVAL
>
> ### **OPTION B — EXPLICIT ADAPTER**
>
> **Conditional on Protocol Custodian resolution of CONFLICT-DQ001-01 (§4.1).**
>
> This is an advisory opinion of the analysis agent. It is **not** a decision, **not**
> approved, and **does not** close DQ-001.

**Why B is better supported by the evidence.**

1. **It is what the highest-ranked on-point normative text describes.** `APS-200:16`
   permits internal structures to differ while requiring semantic and contract
   equivalence. That is a mapping boundary stated in normative words. No other option
   is described this directly by any located text.
2. **It is the only option consistent with both sides of the unresolved conflict.**
   CONFLICT-DQ001-01 splits the corpus between "audit trail" (`APS-100:92`) and "Audit
   Record (ENT-007)" (`INV-REG:273`). A satisfies only the strict reading; C satisfies
   it only through an artifact that does not exist. **B satisfies both** — so B is
   selectable *before* the Custodian resolves the conflict, and remains valid *after*
   either resolution.
3. **It is the only option that respects the D3-S7 scope boundary.** A and C both
   require the canonical-serialization and hash-domain decisions (DQ-002/DQ-003) as
   preconditions. B isolates them behind the adapter's output. DQ-001 must close
   **first**; only B allows that without deciding its successors.
4. **The field evidence supports a small mapping, not a rewrite.** 6 of 10 ENT-007
   fields are already MATCH or DERIVED (§7.1); 3 MISSING fields are adapter-supplied
   constants; 1 CONFLICT field is quarantined pending DQ-002/DQ-003.
5. **It preserves every immutable artifact.** Chain hashes, Merkle roots and RFC 3161
   tokens are unchanged (§10). No option that breaks published evidence should be
   preferred while the specification is `1.0-DRAFT` and "may change freely"
   (`VERSIONING.md:38`).
6. **It matches the corpus' own diagnosis.** `RI-RS_AURA_GUARD.md:22,74` describes the
   defect as *missing APS-200 canonical object headers/objects* — an absent
   protocol-facing object, which is what an adapter supplies.

**Why the alternatives are weaker.**

- **A is weaker** because nothing requires it (`APS-200:16` explicitly permits the
  opposite), it needs an extension mechanism ENT-007 does not define (§3.3 Q8) for its
  7 EXTRA fields, it forces DQ-002/DQ-003 in violation of the decision ordering, it
  breaks the public API and the log format simultaneously, and it is VERY LOW
  reversibility against a mutable DRAFT base with two open TODOs (`APS-200:218`, `:225`)
  inside the contract being adopted.
- **C is weaker** *for now* because its middle layer is an artifact **no normative
  source defines**, and specifying it requires concrete D-3/D-4 semantic values that
  governance has formally recorded as **NOT ESTABLISHED**
  (`review/2026-08-14_P0_6_D3_D4_DECISION_RECORD/D3_D4_DECISION_RECORD.md` §4-§5,
  which further states that no such value may be derived from implementation
  behaviour, comments, RI-PY, ADR-0001, or engineering judgement). C is the strongest
  *long-term* candidate if Aura commits to a shared RI-PY/RI-RS audit domain — but that
  commitment is itself an Architecture Owner decision, not a DQ-001 finding. **B is a
  strict prefix of C**: adopting B forecloses nothing about C.

**What evidence remains missing.**

| ID | Missing evidence | Consequence |
|---|---|---|
| **EG-1** | Custodian resolution of CONFLICT-DQ001-01 (§4.1) | Determines whether ENT-007 is *the* required audit object or one conformant form |
| **EG-2** | APS-200 advancement past DRAFT (`VERSIONING.md:32`) | Whole analysis rests on a freely-mutable base |
| **EG-3** | Canonical serialization for ENT-007 (`APS-200:218`, **TODO**) | `integrity_hash` (`:58`) is not computable; the CONFLICT row cannot be closed |
| **EG-4** | Published JSON Schema per entity (`APS-200:224`, **TODO**) | ENT-007 has no machine-checkable contract |
| **EG-5** | Definition of "session" (U-2) | `sequence_number` scope is undetermined |
| **EG-6** | A CONF test for ENT-007 (`APS-200:238` = `—`; `INV-REG:283` "TODO") | No executable conformance evidence is obtainable for any option — including B |
| **EG-7** | Normative `event_type` vocabulary | The adapter must invent a value the spec never defines |
| **EG-8** | Resolution of OQ-A-CONFLICT-001/002 | Whether APS-200 binds `aura-guard-v1.3` at all is jurisdictionally unresolved |
| **EG-9** | Whether ENT-007 field **names** are normative across a mapping (U-1) | Determines whether the adapter must rename or may alias |

**What would falsify this recommendation.**

1. An approved normative statement that ENT-007 field names and structure MUST be
   implemented directly — which would require **superseding `APS-200:16`**. → A.
2. A Custodian ruling that `INVARIANT_REGISTRY.md:273` is authoritative **and** that
   "leave an Audit Record (ENT-007)" means the persisted internal record must itself be
   ENT-007. → A.
3. An Architecture Owner decision to establish a shared RI-PY/RI-RS audit domain as a
   first-class Aura artifact, plus concrete D-3/D-4 semantic values. → C.
4. Discovery of an approved ADR or ARC (in any repository or branch) already deciding
   this. **Searched: not found** — but the search cannot cover unpushed or private work.
5. A ruling that APS-200 does **not** bind `aura-guard-v1.3` (OQ-A-CONFLICT-001/002). →
   DQ-001 becomes moot rather than answered.

---

## 14. Implementation impact (Phase 9)

**Anticipatory only. Nothing below is implemented, authorized, or scheduled.**

### REQUIRED (if the Architecture Owner approves Option B)

| Item | Repository | Nature |
|---|---|---|
| New adapter module (e.g. `src/aps200.rs`) | `aura-guard-v1.3` | New file. One inbound type (`AuditEntry`), one outbound ENT-007 type. |
| ENT-007 target struct + Common Object Contract struct | `aura-guard-v1.3` | New types. **`models.rs` is not modified.** |
| Mapping decisions for the 3 MISSING fields | Governance | `object_type` = `"AuditRecord"` (per schema enum); `protocol_version` = declared APS version; `event_type` = **requires EG-7**. |
| Adapter unit + equivalence tests | `aura-guard-v1.3` `tests/` | New tests only; no existing test modified. |
| ADR recording the decision | `aura-poc-a-core-v3.3` or `aura-specification/adrs/` | §15 candidate, after approval. |
| Traceability entry | `aura-specification/compliance/TRACEABILITY_MATRIX.md:29` | Currently `NOT VERIFIED \| NOT VERIFIED`. **Spec-repo change — Custodian only.** |

### POSSIBLE (needs a separate authorization)

| Item | Gate |
|---|---|
| Protocol-facing export surface (endpoint or CLI emitting ENT-007) | Should wait on EG-3/EG-7 (§12.1) |
| `integrity_hash` computation | **Blocked on DQ-002 + DQ-003** |
| Retroactive adaptation of historical JSONL | After `object_id` scheme is fixed |
| CONF test for ENT-007 | **Blocked on EG-6** — no CONF test exists to extend |
| Mirror adapter for RI-PY `EventTrustCertificate` | Separate decision; RI-PY has the same gap (`RI-PY_AURA_POC_A_CORE.md:27`) |
| `/spec` directory in `aura-guard-v1.3` (`APS-950:51`; `RI-RS_AURA_GUARD.md:35` `❌ MISSING`) | Independent of DQ-001 |

### NOT REQUIRED

| Item | Why |
|---|---|
| `src/models.rs` | B's defining property: the DTO is untouched |
| `src/chain.rs` — preimage, `SEP`, field order | Preserved bit-for-bit |
| `src/log_writer.rs`, JSONL format | Preserved |
| `src/api/audit.rs` response shape, `docs/openapi.yaml` | Preserved |
| `src/segment.rs`, `src/sealer.rs`, `src/merkle.rs`, RFC 3161 tokens | Preserved; no re-rooting |
| Existing fixtures, `tests/golden.rs`, `tests/d3_chain_observability.rs` pinned digest | Unaffected |
| Format version discriminator (P0-6 D-7) | Not needed for an additive mapping |
| Any change to APS-100 / APS-200 / SPEC-002 / existing ADRs | **Forbidden to this agent in all cases** |
| Resolution of DQ-002 / DQ-003 / DQ-004 / DQ-005 / DQ-006 / DQ-007 / DQ-008 | **Explicitly out of scope; left OPEN** |

---

## 15. ADR candidate (Phase 11)

> **This is a candidate. It is NOT an ADR of record. It has NOT been approved, filed,
> numbered, or registered. Status MUST remain PROPOSED / NOT APPROVED.**

---

# ADR Candidate — DQ-001 Adapter Architecture

**Status:** **PROPOSED / NOT APPROVED**
**Date prepared:** 2026-08-15
**Prepared by:** Claude (forensic architecture analysis agent) — not the Architecture Owner
**Decision Owner:** Architecture Owner
**Conflict resolution required from:** Protocol Custodian (CONFLICT-DQ001-01)

## Context

`AuditEntry` (`aura-guard-v1.3` @ `443f72e`, `src/models.rs:50-97`) is simultaneously
the `/v1/audit` HTTP response body (`src/api/audit.rs:45`; `docs/openapi.yaml:91`) and
the on-disk JSONL audit record (`src/models.rs:44-48`). APS-200 (`1.0-DRAFT`) defines
ENT-007 Audit Record (`aps/APS-200_CANONICAL_DATA_MODEL.md:149-159`) and a Common
Object Contract binding on every entity (`:47-58`). No relationship between the two has
ever been declared, documented or implemented.

## Problem

Is `AuditEntry` (A) a direct implementation of ENT-007, (B) an adapter-compatible
representation, or (C) a deliberately separate Aura domain object connected through an
explicit adapter boundary?

## Normative Evidence

- `APS-200:16` — "Every conformant implementation MUST represent information in
  accordance with this document. Internal structures MAY differ, but data semantics and
  contract MUST be equivalent."
- `APS-200:47-58` — Common Object Contract: 6 MUST fields.
- `APS-200:149-159` — ENT-007: Common Object Contract + `event_type`,
  `sequence_number`, `previous_record_hash`, `event_payload_hash`.
- `APS-200:196`, `:203-207`, `:213-216`, `:218` (TODO), `:224` (TODO), `:238` (no CONF test).
- `APS-100:92` INV-012 ("audit trail") vs `invariants/INVARIANT_REGISTRY.md:273`
  ("Audit Record (ENT-007)") — **CONFLICT-DQ001-01, unreconciled**.
- `APS-100:64` INV-003, `:101` INV-015, `:83` INV-009, `:98` INV-014.
- `SPEC-002` — **zero** references to `AuditEntry` / ENT-007 / Common Object Contract /
  adapter; `SPEC-002:12` "Normative effect: NONE until APPROVED".
- Every APS document bearing on this question is `1.0-DRAFT` — "may change freely"
  (`VERSIONING.md:38`).

## Current Implementation

14 fields; 9 hashed into `chain_hash` (`src/chain.rs:36-47`); `violations`, `audit_id`,
`request_id`, `schema` outside the digest. No APS identifier of any kind appears in
`src/`, `tests/` or `docs/`. Zero mapping code. `reference/RI-RS_AURA_GUARD.md:74`
records "No canonical APS-200 data model objects" as a Key Gap; `:62` records INV-015
as `❌`. Against ENT-007's 10 MUST fields: **2 MATCH, 4 DERIVED, 3 MISSING, 1 CONFLICT**,
plus **7 EXTRA** fields with no ENT-007 counterpart.

## Options Considered

- **A — Direct model.** `AuditEntry` ≡ ENT-007. Not required by any text; contradicted
  as a mandate by `APS-200:16`; requires an extension mechanism ENT-007 does not define;
  breaks the API and log format; forces DQ-002/DQ-003.
- **B — Explicit adapter.** `AuditEntry` → adapter → ENT-007. Directly described by
  `APS-200:16`; additive; preserves all existing evidence; defers DQ-002/DQ-003.
- **C — Separate domain layers.** `AuditEntry` → Aura domain layer → ENT-007. Strongest
  long-term shape for RI-PY/RI-RS convergence; requires authoring a normative artifact
  that does not exist and concrete D-3/D-4 values formally recorded as **NOT
  ESTABLISHED**.

## Decision Candidate

**Option B — explicit adapter boundary**, conditional on Protocol Custodian resolution
of CONFLICT-DQ001-01. `AuditEntry` remains the guard's internal DTO and is not modified;
a separately-testable adapter maps it to an ENT-007 object at the protocol boundary.

**NOT DECIDED by this candidate:** canonical serialization (DQ-003), hash domain
(DQ-002), violation binding, versioning/discriminator (DQ-007), numeric policy,
`object_id` scheme, `event_type` vocabulary, and whether adapter output may be
published externally.

## Consequences

Existing HTTP contract, JSONL format, `chain_hash` preimage, Merkle roots and RFC 3161
tokens are all preserved bit-for-bit. A new adapter module and its tests are added.
`integrity_hash` cannot be emitted until DQ-002/DQ-003 close. Two representations of one
record introduce a drift surface requiring an equivalence test.

## Migration Impact

Additive. No format version bump, no dual-read path, no re-rooting of segments, no
invalidation of historical entries or timestamp tokens.

## Reversibility

**HIGH** while adapter output remains internal; **MEDIUM** once ENT-007 objects are
published externally, because emitted `object_id` and `event_type` values become
referenced facts (§12).

## Open Questions

EG-1 … EG-9 (§13), U-1 and U-2 (§7.2), and the inherited OQ-A-CONFLICT-001/002.

## Evidence References

All file:line citations in §2–§8 of
`review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/D3-S4_DQ-001_ADAPTER_ARCHITECTURE_REVIEW.md`,
pinned at `aura-specification` `62d2d6b`, `aura-guard-v1.3` `443f72e`,
`aura-poc-a-core-v3.3` `98f2f43`.

## Approval Required

- **Architecture Owner** — selection of A, B or C. Claude has not decided and cannot decide.
- **Protocol Custodian** — resolution of CONFLICT-DQ001-01 before this candidate can advance.
- **Two-Key Gate** — per `review/2026-08-12_RD1_ARI_DECISION_READINESS/08_TWO_KEY_DECISION_PROTOCOL.md`.

**Status:** **PROPOSED / NOT APPROVED**

---

## 16. Open evidence gaps

### 16.1 Hard-stop conditions — assessed

| Condition | Triggered? | Finding |
|---|---|---|
| APS-200 ENT-007 cannot be located | **NO** | Located: `aps/APS-200_CANONICAL_DATA_MODEL.md:149-159` @ `62d2d6b` |
| Common Object Contract cannot be located | **NO** | Located: `:47-58`, plus `fixtures/schemas/common-object-contract.schema.json` |
| **Normative sources conflict materially** | **YES** | **CONFLICT-DQ001-01** (§4.1): `APS-100:92` vs `INVARIANT_REGISTRY.md:273`. **Reported, not reconciled. Escalated to the Protocol Custodian.** Inherited: OQ-A-CONFLICT-001/002. |
| Repository history insufficient | **NO** | Full history read: 105 (guard) + 226 (core) + complete spec history, all branches |
| Field mapping cannot be established without guessing | **NO** | Established in §7 with `MISSING`/`CONFLICT`/`UNRESOLVED` used wherever evidence was absent. No mapping was guessed. |
| Resolving DQ-001 requires deciding DQ-002/DQ-006/DQ-005 | **NO for Option B; YES for A and C** | Recorded as a discriminating criterion (§9, §13). No successor DQ is decided anywhere in this document. |
| Implementation changes needed to obtain evidence | **NO** | Analysis is entirely read-only |

**Consequence.** One hard-stop condition is met. Per `CLAUDE.md` §"Authority Precedence"
the conflict is reported and escalated rather than reconciled. **DQ-001 is NOT closed by
this document**, and the §13 recommendation is explicitly conditional on Custodian
resolution of CONFLICT-DQ001-01.

### 16.2 Gap register

| ID | Gap | Blocks | Owner |
|---|---|---|---|
| EG-1 | CONFLICT-DQ001-01 unresolved | Closing DQ-001 | Protocol Custodian |
| EG-2 | APS-200/APS-100 remain `1.0-DRAFT`, freely mutable | Durability of any DQ-001 decision | Chief Architect |
| EG-3 | Canonical serialization undefined (`APS-200:218` TODO) | `integrity_hash`; the CONFLICT row | DQ-003 |
| EG-4 | No published JSON Schema per entity (`APS-200:224` TODO) | Machine-checkable ENT-007 contract | Protocol Custodian |
| EG-5 | "session" undefined (U-2) | `sequence_number` scope | Protocol Custodian |
| EG-6 | No CONF test for ENT-007 (`APS-200:238`) | Executable conformance evidence for **any** option | DQ-006 / APS-400 |
| EG-7 | No normative `event_type` vocabulary | Adapter output | Architecture Owner |
| EG-8 | OQ-A-CONFLICT-001/002 unresolved | Whether APS-200 binds `aura-guard-v1.3` at all | Protocol Custodian |
| EG-9 | Whether ENT-007 field names are normative across a mapping (U-1) | Adapter naming strategy | Protocol Custodian |
| EG-10 | `DQ-001`/`D3-S7`/`D3-S4` identifiers exist in no repository | Traceability of this decision series | Architecture Owner |
| EG-11 | RI-PY has the identical gap (`RI-PY_AURA_POC_A_CORE.md:27`), unaddressed here | Cross-RI interoperability (`APS-200:218`) | Separate decision |

---

## 17. Declarations

- **No production source code was modified** in any repository.
- **No normative document was modified.** APS-200, APS-100, SPEC-002 and all existing
  ADRs are untouched.
- **No ADR was approved, filed or numbered.** §15 is a candidate at
  `PROPOSED / NOT APPROVED`.
- **No DQ was closed.** DQ-002 … DQ-008 are untouched and remain OPEN.
- **No test, fixture, serialization, hash or API surface was changed.**
- **No PR was merged and no decision was frozen.**
- The `aura-guard-v1.3` and `aura-specification` repositories were **read only**;
  neither was written to.
