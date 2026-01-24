# AI Copilot and Contributor Guide

## ⚠️ MANDATORY READING

Before making ANY changes to this repository, you MUST read:

**[CONSTITUTIONAL DECREE FOR AI COPILOT](/CONSTITUTIONAL_DECREE.md)**

This decree is **MANDATORY**, **BINDING**, and **PERMANENT**.

Failure to comply with the Constitutional Decree voids the regulatory certification of this instrument.

## Quick Constitutional Checklist

Before ANY change, verify:

- [ ] No float arithmetic in runtime paths
- [ ] No GPU dependencies
- [ ] No ML frameworks in core
- [ ] No reputation aggregation
- [ ] No identity persistence
- [ ] No thresholds in Layer 0
- [ ] No network calls
- [ ] No modification of sentinel (0.68) or scaling (100,000)
- [ ] No convenience abstractions
- [ ] Authorized task only
- [ ] Bit-identity preserved
- [ ] Layer separation maintained
- [ ] Audit trail intact
- [ ] EU AI Act compliant

**If ANY checkbox is unchecked:** REGULATORY_HALT

## Validation Tools

Before submitting any change, run:

### 1. Constitutional Compliance Check
```bash
bash scripts/check_constitutional_compliance.sh
```

### 2. Constitutional Purity Check
```bash
python3 scripts/verify_constitutional_purity.py
```

### 3. All Mandatory Checks
```bash
bash scripts/run_all_checks.sh
```

## If You Violate the Constitution

If a request violates constitutional principles, AI Copilot will respond with:

```
REGULATORY_HALT

Violated Principle: [Article and section]
Reason (Technical): [Why this violates determinism]
Reason (Legal): [Regulatory implication]
Compliant Alternative: [Alternative approach or "None available"]
```

## Authority Hierarchy

1. **Custodian of the Protocol** (Architect)
   - May modify constitutional constants
   - May authorize new tasks
   - May seal and archive the instrument

2. **AI Copilot / Contributors**
   - May execute authorized tasks
   - May reject unconstitutional requests
   - May NOT modify core principles

3. **The Constitution**
   - ALWAYS prevails in conflicts

## Key Principles

### This is NOT a Product

This repository is a **frozen regulatory measurement instrument**.

It is not:
- A software product
- A service
- A platform
- An SDK

It is:
- A metrological system
- A measurement device
- A regulatory compliance tool

### Optimization = Entropy

- Do NOT "improve" core logic
- Do NOT refactor for convenience
- Do NOT optimize for speed or memory
- Do NOT add abstraction layers

Every change increases entropy.

### Measurement, Not Decision

Layer 0 (core/) **MEASURES ONLY**

It does not:
- Make decisions
- Enforce thresholds
- Apply policy
- Allow/deny actions

Layer 2 (outside core/) makes decisions.

## Regulatory Compliance

### EU AI Act Article 5 - No Social Scoring

✔ Only `MACHINE_ACCOUNT` target type  
✔ Session-bound measurements only  
✔ No identity persistence  
✔ No historical aggregation  

### EU AI Act Article 13 - Transparency

✔ White-box mathematics  
✔ Deterministic replay  
✔ Publicly verifiable  
✔ No opaque heuristics  

### EU AI Act Article 14 - Human Oversight

✔ Manual kill-switch  
✔ Circuit breaker  
✔ Human override always permitted  

## Resources

- [Constitutional Decree](/CONSTITUTIONAL_DECREE.md) - **MANDATORY READING**
- [README.md](/README.md) - Repository overview
- [Architecture Documentation](/docs/architecture.md)
- [Regulatory Compliance](/docs/regulatory_compliance.md)
- [ADR 005: No Float Runtime](/docs/ADR_005_NO_FLOAT_RUNTIME.md)

## Questions?

If you are uncertain whether a change violates the constitution:

**REFUSE THE CHANGE**

Contact the Custodian of the Protocol for guidance.

---

**Truth does not require trust if it can be calculated.**

Compliance is not optional.
