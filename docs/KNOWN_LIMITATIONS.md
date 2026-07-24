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

## KL-001: evaluator.py contained legacy interpretation logic

**Location:** `core/evaluator.py` (v3.2 and earlier)

**Status:** ✅ RESOLVED — SUPERSEDED BY CORE-005  
**Risk:** N/A (resolved)  
**Discovered:** 2026-01-24  
**Resolved:** 2026-07-24 (CORE-005)  
**Reporter:** Constitutional Compliance Audit  

### Description

The `evaluate()` method previously returned a `status` field that interpreted the ARI measurement:

```python
# REMOVED — was present in v3.2:
"status": "COMPLIANT" if ari > self.COMPLIANCE_THRESHOLD else "RISK"
```

### Resolution

CORE-005 (2026-07-24) removed the `status` field and the `COMPLIANCE_THRESHOLD` constant
from `core/evaluator.py`. The method now returns only raw numeric metrics:

```python
return {
    "ari": ari,    # int32, scaled by 10^5 — measurement only
    "drift": drift, # int32, scaled by 10^5 — measurement only
}
```

Policy enforcement (threshold decisions, halt checks) is now handled exclusively by
`compliance/evaluator_wrapper.py` (Layer 2), in compliance with the Constitutional
Decree layer-separation invariant.

**Verification:** `check_3_layer_separation.sh` — PASSED post-CORE-005.

---

## KL-002: Deprecated compatibility wrappers in core/

**Location:** `core/policy.py`, `core/consistency.py`

**Status:** Accepted Architectural Debt — Scheduled removal in v4.0  
**Risk:** Low (emit DeprecationWarning; no functional impact)  
**Discovered:** 2026-07-24 (CORE-005 gap analysis)  
**Reporter:** CORE-005 implementation  

### Description

As part of CORE-005, `core/policy.py` and `core/consistency.py` were converted from
production modules to backward-compatibility wrappers that re-export their counterparts
from the `compliance/` layer. Both files:

- Emit a `DeprecationWarning` at import time
- Re-export classes from `compliance.policy` / `compliance.consistency`
- Violate the Layer 0 purity principle by importing from Layer 2

### Impact

- Does not affect measurement correctness or bit-identity
- Does not affect test results (test imports updated to use `compliance.*` directly)
- Wrappers are excluded from `check_3_layer_separation.sh` by design

### Resolution Plan

**Target Version:** v4.0 (next instrument lineage)

1. Delete `core/policy.py`
2. Delete `core/consistency.py`
3. Update CHECK 3 to remove wrapper exclusions
4. Update all external code to import from `compliance.*`

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
