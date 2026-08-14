# 03 — D-3 Candidate Representation Classes

**All entries below are NON-NORMATIVE CANDIDATES.** None is selected, ranked or
characterised as recommended, preferred, best, safest, simplest or correct.
Letter order is arbitrary and is not an ordering of merit.

Legend: `00_…` §5. Question IDs refer to `01_…`.

---

## A — Delimiter-based encoding

**NON-NORMATIVE CANDIDATE**

- **Definition.** Values are converted to text and concatenated with a reserved
  separator; the digest is taken over the resulting byte string. Requires an
  escaping rule for any value that may contain the separator.
- **Source.** The shape currently in use: `SEP = "|"` with `.join(SEP)`.
- **Path / line.** `src/chain.rs:18–20`, `:35–48`.
- **Source status.** IMPLEMENTATION-DERIVED / NON-NORMATIVE. Its presence in the
  code is not evidence of suitability.
- **Advantages.** Human-readable preimage; debuggable; closest in shape to the
  observed behaviour; introduces no new primitives.
- **Limitations.** Injectivity depends entirely on the escaping rule. Nested
  structures need a second-level separator, whose interaction with the first must
  be specified. The current code has **no** escaping (`01_…` D3-Q-010).
- **Cross-language.** Straightforward, provided the escaping rule is specified
  precisely enough to be reimplemented without reading Rust.
- **Replay.** Verifier rebuilds the same string; must apply identical escaping.
- **Migration.** Historical entries are re-derivable from stored data, subject to
  the `None`/absent erasure noted in D3-Q-024.
- **Security.** The separator comment asserts it "must never overlap with hex,
  base64 or any timestamp character" (`src/chain.rs:18–19`) — **CONFIRMED that
  this assumption does not hold for `context`**, which is arbitrary caller text.
- **Ambiguity risks.** High without escaping; a crafted `context` can imitate
  field boundaries. Escape-of-escape must be defined.

## B — Length-prefixed encoding

**NON-NORMATIVE CANDIDATE**

- **Definition.** Each component is emitted as an explicit length followed by its
  bytes; no separators and no escaping.
- **Source.** No in-repo precedent found for the entry digest.
- **Path / line.** — (EVIDENCE GAP: no existing implementation to cite).
- **Source status.** NON-NORMATIVE CANDIDATE; a standard construction, not drawn
  from this codebase.
- **Advantages.** Injective by construction once the length encoding is fixed; no
  escaping rule to get wrong; nesting composes naturally.
- **Limitations.** Preimages are not human-readable; requires an integer encoding
  decision (D3-Q-003) including width and endianness; a length field is itself a
  parsing surface.
- **Cross-language.** Requires the integer encoding to be specified exactly;
  otherwise straightforward.
- **Replay.** Verifier reconstructs the byte stream; debugging a mismatch is
  harder than with a readable preimage.
- **Migration.** Same re-derivability position as A.
- **Security.** Removes the delimiter-collision class entirely; introduces
  length-field consistency as a new invariant.
- **Ambiguity risks.** Low, if the length encoding is total and unambiguous.

## C — Canonical JSON

**NON-NORMATIVE CANDIDATE**

- **Definition.** Serialize to JSON under a canonicalization profile (fixed key
  order, no insignificant whitespace, specified number and string escaping), then
  hash the resulting bytes.
- **Source.** JSON is already the storage format — but **not** canonicalized.
- **Path / line.** `src/log_writer.rs:96` (`serde_json::to_string`).
- **Source status.** IMPLEMENTATION-DERIVED for JSON-as-storage;
  **canonical JSON is not present in the codebase** and is a candidate only.
- **Advantages.** Reuses an existing format and an existing parse path; tooling
  exists in most languages; the digest input is inspectable.
- **Limitations.** Number canonicalization is the hard part, and `f32` is exactly
  the case that makes it hard (D3-Q-006). `skip_serializing_if` currently erases
  `None` (`src/models.rs:40`), so a canonical profile must state whether an
  omitted key and a null key are the same input.
- **Cross-language.** Depends on which canonicalization profile is named; two
  implementations of "canonical JSON" are not automatically the same function.
- **Replay.** Verifier must reproduce the serializer's exact output, not merely
  an equivalent document.
- **Migration.** Re-derivable, subject to the same `None` erasure.
- **Security.** Ties the digest to a serializer's behaviour unless the profile is
  fully specified independently of any library.
- **Ambiguity risks.** Moderate: string escaping choices (`\/`, `\uXXXX` case,
  surrogate handling) and number formatting are all profile-dependent.

## D — Canonical binary representation

**NON-NORMATIVE CANDIDATE**

- **Definition.** A purpose-defined binary layout: fixed field order, typed
  fields, explicit widths, defined endianness; floats, if included, as raw
  IEEE-754 bits.
- **Source.** No in-repo precedent for the entry digest.
- **Path / line.** — (EVIDENCE GAP).
- **Source status.** NON-NORMATIVE CANDIDATE.
- **Advantages.** No text-formatting dependency at all; `f32` becomes exactly
  reproducible as 4 bytes; no text-formatting ambiguity for numbers.
- **Limitations.** Preimages are opaque; the current pipeline builds a `String`
  before hashing (`src/chain.rs:35–48`, `src/crypto.rs:8–12`), so a binary
  representation cannot use `sha256_hex(&str)` as-is — though
  `sha256_bytes_hex(&[u8])` already exists (`src/crypto.rs:16`) — CONFIRMED.
- **Cross-language.** Good, provided endianness and widths are stated; raw
  IEEE-754 bits reproduce exactly where text renderings may not.
- **Replay.** Verifier reconstructs the byte layout; mismatch debugging is
  harder than with a readable preimage.
- **Migration.** Re-derivable, subject to the same `None` erasure.
- **Security.** Raw float bits make `-0.0` and `0.0` distinct digests
  (D3-Q-017) — a property that must be intended rather than inherited.
- **Ambiguity risks.** Low for numbers; strings still need a length or terminator
  rule, which folds back into B.

## E — Typed field encoding

**NON-NORMATIVE CANDIDATE**

- **Definition.** Each component is emitted as `(type tag, length, value)`, so
  the type is bound into the digest alongside the value.
- **Source.** No in-repo precedent.
- **Path / line.** — (EVIDENCE GAP).
- **Source status.** NON-NORMATIVE CANDIDATE.
- **Advantages.** A string `"1"` and an integer `1` cannot collide; adding a
  field type later does not silently alias an existing encoding; composes with
  nesting (D3-Q-013).
- **Limitations.** Highest byte overhead of the classes listed; requires a type registry that is itself
  versioned; over-specified if the domain stays all-strings.
- **Cross-language.** Good; the tag makes intent explicit to a reimplementer.
- **Replay.** As B, with an extra tag to agree on.
- **Migration.** Re-derivable; the type registry must cover every historical
  field.
- **Security.** Removes type-confusion collisions, a class the current
  all-strings preimage cannot express but a widened domain could.
- **Ambiguity risks.** Low; shifts risk to registry governance.

## F — Domain-separated structured encoding

**NON-NORMATIVE CANDIDATE**

- **Definition.** Any of A–E, plus an explicit domain tag bound into each digest
  so that a digest computed for one purpose cannot be presented as another.
- **Source.** Precedent exists in the codebase, but only in the Merkle layer:
  RFC 6962 `0x00` leaf / `0x01` node prefixes, with the second-preimage rationale
  stated in the module doc.
- **Path / line.** `src/merkle.rs:9–15`, `:29–34`.
- **Source status.** CONFIRMED as an existing precedent for the concept.
  **No convention exists for a third domain** — CONFIRMED. The precedent does not
  extend to the entry digest.
- **Advantages.** A violations sub-digest cannot be confused with a chain hash, a
  leaf hash or a segment hash; directly addresses D3-Q-022.
- **Limitations.** Requires allocating tag values and governing that allocation;
  interacts with the existing `0x00`/`0x01` space, which is RFC 6962's, not the
  project's, to extend.
- **Cross-language.** Neutral — it is an additive rule on top of the chosen base.
- **Replay.** Verifier must apply the correct tag; a wrong tag fails closed.
- **Migration.** If the tag enters the entry digest, historical digests change —
  the D-5 consequence set applies (`02_…` of the D-2/D-5 package, §5).
- **Security.** Addresses cross-domain second-preimage confusion directly.
- **Ambiguity risks.** Low; risk moves to tag allocation discipline.

## G — Hybrid: sub-digest composition

**NON-NORMATIVE CANDIDATE** *(added because the corpus makes it available)*

- **Definition.** Violations are reduced to a single sub-digest by one of A–F,
  and only that sub-digest enters the outer preimage as an ordinary component.
- **Source.** The corpus already uses digest-of-digest composition: the Merkle
  root is built from per-entry leaf hashes, and the segment preimage consumes the
  root rather than the entries.
- **Path / line.** `src/segment.rs:140–158`, `:91–106`.
- **Source status.** CONFIRMED as an existing structural pattern in the codebase.
- **Advantages.** The outer preimage stays flat and all-scalar, so D3-Q-013
  (nesting) is confined to the sub-digest; the sub-digest is independently
  inspectable and testable.
- **Limitations.** Introduces a second hash domain and therefore requires
  D3-Q-022 to be answered; adds an intermediate value that must itself be defined
  as present-or-absent for empty collections (D4-Q-008).
- **Cross-language.** Good; the sub-digest is a natural test-vector boundary.
- **Replay.** Two-stage verification; a mismatch localises to violations vs the
  rest of the entry, which is diagnostically useful.
- **Migration.** Depends on whether the sub-digest enters the outer preimage
  (history changes) or is carried alongside (history preserved) — that is a **D-2
  shape question already closed**, so its outcome constrains this candidate
  rather than the reverse.
- **Security.** Domain separation becomes mandatory rather than optional;
  without it the sub-digest is a bare SHA-256 like any other.
- **Ambiguity risks.** Low at the outer layer; all inner risks are inherited from
  whichever of A–F is used inside.

---

## Cross-candidate observations

**CONFIRMED — the candidates are not mutually exclusive.** F and G are modifiers
that compose with A–E. A decision will therefore likely be a *tuple* (base
encoding × nesting strategy × domain separation), not a single letter. This is
stated as a structural observation about the option space, not as guidance
toward any combination.

**CONFIRMED — one question cuts across all seven.** Every candidate must answer
the float question (D3-Q-006/017/018) and the `None`-vs-absent question
(D3-Q-007), because those are properties of the data, not of the encoding. No
candidate makes them disappear.

**EVIDENCE GAP.** No source states a required property against which these
candidates could be evaluated objectively — cross-language reproducibility is
documented as an intent for the Merkle layer only (`src/merkle.rs:1–5`), not for
the entry digest (`01_…` D3-Q-026).
