# 01 — ADR Review (ADR-002 … ADR-006)

Document ID: REV-2026-08-11-001
Status: DRAFT — ANALYSIS ARTIFACT, NO NORMATIVE EFFECT
Date: 2026-08-11
Precondition: read `00_REVIEW_SCOPE_AND_EVIDENCE_BASE.md` first

---

## 0. Review basis and an unavoidable qualification

**ADR-002, ADR-003, ADR-004, ADR-005 and ADR-006 do not exist** — not on `main`, not on
any of the 22 remote branches of the specification repository, not as drafts, not as
issues. This was verified by directory listing and by `git ls-remote --heads`.

A review of nonexistent documents is not possible, and inventing them in order to review
them would violate the governing rule that this role produces requirements *before*
implementation and does not manufacture normative content (CLAUDE.md, GOV-001 §9).

**What is reviewed instead.** Each section below applies the 14 required criteria to the
**decision domain** that the named ADR is proposed to carry, judged against the only
authoritative description of that domain in the repository: **SPEC-002 v0.3 §6**, plus the
requirements it blocks in SPEC-002 §4. The verdict in each case answers a well-posed and
useful question: *if an ADR were authored today for this domain, could it be written,
approved, and independently implemented?* For every domain the answer is currently **no**,
and the review states precisely what is missing.

**STATUS values used:** `NOT AUTHORED` — no document exists. This is the status of all five.
Sub-verdicts (`BLOCKED`, `NOT WRITEABLE`, `WRITEABLE`) describe whether the domain *could*
be closed if someone sat down to author it now.

---

## 1. Cross-cutting findings that block all five ADRs

These apply to ADR-002 through ADR-006 without exception and are not repeated in each
section.

### X-1 — `ADR-001` is a triple identifier collision (P0)

Three documents claim the identifier `ADR-001`:

| Path | Title | Declared status | In `adrs/README.md` index? |
|---|---|---|---|
| `adrs/ADR-001_REPOSITORY_STRUCTURE.md` | Canonical Repository Structure | **ACCEPTED** | yes |
| `adrs/ADR-001_DOCUMENT_MODEL.md` | Document Model — ARC → SPEC → APS | **PROPOSED** | **no** |
| `docs/adr/001-document-model.md` | Document Model — ARC → SPEC → APS | **DRAFT** | **no** |

The latter two are divergent copies of the same decision: they differ in status, in front
matter, and in body (the `docs/` copy adds a "Merge Blockers" checklist and a
`doc/ci/glossary-check` job that the `adrs/` copy lacks).

Violates: **APS-000 §4** ("Identifiers MUST NOT be reused, even after deprecation"),
**VERSIONING.md §8**, and — with particular irony — **INV-DOC-005** ("Every identifier
SHALL be globally unique"), which is declared *by the colliding document itself*.

**Why this blocks ADR-002…006:** `GOVERNANCE.md` §6 step 2 and `adrs/README.md` step 2 both
require "assign the **next sequential** ADR-NNN identifier". With ADR-001 ambiguous and
`adrs/README.md` indexing only one of three ADR-001s, "next sequential" is undefined. Any
ADR-002 assigned now inherits a corrupt numbering baseline. → **BLOCKER-P0-003**.

### X-2 — Two incompatible document models are simultaneously live (P0)

**Source A — AURA Constitution Article V (FROZEN):**
```
AURA Constitution → APS-001 → APS-100 (Protocol Invariants) → ADR/ARR/RFC → … → Implementation
```
Here APS-001 is the **root normative specification**, and ADR sits *below* Protocol Invariants.

**Source B — `ADR-001_DOCUMENT_MODEL.md` (PROPOSED), "Lifecycle Summary":**
```
RFC → ADR → ARC → SPEC → APS (release aggregation) → Implementation & Evidence
```
Here APS is a **downstream publication** aggregating frozen SPECs, and ADR/ARC sit *above*
SPEC, which sits above APS.

**Nature of conflict.** The two models invert the authority direction between APS and
ADR/SPEC. Under A, an ADR is subordinate to APS-100 and cannot create invariants. Under B,
ADRs and ARCs are upstream of everything normative, and `ADR-001_DOCUMENT_MODEL` proceeds to
declare eight new invariants (`INV-DOC-001` … `INV-DOC-008`) — invariants that appear in
neither APS-100 §3 nor `invariants/INVARIANT_REGISTRY.md`, and whose `INV-DOC` prefix is not
in the APS-000 Appendix A canonical prefix registry.

**Impact.** SPEC-002 exists *only* under Model B — the `SPEC-` artifact class is defined
nowhere else. So SPEC-002's right to exist depends on a **PROPOSED, unapproved** ADR that
**contradicts the FROZEN Constitution**. Per Constitution Article V, "a higher-level document
has authority over a lower-level document in all cases of conflict", and per the Authority
Precedence in AGENTS.md/CLAUDE.md, the Constitution outranks the ADR. On the current record,
Model B is not in force, and SPEC-002 has no defined place in the canonical hierarchy.

**Required decision.** Custodian MUST either (i) amend the Constitution via Article XI to
adopt Model B, or (ii) reject Model B and re-home SPEC-002 inside Model A. Until then no
ADR-00x can be correctly placed in the hierarchy. → **OD-003**, **BLOCKER-P0-005**.

### X-3 — GOV-001 contradicts itself on how an ADR is accepted (P1)

- **GOV-001 §5.2** classifies "new requirements, new invariants, new conformance tests,
  behavioral changes" as **Major Changes**, requiring RFC → 14-day comment → ARB → Chief
  Architect → *then* "ADR created if architectural decision is embedded".
- **GOV-001 §6** states the ADR process is: copy template → assign ID → PR → **"Merging the
  PR = accepting the ADR"** → "ADR status set to ACCEPTED". One reviewer, no RFC.

Every AD-CA domain is a Major Change by the §5.2 test — each fixes normative behaviour and
each will require new invariants. Under §5.2 an RFC is mandatory; under §6 a merge suffices.

**Impact.** The acceptance bar for ADR-002…006 is undefined, and the §6 path would let an
ADR that fixes canonical bytes be accepted by a single PR merge — an outcome the task
statement's own reading of GOV-001 ("ACCEPTED ADR wymaga formalnego procesu governance")
explicitly rejects. Note also that GOV-001 is itself only `1.0-DRAFT`.

**Required decision.** Custodian MUST state which path governs AD-CA-class ADRs.
Recommendation is recorded in `06_OPEN_DECISIONS.md` **OD-004**. → **BLOCKER-P1-001**.

### X-4 — No ARC exists, but Model B requires one per SPEC (P1)

`INV-DOC-002`: *"Every SPEC SHALL reference at least one ARC."* `arc/` contains only a
README stating "ARC-001 … ARC-025 will be synchronized … during Sprint 2".
`compliance/arc_to_spec_mapping.yaml` is `mappings: []`. `ARC_TO_SPEC_MAPPING.md` says
"Mapping will be established when SPEC-001 is approved" — and **SPEC-001 does not exist
either** (only SPEC-002 does).

SPEC-002's Authority line cites the Constitution and APS documents, **no ARC**. Under Model
B, SPEC-002 is non-conformant on its own model's invariant. The task's request for
"ARC-xxx (jeżeli wymagany)" traceability therefore resolves to: **required by Model B,
unsatisfiable today**. → **BLOCKER-P1-002**.

### X-5 — No invariant covers the Constitution Artifact or Vector (P1)

`INVARIANT_REGISTRY.md` holds INV-001…INV-015. None concerns Constitution Artifact
construction, Constitution Vector derivation, artifact/vector identity, provenance binding,
registration, or freeze. Every one of ADR-002…006 will require at least one new invariant.
No identifiers are assigned; per task rule, they are recorded throughout this package as
**"identifier not yet assigned"** and never invented.

Compounding: the registry already **self-reports violation of INV-010** ("Every Invariant
MUST have at least one corresponding Conformance Test") — INV-007, INV-012, INV-013,
INV-014, INV-015 have no CONF test. Adding invariants without CONF tests deepens an
already-live Critical-class violation. → **BLOCKER-P1-003**.

### X-6 — The only canonical-serialization authority is a TODO (P0)

SPEC-002 §7 traces REQ-002-021 ("one canonical serialization format") to **APS-200 §8**.
APS-200 §8 reads in full, after three bullets permitting *any* of JSON/CBOR/Protobuf:

> **TODO**: Define the canonical serialization format for interoperability between RI-PY and RI-RS.

Likewise REQ-002-017/018 (hash domains) trace to APS-200 §4 and APS-300 §5/§9. APS-200 §4
defines `integrity_hash` as "SHA-256 hash of **the canonical serialization** of this object"
— i.e. defined in terms of the undefined. APS-300 §5 carries its own:

> **TODO**: Define the canonical algorithm for computing `evidence_hash`. Must … specify
> whether the hash covers the full JSON serialization or a field-ordered canonical form.

**Impact.** Four of SPEC-002's traceability rows point at TODOs. The matrix looks populated
but is not load-bearing. This is the exact failure mode the task's §10 warns about
("hash całego JSON-a" without canonical serialization). → **BLOCKER-P0-006**.

### X-7 — APS-200 §4 forces a timestamp into every integrity hash (P0)

APS-200 §4 (Common Object Contract) requires of **every** entity both:

| `created_at` | string (ISO 8601) | MUST | Timestamp of object creation (UTC) |
| `integrity_hash` | string | MUST | SHA-256 hash of the canonical serialization of this object |

If a Constitution Artifact is modelled as an APS-200 entity, its canonical serialization
contains a wall-clock timestamp, so its `integrity_hash` **changes on every construction**.
Same source → different hash. That is a direct contradiction of SPEC-002 §5.1 (Positive
Determinism Verification) and of Constitution Article IV P2 (Determinism by Design).

This is the CONTENT / IDENTITY / PROVENANCE conflation the task §7 and §11 single out, and
it is already baked into a DRAFT normative document. AD-CA-009 and AD-CA-010 cannot be
resolved without confronting it. → **BLOCKER-P0-007**, **OD-008**.

---

## 2. ADR-002 — AD-CA-001 (authoritative source boundary) · AD-CA-002 (source canonicalization)

**STATUS:** `NOT AUTHORED` · sub-verdict **NOT WRITEABLE**

**BLOCKERS**
- X-1, X-2, X-3, X-5 (cross-cutting).
- **B-002-a (P0):** The Source Set cannot be named while two repositories are both called
  `aura-specification` (see 00 §6). REQ-002-003 demands "repository location"; there are two
  candidate locations and no supersession record. → OD-001.
- **B-002-b (P0):** SPEC-002 REQ-002-005 requires deciding "which document lifecycle statuses
  are permissible as inputs". In S1 **exactly one** document is FROZEN (the Constitution).
  Everything else is DRAFT, and APS-001 is TODO. If the answer is "FROZEN only", the Source
  Set is the Constitution alone. If DRAFT documents are admissible, the source is mutable and
  the artifact is not reproducible over time. Either answer has severe consequences and
  neither is recorded. → OD-005.
- **B-002-c (P0):** AD-CA-002 (canonicalization) has **two rival, already-implemented
  meanings** in the estate and no arbiter — see CONFLICT C-1 below.

**CONFLICTS**
- **C-1 — Rival canonicalization pipelines.**
  *Source A:* RI-RS `src/normalizer.rs`, "SHADOW_SPEC v1.0", a **strict ordered** pipeline —
  UTF-8 validation → NFKC → hidden-character stripping (21 enumerated code points) →
  confusable folding (Cyrillic/Greek/fullwidth) → ASCII lowercase — with the explicit
  warning "any deviation invalidates the shadow hash".
  *Source B:* RI-PY has **no canonicalization stage at all**; `core/embedding.py` consumes
  a raw `str`.
  *Nature:* Two reference implementations of the same protocol disagree on whether source
  canonicalization exists, and the one that has it declares its own frozen spec
  (`SHADOW_SPEC v1.0`) outside the APS/SPEC hierarchy entirely.
  *Impact:* AD-CA-002 cannot be resolved by "align with the reference implementation" —
  the references contradict each other. Worse, SHADOW_SPEC v1.0's steps are *lossy*
  (lowercasing, confusable folding), which is defensible for regex evasion defence but
  destructive if applied to a normative source text.
  *Required decision:* Custodian must decide whether Constitution-source canonicalization is
  (i) SHADOW_SPEC-like and lossy, (ii) lossless byte-level normalization only, or (iii) a new
  pipeline. → **OD-006**.
- **C-2 — Alias hazard is real, not hypothetical.** REQ-002-009 forbids equating
  `AURA-CON-001` with `AURA-CONSTITUTION-001`. Verified: the Constitution's own front matter
  declares `Document ID: AURA-CON-001`, while the file is `constitution/AURA_CONSTITUTION.md`
  and the preserved original is `AURA Constitution_260723_190157.txt`. Three distinct
  designators for one document, and REQ-002-023 requires binding by "source identifier …
  and source location". Which string is the identifier of record is unrecorded.

**MISSING DEFINITIONS** — Source Set membership; inclusion/exclusion rule; whether the
preserved `.txt`/`.pdf` originals or the `.md` rendering is authoritative (they are *not*
byte-identical, and APS-000's own "Source:" footer claims the `.txt` is the original);
permissible input statuses; character encoding; BOM policy; line-ending policy; Unicode
normalization form; whether front matter / "Source:" footers are in or out of scope.

**REQUIRED EVIDENCE** — E1 (canonicalization fixtures) per `04_EVIDENCE_PLAN.md`. None
exists. Note that no fixture can be authored before C-1 is decided.

**REQUIRED SPEC-002 CHANGES** — REQ-002-003 must be extended to require an explicit
authoritative-repository designation (proposed **REQ-002-041**); the `.md` vs `.txt`/`.pdf`
representation question must be raised to a first-class requirement (proposed
**REQ-002-035**). Both are drafted in `03_SPEC-002_v0.4_DRAFT.md`.

**Criteria 1–14:** unambiguous? **No** (C-1, C-2). Scope closed? **No** (two repos, three
designators). Constitution conflict? **Yes, indirect** — via X-2. GOV-001 conflict?
**Yes** — X-3. APS conflict? **Yes** — APS-000 §4 identifier rules vs the alias situation.
SPEC-002 conflict? No; SPEC-002 correctly marks this UNRESOLVED. Independently
implementable? **No.** Conformance test without reading the RI? **No** — no fixture, and
C-1 means the two RIs would fail each other's tests. Hidden implementation dependency?
**Yes** — SHADOW_SPEC v1.0 is a de-facto normative artifact living in an implementation
repo. Undefined behaviour? **Yes**, extensively. RFC instead of ADR? **Yes** — per GOV-001
§5.2 this is a Major Change; and the repo-identity question likely needs a Constitution-level
answer. New invariant? **Yes** — identifier not yet assigned. Fixture? **Yes** — E1.
SPEC-002 change? **Yes** — as above.

---

## 3. ADR-003 — AD-CA-003 (transformation boundary) · AD-CA-005 (see conflict)

**STATUS:** `NOT AUTHORED` · sub-verdict **NOT WRITEABLE — SCOPE DISPUTED**

**BLOCKERS**
- X-1 … X-6 (cross-cutting).
- **B-003-a (P0):** AD-CA-005's subject matter is disputed between the task statement
  ("vector projection mechanism") and SPEC-002 §6 ("embedding method identity and versioning
  model"). See `00 §4`. An ADR cannot be authored against a domain whose scope is contested.
  → **OD-002**.
- **B-003-b (P0):** **ADP-001 does not exist.** The task states ADR-003 proposes "ADP-001 —
  Aura Deterministic Projection". No such document, identifier, or definition exists in S1,
  S3 or S4. `ADP` is not in the APS-000 canonical prefix registry. Per task §8, ADP-001 is
  **not implemented** here; the full list of its missing definitions is delivered as
  `06_OPEN_DECISIONS.md` **OD-010** and summarised in §7 below.
- **B-003-c (P0):** The only existing transformation is **self-declared a placeholder**.
  `core/embedding.py` line 3: *"Placeholder for deterministic embedding in ℝ¹⁵³⁶ space.
  MUST be frozen + reproducible in production."* It cannot be promoted to normative status,
  and per task §14 must not become a protocol invariant by accident.

**CONFLICTS**
- **C-3 — Vector dimension: 1536 vs `32`.**
  *Source A:* SPEC-002 §6 AD-CA-007 candidate list contains the bare token `32`.
  *Source B:* RI-PY hard-codes 1536 in two places — `core/embedding.py` (`[0] * 1536`,
  `range(1536)`) and `core/offline_normalizer.py` (`CONSTITUTION_DIM = 1536`, with
  `normalize_constitution_vector` raising `ValueError` on any other length).
  `docs/architecture.md` and `docs/mathematical_foundation.md` describe 1536-dimensional space.
  *Nature:* Either `32` in SPEC-002 means dimension — in which case it contradicts every
  implementation and document — or it means "int32 width", in which case SPEC-002's candidate
  list is ambiguously written and **dimension is not listed as a decision at all**, i.e. a
  missing decision domain.
  *Impact:* Vector cardinality is a first-order determinant of canonical bytes. It is not
  currently owned by any AD-CA row under either reading.
  *Required decision:* Custodian must disambiguate the `32` token and, if it is not
  dimension, open dimension as an explicit decision. → **OD-007**, proposed **REQ-002-036**.
- **C-4 — Undefined input-length semantics.** `core/embedding.py` computes
  `base_pattern = [(ord(c) % 32) * 3125 for c in text]` then
  `[base_pattern[i % len(base_pattern)] for i in range(1536)]`. For input shorter than 1536
  characters this **tiles** the pattern cyclically; for input longer than 1536 it **silently
  truncates** to the first 1536 characters. The AURA Constitution is ~6,500 characters, so on
  the only plausible real input this transform *discards ~76% of the source*. Neither tiling
  nor truncation is specified anywhere, and truncation is a silent fallback that alters the
  canonical result — prohibited by REQ-002-031's governing principle.
- **C-5 — Scale claim not met.** The comment `3125 = 100000/32` implies a 10⁵ range, but
  `ord(c) % 32` yields 0…31, so component values lie in **[0, 96875]**, never reaching
  100000; and all values are **non-negative**, so the "vector" occupies a single orthant and
  is not unit-normalized. Whatever this is, it is not the normalized int32 unit vector that
  `core/evaluator.py` documents as its input contract ("Pre-normalized int32 vectors …
  ||v|| = 10^5"). The two modules in the same repository disagree on the vector contract.

**MISSING DEFINITIONS** — every item on the task §8 ADP-001 list: input domain, output
domain, dimension, index ordering, byte ordering, arithmetic model, rounding, overflow,
invalid input, empty input, maximum input, determinism statement, domain separation, test
vectors. Additionally: whether the transform is required to be injective, norm-preserving,
or bounded.

**REQUIRED EVIDENCE** — E2, E3, E4 per `04_EVIDENCE_PLAN.md`. None exists.

**REQUIRED SPEC-002 CHANGES** — proposed REQ-002-036 (dimension & index ordering),
REQ-002-037 (input-length domain: empty / minimum / maximum / tiling / truncation, all
fail-closed unless explicitly approved), REQ-002-043 (ADP-001 may not be referenced by any
normative document until fully defined).

**Criteria 1–14:** unambiguous? **No.** Scope closed? **No — actively disputed.**
Constitution conflict? **Yes** — C-4's silent truncation defeats Article IV P6 (Fail Closed)
and P8 (Explicit over Implicit). GOV-001? X-3. APS conflict? **Yes** — `ADP` prefix is
unregistered (APS-000 §3, Appendix A). SPEC-002 conflict? **Yes** — C-3. Independently
implementable? **No.** Test without reading RI? **No.** Hidden implementation dependency?
**Yes, severe** — the only definition of the transform *is* the placeholder code.
Undefined behaviour? **Yes** — C-4 is textbook. RFC instead of ADR? **Yes** — ADP-001 is a
new protocol element and needs an RFC per GOV-001 §5.2, not an ADR. New invariant? **Yes**
— identifier not yet assigned. Fixture? **Yes** — E3 golden vectors are mandatory here.
SPEC-002 change? **Yes.**

---

## 4. ADR-004 — AD-CA-007 (numeric representation) · AD-CA-008 (canonical serialization & hash domains)

**STATUS:** `NOT AUTHORED` · sub-verdict **NOT WRITEABLE** — and **cannot close its own
stated scope** even if authored (see X-5 / F-ORPHAN: AD-CA-004 also blocks REQ-002-021/022).

This is the highest-risk ADR in the package, and the review found **two reproducible
cross-language divergences already present in the reference implementation**. Both are
demonstrated below with executed output, not asserted.

**BLOCKERS**
- X-1 … X-7 (cross-cutting; X-6 and X-7 are specific to this ADR's requirements).
- **B-004-a (P0):** Integer division semantics are undefined and **already divergent**.
- **B-004-b (P0):** Float→fixed-point rounding mode is undefined and **already divergent**.
- **B-004-c (P0):** No canonical serialization authority exists to point at (X-6).

**CONFLICTS**

- **C-6 — Floor division vs. truncation: proven cross-language divergence.**
  `core/evaluator.py` uses Python's `//` in two places:
  `similarity = dot // self.SCALING_FACTOR`, and
  `raw_ari = (… // SCALING_FACTOR) + (self.weight_semantic * sa // self.SCALING_FACTOR)`.
  Python's `//` **floors toward −∞**. Rust `/`, C/C++ `/`, and JavaScript `Math.trunc`
  **truncate toward zero**. For negative operands these differ by one unit in the last place.
  Executed on the actual class, with a constitution vector containing a negative component
  (reachable through the public API — `PoCAEvaluator.__init__` accepts any `List[int]`):

  ```
  dot                    = -7000029999
  Python floor  (dot//S) = -70001
  Rust/C++/JS trunc      = -70000
  DIVERGENCE             = True
  ```
  and on the ARI path with `sa = -70001`:
  ```
  Python  70000*sa//100000 = -49001
  Rust    70000*sa /100000 = -49000
  ```

  *Nature:* the language's default integer-division rounding has become the de-facto
  protocol semantics without ever being specified.
  *Impact:* a Rust or C++ or JavaScript implementation, written correctly against every
  document that exists today, produces a **different ARI and a different drift** from RI-PY
  whenever the semantic-alignment term is negative. This defeats **INV-002 (Bit-Perfect
  Replay)** and **INV-006 (Platform Independence)**, both Critical class, and falsifies the
  cross-language replay claim in the task's §9 and §15.
  *Scope qualification, stated precisely:* the current `embed_text` emits only non-negative
  components, so the **demo path** does not reach the divergence today; the CI determinism
  checks compare x86_64 against ARM64 **within Python**, where both sides floor, so they
  cannot detect it. The defect is therefore **latent, not currently firing** — but it is
  reachable through the documented public API, and it is exactly the class of accident that
  becomes permanent when a placeholder is frozen. It is reported as a specification gap of
  P0 severity, not as a live production failure.
  *Required decision:* AD-CA-007 MUST fix a single division/rounding semantics
  (floor / truncate / euclidean) as a language-independent rule. → **OD-011**, proposed
  **REQ-002-038**.

- **C-7 — `round()` half-to-even vs. half-away-from-zero: proven cross-language divergence.**
  `core/offline_normalizer.py`: `int_vector = [round(x * SCALING_FACTOR) for x in normalized_vector]`.
  Python's built-in `round()` implements **banker's rounding (half-to-even)**. C's `round()`
  and Rust's `f64::round()` implement **half-away-from-zero**; JavaScript's `Math.round`
  implements **half-up**. Executed:

  ```
         x*1e5  Python round   half-away (C/Rust)   half-up (JS)
        0.5000             0                    1              1  <-- DIVERGES
        1.5000             2                    2              2
        2.5000             2                    3              3  <-- DIVERGES
        3.5000             3                    3              3
  ```

  *Nature:* SPEC-002 §6 lists `round-half-to-even` as a **candidate only**, and §3
  constraint 4 states in terms that "No candidate choice … constitutes a recommendation,
  preference, default, or implied architectural decision." The implementation has
  nevertheless **already committed** to that candidate, silently, by using a language
  builtin.
  *Impact:* this is the Constitution **Vector construction path** — the artifact whose
  identity the whole of SPEC-002 exists to pin down. Any independent implementer in
  Rust/C/JS following the documents produces a different vector at every tie, hence
  different canonical bytes and a different vector hash.
  *Required decision:* AD-CA-007 MUST fix the rounding mode explicitly, and must do so
  *without* being read as ratifying the implementation merely because the implementation got
  there first. → **OD-012**, proposed **REQ-002-039**.

- **C-8 — Tolerance-based validation of a bit-exact artifact.**
  `offline_normalizer.verify_unit_vector` accepts any magnitude within **±1%** of 10⁵
  ("`tolerance = 0.01`"). A ±1% band admits an enormous set of distinct vectors as "valid".
  Validation with tolerance is legitimate for a sanity check; it is **not** capable of
  establishing canonical identity, and nothing in the repository distinguishes the two roles.
  → proposed **REQ-002-042**.

- **C-9 — Float determinism is assumed, not established.**
  `normalize_vector` computes `math.sqrt(sum(x * x for x in vector))`. IEEE-754 addition is
  not associative; the result is stable only if summation order is fixed *and* no compiler
  reassociation, FMA contraction, or vectorization occurs. Constitution Article VII of the
  implementation's own `CONSTITUTIONAL_DECREE.md` permits float **only** in this file, but
  permitting float is not the same as specifying it. Order, precision, and the prohibition on
  FMA/reassociation are unspecified. Per task §14: this is offline/prototype behaviour and
  MUST NOT silently become the protocol invariant.

- **C-10 — `zip` fail-open on mismatched vector lengths.**
  `vector_similarity_int32` computes `sum(a * b for a, b in zip(v1, v2))`. Python's `zip`
  **silently stops at the shorter sequence**. Executed against a 1536-dimension constitution
  with a length-1 agent vector:
  ```
  mismatched-length evaluate (len 1 vs 1536): {'ari': 0, 'drift': 200000}
  ```
  No exception, no error, a confident numeric answer. This violates **INV-008 (Fail Closed,
  Critical)** and Constitution Article IV P6, and it is the precise pattern REQ-002-031
  prohibits ("NO SILENT FALLBACK WHERE IT CAN ALTER THE CANONICAL RESULT").
  → proposed **REQ-002-040**.

- **C-11 — Comment and code disagree on the drift clamp.** `evaluator.py` comments
  "Clamp drift to [0, 100000] to represent [0.0, 1.0]" immediately above
  `drift = min(max(0, self.SCALING_FACTOR - sa), 2 * self.SCALING_FACTOR)`, which clamps to
  **[0, 200000]**. Executed output above shows `drift = 200000`, i.e. the code is what runs.
  Which is normative is unrecorded. Minor in isolation; material because drift is a published
  measurement field.

**MISSING DEFINITIONS** — integer width and signedness at every stage (component,
accumulator, result); overflow behaviour (wrap / saturate / reject); division and rounding
semantics (C-6); float→int rounding mode (C-7); NaN and Infinity rejection; negative-zero
handling; endianness of the numeric serialization (REQ-002-014 explicitly defers this and
nothing supplies it); field set, field order, and absent-field representation for canonical
serialization; the exact byte string of each hash domain; domain-separation prefixes.

**REQUIRED EVIDENCE** — E4 (numeric boundary), E5 (serialization), E6 (hash golden
vectors), E12 (cross-language replay). **E12 is the decisive one and is currently
impossible** — see §8.

**REQUIRED SPEC-002 CHANGES** — proposed REQ-002-038 (division/rounding), REQ-002-039
(float→fixed boundary and rounding mode), REQ-002-040 (dimension-agreement fail-closed check),
REQ-002-042 (tolerance MUST NOT establish identity). All drafted in
`03_SPEC-002_v0.4_DRAFT.md`.

**Criteria 1–14:** unambiguous? **No.** Scope closed? **No** — cannot close REQ-002-021/022
without AD-CA-004. Constitution conflict? **Yes** — C-6/C-7 defeat Article IV P2; C-10
defeats P6. GOV-001? X-3. APS conflict? **Yes** — X-6, X-7. SPEC-002 conflict? **Yes** —
the implementation has pre-empted candidate choices that SPEC-002 §3.4 declares unapproved.
Independently implementable? **No.** Test without reading RI? **No — and this is the
sharpest failure in the package:** the numeric semantics are recoverable *only* by reading
`evaluator.py` and `offline_normalizer.py`. Hidden implementation dependency? **Yes** —
Python's `//` and `round()` are load-bearing and undocumented. Undefined behaviour?
**Yes** — overflow, NaN, mismatched length, endianness. RFC instead of ADR? **Yes.**
New invariant? **Yes** — identifier not yet assigned. Fixture? **Yes** — E4/E6/E12.
SPEC-002 change? **Yes.**

---

## 5. ADR-005 — AD-CA-009 (identity model) · AD-CA-010 (provenance boundary)

**STATUS:** `NOT AUTHORED` · sub-verdict **NOT WRITEABLE**

**BLOCKERS**
- X-1, X-2, X-3, X-5, **X-7 (decisive)**.
- **B-005-a (P0):** X-7 — APS-200 §4 mandates `created_at` in every entity *and* defines
  `integrity_hash` over the canonical serialization of that entity. Identity is therefore
  already contaminated by provenance in a DRAFT normative document. AD-CA-009 and AD-CA-010
  must be resolved **together with an APS-200 correction**, not in isolation.
- **B-005-b (P1):** The five concepts SPEC-002 §4.4 requires be kept distinct — Identity,
  Integrity, Provenance, Lineage, Status — have **no separate representation anywhere**.
  APS-200 gives every entity exactly one `object_id` and one `integrity_hash`; there is no
  artifact-vs-vector distinction, no provenance field, no lineage field, no `supersedes`.
  REQ-002-027 (`supersedes` semantics) has no substrate in the data model.

**CONFLICTS**
- **C-12 — The task's §11 question list has no recorded answer and cannot be answered from
  evidence.** Whether a change of timestamp / Git commit / compiler / OS / CPU / Python
  version / Rust version should change artifact or vector identity is, correctly, an
  architectural decision. The review records only what the *evidence* shows, and refuses to
  infer the decision (task §11: "Nie odpowiadaj z założenia"):
  - *timestamp* — currently **does** change identity, via APS-200 §4 `created_at` +
    `integrity_hash`. Almost certainly unintended. → OD-008.
  - *Git commit* — SPEC-002 REQ-002-025 requires provenance binding to "repository revision",
    but REQ-002-033 explicitly leaves open whether provenance is inside or outside the hash
    domain. No implementation binds a revision at all.
  - *compiler / OS / CPU* — C-6 and C-7 mean these **do** currently change the vector across
    languages, and C-9 means they *may* change it across compilers within a language. Under
    INV-006 they MUST NOT. So today the system's behaviour is the opposite of its invariant.
  - *Python / Rust version* — unbound; no dependency closure exists (AD-CA-006, orphaned).
- **C-13 — RI-PY has no identity fields at all.** `reference/RI-PY_AURA_POC_A_CORE.md`
  records INV-015 (Canonical Identity) as **❌ "No APS-000 identifiers in objects"** and
  INV-009 as **❌ "No protocol_version in evidence objects"**. So the identity model has zero
  implementation coverage, and the conformance record already says so.

**MISSING DEFINITIONS** — field names, formats, and generation rules for
`document_id`, `document_version`, `artifact_id`, `vector_id`, `provenance_id`; which of
these are content-derived vs. assigned; the inter-identity binding field set (REQ-002-016);
`supersedes` semantics; whether provenance is in-hash, out-of-hash, or externally bound
(REQ-002-033 — the decision SPEC-002 explicitly declines to make).

**REQUIRED EVIDENCE** — E7 (identity binding), E8 (provenance). None exists.

**REQUIRED SPEC-002 CHANGES** — none to the *requirements*, which are well posed. The change
needed is upstream: **APS-200 §4 must be corrected** so that a deterministic artifact is not
forced to carry a wall-clock timestamp inside its integrity hash. Recorded as **OD-008** and
as a required SPEC-002 v0.4 note that REQ-002-015/016/033 cannot be satisfied until APS-200
is fixed.

**Criteria 1–14:** unambiguous? **No.** Scope closed? **No** — depends on an APS-200 fix.
Constitution conflict? **Yes, via X-7** (Article IV P2). GOV-001? X-3. APS conflict?
**Yes — direct and material (X-7).** SPEC-002 conflict? No — SPEC-002 §4.4 is the strongest
part of the document and is correct as written. Independently implementable? **No.** Test
without reading RI? **No.** Hidden implementation dependency? Not yet — nothing is
implemented. Undefined behaviour? **Yes** — provenance boundary is explicitly open.
RFC instead of ADR? **Yes** — an APS-200 correction is a Major Change under GOV-001 §5.2.
New invariant? **Yes** — identifier not yet assigned. Fixture? **Yes** — E7/E8.
SPEC-002 change? **Advisory note only**, plus the APS-200 dependency.

---

## 6. ADR-006 — AD-CA-011 (registration) · AD-CA-012 (freeze lifecycle)

**STATUS:** `NOT AUTHORED` · sub-verdict **NOT WRITEABLE**

**BLOCKERS**
- X-1, X-2, X-3, X-5.
- **B-006-a (P0):** **CR-007 is undefined.** SPEC-002 §2.2 forbids implementing it, §11 and
  Appendix B declare it BLOCKED, and the task states it "ma być verifierem, a nie mechanizmem
  tworzącym normatywną tożsamość". But no document in S1, S3 or S4 defines CR-007's inputs,
  outputs, authority, or pass/fail semantics. S3 defines CR-001, CR-003, CR-004 only. Per
  task rule, its semantics are **not** inferred here. → **OD-013**.
- **B-006-b (P1):** The lifecycle the task asks to verify —
  `DRAFT → VERIFIED → REGISTERED → APPROVED → FROZEN` — **does not exist in the repository**.
  `VERSIONING.md` §3 and GOV-001 §4 both define
  `DRAFT → REVIEW → APPROVED → FROZEN (↘ DEPRECATED → ARCHIVED)`.
  There is **no VERIFIED state and no REGISTERED state** anywhere. Introducing them is a new
  decision, not a verification of an existing one, and it changes the document lifecycle for
  every artifact class in the repository.

**CONFLICTS**
- **C-14 — Registration has no registry.** REQ-002-028 requires "the authoritative registry
  and its location". APS-000 §7 describes a "Canonical Registry" covering documents,
  invariants, ADRs, evidence, tests, fixtures, releases and policies — but the only thing
  that materially exists is `invariants/INVARIANT_REGISTRY.md`. There is no artifact registry,
  no vector registry, no location. AD-CA-011 must therefore *create* the registry, not
  describe it.
- **C-15 — Freeze is asserted by implementations without authority.**
  *Source A:* `VERSIONING.md` §3 — `APPROVED → FROZEN` requires "Explicit freeze decision by
  Chief Architect; requires Amendment Procedure (Constitution Article XI)".
  *Source B:* RI-PY declares itself frozen. `CONSTITUTIONAL_DECREE.md` Article VIII calls
  v3.3 the "Frozen Iron Core"; `docs/architecture.md` footer reads "**Status**: FROZEN —
  MC-READY 2026"; `docs/specs/AUDIT_LAYER_SPEC.md` is described as a "normative frozen spec".
  *Source C:* `reference/RI-PY_AURA_POC_A_CORE.md` flags exactly this — *"Self-declared FROZEN
  (v3.3) — this creates a governance challenge as APS gaps require changes"* — and records
  `APS-950 Certification Status: **NOT CERTIFIED**`.
  *Nature:* an implementation has assigned itself a governance status reserved to the Chief
  Architect, in a repository whose own `CONSTITUTIONAL_DECREE.md` Article V places the
  Custodian above the Copilot. FROZEN now means two different things: a governance state
  conferred by authority, and a self-description adopted by an implementation.
  *Impact:* REQ-002-029 requires "the authority who may authorize freeze" and "the
  verification procedure for confirming frozen status". Neither can be specified while
  "frozen" is a word implementations apply to themselves. Additionally, a self-frozen,
  NOT CERTIFIED implementation cannot be corrected to meet the future contract without
  breaking its own freeze claim — a deadlock. → **OD-014**, **BLOCKER-P1-004**.
- **C-16 — `REGISTERED ≠ APPROVED ≠ FROZEN` is asserted but untestable.** SPEC-002 §8 states
  the distinction well. But with no registry (C-14), no VERIFIED/REGISTERED states
  (B-006-b), and no transition evidence requirements anywhere, none of the three separations
  can currently be verified by any test. The requirement is sound; the substrate is absent.

**MISSING DEFINITIONS** — registry location and schema; required registry fields; the
authority for each transition; preconditions per transition; required evidence per
transition; resulting state per transition; **the set of invalid transitions and the
response to attempting one** (the task explicitly requires this, and nothing in the repo
enumerates invalid transitions for any artifact class); immutability enforcement mechanism;
freeze verification procedure; CR-007's role.

**REQUIRED EVIDENCE** — E9 (lifecycle), E10 (negative tests). None exists. Note that
`ADR-001_DOCUMENT_MODEL` proposes a `doc/ci/frozen-check` CI job to enforce immutability;
**no such job exists** in S1 (`.github/` contains only CODEOWNERS, issue templates and a PR
template — there are no workflows at all in the specification repository).

**REQUIRED SPEC-002 CHANGES** — REQ-002-028/029 should additionally require an explicit
enumeration of **invalid** transitions and the fail-closed response to each (proposed
**REQ-002-044**); and REQ-002-029 should require that freeze status be conferred only by a
named authority and never self-asserted by an artifact or implementation.

**Criteria 1–14:** unambiguous? **No.** Scope closed? **No** — the lifecycle to be governed
is itself undefined. Constitution conflict? **Yes** — C-15 vs Article VIII (authority) and
Article XI (freeze immutability). GOV-001? X-3, plus GOV-001 §4 vs the task's proposed
5-state lifecycle. APS conflict? **Yes** — APS-000 §7 registry described but absent.
SPEC-002 conflict? No — §8 is correct. Independently implementable? **No.** Test without
reading RI? **No.** Hidden implementation dependency? **Yes** — CR-007 semantics exist, if
at all, only as tacit knowledge. Undefined behaviour? **Yes** — invalid transitions.
RFC instead of ADR? **Yes, emphatically** — adding VERIFIED and REGISTERED changes
`VERSIONING.md` and GOV-001 for every artifact, which is a Major Change and arguably an
Article XI matter. New invariant? **Yes** — identifier not yet assigned. Fixture? **Yes**
— E9/E10. SPEC-002 change? **Yes.**

---

## 7. ADP-001 — required definitions before it may be referenced (task §8)

ADP-001 is **not** treated as an available protocol here. The following are the definitions
that must exist before any document may cite it. Each is recorded as an **OPEN DECISION**
in `06_OPEN_DECISIONS.md` **OD-010**, with no answer supplied.

| # | Required definition | Current state |
|---|---|---|
| 1 | Input domain (type, encoding, admissible values) | undefined — RI-PY takes a raw `str` |
| 2 | Output domain (component type and range) | undefined — RI-PY yields `[0, 96875]`, contradicting its own 10⁵ claim (C-5) |
| 3 | Dimension | **disputed** — 1536 in RI-PY, `32` token in SPEC-002 (C-3) |
| 4 | Index ordering | undefined |
| 5 | Byte ordering | undefined — REQ-002-014 defers it; nothing supplies it |
| 6 | Arithmetic model (widths, accumulator) | undefined |
| 7 | Rounding | **undefined and already divergent** (C-6, C-7) |
| 8 | Overflow | undefined — Python's unbounded ints mask it entirely |
| 9 | Invalid input | undefined — no rejection path exists |
| 10 | Empty input | RI-PY returns a zero vector; a zero vector is un-normalizable (`normalize_vector` raises on zero magnitude), so the two modules are mutually inconsistent on the empty case |
| 11 | Maximum input | undefined — RI-PY **silently truncates** past 1536 chars (C-4) |
| 12 | Determinism statement | absent |
| 13 | Domain separation | absent — no prefix, no tag, no domain string anywhere |
| 14 | Test vectors | absent — `FIX-001` is all `"TODO"` |

**Verdict:** ADP-001 is 0/14 defined. It MUST NOT be referenced as a protocol by ADR-003 or
by SPEC-002 v0.4. → **BLOCKER-P0-008**.

---

## 8. The decisive gap: no independent implementation exists

The success criterion for this stage is that *two independent engineers implement and verify
the Constitution Artifact without inspecting the reference implementation and obtain
identical bytes, identities and results.*

Verified state of the two nominated Reference Implementations (`APS-950 §11`):

- **RI-PY** (`aura-poc-a-core-v3.3`) — implements a *placeholder* embedding, an offline
  normalizer, and an ARI evaluator. It contains **no** Constitution Artifact, no artifact
  identity, no vector identity, no provenance binding, no registry, no freeze mechanism, and
  **no code path anywhere that reads `AURA_CONSTITUTION.md`**. Its
  `generate_sample_constitution` builds a vector from the synthetic pattern
  `0.5 + 0.1 * (i % 10)` — unrelated to the Constitution text. The "Constitution Vector" in
  the PoC is **not derived from the Constitution**.
- **RI-RS** (`aura-guard-v1.3`) — repository-wide search for `constitution`, `vector` and
  `ARI` returns **no matches in `src/`**. It is a PII/prompt-guard service with a
  hash-chained evidence log and its own `SHADOW_SPEC v1.0` normalizer. It implements **none**
  of the Constitution Artifact surface.

**Consequence.** There is exactly **one** partial implementation and it is a self-declared
placeholder. E12 (cross-language replay) has no second party and cannot be executed. The
success criterion is not merely unmet — it is currently **unfalsifiable**, because there is
nothing to compare against. → **BLOCKER-P0-009**.

---

## 9. Summary table

| ADR | Domains | Status | Sub-verdict | P0 blockers | Needs RFC? | Needs new INV? | Needs fixture? | Needs SPEC-002 change? |
|---|---|---|---|---|---|---|---|---|
| ADR-002 | AD-CA-001, AD-CA-002 | NOT AUTHORED | NOT WRITEABLE | X-1, X-2, X-6, B-002-a/b/c | Yes | Yes (unassigned) | Yes (E1) | Yes |
| ADR-003 | AD-CA-003, AD-CA-005* | NOT AUTHORED | NOT WRITEABLE — SCOPE DISPUTED | X-1, X-2, X-6, B-003-a/b/c | Yes | Yes (unassigned) | Yes (E2, E3) | Yes |
| ADR-004 | AD-CA-007, AD-CA-008 | NOT AUTHORED | NOT WRITEABLE | X-1, X-2, X-6, X-7, B-004-a/b/c | Yes | Yes (unassigned) | Yes (E4–E6, E12) | Yes |
| ADR-005 | AD-CA-009, AD-CA-010 | NOT AUTHORED | NOT WRITEABLE | X-2, X-7, B-005-a | Yes | Yes (unassigned) | Yes (E7, E8) | Advisory + APS-200 fix |
| ADR-006 | AD-CA-011, AD-CA-012 | NOT AUTHORED | NOT WRITEABLE | X-2, B-006-a | Yes | Yes (unassigned) | Yes (E9, E10) | Yes |
| **— none —** | **AD-CA-004** | **ORPHANED** | no owning ADR | F-ORPHAN | Yes | Yes (unassigned) | Yes | Yes |
| **— none —** | **AD-CA-006** | **ORPHANED** | no owning ADR | F-ORPHAN | Yes | Yes (unassigned) | Yes | Yes |

\* AD-CA-005 scope is disputed between the task statement and SPEC-002 §6 — see `00 §4`.

**Aggregate verdict: 0 of 5 ADRs are writeable today, and the package as scoped omits 2 of
12 decision domains, both of which are load-bearing.**

---

*End of 01_ADR_REVIEW.md*
