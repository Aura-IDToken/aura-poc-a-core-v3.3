# KNOWN LIMITATIONS
## Aura Protocol v3.3 Iron Core

**STATUS:** INFORMATIONAL  
**VERSION:** 1.1  
**SCOPE:** Current limitations and resolved records  
**AUTHORITY:** Protocol Custodian  

---

## Open limitations

No open limitations are currently tracked in this document for the CORE-005 synchronization scope.

---

## Resolved record

### KL-001: Layer 0 interpretation logic in `core/evaluator.py`

**Status:** ✅ RESOLVED  
**Resolved in:** CORE-005  
**Resolved on:** 2026-07-24

The legacy `status` interpretation field was removed from `core/evaluator.py`.
Policy-aware interpretation now belongs to Layer 2.

Current repository state:
- `core.evaluator.PoCAEvaluator.evaluate()` returns raw measurement fields only
- `compliance.evaluator_wrapper.evaluate_with_policy()` is the policy-aware orchestration entry point
- `compliance.policy` contains policy and halt logic
- `core.policy` and `core.consistency` are deprecated compatibility wrappers for v3.3

---

**Document Version:** 1.1  
**Last Updated:** 2026-07-24  
**Status:** ACTIVE AND INFORMATIONAL
