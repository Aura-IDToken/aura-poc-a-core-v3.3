# 07 — GOVERNANCE DEPENDENCY MAP

**Date:** 2026-08-12
**Mode:** READ-ONLY. **DR-002 is not solved. NB-021 is not solved. No decision is taken.**
**Normative effect:** NONE.

---

## §1 Purpose

Make it **unambiguous** which work can be executed immediately and which must stop for
human architectural approval.

Every entry follows the required shape:

```
DECISION  →  UNBLOCKS  →  ENGINEERING TASKS  →  TESTS  →  MERGE GATE
```

**This document does not resolve DR-002.** It maps what DR-002's resolution would release.

---

## §2 The Decision Register

| ID | Decision | Authority | Registered where? | State |
|---|---|---|---|---|
| **NB-000** | What `DR-002` refers to, and its mapping onto `AD-CA-001…012` | Protocol Custodian | **nowhere** | **UNRESOLVED** |
| **NB-001** | Which `aura-specification` is authoritative | Protocol Custodian | **nowhere** | **UNRESOLVED** |
| **NB-002** | Which Conformance Kit is authoritative | Protocol Custodian | **nowhere** | **UNRESOLVED** |
| **RD-1** | Does the specification define ARI, or does ARI remain implementation-defined? | Protocol Custodian / Architect | **nowhere** | **UNRESOLVED** |
| **RD-2** | Is APS-001 §2/§5/§8 authored; does INV-008 apply to dimension mismatch? | Protocol Custodian | APS-001 (**TODO**) | **UNRESOLVED** |
| **RD-3** | AD-CA-007 — numeric representation **including division** | Architect | `SPEC-002 §6` (rounding); **division nowhere** | **UNRESOLVED** |
| **RD-4** | Which ARI engine is authoritative; which penalty model | Architect | **nowhere** | **UNRESOLVED** |
| **RD-5** | **NB-021** — does FROZEN permit non-normative defect correction? | Protocol Custodian | **nowhere** | **INDETERMINATE** |
| **RD-6** | Does **CI infrastructure** fall inside the FROZEN boundary? | Protocol Custodian | **nowhere** | **UNRESOLVED** |
| **RD-7** | AD-CA-008 — canonical serialization, byte sequence, hash domains | Architect | `SPEC-002 §6` | **UNRESOLVED — "None approved"** |
| **D1–D8** | Aura-Guard integrity posture and format | **Product owner** | Guard design brief | **OPEN — not governance-gated** |

**Nine of eleven are registered in no specification document.** They are tracked only in the
engineering review packages — which is itself a governance finding (NB-000).

---

## §3 Dependency Chains

---

### CHAIN 1 — RD-6 · CI scope

```
DECISION   RD-6 — does CI infrastructure fall inside the FROZEN boundary?
    ↓
UNBLOCKS   GB-2  extend the determinism report to compute ARI
           GB-3  add a CI step running the ARI test suites
           RM-10 the ARI observability blind spot
    ↓
ENGINEERING TASKS
           • add `python3 -m unittest core.test_ari_observability` to run_all_checks.sh  (1 line)
           • add artifacts/rd-006-ari-observation.json to the upload list             (1 line)
           • wire the CH-01…CH-15 characterization modules into CI
           • add the OB-A…OB-J observations from `05`
           • compare records across the existing x86_64 and arm64 legs
    ↓
TESTS      CH-13 replay + import-set pin; OB-A6, OB-E1…E4, OB-F4, OB-G6
    ↓
MERGE GATE Custodian ruling on RD-6 recorded. **No other gate.**
```

**Cost to decide:** a **scoping ruling**, not a semantic choice. Narrower than RD-5 and
answerable independently of it.
**Value released:** observability for **every** ARI finding — RM-01 through RM-07.

> **This is the cheapest unblock in the entire ecosystem, and it gates the visibility of
> everything else.** The harness already exists, executes, and passes. It is inert because
> no CI step invokes it. **Two lines are drafted and deliberately unapplied.**

---

### CHAIN 2 — RD-5 / NB-021 · the freeze boundary

```
DECISION   RD-5 — does FROZEN permit non-normative defect correction?
           (Sub-questions: is the boundary FROZEN or SEALED?
            what is v3.3's normative identity, given no tag/SHA/artifact exists?
            do Gate 1 and Gate 2 of ROLE §4.1 apply jointly, and which prevails?)
    ↓
UNBLOCKS   GB-1  any code change to core/ or compliance/
           GB-4  any change altering hash inputs or the Constitution Vector
           the fix half of RM-01…RM-07; RM-05 and RM-14 entirely
    ↓
ENGINEERING TASKS
           • RM-05  correct the drift docstring        (documentation-only)
           • S-21   demo.py — catch ValueError          (demo aborts today)
           • S-22   demo.py — stop feeding floats into the int engine
           • S-25   datetime.utcnow() → datetime.now(timezone.utc)
           • RM-14  connect evaluation → Merkle → persistence
           • ...then everything gated on RD-1…RD-4
    ↓
TESTS      RT-A1…RT-A8 (`01` §A.8); regression suites replacing CH-01…CH-15
    ↓
MERGE GATE Custodian ruling recorded **+** `Decree Art. X` custodian signature
           ("Required for core/ changes") **+** AGENTS.md rule 13
```

**Three obstacles inside this chain, all recorded as facts, none reconciled:**

| # | Obstacle |
|---|---|
| **O-1** | `ROLE §4.1` Gate 1 permits correcting a mathematical error; Gate 2 rejects any change not preserving bit-identity, *"UNCERTAIN → REJECTED"*. **Every correction changes output. Gate 2 rejects exactly what Gate 1 permits.** |
| **O-2** | v3.3 has **no bound identity** — no git tag, no `releases/` directory, no checksum. `docs/LEGACY_PROTOCOL.md:78` still reads `SHA-256 checksum: [COMPUTED_AT_SEALING_v3.3]`. The question *"without changing its identity"* has no referent today. |
| **O-3** | **FROZEN ≠ SEALED.** The corpus binds absolute immutability to *sealing* (`OPS_PROTOCOL_CANONICAL.md §4.1`; `ROLE §6.5`). **Sealing has not occurred.** This is evidence against reading FROZEN as absolute — and is **not** evidence that FROZEN permits correction. |

---

### CHAIN 3 — RD-1 · normative ARI

```
DECISION   RD-1 — does the specification define ARI?
    ↓
UNBLOCKS   DB-3  designate the authoritative engine
           DB-4  select a penalty model
           DB-6  define the ARI range and its enforcement point
           RM-04, RM-06, RM-12
    ↓
ENGINEERING TASKS
           • author the ARI section (AG-01…AG-15 in `02`)
           • unify or designate between the two engines
           • define the enforcement point for bounds
           • build the independent implementation (`08`)
    ↓
TESTS      regression per `05` §13.2; conformance CONF-001; independent replay
    ↓
MERGE GATE SPEC-002 (or APS-001) advanced beyond DRAFT through governance
           + RD-5 for any code change
```

**Blocking sub-fact.** ARI is defined **only** in `glossary/GLOSSARY.md:27-28`, by reference
to RI-PY. RD-1 must break a circularity — the definition points at the implementation, and
the implementation is what is under audit.

---

### CHAIN 4 — RD-3 · AD-CA-007 numeric representation

```
DECISION   RD-3 — numeric representation: width, scale, signedness, endianness,
                  dimension, ROUNDING, and DIVISION
    ↓
UNBLOCKS   DB-1 division semantics · DB-2 rounding · DB-7 numeric representation
           RM-02, RM-03; partially RM-07; the Constitution Vector's byte identity
    ↓
ENGINEERING TASKS
           • fix or ratify the division at 4 sites
           • fix or ratify the rounding at core/offline_normalizer.py:88
           • define accumulator width (i64 minimum — measured 1.536×10^13)
           • reconcile CONSTITUTION_DIM=1536 vs init.sql vector(32)
           • define overflow behaviour
    ↓
TESTS      XL-01…XL-05 regression; cross-platform; cross-language (`08`)
    ↓
MERGE GATE AD-CA-007 approved + SPEC-002 beyond DRAFT + RD-5
```

**Sharpest sub-fact, re-verified this session.** AD-CA-007's candidate set is `32`,
`100000`, `signed int32`, `little-endian`, `Dictionary-Based Embedding`,
`round-half-to-even`. **No division rule appears — not as a decision, not as a candidate.**
RD-3 must therefore **extend** the register, not merely resolve it.

---

### CHAIN 5 — RD-7 / AD-CA-008 · serialization and hash domains

```
DECISION   RD-7 — canonical serialization format, canonical byte sequence, hash domains
    ↓
UNBLOCKS   unification of the three JSON canonicalizations (RM-07)
           canonical byte encoding for vectors
           Merkle construction selection (NB-018)
           Conformance Kit layers CANONICALIZATION / SERIALIZATION / CRYPTOGRAPHY / MERKLE
    ↓
ENGINEERING TASKS
           • single canonicalization module
           • defined byte encoding (production, not test-only)
           • reconcile Python odd-node duplication vs Guard RFC 6962
           • domain-separation prefixes
    ↓
TESTS      CH-11; XL-06…XL-08; cross-implementation Merkle verification
    ↓
MERGE GATE AD-CA-008 approved ("None approved" today) + RD-5
```

---

### CHAIN 6 — RD-2 · failure semantics

```
DECISION   RD-2 — is APS-001 §8 authored; does INV-008 cover dimension mismatch?
    ↓
UNBLOCKS   DB-5 required response to malformed input
           the fix half of RM-01 (P0-A)
    ↓
ENGINEERING TASKS
           • implement the decided response at the chosen boundary (BA-1…BA-5)
           • apply it to BOTH engines
           • reconcile the RI-PY INV-008 ✅ claim with observed behaviour
    ↓
TESTS      RT-A1…RT-A8; CONF-007 (currently DRAFT); FIX-ERROR (currently TODO)
    ↓
MERGE GATE APS-001 §8 authored + INV-008 trigger stated + CONF-007 beyond DRAFT + RD-5
```

**Blocking sub-fact.** INV-008 is a **Critical** invariant whose normative source is
**TODO**, whose conformance test is **DRAFT**, whose fixture is **TODO**, and whose
verification status is **NOT VERIFIED**. `RI-PY_AURA_POC_A_CORE.md:55` nonetheless records
it ✅ with evidence *"ARI=0 circuit breaker"* — while the malformed-input class yields
**ARI = 100000**. Recorded as an observation; RI-PY is not edited by this package.

---

### CHAIN 7 — D1–D8 · Guard integrity *(NOT GOVERNANCE-GATED)*

```
DECISION   D1  accept / mitigate / bind cryptographically
           D2  is retroactive verifiability required?
           D3  authoritative byte reduction    ← coupled
           D4  does f32 confidence participate ← coupled
           D5  hash domain
           D6  migration + schema discriminator
           D7  disposition of existing RFC 3161 tokens
           D8  API shape change
    ↓
UNBLOCKS   RM-08, RM-09
    ↓
ENGINEERING TASKS
           • bind violations at or above chain_hash (or adopt B5)
           • migration mechanism per D6
           • verifier updates
    ↓
TESTS      T-0a…T-0c NOW; TG-1…TG-7 and T-1…T-11 after D1–D7
    ↓
MERGE GATE **Product owner sign-off. No Protocol Custodian dependency.**
```

> **The only chain in this document whose gate is not the Protocol Custodian.**
> Guard contains zero occurrences of `constitution`, `ari`, `poca`, `frozen`, `freeze`.
> D1 and D2 can be taken today.

---

### CHAIN 8 — NB-000/001/002 · repository authority

```
DECISION   NB-000  what DR-002 refers to
           NB-001  which aura-specification is authoritative
           NB-002  which Conformance Kit is authoritative
    ↓
UNBLOCKS   the CITABILITY of every document in every review package
    ↓
ENGINEERING TASKS  none — this is not engineering work
    ↓
TESTS      none
    ↓
MERGE GATE Protocol Custodian ruling. Not resolvable by engineering.
```

**Why this is upstream of everything.** Every citation to `SPEC-002`, `AD-CA-007`,
`APS-100` or `INV-008` in **any** review document presupposes NB-001. This session was
scoped to `aura-nomos/aura-specification`, which contains **a one-line README and nothing
else**; the corpus actually cited is `AuraIDToken/aura-specification`. **The discrepancy is
recorded, not resolved.**

---

## §4 THE EXECUTION BOUNDARY

### §4.1 Claude may execute immediately — no approval required

Modifies no production code, changes no computed value, selects no semantic.

| # | Work | Basis |
|---|---|---|
| E-1 | Characterization tests CH-01…CH-15 (`03`) | NB-021 **CASE D**; Decree Art. VII |
| E-2 | Observability cases OB-A…OB-J (`05`) | as above |
| E-3 | Guard characterization T-0a…T-0c (`06`) | `SAFE_ENGINEERING_WORK.md` §1.1 |
| E-4 | Documentation of existing behaviour as AS-IS (`KL-00x`) | NB-021 **CASE A** |
| E-5 | Correct `docs/GAP-001.md` GAP-C5 from *"LARGELY RESOLVED"* | CASE A |
| E-6 | Correct Guard's four overbroad "any" claims (`06` §3.4) | documentation; no Guard gate |
| E-7 | Correct the stale formula comment at Guard `models.rs:95` | as above |
| E-8 | Record that `ari_vector_hash` hashes the constitution vector, not an ARI | CASE A |
| E-9 | Record that RI-PY's INV-008 ✅ is unsupported for the malformed-input class | CASE A — **observation only; RI-PY not edited** |
| E-10 | This entire review package | CASE A |

### §4.2 Must stop — human architectural approval required

| # | Work | Blocked by | Stop condition |
|---|---|---|---|
| S-1 | Add a length check to either engine | RD-2 + RD-5 | 1, 2 |
| S-2 | Add an upper clamp to ARI | RD-1 + RD-5 | 1, 2 |
| S-3 | Change the division semantics | **RD-3 — unregistered** | 1 |
| S-4 | Change the rounding semantics | RD-3 (candidate only) | 1, 8 |
| S-5 | Unify the three JSON canonicalizations | RD-7 ("None approved") | 1 |
| S-6 | Unify or designate between the two engines | RD-4 | 1 |
| S-7 | Correct the drift clamp **in code** | RD-1 + RD-5 | 1, 2 |
| S-8 | Wire ARI into CI | **RD-6** | 2 |
| S-9 | Generate a Constitution Vector / `constitution.json` | AD-CA-005/006/007 | 1, 4 |
| S-10 | Implement CR-007 | **explicitly BLOCKED** — `SPEC-002 §11.B` | 4 |
| S-11 | Write any SPEC-002 conformance test | `SPEC-002 §11` NOT READY | 5 |
| S-12 | Create any fixture with an expected ARI value | RD-1 | 5 |
| S-13 | Build a second ARI implementation | RD-1 + RD-3 | 1, 9 |
| S-14 | Implement any Guard integrity binding | D1–D7 | 1 |
| S-15 | Create a Python/Rust runtime interface | NB-020 + RD-3 | 1 |
| S-16 | Declare any finding remediated or conformant | evidence does not exist | 9 |

### §4.3 The boundary test

For any candidate task:

```
Does it change a value the system computes?           YES → STOP
Does it require choosing a protocol semantic?         YES → STOP
Does it encode an unresolved candidate in a fixture?  YES → STOP
Does it change a hash, byte sequence, or format?      YES → STOP
Does it modify code inside the frozen boundary?       YES → STOP pending RD-5
Does it change what an existing CHECK asserts?        YES → STOP (AGENTS.md rule 10)
                                                       ↓ all NO
                                                    EXECUTE
```

---

## §5 Critical Path

```
NB-001 (which spec repo?) ──────────────────────► citability of everything
                                                            │
RD-6 (CI scope) ──► observability ──► evidence for ─────────┤
                                       every decision       │
                                                            ▼
RD-5 (NB-021) ──────────────────────────────► any code change at all
                                                            │
RD-1 (define ARI) ──► RD-4 (engine) ────────────────────────┤
        │                                                   │
        └──► RD-3 (AD-CA-007 + division) ──► RD-7 (AD-CA-008)
                                                            │
                                                            ▼
                                              independent implementation
                                                            │
                                                            ▼
                                                    Conformance Kit
```

**Parallel and independent of the whole diagram:** **D1–D8 (Guard).**

| Rank | Decision | Cost | Releases |
|---|---|---|---|
| **1** | **RD-6** | scoping ruling | observability for all six Core findings |
| **2** | **D1 + D2** | product decision, **no governance dependency** | the P0 integrity gap |
| **3** | **NB-001** | governance ruling | citability of every document |
| **4** | **RD-5** | governance ruling | all code correction |
| **5** | **RD-1** | specification work | the ARI contract |

## §6 What This Document Does Not Do

Does not solve DR-002. Does not solve NB-021. Does not answer RD-1…RD-7 or D1–D8. Does not
select which repository is authoritative. Does not reconcile the three document conflicts
recorded in `00` §7.1. Does not create an ADR. Does not authorize any §4.2 item.

---

*This document has no normative effect. It maps dependencies and takes no decision.*
