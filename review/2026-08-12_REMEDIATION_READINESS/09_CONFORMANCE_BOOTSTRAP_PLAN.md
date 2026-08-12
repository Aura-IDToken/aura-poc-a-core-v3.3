# 09 — CONFORMANCE BOOTSTRAP PLAN

**Date:** 2026-08-12
**Mode:** STRUCTURE ONLY. **No conformance test, fixture, or expected value was created.**
**Normative effect:** NONE.

---

## §1 The Governing Principle

> **Do not populate normative tests until the corresponding normative decisions exist.**

The Conformance Kit's current emptiness is **correct behaviour, not a defect.**

Writing a SPEC-002 conformance test today would necessarily encode one of the unapproved
candidate answers from `AD-CA-001…012`. `SPEC-002:371` forbids exactly that:

> *"No candidate choice listed in this table constitutes a recommendation, preference,
> default, or implied architectural decision."*

**This plan therefore defines structure and provenance rules. It creates no test content.**

---

## §2 Current State

Verified at primary source; the kit repositories were audited in
`07_CONFORMANCE_AUDIT.md`.

| Aspect | State |
|---|---|
| Total executable test content | `def test_bootstrap(): assert True` — **one test, asserting `True`** |
| Requirements verified | **NONE** — zero references to `CONF-`, `INV-`, `REQ-002-` anywhere in either kit |
| SPEC-002 tested | **NO** — zero textual hits, and **logically impossible** while §6 stands |
| `ConformanceLayer` enum | seven layers named; **none implemented** |
| Declared dependency `jcs` (RFC 8785 canonicalization) | **never imported** — declared in anticipation |
| CONF-001 … CONF-010 | **all DRAFT** |
| APS-400 | `1.0-DRAFT` |
| FIX-001, FIX-ERROR | **TODO** |
| RI-PY / RI-RS certification | both **NOT CERTIFIED**; conformance runner (RI-004) **MISSING** for both |
| **NB-002** — which kit is authoritative | **UNRESOLVED** — active fork vs archived byte-identical twin |

**The kit is blocked by design, and it is correctly blocked.**

---

## §3 The Required Pipeline

```
        SPEC REQUIREMENT
   (approved; beyond DRAFT; an identified clause)
                 │
                 ▼
        NORMATIVE FIXTURE
   (expected value derived FROM THE TEXT —
    never from executing an implementation)
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
REFERENCE IMPL.      INDEPENDENT IMPL.
   (RI-PY)            (different language,
                       different defaults,
                       no RI-PY exposure)
      │                     │
      └──────────┬──────────┘
                 ▼
         CONFORMANCE TEST
   (both must match the FIXTURE — not each other)
```

### §3.1 The load-bearing arrow

**Both implementations are compared to the FIXTURE, not to each other.**

Comparing implementations to each other tests only *agreement*. Two implementations can
agree and both be wrong — and if the second was derived from the first, they will agree by
construction. **Only the fixture, derived from approved text, carries authority.**

### §3.2 Stage gates

| Stage | Precondition | Currently met? |
|---|---|---|
| SPEC REQUIREMENT | An approved clause, beyond DRAFT, with a stable identifier | **NO** — SPEC-002 is `0.3-DRAFT`, *"Normative effect: NONE until APPROVED"* |
| NORMATIVE FIXTURE | Provenance traceable to that clause | **NO** — FIX-001/FIX-ERROR TODO |
| REFERENCE IMPL. | RI-PY with a conformance runner | **NO** — RI-004 MISSING |
| INDEPENDENT IMPL. | Per `08` | **NO** — 9/9 prerequisites unmet |
| CONFORMANCE TEST | All four above | **NO** |

**No stage gate is currently met.** The pipeline is defined so that when gates open, the
order is not improvised.

---

## §4 Preventing Accidental Normative Authority

**The central risk this plan exists to contain.**

An implementation-derived value that enters a fixture becomes, in practice, the
specification — because from that point on, conformance means *"matches the fixture"*, and
the fixture means *"whatever the implementation did on the day it was recorded."* The
decision is then made, permanently, by nobody.

### §4.1 It has already happened once

`core/test_offline_normalizer.py:97-107` (`test_scale_to_fixed_point_rounding`) asserts
Python's half-to-even output. There is no specification to verify against. The test
therefore **locks in a candidate answer to AD-CA-007** — a decision `SPEC-002:371`
explicitly reserves.

**Recorded as a fact, not as an accusation.** The test predates this analysis and was
written in good faith. It is cited because it is the clearest available demonstration that
this failure mode is real, cheap, and invisible.

### §4.2 The controls

| # | Control | Mechanism |
|---|---|---|
| **AC-1** | **Provenance field, mandatory** | Every fixture carries the approved document + clause its expected value derives from. **A fixture without provenance is invalid and must not be loaded.** |
| **AC-2** | **Machine-enforced separation** | Characterization artefacts carry `"normative_effect": "NONE"`. The conformance loader **must refuse** any fixture carrying that marker. |
| **AC-3** | **Directory separation** | `fixtures/normative/` and `fixtures/characterization/` never share a path. No loader reads both. |
| **AC-4** | **Derivation prohibition** | No fixture-generation script may import, invoke, or subprocess any implementation. Enforceable by import audit in the kit's existing `mypy --strict` CI. |
| **AC-5** | **The provenance question** | For every expected value: *"where did this come from?"* must answer **"from clause X of approved document Y"** — never **"from running Z."** |
| **AC-6** | **Draft prohibition** | No fixture may cite a DRAFT document. All ten CONF tests, APS-400, and SPEC-002 are DRAFT today — so **no fixture may be written at all yet.** |
| **AC-7** | **Failure-mode declaration** | A conformance failure must be reportable as *"implementation disagrees with specification"*, never as *"implementations disagree with each other."* |

**AC-2 is the strongest control** because it is mechanical rather than procedural. The
characterization artefacts already carry the marker, and RD-006 already enforces its
presence with a test. Making the conformance loader **reject** that marker closes the loop
in a way review discipline alone cannot.

---

## §5 Future Test Structure

Defined; **not created**.

```
conformance/
├── fixtures/
│   ├── normative/            ← REQUIRES an approved specification clause
│   │   └── (EMPTY — correctly)
│   └── characterization/     ← implementation-derived; NEVER loaded by conformance
│       └── (may be populated now)
├── layers/
│   ├── parser/               ← blocked: AD-CA-004, AD-CA-007
│   ├── canonicalization/     ← blocked: AD-CA-002, AD-CA-008
│   ├── serialization/        ← blocked: AD-CA-008
│   ├── cryptography/         ← blocked: AD-CA-008, AD-CA-012
│   ├── merkle/               ← blocked: NB-018 (no spec selects a construction)
│   ├── oracle/               ← blocked: all of the above
│   └── tck/                  ← blocked: all of the above
├── runner/                   ← DEFINABLE NOW (shape only, no assertions)
└── provenance/               ← DEFINABLE NOW (AC-1 schema)
```

### §5.1 Layer blocking status

| Layer | Blocked by | Any unblocked subset? |
|---|---|---|
| PARSER | AD-CA-004, AD-CA-007 | no |
| CANONICALIZATION | AD-CA-002, AD-CA-008 ("None approved") | no |
| SERIALIZATION | AD-CA-008 | no |
| CRYPTOGRAPHY | AD-CA-008, AD-CA-012 | **partially — see §6** |
| MERKLE | **NB-018** — no specification selects a construction; the two existing implementations disagree | no |
| ORACLE | all of the above — *an Oracle **is** the normative answer, encoded* | no |
| TCK | all of the above | no |

**Seven of seven layers blocked**, six absolutely.

---

## §6 The Genuinely Unblocked Subset

Not everything is downstream of SPEC-002. Properties defined by **their own** implementation
specifications, rather than by the Constitution domain, are available:

| Candidate | Defined by | Status |
|---|---|---|
| Audit-layer behaviours | `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md` | **available** |
| Guard chain-digest rule | Guard's own module documentation + source | **available** |
| Guard RFC 6962 Merkle | RFC 6962 — an external normative standard | **available** |
| SHA-256 / HMAC known-answer vectors | FIPS 180-4 / RFC 2104 | **available** |

**Two cautions.**

1. **Scoping question, not an engineering one.** Whether the Conformance Kit is the right
   home for implementation-specific conformance — as opposed to *protocol* conformance — is
   an open scoping decision. This plan does not answer it.

2. **`AUDIT_LAYER_SPEC.md` is subject to conflict CF-1** (`00` §7.1): it states
   *"implementation governs"*, while Constitution Art. IV P1 and `CONTRIBUTING.md` state
   the opposite. **Building conformance tests on a document that defers to the
   implementation reintroduces the accidental-authority problem** — through a different
   door. CF-1 should be resolved before this subset is used as an authority base.

---

## §7 Bootstrap Sequence

| Step | Work | Gate | Available |
|---|---|---|---|
| **CB-0** | Resolve **NB-002** — which kit is authoritative | governance | blocked |
| **CB-1** | Define the fixture provenance schema (AC-1) | none | **NOW** |
| **CB-2** | Define the directory separation (AC-3) | none | **NOW** |
| **CB-3** | Implement the loader's refusal of `normative_effect: NONE` (AC-2) | none | **NOW** |
| **CB-4** | Define the runner shape — no assertions, no fixtures | none | **NOW** |
| **CB-5** | Add an import audit enforcing AC-4 | none | **NOW** |
| **CB-6** | Resolve **CF-1** (implementation vs specification precedence) | governance | blocked |
| **CB-7** | Conformance tests for the §6 subset | after CB-6 | blocked |
| **CB-8** | Advance CONF-001…010 beyond DRAFT | specification work | blocked |
| **CB-9** | Author FIX-001, FIX-ERROR from approved text | after CB-8 | blocked |
| **CB-10** | Implement the seven layers | after AD-CA-002…012 | blocked |
| **CB-11** | Certify RI-PY / RI-RS | after CB-10 + `08` | blocked |

**CB-1 through CB-5 are unblocked today.** They are the guard-rails — and building the
guard-rails *before* the content is the only order in which they can actually constrain it.

---

## §8 What Must NOT Be Done

| Prohibited | Stop condition |
|---|---|
| Writing any SPEC-002 conformance test | 5 — `SPEC-002 §11` NOT READY |
| Creating a fixture with an ARI expected value | 5 — RD-1 unresolved |
| Creating a fixture with a Constitution Vector | 5 — AD-CA-005/006/007 |
| Generating any fixture by executing an implementation | 8 — makes behaviour normative |
| Citing a DRAFT document as fixture provenance | 5 — AC-6 |
| Treating implementation agreement as conformance | 8 — §3.1 |
| Populating `fixtures/normative/` at all, today | 5 |
| Implementing the ORACLE layer | 1 — an Oracle **is** the normative answer |

---

## §9 What This Document Does Not Do

Does not create any conformance test, fixture, expected value, runner, or loader. Does not
resolve NB-002 or CF-1. Does not advance any CONF test beyond DRAFT. Does not certify any
implementation. Does not decide whether the kit is the right home for implementation-level
conformance. Does not modify either kit repository.

---

*This document has no normative effect. It defines the structure that will hold content,
and the rules that keep implementation behaviour out of it.*
