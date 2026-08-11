# 03 — PYTHON / RUST BOUNDARY (TASK 3)

---

## 1. Determination

# NO CURRENT PYTHON/RUST RUNTIME INTERFACE

Python (`aura-poc-a-core-v3.3`) and Rust (`aura-guard-v1.3`) **do not communicate** in
any form: no FFI, no IPC, no HTTP call, no shared file format, no shared schema, no
shared test vector, no shared constant.

---

## 2. Evidence of Absence

### 2.1 Rust side → Python

Exhaustive case-insensitive grep over `src/`, `tests/`, `Cargo.toml` of
`aura-guard-v1.3` for: `constitution`, `ari`, `poca`, `python`, `pyo3`, `ffi`, `wasm`.

Result: **five hits, all false positives** — four are the substring `ari` inside
`variables`/`arithmetic`-style identifiers in `src/validators.rs:435-439`, one is the
word "boot" context in `src/sealer.rs:131`. Zero real matches.

`Cargo.toml` dependency list (67 lines of dependencies) contains **no** `pyo3`,
`cpython`, `rustpython`, `numpy`, or any Python-interop crate. There is no `cdylib`
crate-type; `[lib]` is a plain Rust `lib` (`Cargo.toml:14-16`). No `build.rs`. No
`.pyi`, no `maturin`, no `setup.py` shim.

### 2.2 Python side → Rust

Exhaustive grep over all `*.py`, `*.toml`, `*.yml`, `*.ts` in `aura-poc-a-core-v3.3` for:
`aura-guard`, `aura_guard`, `rust`, `pyo3`, `cffi`, `ctypes`, `maturin`, `wasmtime`.

Result: **zero real matches.** The only `subprocess` uses are `docker compose` / `psql`
invocations inside two test files and one check script. The only `wasmtime` mentions are
in prose comments (`core/test_bitwise_replay.py:345,393`,
`.github/workflows/execution-checks.yml:84`) describing it as future work.

There are **zero `.rs` files** in `aura-poc-a-core-v3.3`. There is a
`.github/instructions/rust-conformance.instructions.md` that declares rules for `**/*.rs`
— it currently applies to no file in the repository.

### 2.3 No shared data artefacts

| Candidate shared surface | Python side | Rust side | Shared? |
|---|---|---|---|
| Hash chain / evidence record | `EventTrustCertificate` (`audit/merkle.py:37`) | `AuditEntry` (`src/models.rs:50`) | **No** — disjoint field sets, disjoint semantics |
| Merkle construction | pairwise, odd node **duplicated** (`audit/merkle.py:157`) | RFC 6962 (`src/merkle.rs`, `src/segment.rs:6`) | **No** — different algorithms, different roots for the same leaves |
| Canonical bytes | JSON `sort_keys=True`, `separators=(",",":")` (`audit/merkle.py:89`) | `\|`-joined field concatenation (`src/chain.rs:20,36-46`) | **No** |
| Signature | HMAC-SHA256, symmetric (`audit/signing.py:88`) | Ed25519, asymmetric, over policy YAML (`src/crypto.rs`) | **No** |
| Numeric model | int32 fixed-point, scale 10^5 | `f32` confidence scores (`src/models.rs:38`); no vector arithmetic at all | **No** |
| Test fixtures | none shared | `tests/fixtures/tsa/*` (TSA certs/manifests) | **No** |
| Config | none | `figment` TOML/env (`src/config.rs`) | **No** |
| Version identifier | `"0.1.0"` (`pyproject.toml`) / `"v3.3-iron-core"` (`scripts/generate_determinism_report.py:44`) / `"v3.3"` (JSON payloads) / `"1.0.0"` (certificate schema_version) | `1.3.0` (`Cargo.toml`) + `/version` endpoint | **No** |

### 2.4 The two systems solve different problems

This is the structural reason there is no boundary, and it matters for §4.

| | `aura-poc-a-core-v3.3` (Python) | `aura-guard-v1.3` (Rust) |
|---|---|---|
| Input | pre-normalized int32 vector + boolean | free-text `{context, prompt, response}` |
| Decision basis | numeric similarity to a constitution vector | regex + semantic validators against signed YAML policy |
| Output | `ari`, `drift` (integers) | `DENY` / `REVIEW` / `ALLOW` + violations |
| Evidence | in-memory ETC (unpersisted) | append-only hash-chained JSONL on disk, Merkle-sealed segments, optional RFC 3161 |
| Deployment | none (library + one CLI) | HTTP server + 4 binaries + Docker + systemd |

They share vocabulary ("deterministic", "audit", "Merkle", "evidence") and nothing else.
The specification repository already records this: `reference/RI-PY_AURA_POC_A_CORE.md`
and `reference/RI-RS_AURA_GUARD.md` describe them as two separate, independently
**NOT CERTIFIED** reference implementations.

---

## 3. Consequence for the Reported Determinism Issues

The three reported issues (Python `//` vs Rust/C/JS division; Python `round()` vs other
languages; `zip()` truncation) are **cross-language conformance risks that cannot
currently manifest**, because no second-language implementation of the affected
arithmetic exists.

Precisely:
- Aura-Guard implements **no** vector arithmetic, **no** rounding of scaled integers, and
  **no** paired-sequence iteration over vectors. There is nothing on the Rust side to
  disagree with the Python side.
- `VectorRepository.ts` (`packages/database-client/`) is the only other-language artefact
  that touches the same conceptual domain (vector similarity), and it is UNUSED,
  unbuildable, and uses float cosine distance — a third, unrelated model.

This is why `04_DETERMINISM_AUDIT.md` classifies D-1 and D-2 as **LATENT** rather than
**ACTIVE**: they are real properties of the code with no current second implementation to
diverge from. `zip()` truncation (D-3) is classified differently — it is reachable inside
Python alone.

---

## 4. Cleanest Future Integration Boundaries — Options Only

**This section selects nothing.** Per the task, it identifies where a boundary *could*
cleanly be placed given the current architecture, and states the engineering cost of
each. Choosing among them is an architecture decision that belongs to governance, and
several of the options are additionally gated by unresolved decision domains
(`AD-CA-007` numeric representation, `AD-CA-008` canonical serialization / byte
sequence / hash domains).

### Constraints any option must respect (from current code, not from any new decision)

1. `core/` may not import `compliance/`, `audit/`, DB drivers, or network libraries —
   enforced executably by `scripts/check_cr003_layer_boundary.py` (CHECK 9) and
   `check_3_layer_separation.sh` (CHECK 3).
2. `core/` may contain no `float`/`sqrt`/`numpy` tokens — CHECK 2.
3. Aura-Guard forbids `unsafe_code` at crate level (`Cargo.toml:104`,
   `src/lib.rs:8`). Any FFI surface exposing raw pointers into Rust would require
   relaxing that, or confining `unsafe` to a separate crate.
4. Nothing in either repository currently defines a canonical byte sequence for a
   vector. The only such encoding in existence is in test/CI code.

### Option A — Byte-level test-vector boundary (no runtime coupling)

Both implementations independently produce a hash over a defined byte encoding of the
same inputs; CI compares the hashes. This is exactly the shape of the existing
`compare-determinism` job, extended to a second language.

- **Coupling introduced:** none at runtime. Only a shared fixture file + a CI job.
- **Requires:** a defined byte encoding and a defined set of inputs.
- **Blocked by:** `AD-CA-007`, `AD-CA-008` for anything constitution-vector-shaped. **Not
  blocked** for inputs that involve no unresolved normative choice (e.g. the existing
  Merkle/HMAC vectors, which are already defined by `docs/specs/AUDIT_LAYER_SPEC.md`).
- **Cost:** low. Reuses `scripts/compare_determinism_reports.py` unchanged.
- **Cannot answer:** anything about live interoperation.

### Option B — Process boundary over a serialized message (HTTP / stdin-stdout)

One side calls the other over a wire format. Aura-Guard already has an HTTP server,
`axum` routing, auth, body limits and Prometheus metrics (`src/api/mod.rs:50`).

- **Coupling introduced:** an operational dependency and a wire schema.
- **Requires:** the wire schema, which is a canonical-serialization decision.
- **Blocked by:** `AD-CA-008` if any Constitution-derived object crosses the wire. Not
  blocked for message types that carry no such object.
- **Cost:** medium. Guard's HTTP surface is production-shaped; the Python side has none
  and would need one built.
- **Risk to record:** placing a boundary here makes evidence-chain integrity span two
  systems whose evidence models are currently incompatible (§2.3).

### Option C — In-process FFI (`pyo3` / `cdylib` + `ctypes`)

Rust exposes the arithmetic kernel; Python calls it directly.

- **Coupling introduced:** build coupling (Python wheels must ship a compiled artefact
  per platform), ABI coupling, and a shared memory representation.
- **Requires:** a fixed in-memory layout for vectors — i.e. the numeric representation
  decision (`AD-CA-007`) in its strongest form.
- **Conflicts with:** `unsafe_code = "forbid"` in Guard, unless a separate FFI crate is
  introduced.
- **Cost:** high. Cross-platform wheel building, and CI would need to build Rust on both
  the x86_64 and arm64 legs.
- **Note:** this is the **only** option that would make the three reported determinism
  issues immediately ACTIVE rather than LATENT, because it puts Python `//` and Rust `/`
  in the same computation.

### Option D — No integration; keep the two products separate

Formalize what the code already is: two independent products with independent evidence
chains, related only by a shared specification.

- **Coupling introduced:** none.
- **Cost:** zero engineering cost; the cost is that "one ecosystem" claims in READMEs and
  reports would need to be reconciled with reality.
- **Observation:** this is the **current** de-facto state, and the specification repo's
  own RI-PY / RI-RS documents already describe them separately.

### Comparison

| | A: test vectors | B: wire | C: FFI | D: separate |
|---|---|---|---|---|
| Runtime coupling | none | process | in-process | none |
| Blocked by AD-CA-007/008 | partially | partially | fully | no |
| Makes D-1/D-2 ACTIVE | no (detects them) | possibly | **yes** | no |
| Conflicts with Guard's `forbid(unsafe_code)` | no | no | **yes** | no |
| Engineering cost | low | medium | high | none |

**No recommendation is made.** The engineering observation is only that **Option A is the
only one that can be prototyped without first resolving a numeric-representation or
canonical-serialization decision**, and that it is the option that would *detect*
cross-language divergence rather than *introduce* the conditions for it.

---

## 5. If a Boundary Is Later Chosen — What Must Be Defined First

Recorded as an engineering checklist, not as requirements:

1. Byte encoding of an integer vector (width, signedness, endianness, element order).
2. Division semantics at the rescale step (`dot / SCALE`) for negative dividends — Python
   `//` floors, Rust/C/JS `/` truncates toward zero. See `04_DETERMINISM_AUDIT.md` D-1.
3. Rounding rule at any float→int reduction — Python `round()` is half-to-even; Rust
   `f64::round()` and JS `Math.round()` are not. See D-2.
4. Behaviour on length mismatch — currently silent truncation on both Python
   implementations. See D-3.
5. Overflow behaviour — the intermediate dot product reaches ~1.5×10¹³ for 1536-dim
   vectors (measured, §D-4), which exceeds `i32` and requires at least `i64`.
6. Canonical JSON form — the repository currently uses three different ones.

Items 1–6 are engineering prerequisites for *any* second implementation. Which answers
are correct is not an engineering question.
