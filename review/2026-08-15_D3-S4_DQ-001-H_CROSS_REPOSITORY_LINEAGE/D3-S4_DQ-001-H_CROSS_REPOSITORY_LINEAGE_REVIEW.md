# D3-S4 / DQ-001-H — Cross-Repository Lineage Audit

**Sub-gate of:** DQ-001 (`review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/`)
**Document class:** forensic repository-history and architecture-lineage reconstruction. **Normative effect: NONE.**
**Prepared by:** Claude, forensic lineage agent. **Not** the Architecture Owner.
**Date:** 2026-08-15
**Code changed:** NO. **Normative documents changed:** NO. **DQ-001 decision:** NOT MADE.

---

## 0. Labels and method

Every major conclusion is marked **FACT**, **INFERENCE**, or **UNKNOWN**. Inference is
never presented as history. Negative results are stated as *"not found in inspected
scope"*, never as *"does not exist"*, and always carry their search scope.

**Three concepts are held separate throughout and never merged:**

| Concept | Question it answers |
|---|---|
| **Implementation lineage** | Was one codebase derived from, ported from, or a successor to another? |
| **Protocol lineage** | Do the artifacts share a common protocol contract or object model? |
| **Normative lineage** | Does one artifact hold specification authority over another? |

A repository may sit in one of these chains and not the others. **A designation is not
a derivation, and a derivation is not a normative binding.**

### 0.1 Pinned revisions

| Repository | Revision | History state |
|---|---|---|
| `AuraIDToken/aura-poc-a-core-v3.3` | `98f2f43` (origin/main) | **full** — 276 commits, all branches (see §0.2) |
| `AuraIDToken/aura-guard-v1.3` | `443f72e` | full — 105 commits, all branches |
| `AuraIDToken/aura-specification` | `62d2d6b` | full — 44 commits, all branches |

### 0.2 History-completeness disclosure (hard-stop condition 2 — assessed and cleared)

**FACT.** At the start of this audit the working clone of `aura-poc-a-core-v3.3` was a
**shallow clone** (`git rev-parse --is-shallow-repository` → `true`, 227 commits
reachable). A shallow clone truncates exactly the earliest history this audit depends
on, so no origin claim was made against it. `git fetch --unshallow` was run before any
lineage conclusion; the repository then reported `shallow=false` with **276 commits**
— i.e. **49 commits, including the entire January 2026 origin period, were absent from
the initial clone.**

**FACT.** The `aura-guard-v1.3` and `aura-specification` clones were already full
(`shallow=false`) and were not re-fetched.

**INFERENCE.** Any prior analysis of this repository's early history performed against a
shallow clone would have been unable to see the POC-A origin commits. All §4 and §11
findings in this document postdate the unshallow.

---

## 1. Executive summary

**Primary question.** Is there evidence that POC-A / RI-PY → Aura-Guard / RI-RS →
APS-200 / ENT-007 forms an *intentional architectural lineage*, or are these separate
projects later associated only conceptually?

**Answer: the chain is not a lineage. It is a retrospective classification laid over
three independently-originated projects — but the classification itself is real,
explicit, and authored in a normative source.**

Five findings carry the conclusion:

1. **FACT — three independent origins, months apart, in strict reverse order of the
   claimed lineage.** `aura-poc-a-core-v3.3` began 2026-01-04 (`cae9363`).
   `aura-guard-v1.3` began 2026-05-13 (`36fd12f`) — 129 days later, sharing no commit,
   no file and no ancestor. `aura-specification` began 2026-07-23 (`d2b12cd`) — 71 days
   after that. **The specification arrived last, not first.**

2. **FACT — the RI designation is genuine, explicit, and unilateral.** APS-950 §11
   "Supported Reference Implementations" binds `RI-PY → aura-poc-a-core` and
   `RI-RS → aura-guard` **by repository URL**
   (`aps/APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md:132,133`), and the same table
   exists in the **original uploaded Polish source**
   (`APS-950 — Reference Implementation Requirements_260723_194507.txt:147-152`). This
   is not a bot artifact of the Markdown conversion.

3. **FACT — the designation was never acknowledged by either designee.** The string
   `RI-RS` occurs **0 times** in `aura-guard-v1.3` at HEAD and in **0 commits** across
   its entire history and all branches. `RI-PY` and `RI-RS` occur in
   `aura-poc-a-core-v3.3` **only** inside `review/` — Claude-authored audit packages
   first added 2026-08-11 (`8db25b3`), never in README, `core/`, `audit/`,
   `compliance/`, or any production document.

4. **FACT — no implementation lineage between the two RIs, in either direction.** No
   port, parity, cross-language or derivation evidence exists in either repository.
   `aura-guard-v1.3`'s own roadmap places **"v2.0 — Reference implementation (2027)"**
   in the *future* (`docs/ROADMAP.md:78`) and plans a *new* "conformance harness with
   cross-language verifiers (Python, C reference)" (`:82`) — it does not treat the
   existing Python POC-A as its counterpart.

5. **FACT — a material numbering conflict invalidates the only pre-audit cross-reference
   from POC-A to the APS series.** `docs/GAP-001.md:200-217` (2026-07-24) evaluates
   "APS-200" as **"ARI Engine — integer-only ARI computation"** and "APS-100" as
   **"Canonical Data Model"**. In `aura-specification`, APS-200 **is** the Canonical
   Data Model and APS-100 **is** Protocol Invariants. GAP-001 states its own basis at
   `:202`: requirements were *"inferred from the repository's own documentation … as the
   external `aura-specification` repository is not co-located here."* **Hard-stop
   condition 4 is triggered and reported in §14.**

**INFERENCE.** The evidence describes **retrospective normalization**: two working
systems built independently for different purposes, over which a specification corpus
was authored in a single day and to which reference-implementation identities were
assigned without the implementations participating.

**UNKNOWN.** Whether the authors of APS-950 §11 intended the designation as a
description of existing conformance or as a forward-looking assignment. No commit
message, ADR, RFC or issue in any inspected repository states the intent.

---

## 2. Scope

### 2.1 Repositories inspected

| # | Repository | Reason for inclusion |
|---|---|---|
| 1 | `AuraIDToken/aura-poc-a-core-v3.3` | The repository corresponding to POC-A / RI-PY (see §3.1 — the unversioned name does not exist) |
| 2 | `AuraIDToken/aura-guard-v1.3` | Named in the task scope; contains `AuditEntry` |
| 3 | `AuraIDToken/aura-specification` | Contains APS-200 / ENT-007, per the DQ-001 investigation |

### 2.2 Repositories recorded but NOT treated as lineage members

| Repository | Why recorded | Why excluded |
|---|---|---|
| `aura-nomos/aura-specification` | The repository attached to this working session under that name | **FACT.** Contains only `README.md` (one line: `# aura-specification`) and `.github/CODEOWNERS`, across all branches and its complete 3-commit history. It holds no APS document. It is a **name collision**, not the specification source. Recorded here specifically so the two are never collapsed. |
| `Aura-IDToken/aura-poc-a-core-v3.3` | A GitHub **fork** of repository #1 under a differently-spelled owner org (`Aura-IDToken` vs `AuraIDToken`) | **FACT.** Merge commits in #1's mainline originate from *both* org spellings (e.g. `f54494c` "Merge pull request #48 from Aura-IDToken/…", `ca3e4b9` "…from AuraIDToken/…"). The fork is a workflow artifact of the same project, not a separate lineage member. Recorded to satisfy the repository-identity rule. |
| `AuraProtocol/aura-specification`, `AuraProtocol/aura-poc-a-core`, `AuraProtocol/aura-guard`, `AuraProtocol/aura-fixtures`, `AuraProtocol/aura-examples` | Named as future canonical locations in `aura-specification` README at `6ad45f3` | **FACT.** Every migration checkbox in that README is **unchecked**; the note was edited (`aeb6bab`) and **removed entirely** (`7a22522`) on the same day, 2026-07-23. `AuraProtocol` appears **0 times** in `aura-specification` at HEAD. Not found in the account's accessible repository listing. Treated as an **unrealized proposal** (hard-stop condition 3 — see §14). |

### 2.3 Terminology-only matches deliberately not pursued

**FACT.** Other repositories accessible to this account share the "Aura" token
(`Aura-Conformance-Kit`, `Aura-Framework-v1`, `Aura_Architecture_Book`, `aura-protocol`,
`aura-devos`, `Studio-Aura`). Per the repository-identity rule, **none was inspected**:
no artifact in repositories #1–#3 references any of them in connection with the
POC-A → Guard → APS-200 question. Shared branding is not evidence.

---

## 3. Repository identity (Phase 1)

### 3.1 The unversioned `aura-poc-a-core` does not exist

**FACT.** The task names `AuraIDToken/aura-poc-a-core`. A repository listing filtered on
`poc` returns exactly two repositories: `AuraIDToken/aura-poc-a-core-v3.3` and its fork
`Aura-IDToken/aura-poc-a-core-v3.3`. **No unversioned `aura-poc-a-core` is present in
the accessible listing.**

**FACT.** Nonetheless, both `APS-950:132` and the original Polish source
(`APS-950 …_260723_194507.txt:148`) name the implementation **`aura-poc-a-core`**
without the version suffix; the Markdown table's hyperlink resolves it to
`https://github.com/AuraIDToken/aura-poc-a-core-v3.3`. **INFERENCE:** the specification
refers to the project by unversioned name and pins the versioned repository by URL. The
referent is unambiguous.

### 3.2 Identity table

| Field | POC-A | Aura-Guard | Specification |
|---|---|---|---|
| **Repository** | `aura-poc-a-core-v3.3` | `aura-guard-v1.3` | `aura-specification` |
| **Owner** | `AuraIDToken` | `AuraIDToken` | `AuraIDToken` |
| **URL** | `github.com/AuraIDToken/aura-poc-a-core-v3.3` | `github.com/AuraIDToken/aura-guard-v1.3` | `github.com/AuraIDToken/aura-specification` |
| **Branch inspected** | `origin/main` (+ all branches) | `main` (+ all branches) | `main` (+ all branches) |
| **Revision** | `98f2f43` | `443f72e` | `62d2d6b` |
| **Earliest history** | **`cae9363`, 2026-01-04**, "Initial commit", `Aura-IDToken` | **`36fd12f`, 2026-05-13**, "Initial commit", `Aura-IDToken` | **`d2b12cd`, 2026-07-23**, "Initial commit", `Aura-IDToken` |
| **Commits (all branches)** | 276 | 105 | 44 |
| **Language** | Python (+ TypeScript, circom). **Zero `.rs` files** | Rust | Markdown / PDF / JSON (no implementation code) |
| **Self-claimed role** | "AURA PROTOCOL — IRON CORE v3.3"; "FROZEN / CANONICAL"; "Deterministic Measurement & Audit Instrument for AI Agents" (`README.md:1,13-17`) | "Deterministic audit middleware for AI systems" (`README.md:8`) | "The single canonical source of truth for the Aura Protocol… contains no implementation code" (`README.md:3,13`) |
| **Role designated by APS-950 §11** | **RI-PY** — "Deterministic measurement engine (Layer 0)", Status **Active** (`:132`) | **RI-RS** — "Audit middleware with hash-chained evidence log", Status **Active** (`:133`) | n/a (is the specification) |
| **Designation acknowledged by the repository?** | **NO** — `RI-PY` absent outside `review/` | **NO** — `RI-RS` absent at HEAD and in all history | n/a |
| **Certification status** | not stated in `RI-PY_AURA_POC_A_CORE.md` header | **NOT CERTIFIED** (`RI-RS_AURA_GUARD.md:7`) | n/a |
| **Type (evidence-based)** | **core / measurement engine** (self-claimed); **reference implementation** (designated). Repository *name* encodes "PoC-A" = proof-of-concept | **middleware / runtime** (self-claimed); **reference implementation** (designated) | **specification** |

**FACT — a role tension exists between the self-claim and the designation.** POC-A's
README declares the repository **"FROZEN / CANONICAL"** and the "Iron Core **of the Aura
Protocol**" (`README.md:13-14,23`), while `aura-specification`'s README declares itself
"**The single canonical source of truth for the Aura Protocol**" and states "**If
documentation and implementation disagree, documentation wins**" (`README.md:3,17`).
**INFERENCE:** two documents each claim canonical status over the same protocol. This is
an authority question, not a lineage question, and it is already registered as
OQ-A-CONFLICT-001/002 in
`review/2026-08-12_OQ-A_GOVERNANCE_JURISDICTION/10_CONFLICT_REGISTER.md`. **It is
carried forward here, not re-adjudicated.**

---

## 4. POC-A / RI-PY trace (Phase 2)

**Search scope for this section:** `aura-poc-a-core-v3.3`, all branches, complete
276-commit history post-unshallow, plus `origin/main` working tree.

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | What did POC-A actually implement? | A deterministic integer fixed-point **Agent Reliability Index (ARI)** measurement engine with a Merkle/ETC audit layer and AI-Act compliance rendering. Pipeline: `Agent → Event → PoCA Core → Audit Layer → Compliance Output`, `ARI = 0.3×SI + 0.7×SA − Penalties`, scaling 10^5 | `docs/architecture.md:1-16`; `core/evaluator.py`; `audit/merkle.py` |
| 2 | Did it contain an explicit protocol contract? | **NO protocol contract in the APS sense.** It contains a repository-local constitutional/decree regime and an audit-layer spec, but no wire contract, no object contract, no version handshake | `CONSTITUTIONAL_DECREE.md`; `docs/specs/AUDIT_LAYER_SPEC.md`; `GAP-001:207` records "No protocol bootstrap sequence… no version handshake" |
| 3 | Was its data model intended to be normative? | **PARTIAL / self-declared.** `docs/specs/AUDIT_LAYER_SPEC.md` is described as a "normative frozen spec" for the audit layer, and README declares the repository FROZEN/CANONICAL. But GAP-001 records of its own certificate schema: "**Schema not normative.** No JSON Schema validation" | `README.md:13-14`; `GAP-001:208`; `GAP-001` change log 2026-07-24 |
| 4 | Did it anticipate a Rust implementation? | **NO, in the pre-governance era.** Platform targets are x86_64 / ARM64 / **WASM ("Architectural Goal")** — Rust is not among them. The single Rust mention in production code is a portability aside in a test comment. A `**/*.rs` instruction file was added **2026-08-09**, in the governance era, and applies to **zero files** | `README.md:279-284`; `core/test_ari_observability.py:135`; `.github/instructions/rust-conformance.instructions.md` added `d2ec66f` 2026-08-09 |
| 5 | Did it explicitly reference Aura-Guard? | **Not found in inspected scope before 2026-08-11.** Outside `review/`, `aura-guard` appears only in two Claude-authored 2026-08 documents (`docs/ADR_P0_6_GUARD_VIOLATIONS_INTEGRITY.md`, `docs/evidence/P0-1_EVIDENCE.md`) | `git grep -Il aura-guard origin/main -- ':!review/'`; first-introducing commit `8db25b3` 2026-08-11 |
| 6 | Did it explicitly reference APS-200? | **YES — once, on 2026-07-24, and with incompatible semantics.** `docs/GAP-001.md` is the sole non-`review/` file mentioning APS-200. See §8.3 — it defines APS-200 as "ARI Engine" | `ef91cb1` 2026-07-24; `GAP-001:209` |
| 7 | Did it explicitly reference ENT-007? | **NO.** First and only appearance is `17c3916`, 2026-08-12, a Claude evidence commit inside `review/` | `git log --all -S"ENT-007" --reverse` |
| 8 | Does it contain migration / roadmap language? | **YES, but internal only.** GAP-001 defines a CORE-001…CORE-011 remediation programme against its *own* inferred APS numbering. No item targets Aura-Guard, RI-RS, or ENT-007 | `GAP-001:405-420` |

**FACT — "adapter" in POC-A does not refer to an object-model adapter.** All three
non-`review/` occurrences are numeric/embedding adapters: `GAP-001:364` (pgvector float
similarity → int32 ARI space), `:417` and `:662` ("CORE-011 — Embedding → int32
Adapter"). **None** relates to ENT-007, the Common Object Contract, or a protocol object
mapping.

**FACT — POC-A's audit object is `EventTrustCertificate`, not `AuditEntry`.** Defined at
`audit/merkle.py:20`, introduced `80ec4ad` **2026-01-17**. (Note: the prior baseline
package cites this class at `audit/merkle.py:37`; the class statement is at `:20` in the
current tree. Recorded as a citation drift, immaterial to the conclusion.)

---

## 5. RI-PY → RI-RS trace (Phase 3)

**Search scope:** both repositories, all branches, complete histories; READMEs,
`docs/`, ADRs, commit messages, source, tests, fixtures.

### 5.1 Search results

| Term searched | `aura-guard-v1.3` @HEAD | `aura-guard-v1.3` history (`-S`, all branches) | Interpretation |
|---|---|---|---|
| `RI-RS` | **0 files** | **0 commits** | The designee never uses its own designation |
| `RI-PY` | **0 files** | **0 commits** | No awareness of the sibling RI |
| `POC-A` | **0 files** | **0 commits** | — |
| `poc-a` / `aura-poc` | 0 files | **1 commit** — `6661982` (see §5.3) | Audit artifact only |
| `aura-specification` | 0 files | **1 commit** — `6661982` (see §5.3) | Audit artifact only |
| `APS-` | **0 files** | **0 commits** | No APS awareness in mainline, ever |
| `ENT-007` | **0 files** | **0 commits** | — |
| `parity` | **0 files** | **0 commits** | No parity claim |
| `port of` | **0 files** | **0 commits** | No port claim |
| `cross-language` | 2 files | 4 commits | **Future roadmap only** — see §5.2 |
| `reference implementation` | 2 files | 4 commits | **Future roadmap + an unrelated FIPS reference** — see §5.2 |

### 5.2 The two apparent hits are both forward-looking, and both point away from RI-PY

**FACT.** `docs/ROADMAP.md:78` — the section heading is **"## v2.0 — Reference
implementation (2027)"**. `:82` — "Conformance harness with **cross-language verifiers
(Python, C reference)**". `:80` — "**EVIDENCE_SPEC v1.1** — 162-byte binary evidence
envelope, bit-for-bit reproducible across implementations".

**FACT.** `README.md:366` mirrors this: "| v2.0 | Binary evidence envelope,
cross-language verifiers, formal verification | **planned** |".

**FACT.** The other `reference implementation` hit, `src/tst_verify.rs:685`, refers to
"the FIPS 180-4 reference implementation built on top of `sha2`" — an external
cryptographic standard, unrelated.

**INFERENCE — this is the strongest single piece of counter-evidence to H1.** As of
v1.3, Aura-Guard (a) does not consider itself a reference implementation, placing that
status in a 2027 milestone; (b) plans its **own** evidence specification
(`EVIDENCE_SPEC v1.1`), not APS-300 or APS-200; and (c) plans to *author* a Python
verifier as future conformance tooling rather than recognising the existing Python
POC-A as its counterpart. **A project that is a port of RI-PY does not schedule
"reference implementation" and "Python verifier" as future work.**

### 5.3 The single cross-repository mention, and why it is not architecture

**FACT.** `6661982` (2026-08-15, author **Claude**, "docs(d3): reconnaissance + blocker
report for real Rust chain execution") is the **only commit in the entire history of
`aura-guard-v1.3`** to mention `aura-specification`, `aura-poc-a-core-v3.3` or `poc-a`.
The mention is at `D3_REAL_CHAIN_EXECUTION_BLOCKER.md:55`, in a sentence enumerating
where a missing fixture was *searched for* and not found.

**FACT.** That commit is **not an ancestor of HEAD** (`git merge-base --is-ancestor` →
false). It lives on the unmerged branch `origin/d3/real-chain-fixture-export`.

**INFERENCE.** This is an audit trace produced by the present agent lineage in
August 2026, not a project artifact, and it is not in mainline. It carries no
architectural weight.

### 5.4 Disjointness at the technical level

**FACT**, from `review/2026-08-11_ENGINEERING_BASELINE/03_LANGUAGE_BOUNDARY.md:44-54`,
which reached the determination "**NO CURRENT PYTHON/RUST RUNTIME INTERFACE**":

| Surface | POC-A (RI-PY) | Aura-Guard (RI-RS) | Shared? |
|---|---|---|---|
| Audit / evidence record | `EventTrustCertificate` (`audit/merkle.py`) | `AuditEntry` (`src/models.rs:50`) | **No** — disjoint field sets, disjoint semantics (`:49`) |
| Merkle construction | pairwise, odd node **duplicated** | **RFC 6962** | **No** — different roots for identical leaves (`:50`) |
| Canonical bytes | JSON `sort_keys=True`, `separators=(",",":")` | `\|`-joined field concatenation | **No** (`:51`) |
| Signature | **HMAC-SHA256, symmetric** | **Ed25519, asymmetric**, over policy YAML | **No** (`:52`) |
| Numeric model | int32 fixed-point, scale 10^5 | `f32` confidence (`src/models.rs:38`) | **No** (`:53`) |
| Test fixtures | none shared | `tests/fixtures/tsa/*` | **No** (`:54`) |

**FACT.** No FFI, IPC, HTTP call, shared file format, shared schema, shared test vector
or shared constant was found between them; `Cargo.toml` contains no Python-interop
crate, no `cdylib`, no `build.rs` (`03_LANGUAGE_BOUNDARY.md:21-38`).

### 5.5 Phase 3 determination

**Is RI-RS a port of RI-PY?**

| Option | Verdict |
|---|---|
| A) a port of RI-PY | **REJECTED** — no port/parity/cross-language derivation evidence in either repository's full history; disjoint algorithms for every shared concern (§5.4) |
| B) an independent reimplementation | **PARTIALLY APPLICABLE** — independent, yes; but not a *re*implementation, because it does not implement the same function |
| C) a successor | **REJECTED** — POC-A remained active after Aura-Guard began (commits through 2026-08-14); no deprecation, handover or succession statement found in either repository |
| D) a partial implementation | **REJECTED** — of POC-A, no. (It *is* a partial implementation of APS-950's component list, per `RI-RS_AURA_GUARD.md:22-30` — a different relation, to the spec, not to RI-PY) |
| **E) an unrelated implementation** | **BEST SUPPORTED**, with one qualification: unrelated in *implementation* and *protocol* lineage, while **co-designated** as a sibling reference implementation in *normative* lineage by APS-950 §11 |
| F) unresolved | **NOT APPLICABLE** — the negative evidence is exhaustive across both full histories, so the question is answered, not open |

**FACT.** The two systems solve different problems: POC-A computes a deterministic
reliability index over agent events; Aura-Guard evaluates prompt/response pairs against
signed YAML policy at an HTTP boundary and hash-chains the outcome.

---

## 6. RI-RS → Aura-Guard trace (Phase 4)

**FACT — RI-RS is not a component that lives anywhere.** It is an **identifier assigned
to the whole repository**. `APS-950:133` reads:

> `| RI-RS | [aura-guard](https://github.com/AuraIDToken/aura-guard-v1.3) | Rust | Audit middleware with hash-chained evidence log | Active |`

and `reference/RI-RS_AURA_GUARD.md:1-7` gives it Document ID `RI-RS`, Version `v1.3.0`,
Repository `https://github.com/AuraIDToken/aura-guard-v1.3`, APS-950 Certification
Status **NOT CERTIFIED**.

Accordingly:

| Question | Answer | Evidence |
|---|---|---|
| Does RI-RS exist as a named architectural component? | **NO** — it exists as a *designation of a repository*, not as a module, crate, directory or artifact inside one | `APS-950:133`; `RI-RS_AURA_GUARD.md:1-7` |
| Where does it live? | In the specification repository, as a label pointing outward by URL | as above |
| Does Aura-Guard contain it? | **NO** — 0 occurrences of `RI-RS` at HEAD and in all history | §5.1 |
| Is Aura-Guard its successor? | **N/A** — they are the same object under two names | — |
| Does Aura-Guard embed it? | **N/A** — same | — |
| Do they merely share concepts? | **NO** — the relation is identity-by-designation, which is stronger than shared concepts and weaker than derivation | — |
| Did any migration occur? | **Not found in inspected scope.** No migration ADR, no transfer commit, no rename. The one migration *proposal* on record (`AuraProtocol` org) was removed the day it was written | §2.2 |

### 6.1 First-appearance table

| Item | First commit | Date | Repository | Evidence |
|---|---|---|---|---|
| Aura-Guard repository | `36fd12f` "Initial commit" (`README.md`, 2 lines) | 2026-05-13 | guard | `git log --reverse` |
| First substantive source | `d03eb65` "Aura-Guard v1.3.1: Bootstrap fail-closed gate + lineage verification" — monolithic import incl. `src/models.rs`, `Cargo.toml`, `docs/ARCHITECTURE.md` | 2026-05-13 | guard | `git show --stat d03eb65` |
| `AuditEntry` | `d03eb65` (same commit) | 2026-05-13 | guard | `src/models.rs` |
| RI-RS terminology | **never** | — | guard | 0 hits, all history |
| `RI-RS_AURA_GUARD.md` | `b68181e` | 2026-07-23 | **spec** | `git log --diff-filter=A` |
| ADR-0001 (hash chain) | present at HEAD, "Accepted in v1.3, still current" | — | guard | `docs/adrs/0001-hash-chain.md:3` |

### 6.2 A false lineage signal, defused

**FACT.** Commit `d03eb65`'s subject contains the phrase "**lineage verification**", and
`aura-replay` exposes a `--verify-lineage` flag. This does **not** refer to repository or
architectural lineage. `README.md:304` — "`--verify-lineage` reloads each policy YAML
referenced by the log and…"; `SECURITY.md:66` — "checks that each logged `policy_hash`…";
`docs/ROADMAP.md:67-68` — "Today's `--verify-lineage` only proves **policy-hash
continuity**, not model output; **the rename was made specifically to stop overpromising
on that front**."

**INFERENCE.** "Lineage" in Aura-Guard is a *policy-provenance* term. Any lineage
conclusion drawn from that word would be a false positive. Recorded because the phrase
appears in the repository's founding commit message and is the kind of signal this audit
is expected to test rather than accept.

---

## 7. AuditEntry history (Phase 5)

### 7.1 Determinations

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | First introduction | Commit **`d03eb65`**, 2026-05-13, author `aura.idtokenkontakt` | `git log --all -S"AuditEntry" --reverse` |
| 2 | First repository | **`aura-guard-v1.3`** — and no other | see 7/8 below |
| 3 | Original field set | **11 fields**: `schema`, `seq`, `audit_id`, `timestamp`, `decision`, `policy_set`, `policy_hash`, `context`, `input_hash`, `shadow_hash`, `violations`, plus `prev_hash`/`chain_hash` | `git show d03eb65:src/models.rs` |
| 4 | Original semantic purpose | Module doc: "Request / response **data transfer objects (DTOs)** shared by the HTTP API and the audit log file format"; struct doc: "Outbound `/v1/audit` response body **and** the canonical audit log entry" | `src/models.rs:1-2,44-48` |
| 5 | Subsequent field changes | **`request_id` added** `75f1052`, 2026-07-26 ("Log analysis for observability metrics (#23)"). Test-constructor fixups `9dd8757`, 2026-07-27. Net-zero revert pair `56f7b64`→`c5e162e`, 2026-07-27/28. **Current: 14 fields** | `git log --all -- src/models.rs` |
| 6 | Did its semantics change? | **NO.** It remained a DTO throughout. The D-3 reconnaissance commit states independently: "**`models.rs` is a pure DTO module**" | `6661982` commit body |
| 7 | Ever explicitly connected to RI-PY? | **NO — not found in inspected scope.** `AuditEntry` appears in `aura-poc-a-core-v3.3` in only 10 commits, all Claude-authored, earliest `f8ff209` 2026-08-11, all confined to `review/` and `docs/ADR_P0_6_*` | `git log --all -S"AuditEntry"` in POC-A |
| 8 | Ever explicitly connected to RI-RS? | **YES, transitively and only by designation** — `AuditEntry` lives in `aura-guard-v1.3`, which APS-950 §11 designates RI-RS. No source file, commit or doc in the guard uses the term `RI-RS` | §5.1, §6 |
| 9 | Ever explicitly connected to APS-200? | **NO.** `git log --all -S"APS-"` over `aura-guard-v1.3` returns **0 commits** | §5.1 |
| 10 | Ever described as ENT-007? | **NO.** `ENT-007` returns 0 files and 0 commits in `aura-guard-v1.3`. The only association anywhere is the DQ-001 analysis of 2026-08-15 | §5.1; `review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/` |
| 11 | Adapter ever planned or implemented? | **NO — not found in inspected scope.** In `aura-guard-v1.3` the word "adapter" occurs only as *SIEM format adapters* (`docs/ROADMAP.md:62`) and *WORM media adapters* (`:83`, `docs/deployment.md:134`). In `aura-specification` it occurs **0 times**, repo-wide. In POC-A it refers to embedding→int32 conversion only (§4) | §12 |

### 7.2 Chronology

| Date | Commit | Repository | Change | Evidence | Architectural significance |
|---|---|---|---|---|---|
| 2026-01-04 | `cae9363` | POC-A | Repository created | `git log --reverse` | **FACT.** Lineage origin candidate #1 — 129 days before Aura-Guard |
| 2026-01-04 | `befddfa` | POC-A | `merkle.py` created | `git log --diff-filter=A` | POC-A's evidence layer begins |
| 2026-01-17 | `80ec4ad` | POC-A | `EventTrustCertificate` introduced | `git log -S` | **FACT.** POC-A's audit object — a *different* object from `AuditEntry`, never reconciled with it |
| 2026-05-13 | `36fd12f` | Guard | Repository created (README, 2 lines) | `git log --reverse` | **FACT.** Independent origin; no shared ancestor with POC-A |
| **2026-05-13** | **`d03eb65`** | **Guard** | **`AuditEntry` introduced, 11 fields** | `src/models.rs` | **FACT.** Authored **71 days before ENT-007 existed.** **INFERENCE:** it cannot have been written as an implementation of ENT-007. **UNKNOWN:** whether the author anticipated any future protocol object |
| 2026-07-23 | `d2b12cd` | Spec | Repository created | `git log --reverse` | **FACT.** The specification arrives **last** |
| 2026-07-23 | `6f4d971`, `792c43f` | Spec | Original APS-000…950 + Constitution uploaded as **Polish** PDF/TXT | file listing | **FACT.** Normative source authored externally, same day |
| 2026-07-23 | `6ad45f3` | Spec | README naming a planned `AuraProtocol` org migration; **all 6 status boxes unchecked** | `git show 6ad45f3:README.md` | **FACT.** Proposal only |
| 2026-07-23 | `aeb6bab`, `7a22522` | Spec | Migration note edited, then **removed**, same day | `git log -S"AuraProtocol"` | **FACT.** Proposal withdrawn within hours |
| **2026-07-23** | **`b68181e`** | **Spec** | **Entire canonical corpus built in ONE commit** — APS-000…950 incl. **APS-200/ENT-007**, invariants, CONF-001…010, fixtures, ADRs, **and both `RI-PY_AURA_POC_A_CORE.md` and `RI-RS_AURA_GUARD.md`** | `git show --stat b68181e` | **FACT.** ENT-007 and both RI designations are born simultaneously, by `copilot-swe-agent[bot]`, with no participation from either implementation repository |
| 2026-07-24 | `ef91cb1` | POC-A | GAP-001 added — POC-A's **first ever** APS-200 / APS-100 reference | `git log -S"APS-200" --reverse` | **FACT.** One day after the spec repo existed. **CONFLICT** — uses incompatible APS numbering (§8.3) |
| 2026-07-26 | `75f1052` | Guard | `request_id` added to `AuditEntry` | `git log -S"request_id"` | **FACT.** The only post-spec schema extension. **INFERENCE:** the Common Object Contract was not adopted at the one moment the schema was reopened |
| 2026-08-09 | `d2ec66f` | POC-A | `rust-conformance.instructions.md` added (`applyTo: **/*.rs`) | `git log --diff-filter=A` | **FACT.** Governs zero files; names no repository. Not a lineage link |
| 2026-08-11 | `8db25b3` | POC-A | **First ever** appearance of `RI-PY`, `RI-RS`, `aura-guard` in POC-A — inside a Claude review package | `git log -S --reverse` | **FACT.** Cross-repo terminology enters POC-A only in the audit era |
| 2026-08-12 | `17c3916` | POC-A | **First ever** appearance of `ENT-007` in POC-A — Claude evidence commit | `git log -S"ENT-007" --reverse` | **FACT.** |
| 2026-08-15 | `6661982` | Guard | Guard's **only ever** mention of sibling repositories — on the **unmerged** branch `d3/real-chain-fixture-export` | `git merge-base --is-ancestor` → false | **FACT.** Audit artifact, not mainline architecture |
| 2026-08-15 | `e3e4732` | POC-A | DQ-001 adapter-architecture review — **first proposal of an adapter anywhere in the ecosystem** | this review series | **FACT.** No adapter was proposed before this date |

---

## 8. APS-200 / ENT-007 arrival (Phase 6)

### 8.1 Arrival facts

| Question | Answer | Evidence |
|---|---|---|
| First appearance of ENT-007 | **2026-07-23**, commit `b68181e`, in `aps/APS-200_CANONICAL_DATA_MODEL.md:149-159` | `git log --diff-filter=A` |
| First repository | `AuraIDToken/aura-specification` | — |
| Present in the original source? | **YES** — `APS-200 — Canonical Data Model_260723_192852.txt:59-60` contains `ENT-007` / `Audit Record`. **INFERENCE:** ENT-007 is authored content, not an artifact of Markdown conversion | original TXT |
| First reference **from** an implementation **to** APS | `ef91cb1`, 2026-07-24, POC-A `docs/GAP-001.md` — **but see §8.3** | — |
| First reference **from** APS **to** an implementation | `b68181e`, 2026-07-23 — `APS-950:132,133` and both `reference/RI-*.md` files | — |
| First explicit mapping `AuditEntry` ↔ ENT-007 | **Not found in inspected scope.** No mapping exists in any repository | §12 |
| First explicit conformance statement | `b68181e`, 2026-07-23 — and it is **negative**: `RI-RS_AURA_GUARD.md:7` "APS-950 Certification Status: **NOT CERTIFIED**"; `:74` "No canonical APS-200 data model objects"; `RI-PY_AURA_POC_A_CORE.md:27` "RI-006 Audit Interface \| PARTIAL \| audit/ module with Merkle; **not APS-200 ENT-007**" | — |

### 8.2 Character of APS-200

**FACT.** APS-200 and ENT-007 entered the ecosystem 71 days after `AuditEntry` and 200
days after POC-A began, in a single commit that simultaneously created the entire APS
corpus and both RI status documents.

**FACT.** Those RI status documents assess the two implementations against APS-200 and
report them as **non-conformant on arrival** — the specification's first act toward the
implementations was to record a gap, not to record a fulfilled contract.

**FACT.** The corpus was authored externally in Polish and converted to English Markdown
the same day; APS-950 §11's RI table is present in the Polish original
(`…_260723_194507.txt:147-152`), so the designation is source-authored.

**Determination — APS-200 is best characterized as RETROSPECTIVE NORMALIZATION, with a
prospective component.**

- *Retrospective* (**FACT-supported**): it describes and classifies two systems that
  already existed and were built without it; it assigns them identities they never
  requested; it immediately records them as non-conformant.
- *Prospective* (**FACT-supported**): its content is forward-binding — `APS-200:16`
  states what conformant implementations MUST do; `APS-950:23` requires an RI to
  "Implement all mandatory APS requirements"; and it carries unresolved TODOs
  (`APS-200:218`, `:224`) indicating unfinished contract work.
- **NOT** an external standard: authored inside the same GitHub account, by the same
  actors, with no external SDO involvement found.
- **NOT** internal architectural evolution of either implementation: neither repository
  contributed to it, referenced it beforehand, or acknowledged it afterward.

**UNKNOWN.** Whether the RI designation was intended as a description of achieved status
or as an aspirational assignment. No commit message, ADR, RFC or issue states this.
Per the instruction not to decide this from dates alone, the date evidence is treated as
*consistent with* retrospective normalization, and the *decisive* evidence is the
substantive content: a specification whose first assessment of both designees is
"NOT CERTIFIED / no APS-200 objects" is normalizing something that already existed.

### 8.3 CONFLICT-DQ001H-01 — incompatible APS numbering (hard-stop condition 4)

**FACT.** `docs/GAP-001.md:204-217` (POC-A, 2026-07-24) and `aura-specification`
@ `62d2d6b` assign different subject matter to the same identifiers:

| ID | GAP-001 (`:207-217`) | `aura-specification` | Compatible? |
|---|---|---|---|
| APS-000 | Protocol Bootstrap | Foundation & Terminology | **NO** |
| APS-001 | Core Invariants | Protocol Specification | **NO** |
| **APS-100** | **Canonical Data Model** | **Protocol Invariants** | **NO** |
| **APS-200** | **ARI Engine** — integer-only ARI, 10^5 fixed-point | **Canonical Data Model** | **NO** |
| APS-300 | Evidence Engine | Evidence Model | partial |
| APS-400 | Serialization | Conformance Test Matrix | **NO** |
| APS-500 | ZK Layer | Reference Fixtures | **NO** |
| APS-900 | Conformance Runner | Compliance Mapping | **NO** |
| APS-950 | Compliance Reporter | Reference Implementation Requirements | **NO** |

**FACT.** GAP-001 declares its own basis at `:202`: *"Requirements are **inferred** from
the repository's own documentation, the custom directive, and ADR-005, as the external
`aura-specification` repository is **not co-located here**."* Its header nonetheless
cites "**Specification Reference:** aura-specification / spec-v0.1.0" (`:5`).

**FACT.** `GAP-001:417` therefore reads "APS-200: Integer ARI Engine → … CORE-011:
Embedding → int32 Adapter" — an APS-200 "adapter" item that has **no relation whatsoever**
to the ENT-007 object-mapping question of DQ-001.

**INFERENCE.** The single pre-audit cross-reference from POC-A to APS-200 does not refer
to the APS-200 that exists. **Any lineage or conformance claim resting on GAP-001's APS
citations is invalid.** This is reported, not reconciled (§14).

**UNKNOWN.** Whether GAP-001's numbering reflects an earlier, superseded APS scheme that
once existed, or was constructed ad hoc. **Not found in inspected scope:** no document in
any of the three repositories defines APS-200 as "ARI Engine" other than GAP-001 itself.

---

## 9. Roadmap / architecture history (Phase 7)

| Document | Section | Exact statement | Intended dependency | Status |
|---|---|---|---|---|
| `aura-specification/README.md` @ `6ad45f3` | Overview / Status | "This repository is being migrated to the **AuraProtocol** organization. Future canonical location: `github.com/AuraProtocol/aura-specification`" + a 6-item checklist naming `AuraProtocol/aura-poc-a-core`, `AuraProtocol/aura-guard`, `AuraProtocol/aura-fixtures`, `AuraProtocol/aura-examples` | All three systems co-located under one org | **FUTURE PROPOSAL — WITHDRAWN.** All boxes unchecked; note removed same day (`7a22522`); `AuraProtocol` absent at HEAD; org not in accessible listing |
| `aura-specification/aps/APS-950…:131-133` | §11 Supported Reference Implementations | `RI-PY → aura-poc-a-core → Python → Deterministic measurement engine (Layer 0) → Active`; `RI-RS → aura-guard → Rust → Audit middleware with hash-chained evidence log → Active`; `RI-TEST → Reference Fixtures Runner → TBD → Cross-implementation fixture validation → **Planned**` | Both repos are RIs under APS | **CURRENT ARCHITECTURE (declared).** Unilateral; unacknowledged by either designee. RI-TEST **never created** — not found in inspected scope |
| `aura-specification/aps/APS-200…:218` | §8 | "**TODO**: Define the canonical serialization format **for interoperability between RI-PY and RI-RS**" | Cross-RI interoperability | **FUTURE PROPOSAL.** The only place the two RIs are related *to each other* by the spec — and it is an open TODO |
| `aura-guard-v1.3/docs/ROADMAP.md:78-84` | v2.0 (2027) | "**Reference implementation**"; "**EVIDENCE_SPEC v1.1** — 162-byte binary evidence envelope"; "Conformance harness with **cross-language verifiers (Python, C reference)**" | Guard's own future spec + its own future Python verifier | **FUTURE PROPOSAL.** Names no APS document and no existing repository |
| `aura-guard-v1.3/docs/ROADMAP.md:62,83` | v1.6 / v2.0 | "SIEM connectors — … format **adapters**"; "**WORM media adapters**" | Storage/SIEM integration | **FUTURE PROPOSAL.** Unrelated to object mapping |
| `aura-poc-a-core-v3.3/docs/GAP-001.md:405-420` | §Dependency graph | CORE-001…CORE-011 remediation programme | Internal remediation against GAP-001's own APS numbering | **HISTORICAL INTENT.** Invalidated as an APS reference by §8.3 |
| `aura-poc-a-core-v3.3/README.md:279-284` | §6 | Platform table: x86_64 ✅, ARM64 ✅, **WASM 🔶 Architectural Goal** | Cross-platform determinism | **CURRENT + FUTURE.** **Rust is not a target.** No Aura-Guard dependency |

**FACT.** No migration ADR, succession document, handover record or deprecation notice
relating POC-A to Aura-Guard was found in any of the three repositories, on any branch,
in any commit.

---

## 10. Cross-repository evidence matrix (Phase 8)

| Relationship | Evidence | Source | Classification | Confidence |
|---|---|---|---|---|
| **POC-A → RI-PY** | RI table binds `RI-PY` to `aura-poc-a-core` by name and URL; present in the original Polish source; dedicated status document exists. **Counter:** `RI-PY` absent from POC-A outside `review/`; POC-A self-claims "IRON CORE / FROZEN / CANONICAL" instead | `APS-950:132`; `…_260723_194507.txt:147-149`; `reference/RI-PY_AURA_POC_A_CORE.md`; POC-A `README.md:13-14` | **CONFIRMED** *as designation only* — **not** an implementation or protocol lineage; unilateral and unacknowledged | **HIGH** (for the designation) |
| **POC-A → Aura-Guard** | No shared commit, file, ancestor, FFI, IPC, schema, fixture or constant. Disjoint Merkle, canonical bytes, signature scheme and numeric model. Guard created 129 days later with zero POC-A references in 105 commits | `03_LANGUAGE_BOUNDARY.md:21-54`; `git log --all -S` in guard → 0 | **NOT APPLICABLE** — positive evidence of separateness | **HIGH** |
| **RI-PY → RI-RS** | No port/parity/derivation evidence in either full history. Guard schedules "Reference implementation" and a Python verifier as **2027 future work**. Only spec-side relation is an open TODO | guard `docs/ROADMAP.md:78-82`; `APS-200:218`; §5 | **NOT APPLICABLE** as derivation; sibling **co-designation** only | **HIGH** |
| **RI-RS → Aura-Guard** | Identity assigned by URL; dedicated status document with Document ID `RI-RS`, Version `v1.3.0`. **Counter:** 0 occurrences of `RI-RS` in the designee, all history | `APS-950:133`; `reference/RI-RS_AURA_GUARD.md:1-7`; §5.1 | **CONFIRMED** *as designation only*; unacknowledged | **HIGH** (for the designation) |
| **POC-A → APS-200** | GAP-001 is the sole pre-audit reference and defines APS-200 as "ARI Engine", incompatible with the actual APS-200; self-declared as inferred without the spec | `GAP-001:202,209,417`; `APS-200:1` | **CONFLICT** (CONFLICT-DQ001H-01) | **HIGH** (that the conflict exists) |
| **RI-PY → APS-200** | Spec's own assessment: RI-001 "PARTIAL — no APS-200 canonical object headers"; RI-006 "PARTIAL — not APS-200 ENT-007"; RI-007 "no protocol_version" | `RI-PY_AURA_POC_A_CORE.md:22,27,28` | **MISSING** — expected by APS-950:23, no implementing evidence | **HIGH** |
| **RI-RS → APS-200** | Spec's own assessment: "no APS-200 canonical object headers" (`:22`), INV-003 "no APS-200 canonical object schema" (`:50`), INV-015 ❌ (`:62`), Key Gap "No canonical APS-200 data model objects" (`:74`), **NOT CERTIFIED** (`:7`) | `RI-RS_AURA_GUARD.md` | **MISSING** | **HIGH** |
| **Aura-Guard → APS-200** | `APS-` returns **0 files at HEAD and 0 commits in the entire history** of `aura-guard-v1.3`, all branches | `git grep`/`git log --all -S` | **MISSING** | **HIGH** |
| **AuditEntry → RI-PY** | `AuditEntry` never appeared in POC-A except in 10 Claude-authored audit commits from 2026-08-11. POC-A's audit object is `EventTrustCertificate` (`audit/merkle.py:20`, 2026-01-17), disjoint in fields and semantics | `git log --all -S"AuditEntry"` in POC-A; `03_LANGUAGE_BOUNDARY.md:49` | **NOT APPLICABLE** | **HIGH** |
| **AuditEntry → RI-RS** | `AuditEntry` is defined in `aura-guard-v1.3` (`src/models.rs:50`), which APS-950 §11 designates RI-RS. Transitive via the designation only; the guard never uses the term | `src/models.rs:50`; `APS-950:133` | **CONFIRMED** *transitively, via designation* | **MEDIUM** — depends entirely on the RI-RS designation holding |
| **AuditEntry → ENT-007** | No mapping, no adapter, no reference in either direction, in any repository, on any branch, at any time. `ENT-007`: 0 hits in the guard. The sole association is the DQ-001 analysis of 2026-08-15 | §5.1; §7.1 items 9-11; §12 | **MISSING** | **HIGH** |

---

## 11. Temporal lineage (Phase 9)

```
TIMELINE OF ARCHITECTURAL LINEAGE

2026-01-04  ┃ POC-A ORIGIN — aura-poc-a-core-v3.3 created (cae9363)
            ┃ merkle.py created (befddfa)
            ┃
2026-01-17  ┃ EventTrustCertificate introduced (80ec4ad)
            ┃   → POC-A's audit object. NOT AuditEntry.
            ┃
            ┃   ░░░ GAP: 116 days ░░░
            ┃   No Rust work. No Guard. No APS. No RI terminology.
            ┃
2026-05-13  ┃ AURA-GUARD ORIGIN — aura-guard-v1.3 created (36fd12f)
            ┃   ✗ no shared ancestor with POC-A
            ┃   ✗ no reference to POC-A in 105 commits, ever
            ┃ AUDITENTRY ORIGIN — d03eb65, 11 fields, "pure DTO module"
            ┃
            ┃   ░░░ GAP: 71 days ░░░
            ┃   AuditEntry exists. ENT-007 does not.
            ┃
2026-07-23  ┃ SPECIFICATION ORIGIN — aura-specification created (d2b12cd)
            ┃ Polish APS source documents uploaded (6f4d971, 792c43f)
            ┃ AuraProtocol org migration proposed (6ad45f3) … and
            ┃   withdrawn the same day (aeb6bab → 7a22522)
            ┃ ★ b68181e — ONE COMMIT creates simultaneously:
            ┃     • APS-200 ORIGIN + ENT-007 ORIGIN
            ┃     • RI-PY ORIGIN (designation of POC-A)
            ┃     • RI-RS ORIGIN (designation of Aura-Guard)
            ┃     • first conformance statement — and it is NEGATIVE:
            ┃       "NOT CERTIFIED", "No canonical APS-200 data model objects"
            ┃
2026-07-24  ┃ FIRST CROSS-REFERENCE (implementation → spec)
            ┃   POC-A GAP-001 (ef91cb1) cites APS-200 …
            ┃   ⚠ with INCOMPATIBLE NUMBERING — "APS-200 = ARI Engine"
            ┃   ⚠ self-declared as inferred; spec "not co-located here"
            ┃
2026-07-26  ┃ Guard adds request_id to AuditEntry (75f1052)
            ┃   → the one post-spec schema change; Common Object
            ┃     Contract NOT adopted
            ┃
2026-08-09  ┃ POC-A adds rust-conformance.instructions.md (d2ec66f)
            ┃   → governs **/*.rs; POC-A has zero .rs files
            ┃
2026-08-11  ┃ RI-PY / RI-RS / aura-guard terminology enters POC-A
            ┃   for the FIRST TIME (8db25b3) — inside a Claude audit package
2026-08-12  ┃ ENT-007 enters POC-A for the FIRST TIME (17c3916) — audit only
            ┃
2026-08-15  ┃ Guard's ONLY mention of sibling repos (6661982)
            ┃   — on UNMERGED branch d3/real-chain-fixture-export
            ┃ FIRST ADAPTER PROPOSAL anywhere in the ecosystem (e3e4732)
            ┃   — DQ-001 review, PROPOSED / NOT APPROVED
```

**Highlighted gaps.**

| Gap | Span | Significance |
|---|---|---|
| POC-A → Guard | **129 days**, no artifact bridges it | **FACT.** No derivation opportunity is evidenced |
| `AuditEntry` → ENT-007 | **71 days** | **FACT.** `AuditEntry` cannot have implemented a contract that did not exist. **INFERENCE:** Option A is historically impossible *as an origin account* |
| Designation → acknowledgement | **never closed** (388 days from POC-A origin to date of audit) | **FACT.** Neither designee has ever acknowledged its RI identity |
| ENT-007 → any mapping | **never closed** (23 days and counting) | **FACT.** No adapter existed before 2026-08-15, and the one that exists is a non-approved proposal |

---

## 12. Negative evidence (Phase 12)

All statements below are **"not found in inspected scope"**, never "does not exist".

| # | Searched for | Repositories | Branches / history | Method | Result |
|---|---|---|---|---|---|
| N-1 | `ENT-007` | `aura-guard-v1.3` | all branches, 105 commits | `git grep` @HEAD + `git log --all -S` | **0 files, 0 commits** |
| N-2 | `APS-` (any APS identifier) | `aura-guard-v1.3` | all branches, full history | same | **0 files, 0 commits** |
| N-3 | `RI-RS` | `aura-guard-v1.3` | all branches, full history | same | **0 files, 0 commits** — the designee never names itself |
| N-4 | `RI-PY` | `aura-guard-v1.3` | all branches, full history | same | **0 files, 0 commits** |
| N-5 | `RI-PY` / `RI-RS` | `aura-poc-a-core-v3.3` | `origin/main` excluding `review/` | `git grep -Il … -- ':!review/'` | **0 files** — present only in Claude audit packages from 2026-08-11 |
| N-6 | `adapter` (object/protocol sense) | `aura-specification` | all branches, full history | `grep -rni` over `*.md`/`*.json`/`*.yaml` | **0 occurrences repo-wide** — no normative adapter mechanism |
| N-7 | `adapter` (object/protocol sense) | `aura-guard-v1.3`, `aura-poc-a-core-v3.3` | HEAD + history | `git grep -Iin` | Only SIEM/WORM **storage** adapters (guard) and embedding→int32 **numeric** adapters (POC-A). **No object-mapping adapter** |
| N-8 | Mapping / conversion code `AuditEntry` ↔ any protocol object | `aura-guard-v1.3` | all `src/`, `tests/` | `git grep "AuditEntry"` — all 29 references enumerated | **None.** All references are construct / serialize / hash / persist / verify / Merkle-leaf |
| N-9 | Migration, succession, deprecation or handover ADR relating POC-A ↔ Guard | all three | all branches, full histories | commit-message scan + `docs/adrs/` + `adrs/` + `docs/` listing | **Not found** |
| N-10 | `port of`, `parity` | `aura-guard-v1.3` | all branches, full history | `git log --all -S` | **0 commits each** |
| N-11 | Shared conformance fixture or test vector between POC-A and Guard | both | HEAD + history | prior exhaustive audit + fixture-directory inspection | **Not found** — `03_LANGUAGE_BOUNDARY.md:54` "none shared" |
| N-12 | `RI-TEST` / "Reference Fixtures Runner" implementation | all three | all branches | file + term search | **Not found** — `APS-950:134` marks it **Planned**; no artifact |
| N-13 | `AuraProtocol` organization or its five named repositories | `aura-specification` HEAD; account repository listing | HEAD + history | `git grep`; `list_repos` | **0 hits at HEAD**; not in accessible listing. Proposal withdrawn 2026-07-23 |
| N-14 | Any commit in `aura-guard-v1.3` mainline referencing a sibling repository | `aura-guard-v1.3` | **mainline** (ancestors of HEAD) | `git log --all -S` + `merge-base --is-ancestor` | **0 in mainline.** The single hit (`6661982`) is on an unmerged branch |
| N-15 | Acknowledgement by either designee of its RI designation | POC-A, Guard | all branches, full histories | term search + README/docs review | **Not found in either repository** |
| N-16 | Any document defining APS-200 as "ARI Engine" other than GAP-001 | all three | all branches | `grep -rn "ARI Engine"` context review | **Not found** — the numbering has no second witness |

---

## 13. H1 / H2 / H3 evaluation (Phase 10)

### H1 — CONTINUOUS LINEAGE (POC-A/RI-PY → RI-RS/Aura-Guard → APS-200)

**REFUTED.**

- **FACT.** No derivation link POC-A → Guard: no shared ancestor, 129-day gap, zero
  cross-references in 105 guard commits, disjoint algorithms for every shared concern
  (§5.4).
- **FACT.** APS-200 did not emerge *from* the implementations — it was authored
  externally in Polish, imported in one day, and its first assessment of both designees
  was non-conformance (§8).
- **FACT.** The arrow direction is inverted: the chain's claimed *last* element
  (APS-200) is chronologically last, but a continuous lineage requires each stage to
  produce the next, and no stage produced any other.

### H2 — FORKED IMPLEMENTATION LINEAGE (independent evolution; APS-200 introduced later, requiring an adapter)

**BEST SUPPORTED, with one required correction.**

Supported:
- **FACT.** "Independent evolution" — exhaustively evidenced (§5, §12).
- **FACT.** "APS-200 was introduced later" — 71 days after `AuditEntry`, 200 days after
  POC-A began.
- **FACT.** "Requires an adapter" — consistent with the current state: no mapping exists
  in any repository, and the spec's own status documents record the object gap.

**Correction required.** The label **"forked"** overstates the relationship. A fork
implies a common origin that was divided; **no common origin is evidenced**. POC-A and
Aura-Guard have **independent origins**, not a shared one. The accurate statement is
*"independent origins, later co-designated"*.

### H3 — MULTI-LAYER ECOSYSTEM (APS-200 above an explicit contract, over RI-PY/POC-A and RI-RS/Aura-Guard)

**DESCRIBES THE DECLARED TARGET, NOT THE EVIDENCED HISTORY.**

- **FACT supporting it.** The two-branch structure is real and explicitly authored:
  APS-950 §11 designates both repositories as sibling RIs under APS, by URL, in the
  original source. H3's *shape* is the specification's own declared model.
- **FACT refuting it as history.** H3's load-bearing element is the "**explicit
  contract**" between APS-200 and the RIs. That contract is **not satisfied and never
  has been**: RI-RS is `NOT CERTIFIED` with "No canonical APS-200 data model objects";
  RI-PY's audit interface is "not APS-200 ENT-007"; `APS-200:224` still has no published
  JSON Schema; `APS-200:238` records **no CONF test** for ENT-007; and APS-200 remains
  `1.0-DRAFT`.

### Determination

**H2 (as corrected) is the best-supported account of what actually happened. H3 is the
best description of what APS-950 §11 declares should be true, and it is unrealized.**

**INFERENCE.** The two are not alternatives so much as different tenses: H2 is the
history; H3 is the target the specification asserted unilaterally on 2026-07-23. The gap
between them *is* the DQ-001 problem.

---

## 14. DQ-001 implications (Phase 11) and hard-stop assessment

### 14.1 Impact on DQ-001

**STRENGTHENS B.** Reasoning, held to the three-concept separation:

1. **Implementation lineage evidence removes A's origin account, but this was already
   known.** `AuditEntry` predates ENT-007 by 71 days (**FACT**), so it cannot have been
   authored as an ENT-007 implementation. This was already established in the DQ-001
   review; DQ-001-H corroborates it with the origin commits now visible post-unshallow.
   **It does not newly discriminate.**

2. **The genuinely new finding is that the normative lineage is real, explicit, and
   URL-bound.** APS-950 §11 designates `aura-guard-v1.3` as **RI-RS**, in the original
   authored source, with a dedicated status document. **FACT.** This *materially updates*
   **EG-8** of the DQ-001 review ("whether APS-200 binds `aura-guard-v1.3` at all is
   jurisdictionally unresolved"). A designation is not the same as accepted jurisdiction
   — and OQ-A-CONFLICT-001/002 remain open — but the ecosystem is no longer one in which
   the guard is simply outside the specification's declared reach. **This weakens the
   "no relationship is required" reading and therefore raises, not lowers, the need for
   *some* explicit binding.**

3. **Why B rather than A.** The designation binds the *repository* as a reference
   implementation; nothing in APS-950 §11, `RI-RS_AURA_GUARD.md`, or any commit binds the
   *internal DTO* to the *protocol object*. Combined with `APS-200:16` (internal
   structures MAY differ; semantics and contract MUST be equivalent — cited in the DQ-001
   review), a designation-level binding with a structure-level exemption is precisely an
   adapter boundary.

4. **Why B rather than C.** C's intermediate layer would be the natural home for the
   cross-RI convergence that `APS-200:218` calls for ("canonical serialization **for
   interoperability between RI-PY and RI-RS**"). **FACT:** that is an open TODO, and
   `RI-TEST` — the cross-implementation fixture runner that would exercise such a layer —
   is marked **Planned** and was never created (N-12). The lineage evidence shows the
   shared layer C presupposes has **never existed in any form**. C therefore remains a
   greenfield authoring act, exactly as the DQ-001 review concluded.

**Explicit guardrail compliance.**

- POC-A and Aura-Guard being separate layers is **NOT** treated here as establishing that
  they have separate normative contracts. APS-950 §11 designates **both** as RIs under
  **one** APS corpus — implementation separateness coexists with a single declared
  normative umbrella. The separateness argument is used only against *derivation*
  claims (H1), never to argue for separate contracts.
- RI-PY and RI-RS being co-designated is **NOT** treated as establishing that
  `AuditEntry` is ENT-007. §10 classifies `AuditEntry → ENT-007` as **MISSING** on
  direct evidence, independent of any designation.

**No DQ-001 decision is made, and no DQ-002…DQ-008 question is touched.**

### 14.2 Hard-stop conditions

| # | Condition | Triggered? | Disposition |
|---|---|---|---|
| 1 | A repository cannot be distinguished from another | **NO** | Two collision risks identified and resolved by evidence, not assumption: `aura-nomos/aura-specification` (empty; not the APS source) and the `Aura-IDToken` vs `AuraIDToken` fork pair (§2.2). Both recorded, neither collapsed |
| 2 | Git history incomplete in a way affecting the conclusion | **NO — after remediation** | `aura-poc-a-core-v3.3` was initially **shallow**, hiding 49 commits including the entire January 2026 origin. Unshallowed before any lineage claim; **disclosed in §0.2** |
| 3 | A cross-repository relationship exists only in an unverified external source | **PARTIALLY — recorded, not relied upon** | The `AuraProtocol` org and its five repositories are named only in a README revision that was **removed the same day**, with every status box unchecked, and are absent from the accessible listing. **Excluded from the lineage model** (§2.2, N-13); no conclusion rests on it |
| 4 | **Two authoritative sources give materially incompatible accounts** | **YES** | **CONFLICT-DQ001H-01** (§8.3): `GAP-001:207-217` assigns APS-100 = "Canonical Data Model" and APS-200 = "ARI Engine"; `aura-specification` assigns the reverse subject matter. GAP-001 self-declares its APS content as **inferred without the specification** (`:202`) while its header cites `spec-v0.1.0` (`:5`). **Reported, not reconciled.** Consequence: **any lineage or conformance claim resting on GAP-001's APS citations is invalid**, including `GAP-001:417`'s "APS-200 … Adapter" item, which concerns embedding→int32 conversion and not ENT-007 |
| 5 | Determining lineage would require a semantic protocol decision | **NO** | Every arrow was classified from designation records, commit history and term searches. No hash domain, serialization, event semantic, versioning or numeric question was decided |
| 6 | Evidence insufficient to distinguish implementation from normative lineage | **NO** | The two separate cleanly: implementation lineage is **absent** (N-1…N-11); normative lineage is **present and explicit** (APS-950 §11). Distinguishing them is the central result of this audit |

**Because condition 4 is triggered, DQ-001-H STATUS is reported as CONFLICT.** The
lineage reconstruction itself is complete and no arrow was left unclassified; the
conflict is localized to POC-A's APS numbering and does not propagate to any arrow other
than `POC-A → APS-200`.

---

## 15. Open questions

| ID | Question | Class | Owner |
|---|---|---|---|
| **LQ-1** | Is `GAP-001`'s APS numbering a superseded scheme or an ad-hoc construction? Should GAP-001 be corrected, annotated or withdrawn? | **CONFLICT** (CONFLICT-DQ001H-01) | Protocol Custodian / Architecture Owner |
| **LQ-2** | Do the RI-PY and RI-RS designations require acceptance by the designated repositories to take effect, and by what mechanism? No acceptance procedure was found in `GOVERNANCE.md`, APS-950 §12, or any ADR | **UNKNOWN** | Protocol Custodian |
| **LQ-3** | Is `aura-guard-v1.3`'s planned `EVIDENCE_SPEC v1.1` (v2.0/2027) intended to conform to, extend, or compete with APS-200/APS-300? No document relates them | **UNKNOWN** | Architecture Owner |
| **LQ-4** | The guard roadmap plans a *new* Python cross-language verifier while RI-PY already exists. Are these the same artifact? | **UNKNOWN** | Architecture Owner |
| **LQ-5** | Was the `AuraProtocol` organization migration abandoned, deferred, or completed elsewhere? | **UNKNOWN** | Architecture Owner |
| **LQ-6** | `RI-TEST` (Reference Fixtures Runner) is "Planned" and never created. Is cross-RI fixture validation still intended? Bears on `APS-200:218` and on C's feasibility | **UNKNOWN** | Protocol Custodian |
| **LQ-7** | POC-A README claims "FROZEN / CANONICAL" for the protocol; `aura-specification` claims to be "the single canonical source of truth". Which governs? | **CONFLICT** — pre-registered as OQ-A-CONFLICT-001/002; **not re-adjudicated here** | Protocol Custodian |
| **LQ-8** | Does the APS-950 §11 designation constitute accepted jurisdiction over `aura-guard-v1.3` for DQ-001 purposes? Materially updates but does not close **EG-8** | **UNKNOWN** | Protocol Custodian |

---

## 16. Evidence references

**Pinned revisions:** `aura-poc-a-core-v3.3` `98f2f43` (unshallowed, 276 commits) ·
`aura-guard-v1.3` `443f72e` (105 commits) · `aura-specification` `62d2d6b` (44 commits).

**Commits cited:** POC-A — `cae9363`, `befddfa`, `80ec4ad`, `ef91cb1`, `d2ec66f`,
`8db25b3`, `17c3916`, `f8ff209`, `e3e4732`. Guard — `36fd12f`, `d03eb65`, `75f1052`,
`9dd8757`, `56f7b64`, `c5e162e`, `6661982` (unmerged branch `d3/real-chain-fixture-export`).
Spec — `d2b12cd`, `6f4d971`, `792c43f`, `6ad45f3`, `aeb6bab`, `7a22522`, `6a33430`, `b68181e`.

**Files cited:** `aps/APS-200_CANONICAL_DATA_MODEL.md:16,149-159,218,224,238`;
`aps/APS-950_REFERENCE_IMPLEMENTATION_REQUIREMENTS.md:23,51,132,133,134`;
`APS-950 — Reference Implementation Requirements_260723_194507.txt:147-152`;
`APS-200 — Canonical Data Model_260723_192852.txt:59-60`;
`reference/RI-RS_AURA_GUARD.md:7,22,35,50,62,74`; `reference/RI-PY_AURA_POC_A_CORE.md:22,27,28`;
`aura-specification/README.md:3,13,17`; guard `src/models.rs:1-2,38,44-48,50`,
`docs/ROADMAP.md:62,67-68,78,80-83`, `README.md:8,169,288,304,366`, `SECURITY.md:66`,
`docs/adrs/0001-hash-chain.md:3`, `docs/ARCHITECTURE.md:1-13`, `src/tst_verify.rs:685`;
POC-A `README.md:1,13-17,23,38,279-284`, `docs/architecture.md:1-16`, `audit/merkle.py:20`,
`docs/GAP-001.md:5,200-217,364,405-420,417,662`,
`core/test_ari_observability.py:135`, `.github/instructions/rust-conformance.instructions.md`,
`review/2026-08-11_ENGINEERING_BASELINE/03_LANGUAGE_BOUNDARY.md:21-54`,
`review/2026-08-12_OQ-A_GOVERNANCE_JURISDICTION/10_CONFLICT_REGISTER.md`,
`review/2026-08-15_D3-S4_DQ-001_ADAPTER_ARCHITECTURE/`.

---

## 17. Declarations

- **No production source code was modified** in any repository.
- **No protocol, APS, SPEC or ADR document was modified.** `aura-guard-v1.3` and
  `aura-specification` were **read only**; neither was written to and neither can be
  pushed to from this session.
- **No test, fixture, serialization, hash or API surface was changed.**
- **No DQ-001 decision was made.** DQ-002 … DQ-008 are untouched and remain OPEN.
- **No ADR was approved, filed or numbered. No PR was opened. No merge, no freeze.**
- The only change produced by this audit is this single forensic review artifact.
