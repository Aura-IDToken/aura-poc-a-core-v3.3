# D-3 / D-4 — Formal Decision Record

**Document class:** governance record. Recording only — no decision analysis, no
semantic selection.
**Recorded by:** Claude, at the direction of the Human Architectural Authority.
Claude is neither the Authority nor the Independent Reviewer and entered no key.

---

## 1. Decision identity

| Field | Value |
|---|---|
| Decisions | **D-3** (canonical representation) and **D-4** (collection semantics) |
| Programme | **P0-6** — Guard violations integrity |
| Repository | `AuraIDToken/aura-poc-a-core-v3.3` |
| Branch | `claude/p0-1-test-review-qtkye2` |
| Date of record | 2026-08-14 |
| Source decision context | Human Architectural Authority's explicit acceptance, together with the completed Independent Review, of the D-3/D-4 decision-preparation domain and its review process |
| Subject matter under P0-6 | Follows D-1 (violations ∈ integrity domain, CLOSED) and D-2 (integrity-domain contract, CLOSED) |

## 2. Two-Key status

| Key | Status |
|---|---|
| Human Architectural Authority | **YES** |
| Independent Review | **YES** |
| **Two-Key Gate** | **PASSED** |

## 3. Decision status

| Decision | Status |
|---|---|
| **D-3** | **CLOSED — DECISION DOMAIN** |
| **D-4** | **CLOSED — DECISION DOMAIN** |

The closure means the decision-preparation domain and its review process have
passed the Two-Key Gate.

## 4. Semantic-value status

| Item | Status |
|---|---|
| D-3 concrete semantic value | **NOT ESTABLISHED** |
| D-4 concrete semantic value | **NOT ESTABLISHED** |

This distinction is load-bearing and must be carried forward verbatim wherever
these closures are cited:

> **CLOSED — DECISION DOMAIN** is **not** equivalent to
> **CLOSED — SEMANTIC VALUE ESTABLISHED.**

## 5. Explicit non-decisions

This record does **not** establish, select, imply or authorise any of the
following:

- canonical byte encoding
- serialization format
- ordering rule
- set / multiset / ordered collection semantics
- duplicate handling
- float representation
- `NaN` / ±Infinity handling
- hash-domain representation
- version marker
- replay semantics
- migration semantics
- any concrete digest construction

No such value has been derived, and none may be derived, from: implementation
behaviour; the candidate lists in the preparation package; existing code
comments; `mathematical_foundation.md`; RI-PY; ADR-0001; any previous Claude
recommendation; or engineering judgement of any agent.

**Any statement of a concrete D-3 or D-4 semantic value that cites this record as
its authority is invalid.**

## 6. Dependency state

| Relation / decision | State |
|---|---|
| **D-3 ↔ D-4** | **STRONG BIDIRECTIONAL DEPENDENCY (FOR JOINT CLOSURE)** |
| **D-7** | **NOT CLOSED / NOT ADVANCED** |
| **D-5** | **BLOCKED** |
| **D-6** | **NOT ADVANCED** |

Prior closures, unchanged by this record: **D-1 CLOSED**, **D-2 CLOSED**.

## 7. Governance boundary

Establishing the concrete semantic values for D-3 and D-4 requires a **separate
decision process**, culminating in its own Two-Key Gate. Those values:

- cannot be inferred from this closure record;
- cannot be inferred from the fact that the domain is closed;
- cannot be supplied by an implementing agent;
- cannot be treated as settled by any downstream package that cites this record.

Any future artifact asserting a D-3 or D-4 semantic value must cite that separate
decision, not this one.

## 8. Provenance

| Source | Location | Commit | Role |
|---|---|---|---|
| Decision-preparation package | `review/2026-08-14_P0_6_D3_D4_DECISION_PREPARATION/` (12 documents) | `b433708` | The prepared decision space reviewed under the gate |
| Two-Key Gate artifact in that package | `…/11_TWO_KEY_REVIEW_GATE.md` §1 | `b433708` | Records **PENDING / PENDING → OPEN** — the state at the time the package was written |
| Decision Record tables in that package | `…/09_DECISION_BRIEF.md` §6 | `b433708` | Blank at the time of writing — no values were entered |
| Independent-review / evidence-closure pass | `review/2026-08-14_P0_6_D7_EG1_CLOSURE/EG1_CLOSURE_RECORD.md` | `049a4a3` | Established, by inspection of the source-priority order, that the closures are process/domain closures and that no semantic values exist in any available record (Outcome B) |
| Downstream package citing the closures | `review/2026-08-14_P0_6_D7_DECISION_PREPARATION/` | `817272a` | Consumed D-3/D-4 as closed domains; recorded EG-1 because no values were available |

### 8.1 Relationship to the prior PENDING gate tables

The preparation package's gate tables record **PENDING / PENDING** and its
signature blocks are blank. That is the accurate historical state of those
artifacts at the time they were written.

**This document is the subsequent human governance record of the closure. It does
not rewrite, amend or supersede historical evidence.** The prior packages were
deliberately left untouched, so the record shows both the state at preparation
time and the closure recorded afterwards. A reader encountering the PENDING
tables should read them together with this record.

## 9. Implementation boundary

```
PRODUCTION CODE CHANGE:        NONE
SPEC-002 CHANGE:               NONE
ADR ESTABLISHING SEMANTICS:    NONE
FIXTURES CREATED:              NONE
NORMATIVE SEMANTICS SELECTED:  NONE
```

Additionally: `aura-guard-v1.3` was not modified or read for this record; no
previous decision package was modified; no history was amended; no pull request
was created; D-1, D-2, D-3 and D-4 were not reopened; D-5, D-6 and D-7 were not
advanced.

## 10. Next gate

The next required action is **not** implementation and **not** D-7.

The next required action is **preparation of the concrete semantic decision space
for D-3 and D-4**, followed by a further Two-Key Gate over those concrete values.

**D-7 remains blocked** until its dependencies are actually satisfied. Its
blocking gap (EG-1) is unaffected by this record: EG-1 requires the D-3 semantic
value, which §4 records as NOT ESTABLISHED. Recording the domain closure does not
close EG-1.

---

*This record documents governance state only. It confers no normative semantics
and authorises no implementation.*
