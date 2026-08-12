# 01 — GOVERNANCE SOURCE REGISTER

**Package:** OQ-A GOVERNANCE / JURISDICTION · **Normative effect:** NONE

Every governance source located, with what it says about itself. **Nothing in this register
grants authority; it records claims.** Source identifiers `S-nn` (specification corpus) and
`I-nn` (implementation corpus) are local to this package.

---

## 1. Specification corpus — `AuraIDToken/aura-specification` @ `62d2d6b`

| ID | File | Document ID | Version | Status (self-declared) | Self-declared scope | Governance content |
|---|---|---|---|---|---|---|
| **S-01** | `constitution/AURA_CONSTITUTION.md` | AURA-CON-001 | 1.0 | **FROZEN** ("Its content is immutable", `:12`) | "All documents, implementations, and architectural decisions MUST remain consistent with it" (Preamble) | Art. IV principles; Art. V canonical hierarchy; Art. VIII authority; Art. IX conformance; Art. X evidence; Art. XI amendment; Art. XII interpretation |
| **S-02** | `GOVERNANCE.md` | GOV-001 | 1.0-DRAFT | **DRAFT** (per `releases/v0.1.0/DOCUMENT_STATUS.md:25`) | "how the **`aura-specification` repository** is governed: who has authority over what" (§1) | §2 authority hierarchy; §3 artifact table; §5 change process; §6 ADR process; §7 RFC process; §9 AI policy; §10 conflict resolution |
| **S-03** | `VERSIONING.md` | POL-VER-001 | 1.0-DRAFT | **DRAFT** | "versioning model for all artifacts in the **`aura-specification` repository**" (§1) | §3 status lifecycle + transition rules; §4 version numbers; §8 identifier reuse; §9 release artifacts |
| **S-04** | `CONTRIBUTING.md` | — | — | none stated | contribution to the specification repository | Core Rule (spec is source of truth); contribution-type table; PR requirements; RFC/ADR authoring; "What NOT to Do" |
| **S-05** | `README.md` | — | — | none stated | repository orientation | "Canonical Document Hierarchy" (`:63-83`); "Governance" (`:152-158`) |
| **S-06** | `aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` | APS-000 | 1.0-DRAFT | **DRAFT** | terminology, identifiers, document status, canonical registry | §1 "In cases of conflicting definitions, APS-000 takes precedence"; §4 identifier rules; §5 status table; §7 registry |
| **S-07** | `specification/APS-001_PROTOCOL_SPECIFICATION.md` | APS-001 | 0.1-DRAFT | **TODO** ("This document does not yet exist", `:12`) | root normative behavioural specification | none authored |
| **S-08** | `specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` | SPEC-002 | 0.3-DRAFT | **DRAFT**; "**Normative effect: NONE until APPROVED**" (`:11`) | Constitution Artifact / Vector contract surface | `:37` direction-of-authority rule; §6 AD-CA table; §11 readiness status |
| **S-09** | `adrs/ADR-001_DOCUMENT_MODEL.md` | ADR-001 | — | **PROPOSED**; "requires explicit approval by the Protocol Custodian" (`:105`) | canonical document model ARC → SPEC → APS | owners/authorities block (`:52-57`); INV-DOC-001…008; CI enforcement jobs |
| **S-10** | `adrs/ADR-001_REPOSITORY_STRUCTURE.md` | ADR-001 | 1.0 | **ACCEPTED** (`DOCUMENT_STATUS.md:26`) | repository structure | structure decision |
| **S-11** | `adrs/README.md` | — | — | none stated | ADR index and process | "Merging = accepting" (`:23`); index lists only ADR-001_REPOSITORY_STRUCTURE |
| **S-12** | `rfcs/README.md` | — | — | none stated | RFC index and process | RFC is "the **mandatory** process for any change that affects: Protocol behavior, Protocol Invariants, Conformance Tests, Evidence structure, Constitutional principles" (`:7-12`); index: "*No RFCs submitted yet.*" |
| **S-13** | `releases/v0.1.0/DOCUMENT_STATUS.md` | — | v0.1.0 | none stated | status snapshot at release | authoritative-looking status list for 17 documents |
| **S-14** | `.github/CODEOWNERS` | — | — | — | every path (`* @AuraIDToken`) | "Every file in this repository requires **review** by the Chief Architect" |
| **S-15** | `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md` | — | — | — | PRs to the specification repository | checklist: "No FROZEN documents modified"; RFC required for new spec content/invariant/CONF change |
| **S-16** | `ROADMAP.md` | — | — | none stated | planning | records APS-001 as "❌ TODO … the missing root normative document" |
| **S-17** | `compliance/TRACEABILITY_MATRIX.md` | COMP-TM-002 | 1.0-DRAFT | **DRAFT** | traceability | every row NOT VERIFIED |

## 2. Implementation corpus — `AuraIDToken/aura-poc-a-core-v3.3` @ `f3a87cc`

| ID | File | Document ID | Version | Status (self-declared) | Self-declared scope | Governance content |
|---|---|---|---|---|---|---|
| **I-01** | `CONSTITUTIONAL_DECREE.md` | none | 1.0 | **MANDATORY / NON-OVERRIDABLE**; "ACTIVE AND BINDING" (`:468`) | "**SCOPE: ALL AI ASSISTANCE**" (`:5`); authority: "Custodian of the Protocol" (`:6`) | Art. I constants; Art. III permitted/prohibited change list; Art. IV refusal; Art. V authority hierarchy; Art. VI checks; Art. VII permissions; Art. VIII versioning/sealing; Art. X enforcement + "Custodian Signature: [Required for core/ changes]" |
| **I-02** | `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` | none | 1.0 | **CANONICAL**; "Authority: Constitutional Decree Article V" | the Protocol Custodian role for this instrument | Art. II powers (constants, task authorization, rejection, sealing, code-review FINAL AUTHORITY over `core/`); Art. IV decision framework (Gate 1/Gate 2); Art. VII AI interaction; **Art. IX §9.2 conflict-resolution hierarchy** |
| **I-03** | `AGENTS.md` | none | — | none stated | "this repository … role-separation governance for AI-assisted work" (`:3`) | 13 canonical rules; **10-tier Authority Precedence**; conflict rule ("do not silently reconcile … request human/Protocol Custodian resolution") |
| **I-04** | `CLAUDE.md` | none | — | none stated | Claude's role in the Aura workflow | scope/out-of-scope; required workflow; **identical 10-tier Authority Precedence**; defers to `AGENTS.md` as "canonical source" for common rules |
| **I-05** | `README.md` | none | — | "**Status:** FROZEN / CANONICAL" (`:13`) | the instrument | §7 sealing; §8 versioning ("Any change creates a new instrument"); §9–§10 operational governance; §11.4 "Bug fixes or modifications require a new lineage"; §11.5 "ARI is a measurement value, not a decision" |
| **I-06** | `docs/ops/OPS_PROTOCOL_CANONICAL.md` | none | — | none stated | operational governance v3.3 | sealing; versioning; §4.1 "**Once sealed**, the artifact is immutable"; custodianship principles |
| **I-07** | `docs/ops/PROTOCOL_CUSTODIAN.md` | none | 1.0 | **CANONICAL / BINDING** | "Human Governance of a Frozen Measurement Instrument"; "APPLIES TO: Aura Protocol v3.3 and all sealed derivatives" | Custodian as "**sole human authority**" for integrity of the instrument |
| **I-08** | `docs/LEGACY_PROTOCOL.md` | none | — | — | custodian succession and disaster recovery | 5-share Shamir key split; succession triggers; sealing artifact list with `[COMPUTED_AT_SEALING_v3.3]` unfilled |
| **I-09** | `docs/conformance/README.md` | none | — | none stated | conformance governance documentation | restates workflow; "Use the authority precedence defined in `AGENTS.md` and `CLAUDE.md`"; conflict rule |
| **I-10** | `.github/copilot-instructions.md` | none | — | none stated | Copilot behaviour | integer-only arithmetic; layer separation; escalation rule; "Escalation does NOT grant authority to reinterpret canonical definitions" |
| **I-11** | `.github/github/copilot-instructions.md` | none | — | "PROTOCOL FROZEN" (`:38`) | Copilot system directives | "ALL directives below are **subordinate to the Constitutional Decree**" (`:9-10`); ARI formula; int64 accumulator |
| **I-12** | `.github/copilot-guardrails.md` | none | — | none stated | forbidden actions | "See CONSTITUTIONAL_DECREE.md for complete rules"; hard-fail list |
| **I-13** | `.github/copilot-tasks.md` | none | — | none stated | authorized task list | "Copilot may ONLY work on tasks listed below"; TASK-01…04 |
| **I-14** | `.github/instructions/*.instructions.md` | none | — | none stated | path-scoped (`**/*.py`, Rust) | "Follow the canonical repository-level governance rules and authority precedence defined in `AGENTS.md`" |
| **I-15** | `CHANGELOG.md` | none | — | "FROZEN — MC-READY 2026" | change log | states a policy: "Each entry … documents a completed task that was **authorized before execution**" |

## 3. Prior review records (non-normative, used as evidence)

| ID | File | Status | Use here |
|---|---|---|---|
| **R-01** | `review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md` | "Evidence record. **No normative effect.**" | FROZEN-semantics evidence; precedent records P-1…P-5; contradiction register X-1…X-11 |
| **R-02** | `review/2026-08-11_ENGINEERING_BASELINE/BRIEF_DR-002.md` | decision brief; "Brak nowych decyzji" (no new decisions) | records that identifier `DR-002` occurs in **no** repository; maps the nearest tracked equivalent to SPEC-002 §6 AD-CA domains, explicitly as an open governance question |
| **R-03** | `review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` | "no normative effect" | RD-1…RD-6 decision questions; exit criteria |
| **R-04** | `review/2026-08-12_RD1_ARI_DECISION_READINESS/` | "Normative effect: NONE" | the 27 ARI decisions this gate precedes; OQ-A/OQ-B/OQ-C/OQ-D as first stated there |

> **Verification note.** Passages reused from R-01 and R-03 were re-read in the current
> repository state before citation here. Two were confirmed to have moved or to require
> correction of the *label* rather than the content, and are cited from the primary source
> directly in this package rather than through the earlier record.

---

## 4. Sources that do **not** exist

Recorded because their absence is load-bearing for later questions.

| Expected source | Evidence of absence |
|---|---|
| An APS or SPEC defining ARI | RD-1 (CLOSED); `glossary/GLOSSARY.md:27-28` is the only occurrence |
| APS-001 content | `APS-001:5` `Status: TODO`; `:12` "This document does not yet exist" |
| Any RFC | `rfcs/README.md:16` "*No RFCs submitted yet.*" |
| An ARR (Architecture Review Record) | No `ARR-*` file in `adrs/`; GOV-001 §8 defines the artifact |
| An Architecture Review Board roster, charter or membership record | No file; ARB named only in GOV-001 §2, §5.2, §7 |
| A named Chief Architect | No document names the person or maps the role to an account; `CODEOWNERS` maps every path to `@AuraIDToken` |
| A statement that Chief Architect = Protocol Custodian | Absent from both corpora |
| A `CODEOWNERS` file in the implementation repository | `find . -name CODEOWNERS` returns nothing |
| Any repository text describing a "Two-Key" gate, "Key 1"/"Key 2", or ChatGPT review | Case-insensitive search of both repositories returns **zero** hits outside `review/2026-08-12_RD1_ARI_DECISION_READINESS/`, which declares "Normative effect: NONE" |
| The CI jobs `doc/ci/validate-ids`, `doc/ci/traceability-check`, `doc/ci/frozen-check` | Specified by S-09 (PROPOSED); absent from both repositories' workflows |
| A cross-reference between the two corpora | Neither corpus cites the other's governance documents (verified in both directions) |

---

*This document has no normative effect. It records what sources claim about themselves. It
grants no authority, resolves no conflict, and selects nothing.*
