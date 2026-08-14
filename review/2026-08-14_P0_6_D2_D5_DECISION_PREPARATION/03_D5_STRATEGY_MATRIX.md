# 03 — D-5: Strategy Classes and Comparison Matrix

**Decision:** D-5 — *How are existing v1 logs handled after a chain-hash change?*
**Status:** OPEN. **No strategy is selected, ranked, preferred or recommended.**

Classification legend: see `00_SCOPE_AND_DECISION_CONTEXT.md` §4.
Baseline evidence: `02_D5_V1_COMPATIBILITY_ANALYSIS.md`.

> All five classes are presented in label order. Label order is not an ordering
> of merit. In particular **D-5-E is analysed exactly as the others are** — it is
> a NON-NORMATIVE CANDIDATE and is not characterised as simplest, safest,
> cleanest, preferred, recommended or correct.

---

## 1. Strategy classes

### D-5-A — Legacy preservation

Old logs remain verifiable under the old integrity rule; new logs use the new
rule. Both rules remain implemented; the verifier must determine which to apply.

- **How the rule is chosen is not specified by this class** — it is the open
  question that separates D-5-A from D-5-E (which makes the discriminator
  explicit). D-5-A admits out-of-band selection: operator flag, file path
  convention, archived binary, or a sealed cut-over record.
- **Requires:** two verification paths coexisting; a selection mechanism.
- **Preserves:** historical verifiability, Merkle continuity, existing TSA tokens.

### D-5-B — New version only

Existing v1 logs are not accepted by the new verifier; verifying them requires
explicit legacy handling (a separate tool, a pinned old binary, or a documented
archival procedure).

- **Requires:** a stated position on what "explicit legacy handling" means and
  who retains the capability.
- **Preserves:** nothing automatically; historical verifiability becomes an
  operational responsibility rather than a product property.

### D-5-C — Migration / re-sealing

Existing logs are transformed: entry digests recomputed under the new rule,
segments re-sealed, manifests rewritten.

- **CONFIRMED mechanics.** Re-derivation is possible in principle because the
  full entry — `violations` included — is retained on disk
  (`src/log_writer.rs:96`; `02_...` §6.8).
- **CONFIRMED constraint.** Re-sealing changes `merkle_root`
  (`src/segment.rs:151–158`), which changes the segment preimage and therefore
  the TSA imprint (`:91–131`). An RFC 3161 token attests a specific imprint at a
  specific past instant and **cannot be re-issued for that instant**. Existing
  tokens — including the two in-repo fixtures (`02_...` §6.4) — do not survive
  re-sealing.
- **Requires:** a position on the destruction of existing timestamp evidence, and
  on whether rewriting an append-only audit artifact is admissible at all.

### D-5-D — Reject legacy

The new verifier intentionally refuses v1 logs — a deliberate, explicit failure
rather than a silent one.

- **Requires:** the verifier to *detect* that a log is v1. Per `02_...` §3.6–3.7
  no in-band trusted discriminator exists today, so this class still needs a
  detection mechanism; without one, "reject legacy" is indistinguishable at
  runtime from "fail on tampered data".
- **Preserves:** unambiguous verifier semantics; no dual-rule surface.

### D-5-E — Hybrid version-discriminated verification

Old logs verify under the old rule, new logs under the new rule, and the verifier
selects the rule using an **explicit discriminator**.

- **Distinguishing property:** the selection mechanism is in-band and named,
  rather than out-of-band (D-5-A) or absent (D-5-B/D).
- **Requires:** a discriminator; a decision on whether that discriminator is
  itself inside the integrity domain (D2-Q11, and `04_...` §B); a rule for
  entries whose discriminator is missing, unknown, or malformed.
- **CONFIRMED constraint.** The natural candidate discriminator, `schema`, is
  currently unprotected and unread (`02_...` §3.2, §3.6). Using it as-is means
  selecting a verification rule from an attacker-writable field — the downgrade
  question in `04_...` §A. This is a property of the class, not an argument
  against it; the class can also be instantiated with a protected discriminator.
- **Precedent, not endorsement.** The segment path already rejects on schema
  mismatch (`src/segment.rs:341–342`; `src/sealer.rs:100`). That establishes the
  pattern exists in the codebase; it establishes nothing about whether it is
  appropriate for the entry path.

---

## 2. Comparison matrix

All cells are evidence-derived where a citation is given, and marked
**[inference]** where they are reasoned rather than observed. No column is a
score, and no row is a ranking.

| Strategy | Existing logs | New logs | Verifier complexity | Migration cost | Backward compatibility | Security risk | Downgrade risk | Replay impact | Operational impact | Evidence | Open questions |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **D-5-A** Legacy preservation | Remain verifiable under the old rule; digests, Merkle roots and TSA tokens untouched | New rule from a boundary | Two rule paths must coexist and stay correct **[inference]** | None to the data; cost is in the verifier **[inference]** | Full, if selection is reliable | Two live rules = a larger verification surface **[inference]** | **Present** — wherever rule selection is influenceable; unspecified selection is the class's weak point | `aura-replay` gains rule selection; exit-code semantics become D-6 | Old binaries/tools may remain in use **[inference]** | `02_...` §3.7, §4.4 | How is the rule selected? Who is authoritative for the boundary? |
| **D-5-B** New version only | Not accepted by the new verifier; need explicit legacy handling | New rule only | Single rule in the new verifier **[inference]** | None to the data; cost shifts to operations **[inference]** | None automatic | Legacy verification capability may decay if the old tool is lost **[inference]** | Low within the new verifier (one rule); the risk moves to whatever performs legacy handling **[inference]** | Replay of old logs is out of scope for the product | Requires retaining or documenting a legacy path | `02_...` §5 | What is "explicit legacy handling", and who owns it? |
| **D-5-C** Migration / re-sealing | Rewritten under the new rule | New rule only | Single rule **[inference]** | **Highest** — recompute every digest, re-seal every segment, rewrite every manifest | Achieved by transforming history rather than preserving it | Rewriting an append-only audit artifact is itself an integrity event **[inference]** | Low post-migration (one rule) **[inference]** | Uniform after migration | Requires a controlled, auditable rewrite of the audit corpus | `02_...` §6.8; `src/segment.rs:91–158` | Is destroying existing TSA evidence acceptable? Is rewriting an audit log admissible? Who witnesses the migration? |
| **D-5-D** Reject legacy | Refused | New rule only | Single rule, plus detection **[inference]** | None to the data | None, by design | Explicit refusal removes silent misattribution **[inference]** | Low (no second rule to select) **[inference]** | Old logs cannot be replayed by the shipped tool | Historical verifiability is lost unless archived externally | `02_...` §3.6 | How does the verifier *detect* v1 without a trusted discriminator? |
| **D-5-E** Hybrid discriminated | Verify under the old rule, selected in-band | New rule, selected in-band | Two rule paths **plus** discriminator handling **[inference]** | None to the data | Full, conditional on discriminator trustworthiness | Depends entirely on whether the discriminator is protected — see `04_...` §B | **Central question of this class**: with an unprotected discriminator, downgrade is available (`02_...` §3.2); with a protected one, the risk changes shape rather than vanishing | Replay must branch on the discriminator (D-6) | Requires a defined response to missing/unknown/malformed discriminators | `02_...` §3.2, §3.4, §3.6 | Is the discriminator protected? What happens on absent/unknown values? Is `seq`-boundary an acceptable substitute? |

---

## 3. Cross-cutting observations

**IMPLEMENTATION-DERIVED.** Three properties hold across all five classes and are
therefore not differentiators:

1. **Full entry data is on disk.** `violations` is persisted verbatim
   (`src/log_writer.rs:96`), so no class is blocked by missing input data.
2. **TSA tokens are asymmetric.** Any class that changes `merkle_root` for a
   sealed segment invalidates the token over it irrecoverably (`02_...` §6.4,
   §6.8). Classes A, B, D, E leave sealed history untouched; C does not.
3. **Detection is required by more classes than it appears.** B and D read as
   "no dual rule needed", but both still require the verifier to *recognise* a v1
   log to behave correctly — the same discriminator problem E makes explicit.

**Scope boundary.** If D-2 resolves such that `compute_chain_hash` is left
unchanged (a sibling-digest shape, D2-Q12), the premise of D-5 narrows sharply:
existing digests remain reproducible and the question becomes how the *new*
artifact behaves on entries that lack it, rather than how old entries verify. The
two decisions are therefore coupled; see `05_D2_D5_DEPENDENCY_GRAPH.md`.

**EVIDENCE GAP.** Whether any of these classes is *operationally* viable depends
on facts not determinable from the repository: existence of production logs,
external reliance, and retention obligations (`02_...` §6.5–6.7). A strategy
cannot be responsibly chosen while those remain open — see
`06_D2_D5_EVIDENCE_REQUIREMENTS.md`.
