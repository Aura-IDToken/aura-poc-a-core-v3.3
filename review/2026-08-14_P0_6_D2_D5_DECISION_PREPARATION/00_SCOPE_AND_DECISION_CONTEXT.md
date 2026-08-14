# 00 — Scope and Decision Context

**Package:** P0-6 — D-2 + D-5 decision preparation
**Date:** 2026-08-14
**Prepared by:** Claude (conformance audit role, per `CLAUDE.md`)
**Evidence commit:** `AuraIDToken/aura-guard-v1.3` @ `443f72e58483c3ea6112ea517647cc0dbf459960`
**Status:** decision-preparation only. No normative effect. No decision taken.

---

## 1. Accepted architectural input

**D-1 = YES — CLOSED.** Passed the Two-Key Gate (Human Architectural Authority:
YES; Independent Review: YES).

> `violations` **is** part of the cryptographic integrity domain of `AuditEntry`.

D-1 is not reinterpreted, re-argued or re-evidenced anywhere in this package. It
is an input.

**What D-1 did not decide.** D-1 answers only *whether* `violations` belongs to
the integrity domain. It selects no canonical representation, serialization
format, ordering rule, duplicate semantics, empty/`None` semantics, migration
strategy, replay behaviour, versioning mechanism, hash domain, or compatibility
mechanism. All of those remain OPEN.

---

## 2. What this package prepares

| Decision | Question | This package |
|---|---|---|
| **D-2** | Integrity Domain Contract — what exactly is protected | Decision space, per-field matrix, contract template with OPEN cells, question set |
| **D-5** | Existing v1 log compatibility / migration strategy | Evidence baseline, strategy classes A–E, comparison matrix, security consequences |

**Not prepared here, not decided here:** D-3, D-4, D-6, D-7. They are referenced
only where a dependency edge exists (see `05_D2_D5_DEPENDENCY_GRAPH.md`).

---

## 3. Package contents

| File | Purpose |
|---|---|
| `00_SCOPE_AND_DECISION_CONTEXT.md` | This file — scope, inputs, conventions |
| `01_D2_INTEGRITY_DOMAIN_CONTRACT.md` | Per-field analysis, derivation boundary, contract template, D2-Q questions |
| `02_D5_V1_COMPATIBILITY_ANALYSIS.md` | Current serialization/verification baseline, historical-data analysis |
| `03_D5_STRATEGY_MATRIX.md` | Strategy classes D-5-A … D-5-E and comparison matrix |
| `04_D2_D5_SECURITY_CONSEQUENCES.md` | Downgrade, discriminator integrity, legacy ambiguity, replay, audit continuity |
| `05_D2_D5_DEPENDENCY_GRAPH.md` | Decision dependency edges, incl. D-5 ↔ D-7 classification |
| `06_D2_D5_EVIDENCE_REQUIREMENTS.md` | Evidence gaps and what would close each |
| `07_D2_D5_DECISION_BRIEF.md` | The brief for the Authority + Two-Key Gate block |

---

## 4. Evidence classification convention

Every claim in this package carries exactly one tag.

| Tag | Meaning |
|---|---|
| **CONFIRMED** | Verified at a cited `file:line` in the pinned commit, or by an executed command |
| **IMPLEMENTATION-DERIVED** | An observation about how the code currently behaves. Describes the system; establishes no requirement and confers no authority |
| **EVIDENCE GAP** | Not determinable from the sources of truth; requires human input or a later decision |
| **NORMATIVE CONFLICT** | Two authoritative sources disagree; flagged, not reconciled |
| **NON-NORMATIVE CANDIDATE** | A possible design shown to make the decision space concrete. Selects nothing |

### 4.1 Prohibition on semantic drift

The permitted chain is:

```
implementation behaviour → evidence → NON-NORMATIVE CANDIDATE
    → human decision → formal artifact → implementation
```

This package produces **only** the evidence and candidate layers. Nothing here
advances to "recommendation" or "rule". In particular, the current nine-field
digest is described as *what the code does*, never as the correct or intended
formula, and the absence of `violations` from it is described as an **observed
architectural property**, never as a normative bug. That the code behaves a
certain way is not evidence that it ought to.

---

## 5. Sources of truth

1. **D-1 = YES**, as stated above (accepted input).
2. `review/2026-08-11_ENGINEERING_BASELINE/GUARD-G1_INTEGRITY_DESIGN_BRIEF.md`
3. `review/2026-08-11_ENGINEERING_BASELINE/GUARD_P0_6_D1_DECISION_BRIEF.md`
4. `docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` (DRAFT / NON-NORMATIVE)
5. `aura-guard-v1.3` source at `443f72e` — read from a pristine read-only clone
6. Prior review packages: `06_GUARD_AUDIT.md` §5 G-1, `08_BLOCKERS.md` P0-6

**Not re-opened:** the full Guard repository audit, RD-1, the ARI governance
track, and D-1 itself.

### 5.1 Evidence refinement affecting a prior document

**CONFIRMED.** `docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` §2.8 states that the
RFC 3161 exposure is "structural and latent", on the basis that
`tsa_message_imprint()` has no in-tree caller and `tst_path` is `None` at both
construction sites. The first half remains accurate; the conclusion is narrower
than the evidence supports.

**CONFIRMED — refinement.** The repository contains **real RFC 3161 tokens** as
committed fixtures: `tests/fixtures/tsa/segment-001.tsr` and `segment-002.tsr`,
round-tripped against FreeTSA per `tests/tst_verify.rs:3–9`, with trust anchors
at `tests/fixtures/tsa/freetsa-cacert.pem`. `tests/tst_verify.rs:25–33`
reconstructs the imprint inline — `SegmentManifest::segment_chain_preimage(...)`
then `Sha256::digest` — i.e. the identical preimage `tsa_message_imprint()`
computes, and `src/tst_verify.rs:393` (`verify_tsr`) verifies the tokens against
it. The fixture manifest `segment-001.manifest.json` carries a concrete
`merkle_root` and `head_chain_hash_at_close`, both derived from v1 `chain_hash`
values, sealed `2026-05-20T20:22:47`.

**IMPLEMENTATION-DERIVED consequence.** Timestamp evidence over v1-rule chain
hashes is therefore *already materialised in-repo*, not merely possible. This
matters to D-5 (audit continuity) and is carried into
`02_D5_V1_COMPATIBILITY_ANALYSIS.md` §6 and `04_D2_D5_SECURITY_CONSEQUENCES.md`
§E. The ADR is **not** amended by this package — amending it is a separate
decision for the Authority.

---

## 6. Hard boundaries observed

No production code modified. No change to `aura-guard-v1.3`, `chain.rs`,
`models.rs`, `segment.rs`, replay verification, `core/evaluator.py`, or SPEC-002.
No fixtures created or modified. No logs read, modified or migrated. No
migration or compatibility code. No canonical serialization, byte
representation, ordering rule, duplicate rule, `None`/empty rule, versioning
mechanism or migration strategy selected. No ADR establishing a semantic
decision. No PR.

The only output is documentation in this directory.
