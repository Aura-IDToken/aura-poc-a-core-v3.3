# ADR-006: CI/CD Infrastructure Is Outside the FROZEN Semantic Boundary

**Status:** ACCEPTED
**Date:** 2026-08-12
**Decision ID:** RD-006
**Accepted by:** Kamil Krasiński — Human Architectural Authority / Protocol Custodian
**Review path:** Claude (evidence preparation) → ChatGPT (review) → Human Architectural Authority (explicit acceptance)
**Spec Version:** v3.3
**Normative effect on protocol semantics:** NONE

---

## 0. Acceptance Record

The decision recorded in this ADR was **explicitly accepted by the Human Architectural
Authority (Kamil Krasiński)** under the bilateral decision protocol in force:

1. Claude may investigate, reproduce, trace and prepare decision material.
2. Claude MUST NOT make a governance or architectural decision on behalf of the project.
3. A proposed resolution must first be reviewed by ChatGPT.
4. The final decision requires explicit acceptance by Kamil Krasiński.
5. Only after bilateral acceptance may Claude formalize the verdict into ADR/SPEC/code.

**This ADR is the step-5 formalization.** It records a decision taken by the Human
Architectural Authority. It does not itself decide anything, and no part of it may be read
as an agent-originated determination.

### 0.1 Note on the form of this artifact

`RD-006_DECISION_BRIEF.md` §17 recorded *"Is an ADR required?"* as
**DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND**, and §16 recorded the same for the
recording location.

This artifact's form follows (a) the Human Architectural Authority's instruction to
formalize RD-006 in the repository's existing governance/document model, and (b) the
existing precedent in this repository — `docs/ADR_005_NO_FLOAT_RUNTIME.md`, the only
ADR-form document in `aura-poc-a-core-v3.3`.

**The general question is not thereby resolved.** Whether scoping rulings require an ADR,
and where such rulings are recorded, remains open for decisions other than RD-006. See §9.

### 0.2 Note on ADR numbering

`ADR-006` is scoped to **this repository's** sequence, following `ADR-005`. The
`AuraIDToken/aura-specification` repository maintains an independent ADR sequence
(`ADR-001_DOCUMENT_MODEL`, `ADR-001_REPOSITORY_STRUCTURE`). **No cross-reference exists
between the two corpora in either direction** — recorded as gap **G-8** in
`NB-021_FROZEN_SEMANTICS_AUDIT.md`. **G-8 remains open and is not resolved by this ADR.**

---

## 1. Context

The Aura Protocol v3.3 Iron Core is a frozen regulatory measurement instrument. A question
arose during remediation-readiness analysis as to whether CI/CD infrastructure — the
mechanisms that *verify* the instrument — falls inside the same FROZEN boundary as the
instrument itself.

The question was blocking, and specifically:

**Finding CORE-P1-006 / RM-10 — the determinism CI blind spot.** Verified at source:

| # | Fact | Evidence |
|---|---|---|
| 1 | `scripts/generate_determinism_report.py:36-38` imports exactly three modules — `core.offline_normalizer`, `audit.merkle`, `audit.signing`. **`core.evaluator` is not among them.** | source |
| 2 | The output vector `ari_vector_hash` hashes the **constitution vector**, not an ARI. **No ARI value is computed anywhere in the cross-platform determinism report.** | `scripts/generate_determinism_report.py:82-83` |
| 3 | The only CI step executing `PoCAEvaluator.evaluate` is CHECK 8 (`core.test_cr003_statelessness`), which is Docker-gated and asserts only `result_A == result_B` — an assertion that **holds under any division or rounding rule**. | `scripts/checks/check_8_cr003_statelessness.sh:16` |
| 4 | `core/test_ari.py` and `core/test_integration.py` assert ARI values. **Neither is invoked by any CI step.** | `scripts/run_all_checks.sh` |
| 5 | The characterization harness `core/test_ari_observability.py` was added to provide the missing observation point, and is **inert**, because no CI step invokes it. **It is also currently broken — see §1.1.** | `RD-006_ARI_OBSERVABILITY.md` §7; verified this session |

**Consequence.** The subsystem containing CORE-P0-001 … CORE-P1-005 is precisely the
subsystem the determinism pipeline does not observe. Until ARI computation is observed by
CI, no remediation of those findings can be verified to have worked.

**The blocked change was two lines**, drafted in `RD-006_ARI_OBSERVABILITY.md` §7 and
deliberately not applied pending this decision.

### 1.1 Finding recorded during formalization — the harness is currently non-executable

Verified this session at branch base `1d4bb37`:

```
$ python3 -m unittest core.test_ari_observability
NameError: name 'unittest' is not defined
  core/test_ari_observability.py:211, in ARIObservabilityTest(unittest.TestCase)
```

**Cause.** Commit `110a845` — *"Potential fix for pull request finding 'Module is imported
with `import` and `import from`'"*, authored by **Copilot Autofix**, an automated
code-quality tool — deleted the line `import unittest` while leaving
`from unittest import mock` and the module's use of `unittest.TestCase` in place.

```
$ git show 110a845 -- core/test_ari_observability.py
-import unittest
 from unittest import mock
```

**Confirmed by bisection.** At the harness's introducing commit `036ddd8` the module runs:
`Ran 8 tests in 0.056s — OK`. At HEAD it cannot be imported at all.
`RD-006_ARI_OBSERVABILITY.md` §6's report of 8 passing tests was accurate **when written**
and has since been invalidated by `110a845`.

**Why this matters to RD-006, and why it is recorded in this ADR rather than elsewhere.**

This is the blind spot described in §1 **manifesting in practice, on the very artifact
built to close it**. An automated tool removed a required import from a test module; the
module became non-executable; and **nothing detected it — because no CI step invokes the
module.** The interval between breakage and detection was bounded only by a human
happening to run it by hand.

**This finding is recorded, not remediated.** Repairing the module is a test-only change
under NB-021 **CASE D** and is **not** performed by this ADR, which is a formalization
artifact. It is registered as a precondition on U-1 (§8) and requires its own
authorization.

**No inference is drawn from this finding as to the correctness of the accepted decision.**
It is recorded because ADR-006 would otherwise assert, on the strength of a superseded
report, that an artifact executes when it does not.

---

## 2. Decision

**CI/CD infrastructure is outside the FROZEN semantic boundary of the Aura Core.**

### 2.1 CI/CD MAY

| # | Permitted |
|---|---|
| MAY-1 | **Observe** FROZEN Core behaviour |
| MAY-2 | **Execute** characterization and determinism tests |
| MAY-3 | **Detect** regressions |
| MAY-4 | **Enforce** already-established invariants |
| MAY-5 | **Generate** evidence |

### 2.2 CI/CD MUST NOT

| # | Prohibited |
|---|---|
| MUST-NOT-1 | **Modify** FROZEN semantic content |
| MUST-NOT-2 | **Reinterpret** normative semantics |
| MUST-NOT-3 | **Approve** semantic changes |
| MUST-NOT-4 | **Acquire or exercise** governance authority |

### 2.3 The load-bearing distinction

> **"Outside the FROZEN semantic boundary" is NOT "authorized to modify FROZEN semantics."**

These are different propositions and must not be conflated:

| Proposition | Status under this ADR |
|---|---|
| CI/CD artifacts may be modified without breaching the freeze | **ACCEPTED** — this is what the decision establishes |
| CI/CD may change what the Core computes | **PROHIBITED** — MUST-NOT-1 |
| CI/CD may change the meaning of what the Core computes | **PROHIBITED** — MUST-NOT-2 |
| CI/CD may authorize a change to FROZEN content | **PROHIBITED** — MUST-NOT-3 |
| CI/CD may serve as, or substitute for, governance authority | **PROHIBITED** — MUST-NOT-4 |

**CI/CD is an observer and an evidence generator. It is not a decision-maker.**
A green CI run is evidence that a stated property held on the observed inputs. **It is not
approval, not ratification, and not a normative claim.**

---

## 3. Decision Scope

### 3.1 In scope — artifacts this decision governs

All paths in `aura-poc-a-core-v3.3`:

| # | Artifact class | Path |
|---|---|---|
| CI-1 | Workflow definition | `.github/workflows/execution-checks.yml` |
| CI-2 | Master check runner | `scripts/run_all_checks.sh` |
| CI-3 | Individual check scripts | `scripts/checks/check_1…check_9*.sh` |
| CI-4 | Check helper programs | `scripts/verify_constitutional_purity.py`, `scripts/check_cr003_layer_boundary.py`, `scripts/generate_determinism_report.py`, `scripts/compare_determinism_reports.py` |
| CI-5 | Which existing test modules CI invokes | the `unittest` / `pytest` invocations inside CI-2 and CI-3 |

### 3.2 Out of scope — explicitly NOT governed by this decision

| Artifact | Remains governed by |
|---|---|
| `core/` production logic — **including `core/evaluator.py`** | NB-021 / RD-5 |
| `compliance/` production logic | NB-021 / RD-5 |
| Test modules themselves | NB-021 CASE D (already PERMITTED, independently of this ADR) |
| Documentation | NB-021 CASE A (already PERMITTED, independently of this ADR) |
| **What any check asserts** | `AGENTS.md` rule 10 — see §5, INV-3 |
| `aura-guard-v1.3` | Outside NB-021 entirely — zero occurrences of `frozen`/`freeze` |
| SPEC-002 and the specification corpus | Protocol Custodian; unaffected |

### 3.3 Non-transitivity

**This decision does not propagate through invocation.** That CI may invoke a test module,
and that the module may execute `core/evaluator.py`, does **not** place either the module
or `core/evaluator.py` outside the FROZEN boundary. The boundary status of an artifact is
determined by what the artifact *is*, not by what invokes it.

---

## 4. What This Decision Does NOT Do

Recorded explicitly, per the accepted decision text.

| # | This decision does NOT |
|---|---|
| NOT-1 | Define ARI |
| NOT-2 | Select ARI semantics |
| NOT-3 | Authorize any correction to `core/evaluator.py` |
| NOT-4 | Resolve NB-021 globally |
| NOT-5 | Resolve DR-002 |
| NOT-6 | Amend SPEC-002 |
| NOT-7 | Authorize production-code remediation |

**Additionally, and consistent with the above**, this decision does not resolve:

| # | Question | Remains |
|---|---|---|
| NOT-8 | RD-1 — does the specification define ARI? | **UNRESOLVED** |
| NOT-9 | RD-2 — APS-001 §8 / INV-008 trigger | **UNRESOLVED** |
| NOT-10 | RD-3 — AD-CA-007 numeric representation, including division | **UNRESOLVED** |
| NOT-11 | RD-4 — authoritative engine and penalty model | **UNRESOLVED** |
| NOT-12 | RD-7 — AD-CA-008 canonical serialization and hash domains | **UNRESOLVED** |
| NOT-13 | NB-000 / NB-001 / NB-002 — repository and identifier authority | **UNRESOLVED** |
| NOT-14 | CF-1 / CF-2 / CF-3 — the three document conflicts | **UNRECONCILED** |
| NOT-15 | Guard D1–D8 — audit-log integrity posture | **OPEN** (product decision; never governance-gated) |
| NOT-16 | v3.3's normative identity — no tag, no SHA, `[COMPUTED_AT_SEALING_v3.3]` unfilled (gap G-4) | **UNRESOLVED** |
| NOT-17 | Whether scoping rulings require an ADR, and where they are recorded (gap G-6) | **UNRESOLVED** — see §0.1 |

---

## 5. Invariants

Invariants established or preserved by this decision. **INV-CI-1 … INV-CI-5 are new and
scoped to CI/CD. INV-CI-6 … INV-CI-8 are pre-existing and are restated to record that this
decision does not weaken them.**

| ID | Invariant | Source |
|---|---|---|
| **INV-CI-1** | CI/CD MUST NOT modify FROZEN semantic content. | This decision, MUST-NOT-1 |
| **INV-CI-2** | CI/CD MUST NOT reinterpret normative semantics. | This decision, MUST-NOT-2 |
| **INV-CI-3** | CI/CD MUST NOT approve semantic changes. A passing CI run is evidence, never approval. | This decision, MUST-NOT-3 |
| **INV-CI-4** | CI/CD MUST NOT acquire or exercise governance authority. | This decision, MUST-NOT-4 |
| **INV-CI-5** | An observation emitted by CI/CD MUST carry its non-normative status where the observed value is implementation-derived. | `RD-006_ARI_OBSERVABILITY.md` §9; enforced by `test_report_declares_non_normative_status` |
| **INV-CI-6** | Tests MUST NOT be weakened merely to make implementation pass. **Unchanged by this decision.** | `AGENTS.md` rule 10 |
| **INV-CI-7** | Every conformance claim MUST have executable evidence. | `AGENTS.md` rule 9 |
| **INV-CI-8** | Human approval is required before merging protocol-affecting changes. **Unchanged by this decision.** | `AGENTS.md` rule 13; `CONSTITUTIONAL_DECREE.md` Art. X |

**INV-CI-3 is the invariant that keeps this decision narrow.** Without it, "CI is outside
the frozen boundary" could be misread as "CI can bless a change." It cannot. CI produces
evidence; the Human Architectural Authority produces decisions.

---

## 6. Evidence Requirements

Requirements on any CI/CD work performed under this decision.

| ID | Requirement | Rationale |
|---|---|---|
| **ER-1** | Any CI-executed observation of implementation-derived values MUST be labelled non-normative in code, in the emitted artifact, and in any report. | Prevents observation from becoming specification — `RD-006_DECISION_BRIEF.md` §15 |
| **ER-2** | Emitted observation records MUST carry `"normative_effect": "NONE"` and a characterization status marker, **enforced by a test that fails if the markers are removed**. | Established pattern — `RD-006_ARI_OBSERVABILITY.md` §5; the marker must survive the artifact outliving its context |
| **ER-3** | Determinism-report vectors covering the evaluator MUST carry `"status": "CHARACTERIZATION_ONLY"`. | `09_SAFE_WORK.md` §2 (S-20). Adding evaluator vectors to a document titled "determinism vectors" **without** this label would implicitly assert current output as reference output — the one path by which this decision could leak into normative territory |
| **ER-4** | Characterization tests wired into CI MUST carry verbatim: *"THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS."* | `03_CHARACTERIZATION_TEST_PLAN.md` §1 |
| **ER-5** | Characterization modules MUST include controls proving the harness **executes** the implementation rather than replaying constants. | `RD-006_ARI_OBSERVABILITY.md` §6.2 — four controls, patch-and-observe decisive |
| **ER-6** | A CI failure arising from a pinned characterization constant MUST NOT be resolved by editing the constant. It is resolved by recording the authorizing decision, or by treating the change as a finding. | `RD-006_ARI_OBSERVABILITY.md` §9 item 5; INV-CI-6 |
| **ER-7** | No fixture encoding an unresolved normative value may be introduced by CI work. | `09_CONFORMANCE_BOOTSTRAP_PLAN.md` §4; NB-021 CASE E — the only unanimous prohibition in that audit |

---

## 7. Merge Blockers

Conditions that continue to block a merge, notwithstanding this decision.

| ID | Blocker | Applies to |
|---|---|---|
| **MB-1** | Any change to `core/` or `compliance/` production logic | **BLOCKED** — NB-021 / RD-5, unaffected by this ADR |
| **MB-2** | Any change altering a computed value, hash, or byte sequence | **BLOCKED** — ROLE §4.1 Gate 2 |
| **MB-3** | Any CI change that adds a dependency | **CONTESTED** — `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §4.1 Gate 4: *"Adds dependency? → REJECTED."* **This ADR does not dispose of Gate 4.** Tooling additions (`ruff`, `mypy`, `pip-audit`, SBOM, CodeQL) remain contested on that independent ground |
| **MB-4** | Any change weakening what an existing CHECK asserts | **BLOCKED** — `AGENTS.md` rule 10 / INV-CI-6 |
| **MB-5** | Any fixture encoding an unresolved normative value | **BLOCKED** — ER-7 |
| **MB-6** | Any determinism vector added without the `CHARACTERIZATION_ONLY` label | **BLOCKED** — ER-3 |
| **MB-7** | Protocol-affecting changes without human approval | **BLOCKED** — `AGENTS.md` rule 13 |
| **MB-8** | A CI smoke step for `demo.py` | **BLOCKED** — depends on the `demo.py` correction, which is MB-1 |

**MB-3 deserves emphasis.** This decision unblocks the *category* of CI work. It does not
override ROLE §4.1 Gate 4. The CI items that add no dependency are the clean beneficiaries;
those that add tooling remain subject to a separate, undecided question.

---

## 8. What This Decision Unlocks

Subject to the conditions in §6 and §7.

| ID | Unlocked | Condition |
|---|---|---|
| **U-1** | **CI-based ARI observability** — wiring `core.test_ari_observability` into `scripts/run_all_checks.sh` and adding the observation artifact to the CI upload list (the two-line change drafted in `RD-006_ARI_OBSERVABILITY.md` §7) | ER-1, ER-2, ER-5 **and PRE-U1 below** |

> **PRE-U1 — blocking precondition on U-1.** `core/test_ari_observability.py` is currently
> **non-executable** (§1.1): commit `110a845` deleted its `import unittest`. Wiring the
> module into CI in its present state would add a check that fails at import, or — worse,
> depending on the invocation form — a step that silently collects zero tests while
> appearing to pass. **The module must be repaired before U-1 is executed.** The repair is a
> test-only change under NB-021 CASE D; it is **not** authorized by this ADR and requires its
> own authorization.
| **U-2** | **GB-2** — extending the determinism report to compute ARI | **ER-3 mandatory** (`CHARACTERIZATION_ONLY`) |
| **U-3** | **GB-3** — adding a CI step that runs `core/test_ari.py` and `core/test_integration.py` | ER-6; failures MUST NOT be resolved by weakening assertions (MB-4) |
| **U-4** | **EC-6** — *"ARI computation is observed by cross-platform CI"* | Requires U-1 and U-2 executed; **EC-6 is met only once records are compared across both existing architecture legs** |
| **U-5** | Wiring the characterization modules CH-01 … CH-15 into CI | ER-4, ER-5 |
| **U-6** | Running the full unit suite in CI — **105 locally-passing tests currently gate nothing** | MB-4 |
| **U-7** | Making `test_compliance.py` collectible — harness change, alters no assertion | none beyond MB-4 |
| **U-8** | Correcting the `develop` branch trigger, which references a branch that does not exist | none |

### 8.1 Standing limitation on U-4

**EC-6 being met does not make cross-*language* divergence observable.** Both existing CI
legs run CPython. An x86_64-vs-arm64 comparison detects intra-Python platform divergence
only; it **cannot** detect the rounding and division divergences (AG-06, AG-07) that
CORE-P0-002 and CORE-P0/P1-003 actually concern. Those require an independent
implementation, which remains blocked (§9, B-5).

**Recorded so that a green cross-platform run is not misread as cross-language determinism
evidence.**

---

## 9. What Remains Blocked

| ID | Blocked | Blocked by | Status |
|---|---|---|---|
| **B-1** | **ARI normative definition** — all 15 dimensions AG-01 … AG-15 | RD-1 | **UNRESOLVED** |
| **B-2** | **Production remediation** — any correction to `core/` or `compliance/`, including `core/evaluator.py` | RD-5 / NB-021 | **BLOCKED** |
| **B-3** | **NB-021 as a whole** | Protocol Custodian | **INDETERMINATE** — this decision resolves the CI/CD scope sub-question **only** |
| **B-4** | **DR-002** | Protocol Custodian | **UNRESOLVED** — identifier appears in no repository |
| **B-5** | **Independent implementation** | RD-1 + RD-3; 9/9 prerequisites unmet | **BLOCKED** |
| **B-6** | **All unresolved ARI semantic decisions** — division (AG-07, unregistered in any candidate list), rounding (AG-06, candidate only), bounds (AG-12), penalties (AG-10), dimension (AG-02), engine designation (RD-4) | RD-1, RD-3, RD-4 | **UNRESOLVED** |
| **B-7** | Canonical serialization and hash domains | RD-7 / AD-CA-008 — **"None approved"** | **UNRESOLVED** |
| **B-8** | Constitution Vector, `constitution.json`, CR-007 | AD-CA-005/006/007; `SPEC-002 §11.B` explicitly BLOCKED | **BLOCKED** |
| **B-9** | SPEC-002 conformance tests | `SPEC-002 §11` NOT READY | **BLOCKED** |
| **B-10** | Repository authority — NB-000, NB-001, NB-002 | Protocol Custodian | **UNRESOLVED** |
| **B-11** | Document conflicts CF-1, CF-2, CF-3 | Protocol Custodian | **UNRECONCILED** |

> **Critical framing.** This decision unlocks **observation**, never **correction**.
> CI may now *see* the findings; it still may not *fix* them. **RD-5 remains the gate on all
> remediation.**

---

## 10. Alternatives Not Adopted

`RD-006_DECISION_BRIEF.md` §18 presented six candidate wordings, **deliberately unranked and
marked non-normative**, to expose the drafting surface. The Human Architectural Authority
accepted a resolution corresponding in substance to W-3 and W-5 combined — exclusion, with
an explicit non-weakening reservation and an enforcement-mechanism framing.

**The rationale recorded below is derived from the accepted decision text itself. It is not
an agent-originated recommendation, and the brief made none.**

### Alternative 1 — Inclusion (brief W-1)

*"CI infrastructure falls inside the FROZEN boundary. No modification is permitted absent
an explicit authorization recorded under Decree Art. X."*

**Not adopted.** Incompatible with the accepted decision. Its consequences, recorded in the
brief §10, included: RM-10 permanently unobservable; the RD-006 harness permanently inert;
105 tests continuing to gate nothing; and Decree Art. X's *"Pre-commit Hooks (planned)"*
becoming unimplementable.

### Alternative 2 — Deferral until RD-5 (brief W-6)

*"RD-006 cannot be answered independently of NB-021 and is deferred until RD-5 is
resolved."*

**Not adopted.** The accepted decision resolves the CI/CD scope question **without**
resolving NB-021 globally (NOT-4, B-3), establishing that the two are severable.

### Alternative 3 — Partitioned scope (brief W-4)

*"Invoking an existing test module falls outside the boundary; adding a new check that
asserts a new property is a separate question and is not decided here."*

**Not adopted.** The accepted decision governs CI/CD infrastructure as a class (§3.1), and
addresses the concern that motivated partitioning through the MUST NOT list (§2.2) and the
evidence requirements (§6) rather than through a narrower scope.

### Alternative 4 — Unqualified exclusion (brief W-2)

*"CI infrastructure falls outside the FROZEN boundary."* — with no reservations.

**Not adopted.** The accepted decision attaches an explicit MUST NOT list. Unqualified
exclusion would leave INV-CI-1 … INV-CI-4 unstated and would permit CI to be read as
acquiring authority over the semantics it observes.

---

## 11. Consequences

### 11.1 Positive

- ✅ The determinism blind spot (RM-10 / CORE-P1-006) becomes closable
- ✅ ARI arithmetic becomes observable by CI for the first time
- ✅ EC-6 becomes achievable — with EC-7, the only two of nine exit criteria reachable
  without a specification decision
- ✅ 105 existing tests can be made to gate merges
- ✅ Future remediation authorized under RD-5 becomes **verifiable**, where it previously
  would not have been
- ✅ Decree Art. VI's cross-architecture mandate retains a means of discharge
- ✅ The evidence base for RD-1, RD-3 and RD-4 becomes measurable rather than anecdotal

### 11.2 Negative / risks accepted

- ⚠️ **Observation-to-specification leakage.** Wiring implementation-derived values into a
  pipeline that compares them across platforms risks their being read as reference values.
  **Mitigated by ER-1, ER-2, ER-3** — not eliminated. This is the principal residual risk.
- ⚠️ **Maintenance coupling.** Pinned characterization constants will fail when the
  evaluation path changes. That is the intended signal, but ER-6 must hold or the signal is
  lost.
- ⚠️ **Newly-visible failures.** Running 105 previously-ungated tests may surface failures.
  MB-4 forbids resolving them by weakening assertions.
- ⚠️ **Scope pressure.** "CI is outside the freeze" invites incremental broadening.
  §3.3 (non-transitivity) and §2.3 exist to resist it.

### 11.3 Neutral — recorded facts

- The CI modifications of 2026-07-24 (`da1e4ca`), 2026-08-09 (`295badf`, `bccab12`) are
  consistent with this decision. **This ADR does not ratify them**; gap **G-11** (no
  custodian authorization record for post-freeze changes) stands independently and is not
  addressed here.
- `PROTECTED_PATHS = ["core", "packages"]` (`scripts/verify_constitutional_purity.py:22-25`)
  is consistent with this decision. **It remains implementation behaviour and is not
  authority for it** — recorded as gap **EG-6** in the brief.

---

## 12. Evidence Trail

The evidence supporting this decision is preserved in the review packages. **This ADR does
not restate or replace that evidence with general reasoning.**

### 12.1 Primary evidence package

| Document | Contribution |
|---|---|
| `review/2026-08-12_REMEDIATION_READINESS/RD-006_DECISION_BRIEF.md` | **The decision brief.** 20 sections: exact normative evidence quoted verbatim (§5), evidence for inclusion I-1…I-7 (§6), evidence for exclusion E-1…E-10 (§7), contradictions C-1…C-7 (§8), ambiguities A-1…A-8 (§9), consequences (§10–§11), unblocked/blocked work (§12–§14), evidence gaps EG-1…EG-12 (§19) |

### 12.2 Cited evidence

| Document | Contribution |
|---|---|
| `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md` | FROZEN semantics audit; CASE A–F; gaps G-1…G-12; the INDETERMINATE verdict; §13 recording CI wiring as **INDETERMINATE** — the finding that generated RD-006 |
| `review/2026-08-11_ENGINEERING_BASELINE/RD-006_ARI_OBSERVABILITY.md` | The harness; the two-line change drafted and not applied (§7); the non-normative marker pattern (§5, §9); the four controls (§6.2). **§6's report of 8 passing tests was accurate when written and has since been invalidated by commit `110a845` — see §1.1.** |
| `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` | RD-6 as originally posed (§12); GB-2, GB-3 (§11); EC-6 (§14); the CI blind spot's three confirmations (§5.6) |
| `review/2026-08-11_ENGINEERING_BASELINE/09_SAFE_WORK.md` | S-20 and the `CHARACTERIZATION_ONLY` caveat (§2) |
| `review/2026-08-11_ENGINEERING_BASELINE/08_BLOCKERS.md` | P1-1, P1-6, P1-7; normative blockers §4 |
| `review/2026-08-12_REMEDIATION_READINESS/00_REMEDIATION_MATRIX.md` | RM-10; category and nature classification |
| `review/2026-08-12_REMEDIATION_READINESS/03_CHARACTERIZATION_TEST_PLAN.md` | ER-4 mandatory declaration; CH-01…CH-15 |
| `review/2026-08-12_REMEDIATION_READINESS/07_GOVERNANCE_DEPENDENCY_MAP.md` | CHAIN 1 — RD-6's dependency structure and execution boundary |

### 12.3 Governing sources cited in the brief

| Source | Bearing |
|---|---|
| `CONSTITUTIONAL_DECREE.md` Art. III, VI, VII, VIII, **X** | Art. X names the CI/CD Pipeline as an **enforcement mechanism** and lists Pre-commit Hooks as **"(planned)"** |
| `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §4.1, §6.5 | Entropy gates; **Gate 4 survives this decision** (MB-3) |
| `AGENTS.md` rules 9, 10, 13; Operating Constraints | INV-CI-6, INV-CI-7, INV-CI-8 |
| `AuraIDToken/aura-specification` — `VERSIONING.md`, `GOVERNANCE.md`, `aps/APS-000` | FROZEN defined for **documents**; gap G-1 — no definition applicable to an implementation |
| `AuraIDToken/aura-specification` — `adrs/ADR-001_DOCUMENT_MODEL.md` (**PROPOSED**) | `doc/ci/frozen-check` specified to enforce the freeze; job does not exist (G-10) |
| `docs/ops/OPS_PROTOCOL_CANONICAL.md` §4.1 | FROZEN ≠ SEALED; sealing has not occurred |

**All citations to `AuraIDToken/aura-specification` are conditional on NB-001** — which of
two repositories is authoritative — **which remains UNRESOLVED** (B-10, brief EG-11).

---

## 13. Verification

This ADR introduces no code and no CI change. Verification that it has not disturbed the
instrument:

```bash
$ git diff --stat            # over tracked production paths: empty
$ bash scripts/checks/check_2_integer_only.sh
✅ CHECK 2 PASSED: No float/sqrt/numpy in runtime core
$ bash scripts/checks/check_3_layer_separation.sh
✅ CHECK 3 PASSED: Layer separation maintained
$ python3 scripts/verify_constitutional_purity.py
✅ CONSTITUTIONAL PURITY CONFIRMED — IRON CORE STATUS: LEGAL
$ python3 scripts/check_cr003_layer_boundary.py
✅ CR-003 LAYER BOUNDARY CHECK PASSED
```

Harness state, verified this session (§1.1):

```bash
$ python3 -m unittest core.test_ari_observability
NameError: name 'unittest' is not defined          # broken by 110a845

$ git show 036ddd8:core/test_ari_observability.py  # introducing commit
Ran 8 tests in 0.056s — OK                          # confirmed by bisection
```

**Work authorized by this ADR has not been performed.** U-1 … U-8 remain to be executed as
separate, individually reviewable changes, each subject to §6 and §7 — and U-1
additionally to **PRE-U1** (§8).

---

## 14. References

- **Decision brief:** `review/2026-08-12_REMEDIATION_READINESS/RD-006_DECISION_BRIEF.md`
- **Governance role:** `CLAUDE.md`, `AGENTS.md`
- **Constitutional authority:** `CONSTITUTIONAL_DECREE.md`
- **Custodian role:** `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md`
- **Prior ADR in this repository:** `docs/ADR_005_NO_FLOAT_RUNTIME.md`
- **Freeze semantics audit:** `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md`
- **Observability harness:** `core/test_ari_observability.py`

---

## 15. Conclusion

**CI/CD infrastructure is outside the FROZEN semantic boundary of the Aura Core.**

CI/CD may observe the instrument, execute characterization and determinism tests, detect
regressions, enforce established invariants, and generate evidence.

**CI/CD may not modify FROZEN semantic content, reinterpret normative semantics, approve
semantic changes, or acquire governance authority.**

This decision unlocks **observation**. It unlocks no correction. The ARI normative
definition, production remediation, NB-021 as a whole, DR-002, independent implementation,
and every unresolved ARI semantic decision remain blocked.

**The instrument is unchanged by this decision. Only the ability to watch it has changed.**

---

**Decision ID:** RD-006
**Accepted by:** Kamil Krasiński — Human Architectural Authority
**Date:** 2026-08-12
**Normative effect on protocol semantics:** NONE
**Production code changed:** NONE
