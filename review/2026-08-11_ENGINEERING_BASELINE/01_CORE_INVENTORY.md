# 01 — CORE INVENTORY (TASK 1)

Scope: `AuraIDToken/aura-poc-a-core-v3.3` @ `9c6a5d8`.
Aura-Guard is inventoried separately in `06_GUARD_AUDIT.md`.

Total Python/TypeScript source under audit: **4,893 lines** across 30 files
(1,957 lines non-test Python; 2,196 lines test Python; 17 lines TypeScript;
plus 2 `.circom` files, 1 `.sql` file, 1 workflow, 11 shell/py check scripts).

---

## 1. Summary Table

| # | Component | Path | Status | Reachable from |
|---|---|---|---|---|
| 1 | ARI measurement engine | `core/evaluator.py` | **IMPLEMENTED** (with unvalidated inputs) | tests, `demo.py`, `compliance/evaluator_wrapper.py` |
| 2 | Offline vector normalizer | `core/offline_normalizer.py` | **IMPLEMENTED** | tests, determinism report, own CLI |
| 3 | Text embedding | `core/embedding.py` | **PLACEHOLDER** | `test_compliance.py` only |
| 4 | ETC attestor (Layer 0 copy) | `core/merkle.py` | **PLACEHOLDER** | `demo.py`, `core/test_ari.py`, `core/test_integration.py` |
| 5 | Layer-0 policy wrapper | `core/policy.py` | **PARTIAL** (deprecated shim) | back-compat only |
| 6 | Layer-0 consistency wrapper | `core/consistency.py` | **PARTIAL** (deprecated shim) | back-compat only |
| 7 | Regulatory policy + kill-switch | `compliance/policy.py` | **IMPLEMENTED** (process-local state) | wrapper, tests, `demo.py` |
| 8 | Consistency calculator (2nd ARI impl.) | `compliance/consistency.py` | **IMPLEMENTED** | `test_compliance.py`, shim |
| 9 | Layer-2 orchestrator | `compliance/evaluator_wrapper.py` | **IMPLEMENTED** | tests, `demo.py` |
| 10 | Event certificate | `compliance/certificate.py` | **IMPLEMENTED** | `test_compliance.py` |
| 11 | Certificate renderer | `compliance/renderer.py` | **IMPLEMENTED** | package export only |
| 12 | Certificate JSON schema | `compliance/certificate_schema.json` | **UNUSED** | — (0 references) |
| 13 | Merkle tree + ETC (Layer 1) | `audit/merkle.py` | **IMPLEMENTED** | `audit/` tests, `test_compliance.py`, determinism report |
| 14 | Signing abstraction (HMAC) | `audit/signing.py` | **IMPLEMENTED** | `audit/merkle.py`, tests, determinism report |
| 15 | Audit verifier | `audit/verify.py` | **IMPLEMENTED** (thin passthrough) | `audit/test_audit.py` |
| 16 | pgvector client | `packages/database-client/VectorRepository.ts` | **UNUSED** | — (0 references, no build) |
| 17 | ZK circuits | `packages/zk-passport/*.circom` | **UNUSED** | — (0 build, 0 CI, 0 tests) |
| 18 | Persistence schema | `init.sql` | **PARTIAL** (schema only, no writer) | test harnesses via `psql` |
| 19 | Demo / entry point | `demo.py` | **PARTIAL — currently crashes** | manual |
| 20 | Compliance smoke script | `test_compliance.py` | **IMPLEMENTED** (not auto-collected) | manual |
| 21 | Check scripts | `scripts/checks/*.sh`, `scripts/*.py` | **IMPLEMENTED** | CI workflow |
| 22 | Determinism report + compare | `scripts/generate_determinism_report.py`, `scripts/compare_determinism_reports.py` | **IMPLEMENTED** | CI workflow |
| 23 | CI | `.github/workflows/execution-checks.yml` | **PARTIAL** | GitHub Actions |
| 24 | Packaged CLI | *(none)* | **ABSENT** | — |

---

## 2. Executable Components

### 2.1 `core/evaluator.py` — `PoCAEvaluator` — IMPLEMENTED

**What it does (AS-IS):**
- `vector_similarity_int32(v1, v2)` (`core/evaluator.py:26`): integer dot product over
  `zip(v1, v2)`, then `dot // SCALING_FACTOR` (floor division).
- `evaluate(agent_id, vector, valid_schema)` (`core/evaluator.py:51`): returns
  `{"ari": int, "drift": int}`. `SI` is `100000` or `0`; `RAW_ARI =
  (30000*SI)//100000 + (70000*SA)//100000`, clamped at `max(0, …)`.
  `drift = min(max(0, 100000 - SA), 200000)`.

**What it does not do:**
- No dimension check on `vector` vs `self.constitution`.
- No magnitude/normalization check on either vector.
- No upper clamp on `ari`.

**Executed evidence (this session):**
```
PoCAEvaluator([100000]*4).evaluate("a", [100000]*4, True)
  → {'ari': 310000, 'drift': 0}          # ari > documented max 100000
PoCAEvaluator([-100000,0,0,0]).evaluate("a", [100000,0,0,0], True)
  → {'ari': 0, 'drift': 200000}          # drift > docstring's stated [0, 100000] clamp
```
The `evaluate()` docstring at `core/evaluator.py:88` states *"Clamp drift to [0, 100000]
to represent [0.0, 1.0]"*; the code on the next line clamps to `2 * SCALING_FACTOR`.
Docstring and code disagree — **the code is what runs**.

### 2.2 `core/offline_normalizer.py` — IMPLEMENTED

Float L2-normalize (`:64`) → `round(x * 10**5)` (`:88`) → optional 1 % unit-vector
validation (`:118`) → optional JSON write (`:200`). Dimension is hard-checked against
`CONSTITUTION_DIM = 1536` (`:171`). Float use here is explicitly scoped as offline
(module docstring `:23-28`) and is excluded from CHECK 2 by filename.

Has a working `__main__` CLI (`:237`) — the **only** CLI in the repository.

### 2.3 `core/embedding.py` — `embed_text` — PLACEHOLDER

Self-declared: *"Placeholder for deterministic embedding in ℝ¹⁵³⁶ space"* (`:3`).
Returns `[(ord(c) % 32) * 3125 …]` tiled to 1536 entries (`:19-22`).

Referenced only by `test_compliance.py:13`. **Not referenced by `core/evaluator.py`,
`compliance/`, `audit/`, CI, or `demo.py`.**

Already recorded as non-production in `docs/GAP-001.md` GAP-M4 / RISK-010. This audit
confirms the code state; it makes **no** statement about what a correct embedding
would be (AD-CA-005 is unresolved).

### 2.4 `core/merkle.py` — `MerkleAttestor` — PLACEHOLDER

13 lines. `generate_etc()` (`:11`) returns `{"certificate": "AURA-ETC-" + leaf[:16],
"proof": [leaf]}`. **The "proof" is the leaf itself** — it is not a Merkle inclusion
proof and cannot be verified against any root. There is no root.

A genuine Merkle implementation exists separately at `audit/merkle.py` (262 lines, real
proofs, real verification). The two are unrelated code paths. `demo.py`,
`core/test_ari.py` and `core/test_integration.py` use the placeholder; `audit/` tests
and `test_compliance.py` use the real one.

### 2.5 `core/policy.py`, `core/consistency.py` — PARTIAL (deprecated shims)

Both emit `DeprecationWarning` at import and re-export from `compliance.*`. Documented
as accepted debt in `docs/KNOWN_LIMITATIONS.md` KL-002, scheduled for removal in v4.0,
and explicitly excluded from CHECK 3 by `--exclude=policy.py --exclude=consistency.py`
(`scripts/checks/check_3_layer_separation.sh:44`).

### 2.6 `compliance/policy.py` — IMPLEMENTED, with a state-model caveat

- `RegulatoryPolicy.HALTED_AGENTS` (`:29`) is a **class-level `set()` in process
  memory**.
- `KillSwitch` (`:70`) holds `_active` in an instance; `_global_kill_switch` (`:145`) is
  a module singleton.
- `init.sql` defines a `kill_switch_state` table, but **no Python code reads or writes
  it** (grep: 0 hits outside `check_cr003_layer_boundary.py`'s forbidden-import list).

So halt state is per-process and non-durable. AGENTS.md canonical rule 5 states *"No
process-local global state may be treated as a distributed safety guarantee."* The
engineering observation here is only that the state **is** process-local and that a DB
table for it exists unused; whether the Art. 14 control is required to be distributed is
a governance question.

- `validate_target()` (`:23`) raises `ValueError`. This is **not** `assert`, so AGENTS.md
  rule 4 is satisfied. CHECK 6 (`scripts/art5_conformance_proof.py`) re-verifies this
  under `-O` and `-OO` and passes (executed this session: PASS ×3).

### 2.7 `compliance/consistency.py` — `ConsistencyCalculator` — IMPLEMENTED (second ARI implementation)

`calculate()` (`:28`) computes
`score = 30000*structural//100000 + 70000*semantic//100000 - penalty`, clamped to
`[0, 100000]` (`:59-62`).

This is a **parallel, non-identical** implementation of the same ARI formula as
`PoCAEvaluator` + `evaluator_wrapper`. Differences observed:

| Aspect | `core.evaluator` + `evaluator_wrapper` | `compliance.consistency` |
|---|---|---|
| Magnitude validation | none | raises `ValueError` if any `abs(v) > 100000` (`:85`,`:88`) |
| Zero-vector guard | none | returns `0` (`:82`) |
| Upper clamp on score | none | clamps to `100000` (`:62`) |
| Penalty model | `DRIFT_PENALTY = 150000` when `SA < 68000` (`compliance/policy.py:20-21`) | `VIOLATION_PENALTY = 10000` × violation count (`:24`, `:99`) |
| Kill-switch check | `check_halt_status(agent_id)` → raises | `assert_not_halted()` → returns `{"status": "HALTED"}` |
| Length mismatch | silent `zip` truncation | silent `zip` truncation |

Executed evidence:
```
ConsistencyCalculator([200000,0,0,0], []) → ValueError (rejects unnormalized)
PoCAEvaluator([200000,0,0,0]).evaluate(...) → {'ari': 170000, 'drift': 0}  (accepts)
```

`docs/GAP-001.md` GAP-C5 claims duplicate ARI implementations are *"LARGELY RESOLVED"*.
**AS-IS this is not the case**: two independently-behaving implementations remain, with
divergent validation, clamping and penalty semantics.

### 2.8 `compliance/evaluator_wrapper.py` — IMPLEMENTED

`evaluate_with_policy()` (`:27`) orchestrates: halt check → recompute `SA` (a second,
redundant `vector_similarity_int32` call at `:63`) → `evaluator.evaluate()` (which
computes `SA` a **third** time internally) → subtract penalty → return.

`SA` is therefore computed twice per evaluation on the same inputs.

### 2.9 `compliance/certificate.py` / `renderer.py` — IMPLEMENTED

`AuraEventCertificate` is a frozen dataclass holding `ari_score: float` and
`drift: float` (`:39-40`). Its docstring (`:22-33`) explicitly documents int32 → float
conversion at this boundary as intentional and presentation-only.

`fingerprint()` (`:65`) = SHA-256 over `json.dumps(to_dict(), sort_keys=True)`.
**Note:** `sort_keys=True` is used but default separators (`', '`, `': '`) are used, so
the canonical byte form differs from `audit/merkle.py:_signing_payload()` which uses
`separators=(",", ":")` (`audit/merkle.py:89`). Two different JSON canonicalizations
coexist in the repository.

Executed evidence of the float boundary carrying an out-of-range value through:
```
AuraEventCertificate(... 100001/100000 ...).to_dict()["ari"]
  → {'score': 1.00001, 'drift': 1.00001, ...}
```

### 2.10 `audit/` — IMPLEMENTED

- `audit/merkle.py`: real `MerkleTree` with level-by-level construction (`:145`),
  odd-node duplication (`:157`), `get_proof()` (`:172`), `EventTrustCertificate` with
  `verify()` (`:110`) and optional HMAC signature (`:97`).
- `audit/signing.py`: abstract `Signer`/`Verifier` + `HMACSigner`/`HMACVerifier`
  (HMAC-SHA256, `hmac.compare_digest`). Key type is enforced (`:78`, `:104`).
- `audit/verify.py`: 35 lines, pure delegation to `audit/merkle.py`.

This is the most complete and best-tested subsystem in the repository.

### 2.11 `packages/` — UNUSED

- `VectorRepository.ts` (17 lines): raw SQL with pgvector `<=>` cosine operator. There is
  **no `package.json`, no `tsconfig.json`, no lockfile, no build step, no test, and no
  importer** anywhere in the repository or CI. It cannot currently be compiled or run.
- `zk-passport/`: two `.circom` circuits plus three markdown documents
  (`INTEGRATION.md`, `TEST_SPECIFICATION.md`, `README.md`). **No circom toolchain, no
  build, no CI job, no test runner.** `TEST_SPECIFICATION.md` describes tests that do
  not exist as executable artefacts.

Both are inside `PROTECTED_PATHS` of `scripts/verify_constitutional_purity.py:26-29`, so
they are AST-scanned by CHECK 0 despite being unbuildable — the scanner parses `.py`
only, so in practice neither is scanned.

### 2.12 `init.sql` — PARTIAL

Schema is present and non-trivial:
- `audit_events` with append-only `BEFORE UPDATE OR DELETE` trigger (`:74-82`);
- three CHECK constraints binding `certificate->>'RAW_ARI'` to `[0, 100000]` integer and
  binding `poca_score` to a **SQL-side half-up cent rounding rule**
  `((RAW_ARI + 500) / 1000)::NUMERIC / 100` (`:60-62`);
- `agent_constitutions` with `embedding vector(32)` (`:96`);
- `kill_switch_state`, `policy_violations`.

**No application code writes to any of these tables.** Grep for `psycopg|asyncpg|
sqlalchemy|audit_events` across all non-test `*.py`: 0 hits. The only writers are the
two docker-dependent test classes, which shell out to `psql`.

Two AS-IS discrepancies worth recording (both are engineering observations, not
normative claims):
1. `embedding vector(32)` vs `CONSTITUTION_DIM = 1536` in
   `core/offline_normalizer.py:44` — a 48× dimension mismatch between schema and code.
2. `poca_score DECIMAL(3,2)` with a half-up rounding rule in SQL, while the Python
   normalizer uses `round()` (half-to-even) and `compliance/certificate.py` uses plain
   float division. **Three different numeric reduction rules coexist.** Which (if any) is
   correct is AD-CA-007, unresolved.

### 2.13 `demo.py` — PARTIAL, currently crashes

Executed this session:
```
DEMO 1: ARI Score: 0.0000  /  Drift: 100000.0000
DEMO 2: Traceback … ValueError: CRITICAL: Human scoring is strictly prohibited.
```
Two independent defects:
- `demo.py:66` and `:97` catch `AssertionError`, but `compliance/policy.py:27` raises
  `ValueError`. The demo aborts at DEMO 2 and never reaches DEMO 3 or DEMO 4.
- `demo.py:22-26` passes **float** vectors (`[0.5, 0.3, 0.8, 0.1]*4`) into the int32
  evaluator, and formats int32 outputs with `:.4f`. Result: `ari` is `0` and `drift`
  prints as `100000.0000`. The demo's own final banner ("Repository is MC-READY ✓") is
  never reached.

`demo.py` is not run by CI, so this has not been caught.

### 2.14 `test_compliance.py` — IMPLEMENTED but not auto-collected

Four function-level tests (`:18`, `:49`, `:114`, `:191`) with a hand-rolled runner
(`__main__`). Executed this session: **4/4 PASS**.

Because they are module-level `def test_*()` functions rather than `unittest.TestCase`
methods, `python -m unittest discover` **does not collect them**, and CI never invokes
`test_compliance.py` directly (`.github/workflows/execution-checks.yml` calls
`run_all_checks.sh` and one `pytest` selector, neither of which touches this file).
**These four tests do not run in CI.**

---

## 3. Public APIs

There is no packaged, versioned public API surface.

| Surface | Definition | Notes |
|---|---|---|
| `core.__init__.__all__` | `["consistency", "embedding", "policy", "offline_normalizer"]` (`core/__init__.py:2`) | Lists the two **deprecated shims** and the **placeholder** embedder. Does **not** list `evaluator` — the actual engine. |
| `compliance.__init__.__all__` | `["AuraEventCertificate", "render_certificate"]` | Does not export `ConsistencyCalculator`, `RegulatoryPolicy`, or `evaluate_with_policy`. |
| `audit.__init__.__all__` | `["merkle","verify","signing","Signer","Verifier","HMACSigner","HMACVerifier"]` | Coherent. Does not export `MerkleTree` or `EventTrustCertificate` directly. |
| HTTP / RPC | **none** | No server, no endpoint, in any Python file. |
| Console scripts | **none** | `pyproject.toml` declares no `[project.scripts]`. |

**Status: PARTIAL.** The package exports are inconsistent with the code that is actually
exercised by tests and CI.

---

## 4. Mathematical Core

| Element | Location | Status |
|---|---|---|
| Fixed-point scale `10^5` | `core/evaluator.py:19`, `compliance/consistency.py:20`, `compliance/policy.py:19`, `core/offline_normalizer.py:41` | **IMPLEMENTED** — declared independently in 4 places, no shared constant |
| Weights 0.3 / 0.7 | `core/evaluator.py:23-24`, `compliance/consistency.py:21-22` | **IMPLEMENTED** — duplicated |
| Integer dot product | `core/evaluator.py:41`, `compliance/consistency.py:96` | **IMPLEMENTED** |
| Rescale by floor division | `core/evaluator.py:47`, `compliance/consistency.py:97` | **IMPLEMENTED** — see `04_DETERMINISM_AUDIT.md` D-1 |
| Drift | `core/evaluator.py:89` | **IMPLEMENTED** — code/docstring mismatch |
| Penalty | `compliance/policy.py:39` and `compliance/consistency.py:99` | **PARTIAL** — two incompatible definitions |
| L2 norm / sqrt | `core/offline_normalizer.py:64,108` | **IMPLEMENTED** (offline, float, by design) |
| Cosine similarity | *(absent)* | The name appears in docs and in `test_ari.py:214`'s test name, but no cosine is computed anywhere — only a dot product on assumed-unit vectors. |

**Note on the "cosine" naming:** `core/test_ari.py:214` is named
`test_cosine_similarity_calculation` and `scripts/verify_constitutional_purity.py:39`
lists `cosine` as a FORBIDDEN name. The production code computes a dot product, not a
cosine. This is a naming inconsistency, recorded, not resolved.

---

## 5. Normalization Code

| Element | Location | Status |
|---|---|---|
| Offline float→int32 normalizer | `core/offline_normalizer.py` | **IMPLEMENTED** |
| Runtime normalization | *(absent)* | **ABSENT** — runtime assumes inputs are already normalized |
| Runtime enforcement of that assumption | `compliance/consistency.py:85,88` only | **PARTIAL** — `PoCAEvaluator` has none |
| Text normalization | *(absent in this repo)* | Exists only in Aura-Guard (`src/normalizer.rs`), unrelated pipeline |

---

## 6. Vector Operations

| Op | Location | Status |
|---|---|---|
| Dot product | `core/evaluator.py:41`, `compliance/consistency.py:96` | **IMPLEMENTED** |
| L2 magnitude | `core/offline_normalizer.py:64,107` | **IMPLEMENTED** (offline only) |
| Unit-vector verification | `core/offline_normalizer.py:93` | **IMPLEMENTED** (1 % tolerance, offline only) |
| Dimension validation | `core/offline_normalizer.py:171` only | **PARTIAL** — absent at runtime |
| Similarity search (pgvector) | `packages/database-client/VectorRepository.ts` | **UNUSED** |

---

## 7. Hashing

| Element | Location | Status |
|---|---|---|
| SHA-256 over UTF-8 string | `audit/merkle.py:16` | **IMPLEMENTED** |
| Merkle root / proof | `audit/merkle.py:145,172` | **IMPLEMENTED** |
| ETC signing payload | `audit/merkle.py:89` (`sort_keys=True`, `separators=(",",":")`) | **IMPLEMENTED** |
| HMAC-SHA256 | `audit/signing.py:88` | **IMPLEMENTED** |
| Certificate fingerprint | `compliance/certificate.py:69` (`sort_keys=True`, **default separators**) | **IMPLEMENTED** — different canonicalization from above |
| Layer-0 "leaf" | `core/merkle.py:8` (`sort_keys=True`, default separators) | **PLACEHOLDER** — third canonicalization |
| Asymmetric signing | *(absent)* | **ABSENT** — `audit/signing.py` docstring names Ed25519 as future work |

**Three distinct JSON canonicalizations** are used for hash inputs across the
repository. No shared canonicalization module exists.

---

## 8. Serialization

| Element | Location | Status |
|---|---|---|
| ETC → dict | `audit/merkle.py:48` | **IMPLEMENTED** |
| Certificate → dict / JSON / text / compliance report | `compliance/certificate.py:53`, `compliance/renderer.py:14` | **IMPLEMENTED** |
| Int32 vector → little-endian bytes | `core/test_bitwise_replay.py:295`, `scripts/generate_determinism_report.py:65` | **IMPLEMENTED — in test/CI code only, not in `core/`** |
| Normalized vector → JSON file | `core/offline_normalizer.py:192-201` | **IMPLEMENTED** |
| Canonical serialization module | *(absent)* | **ABSENT** — `docs/GAP-001.md` GAP-H3 |
| `certificate_schema.json` | `compliance/certificate_schema.json` | **UNUSED** — 0 code references; its fields (`certificate_id`, `agent.constitution_hash`, `signature`, `ari.formula`, `ari.status`) are **not produced** by `AuraEventCertificate.to_dict()`, and `schema_version` differs (`"1.0"` vs `"1.0.0"`) |

**Note:** the canonical byte encoding used by the determinism report
(`int32 → 4 bytes little-endian signed`) lives in **test and script code**, not in a
production module. Production code never serializes a vector to bytes.

---

## 9. Replay

| Element | Location | Status |
|---|---|---|
| Bitwise replay test suite | `core/test_bitwise_replay.py` | **PARTIAL** — see below |
| Determinism report generator | `scripts/generate_determinism_report.py` | **IMPLEMENTED** |
| Cross-platform comparator | `scripts/compare_determinism_reports.py` | **IMPLEMENTED** |
| Replay of a recorded evaluation | *(absent)* | **ABSENT** |

`core/test_bitwise_replay.py` "replay" (`:159`) recomputes an inline weighted sum twice
in the same process. It does **not** replay a `PoCAEvaluator` evaluation, and it does not
load any recorded input. `PoCAEvaluator` is **not imported** by this file at all.

---

## 10. Persistence

**Status: PARTIAL.** Schema exists (`init.sql`), enforcement (append-only trigger, CHECK
constraints) exists, docker-compose exists — but there is **no application persistence
layer**. Nothing in `core/`, `compliance/`, or `audit/` opens a database connection.
`scripts/check_cr003_layer_boundary.py:39-42` actively *forbids* DB drivers in Layer 0,
which is consistent; but no Layer 1/2 writer exists either.

---

## 11. Configuration

**Status: PARTIAL / minimal.**

| Element | Location | Notes |
|---|---|---|
| Build metadata | `pyproject.toml` | 12 lines. No dependencies declared, no dev extras, no lint/type config, no test config. |
| Runtime config | *(absent)* | No config file, no env-var reader, no `Config` class. All constants are hard-coded literals in source. |
| Compose (root) | `docker-compose.yml` | `pgvector/pgvector:pg16`, password via `${POSTGRES_PASSWORD:-aura_local_dev}`. |
| Compose (infra) | `infra/docker-compose.yml` | `ankane/pgvector:v0.7.0`, **different image, different DB name (`aura_sandbox` vs `aura_core`), default password `cathedral_secure`**, no healthcheck, no `init.sql` mount. Not referenced by any test or CI job. Recorded in `docs/GAP-001.md` GAP-L5. |

Two divergent compose files describing two different databases is an AS-IS
inconsistency; `infra/docker-compose.yml` appears to be dead configuration.

---

## 12. CLI

**Status: PARTIAL.**

- Exactly one CLI: `python core/offline_normalizer.py [input.json] [output.json]` /
  `--generate-sample` (`core/offline_normalizer.py:237-288`).
- `pyproject.toml` declares no console entry points.
- `demo.py` and `test_compliance.py` are runnable scripts, not CLIs.
- No CLI for evaluation, certificate generation, verification, or replay.

By contrast Aura-Guard ships four binaries (see `06_GUARD_AUDIT.md`).

---

## 13. Tests

**Status: IMPLEMENTED (coverage gaps documented in `05_TEST_MATRIX.md`).**

Executed this session — `python3 -m unittest discover -s . -p "test_*.py"`:

```
Ran 107 tests in 0.649s
FAILED (errors=2)
```

Both errors are `setUpClass` failures from Docker being unavailable in this environment:
- `audit.test_audit_db_integration.TestAuditEventsAppendOnlyIntegration`
- `core.test_cr003_statelessness.TestCR003Statelessness`

Neither is a code failure. **105 non-Docker tests pass.**

| File | Tests | Notes |
|---|---|---|
| `audit/test_audit.py` | 47 | largest suite |
| `core/test_offline_normalizer.py` | 29 | |
| `core/test_ari.py` | 14 | |
| `core/test_bitwise_replay.py` | 10 | 8 + 2 WASM-compat |
| `core/test_integration.py` | 3 | |
| `core/test_cr003_statelessness.py` | 1 | Docker-gated |
| `audit/test_audit_db_integration.py` | 1 | Docker-gated |
| `test_compliance.py` | 4 | **not collected by discovery, not in CI** |

---

## 14. CI

**Status: PARTIAL.** `.github/workflows/execution-checks.yml`, 3 jobs:

1. `execution-checks` — matrix `ubuntu-latest` (x86_64) × `ubuntu-24.04-arm` (arm64);
   runs `scripts/run_all_checks.sh`, then generates and uploads a determinism report.
2. `wasm-compat` — runs `pytest core/test_bitwise_replay.py::WASMCompatibilityTest`
   (2 tests). Named "WASM Compatibility Verification"; the job's own comment (`:83-85`)
   concedes it does not execute WASM.
3. `compare-determinism` — downloads both reports, runs
   `scripts/compare_determinism_reports.py`, fails on any vector mismatch.

**Observed CI gaps:**
- The unit test suites (`audit/test_audit.py`, `core/test_ari.py`,
  `core/test_offline_normalizer.py`, `core/test_integration.py`) are **not invoked as
  such**. Only `core/test_bitwise_replay.py` runs, via CHECK 1. There is no
  `unittest discover` / full `pytest` step.
- `test_compliance.py` never runs.
- `demo.py` never runs (which is why its crash is undetected).
- No linter, no formatter, no type checker, no coverage gate, no dependency audit, no
  SBOM, no CodeQL. (Aura-Guard's CI has all of these.)
- `pip install pytest` occurs only in the `wasm-compat` job; the other jobs rely on
  stdlib `unittest`.
- Only Linux. No macOS, no Windows, no 32-bit target, no non-CPython interpreter.
- Branch triggers are `main` and `develop`; a `develop` branch does not exist on the
  remote (`git branch -a` shows `main` only besides working branches).

**Locally executed check status (this session, x86_64, Python 3.11.15):**

| Check | Result |
|---|---|
| CHECK 0 Constitutional Compliance | PASS |
| CHECK 1 Bit Identity | PASS |
| CHECK 2 Integer Only | PASS |
| CHECK 3 Layer Separation | PASS |
| CHECK 4 Audit Path | PASS |
| CHECK 5 Entropy | PASS |
| CHECK 6 Art.5 (DEFAULT / -O / -OO) | PASS / PASS / PASS |
| CHECK 7 CR-004 Append-Only DB | NOT EXECUTED (no Docker) |
| CHECK 8 CR-003 History-Independence | NOT EXECUTED (no Docker) |
| CHECK 9 CR-003 Layer Boundary | NOT EXECUTED here (script is docker-independent but was not run standalone) |

**Observed check-design limitations** (AS-IS, not judgements of intent):
- CHECK 2 is a `grep` for the literal strings `float|sqrt|numpy` over `core/*.py` with
  `--exclude=offline_normalizer.py --exclude=test_*.py`. It is a lexical scan: it cannot
  detect float *values* (e.g. `0.5` literals), float-producing operations (`/`), or
  floats arriving as function arguments. `demo.py` passes float lists into
  `PoCAEvaluator` and CHECK 2 does not see it, because `demo.py` is outside `core/`.
- CHECK 4 verifies that files exist and contain certain function-name substrings. It does
  not execute any audit path.
- CHECK 5 counts SLOC and greps for `random|time.time()|datetime.now()|uuid|os.urandom`
  in `core/*.py` only. `compliance/policy.py:88` uses `datetime.utcnow()`, outside the
  scanned scope.
- CHECK 1 prints "PASSED" unconditionally after the test run, then prints instructions
  telling a human to compare hashes across platforms manually. The actual automated
  cross-platform comparison is done by the separate `compare-determinism` job, whose
  vectors do **not** include any `PoCAEvaluator` output (see §15).

---

## 15. Cross-Platform Tests

**Status: PARTIAL.**

Automated cross-platform comparison exists and is real: the `compare-determinism` job
compares five vectors between x86_64 and arm64 runners
(`scripts/generate_determinism_report.py:107-113`):

| Vector | Covers |
|---|---|
| `ari_vector_hash` | `generate_sample_constitution()` → first 1000 int32 → LE bytes → SHA-256 |
| `canonical_event_hash` | SHA-256 of a fixed string |
| `merkle_root` | `audit/merkle.py` `MerkleTree` over 4 fixed strings |
| `etc_hash` | SHA-256 of the ETC dict |
| `hmac_signature_hex` | HMAC-SHA256 over the ETC signing payload |

**What is NOT covered by any cross-platform vector:**

- `PoCAEvaluator.vector_similarity_int32` — **not imported by the report generator**.
- `PoCAEvaluator.evaluate` — same.
- `ConsistencyCalculator.calculate` — same.
- `RegulatoryPolicy.calculate_penalties` — same.
- `AuraEventCertificate.fingerprint` — same.
- Any negative / malformed / mismatched-length input.

Despite the name `ari_vector_hash`, **no ARI is computed anywhere in the determinism
report**. The vector is the *constitution vector*, not an ARI result. The entire
evaluation path — the subsystem where the three reported determinism issues live — has
**zero cross-platform coverage**.

Only two platforms (Linux x86_64, Linux arm64), one Python (3.12 in CI; 3.11.15 locally),
one interpreter. WASM is asserted by proxy, never executed.
