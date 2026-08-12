# 03 — NON-NORMATIVE CANDIDATES

**Package:** RD-1-ARI-DECISION-READINESS · **Normative effect:** NONE

---

## 0. Status of everything in this document

# NON-NORMATIVE CANDIDATE

Every entry below is a **NON-NORMATIVE CANDIDATE**. Listing a value, algorithm or model here:

- does **not** select it;
- does **not** rank it;
- does **not** recommend, prefer, or default to it;
- does **not** convert it into a requirement, an expectation, or a fixture value;
- carries **no** ordering significance — entries appear in discovery order within each domain.

The words *preferred, best, correct, optimal, should select, recommended* do not appear as this
package's own assessment anywhere in this document. Where such a word appears inside a quotation,
it is attributed to the quoted source and labelled source-derived at that point.

### Candidate class vocabulary

| Class | Meaning |
|---|---|
| **IMPLEMENTATION-DERIVED** | Obtained by reading or executing implementation code |
| **DOCUMENTARY** | Stated in implementation-corpus documentation about the implementation |
| **HISTORICAL** | Explicitly labelled by its own source as superseded / legacy |
| **DIRECTIVE** | Stated in a repository agent/Copilot directive or the Constitutional Decree |
| **DRAFT-SPEC CANDIDATE** | Listed by a DRAFT specification that explicitly denies it normative effect |
| **SCHEMA/DDL-DERIVED** | Encoded in a database schema or JSON schema sketch |
| **REGISTRY-DERIVED** | Recorded in a specification-corpus registry entry describing an implementation |
| **CHARACTERIZATION-OBSERVATION** | A recorded execution result, self-declared non-normative |

### The universal reason none of these can establish normative authority

Per the CLOSED RD-1 verdict (`00_SCOPE_AND_GOVERNING_CONTEXT.md` §3): **no normative ARI
definition exists**, and the implementation's observable behaviour is **not** normative
authority. In addition, the specification corpus states the direction of authority explicitly:

> "Implementation behaviour does not constitute normative evidence unless an approved governance
> artifact explicitly grants that implementation normative authority."
> — `aura-specification/specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:37`
> (v0.3-DRAFT; the document's own header states "**Normative effect: NONE until APPROVED**")

> "A higher-level document has authority over a lower-level document in all cases of conflict."
> — `aura-specification/constitution/AURA_CONSTITUTION.md` Article V (AURA-CON-001 v1.0, FROZEN),
> whose hierarchy places Implementation last.

No approved governance artifact granting any implementation normative ARI authority was found.
Per-entry reasons below are **additional** to this universal one.

---

## DOMAIN 1 — ARI IDENTITY

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-01** | `RAW_ARI = 0.3 × StructuralIntegrity + 0.7 × SemanticAlignment` | `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:8`; restated `core/evaluator.py:4`, `:75-76` (weights `30000`/`70000` at `:22-23`) | Document self-declared "**FROZEN** — Regulatory Audit Phase" (`:207`); no document ID, no version field, not an APS | DOCUMENTARY + IMPLEMENTATION-DERIVED | Repository documentation sits below APS-001/APS-100 in AURA-CON-001 Article V. It describes the implementation rather than specifying the protocol. `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md` §9 P-1 additionally records that this document's formula section was rewritten in place at commit `4ced103` while retaining its FROZEN marker, without version increment or superseding document — so its own stability is contested. |
| **C-02** | `ARI = SI · (0.5 · SA + 0.5 · F)` | `aura-poc-a-core-v3.3/.github/github/copilot-instructions.md:17` ("Physics:") | Repository Copilot directive; `CLAUDE.md` authority tier 4; file states "PROTOCOL FROZEN" (`:38`) | DIRECTIVE | States a *different* formula from C-01, with an undefined term `F`, and a multiplicative rather than additive structure. The directive is subordinate to the Constitutional Decree by its own text (`:9-10`) and defines no protocol authority. Its coexistence with C-01 is recorded as a contradiction, unresolved here. |
| **C-03** | ARI is "a deterministic measurement value computed by RI-PY using integer arithmetic" — i.e. definition by deferral to an implementation | `aura-specification/glossary/GLOSSARY.md:27-28` | GLOSSARY v1.0-**DRAFT**, `Authority: APS-000` | DRAFT-SPEC CANDIDATE (definition-by-reference) | Contains no mathematical content: no formula, range, dimension, division rule or rounding rule. It is the deferral RD-1 identified, not a definition. Deferring to RI-PY cannot itself grant RI-PY authority (boundary 21). |
| **C-04** | Naming set for the measured quantity: `RAW_ARI` (docs, DDL) / `ari` (Layer 0 return key) / `ari` (Layer 2 adjusted return key) | `docs/mathematical_foundation.md:8,23`; `core/evaluator.py:89`; `compliance/evaluator_wrapper.py:73`; `init.sql:32-46` | Mixed: documentation FROZEN-declared; code; DDL | DOCUMENTARY + IMPLEMENTATION-DERIVED + SCHEMA/DDL-DERIVED | Three names for two quantities, with one name (`ari`) carrying both quantities at different layers. No source designates which name is normative. |
| **C-05** | Acronym expansion: "**Aura** Reliability Index" · "**Agent** Reliability Index" | `aura-specification/glossary/GLOSSARY.md:27` · `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:186` ("**Required Term**") | DRAFT glossary · FROZEN-declared implementation documentation | DRAFT-SPEC CANDIDATE · DOCUMENTARY | The two corpora expand the acronym differently and neither cites the other. The "Required Term" phrasing at `:186` is the **source's own** normative language, applying within the implementation corpus; it does not bind the specification glossary. **CONTRADICTED.** |

---

## DOMAIN 2 — INPUT CONTRACT

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-06** | Input shape `(agent_id: str, vector: List[int], valid_schema: bool)` | `aura-poc-a-core-v3.3/core/evaluator.py:50`, docstring `:56-62` | Production code in an instrument whose FROZEN status is self-declared | IMPLEMENTATION-DERIVED | One of two coexisting shapes; neither is specified. `APS-001 §3` (Input Requirements) is `TODO`. |
| **C-07** | Input shape: event dict requiring `timestamp`, `embedding`, `content` | `aura-poc-a-core-v3.3/compliance/consistency.py:28,74-75` | Production code | IMPLEMENTATION-DERIVED | Second coexisting shape, incompatible with C-06 in both arity and typing. |
| **C-08** | Structural validity supplied by the caller as a boolean | `core/evaluator.py:50,67` | Production code | IMPLEMENTATION-DERIVED | Makes the structural term unauditable at the ARI boundary; no source specifies the caller's obligation. |
| **C-09** | Structural validity computed by the engine as an all-required-keys-present test | `compliance/consistency.py:72-75` | Production code | IMPLEMENTATION-DERIVED | Uses a required-key set that appears in no schema; `APS-200:92` marks the canonical `request_fields` schema TODO. |

---

## DOMAIN 3 — VECTOR DIMENSION

> **Framing constraint (task).** Neither the 1536 material nor the 1-element success case is
> treated as proof of any dimension requirement. Both appear here as candidates/observations.

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-10** | Dimension `1536` | `core/offline_normalizer.py:44` (`CONSTITUTION_DIM = 1536`), enforced only at `:171-175`; `core/embedding.py:13,20`; `compliance/certificate_schema.json:16` (`"semantic_space": "R1536"`); `docs/mathematical_foundation.md:116-118` | Code (offline path); a module whose own docstring calls itself a "Placeholder" (`core/embedding.py:2`); a schema file that `docs/GAP-001.md:208` describes as "a sketch … Schema not normative"; a documentation section self-labelled "⚠️ **HISTORICAL ONLY — NOT THE CURRENT RUNTIME**" (`:111-114`) | IMPLEMENTATION-DERIVED + HISTORICAL + SCHEMA/DDL-DERIVED | Every occurrence is either off the evaluation path, self-declared a placeholder, self-declared non-normative, or self-declared historical. The specification corpus states no dimension anywhere. Neither ARI engine references the constant. |
| **C-11** | Dimension unconstrained at the ARI boundary (any length accepted; `zip` truncates to the shorter operand) | `core/evaluator.py:40`; absence of any length check at `:13-23`, `:50-91`; `compliance/consistency.py` likewise has no length check | Production code | IMPLEMENTATION-DERIVED | An absence of validation is not a decision. Recording it as a candidate does not endorse it; the required behaviour is ARI-D-006/ARI-D-017, both open. **Not being fixed here** (boundaries 26, 24). |
| **C-12** | Operand lengths must be equal | No source. Derived as the complement of C-11 | — | — (no source) | Listed for completeness of the decision space. It appears in **no** repository material, which is itself the finding: the equality requirement has never been written down. |

---

## DOMAIN 4 — QUANTIZATION

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-13** | Decimal fixed-point scale `10^5 = 100,000` | `CONSTITUTIONAL_DECREE.md` Art. I §1 and §8; `core/evaluator.py:12`; `core/offline_normalizer.py:41`; `compliance/policy.py:18`; `compliance/consistency.py:18`; `docs/mathematical_foundation.md:42-48` | Decree: `Version 1.0`, `MANDATORY / NON-OVERRIDABLE`, `CLAUDE.md` tier 1 · code: production · docs: FROZEN-declared | DIRECTIVE + IMPLEMENTATION-DERIVED + DOCUMENTARY | Within the implementation corpus the Decree asserts binding force; whether that scope reaches a **protocol-level, cross-language** ARI is undecided (`09_OPEN_QUESTIONS.md` OQ-A/OQ-B) — recorded in `02` as **DISPUTED AUTHORITY — SCOPE UNRESOLVED**, which is not a NORMATIVE entry. The specification corpus independently lists `100000` as candidate-only (C-15) and states no candidate is a default. |
| **C-14** | Binary fixed-point `Q16.16` | `CONSTITUTIONAL_DECREE.md` Art. I §1 ("✔ Fixed-point arithmetic (Q16.16)"); `.github/copilot-instructions.md:20`; `.github/github/copilot-instructions.md:18` | Decree MANDATORY / NON-OVERRIDABLE; directives tier 4 | DIRECTIVE | Q16.16 (2^16 fractional scale) and the decimal scale of C-13 are different representations, listed together in the same article without a stated relationship. No source reconciles them, and no implementation uses Q16.16. **Contradiction recorded, not resolved.** |
| **C-15** | SPEC-002 numeric-representation candidate set: `32`, `100000`, `signed int32`, `little-endian`, `round-half-to-even` | `aura-specification/specification/SPEC-002…:108`, `:141` (REQ-002-014), `:381` (AD-CA-007) | v0.3-**DRAFT**; "**Normative effect: NONE until APPROVED**" (`:11`) | DRAFT-SPEC CANDIDATE | The source itself states: "**No candidate choice listed in this document constitutes a recommendation, preference, default, or implied architectural decision**" (`:108`, repeated `:371`). AD-CA-007 is recorded UNRESOLVED. Additionally, the set is scoped to **Constitution Vector values**; whether ARI operands fall inside that scope is itself undecided (ARI-D-007 D.3). |

---

## DOMAIN 5 — INTEGER REPRESENTATION

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-16** | Signed `int32` operands with an `int64` accumulator | `.github/github/copilot-instructions.md:22`; `CONSTITUTIONAL_DECREE.md` Art. I §1 and `:510`; SPEC-002 `:108` (`signed int32` candidate) | Directive tier 4 · Decree MANDATORY / NON-OVERRIDABLE · SPEC-002 v0.3-DRAFT with normative effect NONE | DIRECTIVE + DRAFT-SPEC CANDIDATE | The widths are stated as implementer guidance, never as an ARI numeric contract; no source states overflow behaviour to accompany them (ARI-D-021 open). SPEC-002's inclusion is explicitly candidate-only. |
| **C-17** | Arbitrary-precision integers throughout | `core/evaluator.py:40` executed under CPython; the name `vector_similarity_int32` (`:25`) constrains nothing | Production code | IMPLEMENTATION-DERIVED | This is a property of the executing language, not a decision. It is recorded because it makes the width question latent in the reference language and active in fixed-width targets. |

---

## DOMAIN 6 — ARITHMETIC SEMANTICS

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-18** | Rescale applied per weighted term before summation: `(w_s·SI)//scale + (w_a·SA)//scale` | `core/evaluator.py:75-76`; same shape at `compliance/consistency.py:57-61` | Production code | IMPLEMENTATION-DERIVED | An operation order read out of code. `docs/ADR_005_NO_FLOAT_RUNTIME.md:103` states a rescale-after-multiply convention but specifies no ARI-level order. |
| **C-19** | Rescale applied once after summation: `(w_s·SI + w_a·SA)//scale` | No source. Derived as the arithmetic alternative to C-18 | — | — (no source) | Listed to make the decision space complete. Its absence from all material is the finding: operation order has never been specified, only implemented. |

---

## DOMAIN 7 — DIVISION SEMANTICS

> **Framing (task).** The ADR-005 statement and the observed Python behaviour are a semantic
> conflict. It is **not resolved** here, and none of the following is fixed.

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-20** | Floor division (round toward −∞) for negative dividends | `core/evaluator.py:46,75-76`; `compliance/consistency.py:58-59,94` — the behaviour of Python's `//` at these six sites | Production code | IMPLEMENTATION-DERIVED | Behaviour of a language operator, never stated as a requirement by any source. Per RD-1 premise 9, implementation behaviour is not authority. |
| **C-21** | Truncation toward zero for negative dividends | `docs/ADR_005_NO_FLOAT_RUNTIME.md:134` — "Integer division (`//`) is deterministic (truncation toward zero)" | ADR-005: header `Status: APPROVED`, footer `Status: FROZEN (MC-READY 2026)`; an implementation-corpus document, not an `aura-specification/adrs/` ADR | DOCUMENTARY | The sentence describes the operator rather than imposing a rule, and its description does not hold for negative dividends in the language used. Whether it is a requirement or a mistaken description is exactly what ARI-D-010 must decide — **this package does not decide it**. |
| **C-22** | Negative dividends excluded by the input contract, making the rule vacuous | No source. Derived from the interaction of ARI-D-004/ARI-D-013 with ARI-D-010 | — | — (no source) | Listed because a division rule may be unnecessary if the decided similarity model and input contract cannot produce negative intermediates. Absence of any source statement is the finding. |

---

## DOMAIN 8 — ROUNDING SEMANTICS

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-23** | Round-half-to-even | `core/offline_normalizer.py:88` (Python `round()` behaviour); listed as candidate at SPEC-002 `:108`, `:381` | Production code (offline path) · SPEC-002 v0.3-DRAFT, normative effect NONE | IMPLEMENTATION-DERIVED + DRAFT-SPEC CANDIDATE | The implementation occurrence is behaviour, not a decision; the SPEC-002 occurrence is explicitly "candidate only" and explicitly not a default. |
| **C-24** | Round-half-away-from-zero | No repository source; recorded in `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §5.3 as the behaviour of other language runtimes | Prior review record, explicitly non-normative | CHARACTERIZATION-OBSERVATION (of other runtimes) | Not a repository decision; recorded so the decision space includes the tie rules that competing target languages implement by default. |
| **C-25** | Round-half-toward-+∞ | As C-24, same source section | Prior review record, explicitly non-normative | CHARACTERIZATION-OBSERVATION | As C-24. |
| **C-26** | Half-up rounding on the persistence path: `(RAW_ARI + 500) / 1000` | `aura-poc-a-core-v3.3/init.sql:57-61`, with the inline comment "Deterministic half-up cent rounding from integer RAW_ARI / 100000" | Database DDL in the implementation repository | SCHEMA/DDL-DERIVED | A rule for a *derived* representation at a persistence boundary that `review/…/04_DETERMINISM_AUDIT.md` records as unreached by any writer. It is not a statement about ARI's own quantization. |
| **C-27** | Binary float division for presentation: `ari_int32 / SCALING_FACTOR` | `compliance/certificate.py:29-31,41` | Production code; the same docstring states the conversion is "limited to the presentation/reporting layer" | IMPLEMENTATION-DERIVED | No rounding rule is stated for this reduction at all; whether the presented form is inside the conformance surface is ARI-D-012, open. |

---

## DOMAIN 9 — SIMILARITY FUNCTION

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-28** | Rescaled integer dot product with unit-norm operands **assumed** | `core/evaluator.py:25-48`; docstrings `:29-31` ("similarity ≈ dot_product / (SCALING_FACTOR)"), `:37` ("range approximately [-10^5, 10^5]"); `docs/mathematical_foundation.md:83-95`; `.github/github/copilot-instructions.md:21` | Production code · FROZEN-declared documentation · tier-4 directive | IMPLEMENTATION-DERIVED + DOCUMENTARY + DIRECTIVE | The sources use "≈" and "approximately"; none fixes the ten properties enumerated in ARI-D-013.A. The cosine-equivalence claim at `docs/mathematical_foundation.md:95` is explicitly conditional on a precondition the code does not verify. |
| **C-29** | Rescaled integer dot product with magnitude validation and a zero-vector guard | `compliance/consistency.py:81-94` | Production code | IMPLEMENTATION-DERIVED | A second, differently-constrained implementation of the same conceptual function in the same repository. Neither engine is designated (ARI-D-023, open). |
| **C-30** | Float cosine similarity with the mapping `(cos + 1) / 2` | `docs/mathematical_foundation.md:122-137` | Section carries "⚠️ **HISTORICAL ONLY — NOT THE CURRENT RUNTIME** … retained for audit traceability only" (`:111-114`); `:140-142` records the reason for removal | HISTORICAL | Self-declared historical by its own source; retained for traceability. Recorded so that the decision space includes the model the project previously used. |

---

## DOMAIN 10 — DRIFT DEFINITION

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-31** | `drift = min(max(0, scale − SA), 2 × scale)` | `core/evaluator.py:86` | Production code | IMPLEMENTATION-DERIVED | Behaviour, not decision; and it contradicts the docstring three lines above it (C-32). |
| **C-32** | `drift = scale − SA`, clamped to `[0, scale]` | `core/evaluator.py:85` (inline comment: "Clamp drift to [0, 100000] to represent [0.0, 1.0]") | Inline comment inside production code | DOCUMENTARY | Describes an intent the adjacent code does not implement. Which is required is ARI-D-014, open. **Not being fixed here.** |
| **C-33** | Drift threshold `68000` (sentinel `0.68`) | `compliance/policy.py:19,41`; `CONSTITUTIONAL_DECREE.md` Art. I §8 ("Sentinel Drift Threshold: 0.68 (FROZEN)"); `docs/mathematical_foundation.md:48` | Decree MANDATORY / NON-OVERRIDABLE (tier 1 of the `CLAUDE.md` ladder) · production code | DIRECTIVE + IMPLEMENTATION-DERIVED | **DISPUTED AUTHORITY — SCOPE UNRESOLVED** for the same reason as C-13. Separately: the constant is compared against the **semantic alignment** value in code, not against the emitted `drift` field, so even accepting the constant would not define drift. |

---

## DOMAIN 11 — PENALTY MODEL

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-34** | Threshold penalty: `150000` when `SA < 68000`, else `0` | `compliance/policy.py:19-20,41` | Production code | IMPLEMENTATION-DERIVED | Not specified anywhere; and the constant exceeds the documented maximum ARI (`100000`, `docs/mathematical_foundation.md:53`), a relationship no source explains. |
| **C-35** | Count penalty: `10000 × violation_count` | `compliance/consistency.py:21,101-102` | Production code | IMPLEMENTATION-DERIVED | A different unit and trigger from C-34, in the same repository. Neither is designated. |
| **C-36** | Composition rule `ARI = max(0, RAW_ARI − P)` with Layer-2 ownership of `P` | `docs/mathematical_foundation.md:23,27-29`; `compliance/evaluator_wrapper.py:70` | FROZEN-declared documentation · production code | DOCUMENTARY + IMPLEMENTATION-DERIVED | Documents the composition without fixing `P`; and `compliance/evaluator_wrapper.py:61` recomputes the Layer 0 similarity inside Layer 2, so the boundary the document asserts is crossed by the call graph. |

---

## DOMAIN 12 — OUTPUT BOUNDS

> **Framing (task).** The documented `[0,100000]` range and the observed values exceeding it are
> **not sufficient** to select a resolution. Both appear here as candidates/observations only.

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-37** | `ARI ∈ [0, scale]` enforced by clamping at the measurement layer | `docs/mathematical_foundation.md:53-59` ("RAW_ARI clamped to [0, 100000] at Layer 0"); implemented as both-sided clamping only in the second engine, `compliance/consistency.py:62` | FROZEN-declared documentation · production code | DOCUMENTARY + IMPLEMENTATION-DERIVED | The document asserts a clamp the primary engine does not implement (C-38); the engine that does implement it is a different, undesignated engine. |
| **C-38** | Lower clamp only: `max(0, …)`, no upper bound | `core/evaluator.py:79` | Production code | IMPLEMENTATION-DERIVED | Behaviour, not decision. **Not being fixed here** (boundary 27). |
| **C-39** | Bounds asserted at persistence: `RAW_ARI BETWEEN 0 AND 100000`; `poca_score DECIMAL(3,2) CHECK 0.0–1.0` | `init.sql:43-46`, `:16` | Database DDL | SCHEMA/DDL-DERIVED | Constrains a boundary that `review/…/04_DETERMINISM_AUDIT.md` records as unreached by any application writer; a persistence constraint is not a definition of the measurement. |
| **C-40** | Bounds as a *derived consequence* of a unit-norm input precondition, rather than an output rule | Implied by `core/evaluator.py:15-19,29-31` (pre-normalization stated as a precondition) and `docs/mathematical_foundation.md:93-95` | Production-code docstrings · FROZEN-declared documentation | DOCUMENTARY + IMPLEMENTATION-DERIVED | No source states this as a rule; it is the reading under which the out-of-range observations describe inadmissible inputs rather than a bounding failure. Recorded so the decision space contains both readings. |

---

## DOMAIN 13 — ERROR / MALFORMED INPUT HANDLING

> **Framing (task).** "Fail-closed" is **not** assumed to imply any particular numerical output.
> C-47 below is a candidate response, not a consequence of INV-008.

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-41** | No input is invalid at the measurement boundary (no validation) | `core/evaluator.py:13-23,50-91` — absence of any check | Production code | IMPLEMENTATION-DERIVED | An absence is not a decision. |
| **C-42** | Invalid = empty vector, all-zero vector, or element magnitude exceeding the scale; length unconstrained | `compliance/consistency.py:81-91` | Production code | IMPLEMENTATION-DERIVED | A partial, undocumented condition set from one of two engines. |
| **C-43** | Assumed-caller posture: preconditions stated in prose, unchecked | `core/evaluator.py:15-19,60-61` docstrings | Production-code docstrings | DOCUMENTARY | States preconditions without an obligation or a consequence. |
| **C-44** | Engine-side detection for a subset of conditions | `compliance/consistency.py:84-91` | Production code | IMPLEMENTATION-DERIVED | Partial; no source states which conditions must be detected. |
| **C-45** | Response: raise / abort (`ValueError`, `Exception`) | `compliance/consistency.py:87-91`; `compliance/policy.py:27,36` | Production code | IMPLEMENTATION-DERIVED | Three different raise sites with three different exception shapes; no source specifies a response class. |
| **C-46** | Response: error object with `status` field (`{"score": 0, "status": "FAIL"}`) | `compliance/consistency.py:52,104-110` | Production code | IMPLEMENTATION-DERIVED | Emits a numeric score alongside a failure marker — the exact ambiguity ARI-D-020 must resolve. |
| **C-47** | Response: sentinel numeric value `0` | `compliance/consistency.py:81-82`; and the registry claim "INV-008 ✅ ARI=0 circuit breaker" at `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:55` | Production code · RI-PY registry entry, "APS-950 Certification Status: NOT CERTIFIED" (`:7`) | IMPLEMENTATION-DERIVED + REGISTRY-DERIVED | Boundary 21: RI-PY is not treated as normative authority. `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §7.1 additionally records that the ✅ is unsupported for the mismatched-length input class. Listing this candidate does **not** imply fail-closed means ARI = 0. |
| **C-48** | Response: rejection upstream, so ARI is never invoked on invalid input | No source in either corpus | — | — (no source) | Listed for completeness of the response space; its absence is the finding. |
| **C-49** | Audit representation: status enum `COMPLIANT` / `DRIFT` / `FAIL` / `HALTED` | `init.sql:18` | Database DDL | SCHEMA/DDL-DERIVED | Derives from no specification; `aura-specification/aps/APS-200_CANONICAL_DATA_MODEL.md:108` marks the canonical `decision` value set "TODO". |
| **C-50** | Audit representation: exception propagates, no record produced | `compliance/policy.py:36`; `compliance/consistency.py:87-91` | Production code | IMPLEMENTATION-DERIVED | Leaves no evidence artifact; INV-008's "no partial output … or persisted" is silent on whether a *failure* record is required. |
| **C-51** | Audit representation: record carrying a sentinel value with no failure marker | `compliance/certificate.py:41-46,53-61` — no field distinguishes "not computed" from `0.0` | Production code | IMPLEMENTATION-DERIVED | Records the current inability to express the distinction; not a decision about how it should be expressed. |

---

## DOMAIN 14 — OVERFLOW / RANGE HANDLING

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-52** | `int64` accumulator with no stated overflow behaviour | `.github/github/copilot-instructions.md:22`; `CONSTITUTIONAL_DECREE.md:510` | Tier-4 directive · Decree MANDATORY / NON-OVERRIDABLE | DIRECTIVE | Names a width without stating what happens at its limit; SPEC-002 REQ-002-014 requires overflow behaviour to be part of the numeric representation, and AD-CA-007 is UNRESOLVED. |
| **C-53** | Arbitrary precision (overflow cannot occur) | `core/evaluator.py:40` under CPython | Production code | IMPLEMENTATION-DERIVED | A property of the executing runtime, not a protocol decision; not available in the other registered reference language. |
| **C-54** | Overflow treated as a rejection condition | `aura-specification/specification/SPEC-002…:304` (REQ-002-031 lists "numeric overflow" and "numeric out-of-domain value" among conditions the future specification MUST address) | v0.3-DRAFT; normative effect NONE | DRAFT-SPEC CANDIDATE | The source states an obligation to *decide*, not a decision; and its scope is the Constitution Artifact contract, not ARI. |

---

## DOMAIN 15 — SERIALIZATION / REPRESENTATION

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-55** | JSON canonicalization: `sort_keys=True`, `separators=(",", ":")`, UTF-8 | `audit/merkle.py:85` | Production code | IMPLEMENTATION-DERIVED | One of three coexisting canonicalizations feeding hashes; no source designates any. |
| **C-56** | JSON canonicalization: `sort_keys=True`, default separators | `core/merkle.py:8`; `compliance/certificate.py:69` | Production code | IMPLEMENTATION-DERIVED | Produces different bytes from C-55 for the same object. `APS-200:218` marks the canonical serialization format TODO. |
| **C-57** | External field: integer `RAW_ARI` | `init.sql:32-46` | Database DDL | SCHEMA/DDL-DERIVED | A persistence-side field name and type, unreferenced by any specification and unwritten by any application code. |
| **C-58** | External field: float `ari.score` in a certificate object `{score, drift, status}` | `compliance/certificate.py:41,53-57` | Production code | IMPLEMENTATION-DERIVED | A second external shape for the same measurement; the source itself scopes the float conversion to "presentation/reporting" (`:32-35`). |

---

## DOMAIN 16 — REFERENCE MODEL

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-59** | RI-PY as the reference exemplar for ARI | `aura-specification/aps/APS-950…:130-134`; `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md` | APS-950 v1.0-DRAFT · RI-PY v3.3, "APS-950 Certification Status: **NOT CERTIFIED**" (`:7`), RI-004/RI-005 "❌ MISSING" (`:25-26`) | REGISTRY-DERIVED | RD-1 premise 5 and boundary 21: a registry/reference entry, not a normative definition. APS-950's own certification conditions (`:120-124`) are not met. SPEC-002 `:37` requires an explicit governance grant that does not exist. |
| **C-60** | Engine A: `core/evaluator.py` + `compliance/evaluator_wrapper.py` | `aura-poc-a-core-v3.3/core/evaluator.py`, `compliance/evaluator_wrapper.py` | Production code | IMPLEMENTATION-DERIVED | Undesignated; differs from C-61 in validation, clamping and penalty model. |
| **C-61** | Engine B: `compliance/consistency.py` | `aura-poc-a-core-v3.3/compliance/consistency.py` | Production code | IMPLEMENTATION-DERIVED | Undesignated; differs from C-60 as above. Neither is designated correct anywhere. |
| **C-62** | A specification-only model with no designated reference implementation | `aura-specification/specification/SPEC-002…:291` (REQ-002-030: independent verification "MUST NOT require inspection of any Reference Implementation"), `:498-537` (§10) | v0.3-DRAFT; normative effect NONE | DRAFT-SPEC CANDIDATE | Expresses a verification posture the corpus requires for the Constitution Artifact; whether it applies to ARI is ARI-D-023/ARI-D-026, open. |

---

## DOMAIN 17 — CONFORMANCE CONTRACT

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-63** | CONF-001 repeatability as the ARI conformance criterion ("All output fields are bit-identical across multiple executions with the same input") | `aura-specification/aps/APS-400…:66-70`; `conformance/CONF-001_DETERMINISTIC_EVALUATION.md:46` | Both `Status: DRAFT`; CONF-001 `:34` "TODO: Specify exact preconditions"; `:73` fixture "TODO" | DRAFT-SPEC CANDIDATE | DRAFT, unexecutable as written (no fixture, no preconditions), and satisfied by any deterministic function irrespective of which division or rounding rule it uses. |
| **C-64** | CONF-006 cross-platform equality ("Same Evidence Pack produced on x86 and ARM platforms") | `aura-specification/aps/APS-400…:96-100` | DRAFT | DRAFT-SPEC CANDIDATE | DRAFT; compares an Evidence Pack whose canonical format is TODO (`APS-200:218`, APS-300 pack format referenced as pending by `APS-500:63`). |
| **C-65** | CONF-007 fail-closed ("Implementation enters safe state; no partial output generated") | `aura-specification/aps/APS-400…:102-106`; `conformance/CONF-007_FAIL_CLOSED.md:46` | DRAFT; preconditions TODO (`:34`); fixture FIX-ERROR TODO | DRAFT-SPEC CANDIDATE | DRAFT, and its trigger set depends on APS-001 §8, which is TODO. |

---

## DOMAIN 18 — REFERENCE FIXTURES

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-66** | APS-500 fixture structure (`fixture_id`, `fixture_version`, `protocol_version`, `input_data`, `expected_output`, `expected_evidence`, `related_invariants`, `related_conformance_tests`) as the container for ARI fixtures | `aura-specification/aps/APS-500_REFERENCE_FIXTURES.md:32-44` | v1.0-DRAFT; `:63` "TODO: Canonical fixture data requires APS-200 entity schemas and APS-300 Evidence Pack format to be finalized" | DRAFT-SPEC CANDIDATE | A container shape, not content. The only fixture file in the corpus (`fixtures/core/FIX-001_BASIC_EVALUATION.json`) has `"_status": "TODO"` and every payload field `"TODO"`. |
| **C-67** | The RD-006 observation-record shape (case id, input identity, evaluator identity, outputs, runtime identity, execution status) as a machine-readable record format | `aura-poc-a-core-v3.3/core/test_ari_observability.py:161-178` and the emitted artifact described in `review/2026-08-11_ENGINEERING_BASELINE/RD-006_ARI_OBSERVABILITY.md` §6.1 | Test module, self-declared characterization; artifact carries `"normative_effect": "NONE"` | CHARACTERIZATION-OBSERVATION | A record *shape* recorded as a candidate format only. The values it carries are excluded from candidacy — see §19 below. |

---

## DOMAIN 19 — CROSS-LANGUAGE EQUIVALENCE

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-68** | Equivalence as bit-identity of a canonical byte sequence | `aura-specification/specification/SPEC-002…:325-337` (§5.1 chain); `aura-poc-a-core-v3.3/docs/ADR_005_NO_FLOAT_RUNTIME.md:60,391` | SPEC-002 v0.3-DRAFT, normative effect NONE · ADR-005 APPROVED/FROZEN within the implementation corpus | DRAFT-SPEC CANDIDATE + DOCUMENTARY | SPEC-002's chain is scoped to the Constitution Artifact and is non-normative in DRAFT; ADR-005's statement is scoped to architectures (x86/ARM/WASM), not to independent language implementations, and there is no canonical byte sequence for ARI to compare (Domain 15 open). |
| **C-69** | Equivalence as equality of the integer ARI/drift outputs | `aura-specification/aps/APS-100…:62` (INV-002 "identical result on every conformant implementation") | APS-100 v1.0-DRAFT | DRAFT-SPEC CANDIDATE | INV-002 does not bind "identical" to a comparison object, and the computation whose result would be compared is undefined. |
| **C-70** | Equivalence as equality of evidence-pack hashes | `aura-specification/aps/APS-400…:96-100` (CONF-006 PASS criterion) | DRAFT | DRAFT-SPEC CANDIDATE | Depends on an Evidence Pack format that is TODO. |
| **C-71** | The SPEC-002 §5.1 determinism chain transferred wholesale to ARI | `aura-specification/specification/SPEC-002…:325-337`, `:498-537` | v0.3-DRAFT; normative effect NONE | DRAFT-SPEC CANDIDATE | The transfer itself is an undecided architectural act; SPEC-002 governs the Constitution Artifact contract and does not claim ARI scope. |

---

## DOMAIN 20 — AUDIT / REPRODUCIBILITY

| ID | Candidate | Exact source | Source status | Class | Why it cannot establish normative authority |
|---|---|---|---|---|---|
| **C-72** | APS-200 Common Object Contract as the header of an ARI record (`object_id`, `object_type`, `protocol_version`, `schema_version`, `created_at`, `integrity_hash`) | `aura-specification/aps/APS-200_CANONICAL_DATA_MODEL.md:49-58` | v1.0-DRAFT; `:224` JSON Schema "TODO" | DRAFT-SPEC CANDIDATE | Defines fields for entities that exist in the model; **no ARI entity is defined in APS-200**, so applying it to ARI is an undecided act. |
| **C-73** | RD-006 runtime-identity fields (`system`, `machine`, `architecture`, `python_version`, `python_implementation`) as provenance | `aura-poc-a-core-v3.3/core/test_ari_observability.py:147-158` | Test module, self-declared characterization | CHARACTERIZATION-OBSERVATION | A field set devised for observation, carrying `"normative_effect": "NONE"`; language-specific by construction. |
| **C-74** | Merkle/ETC certificate as the ARI audit artifact | `aura-poc-a-core-v3.3/core/merkle.py:5-12`; `compliance/certificate.py:48-70` | Production code | IMPLEMENTATION-DERIVED | Not derived from APS-300; `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:24` records the ETC as "not APS-300 canonical Evidence Pack". |

---

## 19. Characterization observations — explicitly NOT candidate values

The following are execution results, recorded here only so that a reviewer can see what has been
observed. **Per hard boundaries 22 and 23, they are not converted into expected normative values,
are not proposed as fixture expectations, and are not candidates for any decision.**

> Source: `aura-poc-a-core-v3.3/core/test_ari_observability.py:138-144`, table named
> `IMPLEMENTATION_DERIVED_NON_NORMATIVE`; module docstring `:5-16` — "CURRENT BEHAVIOUR ≠
> NORMATIVE REQUIREMENT … It does NOT record: 'This is what Aura requires.'" The emitted artifact
> carries `"normative_effect": "NONE"`, enforced by a test (`:273-277`).
> Runtime observed: Linux / x86_64 / CPython 3.11.15 (single architecture only).

| Case | Input (as recorded by the source) | Observed `ari` | Observed `drift` |
|---|---|---:|---:|
| OBS-1 | aligned unit, dim 4, valid schema | 100000 | 0 |
| OBS-2 | orthogonal, dim 4, valid schema | 30000 | 100000 |
| OBS-3 | aligned unit, dim 1536, valid schema | 100000 | 0 |
| OBS-4 | aligned unit, dim 4, invalid schema | 70000 | 0 |
| OBS-5 | anti-aligned, dim 4, valid schema | 29999 | 100001 |

Further measured observations recorded by
`review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §5.1–§5.4 (a prior
review record with no normative effect): maximum similarity returned for mismatched operand
lengths including 1536-vs-1; `ari` values of `310000` and `107550000` for non-unit inputs;
`drift = 200000` for anti-aligned input; divergent division results at negative dividends.

**Interpretation:** these observations demonstrate that the open questions have observable
consequences. They do not answer any of them, and nothing in this package treats them as
answers.

---

*This document has no normative effect. Every entry is a NON-NORMATIVE CANDIDATE. Nothing here is
selected, ranked, recommended, or converted into a requirement.*
