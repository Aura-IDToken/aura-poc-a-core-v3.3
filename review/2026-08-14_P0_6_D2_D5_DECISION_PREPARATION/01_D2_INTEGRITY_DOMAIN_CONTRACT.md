# 01 — D-2: Integrity Domain Contract (decision space)

**Decision:** D-2 — *What exactly belongs to the integrity domain?*
**Input:** D-1 = YES (CLOSED) — `violations` is in the domain.
**Status:** OPEN. Nothing in this file is decided.

Classification legend: see `00_SCOPE_AND_DECISION_CONTEXT.md` §4.

> **No field is proposed for inclusion here.** A field existing in `AuditEntry`
> is not evidence that it belongs in the integrity domain; a field being useful
> for versioning is not evidence that it must be hashed. Those are D-2's to
> decide.

---

## 1. Current derivation boundary — traced from source

**CONFIRMED.** Each link consumes only what is listed. Nothing else.

| # | Link | Function | Consumes | Consumes `violations`? | Cite |
|---|---|---|---|:--:|---|
| 1 | `violations` → `AuditEntry` | struct field | — | n/a (it *is* the field) | `src/models.rs:90` |
| 2 | `AuditEntry` → `chain_hash` | `compute_chain_hash` | 9 scalar args joined by `SEP="\|"`; does not accept an `AuditEntry` | **NO** | `src/chain.rs:20`, `:25–49` |
| 3 | `chain_hash` → `entry_leaf_hash` | `entry_leaf_hash` | `hex::decode(entry.chain_hash)` → `leaf_hash(raw)` — that field alone | **NO** | `src/segment.rs:140–150` |
| 4 | leaf → Merkle root | `segment_merkle_root` | `entry_leaf_hash` per entry; no other entry field | **NO** | `src/segment.rs:151–158` |
| 5 | root → segment chain | `segment_chain_preimage` | `prev_segment_chain_hash`, `merkle_root`, `first_seq`, `last_seq`, `sealed_at` | **NO** | `src/segment.rs:91–106` |
| 6 | preimage → segment hash | `recompute_segment_chain_hash` | `SHA-256(preimage)` | **NO** | `src/segment.rs:109–121` |
| 7 | preimage → TSA imprint | `tsa_message_imprint` | `SHA-256(same preimage)` | **NO** | `src/segment.rs:123–131` |
| 8 | verification | `verify_chain` | `prev_hash` linkage + `recompute_for_entry` equality; two checks, nothing else | **NO** | `src/chain.rs:71–92`, `:53–65` |
| 9 | replay | `aura-replay` | `verify_chain`, optional lineage, `verify_segment_chain`, `verify_manifest_against_entries` | **NO** | `src/bin/aura_replay.rs:113`, `:134–153`, `:175`, `:194` |

```
violations ──✗ (consumed by no integrity link)
    AuditEntry            [models.rs:50-97]
        chain_hash        [chain.rs:25-49]   ← boundary starts here
            entry_leaf_hash    [segment.rs:140-150]
                merkle_root    [segment.rs:151-158]
                    segment_chain_preimage  [segment.rs:91-106]
                        segment_chain_hash  [segment.rs:109-121]
                        tsa_message_imprint [segment.rs:123-131]
            prev_hash of entry N+1          [chain.rs:71-92]
```

**IMPLEMENTATION-DERIVED.** The boundary is a single point: step 2. Every
downstream mechanism inherits whatever step 2 covers. This establishes *where the
boundary currently is*. It does not describe where it ought to be — that is D-2.

---

## 2. Per-field analysis

Thirteen attributes per field, as required. `AuditEntry` declares fourteen fields
(`src/models.rs:50–97`); all fourteen appear below.

Shared to every field, stated once: **evidence** for type/order/doc is
`src/models.rs:50–97`; **D-1 consequence** applies directly only to `violations`.

### A. Currently protected fields (9)

#### A1 `prev_hash`
1. `prev_hash` · 2. `String` (hex SHA-256) · 3. `state.log.current_head()`
(`src/api/audit.rs:118`); genesis for entry 0 —
`sha256_hex("AURA-GUARD-GENESIS-v1.3")` (`src/crypto.rs:27–30`) · 4. links entry
N to N−1 · 5. **YES** (`chain.rs:37`) · 6. none — D-1 does not alter it ·
7. chain continuity · 8. already a fixed-width hex string; no canonicalization
question raised by evidence · 9. **OPEN** — whether a rule change alters the
genesis constant; note `crypto.rs:25` states it "must never be changed without
bumping the protocol version" · 10. checked first in `verify_chain`
(`chain.rs:71–92`) · 11. unchanged in *form* across any rule change; the values
either side of a boundary are computed under different definitions · 12.
CONFIRMED · 13. **OPEN**: does a digest-domain change constitute a protocol
version bump in the sense of `crypto.rs:25`?

#### A2 `decision`
1. `decision` · 2. `String` (`DENY`/`REVIEW`/`ALLOW`) · 3. `evaluate()`
aggregate (`src/engine.rs:58–65`) · 4. the outcome · 5. **YES** (`chain.rs:38`) ·
6. none · 7. aggregate verdict; records *that*, not *why* · 8. free-form
`String`, not an enum — an unconstrained-domain question exists but is not raised
by D-2 · 9. **OPEN** · 10. the §5-control field: tampering here is detected
today · 11. none · 12. CONFIRMED · 13. **OPEN**: does D-2 constrain
`decision`'s value domain, or leave it as-is?

#### A3 `policy_set`
1. `policy_set` · 2. `String` · 3. `policy.name` (`src/api/audit.rs:121`) ·
4. which policy pack was evaluated · 5. **YES** (`chain.rs:39`) · 6. none ·
7. policy identity by name · 8. free-form string · 9. **OPEN** · 10. used by
`--verify-lineage` to reload the policy (`aura_replay.rs:134–137`) · 11. none ·
12. CONFIRMED · 13. **OPEN**: none specific to D-2.

#### A4 `policy_hash`
1. `policy_hash` · 2. `String` (hex SHA-256 of policy YAML bytes) ·
3. `policy.policy_hash` (`src/api/audit.rs:122`) · 4. provenance pin for the
evaluated policy · 5. **YES** (`chain.rs:40`) · 6. none directly; it is the
field that pins *which rules could have fired*, so it interacts with any
argument about reproducing violations · 7. policy content identity · 8. fixed
hex · 9. **OPEN** · 10. compared against on-disk policy under
`--verify-lineage` (`aura_replay.rs:149–153`) · 11. none · 12. CONFIRMED ·
13. **OPEN**: does D-2 treat `policy_hash` + `input_hash` as *sufficient* to
reconstruct violations, or as merely necessary? (Bears on scope, not on D-1.)

#### A5 `context`
1. `context` · 2. `String` · 3. verbatim echo of `req.context`
(`src/api/audit.rs:123`) · 4. caller-supplied evaluation context · 5. **YES**
(`chain.rs:41`) · 6. none · 7. request context · 8. **OPEN** — it is raw
caller-controlled text joined into a `"|"`-delimited preimage; separator
collision is a live question for any preimage change · 9. **OPEN** · 10. hashed
only · 11. none · 12. CONFIRMED · 13. **OPEN**: does D-2 require an
injective/escaped preimage encoding for caller-controlled strings?

#### A6 `input_hash`
1. `input_hash` · 2. `String` (hex SHA-256) · 3. `sha256_hex(context + " " +
prompt + " " + response)` (`src/api/audit.rs:104–109`) · 4. binds the original
input · 5. **YES** (`chain.rs:42`) · 6. none · 7. input identity · 8. fixed hex ·
9. **OPEN** · 10. hashed only · 11. none · 12. CONFIRMED · 13. **OPEN**: none
specific.

#### A7 `shadow_hash`
1. `shadow_hash` · 2. `String` (hex SHA-256) · 3. `sha256_hex(shadow_normalize(
original))` (`src/api/audit.rs:108`, `:110`) · 4. binds the regex evaluation
surface · 5. **YES** (`chain.rs:43`) · 6. none · 7. normalized input identity ·
8. fixed hex · 9. **OPEN** · 10. hashed only · 11. none · 12. CONFIRMED ·
13. **OPEN**: none specific.

#### A8 `seq`
1. `seq` · 2. `u64` · 3. `state.log.next_seq()` (`src/api/audit.rs:116`) ·
4. monotonic 0-based ordering · 5. **YES**, via `&seq.to_string()`
(`chain.rs:44`) · 6. none · 7. record position · 8. **OPEN** — decimal string
rendering of an integer is already an implicit encoding choice; any preimage
redefinition re-opens it · 9. **OPEN** — a `seq` boundary is one candidate
discriminator for D-5 · 10. ordering is verified via `prev_hash` linkage ·
11. **relevant** — a cut-over at a stated `seq` is a D-5-A/E candidate mechanism ·
12. CONFIRMED · 13. **OPEN**: is `seq` an admissible version discriminator, or
must the discriminator be explicit? (D-2 ↔ D-5/D-7.)

#### A9 `timestamp`
1. `timestamp` · 2. `String` · 3. `Utc::now().to_rfc3339()`
(`src/api/audit.rs:117`) · 4. when the decision was produced · 5. **YES**
(`chain.rs:45`) · 6. none · 7. decision time · 8. **OPEN** — RFC 3339 admits
multiple textual renderings of the same instant (offset form, fractional-second
digits). The value is hashed as *text*, so text differences are digest
differences. Compare the fixture `"2026-05-20T20:22:47.560539282+00:00"`
(`tests/fixtures/tsa/segment-001.manifest.json`), which uses `+00:00`, not `Z`,
with nine fractional digits · 9. **OPEN** · 10. hashed only · 11. none ·
12. CONFIRMED · 13. **OPEN**: does the protected domain fix a canonical
timestamp representation, or protect the stored text as-is? *(This is D2-Q4; it
is not answered here.)*

### B. Newly mandated field (1)

#### B1 `violations`
1. `violations` · 2. `Vec<Violation>`; `Violation { rule: String, action:
String, confidence: f32, validator: Option<String> }` (`src/models.rs:32–42`) ·
3. `evaluate()` (`src/engine.rs:14`), pushed at `:50`, stored at
`src/api/audit.rs:143` · 4. the substantiation of the decision — which rule
fired, what action it declared, at what confidence, and any semantic validator
outcome · 5. **NO — currently outside** (`chain.rs:25–49`) · 6. **D-1 = YES:
it must enter the integrity domain. The remaining question is not *whether* but
*where and how*, which is D-2/D-3** · 7. decision substantiation ·
8. **OPEN — the central canonicalization question.** Sub-questions visible in
evidence: `validator: Option<String>` carries `skip_serializing_if =
"Option::is_none"` (`models.rs:40`), so `None` is *absent* on disk and
indistinguishable from an omitted key; `confidence: f32` (`models.rs:38`) is the
only float in the record, sourced from policy YAML (`src/policy.rs:41`, `:94`),
and JSON cannot represent `NaN`/infinity, for which no guard exists. **These are
D-3/D-4, not D-2** · 9. **OPEN** · 10. **currently read by no verifier**
(`chain.rs:71–92`; `aura_replay.rs`) — D-1 changes this, D-6 defines how ·
11. **maximal** — this is the field whose inclusion changes the digest and
therefore invalidates recomputation of existing entries (see `02_...` §5) ·
12. CONFIRMED · 13. **OPEN**: does `violations` enter `compute_chain_hash`
directly, via an intermediate per-entry digest, or through a parallel structure?
Is it treated as an ordered sequence, a multiset, or a set? *(D2-Q5, D2-Q6,
D2-Q7 — not answered here.)*

### C. Fields currently outside the domain (3)

> Their presence in `AuditEntry` is **not** an argument for inclusion. Each is
> listed so D-2 can decide explicitly rather than by omission.

#### C1 `schema`
1. `schema` · 2. `String` · 3. inline literal `"aura-guard.audit.v1"` at the
construction site (`src/api/audit.rs:132`); no named constant exists, and the
only other occurrence in `src/` is a test fixture (`src/chain.rs:101`) ·
4. declares the entry's format version · 5. **NO** · 6. none — D-1 says nothing
about it · 7. version discriminator · 8. **OPEN** · 9. **OPEN — this is the
field on which D-7 will most likely turn, but it is not thereby required to be
hashed** · 10. **read by no verifier**: `read_all_entries` deserializes without
inspecting it (`src/log_writer.rs:151–170`) and `verify_chain` never reads it ·
11. **maximal relevance to D-5** — an unprotected discriminator can be rewritten,
which is the downgrade question in `04_...` §A/§B · 12. CONFIRMED ·
13. **OPEN**: does `schema` belong in the integrity domain? *(D2-Q1.)*

#### C2 `audit_id`
1. `audit_id` · 2. `String` (UUIDv4) · 3. `Uuid::new_v4().to_string()`,
server-generated (`src/api/audit.rs:53`) · 4. unique per-request identifier ·
5. **NO** · 6. none · 7. record identity for correlation and tracing
(`src/api/audit.rs:57`, `:86`) · 8. **OPEN** · 9. **OPEN** · 10. not read by any
verifier · 11. low — it is per-entry metadata, not chain state · 12. CONFIRMED ·
13. **OPEN**: does `audit_id` belong in the integrity domain? Would an
unprotected `audit_id` permit re-identification of a record without breaking the
chain? *(D2-Q2.)*

#### C3 `request_id`
1. `request_id` · 2. `Option<String>`, `#[serde(default,
skip_serializing_if = "Option::is_none")]` (`src/models.rs:64–66`) ·
3. `extract_request_id(&headers)` from `X-Request-ID`, length-bounded
(`src/api/audit.rs:19`, `:25–29`, `:52`) · 4. caller-supplied correlation id ·
5. **NO** · 6. none · 7. cross-service tracing · 8. **OPEN — and it shares
`violations`' `Option` problem**: `None` is omitted from the JSON entirely, so
absent and `None` are indistinguishable on disk · 9. **OPEN** · 10. not read by
any verifier · 11. low · 12. CONFIRMED · 13. **OPEN**: does `request_id` belong
in the integrity domain, given it is caller-controlled? *(D2-Q3.)*

**NORMATIVE CONFLICT (documentation, minor).** `src/models.rs:60–66` carries two
consecutive doc-comments for `request_id` that disagree on provenance: the first
says "Caller-supplied … when present and valid; omitted otherwise", the second
says "Caller-supplied (or server-generated)". `src/api/audit.rs:52` shows
extraction only, with no server-side fallback. Flagged, not reconciled.

### D. Self-referential field (1)

#### D1 `chain_hash`
1. `chain_hash` · 2. `String` (hex SHA-256) · 3. `compute_chain_hash(...)`
(`src/api/audit.rs:119`) · 4. the digest itself · 5. **n/a — it is the output**,
so it cannot be an input to itself · 6. its *definition* changes if D-2 widens
the domain; the field itself is not "added" · 7. per-entry integrity anchor and
the sole input to every downstream mechanism (§1) · 8. fixed hex; the
canonicalization question applies to its *preimage*, not to the field ·
9. **OPEN** · 10. compared against `recompute_for_entry` (`chain.rs:53–65`,
`:71–92`) and consumed by `entry_leaf_hash` and
`verify_manifest_against_entries` (`segment.rs:401`) · 11. **maximal** — every
stored value becomes unreproducible under a changed rule · 12. CONFIRMED ·
13. **OPEN**: does D-2 redefine this digest's preimage, or leave it and add a
sibling digest? Both are admissible readings of D-1.

---

## 3. Integrity Domain Contract — NON-NORMATIVE TEMPLATE

**This is a template, not a contract.** Every unresolved cell is `OPEN` and is
not filled by assumption. "Protected" reflects *current* state; the "Decision"
column is what D-2 fills in.

| Field | Meaning | Type | Protected (now) | Canonical Form | Versioned | Replay | Migration | Evidence | Decision |
|---|---|---|:--:|---|---|---|---|---|---|
| `schema` | format version | `String` | NO | OPEN | OPEN | not read today | OPEN | `api/audit.rs:132`; `log_writer.rs:151–170` | **OPEN** (D2-Q1) |
| `seq` | record position | `u64` | YES | OPEN (decimal-string today) | OPEN | linkage-checked | boundary candidate | `chain.rs:44` | **OPEN** |
| `audit_id` | record identity | `String` | NO | OPEN | OPEN | not read | OPEN | `api/audit.rs:53` | **OPEN** (D2-Q2) |
| `request_id` | correlation id | `Option<String>` | NO | OPEN (`None` ≡ absent today) | OPEN | not read | OPEN | `models.rs:64–66` | **OPEN** (D2-Q3) |
| `timestamp` | decision time | `String` | YES | OPEN (RFC 3339 text as-is) | OPEN | hashed only | OPEN | `api/audit.rs:117` | **OPEN** (D2-Q4) |
| `decision` | verdict | `String` | YES | OPEN | OPEN | control field | none | `chain.rs:38` | **OPEN** |
| `policy_set` | policy pack | `String` | YES | OPEN | OPEN | lineage | none | `chain.rs:39` | **OPEN** |
| `policy_hash` | policy provenance | `String` | YES | fixed hex | OPEN | lineage | none | `chain.rs:40` | **OPEN** |
| `context` | request context | `String` | YES | OPEN (unescaped in `"\|"` preimage) | OPEN | hashed only | OPEN | `chain.rs:41` | **OPEN** |
| `input_hash` | input identity | `String` | YES | fixed hex | OPEN | hashed only | none | `chain.rs:42` | **OPEN** |
| `shadow_hash` | normalized input | `String` | YES | fixed hex | OPEN | hashed only | none | `chain.rs:43` | **OPEN** |
| **`violations`** | substantiation | `Vec<Violation>` | **NO → must become protected (D-1)** | **OPEN** (D-3) | OPEN | not read today (D-6) | **maximal** (D-5) | `chain.rs:25–49`; `models.rs:90` | **placement/shape OPEN** |
| `prev_hash` | chain linkage | `String` | YES | fixed hex | OPEN | linkage-checked | form unchanged | `chain.rs:37` | **OPEN** |
| `chain_hash` | entry digest | `String` | n/a (output) | preimage OPEN | OPEN | recomputed | maximal | `chain.rs:25–49` | **OPEN** |

**Contract clauses left deliberately empty — all OPEN:** domain membership list;
preimage construction and separator/escaping rule; hash domain and any
domain-separation prefix; treatment of `Option`/absent fields; empty-collection
form; ordering rule; duplicate rule; version discriminator and its own
protection status; the boundary at which the contract takes effect.

---

## 4. Integrity Domain Questions

**Questions only. No answers, no leanings, no ranking.**

| ID | Question | Bears on |
|---|---|---|
| **D2-Q1** | Does `schema` belong in the integrity domain? Note it is currently read by no verifier (`log_writer.rs:151–170`), so protecting it and *using* it are separable decisions. | D-5, D-7 |
| **D2-Q2** | Does `audit_id` belong in the integrity domain? | D-2 |
| **D2-Q3** | Does `request_id` belong in the integrity domain, given it is caller-controlled and absent-when-`None`? | D-2, D-4 |
| **D2-Q4** | Does the protected domain require a canonical `timestamp` representation, or does it protect the stored RFC 3339 text as written? | D-3 |
| **D2-Q5** | Is `violations` semantically a list, an ordered sequence, a multiset, a set, or another object? The chosen semantics — not the current `Vec` — governs what the digest must preserve. | D-3, D-4 |
| **D2-Q6** | Does the order of violations carry meaning that the integrity domain must preserve? Evidence: order equals YAML declaration order (`policy.rs:233–237`, `engine.rs:19`, `:50`) while the decision aggregate is order-independent (`engine.rs:58–65`). | D-4 |
| **D2-Q7** | Are duplicate violations meaningful? Evidence: one rule yields at most one violation (`engine.rs:28`, first-match `find`), so duplicates arise only from two YAML rules sharing an `id`. | D-4 |
| **D2-Q8** | Are `None` and `[]` equivalent within the protected domain — and is an *omitted* field distinct from an explicit empty value? Evidence: `skip_serializing_if` erases the distinction on disk for `validator` (`models.rs:40`) and `request_id` (`models.rs:65`). | D-3, D-4 |
| **D2-Q9** | Must semantically equivalent violation objects hash identically (e.g. `0.1` vs `0.10`; key reordering; whitespace)? Equivalently: at which level — bit, structural, or semantic — is equality defined? | D-3 |
| **D2-Q10** | Is field omission distinct from explicit empty value **at the preimage level**, independent of what JSON does? (Q8 asks about the data model; this asks about the digest input.) | D-3 |
| **D2-Q11** | Does the protected domain carry a schema/version discriminator at all — and if so, is that discriminator itself inside the domain it discriminates? | D-5, D-7 |
| **D2-Q12** | Does `violations` enter the existing entry digest, or a sibling digest referenced by it, or a parallel structure? All three satisfy D-1. | D-3, D-5 |
| **D2-Q13** | Does the protected domain require an injective preimage encoding — i.e. must it be impossible for two distinct records to produce identical digest input? Evidence: the current preimage joins unescaped caller-controlled strings with `"\|"` (`chain.rs:35–47`). | D-3 |
| **D2-Q14** | Does a change to the digest domain constitute a "protocol version" bump in the sense of `src/crypto.rs:25`, which states the genesis constant "must never be changed without bumping the protocol version"? | D-7 |

---

## 5. Governing authority for the current domain

**CONFIRMED.** An accepted ADR governs the chain in the Guard repository:
`docs/adrs/0001-hash-chain.md`, "Status: Accepted in v1.3, still current". It
records the decision to adopt a chained SHA-256 per-entry primitive, and pins the
genesis as `SHA-256("AURA-GUARD-GENESIS-v1.3")`.

**CONFIRMED — what it does not say.** ADR-0001 describes `chain_hash` only as
"SHA-256 of **canonical fields** incl. `prev_hash`". It **does not enumerate the
protected field set**, does not name `violations` either way, and specifies no
canonicalization rule.

**EVIDENCE GAP.** No source among (1)–(6) in `00_...` §5 — including ADR-0001 —
states which fields constitute the integrity domain. The nine-field set is
observable behaviour, not a specified requirement. The domain is therefore being
**defined** by D-2, not *recovered* from a prior specification.

**IMPLEMENTATION-DERIVED consequence for process.** Because ADR-0001 is an
accepted, still-current artifact in the Guard repository, any D-2 outcome that
changes the digest interacts with it — whether by amendment, supersession, or
being judged within its existing latitude ("canonical fields" being unenumerated).
Which of those applies is itself **OPEN** and is noted here as a dependency, not
resolved.
