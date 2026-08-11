# RD-006 — ARI OBSERVABILITY

**Date:** 2026-08-11
**Scope executed:** RD-6 as scoped by the task — minimal, non-normative observability of the
real ARI computation.
**Normative effect:** NONE.

> **Scope note, stated up front.** In `05_CORE_REMEDIATION_READINESS.md`, RD-6 is a
> **decision question** — *"Does CI infrastructure fall inside the FROZEN boundary?"* — and
> the work it unblocks is GB-2/GB-3 (wiring ARI into CI). That decision has **not** been
> answered, and this document does not answer it.
>
> What was executed here is the portion that is already permitted without it: a
> **characterization test harness** (NB-021 CASE D; `CONSTITUTIONAL_DECREE.md` Art. VII
> Testing), listed as SW-6 in `05_CORE_REMEDIATION_READINESS.md` §9. The remaining step —
> CI wiring — was **not performed** and is reported as still blocked in §7.

---

## §1 Objective

Make the real ARI computation observable and machine-readable, so that a future
cross-architecture comparison has something to compare, **without**:

- defining ARI,
- fixing ARI,
- selecting among competing ARI implementations,
- selecting division, rounding, normalization or vector-length semantics,
- changing any expected value that a specification defines (none exists),
- changing SPEC-002, the Constitution, ADRs, RI-PY, invariants, or CI policy.

**Problem addressed (CORE-P1-006).** `scripts/generate_determinism_report.py:36-38` imports
exactly three modules — `core.offline_normalizer`, `audit.merkle`, `audit.signing` — and
does **not** import `core.evaluator`. Its `ari_vector_hash` vector hashes the *constitution
vector*, not an ARI. The cross-platform determinism job therefore observes **zero** ARI
arithmetic. This harness is the minimal observation point that changes that.

---

## §2 Scope

**In scope and done:** one new characterization test module executing the real
`core.evaluator.PoCAEvaluator` on five fixed inputs, emitting a machine-readable observation
record with runtime identity, plus four control tests proving the harness genuinely invokes
the evaluator.

**In scope and deliberately NOT done:** wiring the harness into `run_all_checks.sh` or
`.github/workflows/execution-checks.yml` (§7).

**Out of scope, untouched:** `core/evaluator.py`, `core/offline_normalizer.py`,
`compliance/`, `audit/`, `scripts/`, all workflows, SPEC-002, Constitution, ADRs, RI-PY,
invariants, `docs/`.

**Findings NOT remediated:** CORE-P0-001, CORE-P0-002, CORE-P0/P1-003, CORE-P1-004,
CORE-P1-005. None was fixed, mitigated, or worked around. OBS-5 deliberately *observes*
the CORE-P0-002 divergence without resolving it.

---

## §3 Existing Path

The minimal existing place where the real evaluator can be executed observably.

**Surveyed candidates:**

| Candidate | Executes evaluator? | Observable? | Verdict |
|---|---|---|---|
| `scripts/generate_determinism_report.py` | no — imports 3 modules, none is the evaluator | yes, emits JSON + CI artifact | **modifying it is GB-2** |
| `core/test_bitwise_replay.py` (CHECK 1) | no — never imports `PoCAEvaluator` | yes, runs in CI both architectures | modifying an existing CI-executed check |
| `core/test_ari.py` | **yes** | no — invoked by no CI step | closest existing execution path |
| `core/test_integration.py` | **yes** | no — invoked by no CI step | same |
| `core/test_cr003_statelessness.py` (CHECK 8) | **yes** | Docker-gated; asserts only `A == B` | passes under any division/rounding rule |
| `scripts/check_cr003_layer_boundary.py` (CHECK 9) | no — `ast.parse` only (`:134`) | static analysis | never executes the module |

**Chosen path.** A **new** module, `core/test_ari_observability.py`, alongside the existing
`core/test_ari.py`. Rationale:

- adding a test is expressly permitted (`CONSTITUTIONAL_DECREE.md` Art. VII, Art. III item 4);
- it modifies no existing file, so no existing check changes behaviour;
- `test_*.py` files are excluded from every Layer 0 scanner — CHECK 2, CHECK 3, CHECK 5, and
  CHECK 9 (`scripts/check_cr003_layer_boundary.py:165-166`: *"skip test_\*.py"*);
- precedent: `core/test_ari.py:10-11` already imports from `compliance/`, so a test module in
  `core/` importing across layers is established practice, not a new pattern.

---

## §4 Changed Files

| File | Change | Type |
|---|---|---|
| `core/test_ari_observability.py` | **added** (368 lines) | test / characterization harness |
| `review/2026-08-11_ENGINEERING_BASELINE/RD-006_ARI_OBSERVABILITY.md` | **added** | review documentation |

**Production code changed: NO.** `git diff` over all tracked files is empty; both entries
above are new files.

**Runtime artifact** (not committed): `artifacts/rd-006-ari-observation.json`, covered by
`.gitignore:46` (`artifacts/`) — verified with `git check-ignore -v`.

---

## §5 Characterization Semantics

The module states its own status in its docstring:

> "This is what the implementation produces today." — and NOT — "This is what Aura requires."

Concretely:

- Observed values live in a table named
  `IMPLEMENTATION_DERIVED_NON_NORMATIVE`, with an inline comment stating they are *"NOT a
  specification, NOT approved, and NOT a statement that the values are correct."*
- The emitted JSON record carries `"normative_effect": "NONE"` and
  `"status": "CHARACTERIZATION — IMPLEMENTATION-DERIVED / NON-NORMATIVE"`, and a test
  (`test_report_declares_non_normative_status`) fails if those markers are removed — so the
  disclaimer cannot be silently dropped from the artifact.
- **No canonical expected ARI was introduced.** No specification defines one: ARI occurs in
  the specification corpus only at `glossary/GLOSSARY.md:27-28`, which defines it *by
  reference to this implementation*. Every pinned value here was obtained by executing the
  code.
- **No fixture chooses between competing ARI implementations.** The harness observes exactly
  one engine — `core.evaluator.PoCAEvaluator` — and makes no claim about
  `compliance.consistency.ConsistencyCalculator` (CORE-P1-005). Neither is designated
  authoritative.
- Assertion failure messages instruct the reader that a change means the evaluation path
  changed, and that the constant must be replaced *deliberately, with the authorizing
  decision recorded* — never silenced.

---

## §6 Execution Evidence

```
$ python3 -m unittest core.test_ari_observability -v
Ran 8 tests in 0.107s
OK
```

### 6.1 Observation record

Runtime: `Linux / x86_64 / 64bit / CPython 3.11.15`

| Case | Input | Schema | Execution | **ARI** | **drift** | Touches |
|---|---|---|---|---:|---:|---|
| OBS-1 | aligned unit, dim 4 | valid | SUCCESS | **100000** | **0** | — |
| OBS-2 | orthogonal, dim 4 | valid | SUCCESS | **30000** | **100000** | — |
| OBS-3 | aligned unit, **dim 1536** | valid | SUCCESS | **100000** | **0** | — |
| OBS-4 | aligned unit, dim 4 | **invalid** | SUCCESS | **70000** | **0** | — |
| OBS-5 | anti-aligned, dim 4 | valid | SUCCESS | **29999** | **100001** | **CORE-P0-002** |

All five: `"evaluator": "core.evaluator.PoCAEvaluator"`, `"execution": "SUCCESS"`.

**All values are IMPLEMENTATION-DERIVED / NON-NORMATIVE.**

Full record at `artifacts/rd-006-ari-observation.json`, also printed to stdout so it appears
verbatim in any CI log that later runs the harness.

### 6.2 Control cases (the TEST REQUIREMENT)

Four controls prove the harness executes the evaluator rather than reading or hard-coding a
result:

| Control | Mechanism | Result |
|---|---|---|
| `test_control_observation_tracks_evaluator_internals` | patch `PoCAEvaluator.vector_similarity_int32` → `0`; observed ARI must move `100000 → 30000`, then recover when the patch lifts | **PASS** |
| `test_control_distinct_inputs_produce_distinct_observations` | aligned vs orthogonal must differ — proves it is not a constant emitter | **PASS** |
| `test_control_evaluator_failure_is_recorded_not_swallowed` | inject `RuntimeError`; harness must record `execution: FAILURE`, `observed: null` | **PASS** |
| `test_control_evaluator_is_the_real_module` | assert `__module__ == "core.evaluator"` and that `__init__.__code__.co_filename` resolves to `core/evaluator.py` — proves it is the production module, not a stub | **PASS** |

The first control is the decisive one: a harness that replayed or hard-coded a value would
report `100000` under the patch, and it reports `30000`.

### 6.3 Regression evidence

| Check | Before | After |
|---|---|---|
| CHECK 0 Constitutional Compliance | PASS | **PASS** |
| CHECK 1 Bit Identity | PASS | **PASS** |
| CHECK 2 Integer Only | PASS | **PASS** |
| CHECK 3 Layer Separation | PASS | **PASS** |
| CHECK 4 Audit Path | PASS | **PASS** |
| CHECK 5 Entropy | PASS | **PASS** |
| CHECK 6 Art.5 (DEFAULT / -O / -OO) | PASS ×3 | **PASS ×3** |
| CHECK 9 Layer Boundary (Python, no Docker needed) | PASS | **PASS** |
| CHECK 7 / CHECK 8 | not executed (no Docker) | not executed (no Docker) |
| Full suite `unittest discover` | 107 tests, 2 Docker errors | **115 tests, same 2 Docker errors** |

No check changed state. The 8 new tests are additive; the two pre-existing errors are the
unchanged Docker-unavailability failures.

---

## §7 CI Integration

**NOT ACHIEVED. Reported as blocked, not worked around.**

**Fact.** No current CI step would execute the harness. CI invokes `unittest` exactly three
times, each with an explicit module name:

```
scripts/checks/check_1_bit_identity.sh:19        python3 -m unittest core.test_bitwise_replay
scripts/checks/check_7_db_append_only.sh:14      python3 -m unittest audit.test_audit_db_integration
scripts/checks/check_8_cr003_statelessness.sh:16 python3 -m unittest core.test_cr003_statelessness
```

plus one `pytest` selector (`.github/workflows/execution-checks.yml:82`,
`core/test_bitwise_replay.py::WASMCompatibilityTest`). There is no discovery-based step. The
harness is therefore **inert in CI** until a CI file changes.

**Why it was not wired.** Changing `run_all_checks.sh` or the workflow is exactly GB-2/GB-3
in `05_CORE_REMEDIATION_READINESS.md` §11, and NB-021 classifies CI infrastructure as
**not covered by any permitted-change category** — neither `core/` logic, nor documentation,
nor tests. That is precisely the ruling RD-6 asks for. Wiring it here would be answering
RD-6 by action, which the task forbids ("bez zmiany polityki governance").

**Proposed change, NOT APPLIED**, recorded so the decision-maker can see its size — a single
check block appended to `scripts/run_all_checks.sh`:

```bash
# CHECK 10 — RD-006 ARI Observability (characterization; non-normative)
python3 -m unittest core.test_ari_observability -v
```

and one artifact path added to the existing upload list in
`.github/workflows/execution-checks.yml`:

```yaml
            artifacts/rd-006-ari-observation.json
```

Two lines. Neither was applied.

---

## §8 Cross-Platform Observation

**Prepared, not yet performed.**

The observation record carries the same runtime identity fields the existing determinism
report uses (`system`, `machine`, `architecture`, `python_version`, plus
`python_implementation`), so records from an x86_64 and an arm64 runner are directly
comparable once §7 is unblocked.

**Observed on this platform only:** `Linux / x86_64 / CPython 3.11.15`. No second
architecture was exercised; no cross-platform claim is made.

**What such a comparison would detect, once enabled:**

| Case | Would reveal |
|---|---|
| OBS-5 | **CORE-P0-002** — a truncating implementation yields `ari=30000, drift=100000` against this record's `29999 / 100001`. This is the single most valuable comparison in the set. |
| OBS-1…OBS-4 | ARI stability across architectures for well-formed input — currently unverified by anything |
| OBS-3 | behaviour at the documented dimension 1536, currently exercised by no CI step |

Two limits apply even after wiring: both existing CI legs run CPython, so an inter-*language*
divergence (CORE-P0-002, CORE-P0/P1-003) would **not** be detected by x86_64-vs-arm64 alone —
it needs an independent implementation (`05_CORE_REMEDIATION_READINESS.md` §13.5). And the
harness observes one engine, so CORE-P1-005 divergence remains unobserved.

---

## §9 Non-Normative Status

> **Observed ARI values are implementation evidence and do not constitute a normative
> definition of ARI.**

Supporting facts:

1. No specification defines ARI. The only occurrence in the specification corpus is
   `glossary/GLOSSARY.md:27-28`, which defines it as *"A deterministic measurement value
   computed by RI-PY"* — i.e. by reference to this implementation.
2. Every pinned value in the harness is labelled `IMPLEMENTATION-DERIVED /
   NON-NORMATIVE` in code, in the emitted artifact, and in this document.
3. The emitted artifact carries `"normative_effect": "NONE"`, enforced by a test.
4. Nothing here approves, ratifies, or freezes any value. Pinning a value records it; it
   does not authorize it.
5. If RD-1, RD-3 or RD-4 later define ARI, these tests are expected to fail and the constants
   are expected to be replaced deliberately, citing the authorizing decision.

This document creates no ADR, changes no specification, and makes no decision.

---

## §10 Limitations

1. **Not running in CI** (§7). The harness observes nothing automatically until GB-2/GB-3 is
   unblocked. EC-6 is therefore **not met**.
2. **One architecture observed.** No cross-platform comparison has occurred.
3. **One engine observed.** `ConsistencyCalculator` (CORE-P1-005) is not exercised;
   observing both would risk implying a comparison the corpus cannot adjudicate.
4. **Same-language only.** x86_64 vs arm64 under CPython cannot detect the cross-*language*
   divergences that CORE-P0-002 and CORE-P0/P1-003 actually concern.
5. **Well-formed inputs only** (plus one anti-aligned case). Mismatched-length input
   (CORE-P0-001) and out-of-range input (CORE-P1-004) are deliberately excluded: they belong
   to SW-1 and SW-4, and including them here would blur an observability harness into a
   defect characterization suite.
6. **Pinned values create maintenance coupling.** Any authorized change to the evaluation
   path will fail these tests. That is the intended signal, but it must not be resolved by
   editing the constant without recording why.
7. **Docker-gated checks unverified.** CHECK 7 and CHECK 8 were not executed in this
   environment, before or after.
8. **The harness is in `core/`.** It is excluded from every Layer 0 scanner by its `test_`
   prefix, and CHECK 9 was re-run to confirm — but the exclusion is by filename convention,
   not by directory, and that convention is what keeps it compliant.

---

## §11 Relationship to P0/P1 Findings

| Finding | Relationship | Remediated? |
|---|---|---|
| **CORE-P0-001** `zip()` truncation | Not exercised. All harness cases use matching dimensions. | **NO** |
| **CORE-P0-002** division semantics | **Observed** by OBS-5: `ari=29999, drift=100001`. Recorded as the value this implementation produces; a truncating implementation would produce `30000 / 100000`. Neither is designated correct. | **NO** |
| **CORE-P0/P1-003** rounding semantics | Not exercised. The harness supplies int32 vectors directly and never calls `offline_normalizer`, so the `round()` site is not on this path. | **NO** |
| **CORE-P1-004** ARI range | Partially visible: OBS-1/OBS-3 sit at exactly `100000`. Out-of-range inputs are excluded (Limitation 5), so the `310000` / `107550000` behaviour is not exercised here. | **NO** |
| **CORE-P1-005** divergent engines | Explicitly **not** addressed: one engine observed, neither designated authoritative. | **NO** |
| **CORE-P1-006** CI blind spot | **Partially addressed.** The observation capability now exists and executes; the CI wiring that would make it continuous does not (§7). | **PARTIAL** |

Everything the five other findings need remains as recorded in
`05_CORE_REMEDIATION_READINESS.md` §10–§12.

---

## §12 Exit Criteria

Against the nine criteria in `05_CORE_REMEDIATION_READINESS.md` §14:

| # | Criterion | Before | After |
|---|---|---|---|
| EC-1 | NB-021 answered | NOT MET | **NOT MET** |
| EC-2 | Normative definition of ARI exists | NOT MET | **NOT MET** |
| EC-3 | AD-CA-007 resolved (rounding **and** division) | NOT MET | **NOT MET** |
| EC-4 | Required response to malformed input defined | NOT MET | **NOT MET** |
| EC-5 | Authoritative ARI engine and penalty model designated | NOT MET | **NOT MET** |
| **EC-6** | **ARI computation observed by cross-platform CI** | NOT MET | **PARTIALLY MET** — the observation exists and executes; CI wiring and the second architecture remain outstanding |
| **EC-7** | **Characterization tests exist for the findings** | NOT MET | **ADVANCED** — SW-6 delivered; SW-1…SW-5 remain |
| EC-8 | Identity consequence of a corrected Core determined | NOT MET | **NOT MET** |
| EC-9 | Custodian authorization recorded | NOT MET | **NOT MET** |

### Exit criteria specific to RD-006

| # | Criterion | State |
|---|---|---|
| RD6-1 | A harness executes the real `core.evaluator` and records its output | **MET** |
| RD6-2 | The record includes input, evaluator, ARI, drift, runtime identity, success/failure | **MET** |
| RD6-3 | At least one control proves the harness executes rather than replays | **MET** — four controls |
| RD6-4 | No normative expected value introduced | **MET** |
| RD6-5 | No production code changed | **MET** |
| RD6-6 | The harness runs in CI | **NOT MET** — GB-2/GB-3, pending the RD-6 governance ruling |
| RD6-7 | Records compared across architectures | **NOT MET** — depends on RD6-6 |

**The remaining blocker is unchanged and is the ruling RD-6 asks for:** whether CI
infrastructure falls inside the FROZEN boundary. Until it is answered, the harness exists,
executes, and is inert.

---

*This document has no normative effect. It defines no ARI, selects no semantics, creates no
ADR, changes no specification, and modifies no production code.*
