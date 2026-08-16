# INFRA-002 — Canonical-Byte Fixture Framework

**Type:** infrastructure. **Normative effect: NONE.**
**Date:** 2026-08-15
**Code repository:** `AuraIDToken/aura-guard-v1.3`, branch
`claude/auditentry-adapter-dq-001-h0os71`, commit **`d704285`**
**Artifact repository:** this repository (the `review/` convention lives here)
**Production files changed:** **0** — `git diff` over tracked files is empty.

> **Note on the task name.** "Canonical-Byte" is retained in the directory and title for
> project continuity only. The framework's internal terminology deliberately does not use
> it — see §2 and §12.

---

## 1. Objective

Extend the INFRA-001 harness with a **generic, reusable fixture framework** able to
represent:

1. observed implementation bytes;
2. alternative byte representations;
3. expected digests;
4. metadata describing how the bytes were obtained;
5. deterministic replay;
6. byte-for-byte comparison between fixtures.

…while keeping **OBSERVED**, **PROPOSED** and **NORMATIVE** strictly distinct and
treating none of them as canonical.

---

## 2. Governance boundary

> **DQ-006 remains unresolved. This framework does not establish canonical
> serialization.**

Nothing in INFRA-002 defines, selects, approves or implies:

| Not decided | Not decided |
|---|---|
| canonical serialization | JSON vs CBOR vs protobuf |
| UTF-8 vs another encoding | field ordering |
| separators | optional-field rules |
| timestamp representation | numeric representation |

No production serialization or cryptographic semantics were modified. `chain_hash` is
untouched. `integrity_hash`, `event_payload_hash` and `previous_record_hash` are **not**
implemented. No ADR was created. APS-200, APS-100, APS-300 and SPEC-002 are untouched.

**The framework provides no defaults.** It offers no default encoding, no default field
order and no default separator. A fixture states only what was *observed*, or what a
*synthetic comparison input happens to use*. That absence is deliberate: a default would
be a de-facto proposal.

**Governance baseline carried unchanged:** DQ-001 direction B / CONFLICT / OPEN, no
implementation authorization, ADR not approved; DQ-002 CONFLICT; DQ-006 CONFLICT;
INFRA-001 complete.

---

## 3. Relationship to INFRA-001

**The approach is reused. The fixtures are not migrated.**

INFRA-001's fixture files keep their own schema (`source_ref`, `input_utf8`,
`not_canonical`), their own directory (`tests/fixtures/hash_domains/`) and their own
recording flag (`HASH_DOMAINS_RECORD`), **byte-for-byte unchanged**. `git diff` over
tracked files is empty, which is the mechanical proof.

**Why no migration.** The task permits migration only if "purely mechanical", and
requires byte-for-byte preservation if done. Rewriting eleven committed fixture files of a
harness already signed off as COMPLETE carries risk with no functional gain, so the two
schemas coexist. What *is* shared is the design: hex + length + digest, opt-in recording,
replay-on-every-run.

**Two tests pin the separation** so a later change cannot silently absorb INFRA-001:

| Test | Asserts |
|---|---|
| `infra_001_fixtures_remain_in_their_own_schema` | INFRA-001 markers `source_ref` and `input_utf8` still present; its status wording unchanged; INFRA-002's `representation_id` **absent** from INFRA-001 files |
| `infra_001_and_infra_002_observe_identical_entry_bytes` | Both harnesses observe **byte-identical** entry-chain bytes, compared through `compare_bytes` |

The second test is the substantive one: INFRA-001 `HD-001` and INFRA-002 `BR-001`
independently produce the same 315 bytes and the same digest
`506549e15dad5fda9b498087b2f543d4425bcbcf6461eeced29e4ceadf0a2ecd`. Two harnesses, one
answer.

---

## 4. Fixture model

`tests/support/mod.rs` — `ByteFixture`:

| Field | Meaning |
|---|---|
| `fixture_id` | Unique fixture name |
| `status` | **Mandatory** epistemic status — §4.1 |
| `construction_id` | **Semantic identity** — shared across representations |
| `representation_id` | Distinguishes representations of that same object |
| `input_bytes_hex` | **Authoritative** byte record |
| `input_length` | Byte count |
| `sha256` | Digest, **computed from the bytes at construction** |
| `encoding` / `field_order` / `separator` | `Property::Known(..)` or `Property::Unknown` |
| `source` | Where the bytes came from |
| `notes` | Free text, including the non-proposal disclaimer on synthetic fixtures |
| `governance` | Emitted into every fixture file: "DQ-006 unresolved. This fixture does not establish canonical serialization." |

Two integrity properties fall out of the design:

- **A fixture cannot lie about its own digest.** `ByteFixture::new` computes `sha256` from
  the bytes; a caller cannot supply a mismatched pair.
- **`FixtureSpec` prevents transposition.** The many string parameters are passed as a
  named struct rather than positionally.

### 4.1 Epistemic status

| Status | Meaning | Used by |
|---|---|---|
| `AS_IS_OBSERVED` | Bytes read out of the current implementation | BR-001 |
| `PROPOSED` | **Synthetic comparison input.** Never a proposed protocol serialization | BR-002, BR-003 |
| `NORMATIVE` | Representable so the model is complete | **no fixture** |

`no_fixture_is_labelled_normative` walks the fixture directory and fails if any file
carries `NORMATIVE`. The status exists so the model can express the distinction — not
because any byte representation has normative standing.

### 4.2 UNKNOWN is never inferred

`Property::Unknown` serialises as the literal `"UNKNOWN"`.
`br_003_unknown_properties_round_trip` asserts it survives the write/read cycle and is not
silently filled in.

---

## 5. Representation model

```
construction_id  (semantic identity)
        │
        ├── representation_id: observed_rust_delimited          [AS_IS_OBSERVED]
        ├── representation_id: synthetic_delimited_timestamp_z  [PROPOSED]
        └── …
```

**No representation is authoritative over any other.** The framework offers no mechanism
to mark one as preferred, and none is.

| Fixture | `construction_id` | `representation_id` | Status |
|---|---|---|---|
| `BR-001_entry_chain_observed_rust` | `SEM-001_entry_chain_record` | `observed_rust_delimited` | AS_IS_OBSERVED |
| `BR-002_entry_chain_synthetic_timestamp_z` | `SEM-001_entry_chain_record` | `synthetic_delimited_timestamp_z` | PROPOSED |
| `BR-003_demo_object_unknown_properties` | `SEM-002_framework_demonstration_object` | `synthetic_opaque` | PROPOSED |

**On BR-002.** It renders the same semantic fields with a `Z` timestamp instead of the
`+00:00` form the implementation emits. Its `notes` field states in the fixture file
itself: *"Does NOT propose the Z timestamp form or any other form."* It exists to
demonstrate that an unresolved representation choice changes the bytes — which is
precisely the hazard DQ-006 has to settle, and precisely what this framework must not
settle for it.

---

## 6. Byte comparison

`compare_bytes(a, b) -> ByteComparison` over **raw bytes**:

| Field | Value |
|---|---|
| `equal` | byte equality |
| `len_a`, `len_b` | both lengths |
| `first_diff_offset` | `Option<usize>` — for a strict prefix, the shorter length |
| `byte_a_at_diff`, `byte_b_at_diff` | `Option<u8>` each — `None` on the side that ended |
| `sha256_a`, `sha256_b` | both digests |

**Decoded strings are never the authoritative comparison.**
`comparison_operates_on_raw_bytes_not_text` makes the point concretely: the text `"Aé"`
encoded as UTF-8 (`41 C3 A9`) and as Latin-1 (`41 E9`) is the *same text* and **different
bytes** with different digests. Comparing decoded text would have called them equal.

Behaviour is pinned by five tests: equality, first-differing-byte location, the prefix
relationship, empty inputs, and the raw-bytes-not-text case.

---

## 7. Replay

```
stored input_bytes_hex → raw bytes → SHA-256 → compare to stored sha256
```

`replay()` returns `ReplayOutcome { fixture_id, expected_sha256, actual_sha256, matched }`,
so a failure names all three. `assert_stored_and_replayed()` additionally verifies that
the stored bytes, length and **epistemic status** still match the current observation
before replaying — a status change is caught as well as a byte change.

`replay_reports_failure_fields` proves the failure path by deliberately corrupting a
recorded digest and asserting the reported fields.

Recording is opt-in (`BYTE_FIXTURES_RECORD=1`), so an ordinary `cargo test` can never
rewrite a fixture into agreement with changed code.

---

## 8. Tests

| Metric | Value |
|---|---|
| Baseline test count | **257** |
| Final test count | **275** |
| New tests | **18** |
| INFRA-001 tests | **17 passed**, 0 failed |
| INFRA-002 tests | **18 passed**, 0 failed |
| Full suite | **275 passed, 0 failed** |
| `cargo fmt --check` | clean |
| `cargo clippy --tests --all-targets` | clean — 0 errors, 0 warnings |
| Fixtures added | **3** |
| Fixtures migrated | **0** |
| Production files changed | **0** |

**Coverage by requirement:**

| Requirement | Tests |
|---|---|
| Replay | `br_001…replays`, `br_002…replays`, `br_003…round_trip`, `replay_reports_success_fields`, `replay_reports_failure_fields` |
| **Mutation / negative** | `mutation_changes_bytes_and_digest` (UTF-8), `mutation_detected_on_non_utf8_fixture` (raw bytes) |
| **Cross-representation** | `cross_representation_same_semantics_differ_in_bytes`, `cross_representation_distinct_semantic_identities` |
| Comparison | 5 tests (§6) |
| Status model | `no_fixture_is_labelled_normative`, `status_strings_round_trip` |
| INFRA-001 preservation | `infra_001_fixtures_remain_in_their_own_schema`, `infra_001_and_infra_002_observe_identical_entry_bytes` |

**The cross-representation test** asserts that BR-001 and BR-002 share a
`construction_id`, differ in `representation_id`, differ in raw bytes, differ in digest,
and that the difference has a located offset. That is the conflation this framework exists
to prevent: *same semantic object ≠ same bytes*.

**The mutation tests** are **framework integrity checks only — not security proofs**, and
make no claim about SHA-256. Both a UTF-8 and a non-UTF-8 preimage are covered, so
detection is proven in both encoding regimes.

---

## 9. Production impact

**None.**

- `git diff --stat` over tracked files: **empty**.
- `git status` shows only three new untracked paths.
- Nothing under `src/` was read for modification or touched.
- **No test seam was added to production.** As in INFRA-001, the entry-chain preimage is
  reconstructed in the test and proven faithful against `chain::compute_chain_hash`; if
  the production field set, order, separator or encoding changes, that assertion fails.
- No point in this task required a production change, so the STOP-and-report path was not
  triggered.

---

## 10. Unknown properties

| Fixture | Property | Value | Why |
|---|---|---|---|
| BR-003 | `encoding` | `UNKNOWN` | Nothing establishes it for a synthetic opaque byte string |
| BR-003 | `field_order` | `UNKNOWN` | The object has no established field structure |
| BR-003 | `separator` | `UNKNOWN` | No separator is established |

`br_003_unknown_properties_round_trip` asserts all three survive the round trip as
`Property::Unknown` and serialise as `"UNKNOWN"`. **No property was inferred anywhere in
this task.**

BR-003's bytes (`00 ff 10 80 7f`) are deliberately **not valid UTF-8**, so the fixture
also proves the framework does not depend on text decoding.

---

## 11. Files changed

`AuraIDToken/aura-guard-v1.3` @ `d704285` — 5 files, 992 insertions, **all new**:

| File | Lines |
|---|---|
| `tests/byte_representations.rs` | 566 |
| `tests/support/mod.rs` | 381 |
| `tests/fixtures/byte_representations/BR-001_entry_chain_observed_rust.json` | 15 |
| `tests/fixtures/byte_representations/BR-002_entry_chain_synthetic_timestamp_z.json` | 15 |
| `tests/fixtures/byte_representations/BR-003_demo_object_unknown_properties.json` | 15 |

This repository: this artifact only.

---

## 12. Terminology compliance

**Verified mechanically.** `canonical_bytes`, `canonical_preimage`, `normative_bytes`,
`protocol_canonical` and `APS_canonical` return **zero matches** across
`tests/support/`, `tests/byte_representations.rs` and the new fixtures.

Every occurrence of the word "canonical" in the new files is a **negation or a DQ-006
reference** — e.g. "does not establish canonical serialization", "Not canonical; DQ-006
unresolved" — and the disclaimer is emitted into every fixture file's `governance` field,
so the boundary travels with the data rather than living only in this document.

Terminology used: `observed_bytes`, `byte_representation`, `fixture`, `replay`,
`comparison`, `AS_IS_OBSERVED`, `PROPOSED`.

---

## 13. Final status

```
INFRA-002              = COMPLETE
DQ-002                 = UNCHANGED / CONFLICT
DQ-006                 = UNCHANGED / CONFLICT
Architecture Decision  = NOT MADE
```

**Also unchanged:** DQ-001 (direction B; CONFLICT / OPEN; no implementation
authorization; ADR not approved, per
`review/2026-08-15_D3-S5_DQ-001_CANONICAL_STATUS/`), DQ-003…DQ-005, DQ-007, DQ-008,
INFRA-001, and all registered conflicts. No PR. No merge to `main`.
