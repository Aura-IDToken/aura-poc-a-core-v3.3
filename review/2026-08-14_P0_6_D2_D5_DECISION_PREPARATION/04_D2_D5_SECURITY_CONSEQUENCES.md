# 04 — D-2 / D-5 Security Consequences

**Status:** analysis only. No mitigation proposed, no design selected, no
implementation. Questions are identified and their consequence surfaces mapped;
they are not answered.

Classification legend: see `00_SCOPE_AND_DECISION_CONTEXT.md` §4.

---

## A. Downgrade risk

**The question.** If a verifier supports more than one integrity rule, can an
actor cause a record produced under the new rule to be verified under the older,
weaker rule — and thereby restore the pre-D-1 property that `violations` is
unprotected?

**Current architecture — CONFIRMED.**

- Exactly one rule exists and it is hard-coded: `recompute_for_entry`
  (`src/chain.rs:53–65`) always calls `compute_chain_hash` with the same nine
  fields. There is no rule selection, therefore no downgrade surface today.
- No field is consulted to choose a verification path
  (`src/log_writer.rs:151–170`, `src/chain.rs:71–92`).

**Consequence by candidate approach** — each is a NON-NORMATIVE CANDIDATE:

| Approach | Downgrade surface |
|---|---|
| Single rule only (D-5-B/C/D shapes) | None from rule selection — there is one rule. Risk relocates to whatever performs legacy handling or migration |
| Two rules selected by an **unprotected** in-band field | A writer who can edit the log can also edit the selector. Rewriting the selector to the legacy value causes the record to be verified under a rule that does not cover `violations` — the D-1 property is defeated without breaking any digest, because the selector is not in any digest (`src/chain.rs:25–49`) |
| Two rules selected by a **protected** in-band field | Editing the selector breaks the digest that covers it. The residual question becomes bootstrapping: the verifier must decide which rule to apply *in order to check* the field that says which rule applies |
| Two rules selected **out-of-band** (operator flag, path, archived binary) | No in-record surface; the risk becomes operational — whoever controls invocation controls the rule |

**The unresolved question.** Is a multi-rule verifier acceptable at all, and if
so, what makes rule selection non-influenceable by an actor with log write
access? **OPEN — D-5, with a dependency on D2-Q11.**

---

## B. Discriminator integrity

**The question.** If `schema` (or any other field) is used as the discriminator,
is that discriminator itself protected?

> This section deliberately does **not** answer "yes, it should be protected."
> That is D-2's decision (D2-Q1, D2-Q11).

**Current architecture — CONFIRMED.**

- `schema` is stored per entry as an inline literal `"aura-guard.audit.v1"`
  (`src/api/audit.rs:132`), with no named constant.
- It is **outside the digest** (`src/chain.rs:25–49`).
- It is **read by no code** on the audit path (`src/log_writer.rs:151–170`;
  `src/chain.rs:71–92`).
- The segment path shows the opposite arrangement: `SEGMENT_SCHEMA` is checked
  and rejected on mismatch (`src/segment.rs:341–342`; `src/sealer.rs:100`) —
  though a manifest's `schema` is likewise not covered by the segment preimage
  (`src/segment.rs:91–106`), so the precedent covers *checking*, not *protecting*.

**Consequence of each candidate approach:**

| Candidate | Consequence |
|---|---|
| Discriminator outside the integrity domain | It remains freely rewritable. Any verification behaviour keyed on it inherits that mutability. Consistent with today's architecture; it makes the selector a trust input that nothing vouches for |
| Discriminator inside the integrity domain | Rewriting it invalidates the entry digest. Introduces a bootstrapping order: the digest cannot be checked without first knowing the rule, and the rule is stated by a field inside the digest. Resolvable in principle — e.g. trial verification, or a rule fixed by position rather than content — but the resolution is a design decision, not a given |
| No discriminator; boundary by `seq` or by file | Nothing in the record to forge; the boundary becomes external state that must itself be trustworthy and distributed to every verifier |
| Discriminator + separate authentication (e.g. signed manifest of boundaries) | Moves trust to a second artifact, whose own integrity and distribution then require definition |

**The unresolved question.** Does the protected domain include the field that
discriminates the protected domain? **OPEN — D2-Q11.**

---

## C. Legacy ambiguity

**The question.** Can a verifier distinguish (i) genuine legacy v1 data, (ii)
malformed new data, and (iii) intentionally downgraded data?

**Current architecture — CONFIRMED.** No. Under one hard-coded rule, all three
present identically: `recompute_for_entry` returns a value unequal to the stored
`chain_hash`, and `verify_chain` reports a chain break
(`src/chain.rs:71–92`; `src/bin/aura_replay.rs:113–119`, exit code `2`). The
error carries no discrimination between "old format", "corrupt", and "tampered".

**IMPLEMENTATION-DERIVED consequence.** After any rule change, a legitimate v1
entry and a maliciously altered v2 entry produce the **same** verifier outcome.
This is the silent-misattribution property in `02_...` §5 point 4. It is a
property of the current verifier design, not a defect claim.

**Consequence by candidate approach:**

| Candidate | Distinguishes legacy? | Distinguishes malformed? | Distinguishes downgraded? |
|---|---|---|---|
| No discriminator | No | No | No |
| Unprotected discriminator | Yes, if honest — but an attacker can *claim* legacy | Partially | **No** — a downgrade presents as legacy by construction |
| Protected discriminator | Yes | Yes (digest fails) | Yes, subject to §B bootstrapping |
| Out-of-band boundary | Yes, to a verifier that has the boundary | Yes | Depends on boundary integrity |

**The unresolved question.** Must these three cases be distinguishable, and must
they be *reported* distinguishably (distinct exit codes / error classes)? The
second half is D-6. **OPEN.**

---

## D. Replay

**The question.** Can the replay engine determine which rule applies?

**Current architecture — CONFIRMED.** No, and it does not try. `aura-replay`
applies `verify_chain` unconditionally (`src/bin/aura_replay.rs:113`), then
optional lineage checks (`:134–153`), `verify_segment_chain` (`:175`) and
`verify_manifest_against_entries` (`:194`). No branch anywhere depends on an
entry's `schema` or on any version input.

**IMPLEMENTATION-DERIVED consequences of a rule change, per replay stage:**

| Stage | Effect | Cite |
|---|---|---|
| `read_all_entries` | Unaffected — parsing is version-agnostic; an unknown extra field would be handled by serde's defaults, an absent required field would fail to deserialize | `src/log_writer.rs:151–170` |
| `verify_chain` | Fails on every pre-change entry unless rule selection exists | `src/chain.rs:53–65` |
| lineage (`--verify-lineage`) | Unaffected by the digest change itself; it compares `policy_hash` against on-disk policy | `src/bin/aura_replay.rs:149–153` |
| `verify_segment_chain` | Unaffected by the entry digest; it checks manifest-to-manifest continuity | `src/segment.rs:335–342` |
| `verify_manifest_against_entries` | Fails on every pre-change segment — it recomputes the Merkle root from entry `chain_hash` values | `src/segment.rs:394`, `:401` |

**The unresolved question.** Which component owns rule selection — the library
(`verify_chain`), the CLI, or the caller — and what does replay report when a log
spans a boundary? **OPEN — D-5 and D-6 jointly.**

---

## E. Audit continuity

**The question.** Does a version transition preserve historical verifiability,
chain continuity, Merkle continuity, segment continuity, and TSA evidence?

| Property | Current mechanism | Effect of a digest change | Tag |
|---|---|---|---|
| **Historical verifiability** | `recompute_for_entry` over stored fields | Lost for pre-change entries unless the old rule remains available (D-5-A/E) | CONFIRMED |
| **Chain continuity** | `prev_hash` linkage checked per entry (`chain.rs:71–92`) | Preserved *in form* — `prev_hash` remains a 64-char hex value and the linkage still checks — but the two sides of a boundary are computed under different definitions. Continuity of *form* is not continuity of *meaning* | CONFIRMED |
| **Merkle continuity** | `segment_merkle_root` over `entry_leaf_hash` (`segment.rs:140–158`) | Broken for pre-change segments: recomputation yields a different root | CONFIRMED |
| **Segment continuity** | `verify_segment_chain` checks `prev_segment_chain_hash` / `prev_merkle_root` manifest-to-manifest (`segment.rs:335+`) | Manifest-to-manifest linkage is unaffected by the entry rule; but a manifest whose `merkle_root` no longer matches its entries fails `verify_manifest_against_entries` even while the segment chain itself verifies. **The two checks can disagree** | CONFIRMED |
| **TSA evidence** | `verify_tsr` against the imprint from `segment_chain_preimage` (`src/tst_verify.rs:393`; `tests/tst_verify.rs:25–33`) | Unaffected if sealed history is left untouched (D-5-A/B/D/E). **Irrecoverably invalidated by re-sealing** (D-5-C): a token attests a past instant and cannot be re-issued for it | CONFIRMED |

**Concrete, not hypothetical — CONFIRMED.** Two real FreeTSA tokens exist in-repo
(`tests/fixtures/tsa/segment-00{1,2}.tsr`) over imprints descending from v1
`chain_hash` values, sealed `2026-05-20`. Continuity of TSA evidence is therefore
a present concern, not a future one (`02_...` §6.4, §6.9).

**The unresolved question.** Which continuity properties are **requirements** and
which are merely desirable? The evidence establishes what each strategy does to
each property; it cannot establish which properties the Authority requires.
**OPEN — D-5.**

---

## F. Consolidated open security questions

| ID | Question | Owner |
|---|---|---|
| S-1 | Is a multi-rule verifier acceptable, and how is rule selection made non-influenceable by a log writer? | D-5 |
| S-2 | Is the version discriminator itself inside the integrity domain? | D-2 (D2-Q11) |
| S-3 | If the discriminator is protected, how is the bootstrap ordering resolved? | D-2 / D-7 |
| S-4 | Must legacy / malformed / downgraded be distinguishable — and reported distinguishably? | D-5 / D-6 |
| S-5 | Which component owns rule selection, and what does replay report at a boundary? | D-5 / D-6 |
| S-6 | Which continuity properties (historical, chain, Merkle, segment, TSA) are requirements? | D-5 |
| S-7 | Is destroying existing RFC 3161 evidence admissible if D-5-C is chosen? | D-5 |

None is answered here.
