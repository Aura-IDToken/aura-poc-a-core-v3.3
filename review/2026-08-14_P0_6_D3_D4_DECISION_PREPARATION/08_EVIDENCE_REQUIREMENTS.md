# 08 — Evidence Requirements

What is **not** known, what it blocks, and what would close it. No gap is filled
by assumption anywhere in this package.

Legend: `00_…` §5.

---

## 1. Evidence gaps

| ID | Gap | Blocks | What would close it | Closable by |
|---|---|---|---|---|
| **EG-1** | The exact field membership closed by D-2 was not supplied to this package in explicit form | Scope breadth of D3-Q-011 (field ordering) and D3-Q-022 (domain separation); the D-2 shape input to candidate G | Restatement of the closed D-2 contract | Governance record |
| **EG-2** | Is byte-identical reproduction by an independent, non-Rust implementation a **requirement** for the entry digest? | D3-Q-026, and with it the weight of every cross-language consequence in `05_…` §5 | An authoritative statement. Note the codebase documents this intent for the **Merkle layer only** — "verifiable with any off-the-shelf CT tooling" (`src/merkle.rs:1–5`) — with no equivalent for the entry digest | Human decision |
| **EG-3** | Behaviour of `serde_yaml` → `f32` → `serde_json` for `.nan` / `.inf` | D3-Q-018 | An executed round-trip check. **Not performed here** — it would require adding code to the Guard clone, which is prohibited | Executed experiment, once authorized |
| **EG-4** | Is the `action` value domain intended to be closed (`deny\|review\|allow`) and case-normalized? | D4-Q-010, T-D4-11 | A policy-authoring specification statement | Human decision |
| **EG-5** | Is `score` intended to be constrained to 0.0–1.0? | D3-Q-017 | Resolution of the documentation-vs-implementation conflict (§2) | Human decision |
| **EG-6** | Is YAML declaration order intended to be audit-significant? | D4-Q-001, and through it T-D4-04 and T-D4-12 | A statement of intent | Human decision |
| **EG-7** | Is audit *completeness* (every match, not first match) a requirement? | D4-Q-005, D4-Q-006 | A requirements statement | Human decision |
| **EG-8** | Is SHADOW_SPEC v1.0 normative for **evidence text**, or only for the regex surface? | D3-Q-015 | Reading of SHADOW_SPEC as an authority. The module comment says the latter — "the original (untouched) text is always preserved for the evidence hash" (`src/normalizer.rs:11–13`) — but that is a code comment, not a specification | Specification review |
| **EG-9** | Does an in-repo or external specification define the entry digest at all? | The character of D-3 — defining versus recovering | Search beyond the Guard repo. Within it, `docs/adrs/0001-hash-chain.md` is Accepted but says only "canonical fields incl. `prev_hash`", without enumerating them — CONFIRMED | Archival search |

---

## 2. Normative conflicts — flagged, not resolved

### NC-1 · `score` range
- **Source A (documentation).** "Confidence score reported in the audit entry (0.0–1.0)" — `src/policy.rs:40`; and "Confidence score (0.0–1.0) reported for compliance triage" — `src/models.rs:37`.
- **Source B (implementation).** No validation. The value is copied straight through at `src/policy.rs:283`; no range check, clamp or assertion was found — CONFIRMED.
- **Consequence.** A policy may declare `score: 42.0` or a negative value, and it will be recorded. Any float representation decision (D3-Q-006, D3-Q-017) must therefore cover a wider domain than the documentation implies.
- **Resolution:** NOT ATTEMPTED. Recorded for the Authority.

### NC-2 · `action` equality
- **Source A (engine behaviour).** Matched with `to_ascii_lowercase()` — `src/engine.rs:44`. `"DENY"` and `"deny"` are the same value.
- **Source B (record content).** Stored verbatim — `src/engine.rs:51`. They are two different strings.
- **Consequence.** The engine's notion of equality and the record's notion of identity already differ, before any digest decision. D4-Q-010 and T-D4-11 sit exactly on this seam.
- **Resolution:** NOT ATTEMPTED.

### NC-3 · `request_id` provenance (minor, carried forward)
- **Source A.** "Caller-supplied … when present and valid; omitted otherwise" — `src/models.rs:60–62`.
- **Source B.** "Caller-supplied (or server-generated)" — `src/models.rs:63–64`, immediately following.
- **Source C (implementation).** Extraction only, no server-side fallback — `src/api/audit.rs:52`.
- **Consequence.** Minor for D-3/D-4 unless D-2 admitted `request_id`; recorded because two doc-comments on one field disagree.
- **Resolution:** NOT ATTEMPTED. First recorded in the D-2/D-5 package.

---

## 3. Established facts — not gaps

Recorded so they are not re-investigated.

| Question | Answer | Cite |
|---|---|---|
| Byte encoding today | UTF-8 via `input.as_bytes()` | `src/crypto.rs:8–12` |
| A byte-oriented hash helper already exists | Yes — `sha256_bytes_hex(&[u8])` | `src/crypto.rs:16` |
| Delimiter today | `SEP = "\|"`, no escaping | `src/chain.rs:18–20`, `:35–47` |
| Is the delimiter safe from collision? | **No** — `context` is arbitrary caller text joined unescaped | `src/chain.rs:41` |
| Domain separation precedent | Merkle layer only, `0x00`/`0x01`, RFC 6962; no third-domain convention | `src/merkle.rs:9–15` |
| Digest-of-digest precedent | Yes — leaf → root → segment preimage | `src/segment.rs:140–158`, `:91–106` |
| Duplicate violations reachable? | Only via two YAML rules sharing an `id`; **no id-uniqueness check at policy load** | `src/engine.rs:50–55`; `src/policy.rs:233–237` |
| Is `violations` optional in the model? | No — non-optional `Vec`, always serialized as `[]` | `src/models.rs:90` |
| Is `validator: None` distinguishable on disk? | **No** — omitted entirely | `src/models.rs:40` |
| What does `validator: None` mean? | "No validator configured" — a *failed* validator produces no violation at all | `src/engine.rs:32–42` |
| Are there boolean fields in `AuditEntry`? | No | `src/models.rs:50–97` |
| Field order in the digest vs the struct | **Different** — positional arguments vs declaration order | `src/chain.rs:26–34` vs `src/models.rs:50–97` |

---

## 4. Effect of the gaps on readiness

| Decision | Gaps affecting it | Effect |
|---|---|---|
| **D-3** | EG-1, EG-2, EG-3, EG-5, EG-8, EG-9; NC-1 | **Does not block a decision, but narrows its safety.** All 26 elements are enumerated with observed behaviour and candidates. EG-2 is the most consequential: without knowing whether independent reproduction is required, the cost side of `05_…` §5 has no criterion to weigh against. EG-3 leaves one representation edge case (`NaN`/`inf`) unmeasured |
| **D-4** | EG-4, EG-6, EG-7; NC-2 | **Does not block a decision.** All 15 questions are enumerated and the candidate space is closed. EG-6 (is authoring order audit-significant?) is the single input that most directly determines the choice, and it is a statement of intent, not a fact to discover |

**Consequence.** Both decisions are answerable by the Authority as posed. Neither
is answerable *by evidence alone* — which is the expected shape for decisions of
this class, and is why they are routed to the Two-Key Gate rather than resolved
here.
