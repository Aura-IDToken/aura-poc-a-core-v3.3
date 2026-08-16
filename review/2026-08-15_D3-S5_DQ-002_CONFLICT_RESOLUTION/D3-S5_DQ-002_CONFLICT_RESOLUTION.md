# DQ-002 — Conflict Resolution Record

**Document class:** conflict record prepared for Protocol Custodian ruling.
**Normative effect: NONE.**
**Date:** 2026-08-15
**Prepared by:** Claude, acting as recording operator. **Not** the Protocol Custodian and
**not** the Architecture Owner.

**This is not an analytical task, not a DQ-002 decision, and not an architecture
proposal.** No option is selected; no question below is answered.

---

## 1. Purpose

To record **CONFLICT-DQ002-01** narrowly and exactly, and to place before the Protocol
Custodian the three questions whose answers are a prerequisite for DQ-002.

The record states, for each question, only: **SOURCE → LOCATION → NORMATIVE CLAIM →
UNRESOLVED POINT.** No interpretation is offered as an answer.

### 1.1 Source of truth

| Source | Pinned at |
|---|---|
| DQ-002 Decision Readiness | `178b960` |
| D3-S8 Evidence Base Refresh | `349d644` |
| APS-200, APS-300 (`AuraIDToken/aura-specification`) | `62d2d6b` — **re-read for this record** |

Where an earlier artifact was later corrected, the correction governs. Specifically:
ENT-005's entity-table row is **`APS-200:40`**; the value `:41` appearing in D3-S8 was
corrected in the Decision Readiness gate (`178b960`) and the corrected reference is used
here.

---

## 2. Conflict identifier

**CONFLICT-DQ002-01**

| Field | Value |
|---|---|
| Subject | The record-level integrity hash of an APS-200 entity |
| Documents | APS-200 and APS-300 |
| Status | **OPEN — UNRESOLVED** |
| Required authority | **Protocol Custodian** |
| Blocks | **DQ-002** (per Decision Readiness gate `178b960`) |

---

## 3. Evidence

### APS-200

**Document identity:** Document ID `APS-200`, Version `1.0-DRAFT`, Status **DRAFT**,
Authority `APS-001 · APS-100`.

| Location | Verbatim claim |
|---|---|
| `aps/APS-200_CANONICAL_DATA_MODEL.md:40` | `\| ENT-005 \| Evidence \| Execution proof \|` |
| `:49` | "Every entity MUST contain the following fields:" |
| `:58` | `\| `integrity_hash` \| string \| MUST \| SHA-256 hash of the canonical serialization of this object \|` |
| `:129` | "See APS-300 for the full Evidence Model. The canonical Evidence object fields are defined in APS-300 §5." |
| `:206` | "Integrity validation (`integrity_hash` matches computed hash)" — §7 validation rule 4 |
| `:218` | "**TODO**: Define the canonical serialization format for interoperability between RI-PY and RI-RS." |

### APS-300

**Document identity:** Document ID `APS-300`, Version `1.0-DRAFT`, Status **DRAFT**,
Authority `APS-001 · APS-100 · **APS-200**`.

| Location | Verbatim claim |
|---|---|
| `aps/APS-300_EVIDENCE_MODEL.md:54` | Section heading: "## 5. Canonical Evidence Object" |
| `:56` | "Every Evidence object MUST contain **at minimum**:" |
| `:60-71` | The MUST/SHOULD list: `evidence_id`, `protocol_version`, `schema_version`, `implementation_id`, `execution_id`, `timestamp`, `policy_reference`, `input_hash`, `output_hash`, `evidence_hash`, `previous_evidence_hash` (SHOULD), `attestation_reference` |
| `:69` | `\| `evidence_hash` \| string \| MUST \| SHA-256 hash of this Evidence object (excluding this field) \|` |
| `:73` | "**TODO**: Define the canonical algorithm for computing `evidence_hash`. Must reference INV-011 and specify whether the hash covers the full JSON serialization or a field-ordered canonical form." |

**Recorded as fact, not as an answer:** APS-300's Authority line names APS-200. This
record does **not** interpret what that implies for precedence — that is Q3.

**Recorded as fact:** APS-300 §5's list does **not** contain `object_id`, `object_type`,
`created_at` or `integrity_hash`.

---

## 4. Exact conflict

Four facts place both documents over the same object:

| # | Fact | Location |
|---|---|---|
| 1 | ENT-005 Evidence is an APS-200 entity | `APS-200:40` |
| 2 | The Common Object Contract — including `integrity_hash` — binds **every** entity | `APS-200:49`, `:58` |
| 3 | APS-200 delegates Evidence's field definition to APS-300 §5 | `APS-200:129` |
| 4 | APS-300 §5's "at minimum" MUST list omits `integrity_hash` and instead requires `evidence_hash` | `APS-300:56`, `:60-71`, `:69` |

The conflict has three distinct dimensions. **Each is recorded, none is resolved.**

| Dimension | APS-200 | APS-300 | Unresolved point |
|---|---|---|---|
| **Self-inclusion** | "hash of the canonical serialization of **this object**" — silent on whether `integrity_hash` itself is part of that representation (`:58`) | "hash of this Evidence object **(excluding this field)**" — explicit exclusion (`:69`) | Whether APS-200's silence means inclusion, exclusion, or is undetermined |
| **Cardinality** | Requires `integrity_hash` on every entity (`:49`, `:58`) | Requires `evidence_hash` on every Evidence object (`:69`) | Whether one Evidence object bears **one** record-level hash under two names, or **two** distinct record-level hashes |
| **Field set** | Four Common Object Contract fields are MUST on every entity (`:49`) | The "at minimum" list omits those four (`:56`, `:60-71`) | Whether the Common Object Contract binds ENT-005 despite the omission |

**Additional recorded fact, not a resolution.** APS-200's `integrity_hash` is defined by
reference to "the canonical serialization", which `APS-200:218` records as a **TODO**;
`evidence_hash`'s algorithm is likewise a **TODO** at `APS-300:73`. Both definitions
therefore depend on material the same documents state as undefined.

---

## 5. Questions requiring Custodian ruling

**No answer, preference, recommendation or default is offered for any question below.**

### Q1 — Self-inclusion / self-exclusion

> **Is `integrity_hash` computed from a representation of the object:**
> **A.** excluding the `integrity_hash` field;
> **B.** including the `integrity_hash` field;
> **C.** other — to be defined.

| Element | Content |
|---|---|
| **SOURCE** | APS-200 — Canonical Data Model, 1.0-DRAFT, Status DRAFT |
| **LOCATION** | `aps/APS-200_CANONICAL_DATA_MODEL.md:58`; scope at `:49`; validation rule at `:206` |
| **NORMATIVE CLAIM** | "`integrity_hash` \| string \| MUST \| SHA-256 hash of the canonical serialization of this object" |
| **UNRESOLVED POINT** | The text does not state whether the `integrity_hash` field is part of "this object" for the purpose of its own computation. `integrity_hash` is itself a MUST field of the object (`:49`). No other APS-200 text addresses the self-reference. |

### Q2 — Same concept / separate domains

> **Do `integrity_hash` (APS-200:58) and `evidence_hash` (APS-300:69):**
> **A.** denote the same normative concept;
> **B.** denote separate hash domains;
> **C.** other — to be defined.

| Element | Content |
|---|---|
| **SOURCE** | APS-200 — Canonical Data Model, 1.0-DRAFT · APS-300 — Evidence Model, 1.0-DRAFT |
| **LOCATION** | `APS-200:58`, `:49`, `:40`, `:129` · `APS-300:56`, `:69`, `:60-71` |
| **NORMATIVE CLAIM** | APS-200: `integrity_hash` is a MUST field of **every entity**, and ENT-005 Evidence is an entity. APS-300: `evidence_hash` is a MUST field of **every Evidence object**, defined as excluding itself; the same "at minimum" list omits `integrity_hash`. |
| **UNRESOLVED POINT** | No normative statement in either document declares whether the two fields are one concept under two names or two distinct hash domains. Neither document cross-references the other's field. **APS-200 contains no relational verb anywhere in the document** — a search for `includ`, `exclud`, `nest`, `derive`, `depend`, `cover`, `compris`, `consist of`, `based on` returns zero matches — so no relationship is stated to be inferred from. |

### Q3 — Precedence

> **If both texts govern the same concept and conflict, which text takes precedence, and
> what is its binding interpretation?**

| Element | Content |
|---|---|
| **SOURCE** | APS-200 · APS-300 · document identity headers |
| **LOCATION** | `APS-200` header (Authority: `APS-001 · APS-100`) · `APS-300` header (Authority: `APS-001 · APS-100 · APS-200`) · `APS-200:129` (delegation to APS-300 §5) · `APS-300:56` ("at minimum") |
| **NORMATIVE CLAIM** | APS-300 names APS-200 among its authorities. APS-200 delegates the Evidence field definition to APS-300 §5. APS-300 §5 introduces its list as "at minimum". |
| **UNRESOLVED POINT** | Two orderings are textually available and neither is stated to govern: APS-300 naming APS-200 as an authority, versus APS-200 delegating the field definition to APS-300. Whether "at minimum" permits APS-300's list to omit fields APS-200 makes mandatory, or requires them to be read in addition, is not stated. **No document in the corpus adjudicates a conflict between two APS documents.** |

---

## 6. Decision boundary

Answers to Q1–Q3 are a **prerequisite** for DQ-002, because they determine both the
**count** of record-level hash domains and the **definition** of the record-level domain
— the two things the DQ-002 hash-domain architecture decision selects among.

**This document does not take DQ-002.** It records the conflict and formulates the
questions. The DQ-002 decision remains reserved to the Architecture Owner, and is not
reached by answering Q1–Q3 alone.

### 6.1 Category separation

Recorded explicitly, per the required boundary:

> **OBSERVED IMPLEMENTATION:**
> Aura-Guard has its own hash constructions.
>
> **NORMATIVE CONTRACT:**
> APS-200 / APS-300 do not currently establish an unambiguous relationship sufficient to
> close the conflict.
>
> **ARCHITECTURAL DECISION:**
> **NOT MADE.**

### 6.2 Identifiers not equated

The following are **not** treated as the same concept anywhere in this record, and none
is equated with another absent unambiguous normative evidence:

| Identifier | Where it lives |
|---|---|
| `chain_hash` | Implementation only (`aura-guard-v1.3`); **0 occurrences** in the specification corpus |
| `integrity_hash` | `APS-200:58`; **0 occurrences** in `aura-guard-v1.3` `src/`, full history |
| `event_payload_hash` | `APS-200:159`; **0 occurrences** in `aura-guard-v1.3` `src/`, full history |
| `previous_record_hash` | `APS-200:158`; **0 occurrences** in `aura-guard-v1.3` `src/`, full history |
| `evidence_hash` | `APS-300:69`; not implemented |

The existence of hash constructions in Aura-Guard, the INFRA-001 and INFRA-002 harnesses,
the observed byte fixtures, and historical implementations are **not** treated as evidence
of the normative meaning of any of these identifiers.

---

## 7. Explicit non-decisions

This record confirms:

- **DQ-002 remains OPEN / BLOCKED** — decision NOT MADE;
- **no hash-domain architecture selected** — Options A, B, C and D from the prior DQ-002
  analysis all remain unselected;
- **no canonical serialization selected**;
- **DQ-006 remains unchanged** — CONFLICT;
- **no production code changed** in any repository;
- **no normative specification changed** — APS-200, APS-300, APS-100 and SPEC-002 are
  untouched;
- **no ADR approved** or created.

Additionally, this record:

- **does not resolve** Q1 (self-inclusion / self-exclusion);
- **does not resolve** Q2 (`integrity_hash` ↔ `evidence_hash` relationship);
- **does not resolve** Q3 (precedence);
- **does not reinterpret** APS-200, APS-300, APS-100 or SPEC-002;
- **does not perform** a further evidence refresh;
- **does not create** a further test harness;
- **does not change** DQ-001 (direction B; CONFLICT / OPEN; no implementation
  authorization; ADR not approved), DQ-003, DQ-004, DQ-005, DQ-007 or DQ-008;
- **opens no PR.**

---

## 8. Required authority

**Protocol Custodian.**

A ruling on Q1, Q2 and Q3 is required. Per the Decision Readiness gate (`178b960`), such a
ruling is **sufficient** to unblock DQ-002, and **no further evidence refresh is
required** — the gap is normative, not evidential.

---

## 9. Next authorized action

**Protocol Custodian ruling on CONFLICT-DQ002-01** — answering Q1, Q2 and Q3 as recorded
in §5.

No other action is authorized by this record. In particular: not the DQ-002 decision, not
DQ-006, and not a further evidence task.

---

DQ-002:
BLOCKED — CONFLICT-DQ002-01

AUTHORITY REQUIRED:
PROTOCOL CUSTODIAN

ARCHITECTURAL DECISION:
NOT MADE
