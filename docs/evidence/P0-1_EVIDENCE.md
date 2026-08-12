# Evidence Note — P0-1 Fix

**Artefact:** P0-1 Fix — Vector Dimension Validation
**Date:** 2026-08-12
**Scope:** `core/evaluator.py`, `core/test_ari.py`, `scripts/checks/check_10_p01_dimension_validation.sh`
**Author:** Claude (conformance audit role, per `CLAUDE.md`)
**Verifier:** Automated test execution + negative control (documented in §5)
**Status:** IMPLEMENTED → TESTED → CI-WIRED → EVIDENCE RECORDED
**Baseline commit:** `9c6a5d8`
**Environment:** Python 3.11.15, linux x86_64

---

## 1. AS-IS finding (reproduced, not assumed)

`PoCAEvaluator.evaluate()` accepted an action vector of **any** length.
`vector_similarity_int32()` computes its dot product with
`sum(a * b for a, b in zip(v1, v2))`; `zip()` stops at the shorter operand and
raises nothing.

Reproduced against the unmodified baseline with a 10-dimension constitution:

| Input vector | AS-IS output | Problem |
|---|---|---|
| `[50000] * 5` (5 dims) | `{'ari': 85338, 'drift': 20945}` | Silent truncation — emits a plausible **high-reliability** score from a malformed input |
| `[50000] * 15` (15 dims) | `{'ari': 140677, 'drift': 0}` | **`ari` exceeds `SCALING_FACTOR` (100000)**, i.e. ARI > 1.0 |

The second row is a **range-invariant breach** beyond simple truncation: the
documented ARI range is `[0, 10^5]` and `TestARICalculation.test_ari_bounds`
asserts `ari <= SCALING_FACTOR`. That assertion held only because every
existing test supplied a correctly-dimensioned vector. A dimension mismatch
defeated the upper bound entirely.

There was no clamp on the upper bound in `evaluate()` — only
`raw_ari = max(0, raw_ari)` on the lower bound.

---

## 2. What was changed

1. Added `_validate_vector_dimension()` to `PoCAEvaluator`, comparing
   `len(vector)` against `len(self.constitution)`.
2. Invoked it as the **first statement** of `evaluate()` — before any
   arithmetic and before `vector_similarity_int32()`.
3. On mismatch: `raise ValueError` (**not** `assert`), so the guard survives
   `python -O` / `-OO`, per AGENTS.md rule 4.
4. Added 7 tests to `core/test_ari.py` (`TestVectorDimensionValidation`).
5. Added **CHECK 10** (`scripts/checks/check_10_p01_dimension_validation.sh`),
   wired into `scripts/run_all_checks.sh` and the CI artifact upload.

### 2.1 Why CHECK 10 was necessary

`core/test_ari.py` was previously only checked for **existence** by CHECK 4
(`check_4_audit_path.sh:39`: `if [ -f "core/test_ari.py" ]`). It was never
executed by any check script or CI job. Without CHECK 10, the P0-1 tests would
have been added to a file CI never runs, leaving the conformance claim without
executable evidence and violating AGENTS.md rule 9.

---

## 3. What was NOT changed

- ARI formula (`0.3*SI + 0.7*SA`)
- `round()`, `//`, scaling factor (`100000`)
- Existing bounds and clamp logic (see §6 — the upper bound remains unclamped
  by design; P0-1 removes the only known way to breach it, but does not add a
  clamp, as that would alter measurement semantics)
- Class structure
- Guard code (`aura-guard` is not present in this repository)
- Normative specification
- The 14 pre-existing tests in `core/test_ari.py`

---

## 4. Test execution log

```
$ python3 -m unittest core.test_ari.TestVectorDimensionValidation -v

test_dimension_validation_before_similarity ... ok
test_exact_dimension_succeeds ... ok
test_guard_active_under_optimized_bytecode ... ok
test_longer_vector_raises_value_error ... ok
test_mismatch_never_produces_ari ... ok
test_oversized_vector_would_breach_ari_upper_bound ... ok
test_shorter_vector_raises_value_error ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.175s

OK

$ python3 -m unittest core.test_ari

Ran 21 tests in 0.044s
OK
```

### 4.1 Full-suite regression comparison

| Tree | Tests run | Result |
|---|---|---|
| Baseline (unmodified) | 107 | `FAILED (errors=2)` |
| With P0-1 fix | 114 | `FAILED (errors=2)` |

`+7` tests, **no new failures**. The 2 errors are identical in both runs and
are environmental, not regressions: `core.test_cr003_statelessness` and the
audit DB integration suite require Docker
(`pgvector/pgvector:pg16`), which is unavailable in this execution
environment. They are exercised in CI by CHECK 7 and CHECK 8.

### 4.2 Mandatory execution checks

Run against the modified tree (Docker-dependent CHECK 7 / CHECK 8 omitted —
no Docker daemon in this environment):

| Check | Status |
|---|---|
| CHECK 0 — Constitutional Compliance | ✅ PASS |
| CHECK 1 — Bit Identity | ✅ PASS |
| CHECK 2 — Integer Only | ✅ PASS |
| CHECK 3 — Layer Separation | ✅ PASS |
| CHECK 4 — Audit Path | ✅ PASS |
| CHECK 5 — Entropy | ✅ PASS |
| CHECK 6 — Art.5 Runtime Proof (DEFAULT / -O / -OO) | ✅ PASS |
| CHECK 9 — CR-003 Layer Boundary | ✅ PASS |
| CHECK 10 — P0-1 Dimension Validation | ✅ PASS |
| CHECK 7 — CR-004 Append-Only DB | ⚠️ NOT RUN (requires Docker) |
| CHECK 8 — CR-003 History-Independence | ⚠️ NOT RUN (requires Docker) |

CHECK 3 confirms the new guard does not introduce Layer 0 policy: raising on a
malformed **input** is a measurement precondition, not a compliance decision.
No threshold is defined and no status field is returned; `evaluate()` still
returns exactly `{"ari", "drift"}`.

---

## 5. Negative control (adversarial verification)

A passing test proves nothing unless it can fail. The guard call was
temporarily replaced with a comment and CHECK 10 re-run:

| Tree state | CHECK 10 result |
|---|---|
| Guard present | ✅ PASS (exit 0) |
| Guard removed | ❌ FAIL (exit non-zero) |
| Guard restored | ✅ PASS (exit 0) |

CHECK 10 therefore detects the absence of the fix and is not a tautology.

A second fail-open defect was found and fixed **in the check script itself**
during review: the `-O`/`-OO` loop was originally piped into `tee`, which runs
the loop body in a subshell where `exit 1` cannot fail the script. The pipe was
removed; see the comment in `check_10_p01_dimension_validation.sh`.

---

## 6. Residual observations (NOT fixed — flagged for authority)

These were observed while producing this evidence. None is introduced by the
P0-1 fix; none is changed by it. Recording them rather than silently
reconciling them, per `AGENTS.md`.

1. **`drift` clamp contradicts its own comment.** `evaluator.py` says
   "Clamp drift to [0, 100000] to represent [0.0, 1.0]" but the code is
   `min(max(0, SCALING_FACTOR - sa), 2 * SCALING_FACTOR)` — an upper clamp of
   **200000**, not 100000. Observed: a 10-dim anti-aligned vector
   (`[-31622] * 10` against constitution `[31622] * 10`) returns
   `{'ari': 0, 'drift': 199996}` — a drift of ~2.0, double the documented
   maximum. Either the comment or the bound is wrong. Not touched: changing it
   would alter measurement semantics.

2. **`ari` has no upper clamp.** Only `max(0, raw_ari)` is applied. P0-1 closes
   the known route to exceeding `SCALING_FACTOR`, but the bound is a
   consequence of well-formed input rather than an enforced invariant. Whether
   Layer 0 should enforce an explicit upper clamp is a specification question.

3. **The constitution vector itself is unvalidated.** `__init__` accepts any
   list, including empty. With an empty constitution, `_validate_vector_dimension`
   requires an empty action vector, `sa` becomes `0`, and `evaluate()` returns
   `{'ari': 30000, 'drift': 100000}` for `valid_schema=True` — a measurement
   derived from no constitution at all. P0-1 was scoped to the action vector;
   constitution validation is a separate requirement.

4. **`scripts/checks/README.md` is stale.** It describes "5 execution checks"
   and lists CHECK 2 and CHECK 3 as `❌ FAIL` with `core/evaluator.py` named as
   a known violator. Both now pass. Only a CHECK 10 section was added; the
   stale content was left untouched as out of scope.

---

## 7. Conclusion

P0-1 is **verified**. A dimension mismatch is rejected before any similarity
computation and cannot produce an ARI value, under DEFAULT, `-O`, and `-OO`
bytecode. The claim is backed by an executable CI check whose failure mode has
been demonstrated.

Items in §6 remain open and require Protocol Custodian direction.
