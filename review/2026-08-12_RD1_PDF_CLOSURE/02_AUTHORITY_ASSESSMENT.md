# RD-1-PDF — 02 AUTHORITY ASSESSMENT

The task requires assessing whether any of the three PDFs **establishes an authoritative ARI
definition**, without inferring authority from placement.

---

## 1. Assessment per document

| | APS-400 | APS-500 | APS-900 |
|---|---|---|---|
| Self-declared Classification | Normative Specification | Normative Test Specification | Normative Governance |
| Version | 1.0-DRAFT | 1.0-DRAFT | 1.0-DRAFT |
| Status | **DRAFT** | **DRAFT** | **DRAFT** |
| Contains a standalone `ARI` token | **No** | **No** | **No** |
| Contains an ARI formula | **No** | **No** | **No** |
| Contains ARI bounds / rounding / division / drift | **No** | **No** | **No** |
| Contains an ARI fixture or expected value | **No** | **No** (framework only, placeholder example) | **No** |
| References RI-PY | **No** | **No** | **No** |
| **Establishes an authoritative ARI definition** | **NO** | **NO** | **NO** |

## 2. Why the assessment ends here

The authority question is normally the hard part: a document may carry content without carrying
authority (RD-1's `mathematical_foundation.md`), or carry authority without content (RD-1's
Constitution and APS-100). Rules **R3** and **R6** exist to keep those apart.

**Neither rule is reached for these three documents.** They contain no ARI content of any kind.
A document that says nothing about ARI cannot define ARI, whatever its authority. The assessment
terminates on the content test and never arrives at the authority test.

This is worth stating explicitly so the conclusion is not mistaken for a judgement *against*
these documents' authority. Their authority is **untested here** and **irrelevant here**.

## 3. What their `Classification: Normative` does and does not mean

All three self-classify as Normative. Applying rule **R3** — placement and labels do not confer
definitional force — this is recorded, not credited:

- The label is *self-declared* on the cover page; no external artifact in the corpus ratifies it.
- All three carry `Status: DRAFT` and `Version: 1.0-DRAFT`, which is in tension with a
  settled normative classification.
- No adjudication of that tension is offered here. **It does not matter for this audit**: the
  documents are silent on ARI either way.

**DECISION NOT REQUIRED for RD-1 purposes.** Recorded only so the Authority is not later
surprised that three DRAFT documents carry a Normative classification.

## 4. The finding that cuts the other way

The three documents are silent on ARI — but two of them are precisely the artifacts that
*would* carry a binding ARI requirement if one existed:

**APS-400 is the Conformance Test Matrix.** Its ten canonical tests (CONF-001…CONF-010) each
bind to a Protocol Invariant. None concerns ARI. Its determinism test, CONF-001, requires that
identical inputs yield identical outputs — **reproducibility, not correctness**. An
implementation computing ARI by a different formula, or with truncating rather than flooring
division, would **pass CONF-001** provided it were deterministic.

**APS-500 is the Reference Fixtures specification.** It defines the fixture schema — including
an `Expected Output` field — and six fixture categories, then supplies a single placeholder
example whose expected result is *"Wynik zgodny z APS-200"* ("result conforming to APS-200").
**No concrete fixture, no expected value, no ARI.**

So the conformance layer does not merely omit ARI by oversight of placement: the machinery that
would pin an ARI value exists as a **schema with no instances**. This corroborates, from the
specification side, RI-PY's own report of `RI-004 Conformance Runner ❌ MISSING`,
`RI-005 Fixture Loader ❌ MISSING`, `INV-010 ❌`, `INV-014 ❌`.

## 5. Conclusion

**No PDF in scope establishes an authoritative ARI definition.**

None contains a standalone `ARI` token, a formula, a bound, a rounding or division rule, a drift
definition, a fixture value, or a reference to RI-PY. The question of their authority is not
reached.
