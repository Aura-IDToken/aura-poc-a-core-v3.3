# 10 — Consolidated Open Questions

Single index of everything left open by this package. Nothing here is answered.

Permitted statuses: **OPEN · EVIDENCE GAP · NORMATIVE CONFLICT · READY FOR HUMAN
DECISION.** The statuses *APPROVED*, *SELECTED* and *RECOMMENDED* are not used.

---

## 1. D-3 register (26)

| ID | Subject | Status |
|---|---|---|
| D3-Q-001 | Character encoding | OPEN |
| D3-Q-002 | String representation | OPEN |
| D3-Q-003 | Integer representation | OPEN |
| D3-Q-004 | Boolean representation (no boolean field exists today) | OPEN |
| D3-Q-005 | Timestamp representation | OPEN |
| D3-Q-006 | Float / `f32` representation | OPEN |
| D3-Q-007 | `None` / null representation | OPEN |
| D3-Q-008 | Empty-value representation | OPEN |
| D3-Q-009 | Separators / delimiters | OPEN |
| D3-Q-010 | Escaping | OPEN |
| D3-Q-011 | Field ordering | OPEN |
| D3-Q-012 | Collection ordering (representation layer) | OPEN |
| D3-Q-013 | Nested structures | OPEN |
| D3-Q-014 | Duplicate values (representation layer) | OPEN |
| D3-Q-015 | Unicode normalization | OPEN |
| D3-Q-016 | Whitespace | OPEN |
| D3-Q-017 | Numeric special values | **NORMATIVE CONFLICT** (NC-1) |
| D3-Q-018 | `NaN` / ±Infinity | **EVIDENCE GAP** (EG-3) |
| D3-Q-019 | Byte encoding of the final preimage | OPEN |
| D3-Q-020 | Length-prefix vs delimiter | OPEN |
| D3-Q-021 | Ambiguity / injectivity | OPEN |
| D3-Q-022 | Hash-domain separation | OPEN |
| D3-Q-023 | Version marker interaction | OPEN |
| D3-Q-024 | Backward compatibility implications | OPEN |
| D3-Q-025 | Replay implications | OPEN |
| D3-Q-026 | Cross-language equivalence | **EVIDENCE GAP** (EG-2) |

## 2. D-4 register (15)

| ID | Subject | Status |
|---|---|---|
| D4-Q-001 | Ordered list? | OPEN |
| D4-Q-002 | Unordered set? | OPEN |
| D4-Q-003 | Multiset? | OPEN |
| D4-Q-004 | Canonically sorted collection? | OPEN |
| D4-Q-005 | First-match semantics normative? | OPEN |
| D4-Q-006 | All-match semantics required? | **EVIDENCE GAP** (EG-7) |
| D4-Q-007 | Duplicate violations | OPEN |
| D4-Q-008 | Empty collection | OPEN |
| D4-Q-009 | Omitted / `None` | OPEN |
| D4-Q-010 | Semantic equivalence | **NORMATIVE CONFLICT** (NC-2) |
| D4-Q-011 | Order-changing mutation | OPEN |
| D4-Q-012 | Duplicate insertion | OPEN |
| D4-Q-013 | Duplicate removal | OPEN |
| D4-Q-014 | Violation removal | OPEN |
| D4-Q-015 | Violation addition | OPEN |

## 3. Evidence gaps (9)

| ID | Subject | Closable by |
|---|---|---|
| EG-1 | Explicit D-2 membership list not supplied to this package | Governance record |
| EG-2 | Is cross-language reproduction of the entry digest required? | Human decision |
| EG-3 | `serde_yaml` → `f32` → `serde_json` behaviour for `.nan` / `.inf` | Executed experiment, once authorized |
| EG-4 | Is the `action` value domain closed and case-normalized? | Human decision |
| EG-5 | Is `score` intended to be constrained to 0.0–1.0? | Human decision |
| EG-6 | Is YAML declaration order audit-significant? | Human decision |
| EG-7 | Is audit completeness (all matches) required? | Human decision |
| EG-8 | Is SHADOW_SPEC v1.0 normative for evidence text? | Specification review |
| EG-9 | Does any specification define the entry digest? | Archival search |

## 4. Normative conflicts (3) — flagged, not resolved

| ID | Conflict | Sources |
|---|---|---|
| NC-1 | `score` documented as 0.0–1.0; no validation enforces it | `src/policy.rs:40`, `src/models.rs:37` vs `src/policy.rs:283` |
| NC-2 | `action` compared case-insensitively but stored verbatim | `src/engine.rs:44` vs `:51` |
| NC-3 | Two `request_id` doc-comments disagree on provenance | `src/models.rs:60–62` vs `:63–64`, vs `src/api/audit.rs:52` |

## 5. Recorded as open decisions (stop conditions encountered)

Per the task's stop conditions, each of the following was **recorded rather than
decided**, and preparation continued around it:

| # | Item that would have required a decision | Recorded at |
|---|---|---|
| 1 | Choice of canonical format | `03_…`, D3-Q-002/009/020 |
| 2 | Choice of ordered / set / multiset | `04_…`, D4-Q-001/002/003 |
| 3 | Choice of sorting rule | D4-Q-004, D3-Q-012 |
| 4 | Choice of float representation | D3-Q-006/017/018 |
| 5 | Choice of hash domain | D3-Q-022 |
| 6 | Resolution of NC-1 and NC-2 | `08_…` §2 |
| 7 | Resolution of D-5 and D-7 | Referenced only; `06_…` E-04/E-05/E-06/E-09 |
| 8 | Creation of Reference Model artifacts | `09_…` §4 — scoped, not built |

## 6. Questions for the Authority, in the order the graph reaches them

Stated as questions, not as a sequence to follow.

1. Is byte-identical reproduction by an independent implementation a requirement
   for the **entry** digest, as it is documented to be for the Merkle layer?
   *(EG-2 — shapes every D-3 candidate's cost.)*
2. Is YAML authoring order audit-significant? *(EG-6 — most directly determines
   the D-4 class.)*
3. Does `confidence` participate in the digest, and in what form? *(D3-Q-006 —
   the only float in the record.)*
4. Are duplicates meaningful? *(D4-Q-007 — the only place a candidate reduces
   detection below what D-1 enabled.)*
5. Is absent distinguishable from `None`? *(D3-Q-007 / D4-Q-009 — answering
   "yes" forecloses faithful migration of existing records.)*
6. Is injectivity a mandated property with a proof obligation? *(D3-Q-021.)*
7. Is a version marker bound inside the digest? *(D3-Q-023 — the D-3 → D-7 edge.)*
