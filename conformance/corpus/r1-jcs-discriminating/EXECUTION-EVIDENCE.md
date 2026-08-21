# R1-JCS-DISCRIMINATING — Execution Evidence

Scope: conformance only. No production runtime, hashing, Merkle core or protocol
semantics were modified in either repository. R1 does not close DQ-006 or
DQ-002.

---

## 1. Prior-coverage audit (mandate §2)

Before designing R1, the existing JCS conformance surface was inspected.

### 1.1 What actually exists

`aura-poc-a-core-v3.3` **`main` (`64bf959`) has no `conformance/` package at
all** — no `rfc8785`, no JCS adapter, no RFC-6962 leaf. The `JCS-B01…B06`
behaviour suite named in `closures/DQ-002_FINAL_CLOSURE.md` §4 lives at
`conformance/canonical/test_jcs_behavior.py` on the unmerged branch
`claude/cross-language-canonical-001-n4v2c5` (`3e8e0e3`), which is also the only
place the corpus architecture exists. That branch is a strictly additive
descendant of `main` — 14 new files, all under `conformance/`, zero production
changes — so this branch was fast-forwarded onto it rather than reinventing a
second, competing adapter. See §9 (Deviations).

The suite is 13 tests, not 6; `JCS-B01…B06` is a label with no corresponding
identifiers in the code. That drift is already reported as finding 33 of
`aura-specification/ck003/dq-006-closure/DQ-006_SPECIFICATION_CONSISTENCY_SCAN.md`
and is not re-litigated here.

`aura-guard-v1.3` `main` (`35082d7`) has `conformance/canonical/{jcs.rs,
canonical_001.rs}` — **CANONICAL-001 only. There is no RI-RS behaviour suite.**

### 1.2 Coverage matrix

Discrimination measured against
`json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False)`, the
comparator the mandate prescribes.

| Case | Existing RI-PY coverage | Existing RI-RS coverage | Discriminating vs `json.dumps`? | Needed in R1? | Reason |
| --- | --- | --- | --- | --- | --- |
| **A. UTF-16 key ordering** | `test_object_keys_are_sorted_by_utf16_code_unit` — keys `{"b","a","C"}` | none | **NO** | **YES** | The test's keys are all ASCII, where UTF-16 code-unit order, code-point order and byte order coincide. It asserts the *rule's* name while exercising an input that cannot distinguish it. The property only becomes observable across the surrogate boundary. |
| **B. Nested object ordering** | `test_no_insignificant_whitespace`, `test_canonicalisation_is_input_order_independent`; CANONICAL-001 `payload` | CANONICAL-001 `payload` | **NO** | no | `json.dumps(sort_keys=True)` sorts recursively too. Measured: identical bytes. Adding depth to R1 would add size without adding discrimination. |
| **C. String escaping** | `test_string_escaping_is_minimal` — `"`, `\`, `\n`, `U+0001` | none | **NO** | no | `json.dumps` emits the same minimal escapes and the same ``. Measured: identical bytes. |
| **D. UTF-8 / Unicode** | `test_non_ascii_is_emitted_as_raw_utf8` — `é`, `€` | none | **NO** (with `ensure_ascii=False`) | incidental | Discriminating only against the *default* `ensure_ascii=True`. Against the prescribed comparator, identical. R1 carries raw UTF-8 keys, but they are not what makes it discriminate. |
| **E. ECMAScript numbers** | `test_es6_number_serialisation` (`1.0`, `1.5`, `1e21`), `test_integers_are_emitted_without_exponent_or_fraction` | **none** — CANONICAL-001's only number is the integer `42` | **PARTIAL** | **YES** | `1.0 → 1` is discriminating; `1.5` and `1e21 → 1e+21` are not. More importantly these are loose scalar assertions on the engine — **no corpus fixture exercises number formatting**, and RI-RS has no coverage whatsoever. |
| **F. Empty object / array** | none directly | none | **NO** | no | `{}` and `[]` are identical under both. |

### 1.3 Conclusion

The existing surface asserts the RFC 8785 rules but exercises them on inputs
where a conventional serializer satisfies every assertion. **No existing fixture
in either repository is discriminating.** R1 needs case A (which nothing covers
discriminatingly) and case E as a *fixture* rather than a scalar assertion. Cases
B, C, D and F are deliberately not duplicated.

---

## 2. Fixture

`input.json`, SHA-256
`64b737306d2421092cd9f28a5deb525437100c788ab7c39891aaf6b61cd472ca`, stored
byte-identically in both repositories:

```json
{
  "Ｚ": -0.0,
  "a": 1.0,
  "😀": 1e-7
}
```

Fixture ID: `R1-JCS-DISCRIMINATING`. 27 canonical bytes.

The file's key order (`Ｚ`, `a`, `😀`) is non-canonical under *both* candidate
orderings — asserted by `test_fixture_file_key_order_is_not_canonical` — so
ordering stays the engine's job.

**D1 — UTF-16 code-unit key ordering (RFC 8785 §3.2.3).**

| key | code point | UTF-16 code units | first sort unit |
| --- | --- | --- | --- |
| `😀` `U+1F600` | `0x1F600` | `D83D DE00` | `0xD83D` |
| `Ｚ` `U+FF3A` | `0xFF3A` | `FF3A` | `0xFF3A` |
| `a` `U+0061` | `0x0061` | `0061` | `0x0061` |

`0xD83D < 0xFF3A` → JCS emits `😀` before `Ｚ`.
`0xFF3A < 0x1F600` → code-point sorting emits `😀` after `Ｚ`.
The orderings are **inverted**, not merely different.

**D2 — ECMAScript `Number::toString` (RFC 8785 §3.2.2.3).**

| input | RFC 8785 | `json.dumps` | `serde_json::to_vec` |
| --- | --- | --- | --- |
| `1.0` | `1` | `1.0` | `1.0` |
| `-0.0` | `0` | `-0.0` | `-0.0` |
| `1e-7` | `1e-7` | `1e-07` | `1e-7` |

D1 and D2 are independent — repairing one still leaves the other detecting a
substituted engine.

Deliberately excluded after measurement: `1e21` (both emit `1e+21`), nested
ordering, escaping, empty containers. Each would have grown the fixture without
adding discriminating power.

---

## 3. Conventional-serializer comparison (mandate §4, §9)

| Serializer | Bytes | Length |
| --- | --- | --- |
| **RFC 8785 JCS** | `{"a":1,"😀":1e-7,"Ｚ":0}` | 27 |
| Python `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False)` | `{"a":1.0,"Ｚ":-0.0,"😀":1e-07}` | 33 |
| Rust `serde_json::to_vec` | `{"a":1.0,"Ｚ":-0.0,"😀":1e-7}` | 32 |

```text
JCS  hex  7b2261223a312c22f09f9880223a31652d372c22efbcba223a307d
PY   hex  7b2261223a312e302c22efbcba223a2d302e302c22f09f9880223a31652d30377d
RS   hex  7b2261223a312e302c22efbcba223a2d302e302c22f09f9880223a31652d377d
```

Different: **YES**, in key order and in all three number forms. The two
conventional serializers do not even agree with each other; only the two RFC 8785
outputs converge. **Discrimination: PASS.**

This comparison is evidence only. `conformance/canonical/r1_conventional.py`
never produces a digest, a leaf or any protocol value.

---

## 4. RI-PY — actual execution

| Field | Value |
| --- | --- |
| Repository | `Aura-IDToken/aura-poc-a-core-v3.3` |
| Branch | `claude/r1-jcs-discriminating-q981be` |
| Commit at execution | `192c314454756fd4126be2c303c4cd1a950989e1` (clean worktree) |
| Python | CPython 3.11.15, `Linux-6.18.44-fc-v21-x86_64-with-glibc2.39` |
| Engine | `rfc8785` 0.1.4 |
| Adapter | `conformance/canonical/jcs.py`, SHA-256 `8f6c3b440221113721a82c6ff3ff61dcfbaccbcbe972ce7ae635d00444b8b5a4` (byte-identical to CANONICAL-001's) |

Commands:

```text
python -m pytest -q conformance/canonical/test_jcs_behavior.py              -> 13 passed
python -m pytest -q conformance/canonical/test_canonical_001.py             ->  1 passed
python -m pytest -q conformance/canonical/test_cross_language_canonical_001.py -> 13 passed
python -m pytest -q conformance/canonical/test_r1_jcs_discriminating.py     -> 17 passed
python -m pytest -q conformance/canonical/test_cross_language_r1.py         -> 16 passed
python -m conformance.canonical.emit_ri_py_r1_artifact                      -> ri-py.json
python -m conformance.canonical.emit_r1_manifest                            -> manifest.json
```

Observed values:

```text
canonical_bytes_hex = 7b2261223a312c22f09f9880223a31652d372c22efbcba223a307d
canonical_bytes_len = 27
sha256              = a8c01577f4cc4ef73b258cbe66da0103b009fdd88be480c0b811ff2c1ad0946c
leaf_sha256         = fb988d990e39fa4f2f35f9158aaa9bac88aad84add3aaf47fb27426eb450656d
```

Artifact: `ri-py.json`, SHA-256
`5253514952fa053cb65a26f690f060d20442d12239706b13c3f9d9d99e0e4c84`.

The canonical bytes are whatever `rfc8785.dumps` returned. Both digests are
recomputed from those bytes. No RI-RS value and no frozen constant entered the
emitting process — `emit_ri_py_r1_artifact.py` reads neither.

---

## 5. RI-RS — actual execution

| Field | Value |
| --- | --- |
| Repository | `Aura-IDToken/aura-guard-v1.3` |
| Branch | `claude/r1-jcs-discriminating-q981be` |
| Commit at execution | `55015da9d53962049872122f7e6da1c5017f3d75` (clean worktree) |
| Rust | `rustc 1.94.1 (e408947bf 2026-03-25)`, linux/x86_64 |
| Engine | `serde_json_canonicalizer` 0.3.2, read from `Cargo.lock` at test time rather than trusted from a source constant |
| Adapter | `conformance/canonical/jcs.rs`, SHA-256 `cab24c297a4a989e7423e6f0f0c85bbe05ed508dc67fe59a64cdef194a2a9f12` (byte-identical to CANONICAL-001's) |

Commands:

```text
cargo test --locked --test canonical_001              ->  5 passed
cargo test --locked --test r1_jcs_discriminating      -> 11 passed  (also emits ri-rs.json)
cargo test --locked                                   -> 0 failures across the whole suite
cargo fmt --check                                     -> clean
cargo clippy --locked --test r1_jcs_discriminating    -> no warnings
```

Observed values:

```text
canonical_bytes_hex = 7b2261223a312c22f09f9880223a31652d372c22efbcba223a307d
canonical_bytes_len = 27
sha256              = a8c01577f4cc4ef73b258cbe66da0103b009fdd88be480c0b811ff2c1ad0946c
leaf_sha256         = fb988d990e39fa4f2f35f9158aaa9bac88aad84add3aaf47fb27426eb450656d
```

Artifact: `ri-rs.json`, SHA-256
`03662ba0cbee29bd99fc539f37a876cc5c5e3aa54088c9e9dc5c4592bdc16515` — byte-identical
to the file in `aura-guard-v1.3` at `5f4759c`. Nothing in the RI-RS crate reads
an RI-PY value.

---

## 6. Cross-language equality (mandate §8)

Evaluated by `test_cross_language_r1.py`, which reuses the CROSS-LANGUAGE-001
checks verbatim so the two corpora cannot drift on what "equal" means. The
comparator never imports either JCS engine, never re-serializes `input.json`,
and never constructs canonical bytes.

| Check | Result |
| --- | --- |
| CHECK 1 — canonical bytes equality (RI-PY hex == RI-RS hex) | PASS |
| CHECK 2 — RI-PY `sha256` recomputes from RI-PY bytes | PASS |
| CHECK 3 — RI-RS `sha256` recomputes from RI-RS bytes | PASS |
| CHECK 4 — `sha256` equality | PASS |
| CHECK 5 — RI-PY leaf recomputes as `SHA-256(0x00 \|\| bytes)` | PASS |
| CHECK 6 — RI-RS leaf recomputes as `SHA-256(0x00 \|\| bytes)` | PASS |
| CHECK 7 — leaf equality | PASS |

Plus R1-specific guards: distinct implementations, distinct engines, 40-hex
commits, identical `input_sha256` on both sides, `leaf_domain == "0x00"` on both
sides, a recorded discrimination in each artifact, and confirmation that the two
conventional serializers are different tools with different output.

Equality is byte equality throughout — hex strings are decoded and compared as
bytes; no semantic JSON comparison is used anywhere.

---

## 7. Negative controls

### 7.1 Sandboxed controls — `python -m conformance.canonical.negative_controls_r1`

Each control copies the committed corpus to a temporary directory, mutates the
copy, and runs the **real** gate against it via `AURA_R1_CORPUS_DIR`.

```text
baseline (unmutated)                                        16 passed  -> PASS
A  Modified bytes       RI-RS final byte flipped            exit 1, 4 failed  -> detected
B  Modified SHA         RI-PY sha256 first byte corrupted   exit 1, 3 failed  -> detected
C  Wrong leaf domain    both leaves recomputed under 0x01   exit 1, 3 failed  -> detected
D  Wrong engine         RI-PY bytes from json.dumps         exit 1, 5 failed  -> detected
E  Non-discriminating   corpus rebuilt on CANONICAL-001     exit 1, 3 failed  -> detected

committed corpus unmodified: True
R1 NEGATIVE CONTROLS: PASS
```

Control C keeps the two leaves equal to each other, so CHECK 7 still passes —
only the independent recomputations (CHECK 5, CHECK 6) catch it, which is
precisely the property under test.

Control E is R1-specific: the substituted corpus is fully self-consistent and
cross-language equal, and the gate must *still* fail, because a corpus recording
no discrimination is not R1.

### 7.2 Wrong-engine control, in-repository (mandate §10)

The adapters were mutated in place, the suites run, and the mutation reverted via
`git checkout`. Adapter digests were captured before and after to prove exact
restoration.

**RI-PY** — `conformance/canonical/jcs.py`, `rfc8785.dumps` →
`json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False)`:

```text
test_r1_jcs_discriminating.py    9 failed, 8 passed   <- R1 DETECTS the substitution
test_canonical_001.py            1 passed             <- CANONICAL-001 does NOT
```

**RI-RS** — `conformance/canonical/jcs.rs`,
`serde_json_canonicalizer::to_vec` → `serde_json::to_vec`:

```text
cargo test --test r1_jcs_discriminating   4 failed, 7 passed   <- R1 DETECTS
cargo test --test canonical_001           5 passed, 0 failed   <- CANONICAL-001 does NOT
```

This is the R1 result, stated plainly: **in both languages, replacing the RFC 8785
engine with a conventional serializer leaves CANONICAL-001 entirely green while
R1 fails.** The failing R1 tests are the discrimination assertions themselves
(`r1_is_discriminating`, `d1_*`, `d2_*`), not incidental collateral.

Restoration verified:

```text
conformance/canonical/jcs.py  8f6c3b440221113721a82c6ff3ff61dcfbaccbcbe972ce7ae635d00444b8b5a4  (before == after)
conformance/canonical/jcs.rs  cab24c297a4a989e7423e6f0f0c85bbe05ed508dc67fe59a64cdef194a2a9f12  (before == after)
git status --porcelain        empty in both repositories
```

### 7.3 Wrong-leaf-domain control, in-repository (mandate §11)

`SHA-256(0x01 || canonical_bytes)` substituted for `SHA-256(0x00 || …)`:

**RI-PY** — `LEAF_DOMAIN` in `emit_ri_py_r1_artifact.py` set to `b"\x01"`, the
artifact regenerated, and independent verification run:

```text
regenerated leaf_sha256 = 86f8a936aead5f3fcde78f248269b7afdca6671dc6e7da53f0d377ab19ae5adf
                (correct = fb988d990e39fa4f2f35f9158aaa9bac88aad84add3aaf47fb27426eb450656d)

FAILED test_cross_language_r1.py::test_cross_language_check[4]   (CHECK 5 — RI-PY leaf verification)
FAILED test_cross_language_r1.py::test_cross_language_check[6]   (CHECK 7 — leaf equality)
FAILED test_cross_language_r1.py::test_cross_language_gate_overall
FAILED test_r1_jcs_discriminating.py::test_committed_artifact_matches_live_execution
```

**RI-RS** — `LEAF_DOMAIN: u8` set to `0x01`:

```text
FAILED r1_leaf_uses_raw_0x00_prefix
FAILED r1_merkle_leaf_domain_matches_rfc6962   <- production leaf_hash disagrees with the wrong domain
```

Both mutations reverted; both suites re-run green; both worktrees clean.

---

## 8. Production integrity (mandate §12)

**RI-PY** — `git diff` against the branch base is empty for every production
path:

```text
git diff -- core/         (empty)
git diff -- audit/        (empty)
git diff -- compliance/   (empty)
```

Every file R1 adds is under `conformance/`. The three incompatible `json.dumps`
canonicalization sites (`audit/merkle.py:85`, `compliance/certificate.py:69`,
`core/merkle.py:8`) are untouched — R1 characterises that gap, it does not repair
it.

**RI-RS**:

```text
git diff -- src/          (empty)
git diff -- Cargo.lock    (empty)
git diff -- Cargo.toml    +6 lines: one [[test]] target registration
```

The `Cargo.toml` change is the R1 test target and nothing else. Neither
`[dependencies]` nor `[dev-dependencies]` is modified;
`serde_json_canonicalizer = "=0.3.2"` was already present as a dev-dependency
from CANONICAL-001, so the production dependency graph and the resolved lockfile
are bit-identical. This is reported as a deviation in §9 rather than claimed as
"no change to Cargo.toml".

`src/merkle.rs` is read, never written: `r1_merkle_leaf_domain_matches_rfc6962`
observes the shipping `leaf_hash` and reports agreement.

---

## 9. Reproducibility (mandate §13)

Both implementations were executed twice.

| | RI-PY | RI-RS |
| --- | --- | --- |
| `canonical_bytes_hex` | identical | identical |
| `canonical_bytes_len` | identical | identical |
| `sha256` | identical | identical |
| `leaf_sha256` | identical | identical |
| `discrimination` | identical | identical |
| fields that changed | `commit`, `worktree_clean` | `commit` |

**Evidence-infrastructure debt, recorded rather than hidden.** Because each
artifact records the commit it was executed at, committing the artifact advances
`HEAD` past the commit the artifact names, so any later re-execution dirties the
tree by exactly one metadata line. CANONICAL-001 has the same property. The
substantive evidence is unaffected; no evidence was edited to conceal it. A fix
would require decoupling execution provenance from commit identity — out of scope
for R1.

---

## 10. Deviations

1. **Branch name.** The mandate prefers `ck003/r1-jcs-discriminating`. Session
   policy pins this work to `claude/r1-jcs-discriminating-q981be` in both
   repositories. Reported, not silently reconciled.

2. **RI-PY branch base.** `main` (`64bf959`) has no `conformance/` package, no
   `rfc8785` and no JCS adapter, so R1 could not be built on it without creating
   a *second* canonicalization adapter — the exact failure mode already recorded
   as CFL-003 in `aura-specification/ck003/handover-assessment`. This branch was
   therefore fast-forwarded onto `claude/cross-language-canonical-001-n4v2c5`
   (`3e8e0e3`), the branch that carries the established corpus architecture and
   the `JCS-B01…B06` suite, and which is a strictly additive descendant of `main`
   (14 files, all under `conformance/`, zero production changes). R1's own
   commits sit on top. Consequence: this branch carries five inherited
   CANONICAL-001 commits (`41432bf`…`3e8e0e3`) that are not R1 work and remain
   un-merged and un-reviewed. **R1 evidence depends on that unreviewed branch.**

3. **RI-RS `Cargo.toml` modified.** Six lines registering the R1 `[[test]]`
   target. Unavoidable under the repository's established convention of keeping
   conformance tests outside auto-discovered `tests/`. No dependency change; no
   `Cargo.lock` change.

4. **`JCS-B01…B06` is a label without referents.** The suite is 13 unnamed tests.
   Already reported as finding 33 of the DQ-006 specification consistency scan;
   restated in §1.1, not repaired here.

5. **No external oracle for R1.** By construction — see
   `conformance/R1-JCS-DISCRIMINATING.md`. The reference values are a recorded
   two-engine consensus, and the manifest emitter refuses to write without it.

---

## 11. Evidence index

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| Fixture input | `conformance/corpus/r1-jcs-discriminating/input.json` | `64b737306d2421092cd9f28a5deb525437100c788ab7c39891aaf6b61cd472ca` |
| RI-PY execution | `conformance/corpus/r1-jcs-discriminating/ri-py.json` | `5253514952fa053cb65a26f690f060d20442d12239706b13c3f9d9d99e0e4c84` |
| RI-RS execution | `conformance/corpus/r1-jcs-discriminating/ri-rs.json` | `03662ba0cbee29bd99fc539f37a876cc5c5e3aa54088c9e9dc5c4592bdc16515` |
| Manifest | `conformance/corpus/r1-jcs-discriminating/manifest.json` | see file |
| Contract | `conformance/R1-JCS-DISCRIMINATING.md` | — |

| Repository | Branch | Commits |
| --- | --- | --- |
| `Aura-IDToken/aura-poc-a-core-v3.3` | `claude/r1-jcs-discriminating-q981be` | `192c314` (code + corpus), `e00aa29` (clean-worktree re-emission) |
| `Aura-IDToken/aura-guard-v1.3` | `claude/r1-jcs-discriminating-q981be` | `55015da` (code), `5f4759c` (artifact) |

---

## 12. Verdict

**R1: PASS.**

The fixture is genuinely JCS-discriminating; RFC 8785 differs from conventional
JSON serialization on it in two independent dimensions; both reference
implementations executed it for real; their canonical bytes, digests and leaves
are byte-equal and independently verify; both the wrong-engine and wrong-domain
negative controls fail as required; no production code changed in either
repository; and both worktrees are clean.

R1 does **not** close DQ-006 or DQ-002, does not modify APS-001, and does not
authorise wiring JCS into the production runtime. Those remain for the Chief
Architect.
