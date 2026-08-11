# 06 — Open Decisions

Document ID: REV-2026-08-11-006
Status: DRAFT — ANALYSIS ARTIFACT, NO NORMATIVE EFFECT
Date: 2026-08-11

---

## 0. Rules applied

Per task §19/§20: each open decision carries Question, Why it matters, Current evidence,
Options, Recommended option, Impact, Required ADR/RFC, Blocking level.

**"Recommended option" is a review recommendation only.** It carries no authority, resolves
nothing, and is offered because a review that lists options without a view is less useful to
the decision-maker. Where the decision is genuinely architectural and the evidence does not
favour one answer, the recommendation is explicitly **"no recommendation — architectural
decision required"**, and that is not hedging: it is the correct output for a question this
role must not answer.

---

## OD-001 — Which repository is authoritative?

**Question.** Which of `AuraIDToken/aura-specification` and `aura-nomos/aura-specification` is
the authoritative specification repository, and what is the other's status?

**Why it matters.** REQ-002-003 requires "repository location" as part of Source Document
Identity. Two locations claim the same name with no precedence recorded, so AD-CA-001 cannot
be resolved even in principle, and every downstream decision inherits the ambiguity.

**Current evidence.** `AuraIDToken/aura-specification` @ `62d2d6b` holds the entire corpus
(Constitution, all APS, SPEC-002 v0.3, GOVERNANCE, invariants, conformance).
`aura-nomos/aura-specification` @ `eb2a4ec` holds an 11-byte README and a CODEOWNERS whose
paths (`/constitution/`, `/aps/`, `/governance/`) mirror the populated repository's layout —
indicating an intended migration target that was never populated. Both are writable by the
same account. No `supersedes` record exists in either.

**Options.**
- (a) `AuraIDToken/*` authoritative; `aura-nomos/*` marked abandoned or deleted.
- (b) `aura-nomos/*` authoritative; migrate the corpus; mark `AuraIDToken/*` superseded with a redirect.
- (c) Both retained with an explicit primary/mirror relationship and a sync mechanism.

**Recommended option.** **(a) or (b), decided on organisational grounds — not (c).** A mirror
without an enforced sync mechanism reproduces exactly this ambiguity. Between (a) and (b) the
review has no basis to choose: that is an organisational question about which GitHub
organisation the project intends to live in, and no technical evidence bears on it.

**Impact.** Blocks AD-CA-001, therefore ADR-002, therefore everything.

**Required ADR/RFC.** Governance decision, recordable as an ADR. No RFC needed — this changes
no protocol behaviour.

**Blocking level.** **P0** — BLOCKER-P0-001.

---

## OD-002 — What is AD-CA-005's scope?

**Question.** Does AD-CA-005 mean (i) embedding method identity and versioning, (ii) the
vector projection mechanism, or (iii) both?

**Why it matters.** These are different decision types. Method *identity/versioning* is a
dependency-identification decision feeding REQ-002-012. A *projection mechanism* is an
algorithm-definition decision, which SPEC-002 places under AD-CA-003 (pipeline) and AD-CA-007
(numeric contract). Authoring ADR-003 against the wrong reading silently redefines a decision
domain and orphans REQ-002-012.

**Current evidence.** SPEC-002 v0.3 §6 row 5, verbatim: *"Embedding method identity and
versioning model. Candidate: `Dictionary-Based Embedding`. Blocks REQ-002-012, REQ-002-016,
REQ-002-024."* SPEC-002 never uses the word "projection". Review input describes AD-CA-005 as
"vector projection mechanism".

**Options.**
- (a) Retain SPEC-002 wording; projection stays under AD-CA-003.
- (b) Redefine AD-CA-005 as projection; move method identity elsewhere or open a new domain.
- (c) Split AD-CA-005 into two domains, one per concern.

**Recommended option.** **(a).** SPEC-002 §6 is the authoritative record and the review task's
own Rule 20 forbids rewriting prior decisions silently. If projection needs its own domain,
(c) is preferable to (b) — but note that adding a domain requires renumbering discipline and
must not reuse `AD-CA-005`.

**Impact.** Blocks ADR-003 scope definition.

**Required ADR/RFC.** Scope clarification recordable in the ADR that closes AD-CA-005.

**Blocking level.** **P1** — BLOCKER-P1-008.

---

## OD-003 — Which document model is in force?

**Question.** Is the canonical hierarchy Constitution Article V (`Constitution → APS-001 →
APS-100 → ADR/RFC → … → Implementation`), or the model in `ADR-001_DOCUMENT_MODEL` (`RFC → ADR
→ ARC → SPEC → APS(release) → Implementation`)?

**Why it matters.** The models invert the authority relationship between APS and ADR/SPEC.
**SPEC-002 exists only under the second model** — the `SPEC-` artifact class is defined
nowhere else. If the second model is not in force, SPEC-002 has no defined place in the
hierarchy, and neither would ADR-002…006.

**Current evidence.** Constitution Article V is **FROZEN**. `ADR-001_DOCUMENT_MODEL` is
**PROPOSED** (and exists as two divergent copies with different statuses). It declares eight
`INV-DOC-*` invariants that appear in neither APS-100 §3 nor the Invariant Registry, using a
prefix absent from APS-000 Appendix A. Per Constitution Article V and the Authority
Precedence in AGENTS.md/CLAUDE.md, the Constitution outranks the ADR — so on the current
record, Model B is **not** in force.

**Options.**
- (a) Reject Model B; re-home SPEC-002 inside Article V (e.g. as an APS document or an annex to APS-001).
- (b) Adopt Model B via Constitution amendment under Article XI, then accept ADR-001_DOCUMENT_MODEL.
- (c) Leave unresolved and proceed. **Not viable** — it means authoring ADRs into an undefined hierarchy.

**Recommended option.** **No recommendation — architectural decision required.** This is a
constitutional question about how the project structures its normative corpus, and the
evidence supports neither answer over the other. What the review *can* say is that (c) is not
an option, and that whichever is chosen must be recorded before any further SPEC or ADR is
authored.

**Impact.** Blocks the placement of SPEC-002 and of every ADR in the package.

**Required ADR/RFC.** **RFC**, and under option (b) a Constitution amendment (Article XI:
RFC + Architecture Review + impact analysis + dependent-document updates + Chief Architect
approval).

**Blocking level.** **P0** — BLOCKER-P0-005.

---

## OD-004 — What is the acceptance bar for an AD-CA-class ADR?

**Question.** Does an ADR resolving an AD-CA domain follow GOV-001 §5.2 (RFC → 14-day comment
→ ARB → Chief Architect) or GOV-001 §6 (PR merge = ACCEPTED, one reviewer)?

**Why it matters.** Under §6, an ADR fixing canonical bytes could be accepted by a single PR
merge. Every AD-CA domain is a "Major Change" by §5.2's own test ("new requirements, new
invariants, new conformance tests, behavioral changes").

**Current evidence.** GOV-001 §5.2 and §6 are both live and mutually inconsistent. GOV-001 is
itself `1.0-DRAFT`. GOV-001 §9 and Constitution Article VIII forbid AI self-approval, but do
not settle the human bar.

**Options.**
- (a) All AD-CA ADRs are Major Changes: RFC mandatory, §6 applies only to ADRs recording decisions already approved by RFC.
- (b) §6 governs ADRs generally; RFC required only where an invariant changes.
- (c) Amend GOV-001 to remove the contradiction and state one rule.

**Recommended option.** **(a), implemented via (c).** Every AD-CA domain fixes normative
behaviour and will require new invariants, which is squarely §5.2 territory; and GOV-001 §6's
"merging = accepting" should be narrowed to say that merge *records* an acceptance already
conferred, rather than *constituting* it.

**Impact.** Determines whether ADR-002…006 need RFCs. On the recommendation, they do.

**Required ADR/RFC.** RFC amending GOV-001 (Major Change per §5.2).

**Blocking level.** **P1** — BLOCKER-P1-001.

---

## OD-005 — Which document statuses may enter the Source Set?

**Question.** REQ-002-005 requires deciding which lifecycle statuses are permissible as
inputs. Which are?

**Why it matters.** Exactly one document in the repository is FROZEN. If the answer is "FROZEN
only", the Source Set is the Constitution alone. If DRAFT documents are admissible, the source
is mutable and the artifact is not reproducible over time — a DRAFT can change under a
registered artifact.

**Current evidence.** FROZEN: `AURA_CONSTITUTION.md` (AURA-CON-001 v1.0) — the only one.
DRAFT: APS-000/100/200/300/400/500/900/950, GOV-001, VERSIONING, INV registry, CONF-001…010,
SPEC-002. TODO: APS-001. `VERSIONING.md` §3 marks DRAFT as freely mutable.

**Options.**
- (a) FROZEN only. Source Set = the Constitution.
- (b) FROZEN + APPROVED.
- (c) Any status, pinned by content hash at construction time.

**Recommended option.** **(a) for the first artifact, with (b) as the target once APS documents
reach APPROVED.** (c) is superficially attractive but defeats REQ-002-005's purpose: pinning a
DRAFT by hash makes the artifact reproducible while leaving its *authority* undefined, which is
the confusion between integrity and identity that SPEC-002 §4.4 exists to prevent.

**Impact.** Determines the Source Set, hence AD-CA-001.

**Required ADR/RFC.** ADR closing AD-CA-001.

**Blocking level.** **P0** (component of BLOCKER-P0-001's domain).

---

## OD-006 — Is source canonicalization lossy or lossless?

**Question.** Is Constitution-source canonicalization (i) SHADOW_SPEC-like and lossy, (ii)
lossless byte-level normalization only, or (iii) a new pipeline?

**Why it matters.** The two reference implementations already disagree, and one of them
declares its own frozen normalization spec outside the APS/SPEC hierarchy.

**Current evidence.** `aura-guard-v1.3` `src/normalizer.rs` implements "SHADOW_SPEC v1.0": a
**strict ordered** pipeline — UTF-8 validation → NFKC → strip 21 enumerated hidden characters
→ confusable folding (Cyrillic/Greek/fullwidth) → ASCII lowercase — documented as "any
deviation invalidates the shadow hash". `aura-poc-a-core-v3.3` has **no canonicalization stage
at all**; `embed_text` consumes a raw `str`. SHADOW_SPEC's steps are **lossy** (lowercasing
and confusable folding are not reversible).

**Options.**
- (a) Lossless only — encoding, BOM, line endings, one Unicode normalization form. No case folding, no confusable folding.
- (b) Adopt SHADOW_SPEC v1.0 as the normative canonicalization.
- (c) A new pipeline defined from first principles under AD-CA-002.

**Recommended option.** **(a), with (c) as the vehicle.** SHADOW_SPEC was designed for
*regex-evasion defence* on adversarial input — a different problem from canonicalizing a
normative source text, where discarding case and folding homoglyphs destroys content the
document actually carries. Reusing it here would be adopting a tool for a purpose it was not
designed for. Note this recommendation concerns *suitability of purpose* only; the decision
remains AD-CA-002's.

**Impact.** Blocks AD-CA-002 and E1.

**Required ADR/RFC.** ADR closing AD-CA-002; an RFC if SHADOW_SPEC is to be promoted into the
normative hierarchy.

**Blocking level.** **P0** (component of ADR-002's domain).

---

## OD-007 — What does the token `32` mean in AD-CA-007's candidate list?

**Question.** In SPEC-002 §6 AD-CA-007, does the bare token `32` denote vector dimension or
integer width? And if not dimension, which decision domain owns dimension?

**Why it matters.** Cardinality determines canonical byte length and byte positions. Under
either reading, dimension is currently **not owned by any AD-CA row**.

**Current evidence.** SPEC-002 §6 lists candidates `32`, `100000`, `signed int32`,
`little-endian`, `round-half-to-even`. `signed int32` already covers width, which suggests `32`
means something else. Meanwhile RI-PY hard-codes **1536** in `core/embedding.py` and
`core/offline_normalizer.py` (`CONSTITUTION_DIM = 1536`, enforced with `ValueError`), and
`docs/architecture.md` and `docs/mathematical_foundation.md` describe 1536-dimensional space.

**Options.**
- (a) `32` means dimension → contradicts every implementation and document.
- (b) `32` means integer width (redundant with `signed int32`) → dimension is an unowned decision and must be opened.
- (c) `32` is a drafting artifact to be struck; dimension is opened explicitly under AD-CA-003 or AD-CA-007.

**Recommended option.** **(c).** The token is ambiguous as written, and the safest correction
is to remove it and state dimension as an explicit requirement — which is what proposed
REQ-002-036 does. This does **not** endorse 1536; it only makes the question visible.

**Impact.** Blocks AD-CA-007 and E3.

**Required ADR/RFC.** ADR closing AD-CA-007; a SPEC-002 editorial correction for the token.

**Blocking level.** **P0** (component of BLOCKER-P0-011's domain).

---

## OD-008 — Should provenance be inside artifact identity?

**Question.** REQ-002-033's open question: is execution/commit provenance included in,
excluded from, or externally bound to the canonical artifact and its hash domain? And
separately: must APS-200 §4 be corrected?

**Why it matters.** This is the CONTENT / IDENTITY / PROVENANCE separation. It is currently
**already decided by accident, in the wrong direction**, by a DRAFT normative document.

**Current evidence.** APS-200 §4 mandates for every entity both `created_at` (wall clock,
MUST) and `integrity_hash` = SHA-256 over that entity's canonical serialization (MUST).
An artifact modelled as an APS-200 entity therefore hashes differently on every construction —
same source, different hash — contradicting SPEC-002 §5.1 and Constitution Article IV P2.
Regarding the task's other provenance questions: Git commit is bound nowhere; compiler / OS /
language **do** currently change the vector across languages (OD-011, OD-012) although INV-006
says they must not; language versions are unbound because dependency closure (AD-CA-006) is
orphaned.

**Options.**
- (a) Provenance excluded from the canonical artifact; bound externally as separate evidence.
- (b) Provenance included in a separate, explicitly-defined hash domain, distinct from the artifact hash domain.
- (c) Provenance included in the artifact hash. **Incompatible with determinism** — this is what APS-200 §4 currently implies.

**Recommended option.** **(a) or (b) — and (c) must be ruled out explicitly.** The review does
not choose between (a) and (b): both preserve determinism, and the choice depends on whether
provenance must be tamper-evident *as part of* the artifact or alongside it, which is an
architectural judgement. What the evidence *does* establish is that (c) cannot stand, and that
**APS-200 §4 must be corrected regardless of which of (a)/(b) is chosen.**

**Impact.** Blocks AD-CA-009, AD-CA-010, E6, E7, E8.

**Required ADR/RFC.** ADR closing AD-CA-010, **plus an RFC amending APS-200 §4** (Major Change).

**Blocking level.** **P0** — BLOCKER-P0-007.

---

## OD-009 — How is the cross-repository APS identifier collision resolved?

**Question.** APS-200/400/500/900 denote different subject matter in `aura-specification` than
in `aura-poc-a-core-v3.3`'s GAP-001. Which is authoritative, and how is the other corrected?

**Why it matters.** Every cross-repository conformance claim is currently ambiguous between two
different specifications.

**Current evidence.** Spec repo: APS-200 = Canonical Data Model, APS-400 = Conformance Test
Matrix, APS-500 = Reference Fixtures, APS-900 = Compliance Mapping. GAP-001 §3: APS-200 = ARI
Engine, APS-400 = Serialization, APS-500 = ZK Layer, APS-900 = Conformance Runner. GAP-001
states it inferred requirements because *"the external `aura-specification` repository is not
co-located here"*.

**Options.**
- (a) Spec repo authoritative; GAP-001's matrix re-mapped to real APS IDs.
- (b) Spec repo authoritative; GAP-001's matrix withdrawn and re-derived after reading the real documents.
- (c) Renumber one side. **Rejected** — APS-000 §4 forbids identifier reuse and renumbering would break existing references.

**Recommended option.** **(b).** Re-mapping (a) assumes the underlying assessments are sound
and only mislabelled; but GAP-001 states outright that the requirements were inferred rather
than read, so the assessments themselves are unverified. Re-deriving is the honest repair.

**Impact.** Blocks all cross-repository traceability, hence `07_IMPLEMENTATION_CONFORMANCE.md`
becoming authoritative.

**Required ADR/RFC.** Correction to `aura-poc-a-core-v3.3`; no protocol change.

**Blocking level.** **P0** — BLOCKER-P0-010.

---

## OD-010 — Does ADP-001 exist, and what defines it?

**Question.** Should "ADP-001 — Aura Deterministic Projection" be created as a distinct
protocol document, or should the projection be defined directly under AD-CA-003?

**Why it matters.** ADR-003 is proposed to rest on ADP-001. A specification resting on a name
rather than a protocol cannot be independently implemented.

**Current evidence.** No document, identifier or definition exists in any repository. `ADP` is
not a registered prefix (APS-000 §3, Appendix A). Against the fourteen required definitions
(input, output, dimension, indexing, byte ordering, arithmetic, rounding, overflow, invalid
input, empty input, maximum input, determinism, domain separation, test vectors), ADP-001 is
**0/14**. The nearest existing artifact, `core/embedding.py`, is self-declared a *placeholder*
and exhibits undefined truncation/tiling, a scale that does not reach its documented 10⁵, and
sign-restricted output.

**Options.**
- (a) Create ADP-001 as a standalone protocol document via RFC, and register the `ADP` prefix.
- (b) Define the projection inside AD-CA-003/ADR-003; drop the ADP-001 label.
- (c) Defer projection entirely; resolve the other eleven domains first.

**Recommended option.** **(b).** A separate document and a new prefix add governance surface
without adding rigour, and the projection is already within AD-CA-003's stated scope
("transformation pipeline from source to artifact-ready representation"). If it later proves
independently reusable, it can be extracted under (a) then.

**Impact.** Blocks ADR-003 and E3.

**Required ADR/RFC.** **RFC** — this defines new protocol behaviour under GOV-001 §5.2 either way.

**Blocking level.** **P0** — BLOCKER-P0-008.

---

## OD-011 — What are the integer division and rounding semantics?

**Question.** For integer division in the canonical pipeline, does rounding floor toward −∞,
truncate toward zero, or follow euclidean semantics?

**Why it matters.** The languages disagree by default, and the current implementation has
adopted one by accident.

**Current evidence — reproduced.** `core/evaluator.py` applies Python's `//` (floors toward
−∞) at `dot // SCALING_FACTOR` and `weight_semantic * sa // SCALING_FACTOR`. Rust `/`, C/C++
`/` and JS `Math.trunc` truncate toward zero. Executed: `dot = -7000029999` → **−70001**
(Python) vs **−70000** (truncation); ARI path `sa = -70001` → **−49001** vs **−49000**.
Reachable through the public constructor, which accepts any `List[int]`. Defeats INV-002 and
INV-006, both Critical. *Not currently firing in the demo path* (the placeholder embedding
emits only non-negative components) and *invisible to existing CI* (x86 vs ARM comparison runs
Python on both sides).

**Options.**
- (a) Floor toward −∞ (matches current Python behaviour).
- (b) Truncate toward zero (matches Rust/C/C++/JS defaults).
- (c) Euclidean (always non-negative remainder).
- (d) Forbid negative intermediates entirely by construction, making the question moot.

**Recommended option.** **No recommendation between (a)–(c) — architectural decision
required.** All three are defensible; the choice trades off "least change to the existing
implementation" (a) against "least surprise to independent implementers in the majority of
target languages" (b). The review's substantive contribution here is that **(a) must not be
chosen by default merely because the implementation already does it** — SPEC-002 §3.4 forbids
exactly that inference. Option (d) is worth evaluating explicitly, since it would eliminate an
entire class of divergence rather than specifying around it.

**Impact.** Blocks AD-CA-007 and E4.

**Required ADR/RFC.** ADR closing AD-CA-007; RFC if it changes RI-PY's observable output.

**Blocking level.** **P0** — BLOCKER-P0-011.

---

## OD-012 — What is the float→fixed-point rounding mode?

**Question.** At the float→fixed-point boundary, what is the rounding mode, including tie
behaviour? And is any floating-point stage inside the reproducibility contract?

**Why it matters.** This is the **Constitution Vector construction path** — the artifact whose
identity all of SPEC-002 exists to pin down.

**Current evidence — reproduced.** `core/offline_normalizer.py` uses `round(x * SCALING_FACTOR)`.
Python's `round()` is **half-to-even**; C `round()` and Rust `f64::round()` are
**half-away-from-zero**; JS `Math.round` is **half-up**. Executed: `x*1e5 = 0.5` → **0** /
**1** / **1**; `x*1e5 = 2.5` → **2** / **3** / **3**. SPEC-002 §6 lists `round-half-to-even` as
a **candidate only**, and §3.4 states no candidate is a default — yet the implementation has
already committed to it. Separately, `normalize_vector` computes
`math.sqrt(sum(x * x for x in vector))`; IEEE-754 addition is non-associative, so this is
stable only under fixed summation order with no compiler reassociation, FMA contraction, or
vectorized reduction — none of which is specified. `CONSTITUTIONAL_DECREE.md` Article VII
*permits* float in this one file, but permission is not specification.

**Options.**
- (a) Half-to-even (matches current Python behaviour).
- (b) Half-away-from-zero (matches C/Rust).
- (c) Eliminate the float stage: derive the vector by integer-only arithmetic end to end, making the rounding question disappear.

**Recommended option.** **(c) if achievable; otherwise no recommendation between (a) and (b) —
architectural decision required.** (c) is worth serious evaluation because it also discharges
the unspecified-summation-order problem in the same move, and it aligns with the project's own
Zero-Float posture (INV-007). Where (c) is not achievable, the choice between (a) and (b) is
architectural, and — as with OD-011 — **(a) must not win by default merely because the
implementation already does it.**

**Impact.** Blocks AD-CA-007, E3, E4.

**Required ADR/RFC.** ADR closing AD-CA-007; RFC if RI-PY's output changes.

**Blocking level.** **P0** — BLOCKER-P0-011.

---

## OD-013 — What is CR-007?

**Question.** What are CR-007's inputs, outputs, authority, and pass/fail semantics?

**Why it matters.** ADR-006 must state CR-007's role in registration and freeze. It cannot do
so without inventing it.

**Current evidence.** SPEC-002 §2.2 forbids implementing it; §11 and Appendix B declare it
BLOCKED. **No document in either repository defines it.** `aura-poc-a-core-v3.3` defines
CR-001 (Art. 5 runtime conformance), CR-003 (Layer 0 statelessness) and CR-004 (append-only
evidence) — there is no CR-002, CR-005, CR-006 or CR-007. Review scoping states CR-007 "should
be a verifier, not a mechanism creating normative identity", which is a *constraint* on the
answer, not the answer.

**Options.**
- (a) Define CR-007 as a pure verifier: reads a registered artifact plus the specification, recomputes, compares, reports — creates no identity and confers no status.
- (b) Define it as a registration mechanism that also assigns identity. **Contradicts the stated constraint.**
- (c) Withdraw CR-007; fold verification into the conformance test suite (CONF-xxx).

**Recommended option.** **(a) or (c).** (a) matches the stated constraint directly; (c) is
cleaner governance, since a verifier that produces a pass/fail result against a specification
is precisely what a CONF test is, and a parallel `CR-` series duplicates the CONF namespace.
The review has no evidence favouring one, since CR-007's intended role is recorded nowhere.
(b) should be ruled out explicitly.

**Impact.** Blocks ADR-006 and E9.

**Required ADR/RFC.** ADR closing AD-CA-011/012, or an RFC if CR-007 becomes a protocol element.

**Blocking level.** **P1** — BLOCKER-P1-007.

---

## OD-014 — Who may confer FROZEN, and what happens to the self-frozen implementation?

**Question.** Is "FROZEN" conferrable only by the Chief Architect, and if so, what is the
status of an implementation that has declared itself frozen?

**Why it matters.** REQ-002-029 requires "the authority who may authorize freeze" and a
verification procedure. Neither is specifiable while "frozen" means two different things.

**Current evidence.** `VERSIONING.md` §3 reserves `APPROVED → FROZEN` to the Chief Architect
under Constitution Article XI. Yet `CONSTITUTIONAL_DECREE.md` Article VIII calls v3.3 the
"Frozen Iron Core"; `docs/architecture.md` closes with "Status: FROZEN — MC-READY 2026";
`AUDIT_LAYER_SPEC.md` is described as a "normative frozen spec". `reference/RI-PY_AURA_POC_A_CORE.md`
records the conflict itself — *"Self-declared FROZEN (v3.3) — this creates a governance
challenge as APS gaps require changes"* — alongside `APS-950 Certification Status: NOT CERTIFIED`.

**Options.**
- (a) FROZEN is conferred only by the Chief Architect. RI-PY's self-declaration is reclassified as a project-internal stability statement, not a governance status.
- (b) Implementations may self-freeze; the specification's FROZEN is a distinct concept with a distinct name.
- (c) Grandfather RI-PY v3.3 as frozen; all future work happens in v4.x.

**Recommended option.** **(a), with (c) as the practical consequence.** Two different things
must not share the word (that is what (b) concedes and then fails to fix by keeping both). The
deadlock is real and needs naming: a self-frozen, NOT CERTIFIED implementation **cannot be
corrected to meet the future contract without breaking its own freeze claim** — so the
corrections identified in this review (OD-011, OD-012, and the fail-open in
`vector_similarity_int32`) land in a v4.x lineage, exactly as `CONSTITUTIONAL_DECREE.md`
Article VIII already anticipates ("Any change to core logic creates a NEW INSTRUMENT").

**Impact.** Blocks AD-CA-012 and E9.

**Required ADR/RFC.** ADR closing AD-CA-012; coordination with the implementation repository's
Custodian.

**Blocking level.** **P1** — BLOCKER-P1-004.

---

## OD-015 — Are `VERIFIED` and `REGISTERED` new lifecycle states?

**Question.** Should the document lifecycle gain VERIFIED and REGISTERED states, or should
registration be modelled as an attribute rather than a state?

**Why it matters.** Review scoping asks for verification of `DRAFT → VERIFIED → REGISTERED →
APPROVED → FROZEN`. That lifecycle **does not exist** in the repository, so this is a new
decision affecting every artifact class, not a verification of an existing one.

**Current evidence.** `VERSIONING.md` §3 and GOV-001 §4 both define
`DRAFT → REVIEW → APPROVED → FROZEN (↘ DEPRECATED → ARCHIVED)`. Neither VERIFIED nor
REGISTERED appears anywhere. There is also no registry to register into: APS-000 §7 describes
a Canonical Registry that does not exist; only `INVARIANT_REGISTRY.md` is real.

**Options.**
- (a) Add both states to the universal lifecycle in `VERSIONING.md`.
- (b) Keep the universal lifecycle; model registration as an **attribute** of an artifact (`registered: true` + registry entry), orthogonal to status.
- (c) Define a separate lifecycle applying only to Constitution Artifacts, leaving documents on the existing one.

**Recommended option.** **(b).** SPEC-002 §8 already argues that registration and freeze are
*independent* concepts; modelling registration as a state on the same axis as APPROVED and
FROZEN re-couples what §8 separates, and forces every existing document through two new states
it has no use for. An attribute keeps them orthogonal, which is what §8 asks for.

**Impact.** Blocks AD-CA-011 and E9.

**Required ADR/RFC.** **RFC** amending `VERSIONING.md` and GOV-001 (Major Change).

**Blocking level.** **P1** — BLOCKER-P1-006.

---

## OD-016 — Who owns AD-CA-004 and AD-CA-006?

**Question.** Which governance artifact resolves AD-CA-004 (normalization rules) and AD-CA-006
(dictionary identity + dependency closure)?

**Why it matters.** Load-bearing, not bookkeeping. **AD-CA-004 blocks REQ-002-021/022** — the
requirements ADR-004 exists to close via AD-CA-008 — so **ADR-004 cannot close its own stated
scope while AD-CA-004 is unowned**. **AD-CA-006 blocks REQ-002-034**, so "same source → same
vector" remains unprovable: an undeclared dependency may vary between conformant
implementations without either violating anything.

**Current evidence.** Both verified present and UNRESOLVED in SPEC-002 §6 and Appendix A(E).
The five-ADR grouping covers ten of twelve domains; these two appear in none.

**Options.**
- (a) Extend the existing ADRs: AD-CA-004 → ADR-002 (it is canonicalization-adjacent); AD-CA-006 → ADR-003 (it is embedding-dependency-adjacent).
- (b) Author two additional ADRs (ADR-007, ADR-008).
- (c) Fold both into ADR-004, since both feed the canonical-bytes requirements.

**Recommended option.** **(a).** AD-CA-004 sits naturally beside AD-CA-002 — both concern
transforming source text into a canonical form — and AD-CA-006 sits naturally beside AD-CA-005,
which is itself about embedding-dependency identity. (c) would overload ADR-004, already the
highest-risk document in the package. (b) is acceptable but adds governance surface for no
analytical gain.

**Impact.** Blocks the coherence of the whole ADR package.

**Required ADR/RFC.** Scoping decision, recordable in each ADR's Context section.

**Blocking level.** **P0** — BLOCKER-P0-004.

---

## Summary

| OD | Subject | Level | Recommendation offered? |
|---|---|---|---|
| OD-001 | Authoritative repository | P0 | partial — (a)/(b), not (c) |
| OD-002 | AD-CA-005 scope | P1 | yes — (a) |
| OD-003 | Document model | P0 | **no — architectural** |
| OD-004 | ADR acceptance bar | P1 | yes — (a) via (c) |
| OD-005 | Admissible source statuses | P0 | yes — (a) → (b) |
| OD-006 | Lossy vs lossless canonicalization | P0 | yes — (a) via (c) |
| OD-007 | Meaning of `32` | P0 | yes — (c) |
| OD-008 | Provenance boundary | P0 | partial — rule out (c); APS-200 fix mandatory |
| OD-009 | APS ID collision | P0 | yes — (b) |
| OD-010 | ADP-001 | P0 | yes — (b) |
| OD-011 | Integer division semantics | P0 | **no — architectural**; (d) worth evaluating |
| OD-012 | Float→fixed rounding | P0 | partial — (c) if achievable, else architectural |
| OD-013 | CR-007 | P1 | partial — (a) or (c); rule out (b) |
| OD-014 | Freeze authority | P1 | yes — (a) with (c) |
| OD-015 | VERIFIED / REGISTERED states | P1 | yes — (b) |
| OD-016 | Orphaned domains | P0 | yes — (a) |

**16 open decisions. 10 at P0. None resolved by this review; none resolvable by an AI agent.**

---

*End of 06_OPEN_DECISIONS.md*
