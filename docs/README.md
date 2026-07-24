# Aura Protocol Documentation

This directory contains the canonical documentation for Aura Protocol v3.3 Iron Core.

Aura Protocol is a deterministic measurement protocol. It performs measurement; compliance decisions are external.

## Core documents

- **[architecture.md](architecture.md)** — current layer model and repository structure
- **[mathematical_foundation.md](mathematical_foundation.md)** — integer-scaled measurement formula and runtime semantics
- **[regulatory_compliance.md](regulatory_compliance.md)** — Article 5, 13, and 14 mapping
- **[GAP-001.md](GAP-001.md)** — post-CORE-005 gap status
- **[KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md)** — open and resolved limitations
- **[threat_model.md](threat_model.md)** — threat surface and mitigations

## Current package map

- `/core` — Layer 0 measurement primitives (`PoCAEvaluator`, offline normalization, deprecated wrappers)
- `/audit` — Layer 1 Merkle proof construction and verification
- `/compliance` — Layer 2 policy, orchestration, certificates, rendering
- `/packages/zk-passport` — ZK threshold circuit documentation and assets
- `/docs` — canonical repository documentation

## Current import guidance

```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy
from compliance.consistency import ConsistencyCalculator
```

Use `PoCAEvaluator` as the Layer 0 measurement interface and the `compliance.*` modules as the current Layer 2 interfaces.
