# FORBIDDEN ACTIONS — HARD FAIL

Copilot must STOP if any of the following occurs:

❌ Adding thresholds to core (Layer 0)
❌ Using floats in runtime
❌ Using cosine similarity with sqrt
❌ Adding ML models
❌ Aggregating reputation across sessions
❌ Adding owner_id, wallet_id, user_id
❌ Adding network calls
❌ Using GPU
❌ Changing Sentinel 0.68
❌ Changing scaling factor 10^5
❌ Adding convenience abstractions
❌ Refactoring without explicit task

If a forbidden action is requested:
→ Respond with REGULATORY_HALT
