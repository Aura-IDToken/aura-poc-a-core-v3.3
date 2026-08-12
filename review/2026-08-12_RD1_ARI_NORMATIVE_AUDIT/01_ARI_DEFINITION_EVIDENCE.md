# RD-1 — 01 ARI DEFINITION EVIDENCE

Every ARI-bearing artifact found in either corpus. Quoted wording is verbatim.

---

## E-1 — Specification glossary (the only ARI text in the specification corpus)

| Field | Value |
|---|---|
| Document | `AuraIDToken/aura-specification` → `glossary/GLOSSARY.md` |
| Section | `## A`, line 27–28 |
| Version / status | repo @ `62d2d6b`; no per-entry version or status marker |
| Authority level | **2** (specification corpus) |
| Normative or implementation-derived | **Implementation-derived by construction** — it defines ARI *by naming the implementation* |

> **ARI** (Aura Reliability Index)
> A deterministic measurement value computed by RI-PY using integer arithmetic. ARI is a measurement, not a decision.

| D1 formula | D2 input domain | D3 dimensionality | D4 bounds | D5 integer semantics | D6 division | D7 rounding |
|---|---|---|---|---|---|---|
| ❌ | ❌ | ❌ | ❌ | partial — asserts "integer arithmetic", no semantics | ❌ | ❌ |

| D8 malformed input | D9 drift | D10 penalty | D11 serialization |
|---|---|---|---|
| ❌ | ❌ | ❌ (states ARI is not a decision) | ❌ |

**This is the highest-authority ARI text that exists.** It defines ARI by deferring to RI-PY.
See `05_CONFLICTS_AND_CIRCULARITIES.md` C-1.

---

## E-2 — RI-PY reference implementation document

| Field | Value |
|---|---|
| Document | `AuraIDToken/aura-specification` → `reference/RI-PY_AURA_POC_A_CORE.md` |
| Section | `## Role`, line 14 |
| Version / status | **Document ID RI-PY · Version v3.3 · APS-950 Certification Status: NOT CERTIFIED** · Last Review 2026-07-23 |
| Authority level | 2 by location; **but see below** |
| Normative or implementation-derived | **Implementation-derived** — it is a *status report about* an implementation |

> Layer 0 deterministic measurement engine. Computes ARI (Aura Reliability Index) scores via integer-only arithmetic. Does not make decisions — only measures.

All eleven dimensions: **❌**. RI-PY contains no formula, no domain, no bounds, no drift.

Relevant self-reported status:

> | RI-004 Conformance Runner | ❌ MISSING | No APS-400 conformance runner |
> | RI-005 Fixture Loader | ❌ MISSING | No APS-500 fixture support |
> | INV-010 | ❌ | No CONF-xxx tests |
> | INV-014 | ❌ | No fixture runner |
> | /fixtures | ❌ MISSING |

Per rule **R2**, RI-PY's description cannot be treated as normative unless the governing corpus
grants it that authority. It carries `NOT CERTIFIED` — the corpus withholds the grant.

---

## E-3 — Normative APS documents: ARI absent

Measured directly (`grep -cw ARI`) on the markdown documents that constitute the normative
specification:

| Document | Tier | ARI occurrences |
|---|---|---|
| `aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` | terminology | **0** |
| `aps/APS-100_PROTOCOL_INVARIANTS.md` | **invariants (level 3)** | **0** |
| `aps/APS-200_CANONICAL_DATA_MODEL.md` | data model | **0** |
| `aps/APS-300_EVIDENCE_MODEL.md` | evidence | **0** |
| `aps/APS-400_CONFORMANCE_TEST_MATRIX.md` | **conformance matrix (level 5)** | **0** |
| `aps/APS-500_REFERENCE_FIXTURES.md` | **fixtures** | **0** |
| `aps/APS-900_COMPLIANCE_MAPPING.md` | compliance mapping | **0** |
| `aps/APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md` | RI requirements | **0** |
| `specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` | **v0.3-DRAFT, Status DRAFT** | **0** |

**No normative specification document mentions ARI at all.** The Protocol Invariants register
and the Conformance Test Matrix — the two artifacts that would carry a binding ARI requirement
— are silent.

---

## E-4 — PDF snapshots (UNKNOWN, per rule R4)

Three PDFs matched the byte sequence `ARI`: `APS-400 — Conformance Test Matrix_260723_193617.pdf`,
`APS-500 Reference Fixtures_260723_194023.pdf`, `APS-900 — Compliance Mapping_260723_194128.pdf`.

Each yields **exactly one** raw byte-match, inside `FlateDecode`-compressed streams, with no
text layer extractable by available tooling. A single compressed-stream byte match is not a
readable occurrence and **is not treated as evidence of a definition**. Their markdown
counterparts (E-3) contain zero ARI.

**Classification: UNKNOWN — not text-extractable.** If the Authority requires these snapshots
adjudicated, that needs tooling this session does not have.

---

## E-5 — Implementation-repo: `docs/mathematical_foundation.md`

| Field | Value |
|---|---|
| Document | `aura-poc-a-core-v3.3` → `docs/mathematical_foundation.md` |
| Section | `## Agent Reliability Index (ARI)`, lines 3–59, 80–95 |
| Version / status | line 205–207: **`## Status` → `FROZEN — Regulatory Audit Phase (MC-READY 2026)`** |
| Authority level | implementation-repository documentation — **no level in the ladder**; NB-021 CASE A classes it as documentation |
| Normative or implementation-derived | **Implementation-derived / descriptive.** Contains no `MUST`/`SHALL`; the string `normative` does not appear in the file |

> ```
> RAW_ARI = 0.3 × StructuralIntegrity + 0.7 × SemanticAlignment
> ```
> - **StructuralIntegrity (SI)**: Binary validation ∈ {0, SCALING_FACTOR}
> - **SemanticAlignment (SA)**: Integer fixed-point dot product of pre-normalized int32 vectors
>   - Range: approximately [−10^5, 10^5]; clamped to [0, 10^5] in final RAW_ARI

> ```
> ARI = max(0, RAW_ARI − P)
> ```

> ```
> RAW_ARI ∈ [0, 100000]  (int32, scaled by 10^5, Layer 0)
> ```

> ```python
> dot = sum(a * b for a, b in zip(event_vector_int32, constitution_int32))
> sa  = dot // SCALING_FACTOR   # rescale: [−10^10, 10^10] → [−10^5, 10^5]
> ```

| D1 formula | D2 input domain | D3 dimensionality | D4 bounds | D5 integer semantics | D6 division | D7 rounding |
|---|---|---|---|---|---|---|
| ✅ shape | partial — "pre-normalized int32", unconstrained | ⚠ `1536` appears only in the **legacy / offline** section (l.118–128), not as a runtime constraint | ✅ states `[0,100000]` — **contradicted by implementation**, see C-2 | ✅ integer-only | ⚠ **only by exhibiting Python `//`** — no language-independent rule | ❌ |

| D8 malformed input | D9 drift | D10 penalty | D11 serialization |
|---|---|---|---|
| ❌ | **❌ — no drift formula anywhere in the document** | ✅ shape `max(0, RAW_ARI − P)`; `P` owned by Layer 2, undefined here | ❌ |

**This is the only artifact in either corpus that states an ARI formula.** It sits outside the
authority ladder.

---

## E-6 — Implementation-repo: `docs/ADR_005_NO_FLOAT_RUNTIME.md`

| Field | Value |
|---|---|
| Section | `### 1. Bit-Identity Guarantee`, line 133 |
| Version / status | line 3 **`Status: APPROVED`**; line 397 **`Status: FROZEN (MC-READY 2026)`** |
| Authority level | repository ADR |
| Normative or implementation-derived | Asserts a semantic rule — **and asserts it incorrectly** |

> Integer division (`//`) is deterministic (truncation toward zero)

**This statement is false for the language the implementation uses.** Python `//` is *floor*
division (toward −∞). Verified: `-1 // 100000 = -1` (floor) versus `0` under truncation-toward-zero.

D6 division: **✅ stated — ❌ incorrect.** All other dimensions ❌. See C-3.

---

## E-7 — Implementation-repo: `docs/GLOSSARY.md`

| Field | Value |
|---|---|
| Section | `## ARI (Agent Reliability Index)`, lines 32–36 |
| Authority level | implementation-repository documentation |
| Normative or implementation-derived | Descriptive |

> A numerical measurement output produced by Aura Protocol representing the degree of consistency between declared specification and execution.
>
> ARI is a measurement value, not a compliance decision.

All eleven dimensions **❌**. Note the name differs from the specification glossary:
**"Agent Reliability Index"** here versus **"Aura Reliability Index"** in E-1.

---

## E-8 — `CONSTITUTIONAL_DECREE.md` (level 1)

`grep -iE "\bARI\b|reliability index|0\.3|0\.7"` → **zero matches.**

**The highest authority tier is entirely silent on ARI.** All dimensions ❌.

---

## E-9 — `core/evaluator.py` (implementation, level 9)

Per rule **R1**, recorded as behaviour, never as definition.

> ```python
> class PoCAEvaluator:
>     """Implementation of RAW_ARI formula: RAW_ARI = 0.3*SI + 0.7*SA"""
>     SCALING_FACTOR = 100000
>     ...
>     similarity = dot // self.SCALING_FACTOR
>     raw_ari = (self.weight_structural * si // self.SCALING_FACTOR) + \
>               (self.weight_semantic * sa // self.SCALING_FACTOR)
>     raw_ari = max(0, raw_ari)
>     drift = min(max(0, self.SCALING_FACTOR - sa), 2 * self.SCALING_FACTOR)
> ```

Behaviour established by execution during this audit:

| Probe | Result |
|---|---|
| Dimensionality enforcement | **none** — `zip` truncates silently; 1-dim vector against 4-dim constitution returns `{'ari': 100000, 'drift': 0}` (CORE-P0-001) |
| Upper bound enforcement | **none** — over-scaled input returns `{'ari': 7030000, ...}`, 70× the documented ceiling (CORE-P1-004) |
| Division at two sites | `dot // SCALING_FACTOR`, then `weight * sa // SCALING_FACTOR` — floor applied twice |
| Drift clamp | code clamps to `2 × SCALING_FACTOR` = 200000, while the adjacent comment says "Clamp drift to [0, 100000]" |

D9 drift: the implementation is the **only** artifact in either corpus that determines drift.

---

## E-10 — `compliance/evaluator_wrapper.py` (implementation, level 9)

> ```
> 4. Layer 2 applies penalty: adjusted_ARI = max(0, RAW_ARI - P)
> ```
> ```python
> penalty = RegulatoryPolicy.calculate_penalties(sa)
> adjusted_ari = max(0, result["ari"] - penalty)
> ```

D10 penalty: implementation-derived only.

---

## E-11 — Existing tests

| Artifact | Content | Encodes a normative ARI? |
|---|---|---|
| `core/test_ari.py` | `assertGreater(result["ari"], 95000)`, `assertLessEqual(result["ari"], 50000)`; values `95000`, `85000` used as *inputs* to Merkle/certificate tests | **No** — bounded assertions only, no exact expected ARI output |
| `core/test_ari_observability.py` | five implementation-derived observations, explicitly `normative_effect: NONE` | **No** — self-declared characterization |

## E-12 — Fixtures

`find` for `*fixture*`, `*golden*`, `*vector*.json` across the implementation repo → **none**.
APS-500 (specification fixtures) contains **0** ARI. RI-PY reports `/fixtures ❌ MISSING`,
`RI-005 Fixture Loader ❌ MISSING`, `INV-014 ❌`.

**No ARI fixture exists anywhere in either corpus.**

## E-13 — Conformance and traceability material

| Artifact | ARI content |
|---|---|
| `docs/conformance/` (implementation repo) | contains only `README.md` — no matrix |
| `aps/APS-400_CONFORMANCE_TEST_MATRIX.md` | **0** |
| `conformance/CONF-001…CONF-010` | no ARI-bearing conformance test |
| `compliance/TRACEABILITY_MATRIX.md`, `TRACEABILITY_MODEL.md` | no ARI trace |
| implementation repo traceability matrix | **does not exist** |
