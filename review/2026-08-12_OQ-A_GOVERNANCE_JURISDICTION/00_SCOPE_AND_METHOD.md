# 00 — SCOPE AND METHOD

**Package:** OQ-A GOVERNANCE / JURISDICTION EVIDENCE PACKAGE
**Date:** 2026-08-12
**Mode:** EVIDENCE AND DECISION PREPARATION
**Normative effect:** NONE

---

## 1. Purpose

This package prepares the governance/jurisdiction question that must precede
`ARI-D-001 … ARI-D-027`. It establishes **what the repository corpus actually says** about
document hierarchy, authority, approval and formalization — where it is silent, where sources
conflict, and what mechanism would be required to resolve those conflicts.

It answers ten questions, `OQ-A-001` … `OQ-A-010`, with evidence.

## 2. What this package is not

- **Not a governance decision.** No governance model is selected, ranked, or recommended.
- **Not an ARI semantic decision.** No ARI value, formula, scale, dimension, bound, rounding
  rule, division rule, drift model, overflow rule or serialization is chosen.
- **Not an implementation task.** No production code is touched.
- **Not an ADR.** No decision-recording artifact is created.
- **Not a recommendation of an authority, an artifact class, or a process.**

## 3. Position in the required sequence

```
RD-1 (CLOSED)
  ↓
RD-1-ARI-DECISION-READINESS (complete, DECISION-READY)
  ↓
OQ-A GOVERNANCE / JURISDICTION      ← this package prepares this gate
  ↓
Two-Key Acceptance
  ↓
ARI-D-001 … ARI-D-027
  ↓
Formal ADR / SPEC amendment → Reference Model → Fixtures →
Independent Implementation → Conformance → Implementation Remediation
```

`ARI-D-001 … ARI-D-027` **MUST NOT** be resolved until OQ-A is sufficiently resolved. Nothing in
this package resolves any of them.

---

## 4. Method

### 4.1 The critical methodological rule, applied

Authority is **never** inferred from document structure, filename, location, tone, mandatory
language, or the fact that tooling reads a file. For every authority claim the package
establishes, in order:

1. **what the source explicitly claims** — quoted;
2. **what scope that claim has** — as the source itself states it;
3. **whether another source claims something incompatible**;
4. **whether a higher-authority source resolves the conflict**;
5. **whether the corpus provides a mechanism for resolving the conflict** — and whether that
   mechanism is executable.

Where the corpus does not establish the answer: **EVIDENCE GAP**.
Where two authoritative or potentially authoritative sources conflict: **NORMATIVE CONFLICT**.
Where a rule exists but its application to this exact question is unclear:
**JURISDICTION UNRESOLVED**.

None of the three is silently reconciled anywhere in this package.

### 4.2 Distinctions kept separate throughout

Authority · ownership · approval authority · normative source · procedural authority ·
implementation guidance · repository policy · contributor responsibility · custodianship ·
review responsibility · merge authority.

The following equations are **never** assumed:

`OWNER = APPROVER` · `AUTHOR = AUTHORITY` · `CODEOWNER = AUTHORITY` · `REVIEWER = APPROVER` ·
`CLAUDE.md INSTRUCTION = NORMATIVE AUTHORITY` · `IMPLEMENTATION BEHAVIOUR = SPECIFICATION` ·
`DOCUMENT LOCATION = HIERARCHICAL PRECEDENCE` · `COMMIT HISTORY = GOVERNANCE AUTHORITY`

Where a source conflates two of these, the conflation is recorded as a finding rather than
adopted.

### 4.3 Status vocabulary

| Label | Meaning |
|---|---|
| **ESTABLISHED** | The corpus explicitly states it, in a source whose own status gives the statement effect, with scope covering the question |
| **PARTIALLY ESTABLISHED** | Explicitly stated, but scope, status, or applicability to this question is incomplete |
| **JURISDICTION UNRESOLVED** | A rule exists; whether it reaches this question is not established |
| **NORMATIVE CONFLICT** | Two sources state incompatible things and no source subordinates one to the other |
| **EVIDENCE GAP** | The corpus is silent |
| **AUTHORITY UNRESOLVED** | Used in the authority matrix where authority cannot be established |

No newly proposed governance arrangement is labelled APPROVED, ACCEPTED, FROZEN or NORMATIVE
anywhere in this package.

### 4.4 What was read

Targeted governance reads only — no repeat of the full corpus audit, and no new ARI research.
Where a passage was cited by an earlier evidence package, the passage was re-verified in the
current repository state before reuse.

**Implementation corpus** — `AuraIDToken/aura-poc-a-core-v3.3`, branch
`claude/ari-decision-readiness-aryxo5` based on `origin/main` @ `f3a87cc`:
`CONSTITUTIONAL_DECREE.md` (full) · `ROLE_OF_THE_PROTOCOL_CUSTODIAN.md` (Articles I, II, III §3.2,
IV, VII, IX) · `AGENTS.md` (full) · `CLAUDE.md` (full) · `README.md` §7–§12 ·
`docs/ops/OPS_PROTOCOL_CANONICAL.md` · `docs/ops/PROTOCOL_CUSTODIAN.md` ·
`docs/LEGACY_PROTOCOL.md` · `docs/conformance/README.md` · `CHANGELOG.md` (policy statement) ·
`.github/copilot-instructions.md` · `.github/github/copilot-instructions.md` ·
`.github/copilot-guardrails.md` · `.github/copilot-tasks.md` ·
`.github/instructions/python-conformance.instructions.md`

**Specification corpus** — `AuraIDToken/aura-specification` @ `62d2d6b`:
`constitution/AURA_CONSTITUTION.md` · `GOVERNANCE.md` (GOV-001) · `VERSIONING.md` (POL-VER-001) ·
`CONTRIBUTING.md` · `README.md` · `aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` ·
`specification/APS-001_PROTOCOL_SPECIFICATION.md` ·
`specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` · `adrs/ADR-001_DOCUMENT_MODEL.md` ·
`adrs/README.md` · `rfcs/README.md` · `releases/v0.1.0/DOCUMENT_STATUS.md` · `ROADMAP.md` ·
`.github/CODEOWNERS` · `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`

**Prior evidence packages** (used as evidence, cited as non-normative review records):
`review/2026-08-11_ENGINEERING_BASELINE/NB-021_FROZEN_SEMANTICS_AUDIT.md` ·
`review/2026-08-11_ENGINEERING_BASELINE/BRIEF_DR-002.md` ·
`review/2026-08-11_ENGINEERING_BASELINE/05_CORE_REMEDIATION_READINESS.md` ·
`review/2026-08-12_RD1_ARI_DECISION_READINESS/` (all files)

**Third repository:** `aura-nomos/aura-specification` @ `eb2a4ec` contains only a one-line
`README.md` and `.github/CODEOWNERS`. It contributes no governance evidence. Which specification
repository is authoritative is itself recorded as a gap.

---

## 5. Hard constraints observed

| # | Constraint | Status |
|---|---|---|
| 1–12 | No ARI semantic resolved: no `100000`, no `Q16.16`, no `1536`, no similarity formula, division, rounding, bounds, malformed-input behaviour, drift, overflow, serialization selected | **Observed** |
| 13–16 | `core/evaluator.py`, production code, SPEC-002, and every normative document unmodified | **Observed** |
| 17–18 | No fixtures created; no ADR created | **Observed** |
| 19–20 | Implementation behaviour and RI-PY not treated as normative authority | **Observed** |
| 21 | `CLAUDE.md` not treated as authoritative merely because it contains instructions | **Observed** — see `05_CLAUDE_MD_STATUS_ANALYSIS.md` |
| 22 | No conflict resolved by convenience | **Observed** — all recorded in `10_CONFLICT_REGISTER.md`, none reconciled |
| 23–25 | No recommendation of a governance model, an authority, or an artifact class | **Observed** |
| 26–28 | No PR, no merge, no history rewrite | **Observed** |

---

## 6. Package contents

| File | Purpose |
|---|---|
| `00_SCOPE_AND_METHOD.md` | this document |
| `01_GOVERNANCE_SOURCE_REGISTER.md` | every governance source: ID, version, status, scope, self-claim |
| `02_DOCUMENT_HIERARCHY_EVIDENCE.md` | OQ-A-001 — every hierarchy claim found, compared |
| `03_AUTHORITY_AND_APPROVAL_MATRIX.md` | OQ-A-002 — authority matrix and per-artifact approver table |
| `04_DECREE_VS_SPEC_ANALYSIS.md` | OQ-A-003 — seven-step analysis, no forced resolution |
| `05_CLAUDE_MD_STATUS_ANALYSIS.md` | OQ-A-004 — status of `CLAUDE.md` |
| `06_ARI_DECISION_AUTHORITY.md` | OQ-A-005 — who may establish ARI semantics |
| `07_FORMAL_ARTIFACT_ANALYSIS.md` | OQ-A-006 — candidate artifact classes |
| `08_GOVERNANCE_WORKFLOW.md` | OQ-A-007, -008, -009 — ADR requirement, SPEC-002 dependency, workflow |
| `09_TWO_KEY_GATE_ANALYSIS.md` | OQ-A-010 — A/B/C separation of the Two-Key Gate |
| `10_CONFLICT_REGISTER.md` | `OQ-A-CONFLICT-001 …` |
| `11_EVIDENCE_GAP_REGISTER.md` | `OQ-A-GAP-001 …` |
| `12_OQ_A_DECISION_MATRIX.md` | decision-readiness matrix |
| `13_EXECUTIVE_DECISION_BRIEF.md` | compact ten-question table and final status |

---

*This document has no normative effect. It selects no governance model, no authority, and no ARI
semantics; it creates no ADR, amends no normative document, and modifies no code.*
