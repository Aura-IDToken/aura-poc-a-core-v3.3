# 03 — AUTHORITY AND APPROVAL MATRIX (OQ-A-002)

**Question:** *Who possesses approval authority?*
**Required result:** authority evidence
**Normative effect:** NONE

---

## 0. Distinctions applied

Eleven concepts are kept separate. Where a source conflates two, the conflation is recorded.

| Concept | Meaning used here |
|---|---|
| **Authority** | The power to decide a matter |
| **Ownership** | Being recorded as the owner of an artifact |
| **Approval authority** | The power to move an artifact into an approved/accepted status |
| **Normative source** | A document whose text creates obligations |
| **Procedural authority** | The power to define or run a process |
| **Implementation guidance** | Direction to implementers, without authority over the protocol |
| **Repository policy** | Rules for contributing to a repository |
| **Contributor responsibility** | Duties of a person submitting a change |
| **Custodianship** | Guardianship of an artifact's integrity |
| **Review responsibility** | The duty to inspect before merge |
| **Merge authority** | The power to merge a pull request |

**Not assumed anywhere:** `OWNER = APPROVER` · `AUTHOR = AUTHORITY` · `CODEOWNER = AUTHORITY` ·
`REVIEWER = APPROVER` · `COMMIT HISTORY = GOVERNANCE AUTHORITY`.

---

## 1. Authority matrix

Columns are as specified. **No "effective authority" column is present**, because no source
establishes effective authority; where authority cannot be established the row reads
**AUTHORITY UNRESOLVED**.

| Source | Claimed Role | Claimed Scope | Claimed Authority | Actual Subject | Status | Conflicts | Evidence |
|---|---|---|---|---|---|---|---|
| AURA-CON-001 Art. VIII | **Chief Architect** | "the project" | "The Chief Architect is responsible for the project." | Responsibility statement — **no approval verb** | FROZEN v1.0 | — | `constitution/AURA_CONSTITUTION.md` Art. VIII |
| AURA-CON-001 Art. VIII | **AI systems** | all AI systems | "AI systems MUST NOT approve changes to canonical documents or modify frozen documents." | Prohibition on AI approval | FROZEN v1.0 | — | ibid. |
| AURA-CON-001 Art. XI | **Chief Architect** | Constitution amendments | Step 5: "Approval by the Chief Architect" | Approval authority, scoped to the Constitution | FROZEN v1.0 | — | ibid. Art. XI |
| GOV-001 §2 | **Chief Architect** | `aura-specification` repository (§1) | "final and **sole** approval authority over: AURA Constitution amendments; APS document status transitions (APPROVED → FROZEN); Protocol Invariant additions or removals; New reference implementation recognition" | Approval authority over **four enumerated artifact classes** | **DRAFT** (GOV-001 is 1.0-DRAFT) | The list is closed and does **not** include ADRs, SPEC documents, or protocol-semantic decisions | `GOVERNANCE.md:32-36` |
| GOV-001 §2 | **Architecture Review Board (ARB)** | specification repository | "conducts ARRs"; §5.2 step 4 "Architecture Review Board assessment"; §7 step 7 "ARB votes: ACCEPT / REJECT / DEFER" | Assessment and voting role | DRAFT | **No roster, charter, membership record or ARR exists** | `GOVERNANCE.md:22-23, 82, 126` |
| GOV-001 §2 | **Specification Contributors** | specification repository | "author APS, ADRs, RFCs" | Authorship — **not** authority | DRAFT | — | `GOVERNANCE.md:25-26` |
| GOV-001 §2, §9 | **AI Assistants** | specification repository | "may propose, implement, test; **may NOT approve or freeze**" | Prohibition | DRAFT | — | `GOVERNANCE.md:28-29, 147-157` |
| GOV-001 §3 | **Decision author** | ADR | "Owner" of an ADR | **Ownership only.** The table's column is "Owner"; no approval verb attaches | DRAFT | Conflicts with S-09's assignment of ADR approval to the Architecture Board | `GOVERNANCE.md:44` |
| GOV-001 §6 | *(unnamed)* | ADR | "6. **Merging the PR = accepting the ADR** 7. ADR status set to ACCEPTED" | Approval mechanism with **no named approver** | DRAFT | Merge authority is unassigned; §5.1 assigns merge for PATCH to "Chief Architect or delegate", §5.2/§6 assign it to nobody | `GOVERNANCE.md:109-110` |
| POL-VER-001 §3 | **Chief Architect** | document status transitions | "REVIEW → APPROVED: Chief Architect approves after Architecture Review"; "APPROVED → FROZEN: Explicit freeze decision by Chief Architect" | Approval authority over lifecycle transitions | **DRAFT** | — | `VERSIONING.md:48-49` |
| `aura-specification/README.md` | **Chief Architect** | canonical documents | "holds **sole approval authority** over canonical documents" | Broader than GOV-001's four-item list | No document ID, no status | **Scope conflict with GOV-001 §2** (which enumerates four classes, not "canonical documents" generally) | `README.md:154` |
| `.github/CODEOWNERS` | `@AuraIDToken` | every path (`*`) | "Every file in this repository requires **review** by the Chief Architect." | **Review responsibility**, not approval authority. `@AuraIDToken` is an account identifier; no document maps it to a named person or to the Chief Architect role | — | Records a role-to-account mapping nowhere else established | `.github/CODEOWNERS` |
| ADR-001_DOCUMENT_MODEL (S-09) | **Protocol Custodian** | SPEC lifecycle | "approves SPECs, is owner of SPEC lifecycle, and is **signatory for normative acceptance**" | Approval authority over SPEC | **PROPOSED — not in force** | Conflicts with GOV-001 §2, which grants no SPEC authority to anyone | `adrs/ADR-001_DOCUMENT_MODEL.md:54` |
| ADR-001_DOCUMENT_MODEL | **Architecture Board** | ARC baselines and architecture ADRs | "approves and owns ARC baselines and ADRs related to architecture decisions" | Approval authority over ADRs | **PROPOSED** | Conflicts with GOV-001 §6 ("merging = accepting") and §3 (ADR owner = decision author) | ibid. `:55` |
| ADR-001_DOCUMENT_MODEL | **Release Authority** | APS publication | "owns APS publication and release mechanics" | Publication authority | **PROPOSED** | Role appears in no other document | ibid. `:56` |
| ADR-001_DOCUMENT_MODEL | **Compliance Authority / Auditor** | traceability artifacts | "owns TRACEABILITY artifacts and evidence retention policy" | Ownership | **PROPOSED** | Role appears in no other document | ibid. `:57` |
| CONSTITUTIONAL_DECREE Art. V | **Custodian of the Protocol** | "ALL AI ASSISTANCE" (`:5`) | "May modify constitutional constants; may authorize new tasks; may seal and archive the instrument" | Authority over the instrument's constants, tasks, sealing | "MANDATORY / NON-OVERRIDABLE"; no lifecycle status in either corpus's registry | Placement contested — `02_DOCUMENT_HIERARCHY_EVIDENCE.md` H-1 vs H-3/H-4 | `CONSTITUTIONAL_DECREE.md:236-252` |
| CONSTITUTIONAL_DECREE Art. X | **Custodian** | `core/` changes | "Custodian Signature: [Required for core/ changes]" | Merge-gating signature | as above | **No such signature exists for any commit**; recorded by R-01 §9 G-11 and re-verified: no signed attestation file, no `Accepted-by`/signature convention in the repository | `CONSTITUTIONAL_DECREE.md:442` |
| ROLE §2.2.1 | **Protocol Custodian** | `core/`, constitutional constants, layer boundaries, cryptographic primitives | "The Custodian has **FINAL AUTHORITY** over: All changes to `core/` directory …" | Approval authority over an artifact set | "CANONICAL"; authority self-cited to Decree Art. V | Conflicts with nothing in the implementation corpus; **unknown relation** to the Chief Architect's authority in the specification corpus | `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md:117-123` |
| ROLE §2.1.1 | **Protocol Custodian** | Sentinel Drift Threshold, Scaling Factor, fixed-point precision | "MAY modify … but only with: full mathematical justification; regulatory impact assessment; **creation of new instrument version (not update)**; comprehensive documentation" | Conditional authority over constants | CANONICAL | Interacts with the ARI quantization question — see `06_ARI_DECISION_AUTHORITY.md` | ibid. `:70-84` |
| ROLE §2.1.4 | **Protocol Custodian** | sealing | "**SOLE AUTHORITY** to: declare the instrument ready for sealing …" | Sealing authority | CANONICAL | — | ibid. `:104-113` |
| ROLE §7.1 / Decree Art. V | **AI Copilot / AI assistants** | this repository | "MAY NOT: modify constitutional constants; override Custodian decisions; **approve core changes independently**; seal the instrument" | Prohibition | CANONICAL / MANDATORY | Consistent with AURA-CON-001 Art. VIII | `ROLE…:549-562`; `CONSTITUTIONAL_DECREE.md:244-252` |
| `docs/ops/PROTOCOL_CUSTODIAN.md` | **Protocol Custodian** | "Aura Protocol v3.3 and all sealed derivatives" | "the **sole human authority** allowed to: maintain the physical and cryptographic integrity of the instrument …" | Custodianship | "CANONICAL / BINDING" | A second, differently-scoped custodian document coexists with `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md`; neither states which governs | `docs/ops/PROTOCOL_CUSTODIAN.md:1-30` |
| AGENTS.md rule 13 | **"Human"** | protocol-affecting changes | "Human approval is required before merging protocol-affecting changes." | Approval requirement with **no named approver** | no status | Does not say *which* human; `AGENTS.md:53` says "human/Protocol Custodian" | `AGENTS.md:32, 53` |
| CHANGELOG policy line | *(unnamed)* | every logged task | "Each entry in this log documents a completed task that was **authorized before execution**." | An assertion that authorization occurred | no status | **No authorization artifact is referenced by any entry** | `CHANGELOG.md:10` |

---

## 2. Per-artifact approver table

As required: no generalization from one artifact class to another.

| Artifact | Explicit Approver | Source | Scope | Status |
|---|---|---|---|---|
| **AURA Constitution (amendment)** | Chief Architect | AURA-CON-001 Art. XI step 5; GOV-001 §2, §5.3 step 5 | Constitution only | **ESTABLISHED** in text; the approving role is never mapped to a person or account |
| **APS document status transition (APPROVED → FROZEN)** | Chief Architect | GOV-001 §2; POL-VER-001 §3 | APS documents | **ESTABLISHED** in text (both sources DRAFT) |
| **APS document content (authoring a new section/requirement)** | *(process, not approver)* RFC → Architecture Review → PR | CONTRIBUTING type table `:23`; GOV-001 §5.2 | new APS content | **PARTIALLY ESTABLISHED** — the process is stated; the merge/approval actor for step 7 is not |
| **SPEC document (e.g. SPEC-002)** | **ABSENT / EVIDENCE GAP** | — | — | GOV-001 §2's list does not include SPEC; POL-VER-001 governs "APS documents and governance artifacts"; the only source assigning SPEC approval is S-09, **PROPOSED and not in force**. SPEC-002 itself records "Owner: Protocol Custodian" in its header — an **ownership** field, not an approval grant |
| **ADR** | *(mechanism, not actor)* "Merging the PR = accepting the ADR" | GOV-001 §6 steps 6–7; `adrs/README.md:23` | ADRs | **PARTIALLY ESTABLISHED** — the mechanism is explicit; **no approver is named**, and merge authority is unassigned for this class |
| **ADR (contested alternative)** | Architecture Board | S-09 `:55` | architecture ADRs | **NOT IN FORCE** (PROPOSED) |
| **RFC** | Chief Architect, after ARB vote | GOV-001 §7 steps 7–8 | RFCs | **PARTIALLY ESTABLISHED** — actor named; the ARB that must first vote has no established existence |
| **Protocol Invariant addition/removal** | Chief Architect | GOV-001 §2 | APS-100 invariants | **ESTABLISHED** in text |
| **New reference implementation recognition** | Chief Architect | GOV-001 §2 | RI registry | **ESTABLISHED** in text |
| **Conformance test change** | *(process)* RFC → PR referencing RFC | CONTRIBUTING `:25`; POL-VER-001 §6 | CONF tests | **PARTIALLY ESTABLISHED** |
| **Reference fixture** | *(process)* "PR with fixture file + test linkage" | CONTRIBUTING `:26` | fixtures | **PARTIALLY ESTABLISHED** — no approver named; POL-VER-001 §7 governs versioning only |
| **Governance change (spec repo)** | Major Change process (§5.2) | GOV-001 §11 | GOV-001 itself | **PARTIALLY ESTABLISHED** |
| **Implementation change to `core/`** | Protocol Custodian ("FINAL AUTHORITY"), with "Custodian Signature" required | ROLE §2.2.1; Decree Art. X | `aura-poc-a-core-v3.3/core/` | **ESTABLISHED** in text; **no signature instance exists** |
| **Implementation change generally** | "Human approval … before merging protocol-affecting changes" | AGENTS.md rule 13 | this repository | **PARTIALLY ESTABLISHED** — no actor named |
| **Constitutional constants (implementation corpus)** | Protocol Custodian, conditionally | ROLE §2.1.1; Decree Art. V | 0.68, 100,000, Q16.16 | **ESTABLISHED** in text, with mandatory conditions including "creation of new instrument version (not update)" |
| **Sealing the instrument** | Protocol Custodian ("SOLE AUTHORITY") | ROLE §2.1.4; Decree Art. VIII | v3.3 | **ESTABLISHED** in text; not exercised (no tag, no checksum, `[COMPUTED_AT_SEALING_v3.3]` unfilled) |
| **Frozen artifacts (any correction)** | **ABSENT / EVIDENCE GAP** | — | — | The only text is INV-DOC-008 in S-09 ("corrections require a new superseding artifact"), **PROPOSED, not in force**; recorded by R-01 §5.1 |
| **ARI semantics** | **ABSENT / EVIDENCE GAP** | — | — | No source names ARI as an artifact class over which anyone holds authority — see `06_ARI_DECISION_AUTHORITY.md` |

---

## 3. Merge authority, separately

Recorded separately because `REVIEWER ≠ APPROVER` and `CODEOWNER ≠ AUTHORITY`.

| Statement | Source | What it establishes |
|---|---|---|
| "Chief Architect or delegate may merge" (PATCH lane only) | GOV-001 §5.1 step 4 | Merge authority for PATCH changes; "delegate" is undefined and unnamed |
| "Do not merge your own RFC" | CONTRIBUTING `:60`; `rfcs/README.md:45` | A prohibition on the author; does not name who may |
| "Do not merge your own non-trivial pull requests" | CONTRIBUTING `:79` | As above |
| "Every file in this repository requires review by the Chief Architect" (`* @AuraIDToken`) | `.github/CODEOWNERS` | A **review** requirement enforced by GitHub; CODEOWNERS cannot confer governance authority, and the corpus nowhere states that `@AuraIDToken` is the Chief Architect |
| "Merging the PR = accepting the ADR" | GOV-001 §6 | Ties acceptance to merge without naming who may merge — so ADR acceptance authority is, in effect, whoever holds repository merge permission. **This is a platform permission, not a documented governance grant.** Recorded as a finding. |
| No CODEOWNERS in the implementation repository | verified absent | No path-level review requirement exists for `core/`, despite Decree Art. X requiring a Custodian signature for `core/` changes |

---

## 4. Role identity — who these actors actually are

| Role | Named in | Identified as a person or account? |
|---|---|---|
| **Chief Architect** | AURA-CON-001 Art. VIII; GOV-001; POL-VER-001; spec README; CODEOWNERS comment | **No.** No document names the individual. `CODEOWNERS` maps all paths to `@AuraIDToken` and its comment calls that review "by the Chief Architect", but no governance document states that the account **is** the Chief Architect |
| **Protocol Custodian** | Decree (signature block, `:463-464`); ROLE header; `docs/ops/PROTOCOL_CUSTODIAN.md`; README §10 | **Yes** — "Kamil Krasiński", in the implementation corpus only |
| **Architecture Review Board** | GOV-001 §2, §5.2, §7 | **No.** No roster, charter, or ARR |
| **Architecture Board** (distinct name) | S-09 `:55` | **No.** PROPOSED document only |
| **Release Authority** | S-09 `:56` | **No** |
| **Compliance Authority / Auditor** | S-09 `:57` | **No** |
| **"Human"** (AGENTS.md rule 13) | AGENTS.md | **No** |

> **Central identity gap.** The specification corpus vests approval in the **Chief Architect**;
> the implementation corpus vests it in the **Protocol Custodian**. **No document in either
> corpus states whether these are the same person, the same role, or different roles.** Every
> cross-corpus approval question depends on this and it is nowhere answered.
> Recorded as `OQ-A-GAP-002`.

---

## 5. OQ-A-002 — finding

| Question | Finding |
|---|---|
| Is there an approval authority for the Constitution, APS status transitions, invariants and RI recognition? | **ESTABLISHED in text** — Chief Architect, per GOV-001 §2 and AURA-CON-001 Art. XI. Both establishing documents other than the Constitution are DRAFT. |
| For ADRs? | **PARTIALLY ESTABLISHED** — acceptance is by merge; no approver named; a PROPOSED ADR would assign it to an Architecture Board |
| For SPEC documents? | **ABSENT / EVIDENCE GAP** |
| For implementation `core/` changes? | **ESTABLISHED in text** — Protocol Custodian, with a required signature that has never been produced |
| For ARI semantics? | **ABSENT / EVIDENCE GAP** |
| Are the two corpora's approval authorities the same actor? | **EVIDENCE GAP** — never stated |
| Is any approval authority operationally exercisable today? | **Not demonstrable.** The ARB has no established existence; no RFC has ever been filed; no ARR exists; no Custodian signature exists; the CI enforcement jobs specified by S-09 do not exist |

**Status: PARTIALLY ESTABLISHED, with the cross-corpus identity question an EVIDENCE GAP.**

No authority is selected or recommended here.

---

*This document has no normative effect. It records authority claims and their scope. It grants no
authority, appoints no actor, and resolves no conflict.*
