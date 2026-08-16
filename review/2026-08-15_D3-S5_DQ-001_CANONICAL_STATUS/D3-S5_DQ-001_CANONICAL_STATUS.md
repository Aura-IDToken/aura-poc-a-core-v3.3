# DQ-001 — Canonical Status Record

**Document class:** repository governance / status record.
**Purpose:** to give the repository **one** unambiguous statement of the Architecture
Owner's current status for DQ-001.
**Date:** 2026-08-15
**Recorded by:** Claude, acting as repository governance/documentation operator at the
direction of the Architecture Owner. Claude is **not** the Architecture Owner and has
entered no decision here.

**This record does not reopen the DQ-001 evidence investigation, does not re-evaluate
Option A/B/C, does not resolve CONFLICT-DQ001-01, and grants no implementation
authorization.**

---

## 1. Current Status

| Field | Value |
|---|---|
| **Architectural Direction** | **B — Adapter Architecture** |
| **Evidence Status** | **CONFLICT / OPEN** |
| **Normative Closure** | **NOT CLOSED** |
| **Implementation Authorization** | **NO** |
| **ADR** | **NOT APPROVED** |

This is the **current status record** for DQ-001. Where any other artifact in this
repository states a different *status*, this record is the one to read.

---

## 2. Architectural Direction

**Option B — Adapter Architecture is the accepted architectural direction for future
work.**

That means: work that must assume a direction of travel for DQ-001 may assume B.

It does **not** mean any of the following, and this record must not be cited for any of
them:

- B is **not** described as FROZEN.
- B is **not** a normative decision.
- B does **not** authorise implementation.
- B does **not** close DQ-001.
- B does **not** resolve, weaken or supersede CONFLICT-DQ001-01.

The distinction this record exists to preserve is between an accepted **direction** and a
completed **closure**. DQ-001 has the former and not the latter.

---

## 3. Evidence / Normative Status

**CONFLICT / OPEN. NOT CLOSED.**

DQ-001 remains open at the evidence and normative level because the previously identified
conflict has not been resolved. The conflict is recorded in §8 and is unchanged by this
record.

No evidence was re-examined, re-weighed or added in producing this record. The evidence
base remains as established in the artifacts listed in §6.

---

## 4. Implementation Authorization

**NO.**

No implementation authorization is granted by this record. Specifically, this record does
**not** authorise:

- creating an adapter module or an ENT-007 target type;
- modifying `models.rs`, `chain.rs`, or any other production source in
  `AuraIDToken/aura-guard-v1.3`;
- modifying production source in `AuraIDToken/aura-poc-a-core-v3.3`;
- emitting, publishing or anchoring any APS-200-shaped object;
- changing serialization, hashing, field names or any public API.

Implementation authorization for DQ-001 requires a separate, explicit act by the
Architecture Owner. It is not implied by the acceptance of a direction.

---

## 5. ADR Status

**NOT APPROVED.**

An ADR **candidate** exists at
`review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/D3-S4_DQ-001_ADAPTER_ARCHITECTURE_REVIEW.md`
§15, carrying the status `PROPOSED / NOT APPROVED`.

That candidate is **not** approved by this record, is **not** filed, is **not** numbered,
and is **not** registered. No ADR was created, amended or approved in producing this
record.

---

## 6. Historical Status Conflict

Two artifacts already in this repository state DQ-001's status differently. **Both are
preserved unchanged.** Neither has been deleted, edited or rewritten.

| # | Artifact | Commit | Exact statement |
|---|---|---|---|
| **1** | `review/2026-08-15_D3-S6_DQ-006_CANONICAL_SERIALIZATION/D3-S6_DQ-006_CANONICAL_SERIALIZATION_REVIEW.md:18` (premise table §0.1) | `a0c4901` | "**DQ-001** — **ACCEPTED — Option B, explicit adapter architecture.** Frozen." |
| **2** | `review/2026-08-15_D3-S8_EVIDENCE_BASE_REFRESH/` — `D3-S8_EVIDENCE_BASE_REFRESH.md:323` and `DQ_EVIDENCE_GATE.md:10` | `349d644` | "**DQ-001** \| **CONFLICT**" — and, at `DQ_EVIDENCE_GATE.md:23`, that a decision cannot be made from current evidence |

The divergence was itself already detected and registered, before this record existed, as
**CONFLICT-DQ008-01** at
`review/2026-08-15_D3-S8_EVIDENCE_BASE_REFRESH/PREVIOUS_FINDINGS_REASSESSMENT.md:39,52`.
That registration is also preserved unchanged.

**Provenance of artifact 1's wording.** The "ACCEPTED … FROZEN" phrasing entered the
repository as a **premise supplied to the D3-S5 task**, quoted at
`PREVIOUS_FINDINGS_REASSESSMENT.md:46`, and was carried forward into artifact 1's premise
table. It was not a conclusion reached by analysis.

---

## 7. Canonical Interpretation

**This record supersedes the ambiguity between artifacts 1 and 2 only as the CURRENT
STATUS RECORD. It does not rewrite historical evidence.**

Concretely:

| Question | Answer |
|---|---|
| Which artifact states DQ-001's status **now**? | **This one.** |
| Are artifacts 1 and 2 still valid as historical records? | **Yes.** Each accurately records what was stated at the time it was written. |
| Does this record invalidate the *evidence* in artifacts 1 or 2? | **No.** Only their *status statements* are superseded. Every file/line finding in both stands on its own. |
| Was artifact 1's "FROZEN" wording correct? | It is **superseded**. B is a direction, not a frozen decision. This record deliberately does not use the word FROZEN for B. |
| Was artifact 2's "CONFLICT" correct? | **Yes, and it remains correct** at the evidence and normative level. This record restates it. |
| Does accepting direction B close DQ-001? | **No.** Direction accepted; closure not reached. |

Anyone citing DQ-001's status must cite this record. Anyone citing DQ-001's *evidence*
should cite the underlying artifacts directly.

---

## 8. Open Conflict

**CONFLICT-DQ001-01 — OPEN. Unchanged by this record.**

| Field | Content |
|---|---|
| Statement | INV-012 is stated with different scope in two normative-corpus documents |
| Source A | `aura-specification` `aps/APS-100_PROTOCOL_INVARIANTS.md:92` — "audit trail" |
| Source B | `aura-specification` `invariants/INVARIANT_REGISTRY.md:273` — "Audit Record (ENT-007)" |
| Registered in | `review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/` §4.1 |
| Resolution owner | **Protocol Custodian** |
| Status | **OPEN — not resolved, not reconciled, not reinterpreted by this record** |

**CONFLICT-DQ008-01 — ADDRESSED AS TO STATUS ONLY.** The status ambiguity between
artifacts 1 and 2 is resolved by §1 of this record. The underlying governance question it
raised — how a supplied premise should be reconciled with an evidence finding — is not
addressed here.

Other open conflicts recorded elsewhere (CONFLICT-DQ002-01, CONFLICT-DQ006-01,
CONFLICT-DQ006-02, OQ-A-CONFLICT-001/002) are **unaffected** by this record.

---

## 9. Next Authorized Action

1. **Protocol Custodian ruling on CONFLICT-DQ001-01** — required before DQ-001 can reach
   normative closure.
2. **Architecture Owner decision on normative closure of DQ-001** — separate from, and
   not implied by, the acceptance of direction B.
3. **Architecture Owner grant of implementation authorization** — separate again, and not
   implied by either of the above.

Until (1)–(3), DQ-001 remains **CONFLICT / OPEN**, and no DQ-001 implementation work is
authorised.

**Not authorised by this record:** reopening the DQ-001 investigation, re-evaluating
Options A/B/C, resolving CONFLICT-DQ001-01, approving the ADR candidate, modifying
production code, or modifying APS-200/APS-100.

---

## 10. Canonical Statement

> **Option B — Adapter Architecture is the accepted architectural direction.
> DQ-001 remains CONFLICT / OPEN at the evidence and normative level.
> No implementation authorization is granted by this record.**

---

## Declarations

- **No production code was modified** in any repository.
- **No normative document was modified.** APS-200, APS-100, APS-300, SPEC-002 and
  `AUDIT_LAYER_SPEC.md` are untouched.
- **No ADR was created, amended or approved.**
- **No normative decision was made.**
- **No historical artifact was deleted, edited or rewritten.**
- **CONFLICT-DQ001-01 was not resolved.**
- **The DQ-001 evidence investigation was not reopened**, and no evidence was
  re-evaluated.
- **DQ-002 … DQ-008 are untouched** and retain the statuses recorded in
  `review/2026-08-15_D3-S8_EVIDENCE_BASE_REFRESH/DQ_EVIDENCE_GATE.md`.
- **No PR was opened. No merge. No freeze.**
