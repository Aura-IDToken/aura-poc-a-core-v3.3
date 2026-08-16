# INFRA-003 — Guard Verification & Regression Harness

**Type:** implementation / test infrastructure. **Normative effect: NONE.**
**Date:** 2026-08-16
**Code repository:** `AuraIDToken/aura-guard-v1.3`, branch
`claude/auditentry-adapter-dq-001-h0os71`, commit **`8240d9d`**
**Artifact repository:** this repository (per the `review/` convention and REPO-001 §5)
**Production files changed:** **0** — `git diff` over tracked files is empty.

---

## 1. Scope

Extend INFRA-001 and INFRA-002 with a **closed regression layer** that detects unintended
changes to already-observed cryptographic and byte-level behaviour of `aura-guard-v1.3`.

**This is not an architecture task.** The harness tests **what the implementation does
today**. It does not state what the protocol should do, and no test in it depends on an
unresolved DQ.

---

## 2. Baseline

Captured before any change, on a clean tree:

| Item | Value |
|---|---|
| Branch | `claude/auditentry-adapter-dq-001-h0os71` |
| HEAD before | `d704285` (INFRA-002) |
| `git status --short` | *(empty — clean)* |
| **Baseline test count** | **275 passed, 0 failed** |
| Existing fixtures | 12 under `tests/fixtures/hash_domains/`, 3 under `tests/fixtures/byte_representations/` |

---

## 3. Existing infrastructure reused

| Reused | How |
|---|---|
| `tests/support/mod.rs` (INFRA-002 framework) | Imported via `mod support;` — `ByteFixture::from_json`, `replay`, `compare_bytes`, `fixtures_dir`, `FixtureStatus`, `Property`. **No new helper duplicates it.** |
| INFRA-001 fixtures (12 files) | Read **read-only**. Their distinct schema (`source_ref`, `input_utf8`, `not_canonical`) is parsed as raw `serde_json` rather than forced into the INFRA-002 model — appropriate for a regression test that must assert *exact recorded strings*. |
| INFRA-002 fixtures (3 files) | Read through the framework's own `from_json` / `replay` path. |

**No fixture was recorded, edited, renamed or reclassified.** INFRA-003 never writes a
fixture; recording remains with `HASH_DOMAINS_RECORD` (INFRA-001) and
`BYTE_FIXTURES_RECORD` (INFRA-002).

### 3.1 How this avoids duplicating INFRA-001/002

| Dimension | INFRA-001 / INFRA-002 | INFRA-003 |
|---|---|---|
| Fixture selection | Fixed list, each constructed in-test | **Directory-driven sweep** — catches added, removed, renamed or corrupted fixtures |
| Governance metadata | Written into fixtures | **Pinned and asserted** — a silent reclassification fails |
| Mutations covered | single byte, value | **field order, separator, encoding** (new) |

---

## 4. New regression coverage

All ten requested properties, mapped to tests:

| # | Property | Test | Note |
|---|---|---|---|
| 1 | Hash-domain fixtures reproduce exactly | `regression_every_hash_domain_fixture_replays` | Sweep; asserts `checked == 11` so it cannot pass vacuously |
| 2 | Byte observations reproduce exactly | `regression_every_byte_representation_fixture_replays` | Sweep; asserts `checked == 3` |
| 3 | preimage → digest relationships stable | both sweeps + `regression_stored_entry_observations_agree_across_harnesses` | Third compares HD-001 and BR-001 **at file level**, distinct from INFRA-002's recompute-level check |
| 4 | Mutated input → different digest | `mutation_field_value_detected` | `DENY` → `ALLOW` in the recorded preimage |
| 5 | Byte-level mutation detected | `mutation_single_byte_detected_on_raw_fixture` | On BR-003, which is **not** valid UTF-8 |
| 6 | UTF-8 byte-sensitivity | `mutation_encoding_detected` | Same text re-encoded UTF-16LE |
| 7 | Field-order changes detectable | `mutation_field_order_detected` | See §5 |
| 8 | Separator changes detectable | `mutation_separator_detected` | See §5 |
| 9 | Timestamp representation changes detectable | `mutation_timestamp_representation_detected` | Uses the existing BR-001/BR-002 pair |
| 10 | Fixtures remain classified AS_IS_OBSERVED / PROPOSED / UNKNOWN | `regression_infra_001_classification_unchanged`, `regression_infra_002_classification_unchanged`, `regression_no_fixture_became_normative`, `regression_unknown_properties_remain_unknown`, `regression_inventory_counts_and_unknowns_unchanged` | Guards the reclassification stop condition |

Plus two structural regressions:

- `regression_hash_domain_fixture_inventory_unchanged` — exact 12-filename set.
- `regression_byte_representation_fixture_inventory_unchanged` — exact 3-filename set.

And the invariant itself, made machine-checkable:

- `regression_observed_is_not_normative_disclaimer_present` — all **15** fixture files
  still carry a disclaimer denying specification standing.

---

## 5. Mutation / negative tests

**All are harness-sensitivity checks. None is a security claim, and none makes any
assertion about SHA-256's properties.**

Only properties an existing fixture actually records were mutated — field order,
separator, encoding and timestamp form are all recorded in HD-001 / BR-001 / BR-002 /
`INVENTORY.json`. No new cryptographic domain was invented.

| Test | Mutation | Why it is a real test |
|---|---|---|
| `mutation_field_value_detected` | field 2 `DENY` → `ALLOW` | baseline value sensitivity |
| `mutation_field_order_detected` | swap fields 6 and 7 (`input_hash` ↔ `shadow_hash`) | **both are 64-char hex, so length and byte multiset are preserved** — length alone cannot be the signal, only order-sensitivity can |
| `mutation_separator_detected` | `U+007C` → `U+001F` | **length-preserving** one-byte substitution |
| `mutation_encoding_detected` | UTF-8 → UTF-16LE of the same text | asserts the two lengths differ, then that bytes and digests differ |
| `mutation_timestamp_representation_detected` | BR-001 (`+00:00`) vs BR-002 (`Z`) | asserts same `construction_id`, different bytes, different digest. **Asserts nothing about which form is correct**; BR-002 stays PROPOSED |
| `mutation_single_byte_detected_on_raw_fixture` | flip low bit of last byte of BR-003 | proves detection on **non-UTF-8** bytes |

The two length-preserving mutations (order, separator) are the substantive additions: a
naive harness that compared only lengths or digests-of-lengths would pass them.

### 5.1 Sensitivity verified, not assumed

A regression harness that never fails proves nothing. Two deliberate corruptions were
applied to committed fixtures and then reverted:

| Injected fault | Result |
|---|---|
| `HD-005_merkle_leaf.json` — `sha256` replaced with `0…0` | **FAILED** — `regression_every_hash_domain_fixture_replays`: *"HD-005_merkle_leaf.json: replaying the stored bytes no longer reproduces the stored digest"* (16 passed, 1 failed) |
| `BR-002…json` — `status` `PROPOSED` → `NORMATIVE` | **FAILED ×2** — `regression_infra_002_classification_unchanged` (*"epistemic classification changed"*) and `regression_no_fixture_became_normative` (*"a fixture was promoted to NORMATIVE"*) (14 passed, 3 failed) |

Both fixtures were restored with `git checkout --`; `git diff --stat HEAD -- tests/fixtures/`
is **empty**, confirming byte-for-byte restoration. The suite then returned to 292/292.

---

## 6. Tests added

**17**, in one new target `tests/regression.rs`:

| Group | Tests |
|---|---|
| Inventory regression | 2 |
| Sweep replay + cross-harness | 3 |
| Governance / classification | 5 |
| Mutation / negative | 6 |
| Invariant disclaimer | 1 |

---

## 7. Test results

| Gate | Result |
|---|---|
| `cargo test --test regression` | **17 passed, 0 failed** |
| `cargo test --test hash_domains` (INFRA-001) | **17 passed, 0 failed** |
| `cargo test --test byte_representations` (INFRA-002) | **18 passed, 0 failed** |
| `cargo test --all-targets` | **292 passed, 0 failed** |
| `cargo fmt --check` | **clean** |
| `cargo clippy --tests --all-targets` | **clean — 0 errors, 0 warnings** |

**Baseline 275 → final 292 (+17).** No pre-existing test changed status.

---

## 8. Production-code impact

**NONE.**

| Check | Result |
|---|---|
| `git diff --stat` (tracked files) | **empty** |
| `git status --short` | one new untracked path: `tests/regression.rs` |
| `src/` touched | **NO** |
| `Cargo.toml` / `Cargo.lock` touched | **NO** |
| Public API added or changed | **NO** |
| Test-only production seam added | **NO** |
| Fixtures edited or reclassified | **NO** — `git diff --stat HEAD -- tests/fixtures/` empty |
| Previous review artifacts modified | **NO** |

The harness reads only what is already `pub` or already on disk. **No point in this task
required a production change**, so the stop-and-report path was not triggered.

---

## 9. Normative impact

**NONE.** APS-200, APS-300, APS-100, SPEC-002 and `AUDIT_LAYER_SPEC.md` were not read for
authority and not modified. No ADR was created or amended. No normative decision was made.

---

## 10. DQ boundary

```
DQ-002: UNCHANGED
DQ-006: UNCHANGED
```

The harness asserts **none** of the prohibited claims. Specifically absent:
`chain_hash == integrity_hash`; "`chain_hash` is the canonical protocol hash";
`evidence_hash == integrity_hash`; "this serialization is the protocol canonical
serialization"; "RFC 8785/JCS is the Aura canonical serialization"; "APS-200 requires this
exact byte sequence".

The module documentation states the exclusion explicitly, and one test
(`regression_observed_is_not_normative_disclaimer_present`) enforces the invariant
mechanically across all 15 fixture files:

```
OBSERVED IMPLEMENTATION BEHAVIOR  !=  NORMATIVE PROTOCOL CONTRACT
```

**No PROPOSED fixture was converted to normative behaviour**, and **no UNKNOWN property
was converted to known** — `regression_unknown_properties_remain_unknown` and
`regression_inventory_counts_and_unknowns_unchanged` fail if either happens.

Also unchanged: DQ-001 (direction B; CONFLICT / OPEN; no implementation authorization; ADR
not approved), DQ-003, DQ-004, DQ-005, DQ-007, DQ-008, and every registered conflict.

---

## 11. Files changed

`AuraIDToken/aura-guard-v1.3` @ `8240d9d` — **1 file, 632 insertions, new**:

| File | Lines |
|---|---|
| `tests/regression.rs` | 632 |

This repository: this artifact only.

---

## 12. Commit SHA

| Item | Value |
|---|---|
| Guard commit | **`8240d9d`** |
| Guard branch | `claude/auditentry-adapter-dq-001-h0os71` |
| Guard HEAD before | `d704285` |
| Review artifact commit | *(this artifact's commit in `aura-poc-a-core-v3.3`)* |

---

## 13. Final status

> ## **COMPLETE**

No stop condition was triggered: no production change was required, no new public API was
needed, no normative decision was required, no fixture required reclassification, neither
DQ-002 nor DQ-006 needed resolving to continue, and repository placement stayed
unambiguous (code → guard, review → poc-a-core, per REPO-001).

**No PR was opened. No merge to `main`.**
