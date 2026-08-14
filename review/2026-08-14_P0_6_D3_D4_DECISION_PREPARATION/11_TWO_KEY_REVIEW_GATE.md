# 11 — Two-Key Review Gate

**Neither D-3 nor D-4 is closed by this package.** No key is entered on behalf of
any human. Both columns below are filled in only by their respective holders.

---

## 1. Gate table

| Decision | Human Architectural Authority | Independent Review | Final Status |
|---|---|---|---|
| **D-3** | PENDING | PENDING | **OPEN** |
| **D-4** | PENDING | PENDING | **OPEN** |

A decision closes only when **both** keys read YES. One key alone does not close
it, and neither key may be entered by Claude.

## 2. Preceding decisions, for context

| Decision | Human Architectural Authority | Independent Review | Final Status |
|---|---|---|---|
| D-1 | YES | YES | CLOSED |
| D-2 | YES | YES | CLOSED |
| D-3 | PENDING | PENDING | **OPEN** |
| D-4 | PENDING | PENDING | **OPEN** |
| D-5 | — | — | BLOCKED / NOT READY (G-1, G-2, G-3) |
| D-6 | — | — | OPEN |
| D-7 | — | — | OPEN |

## 3. What each key is being asked to consider

**For D-3:** the 26-element register (`01_…`), seven candidate classes
(`03_…`), the consequence matrix (`05_…`), and the evidence gaps EG-1, EG-2,
EG-3, EG-5, EG-8, EG-9 plus NC-1.

**For D-4:** the 15-question register (`02_…`), six candidate classes
(`04_…`), the twelve-case security test design (`07_…`), and the evidence gaps
EG-4, EG-6, EG-7 plus NC-2.

**For both:** D-3 and D-4 are coupled **hard and bidirectionally** (`06_…`
E-03). Closing one without the other silently constrains the other's option
space. Whether they are gated as one decision or two is itself the Authority's
call and is **not decided here**.

## 4. Attestations for this package

| Statement | Value |
|---|---|
| Decision taken by Claude | NONE |
| Normative semantics selected | NONE |
| Canonical format selected | NONE |
| Collection semantics selected | NONE |
| Sorting rule selected | NONE |
| Float representation selected | NONE |
| Hash domain selected | NONE |
| Recommendation offered | NONE |
| Production code changed | NO |
| `aura-guard-v1.3` changed | NO |
| `chain.rs` / `models.rs` / `segment.rs` / `sealer.rs` changed | NO |
| SPEC-002 changed | NO |
| Constitution changed | NO |
| D-2 changed or reopened | NO |
| D-1 reopened | NO |
| Normative ADR created | NO |
| Fixtures created | NO |
| Tests implemented | NO |
| D-5 / D-6 / D-7 resolved | NO |
| Normative conflicts resolved | NO — 3 flagged, 0 resolved |
| Pull request created | NO |

## 5. Signature blocks — to be completed by their holders only

### D-3

```
HUMAN ARCHITECTURAL AUTHORITY
  Decision      : ______________________
  Name          : ______________________
  Date          : ______________________
  Basis         : ______________________

INDEPENDENT REVIEW
  Decision      : ______________________
  Name          : ______________________
  Date          : ______________________
  Basis         : ______________________

FINAL STATUS    : ______________________
```

### D-4

```
HUMAN ARCHITECTURAL AUTHORITY
  Decision      : ______________________
  Name          : ______________________
  Date          : ______________________
  Basis         : ______________________

INDEPENDENT REVIEW
  Decision      : ______________________
  Name          : ______________________
  Date          : ______________________
  Basis         : ______________________

FINAL STATUS    : ______________________
```

---

*No normative effect. No decision recorded. Both gates remain PENDING / PENDING.*
