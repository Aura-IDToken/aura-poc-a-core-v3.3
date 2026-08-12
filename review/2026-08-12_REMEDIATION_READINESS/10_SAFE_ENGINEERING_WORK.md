# 10 — SAFE ENGINEERING WORK REGISTER

**Date:** 2026-08-12
**Mode:** REGISTER ONLY. **No work in this document was executed.**
**Normative effect:** NONE.

---

## §1 The Safety Test

Applied to every candidate. **Any single YES disqualifies it from EXECUTABLE NOW.**

| # | Question | If YES |
|---|---|---|
| 1 | Does it change a value the system computes? | not safe |
| 2 | Does it require choosing a protocol semantic? | not safe |
| 3 | Does it encode an unresolved candidate answer in a fixture? | not safe |
| 4 | Does it change a hash, byte sequence, or serialized format? | not safe |
| 5 | Does it modify code inside the frozen boundary? | needs RD-5 even if otherwise harmless |
| 6 | Does it change what an existing CHECK asserts? | not safe — `AGENTS.md` rule 10 |

**Every item was tested against the current architecture, not assumed safe by category.**
Several items that belong to normally-safe categories fail here for repository-specific
reasons; they are in §3 and §5.

---

## §2 EXECUTABLE NOW

Changes no normative semantics, no computed value, no format, no hash. Modifies no
production code.

### §2.1 Characterization tests — highest value

| ID | Work | Why safe | Dependency | Artifact | Test | Merge blocker |
|---|---|---|---|---|---|---|
| **EN-01** | CH-01, CH-02 — dimension mismatch, both engines | Records; asserts no correctness | none | `core/test_characterization_evaluator.py` | is the test | **none** |
| **EN-02** | CH-03 — negative division boundaries | Records; the cross-language column is computed, never adopted | none | as above | is the test | **none** |
| **EN-03** | CH-04 — malformed schema | Records | none | as above | is the test | **none** |
| **EN-04** | CH-05 — rounding boundaries, both signs | Records; **must be labelled candidate-only** | none | `core/test_characterization_normalizer.py` | is the test | **none** |
| **EN-05** | CH-06 — anti-aligned / drift bound | Records the docstring contradiction | none | evaluator module | is the test | **none** |
| **EN-06** | CH-07 — orthogonal vectors | Records | none | as above | is the test | **none** |
| **EN-07** | CH-08 — zero vectors + engine divergence | Records divergence; **designates no winner** | none | `compliance/test_characterization_engines.py` | is the test | **none** |
| **EN-08** | CH-09 — ARI above documented maximum | Records | none | evaluator module | is the test | **none** |
| **EN-09** | CH-10 — high-dimensional (1536) | Records | none | as above | is the test | **none** |
| **EN-10** | CH-11 — three JSON canonicalizations | Records; **unifies nothing** | none | `audit/test_characterization_canonicalization.py` | is the test | **none** |
| **EN-11** | CH-12 — accumulator magnitude vs i32/i64 | Records; **cannot** observe overflow in CPython | none | evaluator module | is the test | **none** |
| **EN-12** | CH-13 — deterministic replay + import-set pin | Records | none | `core/test_characterization_replay.py` | is the test | **none** |
| **EN-13** | CH-14 — float leakage into the int engine | Records a finding new to this session | none | evaluator module | is the test | **none** |
| **EN-14** | Control tests CT-1…CT-4 for every module above | Proves the harness executes rather than replays | none | each module | is the test | **none** |

**Mandatory framing for EN-01…EN-14.** Each must carry, verbatim:
> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

**Basis:** `CONSTITUTIONAL_DECREE.md` Art. VII (Testing), Art. III items 4–5; NB-021 **CASE
D** (test-only changes **PERMITTED**). Precedent executed twice already
(`GUARD-G1_CHARACTERIZATION_TESTS.rs`, `core/test_ari_observability.py`).

**Placement constraint:** the `test_` filename prefix is load-bearing — CHECK 2, 3, 5 and 9
all skip files by that convention (`scripts/check_cr003_layer_boundary.py:165-166`).

### §2.2 Observability

| ID | Work | Dependency | Artifact | Merge blocker |
|---|---|---|---|---|
| **EN-15** | OB-A6 — ARI as a function of truncation depth (sweep 1…1536) | none | observation record | **none** |
| **EN-16** | OB-E1…E4 — division boundary table | none | as above | **none** |
| **EN-17** | OB-F4 — dimension at which the accumulator crosses `i32::MAX` (≈215) | none | as above | **none** |
| **EN-18** | OB-G6 — separate dimension-driven from magnitude-driven range excess | none | as above | **none** |
| **EN-19** | OB-D4 — end-to-end normalizer → evaluator rounding effect | none | as above | **none** |
| **EN-20** | OB-I5 — side-by-side penalty model comparison | none | as above | **none** |

Each emitted record must carry `"normative_effect": "NONE"`, **enforced by a test** so the
marker cannot be silently dropped.

### §2.3 Aura-Guard — the largest unblocked block

**Guard is not gated by DR-002, SPEC-002, any AD-CA, NB-021, or CR-007.** Verified: zero
occurrences of `constitution`, `ari`, `poca`, `frozen`, `freeze`.

| ID | Work | Dependency | Artifact | Test | Merge blocker |
|---|---|---|---|---|---|
| **EN-21** | T-0a — mutate `violations`, run `verify_chain()` | none | Rust test | is the test | **none** |
| **EN-22** | T-0b — same, then manifest verification | none | as above | is the test | **none** |
| **EN-23** | **T-0c — pin the nine-field preimage as a known-answer vector** | none | as above | is the test | **none** |
| **EN-24** | Correct the four overbroad "any" claims (README ×3, REPLAY_DEMO ×1) | none | documentation | n/a | **none** |
| **EN-25** | Correct the stale formula comment at `src/models.rs:95` (omits `policy_hash`, `context`) | none | documentation | n/a | **none** |
| **EN-26** | Add arm64 to Guard CI (`ci.yml` is `ubuntu-latest` only) | none | workflow | existing suite | **none** |
| **EN-27** | Correct the stale test count in Guard `docs/ROADMAP.md` | none | documentation | n/a | **none** |

**EN-23 is the highest-value single item in this section** — it converts the current digest
definition from an implicit code property into an executable, reviewable fact, so any future
change to it becomes visible.

### §2.4 Documentation of existing behaviour

| ID | Work | Dependency | Artifact | Merge blocker |
|---|---|---|---|---|
| **EN-28** | `KL-00x` entries in `docs/KNOWN_LIMITATIONS.md` for RM-01…RM-07, each stating the correct behaviour is **unresolved** | none | doc | **none** |
| **EN-29** | Correct `docs/GAP-001.md` GAP-C5 from *"LARGELY RESOLVED"* to the reproduced state | none | doc | **none** |
| **EN-30** | Document the four coexisting rounding/reduction rules as an AS-IS table | none | doc | **none** |
| **EN-31** | Record that `ari_vector_hash` hashes the constitution vector, **not** an ARI | none | doc | **none** |
| **EN-32** | Record that CHECK 1/2/4 are lexical or existence checks, not behavioural ones | none | doc | **none** |
| **EN-33** | Record that `packages/**` is unbuildable | none | doc | **none** |
| **EN-34** | Record that RI-PY's INV-008 ✅ is unsupported for the malformed-input class — **observation only; RI-PY not edited** | none | doc | **none** |
| **EN-35** | Record the three document conflicts CF-1/CF-2/CF-3 for Custodian attention | none | doc | **none** |

**Caution carried from the baseline:** documenting behaviour must not slide into documenting
it as *required* behaviour. Every entry must state that the correct behaviour is unresolved.

### §2.5 This review package

| ID | Work | Merge blocker |
|---|---|---|
| **EN-36** | `review/2026-08-12_REMEDIATION_READINESS/` — this package | **none** |

---

## §3 EXECUTABLE AFTER NB-021 *(specifically after RD-6, the CI-scope sub-ruling)*

Requires confirmation that **CI, tests and infrastructure fall outside the frozen
boundary.** RD-6 is narrower than RD-5 and answerable independently.

| ID | Work | Why blocked | Dependency | Artifact | Test | Merge blocker |
|---|---|---|---|---|---|---|
| **NB-A1** | Wire `core.test_ari_observability` into `run_all_checks.sh` (**1 line, drafted, unapplied**) | CI is not covered by any Decree Art. III permitted-change category | **RD-6** | check block | existing 8 tests | RD-6 ruling |
| **NB-A2** | Add the observation artifact to the CI upload list (**1 line**) | as above | RD-6 | workflow | n/a | RD-6 |
| **NB-A3** | Wire EN-01…EN-14 into CI | as above | RD-6 | check block | those tests | RD-6 |
| **NB-A4** | Extend the determinism report to compute ARI — **labelled `CHARACTERIZATION_ONLY`** | as above | RD-6 | report schema | cross-platform compare | RD-6 |
| **NB-A5** | Add a CI step running the full unit suite (**105 locally-passing tests currently gate nothing**) | as above | RD-6 | workflow | existing | RD-6 |
| **NB-A6** | Make `test_compliance.py` collectible (harness change; **alters no assertion**) | as above | RD-6 | test harness | 4 existing tests | RD-6 |
| **NB-A7** | Add `ruff` / `ruff format --check` (the Kit already gates on these; core has nothing) | as above | RD-6 | workflow | lint | RD-6 |
| **NB-A8** | Add `mypy` (non-strict first) | as above | RD-6 | workflow | types | RD-6 |
| **NB-A9** | Add coverage reporting (no gate initially) | as above | RD-6 | workflow | n/a | RD-6 |
| **NB-A10** | Add `pip-audit`, SBOM, CodeQL (Guard and the Kit both have these) | as above | RD-6 | workflow | n/a | RD-6 |
| **NB-A11** | Remove or create the non-existent `develop` branch trigger | as above | RD-6 | workflow | n/a | RD-6 |
| **NB-A12** | Add a `demo.py` smoke step (**would have caught the crash**) | as above | RD-6 | workflow | smoke | RD-6 + the demo fix (§4) |

**NB-A4 carries a mandatory caveat.** The determinism report's vectors are compared across
platforms and then **treated as a determinism claim**. Adding an evaluator vector implicitly
asserts *"this output is the reference output"* — very close to treating current behaviour
as normative.
**Safe formulation:** add the vectors with `"status": "CHARACTERIZATION_ONLY"` and an
explicit non-normativity note.
**Unsafe formulation:** adding them silently alongside vectors that *are* backed by
`docs/specs/AUDIT_LAYER_SPEC.md`.

**NB-A5's significance:** `audit/test_audit.py` (47 tests), `core/test_ari.py`,
`core/test_offline_normalizer.py`, `core/test_integration.py` and `test_compliance.py` are
**never invoked by CI**. 105 passing tests gate nothing today.

---

## §4 EXECUTABLE AFTER ARCHITECTURAL DECISION

Requires a normative choice. **None may be executed before the cited decision exists.**

| ID | Work | Decision required | Findings | Test | Merge blocker |
|---|---|---|---|---|---|
| **AD-01** | Detect and respond to dimension mismatch | **RD-2** (INV-008 trigger) + **NB-015** (required response) + **AG-02** (which dimension) | RM-01 | RT-A1…RT-A8 | decision + RD-5 + custodian signature |
| **AD-02** | Fix or ratify the division semantics at 4 sites | **RD-3** — **unregistered in any candidate list** | RM-02 | XL-01 regression | decision + RD-5 |
| **AD-03** | Fix or ratify the rounding at `offline_normalizer.py:88` | **RD-3** — candidate only | RM-03 | XL-02 regression | decision + RD-5 |
| **AD-04** | Define and enforce the ARI range | **RD-1** (AG-12) | RM-04 | CH-09 → regression | decision + RD-5 |
| **AD-05** | Correct the `drift` **code** to match the docstring | **RD-1** (AG-11 — which of the two is authoritative) | RM-05 | CH-06 → regression | decision + RD-5 |
| **AD-06** | Unify or designate between the two engines | **RD-4** | RM-06 | CH-08 → regression | decision + RD-5 |
| **AD-07** | Select the penalty model | **RD-4** | RM-06 | new | decision + RD-5 |
| **AD-08** | Unify the three JSON canonicalizations | **RD-7** — "None approved" | RM-07 | CH-11 → regression | decision + RD-5 |
| **AD-09** | Define the canonical byte encoding (production, not test-only) | **RD-7** | RM-07, RM-12 | new | decision + RD-5 |
| **AD-10** | Select the Merkle construction (Python duplication vs RFC 6962) | **NB-018** | XL-08 | cross-impl. | decision + RD-5 |
| **AD-11** | Bind `violations` into the Guard digest | **D1–D7** — *product decision, no governance gate* | RM-08, RM-09 | TG-1…TG-7, T-1…T-11 | **product sign-off only** |
| **AD-12** | Define the `f32` representation for hashing | **D4** | RM-09 | T-5 | product sign-off |
| **AD-13** | Connect evaluation → Merkle → persistence | **RD-5** only — no semantic choice | RM-14 | new | RD-5 + custodian signature |
| **AD-14** | Replace `core/merkle.py`'s placeholder proof | **NB-018** + RD-5 | RM-14 | new | decision + RD-5 |

**AD-05 deserves note.** The *docstring* direction (making documentation match the code) is
in §2.4 territory — documentation-only, changing no value. Only the *code* direction
appears here. **The two are not symmetric, and conflating them is a common error.**

**AD-11 and AD-12 are the only rows in this section whose gate is not the Protocol
Custodian.**

---

## §5 BLOCKED — must not be performed

| ID | Work | Blocked by | Stop condition |
|---|---|---|---|
| **BL-01** | Generate a Constitution Vector | AD-CA-005/006/007 | 1, 4 |
| **BL-02** | Create `constitution.json` | as above | 1, 4 |
| **BL-03** | Implement CR-007 | **explicitly BLOCKED** — `SPEC-002 §11.B` | 4 |
| **BL-04** | Select or implement an embedding method | AD-CA-005 | 1 |
| **BL-05** | Replace `core/embedding.py` with a real embedder | AD-CA-005 | 1 |
| **BL-06** | Define hash domains | AD-CA-008 — "None approved" | 1 |
| **BL-07** | Write any SPEC-002 conformance test | `SPEC-002 §11` NOT READY | 5 |
| **BL-08** | Create any fixture with an expected ARI or vector value | RD-1, AD-CA-007 | 5 |
| **BL-09** | Build a second ARI implementation | RD-1 + RD-3 (`08`: 9/9 prerequisites unmet) | 1, 9 |
| **BL-10** | Create a Python/Rust runtime interface | NB-020 + RD-3 | 1 |
| **BL-11** | Decide whether halt state must be durable/distributed | NB-019 | 1 |
| **BL-12** | Declare any finding remediated, conformant, or verified | evidence does not exist; INV rows are NOT VERIFIED | 9 |
| **BL-13** | Resolve DR-002, NB-021, or NB-000/001/002 | governance authority | 6, 7 |
| **BL-14** | Reconcile conflicts CF-1, CF-2, CF-3 | **Custodian only** — `CLAUDE.md` forbids silent reconciliation | 6 |
| **BL-15** | Amend SPEC-002, the Decree, or any invariant | governance authority | 4 |
| **BL-16** | Create an ADR | governance authority | 3 |

---

## §6 Category Verdicts — where the obvious answer is wrong

Recorded because these categories are *normally* safe and are **not** safe here.

| Category | Verdict | Repository-specific reason |
|---|---|---|
| **Malformed-input handling** | **PARTIALLY UNSAFE** | Detection is safe; the required *response* is NB-015. Implementing a `raise` today encodes an unresolved failure-mode decision into the reference implementation. |
| **Bounds checking** | **PARTIALLY UNSAFE** | Same split — and the missing upper clamp cannot be "fixed" by adding one, because clamping changes output values. |
| **Error handling** | **PARTIALLY UNSAFE** | Changing `PolicyRule.is_violated`'s catch-all alters fail-closed behaviour — a policy semantic. |
| **Refactoring** | **CONDITIONALLY SAFE** | Any `core/` refactor must re-pass CHECK 2 (**lexical** float grep — a variable named `float_scale` trips it), CHECK 3, CHECK 5, CHECK 9 (AST boundary). **Renaming a symbol can fail a check for purely lexical reasons.** |
| **Static typing** | **CONDITIONALLY SAFE** | **Do not annotate `core/` with `float` in any position** — CHECK 2 is a plain grep and would fail, even though `verify_constitutional_purity.py` handles annotations correctly. |
| **CI improvements** | **SAFE except one case** | Adding a job is safe. **Changing what an existing CHECK asserts is not** — `AGENTS.md` rule 10 forbids weakening tests to make an implementation pass. |
| **Observability** | **CONDITIONALLY SAFE** | Safe in `compliance/`, `audit/`, Guard. **Not in `core/`** without verifying CHECK 5 and CHECK 9 — logging imports sit near the forbidden-import line. |
| **Performance work** | **MEASUREMENT SAFE; OPTIMIZATION NOT** | Benchmarks are safe. Any optimization changing dot-product evaluation order is **not** — it affects nothing for integers today but would if the numeric model changes. |
| **Documentation** | **SAFE — the safest category** | One caution: documenting behaviour must not slide into documenting it as *required*. |

---

## §7 Summary

| Class | Items | Gate |
|---|:--:|---|
| **EXECUTABLE NOW** | **36** | none |
| **AFTER NB-021 / RD-6** | 12 | one scoping ruling |
| **AFTER ARCHITECTURAL DECISION** | 14 | 2 of which need only product sign-off |
| **BLOCKED** | 16 | governance authority |

**36 items are available today without any decision.** They are the items that convert open
questions into recorded facts — which is what every blocked decision needs as input.

**Recommended order** (value per unit of risk, not by severity label):

1. **§2.3 Guard work (EN-21…EN-27)** — entirely unblocked, and includes the ecosystem's most
   serious integrity finding outside RM-01
2. **§2.1 characterization tests (EN-01…EN-14)** — zero risk; directly feeds every blocked
   decision
3. **§2.4 documentation (EN-28…EN-35)** — corrects claims that currently mislead
4. **§2.2 observability (EN-15…EN-20)** — makes the decisions measurable
5. **§3 after RD-6** — makes 105 existing tests actually gate something

---

*This document has no normative effect. It classifies work by permission and executes none
of it.*
