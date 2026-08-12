# 08 — GOVERNANCE WORKFLOW (OQ-A-007, OQ-A-008, OQ-A-009)

**Normative effect:** NONE

---

# PART 1 — OQ-A-007: IS AN ADR REQUIRED?

**Required result:** procedural determination
**Method constraint:** the answer is not "yes because ADRs are normally used for architecture".
Only repository evidence counts.

## 1.1 Every statement located about when an ADR is required

| # | Statement | Source | Modality |
|---|---|---|---|
| E-1 | "8. **ADR created if architectural decision is embedded**" — step 8 of the Major Change process | GOV-001 §5.2 | **Conditional** ("if") |
| E-2 | "3. No RFC or ADR required" — for PATCH-lane changes (typos, formatting, non-normative clarifications) | GOV-001 §5.1 | **Explicit exemption** |
| E-3 | "ADRs document *decisions already made* — **not proposals** (use RFC for proposals)" | CONTRIBUTING `:70` | Characterisation: an ADR is a **record**, not the decision act |
| E-4 | "ADRs for major decisions require a linked RFC" | `adrs/README.md:25` | Conditional on an ADR existing; requires an RFC alongside |
| E-5 | "Every technically significant architectural decision **SHOULD** leave a verifiable trace" | AURA-CON-001 Art. X | **SHOULD**, not MUST; and "verifiable trace" is not defined as an ADR |
| E-6 | Evidence MUST be "Complete, Immutable, Replayable, Linked to the relevant version" | AURA-CON-001 Art. X | Applies to evidence, not to the decision record's form |
| E-7 | "**Step 4: Documentation** — Update Constitutional Decree; **Create ADR documenting the change**; Update all affected documentation" — within the Constitutional Amendment Framework | ROLE §4.2 | **Mandatory within that framework**, i.e. when a Custodian changes a constitutional constant |
| E-8 | PR template: "Related RFC or ADR — RFC-NNN: [link] or N/A / ADR-NNN: [link] or N/A" | `.github/PULL_REQUEST_TEMPLATE/…` | Permits N/A — so neither is unconditionally required |
| E-9 | PR type table: "New specification content (**requires RFC**)"; "Protocol Invariant change (**requires RFC**)"; "Conformance Test change (**requires RFC**)" | ibid.; CONTRIBUTING type table | **RFC is the named requirement; ADR is not** |
| E-10 | "3. ADR (**if required** for architecture) — ADR-###" — step 3 of the PROPOSED lifecycle | ADR-001_DOCUMENT_MODEL `:74` | Conditional; **and not in force** |
| E-11 | "The Custodian MUST ensure … All ADRs … are accurate" | ROLE §3.2.2 | A maintenance duty, not a creation trigger |

## 1.2 Sub-questions, answered from the evidence above

| Sub-question | Finding |
|---|---|
| Do semantic decisions require an ADR? | **Not stated anywhere.** No source names "semantic decision" as an ADR trigger. The named triggers are "architectural decision **embedded** in a Major Change" (E-1) and "constitutional constant change" (E-7). |
| Do conflicting decisions require an ADR? | **Not stated.** No source ties conflict resolution to ADR creation. |
| Can an ADR establish ARI semantics? | **Contested.** E-3 says an ADR records a decision already made; GOV-001 §5.2 places ADR creation *after* RFC acceptance. Under AURA-CON-001 Art. V, ADRs sit below APS-100. No source grants an ADR normative force over implementations. |
| Is a SPEC amendment alone sufficient? | **Cannot be determined** — the SPEC class has no in-force approval authority (`07_FORMAL_ARTIFACT_ANALYSIS.md` A-5). |
| Are ADR and SPEC amendment complementary? | Under GOV-001 §5.2 the ADR complements the **RFC-driven APS change**, not a SPEC change. The corpus does not describe an ADR + SPEC pairing except in the PROPOSED model (E-10). |

## 1.3 OQ-A-007 — finding

# CONDITIONALLY REQUIRED

Precisely:

| Route | ADR requirement | Evidence |
|---|---|---|
| Specification-corpus Major Change (RFC route) | **Required only if** an architectural decision is embedded in the change | GOV-001 §5.2 step 8 (E-1) |
| Specification-corpus PATCH lane | **Explicitly not required** | GOV-001 §5.1 (E-2) |
| Implementation-corpus constitutional-constant change | **Required** — "Create ADR documenting the change" is a mandatory step of the framework | ROLE §4.2 Step 4 (E-7) |
| Any route, as the act that *makes* the decision | **Not supported** — an ADR records; an RFC proposes | CONTRIBUTING `:70` (E-3) |

**Two conditions are themselves unresolved:** which route applies depends on `ARI-D-001` and on
the hierarchy conflict (`02`, `04`); and if an ADR is created, **which namespace it belongs to is
undetermined**, with `ADR-001` already carried by three files (`07_FORMAL_ARTIFACT_ANALYSIS.md`
§3.1).

---

# PART 2 — OQ-A-008: IS A SPEC-002 AMENDMENT REQUIRED?

**Required result:** dependency determination
**Method constraint:** do not assume that because SPEC-002 discusses adjacent matters, every
semantic decision must modify it.

## 2.1 Four dependency types kept separate

### 2.1.1 Logical dependency — does an ARI decision *entail* a SPEC-002 change?

| Test | Finding |
|---|---|
| Does SPEC-002 govern ARI? | **No.** Its stated scope (§2.1) is the Constitution Artifact / Vector contract surface: source boundary, canonicalization, embedding, numeric representation of **vector values**, identities, hash domains, serialization, registration, freeze. ARI is not named anywhere in it. |
| Does any ARI decision fall inside a SPEC-002 requirement? | **Possibly one region.** REQ-002-014 / AD-CA-007 govern "one numeric representation for **vector values**, including domain, width, sign, scale, rounding behavior, overflow behavior, and byte order". Whether ARI operands and outputs are "vector values" in that sense is **unresolved** — recorded as U-2 in `review/2026-08-12_RD1_ARI_DECISION_READINESS/05_DEPENDENCY_GRAPH.md` §4. |
| If they are? | Then `ARI-D-007`, `ARI-D-008`, `ARI-D-011` and `ARI-D-021` would be **inside** AD-CA-007's domain, and deciding them without SPEC-002 would create two numeric contracts. |
| If they are not? | Then no logical dependency exists, and the two numeric contracts must merely be kept consistent where they meet. |

**Logical dependency: CONDITIONAL on U-2, which is open.**

### 2.1.2 Procedural dependency — does the process require amending SPEC-002?

| Test | Finding |
|---|---|
| Is SPEC-002 in any change process? | **No.** GOV-001 §5.1/§5.2 name PRs, RFCs, ADRs and APS documents. SPEC is absent from the process description. |
| Who may amend SPEC-002? | **EVIDENCE GAP.** GOV-001 §2's approval list excludes SPEC; POL-VER-001 §1's scope list excludes SPEC; the only assignment (Protocol Custodian) is in a PROPOSED ADR. SPEC-002's own header records `Owner: Protocol Custodian` — an ownership field, not an approval grant. |
| Would amending it change anything today? | **No.** "Normative effect: NONE until APPROVED" (`SPEC-002:11`). Editing a document with no normative effect produces no normative result. |

**Procedural dependency: NOT ESTABLISHED — and the amendment path itself is an EVIDENCE GAP.**

### 2.1.3 Normative dependency — does an ARI decision have force only if SPEC-002 carries it?

| Test | Finding |
|---|---|
| Does SPEC-002 claim exclusive coverage of any ARI question? | **No.** It states the opposite about its own force: normative effect NONE; "SPEC-002 READINESS STATUS: NOT READY" (`:543`); all twelve AD-CA domains UNRESOLVED. |
| Does anything else make SPEC-002 a precondition? | **No source.** `BRIEF_DR-002.md` (non-normative review record) notes the nearest tracked equivalent to the identifier `DR-002` is the AD-CA set, and explicitly declines to assert the mapping. |

**Normative dependency: NOT ESTABLISHED.**

### 2.1.4 Documentation dependency — would SPEC-002 become inconsistent if ARI were decided elsewhere?

| Test | Finding |
|---|---|
| Could a decided ARI numeric contract contradict SPEC-002's candidate list? | **Yes, visibly.** SPEC-002 `:108` lists `32`, `100000`, `signed int32`, `little-endian`, `round-half-to-even` as candidates and states none is a default. If a numeric contract were decided elsewhere, SPEC-002 would still describe the same domain as unresolved. |
| Does the corpus require such inconsistencies to be repaired? | CONTRIBUTING PR requirements demand traceability-matrix updates and `Last Review` updates for **normative documents**; SPEC-002's status makes its classification here uncertain. |

**Documentation dependency: LIKELY, but the repair obligation is not established for a DRAFT
document with declared zero normative effect.**

## 2.2 OQ-A-008 — finding

# UNRESOLVED — no established requirement, and no established amendment path

- **Not "required":** no source makes a SPEC-002 amendment a precondition for any ARI decision,
  and SPEC-002 currently has no normative effect to amend.
- **Not "not required":** if U-2 resolves such that ARI operands are "vector values", four ARI
  decisions fall inside AD-CA-007 and a divergence would be created by deciding them separately.
- **Additionally blocked:** even if an amendment were wanted, **no in-force source states who may
  approve a SPEC document** (`07_FORMAL_ARTIFACT_ANALYSIS.md` A-5). This is recorded as
  `OQ-A-GAP-005`.

---

# PART 3 — OQ-A-009: AUTHORITATIVE WORKFLOW

**Required result:** documented workflow
**Method constraint:** do not invent missing steps.

## 3.1 The three documented workflows

### W-1 — Specification corpus, Major Change (GOV-001 §5.2)

| Step | Actor | Authority | Artifact | Required approval | Gate | Evidence | Status |
|---|---|---|---|---|---|---|---|
| 1 Open an RFC in `/rfcs/` | Proposer | Contributor right | RFC-NNN | — | — | RFC file | **Never exercised** — `rfcs/README.md:16` |
| 2 RFC enters DRAFT | Proposer | — | RFC status | — | — | — | — |
| 3 Comment period ≥14 days | Community | — | PR thread | — | Time gate | PR comments | — |
| 4 Architecture Review Board assessment | ARB | GOV-001 §2 | ARR (§8) | ARB vote (§7 step 7) | Review gate | ARR file | **ARB has no roster, charter, or instance; zero ARRs exist** |
| 5 Chief Architect approval | Chief Architect | GOV-001 §2, §7 step 8 | approval record | **Yes** | Approval gate | — | Actor never identified (`03_…MATRIX.md` §4) |
| 6 RFC → APPROVED | — | — | RFC status | — | — | — | — |
| 7 Implementation via PR referencing RFC | Contributor | — | PR + APS change | merge (actor unassigned outside the PATCH lane) | Merge gate | commit | — |
| 8 ADR created if an architectural decision is embedded | Decision author | GOV-001 §3 | ADR-NNN | acceptance = merge | — | ADR file | Namespace collision risk |

### W-2 — Implementation corpus, agent workflow (AGENTS.md / CLAUDE.md / `docs/conformance/README.md`)

```
Protocol Specification → Protocol Invariants → Conformance Test Matrix → Conformance Gap
→ Implementation → CI evidence → Adversarial review → Human approval
```

| Step | Actor | Authority | Artifact | Approval | Status |
|---|---|---|---|---|---|
| Protocol Specification | — | — | APS-001 | — | **WORKFLOW GAP — the first step's input does not exist** (`APS-001:5` `Status: TODO`) |
| Protocol Invariants | — | — | APS-100 | — | Exists, 1.0-DRAFT |
| Conformance Test Matrix | — | — | APS-400 | — | Exists, all tests DRAFT |
| Conformance Gap | Claude (per CLAUDE.md scope) | tier 6 document | gap analysis | — | Exercised (`docs/GAP-001.md`, prior review packages) |
| Implementation | Copilot (AGENTS.md rule 12) | tier 6 | code | — | — |
| CI evidence | CI | — | check outputs | — | Exercised (`scripts/run_all_checks.sh`) |
| Adversarial review | unnamed | — | review record | — | **No named actor** |
| Human approval | "Human" (rule 13) / "human/Protocol Custodian" (`:53`) | tier 6 | — | **Yes** | **Actor ambiguous; no instance recorded** |

### W-3 — Implementation corpus, Custodian change control (Decree Art. VI, X; ROLE §4.1, §4.2)

| Step | Actor | Authority | Artifact | Gate | Status |
|---|---|---|---|---|---|
| Entropy Risk Assessment — 5 questions | Custodian | ROLE §4.1 | — | **Gate 1** (fixes a critical issue?) then **Gate 2** (preserves bit-identity? NO/UNCERTAIN → REJECTED) | Defined |
| Mandatory checks (bit-identity, integer-only, layer separation, audit trail, entropy) | Custodian / CI | Decree Art. VI | check output | Reject on failure | Partially automated |
| Compliance certification with "Custodian Signature: [Required for `core/` changes]" | Custodian | Decree Art. X | signature | **Merge gate** | **No signature instance exists** |
| Constitutional Amendment Framework (5 steps) — for constants only | Custodian | ROLE §4.2 | new instrument + ADR + SHA-256 + M-DISC | new-instrument gate | Never exercised |

## 3.2 Workflow gaps

| ID | Gap | Evidence |
|---|---|---|
| **WG-1** | W-2 begins with "Protocol Specification", which does not exist | `APS-001:5,12` |
| **WG-2** | W-1 requires an ARB with no established existence and produces ARRs of which there are none | GOV-001 §2, §8; no `ARR-*` file |
| **WG-3** | W-1's merge actor is unassigned outside the PATCH lane | GOV-001 §5.1 vs §5.2/§6 |
| **WG-4** | W-3's mandatory Custodian signature has never been produced | Decree Art. X; verified absent |
| **WG-5** | **No step in any workflow transfers a decision from one corpus to the other.** Nothing describes how an implementation-corpus decision is recorded in the specification corpus, or the reverse | absence across GOV-001, CONTRIBUTING, Decree, ROLE, AGENTS.md |
| **WG-6** | No workflow covers the SPEC document class | `07_FORMAL_ARTIFACT_ANALYSIS.md` A-5 |
| **WG-7** | "Adversarial review" (W-2) names no actor, artifact, or acceptance criterion | AGENTS.md; `docs/conformance/README.md` |
| **WG-8** | Neither W-1 nor W-2 states where **conformance evidence** must be published for a claim to count | APS-400 §6 defines a report; no workflow step requires it |

## 3.3 Workflow conflicts

| ID | Conflict |
|---|---|
| **WC-1** | **Direction of authority.** W-1 and CONTRIBUTING `:11` run Specification → Implementation. `docs/specs/AUDIT_LAYER_SPEC.md` (implementation corpus, self-declared FROZEN) states the reverse: "Implementation is the source of truth. If this document conflicts with the implementation, the implementation governs and this document must be corrected." Recorded by R-01 §8 CASE F and re-verified. |
| **WC-2** | **Gate 1 vs Gate 2.** ROLE §4.1 Gate 1 admits corrections of mathematical errors; Gate 2 rejects any change that does not preserve bit-identity. A correction that changes output cannot satisfy both. Recorded by R-01 §4.5 as CONTRADICTED; not reopened here. |
| **WC-3** | **Approval actor.** W-1 names the Chief Architect; W-2 names "Human / Protocol Custodian"; W-3 names the Custodian. No document relates them (`03_…MATRIX.md` §4). |
| **WC-4** | **ADR acceptance.** GOV-001 §6 "merging = accepting" vs ADR-001_DOCUMENT_MODEL `:55` "Architecture Board approves … ADRs" (PROPOSED). |

## 3.4 OQ-A-009 — finding

# PARTIALLY DOCUMENTED — with one structural gap that no source fills

- **Documented:** three workflows exist with actors, artifacts and gates specified in text
  (W-1, W-2, W-3 above).
- **Not documented (WG-5):** the step that would carry a decision **between the two corpora** —
  which is exactly the step an ARI decision needs, because the decision would be made under one
  corpus's authority and would have to bind artifacts governed by the other.
- **Not operational:** every approval gate in W-1 and W-3 has either an unidentified actor, a
  non-existent body, or no instance ever produced.

**No missing step is invented here.** The gap is reported as a gap.

---

*This document has no normative effect. It records procedural determinations and workflow
evidence. It selects no artifact class, no actor, and no process, and it invents no step.*
