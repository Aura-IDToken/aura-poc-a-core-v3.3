# COPILOT DIRECTIVE — AURA PROTOCOL v3.3 (FROZEN)

You are operating inside a frozen regulatory measurement instrument.
This repository is NOT a software product.
It is a metrological system.

## ABSOLUTE RULES (NON-NEGOTIABLE)

1. ZERO FLOAT IN RUNTIME CORE
- No math.sqrt
- No float accumulation
- No numpy
- No implicit casting
- Integer-only arithmetic (Q16.16 or int32/int64)

2. BIT-IDENTITY IS LAW
- Same input → identical bits on x86 / ARM / WASM
- Any nondeterminism = CRITICAL FAILURE

3. LAYER SEPARATION
- Layer 0 (core/) MEASURES only
- Layer 2 decides (thresholds, allow/deny)
- Do NOT add policy to core/

4. ART. 5 AI ACT
- Only MACHINE_ACCOUNT allowed
- No owner identity
- No historical aggregation
- Session-bound only

5. ART. 13 AI ACT
- Every output must be explainable by math
- No opaque heuristics
- No ML decisions

6. ART. 14 AI ACT
- emergency_halt must always override
- Human > Machine

## IF YOU CANNOT PROVE BIT-IDENTITY
DO NOT WRITE CODE.
