# Aura Protocol: Mathematical Foundation

## Agent Reliability Index (ARI)

### Formula

```
ARI = 0.3 × StructuralIntegrity + 0.7 × SemanticAlignment - Penalties
```

Where:
- **StructuralIntegrity (SI)**: Binary validation ∈ {0, SCALING_FACTOR}
  - Validates presence of required fields: timestamp, embedding, content
  - Runtime representation: integer (0 or 100,000)
  
- **SemanticAlignment (SA)**: Integer fixed-point dot product of pre-normalized int32 vectors
  - Computed as: `dot(event_vector_int32, constitution_int32) // SCALING_FACTOR`
  - Range: approximately [−10^5, 10^5]; clamped to [0, 10^5] in final ARI
  
- **Penalties (P)**: Sum of policy violations (int32, scaled by 10^5)
  - Calculated by Layer 2 policy engine, injected into Layer 0 as parameter

### Runtime Representation

All values are **int32 scaled by 10^5** (SCALING_FACTOR = 100,000):

| Conceptual value | Runtime int32 |
|-----------------|---------------|
| 0.0             | 0             |
| 1.0             | 100,000       |
| 0.8 (sentinel)  | 80,000        |

### Output Range

```
ARI ∈ [0, 100000]  (int32, scaled by 10^5)
```

- **100000**: Perfect alignment, no violations
- **0**: Structural failure or complete misalignment / penalty exceeds score
- Clamped to [0, 100000] after penalty application

## Krasinski Principle

```
T ∝ 1/S
```

**Transparency (T)** is inversely proportional to **Secrecy/Entropy (S)**.

### Interpretation

- Trust is not a moral judgment
- Trust is behavioral consistency made transparent
- The more opaque a system (high S), the less transparent (low T)
- Aura Protocol maximizes T by minimizing S through:
  - Deterministic integer computation
  - Cryptographic audit trails
  - Mathematical proofs over narratives

## Semantic Alignment — Current Runtime (v3.3 Integer Core)

### Integer Fixed-Point Dot Product

Semantic alignment is computed entirely in integer arithmetic using pre-normalized vectors:

```python
# Both vectors pre-normalized offline to unit length and scaled by 10^5
dot = sum(a * b for a, b in zip(event_vector_int32, constitution_int32))
sa  = dot // SCALING_FACTOR   # rescale: [−10^10, 10^10] → [−10^5, 10^5]
```

**Properties:**
- No `math.sqrt` at runtime
- No floating-point division at runtime
- Both vectors must be unit-normalized offline (via `core/offline_normalizer.py`)
- Result is equivalent to cosine similarity for unit-normalized inputs, computed entirely in integers

### Pre-normalisation (Offline Step)

Vectors are normalized once offline before deployment:

```python
# offline_normalizer.py (float permitted — runs once, not at runtime)
v_normalized = v_float / np.linalg.norm(v_float)   # L2 normalise
v_int32 = [round(x * 100_000) for x in v_normalized]  # scale to int32
```

This step is the **only** place where floating-point operations are permitted.

## Semantic Alignment — Historical Background (Legacy Float Era)

> ⚠️ **HISTORICAL ONLY — NOT THE CURRENT RUNTIME**  
> The following describes the pre-v3.3 float-based implementation.  
> It is retained for audit traceability only.  
> The current v3.3 Iron Core does **not** use these operations at runtime.

### Vector Space: ℝ¹⁵³⁶

The semantic space was 1536-dimensional, matching modern embedding standards.

### Cosine Similarity (Legacy)

```python
cosine_sim = dot_product(A, B) / (||A|| × ||B||)
```

Where:
- `A` = event embedding vector (1536 dimensions, float)
- `B` = constitution embedding vector (1536 dimensions, float)
- `||A||` = L2 norm of A (computed with `math.sqrt`)
- `||B||` = L2 norm of B (computed with `math.sqrt`)

### Legacy Normalization

Raw cosine similarity ∈ [-1, 1] was normalized to [0, 1]:

```python
semantic_alignment = (cosine_sim + 1.0) / 2.0
```

**Reason for removal:** IEEE-754 non-determinism. Different architectures (x86 AVX, ARM NEON)
produce different bit patterns for the same float computation. This violated the
cross-platform bit-identity requirement. Replaced by integer dot product in v3.3.

## Determinism Guarantee

**Critical Property:** Same input MUST yield identical ARI (bit-for-bit on all architectures).

### Requirements

1. **Frozen int32 embeddings**: No stochastic components
2. **Fixed formula**: No adaptive weights
3. **Integer-only runtime**: No float operations after offline pre-processing
4. **No hidden state**: Pure functions only
5. **Explicit randomness prohibition**: No `random()`, `uuid()`, timestamps as scores

### Verification

```python
from core.evaluator import PoCAEvaluator

evaluator = PoCAEvaluator(constitution_vector_int32)
result_1 = evaluator.evaluate(agent_id, vector_int32, valid_schema=True)
result_2 = evaluator.evaluate(agent_id, vector_int32, valid_schema=True)

assert result_1["ari"] == result_2["ari"]    # Deterministic
assert result_1["drift"] == result_2["drift"] # Deterministic
```

For any event and any two evaluation times t₀ and t₁.

## Regulatory Compliance

### Scope Limitation

**AGENT_ONLY**: System strictly limited to MACHINE_ACCOUNT entities.

**PROHIBITED**:
- Human profiling
- Biometric data processing
- Social scoring of natural persons

**Rationale**: EU AI Act Article 5 compliance.

### Nomenclature

**Required Term**: "Agent Reliability Index" (ARI)

**Forbidden Term**: "Trust Score"

**Reason**: Avoid classification as Social Scoring system under AI Act.

### Transparency Requirements

Per AI Act Article 13:
- Mathematical formula: Public and auditable
- Audit trail: Cryptographically verifiable (Merkle proofs)
- Determinism: Reproducible evaluations (int32 arithmetic)
- Explainability: Score decomposition available (SI, SA, penalty components)

## Author

**Kamil Krasiński**  
Krasinski Principle: T ∝ 1/S

## Status

**FROZEN** — Regulatory Audit Phase (MC-READY 2026)

Formula and principles are immutable pending regulatory review.

