# RD-1-FINAL-PDF — 02 HIGHEST AUTHORITY ASSESSMENT

---

## 1. Assessment per artifact

Authority is **not** inferred from title, status, or self-declared classification (rule R3), and
a formula would **not** be treated as proof of normativity (rule R6).

| Artifact | Self-declared classification | Status | Contains ARI content | Establishes an ARI definition |
|---|---|---|---|---|
| Constitution `AURA-CON-001` | Canonical Governance Document | FROZEN | **No** | **NO** |
| APS-000 Foundation & Terminology | Normative Specification | 1.0-DRAFT | **No** | **NO** |
| APS-100 Protocol Invariants | Normative Specification | 1.0-DRAFT | **No** | **NO** |
| APS-200 Canonical Data Model | Normative Specification | 1.0-DRAFT | **No** | **NO** |
| APS-300 Evidence Model | Normative Specification | 1.0-DRAFT | **No** | **NO** |
| APS-950 Reference Impl. Requirements | Normative Implementation Specification | 1.0-DRAFT | RI-PY registry row only | **NO** |

As in RD-1-PDF, the authority test is **never reached**: five of six documents contain no ARI
content of any kind, and the sixth contains only a registry identifier. A document silent on ARI
cannot define ARI, whatever its authority.

Five of the six self-classify as `Normative` while carrying `Status: DRAFT`. That tension is
recorded, not adjudicated — it does not affect this audit's outcome either way.

## 2. Article V — a correction to RD-1

**This is the one substantive finding in this package beyond the ARI-absence confirmation.**

RD-1 `05_CONFLICTS_AND_CIRCULARITIES.md` recorded conflict **C-4**:

> `CLAUDE.md`'s authority ladder has **no tier for implementation-repository documentation**. […]
> **DECISION REQUIRED — the corpus does not assign implementation-repo documentation an
> authority level.**

**That statement is incorrect.** The Constitution assigns one, in Article V — Canonical
Hierarchy:

```
AURA Constitution
        ↓
Aura Protocol Specification (APS-001)
        ↓
Protocol Invariants (APS-100)
        ↓
ADR / ARR / RFC
        ↓
Aura Development Playbook
        ↓
Repository Documentation          ← level 6 of 7
        ↓
Implementation                    ← level 7 of 7
```

> Dokument wyższego poziomu ma pierwszeństwo przed dokumentem niższego poziomu.
> *(A higher-level document takes precedence over a lower-level document.)*

**Why RD-1 missed it.** RD-1 enumerated ARI-bearing artifacts. `constitution/AURA_CONSTITUTION.md`
contains **zero** ARI tokens, so it never entered the candidate set. The omission did not affect
RD-1's ARI finding — the Constitution is genuinely silent on ARI, exactly as RD-1 reported — but
it did cause RD-1 to answer the *authority-level* question from `CLAUDE.md` alone when the
Constitution answers it directly. Article V is present in **both** the markdown and the PDF; it
was not a PDF-only fact.

### 2.1 What Article V does and does not settle

**Settles:** `docs/mathematical_foundation.md` is *Repository Documentation*, level **6 of 7**.
It is not unranked. It outranks `core/evaluator.py` (Implementation, level 7) and is outranked
by ADR/ARR/RFC (level 4), Protocol Invariants (level 3), the Specification (level 2), and the
Constitution (level 1).

**Does not settle — and this audit does not settle it either:**

- **Article V does not make `mathematical_foundation.md` normative for ARI.** Rule R6 applies:
  possessing a rank in a precedence hierarchy establishes *which document wins in a conflict*,
  not that a document's content constitutes a normative definition. Repository Documentation is
  explicitly subordinate to the three tiers that would carry such a definition — all of which
  are silent on ARI.
- **Article V sharpens RD-1 conflict C-3 without resolving it.** `ADR-005` sits at level 4;
  `mathematical_foundation.md` at level 6. Under Article V, ADR-005 takes precedence — and
  ADR-005 is the artifact whose division claim (*"truncation toward zero"*) does not match the
  implementation's floor division. **This audit does not resolve ADR-005, does not select
  division semantics, and does not recommend a rounding mode.** The precedence fact is recorded
  because it is evidence; its consequences are an architectural decision.

## 3. Article I and Principle 1 versus the glossary delegation

RD-1 recorded circularity **C-1**: the specification glossary defines ARI as *"computed by
RI-PY"*, delegating to an uncertified implementation.

The Constitution states the opposite direction of authority:

- **Article I:** *"Każda implementacja Aura jest jedynie referencyjną realizacją specyfikacji."*
  — every implementation is **merely a reference realization of the specification**.
- **Article IV, Principle 1:** **Specification First.**
- **Article V:** Specification (2) ranks above Implementation (7).

So the corpus's highest authority asserts that specifications determine implementations, while
the specification's own glossary determines ARI by pointing at an implementation.

**Recorded as evidence of tension. Not resolved.** It does not create an ARI definition; it
makes the absence of one more conspicuous, because the delegation that stands in for a
definition runs against the Constitution's stated direction of authority.

## 4. The invariant chain, stated as fact

Assembled from this audit and RD-1-PDF, without inference beyond the documents:

1. **INV-002** requires bit-perfect replay *on every conformant implementation*; **INV-006**
   requires platform independence.
2. **INV-014** defines conformance as passing *all applicable Reference Fixtures*.
3. **INV-010** requires every Invariant to have a corresponding conformance test.
4. **APS-500** (RD-1-PDF) defines the fixture schema — including an `Expected Output` field —
   and supplies a single placeholder instance. No ARI fixture exists.
5. **APS-400** (RD-1-PDF) defines CONF-001…CONF-010; none concerns ARI, and CONF-001 tests
   reproducibility rather than correctness.
6. **APS-200** (this audit) names `ENT-003 Evaluation Result` but leaves its fields to future
   work.

The invariants that would bear on ARI reproducibility are stated; the instrument that would
evaluate them for ARI does not exist. **No remedy is proposed.**

## 5. Conclusion

**No artifact among the six highest-authority documents establishes an authoritative ARI
definition.** None contains a standalone `ARI` token, a formula, a bound, a rounding or division
rule, a drift definition, or an ARI field. APS-950's `RI-PY` occurrences are registry
identifiers, not definitions.
