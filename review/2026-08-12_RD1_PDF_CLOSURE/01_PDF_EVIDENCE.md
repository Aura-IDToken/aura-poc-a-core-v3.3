# RD-1-PDF — 01 PDF EVIDENCE

---

## 1. Extraction outcome

| ID | Pages | pypdf chars | pdfminer chars | Encrypted | Image XObjects | Extraction |
|---|---|---|---|---|---|---|
| APS-400 | 13 | 4 149 | 3 705 | no | **0** | ✅ SUCCESS |
| APS-500 | 12 | 2 901 | 2 531 | no | **0** | ✅ SUCCESS |
| APS-900 | 12 | 3 195 | 2 782 | no | **0** | ✅ SUCCESS |

**All three PDFs are text-extractable.** The RD-1 UNKNOWN is closable.

Character-count differences between engines reflect whitespace and line-break handling, not
content divergence: both engines return identical results on every strict token search (§3).

### 1.1 Page-level coverage

| ID | Pages with a text layer | Pages with none | Image XObjects on empty pages |
|---|---|---|---|
| APS-400 | 1–12 (204–424 chars each) | 13 | **0** |
| APS-500 | 1–8 (200–441 chars each) | 9, 10, 11, 12 | **0** |
| APS-900 | 1–10 (208–417 chars each) | 11, 12 | **0** |

Every page lacking text also contains **zero image XObjects**. These are genuinely blank
trailing pages, not scans. **No OCR is required, and none was performed**: there is no raster
content in which text could be hiding.

The `Impossible to decode XFormObject /FXXn` warnings emitted by `pypdf` concern **form**
XObjects (vector/layout constructs), not images. `pdfminer.six`, which processes form XObjects
by a different code path, returned the same token results — the independent control for this
warning.

---

## 2. Document metadata (verbatim, page 1 of each)

### APS-400
```
Document ID: APS-400
Title: Conformance Test Matrix
Version: 1.0-DRAFT
Status: DRAFT
Classification: Normative Specification
Authority: APS-001 · APS-100 · APS-200 · APS-300
```

### APS-500
```
Document ID: APS-500
Title: Reference Fixtures
Version: 1.0-DRAFT
Status: DRAFT
Classification: Normative Test Specification
Authority: APS-100 · APS-200 · APS-300 · APS-400
```

### APS-900
```
Document ID: APS-900
Title: Compliance Mapping
Version: 1.0-DRAFT
Status: DRAFT
Classification: Normative Governance
Authority: APS-001 · APS-100 · APS-200 · APS-300
```

All three self-classify as **Normative** and all three carry **Status: DRAFT**.

---

## 3. Target-term search — the decisive result

Strict, case-**sensitive**, word-**boundary** matching, both engines:

| Term | APS-400 | APS-500 | APS-900 |
|---|---|---|---|
| `ARI` (standalone token) | **0** | **0** | **0** |
| `PoCA` | **0** | **0** | **0** |
| `RI-PY` | **0** | **0** | **0** |
| `SI` / `SA` (standalone) | **0** | **0** | **0** |
| "Agent Reliability Index" | **0** | **0** | **0** |
| "Aura Reliability Index" | **0** | **0** | **0** |
| "reliability index" (any case) | **0** | **0** | **0** |
| rounding · division · drift · bounds | **0** | **0** | **0** |
| formula · equation | **0** | **0** | **0** |

Identical under `pypdf` and `pdfminer.six`.

### 3.1 What the apparent "ARI hits" actually were

A naive case-insensitive substring search returns 13 / 6 / 4 hits. Every one is a substring
inside another word:

| Document | Actual matched tokens |
|---|---|
| APS-400 | `Invariant` × 13 |
| APS-500 | `Invariant` × 3, `Invariants` × 1, `scenariusze` × 2 (Polish) |
| APS-900 | `Invariant` × 3, `Invariants` × 1 |

`Inv`**`ari`**`ant` and scen**`ari`**usze. **Not one is the token `ARI`.**

This is precisely the failure mode rule **R5** was written to catch, and it is the same class
of error as RD-1's original raw-byte match. Recorded plainly because the naive number would
have supported the opposite conclusion.

### 3.2 A false positive found and corrected during this audit

An intermediate search reported `0.3` ×2 and `0.7` ×1 in APS-400 — the ARI weights, which would
have been significant. The pattern was unescaped: `.` matched any character. Re-run with
literal matching, **APS-400 contains no `0.3`, no `0.7`, no `100000`, and no `10^5`.** No
formula-bearing numeral appears in any of the three documents.

---

## 4. What the three documents actually contain

### APS-400 — Conformance Test Matrix

Defines eight test categories (Functional, Determinism, Replay, Serialization, Evidence,
Integrity, Security, Compatibility), a test-definition template (Purpose, Related APS, Related
Invariant(s), Preconditions, Test Procedure, Expected Result, Evidence Required, PASS/FAIL
Criteria), and a canonical matrix of ten tests:

| Test | Related Invariant | Stated objective (translated) |
|---|---|---|
| CONF-001 Deterministic Evaluation | INV-001 | identical input yields identical result |
| CONF-002 Replay Verification | INV-002 | reproduce execution from Evidence Pack |
| CONF-003 Canonical Serialization | INV-003 | serialization conforms to APS-200 |
| CONF-004 Evidence Integrity | INV-004 | integrity of the Evidence object |
| CONF-005 Traceability | INV-005 | Requirement → Invariant → Test → Evidence path |
| CONF-006 Platform Independence | INV-006 | compare results across platforms |
| CONF-007 Fail Closed | INV-008 | safe termination on error |
| CONF-008 Version Compatibility | INV-009 | APS / data-model / Evidence version agreement |
| CONF-009 Evidence Completeness | — | (page 7+) |
| CONF-010 Cryptographic Verification | — | (page 7+) |

**No test concerns ARI.** Note the shape of CONF-001: it requires that identical inputs produce
identical outputs — **reproducibility, not correctness**. It does not state what the output must
*be*. Nothing in the matrix would fail an implementation that computed ARI differently, provided
it did so deterministically.

Verbatim, page 1:

> APS-400 definiuje oficjalny zestaw testów zgodności (Conformance Tests), które każda
> implementacja Aura MUST przejść, aby zostać uznana za zgodną z protokołem.

*(APS-400 defines the official set of Conformance Tests which every Aura implementation MUST
pass to be considered protocol-conformant.)*

### APS-500 — Reference Fixtures

Defines a fixture **schema** — Fixture ID, Version, Description, Input Data, Expected Output,
Expected Evidence, Related Invariants, Related Conformance Tests — and six categories
(`FIX-CORE`, `FIX-BOUNDARY`, `FIX-ERROR`, `FIX-REPLAY`, `FIX-EVIDENCE`, `FIX-COMPAT`).

The sole canonical example is a placeholder:

> **FIX-001**
> Name: Basic Evaluation
> Input: Referencyjny zestaw danych wejściowych.
> Expected Result: Wynik zgodny z APS-200.

*(Input: reference input dataset. Expected Result: result conforming to APS-200.)*

**No concrete fixture data exists.** No input vector, no expected output value, no ARI. The
document specifies the container for fixtures; it contains none. This corroborates RI-PY's
self-reported `RI-005 Fixture Loader ❌ MISSING` and `INV-014 ❌`.

### APS-900 — Compliance Mapping

Governance-tier mapping document. Contains no ARI token, no formula, no numeric bound.

---

## 5. Occurrence record

The task requires, for every relevant occurrence: PDF, page, section, exact text, status, and
classification as normative / descriptive / implementation-derived / indeterminate.

**There are no relevant occurrences to record.** Across 37 pages and three documents, the terms
`ARI`, `Agent Reliability Index`, `Aura Reliability Index`, `reliability index`, `PoCA`,
`RI-PY`, and every formula, rounding, division, bounds, and drift term are **absent**.

The occurrence table is therefore empty — not because extraction failed, but because extraction
succeeded and found nothing.
