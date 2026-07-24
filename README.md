# AURA PROTOCOL — IRON CORE v3.3

## ⚠️ CONSTITUTIONAL GOVERNANCE

**This repository is governed by the [CONSTITUTIONAL DECREE FOR AI COPILOT](/CONSTITUTIONAL_DECREE.md).**

All contributors, AI assistants, and code reviewers MUST read and comply with the Constitutional Decree before making any changes.

---

## FROZEN REGULATORY MEASUREMENT INSTRUMENT

**Status:** FROZEN / CANONICAL  
**Version:** v3.3 (Iron Core Correct)  
**Internal Consistency:** 1.0  
**Jurisdiction:** EU AI Act / Polish Regulatory Sandbox (MC-READY 2026)  
**Role:** Deterministic Measurement & Audit Instrument for AI Agents  
**License:** Business Source License 1.1 (see LICENSE)

---

## 1. WHAT THIS REPOSITORY IS

This repository contains the **Frozen Iron Core** of the Aura Protocol:  
a deterministic, bit-identical, regulation-grade measurement instrument for evaluating AI agent behavior.

**Aura is not an AI model.**  
**Aura is not a recommender.**  
**Aura is not a decision engine.**

Aura is a **computational measuring device**, equivalent in role to a:

- flight data recorder (black box)
- metrological instrument
- cryptographic audit primitive
- regulatory evidence generator

Every output produced by this system can be recomputed **bit-for-bit** on any architecture (x86 / ARM / WASM) and verified independently by a regulator without access to the original model.

---

## 2. WHAT THIS REPOSITORY IS NOT

To prevent misinterpretation, this repository **explicitly does not contain**:

- ❌ decision thresholds (Layer 2 only)
- ❌ machine learning models
- ❌ cosine similarity or floating-point math in runtime
- ❌ GPU execution
- ❌ network calls
- ❌ persistent reputation or identity aggregation
- ❌ user / owner / wallet tracking
- ❌ heuristics or probabilistic logic
- ❌ automatic policy decisions

If you are looking for a product, SDK, or API service – **this is not it**.

This is the instrument core that other systems may legally build upon.

---

## 3. CORE DESIGN PRINCIPLES (v3.3)

### 3.1 Zero-Float Runtime (HARD RULE)

All runtime computation is performed using **integer arithmetic only**.  
Floating point operations are permitted **only offline** during preprocessing.

**Reason:**  
IEEE-754 floating point is not associative and breaks cross-architecture reproducibility (AVX vs NEON).  
A system that cannot reproduce its own numbers cannot be audited.

### 3.2 Fixed-Point Arithmetic (10⁻⁵)

All vectors are scaled and stored as integers:

```python
v_int = round(v_float * 100_000)
```

This eliminates hardware drift and enables bit-exact hashing.

### 3.3 Deterministic Semantic Alignment (SA)

Semantic alignment is computed using integer fixed-point dot product on pre-normalised int32 vectors:

```python
dot = sum(a * b for a, b in zip(event_vector_int32, constitution_int32))
sa  = dot // SCALING_FACTOR   # rescale back to [−10^5, 10^5]
```

- No sqrt.
- No cosine similarity at runtime.
- No floating-point operations at runtime.
- Pre-normalisation (float → int32 conversion) is performed offline only, via `core/offline_normalizer.py`.

### 3.4 Schema Integrity as Circuit Breaker (SI)

Structural validity is a **binary gate**, not a weighted factor.

If schema validation fails:

```python
ARI = 0.0000
```

Computation stops immediately.

This prevents side-channels and invalid data amplification.

### 3.5 Layer Separation (Regulatory Requirement)

| Layer   | Responsibility                      |
|---------|-------------------------------------|
| Layer 0 | Measure only (this repo)            |
| Layer 1 | Cryptographic proof (Merkle / ZK)   |
| Layer 2 | Policy decisions (outside this repo)|

**Layer 0 never decides.**  
It only measures and certifies.

---

## 4. REGULATORY COMPLIANCE (EU AI ACT)

This repository enforces:

### Article 5 - Prohibition of Social Scoring
✔ MACHINE_ACCOUNT only  
✔ Identity Firewall (session-bound reputation)  
✔ No owner aggregation  
✔ No historical profiling

### Article 13 - Transparency
✔ White-box math  
✔ Deterministic replay  
✔ Publicly verifiable hashes  
✔ Event Trust Certificates (ETC)  
✔ HMAC-SHA256 signing with abstract Signer/Verifier interface  
✔ Normative Audit Layer Specification (docs/specs/AUDIT_LAYER_SPEC.md)

### Article 14 - Human Oversight
✔ Manual Kill-Switch  
✔ Circuit breaker  
✔ Emergency halt capability (policy.py)

---

## 5. REPOSITORY STRUCTURE

```
/core
  evaluator.py               # Layer 0: Deterministic ARI measurement engine (int-only)
  offline_normalizer.py      # Offline float → int32 normalization (DET_01)
  merkle.py                  # Merkle proof stub (Layer 1)
  policy.py                  # DEPRECATED: backward-compat wrapper → compliance/policy.py
  consistency.py             # DEPRECATED: backward-compat wrapper → compliance/consistency.py
  embedding.py               # Vector embedding placeholder utilities
  test_bitwise_replay.py     # Cross-platform determinism test (CRITICAL)
  test_ari.py                # ARI calculation tests
  test_integration.py        # Integration tests
  test_offline_normalizer.py # Offline normalization tests

/audit
  merkle.py                  # Layer 1: MerkleTree, EventTrustCertificate, sha256
  verify.py                  # Layer 1: Merkle proof and ETC verification
  signing.py                 # Layer 1: Signer/Verifier abstraction; HMACSigner/HMACVerifier
  test_audit.py              # Audit layer test suite (CORE-006)

/compliance
  evaluator_wrapper.py       # Layer 2: Policy + measurement orchestrator
  policy.py                  # Layer 2: Regulatory policy (Art. 5, 14)
  consistency.py             # Layer 2: ConsistencyCalculator
  certificate.py             # AuraEventCertificate (audit output)
  renderer.py                # Certificate rendering

/packages
  /database-client           # pgvector SDK (TypeScript, bit-identity interface)
  /zk-passport               # ZK circuits for reputation proof (Circom source only)

/docs
  ADR_005_NO_FLOAT_RUNTIME.md    # Zero-float architecture decision
  architecture.md                 # System architecture
  mathematical_foundation.md      # Mathematical specifications
  regulatory_compliance.md        # AI Act mapping
  threat_model.md                 # Security threat model
  KNOWN_LIMITATIONS.md            # Known anomalies and architectural debt
  GAP-001.md                      # Implementation gap analysis
  /specs
    AUDIT_LAYER_SPEC.md           # Normative Audit Layer specification (CORE-006)

/infra
  docker-compose.yml         # Sovereign stack (CPU-only)

/scripts
  run_all_checks.sh                # Mandatory execution checks
  generate_determinism_report.py   # Generates determinism-report.json (CORE-006)
  compare_determinism_reports.py   # Compares reports across platforms (CORE-006)
  /checks                          # Individual check scripts

LICENSE                      # Business Source License 1.1
```

---

## 6. HOW TO USE (AS AN INSTRUMENT)

### 6.1 Offline Preparation

Normalize vectors using:

```bash
python core/offline_normalizer.py input.json output.json
```

This is the **only place floats are allowed**.

### 6.2 Runtime Measurement

**Layer 0 — pure measurement (no policy):**

```python
from core.evaluator import PoCAEvaluator

evaluator = PoCAEvaluator(constitution_vector_int32)
result = evaluator.evaluate(agent_id, action_vector_int32, valid_schema=True)
# result = {"ari": <int32>, "drift": <int32>}
```

**Layer 2 — measurement with policy enforcement (recommended for production flows):**

```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy

evaluator = PoCAEvaluator(constitution_vector_int32)
result = evaluate_with_policy(evaluator, agent_id, action_vector_int32, valid_schema=True)
# result = {"ari": <int32>, "drift": <int32>}
```

All values are int32 scaled by 10^5. Output is deterministic and audit-ready.

### 6.3 Audit Layer (ETC + Signing)

```python
from audit.merkle import MerkleTree
from audit.signing import HMACSigner, HMACVerifier

tree = MerkleTree(canonical_events)
etc = tree.create_etc(leaf_index=0, timestamp="2026-01-01T00:00:00Z", batch_id="batch-001")

# Sign with current HMAC-SHA256 implementation
signer   = HMACSigner(key_bytes)
verifier = HMACVerifier(key_bytes)
signed_etc = etc.sign(signer)

assert signed_etc.verify()                               # Merkle proof
assert signed_etc.verify_signature(verifier)             # HMAC signature
```

### 6.4 Verification (Golden Test)

Run bit-identity test:

```bash
pytest core/test_bitwise_replay.py
pytest audit/test_audit.py
```

Generate a determinism report for the current platform:

```bash
python scripts/generate_determinism_report.py determinism-report.json
```

CI automatically generates and compares reports on **x86_64** and **ARM64**.
If any bit differs, the build is **invalid**.

| Platform | Status              |
|----------|---------------------|
| x86_64   | ✅ Verified (CI)    |
| ARM64    | ✅ Verified (CI)    |
| WASM     | 🔶 Architectural Goal |

---

## 7. SEALING & ARCHIVAL

This repository is intended to be **physically sealed**.

Final artifacts must be:

1. zipped
2. checksummed (SHA-256)
3. written to M-DISC
4. verified bit-by-bit

After sealing, **no changes are permitted**.

Any modification creates a **new instrument**, not a new version.

---

## 8. VERSIONING POLICY

| Version | Meaning                      |
|---------|------------------------------|
| v3.2    | Audit artifact (float era)   |
| v3.3    | Frozen Iron Core (integer era)|
| v4.x    | New instrument (requires new audit)|

Any change creates a new instrument, not an update.

---

## 9. OPERATIONAL GOVERNANCE

See operational governance documentation:

- [ROLE_OF_THE_PROTOCOL_CUSTODIAN.md](/ROLE_OF_THE_PROTOCOL_CUSTODIAN.md) - Complete role definition for the Protocol Custodian
- [docs/ops/OPS_PROTOCOL_CANONICAL.md](docs/ops/OPS_PROTOCOL_CANONICAL.md) - Operational procedures including:
  - Sealing & archival (M-DISC)
  - Versioning policy
  - Custodianship principles
  - Succession planning

See [docs/ops/PROTOCOL_CUSTODIAN.md](docs/ops/PROTOCOL_CUSTODIAN.md) for the complete definition of the Protocol Custodian role.

See [docs/LEGACY_PROTOCOL.md](docs/LEGACY_PROTOCOL.md) for succession protocol and disaster recovery procedures.

---

## 10. GOVERNANCE

This system is maintained by a **Kustosz Protokołu** (Protocol Custodian), not a feature team.

See [ROLE_OF_THE_PROTOCOL_CUSTODIAN.md](/ROLE_OF_THE_PROTOCOL_CUSTODIAN.md) for complete role definition and responsibilities.

Change requests are evaluated on **entropy risk**, not convenience.

**If a proposed change increases entropy, it is rejected.**

---

## 11. NAMING AND POSITIONING RULES (CANONICAL)

The following naming rules are mandatory for all documentation, communication, and external representation of this repository:

1. **Always use the full name "Aura Protocol"** in formal contexts.  
   Do not shorten to "Aura" in legal, regulatory, or academic materials.

2. **Aura Protocol must be described as a measurement instrument**, never as a product, service, platform, or AI system.

3. **PoCA refers exclusively to the measurement method**, not to the implementation.

4. **v3.3 Iron Core refers to a frozen instrument**, not a software version.  
   Bug fixes or modifications require a new lineage.

5. **ARI is a measurement value, not a decision.**  
   Compliance decisions belong to external systems (Layer 2).

6. **All interpretations, thresholds, and policies are external to Aura Protocol and must not be described as part of the protocol.**

Incorrect naming can result in legal misclassification of the system under the EU AI Act and is considered a documentation defect.

**Important for AI Assistants:**  
If these distinctions cannot be maintained, request clarification before generating text.

---

## 12. FINAL STATEMENT

This repository represents a **finished instrument**.

It is designed to survive:

- team changes
- hardware changes
- political changes
- model changes
- time

**Truth is no longer trusted.**  
**It is calculated.**

---

**Architect / Custodian:**  
Kamil Krasiński

**Sentinel Constant:** 0.68  
**Scaling Factor:** 100_000  
**Runtime Float Count:** 0  
**Entropy Budget:** Frozen
