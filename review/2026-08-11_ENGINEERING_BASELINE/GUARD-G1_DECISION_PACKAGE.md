# GUARD-G1 — DECISION PACKAGE (D1–D8)

**Date:** 2026-08-11
**For:** authorized decision-maker (audit-log format owner)
**Source:** `GUARD-G1_INTEGRITY_DESIGN_BRIEF.md`; `aura-guard-v1.3` @ `443f72e5`
**Mode:** decision support only. **No decision is made in this document.**

---

## 0. How to read this

**Candidates are not ranked and none is recommended.** No normative material in any
inspected repository authorizes a recommendation on any of D1–D8: `aura-guard-v1.3`
contains no governance document, and the specification corpus contains no requirement
addressing audit-record integrity coverage. Absent such authorization, this package lists
options and consequences only.

Candidates listed under "Candidate choices" are limited to those **explicitly supported by
existing repository material** — either named in the committed design brief, or present as
an established pattern in the code. Where the repository offers no candidate, the entry
reads **NO CANDIDATE IN REPOSITORY MATERIAL** rather than supplying one.

**Boundary labels** B1–B5 are as defined in `GUARD-G1_INTEGRITY_DESIGN_BRIEF.md` §11:

| | Where a binding on `violations` would sit |
|---|---|
| **B1** | inside the existing nine-field entry digest |
| **B2** | a separate per-entry digest, itself an input to the entry digest |
| **B3** | a separate per-entry digest, carried alongside, verified independently |
| **B4** | a parallel Merkle tree anchored in the segment manifest |
| **B5** | no cryptographic binding; compensating controls only |

**Shared factual baseline** (established in the brief, re-verified by executed tests —
see `GUARD-G1_CHARACTERIZATION_TESTS.rs` and §9 of this document):

- `chain_hash` digests nine fields joined by `"|"` (`src/chain.rs:36-48`); `violations` is
  not among them.
- Merkle leaves derive from `chain_hash` alone (`src/segment.rs:141-147`).
- `segment_chain_hash` and `tsa_message_imprint` derive from the Merkle root
  (`src/segment.rs:91-132`).
- Therefore the entry chain, the Merkle root, the segment chain and the RFC 3161 anchor
  all share one coverage boundary, and `violations` is outside all four.

---

## D1 — Disposition

**1. Decision question.** Is the current coverage of `violations` accepted as-is, mitigated
procedurally, or addressed cryptographically?

**2. Current factual state.** `violations` is persisted (`src/log_writer.rs:96`), returned
to the caller (`src/api/audit.rs:44`), and covered by no digest and no verification step.
`verify_chain` (`src/chain.rs:71-92`) checks two things per entry: `prev_hash` linkage and
digest recomputation over the nine fields.

**3. Evidence.** Executed: three mutation classes (emptied / rewritten / fabricated) all
pass `verify_chain` and all pass `verify_manifest_against_entries`; the control mutation of
a covered field fails both. 8/8 characterization tests green.

**4. Candidate choices.** B1, B2, B3, B4, B5 (brief §11). No further candidate appears in
repository material.

**5. Consequences.**

| | Detects §7 mutations | Changes existing digests | New verification step |
|---|:--:|:--:|:--:|
| B1 | yes | yes | no |
| B2 | yes | yes | no |
| B3 | yes | no | yes |
| B4 | yes, at segment granularity | segment layer only | yes |
| B5 | no | no | no |

**6. Compatibility.** B1/B2 invalidate every existing `chain_hash` under the new rule.
B3/B4 leave existing entries verifiable. B5 changes nothing.

**7. Security/integrity.** B5 leaves the exposure in place and makes it a documented,
accepted risk. B3/B4 introduce a control that a verifier can skip unless the design also
makes omission fail closed (see D2/§11 of the brief). B1/B2 make the control unskippable
because there is only one digest to check.

**8. Determinism.** B1–B4 all bring the `f32` `confidence` field into a digest unless D4
excludes it. B5 does not.

**9. Evidence required after the decision.** T-1, T-2, T-3, T-4, T-10, T-11 for B1–B4
(brief §13.2). For B5: a documented risk acceptance and a corrected README (`README.md:24`,
`:97`, `:265`; `docs/REPLAY_DEMO.md:50` currently claim "any" mutation is detected).

**10. NO DECISION MADE.**

---

## D2 — Retroactive verifiability

**1. Decision question.** Must logs written under the current rule remain verifiable after
the change ships?

**2. Current factual state.** `read_all_entries` (`src/log_writer.rs:151-170`) deserializes
without inspecting `schema`. `verify_chain` does not read `schema`. There is no version gate
on the audit-entry path.

**3. Evidence.** `src/api/audit.rs:132` sets `schema: "aura-guard.audit.v1"` as a literal
with no corresponding constant. Contrast `SEGMENT_SCHEMA` (`src/segment.rs:44`), which the
sealer does check for equality (`src/sealer.rs:100`).

**4. Candidate choices.** Required / not required. **No repository material states a
retention or re-verification requirement for historical audit logs**, so neither pole is
supported by evidence — this is an unconstrained choice.

**5. Consequences.** "Required" eliminates B1 and B2 from D1, since both redefine every
historical `chain_hash`. "Not required" leaves all five boundaries open.

**6. Compatibility.** This decision *is* the compatibility decision; D6 implements it.

**7. Security/integrity.** If "required" and no discriminator is added, a verifier cannot
distinguish a legitimately old entry from a new entry with the new field stripped — the
control becomes bypassable by deletion.

**8. Determinism.** None directly.

**9. Evidence required after the decision.** T-7 (migration: an entry spanning the change
point verifies under the specified rule, and an old-format entry is either accepted or
rejected per D6, never silently mis-verified).

**10. NO DECISION MADE.**

---

## D3 — Byte reduction of violation data

**1. Decision question.** What byte sequence is authoritative for violation data?

> **Explicitly not answered.** Task constraint: no serialization format is selected.

**2. Current factual state.** No canonical byte form for violation data exists. Violations
reach disk only through serde's derived `Serialize` (`src/log_writer.rs:96`), which is a
transport encoding, not a canonicalization: field order follows struct declaration order,
and `validator` is omitted entirely when `None`
(`src/models.rs:40` — `skip_serializing_if = "Option::is_none"`).

**3. Evidence.** Two reduction patterns exist in the codebase, **neither authorized for
this purpose**:

| Pattern | Site | Property |
|---|---|---|
| `"|"`-joined field concatenation | `src/chain.rs:36-47`; `src/segment.rs:98-105` | no escaping; a field containing `|` could collide |
| `serde_json::to_string` | `src/log_writer.rs:96` | not canonical; `Option` presence is variable |

**4. Candidate choices.** **NO CANDIDATE IN REPOSITORY MATERIAL.** The two patterns above
are observations about existing code, not candidates endorsed for violation data.

**5. Consequences.** Any reduction must be injective over the violation domain, or two
distinct violation lists digest identically and the control is defeated. Note that the
existing `"|"` pattern has no escaping rule, and `Violation.rule` / `Violation.action` /
`Violation.validator` are unconstrained `String`s (`src/models.rs:34-41`) — nothing prevents
a rule identifier containing `|`.

**6. Compatibility.** Determines whether the reduction can be recomputed from an already-
persisted JSONL line, or requires data not present on disk.

**7. Security/integrity.** Collision resistance of the *encoding* is a separate property
from collision resistance of SHA-256 and must be established independently. Empty-vector
versus absent-field, and `None` versus empty-string `validator`, are the two collision
cases visible in the current struct.

**8. Determinism.** An independent verifier in another language must reproduce the bytes
exactly. Field order, `Option` encoding, numeric formatting (D4) and escaping all bear on
this.

**9. Evidence required after the decision.** T-3 (known-answer vectors as checked-in
fixtures), T-4 (injectivity, including empty-vs-absent, `None`-vs-empty-string, and
separator-collision cases), T-6 (cross-toolchain reproduction).

**10. NO DECISION MADE.**

---

## D4 — Participation and representation of `confidence`

**1. Decision question.** Does `Violation.confidence` enter the digest, and if so in what
representation?

**2. Current factual state.** `confidence: f32` (`src/models.rs:38`). It is the only
floating-point value persisted to the audit log. It originates as `score: f32` in the policy
loader (`src/policy.rs:41`, `:94`), parsed from YAML by `serde_yaml`. It is currently
digested nowhere, so its representation has no integrity consequence today.

**3. Evidence.** No float participates in any digest anywhere in `aura-guard-v1.3`. Grep for
float usage returns four sites: `src/models.rs:38`, `src/policy.rs:41`, `:94`, and
`src/api/audit.rs:191` (latency metric, not persisted).

**4. Candidate choices.** Include / exclude. For representation: **NO CANDIDATE IN
REPOSITORY MATERIAL** — the codebase contains no precedent for reducing a float to bytes.

**5. Consequences.** Excluding it keeps the digest free of floating-point reduction
entirely and still binds `rule`, `action` and `validator` — the identifying content.
Including it binds the triage score as well, at the cost of introducing the first
float-to-bytes reduction in the codebase.

**6. Compatibility.** If included, the digest cannot be recomputed by a verifier that parsed
`confidence` into a different width than `f32`.

**7. Security/integrity.** If excluded, an operator can alter `confidence` undetectably
while `rule` and `action` stay bound. Whether that residual exposure matters is part of
this decision.

**8. Determinism.** Four concerns, all live only if "include" is chosen: `serde_json` float
formatting is shortest-round-trip (stable per toolchain, not specified); YAML literals such
as `0.7` are not exactly representable in binary32; an `f64` verifier obtains a different
value; nothing in the code prevents `NaN`/infinity reaching the field, and JSON represents
neither.

**9. Evidence required after the decision.** T-5 (boundary values: `0.0`, `1.0`, a value not
exactly representable in binary32, and the specified handling of `NaN`/infinity), plus T-6.

**10. NO DECISION MADE.**

---

## D5 — Hash domain

**1. Decision question.** Does the violation reduction belong to the existing entry-digest
domain, or to a distinct domain?

> **Explicitly not answered.** Task constraint: no hash domain is selected.

**2. Current factual state.** Two domains exist. The Merkle layer is domain-separated by
construction: leaves `SHA-256(0x00 || data)`, nodes `SHA-256(0x01 || left || right)`
(`src/merkle.rs:29-44`). The chain layer is not domain-separated: `compute_chain_hash`
(`src/chain.rs:36-48`) and `segment_chain_preimage` (`src/segment.rs:91-106`) both hash a
`"|"`-joined string with no domain tag.

**3. Evidence.** `src/merkle.rs:13-15` states the rationale for the existing separation:
"The `0x00`/`0x01` prefixes provide domain separation between leaf and interior node
hashes, defeating second-preimage attacks where a node hash could otherwise be passed off
as a leaf hash."

**4. Candidate choices.** **NO CANDIDATE IN REPOSITORY MATERIAL** for a third domain. The
RFC 6962 prefix scheme is cited above as an existing pattern and a documented rationale —
**not** as an endorsed candidate for this use.

**5. Consequences.** Sharing the entry-digest domain means one digest to verify. A distinct
domain means the violation digest cannot be confused with an entry digest or a Merkle node,
at the cost of a second verification concept.

**6. Compatibility.** Reusing the entry domain forces D1 toward B1/B2 and therefore forces
D2 toward "not required".

**7. Security/integrity.** Cross-domain confusion is the risk the existing `0x00`/`0x01`
scheme was introduced to prevent; the chain layer currently has no equivalent protection,
which is a pre-existing property, not a consequence of this decision.

**8. Determinism.** A domain tag is part of the byte reduction and must be specified with
D3, not separately.

**9. Evidence required after the decision.** T-3, T-4 (specifically: a violation digest must
not be constructible so as to be mistaken for an entry digest or a Merkle node hash).

**10. NO DECISION MADE.**

---

## D6 — Migration mechanism and schema discriminator

**1. Decision question.** How does a verifier know which digest rule applies to a given
entry?

**2. Current factual state.** Audit entries carry `schema: "aura-guard.audit.v1"` as a
string literal at the construction site (`src/api/audit.rs:132`), with no named constant.
No reader validates it. Segment manifests carry `SEGMENT_SCHEMA` (`src/segment.rs:44`) as a
public constant, and the sealer rejects manifests whose schema differs
(`src/sealer.rs:100`).

**3. Evidence.** The asymmetry above is the whole of the repository's material on this
question.

**4. Candidate choices.**

| | Supported by |
|---|---|
| Adopt the segment pattern for audit entries — named constant + equality check at the verifier | existing precedent, `src/segment.rs:44` + `src/sealer.rs:100` |
| Hard cut-over with no discriminator | consistent with D2 = "not required" |
| **No further candidate in repository material** | — |

**5. Consequences.** A discriminator lets one verifier handle both regimes. A hard cut
requires that historical logs be re-sealed, archived under the old verifier, or abandoned.

**6. Compatibility.** This is the implementation of D2 and cannot be settled before it.

**7. Security/integrity.** A discriminator that is read but not bound to the digest is
itself forgeable — `schema` is one of the five uncovered fields (brief §4). Making the
discriminator meaningful may require covering it, which widens scope (see brief §12 Q1).

**8. Determinism.** None directly.

**9. Evidence required after the decision.** T-7, T-8 (fail-closed on omission: an entry
with the new field stripped must be rejected, not silently treated as legacy).

**10. NO DECISION MADE.**

---

## D7 — Disposition of existing RFC 3161 tokens

**1. Decision question.** What becomes of timestamp tokens already obtained under the
current rule?

**2. Current factual state.** `tsa_message_imprint()` (`src/segment.rs:123-132`) hashes the
same preimage that produces `segment_chain_hash`, which contains the Merkle root, which
derives from `chain_hash`. A token therefore anchors the nine covered fields and nothing
else. Timestamping is opt-in and off by default (`docs/ROADMAP.md`, v1.4 section); tokens
exist only where an operator configured `AURA_TSA_URL`.

**3. Evidence.** `tests/fixtures/tsa/` contains `segment-001.tsr`, `segment-002.tsr` and
their manifests; `src/tst_verify.rs` (1,008 lines) performs offline RFC 5652 + PKIX
validation against operator-pinned roots.

**4. Candidate choices.** Tokens remain valid under the old rule / segments are re-sealed
and re-anchored / existing tokens are treated as covering the old field set only. All three
follow from the structure above; **no repository material states a policy.**

**5. Consequences.** Under B1/B2, an existing token continues to attest what it always
attested — a Merkle root over the nine-field digests. It does not become invalid; it becomes
*narrower in meaning* than a post-change token. Whether that distinction must be recorded is
part of this decision.

**6. Compatibility.** Re-anchoring requires a new TSA round-trip per historical segment and
is only possible where the TSA is still reachable and the operator still holds the
configuration.

**7. Security/integrity.** A mixed corpus in which some tokens cover violations and some do
not is a state an auditor must be able to distinguish; otherwise the stronger guarantee is
assumed for records that never had it.

**8. Determinism.** None directly.

**9. Evidence required after the decision.** T-9 (`segment_chain_hash` and
`tsa_message_imprint` behave as specified across the change), plus fixture coverage for a
mixed-regime corpus if one is permitted.

**10. NO DECISION MADE.**

---

## D8 — HTTP response shape

**1. Decision question.** Does the `/v1/audit` response change, and how are integrators
notified?

**2. Current factual state.** The handler returns `Json<AuditEntry>`
(`src/api/audit.rs:44`), i.e. the response body and the log line are the same struct.
`src/models.rs:46-48` states this explicitly: "The on-disk JSONL log uses the exact same
shape … This guarantees 1:1 replayability between the response and the log."

**3. Evidence.** `tests/integration.rs:122` asserts the response `chain_hash` is 64
characters; `:208-209` asserts `prev_hash` linkage across two responses. No test asserts the
response field set, so the shape is not currently pinned by any test.

**4. Candidate choices.** Response gains any new field alongside the log / response and log
diverge / no new field is added to either (follows from D1 = B1, which changes the digest
input without adding a field). Supported by the 1:1 property quoted above.

**5. Consequences.** Preserving 1:1 means any new field appears in both. Breaking it
removes a documented property that `src/models.rs:46-48` currently guarantees.

**6. Compatibility.** Adding a field to a JSON response is tolerated by most clients;
removing or renaming is not. Under B1 no field is added, so the response shape is unchanged
while its `chain_hash` values change.

**7. Security/integrity.** If the response omits a field the log carries, a caller cannot
independently verify the record it was handed.

**8. Determinism.** None directly.

**9. Evidence required after the decision.** A test pinning the response field set (none
exists today), plus T-11.

**10. NO DECISION MADE.**

---

## Dependency order

D2 constrains D1 (if retroactive verifiability is required, B1 and B2 are unavailable).
D3, D4 and D5 are one coupled reduction question and cannot be settled independently.
D6 implements D2. D7 and D8 follow from D1.

```
D2 ──► D1 ──┬──► D7
            └──► D8
D3 ◄──► D4 ◄──► D5      (coupled — settle together)
D2 ──► D6
```

---

## Standing statement

**NO DECISION MADE** on D1, D2, D3, D4, D5, D6, D7 or D8.

No serialization format is selected. No hash domain is selected. No schema is defined. No
candidate is ranked or recommended. G-1 is not implemented. DR-002 and NB-021 are neither
relied upon nor resolved. No production code was modified in producing this package.
