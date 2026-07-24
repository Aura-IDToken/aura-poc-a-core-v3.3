# Aura Protocol: Mathematical Foundation

## Measurement outputs

Aura Protocol v3.3 produces integer-scaled measurement outputs.

- `ari` — primary measurement value
- `drift` — distance from full semantic alignment

Both values use a scaling factor of `100000`.

## Layer 0 evaluator

The canonical Layer 0 evaluator is `core.evaluator.PoCAEvaluator`.

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

## Fixed-point formula

The runtime formula is implemented with integer arithmetic only:

```text
ari = max(0, (30000 * SI // 100000) + (70000 * SA // 100000) - P)
```

Where:
- `SI` = structural integrity, either `100000` or `0`
- `SA` = semantic alignment from the fixed-point dot product
- `P` = Layer 2 penalty value supplied to Layer 0

## Semantic alignment

For pre-normalized vectors:

```text
SA = dot(action_vector, constitution_vector) // 100000
```

No runtime float arithmetic, cosine normalization, or square-root operations are used in Layer 0.

## Drift

The current implementation computes drift as:

```text
drift = min(max(0, 100000 - SA), 200000)
```

`drift` is also integer-scaled.

## Offline preprocessing boundary

`core/offline_normalizer.py` is the repository's float-permitted preprocessing tool.

It is used to convert float vectors into the fixed-point representation consumed by the runtime core.

## Determinism check

```python
from core.evaluator import PoCAEvaluator

constitution_vector = [100000, 0, 0]
action_vector = [100000, 0, 0]

evaluator = PoCAEvaluator(constitution_vector)
left = evaluator.evaluate("machine_agent_001", action_vector, True)
right = evaluator.evaluate("machine_agent_001", action_vector, True)
assert left == right
```

## Layer separation note

Policy thresholds, halt checks, and interpretation are not part of the Layer 0 formula.
They are handled by Layer 2 modules such as `compliance.policy` and `compliance.evaluator_wrapper`.
