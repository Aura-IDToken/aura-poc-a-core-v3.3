# AURA PROTOCOL — IRON CORE v3.3

## ⚠️ CONSTITUTIONAL GOVERNANCE

**This repository is governed by the [CONSTITUTIONAL DECREE FOR AI COPILOT](/CONSTITUTIONAL_DECREE.md).**

All contributors, AI assistants, and code reviewers MUST read and comply with the Constitutional Decree before making any changes.

---

## FROZEN REGULATORY MEASUREMENT INSTRUMENT

**Status:** FROZEN / CANONICAL  
**Version:** v3.3 Iron Core  
**Jurisdiction:** EU AI Act / Polish Regulatory Sandbox (MC-READY 2026)  
**Role:** Deterministic measurement protocol for AI agent behavior  
**License:** Business Source License 1.1 (see LICENSE)

---

## 1. WHAT THIS REPOSITORY IS

This repository contains the **v3.3 Iron Core** of Aura Protocol: a deterministic measurement protocol that performs bit-identical measurement of AI agent behavior.

Aura Protocol is not:
- an AI system
- a decision engine
- a product or service
- a monitoring platform

Aura Protocol performs measurement. Compliance decisions are external.

Every output produced by this repository can be recomputed bit-for-bit on any supported architecture and verified independently without access to the original model.

---

## 2. CORE IMPLEMENTATION RULES

Layer 0 runtime paths use **integer arithmetic only**.

They do not contain:
- floating-point arithmetic
- `math.sqrt`
- NumPy
- decision thresholds
- allow/deny logic
- persistent identity tracking

The only float-permitted path in this repository is the offline preprocessing tool at `core/offline_normalizer.py`.

---

## 3. CURRENT ARCHITECTURE

| Layer | Path | Current responsibility |
|------|------|-------------------------|
| Layer 0 | `core/` | Deterministic measurement primitives |
| Layer 1 | `audit/` | Merkle tree construction and proof verification |
| Layer 2 | `compliance/` | Policy enforcement, orchestration, certificates, rendering |
| Layer 3 | `docs/` | Canonical documentation and compliance mapping |

### CORE-005 outcome

CORE-005 repaired layer separation.

- `core/evaluator.py` performs raw measurement only.
- `compliance/evaluator_wrapper.py` is the policy-aware orchestration entry point.
- `compliance/policy.py` contains Layer 2 policy logic.
- `core/policy.py` and `core/consistency.py` remain as **deprecated compatibility wrappers** for v3.3.

---

## 4. REPOSITORY STRUCTURE

```
/audit
  merkle.py                  # MerkleTree and EventTrustCertificate
  verify.py                  # Proof and ETC verification helpers

/compliance
  __init__.py                # Package documentation and public re-exports
  certificate.py             # AuraEventCertificate dataclass
  consistency.py             # Layer 2 consistency calculator
  evaluator_wrapper.py       # Policy-aware orchestration entry point
  policy.py                  # RegulatoryPolicy, PolicyRule, KillSwitch
  renderer.py                # Certificate renderers

/core
  __init__.py
  consistency.py             # Deprecated wrapper -> compliance.consistency
  embedding.py               # Embedding placeholder
  evaluator.py               # PoCAEvaluator (int32 measurement only)
  merkle.py                  # Minimal ETC helper
  offline_normalizer.py      # Offline normalization (float-permitted)
  policy.py                  # Deprecated wrapper -> compliance.policy
  test_ari.py
  test_bitwise_replay.py
  test_integration.py
  test_offline_normalizer.py

/packages
  /database-client
  /zk-passport               # ZK threshold circuit and integration notes

/docs
  architecture.md
  GAP-001.md
  KNOWN_LIMITATIONS.md
  mathematical_foundation.md
  regulatory_compliance.md
  threat_model.md
```

---

## 5. PREFERRED IMPORTS

Use these imports for current code:

```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy, PolicyRule, get_kill_switch
from compliance.consistency import ConsistencyCalculator
```

Deprecated compatibility imports still exist in v3.3, but new documentation and examples use the `compliance.*` modules.

---

## 6. HOW TO USE

### 6.1 Offline normalization

```bash
python core/offline_normalizer.py input.json output.json
```

This is the only repository path where float preprocessing is permitted.

### 6.2 Pure Layer 0 measurement

```python
from core.evaluator import PoCAEvaluator

constitution_vector = [100000, 0, 0]
action_vector = [100000, 0, 0]

evaluator = PoCAEvaluator(constitution_vector)
result = evaluator.evaluate(
    agent_id="machine_agent_001",
    vector=action_vector,
    valid_schema=True,
)
```

`result` contains raw integer-scaled metrics:
- `ari`
- `drift`

### 6.3 Policy-aware orchestration

```python
from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy
from core.evaluator import PoCAEvaluator

constitution_vector = [100000, 0, 0]
action_vector = [100000, 0, 0]

RegulatoryPolicy.validate_target("MACHINE_ACCOUNT")
evaluator = PoCAEvaluator(constitution_vector)
result = evaluate_with_policy(
    evaluator,
    "machine_agent_001",
    action_vector,
    True,
)
```

This is the correct entry point when Layer 2 halt checks and penalties are required.

### 6.4 Determinism verification

```bash
pytest core/test_bitwise_replay.py
```

If any output differs, the instrument is invalid.

---

## 7. REGULATORY POSITION

Aura Protocol enforces:

- **Article 5:** MACHINE_ACCOUNT scope only
- **Article 13:** deterministic, explainable measurement with cryptographic auditability
- **Article 14:** human-activated emergency halt in Layer 2

Aura Protocol performs measurement only. Policy interpretation remains external.

---

## 8. OPERATIONAL GOVERNANCE

See:

- [ROLE_OF_THE_PROTOCOL_CUSTODIAN.md](/ROLE_OF_THE_PROTOCOL_CUSTODIAN.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/mathematical_foundation.md](docs/mathematical_foundation.md)
- [docs/regulatory_compliance.md](docs/regulatory_compliance.md)
- [docs/GAP-001.md](docs/GAP-001.md)
- [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md)

---

## 9. FINAL STATEMENT

This repository is a finished instrument lineage.

Any material change creates a new instrument lineage, not a routine software update.

**Truth is calculated.**
