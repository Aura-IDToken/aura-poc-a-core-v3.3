# DQ-002 — Decision Readiness Gate

**Question answered:** is the current evidence base sufficient to make the DQ-002 —
Layered Hash Domains — architectural decision?
**Document class:** readiness gate. **Normative effect: NONE.**
**Date:** 2026-08-15
**Prepared by:** Claude. **Not** the Architecture Owner.

**This gate does not decide DQ-002.** It classifies readiness only.

---

## 1. Scope

Exactly five questions are answered (§3–§7). Nothing else was investigated.

**Explicitly outside this gate:** deciding DQ-002; proposing a hash-domain model;
changing code; creating a harness; reinterpreting APS-200 / APS-100 / SPEC-002;
supplying missing semantics by assumption.

### 1.1 Three categories held apart

Per the task's instruction, no item below is allowed to migrate between these columns:

| Category | What it is | What it is **not** |
|---|---|---|
| **OBSERVED IMPLEMENTATION** | SHA-256 constructions running in `aura-guard-v1.3`; the INFRA-001/INFRA-002 fixtures | **not** evidence that any of it has normative meaning |
| **NORMATIVE CONTRACT** | Text in APS-200 / APS-100 / APS-300 / SPEC-002 | **not** established merely because an implementation exists |
| **ARCHITECTURAL INFERENCE** | Reasoning built on the two above | **not** a substitute for either |

Specifically: the existence of hash constructions in the Guard, INFRA-001, INFRA-002, the
observed byte fixtures, and the historical implementations are **not** treated anywhere in
this gate as evidence of normative meaning.

---

## 2. Evidence base used

| Source | Pinned at | Used for |
|---|---|---|
| D3-S8 Evidence Base Refresh | `349d644` | Prior classification, conflict register |
| DQ-002 prior analysis / conflict record | `d7ddc6f` (`review/2026-08-15_D3-S5_DQ-002_LAYERED_HASH_DOMAINS/`) | CONFLICT-DQ002-01 as previously registered |
| INFRA-001 harness + inventory | `9c6bc37` | Construction count, exercised/unexercised split, UNKNOWN properties |
| INFRA-002 fixture framework | `d704285` | Representation model; confirmation that no fixture is NORMATIVE |
| `aura-specification` APS-200 / APS-100 / APS-300 / SPEC-002 | `62d2d6b` | Normative text, re-read for this gate |
| `aura-guard-v1.3` `src/` | `443f72e` | Presence/absence of the three normative fields |

ADR and history were used **as evidence only**, never as a substitute for a normative
contract.

**Re-verification performed for this gate** (not carried from prior reports): the
APS-200/APS-300 conflict text; the INFRA-001 inventory counts; and the absence of all
three normative fields from the Guard's `src/`.

**One citation correction.** D3-S8 cited ENT-005's entity-table row as `APS-200:41`. The
correct line is **`APS-200:40`**; `:41` is ENT-006. The substance is unaffected — ENT-005
is still listed as an entity — but the corrected reference is used below.

---

## 3. Hash construction coverage

**Question 1 — are all material hash constructions now identified?**

**YES, for the observed implementation.**

| Metric | Value | Source |
|---|---|---|
| Distinct construction entries | **15** | `tests/fixtures/hash_domains/INVENTORY.json` @ `9c6bc37` |
| Primitives (`sha256_hex`, `sha256_bytes_hex`) | **2** | same |
| Exercised with a replayable fixture | **11** | same |
| Not exercised | **4** | same |
| Properties recorded `UNKNOWN` | **3** | same |

**The four not exercised**, each with a stated reason — none is a missing or unidentified
construction, all are identified and located:

| Construction | Source | Reason |
|---|---|---|
| `rfc3161_request_digest` | `src/rfc3161.rs:138` | requires a live RFC 3161 TSA |
| `tst_verify_digest_message_imprint` | `src/tst_verify.rs:657` | private TST parsing path |
| `tst_verify_digest_signed_attrs` | `src/tst_verify.rs:839` | private CMS verification path |
| `aura_seal_cli_digest` | `src/bin/aura_seal.rs:500` | binary target, not library surface |

**The three UNKNOWN properties** are all `field_order`, on `rfc3161_request_digest`,
`tst_verify_digest_message_imprint` and `tst_verify_digest_signed_attrs`. Each is UNKNOWN
because the source does not establish it (caller-determined, or DER-determined).
**No missing construction is guessed at, and no UNKNOWN is filled in.**

**Bearing on the decision:** the four unexercised constructions are all in the RFC 3161 /
TSA and CLI periphery. **None of them is a candidate for the record-level, payload-level
or chain-link domains DQ-002 must settle**, so their unexercised status does not itself
block the decision.

**Category discipline:** this section is entirely **OBSERVED IMPLEMENTATION**. It
establishes nothing about normative meaning.

---

## 4. Normative field coverage

**Question 2 — for each of the three APS-200 fields, can the hash domain, input/preimage,
canonical-serialization dependency, and relationship to the other fields be established?**

| | `integrity_hash` | `event_payload_hash` | `previous_record_hash` |
|---|---|---|---|
| **Normative locus** | `APS-200:58` (Common Object Contract, §4) | `APS-200:159` (ENT-007) | `APS-200:158` (ENT-007) |
| **Hash domain** | **CONFLICT** — record-level, but whether it is one domain or two (with `evidence_hash`) is unresolved (§5) | **PARTIAL** — payload-level by name | **ESTABLISHED** — chain-link, stated explicitly |
| **Input / preimage** | **NOT ESTABLISHED** — "the canonical serialization of this object", which `APS-200:218` records as TODO; self-inclusion **unstated** | **NOT ESTABLISHED** — "the event payload" is undefined in APS-200, APS-000 and `GLOSSARY.md` | **PARTIAL** — "the previous Audit Record"; algorithm **unstated** |
| **Canonical serialization dependency** | **YES, blocking** — defined *by reference* to it | **YES** | **YES** |
| **Relationship to the other two** | **NONE STATED** | **NONE STATED** | **NONE STATED** |
| **Implemented in `aura-guard-v1.3`** | **NO** — 0 files, 0 commits in `src/`, full history | **NO** — 0 / 0 | **NO** — 0 / 0 (the *concept* exists as `prev_hash`; the name does not) |

**On relationships.** APS-200 contains **no relational verb anywhere in the document** —
a search for `includ`, `exclud`, `nest`, `derive`, `depend`, `cover`, `compris`,
`consist of`, `based on` returns zero matches. The three fields appear as **sibling MUST
rows** (`:58` in §4; `:158`, `:159` in ENT-007's table). **NO NORMATIVE RELATIONSHIP IS
ESTABLISHED**, and none is inferred here.

**Answer to Question 2: NO — not for all three.** Only `previous_record_hash` has an
establishable domain, and even it lacks a stated algorithm. `integrity_hash` is in
conflict; `event_payload_hash` has no definable input.

---

## 5. Active blocking conflicts

**Question 3 — does a normative conflict still block DQ-002?**

**YES. CONFLICT-DQ002-01 is confirmed present in the current sources**, re-read for this
gate at `62d2d6b`.

### CONFLICT-DQ002-01 — SOURCE → LOCATION → CLAIM → CONFLICT

| # | SOURCE | LOCATION | CLAIM |
|---|---|---|---|
| **A** | APS-200 (Canonical Data Model, 1.0-DRAFT) | `aps/APS-200_CANONICAL_DATA_MODEL.md:58` | "`integrity_hash` \| string \| MUST \| **SHA-256 hash of the canonical serialization of this object**" |
| **B** | APS-300 (Evidence Model, 1.0-DRAFT) | `aps/APS-300_EVIDENCE_MODEL.md:69` | "`evidence_hash` \| string \| MUST \| **SHA-256 hash of this Evidence object (excluding this field)**" |

**Binding facts that put A and B over the same object:**

| Fact | Location |
|---|---|
| ENT-005 Evidence is an APS-200 entity | `APS-200:40` |
| The Common Object Contract binds **every** entity | `APS-200:49` — "Every entity MUST contain the following fields:" |
| APS-200 delegates Evidence's fields to APS-300 §5 | `APS-200:129` |
| APS-300 §5's list is "at minimum" and **omits** `object_id`, `object_type`, `created_at`, `integrity_hash` | `APS-300:56`, `:59-71` |
| `evidence_hash`'s algorithm is itself a TODO | `APS-300:73` |

**CONFLICT — stated precisely, three ways:**

1. **Self-inclusion.** A requires the hash "of this object" and **does not state** that the
   field is excluded from its own input; B states its analogue **is** excluded. As written,
   A is **circular and therefore uncomputable**; B is computable.
2. **Cardinality.** For one Evidence object, A requires `integrity_hash` and B requires
   `evidence_hash`. Whether that is **one** record-level domain under two names, or **two**
   distinct record-level domains, is unresolved.
3. **Field-set.** A makes four Common Object Contract fields mandatory that B's "at
   minimum" MUST-list omits.

### Why this changes the possible outcome of DQ-002

DQ-002 selects the **hash-domain architecture**: how many domains exist and what each
covers. CONFLICT-DQ002-01 changes the answer to **both** halves:

| Custodian ruling | Effect on the DQ-002 outcome |
|---|---|
| `integrity_hash` and `evidence_hash` are **one** concept | One record-level domain; the record-level definition is self-**excluding** |
| They are **two** distinct concepts | Two record-level domains, each needing its own definition |
| A is authoritative **as literally written** | The record-level domain is **circular and uncomputable**, and options premised on a computable record-level hash are unavailable |

Because the domain **count** and the record-level domain's **definition** both move with
the ruling, the conflict does not merely add uncertainty — it changes which architectural
options are available. Under the stated decision rule, that mandates **BLOCKED**.

**Status: OPEN. Not resolved, not reconciled, not reinterpreted by this gate.**

---

## 6. Non-blocking gaps

Recorded for completeness, **not** as blockers. This is deliberately not a list of all
open questions — only items considered and found **not** materially blocking the
hash-domain architecture decision.

| Gap | Why it does **not** block DQ-002 |
|---|---|
| "Event payload" undefined (`APS-200:159`; DQ-004) | Blocks *specifying* the payload domain's input, not *deciding whether a payload domain exists*. It becomes blocking at DQ-006/DQ-004, not here |
| Canonical serialization undefined (`APS-200:218`; DQ-006) | DQ-006 is downstream by the stated ordering; the domain **model** can be chosen before its byte representation |
| `previous_record_hash` algorithm unstated (`APS-200:158`) | The domain's *role* (chain link) is stated; the algorithm is a specification detail |
| 4 constructions not exercised (§3) | All in the RFC 3161 / CLI periphery; none is a candidate for the domains under decision |
| 3 `field_order` properties UNKNOWN (§3) | Confined to the same peripheral constructions |
| No cross-implementation conformance test (CONFLICT-DQ006-01) | Blocks *verifying* a decision once made, not *making* it |
| Authority-direction conflict (CONFLICT-DQ006-02) | Bears on DQ-006's canonical-bytes question |
| `violations` binding (DQ-005) | Determines domain *membership*, decidable after the domain model |
| Whole normative corpus is DRAFT (`VERSIONING.md:38`) | Bounds the **durability** of any decision, not its **availability** |

---

## 7. Decision readiness classification

**Question 4 — is there any other blocker materially preventing the DQ-002 decision?**

**NO.** Every other item examined (§6) either belongs to a downstream DQ, or affects
verification/specification rather than the architecture choice itself. **Exactly one
blocker is material.**

**Question 5 — classification:**

> ## **B — BLOCKED — ONE SPECIFIC NORMATIVE BLOCKER**

Applying the stated decision rule: an unresolved normative conflict exists
(CONFLICT-DQ002-01) and it **changes the possible outcome** of DQ-002 (§5), so the result
must be BLOCKED. The `EVIDENCE INSUFFICIENT` branch is not reached, because that branch
applies only where no such conflict exists.

**Note on what is *not* the problem.** Evidence coverage is good: 15 constructions
identified, 11 replayable, every UNKNOWN attributed to a stated source limitation. DQ-002
is not blocked by a shortage of observation. It is blocked by the **normative corpus
contradicting itself** about the record-level integrity hash.

---

## 8. Exact blocker / required authority

| Field | Content |
|---|---|
| **Blocker** | **CONFLICT-DQ002-01** |
| **Statement** | `APS-200:58` and `APS-300:69` specify the record-level integrity hash of the same object incompatibly: self-inclusion unstated versus explicitly excluded; one name versus two; and APS-300's "at minimum" list omits four fields `APS-200:49` makes mandatory |
| **Required authority** | **Protocol Custodian** |
| **Ruling required on** | (a) Is `integrity_hash` computed **including or excluding** its own field? (b) Are `integrity_hash` and `evidence_hash` **one** concept or **two**? (c) Does the Common Object Contract bind ENT-005 despite APS-300 §5's omission? |
| **Sufficient to unblock?** | **Yes.** A ruling on (a)–(c) settles the record-level domain's count and definition, which is what makes the DQ-002 options determinate |
| **Not required to unblock** | DQ-006, DQ-004, DQ-005, the missing cross-implementation test, or any further evidence refresh |

**Per the operating rule:** the next action addresses **only** this blocker. **No further
broad evidence refresh is warranted** — the D3-S8 refresh is current and the gap is
normative, not evidential.

---

## 9. Explicit non-decisions

This artifact:

- **does NOT select a hash-domain architecture** — Options A, B, C and D from the prior
  DQ-002 analysis remain equally unselected;
- **does NOT establish canonical serialization**;
- **does NOT change DQ-002** — it remains CONFLICT, decision NOT MADE;
- **does NOT change DQ-006** — it remains CONFLICT;
- **does NOT change production code** — no repository source was modified;
- **does NOT create a normative contract**;
- **does NOT resolve, reconcile or reinterpret CONFLICT-DQ002-01**;
- **does NOT reinterpret** APS-200, APS-100, APS-300 or SPEC-002;
- **does NOT supply missing semantics by assumption** — every gap is recorded as
  NOT ESTABLISHED or UNKNOWN;
- **does NOT treat** the Guard's hash constructions, INFRA-001, INFRA-002, the observed
  byte fixtures or historical implementations **as evidence of normative meaning**;
- **does NOT change** DQ-001 (direction B; CONFLICT / OPEN; no implementation
  authorization; ADR not approved), DQ-003, DQ-004, DQ-005, DQ-007 or DQ-008;
- **creates no ADR** and **opens no PR**.

---

DQ-002 DECISION READINESS:
BLOCKED — ONE SPECIFIC NORMATIVE BLOCKER

NEXT AUTHORIZED ACTION:
Obtain a Protocol Custodian ruling on CONFLICT-DQ002-01 — specifically whether `integrity_hash` (`APS-200:58`) is computed including or excluding its own field, and whether it and `evidence_hash` (`APS-300:69`) are one concept or two.
