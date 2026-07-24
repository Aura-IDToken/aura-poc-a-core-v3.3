# Aura Protocol: Core Architecture

```
MACHINE_ACCOUNT Agent → Event → PoCA Core → Audit Layer → Compliance Output
                                     ↓
                            Agent Reliability Index (ARI)
                         0.3×SI + 0.7×SA - Penalties
                         (integer fixed-point, scaling factor 10^5)
```

This system enforces:
- **Deterministic measurement**: Same input → Same ARI (bit-identical on x86_64 and ARM64 — verified in CI; WASM is an architectural goal pending native runtime integration)
- **Cryptographic non-repudiation**: Merkle proofs + SHA-256 + HMAC-SHA256 signing
- **Regulator-readable outputs**: AI Act Article 13 compliance
- **Agent-only scope**: MACHINE_ACCOUNT entities only (Art. 5 compliant)

## Krasinski Principle

**T ∝ 1/S**

Transparency (T) inversely proportional to Secrecy/Entropy (S).

## Layer Model

| Layer | Path | Responsibility |
|-------|------|---------------|
| 0 | `core/` | Measurement only — integer ARI calculation, no policy decisions |
| 1 | `audit/` | Merkle tree construction, immutable anchoring, proof generation, signing |
| 2 | `compliance/` | Policy enforcement, certificate generation, compliance rendering |

## Key Components

1. **Core Engine** (`/core`): ARI measurement — integer-only, frozen formula
2. **Audit Layer** (`/audit`): Merkle trees + proof verification + signing abstraction
3. **Compliance Layer** (`/compliance`): Policy enforcement, certificate generation, rendering
4. **Documentation** (`/docs`): Mathematical foundation, regulatory mapping, ADRs, specifications

## Canonical API

**Layer 0 (pure measurement):**
```python
from core.evaluator import PoCAEvaluator
evaluator = PoCAEvaluator(constitution_vector_int32)
result = evaluator.evaluate(agent_id, vector_int32, valid_schema)
# {"ari": <int32>, "drift": <int32>}
```

**Layer 2 (measurement + policy):**
```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
evaluator = PoCAEvaluator(constitution_vector_int32)
result = evaluate_with_policy(evaluator, agent_id, vector_int32, valid_schema)
# {"ari": <int32>, "drift": <int32>}
```

## Audit Layer Signing

The Audit Layer uses **HMAC-SHA256** to sign Event Trust Certificates (ETCs).
A signing abstraction (`audit/signing.py`) isolates the algorithm behind stable
`Signer` / `Verifier` interfaces:

```
Current:  HMACSigner / HMACVerifier    (HMAC-SHA256, production)
Future:   FutureEd25519Signer / FutureEd25519Verifier  (stub, not implemented)
```

The abstraction allows future migration to asymmetric (Ed25519) signing without
changing the Audit Layer API.  Such a migration requires a new instrument version.

Normative specification: [`docs/specs/AUDIT_LAYER_SPEC.md`](specs/AUDIT_LAYER_SPEC.md)

## Cross-Platform Determinism

CI verifies bit-identical outputs on **x86_64** and **ARM64** using
`scripts/generate_determinism_report.py` and
`scripts/compare_determinism_reports.py`.

Compared values per platform:
- ARI (int32)
- Drift (int32)
- Canonical Event Hash (SHA-256)
- Merkle Root (SHA-256)
- Audit Certificate Hash (SHA-256)

WASM compatibility is verified by `WASMCompatibilityTest` in
`core/test_bitwise_replay.py` (operational WASM execution is an architectural
goal; see docs/GAP-001.md).

