# 10 — DECISION BRIEF

**Package:** RD-1-ARI-DECISION-READINESS
**Date:** 2026-08-12
**Prepared for:** KEY 1 — Human Architectural Authority · KEY 2 — ChatGPT architectural review
**Normative effect:** NONE

---

## 1. The question this package answers

> What must Aura formally decide before ARI can become a normative, cross-language,
> independently verifiable algorithm?

**Answer, in one line:** **27 decisions across 20 domains, none of them made, resting on 4 prior
questions about who decides — with 12 recorded contradictions to resolve along the way.**

This package maps those decisions. It makes none of them.

---

## 2. Starting point (carried, not re-derived)

RD-1 is **CLOSED**. Its verdict — **NO NORMATIVE ARI DEFINITION FOUND** — is the premise of this
work and was not reopened. No contradiction encountered made the package impossible to construct.

The specification corpus's only statement about ARI defines it by deferring to an implementation
(`aura-specification/glossary/GLOSSARY.md:27-28`), and the root specification that would define
protocol behaviour carries `Status: TODO` (`aura-specification/specification/APS-001_PROTOCOL_SPECIFICATION.md:5`).

---

## 3. What the decision space looks like

| | Count |
|---|---|
| Decision domains | 20 |
| Decisions identified (`ARI-D-001` … `ARI-D-027`) | **27** |
| Decisions made | **0** |
| Prior questions about jurisdiction (`OQ-A` … `OQ-D`) | 4 |
| Non-normative candidates catalogued (`C-01` … `C-74`) | 74 |
| Candidates selected, ranked, or recommended | **0** |
| Recorded contradictions (`X-A1` … `X-A12`) | 12 |
| Unresolved dependencies (`U-1` … `U-6`) | 6 |
| Domains marked NORMATIVE | **0** |

**Authority status across all 20 domains: UNRESOLVED.** Two domains (Quantization, Drift)
additionally carry **DISPUTED AUTHORITY — SCOPE UNRESOLVED**, because
`aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` Article I §8 asserts binding constants while
`SPEC-002:108` lists the same value as candidate-only. That is a scope question (OQ-B), not a
NORMATIVE entry.

---

## 4. The four things KEY 1 is asked to settle first

These gate everything else. They are not ARI semantics; they determine whose answer counts.

| # | Question | Why first |
|---|---|---|
| **OQ-A** | Which authority ladder governs an ARI decision — the Constitution's Article V hierarchy, or `CLAUDE.md`'s precedence list? | The two place the Constitutional Decree at opposite ends and neither cites the other. |
| **OQ-B** | Does the Decree's Article I bind a protocol-level, cross-language ARI, or only this instrument? | Determines whether the scale factor and sentinel threshold are settled or open. |
| **OQ-C** | Within Article I, what is the relationship between "Q16.16" and "scaling factor 100,000"? | The same article names both; they are different representations. |
| **OQ-D** | Which repository is the authoritative specification corpus? | The session-attached spec repository is empty; all specification evidence came from a different one. |

---

## 5. The critical path

From `05_DEPENDENCY_GRAPH.md`. The graph has **one root** and a **terminal conformance cluster**.

```
ARI-D-001  is ARI a protocol object?          ← single root, nothing precedes it
      ↓
ARI-D-004  input contract
      ↓                    ┌── ARI-D-007 quantization  (independent of dimension)
ARI-D-006  dimension ──────┤
      ↓                    └── ARI-D-008 → ARI-D-009 → ARI-D-010 / ARI-D-011
ARI-D-013  similarity properties
      ↓
ARI-D-014 drift · ARI-D-015 penalty · ARI-D-016 bounds · ARI-D-021 overflow
      ↓
ARI-D-017…020  error / malformed input
      ↓
ARI-D-022  serialization
      ↓
ARI-D-026 equivalence · ARI-D-027 reproducibility · ARI-D-025 fixtures
      ↓
ARI-D-024  conformance contract    ←?→   ARI-D-023 reference model  (direction UNRESOLVED)
```

**Four departures from the illustrative ordering supplied with the task**, each evidence-backed:
identity precedes the input contract (Δ1); dimension and quantization are independent and both
feed overflow (Δ2); similarity precedes division and bounds (Δ3); the reference model's position
relative to conformance is unresolved (Δ4).

---

## 6. Boundary compliance

| Boundary | Status |
|---|---|
| No ARI semantic value, formula, rounding mode, division rule, dimension, bound, malformed-input behaviour, similarity model, drift model, overflow behaviour, serialization, or reference implementation selected | **Observed** |
| No candidate ranked, preferred, or recommended | **Observed** — `03_NON_NORMATIVE_CANDIDATES.md` §0 |
| RD-1 treated as CLOSED and not reopened | **Observed** |
| Implementation behaviour not used as authority | **Observed** — `06_EVIDENCE_REQUIREMENTS.md` §1 |
| RI-PY not treated as normative authority | **Observed** |
| Characterization observations not converted into expected values | **Observed** — `03_NON_NORMATIVE_CANDIDATES.md` §19 |
| No production code, no `core/evaluator.py`, no SPEC-002, no fixtures, no ADR, no PR, no governance change | **Observed** — files created are documentation only, listed in `00_SCOPE_AND_GOVERNING_CONTEXT.md` §8 |
| `//` vs truncation, `round()`, `zip()`, bounds, malformed input — none fixed | **Observed** |

**Tracked production files changed: none. Normative semantics selected: none.**

---

## 7. What this package does not claim

- It does not claim the decision space is complete; KEY 1 is asked to test that
  (`08_TWO_KEY_DECISION_PROTOCOL.md` §5).
- It does not claim any classification is beyond challenge, in particular the
  DISPUTED AUTHORITY marking (OQ-B).
- It does not claim any current behaviour is a defect. The open questions have observable
  consequences; that is not the same as a finding of error.
- It does not claim the implementation may or may not be changed. That governance question was
  recorded as INDETERMINATE by a prior audit and is **not reopened here**.

---

## 8. What happens next

Per `08_TWO_KEY_DECISION_PROTOCOL.md`:

```
decision preparation → human review (KEY 1) → ChatGPT architectural review (KEY 2)
→ explicit mutual acceptance → formalization → implementation
```

Stage 1 is complete. Nothing may be formalized — no specification text, no ADR, no fixture, no
test expectation, no code — until both keys accept the same text for the same decision
identifier.

---

## 9. Final status

# DECISION-READY — HUMAN ARCHITECTURAL REVIEW REQUIRED

*The decision space is mapped, traceable and non-prescriptive. Every one of the 27 decisions
remains open. This package has no normative effect: it selects no ARI semantics, ranks no
candidate, creates no ADR, amends no specification, creates no fixture, and modifies no code.*
