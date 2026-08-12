# 03 — CHARACTERIZATION TEST PLAN

**Date:** 2026-08-12
**Mode:** PLAN ONLY. **No test file was created. No production code was modified.**
**Normative effect:** NONE.

---

## §1 Mandatory Declaration

Every test specified in this document must carry the following statement, verbatim, in its
module docstring **and** in the body or failure message of each individual test:

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE
> SEMANTICS.**

This is not a formality. It is the mechanism that prevents these tests from becoming
accidental normative authority — the failure mode identified in `09` and already realised
once, in `core/test_offline_normalizer.py:97-107`, which locks in half-to-even rounding
against no specification.

## §2 What a Characterization Test Is

| Property | Requirement |
|---|---|
| Records | What the code does **today** |
| Asserts | That the recorded value is **still** what the code produces |
| Does **not** assert | That the value is **correct** |
| On future failure | The correct response is to **record the authorizing decision**, never to silently update the constant |

**Authority basis for writing these now:** `CONSTITUTIONAL_DECREE.md` Art. VII (Testing),
Art. III items 4–5; NB-021 **CASE D** (test-only changes **PERMITTED**). Precedent already
executed twice: `GUARD-G1_CHARACTERIZATION_TESTS.rs` (386 lines, 8/8 passing) and
`core/test_ari_observability.py` (RD-006, 8 tests passing).

## §3 Placement and Constraints

| Constraint | Consequence |
|---|---|
| **No production code may be modified** | Tests observe; they never adjust the observed. |
| New files only | Modifying an existing CI-executed test changes what a check asserts — forbidden by `AGENTS.md` rule 10. |
| `test_*.py` naming is load-bearing | CHECK 2, 3, 5 and 9 all skip files by the `test_` prefix (`scripts/check_cr003_layer_boundary.py:165-166`). A file placed in `core/` without it would be scanned. |
| No `float` token in `core/` non-test code | CHECK 2 is a plain lexical grep. Test files are excluded, but the exclusion is by filename convention. |
| **Not wired into CI by this plan** | CI wiring is RD-6 (RM-10), unresolved. Tests will be **inert** until it is answered. This is reported, not worked around. |

**Proposed files (not created):**

| File | Covers |
|---|---|
| `core/test_characterization_evaluator.py` | CH-01…CH-07, CH-09, CH-10, CH-12, CH-14 |
| `core/test_characterization_normalizer.py` | CH-05 |
| `compliance/test_characterization_engines.py` | CH-08 (differential), CH-02 (Engine B) |
| `audit/test_characterization_canonicalization.py` | CH-11 |
| `core/test_characterization_replay.py` | CH-13, CH-15 |

---

## §4 THE TEST CASES

All observed values below were **executed this session** at branch base `f3a87cc`,
CPython 3.11.15, Linux x86_64, little-endian. They are **implementation-derived and
non-normative**.

---

### CH-01 — Dimension mismatch *(task case 1)*

**Records:** that `zip()` truncation causes a mismatched vector to score maximum.

| # | Constitution | Agent vector | Observed similarity | Observed `evaluate` |
|---|---|---|---:|---|
| a | `[100000,0,0,0]` | `[100000,0]` | `100000` | `{'ari': 100000, 'drift': 0}` |
| b | `[100000,0,0,0]` | `[100000,0,0,0,99999,12345]` | `100000` | `{'ari': 100000, 'drift': 0}` |
| c | `[100000]+[0]*1535` | `[100000]` | `100000` | `{'ari': 100000, 'drift': 0}` |
| d | `[100000,0,0,0]` | `[]` | `0` | `{'ari': 30000, 'drift': 100000}` |
| e | `[]` | `[100000,0,0,0]` | `0` | `{'ari': 30000, 'drift': 100000}` |

**Control:** exact-length match must produce the same value as case (a) — proving the test
observes truncation and not a constant.

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> In particular it does **not** assert that maximum similarity is the wrong answer, nor
> what the right answer would be. NB-015 / `REQ-002-031` is unresolved.

---

### CH-02 — Dimension mismatch, Engine B *(task case 1, second engine)*

**Records:** that `ConsistencyCalculator` exhibits the same truncation.

```python
ConsistencyCalculator([100000,0,0,0], []).calculate(
    {"timestamp": 1, "embedding": [100000, 0], "content": "x"})
# → {'score': 100000, 'structural': 100000, 'semantic': 100000, 'penalty': 0, 'halted': False}
```

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

---

### CH-03 — Negative division *(task case 2)*

**Records:** floor-division behaviour for negative dividends, and its propagation.

| `dot` | Observed `dot // 100000` | A truncating language would give |
|---:|---:|---:|
| `-1` | `-1` | `0` |
| `-99999` | `-1` | `0` |
| `-100000` | `-1` | `-1` |
| `-100001` | `-2` | `-1` |
| `-150000` | `-2` | `-1` |

**Propagated observation:**
`PoCAEvaluator([-100000,0,0,0]).evaluate("a",[1,0,0,0],True)` → `{'ari': 29999, 'drift': 100001}`

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> The right-hand column is a **computed cross-language comparison**, not an assertion that
> the other value is correct. AG-07 is **unregistered in any decision register** — neither
> rule has authority. The test must not be read as favouring either.

---

### CH-04 — Malformed schema *(task case 8)*

**Records:** the effect of `valid_schema` and of structurally invalid input.

| Case | Observed |
|---|---|
| aligned, `valid_schema=True` | `{'ari': 100000, 'drift': 0}` |
| aligned, `valid_schema=False` | `{'ari': 70000, 'drift': 0}` |
| Engine B, missing `embedding` key | `{'score': 0, 'reason': 'Invalid structure', 'status': 'FAIL', 'halted': False}` |
| Engine B, missing `timestamp` key | as above |

**Records the structural divergence:** Engine A takes schema validity as a **caller
assertion**; Engine B **self-determines** it from required keys. The structural term means
two different things in the two engines.

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

---

### CH-05 — Rounding boundaries *(task case 3)*

**Records:** half-to-even behaviour at `.5` boundaries, both signs.

| Input | Observed `round()` |
|---:|---:|
| `0.5` | `0` |
| `1.5` | `2` |
| `2.5` | `2` |
| `3.5` | `4` |
| `-0.5` | `0` |
| `-1.5` | `-2` |
| `-2.5` | `-2` |

At the scaling site (`core/offline_normalizer.py:88`):

| Input vector | Observed |
|---|---|
| `[5e-6, 1.5e-5, 2.5e-5]` | `[0, 2, 2]` |
| `[-5e-6, -1.5e-5, -2.5e-5]` | `[0, -2, -2]` |

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> **Explicit guard-rail:** this test must **not** be named, described, or documented as
> testing "correct rounding". `round-half-to-even` is listed in `SPEC-002 §6 AD-CA-007` as
> a **candidate only**, and `SPEC-002:371` states that no candidate constitutes a
> recommendation, preference, default, or implied decision. **The implementation exhibiting
> a candidate's behaviour is not evidence that the candidate was selected.**

---

### CH-06 — Anti-aligned vectors and drift bound *(task case 5)*

**Records:** the `drift` docstring contradiction.

| Case | Observed | Docstring says |
|---|---|---|
| anti-aligned, `valid_schema=True` | `{'ari': 0, 'drift': 200000}` | drift clamped to `[0, 100000]` |
| RM-02 case | `{'ari': 29999, 'drift': 100001}` | as above |
| via `compliance/certificate.py` | presented as `2.0` / `1.00001` | field documented as `[0.0, 1.0]` ratio |

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> **Note on nature:** this is the one case where the contradiction itself needs no decision
> — `core/evaluator.py:85` and `:86` disagree inside a single file. Which of the two is
> authoritative is still **ARCHITECTURAL DECISION REQUIRED**.

---

### CH-07 — Orthogonal vectors *(task case 6)*

**Records:** the baseline measurement for zero semantic alignment.

```python
PoCAEvaluator([100000,0,0,0]).evaluate("a", [0,100000,0,0], True)
# → {'ari': 30000, 'drift': 100000}
```

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

---

### CH-08 — Zero vectors and the engine divergence *(task case 4)*

**Records:** that the two engines handle zero and out-of-scale input differently.

| Case | Engine A (`PoCAEvaluator`) | Engine B (`ConsistencyCalculator`) |
|---|---|---|
| zero constitution, zero vector | `{'ari': 30000, 'drift': 100000}` | `_semantic_alignment` returns `0` via explicit guard (`:84`) |
| empty vectors | `{'ari': 30000, 'drift': 100000}` | returns `0` via explicit guard (`:81`) |
| out-of-scale event vector (`200000`) | `{'ari': 170000, 'drift': 0}` | **raises `ValueError`** |
| out-of-scale constitution | accepted silently | **raises `ValueError`** (`:90`) |

> **CORRECTION TO PRIOR EVIDENCE, verified this session.** `08_BLOCKERS.md` P0-2 and
> `05_CORE_REMEDIATION_READINESS.md` §5.5 state that
> `ConsistencyCalculator([200000,0,0,0], …)` *raises at construction*. **It does not.**
> `__init__` (`compliance/consistency.py:23-26`) stores the vector unchecked; the
> `ValueError` is raised **lazily** inside `_semantic_alignment` (`:87`, `:90`), and only
> when `calculate()` reaches it with a structurally valid event. The finding — opposite
> validation postures — **stands unchanged**; only the location of the check is corrected.
> The test must observe the lazy behaviour, not the construction-time behaviour.

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> It records that the engines disagree. **It designates neither authoritative** (RD-4).

---

### CH-09 — ARI above documented maximum *(task case 9)*

**Records:** that ARI is unbounded above.

| Input | Observed `ari` | Ratio to documented max |
|---|---:|---:|
| 4 × `[100000]` vs 4 × `[100000]` | `310000` | **3.1×** |
| 1536 × `[100000]` vs 1536 × `[100000]` | `107550000` | **1075×** |
| out-of-scale `[200000,0,0,0]` | `170000` | 1.7× |

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> The phrase "documented maximum" refers to `core/evaluator.py` docstrings and
> `docs/mathematical_foundation.md`. **Neither is a normative source** (AG-12). The test
> records a discrepancy between code and its own documentation — **not** a violation of a
> specification, because no specification states a range.

---

### CH-10 — High-dimensional vectors *(task case 7)*

**Records:** behaviour at the documented dimension `1536`.

| Case | Observed |
|---|---|
| aligned unit, 1536 dims | `{'ari': 100000, 'drift': 0}` |
| all-at-bound, 1536 dims | `{'ari': 107550000, 'drift': 0}` |
| 1-of-1536 mismatch | `{'ari': 100000, 'drift': 0}` |

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> `1536` is used because it is what `core/offline_normalizer.py:44` declares — **not**
> because it is the specified dimension. AG-02 records three conflicting values (`1536`,
> `32`, and AD-CA-007's candidate `32`), none decided.

---

### CH-11 — JSON canonicalization variants *(task case 11)*

**Records:** that three canonicalization forms coexist and produce different bytes.

| Site | Form | Observed output for `{"b":1,"a":[1,2]}` |
|---|---|---|
| `audit/merkle.py:89` | `sort_keys=True, separators=(",",":")` | `{"a":[1,2],"b":1}` |
| `compliance/certificate.py:69` | `sort_keys=True`, defaults | `{"a": [1, 2], "b": 1}` |
| `core/merkle.py:8` | `sort_keys=True`, defaults | `{"a": [1, 2], "b": 1}` |

The test must additionally record the **SHA-256 of each form**, demonstrating that the
same logical object yields different digests through different paths.

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> It records that three forms exist. **It does not select a canonical form** — AD-CA-008 is
> `UNRESOLVED` with **"None approved"** (verified at `SPEC-002:382`).

---

### CH-12 — Integer overflow / boundary behaviour *(task case 10)*

**Records:** accumulator magnitude against fixed-width boundaries.

| Quantity | Observed |
|---|---:|
| `dot` for 1536 dims at scale bound | `15,360,000,000,000` (`1.536 × 10¹³`) |
| `i32::MAX` | `2,147,483,647` |
| Ratio | **≈ 7154×** |
| `dot // 100000` | `153,600,000` — **fits `i32`** |
| `i64::MAX` | `9,223,372,036,854,775,807` — accumulator fits |

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> **The test cannot characterize overflow behaviour, because CPython cannot exhibit it.**
> It records only the *magnitude* and its relationship to fixed-width boundaries. That the
> reference implementation is structurally incapable of demonstrating the behaviour AG-13
> must specify is itself the finding, and the test should say so.

---

### CH-13 — Deterministic replay *(task case 12)*

**Records:** repeatability within one runtime, and the CI observation gap.

| Assertion | Observed |
|---|---|
| Same input evaluated 3× in one process | identical — `{'ari': 72000, 'drift': 40000}` |
| Fresh evaluator instance per call | identical |
| Runtime identity captured | `CPython 3.11.15 / x86_64 / little-endian` |

The test must **also** pin the determinism report's import set — asserting that
`scripts/generate_determinism_report.py` imports `core.offline_normalizer`, `audit.merkle`,
`audit.signing` and **not** `core.evaluator` — so that the RM-10 blind spot is recorded as
an executable fact rather than a prose claim.

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**
> **Scope limit that must be stated in the test:** same-process repeatability is **not**
> cross-platform determinism and **not** cross-language determinism. It cannot detect
> AG-06 or AG-07, which are the divergences that matter.

---

### CH-14 — Float leakage into the integer engine *(additional; not in the task list)*

**Records:** a finding surfaced during this session's reproduction and not present in the
baseline package.

```python
PoCAEvaluator([1.0, 0.0, 0.0, 0.0]).evaluate("a", [1.0, 0, 0, 0], True)
# → {'ari': 30000.0, 'drift': 100000.0}      ← note: FLOAT outputs
```

**Observation.** The engine named `..._int32`, in a repository whose CHECK 2 gate is
"integer only", **accepts float input and returns float output**. The values are floats,
not integers. CHECK 2 cannot detect this: it is a lexical grep for the token `float` in
`core/*.py`, and no such token appears — the floats arrive as *argument values* at runtime.
`demo.py` does exactly this in production-shaped code.

**Why it is recorded here:** it is directly relevant to AG-01 (input domain) and AG-05
(integer arithmetic), and it demonstrates that CHECK 2's PASS must not be read as
"no floats reach the integer engine".

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

---

### CH-15 — Guard: `violations` mutation *(cross-repository)*

**Records:** that mutating `violations` leaves the chain verifying.

**Already executed and committed** as `GUARD-G1_CHARACTERIZATION_TESTS.rs`. Listed here for
completeness of the matrix; see `06` §7 for T-0a…T-0c, the remaining Guard characterization
work.

> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

---

## §5 Coverage Against the Required Case List

| # | Task-required case | Test | Status |
|---:|---|---|---|
| 1 | dimension mismatch | CH-01, CH-02 | specified |
| 2 | negative division | CH-03 | specified |
| 3 | rounding boundaries (0.5/1.5/2.5 + negatives) | CH-05 | specified |
| 4 | zero vectors | CH-08 | specified |
| 5 | anti-aligned vectors | CH-06 | specified |
| 6 | orthogonal vectors | CH-07 | specified |
| 7 | high-dimensional vectors | CH-10 | specified |
| 8 | malformed schema | CH-04 | specified |
| 9 | ARI above documented maximum | CH-09 | specified |
| 10 | integer overflow / boundary | CH-12 | specified **with a stated limitation** — CPython cannot overflow |
| 11 | JSON canonicalization variants | CH-11 | specified |
| 12 | deterministic replay | CH-13 | specified **with a stated scope limit** |
| — | *(additional)* float leakage | CH-14 | specified |
| — | *(additional)* Guard violations | CH-15 | already executed |

**All 12 required cases are covered.** Two carry explicit limitations that must be stated
in the test body rather than silently accepted.

## §6 Control Tests — the Anti-Tautology Requirement

Following the pattern proven in RD-006, every characterization module must include controls
demonstrating that it **executes** the implementation rather than replaying constants:

| Control | Mechanism |
|---|---|
| CT-1 | Patch `vector_similarity_int32` to return `0`; observed ARI must move, then recover when the patch lifts |
| CT-2 | Distinct inputs must produce distinct observations — proves it is not a constant emitter |
| CT-3 | Inject an exception; the harness must record failure, not swallow it |
| CT-4 | Assert `__module__ == "core.evaluator"` and that `__code__.co_filename` resolves to the real file — proves it is the production module, not a stub |

**CT-1 is the decisive control.** A harness that replayed a hard-coded value would report
the unpatched result under the patch.

## §7 Explicit Non-Goals

This plan does **not**: create any test file; modify any production code, CI file, or
workflow; wire anything into CI (RD-6 unresolved — reported, not worked around); assert
that any observed value is correct; select any semantic; create a normative fixture;
or authorize any subsequent regression test.

**Regression tests** (which *do* assert correctness) are specified in `01` §A.8 and remain
blocked until the corresponding decisions exist.

---

*This document has no normative effect. It specifies observation, not correction.*
