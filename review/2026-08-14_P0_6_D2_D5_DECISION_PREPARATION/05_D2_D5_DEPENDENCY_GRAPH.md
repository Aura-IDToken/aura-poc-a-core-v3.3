# 05 — D-2 / D-5 Dependency Graph

**Status:** analysis only. Dependency edges are asserted from evidence and
labelled; no decision is made or implied.

Classification legend: see `00_SCOPE_AND_DECISION_CONTEXT.md` §4.

---

## 1. Graph

```
                        D-1  (CLOSED — YES)
                          │  violations ∈ integrity domain
                          ▼
                        D-2  Integrity Domain Contract          [OPEN]
                          │  what exactly is protected
        ┌─────────────┬───┴───────┬─────────────┐
        ▼             ▼           ▼             ▼
      D-3           D-4         D-6           D-7
   canonical    ordering /    replay      versioning /
   representation duplicates / behaviour  compatibility
        │        empty / None      │       mechanism
        │             │            │             │
        └──────┬──────┘            │             │
               │                   │             │
               ▼                   ▼             ▼
                        D-5  Existing v1 log compatibility   [OPEN]
                             ◄──────── hard, bidirectional ────────►  D-7
```

**D-5 is not a leaf and not independent.** It is drawn beside the D-2 subtree
rather than beneath it because it receives edges from D-2, D-3 and D-4 and shares
a bidirectional edge with D-7.

---

## 2. Edge inventory

| Edge | Type | Basis |
|---|---|---|
| D-1 → D-2 | **Hard** | D-1 mandates membership for `violations`; D-2 defines the domain that membership sits in. Without D-2 the mandate has no contract to attach to. |
| D-2 → D-3 | **Hard** | A byte representation cannot be specified for a field set that is not fixed. Evidence: the reduction must cover exactly the members D-2 names. |
| D-2 → D-4 | **Hard** | Ordering, duplicate, empty and `None` semantics are properties *of the members*; the member list must exist first. Note `skip_serializing_if` affects `validator` and `request_id` alike (`src/models.rs:40`, `:65`), so D-4's scope depends on whether D-2 admits `request_id`. |
| D-2 → D-6 | **Hard** | Replay must verify whatever the domain contains; the verifier's obligations are defined by the domain. |
| D-2 → D-7 | **Hard** | Whether a discriminator is *needed*, and whether it is itself protected (D2-Q11), is settled inside D-2's contract. |
| D-3 → D-5 | **Soft** | Migration mechanics depend on the reduction only insofar as re-derivation must reproduce it. Any D-3 outcome is re-derivable from retained data (`src/log_writer.rs:96`), so D-5's *strategy space* does not change with D-3 — only its *cost* does. |
| D-4 → D-5 | **Conditional** | Becomes hard **iff** D-4 chooses semantics that cannot be reconstructed from the persisted record. Concretely: if D-4 requires distinguishing an omitted `validator` from an explicit `None`, that distinction is **already erased on disk** (`src/models.rs:40`), so historical entries could not be re-derived faithfully and D-5-C would be foreclosed for them. Under any D-4 outcome that treats absent ≡ `None`, the edge stays soft. |
| D-6 → D-5 | **Soft** | Replay behaviour must accommodate whatever D-5 chooses; the causal direction is mostly D-5 → D-6. |
| **D-5 ↔ D-7** | **Hard, bidirectional** | See §3. |
| D-2 → D-5 | **Hard** | If D-2 leaves `compute_chain_hash` unchanged (sibling-digest shape, D2-Q12), existing digests stay reproducible and D-5's premise narrows to "how does the new artifact behave on entries that lack it". If D-2 widens the entry digest, every consequence in `02_...` §5 applies. **The same question has two different shapes depending on D-2.** |

---

## 3. D-5 ↔ D-7 relationship

**Classification: HARD, and bidirectional.** Not soft, not conditional, not
unresolved.

**Justification from evidence:**

1. **D-5 → D-7.** Strategies D-5-A and D-5-E require the verifier to select a
   rule per log or per entry. Selection requires a mechanism, and the mechanism
   *is* D-7. Choosing A or E therefore forces D-7 to produce a compatible answer.
   Evidence: no selection mechanism exists today (`02_...` §3.3, §3.7).
2. **D-7 → D-5.** The mechanisms available to D-7 are constrained by what the
   record already carries. `schema` exists but is unread and unprotected
   (`src/api/audit.rs:132`; `src/log_writer.rs:151–170`; `src/chain.rs:25–49`);
   the only in-codebase precedent for schema rejection is on the segment path
   (`src/segment.rs:341–342`; `src/sealer.rs:100`). If D-7 concludes that no
   trustworthy discriminator can be established, strategies D-5-A and D-5-E lose
   their selection mechanism and the admissible strategy space collapses toward
   B, C or D.
3. **Shared sub-question.** Both decisions depend on D2-Q11 — whether the
   discriminator is inside the integrity domain. A discriminator that is not
   protected makes D-5-E's rule selection attacker-influenceable (`04_...` §A);
   one that is protected creates the bootstrap ordering question (`04_...` §B).
   The same fact governs both decisions.

**Consequence for sequencing (observation, not instruction).** D-5 and D-7 cannot
be settled independently without risking an unsatisfiable pair — e.g. selecting
D-5-E and later finding D-7 cannot supply a trustworthy discriminator. Whether
they are taken as one decision or two, and in what order, is the Authority's to
determine.

---

## 4. Decisions reachable now

| Decision | Reachable? | Blocking dependency |
|---|---|---|
| D-2 | **Yes** — its inputs are D-1 (closed) and the evidence in `01_...` | None. Subject to the evidence gaps in `06_...` being accepted as gaps |
| D-3 | No | D-2 |
| D-4 | No | D-2 |
| D-5 | **Partially** — the strategy space is fully mapped, but selection is coupled to D-2 (shape) and D-7 (mechanism), and to the operational gaps in `02_...` §6.5–6.7 | D-2, D-7, evidence gaps |
| D-6 | No | D-2, D-5 |
| D-7 | No | D-2 (D2-Q11) |

**IMPLEMENTATION-DERIVED observation.** D-2 is the only decision in the graph with
no unmet decision-dependency. Every other edge terminates in it, directly or
transitively. This is a structural statement about the graph, not a
recommendation about sequencing.

---

## 5. External dependency, non-decision

**CONFIRMED.** `docs/adrs/0001-hash-chain.md` in the Guard repository is
"Accepted in v1.3, still current" and governs the chain primitive. It describes
`chain_hash` as "SHA-256 of canonical fields incl. `prev_hash`" **without
enumerating them**, and pins the genesis string
`SHA-256("AURA-GUARD-GENESIS-v1.3")`; `src/crypto.rs:25` adds that the genesis
"must never be changed without bumping the protocol version".

**OPEN.** Whether a D-2 outcome amends ADR-0001, supersedes it, or falls within
its existing latitude — and whether a digest-domain change constitutes a protocol
version bump in the sense of `crypto.rs:25` (D2-Q14) — is unresolved and is
recorded as a dependency, not settled here.
