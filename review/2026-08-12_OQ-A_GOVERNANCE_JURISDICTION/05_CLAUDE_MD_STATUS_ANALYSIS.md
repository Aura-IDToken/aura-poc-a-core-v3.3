# 05 — `CLAUDE.md` STATUS ANALYSIS (OQ-A-004)

**Question:** *What normative/procedural status does `CLAUDE.md` have?*
**Required result:** NORMATIVE / PROCEDURAL / INFORMATIONAL / UNRESOLVED
**Normative effect:** NONE

---

## 1. Method constraint applied

`CLAUDE.md` is **not** classified as normative because:

- it is named `CLAUDE.md`;
- agents are expected to follow it;
- it contains mandatory language ("MUST NOT override");
- tooling reads it.

It is **also not** classified as non-authoritative without evidence. Both directions require
evidence, and both are tested below.

---

## 2. What the document contains

> **SOURCE** `aura-poc-a-core-v3.3/CLAUDE.md` · **DOC ID** none · **VERSION** none ·
> **STATUS** none stated · **OWNER** none stated

| Section | Content type |
|---|---|
| "CLAUDE Governance Role" (title) | Role definition |
| "Scope" / "Out of Scope" | Role boundaries — "Evaluate conformance against protocol authority"; "Do not implement protocol-affecting code before approved requirements exist" |
| "Required Workflow" | Process: Specification → Invariants → Conformance Test Matrix → Conformance Gap → Implementation → CI evidence → Adversarial review → Human approval |
| "Governance Reference" | **Self-subordination:** "For common repository-level governance rules, use `AGENTS.md` as the **canonical source**." |
| "Authority Precedence (Highest → Lowest)" | A 10-tier list, **verbatim identical** to `AGENTS.md:36-45` |
| Conflict rule | "do not silently reconcile it; stop; report the conflict; request human/Protocol Custodian resolution" |

**No protocol semantics are stated anywhere in the document.** It contains no formula, constant,
data-model element, invariant, or conformance criterion.

---

## 3. Evidence tests

### Test A — Does any source explicitly define `CLAUDE.md`'s status?

| Candidate source | Statement | Result |
|---|---|---|
| `CLAUDE.md` itself | No `Status:`, `Version:`, `Document ID:` or `Authority:` field | **No self-declared status** |
| `AGENTS.md:41` | Tier 6: "AGENTS.md / **CLAUDE.md** governance workflow" | **Yes — a placement**, in a 10-tier precedence list, characterising its content as a *governance workflow* |
| `CLAUDE.md` itself | "For common repository-level governance rules, use `AGENTS.md` as the canonical source" | **Yes — self-subordination** to `AGENTS.md` for the general rules |
| `docs/conformance/README.md:19` | "`CLAUDE.md` defines Claude's role for architectural/conformance audit." | **Yes — a role characterisation**, by an undated, unstatused README |
| `docs/conformance/README.md:25` | "Use the authority precedence defined in `AGENTS.md` and `CLAUDE.md`." | Treats the two as jointly the precedence source for this repository |
| `AGENTS.md:30` (canonical rule 11) | "Claude's role is architectural/conformance audit." | Confirms role scope |
| Specification corpus | **Zero occurrences** of "CLAUDE" in `aura-specification` (verified) | The specification corpus does not recognise the document at all |
| `releases/v0.1.0/DOCUMENT_STATUS.md` | Not listed | Not in the specification corpus's status registry |
| APS-000 §7 canonical registry | Not listed; `CLAUDE.md` has no `PREFIX-NNN` identifier as APS-000 §4 requires | Not a registered artifact under the corpus's own identifier rules |
| AURA-CON-001 Art. V hierarchy | Not named | Position depends on classifying it as "Repository Documentation" — a classification no source makes |

### Test B — Does it create obligations, and over whom?

| Statement | Obligation type | Addressee |
|---|---|---|
| "Do not implement protocol-affecting code before approved requirements exist" | Prohibition | An AI agent working in this repository |
| "Lower-level instructions MUST NOT override higher-level authority" | Ordering rule | Instructions given to an agent |
| "do not silently reconcile … stop; report; request … resolution" | Procedure | An agent detecting a conflict |

All obligations are addressed to **agents operating in this repository**. None is addressed to
implementations generally, to the protocol, or to other repositories. No statement defines
protocol behaviour.

### Test C — Was it approved by anyone with established authority?

| Question | Evidence |
|---|---|
| Is there an approval record? | None. The file entered the repository by commit; per the method rule `COMMIT HISTORY ≠ GOVERNANCE AUTHORITY`, that establishes nothing |
| Does any authority grant it force? | No source names an approver for `CLAUDE.md`. The Decree does not mention it; ROLE does not mention it; GOV-001 governs a different repository |
| Does its tier-6 placement have an established basis? | The placement is made by `AGENTS.md`, which the same list places at tier 6 — the self-referential problem recorded at `02_DOCUMENT_HIERARCHY_EVIDENCE.md` H-3 |

### Test D — Is it a normative specification?

| Criterion for a normative source in this corpus | Met? |
|---|---|
| Carries a document ID per APS-000 §4 | **No** |
| Carries a lifecycle status per POL-VER-001 §3 / APS-000 §5 | **No** |
| Appears in a canonical registry (APS-000 §7) or status snapshot | **No** |
| States protocol behaviour in RFC-2119 terms about the protocol | **No** — its MUST/MUST NOT statements are about agent conduct |
| Is placed in an in-force document hierarchy | **Only** by `AGENTS.md` H-3, whose own authority is unestablished |

---

## 4. Classification

| Candidate classification | Assessment |
|---|---|
| **Model/agent instruction** | **Supported.** Its entire content addresses an agent's role, scope and conduct. |
| **Repository contribution policy** | **Partially.** It constrains what an agent may contribute; it does not define PR mechanics, review, or merge rules. |
| **Governance policy** | **Partially, and derivatively.** It reproduces `AGENTS.md`'s precedence list verbatim while naming `AGENTS.md` the canonical source for such rules — so it restates governance rather than establishing it. |
| **Normative specification** | **Not supported.** It states no protocol behaviour, carries no ID, version or status, and is absent from the specification corpus and its registries. |
| **Procedural instruction** | **Supported.** "Required Workflow", the conflict-handling procedure, and the scope/out-of-scope boundaries are procedure. |
| **Operational guidance** | **Supported**, overlapping with the above. |
| **Informational** | **Not supported as the whole picture** — the document is written in obligation form and is relied on operationally, which is more than informational. |

### Finding

# PROCEDURAL — normative force UNRESOLVED

**PROCEDURAL** is the classification the evidence supports for the document's *content*: it
defines an agent's role, workflow and conflict-handling procedure, and it explicitly defers to
`AGENTS.md` for the substantive governance rules.

**UNRESOLVED** applies to the separate question of whether it *binds*, and with what force:

1. it declares no status and carries no identifier, so the corpus's own status machinery
   (APS-000 §5, POL-VER-001 §3) does not classify it;
2. no actor with established approval authority has approved it;
3. its only hierarchy placement comes from a document that places itself at the same tier;
4. the specification corpus does not acknowledge it.

Two things follow, and both are recorded rather than resolved:

- **`CLAUDE.md` cannot be cited as the authority that settles a governance question** — including
  the authority-precedence question at `02_DOCUMENT_HIERARCHY_EVIDENCE.md` H-3, which it merely
  restates from `AGENTS.md`.
- **Nothing here says its procedural content is invalid.** Whether an agent should follow it is a
  question of repository practice; whether it can *establish* precedence or authority is the
  question tested above, and that is what is unresolved.

---

## 5. The same test applied to `AGENTS.md`

Recorded because `CLAUDE.md` subordinates itself to `AGENTS.md`, so the answer for `CLAUDE.md`
partly depends on it.

| Criterion | `AGENTS.md` |
|---|---|
| Document ID / version / status | **None** |
| Self-declared scope | "This repository adopts the Aura Conformance Restoration workflow and role-separation governance for AI-assisted work" (`:3`) |
| Self-declared canonicity | "The following rules are the **canonical repository-level agent governance rules**" (`:18`) — canonical **for agent governance**, self-declared |
| Placement | Tier 6 of its own list |
| Recognised by the specification corpus | **No** — zero occurrences of "AGENTS.md" in `aura-specification` |
| Approved by an established authority | No record |

**Finding:** `AGENTS.md` is in the same position as `CLAUDE.md` — self-declared canonical for
agent governance, unstatused, unregistered, and unrecognised by the other corpus. Its 10-tier
precedence list is therefore the **only** ordering of Decree vs Specification in either corpus
(`04_DECREE_VS_SPEC_ANALYSIS.md` §5) and simultaneously the ordering whose own authority is least
established. That combination is recorded as `OQ-A-CONFLICT-003`.

---

*This document has no normative effect. It classifies content type and records that binding force
is unestablished. It does not declare `CLAUDE.md` authoritative, and it does not declare it void.*
