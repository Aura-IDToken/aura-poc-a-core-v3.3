# 07 — CONFORMANCE AND REFERENCE MODEL REQUIREMENTS

**Package:** RD-1-ARI-DECISION-READINESS · **Normative effect:** NONE

---

## 0. Status and scope of this document

This document states, in requirement form, **what a future reference model, a future independent
implementation, and a future conformance suite would have to satisfy** for normative ARI to be
independently verifiable.

**These requirements are not approved and are not in force.** They are *prepared for review*
under the two-key protocol in `08_TWO_KEY_DECISION_PROTOCOL.md`. Identifiers `RM-nnn`, `II-nnn`
and `CS-nnn` are local to this package.

**They constrain form, not content.** No requirement below states which formula, division rule,
rounding rule, dimension, bound, similarity model, drift model, penalty model, serialization,
overflow behaviour, or engine ARI must have. Every requirement is of the shape *"whatever is
decided, it must be stated/derivable/verifiable in this way"*.

Each requirement carries the existing source whose pattern it follows, so that the review can see
that it is transcribed from the corpus rather than invented.

---

## 1. Preconditions — none of the following is satisfiable today

| # | Precondition | Current state |
|---|---|---|
| P-1 | A normative ARI definition exists | **Absent** — RD-1 (CLOSED) |
| P-2 | The decisions ARI-D-001 … ARI-D-027 are made | **0 of 27 decided** |
| P-3 | APS-001 §3, §4, §8 are authored | `Status: TODO` (`aura-specification/specification/APS-001_PROTOCOL_SPECIFICATION.md:5,44-46,48-50,64-66`) |
| P-4 | A canonical serialization exists | `TODO` (`aura-specification/aps/APS-200_CANONICAL_DATA_MODEL.md:218`) |
| P-5 | Fixtures exist | `TODO` (`aura-specification/aps/APS-500_REFERENCE_FIXTURES.md:63`; `fixtures/core/FIX-001_BASIC_EVALUATION.json` all fields `"TODO"`) |
| P-6 | CONF tests are beyond DRAFT | All ten are `DRAFT` (`aura-specification/aps/APS-400_CONFORMANCE_TEST_MATRIX.md:53-64`) |
| P-7 | Invariant traceability is verified | Every row **NOT VERIFIED** for both RI-PY and RI-RS (`aura-specification/compliance/TRACEABILITY_MATRIX.md:18-32`) |

Nothing below asserts that these preconditions will be met, or in what order.

---

## 2. Reference-model requirements (RM)

A "reference model" here means whatever artifact a future decision (ARI-D-023) designates as the
model of ARI — a specification section, a specification-plus-fixtures pair, or a designated
implementation. These requirements apply to whichever form is chosen.

| ID | Requirement | Pattern source |
|---|---|---|
| **RM-001** | The reference model MUST be identified by document ID, version and lifecycle status, and MUST NOT be identified by repository name, branch, or filename alone. | `aura-specification/aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` identifier rules; SPEC-002 REQ-002-003 |
| **RM-002** | The reference model MUST state which of the coexisting ARI engines, if any, it describes. A model that does not name its subject MUST NOT be treated as designating either. | Two engines exist: `aura-poc-a-core-v3.3/core/evaluator.py` (+ `compliance/evaluator_wrapper.py`) and `compliance/consistency.py` |
| **RM-003** | If the reference model is an implementation, an explicit approved governance artifact MUST grant it normative authority; absent that grant, its behaviour remains non-normative. | SPEC-002 `:37` verbatim requirement |
| **RM-004** | The reference model MUST be sufficient to derive exactly one result for every admissible input; any legitimate multi-outcome path MUST be recorded as a readiness failure. | SPEC-002 `:315` (REQ-002-032), `:537` (§10) |
| **RM-005** | The reference model MUST be usable without inspecting any implementation source code. | SPEC-002 `:291` (REQ-002-030), `:531-536` |
| **RM-006** | The reference model MUST state, for every value it fixes, the decision identifier that authorized it. | `aura-specification/aps/APS-100_PROTOCOL_INVARIANTS.md:116-134` traceability chain |
| **RM-007** | The reference model MUST carry its own dependency closure: embedding identity and version, dictionary identity and version, constants, and the constitution vector identity it presumes. | SPEC-002 `:246-260` (REQ-002-034) |
| **RM-008** | The reference model MUST NOT contain a value whose only justification is that an implementation produces it. | RD-1 premise 9; hard boundaries 21–23 |
| **RM-009** | The reference model MUST state its versioning and supersession rules, including what happens to evidence produced under a superseded version. | SPEC-002 `:266-267` (REQ-002-026/027); `aura-specification/VERSIONING.md` §3–§4 |
| **RM-010** | Where the reference model leaves a behaviour undefined, it MUST say so explicitly rather than omitting it. | AURA-CON-001 Article IV Principle 8 ("Implicit behaviour is undefined behaviour") |

---

## 3. Independent-implementation requirements (II)

These state what an implementation would have to be able to do — and what the specification would
have to give it — for a conformance claim about ARI to be meaningful.

| ID | Requirement | Pattern source |
|---|---|---|
| **II-001** | An independent implementer MUST be able to produce a conformant ARI implementation using only approved normative documents, approved decisions and approved fixtures — without inspecting `aura-poc-a-core-v3.3`, `aura-guard-v1.3`, or any other implementation. | SPEC-002 `:500-536` (§10) |
| **II-002** | The implementer MUST NOT need to infer any behaviour from a language default. Every construct whose default differs across the in-scope languages MUST be pinned by an approved decision. | `04_CONSEQUENCE_MATRIX.md` Domains 7, 8, 14, 15; SPEC-002 `:107` |
| **II-003** | The specification MUST enumerate the constructs of II-002 explicitly, so that an implementer can check coverage rather than discover gaps by divergence. At minimum: integer division on negative dividends; rounding ties in both signs; integer width and overflow at every arithmetic position; accumulation order; serialization byte production. | ARI-D-026.A.5 |
| **II-004** | The implementer MUST be able to determine, for any input, whether it is admissible, without consulting an implementation. | ARI-D-004, ARI-D-017; AURA-CON-001 Article IV Principle 6 |
| **II-005** | The implementer MUST be able to produce the same failure classification as any other conformant implementation for an inadmissible input, expressed in language-neutral terms rather than as a concrete exception type. | ARI-D-019; `aura-specification/conformance/CONF-007_FAIL_CLOSED.md:46` |
| **II-006** | The implementer MUST be able to emit the observation surface required by the equivalence definition (ARI-D-026), so that equivalence is checkable rather than asserted. | `review/2026-08-11_ENGINEERING_BASELINE/RD-006_ARI_OBSERVABILITY.md` §8 records that no such surface is currently exercised cross-architecture |
| **II-007** | An implementation MUST declare the specification version and decision set it implements, and MUST carry that declaration into evidence. | `aura-specification/aps/APS-200_CANONICAL_DATA_MODEL.md:49-58` (Common Object Contract); INV-009 |
| **II-008** | Two independent implementations MUST NOT be able to disagree on any output for an admissible input while both satisfying the specification; if they can, the specification is incomplete by its own criterion. | SPEC-002 `:315`, `:481` |
| **II-009** | An implementation's claim of conformance MUST be evidenced by executed conformance runs, not by inspection or assertion. | `aura-specification/aps/APS-400_CONFORMANCE_TEST_MATRIX.md:138-148`; `aura-poc-a-core-v3.3/CLAUDE.md` ("Require executable evidence alignment for every conformance claim") |
| **II-010** | The set of in-scope languages and platforms MUST be stated; a conformance claim MUST NOT be generalized beyond the set actually exercised. | `RD-006_ARI_OBSERVABILITY.md` §8 ("Observed on this platform only … no cross-platform claim is made") |

---

## 4. Conformance-suite requirements (CS)

| ID | Requirement | Pattern source |
|---|---|---|
| **CS-001** | Every ARI conformance test MUST cite the invariant and the decision identifier it verifies. | APS-100 §5 traceability chain; APS-400 §3 test-definition fields |
| **CS-002** | The suite MUST distinguish **determinism** (same valid input → same output) from **integrity** (modified or invalid input → detectable failure) and MUST verify both independently. | SPEC-002 `:355-363` (§5.3) |
| **CS-003** | A repeatability-only criterion MUST NOT be accepted as sufficient evidence of ARI conformance on its own, because it is satisfied under any division, rounding or bounds semantics. If it is nevertheless used alone, that limitation MUST be recorded in the conformance report. | `05_CORE_REMEDIATION_READINESS.md` §5.6 records the same property of the existing CHECK 8; APS-400 CONF-001 PASS criterion |
| **CS-004** | The suite MUST include cases that discriminate between the decided rule and the rejected alternatives for every language-dependent construct — at minimum a negative dividend that is not an exact multiple of the scale, and tie cases in both signs. | ARI-D-010, ARI-D-011 |
| **CS-005** | The suite MUST include inadmissible-input cases covering every condition in the decided invalid-input set, verifying the decided response class rather than a numeric value — unless the decision explicitly specifies a value. | ARI-D-017, ARI-D-019; CONF-007 |
| **CS-006** | Every expected value in the suite MUST be derivable from the specification. A value obtained by executing an implementation MUST NOT be used as an expected value. | `NB-021_FROZEN_SEMANTICS_AUDIT.md` §8 CASE E ("the one case … where the corpus is unanimous"); hard boundaries 22–23 |
| **CS-007** | Fixtures MUST be immutable once approved; a changed expectation MUST create a new fixture identifier rather than modifying an existing one. | `aura-specification/aps/APS-500_REFERENCE_FIXTURES.md:81` |
| **CS-008** | The suite MUST be executable by an independent party against an implementation it did not write, using only published artifacts. | SPEC-002 §10; APS-950 §7 |
| **CS-009** | Conformance results MUST distinguish PASS, FAIL, NOT APPLICABLE and ERROR, and MUST NOT report an unexecuted test as passing. | APS-400 `:128-134`; `RD-006_ARI_OBSERVABILITY.md` §6.3 precedent of reporting Docker-gated checks as "not executed" rather than as passing |
| **CS-010** | The suite MUST verify the cross-language equivalence relation defined by ARI-D-026 over the stated input set, and MUST report the residual freedom, if any, that it does not cover. | ARI-D-026; SPEC-002 `:315` |
| **CS-011** | The suite MUST verify that evidence records contain the fields required for reproduction (ARI-D-027), not merely that a value was produced. | INV-005; SPEC-002 REQ-002-034 |
| **CS-012** | Characterization tests, if retained alongside the suite, MUST remain labelled as characterization and MUST NOT be cited as conformance evidence; the two MUST be separable in reporting. | `aura-poc-a-core-v3.3/core/test_ari_observability.py:4-16`; `RD-006_ARI_OBSERVABILITY.md` §9 |

---

## 5. The verification chain a future ARI would have to satisfy

Transcribed in shape from SPEC-002 §5.1 (`:325-337`), which states it for the Constitution
Artifact. **Whether this chain applies to ARI is itself an open decision** (ARI-D-026, candidate
C-71); it is reproduced here as the pattern the corpus already contains, not as a decision.

```
        same admissible input
                 ↓
        same intermediate quantities        (requires ARI-D-009, ARI-D-010, ARI-D-011)
                 ↓
        same ARI value (and drift, if normative)   (requires ARI-D-013 … ARI-D-016)
                 ↓
        same canonical bytes                (requires ARI-D-022)
                 ↓
        same hash values                    (requires ARI-D-022, ARI-D-027)
                 ↓
        same evidence record                (requires ARI-D-020, ARI-D-027)
```

And the negative chain, transcribed in shape from SPEC-002 §5.2 (`:341-353`):

```
        inadmissible input           → detectable, classified failure   (ARI-D-017 … ARI-D-020)
        altered evidence record      → integrity failure                (INV-004, INV-011)
        altered constitution vector  → identity/integrity failure       (SPEC-002 AD-CA-009)
        wrong provenance binding     → provenance failure               (ARI-D-027)
```

---

## 6. What would make a future conformance claim about ARI defensible

Stated as a checklist of conditions, all of which are currently unmet:

1. Every decision ARI-D-001 … ARI-D-027 is resolved, or explicitly ruled out of scope, by an
   authority with jurisdiction over it.
2. Each resolution carries the evidence set required in `06_EVIDENCE_REQUIREMENTS.md` §4.
3. The requirements in §2–§4 above are approved (or replaced by approved equivalents).
4. The preconditions in §1 are satisfied.
5. An independent implementation exists that was built without inspecting an existing one.
6. The conformance suite discriminates the decided semantics from the rejected alternatives.
7. Conformance runs are executed and their evidence recorded, with unexecuted tests reported as
   unexecuted.
8. The governance question of what a corrected or newly-specified Core means for instrument
   identity has been answered by the authority that owns it — recorded as unresolved in
   `NB-021_FROZEN_SEMANTICS_AUDIT.md` and **not reopened here**.

---

*This document has no normative effect. Its requirements are prepared for review, not approved.
It selects no ARI semantics, creates no ADR, amends no specification, creates no fixture, and
modifies no code.*
