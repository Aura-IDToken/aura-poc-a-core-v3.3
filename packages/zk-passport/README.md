# ZK Passport: Threshold Check Circuit

## Overview

This package contains the `reputation_check.circom` threshold circuit used to prove that an integer-scaled ARI measurement meets or exceeds a supplied threshold without revealing the exact ARI value.

The circuit consumes repository-generated integer values.
It does not call the Python runtime directly.

## Current repository integration point

Aura Protocol produces the measurement value with:

```python
from core.evaluator import PoCAEvaluator
```

For policy-aware flows, use:

```python
from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy
```

The resulting `result["ari"]` integer is the value passed to the circuit as `secretARI`.

## Circuit inputs

### Private inputs
- `secretARI`
- `isMachine`
- `schemaIntegrity`

### Public input
- `threshold`

All values are integer-scaled.

## Notes

- The repository does not expose a Python `calculate_ari()` helper.
- The repository does not expose a `generateProof()` or `verifyProof()` helper in this package.
- Proof-generation tooling is external to this repository.
