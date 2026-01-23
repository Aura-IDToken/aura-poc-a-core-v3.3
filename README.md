# AURA PROTOCOL — IRON CORE v3.3

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

Semantic alignment is computed using:

```python
fixed_point_dot_product(int32_vector, int32_constitution)
```

- No sqrt.
- No cosine similarity.
- No floating-point normalization at runtime.

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

### Article 14 - Human Oversight
✔ Manual Kill-Switch  
✔ Circuit breaker  
✔ Emergency halt capability (policy.py)

---

## 5. REPOSITORY STRUCTURE

```
/core
  evaluator.py               # Deterministic ARI measurement engine (int-only)
  offline_normalizer.py      # Offline float → int32 normalization
  merkle.py                  # Audit & proof layer
  policy.py                  # Regulatory enforcement (Art. 5 / 14)
  consistency.py             # Consistency validation
  embedding.py               # Vector embedding utilities
  test_bitwise_replay.py     # Cross-platform determinism test (CRITICAL)
  test_ari.py                # ARI calculation tests
  test_integration.py        # Integration tests
  test_offline_normalizer.py # Offline normalization tests

/packages
  /database-client           # pgvector SDK (bit-identity)
  /zk-passport               # ZK circuits for reputation proof

/docs
  ADR_005_NO_FLOAT_RUNTIME.md    # Zero-float architecture decision
  architecture.md                 # System architecture
  mathematical_foundation.md      # Mathematical specifications
  regulatory_compliance.md        # AI Act mapping
  threat_model.md                 # Security threat model

/infra
  docker-compose.yml         # Sovereign stack (CPU-only)

/scripts
  run_all_checks.sh          # Mandatory execution checks
  /checks                    # Individual check scripts

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

```python
from core.evaluator import evaluate

result = evaluate(action_vector_int32, constitution_vector_int32)
```

Output is deterministic and audit-ready.

### 6.3 Verification (Golden Test)

Run bit-identity test on two architectures:

```bash
pytest core/test_bitwise_replay.py
```

If any bit differs, the build is **invalid**.

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

---

## 9. GOVERNANCE

This system is maintained by a **Kustosz Protokołu**, not a feature team.

Change requests are evaluated on **entropy risk**, not convenience.

**If a proposed change increases entropy, it is rejected.**

---

## 10. FINAL STATEMENT

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
