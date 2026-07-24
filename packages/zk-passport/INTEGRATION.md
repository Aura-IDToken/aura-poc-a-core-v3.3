# Integration Guide: ZK Reputation Circuit ↔ Aura Core

## Overview

This document explains how the `reputation_check.circom` ZK circuit integrates with the Aura Protocol v3.3 deterministic core evaluation system.

## Data Flow

```
┌─────────────────┐
│  Agent Event    │
│  (MACHINE_ACC)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Core Evaluator (Python)           │
│   /core/evaluator.py                │
│                                     │
│   ARI = 0.3×SI + 0.7×SA - Penalties│
│   Output: ARI ∈ [0, 100000] (int32)│
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   ZK Circuit Input Preparation      │
│                                     │
│   secretARI = ari_int  (already     │
│   in 10^5 scale — no re-scaling)    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   ZK Circuit (external toolchain)   │
│   packages/zk-passport/             │
│   reputation_check.circom           │
│                                     │
│   Inputs:                           │
│   - secretARI (private)             │
│   - isMachine (private)             │
│   - schemaIntegrity (private)       │
│   - threshold (public)              │
│                                     │
│   Output:                           │
│   - isVerified (public)             │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Proof Artifact                    │
│   - Zero-knowledge proof            │
│   - Public threshold                │
│   - Binary verification result      │
│   - NO secretARI revealed           │
└─────────────────────────────────────┘
```

## Python Integration Example

> **Note:** The Python steps below show how ARI output from the Aura core is prepared
> for the ZK circuit. Steps 3–4 (proof generation and verification) require the
> external `circom` / `snarkjs` toolchain, which is **not** included in this repository.
> See `packages/zk-passport/TEST_SPECIFICATION.md` for circuit test details.

### Step 1: Calculate ARI (Core Evaluator)

```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
from core.offline_normalizer import SCALING_FACTOR

# Build evaluator with pre-normalised int32 constitution vector
evaluator = PoCAEvaluator(constitution_vector_int32)

# Evaluate agent event (Layer 2 orchestrator handles policy)
result = evaluate_with_policy(
    evaluator,
    agent_id=agent_id,
    vector=action_vector_int32,
    valid_schema=True,
)

# Extract components (all values are int32 scaled by SCALING_FACTOR = 100,000)
ari_int = result["ari"]    # e.g., 85000 (represents 0.85)
drift_int = result["drift"] # e.g., 15000 (represents 0.15)

# Schema validity and machine-account flag are inputs to evaluation, not outputs
valid_schema = True        # validated before calling evaluate_with_policy
is_machine = 1             # enforced by RegulatoryPolicy.validate_target()

# Scale check: ARI is already in int32 space (no further conversion needed)
si_int = 1 if valid_schema else 0
```

### Step 2: Prepare ZK Circuit Inputs

```python
import json

# Define threshold (e.g., 0.8 → 80000)
threshold_float = 0.8
threshold_int = round(threshold_float * SCALING_FACTOR)  # 80000

# Prepare witness (private inputs)
witness = {
    "secretARI": str(ari_int),           # "85000"
    "isMachine": str(is_machine),        # "1"
    "schemaIntegrity": str(si_int)       # "1"
}

# Prepare public inputs
public_inputs = {
    "threshold": str(threshold_int)      # "80000"
}

# Combine for circuit input
circuit_input = {**witness, **public_inputs}

# Save to file for circom
with open('input.json', 'w') as f:
    json.dump(circuit_input, f)
```

### Step 3: Generate ZK Proof

```bash
# Compile circuit (one-time setup)
circom reputation_check.circom --r1cs --wasm --sym

# Generate proving/verification keys (one-time trusted setup)
snarkjs groth16 setup reputation_check.r1cs pot12_final.ptau reputation_check.zkey
snarkjs zkey export verificationkey reputation_check.zkey verification_key.json

# Generate witness
node generate_witness.js reputation_check.wasm input.json witness.wtns

# Generate proof
snarkjs groth16 prove reputation_check.zkey witness.wtns proof.json public.json

# Output:
# - proof.json: ZK proof (can be public)
# - public.json: Contains only threshold and isVerified (no secretARI)
```

### Step 4: Verify Proof (Python)

```python
import subprocess
import json

def verify_reputation_proof(proof_path, public_path, vkey_path):
    """
    Verify ZK proof using snarkjs.
    
    Returns:
        dict: Verification result with isVerified value
    """
    # Run snarkjs verification
    result = subprocess.run(
        [
            'snarkjs', 'groth16', 'verify',
            vkey_path, public_path, proof_path
        ],
        capture_output=True,
        text=True
    )
    
    # Parse verification result
    is_valid = result.returncode == 0
    
    # Load public outputs
    with open(public_path, 'r') as f:
        public_data = json.load(f)
    
    return {
        'proof_valid': is_valid,
        'is_verified': int(public_data[0]),  # Circuit output
        'threshold': int(public_data[1])     # Public input
    }

# Verify
verification = verify_reputation_proof(
    'proof.json',
    'public.json',
    'verification_key.json'
)

print(f"Proof valid: {verification['proof_valid']}")
print(f"Reputation verified: {verification['is_verified'] == 1}")
print(f"Threshold: {verification['threshold'] / SCALING_FACTOR}")
```

## Use Cases

### Use Case 1: Anonymous Reputation Attestation

**Scenario**: Agent wants to prove it meets minimum reputation without revealing exact score.

```python
# Agent generates proof
agent_proof = generate_reputation_proof(
    secret_ari=92000,      # 0.92 (private)
    threshold=80000,       # 0.8 (public)
    is_machine=1,
    schema_integrity=1
)

# Third party verifies (learns nothing about 0.92)
verifier_result = verify_proof(agent_proof)
# Result: "This agent meets the 0.8 threshold" (no exact score revealed)
```

### Use Case 2: Tiered Access Control

**Scenario**: Grant access to resources based on reputation tiers without exposing scores.

```python
tiers = {
    'basic': 50000,     # 0.5
    'standard': 70000,  # 0.7
    'premium': 90000    # 0.9
}

# Agent proves membership in premium tier
proof = generate_reputation_proof(
    secret_ari=agent_ari,
    threshold=tiers['premium'],
    is_machine=1,
    schema_integrity=1
)

if verify_proof(proof)['is_verified']:
    grant_access('premium_resources')
```

### Use Case 3: Compliance Reporting

**Scenario**: Demonstrate regulatory compliance without exposing sensitive scoring data.

```python
# Generate compliance proof
compliance_proof = {
    'timestamp': int(time.time()),
    'regulation': 'EU AI Act Article 5',
    'zk_proof': generate_reputation_proof(
        secret_ari=agent_ari,
        threshold=regulatory_threshold,
        is_machine=1,
        schema_integrity=1
    )
}

# Auditor verifies compliance
auditor_can_verify(compliance_proof)
# Auditor learns: "Agent meets regulatory threshold"
# Auditor does NOT learn: exact ARI score
```

## Security Considerations

### Privacy Guarantees

1. **Zero-Knowledge Property**: Proof reveals ONLY that `secretARI >= threshold`
2. **No Score Leakage**: Exact ARI value remains private
3. **Soundness**: Computationally infeasible to forge proof for `secretARI < threshold`

### Constraints

1. **MACHINE_ACCOUNT Only**: Circuit enforces `isMachine === 1`
   - Prevents misuse for human profiling (EU AI Act Article 5)
   
2. **Schema Integrity**: Circuit enforces `schemaIntegrity === 1`
   - Ensures data quality before reputation claims

3. **Binary Output**: Circuit enforces `isVerified ∈ {0, 1}`
   - Prevents ambiguous results

### Determinism

The Python evaluation pipeline is deterministic:

```python
from core.evaluator import PoCAEvaluator

evaluator = PoCAEvaluator(constitution_vector_int32)

result_1 = evaluator.evaluate(agent_id, vector_int32, valid_schema=True)
result_2 = evaluator.evaluate(agent_id, vector_int32, valid_schema=True)

assert result_1["ari"] == result_2["ari"]    # Deterministic
assert result_1["drift"] == result_2["drift"] # Deterministic
# Same ZK inputs → same proof verification result
```

## Performance Considerations

### Circuit Complexity

- **Constraints**: ~1000-2000 (depends on comparator bit width)
- **Proof Generation**: ~1-5 seconds on modern hardware
- **Proof Verification**: ~10-50ms
- **Proof Size**: ~200-500 bytes

### Optimization Tips

1. **Batch Verification**: Verify multiple proofs in parallel
2. **Proof Caching**: Cache verification keys (one-time setup)
3. **Threshold Presets**: Use fixed thresholds to avoid re-compilation

## Status

**Version**: v3.3 (Iron Core Correct)  
**Integration Status**: Circuit source available — proof toolchain (circom, snarkjs) is an external dependency not included in this repository  
**Dependencies**: 
- Core Evaluator: `/core/evaluator.py`
- Layer 2 Orchestrator: `/compliance/evaluator_wrapper.py`
- ZK Circuit: `/packages/zk-passport/reputation_check.circom`

## Author

Aura Protocol Integration Team  
Aligned with Krasinski Principle: **T ∝ 1/S**
