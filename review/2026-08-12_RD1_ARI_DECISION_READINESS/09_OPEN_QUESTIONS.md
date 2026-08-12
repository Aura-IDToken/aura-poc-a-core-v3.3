# 09 — OPEN QUESTIONS

**Package:** RD-1-ARI-DECISION-READINESS · **Normative effect:** NONE

Every question below is **open**. None is answered here, and no answer is implied by the order in
which options appear.

**Question format:** `Q` (decision-ready question) · `WHY` (why it must be answered) ·
`WHO` (jurisdiction, as named by the corpus — recorded, not assigned by this package) ·
`UNBLOCKS` · `ANSWER SPACE` (the alternatives evidence shows to exist; unranked; **not
exhaustive** — an authority may answer outside it).

---

# PART A — PRIOR QUESTIONS

These are not ARI semantic questions. They determine *whose answer counts* for the ARI questions,
and they are therefore listed first. Each was surfaced by evidence gathered for this package.

## OQ-A — Which authority ladder governs an ARI decision?

- **Q:** When the specification corpus's hierarchy (`aura-specification/constitution/AURA_CONSTITUTION.md` Article V: Constitution → APS-001 → APS-100 → ADR/ARR/RFC → Playbook → Repository Documentation → Implementation) and the implementation corpus's precedence list (`aura-poc-a-core-v3.3/CLAUDE.md`, tier 1 "Constitutional Decree / Constitutional Authority") order the same artifacts differently, which ordering governs a decision about ARI?
- **WHY:** The two ladders place the `CONSTITUTIONAL_DECREE.md` at opposite ends. Under Article V it is repository documentation, below APS-001 and APS-100. Under `CLAUDE.md` it is tier 1, above the Protocol Specification. Neither corpus cites the other. Without this answer, "who decides" and "what binds" are both indeterminate for every question below.
- **WHO:** Chief Architect (AURA-CON-001 Article VIII) and/or Protocol Custodian (`aura-poc-a-core-v3.3/ROLE_OF_THE_PROTOCOL_CUSTODIAN.md`). The corpus does not state which of the two owns a cross-corpus conflict.
- **UNBLOCKS:** OQ-B, ARI-D-001, ARI-D-007, ARI-D-014; and the scope statement required by `08_TWO_KEY_DECISION_PROTOCOL.md` rule 9.
- **ANSWER SPACE:** specification ladder governs · implementation ladder governs · each governs its own corpus with an explicit conflict rule · a new unifying artifact is created.

## OQ-B — Does `CONSTITUTIONAL_DECREE.md` Article I bind a protocol-level, cross-language ARI, or only this instrument?

- **Q:** Do the Decree's Article I constants — scaling factor `100,000`, sentinel drift threshold `0.68`, "Q16.16", "int32/int64" — bind any conformant ARI implementation, or do they bind only `aura-poc-a-core-v3.3`?
- **WHY:** The Decree states these are "CONSTITUTIONAL CONSTANTS that SHALL NOT be modified" (Article I §8) and declares itself "MANDATORY / NON-OVERRIDABLE". Simultaneously, `aura-specification/specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:108` lists `100000` as a **candidate only** and states that no candidate constitutes a recommendation, preference or default. `02_DECISION_DOMAIN_MATRIX.md` therefore marks Domains 4 and 10 **DISPUTED AUTHORITY — SCOPE UNRESOLVED** rather than NORMATIVE. That marking is provisional on this answer.
- **WHO:** as OQ-A.
- **UNBLOCKS:** ARI-D-007, ARI-D-008, ARI-D-014, ARI-D-021.
- **ANSWER SPACE:** binds the protocol · binds only the instrument · binds the instrument and is proposed to the protocol through the specification process.

## OQ-C — What is the relationship between the Decree's "Q16.16" and its "scaling factor 100,000"?

- **Q:** `CONSTITUTIONAL_DECREE.md` Article I §1 lists both "✔ Fixed-point arithmetic (Q16.16)" and "✔ Scaling factor: 100,000 (10^5)". Q16.16 is a binary fixed-point format with a 2^16 fractional scale; 100,000 is a decimal scale. Which applies, or in what relationship do they stand?
- **WHY:** No implementation uses Q16.16; four modules use the decimal scale. The document that declares both is the one the `CLAUDE.md` ladder places at tier 1. A decision on quantization (ARI-D-007) cannot cite this article without resolving which clause it is citing.
- **WHO:** Protocol Custodian (the Decree's own Article on authority states the Custodian "May modify constitutional constants").
- **UNBLOCKS:** ARI-D-007, ARI-D-008.
- **ANSWER SPACE:** decimal scale governs and Q16.16 is descriptive/erroneous · Q16.16 governs · both apply at different positions · the article requires amendment.

## OQ-D — Which repository is the authoritative specification corpus?

- **Q:** This session's attached specification repository (`aura-nomos/aura-specification` @ `eb2a4ec`) contains only a one-line `README.md` and `.github/CODEOWNERS`. All specification evidence in this package comes from `AuraIDToken/aura-specification` @ `62d2d6b`. Which is authoritative, and what is the relationship between them?
- **WHY:** A decision recorded in the wrong repository has no effect. Provenance for every specification citation in this package depends on this answer.
- **WHO:** Chief Architect / repository owner.
- **UNBLOCKS:** the recording location for every decision in this package.
- **ANSWER SPACE:** `AuraIDToken/aura-specification` is authoritative · `aura-nomos/aura-specification` is authoritative and unpopulated · a migration is in progress with a stated cutover.

---

# PART B — ARI SEMANTIC QUESTIONS

One entry per decision identifier. Full statements, provenance and evidence requirements are in
`01_ARI_DECISION_REGISTER.md` and `06_EVIDENCE_REQUIREMENTS.md`.

## Domain 1 — ARI Identity

**OQ-1 (ARI-D-001):** *Does the Aura Protocol define ARI normatively, or is it ruled to be
implementation-defined and therefore outside the conformance surface?*
**WHY:** The corpus's only ARI statement defines it by deferral to an implementation; APS-001 is
`TODO`. **WHO:** Chief Architect. **UNBLOCKS:** everything.
**ANSWER SPACE:** protocol-defined (in APS-001, or a new APS) · explicitly implementation-defined ·
deferred with a stated re-decision trigger.

**OQ-2 (ARI-D-002):** *Which quantity carries the name ARI — the pre-penalty measurement, the
post-penalty value, or both under distinct names?*
**WHY:** Three names currently denote two quantities, and one key (`ari`) carries both at
different layers. **UNBLOCKS:** ARI-D-014, ARI-D-015, ARI-D-022.
**ANSWER SPACE:** pre-penalty · post-penalty · both, separately named.

**OQ-3 (ARI-D-003):** *What is the authoritative expansion of "ARI", given that the specification
glossary and the implementation documentation expand it differently?*
**ANSWER SPACE:** "Aura Reliability Index" · "Agent Reliability Index" · a new term with a
migration path.

## Domain 2 — Input Contract

**OQ-4 (ARI-D-004):** *What is the complete, normative input contract for an ARI computation —
which fields, of which types and domains, and which of them participate in the computation as
opposed to identity/audit?*
**WHY:** APS-001 §3 is `TODO`; two incompatible input shapes exist in the implementation.
**UNBLOCKS:** ARI-D-005, ARI-D-006, ARI-D-013, ARI-D-017.

**OQ-5 (ARI-D-005):** *Is structural validity an input asserted by the caller, or a property the
ARI engine computes — and if computed, against which schema and version?*

## Domain 3 — Vector Dimension

**OQ-6 (ARI-D-006):** *Is vector dimension a normative element of the input contract; must the
agent vector and the constitution vector have equal length; and where is that checked?*
**WHY:** The dimension constant exists only in the offline normalizer and is referenced by neither
engine; the specification corpus states no dimension. **Explicitly not settled by:** the
1536-dimensional material, nor the observed success of a 1-element vector — neither is treated as
proof.
**ANSWER SPACE:** a fixed dimension is required · lengths must merely be equal · dimension is
unconstrained at the ARI boundary and the mismatch outcome is specified.

## Domain 4 — Quantization

**OQ-7 (ARI-D-007):** *What fixed-point scheme and scale does normative ARI use, and what does a
scaled integer denote?* **Depends on:** OQ-A, OQ-B, OQ-C, and on U-2 in
`05_DEPENDENCY_GRAPH.md` §4 (whether ARI operands fall inside SPEC-002 AD-CA-007's scope).

## Domain 5 — Integer Representation

**OQ-8 (ARI-D-008):** *What integer width and signedness apply at each arithmetic position, and is
arbitrary precision conformant?*

## Domain 6 — Arithmetic Semantics

**OQ-9 (ARI-D-009):** *What is the normative ordered operation sequence, where exactly is each
rescaling applied, and is reassociation permitted?*

## Domain 7 — Division Semantics

**OQ-10 (ARI-D-010):** *What integer division semantics does normative ARI require for negative
dividends, at each division site?*
**WHY:** `docs/ADR_005_NO_FLOAT_RUNTIME.md:134` states `//` is "truncation toward zero"; the
operator in use floors. The two do not agree for negative dividends, and SPEC-002's numeric
decision domain lists no division candidate at all. **This package does not resolve the conflict
and changes nothing.**
**ANSWER SPACE:** floor · truncate toward zero · negative dividends excluded by contract, making
the rule unreachable.

## Domain 8 — Rounding Semantics

**OQ-11 (ARI-D-011):** *What rounding semantics does normative ARI require at float→integer
reduction, including tie behaviour and sign symmetry — and is that reduction inside ARI's
conformance surface at all?*
**WHY:** The implementation's `round()` behaviour is not a normative choice; `round-half-to-even`
is listed by SPEC-002 as candidate-only and explicitly not a default.

**OQ-12 (ARI-D-012):** *Are derived/presented ARI representations inside the conformance surface,
and if so what rounding governs each?*
**WHY:** Two different reductions currently exist (a stated half-up rule at persistence; an
unspecified float division at the certificate).

## Domain 9 — Similarity Function

**OQ-13 (ARI-D-013):** *Which mathematical properties must the ARI similarity function satisfy —
domain, codomain/range, normalization precondition, symmetry, identity, boundedness, ordering,
zero-vector behaviour, quantization tolerance, determinism?*
**WHY:** The current sources use "≈" and "approximately" and make the cosine-equivalence claim
conditional on a precondition no code verifies. **Note:** the question asks for the property set,
not for a function.

## Domain 10 — Drift

**OQ-14 (ARI-D-014):** *Is drift a normative protocol output; what is its definition, range and
clamping; and how is it distinguished from the drift threshold constant that shares its name?*
**WHY:** Drift is emitted and enters the audit path; code and docstring disagree on its clamp; the
threshold constant is compared against a different quantity.

## Domain 11 — Penalty Model

**OQ-15 (ARI-D-015):** *Is penalty application inside the normative ARI object; if so which
penalty model; and if not, what keeps a penalized value distinguishable from a measurement in
evidence?*
**WHY:** Two incompatible models coexist, in different units with different triggers.

## Domain 12 — Output Bounds

**OQ-16 (ARI-D-016):** *Are ARI output bounds normative, and if so what are they, by what
mechanism are they enforced, and at which point — and separately, the same for drift?*
**WHY:** The documented range and the observed out-of-range values are **not sufficient** to
select a resolution: they are equally consistent with "bounds are normative and unenforced" and
with "the input precondition is normative and those inputs are inadmissible".

## Domain 13 — Error / Malformed Input

**OQ-17 (ARI-D-017):** *Which conditions make an ARI input invalid?* — decided condition by
condition: dimension mismatch · dimension ≠ required · empty vector · zero vector · magnitude over
scale · non-integer element · missing field · absent constitution vector · unnormalized operand.

**OQ-18 (ARI-D-018):** *For each invalid condition, is detection obligatory, and at which
boundary?*

**OQ-19 (ARI-D-019):** *What is the required response to each invalid condition, expressed as a
behaviour?* **Explicitly open:** whether any numeric ARI value may be emitted at all on invalid
input. Fail-closed is **not** assumed to imply any particular number.

**OQ-20 (ARI-D-020):** *Does a failed ARI computation produce an evidence record; if so with what
schema; and how does a consumer distinguish "not computed" from "computed as zero"?*

## Domain 14 — Overflow / Range

**OQ-21 (ARI-D-021):** *What is the representable range at each arithmetic position, what
constitutes overflow, what is the required behaviour on overflow, and is overflow a fail-closed
trigger?*
**WHY:** SPEC-002 REQ-002-014 requires overflow behaviour to be part of a numeric representation
and REQ-002-031 lists numeric overflow among conditions that must be addressed; neither is decided.

## Domain 15 — Serialization

**OQ-22 (ARI-D-022):** *What is the canonical representation and canonical byte sequence of an ARI
result, and which fields are inside the hash domain?*
**WHY:** Three JSON canonicalizations currently feed hashes in one repository, and two different
external field shapes exist; INV-003 (Canonical Serialization, Critical) has no format.

## Domain 16 — Reference Model

**OQ-23 (ARI-D-023):** *Is there a normative reference model for ARI; if so which artifact, at
which version, granted by which governance act — and which of the two coexisting engines is being
spoken about?*
**WHY:** SPEC-002 `:37` requires an explicit grant for implementation behaviour to be normative,
and none exists; RI-PY is recorded NOT CERTIFIED. **Hard boundary 21 applies: RI-PY is not treated
as authority anywhere in this package.**

## Domain 17 — Conformance Contract

**OQ-24 (ARI-D-024):** *Which conformance tests bind ARI, and what are their PASS criteria
expressed in ARI terms?*
**WHY:** All ten CONF tests are DRAFT; the determinism test as written is satisfied by any
deterministic implementation under any division or rounding rule.

## Domain 18 — Reference Fixtures

**OQ-25 (ARI-D-025):** *Is ARI conformance fixture-based; what is the fixture format; and what
governance act grants a fixture normative status?*
**Constraint recorded:** a fixture value is not authority unless a governing decision grants it,
and no characterization observation may be used as a fixture expectation.

## Domain 19 — Cross-Language Equivalence

**OQ-26 (ARI-D-026):** *What must "bit-equivalent" or "semantically equivalent" mean before
independent Python / Rust / JS implementations can be judged conformant — comparison object,
equivalence relation, input set, failure agreement, pinned constructs, observation surface,
platform set?*

## Domain 20 — Audit / Reproducibility

**OQ-27 (ARI-D-027):** *What must be recorded for a third party to reproduce an ARI value without
inspecting an implementation?*

---

# PART C — CONTRADICTIONS REQUIRING RESOLUTION

Recorded, not resolved. Each is a factual divergence between two sources or between a source and
itself. **None is treated here as a defect to be fixed.**

| # | Contradiction | Source A | Source B | Bears on |
|---|---|---|---|---|
| **X-A1** | Acronym expansion | `aura-specification/glossary/GLOSSARY.md:27` ("Aura Reliability Index") | `aura-poc-a-core-v3.3/docs/mathematical_foundation.md:186` ("Required Term: 'Agent Reliability Index'") | OQ-3 |
| **X-A2** | ARI formula | `docs/mathematical_foundation.md:8` (`0.3·SI + 0.7·SA`) | `.github/github/copilot-instructions.md:17` (`SI·(0.5·SA + 0.5·F)`, with `F` undefined) | OQ-1 |
| **X-A3** | Fixed-point scheme | `CONSTITUTIONAL_DECREE.md` Art. I §1 ("Q16.16") | same article, same section ("Scaling factor: 100,000") | OQ-C, OQ-7 |
| **X-A4** | Authority of `100000` | `CONSTITUTIONAL_DECREE.md` Art. I §8 ("FROZEN … SHALL NOT be modified") | `SPEC-002:108` ("candidate only … not a recommendation, preference, default") | OQ-B, OQ-7 |
| **X-A5** | Division semantics | `docs/ADR_005_NO_FLOAT_RUNTIME.md:134` ("truncation toward zero") | the floor behaviour of the operator at `core/evaluator.py:46` and five further sites | OQ-10 |
| **X-A6** | Drift clamp | `core/evaluator.py:85` inline comment (`[0, 100000]`) | `core/evaluator.py:86` code (`min(…, 2 × SCALING_FACTOR)`) | OQ-14 |
| **X-A7** | ARI clamp | `docs/mathematical_foundation.md:59` ("RAW_ARI clamped to [0, 100000] at Layer 0") | `core/evaluator.py:79` (`max(0, …)` — lower clamp only) | OQ-16 |
| **X-A8** | Canonical serialization | `audit/merkle.py:85` (compact separators) | `core/merkle.py:8` and `compliance/certificate.py:69` (default separators) | OQ-22 |
| **X-A9** | Validation posture | `core/evaluator.py` (no validation) | `compliance/consistency.py:84-91` (magnitude and zero-vector validation) | OQ-17, OQ-18, OQ-23 |
| **X-A10** | Penalty model | `compliance/policy.py:19-20` (`150000` threshold) | `compliance/consistency.py:21` (`10000 × count`) | OQ-15 |
| **X-A11** | Layer ownership of the semantic term | `docs/mathematical_foundation.md:29` ("never computed inside Layer 0") | `compliance/evaluator_wrapper.py:61` (Layer 2 calls the Layer 0 similarity function) | OQ-2, OQ-15 |
| **X-A12** | Reference-implementation status | `aura-specification/aps/APS-950…:132` (RI-PY "Status: Active") | `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md:7` ("NOT CERTIFIED"), `:25-26` (RI-004/RI-005 MISSING) | OQ-23 |

**Handling.** Per `aura-poc-a-core-v3.3/CLAUDE.md` and `docs/conformance/README.md`, a detected
conflict must not be silently reconciled. Each of X-A1 … X-A12 is reported above and referred to
human / Protocol Custodian resolution. None makes the construction of this decision package
impossible, so RD-1 was **not** reopened (`00_SCOPE_AND_GOVERNING_CONTEXT.md` §3).

---

# PART D — QUESTIONS THIS PACKAGE DELIBERATELY DID NOT ASK

Recorded so that their absence is visible and intentional:

1. *"Which candidate should be chosen?"* — outside the gate (`08_TWO_KEY_DECISION_PROTOCOL.md` §1).
2. *"Is the current implementation correct?"* — unanswerable while no normative definition exists,
   and the framing carried from RD-1 forbids treating the open questions as accepted defects.
3. *"Should `zip`, `round`, `//`, the bounds, or the malformed-input handling be fixed?"* — hard
   boundaries 24–28. Whether any of them is a defect is downstream of the decisions above.
4. *"May the instrument be changed?"* — recorded as INDETERMINATE by a prior governance audit and
   **not reopened** by this package.

---

*This document has no normative effect. Every question in it is open. It selects no ARI semantics,
creates no ADR, amends no specification, and modifies no code.*
