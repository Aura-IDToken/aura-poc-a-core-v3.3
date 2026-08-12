# 09 — TWO-KEY GATE ANALYSIS (OQ-A-010)

**Question:** *How exactly does the Two-Key Gate operate?*
**Required result:** acceptance protocol
**Normative effect:** NONE

---

## 1. Mandatory separation

Per the method constraint, three categories are kept strictly apart, and **B is not converted
into A**:

| Category | Meaning |
|---|---|
| **A — CURRENTLY DOCUMENTED GOVERNANCE** | Rules established in the repository corpus |
| **B — CURRENT WORKING PROCESS AGREED IN THIS PROJECT** | How the project is actually operating in this working session/thread |
| **C — PROPOSED FUTURE GOVERNANCE** | Arrangements suggested but not adopted |

---

## 2. Category A — currently documented governance

### 2.1 Search result

Case-insensitive search of both repositories for `two-key`, `two key`, `KEY 1`, `KEY 2`,
`ChatGPT`:

| Repository | Hits |
|---|---|
| `aura-poc-a-core-v3.3` (excluding `review/2026-08-12_RD1_ARI_DECISION_READINESS/`) | **0** |
| `aura-specification` @ `62d2d6b` | **0** |
| `aura-nomos/aura-specification` @ `eb2a4ec` | **0** |

### 2.2 The single artifact that describes it

> `review/2026-08-12_RD1_ARI_DECISION_READINESS/08_TWO_KEY_DECISION_PROTOCOL.md`

| Property | Finding |
|---|---|
| Status | Header: "**Normative effect: NONE**" |
| Nature | A review record, produced as part of a decision-preparation package |
| How it entered the repository | Authored under task instruction and committed as documentation |
| Its position under `AGENTS.md`'s own precedence list | Its content originates as **tier 8 "Prompt/task instructions"**; as a committed file it is at best repository documentation. It is **not** tier 1–5 |
| Does it grant itself force? | No — it disclaims normative effect on its face |

**Therefore:** the Two-Key Gate has **no Category A basis**. Documenting a process in a
non-normative review record does not make it repository-normative governance, and this package
does not treat it as such.

### 2.3 Adjacent Category A rules that a Two-Key arrangement would have to sit beside

These exist and are relevant, but none of them establishes a Two-Key Gate.

| Rule | Source | Relevance |
|---|---|---|
| "Human approval is required before merging protocol-affecting changes." | AGENTS.md rule 13 | Establishes **a** human gate; does not establish two gates, nor a second reviewer |
| "AI systems MUST NOT approve changes to canonical documents or modify frozen documents." | AURA-CON-001 Art. VIII | Bars an AI from being an approving key |
| "AI assistants MUST NOT: Self-approve changes … Override the Chief Architect's decisions" | GOV-001 §9 | Same |
| "AI Copilot MAY NOT … approve core changes independently" | ROLE §7.1 | Same |
| "Chief Architect … final and sole approval authority over [four classes]" | GOV-001 §2 | The word **"sole"** is in direct tension with any *two*-key requirement over those four classes |
| "do not silently reconcile it; stop; report the conflict; request human/Protocol Custodian resolution" | AGENTS.md `:49-53`; CLAUDE.md; `docs/conformance/README.md` | Establishes escalation to **one** human/role |
| "Adversarial review" as a workflow step | AGENTS.md workflow; CLAUDE.md | The **only** documented step resembling an independent second review — but it names no actor, no artifact, and no acceptance criterion (`08_GOVERNANCE_WORKFLOW.md` WG-7) |
| RFC process: ARB **votes**, then Chief Architect **approves** | GOV-001 §7 steps 7–8 | The corpus's only documented two-stage acceptance — a **body vote plus an individual approval**, both human, inside one corpus. It is not the Two-Key Gate, and it has never been exercised |

---

## 3. Category B — current working process agreed in this project

Recorded as fact about how the project is operating, **not** as governance.

| Element | As practised |
|---|---|
| Trigger | A decision-preparation package is produced by Claude |
| KEY 1 | Human Architectural Authority — the person directing this work |
| KEY 2 | ChatGPT architectural review |
| Rule | Claude may formalize a decision only after both keys accept |
| Where stated | Task instructions in this working thread, transcribed into `review/2026-08-12_RD1_ARI_DECISION_READINESS/08_TWO_KEY_DECISION_PROTOCOL.md` (normative effect NONE) |

**This is B. It is not A.** Nothing in this package converts it.

---

## 4. Category C — proposed future governance

**Empty.** No proposal is made here. Making one would be a governance recommendation, which hard
constraints 23–25 forbid.

---

## 5. The nine required points

Each answered against **Category A evidence only**, since that is what "how does it operate"
means in governance terms.

| # | Question | Category A finding |
|---|---|---|
| 1 | Who provides Key 1? | **EVIDENCE GAP.** No document names a "Key 1". The nearest documented actors are "Chief Architect" (spec corpus, never identified) and "Protocol Custodian" (implementation corpus, identified as Kamil Krasiński), whose mutual relationship is unstated (`03_AUTHORITY_AND_APPROVAL_MATRIX.md` §4) |
| 2 | What constitutes explicit acceptance? | **EVIDENCE GAP** for a Two-Key context. The corpus defines acceptance forms for other artifacts: ADR — "Merging the PR = accepting" (GOV-001 §6); RFC — ARB vote + Chief Architect approval (§7); ADR-001_DOCUMENT_MODEL — "adding an `Accepted-by: <Protocol Custodian>` line and merging" (`:105`, PROPOSED). None is stated to apply to a Two-Key acceptance |
| 3 | Who performs Key 2? | **EVIDENCE GAP.** No document names an external model reviewer. GOV-001 §9 and AURA-CON-001 Art. VIII permit AI systems to analyse and propose while barring them from approving — so whether an AI review can be an accepting *key* at all is itself unresolved under Category A |
| 4 | What constitutes architectural acceptance? | **EVIDENCE GAP.** The corpus has "Architecture Review" (GOV-001 §5.2 step 4) producing an ARR (§8), and "Adversarial review" (AGENTS.md workflow) with no defined output. Neither is defined as an acceptance |
| 5 | What happens if keys disagree? | **EVIDENCE GAP.** The corpus's only disagreement rules are: escalate to "human/Protocol Custodian" (AGENTS.md `:49-53`); ARB may DEFER (GOV-001 §7 step 7); "The Custodian has ABSOLUTE OVERRIDE AUTHORITY" over AI error (ROLE §7.2). None addresses two accepting parties |
| 6 | What happens if evidence is insufficient? | **PARTIALLY DOCUMENTED.** Decree Art. IV: "If you are UNSURE … You MUST REFUSE to make the change", with the CONSTITUTIONAL_UNCERTAINTY protocol; ROLE §4.1 Gate 2: "UNCERTAIN → REJECTED"; SPEC-002 `:109`: gaps "MUST be recorded as UNRESOLVED or EVIDENCE GAP … MUST NOT be resolved by assumption". These constrain an *agent*; they do not describe key behaviour |
| 7 | May Claude formalize only after both keys? | **EVIDENCE GAP for "both".** Category A establishes that an AI may not approve (three sources) and that human approval precedes merging protocol-affecting changes (AGENTS.md rule 13). It establishes **one** required human gate, not two |
| 8 | What artifact records the acceptance? | **EVIDENCE GAP.** Per-class acceptance artifacts exist (ADR by merge; RFC status transition; PROPOSED `Accepted-by:` line). No artifact is defined for recording a Two-Key acceptance |
| 9 | Does the acceptance itself require an ADR? | **EVIDENCE GAP**, and prior-conditioned: `08_GOVERNANCE_WORKFLOW.md` Part 1 finds ADR requirement CONDITIONALLY REQUIRED, and none of the triggers found ("architectural decision embedded in a Major Change"; "constitutional constant change") names a governance acceptance event |

---

## 6. Tension worth recording explicitly

> GOV-001 §2: the Chief Architect has "final and **sole** approval authority over" Constitution
> amendments, APS status transitions, invariant changes, and reference-implementation
> recognition.

A gate requiring **two** acceptances over any of those four classes would need to be reconciled
with the word "sole" — either by establishing that Key 2 is advisory rather than an approval, or
by amending GOV-001 through its own §11 (Major Change process). **This package does not propose
either.** It records that the tension exists and that no source resolves it.

Recorded as `OQ-A-CONFLICT-008`.

---

## 7. OQ-A-010 — finding

# EVIDENCE GAP

The Two-Key Gate is **Category B** — a working process agreed in this project — and has **no
Category A basis** in either repository. All nine operational points are EVIDENCE GAPs under
Category A.

**What this finding does not say:**

- It does not say the Two-Key process is invalid, unwise, or should be abandoned — that would be
  a governance recommendation.
- It does not say the process should be adopted into governance — likewise.
- It does not treat the RD-1 package's `08_TWO_KEY_DECISION_PROTOCOL.md` as governance, because
  that document disclaims normative effect on its face.

**What follows for the sequence:** the gate named "Two-Key Acceptance" in the required sequence
sits, today, on a process with no documented governance basis. Whether that is acceptable is a
decision for the authority that OQ-A-002 and OQ-A-005 are trying to identify — and both of those
are themselves unresolved.

---

*This document has no normative effect. It separates documented governance from working process,
records that the latter has no basis in the former, and proposes no arrangement.*
