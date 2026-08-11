# 09 — SAFE WORK NOW (TASK 9)

**Instruction honoured:** each candidate was verified against the current architecture
rather than assumed safe because it belongs to a normally-safe category. Several items
from the task's example list turned out **not** to be safe here; those are in §3.

**Safety test applied to every item:**

1. Does it change any value the system computes? → not safe.
2. Does it require choosing a protocol semantic? → not safe.
3. Does it encode an unresolved candidate answer in a fixture? → not safe.
4. Does it change a hash, a byte sequence, or a serialized format? → not safe.
5. Does it modify code inside a frozen/self-declared-frozen boundary? → needs approval
   even if otherwise harmless.

---

## 1. SAFE TO IMPLEMENT NOW

### 1.1 Characterization tests — the highest-value safe work

A characterization test records what the code **does today** without asserting that it is
**correct**. It creates no normative commitment, and it makes any future behaviour change
visible. This is the one category that is both entirely safe and directly useful to the
blocked decisions.

| # | Test to add | Records | Guard-rail |
|---|---|---|---|
| S-1 | Differing-length vectors into `vector_similarity_int32` and `ConsistencyCalculator._semantic_alignment` | that `zip` truncates and a 2-of-4 vector scores `100000` (D-3) | must be named/documented as *characterization*, not *specification* |
| S-2 | Negative dot product exact values | that `-1 // 100000 == -1` (D-1) | must state in the test that the value is language-dependent and unresolved (NB-009/NB-016) |
| S-3 | `round()` at `.5` boundaries, positive and negative | half-to-even output `[0, 2, 2]` / `[0, -2, -2]` (D-2) | **must not** be phrased as "correct rounding" — `AD-CA-007` lists this as a candidate only |
| S-4 | `drift` upper bound | measured `200000` and `100001`, contradicting the docstring (D-5) | none — pure fact |
| S-5 | `ari` upper bound for un-normalized input | measured `310000` (D-4) | none |
| S-6 | Accumulator magnitude for 1536-dim inputs | measured `1.536 × 10^13`, exceeding i32 (D-4) | none |
| S-7 | Differential test: same input into both ARI engines | that they disagree (P0-3) | records divergence; does not pick a winner |
| S-8 | The three JSON canonicalizations over one object | that they produce different bytes (D-7) | records; does not choose |
| S-9 | Guard: mutate `violations` in a log line, run `aura-replay` | that `CHAIN OK` is still reported (G-1) | records; does not change the digest |

**Why this is safe:** none of these changes a computed value, a format, or a hash. All of
them convert an *unknown* into a *recorded fact*, which is exactly what a governance
decision needs as input.

### 1.2 Test-runner and CI wiring — safe, and currently the largest gap

| # | Work | Rationale |
|---|---|---|
| S-10 | Add a CI step that runs the full unit suite (`python -m unittest discover` or `pytest`) | 105 locally-passing tests currently gate nothing (P1-6) |
| S-11 | Make `test_compliance.py` collectible (convert to `unittest.TestCase` **or** add a pytest invocation) | 4 tests never run in CI (P1-7). Converting the *harness* changes no assertion. |
| S-12 | Add `ruff`/`ruff format --check` to core CI | The Conformance Kit already does this; core has nothing |
| S-13 | Add `mypy` (start non-strict, gate later) | Same precedent |
| S-14 | Add coverage measurement (report only, no gate initially) | Makes §1.1 progress visible |
| S-15 | Add `pip-audit` and an SBOM job | Guard has `cargo audit` + `cargo deny` + CycloneDX |
| S-16 | Add CodeQL to core | Guard and the Kit both have it |
| S-17 | Add a `demo.py` smoke step to CI | Would have caught P1-5 |
| S-18 | Remove or create the `develop` branch trigger (P2-11) | Trivial, no semantic effect |
| S-19 | Add arm64 to Guard's CI matrix (P1-9) | Guard's own CI is single-platform |
| S-20 | Extend the determinism report to **also** cover the evaluator (P1-1) | **See the caveat in §2** |

### 1.3 Bug fixes with no normative content

| # | Fix | Why safe |
|---|---|---|
| S-21 | `demo.py` — catch `ValueError` instead of `AssertionError` (`:66`, `:97`) | The demo currently aborts. No production code touched; `demo.py` is not imported by anything. |
| S-22 | `demo.py` — stop passing float vectors into the int32 engine, and stop `:.4f`-formatting int32 values | Corrects an obviously-wrong caller, not the engine |
| S-23 | `core/evaluator.py:88` docstring — make it state what the code does (clamp at `200000`) | **Documentation-only.** Changes no value. Alternative — changing the clamp — is **not** safe: it changes output. |
| S-24 | Remove or fix `compliance/certificate_schema.json` (P1-13) | It is referenced by nothing; correcting or deleting a stale unused file changes no behaviour |
| S-25 | `compliance/policy.py` — `datetime.utcnow()` → `datetime.now(timezone.utc)` (P2-6) | Deprecation fix; affects only kill-switch state reporting, which is outside the measurement path |
| S-26 | Delete or wire `infra/docker-compose.yml` (P1-11) | Referenced by nothing |

### 1.4 Documentation of existing behaviour

| # | Work |
|---|---|
| S-27 | New `KL-00x` entries in `docs/KNOWN_LIMITATIONS.md` for D-1, D-2, D-3, D-4, D-5, D-6, D-7 — stating the behaviour and that the correct behaviour is unresolved |
| S-28 | Correct `docs/GAP-001.md` GAP-C5 from *"LARGELY RESOLVED"* to reflect the measured divergence (P0-3) |
| S-29 | Document the four coexisting rounding/reduction rules (Python half-to-even, floor `//`, SQL half-up, float division) as an AS-IS table |
| S-30 | Document that `packages/**` is unbuildable (P1-10) |
| S-31 | Document that CHECK 1/2/4 are lexical or existence checks, not behavioural ones (P2-7/8/9) |
| S-32 | Guard: correct the README determinism sentence to distinguish decision-determinism from `chain_hash` reproducibility (G-2) |
| S-33 | Guard: correct the stale test count in `docs/ROADMAP.md` (21+2+10+6 → 240) |
| S-34 | Guard: state in the README that `violations` are not covered by the chain digest (G-1) until it is addressed |

### 1.5 Static typing and refactoring — safe **within limits**

| # | Work | Limit |
|---|---|---|
| S-35 | Add type annotations to `compliance/` and `audit/` | Annotations only. **No `from __future__ import annotations` reorganization that alters import order in `core/`** — CHECK 9's AST boundary check inspects imports. |
| S-36 | Extract shared constants (`SCALING_FACTOR`, weights) into one module | **Only if** the new module lives outside `core/` or passes CHECK 2/3/9 unchanged; a `core/constants.py` importing nothing is acceptable, but must be verified against `check_cr003_layer_boundary.py` before merge |
| S-37 | Fix `core/__init__.__all__` (P2-3) | Changes what `from core import *` exposes; verify no test relies on the current list |

### 1.6 Observability and benchmarks

| # | Work | Note |
|---|---|---|
| S-38 | Add structured logging to `compliance/` and `audit/` | **Not to `core/`** — CHECK 5 (entropy) and CHECK 9 (boundary) constrain what `core/` may import, and logging modules are near the forbidden-import line. Verify before adding. |
| S-39 | Add performance benchmarks for the 1536-dim dot product | Measurement only; must not change the implementation |
| S-40 | Guard: nothing needed — `tracing` + Prometheus already present | |

### 1.7 All Aura-Guard engineering work

**Guard has zero dependency on the Constitution, the Vector, the embedding, the numeric
representation, or ARI** (`06_GUARD_AUDIT.md` §9). It is therefore **not blocked by
DR-002, SPEC-002, any `AD-CA-xxx`, or CR-007**.

Everything in `08_BLOCKERS.md` touching Guard — G-1 through G-5, P1-9, P1-14, P2-18,
P2-19 — is engineering work that can proceed on its own schedule. G-1 (adding `violations`
to the digest) requires a **product** decision about the log format, and must be planned
jointly with P1-14 (`f32` formatting determinism), but neither waits on governance.

**This is the largest block of genuinely unblocked work in the ecosystem.**

---

## 2. SAFE ONLY WITH AN EXPLICIT CAVEAT

### S-20 — Extending the determinism report to cover the evaluator

Adding evaluator vectors to `scripts/generate_determinism_report.py` would close P1-1 —
the most consequential coverage gap. But the report's vectors are **compared for equality
across platforms and then treated as a determinism claim**. Adding an evaluator vector
implicitly asserts *"this output is the reference output"*, which is very close to
treating current behaviour as normative — the exact thing this task forbids.

**Safe formulation:** add the vectors, and label them in the report schema as
`"status": "CHARACTERIZATION_ONLY"` / non-normative, with an explicit note that they
record current Python behaviour and carry no claim of correctness. Compared x86_64 vs
arm64 they still detect intra-Python platform divergence, which is genuinely useful and
normatively neutral.

**Unsafe formulation:** adding them silently to a document titled "determinism vectors"
alongside vectors that *are* backed by `docs/specs/AUDIT_LAYER_SPEC.md`.

### Bounds checking and error handling generally

Adding a *check* is safe. Deciding what happens *after* the check fires is not.

- Safe: detect a length mismatch and record/log it.
- Safe: detect out-of-scale input and record/log it.
- **Not safe:** deciding that a mismatch must `raise ValueError` vs return `0` vs return a
  sentinel vs clamp — that is `REQ-002-031` / NB-015, unresolved.

The practical consequence: P0-1 and P0-2 can be made **visible** now and **resolved** only
after NB-015.

---

## 3. MUST WAIT FOR GOVERNANCE

### 3.1 Absolutely blocked

| Work | Blocked by |
|---|---|
| Generating a Constitution Vector | NB-003, NB-007, NB-008, NB-009 |
| Creating `constitution.json` | same |
| Implementing CR-007 | explicitly BLOCKED per `SPEC-002 §11.B` |
| Selecting or implementing an embedding method | NB-007 (`AD-CA-005`) |
| Replacing `core/embedding.py` with a real embedder | NB-007 |
| Choosing the rounding rule | NB-009 (`AD-CA-007` — candidate only) |
| Choosing integer-division semantics | NB-016 (not even a listed candidate) |
| Choosing the numeric representation (width, endianness, scale, dimension) | NB-009 |
| Defining a canonical serialization format or canonical byte sequence | NB-010 (`AD-CA-008`) |
| Defining hash domains | NB-010 |
| Unifying the three JSON canonicalizations onto one form | NB-010 — *recording the divergence is safe; picking one is not* |
| Writing SPEC-002 conformance tests | `SPEC-002 §11`: NOT READY |
| Creating any fixture whose expected value depends on the above | all of the above |
| Deciding required failure modes on malformed input | NB-015 (`REQ-002-031`) |
| Deciding which ARI engine is authoritative | NB-017 |
| Deciding the Merkle construction | NB-018 |
| Deciding whether halt state must be durable/distributed | NB-019 |
| Deciding whether Core and Guard integrate at all, and how | NB-020 |

### 3.2 Items from the task's "potentially safe" list that are **NOT** safe here

The task explicitly warned against assuming every listed category is safe. Verified
against this architecture:

| Category | Verdict | Reason |
|---|---|---|
| **Malformed-input handling** | **PARTIALLY UNSAFE** | Detection is safe; the required *response* is NB-015. Implementing a `raise` today would encode an unresolved failure-mode decision into the reference implementation. |
| **Bounds checking** | **PARTIALLY UNSAFE** | Same split. Additionally, `evaluate()`'s missing upper clamp cannot be "fixed" by adding one — clamping changes output values. |
| **Error handling** | **PARTIALLY UNSAFE** | Changing `PolicyRule.is_violated`'s catch-all (`compliance/policy.py:79-88`) alters fail-closed behaviour, which is a policy semantic. |
| **Refactoring** | **CONDITIONALLY SAFE** | Any refactor touching `core/` must re-pass CHECK 2 (lexical float grep — a variable named `float_scale` would trip it), CHECK 3 (import scan), CHECK 5 (entropy grep) and CHECK 9 (AST boundary). Renaming a symbol can fail a check for lexical reasons unrelated to correctness. Verify before merge. |
| **Static typing** | **CONDITIONALLY SAFE** | Annotating `core/` risks CHECK 2: the token `float` in an annotation would trip the grep. `scripts/verify_constitutional_purity.py` handles annotations correctly (`visit_arg`, `visit_AnnAssign`), but `check_2_integer_only.sh` is a plain grep and does not. **Do not annotate `core/` with `float` in any position.** |
| **CI improvements** | **SAFE**, with one exception | Adding a job is safe. Changing what an existing CHECK asserts is not — the checks are the repository's conformance evidence, and `AGENTS.md` rule 10 forbids weakening tests to make implementation pass. |
| **Observability** | **CONDITIONALLY SAFE** | Not in `core/` without verifying CHECK 5 / CHECK 9. Safe in `compliance/`, `audit/`, Guard. |
| **Performance benchmarks** | **SAFE** | Measurement only. Any optimization that changes evaluation order of the dot product is **not** safe — summation order affects nothing for integers today, but would if the numeric model changes. |
| **Documentation of existing behaviour** | **SAFE** | The safest category, and the one this package itself occupies. One caution: documenting behaviour must not slide into documenting it as *required* behaviour. |

### 3.3 A note on the "FROZEN" declaration

`aura-poc-a-core-v3.3` self-declares v3.3 as FROZEN
(`scripts/run_all_checks.sh:14`: *"Specification: v3.3 (FROZEN)"*;
`scripts/verify_constitutional_purity.py:9-10`: *"If this script fails, the system MUST
NOT be sealed, released or executed"*). The specification repository's own
`reference/RI-PY_AURA_POC_A_CORE.md` records this as a governance problem: *"Self-declared
FROZEN (v3.3) — this creates a governance challenge as APS gaps require changes."*

**Consequence for this section:** every item in §1.3 (bug fixes) and §1.5 (refactoring)
touches a repository that declares itself frozen. This audit does **not** resolve whether
the freeze permits defect correction. Items are listed as *engineering-safe*; whether they
are *governance-permitted* under the freeze is NB-021, and should be answered before any
of them is merged.

Items in §1.1 (new test files), §1.2 (CI), §1.4 (documentation) and §1.7 (Guard) do not
modify frozen production code and are unaffected by that question.

---

## 4. Suggested Sequencing (engineering only, no governance dependency)

Ordered by value-per-risk, not by priority label:

1. **§1.1 characterization tests** — converts every open determinism question into a
   recorded fact. Zero risk. Directly feeds the blocked decisions with the data they need.
2. **§1.2 CI wiring (S-10, S-11)** — makes 109 already-existing passing tests actually gate
   merges. Zero new semantics.
3. **§1.7 Aura-Guard work** — entirely unblocked; G-1 is the ecosystem's most serious
   integrity finding outside P0-1.
4. **§1.4 documentation** — corrects three stale claims (GAP-C5, Guard README determinism,
   Guard ROADMAP test count) that currently mislead.
5. **§1.2 static analysis (S-12 … S-16)** — brings core CI to the standard the Conformance
   Kit already meets.
6. **§1.3 bug fixes** — pending the NB-021 freeze question.

**Nothing in this sequence requires DR-002, SPEC-002, or any `AD-CA-xxx` to be resolved.**
