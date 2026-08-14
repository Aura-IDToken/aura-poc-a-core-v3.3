# 07 — D-2 + D-5 Decision Brief

**For:** Human Architectural Authority and Independent Reviewer
**Evidence commit:** `aura-guard-v1.3` @ `443f72e58483c3ea6112ea517647cc0dbf459960`
**Accepted input:** D-1 = YES (CLOSED, Two-Key Gate passed)

**Human decision required.** This brief selects nothing, ranks nothing and
recommends nothing. It states what is established, what the options are, what
each would cost, and what remains unknown.

Supporting detail: `01_…` (D-2), `02_…`/`03_…` (D-5), `04_…` (security),
`05_…` (dependencies), `06_…` (evidence gaps).

---

## 1. D-2 — Integrity Domain Contract

### 1.1 Decision question

**What exactly belongs to the integrity domain of `AuditEntry`?**

D-1 places `violations` inside it. D-2 must state the complete membership and the
contract that governs it.

### 1.2 Evidence established

- **CONFIRMED.** The current digest covers exactly nine values, joined by
  `SEP = "|"`: `prev_hash`, `decision`, `policy_set`, `policy_hash`, `context`,
  `input_hash`, `shadow_hash`, `seq`, `timestamp` (`src/chain.rs:20`, `:25–49`).
- **CONFIRMED.** Outside it: `violations`, `schema`, `audit_id`, `request_id`
  (plus `chain_hash` itself, which is the output).
- **CONFIRMED.** The boundary is a single point. `entry_leaf_hash` consumes only
  `chain_hash` (`src/segment.rs:140–150`); the Merkle root consumes only leaves
  (`:151–158`); the segment preimage consumes the root (`:91–106`); both the
  segment chain hash (`:109–121`) and the TSA imprint (`:123–131`) consume that
  preimage. Whatever the entry digest covers, the other four inherit.
- **CONFIRMED.** All fourteen `AuditEntry` fields are enumerated in `01_…` §2
  with type, provenance, current protection status, and citation.
- **CONFIRMED.** `docs/adrs/0001-hash-chain.md` is accepted and still current,
  but describes the digest only as "SHA-256 of **canonical fields** incl.
  `prev_hash`" — it does not enumerate the field set.
- **EVIDENCE GAP (G-6).** No source states an *intended* integrity domain. D-2 is
  therefore **defining** the domain, not recovering a prior specification.

### 1.3 Candidate boundaries

**NON-NORMATIVE CANDIDATES.** Presented in label order; not ranked.

| # | Boundary | Membership |
|---|---|---|
| B-1 | Minimal | nine current fields + `violations` |
| B-2 | Minimal + discriminator | B-1 + `schema` |
| B-3 | Whole record | B-1 + `schema` + `audit_id` + `request_id` |
| B-4 | Sibling digest | `compute_chain_hash` unchanged; a separate violations digest carried and verified alongside |
| B-5 | Nested digest | a violations digest becomes one input to `compute_chain_hash` |

B-4 and B-5 are shape choices orthogonal to B-1…B-3 membership; a decision may
combine one of each. All five satisfy D-1.

### 1.4 Consequences

| Consequence class | Effect |
|---|---|
| **Architectural** | B-1/B-2/B-3/B-5 redefine the entry digest, and the redefinition propagates to leaf, root, segment hash and TSA imprint. B-4 leaves the existing digest intact and adds a second artifact a verifier must be made to check |
| **Implementation** | Every candidate requires a byte reduction for violation data (D-3) and brings `confidence: f32` (`src/models.rs:38`) into a digest for the first time, unless the reduction excludes it |
| **Migration** | B-1/B-2/B-3/B-5 trigger every consequence in `02_…` §5. B-4 does not — it narrows D-5 to "how does the new artifact behave on entries that lack it" |
| **Verification** | B-4's second artifact is skippable unless the design makes omission fail closed; B-1/B-2/B-3/B-5 keep one digest to check |
| **Discriminator** | B-2/B-3 make `schema` unforgeable but create the bootstrap ordering in `04_…` §B; B-1/B-4/B-5 leave it rewritable |

### 1.5 Evidence gaps

G-6 (no recorded intended domain), G-7 (protocol-version semantics of a digest
change), G-5 (external integrators). See `06_…`.

### 1.6 Unresolved questions

**D2-Q1 … D2-Q14**, in `01_…` §4. They cover, at minimum: whether `schema`,
`audit_id` and `request_id` belong; whether `timestamp` requires canonicalization;
whether `violations` is a list, sequence, multiset or set; whether ordering
matters; whether duplicates are meaningful; whether `None` ≡ `[]`; whether
semantically equivalent violations must hash identically; whether omission is
distinct from an explicit empty value; and whether the domain carries a
discriminator that is itself protected.

---

## 2. D-5 — Existing v1 Log Compatibility

### 2.1 Decision question

**How are existing v1 logs handled once the integrity rule changes?**

### 2.2 Evidence established

- **CONFIRMED.** Entries carry `schema: "aura-guard.audit.v1"` as an inline
  literal (`src/api/audit.rs:132`) — **read by no code** (`log_writer.rs:151–170`;
  `chain.rs:71–92`) and **covered by no digest** (`chain.rs:25–49`).
- **CONFIRMED.** No audit-entry versioning mechanism exists. The only precedent
  is on the segment path (`segment.rs:341–342`; `sealer.rs:100`).
- **CONFIRMED.** A verifier cannot determine which rule produced a given entry;
  one hard-coded rule is applied to all (`chain.rs:53–65`).
- **CONFIRMED.** A digest change makes every pre-existing entry, every manifest
  Merkle root (`segment.rs:394`) and every stored `head_chain_hash_at_close`
  (`:401`) unreproducible — and, absent a discriminator, **silently** so: a
  legitimate v1 entry and a tampered v2 entry produce the same verifier outcome.
- **CONFIRMED.** Re-derivation is mechanically possible: the full entry,
  `violations` included, is persisted (`log_writer.rs:96`).
- **CONFIRMED.** Real RFC 3161 tokens over v1-derived imprints exist in-repo
  (`tests/fixtures/tsa/segment-00{1,2}.tsr`, FreeTSA, sealed 2026-05-20),
  verified by `tests/tst_verify.rs` against the `segment_chain_preimage` imprint.
  TSA continuity is a present concern, not a hypothetical one.
- **EVIDENCE GAP.** Whether production logs exist (G-1), are externally relied
  upon (G-2), or carry retention obligations (G-3) is not determinable from the
  repository.

### 2.3 Strategies

**D-5-A** legacy preservation · **D-5-B** new version only · **D-5-C** migration
/ re-sealing · **D-5-D** reject legacy · **D-5-E** hybrid version-discriminated.
Full analysis and the twelve-column comparison matrix are in `03_…`. **No
strategy is ranked or preferred, D-5-E included.**

### 2.4 Consequences

| Class | Summary |
|---|---|
| **Compatibility** | A and E preserve historical verifiability if rule selection is reliable; B and D forgo it in the shipped tool; C achieves uniformity by rewriting history |
| **Security** | A and E introduce a rule-selection surface (`04_…` §A). With an unprotected discriminator, rule selection is influenceable by anyone who can write the log. B, C, D keep one rule but relocate risk to legacy handling, migration, or detection |
| **Replay** | A, E require replay to branch on a discriminator; B, D require replay to *detect* v1 to fail intelligibly; C makes replay uniform post-migration (`04_…` §D) |
| **Continuity** | Chain linkage survives in *form* under every strategy but changes *meaning* across a boundary. Merkle continuity breaks for pre-change segments under any entry-digest change. TSA evidence survives A/B/D/E and is irrecoverably destroyed by C (`04_…` §E) |
| **Operational** | A/E require two rules to remain correct indefinitely; B/D require the legacy capability to be retained or documented; C requires an auditable rewrite of an append-only corpus |

### 2.5 Evidence gaps

G-1 … G-4, G-8, G-9. Critically: **G-1, G-2 and G-3 gate a responsible
selection.** The strategy space is fully mapped; the choice among strategies
depends on deployment facts the repository cannot supply.

### 2.6 Unresolved questions

S-1 … S-7 in `04_…` §F, plus: is retroactive verifiability a requirement, a
preference, or immaterial? Which continuity properties are obligations? Is
destroying existing TSA evidence admissible if C is chosen?

---

## 3. Dependency summary

- **D-2 → D-3, D-4, D-6, D-7:** hard, all four.
- **D-2 → D-5:** hard. A sibling-digest outcome (B-4) narrows D-5's premise
  sharply; an entry-digest outcome triggers it fully.
- **D-5 ↔ D-7:** **hard and bidirectional.** A/E require a selection mechanism,
  which is D-7; and if D-7 cannot supply a trustworthy discriminator, A/E lose
  their mechanism and the space collapses toward B/C/D. Both depend on D2-Q11.
- **D-4 → D-5:** conditional — becomes hard only if D-4 requires a distinction
  the persisted record has already erased (`skip_serializing_if`,
  `src/models.rs:40`).

Full inventory: `05_…`.

---

## 4. Readiness assessment

**Stated as a finding, not as advice on what to decide or in what order.**

- **D-2** has no unmet decision-dependency. Its inputs are D-1 (closed) and the
  field-level evidence in `01_…`, which is complete for all fourteen fields.
- **D-5** has a fully mapped strategy space, but selection among the classes is
  coupled to D-2 (which determines whether the premise even arises), to D-7 (which
  determines whether A/E are mechanically available), and to evidence gaps
  G-1/G-2/G-3, which lie outside the repository.

---

## 5. Two-Key Gate

```
D-2 STATUS: DECISION READY

D-5 STATUS: NOT READY
    Reason: strategy space complete and evidence-derived, but selection depends
    on G-1 (production logs exist?), G-2 (external reliance?), G-3 (retention
    obligations?) — none determinable from the repository — and on D-2 and D-7,
    both OPEN. The D-5 material is decision-READY as an analysis; the decision
    itself cannot be responsibly taken until those inputs are supplied.

HUMAN ARCHITECTURAL AUTHORITY:
PENDING

INDEPENDENT REVIEW:
PENDING

FINAL DECISION:
NONE

NORMATIVE CHANGE:
NONE

PRODUCTION CODE CHANGE:
NONE
```

---

## 6. Decision Record — to be completed by the Authority

### D-2

| Field | Value |
|---|---|
| Integrity domain membership | |
| Shape (entry digest / sibling / nested) | |
| Answers to D2-Q1 … D2-Q14 | |
| Decided by | |
| Independent reviewer | |
| Date | |
| Authority basis | |

### D-5

| Field | Value |
|---|---|
| Strategy (A / B / C / D / E / other) | |
| Evidence supplied for G-1, G-2, G-3 | |
| Continuity properties deemed mandatory | |
| Decided by | |
| Independent reviewer | |
| Date | |
| Authority basis | |

---

*This package has no normative effect. It records evidence and a decision
surface. It selects nothing and implements nothing. No production code was
modified; no file in `aura-guard-v1.3` was created, modified or deleted; the
source was read from a pristine read-only clone pinned at `443f72e`.*
