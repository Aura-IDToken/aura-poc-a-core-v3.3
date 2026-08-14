# 02 — D-4: Collection Semantics Register

**Decision:** D-4 — *What, exactly, is `violations` as a collection?*
**Status:** OPEN. Nothing selected. Legend: `00_…` §5.

D-4 is a question about **meaning**, not about bytes. D-3 answers how the chosen
meaning is encoded; D-4 answers what is being encoded. Where the two touch, the
edge is recorded in `06_…`.

---

## 1. Observed behaviour today — IMPLEMENTATION-DERIVED / NON-NORMATIVE

**None of the following is a normative collection rule.** Each is a fact about
the current code.

| # | Aspect | Observed behaviour | Cite |
|---|---|---|---|
| 1.1 | Rust type | `Vec<Violation>` — an ordered, duplicate-permitting sequence | `src/models.rs:90` |
| 1.2 | Production order | Rules are compiled in YAML order (`into_iter().map().collect()`) and iterated sequentially | `src/policy.rs:233–237`, `src/engine.rs:19` |
| 1.3 | Multiplicity per rule | At most one violation per rule — `pattern.find` (first match), not `find_iter` | `src/engine.rs:28` |
| 1.4 | Duplicate origin | Two YAML rules sharing an `id` are the only source of duplicate `rule` values | `src/engine.rs:50–55` |
| 1.5 | Order significance to the decision | **None** — the aggregate is `DENY` if any deny-rule matched, else `REVIEW`, else `ALLOW` | `src/engine.rs:58–65` |
| 1.6 | Filtering | A rule whose validator fails produces **no** violation (`continue`), so absence is not the same as "checked and passed" | `src/engine.rs:32–42` |
| 1.7 | Empty collection | Serializes as `[]`; every integrity fixture uses `violations: vec![]` | `src/chain.rs:112`, `src/segment.rs:432`, `src/sealer.rs:407` |
| 1.8 | `None` vs `[]` for the collection | **Not expressible today** — `violations` is `Vec<Violation>`, not `Option<Vec<…>>`, and carries no `skip_serializing_if`, so it is always present as `[]` | `src/models.rs:90` |
| 1.9 | `None` inside an element | `validator: Option<String>` is omitted from JSON when `None` | `src/models.rs:40` |
| 1.10 | Semantic vs textual equality | `action` is stored as authored but compared case-insensitively — `"DENY"` and `"deny"` are one value to the engine, two strings in the record | `src/engine.rs:44`, `:51` |

**CONFIRMED — consequence of 1.8.** The "`None` vs empty" question for the
*collection itself* is currently **not reachable in the data model**. It becomes
reachable only if a future schema makes the field optional. This distinguishes it
sharply from 1.9, where the distinction is erased *and* reachable today.

---

## 2. Register — D4-Q-001 … D4-Q-015

Each entry: **QUESTION · WHY IT MATTERS · CURRENT EVIDENCE · CANDIDATES ·
CONSEQUENCES · DEPENDENCIES · EVIDENCE REQUIRED · STATUS.**
Candidate letters refer to `04_D4_CANDIDATES.md`.

---

**D4-Q-001 — Is `violations` an ordered list?**
**Q:** Does the position of an element carry meaning that the integrity domain must preserve?
**Why:** Determines whether reordering is a detectable mutation (T-D4-04) or a no-op.
**Evidence:** the runtime type is ordered (`Vec`, `src/models.rs:90`) and order tracks YAML declaration (`src/policy.rs:233–237`) — but the decision does not depend on order (`src/engine.rs:58–65`) — IMPLEMENTATION-DERIVED both ways. **No source states whether order is meaningful.** EVIDENCE GAP as to intent.
**Candidates:** A (ordered list), B (unordered set), C (multiset), D (canonically sorted).
**Consequences:** ordered ⇒ reordering is tamper; unordered ⇒ reordering is equivalence and the digest must be order-invariant, which forces D3-Q-012 to sort or to digest order-independently.
**Dependencies:** **D3-Q-012 (hard, bidirectional)**; T-D4-04, T-D4-12.
**Evidence required:** a statement of whether YAML authoring order is intended to be audit-significant.
**STATUS: OPEN**

**D4-Q-002 — Is it an unordered set?**
**Q:** Are elements identified by value, with no position and no repetition?
**Why:** A set collapses duplicates by definition — which would make duplicate insertion and removal undetectable.
**Evidence:** duplicates are representable today (1.4) — CONFIRMED — so the runtime type is not a set.
**Candidates:** B; B with an explicit rejection rule for duplicates at write time.
**Consequences:** adopting set semantics requires deciding what happens to a record that already contains duplicates — silently collapse, or refuse.
**Dependencies:** D4-Q-003, D4-Q-007; D3-Q-014.
**Evidence required:** none.
**STATUS: OPEN**

**D4-Q-003 — Is it a multiset?**
**Q:** Do elements have multiplicity but no meaningful position?
**Why:** A multiset makes duplicate insertion detectable while making reordering an equivalence — a combination neither pure list nor pure set provides.
**Evidence:** the data supports it (duplicates possible, order not decision-relevant) — IMPLEMENTATION-DERIVED.
**Candidates:** C.
**Consequences:** the digest must be multiplicity-sensitive and order-insensitive, which in practice forces a canonical sort or a commutative accumulation — a D-3 constraint.
**Dependencies:** **D3-Q-012, D3-Q-014 (hard)**; T-D4-05, T-D4-06, T-D4-12.
**Evidence required:** none.
**STATUS: OPEN**

**D4-Q-004 — Canonically sorted collection?**
**Q:** If order is not semantic, is a canonical sort mandated before hashing, and by which key?
**Why:** Sorting is the usual way to make an unordered semantics reproducible; the sort key and its collation must be specified or the sort is itself ambiguous.
**Evidence:** no sorting anywhere on the path — `src/engine.rs:50`, `src/log_writer.rs:96` — CONFIRMED.
**Candidates:** sort by `rule`; by `(rule, action, confidence, validator)`; by per-element digest; no sort.
**Consequences:** a sort by `rule` alone is not total when duplicates share an id — the tie-break must be defined; string collation must be specified (byte order vs Unicode collation), which re-enters D3-Q-001/015.
**Dependencies:** **D3-Q-012, D3-Q-015 (hard)**; D4-Q-007.
**Evidence required:** none.
**STATUS: OPEN**

**D4-Q-005 — First-match semantics**
**Q:** Is "at most one violation per rule" a normative property of the collection, or an artifact of the current matcher?
**Why:** If normative, the collection has a uniqueness invariant that verification could enforce; if incidental, a future `find_iter` change would alter collection semantics without any decision.
**Evidence:** `pattern.find` — first match only — `src/engine.rs:28` — **IMPLEMENTATION-DERIVED, explicitly not assumed normative.**
**Candidates:** declare it normative; declare it incidental; leave the collection agnostic to how elements were produced.
**Consequences:** declaring it normative constrains future engine changes; declaring it incidental means the collection must tolerate multiple violations per rule, which interacts with D4-Q-007.
**Dependencies:** D4-Q-007; D-4 ↔ engine evolution.
**Evidence required:** whether a future requirement calls for all matches per rule.
**STATUS: OPEN**

**D4-Q-006 — All-match semantics**
**Q:** Would the collection be required to record *every* match, including multiple matches of the same rule?
**Why:** An audit-completeness argument may require it; the current code cannot produce it.
**Evidence:** not produced today (D4-Q-005) — CONFIRMED. No source states a completeness requirement — EVIDENCE GAP.
**Candidates:** all matches with positions; all matches without positions; first match only.
**Consequences:** all-match materially enlarges the collection and re-opens ordering (matches have a natural positional order), duplicates, and the size of the digest input.
**Dependencies:** D4-Q-001, D4-Q-003, D4-Q-005.
**Evidence required:** an audit-completeness requirement statement, if any exists.
**STATUS: EVIDENCE GAP**

**D4-Q-007 — Duplicate violations**
**Q:** Are duplicates meaningful, and are they preserved, collapsed, or rejected?
**Why:** Governs whether T-D4-05 and T-D4-06 are tamper events or equivalences.
**Evidence:** reachable only via two YAML rules sharing an `id` (`src/engine.rs:50–55`) — CONFIRMED. **No uniqueness constraint on rule ids was found at policy load** — `src/policy.rs:233–237` compiles without an id-uniqueness check — CONFIRMED.
**Candidates:** preserve with multiplicity; collapse; reject at write; reject at policy load.
**Consequences:** collapsing at any layer makes duplicate insertion undetectable; rejecting at policy load moves the control out of the integrity domain entirely and into policy validation.
**Dependencies:** **D3-Q-014 (hard)**; D4-Q-002, D4-Q-003; T-D4-05, T-D4-06.
**Evidence required:** none.
**STATUS: OPEN**

**D4-Q-008 — Empty collection**
**Q:** What does an empty `violations` mean, and how is it distinguished within the domain?
**Why:** An `ALLOW` with `[]` is the common case; a `DENY` with `[]` is the sharpest tamper signature identified in the D-1 evidence.
**Evidence:** `[]` is the current form and the state of every integrity fixture (1.7) — CONFIRMED. Note the semantic subtlety at 1.6: `[]` means "no rule produced a violation", which includes "a rule matched but its validator failed" — those are different facts with the same representation.
**Candidates:** empty is a first-class value with a defined encoding; empty contributes a reserved marker; empty contributes nothing.
**Consequences:** if empty contributes nothing to the preimage, an empty collection is indistinguishable from an absent one — injectivity failure (D3-Q-008, D3-Q-021). Every historical entry carries `[]`, so this choice directly governs whether historical entries remain re-derivable (D-5).
**Dependencies:** **D3-Q-008, D3-Q-021 (hard)**; D-5; T-D4-07.
**Evidence required:** none.
**STATUS: OPEN**

**D4-Q-009 — Omitted / `None`**
**Q:** Is an omitted collection distinct from an empty one — and is an omitted *element field* distinct from a `None` one?
**Why:** Two different questions that are easy to conflate; only the second is reachable today.
**Evidence:** collection-level: **not reachable** — `violations` is non-optional and always serialized (1.8) — CONFIRMED. Element-level: **reachable and already erased** — `validator: None` is omitted from JSON (`src/models.rs:40`), and `None` means "no validator configured", not "validator failed" (`src/engine.rs:32–42`) — CONFIRMED.
**Candidates:** treat absent ≡ `None` ≡ empty string; treat all three as distinct; treat absent ≡ `None` but distinct from empty string.
**Consequences:** choosing "distinct" for the element level makes historical entries non-re-derivable, because the distinction was never stored — this **forecloses faithful migration** for those records (D3-Q-024).
**Dependencies:** **D3-Q-007 (hard)**; D-5; T-D4-08, T-D4-09.
**Evidence required:** none.
**STATUS: OPEN**

**D4-Q-010 — Semantic equivalence**
**Q:** Must semantically equivalent collections produce an identical digest?
**Why:** The corpus already contains a live case: `action: "DENY"` and `action: "deny"` are one value to the engine and two strings in the record (1.10).
**Evidence:** `to_ascii_lowercase()` at the decision site (`src/engine.rs:44`) versus verbatim storage (`src/engine.rs:51`) — CONFIRMED. **NORMATIVE CONFLICT in the making:** the engine's notion of equality and the record's notion of identity already differ.
**Candidates:** equality is byte-level (two strings, two digests); equality is semantic (normalize before hashing); equality is byte-level but the value domain is constrained at policy load so the case never arises.
**Consequences:** semantic equality requires normalization rules for every field (case, whitespace, Unicode — D3-Q-015/016), and normalizing evidence text changes what the evidence records. Byte equality leaves the engine and the record disagreeing about what "the same violation" means.
**Dependencies:** **D3-Q-015, D3-Q-016 (hard)**; T-D4-10, T-D4-11.
**Evidence required:** whether the `action` value domain is intended to be closed and case-normalized.
**STATUS: NORMATIVE CONFLICT**

**D4-Q-011 — Order-changing mutation**
**Q:** Is reordering the elements a tamper event?
**Why:** It is the mutation whose classification follows directly from D4-Q-001 and nothing else.
**Evidence:** currently undetectable — the D-1 evidence records reorder as `verify_chain → Ok` (ADR §2.7 mutation 4) — CONFIRMED as the pre-D-1 state.
**Candidates:** tamper (ordered/multiset-with-canonical-order); equivalence (set/multiset with order-invariant digest).
**Consequences:** this determines the expected result of T-D4-04 and T-D4-12; the two tests are the same mutation viewed from the two candidate semantics.
**Dependencies:** D4-Q-001, D4-Q-004; D3-Q-012.
**Evidence required:** D4-Q-001 outcome.
**STATUS: OPEN**

**D4-Q-012 — Duplicate insertion**
**Q:** Is inserting a copy of an existing element a tamper event?
**Why:** Under set semantics it is a no-op; under list/multiset semantics it is a modification.
**Evidence:** currently undetectable (ADR §2.7 mutation 1 covers addition generally) — CONFIRMED.
**Candidates:** as per D4-Q-002 / D4-Q-003 / D4-Q-007.
**Consequences:** if the digest collapses duplicates, an attacker can pad the record with copies without detection — a plausible way to obscure a log.
**Dependencies:** D4-Q-007; D3-Q-014; T-D4-05.
**Evidence required:** D4-Q-007 outcome.
**STATUS: OPEN**

**D4-Q-013 — Duplicate removal**
**Q:** Is removing one of two identical elements a tamper event?
**Why:** The inverse of D4-Q-012, and it can differ: a design may detect insertion but not removal if multiplicity is bounded rather than counted.
**Evidence:** currently undetectable — CONFIRMED.
**Candidates:** as per D4-Q-003 / D4-Q-007.
**Consequences:** under set semantics, removal of a duplicate is invisible; under multiset semantics it changes multiplicity and is detectable.
**Dependencies:** D4-Q-007; T-D4-06.
**Evidence required:** D4-Q-007 outcome.
**STATUS: OPEN**

**D4-Q-014 — Violation removal**
**Q:** Is removing a distinct element a tamper event?
**Why:** This is the mutation class with the sharpest compliance consequence — stripping a `DENY` of its substantiation.
**Evidence:** currently undetectable (ADR §2.7 mutations 2 and 5) — CONFIRMED. D-1 = YES is the decision that this must become detectable; **D-4 does not re-decide that**, it only fixes under which semantics "removal" is defined.
**Candidates:** detectable under every candidate semantics — the candidates differ only in *how* the digest changes, not *whether*.
**Consequences:** none of the D-4 candidates leaves distinct-element removal undetectable; this question is therefore about definition, not about protection level.
**Dependencies:** D4-Q-008 (removal down to empty is the boundary case); T-D4-02, T-D4-07.
**Evidence required:** none.
**STATUS: OPEN**

**D4-Q-015 — Violation addition**
**Q:** Is adding a fabricated element a tamper event, and does the answer depend on where it is inserted?
**Why:** Under ordered semantics, insertion position is itself part of the mutation; under unordered semantics it is not.
**Evidence:** currently undetectable (ADR §2.7 mutation 1) — CONFIRMED.
**Candidates:** detectable under every candidate; position-sensitivity varies with D4-Q-001.
**Consequences:** as with D4-Q-014, the protection level is settled by D-1; D-4 fixes the definition and therefore what a test must assert.
**Dependencies:** D4-Q-001; T-D4-03.
**Evidence required:** none.
**STATUS: OPEN**

---

## 3. Register summary

| Status | Count | IDs |
|---|---|---|
| OPEN | 12 | 001–005, 007–009, 011–015 |
| EVIDENCE GAP | 1 | 006 |
| NORMATIVE CONFLICT | 1 | 010 |
| READY FOR HUMAN DECISION | 0 | — |
| **Total** | **15** | |

**Note.** As with D-3, no individual question is marked ready: D-4 is answered as
one coherent semantics (D4-Q-001/002/003/004 are a single fork, and
D4-Q-011…015 are consequences of it). Readiness for D-4 as a whole is assessed in
`09_DECISION_BRIEF.md`.

**Recorded as open decisions, not resolved** (per the stop conditions): choice of
ordered/set/multiset; choice of sorting rule; resolution of the `action`
case-equivalence conflict; resolution of the `score` range conflict noted in
`01_…` D3-Q-017.
