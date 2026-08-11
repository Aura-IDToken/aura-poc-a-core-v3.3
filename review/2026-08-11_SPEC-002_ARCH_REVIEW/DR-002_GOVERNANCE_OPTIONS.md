# DR-002 — GOVERNANCE OPTIONS

**Decision-support package for the governance authority model**

| Field | Value |
|---|---|
| Document ID | DR-002_GOVERNANCE_OPTIONS |
| Version | 1.0-DRAFT |
| Status | DRAFT — DECISION SUPPORT ONLY |
| Date | 2026-08-11 |
| Evidence base | `DR-002_EVIDENCE_PACKAGE.md` (`ed590e6`) · `DR-002_DECISION_BRIEF.md` (`b68461c`) · sources cited therein |
| Normative effect | **NONE** |

---

> **THIS PACKAGE MAKES NO DECISION AND SELECTS NO MODEL.**
>
> It does not recommend, rank, score, prefer, or imply the correctness of any role or body. It
> creates and modifies no governance document. GOV-001, the AURA Constitution and SPEC-002 are
> untouched. No ADR is created. No pull request is opened. No code is implemented.
>
> Candidate models in §5 are presented **because the repository's own terminology contains
> them**. Their order is by document rank of their primary source, which is a property of the
> corpus and **not** an ordering by merit. §6 is deliberately unordered and unscored: it reports
> per-cell status, and no cell count, tally, or aggregate is provided, because any such
> aggregate would function as a ranking.

**Exclusions.** Authority is not inferred from repository ownership, GitHub permissions,
CODEOWNERS mappings, commit authorship, implementation behaviour, job titles, or prior
conversation. Identifiers `X-n` / `C-n` / `A-n` / `M-n` refer to `DR-002_EVIDENCE_PACKAGE.md`.

---

## 1. Decision Question

> **What governance authority model should formally govern SPEC approval, ADR approval, RFC
> approval, Architecture Review, merge/acceptance, freeze, and conflict resolution?**

### 1.1 The seven governed functions

| # | Function | Currently established? |
|---|---|---|
| F-1 | **SPEC approval** — moving a SPEC-class document to a state carrying normative effect | **No** |
| F-2 | **ADR approval** — accepting an ADR that resolves an architectural decision | **No** |
| F-3 | **RFC approval** — accepting or rejecting an RFC | **Approver named; path not executable** |
| F-4 | **Architecture Review** — the review act required by Constitution Art. XI(2) and by every major-change path | **No** |
| F-5 | **Merge / acceptance** — the act by which approval is recorded | **No, except PATCH** |
| F-6 | **Freeze** — conferring immutable status | **For APS only; contested for SPEC** |
| F-7 | **Conflict resolution** — deciding between contradictory sources | **Criteria exist; no authority named** |

### 1.2 Why this is antecedent to all AD-CA work

SPEC-002 §9 criterion 1 requires every requirement to be backed by an approved normative source
or an approved architecture decision. An approval not attributable to an authorised approver is
not demonstrable as an approval. F-1 and F-2 therefore gate closure of all twelve AD-CA domains.

---

## 2. Current Evidence

Summary only; full inventory in `DR-002_EVIDENCE_PACKAGE.md` §2.

| Measure | Value |
|---|---|
| Distinct role/body strings in the corpus | **9** — Chief Architect · Protocol Custodian · Custodian of the Protocol · Architecture Review Board (ARB) · Architecture Board · Release Authority · Compliance Authority / Auditor · Documentation Architect · Chief Specification Architect |
| Role grants of **FROZEN** rank | **3** (X-1, X-2, X-3) — all naming Chief Architect or "AI systems" |
| Role grants from **DRAFT** sources | 9 (X-4 … X-12) |
| Role grants from **PROPOSED** sources | 4 (X-13 … X-16) |
| Role grants scoped to the **implementation instrument** | 4 (X-17 … X-20) |
| Bodies referenced but **never constituted** | **4** — ARB · Architecture Board · Release Authority · Compliance Authority |
| Direct contradictions | 8 (C-1 … C-8) |
| Ambiguities | 9 (A-1 … A-9) |
| Missing definitions | 14 (M-1 … M-14) |
| Documents in the corpus that name at least one role | 21 |

### 2.1 A structural fact bearing on every candidate

**Every amendment path in the corpus routes through a step that cannot currently be performed.**

| Instrument | Its own amendment clause | Blocking step |
|---|---|---|
| AURA Constitution | Art. XI: RFC → **Architecture Review** → impact analysis → dependent updates → Chief Architect approval | Architecture Review is undefined (**M-2**); conducting body contested (**A-4**) and unconstituted (**M-3**) |
| GOV-001 | §11: "amended via the **Major Change process (§5.2)**" | §5.2(4) requires **ARB assessment**; ARB unconstituted (**M-3**) |
| POL-VER-001 | §10: RFC per CONTRIBUTING.md + **Chief Architect approval** | CONTRIBUTING.md routes RFCs through **Architecture Review** (M-2) |

This is recorded as a fact about the corpus, not as an argument for or against any candidate.
It bears on §7 for **all five** models: the governance change each would require is itself
gated by the same unconstituted or undefined step. §7.6 records the consequence.

---

## 3. Existing Authority Assignments

Explicit grants only — a named role plus a named act. No inference.

### 3.1 FROZEN rank — `AURA-CON-001 v1.0`

| # | Grant | Section | Scope as written |
|---|---|---|---|
| **X-1** | Chief Architect approves Constitution amendments | Art. XI(5) | Constitution only |
| **X-2** | Chief Architect is "responsible for the project" | Art. VIII | Unbounded; unenumerated |
| **X-3** | AI systems MUST NOT approve canonical documents or modify frozen documents | Art. VIII | Prohibition |

### 3.2 DRAFT rank — `GOV-001 1.0-DRAFT`, `POL-VER-001 1.0-DRAFT`

| # | Grant | Section | Scope as written |
|---|---|---|---|
| **X-4** | Chief Architect: "final and sole approval authority" over Constitution amendments · APS APPROVED→FROZEN · Invariant additions/removals · new RI recognition | GOV-001 §2 | **Closed four-item list** |
| **X-5** | Chief Architect approves at step 5 of Major Change | GOV-001 §5.2 | RFC-bearing changes |
| **X-6** | Chief Architect gives final approval of RFCs | GOV-001 §7(8) | RFC class |
| **X-7** | ARB votes ACCEPT / REJECT / DEFER on RFCs | GOV-001 §7(7) | RFC class |
| **X-8** | ARB performs "assessment" in Major Changes | GOV-001 §5.2(4) | character unspecified |
| **X-9** | Chief Architect chairs review meetings producing ARRs | GOV-001 §8 | ARR production |
| **X-10** | Chief Architect **or delegate** may merge | GOV-001 §5.1 | **PATCH only** |
| **X-11** | Chief Architect approves REVIEW→APPROVED and APPROVED→FROZEN | POL-VER-001 §3 | "every APS document and governance artifact" |
| **X-12** | Chief Architect approves changes to the versioning policy | POL-VER-001 §10 | POL-VER-001 |

### 3.3 PROPOSED rank — `ADR-001_DOCUMENT_MODEL` *(not in force)*

| # | Grant | Scope as written |
|---|---|---|
| **X-13** | Protocol Custodian approves SPECs; owns SPEC lifecycle; signatory for normative acceptance | SPEC class |
| **X-14** | Architecture Board approves ARC baselines **and ADRs** | ARC, ADR |
| **X-15** | Release Authority publishes APS | APS class |
| **X-16** | Compliance Authority / Auditor owns traceability and evidence retention | compliance |

### 3.4 Implementation-instrument scope — `S3`

| # | Grant | Scope as written |
|---|---|---|
| **X-17** | Protocol Custodian: SOLE AUTHORITY to seal, archive, declare permanently frozen | the instrument |
| **X-18** | Protocol Custodian: FINAL AUTHORITY over `core/`, constants, layer boundaries, crypto | the instrument |
| **X-19** | Protocol Custodian: ABSOLUTE OVERRIDE AUTHORITY | the instrument |
| **X-20** | Custodian of the Protocol may modify constants, authorize tasks, seal and archive | the instrument |
| **X-21** | Custodian MUST review every PR touching `core/`, constants, layer boundaries, crypto primitives, regulatory compliance mechanisms | the instrument |

---

## 4. Authority Gaps

Per function. Mechanism of failure stated; no remedy proposed.

**F-1 SPEC approval — NOT ESTABLISHED.** Three routes exist, all failing differently.
*Route 1* GOV-001 §2 (X-4): worded "final and **sole**" over four enumerated items; SPEC is not
among them and cannot be, since GOV-001 has no SPEC artifact class — §3's table lists ADR, ARR,
RFC, ADC, ACI, EPR with no SPEC row. Fails by **omission**.
*Route 2* POL-VER-001 §3 (X-11): grants REVIEW→APPROVED for "every APS document and governance
artifact"; whether SPEC-002 is a "governance artifact" is **A-9** — §1's scope enumeration does
not name SPEC. Fails on **unresolved classification**.
*Route 3* `ADR-001_DOCUMENT_MODEL` (X-13): the only text granting SPEC approval to anyone.
Status **PROPOSED**; it states it "requires explicit approval by the Protocol Custodian" — the
role it constitutes. Fails on **circularity**.

**F-2 ADR approval — NOT ESTABLISHED.** GOV-001 §6(6–7) makes acceptance a consequence of an
act, not a decision by a person: "Merging the PR = accepting the ADR"; "ADR status set to
ACCEPTED". No actor at either step. `adrs/README.md` repeats it. The only merge grant (X-10) is
scoped to **PATCH**, which AD-CA decisions are not. Compounded by: X-14 exists only in the
PROPOSED source and names an unconstituted body (**M-3**); `ADR_TEMPLATE.md` has **no approver,
owner or acceptance field**; and the two `ADR-001` copies specify different approver counts and
different field names (**C-7**).

**F-3 RFC approval — NAMED BUT NOT EXECUTABLE.** Stated separately to avoid overstating the
gap. An approver **is** explicitly named: GOV-001 §7(8) (X-6) and `RFC_TEMPLATE.md` line 105
`Decided by: Chief Architect`. But §7(7) places immediately before it "**ARB votes: ACCEPT /
REJECT / DEFER**", and §5.2(4) requires "ARB assessment". Per **M-3** the ARB is not defined,
constituted, or given membership, quorum or appointment method anywhere, and no document states
it exists. A process whose penultimate step requires a vote by an unconstituted body cannot be
executed as written. Secondary: the ARB act is named four ways (**A-8**) with binding-vs-advisory
character unstated; CONTRIBUTING.md's APS and Invariant rows terminate at "PR" with no approver,
contradicting GOV-001 §2 (**C-6**).

**F-4 Architecture Review — NOT ESTABLISHED.** A precondition of FROZEN-rank action
(Constitution Art. XI(2)), and required by CONTRIBUTING.md, POL-VER-001 §3 and GOV-001 §5.2.
Nothing defines what constitutes one, who convenes it, quorum, or output validity (**M-2**).
Conducting body ambiguous between Chief Architect (GOV-001 §8 "chaired by") and ARB (§2
"conducts ARRs") — **A-4** — and the ARB is unconstituted (**M-3**). GOV-001 §8 requires an ARR
be published to `/adrs/ARR-NNN_TITLE.md` within 5 days; **no ARR exists in the repository.**

**F-5 Merge / acceptance — NOT ESTABLISHED except for PATCH.** X-10 is the corpus's only merge
grant and is PATCH-scoped; "delegate" is undefined (**M-6**). Because GOV-001 §6 binds ADR
acceptance to merging, the merge gap propagates directly into F-2. `rfcs/README.md` states "Do
not merge your own RFC" — a restriction, not an authority.

**F-6 Freeze — ESTABLISHED FOR APS ONLY; CONTESTED FOR SPEC.** X-4 explicitly covers "APS
document status transitions (APPROVED → FROZEN)"; X-11 covers "every APS document and governance
artifact" and additionally requires Constitution Art. XI procedure. `ADR-001_DOCUMENT_MODEL`
line 29 assigns SPEC freeze to the Protocol Custodian with no Art. XI reference — **C-5**. For
ADR and RFC classes no freeze state exists in their templates or lifecycles at all.

**F-7 Conflict resolution — CRITERIA WITHOUT AUTHORITY.** Constitution Art. XII and GOV-001 §10
both supply an ordered precedence — mission · constitutional principles · protocol conformance ·
determinism · auditability. Both order **principles**, not **authorities**. Neither names who
applies the ordering, nor whose application binds. `AGENTS.md`/`CLAUDE.md` instruct agents to
"report the conflict; request human/Protocol Custodian resolution" — agent instruction text, not
a governance grant, and it names a role the specification corpus does not use.

---

## 5. Candidate Governance Models

Assembled **only** from role strings and authority statements already present in the
repositories. None is invented; none is recommended. Ordered by document rank of primary source.

---

### Model I — Constitutional Minimal

**Authority structure.** Chief Architect as sole named role; "AI systems" as a constrained
category. No boards, no committees, no delegated bodies.

| Function | Position under this model |
|---|---|
| **SPEC authority** | **None granted.** Constitution Art. V hierarchy contains no SPEC class (E-2.1.6), so the Constitution assigns no authority over SPEC because it does not contemplate SPEC. |
| **ADR authority** | Unenumerated. ADR appears in the Art. V hierarchy and in the Art. VI artifact table, which requires each artifact have an "owner" but names none (**M-1**). Whether Art. VIII's general grant reaches ADR acceptance is **A-1**. |
| **RFC authority** | Unenumerated. Art. XI(1) requires an RFC for Constitution amendment but assigns no RFC approver. |
| **ARB role** | **None.** The Constitution names no board or committee anywhere. |
| **Merge authority** | **None.** The Constitution does not address merging. |
| **Freeze authority** | Art. XI: "Once a version is marked FROZEN, its content is immutable." Art. VIII prohibits AI from modifying frozen documents — presupposing freeze without assigning the conferring authority. |
| **Conflict resolution** | Art. XII supplies an ordered precedence of principles. No authority is named to apply it. |
| **Evidence supporting** | `AURA-CON-001 v1.0` **FROZEN** — Art. VIII, Art. XI(5), Art. XII. The **only** role grants of FROZEN rank in the corpus. Independently reinforced by `CODE_OF_CONDUCT.md`, `README.md` §Governance, `constitution/README.md`, `ROADMAP.md`, `SECURITY.md`, `RFC_TEMPLATE.md`, `CONFORMANCE_REPORT_TEMPLATE.md`. |
| **Evidence contradicting** | Art. VIII is unenumerated — it never states which artifact classes it reaches (**A-1**). No SPEC class exists in Art. V. "Canonical document", the class on which X-3 turns, is undefined (**A-5**, **M-11**). Art. VI requires an owner per artifact and names none (**M-1**). |
| **Unresolved dependencies** | A-1 · A-5 / M-11 · M-2 (Architecture Review) · M-10 (how the office is filled) · M-14 (person or body) · M-1 |

---

### Model II — GOV-001 Four-Tier

**Authority structure.** Chief Architect · Architecture Review Board (ARB) · Specification
Contributors · AI Assistants.

| Function | Position under this model |
|---|---|
| **SPEC authority** | **None granted.** §2's list is closed and excludes SPEC; §3's artifact table has no SPEC row. |
| **ADR authority** | §6: "Merging the PR = accepting the ADR" — **no actor named**. §5.2(5) places Chief Architect approval upstream of ADR creation. The two accounts differ (**C-2**). |
| **RFC authority** | §7(8): Chief Architect final approval (X-6), preceded by §7(7) ARB vote (X-7). |
| **ARB role** | Named with four functions — conducts ARRs (§2), assesses (§5.2), votes (§7), REVIEW (`rfcs/README.md`). **Not defined, constituted, or given membership, quorum or appointment method** (**M-3**). Binding-vs-advisory character unstated (**A-8**). |
| **Merge authority** | §5.1: Chief Architect or delegate — **PATCH only**. "Delegate" undefined (**M-6**). |
| **Freeze authority** | §2: Chief Architect, "final and sole", over APS APPROVED→FROZEN. Reinforced by POL-VER-001 §3 (X-11). |
| **Conflict resolution** | §10 supplies an ordered precedence of principles, not authorities. |
| **Evidence supporting** | `GOV-001` §2 authority tree; §3 artifact-owner table; §5.1, §5.2, §6, §7, §8, §9. ARB reinforced by `rfcs/README.md` lifecycle. Aligned with POL-VER-001 §3/§10 and with CONTRIBUTING.md's Constitution row. |
| **Evidence contradicting** | GOV-001 is `1.0-DRAFT`. §2's list excludes SPEC, ADR and RFC acceptance. §6 is actorless (**C-2**). ARB unconstituted (**M-3**) — so X-7/X-8 cannot be exercised, and §11's own amendment path is thereby blocked. §2's tree renders the FROZEN Constitution as a child node of the Chief Architect (**A-6**). "Delegate" (**M-6**) and "Specification Contributors" (**M-7**) undefined. CONTRIBUTING.md contradicts §2 on Invariants (**C-6**). |
| **Unresolved dependencies** | M-3 · M-4 · A-8 · A-9 · A-6 · A-1 · C-6 |

---

### Model III — Document-Model Four-Body

**Authority structure.** Protocol Custodian · Architecture Board · Release Authority ·
Compliance Authority / Auditor.

| Function | Position under this model |
|---|---|
| **SPEC authority** | Protocol Custodian "approves SPECs, is owner of SPEC lifecycle, and is signatory for normative acceptance" (X-13). **The only text in any repository granting SPEC approval authority.** |
| **ADR authority** | Architecture Board "approves and owns ARC baselines and ADRs related to architecture decisions" (X-14). |
| **RFC authority** | **None granted.** The lifecycle places RFC at step 2 but assigns no RFC approver. |
| **ARB role** | The model names an "**Architecture Board**", not the ARB. Never equated (**C-3**). Unconstituted (**M-3**). |
| **Merge authority** | Implied only: approval "recorded by adding an `Accepted-by:` line **and merging** this ADR into the canonical branch". No merge authority is granted to anyone. The divergent copy uses `accepted_by` and requires **two** approvals (**C-7**). |
| **Freeze authority** | "A SPEC becomes frozen only after explicit approval by the Protocol Custodian" — no Constitution Art. XI reference, contradicting POL-VER-001 §3 (**C-5**). |
| **Conflict resolution** | **Not addressed.** |
| **Evidence supporting** | `adrs/ADR-001_DOCUMENT_MODEL.md` "Owners and Authorities" and "Lifecycle Summary"; divergent copy at `docs/adr/001-document-model.md`. Reinforced by `SPEC_TEMPLATE.md` line 32, `arc/README.md` line 10, and SPEC-002's front matter `Owner: Protocol Custodian`. |
| **Evidence contradicting** | Status **PROPOSED**; second copy **DRAFT** — neither in force. **Circular**: requires approval by the role it constitutes (§4 F-1 Route 3). Its own Open Questions record thresholds, quorum and signature format as undefined (**M-9**). Two copies disagree on approver count and field name (**C-7**); both carry an identifier already held by an ACCEPTED document. Architecture Board, Release Authority and Compliance Authority all unconstituted (**M-3**). Conflicts with GOV-001 §2 on APS authority (**C-4**) and POL-VER-001 §3 on freeze (**C-5**). Depends on an ARC layer that is empty (`arc/` README-only; `arc_to_spec_mapping.yaml` = `mappings: []`; SPEC-001 does not exist). |
| **Unresolved dependencies** | The circularity · C-7 · M-3 (three bodies) · M-9 · C-3 · C-4 · C-5 · DR-003 (which document model governs) · the empty ARC layer |

---

### Model IV — Interchangeable-Title

**Authority structure.** A single office denoted by either "Protocol Custodian" or "Chief
Architect", holding the union of Model I–III grants.

| Function | Position under this model |
|---|---|
| **SPEC authority** | Under the equation, X-11 and X-13 converge on one office and **C-1 dissolves**. The equation itself is stated by no document. |
| **ADR authority** | **C-2 persists** — the actorless merge=accept formula is unaffected by equating two individual roles. |
| **RFC authority** | X-6 unaffected; the ARB executability defect (F-3) persists. |
| **ARB role** | **C-3 persists** — ARB vs Architecture Board is a question about *bodies*, not resolved by equating two *individual* roles. |
| **Merge authority** | Unchanged: PATCH-only grant (X-10); M-4 persists. |
| **Freeze authority** | The role conflict in C-5 dissolves; the **procedural** difference remains — POL-VER-001 requires Constitution Art. XI procedure, the document model does not. |
| **Conflict resolution** | Not addressed by any source under this reading. |
| **Evidence supporting** | `SPEC_TEMPLATE.md` line 9: `Owner: Role / Name (Protocol Custodian / Chief Architect)` — presented as interchangeable options. S3 `CONSTITUTIONAL_DECREE` Art. V: "Custodian of the Protocol **(Architect)**". S3 `README.md` line 389: "Architect / Custodian:". `arc/README.md` uses the same solidus for two bodies. |
| **Evidence contradicting** | **No document states the equation.** `SPEC_TEMPLATE.md` is internally inconsistent — line 9 offers both, line 32 names only the Custodian. The Constitution, POL-VER-001 and GOV-001 never use "Protocol Custodian"; S3's three Custodian-defining documents never use "Chief Architect". The solidus is defined nowhere (**A-3**). Every S3 Custodian grant is instrument-scoped while every S1 Chief Architect grant is document-scoped — a scope disjunction the equation would override without textual warrant. |
| **Unresolved dependencies** | A-2 (four readings, none stated) · A-3 · M-12 (cross-repository authority) · M-14 · C-8 · and every dependency of Models I–III that the equation does not dissolve |

---

### Model V — Instrument-Custodian *(scope-limited; presented for completeness)*

**Authority structure.** Custodian of the Protocol · AI Copilot · Users/Contributors.

| Function | Position under this model |
|---|---|
| **SPEC authority** | **Out of scope.** No S3 document addresses SPEC. |
| **ADR authority** | **Out of scope.** |
| **RFC authority** | **Out of scope.** |
| **ARB role** | **None.** No board exists in the S3 model. |
| **Merge authority** | X-21: "The Custodian MUST review every pull request that touches `/core/`, constitutional constants, layer boundaries, cryptographic primitives, regulatory compliance mechanisms." A **review** obligation over instrument code — not a merge grant over specification artifacts. |
| **Freeze authority** | X-17: SOLE AUTHORITY to declare the instrument ready for sealing, compute the final checksum, archive, certify, and declare permanently frozen. **The most explicit freeze grant in any repository** — instrument-scoped. |
| **Conflict resolution** | X-19: ABSOLUTE OVERRIDE AUTHORITY. Decree Art. V: "When Authority Conflicts Arise — The Constitution prevails." |
| **Evidence supporting** | S3 `CONSTITUTIONAL_DECREE.md` Art. V (MANDATORY / NON-OVERRIDABLE); `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` (CANONICAL); `docs/ops/PROTOCOL_CUSTODIAN.md` (CANONICAL / BINDING); `.github/copilot-instructions.md`; `AGENTS.md` Authority Precedence. **The most fully specified authority model in any repository** — it alone defines succession, override, emergency powers and selection criteria. |
| **Evidence contradicting** | **It does not reach the artifact classes in question.** Every enumerated power concerns the measurement instrument. Its authority derives from `CONSTITUTIONAL_DECREE` Art. V — an S3 document the AURA Constitution does not contemplate (**C-8**). `copilot-instructions.md` extends it to "all canonical definitions", broader than the three CANONICAL documents allow, and is agent-instruction text rather than governance. Whether an S3 role has standing in S1 is undefined (**M-12**). |
| **Unresolved dependencies** | M-12 · C-8 · A-2 · whether instrument scope can be extended to specification artifacts, and by what instrument |

---

### 5.1 Non-selection statement

The five models are **not** ranked, scored, or compared for suitability. Model III is the only
model supplying a SPEC approver; that is a **recorded property of the corpus**, not an argument
in its favour — the same model carries the circularity in §4 F-1 Route 3, three unconstituted
bodies, and a dependency on an empty ARC layer. Model V is the most fully specified authority
model in the corpus; that is likewise a recorded property, and its inclusion is **not** a
suggestion that instrument-scoped authority should be extended. **No model is recommended.**

---

## 6. Comparison Matrix

### 6.1 Value definitions

| Value | Meaning |
|---|---|
| **EXPLICIT** | The model's own sources name both a role/body and an act, and no equal-or-higher-rank source contradicts the assignment. |
| **PARTIAL** | A role/body is named, but the assignment is incomplete: no recorded act, no stated scope, unstated character (binding vs advisory), or the named body is not constituted. |
| **ABSENT** | The model's sources are silent on this function. |
| **CONTRADICTED** | The model asserts an assignment **and** an equal-or-higher-rank source assigns it otherwise. Strictly more informative than ABSENT: an assignment exists but is contested. |
| **UNKNOWN** | Cannot be determined from the model's sources without resolving a prior ambiguity. |

### 6.2 Matrix

| Model | SPEC | ADR | RFC | ARB | Merge | Freeze | Conflict |
|---|---|---|---|---|---|---|---|
| **I — Constitutional Minimal** | ABSENT | PARTIAL | PARTIAL | ABSENT | ABSENT | PARTIAL | PARTIAL |
| **II — GOV-001 Four-Tier** | ABSENT | CONTRADICTED | EXPLICIT | PARTIAL | PARTIAL | EXPLICIT | PARTIAL |
| **III — Document-Model Four-Body** | CONTRADICTED | EXPLICIT | ABSENT | CONTRADICTED | PARTIAL | CONTRADICTED | ABSENT |
| **IV — Interchangeable-Title** | PARTIAL | CONTRADICTED | EXPLICIT | CONTRADICTED | PARTIAL | PARTIAL | UNKNOWN |
| **V — Instrument-Custodian** | ABSENT | ABSENT | ABSENT | ABSENT | PARTIAL | EXPLICIT | EXPLICIT |

### 6.3 Cell notes

Only cells whose value depends on a specific determination are annotated. No totals, counts or
aggregates are given, by design (see preamble).

| Cell | Note |
|---|---|
| I / ADR, RFC | PARTIAL rests on **A-1**: whether Art. VIII's unenumerated grant reaches these classes. If A-1 resolves to "bounded", both become ABSENT. |
| I / Freeze | Art. XI states frozen content is immutable; it does not name who confers freeze on non-Constitution artifacts. |
| I, II / Conflict | Art. XII and GOV-001 §10 order **principles**, not authorities — hence PARTIAL, not EXPLICIT. |
| II / ADR | CONTRADICTED per **C-2**: §6 actorless merge=accept vs §5.2(5) upstream Chief Architect approval. |
| II / RFC | EXPLICIT for the **approver** (X-6). Executability is a separate matter — see §4 F-3; the matrix records assignment, not executability. |
| II / ARB | PARTIAL: four functions named across §2/§5.2/§7, body unconstituted (**M-3**), character unstated (**A-8**). |
| II / Freeze | EXPLICIT for **APS** class (X-4, X-11). SPEC class is not covered by this model. |
| III / SPEC | The assignment exists (X-13) but POL-VER-001 §3 assigns it otherwise — **C-1**. |
| III / ARB | The model names "Architecture Board", GOV-001 names "ARB"; never equated — **C-3**. |
| III / Freeze | Contradicted by POL-VER-001 §3 on both role and Art. XI procedure — **C-5**. |
| III / *all cells* | Every Model III cell derives from a **PROPOSED** source that is additionally self-blocked (§4 F-1 Route 3). |
| IV / SPEC | PARTIAL because the equation dissolving **C-1** is itself stated by no document (**A-2**). |
| IV / ARB | The equation concerns two **individual roles**; **C-3** is a question about **bodies** and is unaffected. |
| IV / Conflict | UNKNOWN: no source addresses conflict-resolution authority under this reading. |
| V / Merge | PARTIAL: X-21 is a **review** obligation over instrument code, not a merge grant over specification artifacts. |
| V / Freeze, Conflict | EXPLICIT **within instrument scope only** (X-17, X-19). Whether that scope reaches SPEC/ADR/RFC is **M-12**. |

---

## 7. Required Governance Changes

Documents that would have to change under each candidate. **No change is made here, and the
lists are neither work plans nor endorsements.**

### 7.1 Model I — Constitutional Minimal

| Document | Change required |
|---|---|
| `AURA_CONSTITUTION.md` (**FROZEN**) | Art. V to admit a SPEC class, or an authoritative statement that SPEC is not a canonical class. Art. VI to name owners. Art. VIII to enumerate scope (**A-1**). **Requires Art. XI amendment.** |
| `GOVERNANCE.md` | §2 list reconciled with the enumerated Art. VIII scope |
| `VERSIONING.md` | §1/§3 scope clarified as to SPEC (**A-9**) |
| `APS-000` | §3 / Appendix A to register the `SPEC` prefix, and define "canonical document" (**M-11**) |
| `SPEC_TEMPLATE.md` | Lines 9 and 32 reconciled to one role |
| `ADR_TEMPLATE.md` | Approver / acceptance field added (**M-4**) |
| `CONTRIBUTING.md` | Approver rows completed (**C-6**) |
| `adrs/ADR-001_DOCUMENT_MODEL.md` + `docs/adr/001-document-model.md` | Withdrawn or superseded; identifier collision resolved (**C-7**) |

### 7.2 Model II — GOV-001 Four-Tier

| Document | Change required |
|---|---|
| `GOVERNANCE.md` | §2 to add SPEC to the authority list; §6 to name an acceptance actor (**C-2**); ARB constitution — membership, appointment, quorum, binding character (**M-3**, **A-8**); "delegate" defined (**M-6**); "Specification Contributors" defined (**M-7**); §2 tree corrected so a DRAFT document does not subordinate the FROZEN Constitution (**A-6**) |
| `VERSIONING.md` | §1 scope to state whether SPEC is a governance artifact (**A-9**) |
| `CONTRIBUTING.md` | Invariant and APS rows reconciled with GOV-001 §2 (**C-6**) |
| `ADR_TEMPLATE.md` | Approver / acceptance field added |
| `SPEC_TEMPLATE.md` | Lines 9 and 32 reconciled |
| `APS-000` | `SPEC` prefix registered; "canonical document" defined |
| `adrs/ADR-001_DOCUMENT_MODEL.md` + copy | Withdrawn or reconciled (**C-1**, **C-4**, **C-5**, **C-7**) |
| `AURA_CONSTITUTION.md` (**FROZEN**) | Only if Art. VIII scope must be enumerated to authorise §2's SPEC extension — **would require Art. XI amendment** |

### 7.3 Model III — Document-Model Four-Body

| Document | Change required |
|---|---|
| `AURA_CONSTITUTION.md` (**FROZEN**) | Art. V hierarchy inverts under this model (APS becomes a downstream release aggregation). **Requires Art. XI amendment** — this is DR-003, not DR-002 alone. |
| `adrs/ADR-001_DOCUMENT_MODEL.md` | Status PROPOSED → accepted; **the circularity must be broken first**; Open Questions (thresholds, quorum, signature format) closed (**M-9**); identifier reassigned (**C-7**) |
| `docs/adr/001-document-model.md` | Divergent copy withdrawn or reconciled |
| `GOVERNANCE.md` | §2/§3 reconciled with four-body structure; ARB vs Architecture Board resolved (**C-3**); APS authority reconciled (**C-4**) |
| `VERSIONING.md` | §3 freeze authority reconciled (**C-5**) |
| New constituting documents | Architecture Board · Release Authority · Compliance Authority — each requires definition, membership, appointment, quorum (**M-3**) |
| `arc/` + `compliance/arc_to_spec_mapping.yaml` | ARC layer populated; `INV-DOC-002` (every SPEC references ≥1 ARC) is otherwise unsatisfiable |
| `APS-000` | `SPEC`, `ARC` prefixes registered |
| `ADR_TEMPLATE.md` | `Accepted-by` / `accepted_by` field added, one form chosen (**C-7**) |

### 7.4 Model IV — Interchangeable-Title

| Document | Change required |
|---|---|
| A document of sufficient rank | **An explicit statement of the equation**, which exists nowhere (**A-2**). Rank must be at least that of the highest document using either string — the Constitution uses "Chief Architect", so this plausibly reaches Art. XI. |
| `SPEC_TEMPLATE.md` | Lines 9 and 32 reconciled |
| `arc/README.md` | Solidus notation defined or replaced (**A-3**) |
| `GOVERNANCE.md`, `VERSIONING.md` | Role string normalised throughout |
| S3 `CONSTITUTIONAL_DECREE.md`, `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md`, `docs/ops/PROTOCOL_CUSTODIAN.md` | Scope reconciled: instrument-scoped grants vs document-scoped grants (**M-12**) |
| `AGENTS.md` / `CLAUDE.md` | Authority Precedence reconciled with Constitution Art. V (**C-8**) |
| **Plus** | Every change under Models I–III that the equation does not dissolve — notably **C-2** (ADR actor) and **C-3** (bodies) |

### 7.5 Model V — Instrument-Custodian

| Document | Change required |
|---|---|
| A document of sufficient rank | **An instrument extending instrument-scoped authority to specification artifacts.** No such instrument exists, and which document could confer it is undetermined (**M-12**). |
| `AURA_CONSTITUTION.md` (**FROZEN**) | Art. V does not contemplate `CONSTITUTIONAL_DECREE`; **C-8** must be resolved. **Requires Art. XI amendment.** |
| S3 CANONICAL documents | Scope extended from the instrument to SPEC/ADR/RFC classes |
| `GOVERNANCE.md`, `VERSIONING.md` | Reconciled with, or subordinated to, the Decree hierarchy |
| `.github/copilot-instructions.md` | "all canonical definitions" reconciled with the three CANONICAL documents' narrower scope |

### 7.6 A constraint common to all five

Per §2.1, **every amendment path in the corpus routes through the unconstituted ARB or the
undefined Architecture Review**:

- Constitution Art. XI requires an Architecture Review (**M-2**, **A-4**, **M-3**);
- GOV-001 §11 amends via §5.2, which requires ARB assessment (**M-3**);
- POL-VER-001 §10 requires an RFC per CONTRIBUTING.md, which routes through Architecture Review.

**Every model in §7.1–7.5 requires changes to at least one document whose own amendment clause
is currently blocked.** Whether this makes the first governance act self-blocking, and if so how
that is broken, is **part of the decision** (§11.1, item 6) and is not resolved here.

---

## 8. Downstream Impact

### 8.1 Differentiator

Closure of an AD-CA domain requires an approved decision, carried by an ADR into SPEC-002.
Therefore a model unblocks AD-CA work only if it supplies **both** F-1 (SPEC approval) and
F-2 (ADR approval) in executable form.

| Model | Supplies F-1? | Supplies F-2? | Unblocks AD-CA work? |
|---|---|---|---|
| **I** | No (ABSENT) | Only if **A-1** resolves to "general grant" | **No** as written; conditional on A-1 + a SPEC class existing |
| **II** | No (ABSENT) | No (**C-2** actorless) | **No** as written |
| **III** | Asserted (**C-1**) | Yes (X-14) | **Conditional** — requires the circularity broken, C-1/C-5 resolved, three bodies constituted |
| **IV** | Conditional on **A-2** | No — **C-2** persists | **No** as written |
| **V** | No (out of scope) | No (out of scope) | **No** |

### 8.2 Per-domain matrix

`—` = no unblocking. `◐` = conditionally unblocked, subject to that model's §5 dependencies.
Additional per-domain dependencies persist **regardless of model** and are listed in the final
column; they are not resolved by DR-002.

| AD-CA | Subject | I | II | III | IV | V | Additional dependency, model-independent |
|---|---|---|---|---|---|---|---|
| **001** | Source identity / Source Set / Boundary | — | — | ◐ | — | — | DR-001 (two repositories claim the name) |
| **002** | Source canonicalization | — | — | ◐ | — | — | DR-011 (lossy vs lossless; two RIs disagree) |
| **003** | Transformation pipeline | — | — | ◐ | — | — | DR-027 (ADP-001 is 0/14 defined) |
| **004** | Normalization rules | — | — | ◐ | — | — | **No carrier artifact assigned** (DR-007) |
| **005** | Embedding method identity / versioning | — | — | ◐ | — | — | DR-008 (scope disputed) |
| **006** | Dictionary identity / dependency closure | — | — | ◐ | — | — | **No carrier artifact assigned** (DR-007) |
| **007** | Numeric representation | — | — | ◐ | — | — | DR-013, DR-014 (content fully specifiable today; only approval is blocked) |
| **008** | Serialization / byte sequence / hash domains | — | — | ◐ | — | — | APS-200 §8 amendment; APS authority contested (**C-4**) |
| **009** | Identity model | — | — | ◐ | — | — | APS-200 §4 amendment; **C-4** |
| **010** | Provenance boundary | — | — | ◐ | — | — | APS-200 §4 amendment; **C-4** |
| **011** | Registration model / registry | — | — | ◐ | — | — | No registry exists (APS-000 §7 describes one that does not); DR-021 |
| **012** | Freeze lifecycle | — | — | ◐ | — | — | Freeze authority contested (**C-5**); self-freeze deadlock (DR-023) |

### 8.3 Two properties of the blockage

Recorded as facts about the dependency structure, not as advice:

1. **The blockage is procedural, not substantive.** It attaches to the approval step common to
   all twelve domains, not to the technical content of any. Analytical work — drafting, evidence
   gathering, option development — requires no approval authority and is not blocked. What is
   blocked is **closure**.
2. **Resolving DR-002 closes no AD-CA domain by itself.** It removes the common obstacle; each
   domain then requires its own decision on its own merits, plus its model-independent
   dependency in the final column above.

---

## 9. Acceptance Criteria

Objective evidence required to close DR-002.

### 9.1 Conditions

**T-1 Independent determinability.** A reviewer with access only to repository documents, and
without consulting any person, can complete every cell of §9.2 by citation to document, section
and quoted text.

**T-2 In-force sources only.** Every citation resolves to a document whose status is APPROVED or
FROZEN, or to a DRAFT document explicitly designated as governing by an APPROVED or FROZEN
document. **No cell may rest on a PROPOSED or unindexed source.**

**T-3 Non-circularity.** No cited grant depends for its own validity on the authority it grants.
*(Excludes the §4 F-1 Route 3 pattern.)*

**T-4 Constituted bodies.** Every body appearing in any cell has, in a cited document: a
definition, a membership or appointment method, and a decision rule. *(Closes M-3, M-9.)*

**T-5 Recorded act.** For each "approves", "merges" and "freezes" cell, the citation specifies
the artifact-level record — field name, location, form — and that field exists in the applicable
template. *(Closes M-4, C-7.)*

**T-6 Single-valued.** No cell has two conflicting citations. Where two documents address one
cell, one cites the other as superseded, out of scope, or subordinate. *(Closes C-1 … C-8.)*

**T-7 Terminological closure.** Every role string used is defined once and used consistently;
every string in the corpus not used is explicitly retired or mapped. *(Closes M-7, M-8, M-11,
M-14, A-2, A-3.)*

**T-8 Executable path.** For each function, every prerequisite step in the process leading to the
authoritative act is performable by a constituted body under a defined procedure.
*(Closes the F-3 defect, where an approver is named but the path cannot be walked.)*

### 9.2 Determinability matrix — 18 cells

| Function | SPEC | ADR | RFC |
|---|---|---|---|
| Who may propose | ☐ | ☐ | ☐ |
| Who reviews | ☐ | ☐ | ☐ |
| Who approves | ☐ | ☐ | ☐ |
| Who may merge | ☐ | ☐ | ☐ |
| Who freezes | ☐ | ☐ | ☐ |
| Who resolves conflicts | ☐ | ☐ | ☐ |

Plus two cells outside the artifact grid, required by §1.1:

| Function | Status |
|---|---|
| Who conducts the **Architecture Review** (F-4) | ☐ |
| What constitutes a valid Architecture Review output | ☐ |

### 9.3 Current state

**0 of 18 grid cells fully determinable; 1 partially** (RFC / who approves — approver named
under T-1/T-2, path fails T-4 and T-8). **Both Architecture Review cells: not determinable.**

### 9.4 Closure condition

> **DR-002 may be marked CLOSED when, and only when, all eighteen grid cells and both
> Architecture Review cells are completable by citation under T-1 … T-8, and an independent
> reviewer applying the test reaches the same answers.**

Partial completion does not close DR-002 but changes the blockage profile: completing the
**"who approves"** row for SPEC and ADR alone would lift the uniform block in §8.2 while leaving
DR-002 open for the remaining functions. That is a property of the dependency structure;
**whether to proceed on a partial basis is itself a governance decision and is not proposed
here.**

---

## 10. Risks

### 10.1 P0 — Provenance / governance risk

| # | Risk | Evidence |
|---|---|---|
| **P0-1** | **Approvals granted now would be unverifiable later.** With no identified approver (F-1, F-2) and no template field to record one (**M-4**, **C-7**), any AD-CA decision accepted today produces an artifact whose authority an auditor cannot reconstruct. This defeats Constitution Art. IV P4 ("Evidence Before Trust") and Art. X ("Every technically significant architectural decision SHOULD leave a verifiable trace"). |
| **P0-2** | **Acceptance by merge is attributable to no one.** GOV-001 §6 makes ADR acceptance a mechanical consequence of an unattributed act. An AD-CA decision fixing canonical bytes could enter the corpus with no recorded decision-maker. |
| **P0-3** | **A self-blocking first act.** Every amendment path routes through the unconstituted ARB or undefined Architecture Review (§2.1, §7.6). The instrument needed to fix governance is gated by the defect being fixed. |
| **P0-4** | **Circular constitution of authority.** The only source granting SPEC approval requires approval by the role it constitutes (§4 F-1 Route 3). Accepting it by any other route sets a precedent that PROPOSED documents may self-actuate. |
| **P0-5** | **Identifier collision precedent.** Three documents hold `ADR-001` with different statuses and different approval requirements (**C-7**), against APS-000 §4 and POL-VER-001 §8. Any ADR-002 assigned now inherits a corrupt numbering baseline. |
| **P0-6** | **Cross-repository authority is undefined.** SPEC-002 §2.2 constrains S3; `AGENTS.md` ranks the S3 Decree above the Protocol Specification (**C-8**); no document states whether an S1 role binds in S3 (**M-12**). A decision taken in one repository may not bind in the other. |
| **P0-7** | **A DRAFT document appears to subordinate a FROZEN one.** GOV-001 §2's tree renders the Constitution as a child of the Chief Architect (**A-6**). Left unresolved, this weakens the precedence rule (Art. V) that all conflict resolution depends on. |

### 10.2 P1 — Implementation divergence risk

| # | Risk | Evidence |
|---|---|---|
| **P1-1** | **Undecided numeric semantics are already divergent.** Integer division (Python floors; Rust/C/JS truncate) and float→fixed tie rounding (Python half-to-even; C/Rust half-away; JS half-up) were reproduced against `9c6a5d8`. AD-CA-007 cannot be approved while DR-002 is open, so the divergence persists undecided. |
| **P1-2** | **Implementation behaviour may become the de-facto specification by default.** SPEC-002 §3.4 states no candidate is a default, yet the implementation has already committed to `round-half-to-even` by using a language builtin. The longer approval is unavailable, the stronger the pull of the status quo — which SPEC-002's Governing Direction forbids. |
| **P1-3** | **No fixture can be authored.** A fixture encodes an expected value, and an expected value is a decision. Authoring fixtures before approval would invert the Governing Direction, making the fixture the de-facto specification. |
| **P1-4** | **Conformance tests cannot detect the divergence class that matters.** CONF-003 compares one implementation with itself; CONF-006 compares x86 with ARM in one language. Neither detects cross-language divergence. New CONF tests require approved requirements, which require DR-002. |
| **P1-5** | **No independent implementation exists.** Cross-language replay has no second party, so the SPEC-002 §10 criterion is unfalsifiable rather than merely unmet. Commissioning is a resourcing act that no document assigns to any role. |

### 10.3 P2 — Operational risk

| # | Risk | Evidence |
|---|---|---|
| **P2-1** | **Unregistered identifier prefixes accumulate.** `SPEC`, `REQ`, `AD-CA`, `GOV`, `ADP`, `INV-DOC`, `COMP-TM`, `POL-VER`, `RI`, `CR` are in active use; APS-000 §3 / Appendix A registers none of them. |
| **P2-2** | **No CI enforcement in the specification repository.** `ADR-001_DOCUMENT_MODEL` specifies `doc/ci/validate-ids`, `traceability-check` and `frozen-check`; none exists — the repository has no workflows. Identifier uniqueness and frozen immutability are unenforced. |
| **P2-3** | **No ARR has ever been published.** GOV-001 §8 requires an ARR within 5 days of each review meeting; `/adrs/` contains none. Either no review has occurred or none has been recorded. |
| **P2-4** | **Contributor guidance contradicts governance.** CONTRIBUTING.md's Invariant row omits an approver GOV-001 §2 reserves (**C-6**). A contributor following it would not seek required approval. |
| **P2-5** | **Divergent duplicate documents persist.** `docs/adr/001-document-model.md` and `adrs/ADR-001_DOCUMENT_MODEL.md` differ in status, approver count and field name, with no supersession record. |
| **P2-6** | **Role-string proliferation.** Nine strings are in use, two appearing exactly once (`Documentation Architect`, `Chief Specification Architect`) and defined nowhere (**M-8**). |

---

## 11. Decision Boundary

### 11.1 What MUST be decided by governance

Each item requires human governance authority. None can be produced by analysis, and none is
decided here.

| # | Must be decided |
|---|---|
| 1 | For each of SPEC, ADR and RFC: the role or body holding **approval authority** |
| 2 | For each: the **recorded act** by which approval is exercised and evidenced |
| 3 | Whether GOV-001 §2's four-item list is **exhaustive or illustrative** (**A-1**) |
| 4 | Whether SPEC-002 is a **"governance artifact"** (POL-VER-001 §3) and a **"canonical document"** (Constitution Art. VIII) (**A-5**, **A-9**, **M-11**) |
| 5 | Whether "Chief Architect" and "Protocol Custodian" name **one office** (**A-2**) |
| 6 | Whether **ARB and Architecture Board** are one body; whether either is constituted; and how the self-blocking amendment path (§7.6) is broken |
| 7 | **Who may merge**, given that acceptance is bound to merging (**C-2**, **M-4**) |
| 8 | What constitutes a valid **Architecture Review** and who conducts it (**M-2**, **A-4**) |
| 9 | **Freeze authority** for SPEC, and whether Constitution Art. XI procedure applies (**C-5**) |
| 10 | **Conflict-resolution authority** — who applies the Art. XII / GOV-001 §10 precedence, and whose application binds |
| 11 | Whether an **S1 role binds in S3** and vice versa (**M-12**, **C-8**) |
| 12 | Which **process** may legitimately produce this decision (§7.6) |

### 11.2 What MUST NOT be delegated to implementation agents

Prohibited to any AI or implementation agent, by Constitution Art. VIII (X-3) and GOV-001 §9,
and restated here because several items are not obviously "approval" acts:

| # | Must not be delegated | Why |
|---|---|---|
| 1 | **Selecting or constituting an authority model** | The subject of DR-002 itself |
| 2 | **Approving, accepting or freezing any document** | Constitution Art. VIII; GOV-001 §9 |
| 3 | **Resolving any AD-CA domain** | SPEC-002 §3.4 requires explicit architectural authority |
| 4 | **Assigning an orphaned domain to a carrier artifact** | An approval act (AD-CA-004, AD-CA-006) |
| 5 | **Assigning or reassigning identifiers** | APS-000 §4; bears on **C-7** |
| 6 | **Resolving a contradiction between sources** | `AGENTS.md`/`CLAUDE.md`: report, do not silently reconcile |
| 7 | **Effecting any lifecycle status transition** | POL-VER-001 §3 |
| 8 | **Authoring fixtures or golden values before the governing decision** | A fixture encodes an expected value; the value *is* the decision. Would invert the Governing Direction. |
| 9 | **Choosing a numeric, rounding, serialization or hash semantics** | AD-CA-007, AD-CA-008 — and the implementation has already done this by accident once (P1-2) |
| 10 | **Treating implementation behaviour as evidence of the correct answer** | SPEC-002 Governing Direction; `AGENTS.md` rule 1 |
| 11 | **Inferring authority from ownership, permissions, authorship or CODEOWNERS** | Excluded throughout this package |
| 12 | **Declaring an artifact FROZEN** | X-3; and the self-freeze precedent already recorded in **C-5** |

### 11.3 What MAY be delegated

Recorded to make the boundary usable rather than only restrictive. Constitution Art. VIII permits
AI systems to "Analyse · Propose · Implement · Prepare tests · Support documentation".

| # | May be delegated | Condition |
|---|---|---|
| 1 | Evidence gathering and inventory | As in this package |
| 2 | Drafting candidate text for governance documents | Marked DRAFT; carries no normative effect; approval remains with governance |
| 3 | Option development and dependency analysis | No selection among options |
| 4 | Authoring fixtures, tests and conformance runners | **Only after** the governing decision exists |
| 5 | Implementing an approved decision | GOV-001 §9: "Implement changes once an RFC/ADR is approved" |
| 6 | Flagging specification gaps and contradictions | GOV-001 §9 |

---

## 12. STOP

| Measure | Value |
|---|---|
| Governed functions | 7 (F-1 … F-7) |
| Functions with an in-force explicit grant | **1** (F-3 RFC approval — prerequisite step not executable) |
| Candidate models present in repository terminology | 5 — **none selected, none ranked** |
| Bodies referenced but never constituted | 4 |
| Amendment paths currently unblocked | **0 of 3** |
| Direct contradictions | 8 · Ambiguities 9 · Missing definitions 14 |
| Acceptance-test cells determinable | **0 of 18 grid cells; 1 partial; 0 of 2 Architecture Review cells** |
| AD-CA domains unblocked by any model **as written** | **0 of 12** |

**No model selected. No role recommended. No governance document created or modified. No ADR
created. No pull request opened. No code implemented.**

---

**DR-002 STATUS: UNRESOLVED**
**DECISION REQUIRED FROM GOVERNANCE**
**NO NORMATIVE EFFECT**
