# Test Specification: Threshold Check Circuit

## Overview

This document specifies test vectors for `reputation_check.circom`.
All values are integer-scaled.

## Prerequisites

- `circom`
- `snarkjs`
- Node.js runtime suitable for the selected proof workflow

## Test matrix

| Test | secretARI | threshold | isMachine | schemaIntegrity | Expected isVerified |
|------|-----------|-----------|-----------|-----------------|---------------------|
| 1 | 85000 | 80000 | 1 | 1 | 1 |
| 2 | 80000 | 80000 | 1 | 1 | 1 |
| 3 | 75000 | 80000 | 1 | 1 | 0 |
| 4 | 85000 | 80000 | 0 | 1 | constraint failure |
| 5 | 85000 | 80000 | 1 | 0 | constraint failure |
| 6 | 100000 | 80000 | 1 | 1 | 1 |
| 7 | 0 | 80000 | 1 | 1 | 0 |
| 8 | 96000 | 95000 | 1 | 1 | 1 |

## Example input JSON

```json
{
  "secretARI": "85000",
  "isMachine": "1",
  "schemaIntegrity": "1",
  "threshold": "80000"
}
```

## Repository alignment

Python-side ARI production should use current repository APIs only:

```python
from core.evaluator import PoCAEvaluator
from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy
```

Use only current repository APIs; do not rely on nonexistent helpers such as `calculate_ari()`.
