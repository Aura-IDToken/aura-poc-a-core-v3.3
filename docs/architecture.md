# Aura Protocol Architecture

## Current flow

```
Normalized int32 vectors
        |
        v
compliance.policy.RegulatoryPolicy
        |
        v
compliance.evaluator_wrapper.evaluate_with_policy()
        |
        v
core.evaluator.PoCAEvaluator.evaluate()
        |
        +--> core.merkle.MerkleAttestor (minimal ETC helper)
        |
        +--> audit.merkle.MerkleTree / audit.verify (Merkle proof layer)
        |
        v
compliance.certificate / compliance.renderer
```

## Layer responsibilities

| Layer | Modules | Responsibility |
|------|---------|----------------|
| Layer 0 | `core.evaluator`, `core.merkle`, `core.offline_normalizer` | Deterministic measurement primitives |
| Layer 1 | `audit.merkle`, `audit.verify` | Merkle proof construction and verification |
| Layer 2 | `compliance.policy`, `compliance.evaluator_wrapper`, `compliance.consistency`, `compliance.certificate`, `compliance.renderer` | Policy enforcement, orchestration, reporting |
| Layer 3 | `docs/` | Canonical documentation |

## CORE-005 synchronization

CORE-005 moved policy-aware orchestration out of Layer 0.

- `core.evaluator.PoCAEvaluator.evaluate()` returns raw integer-scaled measurement fields only.
- `compliance.evaluator_wrapper.evaluate_with_policy()` is the current policy-aware entry point.
- `compliance.policy.RegulatoryPolicy` owns halt checks and penalty logic.
- `core.policy` and `core.consistency` are deprecated wrappers retained for compatibility in v3.3.

## Repository structure

```
aura-poc-a-core-v3.3/
├── audit/
│   ├── merkle.py
│   └── verify.py
├── compliance/
│   ├── __init__.py
│   ├── certificate.py
│   ├── consistency.py
│   ├── evaluator_wrapper.py
│   ├── policy.py
│   └── renderer.py
├── core/
│   ├── consistency.py      # deprecated wrapper
│   ├── embedding.py
│   ├── evaluator.py
│   ├── merkle.py
│   ├── offline_normalizer.py
│   └── policy.py           # deprecated wrapper
├── docs/
├── packages/
│   ├── database-client/
│   └── zk-passport/
└── scripts/
```

## Preferred imports

```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy, PolicyRule, get_kill_switch
from compliance.consistency import ConsistencyCalculator
```
