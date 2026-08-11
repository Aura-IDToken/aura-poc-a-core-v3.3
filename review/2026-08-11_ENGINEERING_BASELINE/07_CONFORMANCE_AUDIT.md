# 07 — CONFORMANCE AUDIT (TASK 7)

**Subjects:**
- `AuraIDToken/Aura-Conformance-Kit` @ `6f10c5e`
- `AuraIDToken/Aura-Conformance-Kits` @ `834ab46` (**archived**)
- Cross-referenced against `AuraIDToken/aura-specification` (`aps/`, `conformance/`,
  `specification/`)

---

## 1. Headline Finding

**The Conformance Kit contains no conformance tests.**

Total executable test content across both repositories:

```python
# tests/test_bootstrap.py — the entire test suite
def test_bootstrap() -> None:
    """Bootstrap sanity check."""
    assert True
```

One test. It asserts `True`.

The repository is a **scaffolding-stage project** and says so plainly in its own README
(translated from Polish): *"At this stage we are focusing on preparing the project
structure and documentation — code implementation will appear only after we jointly go
through the design phase and configuration review."* That statement is accurate.

---

## 2. Complete Inventory

Both repositories contain 21 files. Full listing of everything that is not a
document:

| File | Lines | Content |
|---|---|---|
| `pyproject.toml` | 28 | packaging; deps `jcs>=0.2.0`, `PyYAML>=6.0`; dev extras `pytest`, `ruff`, `mypy` |
| `reference/__init__.py` | 1 | `# Package marker` |
| `reference/python/__init__.py` | 1 | docstring |
| `reference/python/shared/__init__.py` | 1 | docstring |
| `reference/python/errors.py` | ~170 | **24 exception classes**, all `pass`-bodied, in a 5-branch hierarchy |
| `reference/python/shared/requirements.py` | ~45 | **3 `Enum` classes**: `ComplianceStatus`, `ConformanceLayer`, `VerificationResult` |
| `tests/test_bootstrap.py` | 3 | `assert True` |

**There is no parser, no validator, no canonicalizer, no serializer, no oracle, no
fixture loader, no test runner, no test vector, and no requirement implementation.**

The declared dependency `jcs` (JSON Canonicalization Scheme, RFC 8785) is **never
imported**. `PyYAML` is **never imported**. Both are declared in anticipation.

### 2.1 What the two repositories differ by

`diff -rq --exclude=.git` between `Aura-Conformance-Kit` and `Aura-Conformance-Kits`:

```
Only in Aura-Conformance-Kit: .circleci
Only in Aura-Conformance-Kit/.github/workflows: codeql.yml
```

**All Python source, all tests, all documentation are byte-identical.** The `-Kits`
repository is **archived** on GitHub. They are duplicates with divergent CI plumbing.

Having two near-identical conformance-kit repositories, one archived and one not, with no
document in either stating which is authoritative, is itself a finding — recorded as
NB-002 in `08_BLOCKERS.md`.

---

## 3. Which Requirements Are Verified

**None.**

| Verification target | Present? |
|---|---|
| Any `CONF-001` … `CONF-010` from the specification | **No** — zero references to `CONF-` anywhere in either kit |
| Any `INV-001` … `INV-015` | **No** — zero references |
| Any `REQ-002-xxx` | **No** — zero references |
| Any `APS-xxx` document | **No** references except the phrase "EES" in `docs/EES_IMPLEMENTATION_MAP.md` |
| `SPEC-002` | **No** — see §4 |

Grep for `SPEC-002|CONF-0|INV-0|REQ-002` across both repositories (all file types, all
branches at HEAD): **zero hits**.

The `ConformanceLayer` enum (`reference/python/shared/requirements.py`) names seven
layers — `PARSER`, `CANONICALIZATION`, `SERIALIZATION`, `CRYPTOGRAPHY`, `MERKLE`,
`ORACLE`, `TCK`. None of the seven has any implementation. The enum is a taxonomy, not a
capability.

---

## 4. Does the Kit Test SPEC-002?

# NO.

Established three ways:

1. **Textual:** grep for `SPEC-002` across both repositories → 0 hits.
2. **Structural:** SPEC-002 concerns Constitution Artifact / Constitution Vector identity,
   canonicalization, embedding, numeric representation, hash domains, registration and
   freeze semantics. The kit contains no code touching any of those concepts.
3. **Logically impossible at present:** `SPEC-002` declares its own readiness as
   **NOT READY** (`SPEC-002 §11`), with twelve unresolved decision domains `AD-CA-001` …
   `AD-CA-012` (§6). A conformance test asserting a specific Constitution Vector, canonical
   byte sequence, or hash would necessarily encode one of the unapproved candidate answers
   — which SPEC-002 §6 expressly forbids: *"No candidate choice listed in this table
   constitutes a recommendation, preference, default, or implied architectural decision."*

**The kit's emptiness with respect to SPEC-002 is correct behaviour, not a defect.**
Writing SPEC-002 conformance tests today would violate the specification's own
constraints. This audit therefore records the absence without treating it as a gap to
close.

---

## 5. Placeholders

| Placeholder | Location | Nature |
|---|---|---|
| `assert True` test | `tests/test_bootstrap.py:3` | The entire test suite |
| Empty mapping table | `docs/EES_IMPLEMENTATION_MAP.md` | Table has headers and **two blank rows**; instructions say *"If the specification does not define a field, use UNKNOWN — we do not guess"* |
| `docs/.placeholder_for_branch` | both repos | Literal content: `# Placeholder commit to create branch` |
| `PROJECT_MANIFEST.md` | both repos | Body is `(To be expanded)` |
| `docs/WORKLOG.md` | both repos | One entry: `001 — Bootstrap projektu` |
| Oracle | `docs/TESTING_STRATEGY.md §5` | *"At this stage the Oracle is a conceptual element — we are not implementing it now"* |
| TCK | `docs/TESTING_STRATEGY.md §4` | *"TCK will be a separate artefact (folder /tck or a separate repo in the future)"* — neither exists |
| Test directory structure | `docs/TESTING_STRATEGY.md §7` | Prescribes `tests/unit`, `tests/integration`, `tests/determinism`, `tests/tck`, `tests/resources` — **none of these directories exist** |

The `errors.py` hierarchy and the `requirements.py` enums are **not** placeholders in the
pejorative sense — they are real, typed, importable code with no bodies to write. They are
correctly classified as *scaffolding*.

---

## 6. Can the Kit Be Used Without Unresolved Normative Choices?

**Split answer.**

### 6a. As currently constituted — YES, trivially

The kit as it stands (exception hierarchy + enums + `assert True`) encodes **no** normative
choice. It can be installed, linted, type-checked and run today without touching any
unresolved decision. Its CI does exactly this.

### 6b. For anything it is intended to do — NO

The moment the kit implements any of its seven declared `ConformanceLayer`s, it must fix
one or more currently-unresolved decisions:

| Layer | Blocked by |
|---|---|
| `PARSER` | `AD-CA-004` (normalization rules); numeric-type handling depends on `AD-CA-007` |
| `CANONICALIZATION` | `AD-CA-002`, `AD-CA-008` |
| `SERIALIZATION` | `AD-CA-008` (canonical format, byte sequence, hash domains) |
| `CRYPTOGRAPHY` | `AD-CA-008` (what bytes get hashed), `AD-CA-012` (freeze evidence) |
| `MERKLE` | undefined — no specification selects a Merkle construction; the two existing implementations disagree (`04_DETERMINISM_AUDIT.md` D-8) |
| `ORACLE` | all of the above (an Oracle *is* the normative answer, encoded) |
| `TCK` | all of the above |

**Exception — genuinely unblocked work:** conformance tests for properties that require no
Constitution-derived artefact. For example, the audit-layer behaviours already frozen in
`aura-poc-a-core-v3.3/docs/specs/AUDIT_LAYER_SPEC.md`, or Aura-Guard's chain-digest and
RFC 6962 rules, are defined by their own implementations' specs rather than by SPEC-002.
Whether the Conformance Kit is the right home for those is a scoping question, not an
engineering one.

**Bluntly:** the kit is blocked by design, and it is correctly blocked. `docs/DECISIONS.md`
DEC-001 records a deliberate choice to start from a clean baseline and reintroduce code
only via explicit contracts. That is being honoured.

---

## 7. Kit CI

`Aura-Conformance-Kit` has four workflows; `Aura-Conformance-Kits` has three (no CodeQL).

`ci.yml` — "Aura TCK CI", matrix Python 3.11 / 3.12:

| Step | Command |
|---|---|
| Install | `pip install -e .` + `ruff mypy pytest` |
| Format | `ruff format --check .` |
| Lint | `ruff check .` |
| Types | `mypy --strict reference/python/` |
| Tests | `pytest -q` |

**Observation:** this CI is, in the areas it covers, **stricter than the core
repository's**. `mypy --strict` and `ruff` gate every push here; `aura-poc-a-core-v3.3`
has no linter, no formatter and no type checker in CI at all. What it gates, however, is
216 lines of enums and exception classes.

Additional workflows:
- `python-package.yml` — a stock GitHub template (flake8 + pytest, Python 3.9/3.10/3.11).
  It **duplicates** `ci.yml` with a different, looser toolchain and a different Python
  matrix. `flake8` is not a declared dependency. This is unreviewed boilerplate.
- `generator-generic-ossf-slsa3-publish.yml` — SLSA3 provenance publisher, stock template.
- `.circleci/config.yml` (Kit only) — third CI system.
- `codeql.yml` (Kit only).

**Three CI systems (GitHub Actions ×3 workflows, CircleCI) for one `assert True`.**

---

## 8. Specification-Side Conformance Status (context)

For completeness, what the kit would eventually have to implement, per
`AuraIDToken/aura-specification`:

| ID | Name | Invariant | Status |
|---|---|---|---|
| CONF-001 | Deterministic Evaluation | INV-001 | **DRAFT** |
| CONF-002 | Replay Verification | INV-002 | **DRAFT** |
| CONF-003 | Canonical Serialization | INV-003 | **DRAFT** |
| CONF-004 | Evidence Integrity | INV-004 | **DRAFT** |
| CONF-005 | Traceability | INV-005 | **DRAFT** |
| CONF-006 | Platform Independence | INV-006 | **DRAFT** |
| CONF-007 | Fail Closed | INV-008 | **DRAFT** |
| CONF-008 | Version Compatibility | INV-009 | **DRAFT** |
| CONF-009 | Evidence Completeness | INV-004·005 | **DRAFT** |
| CONF-010 | Cryptographic Verification | INV-011 | **DRAFT** |

**All ten are DRAFT.** `APS-400` itself is `1.0-DRAFT`. `CONF-001 §3` carries an inline
`> **TODO**: Specify exact preconditions once APS-200 schemas and APS-500 fixtures are
finalized.`

So the kit is empty **and** the tests it would implement are not yet finalized. These are
consistent states, not contradictory ones.

### Reference-implementation certification status (from the spec repo's own records)

| Implementation | APS-950 status | Conformance runner | Fixture loader |
|---|---|---|---|
| `RI-PY` (aura-poc-a-core) | **NOT CERTIFIED** | ❌ MISSING (RI-004) | ❌ MISSING (RI-005) |
| `RI-RS` (aura-guard) | **NOT CERTIFIED** | ❌ MISSING (RI-004) | PARTIAL (RI-005) |

Neither reference implementation can currently be run against a conformance kit, because
neither has a runner and the kit has no tests.

---

## 9. Summary Classification

| Aspect | Classification |
|---|---|
| Conformance tests that exist | **NONE** (1 tautological bootstrap test) |
| Requirements verified | **NONE** |
| SPEC-002 tested | **NO** — and correctly so (§4) |
| Placeholders present | **YES** — 8 identified (§5) |
| Usable without unresolved normative choices | **As-is yes; for its purpose no** (§6) |
| Kit CI quality | **Good** — stricter than core's, applied to near-zero content |
| Duplicate-repository hazard | **YES** — two near-identical repos, one archived, no authority statement |
| Is the emptiness an engineering blocker? | **NO** — it is a downstream consequence of a normative blocker |
