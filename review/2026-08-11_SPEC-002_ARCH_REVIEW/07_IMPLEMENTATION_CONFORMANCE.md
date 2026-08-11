# 07 — Implementation Conformance

Document ID: REV-2026-08-11-007
Status: DRAFT — ANALYSIS ARTIFACT, NO NORMATIVE EFFECT
Date: 2026-08-11

---

## 0. What is being asked, and what is not

The question here is **not** "does the code work?" It is:
**"is the implementation consistent with the future SPEC-002 contract?"**

Two rules govern the answer and are applied without exception:

1. **The specification is never adjusted to fit the code.** Where the implementation does
   something the specification has not decided, the finding is *"the specification has not
   decided this"* — never *"the specification should say what the code does."* SPEC-002 §3.4
   forbids treating a candidate as a default, and the code has, in several places, already
   adopted candidates by accident.
2. **Assessment is against a contract that does not yet exist.** All twelve AD-CA domains are
   UNRESOLVED. So most verdicts below are **UNRESOLVED — cannot be assessed**, and that is the
   accurate answer, not an evasion. Where a verdict of NON-CONFORMANT is given, it is against
   something already binding: an existing Protocol Invariant, a FROZEN constitutional
   principle, or the implementation's own declared contract.

**Classification scheme (per task §13):** CONFORMANT · PARTIALLY CONFORMANT · NON-CONFORMANT ·
UNRESOLVED · OUT OF SCOPE.

---

## 1. Role classification — what each implementation actually is

The task (§14) requires separating reference implementation from mathematical prototype from
test oracle from demonstrator from normative artifact. Assessed from evidence:

| Component | Claimed role | **Actual role, on evidence** |
|---|---|---|
| `core/embedding.py` | embedding for ℝ¹⁵³⁶ | **Demonstrator.** Docstring line 3: *"Placeholder for deterministic embedding … MUST be frozen + reproducible in production."* Self-declared not-production. |
| `core/offline_normalizer.py` | offline pre-processor | **Mathematical prototype.** Float is permitted here by `CONSTITUTIONAL_DECREE.md` Article VII. Produces int32 vectors, but from *arbitrary caller-supplied floats*, not from any protocol source. |
| `core/evaluator.py` | Layer 0 measurement | **Reference implementation of the ARI formula** — genuinely integer-only, genuinely deterministic within Python. Not a Constitution Artifact implementation. |
| `audit/` | Layer 1 Merkle + ETC | **Reference implementation**, reasonably mature (53 tests). Out of SPEC-002 scope. |
| `compliance/` | Layer 2 policy | **Reference implementation.** Out of SPEC-002 scope. `GAP-001` §2.4 records **0 tests** for `certificate.py` / `renderer.py`. |
| `aura-guard-v1.3` (RI-RS) | Rust reference implementation | **Different product.** PII/prompt guard with hash-chained evidence. Contains no constitution, vector, or ARI code. |

> **Nothing in either repository is a normative artifact, and nothing should be treated as
> one.** `docs/specs/AUDIT_LAYER_SPEC.md` is described in-repo as a "normative frozen spec",
> but it sits in an implementation repository outside the APS/SPEC hierarchy and was never
> approved through GOV-001. Same for `SHADOW_SPEC v1.0` in RI-RS. Both are **de-facto
> normative artifacts living outside governance** — recorded as a finding, not accepted as
> authority.

---

## 2. The central finding

> **There is no Constitution Artifact implementation anywhere.**

Verified by directed search across both repositories:

- **No code path reads `AURA_CONSTITUTION.md`.** Not in RI-PY, not in RI-RS. The Constitution
  document and the "Constitution Vector" are entirely unconnected in code.
- `offline_normalizer.generate_sample_constitution` builds its vector from
  `[0.5 + 0.1 * (i % 10) for i in range(dimension)]` — a synthetic ramp, unrelated to any
  protocol source. The docstring says "for testing/demo purposes", and that is accurate.
- `PoCAEvaluator.__init__` accepts a `constitution_vector: List[int]` from the caller. **Where
  it comes from is outside the system.** There is no derivation, no provenance, no identity,
  no registration, no freeze.
- RI-RS: repository-wide search for `constitution`, `vector`, `ARI` returns **no matches in
  `src/`**.

**Consequence.** AD-CA-001 through AD-CA-012 have **zero implementation coverage**. The term
"Constitution Vector" in the PoC denotes *a caller-supplied int32 array*, not an artifact
derived from the Constitution. This is not a criticism of the PoC — it is a research prototype
and says so — but it means the estate contains no starting point for the SPEC-002 contract,
and any conformance claim that suggests otherwise is unfounded.

---

## 3. RI-PY (`aura-poc-a-core-v3.3`) — conformance against the future contract

| AD-CA domain | Implementation | Verdict | Basis |
|---|---|---|---|
| 001 source boundary | none | **UNRESOLVED** | no source is read |
| 002 source canonicalization | none | **NON-CONFORMANT** | `embed_text` consumes a raw `str`; no encoding, BOM, line-ending or Unicode normalization handling exists. Any source variation propagates silently into the vector. |
| 003 transformation pipeline | `core/embedding.py` | **NON-CONFORMANT** | self-declared placeholder; silent truncation past 1536 chars; cyclic tiling below it; neither specified |
| 004 normalization rules | none | **UNRESOLVED** | domain is orphaned in the ADR package too |
| 005 embedding method identity | none | **NON-CONFORMANT** | the method has no name, no version, no identifier, no integrity binding. REQ-002-012 requires exactly one, identified. |
| 006 dependency closure | none | **NON-CONFORMANT** | no dependency manifest; no dictionary; Python version unbound, and Python version *matters* (see §4.1) |
| 007 numeric representation | `evaluator.py`, `offline_normalizer.py` | **NON-CONFORMANT** | two reproduced cross-language divergences — §4.1, §4.2 |
| 008 serialization / hash domains | none | **UNRESOLVED** | no serializer. `GAP-001` §3 independently records "APS-400 Serialization ❌ Missing" |
| 009 identity model | none | **NON-CONFORMANT** | `reference/RI-PY_AURA_POC_A_CORE.md` records INV-015 ❌ *"No APS-000 identifiers in objects"* and INV-009 ❌ *"No protocol_version in evidence objects"* |
| 010 provenance | none | **UNRESOLVED** | no revision binding of any kind |
| 011 registration | none | **UNRESOLVED** | no registry exists to register into |
| 012 freeze | self-declared | **NON-CONFORMANT** | freeze asserted without the authority `VERSIONING.md` §3 reserves to the Chief Architect — §5 below |

**Totals: 0 CONFORMANT · 0 PARTIAL · 7 NON-CONFORMANT · 5 UNRESOLVED.**

---

## 4. Findings against *currently binding* requirements

These do not depend on any future decision. Each is assessed against an existing Protocol
Invariant or a FROZEN constitutional principle.

### 4.1 Integer division rounding — INV-002, INV-006 (both Critical)

`core/evaluator.py` applies Python's `//` at two points:
`similarity = dot // self.SCALING_FACTOR` and
`raw_ari = (…) + (self.weight_semantic * sa // self.SCALING_FACTOR)`.

Python `//` floors toward −∞; Rust `/`, C/C++ `/` and JS `Math.trunc` truncate toward zero.
Executed against the class, with a negative constitution component (reachable via the public
constructor, which accepts any `List[int]`):

```
dot                    = -7000029999
Python floor  (dot//S) = -70001
Rust/C++/JS trunc      = -70000
DIVERGENCE             = True
```
and on the ARI path with `sa = -70001`: Python `-49001` vs truncation `-49000`.

**Verdict: NON-CONFORMANT against INV-002 (Bit-Perfect Replay) and INV-006 (Platform
Independence)** — both declared *"MUST … on every conformant implementation"*, which is a
cross-implementation obligation, not a cross-architecture one.

**Scope, stated precisely.** The shipped `embed_text` emits only non-negative components, so
the divergence does not fire on the demo path today. The existing `compare-determinism` CI job
compares x86_64 against ARM64 with **Python on both sides**, so it structurally cannot detect
it. This is a **latent, reachable defect and a specification gap** — not a live production
failure, and it is reported as such. It becomes permanent if the instrument is frozen in this
state.

### 4.2 Float→fixed rounding mode — Constitution Article IV P2, and SPEC-002 §3.4

`core/offline_normalizer.py`: `int_vector = [round(x * SCALING_FACTOR) for x in normalized_vector]`.

Python `round()` is half-to-even; C `round()` and Rust `f64::round()` are half-away-from-zero;
JS `Math.round` is half-up. Executed:

```
       x*1e5  Python round   half-away (C/Rust)   half-up (JS)
      0.5000             0                    1              1  <-- DIVERGES
      2.5000             2                    3              3  <-- DIVERGES
```

**Verdict: NON-CONFORMANT.** This is the Constitution Vector construction path. SPEC-002 §6
lists `round-half-to-even` as a **candidate only** and §3.4 states no candidate constitutes a
default — the implementation has nevertheless committed to it silently, by using a language
builtin. This is the exact "implementation accident becoming protocol invariant" the review
task's §14 warns against.

### 4.3 Fail-open on mismatched vector dimensions — INV-008 (Critical)

`vector_similarity_int32` computes `sum(a * b for a, b in zip(v1, v2))`. Python's `zip`
silently stops at the shorter sequence. Executed with a 1536-dimension constitution and a
length-1 agent vector:

```
mismatched-length evaluate (len 1 vs 1536): {'ari': 0, 'drift': 200000}
```

No exception. No diagnostic. A confident numeric answer derived from 1/1536th of the data.

**Verdict: NON-CONFORMANT against INV-008 (Fail Closed)** and Constitution Article IV P6
(*"In the absence of valid input … execution MUST halt safely"*). Also the precise pattern
REQ-002-031 prohibits: a silent fallback that alters the result.

Note the contrast: `offline_normalizer.normalize_constitution_vector` **does** validate
dimension and raises `ValueError`. The two modules apply opposite policies to the same
property, in the same package.

### 4.4 Float determinism assumed, not established

`normalize_vector` computes `math.sqrt(sum(x * x for x in vector))`. IEEE-754 addition is not
associative; the result is stable only under fixed summation order with no compiler
reassociation, no FMA contraction, and no vectorized reduction. None of these is specified.

**Verdict: PARTIALLY CONFORMANT.** `CONSTITUTIONAL_DECREE.md` Article VII explicitly permits
float in this one file, so its *presence* is sanctioned. But permission is not specification —
the *semantics* remain unconstrained. Correctly classified as **offline/prototype behaviour**
per the review task's §14, and it must not become a protocol invariant by default.

### 4.5 Tolerance-based validation of a bit-exact artifact

`verify_unit_vector` accepts any magnitude within **±1%** of 10⁵ (`tolerance = 0.01`). A ±1%
band admits a very large set of mutually distinct vectors as "valid".

**Verdict: NON-CONFORMANT in role.** A tolerance check is a legitimate diagnostic and an
illegitimate identity check; nothing in the repository distinguishes the two, and the
function's name and pipeline position invite the conflation.

### 4.6 Internal contract disagreement on the vector

- `evaluator.py` documents its input as *"Pre-normalized int32 vectors … ||v|| = 10^5"*, sign-unrestricted.
- `embedding.py` produces `(ord(c) % 32) * 3125` → components in **[0, 96875]**, all non-negative, never unit-normalized, never reaching the documented 10⁵ (the comment `3125 = 100000/32` assumes a factor of 32, but `% 32` yields a maximum of 31).
- `offline_normalizer.py` produces genuinely unit-normalized, sign-balanced int32 vectors.

**Verdict: NON-CONFORMANT.** Two producers in one package emit vectors with incompatible
properties into one consumer. The consumer's similarity formula is only valid for the
normalizer's output; fed the embedder's output it computes a number with no defined meaning.

### 4.7 Comment/code disagreement on the drift clamp

`evaluator.py` comments *"Clamp drift to [0, 100000] to represent [0.0, 1.0]"* directly above
`drift = min(max(0, self.SCALING_FACTOR - sa), 2 * self.SCALING_FACTOR)`, which clamps to
**[0, 200000]**. Executed output confirms the code (`drift = 200000`).

**Verdict: PARTIALLY CONFORMANT** — minor, but drift is a published measurement field and
which bound is normative is unrecorded.

---

## 5. Governance conformance

### 5.1 Self-declared FROZEN without authority — NON-CONFORMANT

`VERSIONING.md` §3 reserves `APPROVED → FROZEN` to the Chief Architect under Constitution
Article XI. RI-PY declares itself frozen in at least three places:
`CONSTITUTIONAL_DECREE.md` Article VIII ("Frozen Iron Core"); `docs/architecture.md` footer
("Status: FROZEN — MC-READY 2026"); `AUDIT_LAYER_SPEC.md` ("normative frozen spec").

`reference/RI-PY_AURA_POC_A_CORE.md` records the problem itself: *"Self-declared FROZEN (v3.3)
— this creates a governance challenge as APS gaps require changes"*, alongside
`APS-950 Certification Status: **NOT CERTIFIED**`.

**The deadlock, named plainly.** A self-frozen, uncertified implementation cannot be corrected
to meet the future contract without breaking its own freeze claim. The fixes identified in §4
therefore belong to a **v4.x lineage**, exactly as `CONSTITUTIONAL_DECREE.md` Article VIII
already anticipates: *"Any change to core logic creates a NEW INSTRUMENT, not a new version."*
This is consistent, not contradictory — but it means **v3.3 can never become SPEC-002
conformant**, and that should be stated openly rather than discovered later. → OD-014.

### 5.2 Cross-repository APS identifier collision — NON-CONFORMANT

`docs/GAP-001.md` §3 assigns APS-200 = "ARI Engine", APS-400 = "Serialization", APS-500 = "ZK
Layer", APS-900 = "Conformance Runner". The specification repository assigns APS-200 =
Canonical Data Model, APS-400 = Conformance Test Matrix, APS-500 = Reference Fixtures,
APS-900 = Compliance Mapping.

GAP-001 states the cause outright: *"Requirements are inferred … as the external
`aura-specification` repository is not co-located here."*

**Violates** APS-000 §4 (identifiers unique, never reused) and **AGENTS.md rule 7**
(*"Compliance claims must not be inferred merely from architecture names or README
language"*). Every conformance claim in GAP-001's coverage matrix is ambiguous between two
different specifications, and the assessments themselves are unverified rather than merely
mislabelled. → OD-009.

### 5.3 De-facto normative artifacts outside governance — NON-CONFORMANT

`docs/specs/AUDIT_LAYER_SPEC.md` (RI-PY) and `SHADOW_SPEC v1.0` (RI-RS `src/normalizer.rs`)
both declare themselves normative and frozen. Neither passed through GOV-001, neither has an
APS or SPEC identifier, and both live in implementation repositories. Under Constitution
Article V an implementation is the *lowest* authority level; it cannot originate normative
specifications. SHADOW_SPEC is the more consequential of the two, because it is a
canonicalization pipeline — precisely AD-CA-002's subject matter — defined outside the
hierarchy that is supposed to decide it.

---

## 6. What is genuinely conformant — credit where due

The review would be inaccurate if it recorded only failures. The following are real and
should be preserved through any v4.x transition:

| Item | Assessment |
|---|---|
| **Zero-float runtime in `core/`** | **CONFORMANT** with INV-007. `evaluator.py` and `compliance/consistency.py` are integer-only; `check_2_integer_only.sh` enforces it in CI. Genuine and well executed. |
| **Layer separation (Layer 0 measures, Layer 2 decides)** | **CONFORMANT** with the intent of INV-013 and the Decree's Article I §6. Enforced by `check_3_layer_separation.sh` and `check_cr003_layer_boundary.py` (AST-based), not merely documented. |
| **Cross-architecture determinism CI** | **PARTIALLY CONFORMANT** with INV-006. A real x86_64 + ARM64 comparison over `determinism-report-*.json` that fails the build on divergence. Genuine evidence — but scoped to the ARI path, and Python-on-both-sides, so blind to §4.1/§4.2. |
| **Layer 0 statelessness (CR-003)** | **CONFORMANT** in its own terms. Both a runtime behavioural test and an AST structural check. Well-constructed evidence. |
| **Audit layer signing abstraction** | **CONFORMANT** with APS-950 §5 intent. `Signer`/`Verifier` ABCs with HMAC-SHA256, 53 tests, migration path to Ed25519 without API change. |
| **Honest self-assessment** | **CONFORMANT** with Constitution Article IV P4. `GAP-001.md`, `KNOWN_LIMITATIONS.md` and `RI-PY_AURA_POC_A_CORE.md` document failures candidly, including the self-freeze problem. This is unusual and valuable. |

The engineering discipline in the ARI/audit path is real. **The gap is not quality — it is
that this discipline has never been applied to the Constitution Artifact, because the
Constitution Artifact has never been implemented.**

---

## 7. RI-RS (`aura-guard-v1.3`)

| Aspect | Verdict |
|---|---|
| Constitution Artifact surface | **OUT OF SCOPE** — no constitution, vector, or ARI code exists in `src/` |
| Role as "Reference Implementation" per APS-950 §11 | **NON-CONFORMANT as listed.** APS-950 §11 lists RI-RS as an Active Reference Implementation of the Aura Protocol; it implements a different product (PII/prompt guard with hash-chained evidence log). It cannot serve as the second party for cross-language replay. |
| `SHADOW_SPEC v1.0` normalization | **NON-CONFORMANT in governance** (§5.3) — but technically the most rigorous canonicalization in the estate: strict ordering, enumerated character set, explicit invalidation rule. Worth studying as *input* to AD-CA-002, not as authority. |
| Deterministic execution, fail-closed, auditability | **UNRESOLVED for SPEC-002 purposes** — the code exists and appears disciplined, but it operates on a different object and cannot be assessed against a Constitution Artifact contract. |

---

## 8. Verdict summary

| Category | Count | Items |
|---|---|---|
| **CONFORMANT** | 5 | zero-float runtime; layer separation; CR-003 statelessness; audit signing abstraction; honest self-assessment |
| **PARTIALLY CONFORMANT** | 3 | cross-architecture determinism CI; float determinism in the normalizer; drift clamp |
| **NON-CONFORMANT** | 12 | AD-CA 002/003/005/006/007/009/012 coverage; integer division rounding; float→fixed rounding; fail-open on dimension mismatch; tolerance-as-identity; internal vector contract disagreement; self-declared freeze; APS ID collision; out-of-governance normative specs |
| **UNRESOLVED** | 5 | AD-CA 001/004/008/010/011 — cannot be assessed against an undecided contract |
| **OUT OF SCOPE** | 2 | RI-RS Constitution surface; `packages/zk-passport`, `packages/database-client` |

**Overall: the implementation estate is NOT a viable starting point for SPEC-002 conformance.**
Not because the code is poor — the ARI and audit layers are disciplined and well-tested — but
because the Constitution Artifact was never built, and the one component closest to it
(`embedding.py`) is a self-declared placeholder that has already, silently, committed the
protocol to two language-specific numeric behaviours.

**The specification MUST NOT be adjusted to match any of this.** Every finding in §4 is a
reason to *decide* the corresponding AD-CA domain deliberately — not a reason to ratify what
the code happens to do.

---

*End of 07_IMPLEMENTATION_CONFORMANCE.md*
