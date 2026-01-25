# COPILOT DIRECTIVE — AURA PROTOCOL v3.3 (FROZEN)

⚠️ **CONSTITUTIONAL AUTHORITY:** This repository is governed by [CONSTITUTIONAL_DECREE.md](/CONSTITUTIONAL_DECREE.md)

**READ THE CONSTITUTIONAL DECREE BEFORE MAKING ANY CHANGES.**

You are operating inside a frozen regulatory measurement instrument.
This repository is NOT a software product.
It is a metrological system.

The directives below summarize the Constitutional Decree. In case of conflict, the full decree prevails.

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

---

## CANONICAL NAMING RULES FOR AI ASSISTANTS (MANDATORY)

You are assisting in a repository that defines a regulatory measurement
instrument. Language errors can create legal risk.

You MUST follow these rules:

1. Use **"Aura Protocol"** when referring to the system in documentation.

2. Never describe Aura Protocol as:
   - an AI system
   - a decision engine
   - a monitoring platform
   - a product or service

3. Always describe Aura Protocol as:
   > "a deterministic measurement protocol"

4. Use **PoCA** only to refer to the measurement method.

5. Use **v3.3 Iron Core** only to refer to the frozen instrument instance.

6. Never write:
   - ❌ "Aura decides"
   - ❌ "Aura evaluates humans"
   - ❌ "Aura ensures compliance"

7. Always write:
   - ✅ "Aura Protocol performs measurement"
   - ✅ "Compliance decisions are external"

8. If you cannot maintain this distinction, DO NOT write text.
