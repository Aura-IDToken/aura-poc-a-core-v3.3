# REPO-001 — Cross-Repository Change Placement Audit

**Type:** placement audit. **Read-only.** **Normative effect: NONE.**
**Date:** 2026-08-16
**Prepared by:** Claude, acting as repository placement auditor.

**Nothing was moved, renamed, deleted, merged or corrected.** No architecture decision was
made and no DQ was resolved or reopened.

---

## 1. Scope

Determine whether recent work has been placed in the correct repository, against the
**audit hypothesis** role model supplied with the task. The role model is used as a
yardstick, **not** as an architectural decision, and no inference is drawn that any
repository is a parent of another.

**Audit hypothesis:**

| Repo | Primary location for |
|---|---|
| **A — `aura-guard-v1.3`** | Rust implementation, production middleware, Rust tests, test infrastructure, implementation fixtures, implementation-specific cryptographic observations |
| **B — `aura-poc-a-core-v3.3`** | DQ review artifacts, evidence reports, governance records, audit packages, cross-repository review artifacts, architecture review material |
| **C — `aura-specification`** | Normative APS documents, protocol specifications, normative contracts, specification-level definitions |

No artifact was assumed correctly placed because it is already there, or because a prior
report said so. Every placement below was re-derived from `git` output.

---

## 2. Repositories examined

| # | Repository (remote verified) | Local path | HEAD | Default branch |
|---|---|---|---|---|
| 1 | `https://github.com/AuraIDToken/aura-poc-a-core-v3.3` | `/home/user/aura-poc-a-core-v3.3` | `b7061b8` | `main` |
| 2 | `https://github.com/AuraIDToken/aura-guard-v1.3` | `/workspace/aura-guard-v1.3` | `d704285` | `main` |
| 3 | `https://github.com/AuraIDToken/aura-specification` | `/workspace/auraidtoken/aura-specification` | `62d2d6b` | `main` |

Each remote URL was read with `git remote get-url origin`; none was inferred from a
directory name.

---

## 3. Branches examined

| Repository | `claude/auditentry-adapter-dq-001-h0os71` on remote | Commits ahead of `origin/main` |
|---|---|---|
| `aura-poc-a-core-v3.3` | **EXISTS** — `b7061b8ab7c4e27819438ebe8d84132c53a2c09b` | **11** |
| `aura-guard-v1.3` | **EXISTS** — `d7042852b03284cd5bd83e3c70c20f5f6f9f0593` | **2** |
| `aura-specification` | **ABSENT** | **0** — checked out on `main`, no local commits |

**EVIDENCE:** `git ls-remote --heads origin claude/auditentry-adapter-dq-001-h0os71` per
repository.

**Assessment — branch absent in `aura-specification`: CORRECT.** No normative change was
made or authorized in this work stream, so no branch was required there. Creating an empty
branch would add noise without content.

---

## 4. Commit inventory

### 4.1 `aura-poc-a-core-v3.3` — 11 commits ahead of `origin/main`

| Commit | Repository | Branch | Files | Change type | Expected repo | Placement |
|---|---|---|---|---|---|---|
| `e3e4732` | poc-a-core | `claude/auditentry-…` | 1 — `review/…_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/…REVIEW.md` | Review / architecture analysis | **B** | **CORRECT** |
| `8a67033` | poc-a-core | same | 1 — `review/…_D3-S4_DQ-001-H_CROSS_REPOSITORY_LINEAGE/…REVIEW.md` | Cross-repository review | **B** | **CORRECT** |
| `d7ddc6f` | poc-a-core | same | 1 — `review/…_D3-S5_DQ-002_LAYERED_HASH_DOMAINS/…REVIEW.md` | Review / evidence report | **B** | **CORRECT** |
| `a0c4901` | poc-a-core | same | 1 — `review/…_D3-S6_DQ-006_CANONICAL_SERIALIZATION/…REVIEW.md` | Review / evidence report | **B** | **CORRECT** |
| `349d644` | poc-a-core | same | 8 — `review/…_D3-S8_EVIDENCE_BASE_REFRESH/` (8 `.md`) | Evidence / audit package | **B** | **CORRECT** |
| `2ee54fb` | poc-a-core | same | 1 — `review/…_INFRA-001_HASH_DOMAIN_TEST_HARNESS/…REVIEW.md` | **Review artifact** (not test code) | **B** | **CORRECT** — but see **F1** |
| `1bb92b1` | poc-a-core | same | 1 — `review/…_D3-S5_DQ-001_CANONICAL_STATUS/…md` | Governance record | **B** | **CORRECT** |
| `2e2d725` | poc-a-core | same | 1 — `review/…_INFRA-002_CANONICAL_BYTE_FIXTURE/…REVIEW.md` | **Review artifact** (not test code) | **B** | **CORRECT** — but see **F1** |
| `178b960` | poc-a-core | same | 1 — `review/…_D3-S5_DQ-002_DECISION_READINESS/…md` | Governance record | **B** | **CORRECT** |
| `ab6e68e` | poc-a-core | same | 1 — `review/…_D3-S5_DQ-002_CONFLICT_RESOLUTION/…md` | Governance record | **B** | **CORRECT** |
| `b7061b8` | poc-a-core | same | 1 — `review/…_D3-S5_DQ-002_CANDIDATE_RESOLUTION_ASSESSMENT/…md` | Governance record | **B** | **CORRECT** |

**EVIDENCE — decisive negative check.** Every path touched by all 11 commits was
enumerated (`git log --format="" --name-only origin/main..HEAD | sort -u`):

- **18 unique paths, all under `review/`.** Filtering for anything outside `review/`
  returns **NONE**.
- Filtering for `\.(rs|py|toml|json|yaml|yml|lock|circom|ts)$` returns **NONE** — no code,
  config or fixture file of any kind.

### 4.2 `aura-guard-v1.3` — 2 commits ahead of `origin/main`

| Commit | Repository | Branch | Files | Change type | Expected repo | Placement |
|---|---|---|---|---|---|---|
| `9c6bc37` | guard | `claude/auditentry-…` | 13 — `tests/hash_domains.rs`, `tests/fixtures/hash_domains/HD-001…HD-011*.json`, `INVENTORY.json` | Test infrastructure + implementation fixtures | **A** | **CORRECT** |
| `d704285` | guard | same | 5 — `tests/byte_representations.rs`, `tests/support/mod.rs`, `tests/fixtures/byte_representations/BR-001…BR-003*.json` | Test infrastructure + fixtures | **A** | **CORRECT** |

**EVIDENCE — decisive negative check.** All 18 paths touched are under `tests/`. Filtering
for `^(src/|docs/|Cargo)` returns **NONE** — no production source, no documentation, no
manifest was touched.

### 4.3 `aura-specification` — no commits

**EVIDENCE.** `git log origin/main..HEAD` → **0 commits**. Working tree clean, on `main`
@ `62d2d6b`.

**Assessment:** no normative specification change was made anywhere in this work stream,
so §6 of the audit task (verify normative changes belong in `aura-specification`) resolves
as **NOT APPLICABLE — no such change exists**.

---

## 5. Artifact placement matrix

| Artifact | Current repo | Expected repo | Status | Evidence |
|---|---|---|---|---|
| DQ-001 adapter architecture review | poc-a-core | B | **CORRECT** | `e3e4732`, sole file under `review/` |
| DQ-001-H cross-repository lineage audit | poc-a-core | B | **CORRECT** | `8a67033` |
| DQ-001 canonical status record | poc-a-core | B | **CORRECT** | `1bb92b1` |
| DQ-002 layered hash domains review | poc-a-core | B | **CORRECT** | `d7ddc6f` |
| DQ-002 decision readiness gate | poc-a-core | B | **CORRECT** | `178b960` |
| DQ-002 conflict resolution record | poc-a-core | B | **CORRECT** | `ab6e68e` |
| DQ-002 candidate resolution assessment | poc-a-core | B | **CORRECT** | `b7061b8` |
| DQ-006 canonical serialization review | poc-a-core | B | **CORRECT** | `a0c4901` |
| D3-S8 evidence base refresh (8 files) | poc-a-core | B | **CORRECT** | `349d644` |
| INFRA-001 harness **code + fixtures** | guard | A | **CORRECT** | `9c6bc37`, all under `tests/` |
| INFRA-001 **review artifact** | poc-a-core | B | **CORRECT** | `2ee54fb` |
| INFRA-002 framework **code + fixtures** | guard | A | **CORRECT** | `d704285`, all under `tests/` |
| INFRA-002 **review artifact** | poc-a-core | B | **CORRECT** | `2e2d725` |
| Any normative/APS change | *(none exists)* | C | **NOT APPLICABLE** | 0 commits in `aura-specification` |

**On the INFRA split.** The harness code sits in the guard and its review record sits in
poc-a-core. Under the audit hypothesis this is **exactly what the role model prescribes**
(A: "test infrastructure", "implementation fixtures"; B: "review artifacts", "audit
packages"). It is recorded as CORRECT, not AMBIGUOUS. The one real consequence of the
split is discoverability, recorded as **F2** rather than as a placement error.

---

## 6. Claude work placement — the eight named commits

| Commit | Repo | Branch | File classes | Placement | Cross-repo reference required? |
|---|---|---|---|---|---|
| **`9c6bc37`** | **guard** | `claude/auditentry-…` | test code (`.rs`) + implementation fixtures (`.json`) | **CORRECT** — role A | Desirable; **absent** (F2) |
| **`d704285`** | **guard** | same | test code (`.rs`, incl. `tests/support/mod.rs`) + fixtures | **CORRECT** — role A | Desirable; **absent** (F2) |
| **`2ee54fb`** | **poc-a-core** | same | **review** (1 `.md`) | **CORRECT** — role B | Present — cites `9c6bc37` |
| **`2e2d725`** | **poc-a-core** | same | **review** (1 `.md`) | **CORRECT** — role B | Present — cites `d704285` |
| **`1bb92b1`** | **poc-a-core** | same | governance (1 `.md`) | **CORRECT** — role B | Not required |
| **`178b960`** | **poc-a-core** | same | governance (1 `.md`) | **CORRECT** — role B | Not required |
| **`ab6e68e`** | **poc-a-core** | same | governance (1 `.md`) | **CORRECT** — role B | Not required |
| **`b7061b8`** | **poc-a-core** | same | governance (1 `.md`) | **CORRECT** — role B | Not required |

**Specific check demanded by the audit task — was implementation work accidentally
committed to `aura-poc-a-core-v3.3`?**

**NO.** Verified by exhaustive path enumeration across all 11 poc-a-core commits: 18
unique paths, **100 % under `review/`**, **zero** files matching
`\.(rs|py|toml|json|yaml|yml|lock|circom|ts)$`. No implementation, test, fixture or
manifest file entered poc-a-core.

**Specific check — were review/governance artifacts correctly placed in poc-a-core?**

**YES.** All 18 review/governance files are in poc-a-core under `review/`, and none
appears in the guard (the guard has no `review/` directory at all).

---

## 7. Cross-repository dependencies

Only references established by evidence are recorded. **A cross-reference is not treated
as implementation lineage**, and a review artifact describing the guard is **not** treated
as evidence that guard implementation belongs in poc-a-core.

| From | To | Kind | Evidence |
|---|---|---|---|
| poc-a-core `INFRA-001…REVIEW.md:6,190` | guard `9c6bc37` | **Documentary citation** — names repo, branch, commit and file counts | `grep` of the artifact |
| poc-a-core `INFRA-002…REVIEW.md:6,277` | guard `d704285` | **Documentary citation** | `grep` of the artifact |
| poc-a-core review artifacts (D3-S4…D3-S8) | guard + spec source lines | **Documentary citation** — `file:line` references | throughout the artifacts |
| guard `9c6bc37`, `d704285` | poc-a-core | **NONE** | commit bodies contain no `poc-a-core` or `review/` reference; `grep` over `tests/hash_domains.rs`, `tests/byte_representations.rs`, `tests/support/mod.rs` returns no reference |

**FACT.** The reference relationship is **one-directional**: poc-a-core → guard. Nothing
in the guard points back.

**No build-time, runtime or code-level dependency between the repositories was found.**
The citations are documentary only.

---

## 8. Duplication / misplacement findings

### CONFIRMED

**None.** No duplication was found in any direction.

| Check | Result |
|---|---|
| Guard fixtures (`HD-*.json`, `BR-*.json`, `INVENTORY.json`) present in poc-a-core | **NOT FOUND** |
| Guard harness files (`hash_domains.rs`, `byte_representations.rs`) in poc-a-core | **NOT FOUND** |
| Normative material (`APS-*.md`, `SPEC-002*`, `INVARIANT_REGISTRY*`, `AURA_CONSTITUTION*`) copied into poc-a-core | **NOT FOUND** |
| poc-a-core review artifacts (`D3-S*`, `*REVIEW.md`) duplicated into guard | **NOT FOUND** |
| Normative material duplicated into guard | **NOT FOUND** |

**Note on quotation vs duplication.** The review artifacts quote APS text under
`file:line` citation. That is citation, not duplication: no whole normative document was
copied into poc-a-core or the guard.

### AMBIGUOUS

**F1 — commit-type label does not match commit content (labelling, not placement).**

**EVIDENCE.** `2ee54fb` and `2e2d725` in **poc-a-core** carry the conventional-commit
subject prefix **`test(infra):`** — "add hash domain replay harness" and "add byte
representation fixture framework" — while each contains **exactly one Markdown file under
`review/`** and no test code.

**Commit-type distribution across the 11 poc-a-core commits:** 8 × `docs`, 2 × `test`,
1 × `review`.

**Why this is AMBIGUOUS rather than INCORRECT:** the *files* are correctly placed. Only
the *label* signals implementation work in the governance repository. A reader auditing by
commit subject alone could reasonably conclude that test infrastructure had been committed
to poc-a-core — the exact error this audit was asked to look for. The subjects match the
guard commits `9c6bc37` / `d704285` verbatim, which is the likely origin of the collision.

**F2 — one-directional cross-reference (discoverability, not placement).**

**EVIDENCE.** The poc-a-core review artifacts cite guard commits `9c6bc37` and `d704285`
explicitly. Neither guard commit message, nor any file in the guard, references the review
artifacts; the guard has no `review/` directory.

**Consequence:** the review and governance record for guard test infrastructure is
discoverable **only** from the other repository. Someone reading the guard alone has no
pointer to it.

**Why this is AMBIGUOUS rather than INCORRECT:** the placement follows the role model.
Whether a back-reference is required is a governance convention question that the role
model does not settle.

### NOT FOUND

- Implementation files in poc-a-core — **not found**.
- Review artifacts in the guard — **not found**.
- Normative material outside `aura-specification` — **not found** in the audited change
  set.
- Any file in `aura-specification` changed by this work stream — **not found**.

### Observation outside the audited change set

`aura-poc-a-core-v3.3/docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` — an ADR **about
`aura-guard-v1.3`** located in poc-a-core's `docs/` (not `review/`), added by `76a3e54`
on 2026-08-12.

**Status: NOT APPLICABLE** — it predates the audited change set and is not associated with
any of the audited items. Recorded only because it is the same cross-repository pattern as
F2. Its placement in poc-a-core is **consistent** with role model B ("governance records").

---

## 9. Working tree / branch safety

| Repository | Branch | `git status --short` | Working tree | Local commits unpushed |
|---|---|---|---|---|
| `aura-poc-a-core-v3.3` | `claude/auditentry-adapter-dq-001-h0os71` | *(empty)* | **CLEAN** | none — remote matches `b7061b8` |
| `aura-guard-v1.3` | `claude/auditentry-adapter-dq-001-h0os71` | *(empty)* | **CLEAN** | none — remote matches `d704285` |
| `aura-specification` | `main` | *(empty)* | **CLEAN** | none — 0 ahead of `origin/main` |

All three working trees were clean **before** this audit began, and **nothing was modified
during it**. The only change produced by REPO-001 is this artifact.

---

## 10. Governance findings

Repository-placement and governance only. **No architectural conflict is resolved here.**

| # | Finding | Class | Requires file movement? |
|---|---|---|---|
| **G1** | Placement discipline held across 13 commits and 36 file paths in two repositories: 100 % of poc-a-core changes under `review/`, 100 % of guard changes under `tests/`, zero changes to `src/`, zero changes to any normative document | Positive finding | No |
| **G2** | No production source, no `Cargo` manifest and no APS document was modified anywhere in the audited change set | Positive finding | No |
| **F1** | Two poc-a-core commits carry a `test(infra):` subject while containing only review Markdown (§8 AMBIGUOUS) | Labelling | **No** |
| **F2** | Cross-repository reference is one-directional; the guard carries no pointer to its own review record (§8 AMBIGUOUS) | Discoverability | **No** |
| **G3** | The branch `claude/auditentry-adapter-dq-001-h0os71` is absent from `aura-specification`, correctly, because no normative change was made or authorized | Positive finding | No |

**Explicitly not addressed here:** DQ-001, DQ-002, DQ-006, CONFLICT-DQ002-01 and every
other registered conflict. Their statuses are unchanged by this audit.

---

## 11. Final classification

> ## **CLEAN**

**Every artifact in the audited change set is in the repository the role model
prescribes.** Zero files are misplaced, zero files are duplicated, and no implementation
work reached poc-a-core.

**Why the classification was not inflated to MINOR_PLACEMENT_ISSUES.** F1 and F2 are real
and are recorded prominently, but neither is a *placement* defect: F1 concerns a commit
subject line, F2 concerns cross-repository discoverability. No file would move under
either finding. Classifying correctly-placed work as having placement issues would
misreport the audit's actual result — while suppressing F1 and F2 would hide the two
things a reader most needs to know.

---

## 12. Recommended next action

**No file movement, rename, deletion or history rewrite is recommended.**

Smallest safe actions, **for the Architecture Owner to accept or decline** — none is
performed here:

1. **F1 — leave the commit subjects as they are.** Both are already pushed. Rewriting
   published history to fix a subject line is a materially larger risk than the mislabel
   itself. If the labels matter, the safest remedy is a note in a future governance
   record, not a rebase.
2. **F2 — optionally add a one-line pointer in the guard** (for example in `docs/` or a
   future commit body) naming the review location in poc-a-core. **This would be a change
   to the guard and is therefore outside this audit's authority.** It requires explicit
   authorization.
3. **No action required** for `aura-specification`: it is untouched, clean, and correctly
   carries no branch for this work stream.

---

## Declarations

No source code, test, fixture, normative document or previous review artifact was
modified. No file was moved, renamed or deleted. No ADR was created. No branch was merged.
No PR was opened. No DQ was resolved, closed or reopened. No architecture decision was
made. The audit was read-only and its sole output is this artifact.
