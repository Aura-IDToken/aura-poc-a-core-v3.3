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

**Status:** ✅ RESOLVED (fixed in CORE-005, 2026-07-24)
**Risk:** N/A — resolved
**Discovered:** 2026-01-24
**Resolved:** 2026-07-24
**Reporter:** Constitutional Compliance Audit
**Resolution:** CORE-005 Layer Separation Repair

### Description

The `evaluate()` method previously returned a `status` field that interpreted the ARI measurement:

```python
"status": "COMPLIANT" if ari > self.COMPLIANCE_THRESHOLD else "RISK"
```

### Violation

This violated **Constitutional Decree Article I, Section 6 (Layer Separation)**:

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

**Target Version:** v3.3 (completed ahead of schedule)

**Remediation completed in CORE-005 (2026-07-24):**
1. ✅ Removed the `status` field from `core/evaluator.py`
2. ✅ Removed the `COMPLIANCE_THRESHOLD` constant from Layer 0
3. ✅ Moved threshold interpretation to the `compliance/` layer (`compliance/policy.py`)
4. ✅ Updated all tests to check raw metrics (`ari`, `drift`) only
5. ✅ Created `compliance/evaluator_wrapper.py` as the Layer 2 orchestrator

### Resolution Verification

- ✅ CHECK 2 (Integer Only): PASS
- ✅ CHECK 3 (Layer Separation): PASS
- ✅ `core/evaluator.py` returns only `{"ari": int, "drift": int}` — no status field
- ✅ All 58 tests pass

### Why Fixed Now?

CORE-005 was implemented before v3.3 seal to resolve this layer violation while preserving backward compatibility via deprecated wrappers in `core/policy.py` and `core/consistency.py`.

### Acceptance Criteria

This anomaly was **acceptable** at the time because:

- ✅ It did not compromise determinism
- ✅ It did not violate bit-identity
- ✅ It did not affect regulatory compliance
- ✅ Auditors were notified
- ✅ Workaround was documented
- ✅ Remediation plan existed (now completed)

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
