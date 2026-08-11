# 05 — CORE REMEDIATION READINESS ASSESSMENT

**Phase:** 5 — Core Remediation (preparation only)
**Date:** 2026-08-11
**Role:** Verification & Determinism readiness assessment
**Mode:** READ-ONLY. **No code, CI, specification, ADR or governance artefact was modified.**
**Governing direction:** Decision → Specification → Implementation → Test → Evidence.
This document sits at the **left** of that chain and does not cross rightwards.

> **Filename note.** The prefix `05_` is shared with the existing `05_TEST_MATRIX.md`.
> The name was specified by the task; the two files are distinct and neither replaces the
> other.

---

## §1 Executive Summary

Six findings were assessed. **All six are confirmed and reproduced.** Two are ACTIVE in
pure Python today; three are LATENT pending a second implementation; one is a
verification-coverage gap.

**The blocking result is not any individual defect.** It is that the normative anchor
against which Core would be repaired **does not exist**:

| Anchor sought | State |
|---|---|
| Normative definition of ARI (formula, range, dimension) | **Absent.** ARI appears in exactly one place in the specification corpus — `glossary/GLOSSARY.md:27-28` — which defers to the implementation: *"A deterministic measurement value computed by RI-PY using integer arithmetic."* |
| APS-001 §2 (Determinism by Design) | **TODO** — `compliance/TRACEABILITY_MATRIX.md` |
| APS-001 §5 (Policy determinism) | **TODO** |
| APS-001 §8 (Fail Closed, source of INV-008) | **TODO** |
| Conformance fixtures FIX-001, FIX-ERROR | **TODO** |
| Verification status of every INV row | **NOT VERIFIED / NOT VERIFIED** |
| Numeric representation (AD-CA-007) | **UNRESOLVED**, candidates non-binding |
| Integer-division semantics | **Not present in any register**, not even as a candidate |
| SPEC-002 | **v0.3-DRAFT**, header: *"Normative effect: NONE until APPROVED."* |

Consequently **no finding in this document can be remediated by writing code**, because for
each one the question *"remediated to what?"* has no answer in normative material. The
implementation's current behaviour is implementation evidence, not the target.

**Verdict distribution:**

| Terminal verdict | Count | Findings |
|---|:--:|---|
| SPECIFICATION CHANGE REQUIRED | 2 | CORE-P0-001, CORE-P1-004 |
| ARCHITECTURAL DECISION REQUIRED | 3 | CORE-P0-002, CORE-P0/P1-003, CORE-P1-005 |
| GOVERNANCE DECISION REQUIRED | 1 | CORE-P1-006 |
| SAFE TO CHARACTERIZE (in parallel, all six) | 6 | see §9 |

**Single most consequential observation.** The one finding that is cheapest to fix —
CORE-P1-006, the determinism CI blind spot — is the one whose absence *conceals the other
five*. The cross-platform determinism job computes no ARI (§5.6). Until it does, no
remediation of the other five can be verified to have worked.

---

## §2 Scope

**In scope:** the six findings enumerated in the task, assessed for reproduction,
location, impact, activity, specification coverage, decision dependency and minimal next
step, within `aura-poc-a-core-v3.3` @ `9c6a5d8`.

**Out of scope and untouched:** `core/`, `compliance/`, `audit/`, CI workflows, SPEC-002,
APS documents, governance documents, ADRs, Constitution Artifact / Vector, CR-007.

**Method constraint applied throughout.** Where the implementation behaves in a given way,
that is recorded as **implementation evidence**. It is never read as a normative decision,
a requirement, or a target state. Where existing implementation documentation states a
range or a rule, it is cited as *documentation of the implementation*, not as
specification — with one consequence made explicit in §7: several "documented" values
have no normative source at all.

---

## §3 Evidence Sources

### 3.1 Sources requested by the task that DO NOT EXIST

| Requested source | State |
|---|---|
| `review/2026-08-11_SPEC-002_ARCH_REVIEW/` | **DOES NOT EXIST.** `review/` contains exactly one directory: `2026-08-11_ENGINEERING_BASELINE`. Verified by `ls review/`. |
| SPEC-002 **v0.4 draft** | **DOES NOT EXIST.** The only SPEC-002 in any inspected repository is `v0.3-DRAFT` (`specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:4`). Exhaustive search for `v0.4` returns one unrelated hit: `ROADMAP.md:53`, a repository release milestone. |

Neither was substituted, reconstructed, or inferred. Findings that would have depended on
them are marked accordingly.

### 3.2 Sources used

| Ref | Source |
|---|---|
| ENG-BASE | `review/2026-08-11_ENGINEERING_BASELINE/` — `01`–`10`, incl. `04_DETERMINISM_AUDIT.md`, `05_TEST_MATRIX.md`, `08_BLOCKERS.md` |
| NB-021 | `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md` |
| BRIEFS | `BRIEF_DR-002.md`, `BRIEF_NB-021.md`, `SAFE_ENGINEERING_WORK.md` |
| CORE | `aura-poc-a-core-v3.3` @ `9c6a5d8` — source read + executed reproduction |
| SPEC-002 | `AuraIDToken/aura-specification` · `specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` v0.3-DRAFT |
| APS-100 | `aps/APS-100_PROTOCOL_INVARIANTS.md` v1.0-DRAFT — INV-001…015 |
| INV-REG | `invariants/INVARIANT_REGISTRY.md` |
| TRACE | `compliance/TRACEABILITY_MATRIX.md` |
| GLOSS | `glossary/GLOSSARY.md` |
| RI-PY | `reference/RI-PY_AURA_POC_A_CORE.md` — APS-950 status: **NOT CERTIFIED** |

### 3.3 Reproduction environment

CPython 3.11.15, Linux x86_64. Docker **unavailable** — CHECK 7/8/9 and both DB-gated test
classes were not executed and are reported as *not executed*, never as passing or failing.

---

## §4 Finding Inventory

| ID | Finding | Location | Status | Severity |
|---|---|---|---|---|
| **CORE-P0-001** | `zip()` truncation — mismatched vector lengths silently truncate and yield maximum similarity | `core/evaluator.py:41`; `compliance/consistency.py:96` | **CONFIRMED · ACTIVE · SPEC-BLOCKED** | P0 |
| **CORE-P0-002** | Integer-division semantics — Python `//` floors; Rust/C/JS truncate toward zero | `core/evaluator.py:47`, `:83-84`; `compliance/consistency.py:59-61`, `:97` | **CONFIRMED · LATENT · DECISION-BLOCKED** | P0 |
| **CORE-P0/P1-003** | Rounding semantics — Python `round()` is half-to-even; Rust/C/JS are not | `core/offline_normalizer.py:88` | **CONFIRMED · LATENT · DECISION-BLOCKED** | P0/P1 |
| **CORE-P1-004** | ARI range — implementation produces values far above the documented maximum | `core/evaluator.py:78-81` | **CONFIRMED · ACTIVE · SPEC-BLOCKED** | P1 |
| **CORE-P1-005** | Divergent ARI engines — two implementations, different validation, clamping and penalty models | `core/evaluator.py` + `compliance/evaluator_wrapper.py` vs `compliance/consistency.py` | **CONFIRMED · ACTIVE · DECISION-BLOCKED** | P1 |
| **CORE-P1-006** | Determinism CI blind spot — cross-platform job executes no ARI computation | `scripts/generate_determinism_report.py:36-38`; `.github/workflows/execution-checks.yml` | **CONFIRMED · ACTIVE · GOVERNANCE-BLOCKED** | P1 |

No finding is marked FIXED, RESOLVED, COMPLIANT or SAFE. No evidence supporting any of
those labels was found for any item.

---

## §5 Reproduction Evidence

All results below were executed in this session against the unmodified working tree.

### §5.1 CORE-P0-001 — `zip()` truncation

**Input / claimed behaviour.** `core/evaluator.py:32-38` documents the parameters as
*"Pre-normalized int32 vectors (scaled by 10^5)"* and the return as *"range approximately
[-10^5, 10^5]"*. `CONSTITUTION_DIM = 1536` is enforced at `core/offline_normalizer.py:171`
and referenced **nowhere** in either evaluation engine.

**Actual behaviour.**

| Constitution dim | Agent vector dim | Similarity returned | Exception |
|---:|---:|---:|---|
| 4 | 2 | `100000` (maximum) | none |
| 4 | 6 | `100000` (maximum) | none |
| **1536** | **1** | **`100000`** (maximum) | none |

Full evaluation with a 2-element vector against a 4-element constitution:
`evaluate(...) → {'ari': 100000, 'drift': 0}` — a **perfect score**.

`ConsistencyCalculator` behaves identically:
`calculate({... "embedding": [100000, 0] ...}) → {'score': 100000, 'semantic': 100000, 'penalty': 0}`.

**Reproduction.** Construct `PoCAEvaluator` with a constitution of length *n*; call
`vector_similarity_int32` with a vector of length *m ≠ n* whose leading elements align.
No length comparison exists in either engine.

**Direction of the failure.** Fail-**open**: malformed input yields the most favourable
possible measurement. A 1-element vector scores identically to a correct 1536-element one.

### §5.2 CORE-P0-002 — integer-division semantics

**Input.** Negative dot product at the rescale step `dot // SCALING_FACTOR`.

| `dot` | Python `//` | Rust / C / JS truncation | Δ |
|---:|---:|---:|---:|
| −1 | **−1** | 0 | −1 |
| −99 999 | **−1** | 0 | −1 |
| −100 000 | −1 | −1 | 0 |
| −100 001 | **−2** | −1 | −1 |
| −150 000 | **−2** | −1 | −1 |

**ARI consequence.** Anti-aligned unit vectors, `valid_schema = True`:

| | Python (actual) | Truncating port (computed) |
|---|---|---|
| `SA` | −1 | 0 |
| `evaluate()` | `{'ari': 29999, 'drift': 100001}` | `{'ari': 30000, 'drift': 100000}` |

The 1-LSB divergence propagates into both outputs. Divergence occurs whenever the dot
product is negative and not an exact multiple of 100 000.

**No semantics selected.** Which rule is correct is not determined here.

### §5.3 CORE-P0/P1-003 — rounding semantics

**Entry point — exactly one site.** `core/offline_normalizer.py:88`:
`int_vector = [round(x * SCALING_FACTOR) for x in normalized_vector]`.
Reached from `normalize_constitution_vector()` (`:181`) and therefore from
`generate_sample_constitution()` (`:227`) — i.e. **this is the Constitution Vector
construction path**. A second, test-only occurrence exists at `core/test_ari.py:25`.

**Actual behaviour.**

| | 0.5 | 1.5 | 2.5 | 3.5 |
|---|---:|---:|---:|---:|
| Python `round()` (half-to-even) | **0** | 2 | **2** | 4 |
| Rust `f64::round` / C `round` (half-away-from-zero) | 1 | 2 | 3 | 4 |
| JS `Math.round` (half toward +∞) | 1 | 2 | 3 | 4 |

Applied at the scaling site:

| Input | Python (actual) | Rust (computed) | JS (computed) |
|---|---|---|---|
| `[5e-6, 1.5e-5, 2.5e-5, 3.5e-5]` | `[0, 2, 2, 3]` | `[1, 2, 3, 4]` | `[1, 2, 3, 4]` |
| negated | `[0, -2, -2, -3]` | `[-1, -2, -3, -4]` | `[0, -1, -2, -3]` |

**Three different Constitution Vectors from one input.** Since `ari_vector_hash` in the CI
determinism report is a hash of this output, the CI vector is itself rounding-dependent.

**No semantics selected.**

### §5.4 CORE-P1-004 — ARI range

**Claimed range.** `core/evaluator.py` docstrings and `docs/mathematical_foundation.md`
state `[0, 100000]`. §7 records that **no normative source defines this range**.

**Actual behaviour** (`valid_schema = True`):

| Input | Result | Ratio to claimed max |
|---|---|---:|
| 4 × `[100000]` vs 4 × `[100000]` | `{'ari': 310000, 'drift': 0}` | **3.1×** |
| 1536 × `[100000]` vs 1536 × `[100000]` | `{'ari': 107550000, 'drift': 0}` | **1075×** |
| anti-aligned | `{'ari': 0, 'drift': 200000}` | drift **2×** its documented `[0,100000]` |

**Where the value arises.** `core/evaluator.py:78-80` computes
`raw_ari = (30000*si)//100000 + (70000*sa)//100000`, then line 81 applies `max(0, …)` —
a **lower** clamp only. No upper clamp exists. The value is unbounded above because `sa`
is unbounded above, because no normalization check exists (CORE-P0-001 / D6 of ENG-BASE).

**Downstream.** `compliance/certificate.py` divides by 100 000 for presentation, so an
out-of-range value surfaces as e.g. `ari.score = 1075.5` on a field documented as a
`[0.0, 1.0]` ratio. `init.sql:47` constrains `RAW_ARI` to `BETWEEN 0 AND 100000` — but no
application code writes to that table, so the constraint is never reached.

### §5.5 CORE-P1-005 — divergent ARI engines

**Two engines exist.** Enumerated exhaustively:

| | Engine A | Engine B |
|---|---|---|
| Entry point | `core.evaluator.PoCAEvaluator.evaluate` + `compliance.evaluator_wrapper.evaluate_with_policy` | `compliance.consistency.ConsistencyCalculator.calculate` |
| Input | `(agent_id, vector: List[int], valid_schema: bool)` | `event: Dict` with `timestamp`, `embedding`, `content` |
| Structural term | `100000 if valid_schema else 0` (caller-asserted) | `100000 if required keys present else 0` (self-determined) |
| Semantic term | `dot // 100000` | `dot // 100000` |
| Formula | `30000*SI//1e5 + 70000*SA//1e5` | `30000*S//1e5 + 70000*SA//1e5 − penalty` |
| **Penalty model** | `DRIFT_PENALTY = 150000` if `SA < 68000` (`compliance/policy.py:20-21,39`) | `VIOLATION_PENALTY = 10000` × violation count (`compliance/consistency.py:24,99`) |
| Magnitude validation | **none** | `ValueError` if any `abs(v) > 100000` (`:85`,`:88`) |
| Zero-vector guard | none | returns `0` (`:82`) |
| Length validation | **none** | **none** |
| Upper clamp | **none** | `min(100000, …)` (`:62`) |
| Halt semantics | raises `Exception("POLICY_HALT")` | returns `{"status": "HALTED"}` |
| Output shape | `{ari, drift}` | `{score, structural, semantic, penalty, halted}` |

**Reproduced divergence.** Identical normalized input `[60000, 80000, 0, 0]` (magnitude
exactly 100 000) against an identical constitution:

- Engine A → `{'ari': 100000, 'drift': 0}`
- Engine B → `{'score': 100000, 'structural': 100000, 'semantic': 100000, 'penalty': 0}`

They agree here. They diverge on out-of-contract input:

- `ConsistencyCalculator([200000,0,0,0], …)` → **raises** `ValueError`
- `PoCAEvaluator([200000,0,0,0]).evaluate(…)` → **returns** `{'ari': 170000, 'drift': 0}`

**Penalty models are not reconcilable.** `150000` (threshold-triggered) versus
`10000 × count` are different units of a different quantity. Note additionally that
`DRIFT_PENALTY = 150000` exceeds the maximum possible in-range `RAW_ARI` of `100000`, so
under Engine A any drift penalty floors ARI to 0 regardless of measurement.

**No engine is designated correct here.** `docs/GAP-001.md` GAP-C5 records this as
*"LARGELY RESOLVED"*; the reproduction above shows it is not.

### §5.6 CORE-P1-006 — determinism CI blind spot

**Claim under test.** That the cross-platform determinism job verifies ARI reproducibility.

**Actual state — three independent confirmations:**

1. **Import graph.** `scripts/generate_determinism_report.py:36-38` imports exactly three
   modules: `core.offline_normalizer`, `audit.merkle`, `audit.signing`. **`core.evaluator`
   is not imported.**
2. **`ari_vector_hash` computes no ARI.** `scripts/generate_determinism_report.py:82-83`:
   `constitution = generate_sample_constitution()` then
   `ari_vector_hash = _hash_int32_array(constitution[:1000])`. The hashed object is the
   **constitution vector**, i.e. offline-normalizer output. The name is misleading; no ARI
   value is computed anywhere in the report.
3. **Executed-file survey.** Of the files CI runs, only `scripts/check_cr003_layer_boundary.py`
   references the evaluator — and it does so via `ast.parse` (`:134`), i.e. **static parsing,
   never execution**.

**Which CI step executes `PoCAEvaluator.evaluate` at all?** Exactly one: CHECK 8 →
`core.test_cr003_statelessness` (`scripts/checks/check_8_cr003_statelessness.sh:16`). It is
**Docker-gated** (not executed in this environment) and asserts only
`result_A == result_B` — history independence. That assertion holds under *any* division
or rounding semantics, so it cannot detect CORE-P0-002 or CORE-P0/P1-003.

**Which suites do assert ARI values?** `core/test_ari.py` and `core/test_integration.py`.
Neither is invoked by any CI step: `run_all_checks.sh` invokes `unittest` exactly three
times — `core.test_bitwise_replay` (CHECK 1), `audit.test_audit_db_integration` (CHECK 7),
`core.test_cr003_statelessness` (CHECK 8).

**Conclusion.** The cross-platform comparison (`compare-determinism` job) compares five
hashes covering the offline normalizer, SHA-256, Merkle and HMAC. **Evaluator arithmetic
has zero cross-platform coverage.** The subsystem where CORE-P0-001 … CORE-P1-005 live is
precisely the subsystem the determinism pipeline does not observe.

---

## §6 Determinism Impact

| Finding | Cross-platform | Bit-level | Hash-level | ARI-level | Artifact-level |
|---|---|---|---|---|---|
| **P0-001** `zip()` | no — identical in every language | no | no | **YES** — max score from malformed input | **YES** if the result reaches a certificate/DB |
| **P0-002** division | **YES** — Python vs Rust/C/JS | **YES** — 1 LSB | indirect — only if ARI is hashed (it is not, §5.6) | **YES** — `ari` and `drift` differ by 1 | **YES** for any future cross-language artifact |
| **P0/P1-003** rounding | **YES** — three distinct results | **YES** | **YES** — `ari_vector_hash` is a hash of this output | indirect — via the constitution vector | **YES** — the Constitution Vector itself differs |
| **P1-004** ARI range | no — deterministic in Python | no | no | **YES** — value exceeds documented range by up to 1075× | **YES** — `DECIMAL(3,2)` / `[0,100000]` CHECK would reject at persistence |
| **P1-005** engines | no | no | no | **YES** — same input, two contracts | **YES** — different output shapes |
| **P1-006** CI gap | **YES** — it is the absence of cross-platform observation | n/a | n/a | n/a | n/a |

**Ordering consequence.** CORE-P0/P1-003 is the only finding that changes the Constitution
Vector itself, and therefore the only one that changes a hash CI already compares. It is
also the finding whose decision (AD-CA-007) is furthest upstream.

---

## §7 Specification Traceability

| Finding | SPEC-002 requirement | INV | AD-CA | ADR | Result |
|---|---|---|---|---|---|
| **P0-001** | REQ-002-031 (failure conditions) — *v0.3-DRAFT, no normative effect* | **INV-008 Fail Closed (Critical)** | — | — | **UNRESOLVED** — see below |
| **P0-002** | REQ-002-014 (one numeric representation) | INV-001, INV-002, INV-006 | **AD-CA-007** — division rule **not listed even as a candidate** | — | **UNRESOLVED** |
| **P0/P1-003** | REQ-002-014, REQ-002-017…-022 | INV-001, INV-002, INV-003, INV-006 | **AD-CA-007** — `round-half-to-even` listed as **candidate only** | — | **UNRESOLVED** |
| **P1-004** | — | INV-001 | — | — | **UNRESOLVED** — no normative definition of ARI or its range exists |
| **P1-005** | — | INV-001, INV-013 | — | — | **UNRESOLVED** — no normative designation of an authoritative engine |
| **P1-006** | — | INV-002 Bit-Perfect Replay, INV-006 Platform Independence, **INV-010 Conformance Completeness** | — | — | **UNRESOLVED** |

### §7.1 The structural finding — the anchor is missing

**ARI is not normatively defined anywhere.** Exhaustive search of `aps/`, `specification/`,
`invariants/`, `constitution/`, `conformance/`, `glossary/` returns exactly one hit:

> `glossary/GLOSSARY.md:27-28` — **ARI** (Aura Reliability Index): *"A deterministic
> measurement value computed by RI-PY using integer arithmetic. ARI is a measurement, not a
> decision."*

The glossary defines ARI **by reference to the implementation**. No APS document specifies
its formula, its range, its dimension, its division rule, or its rounding rule.

**Every relevant invariant traces to a section that does not exist.** From
`compliance/TRACEABILITY_MATRIX.md`:

| Principle | Source | INV | Fixture | Status |
|---|---|---|---|---|
| Determinism by Design | **APS-001 §2 (TODO)** | INV-006 | FIX-001 (TODO) | NOT VERIFIED |
| Determinism by Design | **APS-001 §2 (TODO)** | INV-007 | TODO | NOT VERIFIED |
| **Fail Closed by Default** | **APS-001 §8 (TODO)** | **INV-008** | **FIX-ERROR (TODO)** | **NOT VERIFIED** |
| Determinism by Design | **APS-001 §5 (TODO)** | INV-013 | TODO | NOT VERIFIED |

**Consequence for CORE-P0-001 specifically.** INV-008 is a Critical invariant requiring
that *"In case of error, an implementation MUST terminate execution in a safe state"*
(`invariants/INVARIANT_REGISTRY.md:186`). But:

- APS-001 §8, its normative source, is **TODO**;
- what constitutes "an error" is undefined — nothing states that a dimension mismatch is one;
- CONF-007, its conformance test, is **DRAFT**;
- FIX-ERROR, its fixture, is **TODO**;
- its verification status is **NOT VERIFIED**.

`reference/RI-PY_AURA_POC_A_CORE.md:55` records INV-008 as ✅ with evidence *"ARI=0 circuit
breaker"*. The reproduction in §5.1 shows a malformed vector yields **ARI = 100000**, not 0.
That ✅ is not supported by the implementation's behaviour on this input class.

**No normative statement is created here.** This section records that the anchors are
absent, which is why five of six findings cannot be remediated by engineering alone.

---

## §8 Governance Traceability (NB-021 gate)

NB-021 verdict, unchanged and not reopened: **INDETERMINATE**; engineering code changes to
`aura-poc-a-core-v3.3` are **BLOCKED pending governance clarification**.

| Finding | Covered by NB-021? | Applicable NB-021 case | Effect |
|---|---|---|---|
| P0-001 | **YES** | CASE C (correctness defect, spec unchanged) | code fix BLOCKED; characterization PERMITTED (CASE D) |
| P0-002 | **YES** | CASE C | as above |
| P0/P1-003 | **YES** | CASE C | as above |
| P1-004 | **YES** | CASE C | as above |
| P1-005 | **YES** | CASE C | as above |
| P1-006 | **YES** | **not covered by any case** | CI infrastructure is neither `core/` logic, documentation, nor tests → **INDETERMINATE** |

**Additional gate applying to every code fix**, independent of the above:
`ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §4.1 Gate 2 — *"Does this change preserve bit-identity?
… NO → REJECTED. UNCERTAIN → REJECTED."* Every remediation in this document changes output
for at least one input class and therefore does not preserve bit-identity.

**Identity gate.** `README.md` §11.4 — *"Bug fixes or modifications require a new lineage."*
Whether a corrected Core remains v3.3 is NB-021 question 4, unanswered; v3.3 has no bound
identity (no tag, no SHA, `[COMPUTED_AT_SEALING_v3.3]` unfilled).

---

## §9 Safe Engineering Work — A: SAFE NOW

Permitted by `CONSTITUTIONAL_DECREE.md` Art. VII (Testing / Documentation) and Art. III
items 4–5; NB-021 CASE A and CASE D. **None encodes a normative expected value.**

| ID | Work | Finding | Basis |
|---|---|---|---|
| SW-1 | Characterization test: mismatched vector lengths → record maximum-similarity result, both engines | P0-001 | CASE D |
| SW-2 | Characterization test: negative dot product → record exact `SA`, `ari`, `drift`, with an in-test note that the value is language-dependent and unresolved | P0-002 | CASE D |
| SW-3 | Characterization test: `round()` at ±`.5` boundaries → record `[0,2,2,3]` / `[0,-2,-2,-3]`, labelled candidate-only per AD-CA-007 | P0/P1-003 | CASE D |
| SW-4 | Characterization test: `ari` and `drift` upper bounds → record `310000`, `107550000`, `200000` | P1-004 | CASE D |
| SW-5 | Differential test: identical input into both engines; record agreement in-contract and divergence out-of-contract | P1-005 | CASE D |
| SW-6 | Characterization test: assert the determinism report's import set, pinning that `core.evaluator` is absent | P1-006 | CASE D |
| SW-7 | Document the six findings as `KL-00x` entries in `docs/KNOWN_LIMITATIONS.md`, each stating that the correct behaviour is unresolved | all | CASE A |
| SW-8 | Correct `docs/GAP-001.md` GAP-C5 from *"LARGELY RESOLVED"* to the reproduced state | P1-005 | CASE A |
| SW-9 | Record that `ari_vector_hash` hashes the constitution vector, not an ARI | P1-006 | CASE A |
| SW-10 | Record that `RI-PY` INV-008 ✅ is not supported for the malformed-input class (§7.1) — as an observation, without changing the RI-PY document | P0-001 | CASE A |

**Mandatory framing for SW-1…SW-6.** Each test must be named and documented as
*characterization*, must state **CURRENT BEHAVIOUR ≠ NORMATIVE REQUIREMENT**, and must not
be cited as evidence of correctness. This is the pattern already established and executed in
`GUARD-G1_CHARACTERIZATION_TESTS.rs`.

**Explicitly NOT safe**, despite superficial similarity: adding a length check, a bounds
check, an upper clamp, an exception, or any validation *response*; unifying the two engines;
changing CI; annotating `core/` with `float` in any position (`check_2_integer_only.sh` is a
plain grep and would fail).

---

## §10 Decision-Blocked Work — B: DECISION REQUIRED

| ID | Work | Blocked by | Finding |
|---|---|---|---|
| DB-1 | Select integer-division semantics for negative dividends | **not in any register** — AD-CA-007 lists no division candidate | P0-002 |
| DB-2 | Select rounding semantics at float→int reduction | AD-CA-007, UNRESOLVED, candidates non-binding | P0/P1-003 |
| DB-3 | Designate the authoritative ARI engine | no normative designation exists | P1-005 |
| DB-4 | Reconcile or select a penalty model (`150000` threshold vs `10000 × count`) | as above | P1-005 |
| DB-5 | Define the required response to malformed input (raise / sentinel / reject upstream) | REQ-002-031, v0.3-DRAFT with no normative effect | P0-001 |
| DB-6 | Define the ARI value range and its enforcement point | no normative definition of ARI exists | P1-004 |
| DB-7 | Define the numeric representation (width, scale, endianness, dimension) | AD-CA-007 | P0-002, P0/P1-003, P1-004 |

---

## §11 Governance-Blocked Work — C: GOVERNANCE BLOCKED

| ID | Work | Blocked by |
|---|---|---|
| GB-1 | Any code change to `core/` or `compliance/` implementing DB-1…DB-7 | NB-021 INDETERMINATE; Gate 2 (bit-identity); README §11.4 (new lineage) |
| GB-2 | Extending the determinism report to compute ARI | NB-021 — CI infrastructure not covered by any Decree Art. III category |
| GB-3 | Adding a CI step that runs `core/test_ari.py` and `core/test_integration.py` | as GB-2 |
| GB-4 | Any change altering `chain`-equivalent hash inputs or the Constitution Vector | AD-CA-007 / AD-CA-008 **and** NB-021 |
| GB-5 | Declaring any finding remediated, conformant, or verified | requires evidence that does not exist; INV rows are NOT VERIFIED |

**GB-2 is the cheapest unblock in this document.** It requires a single scoping ruling —
whether CI infrastructure falls inside the FROZEN boundary — not a resolution of NB-021.

---

## §12 Required Decisions

**No decision is made here.** Each entry states the question, why it is required, what it
depends on, and what it unblocks.

### RD-1 — Does the specification define ARI, or does ARI remain implementation-defined?

- **WHY REQUIRED:** ARI exists normatively only as a glossary entry deferring to RI-PY
  (§7.1). Without a normative definition there is no target state for P1-004 or P1-005, and
  "correct" is unanswerable.
- **DEPENDENCIES:** none — this is upstream of everything else in this document.
- **IMPACT:** unblocks DB-3, DB-4, DB-6; determines whether APS-001 must gain an ARI section.

### RD-2 — Is APS-001 §2 / §5 / §8 authored, and does INV-008 apply to dimension mismatch?

- **WHY REQUIRED:** INV-008 is Critical but its source section is TODO, its fixture is TODO,
  its conformance test is DRAFT, and its trigger condition is undefined (§7.1).
- **DEPENDENCIES:** RD-1 for the ARI-specific portion.
- **IMPACT:** unblocks DB-5; determines whether P0-001 is an invariant violation or an
  unspecified behaviour.

### RD-3 — AD-CA-007: numeric representation, including rounding **and division**

- **WHY REQUIRED:** rounding is listed as candidate-only; division is not listed at all.
  Both are cross-language divergences (§5.2, §5.3).
- **DEPENDENCIES:** governance process for advancing SPEC-002 beyond DRAFT.
- **IMPACT:** unblocks DB-1, DB-2, DB-7; determines the Constitution Vector's byte identity.

### RD-4 — Which ARI engine is authoritative, and which penalty model applies?

- **WHY REQUIRED:** two engines with incompatible validation, clamping and penalty
  semantics both execute today (§5.5).
- **DEPENDENCIES:** RD-1.
- **IMPACT:** unblocks DB-3, DB-4.

### RD-5 — NB-021: does the FROZEN boundary permit non-normative defect correction?

- **WHY REQUIRED:** every code change in §10 is gated by it; NB-021 is INDETERMINATE.
- **DEPENDENCIES:** none.
- **IMPACT:** unblocks GB-1, GB-4.

### RD-6 — Does CI infrastructure fall inside the FROZEN boundary?

- **WHY REQUIRED:** the determinism blind spot (§5.6) conceals the other five findings, and
  closing it is not covered by any permitted-change category.
- **DEPENDENCIES:** none — narrower than RD-5 and answerable independently.
- **IMPACT:** unblocks GB-2, GB-3. **Lowest cost, highest leverage.**

---

## §13 Test Plan

Separated by class. Only the first class is executable before decisions.

### 13.1 Characterization tests — available now

SW-1 … SW-6 (§9). Purpose: convert every finding into a recorded, executable fact.
Constraint: no normative expected value; explicit CURRENT ≠ NORMATIVE labelling.
Precedent: `GUARD-G1_CHARACTERIZATION_TESTS.rs`, 8/8 executed.

### 13.2 Regression tests — after RD-1 … RD-4

For each finding: the characterization test is **replaced**, not deleted, by an assertion of
the decided behaviour, with the authorizing decision cited in the test. Required coverage:
length mismatch, negative-dividend division, `.5` boundaries both signs, ARI upper bound,
single-engine equivalence, penalty model.

### 13.3 Conformance tests — after RD-2, and after CONF-001…010 leave DRAFT

`APS-400` is `1.0-DRAFT`; all ten CONF tests are DRAFT; `CONF-001 §3` carries an inline
*"TODO: Specify exact preconditions once APS-200 schemas and APS-500 fixtures are
finalized."* FIX-001 and FIX-ERROR are TODO. No conformance test can be authored before
these exist — attempting one would encode an unapproved value (NB-021 CASE E, the one
unanimous prohibition).

### 13.4 Cross-platform tests — after RD-3 and RD-6

Extend the determinism report to compute ARI over fixed inputs and compare x86_64 vs arm64.
**This is the test that would have caught P0-002 and P0/P1-003.** Blocked by RD-6
(scope) and RD-3 (what value is expected). Note: it can be built as
characterization-labelled and normatively neutral — the design constraint is recorded in
`09_SAFE_WORK.md` §2 (S-20).

### 13.5 Independent implementation tests — after RD-1, RD-3, and SPEC-002 approval

The Independent Implementer Test (`SPEC-002 §10`) requires that an independent implementer
using only approved documents derive exactly one canonical result. This is the terminal
verification and is unreachable while SPEC-002 is DRAFT with twelve unresolved decisions.
Prerequisite: a defined byte encoding, division rule, rounding rule and dimension — i.e.
RD-3 in full.

---

## §14 Exit Criteria — what must be true before remediation may begin

Remediation of Core may begin when **all** of the following hold. None holds today.

| # | Criterion | Current state |
|---|---|---|
| **EC-1** | NB-021 answered: the FROZEN boundary's effect on defect correction is determined | **NOT MET** — INDETERMINATE |
| **EC-2** | A normative definition of ARI exists (formula, range, dimension) — or an explicit ruling that ARI remains implementation-defined and is therefore not remediable against a spec | **NOT MET** — glossary entry only, deferring to RI-PY |
| **EC-3** | AD-CA-007 resolved for **both** rounding and division | **NOT MET** — rounding is candidate-only; division is unlisted |
| **EC-4** | The required response to malformed input is defined (APS-001 §8 authored; INV-008 trigger condition stated) | **NOT MET** — §8 TODO, CONF-007 DRAFT, FIX-ERROR TODO |
| **EC-5** | An authoritative ARI engine and penalty model are designated | **NOT MET** |
| **EC-6** | ARI computation is observed by cross-platform CI, so that a remediation can be verified to have worked | **NOT MET** — evaluator not imported by the determinism report |
| **EC-7** | Characterization tests exist for all six findings, so that any behaviour change is visible | **NOT MET** — none written (SW-1…SW-6 available now) |
| **EC-8** | The identity consequence of a corrected Core is determined (same lineage or new) | **NOT MET** — NB-021 Q4; v3.3 has no bound identity |
| **EC-9** | Authorization is recorded per `Decree Art. X` ("Custodian Signature: [Required for core/ changes]") and `AGENTS.md` rule 13 | **NOT MET** |

**EC-6 and EC-7 are the only two achievable without a governance or specification decision**
— EC-7 entirely (§9), EC-6 after the single scoping ruling RD-6.

---

## Per-Finding Terminal Verdicts

| Finding | Verdict | Minimal next step |
|---|---|---|
| **CORE-P0-001** `zip()` truncation | **SPECIFICATION CHANGE REQUIRED** — APS-001 §8 is TODO; INV-008's trigger condition is undefined; CONF-007 DRAFT; FIX-ERROR TODO | SW-1 now; then RD-2 |
| **CORE-P0-002** division semantics | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-007 does not list a division rule even as a candidate | SW-2 now; then RD-3 |
| **CORE-P0/P1-003** rounding semantics | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-007 UNRESOLVED, `round-half-to-even` candidate-only | SW-3 now; then RD-3 |
| **CORE-P1-004** ARI range | **SPECIFICATION CHANGE REQUIRED** — no normative definition of ARI or its range exists | SW-4 now; then RD-1 |
| **CORE-P1-005** divergent engines | **ARCHITECTURAL DECISION REQUIRED** — no normative designation of an authoritative engine or penalty model | SW-5 now; then RD-4 |
| **CORE-P1-006** CI blind spot | **GOVERNANCE DECISION REQUIRED** — CI scope relative to the FROZEN boundary is undetermined | SW-6 now; then RD-6 |

Every finding is additionally **SAFE TO CHARACTERIZE** now, via SW-1 … SW-6.

---

*This document has no normative effect. It makes no decision, creates no ADR, changes no
specification, and modifies no code or CI. It records readiness only.*
