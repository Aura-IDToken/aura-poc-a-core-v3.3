# 07 — D-3 / D-4 Security Test Matrix

**Test design only.** No test implemented. No fixture created. No test file
written or modified in any repository. This is a specification of *what would
need to be verified*, produced so the Authority can see the verification cost
attached to each candidate.

Legend: `00_…` §5. Question IDs refer to `01_…` and `02_…`.

---

## 1. Column meanings

| Column | Meaning |
|---|---|
| **Expected security property** | What the test would establish. Where the expected result depends on an undecided question, the dependency is named instead of an outcome being assumed |
| **Dep. D-3** | Which representation questions must be answered before the expected result is determinate |
| **Dep. D-4** | Which collection-semantics questions must be answered |
| **Dep. D-7** | Whether the version discriminator affects the test |
| **Possible now?** | Whether the test can exist **today** as a characterization test — recording present behaviour without asserting correctness |
| **Needs normative decision?** | Whether asserting a *correct* outcome requires a closed decision |

---

## 2. Matrix

### T-D4-01 — Modify one violation
- **Mutation.** Change a field of an existing element (`rule`, `action`, `confidence`, or `validator`) in the persisted record.
- **Expected security property.** The digest changes; verification fails. Detectable under **every** D-4 candidate (`05_…` §3). The only variable is whether a *semantically equivalent* modification counts — see T-D4-11.
- **Dep. D-3:** D3-Q-002, D3-Q-006 (if `confidence` is the modified field), D3-Q-007 (if `validator`).
- **Dep. D-4:** D4-Q-010 (element identity).
- **Dep. D-7:** none.
- **Possible now?** **Yes** — as characterization. Present behaviour is `Ok` (undetected), recorded in the D-1 evidence.
- **Needs normative decision?** For the *asserted* outcome, no for the general case (D-1 settles it); yes for the equivalence sub-case (D4-Q-010).

### T-D4-02 — Remove one violation
- **Mutation.** Delete a distinct element.
- **Expected security property.** Digest changes; verification fails. Detectable under every candidate. This is the mutation class with the sharpest compliance consequence — stripping substantiation from a `DENY`.
- **Dep. D-3:** D3-Q-008 (if removal empties the collection), D3-Q-020.
- **Dep. D-4:** D4-Q-014; D4-Q-008 at the boundary.
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization; present behaviour `Ok`.
- **Needs normative decision?** No for the general case; yes for the removal-to-empty boundary (D4-Q-008).

### T-D4-03 — Add one violation
- **Mutation.** Insert a fabricated element.
- **Expected security property.** Digest changes; verification fails. Detectable under every candidate. Under ordered semantics the insertion *position* is also bound.
- **Dep. D-3:** D3-Q-013, D3-Q-020.
- **Dep. D-4:** D4-Q-015; D4-Q-001 for position sensitivity.
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization; present behaviour `Ok`.
- **Needs normative decision?** No for detection; yes to assert position sensitivity.

### T-D4-04 — Reorder violations
- **Mutation.** Swap two elements, changing no element content.
- **Expected security property.** **Indeterminate until D-4 closes.** Under A/E: tamper, digest changes. Under B/C/D: equivalence, digest unchanged. The test asserts whichever D-4 selects — it cannot be written correctly before that.
- **Dep. D-3:** D3-Q-012 (emission order).
- **Dep. D-4:** **D4-Q-001, D4-Q-011 — blocking.**
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization only (present behaviour `Ok`).
- **Needs normative decision?** **Yes.** This is the test that most directly encodes the D-4 choice.

### T-D4-05 — Duplicate violation (insertion)
- **Mutation.** Insert a copy of an element already present.
- **Expected security property.** **Indeterminate.** Under A/C/E: tamper. Under B: **undetectable by construction** — one of the two cells in `05_…` §3 where a candidate reduces detection.
- **Dep. D-3:** D3-Q-014 (representation-layer deduplication would overrule D-4).
- **Dep. D-4:** **D4-Q-002, D4-Q-003, D4-Q-007, D4-Q-012 — blocking.**
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization. Note the *precondition* is itself reachable only via two YAML rules sharing an `id`, and no id-uniqueness check exists at policy load (`src/policy.rs:233–237`) — CONFIRMED.
- **Needs normative decision?** **Yes.**

### T-D4-06 — Remove duplicate
- **Mutation.** Delete one of two identical elements.
- **Expected security property.** **Indeterminate.** Under A/C/E: tamper (multiplicity changes). Under B: undetectable.
- **Dep. D-3:** D3-Q-014.
- **Dep. D-4:** **D4-Q-007, D4-Q-013 — blocking.**
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization.
- **Needs normative decision?** **Yes.**

### T-D4-07 — Empty → non-empty
- **Mutation.** Add an element to a record whose `violations` was `[]`.
- **Expected security property.** Digest changes; verification fails. Additionally: an empty collection must have a **defined, distinguishable** encoding, or an empty collection and an absent one collide (injectivity failure).
- **Dep. D-3:** **D3-Q-008, D3-Q-021 — blocking for the injectivity half.**
- **Dep. D-4:** D4-Q-008.
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization. This case has particular weight: **every existing integrity fixture uses `violations: vec![]`** (`src/chain.rs:112`, `src/segment.rs:432`, `src/sealer.rs:407`) — CONFIRMED.
- **Needs normative decision?** Yes for the empty-encoding assertion.

### T-D4-08 — `None` → empty
- **Mutation.** Change an absent/`None` representation into an explicit empty one.
- **Expected security property.** **Indeterminate, and partly not reachable.** At the *collection* level this is **not expressible today**: `violations` is a non-optional `Vec` always serialized as `[]` (`src/models.rs:90`) — CONFIRMED. At the *element* level (`validator`) it is reachable, and the distinction is **already erased on disk** by `skip_serializing_if` (`src/models.rs:40`) — CONFIRMED.
- **Dep. D-3:** **D3-Q-007 — blocking.**
- **Dep. D-4:** **D4-Q-009 — blocking.**
- **Dep. D-7:** none.
- **Possible now?** **Partially.** The element-level case can be characterized; the collection-level case cannot be constructed without a schema change, which is out of scope.
- **Needs normative decision?** **Yes.**

### T-D4-09 — Empty → `None`
- **Mutation.** The inverse of T-D4-08.
- **Expected security property.** **Indeterminate**, same reachability split as T-D4-08. If D-3/D-4 declare absent ≡ `None` ≡ `[]`, this is an equivalence; if they are distinct, it is tamper — **and historical records could not be re-derived**, because the distinction was never stored (E-05, E-06 in `06_…`).
- **Dep. D-3:** D3-Q-007, D3-Q-008.
- **Dep. D-4:** D4-Q-008, D4-Q-009.
- **Dep. D-7:** none.
- **Possible now?** Partially, as T-D4-08.
- **Needs normative decision?** **Yes.** This test also carries the D-5 foreclosure consequence.

### T-D4-10 — Semantically equivalent representations
- **Mutation.** Re-render the same values differently: `0.1` vs `0.10` vs `1e-1` for `confidence`; key reordering; insignificant whitespace in the stored JSON.
- **Expected security property.** **Indeterminate.** If the representation is canonical and the equality rule is semantic, the digest is unchanged and verification passes. If equality is byte-level, the digest changes.
- **Dep. D-3:** **D3-Q-006, D3-Q-011, D3-Q-016, D3-Q-021 — blocking.**
- **Dep. D-4:** D4-Q-010.
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization of what the current serializer emits.
- **Needs normative decision?** **Yes.**

### T-D4-11 — Different textual representation, same semantic value
- **Mutation.** `action: "DENY"` versus `action: "deny"`; a Unicode-equivalent `rule` id under a different normalization form; trailing whitespace.
- **Expected security property.** **Indeterminate — and this is a live conflict, not a hypothetical.** `action` is compared case-insensitively (`src/engine.rs:44`) but stored verbatim (`:51`) — CONFIRMED. So the engine already treats as one value what the record stores as two. Recorded as **NORMATIVE CONFLICT** at D4-Q-010.
- **Dep. D-3:** **D3-Q-015, D3-Q-016 — blocking.** Note `src/normalizer.rs:11–13` states the original text "is always preserved for the evidence hash", so normalizing evidence text would depart from a stated position in the codebase.
- **Dep. D-4:** **D4-Q-010 — blocking.**
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization, and it would document the conflict.
- **Needs normative decision?** **Yes**, and possibly a governance decision beyond D-3/D-4 (`06_…` §5).

### T-D4-12 — Same violations, different ordering
- **Mutation.** Same elements, permuted. Distinct from T-D4-04 only in framing: T-D4-04 asks "is reordering tamper?", T-D4-12 asks "are these two records the same record?".
- **Expected security property.** **Indeterminate.** Under A/E the two records are distinct. Under B/C/D they are the same record and must produce an identical digest — which requires the canonical order or commutative construction from D3-Q-012.
- **Dep. D-3:** **D3-Q-012 — blocking.**
- **Dep. D-4:** **D4-Q-001, D4-Q-004 — blocking.**
- **Dep. D-7:** none.
- **Possible now?** **Yes** — characterization.
- **Needs normative decision?** **Yes.**

---

## 3. Summary

| Property | Count | IDs |
|---|---|---|
| Expected result determinate today (given D-1) | 3 | T-D4-01 (general case), T-D4-02, T-D4-03 |
| Expected result **indeterminate** until D-3/D-4 close | 9 | T-D4-04 … T-D4-12 |
| Possible now as characterization tests | 12 (2 partially) | all; T-D4-08 and T-D4-09 only at element level |
| Blocked on D-7 | 0 | — |

**CONFIRMED — D-7 does not gate this matrix.** No test above depends on the
version discriminator: every one concerns a single record under a single rule.
D-7 would affect *which* rule a verifier applies to a given record, which is a
different test class (it belongs with D-5/D-7 and is not designed here).

**CONFIRMED — the characterization set is available immediately.** All twelve can
be written today against present behaviour without asserting correctness, and
would begin failing exactly when the behaviour changes. Whether to write them now
is **not decided here** — the task prohibits creating fixtures or tests, and no
test file was created.

**Not designed here, recorded as future scope:** cross-language reproduction
vectors (depends on D3-Q-026), migration/replay tests spanning a rule boundary
(depends on D-5 and D-7), and segment/TSA regression across a digest change
(depends on D-5).
