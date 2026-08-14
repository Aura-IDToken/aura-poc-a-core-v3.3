# 09 — D-7 Decision Brief

**For:** Human Architectural Authority and Independent Reviewer
**Evidence:** `AuraIDToken/aura-guard-v1.3` @ `443f72e58483c3ea6112ea517647cc0dbf459960`
**Accepted inputs:** D-1, D-2, D-3, D-4 = CLOSED. D-5 = BLOCKED.

**Human decision required.** This brief selects nothing and ranks nothing. It
does not answer "which candidate should we choose?" — that question belongs to
the two-key review.

---

## 1. The question

How can an audit verifier determine which integrity/digest rule applies to a
given `AuditEntry`, across the transition from the current v1 digest domain to
the D-1/D-2/D-3/D-4-defined integrity domain?

## 2. What the evidence establishes

Seven findings that shape the decision. All CONFIRMED unless marked.

1. **No selection mechanism exists.** One hard-coded rule is applied to every
   entry (`src/chain.rs:53–65`). A verifier cannot determine which rule produced
   a record.
2. **A version string exists but is inert.** `schema: "aura-guard.audit.v1"` is
   an inline literal (`src/api/audit.rs:132`), **outside the digest**
   (`src/chain.rs:25–49`) and **read by no verifier**
   (`src/log_writer.rs:151–170`). It is server-generated, not caller-supplied —
   so it is attacker-controlled only **at rest**.
3. **A schema-rejection precedent exists — but on the segment path only.**
   `SEGMENT_SCHEMA` is checked in two places (`src/segment.rs:341–342`;
   `src/sealer.rs:100`). Note it establishes *checking*, not *protecting*: the
   manifest `schema` is likewise outside the segment preimage
   (`src/segment.rs:91–106`).
4. **An externally-selected verification mode is already precedented.**
   `aura-seal verify-tst` runs strict verification with `--tsa-roots` and
   imprint-only without it, emitting a stderr warning
   (`src/bin/aura_seal.rs:338–365`; `docs/segments-and-timestamping.md`).
5. **Structural discrimination already exists, asymmetrically.** `AuditEntry`
   has no `deny_unknown_fields` (`src/models.rs:50–97`), so unknown extra fields
   are silently ignored while a missing required field is fatal at parse
   (`src/log_writer.rs:163–166`) — surfacing as exit `1` "malformed log", **not**
   exit `2` (`docs/exit-codes.md`).
6. **Version markers already exist at the chain roots.** Genesis constants embed
   version strings (`src/crypto.rs:27–30`; `src/segment.rs:45–49`), and
   `crypto.rs:25` states the genesis "must never be changed without bumping the
   protocol version" (quotation).
7. **Real TSA evidence exists over v1-derived imprints**
   (`tests/fixtures/tsa/segment-00{1,2}.tsr`; `tests/tst_verify.rs`), and **no
   D-7 candidate endangers it** — token destruction would come only from a D-5
   re-sealing strategy.

## 3. Candidate space

Seven NON-NORMATIVE CANDIDATES, unranked (`02_…`): **A** discriminator outside
the digest · **B** inside the digest · **C** external verifier selection ·
**D** self-describing digest / domain separation · **E** dual / parallel
verification · **F** legacy/new verifier families · **G** structural /
genesis-anchored determination.

**Viability assessed, not assumed:** none is ruled out by the evidence. Four
(A, C, F, G-structural) are fully evaluable now. Three (B, D, E) cannot be fully
evaluated until EG-1 closes. Candidates are not mutually exclusive.

## 4. Consequences

| Dimension | Summary |
|---|---|
| **Downgrade** | An unprotected in-band selector creates the exposure by construction (CONFIRMED, mechanical). A bound selector shifts it to a bootstrap ordering. Trial verification makes the accept rule itself the exposure. External selection relocates it to invocation. No candidate resists downgrade automatically |
| **Upgrade confusion** | Appears self-limiting — mislabelling old-as-new yields a verification failure, not a false accept (INFERENCE) |
| **Ambiguity** | Legacy / corrupt / tampered are indistinguishable today; a version mismatch can additionally surface as "malformed log", naming the wrong problem |
| **Merkle** | A segment spanning a generation boundary has no single reproducing rule (INFERENCE). Per-entry vs per-invocation determination differ here |
| **TSA** | Preserved under every candidate |
| **D-5** | No candidate makes any D-5 strategy impossible; several D-5 strategies *require* a D-7 mechanism |
| **Replay / reporting** | Every candidate creates conditions the documented exit-code contract cannot express — handed to D-6 |

## 5. Status

```
D-7 STATUS: DECISION-READY WITH ONE BLOCKING EVIDENCE GAP

Decision space prepared:
    30-question register (D7-Q-001 … D7-Q-030)
    7 candidate mechanisms, viability assessed against evidence
    12 security models
    consequence matrix, dependency graph, TSA/Merkle and replay impact

Decisions selected:            NONE
Normative semantics selected:  NONE
Versioning strategy selected:  NONE
Discriminator selected:        NONE
Production code changed:       NO
Fixtures created:              NO
SPEC-002 changed:              NO
ADR created:                   NO
Recommendations:               NONE
Human decision required:       YES
Independent review required:   YES
```

**Basis for DECISION-READY.** The mechanism space is closed and each candidate
carries all fourteen required attributes; the security models are complete; the
dependency graph is evidenced in both directions where bidirectional; and the
external gaps are statements of fact only the operator can supply.

**Basis for the qualifier.** **EG-1 blocks one register question outright.**
D7-Q-018 — *can a new entry be made to appear as an old entry?* — cannot be
answered without the accepted D-3 values. If the new rule leaves the nine-field
preimage intact and carries a separate component, a legacy verifier could verify
a new record **successfully while ignoring the violations binding entirely** — a
silent loss of the D-1 property. If the new rule alters the preimage, the
exposure does not arise. This package **may not** infer which, and does not.

**EG-1 is closable immediately** from the governance record — it is a
restatement, not an investigation.

## 6. What becomes possible after D-7 closes

- D-5 gains the six inputs listed in `05_…` §3.1 and can move from prepared to
  selectable, subject to G-1/G-2/G-3.
- The reference model's sixth element, **Version selection**, becomes writable
  (`07_…` §1).
- D-6 can define reporting for the conditions D-7 makes possible.
- The specification set in D7-Q-029 becomes completable.

## 7. What remains blocked in D-5

Unchanged by this package: **G-1** (do production v1 logs exist), **G-2**
(external reliance), **G-3** (retention obligations), plus the concrete boundary
and the disposition of existing TSA evidence (`05_…` §3.2). None was closable
from the repository.

## 8. What must not happen yet

No implementation; no `schema` value chosen or bumped; no digest-version
identifier; no hash-domain tag allocated; no change to `chain.rs`, `models.rs`,
`segment.rs`, `sealer.rs`, the verifier, replay or migration tooling; no
fixtures or golden vectors; no ADR establishing D-7; no exit-code change; no
D-5 selection; and no D-3/D-4 semantic value invented to unblock EG-1.

## 9. Decision record — to be completed by the Authority

| Field | Value |
|---|---|
| Is a discriminator required? (D7-Q-001) | |
| Candidate / combination | |
| Discriminator location (D7-Q-003) | |
| Protection status (D7-Q-004) | |
| Behaviour: absent / unknown / malformed / newer / older | |
| Downgrade-resistance requirement (D7-Q-016) | |
| Resolution of EG-1 (D-3 values restated) | |
| Granularity: per entry / per corpus | |
| Decided by (HAA) | |
| Independent Reviewer | |
| Date | |
| Authority basis | |

---

*No normative effect. No decision recorded. No production code modified; no file
in `aura-guard-v1.3` created, modified or deleted; all evidence obtained by
inspection of a pristine read-only clone pinned at `443f72e`.*
