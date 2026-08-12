# 02 — ARI NORMATIVE GAP

**Date:** 2026-08-12
**Purpose:** state exactly what must be **normatively specified** before ARI implementation
can be corrected.
**Mode:** READ-ONLY. **No ARI value, formula, bound, or semantic is proposed or selected.**
**Normative effect:** NONE.

---

## §1 The Governing Fact

**ARI has no normative definition.** Re-verified at primary source this session against
`AuraIDToken/aura-specification` @ `62d2d6b`, exhaustively across `aps/`, `specification/`,
`invariants/`, `constitution/`, `conformance/`, `compliance/`, `glossary/`, `reference/`.

Total occurrences of ARI as a defined term: **one.**

> `glossary/GLOSSARY.md:27-28`
> **ARI** (Aura Reliability Index)
> *"A deterministic measurement value computed by RI-PY using integer arithmetic. ARI is a
> measurement, not a decision."*

The remaining four occurrences (`reference/RI-PY_AURA_POC_A_CORE.md:14,22,55`) are
descriptions of the implementation, not definitions of the term.

**Consequence.** The specification defines ARI *by reference to the implementation*, and
the implementation is the artefact under audit. There is no independent anchor. This is
not an oversight to be patched by engineering — it is the decision that must be taken.

## §2 What "Correcting ARI" Would Currently Mean

Nothing. The question *"correct to what?"* is unanswerable.

| Attempted correction | Why it is not available |
|---|---|
| Clamp ARI to `[0, 100000]` | The range `[0,100000]` appears only in implementation docstrings and `docs/mathematical_foundation.md`. **No normative source states it.** Adopting it would elevate implementation documentation to specification. |
| Make the two engines agree | Requires choosing which one is right — RD-4, undecided. |
| Fix the division to truncate | Requires choosing a division rule — **not listed even as a candidate** in AD-CA-007. |
| Fix the rounding | `round-half-to-even` is a **candidate only**; `SPEC-002:371` states no candidate constitutes a default or implied decision. |
| Reject dimension mismatch | Requires the required failure mode — `REQ-002-031`, unresolved, and APS-001 §8 is **TODO**. |

**Every available "correction" is a normative decision wearing engineering clothes.**

---

## §3 THE NORMATIVE DIMENSIONS

The minimum set that must be specified before implementation may be corrected. Each row
states what must be decided, what the implementation currently exhibits (**as evidence
only**), and the decision status.

> **Reading rule for the "Current implementation-derived behaviour" column.**
> Every value in it was obtained by executing the code. **None is a requirement, a
> recommendation, a default, or a proposal.** Per `SPEC-002 §6`, the fact that the
> implementation exhibits a behaviour matching a listed candidate is **not** evidence that
> the candidate was selected.

---

### AG-01 — Input domain

| | |
|---|---|
| **Must define** | What an ARI evaluation accepts: the type, structure and admissibility of `agent_id`, the agent vector, and `valid_schema`. |
| **Current behaviour** | `PoCAEvaluator.evaluate` accepts any `str`, any `list`, any `bool`. Element types are unchecked — floats are accepted (`demo.py` passes them). `agent_id` is used for nothing (`core/evaluator.py:59`: *"for audit trail only"*) and is never recorded. |
| **Divergence** | Engine B self-determines structural validity from required keys; Engine A takes it as a caller assertion. **The structural term means two different things.** |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** |

---

### AG-02 — Vector dimensions

| | |
|---|---|
| **Must define** | The dimension of the constitution vector and of the agent vector; whether they must be equal; behaviour when they are not. |
| **Current behaviour** | **Three conflicting values coexist.** `CONSTITUTION_DIM = 1536` (`core/offline_normalizer.py:44`, enforced only at `:171`); `embedding vector(32)` (`init.sql:96`) — **48× apart**; AD-CA-007 lists `32` as a **candidate only**. Neither evaluation engine references any of them. |
| **Divergence** | Mismatch is silently truncated by `zip()` and yields maximum similarity (RM-01). |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-007. Note this must be resolved **before** RM-01 detection can be implemented: detection requires an expected dimension, and there is no agreed one. |

---

### AG-03 — Scaling

| | |
|---|---|
| **Must define** | The fixed-point scale, and whether one scale governs all quantities. |
| **Current behaviour** | `SCALING_FACTOR = 100000` (10⁵), declared **independently in four modules** — `core/evaluator.py:12`, `compliance/consistency.py:18`, `compliance/policy.py`, `core/offline_normalizer.py`. No shared constant. AD-CA-007 lists `100000` as a **candidate only**. |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-007 |

---

### AG-04 — Similarity function

| | |
|---|---|
| **Must define** | The similarity measure, its mathematical definition, and its preconditions. |
| **Current behaviour** | Dot product rescaled by the scaling factor: `sum(a*b for a,b in zip(v1,v2)) // SCALING_FACTOR`. The docstring (`core/evaluator.py:29-31`) calls it cosine-equivalent *"for unit-normalized vectors"* — a precondition that is **stated but never enforced**. When it does not hold, the result is not a cosine similarity and is unbounded. |
| **Divergence** | `packages/database-client/VectorRepository.ts` uses **float cosine distance** — a third, unrelated model (unbuildable, unused). |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** |

---

### AG-05 — Integer arithmetic

| | |
|---|---|
| **Must define** | Integer width, signedness, and the width of intermediate accumulators. |
| **Current behaviour** | Functions are *named* `..._int32` and docstrings say "int32 vectors", but **Python integers are arbitrary-precision and nothing constrains any value to 32 bits**. Measured: for 1536 dims at the scale bound, the accumulator reaches `1.536 × 10¹³` — over 7000× `i32::MAX` (`2147483647`). The *result* fits `i32`; the *accumulator* requires at least `i64`. |
| **Consequence** | A direct `i32` port **panics in Rust debug builds and wraps in release builds**. `core/test_bitwise_replay.py:377-379` asserts a hard-coded literal `100000` is in `i32` range — it checks no computed value. |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-007 (`signed int32` is a **candidate only**) |

---

### AG-06 — Rounding

| | |
|---|---|
| **Must define** | The rounding rule at every float→int reduction, and whether one rule governs all sites. |
| **Current behaviour** | Python `round()` — **half-to-even**. Measured: `(0.5,1.5,2.5,3.5)` → `[0,2,2,4]`; negatives → `[0,-2,-2]`. Site: `core/offline_normalizer.py:88` — the **Constitution Vector construction path**. |
| **Divergence** | Rust/C give `[1,2,3,4]`; JS gives `[1,2,3,4]` and `[0,-1,-2]`. **Three different Constitution Vectors from one input.** |
| **Additional finding** | **Four coexisting reduction rules** in one repository: half-to-even (`round()`), floor (`//`), SQL half-up (`init.sql:60-62`: `((RAW_ARI + 500) / 1000)`), and plain float division (`compliance/certificate.py`). No shared definition. |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-007, `round-half-to-even` **candidate only** |

---

### AG-07 — Division

| | |
|---|---|
| **Must define** | Integer-division semantics, **specifically for negative dividends**. |
| **Current behaviour** | Python `//` **floors toward −∞**. Measured: `(-1)//100000 = -1`; `(-99999)//100000 = -1`; `(-100001)//100000 = -2`. |
| **Divergence** | Rust `/`, C, and `Math.trunc` **truncate toward zero** → `0`, `0`, `-1`. Propagated: `evaluate` yields `{'ari': 29999, 'drift': 100001}` where a truncating port yields `{'ari': 30000, 'drift': 100000}`. |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — and note the sharpest form of the gap: **verified this session, AD-CA-007's candidate set (`32`, `100000`, `signed int32`, `little-endian`, `Dictionary-Based Embedding`, `round-half-to-even`) contains no division rule at all.** This is not merely unresolved — it is **unregistered**. Tracked only as NB-016, in the engineering baseline, not in any specification register. |

---

### AG-08 — Negative values

| | |
|---|---|
| **Must define** | Whether negative similarity is admissible, and its meaning. |
| **Current behaviour** | `SA` may be negative (range documented as `[-10⁵, 10⁵]`). `raw_ari` is floored at `0` by `max(0, …)` (`core/evaluator.py:79`) — a **lower clamp only**, applied *after* the weighted sum. Whether that floor is a measurement statement or a presentation choice is undocumented. |
| **Interaction** | The negative branch is exactly where AG-07's divergence lives. AG-07 and AG-08 must be decided **together**. |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** |

---

### AG-09 — Zero vectors

| | |
|---|---|
| **Must define** | Behaviour for a zero constitution vector, a zero agent vector, and empty vectors. |
| **Current behaviour** | **The two engines disagree.** Engine B guards explicitly: `if not event_vec or not self.constitution: return 0` (`:81-82`) and `if all(value == 0 ...): return 0` (`:84-85`). Engine A has **no guard**. Measured this session: `PoCAEvaluator([0,0,0,0]).evaluate("a",[0,0,0,0],True)` → `{'ari': 30000, 'drift': 100000}`; `PoCAEvaluator([]).evaluate("a",[],True)` → **the same**. |
| **Note** | A zero vector has no direction; whether "similarity" is `0`, undefined, or an error is a mathematical modelling decision, not an engineering one. |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** |

---

### AG-10 — Penalties

| | |
|---|---|
| **Must define** | Whether ARI includes penalties; which model; and at which layer they apply. |
| **Current behaviour** | **Two irreconcilable models.** Engine A: `DRIFT_PENALTY = 150000`, threshold-triggered when `SA < 68000` (`compliance/policy.py`). Engine B: `VIOLATION_PENALTY = 10000 × violation count` (`compliance/consistency.py:21,102`). These are **different units of a different quantity** — a threshold constant versus a per-item rate. |
| **Structural note** | `DRIFT_PENALTY = 150000` **exceeds** the maximum in-range `RAW_ARI` of `100000`. Under Engine A, any drift penalty floors ARI to `0` regardless of the measurement. Whether that is intended is undocumented. |
| **Layering note** | `core/evaluator.py:6` states penalties are applied by Layer 2, not Layer 0 — so "ARI" may name two different quantities (pre- and post-penalty) depending on the layer. **The specification must say which one ARI is.** |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — RD-4 |

---

### AG-11 — Drift

| | |
|---|---|
| **Must define** | The definition of drift, its range, and its relationship to ARI. |
| **Current behaviour** | `drift = min(max(0, SCALING_FACTOR - sa), 2 * SCALING_FACTOR)` (`core/evaluator.py:86`). **The docstring one line above (`:85`) says clamp to `[0, 100000]`; the code clamps to `200000`.** Measured: `200000` and `100001`. |
| **Downstream** | `compliance/certificate.py` divides by `100000`, presenting `2.0` / `1.00001` on a field documented as a `[0.0, 1.0]` ratio. |
| **Status** | The **contradiction** is a pure BUG (RM-05) requiring no decision to observe. **Which of the two is authoritative is ARCHITECTURAL DECISION REQUIRED.** |

---

### AG-12 — Bounds

| | |
|---|---|
| **Must define** | The ARI output range and the point at which it is enforced. |
| **Current behaviour** | Documented `[0, 100000]` **with no normative source**. Measured: `310000` (3.1×) for 4 dims and **`107550000` (1075×)** for 1536 dims. No upper clamp exists — `core/evaluator.py:79` applies `max(0, …)` only. |
| **Enforcement inversion** | `init.sql:47` constrains `RAW_ARI BETWEEN 0 AND 100000`. **The invariant is declared where nothing enforces it and absent where the value is produced** — and no writer reaches the database at all (RM-14). |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — RD-1/DB-6 |

---

### AG-13 — Overflow

| | |
|---|---|
| **Must define** | Overflow behaviour: prohibited, wrapping, saturating, or checked. |
| **Current behaviour** | **Impossible in CPython** — arbitrary precision. Therefore *unspecified by construction*: the reference implementation cannot exhibit the behaviour that must be specified. |
| **Consequence** | The reference implementation is **structurally incapable** of demonstrating conformance to an overflow rule. Any second implementation in a fixed-width language will encounter it immediately (AG-05: the accumulator exceeds `i32` by >7000×). |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-007 |

---

### AG-14 — Output encoding

| | |
|---|---|
| **Must define** | How an ARI value is represented for transport, storage, and hashing. |
| **Current behaviour** | In-memory `dict` `{"ari": int, "drift": int}`. Storage: `init.sql` `DECIMAL(3,2)` for `poca_score`, integer for `RAW_ARI`. Presentation: float division by `100000` (`compliance/certificate.py`). **No canonical byte encoding exists in production code** — the only integer encoding anywhere is LE-signed 4-byte, and it lives solely in test/CI code (`core/test_bitwise_replay.py:287`, `scripts/generate_determinism_report.py:65`). |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-008 (`UNRESOLVED`, **"None approved"**) |

---

### AG-15 — Determinism requirements

| | |
|---|---|
| **Must define** | What determinism is claimed, across which axes, and how it is verified. |
| **Current behaviour** | Deterministic **within one CPython build**. Cross-*platform*: unverified for ARI — the determinism job computes no ARI (RM-10). Cross-*language*: **cannot** currently hold, given AG-06 and AG-07. |
| **Invariant coverage** | INV-001, INV-002 (Bit-Perfect Replay), INV-006 (Platform Independence), INV-013 all trace to APS-001 sections marked **TODO**, with fixtures **TODO** and verification status **NOT VERIFIED**. |
| **Status** | **ARCHITECTURAL DECISION REQUIRED** — and dependent on AG-01…AG-14, since determinism cannot be specified over an undefined computation. |

---

## §4 Status Roll-Up

| # | Dimension | Registered in a specification? | Status |
|---|---|---|---|
| AG-01 | Input domain | no | **ARCHITECTURAL DECISION REQUIRED** |
| AG-02 | Vector dimensions | partially — AD-CA-007 (candidate `32`) | **ARCHITECTURAL DECISION REQUIRED** |
| AG-03 | Scaling | partially — AD-CA-007 (candidate `100000`) | **ARCHITECTURAL DECISION REQUIRED** |
| AG-04 | Similarity function | no | **ARCHITECTURAL DECISION REQUIRED** |
| AG-05 | Integer arithmetic | partially — AD-CA-007 (candidate `signed int32`) | **ARCHITECTURAL DECISION REQUIRED** |
| AG-06 | Rounding | AD-CA-007 (candidate only) | **ARCHITECTURAL DECISION REQUIRED** |
| AG-07 | Division | **NO — unregistered anywhere** | **ARCHITECTURAL DECISION REQUIRED** |
| AG-08 | Negative values | no | **ARCHITECTURAL DECISION REQUIRED** |
| AG-09 | Zero vectors | no | **ARCHITECTURAL DECISION REQUIRED** |
| AG-10 | Penalties | no | **ARCHITECTURAL DECISION REQUIRED** |
| AG-11 | Drift | no | **ARCHITECTURAL DECISION REQUIRED** |
| AG-12 | Bounds | no | **ARCHITECTURAL DECISION REQUIRED** |
| AG-13 | Overflow | partially — AD-CA-007 | **ARCHITECTURAL DECISION REQUIRED** |
| AG-14 | Output encoding | AD-CA-008 (**"None approved"**) | **ARCHITECTURAL DECISION REQUIRED** |
| AG-15 | Determinism requirements | INV-001/002/006/013 — sources **TODO** | **ARCHITECTURAL DECISION REQUIRED** |

**15 of 15 dimensions are undecided.**

**Of those, 6 (AG-01, AG-04, AG-08, AG-09, AG-10, AG-11) are not registered in any
specification decision register at all** — they are not "unresolved AD-CA items", they are
questions no register currently asks. **AG-07 is the most acute:** it is a known,
reproduced cross-language divergence that appears in no candidate list anywhere.

## §5 Dependency Order

Decisions cannot be taken independently. Minimum ordering:

```
AG-01 input domain ──┐
AG-02 dimensions ────┼──► AG-04 similarity ──► AG-08 negatives ──┐
AG-03 scaling ───────┘                         AG-09 zero vectors │
                                                                  ▼
AG-05 integer width ──► AG-13 overflow ──────────────────► AG-12 bounds
AG-06 rounding ───────┐                                          │
AG-07 division ───────┴──────────────────────────────────────────┤
                                                                  ▼
                                   AG-10 penalties ──► AG-11 drift
                                                          │
                                                          ▼
                                              AG-14 output encoding
                                                          │
                                                          ▼
                                              AG-15 determinism
```

**AG-15 is terminal** — determinism cannot be specified over an undefined computation.
**AG-01, AG-02, AG-03, AG-05, AG-06, AG-07 are roots** and may be taken in parallel.

## §6 What Must NOT Happen

| Prohibited | Why |
|---|---|
| Adopting the implementation's current behaviour as the definition | Stop condition 8. `SPEC-002 §6` forbids reading candidate-matching behaviour as candidate selection. |
| Adopting `[0, 100000]` because docstrings say so | Implementation documentation is not specification. |
| Choosing `round-half-to-even` because Python does it | It is a **candidate only**; the implementation exhibiting it is not evidence of selection. |
| Choosing floor division because Python does it | **Not even a candidate.** Selecting it would create normative authority from nothing. |
| Writing a conformance fixture with an ARI expected value | Stop condition 5. It would encode an unapproved value. |
| Treating `core/test_offline_normalizer.py:97-107` as authority | It **already** locks in half-to-even against no specification. Flagged as accidental-authority risk in `09`. |

## §7 What This Document Does Not Do

Does not define ARI. Does not select a formula, range, dimension, similarity function,
rounding rule, division rule, penalty model, encoding, or determinism claim. Does not
recommend any candidate. Does not create an ADR. Does not amend SPEC-002. Does not modify
code. Does not assert that the current implementation is wrong — only that **the question
of whether it is wrong currently has no answer**.

---

*This document has no normative effect. It records the shape of a decision that has not
been taken.*
