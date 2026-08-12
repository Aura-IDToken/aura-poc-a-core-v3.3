# 06 — AURA-GUARD G1 REMEDIATION PLAN

**Date:** 2026-08-12
**Subject:** `AuraIDToken/aura-guard-v1.3` @ `443f72e58483c3ea6112ea517647cc0dbf459960`
**Mode:** READ-ONLY. **No Guard source, test, fixture, workflow or document was modified.**
**Normative effect:** NONE.
**Builds on:** `GUARD-G1_INTEGRITY_DESIGN_BRIEF.md`, `GUARD-G1_DECISION_PACKAGE.md`,
`GUARD-G1_CHARACTERIZATION_TESTS.rs`

---

## §1 Verification Status of This Plan

The design brief was written in a prior session. **Every structural fact it asserts was
re-verified at source this session**, against the same pinned commit — not carried forward
on trust.

| Fact | Re-verified | Source |
|---|---|---|
| Chain digest takes exactly **nine** arguments, joined by `SEP = "\|"` | **YES** | `src/chain.rs:25-49` |
| `violations` is **not** among them; `compute_chain_hash` has no access to the field | **YES** | `src/chain.rs:25-49` |
| `recompute_for_entry` reads the same nine fields | **YES** | `src/chain.rs:51-65` |
| `Violation` is `{rule: String, action: String, confidence: f32, validator: Option<String>}` | **YES** | `src/models.rs:31-42` |
| `violations: Vec<Violation>` is field 12 of `AuditEntry` | **YES** | `src/models.rs:90` |
| Merkle leaf is built from `chain_hash` **alone** | **YES** | `src/segment.rs:140-148` |
| `segment_chain_preimage` joins five values, none from `violations` | **YES** | `src/segment.rs:91-106` |
| `AuditEntry` doc claims the on-disk log is **1:1 replayable** with the HTTP response | **YES** | `src/models.rs:44-48` |

**One point sharpened by re-verification.** `src/models.rs:44-48` documents the entry as
guaranteeing *"1:1 replayability between the response and the log"*. That guarantee holds
for **shape**, not for **integrity**: the field is present in both and bound by neither.

---

## §2 The Custody Chain — Where the Binding Must Be Introduced

```
                    engine::evaluate()  ──►  (String, Vec<Violation>)
                                                    │
   ┌────────────────────────────────────────────────┴──────────────┐
   │                                                                │
   ▼                                                                ▼
AuditEntry.violations                                    returned to HTTP caller
   │  [models.rs:90]                                      [api/audit.rs:44]
   │
   │  ✗✗✗  NO PATH FROM HERE INTO ANY DIGEST  ✗✗✗
   │
   └──►  serde_json::to_string  ──►  logs/audit.jsonl
              [log_writer.rs:96]        (no canonicalization,
                                         no field-order normalization)

═══════════════ THE INTEGRITY CHAIN, WHICH violations NEVER ENTERS ═══════════════

  9 fields ──► chain_hash = SHA-256(join("|"))            [chain.rs:36-47]
                    │
                    ├──► prev_hash of entry N+1           [chain.rs:89]
                    │
                    └──► hex::decode ──► leaf_hash(0x00 ‖ raw)   [segment.rs:141-147]
                                │
                                └──► merkle_root          [segment.rs:151-157]
                                          │
                                          └──► segment_chain_preimage
                                                    │      [segment.rs:91-106]
                                                    ├──► segment_chain_hash
                                                    └──► tsa_message_imprint
                                                              │
                                                              └──► RFC 3161 anchor
```

### §2.1 The Answer to the Task's Question

> *"Identify exactly where `violations` must become integrity-bound."*

**At `compute_chain_hash` — `src/chain.rs:36-47` — or nowhere.**

The reasoning is structural, not preferential:

1. All four downstream mechanisms (entry chain, Merkle root, segment chain, TSA imprint)
   derive **transitively** from `chain_hash`.
2. `entry_leaf_hash` (`segment.rs:141`) consumes **only** `entry.chain_hash`.
3. `segment_chain_preimage` (`segment.rs:91-106`) consumes **only** the Merkle root and
   sequence metadata.
4. Therefore **any binding introduced downstream of `chain_hash` leaves the entry chain
   itself unprotected**, and a fifth parallel mechanism does not close the gap — it adds a
   second thing a verifier may skip.

**This is a location, not a design.** *That* the binding must sit at or above `chain_hash`
to be transitive follows from the code. *Whether* to bind at all (D1), *what bytes* to bind
(D3), and *in which hash domain* (D5) are **ARCHITECTURAL DECISION REQUIRED** and are not
answered here.

**Exception, stated for completeness:** boundary B5 (no cryptographic binding; compensating
controls only) makes the question moot. B5 remains admissible under D1.

---

## §3 Consequence Analysis

### §3.1 Merkle consequence

Leaves are `leaf_hash(hex::decode(chain_hash))` — RFC 6962 `SHA-256(0x00 ‖ data)`.
Violation content contributes **zero bits** to any leaf. The root is therefore invariant
under every mutation of `violations`.

### §3.2 Segment consequence

`segment_chain_preimage` joins `prev_segment_chain_hash`, `merkle_root`, `first_seq`,
`last_seq`, `sealed_at`. **Four of five are sequence metadata; the fifth is the Merkle
root**, which §3.1 shows is invariant. Segment manifests continue to verify after any
violation mutation.

The sealer **does** enforce a schema discriminator here (`sealer.rs:100` rejects manifests
whose `SEGMENT_SCHEMA` differs). **No equivalent check exists on the audit-entry path** —
`read_all_entries()` deserializes without inspecting `schema`, and `verify_chain()` never
reads it. The precedent for D6 exists in the codebase but is not applied where it would be
needed.

### §3.3 TSA consequence — the most serious

`tsa_message_imprint` hashes the segment preimage. Therefore:

> **An RFC 3161 token obtained before a violation mutation continues to validate after
> it.** The trusted timestamp attests to a Merkle root that never covered the mutated data.

This converts a third-party trust anchor into an attestation of something narrower than a
reader would reasonably infer. **This is the single strongest argument for treating D1 as
urgent** — and it is recorded as a consequence, not as a claim of regulatory
non-conformance. No regulatory requirement was read for this plan.

### §3.4 Documentation consequence

Four shipped claims are broader than the implementation:

| Source | Claim | True for the 9 covered fields | True for `violations` |
|---|---|:--:|:--:|
| `README.md:24` | "any byte-level mutation is detected by `aura-replay` (exit code `2`)" | yes | **no** |
| `README.md:265` | "`aura-replay` will detect any byte-level mutation" | yes | **no** |
| `README.md:97` | threat-model row: operator edit → `CHAIN BREAK` | yes | **no** |
| `docs/REPLAY_DEMO.md:50` | "**any** mutation — even a one-letter flip — breaks the cryptographic chain" | yes | **no** |

**Correcting these is a documentation change and requires none of D1–D8.** It is available
today and is listed in `10` as EXECUTABLE NOW.

---

## §4 Reproduction

Already executed and committed: `GUARD-G1_CHARACTERIZATION_TESTS.rs` (386 lines, 8/8
passing).

| Mutation applied to the persisted record | Chain verifies? | Merkle leaf changed? |
|---|:--:|:--:|
| `violations` emptied to `[]` | **TRUE** | no |
| `rule`/`action`/`confidence` rewritten | **TRUE** | no |
| fabricated violation appended | **TRUE** | no |
| **CONTROL:** `decision` `DENY` → `ALLOW` | **FALSE — breaks** | yes |

The control establishes fidelity: a covered field does break the chain, exactly as
documented. `aura-replay` reports `CHAIN OK`, exit code `0`, for all three uncovered
mutations.

**Bound on exposure.** The nine covered fields cannot be altered — `decision`,
`policy_hash`, `input_hash`, `shadow_hash`, `context`, `seq`, `timestamp` and ordering are
all protected. A tampered record can therefore be made **internally inconsistent** (e.g.
`decision: "DENY"` with `violations: []`), and that inconsistency is detectable by a reader
who reasons about it. **It is not detected by any automated verification the product
ships.**

**This is a pre-existing property, not a regression.** The field has been outside the digest
since the digest was defined.

---

## §5 Decisions D1–D8 — Open

Reproduced from the design brief §12. **This plan answers none of them.**

| ID | Decision | Status |
|---|---|---|
| **D1** | Accept, mitigate procedurally, or address cryptographically? | **OPEN** — selects among B1–B5 |
| **D2** | Is retroactive verifiability of existing logs required? | **OPEN** — determines whether B1/B2 are admissible at all |
| **D3** | **What byte reduction of violation data is authoritative?** Field set, field order, `Option::None` encoding, empty-vector encoding, separator/escaping rules such that no two distinct violation lists collide | **OPEN — ARCHITECTURAL DECISION REQUIRED. Explicitly not answered.** |
| **D4** | Does `confidence` (`f32`) participate, and in what representation? | **OPEN** — coupled to D3 |
| **D5** | **Which hash domain?** Existing entry digest, or a distinct domain with its own prefix | **OPEN — ARCHITECTURAL DECISION REQUIRED. Explicitly not answered.** |
| **D6** | Migration mechanism and schema-discriminator policy for `"aura-guard.audit.v1"` | **OPEN** |
| **D7** | Disposition of RFC 3161 tokens already obtained | **OPEN** |
| **D8** | Does the `/v1/audit` response shape change; integrator notification path | **OPEN** |

### §5.1 Candidate boundaries — restated, none selected

| # | Boundary | Digest regimes affected | Historical logs |
|---|---|---|---|
| B1 | Inside the existing entry digest | all four, transitively | invalidated under the new rule |
| B2 | Separate per-entry digest, itself an input to the entry digest | all four, transitively | invalidated under the new rule |
| B3 | Separate per-entry digest, verified independently | none | remain valid; field absent on old entries |
| B4 | Parallel Merkle tree anchored in the segment manifest | segment + TSA if included | entry chain valid; manifests change |
| B5 | No cryptographic binding; compensating controls only | none | unaffected |

**Property that the design must supply and that is not automatic:** under B3 and B4, an
entry with the new field **stripped entirely** must be distinguishable from a legitimately
old entry lacking it — otherwise the control is bypassable by deletion.

### §5.2 The `f32` coupling — why D4 cannot be deferred

`Violation.confidence: f32` (`models.rs:38`) is the only floating-point value in the
persisted record. It is **currently inert**: outside every digest, it cannot cause a hash
divergence.

**It stops being inert the moment any of B1–B4 is adopted.** Live concerns at that instant:

1. **Text formatting** — `serde_json` uses shortest-round-trip (ryu). Stable for a given
   Rust toolchain; "stable in practice" is not "specified", and an independent verifier in
   another language must reproduce the same characters.
2. **Provenance** — the value originates in policy YAML (`policy.rs`, `pub score: f32`)
   parsed by `serde_yaml`. A literal such as `0.7` is **not exactly representable in
   binary32**.
3. **Width** — a verifier parsing the same YAML into `f64` obtains a different value and
   therefore a different digest.
4. **Special values** — nothing prevents `NaN` or infinity reaching the field, and **JSON
   can represent neither**.

> **Planning consequence.** D1 and D4 must be decided **together**. Adopting a binding
> without settling the float representation would create a cross-implementation determinism
> surface **where none exists today** — trading a detection gap for a reproducibility gap.

---

## §6 Migration Implications

Any change to the digest input changes every subsequent `chain_hash`.

| Implication | Detail |
|---|---|
| Two regimes in one log | Entries before and after cannot be verified by one rule |
| Anchored artefacts | Merkle roots, segment chain hashes, and RFC 3161 tokens obtained before the change remain valid **only** under the old rule |
| `prev_hash` linkage | Unaffected in *form* (still 64-char hex); the two sides are computed under different definitions |
| Verifier complexity | A verifier must know which rule applies to which entry — the mechanism is D6 |
| API surface | D8: whether `/v1/audit`'s response shape changes for existing integrators |

**Available precedent, currently unused on this path:** `SEGMENT_SCHEMA` equality check at
`sealer.rs:100`. The audit-entry `schema` field exists (`"aura-guard.audit.v1"`, a literal
at the construction site, `api/audit.rs:132`) but is **never inspected** by any verifier.

---

## §7 Test Specification

**Specified, not written.** No test file was created or modified by this plan.

### §7.1 Available now — characterization only, no decision required

Permitted under `SAFE_ENGINEERING_WORK.md` §1.1. These record present state and assert
nothing about correctness. They would not need to change if a design is later chosen —
**they would simply start failing, which is the point.**

| ID | Test | Records |
|---|---|---|
| **T-0a** | Persist an entry with non-empty `violations`, mutate the field in the JSONL, run `verify_chain()` | that it returns `Ok` |
| **T-0b** | Same, then `verify_manifest_against_entries()` | that the manifest still verifies |
| **T-0c** | Assert the exact nine-field preimage of `compute_chain_hash()` against a known-answer vector | **pins the current digest input so any future change is visible** |

**T-0c is the highest-value item in this section.** It converts the current digest
definition from an implicit property of the code into an executable, reviewable fact.

**Context that makes T-0a…T-0c first-of-their-kind:** every existing integrity fixture uses
`violations: vec![]` — `chain.rs:112`, `segment.rs:432`, `sealer.rs:407` — and
`tests/golden.rs:21` discards the field entirely (`let (decision, _) = evaluate(...)`).
**No test in the repository exercises a non-empty violations vector through the chain or
segment path at all.**

### §7.2 Required after D1–D7 — the cases the task enumerates

| ID | Case | Asserts | Applies to |
|---|---|---|---|
| **TG-1** | **empty violations** | digest is well-defined and distinguishable from *absent* | B1–B4 |
| **TG-2** | **one violation** | digest covers it; mutation breaks verification | B1–B4 |
| **TG-3** | **multiple violations** | all covered | B1–B4 |
| **TG-4** | **reordered violations** | reordering is detected **or** explicitly defined as insignificant — **D3 must state which** | B1–B4 |
| **TG-5** | **mutated violation** | each of `rule`, `action`, `confidence`, `validator` individually breaks verification | B1–B4 |
| **TG-6** | **fabricated violation** | insertion breaks verification | B1–B4 |
| **TG-7** | **CONTROL: mutated `decision`** | still breaks — proving the new binding did not *replace* existing coverage | all, incl. B5 |

**TG-4 is the case that most exposes D3.** Whether `[A, B]` and `[B, A]` are the same
compliance finding is a semantic question the byte reduction silently answers. It must be
answered deliberately.

**TG-7 is a regression control, not a feature test.** It must be included even under B5,
where nothing else changes.

### §7.3 Additional required coverage

| ID | Test |
|---|---|
| T-1 | Each §4 mutation now fails verification with the specified exit code |
| T-2 | Round-trip: serialize → deserialize → recompute → digest unchanged |
| T-3 | Known-answer vectors for the chosen reduction, checked in as fixtures |
| T-4 | **Injectivity**: no two distinct violation lists reduce to the same bytes — including empty-vs-absent, `None`-vs-empty-string `validator`, and separator-collision cases |
| T-5 | `f32` boundaries: `0.0`, `1.0`, a value not exactly representable in binary32, and whatever D4 specifies for `NaN`/infinity |
| T-6 | Cross-toolchain reproduction — at minimum the **arm64 leg that Guard's CI lacks entirely** (`ci.yml` is `ubuntu-latest` only) |
| T-7 | Migration: a log spanning the change point verifies per D6; an old-format entry is either accepted or rejected — **never silently mis-verified** |
| T-8 | Fail-closed on omission: an entry with the new field stripped is **rejected, not treated as legacy** |
| T-9 | Segment/TSA regression across the change |
| T-10 | Property test over arbitrary violation vectors, matching the five existing `proptest!` suites |
| T-11 | Golden fixtures updated to carry non-empty violations |

**T-4 is the correctness core.** A byte reduction that is not injective is not an integrity
control — it is a hash of something other than what it claims to cover.

---

## §8 Execution Sequence

| Step | Work | Gate | Available |
|---|---|---|---|
| **G1-0** | Correct the four overbroad "any" documentation claims (§3.4) | **none** | **NOW** |
| **G1-1** | Write T-0a, T-0b, T-0c | **none** — characterization | **NOW** |
| **G1-2** | Correct the stale formula comment at `src/models.rs:95` (omits `policy_hash` and `context`, which the implementation includes) | **none** — documentation | **NOW** |
| **G1-3** | Add arm64 to Guard CI | **none** | **NOW** |
| **G1-4** | Decide **D1 + D2** | **product decision** | blocked |
| **G1-5** | Decide **D3 + D4 + D5** jointly | after G1-4 | blocked |
| **G1-6** | Decide **D6 + D7 + D8** | after G1-5 | blocked |
| **G1-7** | Implement the chosen boundary | after G1-6 | blocked |
| **G1-8** | TG-1…TG-7, T-1…T-11 | after G1-7 | blocked |

**Steps G1-0 through G1-3 are unblocked today**, require no decision, and change no digest.

---

## §9 The Governance Position — Stated Precisely

**RM-08 is not gated by Aura protocol governance.**

| Gate | Applies? | Evidence |
|---|:--:|---|
| DR-002 | **NO** | Guard contains zero occurrences of `constitution`, `ari`, `poca` |
| SPEC-002 / AD-CA-xxx | **NO** | as above; Guard implements no Constitution-derived object |
| NB-021 (FROZEN) | **NO** | Guard contains zero occurrences of `frozen` / `freeze` |
| CR-007 | **NO** | not referenced |
| **Product decision on the audit-log format** | **YES** | this is the only gate |

> **This is the largest genuinely unblocked decision surface in the ecosystem.**
> D1 and D2 can be taken today by a product owner, with no dependency on the Protocol
> Custodian, on DR-002, on NB-021, or on any specification advancing beyond DRAFT.

---

## §10 Explicit Non-Goals

This plan does **not** select a serialization format, a byte reduction, a canonical
representation, a hash domain, a domain-separation prefix, a schema version, or a migration
path. It does not choose among B1–B5 or recommend one. It does not modify any file in
`aura-guard-v1.3`. It does not create a pull request. It does not assert that the current
state violates any regulatory or protocol requirement — no such requirement was read. It
does not authorize any of the work in §7.

---

*This document has no normative effect. It records where the binding would have to sit,
what it would cost, and what must be decided first. It selects nothing.*
