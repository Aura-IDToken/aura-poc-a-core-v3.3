# CHANGELOG
## Aura Protocol — Iron Core v3.3

**Format:** This changelog tracks implementation tasks (CORE-NNN) resolved in the Iron Core v3.3 lineage.  
**Policy:** Changes to core logic create a new instrument, not a new version. This changelog records the path to the frozen v3.3 instrument.  
**Instrument Version:** v3.3 (Iron Core — Integer Era)  
**Status:** FROZEN — MC-READY 2026

---

## [v3.3] — 2026-07-24 — Iron Core Freeze

### CORE-007 — Release Closure (2026-07-24)

**Type:** Documentation synchronization / Release engineering  
**Status:** COMPLETE

- Synchronized GAP-001.md with post-CORE-006 state: updated directory structure (section 2.1), test coverage table (section 2.4), CI/CD status (section 2.5), implementation maturity (section 2.7), and resolved gap entries (GAP-M5, GAP-M6, GAP-L1)
- Created CHANGELOG.md (this file)
- Created RELEASE_CLOSURE_REPORT.md with full release readiness assessment, readiness score, and release recommendation
- No code changes

---

### CORE-006 — Audit Layer Implementation (2026-07-24)

**Type:** Implementation  
**Status:** COMPLETE

- Implemented `audit/signing.py`: `Signer`/`Verifier` abstract interfaces; `HMACSigner`/`HMACVerifier` (HMAC-SHA256)
- Implemented `audit/merkle.py`: `MerkleTree`, `EventTrustCertificate`, `sha256`, `verify_proof`; deterministic odd-leaf duplication; ETC creation, signing, verification
- Implemented `audit/verify.py`: `verify_proof`, `verify_etc`
- Added `audit/test_audit.py`: 41 tests covering signing abstraction, canonical serialisation, Merkle construction, proof verification, ETC lifecycle, combined verification, cross-platform determinism
- Added `scripts/generate_determinism_report.py`: generates `determinism-report-<arch>.json` with 5 hash vectors
- Added `scripts/compare_determinism_reports.py`: exits 0 on PASS, 1 on FAIL
- Updated `.github/workflows/execution-checks.yml`: enabled ARM64 runner; added `compare-determinism` job
- Added `docs/specs/AUDIT_LAYER_SPEC.md`: normative, frozen specification for the Audit Layer (v1.0.0)
- Updated `docs/LEGACY_PROTOCOL.md`: full succession and disaster recovery protocol
- Updated `docs/KNOWN_LIMITATIONS.md`: KL-001 resolved, KL-002 documented

---

### CORE-005 — Layer Separation (2026-07-24)

**Type:** Critical fix / Architectural  
**Status:** COMPLETE

Resolved GAP-C1, GAP-C2, GAP-C3, GAP-C4 (critical invariant violations):

- Removed `COMPLIANCE_THRESHOLD` and `"status"` field from `core/evaluator.py`; Layer 0 now returns only `{"ari": int32, "drift": int32}`
- Converted `core/policy.py` to a deprecated backward-compatibility wrapper (re-exports from `compliance/policy.py`)
- Converted `core/consistency.py` to a deprecated backward-compatibility wrapper (re-exports from `compliance/consistency.py`)
- Created `compliance/evaluator_wrapper.py`: `evaluate_with_policy()` as the canonical Layer 2 orchestrator
- All policy logic (`RegulatoryPolicy`, `KillSwitch`, `PolicyRule`, `ConsistencyCalculator`) resides exclusively in `compliance/`
- `core/` contains only pure measurement (ARI calculation); no policy decisions
- `check_2_integer_only.sh` and `check_3_layer_separation.sh` both pass

---

### CORE-003/004 — Remove Float from Runtime Core (2026-01-23 — 2026-07-24)

**Type:** Critical fix  
**Status:** COMPLETE

- Rewrote `core/evaluator.py` (`PoCAEvaluator`) to use integer-only arithmetic with 10^5 fixed-point scaling
- Removed `import math` and all float operations from runtime paths
- `compliance/consistency.py` (`ConsistencyCalculator`) uses integer arithmetic only
- `core/offline_normalizer.py` remains the sole permitted float computation (DET_01)
- `check_2_integer_only.sh` passes

---

## [v3.2] — Historical (Float Era)

v3.2 used floating-point cosine similarity at runtime. This violated cross-architecture bit-identity requirements (IEEE-754 non-determinism on AVX vs NEON vs WASM).

v3.2 is not auditable under EU AI Act Article 13 due to non-reproducible float results.

**Migration path:** v3.2 → v3.3 requires replacing all runtime float operations with int32 fixed-point arithmetic and pre-normalising vectors offline.

---

**Custodian:** Kamil Krasiński  
**License:** Business Source License 1.1  
**Scaling Factor:** 100,000 (FROZEN)  
**Sentinel Constant:** 0.68 (FROZEN)  
**Runtime Float Count:** 0  
