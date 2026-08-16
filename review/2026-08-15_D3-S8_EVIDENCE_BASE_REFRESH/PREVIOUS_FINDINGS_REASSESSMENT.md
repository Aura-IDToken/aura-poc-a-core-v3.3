# PREVIOUS_FINDINGS_REASSESSMENT — D3-S8

**Phase 12.** Prior audit artifacts are treated as **evidence of prior analysis, not
authoritative evidence**. Every claim below was re-tested against source. The purpose is
to find where the previous understanding was **incomplete or wrong** — not to defend it.
**Normative effect: NONE.**

## 1. Artifacts under reassessment

| Artifact | Commit |
|---|---|
| `review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/` | `e3e4732` |
| `review/2026-08-15_D3-S4_DQ-001-H_CROSS_REPOSITORY_LINEAGE/` | `8a67033` |
| `review/2026-08-15_D3-S5_DQ-002_LAYERED_HASH_DOMAINS/` | `d7ddc6f` |
| `review/2026-08-15_D3-S6_DQ-006_CANONICAL_SERIALIZATION/` | `a0c4901` |

## 2. Claim-by-claim reassessment

| # | Previous claim | Current evidence | Status |
|---|---|---|---|
| 1 | `AuditEntry` is defined at `aura-guard-v1.3` `src/models.rs:50` with 14 fields | Re-read `models.rs` — struct at `:50`, fields at `:52,55,58,66,69,72,75,78,81,84,87,90,93,96` = 14 | **CONFIRMED** |
| 2 | ENT-007 at `APS-200:149-159`; Common Object Contract at `:47-58` | Re-read verbatim | **CONFIRMED** |
| 3 | `chain_hash` occurs 0× in the specification corpus | `git grep` + `git log --all -S` over `aura-specification`: 0 files, 0 commits | **CONFIRMED** |
| 4 | `integrity_hash` / `event_payload_hash` occur 0× in `aura-guard-v1.3` | Re-run over full history: 0 files, 0 commits each | **CONFIRMED** |
| 5 | **"The implementation operates nine distinct SHA-256 constructions"** | Full enumeration of every `Sha256::`/`sha256_*` site returns **13**. The prior count omitted `segment_genesis_hash` (`segment.rs:47-50`), the RFC 3161 request digest (`rfc3161.rs:138`) and two TST verification digests (`tst_verify.rs:657,839`) | **UPDATED — prior count was an undercount** |
| 6 | **Domain separation between the entry chain and the segment chain is "ABSENT"** | `crypto.rs:28` seeds the entry chain with `"AURA-GUARD-GENESIS-v1.3"`; **`segment.rs:48` seeds the segment chain with a distinct constant `b"AURA-GUARD-SEGMENT-GENESIS-v1"`**. The chains are separated at the root, though no per-preimage tag separates them element-wise | **WEAKENED — correct classification is PARTIAL, not ABSENT** |
| 7 | APS-200 asserts no dependency among `integrity_hash`, `event_payload_hash`, `previous_record_hash` | Searched APS-200 for every relational verb (`includ`, `exclud`, `nest`, `derive`, `depend`, `cover`, `compris`, `consist of`, `based on`) — **zero matches in the entire document** | **CONFIRMED — and strengthened** |
| 8 | CONFLICT-DQ002-01: `APS-200:58` vs `APS-300:69` | Re-read both. `APS-200:49` "Every entity MUST contain"; `:41` lists ENT-005; `:129` delegates Evidence fields to APS-300 §5; `APS-300:56` "at minimum" list **omits** `object_id`, `object_type`, `created_at`, `integrity_hash`. The one relational verb in APS-300 is `:69` "excluding this field" | **CONFIRMED** |
| 9 | `chain_hash`'s 9-field preimage byte-stable since `d03eb65` | `git show d03eb65:src/chain.rs` — identical array literal and order to `443f72e` | **CONFIRMED** |
| 10 | `models.rs` documents 7 preimage fields vs 9 implemented, wrong since the first commit | `git show d03eb65:src/models.rs:87` and `443f72e:src/models.rs:95` — identical text, both listing 7 | **CONFIRMED** |
| 11 | CONF-003/002/006 verify only intra-implementation properties | Re-read at `:40,46` in each. Also searched APS-400 + all CONF files for `cross-impl`/`between implementations`/`two implementations` — **zero matches** | **CONFIRMED — and strengthened** |
| 12 | 315-byte canonical stream, SHA-256 `6eb514bf…0222` | Re-verified independently at D3-S8 via `wc -c` and `sha256sum` on the raw blob; field widths re-summed to 315 | **CONFIRMED** |
| 13 | R1 vs R2 timestamp divergence (`+00:00` vs `Z`) | Re-read `AUDIT_LAYER_SPEC.md:41,46` and the exported bytes | **CONFIRMED** — with the qualification, already stated in the DQ-006 artifact, that the two regimes govern **different objects** |
| 14 | APS-950 designates RI-PY/RI-RS by URL, present in the original Polish source | Re-read `APS-950:132-133` and `…_260723_194507.txt:147-152` | **CONFIRMED** |
| 15 | Prior citation `APS-200:145` for `attestation_hash` | Actual line is `:143`; `:145` is the Attestation TODO | **CORRECTED** (fixed in-session before commit) |
| 16 | Prior citation `03_LANGUAGE_BOUNDARY.md:51-54` for the disjointness rows | Actual rows are `:50-53` | **CORRECTED** (fixed in-session before commit) |
| 17 | Prior citation `APS-950:131` for the RI-PY row | `:131` is the table separator; RI-PY is at `:132` | **CORRECTED** (fixed in-session before commit) |
| 18 | Prior citation `EventTrustCertificate` at `audit/merkle.py:37` (quoted from the 2026-08-11 baseline package) | The class statement is at `audit/merkle.py:20` | **CONTRADICTED** — the baseline package's citation is wrong; the class exists, the line number does not match |
| 19 | DQ-006 premise table records **"DQ-001 — ACCEPTED, Option B, Frozen"** | The D3 Decision Gate brief (2026-08-15) states **"DQ-001: CONFLICT / DECISION REQUIRED — Adapter architecture remains unresolved"** | **CONTRADICTED — the DQ-006 artifact's premise is now stale** (§3) |
| 20 | POC-A is internally inconsistent about JSON `separators` | Re-read `audit/merkle.py:85` (compact) vs `core/merkle.py:8` and `compliance/certificate.py:69` (Python defaults) | **CONFIRMED** |
| 21 | DQ-002 recommendation: Option D | Not re-tested — a recommendation is not a fact. Recorded as prior analysis only, carrying no evidential weight into D3-S8 | **N/A — not evidence** |

## 3. The premise contradiction — material, and it propagates

**FACT.** The D3-S5/DQ-002 brief (2026-08-15) opened: "DQ-001 has been formally accepted
by the Architecture Owner: **DECISION = B — EXPLICIT ADAPTER ARCHITECTURE.** This
decision is FROZEN for the purposes of this investigation."

**FACT.** The D3-S6/DQ-006 artifact recorded that premise verbatim in its §0.1 table and
built on it.

**FACT.** The D3 Decision Gate brief (same date) states: "**DQ-001: CONFLICT / DECISION
REQUIRED. Adapter architecture remains unresolved.**"

**INFERENCE.** Two statements of DQ-001's status, both from the Architecture Owner
channel, are mutually exclusive. Under the later statement, the DQ-002 and DQ-006
artifacts each carry a **premise that no longer holds**. Neither artifact's *evidence* is
affected — the file/line facts stand independently — but their framing paragraphs assert
a frozen DQ-001 that is now stated as open.

**Recorded as CONFLICT-DQ008-01.** Not reconciled. Resolution belongs to the Architecture
Owner, who is the only party who can state DQ-001's status. **No prior artifact was
edited** to paper over the change, per the D3-S8 rule against silent reconciliation.

## 4. Net effect on the evidence base

| Category | Count | Items |
|---|---|---|
| **CONFIRMED** | 12 | 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 14, 20 |
| **UPDATED** | 1 | 5 (hash-construction count 9 → 13) |
| **WEAKENED** | 1 | 6 (domain separation ABSENT → PARTIAL) |
| **CONTRADICTED** | 2 | 18 (inherited citation error), 19 (stale DQ-001 premise) |
| **CORRECTED** | 3 | 15, 16, 17 (line-number slips, fixed before commit) |
| **NOT EVIDENCE** | 1 | 21 (a recommendation) |

**INFERENCE.** The two substantive analytical errors — items 5 and 6 — both ran in the
same direction: they **understated the guard's existing cryptographic structure**. The
implementation has more hash domains than reported and more domain separation than
reported. Neither error changes the central DQ-002 finding (the three named hashes still
inhabit disjoint namespaces, and there is still no MATCH row), but both would have made
the implementation look less mature than it is to anyone reading the prior artifact
alone.
