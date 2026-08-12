# 01 — P0 REMEDIATION PLAN

**Date:** 2026-08-12
**Mode:** READ-ONLY. **No fix is implemented in this document.**
**Normative effect:** NONE.

> **Standing constraint for this entire document.** Every "candidate implementation
> boundary" below describes *where* a change would sit, never *what* the change should
> decide. No invariant proposed here is asserted as required; each is stated as the
> invariant that **would have to be normatively adopted** before implementation.

---

## §0 The Three P0 Tracks

| Track | Finding | Gating decision | Governance-gated? |
|---|---|---|---|
| **P0-A** | Vector dimension fail-open (RM-01) | NB-015 / `REQ-002-031` **and** NB-021 | **YES — doubly** |
| **P0-B** | Aura-Guard integrity blind spot (RM-08) | D1–D8 (product decision) | **NO** |
| **P0-C** | ARI lacks normative definition (RM-04) | RD-1 | **YES** |

**The asymmetry is the most important fact in this document.** P0-B is gated by a *product*
decision that the Aura governance corpus does not touch. P0-A and P0-C cannot move at all
until governance rules. Ordering work by severity alone would stall the entire P0 track;
ordering it by *gate* releases P0-B immediately.

---

# P0-A — VECTOR DIMENSION FAIL-OPEN

## A.1 Current Behaviour

`zip()` truncates to the shorter of its two sequences. Neither evaluation engine compares
lengths. A vector of **any** length whose leading elements align with the constitution
returns the **maximum possible similarity**.

## A.2 Exact Reproduction

Executed this session against the unmodified working tree at branch base `f3a87cc`,
CPython 3.11, Linux x86_64.

```python
from core.evaluator import PoCAEvaluator

c4 = [100000, 0, 0, 0]                       # 4-dimensional constitution
e  = PoCAEvaluator(c4)

e.vector_similarity_int32([100000, 0], c4)                    # → 100000   (2 of 4)
e.vector_similarity_int32([100000, 0, 0, 0, 99999, 12345], c4) # → 100000   (6 of 4)
e.evaluate("a", [100000, 0], True)            # → {'ari': 100000, 'drift': 0}

c1536 = [100000] + [0] * 1535                # documented dimension
PoCAEvaluator(c1536).vector_similarity_int32([100000], c1536)  # → 100000   (1 of 1536)

PoCAEvaluator([]).evaluate("a", [], True)     # → {'ari': 30000, 'drift': 100000}
```

**Results table.**

| Constitution dim | Agent vector dim | Similarity | ARI | Exception |
|---:|---:|---:|---:|---|
| 4 | 2 | `100000` | `100000` | none |
| 4 | 6 | `100000` | `100000` | none |
| **1536** | **1** | **`100000`** | **`100000`** | none |
| 0 | 0 | `0` | `30000` | none |

Second engine, same session:

```python
from compliance.consistency import ConsistencyCalculator
ConsistencyCalculator([100000,0,0,0], []).calculate(
    {"timestamp": 1, "embedding": [100000, 0], "content": "x"})
# → {'score': 100000, 'structural': 100000, 'semantic': 100000, 'penalty': 0, 'halted': False}
```

**A single-element vector is indistinguishable, in output, from a correct 1536-element
one.** The `1-of-1536` row is the sharpest statement of the finding: 1535 dimensions of
the constitution contribute nothing, and no signal of that reaches the caller.

**The empty-vector row is a distinct sub-case not recorded in the baseline package.** An
empty vector yields `ari = 30000` — the full structural weight — because `valid_schema`
is caller-asserted and the semantic term is simply `0`. There is no input at all, and the
system returns a positive measurement.

## A.3 Affected Functions

| # | Function | File:line | Role |
|---|---|---|---|
| A-1 | `PoCAEvaluator.vector_similarity_int32` | `core/evaluator.py:40` | `zip()` site, Engine A |
| A-2 | `PoCAEvaluator.evaluate` | `core/evaluator.py:70` | calls A-1; no length check |
| A-3 | `PoCAEvaluator.__init__` | `core/evaluator.py:20` | stores constitution unchecked |
| A-4 | `ConsistencyCalculator._semantic_alignment` | `compliance/consistency.py:93` | `zip()` site, Engine B |
| A-5 | `ConsistencyCalculator.calculate` | `compliance/consistency.py:54` | calls A-4 |
| A-6 | `evaluate_with_policy` | `compliance/evaluator_wrapper.py` | wraps A-2; adds no check |

**The constant that would prevent this exists and is unreferenced.**
`CONSTITUTION_DIM = 1536` is defined at `core/offline_normalizer.py:44` and enforced at
`:171` — inside the *offline normalizer*, which is not on the evaluation path.
`grep -n CONSTITUTION_DIM core/evaluator.py compliance/consistency.py` → **zero hits.**

## A.4 Affected Tests

| Test module | Vector lengths used | Would catch this? |
|---|---|---|
| `core/test_ari.py` | 3-element and 10-element, always matching | **No** |
| `core/test_ari.py:214` `test_cosine_similarity_calculation` | passes `[100000,0,0]` against an inline 3-element `v2`, never against `self.evaluator.constitution` (10-dim) | **No** — even this test avoids the mismatch |
| `core/test_integration.py` | matching 16-dim | **No** |
| `test_compliance.py` | matching 1536-dim | **No** |
| `core/test_ari_observability.py` (RD-006) | matching, by design (Limitation 5) | **No — deliberately** |
| `compliance/` | **no unit-test module exists** | **No** |

**No test in either repository passes vectors of differing lengths to any similarity
function.** Verified by exhaustive review of the test corpus.

## A.5 Security / Compliance Consequence

**Direction of failure: FAIL-OPEN.** Malformed input produces the *most favourable
possible* measurement. This is the inverse of the posture the corpus claims.

| Consequence | Detail |
|---|---|
| **Measurement integrity** | The system's sole purpose is to produce a trustworthy measurement. On this input class it produces an untrustworthy one, silently, today. |
| **Invariant contradiction** | `INV-008 Fail Closed` is **Critical**. `reference/RI-PY_AURA_POC_A_CORE.md:55` records INV-008 as ✅ with evidence *"ARI=0 circuit breaker"*. **The reproduction yields ARI = 100000, not 0.** The ✅ is not supported for this input class. *(Recorded as an observation. RI-PY is not edited by this package.)* |
| **Threat model** | `docs/threat_model.md` contains no mention of dimension or length validation. The class is unmodelled. |
| **Downstream propagation** | An out-of-contract value enters every downstream artefact (certificate, fingerprint) unflagged. It would be caught only at `init.sql:47`'s CHECK constraint — which no writer reaches (RM-14). |
| **Adversarial framing** | An actor able to shape the input vector can obtain a perfect alignment score by supplying a *shorter* vector. No forgery of the constitution is required. |

**Not asserted:** that this constitutes non-conformance with any regulatory requirement.
INV-008's normative source (APS-001 §8) is **TODO**, so no such finding can be made.

## A.6 Required Invariant

**ARCHITECTURAL DECISION REQUIRED.**

The invariant that would have to be adopted has two separable halves. Only the first is
free of normative content:

| Half | Statement | Status |
|---|---|---|
| **Detection** | An evaluation whose agent vector dimension differs from the constitution vector dimension MUST be distinguishable from one where they match. | **No decision required to observe the need.** Implementing detection alone still changes control flow → NB-021. |
| **Response** | *What the system must do on detection.* | **ARCHITECTURAL DECISION REQUIRED — NB-015 / `REQ-002-031`.** |

**Candidate responses, listed to make the decision surface explicit. NOT a menu, and no
option is recommended:**

| Option | Consequence |
|---|---|
| Raise an exception | Changes the exception contract; diverges from Engine A's current no-raise posture |
| Return a sentinel | Requires defining the sentinel's value and its meaning downstream |
| Return `0` / minimum | Converts fail-open to fail-closed, but is itself a measurement claim |
| Reject upstream at a validation layer | Moves the boundary; requires deciding where the layer sits relative to CHECK 3/9 |
| Pad or truncate to a defined dimension | Requires AD-CA-007 (dimension) to be resolved first |

**Additionally required and equally undecided:** the dimension itself. `CONSTITUTION_DIM`
is `1536` in code; `init.sql:96` declares `embedding vector(32)`; AD-CA-007 lists `32` as a
**candidate only**. Three values, no decision. Detection cannot be implemented against
"the" dimension because there is no "the" dimension.

## A.7 Candidate Implementation Boundary

**Boundaries only. No design is selected.**

| # | Boundary | Sits at | Notes |
|---|---|---|---|
| **BA-1** | Inside `vector_similarity_int32` | `core/evaluator.py:40` | Closest to the defect. Touches `core/` — must re-pass CHECK 2, 3, 5, 9. |
| **BA-2** | At `evaluate()` entry | `core/evaluator.py:50` | Keeps the similarity function pure; validates once per evaluation. |
| **BA-3** | At `__init__`, binding the expected dimension | `core/evaluator.py:20` | Makes the evaluator's contract explicit at construction. |
| **BA-4** | In a separate validation layer outside `core/` | new module | Avoids modifying frozen `core/`; requires deciding the layer's position against CHECK 9's AST boundary rules. |
| **BA-5** | Upstream, at the normalizer | `core/offline_normalizer.py` | Where `CONSTITUTION_DIM` already lives — but the evaluator is reachable without passing through it. |

**Invariant across all boundaries:** whichever is chosen, both engines (A-1 and A-4) must
be covered, or the divergence recorded in RM-06 widens.

## A.8 Regression Test — after NB-015 and RD-3

**Not written. Specified only.**

| ID | Case | Asserts |
|---|---|---|
| RT-A1 | shorter vector (2 of 4) | the decided response |
| RT-A2 | longer vector (6 of 4) | the decided response |
| RT-A3 | 1 of 1536 | the decided response at documented dimension |
| RT-A4 | empty vector, non-empty constitution | the decided response |
| RT-A5 | non-empty vector, empty constitution | the decided response |
| RT-A6 | both empty | the decided response |
| RT-A7 | exact match | **unchanged** behaviour — the control |
| RT-A8 | same six cases against `ConsistencyCalculator` | parity between engines |

Each must cite the authorizing decision in the test body. Until then, only the
**characterization** equivalents (CH-01, CH-02, CH-04 in `03`) may be written.

## A.9 Status

> **THE FIX IS NOT IMPLEMENTED AND MUST NOT BE, pending NB-021 and NB-015.**
> Per the task instruction: *"Do NOT implement the fix unless NB-021/FROZEN governance
> explicitly permits it."* NB-021 is **INDETERMINATE**. No permission exists.

---

# P0-B — AURA-GUARD INTEGRITY BLIND SPOT

**Detailed remediation plan: `06_GUARD_G1_REMEDIATION_PLAN.md`.** This section carries the
P0-level summary and the items the task requires here specifically.

## B.1 Finding

`violations` is not among the inputs to the chain digest. **Re-verified at source this
session** — `GUARD src/chain.rs:36-47`, commit `443f72e`.

## B.2 Custody Chain

```
Violation{rule, action, confidence, validator}      [models.rs:30-42]
        │
        ✗  NOT AN INPUT
        │
chain_hash = SHA-256( 9 fields joined by "|" )      [chain.rs:36-47]
        │
        ├──► prev_hash of entry N+1                 [chain.rs:89]
        │
        └──► hex::decode ──► leaf_hash(0x00 ‖ raw)  [segment.rs:141-147]
                    │
                    └──► segment_merkle_root        [segment.rs:151-157]
                                │
                                └──► segment_chain_preimage  [segment.rs:91-106]
                                          ├──► segment_chain_hash
                                          └──► tsa_message_imprint   → RFC 3161 anchor
```

**The gap is at the root.** All four downstream mechanisms derive from `chain_hash`.
Adding a fifth mechanism downstream would not close it.

## B.3 Digest Boundary

Nine of fourteen `AuditEntry` fields are covered. Five are not: `schema`, `audit_id`,
`request_id`, `violations`, `chain_hash` (self-referential). **Of the five, `violations`
is the only one carrying substantive decision content.**

## B.4 Consequences

| Layer | Consequence |
|---|---|
| **Merkle** | Leaves are built from `chain_hash` alone (`segment.rs:141`). Violation mutation changes no leaf. |
| **Segment** | `segment_chain_preimage` joins five values, none derived from `violations`. Manifests continue to verify. |
| **TSA** | `tsa_message_imprint` hashes that same preimage. **An RFC 3161 token obtained before a mutation still validates after it** — the anchor attests to a root that never covered the mutated data. |

## B.5 Reproduction

Executed and committed as `GUARD-G1_CHARACTERIZATION_TESTS.rs` (386 lines).

| Mutation | `recompute_for_entry == chain_hash`? |
|---|:--:|
| `violations` emptied to `[]` | **TRUE — verifies** |
| rule/action/confidence rewritten | **TRUE — verifies** |
| fabricated violation appended | **TRUE — verifies** |
| **CONTROL:** `decision` `DENY` → `ALLOW` | **FALSE — chain breaks** |

The control confirms fidelity. `aura-replay` reports `CHAIN OK`, exit code `0`.

**Bound on exposure (recorded for proportionality):** the nine covered fields cannot be
altered. A tampered record can therefore be made *internally inconsistent* — e.g.
`decision: "DENY"` with `violations: []`. That inconsistency is detectable by a human who
reasons about it; it is **not** detected by any automated verification the product ships.

## B.6 Required Decisions D1–D8

Reproduced from `GUARD-G1_INTEGRITY_DESIGN_BRIEF.md` §12. **All eight remain open.**

| ID | Decision |
|---|---|
| **D1** | Accept, mitigate procedurally, or address cryptographically? (Selects among boundaries B1–B5.) |
| **D2** | Is retroactive verifiability of existing logs a requirement? (Determines whether B1/B2 are admissible at all.) |
| **D3** | What byte reduction of violation data is authoritative? Field set, field order, `Option::None` encoding, empty-vector encoding, separator/escaping rules. **ARCHITECTURAL DECISION REQUIRED — explicitly not answered.** |
| **D4** | Does `confidence` (`f32`) participate, and in what representation? Coupled to D3. |
| **D5** | Which hash domain does the reduction belong to? **ARCHITECTURAL DECISION REQUIRED.** |
| **D6** | Migration mechanism and schema-discriminator policy for `"aura-guard.audit.v1"`. |
| **D7** | Disposition of RFC 3161 tokens already obtained under the current rule. |
| **D8** | Does the `/v1/audit` response shape change, and what is the integrator notification path? |

## B.7 Migration Implications

Any change to the digest input changes every subsequent `chain_hash`. Therefore:

- entries written before and after cannot be verified by one rule;
- a log spanning the change point contains two digest regimes;
- Merkle roots, segment chain hashes, and **any RFC 3161 tokens obtained before the change
  remain valid only under the old rule**;
- `prev_hash` linkage is unaffected in *form* but the two sides are computed under
  different definitions.

**Precedent available, not currently used on this path:** `SEGMENT_SCHEMA` is checked for
equality at `sealer.rs:100`. The audit-entry path has no equivalent — `read_all_entries()`
deserializes without inspecting `schema`, and `verify_chain()` does not read it.

## B.8 Regression Tests

Specified in `06` §7 (T-0a…T-0c available now; T-1…T-11 after D1–D7). Not written here.

## B.9 Status

> **No serialization format, canonical representation, or hash domain is selected.**
> Per the task instruction. D1–D8 are for an authorized decision-maker.

**But note the gate:** P0-B is **not** blocked by DR-002, SPEC-002, any AD-CA, or NB-021.
Guard contains zero occurrences of `constitution`, `ari`, `poca`, `frozen`, or `freeze`.
The decision it waits on is a **product decision about the audit-log format**, and it is
available to be taken today.

---

# P0-C — ARI LACKS NORMATIVE DEFINITION

## C.1 Instruction Compliance

> Per the task: **"Do NOT attempt to fix ARI values."** No ARI value is proposed,
> corrected, clamped, bounded, or recommended anywhere in this package.

The full treatment is `02_ARI_NORMATIVE_GAP.md`. Summary only here.

## C.2 The Structural Fact

**ARI has no normative definition anywhere in the specification corpus.** Re-verified at
primary source this session across `aps/`, `specification/`, `invariants/`,
`constitution/`, `conformance/`, `glossary/`:

> `glossary/GLOSSARY.md:27-28` — **ARI** (Aura Reliability Index): *"A deterministic
> measurement value computed by RI-PY using integer arithmetic. ARI is a measurement, not
> a decision."*

**The glossary defines ARI by reference to the implementation.** No APS document specifies
its formula, range, dimension, division rule, or rounding rule.

## C.3 Why This Blocks Everything Downstream

The question *"remediated to what?"* has no answer. Every ARI-related finding —
RM-01, RM-02, RM-03, RM-04, RM-06 — resolves to the same missing anchor.

**This produces a circularity that must be broken by decision, not by engineering:**

```
ARI is defined as "what RI-PY computes"
        │
        └──► RI-PY's computation is the thing under audit
                    │
                    └──► the audit's finding is that it exceeds its documented range
                                │
                                └──► the documented range has no normative source
                                            │
                                            └──► ARI is defined as "what RI-PY computes"
```

**Any attempt to resolve this circle by engineering makes implementation behaviour
normative** — stop condition 8. The only exit is RD-1.

## C.4 Status

**ARCHITECTURAL DECISION REQUIRED — RD-1.** See `02_ARI_NORMATIVE_GAP.md` for the 15
dimensions that must be specified, all of which are currently undecided.

---

## §9 Cross-Track Summary

| | P0-A | P0-B | P0-C |
|---|---|---|---|
| Reproduced | **YES** | **YES** | **YES** (the absence) |
| Characterization available now | **YES** | **YES** | **YES** |
| Fix available now | **NO** | **NO** — pending D1/D2 | **NO** |
| Governance-gated | **YES** (NB-021 + NB-015) | **NO** | **YES** (RD-1) |
| Decision-maker | Protocol Custodian | **Product owner** | Protocol Custodian |

**Single highest-value observation:** P0-B's decision-maker is different from P0-A's and
P0-C's, and its decision has no dependency on theirs. **P0-B can proceed in parallel while
governance deliberates.**

---

*This document has no normative effect. It implements no fix, selects no semantics,
creates no ADR, and modifies no code.*
