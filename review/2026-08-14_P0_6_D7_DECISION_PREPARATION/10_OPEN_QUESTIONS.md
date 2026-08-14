# 10 — Consolidated Open Questions

Single index of everything left open. Nothing here is answered.

Permitted statuses: **OPEN · EVIDENCE GAP · NORMATIVE STATUS UNRESOLVED ·
DEPENDENT · DECISION-READY.** The statuses *APPROVED*, *SELECTED*,
*RECOMMENDED* and *CLOSED* are not used.

---

## 1. Register (30)

| ID | Subject | Status |
|---|---|---|
| D7-Q-001 | Is a discriminator required at all? | DEPENDENT (G-1/G-2/G-3) |
| D7-Q-002 | What property distinguishes generations? | OPEN |
| D7-Q-003 | Where could it reside? | OPEN |
| D7-Q-004 | Must it be integrity-protected? | OPEN |
| D7-Q-005 | Can an unprotected discriminator safely select the rule? | OPEN |
| D7-Q-006 | Can the verifier bootstrap trust in it? | OPEN |
| D7-Q-007 | Can it be derived externally? | OPEN |
| D7-Q-008 | Can the digest self-describe its generation? | DEPENDENT (EG-1) |
| D7-Q-009 | Interaction with existing v1 entries | DEPENDENT (G-1/G-3) |
| D7-Q-010 | Interaction with new entries | OPEN |
| D7-Q-011 | Behaviour when absent | OPEN |
| D7-Q-012 | Behaviour when unknown | OPEN |
| D7-Q-013 | Behaviour when malformed | OPEN |
| D7-Q-014 | Claims a newer rule | OPEN |
| D7-Q-015 | Claims an older rule | OPEN |
| D7-Q-016 | Can downgrade be detected? | OPEN |
| D7-Q-017 | Old made to appear new? | OPEN |
| D7-Q-018 | **New made to appear old?** | **DEPENDENT — EVIDENCE GAP (EG-1), blocking** |
| D7-Q-019 | Interaction with replay | DEPENDENT (D-6) |
| D7-Q-020 | Interaction with Merkle | OPEN |
| D7-Q-021 | Interaction with TSA | DEPENDENT (D-5, G-4) |
| D7-Q-022 | Disposition of existing tokens | DEPENDENT (D-5) |
| D7-Q-023 | Evidence from production logs | EVIDENCE GAP (G-1) |
| D7-Q-024 | Evidence from external consumers | EVIDENCE GAP (G-2) |
| D7-Q-025 | Evidence from retention obligations | EVIDENCE GAP (G-3) |
| D7-Q-026 | Dependency imposed on D-5 | OPEN |
| D7-Q-027 | Dependency on D-3/D-4 | DEPENDENT — EVIDENCE GAP (EG-1) |
| D7-Q-028 | Dependency on the reference model | DEPENDENT |
| D7-Q-029 | What must be specified before implementation | OPEN |
| D7-Q-030 | What must remain unresolved until D-5 | DEPENDENT |

## 2. Evidence gaps

| ID | Subject | Blocks | Closable by |
|---|---|---|---|
| **EG-1** | Accepted D-3 / D-4 semantic values not supplied | **D7-Q-018 outright**; full evaluation of candidates B, D, E, G | Governance record — restatement, not investigation |
| **G-1** | Do production v1 logs exist? | D7-Q-023; operational viability of C, F, G-`seq`; D-5 | Operator statement |
| **G-2** | External reliance on the logs? | D7-Q-024; distributability of out-of-band context; verifier-agreement requirement | Operator / commercial statement |
| **G-3** | Retention obligations? | D7-Q-025; maintenance horizon for a legacy verifier family | Legal / compliance statement |
| **G-4** | Production TSA tokens beyond the fixtures? | D7-Q-022 weighting | Operator statement |
| **EG-2** | Is verifier agreement across parties required for the entry digest? | `04_…` §6 | Human decision |
| **EG-3** | May the documented exit-code contract gain a new code? | D7-Q-012, D-6 | Human decision |
| **EG-4** | Is trial verification an acceptable accept-rule? | Candidates D, E | Human decision |
| **EG-6** | Does a digest-domain change imply a protocol-version bump per `crypto.rs:25`? | D7-Q-002, `08_…` §3.3 | Human decision |
| **EG-7** | Is log write access operationally constrained? | D7-Q-005 | Operator statement |

## 3. Normative status unresolved

| ID | Item | Why |
|---|---|---|
| **EG-5** | Is serde's ignore-unknown-fields behaviour an intended compatibility posture or incidental? | `AuditEntry` carries no `deny_unknown_fields` (`src/models.rs:50–97`) — CONFIRMED — but no source states intent. Candidate G's structural determination depends on which it is |

## 4. Normative conflicts

**None asserted.** No two sources of confirmed normative status were found to
disagree on any D-7 question. The two conflicts recorded in the D-3/D-4 package
(NC-1 `score` range, NC-2 `action` equality) are out of D-7's scope and are not
restated here as D-7 items.

## 5. Recorded as open decisions (stop conditions encountered)

Each of the following would have required a decision; each was **recorded rather
than decided**, and preparation continued around it.

| # | Item | Recorded at |
|---|---|---|
| 1 | Versioning strategy | `02_…`, D7-Q-001/003 |
| 2 | Discriminator field and value | D7-Q-003, D7-Q-004 |
| 3 | Schema number / digest version | D7-Q-002 |
| 4 | Hash-domain identifier | D7-Q-008, `02_…` D |
| 5 | Migration / legacy-compatibility strategy | Referenced as D-5 only; `05_…` §3 |
| 6 | Replay strategy and exit codes | `07_…` §2.3–2.4, handed to D-6 |
| 7 | Canonical encoding / collection semantics | Not touched — D-3/D-4 are CLOSED and their values were not inferred |
| 8 | Cryptographic construction | Not selected |

## 6. Stop conditions — status

| Stop condition | Triggered? |
|---|---|
| Evidence requiring D-1 to be reopened | **No** |
| Evidence requiring D-2 to be reopened | **No** |
| D-3 or D-4 semantics must be *selected* to continue | **No** — but their *accepted values* are required to close D7-Q-018. Recorded as EG-1; nothing was inferred, and preparation continued |
| Implementation modification necessary | **No** |
| A normative conflict unclassifiable without human authority | **No** — none asserted |
| Repository lacks evidence to distinguish candidates | **Partially** — B, D and E cannot be fully distinguished until EG-1 closes. Recorded, not worked around |
| A production-log / external-consumer / retention fact required but unavailable | **Yes, for D-5-facing questions** — G-1/G-2/G-3 recorded as gaps; D-7's mechanism analysis did not depend on them |

**No stop condition forced abandonment of the package.** The two that engaged
(EG-1, and G-1/G-2/G-3) are recorded as blockers on specific questions rather
than resolved by assumption.
