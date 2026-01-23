# ALLOWED TASKS — AURA v3.3

Copilot may ONLY work on tasks listed below.

## TASK-01 (DONE)
core/offline_normalizer.py
- Offline only
- Float allowed
- Output must be int32
- Deterministic JSON

## TASK-02 (DONE)
packages/zk-passport/reputation_check.circom
- Integer only
- Binary output
- Art.5 gate
- SI gate

## TASK-03 (REQUIRED)
core/test_bitwise_replay.py
- Run on x86
- Run on ARM
- Run on WASM
- Assert identical hash

## TASK-04 (OPTIONAL)
core/wasm_quantizer/
- Implement DET_02
- No SIMD
- No FMA
- No float

## TASK-05 (DOCUMENTATION ONLY)
ADR_005_NO_FLOAT_RUNTIME.md
- Explain removal of float
- Map to DET_01 / DET_02
