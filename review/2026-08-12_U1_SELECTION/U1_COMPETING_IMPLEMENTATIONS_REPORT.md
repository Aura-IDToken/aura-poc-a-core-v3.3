# U-1 COMPETING IMPLEMENTATIONS — DECISION PACKAGE

**Date:** 2026-08-12
**Prepared by:** engineering evidence analyst (not Architectural Authority, not Governance Authority)
**Status:** EVIDENCE ONLY — NO SELECTION MADE
**Normative effect:** NONE

> **Analyst disclosure.** Candidate A (`b73e176`) was authored by this same agent session earlier
> today. Candidate B (`edd53ab`) was authored independently. To control for that bias, every claim
> below was reconstructed directly from git and from executing both candidates, not from the earlier
> session report. The strongest single finding in this package (§14, NEG-5) is **unfavourable to
> Candidate A**. The Human Architectural Authority should nevertheless weigh this disclosure when
> reading the package.

---

## 1. Executive Summary

Two sibling U-1 implementations exist. Both descend from the identical parent `ee3be6f` (PRE-U1),
both are fast-forwardable from `main`, and both **conflict with each other** on all three shared
files. Exactly one may be selected.

Both candidates satisfy the four originally specified negative controls (broken import, zero
collection, wrong observation, partial collection) — verified by execution, not by inspection.
Neither modifies production code, ARI semantics, ADR-006, SPEC-002, or the Constitution.

The differences that matter are **four**, all verified by execution:

| # | Finding | Favours |
|---|---|---|
| F-1 | **Skipped-test blindness.** With all 8 tests skipped, `unittest` prints `Ran 8 tests … OK (skipped=8)` and exits 0. Candidate A passes this state when `artifacts/` is non-empty; Candidate B fails it explicitly. | B |
| F-2 | **Stale-evidence tolerance.** A does not clear the prior observation artifact; its artifact-existence guard can be satisfied by a file from an earlier run. B deletes it before executing. | B |
| F-3 | **Exact pin vs floor.** A requires exactly 8 tests (authorized harness growth to 9 fails CI); B requires ≥ 8 (growth passes, shrinkage fails). | Genuine trade-off — a governance preference, not a defect |
| F-4 | **Scope.** B additionally modifies `CHANGELOG.md` (+79 lines) and replicates the five observed ARI values there; A changes no documentation. | A on scope minimality; neutral on correctness |

A fifth finding applies to **both** candidates and to the frozen harness: **ER-4 is not satisfied by
either** (§13, §16).

**Final status: DECISION READY — HUMAN SELECTION REQUIRED.**

---

## 2. Repository State

| Item | Value | Evidence |
|---|---|---|
| Current `main` | `f3a87cc80d7290a43c7f83d5d053590d42736e65` | `git rev-parse origin/main` |
| Working tree | clean; no files modified by this task except this report | `git status --short` |
| Open PRs | none | `list_pull_requests(state=open)` → `[]` |
| `aura-guard-v1.3` | **not present** in this session workspace | `ls /home/user` |

### §11 — What `main` contains (explicit)

| Artifact | On `main`? | Evidence |
|---|---|---|
| RD-006 harness `core/test_ari_observability.py` | **YES** | `git cat-file -e origin/main:…` |
| PRE-U1 `import unittest` correction | **NO — main carries the broken post-`110a845` state** | `git show origin/main:core/test_ari_observability.py \| grep '^import unittest'` → no match |
| ADR-006 | **NO** | `git cat-file -e origin/main:docs/ADR_006_…md` → absent |
| U-1 CI wiring (CHECK 10) | **NO** | `git show origin/main:scripts/run_all_checks.sh \| grep 'CHECK 10'` → no match |
| `scripts/checks/check_10_ari_observability.sh` | **NO** | absent on `main` |

**`main` therefore contains a harness that cannot import.** This is the state both candidates exist
to make executable and fail-closed.

---

## 3. Commit Graph

```
f3a87cc  main
   │
   ├── 22ab272  review: remediation readiness package        (docs only, +4053)
   ├── 1d4bb37  review: RD-006 decision brief                (docs only,  +743)
   ├── fc6669a  ADR-006                                      (docs only,  +543)
   ├── ee3be6f  PRE-U1 — restores `import unittest`          (harness,      +1)
   │
   ├────────────┬────────────────────────────────────────────────────────────
   │            │
b73e176      edd53ab
 U-1-A        U-1-B
```

| Check | Result | Evidence |
|---|---|---|
| parent of `b73e176` | `ee3be6f` | `git rev-parse b73e176^` |
| parent of `edd53ab` | `ee3be6f` | `git rev-parse edd53ab^` |
| merge-base(A, B) | `ee3be6f` | `git merge-base b73e176 edd53ab` |
| extra commits on A beyond stack | exactly 1 (`b73e176`) | `git log ee3be6f..b73e176` |
| extra commits on B beyond stack | exactly 1 (`edd53ab`) | `git log ee3be6f..edd53ab` |

**Note on the stated dependency graph.** The prerequisite stack is **5 commits**, not 3. `fc6669a`'s
parent is `1d4bb37`, not `main`. The two intervening commits (`22ab272`, `1d4bb37`) are
`review/`-directory documentation only and land with either candidate. Rebase/squash being
prohibited, this is forced by parentage.

---

## 4. U-1-A Description (`b73e176`)

*"ci(U-1): execute ARI observability harness in CI, fail-closed on zero collection"*

3 files, **+118 / −0**:

| File | Change |
|---|---|
| `scripts/checks/check_10_ari_observability.sh` | new, 103 lines |
| `scripts/run_all_checks.sh` | +13 — CHECK 10 block + summary line |
| `.github/workflows/execution-checks.yml` | +2 — two artifact paths |

Structure: `set -euo pipefail` → run `python3 -m unittest core.test_ari_observability -v` via
`tee`, capture `PIPESTATUS` → fail on non-zero exit → parse `Ran N tests` → **require `N == 8`
exactly** (`-ne`, line 80) → require observation artifact exists (line 90).

## 5. U-1-B Description (`edd53ab`)

*"ci(U-1): wire ARI observability harness into CI as CHECK 10"*

4 files, **+262 / −0**:

| File | Change |
|---|---|
| `scripts/checks/check_10_ari_observability.sh` | new, 165 lines |
| `scripts/run_all_checks.sh` | +16 — CHECK 10 block + summary + 3-line ADR-006 note |
| `.github/workflows/execution-checks.yml` | +2 — same two artifact paths |
| `CHANGELOG.md` | +79 — U-1 entry |

Structure: `set -euo pipefail` → **`cd "$REPO_ROOT"`** (line 29) → **delete stale observation
artifact** (line 46) → run harness → fail on non-zero exit → **GUARD 1** `N >= 8` (`-lt`, line 113)
→ **GUARD 2** no skipped / expected-failure outcomes (line 129) → **GUARD 3** artifact exists
(line 142) **and** contains `"normative_effect": "NONE"` (line 148).

---

## 6. File-Level Diff Comparison

| File | A | B | Classification |
|---|---|---|---|
| `.github/workflows/execution-checks.yml` | +2 paths | +2 paths (reverse order) | **NON-MATERIAL** — identical set; `upload-artifact` path order is not significant |
| `scripts/run_all_checks.sh` | +13 | +16 | **NON-MATERIAL** for gating — byte-identical `if/else`, identical `OVERALL_STATUS=1`; B adds 3 explanatory `echo` lines |
| `scripts/checks/check_10_…sh` | 103 lines | 165 lines | **MATERIAL** — see §7 |
| `CHANGELOG.md` | untouched | +79 | **MATERIAL (scope)** — see §13 |

Neither candidate touches `core/`, `audit/`, `compliance/`, `packages/`, `docs/`, ADR-006, SPEC-002,
or the Constitution. Verified by path-filtered `git diff --name-only` on both commits (§3, items G–K
all returned empty).

---

## 7. Behavioural Comparison

All rows verified by **executing** both candidates against isolated trees extracted with
`git archive` into scratchpad. The repository working tree was never modified.

| # | Dimension | U-1-A | U-1-B | Class |
|---|---|---|---|---|
| 1 | CHECK 10 script | 103 lines, 2 guards | 165 lines, 3 guards + hygiene | MATERIAL |
| 2 | `run_all_checks.sh` integration | identical gate | identical gate | NON-MATERIAL |
| 3 | `execution-checks.yml` | identical | identical | NON-MATERIAL |
| 4 | Artifact handling | asserts existence | **deletes stale first**, asserts existence + ER-2 marker | **MATERIAL** |
| 5 | Test invocation | explicit module name | explicit module name | NON-MATERIAL |
| 6 | Test-count enforcement | `-ne 8` (exact pin) | `-lt 8` (floor) | **MATERIAL** |
| 7 | Zero-test detection | ✅ exit 1 | ✅ exit 1 | NON-MATERIAL (both pass) |
| 8 | Import-failure detection | ✅ exit 1 | ✅ exit 1 | NON-MATERIAL (both pass) |
| 9 | Partial-collection detection | ✅ exit 1 | ✅ exit 1 | NON-MATERIAL (both pass) |
| 10 | **Skipped-test detection** | ❌ **exit 0 with stale artifact** | ✅ exit 1 | **MATERIAL** |
| 11 | Observation validation | artifact exists | artifact exists **+ `normative_effect: NONE`** | MATERIAL (but redundant — §9) |
| 12 | Exit-code propagation | `PIPESTATUS`, correct | `PIPESTATUS`, correct | NON-MATERIAL |
| 13 | `OVERALL_STATUS` propagation | correct | correct | NON-MATERIAL |
| 14 | CI failure visibility | failure text + counts | failure text + counts + ER-6 instruction | NON-MATERIAL |
| 15 | Maintainability | fewer lines; pin needs updating on any harness change | more lines; floor needs updating only on authorized shrink | MATERIAL (opposing directions) |
| 16 | Complexity | lower | higher | NON-MATERIAL |
| 17 | Duplicated logic | none | none | NON-MATERIAL |
| 18 | Hardcoded assumptions | `EXPECTED_TESTS=8`; inline log path; **cwd-dependent** | `MIN_EXPECTED_TESTS=8`; path vars; `cd $REPO_ROOT` | **MATERIAL** |
| 19 | Portability | fails if invoked from another cwd (exit 1, fail-closed) | succeeds from any cwd | **MATERIAL** |
| 20 | Interaction with existing CI | none | none | NON-MATERIAL |
| 21 | Effect on other CHECKs | none | none | NON-MATERIAL |
| 22 | Scope creep | none | `CHANGELOG.md` | **MATERIAL** |
| 23 | CHANGELOG/doc changes | none | +79 lines incl. 5 ARI values | **MATERIAL** |
| 24 | Future maintenance burden | any harness size change reds CI until pin updated | only shrink reds CI | MATERIAL (opposing directions) |

### Executed evidence — negative-control matrix

```
                                U-1-A   U-1-B
PRISTINE (8/8)                  exit 0  exit 0
NEG-1  broken import            exit 1  exit 1
NEG-2  zero tests collected     exit 1  exit 1
NEG-3  perturbed observation    exit 1  exit 1
NEG-4  partial collection (4/8) exit 1  exit 1
NEG-5  all 8 tests SKIPPED      exit 0* exit 1     ← divergence
GROWTH to 9 tests               exit 1  exit 0     ← divergence
Invoked from foreign cwd (/)    exit 1  exit 0     ← divergence

* exit 0 when artifacts/ contains an observation file from a prior run.
  With artifacts/ empty, A returns exit 1 — incidentally, via its
  artifact-existence guard, not via any skip guard.
```

---

## 8. RD-006 Conformance

`RD-006_ARI_OBSERVABILITY.md` §7 drafts U-1 as a check block appended to `run_all_checks.sh` plus
one artifact path added to the workflow upload list. ADR-006 §8 U-1 adopts that shape.

| Contract item | A | B | Evidence |
|---|---|---|---|
| Executes `core.test_ari_observability` | ✅ | ✅ | explicit module name, both |
| Executes the evaluator (not replayed constants) | ✅ | ✅ | harness `HarnessIntegrityControlTest` ×4 executes in both |
| Prevents zero-test silent success | ✅ | ✅ | NEG-2 |
| Detects import failure | ✅ | ✅ | NEG-1 |
| Detects partial collection | ✅ | ✅ | NEG-4 |
| **Detects skipped-as-executed** | ❌ conditional | ✅ | NEG-5 |
| Requires expected observation output | ✅ (via harness assertions) | ✅ (+ CI-level marker check) | NEG-3 |
| Preserves NON-NORMATIVE status | ✅ | ✅ | both label output; neither alters harness |
| Introduces no canonical ARI values | ✅ **none** | ⚠ 5 values replicated in `CHANGELOG.md` | §13 |
| Changes no ARI semantics | ✅ | ✅ | harness byte-identical in both |
| Creates no normative fixture | ✅ | ✅ | §13 |
| Uploads observation artifact | ✅ | ✅ | identical workflow diff |
| Makes CI observability executable | ✅ | ✅ | both gate `OVERALL_STATUS` |

Both satisfy the drafted §7 shape. Neither was accepted on inspection alone — every row above with a
✅/❌ for detection was executed.

---

## 9. Negative-Control Analysis

**Implemented and exercised (both):** NEG-1, NEG-2, NEG-3, NEG-4 — all four are *structurally
implemented* in both candidates (not merely documented) and were *actually exercised* here against
isolated trees.

**NEG-5 (skipped tests) — implemented only in B.** B implements it explicitly at line 129. A has no
skip guard. `unittest` counts skipped tests inside its `Ran N` total, so A's count guard cannot see
skips:

```
$ python3 -m unittest core.test_ari_observability     # all 8 classes @unittest.skip
Ran 8 tests in 0.000s
OK (skipped=8)                                        # exit 0
```

A's *only* barrier in this state is its artifact-existence guard, which holds solely because a
skipped `setUpClass` writes no artifact. That barrier is defeated by any pre-existing
`artifacts/rd-006-ari-observation.json`:

```
A, NEG-5, artifacts/ empty   → exit 1   (caught, incidentally)
A, NEG-5, stale artifact     → exit 0   (SILENT SUCCESS — evaluator never ran)
```

**Materiality qualifier — read this before weighting F-1/F-2.** `artifacts/` is `.gitignore`d
(line 46) and `actions/checkout@v4` provisions a clean workspace, so on the *current* GitHub-hosted
runners `artifacts/` is empty at job start and A would return exit 1. The exposure is real but
conditional on: a self-hosted or reused runner, a workspace-caching change, any future step that
restores `artifacts/`, or **any local developer run** — where `artifacts/` routinely persists. A's
protection here is *incidental and environment-dependent*; B's is *explicit and
environment-independent*.

**GUARD 3b (ER-2 marker) in B is redundant, not additive.** Tested by emitting an artifact with
`normative_effect: "ADVISORY"`: **both** candidates failed (exit 1), because the harness's own
`test_report_declares_non_normative_status` fires first. B's CI-level marker check is
defense-in-depth against a future weakening of that harness test — it detects nothing the current
harness does not already detect.

No new controls were created for this analysis beyond NEG-5, the growth probe, and the cwd probe,
all run against throwaway copies.

---

## 10. CI Integration Analysis

Both wire into the same location: a `CHECK 10` block in `scripts/run_all_checks.sh`, invoked by the
`execution-checks` job of `.github/workflows/execution-checks.yml`, which runs on the
`x86_64` + `arm64` matrix. Both therefore produce **two** observation records per CI run, enabling
the cross-architecture comparison prepared in RD-006 §8.

Both gate `OVERALL_STATUS`, so a CHECK 10 failure produces `❌ CHECKS FAILED` / `DO NOT MERGE`.
Neither modifies the `wasm-compat` or `compare-determinism` jobs. Neither adds a dependency,
network call, service, or GPU/cloud requirement — both use stdlib `unittest`.

**Pre-existing, unrelated:** CHECK 7 and CHECK 8 fail in this environment for want of a
Docker/PostgreSQL daemon. Verified to fail identically on the pristine PRE-U1 base — attributable to
neither candidate.

---

## 11. Governance Boundary

Evidence considered: ADR-006 §8 (U-1 row + PRE-U1 note), ADR-006 INV-CI-1…3, ER-1…ER-7,
`RD-006_ARI_OBSERVABILITY.md` §7, CLAUDE.md authority precedence.

ADR-006 §8 already authorizes U-1 as a class of work and fixes its shape. Both candidates
instantiate that authorized shape. Neither alters an ADR, specification, invariant, or the
Constitution. The candidates differ only in the *mechanism* of a CI check — which ADR-006 places
outside the FROZEN boundary.

**Conclusion: selecting A or B requires only human implementation selection.** It requires no new
ADR, no ADR-006 amendment, no specification amendment, no constitutional decision, and no new
governance decision.

**One qualification, evidence-backed.** Two selection-adjacent questions are *not* settled by
existing repository evidence, and are carried to §18 as decision questions rather than resolved
here: (a) whether ER-4's verbatim-string obligation attaches to the CI check script or only to the
test module (§13); (b) whether the exact-pin vs floor choice (F-3) is an engineering preference or
an ER-6 governance posture. Neither blocks selection; both change *which* candidate best matches
intent.

---

## 12. FROZEN Boundary

| | PERMITTED BY ADR-006 | NOT COVERED BY ADR-006 |
|---|---|---|
| **A** | check script, `run_all_checks.sh` block, workflow upload paths | *(nothing identified)* |
| **B** | check script, `run_all_checks.sh` block, workflow upload paths | `CHANGELOG.md` modification — see note |

ADR-006 CI-1…CI-5 enumerate CI infrastructure as workflow definitions, check scripts, and the
test invocations inside them. Both candidates' code changes fall inside that enumeration.

**`CHANGELOG.md` note (no interpretation extended).** `CHANGELOG.md` is not enumerated in ADR-006's
CI inventory, and it is not a specification, ADR, or invariant document either. The repository
evidence does not place it on either side of the line. Recorded as: **DECISION REQUIRED — EVIDENCE
INSUFFICIENT** for the narrow question of whether a `CHANGELOG.md` entry is within U-1's authorized
scope. This is a scope question, not a semantic one — the entry's *content* is analysed in §13 and
is non-normative.

Neither candidate modifies anything inside the FROZEN semantic boundary. The harness is
byte-identical to its PRE-U1 blob under both.

---

## 13. Semantic / Non-Normative Safety

Scan performed over both commits for: hardcoded ARI values, canonical expected values, fixtures,
invariant declarations, specification references, conformance assertions, "must equal" assertions,
and changes to RI-PY / SPEC-002 / Constitution / ADRs.

| Probe | A | B |
|---|---|---|
| Hardcoded ARI values (`100000\|29999\|30000\|70000\|100001`) in the diff | **0 occurrences** | **7 occurrences**, all in `CHANGELOG.md` |
| Changes to RI-PY / SPEC-002 / Constitution / ADRs | none | none |
| New fixture files | none | none |
| Harness modified | no — byte-identical to `ee3be6f` | no — byte-identical to `ee3be6f` |

**Assessment of B's CHANGELOG values — stated fairly.** The five values appear in a passage
explicitly labelled *"Observations unchanged and now CI-visible (implementation-derived, reproduced
this session)"*, immediately followed by *"**Normative effect: NONE.** Per ADR-006 INV-CI-3, a
passing CHECK 10 is evidence, never approval. This task does not define ARI, does not select ARI
semantics, does not resolve RD-1, does not resolve NB-021, does not amend SPEC-002, and introduces
no fixture encoding an unresolved normative value (ER-7)."

This is **not** a hidden semantic effect and **not** an ER-7 violation: the values are labelled
implementation-derived, carry an explicit non-normative declaration, and are not consumed by any
executable assertion. All six ADR-006 clauses B cites (INV-CI-3, ER-1, ER-2, ER-5, ER-6, ER-7) were
verified to exist in `docs/ADR_006_CI_OUTSIDE_FROZEN_BOUNDARY.md`.

The residual concern is **duplication, not status**: the observed values now exist in two places —
the harness (authoritative) and `CHANGELOG.md` (narrative). If an authorized future decision changes
them, the CHANGELOG becomes stale. `CHANGELOG.md` is append-only by convention, so the drift is
historical-record drift rather than a live assertion.

### ER-4 — unsatisfied by BOTH candidates

ADR-006 ER-4 requires characterization tests wired into CI to carry **verbatim**:

> `THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.`

| Location | Carries it? |
|---|---|
| `core/test_ari_observability.py` @ `ee3be6f` (frozen harness) | **NO** — string absent |
| U-1-A check script | **NO** — string absent entirely |
| U-1-B check script | **NEAR** — lines 4 and 52 read `THIS CHECK CHARACTERIZES …`; `CHECK` ≠ `TEST`, so not verbatim |

The primary gap is in the **frozen harness**, which neither candidate may modify. Neither candidate
introduced this gap and neither can close it within U-1's scope. Carried to §18.

---

## 14. Risks Unique to U-1-A

| ID | Risk | Severity | Evidence |
|---|---|---|---|
| **A-R1** | **Skipped tests can report success.** All-skipped harness + non-empty `artifacts/` → exit 0, evaluator never executed, CI green. Precisely the "silently green" class U-1 exists to close. | **HIGH** (conditional — see §9 qualifier) | NEG-5 executed |
| **A-R2** | **Stale-evidence tolerance.** No pre-run deletion of the observation artifact; the existence guard can be satisfied by a prior run's file. | MEDIUM | NEG-5 stale variant |
| **A-R3** | **Exact pin reds CI on authorized growth.** Adding a 9th test fails CI until `EXPECTED_TESTS` is edited — and editing it under CI pressure is the ER-6 anti-pattern in adjacent form. | MEDIUM | growth probe: exit 1 |
| **A-R4** | **cwd-dependent.** No `cd $REPO_ROOT`; relies on the caller's working directory. Fails closed (exit 1), so it degrades safely. | LOW | invoked from `/` → exit 1 |

## 15. Risks Unique to U-1-B

| ID | Risk | Severity | Evidence |
|---|---|---|---|
| **B-R1** | **Scope beyond CI.** Modifies `CHANGELOG.md`, not enumerated in ADR-006's CI inventory. | MEDIUM (scope, not semantic) | §12 |
| **B-R2** | **ARI values duplicated outside the harness.** 5 values in `CHANGELOG.md`; drift risk if an authorized decision later changes them. | LOW–MEDIUM | §13 |
| **B-R3** | **Floor permits silent growth.** A 9th test — including an unauthorized ARI characterization case — passes without signal. The inverse of A-R3. | MEDIUM | growth probe: exit 0 |
| **B-R4** | **Higher surface.** 165 vs 103 lines; GUARD 3b redundant against the current harness. | LOW | §9 |
| **B-R5** | **ER-4 near-miss may read as satisfied.** `THIS CHECK CHARACTERIZES …` closely resembles the required string; a reviewer may credit ER-4 as met when it is not verbatim. | LOW–MEDIUM | §13 |

## 16. Risks Common to Both

| ID | Risk | Evidence |
|---|---|---|
| **C-R1** | **ER-4 unsatisfied**, primarily in the frozen harness. Not closable within U-1. | §13 |
| **C-R2** | **Prerequisite stack is mandatory.** Either candidate landing without `ee3be6f` leaves `main`'s harness unable to import. Structurally prevented — `ee3be6f` is the parent of both — but a cherry-pick onto `main` would produce it. | §17 |
| **C-R3** | **No cross-language observability.** Both CI legs run CPython; per ADR-006 §8.1 the x86_64/arm64 comparison cannot detect CORE-P0-002's cross-language divergence. Neither closes EC-6. | ADR-006 §8.1 |
| **C-R4** | **`8` is hardcoded in both** (as pin or floor) and must track authorized harness changes. | both scripts |
| **C-R5** | **~5,300 lines of `review/`+ADR documentation land with either**, from the shared prerequisite stack. | §3 |

---

## 17. Stack / Merge Consequences

| Question | Answer | Evidence |
|---|---|---|
| Fast-forwardable from `main`? | **Yes, both** | `git merge-base --is-ancestor origin/main <c>` → true for both |
| Conflict-free against `main`? | **Yes, both** — linear descent, 0 merge commits | `git rev-list --merges` → 0 |
| Can both coexist? | **No** | `git merge-tree b73e176 edd53ab` → exit 1 |
| Conflicting paths | `execution-checks.yml` (content), `check_10_ari_observability.sh` (add/add), `run_all_checks.sh` (content) | merge-tree output |
| Must exactly one be selected? | **Yes** | as above |
| If the wrong sibling merges first | The other becomes non-fast-forwardable and requires manual conflict resolution across all three files — i.e. re-deciding the mechanism under merge pressure. Landing both is impossible without rewriting one. | merge-tree |
| Prerequisite stack mandatory? | **Yes** — `22ab272 → 1d4bb37 → fc6669a → ee3be6f` precedes either candidate; forced by parentage | §3 |

**Required merge order (identical for either choice):**

```
22ab272 → 1d4bb37 → fc6669a → ee3be6f → <selected U-1>
```

No merge, rebase, cherry-pick, or history rewrite was performed. `merge-tree --write-tree` is a
read-only dry run that writes no ref.

---

## 18. Decision Questions

1. **Is A-R1 (skipped-test blindness) disqualifying?** It is the exact failure class U-1 exists to
   close, but on current GitHub-hosted runners it is masked by a clean workspace. Does the Authority
   weight the *class* of defect or its *current exploitability*?
2. **Pin or floor (F-3)?** Should CI red on *any* harness size change (A — every change forced
   through authorization), or only on shrinkage (B — authorized growth flows freely)? This is an
   ER-6 posture question, not a style question.
3. **Is a `CHANGELOG.md` entry within U-1's authorized scope?** Repository evidence is insufficient
   (§12).
4. **Does ER-4's verbatim obligation attach to the CI check script, the test module, or both?**
   Determines whether B's `THIS CHECK CHARACTERIZES …` is a near-miss or irrelevant, and whether a
   follow-up item against the frozen harness is required.
5. **Is replicating the five observed ARI values into `CHANGELOG.md` acceptable** given they are
   explicitly labelled non-normative but now live outside the harness?
6. **If A is selected, is a follow-up authorized** to add a skip guard and stale-artifact deletion —
   or must U-1 land exactly as reviewed?

---

## 19. Evidence Table

| # | Claim | Method | Result |
|---|---|---|---|
| E-1 | Both parents = `ee3be6f` | `git rev-parse b73e176^ edd53ab^` | confirmed |
| E-2 | Merge-base = `ee3be6f` | `git merge-base` | confirmed |
| E-3 | One commit each beyond stack | `git log ee3be6f..<c>` | confirmed |
| E-4 | Neither touches production code | `git diff --name-only <c>^ <c> -- core/ audit/ compliance/ packages/` | empty for both |
| E-5 | Neither touches docs/ADR-006/SPEC/Constitution | path-filtered `git diff` | empty for both |
| E-6 | `main` harness cannot import | `git show origin/main:… \| grep '^import unittest'` | no match |
| E-7 | ADR-006 absent from `main` | `git cat-file -e` | absent |
| E-8 | Both fast-forwardable | `git merge-base --is-ancestor` | true, both |
| E-9 | A and B conflict on 3 files | `git merge-tree --write-tree` | exit 1, 3 conflicts |
| E-10 | Both pass pristine 8/8 | executed in isolated trees | exit 0, both |
| E-11 | Both pass NEG-1…NEG-4 | executed | exit 1, both, all four |
| E-12 | **NEG-5 diverges** | executed | A exit 0 (stale artifact) / exit 1 (clean); B exit 1 |
| E-13 | **Growth to 9 diverges** | executed | A exit 1; B exit 0 |
| E-14 | **cwd portability diverges** | executed from `/` | A exit 1; B exit 0 |
| E-15 | ER-2 marker guard redundant | executed with `ADVISORY` marker | both exit 1 |
| E-16 | B's ADR-006 citations all exist | `grep` ADR-006 | INV-CI-3, ER-1/2/5/6/7 all present |
| E-17 | ER-4 string absent from harness and A; near-miss in B | `grep` all three | confirmed |
| E-18 | 7 ARI values in B's diff, 0 in A's | `git diff \| grep -oE` | confirmed |
| E-19 | `unittest` counts skips in `Ran N` | executed | `Ran 8 tests … OK (skipped=8)`, exit 0 |
| E-20 | CHECK 7/8 failures pre-existing | executed on pristine base | exit 1 on base too |

All executions used `git archive` extracts in a scratchpad directory. The repository working tree was
never modified; both branches are untouched.

---

## 20. Final Decision Status

# DECISION READY — HUMAN SELECTION REQUIRED

**Candidate A:** `b73e176`
**Candidate B:** `edd53ab`

**Strongest evidence supporting A**
Minimal authorized scope — 118 lines, three files, zero documentation change, zero ARI values
anywhere in the diff. It is the tightest possible instantiation of ADR-006 §8 U-1 and the easiest to
review line-by-line. Its exact-count pin forces *every* harness size change through explicit
authorization, which is the stricter reading of ER-6.

**Strongest evidence supporting B**
It closes a failure mode A does not: with all tests skipped, `unittest` reports
`Ran 8 tests … OK (skipped=8)` and exits 0. B fails this explicitly; A passes it whenever
`artifacts/` is non-empty. Since U-1's entire purpose is to eliminate silently-green CI, B covers
the objective more completely — and adds stale-artifact deletion and cwd-independence.

**Strongest risk of A**
A-R1 — skipped-test blindness, mitigated today only by clean CI workspaces, and absent entirely for
local runs.

**Strongest risk of B**
B-R1/B-R3 — scope beyond the CI inventory (`CHANGELOG.md`, carrying five ARI values into a narrative
document), and a floor that lets harness growth pass unsignalled.

**Are the differences material?**
**Yes.** Five independent MATERIAL differences, four verified by execution: skipped-test detection
(§7 row 10), stale-artifact handling (row 4), pin-vs-floor (row 6), cwd portability (row 19), and
scope (rows 22–23). The candidates are *not* interchangeable.

**What the Human Architectural Authority must decide**
The six questions in §18 — principally (1) whether A-R1 disqualifies A, (2) whether ER-6 posture
favours an exact pin or a floor, and (3) whether `CHANGELOG.md` is within U-1 scope. Then select
exactly one candidate and land it on the mandatory stack
`22ab272 → 1d4bb37 → fc6669a → ee3be6f → <selected>`.

---

*No implementation was selected. No file in either candidate was modified. No commit, PR, merge,
rebase, cherry-pick, or history rewrite was performed. This document is the sole output.*

**OBSERVATION — OUT OF SCOPE:** `aura-guard-v1.3` is not present in this session workspace, so the
§12 architectural separation (Core = Python engine; Guard = Rust middleware; no Python→Rust runtime
integration; Guard consumes neither ARI nor Constitution nor PoCA) could not be re-verified from
primary sources and is carried forward from the Engineering Baseline as stated. Nothing in either
U-1 candidate touches Guard, and U-1 must not be read as Core↔Guard integration — it provides
observability of current Core ARI behaviour only.
