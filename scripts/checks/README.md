# Execution Checks

This directory contains mandatory execution checks for the Aura Protocol core.

## Overview

Every change to the repository **MUST** pass all 5 execution checks defined in `.github/copilot-checks.md`.

**If any check fails: DO NOT MERGE**

## Running the Checks

### Run All Checks (Recommended)

```bash
./scripts/run_all_checks.sh
```

This will run all 5 checks in sequence and provide a summary.

### Run Individual Checks

```bash
# CHECK 1 - Bit Identity
./scripts/checks/check_1_bit_identity.sh

# CHECK 2 - Integer Only
./scripts/checks/check_2_integer_only.sh

# CHECK 3 - Layer Separation
./scripts/checks/check_3_layer_separation.sh

# CHECK 4 - Audit Path
./scripts/checks/check_4_audit_path.sh

# CHECK 5 - Entropy
./scripts/checks/check_5_entropy.sh
```

## The 5 Checks

### CHECK 1 — Bit Identity

**Requirement:** Tests must produce identical hashes on x86 and ARM platforms.

**What it does:**
- Runs bitwise replay tests (`core/test_bitwise_replay.py`)
- Verifies deterministic computation across platforms
- Ensures bit-for-bit reproducibility

**Pass criteria:** All tests pass, platform hashes are available for comparison.

**Why it matters:** As a regulatory measurement instrument, the system MUST produce identical results across all platforms.

### CHECK 2 — Integer Only

**Requirement:** No float/sqrt/numpy in runtime core.

**What it does:**
- Scans `core/` directory for prohibited operations
- Excludes `offline_normalizer.py` (allowed for preprocessing)
- Excludes test files

**Prohibited in runtime core:**
- `float` type annotations or operations
- `math.sqrt` or similar floating-point math
- `numpy` (introduces BLAS nondeterminism)

**Pass criteria:** Zero matches found.

**Why it matters:** Floating-point operations are nondeterministic across platforms. Only integer arithmetic guarantees bit-identity.

### CHECK 3 — Layer Separation

**Requirement:** `core/` must ONLY measure, not decide.

**What it does:**
- Checks for compliance status returns (COMPLIANT, RISK, etc.)
- Checks for threshold enforcement
- Checks for business logic

**Prohibited in core/:**
- Status fields returning "COMPLIANT" or "RISK"
- Threshold definitions (e.g., `COMPLIANCE_THRESHOLD`)
- Allow/deny logic
- Business rules

**Pass criteria:** Core returns RAW METRICS only (ARI score, drift value).

**Why it matters:** Layer 0 (core/) MEASURES. Layer 2 (compliance/) DECIDES. Mixing these violates architectural separation.

### CHECK 4 — Audit Path

**Requirement:** Every metric must be traceable to integer math, Merkle leaf, and audit record.

**What it does:**
- Verifies `core/merkle.py` exists
- Verifies Merkle leaf/hash functions exist
- Verifies integration tests exist
- Cross-references with CHECK 2 (integer-only)

**Pass criteria:** All audit path components are present and functional.

**Why it matters:** AI Act Article 13 requires transparency and traceability. Every output must be provably derived from inputs.

### CHECK 5 — Entropy

**Requirement:** Changes must not increase system entropy (nondeterminism).

**What it does:**
- Checks for nondeterministic operations (random, time.time(), uuid, etc.)
- Checks for network calls (external dependencies)
- Reports entropy indicators (SLOC, modules, dependencies)

**Prohibited operations:**
- `random`, `time.time()`, `datetime.now()`
- `uuid`, `os.urandom`
- Network calls (`requests`, `urllib`, `socket`)

**Pass criteria:** Zero nondeterministic operations found.

**Why it matters:** Krasinski Principle: T ∝ 1/S (Transparency inversely proportional to Entropy). Minimize entropy for maximum transparency.

## CI Integration

These checks should be integrated into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run Execution Checks
  run: ./scripts/run_all_checks.sh
```

## Expected Status

**Current Status:**
- CHECK 1: ✅ PASS (bitwise replay tests working)
- CHECK 2: ❌ FAIL (float operations in runtime core)
- CHECK 3: ❌ FAIL (compliance status in evaluator.py)
- CHECK 4: ✅ PASS (audit path components verified)
- CHECK 5: ✅ PASS (no entropy increase)

**Known Violations:**

The following files currently violate the checks and need remediation:

1. `core/evaluator.py` - Uses float types and math.sqrt (CHECK 2)
2. `core/evaluator.py` - Returns compliance status (CHECK 3)
3. `core/consistency.py` - Uses math.sqrt (CHECK 2)
4. `core/embedding.py` - Uses float operations (CHECK 2)
5. `core/policy.py` - Uses float types, enforces thresholds (CHECK 2, CHECK 3)

## Remediation

To fix the violations:

### For CHECK 2 (Integer Only)

Replace all float operations with int32 fixed-point arithmetic:

```python
# BEFORE (violates CHECK 2)
similarity = 0.85
norm = math.sqrt(sum(x**2 for x in vector))

# AFTER (complies with CHECK 2)
similarity_int = 85000  # 0.85 × 10^5
# For norm: use integer-only approximation or pre-computed values
```

### For CHECK 3 (Layer Separation)

Remove compliance decisions from core, return raw metrics only:

```python
# BEFORE (violates CHECK 3)
return {
    "ari": 0.85,
    "status": "COMPLIANT" if ari > 0.8 else "RISK"
}

# AFTER (complies with CHECK 3)
return {
    "ari": 85000,  # Raw metric in int32
    "drift": 15000
}
# Let Layer 2 (compliance/) decide COMPLIANT vs RISK
```

## Reference

- Copilot Directive: `.github/copilot-instructions.md`
- Execution Checks: `.github/copilot-checks.md`
- ADR-005: `docs/ADR_005_NO_FLOAT_RUNTIME.md`
- Mathematical Foundation: `docs/mathematical_foundation.md`
