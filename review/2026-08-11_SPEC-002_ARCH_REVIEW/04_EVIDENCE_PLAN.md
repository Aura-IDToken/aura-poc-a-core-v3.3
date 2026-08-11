# 04 — Evidence Plan

Document ID: REV-2026-08-11-004
Status: DRAFT — ANALYSIS ARTIFACT, NO NORMATIVE EFFECT
Date: 2026-08-11

---

## 0. Scope and honest preconditions

This plan specifies the evidence required to demonstrate that the Constitution Artifact
contract is satisfiable. It is a **plan**, not a claim of evidence: at the time of review,
**zero** of the artifacts below exist.

Two preconditions govern the whole plan and are stated up front because they determine
whether any of it is executable:

**P-1 — Nothing in E1…E12 can be authored before its governing AD-CA domain is resolved.**
A fixture encodes an expected value; an expected value *is* the decision. Authoring fixtures
first would make the fixture the de-facto specification and invert the governing direction
that SPEC-002 §"Governing Direction" prohibits. Each evidence item below therefore names its
blocking decision, and the plan's execution order is: **decision → requirement → invariant →
test → fixture → evidence**, never the reverse.

**P-2 — E12 has no second party today.** Cross-language replay requires two independent
implementations of the Constitution Artifact surface. Verified: `aura-poc-a-core-v3.3` has a
*placeholder* embedding and no code path that reads `AURA_CONSTITUTION.md`;
`aura-guard-v1.3` has no constitution, vector, or ARI code at all. E12 is therefore the one
item in this plan that cannot be scheduled until an independent implementation is
commissioned — and E12 is the item that decides the success criterion for the entire stage.

**Identifier discipline.** No EVID, CONF, FIX, or INV identifier is invented. Every such cell
reads `identifier not yet assigned`. The `E1…E12` labels are *plan-local handles* from the
review task, not protocol identifiers, and MUST be replaced by assigned identifiers before
use.

---

## 1. Evidence register

Each item states: the requirement it discharges, the decision that must precede it, the
invariant it exercises, the test, the expected result, and the artifact produced.

---

### E1 — Canonicalization fixtures

| Field | Value |
|---|---|
| **Requirement** | REQ-002-006, 007, 010, 011; REQ-002-035 *(proposed)* |
| **Decision** | **AD-CA-002** (canonicalization) and **AD-CA-004** (normalization rules — currently **ORPHANED**, see 01 §F-ORPHAN) |
| **Invariant** | `identifier not yet assigned` |
| **Test** | `identifier not yet assigned` |
| **Expected result** | For each fixture: the byte sequence produced by canonicalizing the input source is **exactly** the recorded expected byte sequence, on every conformant implementation |
| **Artifact** | `fixtures/canonicalization/FIX-xxx_*.json` + expected `.bin` per case |

**Required cases.** Encoding declaration; BOM present / absent; CRLF vs LF vs CR; trailing
newline present / absent; Unicode normalization form NFC / NFD / NFKC / NFKD applied to the
same logical text; combining-character sequences; homoglyph pairs; zero-width characters;
front-matter inclusion / exclusion; the "*Source: Original text preserved in …*" footer
inclusion / exclusion; `.md` vs preserved `.txt` representation of the same document
(REQ-002-035).

> **Blocking conflict.** E1 cannot be authored while the two reference implementations
> disagree on whether source canonicalization exists at all: `aura-guard-v1.3`
> `src/normalizer.rs` defines a strict, **lossy** ordered pipeline (NFKC → hidden-character
> strip → confusable fold → lowercase, "any deviation invalidates the shadow hash") under its
> own out-of-hierarchy `SHADOW_SPEC v1.0`, while `aura-poc-a-core-v3.3` has no
> canonicalization stage whatsoever. See 01 §C-1, OD-006.

---

### E2 — Artifact fixtures

| Field | Value |
|---|---|
| **Requirement** | REQ-002-010, 021, 023 |
| **Decision** | **AD-CA-003** (transformation pipeline), **AD-CA-008** (serialization) |
| **Invariant** | `identifier not yet assigned` (relates to existing INV-003) |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Canonical source → **exactly one** Constitution Artifact, byte-identical across implementations |
| **Artifact** | `fixtures/artifact/FIX-xxx_*.json` + expected canonical bytes |

**Required cases.** Minimal well-formed source; full AURA Constitution v1.0; multi-document
Source Set (if AD-CA-001 admits one); each field of the artifact present / absent /
null-valued; field-ordering permutations of the same logical content (all MUST serialize to
the same bytes).

> **Blocked by U-2** (`03_SPEC-002_v0.4_DRAFT.md` §7): APS-200 §8 is a TODO and currently
> permits JSON, CBOR, *or* Protobuf. Three permitted formats means three different byte
> sequences for the same artifact.

---

### E3 — Vector golden vectors

| Field | Value |
|---|---|
| **Requirement** | REQ-002-012, 024; REQ-002-036, 037, 043 *(proposed)* |
| **Decision** | **AD-CA-003**, **AD-CA-005**, **AD-CA-006** (**ORPHANED**), and ADP-001 (**does not exist**) |
| **Invariant** | `identifier not yet assigned` |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Artifact → **exactly one** Constitution Vector; every component byte-identical across implementations |
| **Artifact** | `fixtures/vector/FIX-xxx_*.json` with full component listing |

**Required cases.** Empty input; single-character input; input exactly at the vector
dimension; input one below and one above the dimension (**this is where the current
implementation silently truncates**); the full Constitution text; inputs producing extremal
component values.

> **Hard prerequisite.** ADP-001 is **0/14 defined** (01 §7). No golden vector can be computed
> from a name. E3 is unschedulable until ADP-001 exists as a specification — or until the
> projection is defined under AD-CA-003 without the ADP-001 label.

---

### E4 — Numeric boundary fixtures

| Field | Value |
|---|---|
| **Requirement** | REQ-002-014, 031; REQ-002-038, 039, 040, 042 *(proposed)* |
| **Decision** | **AD-CA-007** |
| **Invariant** | `identifier not yet assigned` (relates to existing INV-006, INV-007, INV-008) |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Each boundary input produces either the single specified value or the specified explicit rejection — never a silent fallback |
| **Artifact** | `fixtures/numeric/FIX-xxx_*.json` |

**Required cases — this is the highest-value fixture set in the plan**, because two of these
cases have already been shown to diverge:

| Case | Why | Status |
|---|---|---|
| Negative operand integer division | Python floors; Rust/C/JS truncate | **divergence reproduced** — 01 §C-6 |
| Exact `.5` ties in float→fixed conversion | Python half-to-even; C/Rust half-away; JS half-up | **divergence reproduced** — 01 §C-7 |
| Mismatched operand dimensions | `zip` silently truncates | **fail-open reproduced** — 01 §C-10 |
| int32 min / max, ±1 either side | overflow behaviour undefined | untested |
| Accumulator overflow at maximum dimension | Python ints are unbounded; int64 is not | untested |
| Negative zero | representation undefined | untested |
| NaN / +Inf / −Inf on any float stage | rejection undefined | untested |
| Zero vector | `normalize_vector` raises; `embed_text` returns zeros — modules disagree | untested |
| Magnitude at the ±1% tolerance boundary | tolerance must not confer identity | untested |

> Each case MUST record the expected value **and** the expected behaviour of a conformant
> implementation in at least two languages. A single-language expected value is what produced
> the current situation.

---

### E5 — Serialization fixtures

| Field | Value |
|---|---|
| **Requirement** | REQ-002-021, 022 |
| **Decision** | **AD-CA-008**, and **AD-CA-004** (**ORPHANED**) |
| **Invariant** | `identifier not yet assigned` (relates to existing INV-003) |
| **Test** | `identifier not yet assigned` — MUST be **cross-implementation**, not self-comparison |
| **Expected result** | Logically equal objects serialize to identical bytes; the artifact byte sequence and the vector byte sequence are **separately** defined per their hash domains (REQ-002-022) |
| **Artifact** | `fixtures/serialization/FIX-xxx_*.json` + expected `.bin` |

**Required cases.** Key ordering permutations; absent vs null vs empty-string fields; integer
encoding (decimal string vs binary, width, signedness); endianness for any binary encoding;
nested-structure ordering; Unicode escaping policy; whitespace policy; trailing-separator
policy.

> **Test-design requirement.** The existing CONF-003 procedure — *"Serialize ENT-001 through
> ENT-008 objects twice independently (fresh process each time)"* — verifies one
> implementation against **itself**. That design is structurally incapable of detecting the
> divergences in E4, all of which are cross-language. The E5 test MUST compare two
> independent implementations. See 02 §4, U-7.

---

### E6 — Hash golden vectors

| Field | Value |
|---|---|
| **Requirement** | REQ-002-017, 018, 019, 020 |
| **Decision** | **AD-CA-008** |
| **Invariant** | `identifier not yet assigned` (relates to existing INV-011) |
| **Test** | `identifier not yet assigned` |
| **Expected result** | For each hash domain: the exact input byte sequence is recorded, and the resulting digest matches on every conformant implementation |
| **Artifact** | `fixtures/hash/FIX-xxx_*.json` — MUST record the **pre-image bytes**, not only the digest |

**Required cases.** Source hash domain; artifact hash domain; vector hash domain; any
additional domain the specification declares (REQ-002-018 permits more than two); the
domain-separation prefix or tag for each; a **cross-domain collision test** proving that the
same byte content in two different domains yields different digests; explicit
included-field and excluded-field enumeration per REQ-002-019.

> Recording only digests would make the fixture unverifiable without an implementation,
> defeating REQ-002-020. **The pre-image is the evidence; the digest is the checksum.**
>
> **Blocked by U-3 and U-4.** APS-200 §4 currently forces `created_at` (wall-clock) into every
> entity's `integrity_hash` pre-image, so an artifact hash would change on every
> construction; APS-300 §5 leaves `evidence_hash` undefined. Both must be corrected first.

---

### E7 — Identity binding tests

| Field | Value |
|---|---|
| **Requirement** | REQ-002-015, 016, 023, 024 |
| **Decision** | **AD-CA-009** |
| **Invariant** | `identifier not yet assigned` (relates to existing INV-015) |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Document, Artifact, Vector and Provenance identities remain **distinct and separately resolvable**; every binding field resolves to its target |
| **Artifact** | `evidence/EVID-xxx_identity_binding/` |

**Required cases.** Each identity independently present and distinct; a change to source
identity propagates to artifact identity; a change to artifact identity propagates to vector
identity; **identity collapse is detected and rejected** (`document_id == artifact_id`, etc.);
each binding field resolves; a dangling binding is rejected.

> **Blocked by U-3.** While APS-200 §4 conflates content with wall-clock provenance in a
> single `integrity_hash`, an "identity separation" test would be testing a data model that
> structurally cannot separate them. See 01 §X-7, OD-008.

---

### E8 — Provenance tests

| Field | Value |
|---|---|
| **Requirement** | REQ-002-025, 033 |
| **Decision** | **AD-CA-010** |
| **Invariant** | `identifier not yet assigned` |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Provenance is verifiable, **and** — per the boundary chosen under REQ-002-033 — provenance variation either does or does not alter canonical bytes, exactly as specified, with no unspecified path |
| **Artifact** | `evidence/EVID-xxx_provenance/` |

**Required cases — these are the task's §11 questions, rendered as tests.** For each of
{timestamp, Git commit, compiler, OS, CPU architecture, Python version, Rust version}: does
changing it change artifact identity? does it change vector identity? does it change canonical
bytes? The expected answer for each cell is **whatever AD-CA-010 decides** — the test's job is
to prove the implementation matches the decision, not to discover it.

> Current evidence, recorded without inference: timestamp **does** currently change identity
> (U-3); compiler/OS/language **do** currently change the vector across languages (E4
> divergences) although INV-006 says they must not; Git commit is bound nowhere; language
> versions are unbound because dependency closure (AD-CA-006) is orphaned.

---

### E9 — Lifecycle tests

| Field | Value |
|---|---|
| **Requirement** | REQ-002-026, 027, 028, 029; REQ-002-044 *(proposed)* |
| **Decision** | **AD-CA-011**, **AD-CA-012** |
| **Invariant** | `identifier not yet assigned` |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Every valid transition succeeds only with its required authority, precondition and evidence; **every invalid transition is rejected** |
| **Artifact** | `evidence/EVID-xxx_lifecycle/` |

**Required cases.** Each valid transition, with and without the required authority; each
transition with missing evidence; **REGISTERED without APPROVED** (must not imply approval);
**APPROVED without FROZEN** (must not imply freeze); modification attempt on a FROZEN artifact
(must be rejected); `supersedes` chain consistency; a broken lineage link; **self-asserted
status** (must be rejected — REQ-002-044).

> **Two blockers.** (a) The states `VERIFIED` and `REGISTERED` **do not exist** in
> `VERSIONING.md` §3 or GOV-001 §4; introducing them is a new decision (OD-015). (b) There is
> no registry to register into — APS-000 §7 describes one that does not exist (U-6). (c) The
> `doc/ci/frozen-check` job proposed by `ADR-001_DOCUMENT_MODEL` does not exist; the
> specification repository contains **no CI workflows at all**.

---

### E10 — Negative tests

| Field | Value |
|---|---|
| **Requirement** | REQ-002-031; SPEC-002 §5.2 cases 1–11 |
| **Decision** | all AD-CA domains |
| **Invariant** | `identifier not yet assigned` (relates to existing INV-008) |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Every listed condition produces an **explicit, deterministic rejection**. No silent fallback anywhere it could alter the canonical result |
| **Artifact** | `fixtures/negative/FIX-xxx_*.json` |

**Required cases** — one per REQ-002-031 condition: invalid source; missing source; ambiguous
source boundary; unsupported encoding; missing dependency; unapproved dependency; dependency
integrity mismatch; unknown dependency version; malformed dictionary; numeric overflow;
numeric out-of-domain; invalid canonicalization input; invalid transformation input; invalid
provenance binding; hash mismatch; identity mismatch; lineage inconsistency; registration
inconsistency; frozen-status inconsistency. Plus, from reproduced findings: **mismatched
vector dimensions** (currently returns a confident wrong answer rather than rejecting) and
**over-length input** (currently truncates silently).

---

### E11 — Cross-platform replay

| Field | Value |
|---|---|
| **Requirement** | REQ-002-030, 032 |
| **Decision** | AD-CA-007, AD-CA-008 |
| **Invariant** | existing **INV-006** (Platform Independence) |
| **Test** | existing **CONF-006** — **insufficient as written** |
| **Expected result** | Identical canonical bytes, identities and digests on every target platform |
| **Artifact** | `evidence/EVID-xxx_replay_platform/` |

**Required matrix.** x86_64 · ARM64 · (WASM, currently an architectural goal only), each on at
least two operating systems.

> **Existing coverage assessed.** `aura-poc-a-core-v3.3` does run a real x86_64 + ARM64
> determinism comparison in CI (`compare-determinism` job over
> `determinism-report-*.json`). That is genuine evidence and is credited as such — but it
> covers the **ARI evaluation path**, not Constitution Artifact construction, and it runs
> **Python on both sides**, so it is blind to every divergence in E4. E11 must be extended in
> both dimensions.

---

### E12 — Cross-language replay ⭐ **decisive**

| Field | Value |
|---|---|
| **Requirement** | REQ-002-030, 032; SPEC-002 §10 Independent Implementer Test |
| **Decision** | all AD-CA domains |
| **Invariant** | existing **INV-002**, **INV-014** |
| **Test** | `identifier not yet assigned` |
| **Expected result** | Two implementations in **different languages**, built **only** from approved specifications and without inspecting each other, produce identical canonical bytes, identical vectors, identical identities and identical digests |
| **Artifact** | `evidence/EVID-xxx_replay_language/` |

**Required matrix.** Python ↔ Rust ↔ C++ ↔ JavaScript, per the review task's §9 requirement.
Minimum viable evidence is **two** independent languages; four is the target.

> **This is the item that decides the stage.** It is also the only item in the plan with **no
> second party in existence** (P-2 above). Until an independent implementation is
> commissioned — one whose author has not read `aura-poc-a-core-v3.3` — the central binary
> criterion of SPEC-002 §9 cannot be evaluated at all. It is not failing; it is
> **unfalsifiable**, which is a strictly worse position and is why this is
> **BLOCKER-P0-009**.
>
> The divergences already reproduced under E4 are a preview of what E12 would find: an
> independent Rust implementer following today's documents produces different numbers, and
> **no existing test in either repository would detect it.**

---

## 2. Dependency order

```
AD-CA decisions resolved (all 12, incl. the two orphans)
        ↓
SPEC-002 requirements approved
        ↓
Invariants assigned  ──────────────┐  (must not extend the existing INV-010 violation:
        ↓                          │   5 invariants already lack CONF tests)
Conformance tests defined  ────────┘
        ↓
   ┌────┴──────┬──────────┬──────────┐
  E1          E2 ← E1     E4         E9  (needs a registry to exist first)
   ↓           ↓          ↓           ↓
  E3 ← E2,E4  E5 ← E2,E4  E10        E7 ← E2,E3  (needs APS-200 §4 corrected)
        ↓          ↓                      ↓
       E6 ← E5 (needs APS-200/300 corrected)     E8 ← E7
                   ↓
              E11 ← all
                   ↓
              E12 ← all + an independent implementation that does not yet exist
```

---

## 3. Status summary

| Item | Exists | Blocking decision | Blocking upstream defect |
|---|---|---|---|
| E1 | ❌ | AD-CA-002, **AD-CA-004 (orphaned)** | — |
| E2 | ❌ | AD-CA-003, AD-CA-008 | U-2 |
| E3 | ❌ | AD-CA-003/005/**006 (orphaned)**, ADP-001 absent | — |
| E4 | ❌ | AD-CA-007 | — |
| E5 | ❌ | AD-CA-008, **AD-CA-004 (orphaned)** | U-2, U-7 |
| E6 | ❌ | AD-CA-008 | U-3, U-4 |
| E7 | ❌ | AD-CA-009 | U-3 |
| E8 | ❌ | AD-CA-010 | U-3 |
| E9 | ❌ | AD-CA-011, AD-CA-012 | U-6; states don't exist |
| E10 | ❌ | all | — |
| E11 | ❌ (partial, wrong scope) | AD-CA-007/008 | U-7 |
| E12 | ❌ | all | **no independent implementation exists** |

**0 of 12 evidence items exist. 0 are currently schedulable, because all 12 AD-CA domains are
UNRESOLVED and 2 are unowned.**

---

*End of 04_EVIDENCE_PLAN.md*
