# Aura Protocol: Regulatory Compliance

## EU AI Act Compliance

### Article 5: Prohibited AI Practices

**Status**: ✓ COMPLIANT

**System Scope**: MACHINE_ACCOUNT entities only

**Absolute Prohibitions Implemented**:
1. ❌ Human profiling or scoring
2. ❌ Biometric data processing
3. ❌ Social scoring of natural persons
4. ❌ Behavioral manipulation of humans

**Enforcement Mechanism**:
- Architectural constraint: Agent ID must be MACHINE_ACCOUNT type
- No personal data collection capability
- No human-identifiable information in evaluation pipeline

### Article 13: Transparency and Information Provision

**Status**: ✓ COMPLIANT

**Implementation**:
1. ✓ Mathematical formula publicly documented
2. ✓ Deterministic evaluation (reproducible)
3. ✓ Cryptographic audit trail (Merkle proofs)
4. ✓ Score decomposition available (SI + SA - P)
5. ✓ Open-source core logic

**Documentation**:
- Formula: `ARI = 0.3 × SI + 0.7 × SA - P`
- Semantic space: ℝ¹⁵³⁶ (cosine similarity)
- Non-repudiation: SHA-256 + Merkle trees

### Article 14: Human Oversight

**Status**: ✓ COMPLIANT

**Design**:
- System provides ARI scores as decision support
- Does NOT make autonomous decisions
- Human operators retain full control
- Audit trail enables human review

## Nomenclature Compliance

### Social Scoring Avoidance

**Problem**: "Trust Score" could be classified as social scoring.

**Solution**: Use "Agent Reliability Index" (ARI)

**Rationale**:
- "Reliability" = technical/behavioral consistency
- "Agent" = explicitly non-human scope
- "Index" = mathematical metric, not moral judgment

**Strictly Forbidden Terms**:
- ❌ Trust Score
- ❌ Reputation Score  
- ❌ Trustworthiness Rating
- ❌ Credibility Score

**Approved Terms**:
- ✓ Agent Reliability Index (ARI)
- ✓ Consistency Score
- ✓ Alignment Metric
- ✓ PoCA Score (Proof of Consistent Agency)

## Krasinski Principle

```
T ∝ 1/S
```

**Transparency (T)** is inversely proportional to **Secrecy/Entropy (S)**.

### Compliance Application

**High Transparency (low S)**:
- Open-source algorithm
- Documented formula
- Cryptographic proofs
- Deterministic execution
- Audit trail

**Low Secrecy (low S)**:
- No proprietary black boxes
- No hidden training data
- No opaque model updates
- No undocumented penalties

### Regulatory Benefit

By maximizing T (minimizing S), Aura Protocol achieves:
1. AI Act Article 13 compliance (transparency)
2. Auditor-friendly evidence
3. Non-repudiable proofs
4. Public verifiability

## Data Protection (GDPR)

### Personal Data: NOT APPLICABLE

**Reason**: System processes MACHINE_ACCOUNT entities only.

**No GDPR Applicability**:
- No natural persons as data subjects
- No personal identifiers
- No behavioral profiling of humans
- No biometric data

**Architecture Guarantee**: Agent ID field constrained to machine identifiers.

## Audit Readiness

### Regulatory Audit Support

**Artifacts Generated**:
1. **Mathematical Specification**: Formula + parameters
2. **Cryptographic Proofs**: Merkle root + leaf hashes
3. **Evaluation Logs**: Timestamped, immutable
4. **Source Code**: Open-source, versioned
5. **Compliance Certificate**: Per-event, machine-readable

### Regulator Access

**No Privileged Access Required**:
- Merkle proofs verify without system access
- Certificate fingerprints publicly verifiable
- Formula documented and frozen
- Determinism testable by third parties

### Non-Repudiation

**Cryptographic Guarantee**:
- SHA-256 hashing (collision-resistant)
- Merkle tree construction (tamper-evident)
- Certificate fingerprinting (unique + reproducible)

**Claim**: Agent cannot deny evaluated actions if Merkle proof validates.

## Frozen Status

**Regulatory Audit Phase**: MC-READY 2026

**Immutable Components**:
1. ARI Formula: `0.3 × SI + 0.7 × SA - P`
2. Semantic Space: ℝ¹⁵³⁶
3. Nomenclature: "Agent Reliability Index"
4. Scope: MACHINE_ACCOUNT only
5. Krasinski Principle: T ∝ 1/S

**Rationale**: Regulatory stability during audit process.

Changes require formal review + compliance re-assessment.

## Author & Ownership

**Author**: Kamil Krasiński

**License**: MIT (open-source)

**Status**: Research-backed prototype → Production-ready core

---

**Document Version**: 1.0.0  
**Last Updated**: MC-READY 2026 Freeze  
**Compliance Standard**: EU AI Act (2024)
