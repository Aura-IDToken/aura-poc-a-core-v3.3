# Aura Protocol: Core Architecture

```
MACHINE_ACCOUNT Agent → Event → PoCA Core → Audit Layer → Compliance Output
                                     ↓
                            Agent Reliability Index (ARI)
                         0.3×SI + 0.7×SA - Penalties
                         (integer fixed-point, scaling factor 10^5)
```

This system enforces:
- **Deterministic measurement**: Same input → Same ARI (bit-identical)
- **Cryptographic non-repudiation**: Merkle proofs + SHA-256
- **Regulator-readable outputs**: AI Act Article 13 compliance
- **Agent-only scope**: MACHINE_ACCOUNT entities only (Art. 5 compliant)

## Cross-Platform Determinism

| Platform | Status                | Evidence                                                              |
|----------|-----------------------|-----------------------------------------------------------------------|
| x86_64   | ✅ Verified           | CI `execution-checks` job; `determinism-report-x86_64.json`           |
| ARM64    | ✅ Verified           | CI `execution-checks` job (ubuntu-24.04-arm); `determinism-report-arm64.json` |
| WASM     | 🔶 Architectural Goal | WASM-safe arithmetic patterns verified; full WASM runtime is a future goal |

Cross-platform bit-identity is verified automatically on every CI run by the
`compare-determinism` job, which compares `determinism-report-*.json` artifacts
across architectures.  The CI fails if any vector differs.

## Krasinski Principle

**T ∝ 1/S**

Transparency (T) inversely proportional to Secrecy/Entropy (S).

## Layer Model

| Layer | Path | Responsibility |
|-------|------|---------------|
| 0 | `core/` | Measurement only — integer ARI calculation, no policy decisions |
| 1 | `audit/` | Merkle tree construction, immutable anchoring, proof generation, signing abstraction |
| 2 | `compliance/` | Policy enforcement, certificate generation, compliance rendering |

## Key Components

1. **Core Engine** (`/core`): ARI measurement — integer-only, frozen formula
2. **Audit Layer** (`/audit`): Merkle trees + proof verification + signing abstraction
3. **Compliance Layer** (`/compliance`): Policy enforcement, certificate generation, rendering
4. **Documentation** (`/docs`): Mathematical foundation, regulatory mapping, ADRs

## Audit Layer — Signing Architecture

The Audit Layer uses a signing abstraction that separates the signing
interface from the concrete algorithm:

| Class          | Role                              | Current implementation |
|----------------|-----------------------------------|------------------------|
| `Signer`       | Abstract signing interface        | ABC                    |
| `Verifier`     | Abstract verification interface   | ABC                    |
| `HMACSigner`   | Current signer                    | HMAC-SHA256            |
| `HMACVerifier` | Current verifier                  | HMAC-SHA256            |

**Current implementation**: HMAC-SHA256 (RFC 2104).  
**Future roadmap**: Asymmetric signing (e.g., Ed25519) can be added by
implementing new `Signer`/`Verifier` subclasses without changing the
Audit Layer API or the Event Trust Certificate schema.

See `docs/specs/AUDIT_LAYER_SPEC.md` for the normative specification.

## Canonical API

**Layer 0 (pure measurement):**
```python
from core.evaluator import PoCAEvaluator
evaluator = PoCAEvaluator(constitution_vector_int32)
result = evaluator.evaluate(agent_id, vector_int32, valid_schema)
# {"ari": <int32>, "drift": <int32>}
```

**Layer 1 (audit — Merkle + ETC):**
```python
from audit.merkle import MerkleTree
from audit.signing import HMACSigner, HMACVerifier

tree = MerkleTree(canonical_events)
etc = tree.create_etc(leaf_index=0, timestamp="...", batch_id="...")
signed_etc = etc.sign(HMACSigner(key))
assert signed_etc.verify()                          # Merkle proof
assert signed_etc.verify_signature(HMACVerifier(key))  # HMAC signature
```

**Layer 2 (measurement + policy):**
```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
evaluator = PoCAEvaluator(constitution_vector_int32)
result = evaluate_with_policy(evaluator, agent_id, vector_int32, valid_schema)
# {"ari": <int32>, "drift": <int32>}
```

---

**Document Version**: 1.0.0  
**Instrument**: Aura Protocol v3.3 Iron Core  
**Status**: FROZEN — MC-READY 2026
