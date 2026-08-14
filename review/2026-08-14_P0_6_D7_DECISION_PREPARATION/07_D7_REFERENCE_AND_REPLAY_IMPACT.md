# 07 — D-7 Reference Model and Replay / Verifier Impact

Analysis only. No implementation, no reference-model artifact, no reporting
contract selected.

---

## 1. Reference-model impact

**CONFIRMED.** The D-3/D-4 package scoped six reference-model elements and
assigned one of them to D-7 explicitly:
`review/2026-08-14_P0_6_D3_D4_DECISION_PREPARATION/09_…` §4 lists
**"Version selection — how a verifier determines which representation applies to
a given record — Depends on: D-7, not D-3/D-4."**

| Reference-model element | Owner | D-7's contribution |
|---|---|---|
| Mathematical definition | D-2, D-3 | None |
| Canonical representation | D-3 | None — but D-3 must be able to express a generation marker if a marker-bearing candidate is chosen (`05_…` E-03) |
| Collection semantics | D-4 | None |
| Test vectors | D-3, D-4 | **Per-generation vectors** — vectors are only meaningful once it is stated which generation they exercise |
| Expected digest | D-3, D-4 | Same qualification |
| **Version selection** | **D-7** | **The whole element** |

**What D-7 must eventually supply to the reference model** — listed, **not
specified here**:

1. the distinguishing property and its location;
2. its protection status;
3. the selection algorithm a conforming verifier follows;
4. defined behaviour for absent / unknown / malformed / newer / older;
5. the boundary definition (jointly with D-5);
6. the reporting contract for each outcome (jointly with D-6).

**INFERENCE.** Items 1–4 are D-7's alone; items 5–6 are shared. None can be
written before D-7 closes, and item 4 additionally depends on EG-1
(`06_…` §1).

## 2. Replay / verifier impact

### 2.1 What replay does today — CONFIRMED

| Stage | Call | Cite |
|---|---|---|
| Parse | `read_all_entries` → `serde_json::from_str` per line, no schema inspection | `src/log_writer.rs:151–170` |
| Chain | `verify_chain` — unconditional; exit `2` on break | `src/bin/aura_replay.rs:113–119` |
| Lineage | optional `--verify-lineage`; exit `3` on mismatch | `:134–153` |
| Segment chain | `verify_segment_chain` | `:175` |
| Manifest ↔ entries | `verify_manifest_against_entries` | `:194` |
| Success output | prints `CHAIN OK — head_chain_hash: {head}` | `:213` |

**No branch anywhere depends on a version input** — CONFIRMED.

### 2.2 Where rule selection could sit

**NON-NORMATIVE CANDIDATES**, unranked:

| Location | Consequence |
|---|---|
| Inside `verify_chain` (library) | Every embedder inherits selection automatically; the library's public signature (`verify_chain(&[AuditEntry])`, `src/chain.rs:71`) carries no place to pass a generation, so either the signature changes or selection becomes implicit |
| Inside `recompute_for_entry` (per entry) | Enables mixed-generation files at the finest granularity; hides the choice from callers |
| In the CLI only | Library users remain unversioned — a divergence between the two consumer classes |
| Supplied by the caller | Precedented: `aura-seal verify-tst` takes mode from `--tsa-roots` (`src/bin/aura_seal.rs:338–365`) — CONFIRMED |

**INFERENCE.** The choice determines who bears the versioning burden. It is not
purely internal: `verify_chain` is a public library entry point.

### 2.3 Reporting consequences

**CONFIRMED.** `docs/exit-codes.md` defines `0,1,2,3,4,5,6,78` and is framed as
"the contract that SOC playbooks, supervisors and CI should be wired against"
(quotation). It contains **no** version- or schema-mismatch code.

Conditions that every D-7 candidate can produce, and which the present contract
cannot express distinctly:

| Condition | Today's outcome | Cite |
|---|---|---|
| Legacy entry under a new-only verifier | exit `2` — "chain break", i.e. reported as tampering | `:113–119`; `docs/exit-codes.md` |
| Unknown generation | no code exists | `docs/exit-codes.md` |
| Malformed / missing field | exit `1` — "runtime error / malformed log" | `src/log_writer.rs:163–166` |
| Log spans a generation boundary | undefined | — |
| Verified, but under which generation? | `CHAIN OK` says nothing about the rule | `:213` |

**CONFIRMED — the diagnostic mis-naming.** A structural generation mismatch
surfaces through the **parse** path as exit `1` ("malformed log"), not through
the integrity path as exit `2`. An operator following the documented contract
would triage a version problem as file corruption.

**Precedent for a softer approach — CONFIRMED.** When the project previously
introduced a stronger verification mode, it did **not** add an exit code: it kept
the weaker mode available, selected it by flag absence, and emitted a stderr
warning naming the weaker posture (`src/bin/aura_seal.rs:365`;
`docs/segments-and-timestamping.md §Backward-compatible imprint-only mode`).
Recorded as an existing pattern in this codebase, **not** as a proposal.

### 2.4 Handover to D-6

These reporting questions belong to **D-6**, which is OPEN. D-7 determines *which
conditions can arise*; D-6 determines *how each is reported*. This package does
not select an exit code, a message, or a reporting policy.

## 3. Library-consumer impact

**CONFIRMED.** `verify_chain` and `recompute_for_entry` are `pub`
(`src/chain.rs:53`, `:71`), as are the segment verification functions
(`src/segment.rs:335`, `:382`). Any generation selection placed inside them
changes behaviour for every consumer of the library, not only for the CLI.

**EVIDENCE GAP (G-2).** Whether such consumers exist outside the repository is
not determinable here.
