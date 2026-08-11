# 06 — AURA-GUARD AUDIT (TASK 6)

**Repository:** `AuraIDToken/aura-guard-v1.3`, anonymous read clone at
`/workspace/auraidtoken/aura-guard-v1.3`, `main` HEAD (last push 2026-08-02).

**Method:** source read + executed build and test run. README claims were read **after**
the source and are treated as claims to be checked, not as evidence.

---

## 1. Executed Evidence

```
$ cargo test --locked --all-targets
   … full dependency build …
running 178 tests   test result: ok. 178 passed; 0 failed          (lib unit tests)
running   2 tests   test result: ok.   2 passed; 0 failed          (bootstrap_fail_closed)
running  32 tests   test result: ok.  32 passed; 0 failed          (config_validation)
running  10 tests   test result: ok.  10 passed; 0 failed          (golden)
running   9 tests   test result: ok.   9 passed; 0 failed          (integration)
running   9 tests   test result: ok.   9 passed; 0 failed          (tst_verify)
EXIT=0
```

**240 tests, all passing, on a clean checkout with `--locked`.** This is a substantially
more mature engineering artefact than `aura-poc-a-core-v3.3`.

Source size: **8,512 lines** of Rust across 25 files (`src/` 7,377; `tests/` 1,247).

---

## 2. What Aura-Guard Actually Implements

Determined from source, module by module.

| Capability | Module | Status | Source evidence |
|---|---|---|---|
| HTTP audit endpoint `POST /v1/audit` | `src/api/audit.rs:41` | **IMPLEMENTED** | axum handler, full request→entry pipeline |
| Health / ready / version / metrics endpoints | `src/api/health.rs`, `src/api/mod.rs:50` | **IMPLEMENTED** | routed, unauthenticated |
| API-key auth (`X-API-Key` or `Bearer`) | `src/auth.rs` | **IMPLEMENTED** | constant-time compare; `auth_disabled` dev bypass exists |
| Shadow normalization (SHADOW_SPEC v1.0) | `src/normalizer.rs:47` | **IMPLEMENTED** | NFKC → hidden-char strip (21 codepoints, `:21-42`) → confusable folding → lowercase |
| Regex decision engine | `src/engine.rs:14` | **IMPLEMENTED** | rule iteration in declaration order; `DENY > REVIEW > ALLOW` precedence (`:59-66`) |
| Semantic validators (Luhn / PESEL / IBAN mod-97) | `src/validators.rs` | **IMPLEMENTED** | 44 tests incl. proptest |
| Conditional (context-gated) rules | `src/engine.rs:19-24` | **IMPLEMENTED** | |
| Ed25519 policy signature verification | `src/policy.rs`, `src/crypto.rs` | **IMPLEMENTED** | `<name>.yaml.sig` + `.signer` + `trusted_signers.json` |
| Fail-closed bootstrap (exit 78) | `src/main.rs:1-14` doc, `src/api/mod.rs:29` | **IMPLEMENTED** | `EXPECTED_POLICIES` must all load+verify before the listener binds; **no lazy load path** |
| Hash-chained append-only JSONL log | `src/chain.rs:26`, `src/log_writer.rs` | **IMPLEMENTED** | `SHA-256(prev\|decision\|policy_set\|policy_hash\|context\|input_hash\|shadow_hash\|seq\|timestamp)` |
| Fail-closed log writer | `src/log_writer.rs:1-7` | **IMPLEMENTED** | single mutex; write failure sets `halted` → HTTP 503 until restart |
| RFC 6962 Merkle (domain-separated) | `src/merkle.rs:1-16` | **IMPLEMENTED** | leaf `SHA-256(0x00‖data)`, node `SHA-256(0x01‖L‖R)` |
| Segment manifests + segment chain | `src/segment.rs`, `src/sealer.rs` | **IMPLEMENTED** | atomic temp-file+rename; restart replays unsealed entries |
| Optional RFC 3161 timestamping | `src/rfc3161.rs` | **IMPLEMENTED**, opt-in, fail-open | off unless `AURA_TSA_URL` set |
| Strict offline TST verification | `src/tst_verify.rs` (1,008 lines) | **IMPLEMENTED** | RFC 5652 SignedData + PKIX chain, `signingCertificate(V2)` binding, `id-kp-timeStamping` EKU |
| CLI `aura-replay` | `src/bin/aura_replay.rs` | **IMPLEMENTED** | exit 2 chain break, 3 lineage mismatch |
| CLI `aura-seal` | `src/bin/aura_seal.rs` (518 lines) | **IMPLEMENTED** | `verify`, `verify-chain`, `proof`, `verify-tst`; exits 4/5/6 |
| CLI `aura-sign-policy` | `src/bin/aura_sign_policy.rs` | **IMPLEMENTED** | |
| Prometheus metrics | `src/metrics.rs`, counters throughout | **IMPLEMENTED** | |
| Config from env/TOML (`figment`) | `src/config.rs` | **IMPLEMENTED** | 32 dedicated validation tests |
| Deployment artefacts | `deploy/Dockerfile`, `deploy/docker-compose.yml`, `deploy/systemd/` | **IMPLEMENTED** | multi-stage distroless |
| Privacy posture | `src/api/audit.rs:101-108` | **IMPLEMENTED** | only SHA-256 of `context+prompt+response` is stored; raw text never written |

---

## 3. What Aura-Guard Does NOT Implement

These are absences established by exhaustive grep, not by omission from the README.

| Absent capability | Evidence |
|---|---|
| **Any Constitution concept** | 0 occurrences of `constitution` in `src/`, `tests/`, `Cargo.toml` |
| **Any ARI / PoCA concept** | 0 real occurrences of `ari`, `poca` (5 substring false positives in `src/validators.rs:435-439`, `src/sealer.rs:131`) |
| **Any Constitution Vector** | none |
| **Any vector arithmetic** | no dot product, no similarity, no embedding, no fixed-point scale |
| **Any integer fixed-point model** | `10^5` scaling does not appear |
| **Any Python interface** | no `pyo3`, no `cdylib`, no `build.rs`, no FFI; `unsafe_code = "forbid"` (`Cargo.toml:104`) |
| **Any zero-float policy** | `f32` is used for rule confidence (`src/models.rs:38`, `src/policy.rs:41,94`) and `f64` for latency (`src/api/audit.rs:191`) |
| **APS-400 conformance runner** | none; confirmed by the spec repo's own `RI-RS_AURA_GUARD.md` ("RI-004 ❌ MISSING") |
| **APS-500 fixture loader** | `tests/fixtures/tsa/` exists but is TSA-specific, not APS-500 |
| **APS-200 canonical object headers** | JSON DTOs are ad-hoc (`src/models.rs`) |
| **Interoperability with `aura-poc-a-core`** | no shared format, hash rule, fixture, constant or schema |

---

## 4. README Claims Checked Against Source

Per the task instruction, README claims were verified rather than accepted.

| README claim | Verdict | Evidence |
|---|---|---|
| "No external ML dependency, no cloud control plane, no telemetry in the deterministic core" | **CONFIRMED** | `Cargo.toml` has no ML crate; the only outbound HTTP is `ureq` used solely by the opt-in TSA path (`src/rfc3161.rs`) |
| "Hash-chained audit log … any byte-level mutation is detected by `aura-replay`" | **QUALIFIED — see §5** | true for the nine fields in the digest; **the `violations` array is not among them** |
| "Same `(input, policy)` always produces the same `(decision, chain_hash)`" | **HALF-CONFIRMED** | `decision` is deterministic (`src/engine.rs:14`, no clock/RNG/IO). `chain_hash` is **not** reproducible from `(input, policy)` alone: it incorporates `seq` and `timestamp = Utc::now()` (`src/api/audit.rs:117-118`). The claim as written overstates what the code does. |
| "Signed policies … loader fails closed on missing or invalid signatures" | **CONFIRMED** | `src/policy.rs`; overridable only via `AURA_AUTH_DISABLED=true` dev flag, which is documented |
| "Fail-closed startup … exit code 78 before binding the listener" | **CONFIRMED** | `src/main.rs` doc-comment contract; `tests/bootstrap_fail_closed.rs` (2 tests) exercises it |
| "Privacy by design. Raw prompt/response text is never written to the audit log" | **CONFIRMED** | `AuditEntry` (`src/models.rs:50`) has no prompt/response field; only `input_hash`/`shadow_hash` |
| "Merkle batching (RFC 6962)" | **CONFIRMED** | domain-separated leaf/node prefixes, `src/merkle.rs:9-11` |
| "21 unit + 2 bootstrap + 10 golden + 6 HTTP integration tests" (ROADMAP v1.3 line) | **STALE** | actual: 240 tests. The ROADMAP text describes an earlier state. |

**Version-labelling observation:** the repository is named `aura-guard-v1.3` and
`Cargo.toml:3` declares `version = "1.3.0"`, but `docs/ROADMAP.md` lists Merkle batching,
segment chains, `aura-seal` and RFC 3161 under **"Shipped in v1.4"**, and those features
are present in the source. The crate version does not reflect the shipped feature set.
Recorded as an AS-IS inconsistency.

---

## 5. Engineering Findings

### G-1 — `violations` are outside all integrity coverage — **P1**

`compute_chain_hash` (`src/chain.rs:26-47`) digests exactly nine fields:
`prev_hash, decision, policy_set, policy_hash, context, input_hash, shadow_hash, seq,
timestamp`.

The `violations: Vec<Violation>` field of `AuditEntry` (`src/models.rs:87`) is **not**
among them. `recompute_for_entry` (`src/chain.rs:52`) likewise reads only those nine
fields, and `src/bin/aura_replay.rs` verifies only the chain. Segment Merkle leaves are
built over `chain_hash` values (`src/segment.rs:6,67`), so the segment layer inherits the
same coverage.

**Consequence:** an operator with write access to `logs/audit.jsonl` can alter, remove or
insert entries in the `violations` array — the rule IDs, actions, confidence scores and
validator labels that constitute the *substance* of a compliance finding — and
`aura-replay` will still report `CHAIN OK`.

This is not hypothetical or normative; it is a direct consequence of the field list. The
README's tamper-detection claim is therefore accurate for the decision and its inputs, and
inaccurate for the evidence detail.

**Not fixed.** Any change here alters the chain digest and is therefore a format-breaking
change requiring approval.

### G-2 — `chain_hash` is not reproducible from inputs — **P2 (documentation)**

`timestamp` (`Utc::now()`) and `seq` (monotonic server counter) enter the digest. Two
identical requests produce different `chain_hash` values. This is a reasonable design for
an append-only log — the chain proves *sequence integrity*, not *input reproducibility* —
but the README's determinism sentence conflates the two.

`audit_id` is a `Uuid::new_v4()` (`src/api/audit.rs:52`) — genuinely random, and correctly
**excluded** from the digest.

### G-3 — Float in the recorded evidence — **P2**

`Violation.confidence: f32` (`src/models.rs:38`) is serialized into the JSONL log. Because
of G-1 it is not hashed, so it cannot currently cause a chain divergence. If G-1 were
addressed by adding `violations` to the digest, `f32` serialization would become a
cross-platform determinism concern (shortest-roundtrip float formatting differs between
implementations).

Recorded together because fixing one without considering the other would introduce a new
determinism surface.

### G-4 — Dev bypasses exist and are reachable by env var — **P2**

`AURA_AUTH_DISABLED=true` disables both API-key auth (`src/auth.rs`) and policy-signature
enforcement (`src/policy.rs:7-8`). Both are documented as development-only. There is no
runtime assertion preventing this in a production build; the mitigation is operational
(config review), not technical.

### G-5 — Time-based sealing means log-to-manifest lag is unbounded on a quiet server — **P2**

`SegmentSealer` closes on entry count **or** elapsed interval (`src/sealer.rs:9-12`).
Entries written after the last seal and before the next are chained but not yet
Merkle-anchored. Restart replays them (`src/sealer.rs:6-8`), which is correct. Recorded as
an operational property, not a defect.

---

## 6. Tests

| Suite | Tests | Character |
|---|---|---|
| `src/validators.rs` | 44 | unit + `proptest!` (`:374`) |
| `src/normalizer.rs` | 40 | unit + `proptest!` (`:445`); has a checked-in regression file `proptest-regressions/normalizer.txt` |
| `tests/config_validation.rs` | 32 | config matrix |
| `src/crypto.rs` | 27 | unit + `proptest!` (`:248`) |
| `src/engine.rs` | 24 | unit + `proptest!` (`:305`) |
| `src/chain.rs` | 20 | unit + `proptest!` (`:426`) |
| `tests/golden.rs` | 10 | golden/regression |
| `tests/tst_verify.rs` | 9 | RFC 3161 verification against checked-in fixtures |
| `tests/integration.rs` | 9 | HTTP end-to-end |
| `src/merkle.rs` | 9 | RFC 6962 |
| `src/segment.rs` | 6 | |
| `src/rfc3161.rs` | 5 | |
| `src/sealer.rs` | 3 | |
| `tests/bootstrap_fail_closed.rs` | 2 | exit-78 contract |
| **Total** | **240** | |

**Five property-test suites and a committed proptest regression corpus.** The core
repository has none of either.

**Test gap relative to G-1:** no test asserts that modifying `violations` in a log line is
detected — because it is not. A characterization test recording that fact would be safe
to add; changing the behaviour would not be.

---

## 7. CI

`.github/workflows/` contains 8 workflows. `ci.yml` runs six jobs:

| Job | Toolchain | Content |
|---|---|---|
| `fmt` | pinned `1.86.0` | `cargo fmt --all -- --check` |
| `clippy` | pinned `1.86.0` | `cargo clippy --all-targets --all-features -- -D warnings` |
| `test` | pinned `1.86.0` | `cargo build --locked --release --all-targets` + `cargo test --locked --all-targets` |
| `audit` | stable | `cargo audit --deny warnings --ignore RUSTSEC-2023-0071` (ignore is justified inline: `rsa` used for **verification only**) |
| `deny` | stable | `cargo deny check` |
| `sbom` | stable | CycloneDX SBOM uploaded as an artifact |

Plus `codeql.yml`, `coverage.yml`, `docker-image.yml`, `release.yml`, `rust.yml`,
`semgrep.yml`, `ibm.yml`.

Crate-level lints are enforced in `Cargo.toml:100-110`: `unsafe_code = "forbid"`,
`missing_docs = "warn"`, `clippy::all = "deny"`, `unwrap_used`/`expect_used`/`panic` =
`"warn"`. Release profile is hardened: `lto = "fat"`, `codegen-units = 1`,
`panic = "abort"`, `strip = "symbols"`.

**CI gap:** single platform (`ubuntu-latest`). No arm64 leg, no macOS, no Windows, no
cross-platform determinism comparison of the chain digest. Ironically the Python core —
which has far weaker CI overall — is the one with an arm64 leg.

---

## 8. Integration Boundary with Core

**There is none.** See `03_LANGUAGE_BOUNDARY.md` for the full absence proof.

The two systems are architecturally independent products:

| | Core (Python) | Guard (Rust) |
|---|---|---|
| Question answered | "how consistent is this agent with its constitution?" | "does this prompt/response violate a signed rulebook?" |
| Input | int32 vector | free text |
| Evidence | in-memory ETC, unpersisted | hash-chained JSONL on disk, Merkle-sealed, optionally TSA-anchored |
| Deployment | none | server + 4 binaries + Docker + systemd |
| Maturity | prototype | production-shaped |

They share a vocabulary and a specification repository. They share no code, no format, no
test vector and no runtime.

---

## 9. Dependency on Constitution / Vector / ARI

# NONE.

Aura-Guard has **zero** dependency on the Constitution Artifact, the Constitution Vector,
the embedding method, the numeric representation, or the ARI computation.

**Direct consequence for governance sequencing:** Aura-Guard is **not blocked** by
`DR-002`, by `SPEC-002`, by `AD-CA-001` … `AD-CA-012`, or by `CR-007`. Every engineering
improvement to Aura-Guard — including addressing G-1 through G-5 — can proceed
independently of the Constitution decision domain.

This is the single most useful scheduling fact in this audit and is carried into
`08_BLOCKERS.md` and `09_SAFE_WORK.md`.
