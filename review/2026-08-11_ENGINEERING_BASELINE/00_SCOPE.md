# 00 — SCOPE

**Package:** AURA ENGINEERING BASELINE AUDIT
**Date:** 2026-08-11
**Mode:** ENGINEERING / READ-ONLY
**Author role:** Architectural / conformance auditor (CLAUDE.md)

---

## 1. Purpose

Establish the **current engineering baseline** of the Aura ecosystem as it exists on
2026-08-11. This package is an **AS-IS observation record**. It contains no normative
claims, no architecture selections, and no protocol semantics.

---

## 2. Governance Position

Governance is unresolved. This package **does not**:

- resolve DR-002;
- select a governance authority;
- select a Constitution Vector format;
- select normalization semantics;
- select rounding semantics;
- select integer-division semantics;
- select an embedding method;
- generate a Constitution Vector;
- generate `constitution.json`;
- implement CR-007;
- treat current implementation behaviour as normative specification.

Every observation in this package describes **what the code does**, never **what the
protocol requires**. Where the two are confused in existing repository documentation,
the confusion is reported as a finding, not reconciled.

### Note on the identifier "DR-002"

The identifier `DR-002` does **not** appear in any inspected repository
(`aura-poc-a-core-v3.3`, `aura-guard-v1.3`, `aura-specification` [both owners],
`Aura-Conformance-Kit`, `Aura-Conformance-Kits`). Searched: all tracked `*.md`, `*.py`,
`*.txt`, `*.rs`.

The nearest tracked equivalents are the twelve unresolved architectural decision domains
`AD-CA-001` … `AD-CA-012` in
`aura-specification/specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` §6.

This package does **not** assume `DR-002` maps to any of them. The mapping is itself an
open governance question and is reported as such in `08_BLOCKERS.md` (NB-000).

---

## 3. Repositories Inspected

| # | Repository | Resolution | State inspected |
|---|---|---|---|
| 1 | `AuraIDToken/aura-poc-a-core-v3.3` | local checkout `/home/user/aura-poc-a-core-v3.3` | `main` @ `9c6a5d8` |
| 2 | `AuraIDToken/aura-guard-v1.3` | anonymous read clone (shallow) | `main` HEAD, 2026-08-02 push |
| 3 | `AuraIDToken/aura-specification` | anonymous read clone (shallow) | HEAD, 2026-08-10 push |
| 3b | `aura-nomos/aura-specification` | local checkout `/home/user/aura-specification` | `main` @ `eb2a4ec` |
| 4 | `AuraIDToken/Aura-Conformance-Kit` | anonymous read clone (shallow) | HEAD `6f10c5e` |
| 5 | `AuraIDToken/Aura-Conformance-Kits` | anonymous read clone (shallow) | HEAD `834ab46`, **archived** |

### Repository-identity observations

- **Two distinct `aura-specification` repositories exist.** `aura-nomos/aura-specification`
  contains only `README.md` (a single line: `# aura-specification`) and
  `.github/CODEOWNERS`. `AuraIDToken/aura-specification` contains the actual APS/SPEC/CONF
  document set. The task named `AuraIDToken/aura-specification`; the session was
  pre-attached to `aura-nomos/aura-specification`. Both were inspected. **Which one is
  authoritative is a governance question, not an engineering one** — reported as NB-001.
- **`Aura-Conformance-Kit` and `Aura-Conformance-Kits` are near-identical forks.** The
  only content difference is CI plumbing (`.circleci/`, `codeql.yml` present in `-Kit`,
  absent in `-Kits`). All Python source, docs and tests are byte-identical. `-Kits` is
  **archived**.

---

## 4. Method

All findings are derived from one of:

1. **Direct source read** — cited as `path:line`.
2. **Executed evidence** — commands run in this session, with output recorded.
3. **Absence proof** — an exhaustive grep whose empty result is the finding.

No finding is derived from README prose, badge text, or status claims in existing
documentation. Where documentation and code disagree, both are recorded and the
disagreement is the finding.

### Execution environment for reproduced evidence

| Item | Value |
|---|---|
| Python | 3.11.15 (CPython) |
| Rust / cargo | present (`/root/.cargo/bin`), toolchain resolved from `Cargo.lock` |
| Docker | **NOT AVAILABLE** (`/var/run/docker.sock` absent) |
| Platform | Linux x86_64 |

Docker unavailability means CHECK 7, CHECK 8, CHECK 9 and both DB-dependent test
classes could not be executed locally. This is recorded as *not executed here*, never as
*failing*.

---

## 5. Deliverables

| File | Task |
|---|---|
| `00_SCOPE.md` | this document |
| `01_CORE_INVENTORY.md` | TASK 1 |
| `02_RUNTIME_DATAFLOW.md` | TASK 2 |
| `03_LANGUAGE_BOUNDARY.md` | TASK 3 |
| `04_DETERMINISM_AUDIT.md` | TASK 4 |
| `05_TEST_MATRIX.md` | TASK 5 |
| `06_GUARD_AUDIT.md` | TASK 6 |
| `07_CONFORMANCE_AUDIT.md` | TASK 7 |
| `08_BLOCKERS.md` | TASK 8 |
| `09_SAFE_WORK.md` | TASK 9 |
| `10_ENGINEERING_BASELINE.md` | TASK 10 |

---

## 6. Constraints Honoured

- No production code modified. `git status` on `aura-poc-a-core-v3.3` was clean before
  and after all inspection except for this `review/` directory and gitignored side
  effects (`__pycache__/`, `artifacts/`).
- No PRs created.
- No ADRs created.
- No specifications changed.
- No fixtures created.

---

## 7. Classification Vocabulary

**Component status (TASK 1):**

| Term | Meaning in this package |
|---|---|
| `IMPLEMENTED` | Code exists, is reachable from at least one caller or test, and performs its stated function. |
| `PARTIAL` | Code exists and runs, but a stated capability is missing or only partly present. |
| `PLACEHOLDER` | Code exists and self-identifies (or demonstrably behaves) as a stand-in, not a real implementation. |
| `UNUSED` | Code or artefact exists with **zero** callers, importers, build steps or CI references. |
| `UNKNOWN` | Cannot be determined from the repository contents alone. |

**Determinism findings (TASK 4):** each is classified on four independent axes —
reachability (`LATENT` / `ACTIVE`), test status (`TESTED` / `UNTESTED`), and nature
(`NORMATIVE GAP` and/or `ENGINEERING BUG`). A single finding may carry both nature tags;
this is deliberate and is explained per finding.
