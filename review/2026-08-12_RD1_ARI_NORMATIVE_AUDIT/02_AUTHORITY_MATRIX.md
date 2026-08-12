# RD-1 — 02 AUTHORITY MATRIX

## 1. Candidates ranked by authority

| Rank | Artifact | Tier / level | Status | Defines ARI? | Normative? |
|---|---|---|---|---|---|
| 1 | `CONSTITUTIONAL_DECREE.md` | 1 — Constitutional | FROZEN | **no ARI content at all** | — |
| 2 | `aps/APS-000` … `APS-950` (markdown) | 2 — Specification | various | **0 ARI occurrences** | — |
| 2 | `specification/SPEC-002` | 2 — Specification | **0.3-DRAFT / DRAFT** | **0 ARI occurrences** | no |
| 3 | `aps/APS-100_PROTOCOL_INVARIANTS.md` | 3 — Invariants | — | **0 ARI occurrences** | — |
| 4 | `glossary/GLOSSARY.md` (spec corpus) | 2 — Specification | unversioned entry | **names ARI; defines it by reference to RI-PY** | **no** — delegates |
| 5 | `aps/APS-400_CONFORMANCE_TEST_MATRIX.md` | 5 — Conformance | — | **0 ARI occurrences** | — |
| 6 | `reference/RI-PY_AURA_POC_A_CORE.md` | 2 by location | **NOT CERTIFIED** | describes role only; no formula | **no** — grant withheld |
| 7 | `docs/mathematical_foundation.md` | **no ladder level** | FROZEN | **only formula in either corpus** | **no** — descriptive |
| 8 | `docs/ADR_005_NO_FLOAT_RUNTIME.md` | repository ADR | APPROVED / FROZEN | division semantics — **stated incorrectly** | contested |
| 9 | `docs/GLOSSARY.md` (impl repo) | no ladder level | — | conceptual only | no |
| 10 | `core/evaluator.py` | 9 — Implementation | FROZEN | determines every value in practice | **no** (rule R1) |
| 11 | `compliance/evaluator_wrapper.py` | 9 — Implementation | — | penalty application | no |
| 12 | `core/test_ari_observability.py` | 9 — test | characterization | records observations | **no** — self-declared `normative_effect: NONE` |

## 2. The decisive structural fact

Authority and definitional content are **disjoint** in this corpus:

```
    AUTHORITY                                CONTENT
    ─────────                                ───────
 1  Constitution ......... silent on ARI
 2  APS (normative) ...... 0 occurrences
 3  Invariants ........... 0 occurrences
 5  Conformance matrix ... 0 occurrences
 2  Spec glossary ........ names ARI ──delegates──▶ RI-PY (NOT CERTIFIED)
                                                      │
                                                      ▼
    ─── no ladder level ── math_foundation ....... FORMULA ✅ (descriptive only)
    ─── no ladder level ── ADR-005 ............... DIVISION ✅ (incorrect)
 9  Implementation ....... evaluator.py .......... EVERY ACTUAL VALUE
```

**Every artifact that carries authority is silent. Every artifact that carries content lacks
authority.** No artifact occupies both columns.

## 3. Coverage of the eleven dimensions by any level 1–5 artifact

| Dimension | Defined by any normative-tier artifact? | Where it is actually determined |
|---|---|---|
| D1 formula | **NO** | `docs/mathematical_foundation.md` (no level) + `core/evaluator.py` |
| D2 input domain | **NO** | implementation, implicitly |
| D3 dimensionality | **NO** | **nothing enforces it**; `1536` is legacy prose |
| D4 bounds | **NO** | doc states `[0,100000]`; implementation enforces no ceiling |
| D5 integer arithmetic | **NO** | ADR-005 + implementation |
| D6 division | **NO** | ADR-005 (incorrectly) + CPython `//` |
| D7 rounding | **NO** | nothing — undefined everywhere |
| D8 malformed input | **NO** | nothing — `zip` truncation is incidental |
| D9 drift | **NO** | **`core/evaluator.py` alone** |
| D10 penalty | **NO** | `compliance/` + prose |
| D11 serialization/hash | **NO** | `audit/` Merkle path; no ARI-specific rule |

**Zero of eleven dimensions are defined by any artifact at authority levels 1–5.**

## 4. Why `FROZEN` does not rescue `mathematical_foundation.md`

Applying rule **R3**:

- `FROZEN` is a change-control state, not a grant of definitional authority. `docs/GLOSSARY.md`
  in the same repository defines Iron Core as *"A frozen, immutable implementation … Any
  modification creates a new instrument lineage"* — freezing describes an **instrument**, not a
  norm.
- The document contains no `MUST` or `SHALL`, and the word `normative` does not appear in it.
- ADR-006 §3.2 lists `Documentation` as out of its scope, governed by **NB-021 CASE A**, which
  is titled *"Typographical / documentation-only correction"* and is evidenced by
  `CONSTITUTIONAL_DECREE.md` Art. III item 5: *"Updating documentation to clarify existing
  behavior"*. The corpus therefore classes this document as **describing existing behaviour** —
  the definition of implementation-derived.
- It is contradicted by the implementation on bounds (C-2) and is silent on drift.

A document that describes existing behaviour, carries no obligation language, sits at no
authority level, and disagrees with the artifact it describes cannot be the normative source.

## 5. Why RI-PY does not rescue the chain

Applying rule **R2** — the corpus must *grant* RI-PY authority. It does the opposite:

| Signal | Value |
|---|---|
| `APS-950 Certification Status` | **NOT CERTIFIED** |
| RI-004 Conformance Runner | ❌ MISSING |
| RI-005 Fixture Loader | ❌ MISSING |
| INV-010 (CONF-xxx tests) | ❌ |
| INV-014 (fixture runner) | ❌ |

RI-PY is the *subject* of certification, not a source of it — and it is uncertified. It also
contains no formula, so even if authority were granted, no definition would be transferred.
