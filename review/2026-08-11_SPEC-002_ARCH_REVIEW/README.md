# SPEC-002 Architecture & Conformance Review — 2026-08-11

**Status: DRAFT — ANALYSIS ARTIFACTS, NO NORMATIVE EFFECT**

No document in this package approves, accepts, freezes, registers, or supersedes anything.
No AD-CA decision domain is resolved here. Per GOV-001 §9 and AURA Constitution Article VIII,
the AI author of this package may not approve or freeze canonical documents and has not
attempted to.

---

## Read in this order

| # | Document | What it settles |
|---|---|---|
| 00 | [`00_REVIEW_SCOPE_AND_EVIDENCE_BASE.md`](00_REVIEW_SCOPE_AND_EVIDENCE_BASE.md) | What was actually inspected; which asserted inputs do not exist; artifact classification |
| 01 | [`01_ADR_REVIEW.md`](01_ADR_REVIEW.md) | The 14 review criteria applied to each decision domain; 17 numbered conflicts |
| 02 | [`02_TRACEABILITY_MATRIX.md`](02_TRACEABILITY_MATRIX.md) | AD-CA → ADR → REQ → INV → impl → test → evidence, with every gap marked |
| 03 | [`03_SPEC-002_v0.4_DRAFT.md`](03_SPEC-002_v0.4_DRAFT.md) | Proposed delta: 10 new contract-surface requirements, no decisions |
| 04 | [`04_EVIDENCE_PLAN.md`](04_EVIDENCE_PLAN.md) | E1–E12 with requirement, decision, invariant, test, expected result, artifact |
| 05 | [`05_MERGE_BLOCKERS.md`](05_MERGE_BLOCKERS.md) | 11 P0 · 8 P1 · 6 P2 |
| 06 | [`06_OPEN_DECISIONS.md`](06_OPEN_DECISIONS.md) | 16 open decisions in OD-xxx format |
| 07 | [`07_IMPLEMENTATION_CONFORMANCE.md`](07_IMPLEMENTATION_CONFORMANCE.md) | RI-PY and RI-RS against the future contract |

---

## The three findings that matter most

**1. ADR-002 … ADR-006 do not exist.** Not on `main`, not on any of the 22 remote branches,
not as drafts. The review therefore applies its criteria to the *decision domains* those ADRs
would carry, anchored to SPEC-002 v0.3 §6 — rather than fabricating five documents and
reviewing the fabrication.

**2. Two cross-language divergences are already present in the reference implementation, and
were reproduced during this review.**
- `core/evaluator.py` uses Python's `//` (floors toward −∞) where Rust/C/JS truncate toward
  zero: `dot = -7000029999` yields **−70001** vs **−70000**.
- `core/offline_normalizer.py` uses Python's `round()` (half-to-even) where C/Rust are
  half-away-from-zero and JS is half-up: `0.5 → 0` vs `1`; `2.5 → 2` vs `3`. This is the
  **Constitution Vector construction path**, and SPEC-002 §6 lists `round-half-to-even` as an
  **unapproved candidate**.

Both are latent rather than live — the placeholder embedding emits only non-negative values,
and existing CI runs Python on both sides of its x86/ARM comparison, so nothing detects them
today. Both become permanent if the instrument is frozen in this state.

**3. There is no second implementation, so the success criterion is unfalsifiable.**
`aura-poc-a-core-v3.3` has a self-declared *placeholder* embedding and **no code path that
reads `AURA_CONSTITUTION.md`**. `aura-guard-v1.3` has no constitution, vector, or ARI code at
all. The stage's criterion — two independent engineers obtaining identical bytes — has no
second party, so it cannot be tested, passed, or failed.

---

## Definition of success (unchanged, and currently unmet)

> "Two independent engineers can implement the Constitution Artifact and verify it without
> inspecting the reference implementation and obtain identical canonical bytes, vector bytes,
> identities and verification results."

**SPEC-002 remains NOT READY.** Gate status: **CLOSED**.

---

## Immediate next actions (all require human authority)

1. Resolve **OD-001** (which repository is authoritative) — blocks everything downstream.
2. Resolve **OD-003** (which document model is in force) — determines whether SPEC-002 has a
   defined place in the canonical hierarchy at all.
3. Resolve **BLOCKER-P0-003** (the triple `ADR-001` collision) — until then "next sequential
   ADR-NNN" is undefined and ADR-002 cannot be safely numbered.
4. Assign **AD-CA-004** and **AD-CA-006** to owning artifacts (**OD-016**) — without this,
   ADR-004 cannot close its own stated scope.
5. Correct **APS-200 §4** so a deterministic artifact is not obliged to carry a wall-clock
   timestamp inside its integrity hash (**OD-008**).
6. Commission an independent implementation — longest lead time of anything in this review,
   and it should start first even though it closes last.

---

*Prepared by Claude in the architectural & conformance audit role defined by `CLAUDE.md`.
Every conflict is cited to a file and section that exists in the repositories as of
2026-08-11. Where an identifier does not exist, the text reads "identifier not yet assigned"
rather than inventing one.*
