# 04 — D-4 Candidate Collection Semantics

**All entries below are NON-NORMATIVE CANDIDATES.** None is selected, ranked or
characterised as recommended, preferred, best, safest, simplest or correct.
Letter order is arbitrary.

Legend: `00_…` §5. Question IDs refer to `02_…`; T-IDs to `07_…`.

---

## A — Ordered list (sequence)

**NON-NORMATIVE CANDIDATE**

- **Definition.** `violations` is a sequence. Position is semantic. Two
  collections are equal only if they contain the same elements in the same order.
  Multiplicity is preserved.
- **Source.** Matches the runtime type and production path.
- **Path / line.** `src/models.rs:90` (`Vec<Violation>`); order from
  `src/policy.rs:233–237` and `src/engine.rs:19`.
- **Source status.** IMPLEMENTATION-DERIVED. **The current order is not assumed
  normative** — YAML declaration order is an authoring artifact.
- **Advantages.** Nothing is discarded; reordering, duplication and removal are
  all detectable; the digest can consume elements as stored, so D-3 needs no
  sort rule (D3-Q-012 answered trivially).
- **Limitations.** Binds the digest to policy authoring order: reordering rules
  in the YAML changes the digest of otherwise identical future decisions. Whether
  that is fidelity or brittleness is the decision.
- **Cross-language.** No collation rule and no sort-stability question arise.
- **Replay.** Verifier consumes elements in stored order.
- **Migration.** Historical entries re-derivable — order is preserved in the
  JSONL array.
- **Security.** T-D4-04 (reorder) is tamper; T-D4-05/06 (duplicate insert/remove)
  are tamper; T-D4-12 is tamper.
- **Ambiguity risks.** Low.

## B — Unordered set

**NON-NORMATIVE CANDIDATE**

- **Definition.** `violations` is a set of distinct elements. Neither order nor
  multiplicity is semantic. Two collections are equal if they contain the same
  distinct elements.
- **Source.** No in-repo support — duplicates are representable today.
- **Path / line.** `src/engine.rs:50–55` (duplicates possible via shared rule
  ids); `src/policy.rs:233–237` (**no id-uniqueness check at policy load** —
  CONFIRMED).
- **Source status.** NON-NORMATIVE CANDIDATE.
- **Advantages.** Digest is invariant to policy reordering; equality matches the
  intuition that "the same rules fired".
- **Limitations.** Collapses duplicates by definition, so duplicate insertion and
  removal become **undetectable** — a protection reduction relative to A and C
  that would need to be intended. Requires a rule for records that already
  contain duplicates: collapse silently, or refuse.
- **Cross-language.** Requires a canonical ordering or a commutative accumulation
  for the digest (D3-Q-012), plus element-equality defined precisely.
- **Replay.** Verifier must canonicalise before comparing.
- **Migration.** Historical entries re-derivable, but any historical duplicates
  change meaning under the new semantics.
- **Security.** T-D4-04/12 become equivalences (not tamper); **T-D4-05/06 become
  undetectable** — stated as a property, not an objection.
- **Ambiguity risks.** Moderate — "distinct" requires element equality, which
  re-enters D4-Q-010 (is `"DENY"` the same element as `"deny"`?).

## C — Multiset (bag)

**NON-NORMATIVE CANDIDATE**

- **Definition.** Multiplicity is semantic; position is not. Two collections are
  equal if each element occurs the same number of times.
- **Source.** No in-repo precedent; consistent with the observed data shape.
- **Path / line.** `src/models.rs:90`; `src/engine.rs:58–65` (order not
  decision-relevant).
- **Source status.** NON-NORMATIVE CANDIDATE.
- **Advantages.** Reordering is an equivalence while duplicate insertion and
  removal remain detectable — the only candidate that separates those two
  properties.
- **Limitations.** Requires a canonical order or commutative accumulation for
  hashing (D3-Q-012), and a total tie-break when duplicates share a sort key
  (D4-Q-004).
- **Cross-language.** As B, plus multiplicity counting.
- **Replay.** Verifier canonicalises, preserving counts.
- **Migration.** Re-derivable.
- **Security.** T-D4-04/12 equivalences; T-D4-05/06 tamper.
- **Ambiguity risks.** Moderate — same element-equality question as B.

## D — Canonically sorted collection

**NON-NORMATIVE CANDIDATE**

- **Definition.** The collection is sorted by a specified total key before
  hashing; the sorted form is the canonical form. May be layered on B or C.
- **Source.** No sorting exists anywhere on the path.
- **Path / line.** `src/engine.rs:50`, `src/log_writer.rs:96` — CONFIRMED absent.
- **Source status.** NON-NORMATIVE CANDIDATE.
- **Advantages.** Gives order-invariance a concrete, testable construction;
  produces a deterministic byte order for the digest.
- **Limitations.** The sort key must be **total** — `rule` alone is not, when
  duplicates share an id — and string collation must be specified (byte order vs
  Unicode collation), which re-enters D3-Q-001/015. Sorting also discards the
  stored order, so the digest no longer attests it.
- **Cross-language.** Collation is the classic divergence point; byte-order
  sorting of UTF-8 is reproducible, locale-aware collation is not.
- **Replay.** Verifier sorts identically or fails.
- **Migration.** Re-derivable, provided the key is computable from stored data.
- **Security.** Same profile as B or C depending on which it layers onto; adds
  the risk that an unstable or partial sort makes the digest non-deterministic.
- **Ambiguity risks.** Moderate to high if the key is not total and the collation
  is unstated.

## E — Ordered list with declared order-insignificance

**NON-NORMATIVE CANDIDATE** *(added: the corpus makes the distinction meaningful)*

- **Definition.** The collection is stored and hashed as an ordered sequence (as
  A), but the *specification* declares that order carries no audit meaning.
  Reordering is then a digest change that is not a semantic change.
- **Source.** Corresponds to today's split: the type is ordered
  (`src/models.rs:90`) while the decision is order-independent
  (`src/engine.rs:58–65`) — CONFIRMED.
- **Source status.** NON-NORMATIVE CANDIDATE; describes an option, not the
  current state (today nothing is declared at all).
- **Advantages.** No sort rule, no collation question; strictly stronger tamper
  detection than B or C.
- **Limitations.** Creates a documented gap between "digest differs" and "record
  means something different", which every consumer of a verification failure must
  understand. A legitimate policy reordering makes future digests differ, which
  is expected under A too but is here explicitly declared non-semantic.
- **Cross-language.** As A.
- **Replay.** As A.
- **Migration.** As A.
- **Security.** Detection profile identical to A; the difference is interpretive.
- **Ambiguity risks.** Low technically; the risk is human — a mismatch may be
  misread as semantic tampering.

## F — Composite semantics (per-element identity + collection rule)

**NON-NORMATIVE CANDIDATE**

- **Definition.** Element identity is defined separately from collection
  structure: first specify when two `Violation` values are the same element (all
  four fields? `rule` alone? case-normalized `action`?), then apply A–E over that
  identity.
- **Source.** Made necessary by an observed conflict, not invented here.
- **Path / line.** `src/engine.rs:44` (case-insensitive comparison) vs `:51`
  (verbatim storage) — CONFIRMED; recorded as **NORMATIVE CONFLICT** at D4-Q-010.
- **Source status.** NON-NORMATIVE CANDIDATE.
- **Advantages.** Makes explicit what B, C and D leave implicit — every one of
  them needs an element-equality rule, and this candidate names it rather than
  assuming byte equality.
- **Limitations.** Two decisions instead of one; element identity interacts with
  D-3 normalization (D3-Q-015/016).
- **Cross-language.** Requires the identity rule to be specified as precisely as
  the encoding.
- **Replay.** Verifier applies the identity rule before the collection rule.
- **Migration.** Depends on whether the identity rule needs distinctions the
  JSONL erased (D4-Q-009).
- **Security.** Governs whether `action: "DENY"` → `"deny"` is a detectable
  mutation or a no-op — a case reachable from ordinary policy authoring.
- **Ambiguity risks.** Low once stated; high if left implicit under B/C/D.

---

## Cross-candidate observations

**CONFIRMED — the detection matrix differs only in three cells.** Across A–F,
element modification (T-D4-01), distinct-element addition (T-D4-03) and
distinct-element removal (T-D4-02) are detectable under **every** candidate, once
D-1's mandate is implemented. The candidates diverge only on reorder (T-D4-04,
T-D4-12), duplicate insertion (T-D4-05) and duplicate removal (T-D4-06). This
narrows what the D-4 decision is actually about.

**CONFIRMED — B, C and D each require an element-equality rule.** Candidate F
exists to make that requirement visible. Choosing B, C or D without answering
D4-Q-010 would leave equality defined by whatever the implementation happens to
compare.

**CONFIRMED — no candidate is free of D-3 coupling.** A and E leave D3-Q-012
trivial; B, C and D make it load-bearing. This is the bidirectional edge recorded
in `06_…`.
