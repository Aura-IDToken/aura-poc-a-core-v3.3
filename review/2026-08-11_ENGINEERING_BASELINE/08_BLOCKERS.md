# 08 — BLOCKERS (TASK 8)

---

## 0. The Separation Rule Applied Here

Two categories, kept strictly apart:

**ENGINEERING BLOCKER** — the code is wrong, inconsistent with its own stated contract,
unverified, or unbuildable. Resolvable by engineering work alone. **A missing normative
decision is never listed here.**

**NORMATIVE BLOCKER** — a decision that only governance can make. Listed separately, with
no priority ranking, because engineering priority does not apply to decisions that
engineering may not take.

**Explicitly not treated as engineering blockers**, per the task instruction:
- absence of a Constitution Vector format
- absence of an embedding method
- absence of normalization / rounding / division semantics
- absence of a canonical serialization format
- absence of SPEC-002 conformance tests
- the Conformance Kit's emptiness

Each of those is a downstream consequence of an unresolved decision. They appear in §4.

---

## 1. P0 — Must Be Resolved Before Production

*"Production" means: any deployment whose ARI output, decision, or evidence record is
relied upon by a third party.*

### P0-1 — Silent dimension-mismatch truncation yields maximum score

**Component:** `core/evaluator.py:41`, `compliance/consistency.py:96`
**Determinism ref:** D-3 (ACTIVE / UNTESTED / ENGINEERING BUG)

`zip()` truncates to the shorter vector. Measured: a 2-element agent vector against a
4-element constitution returns `100000` — perfect alignment — and
`ConsistencyCalculator` returns `score: 100000`.

This is **fail-open**: malformed input produces the most favourable possible measurement.
`CONSTITUTION_DIM` is enforced only in `core/offline_normalizer.py:171` and is not
referenced by either evaluation engine.

**Why P0:** the system's sole purpose is to produce a trustworthy measurement. This defect
produces an untrustworthy one silently, today, with no normative decision required to
observe that it is wrong.

**Why it is an engineering blocker and not a normative one:** *detecting* a mismatch
requires no specification. What the system must *do* on detection (raise / sentinel /
reject upstream) is normative (`REQ-002-031`) — so the engineering-only portion is
detection and refusal-to-silently-proceed, which is separable.

### P0-2 — No input validation at the measurement boundary

**Component:** `core/evaluator.py:20-24, 51`
**Determinism ref:** D-6, D-4

`PoCAEvaluator` accepts any list, any magnitude, any element type. Measured consequences:
- floats accepted (`demo.py` does this in production-shaped code);
- un-normalized input yields `ari = 310000`, i.e. 3.1× the documented maximum;
- `ConsistencyCalculator` **rejects** the same input with `ValueError`.

Two engines implementing one formula with opposite validation postures is an engineering
defect regardless of which posture is correct.

**Why P0:** an out-of-contract value silently enters every downstream artefact
(certificate, fingerprint) and would only be caught at the database CHECK constraint —
which no writer reaches.

### P0-3 — Two divergent implementations of the same formula

**Component:** `core/evaluator.py` + `compliance/evaluator_wrapper.py` **vs**
`compliance/consistency.py`

Documented divergences (`01_CORE_INVENTORY.md` §2.7): magnitude validation, zero-vector
handling, upper clamp, **penalty model** (`150000` threshold-penalty vs
`10000 × violations`), and halt semantics (raise vs status field).

`docs/GAP-001.md` GAP-C5 records this as *"LARGELY RESOLVED"*. **It is not.** Same event,
two engines, different answer.

**Why P0:** a measurement instrument that yields two different values for one input cannot
be relied upon, and there is no statement anywhere of which engine is authoritative.

### P0-4 — No evidence is persisted; the evidence chain is not connected

**Component:** repo-wide (`02_RUNTIME_DATAFLOW.md` §7)

- No production module connects an evaluation result to `audit/merkle.py`.
- No production module writes to `audit_events`; grep for `psycopg|asyncpg|sqlalchemy`
  in non-test `*.py` → **0 hits**.
- The only composition of evaluation → Merkle → certificate exists **inside
  `test_compliance.py`**, which CI does not run.
- `init.sql`'s append-only trigger and CHECK constraints protect a table nothing writes.

**Why P0:** a regulatory measurement instrument with no persisted, verifiable record
produces no evidence. This is independent of every normative question.

### P0-5 — `core/merkle.py` "proof" proves nothing, and is what the demo path uses

**Component:** `core/merkle.py:11`

`generate_etc()` returns `{"proof": [leaf]}` — the leaf itself. There is no root and
nothing to verify against. `demo.py`, `core/test_ari.py:185` and `core/test_integration.py`
all use this placeholder rather than the real `audit/merkle.py`.

The tests assert the placeholder's *shape*, which makes it appear covered.

**Why P0:** an artefact named "Event Trust Certificate" that carries no verifiable proof
is an integrity misrepresentation if it ever reaches a consumer.

### P0-6 — Aura-Guard: `violations` are outside all integrity coverage

**Component:** `aura-guard-v1.3/src/chain.rs:26-47`, `src/segment.rs:67`
**Guard ref:** G-1

The chain digest covers nine fields; `violations` is not one of them. Segment Merkle
leaves are built over `chain_hash` values, so the segment layer inherits the gap. An
operator can rewrite the rule IDs, actions and confidence scores in `audit.jsonl` and
`aura-replay` still reports `CHAIN OK`.

**Why P0:** the violations array is the substantive content of a compliance finding. The
README's tamper-detection claim does not hold for it.

**Note:** changing the digest is a format-breaking change and needs approval — but the
approval needed is a *product* decision about the log format, **not** a Constitution
decision. It is not gated by DR-002 / SPEC-002.

---

## 2. P1 — Should Be Resolved Before Integration

*"Integration" means: before Core and Guard, or Core and any second implementation, are
wired together in any of the ways described in `03_LANGUAGE_BOUNDARY.md` §4.*

### P1-1 — The evaluation path has zero cross-platform coverage

`scripts/generate_determinism_report.py:38-40` imports `core.offline_normalizer`,
`audit.merkle`, `audit.signing` — **not** `core.evaluator`. Despite the vector name
`ari_vector_hash`, **no ARI is computed in CI**. `core/test_bitwise_replay.py` never
imports `PoCAEvaluator` either.

The one pipeline built to detect cross-platform divergence does not observe the subsystem
where D-1, D-3, D-4 and D-5 live.

### P1-2 — Zero tests for mismatched lengths, malformed input, or bounds

`05_TEST_MATRIX.md` §3: no test anywhere passes differing-length sequences to any
similarity function; no test asserts an upper bound on `ari` or `drift`; no test covers
non-integer, `None`, or empty vectors into the evaluator; `compliance/` has no unit-test
module at all.

### P1-3 — `drift` violates its own documented range

`core/evaluator.py:88` docstring says clamp to `[0, 100000]`; `:89` clamps to `200000`.
Measured `drift = 200000` and `drift = 100001`. `compliance/certificate.py` then presents
these as `2.0` and `1.00001` on a field documented as a `[0.0, 1.0]` ratio. (D-5 — a pure
engineering bug; no normative input needed.)

### P1-4 — Three JSON canonicalizations for hash inputs

`audit/merkle.py:89` uses compact separators; `compliance/certificate.py:69` and
`core/merkle.py:8` use defaults. The same object hashed through two paths gives two
hashes. (D-7. The *correct* canonical form is normative — `AD-CA-008` — but the
*inconsistency* is engineering.)

### P1-5 — `demo.py` crashes; CI never runs it

`demo.py:66,97` catch `AssertionError`; `compliance/policy.py:27` raises `ValueError`.
The process aborts at DEMO 2. It also feeds float vectors into the int32 engine and
formats int32 outputs with `:.4f`. Executed and reproduced this session.

### P1-6 — Unit tests are not run by CI

CI runs `run_all_checks.sh` (which invokes only `core/test_bitwise_replay.py` via CHECK 1)
plus one pytest selector for two WASM-compat tests. `audit/test_audit.py` (47 tests),
`core/test_ari.py`, `core/test_offline_normalizer.py`, `core/test_integration.py` and
`test_compliance.py` are **never invoked by CI**. 105 locally-passing tests are not
gating anything.

### P1-7 — `test_compliance.py` is not collectible

Module-level `def test_*()` functions are not collected by `unittest discover`, and CI
never invokes the file directly. Four passing compliance tests run only when a human types
the command.

### P1-8 — No linting, formatting, typing, coverage, or dependency audit in core CI

Absent from `aura-poc-a-core-v3.3`: ruff/flake8, black, mypy, coverage gate, `pip-audit`,
SBOM, CodeQL. Present in **both** Aura-Guard's CI (6 jobs incl. `cargo audit`,
`cargo deny`, CycloneDX) **and** the Conformance Kit's CI (`ruff format --check`,
`ruff check`, `mypy --strict`). The core repository has the weakest CI of the three.

### P1-9 — Aura-Guard CI is single-platform

`ci.yml` runs on `ubuntu-latest` only. No arm64, no macOS, no Windows, and no
cross-platform comparison of the chain digest — while the far less mature Python core does
have an arm64 leg.

### P1-10 — `packages/` is unbuildable

`VectorRepository.ts` has no `package.json`, no `tsconfig.json`, no lockfile, no build, no
test, no importer. `zk-passport/*.circom` has no toolchain, no CI, and a
`TEST_SPECIFICATION.md` describing tests that do not exist as executable artefacts. Both
are inside `PROTECTED_PATHS` of the purity scanner, which parses `.py` only and therefore
never examines them.

### P1-11 — Configuration divergence

`docker-compose.yml` (`pgvector/pgvector:pg16`, DB `aura_core`, healthcheck, mounts
`init.sql`) vs `infra/docker-compose.yml` (`ankane/pgvector:v0.7.0`, DB `aura_sandbox`,
default password `cathedral_secure`, no healthcheck, no `init.sql`). The `infra/` file is
referenced by nothing. Recorded in `docs/GAP-001.md` GAP-L5 as a credential issue; the
divergence itself is unrecorded.

### P1-12 — Schema/code dimension mismatch

`init.sql:96` declares `embedding vector(32)`; `core/offline_normalizer.py:44` declares
`CONSTITUTION_DIM = 1536`. 48× apart. No test compares them (the DB tests never touch
`agent_constitutions`).

### P1-13 — `certificate_schema.json` is unused and does not match the emitted certificate

Zero code references. Its fields (`certificate_id`, `agent.constitution_hash`, `signature`,
`ari.formula`, `ari.status`) are not produced by `AuraEventCertificate.to_dict()`, and
`schema_version` differs (`"1.0"` vs `"1.0.0"`). A stale schema is worse than no schema.

### P1-14 — Aura-Guard: `f32` in the evidence record

`Violation.confidence: f32` is serialized to the JSONL log. Harmless while G-1 stands
(it is not hashed); becomes a cross-platform float-formatting determinism surface the
moment `violations` is added to the digest. The two must be considered together.

---

## 3. P2 — Improvement / Hardening

| ID | Item | Location |
|---|---|---|
| P2-1 | `SA` computed twice per evaluation on identical inputs | `compliance/evaluator_wrapper.py:63` + inside `evaluate()` |
| P2-2 | Scale `10^5` and weights `30000/70000` declared independently in 4 / 2 modules | no shared constants module |
| P2-3 | `core/__init__.__all__` lists two deprecated shims and the placeholder embedder, omits `evaluator` | `core/__init__.py:2` |
| P2-4 | `compliance/renderer.py` has zero callers and zero tests | |
| P2-5 | `core/embedding.py` placeholder still importable from a package `__all__` | already GAP-M4 |
| P2-6 | `datetime.utcnow()` (deprecated in 3.12) and outside CHECK 5's grep scope | `compliance/policy.py:88,113,123` |
| P2-7 | CHECK 2 is a lexical grep — cannot see float *values*, float-producing `/`, or floats arriving as arguments; `demo.py` is outside its path scope | `scripts/checks/check_2_integer_only.sh` |
| P2-8 | CHECK 4 verifies file existence and name substrings; executes no audit path | `scripts/checks/check_4_audit_path.sh` |
| P2-9 | CHECK 1 prints "PASSED" unconditionally and delegates the actual cross-platform comparison to a human instruction block | `scripts/checks/check_1_bit_identity.sh` |
| P2-10 | `wasm-compat` job executes no WASM; the workflow says so itself | `.github/workflows/execution-checks.yml:83-85` |
| P2-11 | CI triggers on a `develop` branch that does not exist | `.github/workflows/execution-checks.yml:5,7` |
| P2-12 | No dependency pinning; `pyproject.toml` declares zero dependencies while tests require Docker and CI installs `pytest` ad hoc | |
| P2-13 | No observability of any kind in core (no logging, no metrics, no tracing) — Guard has full `tracing` + Prometheus | |
| P2-14 | No performance benchmark anywhere; the 1536-dim dot product is O(n) Python with a generator expression | |
| P2-15 | Merkle leaf concatenation `sha256(left + right)` has no domain separation, unlike Guard's RFC 6962 `0x00`/`0x01` prefixes | `audit/merkle.py:157` |
| P2-16 | `HALTED_AGENTS` is never cleared outside tests; unbounded process-lifetime growth | `compliance/policy.py:29` |
| P2-17 | `PolicyRule.is_violated` swallows all exceptions and returns `True` (fail-closed) with an untested stderr print | `compliance/policy.py:79-88` |
| P2-18 | Guard: `AURA_AUTH_DISABLED=true` disables both auth and signature enforcement via a single env var | `aura-guard/src/auth.rs`, `src/policy.rs:7-8` |
| P2-19 | Guard: crate version `1.3.0` while ROADMAP lists shipped v1.4 features that are present in source | `Cargo.toml:3`, `docs/ROADMAP.md` |
| P2-20 | Conformance Kit: `python-package.yml` duplicates `ci.yml` with a looser, unreviewed stock toolchain (`flake8`, undeclared dependency) | kit `.github/workflows/` |
| P2-21 | Conformance Kit: three CI systems (Actions ×3, CircleCI) for one `assert True` | |
| P2-22 | `docs/LEGACY_PROTOCOL.md` empty (already GAP-L1) | |

---

## 4. NORMATIVE BLOCKERS — Decisions Only Governance May Take

**No priority is assigned.** These are not engineering items and must not be scheduled as
such. Listed for completeness of the baseline and to make explicit what the engineering
items above do *not* depend on.

| ID | Decision domain | Tracked as | Blocks |
|---|---|---|---|
| NB-000 | **What `DR-002` refers to, and its relationship to `AD-CA-001…012`** | *untracked in any repository* | the mapping between the governance conversation and the specification's own decision register |
| NB-001 | **Which `aura-specification` repository is authoritative** — `AuraIDToken/` (full APS set) or `aura-nomos/` (README only) | untracked | every downstream citation, incl. this package's own references |
| NB-002 | **Which Conformance Kit repository is authoritative** — `Aura-Conformance-Kit` (active) or `Aura-Conformance-Kits` (archived, byte-identical source) | untracked | all conformance work |
| NB-003 | Authoritative Constitution source identity, Source Set, Source Boundary | `AD-CA-001` | `REQ-002-001` … `-011` |
| NB-004 | Canonicalization procedure for the Constitution source | `AD-CA-002` | `REQ-002-007, -010, -011` |
| NB-005 | Transformation pipeline source → artifact | `AD-CA-003` | `REQ-002-010, -011` |
| NB-006 | Normalization rules affecting deterministic output | `AD-CA-004` | `REQ-002-011, -021, -022` |
| NB-007 | Embedding method identity and versioning | `AD-CA-005` | `REQ-002-012, -016, -024` |
| NB-008 | Dictionary identity, versioning, integrity, dependency closure | `AD-CA-006` | `REQ-002-013, -016, -024, -034` |
| NB-009 | **Numeric representation of vector values** (dimension, scale, signedness, endianness, **rounding rule**) | `AD-CA-007` | `REQ-002-014, -017` … `-022`. **Governs D-1, D-2, D-4.** |
| NB-010 | Canonical serialization format, canonical byte sequence, hash domains | `AD-CA-008` | `REQ-002-017` … `-022`. **Governs D-7.** |
| NB-011 | Document / Artifact / Vector identity schema and inter-identity binding | `AD-CA-009` | `REQ-002-015, -016, -023, -024` |
| NB-012 | Commit/execution provenance binding | `AD-CA-010` | `REQ-002-025, -030, -031, -033` |
| NB-013 | Registration model and registry integrity | `AD-CA-011` | `REQ-002-028, -030, -031` |
| NB-014 | Freeze evidence and immutability semantics | `AD-CA-012` | `REQ-002-029` … `-031` |
| NB-015 | **Required failure conditions / failure modes on malformed input** | `REQ-002-031` (unresolved) | the *required* behaviour behind P0-1 and P0-2 |
| NB-016 | Integer-division semantics for negative dividends at the rescale step | **not listed in any AD-CA candidate set** | D-1 |
| NB-017 | Which of the two ARI engines is authoritative, and which penalty model applies | untracked | the *choice* behind P0-3 (the *divergence* is engineering) |
| NB-018 | Whether Merkle construction is RFC 6962 or the duplication variant | untracked | D-8; any cross-implementation proof verification |
| NB-019 | Whether Art. 14 halt state must be durable / distributed rather than process-local | untracked | `compliance/policy.py:29` posture; AGENTS.md rule 5 is a rule about *claims*, not about required architecture |
| NB-020 | Whether Core and Guard are one system or two products, and whether an integration boundary is wanted at all | untracked | `03_LANGUAGE_BOUNDARY.md` §4 option selection |
| NB-021 | **Whether the self-declared v3.3 FROZEN status permits defect correction** (P0-1 … P0-5, P1-3, P1-5) without a lineage bump | untracked; the tension is noted in the spec repo's own `reference/RI-PY_AURA_POC_A_CORE.md` | every code-touching item in `09_SAFE_WORK.md` §1.3 and §1.5 |

---

## 5. The Boundary Between the Two Lists

Several P0/P1 items sit adjacent to a normative blocker. The split is made on this test:
**can an engineer act without choosing a protocol semantic?**

| Item | Engineering portion (actionable) | Normative portion (blocked) |
|---|---|---|
| P0-1 (`zip`) | detect the mismatch; stop returning a maximal score for malformed input; test the current behaviour | what the system must *do* — raise, sentinel, or reject upstream → NB-015 |
| P0-2 (validation) | observe and record that two engines disagree; add characterization tests | which posture is required → NB-015 |
| P0-3 (two engines) | the divergence is a defect regardless | which engine is authoritative → NB-017 |
| P1-3 (`drift`) | **fully actionable** — code contradicts its own docstring | none |
| P1-4 (canonicalization) | record that three forms exist and differ | which form is canonical → NB-010 |
| D-1 / D-2 | document the language-dependence; add characterization tests | which rule is correct → NB-009 / NB-016 |
| P0-6 (Guard violations) | **fully actionable as a product decision** | none from the Constitution domain |

**Nothing in §1–§3 requires resolving DR-002 or any AD-CA decision to be *understood*.**
A subset requires one to be *finally settled*. That subset is marked above and carried
into `09_SAFE_WORK.md`.
