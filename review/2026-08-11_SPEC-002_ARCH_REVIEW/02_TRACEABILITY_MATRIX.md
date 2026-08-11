# 02 — Traceability Matrix

Document ID: REV-2026-08-11-002
Status: DRAFT — ANALYSIS ARTIFACT, NO NORMATIVE EFFECT
Date: 2026-08-11

---

## 0. Rules applied

Per the task's §5 constraints:

- **No REQ / INV / EVID / CONF / ARC identifier is invented.** Where an identifier does not
  exist, the cell reads exactly **`identifier not yet assigned`**.
- Where a link is absent altogether, the cell reads **`UNRESOLVED`**.
- Where a link *appears* to exist in an existing document but the target is a stub, a TODO,
  or a placeholder, the cell reads **`DANGLING → <target>`**. This distinction matters: the
  existing SPEC-002 §7 matrix presents several such links as if they were load-bearing.
- REQ-002-0xx identifiers are quoted from SPEC-002 v0.3 §4 and are **existing**. Identifiers
  in the range REQ-002-035…044 are **proposed in this review** (`03_SPEC-002_v0.4_DRAFT.md`)
  and are marked **(proposed)**. They have no normative effect.

---

## 1. Primary chain — AD-CA → ADR → REQ → INV → implementation → test → evidence

| AD-CA | ADR | SPEC-002 requirement | Invariant | Implementation component | Test | Evidence |
|---|---|---|---|---|---|---|
| **AD-CA-001** authoritative source boundary | ADR-002 **(NOT AUTHORED)** | REQ-002-001 … 005, 008, 009 | `identifier not yet assigned` | **UNRESOLVED** — no code in RI-PY or RI-RS reads `AURA_CONSTITUTION.md` | `identifier not yet assigned` (E1) | **UNRESOLVED** |
| **AD-CA-002** source canonicalization | ADR-002 **(NOT AUTHORED)** | REQ-002-006, 007, 010, 011 | `identifier not yet assigned` | **CONFLICT** — RI-RS `src/normalizer.rs` (SHADOW_SPEC v1.0) vs RI-PY (none). See 01 §C-1 | `identifier not yet assigned` (E1) | **UNRESOLVED** |
| **AD-CA-003** transformation pipeline | ADR-003 **(NOT AUTHORED)** | REQ-002-010, 011 | `identifier not yet assigned` | `core/embedding.py` — **self-declared placeholder** | `identifier not yet assigned` (E2) | **UNRESOLVED** |
| **AD-CA-004** normalization rules | **NONE — ORPHANED** | REQ-002-011, 021, 022 | `identifier not yet assigned` | **UNRESOLVED** | `identifier not yet assigned` | **UNRESOLVED** |
| **AD-CA-005** embedding method identity + versioning *(scope disputed — see 00 §4)* | ADR-003 **(NOT AUTHORED)** | REQ-002-012, 016, 024 | `identifier not yet assigned` | `core/embedding.py` — unnamed, unversioned, no identity | `identifier not yet assigned` (E3) | **UNRESOLVED** |
| **AD-CA-006** dictionary identity + dependency closure | **NONE — ORPHANED** | REQ-002-013, 016, 024, 034 | `identifier not yet assigned` | **UNRESOLVED** — no dictionary exists; no dependency manifest | `identifier not yet assigned` | **UNRESOLVED** |
| **AD-CA-007** numeric representation | ADR-004 **(NOT AUTHORED)** | REQ-002-014, 017 … 022 | `identifier not yet assigned` (relates to existing INV-001, INV-002, INV-006, INV-007) | `core/evaluator.py`, `core/offline_normalizer.py` — **NON-CONFORMANT**, see 01 §C-6, §C-7 | `identifier not yet assigned` (E4) | **UNRESOLVED** |
| **AD-CA-008** canonical serialization + hash domains | ADR-004 **(NOT AUTHORED)** | REQ-002-017 … 022 | `identifier not yet assigned` (relates to INV-003, INV-011) | **UNRESOLVED** — no serializer in RI-PY; GAP-001 §3 records APS-400 "Serialization" as ❌ Missing | `identifier not yet assigned` (E5, E6) | **UNRESOLVED** |
| **AD-CA-009** identity model | ADR-005 **(NOT AUTHORED)** | REQ-002-015, 016, 023, 024 | `identifier not yet assigned` (relates to INV-015) | **UNRESOLVED** — RI-PY records INV-015 as ❌ | `identifier not yet assigned` (E7) | **UNRESOLVED** |
| **AD-CA-010** provenance boundary | ADR-005 **(NOT AUTHORED)** | REQ-002-025, 030, 031, 033 | `identifier not yet assigned` | **UNRESOLVED** — no revision binding anywhere | `identifier not yet assigned` (E8) | **UNRESOLVED** |
| **AD-CA-011** registration | ADR-006 **(NOT AUTHORED)** | REQ-002-028, 030, 031 | `identifier not yet assigned` | **UNRESOLVED** — no registry exists | `identifier not yet assigned` (E9) | **UNRESOLVED** |
| **AD-CA-012** freeze lifecycle | ADR-006 **(NOT AUTHORED)** | REQ-002-029 … 031 | `identifier not yet assigned` | **CONFLICT** — RI-PY self-declares FROZEN without authority. See 01 §C-15 | `identifier not yet assigned` (E9, E10) | **UNRESOLVED** |

**Column totals:** ADR authored 0/12 · invariants assigned 0/12 · implementation
conformant 0/12 · conformance test assigned 0/12 · evidence 0/12.

---

## 2. Requirement-level detail (SPEC-002 v0.3 §4, all 34 existing requirements)

`SRC` = normative source cited by SPEC-002 §7 and whether that citation actually resolves.

| REQ | AD-CA | SRC resolves? | INV | CONF | EVID |
|---|---|---|---|---|---|
| REQ-002-001 | 001 | partial — Constitution Art. IV P8–10 exists but does not name a Source Set | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-002 | 001 | partial — APS-000 §4 is identifier format, not source boundary | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-003 | 001 | **DANGLING** — no repository-location field exists; two repos claim the name | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-004 | 001 | yes — VERSIONING.md §3–§4 | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-005 | 001 | yes — VERSIONING.md §3 (but see OD-005: only 1 doc is FROZEN) | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-006 | 002 | **DANGLING** — Art. IV P2/P8 state principles, define no encoding rules | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-007 | 002 | **DANGLING → APS-200 §8 (TODO)** | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-008 | 001, 002 | **DANGLING → APS-000 §7** (registry described, does not exist) | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-009 | 001 | yes — APS-000 §4 identifier-reuse rule | INV-015 (existing, Major) | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-010 | 003 | **DANGLING** — principles only | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-011 | 004 **(orphaned)** | **DANGLING → APS-200 §8 (TODO)** | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-012 | 005 | **DANGLING** — no embedding method is named anywhere | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-013 | 006 **(orphaned)** | **DANGLING** — no dictionary exists | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-014 | 007 | **DANGLING** — Art. IV P2/P8; no numeric contract in any APS | INV-007 (existing) | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-015 | 009 | partial — APS-000 §4; **contradicted by APS-200 §4** (01 §X-7) | INV-015 (existing) | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-016 | 009 | **DANGLING** — no binding fields defined | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-017 | 007, 008 | **DANGLING → APS-200 §4 + APS-300 §5 (TODO)** | INV-011 (existing) | CONF-010 (DRAFT, does not cover vectors) | UNRESOLVED |
| REQ-002-018 | 007, 008 | **DANGLING → APS-200 §4 + APS-300 §5 (TODO)** | INV-011 (existing) | CONF-010 (DRAFT, does not cover artifacts) | UNRESOLVED |
| REQ-002-019 | 008 | **DANGLING** | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-020 | 008 | **DANGLING** | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-021 | 008 (+004) | **DANGLING → APS-200 §8 (TODO)** | INV-003 (existing) | CONF-003 (DRAFT — **tests self-consistency only**, see §4) | UNRESOLVED |
| REQ-002-022 | 008 (+004) | **DANGLING → APS-200 §4 + APS-300 §5 (TODO)** | INV-003 (existing) | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-023 | 001, 002, 009 | **DANGLING → APS-900 §3–§4** | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-024 | 005, 006, 007, 009 | **DANGLING → APS-900 §3–§4** | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-025 | 010 | partial — Constitution Art. X (Evidence) | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-026 | — | yes — VERSIONING.md §3–§4, §9 | INV-009 (existing) | CONF-008 (DRAFT) | UNRESOLVED |
| REQ-002-027 | 009, 011, 012 | **DANGLING** — `supersedes` has no field in APS-200 | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-028 | 011 | **DANGLING → APS-000 §7** (registry does not exist) | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-029 | 012 | partial — VERSIONING.md §3; **contradicted by self-freeze**, 01 §C-15 | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-030 | 010, 011, 012 | partial — Constitution Art. III/IV | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-031 | 010, 011, 012 | partial — Art. IV P6; APS-300 §12 | INV-008 (existing) | CONF-007 (DRAFT) | UNRESOLVED |
| REQ-002-032 | all | n/a — readiness gate | — | — | — |
| REQ-002-033 | 010 | **DANGLING** — provenance boundary undefined by design | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |
| REQ-002-034 | 005, 006 **(006 orphaned)** | **DANGLING** — no dependency manifest exists | `identifier not yet assigned` | `identifier not yet assigned` | UNRESOLVED |

**Resolution count for existing requirements: 0 of 34 fully traced.**
Sources resolve for 5 (REQ-002-004, 005, 009, 026, and partially 031); **17 are DANGLING**.

---

## 3. Proposed requirements from this review (no normative effect)

| REQ (proposed) | Subject | AD-CA | Evidence of need |
|---|---|---|---|
| REQ-002-035 | Source representation of record (`.md` vs preserved `.txt`/`.pdf`) | 001 | Every APS doc carries a "*Source: Original text preserved in …*" footer, implying the `.txt` is authoritative, while the `.md` is what the repo structure treats as canonical |
| REQ-002-036 | Vector dimension and index ordering | 003, 007 | 1536 in RI-PY vs `32` token in SPEC-002 (01 §C-3) |
| REQ-002-037 | Input-length domain: empty / minimum / maximum / tiling / truncation | 003 | `core/embedding.py` silently truncates past 1536 chars (01 §C-4) |
| REQ-002-038 | Integer division and rounding semantics, language-independent | 007 | Floor-vs-truncate divergence demonstrated (01 §C-6) |
| REQ-002-039 | Float→fixed-point boundary and rounding mode | 007 | `round()` half-to-even vs half-away divergence demonstrated (01 §C-7) |
| REQ-002-040 | Operand-dimension agreement MUST fail closed | 007 | `zip` silently truncates mismatched vectors (01 §C-10) |
| REQ-002-041 | Authoritative repository designation | 001 | Two repos named `aura-specification` (00 §6) |
| REQ-002-042 | Tolerance-based validation MUST NOT establish canonical identity | 007 | `verify_unit_vector` ±1% tolerance (01 §C-8) |
| REQ-002-043 | ADP-001 MUST NOT be referenced until fully defined | 003 | ADP-001 is 0/14 defined (01 §7) |
| REQ-002-044 | Invalid lifecycle transitions MUST be enumerated with fail-closed response | 011, 012 | No invalid-transition set exists for any artifact class (01 §6) |

---

## 4. Conformance-test coverage of the Constitution Artifact surface

| CONF | Declared subject | Covers Constitution Artifact / Vector? | Note |
|---|---|---|---|
| CONF-001 | Deterministic Evaluation | **No** | scoped to Evaluation Request/Result |
| CONF-002 | Replay Verification | **No** | scoped to Evidence Pack replay |
| CONF-003 | Canonical Serialization | **No — and structurally weak** | §4 procedure is "serialize ENT-001…ENT-008 twice … (fresh process each time)". This tests **one implementation against itself**, not two implementations against each other. It cannot detect C-6 or C-7, which are *cross-language* divergences. INV-003 is therefore not actually verified by CONF-003 for interoperability purposes. |
| CONF-004 | Evidence Integrity | No | |
| CONF-005 | Traceability | No | |
| CONF-006 | Platform Independence | **No** | §PASS criterion is "same Evidence Pack produced on x86 and ARM" — same-language, cross-architecture only. Blind to C-6/C-7. |
| CONF-007 | Fail Closed | No | would catch C-10 if extended to vector operations; currently not scoped to them |
| CONF-008 | Version Compatibility | No | |
| CONF-009 | Evidence Completeness | No | |
| CONF-010 | Cryptographic Verification | No | scoped to Evidence Pack hashes |

**Coverage of the Constitution Artifact surface: 0 of 10.** Every conformance test that
SPEC-002 §7 could point at is scoped to the evaluation/evidence path, not to artifact
construction. This is why every Conformance Test ID in SPEC-002 §7 correctly reads
`FUTURE REF`.

---

## 5. Invariant coverage

| Existing INV | Bears on Constitution Artifact? | Status |
|---|---|---|
| INV-001 Deterministic Evaluation | indirectly | CONF-001 exists; does not cover artifact construction |
| INV-002 Bit-Perfect Replay | **yes — currently defeated** by 01 §C-6/§C-7 across languages | CONF-002 exists; cannot detect cross-language divergence |
| INV-003 Canonical Serialization | **yes — unverifiable**, no canonical format defined (X-6) | CONF-003 weak (§4 above) |
| INV-006 Platform Independence | **yes — currently defeated** across languages | CONF-006 weak (§4 above) |
| INV-007 Zero Float Runtime | yes | **no CONF test** — self-reported INV-010 violation |
| INV-008 Fail Closed | **yes — currently violated** by 01 §C-10 | CONF-007 exists, not scoped to vectors |
| INV-011 Cryptographic Integrity | yes | CONF-010 exists, not scoped to artifact/vector hashes |
| INV-015 Canonical Identity | yes | **no CONF test**; RI-PY records ❌ |

**New invariants required by AD-CA-001…012: at least one per domain, `identifier not yet
assigned` in every case.** Note that adding them without CONF tests would extend the
existing INV-010 Critical violation (5 invariants already lack tests).

---

## 6. ARC layer

| ARC | SPEC | Status |
|---|---|---|
| — | SPEC-002 | **UNRESOLVED.** `arc/` is empty; `arc_to_spec_mapping.yaml` is `mappings: []`; `ARC_TO_SPEC_MAPPING.md` defers to "when SPEC-001 is approved", and SPEC-001 does not exist. Under `ADR-001_DOCUMENT_MODEL` INV-DOC-002 every SPEC must reference ≥1 ARC, so SPEC-002 is non-conformant on the model that defines it. |

---

## 7. Cross-repository identifier collision (blocks all cross-repo traceability)

> **CONFLICT DETECTED — C-17 (P0)**

**Source A** — `AuraIDToken/aura-specification`, `aps/`:

| ID | Subject |
|---|---|
| APS-200 | Canonical Data Model |
| APS-400 | Conformance Test Matrix |
| APS-500 | Reference Fixtures |
| APS-900 | Compliance Mapping |

**Source B** — `aura-poc-a-core-v3.3`, `docs/GAP-001.md` §3 "APS Coverage Matrix":

| ID | Subject |
|---|---|
| APS-200 | **ARI Engine** |
| APS-400 | **Serialization** |
| APS-500 | **ZK Layer** |
| APS-900 | **Conformance Runner** |

**Nature of conflict.** The same identifiers denote entirely different subject matter in the
two repositories. GAP-001 states plainly that it inferred requirements because *"the external
`aura-specification` repository is not co-located here"* — i.e. the APS IDs were reconstructed
from memory rather than read.

**Impact.** Every cross-repository traceability claim is unsound. A conformance statement of
the form "RI-PY partially satisfies APS-200" is **ambiguous between two different
specifications**. This directly violates APS-000 §4 (identifiers unique, never reused) and
AGENTS.md rule 7 ("compliance claims must not be inferred merely from architecture names").

**Required decision.** GAP-001's coverage matrix MUST be either withdrawn or re-mapped to the
real APS identifiers before any conformance claim crosses repository boundaries.
→ **OD-009**, **BLOCKER-P0-010**.

---

## 8. What a complete chain would look like (target state, for one domain)

Recorded so the gap is concrete rather than abstract. Nothing below exists yet.

```
AD-CA-007  (numeric representation)
    ↓ resolved by
ADR-004    (NOT AUTHORED)  ── requires RFC per GOV-001 §5.2
    ↓ incorporated into
SPEC-002 v0.5 REQ-002-014, REQ-002-038, REQ-002-039   (035–044 proposed, not approved)
    ↓ enforced by
INV-xxx    identifier not yet assigned
    ↓ verified by
CONF-xxx   identifier not yet assigned      ← must be cross-language, unlike CONF-003/006
    ↓ exercised against
FIX-xxx    identifier not yet assigned      ← E4 numeric boundary vectors
    ↓ producing
EVID-xxx   identifier not yet assigned
    ↓ released in
REL-xxx    identifier not yet assigned
```

Eight links. **Zero currently exist for any of the twelve AD-CA domains.**

---

*End of 02_TRACEABILITY_MATRIX.md*
