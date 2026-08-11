# DR-002 — DECISION BRIEF

**Authority to approve and govern SPEC, ADR and RFC artifacts**

| Field | Value |
|---|---|
| Document ID | DR-002_DECISION_BRIEF |
| Version | 1.0-DRAFT |
| Status | DRAFT — DECISION PREPARATION ONLY · **UNCOMMITTED WORKING FILE** |
| Date | 2026-08-11 |
| Evidence base | `DR-002_EVIDENCE_PACKAGE.md` (commit `ed590e6`) and the sources it cites |
| Normative effect | **NONE** |

---

> **THIS BRIEF MAKES NO DECISION.**
>
> It does not recommend Chief Architect, Protocol Custodian, Architecture Board, Architecture
> Review Board, Release Authority, Compliance Authority, or any other role or body. It creates
> and modifies no governance document. GOV-001, the AURA Constitution and SPEC-002 are
> untouched. No ADR is created. No commit and no pull request is made.
>
> Section 7 presents candidate models **because the repository's own terminology contains
> them**, not because any is preferred. Presentation is not endorsement, and the models are
> deliberately ordered by document rank of their source rather than by any assessment of merit.

**Scope restriction.** Only evidence in `DR-002_EVIDENCE_PACKAGE.md` and the documents it cites
is used. Identifiers `X-n`, `C-n`, `A-n`, `M-n`, `E-2.n.n` refer to that package.

---

## 1. Decision Question

> **Which role or body holds authority to approve and govern SPEC, ADR and RFC artifacts — and
> by what recorded act is that authority exercised?**

### 1.1 Precise form

The question is unresolved in four independent respects. Each must be answered for the question
to be answered; none is answered here.

| # | Component |
|---|---|
| **Q-A** | Which role or body may **approve a SPEC-class document**, moving it from DRAFT to a state carrying normative effect? |
| **Q-B** | Which role or body may **accept an ADR**, and by what act is acceptance recorded? |
| **Q-C** | Which role or body may **accept or reject an RFC**, and is any prerequisite step executable? |
| **Q-D** | Which role or body conducts the **Architecture Review** that the FROZEN Constitution requires as a precondition of amendment, and which the DRAFT process documents require for major changes? |

### 1.2 Why it is antecedent

SPEC-002 §9 criterion 1 requires every requirement to be backed by an approved normative source
or an approved architecture decision. An approval that cannot be attributed to an authorised
approver is not demonstrable as an approval. DR-002 therefore gates the closure of every AD-CA
domain (§9), not by policy preference but by the structure of the approval step common to all
of them.

---

## 2. Current Evidence — explicit authority assignments only

Only direct grants naming both a role and an act. Inference, frequency, ownership,
authorship and permissions are excluded.

### 2.1 Grants of FROZEN rank — `AURA-CON-001 v1.0`

| # | Grant | Section | Scope as written |
|---|---|---|---|
| **X-1** | Chief Architect **approves Constitution amendments** | Art. XI(5) | Constitution only |
| **X-2** | Chief Architect is **"responsible for the project"** | Art. VIII | Unbounded; unenumerated |
| **X-3** | AI systems **MUST NOT approve** canonical documents or modify frozen documents | Art. VIII | Prohibition |

**These three are the entire set of FROZEN-rank role grants.** No FROZEN source addresses SPEC,
ADR, RFC, ARC or APS status transitions, and no FROZEN source names any role other than
Chief Architect. The string "Protocol Custodian" does not appear in the Constitution.

### 2.2 Grants from DRAFT sources — `GOV-001 1.0-DRAFT`, `POL-VER-001 1.0-DRAFT`

| # | Grant | Section | Scope as written |
|---|---|---|---|
| **X-4** | Chief Architect has **"final and sole approval authority"** over: Constitution amendments · APS status transitions APPROVED→FROZEN · Protocol Invariant additions/removals · new RI recognition | GOV-001 §2 | **Closed four-item list** |
| **X-5** | Chief Architect **approves** at step 5 of the Major Change process | GOV-001 §5.2 | RFC-bearing changes |
| **X-6** | Chief Architect gives **final approval** of RFCs | GOV-001 §7(8) | RFC class |
| **X-7** | ARB **votes ACCEPT / REJECT / DEFER** on RFCs | GOV-001 §7(7) | RFC class |
| **X-8** | ARB performs **"assessment"** in Major Changes | GOV-001 §5.2(4) | character unspecified |
| **X-9** | Chief Architect **chairs** review meetings producing ARRs | GOV-001 §8 | ARR production |
| **X-10** | Chief Architect **or delegate** may merge | GOV-001 §5.1 | **PATCH only** |
| **X-11** | Chief Architect approves `REVIEW → APPROVED` and `APPROVED → FROZEN` | POL-VER-001 §3 | "every APS document and governance artifact" |
| **X-12** | Chief Architect approves changes to the versioning policy | POL-VER-001 §10 | POL-VER-001 |

### 2.3 Grants from a PROPOSED source — `ADR-001_DOCUMENT_MODEL` *(recorded; not in force)*

| # | Grant | Scope as written |
|---|---|---|
| **X-13** | **Protocol Custodian approves SPECs**; owns SPEC lifecycle; signatory for normative acceptance | SPEC class |
| **X-14** | **Architecture Board approves ARC baselines and ADRs** | ARC, ADR |
| **X-15** | **Release Authority publishes APS** | APS class |
| **X-16** | **Compliance Authority / Auditor owns traceability and evidence retention** | compliance |

### 2.4 Grants scoped to the implementation instrument — `S3`

| # | Grant | Scope as written |
|---|---|---|
| **X-17** | Protocol Custodian has **SOLE AUTHORITY** to seal and archive the instrument | the instrument |
| **X-18** | Protocol Custodian has **FINAL AUTHORITY** over `core/`, constants, layer boundaries, crypto | the instrument |
| **X-19** | Protocol Custodian has **ABSOLUTE OVERRIDE AUTHORITY** | the instrument |
| **X-20** | Custodian of the Protocol may modify constants, authorize tasks, seal and archive | the instrument |

**None of X-17…X-20 grants authority over any document in the specification repository.** Every
enumerated power concerns the measurement instrument, and all derive from
`CONSTITUTIONAL_DECREE` Article V rather than from the AURA Constitution.

### 2.5 Explicit grants relevant to the four artifact-class questions

| Question | Explicit grant in an **in-force** document? |
|---|---|
| **Q-A** SPEC approval | **NONE.** Only X-13, from a PROPOSED source. |
| **Q-B** ADR acceptance | **NONE.** Acceptance is bound to merging with no actor named. X-14 is PROPOSED. |
| **Q-C** RFC approval | **X-6 exists** (Chief Architect, final approval) — see §6.3, which explains why this does not close Q-C. |
| **Q-D** Architecture Review | **NONE** defines the act or constitutes the conducting body. |

---

## 3. Conflict Set

Direct contradictions between sources. **None is reconciled here.**

| # | Contradiction | Sources | Bears on |
|---|---|---|---|
| **C-1** | **Two roles named as SPEC approver** | POL-VER-001 §3 (Chief Architect, DRAFT, scoped to "every APS document and governance artifact") vs `ADR-001_DOCUMENT_MODEL` X-13 (Protocol Custodian, PROPOSED) vs `SPEC_TEMPLATE.md` line 32 (Protocol Custodian) vs `SPEC_TEMPLATE.md` line 9 (both, as interchangeable options) vs GOV-001 §2 (neither — no SPEC class) | **Q-A** |
| **C-2** | **ADR acceptance attributed to an unnamed actor, and separately to a body** | GOV-001 §6(6–7) "Merging the PR = accepting the ADR", no actor · `adrs/README.md` "Merging = accepting", no actor · X-14 Architecture Board (PROPOSED) · GOV-001 §5.2(5) Chief Architect approval upstream of ADR creation | **Q-B** |
| **C-3** | **"Architecture Review Board" and "Architecture Board" are distinct strings, never equated** | GOV-001 §2/§5.2/§7 and `rfcs/README.md` (ARB: conducts ARRs, assesses, votes) vs `ADR-001_DOCUMENT_MODEL` and `arc/README.md` (Architecture Board: approves ARC and ADRs) | **Q-C, Q-D** |
| **C-4** | **APS status authority vested in two bodies** | GOV-001 §2 "final and **sole**" over APS APPROVED→FROZEN vs X-15 Release Authority publishes APS | Q-A (indirect) |
| **C-5** | **SPEC freeze assigned to different roles** | POL-VER-001 §3 (Chief Architect; requires Constitution Art. XI procedure) vs `ADR-001_DOCUMENT_MODEL` line 29 (Protocol Custodian; no Art. XI reference) | **Q-A** |
| **C-6** | **CONTRIBUTING.md omits an approver GOV-001 reserves** | CONTRIBUTING.md "New Protocol Invariant → RFC → Architecture Review → **PR**" (no approver) vs GOV-001 §2 reserving Invariant additions to the Chief Architect. The adjacent Constitution row *does* name an approver. | Q-C, Q-D |
| **C-7** | **Two `ADR-001` documents specify different approval requirements** | `adrs/ADR-001_DOCUMENT_MODEL.md` (PROPOSED): one approver, field `Accepted-by:` · `docs/adr/001-document-model.md` (DRAFT): **two** approvers required, field `accepted_by` · `adrs/ADR-001_REPOSITORY_STRUCTURE.md` (ACCEPTED): no approver recorded · `ADR_TEMPLATE.md`: **no approver field at all** | **Q-B** |
| **C-8** | **Two documents named as top of the authority hierarchy** | Constitution Art. V (`Constitution → APS-001 → APS-100 → ADR/ARR/RFC → …`, no Decree) vs S3 `AGENTS.md`/`CLAUDE.md` Authority Precedence (`Aura Constitutional Decree` ranked **above** Aura Protocol Specification) | **Q-A…Q-D**, cross-repository |

---

## 4. Ambiguity Set

Cases where the source text permits more than one reading. **No reading is selected.**

| # | Ambiguity | Readings permitted by the text |
|---|---|---|
| **A-1** | **"Responsible for the project" is unenumerated** (X-2) against GOV-001 §2's closed list (X-4) | (i) Art. VIII is a general grant; the list is illustrative → SPEC authority follows from Art. VIII. (ii) "final and **sole**" is exhaustive → items outside the four are not the Chief Architect's. |
| **A-2** | **Whether "Protocol Custodian" and "Chief Architect" denote one office** | (i) same office, two names — `SPEC_TEMPLATE.md` line 9; S3 Decree Art. V "(Architect)". (ii) distinct offices, distinct scopes — S3 grants uniformly instrument-scoped; S1 grants document-scoped. (iii) distinct offices, overlapping scope — `copilot-instructions.md` extends Custodian to "all canonical definitions". (iv) one person, two offices — supported by no text, excluded by none. |
| **A-3** | **The solidus in "Architecture Board/Protocol Custodian"** (`arc/README.md` line 10; also `SPEC_TEMPLATE.md` line 9, S3 `README.md` line 389) | either suffices · both required · same body · undecided shorthand |
| **A-4** | **"An Architecture Review" as act or as body** | an act the Chief Architect performs (GOV-001 §8 "chaired by") · an act the ARB performs (GOV-001 §2 "conducts ARRs") · a meeting requiring both |
| **A-5** | **"Canonical document" is undefined** — the class on which X-3, README §Governance and CODE_OF_CONDUCT all turn | APS-000 §5 defines six **statuses**, not this **class**. Whether SPEC-002 belongs to it is undetermined. |
| **A-6** | **GOV-001 §2 renders the FROZEN Constitution as a child node of the Chief Architect** | (i) the tree depicts custodial responsibility, not authority over the Constitution. (ii) the tree depicts authority, in which a DRAFT document subordinates a FROZEN one — conflicting with Constitution Art. V. |
| **A-7** | **"Owner" versus "approver"** — GOV-001 §3 assigns ADR ownership to "Decision author", RFC ownership to "Proposer" | ownership and approval are distinct · ownership implies approval. GOV-001 never defines "Owner". **Bears directly on SPEC-002, whose only authority statement is `Owner: Protocol Custodian`.** |
| **A-8** | **The ARB's act is named four ways** — "conducts ARRs" (§2), "assessment" (§5.2), "votes ACCEPT/REJECT/DEFER" (§7), "REVIEW" (`rfcs/README.md`) | one act under four names · distinct acts per process. Whether the assessment is advisory or binding is stated nowhere. |
| **A-9** | **Whether SPEC-002 falls under POL-VER-001** | §1 scopes to "APS documents, Protocol Invariants, Conformance Tests, Reference Fixtures, and releases" — SPEC not named. §3 then says "Every **APS document and governance artifact**". (i) SPEC-002 is a governance artifact → X-11 applies → Chief Architect is its approver. (ii) SPEC is outside scope → X-13 (PROPOSED) is the only applicable grant. **This ambiguity is the direct locus of C-1.** |

---

## 5. Missing Definitions

Concepts referenced by governance text but never formally defined.

| # | Undefined concept | Referenced at | What is missing |
|---|---|---|---|
| **M-1** | **Artifact "owner"** | Constitution Art. VI; GOV-001 §3 | What ownership confers. Bears on A-7 and on SPEC-002's sole authority statement. |
| **M-2** | **"Architecture Review"** | Constitution Art. XI(2); CONTRIBUTING.md; ROADMAP.md; POL-VER-001 §3; GOV-001 §5.2, §8 | What constitutes one; who convenes; quorum; output validity. |
| **M-3** | **ARB · Architecture Board · Release Authority · Compliance Authority** | GOV-001 §2/§5.2/§7; `ADR-001_DOCUMENT_MODEL`; `arc/README.md`; `rfcs/README.md` | **None of the four is defined, constituted, or given membership, appointment method, quorum or term. No document states that any currently exists.** |
| **M-4** | **Who may merge** | GOV-001 §6; `adrs/README.md`; `rfcs/README.md` "Do not merge your own RFC" | Acceptance is bound to merging; the merging actor is named only for PATCH (X-10). `ADR_TEMPLATE.md` has no approver field. |
| **M-5** | **"Explicit architectural authority"** | SPEC-002 §3 constraint 4, §6 | The term SPEC-002 uses for its own approver is never bound to a role. |
| **M-6** | **"Delegate"** | GOV-001 §5.1 | Who may be one; how delegation is conferred, recorded, revoked; its scope. |
| **M-7** | **"Specification Contributors"** | GOV-001 §2 | Qualification, admission, standing. |
| **M-8** | **"Documentation Architect"; "Chief Specification Architect"** | `ADR-001_REPOSITORY_STRUCTURE` front matter; `ADR-001_DOCUMENT_MODEL` front matter | Two further architect-titled strings, each appearing once, defined nowhere, related to "Chief Architect" nowhere. |
| **M-9** | **Approval thresholds, quorum, signature format** | `ADR-001_DOCUMENT_MODEL` Open Questions | Listed by that document itself as unresolved. |
| **M-10** | **Appointment / identification of the Chief Architect** | Constitution Art. VIII; GOV-001 §2 | How the office is filled, recorded, succeeded. *(S3 defines Custodian succession — for the instrument role only.)* |
| **M-11** | **"Canonical document"** | Constitution Art. VIII; README.md; CODE_OF_CONDUCT.md | The class is never defined. Whether SPEC-002 belongs to it is undetermined (A-5). |
| **M-12** | **Cross-repository authority** | SPEC-002 §2.2 constrains S3; APS-950 §11 designates RI-PY/RI-RS; S3 governs itself by Decree | Whether an S1 role has authority in S3, or vice versa. |
| **M-13** | **`DRAFT → REVIEW` approver** | POL-VER-001 §3 | The first lifecycle transition names no approver. |
| **M-14** | **Whether a role is a person or a body** | throughout | Six role strings are unclassified as individual or collective. |

---

## 6. Current Authority Gap

Why no current source establishes each of the four authorities. Each subsection states the
mechanism of the gap, not a preference about how to close it.

### 6.1 SPEC approval authority — **NOT ESTABLISHED**

Three routes exist by which a SPEC approver could be identified. All three fail, for different
reasons.

**Route 1 — GOV-001 §2 (X-4).** The grant is worded "final and **sole** approval authority
over" followed by four enumerated items: Constitution amendments; APS status transitions
APPROVED→FROZEN; Protocol Invariant additions/removals; new RI recognition. **SPEC is not among
them**, and cannot be, because GOV-001 contains no SPEC artifact class at all — §3's governance
artifact table lists ADR, ARR, RFC, ADC, ACI, EPR and no SPEC row. The route fails by omission.

**Route 2 — POL-VER-001 §3 (X-11).** This grants the Chief Architect `REVIEW → APPROVED` for
"every APS document **and governance artifact**". Whether SPEC-002 is a "governance artifact" is
**A-9**: §1's scope enumeration does not name SPEC. The route fails on an unresolved
classification question, not on absence of a grant.

**Route 3 — `ADR-001_DOCUMENT_MODEL` (X-13).** This is the **only** text in any inspected
repository that grants SPEC approval authority to anyone. Its status is **PROPOSED**. It states
of itself that it "requires explicit approval by the Protocol Custodian" — the role it
constitutes. The route fails on a circularity: **the authority empowered to accept the document
is created by the document awaiting acceptance.**

**Net:** SPEC-002 declares `Normative effect: NONE until APPROVED` and refers to an "explicit
architectural authority" (M-5) that no in-force document binds to a role.

### 6.2 ADR approval authority — **NOT ESTABLISHED**

**GOV-001 §6 makes acceptance a consequence of an act, not a decision by a person.** Step 6
reads "Merging the PR = accepting the ADR"; step 7, "ADR status set to ACCEPTED". No actor is
named at either step. `adrs/README.md` repeats the formula identically. The only merge-authority
grant in the corpus (X-10) is expressly scoped to **PATCH-class changes**, which AD-CA decisions
are not.

Three further defects compound it:
- **X-14** (Architecture Board approves ADRs) exists only in the PROPOSED source, and names a
  body that is not constituted (**M-3**).
- **`ADR_TEMPLATE.md` contains no approver, owner or acceptance field**, so no template-sanctioned
  place exists to record an approval even if one were given.
- The two `ADR-001` documents specify **different numbers of approvers and different field
  names** (**C-7**), so the corpus does not agree with itself on the form of the record.

**Net:** an ADR resolving an AD-CA domain would today be "accepted" by an unspecified party
performing a merge, recorded in a field that the canonical template does not define.

### 6.3 RFC approval authority — **NAMED BUT NOT EXECUTABLE**

This case differs materially from §6.1 and §6.2 and is stated separately to avoid overstating
the gap.

**An approver is explicitly named.** GOV-001 §7(8) grants the Chief Architect "final approval"
of RFCs (**X-6**), and `templates/RFC_TEMPLATE.md` line 105 records `Decided by: Chief
Architect`. On the question "who approves an RFC", the corpus does supply an answer from an
in-force document.

**The prerequisite step cannot be performed.** GOV-001 §7(7) places immediately before final
approval: "**Architecture Review Board votes: ACCEPT / REJECT / DEFER**". GOV-001 §5.2(4)
likewise requires "Architecture Review Board assessment" in the Major Change path. Per **M-3**,
the ARB is **not defined, constituted, or given membership, quorum or appointment method
anywhere**, and no document states that it exists. A process whose penultimate step requires a
vote by a body that has not been constituted cannot be executed as written.

Two secondary defects: the ARB's act is named four different ways (**A-8**) with its binding or
advisory character never stated; and `CONTRIBUTING.md`'s process rows for APS sections and
Protocol Invariants terminate at "PR" with no approver, contradicting GOV-001 §2 (**C-6**).

**Net:** the RFC gap is not "who approves" but "whether the path to approval can be walked".

### 6.4 Architecture Review authority — **NOT ESTABLISHED**

An Architecture Review is a **precondition of FROZEN-rank action**: Constitution Art. XI(2)
requires one for any Constitution amendment. It is further required by CONTRIBUTING.md for new
APS sections and new Protocol Invariants, by POL-VER-001 §3 for `REVIEW → APPROVED`, and by
GOV-001 §5.2 for all Major Changes.

Nothing defines it (**M-2**): not what constitutes one, not who convenes it, not quorum, not
what makes its output valid. The conducting body is ambiguous between the Chief Architect
(GOV-001 §8, "chaired by") and the ARB (GOV-001 §2, "conducts ARRs") — **A-4** — and the ARB is
unconstituted (**M-3**). GOV-001 §8 requires an ARR be "published to `/adrs/ARR-NNN_TITLE.md`
within 5 days"; **no ARR exists in the repository.**

**Net:** a step required by the only FROZEN-rank amendment procedure is undefined, its
conducting body is contested and unconstituted, and it has never been performed on the record.

### 6.5 Structural summary of the gap

| Authority | Named in an in-force document? | Executable? | Mechanism of failure |
|---|---|---|---|
| SPEC approval | **No** | No | Omission (GOV-001), classification ambiguity (A-9), circularity (X-13) |
| ADR acceptance | **No** | Indeterminate | Actorless act; no template field; corpus self-inconsistent (C-7) |
| RFC approval | **Yes** (X-6) | **No** | Prerequisite body unconstituted (M-3) |
| Architecture Review | **No** | No | Act undefined (M-2); body contested (A-4) and unconstituted (M-3) |

---

## 7. Candidate Governance Models

**Presented, not selected.** Each model below is assembled **only** from role strings and
authority statements that already exist in the repositories. No model is invented, none is
recommended, and the ordering is by the document rank of each model's primary source — not by
merit. Best practice from outside the repository is not introduced.

---

### Model I — Constitutional Minimal

| Field | Content |
|---|---|
| **Authority role/body** | Chief Architect (sole named role); "AI systems" as a constrained category |
| **Scope** | Constitution amendments (X-1); "the project" (X-2) |
| **Evidence supporting existence** | `AURA-CON-001 v1.0` **FROZEN** — Art. VIII, Art. XI(5). The **only** role grants of FROZEN rank in the corpus. Reinforced by `CODE_OF_CONDUCT.md`, `README.md` §Governance, `constitution/README.md`, `ROADMAP.md`, `SECURITY.md`, `templates/RFC_TEMPLATE.md`, `templates/CONFORMANCE_REPORT_TEMPLATE.md`. |
| **Evidence contradicting or limiting it** | Art. VIII is **unenumerated** — it never states which artifact classes it reaches (**A-1**). The Constitution's hierarchy (Art. V) contains **no SPEC class** (E-2.1.6), so it assigns no authority over SPEC because it does not contemplate SPEC. Art. VI requires every artifact have an "owner" but names none (**M-1**). |
| **Unresolved dependencies** | A-1 (is the grant general or bounded?) · A-5 / M-11 (is SPEC-002 a "canonical document"?) · M-2 (what is an Architecture Review?) · M-10 (how is the office filled?) · M-14 (person or body?) |

---

### Model II — GOV-001 Four-Tier

| Field | Content |
|---|---|
| **Authority role/body** | Chief Architect · Architecture Review Board (ARB) · Specification Contributors · AI Assistants |
| **Scope** | Chief Architect: the closed four-item list (X-4) plus RFC final approval (X-6), review chairing (X-9), PATCH merge (X-10). ARB: RFC votes (X-7), Major Change assessment (X-8). Contributors: authoring only. AI: propose/implement/test, never approve or freeze. |
| **Evidence supporting existence** | `GOV-001 §2` authority tree; §3 artifact-owner table; §5.1, §5.2, §6, §7, §8, §9. Reinforced for the ARB by `rfcs/README.md` lifecycle. Aligned with POL-VER-001 §3/§10 (X-11, X-12) and CONTRIBUTING.md's Constitution row. |
| **Evidence contradicting or limiting it** | GOV-001 is **`1.0-DRAFT`**. Its §2 list is **closed and excludes SPEC, ADR and RFC acceptance** (§6.1 Route 1). §6 makes ADR acceptance actorless (**C-2**). The **ARB is not constituted** (**M-3**), so X-7/X-8 cannot be exercised (§6.3). Its §2 tree renders the FROZEN Constitution as a child of the Chief Architect (**A-6**). "Delegate" (**M-6**) and "Specification Contributors" (**M-7**) are undefined. CONTRIBUTING.md contradicts §2 on Invariants (**C-6**). |
| **Unresolved dependencies** | M-3 (constitute the ARB) · M-4 (who merges) · A-8 (is the ARB act binding?) · A-9 (does POL-VER-001 reach SPEC?) · A-6 · A-1 |

---

### Model III — Document-Model Four-Body

| Field | Content |
|---|---|
| **Authority role/body** | Protocol Custodian · Architecture Board · Release Authority · Compliance Authority / Auditor |
| **Scope** | Custodian: approves SPECs, owns SPEC lifecycle, signatory for normative acceptance (X-13), and SPEC freeze. Architecture Board: approves and owns ARC baselines **and ADRs** (X-14). Release Authority: APS publication (X-15). Compliance Authority: traceability and evidence retention (X-16). |
| **Evidence supporting existence** | `adrs/ADR-001_DOCUMENT_MODEL.md` "Owners and Authorities" and "Lifecycle Summary"; the divergent copy at `docs/adr/001-document-model.md`. Reinforced by `SPEC_TEMPLATE.md` line 32, `arc/README.md` line 10, and SPEC-002's own front matter `Owner: Protocol Custodian`. **This is the only model that supplies a SPEC approver at all.** |
| **Evidence contradicting or limiting it** | Status **PROPOSED**; the second copy is **DRAFT** — neither is in force. **Circular**: it requires approval by the Protocol Custodian, the role it constitutes (§6.1 Route 3). Its own Open Questions record that **thresholds, quorum and signature format are undefined** (**M-9**). The two copies require **different numbers of approvers and different field names** (**C-7**), and both carry the identifier `ADR-001`, already held by an ACCEPTED document. **Architecture Board, Release Authority and Compliance Authority are constituted nowhere** (**M-3**). Conflicts with GOV-001 §2 on APS authority (**C-4**) and with POL-VER-001 §3 on freeze (**C-5**). Depends on the ARC layer, which is empty (`arc/` README-only; `arc_to_spec_mapping.yaml` = `mappings: []`). |
| **Unresolved dependencies** | The circularity (§6.1 Route 3) · C-7 (identifier collision and record form) · M-3 (constitute three bodies) · M-9 (thresholds and signature) · C-3 (is Architecture Board the ARB?) · the document-model question itself (DR-003) |

---

### Model IV — Interchangeable-Title

| Field | Content |
|---|---|
| **Authority role/body** | A single office denoted by either "Protocol Custodian" or "Chief Architect" |
| **Scope** | The union of Models I–III grants, on the reading that the two strings name one office |
| **Evidence supporting existence** | `templates/SPEC_TEMPLATE.md` line 9: `Owner: Role / Name (Protocol Custodian / Chief Architect)` — presenting them as interchangeable fill-in options. S3 `CONSTITUTIONAL_DECREE` Art. V: "**Custodian of the Protocol (Architect)**". S3 `README.md` line 389: "**Architect / Custodian:**". `arc/README.md` uses the same solidus form for two bodies. |
| **Evidence contradicting or limiting it** | **No document states the equation.** `SPEC_TEMPLATE.md` is internally inconsistent — line 9 offers both, line 32 names only the Custodian. The Constitution never uses "Protocol Custodian"; POL-VER-001 never uses it; GOV-001 never uses it. Conversely S3's three Custodian-defining documents never use "Chief Architect". The solidus notation is **defined nowhere** (**A-3**). Every S3 Custodian grant is **instrument-scoped** while every S1 Chief Architect grant is **document-scoped** — a scope disjunction that the equation would have to override without textual warrant. |
| **Unresolved dependencies** | A-2 (four readings, none stated) · A-3 (what the solidus means) · M-12 (cross-repository authority) · M-14 (person or office) · C-8 (which hierarchy governs) |

---

### Model V — Instrument-Custodian *(scope-limited; presented for completeness)*

| Field | Content |
|---|---|
| **Authority role/body** | Custodian of the Protocol · AI Copilot · Users/Contributors |
| **Scope** | Constitutional constants; `core/`; layer boundaries; cryptographic primitives; sealing and archival; emergency halt; succession (X-17…X-20) |
| **Evidence supporting existence** | S3 `CONSTITUTIONAL_DECREE.md` Art. V (Status: MANDATORY / NON-OVERRIDABLE); `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` (Status: CANONICAL); `docs/ops/PROTOCOL_CUSTODIAN.md` (Status: CANONICAL / BINDING); `.github/copilot-instructions.md`; `AGENTS.md` Authority Precedence. **The most fully specified authority model in any repository** — it alone defines succession, override, emergency powers and selection criteria. |
| **Evidence contradicting or limiting it** | **It does not reach the artifact classes in question.** Every enumerated power concerns the measurement instrument; none addresses SPEC, ADR, RFC, ARC or APS documents. Its authority derives from `CONSTITUTIONAL_DECREE` Art. V — a document in S3 that the AURA Constitution does not contemplate (**C-8**). `copilot-instructions.md` extends it to "all canonical definitions", broader than the three CANONICAL documents allow, and is agent-instruction text rather than governance. Whether an S3 role has standing in S1 is undefined (**M-12**). |
| **Unresolved dependencies** | M-12 (cross-repository standing) · C-8 (which hierarchy is top) · A-2 (relation to Chief Architect) · whether instrument scope can be extended to specification artifacts, and by what instrument |

---

### 7.1 Non-selection statement

The five models are **not** ranked, scored, or compared for suitability. Model V is included
because the corpus contains it, and its inclusion is not a suggestion that instrument-scoped
authority should be extended. Model III is the only model supplying a SPEC approver; that is a
recorded property of the corpus, **not an argument in its favour** — the same model carries the
circularity in §6.1 Route 3 and three unconstituted bodies. **No model is recommended.**

---

## 8. Minimum Governance Decision

The smallest decision that unblocks DR-002. **This brief does not make it.**

### 8.1 The minimum decision

> **Designate, for each of the artifact classes SPEC, ADR and RFC, the role or body that holds
> approval authority; and specify the recorded act by which that approval is exercised.**

### 8.2 Why nothing smaller suffices

| Reduction considered | Why it does not suffice |
|---|---|
| Decide only for SPEC | ADR acceptance is actorless (**C-2**), and AD-CA decisions are carried by ADRs into SPEC-002. Deciding SPEC alone leaves the upstream approval undemonstrable. |
| Decide only the role, not the act | GOV-001 §6 binds acceptance to **merging**; `ADR_TEMPLATE.md` has **no approver field**; the two `ADR-001` copies specify different field names (**C-7**). A role without a recorded act produces approvals that cannot be verified after the fact. |
| Resolve A-2 alone (are the two roles one office?) | Answering A-2 does not close **C-2** (no ADR actor), **M-3** (unconstituted bodies), or **M-2** (undefined Architecture Review). It removes one ambiguity, not the gap. |
| Adopt an existing model wholesale | Each model carries unresolved dependencies (§7). Adoption without addressing them relocates the gap rather than closing it. |
| Constitute the ARB alone | Closes §6.3's executability defect for RFC, but leaves SPEC and ADR approval unassigned. |

### 8.3 What the minimum decision necessarily entails

Each item below is a **component** of the decision in §8.1, not an addition to it. Listed so
the decision's true extent is visible before it is taken.

| # | Entailed component | Forced by |
|---|---|---|
| 8.3.1 | Whether GOV-001 §2's four-item list is **exhaustive** or illustrative | A-1; §6.1 Route 1 |
| 8.3.2 | Whether SPEC-002 is a **"governance artifact"** under POL-VER-001 §3 and a **"canonical document"** under Constitution Art. VIII | A-5, A-9, M-11 |
| 8.3.3 | Whether "Chief Architect" and "Protocol Custodian" name one office | A-2; C-1 |
| 8.3.4 | Who may **merge**, given that acceptance is bound to merging | C-2, M-4 |
| 8.3.5 | Whether **ARB and Architecture Board** are one body, and whether either is constituted | C-3, M-3 |
| 8.3.6 | How the **circularity** in §6.1 Route 3 is broken | §6.1; Model III |
| 8.3.7 | Whether **"owner"** (SPEC-002's only authority statement) confers approval | A-7, M-1 |

### 8.4 Procedural question — recorded, not answered

Which process may legitimately **produce** this decision is itself undetermined. Constitution
Art. XI supplies the only approval path of FROZEN rank, ending in "Approval by the Chief
Architect" (X-1), but requires an Architecture Review (Art. XI(2)) that is undefined (**M-2**)
and conducted by a contested, unconstituted body (**A-4**, **M-3**). GOV-001 §11 permits its own
amendment via the §5.2 Major Change process, which requires the **same** unconstituted ARB.

**Whether DR-002 is a Constitution-amendment matter, a GOV-001-amendment matter, or resolvable
by a lower instrument is part of the decision and is not answered here.**

---

## 9. Downstream Impact

| AD-CA | Subject *(SPEC-002 §6)* | BLOCKED BY DR-002 | Reason |
|---|---|---|---|
| **AD-CA-001** | Authoritative source identity, Source Set, Source Boundary | **YES** | Carried by ADR-002 into SPEC-002. Both carriers lack an identified approver (§6.1, §6.2). |
| **AD-CA-002** | Source canonicalization | **YES** | Same carriers, same gap. |
| **AD-CA-003** | Transformation pipeline | **YES** | Carried by ADR-003 into SPEC-002. Same gap. |
| **AD-CA-004** | Normalization rules | **YES** | Same gap, **and no carrier artifact is assigned** — assignment is itself an approval act with no identified approver (M-4). |
| **AD-CA-005** | Embedding method identity and versioning | **YES** | Same gap. Scope is additionally disputed (DR-008), and resolving a scope dispute is an approval act. |
| **AD-CA-006** | Dictionary identity and dependency closure | **YES** | Same gap, **and no carrier artifact is assigned** (as AD-CA-004). |
| **AD-CA-007** | Numeric representation | **YES** | Carried by ADR-004 into SPEC-002. Same gap. Note the substantive content is fully specifiable today; only its **approval** is blocked. |
| **AD-CA-008** | Canonical serialization, byte sequence, hash domains | **YES** | Same gap. Additionally requires an APS-200 §8 amendment, and APS authority is contested (**C-4**). |
| **AD-CA-009** | Identity model | **YES** | Same gap. Additionally requires an APS-200 §4 amendment; APS status authority contested (**C-4**). |
| **AD-CA-010** | Provenance boundary | **YES** | Same gap; same APS-200 dependency and contest (**C-4**). |
| **AD-CA-011** | Registration model and registry | **YES** | Same gap. A registry requires an authority to maintain it; **M-3** leaves candidate custodial bodies unconstituted. |
| **AD-CA-012** | Freeze lifecycle | **YES** | Same gap. Freeze authority is directly contested between POL-VER-001 §3 and the PROPOSED model (**C-5**). |

**Result: 12 of 12 BLOCKED.**

### 9.1 Nature of the blockage

The blockage is **uniform and procedural, not substantive**. It attaches to the approval step
common to all twelve domains, not to the technical content of any of them. Two consequences
follow, and both are recorded as facts rather than as advice:

1. **Analytical work on any AD-CA domain may proceed** — drafting, evidence gathering, option
   development — because none of that requires approval authority. What cannot proceed is
   **closure**.
2. **Resolving DR-002 does not by itself close any AD-CA domain.** It removes the common
   obstacle; each domain still requires its own decision on its own merits.

---

## 10. Decision Acceptance Test

Objective evidence that would make **DR-002 CLOSED**. The test is stated so that its outcome
does not depend on who applies it.

### 10.1 Test conditions

**T-1 — Independent determinability.** A reviewer with access only to repository documents, and
without asking any person, can complete every cell of the matrix in §10.2 by citation to a
document, section and quoted text.

**T-2 — In-force sources only.** Every citation resolves to a document whose status is
APPROVED or FROZEN, or to a DRAFT document explicitly designated as governing by an APPROVED or
FROZEN document. **No cell may rest on a PROPOSED or unindexed source.**

**T-3 — Non-circularity.** No cited grant depends for its own validity on the authority it
grants. *(Directly excludes the §6.1 Route 3 pattern.)*

**T-4 — Named bodies are constituted.** Every body appearing in any cell has, in a cited
document: a definition, a membership or appointment method, and a decision rule (quorum or
equivalent). *(Closes M-3, M-9.)*

**T-5 — Recorded act.** For each "approves", "merges" and "freezes" cell, the citation specifies
the artifact-level record — field name, location and form — by which the act is evidenced, and
that field exists in the applicable template. *(Closes M-4, C-7.)*

**T-6 — Single-valued.** No cell has two conflicting citations. Where two documents address the
same cell, one cites the other as superseded, out of scope, or subordinate. *(Closes C-1…C-8.)*

**T-7 — Terminological closure.** Every role string used in any cell is defined once and used
consistently; every string in the corpus not used is explicitly retired or mapped.
*(Closes M-7, M-8, M-11, M-14, A-2, A-3.)*

### 10.2 The determinability matrix

Eighteen cells. **All eighteen must be completable under T-1 … T-7.**

| Function | SPEC | ADR | RFC |
|---|---|---|---|
| **Who may propose** | ☐ | ☐ | ☐ |
| **Who reviews** | ☐ | ☐ | ☐ |
| **Who approves** | ☐ | ☐ | ☐ |
| **Who may merge** | ☐ | ☐ | ☐ |
| **Who freezes** | ☐ | ☐ | ☐ |
| **Who resolves conflicts** | ☐ | ☐ | ☐ |

### 10.3 Current completion state

Assessed against T-1 … T-7 using the evidence in §2:

| Function | SPEC | ADR | RFC |
|---|---|---|---|
| Who may propose | **☐** — no SPEC authoring role defined; GOV-001 §2 "Specification Contributors" is undefined (M-7) | **☐** — `ADR_TEMPLATE.md` has an `Author` field; no eligibility rule | **☐** — `rfcs/README.md` implies any contributor; no eligibility rule |
| Who reviews | **☐** — Architecture Review undefined (M-2); body contested (A-4) and unconstituted (M-3) | **☐** — GOV-001 §6 specifies no review step | **☐** — ARB named (X-7/X-8) but **fails T-4** |
| Who approves | **☐** — **fails T-2** (only X-13, PROPOSED) and **T-3** (circular) | **☐** — **fails T-1** (no actor named, C-2) and **T-6** (C-7) | **◐** — X-6 names the Chief Architect and passes T-1/T-2, but the path **fails T-4** at the ARB step (§6.3) |
| Who may merge | **☐** — no grant | **☐** — acceptance bound to merging; merge authority granted only for PATCH (X-10) — **fails T-1** | **☐** — "Do not merge your own RFC" states a restriction, not an authority |
| Who freezes | **☐** — **fails T-6**: POL-VER-001 §3 vs PROPOSED model (C-5) | **☐** — ADR lifecycle has no freeze state in `ADR_TEMPLATE.md` | **☐** — RFC lifecycle terminates at ACCEPTED/REJECTED; no freeze defined |
| Who resolves conflicts | **☐** — GOV-001 §10 orders **principles**, not authorities | **☐** — same | **☐** — same |

**Legend:** ☐ not determinable · ◐ partially determinable.

**Score: 0 of 18 cells fully determinable. 1 of 18 partially determinable.**

### 10.4 Closure condition

> **DR-002 may be marked CLOSED when, and only when, all eighteen cells of §10.2 are completable
> by citation under T-1 through T-7, and an independent reviewer applying the test reaches the
> same eighteen answers.**

Partial completion does not close DR-002, but it changes the blockage profile: completing the
**"who approves"** row alone for SPEC and ADR would lift the uniform block on AD-CA-001…012 in
§9, while leaving DR-002 open for the remaining functions. That relationship is recorded as a
property of the dependency structure; **whether to proceed on a partial basis is itself a
governance decision and is not proposed here.**

---

## 11. Stop Condition

| Measure | Value |
|---|---|
| Distinct role/body strings in the corpus | 9 |
| Role grants of FROZEN rank | 3 (all naming Chief Architect or "AI systems") |
| In-force grants of **SPEC approval** authority | **0** |
| In-force grants of **ADR acceptance** authority | **0** |
| In-force grants of **RFC approval** authority | 1 (X-6) — prerequisite step not executable |
| In-force definitions of **Architecture Review** | **0** |
| Bodies referenced but never constituted | 4 |
| Direct contradictions | 8 (C-1 … C-8) |
| Ambiguities | 9 (A-1 … A-9) |
| Missing definitions | 14 (M-1 … M-14) |
| Candidate models present in repository terminology | 5 (none selected) |
| Acceptance-test cells fully determinable | **0 of 18** |
| AD-CA domains blocked | **12 of 12** |

**No normative effect. No governance change. No implementation. No decision made. No role
recommended.**

---

**DR-002 STATUS: UNRESOLVED**
