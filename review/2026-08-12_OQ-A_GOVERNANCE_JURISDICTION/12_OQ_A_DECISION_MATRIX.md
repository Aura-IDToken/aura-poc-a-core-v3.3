# 12 — OQ-A DECISION READINESS MATRIX

**Package:** OQ-A GOVERNANCE / JURISDICTION · **Normative effect:** NONE

---

## 0. Meaning of the columns

| Column | Meaning |
|---|---|
| **Evidence** | What the corpus actually supplies for this question |
| **Conflicts** | `OQ-A-CONFLICT-nnn` entries bearing on it (`10_CONFLICT_REGISTER.md`) |
| **Gaps** | `OQ-A-GAP-nnn` entries bearing on it (`11_EVIDENCE_GAP_REGISTER.md`) |
| **Status** | RESOLVED · PARTIALLY RESOLVED · UNRESOLVED · NORMATIVE CONFLICT · EVIDENCE GAP |
| **Can Proceed?** | Whether the question is **sufficiently established to serve as a prerequisite for the next governance stage** |

> **"Can Proceed?" does not mean "we can guess."** It is answered NO wherever the next stage
> would have to rest on an assumption rather than on established evidence.

---

## 1. Matrix

| OQ-A | Question | Evidence | Conflicts | Gaps | Status | Can Proceed? |
|---|---|---|---|---|---|---|
| **OQ-A-001** | What hierarchy of documents is actually established? | Five hierarchy claims located: AURA-CON-001 Art. V (FROZEN, 7 levels); `aura-specification/README.md` (9 levels, different membership); `AGENTS.md`/`CLAUDE.md` (10 tiers); ROLE §9.2 (5 levels); APS-000 §1 (definitions-scoped precedence). One further model (ARC→SPEC→APS) exists but is PROPOSED. Art. V contains a level occupied by a document that does not exist (Aura Development Playbook). SPEC is placed by no in-force hierarchy. | 001, 002, 003, 004 | 001, 006 | **NORMATIVE CONFLICT** over a PARTIALLY ESTABLISHED intra-corpus base | **NO** — the cross-corpus ordering must be established before any authority claim can be evaluated against it |
| **OQ-A-002** | Who possesses approval authority? | Explicit grants exist and are enumerated in `03_AUTHORITY_AND_APPROVAL_MATRIX.md`: Chief Architect over four classes (GOV-001 §2, DRAFT) and over Constitution amendments (AURA-CON-001 Art. XI, FROZEN); Protocol Custodian over `core/`, constants, sealing (ROLE, CANONICAL). ADR acceptance = merge, with no named approver. SPEC-class approver: absent. Neither named role is related to the other by any document; the Chief Architect is never identified; the ARB has no established existence; the required Custodian signature has never been produced. | 005, 006, 007, 012 | 002, 003, 004, 005, 009, 014 | **PARTIALLY RESOLVED** — per-artifact grants exist in text; the cross-corpus actor question is an **EVIDENCE GAP** | **NO** — for ARI, the operative actor cannot be identified |
| **OQ-A-003** | Does the Decree have formal precedence over SPEC? | Seven-step analysis (`04`): the Decree claims MANDATORY/NON-OVERRIDABLE with scope "ALL AI ASSISTANCE" and never mentions the specification corpus; SPEC-002 declares "Normative effect: NONE until APPROVED" and disclaims power over the implementation repository; exactly one text orders the two (`AGENTS.md` tiers 1–2), asserted by a document self-placed at tier 6; no mechanism adjudicates. | 001, 003, 004, 010 | 001, 006, 008 | **NORMATIVE CONFLICT** for SPEC(a) — the specification corpus; **UNRESOLVED** for SPEC(b) — SPEC-002, which currently has no normative effect to outrank or be outranked | **NO** |
| **OQ-A-004** | What normative/procedural status does `CLAUDE.md` have? | No document ID, version, status or owner; not in any registry; absent from the specification corpus; self-subordinates to `AGENTS.md`; placed at tier 6 by `AGENTS.md`, which places itself at the same tier; content is role, workflow and conflict procedure; states no protocol semantics. | 003 | 006 | **PROCEDURAL — normative force UNRESOLVED** | **PARTIALLY** — sufficient to conclude it cannot be cited as the authority that settles a governance question; **not** sufficient to conclude whether it binds |
| **OQ-A-005** | Who may establish ARI semantics? | No source grants authority over ARI by name. Two documented routes exist, each conditional: (i) if ARI is protocol content → RFC → Architecture Review → Chief Architect approval (CONTRIBUTING `:23`; GOV-001 §5.2); (ii) if ARI is instrument content → Protocol Custodian over `core/` and constants (ROLE §2.1.1, §2.2.1), with mandatory conditions. Both conditions (`ARI-D-001`; which ladder governs) are open; both routes have operational blockers. | 001, 004, 006, 010 | 001, 002, 003, 004, 007, 008 | **CONDITIONALLY DETERMINABLE** | **NO** — the determining conditions are unanswered |
| **OQ-A-006** | What artifact formally records such a decision? | Ten candidate classes characterised (`07`). RFC is the only class the corpus calls **mandatory** for changes affecting protocol behaviour (`rfcs/README.md:7`); an ADR, on CONTRIBUTING `:70`, records a decision rather than constituting one; APS is the class designed to carry semantics but APS-001 does not exist; the SPEC class has **no in-force governing authority**; two artifact-model regimes coexist (in-force vs PROPOSED). | 005, 007, 011 | 005, 007, 012 | **UNRESOLVED** | **NO** — the applicable class depends on `ARI-D-001`, and the class most directly implicated (SPEC) has no approver |
| **OQ-A-007** | Is an ADR required? | Eleven statements located (`08` Part 1). GOV-001 §5.2 step 8: required **if** an architectural decision is embedded. GOV-001 §5.1: explicitly not required in the PATCH lane. ROLE §4.2 Step 4: required within the constitutional-constant amendment framework. AURA-CON-001 Art. X: **SHOULD** leave a verifiable trace, not MUST, and not ADR-specific. PR template permits "N/A". | 005, 007, 011 | 012 | **CONDITIONALLY REQUIRED** | **PARTIALLY** — the rule is established; which branch applies is not, and the ADR namespace/number is blocked by an existing `ADR-001` collision |
| **OQ-A-008** | Is a corresponding SPEC-002 amendment required? | Four dependency types separated (`08` Part 2). Logical: **conditional** on whether ARI operands are "vector values" under AD-CA-007 (U-2, open). Procedural: **not established** — SPEC appears in no change process. Normative: **not established** — SPEC-002 has zero normative effect by its own header. Documentation: likely inconsistency, with no established repair obligation for a DRAFT document. | 005 | 005 | **UNRESOLVED** — no established requirement **and** no established amendment path | **NO** |
| **OQ-A-009** | What is the authoritative sequence: human decision → formal artifact → implementation? | Three workflows documented (`08` Part 3): W-1 spec-corpus Major Change; W-2 agent conformance-restoration workflow; W-3 Custodian change control. Eight workflow gaps (WG-1…WG-8) and four workflow conflicts (WC-1…WC-4) recorded. W-2's first input (APS-001) does not exist; W-1's review body has no established existence; W-3's signature gate has no instance. | 010, 012 | 001, 004, 009, 010, 015 | **PARTIALLY DOCUMENTED** with one structural gap (WG-5: no cross-corpus recording step) | **NO** — the step an ARI decision most needs is the one no source describes |
| **OQ-A-010** | How exactly does the Two-Key Gate operate? | Zero occurrences of `two-key`, `KEY 1`, `KEY 2` or `ChatGPT` in either repository outside a review record that disclaims normative effect. All nine operational points are unestablished. Adjacent Category A rules exist (one human approval gate; AI barred from approving by three sources; "sole approval authority" in GOV-001 §2; an undefined "adversarial review" step). | 008, 009 | 011, 015 | **EVIDENCE GAP** — Category B working process, no Category A basis | **NO** |

---

## 2. Aggregate

| Status | Count | Questions |
|---|---|---|
| RESOLVED | **0** | — |
| PARTIALLY RESOLVED / PARTIALLY DOCUMENTED / CONDITIONALLY DETERMINABLE / CONDITIONALLY REQUIRED | 5 | OQ-A-002, -004, -005, -007, -009 |
| UNRESOLVED | 3 | OQ-A-006, -008, and OQ-A-003 for SPEC(b) |
| NORMATIVE CONFLICT | 2 | OQ-A-001, OQ-A-003 (for SPEC(a)) |
| EVIDENCE GAP | 1 | OQ-A-010 |

| "Can Proceed?" | Count | Questions |
|---|---|---|
| YES | **0** | — |
| PARTIALLY | 2 | OQ-A-004, OQ-A-007 |
| NO | 8 | OQ-A-001, -002, -003, -005, -006, -008, -009, -010 |

**Conflicts recorded: 13. Reconciled: 0.**
**Evidence gaps recorded: 15. Fillable from repository material alone: 0.**

---

## 3. Dependency structure among the OQ-A questions

Recorded as observed, not assumed. Where a direction is not established by evidence, it is marked
unresolved rather than guessed.

```
OQ-A-GAP-013 (which specification repository is authoritative)
        ↓  provenance precondition for everything below
OQ-A-001  document hierarchy  ──────────────┐
        ↓                                   │
OQ-A-003  Decree vs SPEC                    │  both feed
        ↓                                   │
OQ-A-002  approval authority  ←─── OQ-A-GAP-002 (Chief Architect ↔ Custodian)
        ↓
OQ-A-005  who may establish ARI semantics  ←─── ARI-D-001 (open, in the RD-1 package)
        ↓
OQ-A-006  formal artifact  ──→  OQ-A-007  ADR required?
        ↓                        ↓
OQ-A-008  SPEC-002 dependency  ←─┘   (also gated by U-2)
        ↓
OQ-A-009  authoritative workflow   ←─── WG-5 (no cross-corpus recording step)
        ↓
OQ-A-010  Two-Key Gate             ←─── no Category A basis
        ↓
Two-Key Acceptance → ARI-D-001 … ARI-D-027
```

**OQ-A-004** (`CLAUDE.md` status) sits beside this chain rather than inside it: it does not gate
the others, but it determines whether the document that supplies the **only** cross-corpus
ordering (via `AGENTS.md`) can be cited in answering OQ-A-001 and OQ-A-003.

---

## 4. What the next governance stage would rest on if it proceeded today

Stated factually, not as advice:

| If the next stage proceeded now | It would rest on |
|---|---|
| Two-Key Acceptance | A process with no documented governance basis (OQ-A-010), operated by actors whose authority for this class of decision is unestablished (OQ-A-002, OQ-A-005) |
| Any `ARI-D-nnn` resolution | An unestablished hierarchy (OQ-A-001), an unidentified approver (OQ-A-003), and an artifact class with no approver (OQ-A-006, OQ-A-008) |
| Recording the result | An undetermined repository (GAP-013), an undetermined ADR namespace (GAP-012), and no documented cross-corpus recording step (WG-5) |

---

*This document has no normative effect. It records readiness, not decisions. It selects no
governance model, no authority, and no artifact, and it resolves no conflict.*
