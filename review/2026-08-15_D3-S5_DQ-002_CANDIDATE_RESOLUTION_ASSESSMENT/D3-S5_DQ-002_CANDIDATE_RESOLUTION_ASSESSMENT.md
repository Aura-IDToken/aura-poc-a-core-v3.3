# DQ-002 — Candidate Resolution Assessment

**Subject:** a candidate resolution of CONFLICT-DQ002-01, submitted for assessment.
**Document class:** assessment. **Normative effect: NONE.**
**Date:** 2026-08-15
**Prepared by:** Claude. **Not** the Architecture Owner and **not** the Protocol Custodian.

**This is an assessment, not a decision.** No normative document was changed, no ADR was
created, no code was implemented, and DQ-002 is not closed.

---

## 0. The candidate as submitted

| # | Candidate element |
|---|---|
| **C1** | Evidence uses a single field, `integrity_hash` |
| **C2** | `evidence_hash` is withdrawn |
| **C3** | `integrity_hash` is computed from the canonical serialization of the Evidence object |
| **C4** | RFC 8785 JCS is indicated as the serialization candidate |

### 0.1 Method

Every claim is labelled **EVIDENCE** (verifiable at a cited location) or **INFERENCE**
(derived, no normative weight). Where the material does not permit confirmation, the
assessment says so explicitly rather than filling the gap.

Sources re-read for this assessment: `AuraIDToken/aura-specification` @ `62d2d6b`,
`AuraIDToken/aura-guard-v1.3` @ `443f72e`, `AuraIDToken/aura-poc-a-core-v3.3` @ `ab6e68e`.

---

## A. Traceability

| # | Candidate element | Source | Location | Status |
|---|---|---|---|---|
| **C1** | Evidence uses a single `integrity_hash` | APS-200 requires `integrity_hash` on every entity; ENT-005 is an entity | `APS-200:49`, `:58`, `:40` | **PARTIAL** — APS-200 supports *requiring* `integrity_hash` on Evidence. It does **not** support *singularity*: nothing states that Evidence bears only one record-level hash |
| **C2** | `evidence_hash` is withdrawn | APS-300 requires `evidence_hash` as **MUST** | `APS-300:69`, `:56` | **CONFLICT** — the candidate proposes removing a field the current normative text makes mandatory. Withdrawal is a **normative change to APS-300**, not a reading of it |
| **C3** | `integrity_hash` from the canonical serialization of Evidence | APS-200 defines it that way | `APS-200:58` | **PARTIAL** — the phrasing matches `:58` verbatim, but `:58` is silent on self-inclusion, and the serialization it refers to is marked **TODO** at `APS-200:218` |
| **C4** | RFC 8785 JCS as serialization candidate | — | — | **UNSUPPORTED** — see §C. No occurrence in any normative document |

**INFERENCE.** C1 and C3 restate APS-200's existing text and are therefore *compatible*
with it, but neither is *established* by it on the disputed points. C2 is the load-bearing
element and it is the one the current text contradicts.

---

## B. CONFLICT-DQ002-01 — the three unresolved questions

### B.1 Self-inclusion vs self-exclusion of `integrity_hash`

**Does the candidate resolve it? NO.**

| Element | Content |
|---|---|
| **EVIDENCE** | `APS-200:58` — "SHA-256 hash of the canonical serialization of **this object**". Silent on whether the `integrity_hash` field is part of that representation. `integrity_hash` is itself a MUST field of the object (`:49`) |
| **Candidate C3** | Says "computed from the canonical serialization of Evidence" — **the same phrasing, with the same silence** |
| **Status** | **UNSUPPORTED / UNCHANGED** |

**INFERENCE.** C3 reproduces the ambiguity rather than removing it. As written, the
definition remains circular: a hash "of this object" where the hash is a field of that
object. Adopting C3 verbatim would leave Q1 exactly where it is.

**Recorded explicitly, as instructed:** *the available material does not permit
confirmation of self-exclusion.* Nothing in APS-200 states it. The only explicit
self-exclusion in the corpus is at `APS-300:69` — attached to the field the candidate
proposes to withdraw.

**INFERENCE — a consequence worth flagging.** C2 + C3 together would **remove the corpus's
only explicit statement of self-exclusion** while keeping the field whose self-inclusion is
undetermined. That direction reduces, rather than increases, the normative material
available to answer Q1.

### B.2 One hash vs two independent hashes

**Does the candidate resolve it? It ANSWERS it, but by amendment, not by interpretation.**

| Element | Content |
|---|---|
| **EVIDENCE** | Neither APS-200 nor APS-300 states whether `integrity_hash` and `evidence_hash` are one concept or two. APS-200 contains **no relational verb anywhere in the document** (search for `includ`, `exclud`, `nest`, `derive`, `depend`, `cover`, `compris`, `consist of`, `based on` → zero matches) |
| **Candidate C1+C2** | Selects "one concept", realised by withdrawing `evidence_hash` |
| **Status** | **PARTIAL — supported as a coherent option, unsupported as a reading of the current text** |

**INFERENCE.** This is a defensible answer to Q2. But it is an **amendment**: it changes
APS-300 rather than resolving what APS-300 currently means. The Custodian may well rule
this way; the point for this assessment is that the candidate cannot be adopted by
interpretation alone.

### B.3 Authority APS-200 ↔ APS-300

**Does the candidate resolve it? NO — and it presupposes an answer.**

| Element | Content |
|---|---|
| **EVIDENCE** | APS-300 header names Authority `APS-001 · APS-100 · **APS-200**`. `APS-200:129` delegates Evidence's field definition **to** APS-300 §5. `APS-300:56` introduces its list as "at minimum" |
| **EVIDENCE** | **No document in the corpus adjudicates a conflict between two APS documents** — not found in inspected scope |
| **Candidate** | By withdrawing an APS-300 MUST field in favour of an APS-200 field, the candidate **presupposes APS-200 precedence** |
| **Status** | **UNSUPPORTED** — the presupposition is not established by any located text |

**INFERENCE.** Two orderings remain textually available and the candidate silently picks
one. That precedence ruling is precisely Q3, which is reserved to the Custodian.

---

## C. RFC 8785 / JCS

**Question: do the available sources establish RFC 8785 / JCS as a normative contract, an
existing implementation, a historical decision, or merely a proposal/mention?**

### C.1 Search performed

`git grep` at HEAD **and** `git log --all -S` over full history, in all three
repositories, for: `8785`, `RFC 8785`, `JCS`, `jcs`, `JSON Canonicalization`,
`canonicalization scheme`.

| Repository | HEAD | History |
|---|---|---|
| `aura-specification` (APS-100/200/300/400/500/950, SPEC-002, Constitution, invariants, conformance, fixtures) | **0** | 1 apparent hit — **investigated and rejected**, see C.2 |
| `aura-guard-v1.3` | **0** | **0** |
| `aura-poc-a-core-v3.3` | hits **only** inside `review/` audit artifacts | — |

### C.2 The apparent specification hit is a false positive

**EVIDENCE.** `git log --all -S"8785"` in `aura-specification` returns commit `6f4d971`
"Add files via upload" — which adds **nine PDF files** and **zero text insertions**
(`9 files changed, 0 insertions(+), 0 deletions(-)`; all entries `Bin 0 -> …`).

**EVIDENCE.** Byte-level inspection of those PDFs:

- `AURA Protocol Specification APS-000 …pdf` — the matched context is
  `…oYK27ЖJCS8�m�@� j��k5!C…`, i.e. the letters `JCS` occurring inside a **compressed
  binary stream**, surrounded by non-printable bytes.
- `APS-200 — Canonical Data Model …pdf` — the match produced **no printable context at
  all**.

**EVIDENCE.** The `.txt` originals extracted from those same PDFs — the authored source
text — contain **no match** for `8785`, `JCS` or `canonicalization`.

**INFERENCE.** The history hit is compressed-stream noise, not content. **RFC 8785 / JCS
does not appear in the Aura specification corpus.**

### C.3 The POC-A hits are audit prose about a different repository

**EVIDENCE.** Every `jcs` / `8785` occurrence in `aura-poc-a-core-v3.3` lies inside
`review/` artifacts. The substantive one is
`review/2026-08-11_ENGINEERING_BASELINE/07_CONFORMANCE_AUDIT.md:40,51`:

> "`pyproject.toml` … deps `jcs>=0.2.0` …"
> "The declared dependency `jcs` (JSON Canonicalization Scheme, RFC 8785) is **never
> imported**. `PyYAML` is **never imported**. Both are declared in anticipation."

**EVIDENCE.** That audit's scope, stated at `07_CONFORMANCE_AUDIT.md:4-5`, is
`AuraIDToken/Aura-Conformance-Kit` @ `6f10c5e` and `AuraIDToken/Aura-Conformance-Kits`
@ `834ab46` (**archived**) — **not** POC-A and **not** the Guard.

**EVIDENCE.** `aura-poc-a-core-v3.3/pyproject.toml` at HEAD declares **no dependencies at
all** — no `jcs`, no `PyYAML`. `grep -rn "import jcs\|from jcs"` over all `*.py` returns
**nothing**.

### C.4 What POC-A actually does is not JCS

**EVIDENCE.** POC-A canonicalises with `json.dumps(..., sort_keys=True)` —
`audit/merkle.py:85` (with `separators=(",", ":")`), `core/merkle.py:8` and
`compliance/certificate.py:69` (**without** `separators`, i.e. Python's space-padded
default).

**INFERENCE.** `json.dumps(sort_keys=True)` is **not** RFC 8785. JCS mandates ECMAScript
`Number::toString` serialization for numbers and key ordering by UTF-16 code units;
Python's `sort_keys` orders by code point and its float repr follows Python rules. The two
agree on many inputs and diverge on others. Treating the existing POC-A behaviour as "JCS
already" would be incorrect.

### C.5 Determination

| Category | Finding |
|---|---|
| Existing **normative contract** | **NO** — 0 occurrences in APS-000/100/200/300/400/500/950, SPEC-002, the Constitution, the invariant registry, the CONF tests and the fixtures |
| Existing **implementation** | **NO** — 0 in `aura-guard-v1.3` (all history). POC-A uses a different scheme (C.4) |
| **Historical decision** | **NO** — the only trace is a declared-but-never-imported dependency in **two different repositories**, one archived, recorded in an audit as "declared in anticipation" |
| **Proposal / mention** | **This assessment's own submission is the first appearance of JCS as a candidate for Aura.** |

> **RFC 8785 / JCS is NOT an accepted Aura standard.** It is not treated as one anywhere
> in this assessment. Its status as an external IETF standard is **not** evidence of
> adoption, applicability or fit here.

**C4 status: UNSUPPORTED.**

---

## D. Architectural fit

| Question | Assessment |
|---|---|
| **Does it resolve the conflict?** | **PARTIALLY, and by amendment.** It answers Q2 (one concept). It does **not** answer Q1 (self-inclusion — C3 reproduces the ambiguity). It **presupposes** rather than answers Q3 (precedence). |
| **Does it leave new unresolved points?** | **YES — five.** See D.1 |
| **Consistent with DQ-001 Option B?** | **NEUTRAL — no conflict found.** DQ-001 direction B places an explicit adapter between `AuditEntry` and ENT-007. The candidate concerns **ENT-005 Evidence**, a different entity. No interaction was found in inspected scope. *(Recorded per the DQ-001 canonical status: direction B accepted, evidence status CONFLICT/OPEN, no implementation authorization.)* |
| **Impact on DQ-006?** | **HIGH — it partly pre-empts DQ-006.** `APS-200:213` currently permits JSON **or CBOR or protobuf**. C4 would narrow that to JSON and fix a specific canonicalisation. That is a DQ-006 decision being taken inside a DQ-002 candidate. |
| **Impact on DQ-005?** | **INDIRECT.** DQ-005 concerns whether `violations` and other fields enter an integrity domain. A single record-level Evidence hash does not by itself settle membership; but a whole-object rule would make field membership immediately byte-significant. |
| **Forces change to existing hash domains?** | **NOT DIRECTLY, but see below.** |

**EVIDENCE on the last row.** `integrity_hash` and `evidence_hash` are **both
unimplemented**: 0 occurrences in `aura-guard-v1.3` `src/`, full history. The Guard's 15
observed constructions (INFRA-001 inventory @ `9c6bc37`) contain neither. So the candidate
changes **no running hash domain today**.

**INFERENCE.** However, JCS applies to **JSON**. The Guard's entry-chain preimage is a
`"|"`-joined flat string (`chain.rs:36-47`), not JSON; JCS is inapplicable to it without
first restructuring it. If C4 were later generalised beyond Evidence, it would force
exactly such a restructuring — which is a DQ-006/DQ-002 decision, not an implementation
detail.

### D.1 New unresolved points the candidate introduces

| # | New point |
|---|---|
| **N1** | Withdrawing `evidence_hash` removes the corpus's **only** explicit self-exclusion statement, while leaving Q1 open (B.1) |
| **N2** | `APS-300:73`'s TODO asks whether the hash covers "the full JSON serialization or a field-ordered canonical form" — unanswered, and its host field is withdrawn |
| **N3** | Choosing JSON-based JCS narrows `APS-200:213`'s explicit JSON/CBOR/protobuf permission without amending it |
| **N4** | JCS number handling would interact with DQ-007 (numeric representation), where `SPEC-002:381` records AD-CA-007 as **UNRESOLVED** |
| **N5** | APS-300 §5's list omits `object_id`, `object_type`, `created_at` — the candidate addresses `integrity_hash` only, leaving the field-set dimension of the conflict untouched |

---

## E. Reversibility / migration

**No migration is proposed and no code change is proposed.** This section assesses cost
only.

| Dimension | Assessment |
|---|---|
| **Code impact today** | **NONE.** Neither field is implemented in either RI; nothing currently emitted would change |
| **Normative impact** | **HIGH.** Requires amending **APS-300** (withdraw a MUST field) and effectively amending **APS-200** (resolve `:58`'s silence, narrow `:213`) — both Custodian acts under a formal change process |
| **Reversibility before adoption** | **VERY HIGH** — nothing has been emitted |
| **Reversibility after adoption, before publication** | **HIGH** — the normative text could be revised while no Evidence objects exist |
| **Reversibility after Evidence objects are published** | **LOW** — emitted `integrity_hash` values become referenced facts; changing the serialization would invalidate them |
| **Durability caveat** | **EVIDENCE.** APS-200 and APS-300 are both `1.0-DRAFT`, defined by `VERSIONING.md:38` as "may change freely". A decision taken now rests on a mutable base |

**INFERENCE.** The reversibility profile is favourable **now** and degrades sharply at
first publication. That argues for settling Q1 and Q3 before adoption, not after.

---

## F. Decision readiness

### Assessment summary

| Element | Status |
|---|---|
| C1 — single `integrity_hash` | **PARTIAL** |
| C2 — withdraw `evidence_hash` | **CONFLICT** (contradicts `APS-300:69` as written; requires amendment) |
| C3 — from canonical serialization | **PARTIAL** (reproduces the Q1 ambiguity; depends on `APS-200:218` TODO) |
| C4 — RFC 8785 JCS | **UNSUPPORTED** (no occurrence in any normative source) |

### Explicit statements required by the task

- **The available material does not permit confirmation of self-exclusion.** No APS-200
  text states it; the corpus's only explicit self-exclusion is the field the candidate
  withdraws.
- **The available material does not permit confirmation of JCS.** It is absent from the
  entire specification corpus; the single apparent history hit is compressed PDF-stream
  noise; the only real-world trace is an unimported dependency in two other repositories.

**The candidate is not endorsed on grounds of technical elegance.** A single record-level
hash over a canonical serialization is a coherent design, and JCS is a reputable external
standard. Neither fact is evidence that Aura has adopted, or should adopt, either.

---

## Explicit non-decisions

This assessment does **not**: decide DQ-002; select a hash-domain architecture; select a
canonical serialization; resolve Q1, Q2 or Q3 of CONFLICT-DQ002-01; treat RFC 8785/JCS as
an accepted Aura standard; change APS-200, APS-300, APS-100 or SPEC-002; create an ADR;
implement code; close DQ-002; or resolve any other DQ. DQ-001, DQ-003, DQ-004, DQ-005,
DQ-006, DQ-007 and DQ-008 are unchanged.

---

CANDIDATE:
PARTIAL

DQ-002:
BLOCKED

BLOCKERS:
1. **CONFLICT-DQ002-01 Q1 — self-inclusion vs self-exclusion of `integrity_hash`** is not resolved by the candidate. C3 reproduces `APS-200:58`'s silence verbatim, and C2 would withdraw `APS-300:69`, the corpus's only explicit self-exclusion statement. Custodian ruling required.
2. **CONFLICT-DQ002-01 Q3 — APS-200 ↔ APS-300 precedence** is presupposed, not established. Withdrawing an APS-300 MUST field in favour of an APS-200 field assumes APS-200 precedence; no located text establishes it, and no document in the corpus adjudicates between two APS documents. Custodian ruling required.
3. **C2 requires a normative amendment to APS-300, not an interpretation.** `APS-300:69` currently makes `evidence_hash` MUST. Withdrawal is a Custodian act under a formal change process and cannot be effected by a DQ-002 decision alone.
4. **C4 is unsupported by any source.** RFC 8785 / JCS occurs zero times in the specification corpus; the one apparent history hit is compressed PDF-stream noise; no implementation exists in either RI. Adopting it would also narrow `APS-200:213` (JSON/CBOR/protobuf) — a DQ-006 decision — without amending it.

*(Not listed as blockers, because they do not by themselves prevent the DQ-002 decision: N2, N4 and N5 from §D.1; the `APS-200:218` and `APS-300:73` TODOs; and the DRAFT status of the whole corpus.)*

RECOMMENDATION:
MODIFY CANDIDATE — the candidate is a viable basis for a Custodian ruling on Q2, but it must (a) state Q1 explicitly rather than inherit APS-200:58's silence, (b) be routed as an APS-300 amendment with an explicit Q3 precedence ruling rather than as an interpretation, and (c) drop or separately justify C4, which no source supports and which pre-empts DQ-006.

ARCHITECTURE OWNER DECISION:
REQUIRED

NO CODE CHANGED:
YES

NO NORMATIVE DOCS CHANGED:
YES
