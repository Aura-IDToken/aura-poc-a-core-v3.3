# Test Specification: Reputation Check Circuit

## Overview

This document specifies test cases for the `reputation_check.circom` ZK circuit to ensure compliance with v3.3 specification requirements.

## Test Setup

### Prerequisites
- circom compiler (v2.1.0 or higher)
- snarkjs for proof generation and verification
- Node.js environment

### Compilation
```bash
circom reputation_check.circom --r1cs --wasm --sym
```

## Test Cases

### Test 1: Valid Proof - Above Threshold

**Purpose**: Verify that a valid MACHINE_ACCOUNT with ARI above threshold produces a valid proof.

**Inputs**:
```json
{
  "secretARI": "85000",        // 0.85 ARI (private)
  "isMachine": "1",            // Valid MACHINE_ACCOUNT
  "schemaIntegrity": "1",      // Valid structure
  "threshold": "80000"         // 0.8 threshold (public)
}
```

**Expected Output**:
- `isVerified = 1`
- Proof generation succeeds
- Proof verification succeeds

**Rationale**: 85000 ≥ 80000, all constraints satisfied

---

### Test 2: Valid Proof - Equal to Threshold

**Purpose**: Verify that ARI exactly equal to threshold is accepted (≥ operator).

**Inputs**:
```json
{
  "secretARI": "80000",        // 0.8 ARI (private)
  "isMachine": "1",
  "schemaIntegrity": "1",
  "threshold": "80000"         // 0.8 threshold (public)
}
```

**Expected Output**:
- `isVerified = 1`
- Proof generation succeeds
- Proof verification succeeds

**Rationale**: 80000 ≥ 80000 is true (edge case)

---

### Test 3: Invalid Proof - Below Threshold

**Purpose**: Verify that ARI below threshold produces invalid proof.

**Inputs**:
```json
{
  "secretARI": "75000",        // 0.75 ARI (private)
  "isMachine": "1",
  "schemaIntegrity": "1",
  "threshold": "80000"         // 0.8 threshold (public)
}
```

**Expected Output**:
- `isVerified = 0`
- Proof generation succeeds
- Proof verification succeeds (but isVerified = 0)

**Rationale**: 75000 < 80000, circuit correctly outputs 0

---

### Test 4: Constraint Failure - Not a Machine Account

**Purpose**: Verify Art. 5 compliance - reject non-MACHINE_ACCOUNT entities.

**Inputs**:
```json
{
  "secretARI": "85000",
  "isMachine": "0",            // INVALID: Not a MACHINE_ACCOUNT
  "schemaIntegrity": "1",
  "threshold": "80000"
}
```

**Expected Output**:
- Constraint failure: `isMachine === 1` violated
- Proof generation fails
- Circuit rejects computation

**Rationale**: EU AI Act Article 5 - prohibits human profiling

---

### Test 5: Constraint Failure - Schema Integrity Error

**Purpose**: Verify that structural errors prevent validation.

**Inputs**:
```json
{
  "secretARI": "85000",
  "isMachine": "1",
  "schemaIntegrity": "0",      // INVALID: Structural error
  "threshold": "80000"
}
```

**Expected Output**:
- Constraint failure: `schemaIntegrity === 1` violated
- Proof generation fails
- Circuit rejects computation

**Rationale**: v3.3 rigor - structural errors block validation

---

### Test 6: Boundary Case - Maximum ARI

**Purpose**: Verify circuit handles maximum scaled ARI (1.0 = 100000).

**Inputs**:
```json
{
  "secretARI": "100000",       // 1.0 ARI (maximum)
  "isMachine": "1",
  "schemaIntegrity": "1",
  "threshold": "80000"
}
```

**Expected Output**:
- `isVerified = 1`
- Proof generation succeeds
- Proof verification succeeds

**Rationale**: 100000 ≥ 80000, perfect ARI score

---

### Test 7: Boundary Case - Minimum ARI

**Purpose**: Verify circuit handles minimum scaled ARI (0.0 = 0).

**Inputs**:
```json
{
  "secretARI": "0",            // 0.0 ARI (minimum)
  "isMachine": "1",
  "schemaIntegrity": "1",
  "threshold": "80000"
}
```

**Expected Output**:
- `isVerified = 0`
- Proof generation succeeds
- Proof verification succeeds (but isVerified = 0)

**Rationale**: 0 < 80000, complete misalignment

---

### Test 8: High Threshold

**Purpose**: Verify circuit with strict threshold (0.95).

**Inputs**:
```json
{
  "secretARI": "96000",        // 0.96 ARI
  "isMachine": "1",
  "schemaIntegrity": "1",
  "threshold": "95000"         // 0.95 threshold (high bar)
}
```

**Expected Output**:
- `isVerified = 1`
- Proof generation succeeds
- Proof verification succeeds

**Rationale**: 96000 ≥ 95000, meets strict requirement

---

## Test Implementation

### Using snarkjs

```bash
# 1. Compile circuit
circom reputation_check.circom --r1cs --wasm --sym

# 2. Generate witness for test case
node generate_witness.js reputation_check.wasm input.json witness.wtns

# 3. Generate proof
snarkjs groth16 prove reputation_check.zkey witness.wtns proof.json public.json

# 4. Verify proof
snarkjs groth16 verify verification_key.json public.json proof.json
```

### Expected Results Summary

| Test | secretARI | threshold | isVerified | Proof Valid | Constraint Check |
|------|-----------|-----------|------------|-------------|------------------|
| 1    | 85000     | 80000     | 1          | ✓           | ✓                |
| 2    | 80000     | 80000     | 1          | ✓           | ✓                |
| 3    | 75000     | 80000     | 0          | ✓           | ✓                |
| 4    | 85000     | 80000     | N/A        | ✗           | ✗ (isMachine)    |
| 5    | 85000     | 80000     | N/A        | ✗           | ✗ (schemaIntegrity) |
| 6    | 100000    | 80000     | 1          | ✓           | ✓                |
| 7    | 0         | 80000     | 0          | ✓           | ✓                |
| 8    | 96000     | 95000     | 1          | ✓           | ✓                |

## Compliance Verification

### Determinism Test

Run the same inputs multiple times and verify bit-identical outputs:

```python
def test_determinism():
    inputs = {"secretARI": 85000, "isMachine": 1, "schemaIntegrity": 1, "threshold": 80000}
    
    proof1 = generate_proof(inputs)
    proof2 = generate_proof(inputs)
    
    # Public outputs must be identical
    assert proof1.public_output == proof2.public_output
    # Both proofs must verify
    assert verify_proof(proof1) == True
    assert verify_proof(proof2) == True
```

### Integer Scaling Validation

Verify that circuit respects $10^5$ scaling:

```python
def test_scaling_factor():
    # ARI 0.8 should be represented as 80000
    assert 0.8 * 10**5 == 80000
    
    # Circuit should accept this scaled value
    inputs = {"secretARI": 80000, "isMachine": 1, "schemaIntegrity": 1, "threshold": 80000}
    assert generate_and_verify(inputs) == True
```

## Status

**Version**: v3.3 Test Specification  
**Status**: Ready for Implementation  
**Dependencies**: circom ≥2.1.0, snarkjs

## Author

Aura Protocol Testing Team  
Based on v3.3 (Iron Core Correct) Specification
