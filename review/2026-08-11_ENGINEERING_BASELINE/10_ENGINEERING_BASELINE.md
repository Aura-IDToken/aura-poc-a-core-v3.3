# AURA ENGINEERING BASELINE v0.1

**Date:** 2026-08-11
**Status:** AS-IS observation record. Non-normative. No protocol semantics are defined,
selected, or implied by this document.
**Supersedes:** nothing. **Superseded by:** nothing.

This is the consolidated view. Every claim below is evidenced in files `00`–`09` of this
package.

---

## 1. Current Architecture

### 1.1 What exists

Five repositories, comprising **two independent products**, **one specification corpus**,
and **one empty conformance scaffold**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ AuraIDToken/aura-specification                                          │
│   APS-000…950 · CONF-001…010 (all DRAFT) · SPEC-002 (NOT READY)         │
│   INVARIANT_REGISTRY · AURA_CONSTITUTION · RI-PY / RI-RS (NOT CERTIFIED)│
└────────────────┬───────────────────────────────┬────────────────────────┘
                 │ describes                     │ describes
                 ▼                               ▼
┌────────────────────────────────┐  ┌────────────────────────────────────┐
│ aura-poc-a-core-v3.3 (Python)  │  │ aura-guard-v1.3 (Rust)             │
│ 4,893 LOC · 107 tests          │  │ 8,512 LOC · 240 tests              │
│ ARI measurement, prototype     │  │ Policy audit middleware, prod-shaped│
│                                │  │                                    │
│  core/       Layer 0 measure   │  │  api/ engine/ normalizer/ policy/  │
│  compliance/ Layer 2 policy    │  │  chain/ merkle/ segment/ sealer/   │
│  audit/      Layer 1 evidence  │  │  4 binaries · Docker · systemd     │
│  packages/   UNUSED            │  │                                    │
│  init.sql    schema, no writer │  │  logs/audit.jsonl  ← real evidence │
└────────────────────────────────┘  └────────────────────────────────────┘
                 ╎                                   ╎
                 ╎        NO INTERFACE               ╎
                 ╎  no FFI · no IPC · no HTTP        ╎
                 ╎  no shared format/fixture/hash    ╎
                 ╎···································╎

┌─────────────────────────────────────────────────────────────────────────┐
│ Aura-Conformance-Kit  /  Aura-Conformance-Kits  (byte-identical source) │
│   24 exception classes · 3 enums · 1 test: assert True                  │
│   Zero conformance tests. Correctly blocked by SPEC-002 NOT READY.      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Layer model inside the Python core

The three-layer model (Layer 0 measure / Layer 1 evidence / Layer 2 decide) is **real and
executably enforced**: `check_3_layer_separation.sh` scans imports and status returns;
`check_cr003_layer_boundary.py` performs an AST-based forbidden-import analysis. Both pass.

**But the layers are not connected.** Layer 0 produces a dict that no Layer 1 or Layer 2
production module consumes end-to-end. The only place all three are composed is a test
file that CI does not run.

### 1.3 The defining structural fact

`aura-poc-a-core-v3.3` is a **collection of correct-in-isolation components without a
pipeline**. Its individual pieces (`audit/`, `offline_normalizer`) are well built and well
tested. Nothing joins them.

`aura-guard-v1.3` is the opposite: a complete, deployable pipeline with real evidence
output.

---

## 2. Current Runtime Flow

**There is no single runtime flow in the Python core.** Three disconnected fragments plus
one broken demo (`02_RUNTIME_DATAFLOW.md`):

| Fragment | Path | Ends at | Callers |
|---|---|---|---|
| **A** Offline normalization | float → L2 → `round(×10⁵)` → int32 → JSON | a JSON file nobody reads | tests, determinism report |
| **B** Evaluation | halt check → dot → floor-div → weights → penalty | a Python dict | tests, broken demo |
| **C** Compliance/evidence | placeholder embed → consistency score → Merkle → certificate | an in-memory certificate | **`test_compliance.py` only** |
| **D** Demo | Fragment B with float inputs | aborts at DEMO 2 | manual |

Canonical-stage coverage:

| Stage | State |
|---|---|
| input | no schema, no parser, no validation |
| normalization | offline only, disconnected from runtime |
| vector representation | `list[int]`; canonical bytes exist **only in test/CI code** |
| arithmetic | present, integer-only, **two implementations** |
| similarity | dot product on assumed-unit vectors; floor-divide rescale |
| policy | present, **two incompatible penalty models** |
| result | present; two different dict shapes |
| serialization | reachable only from a test file; three JSON canonicalizations |
| evidence | real subsystem, **not wired to any result** |
| persistence | schema only; **no writer exists** |

Aura-Guard's flow, by contrast, is complete and executable:
`HTTP → auth → shadow-normalize → regex+validators → decision → chain_hash → append-only
JSONL → Merkle segment → optional RFC 3161`.

---

## 3. Current Implementation Status

| Layer | Component | Status |
|---|---|---|
| Layer 0 | `core/evaluator.py` | IMPLEMENTED, **no input validation** |
| Layer 0 | `core/offline_normalizer.py` | IMPLEMENTED |
| Layer 0 | `core/embedding.py` | **PLACEHOLDER** |
| Layer 0 | `core/merkle.py` | **PLACEHOLDER** (proof = leaf) |
| Layer 0 | `core/policy.py`, `core/consistency.py` | PARTIAL (deprecated shims) |
| Layer 1 | `audit/merkle.py`, `signing.py`, `verify.py` | IMPLEMENTED — best subsystem |
| Layer 2 | `compliance/policy.py` | IMPLEMENTED, process-local state |
| Layer 2 | `compliance/consistency.py` | IMPLEMENTED — **second ARI engine** |
| Layer 2 | `compliance/evaluator_wrapper.py` | IMPLEMENTED |
| Layer 2 | `compliance/certificate.py` | IMPLEMENTED |
| Layer 2 | `compliance/renderer.py` | IMPLEMENTED, **0 callers, 0 tests** |
| Layer 2 | `compliance/certificate_schema.json` | **UNUSED**, does not match emitted output |
| — | `packages/database-client` | **UNUSED**, unbuildable |
| — | `packages/zk-passport` | **UNUSED**, no toolchain |
| — | `init.sql` | PARTIAL — schema + constraints, **no writer** |
| — | `demo.py` | **BROKEN** |
| — | CLI | one only (`offline_normalizer`) |
| — | Public API | none packaged; `__all__` lists are inconsistent with reality |
| Guard | all modules | **IMPLEMENTED** (see `06_GUARD_AUDIT.md` §2) |
| Kit | all | **SCAFFOLD** |

---

## 4. Current Test Status

| Repository | Tests | Result | Property tests | Golden | Negative |
|---|---|---|---|---|---|
| `aura-poc-a-core-v3.3` | 107 (+4 uncollected) | **105 pass**, 2 Docker-gated | 0 | 0 | ~18, almost all in `audit/` |
| `aura-guard-v1.3` | 240 | **240 pass** | **5 suites** | 10 | many |
| `Aura-Conformance-Kit` | 1 | passes (`assert True`) | 0 | 0 | 0 |

Executed this session; commands and output in `05_TEST_MATRIX.md` §1 and
`06_GUARD_AUDIT.md` §1.

**Local check status (core, x86_64):** CHECK 0–6 PASS. CHECK 7–9 not executed (no Docker).

### The coverage inversion

| Component | Coverage |
|---|---|
| `audit/` (supporting evidence layer) | **strongest** — 47 tests, tamper tests, known-answer hashes, cross-platform vectors |
| `core/evaluator.py` (the product) | **weakest** — 14 bound-only assertions, no negative tests, no malformed input, **no cross-platform coverage at all** |

**Untested everywhere:** length mismatch, un-normalized input, `ari`/`drift` upper
bounds, accumulator width, exact negative-division values, cross-engine agreement,
canonical-form agreement.

---

## 5. Current Cross-Language Status

# NO CURRENT PYTHON/RUST RUNTIME INTERFACE

Established by exhaustive grep in both directions (`03_LANGUAGE_BOUNDARY.md` §2). Zero
`.rs` files in core; zero Constitution/ARI/Python references in Guard; no shared format,
fixture, constant or schema.

The two systems disagree on every candidate shared surface:

| Surface | Core | Guard |
|---|---|---|
| Merkle | duplication variant, no domain separation | RFC 6962, `0x00`/`0x01` prefixes |
| Signing | HMAC-SHA256 symmetric | Ed25519 asymmetric |
| Canonical bytes | JSON `sort_keys` (3 variants) | `\|`-joined concatenation |
| Numeric | int32 fixed-point ×10⁵ | `f32` confidence; no vector math |
| Evidence | in-memory ETC, unpersisted | hash-chained JSONL on disk |

**Consequence:** the three reported determinism issues are **LATENT** (D-1, D-2) rather
than active, because there is no second implementation to diverge from. They become active
on the first port or FFI boundary.

**Cross-platform status within Python:** real but narrow — x86_64 + arm64, CPython 3.12,
five hash vectors, **none of which touch the evaluator**. WASM is asserted by proxy, never
executed; the workflow itself says so.

**Scheduling consequence:** Aura-Guard has **zero dependency** on the Constitution, the
Vector, the embedding, the numeric representation, or ARI. It is not blocked by DR-002,
SPEC-002, any `AD-CA-xxx`, or CR-007.

---

## 6. Current Security Posture

### Python core — weak

| Property | State |
|---|---|
| Input validation at the measurement boundary | **NONE** (`PoCAEvaluator`) |
| Fail-open behaviour | **PRESENT** — a truncated vector scores maximum (D-3) |
| Evidence persistence | **NONE** in application code |
| Merkle proof in the demo path | **NOT A PROOF** (`core/merkle.py`) |
| Merkle domain separation | **ABSENT** (`sha256(left+right)`) |
| Signing | HMAC-SHA256 — **symmetric**, so any verifier can forge; Ed25519 named as future work |
| Halt state | process-local, non-durable; a DB table for it exists unused |
| Art. 5 guard | **ROBUST** — `ValueError`, not `assert`; verified under `-O`/`-OO` (CHECK 6) |
| Append-only enforcement | **ROBUST** at the DB layer — trigger + CHECK constraints, integration-tested |
| Secrets | test HMAC key clearly marked `_INSECURE_TEST_KEY_DO_NOT_USE_IN_PROD`; `infra/docker-compose.yml` has a default password (GAP-L5) |
| SAST / dependency audit / SBOM | **NONE** in CI |

### Aura-Guard — strong, with one significant gap

| Property | State |
|---|---|
| `unsafe_code` | **forbidden** at crate level |
| Fail-closed bootstrap | exit 78 before listener bind; tested |
| Fail-closed log writer | write failure → HTTP 503 until restart |
| Policy integrity | Ed25519 signatures, `trusted_signers.json`, policy hash logged per decision |
| Privacy | raw prompt/response never written; only digests |
| Chain integrity | 9 fields digested; tamper → exit 2 |
| **Evidence-detail integrity** | **GAP — `violations` are outside the digest and outside the Merkle leaves (G-1)** |
| TSA verification | full RFC 5652 + PKIX, offline, operator-pinned roots |
| CI security | `cargo audit`, `cargo deny`, CodeQL, Semgrep, CycloneDX SBOM |
| Dev bypass | single env var disables auth **and** signature enforcement (P2-18) |

### Ecosystem

No threat model spans both systems. `docs/threat_model.md` (core) and
`docs/THREAT_MODEL.md` (Guard) are independent and do not reference each other.

---

## 7. Current Performance Posture

**Unmeasured.** There is no benchmark, no profiling harness, and no performance
requirement in either repository.

Observable characteristics from source:

| | Core | Guard |
|---|---|---|
| Hot path | O(n) Python generator dot product over 1536 elements, arbitrary-precision ints | compiled regex over normalized text |
| Redundant work | `SA` computed **twice** per evaluation (P2-1) | none observed |
| Concurrency | none (library) | single mutex serializes all log writes (deliberate — prevents interleaving) |
| Build profile | n/a | `lto = "fat"`, `codegen-units = 1`, `opt-level = 3`, `strip` |
| Measured latency | none | `f64` seconds recorded into Prometheus per request |
| Test-suite runtime (measured) | 0.649 s / 107 tests | ~1.1 s / 240 tests |

The only quantitative performance-relevant measurement in this audit is the dot-product
accumulator magnitude: **1.536 × 10¹³** for the documented 1536-dim case, which exceeds
`i32` and requires ≥ `i64` in any compiled port (D-4).

---

## 8. Engineering Blockers

Full detail in `08_BLOCKERS.md`.

### P0 — before production

| ID | Blocker |
|---|---|
| P0-1 | `zip()` truncation → malformed vector scores **maximum** (fail-open) |
| P0-2 | No input validation at the measurement boundary; `ari` reaches 310000 |
| P0-3 | Two divergent ARI implementations with different penalty models |
| P0-4 | No evidence persisted; evidence chain not connected to any result |
| P0-5 | `core/merkle.py` "proof" proves nothing and is what the demo path uses |
| P0-6 | Guard: `violations` outside all integrity coverage |

### P1 — before integration

14 items, headlined by: **the evaluation path has zero cross-platform coverage** (P1-1);
**no tests for mismatched lengths, malformed input, or bounds** (P1-2); **`drift` violates
its own documented range** (P1-3); **CI does not run the unit tests** (P1-6); **core CI has
no linter, type checker, or dependency audit** (P1-8).

### P2 — hardening

22 items, including four checks that are lexical or existence-based rather than
behavioural (P2-7/8/9/10), duplicated constants, an unbuildable `packages/` tree, and a
`develop` branch trigger for a branch that does not exist.

---

## 9. Normative Blockers

21 items in `08_BLOCKERS.md` §4. **No priority is assigned; these are not engineering
work.**

Three are untracked in any repository and should be resolved first because everything else
cites them:

| ID | Question |
|---|---|
| **NB-000** | What does `DR-002` refer to, and how does it map to `AD-CA-001…012`? *(The identifier does not appear in any inspected repository.)* |
| **NB-001** | Which `aura-specification` repository is authoritative — `AuraIDToken/` (full APS corpus) or `aura-nomos/` (README only)? |
| **NB-002** | Which Conformance Kit is authoritative — the active one or the archived byte-identical twin? |

Twelve map directly to SPEC-002's own register (`AD-CA-001` … `AD-CA-012`). The remainder
are ecosystem questions the specification does not currently track: division semantics for
negative dividends (NB-016), which ARI engine is authoritative (NB-017), Merkle
construction (NB-018), halt-state durability (NB-019), whether Core and Guard integrate at
all (NB-020), and whether the v3.3 freeze permits defect correction (NB-021).

**Critical note carried from `04_DETERMINISM_AUDIT.md`:** the implementation's current
behaviour (`signed int32`, scale `100000`, `little-endian`, `round-half-to-even`) matches
the candidate list in `AD-CA-007`. **This is not evidence that those candidates were
selected.** SPEC-002 §6 states that no listed candidate constitutes a recommendation,
preference, default, or implied decision. This baseline does not select them and does not
treat the implementation as normative.

---

## 10. Safe Next Work

Full list in `09_SAFE_WORK.md`. Ordered by value-per-risk:

1. **Characterization tests** (S-1 … S-9) — record what the code does today for D-1
   through D-7 and for the two-engine divergence. Zero risk, zero normative content, and
   they produce exactly the data the blocked decisions need.
2. **CI wiring** (S-10, S-11) — make the 109 already-passing tests actually gate merges.
   Currently they gate nothing.
3. **All Aura-Guard work** (§1.7) — completely unblocked by governance. G-1 is the most
   serious integrity finding outside P0-1.
4. **Documentation corrections** (S-27 … S-34) — three stale claims currently mislead:
   GAP-C5's "LARGELY RESOLVED", Guard's README determinism sentence, Guard's ROADMAP test
   count.
5. **Static analysis in core CI** (S-12 … S-16) — bring core to the standard the empty
   Conformance Kit already meets.
6. **Bug fixes** (S-21 … S-26) — pending NB-021 (does the freeze permit defect
   correction?).

### Verified NOT safe, despite appearing on the standard "safe work" list

| Category | Why |
|---|---|
| Malformed-input **handling** | Detection is safe; the required response is NB-015 |
| Bounds **enforcement** | Adding a clamp changes computed output |
| Error-handling changes | `PolicyRule.is_violated`'s catch-all is a policy semantic |
| Annotating `core/` with `float` in any position | `check_2_integer_only.sh` is a plain grep; an annotation would fail it |
| Refactoring `core/` | Must re-pass four checks, two of which are lexical |
| Observability in `core/` | Constrained by CHECK 5 and CHECK 9 |
| Unifying the three JSON canonicalizations | Picking one is `AD-CA-008` |

---

## 11. Baseline Statement

As of 2026-08-11:

- **`aura-poc-a-core-v3.3`** is a research prototype whose components are individually
  sound and collectively unconnected. Its strongest subsystem (`audit/`) is not the one it
  is named for. Its measurement engine — the product — is the least validated and least
  covered code in the repository, and contains one active fail-open defect. It persists no
  evidence. It self-declares FROZEN while carrying unresolved defects.
- **`aura-guard-v1.3`** is a production-shaped, well-tested, well-CI'd Rust service with a
  real evidence chain and one significant integrity gap (`violations` outside the digest).
  It is independent of every unresolved Constitution decision.
- **The two do not communicate**, share no format, and solve different problems.
- **`aura-specification`** exists in two repositories with unclear precedence; its
  conformance tests are all DRAFT and SPEC-002 is formally NOT READY with twelve
  unresolved decision domains.
- **The Conformance Kit** is an empty, correctly-blocked scaffold with better CI than the
  reference implementation it is meant to test.

**The ecosystem's engineering readiness is not uniform, and its blockers are not uniform
either.** Roughly half the identified work — all of Aura-Guard, all characterization
testing, all CI wiring, all documentation correction — can proceed today without any
governance decision. The other half genuinely cannot, and this baseline does not attempt
to unblock it.

**Nothing in this document defines, selects, or implies a protocol semantic.**
