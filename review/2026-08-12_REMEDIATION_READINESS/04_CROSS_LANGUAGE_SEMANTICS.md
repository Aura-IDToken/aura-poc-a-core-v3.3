# 04 — CROSS-LANGUAGE SEMANTICS REGISTER

**Date:** 2026-08-12
**Mode:** READ-ONLY. **No canonical behaviour is chosen anywhere in this document.**
**Normative effect:** NONE.

---

## §1 Evidence Status — Read This First

The task asks for a comparison of **current behaviour** in Python, Rust, JS/TS and C/C++.
The honest state of the evidence is:

| Language | Present in the ecosystem? | Implements the affected arithmetic? |
|---|---|---|
| **Python** | `aura-poc-a-core-v3.3` | **YES — the only implementation** |
| **Rust** | `aura-guard-v1.3` | **NO.** Verified this session: zero occurrences of `constitution`, `ari`, `poca`. Guard implements **no vector arithmetic, no rounding of scaled integers, and no paired-sequence iteration.** |
| **JS/TS** | `packages/database-client/VectorRepository.ts` | **NO** — uses **float** cosine distance; unbuildable (no `package.json`, no `tsconfig.json`, no lockfile, no importer); zero callers |
| **C/C++** | — | **Absent from the ecosystem entirely** |

**Therefore the Rust, JS/TS and C/C++ columns in every table below are LANGUAGE
SEMANTICS, not repository evidence.** They state what those languages' standard operators
do, and are included because they are the semantics any future port would inherit. They
are **not** observations of Aura code, because no such Aura code exists.

This distinction is marked in every row. Conflating the two would manufacture evidence.

**Consequence for classification.** This is precisely why `04_DETERMINISM_AUDIT.md`
classifies the division and rounding findings as **LATENT** rather than **ACTIVE**: they are
real properties of the Python code with **no second implementation to diverge from**. They
become ACTIVE the moment any port or FFI boundary is introduced — which is the ordering
trap recorded in `08` §6.

---

## §2 Divergence Register

Format as required by the task. **`DECISION REQUIRED` is filled in for every row; no row
selects a canonical behaviour.**

---

### XL-01 — Integer division, negative dividend

| Field | Content |
|---|---|
| **INPUT** | `dot = -1`, `-99999`, `-100000`, `-100001`, `-150000`; divisor `100000` |
| **PYTHON** | **`-1`, `-1`, `-1`, `-2`, `-2`** — floors toward −∞. *Executed this session, `core/evaluator.py:46`.* |
| **RUST** | `0`, `0`, `-1`, `-1`, `-1` — `i64` `/` truncates toward zero. *Language semantics; no Aura Rust code implements this.* |
| **JS/TS** | `0`, `0`, `-1`, `-1`, `-1` via `Math.trunc(a/b)`. *Language semantics.* Note `Math.floor` would match Python — **the divergence depends on which idiom a porter chooses**, which is itself unspecified. |
| **C/C++** | `0`, `0`, `-1`, `-1`, `-1` — truncation toward zero, mandated since C99 / C++11. *Language semantics.* |
| **CURRENT TEST COVERAGE** | **NONE.** No test asserts an exact value for a negative dot product. `core/test_ari.py:230-235` asserts only `sim3 < -90000` — a bound that passes identically under either rule. `core/test_bitwise_replay.py` never calls `PoCAEvaluator`. The determinism report computes no ARI. |
| **NORMATIVE STATUS** | **UNREGISTERED.** Verified at primary source this session: `SPEC-002 §6 AD-CA-007`'s candidate set is `32`, `100000`, `signed int32`, `little-endian`, `Dictionary-Based Embedding`, `round-half-to-even`. **No division rule appears — not as a decision, not as a candidate.** Tracked only as NB-016, in the engineering baseline. |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED** — integer-division semantics for negative dividends. **Not chosen here.** |

**Propagated effect (executed):** `PoCAEvaluator([-100000,0,0,0]).evaluate("a",[1,0,0,0],True)`
→ `{'ari': 29999, 'drift': 100001}`. A truncating implementation yields
`{'ari': 30000, 'drift': 100000}`. The 1-LSB difference propagates into **both** outputs.

---

### XL-02 — Rounding at `.5` boundaries

| Field | Content |
|---|---|
| **INPUT** | `0.5`, `1.5`, `2.5`, `3.5`, and negatives |
| **PYTHON** | **`0`, `2`, `2`, `4`; `-0.5→0`, `-1.5→-2`, `-2.5→-2`** — half-to-even (banker's). *Executed this session, `core/offline_normalizer.py:88`.* |
| **RUST** | `1`, `2`, `3`, `4`; `-1`, `-2`, `-3` — `f64::round()` is half-away-from-zero. *Language semantics.* |
| **JS/TS** | `1`, `2`, `3`, `4`; `-0`, `-1`, `-2` — `Math.round` is half toward +∞. **Differs from Rust on negatives.** *Language semantics.* |
| **C/C++** | `1`, `2`, `3`, `4`; `-1`, `-2`, `-3` — `round()` is half-away-from-zero. *Language semantics.* |
| **CURRENT TEST COVERAGE** | **PRESENT BUT HAZARDOUS.** `core/test_offline_normalizer.py:97-107` (`test_scale_to_fixed_point_rounding`) asserts against Python's present behaviour. It **locks in half-to-even without a specification to verify against**. No test covers an exact `.5` boundary in a way that reveals the cross-language issue; no test covers negative half-values. Flagged as an accidental-authority risk in `09`. |
| **NORMATIVE STATUS** | **UNRESOLVED, candidate only.** `AD-CA-007` lists `round-half-to-even`; `SPEC-002:371` — *"No candidate choice listed in this table constitutes a recommendation, preference, default, or implied architectural decision."* |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED** — rounding rule at float→int reduction. **Not chosen here.** The implementation exhibiting a candidate's behaviour is **not** evidence the candidate was selected. |

**Consequence, executed:** `[5e-6, 1.5e-5, 2.5e-5]` → Python `[0,2,2]`, Rust `[1,2,3]`,
JS `[1,2,3]`. **Three different Constitution Vectors from one input.** Since the CI
determinism report's `ari_vector_hash` is a hash of this output, **the CI vector is itself
rounding-dependent.**

---

### XL-03 — Overflow / accumulator width

| Field | Content |
|---|---|
| **INPUT** | 1536-dimensional dot product, all elements at the scale bound `100000` |
| **PYTHON** | **`15,360,000,000,000`** — computed exactly; arbitrary precision, **no overflow possible**. *Executed this session.* |
| **RUST** | `i32`: **overflow** — panics in debug builds, wraps in release. `i64`: exact. *Language semantics.* |
| **JS/TS** | `Number` is IEEE-754 double: `1.536e13` < `2^53`, so exact **here** — but silently lossy above `2^53`, with no error. `BigInt` would be exact. *Language semantics.* |
| **C/C++** | `int32_t`: **undefined behaviour** on signed overflow. `int64_t`: exact. *Language semantics.* |
| **CURRENT TEST COVERAGE** | **NONE for computed values.** `core/test_bitwise_replay.py:377-379` asserts a hard-coded literal `100000` is within `i32` range. Nothing tests the accumulator width. |
| **NORMATIVE STATUS** | **UNRESOLVED.** `AD-CA-007` lists `signed int32` as a **candidate only**. |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED** — integer width for values **and** for intermediate accumulators, plus overflow behaviour (prohibited / wrapping / saturating / checked). **Not chosen here.** |

**Structural note.** The functions are *named* `..._int32` and the docstrings say "int32
vectors", but nothing constrains any value to 32 bits. **The accumulator exceeds `i32` by
≈7154×.** The result (`153,600,000`) fits; the accumulator does not. A naive `i32` port is
therefore incorrect on the documented dimension — and **the reference implementation cannot
demonstrate the behaviour that must be specified**, because CPython cannot overflow.

---

### XL-04 — Integer width and representation

| Field | Content |
|---|---|
| **INPUT** | any vector element |
| **PYTHON** | **Arbitrary precision.** No width, no wraparound, no representation guarantee. The `int32` in function names is a **naming convention only**. *Verified at source.* |
| **RUST** | Explicit and checked: `i32`/`i64` chosen at the type level. *Language semantics.* |
| **JS/TS** | `Number` is a double — integers exact only to `2^53`; `| 0` coerces to int32 with wraparound. *Language semantics.* |
| **C/C++** | Platform-dependent (`int` is 32-bit on common ABIs but not guaranteed); `int32_t` is explicit. *Language semantics.* |
| **CURRENT TEST COVERAGE** | **NONE.** |
| **NORMATIVE STATUS** | **UNRESOLVED** — `AD-CA-007`, candidate `signed int32`. |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED.** **Not chosen here.** |

---

### XL-05 — Negative arithmetic beyond division

| Field | Content |
|---|---|
| **INPUT** | negative `SA` flowing through the weighted sum and drift |
| **PYTHON** | `raw_ari = max(0, (30000*si)//100000 + (70000*sa)//100000)` — **lower clamp only**, applied *after* the weighted sum. `drift = min(max(0, 100000 - sa), 200000)`. *Verified at source, `core/evaluator.py:75-86`.* |
| **RUST / JS / C** | Would differ **only** via XL-01 (the `//` sites). The clamp expressions themselves port directly. *Language semantics.* |
| **CURRENT TEST COVERAGE** | **PARTIAL.** `core/test_ari.py:137` asserts `drift < 5000`; `:165` asserts `drift > 30000`. **No upper-bound assertion exists anywhere.** |
| **NORMATIVE STATUS** | **UNDEFINED.** Whether negative similarity is admissible, and whether the `max(0, …)` floor is a measurement statement or a presentation choice, is unspecified (AG-08). |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED** — admissibility and meaning of negative values. **Not chosen here.** |

---

### XL-06 — Serialization

| Field | Content |
|---|---|
| **INPUT** | any object destined for a hash input |
| **PYTHON** | **Three coexisting forms.** `audit/merkle.py:89` compact `separators=(",",":")`; `compliance/certificate.py:69` defaults; `core/merkle.py:8` defaults. Executed: `{"a":[1,2],"b":1}` vs `{"a": [1, 2], "b": 1}` — **different bytes, different SHA-256**. |
| **RUST** | Guard uses **no JSON at all** in its digest: `chain.rs:36-47` joins nine values with `"\|"`. Its on-disk record uses `serde_json::to_string` with **no canonicalization step and no field-order normalization** (`log_writer.rs:96`). *Verified at source this session.* |
| **JS/TS** | `JSON.stringify` does **not** sort keys and preserves insertion order — a fourth form. *Language semantics.* |
| **C/C++** | No standard JSON; library-dependent. |
| **CURRENT TEST COVERAGE** | **NONE.** No test compares canonical forms across sites. |
| **NORMATIVE STATUS** | **UNRESOLVED, "None approved"** — `AD-CA-008`, verified at `SPEC-002:382`. Note the Conformance Kit declares a dependency on `jcs` (RFC 8785 JSON Canonicalization) which is **never imported** — declared in anticipation, not in use. |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED** — canonical serialization format and canonical byte sequence. **Not chosen here.** Recording the divergence is safe; unifying the three forms is **not**. |

---

### XL-07 — Byte ordering

| Field | Content |
|---|---|
| **INPUT** | an integer vector reduced to bytes |
| **PYTHON** | **No canonical encoding exists in production code.** The only integer encoding in the repository is LE-signed 4-byte, and it appears solely in test/CI code (`core/test_bitwise_replay.py:287`, `scripts/generate_determinism_report.py:65`). Runtime observed: `sys.byteorder == 'little'`. |
| **RUST** | Explicit per call site (`to_le_bytes` / `to_be_bytes`). Guard's digest is **text**, not binary, so byte order does not arise there. *Verified at source.* |
| **JS/TS** | `DataView`/`TypedArray`; platform-native unless specified. |
| **C/C++** | Platform-native; no guarantee. |
| **CURRENT TEST COVERAGE** | Indirect only — via the determinism report's cross-platform comparison, which covers the **normalizer**, not the evaluator. |
| **NORMATIVE STATUS** | **UNRESOLVED** — `AD-CA-007` lists `little-endian` as a **candidate only**. |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED.** **Not chosen here.** |

**Observation of consequence.** Because the only byte encoding lives in **test/CI code**,
the CI determinism comparison is verifying an encoding that **production never uses**. A
future normative encoding decision would not automatically be reflected by the existing
job.

---

### XL-08 — Hashing input construction

| Field | Content |
|---|---|
| **INPUT** | the preimage assembled before `SHA-256` |
| **PYTHON** | **JSON text**, three variants (XL-06). Merkle: `sha256(left + right)` with **no domain separation** (`audit/merkle.py:157`); odd nodes **duplicated**, not RFC 6962. |
| **RUST** | **Pipe-joined text**, nine fields, `SEP = "\|"` (`chain.rs:20,36-47`). Merkle: **RFC 6962** with `0x00`/`0x01` domain-separation prefixes (`merkle.rs:29-34`, `segment.rs:6`). *Verified at source this session.* |
| **JS/TS** | Not implemented. |
| **C/C++** | Not implemented. |
| **CURRENT TEST COVERAGE** | Each side tests **its own** construction. `audit/test_audit.py:187` asserts the duplication behaviour. **No cross-implementation comparison exists** — and none can, since the two constructions are incompatible by design. |
| **NORMATIVE STATUS** | **UNRESOLVED.** Hash domains: `AD-CA-008`, "None approved". Merkle construction: **selected by no specification**; tracked as NB-018. |
| **DECISION REQUIRED** | **ARCHITECTURAL DECISION REQUIRED** — hash domains, domain separation, and Merkle construction. **Not chosen here.** |

**The sharpest cross-implementation fact in the register.** The two implementations compute
**different Merkle roots for the same leaves** — Python duplicates odd nodes, Rust follows
RFC 6962. The Python variant carries a documented second-preimage weakness. This is
recorded as a determinism/interoperability observation, **not** as a vulnerability claim:
no cross-implementation Merkle verification currently occurs.

---

## §3 Summary Matrix

| ID | Axis | Python evidence | Second impl. exists? | Test coverage | Normative status |
|---|---|---|---|---|---|
| XL-01 | Integer division | **executed** | no | **none** | **unregistered** |
| XL-02 | Rounding | **executed** | no | present but **locks in a candidate** | candidate only |
| XL-03 | Overflow | **executed** | no | **none** | candidate only |
| XL-04 | Integer width | verified | no | **none** | candidate only |
| XL-05 | Negative arithmetic | verified | no | partial (bounds only) | undefined |
| XL-06 | Serialization | **executed** | Guard: different model | **none** | "None approved" |
| XL-07 | Byte ordering | verified | Guard: N/A | indirect, wrong subsystem | candidate only |
| XL-08 | Hash construction | verified | **yes — and incompatible** | per-side only | unresolved |

**Eight axes. Zero canonical behaviours selected. Zero decided normatively.**

## §4 Structural Observations

**1. The register has one implementation, not four.** Every "divergence" is a divergence
between Python and *language semantics a port would inherit*. This is a **prospective**
register, and it is more valuable for that: it enumerates what will break **before**
anything is built, rather than after.

**2. Test coverage is near-zero exactly where divergence is highest.** XL-01 and XL-03 —
the two axes that would break a Rust port immediately — have **no test coverage at all**.
XL-02 has coverage that *entrenches* an unapproved candidate.

**3. The one axis with two implementations is already incompatible.** XL-08: Python and
Rust compute different Merkle roots. Neither is specified. This is what a cross-language
conformance failure looks like when it is allowed to develop unobserved.

**4. Ordering trap.** Building the second implementation is what makes XL-01…XL-05 ACTIVE.
Building it *before* the decisions exist would not surface a divergence to be resolved — it
would create a second set of implementation-derived behaviours competing for authority.
See `08` §6.

## §5 What This Document Does Not Do

Does not choose canonical behaviour on any axis. Does not recommend a language's semantics.
Does not assert Python's behaviour is right or wrong. Does not create an ADR, amend
SPEC-002, or modify code. Does not present language semantics as Aura evidence.

---

*This document has no normative effect. It records divergence surfaces and selects none.*
