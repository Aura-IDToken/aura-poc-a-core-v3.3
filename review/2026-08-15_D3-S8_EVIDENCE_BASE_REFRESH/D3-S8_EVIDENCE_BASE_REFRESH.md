# D3-S8 — AURA EVIDENCE BASE REFRESH

**Pre-decision evidence reconciliation for DQ-001…DQ-008.**
**Role:** evidence auditor / repository historian. **Not** the Architecture Owner.
**Date:** 2026-08-15
**Normative effect: NONE. No architectural decision is made, proposed or implied.**
**Code changed:** NO. **Normative documents changed:** NO. **ADRs created/approved:** NO.

---

## 0. Package contents

| File | Phase | Contents |
|---|---|---|
| `REPOSITORY_IDENTITY_MATRIX.md` | 0 | Verified remotes, HEADs, shallowness, aliases |
| `NORMATIVE_CORPUS_INVENTORY.md` | 1 | Every normative document with version, status, verified from content |
| `HASH_DOMAIN_MATRIX.md` | 3 | 13 implementation domains + 10 normative fields + lineage |
| `CANONICAL_SERIALIZATION_MATRIX.md` | 4 | Four regimes, side by side |
| `SOURCE_HISTORY_TIMELINE.md` | 9–11 | Timeline, `git log -S` results, five lineage categories |
| `PREVIOUS_FINDINGS_REASSESSMENT.md` | 12 | 21 prior claims re-tested |
| `DQ_EVIDENCE_GATE.md` | 13–14 | Per-DQ gate and decision readiness |
| **this file** | 2, 5–8, final | DQ-001/003/004/005/007 evidence + consolidated report |

**Method rule applied throughout:** prior audit artifacts were treated as *evidence of
prior analysis*, never as fact. Every claim was re-tested against source. Where a prior
claim failed re-testing it is marked **UPDATED**, **WEAKENED** or **CONTRADICTED** in
`PREVIOUS_FINDINGS_REASSESSMENT.md`, not silently corrected.

---

## 1. The single most consequential Phase-0 finding

**FACT.** The repository attached to this session under the name `aura-specification` is
`aura-nomos/aura-specification` (verified by `git remote get-url origin`). Its **entire
content**, across all branches and its full 3-commit history, is `README.md` (one line)
and `.github/CODEOWNERS`. **It contains no APS document.**

**FACT.** The APS corpus is `AuraIDToken/aura-specification` — a different repository
under a different owner — attached separately and cloned read-only.

**INFERENCE.** Any analysis that accepted the session-attached repository as the
specification source would conclude that APS-200 and ENT-007 do not exist. The D3-S8
instruction to verify repository identity before using any document as evidence changes
the outcome, not merely the paperwork.

---

## 2. DQ-001 evidence refresh (Phase 2)

### 2.1 The three field sets, from source

**Common Object Contract** — `APS-200:47-58`, "Every entity MUST contain":
`object_id`, `object_type`, `protocol_version`, `schema_version`, `created_at`,
`integrity_hash` — **6 MUST fields.**

**ENT-007** — `APS-200:149-159`: Common Object Contract fields (`:155`) **plus**
`event_type`, `sequence_number`, `previous_record_hash`, `event_payload_hash` —
**10 MUST fields total.**

**`AuditEntry`** — `aura-guard-v1.3` `models.rs:50-97`: `schema`, `seq`, `audit_id`,
`request_id`, `timestamp`, `decision`, `policy_set`, `policy_hash`, `context`,
`input_hash`, `shadow_hash`, `violations`, `prev_hash`, `chain_hash` — **14 fields.**

### 2.2 The nine questions

| # | Question | Evidence |
|---|---|---|
| 1 | Exact Common Object Contract fields | 6, listed above — `APS-200:53-58` |
| 2 | Exact ENT-007 fields | 10, listed above — `APS-200:155-159` |
| 3 | Exact `AuditEntry` fields | 14, listed above — `models.rs:52-96` |
| 4 | **Any explicit mapping?** | **NONE FOUND.** No mapping code, table or document in any repository |
| 5 | **Any adapter?** | **NONE FOUND.** `adapter` occurs **0×** in the entire `aura-specification` corpus. In the guard it appears only as *SIEM format adapters* (`ROADMAP.md:62`) and *WORM media adapters* (`:83`). In POC-A only as *embedding→int32* adapters (`GAP-001:364,417,662`) |
| 6 | **Any APS identifier in the implementation?** | **NONE.** `APS-`: 0 files @HEAD and **0 commits across the guard's full 105-commit history** |
| 7 | **Any normative statement binding `AuditEntry` to ENT-007?** | **NONE FOUND.** `AuditEntry` occurs 0× in the corpus |
| 8 | **Any statement allowing internal structures to differ?** | **YES — `APS-200:16`**: "Every conformant implementation MUST represent information in accordance with this document. **Internal structures MAY differ, but data semantics and contract MUST be equivalent.**" |
| 9 | **Any historical evidence of intended mapping?** | **NONE FOUND.** `AuditEntry` 2026-05-13 (`d03eb65`) predates ENT-007 2026-07-23 (`b68181e`) by **71 days**. The single post-spec schema change (`request_id`, `75f1052`) states observability intent and no APS alignment |

### 2.3 Which does the evidence establish — A, B, C or D?

**D — NONE ESTABLISHED.**

**FACT.** There is no direct mapping (no APS field names in the implementation), no
adapter (none exists anywhere), and no shared canonical object (`chain_hash` is absent
from the corpus; `integrity_hash`/`event_payload_hash` are absent from the guard). The
specification's own status documents say so: `RI-RS_AURA_GUARD.md:22` "no APS-200
canonical object headers", `:74` "No canonical APS-200 data model objects", `:7`
"**NOT CERTIFIED**"; `RI-PY_AURA_POC_A_CORE.md:27` "not APS-200 ENT-007".

**FACT.** `APS-200:16` **permits** internal structures to differ under semantic
equivalence. That is a permission, not an establishment of any option.

**No architectural option is chosen here.** Per D3-S8 Phase 2, only evidence is reported.

---

## 3. DQ-003 evidence refresh (Phase 5)

| Concept | Normative definition | Implementation |
|---|---|---|
| `protocol_version` | `APS-200:55` "APS version this object conforms to (e.g., `1.0`)"; `APS-300:61` "APS version"; `APS-500:38,79` "Target APS version" | **0 occurrences, 0 commits** in `aura-guard-v1.3`, full history |
| `schema_version` | `APS-200:56` "**Schema version of this entity definition**"; `APS-300:62` "**APS-300 schema version**" | **0 occurrences, 0 commits** |
| `schema` | **not an APS concept** | `"aura-guard.audit.v1"` — hard-coded at `api/audit.rs:132`, echoed at `api/health.rs:43`. Unchanged since `d03eb65`. A second, separate constant `SEGMENT_SCHEMA = "aura-guard.segment.v1"` exists at `segment.rs:44` |

**FACT.** APS requires **two distinct** version fields on every entity. The implementation
has **one** opaque string that conflates three things: vendor (`aura-guard`), object
(`audit`) and version (`v1`).

**FACT.** `APS-200:56` and `APS-300:62` define `schema_version` **differently**:
"schema version of this entity definition" versus "APS-300 schema version". These are not
obviously the same quantity.

**Can `AuditEntry.schema` be mapped to `ENT-007.schema_version` on evidence alone?**
**NO.** Missing evidence, stated exactly:

1. No normative statement of what `schema_version` versions — the entity definition, the
   document, or the wire format.
2. No statement of whether a composite vendor string may satisfy a version field.
3. No `protocol_version` value exists anywhere in the implementation to map at all.
4. No version-format grammar. `fixtures/core/FIX-001…:8,17,18` carry `"TODO"` for both.

**Status: EVIDENCE PARTIAL.**

---

## 4. DQ-004 evidence refresh (Phase 6)

**FACT — the normative side.** `APS-200:156` requires `event_type` — "Canonical event
type". `APS-200:104` defines ENT-003 `decision` — "Canonical decision value (e.g.,
`ALLOW`, `DENY`, `MEASURE`)" — with `APS-200:108` "**TODO**: Define the canonical set of
`decision` values." `APS-000:46-47` TERM-008 defines an Audit Record as "An immutable
record of a single auditable event."

**FACT — "event", "event payload" and "canonical event type" are nowhere defined** in
APS-200, APS-000 terminology or `glossary/GLOSSARY.md`. Not found in inspected scope.

**FACT — the implementation side.** `decision` is produced at `engine.rs:59-63` as
`DENY` / `REVIEW` / `ALLOW`, selected from two boolean flags. **No `event_type` field
exists in `AuditEntry` or anywhere in the guard.**

**FACT — a vocabulary divergence.** APS-200's example set is `ALLOW`, `DENY`, `MEASURE`;
the guard's set is `ALLOW`, `DENY`, `REVIEW`. `MEASURE` and `REVIEW` do not correspond,
and neither list is normative (`:108` TODO).

**Do the normative sources distinguish "what happened?" from "what was decided?"**
**YES structurally, NO substantively.** ENT-007 carries `event_type` (what happened) while
ENT-003 carries `decision` (what was decided) — two different entities, two different
fields. But since `event_type` has no definition and the `decision` set is a TODO, the
distinction is declared and not populated.

**Status: EVIDENCE MISSING.** This directly blocks DQ-002: `event_payload_hash`
(`APS-200:159`) cannot be given an input while "the event payload" is undefined.

---

## 5. DQ-005 evidence refresh (Phase 7)

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Are `violations` inside `chain_hash`? | **NO** | `chain.rs:36-47` hashes exactly 9 fields; `violations` is not among them |
| 2 | Inside any other integrity hash? | **NO** | Enumeration of all 13 SHA-256 sites — no domain covers it |
| 3 | Inside `event_payload_hash`? | **N/A** — the field is unimplemented and its input undefined | `HASH_DOMAIN_MATRIX.md` §4 |
| 4 | Does APS-200 require them to be cryptographically bound? | **NO — the concept does not exist in APS-200.** ENT-007's four specific fields are `event_type`, `sequence_number`, `previous_record_hash`, `event_payload_hash`. There is no violations/rule-match concept | `APS-200:155-159` |
| 5 | Do APS-300/400/500 clarify? | **NO.** The word "violation" appears in the corpus **only** as *invariant* violation (`APS-100:16,109,144`; `APS-400:156`) — a different concept entirely | corpus grep |
| 6 | Is there a fixture proving intended binding? | **NO.** All fixture values are `"TODO"` | `FIX-001…:8,17,18,19` |

**CURRENT IMPLEMENTATION.** `violations: Vec<Violation>` (`models.rs:90`) carries `rule`,
`action`, `confidence: f32` (`:38`), `validator: Option<String>` with
`skip_serializing_if` (`:40`). It is returned in the HTTP response and written to JSONL,
and is **outside every hash domain**. Four fields total are uncovered: `violations`,
`audit_id`, `request_id`, `schema`.

**NORMATIVE CONTRACT.** **None exists** for this concept.

**INFERENCE.** DQ-005 is not a question of whether the implementation departs from a
normative requirement — there is no requirement to depart from. It is a question of
whether a normative requirement should be created. **Status: EVIDENCE PARTIAL** — the
implementation facts are fully established; the normative side is empty.

**No solution is recommended**, per Phase 7.

---

## 6. DQ-007 evidence refresh (Phase 8)

**FACT — the prohibition.** `APS-100:76-77` INV-007 Zero Float Runtime: "**MUST NOT**:
Protocol logic MUST NOT use floating-point arithmetic during execution **if doing so
would violate determinism as defined by the specification**." The clause is
**conditional**.

**FACT — POC-A.** `docs/ADR_005_NO_FLOAT_RUNTIME.md` — **Status: APPROVED**, dated
2026-01-23, "Aura Protocol Core Team". Rationale: bit-for-bit reproducibility across
x86/ARM/WASM; enumerates five IEEE-754 non-determinism sources (rounding modes, FMA
availability, SIMD, compiler reordering, register precision). Implementation:
`core/evaluator.py:7,12` — "fixed-point int32 arithmetic (scaling factor: 10^5 =
100,000)", `SCALING_FACTOR = 100000`.

**FACT — the guard.** `f32` appears at `models.rs:38` (`Violation.confidence`) and
`policy.rs:41,94` (`score`). **It does not participate in the decision.**
`engine.rs:44-63` selects `DENY`/`REVIEW`/`ALLOW` from two booleans (`has_deny`,
`has_review`); `rule.score` is **copied into the record** at `engine.rs:53` but never
compared or arithmetically combined. `api/audit.rs:191` uses `as_secs_f64()` for a
latency metric — outside the decision path.

**INFERENCE.** The guard satisfies INV-007's conditional prohibition in its decision path:
no float arithmetic occurs during evaluation. `f32` is a **recorded payload value**, not a
computation input. This distinction is load-bearing and was not previously stated.

**FACT — the parameters are unresolved.** `SPEC-002:141` REQ-002-014 requires "one numeric
representation … including domain, width, sign, scale, rounding behavior, overflow
behavior, and byte order where applicable"; `:381` records **AD-CA-007 UNRESOLVED** with
`32`, `100000`, `signed int32`, `little-endian`, `round-half-to-even` explicitly
"**candidate only**"; `:108` states no candidate "constitutes a recommendation,
preference, default, or implied architectural decision."

| Item | Established? |
|---|---|
| Runtime floating-point prohibition | **YES** (conditional) — `APS-100:76-77` + ADR-005 APPROVED |
| Offline floating-point allowance | **PARTIAL** — POC-A has `core/offline_normalizer.py`; no APS statement found |
| Fixed-point scale | **NO** — `100000` is implementation + candidate only |
| Integer width | **NO** — `signed int32` candidate only |
| Rounding | **NO** — `round-half-to-even` candidate only |
| Overflow behaviour | **NO** — `SPEC-002:349` requires "deterministic rejection" in a **future** spec |
| Canonical byte representation | **NO** — `little-endian` candidate only; ⇒ DQ-006 |

**Status: EVIDENCE PARTIAL.** The prohibition is evidenced; **no parameter is.**
**No missing parameter is invented here.**

---

## 7. DQ-008 evidence refresh (Phase 9)

| Divergence | Documented | Actual | First present | Still present? |
|---|---|---|---|---|
| Chain preimage field count | **7** (`models.rs:95`) | **9** (`chain.rs:36-47`) | **`d03eb65`, 2026-05-13 — the first commit** | **YES** at `443f72e` |
| Chain preimage in `chain.rs` doc | 9 (`chain.rs:6-8`) | 9 | `d03eb65` | consistent |
| "Tampering with any field … breaks the chain" | `chain.rs:11-12` | 4 of 14 fields are outside the digest | `d03eb65` | **YES** |
| "Field separator is `\|` so the input is unambiguous" | `chain.rs:11` | `context` is free-form and unescaped; `chain.rs:18-19` scopes the claim to hex/base64/timestamp characters only | `d03eb65` | **YES** |
| GAP-001 APS numbering | APS-200 = "ARI Engine" | APS-200 = Canonical Data Model | `ef91cb1`, 2026-07-24 | **YES** |
| POC-A JSON separators | — | compact at `merkle.py:85`; Python defaults at `core/merkle.py:8`, `certificate.py:69` | — | **YES** |

**FACT — ordering.** Implementation (2026-05-13) **predates** the normative specification
(2026-07-23) by 71 days. Documentation did not "drift" from a correct state: the
`models.rs` 7-field comment was **wrong in the commit that introduced it**.

**FACT.** No commit message, ADR or issue explains the 7-vs-9 divergence.
**INTENT NOT ESTABLISHED.**

**Status: CONFLICT** — including **CONFLICT-DQ008-01**, the contradictory statements of
DQ-001's own status (`PREVIOUS_FINDINGS_REASSESSMENT.md` §3).

---

# FINAL REPORT

## 1. WHAT WE KNOW NOW

- Three primary repositories, all with **complete** histories, all verified by remote URL.
  The session-attached `aura-specification` is **not** the specification repository.
- The corpus has **one FROZEN document** (the Constitution). Everything else — every APS,
  the invariant registry, SPEC-002, all ten CONF tests — is **DRAFT**, defined by
  `VERSIONING.md:38` as "may change freely".
- The implementation runs **13** distinct SHA-256 constructions. The corpus names **10**
  hash fields. **Zero** correspondences are both specified and implemented.
- `chain_hash` is byte-stable since 2026-05-13 and appears **0×** in the corpus.
  `integrity_hash` and `event_payload_hash` appear **0×** in the implementation.
- **Four** canonical-serialization regimes coexist. One 315-byte stream exists and its
  digest was re-verified independently.
- `violations`, `event_type`, `schema_version`, `protocol_version` and the numeric
  parameters have **no established normative content**.
- **Five active conflicts**, plus two inherited.

## 2. WHAT CHANGED FROM PREVIOUS DQ ANALYSIS

1. **Hash-construction count 9 → 13.** The prior inventory omitted `segment_genesis_hash`
   (`segment.rs:47-50`), the RFC 3161 request digest (`rfc3161.rs:138`) and two TST
   verification digests (`tst_verify.rs:657,839`).
2. **Domain separation ABSENT → PARTIAL.** The entry chain and segment chain are seeded
   from **two distinct genesis constants** (`crypto.rs:28` vs `segment.rs:48`). The prior
   flat "ABSENT" was an overstatement.
3. **DQ-001's premise is contradicted.** Recorded as CONFLICT-DQ008-01.
4. **Three citation line numbers corrected**; one inherited citation
   (`audit/merkle.py:37`) found wrong — the class is at `:20`.
5. **New:** `f32` in the guard does **not** participate in the decision path — a
   materially different INV-007 posture than "the guard uses floats".

## 3. WHAT WAS CONFIRMED

Twelve of twenty-one prior claims re-tested and confirmed, including: the field sets;
`chain_hash` absent from the corpus; the normative names absent from the guard;
CONFLICT-DQ002-01; the 7-vs-9 documentation divergence dating to the first commit; the
315-byte stream and digest; the intra-implementation-only conformance tests; the APS-950
RI designation being source-authored. **Strengthened:** APS-200 contains **zero**
relational verbs anywhere in the document, and APS-400 + all CONF files contain **zero**
cross-implementation language.

## 4. WHAT WAS INVALIDATED OR WEAKENED

- Prior hash-domain count (**UPDATED**).
- Prior "ABSENT" domain-separation classification (**WEAKENED** to PARTIAL).
- The DQ-006 artifact's DQ-001 premise (**CONTRADICTED**).
- One inherited citation (**CONTRADICTED**).

Both substantive errors ran the same direction: they **understated** the guard's existing
cryptographic structure.

## 5. WHAT REMAINS UNKNOWN

"Event payload"; "canonical event type"; the canonical `decision` set; whether
`integrity_hash` includes itself; what `schema_version` versions; the canonical
serialization; every numeric parameter; whether rule-match records are in APS scope at
all; the intent behind the 7-vs-9 divergence; whether `EVIDENCE_SPEC v1.1` (guard
`ROADMAP.md:80`) relates to APS-300.

## 6. ACTIVE CONFLICTS

CONFLICT-DQ001-01 · CONFLICT-DQ002-01 · CONFLICT-DQ006-01 · CONFLICT-DQ006-02 ·
CONFLICT-DQ008-01 · (inherited) OQ-A-CONFLICT-001/002 · (inherited) GAP-001 numbering.

## 7–14. DQ STATUS

| DQ | Status |
|---|---|
| **DQ-001** | **CONFLICT** |
| **DQ-002** | **CONFLICT** |
| **DQ-003** | **EVIDENCE PARTIAL** |
| **DQ-004** | **EVIDENCE MISSING** |
| **DQ-005** | **EVIDENCE PARTIAL** |
| **DQ-006** | **CONFLICT** |
| **DQ-007** | **EVIDENCE PARTIAL** |
| **DQ-008** | **CONFLICT** |

## 15. WHICH DQs ARE SAFE TO DECIDE

**None outright.** Narrowly decidable: **DQ-007's float prohibition only** (INV-007 plus
ADR-005, the only APPROVED decision artifact found in any repository) and **DQ-008 as a
recording action only** (the divergences are established; the remedy is blocked by
CONFLICT-DQ006-02).

## 16. WHICH DQs MUST REMAIN OPEN

**DQ-001, DQ-002, DQ-003, DQ-004, DQ-005, DQ-006** — and DQ-007's parameters and DQ-008's
remedy.

## 17. MINIMUM EVIDENCE REQUIRED BEFORE THE NEXT DECISION

1. **Protocol Custodian ruling on CONFLICT-DQ002-01** — does `integrity_hash` include
   itself, and are `integrity_hash` and `evidence_hash` one concept or two? *(unblocks
   DQ-002)*
2. **Architecture Owner statement of DQ-001's actual status** — CONFLICT-DQ008-01 must be
   resolved before any artifact can state a premise. *(unblocks DQ-001, DQ-002, DQ-006)*
3. **Custodian ruling on CONFLICT-DQ006-02** — does documentation or implementation
   govern? *(unblocks DQ-006)*
4. **A definition of "event", "event payload" and "canonical event type"** *(unblocks
   DQ-004, then `event_payload_hash` in DQ-002)*
5. **Custodian ruling on CONFLICT-DQ001-01** — INV-012's scope *(unblocks DQ-001)*
6. **A statement on whether rule-match records are in APS scope** *(unblocks DQ-005)*
7. **A cross-implementation conformance procedure** — closing CONFLICT-DQ006-01 *(unblocks
   verification of anything decided)*

Items 1–3 are the critical path: they gate five of the eight DQs.

---

## Declarations

No production source, test, fixture, APS document, SPEC-002, `AUDIT_LAYER_SPEC.md` or
existing ADR was modified. `aura-guard-v1.3` and `aura-specification` were read only.
No architecture, canonical byte format or hash formula was decided or proposed. No prior
artifact was edited to conceal the premise change. No missing evidence was substituted
with best practice. No DQ was closed.

**EVIDENCE BASE REFRESH COMPLETE — NO ARCHITECTURAL DECISION MADE**
