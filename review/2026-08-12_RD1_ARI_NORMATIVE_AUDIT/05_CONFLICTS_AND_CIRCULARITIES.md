# RD-1 — 05 CONFLICTS AND CIRCULARITIES

No conflict below is resolved. Each is recorded with both sides quoted.

---

## C-1 — CIRCULARITY: the specification defines ARI by reference to the implementation

**Severity: STRUCTURAL — this is the finding that determines the verdict.**

`aura-specification/glossary/GLOSSARY.md` (level 2, the highest-authority ARI text in either
corpus):

> **ARI** (Aura Reliability Index)
> A deterministic measurement value computed **by RI-PY** using integer arithmetic.

`aura-specification/reference/RI-PY_AURA_POC_A_CORE.md`:

> Document ID: RI-PY · Version: v3.3
> **APS-950 Certification Status: NOT CERTIFIED**
> Repository: https://github.com/AuraIDToken/aura-poc-a-core-v3.3

The loop:

```
specification ──"ARI is what RI-PY computes"──▶ RI-PY
RI-PY ────────"is aura-poc-a-core-v3.3"───────▶ core/evaluator.py
core/evaluator.py ──is the only determinant──▶ the ARI value
        ▲                                              │
        └──────── nothing external closes the loop ─────┘
```

Two independent reasons this cannot yield a normative definition:

1. **The delegate is uncertified.** RI-PY carries `NOT CERTIFIED`; the corpus withholds the
   authority grant that rule R2 requires.
2. **The delegate contains no definition.** Even if certified, RI-PY states only a role
   ("Computes ARI scores via integer-only arithmetic") — no formula, domain, bounds, or drift.
   Delegation to an empty target transfers nothing.

The specification does not define ARI. It *names* it and points at the implementation.

---

## C-2 — CONFLICT: stated bounds vs implemented bounds

| Side | Statement |
|---|---|
| `docs/mathematical_foundation.md` l.53 | `RAW_ARI ∈ [0, 100000]  (int32, scaled by 10^5, Layer 0)` |
| same, l.18 | SA "clamped to [0, 10^5] in final RAW_ARI" |
| same, l.59 | "RAW_ARI clamped to [0, 100000] at Layer 0" |
| `core/evaluator.py` | `raw_ari = max(0, raw_ari)` — **lower clamp only; no ceiling** |

Reproduced this audit: over-scaled input → `{'ari': 7030000, 'drift': 0}`, 70× the stated
ceiling. Matches recorded finding **CORE-P1-004**.

A second instance inside the same function:

| Side | Statement |
|---|---|
| `core/evaluator.py` comment | "Clamp drift to [0, 100000] to represent [0.0, 1.0]" |
| `core/evaluator.py` code | `drift = min(max(0, SCALING_FACTOR - sa), 2 * SCALING_FACTOR)` — ceiling **200000** |
| RD-006 observation OBS-5 | `drift = 100001` — above the commented ceiling, below the coded one |

The implementation contradicts its own adjacent comment, and the observation record confirms
the code, not the comment.

---

## C-3 — CONFLICT: stated division semantics are factually wrong

**Severity: HIGH — this is the mechanism behind CORE-P0-002.**

`docs/ADR_005_NO_FLOAT_RUNTIME.md` (**Status: APPROVED**, l.3; **FROZEN (MC-READY 2026)**, l.397),
§"Bit-Identity Guarantee" l.133:

> Integer division (`//`) is deterministic (truncation toward zero)

CPython `//` is **floor** division, toward −∞. Verified during this audit:

```
-1 // 100000        = -1      (floor, what Python does)
truncation toward 0 =  0      (what ADR-005 claims)
```

The divergence reaches the output through **two** division sites in `evaluate()`:

```
OBS-5:  dot = −100000
        sa      = dot // 100000            = −1   (floor)   │ truncating: 0
        raw_ari = 30000 + (70000×sa)//100000 = 29999        │ truncating: 30000
        drift   = min(max(0,100000−sa),200000) = 100001     │ truncating: 100000
```

`29999 / 100001` is exactly the RD-006 OBS-5 record. `30000 / 100000` is exactly what the
harness documents a truncating implementation (Rust / C / JS) would produce.

**Consequence for RD-1:** the only artifact in either corpus that states division semantics
states them incorrectly, and the value implied by the stated rule differs from the value the
frozen instrument produces. An independent implementation built to ADR-005 as written would
**not** reproduce the reference implementation. No selection between the two is made here.

---

## C-4 — CONFLICT: which document, if any, is the ARI authority

Three artifacts each carry a marker suggesting authority, and no artifact adjudicates between
them:

| Artifact | Marker | Problem |
|---|---|---|
| `glossary/GLOSSARY.md` (spec) | level 2 location | delegates to an uncertified target (C-1) |
| `docs/mathematical_foundation.md` | `FROZEN` | no ladder level; no MUST/SHALL; contradicted on bounds (C-2) |
| `docs/ADR_005_NO_FLOAT_RUNTIME.md` | `APPROVED` + `FROZEN` | its ARI-relevant claim is false (C-3) |

`CLAUDE.md`'s authority ladder has **no tier for implementation-repository documentation**.
`ADR-006 §3.2` routes `Documentation` to NB-021 CASE A — *"Typographical / documentation-only
correction"*, evidenced by Decree Art. III item 5, *"Updating documentation to clarify existing
behavior"*. The corpus therefore treats these documents as **describing** behaviour, which is
incompatible with their being the source that **prescribes** it.

**DECISION REQUIRED — the corpus does not assign implementation-repo documentation an
authority level.** This audit does not assign one.

---

## C-5 — CONFLICT: the two glossaries disagree on the name

| Corpus | Expansion of "ARI" |
|---|---|
| `aura-specification/glossary/GLOSSARY.md` | **Aura** Reliability Index |
| `aura-poc-a-core-v3.3/docs/GLOSSARY.md` | **Agent** Reliability Index |

Low severity for the formula question, but recorded: the two corpora do not agree on what the
acronym denotes, and neither cites the other.

---

## C-6 — CIRCULARITY (secondary): characterization observations as de facto expectations

`core/test_ari_observability.py` records five implementation-derived observations and asserts
the implementation still reproduces them. It declares `normative_effect: NONE`, and CHECK 10
(U-1-B, `bdaa331`) prints that disclaimer on every run. ADR-006 ER-6 further forbids resolving
a failure by editing the pinned constant.

The controls are correct and the disclaimers are explicit. The residual risk is **sociological,
not technical**: the harness is now the only executable artifact that says anything about
specific ARI values, and it is CI-enforced. Over time, a CI-enforced value is liable to be
read as a requirement — the precise failure mode ADR-006 ER-1 exists to prevent, and the one
already realised once in `core/test_offline_normalizer.py:97-107`, which the corpus records as
locking in half-to-even rounding against no specification.

**Not a defect in U-1-B.** Recorded because RD-1 asks whether ARI has a normative definition,
and the answer must not later be supplied by accident from the characterization record.

---

## Summary

| ID | Type | Severity | Resolved here? |
|---|---|---|---|
| C-1 | Circularity — spec delegates to uncertified implementation | **STRUCTURAL** | No |
| C-2 | Conflict — bounds stated vs implemented | HIGH | No |
| C-3 | Conflict — division semantics stated incorrectly | **HIGH** | No |
| C-4 | Conflict — no authority level for impl-repo documentation | HIGH | No — DECISION REQUIRED |
| C-5 | Conflict — glossaries disagree on the name | LOW | No |
| C-6 | Circularity risk — characterization drifting into expectation | MEDIUM | No |

**No conflict is between two competing *normative* definitions**, because no normative
definition exists. Every conflict is documentation-vs-implementation or
documentation-vs-documentation. This distinction is what separates the verdict
`NO NORMATIVE DEFINITION FOUND` from `CONFLICTING NORMATIVE DEFINITIONS`.
