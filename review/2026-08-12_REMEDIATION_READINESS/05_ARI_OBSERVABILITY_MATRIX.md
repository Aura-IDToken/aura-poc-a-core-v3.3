# 05 — ARI OBSERVABILITY MATRIX

**Date:** 2026-08-12
**Mode:** READ-ONLY. **The evaluator was not modified. No test file was created.**
**Normative effect:** NONE.
**Extends:** `review/2026-08-11_ENGINEERING_BASELINE/RD-006_ARI_OBSERVABILITY.md`

---

## §1 Objective

Make future semantic decisions **measurable**.

Every decision in `02_ARI_NORMATIVE_GAP.md` (AG-01…AG-15) will eventually have to be taken
by a human. This document specifies the observations that would let that human see **what
each choice actually costs** — expressed in the implementation's own measured outputs
rather than in prose.

**What this document does not do:** define ARI, fix ARI, choose among engines, choose any
semantic, or modify the evaluator.

---

## §2 Existing Observability — What RD-006 Already Established

`core/test_ari_observability.py` (368 lines, 8 tests) executes the real
`core.evaluator.PoCAEvaluator` and emits a machine-readable record.

**Values already observed** — all **IMPLEMENTATION-DERIVED / NON-NORMATIVE**:

| Case | Input | Schema | ARI | drift | Exposes |
|---|---|---|---:|---:|---|
| OBS-1 | aligned unit, dim 4 | valid | `100000` | `0` | baseline |
| OBS-2 | orthogonal, dim 4 | valid | `30000` | `100000` | structural term isolated |
| OBS-3 | aligned unit, **dim 1536** | valid | `100000` | `0` | documented dimension |
| OBS-4 | aligned unit, dim 4 | **invalid** | `70000` | `0` | semantic term isolated |
| OBS-5 | anti-aligned, dim 4 | valid | **`29999`** | **`100001`** | **AG-07 division** |

**Four controls** prove the harness executes rather than replays (patch-and-observe,
distinct-inputs, failure-recording, real-module assertion). The patch-and-observe control
is decisive: a replaying harness would report `100000` under the patch and it reports
`30000`.

**Two limits carried forward.** The harness is **inert in CI** (RM-10 / RD-6 unresolved),
and it observes **one engine only** — `ConsistencyCalculator` is deliberately not exercised.

---

## §3 The Observability Gap

RD-006 covers well-formed inputs plus one anti-aligned case. **Deliberately excluded**
(its Limitation 5): mismatched-length input and out-of-range input.

Mapped against the decisions that must be taken:

| Decision | Observable today? | Gap |
|---|---|---|
| AG-01 input domain | **partially** — OBS-4 varies `valid_schema` only | element types, `agent_id`, malformed structure |
| AG-02 dimensions | **no** | all cases use matching dimensions |
| AG-03 scaling | **no** | scale never varied |
| AG-04 similarity | **partially** — OBS-1/2/5 span the range | preconditions never violated |
| AG-05 integer width | **no** | accumulator never measured |
| AG-06 rounding | **no** | harness supplies int vectors directly; never calls the normalizer |
| **AG-07 division** | **YES — OBS-5** | the one decision already measurable |
| AG-08 negatives | **partially** — OBS-5 only | boundary values unexplored |
| AG-09 zero vectors | **no** | |
| AG-10 penalties | **no** | Engine A's penalty path not exercised |
| AG-11 drift | **partially** | upper bound never reached |
| AG-12 bounds | **no** | out-of-range excluded by design |
| AG-13 overflow | **no** | |
| AG-14 output encoding | **no** | |
| AG-15 determinism | **partially** | one architecture, one language |

**1 of 15 decisions is currently measurable.**

---

## §4 THE OBSERVABILITY MATRIX

Test cases required to make each decision measurable. **All are additive test cases; none
modifies the evaluator.** Values shown were executed this session and are
**implementation-derived and non-normative**.

---

### OB-A — Dimension dependence *(AG-02, RM-01)*

| ID | Observation | Measured this session |
|---|---|---|
| OB-A1 | agent dim < constitution dim | 2-of-4 → similarity `100000`, `{'ari': 100000, 'drift': 0}` |
| OB-A2 | agent dim > constitution dim | 6-of-4 → `100000` |
| OB-A3 | **1-of-1536** | `100000` — **1535 dimensions contribute nothing** |
| OB-A4 | empty agent vector | `{'ari': 30000, 'drift': 100000}` |
| OB-A5 | empty constitution | `{'ari': 30000, 'drift': 100000}` |
| OB-A6 | ARI as a function of truncation depth | sweep dim 1…1536 against a fixed 1536 constitution |

**Why OB-A6 matters.** A single sweep makes the fail-open surface *visible as a curve*
rather than as three anecdotes. It is the observation that most directly quantifies what
NB-015 must decide.

**Makes measurable:** AG-02, and the cost of each candidate response in AG-01.

---

### OB-B — Malformed input *(AG-01)*

| ID | Observation | Measured |
|---|---|---|
| OB-B1 | `valid_schema=False`, aligned | `{'ari': 70000, 'drift': 0}` |
| OB-B2 | float elements into the int32 engine | `{'ari': 30000.0, 'drift': 100000.0}` — **float outputs** |
| OB-B3 | Engine B, missing required key | `{'score': 0, 'reason': 'Invalid structure', 'status': 'FAIL'}` |
| OB-B4 | out-of-scale elements | Engine A `{'ari': 170000}`; Engine B **`ValueError`** (lazily, at `_semantic_alignment`) |

**OB-B2 is a new observation from this session**, not present in RD-006. The engine named
`..._int32`, in a repository gated on "integer only", returns **float** values when given
float input. CHECK 2 cannot see it — it is a lexical grep, and the floats arrive as runtime
argument values.

**Makes measurable:** AG-01, AG-05.

---

### OB-C — Negative values *(AG-08)*

| ID | Observation | Measured |
|---|---|---|
| OB-C1 | fully anti-aligned | `{'ari': 0, 'drift': 200000}` |
| OB-C2 | `SA = -1` (the 1-LSB case) | `{'ari': 29999, 'drift': 100001}` |
| OB-C3 | sweep `SA` across `[-100000, +100000]` | records exactly where `max(0, …)` engages |
| OB-C4 | the `max(0, …)` floor boundary | the `SA` at which `raw_ari` first clamps |

**Why OB-C3/C4 matter.** The lower clamp is applied *after* the weighted sum. The sweep
shows how much measurement information the floor discards — the quantity AG-08 must rule on.

**Makes measurable:** AG-08, and the interaction with AG-07.

---

### OB-D — Rounding boundaries *(AG-06)*

| ID | Observation | Measured |
|---|---|---|
| OB-D1 | `round()` at `0.5/1.5/2.5/3.5` | `[0, 2, 2, 4]` |
| OB-D2 | negatives | `-0.5→0`, `-1.5→-2`, `-2.5→-2` |
| OB-D3 | `scale_to_fixed_point` at boundaries | `[5e-6,1.5e-5,2.5e-5]` → `[0,2,2]` |
| OB-D4 | **end-to-end**: normalizer → evaluator | ARI delta attributable to the rounding rule alone |

**OB-D4 is the observation RD-006 explicitly lacks.** RD-006 supplies int vectors directly
and never calls `offline_normalizer`, so the `round()` site is off its path. Closing that
means a constitution built through the real normalizer, then evaluated — making the rounding
rule's effect on **ARI**, not just on the vector, measurable.

**Makes measurable:** AG-06, and its propagation into AG-12.

---

### OB-E — Division boundaries *(AG-07)*

| ID | Observation | Measured |
|---|---|---|
| OB-E1 | `dot` ∈ `{-1, -99999, -100000, -100001, -150000}` | `-1, -1, -1, -2, -2` |
| OB-E2 | ARI/drift at each | `-1` → `{'ari': 29999, 'drift': 100001}` |
| OB-E3 | **truncating-rule comparison column** | computed **arithmetically**, never by adopting the rule |
| OB-E4 | exact-multiple boundaries | `-100000` → `-1` under **both** rules — the agreement case |

**Method constraint, load-bearing.** OB-E3 must be computed as
`int(dot / 100000)` *within the observation record*, labelled explicitly as *"the value a
truncating implementation would produce"*. It **must not** be introduced as an expected
value, a fixture, or a second code path. The moment it becomes an assertion target, it
becomes a normative choice.

**Makes measurable:** AG-07 — the one decision that is **unregistered in any specification
register**.

---

### OB-F — Overflow and width *(AG-05, AG-13)*

| ID | Observation | Measured |
|---|---|---|
| OB-F1 | accumulator, 1536 dims at bound | **`15,360,000,000,000`** |
| OB-F2 | ratio to `i32::MAX` | **≈ 7154×** |
| OB-F3 | result after rescale | `153,600,000` — **fits `i32`** |
| OB-F4 | dimension at which the accumulator crosses `i32::MAX` | ≈ 215 dims at the scale bound |
| OB-F5 | ratio to `i64::MAX` | ≈ 6×10⁻⁷ — comfortable |

**OB-F4 is the decision-relevant number.** It states precisely where a fixed-width port
starts being wrong: **any dimension above ~215 at the scale bound overflows `i32`.** The
documented dimension is 1536.

**Structural limit that must be stated:** CPython **cannot** exhibit overflow. This matrix
can measure *magnitude* and *headroom*; it cannot observe the behaviour AG-13 must specify.
The reference implementation is structurally incapable of demonstrating conformance to an
overflow rule.

**Makes measurable:** AG-05; **bounds but does not resolve** AG-13.

---

### OB-G — Maximum and minimum output *(AG-12)*

| ID | Observation | Measured |
|---|---|---|
| OB-G1 | max observed ARI, 4 dims | `310000` (**3.1×** documented max) |
| OB-G2 | max observed ARI, 1536 dims | **`107550000`** (**1075×**) |
| OB-G3 | min observed ARI | `0` (floor engages) |
| OB-G4 | max observed drift | `200000` (**2×** its docstring range) |
| OB-G5 | ARI as a function of input magnitude | sweep element magnitude `0 → 200000` |
| OB-G6 | ARI as a function of dimension at fixed magnitude | shows the `1075×` is dimension-driven |

**OB-G6 is the clarifying observation.** It separates two causes currently conflated: ARI
exceeds its documented range partly because inputs are un-normalized (AG-01) and partly
because the sum scales with dimension (AG-02). **AG-12 cannot be decided sensibly without
knowing which contributes what.**

**Makes measurable:** AG-12, AG-04.

---

### OB-H — Drift *(AG-11)*

| ID | Observation | Measured |
|---|---|---|
| OB-H1 | drift at `SA = 100000` | `0` |
| OB-H2 | drift at `SA = 0` | `100000` |
| OB-H3 | drift at `SA = -100000` | `200000` — **exceeds the docstring range** |
| OB-H4 | drift at `SA = -1` | `100001` |
| OB-H5 | drift after certificate presentation | `2.0` / `1.00001` on a `[0.0, 1.0]` field |

**OB-H5 is the consequence observation.** It shows the contradiction does not stop at the
evaluator — it reaches the artefact a consumer would read.

**Makes measurable:** AG-11.

---

### OB-I — Schema effects *(AG-01, AG-10)*

| ID | Observation |
|---|---|
| OB-I1 | ARI with `valid_schema` True vs False, all else fixed → isolates the `30000` structural term |
| OB-I2 | Engine B structural determination vs Engine A caller assertion, same logical event |
| OB-I3 | Engine A `DRIFT_PENALTY = 150000` threshold at `SA < 68000` — ARI immediately below and above |
| OB-I4 | Engine B `VIOLATION_PENALTY = 10000 × count` for counts 0…10 |
| OB-I5 | **side-by-side penalty comparison** on one logical event |

**OB-I3 records a structural consequence.** `DRIFT_PENALTY = 150000` **exceeds** the maximum
in-range `RAW_ARI` of `100000`, so under Engine A any drift penalty floors ARI to `0`
**regardless of the measurement**. OB-I3 makes that visible as a cliff, which is what AG-10
must rule on.

**Makes measurable:** AG-10, and the RD-4 engine choice.

---

### OB-J — Drift over time / sequence *(AG-11, AG-15)*

| ID | Observation |
|---|---|
| OB-J1 | repeated evaluation, identical input, same process — measured **identical** |
| OB-J2 | fresh evaluator instance per call — measured **identical** |
| OB-J3 | evaluation sequence with progressively diverging vectors — records drift trajectory |
| OB-J4 | statelessness: result independent of evaluation history |

**Note.** OB-J4 is already asserted by CHECK 8 (`core.test_cr003_statelessness`), which is
**Docker-gated** and asserts only `result_A == result_B`. That assertion holds under **any**
division or rounding rule and therefore cannot detect AG-06 or AG-07.

**Makes measurable:** AG-15 within one runtime.

---

## §5 Cross-Platform and Cross-Language Extension

| Axis | Currently observed | What would be needed | Blocked by |
|---|---|---|---|
| x86_64 vs arm64, CPython | **no** — harness inert in CI | CI wiring (2 lines, drafted and not applied) | **RD-6** |
| CPython vs other Python | **no** | second interpreter leg | RD-6 |
| Python vs Rust/JS/C | **no** | an independent implementation | **RD-1 + RD-3**, then `08` |

**The critical limitation, stated plainly.** Both existing CI legs run **CPython**.
Therefore an x86_64-vs-arm64 comparison — even once RD-6 is answered — **cannot detect
AG-06 or AG-07**, because those are inter-*language* divergences. It would detect
intra-Python platform divergence, which is genuinely useful but is not the risk that
matters most.

**Only an independent implementation makes AG-06 and AG-07 observable.** That is `08`, and
it carries its own ordering trap.

---

## §6 Priority — Observation Value per Unit of Blockage

| Rank | Observation | Decision served | Blocked by | Cost |
|---|---|---|---|---|
| **1** | OB-A6 truncation sweep | AG-02, NB-015 | **nothing** | low |
| **2** | OB-E1…E4 division boundaries | **AG-07 (unregistered)** | **nothing** | low |
| **3** | OB-G6 dimension-vs-magnitude separation | AG-12 | **nothing** | low |
| **4** | OB-F4 `i32` crossover dimension | AG-05, AG-13 | **nothing** | trivial |
| **5** | OB-D4 end-to-end rounding → ARI | AG-06 | **nothing** | medium |
| **6** | OB-I5 penalty comparison | AG-10, RD-4 | **nothing** | medium |
| **7** | CI wiring of all the above | AG-15 | **RD-6** | 2 lines |
| **8** | cross-language comparison | AG-06, AG-07 | RD-1, RD-3, `08` | high |

**Ranks 1–6 are unblocked today.** They are characterization tests (NB-021 CASE D,
PERMITTED) that modify no production code. **Rank 7 is two lines and one governance
ruling.** Rank 8 is the terminal verification.

---

## §7 Mandatory Framing

Every observation added under this matrix must carry, in code and in any emitted artefact:

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

and the emitted record must carry `"normative_effect": "NONE"` and
`"status": "CHARACTERIZATION — IMPLEMENTATION-DERIVED / NON-NORMATIVE"`, **enforced by a
test that fails if the markers are removed** — the mechanism RD-006 already established, so
the disclaimer cannot be silently dropped from an artefact that outlives its context.

**On failure after a future decision:** the constant is replaced **deliberately, citing the
authorizing decision**. Never silenced, never quietly updated.

## §8 What This Document Does Not Do

Does not modify the evaluator. Does not create any test file. Does not define, fix, bound,
or clamp ARI. Does not select an engine or any semantic. Does not wire anything into CI —
RD-6 is unresolved and is **reported, not worked around**. Does not treat any observed value
as a requirement.

---

*This document has no normative effect. It specifies what to measure so that a future
decision can be taken with evidence rather than assumption.*
