# LEGACY PROTOCOL
## Succession and Disaster Recovery for Aura Protocol v3.3

**STATUS:** CANONICAL / BINDING  
**VERSION:** 1.0  
**JURISDICTION:** PL Regulatory Sandbox (MC-READY 2026)  
**SCOPE:** Custodian Succession and Emergency Recovery  
**APPLIES TO:** Aura Protocol v3.3 and all sealed derivatives  

---

## 1. PURPOSE

This document defines the **succession protocol** for the Protocol Custodian role and the **disaster recovery procedures** for the Aura Protocol measurement instrument.

In the event of:
- death of the current Custodian,
- disappearance of the current Custodian,
- incapacity of the current Custodian,
- voluntary resignation,
- revocation due to breach of duty,

this protocol ensures continuity of custodianship without compromising the integrity of the frozen instrument.

---

## 2. SUCCESSION MECHANISM: 3-OF-5 SHAMIR SECRET SHARING

### 2.1 Master Key Structure

The **Master Custodian Key** is split into 5 shares using Shamir's Secret Sharing Scheme.

Reconstruction requires **any 3 of the 5 shares**.

### 2.2 Shareholder Roles

Shares are distributed to:

1. **Legal Representative** (lawyer, notary)
2. **Technical Continuity Officer** (senior engineer)
3. **Regulatory Liaison** (compliance officer)
4. **Independent Auditor** (external third party)
5. **Institutional Archive** (university, foundation, or escrow service)

### 2.3 Activation Conditions

Succession is triggered when:

- The current Custodian is confirmed deceased, OR
- The current Custodian has been unreachable for **90 consecutive days**, OR
- The current Custodian formally declares incapacity, OR
- A court order mandates succession.

### 2.4 Reconstruction Procedure

1. **Notification:** All 5 shareholders are notified of the succession event.
2. **Quorum:** At least 3 shareholders must physically meet or use cryptographic multi-party computation.
3. **Share Presentation:** Each participating shareholder presents their share.
4. **Key Reconstruction:** The Master Custodian Key is reconstructed.
5. **Verification:** The reconstructed key must successfully decrypt the sealed artifact checksums.
6. **Transfer:** A new Custodian is appointed and receives the reconstructed key.

### 2.5 Security Requirements

- Shares must be stored in physically separate locations.
- Shares must be encrypted at rest.
- No shareholder may know the identity of more than 2 other shareholders.
- Shareholders must not be employed by the same organization.

---

## 3. SEALED ARTIFACTS (REQUIRED FOR SUCCESSION)

The following artifacts must be sealed and accessible via the succession protocol:

1. **Source Code Archive**
   - Complete git repository snapshot
   - SHA-256 checksum: `[COMPUTED_AT_SEALING_v3.3]`

2. **Binary Distributions**
   - All compiled artifacts
   - SHA-256 checksums for each

3. **Restoration Instructions**
   - Hardware requirements
   - Execution environment setup
   - Golden Test verification procedure

4. **Cryptographic Proofs**
   - Merkle tree root hashes
   - Audit trail signatures
   - Constitutional checksum chain

5. **Legal Documentation**
   - License agreements
   - Regulatory certifications
   - Compliance attestations

### 3.1 Physical Storage

All sealed artifacts must exist in at least **2 independent physical locations**:

- **Primary:** M-DISC stored in climate-controlled vault
- **Secondary:** M-DISC stored in geographically separate location

### 3.2 Verification Ritual

Upon succession, the new Custodian must:

1. Retrieve sealed artifacts from physical storage.
2. Verify SHA-256 checksums match sealed manifest.
3. Execute Golden Test on reference hardware.
4. Confirm bit-identical output.
5. Sign new custodianship certificate.

---

## 4. EMERGENCY HALT AUTHORITY

In case of:
- Suspected cryptographic compromise,
- Regulatory invalidation,
- Legal prohibition,
- Detected determinism failure,

**Any shareholder** may trigger **EMERGENCY_HALT** by:

1. Publishing signed halt declaration.
2. Notifying all other shareholders.
3. Initiating succession protocol.

### 4.1 Halt Declaration Format

```
EMERGENCY_HALT

Reason: [Technical | Legal | Security]
Triggering Event: [Specific description]
Timestamp: [ISO 8601]
Shareholder Signature: [Cryptographic signature]

This declaration invalidates all active measurements until succession is complete.
```

---

## 5. CONTINUITY REQUIREMENTS

### 5.1 Custodian Obligations

The current Custodian must:

- Update sealed artifacts within 30 days of any authorized change.
- Verify shareholder contact information annually.
- Ensure LEGACY_PROTOCOL.md remains current.
- Maintain at least 2 physically separate sealed copies.

### 5.2 Shareholder Obligations

Each shareholder must:

- Protect their share with the highest level of cryptographic security, equivalent to classified state secrets.
- Report compromise of their share within 24 hours.
- Maintain current contact information.
- Acknowledge succession notifications within 72 hours.

---

## 6. SUCCESSION CEREMONY

The formal transfer of custodianship requires:

1. **Invocation:** 3 shareholders present their shares.
2. **Verification:** Reconstruct Master Key and verify artifacts.
3. **Attestation:** New Custodian signs oath of preservation.
4. **Certification:** Legal witness certifies transfer.
5. **Publication:** Succession is announced in public registry.

### 6.1 Oath of Preservation

The new Custodian must recite:

> "I solemnly affirm that I will:
> - preserve the integrity of this measurement instrument,
> - refuse all pressure to modify its invariants,
> - reject optimization and convenience,
> - execute HALT when integrity is uncertain,
> - maintain the audit chain unbroken,
> - transfer custodianship lawfully when my time ends.
>
> I am not a developer. I am not an operator. I am not an owner.
> I am the guardian of invariants.
>
> Truth is calculated. Trust is obsolete."

---

## 7. REVOCATION (IN CASE OF BREACH)

If the Custodian:
- Modifies constitutional constants without authority,
- Approves float usage in runtime,
- Bypasses mandatory tests,
- Compromises bit-identity,

Then **any 2 shareholders** may initiate **REVOCATION** by:

1. Publishing signed revocation declaration.
2. Triggering succession protocol.
3. Appointing emergency interim Custodian.

### 7.1 Interim Custodianship

During revocation proceedings, an **Interim Custodian** is appointed with powers limited to:

- Execute HALT and FREEZE.
- Preserve sealed artifacts.
- Prevent further changes.

The Interim Custodian **may not** approve new changes until succession is complete.

---

## 8. FINAL PROVISIONS

### 8.1 Protocol Immutability

This LEGACY_PROTOCOL.md is **constitutionally protected**.

Changes require:
- Unanimous consent of all 5 shareholders, AND
- Current Custodian approval, AND
- Legal counsel review, AND
- Regulatory compliance verification.

### 8.2 Jurisdictional Continuity

If the legal jurisdiction changes:
- Succession protocol remains valid.
- Shareholders may be replaced to match new jurisdiction.
- Custodianship continues without interruption.

### 8.3 Time Horizon

This protocol is designed to function for **at least 50 years** beyond the last active use of the instrument.

---

**SIGNED:**  
Protocol Custodian  
Aura Protocol ARI Core v3.3  

**Succession Mechanism:** 3-of-5 Shamir Secret Sharing  
**Sealed Artifact Locations:** 2 (minimum)  
**Status:** ACTIVE AND BINDING  

---

**Truth is calculated. Trust is obsolete.**
