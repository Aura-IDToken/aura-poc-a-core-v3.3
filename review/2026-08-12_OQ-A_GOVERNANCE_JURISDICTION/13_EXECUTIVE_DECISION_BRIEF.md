# 13 — EXECUTIVE DECISION BRIEF

**Package:** OQ-A GOVERNANCE / JURISDICTION EVIDENCE PACKAGE
**Date:** 2026-08-12
**Prepared for:** the authority that OQ-A-002 and OQ-A-005 are attempting to identify
**Normative effect:** NONE

---

## 1. The ten questions

| ID | Question | Evidence-Based Finding | Status | Blocking Dependency |
|---|---|---|---|---|
| **OQ-A-001** | What hierarchy of documents is actually established? | Five hierarchy claims exist. AURA-CON-001 Art. V (the only FROZEN source) states 7 levels and omits SPEC, APS-000 and APS-200…APS-950, while including a level occupied by a document that does not exist. `aura-specification/README.md` states a different 9-level list. `AGENTS.md`/`CLAUDE.md` state a 10-tier list from a document self-placed at tier 6. ROLE §9.2 states a 5-level list in which the specification corpus does not appear. APS-000 §1 claims definitions-scoped precedence from a position no hierarchy assigns it. | **NORMATIVE CONFLICT** (cross-corpus) over a **PARTIALLY ESTABLISHED** intra-corpus base | OQ-A-GAP-001 — no cross-corpus precedence rule exists in either corpus |
| **OQ-A-002** | Who possesses approval authority? | Explicit grants exist per artifact class: Chief Architect over Constitution amendments (FROZEN source), and over APS status transitions, invariant changes and RI recognition (GOV-001 §2, DRAFT); Protocol Custodian over `core/`, constitutional constants and sealing (ROLE, CANONICAL). ADR acceptance is "merging the PR", with no approver named. **No approver exists for the SPEC class.** The Chief Architect is never identified; the ARB has no roster, charter or single instance; the Custodian signature that Decree Art. X requires for `core/` changes has never been produced. | **PARTIALLY RESOLVED**; cross-corpus actor question is an **EVIDENCE GAP** | OQ-A-GAP-002 — no document relates Chief Architect to Protocol Custodian |
| **OQ-A-003** | Does the Decree have formal precedence over SPEC? | The Decree claims "MANDATORY / NON-OVERRIDABLE", scope "ALL AI ASSISTANCE", subject "this repository", and **never mentions the specification corpus**; its "prevails" clause governs user requests, not documents. SPEC-002 declares "Normative effect: NONE until APPROVED" and disclaims any power over the implementation repository. Exactly one text orders the two — `AGENTS.md` tiers 1–2 — and its authority to do so is established by nothing. No mechanism in either corpus adjudicates. | **NORMATIVE CONFLICT** for the specification corpus; **UNRESOLVED** for SPEC-002 specifically; **JURISDICTION UNRESOLVED** for ARI | OQ-A-CONFLICT-001, -003; OQ-A-GAP-001 |
| **OQ-A-004** | What normative/procedural status does `CLAUDE.md` have? | Content is role definition, workflow and conflict procedure; it states no protocol semantics. It carries no document ID, version, status or owner, appears in no registry, is absent from the specification corpus entirely, subordinates itself to `AGENTS.md`, and is placed at tier 6 by `AGENTS.md` — which places itself at the same tier. | **PROCEDURAL — normative force UNRESOLVED** | OQ-A-GAP-006 — no status declaration, no approval record for `CLAUDE.md` or `AGENTS.md` |
| **OQ-A-005** | Who may establish ARI semantics? | **No source grants authority over ARI by name.** Two documented routes exist, each conditional: if ARI is protocol content → RFC → Architecture Review → Chief Architect approval; if ARI is instrument content → Protocol Custodian over `core/` and constants, under four mandatory conditions including "creation of new instrument version (not update)". Extension of either authority to ARI is not itself authorized. Three sources bar AI systems from approving. | **CONDITIONALLY DETERMINABLE** | `ARI-D-001` (ARI's artifact class, open) **and** OQ-A-001/-003 (which ladder governs) |
| **OQ-A-006** | What artifact formally records such a decision? | Ten candidate classes characterised. RFC is the only class the corpus calls **mandatory** for changes affecting protocol behaviour. An ADR, per CONTRIBUTING `:70`, *records* a decision rather than constituting one. APS is the class designed to carry semantics, but APS-001 does not exist. **The SPEC class has no in-force governing authority at all.** Two artifact-model regimes coexist — the in-force GOV-001 model and the PROPOSED ARC→SPEC→APS model — assigning ownership and approval differently. | **UNRESOLVED** | OQ-A-GAP-005 (no SPEC approver); OQ-A-GAP-007 (ARI's class) |
| **OQ-A-007** | Is an ADR required? | Required **only if** an architectural decision is embedded in a Major Change (GOV-001 §5.2 step 8); explicitly **not** required in the PATCH lane (§5.1); **required** within the Custodian's constitutional-constant amendment framework (ROLE §4.2 Step 4). AURA-CON-001 Art. X says a significant decision **SHOULD** leave a verifiable trace — SHOULD, and not ADR-specific. The PR template permits "N/A". | **CONDITIONALLY REQUIRED** | Which branch applies depends on OQ-A-005; and OQ-A-GAP-012 — the ADR namespace is blocked by an existing `ADR-001` collision across three files |
| **OQ-A-008** | Is a corresponding SPEC-002 amendment required? | Logical dependency: **conditional** — only if ARI operands are "vector values" under AD-CA-007 (open). Procedural: **not established** — SPEC appears in no change process. Normative: **not established** — SPEC-002 has zero normative effect by its own header, so amending it produces no normative result. Documentation: an inconsistency would arise, with no established repair obligation for a DRAFT document. | **UNRESOLVED** — no established requirement **and** no established amendment path | OQ-A-GAP-005 — no in-force source states who may advance a SPEC document |
| **OQ-A-009** | What is the authoritative sequence: human decision → formal artifact → implementation? | Three workflows are documented with actors, artifacts and gates: the specification-corpus Major Change process; the agent conformance-restoration workflow; the Custodian change-control framework. Eight gaps and four conflicts recorded. The agent workflow's first input (APS-001) does not exist; the Major Change process requires a review body with no established existence and has never been exercised; the Custodian's signature gate has no instance. | **PARTIALLY DOCUMENTED**, with one structural gap | WG-5 — **no workflow step carries a decision between the two corpora**, which is exactly what an ARI decision requires |
| **OQ-A-010** | How exactly does the Two-Key Gate operate? | Zero occurrences of `two-key`, `KEY 1`, `KEY 2` or `ChatGPT` in either repository, outside one review record that disclaims normative effect on its face. All nine operational points are unestablished. Adjacent rules exist and constrain the space: one human approval gate (AGENTS.md rule 13); AI barred from approving by three sources; "final and **sole** approval authority" in GOV-001 §2; an "adversarial review" workflow step with no actor, artifact or criterion. | **EVIDENCE GAP** — Category B working process, no Category A basis | OQ-A-GAP-011 — no repository-normative text describes the arrangement |

---

## 2. What the evidence establishes overall

**Three findings carry the package.**

1. **The two corpora are governance-disjoint.** Neither cites the other, in either direction.
   Each has its own hierarchy, its own named authority, its own change process, and its own
   conflict rule — and no artifact spans them. Every ARI question is cross-corpus by nature,
   because it would be decided under one corpus's authority and would constrain artifacts
   governed by the other.

2. **The one text that orders them is the text least able to.** `AGENTS.md`/`CLAUDE.md` tier 1
   vs tier 2 is the only ordering of Decree against Specification anywhere in either repository.
   That list is asserted by a document which the same list places at tier 6, which carries no
   document ID, version or status, and which the specification corpus does not acknowledge.

3. **Every approval gate that exists in text has either no identified actor or no instance.**
   Chief Architect — never identified. ARB — no roster, no charter, no ARR. RFC route — never
   exercised. Custodian signature — required for `core/` changes, never produced. SPEC class — no
   approver at all. ADR — accepted by merge, with merge authority unassigned outside the PATCH
   lane.

---

## 3. Conflicts and gaps

**13 conflicts recorded, 0 reconciled** (`10_CONFLICT_REGISTER.md`):
cross-corpus hierarchy · intra-corpus hierarchy (specification) · self-referential precedence ·
intra-corpus hierarchy (implementation) · two artifact-model regimes · scope of Chief Architect
authority · ADR acceptance mechanism · "sole approval authority" vs a two-acceptance gate ·
AI participation in acceptance · direction of authority between specification and implementation ·
identifier uniqueness vs three `ADR-001` files · required Custodian signature never produced ·
which specification repository is authoritative.

**15 evidence gaps recorded, 0 fillable from repository material alone**
(`11_EVIDENCE_GAP_REGISTER.md`). Every one requires human governance action to supply the missing
fact.

---

## 4. Effect on the required sequence

```
RD-1 (CLOSED)  →  ARI Decision Readiness (complete)  →  OQ-A  ←── this gate is NOT passed
                                                          ↓
                                       Two-Key Acceptance   ← no documented governance basis
                                                          ↓
                                       ARI-D-001 … ARI-D-027  ← MUST NOT be resolved yet
```

`ARI-D-001 … ARI-D-027` remain blocked. Nothing in this package unblocks any of them, and nothing
in it resolves any ARI semantic.

---

## 5. Declarations

- **No governance model recommended.** None is ranked, preferred, or proposed.
- **No authority selected.** No actor is named as the answer to OQ-A-002 or OQ-A-005.
- **No artifact selected.** Neither ADR nor SPEC nor any other class is chosen for OQ-A-006.
- **No conflict resolved.** All 13 are recorded and referred onward.
- **No ARI semantic resolved.** No scale, formula, dimension, bound, rounding rule, division
  rule, drift model, overflow rule or serialization is selected.
- **Nothing declared APPROVED, ACCEPTED, FROZEN or NORMATIVE.** No newly proposed governance
  arrangement carries any such label anywhere in this package.

---

## 6. Final status

# UNRESOLVED

Four of the ten questions rest on a normative conflict or an outright evidence gap
(OQ-A-001, OQ-A-003, OQ-A-006, OQ-A-008, OQ-A-010 — five, counting the Two-Key Gate); the five
partially-resolved questions each terminate in a condition the corpus does not supply; and **no
question can currently serve as a settled prerequisite for the next governance stage** — the
"Can Proceed?" column is NO for eight of ten and PARTIALLY for the remaining two.

Per the stop condition, where the corpus does not answer:

> **GOVERNANCE GAP — DECISION REQUIRED.** The questions belong to the human authority that
> OQ-A-002 and OQ-A-005 are attempting to identify — and identifying that authority is itself one
> of the unresolved questions.

---

*This document has no normative effect. It reports evidence-based findings and their status. It
recommends nothing, selects nothing, approves nothing, and resolves nothing.*
