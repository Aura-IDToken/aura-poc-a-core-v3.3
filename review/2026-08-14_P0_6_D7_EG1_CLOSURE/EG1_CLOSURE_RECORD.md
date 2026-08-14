# EG-1 Evidence-Closure Record

**Task:** narrow evidence-closure pass for EG-1, identified in
`review/2026-08-14_P0_6_D7_DECISION_PREPARATION/`
**Date:** 2026-08-14
**Prepared by:** Claude — evidence agent. NOT the Human Architectural Authority.
NOT the Independent Reviewer.
**Outcome:** **B** — see §6.

---

## 1. Scope

Establish only what D-3 and D-4 actually closed, and where that is recorded.

**Not performed:** a new D-7 audit; any D-7 decision; selection of any versioning
mechanism; reopening of D-1, D-2, D-3 or D-4; any Guard audit; any advance of
D-5.

**Inference prohibition honoured.** No D-3/D-4 value was inferred from the
current implementation, existing code, the candidate lists, `mathematical_foundation.md`,
RI-PY, prior implementation behaviour, or the agent's own technical judgment. No
value was manufactured to let D-7 proceed.

## 2. EG-1 statement

As recorded in `review/2026-08-14_P0_6_D7_DECISION_PREPARATION/06_D7_EVIDENCE_REQUIREMENTS.md` §1:

> The accepted D-3 / D-4 semantic values were not supplied … does the new rule
> alter the nine-field preimage, or add a separate component alongside it?

EG-1 blocks **D7-Q-018** — *can a new entry be made to appear as an old entry?*
If the new rule leaves the nine-field preimage intact and carries a separate
component, a legacy verifier could verify a new record successfully while
ignoring the violations binding required by D-1. If the new rule alters the
preimage, that exposure does not arise. The question cannot be answered by
assuming which.

## 3. Evidence inspected

Source order as instructed. Repository `AuraIDToken/aura-poc-a-core-v3.3`,
branch `claude/p0-1-test-review-qtkye2`.

| # | Source | Located? | What it contains |
|---|---|---|---|
| 1 | HAA decisions recorded in the project conversation | **Yes** | Statements that D-3 and D-4 are `CLOSED` and "passed the Two-Key Gate". No semantic value stated. Reproduced verbatim in §4/§5 |
| 2 | D-3/D-4 decision-preparation package | **Yes** — `review/2026-08-14_P0_6_D3_D4_DECISION_PREPARATION/`, commit `b433708` | Registers, candidates, matrices. **No values.** Decision Record tables blank |
| 3 | D-3/D-4 correction pass | **No** — **EVIDENCE GAP — NO AUTHORITATIVE RECORD FOUND** | `git log` shows a single commit for the package (`b433708`). The only commit matching "correct" is `892f17e`, an ADR line-reference fix, unrelated to D-3/D-4 |
| 4 | Two-Key Gate record for D-3/D-4 | **Yes** — `…/11_TWO_KEY_REVIEW_GATE.md`, commit `b433708` | Records **PENDING / PENDING → OPEN** for both. Signature blocks blank |
| 5 | Subsequent formalization records | **No** — **EVIDENCE GAP — NO AUTHORITATIVE RECORD FOUND** | No ADR, no decisions register, no closure artifact anywhere under `review/` or `docs/`. Repo-wide grep for a recorded D-3/D-4 closure returns only cross-references inside preparation packages |

Implementation code was **not** elevated over these sources and was not consulted
for this question.

## 4. D-3 authoritative closure

**Status: CLOSED — PROCESS / DECISION-DOMAIN.**

**Authoritative statement (source 1), verbatim:**

> D-3 = YES / CLOSED
> Canonical-representation decision package has passed the Two-Key Gate.

**What that statement establishes.** That the *package* passed the gate — i.e.
the decision domain is closed as process state.

**What it does not establish.** It names no base encoding class, no separator or
escaping rule, no float representation, no `None`/absent rule, no domain tag, and
no answer to any of D3-Q-001 … D3-Q-026.

**Repository artifact (source 4).** `…/11_TWO_KEY_REVIEW_GATE.md` §1 records:

```
| D-3 | PENDING | PENDING | OPEN |
```

**Decision Record (source 2).** `…/09_DECISION_BRIEF.md` §6 "D-3" — every field
blank: *Base encoding class (A–E)*, *Domain separation (F) applied?*, *Sub-digest
composition (G) applied?*, *Answers to D3-Q-001 … D3-Q-026*, *Resolution of NC-1*,
*Decided by (HAA)*, *Independent Reviewer*, *Date*, *Authority basis*.

## 5. D-4 authoritative closure

**Status: CLOSED — PROCESS / DECISION-DOMAIN.**

**Authoritative statement (source 1), verbatim:**

> D-4 = YES / CLOSED
> Collection-semantics decision package has passed the Two-Key Gate.

**What that statement establishes.** Domain closure as process state.

**What it does not establish.** It names no collection class (ordered list, set,
multiset, sorted, or composite), no element-identity rule, no ordering,
duplicate, empty or `None` semantics, and no answer to any of
D4-Q-001 … D4-Q-015.

**Repository artifact (source 4).** `…/11_TWO_KEY_REVIEW_GATE.md` §1 records:

```
| D-4 | PENDING | PENDING | OPEN |
```

**Decision Record (source 2).** `…/09_DECISION_BRIEF.md` §6 "D-4" — every field
blank: *Collection class (A–F)*, *Element identity rule*, *Answers to
D4-Q-001 … D4-Q-015*, *Resolution of NC-2*, *Decided by (HAA)*, *Independent
Reviewer*, *Date*, *Authority basis*.

## 6. Semantic values established? — **NO**

**OUTCOME B.**

> D-3/D-4 passed the Two-Key Gate as decision domains, but no normative semantic
> values were established.

No source in the priority order contains a concrete semantic value. There is
therefore nothing to reproduce verbatim under Outcome A, and nothing was
paraphrased, improved or extended.

**Terminology recorded precisely:**

| Decision | Classification |
|---|---|
| D-3 | **CLOSED — PROCESS / DECISION-DOMAIN** |
| D-4 | **CLOSED — PROCESS / DECISION-DOMAIN** |
| D-3 semantic value | **NOT ESTABLISHED** |
| D-4 semantic value | **NOT ESTABLISHED** |

## 7. Exact provenance

| Claim | File | Section | Commit | Status |
|---|---|---|---|---|
| D-3 gate recorded PENDING/PENDING → OPEN | `review/2026-08-14_P0_6_D3_D4_DECISION_PREPARATION/11_TWO_KEY_REVIEW_GATE.md` | §1 Gate table | `b433708` | CONFIRMED |
| D-4 gate recorded PENDING/PENDING → OPEN | same | §1 Gate table | `b433708` | CONFIRMED |
| Signature blocks blank for both | same | §5 | `b433708` | CONFIRMED |
| D-3 Decision Record entirely blank | `…/09_DECISION_BRIEF.md` | §6 "D-3" | `b433708` | CONFIRMED |
| D-4 Decision Record entirely blank | `…/09_DECISION_BRIEF.md` | §6 "D-4" | `b433708` | CONFIRMED |
| Package states "Neither D-3 nor D-4 is closed by this package" | `…/11_TWO_KEY_REVIEW_GATE.md` | opening line | `b433708` | CONFIRMED |
| No correction pass exists | `git log` on branch | — | — | **EVIDENCE GAP — NO AUTHORITATIVE RECORD FOUND** |
| No formalization record exists | repo-wide search of `review/`, `docs/` | — | — | **EVIDENCE GAP — NO AUTHORITATIVE RECORD FOUND** |
| D-3/D-4 asserted CLOSED | project conversation, HAA statement | D-7 task prompt; this task prompt | not committed | CONFIRMED as a conversation record; **not present in any repository artifact** |

### 7.1 Provenance divergence — flagged, not resolved

**The closure is asserted by the Authority (source 1) but is recorded nowhere in
the repository.** The gate artifact (source 4) still reads PENDING/PENDING.

These are reconcilable without contradiction: a gate that passed whose artifact
was never updated. Source 1 outranks source 4 in the stated priority order, and
this record treats D-3/D-4 as CLOSED accordingly, per the instruction not to
reopen them.

**This is a provenance gap, not a substantive conflict**, so no stop condition
was triggered. It is nonetheless material: an Independent Reviewer reading only
the repository would find both decisions OPEN. **Recorded for the Authority;
this record does not amend the gate artifact** (the task forbids modifying
previous packages).

## 8. Impact on D-7

**EG-1 is not closed, so no D-7 question is unblocked.**

**D7-Q-018 remains BLOCKED.** Precise reason: answering it requires knowing
whether the new digest rule (i) alters the nine-field preimage, or (ii) leaves it
intact and carries a separate component. That is a D-3 semantic value. Sources
1–5 contain no such value, and the inference prohibition forbids deriving one
from the implementation or from the candidate list. **No workaround is proposed
and none was attempted.**

Consequentially unchanged from the D-7 package:

- Candidates **B**, **D** and **E** remain not fully evaluable
  (`…/D7_DECISION_PREPARATION/02_…` §8).
- Candidate **G**'s structural-observability argument remains unevaluable.
- Finding 4 of `…/04_D7_SECURITY_ANALYSIS.md` §13 — downgrade severity — remains
  bounded by EG-1.
- D-7 remains **DECISION-READY with one blocking evidence gap**. That status is
  unchanged by this pass.

**What would close EG-1.** A recorded statement of the accepted D-3 value —
specifically, whether the new rule alters the nine-field preimage. This is a
restatement from the governance record if the values exist outside the
repository, or a new human decision if they do not. **Which of those two applies
is itself unresolved** (§11).

## 9. Impact on D-5

**None.** EG-1 is not closed, so no D-5 dependency previously identified by D-7
is removed.

Had EG-1 closed, it would have removed exactly one item from
`…/05_D7_DEPENDENCY_GRAPH.md` §3.1 — the D7-Q-018 row. The other five D-7 → D-5
prerequisites in that section would have remained.

**G-1 / G-2 / G-3 are untouched** by this pass and remain open. D-5 remains
BLOCKED / NOT READY.

## 10. Final EG-1 status

**EG-1 = NOT CLOSED / GOVERNANCE EVIDENCE GAP**

D-3 and D-4 passed the Two-Key Gate as decision domains, but no normative
semantic values were established in any source available to this pass.

## 11. What remains unresolved

1. Whether accepted D-3/D-4 semantic values exist in a governance record outside
   this repository and outside the conversation — **EVIDENCE GAP**.
2. If they do not, whether establishing them requires a **new** human decision
   rather than a restatement — **unresolved; potentially a stop condition for any
   future pass that needs the values**.
3. D7-Q-018, and with it the full evaluation of D-7 candidates B, D, E and G.
4. Whether the D-3/D-4 gate artifact should be updated to record the closure
   (§7.1) — a governance action for the Authority, not taken here.
5. G-1 / G-2 / G-3 — untouched.

## 12. Explicit non-decisions

```
D-7 strategy selected:        NONE
D-7 discriminator selected:   NONE
Version selected:             NONE
Digest rule selected:         NONE
D-5 strategy selected:        NONE
D-3 semantic value selected:  NONE
D-4 semantic value selected:  NONE
Production code changed:      NO
SPEC-002 changed:             NO
Fixtures created:             NO
ADR created:                  NO
```

Additionally: D-1, D-2, D-3 and D-4 were not reopened or altered; no canonical
encoding, collection semantics, version number, discriminator or migration
strategy was chosen; `aura-guard-v1.3` was not modified or read for this pass;
no previous decision package was modified; no history was amended; no PR created.

---

*No normative effect. This record establishes what the evidence shows about the
D-3/D-4 closures and nothing further.*
