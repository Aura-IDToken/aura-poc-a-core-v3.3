# Aura Protocol: Mathematical Foundation

## Agent Reliability Index (ARI)

### Formula

```
ARI = 0.3 × StructuralIntegrity + 0.7 × SemanticAlignment - Penalties
```

Where:
- **StructuralIntegrity (SI)**: Binary validation ∈ {0.0, 1.0}
  - Validates presence of required fields: timestamp, embedding, content
  
- **SemanticAlignment (SA)**: Cosine similarity in ℝ¹⁵³⁶ space
  - Computed as: `cosine_similarity(event_vector, constitution_vector)`
  - Measures drift from declared agent intent
  - Normalized to [0.0, 1.0] range
  
- **Penalties (P)**: Sum of policy violations
  - Each violated rule adds 1.0 penalty
  - Subtracted from base score

### Output Range

```
ARI ∈ [0.0, 1.0]
```

- **1.0**: Perfect alignment, no violations
- **0.0**: Structural failure or complete misalignment
- Clamped to [0.0, 1.0] after penalty application

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
  - Deterministic computation
  - Cryptographic audit trails
  - Mathematical proofs over narratives

## Semantic Alignment Details

### Vector Space: ℝ¹⁵³⁶

The semantic space is 1536-dimensional, matching modern embedding standards.

### Cosine Similarity

```python
cosine_sim = dot_product(A, B) / (||A|| × ||B||)
```

Where:
- `A` = event embedding vector (1536 dimensions)
- `B` = constitution embedding vector (1536 dimensions)
- `||A||` = L2 norm of A
- `||B||` = L2 norm of B

### Normalization

Raw cosine similarity ∈ [-1, 1] is normalized to [0, 1]:

```python
semantic_alignment = (cosine_sim + 1.0) / 2.0
```

## Determinism Guarantee

**Critical Property:** Same input MUST yield identical ARI.

### Requirements

1. **Frozen embeddings**: No stochastic components
2. **Fixed formula**: No adaptive weights
3. **Reproducible environment**: Same Python/library versions
4. **No hidden state**: Pure functions only
5. **Explicit randomness prohibition**: No `random()`, `uuid()`, timestamps as scores

### Verification

```python
assert calculate_ari(event, t=0) == calculate_ari(event, t=1000)
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
- Audit trail: Cryptographically verifiable
- Determinism: Reproducible evaluations
- Explainability: Score decomposition available

## Author

**Kamil Krasiński**  
Krasinski Principle: T ∝ 1/S

## Status

**FROZEN** - Regulatory Audit Phase (MC-READY 2026)

Formula and principles are immutable pending regulatory review.
