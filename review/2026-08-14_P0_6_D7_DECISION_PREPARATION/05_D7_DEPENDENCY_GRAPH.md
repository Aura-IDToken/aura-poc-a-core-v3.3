# 05 — D-7 Dependency Graph

Every edge carries **SOURCE · REASON · STATUS**. Directions are asserted only
where evidence supports them. The D-7 → D-5 relationship is developed in §3 as
required.

---

## 1. Graph

```
   D-1 CLOSED     D-2 CLOSED     D-3 CLOSED     D-4 CLOSED
        │              │              │              │
        └──────┬───────┴──────┬───────┴──────┬───────┘
               ▼              ▼              ▼
                        D-7  (OPEN)
              versioning / discriminator
                    │           │
        ┌───────────┘           └────────────┐
        ▼                                    ▼
      D-6 (OPEN)                        D-5 (BLOCKED)
   replay reporting   ◄───────────────►  migration
                         (see §4)
```

## 2. Edge inventory

### E-01 · D-1 → D-7
- **SOURCE:** D-1 CLOSED (governing state); `src/chain.rs:25–49` (CONFIRMED that `violations` is outside the current digest).
- **REASON:** D-1 mandates a rule change. Without a rule change there are no generations to discriminate, and D-7 would not exist.
- **STATUS:** HARD. Satisfied.

### E-02 · D-2 → D-7
- **SOURCE:** D-2 CLOSED.
- **REASON:** The membership contract determines what the new rule covers, hence what distinguishes generations.
- **STATUS:** HARD. Satisfied in principle; the concrete contract was not supplied to this package (`06_…` EG-1).

### E-03 · D-3 → D-7 — **partly blocking**
- **SOURCE:** `01_…` D7-Q-008, D7-Q-018; `02_…` candidates B, D, E; `src/chain.rs:25–49`.
- **REASON:** Two D-7 questions cannot be answered without the accepted representation. (i) D7-Q-008: whether the representation admits a bound domain tag determines whether candidate D is realisable. (ii) **D7-Q-018: whether a new-generation record can also satisfy the legacy rule** — which decides the severity of downgrade under D and E — depends on whether the new rule alters the nine-field preimage or adds a separate component.
- **STATUS:** **HARD and currently UNSATISFIED** — the accepted D-3 values were not supplied. This is the single blocking dependency inside D-7.

### E-04 · D-4 → D-7
- **SOURCE:** `01_…` D7-Q-002.
- **REASON:** Collection semantics affect whether a generation difference is structurally observable in a record (candidate G).
- **STATUS:** SOFT. D-7's mechanism space does not change with D-4; only candidate G's observability argument does.

### E-05 · D-7 ↔ D-5 — **hard, bidirectional**
- **SOURCE:** `review/2026-08-14_P0_6_D2_D5_DECISION_PREPARATION/05_…` §3 (established there and carried forward, not re-derived); `03_…` §5 of this package; `src/log_writer.rs:151–170`; `src/chain.rs:71–92`.
- **REASON — D-7 → D-5:** D-5 strategies that verify legacy and new records under different rules require a selection mechanism; that mechanism is D-7's output. Until D-7 establishes that a trustworthy selector is achievable, those strategies cannot be evaluated.
- **REASON — D-5 → D-7:** D-5 determines whether legacy verifiability is required at all. If it is not, D7-Q-001 may resolve to "no discriminator needed"; if it is, some mechanism is entailed. D-5 also fixes the boundary granularity that candidates C, F and G's `seq` variant depend on.
- **STATUS:** **HARD, BIDIRECTIONAL.** Evidence for both directions is cited.

### E-06 · D-7 → D-6
- **SOURCE:** `docs/exit-codes.md` (CONFIRMED contract, codes `0,1,2,3,4,5,6,78`, no version code); `src/bin/aura_replay.rs:113–119`, `:213`; `01_…` D7-Q-012, D7-Q-019.
- **REASON:** Every D-7 candidate creates conditions the current reporting contract cannot express — unknown generation, malformed marker, mixed-generation log, "verified under generation N". D-6 must define how they are reported.
- **STATUS:** HARD, one-directional as evidenced. A reverse edge (D-6 → D-7) is **not asserted**: no evidence shows that reporting requirements constrain the selection mechanism.

### E-07 · D-7 → reference model
- **SOURCE:** `review/2026-08-14_P0_6_D3_D4_DECISION_PREPARATION/09_…` §4, which assigns the reference-model element **"Version selection"** to D-7 explicitly — CONFIRMED.
- **REASON:** One of the six scoped reference-model elements is D-7's to supply.
- **STATUS:** HARD. See `07_…` §1.

### E-08 · D-7 → segment / TSA layer
- **SOURCE:** `src/segment.rs:140–158`, `:382–405`; `tests/tst_verify.rs`.
- **REASON:** Merkle roots are recomputed from entry `chain_hash` values, so the rule used to verify an entry determines whether its segment's root reproduces.
- **STATUS:** HARD in the verification direction; **no data dependency** — no D-7 candidate rewrites sealed history (`03_…` §4). Detail in `08_…`.

## 3. D-7 → D-5, developed

### 3.1 D-7 questions that must be answered **before** D-5

| D-7 question | Why D-5 cannot proceed without it |
|---|---|
| D7-Q-001 Is a discriminator required? | Determines whether D-5 is choosing among multi-rule strategies at all |
| D7-Q-003 Where does it reside? | D-5-A/E (from the D-2/D-5 package) presuppose a selector; its location determines whether the boundary is per-record or per-corpus |
| D7-Q-004 Must it be protected? | An unprotected selector makes D-5-A/E's rule selection attacker-influenceable (`04_…` §2) |
| D7-Q-011/012 Absent / unknown behaviour | Fixes what happens to records the migration does not touch |
| D7-Q-016 Downgrade detectability | Determines whether a legacy-preserving strategy retains the D-1 property |
| D7-Q-018 Can new appear as old? | **Blocked on EG-1.** If yes, every legacy-preserving strategy silently loses the D-1 property |

### 3.2 D-7 questions that must remain **unresolved until** D-5

| Item | Reason |
|---|---|
| The concrete boundary — which records are legacy | Requires G-1 (do production logs exist, over what `seq` range) |
| Whether legacy verification is retained at all | Requires G-2 / G-3 (external reliance, retention obligations) |
| Disposition of existing TSA evidence | A re-sealing question, which is D-5's, not D-7's (`08_…` §3) |
| How long a legacy verifier family must be maintained (candidate F) | Requires G-3 |

### 3.3 D-5 questions that remain **independent** of D-7

| D-5 question | Why independent |
|---|---|
| Whether production logs exist (G-1) | A fact about deployment; no D-7 outcome changes it |
| Whether external consumers exist (G-2) | Likewise |
| Retention obligations (G-3) | Likewise |
| Whether rewriting an append-only audit corpus is admissible at all | A governance question about audit practice, independent of the selection mechanism |
| Mechanical re-derivability of historical digests | Already CONFIRMED independently: the full entry, `violations` included, is persisted (`src/log_writer.rs:96`) |

### 3.4 Can D-5 be prepared in parallel?

**Partly — and it already has been.** The D-2/D-5 package
(`review/2026-08-14_P0_6_D2_D5_DECISION_PREPARATION/`) mapped the D-5 strategy
space to completion while D-7 was open, and marked D-5 **NOT READY** for
selection rather than unpreparable. **INFERENCE:** further D-5 *preparation* is
possible in parallel; D-5 *selection* is not, because §3.1 lists six D-7 outputs
it consumes.

### 3.5 Does any D-7 candidate make a D-5 strategy impossible?

**No — CONFIRMED** (`03_…` §5). No candidate rewrites history, forecloses
re-derivation, or invalidates existing evidence. The constraint runs one way:
some D-5 strategies *require* a D-7 mechanism; none is *excluded* by one.

**One conditional caveat.** If D7-Q-018 resolves such that a new-generation
record can satisfy the legacy rule, then D-5 strategies that keep the legacy rule
available would silently permit loss of the D-1 property. That would not make
those strategies *impossible* — it would make them **inconsistent with D-1**,
which is a governance matter for the Authority, not a technical exclusion.
**Blocked on EG-1.**

### 3.6 Evidence still required — G-1 / G-2 / G-3

Carried forward unchanged from the D-2/D-5 package; **none has been closed**, and
this package could not close any of them from the repository.

| ID | Question | Still open? |
|---|---|---|
| **G-1** | Do real production v1 logs exist? | **Yes.** No `.jsonl` exists in the repository — CONFIRMED — which establishes nothing about deployment |
| **G-2** | Are logs externally relied upon? | **Yes.** Independent verifiability is documented for the Merkle layer only (`src/merkle.rs:1–5`, quotation) |
| **G-3** | Retention obligations? | **Yes.** No retention statement found in the sources read |

## 4. Edges deliberately **not** asserted

| Non-edge | Why |
|---|---|
| D-6 → D-7 | No evidence that reporting requirements constrain the mechanism |
| D-7 → D-1 / D-2 | Both CLOSED. If a D-7 finding appeared to require reopening either, that is a **governance escalation and a stop condition**, not an edge. No such finding arose |
| D-7 → D-3 / D-4 | Both CLOSED. D-7 consumes them; it does not constrain them |
| D-5 → D-3 / D-4 | Out of scope here; recorded in the D-3/D-4 package |
