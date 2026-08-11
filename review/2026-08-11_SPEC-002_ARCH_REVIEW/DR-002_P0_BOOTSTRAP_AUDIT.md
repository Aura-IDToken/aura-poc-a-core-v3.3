# DR-002-P0 — GOVERNANCE BOOTSTRAP / CHANGE-PATH AUDIT

| Field | Value |
|---|---|
| Document ID | DR-002_P0_BOOTSTRAP_AUDIT |
| Version | 1.0-DRAFT |
| Status | DRAFT — EVIDENCE ACQUISITION ONLY |
| Date | 2026-08-11 |
| Trigger | `DR-002_GOVERNANCE_OPTIONS.md` (`f39b79c`) §2.1, §7.6, risk **P0-3** |
| Normative effect | **NONE** |

---

> **THIS AUDIT PROPOSES NOTHING.**
>
> It does not propose a bootstrap mechanism, invent emergency powers, select Chief Architect,
> Protocol Custodian or ARB, infer authority from ownership or permissions, modify any
> governance document, create an ADR or PR, modify source code, or resolve DR-002.
>
> It answers one closed question from existing evidence, and reports the answer whichever way
> the evidence falls.

**Method.** Case-insensitive regex sweep of all `*.md` in the specification repository
(`AuraIDToken/aura-specification` @ `62d2d6b`), the stub repository
(`aura-nomos/aura-specification` @ `eb2a4ec`), and this repository (`9c6a5d8`, excluding
`review/`) for: `bootstrap · transitional · interim · provisional · grandfather ·
first-instance · emergency · deadlock · tie-break · casting vote · veto · escalat · dispute ·
arbitrat · quorum · succession · appoint`. Every hit is reported in §8. Full directory
inventories of `templates/`, `arc/` and `governance/` were taken.

Identifiers `X-n` / `C-n` / `A-n` / `M-n` refer to `DR-002_EVIDENCE_PACKAGE.md`. **C-9 is new
in this audit.**

---

## 1. Question

> **Does the current Aura governance corpus contain an explicit, executable, non-circular
> mechanism for making the first governance change required to resolve DR-002?**

### 1.1 The three conjunctive criteria

A qualifying mechanism must satisfy **all three**. Each is a separate test, and failing any one
disqualifies.

| Criterion | Satisfied when |
|---|---|
| **EXPLICIT** | The mechanism names, in source text, the actor for each step: who proposes, who reviews, who approves, who records. A step whose actor must be inferred, or which depends on resolving an ambiguity, is not explicit. |
| **EXECUTABLE** | Every step can be performed as written today: every named body is constituted, every named procedure is defined, every required artifact exists. |
| **NON-CIRCULAR** | No step depends for its validity on the authority the mechanism is being used to establish. |

### 1.2 Scope note

"The first governance change required to resolve DR-002" means the change that would establish
approval authority for SPEC, ADR and RFC artifacts. Per `DR-002_GOVERNANCE_OPTIONS.md` §7, every
candidate model requires amending at least one of: the AURA Constitution, GOV-001, VERSIONING.md,
CONTRIBUTING.md, APS-000, one or more templates, or `ADR-001_DOCUMENT_MODEL`. This audit
therefore traces the change path for **each** of those instruments.

---

## 2. Change Mechanisms

Every explicitly defined governance change mechanism in the corpus.

### CM-1 — Constitution Amendment

| Field | Value |
|---|---|
| **Source** | `AURA_CONSTITUTION.md` (AURA-CON-001 v1.0, **FROZEN**) |
| **Section** | Article XI |
| **Initiating actor** | **Not named** — "Amendment … requires: 1. An RFC" |
| **Review actor/body** | **Not named** — "2. An Architecture Review" |
| **Approval actor** | **Chief Architect** (Art. XI(5)) |
| **Merge/recording step** | **Not defined.** Art. XI says "New FROZEN version published" (via `constitution/README.md`); no recording act specified |
| **Freeze step** | "Once a version is marked FROZEN, its content is immutable" — no conferring actor named |
| **Dependencies** | Architecture Review undefined (**M-2**); conducting body contested (**A-4**) and unconstituted (**M-3**); impact analysis undefined; "dependent documents" set undefined |

### CM-2 — GOV-001 Amendment

| Field | Value |
|---|---|
| **Source** | `GOVERNANCE.md` (GOV-001 v1.0-**DRAFT**) |
| **Section** | §11, delegating to §5.2 |
| **Initiating actor** | Any party — "Open an RFC in `/rfcs/`" |
| **Review actor/body** | **Architecture Review Board** — "§5.2(4) Architecture Review Board assessment" |
| **Approval actor** | **Chief Architect** (§5.2(5)) |
| **Merge/recording step** | §5.2(6–7): "RFC transitions to APPROVED"; "Implementation via pull request referencing RFC". **Merging actor not named** |
| **Freeze step** | Not applicable to GOV-001 |
| **Dependencies** | **ARB not constituted** (**M-3**); comment period 14 days; ARB act character unstated (**A-8**) |

### CM-3 — VERSIONING.md (POL-VER-001) Amendment

| Field | Value |
|---|---|
| **Source** | `VERSIONING.md` (POL-VER-001 v1.0-DRAFT) |
| **Section** | §10 |
| **Initiating actor** | Not named — "require an RFC per CONTRIBUTING.md" |
| **Review actor/body** | Via CONTRIBUTING.md → **Architecture Review** |
| **Approval actor** | **Chief Architect** |
| **Merge/recording step** | Not defined |
| **Freeze step** | N/A |
| **Dependencies** | Architecture Review undefined (**M-2**); CONTRIBUTING.md's own rows are incomplete (**C-6**) |

### CM-4 — Major Change (general)

| Field | Value |
|---|---|
| **Source** | `GOVERNANCE.md` §5.2 |
| **Section** | §5.2, eight steps |
| **Initiating actor** | Any party (open an RFC) |
| **Review actor/body** | **ARB** (step 4) |
| **Approval actor** | **Chief Architect** (step 5) |
| **Merge/recording step** | Step 7, "Implementation via pull request" — **actor not named** |
| **Freeze step** | Not in this mechanism |
| **Dependencies** | **M-3**, **A-8**, **M-4** |

### CM-5 — Minor Change (PATCH)

| Field | Value |
|---|---|
| **Source** | `GOVERNANCE.md` §5.1 |
| **Section** | §5.1, four steps |
| **Initiating actor** | Any party (open a PR) |
| **Review actor/body** | "one reviewer approval" — **reviewer not identified** |
| **Approval actor** | Implicit in the reviewer |
| **Merge/recording step** | **"Chief Architect or delegate may merge"** (X-10) — the corpus's only merge grant |
| **Freeze step** | N/A |
| **Dependencies** | "Delegate" undefined (**M-6**). **Scope is expressly limited**: "Typos, formatting, non-normative clarifications **that do not change protocol behavior**"; "No RFC or ADR required" |

### CM-6 — RFC Process

| Field | Value |
|---|---|
| **Source** | `GOVERNANCE.md` §7; `rfcs/README.md`; `templates/RFC_TEMPLATE.md` |
| **Section** | §7, nine steps |
| **Initiating actor** | Any party (copy template, assign RFC-NNN, open PR) |
| **Review actor/body** | **ARB votes ACCEPT / REJECT / DEFER** (§7(7)) |
| **Approval actor** | **Chief Architect final approval** (§7(8)); `RFC_TEMPLATE.md` line 105 `Decided by: Chief Architect` |
| **Merge/recording step** | §7(9) "RFC transitions to ACCEPTED or REJECTED". `rfcs/README.md`: "Do not merge your own RFC" — a **restriction**, not a grant |
| **Freeze step** | None; RFC lifecycle terminates at ACCEPTED/REJECTED |
| **Dependencies** | **ARB not constituted** (**M-3**); **M-4** (who merges) |

### CM-7 — ADR Process

| Field | Value |
|---|---|
| **Source** | `GOVERNANCE.md` §6; `adrs/README.md`; `templates/ADR_TEMPLATE.md` |
| **Section** | §6, seven steps |
| **Initiating actor** | Any party (copy template, assign ADR-NNN, submit PR) |
| **Review actor/body** | **None specified.** §6 has no review step |
| **Approval actor** | **NONE NAMED.** §6(6): "Merging the PR = accepting the ADR" |
| **Merge/recording step** | Merging is itself the acceptance act. **Merging actor not named** for non-PATCH |
| **Freeze step** | None; `ADR_TEMPLATE.md` status enum is `DRAFT \| ACCEPTED \| SUPERSEDED \| DEPRECATED` — no FROZEN |
| **Dependencies** | **M-4**; **C-2**; `ADR_TEMPLATE.md` has **no approver / acceptance field**; **C-7** (two `ADR-001` copies specify different approver counts and different field names) |

### CM-8 — Document Status Transitions

| Field | Value |
|---|---|
| **Source** | `VERSIONING.md` §3; `GOVERNANCE.md` §4; `APS-000` §5 |
| **Section** | POL-VER-001 §3 "Transition Rules" |
| **Initiating actor** | `DRAFT → REVIEW`: "Author submits document for review via pull request" |
| **Review actor/body** | `REVIEW → APPROVED`: "after **Architecture Review**" |
| **Approval actor** | **Chief Architect** for `REVIEW → APPROVED` and `APPROVED → FROZEN` (X-11) |
| **Merge/recording step** | Not defined |
| **Freeze step** | `APPROVED → FROZEN`: "Explicit freeze decision by Chief Architect; **requires Amendment Procedure (Constitution Article XI)**" — i.e. **recursively invokes CM-1** |
| **Dependencies** | **M-2**, **M-13** (no `DRAFT → REVIEW` approver), **A-9** (scope as to SPEC); freeze recursion into CM-1 |

### CM-9 — Contribution Routing

| Field | Value |
|---|---|
| **Source** | `CONTRIBUTING.md` "Types of Contribution" |
| **Section** | routing table |
| **Initiating actor** | Contributor |
| **Review actor/body** | "Architecture Review" for APS sections, Invariants, Constitution amendments |
| **Approval actor** | **Named only for the Constitution row** ("→ Chief Architect approval"). The APS and Invariant rows terminate at "**PR**" |
| **Merge/recording step** | Not defined |
| **Freeze step** | N/A |
| **Dependencies** | **M-2**; **C-6** (contradicts GOV-001 §2 on Invariants) |

### CM-10 — ARC Acceptance

| Field | Value |
|---|---|
| **Source** | `arc/README.md`; `arc/ARC_TEMPLATE.md` |
| **Section** | `arc/README.md` "Workflow" |
| **Initiating actor** | Not named — "authored outside the normal ADR process" |
| **Review actor/body** | Not named |
| **Approval actor** | "**Architecture Board/Protocol Custodian**" — solidus undefined (**A-3**) |
| **Merge/recording step** | "Issue → Branch → Pull Request → Review → Merge cycle" — actors not named |
| **Freeze step** | `ARC_TEMPLATE.md` front matter fixes `Status: ACCEPTED`; per `ADR-001_DOCUMENT_MODEL`, "Once ACCEPTED, an ARC file is treated as frozen" |
| **Dependencies** | Architecture Board unconstituted (**M-3**); **A-3**; the directory is empty (README only); `arc_to_spec_mapping.yaml` is `mappings: []` |

### CM-11 — SPEC Approval *(from a PROPOSED source only)*

| Field | Value |
|---|---|
| **Source** | `adrs/ADR-001_DOCUMENT_MODEL.md` (**PROPOSED**); `templates/SPEC_TEMPLATE.md` |
| **Section** | "Owners and Authorities"; "Lifecycle Summary" step 5 |
| **Initiating actor** | Not named |
| **Review actor/body** | Not named (lifecycle shows `DRAFT → REVIEW → APPROVED → FROZEN` with no review actor) |
| **Approval actor** | **Protocol Custodian** (X-13) |
| **Merge/recording step** | Not defined for SPEC |
| **Freeze step** | "A SPEC becomes frozen only after explicit approval by the Protocol Custodian" — no Art. XI reference, contradicting POL-VER-001 §3 (**C-5**) |
| **Dependencies** | Source is PROPOSED and **self-blocked**; **C-1**, **C-5**; **M-9** (thresholds, quorum, signature format undefined by its own Open Questions) |

### CM-12 — LEGACY_PROTOCOL Amendment *(implementation repository)*

| Field | Value |
|---|---|
| **Source** | `docs/LEGACY_PROTOCOL.md` (S3, Status **CANONICAL / BINDING**) |
| **Section** | §8.1 "Protocol Immutability" |
| **Initiating actor** | Not named |
| **Review actor/body** | "Legal counsel review" + "Regulatory compliance verification" |
| **Approval actor** | "**Unanimous consent of all 5 shareholders, AND Current Custodian approval**" |
| **Merge/recording step** | Not defined |
| **Freeze step** | Document is declared "constitutionally protected" |
| **Dependencies** | Requires 5 constituted shareholders and a current Custodian. **Scope**: "Custodian Succession and Emergency Recovery"; "APPLIES TO: Aura Protocol v3.3 and all sealed derivatives" |

---

## 3. Constitution Change Path

**Required by:** Models I, III, IV, V (`DR-002_GOVERNANCE_OPTIONS.md` §7.1, §7.3, §7.4, §7.5) —
any change to Art. V (canonical hierarchy), Art. VI (artifact owners) or Art. VIII (authority
scope).

### 3.1 Trace

```
STEP 1  RFC submitted                     Art. XI(1)   actor: NOT NAMED
   ↓
STEP 2  Architecture Review conducted     Art. XI(2)   actor: NOT NAMED · procedure: UNDEFINED
   ↓
STEP 3  Impact analysis documented        Art. XI(3)   actor: NOT NAMED · form: UNDEFINED
   ↓
STEP 4  Dependent documents updated       Art. XI(4)   set of dependents: UNDEFINED
   ↓
STEP 5  Approval by Chief Architect       Art. XI(5)   actor: NAMED ✔
   ↓
STEP 6  New FROZEN version published      constitution/README.md   recording act: UNDEFINED
```

### 3.2 Undefined or unconstituted dependencies

| Step | Dependency | State |
|---|---|---|
| 1 | RFC process | Routes to CM-6, which requires an ARB vote (§7(7)) — **ARB unconstituted (M-3)** |
| 2 | "An Architecture Review" | **Undefined (M-2)** — no definition of what constitutes one, who convenes, quorum, or output validity |
| 2 | Conducting body | **Contested (A-4)** between Chief Architect (GOV-001 §8 "chaired by") and ARB (§2 "conducts ARRs"); ARB **unconstituted (M-3)** |
| 2 | ARR output | GOV-001 §8 requires publication to `/adrs/ARR-NNN_TITLE.md` within 5 days. **No ARR exists in the repository** |
| 3 | Impact analysis | No template, no required content, no acceptance criterion |
| 4 | "Dependent documents" | Set is undefined; no dependency graph exists |
| 5 | Chief Architect | Office is **not defined, appointed, or identified** in any specification-repository document (**M-10**) |
| 6 | Publication / recording | No act, field or register specified |

**Steps with a named actor: 1 of 6.** Steps 1, 2, 3, 4 and 6 name no actor; step 2 additionally
has no defined procedure and a contested, unconstituted body.

---

## 4. GOV-001 Change Path

**Required by:** Models I, II, III, IV (`DR-002_GOVERNANCE_OPTIONS.md` §7.1–§7.4) — every
candidate requires a GOV-001 change.

### 4.1 Trace — §11 delegates entirely to §5.2

`GOVERNANCE.md` §11 in full:

> "This document may be amended via the Major Change process (§5.2) above."

```
STEP 1  Open an RFC in /rfcs/                    §5.2(1)   actor: ANY (implicit)
   ↓
STEP 2  RFC enters DRAFT status                  §5.2(2)   mechanical
   ↓
STEP 3  Community comment period (min 14 days)   §5.2(3)   actor: n/a
   ↓
STEP 4  Architecture Review Board assessment     §5.2(4)   body: NOT CONSTITUTED ✘
   ↓
STEP 5  Chief Architect approval                 §5.2(5)   actor: NAMED ✔
   ↓
STEP 6  RFC transitions to APPROVED              §5.2(6)   actor: NOT NAMED
   ↓
STEP 7  Implementation via PR referencing RFC    §5.2(7)   merging actor: NOT NAMED
   ↓
STEP 8  ADR created if decision embedded         §5.2(8)   routes to CM-7 (actorless acceptance)
```

### 4.2 Dependencies

| Step | Dependency | State |
|---|---|---|
| 4 | **Architecture Review Board** | **Not defined, constituted, or given membership, appointment method or quorum anywhere in the corpus (M-3).** No document states it exists. |
| 4 | Character of "assessment" | Binding or advisory is **unstated** (**A-8**); the same body is described as "assessing" (§5.2), "voting" (§7), "conducting ARRs" (§2) and "REVIEW" (`rfcs/README.md`) |
| 5 | Chief Architect | Office not defined or identified (**M-10**) |
| 6 | Transition actor | Not named |
| 7 | Merge authority | **Not granted** for non-PATCH (**M-4**); X-10 is PATCH-scoped |
| 8 | ADR acceptance | Actorless (**C-2**); `ADR_TEMPLATE.md` has no acceptance field |

**Step 4 is a hard stop.** GOV-001's only amendment path requires an assessment by a body that
the corpus never constitutes. **GOV-001 cannot be amended by its own stated procedure.**

---

## 5. RFC Change Path

### 5.1 Trace — GOV-001 §7 and `rfcs/README.md`

```
STEP 1  Copy templates/RFC_TEMPLATE.md            §7(1)   actor: ANY
   ↓
STEP 2  Assign next sequential RFC-NNN            §7(2)   actor: ANY · registry: NONE
   ↓
STEP 3  Fill required sections                    §7(3)   actor: proposer
   ↓
STEP 4  Submit as PR — starts comment period      §7(4)   actor: proposer
   ↓
STEP 5  Minimum 14-day comment period             §7(5)   mechanical
   ↓
STEP 6  Author updates RFC with responses         §7(6)   actor: proposer
   ↓
STEP 7  ARB votes ACCEPT / REJECT / DEFER         §7(7)   body: NOT CONSTITUTED ✘
   ↓
STEP 8  Chief Architect final approval            §7(8)   actor: NAMED ✔
   ↓
STEP 9  RFC transitions to ACCEPTED or REJECTED   §7(9)   actor: NOT NAMED
```

### 5.2 CONTRIBUTING.md routing

| Contribution type | Stated path | Approver named? |
|---|---|---|
| Typo / formatting | PR → 1 review | No |
| Clarification (non-normative) | PR → 1 review | No |
| New APS section / requirement | RFC → Architecture Review → **PR** | **No** |
| New Protocol Invariant | RFC → Architecture Review → **PR** | **No** — contradicts GOV-001 §2 (**C-6**) |
| New Conformance Test | RFC → PR referencing RFC | No |
| New Reference Fixture | PR with fixture file + test linkage | No |
| **Constitution amendment** | RFC → Architecture Review → **Chief Architect approval** | **Yes** |

Six of seven rows name no approver. `rfcs/README.md` adds "6. Do not merge your own RFC" — a
restriction that presupposes an unnamed merging party (**M-4**).

### 5.3 Dependencies

**Step 7 is a hard stop** — the same unconstituted ARB as §4. The approver at step 8 **is**
named (X-6), which distinguishes the RFC path from the ADR and SPEC paths: here the defect is
executability, not attribution. There is also **no RFC registry**: `rfcs/` contains a README with
an empty index table, so "next sequential RFC-NNN" has no authoritative source.

---

## 6. ADR Change Path

### 6.1 Trace — GOV-001 §6 and `adrs/README.md`

```
STEP 1  Copy templates/ADR_TEMPLATE.md      §6(1)   actor: ANY
   ↓
STEP 2  Assign next sequential ADR-NNN      §6(2)   actor: ANY · baseline: CORRUPT (C-7)
   ↓
STEP 3  Fill all required sections          §6(3)   actor: author
   ↓
STEP 4  Submit as pull request              §6(4)   actor: author
   ↓
STEP 5  Link to any related RFC             §6(5)   actor: author
   ↓
STEP 6  MERGING THE PR = ACCEPTING THE ADR  §6(6)   actor: NOT NAMED ✘
   ↓
STEP 7  ADR status set to ACCEPTED          §6(7)   actor: NOT NAMED · field: DOES NOT EXIST ✘
```

### 6.2 Merge / acceptance mechanics

This is the most consequential path for DR-002, because every candidate governance model would
be recorded in an ADR.

| Finding | Evidence |
|---|---|
| **Acceptance is an act, not a decision** | §6(6): "Merging the PR = accepting the ADR". `adrs/README.md`: "5. Merging = accepting". No actor at either. |
| **No merge grant covers ADRs** | X-10 is the corpus's only merge grant and is scoped to PATCH: §5.1 covers "Typos, formatting, non-normative clarifications that do not change protocol behavior … No RFC or ADR required". By its own terms §5.1 **excludes** ADR-bearing changes. |
| **No template field records acceptance** | `ADR_TEMPLATE.md` front matter: `Document ID`, `Status`, `Date`, `Author`, `Related RFC`, `Supersedes`, `Superseded By`. **No approver, owner, or acceptance field.** |
| **The corpus disagrees on the field name** | `ADR-001_DOCUMENT_MODEL` requires `Accepted-by:`; `docs/adr/001-document-model.md` requires `accepted_by`. Neither exists in the template (**C-7**). |
| **The numbering baseline is corrupt** | Three documents claim `ADR-001` with statuses ACCEPTED, PROPOSED and DRAFT. `adrs/README.md` indexes one. "Next sequential" is therefore undefined. |
| **No ADR registry** | `adrs/README.md`'s index table lists one entry; two further ADR-001 documents are unindexed. |

### 6.3 A precise observation on step 6

Step 6 is **mechanically performable** — a merge can occur — while the **authority to perform it
is unestablished**. This is a distinct failure mode from the ARB stops in §4 and §5, where the
step cannot occur at all.

Recorded as fact, not as an opening: an ADR merged today would be "ACCEPTED" per GOV-001 §6 with
no attributable approver, no template field recording one, and, per Constitution Art. VIII
(X-3), **no valid approval if the merging party were an AI system.** §11.2 addresses whether this
constitutes a qualifying mechanism.

---

## 7. SPEC Change Path

### 7.1 Does an explicit SPEC lifecycle exist?

| Source | Status | What it provides |
|---|---|---|
| `AURA_CONSTITUTION.md` Art. V | **FROZEN** | Canonical hierarchy contains **no SPEC class** |
| `GOVERNANCE.md` §3, §4, §5, §6, §7 | DRAFT | **No SPEC row** in the artifact table; no SPEC process |
| `VERSIONING.md` §1, §3 | DRAFT | §1 scope enumerates "APS documents, Protocol Invariants, Conformance Tests, Reference Fixtures, releases" — **SPEC not named**. §3 applies to "every APS document **and governance artifact**" — whether SPEC qualifies is **A-9** |
| `APS-000` §3, Appendix A | DRAFT | Canonical prefix registry does **not** include `SPEC` |
| `CONTRIBUTING.md` | — | **No SPEC row** in the routing table |
| `templates/SPEC_TEMPLATE.md` | template | §"Owner" line 9 offers two roles; line 32: "The SPEC must be accepted by the Protocol Custodian" |
| `adrs/ADR-001_DOCUMENT_MODEL.md` | **PROPOSED** | The only lifecycle: `DRAFT → REVIEW → APPROVED → FROZEN`, approved by Protocol Custodian |

### 7.2 Finding

**No in-force document defines a SPEC lifecycle.** The only lifecycle definition (CM-11) is in a
PROPOSED document that is itself self-blocked, and the only other statements are in a template —
which is not a governance instrument and is internally inconsistent between lines 9 and 32.

Consequently SPEC-002's own header statement — `Normative effect: NONE until APPROVED` — refers
to a state transition for which **no in-force procedure exists**.

---

## 8. Bootstrap / Transitional Authority

Exhaustive search results. Every hit is reported.

### 8.1 Specification repository (`AuraIDToken/aura-specification` @ `62d2d6b`)

Sweep of all `*.md` for the seventeen search terms returned **four hits in total**:

| Hit | File : line | Text | Is it an authority? |
|---|---|---|---|
| 1 | `adrs/ADR-001_DOCUMENT_MODEL.md:101` | "Exact approval thresholds and sign-off procedure for Architecture Board and Protocol Custodian (**quorum**, signature format)." | **No** — listed under "Open Questions (require Protocol Custodian resolution)". It records that quorum is **undefined**. |
| 2 | `docs/adr/001-document-model.md:104` | identical | **No** — same, in the divergent copy |
| 3 | `ROADMAP.md:9` | "## Current State (v0.1.x — Specification **Bootstrap**)" | **No** — a release-phase label, not an authority |
| 4 | `specification/SPEC-002…md:178` | "**Lineage** — describes the **succession** relationship between artifacts (e.g., `supersedes`)" | **No** — artifact lineage, not role succession |

**Directory checks:**

| Path | State |
|---|---|
| `governance/` | **DOES NOT EXIST.** (`aura-nomos` CODEOWNERS references `/governance/`; the directory exists in neither repository.) |
| `templates/` | `ADR_TEMPLATE.md` · `APS_DOCUMENT_TEMPLATE.md` · `CONFORMANCE_REPORT_TEMPLATE.md` · `CONFORMANCE_TEST_TEMPLATE.md` · `FIXTURE_TEMPLATE.json` · `README.md` · `RFC_TEMPLATE.md` · `SPEC_TEMPLATE.md` — **none contains bootstrap, transitional or emergency provisions** |
| `arc/` | `ARC_TEMPLATE.md` · `README.md` — no such provisions |
| `rfcs/` | README with an empty index — no such provisions |

### 8.2 Verdict for the specification repository

| Authority sought | State |
|---|---|
| Bootstrap authority | **ABSENT** |
| Transitional authority | **ABSENT** |
| Emergency authority | **ABSENT** |
| Grandfathering | **ABSENT** |
| Initial-constitution authority | **ABSENT** |
| First-instance authority | **ABSENT** |
| Dispute authority | **ABSENT** |
| Deadlock / tie-break / casting vote | **ABSENT** |
| Quorum rule | **ABSENT** (referenced once, as an open question) |
| Role appointment or succession | **ABSENT** |

**The specification repository contains no bootstrap, transitional, emergency, grandfathering,
first-instance, or dispute authority of any kind.**

### 8.3 Stub repository (`aura-nomos/aura-specification` @ `eb2a4ec`)

Two files: an 11-byte README and `.github/CODEOWNERS`. **ABSENT** for all categories.

### 8.4 Implementation repository (`9c6a5d8`) — where such authority DOES exist

Unlike S1, S3 contains genuine emergency, succession and interim authority. It is reported in
full because a bare "ABSENT" would be inaccurate for the estate as a whole.

**8.4.1 — `docs/LEGACY_PROTOCOL.md`** (Status: **CANONICAL / BINDING**; Scope: "Custodian
Succession and Emergency Recovery"; Applies to: "Aura Protocol v3.3 and all sealed derivatives")

This is **the only document in the entire estate containing a constituted body with a quorum
rule and an appointment mechanism.**

| Provision | Content |
|---|---|
| §2.1–2.2 Constituted body | **5 shareholders**: Legal Representative · Technical Continuity Officer · Regulatory Liaison · Independent Auditor · Institutional Archive |
| §2.1 Quorum | **3 of 5** (Shamir threshold) |
| §2.3 Activation conditions | Custodian deceased · unreachable 90 days · declares incapacity · court order |
| §2.4 Appointment | Six-step reconstruction; "A new Custodian is appointed and receives the reconstructed key" |
| §4 Emergency halt | "**Any shareholder** may trigger EMERGENCY_HALT" — signed declaration, notification, initiate succession |
| §7 Revocation | "**Any 2 shareholders** may initiate REVOCATION" on Custodian breach |
| §7.1 **Interim Custodianship** | Powers **limited to**: "Execute HALT and FREEZE · Preserve sealed artifacts · Prevent further changes." Explicitly: "**The Interim Custodian may not approve new changes until succession is complete.**" |
| §8.1 Its own amendment | Unanimous consent of all 5 shareholders **AND** Current Custodian approval **AND** legal counsel review **AND** regulatory compliance verification |

**8.4.2 — `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §5.3 "Emergency Succession"** (Status: CANONICAL)

> "If Current Custodian becomes unavailable without designating successor:
> **Priority Order:** 1. Most recent contributor to `core/` who has NOT proposed convenience
> changes · 2. Contributor with longest history of rejected pull requests (for entropy reasons)
> · 3. Contributor with most constitutional compliance test additions · 4. External auditor with
> regulatory expertise
> **Emergency Custodian Powers:** May perform critical security fixes only · **May NOT modify
> constitutional constants** · **May NOT seal instrument** · MUST designate permanent successor
> within 90 days"

**8.4.3 — `CONSTITUTIONAL_DECREE.md`** Art. II/IV: `REGULATORY_HALT` and
`CONSTITUTIONAL_UNCERTAINTY` response protocols — **refusal mechanisms**, requiring escalation to
the Custodian; they grant no authority.

**8.4.4 — `.github/copilot-instructions.md` §"Escalation Rule"**: "**Escalation does NOT grant
authority to reinterpret canonical definitions.**" An explicit denial of authority.

### 8.5 Why the S3 mechanisms do not reach DR-002

Three independent reasons, each from source text:

| # | Reason | Evidence |
|---|---|---|
| **R-1** | **Scope is the instrument, not the specification corpus.** | LEGACY_PROTOCOL: "SCOPE: Custodian Succession and Emergency Recovery"; "APPLIES TO: Aura Protocol v3.3 and all sealed derivatives". Every enumerated power concerns sealed artifacts, checksums, the Master Custodian Key, and `core/`. No S3 document addresses SPEC, ADR, RFC or APS classes. Whether an S3 role has standing in S1 is undefined (**M-12**). |
| **R-2** | **Activation conditions do not include governance deadlock.** | LEGACY_PROTOCOL §2.3 lists four triggers: death · 90-day unreachability · declared incapacity · court order. §4 lists four halt triggers: cryptographic compromise · regulatory invalidation · legal prohibition · determinism failure. §7 lists four revocation triggers, all Custodian breach. **An unresolvable governance ambiguity is none of these.** |
| **R-3** | **Interim powers expressly exclude approving changes.** | LEGACY_PROTOCOL §7.1: "The Interim Custodian **may not approve new changes** until succession is complete." ROLE §5.3: Emergency Custodian "May perform critical security fixes only · **May NOT modify constitutional constants** · **May NOT seal instrument**." Both emergency authorities are **preservative**, not constitutive. |

### 8.6 CONFLICT DETECTED — C-9 *(new in this audit)*

**Source A** — `docs/LEGACY_PROTOCOL.md` §2: succession by **3-of-5 Shamir shareholders**, with
five named shareholder roles, activation conditions, and a six-step ceremony.

**Source B** — `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` §5.3: succession by **contributor priority
order** — most recent `core/` contributor, then longest history of rejected PRs, then most
compliance-test additions, then external auditor.

**Nature.** Two different emergency-succession mechanisms for the **same role**, in the **same
repository**, both Status CANONICAL, selecting successors by entirely different criteria
(cryptographic shareholding vs contribution history). Neither cites the other. Neither states
precedence.

**Impact.** The only fully specified authority mechanism in the estate is internally contested.
This does not bear on DR-002 directly, per R-1 through R-3, but it bears on any future proposal
to extend S3 mechanisms to specification governance.

**Recorded, not reconciled.**

---

## 9. Circularity Analysis

Cycles identified. **None is resolved here.**

### CYC-1 — Review body required to constitute the review body

```
Constitute the ARB
  └─ requires amending GOV-001 §2
       └─ GOV-001 §11 → §5.2
            └─ §5.2(4) requires ARB assessment
                 └─ requires a constituted ARB
                      └─ ⟲ back to start
```

**Evidence.** GOV-001 §11 (verbatim): "This document may be amended via the Major Change process
(§5.2) above." §5.2(4): "Architecture Review Board assessment." **M-3**: ARB not constituted.

### CYC-2 — Architecture Review required to define the Architecture Review

```
Define "Architecture Review"
  └─ appears in Constitution Art. XI(2) → amending it requires Art. XI
       └─ Art. XI(2) requires "An Architecture Review"
            └─ ⟲
  └─ or appears in GOV-001 §5.2/§8 → amending requires §5.2
       └─ §5.2(4) requires ARB assessment → CYC-1
```

**Evidence.** Constitution Art. XI(2); GOV-001 §5.2(4), §8. **M-2**, **A-4**.

### CYC-3 — Authority required to create the authority

```
Establish SPEC approval authority
  └─ only source is ADR-001_DOCUMENT_MODEL (X-13), status PROPOSED
       └─ it states: "requires explicit approval by the Protocol Custodian"
            └─ the Protocol Custodian role in the specification corpus
               is constituted by that same document
                 └─ ⟲
```

**Evidence.** `ADR-001_DOCUMENT_MODEL` "Status and Acceptance"; X-13; **C-1**.

### CYC-4 — Freeze requires an amendment procedure that requires a review that requires freeze-capable authority

```
APPROVED → FROZEN (POL-VER-001 §3)
  └─ "requires Amendment Procedure (Constitution Article XI)"
       └─ Art. XI(2) requires an Architecture Review → CYC-2
```

**Evidence.** POL-VER-001 §3 transition rules; Constitution Art. XI.

### CYC-5 — POL-VER-001 amendment routes into CYC-2

```
Amend VERSIONING.md
  └─ §10: "require an RFC per CONTRIBUTING.md and approval by the Chief Architect"
       └─ CONTRIBUTING.md routes all normative changes through "Architecture Review"
            └─ CYC-2
```

### 9.1 Paths that do NOT close a cycle

Reported for completeness; each fails a different criterion rather than looping.

| Path | Why it does not loop | Why it nonetheless fails |
|---|---|---|
| **CM-5** Minor Change (PATCH) | Merge grant X-10 is explicit and needs no ARB | **Scope-excluded**: §5.1 covers only "Typos, formatting, non-normative clarifications that do not change protocol behavior"; "No RFC or ADR required". A governance-authority change is not within it. |
| **CM-7 step 6** ADR merge=accept | No body required; mechanically performable | **Not explicit**: no actor named (**M-4**, **C-2**); no template field to record acceptance; corrupt numbering baseline (**C-7**); AI performance would be void under X-3 |
| **CM-12** LEGACY_PROTOCOL amendment | 5 shareholders + Custodian, no ARB | **Out of scope** (R-1); its interim powers exclude approving changes (R-3) |

---

## 10. Executability Test

**Legend.** EXPLICIT — actor and procedure named in source text · PARTIAL — named but incomplete,
or scope-limited, or character unstated · ABSENT — no actor or procedure named · CONTRADICTED —
named, and an equal-or-higher-rank source assigns otherwise.

| Path | START | PROPOSAL | REVIEW | APPROVAL | MERGE / RECORD | EFFECTIVE STATE |
|---|---|---|---|---|---|---|
| **CM-1** Constitution (Art. XI) | EXPLICIT | PARTIAL | **ABSENT** | EXPLICIT | **ABSENT** | PARTIAL |
| **CM-2** GOV-001 (§11→§5.2) | EXPLICIT | EXPLICIT | **ABSENT** | EXPLICIT | **ABSENT** | PARTIAL |
| **CM-3** VERSIONING (§10) | EXPLICIT | PARTIAL | **ABSENT** | EXPLICIT | **ABSENT** | PARTIAL |
| **CM-4** Major Change (§5.2) | EXPLICIT | EXPLICIT | **ABSENT** | EXPLICIT | **ABSENT** | PARTIAL |
| **CM-5** Minor Change (§5.1) | EXPLICIT | EXPLICIT | PARTIAL | PARTIAL | EXPLICIT | EXPLICIT |
| **CM-6** RFC (§7) | EXPLICIT | EXPLICIT | **ABSENT** | EXPLICIT | **ABSENT** | PARTIAL |
| **CM-7** ADR (§6) | EXPLICIT | EXPLICIT | **ABSENT** | **ABSENT** | **ABSENT** | **CONTRADICTED** |
| **CM-8** Status transition (§3) | PARTIAL | PARTIAL | **ABSENT** | EXPLICIT | **ABSENT** | PARTIAL |
| **CM-9** CONTRIBUTING routing | EXPLICIT | EXPLICIT | **ABSENT** | **CONTRADICTED** | **ABSENT** | **ABSENT** |
| **CM-10** ARC acceptance | PARTIAL | **ABSENT** | **ABSENT** | PARTIAL | PARTIAL | PARTIAL |
| **CM-11** SPEC (PROPOSED) | **ABSENT** | **ABSENT** | **ABSENT** | **CONTRADICTED** | **ABSENT** | **CONTRADICTED** |
| **CM-12** LEGACY_PROTOCOL (S3) | EXPLICIT | PARTIAL | EXPLICIT | EXPLICIT | **ABSENT** | EXPLICIT |

### 10.1 Cell notes

| Cell | Basis |
|---|---|
| CM-1 REVIEW ABSENT | Art. XI(2) names neither actor nor procedure (**M-2**, **A-4**, **M-3**) |
| CM-1 / CM-5 APPROVAL | Chief Architect named (X-1, X-10); the office itself is undefined (**M-10**) — recorded but not treated as disqualifying, since the grant is textually explicit |
| CM-2 / CM-4 / CM-6 REVIEW ABSENT | ARB not constituted (**M-3**) |
| CM-5 REVIEW PARTIAL | "one reviewer approval" — reviewer not identified |
| CM-5 EFFECTIVE EXPLICIT | The only path with an explicit merge grant (X-10) — **but scope-limited to non-behavioural PATCH** |
| CM-7 APPROVAL ABSENT | §6(6) actorless (**C-2**) |
| CM-7 EFFECTIVE CONTRADICTED | Status set to ACCEPTED via a field that `ADR_TEMPLATE.md` does not define; two `ADR-001` copies require different fields (**C-7**) |
| CM-9 APPROVAL CONTRADICTED | APS and Invariant rows name no approver, contradicting GOV-001 §2 (**C-6**) |
| CM-11 APPROVAL CONTRADICTED | X-13 (PROPOSED) vs POL-VER-001 §3 (**C-1**) |
| CM-11 EFFECTIVE CONTRADICTED | Freeze assigned to Protocol Custodian without Art. XI, vs POL-VER-001 §3 (**C-5**) |
| CM-12 REVIEW/APPROVAL EXPLICIT | 5 shareholders, 3-of-5 quorum, Custodian approval — **the only fully specified review-and-approval pair in the estate** — but scope-excluded (R-1, R-2, R-3) |

### 10.2 Observation

**No path has EXPLICIT at every step.** CM-5 comes closest and is disqualified by its own stated
scope. CM-12 has the strongest review/approval pair in the estate and is disqualified by scope,
activation conditions, and an express prohibition on approving changes.

---

## 11. Bootstrap Verdict

### 11.1 Application of the three criteria

| Path | EXPLICIT | EXECUTABLE | NON-CIRCULAR | Qualifies? |
|---|---|---|---|---|
| CM-1 Constitution | ✘ — review actor and recording act unnamed | ✘ — review undefined; body unconstituted | ✘ — CYC-2 | **No** |
| CM-2 GOV-001 | ✘ — merging actor unnamed | ✘ — ARB unconstituted | ✘ — CYC-1 | **No** |
| CM-3 VERSIONING | ✘ | ✘ — routes to Architecture Review | ✘ — CYC-5 | **No** |
| CM-4 Major Change | ✘ | ✘ — ARB unconstituted | ✘ — CYC-1 | **No** |
| CM-5 Minor Change | ✔ | ✔ | ✔ | **No — scope-excluded by §5.1's own terms** |
| CM-6 RFC | ✘ — merging actor unnamed | ✘ — ARB unconstituted | ✘ — CYC-1 | **No** |
| CM-7 ADR | ✘ — **no actor at approval or merge** | ~ mechanically performable | ✔ | **No — fails EXPLICIT** |
| CM-8 Status transition | ✘ | ✘ | ✘ — CYC-4 | **No** |
| CM-9 CONTRIBUTING | ✘ | ✘ | ✘ | **No** |
| CM-10 ARC | ✘ — A-3 solidus | ✘ — Architecture Board unconstituted | ✘ | **No** |
| CM-11 SPEC | ✘ | ✘ — source PROPOSED | ✘ — CYC-3 | **No** |
| CM-12 LEGACY_PROTOCOL | ✔ | ✔ | ✔ | **No — out of scope (R-1), activation conditions unmet (R-2), interim powers exclude approving changes (R-3)** |

### 11.2 Why not INDETERMINATE

INDETERMINATE would be correct if the evidence were silent or insufficient. It is neither.

- The search in §8 was **exhaustive** and returned a complete, small result set. Absence of
  bootstrap authority in the specification repository is a **positive finding**, not a gap in
  the search.
- Every one of the twelve mechanisms fails at least one criterion for a **stated, cited reason**.
  No mechanism's status is unknown.
- The one reading under which a path might exist — that Constitution Art. VIII's unenumerated
  "responsible for the project" (X-2) permits the Chief Architect to act without the Art. XI
  Architecture Review, or to constitute the ARB by fiat — **depends on resolving A-1**, which the
  text does not resolve. A mechanism whose existence is contingent on resolving an ambiguity is
  **by definition not explicit**. The question asks for an *explicit* mechanism; that contingency
  therefore settles the question negatively rather than leaving it open.

### 11.3 Why not PARTIALLY EXECUTABLE

PARTIALLY EXECUTABLE would be correct if some qualifying mechanism existed for part of the
required change. It does not: **the required change is a governance-authority change**, and

- CM-5, the only fully executable path, **excludes** changes to protocol behaviour and requires
  "No RFC or ADR" — a governance-authority change is outside its stated scope; and
- CM-12, the only path with a constituted body and quorum, **expressly prohibits** its interim
  authority from approving changes.

Both exclusions are stated in the source text, not inferred. No fraction of the required change
falls within a qualifying mechanism.

### 11.4 Verdict

> # NOT EXECUTABLE

**The Aura governance corpus does not contain an explicit, executable, non-circular mechanism
for making the first governance change required to resolve DR-002.**

Basis: twelve mechanisms identified; **zero** satisfy all three criteria; five circular
dependencies identified (CYC-1 … CYC-5); the specification repository contains **no** bootstrap,
transitional, emergency, grandfathering, first-instance or dispute authority of any kind; the two
mechanisms that are individually explicit and executable are each excluded by their own stated
scope.

**This verdict is a finding about the corpus. It is not a proposal, and it does not identify or
imply which mechanism should be created, or by whom.**

---

## 12. Impact

### 12.1 DR-002

DR-002 was already UNRESOLVED. This audit establishes that it is additionally **not resolvable by
any procedure the corpus currently defines**. Risk **P0-3** in `DR-002_GOVERNANCE_OPTIONS.md`
("a potentially self-blocking first governance act") is **confirmed as actual rather than
potential**: the self-blocking is demonstrated by CYC-1 through CYC-5, not merely suspected.

Two consequences follow, both recorded as facts:

1. The decision surface in `DR-002_GOVERNANCE_OPTIONS.md` §11.1 is unchanged — the twelve items
   still require governance decision.
2. A **thirteenth** item is now evidenced: the corpus supplies no procedure by which items 1–12
   may be enacted once decided. `DR-002_GOVERNANCE_OPTIONS.md` §11.1 item 12 ("which process may
   legitimately produce this decision") was previously recorded as open; it is now recorded as
   **having no answer in the corpus**.

### 12.2 AD-CA-001 … AD-CA-012

**Unchanged: all twelve remain blocked.** The blockage acquires a second layer:

| Layer | Established by | Effect |
|---|---|---|
| Layer 1 — no approval authority | `DR-002_EVIDENCE_PACKAGE.md` | No one is authorised to approve the ADR carrying a decision |
| **Layer 2 — no procedure to establish that authority** | **This audit** | The authority cannot be conferred by any defined path |

The §8.3 properties of the blockage are **unaffected**: it remains **procedural, not
substantive**. Analytical work on any AD-CA domain requires no approval authority and is not
blocked; only closure is. AD-CA-007 remains the clearest illustration — its numeric semantics are
fully specifiable today, and only the approval is unavailable.

### 12.3 SPEC-002

Three findings compound:

1. SPEC-002 v0.3 states `Normative effect: NONE until APPROVED`. Per §7, **no in-force document
   defines a SPEC lifecycle**, so the APPROVED state has no defined procedure to reach.
2. SPEC-002 §9 criterion 1 requires every requirement be backed by an approved source or approved
   decision. Neither backing can be produced.
3. SPEC-002 §11 records READINESS STATUS: NOT READY on **technical** grounds (twelve unresolved
   AD-CA domains). This audit adds an independent **procedural** ground. The two are separate:
   resolving every technical question would not, on the current corpus, permit SPEC-002 to
   advance beyond DRAFT.

SPEC-002 v0.4 as proposed in `03_SPEC-002_v0.4_DRAFT.md` is unaffected in content — it is a DRAFT
delta with no normative effect and requires no approval to exist. Its **advancement** is blocked.

### 12.4 CR-007

CR-007 remains **BLOCKED and undefined**, and this audit adds a layer.

Previously (`01_ADR_REVIEW.md` §6 B-006-a, `ARCHITECTURE-RESOLUTION-001.md` §13): no document
defines CR-007's inputs, outputs, authority or pass/fail semantics; the `CR` prefix is
unregistered under APS-000 §3.

Now additionally: defining CR-007 would require either a new normative document or an amendment
to an existing one. Both routes traverse CM-1, CM-2, CM-3, CM-6 or CM-7 — **all of which this
audit finds non-qualifying**. CR-007's unblocking is therefore gated by DR-002-P0, not only by
its own missing definition.

SPEC-002 §2.2's prohibition ("This document MUST NOT … Implement CR-007") and §11's "CR-007
remains BLOCKED" are both undisturbed.

### 12.5 Scope of this finding

This audit changes **no** status. It does not make anything worse; it makes an existing condition
visible and precise. Nothing in the estate has been modified, and no artifact's status has
advanced or regressed as a result of it.

---

## 13. STOP

| Measure | Value |
|---|---|
| Change mechanisms identified | 12 (CM-1 … CM-12) |
| Mechanisms satisfying EXPLICIT + EXECUTABLE + NON-CIRCULAR | **0** |
| Circular dependencies identified | 5 (CYC-1 … CYC-5) |
| Bootstrap / transitional / emergency authority in the specification repository | **ABSENT** (exhaustive search; 4 hits, none an authority) |
| Bootstrap / emergency authority in the implementation repository | **PRESENT but scope-excluded** (R-1, R-2, R-3) |
| Executability-test steps marked ABSENT or CONTRADICTED | 38 of 72 |
| Paths with EXPLICIT at every step | **0** |
| New conflict recorded | **C-9** — two contested Custodian succession mechanisms in one repository |
| Bootstrap verdict | **NOT EXECUTABLE** |

**No bootstrap mechanism proposed. No emergency powers invented. No role selected. No authority
inferred from ownership or permissions. No governance document, GOV-001, Constitution or SPEC-002
modified. No ADR created. No PR created. No source code modified. DR-002 not resolved.**

---

**DR-002-P0 STATUS: EVIDENCE COMPLETE**
**DR-002 STATUS: UNRESOLVED**
**NO GOVERNANCE CHANGE MADE**
**NO NORMATIVE EFFECT**
