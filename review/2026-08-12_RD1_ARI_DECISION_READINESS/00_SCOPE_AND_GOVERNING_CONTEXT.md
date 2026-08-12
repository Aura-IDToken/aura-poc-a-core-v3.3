# 00 — SCOPE AND GOVERNING CONTEXT

**Package:** RD-1-ARI-DECISION-READINESS
**Date:** 2026-08-12
**Mode:** DECISION PREPARATION — evidence classification only
**Normative effect:** NONE

---

## 1. What this package is

This package answers exactly one question:

> **What must Aura formally decide before ARI can become a normative, cross-language,
> independently verifiable algorithm?**

It is a *map of the decisions*, not a solution to any of them.

## 2. What this package is NOT

It is **not** an implementation task, **not** a remediation task, **not** an ADR, **not** a
specification amendment, and **not** a re-audit of the Markdown/PDF corpus.

**No ARI semantic value is selected anywhere in this package.** No formula, rounding mode,
division rule, dimension, bound, malformed-input behaviour, similarity model, drift model,
overflow behaviour, serialization, or reference implementation is chosen, ranked, preferred,
or recommended.

---

## 3. Governing RD-1 verdict (CLOSED — not reopened)

RD-1 and its PDF closures are **CLOSED**. The authoritative audit verdict is carried forward
verbatim as the governing premise of this package:

# NO NORMATIVE ARI DEFINITION FOUND

RD-1 established:

| # | RD-1 finding | Carried forward as |
|---|---|---|
| 1 | The specification corpus contains no normative ARI definition | PREMISE |
| 2 | The Constitution does not define, constrain, or delegate ARI | PREMISE |
| 3 | APS-100 does not define ARI semantics | PREMISE |
| 4 | APS-200 does not define the mathematical semantics | PREMISE |
| 5 | APS-950 RI-PY is a registry/reference entry, not a normative definition | PREMISE |
| 6 | The conformance corpus does not provide an authoritative ARI value | PREMISE |
| 7 | The fixture corpus contains no normative ARI fixture instance | PREMISE |
| 8 | The implementation currently provides observable ARI behaviour | PREMISE |
| 9 | That implementation behaviour is NOT normative authority | PREMISE |

**RD-1 was not reopened.** No step in this package required contradicting the verdict, and no
direct, previously unknown contradiction was encountered that would make the decision package
impossible to construct. Where this package cites specification material, it does so to
classify *what exists and with what status* — never to re-derive the RD-1 verdict.

### 3.1 Unresolved semantic questions — NOT accepted defects

The following are treated throughout this package as **unresolved semantic questions**, never
as already-established defects requiring immediate remediation:

Python `//` versus truncation toward zero · `round()` / half-to-even · ARI bounds ·
1-element versus 1536-element vectors · empty vectors · `zip()` behaviour on mismatched
dimensions · malformed input · similarity model · drift · overflow/range behaviour ·
multiple ARI engines/models · serialization implications.

Where earlier repository review material classified any of these as an "ENGINEERING BUG",
that classification is reported as **the cited source's own classification**, attributed to
that source, and is not adopted by this package.

---

## 4. Hard boundaries observed

| # | Boundary | Observed |
|---|---|---|
| 1 | No re-audit of the complete Markdown/PDF corpus | YES — targeted reads only, enumerated in §6 |
| 2 | RD-1 treated as CLOSED evidence finding | YES |
| 3 | RD-1 verdict not reopened | YES |
| 4–15 | No ARI semantic value, formula, rounding mode, division semantics, dimensionality, bounds, malformed-input behaviour, similarity model, drift model, overflow behaviour, serialization, or reference implementation selected | YES |
| 16 | `core/evaluator.py` not modified | YES |
| 17 | No production code modified | YES |
| 18 | SPEC-002 not modified | YES |
| 19 | No fixtures created or modified | YES |
| 20 | No ADR created | YES |
| 21 | RI-PY not treated as normative authority | YES |
| 22 | No normative semantics inferred from implementation behaviour | YES |
| 23 | No characterization observation converted into an expected normative value | YES |
| 24–28 | `//` vs truncation, `round()`, `zip()`, ARI bounds, malformed-input handling — none fixed | YES |
| 29 | No independent implementation created | YES |
| 30 | No PR created | YES |
| 31 | Nothing merged | YES |
| 32 | Governance unchanged | YES |

---

## 5. Explicit statement of non-decision

> **This package makes no semantic decision about ARI.**
>
> It discovers decision points, classifies existing evidence, identifies candidate semantics
> as **NON-NORMATIVE CANDIDATE**, identifies consequences without ranking them, identifies
> dependencies, identifies evidence requirements, records contradictions, and formulates
> decision questions.
>
> Every question in this package remains open at the end of it.

Terms **preferred, best, correct, optimal, should select, recommended** appear in this package
only inside quotations explicitly attributed to an existing source, and are labelled
source-derived at the point of use.

---

## 6. Evidence sources used (targeted, not exhaustive)

### 6.1 Repository states

| Repository | Resolution | State |
|---|---|---|
| `AuraIDToken/aura-poc-a-core-v3.3` | local checkout, working tree | branch `claude/ari-decision-readiness-aryxo5`, based on `origin/main` @ `f3a87cc` |
| `AuraIDToken/aura-specification` | read-only clone (anonymous git read) | HEAD @ `62d2d6b` (2026-08-10, "docs(spec-002): SPEC-002 v0.3-DRAFT") |
| `aura-nomos/aura-specification` | local checkout | `main` @ `eb2a4ec` — contains only `README.md` (one line) and `.github/CODEOWNERS`. **Contributes no evidence.** |

> **Provenance note.** The specification-corpus evidence in this package comes from
> `AuraIDToken/aura-specification` @ `62d2d6b`. The session-attached
> `aura-nomos/aura-specification` repository is empty of governance content and is recorded
> here so that no reader mistakes one for the other.

### 6.2 Documents read for this package

**Specification corpus** (`aura-specification` @ `62d2d6b`):
`specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` ·
`specification/APS-001_PROTOCOL_SPECIFICATION.md` · `aps/APS-100_PROTOCOL_INVARIANTS.md` ·
`aps/APS-200_CANONICAL_DATA_MODEL.md` · `aps/APS-400_CONFORMANCE_TEST_MATRIX.md` ·
`aps/APS-500_REFERENCE_FIXTURES.md` · `aps/APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md` ·
`conformance/CONF-001_DETERMINISTIC_EVALUATION.md` · `conformance/CONF-007_FAIL_CLOSED.md` ·
`invariants/INVARIANT_REGISTRY.md` · `compliance/TRACEABILITY_MATRIX.md` ·
`glossary/GLOSSARY.md` · `reference/RI-PY_AURA_POC_A_CORE.md` ·
`constitution/AURA_CONSTITUTION.md` · `fixtures/core/FIX-001_BASIC_EVALUATION.json`

**Implementation corpus** (`aura-poc-a-core-v3.3` @ `f3a87cc`):
`core/evaluator.py` · `core/offline_normalizer.py` · `core/embedding.py` · `core/merkle.py` ·
`compliance/consistency.py` · `compliance/policy.py` · `compliance/evaluator_wrapper.py` ·
`compliance/certificate.py` · `audit/merkle.py` · `init.sql` ·
`docs/mathematical_foundation.md` · `docs/ADR_005_NO_FLOAT_RUNTIME.md` ·
`docs/KNOWN_LIMITATIONS.md` · `CONSTITUTIONAL_DECREE.md` ·
`.github/github/copilot-instructions.md` · `.github/copilot-instructions.md` ·
`core/test_ari.py` · `core/test_ari_observability.py` ·
`review/2026-08-11_ENGINEERING_BASELINE/` (prior review records — non-normative)

### 6.3 Evidence-class vocabulary

| Class | Meaning |
|---|---|
| **NORMATIVE** | An existing source genuinely holds normative authority for that specific domain, in force, with scope covering it |
| **DISPUTED AUTHORITY — SCOPE UNRESOLVED** | A source asserts binding force, but whether its scope reaches normative cross-language ARI is itself undecided. **This is not a NORMATIVE entry.** |
| **NON-NORMATIVE CANDIDATE** | A concrete value, algorithm, or model exists in repository material without authority to establish it |
| **UNRESOLVED** | No decision exists in any source |
| **ABSENT** | The corpus is silent |
| **CONTRADICTED** | Two sources state incompatible things and neither is subordinated to the other |

No entry in this package is labelled NORMATIVE for any newly proposed ARI semantic.

---

## 7. Authority frame applied

Two authority ladders exist and are **not unified by either corpus**. Both are recorded; neither
is selected as governing.

**Specification corpus** — `aura-specification/constitution/AURA_CONSTITUTION.md`
(AURA-CON-001 v1.0, **FROZEN**) Article V:

```
AURA Constitution → APS-001 → APS-100 → ADR/ARR/RFC → Playbook → Repository Documentation → Implementation
```

> "A higher-level document has authority over a lower-level document in all cases of conflict."
> — AURA-CON-001 Article V

**Implementation corpus** — `aura-poc-a-core-v3.3/CLAUDE.md` "Authority Precedence":

```
1 Constitutional Decree / Constitutional Authority → 2 Aura Protocol Specification →
3 Protocol Invariants → 4 repository constitutional/Copilot directives →
5 Conformance Test Matrix / approved Conformance Requirements → 6 AGENTS.md / CLAUDE.md →
7 path-specific agent instructions → 8 prompt/task instructions → 9 existing implementation →
10 agent assumptions
```

**Recorded fact, not resolved here:** the two ladders order the same artifacts differently, and
neither corpus cites the other. Which ladder governs an ARI decision is itself an open question
(see `09_OPEN_QUESTIONS.md`, OQ-A).

---

## 8. Package contents

| File | Purpose |
|---|---|
| `00_SCOPE_AND_GOVERNING_CONTEXT.md` | this document |
| `01_ARI_DECISION_REGISTER.md` | one identifier per semantic question (ARI-D-nnn) |
| `02_DECISION_DOMAIN_MATRIX.md` | one row per decision domain |
| `03_NON_NORMATIVE_CANDIDATES.md` | every candidate found in repository material |
| `04_CONSEQUENCE_MATRIX.md` | consequences per alternative — no ranking |
| `05_DEPENDENCY_GRAPH.md` | which decisions depend on which |
| `06_EVIDENCE_REQUIREMENTS.md` | evidence needed to make each decision defensible |
| `07_CONFORMANCE_AND_REFERENCE_MODEL.md` | requirements a future reference model / suite must satisfy |
| `08_TWO_KEY_DECISION_PROTOCOL.md` | the two-key process |
| `09_OPEN_QUESTIONS.md` | unresolved questions in decision-ready language |
| `10_DECISION_BRIEF.md` | executive brief and final status |

---

*This document has no normative effect. It selects no ARI semantics, creates no ADR, amends no
specification, and modifies no code.*
