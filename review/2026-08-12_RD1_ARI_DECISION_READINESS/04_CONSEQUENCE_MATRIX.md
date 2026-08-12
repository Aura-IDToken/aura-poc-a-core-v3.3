# 04 — CONSEQUENCE MATRIX

**Package:** RD-1-ARI-DECISION-READINESS · **Normative effect:** NONE

---

## 0. Reading rules

This document states **consequences only**.

- No alternative is ranked, scored, preferred, recommended, or marked correct.
- Order within a table is the order of the candidate identifiers in
  `03_NON_NORMATIVE_CANDIDATES.md` and carries no significance.
- A longer consequence list does not indicate a heavier or lighter option; it indicates only
  that more evidence exists about that alternative.
- Consequences are stated conditionally ("if X were decided, then …"). No conditional in this
  document asserts that X will be, or ought to be, decided.
- Where a consequence concerns existing code, it describes what the decision would *imply about*
  the code. **No change is proposed, scheduled, or made** (hard boundaries 16–17, 24–28).

**Consequence axes used:** `SPEC` (what a specification would have to carry) · `IMPL` (what the
existing implementation would then be, descriptively) · `XLANG` (effect on independent
Python/Rust/JS implementations) · `CONF` (effect on conformance tests and fixtures) · `EVID`
(effect on evidence/audit records) · `GOV` (effect on governance artifacts and instrument
identity) · `DOWN` (effect on other decisions in this package).

> **GOV axis, standing note.** Every alternative that would change any observable output of the
> current instrument interacts with the unresolved governance question recorded in
> `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md` (verdict:
> **INDETERMINATE**; engineering code changes **BLOCKED pending governance clarification**), and
> with `aura-poc-a-core-v3.3/README.md` §11.4 ("Bug fixes or modifications require a new
> lineage") and `CONSTITUTIONAL_DECREE.md` Article VIII ("Any change to core logic creates a
> NEW INSTRUMENT, not a new version"). This package neither reopens NB-021 nor assumes an
> outcome. The GOV rows below therefore record *that the interaction exists*, not how it
> resolves.

---

## DOMAIN 1 — ARI IDENTITY (ARI-D-001 … ARI-D-003)

| Alternative | Consequences |
|---|---|
| **ARI is normatively defined by Aura** (protocol-level object) | **SPEC**: a normative section must be authored and carried by a document with a lifecycle status — APS-001 §3/§4 (currently `Status: TODO`) or a new APS; every decision ARI-D-004…ARI-D-027 becomes *required*, not optional. **CONF**: ARI enters the conformance surface; CONF-001/006/007 acquire ARI-expressed PASS criteria; INV-010 ("every Invariant MUST have a Conformance Test") applies to whatever invariants the ARI section introduces. **XLANG**: independent implementations become judgeable; the constructs in ARI-D-026.A.5 must all be pinned. **GOV**: creates a specification-corpus artifact whose relationship to the implementation corpus's FROZEN instrument must be stated. **DOWN**: unblocks the entire graph in `05_DEPENDENCY_GRAPH.md`. |
| **ARI remains implementation-defined** (explicit ruling) | **SPEC**: the glossary deferral at `GLOSSARY.md:27-28` becomes the settled position; ARI acquires no APS section. **CONF**: what CONF-001 and CONF-006 verify for ARI must be restated, since both are written against protocol behaviour; INV-001/INV-002/INV-006 (all Critical) would apply to a quantity the protocol does not define — that relationship must be stated explicitly rather than left implicit. **XLANG**: a second-language implementation cannot be judged conformant *on ARI*; the cross-language question becomes moot or is redefined as implementation-compatibility rather than conformance. **EVID**: evidence consuming ARI must record which implementation produced it, since the value's meaning is implementation-bound. **DOWN**: ARI-D-004…ARI-D-027 collapse from protocol decisions into implementation-documentation tasks, and ARI-D-023/024/025/026 change character entirely. |
| **ARI is the Layer 0 quantity** (ARI-D-002) | **SPEC**: the penalty composition (`ARI = max(0, RAW_ARI − P)`) sits outside the ARI definition and needs its own named object. **IMPL**: the Layer 2 return key `ari` in `compliance/evaluator_wrapper.py:73` would denote a non-ARI quantity under the same name. **EVID**: certificates emitting `ari` (`compliance/certificate.py:53-57`) would need to state which quantity they carry. **DOWN**: constrains ARI-D-015 (penalty outside) and ARI-D-016 (bounds apply pre-penalty). |
| **ARI is the Layer 2 quantity** | **SPEC**: the penalty model becomes part of the ARI definition, making ARI-D-015 mandatory and coupling ARI to policy versioning. **IMPL**: the Layer 0 output becomes an intermediate, not a protocol output. **EVID**: a penalized value is the reported measurement; evidence must record the policy identity that produced it (APS-200 ENT-004 Policy Reference). **DOWN**: makes ARI-D-015 blocking for ARI-D-016 and ARI-D-024. |
| **Both are normative, separately named** | **SPEC**: two objects, two definitions, two ranges, two conformance criteria. **EVID**: both must appear in evidence with distinct field names — which the current single `ari` key cannot express. **DOWN**: doubles the surface of ARI-D-016, ARI-D-022 and ARI-D-025. |
| **Acronym expansion "Aura" / "Agent"** (ARI-D-003) | **SPEC/GOV**: whichever is chosen, the other corpus's text becomes inconsistent and requires an amendment path; `docs/mathematical_foundation.md:186` states its expansion with the word "Required", and that document is self-declared FROZEN, so changing it engages the NB-021 interaction. **EVID**: any expansion appearing in certificates or reports becomes part of the regulatory-facing vocabulary referenced at `docs/mathematical_foundation.md:190`. |

---

## DOMAIN 2 — INPUT CONTRACT (ARI-D-004, ARI-D-005)

| Alternative | Consequences |
|---|---|
| **C-06 shape** `(agent_id, vector, valid_schema)` | **SPEC**: requires a definition of `valid_schema`'s provenance and of `agent_id`'s role (audit-only vs computational). **IMPL**: matches one existing engine; the other engine's dict input becomes a non-conformant interface. **CONF**: fixtures carry a boolean whose truth is asserted, not derived — a fixture cannot verify it. **DOWN**: forces ARI-D-005 toward caller-assertion and creates an evidence obligation (who asserted validity, and on what basis). |
| **C-07 shape** event dict `{timestamp, embedding, content}` | **SPEC**: requires a canonical event schema, i.e. it depends on `APS-200:92` (currently TODO). **IMPL**: matches the other existing engine. **CONF**: fixtures can be self-contained, since validity is derivable from the payload. **EVID**: `timestamp` inside the computation surface interacts with determinism (a clock-derived field in a hashed input). **DOWN**: forces ARI-D-005 toward engine determination and couples ARI to APS-200 progress. |
| **Structural validity is caller-asserted** (C-08) | **CONF**: CONF-007's malformed-input procedure cannot reach the structural term through the ARI interface. **EVID**: the assertion must itself be evidenced for the measurement to be auditable. **XLANG**: trivially portable — the term is an input, not a computation. |
| **Structural validity is engine-computed** (C-09) | **SPEC**: requires naming the schema and version against which it is computed. **XLANG**: every implementation must implement identical validation, adding a second equivalence surface (validation outcome, not just numeric output). **CONF**: enables fixture-verifiable structural behaviour. |

---

## DOMAIN 3 — VECTOR DIMENSION (ARI-D-006)

| Alternative | Consequences |
|---|---|
| **A fixed dimension is normative** (C-10 is one instance of this class) | **SPEC**: the fixing artifact must be named and versioned, and its relation to the embedding method (SPEC-002 AD-CA-005, UNRESOLVED) stated, since dimension is a property of the embedding. **IMPL**: the constant currently lives only in `core/offline_normalizer.py:44` and is unreferenced by either engine — the decision would make that placement a stated gap rather than an incidental one. **CONF**: fixtures must carry vectors at the fixed dimension; a 1536-element fixture has a size cost for every fixture file. **XLANG**: overflow analysis (ARI-D-021) becomes computable, since worst-case accumulator magnitude is a function of dimension × scale². **DOWN**: makes ARI-D-021 answerable and gives ARI-D-017 a concrete invalid condition. |
| **Dimension is not fixed; operands must merely agree** (C-12) | **SPEC**: the ARI definition becomes dimension-generic; bounds (ARI-D-016) and overflow (ARI-D-021) must then be expressed as functions of dimension rather than constants. **CONF**: fixtures can be small, but must cover multiple dimensions to be meaningful. **XLANG**: implementations must agree on the mismatch response, not just the match case. |
| **Dimension is unconstrained at the ARI boundary** (C-11) | **SPEC**: requires an explicit statement that operand-length divergence is admissible and a definition of the resulting value, since the outcome is otherwise determined by a language construct (`zip` semantics) rather than by specification. **XLANG**: the truncation behaviour of the host language's zip/iterator equivalent becomes semantically load-bearing and must be pinned per language. **CONF**: mismatch cases become expected-behaviour fixtures rather than error fixtures. **EVID**: an evidence consumer cannot infer operand dimensions from the record unless they are recorded (ARI-D-027). |

---

## DOMAIN 4 — QUANTIZATION (ARI-D-007)

| Alternative | Consequences |
|---|---|
| **Decimal scale 10^5** (C-13) | **IMPL**: the four modules already using `100000` would be describable as consistent with the decision. **SPEC**: requires stating what the scaled integer denotes (a ratio in [0,1]? a similarity in [−1,1]?), which Domain 12 depends on. **XLANG**: decimal rescaling requires an integer division at every rescale point, making ARI-D-010 (division on negatives) unavoidable. **GOV**: engages the scope question OQ-A/OQ-B, because the value is asserted by the Decree and simultaneously listed as candidate-only by SPEC-002. |
| **Binary fixed-point Q16.16** (C-14) | **IMPL**: no current module implements it; the decision would make the Decree's own Article I self-consistent only if the decimal-scale clause were also addressed. **XLANG**: rescaling becomes a shift, removing the negative-dividend division question at rescale points (though not necessarily elsewhere) and changing the representable range. **CONF**: every existing observation and every documented constant (`68000`, `30000`, `70000`, `100000`) would be expressed in a different unit. **DOWN**: materially changes ARI-D-008, ARI-D-010, ARI-D-016 and ARI-D-021. |
| **Some other scale** (open) | **SPEC/CONF/EVID**: as above, plus a restatement of every constant and every documented range. **GOV**: interacts with `CONSTITUTIONAL_DECREE.md` Article I §8's "SHALL NOT be modified" language for the scaling factor. |
| **Scaling is decided under AD-CA-007 (Constitution Vector) and ARI inherits it** | **SPEC**: creates an explicit dependency of the ARI specification on SPEC-002's advancement beyond DRAFT, which SPEC-002 §11 records as NOT READY with all twelve AD-CA domains UNRESOLVED. **DOWN**: sequences ARI behind SPEC-002. |
| **ARI's numeric representation is decided independently of AD-CA-007** | **SPEC**: two numeric contracts exist in the project (vector values, ARI values) and their consistency must be stated. **XLANG**: two conversion points to specify wherever the two meet. |

---

## DOMAIN 5 — INTEGER REPRESENTATION (ARI-D-008)

| Alternative | Consequences |
|---|---|
| **Fixed widths (e.g. C-16: int32 operands, int64 accumulator)** | **XLANG**: makes Rust/JS ports expressible; JS in particular requires an explicit strategy, since its number type does not natively provide 64-bit integers. **IMPL**: the current arbitrary-precision execution would be describable as exceeding, not violating, the width — but only if overflow behaviour (ARI-D-021) says so. **CONF**: boundary fixtures at the width limits become required. **DOWN**: ARI-D-021 becomes mandatory; ARI-D-016 bounds must be checked against representable range. |
| **Arbitrary precision** (C-17) | **XLANG**: requires every target language to provide or emulate big integers, or to prove that admissible inputs cannot exceed a native width. **SPEC**: overflow ceases to be a failure mode and becomes a non-condition, which must be stated rather than assumed. **CONF**: removes a class of boundary fixtures and adds a proof obligation instead. |
| **Different widths at different positions** | **SPEC**: requires a per-position table, which is what REQ-002-014's "domain, width, sign" pattern anticipates. **XLANG**: conversion points between positions become normative and must be specified (truncate? check? saturate?). |

---

## DOMAIN 6 — ARITHMETIC SEMANTICS (ARI-D-009)

| Alternative | Consequences |
|---|---|
| **Rescale per weighted term** (C-18) | **IMPL**: describes the current expression shape in both engines. **XLANG**: two divisions per evaluation, each subject to ARI-D-010. **CONF**: intermediate values become part of what a fixture may pin, if intermediates are exposed. |
| **Rescale after summation** (C-19) | **XLANG**: one division per evaluation, reducing the number of sites at which the division rule applies. **IMPL**: would describe an expression shape no current module implements. **CONF**: produces different values from C-18 for inputs where the per-term remainders do not cancel — so the choice is fixture-visible. |
| **Reassociation permitted** | **XLANG**: permits vectorized/parallel accumulation, and simultaneously admits accumulation-order variation, which interacts directly with INV-001/INV-002/INV-006 (all Critical). **CONF**: cross-platform tests must then bound, rather than assert, equality. |
| **Reassociation prohibited** | **XLANG**: fixes accumulation order as normative, constraining permissible optimizations in every implementation. **SPEC**: the order itself must be written down (index order? sorted? as-given?). |

---

## DOMAIN 7 — DIVISION SEMANTICS (ARI-D-010)

| Alternative | Consequences |
|---|---|
| **Floor** (C-20) | **XLANG**: Rust/C/JS integer division truncates toward zero, so every port must implement a floor correction; the correction becomes a conformance-relevant construct. **IMPL**: describes current Python behaviour. **CONF**: requires at least one fixture with a negative dividend that is not an exact multiple of the scale, otherwise the rule is untested. **DOWN**: interacts with ARI-D-016 (a floored negative can push a term below zero before clamping). |
| **Truncate toward zero** (C-21) | **XLANG**: matches the default in Rust/C/JS; Python ports must implement a correction instead. **IMPL**: would describe current Python behaviour as divergent from the rule at negative dividends. **GOV**: engages the NB-021 interaction, since aligning behaviour would change outputs for that input class. **SPEC**: makes `docs/ADR_005_NO_FLOAT_RUNTIME.md:134` a correct description rather than an inaccurate one. |
| **Negative dividends excluded by contract** (C-22) | **SPEC**: shifts the burden to ARI-D-013 (similarity codomain) and ARI-D-017 (invalid input); the division rule becomes unreachable and must be documented as such rather than left unstated. **CONF**: requires evidence that no admissible input can produce a negative dividend — a proof obligation, not a test. **DOWN**: makes ARI-D-013's codomain decision blocking for ARI-D-010. |

---

## DOMAIN 8 — ROUNDING SEMANTICS (ARI-D-011, ARI-D-012)

| Alternative | Consequences |
|---|---|
| **Half-to-even** (C-23) | **XLANG**: matches Python's default and IEEE-754's default rounding attribute; Rust's `f64::round` and JS's `Math.round` differ, so ports need explicit implementations. **CONF**: requires `.5` fixtures in both signs to be tested at all. **EVID**: the constitution vector's bytes — and therefore any hash over them — depend on this choice. |
| **Half-away-from-zero** (C-24) | **XLANG**: matches Rust/C defaults; Python and JS need explicit implementations (JS rounds half toward +∞, which differs for negatives). **IMPL**: would describe the current offline normalizer as divergent at ties. |
| **Half-toward-+∞** (C-25) | **XLANG**: matches JS; Python and Rust need explicit implementations. **IMPL**: asymmetric for negative ties, which must be stated deliberately. |
| **Quantization is outside the ARI boundary** (a precondition supplied to ARI) | **SPEC**: the rounding rule belongs to the Constitution Vector construction contract (SPEC-002 AD-CA-007) rather than to ARI; ARI's specification then depends on SPEC-002 advancing. **CONF**: ARI fixtures take pre-quantized integer inputs and never exercise rounding. **DOWN**: removes ARI-D-011 from ARI's critical path and adds a dependency on SPEC-002. |
| **Derived representations are inside the conformance surface** (ARI-D-012) | **SPEC**: requires one rule per derived form; the DB half-up rule (C-26) and the certificate float division (C-27) would both need to be stated and reconciled. **EVID**: the presented value becomes part of what conformance checks. |
| **Derived representations are outside** | **EVID**: requires an explicit statement that presented values are non-normative, so consumers do not treat a rounded decimal as the measurement. **IMPL**: describes the position that `compliance/certificate.py:32-35` already asserts in prose. |

---

## DOMAIN 9 — SIMILARITY FUNCTION (ARI-D-013)

| Alternative | Consequences |
|---|---|
| **Unit-norm precondition is *assumed*** (C-28) | **SPEC**: bounds (ARI-D-016) become conditional statements — true only for admissible inputs — and out-of-range outputs become evidence of contract violation rather than of a bounding defect. **CONF**: fixtures cannot exercise the violation case, because its behaviour is undefined by construction. **EVID**: the audit record cannot demonstrate that the precondition held unless it is recorded (ARI-D-027). |
| **Unit-norm precondition is *enforced*** (C-29) | **SPEC**: requires a normalization tolerance in integer terms, since exact unit norm is generally unrepresentable after quantization. **XLANG**: every implementation must implement the same magnitude test, including the same tolerance arithmetic — a second equivalence surface. **IMPL**: describes one existing engine's posture and not the other's. **DOWN**: gives ARI-D-016 a derivable bound and gives ARI-D-017 a concrete invalid condition. |
| **Legacy cosine with `(cos+1)/2` mapping** (C-30) | **SPEC**: reintroduces a real-valued operation, engaging `CONSTITUTIONAL_DECREE.md` Article I §1 (no float at runtime) and INV-007. **XLANG**: reintroduces IEEE-754 divergence, which `docs/ADR_005_NO_FLOAT_RUNTIME.md` records as the reason the model was removed. **CONF**: changes the output range to [0,1] by construction, altering Domain 12 entirely. |
| **Exact identity required** (`s(a,a) == scale`) | **SPEC**: requires the quantization contract to guarantee it, which for quantized unit vectors is generally not attainable — so this alternative's feasibility depends on ARI-D-007/ARI-D-011. **CONF**: makes an exact-value fixture possible. |
| **Bounded deviation permitted** | **SPEC**: requires the bound to be stated numerically. **CONF**: fixtures become tolerance-based, which interacts with INV-002's "bit-perfect" language and CONF-001's "bit-identical" PASS criterion. |

---

## DOMAIN 10 — DRIFT (ARI-D-014)

| Alternative | Consequences |
|---|---|
| **Drift is a normative protocol output** | **SPEC**: needs its own definition, range, units and clamping, independent of ARI. **CONF**: needs its own PASS criteria and fixtures; CONF-001's "all output fields" would then cover it. **EVID**: becomes a required evidence field with a defined meaning. **DOWN**: adds a full parallel decision set (bounds, serialization, equivalence) for a second quantity. |
| **Drift is implementation-internal** | **EVID**: the certificate field at `compliance/certificate.py:54-56` would be carrying a non-protocol value into the audit path, which must be stated. **CONF**: excluded from conformance, so cross-implementation drift divergence would not be a conformance failure. |
| **Drift clamped `[0, scale]`** (C-32) vs **`[0, 2×scale]`** (C-31) | **IMPL**: the two alternatives correspond respectively to the current docstring and the current code, which disagree. **EVID**: under `[0, 2×scale]`, the presented decimal exceeds 1.0 for anti-aligned inputs, on a field documented as a ratio; under `[0, scale]`, information about the degree of anti-alignment is not representable. **XLANG**: either way the clamp must be specified, since it is not derivable from the similarity codomain alone. |
| **Threshold `68000` is part of the ARI/drift definition** (C-33) | **SPEC**: couples a policy constant to the measurement definition. **GOV**: engages `CONSTITUTIONAL_DECREE.md` Article I §8's "SHALL NOT be modified" clause and the OQ-A scope question. **IMPL**: the constant is currently compared against SA, not against drift — so this alternative requires stating which operand it applies to. |

---

## DOMAIN 11 — PENALTY MODEL (ARI-D-015)

| Alternative | Consequences |
|---|---|
| **Penalty inside the normative ARI object** | **SPEC**: ARI becomes policy-dependent; every ARI value must be interpreted relative to a policy identity (APS-200 ENT-004). **CONF**: fixtures must pin a policy version alongside the input. **XLANG**: implementations must share the penalty function exactly. **EVID**: policy reference becomes mandatory in the ARI record. |
| **Penalty outside** | **SPEC**: requires a second named object for the penalized value and a rule for how evidence distinguishes them. **IMPL**: the shared `ari` key across both layers becomes an ambiguity that evidence consumers must resolve. **CONF**: ARI conformance becomes independent of policy versioning. |
| **Threshold model** (C-34) | **SPEC**: a step function; a single unit change near the threshold produces a large output change, which must be an accepted property. **IMPL**: with `DRIFT_PENALTY = 150000` exceeding the documented ARI maximum, any triggered penalty floors the result — a property that must be stated deliberately if adopted. **CONF**: requires fixtures immediately either side of the threshold. |
| **Count model** (C-35) | **SPEC**: requires a normative definition of "violation" and of the rule set producing the count, i.e. a policy specification that does not currently exist. **CONF**: fixtures must carry rule sets. **XLANG**: rule evaluation becomes part of the equivalence surface. |
| **`max(0, RAW_ARI − P)` composition** (C-36) | **SPEC**: fixes the lower clamp's position relative to the penalty. **DOWN**: interacts with ARI-D-016: whether the clamp applies before, after, or at both stages is itself a decision. |

---

## DOMAIN 12 — OUTPUT BOUNDS (ARI-D-016)

| Alternative | Consequences |
|---|---|
| **Bounds normative, enforced by clamping** (C-37) | **SPEC**: clamping is lossy — out-of-contract inputs become indistinguishable from in-contract maxima, which must be an accepted property. **IMPL**: would describe the primary engine's single-sided clamp as incomplete relative to the rule. **EVID**: a clamped value cannot be distinguished from a computed one unless recorded. **CONF**: boundary fixtures at both bounds required. |
| **Bounds normative, enforced by rejection** | **SPEC**: an out-of-range result becomes an error, connecting Domain 12 to ARI-D-017/019. **EVID**: failure records become required for a case that currently produces a value. **XLANG**: implementations must agree on rejection, not merely on a number. |
| **Bounds as a derived consequence of the input precondition** (C-40) | **SPEC**: no output rule is needed; the guarantee comes from ARI-D-013's precondition, and a proof obligation replaces an enforcement mechanism. **CONF**: out-of-range inputs are inadmissible, so the observed `310000` / `107550000` class becomes a contract-violation case rather than a bounding case. **DOWN**: makes ARI-D-013 blocking for ARI-D-016. |
| **Bounds only at persistence** (C-39) | **EVID**: the measurement layer may emit values the storage layer rejects, so an evidence record may be unstorable — a condition that must be defined. **CONF**: conformance would not cover the bound at the point of computation. |
| **No normative bounds** | **SPEC**: the ARI range becomes a function of dimension, scale and input magnitude, which must then be documented for consumers. **EVID**: consumers of `ari.score` as a `[0,1]` ratio (`compliance/certificate.py:41`) would need that field's contract restated. **DOWN**: increases the weight of ARI-D-021, since range and overflow become the same question. |

---

## DOMAIN 13 — ERROR / MALFORMED INPUT (ARI-D-017 … ARI-D-020)

| Alternative | Consequences |
|---|---|
| **Broad invalid-input set** (dimension mismatch, empty, zero, over-magnitude, wrong type) | **XLANG**: every implementation must detect the same set identically; detection becomes part of equivalence. **CONF**: enables CONF-007 to be authored with concrete triggers and enables FIX-ERROR fixtures. **IMPL**: would describe the primary engine as detecting none of them and the secondary engine as detecting a subset. **DOWN**: gives ARI-D-018/019/020 concrete content. |
| **Narrow or empty invalid-input set** (C-41) | **SPEC**: every input becomes admissible, so a *value* must be defined for every case now considered malformed — including mismatched lengths and zero vectors. **CONF**: CONF-007 would have no ARI-level triggers, and INV-008's application to ARI would need an explicit statement. **XLANG**: the language construct that currently determines mismatch behaviour would have to be specified rather than inherited. |
| **Detection obligatory at the ARI boundary** (C-44 generalized) | **IMPL**: describes a posture the primary engine does not implement. **XLANG**: adds a validation-equivalence surface. **EVID**: validation outcomes may themselves need recording. |
| **Assumed-caller** (C-43) | **SPEC**: requires stating who owns validation and what evidence proves it occurred. **EVID**: without such evidence, an auditor cannot distinguish a valid measurement from a measurement over invalid input. |
| **Response: raise/abort** (C-45) | **EVID**: no ARI value is produced, so evidence must record the failure rather than a number — connecting to ARI-D-020. **XLANG**: exception types and messages are language-specific; equivalence must be defined over an abstract failure category, not a concrete exception. **CONF**: aligns with CONF-007's "safe-state exit code or error response". |
| **Response: sentinel value** (C-47) | **EVID**: the sentinel is indistinguishable from a legitimately computed identical value unless a marker accompanies it — the distinguishability requirement in ARI-D-020. **SPEC**: requires an explicit statement that fail-closed is being implemented by a value rather than by a halt, since INV-008's text speaks of halting. **CONF**: makes error fixtures value-comparable. |
| **Response: error object** (C-46) | **SPEC**: requires a canonical error schema, which APS-200 does not define (`:108` `decision` set TODO). **EVID**: produces a record for every failure, which must be reconciled with INV-008's "no partial output … or persisted". |
| **Response: upstream rejection** (C-48) | **SPEC**: ARI's own specification carries no error semantics; the burden moves to the calling contract. **CONF**: CONF-007 would test the caller, not ARI. |
| **Failure produces evidence** vs **produces none** (ARI-D-020) | **EVID**: the first requires a failure-record schema and interacts with INV-004 (Immutable Evidence) and INV-005 (Traceability); the second leaves failures invisible to audit, which must be a stated position given AURA-CON-001 Article IV Principle 4 ("Evidence Before Trust"). |

---

## DOMAIN 14 — OVERFLOW / RANGE (ARI-D-021)

| Alternative | Consequences |
|---|---|
| **Fixed width with defined wrap** | **XLANG**: portable and testable, but wrapping produces values with no measurement meaning; the specification must state that a wrapped value is still a conformant output or is an error. **CONF**: requires fixtures at the wrap boundary. |
| **Fixed width with saturation** | **SPEC**: saturation collides with Domain 12 bounds — two clamping mechanisms would coexist and their interaction must be specified. **XLANG**: requires explicit saturating arithmetic in languages whose defaults differ. |
| **Fixed width with trap/error** (C-54) | **SPEC/DOWN**: makes overflow an ARI-D-017 invalid condition and an ARI-D-019 response case. **XLANG**: Rust debug builds panic and release builds wrap by default, so the behaviour must be pinned rather than inherited from build profile. |
| **Arbitrary precision** (C-53) | **XLANG**: requires big-integer support or a proof of non-overflow for admissible inputs; the proof depends on ARI-D-006 (dimension) and ARI-D-007 (scale). **CONF**: replaces boundary fixtures with a documented magnitude analysis. |
| **Width chosen so overflow is impossible for admissible inputs** (C-52 generalized) | **SPEC**: requires the worst-case analysis to be published as part of the specification, since it is what makes the width sufficient. **DOWN**: makes ARI-D-006 and ARI-D-007 blocking. |

---

## DOMAIN 15 — SERIALIZATION (ARI-D-022)

| Alternative | Consequences |
|---|---|
| **Canonical JSON, compact separators, sorted keys** (C-55) | **IMPL**: describes one of three current sites; the other two would produce different bytes for the same object. **EVID**: any hash computed over the other form would not match. **XLANG**: JSON number and string escaping rules must be pinned beyond separators (integer-only fields reduce, but do not eliminate, this surface). |
| **Canonical JSON, default separators** (C-56) | As above with the sites reversed; whitespace becomes semantically load-bearing, which must be stated explicitly. |
| **A non-JSON canonical byte sequence** | **SPEC**: follows the SPEC-002 REQ-002-021/022 pattern (representation-to-bytes, field ordering, encoding, absent-field handling, byte boundaries). **XLANG**: removes JSON-library variance entirely. **IMPL**: describes no current site. **EVID**: existing hashes and certificates would be expressed in a different domain. |
| **Integer field `RAW_ARI`** (C-57) vs **float `ari.score`** (C-58) | **EVID**: the integer form is exactly representable and hashable; the float form introduces a second reduction (ARI-D-012) and a binary-representation question. **CONF**: fixture expected-outputs take the form of whichever is chosen. **DOWN**: couples to ARI-D-012 and ARI-D-002 (which quantity is being serialized). |

---

## DOMAIN 16 — REFERENCE MODEL (ARI-D-023)

| Alternative | Consequences |
|---|---|
| **A reference implementation is granted normative authority** | **GOV**: requires the explicit governance grant SPEC-002 `:37` anticipates, and reverses the direction of authority stated in AURA-CON-001 Article V for that scope — a change that must be made deliberately and visibly. **CONF**: conformance becomes comparison-against-implementation; APS-950's certification conditions (`:120-124`) would need to be satisfied, and RI-PY currently records NOT CERTIFIED with RI-004/RI-005 missing. **XLANG**: independent implementations gain an oracle and lose the SPEC-002 §10 property that verification needs no reference inspection. |
| **Specification-only model, no normative reference** (C-62) | **SPEC**: the specification must be complete enough to derive one result — the SPEC-002 §10 Independent Implementer Test standard. **CONF**: fixtures become the oracle instead of an implementation, making ARI-D-025 blocking. **XLANG**: all implementations are peers; divergence is a specification defect, not an implementation defect. |
| **A reference model exists but is advisory** | **GOV**: requires stating what "advisory" means when outputs disagree with the specification. **CONF**: creates a third possible outcome (spec-conformant but reference-divergent) that the conformance report format must be able to express. |
| **Engine A** (C-60) vs **Engine B** (C-61) as the designated engine | **IMPL**: the two differ in validation, clamping and penalty; designating either makes the other's behaviour non-conformant on those axes. **EVID**: records produced by the non-designated engine would need reclassification. **DOWN**: the choice pre-commits several other decisions (ARI-D-005, ARI-D-013, ARI-D-015, ARI-D-016) to whichever engine is designated — which is a reason the designation cannot be made independently of them. |

---

## DOMAIN 17 — CONFORMANCE CONTRACT (ARI-D-024)

| Alternative | Consequences |
|---|---|
| **Repeatability-only criterion** (C-63) | **CONF**: satisfiable by any deterministic implementation regardless of its division, rounding or bounds semantics — so it cannot detect the divergences this package enumerates. **XLANG**: two implementations could both PASS while producing different values. |
| **Cross-platform equality** (C-64) | **CONF**: detects platform-dependent divergence; does not detect language-dependent divergence if both legs run the same language. **DOWN**: depends on an Evidence Pack format (APS-200 `:218` TODO). |
| **Value-equality against fixtures** | **CONF**: detects semantic divergence directly. **DOWN**: makes ARI-D-025 blocking, and each fixture value is itself a decision requiring authority. |
| **Fail-closed criterion** (C-65) | **CONF**: requires ARI-D-017/019 to be decided first, since the test's triggers and expected responses are exactly those decisions. |
| **ARI conformance separable from evidence-pack conformance** | **CONF**: allows ARI to be certified before APS-300/APS-200 complete. **EVID**: certification would then say nothing about the evidence surface, which must be stated so the claim is not over-read. |

---

## DOMAIN 18 — REFERENCE FIXTURES (ARI-D-025)

| Alternative | Consequences |
|---|---|
| **Fixture-based conformance** (C-66 as container) | **GOV**: each fixture value becomes a normative artifact requiring the governance act that grants it that status; per the provenance rule, a fixture is not authority without it. **CONF**: APS-500's own upstream blockers (APS-200 schemas, APS-300 pack) must clear first, by that document's own statement. **XLANG**: fixtures become the shared oracle across languages. |
| **Property-based conformance** (assertions over classes of input rather than pinned values) | **CONF**: reduces the number of values requiring authority, but requires the properties (ARI-D-013.A) to be specified precisely. **XLANG**: property checks are portable; value checks are more directly comparable. |
| **Exact-value fixtures** vs **tolerance fixtures** | **CONF**: exact values interact with INV-002's "bit-perfect" and CONF-001's "bit-identical" language; tolerances require the tolerance itself to be normative and would need reconciling with that language. |
| **Reusing characterization observations as fixture expectations** | **Recorded and not pursued.** Doing so would convert an implementation-derived observation into a normative expectation — precisely what hard boundaries 22–23 forbid and what `NB-021_FROZEN_SEMANTICS_AUDIT.md` §8 CASE E records as the corpus's one unanimous prohibition. The consequence is stated so that the option is visibly excluded, not so that it is weighed. |

---

## DOMAIN 19 — CROSS-LANGUAGE EQUIVALENCE (ARI-D-026)

| Alternative | Consequences |
|---|---|
| **Bit-identity of a canonical byte sequence** (C-68) | **DOWN**: makes ARI-D-022 blocking — there must be canonical bytes before they can be compared. **XLANG**: strongest comparison; also the most sensitive to serialization detail unrelated to the arithmetic. **CONF**: a hash comparison suffices as the test artifact. |
| **Equality of integer outputs** (C-69) | **XLANG**: isolates the arithmetic from serialization, so divergences localize to Domains 5–8 and 14. **CONF**: requires the outputs to be exposed in a comparable form, i.e. an observation surface. **EVID**: does not by itself establish evidence equality. |
| **Equality of evidence-pack hashes** (C-70) | **DOWN**: depends on APS-300 and APS-200 completion. **CONF**: aligns with CONF-006's existing PASS criterion. **XLANG**: couples arithmetic equivalence to evidence-format equivalence, so a divergence does not localize. |
| **Semantic equivalence with a stated tolerance** | **SPEC**: requires the tolerance to be normative and to be reconciled with INV-002's "bit-perfect" language. **XLANG**: permits differing internal representations. **CONF**: PASS criteria become inequalities, changing the shape of every conformance report. |
| **Equivalence required only over a fixture set** vs **over all admissible inputs** | **CONF**: the first is testable and incomplete; the second is complete and requires proof rather than testing. **XLANG**: the second forces every language-dependent construct in ARI-D-026.A.5 to be pinned; the first can leave some unpinned so long as fixtures avoid them — which must then be an accepted, stated limitation. |

---

## DOMAIN 20 — AUDIT / REPRODUCIBILITY (ARI-D-027)

| Alternative | Consequences |
|---|---|
| **Full dependency closure recorded** (the REQ-002-034 pattern applied to ARI) | **EVID**: the record must carry embedding identity, dictionary identity and version, constants, constitution vector identity, specification version and implementation identity — several of which are undecided elsewhere (SPEC-002 AD-CA-005/006, UNRESOLVED) and one of which is a self-declared placeholder in the implementation. **CONF**: enables third-party reproduction, which is the SPEC-002 §5.1/§10 standard. **DOWN**: makes ARI reproducibility depend on SPEC-002's advancement. |
| **Minimal record (inputs and outputs only)** | **EVID**: reproduction is possible only for a party holding the same implementation and dependencies, which is the position RI-PY's registry entry records as the current state (INV-005 ❌, INV-009 ❌). **CONF**: independent verification cannot be claimed. |
| **Provenance inside the hashed representation** | **EVID**: execution context changes the hash, so identical measurements from different runs hash differently — the exact hazard SPEC-002 REQ-002-033 requires be prevented from arising unintentionally. **XLANG**: cross-implementation hash equality becomes unattainable unless provenance is normalized. |
| **Provenance externally bound** | **EVID**: hashes compare across runs and implementations; the binding artifact becomes a separate required object whose integrity must itself be verifiable. |

---

*This document has no normative effect. It states consequences without ranking them, selects no
alternative, recommends nothing, creates no ADR, amends no specification, and modifies no code.*
