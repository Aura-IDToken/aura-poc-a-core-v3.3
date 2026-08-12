# 01 — ARI DECISION REGISTER

**Package:** RD-1-ARI-DECISION-READINESS · **Normative effect:** NONE

---

## 0. How to read this register

Every semantic question that must be answered before ARI can become a normative,
cross-language, independently verifiable algorithm receives a **new, unique identifier** in the
`ARI-D-nnn` namespace.

**Identifier policy.** `ARI-D-nnn` is a new namespace created for this package. Existing
identifiers (`AD-CA-nnn` from SPEC-002 §6, `INV-nnn` from APS-100, `REQ-002-nnn` from SPEC-002,
`CONF-nnn` from APS-400, `RD-n` / `CORE-Pn-nnn` from `review/2026-08-11_ENGINEERING_BASELINE/`)
are cited as **related identifiers only**, never reused as the identifier of an ARI decision,
because no repository material maps any of them onto an ARI semantic decision. Where SPEC-002
§7 or §6 *does* explicitly map a requirement to an AD-CA identifier, that mapping is quoted and
the AD-CA identifier is shown in the "Related" line — as a citation, not a claim of coverage.

**Each decision is stated in four separate, non-collapsed categories:**

- **A — WHAT MUST BE DEFINED** — the exact semantic question requiring an authoritative answer.
- **B — EXISTING STATE** — what the repositories actually contain, with provenance.
- **C — NON-NORMATIVE CANDIDATES** — candidate behaviours/models found in repository material.
- **D — EVIDENCE REQUIRED** — what evidence a human authority would need before deciding.

A, B, C and D are never merged. C never becomes A. B never becomes an answer to A.

**Provenance line format used throughout:**

`SOURCE` · `PATH:SECTION/LINE` · `STATUS` · `AUTHORITY TIER` · `INTERPRETATION`

**Authority tiers referenced** (both ladders recorded in `00_SCOPE_AND_GOVERNING_CONTEXT.md` §7;
neither selected):
`SPEC-CON` = AURA Constitution · `SPEC-APS` = APS document · `SPEC-DRAFT` = DRAFT specification
with declared zero normative effect · `IMPL-DECREE` = implementation-corpus Constitutional
Decree · `IMPL-DOC` = implementation-corpus documentation · `IMPL-CODE` = implementation code ·
`IMPL-TEST` = test code · `REVIEW` = prior review record (explicitly non-normative).

---

## 1. Register summary

| Domain | Decisions |
|---|---|
| 1. ARI Identity | ARI-D-001, ARI-D-002, ARI-D-003 |
| 2. Input Contract | ARI-D-004, ARI-D-005 |
| 3. Vector Dimension | ARI-D-006 |
| 4. Quantization | ARI-D-007 |
| 5. Integer Representation | ARI-D-008 |
| 6. Arithmetic Semantics | ARI-D-009 |
| 7. Division Semantics | ARI-D-010 |
| 8. Rounding Semantics | ARI-D-011, ARI-D-012 |
| 9. Similarity Function | ARI-D-013 |
| 10. Drift Definition | ARI-D-014 |
| 11. Penalty Model | ARI-D-015 |
| 12. Output Bounds | ARI-D-016 |
| 13. Error / Malformed Input Handling | ARI-D-017, ARI-D-018, ARI-D-019, ARI-D-020 |
| 14. Overflow / Range Handling | ARI-D-021 |
| 15. Serialization / Representation | ARI-D-022 |
| 16. Reference Model | ARI-D-023 |
| 17. Conformance Contract | ARI-D-024 |
| 18. Reference Fixtures | ARI-D-025 |
| 19. Cross-Language Equivalence | ARI-D-026 |
| 20. Audit / Reproducibility Requirements | ARI-D-027 |

**27 decisions. 0 answered.**

---

# DOMAIN 1 — ARI IDENTITY

## ARI-D-001 — Is ARI normatively defined by Aura, or does it remain implementation-defined?

**A — WHAT MUST BE DEFINED**
Whether the Aura Protocol specification undertakes to define ARI normatively at all — or
whether an explicit ruling is issued that ARI remains implementation-defined and is therefore
outside the conformance surface. Until this is answered, "conformant ARI" has no referent, and
every decision below is either required or moot depending on the answer.

**B — EXISTING STATE**

> `aura-specification/glossary/GLOSSARY.md:27-28` — **ARI** (Aura Reliability Index): "A
> deterministic measurement value computed by RI-PY using integer arithmetic. ARI is a
> measurement, not a decision."
> STATUS: GLOSSARY v1.0-DRAFT (header `Version: 1.0-DRAFT`, `Authority: APS-000`) ·
> TIER: SPEC-APS (draft) · INTERPRETATION: the only occurrence of ARI in the specification
> corpus defines it **by reference to an implementation**, not by mathematical content. It
> supplies no formula, range, dimension, division rule or rounding rule.

> `aura-specification/specification/APS-001_PROTOCOL_SPECIFICATION.md:5` — `Status: TODO`;
> `:12` — "This document does not yet exist. It is the highest-priority gap in the Aura
> Protocol Specification."
> STATUS: TODO · TIER: SPEC-APS (root normative specification, unauthored) ·
> INTERPRETATION: the root authority that would define protocol behaviour is absent, including
> §3 Input Requirements, §4 Output Requirements and §8 Error Handling, each marked TODO.

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:8` — `RAW_ARI = 0.3 ×
> StructuralIntegrity + 0.7 × SemanticAlignment`; `:207` — "**FROZEN** — Regulatory Audit
> Phase (MC-READY 2026)".
> STATUS: implementation-corpus documentation, self-declared FROZEN · TIER: IMPL-DOC ·
> INTERPRETATION: documents the implementation. Under AURA-CON-001 Article V, repository
> documentation sits below APS-001 and APS-100; it is not the protocol specification. Recorded
> as a **candidate**, see `03_NON_NORMATIVE_CANDIDATES.md` C-01.

**Related identifiers (citation only):** RD-1 (this package's premise); RD-1 in
`review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §12 poses the same
question as a *readiness* question; EC-2 in the same document.

**C — NON-NORMATIVE CANDIDATES** → C-01, C-02, C-03 in `03_NON_NORMATIVE_CANDIDATES.md`
(the two documented formulas and the "defer to RI-PY" model).

**D — EVIDENCE REQUIRED**
1. A ruling on whether ARI belongs to the protocol surface or to an implementation.
2. If protocol: identification of the document that will carry it (APS-001 §3/§4, a new APS, or
   an amendment path), and its lifecycle status.
3. If implementation-defined: an explicit statement of the conformance consequence — namely
   what CONF-001/CONF-006 then verify, given INV-001 and INV-006 are Critical.

---

## ARI-D-002 — Which quantity is "ARI": Layer 0 RAW_ARI, Layer 2 adjusted ARI, or both?

**A — WHAT MUST BE DEFINED**
Whether the normative object called ARI is (i) the Layer 0 measurement before penalty,
(ii) the Layer 2 value after penalty, or (iii) a pair of separately named normative outputs.
This determines what a fixture pins, what a hash covers, and what "the ARI" means in evidence.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/evaluator.py:4` — "Implementation of RAW_ARI formula: RAW_ARI =
> 0.3*SI + 0.7*SA"; `:6` — "Layer 0 measurement only. Penalties (P) are applied by Layer 2";
> `:89` — returns key `"ari"` (not `"raw_ari"`).
> STATUS: production code · TIER: IMPL-CODE · INTERPRETATION: the Layer 0 return key is
> `ari` while the documented quantity is `RAW_ARI`; the two names denote the same field here.

> `aura-poc-a-core-v3.3/compliance/evaluator_wrapper.py:70` —
> `adjusted_ari = max(0, result["ari"] - penalty)`; `:73` — returned under the same key `"ari"`.
> STATUS: production code · TIER: IMPL-CODE · INTERPRETATION: two different quantities are
> emitted under one field name at two layers.

> `aura-poc-a-core-v3.3/init.sql:32-46` — DB constraints reference a certificate field named
> `RAW_ARI`, constrained `BETWEEN 0 AND 100000`.
> STATUS: schema DDL · TIER: IMPL-CODE · INTERPRETATION: a third name for the persisted value.
> `review/2026-08-11_ENGINEERING_BASELINE/04_DETERMINISM_AUDIT.md` records that no application
> code writes to that table.

**C — NON-NORMATIVE CANDIDATES** → C-04 (`RAW_ARI` / `ari` / adjusted-`ari` naming set).

**D — EVIDENCE REQUIRED**
1. A stated normative naming and layering: which quantity carries the name ARI in evidence.
2. Whether both quantities are protocol outputs or only one.
3. If both: their distinct identifiers and their relationship, stated so that an evidence record
   is unambiguous.

---

## ARI-D-003 — What is the authoritative expansion and nomenclature of "ARI"?

**A — WHAT MUST BE DEFINED**
The authoritative expansion of the acronym, given that two corpora expand it differently, and
whether the mandated/forbidden nomenclature rules apply to the normative definition.

**B — EXISTING STATE — CONTRADICTED**

> `aura-specification/glossary/GLOSSARY.md:27` — "**ARI** (**Aura** Reliability Index)".
> STATUS: DRAFT · TIER: SPEC-APS (draft).

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:186` — "**Required Term**: 'Agent
> Reliability Index' (ARI)"; `:188` — "**Forbidden Term**: 'Trust Score'"; `:190` — rationale:
> "Avoid classification as Social Scoring system under AI Act."
> STATUS: implementation-corpus documentation, self-declared FROZEN · TIER: IMPL-DOC.

> `aura-specification/glossary/GLOSSARY.md:88-99` — Reserved Terms table prohibits "Trust
> Score" as an Aura synonym; consistent with the above on the *forbidden* term only.
> INTERPRETATION: the two corpora agree on what ARI must not be called and disagree on what the
> "A" stands for. Neither corpus cites the other.

**C — NON-NORMATIVE CANDIDATES** → C-05 ("Aura Reliability Index" / "Agent Reliability Index").

**D — EVIDENCE REQUIRED**
1. A ruling on the authoritative expansion, recorded in whichever document is designated
   canonical for terminology (APS-000 / GLOSSARY).
2. Confirmation whether the regulatory rationale quoted from
   `docs/mathematical_foundation.md:190` is itself normative or explanatory.

---

# DOMAIN 2 — INPUT CONTRACT

## ARI-D-004 — What constitutes a valid ARI input?

**A — WHAT MUST BE DEFINED**
The complete input contract for an ARI computation: which fields are required, their types,
their domains, their provenance, and which of them participate in the computation versus in
identity/audit only. Without it, "malformed input" (Domain 13) has no complement.

**B — EXISTING STATE**

> `aura-specification/specification/APS-001_PROTOCOL_SPECIFICATION.md:44-46` — "### 3. Input
> Requirements — **TODO**: Define what constitutes a valid Evaluation Request (APS-200
> ENT-002). What fields are mandatory? What validation is required?"
> STATUS: TODO · TIER: SPEC-APS · INTERPRETATION: the input contract is explicitly unauthored.

> `aura-specification/aps/APS-200_CANONICAL_DATA_MODEL.md:81-92` — ENT-002 Evaluation Request
> defines `input_hash`, `input_schema`, `request_fields`; `:92` — "**TODO**: Define the
> canonical schema for `request_fields`."
> STATUS: 1.0-DRAFT · TIER: SPEC-APS · INTERPRETATION: the container is specified; the payload
> that would carry a vector is not. No ARI field appears in APS-200.

> `aura-poc-a-core-v3.3/core/evaluator.py:50` — `evaluate(self, agent_id: str, vector:
> List[int], valid_schema: bool)`; `:60-62` docstring — "vector: Agent action vector (int32,
> scaled by 10^5)".
> STATUS: production code · TIER: IMPL-CODE · INTERPRETATION: implementation evidence of one
> input shape. Not authority.

> `aura-poc-a-core-v3.3/compliance/consistency.py:74-75` — required keys
> `["timestamp", "embedding", "content"]`.
> STATUS: production code · TIER: IMPL-CODE · INTERPRETATION: a second, different input shape
> in the same repository.

**C — NON-NORMATIVE CANDIDATES** → C-06, C-07 (the two input shapes).

**D — EVIDENCE REQUIRED**
1. An authored input contract (APS-001 §3 or successor) enumerating required fields and types.
2. A statement of which fields are inside the ARI computation and which are audit-only.
3. A decision on whether the contract is schema-validated at the boundary, and by which schema
   artifact (APS-200 §9 JSON Schema is marked TODO).

---

## ARI-D-005 — Is structural validity an input to ARI or a property computed by the ARI engine?

**A — WHAT MUST BE DEFINED**
Whether the structural-integrity term is asserted by the caller (an input) or determined by the
engine (a computation), and, if computed, against which schema.

**B — EXISTING STATE — CONTRADICTED WITHIN THE IMPLEMENTATION**

> `aura-poc-a-core-v3.3/core/evaluator.py:50,67` — `valid_schema: bool` parameter;
> `si = self.SCALING_FACTOR if valid_schema else 0`.
> TIER: IMPL-CODE · INTERPRETATION: caller-asserted.

> `aura-poc-a-core-v3.3/compliance/consistency.py:72-75` — `_validate_structure` returns
> `SCALING_FACTOR` if all of `timestamp`, `embedding`, `content` are present, else `0`.
> TIER: IMPL-CODE · INTERPRETATION: engine-determined.

> `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:23` — "RI-002 Validation Layer | ✅ |
> schema validation as circuit breaker".
> STATUS: RI-PY v3.3, "APS-950 Certification Status: NOT CERTIFIED" (`:7`) · TIER: SPEC-APS
> registry entry · INTERPRETATION: a registry observation about an implementation; per RD-1 it
> is not a normative definition.

**C — NON-NORMATIVE CANDIDATES** → C-08 (caller-asserted boolean), C-09 (engine-determined
required-key check).

**D — EVIDENCE REQUIRED**
1. A ruling on where structural validation sits relative to the ARI boundary.
2. If engine-determined: the schema artifact and version against which it is determined.
3. If caller-asserted: the evidence obligation that makes the assertion auditable.

---

# DOMAIN 3 — VECTOR DIMENSION

## ARI-D-006 — Is vector dimension part of the normative input contract, and must the agent and constitution vectors match exactly?

**A — WHAT MUST BE DEFINED**
This is an **input-contract question**, not a proof question. It requires: (i) whether a fixed
dimension is normatively required at all; (ii) if so, which artifact fixes it and for which
vectors; (iii) whether agent-vector dimension must equal constitution-vector dimension; (iv)
whether dimension is validated at the ARI boundary or upstream.

> **Framing constraint carried from the task.** The 1536-dimensional constitution material and
> the observed success of a 1-element vector **MUST NOT** be treated as proof that 1536 is
> required, nor as proof that any dimension is acceptable. Both are recorded in B/C as evidence
> of current state and candidates; neither is treated as an answer.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/offline_normalizer.py:44` — `CONSTITUTION_DIM = 1536`; `:171-175`
> — `ValueError` if `len(float_vector) != CONSTITUTION_DIM`.
> STATUS: production code, offline path · TIER: IMPL-CODE · INTERPRETATION: a dimension
> constraint exists in the *offline normalizer only*.

> `aura-poc-a-core-v3.3/core/evaluator.py:13-23, 25-48` — neither `__init__` nor
> `vector_similarity_int32` references `CONSTITUTION_DIM` or compares lengths.
> TIER: IMPL-CODE · INTERPRETATION: the evaluation path enforces no dimension.

> `aura-poc-a-core-v3.3/core/evaluator.py:40` — `dot = sum(a * b for a, b in zip(v1, v2))`.
> TIER: IMPL-CODE · INTERPRETATION: `zip()` stops at the shorter sequence. This is the
> mechanism referenced by the length-mismatch question (Domain 13, ARI-D-017/019); it is
> recorded here as a fact about the current code and **is not being fixed**.

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:116-118` — "### Vector Space: ℝ¹⁵³⁶ …
> The semantic space **was** 1536-dimensional"; `:111-114` — "⚠️ **HISTORICAL ONLY — NOT THE
> CURRENT RUNTIME**".
> STATUS: IMPL-DOC, section self-labelled historical · INTERPRETATION: the 1536 statement in
> this document is explicitly scoped to the legacy float era, not to the current runtime.

> `aura-poc-a-core-v3.3/core/embedding.py:6,13,20` — placeholder embedding emits 1536 elements;
> `:2` — "Placeholder for deterministic embedding in ℝ¹⁵³⁶ space. MUST be frozen + reproducible
> in production."
> TIER: IMPL-CODE · INTERPRETATION: a placeholder, self-declared as such.

> `aura-poc-a-core-v3.3/compliance/certificate_schema.json:16` — `"semantic_space": "R1536"`.
> TIER: IMPL-CODE (schema sketch; `docs/GAP-001.md:208` records this file as "a sketch",
> "Schema not normative").

> Specification corpus: no dimension statement. APS-200 defines no vector field
> (`aps/APS-200_CANONICAL_DATA_MODEL.md` §5); SPEC-002 REQ-002-014 governs numeric
> representation of vector values but states no dimension.

**C — NON-NORMATIVE CANDIDATES** → C-10 (1536), C-11 (dimension unconstrained at the ARI
boundary), C-12 (equality-of-length requirement, present nowhere in code).

**D — EVIDENCE REQUIRED**
1. A ruling on whether dimension is a normative element of the input contract.
2. If yes: the artifact that fixes it, and whether it is a single value or a versioned set.
3. A statement on whether dimension equality between the two operands is required, and where it
   is checked (boundary vs upstream).
4. A statement of the relationship, if any, between the embedding method (undecided,
   SPEC-002 AD-CA-005) and dimension — since dimension is a property of the embedding.

---

# DOMAIN 4 — QUANTIZATION

## ARI-D-007 — What is the normative fixed-point scheme and scale for ARI operands and outputs?

**A — WHAT MUST BE DEFINED**
The quantization contract: the fixed-point representation family (decimal-scaled integer vs
binary fixed-point), the scale factor, the quantity each scaled integer represents, and whether
the same scheme applies to operands, intermediate values and outputs.

**B — EXISTING STATE — CONTRADICTED**

> `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` Article I §1 — "✔ Integer-only arithmetic
> (int32/int64) · ✔ Fixed-point arithmetic (**Q16.16**) · ✔ Scaling factor: **100,000 (10^5)**".
> Article I §8 — "**Sentinel Drift Threshold:** 0.68 (FROZEN) · **Scaling Factor:** 100,000
> (FROZEN) · ❌ These values SHALL NOT be modified."
> STATUS: `Version 1.0 · MANDATORY / NON-OVERRIDABLE` · TIER: IMPL-DECREE (tier 1 of the
> `CLAUDE.md` ladder; **not** part of the specification corpus and not cited by it) ·
> INTERPRETATION: **DISPUTED AUTHORITY — SCOPE UNRESOLVED.** The Decree binds this repository by
> its own terms, and `CLAUDE.md` places it at tier 1. It does not follow that it fixes the
> numeric representation of a *protocol-level, cross-language* ARI: the specification corpus
> never cites it, and SPEC-002 §3.4 lists `100000` as candidate-only for vector values. This
> package does not resolve that scope question (see `09_OPEN_QUESTIONS.md` OQ-A, OQ-B).
> **Internal contradiction recorded:** Q16.16 is a binary fixed-point format with a 2^16
> fractional scale; "scaling factor 100,000" is a decimal scale. The Decree lists both in the
> same article without stating their relationship.

> `aura-specification/specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:108` —
> "Candidate choices including `32`, `100000`, `signed int32`, `little-endian`,
> `Dictionary-Based Embedding`, and `round-half-to-even` are non-normative in this draft unless
> and until explicit architectural authority approves them. **No candidate choice listed in this
> document constitutes a recommendation, preference, default, or implied architectural
> decision.**"
> `:11-12` — "**Normative effect: NONE until APPROVED.**"; `:381` — AD-CA-007 "Numeric
> representation of vector values | UNRESOLVED".
> STATUS: v0.3-DRAFT · TIER: SPEC-DRAFT · INTERPRETATION: the specification corpus explicitly
> holds `100000` as a candidate and explicitly denies it the status of a default.

> `aura-poc-a-core-v3.3/core/evaluator.py:12` — `SCALING_FACTOR = 100000  # 10^5`;
> `core/offline_normalizer.py:41` — `SCALING_FACTOR = 10**5`;
> `compliance/policy.py:18` and `compliance/consistency.py:18` — `SCALING_FACTOR = 100000`.
> TIER: IMPL-CODE · INTERPRETATION: implementation evidence, consistent across four modules.

**C — NON-NORMATIVE CANDIDATES** → C-13 (decimal scale 10^5), C-14 (Q16.16), C-15 (SPEC-002
candidate set `32` / `100000` / `signed int32` / `little-endian`).

**D — EVIDENCE REQUIRED**
1. A ruling on whether the Decree's Article I constants bind a protocol-level ARI, or bind only
   this instrument (OQ-A/OQ-B).
2. Resolution of the Q16.16-versus-decimal-scale contradiction inside the Decree itself.
3. If AD-CA-007 is the governing decision domain for vector values: an explicit statement of
   whether ARI operands are "vector values" within its scope, or a separate domain.
4. A statement of what the scaled integer represents (a ratio in [0,1]? a similarity in
   [−1,1]?), since Domain 12 bounds depend on it.

---

# DOMAIN 5 — INTEGER REPRESENTATION

## ARI-D-008 — What integer width and signedness apply to operands, accumulators and outputs?

**A — WHAT MUST BE DEFINED**
Separately for (i) vector elements, (ii) the dot-product accumulator, (iii) intermediate
rescaled values, and (iv) the ARI/drift outputs: the integer width, signedness, and whether
arbitrary-precision integers are permitted for any of them.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/evaluator.py:25` — method named `vector_similarity_int32`; `:36`
> docstring — "Pre-normalized int32 vectors"; `:7` class docstring — "fixed-point int32
> arithmetic".
> TIER: IMPL-CODE · INTERPRETATION: `int32` here is a naming convention. Python integers are
> arbitrary-precision; nothing in the code constrains any value to 32 bits.

> `aura-poc-a-core-v3.3/.github/github/copilot-instructions.md:22` — "**Accumulator:** Use
> **int64** for all dot product accumulations to prevent overflow on 768/1536 dimensions."
> STATUS: repository Copilot directive · TIER: IMPL-DECREE-adjacent (`CLAUDE.md` tier 4:
> "Existing repository-level constitutional/Copilot directives") · INTERPRETATION: a directive
> to implementers stating an accumulator width. It states no ARI formula authority for the
> specification corpus and is a **candidate** here.

> `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md:510` — "Instead of: `float accumulation` —
> **Use:** `int64` accumulator with `10^5` scaling — **File:** `core/evaluator.py`".
> STATUS: MANDATORY / NON-OVERRIDABLE · TIER: IMPL-DECREE · INTERPRETATION: same accumulator
> width, stated as guidance in the Decree's substitution table. Scope question as in ARI-D-007.

> `aura-specification/specification/SPEC-002…:141` (REQ-002-014) — the future specification
> "MUST define one numeric representation for vector values, including domain, width, sign,
> scale, rounding behavior, overflow behavior, and byte order where applicable."
> STATUS: v0.3-DRAFT, normative effect NONE · TIER: SPEC-DRAFT · INTERPRETATION: the
> requirement to decide exists; the decision does not.

> `review/2026-08-11_ENGINEERING_BASELINE/04_DETERMINISM_AUDIT.md` §D-4 records a measured
> intermediate `dot = 15,360,000,000,000` for the 1536-dimension case at the scale bound,
> exceeding `int32` max `2,147,483,647`, with the rescaled result fitting `int32`.
> STATUS: prior review record, explicitly non-normative · TIER: REVIEW · INTERPRETATION:
> evidence that operand width and accumulator width are separate decisions. Not authority.

**C — NON-NORMATIVE CANDIDATES** → C-16 (`signed int32` operands + `int64` accumulator),
C-17 (arbitrary precision, as currently executed).

**D — EVIDENCE REQUIRED**
1. A per-position (operand / accumulator / intermediate / output) width and signedness ruling.
2. A statement on whether arbitrary-precision integers are conformant, since the executing
   reference language provides them and the target languages do not.
3. Coupling statement to ARI-D-021 (overflow behaviour) — width without overflow semantics is
   incomplete.

---

# DOMAIN 6 — ARITHMETIC SEMANTICS

## ARI-D-009 — What is the normative operation order, and at which points is rescaling applied?

**A — WHAT MUST BE DEFINED**
The exact ordered sequence of arithmetic operations for ARI, including where each rescaling
division occurs, whether weights are applied before or after rescaling, and whether any
reassociation is permitted. Two implementations can share a formula, a division rule and a
rounding rule and still differ if the rescale points differ.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/evaluator.py:40,46` — `dot = sum(a*b …)`, then
> `similarity = dot // self.SCALING_FACTOR` — one rescale after full accumulation.
> `:75-76` — `raw_ari = (self.weight_structural * si // self.SCALING_FACTOR) +
> (self.weight_semantic * sa // self.SCALING_FACTOR)` — two independent rescales, each applied
> to a weighted term **before** summation.
> TIER: IMPL-CODE · INTERPRETATION: implementation evidence of one specific rescale placement.

> `aura-poc-a-core-v3.3/compliance/consistency.py:57-61` — the same two-term pattern with
> `- penalty` applied inside the same expression.
> TIER: IMPL-CODE · INTERPRETATION: a second engine with a different expression shape.

> `aura-poc-a-core-v3.3/docs/ADR_005_NO_FLOAT_RUNTIME.md:103` — "✅ Integer multiplication:
> `(a * b) // SCALING_FACTOR` (rescale after multiply)".
> STATUS: ADR-005, header `Status: APPROVED`, footer `Status: FROZEN (MC-READY 2026)` ·
> TIER: IMPL-DOC (an implementation-corpus ADR; not an `aura-specification/adrs/` ADR) ·
> INTERPRETATION: states a rescale convention for multiplication. It does not state an
> operation order for ARI as a whole.

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:8, 17` — formula and
> `dot(event, constitution) // SCALING_FACTOR`.
> TIER: IMPL-DOC · INTERPRETATION: documents the same two steps at a higher level; silent on
> weight-application order.

**C — NON-NORMATIVE CANDIDATES** → C-18 (rescale-per-weighted-term), C-19 (rescale-after-sum,
present in no source but implied as the alternative by the arithmetic).

**D — EVIDENCE REQUIRED**
1. A fully ordered operation sequence, written so that an implementer can transcribe it without
   inspecting code (SPEC-002 §10 Independent Implementer Test standard).
2. An explicit statement on whether reassociation/reordering is permitted.
3. Worked intermediate values for at least one input, to disambiguate rescale placement.

---

# DOMAIN 7 — DIVISION SEMANTICS

## ARI-D-010 — What integer division semantics does normative ARI require?

> **Framing carried from the task.** The ADR-005 statement about integer division and the
> observed Python behaviour are a **semantic conflict**. This package does not resolve it. The
> decision is framed as: *"What integer division semantics does normative ARI require?"*

**A — WHAT MUST BE DEFINED**
The required behaviour of every division in the ARI path for **negative dividends**: floor
(round toward −∞), truncation (round toward zero), or another rule; and whether the same rule
applies at every division site.

**B — EXISTING STATE — CONTRADICTED**

> `aura-poc-a-core-v3.3/docs/ADR_005_NO_FLOAT_RUNTIME.md:134` — "Integer division (`//`) is
> deterministic (**truncation toward zero**)".
> STATUS: ADR-005, `Status: APPROVED` / `FROZEN (MC-READY 2026)` · TIER: IMPL-DOC ·
> INTERPRETATION: a statement of what `//` does. Python's `//` floors; it truncates toward zero
> only for non-negative operands. The statement and the operator it describes diverge for
> negative dividends. **Recorded as a conflict; not resolved, not corrected.**

> `aura-poc-a-core-v3.3/core/evaluator.py:46` — `similarity = dot // self.SCALING_FACTOR`;
> `:75-76` — two further `//` sites; `compliance/consistency.py:58-59,94` — three more.
> TIER: IMPL-CODE · INTERPRETATION: six division sites in the ARI path, all using the same
> operator.

> `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §5.2 records
> measured divergence at `dot = −1` (Python `−1`; truncating port `0`) and an evaluation
> divergence `{'ari': 29999, 'drift': 100001}` versus `{'ari': 30000, 'drift': 100000}`.
> STATUS: prior review record, explicitly non-normative · TIER: REVIEW · INTERPRETATION:
> evidence that the two rules produce different ARI values. Neither is designated correct
> there, and neither is designated correct here.

> `aura-specification/specification/SPEC-002…:381` — AD-CA-007 candidate list contains no
> division rule. `review/…/05_CORE_REMEDIATION_READINESS.md` §7 records: "division rule **not
> listed even as a candidate**".
> STATUS: v0.3-DRAFT · TIER: SPEC-DRAFT · INTERPRETATION: the specification corpus has not
> registered division semantics as a decision domain at all.

**C — NON-NORMATIVE CANDIDATES** → C-20 (floor), C-21 (truncate toward zero), C-22 (avoid the
question by forbidding negative dividends — an input-contract route, not a division rule).

**D — EVIDENCE REQUIRED**
1. A statement of the required rule for negative dividends, applied per division site.
2. Confirmation whether negative intermediate values can occur at all under the decided input
   contract and similarity model (ARI-D-013) — if they cannot, the rule may be vacuous, and
   that too must be stated rather than assumed.
3. A conformance vector set that distinguishes the rules (at minimum one negative dividend that
   is not an exact multiple of the scale).

---

# DOMAIN 8 — ROUNDING SEMANTICS

## ARI-D-011 — What rounding semantics does normative ARI require at float→integer reduction?

> **Framing carried from the task.** The implementation's `round()` behaviour is **not** a
> normative choice. The decision is framed as: *"What rounding semantics does normative ARI
> require?"*

**A — WHAT MUST BE DEFINED**
The rounding rule at every point where a real-valued quantity is reduced to a scaled integer,
including tie behaviour and sign symmetry, and whether that point is inside or outside the ARI
boundary.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/offline_normalizer.py:88` —
> `int_vector = [round(x * SCALING_FACTOR) for x in normalized_vector]`; reached from `:181`
> and `:227`.
> TIER: IMPL-CODE · INTERPRETATION: one site, on the constitution-vector construction path.
> Python's `round()` is half-to-even. This is implementation evidence only.

> `aura-poc-a-core-v3.3/docs/ADR_005_NO_FLOAT_RUNTIME.md:84` — "✅ Fixed-point scaling:
> `v_int = round(v_float × 10^5)`"; `:75-88` — DET_01 declares float permitted offline and
> `:90-99` DET_02 prohibits it at runtime.
> STATUS: APPROVED / FROZEN · TIER: IMPL-DOC · INTERPRETATION: states the operation, not the
> tie rule.

> `aura-specification/specification/SPEC-002…:108, :381` — `round-half-to-even` is listed as
> **candidate only** under AD-CA-007, with the explicit statement that no candidate constitutes
> a recommendation, preference or default.
> STATUS: v0.3-DRAFT, normative effect NONE · TIER: SPEC-DRAFT.

> `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §5.3 records
> measured tie behaviour differences across Python / Rust / JS and notes that the offline
> normalizer output feeds the CI `ari_vector_hash`.
> TIER: REVIEW · INTERPRETATION: evidence of cross-language divergence. Not authority.

**C — NON-NORMATIVE CANDIDATES** → C-23 (half-to-even), C-24 (half-away-from-zero),
C-25 (half-toward-+∞), C-26 (half-up on the presentation path — see ARI-D-012).

**D — EVIDENCE REQUIRED**
1. A stated tie rule and its sign symmetry, per reduction site.
2. A ruling on whether the quantization site is inside the ARI conformance boundary or is a
   pre-condition supplied to it (this changes who must implement the rule).
3. Test vectors at exact `.5` boundaries in both signs.

---

## ARI-D-012 — What rounding applies to derived/presented ARI representations?

**A — WHAT MUST BE DEFINED**
Whether any derived representation of ARI (decimal ratio, database column, certificate field) is
part of the normative surface, and if so, its rounding rule — separately from ARI-D-011.

**B — EXISTING STATE — TWO DIFFERENT REDUCTIONS EXIST**

> `aura-poc-a-core-v3.3/init.sql:57-61` — "Deterministic **half-up** cent rounding from integer
> RAW_ARI / 100000" implemented as `((certificate ->> 'RAW_ARI')::BIGINT + 500) / 1000`.
> TIER: IMPL-CODE (DDL) · INTERPRETATION: a half-up rule, stated explicitly, on the persistence
> path.

> `aura-poc-a-core-v3.3/compliance/certificate.py:29-31` — "`ari_score = ari_int32 /
> SCALING_FACTOR`"; `:41` — `ari_score: float  # Agent Reliability Index ∈ [0.0, 1.0]`;
> `:32-35` — "This conversion is intentional and limited to the presentation/reporting layer.
> Raw int32 values remain the normative measurement."
> TIER: IMPL-CODE · INTERPRETATION: a float division with no stated rounding rule, on the
> certificate path. The quoted phrase "remain the normative measurement" is the **source's own
> characterization**; per RD-1 no normative ARI definition exists, so it is recorded as a
> source claim, not as authority.

**C — NON-NORMATIVE CANDIDATES** → C-26 (half-up, DB), C-27 (binary float division,
certificate).

**D — EVIDENCE REQUIRED**
1. A ruling on whether derived representations are inside the conformance surface.
2. If inside: one rounding rule per representation, and their mutual consistency.
3. If outside: an explicit statement that derived values are non-normative, so that evidence
   consumers do not treat them as the measurement.

---

# DOMAIN 9 — SIMILARITY FUNCTION

## ARI-D-013 — Which mathematical properties must the ARI similarity function satisfy?

> **Framing carried from the task.** No similarity function is chosen here. What is identified
> is the exact set of mathematical properties that a normative specification must fix.

**A — WHAT MUST BE DEFINED — the property set**

1. **Domain** — the admissible set of operand vectors (element domain, magnitude constraint,
   dimension, zero-vector admissibility).
2. **Codomain and range** — the exact output interval in scaled-integer terms, including
   whether negative outputs are in range.
3. **Normalization precondition** — whether operands are required to be unit-norm, and whether
   that is (i) assumed, (ii) validated, or (iii) enforced by construction.
4. **Symmetry** — whether `s(a,b) = s(b,a)` is required.
5. **Identity/reflexivity** — the required value of `s(a,a)` for admissible `a`.
6. **Boundedness** — whether the function is required to be bounded, and by what.
7. **Monotonicity/ordering** — whether any ordering property is required (e.g. anti-aligned ≤
   orthogonal ≤ aligned).
8. **Behaviour on the zero vector** — a value, or an error (links to Domain 13).
9. **Quantization error tolerance** — whether an exact integer identity is required
   (`s(a,a) == scale`) or a bounded deviation is admissible, and the bound.
10. **Determinism obligation** — accumulation order independence, given INV-001 and INV-006.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/evaluator.py:25-48` — a dot product of two integer vectors,
> rescaled once; docstring `:29-31` — "For unit-normalized vectors: similarity ≈ dot_product /
> (SCALING_FACTOR)"; `:37` — "range approximately [-10^5, 10^5]".
> TIER: IMPL-CODE · INTERPRETATION: the word "approximately" appears twice; no exact property
> is asserted. No normalization check exists in this path.

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:95` — "Result is equivalent to cosine
> similarity for unit-normalized inputs, computed entirely in integers".
> TIER: IMPL-DOC · INTERPRETATION: an equivalence claim **conditional** on a precondition that
> the code does not verify.

> `aura-poc-a-core-v3.3/compliance/consistency.py:84-91` — zero-vector guard returning `0`, and
> `ValueError` if any element exceeds the scale.
> TIER: IMPL-CODE · INTERPRETATION: a second engine asserting a different property set for the
> same conceptual function.

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:122-137` — legacy cosine similarity
> and the legacy mapping `(cos + 1)/2`, both under the "HISTORICAL ONLY" banner at `:111-114`.
> TIER: IMPL-DOC (self-labelled historical) · INTERPRETATION: a historical candidate.

> `aura-poc-a-core-v3.3/.github/github/copilot-instructions.md:21` — "SA is defined as a
> fixed-point dot product of pre-normalized unit vectors."
> TIER: `CLAUDE.md` tier 4 directive · INTERPRETATION: states the precondition explicitly as a
> directive to implementers.

**C — NON-NORMATIVE CANDIDATES** → C-28 (rescaled integer dot product with assumed unit-norm),
C-29 (same with enforced magnitude validation), C-30 (legacy cosine + `(cos+1)/2` mapping).

**D — EVIDENCE REQUIRED**
1. A specification that fixes each of the ten properties in A explicitly.
2. A statement of whether the normalization precondition is a caller obligation or an engine
   obligation, with the failure consequence if violated (links to ARI-D-017/019).
3. Fixtures exhibiting each required property (identity, symmetry, ordering, bounds).

---

# DOMAIN 10 — DRIFT DEFINITION

## ARI-D-014 — Is drift a normative protocol output, and what is its definition and range?

> **Framing carried from the task.** Drift is treated as a **separate semantic output**, because
> it is emitted by the engine and participates in the audit path.

**A — WHAT MUST BE DEFINED**
Whether drift is a normative output at all; its definition relative to the similarity term; its
range and clamping; its relationship to the drift *threshold* used by policy; and whether it is
covered by the same determinism and evidence obligations as ARI.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/evaluator.py:86` —
> `drift = min(max(0, self.SCALING_FACTOR - sa), 2 * self.SCALING_FACTOR)`; `:90` — returned as
> `"drift"`; `:85` inline comment — "Clamp drift to [0, 100000] to represent [0.0, 1.0]".
> TIER: IMPL-CODE · INTERPRETATION: the code's upper clamp is `2 × SCALING_FACTOR`; the
> docstring states `100000`. The two disagree. **Recorded as a documented divergence; not
> fixed.**

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:53-54` — states output ranges for
> RAW_ARI and ARI; **no drift range is stated in the Output Range section.**
> TIER: IMPL-DOC · INTERPRETATION: drift's range is undocumented at the level where ARI's is
> documented.

> `aura-poc-a-core-v3.3/compliance/policy.py:19` — `DRIFT_THRESHOLD = 68000`; `:41` — penalty
> triggered by `sa_score < DRIFT_THRESHOLD`.
> TIER: IMPL-CODE · INTERPRETATION: the "drift" threshold is compared against the **semantic
> alignment** value, not against the emitted `drift` field. Two distinct quantities share the
> word "drift".

> `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` Article I §8 — "**Sentinel Drift Threshold:**
> 0.68 (FROZEN)".
> STATUS: MANDATORY / NON-OVERRIDABLE · TIER: IMPL-DECREE · INTERPRETATION: DISPUTED AUTHORITY
> — SCOPE UNRESOLVED, as in ARI-D-007. Fixes a threshold constant; does not define drift.

> `aura-poc-a-core-v3.3/compliance/certificate.py:41,54-56` — `drift` is emitted in the
> certificate `ari` object, i.e. it is on the audit path.
> TIER: IMPL-CODE.

> Specification corpus: no occurrence of drift as a protocol concept in APS-100, APS-200,
> APS-400, APS-500 or the glossary.

**C — NON-NORMATIVE CANDIDATES** → C-31 (`scale − SA`, clamped `[0, 2×scale]`), C-32
(`scale − SA` clamped `[0, scale]`, per the docstring), C-33 (drift threshold `68000` as a
policy constant).

**D — EVIDENCE REQUIRED**
1. A ruling on whether drift is a protocol output or an implementation-internal value.
2. If protocol: definition, range, clamping and units, stated independently of ARI.
3. Disambiguation of the two "drift" quantities (emitted field vs threshold operand).
4. A statement on whether drift is covered by the ARI conformance tests or has its own.

---

# DOMAIN 11 — PENALTY MODEL

## ARI-D-015 — Is a penalty model part of normative ARI, and which model applies?

**A — WHAT MUST BE DEFINED**
Whether penalties are inside the normative ARI definition or belong to a separately specified
policy layer; if inside, the penalty function, its units, its trigger, its interaction with
bounds; and how a penalty is represented in evidence.

**B — EXISTING STATE — TWO INCOMPATIBLE MODELS**

> `aura-poc-a-core-v3.3/compliance/policy.py:19-20,41` — `DRIFT_THRESHOLD = 68000`,
> `DRIFT_PENALTY = 150000`; penalty is `150000` if `sa_score < 68000`, else `0`.
> TIER: IMPL-CODE · INTERPRETATION: a threshold-triggered constant penalty exceeding the
> documented maximum ARI of `100000`.

> `aura-poc-a-core-v3.3/compliance/consistency.py:21,101-102` — `VIOLATION_PENALTY = 10000`;
> penalty is `violations × 10000`.
> TIER: IMPL-CODE · INTERPRETATION: a count-proportional penalty. Different unit, different
> trigger, different quantity from the above.

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:23,27-29` — `ARI = max(0, RAW_ARI − P)`;
> "Penalties (P): Sum of policy violations … Owned and calculated by Layer 2 (compliance/) …
> never computed inside Layer 0".
> TIER: IMPL-DOC · INTERPRETATION: documents the layering and a subtraction, without fixing the
> penalty function.

> `aura-poc-a-core-v3.3/compliance/evaluator_wrapper.py:61-70` — Layer 2 recomputes `sa` by
> calling the Layer 0 similarity function, derives a penalty, then subtracts.
> TIER: IMPL-CODE · INTERPRETATION: the layer boundary is crossed by a recomputation, which is
> a fact about the call graph relevant to where a normative boundary would be drawn.

**C — NON-NORMATIVE CANDIDATES** → C-34 (threshold penalty `150000`), C-35 (count penalty
`10000 × n`), C-36 (`ARI = max(0, RAW_ARI − P)` composition rule).

**D — EVIDENCE REQUIRED**
1. A ruling on the ARI/policy boundary: is penalty application inside the normative ARI object?
2. If inside: one penalty function with units, trigger and interaction with clamping.
3. If outside: a statement of what evidence must record so that a penalized value is never
   mistaken for a measurement.

---

# DOMAIN 12 — OUTPUT BOUNDS

## ARI-D-016 — Are ARI output bounds normative, and if so, what are they and where are they enforced?

> **Framing carried from the task.** The documented `[0, 100000]` range and observed values
> exceeding it are **not enough to select a resolution**. The decision is framed as: *"Are ARI
> output bounds normative, and if so, what are they?"*

**A — WHAT MUST BE DEFINED**
(i) whether bounds are a normative property of ARI; (ii) the bound values; (iii) whether the
bound is achieved by clamping, by rejection, or by an input precondition that makes
out-of-range impossible; (iv) the enforcement point; (v) the same four questions for drift.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:53-54` — "RAW_ARI ∈ [0, 100000] …
> ARI ∈ [0, 100000]"; `:59` — "RAW_ARI clamped to [0, 100000] at Layer 0".
> STATUS: IMPL-DOC, self-declared FROZEN · INTERPRETATION: a documented range and a documented
> clamping claim.

> `aura-poc-a-core-v3.3/core/evaluator.py:79` — `raw_ari = max(0, raw_ari)`.
> TIER: IMPL-CODE · INTERPRETATION: a **lower** clamp only. No upper clamp exists at this site.
> The documentation's "clamped to [0, 100000]" and this line diverge. **Recorded; not fixed.**

> `aura-poc-a-core-v3.3/compliance/consistency.py:62` —
> `final_score = max(0, min(self.SCALING_FACTOR, score))`.
> TIER: IMPL-CODE · INTERPRETATION: the second engine applies both clamps. The two engines
> differ on bounding.

> `aura-poc-a-core-v3.3/init.sql:16` — `poca_score DECIMAL(3,2) … CHECK (poca_score >= 0.0 AND
> poca_score <= 1.0)`; `:43-46` — `RAW_ARI … BETWEEN 0 AND 100000`.
> TIER: IMPL-CODE (DDL) · INTERPRETATION: bounds asserted at the persistence boundary.

> `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §5.4 records
> measured values `{'ari': 310000}` and `{'ari': 107550000}` for non-unit inputs, and
> `drift = 200000` for anti-aligned input.
> TIER: REVIEW · INTERPRETATION: evidence that the documented range and the executed behaviour
> differ for inputs that violate an unstated precondition. Per the task framing, this is **not
> sufficient to select a resolution**: it is equally consistent with "bounds are normative and
> enforcement is missing" and with "the input precondition is normative and these inputs are
> inadmissible".

**C — NON-NORMATIVE CANDIDATES** → C-37 (`[0, scale]` with clamping), C-38 (lower clamp only),
C-39 (`[0, scale]` enforced at persistence), C-40 (bounds as a consequence of a unit-norm input
precondition rather than an output rule).

**D — EVIDENCE REQUIRED**
1. A ruling on whether bounds are normative for ARI and, separately, for drift.
2. If normative: the values, the enforcement mechanism, and the enforcement point.
3. A statement of the relationship between bounds and the input precondition (ARI-D-013 item 3):
   whether bounds are an independent rule or a derived property.
4. Fixtures at and beyond each bound under the decided input contract.

---

# DOMAIN 13 — ERROR / MALFORMED INPUT HANDLING

> **Framing carried from the task.** Do **not** assume fail-closed means any particular numerical
> output. Four questions are kept separate: what constitutes invalid input · detection ·
> response · audit representation. They are ARI-D-017, ARI-D-018, ARI-D-019 and ARI-D-020.

## ARI-D-017 — What constitutes invalid ARI input?

**A — WHAT MUST BE DEFINED**
The enumerated set of conditions that make an ARI input invalid. Candidate condition classes
observed in repository material (each requiring a separate ruling): dimension mismatch between
operands · dimension not equal to a required dimension · empty vector · zero vector · element
magnitude exceeding the scale · non-integer elements · missing required fields · absent
constitution vector · unnormalized operands.

**B — EXISTING STATE**

> `aura-specification/specification/APS-001_PROTOCOL_SPECIFICATION.md:64-66` — "### 8. Error
> Handling — **TODO**: Define the fail-closed behavior. What conditions trigger a halt? What
> constitutes a 'safe state'?"
> STATUS: TODO · TIER: SPEC-APS · INTERPRETATION: the trigger set is explicitly unauthored.

> `aura-specification/invariants/INVARIANT_REGISTRY.md` INV-008 — "**Requirement (MUST)**: In
> case of error, an implementation MUST terminate execution in a safe state. No partial output
> MUST be generated or persisted."; Class Critical; Related APS "APS-001 §8"; Conformance Test
> CONF-007.
> STATUS: INV-REG-001 v1.0-DRAFT · TIER: SPEC-APS (draft) · INTERPRETATION: an obligation
> conditioned on the word "error", whose defining section (APS-001 §8) does not exist. The
> obligation exists; its trigger set does not.

> `aura-specification/specification/SPEC-002…:292-314` (REQ-002-031) — enumerates failure
> conditions a future specification must address, including "numeric overflow", "numeric
> out-of-domain value", "invalid transformation input"; governing principle: "**NO SILENT
> FALLBACK WHERE IT CAN ALTER THE CANONICAL RESULT.**"
> STATUS: v0.3-DRAFT, normative effect NONE · TIER: SPEC-DRAFT · INTERPRETATION: an
> enumeration of what must be decided, scoped to the Constitution Artifact contract, not to ARI.

> `aura-poc-a-core-v3.3/core/evaluator.py` — no validation of length, magnitude, type or
> emptiness at `:13-23` or `:50-91`.
> `aura-poc-a-core-v3.3/compliance/consistency.py:81-91` — validates emptiness, all-zero, and
> magnitude; does **not** validate length.
> TIER: IMPL-CODE · INTERPRETATION: two engines with two different invalid-input sets, neither
> derived from a specification.

**C — NON-NORMATIVE CANDIDATES** → C-41 (no invalid inputs at the Layer 0 boundary), C-42
(empty/zero/over-magnitude invalid; length unconstrained).

**D — EVIDENCE REQUIRED**
1. An enumerated invalid-input set for ARI, decided condition by condition.
2. A statement of which conditions are ARI's responsibility and which belong upstream.
3. An explicit ruling on whether "unnormalized operand" is an invalid input or an admissible
   input with defined behaviour.

---

## ARI-D-018 — Is detection of invalid input obligatory, and where?

**A — WHAT MUST BE DEFINED**
Whether a conformant implementation must actively detect each invalid condition (versus being
permitted to assume a validated caller), and at which boundary detection occurs.

**B — EXISTING STATE**

> `aura-poc-a-core-v3.3/core/evaluator.py:15-19` — docstring: "Initialize evaluator with
> **pre-normalized** int32 constitution vector"; `:60-61` — "vector: Agent action vector (int32,
> scaled by 10^5)".
> TIER: IMPL-CODE · INTERPRETATION: preconditions stated in prose, unchecked in code — i.e. an
> assumed-caller posture.

> `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:23` — "RI-002 Validation Layer | ✅ |
> schema validation as circuit breaker"; `:55` — "INV-008 | ✅ | ARI=0 circuit breaker".
> STATUS: RI-PY v3.3, NOT CERTIFIED · TIER: SPEC-APS registry entry · INTERPRETATION: a
> registry claim about an implementation. Per RD-1 premise 5 and boundary 21, RI-PY is not
> normative authority; and `review/…/05_CORE_REMEDIATION_READINESS.md` §7.1 records that the
> claim is not supported for the mismatched-length input class. Recorded as a claim, adjudicated
> by nobody.

**C — NON-NORMATIVE CANDIDATES** → C-43 (assumed-caller / no detection), C-44 (engine-side
detection for a subset).

**D — EVIDENCE REQUIRED**
1. A ruling on the detection obligation per invalid condition from ARI-D-017.
2. The boundary at which detection occurs, expressed against the decided input contract.
3. Whether detection itself must be evidenced (i.e. is a validation step auditable?).

---

## ARI-D-019 — What is the required response to invalid input?

**A — WHAT MUST BE DEFINED**
The required behaviour once an invalid input is detected — as a *behaviour*, not as a numeric
value. Candidate response classes: raise/abort with no output · return a defined error object ·
return a sentinel numeric value · reject upstream so ARI is never invoked.

> **Explicit constraint carried from the task:** fail-closed **must not** be assumed to mean any
> particular numerical output. In particular, "ARI = 0" is a candidate response, not a
> consequence of INV-008.

**B — EXISTING STATE**

> `aura-specification/invariants/INVARIANT_REGISTRY.md` INV-008 — "terminate execution in a safe
> state. No partial output MUST be generated or persisted." `aura-specification/glossary/
> GLOSSARY.md:57-58` — "Fail Closed … execution MUST halt safely. No partial output is
> permitted."; `aura-specification/constitution/AURA_CONSTITUTION.md` Article IV Principle 6 —
> "**Fail Closed by Default.** In the absence of valid input or valid policy, execution MUST
> halt safely."
> STATUS: Constitution v1.0 FROZEN; registry and glossary DRAFT · TIER: SPEC-CON / SPEC-APS ·
> INTERPRETATION: a halting obligation is stated at constitutional level. **What "safe state"
> is** remains undefined (APS-001 §8 TODO), and no numeric ARI value is implied by any of these
> texts.

> `aura-specification/conformance/CONF-007_FAIL_CLOSED.md:46` — "Implementation MUST return a
> safe-state response. No partial Evidence MUST be persisted. Safe-state exit code or error
> response MUST be returned."; `:5` — `Status: DRAFT`; `:34` — "**TODO**: Specify exact
> preconditions once APS-200 schemas and APS-500 fixtures are finalized."
> TIER: SPEC-APS (draft conformance test) · INTERPRETATION: the closest thing to a response
> specification; DRAFT, with its preconditions unspecified and its fixture (FIX-ERROR) absent.

> `aura-poc-a-core-v3.3/compliance/consistency.py:87-91` — raises `ValueError` on
> over-magnitude; `:52` — returns `{"score": 0, "status": "FAIL"}` on structural failure;
> `:81-82` — returns `0` for empty/zero vectors.
> TIER: IMPL-CODE · INTERPRETATION: three different response classes in one engine
> (raise / error object / sentinel value).

> `aura-poc-a-core-v3.3/compliance/policy.py:27,36` — `raise ValueError` for a non-machine
> target; `raise Exception("POLICY_HALT: …")` for a halted agent.
> TIER: IMPL-CODE · INTERPRETATION: a fourth and fifth response shape on adjacent paths.

**C — NON-NORMATIVE CANDIDATES** → C-45 (raise/abort), C-46 (error object with `status`),
C-47 (sentinel `0`), C-48 (upstream rejection).

**D — EVIDENCE REQUIRED**
1. A response class decided per invalid condition, expressed behaviourally.
2. An explicit statement of whether any numeric ARI value may be emitted on an invalid input,
   and if so, whether that value is distinguishable in evidence from a computed measurement.
3. A definition of "safe state" for an ARI computation (APS-001 §8 or successor).

---

## ARI-D-020 — How is an invalid-input outcome represented in the audit record?

**A — WHAT MUST BE DEFINED**
Whether a failed ARI computation produces an evidence artifact at all; if so, its shape; and how
a consumer distinguishes "no measurement" from "measurement equal to zero".

**B — EXISTING STATE**

> `aura-specification/invariants/INVARIANT_REGISTRY.md` INV-008 — "No partial output MUST be
> generated **or persisted**".
> TIER: SPEC-APS (draft) · INTERPRETATION: an obligation about persistence, without a definition
> of what a non-partial failure record would be.

> `aura-poc-a-core-v3.3/compliance/certificate.py:41-46,53-61` — the certificate carries
> `ari_score: float`, `drift: float`, `status: str`, plus `leaf_hash` / `merkle_root`; there is
> no field distinguishing "not computed" from "computed as 0.0".
> TIER: IMPL-CODE · INTERPRETATION: current evidence shape cannot express the distinction.

> `aura-poc-a-core-v3.3/init.sql:18` — `status VARCHAR(20) … CHECK (status IN ('COMPLIANT',
> 'DRIFT', 'FAIL', 'HALTED'))`.
> TIER: IMPL-CODE (DDL) · INTERPRETATION: a persisted status vocabulary exists at the database
> boundary; it is not derived from any specification, and APS-200 §5 ENT-003 marks the canonical
> `decision` value set "TODO" (`aps/APS-200_CANONICAL_DATA_MODEL.md:108`).

**C — NON-NORMATIVE CANDIDATES** → C-49 (status enum `COMPLIANT/DRIFT/FAIL/HALTED`), C-50
(exception, no record), C-51 (record with sentinel value and no failure marker).

**D — EVIDENCE REQUIRED**
1. A ruling on whether failure produces evidence.
2. If yes: the failure record schema and its relationship to APS-200 ENT-003 / APS-300.
3. An explicit distinguishability requirement between "no measurement" and "measurement 0".

---

# DOMAIN 14 — OVERFLOW / RANGE HANDLING

## ARI-D-021 — What overflow and range behaviour is required for ARI arithmetic?

**A — WHAT MUST BE DEFINED**
Explicitly, for each arithmetic position (element product, accumulator, rescaled term, sum,
output): the representable range · what constitutes overflow · the required behaviour on
overflow (wrap / saturate / trap / arbitrary precision / rejected by precondition) · and whether
overflow is a fail-closed trigger under ARI-D-017.

**B — EXISTING STATE**

> `aura-specification/specification/SPEC-002…:141` (REQ-002-014) — a numeric representation must
> include "**overflow behavior**"; `:304` (REQ-002-031) — failure conditions must address
> "numeric overflow" and "numeric out-of-domain value"; `:381` — AD-CA-007 UNRESOLVED.
> STATUS: v0.3-DRAFT, normative effect NONE · TIER: SPEC-DRAFT · INTERPRETATION: the obligation
> to decide is recorded in the specification corpus; the decision is not.

> `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` Article I §1 — "Integer-only arithmetic
> (int32/int64)"; `:510` — "`int64` accumulator with `10^5` scaling".
> TIER: IMPL-DECREE (DISPUTED AUTHORITY — SCOPE UNRESOLVED) · INTERPRETATION: names widths; does
> not state overflow behaviour.

> `aura-poc-a-core-v3.3/core/evaluator.py:40` — accumulation in Python `int` (arbitrary
> precision); no width bound exists at runtime.
> TIER: IMPL-CODE · INTERPRETATION: in the executing implementation, overflow cannot occur; in a
> fixed-width port it can. The question is therefore latent in this language and active in
> others.

> `review/2026-08-11_ENGINEERING_BASELINE/04_DETERMINISM_AUDIT.md` §D-4 — measured
> `dot = 15,360,000,000,000` at 1536 dimensions and scale bound; notes a Rust `i32` port would
> panic in debug and wrap in release.
> TIER: REVIEW · INTERPRETATION: cross-language evidence that the behaviour differs by target;
> not authority.

**C — NON-NORMATIVE CANDIDATES** → C-52 (int64 accumulator, no stated overflow rule), C-53
(arbitrary precision), C-54 (overflow as a REQ-002-031-style rejection condition).

**D — EVIDENCE REQUIRED**
1. A representable range per arithmetic position, derived from the decided dimension (ARI-D-006)
   and quantization (ARI-D-007).
2. A required overflow behaviour, stated per position.
3. A ruling on whether arbitrary precision is conformant, given that at least one target
   language provides it and others do not.
4. A worst-case magnitude analysis at the decided dimension and scale, as evidence that the
   chosen width cannot overflow for admissible inputs — or a defined behaviour if it can.

---

# DOMAIN 15 — SERIALIZATION / REPRESENTATION

## ARI-D-022 — What is the normative representation and serialization of ARI outputs?

**A — WHAT MUST BE DEFINED**
The canonical external representation of the ARI result: field names, types, integer-vs-decimal
form, the canonical byte sequence for any hashed representation, and which fields are inside the
hash domain.

**B — EXISTING STATE — THREE JSON CANONICALIZATIONS IN ONE REPOSITORY**

> `aura-poc-a-core-v3.3/audit/merkle.py:85` —
> `json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")`.
> `aura-poc-a-core-v3.3/core/merkle.py:8` — `json.dumps(data, sort_keys=True)` (default
> separators).
> `aura-poc-a-core-v3.3/compliance/certificate.py:69` — `json.dumps(self.to_dict(),
> sort_keys=True)` (default separators).
> TIER: IMPL-CODE · INTERPRETATION: three serialization sites feeding hashes, two of which use
> default separators and one compact separators. The same logical object hashed through
> different sites yields different bytes. **Recorded; not fixed.**

> `aura-poc-a-core-v3.3/compliance/certificate.py:53-57` — the emitted `ari` object is
> `{score, drift, status}` with float `score`.
> `aura-poc-a-core-v3.3/init.sql:32-46` — the persisted certificate is expected to carry an
> integer field named `RAW_ARI`.
> TIER: IMPL-CODE · INTERPRETATION: two different external shapes for the same measurement.

> `aura-specification/aps/APS-200_CANONICAL_DATA_MODEL.md:218` — "**TODO**: Define the canonical
> serialization format for interoperability between RI-PY and RI-RS."; `:224` — "**TODO**:
> Publish JSON Schema definitions for each entity".
> STATUS: 1.0-DRAFT · TIER: SPEC-APS · INTERPRETATION: the canonical serialization the ARI
> record would use is explicitly unauthored. INV-003 (Canonical Serialization, Critical) exists
> without the format it requires.

> `aura-specification/specification/SPEC-002…:215-226` (REQ-002-021/022) — require exactly one
> canonical serialization and one canonical byte sequence per hash domain per representation;
> `:382` — AD-CA-008 UNRESOLVED.
> TIER: SPEC-DRAFT · INTERPRETATION: scoped to the Constitution Artifact/Vector, not to ARI; the
> pattern of requirement is directly transferable but the decision does not exist.

**C — NON-NORMATIVE CANDIDATES** → C-55 (`sort_keys=True` + compact separators), C-56
(`sort_keys=True` + default separators), C-57 (integer `RAW_ARI` field), C-58 (float
`ari.score` field).

**D — EVIDENCE REQUIRED**
1. A single canonical representation for ARI outputs, with field names, types and ordering.
2. A canonical byte sequence definition for any hashed ARI-bearing representation, with
   inclusion/exclusion of fields stated (the REQ-002-017…022 pattern).
3. A ruling on whether the decimal/float presentation form is inside the conformance surface
   (links to ARI-D-012).

---

# DOMAIN 16 — REFERENCE MODEL

## ARI-D-023 — Is there a normative reference model for ARI, and what is its status relative to the specification?

**A — WHAT MUST BE DEFINED**
Whether a reference model exists in the normative sense; if so, which artifact it is and what
authority it carries; whether an implementation may ever be cited as the definition; and, given
two ARI engines exist in one repository, which is in scope for any such designation.

**B — EXISTING STATE**

> `aura-specification/specification/SPEC-002…:37` — "Implementation behaviour does not
> constitute normative evidence unless an approved governance artifact explicitly grants that
> implementation normative authority."; `:291` (REQ-002-030) — independent verification "MUST
> NOT require inspection of any Reference Implementation".
> STATUS: v0.3-DRAFT · TIER: SPEC-DRAFT · INTERPRETATION: the corpus states the direction of
> authority even in a draft; no such grant exists for RI-PY.

> `aura-specification/aps/APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md:130-134` — RI-PY
> listed as a supported Reference Implementation, "Status: Active"; `:120-124` — an
> implementation "MAY be marked Aura Reference Implementation if: All APS-950 requirements are
> satisfied; All mandatory APS-400 tests return PASS; …".
> STATUS: 1.0-DRAFT · TIER: SPEC-APS · INTERPRETATION: a registry listing plus a certification
> condition set that is not met.

> `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:7` — "APS-950 Certification Status:
> **NOT CERTIFIED**"; `:25-26` — "RI-004 Conformance Runner ❌ MISSING", "RI-005 Fixture Loader
> ❌ MISSING".
> TIER: SPEC-APS registry entry · INTERPRETATION: consistent with RD-1 premise 5 — a
> registry/reference entry, not a normative definition. **Boundary 21 applies: RI-PY is not
> treated as normative authority anywhere in this package.**

> Two engines exist in the implementation corpus:
> `aura-poc-a-core-v3.3/core/evaluator.py` (+ `compliance/evaluator_wrapper.py`) and
> `aura-poc-a-core-v3.3/compliance/consistency.py`. Their validation, clamping and penalty
> behaviour differ (see ARI-D-005, ARI-D-013, ARI-D-015, ARI-D-016).
> TIER: IMPL-CODE · INTERPRETATION: any designation decision must first state **which** engine
> is being spoken about; the corpus nowhere does.

**C — NON-NORMATIVE CANDIDATES** → C-59 (RI-PY as reference exemplar), C-60 (engine A),
C-61 (engine B), C-62 (a specification-only model with no reference implementation).

**D — EVIDENCE REQUIRED**
1. A ruling on whether a reference model is normative, advisory, or absent by design.
2. If normative: the artifact, its version binding, and the governance act that grants it
   authority (per SPEC-002 `:37`).
3. A statement resolving the two-engine ambiguity before any designation can be meaningful.

---

# DOMAIN 17 — CONFORMANCE CONTRACT

## ARI-D-024 — What conformance obligation attaches to ARI, and how is it tested?

**A — WHAT MUST BE DEFINED**
Which conformance tests bind ARI; their PASS criteria in terms of ARI outputs; whether ARI
conformance is separable from evidence-pack conformance; and what an implementation must
demonstrate to claim ARI conformance.

**B — EXISTING STATE**

> `aura-specification/aps/APS-400_CONFORMANCE_TEST_MATRIX.md:53-64` — all ten CONF tests carry
> `Status: DRAFT`. CONF-001 PASS criterion: "All output fields are bit-identical across multiple
> executions with the same input." CONF-006 PASS criterion: "Same Evidence Pack produced on x86
> and ARM platforms."
> STATUS: 1.0-DRAFT · TIER: SPEC-APS · INTERPRETATION: CONF-001 as written is satisfiable by any
> deterministic function, including one with undecided semantics; it tests repeatability, not
> correctness against a definition.

> `aura-specification/conformance/CONF-001_DETERMINISTIC_EVALUATION.md:34` — "**TODO**: Specify
> exact preconditions once APS-200 schemas and APS-500 fixtures are finalized."; `:73` —
> "Related Fixture | FIX-001 (TODO: assign specific fixture)".
> TIER: SPEC-APS (draft) · INTERPRETATION: the test cannot be executed as specified.

> `aura-specification/aps/APS-100_PROTOCOL_INVARIANTS.md:86` — INV-010: "Every Invariant MUST
> have a corresponding Conformance Test"; `:48,53-56` — INV-007, INV-012, INV-013, INV-014,
> INV-015 have no CONF test in the catalogue.
> TIER: SPEC-APS (draft) · INTERPRETATION: an internal completeness gap recorded by the corpus
> itself.

> `aura-specification/compliance/TRACEABILITY_MATRIX.md:18-32` — every row's RI-PY and RI-RS
> status is **NOT VERIFIED**; INV-008's row shows "APS-001 §8 (TODO)" and "FIX-ERROR (TODO)".
> TIER: SPEC-APS (draft, COMP-TM-002 v1.0-DRAFT) · INTERPRETATION: no conformance link for any
> invariant has been verified against a running implementation.

**C — NON-NORMATIVE CANDIDATES** → C-63 (CONF-001 repeatability as the ARI conformance test),
C-64 (CONF-006 cross-platform equality), C-65 (CONF-007 fail-closed).

**D — EVIDENCE REQUIRED**
1. A ruling on which CONF tests bind ARI and what their PASS criteria are in ARI terms.
2. A statement on whether repeatability-only tests are sufficient, given they pass under any
   division or rounding rule.
3. Advancement of the relevant CONF documents beyond DRAFT, with preconditions specified.

---

# DOMAIN 18 — REFERENCE FIXTURES

## ARI-D-025 — What fixture set defines conformant ARI behaviour, and what authority does a fixture carry?

**A — WHAT MUST BE DEFINED**
Whether ARI conformance is fixture-based; the fixture format for ARI inputs/outputs; the
governance act that grants a fixture normative status; and the categories required
(core / boundary / error / replay).

**B — EXISTING STATE**

> `aura-specification/aps/APS-500_REFERENCE_FIXTURES.md:63` — "**TODO**: Canonical fixture data
> requires APS-200 entity schemas and APS-300 Evidence Pack format to be finalized before
> fixtures can be specified."; `:65-70` — FIX-001 "**Status**: TODO".
> STATUS: 1.0-DRAFT · TIER: SPEC-APS · INTERPRETATION: fixture authoring is explicitly blocked
> upstream.

> `aura-specification/fixtures/core/FIX-001_BASIC_EVALUATION.json` — every payload field is
> `"TODO"`; `"_status": "TODO"`; `"protocol_version": "TODO"`.
> TIER: SPEC-APS artifact · INTERPRETATION: the only fixture file in the corpus contains no
> values. Consistent with RD-1 premise 7 (no normative ARI fixture instance).

> `aura-specification/aps/APS-500_REFERENCE_FIXTURES.md:81` — "A fixture whose Expected Output
> changes becomes a new fixture with a new ID. Old fixtures are deprecated, not modified."
> TIER: SPEC-APS (draft) · INTERPRETATION: a lifecycle rule exists for fixtures that do not yet
> exist.

> `aura-poc-a-core-v3.3/core/test_ari_observability.py:138-144` —
> `IMPLEMENTATION_DERIVED_NON_NORMATIVE = {"OBS-1": {"ari": 100000, "drift": 0}, … "OBS-5":
> {"ari": 29999, "drift": 100001}}`; module docstring `:5-16` — "CURRENT BEHAVIOUR ≠ NORMATIVE
> REQUIREMENT … It does NOT record: 'This is what Aura requires.'"
> STATUS: test module, self-declared characterization · TIER: IMPL-TEST · INTERPRETATION:
> characterization observations. **Boundary 23 applies: these are not converted into expected
> normative values anywhere in this package.** They are listed in
> `03_NON_NORMATIVE_CANDIDATES.md` as observations, not as candidate fixture expectations.

**C — NON-NORMATIVE CANDIDATES** → C-66 (APS-500 fixture structure as the container),
C-67 (the RD-006 observation record shape as a machine-readable record format).

**D — EVIDENCE REQUIRED**
1. A ruling on whether ARI conformance is fixture-based.
2. A fixture format for ARI (inputs, expected outputs, tolerance-or-exactness statement).
3. The governance act that would grant a fixture normative status — noting that per the
   provenance rule, a fixture value is not authority unless a governing decision grants it.
4. Resolution of the upstream blockers APS-500 itself names (APS-200 schemas, APS-300 pack).

---

# DOMAIN 19 — CROSS-LANGUAGE EQUIVALENCE

## ARI-D-026 — What must "equivalent" mean before independent Python/Rust/JS implementations can be judged conformant?

> **Framing carried from the task.** Define what "bit-equivalent" or "semantically equivalent"
> must mean *before* independent implementations can be judged.

**A — WHAT MUST BE DEFINED**

1. **The comparison object** — are two implementations compared on the integer ARI value, on a
   serialized byte sequence, on a hash, or on an evidence pack?
2. **The equivalence relation** — exact equality, equality modulo a stated tolerance, or
   equality of a canonical encoding.
3. **The input set over which equivalence must hold** — all admissible inputs, or a fixture set.
4. **The treatment of inadmissible inputs** — must implementations agree on *failure*, and on
   the failure's representation?
5. **The language-dependent constructs that must be neutralized** — division on negative
   dividends, rounding ties, integer width/overflow, accumulation order, string/JSON encoding.
6. **The observation surface** — what must be emitted so equivalence is *checkable* rather than
   asserted.
7. **The platform set** — which architectures and language runtimes are in scope.

**B — EXISTING STATE**

> `aura-specification/aps/APS-100_PROTOCOL_INVARIANTS.md:62` — INV-002: "Replay of an execution
> MUST reproduce an identical result on **every conformant implementation**"; `:74` — INV-006:
> "An implementation MUST produce conformant results regardless of hardware platform or
> operating system".
> STATUS: 1.0-DRAFT · TIER: SPEC-APS · INTERPRETATION: cross-implementation identity is required
> at invariant level, over a computation whose semantics are undecided. The word "identical" is
> not defined against a comparison object.

> `aura-specification/specification/SPEC-002…:325-337` (§5.1) — the positive determinism chain
> "same authoritative source → same artifact → same vector → same canonical bytes → same hash
> values", with the PASS condition that "any two conformant independent implementations produce
> identical artifacts, vectors, canonical byte sequences, and hash values".
> `:498-537` (§10) — the Independent Implementer Test, requiring construction "without
> inspecting any Reference Implementation".
> STATUS: v0.3-DRAFT, normative effect NONE · TIER: SPEC-DRAFT · INTERPRETATION: an existing,
> fully articulated *pattern* for what equivalence must mean — stated for the Constitution
> Artifact, not for ARI. Its transfer to ARI is itself a decision.

> `aura-specification/aps/APS-950…:130-134` — RI-PY (Python) and RI-RS (Rust) are both listed as
> Active reference implementations.
> TIER: SPEC-APS (draft) · INTERPRETATION: the corpus anticipates at least two languages; the
> constructs enumerated in A.5 are exactly where those two diverge.

> `aura-poc-a-core-v3.3/docs/ADR_005_NO_FLOAT_RUNTIME.md:60` — "Same Input → Identical Bits →
> Identical Hash"; `:391` — "Same input → Identical bits on x86 / ARM / WASM".
> TIER: IMPL-DOC · INTERPRETATION: an implementation-corpus statement of the same goal, scoped
> to architectures rather than to languages.

**C — NON-NORMATIVE CANDIDATES** → C-68 (bit-identity of a canonical byte sequence), C-69
(equality of integer outputs), C-70 (equality of evidence-pack hashes), C-71 (SPEC-002 §5.1
chain applied to ARI).

**D — EVIDENCE REQUIRED**
1. A definition of the comparison object and the equivalence relation.
2. An enumeration of language-dependent constructs that the ARI specification must pin
   (each of which is a decision above: ARI-D-008, -010, -011, -021, -022).
3. A defined observation surface, i.e. what an implementation must emit for equivalence to be
   verifiable.
4. A decided platform/runtime set for conformance claims.

---

# DOMAIN 20 — AUDIT / REPRODUCIBILITY REQUIREMENTS

## ARI-D-027 — What must be recorded for an ARI value to be independently reproducible?

**A — WHAT MUST BE DEFINED**
The complete record required to reproduce an ARI value later, by a third party: the input, the
constitution artifact/vector identity, the dependency closure (embedding method, dictionary,
constants), the specification version, the implementation identity, and the binding between
them.

**B — EXISTING STATE**

> `aura-specification/specification/SPEC-002…:246-260` (REQ-002-034) — the dependency-closure
> requirement: "Every external or auxiliary dependency capable of affecting the canonical
> artifact, vector, canonical byte sequence, or hash MUST be explicitly identified, versioned
> where applicable, integrity-bound"; `:237` (REQ-002-033) — provenance boundary must be
> explicitly defined; `:384` — AD-CA-010 UNRESOLVED.
> STATUS: v0.3-DRAFT · TIER: SPEC-DRAFT · INTERPRETATION: the closure and provenance
> requirements exist as requirements-to-decide, scoped to the Constitution Artifact.

> `aura-specification/aps/APS-200_CANONICAL_DATA_MODEL.md:49-58` — the Common Object Contract
> (`object_id`, `object_type`, `protocol_version`, `schema_version`, `created_at`,
> `integrity_hash`) that every entity MUST carry.
> STATUS: 1.0-DRAFT · TIER: SPEC-APS · INTERPRETATION: an existing field pattern that an ARI
> record would have to satisfy; no ARI entity is defined in APS-200.

> `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:56` — "INV-009 | ❌ | No
> protocol_version in evidence objects"; `:52` — "INV-005 | ❌ | No APS/INV references in
> evidence".
> TIER: SPEC-APS registry entry · INTERPRETATION: registry-recorded gaps in the current
> evidence surface. Not authority; recorded as state.

> `aura-poc-a-core-v3.3/core/embedding.py:2-3` — "Placeholder for deterministic embedding …
> MUST be frozen + reproducible in production."
> TIER: IMPL-CODE · INTERPRETATION: the embedding dependency — an element of the closure — is
> explicitly a placeholder in the implementation and undecided in the specification
> (AD-CA-005/006).

**C — NON-NORMATIVE CANDIDATES** → C-72 (APS-200 Common Object Contract as the record header),
C-73 (RD-006 runtime-identity record fields), C-74 (Merkle/ETC certificate as the audit
artifact).

**D — EVIDENCE REQUIRED**
1. An enumerated reproduction record for ARI, field by field.
2. A dependency-closure statement for the ARI computation specifically (embedding, dictionary,
   constants, constitution vector identity).
3. A ruling on whether execution provenance is inside or outside the hashed representation
   (the ARI analogue of REQ-002-033).
4. A demonstration that the record is sufficient: a third party reproducing an ARI from the
   record alone, without inspecting an implementation.

---

*This document has no normative effect. It creates identifiers for open questions. It selects no
ARI semantics, ranks no candidate, creates no ADR, amends no specification, and modifies no
code.*
