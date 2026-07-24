# ZK Passport: Reputation Check Circuit

## Overview

This package implements **Task #2** from the Aura Protocol v3.3 specification: a Zero-Knowledge proof circuit that verifies membership in the Agent Reliability Index (ARI) reputation threshold without revealing the exact score.

## Circuit: `reputation_check.circom`

### Purpose

The ReputationCheck circuit provides cryptographic proof that a MACHINE_ACCOUNT's ARI score meets or exceeds a specified threshold, while keeping the actual score private.

### Mathematical Foundation

The circuit operates on **integer-scaled values** using the v3.3 specification's $10^5$ scaling factor:

```
v_int = round(v_float × 10^5)
```

For example:
- ARI of 0.8 → 80000 (scaled)
- ARI of 1.0 → 100000 (scaled)
- Threshold of 0.75 → 75000 (scaled)

### Inputs

#### Private Inputs (Secret)
- **`secretARI`**: The scaled Agent Reliability Index value ($v_{int}=v_{float}\cdot10^5$)
- **`isMachine`**: Binary flag (1 = MACHINE_ACCOUNT, as required by EU AI Act Article 5)
- **`schemaIntegrity`**: Binary structural integrity flag (1 = valid, 0 = error)

#### Public Inputs
- **`threshold`**: The minimum acceptable ARI score (scaled by $10^5$)

### Output

- **`isVerified`**: Binary output (1 = proof valid, 0 = proof invalid)

### Circuit Logic

The circuit enforces three critical validations:

1. **Article 5 Compliance** (EU AI Act)
   ```circom
   isMachine === 1;
   ```
   Ensures evaluation is performed only on MACHINE_ACCOUNT entities, not humans.

2. **Structural Integrity Gate**
   ```circom
   schemaIntegrity === 1;
   ```
   In v3.3 rigor, structural errors (SI=0) prevent validation.

3. **Reputation Threshold Check**
   ```circom
   component geq = GreaterEqThan(32);
   geq.in[0] <== secretARI;
   geq.in[1] <== threshold;
   isVerified <== geq.out;
   ```
   Uses deterministic integer comparison (32-bit values) to verify ARI ≥ threshold.

4. **Binary Output Enforcement**
   ```circom
   isVerified * (isVerified - 1) === 0;
   ```
   Guarantees output is strictly 0 or 1.

## Files

- **`reputation_check.circom`**: Main ZK circuit implementation
- **`comparators.circom`**: Supporting comparison operators (GreaterEqThan, LessThan, Num2Bits)
- **`README.md`**: This documentation

## Compliance

### EU AI Act Alignment

- **Article 5**: Prohibits human profiling → Circuit enforces `isMachine === 1`
- **Article 13**: Transparency & traceability → Mathematical logic is publicly auditable
- **Article 14**: Human oversight → Emergency halt mechanisms exist outside circuit

### Zero-Float Policy

This circuit is **float-free** and operates entirely on:
- Fixed-point integer arithmetic ($10^5$ scaling)
- Deterministic comparisons (no floating-point rounding errors)
- Bit-identical results across platforms

## Usage Example

### Proof Generation (Conceptual)

```javascript
// Private witness
const witness = {
  secretARI: 85000,        // 0.85 ARI (private)
  isMachine: 1,            // Valid MACHINE_ACCOUNT
  schemaIntegrity: 1       // Valid structure
};

// Public input
const publicInput = {
  threshold: 80000         // 0.8 threshold (public)
};

// Generate proof
const proof = await generateProof(circuit, witness, publicInput);

// Verify proof (anyone can verify without knowing secretARI)
const isValid = await verifyProof(proof, publicInput);
// isValid === true (because 85000 >= 80000)
```

### Key Properties

- **Privacy**: Actual ARI value (85000) is never revealed
- **Verifiability**: Anyone can verify the proof using only the public threshold
- **Soundness**: It's computationally infeasible to generate a valid proof for ARI < threshold
- **Completeness**: Valid inputs always produce verifiable proofs

## Integration with Aura Core

This circuit extends the Aura PoCA Core deterministic evaluation:

```
Event → Core Evaluator → ARI (private) → ZK Circuit → Proof
                                              ↓
                                        Public Verification
```

### Workflow

1. **Core evaluator** calculates ARI using deterministic formula
2. **Offline normalizer** scales ARI to integer: `ARI_int = round(ARI × 10^5)`
3. **ZK circuit** generates proof: `ARI_int >= threshold`
4. **Verifier** validates proof without learning ARI_int

## Specification Compliance

**Version**: v3.3 (Iron Core Correct)  
**Status**: FROZEN circuit source — external proof toolchain (circom/snarkjs) not included  
**Determinism**: Circuit logic is integer-only and deterministic; proof generation requires an external ZK toolchain  
**Scaling Factor**: $10^5$ (per v3.3 spec)

## Author

Aura Protocol Core Team  
Based on Krasinski Principle: **T ∝ 1/S** (Transparency inversely proportional to Secrecy)

## License

Business Source License 1.1 (BSL 1.1) — see repository root LICENSE file.
