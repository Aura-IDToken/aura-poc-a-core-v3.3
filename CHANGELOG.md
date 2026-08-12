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

## v3.3 Iron Core — 2026-08-12

### RD-006 — CI/CD Scope Relative to the FROZEN Boundary (2026-08-12)

**Type:** Governance / Documentation
**Decision ID:** RD-006
**Accepted by:** Kamil Krasiński — Human Architectural Authority / Protocol Custodian
**Authorization:** Explicit acceptance recorded prior to formalization, under the bilateral
decision protocol (evidence preparation → ChatGPT review → human acceptance → formalization).

**Decision recorded:** CI/CD infrastructure is outside the FROZEN **semantic** boundary of
the Aura Core. CI/CD MAY observe FROZEN Core behaviour, execute characterization and
determinism tests, detect regressions, enforce already-established invariants, and generate
evidence. CI/CD MUST NOT modify FROZEN semantic content, reinterpret normative semantics,
approve semantic changes, or acquire or exercise governance authority.

**Documentation added:**
- `docs/ADR_006_CI_OUTSIDE_FROZEN_BOUNDARY.md` — the accepted decision, its scope,
  invariants (INV-CI-1 … INV-CI-8), evidence requirements (ER-1 … ER-7), merge blockers
  (MB-1 … MB-8), what it unlocks (U-1 … U-8), what remains blocked (B-1 … B-11),
  alternatives not adopted, and the preserved evidence trail.
- `CHANGELOG.md` — this entry.

**Scope limits recorded in the ADR.** This decision does not define ARI, does not select
ARI semantics, does not authorize any correction to `core/evaluator.py`, does not resolve
NB-021 globally, does not resolve DR-002, does not amend SPEC-002, and does not authorize
production-code remediation. It unlocks observation only.

**No code changes. No CI changes. No new functionality. No constitutional constants
modified. No protocol semantics selected.**

Work authorized by ADR-006 (CI-based ARI observability, GB-2, GB-3, EC-6) has **not** been
performed and remains subject to the ADR's evidence requirements and merge blockers.

**Finding recorded during formalization (ADR-006 §1.1), not remediated.**
`core/test_ari_observability.py` is currently non-executable: commit `110a845`
("Potential fix for pull request finding...", authored by Copilot Autofix) deleted its
`import unittest` while leaving `unittest.TestCase` in use. The module ran 8 passing tests
at its introducing commit `036ddd8` and cannot be imported at HEAD. **No CI step invokes
the module, so the breakage went undetected** — the RM-10 blind spot manifesting on the
artifact built to close it. Repair is a test-only change under NB-021 CASE D, is **not**
authorized by ADR-006, and is registered as blocking precondition **PRE-U1**.

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
- `audit/test_audit.py` — 53-test normative test suite covering signing abstraction,
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
