# 07 — FORMAL ARTIFACT ANALYSIS (OQ-A-006)

**Question:** *What artifact formally records such a decision?*
**Required result:** ADR / SPEC / amendment / other / UNRESOLVED
**Normative effect:** NONE

> **No artifact is selected in this document.** Each candidate is characterised from its own
> governing text.

---

## 1. Candidate artifact classes located

| # | Class | Defined by | Exists in corpus? |
|---|---|---|---|
| A-1 | **ADR** — Architecture Decision Record | GOV-001 §3, §6; `adrs/README.md`; CONTRIBUTING; `templates/ADR_TEMPLATE.md`; AURA-CON-001 Art. VI | Yes — 1 ACCEPTED, 1 PROPOSED, 1 duplicate-ID draft |
| A-2 | **RFC** — Request for Comments | GOV-001 §7; `rfcs/README.md`; CONTRIBUTING; `templates/RFC_TEMPLATE.md` | Class defined; **zero instances** |
| A-3 | **APS section** — content in a numbered APS document | AURA-CON-001 Art. V; APS-000; POL-VER-001 | Yes (all DRAFT; APS-001 TODO) |
| A-4 | **Constitution amendment** | AURA-CON-001 Art. XI; GOV-001 §5.3 | Procedure defined; **zero instances** |
| A-5 | **SPEC document** | ADR-001_DOCUMENT_MODEL (PROPOSED); `templates/SPEC_TEMPLATE.md` | One instance (SPEC-002, v0.3-DRAFT); **class not established by any in-force source** |
| A-6 | **ARR** — Architecture Review Record | GOV-001 §3, §8; AURA-CON-001 Art. VI | Class defined; **zero instances** |
| A-7 | **Constitutional Decree amendment / new Decree** | Decree itself; ROLE §4.2 | One Decree; no amendment procedure for it in the Decree itself |
| A-8 | **New instrument declaration** | Decree Art. VIII; ROLE §4.2 Step 3; README §8, §11.4 | Procedure defined; **never exercised** (no v4.x, no sealed v3.3) |
| A-9 | **ARC** — Architecture Baseline | ADR-001_DOCUMENT_MODEL (PROPOSED); `arc/ARC_TEMPLATE.md` | Template exists; **zero instances**; class not in force |
| A-10 | **ADC / ACI / EPR** | GOV-001 §3 table | Named once, never defined further; **zero instances** |

---

## 2. Per-class characterisation

Six properties per the required investigation.

### A-1 — ADR

| Property | Finding | Evidence |
|---|---|---|
| **Purpose** | "documents a single architectural decision"; "captures *why* a decision was made, not just what was decided"; ADRs are "permanent records … never deleted" | GOV-001 §3, §6; `adrs/README.md:7-9` |
| **Authority** | Owner is the "Decision author" (an **ownership** field, not an approval grant). ADR-001_DOCUMENT_MODEL would assign approval to the Architecture Board — **PROPOSED, not in force** | GOV-001 §3; S-09 `:55` |
| **Approval mechanism** | "6. **Merging the PR = accepting the ADR** 7. ADR status set to ACCEPTED" — **no approver named** | GOV-001 §6 |
| **Lifecycle** | PROPOSED → ACCEPTED (by merge) → SUPERSEDED (marked, with reference to replacement) | `adrs/README.md:9`; ADR-001_DOCUMENT_MODEL header `Status: PROPOSED` |
| **Can it establish semantic requirements?** | **Contested.** CONTRIBUTING `:70`: "ADRs document *decisions already made* — **not proposals** (use RFC for proposals)." On that text an ADR *records* a decision made elsewhere; it does not constitute it. GOV-001 §5.2 step 8 places ADR creation *after* RFC acceptance, consistent with that reading | CONTRIBUTING `:70`; GOV-001 §5.2 |
| **Can it amend an existing specification?** | No source says it can. GOV-001 §5.2 has the RFC drive the change and the ADR record the embedded architectural decision | GOV-001 §5.2 |
| **Can it create a new normative rule?** | **Not established.** No text grants an ADR normative force over implementations; AURA-CON-001 Art. V places ADR/ARR/RFC *below* APS-100 | AURA-CON-001 Art. V |
| **Complication** | Two ADR namespaces exist (specification corpus `adrs/`; implementation corpus `docs/ADR_005_NO_FLOAT_RUNTIME.md`). The implementation-corpus ADR-005 carries `Status: APPROVED` / `FROZEN` with no approver recorded and no registry entry in either corpus | direct inspection |

### A-2 — RFC

| Property | Finding | Evidence |
|---|---|---|
| **Purpose** | "a formal proposal for a protocol change … the **mandatory** process for any change that affects: Protocol behavior, Protocol Invariants, Conformance Tests, Evidence structure, Constitutional principles" | `rfcs/README.md:7-12` |
| **Authority** | Proposer owns it; ARB votes; "Chief Architect final approval" | GOV-001 §3, §7 steps 7–8 |
| **Approval mechanism** | 9 steps: copy template → number → PR (starts ≥14-day comment period) → ARB vote → Chief Architect approval → ACCEPTED or REJECTED (both permanently recorded) | GOV-001 §7; `rfcs/README.md:22-36` |
| **Lifecycle** | DRAFT (open PR) → COMMENT PERIOD → REVIEW (ARB) → ACCEPTED/REJECTED → implementation PR referencing the RFC | `rfcs/README.md:24-33` |
| **Can it establish semantic requirements?** | It is the **only** class the corpus calls mandatory for changes affecting protocol behaviour. Whether the RFC itself carries the requirement, or the APS text merged afterwards does, is not stated | `rfcs/README.md:7`; GOV-001 §5.2 step 7 |
| **Can it amend an existing specification?** | Yes, as the driving process: "Implementation via pull request referencing RFC" | GOV-001 §5.2 step 7 |
| **Can it create a new normative rule?** | Consistent with the corpus, via the APS change it drives. Under AURA-CON-001 Art. V an RFC sits below APS-100 | GOV-001 §5.2; Art. V |
| **Operational status** | **Never exercised.** `rfcs/README.md:16` — "*No RFCs submitted yet.*" The ARB required at step 4/7 has no roster, charter, or ARR | direct inspection |

### A-3 — APS section

| Property | Finding | Evidence |
|---|---|---|
| **Purpose** | Normative specification content; "All implementations MUST be semantically equivalent to this model" (APS-200 §1 pattern) | APS documents |
| **Authority** | Status transitions approved by the Chief Architect | GOV-001 §2; POL-VER-001 §3 |
| **Approval mechanism** | Content arrives by RFC → Architecture Review → PR; status advances DRAFT → REVIEW → APPROVED → FROZEN | CONTRIBUTING `:23`; POL-VER-001 §3 |
| **Lifecycle** | Four statuses plus DEPRECATED/ARCHIVED; "A FROZEN document never receives a new version number" | POL-VER-001 §3–§4 |
| **Can it establish semantic requirements?** | **Yes — this is the class designed for it.** APS-001 is the root behavioural specification | AURA-CON-001 Art. V; APS-001 Purpose |
| **Can it amend an existing specification?** | Yes, within the lifecycle rules; a FROZEN document is revised by creating a new document | POL-VER-001 §4 |
| **Can it create a new normative rule?** | Yes | Art. V |
| **Operational status** | **APS-001 does not exist** (`Status: TODO`). Every other APS is 1.0-DRAFT. No APS has ever transitioned beyond DRAFT | `DOCUMENT_STATUS.md`; ROADMAP |

### A-4 — Constitution amendment

| Property | Finding | Evidence |
|---|---|---|
| **Purpose** | Change the FROZEN Constitution | AURA-CON-001 Art. XI |
| **Authority** | Chief Architect approval, step 5 | Art. XI; GOV-001 §5.3 |
| **Approval mechanism** | RFC → Architecture Review (ARR) → impact analysis → dependent-document updates → Chief Architect approval → "New FROZEN version published" | Art. XI; GOV-001 §5.3 |
| **Lifecycle** | Produces a **new version**; "Once a version is marked FROZEN, its content is immutable" | Art. XI |
| **Can it establish semantic requirements?** | The Constitution states principles, not protocol mechanics; ARI semantics would be an unusual fit | AURA-CON-001 Art. IV |
| **Can it amend an existing specification?** | It amends itself; dependent documents are updated as step 4 | Art. XI |
| **Operational status** | Never exercised | — |

### A-5 — SPEC document (e.g. SPEC-002)

| Property | Finding | Evidence |
|---|---|---|
| **Purpose** | "normative specification units that express requirements (MUST/SHOULD/MAY) derived from one or more ARCs" | ADR-001_DOCUMENT_MODEL `:27-32` |
| **Authority** | "Protocol Custodian (owner/approver for normative acceptance)" — **in a PROPOSED ADR** | ibid. `:30`, `:54` |
| **Approval mechanism** | "A SPEC becomes frozen only after explicit approval by the Protocol Custodian" — **not in force** | ibid. `:29` |
| **Lifecycle** | DRAFT → REVIEW → APPROVED → FROZEN — **per the PROPOSED model only** | ibid. |
| **Can it establish semantic requirements?** | It is designed to. **But** SPEC-002 itself states "Normative effect: NONE until APPROVED", and no in-force source defines how a SPEC becomes approved | SPEC-002 `:11`; §2 above |
| **Can it amend an existing specification?** | Not stated by any in-force source | — |
| **Critical finding** | **The SPEC class has no in-force governing document.** GOV-001 §2's approval list does not include SPEC; POL-VER-001 §1 governs "APS documents, Protocol Invariants, Conformance Tests, Reference Fixtures, and releases"; AURA-CON-001 Art. V does not name SPEC. The only text that would govern SPEC is PROPOSED | `04_DECREE_VS_SPEC_ANALYSIS.md` §9; `03_…MATRIX.md` §2 |

### A-6 — ARR

| Property | Finding |
|---|---|
| Purpose | "records a formal review session"; owner Chief Architect (GOV-001 §3) |
| Mechanism | "ARR published to `/adrs/ARR-NNN_TITLE.md` within 5 days of meeting" (GOV-001 §8) |
| Can it establish semantics? | Not stated — it records a review, not a decision |
| Operational status | **Zero instances**; the review body that would produce it has no established existence |

### A-7 / A-8 — Decree amendment and new-instrument declaration (implementation corpus)

| Property | Finding | Evidence |
|---|---|---|
| **Purpose (A-7)** | The Decree provides no amendment procedure for itself. ROLE §9.1 provides one for **ROLE**, by the Custodian | Decree (full read); ROLE §9.1 |
| **Purpose (A-8)** | Record that a change creates a **new instrument**: "Any change to core logic creates a NEW INSTRUMENT, not a new version" | Decree Art. VIII; README §8, §11.4 |
| **Authority** | Protocol Custodian | ROLE §4.2 |
| **Approval mechanism (A-8)** | ROLE §4.2 five steps: mathematical justification → regulatory impact assessment → version declaration → documentation (**"Create ADR documenting the change"**) → audit trail (SHA-256, M-DISC archive) | ROLE §4.2 |
| **Can it establish semantic requirements?** | For **the instrument**, yes — it is how a constant changes. For the **protocol**, unestablished (`OQ-B`) | ROLE §2.1.1 |
| **Operational status** | Never exercised: no tag, no checksum, `docs/LEGACY_PROTOCOL.md` still carries `[COMPUTED_AT_SEALING_v3.3]` | direct inspection |

---

## 3. Cross-cutting observations

1. **Two ADR namespaces, one already collided.** Three files carry `ADR-001`
   (`adrs/ADR-001_DOCUMENT_MODEL.md` PROPOSED, `adrs/ADR-001_REPOSITORY_STRUCTURE.md` ACCEPTED,
   `docs/adr/001-document-model.md`), against APS-000 §4 ("Identifiers MUST NOT be reused") and
   against ADR-001_DOCUMENT_MODEL's own INV-DOC-005. A new ADR would need a namespace decision
   before it could be numbered.
2. **"Merging = accepting" makes merge permission the de facto ADR gate**, which is a platform
   capability rather than a documented grant (`03_AUTHORITY_AND_APPROVAL_MATRIX.md` §3).
3. **The two artifact classes that could carry an ARI semantic — APS section and SPEC — are both
   blocked**: APS-001 does not exist, and SPEC has no in-force lifecycle authority.
4. **Every class that has an approval actor has never been exercised**; every class that has been
   exercised (ADR by merge) has no named approval actor.

---

## 4. OQ-A-006 — finding

# UNRESOLVED

**What the evidence does establish:**

| If the decision is … | The corpus's explicit route is … | Blocking condition |
|---|---|---|
| a change affecting **protocol behaviour** | **RFC** — called "mandatory" for exactly that trigger (`rfcs/README.md:7`) — followed by the APS change it drives, with an ADR "if an architectural decision is embedded" (GOV-001 §5.2 step 8) | ARB existence; APS-001 does not exist; never exercised |
| a change to an **instrument constant** | ROLE §4.2: justification → impact assessment → **new instrument** declaration → documentation incl. an ADR → audit trail | scope limited to the instrument (`OQ-B`); never exercised |
| a change to the **Constitution** | AURA-CON-001 Art. XI | never exercised |

**Why the overall answer is UNRESOLVED and not "RFC" or "ADR":**

1. Which route applies depends on whether ARI is protocol content or instrument content —
   `ARI-D-001`, **open** (`06_ARI_DECISION_AUTHORITY.md` C-1).
2. The artifact class that would most directly carry ARI numerics (SPEC) has **no in-force
   governing authority at all**.
3. The corpus contains **two artifact-model regimes** — the in-force GOV-001/AURA-CON-001 model
   and the PROPOSED ARC → SPEC → APS model — which assign ownership and approval differently.
   Recorded as `OQ-A-CONFLICT-005`.
4. An ADR, on CONTRIBUTING's own text, **records** a decision rather than constituting one — so
   naming "ADR" as the answer would misstate what the corpus says the artifact does.

**No artifact class is selected or recommended.**

---

*This document has no normative effect. It characterises candidate artifact classes from their
governing texts. It selects no artifact, recommends none, and creates none.*
