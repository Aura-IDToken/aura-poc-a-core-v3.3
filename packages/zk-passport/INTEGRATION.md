# Integration Guide: ZK Threshold Circuit ↔ Aura Protocol

## Overview

This document describes the current repository-supported integration point between Aura Protocol and `packages/zk-passport/reputation_check.circom`.

The Python side of the integration is the production of an integer-scaled ARI value.
The circuit side consumes that integer value as `secretARI`.

## Current data flow

```
normalized int32 vectors
        |
        v
core.evaluator.PoCAEvaluator
        |
        +--> raw result: {"ari": int, "drift": int}
        |
        v
optional Layer 2 orchestration
(compliance.evaluator_wrapper.evaluate_with_policy)
        |
        v
circuit input JSON for reputation_check.circom
```

## Current Python integration example

```python
import json

from compliance.evaluator_wrapper import evaluate_with_policy
from compliance.policy import RegulatoryPolicy
from core.evaluator import PoCAEvaluator

constitution_vector = [100000, 0, 0]
action_vector = [100000, 0, 0]
threshold_int = 80000

RegulatoryPolicy.validate_target("MACHINE_ACCOUNT")
evaluator = PoCAEvaluator(constitution_vector)
result = evaluate_with_policy(
    evaluator,
    "machine_agent_001",
    action_vector,
    True,
)

circuit_input = {
    "secretARI": str(result["ari"]),
    "isMachine": "1",
    "schemaIntegrity": "1",
    "threshold": str(threshold_int),
}

with open("input.json", "w", encoding="utf-8") as handle:
    json.dump(circuit_input, handle, indent=2, sort_keys=True)
```

This example uses only APIs that exist in the current repository.

## Integration notes

- `secretARI` is the integer-scaled ARI measurement output.
- `threshold` should also be provided as an integer-scaled value.
- Layer 2 threshold selection is external to Aura Protocol.
- The repository documents the circuit, but does not bundle a complete `circom`/`snarkjs` proof-generation toolchain.

## Import guidance

Use `PoCAEvaluator`, `evaluate_with_policy`, and `RegulatoryPolicy` from the current modules shown above.
These modules define the current repository-supported measurement and orchestration surface.
