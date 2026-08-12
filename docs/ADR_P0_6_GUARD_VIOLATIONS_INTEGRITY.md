# ADR-P0-6: Guard Violations Integrity

**Status:** DRAFT — NON-NORMATIVE — REQUIRES HUMAN APPROVAL
**Scope:** `aura-guard-v1.3` only
**Date:** 2026-08-12
**Author:** Claude (conformance audit role, per `CLAUDE.md`)
**Authority:** Pending Chief Architect / Protocol Custodian approval
**Finding status:** CONFIRMED — verified against source **and** by executable proof (§2.7)
**Evidence basis:** `AuraIDToken/aura-guard-v1.3` @ commit `443f72e`
**Independent re-verification:** 2026-08-12 — all file/line references and the
§2.7 test-count arithmetic re-checked against a fresh read-only clone at
`443f72e`; documentation-only corrections applied to §2.2, §8 and §9.

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

---

## 1. Context

P0-1 is closed and verified (see `docs/evidence/P0-1_EVIDENCE.md`). This ADR
addresses P0-6:

> Aura-Guard audit violations must have verifiable integrity.

The Guard claims tamper-evident audit logging via a SHA-256 hash chain. The
question is whether `violations` — the list of rule matches that substantively
explain *why* a decision was made — are integrity-protected by that chain.

---

## 2. Evidence Summary

All file/line references below were confirmed at commit `443f72e`.

### 2.1 Data Model

**File:** `src/models.rs` — `Violation` at line 32, `AuditEntry` at line 50

```rust
pub struct Violation {
    pub rule: String,
    pub action: String,
    pub confidence: f32,
    pub validator: Option<String>,
}
```

- `AuditEntry` holds `violations: Vec<Violation>` alongside `chain_hash`.
- Both structs derive `Serialize`/`Deserialize` via serde.
- `validator` carries `skip_serializing_if = "Option::is_none"`, so it is
  **omitted entirely** when `None` — relevant to any canonicalization design.

### 2.2 Chain Hash Construction

**File:** `src/chain.rs` — `compute_chain_hash` at lines 25–49

```rust
let canonical = [
    prev_hash, decision, policy_set, policy_hash,
    context, input_hash, shadow_hash,
    &seq.to_string(), timestamp,
]
.join(SEP);   // SEP = "|"
sha256_hex(&canonical)
```

**Finding:** `violations` is **NOT** an input to `compute_chain_hash`.

Covered: `prev_hash`, `decision`, `policy_set`, `policy_hash`, `context`,
`input_hash`, `shadow_hash`, `seq`, `timestamp`.

**Not** covered: `violations`, `audit_id`, `request_id`, `schema`.

The module doc-comment at the top of `src/chain.rs` states that "Tampering with
any field — *or with the order of records* — breaks the chain." As written this
is **inaccurate**: four fields are outside the digest. The doc-comment
overstates the guarantee.

The `AuditEntry::chain_hash` doc-comment (`src/models.rs`) is also stale — it
omits `policy_hash` and `context`, both of which *are* hashed.

### 2.3 Violations Creation

**File:** `src/engine.rs` — `evaluate` at line 14

```rust
pub fn evaluate(shadow: &str, context: &str, rules: &[CompiledRule]) -> (String, Vec<Violation>)
```

**Finding:** `violations` order equals declaration order of matching rules in
the policy YAML. Confirmed that line 28 uses `rule.pattern.find(shadow)`
(first match only), not `find_iter`, so one rule contributes at most one
violation.

### 2.4 Log Persistence

**File:** `src/log_writer.rs` — `append` at line 88

The entire `AuditEntry` — including `violations` — is serialized to JSONL via
`serde_json::to_string` (line 96) and persisted verbatim. However, `chain_hash`
is computed **before** serialization and does not cover `violations`.

### 2.5 Replay Verification

**File:** `src/chain.rs` — `verify_chain` at line 71

`verify_chain` calls `recompute_for_entry`, which delegates to
`compute_chain_hash`. Since that function ignores `violations`, **modifying the
violations list after the entry is written does not break chain verification.**

### 2.6 Existing Chain Tests

`violations` appears exactly **once** in `src/chain.rs` — at line 112, as
`violations: vec![]` in the test fixture. No existing test covers non-empty
violations, tamper detection on violations, or violation ordering.

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

**This test was NOT committed.** It was written solely to generate this
evidence; the clone was reverted to pristine afterwards. Landing it belongs to
the implementation phase in `aura-guard-v1.3`.

---

## 3. Current-State Finding

**P0-6 is CONFIRMED.**

The `violations` field is **outside the integrity boundary** of the hash chain.
An attacker or buggy operator with write access to the JSONL log can add,
remove, modify, reorder, or wipe violations, and all such mutations pass
`aura-replay` with `CHAIN OK` (§2.7).

This is a **substantive compliance integrity gap**: the chain proves *that a
decision was made*, but not *why*. Mutation class 5 is the sharpest form — a
`DENY` can be stripped of all substantiation while still verifying.

Note this is a **post-write tampering** gap (integrity of the record at rest),
not a claim that the Guard computes violations incorrectly at runtime.

---

## 4. Analysis of Required Decisions

### 4.1 Are violations part of the integrity-protected audit record?

**Current state:** No. **Question for authority:** Should they be?

Arguments FOR inclusion:
- Without violations, the log says "DENY" but cannot prove which rules fired.
- Regulatory frameworks (EU AI Act Art. 13) require explainability. A decision
  without substantiation is not transparent.
- The Guard markets itself as "tamper-evident". A log that hides tampering in
  violations does not meet that description, and its own module doc-comment
  asserts a guarantee it does not provide (§2.2).

Arguments AGAINST inclusion:
- `decision` already captures the outcome; violations are derivative.
- Including violations increases hash sensitivity to rule ordering and
  confidence scores, which may change between policy versions.
- `input_hash` and `shadow_hash` already bind the input, so re-running the same
  policy should reproduce the same violations.

**Observation:** the re-run reproducibility argument assumes a static policy.
`policy_hash` is in the chain, so the *policy identity* is pinned — but
reproduction requires still **possessing** that exact policy file. Nothing in
the log guarantees the policy is retrievable. The chain must protect the
*recorded* violations, not merely the *reproducible* ones.

### 4.2 What canonical representation is required?

- **A. `serde_json::to_string` on `Vec<Violation>`** — trivial, reuses JSONL
  path; but depends on serde_json formatting and `f32` float rendering.
- **B. Custom canonical format** (pipe-delimited, fixed field order) — fully
  deterministic; more code.
- **C. Hash-of-hashes (Merkle-like)** — supports partial verification; likely
  overkill for small lists.

Note the `skip_serializing_if` on `validator` (§2.1) means option A must define
whether an absent validator and a `None` validator canonicalize identically.

### 4.3 Does ordering of violations matter?

**Current behavior:** order = rule declaration order in the YAML (§2.3).

- If order is significant: hash as-is.
- If not: sort (e.g. by rule ID) so the hash is stable across policy reordering.

**Observation:** order currently matters for human readability, but not for the
decision logic (`deny > review > allow` is order-independent).

### 4.4 How are duplicate violations treated?

Confirmed `engine.rs` uses `find` (first match only), so a single rule cannot
self-duplicate. Duplicates arise only if two YAML rules share an `id`.
**Question:** deduplicate, or treat the YAML as the author's responsibility?

### 4.5 What happens with an empty violations list?

Empty `Vec<Violation>` serializes as `[]`. If violations enter the chain hash,
the empty case needs a well-defined canonical form. This matters for backward
compatibility: every existing entry with `violations: []` must either keep
verifying or be explicitly migrated.

### 4.6 What constitutes semantically equivalent representation?

Bit-identical vs structurally identical vs semantically identical. The chain
must state which level it enforces. **Recommendation (NON-NORMATIVE):** start
with bit-identical canonical JSON; document that future versions may relax.

### 4.7 Inline in `chain_hash`, or a separate `violations_hash`?

- **Option A — include violations directly in `chain_hash`:** single hash, no
  schema change; but changes the chain hash format for all existing logs.
- **Option B — add a `violations_hash` field**, then feed it into
  `compute_chain_hash`: separates concerns, independently verifiable, easier to
  debug; requires a schema bump.
- **Option C** is equivalent to A.

**Observation:** Option B is architecturally cleaner. Either way, existing
`aura-guard.audit.v1` logs will no longer recompute to their stored digests
unless verification is version-aware — so a **replay compatibility path is
required**, not merely a schema bump. `schema` is currently *outside* the chain
(§2.2), which itself needs addressing if the version is to be trusted.

### 4.8 What tests are required to prove integrity?

Round-trip; tamper detection; order sensitivity; empty list; duplicate rule
IDs; float stability. The harness in §2.7 is a working starting point — its
assertions need inverting from `is_ok()` to `ChainBreak` once the fix lands.

---

## 5. Alternatives and Trade-offs

| Approach | Integrity | Complexity | Breaking Change | Float Risk |
|---|---|---|---|---|
| A. Include violations in `chain_hash` | Full | Low | Yes (hash format) | High |
| B. Add `violations_hash` field | Full | Medium | Yes (schema) | Medium |
| C. Hash only rule IDs (ignore confidence) | Partial | Low | Yes | None |
| D. Do nothing (status quo) | None | None | No | None |
| E. Separate Merkle tree | Full | High | Yes | Medium |

---

## 6. Recommendation (NON-NORMATIVE)

**Pending human authority approval.**

1. **Adopt Option B** (separate `violations_hash`), fed into `compute_chain_hash`.
2. **Define canonical serialization** as compact deterministic JSON with fixed
   field order and `confidence` converted to a **fixed-point integer** (or
   rounded to 4 dp) to eliminate `f32` platform jitter. Prefer fixed-point:
   `aura-poc-a-core` already establishes that precedent in ADR-005.
3. **Preserve violation order** as-is (do not sort) to maintain audit fidelity.
4. **Do not deduplicate**; treat the YAML as the source of truth.
5. **Bump schema** `aura-guard.audit.v1` → `v2`, and bring `schema` itself
   inside the chain digest so the version cannot be silently rewritten.
6. **Define a replay compatibility path** for existing v1 logs (see §4.7).
7. **Correct the `src/chain.rs` module doc-comment and the `chain_hash`
   doc-comment in `src/models.rs`**, both of which currently misstate coverage
   (§2.2). This is worth doing regardless of the D-1 outcome.
8. **Write tests** covering all scenarios in §4.8, starting from §2.7.

---

## 7. Test Plan (for eventual implementation)

| Test ID | Scenario | Expected Result |
|---|---|---|
| T-1 | Entry with 3 violations round-trips through JSONL | `violations_hash` matches |
| T-2 | Modify `confidence` in JSONL, replay | `ChainBreak` at tampered index |
| T-3 | Swap violation order, replay | `ChainBreak` at tampered index |
| T-4 | Remove middle violation, replay | `ChainBreak` at tampered index |
| T-5 | Empty violations list | `violations_hash` is a well-defined constant |
| T-6 | Duplicate rule IDs | Hash includes both instances |
| T-7 | `confidence` 0.1 / 0.10 / 0.100 | Same hash after canonicalization |
| T-8 | Pre-existing v1 log with `violations: []` | Verifies per the §4.7 compatibility path |

---

## 8. Unresolved Decisions Requiring Human Approval

| ID | Question | Blocking? |
|---|---|---|
| D-1 | Should violations be integrity-protected at all? | **YES** — blocks all of P0-6 |
| D-2 | Option A (inline) vs Option B (separate hash) vs other? | **YES** — blocks design |
| D-3 | Is violation order semantically significant? | **YES** — affects canonicalization |
| D-4 | How to handle `f32` confidence determinism? | **YES** — affects canonicalization |
| D-5 | Replay compatibility path for existing v1 logs? | **YES** — raised from non-blocking; without it, replay of existing logs breaks |
| D-6 | Should `schema` / `audit_id` / `request_id` also enter the chain? | No — related but separable |
| D-7 | Should deduplication happen? | No — can default to "no dedup" |

**Note on numbering.** The `D-n` identifiers above are local to this ADR. They do
**not** correspond to the `D1`–`D8` identifiers in
`review/2026-08-11_ENGINEERING_BASELINE/GUARD-G1_INTEGRITY_DESIGN_BRIEF.md` §12,
which numbers the same decision surface differently (e.g. this ADR's D-5
"replay compatibility" is the brief's D2/D6/D7, while the brief's D5 is the hash
domain question). Cite the document alongside the identifier when approving.

---

## 9. References

- `src/models.rs` — `Violation` (L32), `AuditEntry` (L50)
- `src/chain.rs` — `compute_chain_hash` (L25), `recompute_for_entry` (L53), `verify_chain` (L71)
- `src/engine.rs` — `evaluate` (L14), first-match regex `pattern.find` (L28), violation creation `violations.push` (L50)
- `src/log_writer.rs` — `append` (L88)
- `docs/evidence/P0-1_EVIDENCE.md` — P0-1 closure (this repository)

---

*Prepared in controlled execution mode. No code was modified in either
repository. The §2.7 evidence test was executed in an ephemeral clone and
reverted. All recommendations are explicitly NON-NORMATIVE pending Chief
Architect approval.*
