# RD-1-FINAL-PDF — 01 PDF EVIDENCE

---

## 1. Extraction outcome

| ID | Pages | pypdf chars | pdfminer chars | Image XObjects | Blank pages | Extraction |
|---|---|---|---|---|---|---|
| Constitution | 14 | 4 513 | 4 023 | **0** | 14 | ✅ |
| APS-000 | 19 | 5 299 | 4 635 | **0** | 18, 19 | ✅ |
| APS-100 | 15 | 4 537 | 4 086 | **0** | 14, 15 | ✅ |
| APS-200 | 11 | 3 200 | 2 807 | **0** | 10, 11 | ✅ |
| APS-300 | 13 | 4 107 | 3 654 | **0** | 12, 13 | ✅ |
| APS-950 | 14 | 3 886 | 3 387 | **0** | 12, 13, 14 | ✅ |

**All six are born-digital with complete text layers. Zero image XObjects across 86 pages.**
Every page lacking text is a blank trailing page containing no raster content. **No OCR was
required and none was performed** — there is no image in which text could be concealed.

## 2. Strict token search — the decisive table

Case-**sensitive**, word-**boundary**, both engines:

| Document | `ARI` | `PoCA` | `RI-PY` | `MUST` | `SHALL` | `REQUIRED` |
|---|---|---|---|---|---|---|
| Constitution | **0** | **0** | **0** | 0 | 0 | 0 |
| APS-000 | **0** | **0** | **0** | 4–6 | 0 | 0 |
| APS-100 | **0** | **0** | **0** | 36 | 0 | 0 |
| APS-200 | **0** | **0** | **0** | 7 | 0 | 0 |
| APS-300 | **0** | **0** | **0** | 7 | 0 | 0 |
| APS-950 | **0** | **0** | 2 | 12 | 0 | 14 |

Case-insensitive literal phrase search — **all six documents, both engines**:

| Phrase | Result |
|---|---|
| `Agent Reliability Index` | **0 in all six** |
| `Aura Reliability Index` | **0 in all six** |
| `reliability index` | **0 in all six** |
| `drift` | **0 in all six** |
| `rounding` | **0 in all six** |
| `division` | **0 in all six** |
| `bounds` | **0 in all six** |
| `formula` | **0 in all six** |

**Not one standalone `ARI` token exists in any of the six highest-authority PDFs.** No
formula-, rounding-, division-, bounds- or drift-bearing term appears in any of them.

### 2.1 Engine divergence — investigated and resolved

APS-950 showed `RI-PY` = 2 (pypdf) vs 0 (pdfminer), and `REQUIRED` = 14 vs 0. Both are
extraction artifacts, not content differences:

- `RI-PY` — the pattern `RI-\s*PY` returns **2 in both engines**. The `\b` word-boundary
  assertion behaved differently around the surrounding table whitespace. Content identical.
- `REQUIRED` — pdfminer returns 0 for uppercase but **15** case-insensitively; pypdf returns 14
  uppercase and 15 case-insensitively. The document renders these in small-caps, which the two
  engines case-normalise differently. Content equivalent.

No document content differs between engines. `ARI` is 0 under both engines for all six.

### 2.2 Substring false positives (rule R5)

As in RD-1-PDF, a naive case-insensitive search for `ari` returns hits in all six documents.
Every one is a substring of `Invariant` / `Invariants` (and, in the Polish text,
`scen`**`ari`**`usze`, `granicznych` forms). **None is the token `ARI`.** Reported because the
naive figure would support the opposite conclusion.

---

## 3. Constitution (special attention A)

```
Document ID: AURA-CON-001
Title: AURA Constitution
Version: 1.0
Status: FROZEN (po zatwierdzeniu)          ["FROZEN (after approval)"]
Classification: Canonical Governance Document
Owner: Chief Architect
```

**ARI: not defined, not constrained, not delegated — the token does not appear.**

Content of record:

**Article I — Identity**, page 2:
> Aura jest protokołem. Nie jest aplikacją, frameworkiem ani modelem AI. **Każda implementacja
> Aura jest jedynie referencyjną realizacją specyfikacji.**

*(Aura is a protocol. It is not an application, framework or AI model. Every Aura implementation
is merely a reference realization of the specification.)*

**Article IV — Constitutional Principles**, page 4 — ten principles, beginning:
> Specification First. Determinism by Design. Conformance Before Features. Evidence Before
> Trust. Human Accountability. Fail Closed by Default. Immutable Evidence. Explicit over
> Implicit. Version Everything. Documentation is Part of the Product.

**Article V — Canonical Hierarchy**, page 5:
> ```
> AURA Constitution
>         ↓
> Aura Protocol Specification
>         ↓
> Protocol Invariants
>         ↓
> ADR / ARR / RFC
>         ↓
> Aura Development Playbook
>         ↓
> Repository Documentation
>         ↓
> Implementation
> ```
> Dokument wyższego poziomu ma pierwszeństwo przed dokumentem niższego poziomu.

*(A higher-level document takes precedence over a lower-level document.)*

Article V is analysed in `02_HIGHEST_AUTHORITY_ASSESSMENT.md` §2 — it bears directly on a
finding RD-1 left open.

---

## 4. APS-100 Protocol Invariants (special attention B)

```
Document ID: APS-100 · Version: 1.0-DRAFT · Status: DRAFT
Classification: Normative Specification · Authority: APS-001
```

Complete catalogue, INV-001 … INV-015, transcribed from pages 3–9:

| ID | Title | Requirement (MUST) — translated |
|---|---|---|
| INV-001 | Deterministic Evaluation | identical input MUST lead to identical result |
| INV-002 | Bit-Perfect Replay | replay MUST reproduce an identical result **on every conformant implementation** |
| INV-003 | Canonical Serialization | every protocol object MUST have an unambiguous serialization |
| INV-004 | Immutable Evidence | Evidence MUST NOT be modified once generated |
| INV-005 | Evidence Traceability | every Evidence MUST indicate the requirement it documents |
| INV-006 | Platform Independence | MUST maintain conformance regardless of hardware/system platform |
| INV-007 | Zero Float Runtime | protocol logic MUST NOT use floating-point arithmetic at runtime where it would violate specified determinism |
| INV-008 | Fail Closed | on error, MUST terminate in a safe state |
| INV-009 | Version Consistency | Evidence, Protocol and Data Model MUST reference compatible versions |
| INV-010 | Conformance Completeness | every Invariant MUST have a corresponding conformance test |
| INV-011 | Cryptographic Integrity | Evidence integrity MUST be cryptographically verifiable |
| INV-012 | Auditability | every protocol execution MUST leave an audit trail per APS |
| INV-013 | Policy Determinism | same policy version + identical input MUST yield an identical decision |
| INV-014 | Reference Compatibility | implementation MUST pass all applicable Reference Fixtures |
| INV-015 | Canonical Identity | every protocol artifact MUST have an identifier per APS-000 |

### Assessment against the question asked

| Property | Constrained by an invariant? | Which |
|---|---|---|
| **ARI** (as such) | **NO** — no invariant mentions it | — |
| **Determinism** | **YES** | INV-001 (same-implementation), INV-002 (cross-implementation), INV-013 (policy) |
| **Platform independence** | **YES** | INV-006 |
| **Bounds** | **NO** | — |
| **Division semantics** | **NO** | — |
| **Rounding semantics** | **NO** | — |
| **Drift** | **NO** | — |
| **Malformed input** | **INDIRECT ONLY** | INV-008 requires safe termination *on error*, but no artifact defines what constitutes an error for an evaluation input |
| **Float arithmetic** | **YES, prohibitively** | INV-007 forbids float at runtime — but specifies nothing about *integer* division or rounding behaviour |

**Recorded without resolution:** INV-002 requires bit-perfect replay *on every conformant
implementation*, and INV-006 requires platform independence. Conformance is defined by INV-014
as passing all applicable Reference Fixtures. RD-1-PDF established that APS-500 defines the
fixture schema and supplies **no instance** — no ARI fixture exists. INV-002 and INV-006 are
therefore stated but, for ARI, have no instrument through which they could be evaluated.

This is an observation about enforceability. **No division or rounding semantics are selected or
recommended, and ADR-005 is not resolved.**

---

## 5. APS-200 Canonical Data Model (special attention C)

```
Document ID: APS-200 · Version: 1.0-DRAFT · Status: DRAFT
Classification: Normative Specification · Authority: APS-001 · APS-100
```

**Mathematical semantics relevant to ARI: ABSENT — not merely non-normative, but not present.**

Term search across the document: `int32` 0 · `integer` 0 · `numeric` 0 · `precision` 0 ·
`rounding` 0 · `division` 0 · arithmetic terms 0.

The document defines eight canonical entities by **name and description only**:

> ENT-001 Protocol Header · ENT-002 Evaluation Request · **ENT-003 Evaluation Result** ·
> ENT-004 Policy Reference · ENT-005 Evidence · ENT-006 Attestation · ENT-007 Audit Record ·
> ENT-008 Implementation Metadata

and a Common Object Contract (`object_id`, `object_type`, `protocol_version`, `schema_version`,
`created_at`, `integrity_hash`).

Decisively, §5 *Entity Definitions* states the per-entity detail is **future work**:

> Każda encja **będzie opisana** według jednolitego szablonu: Identifier · Purpose · Required
> Fields · Optional Fields · Constraints · Related Invariants · Related Evidence ·
> Serialization Rules

*(Each entity **will be** described according to a uniform template.)*

`ENT-003 Evaluation Result` — the entity that would carry an ARI field, its type, and its
constraints — is **named but undefined**. The template exists; the instance does not.

---

## 6. APS-950 Reference Implementation Requirements (special attention D)

```
Document ID: APS-950 · Version: 1.0-DRAFT · Status: DRAFT
Classification: Normative Implementation Specification
Authority: APS-001 · APS-100 · APS-200 · APS-300 · APS-400 · APS-500 · APS-900
```

**RI-PY contains no ARI definition. APS-950 is implementation/reference material only.**

§3 requires seven components of any reference implementation — `RI-001 Protocol Engine`,
`RI-002 Validation Layer`, `RI-003 Evidence Generator`, `RI-004 Conformance Runner`, … — each
marked `REQUIRED`.

§11 *Supported Reference Implementations* (pages 9–10) is a **registry table**:

| ID | Implementation | Role |
|---|---|---|
| RI-PY | `aura-poc-a-core` | Referencyjna implementacja w Pythonie *(reference implementation in Python)* |
| RI-RS | `aura-guard` | Referencyjna implementacja w Rust |
| RI-TEST | Reference Fixtures Runner | reference test-environment implementation |

The two `RI-PY` occurrences are the same table row, repeated across the page 9/10 boundary — a
table-header repeat artifact of PDF export, not two statements.

`RI-PY` here is an **identifier mapping an ID to a repository and a role**. It carries no
formula, no domain, no bounds, no drift, no arithmetic semantics. §2 requires a reference
implementation to *"implement all mandatory APS requirements"* and *"pass the full Conformance
test set"* — obligations that, for ARI, point at requirements and tests that this audit and
RD-1-PDF have established do not exist.

---

## 7. APS-000 and APS-300

| Document | Status | ARI | Relevant content |
|---|---|---|---|
| APS-000 Foundation & Terminology | 1.0-DRAFT / DRAFT | **0** | terminology and identifier scheme; ARI is not a defined term |
| APS-300 Evidence Model | 1.0-DRAFT / DRAFT | **0** | Evidence Pack structure; no ARI field, no numeric semantics |

**APS-000 is the corpus's terminology document and it does not define ARI.**
