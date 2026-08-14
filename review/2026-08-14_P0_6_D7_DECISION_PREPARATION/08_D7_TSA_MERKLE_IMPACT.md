# 08 — D-7 Impact on Merkle and RFC 3161 / TSA Evidence

Analysis only. No candidate selected; no migration proposed.

---

## 1. The derivation chain — CONFIRMED from source

All at `aura-guard-v1.3` @ `443f72e`.

| Step | Function | Consumes | Cite |
|---|---|---|---|
| 1 | `compute_chain_hash` | nine field values | `src/chain.rs:25–49` |
| 2 | `entry_leaf_hash` | `hex::decode(entry.chain_hash)` → `leaf_hash(raw)` — that field alone | `src/segment.rs:140–150` |
| 3 | `leaf_hash` | `SHA-256(0x00 ‖ data)`, RFC 6962 | `src/merkle.rs:29–34` |
| 4 | `segment_merkle_root` | leaf hashes only | `src/segment.rs:151–158` |
| 5 | `segment_chain_preimage` | `prev_segment_chain_hash ‖ merkle_root ‖ first_seq ‖ last_seq ‖ sealed_at` | `src/segment.rs:91–106` |
| 6 | `recompute_segment_chain_hash` | `SHA-256(preimage)` | `src/segment.rs:109–121` |
| 7 | `tsa_message_imprint` | `SHA-256(same preimage)` | `src/segment.rs:123–131` |

**Consequence for D-7.** Generation propagates implicitly: the rule used to
compute an entry's `chain_hash` determines its leaf, hence the root, hence the
segment hash and the TSA imprint. Nothing downstream carries a generation marker
of its own — **CONFIRMED**, steps 2–7 read no version field.

## 2. Merkle continuity

**CONFIRMED.** `verify_manifest_against_entries` **recomputes** the root from the
entries (`src/segment.rs:394`) and compares the last entry's `chain_hash` to
`head_chain_hash_at_close` (`:401`). It does not trust the stored root.

**Consequences by scenario:**

| Scenario | Outcome |
|---|---|
| Segment entirely of generation 1, verified under rule 1 | Root reproduces; manifest verifies — CONFIRMED behaviour today |
| Segment entirely of generation 1, verified under rule 2 | Every entry's recomputed `chain_hash` differs → every leaf differs → root mismatch → exit `5` (`docs/exit-codes.md`) — **INFERENCE** from steps 1–4 |
| Segment entirely of generation 2, verified under rule 2 | Reproduces, provided the verifier applies rule 2 |
| **Segment spanning a generation boundary** | **No single rule reproduces the root.** A verifier must apply the correct rule *per entry* within one segment — **INFERENCE**, and the structurally hardest case in D-7 (D7-Q-020) |

**Implication for candidate granularity.** Candidates that determine generation
**per entry** (A, B, D, E, G-structural) can in principle handle a
boundary-spanning segment. Candidates that determine it **per invocation or per
artifact** (C, F, G-`seq`-boundary) cannot, unless the boundary is constrained to
fall on a segment edge. **Whether the boundary may fall inside a segment is a
D-5 question**, not decided here.

**CONFIRMED — a second check exists and can disagree with the first.**
`verify_segment_chain` (`src/segment.rs:335–342`) validates manifest-to-manifest
linkage only, and is unaffected by the entry rule. So a manifest chain can verify
(exit path clean) while `verify_manifest_against_entries` fails (exit `5`) for
the same corpus. The two checks answer different questions.

## 3. RFC 3161 / TSA evidence

### 3.1 What exists — CONFIRMED

| Artifact | Evidence |
|---|---|
| Two real tokens | `tests/fixtures/tsa/segment-001.tsr`, `segment-002.tsr` |
| Trust anchors | `tests/fixtures/tsa/freetsa-cacert.pem` |
| Provenance | Round-tripped against FreeTSA per `tests/tst_verify.rs:3–9` (quotation: "The TSR + root fixtures are real") |
| Imprint derivation in test | `SegmentManifest::segment_chain_preimage(...)` then `Sha256::digest` — the identical preimage `tsa_message_imprint()` computes | `tests/tst_verify.rs:25–33` |
| Strict verifier | `verify_tsr` | `src/tst_verify.rs:393` |
| Manifests attested | `segment-001.manifest.json` carries a concrete `merkle_root` and `head_chain_hash_at_close`, sealed `2026-05-20T20:22:47.560539282+00:00` | fixture file |

**These tokens attest imprints that descend from v1-rule `chain_hash` values.**
TSA continuity is therefore a present concern, not a hypothetical one.

**Note on linkage.** Both fixture manifests carry `"tst_path": null` while their
`.tsr` files sit alongside; the association is by filename convention in
`tests/tst_verify.rs:20–22`, not by the manifest field — **IMPLEMENTATION-DERIVED**.
Relevant only to a migration that touches manifests.

### 3.2 The asymmetry that matters

**CONFIRMED.** An RFC 3161 token attests a specific imprint at a specific past
instant. If the imprint changes, the token cannot be re-issued for that instant —
a new token would attest the new time, not the original one. Timestamp evidence
is therefore **not reconstructible**, unlike digests, which are re-derivable from
retained data (`src/log_writer.rs:96`).

### 3.3 Per-candidate disposition — D7-Q-022

| Candidate | Effect on existing tokens |
|---|---|
| A discriminator outside digest | **Preserved** — sealed history untouched |
| B discriminator inside digest | **Preserved**, provided legacy entries keep verifying under the legacy rule |
| C external selection | **Preserved** |
| D self-describing digest | **Preserved** |
| E dual / parallel | **Preserved** |
| F verifier families | **Preserved** |
| G structural / genesis | **Preserved**. One caveat: the genesis constant's doc-comment states it "must never be changed without bumping the protocol version" (quotation, `src/crypto.rs:25`) — a genesis change would re-root every chain and invalidate every downstream root and token. **Whether a digest-domain change implies a genesis change is EG-6, unresolved** |

**CONFIRMED — the key separation.** **No D-7 candidate endangers existing TSA
tokens.** Token destruction arises only from re-computing `merkle_root`, i.e.
from a **re-sealing migration**, which is a **D-5** strategy (D-5-C in the
D-2/D-5 package). D-7 chooses how a rule is selected; D-5 chooses what happens to
old records.

### 3.4 Evidence still required

- **G-4** — whether production tokens exist beyond the two fixtures
  (`06_…` §2). If they do, the D-5 re-sealing option carries proportionally
  greater irreversible cost.
- **EG-6** — whether a digest-domain change constitutes a protocol-version bump
  in the sense of `src/crypto.rs:25`.

## 4. Summary

| Question | Answer | Status |
|---|---|---|
| Does generation propagate to Merkle and TSA? | Yes, implicitly through `chain_hash` | CONFIRMED |
| Does any downstream layer carry its own generation marker? | No | CONFIRMED |
| Can a boundary-spanning segment verify under one rule? | No | INFERENCE |
| Does any D-7 candidate rewrite sealed history? | No | CONFIRMED |
| Does any D-7 candidate destroy existing tokens? | No | CONFIRMED |
| Which decision could destroy them? | D-5, if a re-sealing strategy is chosen | CONFIRMED (scope statement) |
| Is per-entry generation determination required? | Only if a boundary may fall inside a segment — a D-5 question | DEPENDENT |
