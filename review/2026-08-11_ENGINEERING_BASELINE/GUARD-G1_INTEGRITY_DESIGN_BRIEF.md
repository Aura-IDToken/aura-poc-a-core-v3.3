# GUARD-G1 — ENGINEERING DESIGN BRIEF
## `violations` outside the chain digest and outside the Merkle leaves

**Date:** 2026-08-11
**Subject:** `AuraIDToken/aura-guard-v1.3` @ `443f72e58483c3ea6112ea517647cc0dbf459960`
**Mode:** READ-ONLY. **No code was modified. No design was selected. No PR was created.**
**Finding origin:** `06_GUARD_AUDIT.md` §5 G-1 · `08_BLOCKERS.md` P0-6

### Labelling convention used throughout

| Label | Meaning |
|---|---|
| **FACT** | Verifiable from source at a cited `file:line`, or reproduced by an executed command in this session |
| **OBSERVATION** | A consequence or discrepancy derived from FACTs, stated without normative claim |
| **DESIGN QUESTION** | An engineering question with more than one defensible answer; **not answered here** |
| **DECISION REQUIRED** | A choice that must be made by an authorized decision-maker before implementation |

No requirement is inferred from implementation behaviour. Where the implementation and its
own documentation disagree, both are cited and the disagreement is the finding.

---

## 1. Scope

**In scope:** the factual state of integrity coverage for the `violations` field of
`AuditEntry` in `aura-guard-v1.3`, and the design surface that must be settled before any
implementation decision.

**Out of scope, explicitly:**

- `aura-specification` — not read for this brief, not modified
- `APS-001`, `APS-100`, `APS-200`, `SPEC-002` — untouched
- governance documents, DR-002, NB-021 — untouched, unresolved
- `aura-poc-a-core-v3.3` implementation — untouched
- Core defects (`zip()`, division, rounding, ARI, drift) — untouched
- Constitution Vector, `constitution.json`, CR-007 — not generated, not implemented

**Why this work is available at all:** `06_GUARD_AUDIT.md` §9 records that
`aura-guard-v1.3` contains zero occurrences of `constitution`, `ari`, or `poca`, and
`SAFE_ENGINEERING_WORK.md` §1.3 records that the repository contains zero occurrences of
`frozen`/`freeze`. G-1 is therefore not gated by DR-002 or NB-021. It is gated by a
**product decision about the audit-log format**, which is a different decision entirely.

---

## 2. Evidence Sources

All citations are to the pinned commit above.

| Ref | Path | What it establishes |
|---|---|---|
| E1 | `src/models.rs:30–42` | `Violation` struct definition |
| E2 | `src/models.rs:44–97` | `AuditEntry` struct definition and field order |
| E3 | `src/chain.rs:1–12` | Module doc: stated chain-hash formula |
| E4 | `src/chain.rs:18–49` | `SEP`, `compute_chain_hash()` — the actual digest input |
| E5 | `src/chain.rs:51–65` | `recompute_for_entry()` — verification input |
| E6 | `src/chain.rs:71–92` | `verify_chain()` — the whole verification loop |
| E7 | `src/merkle.rs:27–34` | `leaf_hash()` — RFC 6962 `0x00` prefix |
| E8 | `src/segment.rs:135–148` | `entry_leaf_hash()` — what becomes a Merkle leaf |
| E9 | `src/segment.rs:150–157` | `segment_merkle_root()` |
| E10 | `src/segment.rs:89–132` | `segment_chain_preimage()`, `recompute_segment_chain_hash()`, `tsa_message_imprint()` |
| E11 | `src/api/audit.rs:110–146` | Entry construction; where `violations` is populated |
| E12 | `src/log_writer.rs:88–105` | `append()` — serialization to JSONL |
| E13 | `src/bin/aura_replay.rs:1–120` | What the replay CLI actually verifies |
| E14 | `src/segment.rs:44` | `SEGMENT_SCHEMA = "aura-guard.segment.v1"` |
| E15 | `src/api/audit.rs:132` | `schema: "aura-guard.audit.v1"` |
| E16 | `README.md:24`, `:97`, `:265`; `docs/REPLAY_DEMO.md:50`; `docs/ARCHITECTURE.md:91–96` | Documented tamper-detection claims |
| E17 | Executed reproduction, this session | §7 |
| E18 | `src/chain.rs:112`, `src/segment.rs:432`, `src/sealer.rs:407`; `tests/golden.rs:21` | Test fixtures' treatment of `violations` |

---

## 3. Current Record Structure

**FACT (E2).** `AuditEntry` declares fourteen fields, in this declaration order:

| # | Field | Type | Notes |
|---|---|---|---|
| 1 | `schema` | `String` | `"aura-guard.audit.v1"` (E15) |
| 2 | `seq` | `u64` | monotonic, 0-based |
| 3 | `audit_id` | `String` | UUIDv4, server-generated |
| 4 | `request_id` | `Option<String>` | `#[serde(default, skip_serializing_if = "Option::is_none")]` |
| 5 | `timestamp` | `String` | RFC 3339 UTC |
| 6 | `decision` | `String` | `DENY` / `REVIEW` / `ALLOW` |
| 7 | `policy_set` | `String` | |
| 8 | `policy_hash` | `String` | SHA-256 of policy YAML bytes |
| 9 | `context` | `String` | verbatim echo |
| 10 | `input_hash` | `String` | SHA-256 of `context + prompt + response` |
| 11 | `shadow_hash` | `String` | SHA-256 of normalized input |
| 12 | **`violations`** | **`Vec<Violation>`** | **subject of this brief** |
| 13 | `prev_hash` | `String` | |
| 14 | `chain_hash` | `String` | |

**FACT (E1).** `Violation` declares four fields:

```rust
pub struct Violation {
    pub rule: String,        // rule identifier from the policy YAML
    pub action: String,      // "deny" | "review" | "allow"
    pub confidence: f32,     // 0.0–1.0
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub validator: Option<String>,
}
```

**FACT (E12).** The on-disk record is produced by
`serde_json::to_string(entry)` (`src/log_writer.rs:96`) written as one line
(`src/log_writer.rs:104`). Serialization is serde's derived implementation; there is no
canonicalization step, no field-order normalization, and no separate on-disk schema.

**FACT (E11).** `violations` is written into the entry at `src/api/audit.rs:143`
(`violations: violations.clone()`), i.e. the same values returned by the decision engine
are both returned to the caller and persisted.

---

## 4. Current Chain-Hash Input

**FACT (E4).** `compute_chain_hash()` (`src/chain.rs:25–49`) takes exactly **nine**
arguments and joins them with `SEP = "|"` (`src/chain.rs:20`) before hashing:

```rust
let canonical = [
    prev_hash, decision, policy_set, policy_hash,
    context, input_hash, shadow_hash,
    &seq.to_string(), timestamp,
].join(SEP);
sha256_hex(&canonical)
```

**FACT.** `violations` is **not** among the nine arguments. `compute_chain_hash()` does not
accept an `AuditEntry` and has no access to the field.

**FACT (E5).** `recompute_for_entry()` (`src/chain.rs:53–65`) reads exactly the same nine
fields from the entry. It does not read `violations`.

**FACT (E6).** `verify_chain()` (`src/chain.rs:71–92`) performs exactly two checks per
entry: `entry.prev_hash == expected_prev`, and
`recompute_for_entry(entry) == entry.chain_hash`. No other field is examined.

**OBSERVATION.** Chain coverage is therefore closed at nine fields. Five of the fourteen
`AuditEntry` fields are outside it: `schema`, `audit_id`, `request_id`, `violations`, and
`chain_hash` itself. Of those five, four are metadata or self-referential; `violations` is
the only one carrying substantive decision content.

**OBSERVATION — documentation discrepancy.** `src/models.rs:95` documents the digest as:

> ``` `SHA-256(prev_hash || decision || policy_set || input_hash || shadow_hash || seq || timestamp)` ```

This omits `policy_hash` and `context`, which the implementation does include
(`src/chain.rs:40–41`). The module doc at `src/chain.rs:6–8` and
`docs/ARCHITECTURE.md:94–95` both list all nine correctly. `src/models.rs:95` is stale.
This is a separate, smaller defect noted for completeness; it is not G-1.

---

## 5. Current Merkle-Leaf Input

**FACT (E8).** `entry_leaf_hash()` (`src/segment.rs:140–148`) constructs a leaf from a
single field:

```rust
let raw = hex::decode(&entry.chain_hash)?;
Ok(leaf_hash(&raw))
```

**FACT (E7).** `leaf_hash()` (`src/merkle.rs:29–34`) is RFC 6962: `SHA-256(0x00 || data)`.

**FACT (E9).** `segment_merkle_root()` (`src/segment.rs:151–157`) builds the root from
`entry_leaf_hash()` over each entry, and nothing else.

**FACT (E10).** `segment_chain_preimage()` (`src/segment.rs:91–106`) joins five values —
`prev_segment_chain_hash`, `merkle_root`, `first_seq`, `last_seq`, `sealed_at` — with `"|"`.
`tsa_message_imprint()` (`src/segment.rs:123–132`) hashes that same preimage.

**OBSERVATION — the coverage is transitive and therefore inherits the gap.** The full
chain of custody is:

```
violations ──✗── (absent)
                     chain_hash = SHA-256(9 fields)          [chain.rs:36-48]
                          │
                          ├─ hex::decode ──► leaf_hash(0x00‖raw)  [segment.rs:141-147]
                          │                       │
                          │                       └─► merkle_root  [segment.rs:151-157]
                          │                                 │
                          │                                 └─► segment_chain_preimage
                          │                                       [segment.rs:91-106]
                          │                                          │
                          │                                          ├─► segment_chain_hash
                          │                                          └─► tsa_message_imprint
                          │                                                (RFC 3161 anchor)
                          └─► prev_hash of entry N+1        [chain.rs:89]
```

Every downstream integrity mechanism — the entry chain, the Merkle root, the segment
chain, and the RFC 3161 timestamp anchor — derives from `chain_hash`. Because `violations`
is absent from `chain_hash`, it is absent from **all four**. Adding a fifth mechanism
downstream would not close the gap; the gap is at the root.

---

## 6. Current Location and Treatment of `violations`

**FACT.** `violations` is:

| Aspect | State | Citation |
|---|---|---|
| Produced by | `engine::evaluate()` returning `(String, Vec<Violation>)` | `src/engine.rs:14`, `:67` |
| Stored in the entry | yes | `src/api/audit.rs:143` |
| Returned to the HTTP caller | yes — the handler returns `Json<AuditEntry>` | `src/api/audit.rs:44` |
| Written to `logs/audit.jsonl` | yes, via `serde_json::to_string` | `src/log_writer.rs:96` |
| Covered by `chain_hash` | **no** | §4 |
| Covered by Merkle leaves | **no** | §5 |
| Covered by segment chain | **no** | §5 |
| Covered by RFC 3161 imprint | **no** | §5 |
| Checked by `verify_chain()` | **no** | `src/chain.rs:71–92` |
| Checked by `aura-replay` | **no** — the CLI calls `verify_chain`, `verify_manifest_against_entries`, `verify_segment_chain`, and optional policy-lineage checks; none reads `violations` | `src/bin/aura_replay.rs:31–34`, `:113` |
| Asserted by any test | **no** | see below |

**FACT (E18).** Every fixture in the integrity test suites constructs entries with an
**empty** violations vector: `src/chain.rs:112`, `src/segment.rs:432`, `src/sealer.rs:407`
all use `violations: vec![]`. `tests/golden.rs:21` discards the field entirely
(`let (decision, _) = evaluate(...)`). `tests/integration.rs` asserts on `chain_hash`
length and `prev_hash` linkage (`:122`, `:208–209`) but never on `violations`.

**OBSERVATION.** There is no test in the repository that would fail if `violations` were
altered in a persisted log line — because no test exercises a non-empty `violations` vector
through the chain or segment path at all.

---

## 7. Reproducible Integrity-Failure Scenario

**FACT — reproduced in this session.** The preimage construction of §4 was reproduced
independently (`join("|")` of the nine fields, then SHA-256 hex) and applied to a
synthetic entry carrying one violation. Results:

| Mutation applied to the persisted record | `recompute_for_entry` == stored `chain_hash`? | Merkle leaf input changed? |
|---|:--:|:--:|
| `violations` emptied (`[]`) | **TRUE** — verifies | no |
| `rule`, `action`, `confidence` rewritten (`cc-luhn`/`deny`/`0.99` → `benign-match`/`allow`/`0.01`) | **TRUE** — verifies | no |
| Fabricated violation appended | **TRUE** — verifies | no |
| **CONTROL:** `decision` changed `DENY` → `ALLOW` | **FALSE** — chain breaks | yes |

The control case confirms the reproduction is faithful: a mutation to a covered field does
break the chain, exactly as documented.

**OBSERVATION.** An operator with write access to `logs/audit.jsonl` can, for any entry:

1. delete the record of which rules matched;
2. rewrite rule identifiers, actions, confidence values and validator outcomes;
3. insert violations that never occurred;

…and `aura-replay` will report `CHAIN OK` with exit code `0`. The segment manifests will
verify. If an RFC 3161 token was obtained, it will still validate, because the timestamped
imprint derives from the Merkle root, which derives from `chain_hash`.

**OBSERVATION — bound on the exposure.** The mutation cannot change the `decision` field,
`policy_hash`, `input_hash`, `shadow_hash`, `context`, `seq`, `timestamp`, or ordering —
all nine are covered. So a tampered record can be made *internally inconsistent* (e.g.
`decision: "DENY"` with `violations: []`), and that inconsistency is detectable by a
reader who reasons about it. It is **not** detected by any automated verification the
product ships.

**OBSERVATION — this is a pre-existing property, not a regression.** No commit introduced
it; the field has been outside the digest since the digest was defined.

---

## 8. Security / Audit Consequence

**OBSERVATION.** `violations` is the field that carries the substance of a compliance
finding: *which rule fired, what action it declared, at what confidence, and whether a
semantic validator (Luhn / PESEL / IBAN) confirmed the match*. The `decision` field records
only the aggregate outcome (`src/engine.rs:59–66`: `DENY` if any deny-rule matched, else
`REVIEW`, else `ALLOW`).

**OBSERVATION.** Consequently, for an entry whose `decision` is `ALLOW`, the covered fields
carry no information about what was inspected; and for an entry whose `decision` is `DENY`,
the covered fields record *that* something was denied but not *what*. The evidentiary
detail lives entirely in the uncovered field.

**OBSERVATION — documented claims that do not hold for this field.**

| Source | Quote | Holds for the 9 covered fields | Holds for `violations` |
|---|---|:--:|:--:|
| `README.md:24` | "any byte-level mutation is detected by `aura-replay` (exit code `2`)" | yes | **no** |
| `README.md:265` | "`aura-replay` will detect any byte-level mutation" | yes | **no** |
| `README.md:97` (threat model row) | "Operator silently edits the audit log → SHA-256 hash chain → `CHAIN BREAK` at exit code `2`" | yes | **no** |
| `docs/REPLAY_DEMO.md:50` | "This proves that **any** mutation — even a one-letter flip — breaks the cryptographic chain." | yes | **no** |

The word "any" in all four places is broader than the implementation. This is recorded as a
**documentation accuracy** finding; correcting the text is a documentation change and does
not require the integrity design decision.

**OBSERVATION — threat-model position.** The mitigation is presently *procedural, not
cryptographic*: the audit log is append-only by convention and file permissions, and the
chain protects sequence and decision integrity. Nothing cryptographically binds the
violation detail to the entry it belongs to.

**Not asserted here:** whether this constitutes non-conformance with any regulatory or
protocol requirement. No such requirement was read for this brief, and none is inferred.

---

## 9. Interaction with `f32` Evidence Fields

**FACT (E1).** `Violation.confidence` is `f32` (`src/models.rs:38`).

**FACT.** It is the only floating-point value in the persisted record. (`f64` appears once
more at `src/api/audit.rs:191` for latency metrics, which are not persisted to the log.)

**OBSERVATION — currently inert.** Because `violations` is outside every digest (§5), the
`f32` value cannot presently cause a hash divergence. It is serialized, transmitted, and
stored, but never hashed.

**OBSERVATION — it stops being inert the moment G-1 is addressed.** Any design that brings
`violations` inside a digest brings `f32` inside that digest, and the following become live
concerns:

1. **Text formatting.** `serde_json` formats floats via shortest-round-trip (ryu). The
   output is stable for a given Rust toolchain, but "stable in practice" is not the same
   property as "specified", and an independent verifier in another language must reproduce
   the same characters to reproduce the hash.
2. **Value provenance.** `confidence` originates in the policy YAML (`src/policy.rs:41`,
   `:94` — `pub score: f32`) and is parsed by `serde_yaml`. The parsed `f32` is what is
   recorded. A YAML literal such as `0.7` is not exactly representable in binary32.
3. **Width.** `f32` carries ~7 decimal digits. A verifier that parsed the same YAML into
   `f64` would obtain a different value and therefore a different digest.
4. **Special values.** No constraint in the code prevents `NaN` or infinity from reaching
   the field; JSON cannot represent either, so serialization behaviour would need to be
   established rather than assumed.

**DESIGN QUESTION.** Should `confidence` participate in the integrity digest at all, or
should the digest cover the identifying fields (`rule`, `action`, `validator`) while
`confidence` remains outside as triage metadata?

**DESIGN QUESTION.** If `confidence` does participate, is it digested as the stored text,
as a fixed-precision decimal, as raw IEEE-754 bits, or as an integer in a defined scale?

**DECISION REQUIRED.** Both of the above. They are coupled: choosing to include the field
without settling its representation would create a cross-implementation determinism surface
where none exists today. `08_BLOCKERS.md` P1-14 already records that G-1 and the `f32`
question must be planned together, not sequentially.

---

## 10. Backward-Compatibility Implications

**FACT (E15).** Audit entries carry `schema: "aura-guard.audit.v1"` (`src/api/audit.rs:132`).
The value is a literal at the construction site; there is no schema-version constant for it.

**FACT (E14).** Segment manifests carry `SEGMENT_SCHEMA = "aura-guard.segment.v1"`
(`src/segment.rs:44`), and the sealer rejects manifests whose schema differs
(`src/sealer.rs:100`).

**FACT.** No equivalent check exists for the audit-entry schema: `read_all_entries()`
(`src/log_writer.rs:151–170`) deserializes without inspecting `schema`, and
`verify_chain()` does not read it.

**OBSERVATION.** Any change to the digest input changes every subsequent `chain_hash`, and
therefore:

- entries written before the change and after the change cannot be verified by one rule;
- a log spanning the change point contains two digest regimes;
- Merkle roots, segment chain hashes, and any RFC 3161 tokens obtained before the change
  remain valid **only** under the old rule;
- `prev_hash` linkage across the boundary is unaffected in form (it is still a 64-char hex
  string) but the two sides are computed under different definitions.

**OBSERVATION.** The repository provides one precedent for handling a format discriminator —
`SEGMENT_SCHEMA` with an equality check at `src/sealer.rs:100` — but the audit-entry path
does not currently use it.

**DESIGN QUESTION.** Does a verifier need to validate historical logs written under the
current rule after the change ships?

**DESIGN QUESTION.** If yes, is the mechanism a schema discriminator read by the verifier, a
hard cut-over at a stated sequence number, a re-sealing of historical segments, or
something else?

**DESIGN QUESTION.** Does the `/v1/audit` HTTP response shape change, and if so, is that a
breaking API change for existing callers?

**DECISION REQUIRED.** Whether the change is a versioned format migration or a hard break,
and what happens to already-anchored RFC 3161 tokens. This is the product decision referred
to in §1 — it is the gating decision, and it is not an engineering one.

---

## 11. Candidate Design Boundaries

**These are boundaries, not designs.** No option below is recommended, and the list is not
a menu to pick from — it exists to make the decision surface explicit. Per the task rules,
**no serialization format, no hash domain, and no schema is selected here.**

Each boundary is characterized by *where* the violation data would be bound, not *how*.

| # | Boundary | Where the binding sits | Digest regimes affected | Historical logs |
|---|---|---|---|---|
| **B1** | Inside the existing entry digest | `compute_chain_hash()` gains an input derived from `violations` | chain, Merkle, segment, TSA — all four, transitively | invalidated under the new rule |
| **B2** | A separate per-entry digest, itself placed inside the existing entry digest | a new field (e.g. a digest of the violations) becomes one of the `compute_chain_hash` inputs | same four, transitively | invalidated under the new rule |
| **B3** | A separate per-entry digest, carried alongside and verified independently | a new field verified by a new check in `verify_chain()` or the replay CLI | none of the four change | remain valid; new field absent on old entries |
| **B4** | A parallel Merkle tree over violation data, anchored in the segment manifest | `SegmentManifest` gains a second root; `segment_chain_preimage()` would decide whether it participates | segment and TSA if included in the preimage; chain unaffected | entry chain remains valid; manifests change |
| **B5** | No cryptographic binding; compensating controls only (file permissions, WORM storage, external shipping) | outside the codebase | none | unaffected |

**Properties that differ across boundaries** — the axes on which a decision would turn:

- **Retroactive verifiability.** B1/B2 break it; B3/B4/B5 preserve it.
- **Single-artifact verification.** B1/B2 keep one digest to check; B3/B4 introduce a second
  verification step that a naive verifier could skip.
- **Fail-closed on omission.** Under B3, an entry with the new field stripped entirely must
  be distinguishable from an old entry that legitimately lacks it — otherwise the control is
  bypassable by deletion. This is a property the design must supply; it is not automatic.
- **TSA coupling.** B1/B2/B4-if-included change `tsa_message_imprint()`
  (`src/segment.rs:123–132`), which means the anchored value changes.
- **`f32` exposure.** B1/B2/B3/B4 all bring §9 into scope. B5 does not.

**FACT — invariant across all boundaries.** Whatever is chosen, the data must be reduced to
bytes before hashing, and that reduction must be reproducible by an independent verifier.
That is the serialization/hash-domain question this brief is forbidden to answer, and it is
the reason §12 lists it as a decision rather than a design task.

---

## 12. Open Decisions

**DECISION REQUIRED — D1.** Is the current state accepted, mitigated procedurally, or
addressed cryptographically? (Selects among §11 B1–B5, or none.)

**DECISION REQUIRED — D2.** If addressed cryptographically: is retroactive verifiability of
existing logs a requirement? (Determines whether B1/B2 are admissible at all.)

**DECISION REQUIRED — D3.** What byte reduction of violation data is authoritative?
*Explicitly not answered in this brief.* Sub-questions that must be settled together:
field set, field order, encoding of `Option::None` for `validator`, encoding of the empty
vector, and separator/escaping rules such that no two distinct violation lists can produce
the same bytes.

**DECISION REQUIRED — D4.** Does `confidence` participate, and in what representation?
(§9. Coupled to D3.)

**DECISION REQUIRED — D5.** Which hash domain does the reduction belong to — the existing
entry digest, or a distinct domain with its own prefix? *Explicitly not answered.*
Note as context only, not as a recommendation: `src/merkle.rs:9–15` already documents
domain separation via `0x00`/`0x01` prefixes for leaf vs node, so the codebase has a
precedent for the concept but no established convention for a third domain.

**DECISION REQUIRED — D6.** Migration mechanism and schema-discriminator policy for
`"aura-guard.audit.v1"`. (§10.)

**DECISION REQUIRED — D7.** Disposition of RFC 3161 tokens already obtained under the
current rule. (§10.)

**DECISION REQUIRED — D8.** Whether the `/v1/audit` response shape changes, and the
notification path for existing integrators.

**DESIGN QUESTION — Q1.** Should `schema`, `audit_id`, and `request_id` — the other three
uncovered fields (§4) — be reconsidered at the same time, or is that a separate change?
Widening scope has a cost; keeping it narrow means touching the digest twice.

**DESIGN QUESTION — Q2.** Should `verify_chain()` (`src/chain.rs:71–92`) gain an internal
consistency check — e.g. that a `DENY` decision is accompanied by at least one deny-action
violation — independent of any digest change? This would detect the §7 mutations without
altering any hash. It is a different control with different properties, not a substitute.

**DESIGN QUESTION — Q3.** Is the stale formula comment at `src/models.rs:95` (§4) corrected
now as documentation, or as part of whatever change lands?

---

## 13. Tests That Would Be Required AFTER Authorization

**Listed, not written.** No test file was created or modified. This section exists so that
the decision-maker can see the verification cost attached to each boundary.

### 13.1 Available before any decision — characterization only

These record the present state and assert nothing about correctness. They are permitted
under `SAFE_ENGINEERING_WORK.md` §1.1 and would not need to change if a design is later
chosen — they would simply start failing, which is the point.

| ID | Test | Records |
|---|---|---|
| T-0a | Persist an entry with a non-empty `violations`, mutate the field in the JSONL, run `verify_chain()` | that it returns `Ok` (§7) |
| T-0b | Same, then `verify_manifest_against_entries()` | that the manifest still verifies |
| T-0c | Assert the exact nine-field preimage of `compute_chain_hash()` against a known-answer vector | pins the current digest input so any future change is visible |

**Note.** No such test exists today, and every current integrity fixture uses
`violations: vec![]` (§6). T-0a–T-0c would be the first tests to exercise a non-empty
violations vector through the integrity path at all.

### 13.2 Required only after D1–D7 are decided

| ID | Test | Applies to |
|---|---|---|
| T-1 | Each §7 mutation now fails verification with the specified exit code | B1–B4 |
| T-2 | Round-trip: serialize → deserialize → recompute → digest unchanged | B1–B4 |
| T-3 | Known-answer vectors for the chosen byte reduction, checked in as fixtures | B1–B4 |
| T-4 | Injectivity: two distinct violation lists never reduce to the same bytes — including empty-vs-absent, `None`-vs-empty-string `validator`, and separator-collision cases | B1–B4 |
| T-5 | `f32` boundary values: `0.0`, `1.0`, a value not exactly representable in binary32, and whatever the design specifies for `NaN`/infinity | D4 |
| T-6 | Cross-toolchain reproduction of the digest — at minimum the arm64 leg missing from CI today (`08_BLOCKERS.md` P1-9) | B1–B4 |
| T-7 | Migration: a log spanning the change point verifies under the specified rule; an old-format entry is either accepted or rejected per D6, never silently mis-verified | D6 |
| T-8 | Fail-closed on omission: an entry with the new field stripped is rejected, not treated as legacy | B3, B4 |
| T-9 | Segment/TSA regression: `segment_chain_hash` and `tsa_message_imprint` behave as specified across the change | B1, B2, B4-if-included |
| T-10 | Property test over arbitrary violation vectors, in the style of the five existing `proptest!` suites (`src/chain.rs:426`, `src/engine.rs:305`, `src/normalizer.rs:445`, `src/validators.rs:374`, `src/crypto.rs:248`) | B1–B4 |
| T-11 | Golden fixtures updated to carry non-empty violations (`tests/golden.rs:21` currently discards them) | all |

---

## 14. Explicit Non-Goals

This brief did **not**:

- select a serialization format, a byte reduction, or a canonicalization rule;
- select a hash domain or a domain-separation prefix;
- select or propose a new schema, schema version, or migration path;
- choose among boundaries B1–B5, or recommend one;
- modify any source file, test, fixture, workflow, or documentation in `aura-guard-v1.3`;
- modify `aura-poc-a-core-v3.3` implementation, or any Core defect (`zip()`, division,
  rounding, ARI, drift);
- modify `aura-specification`, `APS-001`, `APS-100`, `APS-200`, `SPEC-002`, or any
  governance document;
- resolve DR-002 or NB-021, or rely on either being resolved;
- generate a Constitution Vector, create `constitution.json`, or implement CR-007;
- create or modify a normative decision, or infer a normative requirement from
  implementation behaviour;
- assert that the current state violates any regulatory or protocol requirement;
- create a pull request;
- authorize any of the work in §13.

**Status:** engineering design brief only. Implementation requires D1–D7 to be decided by an
authorized decision-maker, plus the audit-log format decision identified in §1 and §10.

---

*This document has no normative effect. It records the factual state and the decision
surface. It selects nothing and implements nothing.*
