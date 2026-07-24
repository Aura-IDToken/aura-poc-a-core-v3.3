# Aura Protocol: Core Architecture

```
MACHINE_ACCOUNT Agent → Event → PoCA Core → Audit Layer → Compliance Output
                                     ↓
                            Agent Reliability Index (ARI)
                         0.3×SI + 0.7×SA - Penalties
                         (integer fixed-point, scaling factor 10^5)
```

This system enforces:
- **Deterministic measurement**: Same input → Same ARI (bit-identical on x86; ARM and WASM cross-platform verification is an architectural goal — see GAP-001)
- **Cryptographic non-repudiation**: Merkle proofs + SHA-256
- **Regulator-readable outputs**: AI Act Article 13 compliance
- **Agent-only scope**: MACHINE_ACCOUNT entities only (Art. 5 compliant)

## Krasinski Principle

**T ∝ 1/S**

Transparency (T) inversely proportional to Secrecy/Entropy (S).

## Layer Model

| Layer | Path | Responsibility |
|-------|------|---------------|
| 0 | `core/` | Measurement only — integer ARI calculation, no policy decisions |
| 1 | `audit/` | Merkle tree construction, immutable anchoring, proof generation |
| 2 | `compliance/` | Policy enforcement, certificate generation, compliance rendering |

## Key Components

1. **Core Engine** (`/core`): ARI measurement — integer-only, frozen formula
2. **Audit Layer** (`/audit`): Merkle trees + proof verification
3. **Compliance Layer** (`/compliance`): Policy enforcement, certificate generation, rendering
4. **Documentation** (`/docs`): Mathematical foundation, regulatory mapping, ADRs

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
