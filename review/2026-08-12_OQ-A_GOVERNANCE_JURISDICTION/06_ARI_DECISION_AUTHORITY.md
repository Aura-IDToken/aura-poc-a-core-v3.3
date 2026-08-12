# 06 — ARI DECISION AUTHORITY (OQ-A-005)

**Question:** *Who may establish ARI semantics?*
**Required result:** decision-authority evidence
**Normative effect:** NONE

> **No actor is recommended, proposed, or selected in this document.**

---

## 1. Direct test — does any source grant authority over ARI by name?

Exhaustive check of every authority grant located in `03_AUTHORITY_AND_APPROVAL_MATRIX.md`:

| Source | Does the grant name ARI? |
|---|---|
| AURA-CON-001 Art. VIII, Art. XI | No |
| GOV-001 §2 (four enumerated classes) | No |
| POL-VER-001 §3 (status transitions) | No |
| `aura-specification/README.md:154` | No |
| `.github/CODEOWNERS` | No |
| ADR-001_DOCUMENT_MODEL (PROPOSED) | No |
| CONSTITUTIONAL_DECREE Art. V, Art. X | No |
| ROLE §2.1.1, §2.1.2, §2.1.4, §2.2.1 | No |
| `docs/ops/PROTOCOL_CUSTODIAN.md` | No |
| AGENTS.md rule 13 | No |

**Result: no source grants any role authority over ARI semantics by name.**

The only occurrence of ARI in the specification corpus is
`aura-specification/glossary/GLOSSARY.md:27-28`, which defines it by deferral to an
implementation and grants nothing to anyone. This is consistent with RD-1 (CLOSED).

---

## 2. Roles explicitly granted relevant authority, and over which artifact classes

| Role | Artifact class covered | Exact grant | Source | Status |
|---|---|---|---|---|
| **Chief Architect** | AURA Constitution amendments | "final and sole approval authority" | GOV-001 §2; AURA-CON-001 Art. XI | Constitution FROZEN; GOV-001 DRAFT |
| **Chief Architect** | APS document status transitions (APPROVED → FROZEN) | as above | GOV-001 §2; POL-VER-001 §3 | DRAFT |
| **Chief Architect** | Protocol Invariant additions or removals | as above | GOV-001 §2 | DRAFT |
| **Chief Architect** | New reference implementation recognition | as above | GOV-001 §2 | DRAFT |
| **Chief Architect** | "canonical documents" (broader phrasing) | "sole approval authority" | `aura-specification/README.md:154` | no status |
| **Architecture Review Board** | RFCs | "votes: ACCEPT / REJECT / DEFER" | GOV-001 §7 | DRAFT; body has no established existence |
| *(unnamed — whoever merges)* | ADRs | "Merging the PR = accepting the ADR" | GOV-001 §6 | DRAFT |
| **Protocol Custodian** | `core/` directory; constitutional constants; layer boundaries; cryptographic primitives | "FINAL AUTHORITY" | ROLE §2.2.1 | CANONICAL (implementation corpus) |
| **Protocol Custodian** | Sentinel Drift Threshold; Scaling Factor; fixed-point precision | "MAY modify … only with [four conditions]" | ROLE §2.1.1; Decree Art. V | CANONICAL |
| **Protocol Custodian** | task authorization for AI assistants | "MAY authorize specific tasks" | ROLE §2.1.2; Decree Art. III item 6 | CANONICAL |
| **Protocol Custodian** | sealing | "SOLE AUTHORITY" | ROLE §2.1.4 | CANONICAL |
| **Protocol Custodian** (PROPOSED only) | SPEC documents | "approves SPECs … signatory for normative acceptance" | ADR-001_DOCUMENT_MODEL `:54` | **PROPOSED — not in force** |

---

## 3. Does ARI belong to any of these artifact classes?

Tested class by class. **Each test is a question about the corpus, not an inference.**

| Class | Would ARI fall inside it? | Evidence |
|---|---|---|
| **AURA Constitution content** | **No.** RD-1 premise 2 (CLOSED): the Constitution does not define, constrain, or delegate ARI. Verified: no occurrence of "ARI" in `constitution/AURA_CONSTITUTION.md` | RD-1; direct search |
| **APS document content** | **Conditionally.** If ARI is decided to be protocol behaviour, its natural home is APS-001 §3/§4 (Input/Output Requirements) — both `TODO` — or a new APS. Whether ARI *is* protocol behaviour is `ARI-D-001`, **open** | `APS-001:44-50`; `ARI-D-001` |
| **Protocol Invariant** | **Partially.** ARI outputs are covered indirectly by INV-001 (Deterministic Evaluation), INV-002 (Bit-Perfect Replay), INV-006 (Platform Independence), INV-008 (Fail Closed) — all Critical. None defines ARI; each constrains any computation the protocol has. Adding an ARI-specific invariant would be a Chief-Architect matter under GOV-001 §2 | `APS-100:42-56`; `INVARIANT_REGISTRY.md` |
| **Reference implementation recognition** | **Adjacent, not identical.** Recognising RI-PY would not define ARI; and SPEC-002 `:37` requires an explicit governance grant before implementation behaviour becomes normative — none exists | GOV-001 §2; SPEC-002 `:37` |
| **`core/` directory changes** | **Yes for the code, no for the semantics.** ROLE §2.2.1 gives the Custodian final authority over changes *to `core/`*. That is authority over the artifact, not authority to define what the protocol requires of any implementation | ROLE §2.2.1 |
| **Constitutional constants (0.68 / 100,000 / Q16.16)** | **Overlapping.** Three of the 27 ARI decisions touch these constants — `ARI-D-007` (quantization), `ARI-D-014` (drift threshold), `ARI-D-008` (widths). ROLE §2.1.1 gives the Custodian conditional authority over exactly these three values **for this instrument**. Whether that reaches a cross-language protocol ARI is `OQ-B`, **open** | ROLE §2.1.1; `review/2026-08-12_RD1_ARI_DECISION_READINESS/09_OPEN_QUESTIONS.md` OQ-B |
| **SPEC documents** | **Unresolved.** SPEC-002's AD-CA-007 covers "numeric representation of vector values"; whether ARI operands are within that scope is U-2, **open**. And no in-force source assigns SPEC approval to anyone | SPEC-002 §6; U-2 |

---

## 4. Does authority extend from these classes to ARI, and is the extension authorized?

The method requires this step to be asked separately, because an actor's authority over class X
does not automatically reach a question that merely touches X.

| Candidate extension | Would it reach ARI? | Is the extension itself authorized? |
|---|---|---|
| Chief Architect's authority over **APS status transitions** → authority to decide APS *content* about ARI | GOV-001 §2 grants authority over **transitions**, not content. Content arrives via the §5.2 process (RFC → ARB → Chief Architect approval), where the Chief Architect's approval **is** named at step 5 | **Partially authorized.** The RFC route is explicit; but it presupposes that ARI is APS content, which is `ARI-D-001` |
| Chief Architect's authority over **invariants** → authority over ARI, since INV-001/002/006/008 constrain it | The invariants constrain any computation; deciding ARI is not the same act as adding or removing an invariant | **Not authorized as stated.** No source says authority over invariants includes authority over the quantities they constrain |
| Custodian's authority over **constants** → authority over ARI quantization | Directly touches `ARI-D-007` and `ARI-D-014` **for this instrument** | **Authorized for the instrument; unauthorized (unestablished) for the protocol.** ROLE §2.1.1's scope is the instrument; whether it binds other implementations is `OQ-B`, open. Note also the four mandatory conditions, including "creation of new instrument version (not update)" |
| Custodian's authority over **`core/`** → authority over ARI semantics | Would make the implementation the definition | **Explicitly blocked** by SPEC-002 `:37` (an explicit governance grant is required, and none exists), by APS-000 TERM-002 ("An implementation does not define the protocol"), by AURA-CON-001 Art. IV P1, and by RD-1 premise 9 |
| Protocol Custodian's authority over **SPECs** → authority over SPEC-002 and thence ARI numerics | Would matter if AD-CA-007 covers ARI operands (U-2) | **Not in force.** The only source is ADR-001_DOCUMENT_MODEL, PROPOSED, with no `Accepted-by:` line |
| Whoever holds **merge permission** → ADR acceptance → ARI decision recorded by ADR | GOV-001 §6 makes merge the acceptance act | **Recorded as a finding, not an authorization.** Merge permission is a platform capability; no governance document grants it decision authority (`03_AUTHORITY_AND_APPROVAL_MATRIX.md` §3) |

---

## 5. Cross-cutting blockers

| # | Blocker | Effect on OQ-A-005 |
|---|---|---|
| B-1 | **Chief Architect and Protocol Custodian are never related to each other** by any document | If the two corpora each grant authority to "their" actor, and the actors are not identified as the same, an ARI decision could be authorized in one corpus and unauthorized in the other |
| B-2 | **Which hierarchy governs is a NORMATIVE CONFLICT** (`02`, `04`) | Even a valid grant may be outranked under one ladder and not the other |
| B-3 | **ARI's artifact class is undetermined** (`ARI-D-001`, open) | Until ARI is classified as protocol content or implementation content, no class-based grant applies |
| B-4 | **The RFC route has never been exercised**, and the ARB has no established existence | The one explicit content-approval path in the corpus is not demonstrably operational |
| B-5 | **AI assistants are barred from approving** by three independent sources | AURA-CON-001 Art. VIII; GOV-001 §9; ROLE §7.1 / Decree Art. V. This forecloses any route in which an agent settles ARI |

---

## 6. OQ-A-005 — finding

# CONDITIONALLY DETERMINABLE

**Not UNRESOLVED**, because the corpus does contain explicit authority grants that would reach
ARI once a prior classification is made. **Not AUTHORIZED ACTOR**, because no source establishes
authority over ARI semantics today.

The determination is conditional on two facts, neither of which the corpus supplies:

| Condition | Where it must be answered | If answered one way | If answered the other |
|---|---|---|---|
| **C-1: Is ARI protocol content or instrument content?** | `ARI-D-001` (open) | Protocol content → the explicit route is CONTRIBUTING `:23` / GOV-001 §5.2: **RFC → Architecture Review → Chief Architect approval**, with the Chief Architect's approval named at step 5 | Instrument content → the explicit route is the **Protocol Custodian**'s authority over `core/` and constants (ROLE §2.1.1, §2.2.1), with the mandatory conditions attached, **and** the consequence that ARI is not a protocol-conformance object |
| **C-2: Which corpus's authority ladder governs?** | `OQ-A` / this package's `02` and `04` — **NORMATIVE CONFLICT** | Specification ladder → Chief Architect route | Implementation ladder → Custodian route |

Both conditions are open. Therefore:

> **Who may establish ARI semantics cannot be stated today.** Two candidate routes exist, each
> explicitly documented, each conditional on an unanswered prior question, and each currently
> facing an operational blocker (B-4 for the RFC route; B-1/OQ-B for the Custodian route).

**No actor is named as the answer, and neither route is recommended.**

---

*This document has no normative effect. It records which authority grants exist, which artifact
classes they cover, and why their extension to ARI is not established. It appoints no actor and
recommends no route.*
