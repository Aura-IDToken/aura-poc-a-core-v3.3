# ADR-P0-6: Guard Violations Integrity

**Status:** DRAFT — NON-NORMATIVE — REQUIRES HUMAN APPROVAL
**Scope:** `aura-guard-v1.3` only
**Date:** 2026-08-12
**Author:** Claude (conformance audit role, per `CLAUDE.md`)
**Authority:** Pending Chief Architect / Protocol Custodian approval
**Finding status:** CONFIRMED — verified against source **and** by executable proof (§2.7)
**Evidence basis:** `AuraIDToken/aura-guard-v1.3` @ commit
`443f72e58483c3ea6112ea517647cc0dbf459960`
**Independent re-verification:** 2026-08-12 — all file/line references, the §2.7
test-count arithmetic, the §2.8 blast radius and the §2.9 compatibility surface
re-checked against a fresh read-only clone pinned at that commit.

---

## 0. Scope and repository boundary (READ FIRST)

This ADR analyses **`aura-guard-v1.3`**, which is a **separate repository**. It
contains no Rust code and no `aura-guard` sources; nothing in this ADR
describes or constrains `aura-poc-a-core-v3.3`.

This document is filed here as the **audit record** only. Any implementation
resulting from it belongs in `aura-guard-v1.3`, and **no implementation has
been produced** in either repository.

The evidence below was verified by cloning `aura-guard-v1.3` at commit
`443f72e` and reading and executing that source directly. It is not inferred
from this repository.

**This ADR does not:** select a serialization format, choose a hash domain,
define a migration, change the log format, resolve any of D-1…D-7, create test
fixtures, or authorize implementation work.

### 0.1 Labelling convention

Every statement in this document carries one of five labels. The distinction is
load-bearing: only **FACT** is verified, and only **OPEN DECISION** binds anyone.

| Label | Meaning |
|---|---|
| **FACT** | Verifiable at a cited `file:line` in the pinned commit, or produced by an executed command |
| **OBSERVATION** | A consequence derived from FACTs; carries no normative weight |
| **ALTERNATIVE** | One of several defensible designs; listed, never selected |
| **RECOMMENDATION (NON-NORMATIVE)** | The auditor's advisory opinion. **Advisory only. Not a decision. Not approved.** |
| **OPEN DECISION** | A question reserved to the human authority; unresolved in this document |

---

## 1. Context

P0-1 is closed and verified (see `docs/evidence/P0-1_EVIDENCE.md`) and is not
reopened here. This ADR addresses P0-6:

> Aura-Guard audit violations must have verifiable integrity.

The Guard claims tamper-evident audit logging via a SHA-256 hash chain. The
question is whether `violations` — the list of rule matches that substantively
explain *why* a decision was made — are integrity-protected by that chain.

---

## 2. Evidence Summary

All file/line references below were confirmed at commit `443f72e`.

### 2.1 Data Model

**FACT.** `src/models.rs` — `Violation` at line 32, `AuditEntry` at line 50.

```rust
pub struct Violation {
    pub rule: String,
    pub action: String,
    pub confidence: f32,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub validator: Option<String>,
}
```

- **FACT.** `AuditEntry` holds `violations: Vec<Violation>` (`models.rs:90`)
  alongside `chain_hash` (`models.rs:96`).
- **FACT.** Both structs derive `Serialize`/`Deserialize` (`models.rs:31`, `:49`).
- **FACT.** `validator` carries `skip_serializing_if = "Option::is_none"`
  (`models.rs:40`), so it is **omitted entirely** when `None` — directly
  relevant to any canonicalization design (D-3, D-4).
- **FACT.** `confidence` is the only floating-point value in the persisted
  record (`models.rs:38`).

### 2.2 Chain Hash Construction

**FACT.** `src/chain.rs` — `compute_chain_hash` at lines 25–49.

```rust
let canonical = [
    prev_hash, decision, policy_set, policy_hash,
    context, input_hash, shadow_hash,
    &seq.to_string(), timestamp,
]
.join(SEP);   // SEP = "|"  (chain.rs:20)
sha256_hex(&canonical)
```

**FACT.** `violations` is **NOT** an input to `compute_chain_hash`. The function
does not accept an `AuditEntry` and has no access to the field.

Covered (9): `prev_hash`, `decision`, `policy_set`, `policy_hash`, `context`,
`input_hash`, `shadow_hash`, `seq`, `timestamp`.

Not covered (4, excluding the self-referential `chain_hash`): `violations`,
`audit_id`, `request_id`, `schema`.

**FACT.** The module doc-comment at `chain.rs:11–12` states that "Tampering with
any field — *or with the order of records* — breaks the chain."

**OBSERVATION.** As written that is inaccurate: four fields are outside the
digest. The doc-comment overstates the guarantee.

**FACT.** The `AuditEntry::chain_hash` doc-comment (`models.rs:95`) is stale — it
omits `policy_hash` and `context`, both of which *are* hashed.

### 2.3 Violations Creation

**FACT.** `src/engine.rs` — `evaluate` at line 14.

```rust
pub fn evaluate(shadow: &str, context: &str, rules: &[CompiledRule]) -> (String, Vec<Violation>)
```

**FACT.** `violations` order equals declaration order of matching rules in the
policy YAML: `policy.rs:233–237` compiles rules with
`into_iter().map(compile_rule).collect()` (order-preserving), and `engine.rs:19`
iterates that slice sequentially, pushing at `engine.rs:50`.

**FACT.** `engine.rs:28` uses `rule.pattern.find(shadow)` (first match only), not
`find_iter`; the repository contains zero `find_iter` calls in `engine.rs`. One
rule therefore contributes at most one violation.

**FACT.** The decision aggregate is order-independent (`engine.rs:58–65`:
`DENY` if any deny-rule matched, else `REVIEW`, else `ALLOW`).

### 2.4 Log Persistence

**FACT.** `src/log_writer.rs` — `append` at line 88; `serde_json::to_string` at
line 96; single-line write at `:104`.

**FACT.** `chain_hash` is computed at `src/api/audit.rs:119`, *before* the
`AuditEntry` is constructed (`:131`) and before `append` is called (`:149`).

**OBSERVATION.** The entire entry — including `violations` — is persisted
verbatim, but the digest that protects it was computed without ever reading the
field. There is no canonicalization step and no on-disk schema normalization.

### 2.5 Replay Verification

**FACT.** `src/chain.rs` — `verify_chain` at line 71, `recompute_for_entry` at
line 53.

**FACT.** `recompute_for_entry` reads exactly the same nine fields; it does not
read `violations`. `verify_chain` performs exactly two checks per entry:
`prev_hash` linkage and digest equality.

**OBSERVATION.** Modifying the violations list after the entry is written does
not break chain verification.

### 2.6 Existing Chain Tests

**FACT.** `violations` appears exactly **once** in `src/chain.rs` — at line 112,
as `violations: vec![]` in a test fixture (`grep -c` = 1).

**FACT.** Every integrity fixture in the repository uses an empty vector:
`chain.rs:112`, `segment.rs:432`, `sealer.rs:407`. `tests/golden.rs:21` discards
the field (`let (decision, _) = evaluate(...)`). The string `violations` does not
occur anywhere under `tests/`.

**OBSERVATION.** No existing test covers non-empty violations, tamper detection
on violations, or violation ordering.

### 2.7 Executable proof of the gap

Code reading alone is not evidence (AGENTS.md rule 9). A temporary test was
added to `src/chain.rs` in a local clone and executed with
`cargo test --lib p06_evidence`. It builds an entry with two real violations,
verifies the clean chain, then applies five mutation classes:

| # | Mutation | `verify_chain` result | Detected? |
|---|---|---|---|
| 1 | **ADD** a fabricated violation (`R-999-FABRICATED`) | `Ok` | ❌ No |
| 2 | **REMOVE** a violation that did occur | `Ok` | ❌ No |
| 3 | **MODIFY** `confidence` 0.91→0.01 and `action` deny→allow | `Ok` | ❌ No |
| 4 | **REORDER** two violations | `Ok` | ❌ No |
| 5 | **WIPE** all violations (DENY with zero substantiation) | `Ok` | ❌ No |
| — | *Control:* tamper `decision` DENY→ALLOW | `Err(ChainBreak)` | ✅ Yes |

```
running 1 test
test chain::p06_evidence::p06_violations_are_outside_integrity_boundary ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 178 filtered out
```

The control case proves the harness detects tampering *inside* the boundary, so
the five `Ok` results are a real gap and not a broken test.

**Corroboration.** `cargo test --lib -- --list` at `443f72e` reports **178
tests**, which is exactly the "178 filtered out" above with one temporary test
added. **FACT.** The temporary test is not in the repository: `grep` for
`p06_evidence` / `p06_violations` across `src/` and `tests/` returns nothing.

**This test was NOT committed.** It was written solely to generate this
evidence. Landing it belongs to the implementation phase in `aura-guard-v1.3`.

### 2.8 Blast radius — transitive coverage, verified from source

Determined by reading each function, not assumed.

| Step | Function | Input it actually consumes | Cite |
|---|---|---|---|
| 1 | `compute_chain_hash` | 9 fields; **not** `violations` | `chain.rs:25–49` |
| 2 | `entry_leaf_hash` | `hex::decode(entry.chain_hash)` → `leaf_hash(raw)` — **the chain hash and nothing else** | `segment.rs:140–150` |
| 3 | `leaf_hash` | `SHA-256(0x00 ‖ data)`, RFC 6962 | `merkle.rs:29–34` |
| 4 | `segment_merkle_root` | `entry_leaf_hash` per entry → `merkle_root(&leaves)`; no other entry field | `segment.rs:151–158` |
| 5 | `segment_chain_preimage` | `prev_segment_chain_hash ‖ merkle_root ‖ first_seq ‖ last_seq ‖ sealed_at`, joined with `"\|"` | `segment.rs:91–106` |
| 6 | `recompute_segment_chain_hash` | `SHA-256(preimage)` from step 5 | `segment.rs:109–121` |
| 7 | `tsa_message_imprint` | `SHA-256(same preimage)` from step 5 | `segment.rs:123–131` |

```
violations ──✗ (never read)
                  chain_hash            [chain.rs:25-49]
                       │
                       ├─► entry_leaf_hash  [segment.rs:140-150]
                       │        └─► segment_merkle_root  [segment.rs:151-158]
                       │                 └─► segment_chain_preimage  [segment.rs:91-106]
                       │                          ├─► segment_chain_hash  [segment.rs:109-121]
                       │                          └─► tsa_message_imprint [segment.rs:123-131]
                       └─► prev_hash of entry N+1        [chain.rs:71-92]
```

**FACT — inheritance confirmed.** Each downstream mechanism consumes only the
output of the step above it. Because `violations` is absent at step 1, it is
absent from **the entry leaf hash, the Merkle root, the segment chain hash, and
the RFC 3161 message imprint**. The gap is at the root of the derivation, so no
downstream mechanism can compensate for it.

**FACT — precision on the TSA leg.** `tsa_message_imprint()` is defined but has
**no in-tree caller** (`grep`: one occurrence, its own definition), and
`tst_path` is `None` at both construction sites (`segment.rs:203`,
`sealer.rs:381`). The TSA exposure is therefore **structural and latent** at this
commit, not a statement that tokens have been issued. Any token obtained over
that imprint would inherit the gap.

**OBSERVATION.** This is impact, not a work item. It widens the consequence of
D-1 and D-2; it does not add a separate defect.

### 2.9 Existing v1 logs, replay, and schema handling

**FACT.** Audit entries carry `schema: "aura-guard.audit.v1"` as a string literal
at the construction site (`api/audit.rs:132`). There is no named constant for it;
the only other occurrence in `src/` is a test fixture (`chain.rs:101`).

**FACT.** `read_all_entries` (`log_writer.rs:151–170`) deserializes each JSONL
line into `AuditEntry` **without inspecting `schema`**. `verify_chain` does not
read it either (§2.5). No code path gates audit-entry verification on a version.

**FACT — a precedent exists, on the other path.** Segment manifests carry
`SEGMENT_SCHEMA = "aura-guard.segment.v1"` (`segment.rs:44`) and are rejected on
mismatch in two places: `sealer.rs:100` and `verify_segment_chain`
(`segment.rs:341–342`, `SegmentError::BadSchema`).

**FACT — what `aura-replay` verifies.** `src/bin/aura_replay.rs` calls
`verify_chain` unconditionally (`:113`), optional policy-lineage checks
(`:134–153`), `verify_segment_chain` (`:175`), and
`verify_manifest_against_entries` (`:194`), then prints `CHAIN OK` (`:213`).
None of these reads `violations`.

**FACT — why a digest change invalidates history.**
`verify_manifest_against_entries` (`segment.rs:382–405`) **recomputes** the Merkle
root from the entries (`:394`) and compares it to the stored `merkle_root`, and
compares the last entry's `chain_hash` to `head_chain_hash_at_close` (`:401`).

**OBSERVATION.** Consequently, if the `chain_hash` formula changes:

1. every pre-existing entry fails `recompute_for_entry` under the new rule;
2. every pre-existing segment manifest fails the Merkle-root recomputation;
3. any RFC 3161 token, had one been obtained, would attest a now-unreproducible
   imprint;
4. and nothing in the audit-entry path currently reads `schema`, so a verifier
   has **no in-band signal** telling it which rule to apply.

Point 4 is the sharp one: the compatibility problem is not merely "old logs
break", it is "old logs break silently and the verifier cannot tell why". That is
the substance of D-5, D-6 and D-7.

---

## 3. Current-State Finding

**P0-6 is CONFIRMED.**

The `violations` field is **outside the integrity boundary** of the hash chain
and, transitively, outside the Merkle root, the segment chain and the TSA imprint
(§2.8). An attacker or buggy operator with write access to the JSONL log can add,
remove, modify, reorder, or wipe violations, and all such mutations pass
`aura-replay` with `CHAIN OK` (§2.7).

This is a **substantive compliance integrity gap**: the chain proves *that a
decision was made*, but not *why*. Mutation class 5 is the sharpest form — a
`DENY` can be stripped of all substantiation while still verifying.

**OBSERVATION — bound on the exposure.** The nine covered fields cannot be
altered undetected. A tampered record can therefore be made *internally
inconsistent* (e.g. `decision: "DENY"` with `violations: []`), and a human reader
reasoning about it could notice. No automated check the product ships does.

**OBSERVATION.** This is a **post-write tampering** gap (integrity of the record
at rest), not a claim that the Guard computes violations incorrectly at runtime.
It is also pre-existing, not a regression: the field has been outside the digest
since the digest was defined.

---

## 4. The Integrity Boundary Today

| Field | In `chain_hash` | In Merkle leaf | In segment hash | In TSA imprint | Checked by `aura-replay` |
|---|:--:|:--:|:--:|:--:|:--:|
| `prev_hash`, `decision`, `policy_set`, `policy_hash`, `context`, `input_hash`, `shadow_hash`, `seq`, `timestamp` | ✅ | ✅ (via `chain_hash`) | ✅ | ✅ | ✅ |
| **`violations`** | ❌ | ❌ | ❌ | ❌ | ❌ |
| `schema`, `audit_id`, `request_id` | ❌ | ❌ | ❌ | ❌ | ❌ |
| `chain_hash` | n/a (output) | ✅ (is the leaf input) | ✅ | ✅ | ✅ |

---

## 5. Design Alternatives

**ALTERNATIVES — listed, not selected.** No option below is chosen, ranked as a
decision, or recommended in this section.

| # | Approach | Integrity | Complexity | Breaks existing logs | `f32` exposure |
|---|---|---|---|---|---|
| A | Include a violations reduction directly in `chain_hash` | Full | Low | Yes (digest rule) | Yes |
| B | Add a `violations_hash` field, fed into `compute_chain_hash` | Full | Medium | Yes (digest rule + schema) | Yes |
| C | Carry a `violations_hash` verified independently, outside `chain_hash` | Full, if the verifier checks it | Medium | No | Yes |
| D | Hash only identifying fields (`rule`, `action`, `validator`), excluding `confidence` | Partial | Low | Yes | No |
| E | Parallel Merkle tree over violation data, anchored in the manifest | Full | High | Entry chain unaffected; manifests change | Yes |
| F | No cryptographic binding; compensating controls (WORM, permissions, shipping) | None | None | No | No |

**OBSERVATION — the axes that actually separate these.**

- **Retroactive verifiability.** A, B, D break it. C, E, F preserve it.
- **Single-artifact verification.** A, B keep one digest to check. C, E add a
  second step a naive verifier can skip.
- **Fail-closed on omission.** Under C, an entry with the new field *stripped*
  must be distinguishable from a legitimately old entry, or the control is
  bypassable by deletion. The design must supply this; it is not automatic.
- **TSA coupling.** A, B, and E-if-anchored change `tsa_message_imprint`
  (§2.8 step 7).
- **`f32` exposure.** Every option except D and F brings §2.1's `f32` into a
  digest for the first time.

---

## 6. Recommendation (NON-NORMATIVE)

> **Advisory only.** Nothing in this section is decided, approved, or
> implementable as written. Each item maps to an open decision in §7 and has no
> force until that decision is taken by the human authority. If the authority
> decides otherwise, this section is simply wrong and the decision governs.

| # | Advisory opinion | Maps to |
|---|---|---|
| R-1 | Bring violations inside the integrity boundary rather than relying on procedural controls | D-1 |
| R-2 | Prefer a separate `violations_hash` fed into `compute_chain_hash` (Alternative B) over inlining, for independent verifiability and easier debugging | D-2 |
| R-3 | Consider bringing `schema` inside the digest at the same time, so the version discriminator cannot be silently rewritten | D-2, D-7 |
| R-4 | Define the reduction as compact deterministic bytes with fixed field order; represent `confidence` as a fixed-point integer rather than a rendered float (`aura-poc-a-core` sets that precedent in ADR-005) | D-3 |
| R-5 | Preserve violation order rather than sorting, to keep audit fidelity; do not deduplicate | D-4 |
| R-6 | Treat replay compatibility as a first-class deliverable, not a follow-up | D-5, D-6 |
| R-7 | Correct the `chain.rs:11–12` module doc-comment and the stale `models.rs:95` formula. This is a documentation fix and is independent of every decision below | — |
| R-8 | Write the §8 tests before the behaviour change, starting from the §2.7 harness with its assertions inverted | D-1…D-7 |

---

## 7. Decision Register — D-1 … D-7

**None of these is resolved by this ADR.** Each records evidence, alternatives
and consequences so the authority can decide. No approval is assumed anywhere.

### D-1 — Should violations be integrity-protected at all?

- **Current evidence.** They are not (§2.2, §2.7). The gap propagates to all four
  downstream mechanisms (§2.8). No test would catch a mutation (§2.6).
- **Alternatives.** (a) Yes — cryptographic binding (§5 A–E). (b) No — accept and
  document, with procedural controls only (§5 F). (c) Defer, and correct only the
  overstated documentation (R-7).
- **Consequences.** (a) changes a digest that four mechanisms inherit. (b) leaves
  "tamper-evident" claims broader than the implementation, which is then a
  documentation-accuracy obligation. (c) preserves the status quo risk.
- **Unresolved question.** Is the audit record required to bind *why* a decision
  was made, or only *that* it was made?
- **Status: OPEN.** Blocks all of P0-6. No approval assumed.

### D-2 — What exactly belongs to the integrity domain?

- **Current evidence.** Nine fields are covered; `violations`, `schema`,
  `audit_id`, `request_id` are not (§2.2, §4). `schema` being uncovered is what
  makes silent mis-verification possible (§2.9 point 4).
- **Alternatives.** (a) `violations` only. (b) `violations` + `schema`.
  (c) all four uncovered fields. (d) a separate digest carried alongside (§5 C/E)
  rather than widening the entry digest.
- **Consequences.** Widening the digest once is cheaper than twice, but enlarges
  the blast radius (§2.8) and the migration (D-5). Excluding `schema` leaves the
  version discriminator forgeable.
- **Unresolved question.** Is the integrity domain "the decision and its
  substantiation", or "the entire record"?
- **Status: OPEN.** Blocks design. No approval assumed. *(Subsumes the earlier
  draft's D-2 and D-6.)*

### D-3 — What canonical representation of violations is required?

- **Current evidence.** No canonicalization exists anywhere in the codebase;
  persistence is plain `serde_json::to_string` (§2.4). `confidence: f32` is the
  only float in the record (§2.1), parsed from policy YAML (`policy.rs:41`, `:94`).
  `merkle.rs:9–15` documents `0x00`/`0x01` domain separation — a precedent for
  the concept, but no convention for a third domain.
- **Alternatives.** (a) `serde_json` output as-is. (b) a custom fixed-order,
  delimited encoding. (c) a hash-of-hashes construction. For `confidence`:
  rendered text, fixed-point integer, fixed decimal places, raw IEEE-754 bits, or
  exclusion (§5 D).
- **Consequences.** Any choice becomes a cross-implementation determinism
  surface where none exists today: an independent verifier must reproduce the
  exact bytes. Float rendering is stable per toolchain but is not *specified*.
  `NaN`/infinity have no JSON representation and no guard in the code.
- **Unresolved question.** Which byte reduction is authoritative, and does
  `confidence` participate in it?
- **Status: OPEN.** No canonical serialization is selected by this ADR. No
  approval assumed. *(Subsumes the earlier draft's D-4.)*

### D-4 — Ordering, duplicates, empty lists, `None`/omitted fields, semantic equivalence

- **Current evidence.** Order = YAML declaration order (§2.3), and the decision
  aggregate does not depend on it (`engine.rs:58–65`). One rule yields at most
  one violation (`find`, not `find_iter`), so duplicates require two YAML rules
  sharing an `id`. Empty lists serialize as `[]` and are what every existing
  fixture contains (§2.6). `validator: None` is **omitted entirely** from the JSON
  (§2.1) — so absent and `None` are indistinguishable on disk.
- **Alternatives.** Order: preserve vs sort by rule id. Duplicates: reject,
  deduplicate, or accept as authored. Empty: a defined constant vs the empty
  string vs skipping the component. `None`: distinct marker vs identical to
  omitted. Equivalence: bit-identical vs structurally identical vs semantically
  identical.
- **Consequences.** Sorting makes the digest stable across policy reordering but
  discards the recorded sequence. Collapsing `None` and omitted forecloses ever
  distinguishing them. Failing to fix the empty-list form breaks every existing
  `violations: []` entry (D-5). Without an injectivity rule, two distinct
  violation lists could reduce to identical bytes.
- **Unresolved question.** For each of the five sub-cases, which representation
  is authoritative — and is the rule injective?
- **Status: OPEN.** No approval assumed. *(Subsumes the earlier draft's D-3 and
  D-7.)*

### D-5 — How are existing v1 logs handled after a chain-hash change?

- **Current evidence.** §2.9: every existing entry, every manifest Merkle root
  (`segment.rs:394`) and every `head_chain_hash_at_close` (`:401`) is computed
  under the current rule. Nothing in the audit-entry path reads `schema`
  (`log_writer.rs:151–170`), so there is no in-band discriminator.
- **Alternatives.** (a) Hard cut-over at a stated `seq`. (b) Version-aware
  verification keyed on `schema`. (c) Re-seal history under the new rule.
  (d) Choose a boundary-preserving design (§5 C/E) so the question does not
  arise. (e) Accept that history verifies only with an archived old binary.
- **Consequences.** (a) and (b) require the verifier to know the boundary; (b)
  requires `schema` itself to be trustworthy, which is D-2. (c) destroys the
  original digests and any timestamp anchoring over them. (d) trades retroactive
  verifiability for a second verification step a verifier can skip.
- **Unresolved question.** Is retroactive verifiability of existing v1 logs a
  requirement? If yes, by which mechanism?
- **Status: OPEN — explicitly not resolved by assumption.** No approval assumed.

### D-6 — How does the chosen design interact with replay verification?

- **Current evidence.** `aura-replay` runs `verify_chain`, optional lineage,
  `verify_segment_chain`, `verify_manifest_against_entries` (§2.9); none reads
  `violations`. Exit codes are documented in `docs/exit-codes.md` (Guard repo).
- **Alternatives.** (a) Violations tampering surfaces as the existing chain-break
  exit code. (b) A distinct exit code / failure class for violations integrity.
  (c) An independent verification step (§5 C/E) that a caller must opt into.
- **Consequences.** (a) is simplest but conflates two failure meanings for
  operators and any CI parsing exit codes. (b) is clearer but is an interface
  change. (c) risks a verifier reporting success while skipping the new check —
  the fail-closed-on-omission property in §5 must then be designed in explicitly.
- **Unresolved question.** What must `aura-replay` report, with which exit code,
  when violations fail to verify — and must the new check be impossible to skip?
- **Status: OPEN.** No approval assumed.

### D-7 — What compatibility/versioning mechanism is required?

- **Current evidence.** The audit-entry schema is an inline literal with no
  constant and no check (§2.9). The segment path already has the pattern:
  `SEGMENT_SCHEMA` + rejection at `sealer.rs:100` and `segment.rs:341`.
- **Alternatives.** (a) Mirror the segment pattern: a constant plus a rejecting
  check on the audit path. (b) Bump to `aura-guard.audit.v2` and verify
  version-aware. (c) A capability/feature flag rather than a version bump.
  (d) No mechanism — implied by choosing a non-breaking design.
- **Consequences.** Any mechanism only works if the discriminator is itself
  integrity-protected (D-2), otherwise it can be rewritten to force the weaker
  rule — a downgrade attack. A version bump also raises whether the `/v1/audit`
  HTTP response shape changes for existing integrators.
- **Unresolved question.** Which mechanism, and does the public API change?
- **Status: OPEN.** No approval assumed.

### 7.1 Numbering provenance

This register replaces the earlier draft's D-1…D-7 with the seven decisions named
in the P0-6 task. Nothing was dropped; the mapping is:

| This register | Earlier ADR draft | `GUARD-G1_INTEGRITY_DESIGN_BRIEF.md` §12 |
|---|---|---|
| D-1 | D-1 | D1 |
| D-2 | D-2, D-6 | D5, Q1 |
| D-3 | D-4 | D3, D4 |
| D-4 | D-3, D-7 | D3 (sub-questions) |
| D-5 | D-5 | D2, D7 |
| D-6 | — (new; was implicit in §4.7) | Q2 (related, not identical) |
| D-7 | — (new; was folded into D-5) | D6, D8 |

Cite the document alongside the identifier when approving — the three numbering
schemes do not coincide.

---

## 8. Test Plan (NON-NORMATIVE — to be written only after approval)

**Not implemented. No fixtures created.** Listed so the authority can see the
verification cost attached to each decision. The §2.7 harness is the starting
point; its assertions invert from `is_ok()` to a chain-break once a fix lands.

| # | Scenario | Expected after a D-1 "yes" | Gates |
|---|---|---|---|
| T-1 | **Modify** a violation (`confidence`, `action`, `rule`, `validator`) | verification fails at the tampered index | D-1, D-3 |
| T-2 | **Add** a fabricated violation | verification fails | D-1 |
| T-3 | **Remove** a violation that did occur | verification fails | D-1 |
| T-4 | **Reorder** two violations | fails if order is significant; identical digest if sorting was chosen — the test asserts whichever D-4 selects | D-4 |
| T-5 | **Duplicate** violations (two YAML rules sharing an id) | per D-4: both instances digested, or rejected | D-4 |
| T-6 | **Empty** violations list | a well-defined constant reduction; every existing `violations: []` entry behaves per D-5 | D-3, D-4, D-5 |
| T-7 | **Omitted vs `None`** `validator` | distinguishable, or provably identical — whichever D-4 selects; asserted, not incidental | D-3, D-4 |
| T-8 | **Semantically equivalent representations** (`0.1` / `0.10` / `0.100`; key reordering; whitespace) | identical digest after canonicalization; injectivity holds for distinct lists | D-3, D-4 |
| T-9 | **Existing v1 log replay** | verifies, or is rejected with a clear diagnostic per D-5/D-7 — never silently mis-verified | D-5, D-7 |
| T-10 | **Valid unchanged entry** (positive control) | verifies clean, round-trips through JSONL | all |
| T-11 | **Tampering with a protected field** (e.g. `decision`) | still detected — the §2.7 control must not regress | all |

**Additional coverage the decisions imply:** cross-architecture reproduction of
the digest (the arm64 leg absent from Guard CI today), a property test over
arbitrary violation vectors in the style of the five existing `proptest!` suites
(`chain.rs:426`, `engine.rs:305`, `normalizer.rs:445`, `validators.rs:374`,
`crypto.rs:248`), segment/TSA regression across the change (§2.8), and updating
`tests/golden.rs:21`, which currently discards violations.

---

## 9. Proposed Implementation Sequence — AFTER approval only

**NON-NORMATIVE and strictly conditional.** This is a proposed ordering, not a
plan of record and not authorization. Nothing below may start until D-1…D-7 are
decided by the human authority.

| Step | Action | Precondition |
|---|---|---|
| 0 | Documentation-only correction of `chain.rs:11–12` and `models.rs:95` (R-7) | None — independent of every decision |
| 1 | Record the authority's answers to D-1…D-7 in this ADR; flip status from DRAFT | D-1…D-7 decided |
| 2 | Land characterization tests that pin present behaviour (nine-field known-answer vector; §2.7 harness as-is) | Step 1 |
| 3 | Specify the canonical byte reduction as written text before code | D-3, D-4 |
| 4 | Implement the reduction plus its unit tests | Step 3 |
| 5 | Wire it into the chosen boundary (§5) | D-1, D-2 |
| 6 | Implement the compatibility/versioning mechanism | D-5, D-7 |
| 7 | Update `aura-replay` reporting and exit codes | D-6 |
| 8 | Invert the §2.7 assertions; complete the §8 matrix; update golden fixtures | Steps 4–7 |
| 9 | Segment/TSA regression and cross-architecture reproduction (§2.8) | Steps 4–7 |
| 10 | Adversarial review, then human sign-off per `CLAUDE.md` workflow | All above |

Steps 1–10 belong to `aura-guard-v1.3`. None has been performed.

---

## 10. References

**`aura-guard-v1.3` @ `443f72e` (read-only):**

- `src/models.rs` — `Violation` (L32), `AuditEntry` (L50), `violations` (L90),
  `chain_hash` + stale formula comment (L95–96)
- `src/chain.rs` — module doc (L1–12), `SEP` (L20), `compute_chain_hash`
  (L25–49), `recompute_for_entry` (L53), `verify_chain` (L71), empty fixture
  (L112)
- `src/engine.rs` — `evaluate` (L14), first-match regex `pattern.find` (L28),
  `violations.push` (L50), decision aggregate (L58–65)
- `src/policy.rs` — order-preserving rule compilation (L233–237), `score: f32`
  (L41, L94)
- `src/log_writer.rs` — `append` (L88), `serde_json::to_string` (L96),
  `read_all_entries` (L151–170)
- `src/api/audit.rs` — `evaluate` call (L113), `compute_chain_hash` (L119),
  `schema` literal (L132), `violations` stored (L143), `append` (L149)
- `src/merkle.rs` — domain-separation doc (L9–15), `leaf_hash` (L29–34)
- `src/segment.rs` — `SEGMENT_SCHEMA` (L44), `segment_chain_preimage` (L91–106),
  `recompute_segment_chain_hash` (L109–121), `tsa_message_imprint` (L123–131),
  `entry_leaf_hash` (L140–150), `segment_merkle_root` (L151–158),
  `verify_segment_chain` (L335, schema check L341–342),
  `verify_manifest_against_entries` (L382–405)
- `src/sealer.rs` — manifest schema check (L100)
- `src/bin/aura_replay.rs` — `verify_chain` (L113), lineage (L134–153),
  `verify_segment_chain` (L175), `verify_manifest_against_entries` (L194)
- `tests/golden.rs` — discards violations (L21)

**This repository:**

- `docs/evidence/P0-1_EVIDENCE.md` — P0-1 closure (closed; not reopened here)
- `review/2026-08-11_ENGINEERING_BASELINE/GUARD-G1_INTEGRITY_DESIGN_BRIEF.md` —
  the prior read-only design brief (different D-numbering; see §7.1)
- `review/2026-08-11_ENGINEERING_BASELINE/GUARD-G1_DECISION_PACKAGE.md`
- `review/2026-08-11_ENGINEERING_BASELINE/08_BLOCKERS.md` — P0-6 origin

---

## 11. Explicit Non-Goals

This ADR did **not**: write or modify any code in `aura-guard-v1.3`; touch
`chain.rs`; implement violations hashing; select a canonical serialization or
hash domain; change the log format; create a migration; create test fixtures;
resolve D-1 through D-7; modify ARI, P0-1, or `aura-poc-a-core-v3.3` runtime
code; broaden into a general Guard audit; or open a pull request against the
Guard repository.

---

*Prepared in controlled execution mode. No code was modified in either
repository. The §2.7 evidence test was executed in an ephemeral clone and was
never committed. All recommendations are explicitly NON-NORMATIVE and remain
advisory until the Chief Architect / Protocol Custodian decides D-1 … D-7.*
