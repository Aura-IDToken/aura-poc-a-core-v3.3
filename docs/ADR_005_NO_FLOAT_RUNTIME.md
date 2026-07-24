# ADR-005: Removal of Float from Runtime Core

**Status:** APPROVED  
**Date:** 2026-01-23  
**Author:** Aura Protocol Core Team  
**Spec Version:** v3.3  

---

## Context

The Aura Protocol is a **regulatory measurement instrument** (not a software product) designed for the 2026 AI Regulatory Sandbox. As a metrological system, it must guarantee **bit-for-bit reproducibility** across all execution environments: x86, ARM, and WASM.

Floating-point arithmetic introduces **non-deterministic behavior** that violates this core requirement.

---

## Problem

### The Floating-Point Non-Determinism Issue

Floating-point operations (IEEE 754) produce **architecture-dependent results** due to:

1. **Different rounding modes** across CPU architectures
2. **FMA (Fused Multiply-Add)** availability varies (x86 vs ARM vs WASM)
3. **SIMD instruction sets** produce different intermediate results
4. **Compiler optimizations** reorder operations differently
5. **Register precision** varies (80-bit x87 vs 64-bit SSE)

**Example of non-determinism:**
```python
# Different platforms may compute floating-point operations differently:

# Example 1: Binary representation limitations
# (Same on all platforms, but demonstrates float imprecision)
result = 0.1 + 0.2  # Typically 0.30000000000000004 due to binary representation

# Example 2: FMA (Fused Multiply-Add) differences
# x86 with FMA enabled:
a, b, c = 0.5, 0.3, 0.2
result_fma = a * b + c  # Computed as single FMA operation: one rounding

# ARM without FMA (or FMA disabled):
result_no_fma = a * b + c  # Computed as multiply + add: two roundings
# result_fma ≠ result_no_fma (different bit patterns)

# Example 3: Compiler optimizations
# Depending on optimization flags, compilers may reorder operations:
x = (a + b) + c  # May be reordered to a + (b + c) with -fassociative-math
# Different parenthesization = different rounding = different bits
```

Even though these differences are tiny (typically in the last few bits), they produce **different bit patterns** in memory, which means **different SHA256 hashes**.

### Regulatory Requirement

For a metrological system used in regulatory compliance (AI Act Article 13), we MUST guarantee:

```
Same Input → Identical Bits → Identical Hash
```

This is impossible with floating-point arithmetic.

---

## Decision

**ELIMINATE ALL FLOATING-POINT OPERATIONS FROM RUNTIME CORE**

### Implementation: Fixed-Point Arithmetic

Replace all float operations with **int32 fixed-point arithmetic** using a scaling factor of **10^5**.

#### DET_01: Offline Normalization (Float Allowed)

**File:** `core/offline_normalizer.py`

**Purpose:** Pre-process constitution vectors offline before deployment.

**Allowed operations:**
- ✅ Floating-point math (math.sqrt, division, etc.)
- ✅ L2 normalization: `v_normalized = v / ||v||`
- ✅ Fixed-point scaling: `v_int = round(v_float × 10^5)`

**Output:** Deterministic int32 JSON file

**Justification:** This runs ONCE offline, not in production runtime. The output is stored and reused, so slight platform differences during preprocessing don't matter—only the final int32 output matters.

#### DET_02: Runtime Fixed-Point Operations (No Float)

**Files:** Runtime core (`core/evaluator.py`, `core/consistency.py`, etc.)

**Prohibited operations:**
- ❌ Float arithmetic (`+`, `-`, `*`, `/` on floats)
- ❌ `math.sqrt`, `math.pow`, `math.exp`
- ❌ NumPy operations (introduces BLAS non-determinism)
- ❌ Any implicit float casting

**Allowed operations:**
- ✅ Integer addition: `a + b` (int32)
- ✅ Integer subtraction: `a - b` (int32)
- ✅ Integer multiplication: `(a * b) // SCALING_FACTOR` (rescale after multiply)
- ✅ Bit shifts for division by powers of 2
- ✅ Comparison operators (`<`, `>`, `==`)

**Scaling Factor:** `10^5 = 100,000`

**Example:**
```python
# OLD (non-deterministic):
similarity = 0.85
threshold = 0.8
if similarity > threshold:
    pass

# NEW (deterministic):
similarity_int = 85000  # 0.85 × 10^5
threshold_int = 80000   # 0.8 × 10^5
if similarity_int > threshold_int:
    pass
```

---

## Rationale

### 1. **Bit-Identity Guarantee**

Integer operations produce **identical results** on all platforms:
- x86, ARM, WASM all use two's complement for signed integers
- Integer addition/subtraction/multiplication are deterministic
- Integer division (`//`) is deterministic (truncation toward zero)

### 2. **Regulatory Compliance (AI Act Art. 13)**

Regulators can **independently verify** our computations:
```bash
# Regulator runs the SAME input through our system
# Expected: IDENTICAL output hash

$ python core/evaluator.py input.json
Output hash: a3f2c9b1...

# On ANY platform (x86, ARM, WASM):
Output hash: a3f2c9b1...  # MUST match
```

### 3. **Metrological System Requirements**

As a measurement instrument, we must meet **metrological standards**:
- **Reproducibility:** Same measurement repeated → same result
- **Traceability:** Each result can be traced to input data
- **Verification:** Independent third parties can verify results

Floating-point operations violate **reproducibility**.

### 4. **Zero Trust Model**

The Krasinski Principle states: **T ∝ 1/S** (Transparency inversely proportional to Secrecy)

Floating-point non-determinism is a form of **hidden entropy (S)**:
- You cannot predict exact bit-level output
- Different platforms produce different results
- This reduces **transparency (T)**

Integer arithmetic eliminates this entropy source.

---

## Mapping to Determinism Requirements

### DET_01: Offline Preprocessing

**Policy:** Float operations ALLOWED (runs once offline)

**Scope:**
- `core/offline_normalizer.py`
- Pre-deployment constitution vector generation
- Test data generation

**Output:** Deterministic int32 JSON

**Verification:**
```bash
# Run normalizer
$ python core/offline_normalizer.py input_float.json output_int32.json

# Output is ALWAYS the same int32 vector
$ sha256sum output_int32.json
# Hash is deterministic
```

### DET_02: Runtime Execution

**Policy:** Float operations PROHIBITED (zero-float runtime)

**Scope:**
- `core/evaluator.py` - ARI calculation
- `core/consistency.py` - Consistency checking
- `core/policy.py` - Policy enforcement
- `core/merkle.py` - Cryptographic hashing
- All runtime components

**Arithmetic:** Fixed-point int32 only (scaling: 10^5)

**Verification:**
```bash
# Run test suite
$ python -m unittest core.test_bitwise_replay

# Verifies:
# - No float operations in runtime
# - Bit-identical results on repeated runs
# - Cross-platform hash matching (x86, ARM, WASM)
```

---

## WASM Considerations

### TASK-04: WASM Quantizer (Future)

**Directory:** `core/wasm_quantizer/` (OPTIONAL)

**Requirements:**
- Implement DET_02 in WebAssembly
- Use `i32` and `i64` types only (no `f32`/`f64`)
- No SIMD instructions (platform-dependent)
- No FMA instructions (platform-dependent)
- Bit-identical results with Python implementation

**Purpose:** Enable browser-based regulatory verification

**Status:** OPTIONAL for v3.3 (Python-only is sufficient)

---

## Consequences

### Positive

✅ **Guaranteed bit-identity** across x86, ARM, WASM  
✅ **Regulatory compliance** (AI Act Art. 13 transparency)  
✅ **Metrological validity** (reproducible measurements)  
✅ **Cryptographic auditability** (hash-based verification)  
✅ **Zero hidden entropy** (Krasinski Principle: maximize T)  

### Negative

⚠️ **Precision loss** compared to float (but acceptable for our use case)  
⚠️ **Manual scaling** required for all operations  
⚠️ **Complexity** in implementation (need to manage scaling factors)  

### Mitigation

The precision loss is **acceptable** because:
- Constitution vectors are semantic embeddings (approximate by nature)
- Threshold is 0.8 → 80,000 in fixed-point (precise enough)
- Error margin of ±0.00001 (1 unit in 10^5) is negligible for ARI calculation

---

## Verification

### TASK-03: Bitwise Replay Test

**File:** `core/test_bitwise_replay.py`

**Purpose:** Verify DET_02 compliance

**Tests:**
1. ✅ Integer addition determinism
2. ✅ Integer multiplication with rescaling
3. ✅ Vector dot product (int-only)
4. ✅ Constitution vector hashing
5. ✅ Replay determinism (same input → same output)
6. ✅ Cross-platform reference hashing
7. ✅ No float contamination
8. ✅ Byte-level bit-identity
9. ✅ Platform hash record generation
10. ✅ WASM compatibility checks

**Execution:**
```bash
$ python -m unittest core.test_bitwise_replay -v

# Expected output:
# ======================================================================
# BITWISE REPLAY TEST - Platform: x86_64
# ======================================================================
# test_int32_fixed_point_addition ... ok
# test_constitution_vector_hash ... ok
# [...]
# Ran 11 tests in 0.013s
# OK
```

**Reference Hash (x86_64 baseline):**
```json
{
  "platform": {
    "machine": "x86_64",
    "architecture": "64bit"
  },
  "test_vector_hash": "de563725627d2a2ccd96a2c00095a8eeea00b2e580c396145661455e4e516cd0",
  "test_vector_length": 1000,
  "scaling_factor": 100000,
  "spec_version": "v3.3"
}
```

**Note:** The test `test_cross_platform_reference_hash` in `core/test_bitwise_replay.py` 
uses a hardcoded baseline hash to verify that all platforms produce identical results.
The baseline was established on x86_64 and serves as the reference for ARM and WASM builds.

---

## Alternatives Considered

### Alternative 1: Use decimal.Decimal

**Pros:** Deterministic decimal arithmetic  
**Cons:** 
- ❌ Not available in WASM
- ❌ 10x-100x slower than int32
- ❌ Still not truly bit-identical across Python versions

**Rejected:** WASM incompatibility is a blocker.

### Alternative 2: Use Fixed-Point Library

**Pros:** Existing implementation  
**Cons:**
- ❌ Additional dependency
- ❌ Not in stdlib (harder to audit)
- ❌ May have platform-specific optimizations

**Rejected:** Prefer zero-dependency int32 for auditability.

### Alternative 3: Document Float Non-Determinism

**Pros:** No code changes needed  
**Cons:**
- ❌ Violates metrological requirements
- ❌ Fails AI Act Art. 13 (not reproducible)
- ❌ Cannot be independently verified

**Rejected:** Unacceptable for regulatory compliance.

---

## Implementation Status

### Completed (v3.3)

✅ **TASK-01:** `core/offline_normalizer.py` (DET_01)  
✅ **TASK-02:** `packages/zk-passport/reputation_check.circom` (integer-only ZK)  
✅ **TASK-03:** `core/test_bitwise_replay.py` (verification)  
✅ **TASK-05:** `docs/ADR_005_NO_FLOAT_RUNTIME.md` (this document)  

### Optional (Future)

⏸️ **TASK-04:** `core/wasm_quantizer/` (WASM implementation)

---

## References

- **Copilot Directive:** `.github/copilot-instructions.md`
- **Mathematical Foundation:** `docs/mathematical_foundation.md`
- **Regulatory Compliance:** `docs/regulatory_compliance.md`
- **Offline Normalizer:** `core/offline_normalizer.py`
- **Bitwise Replay Test:** `core/test_bitwise_replay.py`
- **AI Act Article 5:** Human profiling prohibition
- **AI Act Article 13:** Transparency and traceability requirements
- **IEEE 754:** Floating-point standard (deliberately NOT used in runtime)

---

## Conclusion

**Floating-point operations are BANNED from runtime core.**

This is not a performance optimization. This is not a coding preference.

**This is a regulatory requirement.**

The Aura Protocol is a **frozen regulatory measurement instrument**. Bit-for-bit reproducibility is **non-negotiable**.

Same input → Identical bits on x86 / ARM / WASM.

**Any nondeterminism = CRITICAL FAILURE.**

---

**Status:** FROZEN (MC-READY 2026)  
**Enforcement:** Automated tests (`test_bitwise_replay.py`)  
**Compliance:** AI Act Article 13 (Transparency & Traceability)
