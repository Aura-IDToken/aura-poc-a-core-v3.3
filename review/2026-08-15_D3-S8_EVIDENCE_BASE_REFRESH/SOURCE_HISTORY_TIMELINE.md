# SOURCE_HISTORY_TIMELINE — D3-S8

**Phases 9–11.** Built from `git log` / `git show` against complete histories.
**Normative effect: NONE.** Where a commit message states no intent, the entry reads
**INTENT NOT ESTABLISHED** rather than an inferred motive.

## 1. Timeline

| Date | Commit | Repo | Author | Change | Stated intent |
|---|---|---|---|---|---|
| 2026-01-04 | `cae9363` | POC-A | Aura-IDToken | Repository created | — |
| 2026-01-04 | `befddfa` | POC-A | Aura-IDToken | `merkle.py` created | — |
| 2026-01-17 | `80ec4ad` | POC-A | copilot-swe-agent[bot] | `EventTrustCertificate` + JSON `sort_keys` canonicalization | "Implement PoCA compliance features: Docker setup, Art. 5/13/14 compliance" |
| **2026-01-23** | — | POC-A | Aura Protocol Core Team | **ADR-005 "Removal of Float from Runtime Core", Status APPROVED** | Bit-for-bit reproducibility across x86/ARM/WASM; enumerates 5 IEEE-754 non-determinism sources (`ADR_005…:1-33`) |
| **2026-05-13** | **`d03eb65`** | **Guard** | aura.idtokenkontakt | Monolithic v1.3.1 import. **`AuditEntry` (11 fields)**, **`chain_hash` with the full 9-field preimage**, `prev_hash`, `input_hash`, `shadow_hash`, `policy_hash`, `genesis_hash` | "Aura-Guard v1.3.1: Bootstrap fail-closed gate + lineage verification". **"lineage" = policy-hash continuity** (`README.md:304`, `SECURITY.md:66`, `ROADMAP.md:67-68`), **not** repository lineage |
| **2026-05-13** | `d03eb65` | Guard | — | **`models.rs` doc-comment documents a 7-field preimage** (`prev_hash, decision, policy_set, input_hash, shadow_hash, seq, timestamp`) while `chain.rs` implements **9** (adds `policy_hash`, `context`) | **INTENT NOT ESTABLISHED** — no commit message, ADR or issue explains the divergence |
| 2026-05-19 | `31a60de` | Guard | Devin AI | v1.4 — RFC 6962 Merkle (`leaf_hash`, `node_hash`), `segment_chain_hash`, **`segment_genesis_hash`**, optional RFC 3161 | "Merkle batching (RFC 6962) + optional RFC 3161 timestamping". `CHANGELOG.md:64-72` records these as **layered on top of**, not replacing, the chain |
| 2026-05-20 | `1e801c3` | Guard | aura.idtokenkontakt | v1.5 — `tsa_message_imprint`, full RFC 3161/5652/5816 verifier | as titled |
| **2026-07-23** | `d2b12cd` | **Spec** | Aura-IDToken | Specification repository created | — |
| 2026-07-23 | `6f4d971`, `792c43f` | Spec | Aura-IDToken | Original APS-000…950 + Constitution uploaded as **Polish** PDF/TXT | "Add files via upload" |
| 2026-07-23 | `6ad45f3` → `aeb6bab` → `7a22522` | Spec | copilot-swe-agent[bot] / Aura-IDToken | `AuraProtocol` org migration proposed, all 6 boxes unchecked, then **removed the same day** | "Add README.md with AuraProtocol organization structure and migration status"; then "Update README to remove migration information" |
| **2026-07-23** | **`b68181e`** | **Spec** | copilot-swe-agent[bot] | **Entire canonical corpus in ONE commit**: APS-000…950 incl. **APS-200/ENT-007, `integrity_hash`, `event_payload_hash`, `previous_record_hash`, `evidence_hash`**, invariants, CONF-001…010, fixtures, **and both `RI-PY_…` and `RI-RS_…` designations** | "feat: build complete canonical repository structure for aura-specification" |
| **2026-07-24** | `ef91cb1` | POC-A | copilot-swe-agent[bot] | GAP-001 — POC-A's **first ever** APS-200/APS-100 reference | "docs: add GAP-001 Implementation Gap Report". **Uses an APS numbering incompatible with the corpus** (§3) |
| **2026-07-24** | — | POC-A | "Aura Protocol Custodian" | `AUDIT_LAYER_SPEC.md` **"Last Frozen"**, Status **NORMATIVE**, containing the **implementation-governs** clause (`:17-19`) | **INTENT NOT ESTABLISHED** relative to APS-200, created one day earlier |
| 2026-07-26 | `75f1052` | Guard | Copilot | **`request_id` added** to `AuditEntry` — the only post-spec schema change | "Log analysis for observability metrics (#23)". **No APS alignment stated** |
| 2026-07-26 | `025f092`, `51bcdd2` | Guard | Copilot / bot | Test-coverage expansion touching `chain.rs` | **No preimage change** — 9 fields identical to `d03eb65` |
| 2026-07-27 | `9dd8757` | Guard | Aura-IDToken | Doc fixes, header guards, `request_id` test constructors | as titled |
| 2026-07-27/28 | `56f7b64` → `c5e162e` | Guard | Aura-IDToken | Revert pair — net zero on `models.rs` | "Description (#47)" / "Revert…" |
| 2026-08-09 | `d2ec66f` | POC-A | Aura-IDToken | `rust-conformance.instructions.md` added (`applyTo: **/*.rs`) | "chore: add agent conformance governance". **Governs zero files** — POC-A has no `.rs` |
| 2026-08-11 | `8db25b3` | POC-A | Claude | **First ever** `RI-PY`/`RI-RS`/`aura-guard` strings in POC-A — inside a review package | audit artifact |
| 2026-08-12 | `17c3916` | POC-A | Claude | **First ever** `ENT-007` string in POC-A | audit artifact |
| **2026-08-14** | `39ecd2f` | POC-A | Claude (recording) | **P0-6 D-3/D-4 "CLOSED — DECISION DOMAIN"**, with "**concrete semantic value: NOT ESTABLISHED**" | Explicit non-decisions incl. canonical byte encoding, serialization format, ordering rule, hash-domain representation (§5) |
| 2026-08-15 | `70b9881` | Guard | Claude | `chain_preimage()` accessor extracted **verbatim**; `D3_REAL_CHAIN_CANONICAL.bin` exported; digest identical before/after | "instrumentation only". Unmerged branch |

## 2. `git log -S` results for the disputed fields

| Field | Commits touching it | First | Semantic change since first? |
|---|---|---|---|
| `AuditEntry` | 4 in guard (`d03eb65`, `75f1052`, `9dd8757`, `56f7b64`/`c5e162e`) | `d03eb65` | **NO** — remained a DTO. `6661982` records independently: "`models.rs` is a pure DTO module" |
| `schema` (guard) | `d03eb65` | 2026-05-13 | **NO** — constant `"aura-guard.audit.v1"` at `api/audit.rs:132`, echoed at `api/health.rs:43` |
| `schema_version` / `protocol_version` | **0 commits in guard, all history** | — | **never implemented** |
| `chain_hash` | 9 in guard | `d03eb65` | **NO** — preimage byte-stable |
| `prev_hash` | 7 in guard | `d03eb65` | NO |
| `violations` | `d03eb65` | 2026-05-13 | NO — never entered any hash domain |
| `confidence` | `d03eb65` | 2026-05-13 | NO — `f32` since introduction |

## 3. GAP-001 APS-numbering divergence (bears on DQ-001, DQ-002, DQ-008)

**FACT.** `docs/GAP-001.md:207-217` (POC-A, 2026-07-24) assigns:

| ID | GAP-001 | `aura-specification` | Compatible? |
|---|---|---|---|
| APS-100 | **Canonical Data Model** | **Protocol Invariants** | NO |
| APS-200 | **ARI Engine** | **Canonical Data Model** | NO |
| APS-400 | Serialization | Conformance Test Matrix | NO |
| APS-500 | ZK Layer | Reference Fixtures | NO |
| APS-900 | Conformance Runner | Compliance Mapping | NO |
| APS-950 | Compliance Reporter | Reference Implementation Requirements | NO |

**FACT.** `GAP-001:202` states its own basis: requirements were "**inferred** from the
repository's own documentation, the custom directive, and ADR-005, **as the external
`aura-specification` repository is not co-located here**" — while `:5` cites
"Specification Reference: aura-specification / spec-v0.1.0".

**INFERENCE.** The only pre-audit cross-reference from POC-A to APS-200 does not refer to
the APS-200 that exists. Any claim resting on GAP-001's APS citations is invalid,
including its `:417` "APS-200 … Adapter" item, which concerns embedding→int32 conversion.

## 4. Cross-repository lineage — five categories held separate (Phase 11)

| Category | Finding | Evidence |
|---|---|---|
| **A. Repository lineage** | **NONE.** POC-A `cae9363` (2026-01-04) and Guard `36fd12f` (2026-05-13) share **no commit and no ancestor**. 129 days apart | `git log --all --reverse` in both |
| **B. Declared protocol designation** | **PRESENT and explicit.** `APS-950:132` binds RI-PY → `aura-poc-a-core` by URL; `:133` binds RI-RS → `aura-guard`. Present in the **original Polish source** (`APS-950 …_260723_194507.txt:147-152`), so not a conversion artifact | as cited |
| **C. Implementation lineage** | **NONE FOUND.** `RI-RS`, `RI-PY`, `POC-A`: **0 files @HEAD and 0 commits in the guard's full history**. `port of`, `parity`: 0 commits. Guard's own roadmap places "**Reference implementation**" at **v2.0 (2027)** (`ROADMAP.md:78`) and plans a *new* Python verifier (`:82`) | `git grep`, `git log --all -S` |
| **D. Semantic mapping** | **NONE FOUND.** No mapping or adapter code in either repository | §D3-S8 Phase 2 |
| **E. Normative binding** | **ASSERTED, UNACKNOWLEDGED.** The designation exists (B) but neither designee ever references it | B + C |

**Per D3-S8 safety rule 9:** the APS-950 designation is recorded as a *classification*
and is **not** used anywhere to merge POC-A and Guard semantics.
