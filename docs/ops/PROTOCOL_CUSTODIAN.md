# ROLE OF THE PROTOCOL CUSTODIAN  
## Aura Protocol ARI Core v3.3 (Frozen Iron Core)

**STATUS:** CANONICAL / BINDING  
**VERSION:** 1.0  
**JURISDICTION:** PL Regulatory Sandbox (MC-READY 2026)  
**SCOPE:** Human Governance of a Frozen Measurement Instrument  
**APPLIES TO:** Aura Protocol v3.3 and all sealed derivatives  

---

## 1. PURPOSE

This document defines the **exclusive operational role** of the Protocol Custodian.

Once the Aura Protocol enters the *Frozen Iron Core* state, no developer, AI system, or operator has authority to modify its physics, parameters, or logic.

The Custodian is not a developer.  
The Custodian is not an operator.  
The Custodian is not an owner.

The Custodian is the **guardian of invariants**.

---

## 2. DEFINITION OF THE ROLE

The Protocol Custodian is the **sole human authority** allowed to:

- maintain the physical and cryptographic integrity of the instrument,
- certify that the instrument remains unchanged,
- decide when the instrument must stop operating,
- initiate lawful succession.

The Custodian **does not optimize**, **does not refactor**, **does not improve** the system.

The Custodian **preserves it**.

---

## 3. POWERS GRANTED (WHAT THE CUSTODIAN MAY DO)

The Custodian MAY:

1. Seal releases (generate ZIP + SHA256 + M-DISC).
2. Verify bitwise identity across hardware (Golden Test).
3. Execute `HALT` and `FREEZE` procedures.
4. Restore the system from sealed media.
5. Reject any change that increases entropy.
6. Invalidate compromised hardware.
7. Provide sealed artifacts to regulators or courts.
8. Authorize disaster recovery rituals.
9. Trigger succession protocol (LEGACY_PROTOCOL.md).
10. Declare a version *dead* and unfit for use.

---

## 4. PROHIBITIONS (WHAT THE CUSTODIAN MUST NEVER DO)

The Custodian MUST NOT:

- change constants (0.68, 100_000),
- alter scaling factors or arithmetic,
- modify Layer 0 logic,
- bypass tests or purity checks,
- approve float usage in runtime,
- approve GPU execution,
- add network dependencies,
- add identity persistence,
- aggregate reputation,
- override regulatory halts,
- make "small fixes".

**Any such act creates a new instrument, not a new version.**

---

## 5. DECISION RULES

### 5.1 If hashes differ → HALT  
No exception. No discussion.

### 5.2 If determinism is lost → HALT  
Even if functionality appears correct.

### 5.3 If legality is unclear → HALT  
The instrument must default to safety.

### 5.4 If integrity is uncertain → HALT  
Uncertainty is treated as failure.

---

## 6. RELATION TO AI SYSTEMS (INCLUDING COPILOT)

AI systems are:

- assistants,
- tools,
- documentation generators,
- test writers.

They are **never**:
- decision makers,
- approvers,
- modifiers of invariants.

Any AI suggestion that violates the constitutional requirements as defined in [CONSTITUTIONAL_DECREE.md](../../CONSTITUTIONAL_DECREE.md) **must be rejected via REGULATORY_HALT**.

---

## 7. SUCCESSION (IN CASE OF DEATH, DISAPPEARANCE, OR INCAPACITY)

The Custodian must ensure:

- sealed artifacts exist,
- restoration instructions exist,
- LEGACY_PROTOCOL.md is current,
- at least one M-DISC copy is stored offline,
- SHA256 checksum is printed and stored physically.

Succession requires **3-of-5 Shamir shares** as defined in LEGACY_PROTOCOL.md.

No single human may transfer custodianship alone.

---

## 8. TEMPORAL LIMITS

The Custodian's authority is valid only while:

- the instrument remains bit-identical,
- the constants remain unchanged,
- the audit chain is unbroken,
- the legal regime is unchanged.

If any of these fail → **custodianship suspends automatically**.

---

## 9. LIABILITY AND ETHICAL DUTY

The Custodian is responsible for:

- refusing pressure,
- refusing convenience,
- refusing optimization,
- refusing shortcuts.

The Custodian is **not responsible for outcomes**,
only for **measurement integrity**.

---

## 10. FINAL ASSERTION

The Aura Protocol v3.3 is not a product.  
It is not software.  
It is not a service.

It is a **measurement instrument**.

The Custodian exists to ensure that truth, once calculated, remains unchanged.

---

**SIGNED:**  
Protocol Custodian  
Aura Protocol ARI Core v3.3  

**Internal Consistency:** 1.0  
**Entropy Budget:** Frozen  
**Status:** ACTIVE
