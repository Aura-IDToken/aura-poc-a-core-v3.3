# Threat Model

## Covered Threats

### 1. Log Tampering
**Mitigation**: Merkle tree construction + SHA-256 hashing
- Tamper-evident audit trail
- Any modification breaks hash chain
- Verifiable without privileged access

### 2. Narrative Manipulation  
**Mitigation**: Deterministic ARI calculation
- Mathematical formula (frozen): `ARI = 0.3×SI + 0.7×SA - P`
- No subjective interpretation
- Same input always yields same output

### 3. Post-hoc Justification
**Mitigation**: Cryptographic non-repudiation
- Event certificates timestamped + hashed
- Merkle proofs prevent retroactive changes
- Certificate fingerprints publicly verifiable

### 4. Social Scoring Classification Risk
**Mitigation**: Agent-only scope + nomenclature
- MACHINE_ACCOUNT entities exclusively
- "Agent Reliability Index" not "Trust Score"
- No human profiling capability (AI Act Art. 5)

### 5. Scope Creep (Human Data)
**Mitigation**: Architectural constraint
- Agent ID type enforcement
- No biometric data fields
- No personal identifiers

## Out of Scope (By Design)

### 1. Model Poisoning
**Reason**: Embedding model is external dependency
**Assumption**: Frozen, audited embedding model in production

### 2. Hardware Side-Channels
**Reason**: Outside software security boundary
**Assumption**: Trusted execution environment

### 3. Regulatory Reclassification
**Reason**: Legal risk, not technical threat
**Mitigation**: Compliance documentation + frozen nomenclature

## Krasinski Principle Application

**T ∝ 1/S**

### Threat: Opacity (High S)
**Mitigation**: Maximize Transparency (T)
- Open-source core
- Documented formula  
- Public audit trail
- Deterministic proofs

### Result: Low S → High T → Verifiable Trust
