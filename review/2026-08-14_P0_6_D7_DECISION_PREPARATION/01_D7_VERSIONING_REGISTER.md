# 01 — D-7 Versioning / Discriminator Register

Register format per question: **A** what must be defined · **B** existing
evidence · **C** NON-NORMATIVE CANDIDATES · **D** evidence required ·
**E** consequences · **F** dependencies · **G** current status.

Permitted statuses: **OPEN · EVIDENCE GAP · NORMATIVE STATUS UNRESOLVED ·
DEPENDENT · DECISION-READY.** Candidate letters refer to `02_…`.

Legend: `00_…` §4. Repository/commit for all `src/…` citations:
`aura-guard-v1.3` @ `443f72e`.

---

## Baseline facts used repeatedly

Stated once; referenced by number below.

| # | Fact | Cite | Status |
|---|---|---|---|
| **F1** | The digest covers nine values joined by `SEP = "\|"`; `violations` is not among them | `src/chain.rs:20`, `:25–49` | CONFIRMED |
| **F2** | `schema: "aura-guard.audit.v1"` is an inline literal at the construction site; no named constant | `src/api/audit.rs:132` | CONFIRMED |
| **F3** | `schema` is **outside** the digest | `src/chain.rs:25–49` | CONFIRMED |
| **F4** | `schema` is **read by no verifier**: `read_all_entries` never inspects it; `verify_chain` never reads it | `src/log_writer.rs:151–170`; `src/chain.rs:71–92` | CONFIRMED |
| **F5** | `AuditEntry` carries **no** `#[serde(deny_unknown_fields)]`, and `#[serde(default)]` appears only on `request_id` and `Violation::validator` | `src/models.rs:40`, `:65`; `:50–97` | CONFIRMED |
| **F6** | The segment path **does** check its schema and rejects on mismatch, in two places | `src/segment.rs:341–342`; `src/sealer.rs:100` | CONFIRMED |
| **F7** | Entry genesis is `SHA-256("AURA-GUARD-GENESIS-v1.3")`, with the doc-comment "It must never be changed without bumping the protocol version" | `src/crypto.rs:25–30` | CONFIRMED |
| **F8** | Segment genesis is `SHA-256("AURA-GUARD-SEGMENT-GENESIS-v1")` | `src/segment.rs:45–49` | CONFIRMED |
| **F9** | Merkle layer uses RFC 6962 domain separation `0x00`/`0x01` with an explicit second-preimage rationale; **no convention exists for a third domain** | `src/merkle.rs:9–15`, `:29–34` | CONFIRMED |
| **F10** | The exit-code contract is documented and framed as "the contract that SOC playbooks, supervisors and CI should be wired against"; it defines `0,1,2,3,4,5,6,78` and contains **no version/schema-mismatch code** | `docs/exit-codes.md` | CONFIRMED (quotation marked) |
| **F11** | An in-repo precedent exists for an **externally selected** verification mode: `aura-seal verify-tst` runs strict verification when `--tsa-roots` is supplied and imprint-only (v1.4 behaviour) when it is not, emitting a stderr warning | `src/bin/aura_seal.rs:90–96`, `:338–365`; `docs/segments-and-timestamping.md §Backward-compatible imprint-only mode` | CONFIRMED |
| **F12** | Real RFC 3161 tokens exist as committed fixtures over imprints derived from v1 chain hashes | `tests/fixtures/tsa/segment-00{1,2}.tsr`; `tests/tst_verify.rs:20–48` | CONFIRMED |
| **F13** | ADR-0001 is "Accepted in v1.3, still current" and describes the digest as "SHA-256 of canonical fields incl. `prev_hash`" **without enumerating them** | `docs/adrs/0001-hash-chain.md` | CONFIRMED (quotation marked) |

---

## D7-Q-001 — Is a version/discriminator required at all?

**A.** Whether the transition can be handled without any per-record or
per-corpus generation marker.
**B.** F1, F3, F4, F7. Today one hard-coded rule is applied to every entry
(`src/chain.rs:53–65`) — CONFIRMED. There is no selection mechanism of any kind.
**C.** A–G (`02_…`), including the null case: no discriminator, single-rule
verifier (expressed within candidates C and F).
**D.** Whether any record must remain verifiable across a rule change — which is
G-1/G-2/G-3 in `06_…`.
**E.** If no record must survive the transition, D-7 may reduce to "one rule,
one verifier". If any must, some generation-selection mechanism is entailed —
**INFERENCE** from F4 plus the D-5 baseline.
**F.** D-5 (whether legacy verifiability is required); D-1/D-2 (that the rule
changes at all).
**G. DEPENDENT** — on G-1/G-2/G-3.

## D7-Q-002 — What property must distinguish digest-rule generations?

**A.** The distinguishing property itself: a stored value, a structural
difference, a corpus boundary, or a derived property of the digest.
**B.** F1, F5, F7, F8. Three distinguishing properties already exist latently:
a stored `schema` string (F2, unused), a version-bearing genesis constant (F7,
per-chain not per-entry), and **structural shape** — because `AuditEntry` has no
`deny_unknown_fields` (F5), a record missing a newly required field fails
deserialization while a record carrying an unknown extra field parses silently.
**C.** stored marker (A/B); external context (C/E/F); structural/self-describing
(D/G).
**D.** Whether the property must be per-entry, per-file, per-segment or
per-deployment.
**E.** A per-entry property permits mixed-generation files; a per-corpus property
does not. Structural distinction is **asymmetric** — see D7-Q-011/013.
**F.** D-3 (whether the representation binds a marker), D-5 (granularity of the
boundary).
**G. OPEN**

## D7-Q-003 — Where could the discriminator reside?

**A.** The location(s) the decision admits.
**B.** Locations evidenced as available: (i) the `schema` field, F2/F3/F4;
(ii) inside the digest preimage, currently containing no marker, F1;
(iii) the segment manifest, which already carries and checks a schema, F6;
(iv) the genesis constant, which already encodes a version string, F7/F8;
(v) verifier invocation context, precedent at F11; (vi) record structure itself,
F5.
**C.** A (outside digest) · B (inside digest) · C (external to the record) ·
D (self-describing digest) · E (dual verification) · F (verifier families) ·
G (structural/genesis-anchored) — `02_…`.
**D.** Whether mixed-generation single files must be supported.
**E.** Location determines who can modify the discriminator and what a modification
costs — see `04_…` §1.
**F.** D-3 for (ii); D-5 for granularity.
**G. OPEN**

## D7-Q-004 — Must the discriminator itself be integrity-protected?

**A.** Whether the value that selects the verification rule is itself bound by a
digest.
**B.** F3/F4: today `schema` is neither protected nor read. F6: the segment path
*checks* its schema but the manifest `schema` is likewise **not** part of the
segment preimage (`src/segment.rs:91–106`) — CONFIRMED. So the existing precedent
covers **checking**, not **protecting**.
**C.** protected (B, D, parts of G); unprotected (A); not applicable (C, E, F).
**D.** None beyond the decision — the consequences are fully derivable.
**E.** Unprotected: the selector is editable by anyone who can write the log, and
editing it invalidates no digest (F3) — CONFIRMED. Protected: editing breaks the
digest, but a bootstrap ordering appears (D7-Q-006).
**F.** D-3 (a protected marker must be representable in the canonical form);
D7-Q-006.
**G. OPEN** — explicitly **not** answered "yes" by this package.

## D7-Q-005 — Can an unprotected discriminator safely select the verification rule?

**A.** Whether "safely" is achievable without protection, and under what
compensating conditions.
**B.** F3/F4. An unprotected in-band selector is writable by any actor with log
write access, and its modification breaks nothing — CONFIRMED. This is the same
write capability the whole P0-6 threat model already assumes (post-write
tampering).
**C.** unprotected + out-of-band cross-check; unprotected + fail-closed defaults;
protected instead (B/D); no in-band selector at all (C/E/F/G).
**D.** Whether the deployment model already constrains log write access (an
operational control, not a code fact) — **EVIDENCE GAP**.
**E.** If unprotected selection is admitted, downgrade becomes available by
construction (`04_…` §2). Whether that is acceptable depends on the threat model
the Authority adopts.
**F.** D7-Q-004, D7-Q-016.
**G. OPEN**

## D7-Q-006 — Can the verifier bootstrap trust in the discriminator?

**A.** How a verifier establishes which rule to use when the marker that says so
is inside the thing being verified.
**B.** Mechanically the ordering is: parse → select rule → recompute → compare
(`src/log_writer.rs:151–170` then `src/chain.rs:71–92`) — CONFIRMED. A marker
inside the digest is only *validated* at the compare step, i.e. after it has
already been used.
**C.** trial verification (attempt each supported generation, accept the one that
verifies); positional/structural determination (G); externally supplied
generation (C/F); marker authenticated by a separate artifact (e.g. a signed
manifest — note the segment manifest is itself unsigned in-repo, `src/segment.rs:74–87` — CONFIRMED).
**D.** Whether trial verification is acceptable, given it necessarily accepts
whichever generation verifies.
**E.** Trial verification dissolves the bootstrap problem but **admits any
generation the verifier still supports**, which is exactly the downgrade surface
(`04_…` §2). Structural determination avoids trust in a value but is coarse
(D7-Q-011/013).
**F.** D7-Q-004, D7-Q-005, D7-Q-016.
**G. OPEN**

## D7-Q-007 — Can the discriminator be derived externally rather than stored in `AuditEntry`?

**A.** Whether generation can be supplied by context rather than by the record.
**B.** **F11 — an in-repo precedent exists.** `aura-seal verify-tst` selects
strict versus imprint-only verification from the presence of a `--tsa-roots`
flag, with a stderr warning and the documented posture that "The strict mode is
the production default" (quotation, `docs/segments-and-timestamping.md`) —
CONFIRMED. Also available: file path/directory convention, deployment
configuration, or an operator-declared boundary `seq`.
**C.** C (external verifier selection) · F (verifier families) · E (dual).
**D.** Whether every consumer of the logs can be relied on to supply the correct
context — **EVIDENCE GAP**, tied to G-2.
**E.** Externally derived generation removes the in-record forgery surface and
relocates the risk to invocation: whoever controls the command line controls the
rule. F11 shows the project has previously accepted that trade for TSA
verification.
**F.** D-5 (boundary definition); D-6 (how a mis-selection is reported).
**G. OPEN**

## D7-Q-008 — Can the digest itself encode its generation unambiguously?

**A.** Whether the digest value or its construction can be self-describing.
**B.** **F9** — RFC 6962 domain separation already exists at the Merkle layer,
with a stated second-preimage rationale, and **no convention exists for a third
domain** — CONFIRMED. **F7/F8** — both genesis constants embed a version string,
so a generation marker already exists at the chain root, though per chain rather
than per entry.
**C.** D (self-describing digest via a domain tag bound into the preimage);
G (generation anchored at the genesis constant).
**D.** Whether per-entry or per-chain granularity is required (D7-Q-002).
**E.** A domain tag makes a digest unusable in the wrong generation — it fails
closed rather than mis-verifying. It does **not** by itself tell a verifier which
generation to try; unless combined with trial verification or an external
selector, self-description yields "this is not generation X" rather than "this is
generation Y". **INFERENCE** from F9.
**F.** D-3 (the tag must be part of the canonical representation — D3-Q-022/023);
D7-Q-006.
**G. DEPENDENT** — on D-3's accepted representation, which was not supplied
(`06_…` EG-1).

## D7-Q-009 — How does version selection interact with existing v1 entries?

**A.** What a post-transition verifier does with entries written under the
current rule.
**B.** Existing entries carry `schema: "aura-guard.audit.v1"` (F2) that nothing
reads (F4); their digests were computed under F1. Under a changed rule they fail
`recompute_for_entry` — CONFIRMED. `read_all_entries` parses them without
complaint provided the struct still deserializes (F5).
**C.** A/B/C/D/E/F/G all provide *some* answer; they differ in whether the
verifier can tell "old" from "tampered".
**D.** G-1 (do production v1 logs exist), G-3 (retention).
**E.** Without a working discriminator, a legitimate v1 entry and a tampered new
entry are indistinguishable — both surface as exit code `2`
(`src/bin/aura_replay.rs:113–119`; F10) — CONFIRMED.
**F.** D-5 (whether legacy must verify at all).
**G. DEPENDENT** — on D-5 inputs G-1/G-3.

## D7-Q-010 — How does version selection interact with new entries?

**A.** How entries written after the transition are identified.
**B.** New entries would be produced by the writer, so their marker (if any) is
under the project's control at write time — unlike legacy entries, which cannot
be retro-marked without rewriting them (which is a D-5 question).
**C.** All candidates.
**D.** None.
**E.** Asymmetry: new entries can carry any marker chosen; legacy entries carry
only `"aura-guard.audit.v1"` (F2) or nothing. **INFERENCE** — a scheme relying on
new-entry markers alone cannot classify legacy entries positively, only by
exclusion.
**F.** D-5.
**G. OPEN**

## D7-Q-011 — What happens when the discriminator is absent?

**A.** The defined behaviour for a record with no generation marker.
**B.** **F5 is decisive here.** With no `deny_unknown_fields` and defaults only on
two optional fields: a record **missing a required field** fails
`serde_json::from_str` and `read_all_entries` returns
`AuraError::PolicyParse { … "line {} not valid JSON" }`
(`src/log_writer.rs:163–166`) — CONFIRMED — which the exit-code contract maps to
`1` (runtime error / "malformed log"), **not** `2` (F10) — CONFIRMED.
**C.** treat absent as legacy; treat absent as invalid (fail closed); treat
absent as "determine structurally".
**D.** Whether absence must be distinguishable from deletion — an attacker who
strips a marker produces a record indistinguishable from a legitimately unmarked
one, unless absence is itself invalid.
**E.** "Absent ⇒ legacy" makes marker deletion a downgrade primitive
(`04_…` §2). "Absent ⇒ invalid" fails closed but rejects every existing v1 entry
by construction, which is a D-5 outcome, not a D-7 one.
**F.** D-5; D-6 (reporting); D7-Q-016.
**G. OPEN**

## D7-Q-012 — What happens when it is unknown?

**A.** Behaviour on a syntactically valid but unrecognised generation value.
**B.** No audit-path precedent (F4). The **segment** path rejects an unrecognised
schema with `SegmentError::BadSchema` (F6) — CONFIRMED — and the exit-code
contract routes segment-chain failures to `4` (F10).
**C.** fail closed (reject); fail open (attempt a default); attempt trial
verification; report as a distinct condition.
**D.** Whether a new failure class may be added to the documented exit-code
contract (F10) — that contract is framed as binding on SOC playbooks and CI.
**E.** Fail-open on unknown re-creates the downgrade surface. Fail-closed
requires operators to update verifiers before writers, an ordering constraint
that is an operational fact, not a code fact.
**F.** D-6 (exit codes); D-5 (rollout ordering).
**G. OPEN**

## D7-Q-013 — What happens when it is malformed?

**A.** Behaviour on a corrupt or type-invalid marker.
**B.** If the marker is a struct field with a wrong JSON type, deserialization
fails at `read_all_entries` → exit `1` (as D7-Q-011) — CONFIRMED. If it is a
well-typed but nonsensical string, nothing today inspects it (F4).
**C.** as D7-Q-012, plus: distinguish "malformed" from "unknown" in reporting.
**D.** Whether malformed and unknown must be separately reportable (D-6).
**E.** Today all three of malformed-marker, legacy-record and tampered-record can
collapse into a single operator-visible outcome. Separating them is a reporting
decision.
**F.** D-6.
**G. OPEN**

## D7-Q-014 — What happens when it claims a newer rule than the verifier supports?

**A.** Forward-compatibility behaviour.
**B.** No precedent on the audit path (F4). On the segment path, any non-matching
schema — newer included — is rejected (F6) — CONFIRMED.
**C.** reject (fail closed); verify what is understood and report partial;
attempt partial verification under the highest supported generation.
**D.** Whether partial verification may ever be reported as success — bears on
whether a verifier can silently under-verify a newer record.
**E.** Partial verification of a newer-claiming record is an under-verification surface: a record claiming
generation N+1 could be checked under generation N rules. **INFERENCE.**
**F.** D-6; D7-Q-016.
**G. OPEN**

## D7-Q-015 — What happens when it claims an older rule?

**A.** Backward-compatibility behaviour.
**B.** This is the downgrade-relevant direction. Today no claim is read at all
(F4), so the question does not yet arise.
**C.** accept under the older rule (legacy support); reject after a boundary;
accept only if corroborated externally (C/E/F).
**D.** Whether a corroborating boundary (e.g. a `seq` threshold, a sealed
manifest) is available — the segment manifest carries `first_seq`/`last_seq`
(`src/segment.rs`, manifest schema, CONFIRMED) and could in principle corroborate
a claim, though it is unsigned.
**E.** Unconditional acceptance of an older claim **is** the downgrade primitive
(`04_…` §2). Conditional acceptance requires the condition to be trustworthy.
**F.** D-5; D7-Q-016.
**G. OPEN**

## D7-Q-016 — Can downgrade attacks be detected?

**A.** Whether a verifier can distinguish a genuine legacy record from a
new-generation record presented as legacy.
**B.** Under today's architecture the question is vacuous — one rule, no
selection (F1, F4). Post-transition it becomes live. Relevant facts: an
unprotected marker is freely editable (F3); a protected marker breaks its digest
when edited; structural determination (F5) cannot be edited *away* without also
removing data.
**C.** protected marker; external corroboration; structural determination;
monotonic boundary (accept legacy only below a stated `seq`).
**D.** Whether an authoritative boundary can be published and trusted.
**E.** Detection is achievable under several candidates; **no candidate provides
it automatically**, and one (unprotected in-band marker, A) forecloses it by
construction. **INFERENCE** from F3.
**F.** D7-Q-004, D7-Q-005, D7-Q-011, D7-Q-015.
**G. OPEN**

## D7-Q-017 — Can a valid old entry be made to appear as a new entry?

**A.** Upgrade-direction confusion.
**B.** An old entry lacks whatever the new generation requires — most concretely,
its digest was computed without `violations` (F1) while D-1 mandates their
inclusion. Re-labelling it as new-generation would cause the new rule's
recomputation to fail — CONFIRMED as a mechanical consequence of F1.
**C.** —
**D.** None.
**E.** **INFERENCE:** the upgrade direction appears self-limiting: mislabelling
old-as-new produces a verification failure, not a false accept. It is therefore a
denial/confusion vector rather than an evidence-forging vector. This holds only
if the new rule genuinely differs in inputs, which D-1 guarantees.
**F.** D-3 (the actual new rule).
**G. OPEN** — recorded as low-consequence pending D-3 values (`06_…` EG-1).

## D7-Q-018 — Can a new entry be made to appear as an old entry?

**A.** Downgrade-direction confusion — the inverse and the materially dangerous
direction.
**B.** A new-generation entry contains `violations` in its digest; verified under
the old rule, `violations` is simply not read (F1) — so the old rule would
recompute over the nine fields only. **Whether that recomputation matches the
stored digest depends on D-3's accepted representation, which is not available to
this package** — `06_…` EG-1.
**C.** —
**D.** **The D-3 accepted values.** Without them, this question cannot be closed:
if the new rule leaves the nine-field preimage intact and adds a component, an
old verifier would compute a different digest and fail; if the new rule carries a
sibling digest instead, an old verifier could verify the nine fields
successfully and ignore the violations binding entirely.
**E.** In the second shape, downgrade yields a **silent loss of the D-1
property** while still reporting success. This is the single most consequential
open item in D-7.
**F.** **D-3 (hard)**, D-2 shape, D7-Q-016.
**G. DEPENDENT — EVIDENCE GAP (EG-1).**

## D7-Q-019 — How does D-7 interact with replay verification?

**A.** Which component selects the rule, and what replay reports.
**B.** `aura-replay` calls `verify_chain` unconditionally (`:113`), optional
lineage (`:134–153`), `verify_segment_chain` (`:175`),
`verify_manifest_against_entries` (`:194`), prints `CHAIN OK` (`:213`) —
CONFIRMED. No branch depends on any version input. Exit codes are a documented
contract (F10).
**C.** selection in the library (`verify_chain`); in the CLI; supplied by the
caller (F11 precedent).
**D.** Whether the exit-code contract may gain a new code (F10).
**E.** See `07_…`. Placing selection in the library makes every embedder inherit
it; placing it in the CLI leaves library users unversioned.
**F.** **D-6 (hard)**.
**G. DEPENDENT** — on D-6.

## D7-Q-020 — How does D-7 interact with Merkle verification?

**A.** Whether generation affects leaf/root computation.
**B.** `entry_leaf_hash` consumes only `chain_hash` (`src/segment.rs:140–150`);
`segment_merkle_root` consumes only leaves (`:151–158`) — CONFIRMED. So Merkle
inherits generation implicitly through `chain_hash`, and a segment mixing
generations would produce a root that no single rule reproduces.
**C.** per-segment generation uniformity; per-entry generation with mixed
segments; re-sealing (a D-5 matter).
**D.** Whether mixed-generation segments must be supported.
**E.** See `08_…`. A generation boundary that falls inside a segment is the
structurally hardest case.
**F.** D-5.
**G. OPEN**

## D7-Q-021 — How does D-7 interact with RFC 3161 / TSA evidence?

**A.** Whether generation selection affects timestamp verification.
**B.** The imprint derives from `segment_chain_preimage` → `merkle_root` →
`chain_hash` (`src/segment.rs:91–131`, `:140–158`) — CONFIRMED. Real tokens exist
(F12).
**C.** leave sealed history untouched; re-seal (D-5-C shape).
**D.** G-1/G-4 (whether production tokens exist beyond the fixtures).
**E.** See `08_…`. A token attests a past instant and cannot be re-issued for it.
**F.** D-5.
**G. DEPENDENT** — on D-5 and G-4.

## D7-Q-022 — What happens to existing TSA tokens under each candidate?

**A.** Per-candidate disposition of existing timestamp evidence.
**B.** F12; `08_…` §3 gives the per-candidate table.
**C.** —
**D.** G-4.
**E.** Candidates that leave sealed history verifiable under its original rule
preserve tokens; any path that recomputes `merkle_root` destroys their
verifiability irrecoverably.
**F.** D-5.
**G. DEPENDENT**

## D7-Q-023 — What evidence is required from production logs?

**A.** Facts about deployed logs needed before selection.
**B.** Not determinable from the repository. **No `.jsonl` file exists anywhere
in the repo** (`find -name "*.jsonl"` → empty) — CONFIRMED.
**C.** —
**D.** **G-1** — do production v1 logs exist, in what volume, spanning what
`seq` range?
**E.** If none exist, several candidates collapse to equivalent outcomes and D-7
simplifies dramatically.
**F.** D-5.
**G. EVIDENCE GAP (G-1)**

## D7-Q-024 — What evidence is required from external consumers?

**A.** Who verifies these logs besides the project.
**B.** The repository documents an intent for independent verifiability at the
**Merkle layer** — "verifiable with any off-the-shelf CT tooling"
(quotation, `src/merkle.rs:1–5`) — CONFIRMED. No equivalent statement exists for
the entry digest — EVIDENCE GAP.
**C.** —
**D.** **G-2** — are there external verifiers, integrators or auditors, and can
they be coordinated on a boundary?
**E.** External verifiers constrain candidates that require out-of-band context
(C/E/F): context that cannot be distributed cannot be relied upon.
**F.** D-5.
**G. EVIDENCE GAP (G-2)**

## D7-Q-025 — What evidence is required from retention obligations?

**A.** How long records must remain verifiable.
**B.** No retention statement found in the sources read — EVIDENCE GAP.
**C.** —
**D.** **G-3** — legal/compliance retention periods.
**E.** A long obligation forces long-lived multi-generation verification; a short
one may allow a clean cut-over.
**F.** D-5.
**G. EVIDENCE GAP (G-3)**

## D7-Q-026 — What dependency does D-7 impose on D-5?

**A.** Precisely which D-5 questions D-7 must answer first.
**B.** See `05_…` §3 for the evidence-backed graph.
**C.** —
**D.** —
**E.** D-5 strategies requiring per-record rule selection cannot be evaluated
until D-7 establishes whether a trustworthy selector exists.
**F.** Bidirectional (`05_…` E-05).
**G. OPEN**

## D7-Q-027 — What dependency does D-7 have on D-3/D-4?

**A.** What D-7 needs from the closed representation and semantics.
**B.** D7-Q-008 needs to know whether the representation admits a bound domain
tag; **D7-Q-018 needs to know the shape of the new rule** to determine whether
old-rule verification of a new record fails or silently succeeds. **The accepted
D-3/D-4 values were not supplied** — `06_…` EG-1.
**C.** —
**D.** EG-1.
**E.** One D-7 question (D7-Q-018) is **blocked**, not merely informed, by EG-1.
**F.** D-3 (hard), D-4 (soft).
**G. DEPENDENT — EVIDENCE GAP (EG-1)**

## D7-Q-028 — What dependency does D-7 have on the reference model?

**A.** What the future reference model must contain for D-7 to be implementable.
**B.** The D-3/D-4 package scoped six reference-model elements, one of which is
explicitly **"Version selection … Depends on D-7, not D-3/D-4"**
(`review/2026-08-14_P0_6_D3_D4_DECISION_PREPARATION/09_…` §4) — CONFIRMED.
**C.** —
**D.** —
**E.** D-7 supplies exactly one of the six reference-model elements; the other
five are already assigned to D-2/D-3/D-4. See `07_…` §1.
**F.** D-3, D-4.
**G. DEPENDENT**

## D7-Q-029 — What must be specified before implementation?

**A.** The minimum specification set for a D-7 implementation.
**B.** Derived from the questions above: the distinguishing property and its
location; its protection status; the selection algorithm; behaviour on absent /
unknown / malformed / newer / older; the reporting contract (D-6); and the
boundary definition (D-5).
**C.** —
**D.** —
**E.** Any of these left unspecified becomes an implementation choice — i.e. the
implementation would decide policy, which the governance model forbids.
**F.** D-5, D-6.
**G. OPEN**

## D7-Q-030 — What must remain unresolved until D-5?

**A.** Which parts of D-7 must **not** be settled before D-5.
**B.** `05_…` §3.2 lists them: the concrete boundary (which records are legacy),
whether legacy verification is retained at all, and the disposition of existing
TSA evidence. Each depends on G-1/G-2/G-3, which are outside the repository.
**C.** —
**D.** G-1, G-2, G-3.
**E.** Settling these inside D-7 would pre-empt D-5 — the governance sequence
places D-5 after D-7 precisely so the mechanism exists before the boundary is
drawn.
**F.** D-5.
**G. DEPENDENT**

---

## Register summary

| Status | Count | IDs |
|---|---|---|
| OPEN | 17 | 002, 003, 004, 005, 006, 007, 010, 011, 012, 013, 014, 015, 016, 017, 020, 026, 029 |
| DEPENDENT | 8 | 001, 008, 009, 019, 021, 022, 028, 030 |
| DEPENDENT + EVIDENCE GAP | 2 | 018, 027 |
| EVIDENCE GAP | 3 | 023 (G-1), 024 (G-2), 025 (G-3) |
| DECISION-READY | 0 | none individually — readiness is assessed for D-7 as a whole in `09_…` §5 |
| **Total** | **30** | |

**No question was added beyond the required thirty.** The evidence did not
demonstrate a need to expand the domain.
