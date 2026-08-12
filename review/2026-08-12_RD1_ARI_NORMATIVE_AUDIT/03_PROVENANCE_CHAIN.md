# RD-1 — 03 PROVENANCE CHAIN

Every edge is marked `PRESENT`, `BROKEN`, or `INVERTED`.

---

## 1. The chain as required

```
NORMATIVE SOURCE
    ↓ [1]
FORMULA
    ↓ [2]
INPUT CONTRACT
    ↓ [3]
ARITHMETIC SEMANTICS
    ↓ [4]
OUTPUT CONTRACT
    ↓ [5]
IMPLEMENTATION
    ↓ [6]
CHARACTERIZATION TEST
    ↓ [7]
INDEPENDENT IMPLEMENTATION
```

## 2. The chain as found

```
NORMATIVE SOURCE
   ✗ DOES NOT EXIST
   Constitution: 0 ARI · APS-000…950: 0 ARI · APS-100 invariants: 0 ARI
   APS-400 conformance: 0 ARI · SPEC-002 (DRAFT): 0 ARI
   Spec glossary: names ARI, delegates to RI-PY (NOT CERTIFIED)
        ┊
        ┊  [1] BROKEN — no source to originate from
        ▼
FORMULA
   ⚠ EXISTS WITHOUT A SOURCE
   docs/mathematical_foundation.md: RAW_ARI = 0.3×SI + 0.7×SA
   Authority level: none. Status: FROZEN (≠ normative, rule R3)
        ┊
        ┊  [2] BROKEN — no input contract is stated
        ▼
INPUT CONTRACT
   ✗ DOES NOT EXIST
   No dimensionality requirement · no domain constraint · no validity precondition
   `1536` appears only in legacy/offline prose, never as a runtime rule
   Implementation enforces nothing: zip() truncates silently  → CORE-P0-001
        ┊
        ┊  [3] BROKEN, and the one statement that exists is WRONG
        ▼
ARITHMETIC SEMANTICS
   ⚠ STATED INCORRECTLY
   ADR-005 (APPROVED/FROZEN): "Integer division (//) is deterministic
   (truncation toward zero)" — false; CPython // floors toward −∞
   Rounding: undefined everywhere in both corpora
        ┊
        ┊  [4] BROKEN — output contract contradicts the implementation
        ▼
OUTPUT CONTRACT
   ⚠ STATED AND VIOLATED
   Doc: RAW_ARI ∈ [0, 100000].  Implementation: no upper clamp; 7,030,000 demonstrated
   Doc comment: drift clamped [0,100000].  Code: clamps to 200000; OBS-5 drift = 100001
   DRIFT: no definition anywhere in either corpus
        ┊
        ┊  [5] INVERTED — see §3
        ▼
IMPLEMENTATION
   ✓ EXISTS — core/evaluator.py, FROZEN
   The de facto sole determinant of every ARI and drift value
        ┊
        ┊  [6] PRESENT — the only sound edge in the chain
        ▼
CHARACTERIZATION TEST
   ✓ EXISTS — core/test_ari_observability.py, executed by CHECK 10 (U-1-B, bdaa331)
   5 observations, 8 tests, normative_effect: NONE — self-declared non-normative
        ┊
        ┊  [7] BROKEN — nothing to implement against
        ▼
INDEPENDENT IMPLEMENTATION
   ✗ DOES NOT EXIST
   No fixtures (APS-500: 0 ARI; /fixtures MISSING; INV-014 ❌)
   No conformance runner (RI-004 MISSING; INV-010 ❌)
   Both CI legs are CPython — cross-language divergence unobservable (ADR-006 §8.1)
```

## 3. Edge [5] is INVERTED, not merely broken

The required direction is `OUTPUT CONTRACT → IMPLEMENTATION`: the contract constrains the code.

The actual direction is the reverse. The specification glossary — the highest-authority ARI
text in existence — defines ARI as *"a deterministic measurement value **computed by RI-PY**"*.
RI-PY is a document *about* `aura-poc-a-core-v3.3`. So the authority chain terminates in the
implementation and then points back at it:

```
   spec glossary ──defines ARI as──▶ "whatever RI-PY computes"
                                            │
                                            ▼
                                    RI-PY (NOT CERTIFIED)
                                            │
                                    describes
                                            ▼
                                    core/evaluator.py
                                            │
                                            └──── is the only thing that
                                                  determines ARI ────┐
                                                                     │
   ◀─────────────────────────────────────────────────────────────────┘
                        (no independent norm closes this loop)
```

The implementation is not constrained by the contract; the contract is *populated by* the
implementation. This is the circularity recorded as **C-1** in
`05_CONFLICTS_AND_CIRCULARITIES.md`.

## 4. Edge summary

| Edge | From → To | State | Basis |
|---|---|---|---|
| [1] | NORMATIVE SOURCE → FORMULA | **BROKEN** | no normative source exists |
| [2] | FORMULA → INPUT CONTRACT | **BROKEN** | no input contract stated anywhere |
| [3] | INPUT CONTRACT → ARITHMETIC SEMANTICS | **BROKEN** | ADR-005's only statement is factually wrong; rounding undefined |
| [4] | ARITHMETIC SEMANTICS → OUTPUT CONTRACT | **BROKEN** | stated bounds violated by implementation; drift undefined |
| [5] | OUTPUT CONTRACT → IMPLEMENTATION | **INVERTED** | glossary defines ARI *by* the implementation |
| [6] | IMPLEMENTATION → CHARACTERIZATION TEST | **PRESENT** | CHECK 10 executes the harness fail-closed |
| [7] | CHARACTERIZATION TEST → INDEPENDENT IMPLEMENTATION | **BROKEN** | no fixtures, no conformance runner, single language |

**1 of 7 edges is sound.** The one sound edge is the one U-1 delivered — and it connects the
implementation to a test that explicitly disclaims normative force.

## 5. What edge [6] does and does not establish

CHECK 10 proves the implementation still produces what it produced before. It is a
**regression detector against itself**. It cannot supply the missing normative source, and the
harness says so in its own text (`normative_effect: NONE`). Per rule **R1**, a green CHECK 10
is not evidence that any observed ARI value is correct.
