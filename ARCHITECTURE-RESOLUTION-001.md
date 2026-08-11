# ARCHITECTURE-RESOLUTION-001

**Architecture Resolution Brief — SPEC-002 v0.3 → v0.4**

| Field | Value |
|---|---|
| Document ID | ARCHITECTURE-RESOLUTION-001 |
| Version | 1.0-DRAFT |
| Status | DRAFT — ANALYSIS ARTIFACT |
| Classification | Decision-Ready Brief for Protocol Custodian / Chief Architect |
| Date | 2026-08-11 |
| Author | Claude — architectural & conformance audit role (`CLAUDE.md`) |
| Basis | `review/2026-08-11_SPEC-002_ARCH_REVIEW/` |
| Normative effect | **NONE** |

---

> **NORMATIVE EFFECT: NONE.**
>
> This document decides nothing. It approves nothing. It accepts, registers, freezes,
> supersedes and implements nothing. It resolves no AD-CA decision domain. It creates no
> ADR. It modifies no source code.
>
> Its sole function is to convert the SPEC-002 v0.3 architecture review into a set of
> **well-posed questions addressed to human architectural authority**, each anchored to
> evidence that exists in the repositories as of 2026-08-11.
>
> Per GOV-001 §9 and AURA Constitution Article VIII, the AI author of this document may not
> approve or freeze canonical documents and has not attempted to.

**Evidence discipline applied throughout.** Every claim cites a file and section that exists.
Where an identifier does not exist, the text reads *"identifier not yet assigned"*. Where the
repository supplies no candidate answer, the text reads **"decision required — no candidate
supported by existing material"** rather than importing an answer from outside the repository.
Candidate alternatives appear **only** where the repository itself contains them, and are
labelled with their source. Recommendations appear only where the question is clerical rather
than architectural, and are marked **[RECOMMENDATION — non-binding]**.

---

## 1. Executive Decision Summary

SPEC-002 v0.3 is a well-constructed contract document. Its requirements are sound, its
identity-separation discipline (§4.4) is correct, and its readiness self-assessment (§11
"NOT READY") is accurate. **The obstacle to v0.4 is not the quality of SPEC-002.** It is that
SPEC-002 rests on a normative substrate that is incomplete, internally contradictory, and in
two places already contradicted by shipped implementation behaviour.

Nothing below can be resolved by further analysis. Each item requires a human decision.

**The five findings that determine everything else:**

**A. The addressee of this brief is not unambiguously defined.**
The AURA Constitution (FROZEN) and GOV-001 name only a **Chief Architect**. SPEC-002,
`ADR-001_DOCUMENT_MODEL` and `arc/README.md` name only a **Protocol Custodian**.
`templates/SPEC_TEMPLATE.md` line 9 writes `Owner: Role / Name (Protocol Custodian / Chief
Architect)` — offering them as alternatives without equating them. No document in the
specification repository states that the two roles are the same person, the same office, or
distinct offices with distinct powers. This is recorded first because **every "decision
authority" cell in §5 is affected by it** — a brief cannot be routed to an undefined
addressee. → **DR-002**

**B. Two repositories claim the name `aura-specification`, and the authoritative one cannot
be determined from either.** REQ-002-003 requires "repository location" as part of Source
Document Identity. With two locations and no supersession record, **AD-CA-001 is
unresolvable in principle**, and AD-CA-001 blocks REQ-002-001 through REQ-002-011.
→ **DR-001**

**C. The document authority model is contested, and SPEC-002 exists only under the contested
side.** Constitution Article V (FROZEN) places APS-001 as root with ADR *below* Protocol
Invariants. `ADR-001_DOCUMENT_MODEL` (PROPOSED) inverts this: `RFC → ADR → ARC → SPEC → APS`.
The `SPEC-` artifact class is defined nowhere else, so on the current record **SPEC-002 has no
defined position in the canonical hierarchy**. → **DR-003**

**D. Two cross-language numeric divergences already exist in this repository and were
reproduced during review.** Integer division (Python floors, Rust/C/JS truncate) and
float→fixed rounding (Python half-to-even, C/Rust half-away, JS half-up). The second is on the
**Constitution Vector construction path**, and SPEC-002 §6 lists `round-half-to-even` as an
**unapproved candidate** — meaning the implementation has already committed to a candidate the
specification has not approved. Both are latent, not live. Both become permanent at freeze.
→ **DR-013, DR-014**

**E. No Constitution Artifact exists, and no independent implementation exists.**
No code path in `aura-poc-a-core-v3.3` or `aura-guard-v1.3` reads `AURA_CONSTITUTION.md`. The
success criterion — two independent engineers obtaining identical bytes — has **no second
party**, so it cannot be tested, passed, or failed. It is **unfalsifiable**, which is a worse
position than failing, because no CI signal can ever report it. → **DR-025**

**Decision load: 27 decisions, of which 13 are P0.** None is resolvable by an AI agent.
Execution order is given in §15; it is ordered by dependency, and the first three decisions
(DR-002, DR-001, DR-003) unblock disproportionately.

---

## 2. Repository Identity

### 2.1 Evidence

| Repository | HEAD at review | Contents | Write access from this session |
|---|---|---|---|
| `AuraIDToken/aura-specification` | `62d2d6b` | Full corpus: Constitution, APS-000…APS-950, SPEC-002 v0.3, GOVERNANCE.md, VERSIONING.md, invariants, conformance, templates, fixtures | Read only |
| `aura-nomos/aura-specification` | `eb2a4ec` | `README.md` (11 bytes, content: `# aura-specification`) and `.github/CODEOWNERS` | **Denied — HTTP 403** |

`aura-nomos/aura-specification` `.github/CODEOWNERS`:

```
* @AuraIDToken

/constitution/ @AuraIDToken
/aps/ @AuraIDToken
/governance/ @AuraIDToken
```

The path list mirrors the populated repository's directory layout, but `/governance/` does not
exist in `AuraIDToken/aura-specification` (governance lives in root `GOVERNANCE.md`). The
CODEOWNERS therefore describes an *intended* layout, not an observed one.

Both repositories are owned by accounts under the same project. Neither contains a
`supersedes` record, a redirect, a deprecation notice, or any statement of relationship.

### 2.2 Conflict

> **CONFLICT DETECTED — CR-A**
>
> **Source A:** Task and review scoping identify `AuraIDToken/aura-specification` as the
> specification repository.
> **Source B:** Session repository scope and the working clone identify
> `aura-nomos/aura-specification`.
> **Nature:** Two distinct repositories bear the same canonical name. Neither declares
> precedence. One holds all content; the other holds a layout stub and is the one this session
> was scoped to.
> **Impact:** SPEC-002 REQ-002-003 requires the *repository location* of each Source Document
> as part of Source Document Identity. "Which repository" is unanswerable, so **AD-CA-001
> cannot be resolved even in principle**, and AD-CA-001 blocks REQ-002-001 → REQ-002-011.
> Additionally, `aura-nomos/*` is the designated development target for this workstream but
> rejects pushes with HTTP 403 (an authorization denial — the egress proxy reports no relay
> failures), so the review package could not be filed in a specification repository at all.

### 2.3 Decision required

→ **DR-001.** No candidate is favoured by the evidence: the populated repository has content
on its side; the stub repository has session scope and CODEOWNERS intent on its side. This is
an organisational question about which GitHub organisation the project intends to inhabit, and
**no technical evidence bears on it.**

---

## 3. Document Authority Model

### 3.1 The three models present in the repository

**Model A — AURA Constitution Article V (Status: FROZEN, AURA-CON-001 v1.0)**

```
AURA Constitution
        ↓
Aura Protocol Specification (APS-001)
        ↓
Protocol Invariants (APS-100)
        ↓
ADR / ARR / RFC
        ↓
Aura Development Playbook
        ↓
Repository Documentation
        ↓
Implementation
```

Article V adds: *"A higher-level document has authority over a lower-level document in all
cases of conflict."*

In Model A: APS-001 is the **root normative specification**; ADRs sit **below** Protocol
Invariants and therefore cannot create invariants; there is **no `SPEC-` artifact class** and
**no `ARC-` artifact class**.

**Model B — `adrs/ADR-001_DOCUMENT_MODEL.md` (Status: PROPOSED, dated 2026-08-02)**

```
1. Idea / Problem Statement (informal)
2. RFC — RFC-###
3. ADR (if required for architecture) — ADR-###
4. ARC (architecture baseline derived from ADR/RFC) — ARC-###: ACCEPTED by Architecture Board
5. SPEC (normative requirements derived from ARC) — SPEC-###: APPROVED by Protocol Custodian
6. APS (release aggregation) — APS-###: Published by Release Authority
7. Implementation & Conformance Tests — Evidence (EVID-###)
```

In Model B: APS is a **downstream publication** aggregating frozen SPECs; ADR and ARC sit
**above** SPEC; the model declares eight new invariants `INV-DOC-001` … `INV-DOC-008`.

**Model C — the repository as actually structured.** `ADR-001_REPOSITORY_STRUCTURE.md`
(Status: **ACCEPTED**, 2026-07-23) established directories `/aps`, `/specification`,
`/invariants`, `/conformance`, `/adrs`, `/rfcs`, `/arc`, `/compliance`. This layout
accommodates both models simultaneously and adjudicates neither. `/arc` is empty; `/rfcs`
contains only a README.

### 3.2 Conflict — stated, not reconciled

> **CONFLICT DETECTED — CR-B**
>
> **Source A:** Constitution Article V (FROZEN) — APS-001 is root; ADR is subordinate to
> APS-100.
> **Source B:** `ADR-001_DOCUMENT_MODEL` (PROPOSED) — ADR/ARC are upstream of SPEC, which is
> upstream of APS.
> **Nature:** The two models **invert the authority direction** between APS and ADR/SPEC. They
> are not reconcilable by interpretation; one must yield.
> **Impact, three parts:**
> 1. **SPEC-002 has no defined position.** The `SPEC-` class exists only in Model B. Per
>    Article V and the Authority Precedence in `AGENTS.md`/`CLAUDE.md` (Constitution outranks
>    ADR), Model B is **not currently in force** — so SPEC-002 sits outside the canonical
>    hierarchy.
> 2. **Model B creates invariants an ADR is not entitled to create.** `INV-DOC-001`…`008`
>    appear in neither APS-100 §3 nor `invariants/INVARIANT_REGISTRY.md`, and the prefix
>    `INV-DOC` is absent from the APS-000 Appendix A canonical prefix registry. Under Model A,
>    Protocol Invariants (APS-100) outrank ADRs, so an ADR cannot originate them.
> 3. **Model B's own invariant is unsatisfiable today.** `INV-DOC-002` requires every SPEC to
>    reference at least one ARC. `/arc` contains only a README stating "ARC-001 … ARC-025 will
>    be synchronized … during Sprint 2"; `compliance/arc_to_spec_mapping.yaml` is
>    `mappings: []`; `compliance/ARC_TO_SPEC_MAPPING.md` defers to "when SPEC-001 is approved"
>    — and **SPEC-001 does not exist**. SPEC-002's Authority line cites the Constitution and
>    APS documents, **no ARC**.

### 3.3 Compounding conflict — the role set differs between models

> **CONFLICT DETECTED — CR-C**
>
> **Source A:** GOV-001 §2 authority hierarchy names: Chief Architect · Architecture Review
> Board (ARB) · Specification Contributors · AI Assistants. Constitution Article VIII names
> only **Chief Architect**.
> **Source B:** `ADR-001_DOCUMENT_MODEL` "Owners and Authorities" names: **Protocol Custodian**
> (approves SPECs) · **Architecture Board** (ARC + ADRs) · **Release Authority** (APS
> publication) · **Compliance Authority / Auditor**.
> **Source C:** `templates/SPEC_TEMPLATE.md` line 9: `Owner: Role / Name (Protocol Custodian /
> Chief Architect)` — presented as alternatives, never equated.
> **Source D:** This repository's `CONSTITUTIONAL_DECREE.md` Article V names *"Custodian of the
> Protocol (Architect)"*, and `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §2 derives the Custodian's
> powers from *"Constitutional Decree Article V"* — the **implementation repository's** decree,
> not the AURA Constitution.
> **Nature:** Two role vocabularies, four bodies in one and one office in the other, with no
> mapping between them. "Architecture Review Board" and "Architecture Board" are not stated to
> be the same body. "Release Authority" and "Compliance Authority" have no counterpart in
> GOV-001 or the Constitution.
> **Impact:** **The decision authority for every item in this brief is itself undetermined.**
> §5's "decision authority" column cannot be filled without this. It also means GOV-001 §5.2's
> "Architecture Review Board assessment" step may have no constituted body.

### 3.4 Decision required

→ **DR-002** (role identity and authority mapping) and **DR-003** (which document model is in
force). Both are **architectural and constitutional**. Under Model B's adoption path, a
Constitution amendment under Article XI would be required (RFC → Architecture Review → impact
analysis → dependent-document updates → Chief Architect approval).

**No candidate is recommended.** The evidence establishes only that the present state — both
models live, neither adjudicated — is not a viable third option, because ADRs cannot be
authored into an undefined hierarchy.

---

## 4. APS-001

### 4.1 Current state

`specification/APS-001_PROTOCOL_SPECIFICATION.md`:

```
Document ID: APS-001
Version: 0.1-DRAFT
Status: TODO
Classification: Root Normative Specification
Authority: AURA Constitution v1.0 (FROZEN)
Last Review: —

> **TODO: This document does not yet exist. It is the highest-priority gap in the
> Aura Protocol Specification. See ROADMAP.md Milestone 1.**
```

All ten sections are `> **TODO**` placeholders. The document contains **no normative content
whatsoever**. Its own Authoring Notes state: *"Do not copy or paraphrase existing
implementation behavior — specify from first principles."*

### 4.2 Dependencies on APS-001

Under Constitution Article V, APS-001 sits directly beneath the Constitution and above
APS-100. Every document below declares `Authority: APS-001`:

| Document | Declared Authority line | Consequence |
|---|---|---|
| APS-100 Protocol Invariants | `APS-001` | Every invariant's authority is a dangling reference |
| APS-200 Canonical Data Model | `APS-001 · APS-100` | ditto |
| APS-300 Evidence Model | `APS-001 · APS-100 · APS-200` | ditto |
| APS-400 Conformance Test Matrix | `APS-001 · APS-100 · APS-200 · APS-300` | ditto |
| APS-500 Reference Fixtures | `APS-100 · APS-200 · APS-300 · APS-400` | transitively |
| APS-950 Reference Impl. Requirements | `APS-001 · …` | ditto |

`invariants/INVARIANT_REGISTRY.md` cites APS-001 sections that do not exist: INV-001 and
INV-002 cite `APS-001 §2`; INV-008 cites `APS-001 §8`; INV-013 cites `APS-001 §5`.
`compliance/TRACEABILITY_MATRIX.md` marks these `APS-001 §2 (TODO)` — the matrix is honest
about it.

### 4.3 Which SPEC-002 requirements depend on APS-001

SPEC-002 §7 does not cite APS-001 directly. But the dependency is transitive and total: every
SPEC-002 requirement traced to APS-000, APS-200, APS-300, APS-900 or APS-950 inherits their
undefined authority. Specifically:

| SPEC-002 requirement | Depends on APS-001 section | Section status |
|---|---|---|
| REQ-002-017, 018 (hash domains) | §7 Cryptographic Requirements — *"Which hash algorithm is canonical?"* | TODO |
| REQ-002-031 (failure conditions) | §8 Error Handling — *"Define the fail-closed behavior… What constitutes a 'safe state'?"* | TODO |
| REQ-002-030 (independent verification) | §9 Conformance Requirements | TODO |
| REQ-002-010 (transformation pipeline) | §2 Protocol Execution Model | TODO |
| REQ-002-021, 022 (canonical serialization/bytes) | §4 Output Requirements | TODO |

SPEC-002 §11 already records this: *"APS-001 remains incomplete and upstream normative
authority is still blocked by documented gaps."* Review confirms the stronger statement:
APS-001 is not incomplete, it is **absent**.

### 4.4 Minimum decisions required before SPEC-002 can rely on APS-001

The following is a **statement of dependency, not a proposed scope**. SPEC-002 requires
answers from APS-001 in exactly these places:

| APS-001 section | Minimum content SPEC-002 needs | Serving |
|---|---|---|
| §7 Cryptographic Requirements | Which hash algorithm is canonical; whether more than one is permitted; key management if signatures are in scope | REQ-002-017, 018, 020 |
| §8 Error Handling | What "fail closed" means operationally; what a "safe state" is; whether partial output is ever permissible | REQ-002-031, and INV-008 conformance |
| §2 Protocol Execution Model | Whether artifact construction is a "protocol execution" at all — and therefore whether APS-200/APS-300 entity contracts apply to a Constitution Artifact | **REQ-002-015, 016, 022, 033** — see §9.2, this is the crux of the provenance problem |
| §9 Conformance Requirements | What "conformant" means; relationship to APS-400/APS-500 | REQ-002-030, 032 |

→ **DR-006.** Whether APS-001 must be complete, or whether a bounded subset (§2, §7, §8, §9)
suffices to unblock SPEC-002, is itself a decision. **Decision required — no candidate
supported by existing material**; `ROADMAP.md` Milestone 1 is referenced by APS-001 but
specifies no scope split.

---

## 5. AD-CA Ownership Matrix

**Column definitions.** *Owner artifact* — the governance artifact that would resolve the
domain. *Status* — as recorded in SPEC-002 v0.3 §6 and Appendix A(E). *Blocking requirements*
— quoted from SPEC-002 §6 "Blocking Effect". *Dependency* — what must be settled first.
*Decision authority* — **see the caveat below.**

> **CAVEAT ON THE AUTHORITY COLUMN.** Per §3.3 (CR-C), the role set is contested. Every cell
> below reads `Custodian / Chief Architect — role identity undetermined (DR-002)`. This is not
> hedging: SPEC-002's header names "Protocol Custodian", the Constitution and GOV-001 name
> "Chief Architect", and no document equates them. The column cannot be filled correctly until
> DR-002 is answered.

| AD-CA | Subject *(verbatim, SPEC-002 §6)* | Owner artifact | Status | Blocking requirements | Dependency | Decision authority |
|---|---|---|---|---|---|---|
| **001** | Authoritative Constitution source identity, Source Set, and exact Source Boundary | ADR-002 — **NOT AUTHORED** | UNRESOLVED | REQ-002-001 → 011 | **DR-001** (repository identity) must precede | Custodian / Chief Architect — undetermined (DR-002) |
| **002** | Canonicalization procedure for the authoritative Constitution source | ADR-002 — **NOT AUTHORED** | UNRESOLVED | REQ-002-007, 010, 011 | AD-CA-001; DR-011 (lossy vs lossless) | ditto |
| **003** | Transformation pipeline from source to artifact-ready representation | ADR-003 — **NOT AUTHORED** | UNRESOLVED | REQ-002-010, 011 | AD-CA-002; DR-027 (ADP-001) | ditto |
| **004** | Normalization rules affecting deterministic output | **NONE — ORPHANED** | UNRESOLVED | REQ-002-011, **021, 022** | — | ditto |
| **005** | Embedding method identity and versioning model | ADR-003 — **NOT AUTHORED**; **scope disputed** | UNRESOLVED | REQ-002-012, 016, 024 | **DR-008** (scope) must precede | ditto |
| **006** | Dictionary identity, versioning, integrity, change policy, and complete dependency closure | **NONE — ORPHANED** | UNRESOLVED | REQ-002-013, 016, 024, **034** | — | ditto |
| **007** | Numeric representation of vector values | ADR-004 — **NOT AUTHORED** | UNRESOLVED | REQ-002-014, 017 → 022 | DR-012, DR-013, DR-014, DR-015, DR-016 | ditto |
| **008** | Canonical serialization format, canonical byte sequence, and hash domain definitions | ADR-004 — **NOT AUTHORED** | UNRESOLVED | REQ-002-017 → 022 | **AD-CA-004** (orphaned); DR-017; upstream APS-200 §8 | ditto |
| **009** | Document / Artifact / Vector Identity schema and inter-identity binding fields | ADR-005 — **NOT AUTHORED** | UNRESOLVED | REQ-002-015, 016, 023, 024 | **DR-019** (APS-200 §4 correction) | ditto |
| **010** | Commit/execution provenance binding schema; whether provenance is in, out of, or externally bound to the canonical representation and hash domain(s) | ADR-005 — **NOT AUTHORED** | UNRESOLVED | REQ-002-025, 030, 031, 033 | AD-CA-009; DR-019 | ditto |
| **011** | Registration model, authoritative registry, registry fields, registration integrity semantics | ADR-006 — **NOT AUTHORED** | UNRESOLVED | REQ-002-028, 030, 031 | **DR-021** (registry does not exist); DR-022 | ditto |
| **012** | Freeze evidence, frozen-status verification model, immutability semantics | ADR-006 — **NOT AUTHORED** | UNRESOLVED | REQ-002-029 → 031 | **DR-023** (freeze authority / self-freeze) | ditto |

### 5.1 Ownership findings

**F-1 — Two domains are orphaned.** A five-ADR grouping covering
{002: 001,002 · 003: 003,005 · 004: 007,008 · 005: 009,010 · 006: 011,012} covers **10 of 12**.
**AD-CA-004 and AD-CA-006 have no owning artifact.** Both were verified present and UNRESOLVED
in SPEC-002 §6 and Appendix A(E); neither is inferred here.

This is load-bearing, not bookkeeping:

- **AD-CA-004 blocks REQ-002-021 and REQ-002-022** — the identical requirements ADR-004 exists
  to close through AD-CA-008. **ADR-004 therefore cannot close its own stated scope while
  AD-CA-004 is unowned.**
- **AD-CA-006 blocks REQ-002-034** (dependency closure). No ADR in the grouping addresses it,
  so *"same source → same vector"* remains unprovable: an undeclared dependency may vary
  between two conformant implementations without either violating anything.

→ **DR-007**

**F-2 — AD-CA-005's scope is disputed.** SPEC-002 §6 row 5 reads *"Embedding method identity
and versioning model"*, with `Dictionary-Based Embedding` as candidate. Review scoping
described it as *"vector projection mechanism"*. These are different decision types: method
identity/versioning is a **dependency-identification** decision feeding REQ-002-012; a
projection mechanism is an **algorithm-definition** decision, which SPEC-002 places under
AD-CA-003 and AD-CA-007. SPEC-002 never uses the word "projection". → **DR-008**

**F-3 — Zero coverage.** ADRs authored: **0/12**. Invariants assigned: **0/12** (all
*identifier not yet assigned*). Conformance tests assigned: **0/12**. Implementation coverage:
**0/12**. Evidence: **0/12**.

---

## 6. Numeric Semantics

### 6.1 Reproduced divergence 1 — integer division rounding

**Location.** `core/evaluator.py`, two sites:

```python
similarity = dot // self.SCALING_FACTOR
raw_ari = (self.weight_structural * si // self.SCALING_FACTOR) + \
          (self.weight_semantic * sa // self.SCALING_FACTOR)
```

**Mechanism.** Python `//` floors toward −∞. Rust `/`, C/C++ `/`, and JavaScript `Math.trunc`
truncate toward zero. For negative operands these differ by one unit in the last place.

**Reproduction.** Executed against `PoCAEvaluator` with a negative constitution component —
reachable through the public constructor, which accepts any `List[int]`:

```
dot                    = -7000029999
Python floor  (dot//S) = -70001
Rust/C++/JS trunc      = -70000
DIVERGENCE             = True
```

On the ARI path with `sa = -70001`:

```
Python  70000*sa//100000 = -49001
Rust    70000*sa /100000 = -49000
```

**Invariants affected.** INV-002 (Bit-Perfect Replay, Critical) and INV-006 (Platform
Independence, Critical). Both are worded *"on every conformant implementation"* — a
cross-implementation obligation, not merely cross-architecture.

**Scope qualification, stated precisely.** The shipped `core/embedding.py` emits only
non-negative components, so this does not fire on the demo path today. The existing
`compare-determinism` CI job compares x86_64 against ARM64 with **Python on both sides**, so it
is structurally incapable of detecting it. This is a **latent, reachable defect and a
specification gap** — not a live production failure. It becomes permanent if the instrument is
frozen in this state.

### 6.2 Reproduced divergence 2 — float→fixed-point tie rounding

**Location.** `core/offline_normalizer.py`:

```python
int_vector = [round(x * SCALING_FACTOR) for x in normalized_vector]
```

**Mechanism.** Python's built-in `round()` is **half-to-even** (banker's). C `round()` and
Rust `f64::round()` are **half-away-from-zero**. JavaScript `Math.round` is **half-up**.

**Reproduction.**

```
       x*1e5  Python round   half-away (C/Rust)   half-up (JS)
      0.5000             0                    1              1  <-- DIVERGES
      1.5000             2                    2              2
      2.5000             2                    3              3  <-- DIVERGES
      3.5000             3                    3              3
```

**Why this one is the more serious.** This is the **Constitution Vector construction path** —
the artifact whose identity the whole of SPEC-002 exists to pin down. And SPEC-002 §6 lists
`round-half-to-even` as a **candidate only**, with §3 constraint 4 stating: *"No candidate
choice listed in this document constitutes a recommendation, preference, default, or implied
architectural decision."* The implementation has nevertheless **already committed to that
candidate**, silently, by using a language builtin.

### 6.3 Related undefined numeric surface

| Item | Evidence | Status |
|---|---|---|
| Accumulator width / overflow | `sum(a * b for a, b in zip(v1, v2))` — Python ints are unbounded, so overflow is invisible. At dim 1536 × (10⁵)² the accumulator reaches ~1.5×10¹³, which fits int64 but not int32. Nothing specifies the width. | undefined |
| Endianness | REQ-002-014 explicitly defers byte order to the numeric contract; nothing supplies it. `to_bytes(..., byteorder='little')` appears in a test only. | undefined |
| NaN / ±Infinity | No rejection path on any float stage | undefined |
| Negative zero | No representation rule | undefined |
| Float summation order | `math.sqrt(sum(x * x for x in vector))` — IEEE-754 addition is non-associative; stable only under fixed order with no reassociation, FMA contraction, or vectorized reduction. `CONSTITUTIONAL_DECREE.md` Article VII *permits* float in this file; permission is not specification. | undefined |
| Tolerance vs identity | `verify_unit_vector` accepts ±1% (`tolerance = 0.01`) — a band admitting a large set of distinct vectors as "valid" | conflated |
| Fail-open on dimension mismatch | `zip(v1, v2)` silently stops at the shorter sequence. Executed with dim-1536 constitution and length-1 vector: returned `{'ari': 0, 'drift': 200000}` — no exception. Violates INV-008 and Constitution Article IV P6. | **NON-CONFORMANT against a live invariant** |
| Vector dimension | 1536 hard-coded in `embedding.py` and `offline_normalizer.py` (`CONSTITUTION_DIM`); SPEC-002 §6 lists bare token `32` | **conflict** |
| Input-length domain | `[base_pattern[i % len(base_pattern)] for i in range(1536)]` — tiles short input, **silently truncates** input over 1536 chars. The Constitution is ~6,500 chars. | undefined |

### 6.4 Decision questions — no model is selected

**DQ-6.1** — For integer division in the canonical pipeline, what is the rounding direction
for negative operands? *Candidates supported by existing material:* none. SPEC-002 §6 lists
`round-half-to-even` but that is a float rounding mode, not an integer division rule; no
document addresses integer division at all. → **DR-013. Decision required — no candidate
supported by existing material.**

**DQ-6.2** — At the float→fixed boundary, what is the rounding mode including tie behaviour?
*Candidate supported by existing material:* `round-half-to-even` (SPEC-002 §6, explicitly
**non-normative**, explicitly **not a default**). → **DR-014**

**DQ-6.3** — Is any floating-point stage inside the reproducibility contract? If yes, what
constrains summation order, reassociation, and FMA? *Candidate supported by existing material:*
`CONSTITUTIONAL_DECREE.md` Article VII permits float **only** in `offline_normalizer.py`,
which bounds *location* but not *semantics*. → **DR-014**

**DQ-6.4** — What are the integer widths at each stage (component, accumulator, result), and
what is the overflow behaviour (wrap / saturate / reject)? *Candidate:* `signed int32`
(SPEC-002 §6, non-normative) for components; nothing for the accumulator. → **DR-015**

**DQ-6.5** — What is the byte order of the numeric serialization? *Candidate:* `little-endian`
(SPEC-002 §6, non-normative). → **DR-015**

**DQ-6.6** — What is the vector dimension, and what does the token `32` in SPEC-002 §6 denote?
*Candidates:* `32` (SPEC-002 §6, non-normative, ambiguous between dimension and integer width);
`1536` (implementation and `docs/architecture.md`, **implementation-derived and therefore
inadmissible as authority**). → **DR-012**

**DQ-6.7** — What is the admissible input-length domain, and what is the behaviour for empty,
minimum, maximum, under-dimension and over-dimension input? *Candidate:* none. → **DR-016**

**DQ-6.8** — May tolerance-based validation establish canonical identity? → **DR-015**

> **NO ROUNDING OR DIVISION MODEL IS SELECTED BY THIS DOCUMENT.** The behaviours currently in
> `aura-poc-a-core-v3.3` are **implementation accidents**, not approved decisions. Per SPEC-002
> §3.4 and the review task's standing rule, they **must not be ratified by default merely
> because the implementation reached them first**. The reproductions in §6.1 and §6.2 are cited
> as evidence that the contract surface is incomplete — never as evidence of what the contract
> should say.

---

## 7. Canonical Serialization

### 7.1 Conflicting and undefined requirements

**S-1 — The cited authority is a TODO that permits three formats.**
SPEC-002 §7 traces REQ-002-021 ("one canonical serialization format") to **APS-200 §8**.
APS-200 §8 reads in full:

> Implementations MAY use different formats (JSON, CBOR, Protocol Buffers), provided:
> - Full model semantics are preserved
> - Deterministic serialization is guaranteed where required by the protocol
> - INV-003 (Canonical Serialization) is not violated
>
> > **TODO**: Define the canonical serialization format for interoperability between RI-PY and RI-RS.

Three permitted formats produce three different byte sequences for one artifact.

**S-2 — Circular definition.** APS-200 §4 defines `integrity_hash` as *"SHA-256 hash of **the
canonical serialization** of this object"*. The canonical serialization is S-1's TODO. The hash
is defined in terms of the undefined.

**S-3 — The evidence hash is likewise undefined, and its TODO names the open question.**
APS-300 §5: *"**TODO**: Define the canonical algorithm for computing `evidence_hash`. Must
reference INV-011 and specify whether the hash covers the full JSON serialization or a
field-ordered canonical form."*

**S-4 — APS-200 §9 defers the schemas.** *"**TODO**: Publish JSON Schema definitions for each
entity at a stable URL. Schemas belong in `fixtures/schemas/`."* Only
`fixtures/schemas/common-object-contract.schema.json` exists.

**S-5 — The conformance test cannot detect cross-implementation divergence.**
`conformance/CONF-003_CANONICAL_SERIALIZATION.md` §4 Test Procedure: *"Serialize ENT-001
through ENT-008 objects twice independently (fresh process each time)."* This verifies **one
implementation against itself**. It is structurally incapable of detecting the divergences in
§6. Its §3 also carries *"**TODO**: Specify exact preconditions once APS-200 schemas and
APS-500 fixtures are finalized"*, and §8 *"**TODO**: Link to specific fixture file"*.

**S-6 — There is no serializer in either implementation.** `docs/GAP-001.md` §3 independently
records *"APS-400 Serialization — ❌ Missing … No canonical serialisation module … No binary
serialisation contract. Byte order not specified in code."* (Note that GAP-001's "APS-400"
denotes Serialization, not the specification repository's Conformance Test Matrix — see §14
DR-026.)

**S-7 — REQ-002-022 requires two byte sequences, not one.** SPEC-002 §4.6: the canonical byte
sequence for the Artifact and for the Vector are *"SEPARATE definitions within their respective
hash domains and MUST NOT be treated as a single universal byte sequence"*. Nothing in the
repository defines either.

### 7.2 What must be decided — no format is chosen

| # | Decision question | Candidates supported by existing material |
|---|---|---|
| DQ-7.1 | Which single canonical serialization format governs? | JSON · CBOR · Protocol Buffers — **all three named in APS-200 §8, none endorsed** |
| DQ-7.2 | Field set and field ordering for the Artifact representation | none |
| DQ-7.3 | Field set and field ordering for the Vector representation | none |
| DQ-7.4 | Representation of absent / optional / null fields | none |
| DQ-7.5 | Integer encoding within the serialization (decimal string vs binary; width; signedness) | `signed int32` (SPEC-002 §6, non-normative) |
| DQ-7.6 | Unicode escaping and whitespace policy | none |
| DQ-7.7 | Which hash domains exist beyond Vector Hash and Artifact Hash (REQ-002-018 permits more) | none |
| DQ-7.8 | Domain-separation mechanism (prefix, tag, or other) | none — **no domain separation exists anywhere in either repository** |
| DQ-7.9 | Included vs excluded fields per hash domain (REQ-002-019) | none |
| DQ-7.10 | Whether a Constitution Artifact is an APS-200 entity at all — and therefore whether the Common Object Contract applies to it | none — depends on APS-001 §2 (§4.4) |

→ **DR-017** (format and byte sequence), **DR-018** (hash domains and separation).
DQ-7.10 is the pivot: if the answer is "yes", §9's provenance problem is inherited
automatically.

> **NO SERIALIZATION FORMAT IS CHOSEN BY THIS DOCUMENT.**

---

## 8. Identity Model

SPEC-002 §4.4 requires four identities to remain distinct, and separately requires that
Identity, Integrity, Provenance, Lineage and Status not be used as synonyms. Current state of
each:

### 8.1 Source identity (Constitution Document Identity)

| Aspect | Evidence | State |
|---|---|---|
| Identifier | `constitution/AURA_CONSTITUTION.md` front matter: `Document ID: AURA-CON-001` | exists |
| Version / Status | `Version: 1.0`, `Status: FROZEN` | exists |
| Repository location | **two repositories claim the name** (§2) | **UNRESOLVED** |
| Representation | three designators for one document: `AURA-CON-001` (ID), `constitution/AURA_CONSTITUTION.md` (path), `AURA Constitution_260723_190157.txt` (preserved original, referenced by the file's own footer). Not byte-identical. | **UNRESOLVED** |
| Alias hazard | REQ-002-009 forbids equating `AURA-CON-001` with `AURA-CONSTITUTION-001` without approval | requirement exists; no binding rule |

→ **DR-001, DR-010**

### 8.2 Artifact identity (Constitution Artifact Identity)

**Does not exist.** No field, no schema, no generation rule, no implementation. APS-200 §3
enumerates entities ENT-001…ENT-008; **none is a Constitution Artifact**. APS-900 §3's mapping
chain runs `APS Requirement → INV → ENT → Evidence Model → CONF → FIX → EVID → RI → REL` —
with **no artifact node and no vector node anywhere in it**.

### 8.3 Vector identity (Constitution Vector Identity)

**Does not exist.** Same evidence as §8.2. `PoCAEvaluator.__init__` accepts
`constitution_vector: List[int]` from the caller with no identity, no provenance, and no
validation beyond dimension (and, per §6.3, not even that at the similarity step).

### 8.4 Execution / commit provenance identity

**Does not exist.** No repository revision, build identity, or execution context is bound
anywhere in either implementation. APS-950 §6 requires builds be *"reproducible (same source →
same binary/artifact)"* and *"document all dependencies"*, but defines no provenance record.

### 8.5 The structural obstacle

> **CONFLICT DETECTED — CR-D**
>
> **Source A:** SPEC-002 §4.4 — Identity, Integrity, Provenance, Lineage and Status *"MUST NOT
> be used interchangeably"*; the future specification *"MUST define each concept independently
> and MUST NOT make them synonyms"*. REQ-002-015 prohibits collapsing the four identities.
> **Source B:** APS-200 §4 Common Object Contract gives every entity exactly **one**
> `object_id` and **one** `integrity_hash`. There is no artifact-vs-vector distinction, no
> provenance field, no lineage field, and **no `supersedes` field** — despite REQ-002-027
> requiring `supersedes` semantics.
> **Nature:** The canonical data model provides one identity slot where SPEC-002 requires four,
> and no substrate at all for lineage.
> **Impact:** REQ-002-015, 016, 023, 024 and 027 have no representation to bind to. AD-CA-009
> cannot be resolved inside SPEC-002 — it requires an **APS-200 extension**.

→ **DR-020**

---

## 9. Provenance Model

### 9.1 Current state

No provenance binding exists in either implementation. The specification requirement
(REQ-002-033) deliberately leaves the boundary open, listing three possibilities: provenance
*included in*, *excluded from*, or *externally bound to* the canonical artifact and its hash
domain(s).

### 9.2 The obstacle — provenance is already inside identity, by accident

> **CONFLICT DETECTED — CR-E — this is the single most consequential defect in the brief**
>
> **Source A:** `aps/APS-200_CANONICAL_DATA_MODEL.md` §4, Common Object Contract. Every entity
> MUST carry both:
>
> | Field | Type | Requirement | Description |
> |---|---|---|---|
> | `created_at` | string (ISO 8601) | MUST | Timestamp of object creation (UTC) |
> | `integrity_hash` | string | MUST | SHA-256 hash of the canonical serialization of this object |
>
> **Source B:** SPEC-002 §5.1 Positive Determinism Verification requires
> `same authoritative source → same Constitution Artifact → same canonical bytes → same hash values`.
> **Source C:** AURA Constitution Article IV P2 (FROZEN): *"Determinism by Design. All protocol
> behaviour is deterministic. Non-determinism is a defect."*
> **Nature:** If a Constitution Artifact is modelled as an APS-200 entity, its canonical
> serialization contains a wall-clock timestamp, so its `integrity_hash` **changes on every
> construction**. Same source, different hash.
> **Impact:** The CONTENT / IDENTITY / PROVENANCE conflation that SPEC-002 §4.4 exists to
> prevent is **already present in a DRAFT normative document upstream of SPEC-002**. AD-CA-009
> and AD-CA-010 cannot be resolved around it — APS-200 §4 must be corrected, or APS-001 §2 must
> establish that a Constitution Artifact is not an APS-200 entity.

### 9.3 Provenance factors — evidence only, no inference

SPEC-002 §4.7a requires the future specification to decide whether provenance may alter
canonical output. The following records **only what the evidence shows today**. It does not
propose what the answer should be.

| Factor | Does it change artifact/vector identity today? | Evidence | Should it? |
|---|---|---|---|
| Timestamp | **Yes** | APS-200 §4 `created_at` inside `integrity_hash` (CR-E) | **decision required** |
| Git commit / repository revision | **No** | bound nowhere in either implementation | **decision required** — REQ-002-025 requires binding, REQ-002-033 leaves the hash relationship open |
| Compiler | **Yes, potentially** | float summation reassociation / FMA unconstrained (§6.3) | **decision required** — INV-006 says it must not |
| OS | No evidence of effect | — | **decision required** |
| CPU architecture | **No** (verified) | `compare-determinism` CI compares x86_64 and ARM64 and passes | INV-006 already requires no effect |
| Python version | **Unbound** | no dependency manifest; AD-CA-006 (dependency closure) is **orphaned** | **decision required** |
| Rust version | **Unbound** | ditto; and RI-RS implements none of this surface | **decision required** |
| **Language** | **Yes — reproduced** | §6.1, §6.2 | INV-002 and INV-006 already require no effect — **the system's current behaviour is the opposite of its own invariant** |

→ **DR-019**

---

## 10. Registration vs Freeze

### 10.1 The existing lifecycle

Two documents define it identically.

`VERSIONING.md` §3:

```
DRAFT → REVIEW → APPROVED → FROZEN
                           ↘ DEPRECATED → ARCHIVED
```

| Status | Meaning | Mutable? |
|---|---|---|
| DRAFT | Under active authoring; may change freely | Yes |
| REVIEW | Under Architecture Review; changes require justification | With justification |
| APPROVED | Formally approved; changes require RFC + ADR | Via RFC/ADR only |
| FROZEN | Immutable; content cannot change | No |
| DEPRECATED | Superseded; retained for reference | No |
| ARCHIVED | No longer active; historical record only | No |

Transition rules (`VERSIONING.md` §3): `DRAFT → REVIEW` by author PR; `REVIEW → APPROVED` by
Chief Architect after Architecture Review; **`APPROVED → FROZEN` requires explicit freeze
decision by Chief Architect under Constitution Article XI**; `→ DEPRECATED` requires a
superseding document; `DEPRECATED → ARCHIVED` after minimum 2 major versions.

`GOV-001` §4 states the same chain. APS-000 §5 lists the same six statuses.

**There is no VERIFIED state and no REGISTERED state anywhere in the repository.**

### 10.2 The proposed lifecycle

Review scoping referenced:

```
DRAFT → VERIFIED → REGISTERED → APPROVED → FROZEN
```

This appears in **no repository document**. It is a proposal, not an existing artefact.
Adopting it would add two states to the universal lifecycle governing every artifact class.

> **This document does not change the lifecycle.** The two are recorded side by side; the
> difference is a decision, not a clarification. → **DR-022**

### 10.3 Registration — no substrate

REQ-002-028 requires *"the authoritative registry and its location"*. APS-000 §7 describes a
Canonical Registry covering documents, invariants, ADRs/ARRs/RFCs, evidence, conformance tests,
fixtures, releases and policies, with fields *Identifier, Version, Owner, Status, Related
Documents, Last Review*.

**Only `invariants/INVARIANT_REGISTRY.md` materially exists.** There is no artifact registry,
no vector registry, no document registry, and no location. AD-CA-011 must therefore **create**
the registry, not describe it. → **DR-021**

### 10.4 Freeze — conferred authority vs self-assertion

> **CONFLICT DETECTED — CR-F**
>
> **Source A:** `VERSIONING.md` §3 — `APPROVED → FROZEN` requires *"Explicit freeze decision by
> Chief Architect; requires Amendment Procedure (Constitution Article XI)"*. Constitution
> Article XI: *"Once a version is marked FROZEN, its content is immutable."*
> **Source B:** This repository declares itself frozen in at least three places:
> `CONSTITUTIONAL_DECREE.md` Article VIII ("v3.3 — Frozen Iron Core");
> `docs/architecture.md` footer (*"**Status**: FROZEN — MC-READY 2026"*);
> `docs/specs/AUDIT_LAYER_SPEC.md` (described in `docs/GAP-001.md` as a *"normative frozen
> spec"*).
> **Source C:** `reference/RI-PY_AURA_POC_A_CORE.md` records the conflict itself —
> *"Self-declared FROZEN (v3.3) — this creates a governance challenge as APS gaps require
> changes"* — alongside `APS-950 Certification Status: **NOT CERTIFIED**`.
> **Nature:** An implementation has assigned itself a governance status that `VERSIONING.md`
> reserves to the Chief Architect. "FROZEN" now denotes two different things: a state conferred
> by authority, and a self-description adopted by an artifact.
> **Impact:** REQ-002-029 requires *"the authority who may authorize freeze"* and *"the
> verification procedure for confirming frozen status"*. Neither is specifiable while the word
> carries two meanings. It also produces a **deadlock**: a self-frozen, NOT CERTIFIED
> implementation cannot be corrected to meet the future contract without breaking its own
> freeze claim.

Note that `CONSTITUTIONAL_DECREE.md` Article VIII already anticipates the resolution shape —
*"Any change to core logic creates a NEW INSTRUMENT, not a new version"* — but whether that
governs, and what it implies for SPEC-002 conformance of v3.3, is not recorded. → **DR-023**

### 10.5 REGISTERED ≠ APPROVED ≠ FROZEN

SPEC-002 §8 states the separation correctly. But with no registry (§10.3), no VERIFIED or
REGISTERED states (§10.2), and no enumeration of invalid transitions for any artifact class,
**none of the three separations can currently be verified by any test.** The requirement is
sound; the substrate is absent.

---

## 11. Constitution Artifact — what exists and what does not

### 11.1 What exists

| Item | Location | Nature |
|---|---|---|
| The Constitution **document** | `constitution/AURA_CONSTITUTION.md`, AURA-CON-001 v1.0 FROZEN | The only FROZEN normative document in the specification repository |
| A contract **specification** for a future artifact | `specification/SPEC-002_…md` v0.3-DRAFT | 34 requirements, explicitly non-normative until approved |
| An int32 vector **consumer** | `core/evaluator.py` `PoCAEvaluator` | Accepts `constitution_vector: List[int]` from the caller |
| An offline float→int32 **normalizer** | `core/offline_normalizer.py` | Operates on arbitrary caller-supplied floats |
| A **placeholder** text→vector function | `core/embedding.py` | Docstring line 3: *"Placeholder for deterministic embedding in ℝ¹⁵³⁶ space. MUST be frozen + reproducible in production."* |

### 11.2 What does not exist

| Item | Verification |
|---|---|
| **Any code path that reads `AURA_CONSTITUTION.md`** | Directed search across both repositories: **no matches** |
| A Constitution Artifact | no schema, no entity, no file, no generator |
| A Constitution Vector derived from the Constitution | `generate_sample_constitution` builds from `[0.5 + 0.1 * (i % 10) for i in range(dimension)]` — a synthetic ramp, unrelated to any protocol source. Its docstring says "for testing/demo purposes", accurately. |
| Artifact identity / vector identity / provenance identity | §8.2–8.4 |
| An artifact or vector registry | §10.3 |
| A freeze mechanism for artifacts | §10.4 |
| Any Constitution Artifact code in RI-RS | Repository-wide search of `aura-guard-v1.3/src/` for `constitution`, `vector`, `ARI`: **no matches**. RI-RS is a PII/prompt guard with a hash-chained evidence log. |
| Any usable fixture | `fixtures/core/FIX-001_BASIC_EVALUATION.json` — every data field is the literal string `"TODO"`; APS-500 §5 is a TODO |
| Any conformance test covering this surface | CONF-001…010 are all scoped to the evaluation/evidence path. Coverage of the Constitution Artifact surface: **0 of 10** |

### 11.3 Statement of fact

**The term "Constitution Vector" in `aura-poc-a-core-v3.3` denotes a caller-supplied int32
array of unknown origin.** It is not derived from the Constitution, not bound to it, and not
identified. This is not a criticism — the repository describes itself as a research prototype
and `docs/GAP-001.md` documents its gaps candidly — but it means **the estate contains no
starting point for the SPEC-002 contract**, and any traceability claim implying otherwise is
unfounded.

> **This document does not implement the artifact.**

---

## 12. Independent Implementation

### 12.1 Why current tests cannot prove independent conformance

**R-1 — There is no second implementation.** APS-950 §11 lists two Reference Implementations:
RI-PY (`aura-poc-a-core-v3.3`) and RI-RS (`aura-guard-v1.3`). RI-PY implements a *placeholder*
projection and no artifact surface (§11). RI-RS implements **none** of the surface. There is
therefore **no second party** to compare against.

**R-2 — CONF-003 tests self-consistency, not interoperability.** Its §4 procedure —
*"Serialize ENT-001 through ENT-008 objects twice independently (fresh process each time)"* —
compares one implementation with itself. A single implementation is trivially self-consistent
in its rounding, division and serialization choices, so this test **passes precisely when the
divergences in §6 are present**.

**R-3 — CONF-006 is same-language.** Its PASS criterion is *"Same Evidence Pack produced on x86
and ARM platforms"*. The existing `compare-determinism` CI job implements exactly this and is
genuine evidence of cross-*architecture* determinism — but it runs **Python on both sides**, so
it is blind to every divergence in §6, all of which are cross-*language*.

**R-4 — There are no fixtures.** INV-014 (Reference Compatibility) requires passing all
applicable Reference Fixtures; `FIX-001` is a placeholder of `"TODO"` strings, and INV-014 has
**no assigned conformance test** (a self-reported INV-010 violation in
`invariants/INVARIANT_REGISTRY.md` §"Missing Conformance Tests").

**R-5 — The specification is not yet sufficient to implement from.** SPEC-002 §11 states this
directly. The numeric semantics of §6 are recoverable **only** by reading
`core/evaluator.py` and `core/offline_normalizer.py` — which SPEC-002 §10 explicitly forbids an
independent implementer from doing.

**Consequence.** The success criterion is not failing. It is **unfalsifiable**: there exists no
experiment, in the current estate, whose outcome could distinguish conformance from
non-conformance. That is a worse position than a failing test, because no CI signal can ever
report it.

### 12.2 Evidence required for a future independent implementation

Necessary conditions, each traced to an existing requirement. **None is a proposal about
scope; each is a restatement of what SPEC-002 §9/§10 already demands.**

| # | Required evidence | Serves | Precondition |
|---|---|---|---|
| IE-1 | A specification sufficient to implement from without reading any RI | SPEC-002 §10 | All 12 AD-CA domains resolved |
| IE-2 | Canonicalization fixtures: input bytes → expected canonical bytes | REQ-002-006, 007, 011 | AD-CA-002, **AD-CA-004 (orphaned)** |
| IE-3 | Artifact fixtures: canonical source → expected artifact bytes | REQ-002-010, 021 | AD-CA-003, AD-CA-008 |
| IE-4 | Vector golden vectors, full component listing | REQ-002-012, 024 | AD-CA-003/005/**006 (orphaned)** |
| IE-5 | Numeric boundary fixtures — **must include negative-operand division and exact-`.5` ties**, with expected values stated for at least two languages | REQ-002-014 | AD-CA-007 |
| IE-6 | Serialization fixtures compared **across two implementations**, not within one | REQ-002-021, 022 | AD-CA-008; supersedes CONF-003's design |
| IE-7 | Hash golden vectors recording **pre-image bytes**, not only digests | REQ-002-017–020 | AD-CA-008; APS-200 §4 and APS-300 §5 corrected |
| IE-8 | Identity binding tests, including detection of identity collapse | REQ-002-015, 016 | AD-CA-009; APS-200 extension |
| IE-9 | Provenance tests covering each factor in §9.3 | REQ-002-025, 033 | AD-CA-010 |
| IE-10 | Lifecycle tests including **invalid** transitions | REQ-002-028, 029 | AD-CA-011, 012; a registry must exist |
| IE-11 | Negative tests — one per REQ-002-031 condition, plus dimension mismatch and over-length input | REQ-002-031 | all |
| IE-12 | Cross-platform replay: x86_64 · ARM64 · (WASM), ≥2 OSes | REQ-002-030 | AD-CA-007, 008 |
| **IE-13** | **Cross-language replay: ≥2 languages, implemented independently, authors having not read RI-PY** | **REQ-002-030, 032; §10 Independent Implementer Test** | **all of the above** |

**IE-13 is the criterion.** It has the longest lead time of anything in this brief and no
second party today. → **DR-025**

---

## 13. CR-007

### 13.1 Record of state

**CR-007 is undefined.**

| Source | What it says | What it does not say |
|---|---|---|
| SPEC-002 §2.2 Non-Goals | *"This document MUST NOT: … Implement CR-007"* | what CR-007 is |
| SPEC-002 §11 | *"CR-007 remains BLOCKED"* | what CR-007 is |
| SPEC-002 Appendix A(B) | *"CR-007 remains BLOCKED. No requirement in SPEC-002 constitutes approval or unblocking of CR-007."* | what CR-007 is |
| Review scoping | *"CR-007 ma być verifierem, a nie mechanizmem tworzącym normatywną tożsamość"* | a definition — this is a **constraint on the answer**, not the answer |

Repository-wide search across both repositories: this repository defines **CR-001** (Art. 5
runtime conformance proof), **CR-003** (Layer 0 statelessness / layer boundary) and **CR-004**
(append-only evidence hardening) — implemented in `scripts/checks/` and `core/`. There is **no
CR-002, CR-005, CR-006 or CR-007**. The specification repository contains no `CR-` series at
all, and `CR` is not in the APS-000 Appendix A canonical prefix registry.

> **This document does not infer CR-007's semantics.** Doing so would manufacture normative
> content, which is out of scope for this role per `CLAUDE.md`.

### 13.2 What must be specified before CR-007 can become an implementation target

| # | Required specification | Currently |
|---|---|---|
| 1 | What CR-007 **is**: a conformance requirement, a check script, a verifier component, or a governance gate | undefined |
| 2 | Its **inputs**: which artifacts, in which state, from which registry | undefined — no registry exists (§10.3) |
| 3 | Its **outputs**: pass/fail, a report, an evidence artifact, or a status transition | undefined |
| 4 | Its **authority**: whether its output *confers* any status, or only *reports* on one | constrained ("verifier, not identity-creating") but not specified |
| 5 | Its **pass/fail criteria** | undefined |
| 6 | Its relationship to the **CONF-xxx** series — whether CR- and CONF- are parallel namespaces or CR-007 belongs in CONF | undefined; note APS-000 registers `CONF` but not `CR` |
| 7 | Its position in the **lifecycle** — which transition, if any, it gates | undefined; depends on DR-022 |
| 8 | Whether the `CR` **prefix** is registered under APS-000 §3 | not registered |

→ **DR-024**. Candidate alternatives supported by existing material: **CR-001/003/004 exist as
executable check scripts with `scripts/checks/check_N_*.sh` + a Python/AST or runtime test**,
which establishes a *precedent shape* for what a `CR-` is in this repository. Whether CR-007
should follow that precedent is a decision.

---

## 14. Decision Register

**Format per required section 14.** Where the repository supplies no candidate, the entry reads
**"Decision required — no candidate supported by existing material"** rather than importing one.
Recommendations appear only on clerical items and are marked.

---

### DR-001 — Authoritative repository
**Question.** Which of `AuraIDToken/aura-specification` and `aura-nomos/aura-specification` is
authoritative, and what is the other's recorded status?
**Why it matters.** REQ-002-003 requires repository location as part of Source Document
Identity. AD-CA-001 is unresolvable while two locations claim one name.
**Evidence.** §2.1–2.2. Populated repo `62d2d6b`; stub repo `eb2a4ec` (11-byte README +
CODEOWNERS mirroring the other's layout); no supersession record in either; push to the stub
denied HTTP 403.
**Blocking impact.** AD-CA-001 → REQ-002-001…011 → ADR-002 → all downstream.
**Required authority.** Custodian / Chief Architect (role undetermined — DR-002).
**Candidates.** Neither repository is favoured by repository evidence. **Decision required.**

---

### DR-002 — Role identity and decision authority
**Question.** Are "Chief Architect" and "Protocol Custodian" the same office? If distinct, which
holds authority over each artifact class? Are "Architecture Review Board" (GOV-001) and
"Architecture Board" (`ADR-001_DOCUMENT_MODEL`) the same body? Do "Release Authority" and
"Compliance Authority" exist?
**Why it matters.** Every "decision authority" cell in §5 depends on it. GOV-001 §5.2 requires
an "Architecture Review Board assessment"; if no such body is constituted, that step cannot be
executed. A decision-ready brief cannot be routed to an undefined addressee.
**Evidence.** §3.3 CR-C. Constitution Article VIII and GOV-001 §2 name only Chief Architect.
SPEC-002 header, `ADR-001_DOCUMENT_MODEL` and `arc/README.md` name only Protocol Custodian.
`templates/SPEC_TEMPLATE.md` line 9 offers both as alternatives without equating them. This
repository's `CONSTITUTIONAL_DECREE.md` Article V says *"Custodian of the Protocol (Architect)"*
and `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` derives its powers from that decree, not the AURA
Constitution.
**Blocking impact.** **All 27 decisions in this register.**
**Required authority.** Constitutional — the Constitution names the office.
**Candidates.** **Decision required — no candidate supported by existing material.** The
`(Architect)` parenthetical in this repository's decree is the closest thing to an equation, but
it appears in an implementation repository and does not bind the AURA Constitution.

---

### DR-003 — Document authority model
**Question.** Is Constitution Article V in force, or the ARC/SPEC/APS model of
`ADR-001_DOCUMENT_MODEL`?
**Why it matters.** The `SPEC-` class exists only in the latter. SPEC-002's position in the
canonical hierarchy depends entirely on this.
**Evidence.** §3.1–3.2 CR-B. Article V is FROZEN; `ADR-001_DOCUMENT_MODEL` is PROPOSED and
declares eight `INV-DOC-*` invariants absent from APS-100 and the registry.
**Blocking impact.** ADR-002…006 cannot be placed in the hierarchy. `INV-DOC-002`
(every SPEC references ≥1 ARC) is unsatisfiable — `/arc` is empty, mapping is `[]`, SPEC-001
does not exist.
**Required authority.** Constitutional. Adopting Model B requires Article XI amendment.
**Candidates.** Model A (Constitution Article V, FROZEN) · Model B (`ADR-001_DOCUMENT_MODEL`,
PROPOSED). Both are in the repository. **No recommendation — architecture must decide.** The
evidence establishes only that "both live, neither adjudicated" is not a viable third option.

---

### DR-004 — `ADR-001` identifier collision
**Question.** Which document is ADR-001? What becomes of the other two?
**Why it matters.** GOVERNANCE.md §6 step 2 and `adrs/README.md` step 2 require "the next
sequential ADR-NNN". With ADR-001 ambiguous, "next" is undefined and ADR-002 cannot be safely
numbered.
**Evidence.** Three documents claim `ADR-001`: `adrs/ADR-001_REPOSITORY_STRUCTURE.md`
(ACCEPTED, indexed), `adrs/ADR-001_DOCUMENT_MODEL.md` (PROPOSED, not indexed),
`docs/adr/001-document-model.md` (DRAFT, not indexed). The latter two are divergent copies —
differing in status, front matter, and body (the `docs/` copy adds a "Merge Blockers" checklist
and a `doc/ci/glossary-check` job). Violates APS-000 §4, VERSIONING.md §8, and `INV-DOC-005`
declared by the colliding document itself.
**Blocking impact.** All ADR numbering.
**Required authority.** Custodian / Chief Architect (DR-002).
**Candidates.** Repository material supports retaining `ADR-001_REPOSITORY_STRUCTURE` as
ADR-001 (it is ACCEPTED and indexed; the others are not). **[RECOMMENDATION — non-binding]**
The clerical component — that the two unindexed copies must not both persist under the same
identifier — follows from APS-000 §4 regardless of which is retained. **Which** document keeps
the identifier, and what number the Document Model receives, remains a decision.

---

### DR-005 — ADR acceptance bar
**Question.** Do AD-CA-class ADRs follow GOV-001 §5.2 (RFC → 14-day comment → ARB → Chief
Architect) or §6 (PR merge = ACCEPTED, one reviewer)?
**Why it matters.** Under §6, an ADR fixing canonical bytes could be accepted by a single merge.
**Evidence.** GOV-001 §5.2 classifies "new requirements, new invariants, new conformance tests,
behavioral changes" as Major Changes requiring RFC. §6 states *"Merging the PR = accepting the
ADR"*. Every AD-CA domain is a Major Change by §5.2's own test. GOV-001 is itself `1.0-DRAFT`.
**Blocking impact.** Whether ADR-002…006 require RFCs.
**Required authority.** Custodian / Chief Architect; amending GOV-001 is itself a Major Change.
**Candidates.** §5.2 path · §6 path — both in GOV-001. **No recommendation — architecture must
decide**, since the choice determines the governance weight of every canonical-bytes decision.

---

### DR-006 — APS-001 minimum scope
**Question.** Must APS-001 be complete before SPEC-002 v0.4, or does a bounded subset
(§2, §7, §8, §9) suffice?
**Why it matters.** APS-001 is the root of the entire normative chain and currently has Status
TODO with no content.
**Evidence.** §4.1–4.4.
**Blocking impact.** REQ-002-010, 017, 018, 021, 022, 030, 031 depend on named APS-001 sections.
**Required authority.** Custodian / Chief Architect.
**Candidates.** **Decision required — no candidate supported by existing material.**
`ROADMAP.md` Milestone 1 is cited by APS-001 but specifies no scope split.

---

### DR-007 — Ownership of AD-CA-004 and AD-CA-006
**Question.** Which governance artifact resolves each?
**Why it matters.** AD-CA-004 blocks REQ-002-021/022 — the requirements ADR-004 exists to close
— so **ADR-004 cannot close its own scope**. AD-CA-006 blocks REQ-002-034, leaving "same source
→ same vector" unprovable.
**Evidence.** §5 F-1. Both verified UNRESOLVED in SPEC-002 §6 and Appendix A(E); neither appears
in the five-ADR grouping.
**Blocking impact.** Coherence of the entire ADR package.
**Required authority.** Custodian / Chief Architect.
**Candidates.** Repository material supports no particular assignment. **Decision required.**
The only constraint the evidence imposes is that **every domain must be owned before any ADR in
the set is accepted**, since SPEC-002 §9 criterion 1 requires every requirement to be backed by
an approved source or decision.

---

### DR-008 — AD-CA-005 scope
**Question.** Does AD-CA-005 cover embedding method identity/versioning, the projection
mechanism, or both?
**Why it matters.** Authoring ADR-003 to the wrong reading silently redefines a decision domain
and orphans REQ-002-012.
**Evidence.** §5 F-2. SPEC-002 §6 row 5 verbatim: *"Embedding method identity and versioning
model"*. SPEC-002 never uses "projection".
**Blocking impact.** ADR-003 scope.
**Required authority.** Custodian / Chief Architect.
**Candidates.** SPEC-002 §6 wording (in repository) · "projection mechanism" (review scoping
only, **not in repository**). **Decision required.** Note that adopting the second without a
recorded decision would breach the standing rule against silently reinterpreting protocol
semantics (`AGENTS.md` rule 2).

---

### DR-009 — Admissible source document statuses
**Question.** Which lifecycle statuses (REQ-002-005) may enter the Source Set?
**Why it matters.** Exactly one document is FROZEN. If "FROZEN only", the Source Set is the
Constitution alone. If DRAFT is admissible, the source is mutable and the artifact is not
reproducible over time.
**Evidence.** FROZEN: `AURA_CONSTITUTION.md` only. DRAFT: all APS documents, GOV-001,
VERSIONING, invariant registry, all CONF, SPEC-002. TODO: APS-001. `VERSIONING.md` §3 marks
DRAFT *"may change freely"*.
**Blocking impact.** AD-CA-001.
**Required authority.** Custodian / Chief Architect.
**Candidates.** The six statuses in `VERSIONING.md` §3 / APS-000 §5 are the supported set. Which
subset is admissible is a **decision required**.

---

### DR-010 — Authoritative source representation
**Question.** Where multiple stored representations of one document exist, which is
authoritative?
**Why it matters.** A source boundary naming a *document* but not a *representation* does not
determine a byte sequence, hence cannot determine a hash.
**Evidence.** Every APS document carries a footer *"Source: Original text preserved in
`<name>_260723_NNNNNN.txt`"*; `.txt` and `.pdf` originals sit at repository root beside the
`.md` renderings; they are not byte-identical. `ADR-001_REPOSITORY_STRUCTURE` Consequences notes
*"Original source files (PDF + TXT) are preserved in the repository root for provenance"* and
*"Existing APS source content is re-expressed as canonical Markdown in `/aps/`"* — describing
both as canonical-adjacent without adjudicating.
**Blocking impact.** AD-CA-001, AD-CA-002.
**Required authority.** Custodian / Chief Architect.
**Candidates.** `.md` rendering · preserved `.txt` · `.pdf`. All three are in the repository;
`ADR-001_REPOSITORY_STRUCTURE` supports the `.md` as "canonical Markdown" while the footers
support the `.txt` as "original". **Decision required.**

---

### DR-011 — Canonicalization: lossy or lossless
**Question.** Is Constitution-source canonicalization lossless byte-level normalization, or a
lossy pipeline of the SHADOW_SPEC kind, or something else?
**Why it matters.** The two reference implementations already disagree, and one declares its own
frozen normalization spec outside the APS/SPEC hierarchy.
**Evidence.** `aura-guard-v1.3/src/normalizer.rs` implements "SHADOW_SPEC v1.0": strict ordered
pipeline — UTF-8 validation → NFKC → strip 21 enumerated hidden characters → confusable folding
(Cyrillic/Greek/fullwidth) → ASCII lowercase — documented *"any deviation invalidates the shadow
hash"*, and explicitly *"intended **only** for regex matching. The original `input` should be
retained verbatim for the SHA-256 evidence hash."* `aura-poc-a-core-v3.3` has **no**
canonicalization stage; `embed_text` consumes a raw `str`.
**Blocking impact.** AD-CA-002, evidence item IE-2.
**Required authority.** Custodian / Chief Architect.
**Candidates.** SHADOW_SPEC v1.0 (exists in repository, but its own docstring scopes it to
regex matching and reserves the verbatim text for hashing) · no canonicalization (RI-PY's
current state) · a new pipeline. **Decision required.**

---

### DR-012 — Vector dimension, and the meaning of `32`
**Question.** What is the Constitution Vector dimension, and does the token `32` in SPEC-002 §6
denote dimension or integer width?
**Why it matters.** Cardinality determines canonical byte length and byte positions. Under
either reading, **dimension is currently owned by no AD-CA row**: if `32` means dimension it
contradicts every implementation; if it means width it is redundant with `signed int32` and
dimension is simply absent from the decision set.
**Evidence.** SPEC-002 §6 AD-CA-007 candidates: `32`, `100000`, `signed int32`, `little-endian`,
`round-half-to-even`. `core/embedding.py` and `core/offline_normalizer.py`
(`CONSTITUTION_DIM = 1536`, enforced by `ValueError`) hard-code 1536; `docs/architecture.md` and
`docs/mathematical_foundation.md` describe 1536-dimensional space.
**Blocking impact.** AD-CA-003, AD-CA-007, IE-4.
**Required authority.** Custodian / Chief Architect.
**Candidates.** `32` (SPEC-002 §6, non-normative, ambiguous) · `1536`
(**implementation-derived — inadmissible as authority per SPEC-002 §"Governing Direction"**).
**Decision required.**

---

### DR-013 — Integer division semantics
**Question.** For integer division in the canonical pipeline, what is the rounding direction for
negative operands?
**Why it matters.** Languages disagree by default; the implementation has adopted one by
accident; INV-002 and INV-006 (both Critical) are defeated where it is reached.
**Evidence.** §6.1, reproduced.
**Blocking impact.** AD-CA-007, IE-5.
**Required authority.** Custodian / Chief Architect.
**Candidates.** **Decision required — no candidate supported by existing material.** No document
in either repository addresses integer division. Python's floor behaviour is
implementation-derived and inadmissible as authority.

---

### DR-014 — Float→fixed rounding and the float boundary
**Question.** What is the rounding mode at the float→fixed boundary including tie behaviour? Is
any float stage inside the reproducibility contract, and if so what constrains summation order,
reassociation and FMA?
**Why it matters.** This is the Constitution Vector construction path. SPEC-002 §3.4 forbids
treating a candidate as a default, and the implementation has done exactly that.
**Evidence.** §6.2, reproduced. §6.3 float summation row.
**Blocking impact.** AD-CA-007, IE-4, IE-5.
**Required authority.** Custodian / Chief Architect.
**Candidates.** `round-half-to-even` (SPEC-002 §6 — **explicitly non-normative, explicitly not a
default**). `CONSTITUTIONAL_DECREE.md` Article VII bounds float to `offline_normalizer.py` by
*location* but says nothing about *semantics*. **Decision required.**

---

### DR-015 — Numeric widths, overflow, endianness, tolerance
**Question.** Integer widths at each stage; overflow behaviour (wrap/saturate/reject); NaN and
±Infinity handling; negative zero; byte order; and whether tolerance-based validation may
establish canonical identity.
**Why it matters.** Each is a degree of freedom permitting two conformant implementations to
diverge — the condition REQ-002-032 defines as NOT READY.
**Evidence.** §6.3 table.
**Blocking impact.** AD-CA-007, AD-CA-008, IE-5.
**Required authority.** Custodian / Chief Architect.
**Candidates.** `signed int32`, `little-endian`, `100000` (SPEC-002 §6, all non-normative).
Nothing addresses accumulator width, NaN, or negative zero. **Decision required.**

---

### DR-016 — Input-length domain
**Question.** What is the admissible input-length domain, and what is the behaviour for empty,
minimum, maximum, under-dimension and over-dimension input?
**Why it matters.** The current transform **silently truncates** input over 1536 characters; the
Constitution is ~6,500 characters, so on the most plausible real input the majority of the
source is discarded without signal. Silent truncation is a fallback that alters the canonical
result, which REQ-002-031 prohibits.
**Evidence.** §6.3. Also: the two modules disagree on the empty case — `embed_text("")` returns
a zero vector while `normalize_vector` raises `ValueError("Cannot normalize zero vector")`.
**Blocking impact.** AD-CA-003, IE-4, IE-11.
**Required authority.** Custodian / Chief Architect.
**Candidates.** **Decision required — no candidate supported by existing material.**

---

### DR-017 — Canonical serialization format and byte sequences
**Question.** Which single format governs? What are the field sets, orderings, absent-field
representation, integer encoding, and escaping policy for the Artifact and — separately — the
Vector?
**Why it matters.** Three permitted formats produce three byte sequences for one artifact; the
hash is defined in terms of the undefined.
**Evidence.** §7.1 S-1…S-7.
**Blocking impact.** AD-CA-008 (with AD-CA-004), REQ-002-021/022, IE-3, IE-6, IE-7.
**Required authority.** Custodian / Chief Architect; APS-200 §8 is a Major Change under GOV-001
§5.2.
**Candidates.** JSON · CBOR · Protocol Buffers — **all three named in APS-200 §8, none
endorsed.** **No recommendation — architecture must decide.**

---

### DR-018 — Hash domains and domain separation
**Question.** Which hash domains exist; what is the exact pre-image of each; what fields are
included and excluded; what is the domain-separation mechanism?
**Why it matters.** REQ-002-020 requires an independent implementer reproduce the exact byte
sequence fed to each hash **without inspecting any Reference Implementation**.
**Evidence.** §7.1 S-2, S-3, S-7. **No domain separation exists anywhere in either
repository.** REQ-002-018 permits more than two domains.
**Blocking impact.** AD-CA-008, IE-7.
**Required authority.** Custodian / Chief Architect.
**Candidates.** SHA-256 is used throughout APS-200/APS-300 and `audit/merkle.py`, but APS-001 §7
("Which hash algorithm is canonical?") is TODO, so **the algorithm itself is formally
undecided.** **Decision required.**

---

### DR-019 — Provenance boundary and APS-200 §4 correction
**Question.** Is execution/commit provenance included in, excluded from, or externally bound to
the canonical artifact and its hash domain(s)? And: must APS-200 §4 be corrected so a
deterministic artifact is not obliged to carry a wall-clock timestamp inside its integrity hash?
**Why it matters.** The conflation SPEC-002 §4.4 exists to prevent is already present upstream.
**Evidence.** §9.2 CR-E; §9.3 factor table.
**Blocking impact.** AD-CA-009, AD-CA-010, IE-7, IE-8, IE-9.
**Required authority.** Custodian / Chief Architect; APS-200 amendment is a Major Change.
**Candidates.** REQ-002-033 itself enumerates three: *included in* · *excluded from* ·
*externally bound to*. **No recommendation — architecture must decide.** The evidence
establishes only that the current de-facto state (provenance inside the integrity hash via
`created_at`) contradicts Constitution Article IV P2 and SPEC-002 §5.1.

---

### DR-020 — Identity schema and APS-200 extension
**Question.** What are the field names, formats and generation rules for `document_id`,
`document_version`, `artifact_id`, `vector_id`, `provenance_id`? Which are content-derived and
which assigned? What binds them (REQ-002-016)? What carries `supersedes` (REQ-002-027)?
**Why it matters.** APS-200 §4 provides one identity slot where SPEC-002 §4.4 requires four, and
no lineage substrate at all.
**Evidence.** §8.5 CR-D. APS-900 §3's mapping chain contains no artifact or vector node.
**Blocking impact.** AD-CA-009, IE-8.
**Required authority.** Custodian / Chief Architect; requires an APS-200 extension.
**Candidates.** **Decision required — no candidate supported by existing material.**

---

### DR-021 — The registry
**Question.** Does the Canonical Registry described in APS-000 §7 get created? Where does it
live, what are its fields, and what integrity/identity/provenance checks run at registration?
**Why it matters.** REQ-002-028 requires *"the authoritative registry and its location"*.
AD-CA-011 must **create** it, not describe it.
**Evidence.** §10.3. Only `invariants/INVARIANT_REGISTRY.md` materially exists.
**Blocking impact.** AD-CA-011, IE-10.
**Required authority.** Custodian / Chief Architect.
**Candidates.** APS-000 §7 supplies a field set (*Identifier, Version, Owner, Status, Related
Documents, Last Review*) and a scope list; it supplies no location and no checks. Partial
material only — **decision required** for the rest.

---

### DR-022 — VERIFIED and REGISTERED lifecycle states
**Question.** Are two new states added to the universal lifecycle, or is registration modelled
as an attribute orthogonal to status?
**Why it matters.** The proposed lifecycle does not exist in the repository. Adding states
changes `VERSIONING.md`, GOV-001 and APS-000 §5 for **every** artifact class.
**Evidence.** §10.1–10.2. `VERSIONING.md` §3, GOV-001 §4 and APS-000 §5 all define the same
six-status model with no VERIFIED and no REGISTERED.
**Blocking impact.** AD-CA-011, AD-CA-012, IE-10.
**Required authority.** Custodian / Chief Architect; RFC required (Major Change).
**Candidates.** Existing 6-state model (in repository) · proposed 5-state chain (**not in
repository**). **No recommendation — architecture must decide.** Note only that SPEC-002 §8
requires registration and freeze be *independent*, which bears on whether they belong on the
same axis.

---

### DR-023 — Freeze authority and the self-freeze deadlock
**Question.** Is FROZEN conferrable only by named authority? What is the status of an
implementation that has declared itself frozen? Can v3.3 ever become SPEC-002 conformant?
**Why it matters.** REQ-002-029 requires a freeze authority and a verification procedure;
neither is specifiable while "frozen" carries two meanings.
**Evidence.** §10.4 CR-F.
**Blocking impact.** AD-CA-012, IE-10.
**Required authority.** Custodian / Chief Architect; coordination with this repository's
Custodian.
**Candidates.** `CONSTITUTIONAL_DECREE.md` Article VIII supplies material bearing on the
deadlock — *"Any change to core logic creates a NEW INSTRUMENT, not a new version"*, with the
v3.2/v3.3/v4.x lineage table. Whether that governs the SPEC-002 corrections is a
**decision required**.

---

### DR-024 — CR-007
**Question.** What is CR-007? See §13.2 for the eight items requiring specification.
**Why it matters.** ADR-006 must state CR-007's role in registration and freeze; it cannot do so
without inventing it.
**Evidence.** §13.1.
**Blocking impact.** AD-CA-011, AD-CA-012, ADR-006.
**Required authority.** Custodian / Chief Architect.
**Candidates.** CR-001/003/004 exist in this repository as executable check scripts
(`scripts/checks/check_N_*.sh` plus a runtime or AST test), establishing a **precedent shape**
for the `CR-` series. Whether CR-007 follows it is a **decision required**. The `CR` prefix is
not registered under APS-000 §3.

---

### DR-025 — Independent implementation
**Question.** Is a second implementation commissioned? In which language, by whom, under what
isolation condition (author must not have read RI-PY)?
**Why it matters.** IE-13 is the criterion for the entire stage, and it has no second party.
The success condition is currently unfalsifiable.
**Evidence.** §12.1 R-1…R-5; §11.2.
**Blocking impact.** SPEC-002 §9 criterion 7, §10 Independent Implementer Test, REQ-002-032.
**Required authority.** Custodian / Chief Architect — resourcing decision.
**Candidates.** APS-950 §11 lists `RI-TEST — Reference Fixtures Runner — TBD — Planned`, which is
the only existing material bearing on a third implementation. **Decision required.**
**Longest lead time in this register.**

---

### DR-026 — Cross-repository APS identifier collision
**Question.** Is `docs/GAP-001.md`'s APS coverage matrix withdrawn, or re-mapped to the real APS
identifiers?
**Why it matters.** Every cross-repository conformance claim is ambiguous between two different
specifications.
**Evidence.** Specification repository: APS-200 = Canonical Data Model, APS-400 = Conformance
Test Matrix, APS-500 = Reference Fixtures, APS-900 = Compliance Mapping. `docs/GAP-001.md` §3:
APS-200 = ARI Engine, APS-400 = Serialization, APS-500 = ZK Layer, APS-900 = Conformance Runner.
GAP-001 §3 states the cause: *"Requirements are inferred from the repository's own
documentation, the custom directive, and ADR-005, as the external `aura-specification`
repository is not co-located here."* Violates APS-000 §4 and `AGENTS.md` rule 7.
**Blocking impact.** All cross-repository traceability; §7 of this brief; the authority of
`07_IMPLEMENTATION_CONFORMANCE.md`.
**Required authority.** This repository's Custodian.
**Candidates.** Withdraw · re-map. Note the evidence bears on the choice: GAP-001 states its
requirements were **inferred rather than read**, so the underlying assessments are unverified,
not merely mislabelled. **Decision required.**

---

### DR-027 — ADP-001
**Question.** Is ADP-001 created as a standalone protocol document, or is the projection defined
inside AD-CA-003?
**Why it matters.** ADR-003 is proposed to rest on it; a specification resting on a name cannot
be independently implemented.
**Evidence.** No document, identifier or definition exists in either repository. `ADP` is not in
the APS-000 Appendix A prefix registry. Against the fourteen definitions required by SPEC-002's
determinism contract (input, output, dimension, indexing, byte ordering, arithmetic, rounding,
overflow, invalid input, empty input, maximum input, determinism, domain separation, test
vectors), ADP-001 is **0/14 defined**.
**Blocking impact.** ADR-003, AD-CA-003, IE-4.
**Required authority.** Custodian / Chief Architect; RFC required either way (new protocol
behaviour under GOV-001 §5.2).
**Candidates.** **Decision required — no candidate supported by existing material.**

---

## 15. Proposed Execution Order

Ordered by **dependency**, not convenience. Each wave is unblocked only by the waves above it.
**"Proposed" is literal — the ordering is derived from the dependency evidence in §5, §14 and
`review/.../04_EVIDENCE_PLAN.md` §2, and is not itself a decision.**

### Wave 0 — Prerequisites to deciding anything

| Order | Decision | Rationale |
|---|---|---|
| 1 | **DR-002** role identity / decision authority | Every other decision needs a defined decider. Blocks all 26 remaining. |
| 2 | **DR-001** authoritative repository | AD-CA-001 is unresolvable without it; also determines where decisions are recorded. |
| 3 | **DR-003** document authority model | Determines whether SPEC-002 has a position in the hierarchy at all. |

> **Start DR-025 (commission an independent implementation) in parallel with Wave 0.** It
> appears in Wave 5 by dependency, but it has the longest lead time in the register and its
> author must remain isolated from RI-PY throughout. Starting it late is the single most
> likely cause of schedule failure.

### Wave 1 — Governance hygiene (parallelisable, no cross-dependencies)

| Order | Decision | Rationale |
|---|---|---|
| 4 | **DR-004** ADR-001 collision | Unblocks ADR numbering. |
| 5 | **DR-005** ADR acceptance bar | Determines whether Waves 3–4 need RFCs; must precede authoring. |
| 6 | **DR-007** orphaned domain ownership | Cheap; without it ADR-004 cannot close its own scope. |
| 7 | **DR-008** AD-CA-005 scope | Cheap; without it ADR-003 has no defined subject. |
| 8 | **DR-026** APS ID collision | Independent of the rest; unblocks cross-repository traceability. |

### Wave 2 — Upstream normative repairs

| Order | Decision | Rationale |
|---|---|---|
| 9 | **DR-006** APS-001 minimum scope | Everything below inherits APS-001's authority. |
| 10 | **DR-019** provenance boundary + APS-200 §4 correction | CR-E blocks AD-CA-009 **and** AD-CA-010 **and** all hash work. Must precede DR-017/018/020. |
| 11 | **DR-020** identity schema + APS-200 extension | Depends on DR-019; supplies the substrate DR-021 registers. |

### Wave 3 — Source boundary (ADR-002 domain)

| Order | Decision | Rationale |
|---|---|---|
| 12 | **DR-009** admissible source statuses | Determines Source Set membership. |
| 13 | **DR-010** authoritative representation | Determines the byte sequence. |
| 14 | **DR-011** canonicalization lossy/lossless | Depends on 12–13. Enables evidence IE-2. |

### Wave 4 — Numeric and serialization (ADR-003 / ADR-004 domains)

| Order | Decision | Rationale |
|---|---|---|
| 15 | **DR-027** ADP-001 disposition | Determines where the projection is defined. |
| 16 | **DR-012** dimension | Determines byte length; precedes all other numeric decisions. |
| 17 | **DR-013** integer division semantics | Independent of 18; both feed IE-5. |
| 18 | **DR-014** float→fixed rounding + float boundary | ditto. |
| 19 | **DR-015** widths, overflow, endianness, tolerance | Depends on 16–18. |
| 20 | **DR-016** input-length domain | Depends on 16. |
| 21 | **DR-017** canonical serialization format | Depends on 16–20 and on DR-019/DR-020. |
| 22 | **DR-018** hash domains + separation | Depends on 21. **Last of the technical core.** |

### Wave 5 — Lifecycle and verification (ADR-006 domain)

| Order | Decision | Rationale |
|---|---|---|
| 23 | **DR-022** VERIFIED / REGISTERED states | Determines the lifecycle to be governed. |
| 24 | **DR-021** registry creation | Depends on 23 and on DR-020. |
| 25 | **DR-023** freeze authority + self-freeze deadlock | Depends on 23. |
| 26 | **DR-024** CR-007 | Depends on 23–25 — CR-007's inputs are registered artifacts. |
| 27 | **DR-025** independent implementation *(started in Wave 0)* | Verification closes only after all of the above. |

**Critical path:** DR-002 → DR-001 → DR-003 → DR-019 → DR-020 → DR-017 → DR-018 → IE-13.
**Longest lead item:** DR-025, which must start first and closes last.

---

## 16. Merge Blockers

### P0 — Cannot proceed

No ADR may be authored, submitted, or accepted while any of these is open.

| ID | Blocker | Decision |
|---|---|---|
| P0-01 | Decision authority undefined — Chief Architect vs Protocol Custodian never equated | DR-002 |
| P0-02 | Two repositories claim `aura-specification` | DR-001 |
| P0-03 | Document authority model contested; SPEC-002 has no defined position | DR-003 |
| P0-04 | `ADR-001` triple identifier collision; "next sequential ADR-NNN" undefined | DR-004 |
| P0-05 | APS-001 Status TODO — root of the normative chain is absent | DR-006 |
| P0-06 | AD-CA-004 and AD-CA-006 orphaned; ADR-004 cannot close its own scope | DR-007 |
| P0-07 | APS-200 §8 canonical serialization is a TODO permitting three formats | DR-017 |
| P0-08 | APS-200 §4 forces a wall-clock timestamp into every integrity hash | DR-019 |
| P0-09 | Integer division semantics undefined and already divergent | DR-013 |
| P0-10 | Float→fixed rounding undefined and already divergent, on the Vector path | DR-014 |
| P0-11 | ADP-001 referenced but 0/14 defined | DR-027 |
| P0-12 | No independent implementation exists; success criterion unfalsifiable | DR-025 |
| P0-13 | Cross-repository APS identifier collision | DR-026 |

### P1 — Can prepare but cannot accept

Authoring may proceed; acceptance may not.

| ID | Blocker | Decision |
|---|---|---|
| P1-01 | GOV-001 §5.2 vs §6 contradict on ADR acceptance | DR-005 |
| P1-02 | No ARC exists; `INV-DOC-002` unsatisfiable; SPEC-001 does not exist | DR-003 |
| P1-03 | No invariant covers the artifact surface; INV-010 already violated (5 invariants lack CONF tests) | DR-007, and identifiers not yet assigned |
| P1-04 | "FROZEN" self-asserted by an implementation without conferring authority | DR-023 |
| P1-05 | CONF-003 and CONF-006 cannot detect cross-language divergence | DR-017, DR-018 |
| P1-06 | VERIFIED / REGISTERED states do not exist; no registry substrate | DR-021, DR-022 |
| P1-07 | CR-007 undefined | DR-024 |
| P1-08 | AD-CA-005 scope disputed | DR-008 |
| P1-09 | Fail-open on mismatched vector dimensions — violates INV-008 (live Critical invariant) | DR-015 |
| P1-10 | Numeric widths, overflow, NaN, endianness undefined | DR-015 |
| P1-11 | Input-length domain undefined; silent truncation of over-length input | DR-016 |

### P2 — Can defer

Must close before SPEC-002 leaves DRAFT.

| ID | Blocker | Note |
|---|---|---|
| P2-01 | Unregistered identifier prefixes: `SPEC`, `REQ`, `AD-CA`, `GOV`, `ADP`, `INV-DOC`, `COMP-TM`, `POL-VER`, `RI`, `CR` | APS-000 §3 / Appendix A registers only APS, INV, ADR, ARR, RFC, CONF, EVID, FIX, REL, POL, ENT, DOC |
| P2-02 | APS-500 §5 links `../fixtures/FIX-001…`; file is at `fixtures/core/FIX-001…` | broken internal reference |
| P2-03 | `docs/adr/001-document-model.md` duplicates `adrs/ADR-001_DOCUMENT_MODEL.md` divergently | subsumed by P0-04 |
| P2-04 | `core/evaluator.py` comment says drift clamps to [0, 100000]; code clamps to [0, 200000] | executed output confirms the code |
| P2-05 | `(ord(c) % 32) * 3125` yields [0, 96875], never the documented 10⁵, all non-negative — contradicts `evaluator.py`'s stated input contract | placeholder module; replaced regardless |
| P2-06 | No CI in the specification repository — `doc/ci/validate-ids`, `traceability-check`, `frozen-check` specified by `ADR-001_DOCUMENT_MODEL` do not exist | identifier uniqueness and frozen immutability unenforced |
| P2-07 | APS-900 §7 example entries cite `EVID-001`, `EVID-005`, `FIX-005` — identifiers that exist nowhere | invented examples in a normative document |

**Totals: 13 P0 · 11 P1 · 7 P2. Gate status: CLOSED.**

---

## 17. Explicit Non-Decisions

This document **deliberately does not decide** the following. Each is listed so that no reader
can mistake analysis for authority.

**Governance**
1. Which repository is authoritative.
2. Whether "Chief Architect" and "Protocol Custodian" are one office.
3. Which document authority model governs.
4. Which document keeps the identifier `ADR-001`.
5. Whether AD-CA-class ADRs require RFCs.
6. Which artifacts own AD-CA-004 and AD-CA-006.
7. The scope of AD-CA-005.

**Source and canonicalization**
8. The Source Set or Source Boundary.
9. Which document statuses may enter the Source Set.
10. Which stored representation of a document is authoritative.
11. Whether canonicalization is lossy or lossless; whether SHADOW_SPEC v1.0 applies.

**Numeric — explicitly required by the task, and honoured**
12. **No rounding model is selected.**
13. **No division model is selected.**
14. No vector dimension is selected.
15. No integer widths, overflow policy, NaN policy, or endianness is selected.
16. No input-length policy is selected.
17. No position is taken on whether tolerance may establish identity.

**Serialization — explicitly required by the task, and honoured**
18. **No serialization format is chosen. Not JSON, not CBOR, not Protocol Buffers.**
19. No field set, field ordering, or absent-field representation is chosen.
20. No hash domain, pre-image, or domain-separation mechanism is chosen.
21. No hash algorithm is chosen (APS-001 §7 remains TODO).

**Identity, provenance, lifecycle**
22. No identity schema, field name, or binding rule is chosen.
23. No position is taken on whether provenance belongs inside, outside, or bound to the
    canonical representation.
24. No position is taken on whether timestamp, commit, compiler, OS, CPU, or language version
    *should* change identity — only on what they *do* today.
25. **The lifecycle is not changed.** Existing and proposed lifecycles are recorded side by
    side.
26. No registry is created, located, or specified.
27. No freeze authority is assigned; the self-freeze deadlock is not resolved.

**Artifact and implementation**
28. **No Constitution Artifact is created, generated, registered, or frozen.**
29. **No Constitution Vector is created or generated.**
30. **No source code is modified.** No fix is applied to the reproduced divergences in §6 or to
    the fail-open in `vector_similarity_int32`.
31. No ADR is created, and **ADR-002…ADR-006 are neither authored nor accepted**.
32. ADP-001 is not defined or implemented.
33. CR-007's semantics are not inferred.
34. No fixture is authored — doing so would make the fixture the de-facto specification and
    invert SPEC-002's Governing Direction.
35. No implementation is recognised, certified, or decertified.

**Status**
36. SPEC-002's readiness status is **not changed**. It remains **NOT READY**.
37. No document's lifecycle status is advanced, and nothing is marked APPROVED or FROZEN.

---

## Appendix A — Conflict index

| ID | Conflict | Section | Severity |
|---|---|---|---|
| CR-A | Two repositories named `aura-specification` | §2.2 | P0 |
| CR-B | Constitution Article V vs `ADR-001_DOCUMENT_MODEL` | §3.2 | P0 |
| CR-C | Role vocabularies differ; authority undetermined | §3.3 | P0 |
| CR-D | APS-200 §4 supplies one identity slot where SPEC-002 §4.4 requires four | §8.5 | P0 |
| CR-E | APS-200 §4 forces wall-clock provenance into every integrity hash | §9.2 | P0 |
| CR-F | FROZEN conferred by authority vs self-asserted by implementation | §10.4 | P1 |

## Appendix B — Reproduction record

Both divergences below were executed during review against the code as committed at `9c6a5d8`.
Neither is a modification; neither was written to any file.

```
# Divergence 1 — integer division (core/evaluator.py)
dot                    = -7000029999
Python floor  (dot//S) = -70001
Rust/C++/JS trunc      = -70000
ARI path, sa = -70001:  Python -49001   |   Rust -49000

# Divergence 2 — float→fixed tie rounding (core/offline_normalizer.py)
       x*1e5  Python round   half-away (C/Rust)   half-up (JS)
      0.5000             0                    1              1
      2.5000             2                    3              3

# Fail-open — mismatched operand dimensions (core/evaluator.py)
evaluate(dim-1536 constitution, length-1 vector) -> {'ari': 0, 'drift': 200000}
# no exception, no diagnostic
```

## Appendix C — Cross-reference to the review package

| This brief | Source |
|---|---|
| §2, §3 | `review/.../00_REVIEW_SCOPE_AND_EVIDENCE_BASE.md` §4, §6 |
| §5, §6, §7 | `review/.../01_ADR_REVIEW.md` §1–§4, §7 |
| §5 matrix, §8 | `review/.../02_TRACEABILITY_MATRIX.md` §1–§5 |
| §4, §9 | `review/.../03_SPEC-002_v0.4_DRAFT.md` §7 (upstream register U-1…U-7) |
| §12 | `review/.../04_EVIDENCE_PLAN.md` E1–E12 |
| §16 | `review/.../05_MERGE_BLOCKERS.md` |
| §14 | `review/.../06_OPEN_DECISIONS.md` OD-001…OD-016 |
| §6, §10.4, §11 | `review/.../07_IMPLEMENTATION_CONFORMANCE.md` §2–§5 |

---

**END OF ARCHITECTURE-RESOLUTION-001**

*No normative effect. No decision made. 27 decisions identified, 13 at P0. All require human
architectural authority. SPEC-002 remains NOT READY.*
