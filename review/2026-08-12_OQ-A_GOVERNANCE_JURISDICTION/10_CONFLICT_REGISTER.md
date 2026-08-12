# 10 — CONFLICT REGISTER

**Package:** OQ-A GOVERNANCE / JURISDICTION · **Normative effect:** NONE

**No conflict below is reconciled.** Each entry records both sides, their scope and status, any
apparent precedence, the conflict-resolution mechanism the corpus offers, whether that mechanism
is executable, the consequence, and the unresolved question that remains.

Conflicts already registered by `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md`
§10 (X-1 … X-11) and by `review/2026-08-12_RD1_ARI_DECISION_READINESS/09_OPEN_QUESTIONS.md`
Part C (X-A1 … X-A12) are **not duplicated** here; cross-references are given where relevant.

---

## OQ-A-CONFLICT-001 — Document hierarchy: Decree above Specification, or below it

| Field | Content |
|---|---|
| **Source A** | `aura-poc-a-core-v3.3/AGENTS.md:36-37` (identically `CLAUDE.md`) |
| **Claim A** | Tier 1 "Aura Constitutional Decree / Constitutional Authority"; tier 2 "Aura Protocol Specification". "Lower-level instructions MUST NOT override higher-level authority." |
| **Source B** | `aura-specification/constitution/AURA_CONSTITUTION.md` Article V |
| **Claim B** | Constitution → APS-001 → APS-100 → ADR/ARR/RFC → Playbook → Repository Documentation → Implementation. "A higher-level document has authority over a lower-level document in all cases of conflict." |
| **Subject** | Precedence between the implementation-corpus Decree and the specification corpus |
| **Scope A** | "AI-assisted work" in `aura-poc-a-core-v3.3` |
| **Scope B** | All documents, implementations and architectural decisions |
| **Status A** | No document ID, no version, no lifecycle status, in no registry |
| **Status B** | AURA-CON-001 v1.0, **FROZEN** |
| **Apparent precedence** | Undeterminable without begging the question: assessing A against B requires already knowing which ladder governs |
| **Explicit resolution mechanism** | None that covers both. Art. V governs only the documents it names, and it does not name the Decree |
| **Mechanism executable?** | n/a |
| **Consequence** | Every downstream authority question inherits the ambiguity — including OQ-A-002, OQ-A-003 and OQ-A-005 |
| **Unresolved question** | Which ladder governs an ARI decision? (= `OQ-A` in the RD-1 package) |

---

## OQ-A-CONFLICT-002 — Two hierarchies inside the specification corpus

| Field | Content |
|---|---|
| **Source A** | AURA-CON-001 Article V — 7 levels **including** ADR/ARR/RFC, Playbook, Repository Documentation, Implementation |
| **Source B** | `aura-specification/README.md:63-83` — 9 levels **including** APS-200…APS-950, **excluding** ADR/ARR/RFC |
| **Subject** | Which documents are in the canonical hierarchy |
| **Status A** | FROZEN | **Status B** | README, no ID, no version, no status |
| **Apparent precedence** | Under A itself, a README is "Repository Documentation" — near the bottom of A |
| **Explicit resolution mechanism** | Art. V, if the README is classified as Repository Documentation — but nothing performs that classification |
| **Mechanism executable?** | Not without a classification act that no source authorizes |
| **Consequence** | APS-000 and APS-200…APS-950 are placed **only** by the lower-status document; the Aura Development Playbook is placed by the higher-status document and **does not exist** |
| **Unresolved question** | Is Article V's list closed, and where do the unlisted APS documents sit? |

---

## OQ-A-CONFLICT-003 — A tier-6 document establishes the ordering of tiers 1–5

| Field | Content |
|---|---|
| **Source A** | `AGENTS.md:34-47` — the 10-tier Authority Precedence list |
| **Source B** | `AGENTS.md:41` — tier 6: "AGENTS.md / CLAUDE.md governance workflow" |
| **Subject** | The authority of the precedence list itself |
| **Claim** | A document that places itself at tier 6 asserts the relative authority of tiers 1–5 |
| **Status** | `AGENTS.md`: no ID, no version, no status; self-declared "canonical repository-level agent governance rules" (`:18`) |
| **Apparent precedence** | None establishable — no tier-1…tier-5 source authorizes `AGENTS.md` to order them |
| **Explicit resolution mechanism** | None |
| **Consequence** | The **only** text in either corpus that orders Decree vs Specification is the text whose own authority to do so is least established (`04_DECREE_VS_SPEC_ANALYSIS.md` §5) |
| **Unresolved question** | What grants `AGENTS.md` (and `CLAUDE.md`) authority to establish precedence above their own tier? |

---

## OQ-A-CONFLICT-004 — Two authority hierarchies inside the implementation corpus

| Field | Content |
|---|---|
| **Source A** | `AGENTS.md` / `CLAUDE.md` 10-tier list — tier 1 Decree, tier 2 Specification, tier 3 Invariants |
| **Source B** | `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §9.2 — 1 Decree, 2 ROLE, 3 OPS_PROTOCOL_CANONICAL, 4 ADRs, 5 code comments |
| **Subject** | What ranks below the Decree |
| **Status A** | unstatused | **Status B** | "CANONICAL", authority self-cited to Decree Art. V |
| **Apparent precedence** | B cites the Decree as its authority; A does not cite anything |
| **Explicit resolution mechanism** | None; neither list mentions the other |
| **Consequence** | Under A the specification corpus is tier 2; under B it is absent entirely, so a specification requirement would rank below "code comments and documentation" or nowhere at all |
| **Unresolved question** | Does the specification corpus bind the instrument at all, and if so at which rank? |

---

## OQ-A-CONFLICT-005 — Two artifact-model regimes

| Field | Content |
|---|---|
| **Source A** | GOV-001 §3, §6, §7 + AURA-CON-001 Art. V/VI — ADR/ARR/RFC model; ADR owner = decision author; "Merging the PR = accepting the ADR"; Chief Architect approves the four enumerated classes |
| **Source B** | `adrs/ADR-001_DOCUMENT_MODEL.md` — ARC → SPEC → APS model; Architecture Board approves ARCs and architecture ADRs; Protocol Custodian approves SPECs; Release Authority publishes APS |
| **Subject** | Which artifact classes exist and who approves them |
| **Status A** | GOV-001 1.0-DRAFT; Constitution FROZEN | **Status B** | **PROPOSED**; "requires explicit approval by the Protocol Custodian"; no `Accepted-by:` line; not in the ADR index; not in `DOCUMENT_STATUS.md` |
| **Apparent precedence** | A is in force; B is not |
| **Explicit resolution mechanism** | B's own acceptance procedure (`:105`) — add `Accepted-by:` and merge |
| **Mechanism executable?** | **Only if** the Protocol Custodian has jurisdiction over the specification repository — which is unestablished (`03_AUTHORITY_AND_APPROVAL_MATRIX.md` §4) |
| **Consequence** | The SPEC class — the class SPEC-002 belongs to — is defined and given an approver **only** by a document that is not in force. SPEC-002 therefore has no in-force lifecycle authority |
| **Unresolved question** | Who may advance SPEC-002 beyond DRAFT? |

---

## OQ-A-CONFLICT-006 — Scope of the Chief Architect's approval authority

| Field | Content |
|---|---|
| **Source A** | `GOVERNANCE.md:32-36` — "final and **sole** approval authority over" **four enumerated classes** |
| **Source B** | `aura-specification/README.md:154` — "holds **sole approval authority over canonical documents**" (unenumerated, broader) |
| **Subject** | How wide the approval authority is |
| **Status A** | GOV-001 1.0-DRAFT | **Status B** | README, unstatused |
| **Apparent precedence** | A carries a document ID and appears in `DOCUMENT_STATUS.md`; B does not |
| **Explicit resolution mechanism** | None |
| **Consequence** | Whether the Chief Architect may approve an artifact **outside** the four classes — e.g. a SPEC, or an ARI decision — depends on which statement governs |
| **Unresolved question** | Is GOV-001 §2's list exhaustive? |

---

## OQ-A-CONFLICT-007 — ADR acceptance mechanism

| Field | Content |
|---|---|
| **Source A** | `GOVERNANCE.md:109-110`; `adrs/README.md:23` — "**Merging the PR = accepting the ADR**"; status set to ACCEPTED. No approver named |
| **Source B** | `adrs/ADR-001_DOCUMENT_MODEL.md:55` — "Architecture Board: **approves** and owns … ADRs related to architecture decisions" (PROPOSED) |
| **Source C** | `CONTRIBUTING.md:70` — "ADRs document *decisions already made* — **not proposals**" |
| **Subject** | What act accepts an ADR, and what an ADR can do |
| **Consequence** | Under A, ADR acceptance is effectively held by whoever has merge permission — a platform capability, not a documented governance grant. Under C, an ADR cannot *constitute* a decision at all, only record one |
| **Explicit resolution mechanism** | None |
| **Unresolved question** | Can an ADR establish an ARI semantic, or only record one established elsewhere? (bears on OQ-A-006, OQ-A-007) |

---

## OQ-A-CONFLICT-008 — "Sole approval authority" versus a two-acceptance gate

| Field | Content |
|---|---|
| **Source A** | `GOVERNANCE.md:32` — Chief Architect has "final and **sole** approval authority" over four classes |
| **Source B** | The project's working Two-Key process (Category B, `09_TWO_KEY_GATE_ANALYSIS.md`), requiring two acceptances before formalization |
| **Subject** | Whether a second accepting party is compatible with "sole" |
| **Status A** | DRAFT, in the specification corpus | **Status B** | **No Category A status** — a working process only |
| **Apparent precedence** | Not comparable: B is not repository governance |
| **Explicit resolution mechanism** | GOV-001 §11 (amend GOV-001 via the Major Change process) — available in principle |
| **Mechanism executable?** | Requires an RFC and an ARB (`08_GOVERNANCE_WORKFLOW.md` WG-2) |
| **Consequence** | If the Two-Key arrangement were ever adopted into governance, it would need reconciling with "sole" for those four classes |
| **Unresolved question** | Is Key 2 an approval or an advisory review? **Not answered here**; answering it would be a governance recommendation |

---

## OQ-A-CONFLICT-009 — AI participation in acceptance

| Field | Content |
|---|---|
| **Source A** | AURA-CON-001 Art. VIII — "AI systems MUST NOT approve changes to canonical documents"; GOV-001 §9 — "may NOT approve or freeze"; ROLE §7.1 — "MAY NOT … approve core changes independently" |
| **Source B** | The working process in which an AI review (KEY 2) is one of two acceptances |
| **Subject** | Whether an AI can hold an accepting key |
| **Status A** | FROZEN (Art. VIII) plus two supporting sources | **Status B** | no Category A status |
| **Consequence** | Under A, an AI review cannot be an *approval*. Whether it can be a non-approving acceptance gate is not addressed by any source |
| **Explicit resolution mechanism** | None |
| **Unresolved question** | Is "architectural review acceptance" an approval within the meaning of Art. VIII? |

---

## OQ-A-CONFLICT-010 — Direction of authority between specification and implementation

| Field | Content |
|---|---|
| **Source A** | AURA-CON-001 Art. IV P1 ("Specification First. … Implementation follows specification"); Art. V (Implementation lowest); `CONTRIBUTING.md:11-13`; APS-000 TERM-002 ("An implementation does not define the protocol"); `SPEC-002:37` |
| **Source B** | `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md`, self-declared FROZEN — "**Implementation is the source of truth.** If this document conflicts with the implementation, the implementation governs and this document must be corrected." |
| **Subject** | Which governs when specification and implementation disagree |
| **Status A** | FROZEN Constitution + DRAFT/undeclared others | **Status B** | self-declared FROZEN, no document ID, in no registry |
| **Apparent precedence** | A is stated by the only FROZEN document in the specification corpus; B is scoped to one implementation-corpus document |
| **Explicit resolution mechanism** | None spanning both |
| **Consequence** | Bears directly on whether implementation behaviour could ever define ARI (RD-1 premise 9 says it cannot) |
| **Cross-reference** | Already recorded as X-5 by `NB-021_FROZEN_SEMANTICS_AUDIT.md` §10; re-verified here, **not reopened** |
| **Unresolved question** | Does `AUDIT_LAYER_SPEC.md`'s self-correction clause bind anything beyond itself? |

---

## OQ-A-CONFLICT-011 — Identifier uniqueness versus actual identifiers

| Field | Content |
|---|---|
| **Source A** | `APS-000:90` — "Identifiers MUST NOT be reused, even after deprecation"; `POL-VER-001:100` — "One identifier MUST never be reused"; ADR-001_DOCUMENT_MODEL INV-DOC-005 — "Every identifier SHALL be globally unique" |
| **Source B** | Three files carry `ADR-001`: `adrs/ADR-001_DOCUMENT_MODEL.md` (PROPOSED), `adrs/ADR-001_REPOSITORY_STRUCTURE.md` (ACCEPTED), `docs/adr/001-document-model.md` |
| **Subject** | Identifier integrity in the governance corpus |
| **Consequence** | A new ADR cannot be numbered without first resolving the collision and the namespace question (spec-corpus `adrs/` vs implementation-corpus `docs/`) |
| **Explicit resolution mechanism** | None stated for an existing collision |
| **Cross-reference** | Recorded as X-11 by `NB-021_FROZEN_SEMANTICS_AUDIT.md`; re-verified |
| **Unresolved question** | Which `ADR-001` holds the identifier, and what is the ADR namespace for cross-corpus decisions? |

---

## OQ-A-CONFLICT-012 — Custodian signature required, never produced

| Field | Content |
|---|---|
| **Source A** | `CONSTITUTIONAL_DECREE.md:442` — "Custodian Signature: [Required for core/ changes]"; ROLE §2.2.1 "FINAL AUTHORITY over all changes to `core/`"; AGENTS.md rule 13 |
| **Source B** | Repository state: no signature artifact, no `Accepted-by` convention, **no CODEOWNERS file in the implementation repository**, and `core/` changes present in history (e.g. the Layer-0 API change recorded as P-3 by `NB-021_FROZEN_SEMANTICS_AUDIT.md` §9) |
| **Subject** | Whether the documented merge gate operates |
| **Status** | A: MANDATORY / CANONICAL. B: fact |
| **Consequence** | The implementation corpus's only documented approval gate has no recorded instance; per the method rule, **commit history is not governance authority**, so the absence cannot be cured by pointing at merges |
| **Explicit resolution mechanism** | None; ROLE §7.2 gives the Custodian override authority after the fact |
| **Unresolved question** | Were past `core/` changes authorized, and by what artifact? (already `G-11` in NB-021; re-verified, **not reopened**) |

---

## OQ-A-CONFLICT-013 — Which specification repository is authoritative

| Field | Content |
|---|---|
| **Source A** | `AuraIDToken/aura-specification` @ `62d2d6b` — full governance corpus; referenced by `APS-950:132` and `reference/RI-PY…` as the home of the specification |
| **Source B** | `aura-nomos/aura-specification` @ `eb2a4ec` — one-line README plus CODEOWNERS; attached to this working session |
| **Subject** | Where a governance or ARI decision would be recorded |
| **Status** | Neither repository states its relationship to the other |
| **Consequence** | A decision recorded in the wrong repository has no effect; every specification citation in this package is provenance-dependent on the answer |
| **Explicit resolution mechanism** | None |
| **Cross-reference** | `OQ-D` in `review/2026-08-12_RD1_ARI_DECISION_READINESS/09_OPEN_QUESTIONS.md` |
| **Unresolved question** | Which repository is the authoritative specification corpus, and is a migration in progress? |

---

## Summary

| Conflict | Type | Blocks |
|---|---|---|
| OQ-A-CONFLICT-001 | NORMATIVE CONFLICT (cross-corpus) | OQ-A-001, -002, -003, -005 |
| OQ-A-CONFLICT-002 | NORMATIVE CONFLICT (intra-corpus) | OQ-A-001 |
| OQ-A-CONFLICT-003 | JURISDICTION UNRESOLVED (self-referential authority) | OQ-A-001, -003, -004 |
| OQ-A-CONFLICT-004 | NORMATIVE CONFLICT (intra-corpus) | OQ-A-001, -003 |
| OQ-A-CONFLICT-005 | NORMATIVE CONFLICT (in-force vs PROPOSED) | OQ-A-006, -007, -008 |
| OQ-A-CONFLICT-006 | NORMATIVE CONFLICT (scope) | OQ-A-002, -005 |
| OQ-A-CONFLICT-007 | JURISDICTION UNRESOLVED | OQ-A-006, -007 |
| OQ-A-CONFLICT-008 | JURISDICTION UNRESOLVED | OQ-A-010 |
| OQ-A-CONFLICT-009 | JURISDICTION UNRESOLVED | OQ-A-010 |
| OQ-A-CONFLICT-010 | NORMATIVE CONFLICT | OQ-A-001, -005 |
| OQ-A-CONFLICT-011 | NORMATIVE CONFLICT (rule vs state) | OQ-A-006, -007 |
| OQ-A-CONFLICT-012 | NORMATIVE CONFLICT (rule vs state) | OQ-A-002, -009 |
| OQ-A-CONFLICT-013 | EVIDENCE GAP | all — provenance of any recorded decision |

**13 conflicts. 0 reconciled.**

---

*This document has no normative effect. It records conflicts without resolving them, and selects
no side of any conflict.*
