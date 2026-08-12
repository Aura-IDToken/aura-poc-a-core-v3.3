# RD-1-FINAL-PDF — 00 SCOPE

**Date:** 2026-08-12
**Purpose:** Close the residual PDF gap for the six highest-authority artifacts.
**Status:** EVIDENCE ONLY
**normative_effect:** NONE

---

## 1. What this closes

`RD-1-PDF/04_DECISION_BRIEF.md` §7 recorded six PDFs as *"NOT EXAMINED — out of scope"*, noting
that RD-1's finding for them rested on their markdown forms alone, and that the Constitution and
APS-100 are the two highest-authority artifacts in the corpus. This package examines exactly
those six. Nothing else.

RD-1 and RD-1-PDF conclusions are **not reopened**. Neither package is modified.

## 2. Artifacts in scope

Repository `AuraIDToken/aura-specification` @ `62d2d6b`.

| # | ID | File | Pages | SHA-256 (16) |
|---|---|---|---|---|
| 1 | Constitution | `AURA Constitution_260723_190157.pdf` | 14 | `10cb4d8a3acce8dd` |
| 2 | APS-000 | `AURA Protocol Specification APS-000 — Foundation &_260723_191759.pdf` | 19 | `d781137761f4520b` |
| 3 | APS-100 | `APS-100 — Protocol Invariants_260723_192315.pdf` | 15 | `469d9e3ce9977ccb` |
| 4 | APS-200 | `APS-200 — Canonical Data Model_260723_192852.pdf` | 11 | `edafec28ae3b5568` |
| 5 | APS-300 | `APS-300 — Evidence Model_260723_193234.pdf` | 13 | `fec2a10802ae0a35` |
| 6 | APS-950 | `APS-950 — Reference Implementation Requirements_260723_194507.pdf` | 14 | `3f75be8b139b74fb` |

**86 pages total.**

## 3. Method

1. **Dual independent extraction** — every PDF extracted with `pypdf` 6.15.0 and
   `pdfminer.six`, results compared. Divergence between engines is investigated, not averaged.
2. **Raster census** — per-page character counts plus a census of `/Subtype == /Image` XObjects,
   to establish whether any page carries content requiring OCR.
3. **Literal token search, not substring** — case-**sensitive**, word-**boundary** matching for
   `ARI`, `PoCA`, `RI-PY`, `MUST`, `SHALL`, `REQUIRED`; case-insensitive literal phrase matching
   for `Agent Reliability Index`, `Aura Reliability Index`, `reliability index`, `drift`,
   `rounding`, `division`, `bounds`, `formula`.
4. **Markdown comparison** — each PDF compared against its markdown counterpart, specifically
   testing for any target term present in the PDF but **absent** from the markdown.
5. **Manual reading** — the invariant catalogue, the Constitution's articles, the APS-200 entity
   model and the APS-950 implementation registry were read in full, not merely searched.

## 4. Rules carried forward and applied

- **R1** implementation behaviour is not evidence of normativity.
- **R2** a reference to RI-PY is not authority unless the corpus grants it.
- **R3** `FROZEN`, title, placement and self-declared classification are **not** synonyms for
  `normative`.
- **R4** unextractable content yields UNKNOWN, never a definition.
- **R5** a substring occurrence of "ARI" is not an occurrence — only a standalone,
  case-correct token counts.
- **R6** the existence of a formula is not proof of normativity.

Per the task, **R3** and **R6** are load-bearing here: several documents in scope self-classify
as `Normative Specification` and one is `FROZEN`. Neither fact is credited as authority.

## 5. Out of scope

No ARI semantics selected. ADR-005 **not resolved**. No rounding mode or division semantics
recommended. No source document modified, no fixture created, no production code changed, no
ADR, no specification change, no PR.

## 6. Extraction reliability control

`pypdf` emitted `Impossible to decode XFormObject /FXXn` warnings on several files. These
concern **form** XObjects (layout constructs), not images. `pdfminer.six` processes form
XObjects through an unrelated code path and returned identical token results on every document,
which is the control for that warning class. The one engine disagreement observed (APS-950) was
investigated to root cause and resolved as an extraction artifact — see
`01_PDF_EVIDENCE.md` §2.1.
