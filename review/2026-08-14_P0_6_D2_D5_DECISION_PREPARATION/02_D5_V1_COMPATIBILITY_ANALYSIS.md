# 02 — D-5: Existing v1 Log Compatibility Analysis

**Decision:** D-5 — *How are existing v1 logs handled after a chain-hash change?*
**Status:** OPEN. Nothing decided. No log read, modified or migrated by this analysis.

Classification legend: see `00_SCOPE_AND_DECISION_CONTEXT.md` §4.

---

## 1. Serialization baseline

| # | Question | Finding | Cite | Tag |
|---|---|---|---|---|
| 1.1 | How is `AuditEntry` serialized? | `serde_json::to_string(entry)`, written as one line with `writeln!` | `src/log_writer.rs:96`, `:104` | CONFIRMED |
| 1.2 | Is there a canonicalization step? | No. Serde's derived implementation; no field-order normalization, no separate on-disk schema | `src/log_writer.rs:88–105` | CONFIRMED |
| 1.3 | Is the entry written verbatim, including `violations`? | Yes — the whole struct, `violations` included | `src/log_writer.rs:96`; `src/models.rs:90` | CONFIRMED |
| 1.4 | Which fields disappear when empty? | `request_id` and `violation.validator` are omitted entirely when `None` (`skip_serializing_if`) | `src/models.rs:65`, `:40` | CONFIRMED |
| 1.5 | Write failure behaviour | Fail-closed: the log halts and the API returns 503 | `src/log_writer.rs:89–94`; `src/api/audit.rs:149` | CONFIRMED |

## 2. Digest baseline

| # | Question | Finding | Cite | Tag |
|---|---|---|---|---|
| 2.1 | How is `chain_hash` calculated? | `SHA-256` over nine values joined by `SEP = "\|"` | `src/chain.rs:20`, `:25–49` | CONFIRMED |
| 2.2 | When is it computed? | Before the `AuditEntry` is constructed and before persistence | `src/api/audit.rs:119`, `:131`, `:149` | CONFIRMED |
| 2.3 | Genesis | `prev_hash` for entry 0 is `sha256_hex("AURA-GUARD-GENESIS-v1.3")`; the doc-comment states it "must never be changed without bumping the protocol version" | `src/crypto.rs:25–30` | CONFIRMED |
| 2.4 | Is the field set specified anywhere? | No. `docs/adrs/0001-hash-chain.md` (Accepted, still current) says "canonical fields incl. `prev_hash`" without enumerating them | `docs/adrs/0001-hash-chain.md` | CONFIRMED / EVIDENCE GAP |

## 3. Version discriminator baseline

| # | Question | Finding | Cite | Tag |
|---|---|---|---|---|
| 3.1 | Is `schema` stored? | Yes — `"aura-guard.audit.v1"`, an inline literal at the construction site; no named constant | `src/api/audit.rs:132` | CONFIRMED |
| 3.2 | Is `schema` verified? | **No.** `read_all_entries` deserializes without inspecting it; `verify_chain` never reads it; the only other `src/` occurrence is a test fixture | `src/log_writer.rs:151–170`; `src/chain.rs:71–92`, `:101` | CONFIRMED |
| 3.3 | Does audit-entry versioning exist? | No mechanism — no constant, no check, no branch on version anywhere in the audit path | as 3.1–3.2 | CONFIRMED |
| 3.4 | Does a precedent exist elsewhere? | Yes, on the **segment** path only: `SEGMENT_SCHEMA = "aura-guard.segment.v1"`, rejected on mismatch in two places | `src/segment.rs:44`, `:341–342`; `src/sealer.rs:100` | CONFIRMED |
| 3.5 | Can an old entry be distinguished from a future entry? | Only by reading the `schema` string, which is (a) not checked by any code and (b) not covered by the digest, so it is rewritable without breaking verification | `src/chain.rs:25–49`; `src/log_writer.rs:151–170` | CONFIRMED |
| 3.6 | Is there an in-band discriminator a verifier can trust? | **No.** A `schema` value exists in-band but carries no integrity protection and drives no code path | as 3.5 | CONFIRMED |
| 3.7 | Can a verifier determine which integrity rule produced a given entry? | **No.** Nothing in the record, and nothing in the verifier, selects a rule. Verification applies one hard-coded rule to every entry | `src/chain.rs:53–65` | CONFIRMED |

## 4. Verification and replay baseline

| # | Component | Behaviour | Cite | Tag |
|---|---|---|---|---|
| 4.1 | `read_all_entries` | Reads the file, skips blank lines, `serde_json::from_str` per line into `AuditEntry`, errors with the line number on malformed JSON. No schema inspection, no version branch | `src/log_writer.rs:151–170` | CONFIRMED |
| 4.2 | `verify_chain` | Two checks per entry: `prev_hash == expected_prev`, and `recompute_for_entry(entry) == entry.chain_hash`. Returns the head hash on success | `src/chain.rs:71–92` | CONFIRMED |
| 4.3 | `recompute_for_entry` | Reads the same nine fields; never reads `violations` | `src/chain.rs:53–65` | CONFIRMED |
| 4.4 | `aura-replay` | Always `verify_chain` (exit code `2` on break); optional `--verify-lineage` policy-hash comparison (exit `3`); `verify_segment_chain`; `verify_manifest_against_entries`; prints `CHAIN OK` | `src/bin/aura_replay.rs:113–119`, `:134–153`, `:175`, `:194`, `:213` | CONFIRMED |
| 4.5 | `verify_segment_chain` | Rejects a manifest whose `schema != SEGMENT_SCHEMA`; then checks `segment_id` continuity, `prev_segment_chain_hash`, `prev_merkle_root` | `src/segment.rs:335`, `:341–342` | CONFIRMED |
| 4.6 | `verify_manifest_against_entries` | Checks `entry_count`; **recomputes** the Merkle root from the entries and compares to the stored `merkle_root`; compares the last entry's `chain_hash` to `head_chain_hash_at_close` | `src/segment.rs:382–405`, esp. `:394`, `:401` | CONFIRMED |
| 4.7 | RFC 3161 verification | `verify_tsr` performs strict token verification against trust anchors | `src/tst_verify.rs:393`; `tests/tst_verify.rs` | CONFIRMED |

## 5. What happens when the digest input domain changes

**IMPLEMENTATION-DERIVED**, from §2 and §4 — stated as consequence, not as
objection:

1. **Every existing entry** fails `recompute_for_entry` under a new rule
   (`chain.rs:53–65`), because the stored `chain_hash` was produced by the old
   preimage.
2. **Every existing segment manifest** fails `verify_manifest_against_entries`,
   because that function recomputes the Merkle root from entry `chain_hash`
   values (`segment.rs:394`) and compares `head_chain_hash_at_close`
   (`segment.rs:401`).
3. **Every existing RFC 3161 token** attests an imprint derived from a
   `merkle_root` that can no longer be reproduced under the new rule
   (`segment.rs:91–131`).
4. **The verifier has no way to know**, because no in-band discriminator is read
   (§3.6, §3.7). The failure mode is therefore *silent misattribution*: a
   legitimate old entry is indistinguishable from a tampered new one.

Point 4 is the structural core of D-5 and is what separates the strategy classes
in `03_D5_STRATEGY_MATRIX.md`.

**Scope note.** Points 1–3 hold for any change to the digest *input domain*. They
do not presuppose that D-2 will widen the entry digest — a design that adds a
sibling digest without altering `compute_chain_hash` would not trigger them. That
distinction is D-2's to make (D2-Q12), not this file's.

---

## 6. Historical data analysis — what actually exists

Six levels, kept strictly separate. **The existence of a format is not evidence
that production logs exist.**

| # | Question | Finding | Cite | Tag |
|---|---|---|---|---|
| 6.1 | Does the v1 **format** exist? | **Yes.** `AuditEntry` with `schema: "aura-guard.audit.v1"`, JSONL persistence | `src/models.rs:50–97`; `src/api/audit.rs:132` | CONFIRMED |
| 6.2 | Do **audit-log fixtures** exist in-repo? | **No `.jsonl` file exists anywhere in the repository** (`find -name "*.jsonl"` → empty). Entry fixtures are constructed in-code, and every integrity fixture uses `violations: vec![]` | `src/chain.rs:112`; `src/segment.rs:432`; `src/sealer.rs:407` | CONFIRMED |
| 6.3 | Do **segment-manifest fixtures** exist? | **Yes** — `tests/fixtures/tsa/segment-001.manifest.json` and `segment-002.manifest.json`, carrying concrete `merkle_root`, `segment_chain_hash` and `head_chain_hash_at_close` values, `sealed_at 2026-05-20T20:22:47.560539282+00:00` | fixture files | CONFIRMED |
| 6.4 | Do **real RFC 3161 tokens** exist? | **Yes** — `segment-001.tsr`, `segment-002.tsr`, round-tripped against FreeTSA, with `freetsa-cacert.pem` anchors. `tests/tst_verify.rs:25–33` recomputes the imprint via `segment_chain_preimage` + SHA-256 and `verify_tsr` validates the tokens against it | `tests/tst_verify.rs:3–9`, `:20–48` | CONFIRMED |
| 6.5 | Do **real production logs** exist? | Not determinable from the repository | — | **EVIDENCE GAP** |
| 6.6 | Are any logs **externally relied upon** (customers, auditors, regulators)? | Not determinable from the repository | — | **EVIDENCE GAP** |
| 6.7 | Do any logs carry a **legal/compliance retention** obligation? | Not determinable from the repository. No retention statement was found in the sources of truth | — | **EVIDENCE GAP** |
| 6.8 | Is migration **technically possible**? | Partially answerable. Re-deriving `chain_hash` under a new rule is mechanically possible *if* the full entry is retained — every input to a widened digest is present in the persisted JSONL (`violations` included, §1.3). **But** re-sealing changes `merkle_root`, which invalidates existing TSA tokens irrecoverably: a token attests the old imprint and cannot be re-issued for the past instant | `src/log_writer.rs:96`; `src/segment.rs:91–131` | CONFIRMED (mechanics) / **EVIDENCE GAP** (acceptability) |

### 6.9 Consequence of 6.3 + 6.4 for D-5

**IMPLEMENTATION-DERIVED.** Timestamp evidence over v1-rule chain hashes is
**already materialised in the repository**, not hypothetical. Two committed,
externally-issued tokens attest imprints that descend from v1 `chain_hash`
values. Any D-5 strategy that invalidates v1 digests therefore has a concrete,
in-repo consequence today — independent of whether production logs exist (6.5,
still a gap).

**Note.** This refines `docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md` §2.8, which
described the TSA exposure as "structural and latent". The narrower fact — that
`tsa_message_imprint()` has no in-tree caller — remains true; the tokens exist
regardless, because the test recomputes the identical preimage inline. The ADR is
not amended by this package.

**Observation on fixture linkage.** Both fixture manifests carry
`"tst_path": null` while their `.tsr` files sit beside them; the association is
by filename convention in `tests/tst_verify.rs:20–22`, not by the manifest field.
**IMPLEMENTATION-DERIVED**; noted because any migration touching manifests would
need to preserve a linkage that is currently implicit. Not a defect claim.

---

## 7. Summary of the D-5 baseline

| Property | State | Tag |
|---|---|---|
| Entries carry a version string | Yes (`aura-guard.audit.v1`) | CONFIRMED |
| Any code reads that string | **No** | CONFIRMED |
| That string is integrity-protected | **No** | CONFIRMED |
| A verifier can select a rule per entry | **No** | CONFIRMED |
| Segment path has a schema-rejection precedent | Yes | CONFIRMED |
| Entry path has any versioning precedent | **No** | CONFIRMED |
| Full entry data is retained on disk (so re-derivation is possible) | Yes | CONFIRMED |
| Existing TSA tokens exist over v1-derived imprints | Yes (in-repo fixtures) | CONFIRMED |
| Production logs exist / are relied upon / must be retained | Unknown ×3 | **EVIDENCE GAP** |
