# NB-021 — FROZEN BASELINE SEMANTICS AUDIT

**Date:** 2026-08-11
**Mode:** GOVERNANCE / EVIDENCE ONLY
**Status:** Evidence record. **No normative effect. No governance change. No implementation.**

---

## 1. Scope

Determine what the current Aura governance/specification corpus **actually states** about
FROZEN, and specifically whether a FROZEN v3.3 baseline may receive non-normative
engineering defect corrections without changing its normative identity.

This document does not solve the governance problem, does not choose a governance model,
does not invent missing authority, and does not propose any override, new lifecycle state,
or amendment process.

### Explicitly excluded from this document

- Any implementation change (including the P0 vector-length defect)
- Any specification, ADR, or status change
- Any inference from filenames, repository names, branch names, commit messages, current
  implementation behaviour, or general software-engineering practice

Where the corpus is silent, this document records **ABSENT**. Where the corpus contradicts
itself, it records **CONTRADICTED** and does not resolve the contradiction.

---

## 2. Method

1. Exhaustive case-insensitive grep for `frozen|freeze|freezing` across all tracked files
   in five repositories (`*.md`, `*.py`, `*.sh`, `*.txt`, `*.yml`, `*.json`, `*.sql`,
   `*.rs`, `*.toml`).
2. Full read of every document returned that contains a normative statement about FROZEN.
3. Git history inspection for Q9 (precedent) only, using commit SHAs and diffs as **facts
   about what happened**, never as normative authority.
4. Every finding is recorded with FILE / DOCUMENT ID / VERSION / STATUS / SECTION / QUOTE /
   FINDING / EVIDENCE CLASS.

**Evidence classes used:** `EXPLICIT`, `IMPLICIT`, `ABSENT`, `AMBIGUOUS`, `CONTRADICTED`.

### Interpretive rules applied

- A statement in a document whose own `Status` is DRAFT or PROPOSED is recorded with that
  status attached. Its status is reported, not discounted.
- A general rule that does not name FROZEN is not treated as governing FROZEN.
- Repository history is precedent-of-fact, not authority.
- The two words "frozen document" and "frozen instrument" are treated as **potentially
  distinct terms** until the corpus is shown to unify them. §4.3 records that it does not.

---

## 3. Evidence Sources

| Repository | Resolution | State |
|---|---|---|
| `AuraIDToken/aura-poc-a-core-v3.3` | local checkout | `main` @ `9c6a5d8` |
| `AuraIDToken/aura-specification` | read clone | HEAD (push 2026-08-10) |
| `aura-nomos/aura-specification` | local checkout | `main` @ `eb2a4ec` — contains only `README.md` (one line) and `.github/CODEOWNERS`; **no governance content**; contributes no evidence |
| `AuraIDToken/aura-guard-v1.3` | read clone | HEAD — **zero** occurrences of `frozen`/`freeze` in `src/`, `tests/`, `Cargo.toml`; contributes no evidence |
| `AuraIDToken/Aura-Conformance-Kit(s)` | read clones | HEAD — **zero** occurrences; contributes no evidence |

**Finding:** all FROZEN-related normative text exists in exactly two repositories, and they
use the term for two different subjects. This is the structural fact underlying NB-021.

### Primary documents

| # | File | Document ID | Version | Status |
|---|---|---|---|---|
| S1 | `aura-specification/constitution/AURA_CONSTITUTION.md` | AURA-CON-001 | 1.0 | **FROZEN** |
| S2 | `aura-specification/VERSIONING.md` | POL-VER-001 | 1.0-DRAFT | **DRAFT** |
| S3 | `aura-specification/GOVERNANCE.md` | GOV-001 | 1.0-DRAFT | **DRAFT** |
| S4 | `aura-specification/aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` | APS-000 | 1.0-DRAFT | **DRAFT** |
| S5 | `aura-specification/adrs/ADR-001_DOCUMENT_MODEL.md` | ADR-001 | — | **PROPOSED** |
| S6 | `aura-specification/CONTRIBUTING.md` | — | — | — |
| S7 | `aura-specification/CODE_OF_CONDUCT.md` | — | — | — |
| S8 | `aura-specification/.github/PULL_REQUEST_TEMPLATE/pull_request_template.md` | — | — | — |
| S9 | `aura-specification/releases/v0.1.0/DOCUMENT_STATUS.md` | — | v0.1.0 | — |
| S10 | `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md` | RI-PY | v3.3 | NOT CERTIFIED |
| C1 | `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` | — | 1.0 | MANDATORY / NON-OVERRIDABLE |
| C2 | `aura-poc-a-core-v3.3/ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` | — | — | — |
| C3 | `aura-poc-a-core-v3.3/README.md` | — | — | FROZEN / CANONICAL |
| C4 | `aura-poc-a-core-v3.3/docs/ops/OPS_PROTOCOL_CANONICAL.md` | — | — | — |
| C5 | `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md` | — | 1.0.0 | **FROZEN** |
| C6 | `aura-poc-a-core-v3.3/docs/mathematical_foundation.md` | — | — | **FROZEN** |
| C7 | `aura-poc-a-core-v3.3/docs/regulatory_compliance.md` | — | 1.0.0 | Frozen |
| C8 | `aura-poc-a-core-v3.3/RELEASE_CLOSURE_REPORT.md` | — | — | — |
| C9 | `aura-poc-a-core-v3.3/CHANGELOG.md` | — | — | FROZEN — MC-READY 2026 |
| C10 | `aura-poc-a-core-v3.3/AGENTS.md` | — | — | — |
| C11 | `aura-poc-a-core-v3.3/docs/GLOSSARY.md` | — | — | — |
| C12 | `aura-poc-a-core-v3.3/docs/LEGACY_PROTOCOL.md` | — | — | — |

---

## 4. Definition of FROZEN

### 4.1 Specification-corpus definition — applies to DOCUMENTS

> **FILE** `aura-specification/VERSIONING.md`
> **DOCUMENT ID** POL-VER-001 · **VERSION** 1.0-DRAFT · **STATUS** DRAFT
> **SECTION** §3 Document Status Lifecycle
>
> **QUOTE:**
> ```
> DRAFT → REVIEW → APPROVED → FROZEN
>                            ↘ DEPRECATED → ARCHIVED
> ```
> | Status | Meaning | Mutable? |
> |--------|---------|----------|
> | FROZEN | Immutable; content cannot change | No |
>
> **FINDING:** FROZEN is defined as a **document lifecycle status** meaning
> "Immutable; content cannot change", with mutability explicitly "No".
> **EVIDENCE CLASS:** EXPLICIT

---

> **FILE** `aura-specification/VERSIONING.md` · **SECTION** §4 Document Version Numbers
>
> **QUOTE:** "A FROZEN document **never receives a new version number**. A revision creates
> a new document (e.g., APS-200 v2.0-DRAFT)."
>
> **FINDING:** The corpus defines the mechanism for revising a FROZEN document: create a
> **new document**. The frozen artifact itself is never revised in place.
> **EVIDENCE CLASS:** EXPLICIT

---

> **FILE** `aura-specification/aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md`
> **DOCUMENT ID** APS-000 · **VERSION** 1.0-DRAFT · **STATUS** DRAFT
> **SECTION** §5 Document Status
>
> **QUOTE:** "| FROZEN | Immutable |"
>
> **FINDING:** FROZEN is equated with IMMUTABLE. No distinction is drawn between the two.
> **EVIDENCE CLASS:** EXPLICIT

---

> **FILE** `aura-specification/constitution/AURA_CONSTITUTION.md`
> **DOCUMENT ID** AURA-CON-001 · **VERSION** 1.0 · **STATUS** FROZEN
> **SECTION** Article XI — Amendment Procedure
>
> **QUOTE:** "Once a version is marked FROZEN, its content is immutable."
>
> **FINDING:** The highest-authority document in the specification corpus states
> immutability of frozen content unconditionally. Article XI's five-step amendment
> procedure produces a **new version**, per GOVERNANCE.md §5.3 step 6 ("New FROZEN version
> published").
> **EVIDENCE CLASS:** EXPLICIT

---

> **FILE** `aura-specification/constitution/AURA_CONSTITUTION.md` · **SECTION** Article VIII
>
> **QUOTE:** "AI systems MUST NOT approve changes to canonical documents or modify frozen
> documents."
>
> **FINDING:** An explicit, unconditional prohibition binding on AI systems specifically.
> This binds the present author.
> **EVIDENCE CLASS:** EXPLICIT

### 4.2 Implementation-corpus definition — applies to the INSTRUMENT

> **FILE** `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md`
> **VERSION** 1.0 · **STATUS** MANDATORY / NON-OVERRIDABLE · **SECTION** Preamble
>
> **QUOTE:** "This repository is a **FROZEN REGULATORY MEASUREMENT INSTRUMENT**. It is not a
> software product. It is not a service. It is not a platform. It is a **metrological
> system** …"
>
> **FINDING:** FROZEN here qualifies a *repository / instrument*, not a document status.
> The Decree **never defines FROZEN as a lifecycle status** and never states mutability
> rules for it. It instead enumerates permitted and prohibited changes (§4.4) and the
> identity consequence of change (§6).
> **EVIDENCE CLASS:** EXPLICIT (for the declaration) · **ABSENT** (for a status definition)

---

> **FILE** `aura-poc-a-core-v3.3/README.md` · **SECTION** "FROZEN REGULATORY MEASUREMENT INSTRUMENT"
>
> **QUOTE:** "**Status:** FROZEN / CANONICAL
> **Version:** v3.3 (Iron Core Correct)"
>
> **FINDING:** A status declaration by assertion. No transition record, no authority
> signature, no date, no bound artifact.
> **EVIDENCE CLASS:** EXPLICIT (declaration) · **ABSENT** (transition evidence)

### 4.3 The two definitions are never unified

**FINDING:** The specification corpus defines FROZEN **only** for documents. The
implementation corpus applies FROZEN **only** to an instrument/repository. Neither corpus
cites the other's definition. Cross-checked:

- `aura-specification` contains **zero** references to `CONSTITUTIONAL_DECREE`,
  `Iron Core`, or `v3.3 Iron Core` as a governed status.
- `aura-poc-a-core-v3.3` contains **zero** references to `POL-VER-001`, `VERSIONING.md`,
  `AURA-CON-001`, or `GOV-001`.

The only document that connects the two is an observation, not a rule:

> **FILE** `aura-specification/reference/RI-PY_AURA_POC_A_CORE.md`
> **DOCUMENT ID** RI-PY · **VERSION** v3.3 · **STATUS** NOT CERTIFIED
> **SECTION** Key Notes
>
> **QUOTE:** "Self-declared FROZEN (v3.3) — this creates a governance challenge as APS gaps
> require changes"
>
> **FINDING:** The specification corpus **itself records** that v3.3's frozen status is
> self-declared and that this creates an unresolved governance challenge. NB-021 is
> therefore a pre-existing, corpus-acknowledged open question, not a new one raised by this
> audit.
> **EVIDENCE CLASS:** EXPLICIT

### 4.4 What the implementation corpus explicitly permits

> **FILE** `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md`
> **SECTION** Article III — What You Must Not "Improve" → "What IS Permitted"
>
> **QUOTE:**
> ```
> 1. ✔ Fixing critical security vulnerabilities in changed lines
> 2. ✔ Correcting provable mathematical errors
> 3. ✔ Fixing violations of Articles I-V
> 4. ✔ Adding tests that validate constitutional compliance
> 5. ✔ Updating documentation to clarify existing behavior
> 6. ✔ Implementing explicitly authorized tasks (see .github/copilot-tasks.md)
> ```
>
> **FINDING:** A closed, enumerated permission list. Change to a frozen instrument is
> **explicitly contemplated and permitted** within these six categories.
> Note the scope qualifier on item 1: **"in changed lines"**.
> **EVIDENCE CLASS:** EXPLICIT

The same list is restated twice more, with the same qualifier:

> **FILE** `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` · **SECTION** §2.1.2 Authorize Tasks
> **QUOTE:** "✔ Fixing critical security vulnerabilities in changed lines"
>
> **FILE** `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` · **SECTION** §3.2.3 Entropy Budget Management
> **QUOTE:** "**Acceptable Changes:** Fix security vulnerabilities in changed code · Correct
> mathematical errors · Enforce constitutional requirements · Implement authorized tasks"
>
> **FINDING:** Three independent occurrences, consistently scoping the security-fix
> permission to **changed lines / changed code**. The corpus nowhere grants permission to
> fix a security defect in **unchanged, already-frozen** code.
> **EVIDENCE CLASS:** EXPLICIT (scope) · **ABSENT** (permission for unchanged code)

### 4.5 The bit-identity gate

> **FILE** `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` · **SECTION** §4.1 Entropy Risk Assessment
>
> **QUOTE:**
> ```
> 1. Does this change fix a critical issue?
>    - Security vulnerability in changed code? → Acceptable
>    - Mathematical error? → Acceptable
>    - Constitutional violation? → Acceptable
>    - Regulatory non-compliance? → Acceptable
>    - "Improvement" or "optimization"? → REJECTED
>
> 2. Does this change preserve bit-identity?
>    - YES → Proceed to next question
>    - NO → REJECTED
>    - UNCERTAIN → REJECTED (Constitutional Decree Article IV)
> ```
>
> **FINDING — CRITICAL:** Gate 1 and Gate 2 are **sequential and conjunctive**. A change
> must pass *both*. But any correction of a defect that produces a wrong output
> **necessarily changes output**, and therefore cannot "preserve bit-identity". Applied
> literally, Gate 2 rejects the very class of change Gate 1 declares acceptable.
>
> This is not an edge case: it is the governing decision framework's response to every
> correctness fix. The two gates are, as written, mutually defeating for defect correction.
> **EVIDENCE CLASS:** CONTRADICTED

---

## 5. Lifecycle Semantics

| Transition | Specification corpus (documents) | Implementation corpus (instrument) |
|---|---|---|
| **Entry into FROZEN** | **EXPLICIT** — `APPROVED → FROZEN`: "Explicit freeze decision by Chief Architect; requires Amendment Procedure (Constitution Article XI)" (VERSIONING §3) | **ABSENT** — no defined transition. Status is asserted in README/DECREE/CHANGELOG headers. `RELEASE_CLOSURE_REPORT.md` states "APPROVE RELEASE … approved for frozen release", which is a recommendation in a report, not a recorded transition. |
| **Exit from FROZEN** | **ABSENT** — the lifecycle diagram has no arrow leaving FROZEN except to DEPRECATED, which is not a return to mutability | **ABSENT** |
| **Amendment** | **EXPLICIT** — Constitution Art. XI (RFC → Architecture Review → impact analysis → dependent updates → Chief Architect approval); GOVERNANCE §5.3 step 6: "New FROZEN version published" | **PARTIAL** — Decree Art. V and ROLE §2.1.1 permit the Custodian to modify constitutional constants "with full mathematical justification, regulatory impact assessment, creation of new instrument version (not update), comprehensive documentation" |
| **Correction** | **EXPLICIT but PROPOSED** — see INV-DOC-008 below | **EXPLICIT** — Decree Art. III six-item list (§4.4 above) |
| **Supersession** | **EXPLICIT** — `APPROVED/FROZEN → DEPRECATED`: "Requires new version of superseding document and formal deprecation notice" (VERSIONING §3) | **PARTIAL** — "The old instrument remains sealed and archived" (ROLE §2.1.1) |
| **Version increment** | **EXPLICIT** — "A FROZEN document never receives a new version number" (VERSIONING §4) | **EXPLICIT** — "Any change to core logic creates a **NEW INSTRUMENT**, not a new version" (Decree Art. VIII; ROLE §3.2.4) |
| **Replacement** | **EXPLICIT** — "A revision creates a new document" (VERSIONING §4) | **EXPLICIT** — v4.x = "New instrument (requires new audit)" (README §8; OPS §2) |

### 5.1 INV-DOC-008 — the closest thing to a correction rule, and its status

> **FILE** `aura-specification/adrs/ADR-001_DOCUMENT_MODEL.md`
> **DOCUMENT ID** ADR-001 · **STATUS** **PROPOSED** · **SECTION** Repository Invariants
>
> **QUOTE:** "INV-DOC-008: Frozen artifacts SHALL NOT be modified; corrections require a new
> superseding artifact and an explicit link to the correction."
>
> **FINDING:** This is the **only** statement in the entire corpus that uses the word
> "corrections" in direct connection with frozen artifacts. It states that corrections are
> made by superseding artifact, never in place.
>
> **However, it is not in force.** The document's own closing section states: "This ADR is
> **PROPOSED** and requires explicit approval by the Protocol Custodian. Approval is
> recorded by adding an `Accepted-by: <Protocol Custodian>` line and merging this ADR into
> the repository's canonical branch." No `Accepted-by:` line exists in the file. The
> `adrs/README.md` index does not list it. `releases/v0.1.0/DOCUMENT_STATUS.md` does not
> list it.
> **EVIDENCE CLASS:** EXPLICIT text · **NOT IN FORCE** by its own terms

### 5.2 An additional state exists: SEALED — and it has not been reached

> **FILE** `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` · **SECTION** Article VIII — Sealing Protocol
>
> **QUOTE:**
> ```
> When this instrument is sealed:
> 1. ✔ All code frozen
> 2. ✔ SHA-256 checksum computed
> 3. ✔ Archived to M-DISC (physical media)
> 4. ✔ Bit-verified
> 5. ❌ NO further changes permitted
> ```

> **FILE** `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` · **SECTION** §6.5 Sealing Operations
>
> **QUOTE:** "**Post-Seal:** Archive receives notation: `v3.3-SEALED` · No further changes
> permitted to this version · Any future work creates NEW INSTRUMENT (v4.0)"

> **FILE** `docs/ops/OPS_PROTOCOL_CANONICAL.md` · **SECTION** §4.1 Immutability
>
> **QUOTE:** "This repository represents a **finished instrument**. **Once sealed**, the
> artifact is immutable."

> **FINDING — MATERIAL:** The implementation corpus conditions **absolute** immutability on
> **SEALING**, not on FROZEN. FROZEN and SEALED are distinct states, and only SEALED carries
> "NO further changes permitted".
>
> **Sealing has not occurred.** Verified:
> - `git tag -l` → **no tags**
> - no `releases/` directory
> - no `v3.3-SEALED` notation anywhere in the repository
> - no custodianship certificate, no M-DISC record
> - `docs/LEGACY_PROTOCOL.md:78` still contains the unfilled placeholder:
>   "SHA-256 checksum: `[COMPUTED_AT_SEALING_v3.3]`"
> - `RELEASE_CLOSURE_REPORT.md` lists sealing as a **future** 7-step procedure
>
> **EVIDENCE CLASS:** EXPLICIT (the distinction) · EXPLICIT (sealing not performed)

This is the single strongest piece of evidence *against* reading FROZEN as absolute
immutability in the implementation corpus — and simultaneously it does **not** establish
that FROZEN permits correction. It establishes only that the corpus reserves a stricter
state for that purpose and has not entered it.

---

## 6. Identity Semantics

The question "without changing the normative identity" presupposes that v3.3 **has** a
recorded normative identity. It does not.

| Identity dimension | Corpus statement | Actual state |
|---|---|---|
| **Version** | "v3.3 Iron Core refers to a frozen instrument, not a software version" (README §11.4) | Declared in prose headers only |
| **Document ID** | v3.3 has no document ID; it is not an APS, SPEC, or ARC | ABSENT |
| **Commit SHA** | ADR-001 (PROPOSED) would record "commit_sha: (commit SHA at freeze/acceptance)" | **ABSENT** — never recorded for v3.3 |
| **Artifact identity** | GLOSSARY: "The cryptographic identity of each frozen protocol version is defined by hashes and archival artifacts (e.g., M-DISC)." | **ABSENT** — no hash, no M-DISC, placeholder unfilled |
| **Release identity** | VERSIONING §9 requires `releases/vX.Y.Z/` + RELEASE_NOTES + CONFORMANCE_REPORT + DOCUMENT_STATUS + SHA-256 checksums | **ABSENT** in the implementation repository (that rule governs `aura-specification` only, which does have `releases/v0.1.0/`) |
| **Provenance identity** | AD-CA-010 (SPEC-002 §6) — "Commit/execution provenance binding schema" | **UNRESOLVED** |
| **Package version** | `pyproject.toml` declares `version = "0.1.0"` | RELEASE_CLOSURE_REPORT §A.5 records this as a known inconsistency, "**Noted as informational; not corrected.**" |

> **FINDING — MATERIAL:** v3.3 has **no bound, verifiable identity**. There is no tag, no
> checksum, no release record, no SHA binding. Per the corpus's own definition
> (GLOSSARY: cryptographic identity is "defined by hashes and archival artifacts"), v3.3's
> identity is **undefined**.
>
> Consequently the question "can a correction be made *without changing the normative
> identity*" **cannot be evaluated against the corpus**: there is no recorded identity for
> a correction to preserve or destroy.
> **EVIDENCE CLASS:** ABSENT

### 6.1 What the corpus says the identity consequence of a fix would be

> **FILE** `aura-poc-a-core-v3.3/README.md` · **SECTION** §11 Naming and Positioning Rules (Canonical), rule 4
>
> **QUOTE:** "**v3.3 Iron Core refers to a frozen instrument**, not a software version.
> **Bug fixes or modifications require a new lineage.**"
>
> **FINDING — DIRECTLY ON POINT.** This is the **only** sentence in the corpus that uses the
> phrase "bug fixes" together with an identity consequence. It states that a bug fix
> requires a **new lineage** — i.e. the corrected artifact is **not** v3.3.
> **EVIDENCE CLASS:** EXPLICIT

> **FILE** `aura-poc-a-core-v3.3/CONSTITUTIONAL_DECREE.md` · **SECTION** Article VIII — Versioning Philosophy
>
> **QUOTE:** "Any change to core logic creates a **NEW INSTRUMENT**, not a new version."
>
> **FINDING:** Same consequence, scoped to "core logic".
> **EVIDENCE CLASS:** EXPLICIT

> **FILE** `aura-poc-a-core-v3.3/README.md` · **SECTION** §7 and §8
>
> **QUOTE:** "Any modification creates a **new instrument**, not a new version." /
> "Any change creates a new instrument, not an update."
>
> **FINDING:** Same consequence, **unscoped** — "any modification", "any change".
> **EVIDENCE CLASS:** EXPLICIT
>
> **CONFLICT:** README §7/§8 ("any change") is broader than Decree Art. VIII ("any change to
> core logic"). Under README, a documentation fix creates a new instrument; under the Decree
> it does not. The Decree's own Article VII expressly permits documentation changes. The
> scope of "change" is therefore **AMBIGUOUS**.

### 6.2 The unresolvable pairing

Placing §4.4 beside §6.1 yields the core of NB-021:

| Statement | Source | Class |
|---|---|---|
| Correcting provable mathematical errors is **permitted** | Decree Art. III | EXPLICIT |
| Fixing critical security vulnerabilities **in changed lines** is permitted | Decree Art. III | EXPLICIT |
| A change that does not preserve bit-identity is **REJECTED** | ROLE §4.1 Gate 2 | EXPLICIT |
| Bug fixes **require a new lineage** | README §11.4 | EXPLICIT |
| Any change to core logic creates a **new instrument** | Decree Art. VIII | EXPLICIT |

If every permitted fix creates a new instrument, then Article III's permission can never be
exercised *on v3.3* — it can only ever be exercised *while creating v4*. Read that way,
Article III is inoperative for the artifact it governs. Read the other way — that permitted
fixes stay within v3.3 — README §11.4 and Article VIII are contradicted.

**The corpus supports both readings and selects neither.** This audit does not select
either.

---

## 7. Correction vs Amendment

The task requires seven categories be kept distinct. Corpus coverage:

| # | Category | Corpus treatment | Class |
|---|---|---|---|
| 1 | **Normative amendment** | Fully defined: Constitution Art. XI; GOVERNANCE §5.2/§5.3; VERSIONING §3–§4. Produces a **new version / new document**. | EXPLICIT |
| 2 | **Specification correction** | For non-frozen documents: GOVERNANCE §5.1 PATCH lane. For FROZEN documents: prohibited in place (CONTRIBUTING, PR template, VERSIONING §3); mechanism is a superseding artifact (INV-DOC-008, PROPOSED). | EXPLICIT / PROPOSED |
| 3 | **Documentation correction** | Explicitly permitted: Decree Art. VII ("Documentation changes are permitted when they clarify existing behavior…"); Art. III item 5. | EXPLICIT |
| 4 | **Implementation defect correction** | Permitted **only** within Decree Art. III's six categories. "Defect" as a general category **does not appear**. | PARTIAL |
| 5 | **Security defect correction** | Permitted **only** "in changed lines / changed code" (three consistent occurrences). No permission for unchanged frozen code. | EXPLICIT (scoped) |
| 6 | **Test-only correction** | Explicitly permitted, with conditions: Decree Art. VII Testing; Art. III item 4. | EXPLICIT |
| 7 | **Refactoring with no intended behavioural change** | Explicitly **PROHIBITED**: Decree Art. I §9 "NO CONVENIENCE ABSTRACTIONS — ❌ No 'helpful' refactoring"; Art. III prohibited list items 5–6; Art. I §10 "NO UNAUTHORIZED CHANGES — ❌ No refactoring without explicit authorization"; `copilot-guardrails.md` "❌ Refactoring without explicit task". | EXPLICIT |

> **FINDING — MATERIAL:** The corpus does **not** recognize "non-normative engineering defect
> correction" as a category. It recognizes four justifications (security vulnerability in
> changed lines, provable mathematical error, constitutional violation, authorized task) and
> nothing else. A defect that is none of those four has **no permission pathway**.
> **EVIDENCE CLASS:** ABSENT

---

## 8. Case Analysis A–F

### CASE A — Typographical / documentation-only correction

**STATUS: PERMITTED**

**EVIDENCE:**
> `CONSTITUTIONAL_DECREE.md` Article VII — Special Permissions → Documentation:
> "Documentation changes are permitted when they: ✔ Clarify existing behavior ✔ Improve
> constitutional compliance understanding ✔ Add regulatory mapping ❌ Do NOT advocate for
> forbidden changes"

> `CONSTITUTIONAL_DECREE.md` Article III → What IS Permitted, item 5:
> "✔ Updating documentation to clarify existing behavior"

**CLASS:** EXPLICIT

**Boundary recorded:** this permission is granted by the *implementation* corpus for the
implementation repository's documentation. It does **not** extend to documents marked
FROZEN in the specification corpus, where `CONTRIBUTING.md` states "Do not modify FROZEN
documents" and the PR template requires "No FROZEN documents modified". For a FROZEN APS,
see Q4 in §12.

---

### CASE B — Security defect correction in implementation

**STATUS: INDETERMINATE**

**EVIDENCE FOR:**
> `CONSTITUTIONAL_DECREE.md` Article III: "✔ Fixing critical security vulnerabilities in
> changed lines"
> `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §2.1.2, §3.2.3, §4.1: same permission, same scope

**EVIDENCE AGAINST / LIMITING:**
1. **Scope qualifier.** All three occurrences restrict the permission to "**changed
   lines**" / "**changed code**". A pre-existing defect in frozen, unchanged code is not
   within the quoted scope. The corpus grants no permission for it. **CLASS: ABSENT**
2. **Bit-identity gate.** ROLE §4.1 Gate 2: "Does this change preserve bit-identity? …
   NO → REJECTED. UNCERTAIN → REJECTED." A security fix that alters behaviour fails Gate 2.
   **CLASS: CONTRADICTED**
3. **Identity consequence.** README §11.4: "Bug fixes or modifications require a new
   lineage." **CLASS: EXPLICIT**
4. **Authority.** Decree Art. X: "Custodian Signature: [Required for core/ changes]";
   AGENTS.md rule 13: "Human approval is required before merging protocol-affecting
   changes." No such signature exists for any prospective fix. **CLASS: EXPLICIT**

**FINDING:** The corpus permits security fixes in a defined scope that does not cover
already-frozen unchanged code, subjects any fix to a gate that rejects behaviour changes,
and assigns the resulting artifact a new lineage. The three cannot be satisfied
simultaneously. INDETERMINATE.

---

### CASE C — Correctness defect correction in implementation, specification unchanged

**STATUS: INDETERMINATE**

**EVIDENCE FOR:**
> `CONSTITUTIONAL_DECREE.md` Article III: "✔ Correcting provable mathematical errors"
> `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §3.2.3: "**Acceptable Changes:** … Correct
> mathematical errors"

**EVIDENCE AGAINST / LIMITING:**
1. Whether a given defect **is** a "provable mathematical error" is a determination the
   corpus assigns to the Custodian (ROLE §2.2.1: "The Custodian has **FINAL AUTHORITY**
   over: All changes to `core/` directory"), not to an implementer or an AI system.
   **CLASS: EXPLICIT**
2. Gate 2 (bit-identity) rejects it, as in CASE B. **CLASS: CONTRADICTED**
3. README §11.4 assigns a new lineage. **CLASS: EXPLICIT**
4. Decree Art. IV: "If you are UNSURE whether a change: Violates determinism / Breaks
   bit-identity … You **MUST REFUSE** to make the change." **CLASS: EXPLICIT**

**FINDING:** Same structural deadlock as CASE B. Additionally, the corpus places the
threshold determination ("is this a provable mathematical error?") outside engineering
authority. INDETERMINATE.

---

### CASE D — Correction to a test exposing an existing invariant

**STATUS: PERMITTED**

**EVIDENCE:**
> `CONSTITUTIONAL_DECREE.md` Article VII — Special Permissions → Testing:
> "New tests are permitted when they: ✔ Validate constitutional compliance ✔ Enforce
> bit-identity ✔ Verify regulatory requirements ❌ Do NOT introduce non-deterministic
> behavior"

> `CONSTITUTIONAL_DECREE.md` Article III → What IS Permitted, item 4:
> "✔ Adding tests that validate constitutional compliance"

**CLASS:** EXPLICIT

**Boundary recorded:**
> `AGENTS.md` canonical rule 10: "Tests must not be weakened merely to make implementation
> pass."

A test that *records existing behaviour* and a test that *weakens an assertion* are
distinct; only the former is within Article VII. Note also that adding a test is not a
"change to core logic" under Decree Art. VIII, so no new-instrument consequence is
triggered by the Decree — though README §8's unscoped "Any change creates a new instrument"
would say otherwise (see §6.1 conflict, AMBIGUOUS).

---

### CASE E — Addition of a regression test whose expected value depends on an unresolved normative decision

**STATUS: PROHIBITED**

**EVIDENCE:**
1. > `CONSTITUTIONAL_DECREE.md` Article VII → Testing: permission is **conditional** on the
   > test validating constitutional compliance, enforcing bit-identity, or verifying a
   > regulatory requirement. A test whose expected value is normatively undetermined does
   > none of the three. **CLASS: EXPLICIT (condition not met)**
2. > `aura-specification/specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` §6:
   > "**No candidate choice listed in this table constitutes a recommendation, preference,
   > default, or implied architectural decision.**" **CLASS: EXPLICIT**
3. > `AGENTS.md` canonical rule 2: "Agents must not silently change protocol semantics."
   > `AGENTS.md` canonical rule 3: "Agents must distinguish AS-IS from TO-BE."
   > **CLASS: EXPLICIT**
4. > `AURA_CONSTITUTION.md` Article IV Principle 8: "**Explicit over Implicit.** All
   > behaviour MUST be explicitly specified. Implicit behaviour is undefined behaviour."
   > **CLASS: EXPLICIT**

**FINDING:** Encoding an unresolved normative value as a test expectation would constitute
selecting that value. This is prohibited by four independent sources across both corpora.
This is the one case in A–F where the corpus is unanimous.

---

### CASE F — Change to the specification itself because the existing specification is mathematically incorrect

**STATUS: INDETERMINATE (CONTRADICTED)**

**EVIDENCE — implementation corpus says CORRECT THE SPECIFICATION:**
> **FILE** `aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md`
> **VERSION** 1.0.0 · **STATUS** FROZEN — MC-READY 2026 · **SECTION** Constitutional Note
>
> **QUOTE:** "Implementation is the source of truth. If this document conflicts with the
> implementation, the implementation governs and **this document must be corrected**."
>
> **FINDING:** A document that declares itself FROZEN contains an explicit, mandatory
> self-correction clause, and subordinates itself to the implementation.
> **CLASS: EXPLICIT — and CONTRADICTS its own FROZEN status**

**EVIDENCE — specification corpus says THE OPPOSITE:**
> `AURA_CONSTITUTION.md` Article IV Principle 1: "**Specification First.** Architecture
> precedes implementation. Implementation follows specification."
> `AURA_CONSTITUTION.md` Article V: canonical hierarchy places Implementation **last**;
> "A higher-level document has authority over a lower-level document in all cases of
> conflict."
> `CONTRIBUTING.md` Core Rule: "**Specification is the source of truth. Implementation
> follows specification.** Never propose changes to specifications to match existing
> implementations."
> **CLASS: EXPLICIT**

**FINDING:** The two corpora state **exactly opposite** conflict-resolution rules. One says
implementation governs and the spec must be corrected; the other says the spec governs and
must never be changed to match implementation. Both are explicit. Neither cites the other.
INDETERMINATE.

---

## 9. Repository Precedent

Recorded as **facts about what happened**. Per instruction, implementation behaviour is
**not** treated as normative precedent; these entries establish only that the corpus's
stated rules have been departed from without a recorded authority.

### P-1 — A document declaring itself FROZEN and immutable was modified in place

| Field | Value |
|---|---|
| **Commit SHA** | `4ced103` (`4ced1032c7598275a5cbba1f396e444c597e31e2`), 2026-08-09 |
| **Message** | "implement approved CRs: CR-001 Art.5 fail-closed, CR-003/005 Layer 0 separation, E2 docs" |
| **File** | `docs/mathematical_foundation.md` |
| **Status before** | `**FROZEN** — Regulatory Audit Phase (MC-READY 2026)` / "Formula and principles are immutable pending regulatory review." |
| **Status after** | **unchanged** — identical FROZEN text retained |
| **Change** | The normative formula section was rewritten: `ARI = 0.3 × SI + 0.7 × SA - Penalties` → `RAW_ARI = 0.3 × SI + 0.7 × SA`, plus a new "Layer 2 Formula (Adjusted ARI)" section and a new "Layer Separation" table |
| **Version increment** | **none** |
| **Superseding document** | **none** |
| **Stated rationale** | commit message only ("implement approved CRs"); no RFC, no ADR, no custodian signature in the commit |

**FINDING:** A document whose own text reads "immutable" received a normative content change
in place, retaining its FROZEN marker. This is directly contrary to
`RELEASE_CLOSURE_REPORT.md` Part B.1, which recorded that document's change policy as
"**Changes create new instrument**".
**EVIDENCE CLASS:** CONTRADICTED

### P-2 — Implementation behaviour was changed after the declared freeze

| Field | Value |
|---|---|
| **Commit SHA** | `4ced103`, 2026-08-09 |
| **File** | `compliance/policy.py` |
| **Before** | `assert target_type == "MACHINE_ACCOUNT", "CRITICAL: Human scoring is strictly prohibited."` |
| **After** | `if target_type != "MACHINE_ACCOUNT": raise ValueError("CRITICAL: Human scoring is strictly prohibited.")` |
| **Observable effect** | exception type changes `AssertionError` → `ValueError`; behaviour under `python -O` changes from *no check* to *check enforced* |
| **Instrument version after** | **v3.3** — unchanged |
| **New lineage created** | **no** |

**FINDING:** An observable behaviour change to the frozen instrument, retaining the v3.3
label, contrary to README §11.4 ("Bug fixes or modifications require a new lineage").

**Compounding fact:** `CONSTITUTIONAL_DECREE.md` Article IX still reads:
> "**Validation:** `assert target_type == "MACHINE_ACCOUNT"` — This assertion is
> **MANDATORY** in every evaluation path."

The change removed the mandatory assertion the Decree still requires. The Decree has not
been amended (last modified `7931c9f`, 2026-01-24). The implementation and the
non-overridable governing document are now in direct conflict.
**EVIDENCE CLASS:** CONTRADICTED

### P-3 — Layer 0 public API changed after the declared freeze

| Field | Value |
|---|---|
| **Commit SHA** | `4ced103`, 2026-08-09 |
| **File** | `core/evaluator.py` |
| **Change** | `evaluate(self, agent_id, vector, valid_schema, penalty: int = 0)` → `evaluate(self, agent_id, vector, valid_schema)`; penalty subtraction removed from Layer 0 |
| **Scope** | `core/` — i.e. "core logic" in the sense of Decree Art. VIII |
| **Instrument version after** | **v3.3** — unchanged |

**FINDING:** A breaking signature change and a behaviour change to `core/`, which Decree
Art. VIII states "creates a **NEW INSTRUMENT**, not a new version". No new instrument was
created.
**EVIDENCE CLASS:** CONTRADICTED

### P-4 — Documentation corrections under FROZEN status (consistent with the rules)

| Field | Value |
|---|---|
| **Commits** | `a81619c`, `0bbf86a`, `da22123` (2026-07-24), `93f51c8` (2026-07-25) |
| **Messages** | "CORE-007: Documentation corrections…", "CORE-007: Fix documentation defects — sentinel value and stale policy reference", "CORE-007: Fix test count accuracy…", "docs: address review thread inconsistencies" |
| **Recorded rationale** | `CHANGELOG.md` records these under a stated policy: "Each entry in this log documents a completed task that was authorized before execution. No entry represents a new feature or a change to the constitutional constants." |

**FINDING:** Documentation-only corrections were performed under FROZEN status **with a
recorded authorization claim**. This is consistent with Decree Art. VII and Art. III item 5,
and supports CASE A.
**EVIDENCE CLASS:** EXPLICIT (consistent precedent)

### P-5 — No precedent exists for a FROZEN *specification-corpus* document being corrected

Verified: `releases/v0.1.0/DOCUMENT_STATUS.md` records exactly **one** FROZEN document in
`aura-specification` — `AURA-CON-001` v1.0. Its git history shows no post-freeze content
modification. **No APS document is FROZEN**; all are `1.0-DRAFT` / DRAFT.

**FINDING:** Q4 and Q5 concern a state that does not currently exist for any APS.
**EVIDENCE CLASS:** ABSENT (no instance)

---

## 10. Contradictions / Ambiguities

| # | Contradiction | Source A | Source B | Class |
|---|---|---|---|---|
| X-1 | Defect fixes are permitted **vs** any change that does not preserve bit-identity is rejected | Decree Art. III; ROLE §4.1 Gate 1 | ROLE §4.1 Gate 2 | CONTRADICTED |
| X-2 | Fixes permitted on v3.3 **vs** bug fixes require a new lineage | Decree Art. III | README §11.4; Decree Art. VIII | CONTRADICTED |
| X-3 | "Any change" creates a new instrument **vs** documentation and test changes are expressly permitted | README §7, §8; OPS §2 | Decree Art. VII | AMBIGUOUS (scope of "change") |
| X-4 | FROZEN = immutable **vs** immutability begins at SEALING | VERSIONING §3; APS-000 §5; Constitution Art. XI | OPS §4.1; Decree Art. VIII; ROLE §6.5 | CONTRADICTED |
| X-5 | Implementation governs and the spec must be corrected **vs** specification governs and must never follow implementation | `AUDIT_LAYER_SPEC.md` Constitutional Note | Constitution Art. IV P1, Art. V; CONTRIBUTING Core Rule | CONTRADICTED |
| X-6 | "Do not modify FROZEN documents" **vs** modifying frozen documents *without the Amendment Procedure* is what is unacceptable | CONTRIBUTING; PR template | CODE_OF_CONDUCT ("Modifying frozen or approved documents **without the Amendment Procedure**") | AMBIGUOUS |
| X-7 | PATCH lane permits typo/clarification fixes with no status qualification **vs** FROZEN is "Mutable? No" | GOVERNANCE §5.1; CONTRIBUTING type table | VERSIONING §3 | AMBIGUOUS |
| X-8 | `assert target_type == "MACHINE_ACCOUNT"` is MANDATORY **vs** no compliance enforcement may rely on Python `assert` | Decree Art. IX | AGENTS.md rule 4; implemented state since `4ced103` | CONTRADICTED |
| X-9 | Immutable components "require formal review + compliance re-assessment" **vs** immutable | `docs/regulatory_compliance.md` §Frozen Status | VERSIONING §3; Constitution Art. XI | AMBIGUOUS |
| X-10 | A FROZEN document "never receives a new version number" **vs** "A revision creates a new document (e.g., APS-200 v2.0-DRAFT)" — the example reuses the same document ID at a new version | VERSIONING §4 sentence 1 | VERSIONING §4 sentence 2 | AMBIGUOUS |
| X-11 | Three distinct documents carry the identifier `ADR-001`: `adrs/ADR-001_REPOSITORY_STRUCTURE.md` (ACCEPTED), `adrs/ADR-001_DOCUMENT_MODEL.md` (PROPOSED), `docs/adr/001-document-model.md` (DRAFT) | — | APS-000 §4 "Identifiers MUST NOT be reused"; VERSIONING §8; INV-DOC-005 | CONTRADICTED |

---

## 11. Evidence Gaps

| # | Gap | Class |
|---|---|---|
| G-1 | No definition of FROZEN that applies to an **implementation**. The specification corpus defines it for documents only. | ABSENT |
| G-2 | No defined transition **into** FROZEN for the v3.3 instrument. Status is asserted, not recorded. | ABSENT |
| G-3 | No defined transition **out of** FROZEN for anything. | ABSENT |
| G-4 | No recorded identity for v3.3: no tag, no SHA-256, no release record, no M-DISC artifact. `docs/LEGACY_PROTOCOL.md:78` still reads `[COMPUTED_AT_SEALING_v3.3]`. | ABSENT |
| G-5 | No definition of "normative identity" anywhere in either corpus. | ABSENT |
| G-6 | No category "non-normative defect correction". Only four justifications exist (§7). | ABSENT |
| G-7 | No permission for security fixes in **unchanged** frozen code — all three occurrences say "in changed lines / changed code". | ABSENT |
| G-8 | No cross-reference between the two governance corpora in either direction. | ABSENT |
| G-9 | INV-DOC-008, the only correction rule for frozen artifacts, is in a **PROPOSED** ADR with no `Accepted-by:` line. | NOT IN FORCE |
| G-10 | The `doc/ci/frozen-check` job specified in ADR-001 to "prevent direct modification of files marked FROZEN" **does not exist** in either repository's CI. | ABSENT |
| G-11 | No record of any custodian authorization for the post-freeze changes in P-1 through P-3 — no RFC, no ADR, no signed attestation, despite Decree Art. X requiring "Custodian Signature: [Required for core/ changes]". | ABSENT |
| G-12 | The documents that *define* FROZEN in the specification corpus (VERSIONING.md POL-VER-001, GOVERNANCE.md GOV-001, APS-000) are themselves **1.0-DRAFT**, i.e. by their own table "Under active authoring; may change freely". | AMBIGUOUS |

---

## 12. NB-021 Verdict

### Q1 — Where is FROZEN formally defined?

Two independent definitions, for two different subjects, never unified. Full citations in
§4. Summary:

- **Documents:** `VERSIONING.md` (POL-VER-001, 1.0-DRAFT) §3 — "Immutable; content cannot
  change", Mutable? "No"; §4 — never receives a new version number. Reinforced by APS-000
  §5 ("FROZEN | Immutable") and AURA-CON-001 Article XI ("Once a version is marked FROZEN,
  its content is immutable").
- **Instrument:** `CONSTITUTIONAL_DECREE.md` Preamble and `README.md` — declared as a
  status of the repository, with **no mutability rule**, only a permitted-change list
  (Art. III) and an identity consequence (Art. VIII).

**CLASS:** EXPLICIT for documents · ABSENT for implementations.

### Q2 — Lifecycle transitions

Tabulated in §5. Entry (documents) EXPLICIT; entry (instrument) ABSENT; exit ABSENT for
both; amendment EXPLICIT; correction EXPLICIT-but-PROPOSED (documents) / EXPLICIT-but-
enumerated (instrument); supersession EXPLICIT; version increment EXPLICIT; replacement
EXPLICIT. A further state, **SEALED**, exists in the implementation corpus and **has not
been entered** (§5.2).

### Q3 — FROZEN vs IMMUTABLE vs APPROVED vs RELEASED vs VERSIONED

| Pair | Distinguished? | Evidence |
|---|---|---|
| FROZEN vs APPROVED | **YES** | VERSIONING §3: APPROVED is mutable "Via RFC/ADR only"; FROZEN is "No" |
| FROZEN vs IMMUTABLE | **NO — equated** | APS-000 §5 "FROZEN \| Immutable"; VERSIONING §3 "Immutable; content cannot change". **But contradicted** by OPS §4.1 "Once **sealed**, the artifact is immutable" |
| FROZEN vs RELEASED | **NOT ESTABLISHED** | RELEASED is not a document status. VERSIONING §9 defines release artifacts; no relation to FROZEN is stated |
| FROZEN vs VERSIONED | **NOT ESTABLISHED** | "Version Everything" is a principle (Constitution Art. IV P9), not a status |
| FROZEN vs **SEALED** | **YES — EXPLICIT** | Decree Art. VIII; ROLE §6.5 (`v3.3-SEALED`); OPS §4.1. Only SEALED carries "NO further changes permitted" |

### Q4 — Can an APS marked FROZEN receive a typo/documentation correction?

**NO** — for the document in place.

**EVIDENCE:** `CONTRIBUTING.md` What NOT to Do: "Do not modify FROZEN documents";
PR template checklist: "- [ ] No FROZEN documents modified"; `VERSIONING.md` §3: Mutable?
"No"; Constitution Article XI. The defined mechanism is a new document (VERSIONING §4).

**Recorded qualifications:** (a) **no APS is currently FROZEN** — all are DRAFT per
`releases/v0.1.0/DOCUMENT_STATUS.md`, so this is a rule without a present instance;
(b) contradicted in part by X-6 (CODE_OF_CONDUCT implies frozen docs may be modified *with*
the Amendment Procedure) and X-7 (GOVERNANCE §5.1's PATCH lane is not status-qualified).

### Q5 — Can an APS marked FROZEN receive a normative correction?

**NO.**

**EVIDENCE:** Constitution Article XI: "Once a version is marked FROZEN, its content is
immutable." `VERSIONING.md` §4: "A revision creates a new document." `GOVERNANCE.md` §5.3
step 6: "New FROZEN version published." Consistent across three sources.
**CLASS:** EXPLICIT

### Q6 — Can an implementation corresponding to a FROZEN specification receive a non-normative bug/security fix?

**INDETERMINATE.**

**EVIDENCE FOR:** Decree Art. III's six-item permitted list; ROLE §2.1.2, §3.2.3, §4.1
Gate 1. All EXPLICIT.

**EVIDENCE AGAINST:**
- ROLE §4.1 Gate 2 rejects any change that does not preserve bit-identity — which every
  behavioural correction is (CONTRADICTED, X-1).
- The security-fix permission is scoped to "changed lines / changed code" in all three
  occurrences; unchanged frozen code is outside it (ABSENT, G-7).
- "Non-normative defect correction" is not a recognized category (ABSENT, G-6).
- Decree Art. IV: "If you are UNSURE … You MUST REFUSE to make the change" (EXPLICIT).
- Custodian signature is required for `core/` changes and none exists (ABSENT, G-11).

### Q7 — Can tests be changed or expanded against a FROZEN baseline?

**YES — conditionally.**

**EVIDENCE:** Decree Art. VII → Testing: "New tests are permitted when they: ✔ Validate
constitutional compliance ✔ Enforce bit-identity ✔ Verify regulatory requirements ❌ Do NOT
introduce non-deterministic behavior"; Art. III item 4. **CLASS: EXPLICIT**

**Required distinction:**
- **Tests that merely expose existing behaviour** → PERMITTED (CASE D). Within Art. VII's
  three conditions; not a change to core logic under Art. VIII.
- **Tests that encode a new normative expected value** → PROHIBITED (CASE E). Art. VII's
  conditions are not met, and four independent sources forbid selecting an unresolved value
  (§8 CASE E).

**Boundary:** AGENTS.md rule 10 — "Tests must not be weakened merely to make implementation
pass."

### Q8 — Does the corpus define a mechanism for "defect correction without normative change"?

# DEFECT-CORRECTION MECHANISM — ABSENT

The nearest candidates and why each falls short:

| Candidate | Why it is not such a mechanism |
|---|---|
| Decree Art. III permitted list | Enumerates four justifications; says nothing about preserving normative identity, and Art. VIII assigns the opposite consequence |
| ROLE §4.1 Entropy Risk Assessment | A rejection filter, not a correction procedure; Gate 2 rejects behavioural corrections |
| INV-DOC-008 (ADR-001) | States the opposite — corrections require a **new superseding artifact** — and is PROPOSED, not in force |
| GOVERNANCE §5.1 PATCH lane | Applies to specification documents, not implementations; not status-qualified |
| Constitution Art. XI | Produces a **new version**, i.e. explicitly changes identity |
| `docs/regulatory_compliance.md` §Frozen Status | "Changes require formal review + compliance re-assessment" — names no procedure, no authority, no artifact |

### Q9 — Repository precedent

Five precedents recorded in §9 with SHAs, before/after states and stated rationales.
Summary: **P-1, P-2, P-3 are precedents of departure** — a self-declared-immutable FROZEN
document was edited in place, and observable implementation behaviour including `core/` was
changed, all retaining the v3.3 label, with no version increment, no new lineage, no
superseding artifact and no recorded custodian authorization. **P-4 is a precedent of
compliance** for documentation-only corrections. **P-5**: no precedent exists for a
specification-corpus FROZEN document being corrected, because only one such document exists
and it has not been modified.

Per instruction, none of these is treated as normative authority. They establish only that
the stated rules and the recorded practice diverge.

### Q10 — Does v3.3 specifically have an explicit correction policy?

**NO.**

v3.3 has: a freeze **declaration** (README, CHANGELOG, Decree, `run_all_checks.sh`), a
permitted-change **list** (Decree Art. III), an identity **consequence** (Decree Art. VIII;
README §11.4), a rejection **filter** (ROLE §4.1), and a future sealing **procedure**
(ROLE §6.5). It does **not** have a correction policy: no procedure, no authority record,
no artifact form, no identity rule for the corrected result, and no defined meaning for
"non-normative".
**CLASS:** ABSENT

---

## 13. Impact on Engineering Work

Mapping onto the items in `09_SAFE_WORK.md`. **Nothing below authorizes any change.**

| Work class | NB-021 status | Basis |
|---|---|---|
| §1.1 Characterization tests (S-1 … S-9) — recording existing behaviour | **PERMITTED** within Decree Art. VII's three conditions | CASE D |
| §1.2 CI wiring (S-10 … S-19) — running existing tests, adding lint/type/audit jobs | **INDETERMINATE** | Not addressed by Art. III's list. CI files are neither `core/` logic, documentation, nor tests. G-6 applies. |
| §1.3 Bug fixes (S-21 … S-26) incl. `demo.py` crash | **BLOCKED** | CASE C |
| §1.4 Documentation of existing behaviour (S-27 … S-34) | **PERMITTED** | CASE A |
| §1.5 Static typing / refactoring (S-35 … S-37) | **PROHIBITED** | Decree Art. I §9, §10; Art. III prohibited items 5–6; `copilot-guardrails.md`. §7 row 7. |
| §1.6 Observability in `compliance/` (S-38) | **PROHIBITED** | Decree Art. III prohibited items 7–9: "Adding logging decorators / Adding telemetry / Adding monitoring hooks" |
| §1.6 Performance benchmarks (S-39) | **INDETERMINATE** | Measurement-only tooling is not addressed |
| §1.7 **All Aura-Guard work** | **UNAFFECTED** | `aura-guard-v1.3` contains **zero** occurrences of `frozen`/`freeze`. No freeze declaration governs it. NB-021 does not reach it. |
| P0-1 vector-length defect fix | **BLOCKED** | CASE C; also fails ROLE §4.1 Gate 2, since the fix changes output for mismatched-length input |
| Adding a fixture with an unresolved expected value | **PROHIBITED** | CASE E — the only unanimous finding in this audit |

**Net effect:** the two largest blocks of previously-identified safe work —
characterization testing and documentation — remain available. Code-modifying work on
`aura-poc-a-core-v3.3` does not.

---

## 14. Explicit Non-Decisions

This audit did **not**:

- resolve NB-021;
- choose between the two FROZEN vocabularies, or unify them;
- decide whether the v3.3 freeze permits defect correction;
- decide whether any identified defect is a "provable mathematical error";
- decide whether FROZEN or SEALED is the operative immutability boundary;
- decide which corpus governs when `AUDIT_LAYER_SPEC.md` and the Constitution conflict;
- decide whether the P-1/P-2/P-3 precedents were authorized;
- propose a Chief Architect, Protocol Custodian, Architecture Review Board, or emergency
  override;
- propose a new lifecycle state, amendment process, correction mechanism, or ADR;
- modify any code, specification, governance document, or document status;
- approve, freeze, seal, or version anything.

Per the stop condition, where the corpus does not answer:

# GOVERNANCE GAP — DECISION REQUIRED

The decision belongs to the Protocol Custodian / Chief Architect. The specific questions
requiring resolution, in dependency order:

1. Does the specification corpus's FROZEN status apply to the v3.3 implementation at all,
   or are these two unrelated terms? (G-1, G-8)
2. Is the operative immutability boundary FROZEN or SEALED? (X-4, §5.2)
3. Is "non-normative defect correction" a recognized category, and if so what are its
   procedure, authority, artifact form, and identity consequence? (Q8, G-6)
4. What is v3.3's normative identity, given that no tag, SHA, or archival artifact exists?
   (G-4, G-5)
5. Do the bit-identity gate (ROLE §4.1 Gate 2) and the defect-correction permission
   (Decree Art. III) both apply, and which prevails? (X-1)
6. When implementation and specification conflict, which governs? (X-5)
7. Were the post-freeze changes in P-1, P-2 and P-3 authorized, and if so under what
   authority? (G-11)

---

## FINAL VERDICT

**Question:** *"May a non-normative engineering defect correction be made to the
implementation associated with the FROZEN v3.3 baseline without changing the normative
identity?"*

# INDETERMINATE

**Basis:** the corpus explicitly permits certain corrections (Decree Art. III) while
explicitly assigning those corrections a new lineage (README §11.4) and explicitly
rejecting any change that does not preserve bit-identity (ROLE §4.1 Gate 2). It defines no
category of "non-normative defect correction" (G-6), no mechanism for one (Q8), and no
normative identity for v3.3 against which preservation could be assessed (G-4, G-5). Both
readings are supported by explicit text; repository precedent contradicts the stricter
reading without recorded authority.

---

**SPECIFICATION AMENDMENT:**

# PROHIBITED

*(in place, retaining the same frozen identity — Constitution Art. XI; VERSIONING §4;
CONTRIBUTING; PR template. The corpus's defined path is a new version / new document, which
by construction changes identity. Recorded contradiction: `AUDIT_LAYER_SPEC.md`'s
self-correction clause, X-5.)*

---

**TEST-ONLY CHANGE:**

# PERMITTED

*(within Decree Art. VII's three conditions and Art. III item 4; limited to tests that
record or validate existing behaviour. Tests encoding an unresolved normative expected
value are PROHIBITED — CASE E. Bounded by AGENTS.md rule 10.)*

---

**SECURITY DEFECT FIX:**

# INDETERMINATE

*(permitted by Decree Art. III item 1 and ROLE §2.1.2/§3.2.3, but scoped in all three
occurrences to "changed lines / changed code"; no permission exists for unchanged frozen
code (G-7), the bit-identity gate rejects behavioural change (X-1), and the identity
consequence is a new lineage (README §11.4).)*

---

## ENGINEERING GATE

**NB-021:**

# UNRESOLVED

**ENGINEERING CODE CHANGES:**

# BLOCKED PENDING GOVERNANCE CLARIFICATION

Work permitted by explicit corpus evidence and therefore **not** blocked by this gate:

- documentation of existing behaviour (CASE A — Decree Art. VII, Art. III item 5)
- characterization tests recording existing behaviour (CASE D — Decree Art. VII, Art. III
  item 4)
- all `aura-guard-v1.3` work (no freeze declaration governs that repository)

These remain permitted but were **not** performed in this task.

---

*This document has no normative effect. It records evidence only. It approves nothing,
freezes nothing, amends nothing, and implements nothing.*
