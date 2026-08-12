# RD-1-PDF — 00 SCOPE

**Date:** 2026-08-12
**Purpose:** Close the single evidence gap left open by RD-1 — three APS PDFs classified UNKNOWN.
**Status:** EVIDENCE ONLY
**normative_effect:** NONE

---

## 1. What RD-1 left open

`06_DECISION_BRIEF.md` §6 recorded:

> **PDF snapshots — UNKNOWN.** `APS-400`, `APS-500`, `APS-900` PDFs each yield one raw `ARI`
> byte-match inside `FlateDecode` streams, with no extractable text layer. Per rule R4 these
> are not treated as evidence. […] If the Authority requires them adjudicated, that needs PDF
> text-extraction tooling this session lacks.

This package closes exactly that gap. Nothing else.

## 2. Scope

**In scope — the three PDFs only:**

| ID | File | Bytes | SHA-256 (first 16) |
|---|---|---|---|
| APS-400 | `APS-400 — Conformance Test Matrix_260723_193617.pdf` | 1 524 289 | `b3e1323fea52bee4` |
| APS-500 | `APS-500 Reference Fixtures_260723_194023.pdf` | 1 495 756 | `973ae85d068d4408` |
| APS-900 | `APS-900 — Compliance Mapping_260723_194128.pdf` | 1 519 951 | `15dfafc7d3d6382c` |

Repository: `AuraIDToken/aura-specification` @ `62d2d6b`.

**Out of scope:** everything else. No production code, SPEC-002, ADR, fixture, or test was
touched. No ARI semantics, formula, rounding mode, or division mode is selected or recommended.
No ADR created. No PR. The existing RD-1 package was not modified.

## 3. Method

1. **Tooling.** No PDF utility was present (`pdftotext`, `pdftoppm`, `mutool`, `gs`, `qpdf`,
   `tesseract` — all absent; no Python PDF library installed). `pypdf` 6.15.0 and
   `pdfminer.six` were installed into the session environment. A broken system `cryptography`
   (missing `_cffi_backend`) blocked `pypdf` until `cffi` was upgraded. These are session-local
   environment changes; no repository file was affected.
2. **Dual independent extraction.** Every PDF was extracted twice, with two unrelated engines
   (`pypdf` and `pdfminer.six`), and the results compared. Agreement between engines is treated
   as the extraction-reliability control.
3. **Page-level coverage census.** Per-page character counts plus a census of image XObjects
   (`/Subtype == /Image`), to establish whether any page carries content outside the text layer
   that would require OCR.
4. **Strict token search.** Case-**sensitive**, word-**boundary** matching for `ARI`, `PoCA`,
   `SI`, `SA`, `RI-PY`; case-insensitive phrase matching for `Agent Reliability Index`,
   `Aura Reliability Index`, `reliability index`; literal matching for formula-bearing terms.
5. **Metadata capture.** Document ID, Title, Version, Status, Classification, Authority from
   each cover page.

## 4. Evidential rules carried forward from RD-1

- **R1** — implementation behaviour is not evidence of normativity.
- **R2** — a reference to RI-PY is not authority unless the corpus grants it.
- **R3** — `FROZEN` / placement is not a synonym for `normative`.
- **R4** — unextractable content yields UNKNOWN, never a definition.

Added for this package, per the task's explicit instruction:

- **R5** — a **numerical or substring occurrence of "ARI" is not sufficient**. Only a
  standalone, case-correct `ARI` token counts as an occurrence.
- **R6** — a formula is not automatically normative; authority is not inferred from document
  placement alone.

**R5 proved decisive** (see `01_PDF_EVIDENCE.md` §3).

## 5. Two corrections to RD-1's characterisation

Both concern *how the gap was described*, not the RD-1 verdict.

1. **"No extractable text layer" was wrong.** All three PDFs are born-digital and carry a
   complete, coherent text layer. RD-1 could not read them because the session had no PDF
   tooling — an environment limitation, correctly handled as UNKNOWN at the time, but the
   underlying claim about the files was inaccurate.
2. **The "one raw `ARI` byte-match in FlateDecode streams" was meaningless.** That figure came
   from matching the byte sequence `ARI` against *compressed* stream data, where such a match
   carries no information. Decompressed, the documents contain **zero** standalone `ARI`
   tokens. The byte-match was noise, and reporting it as a partial signal overstated it.

## 6. Observation — out of scope

Six further PDFs exist in the same repository and were **not** examined, this task being scoped
to three: `AURA Constitution`, `APS-000 Foundation & Terminology`, `APS-100 Protocol
Invariants`, `APS-200 Canonical Data Model`, `APS-300 Evidence Model`, `APS-950 Reference
Implementation Requirements`. RD-1 assessed their **markdown** counterparts (all `0` ARI).

**OBSERVATION — OUT OF SCOPE:** the tooling to adjudicate those six now exists in this session.
Whether the PDF snapshots of the Constitution and APS-100 need adjudicating alongside their
markdown counterparts is a question for the Authority. No such examination was performed here.
