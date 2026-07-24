# CHANGELOG — Aura Protocol v3.3 Iron Core

**Instrument:** Aura Protocol v3.3 Iron Core  
**Status:** FROZEN — MC-READY 2026  
**License:** Business Source License 1.1

---

> **Policy:** This repository is a frozen regulatory measurement instrument.
> Each entry in this log documents a completed task that was authorized before
> execution. No entry represents a new feature or a change to the
> constitutional constants.

---

## v3.3 Iron Core — 2026-07-24

### CORE-007 — Release Closure (2026-07-24)

**Type:** Release Engineering / Documentation  
**Purpose:** Verify, synchronize, and freeze the repository for external technical review,
independent security audit, and regulatory assessment.

**Documentation corrections:**
- `docs/GAP-001.md` — updated change log, directory structure, test coverage table, CI/CD
  section, and implementation maturity table to reflect CORE-006 completion.
- `docs/architecture.md` — added `Document Version` and `Status: FROZEN` footer to match
  other normative documents.
- `CHANGELOG.md` — created (this file); standard release artifact.

**No code changes. No new functionality. No constitutional constants modified.**

---

### CORE-006 — Audit Layer Hardening (2026-07-24)

**Type:** Architecture / Implementation  
**Branch:** `copilot/featurecore-006-audit-hardening`  
**Merged:** PR #39

**Files added / modified:**
- `audit/signing.py` — `Signer` / `Verifier` abstract interfaces; `HMACSigner` /
  `HMACVerifier` (HMAC-SHA256 via RFC 2104). Constant-time comparison via
  `hmac.compare_digest`. Type enforcement (bytes-only keys).
- `audit/merkle.py` — `EventTrustCertificate` extended with `sign()`,
  `verify_signature()`, `_signing_payload()`, and `to_dict()` signature serialisation.
  `MerkleTree.create_etc()` updated to accept `Signer`.
- `audit/verify.py` — `verify_etc()` added.
- `audit/test_audit.py` — 49-test normative test suite covering signing abstraction,
  canonical serialisation, Merkle construction, proof verification, ETC lifecycle,
  combined verification, and cross-platform determinism vectors.
- `scripts/generate_determinism_report.py` — generates `determinism-report-<arch>.json`
  containing five determinism vectors (ARI hash, canonical event hash, Merkle root, ETC
  hash, HMAC signature).
- `scripts/compare_determinism_reports.py` — compares two reports and exits non-zero on
  any mismatch.
- `docs/specs/AUDIT_LAYER_SPEC.md` — normative frozen specification for the Audit Layer
  (canonical event format, SHA-256, append-only log, Merkle tree, ETC schema, signing).
- `.github/workflows/execution-checks.yml` — ARM64 runner enabled
  (`ubuntu-24.04-arm`); `wasm-compat` job added; `compare-determinism` job added.

**Constitutional compliance:** All changes are integer/byte-only. No float operations
introduced. Layer separation preserved (audit/ = Layer 1). No new runtime dependencies.

---

### CORE-005 — Layer Separation Repair (2026-07-24)

**Type:** Architecture / Critical Fix  
**Reference:** `CORE-005-IMPLEMENTATION-REPORT.md`

**Summary:** Resolved GAP-C1 through GAP-C4 identified in GAP-001:
- Removed float arithmetic from `core/evaluator.py` (GAP-C1).
- Removed float arithmetic from `core/consistency.py` → deprecated wrapper (GAP-C2).
- Removed policy/threshold logic from `core/evaluator.py` (GAP-C3).
- Moved `RegulatoryPolicy`, `PolicyRule`, `KillSwitch` to `compliance/policy.py` (GAP-C4).
- `core/policy.py` and `core/consistency.py` converted to backward-compatibility wrappers
  emitting `DeprecationWarning`; scheduled removal in v4.0 (KL-002).
- `compliance/evaluator_wrapper.py` created: `evaluate_with_policy()` orchestrator.
- All tests updated to import from `compliance.*`.

---

## v3.2 — Legacy Float Era (pre-2026)

Prior to v3.3, `core/evaluator.py` used `math.sqrt` and IEEE-754 floating-point cosine
similarity at runtime, which violated cross-architecture reproducibility requirements
(ADR-005). The v3.2 artifact is retained for audit traceability only.

See `docs/mathematical_foundation.md` §"Semantic Alignment — Historical Background" for
the removed float implementation.

---

**Custodian:** Kamil Krasiński  
**Constitutional Version:** 1.0  
**Entropy Budget:** Frozen
