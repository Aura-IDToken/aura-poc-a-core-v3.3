# 11 — EVIDENCE GAP REGISTER

**Package:** OQ-A GOVERNANCE / JURISDICTION · **Normative effect:** NONE

Each gap records: the missing fact · why it matters · the affected OQ-A question · the evidence
needed · whether that evidence can be obtained from repository material · whether human
governance action is required.

**"Human governance action required" is a factual observation about where the missing fact can
come from. It is not a recommendation that any particular action be taken.**

---

## OQ-A-GAP-001 — No cross-corpus precedence rule

| Field | Content |
|---|---|
| **Missing fact** | Which authority ladder governs when the specification corpus and the implementation corpus order the same artifacts differently |
| **Why it matters** | Determines whose approval counts for every ARI decision, and whether the Decree's Article I constants bind a protocol-level ARI |
| **Affects** | OQ-A-001, OQ-A-002, OQ-A-003, OQ-A-005, OQ-A-009 |
| **Evidence needed** | A statement, in a source with established authority over both corpora, ordering them — or an explicit statement that each governs only its own corpus, with a conflict rule |
| **Obtainable from repository material?** | **No.** Both corpora were searched in both directions; neither cites the other |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-002 — Relationship between Chief Architect and Protocol Custodian

| Field | Content |
|---|---|
| **Missing fact** | Whether these are the same person, the same role under two names, or distinct roles with distinct jurisdictions |
| **Why it matters** | The specification corpus vests approval in the Chief Architect; the implementation corpus vests it in the Protocol Custodian. An ARI decision could be authorized under one and unauthorized under the other |
| **Affects** | OQ-A-002, OQ-A-005, OQ-A-009, OQ-A-010 |
| **Evidence needed** | A document stating the relationship, or a single role definition covering both corpora |
| **Obtainable from repository material?** | **No.** The Custodian is identified (Kamil Krasiński, implementation corpus); the Chief Architect is never identified in either corpus |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-003 — Identity of the Chief Architect

| Field | Content |
|---|---|
| **Missing fact** | Which person or account holds the Chief Architect role |
| **Why it matters** | Four approval classes and every APS status transition depend on this actor |
| **Affects** | OQ-A-002, OQ-A-005, OQ-A-009 |
| **Evidence needed** | A role-to-identity mapping in a governance document |
| **Obtainable from repository material?** | **Partially and unreliably.** `.github/CODEOWNERS` maps every path to `@AuraIDToken` with the comment "review by the Chief Architect" — but per the method rule `CODEOWNER ≠ AUTHORITY`, and no document states the account **is** the Chief Architect |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-004 — Existence and composition of the Architecture Review Board

| Field | Content |
|---|---|
| **Missing fact** | Whether the ARB exists, who is on it, and how it convenes |
| **Why it matters** | The ARB is a mandatory step in the only documented route for changes affecting protocol behaviour (GOV-001 §5.2 step 4, §7 step 7). Without it, that route is not executable |
| **Affects** | OQ-A-002, OQ-A-006, OQ-A-007, OQ-A-009 |
| **Evidence needed** | A roster, charter, or at least one ARR |
| **Obtainable from repository material?** | **No.** Zero `ARR-*` files; no roster; no charter |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-005 — Approval authority for the SPEC document class

| Field | Content |
|---|---|
| **Missing fact** | Who may advance a SPEC document (concretely SPEC-002) beyond DRAFT |
| **Why it matters** | SPEC-002 carries AD-CA-007, which may or may not cover ARI numerics (U-2). If it does, the ARI decisions depend on a class with no in-force approver |
| **Affects** | OQ-A-006, OQ-A-008 |
| **Evidence needed** | An in-force statement assigning SPEC approval — GOV-001 §2 does not include SPEC; POL-VER-001 §1 does not cover it; the only assignment is in a PROPOSED ADR |
| **Obtainable from repository material?** | **No** — only by accepting ADR-001_DOCUMENT_MODEL, which itself requires an authority whose jurisdiction is unestablished |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-006 — Status of `AGENTS.md` and `CLAUDE.md`

| Field | Content |
|---|---|
| **Missing fact** | Whether these documents have binding force, and on what basis |
| **Why it matters** | They contain the **only** text in either corpus ordering Decree vs Specification, and they define the agent workflow this work is conducted under |
| **Affects** | OQ-A-001, OQ-A-003, OQ-A-004 |
| **Evidence needed** | A status declaration (ID, version, lifecycle status) and an approval record from an actor with established authority |
| **Obtainable from repository material?** | **No.** Neither carries an ID, version or status; neither appears in any registry; the specification corpus does not mention them |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-007 — Whether ARI is protocol content or instrument content

| Field | Content |
|---|---|
| **Missing fact** | The artifact class ARI belongs to |
| **Why it matters** | Determines which authority grant reaches it and which formal artifact would record a decision |
| **Affects** | OQ-A-005, OQ-A-006, OQ-A-007, OQ-A-008 |
| **Evidence needed** | The `ARI-D-001` ruling |
| **Obtainable from repository material?** | **No** — RD-1 (CLOSED) established that no normative ARI definition exists |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-008 — Scope of the Decree's Article I constants

| Field | Content |
|---|---|
| **Missing fact** | Whether "Scaling Factor: 100,000", "Sentinel Drift Threshold: 0.68", "Q16.16" and "int32/int64" bind any conformant implementation or only `aura-poc-a-core-v3.3` |
| **Why it matters** | Three ARI decisions (`ARI-D-007`, `ARI-D-008`, `ARI-D-014`) touch exactly these values, and SPEC-002 simultaneously lists `100000` as candidate-only |
| **Affects** | OQ-A-003, OQ-A-005 |
| **Evidence needed** | A scope statement in the Decree or in a source with authority over it |
| **Obtainable from repository material?** | **No.** The Decree declares scope "ALL AI ASSISTANCE" and subject "this repository"; it says nothing about other implementations |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-009 — Meaning of "authorized before execution" in the CHANGELOG policy

| Field | Content |
|---|---|
| **Missing fact** | What artifact records the authorization the CHANGELOG asserts occurred for each logged task |
| **Why it matters** | It is the corpus's only standing claim that a documented approval practice exists in the implementation repository |
| **Affects** | OQ-A-002, OQ-A-009 |
| **Evidence needed** | An authorization artifact referenced by at least one entry |
| **Obtainable from repository material?** | **No.** No entry references one; no signature artifact exists (`OQ-A-CONFLICT-012`) |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-010 — Cross-corpus recording step

| Field | Content |
|---|---|
| **Missing fact** | How a decision made under one corpus's authority is recorded so that it binds artifacts governed by the other |
| **Why it matters** | An ARI decision necessarily spans both: it would be decided under some authority and would constrain both the specification and the instrument |
| **Affects** | OQ-A-006, OQ-A-008, OQ-A-009 |
| **Evidence needed** | A documented step in any workflow |
| **Obtainable from repository material?** | **No** — recorded as WG-5 in `08_GOVERNANCE_WORKFLOW.md` |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-011 — Two-Key Gate: all nine operational points

| Field | Content |
|---|---|
| **Missing fact** | Who provides Key 1 · what constitutes explicit acceptance · who performs Key 2 · what constitutes architectural acceptance · disagreement handling · insufficient-evidence handling · whether formalization requires both · what artifact records acceptance · whether the acceptance requires an ADR |
| **Why it matters** | "Two-Key Acceptance" is a named gate in the required sequence, immediately before `ARI-D-001 … ARI-D-027` |
| **Affects** | OQ-A-010 |
| **Evidence needed** | Any repository-normative text describing the arrangement |
| **Obtainable from repository material?** | **No.** Zero hits for `two-key`, `KEY 1`, `KEY 2`, `ChatGPT` in either repository outside a review record that disclaims normative effect |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-012 — ADR namespace for a cross-corpus decision

| Field | Content |
|---|---|
| **Missing fact** | Whether an ADR recording an ARI decision belongs to `aura-specification/adrs/` or to the implementation corpus's `docs/`, and what number it takes given the existing `ADR-001` collision |
| **Why it matters** | An ADR cannot be created without a namespace and a number |
| **Affects** | OQ-A-006, OQ-A-007 |
| **Evidence needed** | A namespace rule; a resolution of the collision |
| **Obtainable from repository material?** | **No** — the rules (APS-000 §4, POL-VER-001 §8, INV-DOC-005) prohibit reuse but do not resolve an existing collision |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-013 — Authoritative specification repository

| Field | Content |
|---|---|
| **Missing fact** | Which of the two `aura-specification` repositories is authoritative |
| **Why it matters** | Determines where any decision would be recorded and whether this package's specification citations are provenance-valid |
| **Affects** | all ten OQ-A questions, as a provenance precondition |
| **Evidence needed** | A statement in either repository, or an organizational record |
| **Obtainable from repository material?** | **No** — neither repository mentions the other |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-014 — Merge authority outside the PATCH lane

| Field | Content |
|---|---|
| **Missing fact** | Who may merge a non-PATCH pull request in the specification repository, given that "Merging the PR = accepting the ADR" |
| **Why it matters** | Under GOV-001 §6, merge permission is the operative ADR acceptance act, yet only §5.1 (PATCH) names a merger |
| **Affects** | OQ-A-002, OQ-A-006, OQ-A-007 |
| **Evidence needed** | An assignment of merge authority per change class |
| **Obtainable from repository material?** | **Partially** — GitHub branch-protection settings could show who *can* merge, but per the method rule a platform permission is not a governance grant |
| **Human governance action required?** | **Yes** |

## OQ-A-GAP-015 — Definition of "adversarial review"

| Field | Content |
|---|---|
| **Missing fact** | The actor, artifact and acceptance criterion for the "Adversarial review" step in the AGENTS.md / CLAUDE.md workflow |
| **Why it matters** | It is the only documented step resembling an independent second review, and therefore the nearest Category A analogue to a second key |
| **Affects** | OQ-A-009, OQ-A-010 |
| **Evidence needed** | A definition in any governance document |
| **Obtainable from repository material?** | **No** — the term appears only as a workflow step name |
| **Human governance action required?** | **Yes** |

---

## Summary

| # | Gap | Obtainable from repository? | Human action required |
|---|---|---|---|
| 001 | Cross-corpus precedence rule | No | Yes |
| 002 | Chief Architect ↔ Protocol Custodian relationship | No | Yes |
| 003 | Identity of the Chief Architect | No (CODEOWNERS is not evidence of authority) | Yes |
| 004 | ARB existence and composition | No | Yes |
| 005 | SPEC-class approval authority | No | Yes |
| 006 | Status of `AGENTS.md` / `CLAUDE.md` | No | Yes |
| 007 | ARI's artifact class | No | Yes |
| 008 | Scope of Decree Article I constants | No | Yes |
| 009 | Authorization artifact behind the CHANGELOG policy | No | Yes |
| 010 | Cross-corpus recording step | No | Yes |
| 011 | Two-Key Gate — nine points | No | Yes |
| 012 | ADR namespace and collision | No | Yes |
| 013 | Authoritative specification repository | No | Yes |
| 014 | Merge authority outside the PATCH lane | Partially, and not as governance evidence | Yes |
| 015 | Definition of "adversarial review" | No | Yes |

**15 gaps. 0 fillable from repository material alone.**

---

*This document has no normative effect. It records what is missing and where the missing fact
would have to come from. It proposes no governance arrangement and recommends no action.*
