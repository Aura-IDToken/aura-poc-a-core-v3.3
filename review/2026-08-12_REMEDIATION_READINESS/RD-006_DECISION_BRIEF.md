# RD-006 — DECISION BRIEF

**Prepared:** 2026-08-12
**Prepared by:** Claude (architectural / conformance audit role)
**Mode:** READ-ONLY. **No production code, CI file, specification, ADR, or fixture was modified.**
**Normative effect:** NONE.

> **BILATERAL DECISION PROTOCOL.** This brief prepares decision material only. It does not
> decide. Per the protocol in force: Claude investigates and prepares; ChatGPT reviews the
> proposed resolution; **Kamil Krasiński** provides explicit acceptance; only then may the
> verdict be formalized into ADR/SPEC/code.
>
> **This document answers neither YES nor NO, recommends no governance model, and ranks no
> alternative.**

---

## 1. DECISION ID

| Field | Value |
|---|---|
| **ID** | **RD-006** |
| Source | `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` §12 |
| Related | NB-021 (parent, INDETERMINATE) · RD-5 (sibling, broader) · GB-2, GB-3 (blocked work) |
| Finding served | CORE-P1-006 / RM-10 — the determinism CI blind spot |
| Register status | **Tracked in no specification document.** Exists only in the engineering review packages |
| Decision authority | Protocol Custodian (per `CONSTITUTIONAL_DECREE.md` Art. X, `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md`) |

---

## 2. EXACT DECISION QUESTION

> **Does CI infrastructure fall inside the FROZEN boundary of the Aura core?**

**Scope of "CI infrastructure"** — enumerated so the decision is not answered against an
undefined object. All paths are in `aura-poc-a-core-v3.3` at commit `22ab272`:

| # | Artefact | Path |
|---|---|---|
| CI-1 | Workflow definition | `.github/workflows/execution-checks.yml` |
| CI-2 | Master check runner | `scripts/run_all_checks.sh` |
| CI-3 | Individual check scripts | `scripts/checks/check_1…check_9*.sh` |
| CI-4 | Check helper programs | `scripts/verify_constitutional_purity.py`, `scripts/check_cr003_layer_boundary.py`, `scripts/generate_determinism_report.py`, `scripts/compare_determinism_reports.py` |
| CI-5 | Which existing test modules CI invokes | the `unittest`/`pytest` invocations inside CI-2/CI-3 |

**Explicitly NOT in scope of this question** (each is governed elsewhere and must not be
resolved by RD-006 as a side effect):

- `core/` and `compliance/` production logic → RD-5 / NB-021
- test modules themselves → NB-021 CASE D (already **PERMITTED**)
- documentation → NB-021 CASE A (already **PERMITTED**)
- what any check *asserts* → `AGENTS.md` rule 10, independent of RD-006
- `aura-guard-v1.3` → contains zero occurrences of `frozen`/`freeze`; NB-021 does not reach it

---

## 3. WHY RD-006 MATTERS

**Factual chain, each link independently verified:**

1. `scripts/generate_determinism_report.py:36-38` imports exactly three modules —
   `core.offline_normalizer`, `audit.merkle`, `audit.signing`. **`core.evaluator` is not
   among them.**
2. Its output vector `ari_vector_hash` hashes the **constitution vector**, not an ARI. The
   name is misleading; **no ARI value is computed anywhere in the cross-platform report.**
3. The one CI step that executes `PoCAEvaluator.evaluate` at all is CHECK 8
   (`core.test_cr003_statelessness`) — Docker-gated, and asserting only `result_A ==
   result_B`. That assertion **holds under any division or rounding rule** and therefore
   cannot detect CORE-P0-002 or CORE-P0/P1-003.
4. `core/test_ari.py` and `core/test_integration.py` do assert ARI values. **Neither is
   invoked by any CI step.**
5. The RD-006 characterization harness `core/test_ari_observability.py` exists, executes,
   and passes 8/8 — and is **inert**, because no CI step invokes it.

**Consequence.** The subsystem containing CORE-P0-001 … CORE-P1-005 is precisely the
subsystem the determinism pipeline does not observe.

> **The finding that is cheapest to close is the one whose absence conceals the other five.**
> Until ARI computation is observed by CI, **no remediation of the other five findings can
> be verified to have worked** — including any remediation authorized by a future RD-5, RD-1
> or RD-3 ruling.

**Magnitude of the blocked change.** Two lines, drafted in
`RD-006_ARI_OBSERVABILITY.md` §7 and deliberately **not applied**:

```bash
# scripts/run_all_checks.sh
python3 -m unittest core.test_ari_observability -v
```
```yaml
# .github/workflows/execution-checks.yml — appended to the existing upload list
            artifacts/rd-006-ari-observation.json
```

**Secondary consequence.** 105 locally-passing tests currently gate nothing —
`audit/test_audit.py` (47 tests), `core/test_ari.py`, `core/test_offline_normalizer.py`,
`core/test_integration.py`, `test_compliance.py` are **never invoked by CI**. Whether that
can be corrected is the same question.

---

## 4. GOVERNING SOURCES

Listed in the authority precedence of `AGENTS.md` §"Authority Precedence" / `CLAUDE.md`.

| Rank | Source | Bearing on RD-006 |
|---|---|---|
| 1 | `CONSTITUTIONAL_DECREE.md` Art. III, VI, VII, VIII, X | permitted-change list; mandatory checks; special permissions; sealing; **enforcement mechanisms** |
| 1 | `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §4.1, §6.5 | entropy gates; post-seal notation |
| 2 | `AuraIDToken/aura-specification` — `VERSIONING.md` (POL-VER-001), `GOVERNANCE.md` (GOV-001), `aps/APS-000` | the **document** lifecycle definition of FROZEN |
| 2 | `adrs/ADR-001_DOCUMENT_MODEL.md` — **Status: PROPOSED** | INV-DOC-008; the specified `doc/ci/frozen-check` job |
| 4 | `docs/ops/OPS_PROTOCOL_CANONICAL.md` §4.1 | *"Once sealed, the artifact is immutable"* |
| 6 | `AGENTS.md` rules 9, 10, 13; Operating Constraints | CI evidence; test-weakening prohibition; human approval |
| 9 | `scripts/verify_constitutional_purity.py:22-25` | the repository's **executable** definition of the protected zone |
| 9 | `scripts/run_all_checks.sh:16` | the freeze **declaration** itself |

**Governing source that does not exist:** no document in either corpus defines the term
**"CI infrastructure"**, assigns it a lifecycle status, or places it inside or outside any
boundary. This absence is the decision.

---

## 5. EXACT NORMATIVE EVIDENCE

Verbatim. Emphasis added only where noted.

### 5.1 The freeze declaration itself

> `scripts/run_all_checks.sh:16`
> ```
> echo "Specification: v3.3 (FROZEN)"
> ```

**Observation (not a conclusion).** This is the **only** occurrence of `FROZEN` in
`scripts/` or `.github/` in the entire repository. It is a line **inside a CI script**,
declaring **the specification** frozen. It does not declare the script frozen, and it does
not state what else the freeze covers.

### 5.2 Decree Art. III — the permitted-change list

> **### What IS Permitted**
> 1. ✔ Fixing critical security vulnerabilities **in changed lines**
> 2. ✔ Correcting provable mathematical errors
> 3. ✔ Fixing violations of Articles I-V
> 4. ✔ **Adding tests that validate constitutional compliance**
> 5. ✔ **Updating documentation to clarify existing behavior**
> 6. ✔ Implementing explicitly authorized tasks (see .github/copilot-tasks.md)

**Observation.** Six categories. **CI infrastructure is not among them, and is not among
the ten prohibited "improvements" either.** It is unlisted in both directions.

### 5.3 Decree Art. III — the Entropy Principle

> **Every change increases entropy.**
> If a proposed change does not:
> - Fix a security vulnerability in changed code
> - Correct a mathematical error
> - Enforce a constitutional requirement
> - Implement an authorized task
>
> Then it is **REJECTED**.

**Observation.** Four justifications. The third — *"Enforce a constitutional requirement"* —
is the only one under which a CI change could plausibly fall. Whether wiring a
characterization harness into CI *enforces* a constitutional requirement is **not stated**.

### 5.4 Decree Art. VI — mandatory checks

> **Before ANY code change is finalized:**
> **1. Bit-Identity Test** — `pytest core/test_bitwise_replay.py`
> - MUST pass on x86
> - **MUST pass on ARM (if available)**
> - Hashes MUST be identical

**Observation.** The Decree **mandates** a cross-architecture check. Executing that mandate
requires CI capability. The Decree does not state whether extending that capability is
itself permitted.

### 5.5 Decree Art. VII — special permissions

> **### Testing**
> New tests are permitted when they:
> - ✔ Validate constitutional compliance
> - ✔ Enforce bit-identity
> - ✔ Verify regulatory requirements
> - ❌ Do NOT introduce non-deterministic behavior

**Observation.** Grants permission for **new tests**. Silent on whether a permitted test may
be **executed by CI**. The harness at issue already exists under this permission; RD-006
concerns only its invocation.

### 5.6 Decree Art. X — enforcement mechanisms *(the most directly on-point text)*

> **## ARTICLE X – ENFORCEMENT AND COMPLIANCE**
> **### Enforcement Mechanisms**
> 1. **Pre-commit Hooks** *(planned)*
>    - Float detection
>    - Import validation
>    - Constant verification
> 2. **CI/CD Pipeline**
>    - Bit-identity tests
>    - Layer separation validation
>    - Entropy budget checks
> 3. **Code Review**
>    - Constitutional compliance checklist
>    - **Custodian approval required**

**Observation.** The Decree names the CI/CD Pipeline as an **enforcement mechanism** — an
instrument *of* the constitutional regime — and lists Pre-commit Hooks as **"(planned)"**,
i.e. as a mechanism **anticipated to be added in future**. The Decree does not state whether
enforcement mechanisms are themselves subject to the freeze they enforce.

### 5.7 Decree Art. VIII — versioning and sealing

> Any change to **core logic** creates a **NEW INSTRUMENT**, not a new version.
>
> **### Sealing Protocol**
> When this instrument is sealed:
> 1. ✔ All code frozen
> 2. ✔ SHA-256 checksum computed
> 3. ✔ Archived to M-DISC (physical media)
> 4. ✔ Bit-verified
> 5. ❌ NO further changes permitted

**Observation.** The new-instrument trigger is scoped to **"core logic"**. "All code frozen"
appears as step 1 of a **sealing protocol that has not been executed** (§5.11).

### 5.8 ROLE §4.1 — the entropy gates

> **1. Does this change fix a critical issue?**
> - Security vulnerability in changed code? → Acceptable
> - **Mathematical error? → Acceptable**
> - Constitutional violation? → Acceptable
> - Regulatory non-compliance? → Acceptable
> - "Improvement" or "optimization"? → **REJECTED**
>
> **2. Does this change preserve bit-identity?**
> - YES → Proceed to next question
> - NO → **REJECTED**
> - **UNCERTAIN → REJECTED**
>
> **4. Does this change increase entropy?**
> - **Adds dependency? → REJECTED**
> - Adds abstraction? → **REJECTED**

**Observation.** Gate 2 asks whether the change preserves **bit-identity**. A CI change
that only *invokes* an existing test **does not alter any computed value** — so unlike a
code fix, it does not obviously fail Gate 2. Gate 4's *"Adds dependency? → REJECTED"* is
directly engaged by CI items that install tooling (`ruff`, `mypy`, `pip-audit`), and not
engaged by an item that merely runs an existing module.

### 5.9 The specification corpus — FROZEN defined for documents only

> `VERSIONING.md` (POL-VER-001, **1.0-DRAFT**) §3
> | Status | Meaning | Mutable? |
> | **FROZEN** | **Immutable; content cannot change** | **No** |
>
> §4 — *"A FROZEN document **never receives a new version number**. A revision creates a new
> document."*
>
> `aps/APS-000` (**1.0-DRAFT**) §5
> | **FROZEN** | **Immutable** |

**Observation.** Both definitions govern **documents**. Neither mentions implementations,
repositories, build systems, or CI. Both are themselves **1.0-DRAFT** — by their own table,
*"Under active authoring; may change freely."*

### 5.10 ADR-001 — CI specified as the *enforcer* of FROZEN

> `adrs/ADR-001_DOCUMENT_MODEL.md` — **Status: PROPOSED**
> - INV-DOC-008: *"Frozen artifacts SHALL NOT be modified; corrections require a new
>   superseding artifact and an explicit link to the correction."*
> - `:84` — *"A CI job (`doc/ci/frozen-check`) **shall prevent direct modification of files
>   marked FROZEN** (by checking headers and approved status)."*

**Observation.** The only document that connects CI and FROZEN positions CI as the
**mechanism that enforces** the freeze. Two independent limits: the ADR is **PROPOSED**, not
accepted, with no `Accepted-by:` line; and **the `doc/ci/frozen-check` job does not exist in
either repository** (NB-021 gap G-10).

### 5.11 FROZEN ≠ SEALED

> `docs/ops/OPS_PROTOCOL_CANONICAL.md` §4.1 — *"**Once sealed**, the artifact is immutable."*
> `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §6.5 — *"**Post-Seal:** Archive receives notation:
> `v3.3-SEALED` · No further changes permitted to this version"*

**Observation.** The corpus binds absolute immutability to **sealing**. **Sealing has not
occurred:** no `v3.3-SEALED` notation, no M-DISC artefact, no custodial certificate, and
`docs/LEGACY_PROTOCOL.md:78` still reads:

> `SHA-256 checksum: [COMPUTED_AT_SEALING_v3.3]`

### 5.12 The repository's own executable protected zone

> `scripts/verify_constitutional_purity.py:21-25`
> ```python
> # === PROTECTED ZONES (LAW APPLIES HERE) ===
> PROTECTED_PATHS = [
>     "core",
>     "packages",
> ]
> ```

**Observation.** The repository's only **machine-checkable** statement of where "LAW
APPLIES" names two directories. `scripts/` and `.github/` are **not among them**. This is
implementation behaviour and **must not be treated as normative authority** — it is recorded
because it is the sole executable expression of a protected boundary anywhere in the
repository.

### 5.13 AGENTS.md — CI as a workflow stage and an evidence requirement

> **Conformance Restoration Workflow**
> Protocol Specification → Protocol Invariants → Conformance Test Matrix → Conformance Gap
> → Implementation → **CI evidence** → Adversarial review → Human approval
>
> Rule 9 — *"Every conformance claim must have **executable evidence**."*
> Rule 10 — *"Tests must not be weakened merely to make implementation pass."*
> Rule 13 — *"Human approval is required before merging protocol-affecting changes."*
>
> Operating Constraints — *"Governance-only updates must not modify source code, tests,
> **CI workflows**, compliance logic, policy logic, protocol specifications, constitutional
> documents, or ADRs."*

**Observation.** `AGENTS.md` treats **CI workflows as a category distinct from both source
code and tests**. The Operating Constraint restricts *governance-only* updates from touching
CI; it does not state whether *non-governance* updates may. Rule 9 makes executable evidence
a requirement, and CI is the mechanism that executes it.

---

## 6. EVIDENCE SUPPORTING **INCLUSION** OF CI INSIDE FROZEN

Presented without endorsement.

| # | Evidence | Strength |
|---|---|---|
| **I-1** | Decree Art. VIII sealing step 1 reads **"All code frozen"** — unqualified. CI check scripts (`.sh`) and helper programs (`.py`) are code. | Moderate. Weakened by §5.11: this is a *sealing* protocol, and sealing has not occurred. |
| **I-2** | Decree Art. III's permitted list is **exhaustive in form** — *"What IS Permitted"* followed by six numbered items, with the Entropy Principle stating that anything outside four justifications is **REJECTED**. CI infrastructure appears in neither list. Under a closed-list reading, absence means prohibition. | **Strong.** This is the principal argument for inclusion. |
| **I-3** | `AGENTS.md` Operating Constraints name **"CI workflows"** as a protected category alongside source code, tests, specifications and ADRs — indicating the corpus does regard CI as governed material rather than free space. | Moderate. The restriction is scoped to *governance-only* updates. |
| **I-4** | ROLE §4.1 Gate 4 — *"Adds dependency? → REJECTED"*. Several CI items (`ruff`, `mypy`, `pip-audit`, SBOM, CodeQL) add tooling dependencies and are directly caught. | **Strong for that subset.** Does not reach the two-line wiring change, which adds nothing. |
| **I-5** | Decree Art. I §10 — **NO UNAUTHORIZED CHANGES**. Absent an explicit authorization for CI modification, the default posture is refusal (Art. IV — *"IF IN DOUBT, REFUSE"*). | **Strong as a default rule.** It is a tie-breaker rather than a definitional statement. |
| **I-6** | CI scripts are the repository's **conformance evidence**. `AGENTS.md` rule 10 forbids weakening tests to make implementation pass; a freeze over CI protects the evidence base from erosion. | Moderate. Rule 10 already constrains *what checks assert*, independently of RD-006. |
| **I-7** | The freeze declaration is **physically located inside a CI script** (`run_all_checks.sh:16`), which could be read as the CI runner being part of the frozen instrument's self-description. | **Weak.** The line declares *the specification* frozen, not the script. |

---

## 7. EVIDENCE SUPPORTING **EXCLUSION** OF CI FROM FROZEN

Presented without endorsement.

| # | Evidence | Strength |
|---|---|---|
| **E-1** | Decree **Art. X names the CI/CD Pipeline as an ENFORCEMENT MECHANISM** — an instrument *of* the constitutional regime. A mechanism that enforces a boundary is structurally distinct from the material inside it. | **Strong.** The most directly on-point text in the corpus. |
| **E-2** | Art. X lists **"Pre-commit Hooks (planned)"**. The Decree explicitly anticipates that enforcement mechanisms **will be added in future**. A category the Decree expects to grow is difficult to read as frozen. | **Strong.** This is the clearest textual signal in either direction. |
| **E-3** | ADR-001 specifies `doc/ci/frozen-check` **to prevent modification of FROZEN files** — positioning CI as the enforcer of the freeze, not its subject. | Moderate. ADR-001 is **PROPOSED**, and the job does not exist (G-10). |
| **E-4** | Both corpus definitions of FROZEN (`VERSIONING.md`, `APS-000`) govern **documents**. Neither extends to implementations, repositories, or build systems. NB-021 gap **G-1**: *"No definition of FROZEN that applies to an implementation."* | **Strong.** The definitional gap is documented and undisputed. |
| **E-5** | The repository's only executable protected zone is `PROTECTED_PATHS = ["core", "packages"]` — **`scripts/` and `.github/` excluded**. | Moderate. **Implementation behaviour; must not be treated as authority** (see §19, EG-6). |
| **E-6** | **FROZEN ≠ SEALED** (§5.11). Absolute immutability attaches to sealing, which has not occurred. Art. VIII's *"All code frozen"* is step 1 of an unexecuted protocol. | **Strong.** |
| **E-7** | Decree Art. VI **mandates** a cross-architecture bit-identity check. Art. VI's mandate cannot be discharged without CI capability; freezing CI would freeze the means of satisfying a constitutional requirement. | Moderate-strong. Engages Entropy Principle justification 3 (*enforce a constitutional requirement*). |
| **E-8** | `AGENTS.md` places **"CI evidence"** as a stage in the mandated workflow and rule 9 requires **executable evidence** for every conformance claim. CI is the execution mechanism for a mandatory requirement. | Moderate. |
| **E-9** | Art. VIII's new-instrument trigger is scoped to **"core logic"**. A CI invocation line is not core logic; it changes no computed value and therefore passes ROLE §4.1 Gate 2 (bit-identity) without the uncertainty that defeats every code fix. | **Strong for the minimal wiring change specifically.** |
| **E-10** | **FACTUAL RECORD — see §7.1.** CI has been modified repeatedly and substantially in the six months after the freeze declaration was introduced. | **Recorded as fact. Explicitly NOT offered as precedent or authority** (§7.1). |

### 7.1 The factual record — recorded, not treated as authority

Verified from git history this session. The FROZEN declaration entered
`scripts/run_all_checks.sh` in commit `2501c37` (**2026-01-23**), in the same commit that
created the check infrastructure. CI was modified after that date as follows:

| Commit | Date | Change |
|---|---|---|
| `da1e4ca` | 2026-07-24 | CORE-006 — **cross-platform determinism CI added** |
| `295badf` | 2026-08-09 | CR-004 DB check integrated into execution checks |
| `bccab12` | 2026-08-09 | CR-003 — **CHECK 8 and CHECK 9 added** |

33 commits touch `.github/` or `scripts/`. **Six months of substantial CI evolution
occurred after the freeze declaration existed.** No custodian authorization record was
found for these, consistent with NB-021 gap **G-11**.

> **This is recorded as a FACT about practice, exactly as NB-021 records P-1, P-2 and P-3.**
> **It is NOT treated as normative authority, and it does NOT establish a precedent.**
> Per `CLAUDE.md`: authority must not be inferred from implementation behaviour. That
> practice diverged from — or was never constrained by — the stated rules is an observation
> the decision-maker may weigh; it is not itself an answer.

---

## 8. CONTRADICTIONS

Recorded under `CLAUDE.md`'s requirement to report rather than silently reconcile.

| # | Contradiction | Sides |
|---|---|---|
| **C-1** | **CI is both the enforcer and a candidate subject of the freeze.** | Decree Art. X names CI/CD as an enforcement mechanism (§5.6) and ADR-001 specifies a CI job to *prevent* modification of frozen files (§5.10) — while Art. VIII step 1 says *"All code frozen"* (§5.7). A mechanism cannot coherently be both the instrument that enforces a boundary and material sealed inside it, without a rule stating which reading prevails. |
| **C-2** | **The Decree anticipates CI growth while the Entropy Principle rejects unlisted change.** | Art. X lists Pre-commit Hooks as **"(planned)"** — an explicit expectation of future addition. Art. III's Entropy Principle rejects anything outside four justifications. **Adding the planned hooks would itself be an unlisted change.** |
| **C-3** | **Art. VI mandates a capability that Art. III may forbid maintaining.** | Art. VI requires the bit-identity test to pass **on ARM**. Discharging that mandate requires CI capability. If CI is frozen, the means of satisfying a constitutional requirement is frozen alongside it. |
| **C-4** | **FROZEN vs SEALED.** | `OPS_PROTOCOL_CANONICAL.md` §4.1 and `ROLE` §6.5 attach immutability to *sealing*; Art. VIII step 1 attaches "all code frozen" to the same unexecuted protocol; `run_all_checks.sh:16` declares FROZEN today. **Three timelines, one label.** |
| **C-5** | **The FROZEN definitions are themselves DRAFT.** | `VERSIONING.md` (POL-VER-001) and `APS-000` are both **1.0-DRAFT** — *"Under active authoring; may change freely"* — yet they are the corpus's only definitions of the status being asserted over v3.3. **The definition of immutability is itself mutable.** (NB-021 gap G-12.) |
| **C-6** | **INV-DOC-008 is cited but not in force.** | The only correction rule for frozen artefacts sits in ADR-001, **Status: PROPOSED**, with no `Accepted-by:` line, and its enforcing CI job **does not exist** (G-9, G-10). |
| **C-7** | **`AGENTS.md` classifies CI as governed material; `PROTECTED_PATHS` excludes it.** | Operating Constraints name "CI workflows" alongside source code and specifications; `verify_constitutional_purity.py:22-25` restricts the protected zone to `core` and `packages`. One is prose governance, one is executable enforcement, **and they disagree on scope.** |

**None of C-1 … C-7 is reconciled in this brief.**

---

## 9. AMBIGUITIES

| # | Ambiguity | Why it is unresolved |
|---|---|---|
| **A-1** | **"CI infrastructure" is undefined.** | No document defines the term. §2 enumerates five candidate artefact classes; the corpus supports no partition among them. A ruling that does not state its scope will be re-litigated at the first boundary case. |
| **A-2** | **Is Art. III's permitted list closed or open?** | It is titled *"What IS Permitted"* and paired with a rejection principle, suggesting closure. But it also permits *"explicitly authorized tasks"*, which is an open-ended escape hatch. **Whether omission means prohibition is the crux of I-2.** |
| **A-3** | **What is the frozen object?** | `run_all_checks.sh:16` freezes *"Specification: v3.3"*. NB-021 gap **G-1**: no definition of FROZEN applies to an implementation. It is unstated whether the freeze covers the specification, the implementation, the repository, or the instrument. |
| **A-4** | **Does "invoking an existing test" constitute a change to CI?** | The minimal item adds one invocation line for a module already permitted under Art. VII. Whether that is *modifying enforcement infrastructure* or *exercising an existing permission* is unstated. |
| **A-5** | **Is CI a "test" for Art. III item 4 purposes?** | Art. III item 4 permits *"Adding tests that validate constitutional compliance"*. CHECK scripts arguably are such tests. **`AGENTS.md` treats CI workflows and tests as distinct categories**, cutting the other way. |
| **A-6** | **Does RD-006 govern adding checks as well as running existing ones?** | Adding a *new* check that asserts something new is closer to a semantic act than wiring an existing harness. **The corpus draws no such line.** |
| **A-7** | **Does a ruling bind `aura-guard-v1.3`?** | Guard contains zero occurrences of `frozen`/`freeze`; NB-021 does not reach it. Whether an RD-006 ruling is repository-scoped or ecosystem-scoped is unstated. |
| **A-8** | **What is v3.3's identity, such that a CI change could preserve or break it?** | Gap **G-4**: no tag, no SHA, no release record; `[COMPUTED_AT_SEALING_v3.3]` unfilled. **A change cannot be assessed against an identity that has no referent.** |

---

## 10. CONSEQUENCES OF **YES** *(CI is inside the FROZEN boundary)*

**Stated as consequences, not as arguments.**

| # | Consequence |
|---|---|
| Y-1 | RM-10 / CORE-P1-006 becomes **permanently unobservable** for as long as the freeze stands. ARI arithmetic receives no cross-platform coverage. |
| Y-2 | The RD-006 harness (`core/test_ari_observability.py`, 8 passing tests) remains **permanently inert**. |
| Y-3 | **105 locally-passing tests continue to gate nothing.** |
| Y-4 | Any future remediation authorized by RD-5, RD-1 or RD-3 **cannot be verified to have worked**, because the pipeline that would verify it cannot be extended. Exit criterion **EC-6** becomes unreachable without a further ruling. |
| Y-5 | Decree Art. VI's ARM mandate is capped at its current implementation (C-3). |
| Y-6 | Art. X's *"Pre-commit Hooks (planned)"* becomes **unimplementable** (C-2). |
| Y-7 | Security tooling — `pip-audit`, SBOM, CodeQL, dependency scanning — cannot be added. Core CI remains the weakest of the three repositories, while Guard and the Conformance Kit both have stricter gates. |
| Y-8 | The `develop` branch trigger, which references a **branch that does not exist**, cannot be corrected. |
| Y-9 | A **precedent-practice conflict** requires disposition: the CI changes of 2026-07-24 and 2026-08-09 (§7.1) become retrospectively unauthorized, raising NB-021 question 7 (ratify or reverse). |
| Y-10 | The characterization work in `10` §2 remains available but **its results stay invisible to CI** — recorded in files, executed only by hand. |
| Y-11 | An exception procedure would be needed for any future CI change, and **no such procedure exists** (gap G-6: no category "non-normative defect correction"). |

---

## 11. CONSEQUENCES OF **NO** *(CI is outside the FROZEN boundary)*

**Stated as consequences, not as arguments.**

| # | Consequence |
|---|---|
| N-1 | GB-2 and GB-3 unblock. The two-line wiring may be applied; ARI computation becomes observable across the existing x86_64 and arm64 legs. |
| N-2 | EC-6 becomes achievable; EC-7 is already achievable. **These are the only two of nine exit criteria reachable without a specification decision.** |
| N-3 | 105 existing tests can be made to gate merges. |
| N-4 | Linting, typing, coverage and dependency-audit jobs become addable — subject to ROLE §4.1 Gate 4 (*"Adds dependency? → REJECTED"*), which is **not** disposed of by RD-006 and would still reject several of them. |
| N-5 | **A new boundary question arises immediately:** if CI is outside the freeze, what prevents a CI change from weakening what a check asserts? **`AGENTS.md` rule 10 already governs this** and is unaffected by RD-006 — but the ruling should say so explicitly, or the protection is assumed rather than stated. |
| N-6 | The CI changes of 2026-07-24 and 2026-08-09 (§7.1) become retrospectively consistent with the rules. **This does not ratify them** — G-11 (no custodian authorization record) stands independently. |
| N-7 | A scope boundary must be drawn: CI-1…CI-5 (§2) are outside, but the **test modules and production code they invoke remain governed by NB-021/RD-5**. Without that statement, RD-006 could be read as unfreezing by transitivity. |
| N-8 | `doc/ci/frozen-check` (ADR-001 `:84`) becomes implementable — CI could enforce the freeze on the material that *is* frozen. |
| N-9 | RD-006 is answered **without** answering RD-5. NB-021 remains INDETERMINATE; **all code-modifying work stays blocked.** |

---

## 12. WHAT WORK BECOMES UNBLOCKED UNDER **YES**

**None.**

`10` §3 lists twelve items (NB-A1 … NB-A12) gated on RD-006. Under YES, **all twelve remain
blocked**, and additionally acquire the status of *settled prohibition* rather than
*pending question*.

Work already available and **unaffected** by either answer — it does not depend on RD-006:

- characterization tests EN-01 … EN-14 (NB-021 CASE D, PERMITTED)
- observability EN-15 … EN-20
- Guard work EN-21 … EN-27 (Guard is outside NB-021 entirely)
- documentation EN-28 … EN-35 (CASE A, PERMITTED)

**A YES ruling does not reduce the currently-available work. It converts twelve open items
into closed ones.**

---

## 13. WHAT WORK BECOMES UNBLOCKED UNDER **NO**

The twelve items in `10` §3 — subject to the caveats in each row:

| ID | Work | Residual constraint after a NO ruling |
|---|---|---|
| NB-A1 | Wire `core.test_ari_observability` into `run_all_checks.sh` (1 line) | none — adds no dependency, changes no value |
| NB-A2 | Add the observation artifact to the CI upload list (1 line) | none |
| NB-A3 | Wire EN-01 … EN-14 characterization modules into CI | tests must already exist under CASE D |
| NB-A4 | Extend the determinism report to compute ARI | **must be labelled `CHARACTERIZATION_ONLY`** — otherwise it asserts current output as reference output, which is stop condition 8 |
| NB-A5 | Run the full unit suite in CI | may surface failures; **must not be resolved by weakening assertions** (rule 10) |
| NB-A6 | Make `test_compliance.py` collectible | harness change; alters no assertion |
| NB-A7 | Add `ruff` / `ruff format --check` | **ROLE §4.1 Gate 4 — adds a dependency** |
| NB-A8 | Add `mypy` | Gate 4 |
| NB-A9 | Add coverage reporting | Gate 4 |
| NB-A10 | Add `pip-audit`, SBOM, CodeQL | Gate 4 |
| NB-A11 | Remove or create the non-existent `develop` trigger | none |
| NB-A12 | Add a `demo.py` smoke step | depends on the `demo.py` fix, which is **RD-5-blocked** |

> **Note.** A NO ruling unblocks the *category*. **It does not dispose of ROLE §4.1 Gate 4**,
> which independently rejects dependency-adding changes. NB-A7 … NB-A10 would remain
> contested on that separate ground. **NB-A1, NB-A2, NB-A6 and NB-A11 add nothing and are
> the cleanest beneficiaries.**

---

## 14. WHAT REMAINS BLOCKED UNDER **EITHER** ANSWER

RD-006 is narrow. It does not touch:

| Work | Blocked by | Unaffected by RD-006 |
|---|---|---|
| Any code change to `core/` or `compliance/` | **RD-5 / NB-021** | ✔ |
| Fixing the `zip()` dimension fail-open | RD-2 + NB-015 + RD-5 | ✔ |
| Fixing or ratifying division semantics | **RD-3** — unregistered in any candidate list | ✔ |
| Fixing or ratifying rounding semantics | RD-3 — candidate only | ✔ |
| Defining or bounding ARI | **RD-1** — 15/15 dimensions undecided | ✔ |
| Designating an authoritative engine / penalty model | RD-4 | ✔ |
| Unifying the three JSON canonicalizations | RD-7 / AD-CA-008 — "None approved" | ✔ |
| Generating a Constitution Vector; `constitution.json`; CR-007 | AD-CA-005/006/007; `SPEC-002 §11.B` | ✔ |
| Writing any SPEC-002 conformance test | `SPEC-002 §11` NOT READY | ✔ |
| Building an independent implementation | RD-1 + RD-3 (9/9 prerequisites unmet) | ✔ |
| Resolving CF-1, CF-2, CF-3 | Custodian only | ✔ |
| Resolving NB-000 / NB-001 / NB-002 | Custodian only | ✔ |

> **Critical framing.** RD-006 unblocks **observation**, never **correction**. Under NO, CI
> can *see* the defects; it still cannot *fix* them. Under YES, CI can neither see nor fix
> them. **RD-5 remains the gate on all remediation under either answer.**

---

## 15. DOES THE DECISION CHANGE NORMATIVE SEMANTICS?

# NO — under either answer.

| Test | Assessment |
|---|---|
| Does it select a protocol semantic? | **No.** RD-006 selects no division rule, rounding rule, ARI definition, bound, encoding, hash domain, or failure mode. |
| Does it change a computed value? | **No.** Neither answer alters any output of any function. |
| Does it change a hash or byte sequence? | **No.** |
| Does it make implementation behaviour normative? | **No — provided NB-A4 carries the `CHARACTERIZATION_ONLY` label.** Adding evaluator vectors to a document titled "determinism vectors" **without** that label would implicitly assert current output as reference output. **This is the one path by which RD-006 could leak into normative territory, and it is controllable by labelling.** |
| Does it resolve NB-021? | **No.** RD-006 is a **scoping** sub-question. NB-021 remains INDETERMINATE either way. |

**RD-006 is a decision about the *extent of a boundary*, not about the *content of a
semantic*.** This distinguishes it from RD-1 … RD-4 and RD-7, each of which does select a
semantic.

---

## 16. DOES THE DECISION REQUIRE AN AMENDMENT TO AN EXISTING DOCUMENT?

**DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND.**

The corpus does not establish where such a ruling would be recorded. What can be stated
factually:

| Candidate location | Consideration |
|---|---|
| `CONSTITUTIONAL_DECREE.md` Art. III or Art. X | Art. X already names the CI/CD Pipeline; a scope clause would sit naturally there. **But the Decree's own Art. VIII says it becomes *"permanent and immutable"* after sealing — and its amendment procedure before sealing is not stated.** |
| `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §4.1 | Would clarify how the gates apply to non-value-changing changes. |
| `AGENTS.md` Operating Constraints | Already names "CI workflows"; **lowest-authority option** (precedence rank 6) and cannot override the Decree (rank 1). |
| `VERSIONING.md` / `APS-000` | Would fix gap G-1 by defining FROZEN for implementations. **Both are 1.0-DRAFT (C-5).** Requires NB-001 to be answered first — *which* specification repository is authoritative. |
| A new ADR | See §17. |
| No amendment; ruling recorded as a custodian decision | Consistent with `Decree Art. X` (*"Custodian approval required"*), but leaves gap G-6 open — no artefact form exists for such a ruling. |

**Two structural obstacles are recorded, not resolved:**

- **NB-001 is unanswered.** Two `aura-specification` repositories exist —
  `AuraIDToken/` (full corpus) and `aura-nomos/` (one-line README). **Amending "the
  specification" is not currently a well-defined act.**
- **Gap G-6** — the corpus has no category, procedure, authority record, or artefact form for
  a scoping ruling of this kind.

---

## 17. IS AN ADR REQUIRED?

**DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND.**

**No ADR has been created by this brief**, per the constraints in force.

Facts bearing on the question:

| Fact | Source |
|---|---|
| ADRs exist as an artefact class in the specification repository | `adrs/` — ADR-001 (**PROPOSED**), ADR-001_REPOSITORY_STRUCTURE |
| The core repository has one ADR-shaped document | `docs/ADR_005_NO_FLOAT_RUNTIME.md` |
| The two repositories use **different ADR conventions**, and **no cross-reference exists** between the corpora | NB-021 gap **G-8** |
| ADR-001, the document defining the ADR model itself, is **PROPOSED** with no `Accepted-by:` line | `adrs/ADR-001_DOCUMENT_MODEL.md:4` |
| `VERSIONING.md` states APPROVED documents change *"Via RFC/ADR only"* — **but that governs documents, and RD-006 does not modify a document** | `VERSIONING.md` §3 |
| **No rule states whether a scoping ruling requires an ADR** | gap G-6 |

**Observation.** The mechanism that would determine whether an ADR is required is itself in
PROPOSED status. **A decision to require an ADR would rely on a document not yet in force.**

---

## 18. MINIMAL DECISION WORDING CANDIDATES

> ### ⚠ NON-NORMATIVE — ILLUSTRATIVE DRAFTING AID ONLY
>
> **These are candidate *wordings*, not candidate *answers*.** None is recommended, none is
> preferred, none is a default, and **they are deliberately not ranked**. They exist so that
> the decision authority can see the drafting surface — in particular which scope questions
> a ruling must settle (§9 A-1, A-6, A-7) to avoid immediate re-litigation.
>
> **Adopting any wording below without the bilateral protocol in §0 would be invalid.**
> Presence in this list confers no status whatsoever.

**W-1 — Inclusion, unqualified**
> *"CI infrastructure, including workflow definitions, check scripts and check helper
> programs, falls inside the FROZEN boundary of aura-poc-a-core-v3.3. No modification is
> permitted absent an explicit authorization recorded under Decree Art. X."*

**W-2 — Exclusion, unqualified**
> *"CI infrastructure falls outside the FROZEN boundary. The FROZEN boundary covers the
> measurement instrument — `core/` and `compliance/` production logic — and not the
> mechanisms that verify it."*

**W-3 — Exclusion with an explicit non-weakening reservation**
> *"CI infrastructure falls outside the FROZEN boundary. This ruling does not authorize any
> change to what an existing check asserts; `AGENTS.md` rule 10 continues to apply in full.
> This ruling does not extend to the test modules or production code that CI invokes, which
> remain governed by NB-021."*

**W-4 — Partitioned scope**
> *"Invoking an existing, already-permitted test module from CI falls outside the FROZEN
> boundary. Adding a new check that asserts a new property is a separate question and is not
> decided here."*

**W-5 — Enforcement-mechanism framing**
> *"CI infrastructure is an enforcement mechanism under Decree Art. X, not material subject
> to the freeze it enforces. It may be extended where the extension enforces an existing
> constitutional requirement and adds no dependency."*

**W-6 — Deferral**
> *"RD-006 cannot be answered independently of NB-021 and is deferred until RD-5 is
> resolved."*

**Scope elements any wording must settle** — regardless of direction:

1. Which artefact classes CI-1 … CI-5 are covered (A-1)
2. Whether *invoking* an existing test differs from *adding* a check (A-4, A-6)
3. Whether `AGENTS.md` rule 10 survives unchanged (N-5)
4. Whether the ruling reaches `aura-guard-v1.3` (A-7)
5. Disposition of the 2026-07-24 / 2026-08-09 CI changes (Y-9, N-6)
6. Whether ROLE §4.1 Gate 4 (dependency rejection) is affected (N-4)

---

## 19. EVIDENCE GAPS

| # | Gap | Effect on RD-006 |
|---|---|---|
| **EG-1** | **No definition of "CI infrastructure"** anywhere in either corpus. | The question's object is undefined (A-1). |
| **EG-2** | **No definition of FROZEN that applies to an implementation.** Both corpus definitions govern documents. *(NB-021 G-1)* | The boundary being scoped has no definition for this subject class. |
| **EG-3** | **No defined transition into or out of FROZEN** for the v3.3 instrument. *(G-2, G-3)* | Status is asserted, not recorded. |
| **EG-4** | **No recorded identity for v3.3** — no tag, no SHA, no release record; `[COMPUTED_AT_SEALING_v3.3]` unfilled. *(G-4)* | A change cannot be assessed against a non-existent referent (A-8). |
| **EG-5** | **No category "non-normative change"** and no procedure, authority record, or artefact form for a scoping ruling. *(G-6)* | Affects §16 and §17 directly. |
| **EG-6** | `PROTECTED_PATHS = ["core", "packages"]` is **implementation behaviour, not authority.** | E-5 must be weighted accordingly. **It is the only executable expression of a protected boundary, and it has no normative standing.** |
| **EG-7** | **No cross-reference between the two governance corpora** in either direction. *(G-8)* | Unclear whether the specification's FROZEN definition governs the core repository at all. |
| **EG-8** | **ADR-001 is PROPOSED**; INV-DOC-008 is not in force; `doc/ci/frozen-check` **does not exist**. *(G-9, G-10)* | E-3 and §17 rest on a document not in force. |
| **EG-9** | **No custodian authorization record** for any post-freeze change. *(G-11)* | §7.1 cannot be read as authorized practice. |
| **EG-10** | **The FROZEN definitions are themselves 1.0-DRAFT.** *(G-12, C-5)* | The definition of immutability is mutable. |
| **EG-11** | **NB-001 unanswered** — which `aura-specification` is authoritative. | Every specification-corpus citation in this brief is conditional on it. Citations here are to `AuraIDToken/aura-specification` @ `62d2d6b`; the repository this session was scoped to (`aura-nomos/`) contains **a one-line README and nothing else**. |
| **EG-12** | **No stated relationship between RD-006 and RD-5.** | Whether RD-006 is genuinely severable from NB-021, or merely appears so, is itself unestablished (W-6). |

---

## 20. EXACT QUESTION FOR THE HUMAN DECISION AUTHORITY

**To: Kamil Krasiński, acting as Protocol Custodian / architectural authority.**
**Review path: ChatGPT review → explicit human acceptance → only then formalization.**

> **PRIMARY QUESTION**
>
> **Does CI infrastructure — specifically `.github/workflows/execution-checks.yml`,
> `scripts/run_all_checks.sh`, `scripts/checks/*.sh`, and the check helper programs in
> `scripts/` — fall inside the FROZEN boundary of `aura-poc-a-core-v3.3` v3.3?**

**Six sub-questions a complete ruling must also settle** (from §18; each has been shown to
be independently unresolved):

> **SQ-1 — Scope.** Does the ruling cover all of CI-1 … CI-5 (§2), or does it partition
> them?
>
> **SQ-2 — Granularity.** Does *invoking* an existing, already-permitted test module differ
> from *adding a new check that asserts a new property*?
>
> **SQ-3 — Non-weakening.** Does `AGENTS.md` rule 10 (*"Tests must not be weakened merely to
> make implementation pass"*) continue to apply in full, independently of this ruling?
>
> **SQ-4 — Transitivity.** Does the ruling reach the test modules and production code that
> CI invokes, or does it stop at the CI artefacts themselves?
>
> **SQ-5 — Retrospective disposition.** How are the CI changes of 2026-07-24 (`da1e4ca`) and
> 2026-08-09 (`295badf`, `bccab12`) treated — ratified, reversed, or left unaddressed?
> *(See §7.1. These are recorded as facts, not as precedent.)*
>
> **SQ-6 — Recording.** Where is the ruling recorded, and does it require an ADR?
> *(§16 and §17 are both* **DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND.***)*

**Material the decision authority should have to hand:**

| Item | Where |
|---|---|
| The two-line change at issue | `RD-006_ARI_OBSERVABILITY.md` §7 — drafted, **not applied** |
| What YES forecloses | §10 (Y-1 … Y-11) |
| What NO releases | §13 (NB-A1 … NB-A12), with Gate 4 caveats |
| What is blocked either way | §14 — **all remediation; RD-5 is the gate** |
| The seven contradictions | §8 |
| The twelve evidence gaps | §19 |

---

## SUMMARY OF FINDINGS REQUIRING THE STANDARD FORMULA

Per the rule in force, where the repository does not establish the answer:

| Item | Finding |
|---|---|
| **The primary question** | **DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND.** |
| §16 — amendment required? | **DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND.** |
| §17 — ADR required? | **DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND.** |
| SQ-1 … SQ-6 | **DECISION REQUIRED — NO AUTHORITATIVE ANSWER FOUND** for each. |

**Basis:** the corpus contains no definition of "CI infrastructure", no definition of FROZEN
applicable to an implementation (EG-2), and no rule placing enforcement mechanisms inside or
outside the material they enforce (C-1). **The question is genuinely open in the documents,
not merely unlocated by this search.**

---

```
STATUS:                 DECISION READY
NORMATIVE CHANGE:       NONE
PRODUCTION CODE CHANGE: NONE
DECISION REQUIRED FROM: HUMAN ARCHITECTURAL AUTHORITY
```

---

*This document has no normative effect. It answers neither YES nor NO, recommends no
governance model, ranks no alternative, creates no ADR, amends no specification, and
modifies no code or CI. It prepares a decision that remains to be taken.*
