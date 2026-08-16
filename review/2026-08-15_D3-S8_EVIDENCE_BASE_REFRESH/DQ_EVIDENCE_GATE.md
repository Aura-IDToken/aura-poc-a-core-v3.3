# DQ_EVIDENCE_GATE — D3-S8

**Phases 13–14.** Classifications use only: **EVIDENCE SUFFICIENT / EVIDENCE PARTIAL /
EVIDENCE MISSING / CONFLICT**. **Normative effect: NONE. No architecture is recommended.**

## 1. Evidence gate

| DQ | Question | Evidence status | Primary source | Secondary source | Implementation evidence | Historical evidence | Critical gap | Conflict | Impact on next decision |
|---|---|---|---|---|---|---|---|---|---|
| **DQ-001** | `AuditEntry` ↔ ENT-007 / Common Object Contract | **CONFLICT** | `APS-200:16,47-58,149-159` | `RI-RS_…:22,74`; `APS-950:133` | `models.rs:50-97` — 14 fields; **zero APS identifiers in `src/`**; no adapter | `AuditEntry` 2026-05-13 predates ENT-007 2026-07-23 by 71 days | No mapping exists; ENT-007 has no CONF test (`APS-200:238`) | **CONFLICT-DQ001-01** — INV-012 stated as "audit trail" (`APS-100:92`) vs "Audit Record (ENT-007)" (`INV-REG:273`) | Determines whether a binding is required at all |
| **DQ-002** | Hash-domain architecture | **CONFLICT** | `APS-200:58,158,159`; `APS-300:69` | `SPEC-002:186-195,208-211` | **13** SHA-256 sites; `chain_hash` 0× in corpus; `integrity_hash`/`event_payload_hash` 0× in guard | `chain_hash` byte-stable since `d03eb65`; normative names born `b68181e` | **Zero MATCH rows.** `event_payload_hash` states no algorithm | **CONFLICT-DQ002-01** — `APS-200:58` vs `APS-300:69` | Determines how many canonical byte sequences DQ-006 must define |
| **DQ-003** | `schema` ↔ `schema_version` / `protocol_version` | **EVIDENCE PARTIAL** | `APS-200:55,56`; `APS-300:61,62` | `fixtures/schemas/…:11-12,35,39` | `schema = "aura-guard.audit.v1"` (`api/audit.rs:132`, `health.rs:43`); **`schema_version` and `protocol_version`: 0 commits in guard, all history** | `schema` unchanged since `d03eb65` | **One opaque string conflates vendor + object + version**; APS requires **two** distinct fields | None found | Blocks any version-compatibility claim (INV-009) |
| **DQ-004** | Event semantics ↔ `decision` | **EVIDENCE MISSING** | `APS-200:156` `event_type` "Canonical event type"; `:104,108` `decision` + **TODO** | `APS-000` TERM-008 `:46-47` | `decision` ∈ {`DENY`,`REVIEW`,`ALLOW`} from boolean flags (`engine.rs:59-63`); **no `event_type` field anywhere** | `decision` unchanged since `d03eb65` | **"Event payload" and "canonical event type" are undefined** in APS-200, APS-000 and `GLOSSARY.md`. `APS-200:108` TODO: canonical `decision` set undefined | None found | Blocks `event_payload_hash` from having a definable input |
| **DQ-005** | Violation integrity binding | **EVIDENCE PARTIAL** | — | `APS-200:149-159` (ENT-007 has no violations concept) | **`violations` is NOT in `chain_hash`** (`chain.rs:36-47` covers 9 of 14 fields); not in any other domain | `violations` present since `d03eb65`, never hashed | **The word "violation" in the corpus refers only to *invariant* violations** (`APS-100:16,109,144`; `APS-400:156`) — **no normative counterpart to rule-match records exists** | None found | Determines whether a whole-record domain must cover it |
| **DQ-006** | Canonical serialization / bytes | **CONFLICT** | `APS-200:211-218` (+ TODO) | `SPEC-002:215-216,382`; `AUDIT_LAYER_SPEC.md` §1 | **4 regimes** (R1/R2/R2-impl/R3); one exported 315-byte stream, digest re-verified | R1 stable since 2026-05-13; R2 frozen 2026-07-24 | No cross-implementation test exists; all fixtures are `"TODO"` | **CONFLICT-DQ006-01** (invariants vs tests) and **CONFLICT-DQ006-02** (authority direction) | Blocks `integrity_hash` from being computable |
| **DQ-007** | Numeric representation | **EVIDENCE PARTIAL** | `APS-100:76-77` INV-007 | `SPEC-002:141,381` AD-CA-007 **UNRESOLVED** | POC-A: `SCALING_FACTOR = 100000`, int32 (`core/evaluator.py:12`), ADR-005 **APPROVED**. Guard: `f32` in `Violation.confidence` (`models.rs:38`), `policy.rs:41,94` — **but the decision path uses boolean flags only** (`engine.rs:44-63`) | ADR-005 2026-01-23; `f32` since `d03eb65` | **INV-007 is conditional** ("if doing so would violate determinism"); scale/width/rounding/overflow/endianness **unapproved** (`SPEC-002:381`) | None found — POC-A and guard differ but govern different objects | Determines `seq` and `confidence` byte encoding |
| **DQ-008** | Documentation ↔ implementation | **CONFLICT** | — | `chain.rs:6-12` vs `models.rs:95` | **7-field doc vs 9-field implementation, wrong since `d03eb65`**; `chain.rs:11` "unambiguous" claim; GAP-001 APS numbering | Divergence present at first commit and still present | Multiple documented-vs-actual divergences | **CONFLICT-DQ008-01** — DQ-001 status stated both as ACCEPTED-B and as unresolved | Affects trust in every doc-sourced claim |

## 2. Decision readiness (Phase 14)

| DQ | Can a decision be made from current evidence? | Minimum additional evidence required |
|---|---|---|
| **DQ-001** | **NO** | Protocol Custodian ruling on CONFLICT-DQ001-01 (INV-012 scope); a stated Architecture Owner position on DQ-001's actual status (CONFLICT-DQ008-01) |
| **DQ-002** | **NO** | Custodian ruling on CONFLICT-DQ002-01 (`integrity_hash` self-inclusion, and whether `evidence_hash` and `integrity_hash` are one concept or two); a definable input for `event_payload_hash` (⇒ DQ-004) |
| **DQ-003** | **NO** | A normative statement of what `schema_version` versions (the entity definition) versus what `protocol_version` versions (the APS release), and whether one opaque implementation string may satisfy both |
| **DQ-004** | **NO** | A definition of "event", "event payload" and "canonical event type"; resolution of the `APS-200:108` TODO on canonical `decision` values |
| **DQ-005** | **NO** | A normative statement on whether rule-match records are in scope for ENT-007 at all — the corpus currently has no such concept; then DQ-002's domain set |
| **DQ-006** | **NO** | Custodian ruling on CONFLICT-DQ006-02 (authority direction); DQ-002's domain set; a cross-implementation conformance procedure to close CONFLICT-DQ006-01 |
| **DQ-007** | **PARTIAL** | The *prohibition* is evidenced (INV-007 + ADR-005 APPROVED). The *parameters* (width, scale, rounding, overflow, endianness) are explicitly **UNRESOLVED** at `SPEC-002:381`. A decision on the prohibition alone could be made; a decision on encoding could not |
| **DQ-008** | **PARTIAL** | The divergences are fully evidenced and could be *recorded* now. Correcting them touches documentation the corpus disputes authority over (CONFLICT-DQ006-02), so the *remedy* is blocked |

## 3. Safe to decide / must remain open

| Classification | DQs | Reason |
|---|---|---|
| **SAFE TO DECIDE NOW** | **None outright.** | Every DQ is gated on at least one unresolved conflict or missing definition |
| **NARROWLY DECIDABLE** | **DQ-007 (prohibition only)**; **DQ-008 (recording only)** | DQ-007's float prohibition rests on INV-007 plus an **APPROVED** ADR-005 — the only APPROVED decision artifact found in any repository. DQ-008's divergences are documented facts; only the remedy is blocked |
| **MUST REMAIN OPEN** | DQ-001, DQ-002, DQ-003, DQ-004, DQ-005, DQ-006 | Four unresolved conflicts (DQ001-01, DQ002-01, DQ006-01, DQ006-02, DQ008-01) plus three undefined normative terms ("event payload", "canonical event type", `integrity_hash` self-inclusion) |

## 4. Active conflicts

| ID | Statement | Status |
|---|---|---|
| **CONFLICT-DQ001-01** | `APS-100:92` "audit trail" vs `INVARIANT_REGISTRY.md:273` "Audit Record (ENT-007)" | OPEN — Custodian |
| **CONFLICT-DQ002-01** | `APS-200:58` `integrity_hash` "of this object" (self-inclusion unstated) vs `APS-300:69` `evidence_hash` "excluding this field" | OPEN — Custodian |
| **CONFLICT-DQ006-01** | INV-002/003/014 require cross-implementation equality; CONF-002/003/006 verify only intra-implementation; INV-014 has no test | OPEN — Custodian / APS-400 |
| **CONFLICT-DQ006-02** | `AUDIT_LAYER_SPEC.md:17-19` "implementation governs" vs `README.md:17` / `SPEC-002:37` "documentation wins" — both attributed to the Protocol Custodian | OPEN — Custodian |
| **CONFLICT-DQ008-01** | DQ-001 stated as ACCEPTED-B in one brief and as unresolved in another | OPEN — Architecture Owner |
| OQ-A-CONFLICT-001/002 | Decree vs Specification precedence; two hierarchies inside the corpus (Article V does not name APS-200) | OPEN — inherited, not reopened |
| GAP-001 numbering | POC-A's APS numbering incompatible with the corpus; self-declared as inferred without the spec | OPEN — inherited |
