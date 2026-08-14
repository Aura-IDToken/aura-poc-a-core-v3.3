# 11 — Two-Key Review Gate

**Prepared, NOT executed.** No key is entered on behalf of any human. D-7 is not
closed by this package.

---

## 1. Gate

| Decision | Human Architectural Authority | Independent Review | Final Status |
|---|---|---|---|
| **D-7** | **PENDING** | **PENDING** | **OPEN** |

```
Human Architectural Authority : PENDING
Independent Review            : PENDING
Final Decision                : NONE
Normative Change              : NONE
Production Code Change        : NONE
```

Only after **both** keys read YES may D-7 become CLOSED. One key alone does not
close it. Neither key may be entered by Claude.

## 2. Process state

| Decision | HAA | Independent Review | Final Status |
|---|---|---|---|
| D-1 | YES | YES | CLOSED |
| D-2 | YES | YES | CLOSED |
| D-3 | YES | YES | CLOSED |
| D-4 | YES | YES | CLOSED |
| **D-7** | **PENDING** | **PENDING** | **OPEN** |
| D-5 | — | — | BLOCKED / NOT READY (G-1, G-2, G-3) |
| D-6 | — | — | OPEN |

## 3. The package is ready for

1. **Independent Review**
2. **Human Architectural Authority review**
3. **Two-Key Gate**

## 4. What each key is asked to consider

- The 30-question register (`01_…`) and its status distribution.
- Seven candidate mechanisms with all fourteen required attributes, and the
  viability assessment in `02_…` §8.
- The consequence matrix (`03_…`) and twelve security models (`04_…`).
- The dependency graph, including the evidence-backed **D-7 ↔ D-5** relationship
  (`05_…` §3).
- **EG-1 first.** One register question — D7-Q-018, *can a new entry be made to
  appear as an old entry?* — is **blocked** because the accepted D-3 values were
  not supplied to this package. It is closable by restatement from the governance
  record, and its answer changes the severity assessment for candidates D and E.
- The external gaps **G-1 / G-2 / G-3 / G-4**, which are shared with D-5 and
  cannot be closed from the repository.

## 5. Attestations for this package

| Statement | Value |
|---|---|
| Decision taken by Claude | NONE |
| Versioning strategy selected | NONE |
| Discriminator field selected | NONE |
| Discriminator value / schema number selected | NONE |
| Digest version selected | NONE |
| Hash-domain identifier selected | NONE |
| Migration strategy selected | NONE |
| Legacy-compatibility strategy selected | NONE |
| Replay strategy selected | NONE |
| Canonical encoding selected | NONE |
| Collection semantic selected | NONE |
| Cryptographic construction selected | NONE |
| Recommendation offered | NONE |
| Candidates ranked | NO |
| Production code changed | NO |
| `aura-guard-v1.3` changed | NO |
| `chain.rs` / `models.rs` / `segment.rs` / `sealer.rs` changed | NO |
| Verifier / replay / migration tooling changed | NO |
| `core/` changed | NO |
| SPEC-002 changed | NO |
| Constitution changed | NO |
| Fixtures or golden vectors created | NO |
| Normative test vectors created | NO |
| ADR establishing D-7 created | NO |
| D-1 / D-2 reopened | NO |
| D-3 / D-4 semantics invented or inferred | NO |
| D-5 resolved or advanced to selection | NO |
| D-6 resolved | NO |
| New code executed against the Guard clone | NO — evidence obtained by inspection |
| Pull request created | NO |
| Prior packages silently corrected | NO — one correction recorded explicitly (`00_…` §6) |

## 6. Signature block — to be completed by the key holders only

```
D-7 — VERSIONING / DISCRIMINATOR

HUMAN ARCHITECTURAL AUTHORITY
  Decision            : ______________________
  Candidate / combo   : ______________________
  Name                : ______________________
  Date                : ______________________
  Basis               : ______________________

INDEPENDENT REVIEW
  Decision            : ______________________
  Concurs with combo  : ______________________
  Name                : ______________________
  Date                : ______________________
  Basis               : ______________________

EG-1 RESOLUTION (D-3 values restated)
  Supplied by         : ______________________
  Effect on D7-Q-018  : ______________________

FINAL STATUS         : ______________________
```

---

*No normative effect. No decision recorded. Gate remains PENDING / PENDING.*
