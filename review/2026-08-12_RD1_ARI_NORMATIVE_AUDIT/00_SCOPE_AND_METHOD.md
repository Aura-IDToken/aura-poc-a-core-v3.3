# RD-1 — 00 SCOPE AND METHOD

**Date:** 2026-08-12
**Audit:** Does AURA currently contain an authoritative normative definition of ARI?
**Status:** EVIDENCE ONLY — no semantic selection, no production change
**normative_effect:** NONE

> **Filename note.** The task specified `01_AR I_DEFINITION_EVIDENCE.md`, which contains a
> space inside the identifier. This package uses `01_ARI_DEFINITION_EVIDENCE.md`. No other
> deviation from the requested file set.

---

## 1. Question

Determine, **from the existing repository corpus only**, whether an authoritative *normative*
definition of ARI exists.

This audit does **not** ask what ARI currently computes. That is already recorded
(RD-006 observation harness, CHECK 10). It asks whether any artifact carrying normative
authority *defines* it.

## 2. Method

1. Enumerate every ARI-bearing artifact in both repositories.
2. For each candidate, record document, section, version/status, exact quoted wording,
   authority level, and coverage across thirteen definitional dimensions (§4).
3. Build the provenance chain and mark every missing edge.
4. Record conflicts and circularities.
5. Issue a single verdict.

## 3. Corpus examined

| Corpus | Identity | Files | Notes |
|---|---|---|---|
| Implementation | `AuraIDToken/aura-poc-a-core-v3.3` @ `bdaa331` | full tree | working repository |
| **Specification** | `AuraIDToken/aura-specification` @ `62d2d6b` | 95 tracked | APS-000…950, CONF-001…010, SPEC-002, invariants, traceability, glossary, RI-PY |
| Specification (stub) | `aura-nomos/aura-specification` @ `eb2a4ec` | **2** (`README.md`, `.github/CODEOWNERS`) | **empty stub — no ARI, no APS** |
| Guard | `AuraIDToken/aura-guard-v1.3` | **not examined** | out of scope; see §6 |

### 3.1 Correction to an earlier statement in this session

An earlier turn stated that the specification corpus contained no ARI material, based on
`aura-nomos/aura-specification` — the repository present in this session's workspace, which is
a **2-file stub**. The substantive specification corpus lives at
**`AuraIDToken/aura-specification`**, a different repository under a different owner, attached
during this audit. All specification findings in this package derive from the substantive
corpus. The earlier observation was wrong about *which* repository, and is superseded here.

## 4. Definitional dimensions

Each candidate is scored on whether it defines:

`D1` formula · `D2` input domain · `D3` dimensionality · `D4` bounds ·
`D5` integer arithmetic semantics · `D6` division semantics · `D7` rounding semantics ·
`D8` malformed-input behaviour · `D9` drift · `D10` penalty behaviour ·
`D11` serialization/hash implications

Plus, per candidate: authority level, and whether **normative** or **implementation-derived**.

## 5. Evidential rules applied

Carried directly from the task and applied without exception:

- **R1** — That `core/evaluator.py` produces a value is **not** evidence that the value is
  normative.
- **R2** — That RI-PY describes a value does **not** make it normative unless the governing
  corpus grants RI-PY that authority. This audit tested that grant explicitly (§05, C-1).
- **R3** — `FROZEN` is **not** a synonym for `normative`. `FROZEN` constrains change; it does
  not confer definitional authority. Where a document is marked FROZEN, that is recorded as
  status, not as authority.
- **R4** — Binary artifacts that cannot be text-extracted yield **UNKNOWN**, never a
  definition.

## 6. Out of scope

No formula, rounding mode, division mode, dimension, or bound is selected or recommended. No
fixture is created; no existing fixture is modified. No production code, SPEC-002, ADR, or
specification document is modified. `aura-guard-v1.3` was not examined: no evidence in either
examined corpus indicates Guard consumes ARI.

## 7. Authority ladder used

From `CLAUDE.md` (highest → lowest), abbreviated to the levels that arise here:

| Level | Tier |
|---|---|
| 1 | Aura Constitutional Decree / Constitutional Authority |
| 2 | Aura Protocol Specification (APS / SPEC) |
| 3 | Protocol Invariants |
| 5 | Conformance Test Matrix / approved Conformance Requirements |
| — | *(implementation-repository documentation — no assigned level; see §05 C-4)* |
| 9 | Existing implementation |
| 10 | Agent assumptions |

Levels 1–5 are the only tiers capable of carrying a normative definition. This distinction
does the decisive work in `02_AUTHORITY_MATRIX.md`.
