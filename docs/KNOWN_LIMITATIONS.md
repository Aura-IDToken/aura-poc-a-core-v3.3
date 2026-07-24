# KNOWN LIMITATIONS
## Aura Protocol v3.3 Iron Core

**STATUS:** INFORMATIONAL  
**VERSION:** 1.0  
**SCOPE:** POC Phase Known Anomalies  
**AUTHORITY:** Protocol Custodian  

---

## Purpose

This document tracks known technical limitations and architectural anomalies in Aura Protocol v3.3 that:
- Do not compromise bit-identity or determinism
- Do not violate EU AI Act compliance
- Are understood, documented, and acceptable within POC scope
- Will be addressed in future instrument lineages (v4.x+)

**These are NOT bugs or security vulnerabilities.**

They are **architectural debt** acknowledged for transparency.

---

## KL-001: evaluator.py contains legacy interpretation logic

**Location:** `core/evaluator.py:94`

**Status:** Known Anomaly  
**Risk:** Low (POC scope only)  
**Discovered:** 2026-01-24  
**Reporter:** Constitutional Compliance Audit  

### Description

The `evaluate()` method returns a `status` field that interprets the ARI measurement:

```python
"status": "COMPLIANT" if ari > self.COMPLIANCE_THRESHOLD else "RISK"
```

### Violation

This violates **Constitutional Decree Article I, Section 6 (Layer Separation)**:

- ❌ Layer 0 (`core/`) should MEASURE only
- ❌ Layer 2 should DECIDE (thresholds, allow/deny)
- ❌ Interpretation logic belongs in `compliance/` or `audit/` layer

### Impact

**Technical:**
- Does not affect bit-identity (threshold comparison is deterministic)
- Does not affect measurement accuracy (ARI calculation is unaffected)
- Violates architectural separation of concerns

**Regulatory:**
- No EU AI Act violation (interpretation is transparent and traceable)
- Audit trail remains intact (raw ARI value is still returned)

**Operational:**
- External auditors can ignore the `status` field
- Raw ARI score is the normative measurement
- Layer 2 components can re-interpret based on their own thresholds

### Mitigation

**For Auditors:**
- Interpretation logic is **non-normative**
- Use raw `ari` and `drift` values only
- Ignore the `status` field in compliance decisions

**For Integrators:**
- Do NOT rely on `status` field for production decisions
- Implement threshold logic in Layer 2 (compliance layer)
- Use raw metrics for policy enforcement

### Resolution Plan

**Target Version:** v4.x (next instrument lineage)

**Remediation:**
1. Remove the `status` field from `core/evaluator.py`
2. Remove the `COMPLIANCE_THRESHOLD` constant from Layer 0
3. Move threshold interpretation to the `compliance/` layer
4. Update all tests to check raw metrics only
5. Update integration contracts to remove the `status` dependency

**Blocked By:**
- Requires backward-incompatible API change
- Requires audit of all downstream consumers
- Requires Layer 2 policy module implementation

### Why Not Fixed Now?

1. **POC Scope:** Current implementation is demonstration-grade
2. **Audit Status:** External auditors have been instructed to ignore `status`
3. **Migration Cost:** Removing would require coordinated downstream changes
4. **Risk Assessment:** Low priority (does not affect correctness or compliance)
5. **Instrument Freeze:** v3.3 is approaching seal; changes deferred to v4.x

### Acceptance Criteria

This anomaly is **acceptable** because:

- ✅ It does not compromise determinism
- ✅ It does not violate bit-identity
- ✅ It does not affect regulatory compliance
- ✅ Auditors have been notified
- ✅ Workaround is documented
- ✅ Remediation plan exists for next lineage

---

## Future Limitations

Additional known limitations will be documented here as they are discovered.

### Template for New Entries

```
## KL-XXX: [Short description]

**Location:** [File:line or module]
**Status:** Known Anomaly | Accepted Debt | Scheduled Fix
**Risk:** Critical | High | Medium | Low
**Discovered:** [Date]
**Reporter:** [Source]

### Description
[Detailed explanation]

### Violation
[Which principle/article is violated]

### Impact
[Technical, regulatory, operational consequences]

### Mitigation
[How to work around this limitation]

### Resolution Plan
[How and when this will be fixed]
```

---

## Escalation

If a new limitation is discovered that:

- Compromises bit-identity
- Violates EU AI Act compliance
- Breaks deterministic replay
- Creates security vulnerability

It is **NOT** a "known limitation"—it is a **CRITICAL BUG** and must trigger:

```
REGULATORY_HALT
```

See: [CONSTITUTIONAL_DECREE.md](/CONSTITUTIONAL_DECREE.md) Article II

---

**Custodian Signature:**  
Protocol Custodian  
Aura Protocol ARI Core v3.3  

**Document Version:** 1.0  
**Last Updated:** 2026-01-25  
**Status:** ACTIVE AND INFORMATIONAL  

---

**Truth is calculated. Trust is obsolete.**
