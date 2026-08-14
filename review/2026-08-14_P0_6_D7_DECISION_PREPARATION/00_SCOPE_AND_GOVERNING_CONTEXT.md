# 00 — Scope and Governing Context

**Package:** P0-6 — D-7 decision preparation (Versioning / Discriminator)
**Date:** 2026-08-14
**Prepared by:** Claude — evidence and decision-preparation agent
**Role disclaimer:** NOT the Human Architectural Authority. NOT the Independent
Reviewer. This package prepares a decision space; it does not decide.

## 1. Provenance of evidence

| Field | Value |
|---|---|
| Primary repository | `AuraIDToken/aura-guard-v1.3` |
| Commit | `443f72e58483c3ea6112ea517647cc0dbf459960` |
| Access | pristine read-only clone; unmodified, verified at package time |
| Crate version | `1.3.0` (`Cargo.toml:3`) |
| Secondary repository | `AuraIDToken/aura-poc-a-core-v3.3`, branch `claude/p0-1-test-review-qtkye2` |

Every material claim below and in the sibling files identifies repository, file,
line/section and source status. No claim rests on memory.

## 2. Governing state — CLOSED, not reopened

| Decision | State | Meaning taken as authoritative |
|---|---|---|
| **D-1** | YES / CLOSED | `violations` MUST belong to the integrity domain |
| **D-2** | YES / CLOSED | The integrity-domain contract has been accepted |
| **D-3** | YES / CLOSED | Canonical-representation package passed the Two-Key Gate |
| **D-4** | YES / CLOSED | Collection-semantics package passed the Two-Key Gate |
| **D-5** | BLOCKED / NOT READY | Migration and compatibility strategy cannot yet be selected |
| **D-6** | OPEN | Replay behaviour / reporting |
| **D-7** | **OPEN — prepared here** | Versioning / discriminator |

**Constraint honoured throughout.** D-3 and D-4 are closed *as decision domains*.
Their accepted **semantic values were not supplied to this package**, and this
package does **not** invent, infer or assume them. Where a D-7 property depends
on a specific D-3/D-4 value, the dependency is named and the value is left
unstated. See `05_…` E-04 and `06_…` EG-1.

## 3. The D-7 question

> How can an audit verifier determine which integrity/digest rule applies to a
> given `AuditEntry`, especially across a transition from the current v1 digest
> domain to the future D-1/D-2/D-3/D-4-defined integrity domain?

## 4. Evidence classification

| Status | Meaning |
|---|---|
| **CONFIRMED** | Verified at a cited `file:line` in the pinned commit, or by an executed read-only command |
| **IMPLEMENTATION-DERIVED** | Describes current behaviour. Establishes no requirement, confers no authority |
| **INFERENCE** | A conclusion reasoned from CONFIRMED facts, labelled as reasoning rather than observation |
| **EVIDENCE GAP** | Not determinable from the available sources |
| **NORMATIVE STATUS UNRESOLVED** | A source exists but its normative force is undetermined |
| **NORMATIVE CONFLICT** | Two sources **both of confirmed normative status** disagree. Used only under that condition |

### 4.1 Non-decision rule

No versioning strategy, discriminator field, discriminator value, schema number,
digest version, hash-domain identifier, migration strategy, legacy-compatibility
strategy, replay strategy, canonical encoding, collection semantic or
cryptographic construction is selected in this package. Every option carries the
label **NON-NORMATIVE CANDIDATE** and is unranked.

The words *recommended, preferred, best, safest, correct, simplest* do not appear
as this package's characterisation of any option. Where such a word occurs inside
a quotation from a repository source, it is marked as a quotation.

Explicitly **not assumed**: that `schema` is the answer; that a new `schema`
value is the answer; that the discriminator must be inside the digest. All three
are decision questions (D7-Q-003, D7-Q-004).

## 5. Sources actually read for this package

Scope was limited to what D-7 requires. No full repository audit; RD-1, the D-2
analysis and the whole D-3/D-4 analysis were not repeated.

| Source | Used for |
|---|---|
| `src/chain.rs` (`:18–20`, `:25–49`, `:53–65`, `:71–92`) | current digest rule and verification loop |
| `src/models.rs` (`:32–42`, `:50–97`) | `AuditEntry` shape, serde attributes |
| `src/api/audit.rs` (`:52–53`, `:113–149`) | entry construction, `schema` literal |
| `src/log_writer.rs` (`:88–105`, `:151–170`) | persistence and parse path |
| `src/crypto.rs` (`:8–12`, `:16`, `:25–30`) | hashing helpers, genesis constant |
| `src/segment.rs` (`:44–50`, `:91–158`, `:335–405`) | segment schema, Merkle, TSA imprint |
| `src/sealer.rs` (`:100`) | manifest schema rejection |
| `src/merkle.rs` (`:9–15`, `:29–34`) | domain-separation precedent |
| `src/bin/aura_replay.rs` (`:113–119`, `:134–153`, `:175`, `:194`, `:213`) | verifier behaviour |
| `src/bin/aura_seal.rs` (`:90–131`, `:338–365`) | externally-selected verification mode |
| `tests/tst_verify.rs`, `tests/fixtures/tsa/*` | real RFC 3161 evidence |
| `docs/exit-codes.md` | documented exit-code contract |
| `docs/segments-and-timestamping.md` (`§Manifest schema`, `§Backward-compatible imprint-only mode`) | in-repo compatibility precedent |
| `docs/adrs/0001-hash-chain.md` | governing ADR for the chain |
| `review/2026-08-14_P0_6_D2_D5_DECISION_PREPARATION/` | D-5 material, prior evidence |
| `review/2026-08-14_P0_6_D3_D4_DECISION_PREPARATION/` | D-3/D-4 question structure |

## 6. Corrections to prior evidence

**CORRECTION TO PRIOR EVIDENCE — 1.**
`docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` §2.8 (this repository) states the
RFC 3161 exposure is "structural and latent". **Reason for correction:** real
FreeTSA tokens exist as committed fixtures
(`tests/fixtures/tsa/segment-001.tsr`, `segment-002.tsr`) and are verified in
`tests/tst_verify.rs` against an imprint recomputed inline from
`SegmentManifest::segment_chain_preimage` — CONFIRMED. The narrower fact that
`tsa_message_imprint()` has no in-tree caller remains accurate. This correction
was first recorded in `review/2026-08-14_P0_6_D2_D5_DECISION_PREPARATION/00_…`
§5.1 and is restated here because D-7 candidates turn on it (`08_…`). **The ADR
is not silently amended by this package.**

No other prior-package error was identified while preparing D-7.

## 7. Package contents

| File | Purpose |
|---|---|
| `00_SCOPE_AND_GOVERNING_CONTEXT.md` | This file |
| `01_D7_VERSIONING_REGISTER.md` | D7-Q-001 … D7-Q-030 in the A–G register format |
| `02_D7_CANDIDATES.md` | Candidate mechanisms A–G, each with the 14 required attributes |
| `03_D7_CONSEQUENCE_MATRIX.md` | Cross-candidate consequence matrix |
| `04_D7_SECURITY_ANALYSIS.md` | The twelve required threat models |
| `05_D7_DEPENDENCY_GRAPH.md` | Edges incl. the evidence-backed D-7 → D-5 graph |
| `06_D7_EVIDENCE_REQUIREMENTS.md` | Gaps, including G-1/G-2/G-3 |
| `07_D7_REFERENCE_AND_REPLAY_IMPACT.md` | Reference-model and replay/verifier impact |
| `08_D7_TSA_MERKLE_IMPACT.md` | Merkle and RFC 3161 continuity |
| `09_DECISION_BRIEF.md` | Brief for the two-key review |
| `10_OPEN_QUESTIONS.md` | Consolidated index |
| `11_TWO_KEY_REVIEW_GATE.md` | Gate prepared, not executed |

## 8. Boundaries observed

No production code modified in either repository. No change to `chain.rs`,
`models.rs`, `segment.rs`, `sealer.rs`, the verifier, replay, migration tooling,
`core/`, SPEC-002, the Constitution, fixtures, golden vectors or production
schemas. No ADR establishing D-7. No PR. No new code executed against the Guard
clone — all evidence was obtained by inspection, per the instruction to prefer
evidence inspection over execution.
