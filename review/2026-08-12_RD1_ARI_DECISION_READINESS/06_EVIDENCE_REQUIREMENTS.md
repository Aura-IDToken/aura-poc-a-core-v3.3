# 06 — EVIDENCE REQUIREMENTS

**Package:** RD-1-ARI-DECISION-READINESS · **Normative effect:** NONE

What evidence would be required before a human authority could make each decision in a
defensible way. This document **requests** evidence; it supplies none of the decisions and
proposes no answers.

---

## 1. What does NOT count as evidence for a decision

Stated first, because it constrains everything below.

| Not evidence | Basis |
|---|---|
| **Implementation behaviour** | RD-1 premise 9 (CLOSED). Reinforced by `aura-specification/specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:37`: "Implementation behaviour does not constitute normative evidence unless an approved governance artifact explicitly grants that implementation normative authority." |
| **Test behaviour** | A test asserts what an implementation does. `aura-poc-a-core-v3.3/core/test_ari_observability.py:4-16` states the distinction in its own terms: "CURRENT BEHAVIOUR ≠ NORMATIVE REQUIREMENT". |
| **A fixture value** | Not authority unless a governing decision has already granted that fixture normative status. `aura-specification/aps/APS-500_REFERENCE_FIXTURES.md:63` records that canonical fixture data cannot yet be specified; the sole fixture file is entirely `"TODO"`. |
| **RI-PY's registry status** | RD-1 premise 5 and hard boundary 21. `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:7` records "APS-950 Certification Status: **NOT CERTIFIED**". |
| **This package** | It classifies evidence and formulates questions. It confers no authority on anything it cites. |
| **Repository precedent** | `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md` §9 records precedents of departure from stated rules "without a recorded authority", and treats them as facts about what happened, not as authority. The same treatment applies here. |

---

## 2. Evidence classes used below

| Class | Definition | Acceptance form |
|---|---|---|
| **E-NORM** | A statement in a document that holds normative authority for the domain, at a lifecycle status that gives it effect | Document ID · version · status · section · quoted text |
| **E-DERIV** | A derivation showing that a decided value follows from other decided values (e.g. a worst-case magnitude analysis) | Written derivation reproducible by a reader without code access |
| **E-XLANG** | Demonstration that the decision is implementable identically in each in-scope language, or that its divergence points are pinned | Per-language statement of the construct used, with the divergence explicitly addressed |
| **E-EXEC** | Executable evidence that a decided rule is satisfied — after the decision, never before it | Test or fixture citing the authorizing decision |
| **E-PROV** | Provenance evidence: identity, version and integrity binding of every input the decision depends on | Field-level record per SPEC-002 REQ-002-034's dependency-closure pattern |
| **E-IMPACT** | Impact statement: what existing artifacts the decision would render inconsistent, and what governance path applies | Enumeration with citations |

> **Ordering note.** E-EXEC is listed last deliberately. `NB-021_FROZEN_SEMANTICS_AUDIT.md` §8
> CASE E records that encoding an unresolved normative value as a test expectation "would
> constitute selecting that value", and identifies this as the one prohibition on which the whole
> corpus is unanimous. Executable evidence therefore follows a decision; it cannot support one.

---

## 3. Evidence standard applied to every decision

Derived from statements that already exist in the corpus; not invented here:

1. **Explicitness.** `aura-specification/constitution/AURA_CONSTITUTION.md` Article IV Principle 8
   (AURA-CON-001 v1.0, FROZEN): "All behaviour MUST be explicitly specified. Implicit behaviour is
   undefined behaviour."
2. **Single-outcome forcing.** SPEC-002 `:315` (REQ-002-032): a specification "MUST remain NOT
   READY if any conformant independent implementation can legitimately produce more than one"
   result from the same inputs.
3. **Independent derivability.** SPEC-002 `:291` (REQ-002-030) and `:498-537` (§10): an
   independent implementer must reach exactly one result **without inspecting any Reference
   Implementation**.
4. **Traceability.** `aura-specification/aps/APS-100_PROTOCOL_INVARIANTS.md:116-134`: every
   invariant links requirement → APS → CONF → evidence → ADR → release.
5. **Documented product.** AURA-CON-001 Article IV Principle 10: "An undocumented requirement does
   not exist."

A decision is **architecturally defensible** in this package's sense when its evidence set is
sufficient for an independent reader to (i) reconstruct why it was decided that way, (ii) derive
exactly one behaviour from it, and (iii) verify it without reading an implementation.

---

## 4. Per-decision evidence requirements

Columns: **Evidence required** · **Acceptance criterion** · **Prerequisites** (what must be
available before this evidence can even be gathered).

### Domain 1 — ARI Identity

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-001** | **E-NORM**: an authority ruling recorded in a document with a stated lifecycle status, saying whether ARI is a protocol object. **E-IMPACT**: enumeration of what becomes required (APS sections, CONF criteria, INV coverage) under each answer. | The ruling names the carrying document and its status; the impact list cites each affected artifact. | A decision on which authority ladder governs (`09_OPEN_QUESTIONS.md` OQ-A). |
| **ARI-D-002** | **E-NORM**: a statement naming the quantity or quantities that carry the name ARI, with the layer at which each is produced. **E-IMPACT**: effect on evidence records that currently emit one key for two quantities. | An evidence consumer can determine, from the record alone, which quantity a value is. | ARI-D-001. |
| **ARI-D-003** | **E-NORM**: a terminology ruling in the document designated canonical for terms (APS-000 / GLOSSARY). **E-IMPACT**: the cross-corpus inconsistency this creates and the amendment path for the other corpus. | One expansion is authoritative and the other document's status is addressed rather than left contradictory. | ARI-D-001 (informing). |

### Domain 2 — Input Contract

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-004** | **E-NORM**: an authored input contract (APS-001 §3 or successor) enumerating fields, types and domains, and marking each as computational or audit-only. **E-PROV**: for each field, where it comes from and how its integrity is bound. | An implementer can construct a valid input without reading code; every field's role is stated. | APS-001 §3 authored (currently `TODO`); ARI-D-001. |
| **ARI-D-005** | **E-NORM**: a statement placing structural validation inside or outside the ARI boundary. If inside, **E-NORM** naming the schema artifact and version; if outside, **E-PROV** defining the evidence that the caller's assertion is auditable. | The structural term's value is derivable by an auditor from the record. | ARI-D-004; if schema-based, `APS-200:92` (`request_fields` schema, `TODO`). |

### Domain 3 — Vector Dimension

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-006** | **E-NORM**: a ruling on whether dimension is a contract element, and if so, the fixing artifact. **E-NORM**: a ruling on operand-length equality and the check location. **E-DERIV**: the relation between dimension and the embedding method that produces vectors of that dimension. **E-IMPACT**: consequences for fixture size and for overflow analysis. | Dimension (or its absence) is derivable from the specification alone; the mismatch case has a stated outcome. | ARI-D-004; SPEC-002 AD-CA-005 (embedding identity, UNRESOLVED). |

### Domain 4 — Quantization

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-007** | **E-NORM**: a scope ruling on whether `CONSTITUTIONAL_DECREE.md` Article I binds a protocol-level ARI (OQ-A/OQ-B). **E-NORM**: resolution of the Decree's own Q16.16-versus-decimal-scale coexistence. **E-NORM**: a statement of the quantity a scaled integer denotes. **E-DERIV**: representable-range implications. **E-IMPACT**: which existing constants and documented ranges would need restating under each option. | Exactly one fixed-point contract is derivable; the Decree's internal inconsistency is addressed rather than inherited. | OQ-A/OQ-B; possibly SPEC-002 AD-CA-007 depending on U-2 (`05_DEPENDENCY_GRAPH.md` §4). |

### Domain 5 — Integer Representation

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-008** | **E-NORM**: a per-position table (element / accumulator / intermediate / output) of width and signedness. **E-NORM**: a ruling on arbitrary-precision admissibility. **E-XLANG**: per-language statement of how each position is represented, including a language without native 64-bit integers. **E-DERIV**: conversion behaviour at each position boundary. | Two implementers in different languages derive the same representation without consulting each other. | ARI-D-007. |

### Domain 6 — Arithmetic Semantics

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-009** | **E-NORM**: a fully ordered operation sequence with every rescale point marked. **E-NORM**: a reassociation ruling. **E-DERIV**: worked intermediate values for at least one input, sufficient to distinguish rescale placements. | A reader can transcribe the sequence into any language without ambiguity, and the worked example distinguishes C-18 from C-19. | ARI-D-007, ARI-D-008. |

### Domain 7 — Division Semantics

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-010** | **E-NORM**: a rule for negative dividends, stated per division site. **E-DERIV**: a demonstration of whether negative dividends are reachable at all under the decided similarity codomain and input contract (if unreachable, that must be stated, not assumed). **E-XLANG**: per-language statement of the construct implementing the rule, given that the registered languages differ by default. **E-IMPACT**: the status of `docs/ADR_005_NO_FLOAT_RUNTIME.md:134` under the decision, since that sentence currently describes the operator differently. | Every division site has one stated behaviour for every sign of dividend; the ADR-005 sentence is addressed explicitly. | ARI-D-009, ARI-D-013. |

### Domain 8 — Rounding Semantics

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-011** | **E-NORM**: a tie rule with stated sign symmetry, per reduction site. **E-NORM**: a boundary ruling — is the quantization site inside ARI's conformance surface or a precondition supplied to it (U-3)? **E-XLANG**: per-language implementation statement, given three different runtime defaults. **E-DERIV**: the effect on any hash computed over quantized output. | The rule is stated independently of any language's default; the boundary ruling determines who must implement it. | ARI-D-007; U-3 resolved. |
| **ARI-D-012** | **E-NORM**: a ruling on whether derived representations are inside the conformance surface, and one rule per derived form if so. **E-IMPACT**: reconciliation of the two existing reductions (half-up at persistence; float division at the certificate). | A consumer of a derived value knows whether it is normative and how it was produced. | ARI-D-011, ARI-D-022. |

### Domain 9 — Similarity Function

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-013** | **E-NORM**: an explicit statement fixing each of the ten properties enumerated in `01_ARI_DECISION_REGISTER.md` ARI-D-013.A. **E-NORM**: whether the normalization precondition is a caller obligation or an engine obligation, with the consequence of violation. **E-DERIV**: for any exactness property, a demonstration that quantization permits it. **E-EXEC** *(after decision)*: property-exhibiting fixtures. | No property in the list of ten is left implicit; the equivalence-to-cosine claim, if retained, is stated with its precondition and its tolerance. | ARI-D-004, ARI-D-006, ARI-D-007. |

### Domain 10 — Drift

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-014** | **E-NORM**: a ruling on drift's status as a protocol output. **E-NORM**: definition, range, units, clamping — stated independently of ARI. **E-NORM**: disambiguation of the two quantities currently sharing the word (emitted field vs threshold operand). **E-IMPACT**: whether drift enters conformance and evidence obligations. | Drift's definition is readable without reference to ARI's, and the two "drift" quantities are separately named. | ARI-D-002, ARI-D-013. |

### Domain 11 — Penalty Model

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-015** | **E-NORM**: an ARI/policy boundary ruling. **E-NORM**: if inside, one penalty function with units, trigger and clamp interaction; if outside, the evidence rule that keeps a penalized value distinguishable from a measurement. **E-DERIV**: the relationship between penalty magnitude and the decided output bound. **E-PROV**: policy identity and version binding, if the penalty is policy-dependent. | A reader can compute the penalized value, or can tell that penalization is out of scope, without consulting code. | ARI-D-002; ARI-D-016 (mutually informing). |

### Domain 12 — Output Bounds

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-016** | **E-NORM**: separate normativity rulings for ARI and for drift. **E-NORM**: bound values, enforcement mechanism (clamp / reject / precondition) and enforcement point. **E-DERIV**: if bounds are derived from the input precondition, the derivation showing admissible inputs cannot exceed them. **E-IMPACT**: the status of the documented `[0,100000]` statements and of the persistence constraints under the decision. **E-EXEC** *(after decision)*: boundary fixtures. | A value outside the bound has a stated status (impossible / clamped / rejected), and the mechanism is derivable from the specification. | ARI-D-013, ARI-D-015, ARI-D-021. |

### Domain 13 — Error / Malformed Input

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-017** | **E-NORM**: an enumerated invalid-input set, decided condition by condition, covering at minimum the classes listed in ARI-D-017.A. **E-NORM**: a statement of which conditions ARI owns and which belong upstream. | Every listed condition has an explicit in/out ruling; no condition is left to inference. | ARI-D-004, ARI-D-006, ARI-D-013, ARI-D-021; APS-001 §8 authored. |
| **ARI-D-018** | **E-NORM**: a detection obligation per condition, with the boundary at which detection occurs. **E-XLANG**: statement that detection is implementable identically across languages. | An implementation that omits a required detection is identifiably non-conformant. | ARI-D-017. |
| **ARI-D-019** | **E-NORM**: a response class per condition, expressed behaviourally rather than as a number. **E-NORM**: an explicit statement of whether any numeric ARI value may be emitted on invalid input. **E-NORM**: a definition of "safe state" for an ARI computation, which INV-008 requires and APS-001 §8 does not yet supply. **E-XLANG**: an abstract failure category that is expressible in every in-scope language. | No reader can conclude that fail-closed implies a particular number unless that is explicitly what was decided. | ARI-D-017; APS-001 §8. |
| **ARI-D-020** | **E-NORM**: whether failure produces evidence; if so, the failure-record schema and its relation to APS-200 ENT-003 / APS-300. **E-NORM**: an explicit distinguishability requirement between "not computed" and "computed as zero". **E-IMPACT**: interaction with INV-004 (Immutable Evidence) and INV-008's "no partial output … or persisted". | An auditor can distinguish a failure record from a measurement record by inspection. | ARI-D-019; APS-300 Evidence Pack format. |

### Domain 14 — Overflow / Range

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-021** | **E-DERIV**: a worst-case magnitude analysis per arithmetic position, computed from the decided dimension and scale. **E-NORM**: an overflow behaviour per position. **E-NORM**: a ruling on arbitrary-precision admissibility. **E-XLANG**: per-language statement including build-profile-dependent behaviours. **E-NORM**: whether overflow is an ARI-D-017 condition. | The analysis shows either that overflow cannot occur for admissible inputs, or exactly what happens when it does. | ARI-D-006, ARI-D-007, ARI-D-008. |

### Domain 15 — Serialization

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-022** | **E-NORM**: one canonical representation (field names, types, ordering, absent-field handling). **E-NORM**: one canonical byte sequence per hashed representation, with field inclusion/exclusion — the SPEC-002 REQ-002-017…022 pattern. **E-XLANG**: demonstration that the byte sequence is reproducible in each in-scope language without relying on a particular library's defaults. **E-IMPACT**: the status of the three existing canonicalizations and the two existing external shapes. | Two implementations produce identical bytes for the same logical result, derivable from the specification alone. | ARI-D-002, ARI-D-008, ARI-D-012, ARI-D-016; SPEC-002 AD-CA-008 (UNRESOLVED). |

### Domain 16 — Reference Model

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-023** | **E-NORM**: a ruling on whether a reference model is normative, advisory, or absent by design. **E-NORM**: if normative, the explicit governance grant SPEC-002 `:37` requires, naming artifact and version. **E-NORM**: resolution of which engine is being spoken about, given two exist. **E-IMPACT**: effect on the SPEC-002 §10 property that verification requires no reference inspection. | No implementation acquires authority implicitly; the designated object is identified to a version. | The semantics it would exemplify (ARI-D-004 … ARI-D-022); U-1 direction resolved. |

### Domain 17 — Conformance Contract

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-024** | **E-NORM**: which CONF tests bind ARI, with PASS criteria expressed in ARI terms. **E-DERIV**: a demonstration that the chosen criteria can distinguish the divergences enumerated in this package — a repeatability-only criterion demonstrably cannot. **E-NORM**: advancement of the relevant CONF documents beyond DRAFT with preconditions specified. **E-EXEC** *(after decision)*: executed conformance runs with evidence. | A conformant-but-divergent pair of implementations is impossible under the stated criteria, or the residual divergence is explicitly accepted and documented. | ARI-D-019, ARI-D-025, ARI-D-026, ARI-D-027. |

### Domain 18 — Reference Fixtures

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-025** | **E-NORM**: a ruling on fixture-based conformance. **E-NORM**: an ARI fixture format with an exactness-or-tolerance statement. **E-NORM**: the governance act that grants a fixture normative status. **E-DERIV**: for each fixture value, a derivation from the decided semantics — never from an execution. **E-PROV**: dependency closure for each fixture (constitution vector identity, embedding identity, versions). | Each fixture value is reproducible by derivation from the specification, and its authority is traceable to a governance act. | ARI-D-001 … ARI-D-022; APS-500's own prerequisites (APS-200 schemas, APS-300 pack). |

### Domain 19 — Cross-Language Equivalence

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-026** | **E-NORM**: the comparison object and the equivalence relation. **E-NORM**: the input set over which equivalence must hold, and whether failure behaviour is included. **E-NORM**: the enumerated language-dependent constructs that are pinned, each traced to the decision that pins it. **E-NORM**: the observation surface that makes equivalence checkable. **E-XLANG**: at least two independent implementations, or a derivation showing that the pinned constructs leave no residual freedom. **E-NORM**: the platform and runtime set in scope. | "Equivalent" has one meaning, one comparison object, and one verification procedure. | ARI-D-008, ARI-D-010, ARI-D-011, ARI-D-021, ARI-D-022. |

### Domain 20 — Audit / Reproducibility

| Decision | Evidence required | Acceptance criterion | Prerequisites |
|---|---|---|---|
| **ARI-D-027** | **E-NORM**: a field-by-field reproduction record. **E-PROV**: an ARI-specific dependency closure (embedding identity and version, dictionary identity and version, constants, constitution vector identity, specification version, implementation identity) following the REQ-002-034 pattern. **E-NORM**: a provenance-boundary ruling — inside, outside, or externally bound to the hashed representation. **E-EXEC** *(after decision)*: a third party reproducing a recorded ARI from the record alone, without inspecting an implementation. | The reproduction demonstration succeeds without implementation access. | ARI-D-022, ARI-D-023, ARI-D-026; SPEC-002 AD-CA-005/006/010 (all UNRESOLVED). |

---

## 5. Evidence that is currently obtainable without any decision

Recorded so that reviewers can see what is *not* blocked. **Nothing in this section is a
recommendation, a plan, a task list, or an authorization**; it is a statement of which evidence
classes are reachable in the current state.

| Evidence | Reachable now? | Basis |
|---|---|---|
| **E-IMPACT** enumerations (what a decision would render inconsistent) | Yes — this package is itself partly that | Documentation of existing state; no decision required |
| **E-DERIV** worst-case magnitude analysis | Only **conditionally** — it is a function of dimension and scale, both undecided (ARI-D-006, ARI-D-007). A parametric derivation is possible; a concrete one is not | ARI-D-021 prerequisites |
| **E-XLANG** enumeration of divergence points | Yes as an *enumeration*; no as a *resolution* | The constructs are observable; pinning them is a decision |
| **E-NORM** for any ARI decision | **No** | RD-1 (CLOSED): no normative ARI definition exists |
| **E-EXEC** for any ARI decision | **No** | Would require a decision first; `NB-021_FROZEN_SEMANTICS_AUDIT.md` §8 CASE E records this as prohibited by four independent sources |
| **E-PROV** dependency closure | **Partially** — the embedding dependency is a self-declared placeholder (`aura-poc-a-core-v3.3/core/embedding.py:2-3`) and its identity is undecided (SPEC-002 AD-CA-005/006) | Cannot be completed while those remain UNRESOLVED |

---

*This document has no normative effect. It states what evidence would be required; it supplies no
decision, ranks no candidate, creates no ADR, amends no specification, and modifies no code.*
