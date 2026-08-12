# 00 — REMEDIATION MATRIX

**Phase:** Remediation Readiness & Controlled Engineering
**Date:** 2026-08-12
**Mode:** READ-ONLY. **No production code, specification, ADR, fixture, CI file or governance artefact was modified.**
**Normative effect:** NONE.

---

## §0 What This Package Is

This package converts the findings already established in
`review/2026-08-11_ENGINEERING_BASELINE/` into a **controlled remediation plan**.

It does **not** redesign Aura, does not invent missing semantics, and does not convert
implementation behaviour into specification. Where the repository corpus does not decide
something, this package writes **ARCHITECTURAL DECISION REQUIRED** and stops there.

**Direction of travel enforced throughout:**

```
Decision → Specification → Implementation → Test → Evidence
```

This package sits at the far **left** of that chain and does not cross rightwards.

---

## §1 Evidence Provenance

Unlike the baseline package, this phase was executed with **primary access to all four
repositories**. Every citation below is first-hand unless marked otherwise.

| Ref | Source | Commit / state | Access this session |
|---|---|---|---|
| CORE | `AuraIDToken/aura-poc-a-core-v3.3` | `f3a87cc` (branch base) | **primary — read + executed** |
| SPEC | `AuraIDToken/aura-specification` | `62d2d6b` | **primary — read** |
| GUARD | `AuraIDToken/aura-guard-v1.3` | `443f72e` | **primary — read** |
| NOMOS | `aura-nomos/aura-specification` | `eb2a4ec` | **primary — read (README only, 1 line)** |
| BASE | `review/2026-08-11_ENGINEERING_BASELINE/` (20 files) | in-tree | **primary — read** |

**Note on GUARD.** `443f72e` is the *same commit* the `GUARD-G1_INTEGRITY_DESIGN_BRIEF.md`
pinned. The nine-field digest and the absence of `violations` were **re-verified at source
this session** (`src/chain.rs:25-49`), not carried over on trust.

**Note on NOMOS.** `aura-nomos/aura-specification` contains exactly one file of content —
a one-line `README.md` reading `# aura-specification`. It contains no APS documents, no
SPEC-002, no invariants. This is the repository this session was scoped to; the corpus
actually cited throughout is `AuraIDToken/aura-specification`. **This is NB-001, and it is
unresolved.** See §6.

### 1.1 Facts re-verified at primary source this session

| Claim | Verified | Source |
|---|---|---|
| SPEC-002 is `0.3-DRAFT`, `Normative effect: NONE until APPROVED` | **YES** | `specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md:4,11` |
| **No SPEC-002 v0.4 exists** | **YES** — sole `v0.4` hit corpus-wide is `ROADMAP.md:53`, a release milestone | SPEC |
| AD-CA-007 `UNRESOLVED`; `round-half-to-even` **candidate only** | **YES** | `SPEC-002:381` |
| AD-CA-007 candidate set lists **no division rule** | **YES** — candidates are `32`, `100000`, `signed int32`, `little-endian`, `Dictionary-Based Embedding`, `round-half-to-even` | `SPEC-002:108,141,381` |
| AD-CA-008 `UNRESOLVED`, **"None approved"** | **YES** | `SPEC-002:382` |
| **`DR-002` appears nowhere in the specification corpus** | **YES** — zero hits across all `*.md` | SPEC |
| ARI has **no normative definition**; sole corpus definition defers to the implementation | **YES** — `glossary/GLOSSARY.md:27-28`: *"A deterministic measurement value computed by RI-PY"* | SPEC |
| Guard chain digest covers **nine** fields; `violations` absent | **YES** | `GUARD src/chain.rs:36-47` |

### 1.2 Corrections to the baseline package

Recorded because the matrix below depends on them. Both are minor and neither changes any
verdict.

| # | Baseline statement | Verified state at current HEAD | Effect |
|---|---|---|---|
| C-1 | `08_BLOCKERS.md` P0-2 / `05_CORE_REMEDIATION_READINESS.md` §5.5: *"`ConsistencyCalculator([200000,0,0,0], …)` → **raises** `ValueError`"* | The **constructor does not validate**. `ConsistencyCalculator.__init__` (`compliance/consistency.py:23-26`) stores the vector unchecked. The `ValueError` is raised **lazily**, inside `_semantic_alignment` (`:87-91`), and only when `calculate()` is reached with a structurally valid event. Reproduced this session. | The engine-divergence finding **stands unchanged** — the two engines still have opposite validation postures. Only the *location* of the check is corrected. Matters for characterization test design (see `03`, CH-08). |
| C-2 | Baseline cites `compliance/consistency.py:96` for the `zip()` site and `:82/:85/:88` for the guards | At current HEAD the `zip()` site is **`:93`**, the zero-guard is **`:84`**, and the magnitude guards are **`:87`** and **`:90`** | Line-number drift only (baseline was written against `9c6a5d8`). All line references in this package are to current HEAD. |

---

## §2 Category Definitions

Every finding is assigned exactly one **primary category** and one **nature**.

### 2.1 Categories

| Category | Meaning |
|---|---|
| **GOVERNANCE** | Blocked on an authority ruling about *who may decide* or *what may be changed* |
| **NORMATIVE** | Blocked on a specification stating *what the correct behaviour is* |
| **ARCHITECTURAL** | Blocked on a design choice with more than one defensible answer, not yet made |
| **ENGINEERING** | The code contradicts its own stated contract, or is inconsistent with itself |
| **SECURITY** | Has a direct integrity, tamper-detection, or fail-open consequence |
| **TESTING** | A verification-coverage gap |
| **DOCUMENTATION** | A stated claim that is not true of the implementation |

### 2.2 Nature — the three-way distinction required by the task

This is the load-bearing distinction of the whole package.

| Nature | Definition | Test that assigns it | May engineering act alone? |
|---|---|---|---|
| **BUG** | The implementation contradicts **its own documented contract**, or is internally inconsistent. Wrongness is demonstrable **without consulting any specification**. | *"Can I show this is wrong using only artefacts already in this repository?"* → YES | **YES** (subject to the NB-021 freeze gate, which is separate) |
| **UNDEFINED SEMANTICS** | The implementation exhibits **one** of several possible behaviours, and **no authority has selected** which is correct. The code is not "wrong" — the question has no answer yet. | *"Would I have to choose a semantic to call this wrong?"* → YES | **NO** — acting would make implementation behaviour normative |
| **GOVERNANCE BLOCKER** | The obstacle is not the code and not the specification, but an **unanswered question about authority** — what may be changed, by whom, and under what identity. | *"Is the obstacle a permission rather than a fact?"* → YES | **NO** |

**A finding may carry a BUG aspect and an UNDEFINED SEMANTICS aspect simultaneously.**
Where it does, the two are split explicitly in the matrix, because **only the BUG aspect is
actionable**. This split is the single most important column in this document.

**Worked example — RM-01.** That a 2-element vector scores `100000` against a 4-element
constitution is a **BUG**: `core/evaluator.py:34,37` documents the inputs as
*"Pre-normalized int32 vectors"* returning *"range approximately [-10^5, 10^5]"*, and a
2-element vector is not that. No specification is needed to see the contradiction.
But *what the system must do about it* — raise, return a sentinel, clamp, or reject
upstream — is **UNDEFINED SEMANTICS** (`REQ-002-031`, unresolved). So detection is
available; response is not.

---

## §3 THE REMEDIATION MATRIX

Severity uses the baseline's scale. **"Safe Engineering Work"** lists only work that
changes no computed value, no format, and no hash.

---

### RM-01 — Vector dimension mismatch is fail-open

| Field | Content |
|---|---|
| **ID** | RM-01 (= CORE-P0-001 · D-3 · P0-1) |
| **Finding** | `zip()` truncates to the shorter sequence. A vector of *any* length whose leading elements align returns the **maximum** similarity `100000`. Both engines. |
| **Severity** | **P0** |
| **Root Cause** | `dot = sum(a * b for a, b in zip(v1, v2))` — `core/evaluator.py:40`, `compliance/consistency.py:93`. No length comparison exists in either engine. `CONSTITUTION_DIM = 1536` is enforced only at `core/offline_normalizer.py:171` and is referenced by **neither** engine. |
| **Category** | **SECURITY** (primary) · ENGINEERING · NORMATIVE (response only) |
| **Nature** | **BUG** (that maximal score is returned for malformed input) **+ UNDEFINED SEMANTICS** (what must happen instead) |
| **Current Evidence** | Reproduced this session at HEAD: 2-of-4 → `100000`; 6-of-4 → `100000`; **1-of-1536 → `100000`**; `evaluate("a",[100000,0],True)` → `{'ari': 100000, 'drift': 0}`. `ConsistencyCalculator` 2-of-4 → `{'score': 100000, 'semantic': 100000, 'penalty': 0}`. **Empty vector → `{'ari': 30000, 'drift': 100000}`, no error.** |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — the required response to a dimension mismatch. Tracked: NB-015 / `REQ-002-031` (`SPEC-002`, DRAFT, no normative effect). Also **RD-2**: does INV-008 (Fail Closed, Critical) treat a dimension mismatch as "an error"? Its normative source APS-001 §8 is **TODO**. |
| **Safe Engineering Work** | Characterization tests **CH-01, CH-02, CH-04** (`03`). Documentation entry `KL-00x`. **Recording** that `RI-PY_AURA_POC_A_CORE.md:55` marks INV-008 ✅ with evidence *"ARI=0 circuit breaker"* while the malformed-input class yields ARI **100000** — as an observation, without editing RI-PY. |
| **Blocker** | Fix is **BLOCKED** twice over: NB-015 (what response) **and** NB-021 (may frozen code be corrected at all). Characterization is **NOT blocked**. |
| **Target Test** | `CH-01` dimension mismatch (both engines, both directions, incl. 1-of-1536 and empty); regression `RT-01` after NB-015 |

---

### RM-02 — Integer division semantics are language-dependent

| Field | Content |
|---|---|
| **ID** | RM-02 (= CORE-P0-002 · D-1) |
| **Finding** | Python `//` floors toward −∞; Rust `/`, C, and `Math.trunc` truncate toward zero. Differ by 1 LSB for negative non-exact dividends. |
| **Severity** | **P0** |
| **Root Cause** | `core/evaluator.py:46` (`dot // SCALING_FACTOR`), `:75-76` (weight rescale), `compliance/consistency.py:58-59`, `:94`. |
| **Category** | **NORMATIVE** (primary) · ARCHITECTURAL · DOCUMENTATION |
| **Nature** | **UNDEFINED SEMANTICS** (primary) **+ BUG** (secondary — the divergence is undocumented in `ADR_005`, `mathematical_foundation.md`, and `KNOWN_LIMITATIONS.md`) |
| **Current Evidence** | Reproduced at HEAD: `(-1)//100000 = -1`, `(-99999)//100000 = -1`, `(-100001)//100000 = -2`. Propagated: `PoCAEvaluator([-100000,0,0,0]).evaluate("a",[1,0,0,0],True)` → `{'ari': 29999, 'drift': 100001}`; a truncating port yields `30000 / 100000`. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — integer-division semantics for negative dividends. Tracked NB-016. **Verified this session: AD-CA-007's candidate list contains no division rule at all** — this is not merely unresolved, it is *unregistered*. |
| **Safe Engineering Work** | Characterization **CH-03**; cross-language register (`04`); documentation of the divergence as AS-IS. |
| **Blocker** | **BLOCKED** on NB-016 / RD-3. Selecting either rule today would make implementation behaviour normative. |
| **Target Test** | `CH-03` negative-dividend boundary table; `XL-01` in `04` |

---

### RM-03 — Rounding semantics are language-dependent

| Field | Content |
|---|---|
| **ID** | RM-03 (= CORE-P0/P1-003 · D-2) |
| **Finding** | Python `round()` is half-to-even; Rust/C round half-away-from-zero; JS rounds half toward +∞. **Three different Constitution Vectors from one input.** |
| **Severity** | **P0/P1** |
| **Root Cause** | `core/offline_normalizer.py:88` — `[round(x * SCALING_FACTOR) for x in normalized_vector]`. This is the **Constitution Vector construction path**. |
| **Category** | **NORMATIVE** (primary) · ARCHITECTURAL · DOCUMENTATION |
| **Nature** | **UNDEFINED SEMANTICS** (primary) **+ BUG** (secondary — the docstring at `:15` states `v_int = round(v_float × 10^5)` without qualifying *which* rounding; a reader implementing from it in another language produces a different vector) |
| **Current Evidence** | Reproduced at HEAD: `round()` over `(0.5,1.5,2.5,3.5)` → `[0,2,2,4]`; negatives → `[0,-2,-2]`. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — rounding rule. AD-CA-007, **UNRESOLVED**; `round-half-to-even` is **candidate only** and `SPEC-002:371` states plainly that no candidate constitutes a recommendation, preference, default, or implied decision. **The implementation exhibiting a candidate's behaviour is not evidence that the candidate was selected.** |
| **Safe Engineering Work** | Characterization **CH-05** — must be labelled candidate-only and must not be phrased as "correct rounding". |
| **Blocker** | **BLOCKED** on AD-CA-007 / RD-3. |
| **Target Test** | `CH-05` `.5` boundaries both signs; `XL-02` in `04` |
| **Note** | `core/test_offline_normalizer.py:97-107` already **locks in** half-to-even against no specification. This is pre-existing and is flagged in `09` as an accidental-authority risk. |

---

### RM-04 — ARI has no normative definition, and exceeds its documented range

| Field | Content |
|---|---|
| **ID** | RM-04 (= CORE-P1-004 · D-4) |
| **Finding** | ARI is documented as `[0, 100000]` and observed at up to `107550000`. No normative source defines the range — or ARI itself. |
| **Severity** | **P1** (range) — but the *definitional* gap beneath it is the package's **critical path** |
| **Root Cause** | `core/evaluator.py:75-79` applies `max(0, …)` — a **lower** clamp only. No upper clamp. `sa` is unbounded above because no normalization check exists (RM-01/RM-06). |
| **Category** | **NORMATIVE** (primary) · ENGINEERING · DOCUMENTATION |
| **Nature** | **UNDEFINED SEMANTICS** (the range) **+ BUG** (`drift` — see RM-05) |
| **Current Evidence** | Reproduced at HEAD: 4×`[100000]` → `{'ari': 310000}` (**3.1×**); 1536×`[100000]` → `{'ari': 107550000}` (**1075×**). `init.sql:47` constrains `RAW_ARI BETWEEN 0 AND 100000` — a constraint no writer ever reaches. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — the ARI contract in full. See `02_ARI_NORMATIVE_GAP.md`, which enumerates **15 dimensions**, of which **15 are undecided**. Tracked RD-1. |
| **Safe Engineering Work** | Characterization **CH-09, CH-12**; documentation that the `[0,100000]` claim has **no normative source**. |
| **Blocker** | **BLOCKED** on RD-1. Adding an upper clamp is **not** safe: clamping changes output. |
| **Target Test** | `CH-09` ARI above documented maximum; `CH-12` accumulator magnitude |

---

### RM-05 — `drift` contradicts its own docstring

| Field | Content |
|---|---|
| **ID** | RM-05 (= D-5 · P1-3) |
| **Finding** | Docstring says clamp to `[0, 100000]`; the code clamps to `200000`. |
| **Severity** | **P1** |
| **Root Cause** | `core/evaluator.py:85` (docstring) vs `:86` (`min(max(0, SCALING_FACTOR - sa), 2 * SCALING_FACTOR)`). |
| **Category** | **ENGINEERING** · DOCUMENTATION |
| **Nature** | **BUG — pure.** The single cleanest finding in the package: two artefacts in the same file disagree. **No specification is required, and none is consulted.** |
| **Current Evidence** | Reproduced at HEAD: anti-aligned → `drift = 200000`; the RM-02 case → `drift = 100001`. `compliance/certificate.py` then divides by `100000`, presenting `2.0` and `1.00001` on a field documented as a `[0.0, 1.0]` ratio. |
| **Required Decision** | **NONE for the documentation direction.** Correcting the *docstring* to state what the code does requires no decision. Correcting the *code* to match the docstring changes output → **ARCHITECTURAL DECISION REQUIRED** (which of the two is authoritative) + NB-021. |
| **Safe Engineering Work** | Characterization **CH-06**; docstring correction (`S-23`, documentation-only, changes no value). |
| **Blocker** | Docstring direction: **NB-021 only** (it touches a frozen file). Code direction: **BLOCKED** on RD-1 + NB-021. |
| **Target Test** | `CH-06` drift upper bound both branches |

---

### RM-06 — Two divergent ARI engines

| Field | Content |
|---|---|
| **ID** | RM-06 (= CORE-P1-005 · D-6 · P0-3) |
| **Finding** | Two implementations of one formula, with different validation, clamping, penalty models and halt semantics. Neither is designated authoritative. |
| **Severity** | **P0** (baseline) / **P1** (readiness) — recorded as **P0**, per `08_BLOCKERS.md` |
| **Root Cause** | Engine A: `core/evaluator.py` + `compliance/evaluator_wrapper.py`. Engine B: `compliance/consistency.py`. Divergences: magnitude validation (none vs lazy `ValueError`), zero-vector guard (none vs `0`), upper clamp (none vs `min(100000, …)`), **penalty model** (`150000` threshold vs `10000 × count`), halt semantics (raise vs status field). |
| **Category** | **ARCHITECTURAL** (primary) · ENGINEERING |
| **Nature** | **BUG** (that one repository yields two answers for one input is a defect **regardless of which is correct**) **+ UNDEFINED SEMANTICS** (which engine, which penalty model) |
| **Current Evidence** | Reproduced at HEAD. In-contract they agree (`[60000,80000,0,0]` → both `100000`). Out-of-contract they diverge: `PoCAEvaluator([200000,0,0,0]).evaluate(...)` → `{'ari': 170000}`; `ConsistencyCalculator(...).calculate(...)` with an out-of-scale **event** vector → `ValueError`. **Correction C-1 applies: the ValueError is raised lazily in `_semantic_alignment` (`:87`), not at construction.** |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — authoritative engine **and** penalty model. Tracked NB-017 / RD-4. Note: `DRIFT_PENALTY = 150000` exceeds the maximum in-range `RAW_ARI` of `100000`, so under Engine A any drift penalty floors ARI to 0 regardless of measurement. |
| **Safe Engineering Work** | Differential characterization **CH-08** — records divergence, picks no winner. Correcting `docs/GAP-001.md` GAP-C5 from *"LARGELY RESOLVED"* to the reproduced state. |
| **Blocker** | **BLOCKED** on RD-4. |
| **Target Test** | `CH-08` differential, in-contract and out-of-contract |

---

### RM-07 — Three JSON canonicalizations

| Field | Content |
|---|---|
| **ID** | RM-07 (= D-7 · P1-4) |
| **Finding** | Three canonicalization forms feed hash inputs. The same object hashed through two paths yields two hashes. |
| **Severity** | **P1** |
| **Root Cause** | `audit/merkle.py:89` compact `separators=(",",":")`; `compliance/certificate.py:69` default separators; `core/merkle.py:8` default separators. No shared canonicalization module. |
| **Category** | **ENGINEERING** · NORMATIVE |
| **Nature** | **BUG** (the *inconsistency* — three forms in one repository) **+ UNDEFINED SEMANTICS** (which form is *canonical*) |
| **Current Evidence** | Reproduced at HEAD: `{"a":[1,2],"b":1}` vs `{"a": [1, 2], "b": 1}` — different bytes, therefore different SHA-256. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — canonical serialization form. AD-CA-008, **UNRESOLVED, "None approved"** (verified at `SPEC-002:382`). |
| **Safe Engineering Work** | Characterization **CH-11** — records that three forms exist and differ. **Unifying them is NOT safe**: it selects a canonical form. |
| **Blocker** | **BLOCKED** on AD-CA-008 / NB-010. |
| **Target Test** | `CH-11` canonicalization variants |

---

### RM-08 — Guard: `violations` outside the integrity boundary

| Field | Content |
|---|---|
| **ID** | RM-08 (= G-1 · P0-6) |
| **Finding** | The chain digest covers nine fields. `violations` is not one of them. Every downstream mechanism — Merkle leaf, Merkle root, segment chain, RFC 3161 imprint — derives from `chain_hash` and therefore inherits the gap. |
| **Severity** | **P0** |
| **Root Cause** | `GUARD src/chain.rs:36-47` — `compute_chain_hash()` takes nine `&str`/`u64` arguments joined by `SEP = "\|"`. It does not accept an `AuditEntry` and **has no access to the field**. Verified at source this session. |
| **Category** | **SECURITY** (primary) · ARCHITECTURAL |
| **Nature** | **BUG** — but of a specific kind: the *implementation* is self-consistent; what it contradicts is **its own shipped documentation**. `README.md:24`, `:97`, `:265` and `docs/REPLAY_DEMO.md:50` all claim **"any"** byte-level mutation is detected. That claim is false for this field. |
| **Current Evidence** | Characterization already executed and committed: `GUARD-G1_CHARACTERIZATION_TESTS.rs` (386 lines). Mutations of `violations` — emptied, rewritten, fabricated — all leave `recompute_for_entry == chain_hash` **TRUE**. Control (`decision` `DENY`→`ALLOW`) breaks the chain, confirming the reproduction is faithful. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — D1…D8 in `06`. **Critically: this is a *product* decision about the audit-log format, NOT a Constitution decision.** Guard contains zero occurrences of `constitution`, `ari`, `poca`, or `frozen`. **RM-08 is not gated by DR-002, SPEC-002, any AD-CA, or NB-021.** |
| **Safe Engineering Work** | Characterization **T-0a/T-0b/T-0c** (`06` §7). Documentation correction of the four overbroad "any" claims — a documentation change requiring **no** integrity decision. |
| **Blocker** | **NOT governance-blocked.** Blocked only on the product decision D1–D2. This is the **largest genuinely unblocked decision surface in the ecosystem**. |
| **Target Test** | `06` §7 T-0a…T-0c now; T-1…T-11 after D1–D7 |

---

### RM-09 — Guard: `f32` in the evidence record

| Field | Content |
|---|---|
| **ID** | RM-09 (= P1-14) |
| **Finding** | `Violation.confidence: f32` is serialized into the persisted record. Currently inert; becomes a cross-language determinism surface the instant RM-08 is addressed. |
| **Severity** | **P1** |
| **Root Cause** | `GUARD src/models.rs:38`. Value originates in policy YAML (`src/policy.rs`) parsed by `serde_yaml`. |
| **Category** | **ARCHITECTURAL** · SECURITY |
| **Nature** | **UNDEFINED SEMANTICS** — no rule exists for how a float is reduced to hashable bytes. |
| **Current Evidence** | `06`/design brief §9: only floating-point value in the record; `0.7` is not exactly representable in binary32; nothing prevents `NaN`/infinity, which JSON cannot represent. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — D4: does `confidence` participate in the digest, and in what representation (stored text / fixed-precision decimal / IEEE-754 bits / scaled integer)? |
| **Safe Engineering Work** | Documentation only. |
| **Blocker** | **Coupled to RM-08.** Must be planned jointly, not sequentially — deciding RM-08 without D4 would create a determinism surface where none exists today. |
| **Target Test** | `06` T-5 `f32` boundary values |

---

### RM-10 — CI does not execute the ARI evaluation path

| Field | Content |
|---|---|
| **ID** | RM-10 (= CORE-P1-006 · P1-1) |
| **Finding** | The cross-platform determinism job computes **no ARI**. The subsystem where RM-01…RM-06 live is precisely the subsystem CI does not observe. |
| **Severity** | **P1** — but **highest leverage in the package** |
| **Root Cause** | `scripts/generate_determinism_report.py:36-38` imports exactly three modules; `core.evaluator` is **not** among them. Its `ari_vector_hash` hashes the **constitution vector**, not an ARI — the name is misleading. |
| **Category** | **TESTING** · **GOVERNANCE** |
| **Nature** | **GOVERNANCE BLOCKER.** The engineering is trivial (a two-line change, already drafted and deliberately not applied in `RD-006` §7). What blocks it is a **permission question**: NB-021 classifies CI infrastructure as falling under *no* permitted-change category — neither `core/` logic, nor documentation, nor tests. |
| **Current Evidence** | Three independent confirmations in `05_CORE_REMEDIATION_READINESS.md` §5.6. The `RD-006` harness (`core/test_ari_observability.py`, 8 tests, executed, passing) **exists and is inert** — no CI step would invoke it. |
| **Required Decision** | **GOVERNANCE DECISION REQUIRED** — RD-6: does CI infrastructure fall inside the FROZEN boundary? **This is narrower than NB-021 and answerable independently of it.** |
| **Safe Engineering Work** | Characterization **CH-13**: assert the determinism report's import set, pinning that `core.evaluator` is absent. |
| **Blocker** | **BLOCKED** on RD-6 alone. |
| **Target Test** | `CH-13`; then `05` §5 wiring |

---

### RM-11 — Conformance Kit contains no substantive tests

| Field | Content |
|---|---|
| **ID** | RM-11 (= `07_CONFORMANCE_AUDIT.md`) |
| **Finding** | Total executable test content across both kit repositories: one `assert True`. |
| **Severity** | **P1** |
| **Root Cause** | Downstream consequence of every unresolved normative decision. |
| **Category** | **NORMATIVE** · TESTING |
| **Nature** | **NOT A BUG.** Explicitly recorded as **correct behaviour**: writing SPEC-002 conformance tests today would necessarily encode one of the unapproved candidate answers, which `SPEC-002:371` expressly forbids. |
| **Current Evidence** | `07_CONFORMANCE_AUDIT.md` §1–§4. All ten CONF-001…010 are **DRAFT**; `APS-400` is `1.0-DRAFT`; FIX-001 and FIX-ERROR are **TODO**. |
| **Required Decision** | Downstream of RD-1, RD-2, RD-3. Also **NB-002**: which kit repository is authoritative — the active fork or the archived byte-identical twin. |
| **Safe Engineering Work** | Structure only, no fixtures: `09_CONFORMANCE_BOOTSTRAP_PLAN.md`. |
| **Blocker** | **BLOCKED**, and correctly so. |
| **Target Test** | None may be written yet. **This is the correct state.** |

---

### RM-12 — No independent implementation evidence exists

| Field | Content |
|---|---|
| **ID** | RM-12 |
| **Finding** | Both reference implementations are **NOT CERTIFIED**; neither has a conformance runner. No second implementation of the ARI arithmetic exists in any language. |
| **Severity** | **P1** |
| **Root Cause** | `03_LANGUAGE_BOUNDARY.md` §1: **no Python/Rust runtime interface exists** — no FFI, IPC, HTTP, shared format, shared schema, shared test vector, or shared constant. |
| **Category** | **ARCHITECTURAL** · TESTING |
| **Nature** | **GOVERNANCE BLOCKER** + **UNDEFINED SEMANTICS.** An independent implementation cannot be built from a specification that does not define the arithmetic. |
| **Current Evidence** | Verified at SPEC: `RI-PY` and `RI-RS` both **NOT CERTIFIED**; RI-004 (conformance runner) **MISSING** for both. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — RD-1 + RD-3 in full, then the SPEC-002 §10 Independent Implementer Test. |
| **Safe Engineering Work** | Define the protocol, contamination controls and fixture contracts **without building it**: `08`. |
| **Blocker** | **BLOCKED.** Note the ordering trap: this is why RM-02/RM-03 are `LATENT` rather than `ACTIVE` — and building an independent implementation is what makes them `ACTIVE`. |
| **Target Test** | `08` replay protocol; byte-level comparison |

---

### RM-13 — The Constitution Artifact is not implemented

| Field | Content |
|---|---|
| **ID** | RM-13 |
| **Finding** | No Constitution Artifact exists in the runtime. No production runtime interface for Constitution or ARI exists in Python or Rust. |
| **Severity** | **P1** |
| **Root Cause** | CR-007 is **explicitly BLOCKED** per `SPEC-002 §11.B`. Generating a Constitution Vector requires AD-CA-005 (embedding), AD-CA-006 (dictionary), AD-CA-007 (numeric representation) — all UNRESOLVED. |
| **Category** | **NORMATIVE** · GOVERNANCE |
| **Nature** | **GOVERNANCE BLOCKER.** Not a defect — the correct state given the decisions outstanding. |
| **Current Evidence** | Verified at SPEC: `SPEC-002:11` — *"Normative effect: NONE until APPROVED"*; §17 — MUST NOT be used to implement, generate, register or freeze a Constitution Artifact until blocking decisions are approved. |
| **Required Decision** | **ARCHITECTURAL DECISION REQUIRED** — AD-CA-001…012, i.e. the whole DR-002 domain. |
| **Safe Engineering Work** | **NONE.** Any work here would generate an artefact the specification forbids generating. |
| **Blocker** | **ABSOLUTELY BLOCKED.** |
| **Target Test** | None permitted. |

---

### RM-14 — No evidence is persisted; the evidence chain is unconnected (Core)

| Field | Content |
|---|---|
| **ID** | RM-14 (= P0-4 · P0-5) |
| **Finding** | No production module connects an evaluation result to `audit/merkle.py`; none writes to `audit_events`. `core/merkle.py:11` `generate_etc()` returns `{"proof": [leaf]}` — the leaf itself, with no root to verify against — and that is the path `demo.py` and two test modules use. |
| **Severity** | **P0** |
| **Root Cause** | `02_RUNTIME_DATAFLOW.md` §7. Grep for `psycopg\|asyncpg\|sqlalchemy` in non-test `*.py` → **0 hits**. |
| **Category** | **ENGINEERING** · SECURITY |
| **Nature** | **BUG — pure.** Independent of every normative question. An artefact named "Event Trust Certificate" carrying no verifiable proof is an integrity misrepresentation if it reaches a consumer. |
| **Current Evidence** | `08_BLOCKERS.md` P0-4, P0-5. The only evaluation → Merkle → certificate composition exists inside `test_compliance.py`, which CI does not run and `unittest discover` cannot collect. |
| **Required Decision** | **NONE to observe.** Building the missing path is new production code → NB-021. |
| **Safe Engineering Work** | Documentation of the disconnection. Making `test_compliance.py` collectible (harness change, alters no assertion). |
| **Blocker** | NB-021 for any code path. **Not** blocked on DR-002 or SPEC-002. |
| **Target Test** | Out of scope for this phase; recorded in `10`. |

---

### RM-15 — Repository authority is ambiguous

| Field | Content |
|---|---|
| **ID** | RM-15 (= NB-000 · NB-001 · NB-002) |
| **Finding** | Three unresolved authority questions: what `DR-002` refers to; which `aura-specification` is authoritative; which Conformance Kit is authoritative. |
| **Severity** | **P0 for governance** (no engineering severity) |
| **Root Cause** | **NB-000:** `DR-002` appears in **no** repository — re-verified across the full specification corpus this session, zero hits. **NB-001:** two `aura-specification` repositories exist — `AuraIDToken/` (full APS corpus, 40+ documents) and `aura-nomos/` (one-line README). **This session was scoped to the latter.** **NB-002:** `Aura-Conformance-Kit` (active) vs `Aura-Conformance-Kits` (archived, byte-identical source). |
| **Category** | **GOVERNANCE** |
| **Nature** | **GOVERNANCE BLOCKER** — and the *upstream-most* one. Every citation in every document in this package inherits NB-001. |
| **Current Evidence** | Verified this session. |
| **Required Decision** | **GOVERNANCE DECISION REQUIRED.** Not resolvable by engineering under any circumstances. |
| **Safe Engineering Work** | Recording the ambiguity. **Nothing else.** |
| **Blocker** | Blocks the *citability* of everything downstream. |
| **Target Test** | None. |

---

## §4 Roll-Up by Nature

| Nature | IDs | Count | Engineering may act alone? |
|---|---|:--:|---|
| **BUG** (pure — no normative input needed) | RM-05, RM-14 | **2** | **YES** — subject only to NB-021 |
| **BUG + UNDEFINED SEMANTICS** (split; only the BUG aspect actionable) | RM-01, RM-02, RM-03, RM-04, RM-06, RM-07, RM-08 | **7** | **PARTIALLY** — detection/recording only |
| **UNDEFINED SEMANTICS** (pure) | RM-09 | **1** | **NO** |
| **GOVERNANCE BLOCKER** | RM-10, RM-12, RM-13, RM-15 | **4** | **NO** |
| **NOT A DEFECT** (correct state) | RM-11 | **1** | n/a |

## §5 Roll-Up by Category

| Category | Primary | Secondary |
|---|---|---|
| SECURITY | RM-01, RM-08 | RM-09, RM-14 |
| NORMATIVE | RM-02, RM-03, RM-04, RM-11, RM-13 | RM-01, RM-07 |
| ARCHITECTURAL | RM-06, RM-09, RM-12 | RM-02, RM-03, RM-08 |
| ENGINEERING | RM-05, RM-07, RM-14 | RM-01, RM-04, RM-06 |
| GOVERNANCE | RM-10, RM-15 | RM-12, RM-13 |
| TESTING | RM-10 | RM-11, RM-12 |
| DOCUMENTATION | — | RM-02, RM-03, RM-04, RM-05, RM-08 |

## §6 Decision Dependency Summary

Full map in `07_GOVERNANCE_DEPENDENCY_MAP.md`.

| Decision | Findings unblocked | Cost to decide |
|---|---|---|
| **RD-6** — CI inside the FROZEN boundary? | RM-10 → observability for **all** of RM-01…RM-07 | **Lowest.** A scoping ruling, not a semantic choice |
| **D1/D2** — Guard integrity posture | RM-08, RM-09 | Product decision; **no governance dependency** |
| **RD-5 / NB-021** — may frozen code be corrected? | RM-05, RM-14, and the fix half of RM-01…RM-07 | Governance ruling |
| **RD-1** — normative ARI definition | RM-04, RM-06, RM-12 | Specification work |
| **RD-3** — AD-CA-007 incl. division | RM-02, RM-03, RM-07, RM-12 | Specification work |
| **RD-2** — APS-001 §8 / INV-008 trigger | RM-01 | Specification work |
| **NB-000/001/002** — repository authority | RM-15, and the citability of everything | Governance ruling |

---

## §7 STOP CONDITIONS TRIGGERED

Per §15 of the task instruction. **These are reported, not worked around.** No document in
this package resolves any of them.

| # | Condition | Triggered | Where |
|---|---|:--:|---|
| 1 | A task requires choosing an unspecified semantic | **YES** | Every "Required Decision" cell. **Handled as instructed** — written as ARCHITECTURAL DECISION REQUIRED, never filled with a reasonable engineering choice. |
| 2 | A production fix requires interpreting FROZEN authority | **YES** | RM-01…RM-07, RM-14. **No fix was made.** |
| 3 | An ADR is needed | **YES** | RD-1, RD-3, D1–D8. **No ADR was created.** |
| 4 | A specification amendment is needed | **YES** | RM-01 (APS-001 §8 TODO), RM-04 (no ARI definition). **SPEC-002 untouched.** |
| 5 | A fixture would encode an unapproved expected value | **YES** | RM-11. **No fixture was created.** |
| 6 | **Two authoritative documents conflict** | **YES** | See §7.1 — three live conflicts |
| 7 | **Repository authority is ambiguous** | **YES** | RM-15 (NB-000/001/002) |
| 8 | A change would make implementation behaviour normative | **YES** | RM-02, RM-03, RM-07. **Avoided** — characterization only, explicitly labelled. |
| 9 | Required evidence does not exist | **PARTIALLY** | SPEC-002 **v0.4 does not exist**; `DR-002` exists in no repository. Both re-verified. All *other* evidence was located and read at primary source. |

### 7.1 Document conflicts requiring Protocol Custodian resolution

`CLAUDE.md` requires that a detected conflict be reported and escalated, **not silently
reconciled**. Three are live:

| # | Conflict | Sides |
|---|---|---|
| **CF-1** | **Which governs when implementation and specification disagree** | `docs/specs/AUDIT_LAYER_SPEC.md` says *"implementation governs"*; Constitution Art. IV P1 and `CONTRIBUTING.md` say the opposite. **Directly determines whether RM-01…RM-07 are defects or specification gaps.** |
| **CF-2** | **The Decree contradicts the shipped code** | `CONSTITUTIONAL_DECREE.md` Art. IX states `assert target_type == "MACHINE_ACCOUNT"` is **MANDATORY in every evaluation path**. Commit `4ced103` removed it. The Decree has not been amended. |
| **CF-3** | **The freeze framework invalidates itself** | `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §4.1 Gate 1 permits correcting a mathematical error; Gate 2 rejects any change not preserving bit-identity — *"UNCERTAIN → REJECTED"*. Every error correction changes output. **Gate 2 rejects exactly what Gate 1 permits.** |

**None is reconciled here.** Each requires human/Protocol Custodian resolution.

---

*This document has no normative effect. It makes no decision, creates no ADR, changes no
specification, and modifies no code, CI, or fixture. It records readiness only.*
