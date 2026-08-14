# 04 — D-7 Security Analysis

The twelve required threat models. **No attack is claimed unless the evidence
establishes it.** Each item states the current architecture, what the evidence
supports, and the per-candidate consequence — without selecting a candidate.

Status labels per `00_…` §4. `NORMATIVE CONFLICT` is used only where two sources
**both of confirmed normative status** disagree; no such case was found in D-7,
and none is asserted.

---

## 1. Discriminator tampering

**Current architecture — CONFIRMED.** `schema` is persisted
(`src/api/audit.rs:132`), outside the digest (`src/chain.rs:25–49`), and read by
no verifier (`src/log_writer.rs:151–170`; `src/chain.rs:71–92`). Editing it today
changes nothing, because nothing consumes it.

**What the evidence establishes.** An actor able to write the log can alter
`schema` without invalidating any digest — CONFIRMED, mechanically, from the
three citations above. **This is not yet an attack**, because no code reads the
field. It becomes one only if a future design makes verification depend on it
while leaving it unbound.

**Per candidate.** A: tampering is fully available. B/D: tampering breaks the
digest. C/F: no in-record target. E: no target, but see §2. G: no label to edit,
though structure can still be altered by removing data.

## 2. Downgrade

**Current architecture.** Vacuous today — one hard-coded rule
(`src/chain.rs:53–65`), no selection. **CONFIRMED.**

**What the evidence establishes.** Post-transition, whether downgrade is
available is a property of the selection mechanism:

- **Unprotected in-band selector (A):** available by construction — the actor
  edits the selector, the verifier applies the weaker rule, and no digest breaks
  (§1) — **CONFIRMED** as a mechanical property.
- **Bound selector (B/D):** editing breaks the digest; the residual is the
  bootstrap ordering — a verifier must choose a rule before it can validate the
  field naming the rule (D7-Q-006).
- **Trial verification (D/E):** the accept rule is "some supported generation
  verifies", so downgrade succeeds **iff a new-generation record can also satisfy
  the legacy rule** — that is D7-Q-018, **blocked on EG-1**.
- **External selection (C/F):** no in-record surface; the risk is whoever
  controls invocation or artifact choice.
- **Structural (G):** removing a new-generation field is the downgrade primitive;
  whether it succeeds depends on EG-1.

**INFERENCE.** Downgrade resistance is not a property any candidate has
automatically. It must be specified as a requirement and then satisfied.

## 3. Upgrade / forward-version confusion

**What the evidence establishes.** An old-rule record presented as
new-generation would be recomputed under the new rule. Because D-1 mandates
`violations` in the domain and they are absent from the old digest
(`src/chain.rs:25–49`) — CONFIRMED — the recomputation would not reproduce the
stored value.

**INFERENCE.** The upgrade direction appears self-limiting: it yields a
verification failure, not a false accept. It is therefore a denial or confusion
vector rather than an evidence-forging one. This holds only while the new rule
genuinely differs in inputs from the old — which D-1 guarantees.

**Per candidate.** B/D fail closed. A/C/F/G: behaviour on a "newer than
supported" claim is **undefined by the candidate** and must be specified
(D7-Q-014). E: no generation verifies → failure.

## 4. Algorithm confusion

**Current architecture — CONFIRMED.** One hash function throughout: SHA-256, via
`sha256_hex` (`src/crypto.rs:8–12`) and `sha256_bytes_hex` (`:16`); the Merkle
layer uses RFC 6962 `0x00`/`0x01` domain separation with an explicit
second-preimage rationale (`src/merkle.rs:9–15`). **No algorithm agility exists
anywhere in the codebase** — CONFIRMED.

**What the evidence establishes.** There is no algorithm-selection surface today,
so no algorithm-confusion attack exists. **INFERENCE:** if D-7 introduces
generation selection that could later carry an algorithm choice, the same
downgrade reasoning in §2 would apply to it. **Recorded as a property to be
avoided or accepted deliberately, not as a present vulnerability.**

**Note.** `merkle.rs:9–15` documents domain separation as defeating
"second-preimage attacks where a node hash could otherwise be passed off as a
leaf hash" (quotation). No equivalent protection exists at the entry-digest layer
— CONFIRMED, and relevant to candidate D.

## 5. Ambiguous interpretation

**Current architecture — CONFIRMED.** Three distinct conditions collapse to one
outcome today: a legitimately old record, a corrupt record, and a tampered record
all produce a `verify_chain` mismatch → exit `2`
(`src/bin/aura_replay.rs:113–119`; `docs/exit-codes.md`).

**What the evidence establishes.** Post-transition this ambiguity widens unless
the design distinguishes the cases. A fourth condition joins them: a record whose
*structure* does not match the verifier's expectation fails at the **parse** stage
instead, returning `AuraError::PolicyParse` (`src/log_writer.rs:163–166`) → exit
`1` — CONFIRMED. So a version mismatch may surface as "malformed log", which
names the wrong problem.

**Per candidate.** Every candidate must specify D7-Q-011 … D7-Q-015. G inherits
the parse-path diagnostic described above.

## 6. Verifier disagreement

**What the evidence establishes.** Today all verifiers necessarily agree — there
is one rule. **INFERENCE:** any multi-rule design admits disagreement between
verifiers that support different generation sets, or apply a different accept
policy.

**Sharpest under C, F and E.** C and F make the rule an operational choice, so
two honest verifiers can legitimately reach different conclusions on the same
file. E makes "any supported generation verifies" the accept rule, so verifiers
supporting different generation sets will disagree by construction.

**Evidence required.** Whether verifier agreement across independent parties is a
requirement — related to G-2 and to the entry-layer analogue of the Merkle
layer's documented "verifiable with any off-the-shelf CT tooling" intent
(quotation, `src/merkle.rs:1–5`) — **EVIDENCE GAP**.

## 7. Replay ambiguity

**Current architecture — CONFIRMED.** `aura-replay` prints `CHAIN OK` on success
(`:213`) and returns `2` on a break (`:113–119`); no output names a generation.

**What the evidence establishes.** Under any multi-generation design, `CHAIN OK`
becomes under-specified: it does not say *under which rule* the log verified. A
log spanning a boundary has no defined single outcome today.

**Per candidate.** E must report which generation succeeded, or the result is
uninterpretable. C and F must report the selected mode — F11 shows the project
has previously handled exactly this with a stderr warning for the weaker mode
(`src/bin/aura_seal.rs:365`) — CONFIRMED.

## 8. Legacy-log ambiguity

**What the evidence establishes.** Legacy entries carry
`"aura-guard.audit.v1"` (`src/api/audit.rs:132`) that nothing reads, and no
audit-path code branches on any version — CONFIRMED. So a legacy log is today
identifiable only by inspection, not by the tooling.

**Consequence.** A design that treats "unmarked or v1-marked" as legacy makes
marker removal or retention a downgrade primitive (§2). A design that treats
legacy as invalid rejects every existing record — a D-5 outcome, not a D-7 one.

## 9. TSA continuity

**CONFIRMED.** Real RFC 3161 tokens exist in-repo
(`tests/fixtures/tsa/segment-00{1,2}.tsr`), verified in `tests/tst_verify.rs`
against an imprint recomputed from `SegmentManifest::segment_chain_preimage`
(`:25–33`), which derives from `merkle_root` → `chain_hash`
(`src/segment.rs:91–158`).

**What the evidence establishes.** **No D-7 candidate alters sealed history**
(`03_…` §4) — CONFIRMED. Token continuity is therefore preserved under every
candidate. The destruction scenario arises only from a re-sealing migration,
which is **D-5**. Detail in `08_…`.

## 10. Merkle continuity

**CONFIRMED.** `entry_leaf_hash` consumes only `chain_hash`
(`src/segment.rs:140–150`); the root consumes only leaves (`:151–158`);
`verify_manifest_against_entries` **recomputes** the root from entries
(`:394`) and compares `head_chain_hash_at_close` (`:401`).

**What the evidence establishes.** A segment whose entries were written under one
rule verifies only if the verifier recomputes their `chain_hash` under that same
rule. **A segment spanning a generation boundary therefore has no single rule
under which its root reproduces** — **INFERENCE** from the three citations, and
the structurally hardest case in D-7 (D7-Q-020). Detail in `08_…` §2.

## 11. Migration-induced verification failure

**What the evidence establishes.** Distinguish two failures:
(i) a verifier applying the wrong rule — a D-7 concern;
(ii) records changed by a migration — a D-5 concern.
Only (i) is in D-7's scope. Under every candidate, applying the wrong rule
produces a mismatch that today reports as exit `2` (F10) — CONFIRMED — i.e.
indistinguishable from tampering unless the design says otherwise.

## 12. Attacker-controlled schema / version fields

**CONFIRMED — a related, already-documented precedent.** The codebase already
treats one caller-supplied field as untrusted for a different reason: the
`policy_set` metric label is deliberately replaced with `"unknown"` because
"using it verbatim would allow unbounded metric label cardinality"
(quotation, `src/api/audit.rs:95–97`). `request_id` is likewise
length-bounded on extraction (`src/api/audit.rs:19`, `:25–29`) — CONFIRMED.

**What the evidence establishes.** `schema` is **not** caller-supplied — it is a
server-side literal (`src/api/audit.rs:132`) — CONFIRMED. So at write time it is
not attacker-controlled. It becomes attacker-controlled only **at rest**, by an
actor with log write access, which is the P0-6 threat model's premise.

**Consequence.** Any candidate placing trust in an at-rest, unbound field inherits
that exposure (§1). Any candidate binding it, or not using a field at all, does
not.

---

## 13. Summary of security findings

| # | Finding | Status |
|---|---|---|
| 1 | No downgrade surface exists **today** — there is only one rule | CONFIRMED |
| 2 | An unprotected in-band selector would create one by construction | CONFIRMED (mechanical) |
| 3 | The upgrade direction appears self-limiting | INFERENCE |
| 4 | The downgrade direction's severity depends on the accepted D-3 shape | **EVIDENCE GAP (EG-1)** — the single most consequential open item |
| 5 | Version problems can surface as "malformed log" (exit `1`), naming the wrong problem | CONFIRMED |
| 6 | Legacy / corrupt / tampered are indistinguishable in current reporting | CONFIRMED |
| 7 | No D-7 candidate endangers existing TSA tokens or Merkle roots | CONFIRMED |
| 8 | A segment spanning a generation boundary has no single reproducing rule | INFERENCE |
| 9 | No algorithm agility exists, so no algorithm-confusion attack exists today | CONFIRMED |
| 10 | `schema` is server-generated, not caller-supplied; the exposure is at rest, not at write | CONFIRMED |

**No NORMATIVE CONFLICT is asserted in D-7.** No two sources of confirmed
normative status were found to disagree on any question in this register.
