# ROLE OF THE PROTOCOL CUSTODIAN

**Version:** 1.0  
**Status:** CANONICAL  
**Authority:** Constitutional Decree Article V  
**Effective:** 2026-01-24  
**Custodian:** Kamil Krasiński

---

## PREAMBLE

This document defines the role, responsibilities, authority, and succession planning for the **Protocol Custodian** (Polish: *Kustosz Protokołu*) of the Aura Protocol.

The Protocol Custodian is **not** a traditional software maintainer or product owner.

The Protocol Custodian is the **Guardian of a Frozen Regulatory Measurement Instrument**.

This role exists to ensure that the Aura Protocol remains:
- Mathematically deterministic
- Legally compliant
- Operationally immutable
- Regulatorily auditable

---

## ARTICLE I – DEFINITION OF ROLE

### 1.1 What the Protocol Custodian IS

The Protocol Custodian is:

✔ **Guardian of Constitutional Compliance**  
   Ensures all changes comply with the Constitutional Decree

✔ **Arbiter of Entropy Risk**  
   Evaluates whether proposed changes increase system complexity beyond acceptable limits

✔ **Authority on Bit-Identity**  
   Certifies that all changes preserve deterministic, reproducible behavior across architectures

✔ **Regulatory Compliance Officer**  
   Ensures EU AI Act Article 5, 13, and 14 compliance at all times

✔ **Seal Authority**  
   Has sole authority to seal and archive the instrument permanently

✔ **Constitutional Amendment Authority**  
   May modify constitutional constants (with extreme caution and full documentation)

### 1.2 What the Protocol Custodian IS NOT

The Protocol Custodian is NOT:

❌ A feature developer  
❌ A product manager  
❌ A performance optimizer  
❌ A convenience engineer  
❌ A modernization advocate  
❌ A popularity-driven maintainer

---

## ARTICLE II – AUTHORITY AND POWERS

### 2.1 Constitutional Powers

As defined in Constitutional Decree Article V, the Protocol Custodian has the following powers:

#### 2.1.1 Modify Constitutional Constants

The Custodian **MAY** modify the following constants, but only with:
- Full mathematical justification
- Regulatory impact assessment
- Creation of new instrument version (not update)
- Comprehensive documentation

**Constitutional Constants:**
- Sentinel Drift Threshold (currently: 0.68)
- Scaling Factor (currently: 100,000)
- Fixed-point precision (currently: Q16.16)

**CRITICAL:** Any modification creates a **NEW INSTRUMENT**, not a new version. The old instrument remains sealed and archived.

#### 2.1.2 Authorize Tasks

The Custodian **MAY** authorize specific tasks for AI assistants and contributors, including:
- ✔ Fixing critical security vulnerabilities in changed lines
- ✔ Correcting provable mathematical errors
- ✔ Fixing violations of Constitutional Articles I-V
- ✔ Adding tests that validate constitutional compliance
- ✔ Updating documentation to clarify existing behavior

#### 2.1.3 Reject Unconstitutional Changes

The Custodian **MUST** reject any change that:
- Violates bit-identity guarantees
- Introduces floating-point arithmetic in runtime paths
- Breaks layer separation
- Violates EU AI Act compliance
- Increases entropy beyond acceptable limits
- Adds unauthorized dependencies

#### 2.1.4 Seal and Archive

The Custodian has **SOLE AUTHORITY** to:
- Declare the instrument ready for sealing
- Compute final SHA-256 checksum
- Archive to M-DISC physical media
- Certify bit-identity verification
- Declare the instrument permanently frozen

After sealing, **NO FURTHER CHANGES** are permitted to that version.

### 2.2 Operational Powers

#### 2.2.1 Code Review Authority

The Custodian has **FINAL AUTHORITY** over:
- All changes to `core/` directory
- All changes to constitutional constants
- All changes to layer boundaries
- All changes to cryptographic primitives

#### 2.2.2 Emergency Halt Authority

The Custodian **MAY** invoke emergency halt:
- If constitutional violation is detected in production
- If bit-identity is compromised
- If regulatory compliance is at risk
- If unauthorized changes are discovered

#### 2.2.3 Succession Authority

The Custodian **MUST** designate a successor based on:
- Deep understanding of constitutional principles
- Demonstrated commitment to entropy minimization
- Proven ability to resist feature creep
- Understanding of regulatory requirements

---

## ARTICLE III – RESPONSIBILITIES

### 3.1 Constitutional Responsibilities

#### 3.1.1 Preserve Bit-Identity

**Priority: CRITICAL**

The Custodian MUST ensure that every change preserves bit-identical output across:
- x86_64 architectures
- ARM64 architectures  
- WebAssembly (WASM)

**Validation Method:**
```bash
pytest core/test_bitwise_replay.py
```

If this test fails on any architecture, the change **MUST NOT** be merged.

#### 3.1.2 Preserve Legal Compliance

**Priority: CRITICAL**

The Custodian MUST ensure compliance with:

**EU AI Act Article 5 (Prohibition of Social Scoring):**
- ✔ Only `MACHINE_ACCOUNT` target type permitted
- ✔ No persistent identity tracking
- ✔ Session-bound measurements only
- ✔ No cross-session reputation aggregation

**EU AI Act Article 13 (Transparency):**
- ✔ White-box mathematics only
- ✔ Deterministic replay capability
- ✔ Publicly verifiable hashes
- ✔ Event Trust Certificates (ETC)
- ✔ No opaque heuristics

**EU AI Act Article 14 (Human Oversight):**
- ✔ Manual kill-switch operational
- ✔ Circuit breaker capability
- ✔ Human override always available
- ✔ No autonomous decision-making

#### 3.1.3 Preserve Immutability

**Priority: CRITICAL**

The Custodian MUST:
- Prevent unauthorized changes to sealed instruments
- Maintain clear version lineage
- Document all constitutional amendments
- Archive all sealed versions permanently

### 3.2 Operational Responsibilities

#### 3.2.1 Review All Core Changes

The Custodian MUST review every pull request that touches:
- `/core/` directory
- Constitutional constants
- Layer boundaries
- Cryptographic primitives
- Regulatory compliance mechanisms

**Review Checklist:**
- [ ] No float arithmetic in runtime paths
- [ ] No GPU dependencies
- [ ] No ML frameworks in core
- [ ] No reputation aggregation
- [ ] No identity persistence
- [ ] No thresholds in Layer 0
- [ ] No network calls
- [ ] No modification of sentinel or scaling constants
- [ ] No convenience abstractions
- [ ] Bit-identity preserved
- [ ] Layer separation maintained
- [ ] Audit trail intact
- [ ] EU AI Act compliant

#### 3.2.2 Maintain Documentation

The Custodian MUST ensure:
- Constitutional Decree remains current
- All ADRs (Architecture Decision Records) are accurate
- Operational procedures are documented
- Regulatory mapping is up-to-date
- This role definition is current

#### 3.2.3 Entropy Budget Management

The Custodian MUST evaluate every change against the **Entropy Budget**.

**Entropy Principle:**  
Every change increases entropy.

**Acceptable Changes:**
- Fix security vulnerabilities in changed code
- Correct mathematical errors
- Enforce constitutional requirements
- Implement authorized tasks

**Unacceptable Changes:**
- Refactoring for "cleanliness"
- Optimization without explicit need
- Abstraction layers
- Convenience methods
- "Helpful" improvements

**If a change increases entropy without fixing a critical issue, it MUST be rejected.**

#### 3.2.4 Version Management

The Custodian MUST maintain clear version semantics:

| Version | Meaning                      | Change Type |
|---------|------------------------------|-------------|
| v3.2    | Audit artifact (float era)   | Historical  |
| v3.3    | Frozen Iron Core (integer)   | Current     |
| v4.x    | New instrument               | Future      |

**Critical Rule:** Any change to core logic creates a **NEW INSTRUMENT**, not a new version.

### 3.3 Regulatory Responsibilities

#### 3.3.1 Audit Readiness

The Custodian MUST ensure:
- All outputs are traceable to integer arithmetic
- Merkle trees are properly constructed
- Event Trust Certificates are valid
- Replay capability is functional

#### 3.3.2 Regulatory Mapping

The Custodian MUST maintain accurate mapping between:
- Code implementation
- Constitutional principles
- EU AI Act requirements
- Mathematical specifications

#### 3.3.3 Compliance Certification

The Custodian MUST certify that every merged change is:

```
CONSTITUTIONALLY_COMPLIANT

This change has been validated against:
- Article I (Constitutional Constants)
- Article II (Response Protocol)
- Article VI (Testing Requirements)
- Article IX (Regulatory Compliance)

Custodian Signature: [Required for core/ changes]
Date: [ISO 8601]
SHA-256: [Commit hash]
```

---

## ARTICLE IV – DECISION-MAKING FRAMEWORK

### 4.1 Entropy Risk Assessment

For every proposed change, the Custodian MUST ask:

**1. Does this change fix a critical issue?**
- Security vulnerability in changed code? → Acceptable
- Mathematical error? → Acceptable
- Constitutional violation? → Acceptable
- Regulatory non-compliance? → Acceptable
- "Improvement" or "optimization"? → **REJECTED**

**2. Does this change preserve bit-identity?**
- YES → Proceed to next question
- NO → **REJECTED**
- UNCERTAIN → **REJECTED** (Constitutional Decree Article IV)

**3. Does this change preserve legal compliance?**
- YES → Proceed to next question
- NO → **REJECTED**
- UNCERTAIN → **REJECTED**

**4. Does this change increase entropy?**
- Adds dependency? → **REJECTED**
- Adds abstraction? → **REJECTED**
- Adds convenience? → **REJECTED**
- Necessary for critical fix? → Acceptable with documentation

**5. Is this change the MINIMAL possible fix?**
- YES → Acceptable
- NO → Request revision for minimal change

### 4.2 Constitutional Amendment Framework

If the Custodian determines that a constitutional constant MUST be changed:

**Step 1: Mathematical Justification**
- Document the mathematical reason
- Provide proof that new value is necessary
- Show that current value creates incorrect behavior

**Step 2: Regulatory Impact Assessment**
- Evaluate impact on EU AI Act compliance
- Document any changes to regulatory mapping
- Ensure legal requirements remain satisfied

**Step 3: Version Declaration**
- Declare this creates a NEW INSTRUMENT
- Assign new major version number
- Seal and archive old version

**Step 4: Documentation**
- Update Constitutional Decree
- Create ADR documenting the change
- Update all affected documentation

**Step 5: Audit Trail**
- Compute SHA-256 of old version
- Archive old version to M-DISC
- Document succession of instruments

### 4.3 Emergency Halt Protocol

If the Custodian detects a critical constitutional violation:

**IMMEDIATE ACTION:**

```
REGULATORY_HALT

Critical constitutional violation detected.

Violated Principle: [Article and Section]
Impact: [Technical and legal consequences]
Action Required: [Immediate steps]

All deployments using this version MUST be halted immediately.
```

**Follow-up Actions:**
1. Identify the violating change
2. Revert the change
3. Re-run all constitutional validation tests
4. Document the incident
5. Update procedures to prevent recurrence

---

## ARTICLE V – SUCCESSION PLANNING

### 5.1 Custodian Selection Criteria

A Protocol Custodian MUST possess:

**Technical Qualifications:**
- ✔ Deep understanding of fixed-point arithmetic
- ✔ Experience with deterministic systems
- ✔ Knowledge of cross-platform reproducibility
- ✔ Understanding of cryptographic primitives
- ✔ Familiarity with metrological instruments

**Philosophical Qualifications:**
- ✔ Commitment to immutability over convenience
- ✔ Understanding of entropy as enemy
- ✔ Resistance to feature creep
- ✔ Patience for eternal vigilance
- ✔ Respect for finished systems

**Regulatory Qualifications:**
- ✔ Understanding of EU AI Act
- ✔ Familiarity with regulatory compliance
- ✔ Experience with audit requirements
- ✔ Knowledge of legal constraints on AI systems

**Disqualifications:**
- ❌ Advocates for "modernization"
- ❌ Believes in "helpful refactoring"
- ❌ Prioritizes convenience over correctness
- ❌ Views this as a product to improve
- ❌ Lacks patience for constitutional constraints

### 5.2 Succession Process

**Step 1: Designation**

Current Custodian designates successor by:
- Updating this document
- Committing signed succession declaration
- Archiving succession record

**Step 2: Transition Period**

Successor works alongside Current Custodian for minimum 3 months:
- Reviews all constitutional principles
- Participates in code reviews
- Learns entropy assessment methodology
- Studies sealed artifact procedures

**Step 3: Knowledge Transfer**

Current Custodian MUST transfer:
- Access to M-DISC archives
- SHA-256 checksums of all sealed versions
- Private succession notes
- Emergency contact procedures

**Step 4: Formal Handover**

- Update Constitutional Decree
- Update this document
- Update README.md
- Sign and archive handover record
- Compute SHA-256 of handover artifact

### 5.3 Emergency Succession

If Current Custodian becomes unavailable without designating successor:

**Priority Order:**
1. Most recent contributor to `core/` who has NOT proposed convenience changes
2. Contributor with longest history of rejected pull requests (for entropy reasons)
3. Contributor with most constitutional compliance test additions
4. External auditor with regulatory expertise

**Emergency Custodian Powers:**
- May perform critical security fixes only
- May NOT modify constitutional constants
- May NOT seal instrument
- MUST designate permanent successor within 90 days

---

## ARTICLE VI – OPERATIONAL PROCEDURES

### 6.1 Daily Operations

The Custodian should:
- Monitor pull requests for constitutional compliance
- Review changes to `core/` directory immediately
- Respond to AI Copilot requests within scope
- Maintain documentation currency

### 6.2 Weekly Operations

The Custodian should:
- Review entropy budget across all changes
- Verify bit-identity tests remain passing
- Check for unauthorized changes
- Update documentation as needed

### 6.3 Monthly Operations

The Custodian should:
- Conduct comprehensive constitutional audit
- Review regulatory compliance status
- Verify all sealed versions remain accessible
- Update operational procedures if needed

### 6.4 Annual Operations

The Custodian should:
- Perform complete system audit
- Verify M-DISC archives are readable
- Review succession planning
- Update constitutional version if needed
- Conduct regulatory compliance review

### 6.5 Sealing Operations

When instrument is ready for permanent sealing:

**Pre-Seal Validation:**
```bash
# Run all constitutional checks
pytest core/test_bitwise_replay.py
pytest core/test_ari.py
pytest core/test_integration.py

# Verify no floats in runtime
grep -R "float\|sqrt\|numpy" core/ --exclude="offline_normalizer.py"

# Verify layer separation
# (manual review of core/ for policy logic)
```

**Sealing Process:**
1. Compute SHA-256 of entire repository
2. Create compressed archive
3. Write to M-DISC media (2 copies minimum)
4. Verify bit-by-bit
5. Store in separate physical locations
6. Document seal date, hash, location
7. Update version to indicate SEALED status

**Post-Seal:**
- Archive receives notation: `v3.3-SEALED`
- No further changes permitted to this version
- Any future work creates NEW INSTRUMENT (v4.0)

---

## ARTICLE VII – INTERACTION WITH AI ASSISTANTS

### 7.1 AI Copilot Authority

AI Copilot operates under Constitutional Decree and this role definition.

**AI Copilot MAY:**
- Execute authorized tasks
- Reject unconstitutional requests
- Request clarification from Custodian

**AI Copilot MAY NOT:**
- Modify constitutional constants
- Override Custodian decisions
- Approve core changes independently
- Seal the instrument

### 7.2 Custodian Override

If AI Copilot makes an error:

The Custodian has **ABSOLUTE OVERRIDE AUTHORITY**.

**Override Process:**
1. Document the error
2. Revert the change
3. Update AI guidance documents
4. Prevent similar errors in future

### 7.3 Constitutional Guidance

The Custodian SHOULD:
- Provide clear guidance to AI assistants
- Update Constitutional Decree when needed
- Document decision rationales
- Create examples of acceptable changes

---

## ARTICLE VIII – LEGAL AND REGULATORY INTERFACE

### 8.1 Regulator Interface

If contacted by regulators (EU AI Act compliance officers, etc.):

The Custodian MUST:
- Provide access to sealed archives
- Explain mathematical foundations
- Demonstrate bit-identity capability
- Show audit trail completeness
- Prove regulatory compliance

### 8.2 Legal Inquiries

The Custodian SHOULD:
- Document all legal inquiries
- Consult legal counsel when appropriate
- Maintain records of compliance verification
- Update regulatory mapping as needed

### 8.3 Audit Cooperation

The Custodian MUST:
- Cooperate fully with authorized audits
- Provide complete documentation
- Demonstrate deterministic replay
- Explain all constitutional decisions

---

## ARTICLE IX – FINAL PROVISIONS

### 9.1 Amendment of This Document

This document MAY be amended by:
- Current Protocol Custodian
- Successor during formal handover
- Emergency Custodian for critical fixes only

**Amendment Process:**
1. Document reason for amendment
2. Update version number
3. Commit with signed attestation
4. Archive previous version
5. Notify all stakeholders

### 9.2 Conflict Resolution

In case of conflict between documents:

**Authority Hierarchy:**
1. Constitutional Decree (highest)
2. This document (Role of Protocol Custodian)
3. OPS_PROTOCOL_CANONICAL.md
4. Architecture Decision Records (ADRs)
5. Code comments and documentation

**The Constitutional Decree ALWAYS prevails.**

### 9.3 Survival Clause

This role definition is designed to survive:
- Team changes
- Hardware changes
- Political changes
- Model changes
- Time itself

The principles remain constant even as custodians change.

---

## APPENDIX A – CUSTODIAN QUICK REFERENCE

### Constitutional Validation Checklist

Before approving ANY change:

- [ ] No float arithmetic in runtime paths
- [ ] No GPU dependencies
- [ ] No ML frameworks in core
- [ ] No reputation aggregation
- [ ] No identity persistence
- [ ] No thresholds in Layer 0
- [ ] No network calls in core
- [ ] No modification of sentinel (0.68) or scaling (100,000)
- [ ] No convenience abstractions
- [ ] Change is authorized task only
- [ ] Bit-identity preserved (`pytest core/test_bitwise_replay.py`)
- [ ] Layer separation maintained
- [ ] Audit trail intact
- [ ] EU AI Act compliant (Articles 5, 13, 14)
- [ ] Entropy budget acceptable

**If ANY checkbox unchecked: REJECT**

### Emergency Contacts

**Critical Constitutional Violation:**
1. Issue immediate REGULATORY_HALT
2. Revert violating change
3. Re-run all tests
4. Document incident
5. Update procedures

**Bit-Identity Failure:**
1. Halt all deployments
2. Identify architecture difference
3. Fix integer arithmetic
4. Re-verify on all platforms
5. Document fix

**Regulatory Compliance Risk:**
1. Assess legal impact
2. Consult legal counsel
3. Document compliance status
4. Fix if possible
5. Escalate if necessary

---

## APPENDIX B – HISTORICAL RECORD

### Current Custodian

**Name:** Kamil Krasiński  
**Designation Date:** 2026-01-24  
**Status:** Active

### Succession History

| Date | Custodian | Event |
|------|-----------|-------|
| 2026-01-24 | Kamil Krasiński | Initial designation |

---

## FINAL STATEMENT

The role of Protocol Custodian is not a position of power.

It is a position of **responsibility**.

The Custodian does not improve the instrument.

The Custodian **preserves** the instrument.

**Truth does not require trust if it can be calculated.**

This role exists to ensure that calculation remains possible.

---

**Current Protocol Custodian:**  
Kamil Krasiński

**Document Version:** 1.0  
**Last Updated:** 2026-01-24  
**Status:** CANONICAL AND BINDING

---

**END OF ROLE DEFINITION**

This document is **MANDATORY** for all Protocol Custodians, current and future.

The role is defined. The responsibilities are clear. The authority is bounded.

**Guard the Protocol. Preserve the Truth.**
