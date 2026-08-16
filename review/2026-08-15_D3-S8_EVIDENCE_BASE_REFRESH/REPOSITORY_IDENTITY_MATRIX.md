# REPOSITORY_IDENTITY_MATRIX — D3-S8

**Phase 0.** Every value below was produced by an executed `git` command against the live
clone, not carried from prior analysis. **Normative effect: NONE.**

## 1. Matrix

| Repository | Remote (verified) | Branch | HEAD | History complete? | Earliest commit | Relevant paths | Role in Aura ecosystem |
|---|---|---|---|---|---|---|---|
| `aura-poc-a-core-v3.3` | `https://github.com/AuraIDToken/aura-poc-a-core-v3.3` | `claude/auditentry-adapter-dq-001-h0os71` | `a0c4901` | **YES** — `is-shallow-repository=false`, 279 commits | `cae9363` 2026-01-04 "Initial commit" | `core/`, `audit/`, `compliance/`, `docs/`, `review/` | Python measurement engine. **Designated RI-PY** by `APS-950:132` |
| `aura-guard-v1.3` | `https://github.com/AuraIDToken/aura-guard-v1.3` | `main` | `443f72e` | **YES** — false, 105 commits | `36fd12f` 2026-05-13 "Initial commit" | `src/`, `tests/`, `docs/` | Rust audit middleware. **Designated RI-RS** by `APS-950:133` |
| `aura-specification` | `https://github.com/AuraIDToken/aura-specification` | `main` | `62d2d6b` | **YES** — false, 44 commits | `d2b12cd` 2026-07-23 "Initial commit" | `aps/`, `specification/`, `invariants/`, `conformance/`, `fixtures/`, `constitution/`, `reference/` | **The APS corpus.** Source of APS-000…950, SPEC-002, Constitution |
| `aura-nomos/aura-specification` | `https://github.com/aura-nomos/aura-specification` | `claude/auditentry-adapter-dq-001-h0os71` | `eb2a4ec` | YES — 3 commits total | `9250853` 2026-07-24 "Initial commit" | `README.md`, `.github/CODEOWNERS` **only** | **NOT the specification repository.** See §2 |

## 2. Repository-identity hazard — verified, not assumed

**FACT.** The repository attached to this Claude session under the name
`aura-specification` is **`aura-nomos/aura-specification`**, verified by
`git remote get-url origin`. Its complete content across all branches and its entire
3-commit history is `README.md` (one line: `# aura-specification`) and
`.github/CODEOWNERS`.

**FACT.** It contains **no APS document, no SPEC-002, no Constitution, no invariant
registry.**

**FACT.** The APS corpus used as evidence throughout D3-S8 is
**`AuraIDToken/aura-specification`**, a different repository under a different owner,
attached via `add_repo` and cloned read-only to
`/workspace/auraidtoken/aura-specification`.

**INFERENCE.** Any analysis that had accepted the session-attached repository as the
specification source would have concluded that APS-200 and ENT-007 do not exist. The
D3-S8 instruction to verify repository identity before using any document as evidence is
therefore load-bearing, and the verification changes the outcome.

## 3. Aliases, renames and moves

| Candidate | Finding | Evidence |
|---|---|---|
| `AuraIDToken/aura-poc-a-core` (unversioned) | **Not present** in the account's accessible repository listing. `APS-950:132` names the implementation unversioned and resolves it by hyperlink to the `-v3.3` repository | repository listing; `APS-950:132` |
| `Aura-IDToken/aura-poc-a-core-v3.3` | **A GitHub fork** under a differently-spelled owner org (`Aura-IDToken` vs `AuraIDToken`). Merge commits in the mainline originate from both spellings (e.g. `f54494c` "…from Aura-IDToken/…", `ca3e4b9` "…from AuraIDToken/…") | `git log` |
| `AuraProtocol/*` (5 repositories) | **Named but unrealized.** Proposed in `aura-specification` README at `6ad45f3` (2026-07-23) with all six migration checkboxes unchecked; note edited (`aeb6bab`) then **removed** (`7a22522`) the same day. `AuraProtocol` occurs **0 times** at HEAD. Not in the accessible listing | `git log -S"AuraProtocol"` |
| Repository renames/moves affecting the three primary repositories | **None found in inspected scope** | remote URLs verified above |

## 4. Branches relevant to evidence

| Repository | Branch | Relevance |
|---|---|---|
| `aura-guard-v1.3` | `main` @ `443f72e` | Primary implementation evidence |
| `aura-guard-v1.3` | `d3/real-chain-observability` @ `70b9881` | **Not an ancestor of `main`.** Carries `D3_REAL_CHAIN_CANONICAL.bin` — the only exported canonical byte stream in the ecosystem |
| `aura-guard-v1.3` | `d3/real-chain-fixture-export` @ `6661982` | **Not an ancestor of `main`.** Reconnaissance/blocker report |
| `aura-poc-a-core-v3.3` | `origin/main` @ `98f2f43` | Baseline for all POC-A citations |
| `aura-poc-a-core-v3.3` | `claude/auditentry-adapter-dq-001-h0os71` @ `a0c4901` | Working branch; carries only `review/` artifacts ahead of `main` |

## 5. History-completeness disclosure

**FACT.** `aura-poc-a-core-v3.3` was originally cloned **shallow** (227 commits
reachable). It was unshallowed during D3-S4/DQ-001-H, revealing **279 commits** — the
entire January 2026 origin period had been absent. Re-verified at D3-S8:
`is-shallow-repository=false`.

**FACT.** `aura-guard-v1.3` and `aura-specification` were cloned with full history and
report `false`; neither required unshallowing.

**INFERENCE.** All D3-S8 history claims rest on complete histories. Any DQ finding dated
before the unshallow that depended on POC-A's early history would have been derived from
a truncated record.
