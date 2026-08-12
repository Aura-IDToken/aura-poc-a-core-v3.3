# 02 — DOCUMENT HIERARCHY EVIDENCE (OQ-A-001)

**Question:** *What hierarchy of documents is actually established?*
**Required result:** evidence + hierarchy
**Normative effect:** NONE

---

## 0. Four things kept separate

Per the mandatory distinctions, this document separates:

| Concept | Definition used here | Where each is found |
|---|---|---|
| **DOCUMENT HIERARCHY** | Which document prevails over which in a textual conflict | H-1, H-2, H-3, H-4, H-5 below |
| **AUTHORITY HIERARCHY** | Which *actor* may decide | `03_AUTHORITY_AND_APPROVAL_MATRIX.md` |
| **APPROVAL WORKFLOW** | What must happen for an artifact to acquire status | `08_GOVERNANCE_WORKFLOW.md` |
| **CHANGE WORKFLOW** | What must happen for a change to be made | `08_GOVERNANCE_WORKFLOW.md` |

They are **not** assumed to be the same. Three of the five hierarchy claims below mix document
ordering with actor ordering; that mixing is recorded as a finding, not resolved.

---

## 1. Hierarchy claims found

### H-1 — AURA Constitution Article V ("Canonical Hierarchy")

> **SOURCE** `aura-specification/constitution/AURA_CONSTITUTION.md` · **DOC ID** AURA-CON-001 ·
> **VERSION** 1.0 · **STATUS** FROZEN · **SECTION** Article V
>
> ```
> AURA Constitution → Aura Protocol Specification (APS-001) → Protocol Invariants (APS-100)
> → ADR / ARR / RFC → Aura Development Playbook → Repository Documentation → Implementation
> ```
> "A higher-level document has authority over a lower-level document in all cases of conflict."

| Property | Finding |
|---|---|
| Levels | 7, ordered |
| Establishing source | The only FROZEN document in either corpus |
| Terminology | "canonical hierarchy"; "authority over"; "in all cases of conflict" |
| Subject covered | Documents |
| Closed or open? | **Neither stated.** No clause says the list is exhaustive, and no clause says other documents may be inserted. Documents not named have no stated position — see §2. |
| Includes SPEC? | **No.** "SPEC" as an artifact class does not appear. `SPEC-002` is therefore unplaced by this hierarchy. |
| Includes ADR? | **Yes** — jointly with ARR and RFC at one level, below APS-100 |
| Includes RFC? | **Yes** — same level as ADR/ARR |
| Includes implementation-repository documentation? | **Ambiguous.** "Repository Documentation" is listed, but the article does not state *which* repository. |
| Includes `CLAUDE.md`? | **Not by name.** Its placement depends on whether it is "Repository Documentation". |
| Includes governance instructions (`AGENTS.md`, Copilot directives)? | **Not by name.** |
| Includes APS-000, APS-200…APS-950? | **No.** Only APS-001 and APS-100 are named. |
| Contradicted by | H-2 (different membership), H-3 (different ordering and different top), H-4 (different top), H-5 (a precedence claim by a document the ladder omits) |

---

### H-2 — `aura-specification/README.md` "Canonical Document Hierarchy"

> **SOURCE** `aura-specification/README.md:63-83` · **DOC ID** none · **VERSION** none ·
> **STATUS** none stated
>
> ```
> AURA Constitution (FROZEN) → APS-001 → APS-100 → APS-200 ←→ APS-300 → APS-400
> → APS-500 → APS-900 → APS-950
> ```
> "Higher documents have authority over lower documents. No implementation may contradict any
> document in this hierarchy."

| Property | Finding |
|---|---|
| Levels | 9 (with one lateral pair) |
| Establishing source | A README with no document ID, no version, no status; not listed in `releases/v0.1.0/DOCUMENT_STATUS.md` |
| Subject covered | APS documents only |
| Closed or open? | Not stated |
| Includes ADR / ARR / RFC? | **No** — the three artifact classes present in H-1 are absent here |
| Includes SPEC? | **No** |
| Relation to H-1 | **Different membership in both directions.** H-1 has ADR/ARR/RFC + Playbook + Repository Documentation, which H-2 lacks; H-2 has APS-200…APS-950, which H-1 lacks. Neither document mentions the other's list. |
| Status of the claim | A README statement of a hierarchy, not a lifecycle-managed normative statement. Under H-1 itself, a README is "Repository Documentation" — i.e. the document asserting H-2 sits near the bottom of H-1. |

---

### H-3 — `AGENTS.md` / `CLAUDE.md` "Authority Precedence (Highest → Lowest)"

> **SOURCE** `aura-poc-a-core-v3.3/AGENTS.md:34-53`, reproduced **verbatim and identically** at
> `aura-poc-a-core-v3.3/CLAUDE.md` · **DOC ID** none · **VERSION** none · **STATUS** none stated
>
> ```
> 1 Aura Constitutional Decree / Constitutional Authority
> 2 Aura Protocol Specification
> 3 Protocol Invariants
> 4 Existing repository-level constitutional/Copilot directives
> 5 Conformance Test Matrix / approved Conformance Requirements
> 6 AGENTS.md / CLAUDE.md governance workflow
> 7 Path-specific agent instructions
> 8 Prompt/task instructions
> 9 Existing implementation
> 10 Agent assumptions
> ```
> "Lower-level instructions MUST NOT override higher-level authority."

| Property | Finding |
|---|---|
| Levels | 10, ordered |
| Establishing source | `AGENTS.md`, which the same list places at **tier 6** |
| Subject covered | Mixed: documents (tiers 1–5, 7), a workflow (6), instructions (8), an artifact (9), and a cognitive state (10) |
| Closed or open? | Not stated |
| Applies to ARI? | Not stated. The list governs "AI-assisted work" (`AGENTS.md:3`); it does not name ARI or any protocol semantic. |
| Applies to governance artifacts? | Partially — tiers 1, 4, 6, 7 are governance artifacts |
| Self-referential problem | **RECORDED.** A tier-6 document asserts the ordering of tiers 1–5. No tier-1…tier-5 source authorizes `AGENTS.md` to establish that ordering, and no higher source states that the ordering is correct. The list's own authority to bind tiers above it is **not established**. |
| Relation to H-1 | **Incompatible on the placement of the Decree.** H-3 tier 1 = "Aura Constitutional Decree"; under H-1 the Decree is not named at all and would fall under "Repository Documentation" — i.e. *below* APS-001 and APS-100, which H-3 places at tiers 2 and 3. |
| Relation to H-2 | H-2 contains no Decree and no agent instructions |

---

### H-4 — `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §9.2 "Authority Hierarchy"

> **SOURCE** `aura-poc-a-core-v3.3/ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §9.2 · **VERSION** 1.0 ·
> **STATUS** CANONICAL · **AUTHORITY** (self-declared) "Constitutional Decree Article V"
>
> ```
> 1 Constitutional Decree (highest)
> 2 This document (Role of Protocol Custodian)
> 3 OPS_PROTOCOL_CANONICAL.md
> 4 Architecture Decision Records (ADRs)
> 5 Code comments and documentation
> ```
> "**The Constitutional Decree ALWAYS prevails.**"

| Property | Finding |
|---|---|
| Levels | 5, ordered |
| Subject covered | Documents, "in case of conflict between documents" |
| Scope | The implementation instrument; the specification corpus is **not mentioned at any level** |
| Includes APS / SPEC / Constitution (AURA-CON-001)? | **No.** None of the specification corpus's documents appears anywhere in this ladder. |
| Includes ADR? | Yes, at tier 4 — but which ADR namespace (spec corpus `adrs/`, or the implementation corpus's `docs/ADR_005_NO_FLOAT_RUNTIME.md`) is not stated |
| Closed or open? | Not stated |
| Relation to H-1 | **Incompatible.** H-1 places the Constitution highest and implementation lowest; H-4 places the Decree highest and does not include the Constitution at all. |
| Relation to H-3 | Compatible on the top slot (Decree), incompatible on everything below: H-3 places "Aura Protocol Specification" at 2, H-4 places the ROLE document at 2 and omits the specification entirely. |

---

### H-5 — APS-000 §1 precedence claim

> **SOURCE** `aura-specification/aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md:18` ·
> **DOC ID** APS-000 · **VERSION** 1.0-DRAFT · **STATUS** DRAFT
>
> "In cases of conflicting definitions, **APS-000 takes precedence**."

| Property | Finding |
|---|---|
| Subject covered | **Definitions only** — a scoped precedence claim, not a general one |
| Position under H-1 | **APS-000 is not in H-1 at all.** H-1 names APS-001 and APS-100; APS-000 is unplaced. |
| Position under H-2 | Also absent |
| Status | DRAFT — a document whose own status table (§5) says DRAFT means "Under development" |
| Effect | A DRAFT document asserts precedence over unnamed others for a defined subject, from a position no hierarchy assigns it. **JURISDICTION UNRESOLVED.** |

---

### H-6 (not in force) — ADR-001 Document Model

> **SOURCE** `aura-specification/adrs/ADR-001_DOCUMENT_MODEL.md` · **STATUS** **PROPOSED** ·
> `:105` "This ADR is PROPOSED and requires explicit approval by the Protocol Custodian.
> Approval is recorded by adding an `Accepted-by: <Protocol Custodian>` line"
>
> Proposes `ARC → SPEC → APS` with ARC "canonical for architecture decisions", SPEC "canonical
> for normative requirements", APS the published aggregation.

| Property | Finding |
|---|---|
| In force? | **No.** No `Accepted-by:` line exists in the file; `adrs/README.md:15` indexes only ADR-001_REPOSITORY_STRUCTURE; `releases/v0.1.0/DOCUMENT_STATUS.md:26` lists only "Repository Structure ADR \| ADR-001 \| 1.0 \| ACCEPTED" |
| If it were in force | It would restructure the hierarchy entirely and would place SPEC (hence SPEC-002) as "canonical for normative requirements" under Protocol Custodian approval — a placement no in-force source provides |
| Identifier problem | Three documents carry `ADR-001`: `adrs/ADR-001_DOCUMENT_MODEL.md` (PROPOSED), `adrs/ADR-001_REPOSITORY_STRUCTURE.md` (ACCEPTED), `docs/adr/001-document-model.md`. APS-000 §4 states "Identifiers MUST NOT be reused, even after deprecation"; ADR-001_DOCUMENT_MODEL itself states INV-DOC-005 "Every identifier SHALL be globally unique". |

---

## 2. What is *not* placed by any in-force hierarchy

| Artifact | H-1 | H-2 | H-3 | H-4 | Consequence |
|---|---|---|---|---|---|
| `SPEC-002` (and the SPEC class) | absent | absent | arguably tier 2 "Aura Protocol Specification", **not stated** | absent | The document the ARI decisions repeatedly touch has **no established position in any in-force hierarchy** |
| `CONSTITUTIONAL_DECREE.md` | absent by name | absent | **tier 1** | **tier 1** | Placed at the top by two implementation-corpus documents and nowhere by the specification corpus |
| `CLAUDE.md` | absent by name | absent | **tier 6** | absent | see `05_CLAUDE_MD_STATUS_ANALYSIS.md` |
| `AGENTS.md` | absent | absent | **tier 6** (self-placed) | absent | as above |
| APS-000, APS-200…APS-950 | absent | present | "Protocol Invariants" covers APS-100 only | absent | Most APS documents are placed by a README and by nothing else |
| `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md`, `OPS_PROTOCOL_CANONICAL.md` | absent | absent | arguably tier 4 | tiers 2–3 | placed only by themselves and by H-3's generic tier 4 |
| The Aura Development Playbook (named in H-1) | present | absent | absent | absent | **The document does not exist in either repository** — H-1 contains a level occupied by nothing |

---

## 3. Conflict-resolution mechanisms that exist, and what they resolve

| Mechanism | Source | What it actually resolves | Does it resolve document precedence between corpora? |
|---|---|---|---|
| "A higher-level document has authority over a lower-level document in all cases of conflict" | AURA-CON-001 Art. V | Conflicts **between documents named in H-1** | **No** — silent on documents it does not name, including the Decree and SPEC |
| Interpretation precedence: mission → constitutional principles → protocol conformance → determinism → auditability | AURA-CON-001 Art. XII; restated GOV-001 §10 | Ambiguity of **interpretation**, by ranking values | **No** — it ranks values, not documents; it cannot say which document wins |
| "The Constitutional Decree ALWAYS prevails" | ROLE §9.2 | Conflicts among the five documents in H-4 | **No** — the specification corpus is not in its list |
| "The Constitution prevails" | Decree Art. V ("When Authority Conflicts Arise") | Conflicts between **a user request** and the Decree | **No** — the clause is about user requests, and "the Constitution" there denotes the Decree itself |
| "Lower-level instructions MUST NOT override higher-level authority" + "do not silently reconcile … request human/Protocol Custodian resolution" | AGENTS.md `:47-53`; CLAUDE.md; `docs/conformance/README.md` | Agent behaviour on detecting a conflict — it **routes** the conflict to a human | **No** — it is an escalation rule, and it names the resolver ambiguously ("human/Protocol Custodian") |
| Amendment Procedure | AURA-CON-001 Art. XI; GOV-001 §5.3 | How the Constitution is changed | **No** |

**Finding:** every mechanism found either (i) resolves conflicts only inside one corpus, (ii)
ranks values rather than documents, or (iii) escalates to a human whose identity for this class
of conflict is not established (`03_AUTHORITY_AND_APPROVAL_MATRIX.md` §4). **No mechanism in the
corpus adjudicates a conflict between the two corpora.**

---

## 4. OQ-A-001 — finding

**What hierarchy is actually established?**

| | Finding |
|---|---|
| Within the specification corpus, for the documents it names | **PARTIALLY ESTABLISHED** — H-1 is stated by the only FROZEN document and is explicit ("in all cases of conflict"), but it omits SPEC, APS-000 and APS-200…APS-950, contains one level occupied by a non-existent document, and is contradicted in membership by H-2 |
| Within the implementation corpus | **PARTIALLY ESTABLISHED** — H-3 and H-4 agree that the Decree is highest and disagree on everything below; H-3's establishing document places itself at tier 6 |
| **Between the two corpora** | **NORMATIVE CONFLICT + EVIDENCE GAP** — H-1 and H-3/H-4 order the same artifacts incompatibly; neither corpus cites the other; no mechanism adjudicates |
| For ARI specifically | **JURISDICTION UNRESOLVED** — no hierarchy claim states that it applies to ARI, and ARI is not an artifact class in any of them |

**Status: NORMATIVE CONFLICT (cross-corpus) over a PARTIALLY ESTABLISHED intra-corpus base.**

No hierarchy is selected here, and no document is declared to prevail.

---

*This document has no normative effect. It records hierarchy claims and their conflicts. It
selects no hierarchy, grants no authority, and resolves nothing.*
