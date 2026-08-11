# 00 — Review Scope and Evidence Base

Document ID: REV-2026-08-11-000
Status: DRAFT — ANALYSIS ARTIFACT, NO NORMATIVE EFFECT
Classification: Architecture / Conformance Review Input Record
Author: Claude (architectural & conformance audit role, per CLAUDE.md)
Date: 2026-08-11
Authority: subordinate to AURA Constitution v1.0 (FROZEN) → APS-001 → APS-100 → GOV-001

---

## 0. Normative effect

**NONE.** This document and every document in this review package is an analysis
artifact. No document here approves, accepts, freezes, registers, or supersedes
anything. No AD-CA decision domain is resolved by this package. Per GOV-001 §9 and
AURA Constitution Article VIII, the AI author of this package may not approve or
freeze canonical documents and has not attempted to.

---

## 1. Why this document exists

The review task supplied a list of input artifacts (§3 of the task) and asserted a
project state. Before reviewing anything, that asserted state was checked against
the actual repositories. **It does not match.** Several named inputs do not exist,
one named input is ambiguous between two repositories, and one grouping in the task
statement contradicts the authoritative text of SPEC-002 v0.3.

Per the task's own Rule 20 ("Nie 'naprawiaj' historii projektu") and Rule 3 ("Nie
zakładaj, że wszystkie materiały są aktualne tylko dlatego, że istnieją"), the
divergence is recorded here rather than silently reconciled. Recording it first is
also required by CLAUDE.md: *"If a conflict is detected: do not silently reconcile
it; stop; report the conflict; request human/Protocol Custodian resolution."*

---

## 2. Evidence base actually inspected

| # | Source | Revision / state at review time | Role assigned in this review |
|---|--------|--------------------------------|------------------------------|
| S1 | `github.com/AuraIDToken/aura-specification` @ `62d2d6b` (`main`) | shallow clone, 2026-08-10 push | **Treated as the specification repository of record for this review** |
| S2 | `github.com/aura-nomos/aura-specification` @ `eb2a4ec` (`main`) | contains only `README.md` (11 bytes) + `.github/CODEOWNERS` | Empty stub; push target for this review package |
| S3 | `github.com/AuraIDToken/aura-poc-a-core-v3.3` @ `9c6a5d8` (`main`) | full clone | RI-PY implementation under review |
| S4 | `github.com/AuraIDToken/aura-guard-v1.3` @ default HEAD | shallow clone | RI-RS implementation under review |

Documents read in full from S1: `specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md`,
`GOVERNANCE.md`, `templates/ADR_TEMPLATE.md`, `constitution/AURA_CONSTITUTION.md`,
`aps/APS-000`, `aps/APS-100`, `aps/APS-200`, `aps/APS-300`, `aps/APS-400`, `aps/APS-500`,
`aps/APS-950`, `specification/APS-001`, `invariants/INVARIANT_REGISTRY.md`,
`adrs/ADR-001_DOCUMENT_MODEL.md`, `adrs/ADR-001_REPOSITORY_STRUCTURE.md`, `adrs/README.md`,
`docs/adr/001-document-model.md`, `VERSIONING.md`, `compliance/TRACEABILITY_MATRIX.md`,
`compliance/ARC_TO_SPEC_MAPPING.md`, `compliance/arc_to_spec_mapping.yaml`, `arc/README.md`,
`conformance/CONF-003`, `fixtures/core/FIX-001_BASIC_EVALUATION.json`,
`reference/RI-PY_AURA_POC_A_CORE.md`.

Source read from S3: `core/embedding.py`, `core/evaluator.py`, `core/offline_normalizer.py`,
`CONSTITUTIONAL_DECREE.md`, `AGENTS.md`, `CLAUDE.md`, `docs/architecture.md`, `docs/GAP-001.md`.

Source read from S4: `src/normalizer.rs`, plus repository-wide symbol search.

---

## 3. Input artifacts that DO NOT EXIST

> **EVIDENCE GAP — E-GAP-001 (P0).**

| Task-asserted input | Actual state | Verification |
|---|---|---|
| **ADR-002 … ADR-006 DRAFT PACKAGE** | **DOES NOT EXIST** in any form | `adrs/` contains exactly two files plus README. No `ADR-002`…`ADR-006` on `main`, nor on any of the 22 remote branches of S1 (`git ls-remote --heads`). No file, no draft, no branch. |
| APS-100 / APS-200 "if present" | Present, but all `1.0-DRAFT` / Status DRAFT | S1 `aps/` headers |
| ARC-xxx baselines | **NONE EXIST.** `arc/` holds only a README; `compliance/arc_to_spec_mapping.yaml` is `mappings: []` | S1 |
| Fixtures | **NONE USABLE.** `FIX-001` is a placeholder whose every data field is the literal string `"TODO"` | S1 `fixtures/core/FIX-001_BASIC_EVALUATION.json` |
| CR-007 | **NOT DEFINED ANYWHERE.** S3 defines CR-001, CR-003, CR-004 only. SPEC-002 calls CR-007 "BLOCKED" but no document defines what CR-007 *is* | repo-wide grep of S1+S3 |

**Consequence.** The task's First Goal — "audit ADR-002…ADR-006" — has no object. This
review therefore does **not** fabricate five ADRs and then review the fabrication.
Instead, `01_ADR_REVIEW.md` applies the 14 review criteria to the **decision domains**
those ADRs are said to carry, using the only authoritative record of those domains
that exists: **SPEC-002 v0.3 §6**. Every finding is anchored to text that is actually
in the repository.

---

## 4. CONFLICT DETECTED — task grouping vs. SPEC-002 §6

**Source A** — task statement §1: `ADR-003` covers "AD-CA-005 — vector projection mechanism".

**Source B** — SPEC-002 v0.3 §6, row AD-CA-005: *"Embedding method identity and versioning
model. Candidate: `Dictionary-Based Embedding`."*

**Nature of conflict.** These are different decision domains. "Embedding method identity
and versioning" is a *dependency-identification* decision (which named, versioned method is
authoritative). "Vector projection mechanism" is an *algorithm-definition* decision (what
transform maps input to vector components). SPEC-002 places the algorithmic pipeline under
AD-CA-003 and the *numeric* contract under AD-CA-007; it never uses the term "projection".

**Impact.** If ADR-003 is authored to the task's wording, it will silently redefine
AD-CA-005 away from its SPEC-002 meaning, and AD-CA-005's actual subject matter
(method identity + versioning, feeding REQ-002-012) will be left with no owning ADR.
This is precisely the "silent reinterpretation of protocol semantics" that CLAUDE.md
places out of scope and AGENTS.md rule 2 prohibits.

**Required decision.** Protocol Custodian MUST state whether AD-CA-005 means (a) embedding
method identity/versioning as written in SPEC-002 §6, (b) the projection algorithm, or
(c) both — in which case AD-CA-005 MUST be split before any ADR is authored against it.
Tracked as **OD-002**.

---

## 5. Verification of AD-CA-004 and AD-CA-006 (task §1 explicitly required)

The task required these two be verified against the current SPEC-002/repository audit and
**not** filled in by assumption. Verified:

**AD-CA-004 — EXISTS.** SPEC-002 §6 row 4: *"Normalization rules affecting deterministic
output. UNRESOLVED. None approved. Blocks REQ-002-011, REQ-002-021, REQ-002-022."*
Also listed in Appendix A(E). **Status: UNRESOLVED, and assigned to NO ADR in the task's
five-ADR grouping.**

**AD-CA-006 — EXISTS.** SPEC-002 §6 row 6: *"Dictionary identity, versioning, integrity,
change policy, and complete dependency closure of all external or auxiliary inputs capable
of affecting canonical artifact, vector, bytes, or hash. UNRESOLVED. Blocks REQ-002-013,
REQ-002-016, REQ-002-024, REQ-002-034."* Also §4.7b and Appendix A(E).
**Status: UNRESOLVED, and assigned to NO ADR in the task's five-ADR grouping.**

> **FINDING F-ORPHAN (P0).** The five-ADR package covers 10 of 12 decision domains.
> AD-CA-004 and AD-CA-006 are **orphaned**. Both are load-bearing:
> AD-CA-004 blocks REQ-002-021/022 (canonical serialization + canonical byte sequence) — the
> same requirements ADR-004 is meant to close via AD-CA-008. AD-CA-006 blocks REQ-002-034
> (dependency closure) — without which "same source → same vector" is unprovable, because an
> undeclared dependency may vary.
> **Therefore ADR-004 cannot close REQ-002-021/022 while AD-CA-004 is unresolved, and no ADR
> in the package can close REQ-002-034 at all.** The package as scoped cannot reach its own
> stated goal. Tracked as **BLOCKER-P0-004**.

---

## 6. CONFLICT DETECTED — two repositories named `aura-specification`

**Source A.** Task statement §1: *"Repozytorium specyfikacji: AuraIDToken/aura-specification."*
**Source B.** Session repository scope and the working clone: `aura-nomos/aura-specification`.

Both exist and both are writable by this account. S1 holds the entire specification corpus.
S2 holds an 11-byte README and a CODEOWNERS file whose paths (`/constitution/`, `/aps/`,
`/governance/`) mirror S1's layout, indicating an intended migration target that was never
populated.

**Nature of conflict.** Two repositories claim the same canonical name. Neither declares
which is authoritative, and no `supersedes` relation exists between them.

**Impact.** Directly defeats REQ-002-003 (Source Document Identity: *"the immutable
identifier, version, status, and **repository location** of each document in the Source
Set"*). If the Source Set is to include Constitution or APS documents, "which repository"
is unanswerable today, so AD-CA-001 cannot be resolved even in principle.

**Required decision.** Protocol Custodian MUST designate exactly one authoritative
repository and record the other's status (mirror / superseded / abandoned).
Tracked as **OD-001**, **BLOCKER-P0-001**.

**Handling in this review.** S1 is used as the evidence base because it is the only one
with content. This is an *evidentiary* choice for review purposes and explicitly **does
not** constitute a normative designation.

---

## 7. Artifact classification applied throughout this review

Per task §3, every referenced item is classified. Summary of what was found:

| Class | Items found |
|---|---|
| **canonical + frozen** | `AURA_CONSTITUTION.md` (AURA-CON-001 v1.0 FROZEN) — the *only* frozen normative document in S1 |
| **approved** | `ADR-001_REPOSITORY_STRUCTURE.md` (ACCEPTED) — scope is directory layout only |
| **draft** | GOV-001 v1.0-DRAFT; APS-000/100/200/300/400/500/900/950 all 1.0-DRAFT; INV registry 1.0-DRAFT; VERSIONING 1.0-DRAFT; CONF-001…010 all 1.0-DRAFT; SPEC-002 v0.3-DRAFT |
| **placeholder / TODO** | APS-001 (Status: **TODO**, body is entirely `> **TODO**` stubs); FIX-001; `arc/`; `arc_to_spec_mapping.yaml` |
| **implementation** | RI-PY (S3), RI-RS (S4) — both **NOT CERTIFIED** per `reference/RI-PY_AURA_POC_A_CORE.md` |
| **evidence** | none that bears on the Constitution Artifact; S3's determinism reports cover ARI replay only |
| **historical/deprecated** | root `*.txt` / `*.pdf` originals in S1; `core/policy.py`, `core/consistency.py` in S3 (deprecated wrappers) |

> **FINDING F-ROOT (P0).** `APS-001` — the root normative specification, placed directly
> under the Constitution by **Constitution Article V** and cited as the Authority of
> APS-100/200/300/400/500/950 — has **Status: TODO** and contains no normative content.
> The entire normative chain is anchored to an empty document. SPEC-002 §11 already
> acknowledges this ("APS-001 remains incomplete"), and this review confirms it is not
> merely incomplete but **absent**. Every downstream "Authority: APS-001" header in S1 is
> a dangling reference. Tracked as **BLOCKER-P0-002**.

---

## 8. What this review can and cannot conclude

**Can conclude:** whether the *contract surface* in SPEC-002 v0.3 is sound, complete, and
independently implementable; whether the repository's governance artifacts are internally
consistent; whether the implementations conflict with the future contract; and what must be
decided, by whom, before anything can advance.

**Cannot conclude:** anything about the content of ADR-002…ADR-006, because they do not
exist. Any statement in this package about those ADRs is a statement about the *decision
domains they are proposed to carry*, never about their (nonexistent) text.

---

*End of 00_REVIEW_SCOPE_AND_EVIDENCE_BASE.md*
