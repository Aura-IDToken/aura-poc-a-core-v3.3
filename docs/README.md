# Aura Protocol Documentation

This directory contains formal specifications, design documents, and compliance materials.

## Documents

### Core Specifications
- **[mathematical_foundation.md](mathematical_foundation.md)**: ARI formula, Krasinski Principle, semantic alignment (integer fixed-point dot product, v3.3 runtime)
- **[architecture.md](architecture.md)**: System architecture and component overview
- **[threat_model.md](threat_model.md)**: Security considerations and mitigations

### Compliance Materials  
- **[regulatory_compliance.md](regulatory_compliance.md)**: EU AI Act compliance, nomenclature, audit readiness
- **[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md)**: Known anomalies and architectural debt in v3.3

## Directory Structure

- `/core` — PoCA math & logic (ARI calculation, embeddings, policy)
- `/audit` — Merkle proofs, hash verification, audit tooling
- `/compliance` — Certificate generation, rendering, schemas
- `/docs` — This directory (specifications and compliance docs)

## Key Principles

### Krasinski Principle
**T ∝ 1/S**  
Transparency (T) inversely proportional to Secrecy/Entropy (S).

### Agent Reliability Index (ARI)
```
ARI = 0.3 × StructuralIntegrity + 0.7 × SemanticAlignment - Penalties
```

### Regulatory Compliance
- **Scope**: MACHINE_ACCOUNT entities only
- **Prohibition**: No human profiling (AI Act Art. 5)
- **Nomenclature**: "Agent Reliability Index" not "Trust Score"
- **Status**: FROZEN (MC-READY 2026)

## Author

Kamil Krasiński

## Next Steps

1. Review mathematical foundation for ARI calculation details
2. Check regulatory compliance doc for AI Act mapping
3. See architecture doc for system component descriptions
4. Consult threat model for security guarantees
