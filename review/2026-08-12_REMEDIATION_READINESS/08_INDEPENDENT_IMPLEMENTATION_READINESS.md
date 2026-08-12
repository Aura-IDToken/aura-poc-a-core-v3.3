# 08 — INDEPENDENT IMPLEMENTATION READINESS

**Date:** 2026-08-12
**Mode:** DEFINITION ONLY. **No second ARI engine was implemented, prototyped, or scaffolded.**
**Normative effect:** NONE.

---

## §1 The Governing Constraint

> **AN INDEPENDENT IMPLEMENTATION CANNOT BE BASED ON COPYING PYTHON IMPLEMENTATION
> SEMANTICS.**

This is not a stylistic preference. It is the **entire evidentiary value** of the exercise.

An implementation derived from RI-PY's behaviour proves only that copying works. It cannot
detect the divergences it exists to detect, because it inherits them by construction. Two
implementations agreeing because one was copied from the other is **not** independent
verification — it is the same measurement taken twice.

`SPEC-002 §10` states the requirement in its own terms: an independent implementer, using
**only approved documents**, must derive exactly one canonical result.

**Today that test cannot be run**, because the approved documents do not define the
computation. See §7.

---

## §2 Readiness Verdict

# NOT READY

| Prerequisite | State |
|---|---|
| A normative definition of ARI exists | **NO** — `glossary/GLOSSARY.md:27-28` defers to RI-PY (AG-01…AG-15 all undecided) |
| Division semantics decided | **NO** — **unregistered in any candidate list** |
| Rounding semantics decided | **NO** — candidate only |
| Numeric representation decided | **NO** — AD-CA-007 UNRESOLVED |
| Canonical byte encoding decided | **NO** — AD-CA-008 "None approved" |
| Vector dimension decided | **NO** — three conflicting values (`1536`, `32`, candidate `32`) |
| Failure semantics decided | **NO** — `REQ-002-031` unresolved; APS-001 §8 TODO |
| Conformance fixtures exist | **NO** — FIX-001, FIX-ERROR both **TODO** |
| A conformance runner exists | **NO** — RI-004 **MISSING** for both RI-PY and RI-RS |

**Nine of nine prerequisites unmet.** Building now would not produce independent evidence;
it would produce **a second set of implementation-derived behaviours competing for
authority** — doubling the problem this package exists to contain.

---

## §3 What the Independent Implementation MUST Receive

Only these. Nothing else.

| # | Input | Form | Currently exists? |
|---|---|---|---|
| **R-1** | The normative ARI specification | approved document covering AG-01…AG-15 | **NO** |
| **R-2** | Numeric representation | width, signedness, scale, endianness, dimension, accumulator width, overflow behaviour | **NO** — AD-CA-007 |
| **R-3** | Division rule | explicit statement for negative dividends | **NO** — unregistered |
| **R-4** | Rounding rule | explicit statement including `.5` boundaries, both signs | **NO** — candidate only |
| **R-5** | Failure semantics | required response to malformed input, dimension mismatch, zero vectors, out-of-scale values | **NO** — `REQ-002-031` |
| **R-6** | Canonical byte encoding | for inputs and outputs, production-grade | **NO** — AD-CA-008 |
| **R-7** | Normative input fixtures | approved, with provenance | **NO** — FIX-001 TODO |
| **R-8** | Normative output fixtures | approved expected values | **NO** — see §5 |
| **R-9** | The replay protocol | §6 below | definable now |
| **R-10** | The comparison procedure | §7 below | definable now |

**R-1 through R-8 do not exist.** R-9 and R-10 are definable today and are defined below —
that is the whole of the available work.

---

## §4 What It MUST NOT Receive

This section is the contamination control. Each item is a **channel through which
implementation semantics could leak into a supposedly independent implementation.**

| # | Prohibited input | Why |
|---|---|---|
| **X-1** | RI-PY source code, in whole or in part | Direct copying. The implementer must not read `core/evaluator.py`. |
| **X-2** | RI-PY docstrings | They state `[0,100000]` and "cosine-equivalent" — **implementation documentation, not specification**, and demonstrably at odds with observed behaviour. |
| **X-3** | Observed ARI values (OBS-1…OBS-5, CH-01…CH-15, OB-A…OB-J) | **Implementation-derived and non-normative.** Supplying them as expected outputs converts characterization into specification — stop condition 8. |
| **X-4** | `artifacts/rd-006-ari-observation.json` | Same. It carries `"normative_effect": "NONE"` precisely so it is not used this way. |
| **X-5** | The determinism report's vectors | `ari_vector_hash` hashes the constitution vector, not an ARI, and encodes `round()`'s current behaviour. |
| **X-6** | `core/test_*.py` expected values | `test_offline_normalizer.py:97-107` **already locks in half-to-even against no specification** — the clearest existing example of accidental authority. |
| **X-7** | Any Python-language idiom as a specification statement | "`//`" is not a rule; it is one language's spelling of one of two rules. |
| **X-8** | `init.sql` constraints | `RAW_ARI BETWEEN 0 AND 100000` and `vector(32)` are **unratified** and conflict with `CONSTITUTION_DIM = 1536`. |
| **X-9** | This review package's reproductions | Everything in `00`–`11` is AS-IS evidence, explicitly non-normative. |
| **X-10** | Informal transfer — conversation, review comments, a shared engineer | The most likely leak in practice, and the hardest to audit. |

---

## §5 The Fixture Trap

**This is the single most dangerous step in the entire remediation programme.**

The natural move — *"run RI-PY, record outputs, use them as expected values"* — would:

1. convert implementation behaviour into normative authority (**stop condition 8**);
2. encode unapproved candidate answers into fixtures (**stop condition 5**);
3. guarantee the independent implementation "passes" by reproducing the defects — including
   RM-01's fail-open maximum score;
4. **retire the open questions without deciding them.**

The failure is silent. A green conformance run would be produced, and it would mean nothing.

### §5.1 The required order

```
NORMATIVE DECISION  (AG-01…AG-15)
        ↓
SPECIFICATION TEXT  (approved, beyond DRAFT)
        ↓
NORMATIVE FIXTURE   (expected value derived FROM THE TEXT, by hand or by an
                     independent tool — NEVER by executing RI-PY)
        ↓
BOTH implementations run against the fixture
        ↓
Divergence from the fixture is a DEFECT — in either or both
```

### §5.2 The prohibited order

```
RUN RI-PY  →  record output  →  call it a fixture  →  both implementations "pass"
```

**Distinguishing test.** For every fixture, the question *"where did this expected value
come from?"* must be answerable with **"from the specification text"** — never with
**"from running the implementation."** If a fixture's provenance cannot be traced to an
approved document, it is contaminated and must not be used.

---

## §6 Replay Protocol — definable now

| Step | Requirement |
|---|---|
| **P-1** | Both implementations receive **identical normative input fixtures** — byte-identical files, not equivalent constructions |
| **P-2** | Both emit output in the **normatively defined encoding** (R-6). Comparison at the byte level requires a defined encoding; equal-numbers-different-bytes is a failure. |
| **P-3** | Each emits a **runtime identity record**: OS, architecture, word size, endianness, language version, toolchain version |
| **P-4** | Comparison is **byte-level over the encoded output**, not value-level over parsed structures |
| **P-5** | Any divergence is a **finding**, never auto-reconciled, never "explained" by adjusting one side |
| **P-6** | Failure cases are compared too — same input class must produce the same **defined** failure |
| **P-7** | Records must be **reproducible from the fixtures alone**, with no environmental input |
| **P-8** | The comparison harness must not import either implementation — it consumes emitted records only |

**P-8 is the structural independence guarantee.** A harness that imports both can leak
semantics between them. The existing `scripts/compare_determinism_reports.py` already has
the right shape: it compares emitted artefacts.

### §6.1 Byte-level comparison — what it requires

| Requirement | Currently exists? |
|---|---|
| A defined byte encoding for integer vectors | **NO** — AD-CA-007/008 |
| A defined encoding for ARI/drift output | **NO** — AG-14 |
| A defined encoding for failure results | **NO** — AG-01/R-5 |
| A defined canonical JSON form for records | **NO** — AD-CA-008 "None approved" |

**None exists.** The only integer encoding anywhere in the ecosystem is LE-signed 4-byte
and it lives **solely in test/CI code** (`core/test_bitwise_replay.py:287`,
`scripts/generate_determinism_report.py:65`) — production uses none. A byte-level protocol
therefore cannot be executed today even if both implementations existed.

---

## §7 Independence Requirements

| # | Requirement | Verification |
|---|---|---|
| **I-1** | Different implementer(s) from RI-PY's authors | recorded provenance |
| **I-2** | Implementer has **not read** RI-PY source | attestation |
| **I-3** | Implementation derived **only** from approved documents | traceability from each behaviour to a document clause |
| **I-4** | Different language, with **different default semantics** for division, rounding and integer width | **This is the point.** A second Python implementation would inherit `//` and `round()` and detect nothing. |
| **I-5** | No shared code, no shared constants, no shared fixtures **other than the normative ones** | dependency audit |
| **I-6** | Fixture provenance traceable to specification text, never to execution | §5.2 |
| **I-7** | Divergences reported before reconciliation | process control |

**I-4 deserves emphasis.** The divergences at stake (AG-06, AG-07) are precisely those where
Python's defaults differ from Rust's, C's and JavaScript's. **An independent implementation
in Python would be independent in authorship and useless in effect.**

---

## §8 Contamination Risks

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| **CR-1** | Fixtures generated by executing RI-PY | **HIGH** — it is the path of least resistance | §5.2 provenance rule |
| **CR-2** | The specification is written **by reading the implementation** | **HIGH** | RD-1 must be a decision, not a transcription. The glossary already does this: it *defines ARI as what RI-PY computes*. |
| **CR-3** | Implementer consults RI-PY when the spec is ambiguous | **HIGH** | Ambiguity must be escalated as a specification defect, never resolved by reading code |
| **CR-4** | Reviewer transfers semantics informally | **MEDIUM** | Review by document reference only |
| **CR-5** | Observed values leak in via a review package | **MEDIUM** | Every value in this package is labelled non-normative; X-9 |
| **CR-6** | Second implementation adjusted until it matches RI-PY | **HIGH** | P-5: divergence is a finding, not a defect in the newcomer |
| **CR-7** | Ported test suites carry expected values | **MEDIUM** | X-6 — the existing rounding test is already contaminated |
| **CR-8** | Same LLM/agent writes both | **MEDIUM** | Recorded provenance; separate context |

**CR-2 is the most consequential and is already realised.** `glossary/GLOSSARY.md:27-28`
defines ARI as *"a deterministic measurement value computed by RI-PY"* — the specification
already defers to the implementation. **RD-1 must break that, or the independent
implementation is contaminated at its source, before a line is written.**

---

## §9 What Can Be Done Now

| # | Work | Blocked? |
|---|---|---|
| N-1 | This document — define receives / must-not-receive / protocol / independence / risks | **NO** |
| N-2 | Define the fixture **format** (not its contents) | **NO** |
| N-3 | Define the runtime identity record schema | **NO** |
| N-4 | Define the comparison harness **shape** (P-8: consumes records, imports nothing) | **NO** |
| N-5 | Record contamination controls as a reviewable checklist | **NO** |
| N-6 | Write any fixture **content** | **BLOCKED** — R-7/R-8 |
| N-7 | Implement any part of a second engine | **BLOCKED** — R-1…R-6 |
| N-8 | Run any comparison | **BLOCKED** — nothing to compare |

---

## §10 The Ordering Trap

Recorded explicitly, because it is counter-intuitive and easy to get backwards.

`04_DETERMINISM_AUDIT.md` classifies the division and rounding findings as **LATENT**
*because no second implementation exists*. Building one makes them **ACTIVE**.

> **Building the independent implementation before the decisions exist does not surface a
> divergence to be resolved. It creates a second implementation-derived behaviour with
> equal claim to authority — and no means of adjudicating between them.**

The ecosystem currently has **one** unspecified measurement. Building now yields **two**
unspecified measurements and a disagreement no document can settle.

**Correct order:** RD-1 and RD-3 → specification text → normative fixtures → independent
implementation → comparison.

---

## §11 Explicit Non-Goals

Does not implement a second ARI engine. Does not scaffold, prototype, or stub one. Does not
select a language. Does not create fixtures. Does not define ARI or any semantic. Does not
authorize construction. Does not treat any RI-PY behaviour as a requirement.

---

*This document has no normative effect. It defines the conditions under which an
independent implementation would constitute evidence — and records that those conditions
are not met.*
