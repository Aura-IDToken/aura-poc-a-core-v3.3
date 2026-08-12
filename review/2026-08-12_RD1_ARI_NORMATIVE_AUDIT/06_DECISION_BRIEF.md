# RD-1 — 06 DECISION BRIEF

**For:** Human Architectural Authority / Protocol Custodian
**Prepared by:** engineering evidence analyst — not the Architectural Authority
**normative_effect:** NONE

---

## 1. Verdict

# NO NORMATIVE DEFINITION FOUND

AURA does not currently contain an authoritative normative definition of ARI.

## 2. The three facts that decide it

**(a) Every artifact carrying normative authority is silent on ARI.**

| Tier | Artifact | ARI occurrences |
|---|---|---|
| 1 Constitutional | `CONSTITUTIONAL_DECREE.md` | **0** |
| 2 Specification | `APS-000`, `APS-200`, `APS-300`, `APS-950` | **0** |
| 3 Invariants | `APS-100_PROTOCOL_INVARIANTS.md` | **0** |
| 5 Conformance | `APS-400_CONFORMANCE_TEST_MATRIX.md` | **0** |
| 2 Specification | `SPEC-002` (0.3-DRAFT) | **0** |
| — Fixtures | `APS-500_REFERENCE_FIXTURES.md` | **0** |

Across 95 specification files, ARI appears in exactly **two** readable places: a glossary entry
and an uncertified reference-implementation status report.

**(b) The single highest-authority ARI text defines it by pointing at the implementation.**

> **ARI** (Aura Reliability Index) — A deterministic measurement value computed **by RI-PY**
> using integer arithmetic. — `aura-specification/glossary/GLOSSARY.md`

RI-PY is `NOT CERTIFIED` and contains no formula. The definition therefore terminates in
`core/evaluator.py`. Under rule R1, that the implementation produces a value is not evidence
that the value is normative — so the chain ends without ever reaching a norm. This is the
circularity **C-1**.

**(c) The only formula-bearing documents sit outside the authority ladder and disagree with the
implementation.**

`docs/mathematical_foundation.md` states the formula and is marked `FROZEN` — but carries no
`MUST`/`SHALL`, never uses the word `normative`, has no tier in `CLAUDE.md`'s ladder, and is
classed by ADR-006 §3.2 as `Documentation` under NB-021 CASE A, *"documentation-only
correction… clarify existing behavior"*. It states `RAW_ARI ∈ [0,100000]`; the implementation
returned **7,030,000** under test. `ADR-005` (APPROVED, FROZEN) states integer division is
*"truncation toward zero"*; CPython floors — the discrepancy that produces OBS-5's
`29999/100001` instead of `30000/100000`.

## 3. Coverage

**0 of 11** definitional dimensions have normative coverage. **4 are total gaps**, undefined in
every artifact of both corpora:

| Total gap | Consequence |
|---|---|
| **D7 rounding** | no rounding rule exists anywhere |
| **D8 malformed input** | `zip` truncation yields a perfect score on mismatched dimensions (CORE-P0-001) |
| **D9 drift** | `core/evaluator.py` is the sole determinant of a value the protocol emits and hashes |
| **D11 serialization/hash** | no ARI-specific canonicalization rule |

## 4. Provenance chain

**1 of 7 edges is sound** — `IMPLEMENTATION → CHARACTERIZATION TEST`, delivered by U-1 and
enforced by CHECK 10 at `bdaa331`. It connects the implementation to a harness that explicitly
disclaims normative force. Edge [5] `OUTPUT CONTRACT → IMPLEMENTATION` is **INVERTED**: the
contract is populated by the implementation rather than constraining it.

## 5. Why not one of the other three verdicts

| Verdict | Why rejected |
|---|---|
| NORMATIVE DEFINITION ESTABLISHED | No artifact at levels 1–5 defines any of the 11 dimensions. |
| NORMATIVE DEFINITION **PARTIALLY** ESTABLISHED | Tempting, because a formula exists in writing. Rejected: partial establishment requires *some* dimension to be normatively covered, and none is. The formula's problem is not incompleteness but **absence of authority** — it sits at no tier, is classed as descriptive documentation by the corpus itself, and is contradicted by the artifact it describes. Per rule R3, `FROZEN` does not supply the missing grant. |
| CONFLICTING NORMATIVE DEFINITIONS | Requires ≥2 *normative* definitions in conflict. The six recorded conflicts are documentation-vs-implementation or documentation-vs-documentation. There are not two competing norms; there are zero. |

## 6. Evidence sufficiency

Sufficient for the verdict. Two limitations, neither affecting it:

1. **PDF snapshots — UNKNOWN.** `APS-400`, `APS-500`, `APS-900` PDFs each yield one raw `ARI`
   byte-match inside `FlateDecode` streams, with no extractable text layer. Per rule R4 these
   are not treated as evidence. Their markdown counterparts contain **0** ARI. If the Authority
   requires them adjudicated, that needs PDF text-extraction tooling this session lacks.
2. **`aura-guard-v1.3` not examined.** No evidence in either examined corpus indicates Guard
   consumes ARI.

A correction to an earlier statement in this session is recorded in `00_SCOPE_AND_METHOD.md`
§3.1: the specification corpus was initially reported as empty on the basis of
`aura-nomos/aura-specification`, a 2-file stub. The substantive corpus is
`AuraIDToken/aura-specification`; all findings here derive from it.

## 7. What is NOT claimed

- No formula, rounding mode, division mode, dimension, or bound is selected or recommended.
- No existing ARI defect is fixed or characterized as having a correct answer.
- No claim that the implementation is wrong — only that **nothing defines what right would be**.
- No fixture created; none modified. No production code, SPEC-002, ADR, or specification
  document touched.

## 8. Open questions for the Authority

1. **Does implementation-repository documentation carry an authority level?** `CLAUDE.md`'s
   ladder has no tier for it; ADR-006 §3.2 routes it to NB-021 CASE A as descriptive. Until
   settled, `mathematical_foundation.md`'s status is formally undetermined (**C-4**).
2. **Is the specification glossary's delegation to RI-PY intentional?** If so, ARI is defined as
   "whatever the implementation computes", and the FROZEN instrument — including CORE-P0-001,
   P0-002 and P1-004 — is by construction correct. If not, C-1 is a specification defect.
3. **ADR-005's division claim is factually wrong (C-3).** Correcting the text and selecting the
   division semantics are different acts requiring different authority. Which is in scope?
4. **Which artifact should carry the drift definition?** It is currently determined solely by
   `core/evaluator.py`, and drift is emitted and hashed.
5. **Do the PDF snapshots need adjudication** before RD-1 can close?

---

**Verdict: NO NORMATIVE DEFINITION FOUND.**

No semantic selection has been made. No ADR created. No specification amended. No production
code changed.
