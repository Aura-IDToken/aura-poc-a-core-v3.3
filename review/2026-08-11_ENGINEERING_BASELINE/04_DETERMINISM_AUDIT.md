# 04 — DETERMINISM AUDIT (TASK 4)

**Nothing in this document is fixed.** Every finding is an AS-IS observation with
reproduction evidence. No semantics are selected.

---

## 0. Classification Key

Each finding carries four independent tags:

- **Reachability:** `LATENT` (property of the code, cannot currently produce a divergent
  observable result because no second implementation / no reaching caller exists) or
  `ACTIVE` (can produce a wrong or divergent observable result today).
- **Test status:** `TESTED` (an existing test would fail if the behaviour changed) or
  `UNTESTED`.
- **Nature:** `NORMATIVE GAP` (the specification does not define which behaviour is
  correct, so the code cannot be said to be wrong) and/or `ENGINEERING BUG` (the code
  contradicts its own documented contract, or fails independently of any normative
  choice).

A finding may be both `NORMATIVE GAP` and `ENGINEERING BUG`. Where it is, the two aspects
are separated explicitly, because only the engineering aspect is actionable without
governance.

**Determinism within one Python build is not in question.** Every finding below concerns
either (a) agreement with a *different* implementation, or (b) agreement with the code's
*own stated contract*.

---

## 1. Specifically Verified Reported Issues

### D-1 — Python `//` vs Rust / C / JS division semantics

**Location:** `core/evaluator.py:47` (`similarity = dot // self.SCALING_FACTOR`),
`core/evaluator.py:83-84` (weight rescale), `compliance/consistency.py:97`,
`compliance/consistency.py:59-61`.

**Confirmed.** Python `//` on integers **floors** toward −∞. Rust `/` on integers, C
integer division, and JS `Math.trunc(a/b)` **truncate** toward zero. For a negative
dividend that is not an exact multiple, the two differ by 1 LSB.

**Reproduced this session:**
```
(-1) // 100000            → -1        # Python floor
                            (Rust i64: -1 / 100000 == 0)

PoCAEvaluator([-100000,0,0,0]).vector_similarity_int32([1,0,0,0], const)
                          → -1        # a Rust port would give 0
PoCAEvaluator([-100000,0,0,0]).evaluate("a", [1,0,0,0], True)
                          → {'ari': 29999, 'drift': 100001}
                            (a truncating port would give ari 30000, drift 100000)
```
The 1-LSB divergence propagates: `70000 * (-1) // 100000 = -1`, so `ari` differs by 1,
and `drift = 100000 - (-1) = 100001` versus `100000 - 0 = 100000`.

**Reachability:** `LATENT`. Negative `SA` is reachable in Python (shown above), and the
divergence is deterministic within Python. It is LATENT only because **no second-language
implementation of this arithmetic exists** (see `03_LANGUAGE_BOUNDARY.md` §1). It becomes
`ACTIVE` the moment any Rust/C/JS/WASM port, or any FFI boundary, is introduced.

**Test status:** `UNTESTED`.
- No test asserts the exact value of `vector_similarity_int32` for a negative dot
  product. `core/test_ari.py:230-235` asserts only `sim3 < -90000` — a bound, not a value,
  and it would pass identically under either division rule.
- `core/test_bitwise_replay.py` never calls `PoCAEvaluator` at all.
- The cross-platform determinism report does not include any evaluator output.

**Nature:** `NORMATIVE GAP` **and** `ENGINEERING BUG`, separable:
- *Normative aspect:* which rounding-of-division is correct is unresolved.
  `SPEC-002 §6 AD-CA-007` lists `round-half-to-even` as a **candidate only** for numeric
  representation and lists no division rule at all. The specification does not say the
  code is wrong.
- *Engineering aspect:* the divergence is **undocumented and untested**. Neither
  `docs/ADR_005_NO_FLOAT_RUNTIME.md` nor `docs/mathematical_foundation.md` nor
  `docs/KNOWN_LIMITATIONS.md` records that the rescale step's negative-value behaviour is
  implementation-defined across languages. That omission is an engineering defect
  independent of which rule is eventually chosen.

**Not fixed.**

---

### D-2 — Python `round()` vs other-language rounding

**Location:** `core/offline_normalizer.py:88`
(`int_vector = [round(x * SCALING_FACTOR) for x in normalized_vector]`).
Also present in test helper `core/test_ari.py:25`.

**Confirmed.** Python 3 `round()` implements **banker's rounding** (half-to-even). Rust
`f64::round()`, C `round()`, and JS `Math.round()` do not: Rust/C round half away from
zero; JS rounds half toward +∞.

**Reproduced this session:**
```
round(0.5)  → 0        round(1.5) → 2        round(2.5) → 2
scale_to_fixed_point([0.000005, 0.000015, 0.000025])   → [0, 2, 2]
scale_to_fixed_point([-0.000005, -0.000015, -0.000025]) → [0, -2, -2]
```
A Rust port of the same function would produce `[1, 2, 3]` and `[-1, -2, -3]`.
A JS port would produce `[1, 2, 3]` and `[0, -1, -2]`. **Three different vectors from the
same input.**

**Reachability:** `LATENT`, for two independent reasons:
1. No second-language normalizer exists.
2. `normalize_constitution_vector` output is not consumed by any production runtime path
   (`02_RUNTIME_DATAFLOW.md` §2) — only hashed by tests and the determinism report.

Note that it **is** ACTIVE inside the CI determinism vector: `ari_vector_hash` is a hash
of `round()` output. A non-CPython Python implementation, or a Python version with
different rounding, would change that hash. All current CI legs use CPython 3.12, so this
does not currently fire.

**Test status:** `TESTED` — but for the *current* behaviour, and only partially.
`core/test_offline_normalizer.py:97-107` (`test_scale_to_fixed_point_rounding`) asserts
against Python's present behaviour. It **locks in** half-to-even; it does not verify it
against a specification, because none exists. There is no test asserting behaviour at an
exact `.5` boundary in a way that would reveal the cross-language issue, and no test
covering negative half-values.

**Nature:** `NORMATIVE GAP` (primary) **and** `ENGINEERING BUG` (secondary):
- *Normative aspect:* `AD-CA-007` explicitly lists `round-half-to-even` as a **candidate
  only** — "No candidate choice listed in this table constitutes a recommendation,
  preference, default, or implied architectural decision" (`SPEC-002 §6`). The
  implementation currently exhibits one of the candidate behaviours. **This must not be
  read as the candidate having been selected, and this audit does not select it.**
- *Engineering aspect:* the module docstring at `core/offline_normalizer.py:15` states
  the rule as `v_int = round(v_float × 10^5)` without qualifying *which* rounding.
  `scale_to_fixed_point`'s docstring (`:79`) repeats it. A reader implementing from that
  documentation in any other language produces a different vector. The documentation is
  under-specified relative to the code — that is an engineering defect regardless of the
  eventual normative answer.

**Additional AS-IS observation (recorded, not resolved):** the repository contains a
**third** numeric reduction rule, in SQL: `init.sql:60-62` derives `poca_score` from
`RAW_ARI` via `((RAW_ARI + 500) / 1000)` — integer half-up. And a **fourth**, in
`compliance/certificate.py`, plain float division by 100000. Four rounding/reduction
behaviours coexist (Python half-to-even, SQL half-up, float division, and floor division
in the evaluator). No shared definition exists.

**Not fixed.**

---

### D-3 — `zip()` truncation in `vector_similarity_int32`

**Location:** `core/evaluator.py:41` (`dot = sum(a * b for a, b in zip(v1, v2))`).
Identical pattern at `compliance/consistency.py:96`.

**Confirmed.** `zip` stops at the shorter sequence. A dimension mismatch is silently
ignored; the excess tail of the longer vector contributes nothing and no error is raised.

**Reproduced this session** (constitution = `[100000,0,0,0]`, 4 dims):
```
vector_similarity_int32([100000, 0], constitution)
    → 100000        # 2-dim agent vector vs 4-dim constitution: full-alignment score
vector_similarity_int32([100000, 0, 0, 0, 99999, 12345], constitution)
    → 100000        # 6-dim agent vector: excess silently discarded
```
Both return the **maximum possible similarity**, i.e. a truncated or malformed vector
scores as perfectly aligned.

Same on the Layer-2 engine:
```
ConsistencyCalculator([100000,0,0,0], []).calculate(
    {"timestamp":1, "embedding":[100000,0], "content":"x"})
    → {'score': 100000, 'structural': 100000, 'semantic': 100000, 'penalty': 0, ...}
```
A 2-element embedding against a 4-element constitution yields the **maximum score of
100000**.

**Reachability:** `ACTIVE`. Unlike D-1 and D-2 this requires no second language and no
future port. It is reachable today, in Python, from every caller, and it produces a
wrong-and-favourable result. `PoCAEvaluator.__init__` accepts any list; `evaluate()`
accepts any list; neither compares lengths, and `CONSTITUTION_DIM` is not referenced
anywhere in `core/evaluator.py`.

**Test status:** `UNTESTED`. Exhaustively:
- `core/test_ari.py` uses 3-element and 10-element vectors with matching lengths
  throughout; `test_cosine_similarity_calculation` (`:214`) passes `[100000,0,0]` against
  a 3-element `v2` supplied inline, never against `self.evaluator.constitution` (which is
  10-dim) — so even that test never exercises a mismatch.
- `core/test_integration.py` uses matching 16-dim vectors.
- `compliance` has no dedicated test module; `test_compliance.py` uses matching 1536-dim
  embeddings.
- **No test in the repository passes vectors of differing lengths to any similarity
  function.**

**Nature:** `ENGINEERING BUG` (primary), with a `NORMATIVE GAP` component:
- *Engineering aspect, independent of any normative choice:* `core/evaluator.py:32-38`
  documents the parameters as *"Pre-normalized int32 vectors (scaled by 10^5)"* and the
  return as *"range approximately [-10^5, 10^5]"*. A 2-element vector is not a
  pre-normalized 1536-dim vector, and the function accepts it and returns the maximal
  value. Silently scoring malformed input as perfectly aligned is a defect under any
  specification. `docs/GAP-001.md` does not record it.
- *Normative aspect:* whether a length mismatch must raise, must return a sentinel, or
  must be prevented upstream by a validation layer is undefined — `SPEC-002 REQ-002-031`
  lists "failure conditions" as a thing the future specification MUST define, and it is
  unresolved. So the *required* behaviour cannot be chosen here.

**Security-relevant note (recorded, not acted on):** this is the one finding of the three
with a direct integrity consequence. Because `ari` is the measurement the whole system
exists to produce, an input-shaping error that yields maximum score is a
fail-**open** behaviour. `docs/threat_model.md` was not found to address it (no mention of
dimension or length validation).

**Not fixed.**

---

## 2. Additional Determinism / Correctness Findings

Found during the same inspection. Recorded for completeness; none fixed.

### D-4 — Intermediate dot product exceeds int32; `int32` is a naming convention only

**Location:** `core/evaluator.py:41`, `compliance/consistency.py:96`.

The function is named `vector_similarity_int32` and the docstrings say "int32 vectors".
Python integers are arbitrary-precision; nothing constrains any value to 32 bits.

**Measured this session** for the documented 1536-dim case with all elements at the
scale bound `100000`:
```
dot          = 15,360,000,000,000      (1.536 × 10^13)
int32 max    =      2,147,483,647
dot > int32 max            → True
dot // 100000 = 153,600,000            (fits in int32)
```
So the **result** fits `i32`, but the **accumulator** requires at least `i64`. A direct
`i32` port overflows; in Rust debug builds it panics, in release builds it wraps.

Two further consequences observed:
- `evaluate()` has no upper clamp. Measured: `PoCAEvaluator([100000]*4).evaluate("a",
  [100000]*4, True)` → `{'ari': 310000, …}`, i.e. **3.1× the documented maximum** of
  100000, because the 4-element "unit" vectors are not actually unit vectors and nothing
  checks.
- `init.sql:47` constrains `RAW_ARI` to `BETWEEN 0 AND 100000`. An out-of-range `ari`
  would therefore be rejected at the database boundary — but only if a writer existed,
  and none does (`02_RUNTIME_DATAFLOW.md` §6). The invariant is declared where nothing
  enforces it and absent where the value is produced.

**Classification:** `LATENT` (no i32 implementation exists) / `UNTESTED` /
`NORMATIVE GAP` + `ENGINEERING BUG`.
`core/test_bitwise_replay.py:377-379` asserts a *hard-coded literal* `100000` is within
i32 range; it does not check any computed value. Nothing tests the accumulator width.
The normative component is `AD-CA-007` (numeric representation, unresolved).

### D-5 — `drift` code contradicts its own docstring

**Location:** `core/evaluator.py:85-90`.

Docstring: *"Clamp drift to [0, 100000] to represent [0.0, 1.0]"*.
Code: `drift = min(max(0, self.SCALING_FACTOR - sa), 2 * self.SCALING_FACTOR)`.

Measured: anti-aligned input yields `drift = 200000`, and the D-1 example yields
`drift = 100001`. Both exceed the documented range. `compliance/certificate.py` then
divides by 100000 for presentation, yielding `drift = 2.0` / `1.00001` on a field
documented as a `[0.0, 1.0]` ratio (verified: `to_dict()["ari"]` →
`{'score': 1.00001, 'drift': 1.00001, …}`).

**Classification:** `ACTIVE` / `UNTESTED` / `ENGINEERING BUG` (pure — no normative choice
is needed to observe that code and docstring disagree). `core/test_ari.py:137` asserts
only `drift < 5000` for the aligned case; `:165` asserts `drift > 30000`. No upper-bound
assertion exists.

### D-6 — No input validation at the Layer-0 boundary

**Location:** `core/evaluator.py:20-24` (`__init__`), `:51` (`evaluate`).

`PoCAEvaluator` accepts: vectors of any length, any magnitude, any element type
(including floats — `demo.py` does exactly this), `None`-free but otherwise unchecked
input. `ConsistencyCalculator` is stricter (`:82`, `:85`, `:88`) but still does not check
length.

Measured contrast:
```
ConsistencyCalculator([200000,0,0,0], []) → ValueError  ("must be normalized")
PoCAEvaluator([200000,0,0,0]).evaluate("a",[100000,0,0,0],True) → {'ari': 170000, ...}
```
Two engines in the same repository, same formula, opposite validation postures.

**Classification:** `ACTIVE` / `UNTESTED` / `ENGINEERING BUG` (the divergence between two
implementations of one formula is a defect regardless of which posture is correct) +
`NORMATIVE GAP` (which posture is *required* is undefined).

### D-7 — Three JSON canonicalizations for hash inputs

| Site | Form |
|---|---|
| `audit/merkle.py:89` | `sort_keys=True, separators=(",",":")` |
| `compliance/certificate.py:69` | `sort_keys=True`, **default separators** (`", "`, `": "`) |
| `core/merkle.py:8` | `sort_keys=True`, default separators |

The same logical object serialized through two of these paths produces different bytes
and therefore a different hash. There is no shared canonicalization module.
`docs/GAP-001.md` GAP-H3 records the absence of a canonical serialization module; it does
not record that three ad-hoc ones are in use.

**Classification:** `ACTIVE` (within Python) / `UNTESTED` (no test compares canonical
forms across sites) / `ENGINEERING BUG` + `NORMATIVE GAP` (`AD-CA-008` is unresolved, so
the *correct* canonical form cannot be chosen — but the *inconsistency* is an engineering
fact).

### D-8 — Merkle construction is not RFC 6962; odd nodes are duplicated

**Location:** `audit/merkle.py:157` (`right = current_level[i+1] if i+1 < len else left`).

The odd-node-duplication strategy is a known Merkle variant with a documented
second-preimage weakness (it permits distinct leaf multisets to yield the same root in
some shapes). Aura-Guard's Rust implementation uses RFC 6962 instead (`src/segment.rs:6`).
The two therefore compute different roots for the same leaves.

Recorded here as a determinism/interoperability observation, not as a vulnerability
claim: no cross-implementation Merkle verification currently occurs.

**Classification:** `LATENT` / `TESTED` (for its own behaviour —
`audit/test_audit.py:187` `test_odd_leaves_handled` asserts the duplication behaviour) /
`NORMATIVE GAP` (no specification selects a Merkle construction for this repository;
`docs/specs/AUDIT_LAYER_SPEC.md` describes the current one).

### D-9 — Timestamp non-determinism at the compliance boundary

`compliance/policy.py:88,113,123` use `datetime.utcnow()`. CHECK 5 (entropy) greps for
`datetime.now()` — not `utcnow()` — and only in `core/*.py`, so this is outside its
scope by two independent margins.

The values feed `KillSwitch` state reporting, not the measurement path, so no ARI is
affected. Recorded because CHECK 5's PASS should not be read as "no non-deterministic
time source anywhere".

**Classification:** `ACTIVE` (values differ per run) / `UNTESTED` / not a bug in the
measurement path; an **evidence-scope observation**. Also relevant: `datetime.utcnow()` is
deprecated as of Python 3.12.

---

## 3. Axis-by-Axis Summary (as requested by TASK 4)

| Axis | AS-IS state | Evidence |
|---|---|---|
| **Integer arithmetic** | Runtime path is integer-only. Arbitrary-precision, not width-bounded. Scale `10^5` declared independently in 4 modules. | `core/evaluator.py:19`, `compliance/consistency.py:20`, `compliance/policy.py:19`, `core/offline_normalizer.py:41` |
| **Float usage** | Confined to `core/offline_normalizer.py` (by design, CHECK 2-excluded), `compliance/certificate.py` (presentation, documented), `core/test_ari.py:25` (test helper). **Leaks:** `demo.py` passes floats into the int engine; `init.sql` stores `DECIMAL(3,2)`; `VectorRepository.ts` uses float cosine. | CHECK 2 passes; `demo.py:22`; `init.sql:16-17` |
| **Rounding** | Four coexisting rules: `round()` half-to-even (normalizer), floor `//` (evaluator, consistency), SQL half-up (`init.sql:60`), float division (certificate). No shared definition. | D-2 |
| **Division** | Floor (`//`) throughout the runtime path; float `/` in the offline normalizer. Diverges from truncating languages on negatives. | D-1 |
| **Overflow** | Impossible in CPython; the intermediate accumulator measured at 1.536×10¹³ exceeds i32. No width assertions on any computed value. | D-4 |
| **Signed/unsigned conversions** | None performed anywhere in production code. LE-signed 4-byte encoding exists only in test/CI code (`core/test_bitwise_replay.py:287`, `scripts/generate_determinism_report.py:65`). | §D-4 |
| **Vector dimensions** | `CONSTITUTION_DIM = 1536` enforced **only** in `core/offline_normalizer.py:171`. Not referenced by `core/evaluator.py` or `compliance/consistency.py`. `init.sql:96` declares `vector(32)`. | D-3 |
| **Serialization** | Three JSON canonicalizations; no canonical byte sequence in production code. | D-7 |
| **Hashing** | SHA-256 (`audit/merkle.py:16`), HMAC-SHA256 (`audit/signing.py:88`). Deterministic and cross-platform-verified by the CI determinism job. Merkle variant is non-RFC-6962. | D-8; `scripts/generate_determinism_report.py:107-113` |
| **Platform assumptions** | CI covers Linux x86_64 + Linux arm64, CPython 3.12 only. WASM is asserted by proxy (`WASMCompatibilityTest`), never executed — the workflow says so itself at `.github/workflows/execution-checks.yml:83-85`. No macOS, Windows, 32-bit, or alternative interpreter. | `01_CORE_INVENTORY.md` §15 |

---

## 4. Classification Roll-Up

| ID | Finding | Reach | Test | Nature |
|---|---|---|---|---|
| D-1 | `//` floor vs truncate | LATENT | UNTESTED | NORMATIVE GAP + ENGINEERING BUG (undocumented) |
| D-2 | `round()` half-to-even | LATENT | TESTED (locks current behaviour) | NORMATIVE GAP + ENGINEERING BUG (under-specified doc) |
| D-3 | `zip()` truncation | **ACTIVE** | UNTESTED | **ENGINEERING BUG** + NORMATIVE GAP (required failure mode undefined) |
| D-4 | i32 accumulator overflow / no upper clamp | LATENT | UNTESTED | NORMATIVE GAP + ENGINEERING BUG |
| D-5 | `drift` exceeds documented range | **ACTIVE** | UNTESTED | **ENGINEERING BUG** (pure) |
| D-6 | No Layer-0 input validation | **ACTIVE** | UNTESTED | ENGINEERING BUG + NORMATIVE GAP |
| D-7 | Three JSON canonicalizations | **ACTIVE** | UNTESTED | ENGINEERING BUG + NORMATIVE GAP |
| D-8 | Non-RFC-6962 Merkle | LATENT | TESTED | NORMATIVE GAP |
| D-9 | `datetime.utcnow()` outside CHECK 5 scope | ACTIVE | UNTESTED | evidence-scope observation |

**Three findings are pure or primarily engineering defects and can be addressed without
any governance decision: D-3, D-5, D-6.** They are carried forward to `09_SAFE_WORK.md`
with the caveat that *detecting and reporting* a malformed input is safe, while *choosing
what the system must do about it* is not.
