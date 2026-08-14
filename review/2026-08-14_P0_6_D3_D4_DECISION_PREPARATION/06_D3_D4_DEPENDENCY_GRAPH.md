# 06 — D-3 / D-4 Dependency Graph

Every edge carries **SOURCE**, **REASON** and **STATUS**. No edge is asserted as
one-directional without evidence for the direction; where evidence supports both
directions, the edge is marked bidirectional.

Legend: `00_…` §5.

---

## 1. Graph

```
        D-1 (CLOSED)            D-2 (CLOSED)
              │                       │
              └───────────┬───────────┘
                          ▼
              ┌─────────────────────────┐
              │   D-3  ◄──────────►  D-4 │   bidirectional, hard
              │ representation  semantics│
              └────┬───────────────┬────┘
                   │               │
                   ▼               ▼
                  D-7             D-5
            version discr.   migration (BLOCKED)
                   │               ▲
                   └───────────────┘
                     (D-5 ↔ D-7 hard, established in the
                      D-2/D-5 package, not re-derived here)

                  D-6 replay ◄─── D-3, D-4, D-5
```

---

## 2. Edge inventory

### E-01 · D-2 → D-3
- **SOURCE:** D-2 CLOSED (accepted input); `01_…` D3-Q-011, D3-Q-022.
- **REASON:** A representation can only be specified for a fixed membership set.
  Field ordering (D3-Q-011) and domain separation (D3-Q-022) both take the member
  list as input.
- **STATUS:** **HARD.** Satisfied — D-2 is closed. *Caveat:* the closed membership
  list was not supplied to this package in explicit form (`00_…` §8), so the
  edge is satisfied in principle while the concrete list remains an input to be
  restated at decision time.

### E-02 · D-2 → D-4
- **SOURCE:** D-2 CLOSED; `02_…` §1.
- **REASON:** D-4 defines semantics for a collection that D-2 placed in the
  domain. Without membership there is nothing to give semantics to.
- **STATUS:** **HARD.** Satisfied.

### E-03 · D-3 ↔ D-4 — bidirectional
- **SOURCE:** `01_…` D3-Q-012, D3-Q-014; `02_…` D4-Q-001, D4-Q-003, D4-Q-004,
  D4-Q-007, D4-Q-010; `05_…` §1–§2.
- **REASON — D-4 → D-3.** The chosen semantics determines what the encoding must
  do. Under an unordered or multiset semantics the digest must be order-invariant,
  which forces a canonical sort or a commutative construction (D3-Q-012); under a
  set semantics the encoding must collapse duplicates (D3-Q-014). Under an ordered
  semantics both questions become trivial.
- **REASON — D-3 → D-4.** The encoding determines which semantics are
  *expressible*. A length-prefixed encoding forces the element count to be
  explicit, which forces D-4 to state whether multiplicity is semantic
  (D4-Q-007). A canonical-JSON profile forces an answer on `[]` versus absent and
  omitted versus null (D4-Q-008, D4-Q-009). A representation-layer deduplication
  would silently overrule any D-4 answer (D3-Q-014).
- **STATUS:** **HARD, BIDIRECTIONAL.** Neither can be closed in isolation without
  constraining the other. **Evidence for the direction exists in both directions**
  and is cited above; this is not an assumed symmetry.

### E-04 · D-3 → D-7
- **SOURCE:** `01_…` D3-Q-023; `src/chain.rs:35–47` (no version marker in the
  digest input — CONFIRMED); `src/api/audit.rs:132` and `src/log_writer.rs:151–170`
  (`schema` present but unread and unprotected — CONFIRMED).
- **REASON:** D-3 must state whether a version marker is bound *inside* the digest
  input. If it is, the digest becomes self-describing and D-7's discriminator is
  partly determined by D-3. If it is not, D-7 must supply the discriminator
  entirely from outside the digest.
- **STATUS:** **HARD, one-directional as evidenced.** A reverse edge (D-7 → D-3)
  is **plausible but not evidenced**: if D-7 mandated a particular discriminator
  form, D-3 would have to encode it. Because D-7 is OPEN and has stated nothing,
  no reverse constraint currently exists. **Recorded as CONDITIONAL-REVERSE:
  becomes an edge only if D-7 selects a mechanism requiring in-digest encoding.**

### E-05 · D-4 → D-5
- **SOURCE:** `02_…` D4-Q-008, D4-Q-009; `01_…` D3-Q-024; `src/models.rs:40`
  (`skip_serializing_if` erases `None` vs absent — CONFIRMED);
  `src/log_writer.rs:96` (full entry persisted — CONFIRMED).
- **REASON:** Migration re-derives digests from stored data. If D-4 requires a
  distinction the stored record never captured — specifically absent versus
  `None` for `validator` — historical entries cannot be faithfully re-derived, and
  the affected D-5 strategies are foreclosed **before D-5 is taken**.
- **STATUS:** **HARD, CONDITIONAL.** The edge is hard *if* D-4 chooses an identity
  rule finer than the stored data; otherwise it is soft. The condition is
  D4-Q-009.

### E-06 · D-3 → D-5
- **SOURCE:** `01_…` D3-Q-024, D3-Q-025; `05_…` §4.
- **REASON:** Same mechanism as E-05, entered from the representation side: a
  representation depending on distinctions the JSONL erased makes re-derivation
  impossible; one depending only on recoverable data leaves every D-5 strategy
  available.
- **STATUS:** **HARD, CONDITIONAL** on D3-Q-007 and D3-Q-024.

### E-07 · D-3 → D-6
- **SOURCE:** `01_…` D3-Q-025; `src/chain.rs:53–65` (replay reconstructs from the
  **parsed** struct, not from raw bytes — CONFIRMED).
- **REASON:** The verifier must rebuild the preimage. If the representation
  depends on anything the parse loses, replay cannot reproduce the digest.
- **STATUS:** **HARD.** D-6 is OPEN and not resolved here.

### E-08 · D-4 → D-6
- **SOURCE:** `07_…` (test matrix); `02_…` D4-Q-011…015.
- **REASON:** D-4 fixes which mutations are detectable; D-6 fixes how a detection
  is reported. The set of reportable conditions is a function of D-4.
- **STATUS:** **HARD.** Not resolved here.

### E-09 · D-5 ↔ D-7
- **SOURCE:** `review/2026-08-14_P0_6_D2_D5_DECISION_PREPARATION/05_…` §3.
- **REASON:** Established in the prior package: strategies requiring rule
  selection depend on a mechanism only D-7 can supply, and D-7's available
  mechanisms are constrained by what the record carries.
- **STATUS:** **HARD, BIDIRECTIONAL.** Carried forward, **not re-derived** — both
  decisions are outside this package's scope.

### E-10 · D-1 → D-3, D-1 → D-4
- **SOURCE:** D-1 CLOSED.
- **REASON:** D-1 created the need for both: without violations in the domain
  there would be nothing to represent and no collection semantics to fix.
- **STATUS:** **HARD.** Satisfied; not reopened.

---

## 3. Edges deliberately *not* asserted

Recorded so that absence is visible rather than accidental.

| Non-edge | Why it is not asserted |
|---|---|
| D-3 → D-2 | D-2 is CLOSED. A representation choice cannot alter closed membership. If a D-3 outcome appeared to require reopening D-2, that would be a **governance escalation**, not an edge — see §5 |
| D-4 → D-2 | Same reasoning |
| D-6 → D-3 | No evidence that reporting requirements constrain the encoding. Plausible in principle; **not evidenced**, so not asserted |
| D-7 → D-3 | See E-04 — recorded as CONDITIONAL-REVERSE, not as a current edge |
| D-5 → D-3 / D-5 → D-4 | D-5 is BLOCKED and has stated nothing. Its future outcome could constrain neither retroactively without reopening D-3/D-4 — also a governance question, not an edge |

## 4. Closure order implied by the graph

**Stated as a structural reading of the edges, not as advice on sequencing.**

- D-3 and D-4 are mutually constraining (E-03) and therefore form **one closure
  unit**: closing either alone leaves the other's option space silently reduced.
- Both are reachable now — their only inbound hard edges (E-01, E-02, E-10) come
  from closed decisions.
- D-7 has an inbound edge from D-3 (E-04); D-5 has inbound edges from both
  (E-05, E-06) plus its own bidirectional edge with D-7 (E-09) and its unresolved
  evidence gaps.
- This is consistent with the agreed sequence **D-3 + D-4 → D-7 → D-5**; the graph
  is presented as evidence for that ordering, not as a proposal to change it.

## 5. Governance dependency — recorded, not resolved

**NORMATIVE CONFLICT (potential, not actual).** Two conflicts surfaced during
preparation that D-3/D-4 will encounter but cannot resolve alone:

1. **`score` range** — documented as "0.0–1.0" (`src/policy.rs:40`,
   `src/models.rs:37`) but **no validation enforces it** (`src/policy.rs:283`
   copies the value straight through) — CONFIRMED. Recorded at D3-Q-017.
2. **`action` equality** — compared case-insensitively (`src/engine.rs:44`) but
   stored verbatim (`:51`), so the engine's equality and the record's identity
   already differ — CONFIRMED. Recorded at D4-Q-010.

Neither is resolved here. Both may require a decision from an authority beyond
D-3/D-4 (policy validation is arguably outside the integrity domain entirely).
**RECORDED AS OPEN DECISION.**
