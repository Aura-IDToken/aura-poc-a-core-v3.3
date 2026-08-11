# DR-002 — EVIDENCE PACKAGE

**Decision Authority Model — Evidence Acquisition**

| Field | Value |
|---|---|
| Document ID | DR-002_EVIDENCE_PACKAGE |
| Version | 1.0-DRAFT |
| Status | DRAFT — EVIDENCE ACQUISITION ONLY |
| Date | 2026-08-11 |
| Author | Claude — architectural & conformance audit role (`CLAUDE.md`) |
| Parent artifact | `ARCHITECTURE-RESOLUTION-001.md` §3.3, §14 DR-002 |
| Parent commit | `af5036d` |
| Normative effect | **NONE** |

---

> **THIS DOCUMENT DECIDES NOTHING.**
>
> It does not select a role. It does not rename, merge, split, or reconcile roles. It does not
> recommend Chief Architect, Protocol Custodian, Architecture Board, Architecture Review Board,
> Release Authority, Compliance Authority, or any other body as the correct authority. It
> creates no governance, modifies no governance, and creates no ADR.
>
> It is an **evidence inventory**. Interpretation is confined to §5 (ambiguity) and §6
> (contradiction), and in both cases the interpretation is *"these sources permit more than one
> reading"* — never *"this reading is correct."*

### Exclusion rules applied

Per the task's standing constraint, the following were **not** used as authority evidence, and
no authority is inferred from any of them:

| Excluded source of inference | Handling |
|---|---|
| Repository ownership | Not consulted for authority. |
| Commit authorship | Not consulted. |
| GitHub permissions / CODEOWNERS mechanism | The `@AuraIDToken` mappings are **excluded**. The *prose comment* inside one CODEOWNERS file is recorded in §2 as a documentary statement naming a role, and is explicitly marked non-authoritative. |
| Job titles | Not consulted. |
| Previous conversations | Not consulted. Every entry below is re-derived from file text at the stated path. |
| Implementation behaviour | Not consulted. |

### Path correction

The task statement locates the parent artifact at
`review/2026-08-11_SPEC-002_ARCH_REVIEW/ARCHITECTURE-RESOLUTION-001.md`. Its actual path at
commit `af5036d` is the **repository root**: `ARCHITECTURE-RESOLUTION-001.md`. This package is
filed at the requested path. No file was moved.

### Repositories inspected

| Ref | Repository | Revision |
|---|---|---|
| **S1** | `AuraIDToken/aura-specification` | `62d2d6b` (`main`) |
| **S2** | `aura-nomos/aura-specification` | `eb2a4ec` (`main`) |
| **S3** | `AuraIDToken/aura-poc-a-core-v3.3` | `9c6a5d8` (`main`) |

Method: exhaustive `grep` across all `*.md` and `*.txt` in S1, S2 and S3 for the strings
`Chief Architect`, `Protocol Custodian`, `Custodian of the Protocol`, `Custodian`,
`Architecture Review Board`, `Architecture Board`, `Release Authority`, `Compliance Authority`,
`Decision Owner`, `Documentation Architect`, `Specification Contributor`. Every hit is
represented below or in §2.7.

---

## 1. Decision Question

> **Which role/body has authority to make and approve the architectural decisions required by
> SPEC-002?**

### 1.1 Decomposition

The question as posed resolves into five sub-questions, each independently unanswered by the
evidence in §2. They are listed to make the scope of the decision precise; **none is answered
here**.

| # | Sub-question |
|---|---|
| Q1 | Which role/body may **approve a SPEC-class document** (SPEC-002 itself)? |
| Q2 | Which role/body may **accept an ADR** that resolves an AD-CA decision domain? |
| Q3 | Which role/body may **accept or reject an RFC**, if AD-CA decisions require one? |
| Q4 | Are "Chief Architect" and "Protocol Custodian" the **same office**, distinct offices, or offices with distinct scopes? |
| Q5 | Are "Architecture Review Board" and "Architecture Board" the **same body**? Do "Release Authority" and "Compliance Authority / Auditor" exist as constituted bodies? |

### 1.2 Why the question is prior to all others

`ARCHITECTURE-RESOLUTION-001.md` §5 requires a "decision authority" value for each of
AD-CA-001 … AD-CA-012. That column could not be filled. Consequently DR-002 gates the other 26
entries in that register — not by preference, but because an unapproved decision is not a
decision, and approval requires an identified approver.

---

## 2. Evidence Inventory

Ordered by document authority level as declared in each document's own front matter, not by
significance.

---

### 2.1 AURA Constitution

| Field | Value |
|---|---|
| Path | `S1: constitution/AURA_CONSTITUTION.md` |
| Document ID | `AURA-CON-001` |
| Version / Status | `1.0` / **FROZEN** |
| Note | The **only FROZEN document** in S1. `releases/v0.1.0/DOCUMENT_STATUS.md` confirms: `AURA Constitution | AURA-CON-001 | 1.0 | FROZEN`. |

**E-2.1.1 — Front matter, line 7**
> `Owner: Chief Architect`

*Role named:* Chief Architect. *Authority described:* ownership of the Constitution document.

**E-2.1.2 — Article VIII "Authority", line 137**
> "The Chief Architect is responsible for the project."

*Role named:* Chief Architect. *Authority described:* responsibility for the project — stated
without enumeration, delegation rule, or scope boundary.

**E-2.1.3 — Article VIII, lines 139–146**
> "AI systems MAY:
> - Analyse
> - Propose
> - Implement
> - Prepare tests
> - Support documentation
>
> AI systems MUST NOT approve changes to canonical documents or modify frozen documents."

*Role named:* AI systems. *Authority described:* a prohibition. Note this is the **only**
role-scoping statement in the Constitution besides E-2.1.2.

**E-2.1.4 — Article XI "Amendment Procedure", lines 176–181**
> "Amendment of the Constitution requires:
> 1. An RFC
> 2. An Architecture Review
> 3. An impact analysis
> 4. Updates to dependent documents
> 5. Approval by the Chief Architect"

*Role named:* Chief Architect. *Authority described:* approval of Constitution amendments.
*Body referenced but not named:* whoever conducts "An Architecture Review".

**E-2.1.5 — Article VI "Governance Artifacts", lines 97–107**
> Table listing ADR, ARR, RFC, ADC, ACI, ADM, EPR with a Purpose column only.
> "Every artifact has an identifier, version, owner, and status."

*Roles named:* **none**. The Constitution requires each artifact have an "owner" but names no
owner for any artifact class, and defines no artifact class named SPEC.

**E-2.1.6 — Article V "Canonical Hierarchy", lines 75–89**
> `AURA Constitution → Aura Protocol Specification (APS-001) → Protocol Invariants (APS-100) →
> ADR / ARR / RFC → Aura Development Playbook → Repository Documentation → Implementation`

*Roles named:* none. *Relevance:* the hierarchy contains **no SPEC class**, so the Constitution
assigns no authority over SPEC documents because it does not contemplate them.

> **Summary of Constitution evidence.** The Constitution names exactly **one** role —
> Chief Architect — plus the category "AI systems". It names **no board, no committee, no
> Custodian, no Release Authority, and no Compliance Authority.** It never uses the string
> "Protocol Custodian".

---

### 2.2 GOV-001 — Governance

| Field | Value |
|---|---|
| Path | `S1: GOVERNANCE.md` |
| Document ID | `GOV-001` |
| Version / Status | `1.0-DRAFT` / **DRAFT** (confirmed by `releases/v0.1.0/DOCUMENT_STATUS.md`) |
| Declared Authority | `AURA Constitution v1.0 (FROZEN)` |

**E-2.2.1 — §2 "Authority Hierarchy", lines 17–30 (verbatim)**
```
Chief Architect
        │
        ├── AURA Constitution (FROZEN — immutable)
        │
        ├── Architecture Review Board (ARB)
        │       └── conducts ARRs
        │
        ├── Specification Contributors
        │       └── author APS, ADRs, RFCs
        │
        └── AI Assistants
                └── may propose, implement, test; may NOT approve or freeze
```

*Roles/bodies named:* Chief Architect · **Architecture Review Board (ARB)** · Specification
Contributors · AI Assistants. *Authority described:* a tree in which the Constitution appears
as a *child node of the Chief Architect* — see §5 A-6.

**E-2.2.2 — §2, lines 32–37**
> "The Chief Architect has final and sole approval authority over:
> - AURA Constitution amendments
> - APS document status transitions (APPROVED → FROZEN)
> - Protocol Invariant additions or removals
> - New reference implementation recognition"

*Role named:* Chief Architect. *Authority described:* **an enumerated, closed list of four
items.** *Scope observation, recorded as fact:* the list does **not** include SPEC-class
documents, ADR acceptance, RFC acceptance, or the `DRAFT → REVIEW` and `REVIEW → APPROVED`
transitions.

**E-2.2.3 — §3 "Governance Artifacts", lines 42–51**

| Artifact | Purpose | Owner |
|---|---|---|
| ADR | Architecture Decision Record | **Decision author** |
| ARR | Architecture Review Record | Chief Architect |
| RFC | Request for Comments | **Proposer** |
| ADC | Architecture Decision Confidence | Chief Architect |
| ACI | Architecture Conformance Inspection | Chief Architect |
| EPR | Evidence Pack Report | **Implementer** |

*Roles named:* Decision author · Chief Architect · Proposer · Implementer. *Authority
described:* **ownership**, which the table does not equate with approval. No SPEC row exists.

**E-2.2.4 — §5.1 "Minor Changes (PATCH)", line 74**
> "4. Chief Architect **or delegate** may merge"

*Roles named:* Chief Architect; **"delegate"** (undefined — see §7 M-6). *Scope:* PATCH-class
changes only.

**E-2.2.5 — §5.2 "Major Changes (MINOR/MAJOR)", lines 78–86**
> "1. Open an RFC in `/rfcs/`
> 2. RFC enters DRAFT status
> 3. Community comment period (minimum 14 days)
> 4. **Architecture Review Board assessment**
> 5. **Chief Architect approval**
> 6. RFC transitions to APPROVED
> 7. Implementation via pull request referencing RFC
> 8. ADR created if architectural decision is embedded"

*Bodies named:* Architecture Review Board; Chief Architect. *Authority described:* ARB
"assessment" (character unspecified — advisory or binding is not stated); Chief Architect
"approval".

**E-2.2.6 — §5.3 "Constitution Amendments", line 95**
> "5. Chief Architect approval"

*Consistent with* E-2.1.4.

**E-2.2.7 — §6 "ADR Process", lines 104–111**
> "1. Copy `templates/ADR_TEMPLATE.md`
> 2. Assign next sequential `ADR-NNN` identifier
> 3. Fill all required sections
> 4. Submit as pull request
> 5. Link to any related RFC
> 6. **Merging the PR = accepting the ADR**
> 7. ADR status set to ACCEPTED"

*Roles named:* **NONE.** *Authority described:* acceptance is attached to the act of merging,
with **no actor specified**. This is the single most consequential gap in the inventory for Q2.

**E-2.2.8 — §7 "RFC Process", lines 126–128**
> "7. **Architecture Review Board votes: ACCEPT / REJECT / DEFER**
> 8. **Chief Architect final approval**
> 9. RFC transitions to ACCEPTED or REJECTED"

*Bodies named:* ARB (votes) · Chief Architect (final approval). *Note:* here the ARB "votes",
whereas in E-2.2.5 it "assesses". Whether these are the same act is not stated.

**E-2.2.9 — §8 "Review Meetings", lines 136–139**
> "- Held as needed, triggered by RFC acceptance or major milestone
> - **Chaired by Chief Architect**
> - ARR published to `/adrs/ARR-NNN_TITLE.md` within 5 days of meeting"

**E-2.2.10 — §9 "AI Assistant Policy", lines 145–158**
> "Per AURA Constitution Article VIII:
> AI assistants MAY: Analyze and propose · Implement changes once an RFC/ADR is approved ·
> Prepare tests and documentation · Flag specification gaps
> AI assistants MUST NOT: Self-approve changes to canonical documents · Freeze or deprecate
> documents · **Override the Chief Architect's decisions** · Introduce undocumented protocol
> behavior"

**E-2.2.11 — §10 "Conflict Resolution", lines 163–170**
> "In case of ambiguity, the priority order is:
> 1. Mission of the project … 2. AURA Constitution principles … 3. Conformance with protocol
> … 4. Determinism … 5. Auditability (AURA Constitution Article XII)"

*Roles named:* none. *Relevance:* the repository's own conflict-resolution rule orders
**principles**, not **authorities**, and therefore does not resolve DR-002.

---

### 2.3 SPEC-002 v0.3

| Field | Value |
|---|---|
| Path | `S1: specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` |
| Document ID | `SPEC-002` |
| Version / Status | `0.3-DRAFT` / **DRAFT** |
| Declared Authority | `AURA Constitution v1.0 (FROZEN) · APS-000 · APS-200 · APS-300 · APS-400 · APS-900` |

**E-2.3.1 — Front matter, line 7**
> `Owner: Protocol Custodian`

*Role named:* **Protocol Custodian.** *Authority described:* ownership of SPEC-002.
*Recorded fact:* neither the Constitution nor GOV-001 uses this string anywhere.

**E-2.3.2 — Line 11**
> "**Normative effect: NONE until APPROVED.**"

*Roles named:* none. *Authority described:* an approval event is required, **with no approver
identified anywhere in the document.**

**E-2.3.3 — §9 "Acceptance Criteria", line 471**
> "SPEC-002 MAY advance from DRAFT only when all of the following are true: …"

Sixteen criteria follow. *Roles named:* **none.** No criterion identifies who determines that a
criterion is met, and no criterion names an approver.

**E-2.3.4 — §6, and §3 constraint 4**
> "…unless and until **explicit architectural authority** approves them."
> "The identifiers below are local placeholders … and MUST be replaced by approved architecture
> decisions before SPEC-002 advances beyond DRAFT."

*Role named:* "explicit architectural authority" — **an unbound term.** *Authority described:*
approval of AD-CA decisions. *Recorded fact:* SPEC-002 asserts that such an authority must act,
and never identifies it.

> **Summary of SPEC-002 evidence.** SPEC-002 declares an Owner (Protocol Custodian), requires
> approval by an "explicit architectural authority", and identifies that authority nowhere.

---

### 2.4 ADR-001_DOCUMENT_MODEL

| Field | Value |
|---|---|
| Path | `S1: adrs/ADR-001_DOCUMENT_MODEL.md` |
| Document ID | `ADR-001` *(collides — see §6 C-7)* |
| Status | **PROPOSED** |
| Date | 2026-08-02 |
| Not indexed in | `adrs/README.md` |

**E-2.4.1 — Front matter, lines 6–7**
> `Authors: Chief Specification Architect`
> `Decision Owner: Protocol Custodian`

*Roles named:* **"Chief Specification Architect"** — a **fifth** distinct architect-titled
string appearing nowhere else in either repository — and Protocol Custodian.

**E-2.4.2 — "Owners and Authorities", lines 54–57 (verbatim)**
> "- **Protocol Custodian**: approves SPECs, is owner of SPEC lifecycle, and is signatory for
> normative acceptance.
> - **Architecture Board**: approves and owns ARC baselines and ADRs related to architecture
> decisions.
> - **Release Authority**: owns APS publication and release mechanics.
> - **Compliance Authority / Auditor**: owns TRACEABILITY artifacts and evidence retention
> policy."

*Bodies named:* Protocol Custodian · **Architecture Board** · **Release Authority** ·
**Compliance Authority / Auditor**. *Authority described:* the **only** text in either
repository that grants SPEC approval authority to anyone.

**E-2.4.3 — "Lifecycle Summary", lines 75–77**
> "4. ARC … **ACCEPTED by Architecture Board**
> 5. SPEC … **APPROVED by Protocol Custodian**
> 6. APS … **Published by Release Authority**"

**E-2.4.4 — Lines 24, 29–30, 36–37**
> "- Ownership: Architecture Board (owner/approver)." *(ARC)*
> "- Lifecycle: DRAFT → REVIEW → APPROVED → FROZEN. A SPEC becomes frozen only after explicit
> approval by the Protocol Custodian."
> "- Ownership: Protocol Custodian (owner/approver for normative acceptance)." *(SPEC)*
> "- Lifecycle: Composed from frozen SPECs, released by Release Authority."
> "- Ownership: Release Authority (owner/approver for publication)." *(APS)*

**E-2.4.5 — "Open Questions (require Protocol Custodian resolution)", lines 98–101**
> "- Exact **approval thresholds and sign-off procedure for Architecture Board and Protocol
> Custodian (quorum, signature format)**."

*Recorded fact:* the document that grants these authorities **states on its own face that the
procedure for exercising them is undefined.**

**E-2.4.6 — "Status and Acceptance", line 105**
> "This ADR is **PROPOSED** and requires explicit approval by the Protocol Custodian. Approval
> is recorded by adding an `Accepted-by: <Protocol Custodian>` line and merging this ADR into
> the repository's canonical branch."

*Recorded fact:* the document is **self-referentially blocked** — the Protocol Custodian role
whose approval it requires is constituted by no document other than itself and its own
divergent copy (§2.5).

---

### 2.5 `docs/adr/001-document-model.md` — divergent second copy

| Field | Value |
|---|---|
| Path | `S1: docs/adr/001-document-model.md` |
| Document ID | `ADR-001` *(collides — see §6 C-7)* |
| Status | **DRAFT** (differs from §2.4's PROPOSED) |
| Not indexed in | `adrs/README.md` |

**E-2.5.1 — Line 49, present only in this copy**
> "- authority: canonical authority (Protocol Custodian, Architecture Board, Release Authority)"

**E-2.5.2 — "Merge Blockers (Draft PR Checklist — MUST be satisfied before ACCEPTED)", lines 115–116**
> "- [ ] **Protocol Custodian approval (required)**
> - [ ] **Architecture Board approval (required)**"

*Recorded fact:* this copy requires **two** approvals; the `adrs/` copy (E-2.4.6) requires
**one**. Both claim identifier `ADR-001`.

**E-2.5.3 — "Acceptance procedure", line 126**
> "This ADR is DRAFT until Protocol Custodian adds an `accepted_by` entry and the PR is merged."

*vs* E-2.4.6, which specifies an `Accepted-by:` line. The two copies specify **different field
names** for recording the same approval.

---

### 2.6 Remaining S1 sources

**E-2.6.1 — `arc/README.md`, line 10** *(no document ID, no version, no status)*
> "ARC documents are authored outside the normal ADR process when the Architecture Baseline has
> been formally accepted by the **Architecture Board/Protocol Custodian**."

*Authority described:* acceptance of ARC baselines, attributed to two bodies joined by an
unexplained solidus — see §5 A-3.

**E-2.6.2 — `templates/SPEC_TEMPLATE.md`, lines 9 and 32**
> Line 9: `Owner: Role / Name (**Protocol Custodian / Chief Architect**)`
> Line 32: "The SPEC must be accepted by the **Protocol Custodian**."

*Recorded fact:* line 9 presents the two roles as interchangeable fill-in options; line 32 of
the same file names only one. The template is **internally inconsistent**. It is the **only
place in either repository where the two strings appear together**, and it does not equate them.

**E-2.6.3 — `VERSIONING.md`** — Document ID `POL-VER-001`, Version `1.0-DRAFT`, Authority
`AURA Constitution Article XI`
> §3 line 48: "`REVIEW → APPROVED`: **Chief Architect** approves after Architecture Review"
> §3 line 49: "`APPROVED → FROZEN`: Explicit freeze decision by **Chief Architect**; requires
> Amendment Procedure (Constitution Article XI)"
> §10 line 119: "Changes to this versioning policy require an RFC per CONTRIBUTING.md and
> approval by the **Chief Architect**."

*Authority described:* status transitions for "every APS document and governance artifact"
(§1 scope). *Recorded fact:* VERSIONING.md governs **all** artifacts and names **only** the
Chief Architect. It does not use the string "Protocol Custodian" anywhere.

**E-2.6.4 — `README.md`, line 154**
> "- **Chief Architect**: holds sole approval authority over canonical documents"

*Scope described:* "canonical documents", broader than GOV-001 §2's four-item list (E-2.2.2)
and unqualified as to SPEC.

**E-2.6.5 — `CONTRIBUTING.md`, §"Types of Contribution" table**
> "| New APS section / requirement | RFC → Architecture Review → PR |"
> "| New Protocol Invariant | RFC → Architecture Review → PR |"
> "| New Conformance Test | RFC → PR referencing RFC |"
> "| Constitution amendment | RFC → **Architecture Review → Chief Architect approval** |"

*Recorded fact:* only the Constitution row names an approver. The APS and Invariant rows
terminate at "PR" with **no approver named** — although GOV-001 §2 (E-2.2.2) reserves Invariant
additions to the Chief Architect. No SPEC row exists.

**E-2.6.6 — `rfcs/README.md`, RFC Lifecycle diagram, line 29**
> `REVIEW (**Architecture Review Board**)`
> Line 45: "6. **Do not merge your own RFC**"

*Recorded fact:* a merge restriction stated without identifying who may merge.

**E-2.6.7 — `adrs/README.md`, §Process**
> "5. **Merging = accepting**
> ADRs for major decisions require a linked RFC."

*Roles named:* **none** — consistent with E-2.2.7.

**E-2.6.8 — `adrs/ADR-001_REPOSITORY_STRUCTURE.md`** — Status **ACCEPTED**, Date 2026-07-23
> Line 6: `Author: **Documentation Architect**`

*Recorded fact:* a **sixth** distinct role string, appearing in the front matter of the only
ACCEPTED ADR in the repository and defined nowhere. The document records **no approver**.

**E-2.6.9 — `templates/RFC_TEMPLATE.md`, line 105**
> `**Decided by**: Chief Architect`

**E-2.6.10 — `templates/CONFORMANCE_REPORT_TEMPLATE.md`, line 74**
> `Chief Architect: ___________________`  *(signature line)*

**E-2.6.11 — `arc/ARC_TEMPLATE.md`, front matter**
> `Owner: Organization / Role / Name`

*Recorded fact:* the ARC template does **not** name Architecture Board, although E-2.4.2 and
E-2.4.3 assign ARC ownership to it.

**E-2.6.12 — `templates/ADR_TEMPLATE.md`, lines 1–9**
> `Status: DRAFT | ACCEPTED | SUPERSEDED | DEPRECATED`
> `Author: [Author]`

*Recorded fact:* the ADR template has an `Author` field and **no approver, owner, or
`Accepted-by` field** — although E-2.4.6 and E-2.5.3 both specify recording approval in front
matter, under two different field names.

**E-2.6.13 — `CODE_OF_CONDUCT.md`, lines 12 and 24**
> "- Accepting that the **Chief Architect** holds final authority over canonical documents"
> "Final decisions rest with the **Chief Architect** as defined in the AURA Constitution
> Article VIII."

**E-2.6.14 — `constitution/README.md`, line 17; `reference/README.md`, line 24; `ROADMAP.md`, line 5; `SECURITY.md`, line 18**
> "Amendments require: RFC → Architecture Review → Impact Analysis → Dependent Document Updates
> → **Chief Architect** Approval."
> "5. **Chief Architect** approval" *(reference implementation recognition)*
> "It is maintained by the **Chief Architect** and updated after each Architecture Review."
> "Contact: … or email the **Chief Architect** directly."

**E-2.6.15 — `releases/v0.1.0/DOCUMENT_STATUS.md`** *(release snapshot, 2026-07-23)*
> `| Governance | GOV-001 | 1.0-DRAFT | DRAFT |`
> `| Repository Structure ADR | ADR-001 | 1.0 | ACCEPTED |`

*Recorded fact:* the release snapshot recognises **one** ADR-001 — Repository Structure — and
records no approver for it. GOV-001 is confirmed DRAFT.

**E-2.6.16 — `.github/CODEOWNERS`, line 2 — RECORDED, EXPLICITLY NON-AUTHORITATIVE**
> `# Every file in this repository requires review by the Chief Architect.`

*Handling:* recorded as a **prose statement naming a role**, because it is text. The
accompanying `* @AuraIDToken` mappings are **excluded from this inventory** under the exclusion
rules in the preamble. This line is **not** treated as a grant of authority.

---

### 2.7 S3 — `AuraIDToken/aura-poc-a-core-v3.3`

Included because SPEC-002 §2.2 names this repository, APS-950 §11 designates it RI-PY, and it
is the repository in which this package is filed.

**E-2.7.1 — `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md`** — Version `1.0`, Status **CANONICAL**,
Authority **`Constitutional Decree Article V`**, Effective 2026-01-24
> Line 13: "This document defines the role, responsibilities, authority, and succession
> planning for the **Protocol Custodian** (Polish: *Kustosz Protokołu*) of the Aura Protocol."
> Line 68: "As defined in **Constitutional Decree Article V**, the Protocol Custodian has the
> following powers:"
> §2.1.4: "The Custodian has **SOLE AUTHORITY** to: Declare the instrument ready for sealing ·
> Compute final SHA-256 checksum · Archive to M-DISC physical media · Certify bit-identity
> verification · Declare the instrument permanently frozen"
> §2.2.1: "The Custodian has **FINAL AUTHORITY** over: All changes to `core/` directory · All
> changes to constitutional constants · All changes to layer boundaries · All changes to
> cryptographic primitives"
> §7.2: "The Custodian has **ABSOLUTE OVERRIDE AUTHORITY**."

*Authority described:* extensive and explicit — **and every enumerated power is scoped to the
implementation instrument**: constants, `core/`, sealing, M-DISC archival, emergency halt,
succession. *Recorded fact:* the document contains **no** grant of authority over APS
documents, SPEC documents, ADRs, RFCs, or the specification repository. Its declared Authority
is `Constitutional Decree Article V` — a document in **S3**, not the AURA Constitution.

**E-2.7.2 — `CONSTITUTIONAL_DECREE.md`** — Version `1.0`, Status `MANDATORY / NON-OVERRIDABLE`,
Authority `Custodian of the Protocol`
> Article V, "Authority Hierarchy":
> "1. **Custodian of the Protocol (Architect)** — May modify constitutional constants · May
> authorize new tasks · May seal and archive the instrument
> 2. **AI Copilot** (You) …
> 3. **Users/Contributors** …"
> Closing block: "**Custodian of the Protocol:** Kamil Krasiński"

*Recorded fact:* the parenthetical **"(Architect)"** is the closest textual proximity between
the Custodian and Architect vocabularies found anywhere in the three repositories. It appears
in **S3**, in a document that declares its own authority as the Custodian, and it does **not**
state that the Custodian is the AURA Constitution's Chief Architect. See §5 A-2.

**E-2.7.3 — `docs/ops/PROTOCOL_CUSTODIAN.md`** — Version `1.0`, Status `CANONICAL / BINDING`,
Scope `Human Governance of a Frozen Measurement Instrument`
> §2: "The Protocol Custodian is the **sole human authority** allowed to: maintain the physical
> and cryptographic integrity of the instrument · certify that the instrument remains unchanged
> · decide when the instrument must stop operating · initiate lawful succession."

*Recorded fact:* a **third** Custodian-defining document in S3, again scoped to the instrument.
Its title duplicates E-2.7.1's title (`ROLE OF THE PROTOCOL CUSTODIAN`) with different content.

**E-2.7.4 — `.github/copilot-instructions.md`, lines 94–102**
> "- **Protocol Custodian:** Final authority on all canonical definitions, constitutional
> constants, and regulatory interpretations"
> "- For canonical definition conflicts → **Protocol Custodian ONLY**"
> "**Final authority always resides with the Protocol Custodian.**"

*Recorded fact:* "canonical definitions" is broader than E-2.7.1's instrument scope, and this
is agent-instruction text, not a governance document.

**E-2.7.5 — `CLAUDE.md`, line 54 and `AGENTS.md`**
> "- request human/**Protocol Custodian** resolution."
> `AGENTS.md` Authority Precedence: "1. Aura Constitutional Decree / Constitutional Authority
> 2. Aura Protocol Specification 3. Protocol Invariants …"

*Recorded fact:* `AGENTS.md` places "Aura Constitutional Decree" (S3) **above** "Aura Protocol
Specification" (S1). The AURA Constitution Article V places APS-001 directly beneath the AURA
Constitution and does not mention a Decree. Two different top-of-hierarchy documents.

**E-2.7.6 — `RELEASE_CLOSURE_REPORT.md`, line 9**
> `**Authority:** Protocol Custodian`

**E-2.7.7 — `README.md`, line 389**
> `**Architect / Custodian:**`

*Recorded fact:* a solidus construction, as in E-2.6.1 and E-2.6.2. Recorded; not interpreted.

---

### 2.8 S2 — `aura-nomos/aura-specification`

**E-2.8.1** — Contains `README.md` (11 bytes: `# aura-specification`) and `.github/CODEOWNERS`.
**No governance document, no role definition, no authority statement.** The CODEOWNERS mappings
are excluded per the preamble.

---

## 3. Authority Matrix

Conflicts are **flagged, not reconciled**. "Conflict" identifies the §6 entry or §5 entry the
row participates in; `—` means no conflict was detected for that row in isolation.

| Source | Section | Role/Body | Authority | Scope | Conflict |
|---|---|---|---|---|---|
| AURA-CON-001 (FROZEN) | front matter | Chief Architect | Owner | Constitution document | — |
| AURA-CON-001 (FROZEN) | Art. VIII | Chief Architect | "responsible for the project" | Unbounded, unenumerated | A-1 |
| AURA-CON-001 (FROZEN) | Art. VIII | AI systems | MUST NOT approve canonical documents / modify frozen | Prohibition | — |
| AURA-CON-001 (FROZEN) | Art. XI(5) | Chief Architect | Approval | Constitution amendments | — |
| AURA-CON-001 (FROZEN) | Art. XI(2) | *(unnamed)* | "An Architecture Review" | Constitution amendments | A-4, M-2 |
| AURA-CON-001 (FROZEN) | Art. VI | *(none)* | "owner" required per artifact | All artifact classes | M-1 |
| GOV-001 (DRAFT) | §2 tree | Chief Architect | root of hierarchy | Whole repository | A-6 |
| GOV-001 (DRAFT) | §2 tree | Architecture Review Board (ARB) | "conducts ARRs" | Reviews | C-3, M-3 |
| GOV-001 (DRAFT) | §2 tree | Specification Contributors | "author APS, ADRs, RFCs" | Authoring only | M-7 |
| GOV-001 (DRAFT) | §2 tree | AI Assistants | may propose/implement/test; **not** approve or freeze | — | — |
| GOV-001 (DRAFT) | §2 list | Chief Architect | "final and sole approval authority" | **Closed list of 4** — excludes SPEC, ADR, RFC | **C-1**, A-5 |
| GOV-001 (DRAFT) | §3 | Decision author | Owner | ADR | A-7 |
| GOV-001 (DRAFT) | §3 | Proposer | Owner | RFC | A-7 |
| GOV-001 (DRAFT) | §3 | Chief Architect | Owner | ARR, ADC, ACI | — |
| GOV-001 (DRAFT) | §3 | Implementer | Owner | EPR | — |
| GOV-001 (DRAFT) | §5.1 | Chief Architect **or delegate** | may merge | PATCH only | M-6 |
| GOV-001 (DRAFT) | §5.2(4) | Architecture Review Board | "assessment" | Major changes | A-8, M-3 |
| GOV-001 (DRAFT) | §5.2(5) | Chief Architect | approval | Major changes | **C-2** |
| GOV-001 (DRAFT) | §6(6–7) | **NONE NAMED** | "Merging the PR = accepting the ADR" | All ADRs | **C-2**, **M-4** |
| GOV-001 (DRAFT) | §7(7) | Architecture Review Board | votes ACCEPT/REJECT/DEFER | RFC | A-8 |
| GOV-001 (DRAFT) | §7(8) | Chief Architect | final approval | RFC | — |
| GOV-001 (DRAFT) | §8 | Chief Architect | chairs review meetings | ARR production | — |
| SPEC-002 (DRAFT) | front matter | **Protocol Custodian** | Owner | SPEC-002 | **C-1**, A-2 |
| SPEC-002 (DRAFT) | line 11 | *(unnamed)* | APPROVED event required | SPEC-002 normative effect | **M-5** |
| SPEC-002 (DRAFT) | §3.4, §6 | "explicit architectural authority" | approves AD-CA decisions | AD-CA-001…012 | **M-5** |
| ADR-001_DOCUMENT_MODEL (**PROPOSED**) | front matter | **Chief Specification Architect** | Author | — | **M-8** |
| ADR-001_DOCUMENT_MODEL (**PROPOSED**) | front matter | Protocol Custodian | Decision Owner | this ADR | — |
| ADR-001_DOCUMENT_MODEL (**PROPOSED**) | Owners & Authorities | Protocol Custodian | **approves SPECs**, owns SPEC lifecycle, signatory for normative acceptance | SPEC class | **C-1** |
| ADR-001_DOCUMENT_MODEL (**PROPOSED**) | Owners & Authorities | **Architecture Board** | approves/owns ARC baselines **and ADRs** | ARC, ADR | **C-2**, **C-3**, M-3 |
| ADR-001_DOCUMENT_MODEL (**PROPOSED**) | Owners & Authorities | **Release Authority** | owns APS publication | APS class | **C-4**, M-3 |
| ADR-001_DOCUMENT_MODEL (**PROPOSED**) | Owners & Authorities | **Compliance Authority / Auditor** | owns traceability + evidence retention | Compliance | M-3 |
| ADR-001_DOCUMENT_MODEL (**PROPOSED**) | Open Questions | Architecture Board, Protocol Custodian | **thresholds and sign-off procedure UNDEFINED** | — | **M-9** |
| `docs/adr/001-document-model.md` (**DRAFT**) | Merge Blockers | Protocol Custodian **AND** Architecture Board | **both** approvals required | this ADR | **C-7** |
| arc/README.md (no ID/status) | line 10 | Architecture Board **/** Protocol Custodian | accepts ARC baselines | ARC | A-3 |
| templates/SPEC_TEMPLATE.md | line 9 | Protocol Custodian **/** Chief Architect | Owner field options | SPEC class | **C-1**, A-2 |
| templates/SPEC_TEMPLATE.md | line 32 | Protocol Custodian | "must be accepted by" | SPEC class | **C-1** |
| POL-VER-001 (DRAFT) | §3 | Chief Architect | REVIEW→APPROVED; APPROVED→FROZEN | **every** APS doc + governance artifact | **C-1**, **C-5** |
| POL-VER-001 (DRAFT) | §10 | Chief Architect | approval | VERSIONING.md changes | — |
| README.md | §Governance | Chief Architect | "sole approval authority" | "canonical documents" | A-5 |
| CONTRIBUTING.md | table | *(none)* | APS/Invariant rows end at "PR" | APS, INV | **C-6** |
| CONTRIBUTING.md | table | Chief Architect | approval | Constitution amendment | — |
| rfcs/README.md | lifecycle | Architecture Review Board | REVIEW | RFC | A-8 |
| adrs/README.md | §Process | **NONE NAMED** | "Merging = accepting" | ADR | **M-4** |
| ADR-001_REPOSITORY_STRUCTURE (ACCEPTED) | front matter | **Documentation Architect** | Author | — | **M-8** |
| templates/ADR_TEMPLATE.md | front matter | *(none)* | **no approver field exists** | ADR | **M-4**, C-7 |
| templates/RFC_TEMPLATE.md | line 105 | Chief Architect | "Decided by" | RFC | — |
| CODE_OF_CONDUCT.md | §§ | Chief Architect | "final authority over canonical documents" | canonical documents | A-5 |
| `.github/CODEOWNERS` comment | line 2 | Chief Architect | "requires review by" — **NON-AUTHORITATIVE, recorded only** | all files | — |
| S3 ROLE_OF_THE_PROTOCOL_CUSTODIAN (CANONICAL) | §2.1.4 | Protocol Custodian | **SOLE AUTHORITY** to seal/archive | **the instrument** | A-2 |
| S3 ROLE_OF_THE_PROTOCOL_CUSTODIAN (CANONICAL) | §2.2.1 | Protocol Custodian | **FINAL AUTHORITY** | `core/`, constants, layer boundaries, crypto | A-2 |
| S3 ROLE_OF_THE_PROTOCOL_CUSTODIAN (CANONICAL) | §7.2 | Protocol Custodian | **ABSOLUTE OVERRIDE AUTHORITY** | instrument | A-2 |
| S3 CONSTITUTIONAL_DECREE (MANDATORY) | Art. V | **Custodian of the Protocol (Architect)** | modify constants, authorize tasks, seal | instrument | **A-2** |
| S3 docs/ops/PROTOCOL_CUSTODIAN (CANONICAL) | §2 | Protocol Custodian | "sole human authority" | instrument integrity, succession | A-2 |
| S3 .github/copilot-instructions.md | §§94–102 | Protocol Custodian | "Final authority on all **canonical definitions**" | broader than instrument | A-2 |
| S3 AGENTS.md | Authority Precedence | *(none)* | Decree ranked **above** Protocol Specification | cross-repo | **C-8** |
| S2 | — | **NONE** | — | — | — |

---

## 4. Explicit Authority

Authorities granted by source text, without inference. Each entry is a direct grant naming both
a role and an act.

### 4.1 From a FROZEN source

| # | Grant | Source | Scope as written |
|---|---|---|---|
| X-1 | Chief Architect **approves Constitution amendments** | AURA-CON-001 Art. XI(5) | Constitution only |
| X-2 | Chief Architect is **"responsible for the project"** | AURA-CON-001 Art. VIII | Unbounded; no enumeration |
| X-3 | AI systems **MUST NOT approve** canonical documents or modify frozen documents | AURA-CON-001 Art. VIII | Prohibition, all AI |

> **X-1, X-2 and X-3 are the only role grants of FROZEN rank in the entire evidence base.**
> No FROZEN source grants authority over SPEC documents, ADRs, RFCs, ARCs, or APS status
> transitions, and no FROZEN source names any role other than Chief Architect.

### 4.2 From DRAFT sources

| # | Grant | Source | Scope as written |
|---|---|---|---|
| X-4 | Chief Architect has **final and sole approval** over: Constitution amendments; APS status transitions APPROVED→FROZEN; Protocol Invariant additions/removals; new RI recognition | GOV-001 §2 | **Closed four-item list** |
| X-5 | Chief Architect **approves** at step 5 of the Major Change process | GOV-001 §5.2 | RFC-bearing changes |
| X-6 | Chief Architect gives **final approval** of RFCs | GOV-001 §7(8) | RFC class |
| X-7 | ARB **votes ACCEPT / REJECT / DEFER** on RFCs | GOV-001 §7(7) | RFC class |
| X-8 | ARB performs **"assessment"** in Major Changes | GOV-001 §5.2(4) | character unspecified |
| X-9 | Chief Architect **chairs** review meetings | GOV-001 §8 | ARR production |
| X-10 | Chief Architect **or delegate** may merge PATCH changes | GOV-001 §5.1 | PATCH only |
| X-11 | Chief Architect approves `REVIEW → APPROVED` and `APPROVED → FROZEN` | POL-VER-001 §3 | **every** APS doc and governance artifact |
| X-12 | Chief Architect approves changes to the versioning policy | POL-VER-001 §10 | POL-VER-001 |

### 4.3 From a PROPOSED source *(recorded; not in force)*

| # | Grant | Source | Scope as written |
|---|---|---|---|
| X-13 | **Protocol Custodian approves SPECs** and is signatory for normative acceptance | ADR-001_DOCUMENT_MODEL, PROPOSED | SPEC class |
| X-14 | **Architecture Board approves ARC baselines and ADRs** | ADR-001_DOCUMENT_MODEL, PROPOSED | ARC, ADR |
| X-15 | **Release Authority publishes APS** | ADR-001_DOCUMENT_MODEL, PROPOSED | APS class |
| X-16 | **Compliance Authority / Auditor owns traceability + evidence retention** | ADR-001_DOCUMENT_MODEL, PROPOSED | compliance |

> **X-13 is the only text in either repository that grants SPEC approval authority to anyone,
> and its source document has Status: PROPOSED and is self-blocked** (E-2.4.6: it requires the
> approval of the very role it constitutes).

### 4.4 From S3 sources, scoped to the implementation instrument

| # | Grant | Source | Scope as written |
|---|---|---|---|
| X-17 | Protocol Custodian has **SOLE AUTHORITY** to seal and archive the instrument | S3 ROLE_OF_THE_PROTOCOL_CUSTODIAN §2.1.4 | the instrument |
| X-18 | Protocol Custodian has **FINAL AUTHORITY** over `core/`, constants, layer boundaries, crypto primitives | S3 ROLE_OF_THE_PROTOCOL_CUSTODIAN §2.2.1 | the instrument |
| X-19 | Protocol Custodian has **ABSOLUTE OVERRIDE AUTHORITY** | S3 ROLE_OF_THE_PROTOCOL_CUSTODIAN §7.2 | the instrument |
| X-20 | Custodian of the Protocol may modify constitutional constants, authorize tasks, seal and archive | S3 CONSTITUTIONAL_DECREE Art. V | the instrument |

> **None of X-17 … X-20 grants authority over any document in S1.** Every enumerated power
> concerns the measurement instrument: constants, `core/`, sealing, archival, halt, succession.

### 4.5 Authorities that do NOT appear in any explicit grant

Recorded as absences, verified by exhaustive search:

| Act | Explicit grant found? |
|---|---|
| Approve a SPEC-class document | **Only X-13, from a PROPOSED source** |
| Accept an ADR | **NONE.** GOV-001 §6 and `adrs/README.md` attach acceptance to merging without naming an actor. X-14 exists only in a PROPOSED source. |
| Effect `DRAFT → REVIEW` | **NONE.** POL-VER-001 §3 says "Author submits document for review via pull request" — no approver. |
| Resolve an AD-CA decision domain | **NONE.** SPEC-002 refers to "explicit architectural authority" and never binds the term. |
| Constitute or appoint the ARB | **NONE** |
| Constitute Architecture Board / Release Authority / Compliance Authority | **NONE** |
| Appoint or identify a Chief Architect | **NONE in S1** |

---

## 5. Ambiguous Authority

Cases where the source text permits more than one reading. **No reading is selected.**

**A-1 — "Responsible for the project" is unenumerated.**
Constitution Art. VIII (X-2) grants the Chief Architect responsibility for "the project" without
enumeration. GOV-001 §2 (X-4) then states a **closed four-item** list of "final and sole"
authority. *Reading 1:* Art. VIII is a general grant and GOV-001's list is illustrative, so
authority over SPEC follows from Art. VIII. *Reading 2:* GOV-001's "final and sole" is
exhaustive, so items outside the four are not the Chief Architect's. The text supports both.

**A-2 — Whether "Protocol Custodian" and "Chief Architect" denote one office.**
Four possible readings are each supported by some text and contradicted by none decisively:
(i) *same office, two names* — supported by `SPEC_TEMPLATE.md` line 9 presenting them as
interchangeable fill-ins, and by S3's `CONSTITUTIONAL_DECREE` Art. V parenthetical
"(Architect)"; (ii) *distinct offices with distinct scopes* — supported by S3's Custodian
documents being uniformly instrument-scoped while S1's Chief Architect grants are
document-scoped; (iii) *distinct offices with overlapping scope* — supported by
`copilot-instructions.md` extending the Custodian to "all canonical definitions";
(iv) *the same person holding two distinct offices* — supported by no text, excluded by neither.
**No source states any of the four.**

**A-3 — The solidus in "Architecture Board/Protocol Custodian".**
`arc/README.md` line 10 (E-2.6.1) attributes ARC acceptance to "Architecture Board/Protocol
Custodian". *Readings:* either body suffices · both are required · they are the same body · the
notation is undecided shorthand. The same construction appears in `SPEC_TEMPLATE.md` line 9 and
S3 `README.md` line 389. **No source defines the notation.**

**A-4 — "An Architecture Review" as act versus body.**
Constitution Art. XI(2) requires "An Architecture Review". CONTRIBUTING.md, ROADMAP.md and
POL-VER-001 §3 repeat the phrase. GOV-001 §8 describes "Architecture Review meetings" chaired by
the Chief Architect and producing ARRs; GOV-001 §2 says the ARB "conducts ARRs".
*Readings:* the Review is an act the Chief Architect performs · an act the ARB performs · a
meeting requiring both. **Unresolved by the text.**

**A-5 — "Canonical documents" is undefined.**
X-3 (Constitution), README.md §Governance, and CODE_OF_CONDUCT.md all turn on "canonical
documents". APS-000 §5 defines six **statuses** but never defines the **class** "canonical
document". Whether SPEC-002 is one is therefore undetermined — which matters because X-3's
prohibition on AI approval, and README's "sole approval authority", both attach to that class.

**A-6 — GOV-001 §2 places the FROZEN Constitution beneath the Chief Architect.**
In the §2 tree (E-2.2.1) "AURA Constitution (FROZEN — immutable)" is rendered as a **child node
of the Chief Architect**, alongside the ARB and Contributors. *Readings:* the tree depicts
custodial responsibility, not authority over the Constitution · the tree depicts an authority
hierarchy in which a DRAFT document subordinates a FROZEN one. The second reading conflicts with
Constitution Art. V. **Recorded, not resolved.**

**A-7 — "Owner" versus "approver".**
GOV-001 §3 (E-2.2.3) assigns ADR ownership to the "Decision author" and RFC ownership to the
"Proposer". X-6 gives the Chief Architect final RFC approval. *Readings:* ownership and approval
are distinct roles · ownership implies approval. GOV-001 never defines "Owner". This bears
directly on SPEC-002, whose only authority statement is `Owner: Protocol Custodian`.

**A-8 — The ARB's act is named twice, differently.**
GOV-001 §5.2(4) "Architecture Review Board **assessment**"; §7(7) "Architecture Review Board
**votes** ACCEPT / REJECT / DEFER"; §2 "conducts ARRs"; `rfcs/README.md` "REVIEW (Architecture
Review Board)". *Readings:* one act under four names · distinct acts for distinct processes.
Whether the assessment is advisory or binding is stated nowhere.

**A-9 — Whether SPEC-002 is subject to POL-VER-001.**
POL-VER-001 §1 scopes itself to "all artifacts in the `aura-specification` repository,
including APS documents, Protocol Invariants, Conformance Tests, Reference Fixtures, and
releases" — a list that does not name SPEC. §3 then says "Every **APS document and governance
artifact** passes through the following lifecycle". *Readings:* SPEC-002 is a governance
artifact and X-11 applies, making the Chief Architect its approver · SPEC is outside
POL-VER-001's enumerated scope and X-13 (PROPOSED) is the only applicable grant.
**This ambiguity is the direct locus of C-1.**

---

## 6. Contradictions

Direct contradictions between sources. **None is reconciled.**

---

### C-1 — Two different roles are named as SPEC approver, by sources of different rank

**Source A** — `POL-VER-001` §3 (DRAFT), X-11:
> "`REVIEW → APPROVED`: **Chief Architect** approves after Architecture Review"

scoped by §3 to "Every APS document **and governance artifact**".

**Source B** — `ADR-001_DOCUMENT_MODEL` (**PROPOSED**), X-13:
> "**Protocol Custodian**: approves SPECs, is owner of SPEC lifecycle, and is signatory for
> normative acceptance."

**Source C** — `templates/SPEC_TEMPLATE.md` line 32:
> "The SPEC must be accepted by the **Protocol Custodian**."

**Source D** — `templates/SPEC_TEMPLATE.md` line 9, the *same file*:
> `Owner: Role / Name (**Protocol Custodian / Chief Architect**)`

**Source E** — `SPEC-002` front matter: `Owner: Protocol Custodian`.

**Nature.** A DRAFT policy of general scope names one role; a PROPOSED ADR names another; a
template names both, in two lines, inconsistently. **GOV-001 §2's closed list (X-4) names
neither, because it does not contemplate a SPEC class at all.**

**Consequence, recorded as fact:** no APPROVED or in-force document grants **anyone** authority
to approve a SPEC-class document. The only such grant (X-13) sits in a PROPOSED document that is
itself blocked pending the approval of the role it constitutes.

---

### C-2 — ADR acceptance is attributed to an unnamed actor, and separately to a body

**Source A** — GOV-001 §6(6–7) (DRAFT):
> "6. **Merging the PR = accepting the ADR**
> 7. ADR status set to ACCEPTED"

*No actor named.*

**Source B** — `adrs/README.md` §Process: "5. **Merging = accepting**". *No actor named.*

**Source C** — `ADR-001_DOCUMENT_MODEL` (PROPOSED), X-14:
> "**Architecture Board**: approves and owns ARC baselines **and ADRs** related to architecture
> decisions."

**Source D** — GOV-001 §5.2(5): Chief Architect approval precedes step 8, "ADR created if
architectural decision is embedded".

**Nature.** Source A makes acceptance a **mechanical consequence of merging** by an unspecified
party. Source C vests it in a **named body that exists in no in-force document**. Source D
implies Chief Architect approval upstream of ADR creation. Three incompatible accounts.

**Direct bearing on the task:** every ADR resolving an AD-CA domain is accepted under one of
these three regimes, and they do not agree on who acts.

---

### C-3 — "Architecture Review Board" and "Architecture Board" are named as distinct strings and never equated

**Source A** — GOV-001 §2 and §5.2 and §7: "**Architecture Review Board (ARB)**", described as
conducting ARRs, assessing Major Changes, and voting on RFCs.
**Source B** — `ADR-001_DOCUMENT_MODEL` and `arc/README.md`: "**Architecture Board**", described
as approving ARC baselines and ADRs.

**Nature.** Two distinct strings with two distinct described functions. No document states they
are the same body; no document states they are different. Neither is defined, constituted, or
given membership anywhere (see M-3).

---

### C-4 — APS status authority is vested in two different bodies

**Source A** — GOV-001 §2 (X-4): the Chief Architect has "final and sole approval authority over
… **APS document status transitions (APPROVED → FROZEN)**".
**Source B** — `ADR-001_DOCUMENT_MODEL` (X-15): "**Release Authority**: owns APS publication and
release mechanics"; "APS … **Published by Release Authority**".

**Nature.** Source A says "final and **sole**". Source B vests APS publication in a different
body. Under Model B, APS is a release artifact rather than a specification — so the conflict is
partly downstream of DR-003 — but the two texts as written assign the same artifact class to two
different authorities.

---

### C-5 — POL-VER-001 and ADR-001_DOCUMENT_MODEL assign SPEC freeze to different roles

**Source A** — POL-VER-001 §3 (X-11): "`APPROVED → FROZEN`: Explicit freeze decision by **Chief
Architect**; requires Amendment Procedure (Constitution Article XI)", scoped to every APS
document and governance artifact.
**Source B** — `ADR-001_DOCUMENT_MODEL` line 29: "A SPEC becomes frozen **only after explicit
approval by the Protocol Custodian**."

**Nature.** Both address the freeze transition. They name different roles, and Source A
additionally requires Constitution Article XI amendment procedure, which Source B does not
mention.

---

### C-6 — CONTRIBUTING.md omits an approver that GOV-001 reserves

**Source A** — GOV-001 §2 (X-4): "Chief Architect has final and sole approval authority over …
**Protocol Invariant additions or removals**".
**Source B** — `CONTRIBUTING.md` table: "| New Protocol Invariant | RFC → Architecture Review →
**PR** |" — the process terminates at "PR" with no approver named, while the adjacent
Constitution row explicitly ends "→ Chief Architect approval".

**Nature.** The contrast within a single table is deliberate in form and inconsistent with
GOV-001 in substance. A contributor following CONTRIBUTING.md would not seek the approval
GOV-001 requires.

---

### C-7 — Two documents bearing identifier `ADR-001` specify different approval requirements

**Source A** — `adrs/ADR-001_DOCUMENT_MODEL.md`, Status **PROPOSED**:
> "requires explicit approval by the **Protocol Custodian**. Approval is recorded by adding an
> **`Accepted-by: <Protocol Custodian>`** line and merging"

**Source B** — `docs/adr/001-document-model.md`, Status **DRAFT**, Merge Blockers:
> "- [ ] **Protocol Custodian approval (required)**
> - [ ] **Architecture Board approval (required)**"
> "…until Protocol Custodian adds an **`accepted_by`** entry and the PR is merged"

**Source C** — `adrs/ADR-001_REPOSITORY_STRUCTURE.md`, Status **ACCEPTED** — a third document
with the same identifier, recording **no approver at all**.

**Source D** — `templates/ADR_TEMPLATE.md` — the canonical ADR template contains **no approver,
owner, or acceptance field** in its front matter, so neither `Accepted-by:` nor `accepted_by` is
a template-sanctioned field.

**Nature.** One approver versus two; `Accepted-by:` versus `accepted_by`; and a template
supporting neither. All three documents claim identifier `ADR-001`, which APS-000 §4 and
POL-VER-001 §8 both forbid.

---

### C-8 — Two different documents are named as top of the authority hierarchy

**Source A** — AURA Constitution Art. V (FROZEN): hierarchy begins
`AURA Constitution → APS-001 → APS-100 → ADR/ARR/RFC → …`. No "Decree" appears.
**Source B** — S3 `AGENTS.md` and `CLAUDE.md` Authority Precedence: "1. **Aura Constitutional
Decree** / Constitutional Authority 2. Aura Protocol Specification 3. Protocol Invariants …"

**Nature.** Source B ranks a document that exists only in S3 (`CONSTITUTIONAL_DECREE.md`) above
the Aura Protocol Specification. Source A does not contemplate that document. Because the
Decree is the source from which S3's Protocol Custodian derives all authority (E-2.7.1: "As
defined in Constitutional Decree Article V"), the two hierarchies produce different answers to
"which document constitutes the deciding role".

---

## 7. Missing Governance Definitions

Concepts referenced by governance text but never formally defined. Verified absent by exhaustive
search of S1, S2 and S3.

| # | Undefined concept | Referenced at | What is missing |
|---|---|---|---|
| **M-1** | **Artifact "owner"** | Constitution Art. VI: "Every artifact has an identifier, version, owner, and status"; GOV-001 §3 | No definition of what ownership confers. Bears on A-7 and on SPEC-002's sole authority statement. |
| **M-2** | **"Architecture Review"** | Constitution Art. XI(2); CONTRIBUTING.md; ROADMAP.md; POL-VER-001 §3; GOV-001 §5.2, §8 | No definition of what constitutes one, who convenes it, quorum, or output validity. |
| **M-3** | **ARB / Architecture Board / Release Authority / Compliance Authority** | GOV-001 §2, §5.2, §7; ADR-001_DOCUMENT_MODEL; arc/README.md; rfcs/README.md | **None of the four is defined, constituted, given membership, appointment method, quorum, or term.** No document states that any currently exists. |
| **M-4** | **Who may merge** | GOV-001 §6 "Merging the PR = accepting"; adrs/README.md; rfcs/README.md "Do not merge your own RFC" | Acceptance is bound to merging; the merging actor is named only for PATCH changes (X-10). `templates/ADR_TEMPLATE.md` has no approver field. |
| **M-5** | **"Explicit architectural authority"** | SPEC-002 §3 constraint 4, §6 | The term SPEC-002 uses for its own approver is never bound to a role. |
| **M-6** | **"Delegate"** | GOV-001 §5.1 "Chief Architect **or delegate** may merge" | No definition of who may be a delegate, how delegation is conferred, recorded, or revoked, or its scope. |
| **M-7** | **"Specification Contributors"** | GOV-001 §2 | No definition of qualification, admission, or standing. |
| **M-8** | **"Documentation Architect"**, **"Chief Specification Architect"** | ADR-001_REPOSITORY_STRUCTURE front matter; ADR-001_DOCUMENT_MODEL front matter | Two further architect-titled strings, each appearing exactly once, defined nowhere, related to "Chief Architect" nowhere. |
| **M-9** | **Approval thresholds, quorum, signature format** | ADR-001_DOCUMENT_MODEL Open Questions | Explicitly listed by that document as unresolved: "Exact approval thresholds and sign-off procedure … (quorum, signature format)". |
| **M-10** | **Appointment / identification of the Chief Architect** | Constitution Art. VIII; GOV-001 §2 | No S1 document states how the office is filled, recorded, or succeeded. *(By contrast S3 defines Custodian succession in ROLE_OF_THE_PROTOCOL_CUSTODIAN §5 — for the instrument role only.)* |
| **M-11** | **"Canonical document"** | Constitution Art. VIII; README.md; CODE_OF_CONDUCT.md; copilot-instructions.md | APS-000 §5 defines statuses, not this class. Whether SPEC-002 belongs to it is undetermined (A-5). |
| **M-12** | **Cross-repository authority** | SPEC-002 §2.2 constrains S3; APS-950 §11 designates RI-PY/RI-RS; S3 governs itself by Decree | No document states whether an S1 role has authority in S3, or an S3 role in S1. |
| **M-13** | **`DRAFT → REVIEW` approver** | POL-VER-001 §3: "Author submits document for review via pull request" | The first transition of the lifecycle names no approver. |
| **M-14** | **Whether a role is a person or a body** | throughout | "Chief Architect" and "Protocol Custodian" are used in the singular; "Board" implies plurality; no document classifies any of the six. |

---

## 8. Dependency Impact

Which AD-CA decisions cannot be **legitimately assigned** until DR-002 is resolved.

### 8.1 The dependency, stated precisely

An AD-CA domain is resolved by an approved architectural decision (SPEC-002 §9 criterion 1;
§3 constraint 4). Approval requires an approver with authority over the artifact class carrying
the decision. Per §4.5 and C-1/C-2, **no in-force document identifies an approver for either the
SPEC class or ADR acceptance.** Therefore no AD-CA domain can be closed by an approval whose
validity is demonstrable from the current text.

The dependency is **uniform**. It does not vary by domain, because it operates on the approval
step common to all of them.

### 8.2 Impact table

| AD-CA | Carrier artifact | Blocked by | Legitimately assignable today? |
|---|---|---|---|
| AD-CA-001 | ADR-002 → SPEC-002 | C-1, C-2, M-4, M-5 | **No** |
| AD-CA-002 | ADR-002 → SPEC-002 | C-1, C-2, M-4, M-5 | **No** |
| AD-CA-003 | ADR-003 → SPEC-002 | C-1, C-2, M-4, M-5 | **No** |
| AD-CA-004 | **unassigned** | above, **plus no artifact exists to carry it** | **No** |
| AD-CA-005 | ADR-003 → SPEC-002 | above, plus scope dispute (DR-008) | **No** |
| AD-CA-006 | **unassigned** | above, **plus no artifact exists to carry it** | **No** |
| AD-CA-007 | ADR-004 → SPEC-002 | C-1, C-2, M-4, M-5 | **No** |
| AD-CA-008 | ADR-004 → SPEC-002 | C-1, C-2, M-4, M-5 | **No** |
| AD-CA-009 | ADR-005 → SPEC-002 + APS-200 amendment | above, **plus C-4** (APS authority contested) | **No** |
| AD-CA-010 | ADR-005 → SPEC-002 + APS-200 amendment | above, **plus C-4** | **No** |
| AD-CA-011 | ADR-006 → SPEC-002 | above, **plus C-5** (freeze authority contested) | **No** |
| AD-CA-012 | ADR-006 → SPEC-002 | above, **plus C-5** | **No** |

**Result: 0 of 12 legitimately assignable.**

### 8.3 Secondary dependencies

| Dependent item | Why DR-002 gates it |
|---|---|
| **DR-005** (ADR acceptance bar: GOV-001 §5.2 vs §6) | Choosing between the paths presupposes knowing who acts in each. §5.2 requires an **ARB assessment**; per M-3 the ARB is not constituted, so that path may not be executable. |
| **DR-003** (document authority model) | Model B is constituted by `ADR-001_DOCUMENT_MODEL`, which requires Protocol Custodian approval (E-2.4.6) — a role that document itself constitutes. **Circular:** adopting Model B requires an authority that only Model B grants. |
| **DR-004** (ADR-001 collision) | Resolution requires deciding which document keeps the identifier — an approval act with no identified approver (M-4). |
| **DR-023** (freeze authority) | Directly downstream of C-5. |
| **DR-025** (independent implementation) | Commissioning is a resourcing decision; no document assigns resourcing authority to any role. |
| **`ARCHITECTURE-RESOLUTION-001.md` §5 authority column** | Cannot be completed. |

### 8.4 A recorded circularity

`ADR-001_DOCUMENT_MODEL` is the sole source of X-13 (Protocol Custodian approves SPECs) and
X-14 (Architecture Board approves ADRs). It is **PROPOSED**, and E-2.4.6 states it "requires
explicit approval by the Protocol Custodian".

Under GOV-001 §6 an ADR is accepted by merging (M-4: actor unnamed). Under its own terms it
requires an `Accepted-by: <Protocol Custodian>` line. **The role empowered to accept it is
constituted by the document awaiting acceptance.** Whether this is breakable from within the
current text is **not determined here**; it is recorded because it bears directly on §9.

---

## 9. Required Governance Decision

The minimum question that must be answered by the authorized Protocol governance process.

> **Which role or body holds authority to approve (a) a SPEC-class document and (b) an ADR that
> resolves an AD-CA architectural decision domain — and by what recorded act is that approval
> exercised?**

Answering it necessarily entails answering the following, because each is a component of the
question rather than an addition to it:

| # | Component | Evidence that it is entailed |
|---|---|---|
| 9.1 | Whether "Chief Architect" and "Protocol Custodian" are the same office, distinct offices, or offices of distinct scope | A-2; C-1 |
| 9.2 | Whether the Chief Architect's authority under GOV-001 §2 is the closed four-item list or a general grant under Constitution Art. VIII | A-1; X-2 vs X-4 |
| 9.3 | Whether SPEC-002 is a "governance artifact" under POL-VER-001 §3, and whether it is a "canonical document" under Constitution Art. VIII | A-5; A-9; M-11 |
| 9.4 | Whether ADR acceptance-by-merge (GOV-001 §6) names an actor, and who may merge | C-2; M-4 |
| 9.5 | Whether the ARB and the Architecture Board exist, are the same body, and are constituted | C-3; M-3 |
| 9.6 | Whether Release Authority and Compliance Authority exist as constituted bodies | C-4; M-3 |
| 9.7 | How the circularity in §8.4 is to be broken | §8.4 |
| 9.8 | Whether an S1 role holds authority in S3 and vice versa | M-12; C-8 |

**This document does not answer the question or any of its components.**

### 9.1 Procedural note, recorded without recommendation

The evidence does not establish which process may legitimately produce the answer. Constitution
Art. XI supplies an amendment procedure ending in "Approval by the Chief Architect" (X-1), and
that procedure is the only approval path of FROZEN rank in the evidence base. Whether DR-002 is
a Constitution-amendment matter, a GOV-001 amendment matter under GOV-001 §11, or a matter
resolvable by a lower instrument, **is itself undetermined by the text and is part of the
decision.**

---

## 10. Stop Condition

### 10.1 Resolution test

The stop condition permits a status other than UNRESOLVED only if the repository contains
explicit evidence that **completely** resolves the authority model. Applying that test:

| Test | Result | Basis |
|---|---|---|
| Does any in-force document name an approver for SPEC-class documents? | **No** | §4.5; C-1. The only such grant (X-13) is PROPOSED and self-blocked. |
| Does any document name an actor for ADR acceptance? | **No** | C-2; M-4 |
| Do any two role vocabularies get equated by source text? | **No** | A-2; §2.6.2 shows the only co-occurrence, which offers them as alternatives |
| Are ARB / Architecture Board / Release Authority / Compliance Authority defined or constituted? | **No** | M-3 |
| Is the term SPEC-002 uses for its own approver bound to a role? | **No** | M-5 |
| Is there a non-circular path to constituting the SPEC-approval authority? | **Not established** | §8.4 |

Six of six negative. The repository does not contain evidence that completely resolves the
authority model.

### 10.2 Summary of the evidence base

| Measure | Count |
|---|---|
| Distinct role/body strings found | **9** — Chief Architect · Protocol Custodian · Custodian of the Protocol · Architecture Review Board (ARB) · Architecture Board · Release Authority · Compliance Authority / Auditor · Documentation Architect · Chief Specification Architect |
| Role grants of FROZEN rank | **3** (X-1, X-2, X-3) — all naming Chief Architect or "AI systems" |
| Role grants from DRAFT sources | 9 (X-4 … X-12) |
| Role grants from PROPOSED sources | 4 (X-13 … X-16) |
| Role grants scoped to the S3 instrument | 4 (X-17 … X-20) |
| Explicit grants of SPEC-approval authority in force | **0** |
| Explicit grants of ADR-acceptance authority in force | **0** |
| Bodies referenced but never constituted | **4** |
| Direct contradictions | **8** (C-1 … C-8) |
| Ambiguities | **9** (A-1 … A-9) |
| Missing definitions | **14** (M-1 … M-14) |
| AD-CA domains legitimately assignable | **0 of 12** |

### 10.3 Status

**DR-002 STATUS: UNRESOLVED**

---

## Appendix A — Roles not recommended

For the avoidance of doubt, this document does **not** recommend, endorse, prefer, or imply as
correct any of: Chief Architect · Protocol Custodian · Custodian of the Protocol · Architecture
Review Board · Architecture Board · Release Authority · Compliance Authority / Auditor ·
Documentation Architect · Chief Specification Architect · or any other role or body.

Where a role appears more frequently than another in this inventory, that frequency is a
property of the corpus and is **not** evidence of authority. Frequency was not used, and must
not be read, as a tiebreaker.

## Appendix B — Sources inspected and found to contain no role or authority statement

`S1`: `aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` · `aps/APS-100_PROTOCOL_INVARIANTS.md` ·
`aps/APS-200_CANONICAL_DATA_MODEL.md` · `aps/APS-300_EVIDENCE_MODEL.md` ·
`aps/APS-400_CONFORMANCE_TEST_MATRIX.md` · `aps/APS-500_REFERENCE_FIXTURES.md` ·
`specification/APS-001_PROTOCOL_SPECIFICATION.md` (Status TODO) ·
`invariants/INVARIANT_REGISTRY.md` · `compliance/TRACEABILITY_MATRIX.md` ·
`conformance/CONF-001` … `CONF-010` · `glossary/GLOSSARY.md` · `fixtures/` ·
`STYLE_GUIDE.md` · `CHANGELOG.md`.

*Note:* `APS-900_COMPLIANCE_MAPPING.md` §10 and `APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md`
§12 are both titled "Governance" and both describe **process requirements only** — "MUST pass
Architecture Review", "MUST be documented in ADRs" — **without naming any role or body.** They
are recorded here rather than in §2 for that reason.

`S2`: entire repository (two files, no governance content).

---

**END OF DR-002_EVIDENCE_PACKAGE**

*Evidence acquisition only. No decision made. No role recommended. No governance created or
modified. No ADR created. No source code modified.*

**DR-002 STATUS: UNRESOLVED**
