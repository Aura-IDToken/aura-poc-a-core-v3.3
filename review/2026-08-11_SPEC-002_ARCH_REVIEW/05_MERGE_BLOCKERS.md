# 05 — Merge Blockers

Document ID: REV-2026-08-11-005
Status: DRAFT — ANALYSIS ARTIFACT, NO NORMATIVE EFFECT
Date: 2026-08-11

---

## 0. Severity definitions (as given in the review task)

| Level | Meaning |
|---|---|
| **P0** | Work cannot continue. No ADR may be authored, submitted, or accepted while any P0 is open. |
| **P1** | Required before any ADR reaches ACCEPTED. Authoring may proceed in parallel. |
| **P2** | May be deferred. Must be closed before SPEC-002 leaves DRAFT. |

Every blocker names the authority that can close it. **None can be closed by an AI agent**
(GOV-001 §9; Constitution Article VIII).

---

## P0 — Cannot continue

### BLOCKER-P0-001 — Two repositories claim the name `aura-specification`
**Evidence.** `AuraIDToken/aura-specification` (full corpus, `62d2d6b`) and
`aura-nomos/aura-specification` (README stub of 11 bytes + CODEOWNERS mirroring the other's
layout). Both writable by the same account. No supersession recorded in either.
**Impact.** REQ-002-003 requires "repository location" as part of Source Document Identity.
With two locations and no precedence, **AD-CA-001 cannot be resolved even in principle**, and
every downstream decision inherits the ambiguity.
**Closes when.** Protocol Custodian designates one authoritative repository and records the
other's status. → **OD-001**

### BLOCKER-P0-002 — APS-001, the root normative specification, does not exist
**Evidence.** `specification/APS-001_PROTOCOL_SPECIFICATION.md`, `Status: TODO`, `Version:
0.1-DRAFT`, body entirely `> **TODO**` stubs, header: *"This document does not yet exist. It
is the highest-priority gap."*
**Impact.** Constitution Article V places APS-001 directly beneath the Constitution and above
APS-100. APS-100/200/300/400/500/950 all declare `Authority: APS-001`. Every one of those
headers is a dangling reference. SPEC-002 §11 already notes this; review confirms APS-001 is
not merely incomplete but **absent**. No requirement can rest on an absent root.
**Closes when.** APS-001 exists with normative content, at minimum for §2 (execution model),
§7 (cryptographic requirements) and §8 (error handling), which SPEC-002 depends on.

### BLOCKER-P0-003 — `ADR-001` is a triple identifier collision
**Evidence.** `adrs/ADR-001_REPOSITORY_STRUCTURE.md` (**ACCEPTED**);
`adrs/ADR-001_DOCUMENT_MODEL.md` (**PROPOSED**); `docs/adr/001-document-model.md`
(**DRAFT**). The latter two are divergent copies of one decision, differing in status, front
matter and body. `adrs/README.md` indexes only the first.
**Impact.** Violates APS-000 §4, VERSIONING.md §8, and `INV-DOC-005` declared by the colliding
document itself. GOVERNANCE.md §6 requires "the next sequential ADR-NNN"; with ADR-001
ambiguous, "next" is undefined and **any ADR-002 inherits a corrupt baseline**.
**Closes when.** Custodian resolves the collision: retain one ADR-001, reassign or withdraw
the others, delete or clearly mark the duplicate copy, and update the index.

### BLOCKER-P0-004 — AD-CA-004 and AD-CA-006 are orphaned
**Evidence.** SPEC-002 §6 defines twelve decision domains. The five-ADR grouping covers ten.
AD-CA-004 (normalization rules) and AD-CA-006 (dictionary identity + dependency closure) have
no owning artifact. Both verified present and UNRESOLVED in §6 and Appendix A(E).
**Impact.** Not bookkeeping. **AD-CA-004 blocks REQ-002-021 and REQ-002-022** — the very
requirements ADR-004 exists to close via AD-CA-008, so **ADR-004 cannot close its own scope**.
**AD-CA-006 blocks REQ-002-034** (dependency closure), so "same source → same vector" stays
unprovable: an undeclared dependency may vary between conformant implementations.
**Closes when.** Every AD-CA domain is assigned to exactly one governance artifact. → **OD-016**

### BLOCKER-P0-005 — Two incompatible document models are simultaneously live
**Evidence.** Constitution Article V (**FROZEN**): `Constitution → APS-001 → APS-100 →
ADR/ARR/RFC → … → Implementation`. `ADR-001_DOCUMENT_MODEL` (**PROPOSED**): `RFC → ADR → ARC →
SPEC → APS(release) → Implementation`, plus eight new `INV-DOC-*` invariants absent from
APS-100 and the registry, using a prefix absent from APS-000 Appendix A.
**Impact.** The models invert the authority direction between APS and ADR/SPEC. **SPEC-002
exists only under the PROPOSED model**, which contradicts the FROZEN Constitution. Per
Article V and the Authority Precedence in AGENTS.md/CLAUDE.md, the Constitution prevails — so
on the current record SPEC-002 has no defined place in the canonical hierarchy, and neither
would ADR-002…006.
**Closes when.** Custodian either amends the Constitution under Article XI to adopt the new
model, or rejects it and re-homes SPEC-002 under Article V. → **OD-003**

### BLOCKER-P0-006 — Canonical serialization has no authority to point at
**Evidence.** SPEC-002 §7 traces REQ-002-021 to **APS-200 §8**, which reads: *"**TODO**:
Define the canonical serialization format for interoperability between RI-PY and RI-RS"* —
after text permitting **any** of JSON, CBOR or Protobuf. REQ-002-017/018 trace to APS-200 §4
(which defines `integrity_hash` in terms of the undefined canonical serialization) and
APS-300 §5 (*"**TODO**: Define the canonical algorithm for computing `evidence_hash`…"*).
**Impact.** Four traceability rows point at TODOs. Three permitted formats means three byte
sequences for one artifact. **AD-CA-008 cannot be resolved by SPEC-002 alone** — it requires
upstream APS changes.
**Closes when.** APS-200 §8 defines exactly one canonical serialization; APS-300 §5 defines
`evidence_hash`.

### BLOCKER-P0-007 — APS-200 §4 forces a wall-clock timestamp into every integrity hash
**Evidence.** APS-200 §4 Common Object Contract mandates, for **every** entity, both
`created_at` (ISO 8601 wall clock, MUST) and `integrity_hash` = *"SHA-256 hash of the
canonical serialization of this object"* (MUST).
**Impact.** An artifact modelled as an APS-200 entity hashes differently on every
construction. Same source → different hash. Direct contradiction of SPEC-002 §5.1 and
Constitution Article IV P2. This is the CONTENT/IDENTITY/PROVENANCE conflation that SPEC-002
§4.4 exists to prevent, **already baked into a DRAFT normative document upstream**.
AD-CA-009 and AD-CA-010 cannot be resolved around it.
**Closes when.** APS-200 §4 is corrected so a deterministic artifact is not obliged to carry
wall-clock provenance inside its integrity hash. → **OD-008**

### BLOCKER-P0-008 — ADP-001 does not exist but is proposed as a dependency
**Evidence.** No document, identifier or definition for "ADP-001 — Aura Deterministic
Projection" exists in the specification repository or either implementation. `ADP` is not a
registered prefix (APS-000 §3, Appendix A). Assessed against the fourteen required
definitions, it is **0/14**.
**Impact.** ADR-003 is proposed to rest on it. A specification resting on a name rather than a
protocol cannot be independently implemented.
**Closes when.** Either ADP-001 is fully specified through the RFC process, or the projection
is defined directly under AD-CA-003 and the ADP-001 label is dropped. → **OD-010**

### BLOCKER-P0-009 — No independent implementation exists ⭐
**Evidence.** `aura-poc-a-core-v3.3`: `core/embedding.py` is self-declared *"Placeholder"*;
**no code path reads `AURA_CONSTITUTION.md`**; `generate_sample_constitution` builds a vector
from the synthetic pattern `0.5 + 0.1 * (i % 10)`, unrelated to the Constitution.
`aura-guard-v1.3`: repository-wide search for `constitution`, `vector`, `ARI` returns **no
matches in `src/`** — it is a PII/prompt guard with its own `SHADOW_SPEC v1.0` normalizer.
**Impact.** The stage's success criterion — *two independent engineers obtain identical bytes
without inspecting the reference implementation* — has **no second party**. E12 cannot be
executed. The criterion is not failing; it is **unfalsifiable**, which is worse, because
nothing in CI can ever report it red.
**Closes when.** A second implementation of the Constitution Artifact surface exists, authored
without reading `aura-poc-a-core-v3.3`.

### BLOCKER-P0-010 — Cross-repository APS identifier collision
**Evidence.** In `aura-specification`: APS-200 = Canonical Data Model, APS-400 = Conformance
Test Matrix, APS-500 = Reference Fixtures, APS-900 = Compliance Mapping. In
`aura-poc-a-core-v3.3` `docs/GAP-001.md` §3: APS-200 = **ARI Engine**, APS-400 =
**Serialization**, APS-500 = **ZK Layer**, APS-900 = **Conformance Runner**. GAP-001 states
plainly that requirements were *inferred* because *"the external `aura-specification`
repository is not co-located here"*.
**Impact.** Every cross-repository conformance claim is ambiguous between two different
specifications. Violates APS-000 §4 and AGENTS.md rule 7 ("compliance claims must not be
inferred merely from architecture names").
**Closes when.** GAP-001's coverage matrix is withdrawn or re-mapped to the real APS
identifiers. → **OD-009**

### BLOCKER-P0-011 — Numeric semantics are undefined and already divergent
**Evidence — reproduced, not asserted.**
*(a)* `core/evaluator.py` uses Python `//` (floor toward −∞) where Rust/C/JS truncate toward
zero. Executed: `dot = -7000029999` → **−70001** (Python) vs **−70000** (truncation); ARI path
`sa = -70001` → **−49001** vs **−49000**.
*(b)* `core/offline_normalizer.py` uses Python `round()` (half-to-even) where C/Rust are
half-away-from-zero and JS is half-up. Executed: `0.5` → **0** / **1** / **1**; `2.5` → **2** /
**3** / **3**. This is the **Constitution Vector construction path**.
**Impact.** A correct Rust implementation written against every document that exists today
produces a different vector and a different ARI. Defeats **INV-002** and **INV-006** (both
Critical). SPEC-002 §6 lists `round-half-to-even` as a **candidate only** and §3.4 says no
candidate is a default — yet the implementation has already committed to it silently. This is
precisely "implementation accident becoming protocol invariant".
*Qualification, stated precisely.* Current `embed_text` emits only non-negative components, so
the demo path does not fire today, and the existing x86_64-vs-ARM64 CI comparison runs Python
on both sides and cannot detect it. **Latent and reachable, not a live production failure** —
but permanent if frozen.
**Closes when.** AD-CA-007 fixes division/rounding semantics language-independently
(proposed REQ-002-038, REQ-002-039). → **OD-011**, **OD-012**

---

## P1 — Required before ACCEPTED

### BLOCKER-P1-001 — GOV-001 contradicts itself on ADR acceptance
GOV-001 §5.2 requires RFC + 14-day comment + ARB + Chief Architect for changes of this class;
§6 says *"Merging the PR = accepting the ADR"* with one reviewer. Every AD-CA domain is a
Major Change by the §5.2 test. The acceptance bar for ADR-002…006 is therefore undefined, and
the §6 path would let canonical bytes be fixed by a single merge. GOV-001 is itself only
`1.0-DRAFT`. → **OD-004**

### BLOCKER-P1-002 — No ARC exists, but the live document model requires one per SPEC
`INV-DOC-002` requires every SPEC to reference ≥1 ARC. `arc/` holds only a README;
`arc_to_spec_mapping.yaml` is `mappings: []`; `ARC_TO_SPEC_MAPPING.md` defers to "when SPEC-001
is approved" — and **SPEC-001 does not exist**. SPEC-002 cites no ARC and is therefore
non-conformant on the model that defines it.

### BLOCKER-P1-003 — No invariant covers the Constitution Artifact, and INV-010 is already violated
`INVARIANT_REGISTRY.md` holds INV-001…015; none concerns artifact construction, vector
derivation, identity, provenance, registration or freeze. Each of AD-CA-001…012 needs at least
one new invariant (**identifier not yet assigned** throughout). Meanwhile the registry
**self-reports violation of INV-010** — INV-007, INV-012, INV-013, INV-014, INV-015 have no
CONF test. Adding invariants without tests deepens a live Critical-class violation.

### BLOCKER-P1-004 — "FROZEN" is self-asserted by an implementation
`VERSIONING.md` §3 reserves `APPROVED → FROZEN` to the Chief Architect under Article XI. Yet
`CONSTITUTIONAL_DECREE.md` Article VIII calls v3.3 the "Frozen Iron Core";
`docs/architecture.md` closes with "Status: FROZEN — MC-READY 2026"; `AUDIT_LAYER_SPEC.md` is
a "normative frozen spec". `reference/RI-PY_AURA_POC_A_CORE.md` records the conflict itself —
*"Self-declared FROZEN (v3.3) — this creates a governance challenge as APS gaps require
changes"* — alongside `APS-950 Certification Status: NOT CERTIFIED`. REQ-002-029 cannot specify
a freeze verification procedure while "frozen" means two different things. It also creates a
deadlock: a self-frozen, uncertified implementation cannot be corrected to meet the future
contract without breaking its own freeze claim. → **OD-014**

### BLOCKER-P1-005 — Conformance tests cannot detect cross-language divergence
CONF-003's procedure is *"serialize … twice independently (fresh process each time)"* — one
implementation against itself. CONF-006's PASS criterion is x86 vs ARM — one language across
two architectures. **Neither can detect BLOCKER-P0-011**, which is the divergence class that
actually matters. INV-003 and INV-006 are therefore not effectively verified for
interoperability. Any new CONF test for AD-CA-007/008 must be cross-implementation by
construction.

### BLOCKER-P1-006 — `VERIFIED` and `REGISTERED` states do not exist
The lifecycle `DRAFT → VERIFIED → REGISTERED → APPROVED → FROZEN` appears in review scoping but
not in the repository. `VERSIONING.md` §3 and GOV-001 §4 both define `DRAFT → REVIEW →
APPROVED → FROZEN (↘ DEPRECATED → ARCHIVED)`. Adding two states is a **new decision** affecting
every artifact class, not a clarification, and REQ-002-028's registry has no substrate:
APS-000 §7 describes a Canonical Registry that does not exist. → **OD-015**

### BLOCKER-P1-007 — CR-007 is undefined
SPEC-002 §2.2 forbids implementing it, §11 and Appendix B call it BLOCKED, and it is expected
to act as a verifier rather than an identity-creating mechanism. But **no document defines its
inputs, outputs, authority, or pass/fail semantics.** The implementation repository defines
CR-001, CR-003, CR-004 only. ADR-006 cannot state CR-007's role without inventing it. → **OD-013**

### BLOCKER-P1-008 — AD-CA-005 scope is disputed
Review input describes AD-CA-005 as "vector projection mechanism"; SPEC-002 §6 defines it as
"embedding method identity and versioning model". Different domains. Authoring ADR-003 to the
former silently redefines AD-CA-005 and orphans its actual subject matter (REQ-002-012).
→ **OD-002**

---

## P2 — May be deferred, must close before DRAFT exit

### BLOCKER-P2-001 — Unregistered identifier prefixes
`SPEC`, `REQ`, `AD-CA`, `GOV`, `ADP`, `INV-DOC`, `COMP-TM`, `POL-VER`, `RI` are all in active
use; APS-000 §3 and Appendix A register only APS, INV, ADR, ARR, RFC, CONF, EVID, FIX, REL,
POL, ENT, DOC. Either the registry or the usage must change.

### BLOCKER-P2-002 — Broken internal reference in APS-500
APS-500 §5 links `../fixtures/FIX-001_BASIC_EVALUATION.json`; the file is at
`fixtures/core/FIX-001_BASIC_EVALUATION.json`.

### BLOCKER-P2-003 — `docs/adr/001-document-model.md` duplicates `adrs/ADR-001_DOCUMENT_MODEL.md`
Two divergent copies in two directories. Subsumed by P0-003 but listed separately because the
`docs/adr/` path is outside the structure ADR-001_REPOSITORY_STRUCTURE established.

### BLOCKER-P2-004 — Comment/code disagreement on the drift clamp
`core/evaluator.py` comments "Clamp drift to [0, 100000]" above code clamping to
**[0, 200000]**; executed output confirms the code (`drift = 200000`). Which is normative is
unrecorded.

### BLOCKER-P2-005 — Scale claim not met by the placeholder embedding
`(ord(c) % 32) * 3125` yields components in **[0, 96875]**, never the documented 10⁵, and all
non-negative — so the output is neither unit-normalized nor sign-balanced, contradicting
`evaluator.py`'s stated input contract ("Pre-normalized … ||v|| = 10^5"). Two modules in one
repository disagree on the vector contract. P2 only because the module is a placeholder that
must be replaced regardless.

### BLOCKER-P2-006 — No CI in the specification repository
`ADR-001_DOCUMENT_MODEL` specifies `doc/ci/validate-ids`, `doc/ci/traceability-check` and
`doc/ci/frozen-check`. **None exists** — `.github/` contains only CODEOWNERS, issue templates
and a PR template. There are no workflows at all, so identifier uniqueness (P0-003) and frozen
immutability are unenforced.

---

## Summary

| Severity | Count | Effect |
|---|---|---|
| **P0** | **11** | **No ADR may be authored, submitted, or accepted.** |
| **P1** | 8 | No ADR may reach ACCEPTED. |
| **P2** | 6 | Must close before SPEC-002 leaves DRAFT. |

**Gate status: CLOSED.**

Four P0 blockers (002, 006, 007, 010) cannot be closed inside `aura-specification` at all —
they require changes to APS-001, APS-200, APS-300, and to `GAP-001.md` in the implementation
repository. Three (001, 003, 005) are governance decisions requiring no engineering. One
(009) requires commissioning an independent implementation and has the longest lead time of
anything in this list; it should be started first even though it closes last.

---

*End of 05_MERGE_BLOCKERS.md*
