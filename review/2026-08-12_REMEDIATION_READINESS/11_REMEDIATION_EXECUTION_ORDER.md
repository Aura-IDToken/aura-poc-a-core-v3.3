# 11 — REMEDIATION EXECUTION ORDER

**Date:** 2026-08-12
**Mode:** PLAN ONLY. **No phase was executed.**
**Normative effect:** NONE.

---

## §1 Ordering Principle

Phases are ordered by **dependency**, not by severity.

A P0 finding whose fix requires an undecided semantic cannot precede the decision that
defines it. Ordering by severity would place RM-01 first and stall the entire programme,
because RM-01's fix depends on three unresolved decisions.

**Two tracks run in parallel** and are marked throughout:

| Track | Gate | Phases |
|---|---|---|
| **CORE** | Protocol Custodian / Architect | 0 → 10 sequentially |
| **GUARD** | **Product owner — no governance dependency** | may start immediately |

---

## §2 Phase Overview

| Phase | Name | Gate | Available today? |
|---|---|---|---|
| **0** | Governance clarification | Custodian | **YES — start here** |
| **1** | Characterization | none | **YES — parallel with 0** |
| **2** | Normative ARI contract | Custodian + Architect | after 0 |
| **3** | Deterministic arithmetic contract | Architect | after 2 |
| **4** | Integrity contract | Architect · **Guard: product owner** | **Guard half: YES** |
| **5** | Reference implementation correction | Custodian | after 2, 3, 4 |
| **6** | Independent implementation | Architect | after 5 |
| **7** | Conformance Kit | Architect | after 6 |
| **8** | Python/Rust runtime integration | Architect | after 7 |
| **9** | Cross-platform replay | Architect | after 8 |
| **10** | Release gate | Custodian | after 9 |

---

# PHASE 0 — GOVERNANCE CLARIFICATION

**Prerequisites:** none. **This phase is available today and blocks almost everything else.**

### Allowed work
- Answer **NB-001** — which `aura-specification` is authoritative
- Answer **NB-000** — what `DR-002` refers to and how it maps onto `AD-CA-001…012`
- Answer **NB-002** — which Conformance Kit is authoritative
- Answer **RD-6** — does CI infrastructure fall inside the FROZEN boundary?
- Answer **RD-5 / NB-021** — does FROZEN permit non-normative defect correction?
- Resolve conflicts **CF-1**, **CF-2**, **CF-3** (`00` §7.1)
- Determine v3.3's normative identity (no tag, no SHA, `[COMPUTED_AT_SEALING_v3.3]` unfilled)

### Forbidden work
- Any code change to `core/` or `compliance/`
- Any CI change (that is what RD-6 decides)
- Any specification amendment before NB-001 is answered — the target repository is ambiguous
- Reconciling CF-1/CF-2/CF-3 by engineering judgement (`CLAUDE.md` forbids silent reconciliation)

### Deliverables
Recorded rulings on NB-000/001/002, RD-5, RD-6; resolutions of CF-1/CF-2/CF-3; a statement
of v3.3's identity or an explicit ruling that it has none.

### Tests
None — this phase produces decisions, not code.

### Exit criteria
- [ ] NB-001 answered — every citation in every review package becomes well-founded
- [ ] RD-6 answered — Phase 1 results become observable in CI
- [ ] RD-5 answered — Phase 5 becomes reachable at all
- [ ] CF-1 answered — determines whether RM-01…RM-07 are defects or specification gaps
- [ ] CF-3 answered — Gate 1 / Gate 2 precedence stated

> **RD-6 is the cheapest and highest-leverage item in the programme.** It is a scoping
> ruling, not a semantic choice, and it is answerable independently of RD-5.

---

# PHASE 1 — CHARACTERIZATION

**Prerequisites:** none. **Runs in parallel with Phase 0.**

### Allowed work
- EN-01…EN-14 — characterization tests CH-01…CH-15 (`03`)
- EN-15…EN-20 — observability OB-A6, OB-E, OB-F4, OB-G6, OB-D4, OB-I5 (`05`)
- EN-21…EN-23 — Guard T-0a, T-0b, T-0c (`06`)
- EN-24…EN-35 — documentation of existing behaviour
- Control tests CT-1…CT-4 in every module

### Forbidden work
- Changing **any** computed value
- Adding any check, clamp, bound, or validation **response**
- Wiring into CI (**RD-6** — this is reported, not worked around)
- Phrasing any test as asserting correctness
- Creating any fixture in `fixtures/normative/`

### Deliverables
Five characterization modules; observation records carrying
`"normative_effect": "NONE"`; three Guard characterization tests; `KL-00x` documentation
entries; corrected GAP-C5 and the four Guard "any" claims.

### Tests
The deliverables **are** the tests. Each carries verbatim:
> **THIS TEST CHARACTERIZES CURRENT IMPLEMENTATION BEHAVIOUR AND DOES NOT SELECT NORMATIVE SEMANTICS.**

### Exit criteria
- [ ] All 12 task-required characterization cases recorded as executable facts
- [ ] Every module carries controls proving it **executes** rather than replays
- [ ] **T-0c pins the Guard nine-field preimage** as a known-answer vector
- [ ] No production code modified — verifiable by `git diff` over non-test paths
- [ ] Every observed value labelled implementation-derived and non-normative

---

# PHASE 2 — NORMATIVE ARI CONTRACT

**Prerequisites:** Phase 0 (NB-001, RD-5). Phase 1 evidence strongly recommended — it is
what makes the decisions measurable.

### Allowed work
- Answer **RD-1** — does the specification define ARI, or does it remain implementation-defined?
- Specify AG-01, AG-02, AG-03, AG-04, AG-08, AG-09, AG-10, AG-11, AG-12 (`02`)
- Answer **RD-4** — authoritative engine and penalty model
- Answer **RD-2** — author APS-001 §8; state INV-008's trigger condition
- Advance SPEC-002 (or APS-001) beyond DRAFT through governance

### Forbidden work
- **Adopting current implementation behaviour as the definition** (stop condition 8)
- Adopting `[0, 100000]` because docstrings state it — no normative source does
- Writing conformance fixtures (Phase 7)
- Changing implementation code (Phase 5)
- Reading `core/evaluator.py` as a specification source

### Deliverables
An approved ARI specification covering AG-01…AG-04 and AG-08…AG-12; a designated
authoritative engine and penalty model; APS-001 §8 authored; INV-008's trigger stated.

### Tests
None yet — specification text precedes fixtures.

### Exit criteria
- [ ] ARI defined **without reference to RI-PY** — breaking the `GLOSSARY.md:27-28` circularity
- [ ] Range defined, with its enforcement point stated
- [ ] One engine designated authoritative; one penalty model selected
- [ ] Behaviour for dimension mismatch, zero vectors and malformed input specified
- [ ] Every AG dimension in scope traceable to an approved clause

---

# PHASE 3 — DETERMINISTIC ARITHMETIC CONTRACT

**Prerequisites:** Phase 2.

### Allowed work
- Answer **RD-3** — AD-CA-007 in full: width, signedness, scale, endianness, dimension,
  **rounding**, and **division**
- **Extend the register to include a division rule** — verified absent from every candidate list
- Specify AG-05, AG-06, AG-07, AG-13
- Answer **RD-7** — AD-CA-008: canonical serialization, byte sequence, hash domains
- Answer **NB-018** — Merkle construction
- Reconcile `CONSTITUTION_DIM = 1536` against `init.sql`'s `vector(32)`

### Forbidden work
- Selecting `round-half-to-even` **because Python does it** — it is a candidate only
- Selecting floor division **because Python does it** — it is not even a candidate
- Treating `core/test_offline_normalizer.py:97-107` as authority — it already locks in a candidate
- Implementing anything (Phase 5)

### Deliverables
Approved AD-CA-007 including a division rule; approved AD-CA-008; a Merkle construction
selection; a production-grade canonical byte encoding; a single dimension.

### Tests
None yet.

### Exit criteria
- [ ] Division rule for negative dividends **explicitly stated** — the register extended, not merely resolved
- [ ] Rounding rule stated, covering `.5` boundaries **both signs**
- [ ] Integer width **and accumulator width** stated (measured: `1.536×10¹³`, ≈7154× `i32::MAX`)
- [ ] Overflow behaviour stated
- [ ] One canonical serialization form; one byte encoding; hash domains defined
- [ ] Merkle construction selected

---

# PHASE 4 — INTEGRITY CONTRACT

**Prerequisites:**
**Core half:** Phase 3. **Guard half: NONE — available today.**

### Allowed work
- **GUARD (now):** decide D1, D2, then D3+D4+D5 jointly, then D6, D7, D8 (`06`)
- **CORE (after Phase 3):** define the evidence-chain contract; resolve the three
  canonicalizations; specify Merkle domain separation

### Forbidden work
- Deciding D1 **without** D4 — would create a determinism surface where none exists today
- Implementing any binding before D1–D7 are complete
- Choosing a byte reduction that is **not injective** (T-4 is the correctness core)

### Deliverables
Guard: D1–D8 recorded; a selected boundary among B1–B5; a migration mechanism; a
disposition for existing RFC 3161 tokens. Core: an evidence-chain contract.

### Tests
Guard: TG-1…TG-7 (empty / one / multiple / reordered / mutated / fabricated / control) plus
T-1…T-11 specified in `06`.

### Exit criteria
- [ ] D1–D8 recorded with rationale
- [ ] **TG-4 answered explicitly** — is violation order significant?
- [ ] Injectivity of the byte reduction demonstrated (T-4)
- [ ] `f32` representation settled (D4)
- [ ] Migration path stated; historical-log disposition stated
- [ ] **TG-7 control passes** — existing coverage was extended, not replaced

> **The Guard half of this phase can begin before Phase 0 concludes.** It is the only
> substantial engineering decision in the ecosystem with no governance dependency.

---

# PHASE 5 — REFERENCE IMPLEMENTATION CORRECTION

**Prerequisites:** Phases 2, 3, 4 **and RD-5 answered permissively**. If RD-5 rules that
FROZEN prohibits correction, this phase **cannot occur under the v3.3 identity** and a
lineage decision is required first.

### Allowed work
- AD-01…AD-10, AD-13, AD-14 (`10` §4) — each citing its authorizing decision
- Replace characterization tests with regression tests asserting the **decided** behaviour

### Forbidden work
- Any correction whose authorizing decision is not recorded
- **Deleting** characterization tests — they are **replaced**, and the replacement cites the decision
- Silently updating a pinned constant when a characterization test fails
- Any change without the custodian signature `Decree Art. X` requires for `core/` changes

### Deliverables
A corrected RI-PY; regression suites; a recorded authorization per change; a lineage/identity
statement.

### Tests
RT-A1…RT-A8; XL-01…XL-08 regressions; CH-01…CH-15 converted to assertions of decided
behaviour.

### Exit criteria
- [ ] Every correction traceable to an approved decision
- [ ] Every characterization test either still passing or **deliberately replaced with the decision cited**
- [ ] Both engines reconciled per RD-4
- [ ] `drift` and its docstring agree
- [ ] Evidence chain connected — evaluation → Merkle → persistence
- [ ] Custodian signature recorded for every `core/` change

---

# PHASE 6 — INDEPENDENT IMPLEMENTATION

**Prerequisites:** Phases 2, 3, 5. All nine `08` §2 prerequisites met.

### Allowed work
- Build a second implementation **in a different language with different default semantics**
- Author normative fixtures **derived from specification text**
- Build the comparison harness (P-8: consumes emitted records, imports neither implementation)

### Forbidden work
- Supplying RI-PY source, docstrings, observed values, or artefacts to the implementer (X-1…X-10)
- Generating any fixture **by executing an implementation** (§5.2 of `08`)
- Building it in **Python** — it would inherit `//` and `round()` and detect nothing (I-4)
- Adjusting the second implementation until it matches RI-PY (CR-6)
- Resolving specification ambiguity by reading code — ambiguity is a **specification defect**

### Deliverables
A second implementation; normative fixtures with provenance; a comparison harness; an
independence attestation.

### Tests
Byte-level replay per `08` §6 (P-1…P-8), including failure-case comparison.

### Exit criteria
- [ ] Implementer attests to no RI-PY exposure
- [ ] Every fixture's provenance traces to an approved clause, **never to execution**
- [ ] Both implementations match the **fixture** — not merely each other
- [ ] Divergences reported **before** reconciliation
- [ ] `SPEC-002 §10` Independent Implementer Test satisfiable

---

# PHASE 7 — CONFORMANCE KIT

**Prerequisites:** Phase 6; CONF-001…010 beyond DRAFT; APS-400 beyond DRAFT; FIX-001 and
FIX-ERROR authored; NB-002 and CF-1 answered.

### Allowed work
- CB-1…CB-5 guard-rails — **available today** (`09` §7)
- Implement the seven `ConformanceLayer`s
- Populate `fixtures/normative/`
- Build the conformance runner (RI-004, currently MISSING for both implementations)

### Forbidden work
- Populating `fixtures/normative/` before the corresponding decision exists
- Citing a DRAFT document as fixture provenance (AC-6)
- Loading any artefact carrying `"normative_effect": "NONE"` (AC-2)
- Treating implementation agreement as conformance (§3.1 of `09`)
- Implementing the ORACLE layer before all others — **an Oracle *is* the normative answer, encoded**

### Deliverables
A populated kit; a conformance runner; fixtures with provenance; the AC-1…AC-7 controls
enforced mechanically.

### Tests
CONF-001…CONF-010 executed against both implementations.

### Exit criteria
- [ ] Every fixture carries provenance to an approved clause
- [ ] The loader **mechanically refuses** characterization artefacts
- [ ] Both implementations run against the same fixtures
- [ ] A failure reports *"implementation disagrees with specification"*, never *"implementations disagree"*
- [ ] No fixture derived by executing an implementation

---

# PHASE 8 — PYTHON/RUST RUNTIME INTEGRATION

**Prerequisites:** Phases 3, 5, 6, 7; **NB-020 answered** — are Core and Guard one system or
two products, and is an integration boundary wanted **at all**?

### Allowed work
- Implement the boundary option selected under NB-020 (A: test vectors · B: wire · C: FFI ·
  D: remain separate)
- Define the wire schema or in-memory layout if applicable

### Forbidden work
- Building a boundary before NB-020 — **Option D (remain separate) is the current de-facto
  state and a legitimate outcome**
- Option C (FFI) without AD-CA-007 in its strongest form
- Option C without resolving Guard's crate-level `unsafe_code = "forbid"`

### Deliverables
Per NB-020. **Possibly none** — Option D requires only that "one ecosystem" claims in
READMEs be reconciled with reality.

### Tests
Boundary-specific; cross-language replay if a runtime boundary is built.

### Exit criteria
- [ ] NB-020 answered
- [ ] If a boundary is built: schema/layout defined, and cross-language determinism verified
- [ ] If Option D: documentation reconciled with the two-product reality

---

# PHASE 9 — CROSS-PLATFORM REPLAY

**Prerequisites:** Phases 5, 6; RD-6 answered (CI scope).

### Allowed work
- Extend determinism comparison to the full evaluation path
- Add architectures beyond x86_64 and arm64
- Add a **non-CPython** leg
- Compare **cross-language** records from Phase 6

### Forbidden work
- Treating x86_64-vs-arm64 agreement as **cross-language** determinism — both legs are
  CPython and **cannot** detect AG-06 or AG-07
- Comparing implementations without comparing both to the fixtures

### Deliverables
Cross-platform and cross-language determinism evidence; a determinism report covering the
evaluator.

### Tests
Byte-level replay across architectures **and** languages.

### Exit criteria
- [ ] ARI computation observed on ≥2 architectures
- [ ] ARI computation observed in ≥2 languages
- [ ] Byte-identical outputs for identical normative fixtures
- [ ] Failure classes reproduce identically
- [ ] **INV-002 (Bit-Perfect Replay) and INV-006 (Platform Independence) move off NOT VERIFIED**

---

# PHASE 10 — RELEASE GATE

**Prerequisites:** all prior phases.

### Allowed work
- Certify RI-PY and RI-RS against APS-950
- Bind v3.3's (or its successor's) cryptographic identity — the unfilled
  `[COMPUTED_AT_SEALING_v3.3]` placeholder
- Perform the sealing ceremony per `OPS_PROTOCOL_CANONICAL.md`
- Record custodian authorization

### Forbidden work
- Declaring conformance without conformance evidence (stop condition 9)
- Sealing while any INV row reads NOT VERIFIED
- Releasing while any AD-CA domain remains UNRESOLVED
- Sealing without a computed checksum — the current identity gap

### Deliverables
Certified implementations; a bound identity (tag + SHA + archival artefact); a sealing
record; a custodian signature.

### Tests
The full conformance suite, green, on all supported platforms and both implementations.

### Exit criteria
- [ ] Both implementations **CERTIFIED** (both are NOT CERTIFIED today)
- [ ] Every INV row VERIFIED (all are NOT VERIFIED today)
- [ ] Every AD-CA domain RESOLVED (all twelve are UNRESOLVED today)
- [ ] SPEC-002 APPROVED (`0.3-DRAFT` today)
- [ ] All ten CONF tests beyond DRAFT
- [ ] Identity bound — checksum computed, tag created, archival artefact produced
- [ ] Custodian signature recorded

---

## §3 The Two Tracks

```
CORE TRACK  (Protocol Custodian gate)
Phase 0 ──► Phase 2 ──► Phase 3 ──► Phase 4(core) ──► Phase 5 ──► 6 ──► 7 ──► 8 ──► 9 ──► 10
   │
   └── Phase 1 runs in parallel, gated by nothing

GUARD TRACK  (product-owner gate — NO governance dependency)
Phase 1(Guard: T-0a/b/c, docs, arm64) ──► Phase 4(Guard: D1…D8) ──► implement ──► TG-1…TG-7
   │
   └── may start TODAY
```

## §4 Critical Path

**Longest dependent chain:**
`Phase 0 (RD-5) → Phase 2 (RD-1) → Phase 3 (RD-3) → Phase 5 → Phase 6 → Phase 7 → Phase 9 → Phase 10`

**Every link is a decision, not an engineering task.** The programme is
decision-bound, not implementation-bound — which is why Phase 1 (unblocked, and the input
those decisions need) should start immediately and in parallel.

## §5 What Is Available Today

| Work | Phase | Gate |
|---|---|---|
| Characterization tests EN-01…EN-14 | 1 | **none** |
| Observability EN-15…EN-20 | 1 | **none** |
| Guard T-0a/T-0b/T-0c, docs, arm64 (EN-21…EN-27) | 1 | **none** |
| Documentation EN-28…EN-35 | 1 | **none** |
| Conformance guard-rails CB-1…CB-5 | 7 (prep) | **none** |
| **Guard decisions D1–D8** | 4 | **product owner** |
| **Governance rulings RD-5, RD-6, NB-000/001/002, CF-1/2/3** | 0 | **Custodian** |

**Everything else waits on a decision.**

---

*This document has no normative effect. It orders work by dependency and executes none of it.*
