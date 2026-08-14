# 00 — Scope and Governing Context

**Package:** P0-6 — D-3 + D-4 decision preparation
**Date:** 2026-08-14
**Prepared by:** Claude (conformance audit role, per `CLAUDE.md`)
**Evidence commit:** `AuraIDToken/aura-guard-v1.3` @ `443f72e58483c3ea6112ea517647cc0dbf459960`
**Output class:** evidence + options + consequences. **No decision. No normative semantics.**

---

## 1. Closed inputs — not reopened

| Decision | Outcome | Gate | Status |
|---|---|---|---|
| **D-1** | YES — `violations` ∈ integrity domain | HAA = YES, Independent Review = YES | **CLOSED** |
| **D-2** | YES — integrity domain contract closed | HAA = YES, Independent Review = YES | **CLOSED** |

These are accepted facts. This package does **not** re-audit them, does not
re-argue membership, and does not re-derive the D-1 mutation evidence. The
question "does `violations` belong to the integrity domain" is settled: **YES**.

## 2. Current decision state

| Decision | Subject | Status |
|---|---|---|
| D-1 | membership | CLOSED |
| D-2 | integrity domain contract | CLOSED |
| **D-3** | **canonical representation** | **OPEN — prepared here** |
| **D-4** | **collection semantics** | **OPEN — prepared here** |
| D-5 | compatibility / migration | BLOCKED — NOT READY (G-1/G-2/G-3) |
| D-6 | replay behaviour | OPEN |
| D-7 | version discriminator | OPEN |

Agreed sequence: **D-2 (closed) → D-3 + D-4 → D-7 → D-5.**

## 3. What D-3 and D-4 decide

- **D-3 — canonical representation.** *How* is data in the integrity domain
  reduced to bytes, such that two independent implementations produce an
  identical digest for an identical `AuditEntry`?
- **D-4 — collection semantics.** *What* is `violations` as a collection —
  what does membership, order, multiplicity and emptiness mean within it?

## 4. Distinctions that must not be conflated

| Layer | Question | Decision | State |
|---|---|---|---|
| 1. Integrity membership | *what* is protected | D-2 | CLOSED |
| 2. Semantic meaning | *what the data means* as a collection | D-4 | OPEN |
| 3. Canonical representation | *how* it becomes bytes for hashing | D-3 | OPEN |
| 4. Serialization | how it is stored/transported on the wire | (separable; not D-3 by definition) | — |
| 5. Versioning | which rule applies to a given record | D-7 | OPEN |
| 6. Migration / compatibility | what happens to existing records | D-5 | BLOCKED |

**Layer 3 ≠ layer 4.** The existing JSON serialization is a storage format. It
is **not** established as a canonical hashing representation, and this package
does not treat it as one.

## 5. Evidence discipline

Every claim carries a source, a path, a section/line where available, and a
status. Statuses used:

| Status | Meaning |
|---|---|
| **CONFIRMED** | Verified at a cited `file:line` in the pinned commit, or by an executed command |
| **IMPLEMENTATION-DERIVED** | Describes how the code currently behaves. Establishes no requirement and confers no authority |
| **NORMATIVE** | Stated by an authoritative source (closed decision, accepted ADR, specification) |
| **NON-NORMATIVE** | Illustrative, advisory, or draft material with no binding force |
| **EVIDENCE GAP** | Not determinable from the sources of truth |
| **NORMATIVE CONFLICT** | Authoritative sources disagree. Flagged, **not resolved** |

### 5.1 Prohibited inference

The current implementation is **not** normative authority. Specifically, and
stated once so it need not be repeated at every occurrence:

- `SEP = "|"` (`src/chain.rs:20`) is **IMPLEMENTATION-DERIVED / NON-NORMATIVE**.
  It is not assumed to be a correct normative separator.
- The existing `serde_json` output (`src/log_writer.rs:96`) is
  **IMPLEMENTATION-DERIVED / NON-NORMATIVE**. It is not assumed canonical.
- YAML declaration order of violations (`src/policy.rs:233–237`,
  `src/engine.rs:19`) is **IMPLEMENTATION-DERIVED**, not a normative ordering.
- First-match behaviour (`src/engine.rs:28`) is **IMPLEMENTATION-DERIVED**, not
  a normative collection rule.

### 5.2 Vocabulary constraint

The words *recommended, preferred, best, safest, simplest, correct* are not used
in this package to characterise any option. Where such a word appears in an
authoritative source it is presented as a **quotation**, attributed, and never as
this package's own position.

## 6. Boundaries observed

Not done, by instruction: no canonical format chosen; no ordered/set/multiset
chosen; no sorting rule chosen; no float representation chosen; no hash domain
chosen; no change to `chain.rs`, `models.rs`, `segment.rs`, `sealer.rs`, any
production code, SPEC-002, or the constitution; no fixtures; no normative ADR;
no resolution of D-5, D-6 or D-7; no re-opening of D-1 or D-2; no PR.

Where the work would have required any of the above, the item is **RECORDED AS
OPEN DECISION** and preparation continues around it.

## 7. Package contents

| File | Purpose |
|---|---|
| `00_SCOPE_AND_GOVERNING_CONTEXT.md` | This file |
| `01_D3_CANONICAL_REPRESENTATION_REGISTER.md` | Observed representation + D3-Q-001…026 register |
| `02_D4_COLLECTION_SEMANTICS_REGISTER.md` | Observed semantics + D4-Q-001…015 register |
| `03_D3_CANDIDATES.md` | Representation candidate classes A–G |
| `04_D4_CANDIDATES.md` | Collection-semantics candidate classes A–F |
| `05_D3_D4_CONSEQUENCE_MATRIX.md` | Cross-consequences of D-3 × D-4 combinations |
| `06_D3_D4_DEPENDENCY_GRAPH.md` | Edges with SOURCE / REASON / STATUS |
| `07_D3_D4_SECURITY_TEST_MATRIX.md` | T-D4-01…12 test design (design only) |
| `08_EVIDENCE_REQUIREMENTS.md` | Evidence gaps and what closes them |
| `09_DECISION_BRIEF.md` | Summary, Reference Model scope, status block |
| `10_OPEN_QUESTIONS.md` | Consolidated open questions |
| `11_TWO_KEY_REVIEW_GATE.md` | Gate table — PENDING / PENDING |

## 8. Sources of truth

1. D-1 = YES (CLOSED); D-2 = YES (CLOSED) — accepted inputs
2. `review/2026-08-14_P0_6_D2_D5_DECISION_PREPARATION/` (D-2/D-5 package)
3. `review/2026-08-11_ENGINEERING_BASELINE/GUARD-G1_INTEGRITY_DESIGN_BRIEF.md`
4. `docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` (DRAFT / NON-NORMATIVE)
5. `aura-guard-v1.3` @ `443f72e` — pristine read-only clone
6. `docs/adrs/0001-hash-chain.md` in the Guard repository (Accepted, still current)

**EVIDENCE GAP — carried forward.** The exact field membership closed by D-2 was
not supplied to this package in machine-readable form. Where a D-3 or D-4
question's scope depends on which fields D-2 admitted, this is marked at the
question. It does not block preparation: D-3's element list and D-4's semantics
are the same regardless of whether `schema` / `audit_id` / `request_id` were
admitted; only the *breadth of application* varies.
