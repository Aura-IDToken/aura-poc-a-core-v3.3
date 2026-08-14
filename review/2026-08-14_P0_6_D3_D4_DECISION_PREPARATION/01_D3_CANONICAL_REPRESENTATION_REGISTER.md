# 01 — D-3: Canonical Representation Register

**Decision:** D-3 — *How is integrity-domain data reduced to bytes so that two
independent implementations produce an identical digest for an identical
`AuditEntry`?*
**Status:** OPEN. Nothing selected. Legend: `00_…` §5.

---

## 1. Observed representation today — IMPLEMENTATION-DERIVED / NON-NORMATIVE

Stated as fact about the code. **None of it is a normative baseline**, and none
of it is assumed correct.

| # | Aspect | Observed behaviour | Cite |
|---|---|---|---|
| 1.1 | Digest input | Nine values joined by `SEP = "\|"`, then SHA-256 | `src/chain.rs:20`, `:35–48` |
| 1.2 | Byte encoding | `sha256_hex(input: &str)` hashes `input.as_bytes()` — UTF-8 | `src/crypto.rs:8–12` |
| 1.3 | Integers | `seq: u64` rendered via `&seq.to_string()` — decimal, no padding | `src/chain.rs:44` |
| 1.4 | Timestamps | `Utc::now().to_rfc3339()` stored and hashed as text | `src/api/audit.rs:117` |
| 1.5 | Escaping | **None.** Caller-controlled `context` is joined unescaped into a `"\|"`-delimited preimage | `src/chain.rs:41` |
| 1.6 | Field order | Fixed by the argument order of `compute_chain_hash` | `src/chain.rs:26–34` |
| 1.7 | `violations` | Not in the digest at all today (the gap D-1 closes) | `src/chain.rs:25–49` |
| 1.8 | Storage form | `serde_json::to_string(entry)`; serde-derived, no canonicalization | `src/log_writer.rs:96` |
| 1.9 | `Option` fields | `validator`, `request_id` omitted entirely when `None` (`skip_serializing_if`) | `src/models.rs:40`, `:65` |
| 1.10 | Floats | `confidence: f32`, serialized by `serde_json` (shortest-round-trip); never hashed today | `src/models.rs:38` |
| 1.11 | Domain separation | Exists in the Merkle layer only: `0x00` leaf / `0x01` node, RFC 6962 | `src/merkle.rs:9–15`, `:29–34` |
| 1.12 | Normalization precedent | A frozen, strictly ordered pipeline exists (SHADOW_SPEC v1.0: NFKC → hidden-char strip → confusable fold → lowercase) — but it feeds the **regex engine only**; the module states the original text "is always preserved for the evidence hash" | `src/normalizer.rs:1–13` |

**CONFIRMED — a live equivalence hazard already in the data.** `Violation.action`
is stored as the raw YAML string (`src/engine.rs:51`), while decision logic
matches it case-insensitively via `to_ascii_lowercase()` (`src/engine.rs:44`).
Two violations with `action: "DENY"` and `action: "deny"` are therefore
**semantically identical to the engine but textually different in the record**.
Any representation that hashes the stored text distinguishes them; any
representation that normalizes case does not. This is not hypothetical — it is
reachable from ordinary policy authoring.

**CONFIRMED.** An unknown `action` value contributes nothing to the decision
(`src/engine.rs:47`, `_ => {}`) yet still produces a stored violation. The value
domain of `action` is therefore open in the data, not closed to
`deny|review|allow`.

---

## 2. Register — D3-Q-001 … D3-Q-026

Each entry: **QUESTION · WHY IT MATTERS · CURRENT EVIDENCE · CANDIDATES ·
CONSEQUENCES · DEPENDENCIES · EVIDENCE REQUIRED · STATUS.**
Permitted statuses: OPEN · EVIDENCE GAP · NORMATIVE CONFLICT · READY FOR HUMAN DECISION.
Candidate letters refer to `03_D3_CANDIDATES.md`.

---

**D3-Q-001 — Character encoding**
**Q:** Which character encoding defines the byte image of every string in the digest?
**Why:** Two implementations disagreeing on encoding produce different digests for identical data; this is the root of cross-language reproducibility.
**Evidence:** UTF-8 via `input.as_bytes()` — `src/crypto.rs:8–12` — IMPLEMENTATION-DERIVED. No specification states it.
**Candidates:** UTF-8 mandated; UTF-8 with explicit BOM prohibition; encoding declared per version marker.
**Consequences:** A verifier in another language must reproduce byte-identical encoding; unpaired surrogates and non-UTF-8 input must have a defined outcome (Rust `&str` forbids them, other languages do not).
**Dependencies:** D3-Q-019, D3-Q-026.
**Evidence required:** none beyond a decision.
**STATUS: OPEN**

**D3-Q-002 — String representation**
**Q:** How is a string value represented — raw bytes, quoted, escaped, length-tagged?
**Why:** Determines whether string content can imitate structure.
**Evidence:** raw, unquoted, unescaped, delimiter-joined — `src/chain.rs:35–47` — IMPLEMENTATION-DERIVED.
**Candidates:** raw+delimiter (A); length-prefixed (B); JSON-quoted+escaped (C); typed tag+length+bytes (E).
**Consequences:** raw+delimiter requires an escaping rule to be injective (D3-Q-010, D3-Q-021); length-prefixed removes the need for escaping but adds an integer encoding question.
**Dependencies:** D3-Q-009, D3-Q-010, D3-Q-020, D3-Q-021.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-003 — Integer representation**
**Q:** How are integers (`seq`, any counts, any length prefixes) represented?
**Why:** Decimal text, zero-padded text, and fixed-width big-endian binary give different digests.
**Evidence:** `&seq.to_string()` — decimal, unpadded — `src/chain.rs:44` — IMPLEMENTATION-DERIVED.
**Candidates:** decimal ASCII; zero-padded fixed width; big-endian `u64`; varint.
**Consequences:** decimal text needs a rule for leading zeros and for any future signed value; binary forms need endianness fixed.
**Dependencies:** D3-Q-020 (length prefixes are integers too).
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-004 — Boolean representation**
**Q:** How is a boolean represented, if any enters the domain?
**Why:** `true`/`1`/`0x01` are all defensible and mutually incompatible.
**Evidence:** **no boolean field exists in `AuditEntry` today** (`src/models.rs:50–97`) — CONFIRMED. `validator_passed` is internal only and never persisted (`src/engine.rs:32–42`).
**Candidates:** define now for future-proofing; declare booleans out of scope until one exists.
**Consequences:** deciding now avoids an ad-hoc choice later; deciding for a non-existent field risks specifying something unused.
**Dependencies:** D-2 membership.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-005 — Timestamp representation**
**Q:** Is the timestamp digested as stored text, or as a normalized instant?
**Why:** RFC 3339 admits multiple textual forms of the same instant — `Z` vs `+00:00`, and variable fractional-second digits.
**Evidence:** `Utc::now().to_rfc3339()` hashed as text — `src/api/audit.rs:117`, `src/chain.rs:45`. The in-repo manifest fixture shows the `+00:00` form with nine fractional digits: `"2026-05-20T20:22:47.560539282+00:00"` (`tests/fixtures/tsa/segment-001.manifest.json`) — CONFIRMED.
**Candidates:** hash stored text verbatim; mandate strict RFC 3339 UTC with `Z` and fixed precision; digest an integer epoch value.
**Consequences:** hashing text makes the digest sensitive to a formatting change in a dependency; normalizing requires a parse step in every verifier and a rule for unparseable historical values.
**Dependencies:** D-5 (historical values already written in one form).
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-006 — Float / `f32` representation**
**Q:** How is `Violation.confidence` (`f32`) represented in the digest — or is it excluded?
**Why:** This is the only floating-point value in the record and the principal cross-language reproducibility hazard.
**Evidence:** `confidence: f32` (`src/models.rs:38`), sourced from YAML `score: f32` (`src/policy.rs:41`, `:94`), currently never hashed — CONFIRMED. `serde_json` renders floats shortest-round-trip; stable per toolchain, not specified.
**Candidates:** rendered decimal text; fixed decimal places; fixed-point integer at a stated scale; raw IEEE-754 bits; exclusion from the digest.
**Consequences:** any text form binds the digest to a formatting library; a verifier parsing into `f64` obtains a different value than `f32`; exclusion leaves `confidence` mutable without detection, which interacts with what D-2 closed.
**Dependencies:** D3-Q-017, D3-Q-018, D3-Q-026; D-2 membership breadth.
**Evidence required:** whether `confidence` was inside the D-2 contract — see `00_…` §8.
**STATUS: OPEN**

**D3-Q-007 — `None` / null representation**
**Q:** How is an absent optional value represented in the digest?
**Why:** `validator: Option<String>` is `None` for every violation whose rule declares no validator.
**Evidence:** `skip_serializing_if = "Option::is_none"` — the key vanishes from JSON entirely (`src/models.rs:40`) — CONFIRMED. `None` means "no validator was configured"; a *failed* validator produces no violation at all (`src/engine.rs:32–42`, `continue`) — CONFIRMED.
**Candidates:** distinct null marker; empty-string equivalence; omit the component; length prefix of a reserved value.
**Consequences:** if `None` and empty string collapse, a future validator returning `""` becomes indistinguishable from no validator; if they are distinct, the representation must encode the distinction that JSON currently erases.
**Dependencies:** D3-Q-008, D3-Q-021; D4-Q-009.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-008 — Empty-value representation**
**Q:** How are empty values represented — empty string, empty collection, empty optional?
**Why:** Three different emptinesses currently all reduce to "nothing" in various paths.
**Evidence:** empty `Vec<Violation>` serializes as `[]` (`src/models.rs:90`); `prev_merkle_root` is an empty string for the first segment (`src/segment.rs`, fixture `"prev_merkle_root": ""`) — CONFIRMED, showing empty-string-as-sentinel already exists in the corpus.
**Candidates:** explicit empty marker; zero-length with length prefix; omission.
**Consequences:** an empty collection that contributes zero bytes is indistinguishable from an omitted collection — an injectivity failure (D3-Q-021).
**Dependencies:** D3-Q-007, D3-Q-021; D4-Q-008.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-009 — Separators / delimiters**
**Q:** Does the representation use delimiters, and if so which, with what guarantees?
**Why:** A delimiter that can occur inside a value destroys injectivity.
**Evidence:** `SEP = "|"` with the comment "Must never overlap with hex, base64 or any timestamp character" (`src/chain.rs:18–20`) — IMPLEMENTATION-DERIVED. **The comment's assumption does not hold for `context`**, which is arbitrary caller text and may contain `|` (`src/chain.rs:41`) — CONFIRMED.
**Candidates:** delimiter + escaping (A); no delimiter, length-prefixed (B); structural encoding (C/D/E/F).
**Consequences:** retaining a delimiter without escaping leaves a collision surface reachable by a caller.
**Dependencies:** D3-Q-010, D3-Q-020, D3-Q-021.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-010 — Escaping**
**Q:** What escaping rule applies, and is it itself injective?
**Why:** Escaping is the usual repair for delimiter collision, and is itself a source of ambiguity if under-specified.
**Evidence:** **no escaping exists** — `src/chain.rs:35–47` — CONFIRMED.
**Candidates:** backslash escaping; percent-encoding; JSON string escaping; none (if length-prefixed).
**Consequences:** every escaping scheme needs a defined escape-of-escape rule and a decoder that is the exact inverse.
**Dependencies:** D3-Q-002, D3-Q-009, D3-Q-021.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-011 — Field ordering**
**Q:** Is field order fixed by explicit specification, by struct declaration order, or by sorted key name?
**Why:** Order determines the byte sequence; struct order is an implementation artifact that can change silently under refactoring.
**Evidence:** order fixed by the positional argument list of `compute_chain_hash` (`src/chain.rs:26–34`), which differs from `AuditEntry` declaration order (`src/models.rs:50–97`) — CONFIRMED. The two orders are already not the same.
**Candidates:** explicit normative sequence; lexicographic by field name; declaration order.
**Consequences:** an implicit order is not reproducible from the specification alone; a refactor could change the digest without any intent to.
**Dependencies:** D-2 membership; D3-Q-023.
**Evidence required:** the D-2 field list — `00_…` §8.
**STATUS: OPEN**

**D3-Q-012 — Collection ordering (representation layer)**
**Q:** In what order are collection elements emitted into the byte stream?
**Why:** This is the representation-layer counterpart to D-4's semantic question, and the two must agree.
**Evidence:** no collection is currently in the digest — CONFIRMED.
**Candidates:** as-stored order; sorted by a defined key; sorted by element digest.
**Consequences:** if D-4 declares the collection unordered but D-3 emits as-stored, the digest contradicts the semantics.
**Dependencies:** **D4-Q-001, D4-Q-004 — hard.** See `06_…`.
**Evidence required:** D-4 outcome.
**STATUS: OPEN**

**D3-Q-013 — Nested structures**
**Q:** How is nesting represented — flattened, recursively encoded, or reduced to a sub-digest?
**Why:** `Vec<Violation>` is a collection of structs: two levels of nesting enter the domain for the first time.
**Evidence:** the current digest has no nesting; all nine inputs are scalars — `src/chain.rs:35–47` — CONFIRMED.
**Candidates:** flatten with delimiters; recursive length-prefixing; per-element digest then digest-of-digests; canonical JSON subtree.
**Consequences:** flattening without depth markers allows a nested boundary to be forged from scalar content; sub-digests introduce a second hash domain (D3-Q-022).
**Dependencies:** D3-Q-020, D3-Q-021, D3-Q-022.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-014 — Duplicate values (representation layer)**
**Q:** Are duplicate elements emitted once, repeatedly, or rejected at the representation layer?
**Why:** Deduplication at the representation layer would silently overrule D-4's semantics.
**Evidence:** one rule yields at most one violation (`src/engine.rs:28`, first-match `find`); duplicates arise only from two YAML rules sharing an `id` — CONFIRMED.
**Candidates:** emit all occurrences; emit distinct only; reject.
**Consequences:** representation-layer deduplication makes duplicate insertion undetectable regardless of what D-4 decides.
**Dependencies:** **D4-Q-007 — hard.**
**Evidence required:** D-4 outcome.
**STATUS: OPEN**

**D3-Q-015 — Unicode normalization**
**Q:** Are strings Unicode-normalized before hashing, and if so under which form?
**Why:** Visually identical strings with different code-point sequences otherwise digest differently — or, if normalized, distinct strings collapse.
**Evidence:** a frozen NFKC-based pipeline exists but is scoped to the regex surface; `src/normalizer.rs:11–13` states the original text "is always preserved for the evidence hash" — CONFIRMED. So the codebase currently **deliberately does not normalize** evidence text.
**Candidates:** no normalization (hash as received); NFC; NFKC; reuse SHADOW_SPEC v1.0.
**Consequences:** normalizing evidence text would change what the evidence *is*, not merely how it is hashed — it makes two different recorded values verify as one. Not normalizing leaves homoglyph-distinct rule ids as distinct digests.
**Dependencies:** D3-Q-001, D3-Q-016; interacts with the SHADOW_SPEC freeze.
**Evidence required:** whether SHADOW_SPEC v1.0 is normative for evidence text or only for the regex surface — the module comment says the latter. **Flagged for confirmation.**
**STATUS: OPEN**

**D3-Q-016 — Whitespace**
**Q:** Is whitespace significant, trimmed, or collapsed?
**Why:** Leading/trailing whitespace in a YAML-authored `rule` id or `action` would otherwise be silently significant.
**Evidence:** no trimming anywhere on the persistence path — `src/engine.rs:50–55`, `src/log_writer.rs:96` — CONFIRMED.
**Candidates:** significant (hash as-is); trim; collapse internal runs.
**Consequences:** trimming makes `"deny "` and `"deny"` one value, which is a semantic change, not a formatting one.
**Dependencies:** D3-Q-015, D4-Q-010.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-017 — Numeric special values**
**Q:** How are numeric values outside the ordinary range handled — subnormals, `-0.0`, very large magnitudes?
**Why:** `-0.0` and `0.0` compare equal but have distinct bit patterns and distinct text renderings in some libraries.
**Evidence:** no constraint anywhere on `score` / `confidence` values — `src/policy.rs:41`, `src/models.rs:38` — CONFIRMED. No range validation was found on policy load.
**Candidates:** define a valid range and reject outside it; define representation for every IEEE-754 value; exclude floats entirely.
**Consequences:** without a rule, two implementations may render `-0.0` differently and diverge.
**Dependencies:** D3-Q-006, D3-Q-018.
**Evidence required:** whether policy load constrains `score` to `0.0–1.0` — the doc comment says "0.0–1.0" (`src/models.rs:37`) but **no validation code enforcing it was found**. **NORMATIVE CONFLICT (documentation vs implementation) — flagged, not resolved.**
**STATUS: NORMATIVE CONFLICT**

**D3-Q-018 — `NaN` / ±Infinity**
**Q:** Can these reach the field, and if so what is their representation?
**Why:** JSON cannot represent either; a representation that assumes JSON silently cannot encode them.
**Evidence:** no guard prevents them; YAML can express `.nan` and `.inf` and `serde_yaml` can parse them into `f32` — CONFIRMED as a reachable path. `serde_json` serialization of `NaN` produces `null`, which would then round-trip as a type error or a lost value.
**Candidates:** reject at policy load; define a reserved encoding; exclude floats.
**Consequences:** if unaddressed, a policy containing `.nan` produces a record whose digest may not be reproducible from its own serialized form.
**Dependencies:** D3-Q-006, D3-Q-017.
**Evidence required:** an executed check of `serde_yaml` → `f32` → `serde_json` behaviour for `.nan` / `.inf`. **Not executed here** (would require adding code to the Guard clone). **EVIDENCE GAP.**
**STATUS: EVIDENCE GAP**

**D3-Q-019 — Byte encoding of the final preimage**
**Q:** What exactly is fed to SHA-256 — a UTF-8 string, a byte buffer, or a structured stream?
**Why:** The hash function consumes bytes; the specification must define the byte sequence, not a string abstraction.
**Evidence:** a `String` is built, then `.as_bytes()` is hashed — `src/chain.rs:35–48`, `src/crypto.rs:8–12` — IMPLEMENTATION-DERIVED. Note `sha256_bytes_hex` already exists for arbitrary bytes (`src/crypto.rs:16`).
**Candidates:** string-then-bytes; direct byte-buffer construction; streaming update per component.
**Consequences:** a string intermediate constrains the representation to valid UTF-8 and forbids raw binary components such as IEEE-754 bits.
**Dependencies:** D3-Q-001, D3-Q-006.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-020 — Length-prefix vs delimiter**
**Q:** Is the encoding delimiter-based or length-prefixed?
**Why:** This is the structural fork from which escaping and injectivity follow.
**Evidence:** delimiter-based today, no lengths — `src/chain.rs:35–47` — IMPLEMENTATION-DERIVED.
**Candidates:** delimiter + escaping (A); length-prefix (B); both (belt-and-braces); structural format (C/D/E/F).
**Consequences:** length-prefixing removes escaping and gives injectivity by construction, at the cost of an integer encoding decision (D3-Q-003) and human-unreadable preimages.
**Dependencies:** D3-Q-003, D3-Q-009, D3-Q-010, D3-Q-021.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-021 — Ambiguity / injectivity**
**Q:** Is the representation required to be injective — must distinct records always produce distinct preimages?
**Why:** Without injectivity, two different audit records can share a digest, and tamper detection has a blind spot that no amount of hashing strength fixes.
**Evidence:** the current preimage is **not injective**: caller-controlled `context` is joined unescaped with `"|"` (`src/chain.rs:41`), so a crafted `context` can reproduce the field structure — CONFIRMED as a structural property. No test asserts injectivity.
**Candidates:** injectivity mandated as a normative property with a proof obligation; injectivity for the violations sub-encoding only; no explicit requirement.
**Consequences:** mandating it forces length-prefixing or escaping and creates a testable obligation (T-D4-10/11); not mandating it leaves the collision surface.
**Dependencies:** D3-Q-002, D3-Q-009, D3-Q-010, D3-Q-013, D3-Q-020.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-022 — Hash-domain separation**
**Q:** Does the violations reduction occupy its own hash domain, with a distinguishing prefix or tag?
**Why:** Without domain separation, a digest computed for one purpose can be presented as a digest for another.
**Evidence:** precedent exists but only in the Merkle layer — `0x00` leaf / `0x01` node with an explicit second-preimage rationale (`src/merkle.rs:9–15`) — CONFIRMED. **No convention exists for a third domain** — CONFIRMED.
**Candidates:** reuse the RFC 6962 prefix space with a new tag; a distinct string tag; no separation.
**Consequences:** a sub-digest that is a bare SHA-256 of a byte string can collide by construction with any other bare SHA-256 in the system.
**Dependencies:** D3-Q-013; D-2 shape (sibling vs nested digest).
**Evidence required:** the D-2 shape outcome — `00_…` §8.
**STATUS: OPEN**

**D3-Q-023 — Version marker interaction**
**Q:** Does the canonical representation itself carry a version marker inside the digest input?
**Why:** A representation whose version is not bound cannot prove which rule produced a given digest.
**Evidence:** no version marker of any kind is in the digest input today — `src/chain.rs:35–47` — CONFIRMED. The `schema` string exists in the record but is outside the digest and read by no code (`src/api/audit.rs:132`, `src/log_writer.rs:151–170`).
**Candidates:** version tag as the first digest component; version implied by an external discriminator; no marker.
**Consequences:** binding the version inside makes the digest self-describing but couples D-3 to D-7; not binding it defers the whole question to D-7 with the downgrade surface intact.
**Dependencies:** **D-7 — this is the D-3 ↔ D-7 edge.** See `06_…`.
**Evidence required:** none — but the decision is jointly constrained with D-7.
**STATUS: OPEN**

**D3-Q-024 — Backward compatibility implications of the representation**
**Q:** Does the representation admit re-derivation of digests for records already written?
**Why:** Determines whether D-5's migration strategies remain available after D-3 is fixed.
**Evidence:** the full entry, `violations` included, is persisted (`src/log_writer.rs:96`) — CONFIRMED, so inputs exist. **But** `validator: None` vs an absent key is already erased on disk (`src/models.rs:40`) — CONFIRMED.
**Candidates:** representation that depends only on data recoverable from the JSONL; representation that requires distinctions the JSONL has erased.
**Consequences:** choosing a representation that distinguishes absent from `None` makes faithful re-derivation of historical entries impossible — it would **foreclose D-5-C for those records**.
**Dependencies:** **D-5 — this is the D-3 → D-5 edge, via D-4.** See `06_…`.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-025 — Replay implications**
**Q:** What must a replay verifier reconstruct, and from what inputs?
**Why:** The representation defines the verifier's obligations.
**Evidence:** `recompute_for_entry` reads nine fields from the parsed entry (`src/chain.rs:53–65`) — replay reconstructs from *parsed* data, not from raw bytes — CONFIRMED.
**Candidates:** reconstruct from parsed struct; recompute from the raw line as stored; hybrid.
**Consequences:** reconstructing from parsed data means the JSON parse must be lossless for every digest-relevant distinction — which currently it is not (`skip_serializing_if`).
**Dependencies:** D3-Q-007, D3-Q-024; D-6.
**Evidence required:** none.
**STATUS: OPEN**

**D3-Q-026 — Cross-language equivalence**
**Q:** Is byte-identical reproduction by an independent, non-Rust implementation a requirement?
**Why:** This is the property the whole of D-3 exists to deliver, and it determines how much may be left to library behaviour.
**Evidence:** the codebase already advertises independent verifiability for the Merkle layer — "verifiable with any off-the-shelf CT tooling" (`src/merkle.rs:1–5`) — CONFIRMED as a documented intent for *that* layer. No equivalent statement exists for the entry digest — EVIDENCE GAP.
**Candidates:** required, with published test vectors; required for the Merkle/segment layer only; not required.
**Consequences:** if required, every library-dependent behaviour (float rendering, JSON key order, `to_rfc3339` output) must be replaced by an explicit rule; if not required, the digest is defined by the Rust implementation, which makes the implementation normative — a position that contradicts this package's evidence discipline and would need to be taken deliberately.
**Dependencies:** D3-Q-001, D3-Q-005, D3-Q-006, D3-Q-015.
**Evidence required:** an authoritative statement of whether third-party verification of the entry digest is a product requirement.
**STATUS: EVIDENCE GAP**

---

## 3. Register summary

| Status | Count | IDs |
|---|---|---|
| OPEN | 23 | 001–005, 007–016, 019–025 |
| EVIDENCE GAP | 2 | 018, 026 |
| NORMATIVE CONFLICT | 1 | 017 |
| READY FOR HUMAN DECISION | 0 | — |
| **Total** | **26** | |

**Note on "READY FOR HUMAN DECISION" = 0.** Individual questions are not marked
ready in isolation because D-3 is answered as a coherent representation, not
question-by-question: D3-Q-009/010/020/021 are one structural fork, and
D3-Q-006/017/018 are one float question. Readiness is assessed for D-3 as a whole
in `09_DECISION_BRIEF.md`.
