# FORBIDDEN ACTIONS — HARD FAIL

⚠️ **See [CONSTITUTIONAL_DECREE.md](/CONSTITUTIONAL_DECREE.md) for complete rules.**

Copilot must STOP if any of the following occurs:

❌ Adding thresholds to core (Layer 0)
❌ Using floats in runtime
❌ Using cosine similarity with sqrt
❌ Adding ML models
❌ Aggregating reputation across sessions
❌ Adding owner_id, wallet_id, user_id
❌ Adding network calls
❌ Using GPU
❌ Changing Sentinel drift threshold (0.68)
❌ Changing scaling factor (10^5 integer multiplier)
❌ Adding convenience abstractions
❌ Refactoring without explicit task

## Response Protocol

If a forbidden action is requested:
1. Respond with `REGULATORY_HALT`
2. Cite the specific violated rule
3. Explain the regulatory/technical reason
4. Suggest compliant alternatives if applicable
