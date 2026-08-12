# RD-1-PDF — 04 DECISION BRIEF

**For:** Human Architectural Authority / Protocol Custodian
**Prepared by:** engineering evidence analyst — not the Architectural Authority
**normative_effect:** NONE

---

## 1. Verdict

# A. UNKNOWN CLOSED — NO ARI NORMATIVE DEFINITION FOUND

**The original RD-1 verdict is explicitly STRENGTHENED.**

RD-1 concluded `NO NORMATIVE DEFINITION FOUND` while three documents were unreadable. Those
three are now read. They contain no ARI content whatsoever. The verdict that was reached on
incomplete evidence now stands on complete evidence for these artifacts.

## 2. What was done

Three PDFs, 37 pages, extracted with **two independent engines** (`pypdf` 6.15.0,
`pdfminer.six`) after installing PDF tooling the session previously lacked.

| ID | Pages | Extraction | Standalone `ARI` tokens |
|---|---|---|---|
| APS-400 Conformance Test Matrix | 13 | ✅ both engines | **0** |
| APS-500 Reference Fixtures | 12 | ✅ both engines | **0** |
| APS-900 Compliance Mapping | 12 | ✅ both engines | **0** |

Also zero, in all three: `PoCA`, `RI-PY`, `SI`/`SA` as tokens, "Agent Reliability Index",
"Aura Reliability Index", "reliability index", and every rounding, division, drift, bounds,
formula and equation term. Both engines agree exactly.

**No OCR was needed.** Pages without a text layer are blank trailing pages carrying **zero image
XObjects** — these are born-digital documents, not scans, so there is no raster content in which
text could hide.

## 3. The finding that could have reversed the verdict

A naive case-insensitive search returns 13 / 6 / 4 "ARI hits". **Every one is a substring**:
`Inv`**`ari`**`ant`, `Invariants`, and the Polish `scen`**`ari`**`usze`. Not one is the token
`ARI`.

Reported plainly because the naive number supports the opposite conclusion, and because it is
the same error class as RD-1's original raw-byte match. Rule **R5** — *a numerical occurrence of
"ARI" is not sufficient* — is what caught it.

A second false positive was found and corrected mid-audit: an unescaped regex reported `0.3` and
`0.7` in APS-400 (the ARI weights). With literal matching, **APS-400 contains no `0.3`, no
`0.7`, no `100000`, no `10^5`** — no formula-bearing numeral appears in any of the three.

## 4. Why authority was never the question

All three self-classify as **Normative** (`Normative Specification`, `Normative Test
Specification`, `Normative Governance`) and all three carry **`Status: DRAFT`,
`Version: 1.0-DRAFT`**.

That tension is recorded but **not adjudicated, because it does not matter**: a document silent
on ARI cannot define ARI regardless of its authority. The assessment terminates on the content
test and never reaches the authority test. Rules R3 and R6 are not engaged.

## 5. The corroborating finding

New, and only obtainable by reading the PDFs:

**The conformance layer is structurally incapable of pinning an ARI value.**

- **APS-400** defines ten canonical tests (CONF-001…CONF-010), each bound to a Protocol
  Invariant. None concerns ARI. CONF-001 *Deterministic Evaluation* requires that identical
  inputs yield identical outputs — **reproducibility, not correctness**. An implementation using
  truncation toward zero instead of floor division (RD-1 conflict **C-3**, producing
  `30000/100000` rather than the reference `29999/100001`) would **pass CONF-001**, being
  internally deterministic.
- **APS-500** defines the fixture schema — including an `Expected Output` field — and six
  categories, then supplies one placeholder whose expected result is *"Wynik zgodny z APS-200"*.
  **The container for fixtures exists; it holds no instances.**

This corroborates from the specification side what RI-PY reports from the implementation side:
`RI-004 Conformance Runner ❌ MISSING`, `RI-005 Fixture Loader ❌ MISSING`, `INV-010 ❌`,
`INV-014 ❌`.

**No remedy is proposed.** Recorded as evidence for architectural decision.

## 6. Corrections to RD-1's characterisation

Two, neither altering the verdict:

1. **"No extractable text layer" was inaccurate.** The files are fully extractable; the session
   lacked PDF tooling. UNKNOWN was the right classification at the time; the stated reason was
   wrong.
2. **The "one raw `ARI` byte-match in FlateDecode streams" was noise.** It came from matching
   bytes in *compressed* data. It should not have been reported as a partial signal; decompressed,
   the count is zero.

The existing RD-1 package was **not modified**, per instruction.

## 7. Residual evidence gaps

| Gap | Status |
|---|---|
| The three scoped PDFs | **CLOSED** |
| Six further PDFs in the same repository — `AURA Constitution`, `APS-000`, `APS-100 Protocol Invariants`, `APS-200`, `APS-300`, `APS-950` | **NOT EXAMINED — out of scope.** RD-1 assessed their markdown counterparts (all 0 ARI). The tooling to adjudicate them now exists in this session. |

**OBSERVATION — OUT OF SCOPE.** The Constitution and APS-100 PDFs are the two highest-authority
artifacts in the corpus. RD-1's finding that both are silent on ARI rests on their markdown
forms alone. For the three documents examined here, markdown and PDF **agreed exactly**, which
is mild evidence that the two representations are consistent generally — but it is not proof for
the other six. Whether that residual matters is the Authority's call; no examination was
performed and none is recommended here.

## 8. What is NOT claimed

- No ARI formula, rounding mode, division mode, dimension, or bound is selected or recommended.
- No conflict from RD-1 is resolved; none is introduced.
- No claim that the three documents lack authority — only that they lack ARI content.
- No production code, SPEC-002, ADR, fixture, or test modified. No ADR created. No PR.

---

## 9. Statement required by the task

**The original RD-1 verdict — `NO NORMATIVE DEFINITION FOUND` — is STRENGTHENED.**

The three documents that would most plausibly have carried a binding ARI requirement — the
Conformance Test Matrix, the Reference Fixtures specification, and the Compliance Mapping — are
now confirmed silent on ARI in both their markdown and PDF forms. The last readable place a
normative ARI definition could have been hiding within RD-1's scope has been checked, and it is
empty.
