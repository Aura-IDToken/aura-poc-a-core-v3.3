# Aura PoCA Core Architecture

```
MACHINE_ACCOUNT Agent → Event → PoCA Core → Audit Layer → Compliance Output
                                     ↓
                            Agent Reliability Index (ARI)
                         0.3×SI + 0.7×SA - Penalties
                              in ℝ¹⁵³⁶ space
```

This system enforces:
- **Deterministic evaluation**: Same input → Same ARI
- **Cryptographic non-repudiation**: Merkle proofs + SHA-256
- **Regulator-readable outputs**: AI Act Article 13 compliance
- **Agent-only scope**: MACHINE_ACCOUNT entities (Art. 5 compliant)

## Krasinski Principle

**T ∝ 1/S**

Transparency (T) inversely proportional to Secrecy/Entropy (S).

## Key Components

1. **Core Engine** (`/core`): ARI calculation (frozen formula)
2. **Audit Layer** (`/audit`): Merkle trees + verification
3. **Compliance Layer** (`/compliance`): Certificate generation + rendering
4. **Documentation** (`/docs`): Mathematical foundation + regulatory mapping
