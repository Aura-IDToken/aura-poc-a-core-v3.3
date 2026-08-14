# 02 — D-7 Candidate Mechanisms

**Every entry is a NON-NORMATIVE CANDIDATE.** None is selected, ranked, or
characterised as recommended, preferred, best, safest, correct or simplest.
Letter order follows the task's enumeration and is not an ordering of merit.

Each candidate carries the fourteen required attributes. Baseline facts F1–F13
are defined in `01_…`. Repository/commit for all `src/…` citations:
`aura-guard-v1.3` @ `443f72e`.

**Viability was assessed, not assumed.** §8 records which candidates the evidence
supports and which it does not.

---

## A — Discriminator outside the digest

**NON-NORMATIVE CANDIDATE**

| Attribute | Content |
|---|---|
| **Exact mechanism** | A generation value carried in the record but not bound by any digest; the verifier reads it and selects a rule |
| **Where the discriminator lives** | In `AuditEntry`, e.g. the existing `schema` field (F2) or a new sibling field |
| **What the verifier reads** | The field value, before recomputation |
| **What is cryptographically bound** | **Nothing.** `schema` is outside the digest (F3) — CONFIRMED |
| **Legacy behaviour** | Existing entries already carry `"aura-guard.audit.v1"` (F2), so legacy is positively identifiable without rewriting any record |
| **New-entry behaviour** | Writer emits a different value |
| **Unknown-version behaviour** | Undefined by the candidate; must be specified (D7-Q-012) |
| **Downgrade exposure** | **Maximal and structural.** The selector is editable by any actor with log write access and editing it invalidates no digest (F3) — CONFIRMED. Rule selection becomes attacker-influenceable |
| **TSA impact** | None — sealed history untouched |
| **Replay impact** | `verify_chain` or its caller gains a branch on the field |
| **D-5 impact** | Leaves every D-5 strategy available; imposes no rewrite |
| **Implementation impact** | Smallest surface: one read plus a branch. `schema` already exists and is already persisted |
| **Required evidence** | Whether the deployment model constrains log write access (operational, **EVIDENCE GAP**) |
| **Unresolved assumptions** | That an unprotected selector is acceptable within the adopted threat model — **this is D7-Q-005, not an assumption this package may make** |

## B — Discriminator inside the digest

**NON-NORMATIVE CANDIDATE**

| Attribute | Content |
|---|---|
| **Exact mechanism** | The generation value becomes a component of the digest preimage; tampering with it invalidates the digest |
| **Where the discriminator lives** | In the record **and** in the preimage |
| **What the verifier reads** | The field, then validates it implicitly by recomputation |
| **What is cryptographically bound** | The generation value itself |
| **Legacy behaviour** | Existing v1 digests contain **no** marker (F1) — CONFIRMED — so legacy entries cannot be retro-marked without recomputing their digests, which is a rewrite |
| **New-entry behaviour** | Marker bound from the transition forward |
| **Unknown-version behaviour** | Must be specified; a bound unknown marker still fails recomputation under every supported rule |
| **Downgrade exposure** | Editing the marker breaks the digest. **Residual:** the bootstrap ordering (D7-Q-006) — the verifier must pick a rule before it can validate the field that names the rule |
| **TSA impact** | None for sealed history if legacy remains verifiable under the old rule; otherwise as D-5 |
| **Replay impact** | Requires trial verification or an external hint to resolve the bootstrap |
| **D-5 impact** | Legacy cannot self-identify; D-5 must supply the boundary by other means |
| **Implementation impact** | Requires the canonical representation to admit the marker — **depends on the accepted D-3 values, not available** (`06_…` EG-1) |
| **Required evidence** | EG-1 |
| **Unresolved assumptions** | That the accepted D-3 representation can carry a marker component |

## C — Version-specific verifier selected externally

**NON-NORMATIVE CANDIDATE**

| Attribute | Content |
|---|---|
| **Exact mechanism** | Generation is supplied by invocation context — a flag, a config value, a path convention, or a declared boundary — not read from the record |
| **Where the discriminator lives** | Outside the record entirely |
| **What the verifier reads** | Its own invocation parameters |
| **What is cryptographically bound** | Nothing in-record; the trust anchor is the invocation |
| **Legacy behaviour** | Operator points the legacy-mode verifier at legacy logs |
| **New-entry behaviour** | Symmetric |
| **Unknown-version behaviour** | Not expressible in-record; a mis-specified context yields a verification failure indistinguishable from tampering (**INFERENCE** from F4) |
| **Downgrade exposure** | No in-record surface. Risk relocates entirely to whoever controls invocation |
| **TSA impact** | None |
| **Replay impact** | The CLI already has the shape: **F11** — `aura-seal verify-tst` selects strict vs imprint-only verification from the presence of `--tsa-roots`, with a stderr warning, and the docs state "The strict mode is the production default" (quotation) — CONFIRMED |
| **D-5 impact** | Requires D-5 to define and publish the boundary; leaves data untouched |
| **Implementation impact** | Precedented in-repo (F11); no record-format change |
| **Required evidence** | **G-2** — whether every external consumer can be given the correct context (`06_…`) |
| **Unresolved assumptions** | That invocation context can be reliably distributed to all verifiers, including third parties |

## D — Self-describing digest / domain separation

**NON-NORMATIVE CANDIDATE**

| Attribute | Content |
|---|---|
| **Exact mechanism** | Each generation computes its digest in a distinct hash domain (e.g. a domain tag bound into the preimage), so a digest is only valid within its own generation |
| **Where the discriminator lives** | Implicit in the digest construction |
| **What the verifier reads** | Nothing declarative; it attempts a generation and observes success or failure |
| **What is cryptographically bound** | The domain tag, hence the generation |
| **Legacy behaviour** | Legacy digests have no tag (F1) — the untagged construction is itself generation-1's "tag" by absence |
| **New-entry behaviour** | Tagged |
| **Unknown-version behaviour** | Fails closed — an unrecognised domain cannot be reproduced |
| **Downgrade exposure** | A record cannot be re-labelled, because there is no label to edit. **Residual:** a verifier supporting multiple domains must still choose which to try (D7-Q-006, D7-Q-008) |
| **TSA impact** | None if sealed history is verified under its own domain |
| **Replay impact** | Trial verification across supported domains, or an external hint |
| **D-5 impact** | Leaves data untouched; the boundary can be discovered per record rather than declared |
| **Implementation impact** | Precedent exists **only** at the Merkle layer — RFC 6962 `0x00`/`0x01` with a stated second-preimage rationale (F9) — and **no convention exists for a third domain** (F9) — CONFIRMED. Requires D-3's representation to admit a tag |
| **Required evidence** | EG-1 (D-3 values); a tag-allocation convention, which does not exist |
| **Unresolved assumptions** | That trial verification is acceptable — it necessarily accepts whichever supported generation verifies |

## E — Dual / parallel verification on known protocol context

**NON-NORMATIVE CANDIDATE**

| Attribute | Content |
|---|---|
| **Exact mechanism** | The verifier attempts every supported generation and reports the outcome set — accept if any verifies, or report which one did |
| **Where the discriminator lives** | Nowhere; generation is *discovered*, not declared |
| **What the verifier reads** | Only the record and its own rule set |
| **What is cryptographically bound** | Whatever each generation binds; no separate selector exists |
| **Legacy behaviour** | Verifies under the legacy rule |
| **New-entry behaviour** | Verifies under the new rule |
| **Unknown-version behaviour** | No generation verifies → failure |
| **Downgrade exposure** | **Inherent to the mechanism:** a record that verifies under the legacy rule is accepted, whether or not it was written under it. If a new-generation record can also satisfy the legacy rule, the D-1 property is silently lost — this is exactly D7-Q-018, which is **blocked on EG-1** |
| **TSA impact** | None |
| **Replay impact** | Cost multiplies by the number of supported generations; reporting must state which generation succeeded, or the result is ambiguous |
| **D-5 impact** | No boundary needs to be declared, which is also why no boundary is enforced |
| **Implementation impact** | No format change; verifier complexity grows with generation count |
| **Required evidence** | **EG-1 — decisive.** Whether a new-generation record can satisfy the legacy rule depends on the accepted D-3 shape |
| **Unresolved assumptions** | That "any generation verifies" is an acceptable accept-condition |

## F — Explicit legacy / new verifier families

**NON-NORMATIVE CANDIDATE**

| Attribute | Content |
|---|---|
| **Exact mechanism** | Two separate verifier artifacts (binaries, library versions, or subcommands); each implements exactly one generation and refuses the other |
| **Where the discriminator lives** | In the choice of artifact — an operational, not a data, property |
| **What the verifier reads** | Only its own rule |
| **What is cryptographically bound** | Nothing additional |
| **Legacy behaviour** | The legacy artifact must be retained and remain runnable |
| **New-entry behaviour** | The new artifact refuses legacy records |
| **Unknown-version behaviour** | Failure, without diagnosis of *why* |
| **Downgrade exposure** | No in-record surface; risk is which artifact an operator runs. Distinct from C in that the rule set is fixed at build time rather than at invocation |
| **TSA impact** | None |
| **Replay impact** | Two tools to operate; `docs/exit-codes.md` is written as one contract across binaries (F10) and would need to cover both |
| **D-5 impact** | Requires an operational boundary; leaves data untouched |
| **Implementation impact** | No format change; long-term maintenance of a frozen legacy artifact |
| **Required evidence** | **G-3** (how long legacy verification must remain available) |
| **Unresolved assumptions** | That a frozen legacy artifact remains buildable and trustworthy for the retention period |

## G — Structural / genesis-anchored determination

**NON-NORMATIVE CANDIDATE** *(added because repository evidence supports it —
see §8)*

| Attribute | Content |
|---|---|
| **Exact mechanism** | Generation is determined from properties the record or chain already has, rather than from a declared value: (i) **structural shape** — which fields are present; (ii) **genesis anchoring** — the chain's genesis constant already embeds a version string; (iii) **corpus position** — a `seq` boundary corroborated by segment manifests |
| **Where the discriminator lives** | In the data's structure and in existing constants, not in a dedicated field |
| **What the verifier reads** | Field presence; the genesis value at chain head; `first_seq`/`last_seq` in manifests |
| **What is cryptographically bound** | The genesis value is bound transitively — it is the `prev_hash` of entry 0 (F7) and therefore inside every subsequent digest. Structural shape is not "bound" but is not editable without altering the data |
| **Legacy behaviour** | Legacy records are identified by lacking whatever the new generation adds |
| **New-entry behaviour** | Identified by carrying it |
| **Unknown-version behaviour** | Manifests as a parse failure, not a version error — **F5 is decisive**: with no `deny_unknown_fields`, a record missing a required field fails `serde_json::from_str`, and `read_all_entries` returns `AuraError::PolicyParse` (`src/log_writer.rs:163–166`) → exit `1` "runtime error / malformed log", **not** exit `2` (F10) — CONFIRMED |
| **Downgrade exposure** | A label cannot be forged because none exists. **But the asymmetry in F5 is a real exposure:** unknown *extra* fields are silently ignored, while *missing* fields are fatal. An actor removing a new-generation field turns a new record into something a legacy verifier may accept, subject to D7-Q-018 / EG-1 |
| **TSA impact** | None if history is untouched. Note the genesis constant's own doc-comment: it "must never be changed without bumping the protocol version" (quotation, F7) — a change to the genesis would itself re-root every chain |
| **Replay impact** | No declared value to branch on; the branch is on structure |
| **D-5 impact** | The `seq`-boundary variant needs D-5 to declare the boundary; the structural variant does not |
| **Implementation impact** | No new field. Depends on the accepted D-3/D-4 outcome producing an observable structural difference — **EG-1** |
| **Required evidence** | **EG-1**; and whether serde's ignore-unknown behaviour is intended or incidental — **NORMATIVE STATUS UNRESOLVED** (no source states it) |
| **Unresolved assumptions** | That the new generation is structurally distinguishable at all |

---

## §8 — Viability assessment against evidence

**The task requires that viability not be assumed.** Assessed:

| Candidate | Evidence permits consideration? | Basis |
|---|---|---|
| **A** | **Yes** | The field exists and is persisted (F2); the mechanism is realisable today. Its downgrade property is CONFIRMED, not a reason to exclude it from the space |
| **B** | **Conditionally** | Realisable only if the accepted D-3 representation admits a bound marker — unknown (EG-1). Cannot be excluded, cannot be fully evaluated |
| **C** | **Yes** | Directly precedented in-repo (F11) |
| **D** | **Conditionally** | Domain separation exists as a concept in the codebase (F9) but with no third-domain convention and no entry-layer precedent; depends on D-3 (EG-1) |
| **E** | **Conditionally** | Mechanically realisable, but its central security property is **blocked on EG-1** (D7-Q-018) |
| **F** | **Yes** | No technical obstacle; cost is operational. Constrained by G-3 |
| **G** | **Yes for the structural and genesis variants** | F5 and F7 are CONFIRMED properties of the current code. The `seq`-boundary variant additionally depends on D-5 |

**No candidate is ruled out by the evidence.** Four (A, C, F, and G's structural
variant) are fully evaluable now; three (B, D, E) cannot be fully evaluated until
EG-1 is closed. This is recorded as a fact about the evidence, not as a ranking.

**Candidates are not mutually exclusive** — **INFERENCE.** C and F differ only in
where the rule set is fixed (invocation vs artifact); D and E compose (a
self-describing digest makes trial verification fail-closed); A and G compose
(a declared marker corroborated by structure). A decision may therefore be a
combination.
