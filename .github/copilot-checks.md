# EXECUTION CHECKS — MANDATORY

Every change MUST pass:

## CHECK 1 — Bit Identity
Run tests on:
- x86
- ARM
Hashes MUST match exactly.

## CHECK 2 — Integer Only
grep -R "float\|sqrt\|numpy" core/
must return NOTHING

## CHECK 3 — Layer Separation
core/ must not:
- return booleans of compliance
- enforce thresholds
- contain business logic

## CHECK 4 — Audit Path
Every metric must be traceable to:
- integer math
- Merkle leaf
- ETC field

## CHECK 5 — Entropy
If change increases entropy:
REJECT

If any check fails:
DO NOT MERGE
