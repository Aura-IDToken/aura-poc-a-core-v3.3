# NORMATIVE_CORPUS_INVENTORY — D3-S8

**Phase 1.** Document identity verified from **content headers**, not filenames.
Repository: `AuraIDToken/aura-specification` @ **`62d2d6b`**, branch `main`.
**Normative effect: NONE.**

## 1. Inventory

| Document ID | Path | Version | Status | Classification (from content) | Sections relevant to DQ-001…008 |
|---|---|---|---|---|---|
| **AURA-CON-001** | `constitution/AURA_CONSTITUTION.md` | **1.0** | **FROZEN** | Constitution | Article V `:73-91` canonical hierarchy; Article VI `:95-107`; Article VII `:111` |
| **APS-000** | `aps/APS-000_FOUNDATION_AND_TERMINOLOGY.md` | 1.0-DRAFT | DRAFT | Normative | `:46-47` TERM-008 Audit Record; `:86` identifier format; `:117` MAY = Optional |
| **APS-001** | `specification/APS-001_PROTOCOL_SPECIFICATION.md` | **0.1-DRAFT** | **TODO** | Normative (stub) | Named in Constitution Art. V `:78` as tier 2 |
| **APS-100** | `aps/APS-100_PROTOCOL_INVARIANTS.md` | 1.0-DRAFT | DRAFT | Normative | `:58` INV-001, `:61` INV-002, `:64-65` INV-003, `:76-77` INV-007, `:83` INV-009, `:89` INV-011, `:92` INV-012, `:98` INV-014, `:101` INV-015; `:33` delegation to registry; `:148-156` Extension Rules |
| **APS-200** | `aps/APS-200_CANONICAL_DATA_MODEL.md` | 1.0-DRAFT | DRAFT | Normative | `:16` internal-structures clause; `:23,25` design principles; `:47-58` Common Object Contract; `:88` ENT-002 `input_hash`; `:104,108` ENT-003 `decision` + TODO; `:121` ENT-004; `:129` ENT-005 delegation; `:143` ENT-006; `:149-159` ENT-007; `:196` object_id traceability; `:203-207` validation; `:211-218` §8 serialization + TODO; `:224` schema TODO; `:238` ENT-007 traceability |
| **APS-300** | `aps/APS-300_EVIDENCE_MODEL.md` | 1.0-DRAFT | DRAFT | Normative | `:56` "at minimum"; `:59-71` Evidence fields; `:67-70` `input_hash`/`output_hash`/`evidence_hash`/`previous_evidence_hash`; `:73` TODO |
| **APS-400** | `aps/APS-400_CONFORMANCE_TEST_MATRIX.md` | 1.0-DRAFT | DRAFT | Normative | `:156` Critical violations |
| **APS-500** | `aps/APS-500_REFERENCE_FIXTURES.md` | 1.0-DRAFT | DRAFT | Normative | `:16` MUST pass unchanged; `:24-27` objectives incl. "Comparability"; `:35-44` fixture structure; `:38,79` `protocol_version` |
| **APS-900** | `aps/APS-900_COMPLIANCE_MAPPING.md` | 1.0-DRAFT | DRAFT | Normative | not DQ-relevant in inspected scope |
| **APS-950** | `aps/APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md` | 1.0-DRAFT | DRAFT | Normative | `:23` "Implement all mandatory APS requirements"; `:47-57` repo requirements; `:132-134` **RI registry** |
| **INV-REG-001** | `invariants/INVARIANT_REGISTRY.md` | 1.0-DRAFT | DRAFT | Registry | `:41-55` INV-002; `:63-77` INV-003; `:241-253` INV-011; `:261-283` INV-012; `:311-323` INV-014 |
| **SPEC-002** | `specification/SPEC-002_CONSTITUTION_ARTIFACT_CONTRACT.md` | **0.3-DRAFT** | **DRAFT** | Normative Contract | `:12` **"Normative effect: NONE until APPROVED"**; `:25-37` governing direction; `:45,95,108` non-approval clauses; `:124` REQ-002-006; `:141` REQ-002-014; `:186-195` §4.5 Hash Domains; `:208-211` architecture note; `:215-216` REQ-002-021/022; `:381-382` AD-CA-007/008 |
| **POL-VER-001** | `VERSIONING.md` | 1.0-DRAFT | (no Status line) | Policy | `:32` lifecycle; `:36-40` DRAFT="may change freely" |
| **CONF-001…010** | `conformance/CONF-*.md` | 1.0-DRAFT | DRAFT | Normative Conformance Test | CONF-002 `:40,46`; CONF-003 `:40,46`; CONF-006 `:40,46`; CONF-010 `:40` |
| **RI-PY** | `reference/RI-PY_AURA_POC_A_CORE.md` | — | — | RI status record | `:22,27,28` component status |
| **RI-RS** | `reference/RI-RS_AURA_GUARD.md` | v1.3.0 | **NOT CERTIFIED** (`:7`) | RI status record | `:7,22,35,50,52,60,62,74` |
| **ADR-001** | `adrs/ADR-001_DOCUMENT_MODEL.md` | — | **PROPOSED** | ADR | document model only; no hash/serialization content |
| Fixture schema | `fixtures/schemas/common-object-contract.schema.json` | — | `"_status": "TODO — pending finalization of APS-200"` | JSON Schema | `:11-14` required; `:35,39,48` |
| Fixture | `fixtures/core/FIX-001_BASIC_EVALUATION.json` | — | — | Fixture | `:8,17,18,19` — **all values `"TODO"`** |

## 2. APS-1000

**FACT.** **Not found in inspected scope.** `aps/` contains APS-000, 100, 200, 300, 400,
500, 900, 950 and a README. No APS-1000 exists in any branch of
`AuraIDToken/aura-specification` @ `62d2d6b`.

## 3. Status distribution — decisive for every DQ

**FACT.** Of the entire normative corpus, exactly **one** document is FROZEN:
`AURA_CONSTITUTION.md` (v1.0). **Every APS document, the invariant registry, SPEC-002,
the versioning policy and all ten CONF tests are `DRAFT`.** APS-001 — the tier-2 document
in the Constitution's own hierarchy (`Article V:78`) — is `0.1-DRAFT` with Status
**TODO**.

**FACT.** `VERSIONING.md:36-40` defines the lifecycle `DRAFT → REVIEW → APPROVED →
FROZEN` and defines DRAFT as "Under active authoring; **may change freely** — Mutable:
Yes". No APS document has entered REVIEW.

**INFERENCE.** Per D3-S8 safety rule 10 ("NO treating DRAFT documents as immutable
contracts"), every normative citation in this refresh is a citation to a **mutable**
source. This does not void the evidence; it bounds the durability of any decision taken
against it.

## 4. Open TODOs inside the normative corpus, by DQ

| TODO | Location | DQ affected |
|---|---|---|
| Canonical serialization format for RI-PY/RI-RS interop | `APS-200:218` | **DQ-006**, DQ-002 |
| Publish JSON Schema per entity | `APS-200:224` | DQ-006, DQ-001 |
| Canonical set of `decision` values | `APS-200:108` | **DQ-004** |
| `execution_id` format | `APS-200:78` | DQ-001 |
| Canonical schema for `request_fields` | `APS-200:94` | DQ-001 |
| Attestation lifecycle and authority | `APS-200:145` | — |
| Canonical algorithm for `evidence_hash` | `APS-300:73` | **DQ-002** |
| Evidence Pack container format / `pack_hash` | `APS-300:91` | DQ-002 |
| Conformance Test for INV-012 | `INVARIANT_REGISTRY.md:283` | DQ-001, DQ-002 |
| Conformance Test for INV-014 | `INVARIANT_REGISTRY.md:319` | **DQ-006** |
| CONF preconditions "once APS-200 schemas and APS-500 fixtures are finalized" | CONF-002/003/006 `:34` | DQ-006 |
| Fixture assignment for CONF-003 | `CONF-003:71,76` | DQ-006 |
| AD-CA-007 numeric representation **UNRESOLVED** | `SPEC-002:381` | **DQ-007** |
| AD-CA-008 canonical serialization + hash domains **UNRESOLVED** | `SPEC-002:382` | **DQ-002, DQ-006** |
