# 05 — TEST MATRIX (TASK 5)

**Constraint honoured:** no fixtures were created. Nothing in this document proposes a
test whose expected value would depend on an unresolved normative choice; where a gap can
only be closed by first making such a choice, it is marked **GOVERNANCE-GATED**.

---

## 1. Executed Baseline

```
$ python3 -m unittest discover -s . -p "test_*.py"
Ran 107 tests in 0.649s
FAILED (errors=2)
```

Both errors are `setUpClass` Docker-unavailability errors, not code failures:
`audit.test_audit_db_integration` and `core.test_cr003_statelessness`.
**105 tests pass; 2 are environment-gated and did not run.**

```
$ python3 test_compliance.py
Total: 4/4 tests passed          # separate runner; NOT collected by discovery, NOT in CI
```

```
$ python3 demo.py
DEMO 1 completes with ARI 0.0000 / Drift 100000.0000
DEMO 2 → uncaught ValueError, process aborts       # demo.py is not run by CI
```

Local check scripts (x86_64, Python 3.11.15): CHECK 0–6 all PASS. CHECK 7–9 require
Docker and were **not executed**.

---

## 2. Component → Test Mapping

Columns: what the test file actually asserts, and what it demonstrably does not.

### 2.1 `core/evaluator.py` — `PoCAEvaluator`

| Test | What IS verified | What is NOT verified |
|---|---|---|
| `core/test_ari.py::TestLayerSeparation` (3 tests, `:60-84`) | `evaluate()` returns exactly `{"ari","drift"}`; no key from a 12-item prohibited set; both values are `int` | anything numeric |
| `test_ari_calculation_basic` (`:112`) | `ari ∈ [0, 100000]` for one aligned 10-dim input | any exact value |
| `test_ari_calculation_perfect_alignment` (`:127`) | `ari > 95000`, `drift < 5000` | exact value; upper bound on `ari`; that `drift` cannot exceed 100000 |
| `test_ari_calculation_invalid_schema` (`:140`) | `ari < 100000` when `valid_schema=False` | that `ari == 0.7*SA`; the SI=0 branch value |
| `test_ari_penalty_for_drift` (`:153`) | via `evaluate_with_policy`: `drift > 30000`, `ari ≤ 50000` for an anti-aligned vector | the penalty value (150000); the threshold (68000); that `max(0, …)` clamps |
| `test_cosine_similarity_calculation` (`:214`) | aligned `> 90000`; orthogonal `≈ 0 ± 1000`; opposite `< -90000` | **exact values** — so D-1 (floor vs truncate, a 1-LSB difference) passes either way |
| `test_ari_bounds` (`:237`) | `ari ∈ [0, 100000]` for one *normalized* extreme input | that the bound holds for **un-normalized** input — measured `310000`, D-4 |
| `core/test_integration.py::test_complete_workflow` (`:40`) | full Fragment-B call returns `ari > 80000` and an ETC-shaped dict | any exact value; any serialization |
| `core/test_cr003_statelessness.py::test_history_independence` (`:218`) | `evaluate()` output is byte-identical with an empty vs. a populated `audit_events` table | anything about the values themselves; **Docker-gated** |

**Not verified anywhere for this component:**
- length mismatch between `vector` and `constitution` (**D-3, ACTIVE bug**)
- un-normalized / out-of-scale input (**D-6**)
- `None`, empty list, non-integer elements, `NaN`
- `drift` upper bound (**D-5, ACTIVE bug**)
- accumulator width (**D-4**)
- exact `SA` for negative dot products (**D-1**)
- **cross-platform reproduction of any evaluator output** (see §5)

### 2.2 `core/offline_normalizer.py`

| Test | What IS verified | What is NOT verified |
|---|---|---|
| `test_normalize_vector_simple/_already_unit` (`:36,:51`) | L2 norm ≈ 1.0 after normalization | float determinism across platforms |
| `test_normalize_vector_zero_raises_error` (`:60`) | `ValueError` on zero vector | other degenerate inputs (`inf`, `NaN`, empty) |
| `test_scale_to_fixed_point_*` (4 tests, `:69-107`) | scaling by 10^5; negatives; **current rounding behaviour** | that the rounding rule is the *required* one — **GOVERNANCE-GATED (AD-CA-007)**; behaviour at negative `.5` boundaries |
| `test_verify_unit_vector_*` (3 tests, `:109-128`) | 1 % tolerance band accept/reject | that 1 % is the correct tolerance |
| `test_normalize_constitution_vector_wrong_dimension` (`:142`) | `ValueError` when `len != 1536` | — (this is the repo's **only** dimension test) |
| `test_normalize_constitution_vector_determinism` (`:151`) | same input → same output, same process | same input → same output across processes/platforms/interpreters |
| `test_*_file_io*` (2 tests, `:164,:200`) | round-trip through JSON, both bare-list and `{"vector": …}` forms | malformed JSON; missing keys; wrong types; oversized files |
| `TestEdgeCases` (3 tests, `:307-333`) | very small / very large / mixed-sign values normalize | overflow of the float sum in `magnitude` |

**Not verified:** float `NaN`/`inf` inputs; non-numeric elements; concurrent writes;
that the emitted JSON is canonical in any sense.

### 2.3 `compliance/consistency.py` — `ConsistencyCalculator`

| Test | What IS verified | What is NOT verified |
|---|---|---|
| `test_compliance.py::test_art14_kill_switch` (`:114`) | halted → `{"status":"HALTED"}`; resumes after deactivate; score `100000` on the happy path | **not run by CI** |
| `test_compliance.py::test_integrated_poca_flow` (`:191`) | score `100000` end-to-end with placeholder embeddings | **not run by CI** |

**There is no dedicated unit-test module for `compliance/`.** Specifically **not
verified**: the `ValueError` magnitude guards (`:85`,`:88`), the zero-vector guard
(`:82`), the upper clamp (`:62`), the `VIOLATION_PENALTY` arithmetic (`:99`), length
mismatch (**D-3**), and the divergence from `PoCAEvaluator` (**D-6**).

`docs/GAP-001.md` GAP-M5 already records "Audit and Compliance Layer Test Coverage" as a
gap. This audit confirms it is unchanged for `compliance/` and **no longer true** for
`audit/` (which now has 47 tests).

### 2.4 `compliance/policy.py`

| Test | What IS verified | What is NOT verified |
|---|---|---|
| `core/test_ari.py:97,104` | `validate_target` raises on `"HUMAN"`, passes on `"MACHINE_ACCOUNT"` | other values; case sensitivity; `None` |
| `core/test_ari.py:169`, `core/test_integration.py:70` | `POLICY_HALT` raised for a halted agent | that halt state is durable, shared, or restored |
| `scripts/art5_conformance_proof.py` (CHECK 6, ×3 opt levels) | the Art. 5 guard is not an `assert` and survives `-O`/`-OO` | — |
| `test_compliance.py:18,114` | `PolicyRule` callable enforcement; `KillSwitch` lifecycle | **not run by CI** |

**Not verified:** `calculate_penalties` boundary at exactly `sa == 68000`;
`DRIFT_PENALTY = 150000` exceeding the maximum possible `RAW_ARI` of `100000` (so any
drift penalty always floors `ari` to 0 — a semantic observation, untested);
`PolicyRule.is_violated`'s broad `except` returning `True` (fail-closed) — untested;
`HALTED_AGENTS` never being cleared except by tests.

### 2.5 `compliance/certificate.py`, `renderer.py`

| Test | What IS verified | What is NOT verified |
|---|---|---|
| `test_compliance.py:191` | a certificate is constructible and `fingerprint()` returns a hex string | **not run by CI** |

**`compliance/renderer.py` has zero test coverage and zero callers.**
`compliance/certificate_schema.json` has zero validators — and does not match the
certificate the code emits (`01_CORE_INVENTORY.md` §8).

### 2.6 `audit/` — the best-covered subsystem

| Test class | Tests | What IS verified |
|---|---|---|
| `TestHMACSigner` (`:59`) | 6 | determinism; 32-byte length; payload/key sensitivity; non-bytes key rejected |
| `TestHMACVerifier` (`:92`) | 5 | correct/wrong signature, wrong key, modified payload, key type |
| `TestCanonicalSha256` (`:127`) | 3 | known-answer hashes; call stability; UTF-8 encoding |
| `TestMerkleTree` (`:170`) | 6 | single leaf; root determinism; distinct roots; **odd-leaf duplication**; empty raises; pre-hashed leaves |
| `TestMerkleProof` (`:208`) | 5 | all proofs valid; wrong root; wrong leaf; tampered step; out-of-range index |
| `TestEventTrustCertificate` (`:247`) | 9 | verify; dict keys; serialization stability; three tamper cases; no-signature default |
| `TestETCSigning` (`:303`) | 11 | immutability of `sign()`; validity; key mismatch; tamper; payload determinism |
| `TestCombinedVerification` (`:368`) | 2 | signed and unsigned ETCs verify |
| `TestAuditDeterminism` (`:390`) | 6 | event hash, root, proof, HMAC, UTF-8 payload stability; platform info recorded |

**47 tests.** Includes genuine negative and tamper tests — the only subsystem where these
exist.

**Not verified even here:** proof length bounds; very large trees; leaves containing the
concatenation separator (the construction is `sha256(left + right)` with no domain
separation — a second-preimage consideration, untested); cross-implementation agreement
with any RFC 6962 implementation (**D-8**).

### 2.7 `core/merkle.py` — `MerkleAttestor` (placeholder)

| Test | What IS verified | What is NOT verified |
|---|---|---|
| `core/test_ari.py:185` | `certificate` starts with `"AURA-ETC-"`; `proof` is a non-empty list | **that the "proof" proves anything** — it is the leaf itself |
| `core/test_ari.py:203` | leaf generation is deterministic | — |

The tests assert the placeholder's shape, which makes the placeholder look tested. It is
not verified against any root because there is no root.

### 2.8 Persistence

| Test | What IS verified | Gate |
|---|---|---|
| `audit/test_audit_db_integration.py::test_append_only_enforcement` (`:179`) | `UPDATE`/`DELETE` on `audit_events` are rejected by the trigger; the `RAW_ARI` CHECK constraints reject non-integer and out-of-range values; the `poca_score` derivation constraint rejects mismatches | **Docker** |
| `core/test_cr003_statelessness.py::test_history_independence` (`:218`) | Layer-0 output is unchanged by populated history | **Docker** |

Both are real integration tests against a live PostgreSQL. Both were **not executed here**
(no Docker socket). Neither exercises any application persistence code, because none
exists — they drive `psql` directly.

### 2.9 Cross-platform / determinism

| Test | What IS verified | What is NOT verified |
|---|---|---|
| `core/test_bitwise_replay.py` (8 tests) | inline int arithmetic; a fixed reference SHA-256 of `45000`; LE-byte determinism; hashing of the sample constitution vector; intra-process replay of an inline weighted sum | **`PoCAEvaluator` is never imported.** No evaluator output is hashed, replayed, or compared. |
| `WASMCompatibilityTest` (2 tests) | that `+ - * // & | ^` on Python ints give expected literals; that two literals are within i32 range | **nothing WASM.** No WASM runtime is invoked. The workflow comment concedes this (`.github/workflows/execution-checks.yml:83-85`). |
| `scripts/compare_determinism_reports.py` (CI job) | 5 hex vectors identical between x86_64 and arm64 | see §5 |

---

## 3. Test-Category Inventory

### Deterministic tests — PRESENT, partial

`core/test_bitwise_replay.py` (8), `audit/test_audit.py::TestAuditDeterminism` (6),
`core/test_offline_normalizer.py::test_*_determinism` (2), plus the CI comparison job.

**Scope limit:** all of them cover hashing, byte encoding, and the offline normalizer.
**None covers the evaluation arithmetic.**

### Cross-platform tests — PRESENT, narrow

Real: the `execution-checks` matrix (x86_64 + arm64) plus `compare-determinism`.
Limits: 2 architectures, 1 OS, 1 interpreter, 1 Python version, 5 vectors, **0 evaluator
coverage**, 0 WASM execution.

### Negative tests — PRESENT only in `audit/`

| Location | Count | Examples |
|---|---|---|
| `audit/test_audit.py` | ~14 | wrong root, wrong leaf, tampered proof step, wrong key, modified payload, out-of-range index, empty leaves |
| `core/test_offline_normalizer.py` | 2 | zero vector, wrong dimension |
| `core/test_ari.py` | 2 | `validate_target("HUMAN")`, halted agent |
| `compliance/` | **0** | — |
| `core/evaluator.py` | **0** | — |

### Malformed-input tests — LARGELY ABSENT

| Input class | Covered? |
|---|---|
| Wrong-dimension vector into the normalizer | YES (`:142`) |
| Wrong-dimension vector into the **evaluator** | **NO** (D-3) |
| Non-integer elements | NO |
| `None` / empty vector into the evaluator | NO |
| Out-of-scale magnitudes into the evaluator | NO (D-6) |
| Malformed JSON into the normalizer | NO |
| Missing event keys | YES, indirectly (`compliance/consistency.py:76`, exercised in `test_compliance.py` — not in CI) |
| Non-bytes key into signer | YES (`audit/test_audit.py:87,118`) |

### Length-mismatch tests — **ABSENT**

Zero tests anywhere pass differing-length sequences to any similarity function. This is
the single most consequential coverage gap, because the behaviour is silent and
fail-open (D-3).

### Overflow tests — ABSENT

`core/test_bitwise_replay.py:377-379` range-checks two **literals**, not any computed
value. No test observes the ~1.5×10¹³ accumulator, no test asserts an upper bound on
`ari` for un-normalized input, and no test would fail if the accumulator exceeded any
width (D-4).

### Serialization tests — PARTIAL

Covered: `EventTrustCertificate.to_dict()` key set and stability
(`audit/test_audit.py:263,268`); signing-payload determinism (`:349,428`); normalizer JSON
round-trip.
Not covered: `AuraEventCertificate.to_dict()`/`fingerprint()` in CI; **any comparison
between the three JSON canonicalizations** (D-7); `render_certificate` in any form; any
canonical byte sequence for a vector outside test code.

### Hash tests — PRESENT and strong

Known-answer SHA-256 (`audit/test_audit.py:148`), stability, UTF-8 sensitivity, HMAC
determinism and length, tamper detection, plus the fixed reference hash in
`core/test_bitwise_replay.py:213`.

---

## 4. Coverage Heat Map

| Component | Unit | Negative | Malformed | Cross-platform | In CI |
|---|:--:|:--:|:--:|:--:|:--:|
| `audit/merkle.py` | ●●● | ●●● | ●● | ●●● | ●●● |
| `audit/signing.py` | ●●● | ●●● | ●● | ●●● | ●●● |
| `core/offline_normalizer.py` | ●●● | ●● | ● | ●●● | ●●● |
| `core/evaluator.py` | ●● | ○ | ○ | **○** | **○** |
| `compliance/consistency.py` | ● | ○ | ○ | ○ | **○** |
| `compliance/policy.py` | ●● | ● | ○ | ○ | ●● (CHECK 6 only) |
| `compliance/certificate.py` | ● | ○ | ○ | ○ | **○** |
| `compliance/renderer.py` | ○ | ○ | ○ | ○ | ○ |
| `core/merkle.py` | ● (shape only) | ○ | ○ | ○ | ○ |
| `core/embedding.py` | ○ | ○ | ○ | ○ | ○ |
| `init.sql` | ●● | ●● | ● | ○ | ●● (Docker) |
| `packages/**` | ○ | ○ | ○ | ○ | ○ |

●●● strong · ●● moderate · ● minimal · ○ none

**The inverse relationship is the headline: the subsystem the product is named for
(ARI measurement) has the weakest coverage; the supporting audit layer has the
strongest.**

---

## 5. The Determinism-Coverage Inversion

CI's determinism job compares five vectors between architectures:

| Vector | Underlying code |
|---|---|
| `ari_vector_hash` | `core/offline_normalizer.generate_sample_constitution` |
| `canonical_event_hash` | `audit/merkle.sha256` |
| `merkle_root` | `audit/merkle.MerkleTree` |
| `etc_hash` | `audit/merkle.EventTrustCertificate.to_dict` |
| `hmac_signature_hex` | `audit/signing.HMACSigner` |

`scripts/generate_determinism_report.py` imports exactly three modules
(`:38-40`): `core.offline_normalizer`, `audit.merkle`, `audit.signing`.

**It does not import `core.evaluator`.** Despite the name `ari_vector_hash`, no ARI is
computed. The determinism pipeline verifies the parts that are already deterministic by
construction (SHA-256, HMAC) and does not verify the part where D-1, D-3, D-4 and D-5
live.

---

## 6. Gaps, Split by Whether Governance Blocks Them

### 6a. Closable without any normative decision (safe to specify now)

| Gap | Component | Note |
|---|---|---|
| Length-mismatch behaviour is unobserved | `core/evaluator.py`, `compliance/consistency.py` | A test can **pin current behaviour** (`zip` truncation) as a characterization test without asserting it is correct. |
| `drift` upper bound unasserted | `core/evaluator.py` | Code and docstring disagree; a test can pin the code's actual range (D-5). |
| `ari` upper bound unasserted for un-normalized input | `core/evaluator.py` | Same; measured `310000`. |
| Two engines diverge on the same input | `evaluator` vs `consistency` | A differential test can **record** the divergence. |
| `compliance/` has no unit-test module | `compliance/*` | Covering existing guards requires no new semantics. |
| `test_compliance.py` not collected / not in CI | repo-wide | Purely a runner/CI wiring issue. |
| `demo.py` crashes | `demo.py` | Wrong exception type caught; no test guards it. |
| `renderer.py` untested and uncalled | `compliance/renderer.py` | — |
| Three JSON canonicalizations uncompared | repo-wide | A test can **record** that they differ. |
| Accumulator width unobserved | `core/evaluator.py` | A test can record the measured magnitude. |

### 6b. GOVERNANCE-GATED (a fixture here would encode an unresolved decision)

| Gap | Gated by |
|---|---|
| Expected value of any Constitution Vector | `AD-CA-005` embedding, `AD-CA-006` dictionary, `AD-CA-007` numeric representation |
| Correct rounding rule at float→int reduction | `AD-CA-007` |
| Correct division rule for negative dividends | undefined (not even listed in `AD-CA-007`'s candidates) |
| Required failure mode on malformed input | `REQ-002-031` (failure conditions), unresolved |
| Canonical byte sequence / canonical JSON form | `AD-CA-008` |
| Cross-language conformance fixtures | all of the above |

**No fixture representing any item in 6b was created by this audit.**

---

## 7. Aura-Guard Test Position (cross-reference)

For contrast, executed this session in `aura-guard-v1.3`:

```
$ cargo test --locked --all-targets
178 passed (lib) + 32 + 10 + 9 + 9 + 2 (integration) = 240 passed; 0 failed
EXIT=0
```

Guard has **240 passing tests including 5 `proptest!` property suites**
(`src/chain.rs:426`, `src/engine.rs:305`, `src/normalizer.rs:445`,
`src/validators.rs:374`, `src/crypto.rs:248`), a checked-in proptest regression file
(`proptest-regressions/normalizer.txt`), golden tests (`tests/golden.rs`), and
fail-closed bootstrap tests (`tests/bootstrap_fail_closed.rs`).

Core has 107 tests, 0 property tests, 0 golden files, 0 fuzz targets. Details in
`06_GUARD_AUDIT.md`.
