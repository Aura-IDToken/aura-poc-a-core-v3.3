# 06 — D-7 Evidence Requirements

What is not known, what it blocks, what would close it. **No gap is filled by
assumption.**

---

## 1. Blocking gap

### EG-1 — The accepted D-3 / D-4 semantic values were not supplied

- **What is missing.** D-3 and D-4 are CLOSED as decision domains, but this
  package was given only that fact, not the accepted values. In particular: does
  the new rule alter the nine-field preimage, or add a separate component
  alongside it?
- **What it blocks.**
  - **D7-Q-018** (can a new entry be made to appear old?) — cannot be answered.
    If the new rule leaves the nine-field preimage intact and carries a sibling
    digest, a legacy verifier could verify a new record successfully **and ignore
    the violations binding entirely** — a silent loss of the D-1 property. If the
    new rule changes the preimage, old-rule verification fails and the exposure
    does not arise.
  - **Candidate B** feasibility (can the representation carry a bound marker?).
  - **Candidate D** mechanics (can a domain tag be bound?).
  - **Candidate E** safety (its accept rule is "some generation verifies").
  - **Candidate G** observability (is the new generation structurally distinct?).
- **What would close it.** Restatement of the accepted D-3 (and, for candidate G,
  D-4) values from the governance record.
- **Closable by.** Governance record — **not** by inspection, and **not** by
  inference. The task forbids inventing or inferring them.
- **Status.** **EVIDENCE GAP — BLOCKING for one register question and for the
  full evaluation of three candidates.** Recorded as a stop-condition-adjacent
  item: preparation continued around it, and no D-3/D-4 semantics were selected.

## 2. External-fact gaps (carried forward, none closed)

| ID | Question | Blocks | What would close it |
|---|---|---|---|
| **G-1** | Do real production v1 logs exist, in what volume, over what `seq` range? | D7-Q-023; D-5 selection; the operational viability of C, F, G-`seq` | Operator statement of deployment state |
| **G-2** | Are logs externally relied upon (customers, auditors, integrators)? | D7-Q-024; whether out-of-band context (C/F) can be distributed; verifier-agreement requirements (`04_…` §6) | Operator / commercial statement |
| **G-3** | Retention obligations, and for how long? | D7-Q-025; how long a legacy verifier family (F) must remain maintained | Legal / compliance statement |
| **G-4** | Have RFC 3161 tokens been obtained **in production**, beyond the two in-repo fixtures? | D7-Q-022; the real-world weight of TSA continuity | Operator statement on TSA usage |

## 3. Definitional gaps the Authority must supply

| ID | Question | Why evidence cannot answer it |
|---|---|---|
| **EG-2** | Is verifier agreement across independent parties a requirement for the **entry** digest? | The repository documents this intent for the Merkle layer only — "verifiable with any off-the-shelf CT tooling" (quotation, `src/merkle.rs:1–5`) — CONFIRMED; there is no equivalent statement for the entry digest |
| **EG-3** | May the documented exit-code contract gain a new code? | `docs/exit-codes.md` is framed as "the contract that SOC playbooks, supervisors and CI should be wired against" (quotation) — changing it is a decision, not a discovery |
| **EG-4** | Is trial verification an acceptable accept-rule? | It necessarily accepts whichever supported generation verifies (`04_…` §2); acceptability is a policy judgement |
| **EG-5** | Is serde's ignore-unknown-fields behaviour intended or incidental? | `AuditEntry` carries no `deny_unknown_fields` (`src/models.rs:50–97`) — CONFIRMED — but no source states whether that is a deliberate compatibility posture. **NORMATIVE STATUS UNRESOLVED** |
| **EG-6** | Does a digest-domain change constitute a "protocol version" bump in the sense of `src/crypto.rs:25`? | The doc-comment states the genesis "must never be changed without bumping the protocol version" (quotation) — its scope is undefined. Also raised as D3-Q-014 in the D-3/D-4 package |
| **EG-7** | Is log write access constrained operationally? | A deployment property, not a code property; bears on D7-Q-005 |

## 4. Established facts — not gaps

Recorded so they are not re-investigated. All CONFIRMED at
`aura-guard-v1.3` @ `443f72e`.

| Question | Answer | Cite |
|---|---|---|
| Is `schema` persisted? | Yes, as an inline literal | `src/api/audit.rs:132` |
| Is `schema` inside the digest? | No | `src/chain.rs:25–49` |
| Does any verifier read `schema`? | No | `src/log_writer.rs:151–170`; `src/chain.rs:71–92` |
| Is `schema` caller-supplied? | No — server-side literal | `src/api/audit.rs:132` |
| Does a schema-rejection precedent exist? | Yes, segment path only | `src/segment.rs:341–342`; `src/sealer.rs:100` |
| Is the manifest `schema` inside the segment preimage? | No | `src/segment.rs:91–106` |
| Does `AuditEntry` reject unknown fields? | No — no `deny_unknown_fields` | `src/models.rs:50–97` |
| What happens on a missing required field? | Deserialization fails → `AuraError::PolicyParse` → exit `1` | `src/log_writer.rs:163–166`; `docs/exit-codes.md` |
| Does a version string exist anywhere bound to the chain? | Yes — genesis constants embed `v1.3` and `v1` | `src/crypto.rs:27–30`; `src/segment.rs:45–49` |
| Does domain separation exist? | Yes, Merkle layer only (`0x00`/`0x01`); no third-domain convention | `src/merkle.rs:9–15` |
| Is there an externally-selected verification-mode precedent? | Yes — `--tsa-roots` strict vs imprint-only, with a stderr warning | `src/bin/aura_seal.rs:90–96`, `:338–365`; `docs/segments-and-timestamping.md` |
| Do real RFC 3161 tokens exist in-repo? | Yes — two FreeTSA tokens with anchors | `tests/fixtures/tsa/`; `tests/tst_verify.rs` |
| Do audit-log fixtures exist? | No `.jsonl` anywhere in the repository | `find` — CONFIRMED |
| Is there algorithm agility? | No — SHA-256 throughout | `src/crypto.rs`; `src/merkle.rs` |
| Does ADR-0001 enumerate the protected fields? | No — "canonical fields incl. `prev_hash`" | `docs/adrs/0001-hash-chain.md` |

## 5. Effect on readiness

| Aspect | Effect |
|---|---|
| **Mechanism space** | Complete. Seven candidates, viability assessed against evidence, none ruled out, four fully evaluable now |
| **Security models** | Complete for eleven of twelve; the twelfth (downgrade severity) is bounded by EG-1 |
| **Dependency graph** | Complete and evidenced in both directions where bidirectional |
| **Candidate selection** | **Not responsibly possible for B, D and E until EG-1 closes**, and not operationally assessable for C, F and G-`seq` until G-1/G-2/G-3 close |

**Consequence.** D-7's decision *space* is prepared. D-7's *decision* has one
internal blocker (EG-1) that is closable immediately from the governance record,
and three external blockers (G-1/G-2/G-3) shared with D-5.
