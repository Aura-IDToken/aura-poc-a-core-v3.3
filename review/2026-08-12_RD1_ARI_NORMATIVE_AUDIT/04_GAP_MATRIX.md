# RD-1 — 04 GAP MATRIX

## 1. Definitional gaps

`N` = defined by a normative-tier artifact (levels 1–5) · `D` = stated only in descriptive
documentation · `I` = determined only by the implementation · `∅` = nowhere.

| # | Dimension | N | D | I | Verdict | Evidence |
|---|---|---|---|---|---|---|
| D1 | Formula | ✗ | ✅ | ✅ | **GAP — no authority** | E-5, E-9 |
| D2 | Input domain | ✗ | partial | ✅ | **GAP** | E-5, E-9 |
| D3 | Dimensionality | ✗ | legacy prose only | **none enforced** | **GAP — unbounded** | E-5 l.118, E-9 probe |
| D4 | Bounds | ✗ | ✅ `[0,100000]` | **no ceiling** | **GAP + CONFLICT (C-2)** | E-5 l.53, E-9 probe |
| D5 | Integer arithmetic | ✗ | ✅ | ✅ | **GAP — no authority** | E-6, E-9 |
| D6 | Division semantics | ✗ | ✅ **incorrect** | ✅ floor | **GAP + CONFLICT (C-3)** | E-6 l.133 |
| D7 | Rounding semantics | ✗ | ✗ | implicit | **TOTAL GAP** | corpus-wide absence |
| D8 | Malformed input | ✗ | ✗ | incidental | **TOTAL GAP** | E-9 probe, CORE-P0-001 |
| D9 | Drift | ✗ | ✗ | ✅ **sole determinant** | **TOTAL GAP** | E-5, E-9 |
| D10 | Penalty | ✗ | ✅ shape only; `P` undefined | ✅ | **GAP** | E-5, E-10 |
| D11 | Serialization / hash | ✗ | ✗ | audit path only | **TOTAL GAP** | E-13 |

**0 / 11 dimensions have normative coverage. 4 / 11 are total gaps — undefined in every
artifact of both corpora.**

## 2. Infrastructure gaps

| Artifact required to close RD-1 | Present? | Evidence |
|---|---|---|
| Normative ARI definition (any level 1–5) | **NO** | E-3, E-8 |
| ARI entry in Protocol Invariants (APS-100) | **NO** — 0 occurrences | E-3 |
| ARI conformance test (APS-400 / CONF-xxx) | **NO** — 0 occurrences; INV-010 ❌ | E-3, E-2 |
| ARI reference fixtures (APS-500) | **NO** — 0 occurrences; `/fixtures` MISSING; INV-014 ❌ | E-2, E-12 |
| Conformance runner (RI-004) | **NO** — MISSING | E-2 |
| Fixture loader (RI-005) | **NO** — MISSING | E-2 |
| Traceability from ARI to any requirement | **NO** | E-13 |
| Certified reference implementation | **NO** — RI-PY `NOT CERTIFIED` | E-2 |
| Independent (non-CPython) implementation | **NO** | ADR-006 §8.1 |
| Characterization harness executed by CI | **YES** | CHECK 10 @ `bdaa331` |

**One of ten exists** — the one U-1 delivered, and it is explicitly non-normative.

## 3. Gap severity relative to already-recorded findings

| Finding | Gap that permits it | Status |
|---|---|---|
| **CORE-P0-001** — malformed dimensionality yields a perfect score | D3 + D8 both total gaps; nothing constrains vector length, `zip` truncates | reproduced this audit: 1-dim vs 4-dim → `ari=100000` |
| **CORE-P0-002** — negative-value division diverges across languages | D6 gap; the sole statement (ADR-005) is wrong | reproduced: floor gives `29999/100001`, truncation gives `30000/100000` |
| **CORE-P1-004** — ARI exceeds the documented ceiling | D4 gap; doc states `[0,100000]`, code has no upper clamp | reproduced: `ari=7030000` |

Each of the three recorded P0/P1 ARI findings maps onto a dimension with **no normative
coverage**. They are not isolated defects: they are the observable consequences of the gaps in
§1. This is an observation about causation, not a remediation proposal.

## 4. What is NOT a gap

Recorded to keep the matrix honest:

- **The formula shape is not missing.** `RAW_ARI = 0.3×SI + 0.7×SA` is written down and is
  consistent between `mathematical_foundation.md`, the `evaluator.py` docstring, and
  `compliance/evaluator_wrapper.py`. What is missing is *authority*, not text.
- **Determinism within CPython is not in question.** Integer-only arithmetic and the frozen
  instrument make single-language reproducibility sound; INV-006 and INV-013 are ✅ in RI-PY.
- **Layer separation is not in question.** Measurement/decision separation is stated
  consistently in the Constitution, both glossaries, and the implementation.

The gap is confined to: **what ARI is required to be**, as distinct from what it currently is.
